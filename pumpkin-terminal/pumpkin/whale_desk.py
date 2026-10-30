"""Whale Desk — mengikuti aliran dompet, menilai token, mengeksekusi scalp.

Alur satu tick:

    market → transaksi whale → agregasi sinyal (FlowAggregator)
           → forensics token (rug risk, dev %, bundle %)
           → keputusan SNIPER (5% ekuitas/posisi, target +50%)
           → eksekusi tertunda 1 tick (deteksi + analisis + inklusi tx)
           → GUARD mengawasi TP/SL/trailing/batas waktu
           → SCRIBE mencatat semuanya, termasuk sinyal yang ditolak
"""

from __future__ import annotations

import time
import uuid
from pathlib import Path

from .agents import Scribe
from .config import RUNS_DIR, ScalpRules, WhaleRules, WhaleSimConfig
from .forensics import DevLedger, Forensics
from .models import Event, Position, Trade
from .whale_market import MemeToken, WhaleMarket
from .whales import FlowAggregator, FlowSignal, WhaleRegistry


class WhaleDesk:
    def __init__(self, sim: WhaleSimConfig | None = None,
                 rules: WhaleRules | None = None,
                 scalp: ScalpRules | None = None,
                 run_dir: Path | None = None):
        self.sim = sim or WhaleSimConfig()
        self.rules = rules or WhaleRules()
        # Catatan penting: pada mode `noise` aturan TIDAK dilonggarkan.
        # Kalau whale-nya acak, lapisan reputasi akan menurunkan kepercayaan dan
        # desk berhenti trading dengan sendirinya. Itu hasil yang benar.
        self.scalp = scalp or ScalpRules()
        self.session_id = time.strftime("%Y%m%d-%H%M%S") + "-w" + uuid.uuid4().hex[:3]
        self.run_dir = run_dir or (RUNS_DIR / self.session_id)

        self.market = WhaleMarket(seed=self.sim.seed, tokens_per_tick=self.sim.tokens_per_tick,
                                  n_whales=self.sim.whales, edge_mode=self.sim.edge_mode)
        self.registry = WhaleRegistry()
        self.flow = FlowAggregator(window_ticks=self.rules.window_ticks,
                                   max_tokens=self.rules.max_tracked_tokens)
        self.ledger = DevLedger()
        self.forensics = Forensics(self.ledger)
        self.scribe = Scribe(self.run_dir)

        self.tick_no = 0
        self.start_balance = self.sim.start_balance
        self.cash = self.start_balance
        self.positions: dict[str, Position] = {}
        self.trades: list[Trade] = []
        self.equity_curve: list[tuple[int, float]] = []
        self.peak_equity = self.start_balance
        self.max_drawdown = 0.0
        self.fees_paid = 0.0

        self._queue: list[tuple[int, FlowSignal, float]] = []   # (tick, signal, risk)
        self._traded: set[str] = set()
        self._in_position: set[str] = set()
        self._pending_calls: dict[str, list[tuple[str, float, int]]] = {}
        self._signals_seen = 0
        # kualitas sinyal mentah: seberapa sering token yang kita ikuti benar-benar
        # mencapai +50% dari harga saat sinyal terlihat (terlepas dari exit policy)
        self._probes: list[dict] = []
        self._probe_total = 0
        self._probe_hit = 0
        self._rejected = {"rug_risk": 0, "reputasi": 0, "whale_kurang": 0, "likuiditas": 0}
        self.finished = False

    # ------------------------------------------------------------------ log
    def _log(self, agent: str, kind: str, message: str, **data) -> None:
        self.scribe.write(Event(tick=self.tick_no, agent=agent, kind=kind,
                                message=message, data=data))

    def _exit_cost(self) -> float:
        r = self.scalp
        return 1.0 - (1 - r.exit_slippage_pct) * (1 - r.exit_fee_pct)

    def equity(self) -> float:
        ec = self._exit_cost()
        mtm = sum(p.qty * p.last_price * (1 - ec) for p in self.positions.values())
        return self.cash + mtm

    # ----------------------------------------------------------------- tick
    def tick(self) -> None:
        if self.finished:
            return
        self.tick_no += 1

        fresh, txs = self.market.step(self.tick_no)
        for tok in fresh:
            self.ledger.register(tok.dev_address)

        # 1. serap aliran whale
        for tx in txs:
            self.flow.ingest(tx)
            if tx.side == "buy":
                self.registry.touch(tx)
                self._pending_calls.setdefault(tx.token, []).append(
                    (tx.whale, tx.price, self.tick_no))
            elif tx.label == "DEV RUG":
                self._log("FORENSICS", "rug", f"{tx.symbol} RUG · dev keluar ${tx.usd:,.0f}",
                          symbol=tx.symbol)
                self._register_rug(tx.token)
        if txs:
            buys = [t for t in txs if t.side == "buy"]
            self._log("RADAR", "flow",
                      f"{len(buys)} buy whale · ${sum(t.usd for t in buys):,.0f} "
                      f"dalam 1 tick" if buys else "aliran keluar", tx=len(txs))

        # 2. selesaikan panggilan whale (untuk reputasi)
        self._resolve_calls()
        self._update_probes()

        # 3. buang sinyal kedaluwarsa
        self.flow.prune(self.tick_no)

        # 4. GUARD
        for addr, pos in list(self.positions.items()):
            tok = self.market.tokens.get(addr)
            if tok is None:
                self._close(pos, pos.last_price, "token_mati")
                continue
            pos.last_price = tok.price
            if tok.price > pos.peak_price:
                pos.peak_price = tok.price
                pos.peak_gain_pct = (tok.price - pos.entry_price) / pos.entry_price
            reason = self._guard(pos)
            if reason:
                self._close(pos, tok.price, reason)

        # 5. eksekusi antrean (yang sudah tiba waktunya)
        due = [q for q in self._queue if q[0] <= self.tick_no]
        self._queue = [q for q in self._queue if q[0] > self.tick_no]
        for _, signal, risk in due:
            self._execute(signal, risk)

        # 6. SINYAL baru
        self._scan()

        # 7. ekuitas
        eq = self.equity()
        if self.tick_no % 4 == 0:
            self.equity_curve.append((self.tick_no, round(eq, 2)))
        self.peak_equity = max(self.peak_equity, eq)
        if self.peak_equity:
            self.max_drawdown = max(self.max_drawdown,
                                    (self.peak_equity - eq) / self.peak_equity)

        if self.tick_no >= self.sim.ticks:
            self._finish()

    # ------------------------------------------------------------- sinyal
    def _scan(self) -> None:
        if len(self.positions) + len(self._queue) >= self.scalp.max_concurrent:
            return
        for sig in self.flow.top_signals(self.tick_no, self.registry, n=12):
            if sig.token in self._traded or sig.token in self._in_position:
                continue
            tok = self.market.tokens.get(sig.token)
            if tok is None or tok.state == "dump":
                continue
            if sig.signal < self.rules.min_signal:
                continue
            if len(sig.whales) < self.rules.min_whales_confirm:
                self._rejected["whale_kurang"] += 1
                continue
            if sig.net_usd < self.rules.min_net_inflow_usd:
                continue
            if sig.avg_reputation < self.rules.min_whale_reputation:
                self._rejected["reputasi"] += 1
                self._log("RADAR", "reject",
                          f"SINYAL {tok.symbol} diabaikan · reputasi {sig.avg_reputation:.2f}")
                continue

            report = self.forensics.analyze(tok)
            self._signals_seen += 1
            if report.rug_risk > self.rules.max_rug_risk:
                self._rejected["rug_risk"] += 1
                self._log("FORENSICS", "reject",
                          f"{tok.symbol} rug risk {report.rug_risk:.2f} · "
                          f"{', '.join(report.findings[:2]) or 'konsentrasi'}")
                continue
            self._log("FORENSICS", "pass",
                      f"{tok.symbol} aman (risk {report.rug_risk:.2f}) · "
                      f"dev {report.dev_pct:.1f}% · bundle {report.bundle_pct:.1f}% "
                      f"· {report.latency_ms:.1f} ms")
            sig.price = tok.price
            self._log("RADAR", "signal",
                      f"{tok.symbol}: {len(sig.whales)} whale · "
                      f"${sig.net_usd:,.0f} · sinyal {sig.signal:.2f}")
            self._queue.append((self.tick_no + self.rules.entry_delay_ticks, sig,
                                report.rug_risk))
            self._probes.append({"token": tok.address, "price": tok.price,
                                 "tick": self.tick_no, "hit": False})
            self._probe_total += 1
            self._traded.add(sig.token)
            if len(self.positions) + len(self._queue) >= self.scalp.max_concurrent:
                return

    # ------------------------------------------------------------ eksekusi
    def _execute(self, sig: FlowSignal, risk: float) -> None:
        tok = self.market.tokens.get(sig.token)
        if tok is None or tok.state == "dump":
            return
        # Disiplin: jangan mengejar. Kalau harga sudah lari lebih dari
        # `max_chase_pct` sejak sinyal terlihat, kita sudah terlambat.
        ref = getattr(sig, "price", 0.0) or tok.price
        if ref > 0 and tok.price > ref * (1 + self.rules.max_chase_pct):
            self._rejected["terlalu_telat"] = self._rejected.get("terlalu_telat", 0) + 1
            self._log("SNIPER", "reject",
                      f"{tok.symbol} dilewati · harga sudah +{(tok.price/ref-1)*100:.1f}% "
                      f"sejak sinyal")
            return
        equity = self.equity()
        size = equity * self.scalp.position_pct
        size = min(size, tok.liquidity_usd * self.scalp.max_pct_of_liquidity)
        if size < 1.0 or size > self.cash:
            self._rejected["likuiditas"] += 1
            return
        r = self.scalp
        slip = r.entry_slippage_pct + min(0.03, sig.signal * 0.02)
        entry_price = tok.price * (1 + slip)
        qty = size * (1 - r.entry_fee_pct) / entry_price
        self.cash -= size
        self.fees_paid += size * r.entry_fee_pct

        self.positions[tok.address] = Position(
            id=len(self.trades) + len(self.positions) + 1, address=tok.address,
            symbol=tok.symbol, qty=qty, entry_price=entry_price,
            entry_tick=self.tick_no, cost_usd=size, score=sig.signal,
            peak_price=entry_price, last_price=tok.price,
        )
        self._in_position.add(tok.address)
        self._log("SNIPER", "enter",
                  f"BELI {tok.symbol} ${size:,.2f} (5% ekuitas) · sinyal {sig.signal:.2f} "
                  f"· target +50%", symbol=tok.symbol, usd=round(size, 2),
                  price=tok.price, signal=round(sig.signal, 3))

    def _guard(self, pos: Position) -> str | None:
        r = self.scalp
        price = pos.last_price
        gain = (price - pos.entry_price) / pos.entry_price
        dd = (price - pos.peak_price) / pos.peak_price if pos.peak_price else 0.0

        if gain >= r.take_profit_pct:
            return "take_profit_50"
        if gain <= -r.stop_loss_pct:
            return "stop_loss"
        if pos.peak_gain_pct >= r.trail_after_pct and dd <= -r.trail_distance_pct:
            return "trailing"
        if self.tick_no - pos.entry_tick >= r.max_hold_ticks:
            return "time_stop"
        return None

    def _exit_slippage(self, pos: Position, price: float, reason: str) -> float:
        """Saat semua orang keluar bersamaan, stop-loss tidak terisi di harganya."""
        r = self.scalp
        tok = self.market.tokens.get(pos.address)
        slip = r.exit_slippage_pct
        if tok is not None and (tok.rugged or tok.state == "dump"):
            slip += 0.09 + 0.07 * min(1.0, abs(pos.peak_gain_pct))
        elif reason in ("token_mati", "session_end"):
            slip += 0.06
        return min(0.45, slip)

    def _close(self, pos: Position, price: float, reason: str) -> None:
        r = self.scalp
        exit_price = price * (1 - self._exit_slippage(pos, price, reason))
        proceeds = pos.qty * exit_price * (1 - r.exit_fee_pct)
        fee = pos.qty * exit_price * r.exit_fee_pct
        pnl = proceeds - pos.cost_usd
        self.cash += proceeds
        self.fees_paid += fee
        hold = self.tick_no - pos.entry_tick
        self.positions.pop(pos.address, None)
        self._in_position.discard(pos.address)
        self.trades.append(Trade(
            id=len(self.trades) + 1, address=pos.address, symbol=pos.symbol,
            score=pos.score, entry_price=pos.entry_price, exit_price=exit_price,
            size_usd=pos.cost_usd, pnl_usd=pnl, pnl_pct=pnl / pos.cost_usd,
            reason=reason, entry_tick=pos.entry_tick, exit_tick=self.tick_no,
            hold_ticks=hold, fees_usd=fee,
        ))
        self._log("GUARD", "exit",
                  f"JUAL {pos.symbol} {pnl/pos.cost_usd*100:+.1f}% (${pnl:+.2f}) · "
                  f"{reason} · tahan {hold*self.sim.sim_seconds_per_tick}s",
                  symbol=pos.symbol, pnl=round(pnl, 2), reason=reason)

    # -------------------------------------------------------- reputasi whale
    def _resolve_calls(self) -> None:
        for token, calls in list(self._pending_calls.items()):
            tok = self.market.tokens.get(token)
            still = []
            for whale, entry, tick in calls:
                if tok is None:
                    self.registry.mark(whale, False)
                elif tok.price >= entry * (1 + self.scalp.take_profit_pct):
                    self.registry.mark(whale, True)
                elif tok.state == "dump" or self.tick_no - tick > self.scalp.max_hold_ticks:
                    self.registry.mark(whale, False)
                else:
                    still.append((whale, entry, tick))
            if still:
                self._pending_calls[token] = still
            else:
                self._pending_calls.pop(token, None)

    def _update_probes(self) -> None:
        keep = []
        for p in self._probes:
            tok = self.market.tokens.get(p["token"])
            if tok is None:
                continue
            if tok.price >= p["price"] * (1 + self.scalp.take_profit_pct):
                if not p["hit"]:
                    p["hit"] = True
                    self._probe_hit += 1
                continue
            if self.tick_no - p["tick"] > self.scalp.max_hold_ticks:
                continue
            keep.append(p)
        self._probes = keep

    def _register_rug(self, token: str) -> None:
        tok = self.market.tokens.get(token)
        if tok:
            self.ledger.mark_rug(tok.dev_address)

    def _finish(self) -> None:
        for addr, pos in list(self.positions.items()):
            tok = self.market.tokens.get(addr)
            self._close(pos, tok.price if tok else pos.last_price, "session_end")
        self.finished = True
        self._log("SCRIBE", "info", "Sesi selesai · semua posisi ditutup")
        self.scribe.close()

    # ---------------------------------------------------------------- KPI
    def kpis(self) -> dict:
        eq = equity = self.equity()
        wins = [t for t in self.trades if t.pnl_usd > 0]
        losses = [t for t in self.trades if t.pnl_usd <= 0]
        tp = [t for t in self.trades if t.reason == "take_profit_50"]
        holds = [t.hold_ticks for t in self.trades]
        avg_win = sum(t.pnl_pct for t in wins) / len(wins) if wins else 0.0
        avg_loss = abs(sum(t.pnl_pct for t in losses) / len(losses)) if losses else 0.0
        emp_be = avg_loss / (avg_win + avg_loss) if (avg_win + avg_loss) else 1.0
        expectancy = (sum(t.pnl_pct for t in self.trades) / len(self.trades)
                      if self.trades else 0.0)
        lat = self.forensics.latency_stats()
        return {
            "session_id": self.session_id,
            "tick": self.tick_no,
            "ticks_total": self.sim.ticks,
            "sim_minutes": round(self.tick_no * self.sim.sim_seconds_per_tick / 60, 1),
            "equity": round(equity, 2),
            "cash": round(self.cash, 2),
            "start_balance": round(self.start_balance, 2),
            "pnl_usd": round(equity - self.start_balance, 2),
            "pnl_pct": round((equity / self.start_balance - 1) * 100, 2),
            "trades": len(self.trades),
            "wins": len(wins),
            "losses": len(losses),
            "win_rate": round(len(wins) / len(self.trades) * 100, 1) if self.trades else 0.0,
            "breakeven_hit_rate": round(self.scalp.breakeven_hit_rate * 100, 1),
            "avg_win_pct": round(avg_win * 100, 2),
            "avg_loss_pct": round(-avg_loss * 100, 2),
            "empirical_breakeven": round(emp_be * 100, 1),
            "expectancy_pct": round(expectancy * 100, 3),
            "tp_hits": len(tp),
            "avg_hold_s": round(sum(holds) / len(holds) * self.sim.sim_seconds_per_tick, 1)
            if holds else 0.0,
            "fees_paid": round(self.fees_paid, 2),
            "max_drawdown_pct": round(self.max_drawdown * 100, 2),
            "open_positions": len(self.positions),
            "queued": len(self._queue),
            "signals": self._signals_seen,
            "signal_hit_rate": round(self._probe_hit / self._probe_total * 100, 1)
            if self._probe_total else 0.0,
            "signal_probes": self._probe_total,
            "rejected": dict(self._rejected),
            "whale_tx": self.flow.stats()["tx"],
            "whale_volume": self.flow.stats()["buy_usd"],
            "tokens_scanned": self.market.scanned,
            "latency_p50_ms": lat["p50"],
            "latency_p95_ms": lat["p95"],
            "edge_mode": self.sim.edge_mode,
            "finished": self.finished,
            "position_pct": self.scalp.position_pct * 100,
            "tp_pct": self.scalp.take_profit_pct * 100,
            "sl_pct": self.scalp.stop_loss_pct * 100,
        }

    def snapshot(self) -> dict:
        ec = self._exit_cost()
        signals = self.flow.top_signals(self.tick_no, self.registry, n=6)
        return {
            "kpis": self.kpis(),
            "positions": [{
                "symbol": p.symbol,
                "size_usd": round(p.cost_usd, 2),
                "entry_price": p.entry_price,
                "price": p.last_price,
                "unrealized_pct": round((p.qty * p.last_price * (1 - ec) / p.cost_usd - 1) * 100, 2),
                "progress": round(max(0.0, min(1.0,
                    (p.last_price / p.entry_price - 1) / self.scalp.take_profit_pct)), 3),
                "peak_pct": round(p.peak_gain_pct * 100, 2),
                "age_s": (self.tick_no - p.entry_tick) * self.sim.sim_seconds_per_tick,
                "target_s": self.scalp.max_hold_ticks * self.sim.sim_seconds_per_tick,
                "signal": round(p.score, 2),
            } for p in self.positions.values()],
            "signals": [s.public() for s in signals],
            "trades": [t.public() for t in self.trades[-20:]][::-1],
            "leaderboard": self.registry.leaderboard(8, min_samples=1),
            "whales": self.registry.stats(),
            "ledger": self.ledger.stats(),
            "equity_curve": self.equity_curve[-400:],
            "config": {
                "position_pct": self.scalp.position_pct * 100,
                "take_profit_pct": self.scalp.take_profit_pct * 100,
                "stop_loss_pct": self.scalp.stop_loss_pct * 100,
                "breakeven_hit_rate": round(self.scalp.breakeven_hit_rate * 100, 1),
                "round_trip_cost_pct": round(self.scalp.round_trip_cost_pct * 100, 2),
                "entry_delay_ticks": self.rules.entry_delay_ticks,
                "max_chase_pct": round(self.rules.max_chase_pct * 100, 1),
                "min_whales_confirm": self.rules.min_whales_confirm,
                "sim_seconds_per_tick": self.sim.sim_seconds_per_tick,
            },
        }


# --------------------------------------------------------------------------- #
# Laporan
# --------------------------------------------------------------------------- #
def build_whale_report(desk: WhaleDesk) -> dict:
    k = desk.kpis()
    return {
        "session_id": desk.session_id,
        "kpis": k,
        "config": {
            "position_pct": desk.scalp.position_pct,
            "take_profit_pct": desk.scalp.take_profit_pct,
            "stop_loss_pct": desk.scalp.stop_loss_pct,
            "max_hold_ticks": desk.scalp.max_hold_ticks,
            "round_trip_cost_pct": desk.scalp.round_trip_cost_pct,
            "breakeven_hit_rate": desk.scalp.breakeven_hit_rate,
            "entry_delay_ticks": desk.rules.entry_delay_ticks,
            "min_whales_confirm": desk.rules.min_whales_confirm,
            "max_rug_risk": desk.rules.max_rug_risk,
            "edge_mode": desk.sim.edge_mode,
            "seed": desk.sim.seed,
            "sim_seconds_per_tick": desk.sim.sim_seconds_per_tick,
        },
        "trades": [t.public() for t in desk.trades],
        "whale_leaderboard": desk.registry.leaderboard(15, min_samples=1),
        "whale_stats": desk.registry.stats(),
        "dev_ledger": desk.ledger.stats(),
        "rejected": dict(desk._rejected),
        "disclaimer": (
            "PAPER TRADING / SIMULASI. Tidak ada wallet, private key, atau order on-chain. "
            "Aliran whale pada mode simulasi dihasilkan generator, bukan dari jaringan Solana."
        ),
    }


def render_whale_markdown(d: dict) -> str:
    k, c = d["kpis"], d["config"]
    rows = "\n".join(
        f"| {t['symbol']} | {t['score']:.2f} | ${t['size_usd']:.2f} | {t['pnl_pct']:+.1f}% "
        f"| ${t['pnl_usd']:+.2f} | {t['hold_ticks'] * c['sim_seconds_per_tick']:.0f}s | {t['reason']} |"
        for t in d["trades"]
    ) or "| — | — | — | — | — | — | — |"

    whales = "\n".join(
        f"| `{w['address']}` | {w['label']} | {w['hits']} | {w['misses']} | "
        f"{w['reputation']:.2f} | ${w['usd_seen']:,.0f} |"
        for w in d["whale_leaderboard"]
    ) or "| — | — | — | — | — | — |"

    edge = "**ya**" if k["win_rate"] > k["breakeven_hit_rate"] else "**tidak**"

    return f"""# Whale Radar — Laporan Sesi `{d['session_id']}`

> ⚠️ **Simulasi.** Tidak ada wallet, private key, atau order on-chain.
> Mode `{c['edge_mode']}`. Pada mode `informed`, whale di generator memang punya
> informasi; pada mode `noise` mereka memilih acak. Angka di bawah mengukur
> mesinnya, bukan pasar sungguhan.

## Ringkasan

| Metrik | Nilai |
|---|---|
| Saldo awal | ${k['start_balance']:,.2f} |
| Ekuitas akhir | ${k['equity']:,.2f} |
| PnL | ${k['pnl_usd']:+,.2f} ({k['pnl_pct']:+.2f}%) |
| Posisi per trade | {c['position_pct']*100:.0f}% ekuitas |
| Target / Stop | +{c['take_profit_pct']*100:.0f}% / −{c['stop_loss_pct']*100:.0f}% |
| Trade | {k['trades']} (W {k['wins']} / L {k['losses']}) |
| **Hit rate** | **{k['win_rate']:.1f}%** |
| **Hit rate impas** | **{k['breakeven_hit_rate']:.1f}%** (biaya {c['round_trip_cost_pct']*100:.1f}%) |
| Menguntungkan? | {edge} |
| TP +50% tercapai | {k['tp_hits']} trade |
| Rata-rata tahan | {k['avg_hold_s']:.1f} detik pasar |
| Fee dibayar | ${k['fees_paid']:,.2f} |
| Max drawdown | {k['max_drawdown_pct']:.2f}% |
| Token dipindai | {k['tokens_scanned']:,} |
| Transaksi whale | {k['whale_tx']:,} |
| Latency forensics | p50 {k['latency_p50_ms']:.3f} ms · p95 {k['latency_p95_ms']:.3f} ms |
| Ditolak forensics | {d['rejected'].get('rug_risk', 0)} sinyal (rug risk) |
| Ditolak reputasi | {d['rejected'].get('reputasi', 0)} sinyal |

## Whale terbaik (dipelajari selama sesi)

| Dompet | Label | Hit | Miss | Reputasi | Volume |
|---|---|---|---|---|---|
{whales}

## Trade

| Token | Sinyal | Ukuran | PnL % | PnL $ | Tahan | Exit |
|---|---|---|---|---|---|---|
{rows}

## Catatan

- Hit rate {k['win_rate']:.1f}% vs impas {k['breakeven_hit_rate']:.1f}%: dengan target
  +50% dan stop −20%, kamu **harus** menang lebih dari {k['breakeven_hit_rate']:.0f}%
  hanya untuk tidak merugi — biaya round-trip {c['round_trip_cost_pct']*100:.1f}% masuk
  ke kedua sisi.
- Entry selalu tertunda {c['entry_delay_ticks']} tick setelah whale terdeteksi
  (deteksi + forensics + inklusi transaksi). Kamu membeli setelah harga naik.
- Forensics menolak {d['rejected'].get('rug_risk', 0)} token. Tanpa lapisan itu,
  satu rug −90% menghapus puluhan kemenangan.
"""


def write_whale_report(desk: WhaleDesk, out_dir: Path | None = None) -> tuple[Path, Path]:
    import json

    out = out_dir or desk.run_dir
    out.mkdir(parents=True, exist_ok=True)
    data = build_whale_report(desk)
    jpath = out / "whale-report.json"
    mpath = out / "whale-report.md"
    jpath.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    mpath.write_text(render_whale_markdown(data), encoding="utf-8")
    return jpath, mpath
