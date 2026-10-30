"""Desk: orkestrator yang menjalankan keenam agen dalam satu loop tick."""

from __future__ import annotations

import time
import uuid
from pathlib import Path

from .agents import Analyst, Filter, Guard, Scout, Scribe, Sniper
from .config import Config, RUNS_DIR
from .feed import SimMarket, make_feed
from .models import Event, Position, Token, Trade


class Desk:
    def __init__(self, cfg: Config | None = None, run_dir: Path | None = None):
        self.cfg = cfg or Config()
        self.session_id = time.strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:4]
        self.run_dir = run_dir or (RUNS_DIR / self.session_id)

        self.feed = make_feed(self.cfg)
        self.scout = Scout()
        self.filter = Filter(self.cfg.filters)
        self.analyst = Analyst(self.cfg.risk.min_score, self.cfg.sim.edge_mode)
        self.sniper = Sniper(self.cfg.risk)
        self.guard = Guard(self.cfg.risk)
        self.scribe = Scribe(self.run_dir)

        self.tick_no = 0
        self.cash = self.cfg.sim.start_balance
        self.start_balance = self.cfg.sim.start_balance
        self.positions: dict[str, Position] = {}
        self.trades: list[Trade] = []
        self.equity_curve: list[tuple[int, float]] = []
        self.peak_equity = self.start_balance
        self.max_drawdown = 0.0
        self.fees_paid = 0.0
        self._retry: list[tuple[Token, int, int]] = []   # token, tick_retry, attempts
        self._candidates: list[tuple[float, Token, int]] = []  # score, token, expiry
        self._traded: set[str] = set()
        self._watch: dict[str, tuple[Token, int]] = {}
        self._rejected: set[str] = set()
        self._last_entry_tick = -99
        self._trade_id = 0
        self.finished = False
        self.started_at = time.time()

    # ------------------------------------------------------------------ utils
    def _log(self, agent: str, kind: str, message: str, **data) -> None:
        self.scribe.write(Event(tick=self.tick_no, agent=agent, kind=kind,
                                message=message, data=data))

    def _exit_cost_pct(self) -> float:
        r = self.cfg.risk
        return 1.0 - (1.0 - r.exit_slippage_pct) * (1.0 - r.exit_fee_pct)

    def equity(self) -> float:
        ec = self._exit_cost_pct()
        mtm = sum(p.qty * p.last_price * (1 - ec) for p in self.positions.values()
                  if p.last_price > 0)
        return self.cash + mtm

    # ------------------------------------------------------------------- tick
    def tick(self) -> None:
        if self.finished:
            return
        self.tick_no += 1
        cfg = self.cfg

        fresh = self.feed.step(self.tick_no)

        # 1. GUARD lebih dulu — risiko sebelum peluang.
        for addr, pos in list(self.positions.items()):
            tok = self._lookup(addr)
            if tok is None:
                continue
            self.guard.update(pos, tok)
            reason = self.guard.decide(pos, tok, self.tick_no)
            if reason:
                self._close(pos, tok, reason)

        # 2. SCOUT + FILTER untuk token baru
        for tok in fresh:
            if self.scout.ingest(tok):
                self._log("SCOUT", "scan", f"{tok.symbol} · liq ${tok.liquidity_usd:,.0f} "
                          f"· {tok.holders} holder", symbol=tok.symbol,
                          liquidity=round(tok.liquidity_usd, 0))
                self._screen(tok, attempt=0)

        # 2b. Watchlist: pair yang sudah lolos FILTER dipantau terus sampai
        #     momentumnya muncul atau jendela pengamatan habis.
        for addr, (tok, until) in list(self._watch.items()):
            if tok.dead or self.tick_no > until:
                self._watch.pop(addr, None)
                if not tok.dead:
                    sc = self.analyst.probe(tok)
                    self.analyst.bump("tolak_skor")
                    self._log("ANALYST", "reject",
                              f"{tok.symbol} tidak pernah capai {self.cfg.risk.min_score:.2f} "
                              f"(terbaik {sc:.2f}) · jendela habis",
                              symbol=tok.symbol, score=round(sc, 3))
                continue
            passed, score = self.analyst.evaluate(tok, count=False)
            if passed:
                self._watch.pop(addr, None)
                self._log("ANALYST", "score", f"{tok.symbol} skor {score:.3f} (momentum)",
                          symbol=tok.symbol, score=round(score, 3), passed=True)
                self._candidates.append((score, tok, self.tick_no + 6))

        # 3. Retry untuk token yang tertolak hanya karena masih terlalu baru
        still: list[tuple[Token, int, int]] = []
        for tok, at, attempts in self._retry:
            if self.tick_no >= at:
                if tok.dead:
                    continue
                self._screen(tok, attempt=attempts)
            else:
                still.append((tok, at, attempts))
        self._retry = still

        # 4. SNIPER
        self._candidates = [c for c in self._candidates if c[2] > self.tick_no]
        self._sniping()

        # 5. Penutupan sesi
        self._sample_equity()
        if self.tick_no >= cfg.sim.ticks:
            self._finish()

    def _lookup(self, addr: str) -> Token | None:
        live = getattr(self.feed, "live", {})
        return live.get(addr)

    def _screen(self, tok: Token, attempt: int) -> None:
        if self.cfg.sim.edge_mode == "null":
            # KONTROL: tidak ada keahlian sama sekali. Filter dimatikan dan skor
            # acak, jadi yang diukur murni ongkos pasar (fee, slippage, rug).
            self._watch[tok.address] = (tok, self.tick_no + 45)
            return
        ok, reason = self.filter.check(tok)
        if not ok:
            if reason == "terlalu_baru" and attempt < 2:
                self._retry.append((tok, self.tick_no + 2, attempt + 1))
                return
            self._rejected.add(tok.address)
            self._log("FILTER", "reject", f"{tok.symbol} ditolak: {reason}",
                      symbol=tok.symbol, reason=reason)
            return
        self._log("FILTER", "pass", f"{tok.symbol} lolos filter", symbol=tok.symbol)
        self._watch[tok.address] = (tok, self.tick_no + 45)   # pantau sampai 45 tick

    def _sniping(self) -> None:
        self._candidates.sort(key=lambda c: -c[0])
        cfg = self.cfg
        if self.tick_no - self._last_entry_tick < cfg.risk.min_ticks_between_entries:
            return
        while self._candidates and len(self.positions) < cfg.risk.max_concurrent:
            score, tok, _ = self._candidates[0]
            if tok.dead or tok.address in self.positions or tok.address in self._traded:
                self._candidates.pop(0)
                continue
            usd, why = self.sniper.size(self.cash, tok)
            if usd <= 0:
                self._log("SNIPER", "info", f"{tok.symbol} dilewati: {why}", symbol=tok.symbol)
                self._candidates.pop(0)
                continue
            self._candidates.pop(0)
            self._traded.add(tok.address)
            self._last_entry_tick = self.tick_no
            self._open(tok, usd, score)
            return   # maksimal satu entry per tick

    def _entry_slippage(self, tok: Token) -> float:
        """Token yang sedang lari punya slippage lebih besar — seperti di DEX nyata."""
        extra = min(0.030, abs(tok.change_5_pct) / 100.0 * 0.18)
        return self.cfg.risk.entry_slippage_pct + extra

    def _open(self, tok: Token, usd: float, score: float) -> None:
        r = self.cfg.risk
        slip = self._entry_slippage(tok)
        entry_price = tok.price * (1 + slip)
        qty = usd * (1 - r.entry_fee_pct) / entry_price
        self.cash -= usd
        self.fees_paid += usd * r.entry_fee_pct
        pos = Position(
            id=len(self.positions) + 1, address=tok.address, symbol=tok.symbol,
            qty=qty, entry_price=entry_price, entry_tick=self.tick_no,
            cost_usd=usd, score=score, peak_price=entry_price, last_price=tok.price,
        )
        self.positions[tok.address] = pos
        self.sniper.confirm(tok, usd)
        self._log("SNIPER", "enter", f"BELI {tok.symbol} ${usd:,.2f} @ {_px(tok.price)}",
                  symbol=tok.symbol, usd=round(usd, 2), score=round(score, 3),
                  price=tok.price, slippage_pct=round(slip * 100, 2))

    def _close(self, pos: Position, tok: Token, reason: str) -> None:
        r = self.cfg.risk
        exit_price = tok.price * (1 - r.exit_slippage_pct)
        proceeds = pos.qty * exit_price * (1 - r.exit_fee_pct)
        fee = pos.qty * exit_price * r.exit_fee_pct
        pnl = proceeds - pos.cost_usd
        self.cash += proceeds
        self.fees_paid += fee
        self.positions.pop(pos.address, None)

        self._trade_id += 1
        trade = Trade(
            id=self._trade_id, address=pos.address, symbol=pos.symbol, score=pos.score,
            entry_price=pos.entry_price, exit_price=exit_price, size_usd=pos.cost_usd,
            pnl_usd=pnl, pnl_pct=pnl / pos.cost_usd, reason=reason,
            entry_tick=pos.entry_tick, exit_tick=self.tick_no,
            hold_ticks=self.tick_no - pos.entry_tick, fees_usd=fee,
        )
        self.trades.append(trade)
        self._log("GUARD", "exit",
                  f"JUAL {pos.symbol} {trade.pnl_pct*100:+.2f}% (${pnl:+.2f}) · {reason}",
                  symbol=pos.symbol, pnl=round(pnl, 2), pnl_pct=round(trade.pnl_pct * 100, 2),
                  reason=reason)

    def _sample_equity(self) -> None:
        eq = self.equity()
        if self.tick_no % 5 == 0 or self.tick_no == 1:
            self.equity_curve.append((self.tick_no, round(eq, 2)))
        if eq > self.peak_equity:
            self.peak_equity = eq
        dd = (self.peak_equity - eq) / self.peak_equity if self.peak_equity else 0.0
        self.max_drawdown = max(self.max_drawdown, dd)

    def _finish(self) -> None:
        for addr, pos in list(self.positions.items()):
            tok = self._lookup(addr)
            if tok is not None:
                self._close(pos, tok, "session_end")
        self.finished = True
        self._log("SCRIBE", "info", "Sesi selesai · semua posisi ditutup paksa")
        self.scribe.close()
        close = getattr(self.feed, "close", None)
        if close:
            close()

    # --------------------------------------------------------------- snapshot
    def kpis(self) -> dict:
        eq = self.equity()
        wins = [t for t in self.trades if t.pnl_usd > 0]
        losses = [t for t in self.trades if t.pnl_usd <= 0]
        gross_win = sum(t.pnl_usd for t in wins)
        gross_loss = -sum(t.pnl_usd for t in losses)
        scanned = getattr(self.feed, "scanned", self.scout.counts.get("scanned", 0))
        rejected = self.filter.counts.get("ditolak", 0) + self.analyst.counts.get("tolak_skor", 0)
        return {
            "session_id": self.session_id,
            "tick": self.tick_no,
            "ticks_total": self.cfg.sim.ticks,
            "sim_minutes": round(self.tick_no * self.cfg.sim.sim_seconds_per_tick / 60.0, 1),
            "equity": round(eq, 2),
            "cash": round(self.cash, 2),
            "start_balance": round(self.start_balance, 2),
            "pnl_usd": round(eq - self.start_balance, 2),
            "pnl_pct": round((eq / self.start_balance - 1) * 100, 2),
            "scanned": scanned,
            "rejected": len(self._rejected),
            "rejection_rate": round(len(self._rejected) / scanned * 100, 2) if scanned else 0.0,
            "trades": len(self.trades),
            "wins": len(wins),
            "losses": len(losses),
            "win_rate": round(len(wins) / len(self.trades) * 100, 1) if self.trades else 0.0,
            "gross_win": round(gross_win, 2),
            "gross_loss": round(gross_loss, 2),
            "expectancy": round((gross_win - gross_loss) / len(self.trades), 3) if self.trades else 0.0,
            "fees_paid": round(self.fees_paid, 2),
            "max_drawdown_pct": round(self.max_drawdown * 100, 2),
            "open_positions": len(self.positions),
            "finished": self.finished,
            "edge_mode": self.cfg.sim.edge_mode,
            "feed": self.cfg.sim.feed,
        }

    def snapshot(self) -> dict:
        ec = self._exit_cost_pct()
        return {
            "kpis": self.kpis(),
            "agents": [
                self.scout.stats(), self.filter.stats(), self.analyst.stats(),
                self.sniper.stats(), self.guard.stats(), self.scribe.stats(),
            ],
            "positions": [
                {
                    "symbol": p.symbol,
                    "address": p.address,
                    "size_usd": round(p.cost_usd, 2),
                    "entry_price": p.entry_price,
                    "price": p.last_price,
                    "unrealized_pct": round((p.qty * p.last_price * (1 - ec) / p.cost_usd - 1) * 100, 2),
                    "peak_pct": round(p.peak_gain_pct * 100, 2),
                    "age": self.tick_no - p.entry_tick,
                    "score": round(p.score, 3),
                }
                for p in sorted(self.positions.values(), key=lambda x: -x.cost_usd)
            ],
            "trades": [t.public() for t in self.trades[-25:]][::-1],
            "equity_curve": self.equity_curve[-400:],
            "config": self.cfg.to_dict(),
        }


def _px(p: float) -> str:
    if p >= 1:
        return f"${p:,.3f}"
    if p >= 0.001:
        return f"${p:.6f}"
    return f"${p:.9f}"
