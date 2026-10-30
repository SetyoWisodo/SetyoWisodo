"""Social Desk — mesin yang menolak kalah.

Aturan main:

1. **Tidak ada trade tanpa probabilitas.** Setiap kandidat harus punya p̂ ≥ 0,72,
   EV ≥ 2× biaya, dan upside realistis ≥ target. Kalau tidak, dilewati.
2. **Target diturunkan dari biaya**, bukan dari harapan (`required_tp`).
3. **Ukuran dari Kelly, dipotong ¼**, dan dibatasi 5% ekuitas.
4. **Exit bertingkat**: separuh di 60% target, sisanya di target, stop keras 6%.
5. **Batas rugi harian** mematikan mesin sebelum satu hari buruk jadi bencana.
6. **Modal ditarik ke vault** saat ekuitas 2×; setelah itu semua trading memakai
   uang profit ("free trading") — risiko terhadap modal = 0 secara struktural.
"""

from __future__ import annotations

import math
import time
import uuid
from pathlib import Path

from .agents import Scribe
from .config import RUNS_DIR, SocialRules, SocialSimConfig
from .forensics import DevLedger, Forensics
from .journal import Journal
from .models import Event, Trade
from .social_market import SocialMarket
from .social_signal import (AlphaEngine, InfluenceGraph, SocialAggregator,
                            SocialPost, SocialSignal)


class LivePosition:
    __slots__ = ("address", "symbol", "qty", "entry_price", "entry_tick", "cost_usd",
                 "initial_qty", "peak_price", "last_price", "realized", "tp1_done",
                 "p_win", "ev_pct", "tp", "sl", "features", "fees", "initial_cost")

    def __init__(self, address: str, symbol: str, qty: float, entry_price: float,
                 entry_tick: int, cost_usd: float, p_win: float, ev_pct: float,
                 tp: float, sl: float, features: dict):
        self.address = address
        self.symbol = symbol
        self.qty = qty
        self.initial_qty = qty
        self.entry_price = entry_price
        self.entry_tick = entry_tick
        self.cost_usd = cost_usd
        self.initial_cost = cost_usd
        self.peak_price = entry_price
        self.last_price = entry_price
        self.realized = 0.0
        self.tp1_done = False
        self.p_win = p_win
        self.ev_pct = ev_pct
        self.tp = tp
        self.sl = sl
        self.features = features
        self.fees = 0.0

    @property
    def gain(self) -> float:
        return (self.last_price - self.entry_price) / self.entry_price

    def market_value(self, exit_cost_pct: float) -> float:
        return self.qty * self.last_price * (1 - exit_cost_pct)


class SocialDesk:
    def __init__(self, sim: SocialSimConfig | None = None,
                 rules: SocialRules | None = None,
                 run_dir: Path | None = None):
        self.sim = sim or SocialSimConfig()
        self.rules = rules or SocialRules()
        self.session_id = time.strftime("%Y%m%d-%H%M%S") + "-s" + uuid.uuid4().hex[:3]
        self.run_dir = run_dir or (RUNS_DIR / self.session_id)

        self.market = SocialMarket(
            seed=self.sim.seed, tokens_per_tick=self.sim.tokens_per_tick,
            n_whales=self.sim.whales, edge_mode="informed",
            n_kols=self.sim.kols, n_bots=self.sim.bots,
            bot_farms=(self.sim.mode == "dirty"),
        )
        self.graph = InfluenceGraph()
        self.social = SocialAggregator(window=8)
        self.ledger = DevLedger()
        self.forensics = Forensics(self.ledger)
        self.alpha = AlphaEngine(
            cost_round_trip=self.rules.cost_round_trip,
            min_p_win=self.rules.min_p_win,
            max_coordination=self.rules.max_coordination,
            max_size_pct=self.rules.max_position_pct,
            stop_loss=self.rules.stop_loss,
            min_tp=self.rules.min_tp,
            max_tp=self.rules.max_tp,
        )
        self.scribe = Scribe(self.run_dir)
        self.journal = Journal(self.run_dir / "trades.db")

        self.tick_no = 0
        self.start_balance = self.sim.start_balance
        self.cash = self.start_balance
        self.vault_locked = 0.0
        self.principal = self.start_balance
        self.positions: dict[str, LivePosition] = {}
        self.trades: list[Trade] = []
        self.equity_curve: list[tuple[int, float]] = []
        self.peak_equity = self.start_balance
        self.max_drawdown = 0.0
        self.fees_paid = 0.0

        self._queue: list[tuple[int, object]] = []
        self._traded: set[str] = set()
        self._pending_calls: dict[str, list[str]] = {}
        self._price_hist: dict[str, list[float]] = {}
        self._by_symbol: dict[str, object] = {}
        self._decisions: list[dict] = []
        self._rejected: dict[str, int] = {}
        self._news_seen = 0
        self._regime = 0.6
        self._day_start_equity = self.start_balance
        self._day_start_tick = 0
        self._day_pnl = 0.0
        self._halted_until = 0
        self.finished = False
        self._signal_probes: list[dict] = []
        self._probe_total = 0
        self._probe_hit = 0
        self._p_log: list[float] = []

    # ------------------------------------------------------------------ util
    def _log(self, agent: str, kind: str, message: str, **data) -> None:
        self.scribe.write(Event(tick=self.tick_no, agent=agent, kind=kind,
                                message=message, data=data))

    def _bump(self, key: str) -> None:
        self._rejected[key] = self._rejected.get(key, 0) + 1

    def _exit_cost(self) -> float:
        return self.rules.cost_round_trip / 2.0

    def equity(self) -> float:
        ec = self._exit_cost()
        mtm = sum(p.market_value(ec) for p in self.positions.values())
        return self.cash + mtm

    def total_equity(self) -> float:
        return self.equity() + self.vault_locked

    # ------------------------------------------------------------------ tick
    def tick(self) -> None:
        if self.finished:
            return
        self.tick_no += 1
        fresh, txs, posts, news = self.market.step(self.tick_no)

        self._ingest_social(posts)
        self._ingest_news(news)
        self._update_prices()
        self._update_day()

        for pos in list(self.positions.values()):
            self._manage(pos)

        self._exec_queue()
        self._scan()
        self._resolve_calls()
        self._update_probes()
        self._sample()

        if self.tick_no >= self.sim.ticks:
            self._finish()

    # ---------------------------------------------------------------- sosial
    def _ingest_social(self, posts: list[SocialPost]) -> None:
        if not posts:
            return
        for p in posts:
            self.graph.upsert(p)
        self.social.ingest(posts)
        bots = sum(1 for p in posts if p.is_bot)
        if bots:
            self._log("SOCIAL", "bots", f"{bots} post bot terdeteksi dalam 1 tick")
        if posts:
            top = max(posts, key=lambda p: p.engagement)
            self._log("SOCIAL", "post",
                      f"{top.author} ({top.followers:,} f) · "
                      f"{top.tickers[0] if top.tickers else '—'} · "
                      f"{top.engagement:,} engagement")

    def _ingest_news(self, news: list) -> None:
        if len(news) <= self._news_seen:
            return
        for ev in news[self._news_seen:]:
            self._regime = min(1.0, max(0.0, self._regime + 0.25 * ev.direction))
            self._log("NEWS", "news",
                      f"[{ev.kind}] {ev.headline} · rezim {self._regime:.2f}")
            self.journal.record_news(session=self.session_id, tick=self.tick_no,
                                     kind=ev.kind, direction=ev.direction,
                                     headline=ev.headline)
        self._news_seen = len(news)

    def _update_prices(self) -> None:
        for addr, pos in self.positions.items():
            tok = self.market.tokens.get(addr)
            if tok is None:
                continue
            pos.last_price = tok.price
            pos.peak_price = max(pos.peak_price, tok.price)
        for addr, tok in list(self.market.tokens.items()):
            if not tok.dead:
                cur = self._by_symbol.get(tok.symbol)
                if cur is None or tok.created_tick >= cur.created_tick:
                    self._by_symbol[tok.symbol] = tok
            h = self._price_hist.setdefault(addr, [])
            h.append(tok.price)
            if len(h) > 4:
                h.pop(0)
        if len(self._price_hist) > 2_000:
            self._price_hist = dict(list(self._price_hist.items())[-1_200:])

    # --------------------------------------------------------------- eksekusi
    def _exec_queue(self) -> None:
        due = [q for q in self._queue if q[0] <= self.tick_no]
        self._queue = [q for q in self._queue if q[0] > self.tick_no]
        for _, decision in due:
            self._open(decision)

    def _open(self, d) -> None:
        tok = self.market.tokens.get(d.token)
        if tok is None or tok.state == "dump" or self.tick_no < self._halted_until:
            return
        if d.token in self.positions:      # sudah punya posisi di token ini
            return
        if len(self.positions) >= self.rules.max_concurrent:
            self._bump("slot_penuh")
            return
        equity = self.equity()
        size = min(equity * d.size_pct, tok.liquidity_usd * self.rules.max_pct_of_liquidity)
        size = min(size, self.cash)
        if size < 1.0:
            self._bump("kas_kurang")
            return

        entry_price = tok.price * (1 + 0.015)
        fee = size * 0.01
        qty = (size - fee) / entry_price
        self.cash -= size
        self.fees_paid += fee

        self.positions[d.token] = LivePosition(
            address=d.token, symbol=d.symbol, qty=qty, entry_price=entry_price,
            entry_tick=self.tick_no, cost_usd=size, p_win=d.p_win, ev_pct=d.ev_pct,
            tp=d.take_profit, sl=d.stop_loss, features={
                "social": d.features["social"], "coordination": d.features["coordination"],
                "safety": d.features["safety"], "momentum": d.features["momentum"],
                "regime": d.features["regime"], "liquidity": d.features["liquidity"]},
        )
        self._log("SNIPER", "enter",
                  f"BELI {d.symbol} ${size:,.2f} · p̂ {d.p_win:.2f} · EV {d.ev_pct*100:+.2f}% "
                  f"· TP {d.take_profit*100:.1f}% / SL {d.stop_loss*100:.1f}%",
                  symbol=d.symbol, usd=round(size, 2), p_win=round(d.p_win, 3))

    def _manage(self, pos: LivePosition) -> None:
        tok = self.market.tokens.get(pos.address)
        if tok is None:
            self._close(pos, pos.last_price, "token_mati")
            return
        gain = pos.gain
        r = self.rules

        # eksit bertingkat: separuh di 60% target
        if not pos.tp1_done and gain >= pos.tp * 0.6:
            self._sell(pos, pos.qty * r.tp1_fraction, tok.price, "tp1_partial")
            pos.tp1_done = True
            if pos.qty <= pos.initial_qty * 0.01:
                return

        if gain >= pos.tp:
            self._close(pos, tok.price, "take_profit")
            return

        if gain <= -pos.sl:
            self._close(pos, tok.price, "stop_loss")
            return

        # trailing setelah tp1: kunci sebagian keuntungan
        if pos.tp1_done:
            drawdown = (tok.price - pos.peak_price) / pos.peak_price
            if drawdown <= -0.05:
                self._close(pos, tok.price, "trailing")
                return

        if self.tick_no - pos.entry_tick >= r.max_hold_ticks:
            self._close(pos, tok.price, "time_stop")

    def _sell(self, pos: LivePosition, qty: float, price: float, reason: str) -> None:
        qty = min(qty, pos.qty)
        if qty <= 0:
            return
        fraction = qty / pos.qty
        exit_price = price * (1 - self.rules.cost_round_trip / 2)
        fee = qty * exit_price * 0.01
        proceeds = qty * exit_price - fee
        self.cash += proceeds
        self.fees_paid += fee
        pos.realized += proceeds
        pos.cost_usd -= pos.cost_usd * fraction
        pos.qty -= qty
        self._log("GUARD", "partial",
                  f"JUAL sebagian {pos.symbol} · {reason} · "
                  f"sisa {pos.qty / pos.initial_qty * 100:.0f}%")

    def _close(self, pos: LivePosition, price: float, reason: str) -> None:
        if pos.qty > 0:
            exit_price = price * (1 - self.rules.cost_round_trip / 2)
            fee = pos.qty * exit_price * 0.01
            proceeds = pos.qty * exit_price - fee
            self.cash += proceeds
            self.fees_paid += fee
            pos.realized += proceeds
            pos.qty = 0.0

        pnl = pos.realized - pos.initial_cost
        pnl_pct = pnl / pos.initial_cost if pos.initial_cost else 0.0
        self.positions.pop(pos.address, None)

        trade = Trade(
            id=len(self.trades) + 1, address=pos.address, symbol=pos.symbol,
            score=pos.p_win, entry_price=pos.entry_price, exit_price=price,
            size_usd=pos.initial_cost, pnl_usd=pnl, pnl_pct=pnl_pct, reason=reason,
            entry_tick=pos.entry_tick, exit_tick=self.tick_no,
            hold_ticks=self.tick_no - pos.entry_tick, fees_usd=0.0,
        )
        self.trades.append(trade)
        self.journal.record_trade(
            session=self.session_id, tick=self.tick_no, token=pos.address,
            symbol=pos.symbol, p_win=pos.p_win, ev_pct=pos.ev_pct, tp=pos.tp,
            sl=pos.sl, size_pct=pos.initial_cost / max(1.0, self.start_balance),
            features=pos.features, entry_price=pos.entry_price, exit_price=price,
            pnl_pct=pnl_pct, pnl_usd=pnl, reason=reason,
            hold_ticks=self.tick_no - pos.entry_tick,
        )
        self._day_pnl += pnl
        self._log("GUARD", "exit",
                  f"JUAL {pos.symbol} {pnl_pct*100:+.2f}% (${pnl:+.2f}) · {reason} · "
                  f"tahan {self.tick_no - pos.entry_tick} tick",
                  symbol=pos.symbol, pnl=round(pnl, 2), reason=reason)

    # ------------------------------------------------------------------ scan
    def _scan(self) -> None:
        if self.tick_no < self._halted_until:
            return
        if len(self.positions) + len(self._queue) >= self.rules.max_concurrent:
            return

        for sig in self.social.top(self.tick_no, self.graph, n=15,
                                       naive=not self.rules.use_coordination_filter):
            if sig.symbol in self._traded or any(
                    p.symbol == sig.symbol for p in self.positions.values()):
                continue
            tok = self._by_symbol.get(sig.symbol)
            if tok is None or tok.dead or tok.state == "dump":
                continue
            if sig.strength < self.rules.min_signal:
                continue
            if len(sig.findings) and self.rules.use_coordination_filter:
                self._bump("koordinasi")
                continue
            if self.rules.use_coordination_filter and sig.coordination > self.rules.max_coordination:
                self._bump("koordinasi")
                self._log("SOCIAL", "reject",
                          f"{sig.symbol} diabaikan · koordinasi {sig.coordination:.2f} "
                          f"({', '.join(sig.findings) or 'bot farm'})")
                continue

            report = self.forensics.analyze(tok) if self.rules.use_forensics else None
            if report is not None and report.rug_risk > 0.42:
                self._bump("rug_risk")
                self._log("FORENSICS", "reject",
                          f"{sig.symbol} rug risk {report.rug_risk:.2f} · "
                          f"{', '.join(report.findings[:2]) or 'konsentrasi holder'}")
                continue

            momentum = self._momentum(tok)
            liquidity = min(1.0, tok.liquidity_usd / 60_000.0)
            safety = 1.0 - (report.rug_risk if report else 0.3)
            upside = self._upside(tok, sig)

            decision = self.alpha.decide(
                token=tok.address, symbol=sig.symbol, social=sig.strength,
                coordination=sig.coordination, safety=safety, momentum=momentum,
                regime=self._regime, liquidity=liquidity, upside_est=upside,
            )
            decision.features = {
                "social": sig.strength, "coordination": sig.coordination,
                "safety": safety, "momentum": momentum, "regime": self._regime,
                "liquidity": liquidity,
            }
            if decision.approved:
                self._p_log.append(decision.p_win)
            self.journal.record_decision(
                session=self.session_id, tick=self.tick_no, token=tok.address,
                symbol=sig.symbol, approved=decision.approved, p_win=decision.p_win,
                coordination=sig.coordination, social=sig.strength, safety=safety,
                reasons=decision.reasons)

            if not decision.approved:
                for reason in decision.reasons:
                    key = reason.split()[0]
                    self._bump(key)
                self._log("ALPHA", "reject",
                          f"{sig.symbol} ditolak · {'; '.join(decision.reasons[:2])}")
                continue

            self._queue.append((self.tick_no + self.rules.entry_delay_ticks, decision))
            self._traded.add(sig.symbol)
            self._signal_probes.append({"token": tok.address, "price": tok.price,
                                        "tick": self.tick_no, "hit": False})
            self._probe_total += 1
            self._log("ALPHA", "approve",
                      f"{sig.symbol} lolos · p̂ {decision.p_win:.2f} · "
                      f"TP {decision.take_profit*100:.1f}% · EV {decision.ev_pct*100:+.2f}%")
            if len(self.positions) + len(self._queue) >= self.rules.max_concurrent:
                return

    def _momentum(self, tok) -> float:
        """Momentum dinilai sebagai BAND, bukan "makin naik makin bagus".

        Skor puncak di +8% per 3 tick. Kalau harga sudah naik >25% dalam 3 tick
        kita bukan lagi pembeli awal — kita adalah exit liquidity orang lain.
        """
        h = self._price_hist.get(tok.address, [])
        if len(h) < 3:
            return 0.35
        chg = h[-1] / h[0] - 1.0
        return max(0.0, math.exp(-((chg - 0.08) / 0.12) ** 2))

    def _upside(self, tok, sig: SocialSignal) -> float:
        """Perkiraan upside dari data yang TERAMATI (bukan variabel laten)."""
        liq = min(1.0, tok.liquidity_usd / 80_000.0)
        holders = min(1.0, tok.holders / 800.0)
        return max(0.02, min(0.9, 0.10 + 0.34 * sig.strength + 0.18 * liq
                            + 0.12 * holders + 0.16 * min(1.0, sig.reach)))

    # ------------------------------------------------------------- reputasi
    def _resolve_calls(self) -> None:
        for token, authors in list(self._pending_calls.items()):
            tok = self.market.tokens.get(token)
            if tok is None:
                for a in authors:
                    self.graph.mark(a, False)
                self._pending_calls.pop(token, None)
                continue
            if (tok.price / tok.p0) >= 1.25:
                for a in authors:
                    self.graph.mark(a, True)
                self._pending_calls.pop(token, None)

    def _update_probes(self) -> None:
        keep = []
        for p in self._signal_probes:
            tok = self.market.tokens.get(p["token"])
            if tok is None:
                continue
            if tok.price >= p["price"] * 1.12:
                if not p["hit"]:
                    p["hit"] = True
                    self._probe_hit += 1
                continue
            if self.tick_no - p["tick"] > self.rules.max_hold_ticks:
                continue
            keep.append(p)
        self._signal_probes = keep

    # -------------------------------------------------------------- harian
    def _update_day(self) -> None:
        if self.tick_no - self._day_start_tick >= self.rules.day_length_ticks:
            equity = self.equity()
            change = (equity / self._day_start_equity - 1) if self._day_start_equity else 0
            self._log("RISK", "day",
                      f"hari selesai · {change*100:+.2f}% · target "
                      f"{self.rules.daily_target_pct*100:.1f}%")
            self._day_start_equity = equity
            self._day_start_tick = self.tick_no
            self._day_pnl = 0.0
            self._halted_until = 0

        equity = self.equity()
        if self._day_start_equity and equity < self._day_start_equity * (1 - self.rules.daily_loss_limit_pct):
            if self._halted_until <= self.tick_no:
                self._halted_until = self._day_start_tick + self.rules.day_length_ticks
                self._log("RISK", "halt",
                          f"batas rugi harian kena ({(equity/self._day_start_equity-1)*100:.2f}%) "
                          f"· berhenti sampai hari berganti")

        if (self.rules.withdraw_at_multiple and self.vault_locked == 0
                and equity >= self.principal * self.rules.withdraw_at_multiple):
            withdrawn = min(self.cash, self.principal)
            if withdrawn > 0:
                self.cash -= withdrawn
                self.vault_locked += withdrawn
                self._log("VAULT", "withdraw",
                          f"modal ${withdrawn:,.2f} ditarik ke vault · trading sekarang "
                          f"100% uang profit (free trading)")

    def _sample(self) -> None:
        eq = self.equity()
        if self.tick_no % 3 == 0:
            self.equity_curve.append((self.tick_no, round(eq, 2)))
        self.peak_equity = max(self.peak_equity, eq)
        if self.peak_equity:
            self.max_drawdown = max(self.max_drawdown, (self.peak_equity - eq) / self.peak_equity)

    def _finish(self) -> None:
        for pos in list(self.positions.values()):
            self._close(pos, pos.last_price, "session_end")
        self.finished = True
        self._log("SCRIBE", "info", "Sesi selesai")
        self.scribe.close()
        self.journal.close()

    # ------------------------------------------------------------------ KPI
    def kpis(self) -> dict:
        eq = self.equity()
        wins = [t for t in self.trades if t.pnl_usd > 0]
        losses = [t for t in self.trades if t.pnl_usd <= 0]
        avg_win = sum(t.pnl_pct for t in wins) / len(wins) if wins else 0.0
        avg_loss = abs(sum(t.pnl_pct for t in losses) / len(losses)) if losses else 0.0
        emp_be = avg_loss / (avg_win + avg_loss) if (avg_win + avg_loss) else 1.0
        exp = sum(t.pnl_pct for t in self.trades) / len(self.trades) if self.trades else 0.0
        lat = self.forensics.latency_stats()
        return {
            "session_id": self.session_id,
            "tick": self.tick_no,
            "ticks_total": self.sim.ticks,
            "sim_minutes": round(self.tick_no * self.sim.sim_seconds_per_tick / 60, 1),
            "equity": round(eq, 2),
            "total_equity": round(self.total_equity(), 2),
            "vault_locked": round(self.vault_locked, 2),
            "free_trading": self.vault_locked > 0,
            "cash": round(self.cash, 2),
            "start_balance": round(self.start_balance, 2),
            "pnl_usd": round(eq + self.vault_locked - self.start_balance, 2),
            "pnl_pct": round((eq + self.vault_locked) / self.start_balance * 100 - 100, 2),
            "trades": len(self.trades),
            "wins": len(wins),
            "losses": len(losses),
            "win_rate": round(len(wins) / len(self.trades) * 100, 1) if self.trades else 0.0,
            "avg_win_pct": round(avg_win * 100, 2),
            "avg_loss_pct": round(-avg_loss * 100, 2),
            "empirical_breakeven": round(emp_be * 100, 1),
            "expectancy_pct": round(exp * 100, 3),
            "avg_p_win": round(sum(self._p_log) / len(self._p_log), 3) if self._p_log else 0.0,
            "signal_hit_rate": round(self._probe_hit / self._probe_total * 100, 1)
            if self._probe_total else 0.0,
            "signals": self._probe_total,
            "rejected": dict(self._rejected),
            "fees_paid": round(self.fees_paid, 2),
            "max_drawdown_pct": round(self.max_drawdown * 100, 2),
            "open_positions": len(self.positions),
            "queued": len(self._queue),
            "regime": round(self._regime, 2),
            "halted": self.tick_no < self._halted_until,
            "latency_p50_ms": lat["p50"],
            "latency_p95_ms": lat["p95"],
            "accounts": self.graph.stats(),
            "mode": self.sim.mode,
            "cost_pct": round(self.rules.cost_round_trip * 100, 2),
            "finished": self.finished,
        }

    def snapshot(self) -> dict:
        ec = self._exit_cost()
        signals = self.social.top(self.tick_no, self.graph, n=7,
                                  naive=not self.rules.use_coordination_filter)
        return {
            "kpis": self.kpis(),
            "signals": [s.public() for s in signals],
            "positions": [{
                "symbol": p.symbol, "size_usd": round(p.cost_usd, 2),
                "entry": p.entry_price, "price": p.last_price,
                "unrealized": round((p.market_value(ec) / max(1e-9, p.cost_usd) - 1) * 100, 2),
                "progress": round(max(0.0, min(1.0, p.gain / p.tp)), 3),
                "p_win": round(p.p_win, 2), "tp": round(p.tp * 100, 1),
                "age": self.tick_no - p.entry_tick, "tp1": p.tp1_done,
            } for p in self.positions.values()],
            "trades": [t.public() for t in self.trades[-20:]][::-1],
            "leaderboard": self.graph.leaderboard(8),
            "news": [n.public() for n in self.market.news[-6:]],
            "equity_curve": self.equity_curve[-400:],
            "config": {
                "min_p_win": self.rules.min_p_win,
                "cost_pct": round(self.rules.cost_round_trip * 100, 2),
                "sl_pct": round(self.rules.stop_loss * 100, 1),
                "max_tp_pct": round(self.rules.max_tp * 100, 1),
                "max_position_pct": self.rules.max_position_pct * 100,
                "daily_loss_limit_pct": self.rules.daily_loss_limit_pct * 100,
                "sim_seconds_per_tick": self.sim.sim_seconds_per_tick,
                "mode": self.sim.mode,
            },
        }


# ---------------------------------------------------------------- laporan
DISCLAIMER = (
    "PAPER TRADING / SIMULASI. Tidak ada wallet, private key, atau order on-chain. "
    "Postingan sosial, KOL, bot farm, dan berita di sini dihasilkan generator, bukan "
    "diambil dari X/Telegram. Angka di laporan ini mengukur mesinnya, bukan pasar nyata."
)


def build_social_report(desk: SocialDesk) -> dict:
    k = desk.kpis()
    return {
        "session_id": desk.session_id,
        "kpis": k,
        "config": {
            "min_p_win": desk.rules.min_p_win,
            "cost_round_trip_pct": desk.rules.cost_round_trip * 100,
            "stop_loss_pct": desk.rules.stop_loss * 100,
            "tp_range_pct": [desk.rules.min_tp * 100, desk.rules.max_tp * 100],
            "max_position_pct": desk.rules.max_position_pct * 100,
            "max_pct_of_liquidity": desk.rules.max_pct_of_liquidity * 100,
            "daily_loss_limit_pct": desk.rules.daily_loss_limit_pct * 100,
            "max_concurrent": desk.rules.max_concurrent,
            "entry_delay_ticks": desk.rules.entry_delay_ticks,
            "coordination_filter": desk.rules.use_coordination_filter,
            "mode": desk.sim.mode,
            "seed": desk.sim.seed,
            "sim_seconds_per_tick": desk.sim.sim_seconds_per_tick,
        },
        "trades": [t.public() for t in desk.trades],
        "leaderboard": desk.graph.leaderboard(20),
        "account_stats": desk.graph.stats(),
        "news": [n.public() for n in desk.market.news],
        "rejected": dict(desk._rejected),
        "disclaimer": DISCLAIMER,
    }


def render_social_markdown(d: dict) -> str:
    k, c = d["kpis"], d["config"]
    rows = "\n".join(
        f"| {t['symbol']} | {t['score']:.2f} | ${t['size_usd']:.2f} | {t['pnl_pct']:+.1f}% "
        f"| ${t['pnl_usd']:+.2f} | {t['hold_ticks'] * c['sim_seconds_per_tick']:.0f}s | {t['reason']} |"
        for t in d["trades"]
    ) or "| — | — | — | — | — | — | — |"

    leaders = "\n".join(
        f"| {a['handle']} | {a['kind']} | {a['followers']:,} | {a['hits']} | {a['misses']} "
        f"| {a['reputation']:.2f} |"
        for a in d["leaderboard"]
    ) or "| — | — | — | — | — | — |"

    news = "\n".join(f"| {n['tick']} | {n['kind']} | {n['headline']} |"
                     for n in d["news"][-10:]) or "| — | — | — |"

    rej = ", ".join(f"{k2} ×{v}" for k2, v in sorted(d["rejected"].items())) or "—"
    calib = (k["win_rate"] - k["avg_p_win"] * 100) if k["trades"] else 0.0
    edge = "**ya**" if k["win_rate"] > k["empirical_breakeven"] else "**tidak**"

    return f"""# Social Radar — Laporan Sesi `{d['session_id']}`

> ⚠️ **Simulasi.** {d['disclaimer']}

## Ringkasan

| Metrik | Nilai |
|---|---|
| Mode pasar | `{c['mode']}` (bot farm {'aktif' if c['mode'] == 'dirty' else 'mati'}) |
| Saldo awal | ${k['start_balance']:,.2f} |
| Ekuitas akhir | ${k['equity']:,.2f} |
| Modal di vault | ${k['vault_locked']:,.2f} |
| Free trading aktif | {'ya — trading memakai uang profit' if k['free_trading'] else 'belum (butuh ekuitas 2× modal)'} |
| PnL | ${k['pnl_usd']:+,.2f} ({k['pnl_pct']:+.2f}%) |
| Trade | {k['trades']} (W {k['wins']} / L {k['losses']}) |
| **Win rate** | **{k['win_rate']:.1f}%** |
| Ambang impas empiris | {k['empirical_breakeven']:.1f}% |
| Menguntungkan? | {edge} |
| Rata-rata menang / kalah | {k['avg_win_pct']:+.2f}% / {k['avg_loss_pct']:+.2f}% |
| Expectancy per trade | {k['expectancy_pct']:+.3f}% |
| Rata-rata p̂ saat entry | {k['avg_p_win']:.3f} |
| Kalibrasi (win rate − p̂) | {calib:+.1f} poin |
| Max drawdown | {k['max_drawdown_pct']:.2f}% |
| Fee dibayar | ${k['fees_paid']:,.2f} |
| Sinyal disaring | {rej} |
| Latency skor p50/p95 | {k['latency_p50_ms']:.3f} / {k['latency_p95_ms']:.3f} ms |
| Waktu pasar disimulasikan | {k['sim_minutes']:.0f} menit ({k['tick']} tick × {c['sim_seconds_per_tick']}s) |

## Aturan yang dipakai

- p̂ minimum **{c['min_p_win']:.2f}**, biaya pulang-pergi **{c['cost_round_trip_pct']:.1f}%**
- Target diturunkan dari biaya: `t > ((1−p)s + c)/p`, dibatasi {c['tp_range_pct'][0]:.0f}–{c['tp_range_pct'][1]:.0f}%
- Stop keras **−{c['stop_loss_pct']:.0f}%**, exit bertingkat (50% di 60% target, sisanya trailing 5%)
- Posisi maksimum **{c['max_position_pct']:.0f}% ekuitas** dan **{c['max_pct_of_liquidity']:.1f}% likuiditas pool**
- Batas rugi harian **{c['daily_loss_limit_pct']:.1f}%** → mesin berhenti sampai hari berganti

## Trade

| Token | p̂ | Ukuran | PnL | $ | Tahan | Alasan keluar |
|---|---|---|---|---|---|---|
{rows}

## Reputasi akun (dihitung dari hasil, bukan daftar statis)

| Akun | Jenis | Followers | Hit | Miss | Reputasi |
|---|---|---|---|---|---|
{leaders}

## Berita yang masuk

| Tick | Jenis | Judul |
|---|---|---|
{news}
"""


def write_social_report(desk: SocialDesk):
    import json
    rep = build_social_report(desk)
    desk.run_dir.mkdir(parents=True, exist_ok=True)
    jpath = desk.run_dir / "social-report.json"
    mpath = desk.run_dir / "social-report.md"
    jpath.write_text(json.dumps(rep, indent=2, ensure_ascii=False), encoding="utf-8")
    mpath.write_text(render_social_markdown(rep), encoding="utf-8")
    return jpath, mpath


def run_social_bench(ticks: int = 1200, seeds: int = 10) -> dict:
    """Tiga lengan: pasar kotor (filter ON), pasar kotor (filter OFF), pasar bersih."""
    import statistics as st

    arms = [
        ("dirty+filter", "dirty", True),
        ("dirty-filter", "dirty", False),
        ("clean+filter", "clean", True),
    ]
    out = []
    for name, mode, filt in arms:
        pnls, wrs, trs, exps, ps = [], [], [], [], []
        for seed in range(1, seeds + 1):
            rules = SocialRules(use_coordination_filter=filt)
            desk = SocialDesk(SocialSimConfig(ticks=ticks, seed=seed, mode=mode), rules)
            while not desk.finished:
                desk.tick()
            k = desk.kpis()
            pnls.append(k["pnl_pct"])
            wrs.append(k["win_rate"])
            trs.append(k["trades"])
            exps.append(k["expectancy_pct"])
            ps.append(k["avg_p_win"])
        srt = sorted(pnls)
        q1 = srt[len(srt) // 4]
        q3 = srt[(3 * len(srt)) // 4]
        out.append({
            "arm": name, "mode": mode, "coordination_filter": filt,
            "median_pnl_pct": round(st.median(pnls), 2),
            "q1_pnl_pct": round(q1, 2), "q3_pnl_pct": round(q3, 2),
            "min_pnl_pct": round(srt[0], 2), "max_pnl_pct": round(srt[-1], 2),
            "profitable_sessions": sum(1 for p in pnls if p > 0),
            "sessions": seeds,
            "avg_win_rate": round(st.mean(wrs), 1),
            "avg_trades": round(st.mean(trs), 1),
            "avg_expectancy_pct": round(st.mean(exps), 3),
            "avg_p_win": round(st.mean(ps), 3),
            "all_pnl_pct": [round(p, 2) for p in pnls],
        })
    return {"ticks": ticks, "seeds": seeds, "start_balance": 250.0, "results": out,
            "disclaimer": DISCLAIMER}
