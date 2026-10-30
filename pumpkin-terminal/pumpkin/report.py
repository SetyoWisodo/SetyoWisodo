"""Laporan akhir sesi: JSON untuk mesin, Markdown untuk manusia."""

from __future__ import annotations

import json
from pathlib import Path

from .engine import Desk

HONESTY = """\
> ⚠️ **Baca ini dulu.** Angka di laporan ini berasal dari **simulasi**
> (`edge_mode = {mode}`), bukan dari uang nyata dan bukan bukti bahwa strategi
> ini profitable. Pada mode `correlated`, generator pasar sengaja menciptakan
> akumulasi harga sebelum lonjakan, jadi momentum yang dibaca ANALYST memang
> punya arti — agen punya sinyal untuk "dimenangkan". Pada mode `null`, semua
> keahlian dimatikan (FILTER dilewati, skor acak) dan hasilnya menunjukkan
> ongkos sesungguhnya: fee + slippage, ditambah rug yang menembus stop-loss.
"""


def build_report(desk: Desk) -> dict:
    k = desk.kpis()
    trades = [t.public() for t in desk.trades]
    return {
        "session_id": desk.session_id,
        "generated_at": desk.session_id[:8],
        "config": desk.cfg.to_dict(),
        "kpis": k,
        "agent_activity": {
            "scout": desk.scout.stats(),
            "filter": desk.filter.stats(),
            "analyst": desk.analyst.stats(),
            "sniper": desk.sniper.stats(),
            "guard": desk.guard.stats(),
            "scribe": desk.scribe.stats(),
        },
        "trades": trades,
        "equity_curve": desk.equity_curve,
        "disclaimer": (
            "PAPER TRADING / SIMULASI. Tidak ada wallet, tidak ada order on-chain. "
            "Hasil sintetis tidak boleh dipakai sebagai ekspektasi return nyata."
        ),
    }


def write_report(desk: Desk, out_dir: Path | None = None) -> tuple[Path, Path]:
    out = out_dir or desk.run_dir
    out.mkdir(parents=True, exist_ok=True)
    data = build_report(desk)
    jpath = out / "report.json"
    jpath.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    mpath = out / "report.md"
    mpath.write_text(render_markdown(data), encoding="utf-8")
    return jpath, mpath


def render_markdown(d: dict) -> str:
    k, c = d["kpis"], d["config"]
    r, s = c["risk"], c["sim"]
    rows = "\n".join(
        f"| {t['symbol']} | {t['score']:.2f} | ${t['size_usd']:.2f} | "
        f"{t['pnl_pct']:+.2f}% | ${t['pnl_usd']:+.2f} | {t['reason']} |"
        for t in d["trades"]
    ) or "| — | — | — | — | — | — |"

    return f"""# Pumpkin Terminal — Laporan Sesi `{d['session_id']}`

{HONESTY.format(mode=s['edge_mode'])}

## Ringkasan

| Metrik | Nilai |
|---|---|
| Saldo awal | ${k['start_balance']:,.2f} |
| Ekuitas akhir | ${k['equity']:,.2f} |
| PnL | ${k['pnl_usd']:+,.2f} ({k['pnl_pct']:+.2f}%) |
| Pair dipindai | {k['scanned']:,} |
| Ditolak | {k['rejected']:,} ({k['rejection_rate']:.1f}%) |
| Trade | {k['trades']} (W {k['wins']} / L {k['losses']}, win-rate {k['win_rate']}%) |
| Expectancy per trade | ${k['expectancy']:+.3f} |
| Fee dibayar | ${k['fees_paid']:,.2f} |
| Max drawdown | {k['max_drawdown_pct']:.2f}% |
| Waktu pasar tersimulasi | {k['sim_minutes']:.1f} menit (dipadatkan) |

## Konfigurasi

- Filter: liq ≥ ${c['filters']['min_liquidity_usd']:,.0f}, holder ≥ {c['filters']['min_holders']},
  top-10 ≤ {c['filters']['max_top10_pct']:.0f}%, dev ≤ {c['filters']['max_dev_pct']:.0f}%,
  mint revoked = {c['filters']['require_mint_revoked']}, LP locked = {c['filters']['require_lp_locked']}
- Risiko: maks {r['max_position_pct']*100:.0f}% saldo/posisi, maks {r['max_concurrent']} posisi,
  SL -{r['stop_loss_pct']*100:.0f}%, trailing setelah +{r['trail_after_pct']*100:.0f}%
  (jarak {r['trail_distance_pct']*100:.0f}%), hold maks {r['max_hold_ticks']} tick
- Biaya: fee masuk {r['entry_fee_pct']*100:.1f}%, fee keluar {r['exit_fee_pct']*100:.1f}%,
  slippage masuk {r['entry_slippage_pct']*100:.1f}%, slippage keluar {r['exit_slippage_pct']*100:.1f}%
  → **round-trip {r['round_trip_cost_pct']*100:.1f}%**
- Ambang skor ANALYST: {r['min_score']}
- Mode: `{s['edge_mode']}`, seed {s['seed']}, {s['ticks']:,} tick

## Trade

| Token | Skor | Ukuran | PnL % | PnL $ | Exit |
|---|---|---|---|---|---|
{rows}

## Aktivitas agen

```json
{json.dumps(d['agent_activity'], indent=2, ensure_ascii=False)}
```

## Catatan

- Setiap penolakan tercatat di `events.jsonl` — filternya bisa diaudit.
- Round-trip cost {r['round_trip_cost_pct']*100:.1f}% berarti strategi harus menang
  lebih dari itu hanya untuk kembali ke titik nol.
- Jangan pernah menaikkan `max_position_pct` atau mematikan stop-loss untuk
  "mengejar" angka di thread media sosial.
"""
