"""Pasar pump.fun sintetis yang digerakkan oleh whale.

Kenapa sintetis? Sandbox ini tidak punya akses ke RPC Solana / pump.fun API.
Tapi mekanika yang dimodelkan sama dengan yang ingin kamu pakai:

* token baru lahir terus-menerus (pump.fun: ribuan per hari),
* sekumpulan dompet whale bertindak, dan ukuran transaksi mereka **menggerakkan
  harga** (price impact) — inilah yang membuat "follow the smart money" masuk akal,
* sebagian token adalah rug: dipompa dulu supaya terlihat menarik, lalu dev
  mengeluarkan likuiditasnya dalam satu tick,
* atribut yang bisa dilihat (dev %, bundle %, LP, mint authority, riwayat dev)
  memang berkorelasi dengan risiko rug — jadi forensics punya sesuatu untuk diukur.

Mode ``noise`` mematikan informasi whale: mereka memilih token secara acak.
Itu kontrol untuk membuktikan bahwa profit (kalau ada) datang dari sinyal,
bukan dari keberuntungan.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field

_WORDS = [
    "BONK", "WIF", "POPCAT", "MOON", "CHAD", "PEPE", "FROG", "DOGE", "CAT", "GIGA",
    "SOL", "JUP", "PUMP", "MOCHI", "BORK", "SNEK", "BANANA", "TURBO", "MILK", "BEAN",
    "COPE", "WOJAK", "GME", "APE", "DUCK", "GOAT", "MOG", "BOME", "RETARD", "FART",
]
_SUFFIX = ["", "2", "X", "AI", "INU", "COIN", "FI", "DAO", "Z", "420", "69", "ELON", "PUMP"]
_LABELS = ["Smart Money", "Early Sniper", "Dev-Adjacent", "Rotation Fund", "KOL Wallet",
           "Insider Cluster", "MEV Bundle", "Diamond Hand", "Sniper Bot", "Treasury"]


@dataclass
class Whale:
    address: str
    label: str
    skill: float          # 0..1 — peluang memilih token yang benar (laten)
    aggression: float     # peluang bertindak tiap tick
    size_lo: float
    size_hi: float


@dataclass
class MemeToken:
    address: str
    symbol: str
    name: str
    price: float
    p0: float
    liquidity_usd: float
    holders: int
    top10_pct: float
    dev_pct: float
    bundle_pct: float
    mint_revoked: bool
    lp_locked: bool
    dev_address: str
    dev_prior_rugs: int = 0
    quality: float = 0.5
    is_rug: bool = False
    rugged: bool = False
    age_ticks: int = 0
    created_tick: int = 0
    state: str = "seed"          # seed → pump → dump → dead
    pump_left: int = 0
    pump_rate: float = 0.0
    rug_at: int = 0
    volume_usd: float = 0.0
    whale_inflow: float = 0.0
    cap_mult: float = 2.0
    dead: bool = False
    dev_pct0: float = 0.0
    whale_buys: list[tuple[int, str, float]] = field(default_factory=list)


@dataclass
class WhaleTx:
    tick: int
    whale: str
    label: str
    token: str
    symbol: str
    side: str            # buy | sell
    usd: float
    price: float


class WhaleMarket:
    """Pasar + populasi whale. Semua deterministik per seed."""

    def __init__(self, seed: int = 21, tokens_per_tick: int = 6,
                 n_whales: int = 48, edge_mode: str = "informed"):
        self.rng = random.Random(seed)
        self.tokens_per_tick = tokens_per_tick
        self.edge_mode = edge_mode
        self.tick = 0
        self.scanned = 0
        self.tokens: dict[str, MemeToken] = {}
        self.txs: list[WhaleTx] = []
        self.whales = self._make_whales(n_whales)
        # Populasi dev terbatas: sebagian memang residivis, dan riwayatnya
        # terlihat oleh siapa pun yang mau mengecek on-chain.
        self.devs: list[tuple[str, float]] = [
            ("D" + "".join(self.rng.choice("0123456789abcdef") for _ in range(9)),
             self.rng.betavariate(0.7, 2.6))
            for _ in range(140)
        ]
        self.dev_rugs: dict[str, int] = {}
        self.dev_launches: dict[str, int] = {}

    # ------------------------------------------------------------------ setup
    def _make_whales(self, n: int) -> list[Whale]:
        r = self.rng
        out = []
        for i in range(n):
            skill = min(0.92, max(0.05, r.betavariate(2.2, 2.2)))
            if self.edge_mode == "noise":
                skill = 0.0            # kontrol: tidak ada informasi sama sekali
            out.append(Whale(
                address="W" + "".join(r.choice("0123456789abcdef") for _ in range(9)),
                label=f"{r.choice(_LABELS)} #{i+1:02d}",
                skill=skill,
                aggression=r.uniform(0.08, 0.45),
                size_lo=r.choice([200, 500, 1_000, 2_500, 5_000]),
                size_hi=r.choice([8_000, 15_000, 40_000, 90_000, 180_000]),
            ))
        return out

    def _make_token(self) -> MemeToken:
        r = self.rng
        dev_addr, dev_bias = r.choice(self.devs)
        is_rug = r.random() < (0.10 + 0.62 * dev_bias)
        prior = self.dev_rugs.get(dev_addr, 0)
        self.dev_launches[dev_addr] = self.dev_launches.get(dev_addr, 0) + 1
        # Rug pun ikut terbang dulu — itu umpannya.
        quality = r.uniform(0.45, 1.0) if is_rug else r.uniform(0.0, 1.0)

        if is_rug:
            dev_pct = r.uniform(16, 44)
            bundle = r.uniform(18, 55)
            top10 = r.uniform(45, 82)
            lp = r.random() < 0.18
            mint = r.random() < 0.30
        else:
            dev_pct = r.uniform(0.5, 11)
            bundle = r.uniform(0, 16)
            top10 = r.uniform(12, 42)
            lp = r.random() < 0.82
            mint = r.random() < 0.90

        p0 = r.uniform(2e-7, 3e-5)
        symbol = r.choice(_WORDS) + r.choice(_SUFFIX)
        if r.random() < 0.4:
            symbol += str(r.randint(1, 999))

        tok = MemeToken(
            address="T" + "".join(r.choice("0123456789abcdef") for _ in range(11)),
            symbol=symbol,
            name=symbol.capitalize() + r.choice([" Inu", " Coin", " AI", " Protocol", "", " 2.0"]),
            price=p0, p0=p0,
            liquidity_usd=r.uniform(1_500, 22_000),
            holders=r.randint(15, 260),
            top10_pct=top10, dev_pct=dev_pct, bundle_pct=bundle,
            mint_revoked=mint, lp_locked=lp,
            dev_address=dev_addr,
            quality=quality, is_rug=is_rug,
            created_tick=self.tick, dev_pct0=dev_pct, dev_prior_rugs=prior,
        )
        tok.rug_at = r.randint(3, 16)
        tok.cap_mult = 10 ** r.uniform(math.log10(1.15), math.log10(4.2))
        return tok

    # ------------------------------------------------------------------- tick
    def step(self, tick: int) -> tuple[list[MemeToken], list[WhaleTx]]:
        self.tick = tick
        r = self.rng
        n = max(1, int(r.gauss(self.tokens_per_tick, 1.6)))
        fresh = [self._make_token() for _ in range(n)]
        for t in fresh:
            self.tokens[t.address] = t
        self.scanned += n

        self.txs = []
        self._whales_act()
        for t in list(self.tokens.values()):
            self._advance(t)
            if t.dead:
                self.tokens.pop(t.address, None)
        return fresh, self.txs

    # ------------------------------------------------------------------ whale
    def _whales_act(self) -> None:
        r = self.rng
        live = [t for t in self.tokens.values() if not t.dead and t.age_ticks < 45
                and t.state in ("seed", "pump") and t.price < t.p0 * 6]
        if not live:
            return
        good = [t for t in live if t.quality >= 0.72] or live

        for w in self.whales:
            if r.random() > w.aggression:
                continue
            # whale yang "informed" memilih token bagus; mode noise memilih acak
            pool = good if (w.skill > 0 and r.random() < w.skill) else live
            tok = pool[int(r.random() * len(pool)) % len(pool)]
            if tok.state == "dump":
                continue
            usd = r.uniform(w.size_lo, w.size_hi)
            self._apply_buy(w, tok, usd)

    def _apply_buy(self, w: Whale, tok: MemeToken, usd: float) -> None:
        r = self.rng
        impact = min(0.30, usd / max(tok.liquidity_usd, 1.0) * 0.9)
        tok.price *= 1.0 + impact * 0.55
        tok.liquidity_usd += usd * 0.55
        tok.whale_inflow += usd
        tok.volume_usd += usd
        tok.holders += r.randint(5, 40)
        tok.whale_buys.append((self.tick, w.address, usd))

        if tok.state == "seed":
            # Transaksi pertama whale menyalakan pump — tapi TIDAK semua pump
            # berhasil. Hanya token dengan kualitas dasar tinggi yang benar-benar
            # "runner"; sisanya pump pendek lalu mati. Inilah yang membuat
            # mengikuti whale acak berbeda dengan mengikuti whale yang benar.
            # Tidak semua buy whale ditindaklanjuti pasar. Kalau tidak ada yang
            # ikut beli, harga hanya naik sesaat lalu balik — dan kita yang telat
            # masuk jadi penanggungnya.
            if r.random() > (0.18 + 0.68 * tok.quality):
                return
            tok.state = "pump"
            if tok.quality >= 0.72:
                k = (tok.quality - 0.72) / 0.28
                tok.pump_left = int(5 + 11 * k) + r.randint(0, 2)
                tok.pump_rate = 0.070 + 0.160 * k
                tok.cap_mult = 10 ** r.uniform(math.log10(1.25), math.log10(3.2))
            else:
                tok.pump_left = r.randint(2, 4)
                tok.pump_rate = 0.020 + 0.030 * tok.quality
                tok.cap_mult = 10 ** r.uniform(math.log10(1.05), math.log10(1.45))
        elif tok.state == "pump":
            tok.pump_left += 1 if r.random() < 0.4 else 0

        self.txs.append(WhaleTx(
            tick=self.tick, whale=w.address, label=w.label, token=tok.address,
            symbol=tok.symbol, side="buy", usd=usd, price=tok.price,
        ))

    # ------------------------------------------------------------------ price
    def _advance(self, t: MemeToken) -> None:
        r = self.rng
        t.age_ticks += 1

        if t.state == "pump":
            t.price *= 1.0 + t.pump_rate * r.uniform(0.45, 1.30)
            # bukan jalan lurus: satu candle merah bisa menghapus ekspektasi +50%
            if r.random() < 0.18:
                t.price *= r.uniform(0.78, 0.93)
            t.liquidity_usd *= r.uniform(1.00, 1.06)
            t.holders += r.randint(2, 30)
            t.pump_left -= 1
            if t.price >= t.p0 * t.cap_mult:
                t.state = "dump"
                t.dev_pct *= 0.4
                self._whales_exit(t)

            # dev mengeluarkan likuiditas: inilah rugpull
            if t.is_rug and t.age_ticks >= t.rug_at and r.random() < 0.35:
                t.price *= r.uniform(0.12, 0.35)
                t.liquidity_usd *= 0.18
                t.rugged = True
                t.dev_pct = 0.0
                t.state = "dump"
                self.dev_rugs[t.dev_address] = self.dev_rugs.get(t.dev_address, 0) + 1
                self.txs.append(WhaleTx(
                    tick=self.tick, whale=t.dev_address, label="DEV RUG",
                    token=t.address, symbol=t.symbol, side="sell",
                    usd=t.liquidity_usd, price=t.price,
                ))
            elif t.pump_left <= 0:
                t.state = "dump"
                t.dev_pct *= 0.3
                self._whales_exit(t)

        elif t.state == "dump":
            t.price *= r.uniform(0.78, 0.92)
            t.liquidity_usd *= r.uniform(0.90, 0.99)
            t.holders = int(t.holders * 0.97)

        else:  # seed
            t.price *= 1.0 + r.gauss(0, 0.02)
            t.liquidity_usd *= r.uniform(0.995, 1.02)
            t.holders += r.randint(0, 6)

        if t.price < t.p0 * 0.05 or t.age_ticks > 90:
            t.dead = True
        t.top10_pct = max(5.0, min(95.0, t.top10_pct + r.gauss(0, 0.6)))

    def _whales_exit(self, t: MemeToken) -> None:
        """Whale yang membeli ikut menjual di puncak — kita adalah exit liquidity-nya."""
        r = self.rng
        for tick, whale, usd in t.whale_buys[-4:]:
            self.txs.append(WhaleTx(
                tick=self.tick, whale=whale, label="Whale Exit", token=t.address,
                symbol=t.symbol, side="sell", usd=usd * r.uniform(0.6, 1.4),
                price=t.price,
            ))

    def close(self) -> None:
        pass


def growth_pct(tok: MemeToken) -> float:
    return (tok.price / tok.p0 - 1.0) * 100.0


def log_slug(x: float) -> float:
    return math.log10(max(1.0, x))
