#!/usr/bin/env python3
"""Eksperimen: dua dompet, satu beli UP satu beli DOWN, di kontrak biner BTC 5 menit.

Pertanyaan yang diuji: kalau sisi yang menang dibiarkan sampai $1 dan sisi yang kalah
di-cut di 35¢ — apakah tetap untung?

Model (semua asumsi ditulis, bukan disembunyikan):

* BTC mengikuti random walk tanpa drift; sigma 5 menit = 0.11% dari harga (≈$121 pada
  BTC $110k). Ini yang membuat pasar biner "adil" — kalau BTC punya tren, hasilnya
  berubah dan itu justru inti persoalannya.
* Harga wajar UP pada detik ke-t = Phi(d / (sigma * sqrt(sisa waktu))).
  Harga DOWN = 1 - harga UP. Jadi **kedua harga selalu berjumlah ~1**.
* Spread 2¢ per kontrak (1¢ di tiap sisi order book). Tanpa spread, seluruh eksperimen
  ini pasti impas — spread-lah yang membuatnya negatif.

Variabel yang diuji: aturan keluar untuk sisi yang kalah.
    hold      : tidak melakukan apa pun, tunggu settlement
    cut X     : jual sisi yang kalah begitu bid-nya menyentuh X
    add X     : BELI TAMBAH sisi yang kalah di X (averaging down / martingale)

Jalankan:  python tools/polymarket_dual_wallet.py --paths 50000
"""

from __future__ import annotations

import argparse
import math
import random
from statistics import NormalDist

N = NormalDist()

S0 = 110_000.0
SIGMA_5MIN = 0.0011 * S0        # ≈ $121 simpangan baku 5 menit
SECONDS = 300
HALF_SPREAD = 0.01              # 1¢ di tiap sisi → 2¢ spread per kontrak
FEE_ON_PROCEEDS = 0.0           # Polymarket umumnya 0 fee trading; coba juga 1%


def fair_up(d: float, tau: float) -> float:
    """Harga wajar kontrak UP, dalam dolar per $1 payout."""
    if tau <= 0:
        return 1.0 if d > 0 else (0.0 if d < 0 else 0.5)
    sigma = SIGMA_5MIN * math.sqrt(tau / SECONDS)
    return min(1.0, max(0.0, N.cdf(d / sigma)))


def run(paths: int, rule: str, level: float, steps: int = 60,
        fee: float = FEE_ON_PROCEEDS, seed: int = 17) -> dict:
    rng = random.Random(seed)
    dt = SECONDS / steps
    sigma_step = SIGMA_5MIN * math.sqrt(dt / SECONDS)

    pnls, wins, triggered, big_loss = [], 0, 0, 0

    for _ in range(paths):
        cost = (0.5 + HALF_SPREAD) * 2   # 1 kontrak UP + 1 kontrak DOWN, di ask
        d = 0.0
        up_units = down_units = 1.0
        bag = 0.0
        acted = False

        # jalur harga tetap berjalan sampai settlement — aksi hanya mengubah posisi,
        # bukan menghentikan waktu
        for i in range(1, steps + 1):
            d += rng.gauss(0.0, sigma_step)
            tau = SECONDS - i * dt
            f_up = fair_up(d, tau)
            f_dn = 1.0 - f_up

            if acted or i == steps:
                continue

            if rule == "cut":
                # jual sisi yang kalah di BID (harga wajar dikurangi setengah spread)
                if f_up < f_dn and f_up - HALF_SPREAD <= level and up_units > 0:
                    bag += up_units * max(0.0, f_up - HALF_SPREAD)
                    up_units, acted = 0.0, True
                elif f_dn < f_up and f_dn - HALF_SPREAD <= level and down_units > 0:
                    bag += down_units * max(0.0, f_dn - HALF_SPREAD)
                    down_units, acted = 0.0, True
            elif rule == "add":
                # BELI TAMBAH sisi yang kalah di harga ask-nya
                if f_up < f_dn and f_up + HALF_SPREAD <= level:
                    cost += level + HALF_SPREAD
                    up_units += 1.0
                    acted = True
                elif f_dn < f_up and f_dn + HALF_SPREAD <= level:
                    cost += level + HALF_SPREAD
                    down_units += 1.0
                    acted = True

        triggered += 1 if acted else 0

        payout = (up_units if d > 0 else 0.0) + (down_units if d < 0 else 0.0)
        payout *= (1.0 - fee)
        pnl = (payout + bag - cost) / cost
        pnls.append(pnl)
        wins += 1 if pnl > 0 else 0
        big_loss += 1 if pnl < -0.30 else 0

    pnls.sort()
    n = len(pnls)
    avg = sum(pnls) / n
    return {
        "rule": rule, "level": level, "paths": n,
        "win_rate": round(100 * wins / n, 2),
        "ev_pct": round(100 * avg, 3),
        "median_pct": round(100 * pnls[n // 2], 2),
        "p05_pct": round(100 * pnls[int(0.05 * n)], 2),
        "p95_pct": round(100 * pnls[int(0.95 * n) - 1], 2),
        "loss_gt_30pct": round(100 * big_loss / n, 2),
        "triggered_pct": round(100 * triggered / n, 2),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--paths", type=int, default=50_000)
    ap.add_argument("--fee", type=float, default=0.0)
    args = ap.parse_args()

    arms = [("hold", 0.0), ("cut", 0.45), ("cut", 0.35), ("cut", 0.20), ("add", 0.35)]
    print(f"\n  EKSPERIMEN DUA DOMPET · {args.paths:,} jalur · spread 2¢ · fee {args.fee*100:.1f}%")
    print(f"  Beli UP dan DOWN di 50¢+spread → biaya {100*(0.5+HALF_SPREAD)*2:.1f}¢ per pasang\n")
    print(f"  {'aturan':<12}{'win rate':>10}{'EV/trade':>11}{'median':>9}{'P05':>9}{'P95':>9}{'rugi>30%':>10}{'terpicu':>9}")
    print("  " + "-" * 79)
    results = []
    for rule, level in arms:
        r = run(args.paths, rule, level, fee=args.fee)
        results.append(r)
        name = f"{rule} {level:.2f}" if level else rule
        print(f"  {name:<12}{r['win_rate']:>9.1f}%{r['ev_pct']:>10.2f}%"
              f"{r['median_pct']:>8.1f}%{r['p05_pct']:>8.0f}%{r['p95_pct']:>8.0f}%"
              f"{r['loss_gt_30pct']:>9.1f}%{r['triggered_pct']:>8.1f}%")
    print()
    print("  Bacaan: EV negatif di SEMUA aturan — biaya (spread) tidak bisa dihilangkan")
    print("  oleh aturan keluar. Yang berubah hanya bentuk distribusinya: 'cut' membuat")
    print("  win rate terlihat tinggi (menang kecil sering, kalah besar jarang).\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
