"""Server dashboard Pumpkin Terminal — hanya stdlib, nol dependensi.

    python run.py serve --port 8000

Endpoint:
    GET  /                 dashboard
    GET  /api/state        snapshot JSON
    GET  /api/stream       Server-Sent Events (dashboard memakai ini)
    POST /api/control      {"action": "start|pause|reset", "speed": 0.5..8}
    GET  /api/report       laporan sesi (JSON)
    GET  /api/report.md    laporan sesi (Markdown)
"""

from __future__ import annotations

import json
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from .config import Config
from .engine import Desk
from .report import build_report, write_report

STATIC = Path(__file__).resolve().parent / "static"


class Session:
    """Satu sesi paper trading yang berjalan di thread sendiri."""

    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.lock = threading.RLock()
        self.desk: Desk | None = None
        self.paused = False
        self.speed = cfg.sim.speed
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self._event_cursor = 0
        self._session_no = 0
        self._finished_at: float | None = None
        self.new_session()

    # ------------------------------------------------------------------ life
    def new_session(self) -> None:
        with self.lock:
            if self.desk is not None:
                self.desk.scribe.close()
            self._session_no += 1
            # tiap sesi baru memakai pasar yang berbeda — bukan mengulang seed yang sama
            self.cfg.sim.seed += 1013
            self.desk = Desk(self.cfg)
            self.paused = False
            self._finished_at = None
            self._event_cursor = self.desk.scribe.total
        if self._thread is None or not self._thread.is_alive():
            self._thread = threading.Thread(target=self._loop, daemon=True)
            self._thread.start()

    def _loop(self) -> None:
        while not self._stop.is_set():
            t0 = time.time()
            if not self.paused:
                with self.lock:
                    if self.desk and not self.desk.finished:
                        self.desk.tick()
                    elif self.desk and self.desk.finished:
                        if self._finished_at is None:
                            self._finished_at = time.time()
                        elif time.time() - self._finished_at > 8.0:
                            # lanjut otomatis ke sesi berikutnya (pasar berbeda)
                            self.new_session()
            target = self.cfg.sim.tick_seconds_wall / max(0.1, self.speed)
            time.sleep(max(0.0, target - (time.time() - t0)))

    def stop(self) -> None:
        self._stop.set()

    # -------------------------------------------------------------- payloads
    def snapshot(self) -> dict:
        with self.lock:
            d = self.desk.snapshot()
            events = [e.public() for e in d_events(self.desk, self._event_cursor)]
            self._event_cursor = self.desk.scribe.total
        d["events"] = events
        d["paused"] = self.paused
        d["speed"] = self.speed
        return d


def d_events(desk: Desk, cursor: int):
    """Ambil event baru sejak cursor (dibatasi 60 per payload)."""
    buf = list(desk.scribe.buffer)
    total = desk.scribe.total
    start_in_buf = max(0, len(buf) - (total - cursor))
    if total - cursor > len(buf):
        start_in_buf = 0
    return buf[start_in_buf:][-60:]


class Handler(BaseHTTPRequestHandler):
    session: Session

    def log_message(self, *args):  # senyap
        pass

    # ------------------------------------------------------------------ util
    def _send(self, code: int, body: bytes, ctype: str = "application/json",
              extra: dict | None = None) -> None:
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-store")
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        try:
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def _json(self, obj, code: int = 200) -> None:
        self._send(code, json.dumps(obj, ensure_ascii=False).encode(), "application/json")

    # ------------------------------------------------------------------- get
    def do_GET(self) -> None:  # noqa: N802
        path = self.path.split("?")[0]
        if path in ("/", "/index.html"):
            f = STATIC / "index.html"
            if not f.exists():
                return self._send(404, b"dashboard belum ada", "text/plain")
            return self._send(200, f.read_bytes(), "text/html; charset=utf-8")
        if path == "/api/state":
            return self._json(self.session.snapshot())
        if path == "/api/stream":
            return self._stream()
        if path == "/api/report":
            with self.session.lock:
                return self._json(build_report(self.session.desk))
        if path == "/api/report.md":
            with self.session.lock:
                desk = self.session.desk
            jpath, mpath = write_report(desk)
            return self._send(200, mpath.read_bytes(), "text/markdown; charset=utf-8",
                              {"Content-Disposition": f'attachment; filename="pumpkin-{desk.session_id}.md"'})
        if path == "/healthz":
            return self._json({"ok": True})
        return self._send(404, b"not found", "text/plain")

    def _stream(self) -> None:
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
        self.send_header("Cache-Control", "no-cache, no-transform")
        self.send_header("Connection", "keep-alive")
        self.send_header("X-Accel-Buffering", "no")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        try:
            self.wfile.write(b": connected\n\n")
            self.wfile.flush()
            while True:
                payload = self.session.snapshot()
                self.wfile.write(b"data: " + json.dumps(payload, ensure_ascii=False).encode() + b"\n\n")
                self.wfile.flush()
                time.sleep(0.3)
        except (BrokenPipeError, ConnectionResetError, OSError):
            return

    # ------------------------------------------------------------------ post
    def do_POST(self) -> None:  # noqa: N802
        path = self.path.split("?")[0]
        length = int(self.headers.get("Content-Length") or 0)
        try:
            body = json.loads(self.rfile.read(length) or b"{}")
        except json.JSONDecodeError:
            body = {}
        if path != "/api/control":
            return self._send(404, b"not found", "text/plain")
        if self.headers.get("Content-Type", "").startswith("text/plain"):
            pass
        action = body.get("action", "")
        s = self.session
        if action == "pause":
            s.paused = True
        elif action == "start":
            s.paused = False
        elif action == "reset":
            s.new_session()
        elif action == "speed":
            s.speed = max(0.25, min(16.0, float(body.get("speed", 1.0))))
        else:
            return self._json({"error": "action tidak dikenal"}, 400)
        return self._json({"ok": True, "paused": s.paused, "speed": s.speed})

    def do_OPTIONS(self) -> None:  # noqa: N802
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


def serve(host: str = "0.0.0.0", port: int = 8000, cfg: Config | None = None) -> None:
    cfg = cfg or Config()
    Handler.session = Session(cfg)
    httpd = ThreadingHTTPServer((host, port), Handler)
    httpd.daemon_threads = True
    print(f"\n  PUMPKIN TERMINAL · http://{host}:{port}")
    print(f"  mode={cfg.sim.edge_mode} · saldo ${cfg.sim.start_balance:,.2f} · "
          f"{cfg.sim.ticks:,} tick · paper trading (tidak ada wallet)\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n  berhenti.")
    finally:
        Handler.session.stop()
        httpd.server_close()
