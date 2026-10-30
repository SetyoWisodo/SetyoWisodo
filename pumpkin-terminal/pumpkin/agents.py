"""Enam agen Pumpkin Terminal.

SCOUT   → menerima setiap pair baru dari feed
FILTER  → aturan keras: likuiditas, holder, distribusi, wallet dev, keamanan kontrak
ANALYST → skor komposit 0..1, hanya lolos kalau >= min_score
SNIPER  → eksekusi, ukuran posisi maksimal 8% saldo per posisi
GUARD   → stop-loss -6%, trailing setelah +12%, batas waktu
SCRIBE  → mencatat semua keputusan (termasuk penolakan)
"""

from __future__ import annotations

import json
import math
import threading
from collections import deque
from pathlib import Path

from .config import FilterRules, RiskRules
from .models import Event, Position, Token


def _clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


class Agent:
    name = "AGENT"

    def __init__(self) -> None:
        self.counts: dict[str, int] = {}
        self.last: str = ""
        self.notes: deque[str] = deque(maxlen=3)

    def bump(self, key: str, n: int = 1) -> None:
        self.counts[key] = self.counts.get(key, 0) + n

    def say(self, msg: str) -> None:
        self.last = msg
        self.notes.appendleft(msg)

    def stats(self) -> dict:
        return {"name": self.name, "counts": dict(self.counts), "last": self.last}


class Scout(Agent):
    """Menemukan pair baru. Tidak menilai apa pun — hanya inventarisasi."""

    name = "SCOUT"

    def __init__(self) -> None:
        super().__init__()
        self.seen: set[str] = set()

    def ingest(self, tok: Token) -> bool:
        if tok.address in self.seen:
            self.bump("duplikat")
            return False
        self.seen.add(tok.address)
        self.bump("scanned")
        self.say(f"{tok.symbol} terdeteksi · liq ${tok.liquidity_usd:,.0f}")
        return True


class Filter(Agent):
    """Aturan keras. Satu saja gagal → token mati di sini."""

    name = "FILTER"

    def __init__(self, rules: FilterRules) -> None:
        super().__init__()
        self.r = rules

    def check(self, tok: Token) -> tuple[bool, str]:
        r = self.r
        if tok.liquidity_usd < r.min_liquidity_usd:
            return self._reject("likuiditas_tipis", f"liq ${tok.liquidity_usd:,.0f} < ${r.min_liquidity_usd:,.0f}")
        if tok.holders < r.min_holders:
            return self._reject("holder_sedikit", f"{tok.holders} holder < {r.min_holders}")
        if tok.top10_pct > r.max_top10_pct:
            return self._reject("top10_terlalu_besar", f"top10 {tok.top10_pct:.1f}% > {r.max_top10_pct:.0f}%")
        if tok.dev_pct > r.max_dev_pct:
            return self._reject("wallet_dev_besar", f"dev {tok.dev_pct:.1f}% > {r.max_dev_pct:.0f}%")
        if r.require_mint_revoked and not tok.mint_revoked:
            return self._reject("mint_authority_aktif", "mint authority belum dicabut")
        if r.require_lp_locked and not tok.lp_locked:
            return self._reject("lp_tidak_terkunci", "LP tidak terkunci/burn")
        if tok.age_ticks < r.min_age_ticks:
            return self._reject("terlalu_baru", f"umur {tok.age_ticks} tick")
        self.bump("lolos")
        self.say(f"{tok.symbol} lolos semua aturan")
        return True, "lolos"

    def _reject(self, reason: str, detail: str) -> tuple[bool, str]:
        self.bump("ditolak")
        self.bump(f"alasan:{reason}")
        self.say(f"{reason} · {detail}")
        return False, reason


class Analyst(Agent):
    """Skor komposit. Hanya atribut publik — tidak melihat archetype laten."""

    name = "ANALYST"

    W_LIQ, W_HOLD, W_DIST, W_DEV, W_SAFE, W_MOM, W_VOL = (
        0.13, 0.10, 0.13, 0.08, 0.12, 0.38, 0.06,
    )
    LATE_PENALTY_FROM = 45.0   # change_5_pct di atas ini = sudah terbang

    def __init__(self, min_score: float, edge_mode: str = "correlated") -> None:
        super().__init__()
        self.min_score = min_score
        self.edge_mode = edge_mode

    def score(self, tok: Token) -> float:
        if self.edge_mode == "null":
            # Kontrol: skor acak, tidak berkorelasi dengan kualitas asli.
            # Dipakai untuk membuktikan bahwa profit bisa datang dari generator,
            # bukan dari strategi.
            return (hash(tok.address) % 10_000) / 10_000.0

        liq = _clamp(math.log10(max(tok.liquidity_usd, 1) / 1_000) / 2.0)
        hold = _clamp(math.log10(max(tok.holders, 1) / 100) / 1.5)
        dist = _clamp((40.0 - tok.top10_pct) / 25.0)
        dev = _clamp((10.0 - tok.dev_pct) / 10.0)
        safe = 0.5 * float(tok.mint_revoked) + 0.5 * float(tok.lp_locked)
        # momentum: akumulasi sehat = bagus; sudah vertikal = kita exit liquidity
        mom = _clamp((tok.change_5_pct + 3.0) / 16.0)
        if tok.change_5_pct > self.LATE_PENALTY_FROM:
            mom *= 0.25
        vol = _clamp(tok.volume_usd / max(tok.liquidity_usd, 1.0) / 3.0)
        return (
            self.W_LIQ * liq + self.W_HOLD * hold + self.W_DIST * dist
            + self.W_DEV * dev + self.W_SAFE * safe + self.W_MOM * mom
            + self.W_VOL * vol
        )

    def probe(self, tok: Token) -> float:
        """Skor tanpa mencatat aktivitas (dipakai saat memantau watchlist)."""
        return self.score(tok)

    def evaluate(self, tok: Token, count: bool = True) -> tuple[bool, float]:
        s = self.score(tok)
        if s < self.min_score:
            if count:
                self.bump("tolak_skor")
            return False, s
        self.bump("lolos")
        self.say(f"{tok.symbol} skor {s:.2f} ✓")
        return True, s


class Sniper(Agent):
    """Menentukan ukuran posisi. Tidak pernah melebihi aturan risiko."""

    name = "SNIPER"

    def __init__(self, rules: RiskRules) -> None:
        super().__init__()
        self.r = rules

    def size(self, balance: float, tok: Token) -> tuple[float, str]:
        cap_balance = balance * self.r.max_position_pct
        cap_liq = tok.liquidity_usd * self.r.max_pct_of_liquidity
        usd = min(cap_balance, cap_liq)
        if usd < 1.0:
            self.bump("dilewati")
            return 0.0, "likuiditas terlalu tipis untuk ukuran minimum"
        if usd < cap_balance - 0.01:
            self.bump("dikecilkan_likuiditas")
        self.bump("siap")
        return usd, "ok"

    def confirm(self, tok: Token, usd: float) -> None:
        self.bump("entry")
        self.say(f"BELI {tok.symbol} ${usd:,.2f}")


class Guard(Agent):
    """Mengawasi posisi terbuka dan memutuskan kapan keluar."""

    name = "GUARD"

    def __init__(self, rules: RiskRules) -> None:
        super().__init__()
        self.r = rules

    def update(self, pos: Position, tok: Token | None) -> None:
        if tok is None:
            return
        pos.last_price = tok.price
        gain = (tok.price - pos.entry_price) / pos.entry_price
        if tok.price > pos.peak_price:
            pos.peak_price = tok.price
            pos.peak_gain_pct = (tok.price - pos.entry_price) / pos.entry_price

    def decide(self, pos: Position, tok: Token, tick: int) -> str | None:
        r = self.r
        price = tok.price
        drawdown = (price - pos.peak_price) / pos.peak_price if pos.peak_price else 0.0
        gain = (price - pos.entry_price) / pos.entry_price

        if gain <= -r.stop_loss_pct:
            self.bump("exit:stop_loss")
            self.say(f"STOP {pos.symbol} {gain*100:+.1f}%")
            return "stop_loss"

        if pos.peak_gain_pct >= r.trail_after_pct and drawdown <= -r.trail_distance_pct:
            self.bump("exit:trailing")
            self.say(f"TRAIL {pos.symbol} dari puncak {pos.peak_gain_pct*100:+.1f}%")
            return "trailing_stop"

        if tick - pos.entry_tick >= r.max_hold_ticks:
            self.bump("exit:waktu_habis")
            self.say(f"TIMEOUT {pos.symbol}")
            return "max_hold"

        if tok.liquidity_usd < 1_000:
            self.bump("exit:likuiditas_hilang")
            self.say(f"LIQ HILANG {pos.symbol}")
            return "liquidity_gone"

        return None


class Scribe(Agent):
    """Pencatat. Semua penolakan ikut dicatat — di sinilah audit trail-nya."""

    name = "SCRIBE"

    def __init__(self, run_dir: Path | None = None, buffer: int = 400) -> None:
        super().__init__()
        self.buffer: deque[Event] = deque(maxlen=buffer)
        self.total = 0
        self._lock = threading.Lock()
        self.path = None
        self._fh = None
        if run_dir is not None:
            run_dir.mkdir(parents=True, exist_ok=True)
            self.path = run_dir / "events.jsonl"
            self._fh = open(self.path, "w", encoding="utf-8")

    def write(self, ev: Event) -> None:
        with self._lock:
            self.buffer.append(ev)
            self.total += 1
            self.bump(ev.agent)
            if self._fh is not None:
                self._fh.write(json.dumps(ev.public(), ensure_ascii=False) + "\n")
                self._fh.flush()

    def since(self, n: int) -> list[Event]:
        with self._lock:
            return list(self.buffer)[-n:] if n > 0 else []

    def close(self) -> None:
        if self._fh is not None:
            self._fh.close()
            self._fh = None

    def stats(self) -> dict:
        d = super().stats()
        d["total"] = self.total
        return d
