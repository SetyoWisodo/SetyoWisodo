#!/usr/bin/env python3
"""Pumpkin Terminal — entry point.

    python run.py serve                      # dashboard live (paper trading)
    python run.py sim --ticks 1800           # sesi headless + laporan
    python run.py bench                      # uji jujur: correlated vs null edge
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from pumpkin.config import Config, SimConfig  # noqa: E402
from pumpkin.engine import Desk            # noqa: E402
from pumpkin.report import write_report    # noqa: E402


def _cfg(args) -> Config:
    cfg = Config()
    cfg.sim = SimConfig(
        start_balance=args.balance,
        ticks=args.ticks,
        seed=args.seed,
        edge_mode=args.edge,
        tokens_per_tick=args.tokens_per_tick,
        tick_seconds_wall=args.tick_seconds,
        feed=args.feed,
    )
    if args.threshold is not None:
        cfg.risk.min_score = args.threshold
    return cfg


def cmd_sim(args) -> int:
    cfg = _cfg(args)
    desk = Desk(cfg)
    t0 = time.time()
    total = cfg.sim.ticks
    step = max(1, total // 20)
    print(f"\n  PUMPKIN TERMINAL · mode={cfg.sim.edge_mode} · seed={cfg.sim.seed}")
    print(f"  saldo awal ${cfg.sim.start_balance:,.2f} · {total:,} tick "
          f"(≈{cfg.sim.sim_minutes:.0f} menit pasar)\n")
    while not desk.finished:
        desk.tick()
        if desk.tick_no % step == 0:
            k = desk.kpis()
            print(f"  [{desk.tick_no:>5}/{total}] ekuitas ${k['equity']:>9,.2f} "
                  f"({k['pnl_pct']:+6.2f}%) · scan {k['scanned']:>6,} · "
                  f"tolak {k['rejected']:>6,} · trade {k['trades']:>3}")
    print(f"\n  selesai dalam {time.time() - t0:.1f}s")
    jpath, mpath = write_report(desk)
    k = desk.kpis()
    print(f"  ekuitas akhir ${k['equity']:,.2f} ({k['pnl_pct']:+.2f}%) · "
          f"win-rate {k['win_rate']}% · DD {k['max_drawdown_pct']}% · fee ${k['fees_paid']:,.2f}")
    print(f"  laporan: {mpath}\n")
    return 0


def cmd_bench(args) -> int:
    import statistics as st

    print("\n  UJI JUJUR — apakah profit berasal dari strategi, atau dari generator?\n")
    out_rows = []
    for mode in ("correlated", "null"):
        pnls, trades, fees = [], [], []
        for seed in range(1, args.seeds + 1):
            cfg = Config()
            cfg.sim = SimConfig(start_balance=80.0, ticks=args.ticks, seed=seed,
                                edge_mode=mode, tokens_per_tick=args.tokens_per_tick)
            desk = Desk(cfg)
            while not desk.finished:
                desk.tick()
            k = desk.kpis()
            pnls.append(k["pnl_pct"])
            trades.append(k["trades"])
            fees.append(k["fees_paid"])
        pnls.sort()
        med = st.median(pnls)
        q1, q3 = pnls[len(pnls) // 4], pnls[(3 * len(pnls)) // 4]
        pos = sum(1 for p in pnls if p > 0)
        print(f"  {mode:>10} · {args.seeds} sesi")
        print(f"      median PnL  : {med:+8.1f}%")
        print(f"      rentang IQR : {q1:+.1f}% .. {q3:+.1f}%   (min {pnls[0]:+.1f}%, max {pnls[-1]:+.1f}%)")
        print(f"      sesi profit : {pos}/{args.seeds} · trade rata-rata {st.mean(trades):.0f} "
              f"· fee rata-rata ${st.mean(fees):.2f}\n")
        out_rows.append({
            "mode": mode, "seeds": args.seeds, "median_pnl_pct": round(med, 2),
            "q1": round(q1, 2), "q3": round(q3, 2), "positive_sessions": pos,
            "avg_trades": round(st.mean(trades), 1), "avg_fees": round(st.mean(fees), 2),
            "all_pnl_pct": [round(p, 2) for p in pnls],
        })

    print("  Interpretasi:")
    print("   • correlated: generator menyuntikkan akumulasi sebelum lonjakan, jadi")
    print("     momentum yang dibaca ANALYST memang punya arti. Ini menguji pipeline,")
    print("     BUKAN membuktikan strategi ini akan profit di pasar nyata.")
    print("   • null: semua keahlian dimatikan (FILTER dilewati, skor ANALYST acak).")
    print("     Ini setara melempar panah: hasilnya negatif, dan penyebabnya jelas —")
    print("     fee + slippage round-trip 5,5% plus rug yang menembus stop-loss.")
    print("   • Klaim thread: $80 → $5.432 = +6.690% dalam semalam. Itu satu undian")
    print("     paper-trading, bukan distribusi hasil yang bisa kamu harapkan.\n")

    out = Path(__file__).resolve().parent / "runs" / "bench.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"ticks": args.ticks, "results": out_rows}, indent=2), encoding="utf-8")
    print(f"  detail: {out}\n")
    return 0


def cmd_serve(args) -> int:
    from pumpkin.server import serve
    serve(host=args.host, port=args.port, cfg=_cfg(args))
    return 0


def main() -> int:
    p = argparse.ArgumentParser(prog="pumpkin", description="Pumpkin Terminal — paper trading desk 6 agen")
    sub = p.add_subparsers(dest="cmd", required=True)

    def common(sp):
        sp.add_argument("--ticks", type=int, default=1800)
        sp.add_argument("--balance", type=float, default=80.0)
        sp.add_argument("--seed", type=int, default=7)
        sp.add_argument("--edge", choices=("correlated", "null"), default="correlated")
        sp.add_argument("--threshold", type=float, default=None, help="ambang skor ANALYST (default 0.6)")
        sp.add_argument("--tokens-per-tick", type=int, default=7)
        sp.add_argument("--feed", choices=("sim", "dexscreener"), default="sim")

    s = sub.add_parser("sim", help="jalankan satu sesi headless")
    common(s)
    s.add_argument("--tick-seconds", type=float, default=0.0)
    s.set_defaults(func=cmd_sim)

    b = sub.add_parser("bench", help="bandingkan edge correlated vs null")
    b.add_argument("--ticks", type=int, default=1000)
    b.add_argument("--seeds", type=int, default=10, help="jumlah sesi per mode")
    b.add_argument("--tokens-per-tick", type=int, default=7)
    b.set_defaults(func=cmd_bench)

    v = sub.add_parser("serve", help="jalankan dashboard live")
    common(v)
    v.add_argument("--host", default="0.0.0.0")
    v.add_argument("--port", type=int, default=8000)
    v.add_argument("--tick-seconds", type=float, default=0.1)
    v.set_defaults(func=cmd_serve)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
