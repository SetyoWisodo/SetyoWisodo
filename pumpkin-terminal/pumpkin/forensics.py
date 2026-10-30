"""Forensics token — dijalankan dalam hitungan detik setelah whale masuk.

Yang diukur (semuanya data publik on-chain, bukan ramalan):

* porsi supply yang dipegang dev
* konsentrasi top-10 holder
* bundle % (porsi supply yang dibeli bot di blok pertama peluncuran)
* status mint authority & LP lock
* riwayat dev: berapa token sebelumnya yang berakhir rug

Output: ``rug_risk`` 0..1 + daftar temuan + estimasi waktu analisis.
Batas waktu yang dipakai desk: ``max_rug_risk`` — di atas itu tidak disentuh.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from statistics import median

from .whale_market import MemeToken


def _norm(x: float, lo: float, hi: float) -> float:
    if hi == lo:
        return 0.0
    return max(0.0, min(1.0, (x - lo) / (hi - lo)))


class DevLedger:
    """Riwayat dev yang berakhir rug — 'big data' paling murah dan paling berguna."""

    def __init__(self) -> None:
        self.rugged: dict[str, int] = {}
        self.launched: dict[str, int] = {}

    def register(self, dev: str) -> None:
        self.launched[dev] = self.launched.get(dev, 0) + 1

    def mark_rug(self, dev: str) -> None:
        self.rugged[dev] = self.rugged.get(dev, 0) + 1

    def prior_rugs(self, dev: str) -> int:
        return self.rugged.get(dev, 0)

    def rug_rate(self, dev: str) -> float:
        n = self.launched.get(dev, 0)
        return self.rugged.get(dev, 0) / n if n else 0.0

    def stats(self) -> dict:
        return {"devs": len(self.launched), "rugs": sum(self.rugged.values()),
                "repeat_offenders": sum(1 for v in self.rugged.values() if v > 1)}


@dataclass
class ForensicReport:
    address: str
    symbol: str
    rug_risk: float
    findings: list[str] = field(default_factory=list)
    dev_pct: float = 0.0
    bundle_pct: float = 0.0
    top10_pct: float = 0.0
    dev_prior_rugs: int = 0
    latency_ms: float = 0.0

    @property
    def safe(self) -> bool:
        return self.rug_risk < 0.42

    def public(self) -> dict:
        return {
            "symbol": self.symbol,
            "rug_risk": round(self.rug_risk, 3),
            "dev_pct": round(self.dev_pct, 1),
            "bundle_pct": round(self.bundle_pct, 1),
            "top10_pct": round(self.top10_pct, 1),
            "dev_prior_rugs": self.dev_prior_rugs,
            "findings": self.findings,
            "latency_ms": round(self.latency_ms, 2),
        }


class Forensics:
    """Analisis cepat + pengukuran latency nyata (p50/p95)."""

    W_DEV = 0.28
    W_BUNDLE = 0.20
    W_TOP10 = 0.14
    W_LP = 0.12
    W_MINT = 0.06
    W_HISTORY = 0.20

    def __init__(self, ledger: DevLedger | None = None, sample: int = 500):
        self.ledger = ledger or DevLedger()
        self.samples: list[float] = []
        self._sample = sample
        self.count = 0

    def analyze(self, tok: MemeToken) -> ForensicReport:
        t0 = time.perf_counter()
        findings: list[str] = []

        dev = _norm(tok.dev_pct, 0.0, 25.0)
        bundle = _norm(tok.bundle_pct, 0.0, 30.0)
        top10 = _norm(tok.top10_pct, 10.0, 70.0)
        lp = 0.0 if tok.lp_locked else 1.0
        mint = 0.0 if tok.mint_revoked else 1.0
        prior = self.ledger.prior_rugs(tok.dev_address) or tok.dev_prior_rugs
        history = _norm(prior, 0.0, 3.0)

        if tok.dev_pct >= 15:
            findings.append(f"dev pegang {tok.dev_pct:.1f}% supply")
        if tok.bundle_pct >= 20:
            findings.append(f"bundle {tok.bundle_pct:.1f}% di blok pertama")
        if tok.top10_pct >= 45:
            findings.append(f"top-10 holder {tok.top10_pct:.1f}%")
        if not tok.lp_locked:
            findings.append("LP tidak terkunci")
        if not tok.mint_revoked:
            findings.append("mint authority masih aktif")
        if prior:
            findings.append(f"dev punya {prior} riwayat rug")

        risk = (self.W_DEV * dev + self.W_BUNDLE * bundle + self.W_TOP10 * top10
                + self.W_LP * lp + self.W_MINT * mint + self.W_HISTORY * history)

        ms = (time.perf_counter() - t0) * 1000.0
        self.count += 1
        self.samples.append(ms)
        if len(self.samples) > self._sample:
            self.samples.pop(0)
        return ForensicReport(
            address=tok.address, symbol=tok.symbol, rug_risk=min(1.0, risk),
            findings=findings, dev_pct=tok.dev_pct, bundle_pct=tok.bundle_pct,
            top10_pct=tok.top10_pct, dev_prior_rugs=prior, latency_ms=ms,
        )

    # ------------------------------------------------------------- statistik
    def latency_stats(self) -> dict:
        if not self.samples:
            return {"p50": 0.0, "p95": 0.0, "n": 0}
        s = sorted(self.samples)
        p95 = s[min(len(s) - 1, int(len(s) * 0.95))]
        return {"p50": round(median(s), 3), "p95": round(p95, 3), "n": len(s)}
