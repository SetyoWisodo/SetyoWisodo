"""Komite risiko: satu pihak wajib membela **kerugian**, bukan keuntungan.

Diambil dari pola *TradingAgents* (analis → peneliti bull vs bear → trader →
tim risiko yang harus menandatangani). Yang saya ambil bukan "AI debat", tapi
**struktur keputusannya**: setiap entry harus melewati seseorang yang tugasnya
mencari alasan untuk menolak.

Urutannya di desk:

```
AlphaEngine (p̂, target, EV)  →  BearResearcher (keberatan + skor)
                              →  RiskCommittee (tolak / perkecil / setujui)
                              →  SNIPER baru boleh membeli
```

Keberatan dihitung dari data yang **teramati**, bukan opini model bahasa:
tidak ada LLM di jalur ini, jadi hasilnya bisa diuji ulang dan deterministik.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field


@dataclass
class Objection:
    key: str
    severity: float          # 0..1
    detail: str

    def public(self) -> dict:
        return {"key": self.key, "severity": round(self.severity, 3),
                "detail": self.detail}


@dataclass
class BearCase:
    score: float = 0.0
    thesis: str = ""
    objections: list[Objection] = field(default_factory=list)

    def public(self) -> dict:
        return {"score": round(self.score, 3), "thesis": self.thesis,
                "objections": [o.public() for o in self.objections]}


@dataclass
class Verdict:
    approved: bool
    scale: float                       # 1.0 = ukuran penuh, 0.5 = separuh
    note: str = ""
    objections: list[Objection] = field(default_factory=list)

    def public(self) -> dict:
        return {"approved": self.approved, "scale": round(self.scale, 2),
                "note": self.note,
                "objections": [o.public() for o in self.objections]}


class BearResearcher:
    """Mencari alasan untuk TIDAK membeli, lalu memberi skor 0..1."""

    def __init__(self, ideal_chase: float = 0.08, max_chase: float = 0.22,
                 min_liquidity: float = 45_000.0, min_regime: float = 0.45,
                 min_margin: float = 0.03):
        self.ideal_chase = ideal_chase
        self.max_chase = max_chase
        self.min_liquidity = min_liquidity
        self.min_regime = min_regime
        self.min_margin = min_margin

    def examine(self, *, features: dict, decision, price_hist: list[float],
                max_hold_ticks: int, heat: float = 0.0,
                heat_cap: float = 0.08) -> BearCase:
        f = features
        social = f.get("social", 0.0)
        coord = f.get("coordination", 0.0)
        safety = f.get("safety", 0.5)
        regime = f.get("regime", 0.5)
        liquidity = f.get("liquidity", 0.0)
        p = decision.p_win
        tp = decision.take_profit
        out: list[Objection] = []

        # 1. hype tanpa substansi: ramai dibicarakan, tapi on-chain-nya buruk
        sev = max(0.0, min(1.0, social * (1.0 - safety) * 1.6))
        if sev > 0.15:
            out.append(Objection("hype_tanpa_substansi", sev,
                                 f"social {social:.2f} tapi safety {safety:.2f}"))

        # 2. percakapan yang dipesan
        if coord > 0.25:
            out.append(Objection("percakapan_dipesan", coord,
                                 f"skor koordinasi {coord:.2f}"))

        # 3. terlambat masuk
        chg = (price_hist[-1] / price_hist[0] - 1.0) if len(price_hist) >= 2 else 0.0
        sev = max(0.0, min(1.0, (chg - self.ideal_chase) / (self.max_chase - self.ideal_chase)))
        if sev > 0.15:
            out.append(Objection("kejar_harga", sev,
                                 f"harga sudah {chg*100:+.1f}% dalam 3 tick"))

        # 4. rezim pasar
        sev = max(0.0, min(1.0, (self.min_regime - regime) / self.min_regime))
        if sev > 0.05:
            out.append(Objection("rezim_lemah", sev, f"rezim {regime:.2f}"))

        # 5. likuiditas tipis → slippage keluar bisa jauh dari asumsi
        sev = max(0.0, min(1.0, 1.0 - (liquidity * 60_000.0) / self.min_liquidity))
        if sev > 0.2:
            out.append(Objection("likuiditas_tipis", sev,
                                 f"likuiditas ~${liquidity*60_000:,.0f}"))

        # 6. target tidak terjangkau dalam waktu yang diizinkan
        #    (ini bagian "forecast": drift 3 tick terakhir dipakai sebagai proyeksi)
        drift = chg / 3.0 if len(price_hist) >= 4 else 0.0
        proyeksi = max(0.0, drift) * max_hold_ticks
        sev = max(0.0, min(1.0, 1.0 - proyeksi / max(1e-6, tp)))
        if sev > 0.45:
            out.append(Objection("target_tidak_terjangkau", sev,
                                 f"proyeksi {proyeksi*100:+.1f}% vs target {tp*100:.1f}%"))

        # 7. margin probabilitas terlalu tipis terhadap ambang
        sev = max(0.0, min(1.0, 1.0 - (p - 0.70) / self.min_margin))
        if sev > 0.2:
            out.append(Objection("margin_tipis", sev, f"p̂ {p:.3f} hanya di ambang"))

        # 8. portofolio sudah panas
        sev = max(0.0, min(1.0, heat / max(1e-6, heat_cap)))
        if sev > 0.5:
            out.append(Objection("portofolio_panas", sev,
                                 f"heat {heat*100:.1f}% dari batas {heat_cap*100:.0f}%"))

        if not out:
            return BearCase(0.0, "tidak ada keberatan material", [])

        # satu keberatan fatal sudah cukup: 60% bobot ke yang terburuk
        worst = max(o.severity for o in out)
        mean = sum(o.severity for o in out) / len(out)
        score = max(0.0, min(1.0, 0.6 * worst + 0.4 * mean))
        top = sorted(out, key=lambda o: -o.severity)[:2]
        thesis = "Berhenti. " + "; ".join(f"{o.detail} ({o.key})" for o in top)
        return BearCase(score, thesis, out)


class RiskCommittee:
    """Menandatangani atau menolak. Tidak punya kewenangan memperbesar posisi."""

    def __init__(self, veto_at: float = 0.62, downsize_at: float = 0.38,
                 downsize_scale: float = 0.5, heat_cap: float = 0.08,
                 max_bear_dist: float = 0.0):
        self.veto_at = veto_at
        self.downsize_at = downsize_at
        self.downsize_scale = downsize_scale
        self.heat_cap = heat_cap

    def sign_off(self, *, bear: BearCase, decision, heat: float,
                 new_heat: float) -> Verdict:
        if not decision.approved:
            return Verdict(False, 0.0, "alpha menolak lebih dulu", bear.objections)

        if bear.score >= self.veto_at:
            return Verdict(False, 0.0,
                           f"komite menolak: {bear.thesis}", bear.objections)

        if heat + new_heat > self.heat_cap:
            return Verdict(False, 0.0,
                           f"heat portofolio {heat*100:.1f}% + {new_heat*100:.1f}% "
                           f"melewati batas {self.heat_cap*100:.0f}%", bear.objections)

        if bear.score >= self.downsize_at:
            scale = self.downsize_scale
            # makin dekat ke ambang veto, makin kecil
            span = max(1e-6, self.veto_at - self.downsize_at)
            scale = max(0.25, min(1.0, scale - 0.25 * (bear.score - self.downsize_at) / span))
            return Verdict(True, scale,
                           f"disetujui separuh: {bear.thesis}", bear.objections)

        return Verdict(True, 1.0, "disetujui", bear.objections)


def stop_risk_pct(size_pct: float, stop_loss: float) -> float:
    """Bagian ekuitas yang hilang kalau stop kena (dipakai untuk heat)."""
    return max(0.0, size_pct * stop_loss)


def expected_shortfall_from_heat(heat: float, gap_factor: float = 1.8) -> float:
    """Perkiraan kerugian kalau semua stop kena serentak **dengan gap**.

    ``gap_factor`` > 1 karena di memecoin stop sering dieksekusi di bawah level
    (kita sudah melihat ini di data: kerugian rata-rata lebih besar dari stop).
    """
    return math.fsum([heat * gap_factor])
