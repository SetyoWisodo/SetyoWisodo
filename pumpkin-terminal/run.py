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

from pumpkin.config import (Config, SimConfig, SocialSimConfig,  # noqa: E402
                            WhaleSimConfig)
from pumpkin.engine import Desk            # noqa: E402
from pumpkin.report import write_report    # noqa: E402
from pumpkin.whale_desk import WhaleDesk, write_whale_report  # noqa: E402
from pumpkin.social_desk import (SocialDesk, run_social_bench,  # noqa: E402
                                 write_social_report)


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
    cfg.whale_sim = WhaleSimConfig(
        start_balance=getattr(args, "whale_balance", 250.0),
        ticks=getattr(args, "whale_ticks", 2400),
        seed=101,
        edge_mode=getattr(args, "whale_edge", "informed") or "informed",
    )
    if args.threshold is not None:
        cfg.risk.min_score = args.threshold
    if getattr(args, "whale_edge", None):
        cfg.whale_sim.edge_mode = args.whale_edge
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



def _social_cfg(args) -> SocialSimConfig:
    return SocialSimConfig(
        start_balance=getattr(args, "balance", 250.0),
        ticks=getattr(args, "ticks", 1200),
        seed=getattr(args, "seed", 21),
        mode=getattr(args, "mode", "dirty"),
        tokens_per_tick=getattr(args, "tokens_per_tick", 6),
    )


def cmd_social(args) -> int:
    cfg = Config()
    sim = _social_cfg(args)
    desk = SocialDesk(sim, cfg.social)
    total = sim.ticks
    step = max(1, total // 20)
    print(f"\n  SOCIAL RADAR · pasar={sim.mode} · seed={sim.seed} · "
          f"p̂ min {cfg.social.min_p_win:.2f}")
    print(f"  saldo ${sim.start_balance:,.2f} · {total:,} tick "
          f"(≈{sim.sim_minutes:.0f} menit pasar)\n")
    while not desk.finished:
        desk.tick()
        if desk.tick_no % step == 0:
            k = desk.kpis()
            print(f"   tick {desk.tick_no:>5,} · ekuitas ${k['equity']:>9,.2f} "
                  f"({k['pnl_pct']:+7.2f}%) · trade {k['trades']:>3} · "
                  f"win {k['win_rate']:5.1f}% · koordinasi dibuang "
                  f"{k['rejected'].get('koordinasi', 0)}")
    k = desk.kpis()
    print(f"\n  selesai: ekuitas ${k['equity']:,.2f} ({k['pnl_pct']:+.2f}%) · "
          f"{k['trades']} trade · win rate {k['win_rate']:.1f}% · "
          f"expectancy {k['expectancy_pct']:+.2f}%/trade")
    jpath, mpath = write_social_report(desk)
    print(f"  laporan: {mpath}")
    print(f"  json   : {jpath}\n")
    return 0


def cmd_social_bench(args) -> int:
    print("\n  SOCIAL RADAR — apakah lapisan deteksi koordinasi layak dipakai?\n")
    rep = run_social_bench(ticks=args.ticks, seeds=args.seeds)
    for a in rep["results"]:
        print(f"  {a['arm']:>13} · {a['sessions']} sesi")
        print(f"      median PnL  : {a['median_pnl_pct']:+7.2f}%   "
              f"IQR {a['q1_pnl_pct']:+.2f}% .. {a['q3_pnl_pct']:+.2f}%")
        print(f"      rentang     : {a['min_pnl_pct']:+.2f}% .. {a['max_pnl_pct']:+.2f}%")
        print(f"      sesi profit : {a['profitable_sessions']}/{a['sessions']} · "
              f"win rate {a['avg_win_rate']:.1f}% · trade {a['avg_trades']:.0f} · "
              f"expectancy {a['avg_expectancy_pct']:+.2f}%/trade\n")

    base = {a["arm"]: a for a in rep["results"]}
    with_f = base["dirty+filter"]["median_pnl_pct"]
    no_f = base["dirty-filter"]["median_pnl_pct"]
    print(f"  Kesimpulan: di pasar yang sama, tanpa detektor koordinasi median "
          f"{no_f:+.2f}% vs {with_f:+.2f}% dengan detektor. "
          f"Selisih {with_f - no_f:+.2f} poin — itu nilai lapisan tersebut.\n")
    print("   • 'dirty-filter' = trader yang membaca jumlah mention saja. Bot farm")
    print("     membuat token naik 2-3 tick lalu menjatuhkannya; dia yang menanggung.")
    print("   • Angka ini mengukur mesin di pasar sintetis, bukan hasil di Solana.")
    print("   • Win rate di sini dihitung dari trade yang benar-benar dieksekusi,")
    print("     dibandingkan dengan ambang impas empiris (bukan target 70% di atas kertas).\n")

    out = Path(__file__).resolve().parent / "runs" / "social-bench.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rep, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  detail: {out}\n")
    return 0


def cmd_whale(args) -> int:
    from pathlib import Path as _P
    cfg = Config()
    cfg.whale_sim = WhaleSimConfig(
        start_balance=args.balance, ticks=args.ticks, seed=args.seed,
        edge_mode=args.whale_edge, tokens_per_tick=args.tokens_per_tick,
        tick_seconds_wall=0.0,
    )
    desk = WhaleDesk(cfg.whale_sim, cfg.whale, cfg.scalp)
    total = cfg.whale_sim.ticks
    step = max(1, total // 15)
    print(f"\n  WHALE RADAR · mode={cfg.whale_sim.edge_mode} · seed={cfg.whale_sim.seed}")
    print(f"  saldo ${cfg.whale_sim.start_balance:,.2f} · posisi {cfg.scalp.position_pct*100:.0f}% "
          f"· target +{cfg.scalp.take_profit_pct*100:.0f}% · stop -{cfg.scalp.stop_loss_pct*100:.0f}%")
    print(f"  hit-rate impas: {cfg.scalp.breakeven_hit_rate*100:.1f}%\n")
    while not desk.finished:
        desk.tick()
        if desk.tick_no % step == 0:
            k = desk.kpis()
            print(f"  [{desk.tick_no:>5}/{total}] ekuitas ${k['equity']:>10,.2f} "
                  f"({k['pnl_pct']:+7.2f}%) · whale tx {k['whale_tx']:>6,} · "
                  f"trade {k['trades']:>3} · hit {k['win_rate']:>4.1f}%")
    k = desk.kpis()
    jpath, mpath = write_whale_report(desk)
    print(f"\n  ekuitas akhir ${k['equity']:,.2f} ({k['pnl_pct']:+.2f}%) · "
          f"{k['trades']} trade · hit rate {k['win_rate']}% vs impas {k['breakeven_hit_rate']}% "
          f"· tahan {k['avg_hold_s']}s")
    print(f"  forensics p50 {k['latency_p50_ms']:.3f} ms · p95 {k['latency_p95_ms']:.3f} ms")
    print(f"  laporan: {mpath}\n")
    return 0


def cmd_whale_bench(args) -> int:
    import statistics as st
    print("\n  WHALE RADAR — uji jujur: apakah mengikuti whale lebih baik dari menebak?\n")
    rows = []
    for mode in ("informed", "noise"):
        pnls, wrs, trs = [], [], []
        for seed in range(1, args.seeds + 1):
            cfg = Config()
            cfg.whale_sim = WhaleSimConfig(start_balance=250.0, ticks=args.ticks,
                                           seed=seed, edge_mode=mode)
            d = WhaleDesk(cfg.whale_sim, cfg.whale, cfg.scalp)
            while not d.finished:
                d.tick()
            k = d.kpis()
            pnls.append(k["pnl_pct"]); wrs.append(k["win_rate"]); trs.append(k["trades"])
        pnls.sort()
        med = st.median(pnls)
        q1, q3 = pnls[len(pnls)//4], pnls[(3*len(pnls))//4]
        pos = sum(1 for p in pnls if p > 0)
        print(f"  {mode:>8} · {args.seeds} sesi")
        print(f"      median PnL  : {med:+7.1f}%")
        print(f"      rentang IQR : {q1:+.1f}% .. {q3:+.1f}%   (min {pnls[0]:+.1f}%, max {pnls[-1]:+.1f}%)")
        print(f"      sesi profit : {pos}/{args.seeds} · hit rate {st.mean(wrs):.1f}% "
              f"· trade {st.mean(trs):.0f}\n")
        rows.append({"mode": mode, "median_pnl_pct": round(med, 2), "q1": round(q1, 2),
                     "q3": round(q3, 2), "positive_sessions": pos,
                     "avg_win_rate": round(st.mean(wrs), 1), "avg_trades": round(st.mean(trs), 1),
                     "all_pnl_pct": [round(p, 2) for p in pnls]})

    scal = Config().scalp
    print(f"  Hit-rate impas pada target +{scal.take_profit_pct*100:.0f}% / stop "
          f"-{scal.stop_loss_pct*100:.0f}% dan biaya {scal.round_trip_cost_pct*100:.1f}%: "
          f"{scal.breakeven_hit_rate*100:.1f}%")
    print("   • informed: whale di generator benar-benar tahu token mana yang akan naik.")
    print("     Hasil positif mengukur apakah mesinnya bekerja — bukan bukti strategi")
    print("     ini profit di Solana sungguhan.")
    print("   • noise: whale memilih acak. Lapisan reputasi langsung mendeteksinya dan")
    print("     desk berhenti trading (perhatikan jumlah trade-nya nyaris nol).")
    print("     Itu perilaku yang benar: lebih baik tidak trading daripada ikut omong kosong.")
    print("   • Perhatikan kolom 'sinyal→+50%': itu kualitas sinyal mentah, sebelum")
    print("     biaya. Selisih antara angka itu dan hasil akhir adalah ongkos eksekusi.\n")

    out = Path(__file__).resolve().parent / "runs" / "whale-bench.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"ticks": args.ticks, "results": rows}, indent=2), encoding="utf-8")
    print(f"  detail: {out}\n")
    return 0


def cmd_whale_watch(args) -> int:
    """Pantau dompet whale SUNGGUHAN (baca saja, tanpa order)."""
    import os
    from pumpkin.whale_feed_live import HeliusWhaleMonitor, load_wallets

    key = os.environ.get("HELIUS_API_KEY", "")
    if not key:
        print("\n  HELIUS_API_KEY belum diset.\n"
              "  Daftar gratis di helius.dev, lalu:  export HELIUS_API_KEY=xxxx\n"
              "  (modul ini hanya membaca; tidak ada private key yang dipakai)\n")
        return 2
    wallets = load_wallets(args.wallets)
    mon = HeliusWhaleMonitor(wallets, key, poll_seconds=args.poll)
    mon.start()
    print(f"\n  memantau {len(wallets)} dompet · poll {args.poll}s · Ctrl+C untuk berhenti\n")
    try:
        while True:
            batch = mon.drain()
            for tx in batch:
                arrow = "BELI " if tx.side == "buy" else "JUAL "
                print(f"  [{time.strftime('%H:%M:%S')}] {tx.label:<18} {arrow} "
                      f"{tx.symbol:<12} ${tx.usd:>12,.0f}")
            if mon.errors:
                print(f"  ! {mon.errors[-1]}")
            time.sleep(1.0)
    except KeyboardInterrupt:
        mon.stop()
        print("\n  berhenti.\n")
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

    w = sub.add_parser("whale", help="jalankan Whale Radar headless")
    w.add_argument("--ticks", type=int, default=2400)
    w.add_argument("--balance", type=float, default=250.0)
    w.add_argument("--seed", type=int, default=21)
    w.add_argument("--whale-edge", choices=("informed", "noise"), default="informed")
    w.add_argument("--tokens-per-tick", type=int, default=6)
    w.set_defaults(func=cmd_whale)

    wb = sub.add_parser("whale-bench", help="bandingkan informed vs noise (whale)")
    wb.add_argument("--ticks", type=int, default=600)
    wb.add_argument("--seeds", type=int, default=10)
    wb.set_defaults(func=cmd_whale_bench)

    ww = sub.add_parser("whale-watch", help="pantau dompet whale sungguhan (butuh HELIUS_API_KEY)")
    ww.add_argument("--wallets", default="wallets.example.json")
    ww.add_argument("--poll", type=float, default=6.0)
    ww.set_defaults(func=cmd_whale_watch)


    so = sub.add_parser("social", help="jalankan Social Radar headless")
    so.add_argument("--ticks", type=int, default=1200)
    so.add_argument("--balance", type=float, default=250.0)
    so.add_argument("--seed", type=int, default=21)
    so.add_argument("--mode", choices=("dirty", "clean"), default="dirty")
    so.add_argument("--tokens-per-tick", type=int, default=6)
    so.set_defaults(func=cmd_social)

    sb = sub.add_parser("social-bench", help="bandingkan dengan vs tanpa detektor koordinasi")
    sb.add_argument("--ticks", type=int, default=1000)
    sb.add_argument("--seeds", type=int, default=10)
    sb.set_defaults(func=cmd_social_bench)

    v = sub.add_parser("serve", help="jalankan dashboard live")
    common(v)
    v.add_argument("--host", default="0.0.0.0")
    v.add_argument("--port", type=int, default=8000)
    v.add_argument("--tick-seconds", type=float, default=0.1)
    v.add_argument("--whale-edge", choices=("informed", "noise"), default="informed")
    v.add_argument("--whale-ticks", type=int, default=2400)
    v.add_argument("--whale-balance", type=float, default=250.0)
    v.add_argument("--social-mode", choices=("dirty", "clean"), default="dirty")
    v.add_argument("--social-ticks", type=int, default=1600)
    v.set_defaults(func=cmd_serve)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
