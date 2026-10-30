"""Server dashboard — dua desk, satu proses, stdlib saja.

    /            Pumpkin Terminal (scan semua pair)
    /whale       Whale Radar (mengikuti aliran dompet whale)

Endpoint generik per desk:
    GET  /api/<desk>/state        snapshot JSON
    GET  /api/<desk>/stream       Server-Sent Events
    POST /api/<desk>/control      {"action": "start|pause|reset|speed"}
    GET  /api/<desk>/report.md    unduh laporan
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
from .social_desk import SocialDesk, write_social_report
from .whale_desk import WhaleDesk, write_whale_report

STATIC = Path(__file__).resolve().parent / "static"


class BaseSession:
    desk_name = "scan"

    def __init__(self) -> None:
        self.lock = threading.RLock()
        self.paused = False
        self.speed = 1.0
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self._cursor = 0
        self._finished_at: float | None = None
        self._started = False

    # anak kelas mengisi ini
    def make_desk(self):  # pragma: no cover - abstrak
        raise NotImplementedError

    def tick_delay(self) -> float:  # pragma: no cover - abstrak
        return 0.1

    def new_session(self) -> None:
        with self.lock:
            if getattr(self, "desk", None) is not None:
                self.desk.scribe.close()
            self.desk = self.make_desk()
            self.paused = False
            self._cursor = self.desk.scribe.total
            self._finished_at = None
        if not self._started:
            self._started = True
            self._thread = threading.Thread(target=self._loop, daemon=True)
            self._thread.start()

    def _loop(self) -> None:
        while not self._stop.is_set():
            t0 = time.time()
            if not self.paused:
                with self.lock:
                    if not self.desk.finished:
                        self.desk.tick()
                    elif self._finished_at is None:
                        self._finished_at = time.time()
                    elif time.time() - self._finished_at > 8.0:
                        self.new_session()
            time.sleep(max(0.0, self.tick_delay() / max(0.1, self.speed) - (time.time() - t0)))

    def stop(self) -> None:
        self._stop.set()

    def snapshot(self) -> dict:
        with self.lock:
            d = self.desk.snapshot()
            events = [e.public() for e in self._new_events()]
            self._cursor = self.desk.scribe.total
        d["events"] = events
        d["paused"] = self.paused
        d["speed"] = self.speed
        return d

    def _new_events(self):
        buf = list(self.desk.scribe.buffer)
        total = self.desk.scribe.total
        start = max(0, len(buf) - (total - self._cursor))
        if total - self._cursor > len(buf):
            start = 0
        return buf[start:][-60:]


class ScanSession(BaseSession):
    desk_name = "scan"

    def __init__(self, cfg: Config):
        super().__init__()
        self.cfg = cfg
        self.speed = cfg.sim.speed
        self.new_session()

    def make_desk(self):
        # tiap sesi baru = pasar berbeda
        self.cfg.sim.seed += 1013
        return Desk(self.cfg)

    def tick_delay(self):
        return self.cfg.sim.tick_seconds_wall


class WhaleSession(BaseSession):
    desk_name = "whale"

    def __init__(self, cfg: Config):
        super().__init__()
        self.cfg = cfg
        self.speed = cfg.whale_sim.speed
        self.new_session()

    def make_desk(self):
        self.cfg.whale_sim.seed += 733
        return WhaleDesk(self.cfg.whale_sim, self.cfg.whale, self.cfg.scalp)

    def tick_delay(self):
        return self.cfg.whale_sim.tick_seconds_wall

    def report_md(self) -> Path:
        with self.lock:
            _, md = write_whale_report(self.desk)
        return md


class SocialSession(BaseSession):
    desk_name = "social"

    def __init__(self, cfg: Config):
        super().__init__()
        self.cfg = cfg
        self.speed = cfg.social_sim.speed
        self.new_session()

    def make_desk(self):
        self.cfg.social_sim.seed += 977      # tiap sesi baru = pasar berbeda
        return SocialDesk(self.cfg.social_sim, self.cfg.social)

    def tick_delay(self):
        return self.cfg.social_sim.tick_seconds_wall

    def report_md(self) -> Path:
        with self.lock:
            _, md = write_social_report(self.desk)
        return md


class Handler(BaseHTTPRequestHandler):
    sessions: dict[str, BaseSession] = {}

    def log_message(self, *args):
        pass

    # ------------------------------------------------------------------ util
    def _send(self, code, body: bytes, ctype="application/json", extra=None):
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

    def _json(self, obj, code=200):
        self._send(code, json.dumps(obj, ensure_ascii=False).encode())

    def _page(self, name: str):
        f = STATIC / name
        if not f.exists():
            return self._send(404, b"halaman belum ada", "text/plain")
        self._send(200, f.read_bytes(), "text/html; charset=utf-8")

    def _parse(self):
        """/api/<desk>/<action> → (desk, action)"""
        parts = self.path.split("?")[0].strip("/").split("/")
        if len(parts) >= 3 and parts[0] == "api":
            desk = "scan" if parts[1] == "scan" else parts[1]
            return desk, parts[2]
        return None, None

    # ------------------------------------------------------------------- get
    def do_GET(self):  # noqa: N802
        try:
            return self._route_get()
        except Exception as exc:  # jangan biarkan satu bug mematikan koneksi
            import traceback
            traceback.print_exc()
            return self._json({"error": str(exc)}, 500)

    def _route_get(self):
        path = self.path.split("?")[0]
        if path in ("/", "/index.html"):
            return self._page("index.html")
        if path in ("/whale", "/whale.html"):
            return self._page("whale.html")
        if path in ("/social", "/social.html"):
            return self._page("social.html")
        if path == "/healthz":
            return self._json({"ok": True, "desks": list(self.sessions)})

        desk, action = self._parse()
        if desk not in self.sessions:
            return self._send(404, b"not found", "text/plain")
        session = self.sessions[desk]

        if action == "state":
            return self._json(session.snapshot())
        if action == "stream":
            return self._stream(session)
        if action == "report.md":
            if desk in ("whale", "social"):
                p = session.report_md()
            else:
                with session.lock:
                    _, p = write_report(session.desk)
            return self._send(200, p.read_bytes(), "text/markdown; charset=utf-8",
                              {"Content-Disposition": f'attachment; filename="{p.name}"'})
        return self._send(404, b"not found", "text/plain")

    def _stream(self, session: BaseSession):
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
                payload = session.snapshot()
                self.wfile.write(b"data: " + json.dumps(payload, ensure_ascii=False).encode() + b"\n\n")
                self.wfile.flush()
                time.sleep(0.3)
        except (BrokenPipeError, ConnectionResetError, OSError):
            return

    # ------------------------------------------------------------------ post
    def do_POST(self):  # noqa: N802
        desk, action = self._parse()
        length = int(self.headers.get("Content-Length") or 0)
        try:
            body = json.loads(self.rfile.read(length) or b"{}")
        except json.JSONDecodeError:
            body = {}
        if desk not in self.sessions or action != "control":
            return self._send(404, b"not found", "text/plain")
        s = self.sessions[desk]
        act = body.get("action", "")
        if act == "pause":
            s.paused = True
        elif act == "start":
            s.paused = False
        elif act == "reset":
            s.new_session()
        elif act == "speed":
            s.speed = max(0.25, min(16.0, float(body.get("speed", 1.0))))
        else:
            return self._json({"error": "action tidak dikenal"}, 400)
        return self._json({"ok": True, "paused": s.paused, "speed": s.speed})

    def do_OPTIONS(self):  # noqa: N802
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


def serve(host: str = "0.0.0.0", port: int = 8000, cfg: Config | None = None) -> None:
    cfg = cfg or Config()
    Handler.sessions = {"scan": ScanSession(cfg), "whale": WhaleSession(cfg),
                        "social": SocialSession(cfg)}
    httpd = ThreadingHTTPServer((host, port), Handler)
    httpd.daemon_threads = True
    print(f"\n  PUMPKIN TERMINAL · http://{host}:{port}")
    print(f"  /       scan desk   · mode={cfg.sim.edge_mode}")
    print(f"  /social social radar · pasar={cfg.social_sim.mode} · "
          f"p̂≥{cfg.social.min_p_win:.2f} · target {cfg.social.min_tp*100:.0f}-"
          f"{cfg.social.max_tp*100:.0f}%")
    print(f"  /whale  whale radar · mode={cfg.whale_sim.edge_mode} · "
          f"{cfg.scalp.position_pct*100:.0f}% per posisi · target +{cfg.scalp.take_profit_pct*100:.0f}%")
    print(f"  paper trading murni — tidak ada wallet, tidak ada order on-chain\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n  berhenti.")
    finally:
        for s in Handler.sessions.values():
            s.stop()
        httpd.server_close()
