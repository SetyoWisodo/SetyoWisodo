"""Alat ukur untuk menjawab satu pertanyaan: **apakah fitur ini benar-benar bernilai?**

Diambil dari ide stack kuant yang dipakai orang sungguhan (lihat
``docs/QUANT-STACK.md``), tapi ditulis ulang tanpa dependency:

* **information coefficient (IC)** — dari qlib/RD-Agent. Kalau sebuah fitur tidak
  berkorelasi dengan hasil, ia hanya menambah derau. Di sini IC dihitung
  point-biserial terhadap "trade menang", lengkap dengan interval kepercayaan
  bootstrap, supaya kamu tidak mengejar derau pada sampel 30 trade.
* **CVaR / expected shortfall** — dari gs-quant. Rata-rata kerugian di 5% ekor
  terburuk. Jauh lebih jujur daripada "max drawdown" yang cuma satu angka.
* **portfolio heat** — dari skfolio. Total uang yang benar-benar dipertaruhkan
  (jarak ke stop), bukan sekadar jumlah posisi.
* **risk of ruin** — peluang menyentuh drawdown tertentu sebelum modal habis.
"""

from __future__ import annotations

import math
import random


# --------------------------------------------------------------------------- #
# 1. Information coefficient
# --------------------------------------------------------------------------- #
def point_biserial(values: list[float], wins: list[bool]) -> float:
    """Korelasi fitur kontinu dengan label biner (IC).

    Positif = makin besar fitur, makin sering menang. Nol = tidak ada informasi.
    """
    n = len(values)
    if n < 3 or n != len(wins):
        return 0.0
    pos = [v for v, w in zip(values, wins) if w]
    neg = [v for v, w in zip(values, wins) if not w]
    if not pos or not neg:
        return 0.0
    m_all = sum(values) / n
    sd = math.sqrt(sum((v - m_all) ** 2 for v in values) / n)
    if sd < 1e-12:
        return 0.0
    m1, m0 = sum(pos) / len(pos), sum(neg) / len(neg)
    share = len(pos) / n
    return (m1 - m0) / sd * math.sqrt(share * (1 - share))


def feature_ic(rows: list[dict], keys: list[str] | None = None,
               boot: int = 300, seed: int = 7) -> dict[str, dict]:
    """IC per fitur + interval kepercayaan 95% lewat bootstrap.

    ``rows`` = [{"features": {...}, "won": bool}, ...]
    Kalau ``lo`` dan ``hi`` melewati nol, fitur itu **belum terbukti** berguna —
    berapa pun besar angkanya.
    """
    if not rows:
        return {}
    keys = keys or sorted({k for r in rows for k in r.get("features", {})})
    rng = random.Random(seed)
    out: dict[str, dict] = {}
    for k in keys:
        vals = [float(r["features"].get(k, 0.0)) for r in rows]
        wins = [bool(r["won"]) for r in rows]
        ic = point_biserial(vals, wins)
        samples = []
        for _ in range(boot):
            idx = [rng.randrange(len(rows)) for _ in range(len(rows))]
            samples.append(point_biserial([vals[i] for i in idx],
                                          [wins[i] for i in idx]))
        samples.sort()
        lo = samples[int(0.025 * len(samples))]
        hi = samples[int(0.975 * len(samples)) - 1]
        out[k] = {
            "ic": round(ic, 4),
            "lo": round(lo, 4),
            "hi": round(hi, 4),
            "n": len(rows),
            "berguna": bool(lo > 0 or hi < 0),
        }
    return out


def prune_features(ic: dict[str, dict]) -> tuple[list[str], list[str]]:
    """Pisahkan fitur yang terbukti dari yang cuma derau (prinsip RD-Agent)."""
    useful = [k for k, v in ic.items() if v["berguna"]]
    noise = [k for k, v in ic.items() if not v["berguna"]]
    return sorted(useful), sorted(noise)


# --------------------------------------------------------------------------- #
# 2. Risiko ekor
# --------------------------------------------------------------------------- #
def cvar(pnls_pct: list[float], q: float = 0.05) -> float:
    """CVaR: rata-rata kerugian di ``q`` ekor terburuk (dalam persen).

    Dikembalikan sebagai angka negatif (kerugian).
    """
    if not pnls_pct:
        return 0.0
    s = sorted(pnls_pct)
    k = max(1, int(round(len(s) * q)))
    tail = s[:k]
    return sum(tail) / len(tail)


def percentiles(pnls_pct: list[float]) -> dict:
    if not pnls_pct:
        return {"p05": 0.0, "p50": 0.0, "p95": 0.0, "mean": 0.0}
    s = sorted(pnls_pct)

    def pick(p: float) -> float:
        i = min(len(s) - 1, max(0, int(round(p * (len(s) - 1)))))
        return s[i]

    return {"p05": pick(0.05), "p50": pick(0.50), "p95": pick(0.95),
            "mean": sum(s) / len(s)}


# --------------------------------------------------------------------------- #
# 3. Heat portofolio
# --------------------------------------------------------------------------- #
def portfolio_heat(stop_risk_usd: list[float], equity: float) -> float:
    """Total risiko terbuka (uang yang bisa hilang kalau semua stop kena)."""
    if equity <= 0:
        return 1.0
    return sum(stop_risk_usd) / equity


# --------------------------------------------------------------------------- #
# 4. Risk of ruin
# --------------------------------------------------------------------------- #
def risk_of_ruin(p: float, win_pct: float, loss_pct: float, ruin_dd: float = 0.30,
                 paths: int = 4000, seed: int = 11) -> float:
    """Peluang menyentuh drawdown ``ruin_dd`` sebelum modal berlipat 2×.

    Monte Carlo sederhana atas hit rate dan payoff yang **diukur**, bukan diasumsikan.
    """
    if p <= 0 or win_pct <= 0:
        return 1.0
    if loss_pct <= 0 or p >= 1.0:
        return 0.0          # tidak pernah turun → tidak ada ruin
    rng = random.Random(seed)
    ruined = 0
    for _ in range(paths):
        eq = peak = 1.0
        for _ in range(200):
            eq *= (1 + win_pct) if rng.random() < p else (1 - loss_pct)
            peak = max(peak, eq)
            if (peak - eq) / peak >= ruin_dd:
                ruined += 1
                break
            if eq >= 2.0:
                break
    return ruined / paths


# --------------------------------------------------------------------------- #
# 5. Ringkasan
# --------------------------------------------------------------------------- #
def risk_report(trades: list[dict], equity_start: float) -> dict:
    """Ringkasan risiko dari daftar trade (dict dengan 'pnl_pct' & 'pnl_usd')."""
    pnls = [t["pnl_pct"] for t in trades]
    wins = [t for t in trades if t["pnl_pct"] > 0]
    losses = [t for t in trades if t["pnl_pct"] <= 0]
    if not trades:
        return {"trades": 0, "cvar_95_pct": 0.0, "cvar_95_usd": 0.0,
                "percentiles": percentiles([]), "risk_of_ruin_pct": 0.0,
                "tail_losses": 0}
    avg_win = sum(t["pnl_pct"] for t in wins) / len(wins) / 100 if wins else 0.0
    avg_loss = abs(sum(t["pnl_pct"] for t in losses) / len(losses)) / 100 if losses else 0.0
    cv = cvar(pnls, 0.05)
    k = max(1, int(round(len(pnls) * 0.05)))
    worst = sorted(t["pnl_usd"] for t in trades)[:k]
    return {
        "trades": len(trades),
        "cvar_95_pct": round(cv, 3),
        "cvar_95_usd": round(sum(worst) / len(worst), 2),
        "percentiles": {k2: round(v, 3) for k2, v in percentiles(pnls).items()},
        # di bawah 30 trade, estimasi ini cuma mencerminkan derau sampel —
        # lebih baik kosong daripada angka yang menyesatkan
        "risk_of_ruin_pct": (round(risk_of_ruin(len(wins) / len(trades), avg_win,
                                                avg_loss, 0.30) * 100, 2)
                             if len(trades) >= 30 else None),
        "tail_losses": k,
    }
