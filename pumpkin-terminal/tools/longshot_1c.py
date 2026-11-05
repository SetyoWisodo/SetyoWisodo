#!/usr/bin/env python3
"""Eksperimen: beli tiket 1,2¢ di kontrak biner BTC 5 menit — "lotre" itu +EV atau tidak?

Konteksnya: ada thread yang menunjukkan wallet yang membeli sisi "hampir mati" seharga
1–1,2¢ lalu dibayar $1 (≈80x). Yang ditampilkan hanya pemenangnya.

Model (asumsi ditulis terbuka):

* BTC mengikuti random walk. Volatilitas **acuan pembuat pasar** sigma_maker adalah
  sigma tenang (0,11% per 5 menit ≈ $121 pada BTC $110k).
* Volatilitas **sebenarnya** sigma_true = k × sigma_maker. ``k`` adalah satu-satunya
  variabel yang menentukan apakah strategi ini untung: seberapa salah pembuat pasar
  mengukur volatilitas saat harga bergerak kasar.
* Harga yang kita bayar 1,2¢; payout $1. Kontrak hanya dibeli kalau sisi itu memang
  ditawarkan ≤1,2¢ menurut harga si pembuat pasar.
* Tidak ada fee (Polymarket umumnya 0 untuk trading; settlement fee diabaikan agar
  hasilnya tidak "menang" karena asumsi biaya).

Karena break-even tiket 1,2¢ adalah **hit rate 1,2%**, seluruh pertanyaan menyusut jadi:
saat quote menyentuh 1,2¢, apakah peluang sebenarnya lebih besar dari 1,2%?

Jalankan:  python tools/longshot_1c.py --markets 3000
"""

from __future__ import annotations

import argparse
import math
import random
from statistics import NormalDist

N = NormalDist()

S0 = 110_000.0
SIGMA_5MIN = 0.0011 * S0      # ≈ $121 per 5 menit
SECONDS = 300
PRICE = 0.012                 # tiket yang dibeli
STEPS = 150                   # resolusi 2 detik


def maker_fair(d: float, tau: float, sigma: float) -> float:
    if tau <= 0:
        return 1.0 if d > 0 else (0.0 if d < 0 else 0.5)
    s = sigma * math.sqrt(tau / SECONDS)
    return min(1.0, max(0.0, N.cdf(d / s)))


def run(markets: int, k: float, ticket: float = 100.0, bankroll: float = 10_000.0,
        seed: int = 23) -> dict:
    rng = random.Random(seed)
    sigma_true = SIGMA_5MIN * k
    sigma_maker = SIGMA_5MIN
    dt = SECONDS / STEPS
    sigma_step = sigma_true * math.sqrt(dt / SECONDS)

    trades = wins = 0
    equity = bankroll
    peak = bankroll
    max_dd = 0.0
    streak = worst_streak = 0
    ruined = False

    for _ in range(markets):
        d = 0.0
        side = 0                      # +1 = UP, -1 = DOWN, 0 = belum ada tiket
        for i in range(1, STEPS + 1):
            d += rng.gauss(0.0, sigma_step)
            tau = SECONDS - i * dt
            if side:
                continue              # tiket sudah dibeli; jalur tetap berjalan ke settlement
            f_up = maker_fair(d, tau, sigma_maker)
            if f_up >= 1 - PRICE:
                side = -1             # DOWN yang murah
            elif f_up <= PRICE:
                side = +1             # UP yang murah
        if not side:
            continue                  # tidak ada tiket yang cukup murah

        trades += 1
        cost = ticket
        won = (d > 0 and side > 0) or (d < 0 and side < 0)
        payout = ticket * (1.0 / PRICE) if won else 0.0
        equity += payout - cost
        if won:
            wins += 1
            streak = 0
        else:
            streak += 1
            worst_streak = max(worst_streak, streak)
        peak = max(peak, equity)
        max_dd = max(max_dd, (peak - equity) / peak if peak > 0 else 1.0)
        if equity < ticket:          # tidak sanggup beli tiket berikutnya
            ruined = True
            break

    equity = max(0.0, equity)
    hit = wins / trades if trades else 0.0
    ev_per_contract = hit - PRICE
    return {
        "k": k, "trades": trades, "wins": wins,
        "hit_rate_pct": round(100 * hit, 3),
        "ev_per_contract_c": round(100 * ev_per_contract, 3),
        "roi_pct": round(100 * ev_per_contract / PRICE, 1),
        "final_equity": round(equity, 0),
        "worst_streak": worst_streak,
        "max_dd_pct": round(100 * max_dd, 1),
        "ruined": ruined,
        "signal_pct": round(100 * trades / markets, 1),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--markets", type=int, default=3000)
    ap.add_argument("--ticket", type=float, default=100.0)
    ap.add_argument("--bankroll", type=float, default=10_000.0)
    args = ap.parse_args()

    print(f"\n  LOTRE 1,2¢ · {args.markets:,} pasar · tiket ${args.ticket:,.0f} · "
          f"bankroll ${args.bankroll:,.0f}")
    print(f"  Break-even: hit rate 1,2% (= harga tiket). Pertanyaannya cuma itu.\n")
    print(f"  {'k':>5}{'sinyal':>9}{'trade':>8}{'hit rate':>11}{'EV/kontrak':>12}"
          f"{'ROI':>9}{'streak':>8}{'max DD':>9}{'akhir':>11}{'bangkrut':>10}")
    print("  " + "-" * 92)
    for k in (1.0, 1.1, 1.2, 1.5, 2.0, 3.0):
        r = run(args.markets, k, args.ticket, args.bankroll)
        print(f"  {r['k']:>5.1f}{r['signal_pct']:>8.1f}%{r['trades']:>8}"
              f"{r['hit_rate_pct']:>10.2f}%{r['ev_per_contract_c']:>11.2f}¢"
              f"{r['roi_pct']:>8.0f}%{r['worst_streak']:>8}"
              f"{r['max_dd_pct']:>8.0f}%{r['final_equity']:>11,.0f}"
              f"{'  YA' if r['ruined'] else '  tidak':>10}")
    print()
    print("  k = seberapa salah pembuat pasar mengukur volatilitas (sigma_true/sigma_maker).")
    print("  k=1,0 → harga wajar, EV nol. k=1,2 (vol 20% lebih tinggi) sudah +150% ROI per tiket.")
    print("  Artinya: ini bukan 'pasar lupa menaruh harga', ini taruhan pada rezim volatilitas.")
    print("  Perhatikan kolom streak: kalah 100+ kali berturut-turut itu normal, bukan anomali.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
