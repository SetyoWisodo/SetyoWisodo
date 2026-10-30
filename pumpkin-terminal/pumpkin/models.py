"""Model data yang dipakai bersama oleh semua agen."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Literal

Archetype = Literal["rug", "dead", "pump", "solid"]


@dataclass
class Token:
    """Snapshot sebuah pair/token. Feed simulasi mengisi semuanya;

    feed live (Dexscreener) hanya mengisi field pasar yang tersedia.
    """

    address: str
    symbol: str
    name: str
    price: float
    liquidity_usd: float
    holders: int
    top10_pct: float
    dev_pct: float
    mint_revoked: bool
    lp_locked: bool
    volume_usd: float = 0.0
    buys: int = 0
    sells: int = 0
    age_ticks: int = 0
    created_tick: int = 0
    change_5_pct: float = 0.0
    dead: bool = False
    rugged: bool = False

    # hanya dipakai generator simulasi (tidak pernah terlihat oleh agen)
    archetype: Archetype = "dead"
    p0: float = 1.0
    liq0: float = 1.0
    hold0: int = 0
    lifetime_ticks: int = 0
    rug_tick: int = 0
    spike_tick: int = 0
    spike_size: float = 0.0
    logprice: float = 0.0
    _recent: list[float] = field(default_factory=list, repr=False)

    def public(self) -> dict:
        """Yang boleh dipakai ANALYST (field laten sengaja tidak ikut)."""
        return {
            "address": self.address,
            "symbol": self.symbol,
            "name": self.name,
            "price": self.price,
            "liquidity_usd": round(self.liquidity_usd, 2),
            "holders": self.holders,
            "top10_pct": round(self.top10_pct, 2),
            "dev_pct": round(self.dev_pct, 2),
            "mint_revoked": self.mint_revoked,
            "lp_locked": self.lp_locked,
            "volume_usd": round(self.volume_usd, 2),
            "age_ticks": self.age_ticks,
            "change_5_pct": round(self.change_5_pct, 2),
        }


@dataclass
class Position:
    id: int
    address: str
    symbol: str
    qty: float
    entry_price: float         # sudah termasuk slippage masuk
    entry_tick: int
    cost_usd: float            # kas yang benar-benar keluar (posisi + fee)
    score: float
    peak_price: float = 0.0
    peak_gain_pct: float = 0.0
    last_price: float = 0.0
    status: str = "open"

    def market_value(self, price: float, exit_cost_pct: float) -> float:
        return self.qty * price * (1.0 - exit_cost_pct)


@dataclass
class Trade:
    id: int
    address: str
    symbol: str
    score: float
    entry_price: float
    exit_price: float
    size_usd: float
    pnl_usd: float
    pnl_pct: float
    reason: str
    entry_tick: int
    exit_tick: int
    hold_ticks: int
    fees_usd: float

    def public(self) -> dict:
        return {
            "id": self.id,
            "symbol": self.symbol,
            "score": round(self.score, 3),
            "entry_price": self.entry_price,
            "exit_price": self.exit_price,
            "size_usd": round(self.size_usd, 2),
            "pnl_usd": round(self.pnl_usd, 2),
            "pnl_pct": round(self.pnl_pct * 100, 2),
            "reason": self.reason,
            "hold_ticks": self.hold_ticks,
            "fees_usd": round(self.fees_usd, 3),
        }


@dataclass
class Event:
    """Satu baris log SCRIBE."""

    tick: int
    agent: str
    kind: str            # scan | reject | score | enter | exit | info
    message: str
    data: dict = field(default_factory=dict)
    ts: float = field(default_factory=time.time)

    def public(self) -> dict:
        return {
            "tick": self.tick,
            "agent": self.agent,
            "kind": self.kind,
            "message": self.message,
            "data": self.data,
        }
