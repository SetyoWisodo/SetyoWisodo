"""Radar whale: reputasi dompet + agregasi aliran dana menjadi satu sinyal.

Dua bagian:

``WhaleRegistry``
    Mencatat setiap whale yang terlihat masuk ke sebuah token, lalu menandai
    panggilan itu **berhasil** (token mencapai target +50%) atau **gagal**
    (token mati / kena stop). Reputasi memakai Laplace smoothing supaya whale
    baru tidak langsung dianggap dewa atau sampah.

``FlowAggregator``
    Menyimpan transaksi whale dalam jendela waktu pendek, lalu mengubahnya jadi
    satu angka 0..1 per token: berapa whale berbeda, berapa dolar bersih, dan
    seberapa bagus rekam jejak mereka. Inilah "big data" yang dipakai SNIPER.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from .whale_market import WhaleTx


@dataclass
class WhaleProfile:
    address: str
    label: str = "unknown"
    hits: int = 0
    misses: int = 0
    usd_seen: float = 0.0
    tokens_seen: int = 0
    last_tick: int = 0

    @property
    def reputation(self) -> float:
        return (self.hits + 1.0) / (self.hits + self.misses + 2.0)

    @property
    def samples(self) -> int:
        return self.hits + self.misses

    def public(self) -> dict:
        return {
            "address": self.address,
            "label": self.label,
            "hits": self.hits,
            "misses": self.misses,
            "reputation": round(self.reputation, 3),
            "usd_seen": round(self.usd_seen, 0),
            "tokens_seen": self.tokens_seen,
        }


class WhaleRegistry:
    def __init__(self) -> None:
        self.profiles: dict[str, WhaleProfile] = {}

    def touch(self, tx: WhaleTx) -> WhaleProfile:
        p = self.profiles.get(tx.whale)
        if p is None:
            p = WhaleProfile(address=tx.whale, label=tx.label)
            self.profiles[tx.whale] = p
        p.label = tx.label or p.label
        p.usd_seen += tx.usd
        p.tokens_seen += 1
        p.last_tick = tx.tick
        return p

    def mark(self, address: str, hit: bool) -> None:
        p = self.profiles.get(address)
        if p is None:
            return
        if hit:
            p.hits += 1
        else:
            p.misses += 1

    def reputation(self, address: str) -> float:
        p = self.profiles.get(address)
        return p.reputation if p else 0.5

    def leaderboard(self, n: int = 8, min_samples: int = 1) -> list[dict]:
        rows = [p for p in self.profiles.values() if p.samples >= min_samples]
        rows.sort(key=lambda p: (-p.reputation, -p.samples))
        return [p.public() for p in rows[:n]]

    def stats(self) -> dict:
        n = len(self.profiles)
        known = [p for p in self.profiles.values() if p.samples > 0]
        good = [p for p in known if p.reputation >= 0.55]
        return {
            "tracked": n,
            "resolved": len(known),
            "reliable": len(good),
            "avg_reputation": round(
                sum(p.reputation for p in known) / len(known), 3) if known else 0.5,
        }


@dataclass
class FlowSignal:
    token: str
    symbol: str
    whales: list[str] = field(default_factory=list)
    net_usd: float = 0.0
    avg_reputation: float = 0.5
    first_tick: int = 0
    signal: float = 0.0
    price: float = 0.0   # harga saat sinyal terlihat

    def public(self) -> dict:
        return {
            "symbol": self.symbol,
            "token": self.token,
            "whales": len(self.whales),
            "net_usd": round(self.net_usd, 0),
            "avg_reputation": round(self.avg_reputation, 3),
            "signal": round(self.signal, 3),
            "age": self.first_tick,
        }


class FlowAggregator:
    """Menggabungkan transaksi whale jadi sinyal per token dalam jendela pendek."""

    W_COUNT = 0.45
    W_SIZE = 0.30
    W_REP = 0.25

    def __init__(self, window_ticks: int = 8, max_tokens: int = 400):
        self.window = window_ticks
        self.max_tokens = max_tokens
        self.flows: dict[str, list[tuple[int, str, float, str]]] = {}
        self.sells: dict[str, int] = {}
        self.tx_count = 0
        self.buy_usd = 0.0

    # ------------------------------------------------------------------ input
    def ingest(self, tx: WhaleTx) -> None:
        self.tx_count += 1
        if tx.side == "sell":
            self.sells[tx.token] = self.sells.get(tx.token, 0) + int(tx.usd)
            return
        self.buy_usd += tx.usd
        bucket = self.flows.setdefault(tx.token, [])
        bucket.append((tx.tick, tx.whale, tx.usd, tx.symbol))
        if len(self.flows) > self.max_tokens:
            oldest = min(self.flows, key=lambda k: self.flows[k][0][0])
            self.flows.pop(oldest, None)

    def prune(self, tick: int) -> None:
        cutoff = tick - self.window
        for key in list(self.flows):
            bucket = [b for b in self.flows[key] if b[0] >= cutoff]
            if bucket:
                self.flows[key] = bucket
            else:
                self.flows.pop(key, None)

    # ----------------------------------------------------------------- sinyal
    def signal_for(self, token: str, tick: int, registry: WhaleRegistry) -> FlowSignal | None:
        bucket = self.flows.get(token)
        if not bucket:
            return None
        addresses = []
        net = 0.0
        rep_sum = 0.0
        for t, whale, usd, _sym in bucket:
            net += usd
            if whale not in addresses:
                addresses.append(whale)
                rep_sum += registry.reputation(whale)
        if not addresses:
            return None
        avg_rep = rep_sum / len(addresses)
        first = min(b[0] for b in bucket)
        recency = math.exp(-(tick - first) / max(1.0, self.window))

        size_score = min(1.0, math.log10(max(1.0, net) / 500.0) / 2.2)
        count_score = min(1.0, len(addresses) / 3.0)
        signal = (self.W_COUNT * count_score + self.W_SIZE * size_score
                  + self.W_REP * avg_rep) * (0.55 + 0.45 * recency)

        return FlowSignal(
            token=token, symbol=bucket[-1][3], whales=addresses, net_usd=net,
            avg_reputation=avg_rep, first_tick=first, signal=min(1.0, signal),
        )

    def top_signals(self, tick: int, registry: WhaleRegistry, n: int = 8) -> list[FlowSignal]:
        out = []
        for token in self.flows:
            s = self.signal_for(token, tick, registry)
            if s:
                out.append(s)
        out.sort(key=lambda s: -s.signal)
        return out[:n]

    def stats(self) -> dict:
        return {"tx": self.tx_count, "buy_usd": round(self.buy_usd, 0),
                "tokens_in_window": len(self.flows)}
