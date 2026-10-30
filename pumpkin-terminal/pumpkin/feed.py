"""Feed pasar untuk Pumpkin Terminal.

Dua implementasi:

* ``SimMarket``  — generator pasar sintetis. Dipakai default karena sandbox/CI
  biasanya tidak punya akses ke RPC Solana. Token punya "archetype" laten
  (rug / dead / pump / solid), dan atribut yang *terlihat* oleh agen
  (likuiditas, holder, distribusi, aktivitas dev) memang berkorelasi dengan
  archetype itu. Jadi FILTER & ANALYST punya sinyal, seperti di pasar nyata.

  Yang penting: lonjakan harga TIDAK bisa diprediksi dari harga masa depan.
  Satu-satunya jejak yang tersedia adalah *buy pressure* beberapa tick sebelum
  lonjakan — persis seperti momentum di pasar sungguhan (dan sama rapuhnya).

* ``DexscreenerFeed`` — menarik pair Solana dari API publik Dexscreener.
  Ini *hanya data*, tidak ada eksekusi order dan tidak ada wallet.
"""

from __future__ import annotations

import json
import math
import random
import threading
import urllib.request
from typing import Iterable

from .models import Token

_WORDS = [
    "BONK", "WIF", "POP", "MOON", "CHAD", "PEPE", "FROG", "DOGE", "CAT", "DOG",
    "SOL", "JUP", "PUMP", "GIGA", "MOCHI", "BORK", "SNEK", "BANANA", "TURBO",
    "MILK", "BEAN", "COPE", "WOJAK", "GME", "APE", "DUCK", "GOAT", "MOG", "BOME",
]
_SUFFIX = ["", "2", "X", "AI", "INU", "COIN", "FI", "DAO", "Z", "420", "69", "ELON"]


class SimMarket:
    """Generator pasar memecoin sintetis yang deterministik per-seed."""

    ARCHETYPES = ("rug", "dead", "pump", "solid")
    WEIGHTS = (0.50, 0.28, 0.19, 0.03)

    def __init__(self, seed: int = 7, tokens_per_tick: int = 7, edge_mode: str = "correlated"):
        self.rng = random.Random(seed)
        self.tokens_per_tick = tokens_per_tick
        self.edge_mode = edge_mode
        self.live: dict[str, Token] = {}
        self.scanned = 0
        self.tick = 0

    # ------------------------------------------------------------------ create
    def _make_token(self) -> Token:
        r = self.rng
        arch = r.choices(self.ARCHETYPES, weights=self.WEIGHTS, k=1)[0]
        q = {"rug": 0.05, "dead": 0.30, "pump": 0.85, "solid": 0.95}[arch]

        p0 = r.uniform(1.2e-6, 6.0e-5)
        liq0 = r.uniform(2_000, 90_000)
        hold0 = int(r.lognormvariate(4.4, 0.7))          # median ~81
        top10 = max(4.0, min(92.0, 62 - 48 * q + r.gauss(0, 10)))
        dev = max(0.0, min(45.0, 15 - 14 * q + r.gauss(0, 3.2)))
        mint = r.random() < (0.28 + 0.64 * q)
        lp = r.random() < (0.24 + 0.68 * q)

        symbol = r.choice(_WORDS) + r.choice(_SUFFIX)
        if r.random() < 0.35:
            symbol += str(r.randint(1, 999))
        name = symbol.capitalize() + r.choice([" Inu", " Coin", " Terminal", " Protocol", "", " AI"])

        life = {
            "rug": r.randint(40, 240),
            "dead": r.randint(60, 320),
            "pump": r.randint(110, 380),
            "solid": r.randint(200, 600),
        }[arch]

        # Lonjakan: satu event tajam, bukan drift abadi.
        spike_tick = r.randint(14, max(15, int(life * 0.8)))
        spike_size = r.uniform(0.45, 2.10)       # e^0.45 = +57%, e^2.1 = +716%

        return Token(
            address="0x" + "".join(r.choice("0123456789abcdef") for _ in range(40)),
            symbol=symbol,
            name=name,
            price=p0,
            liquidity_usd=liq0,
            holders=hold0,
            top10_pct=top10,
            dev_pct=dev,
            mint_revoked=mint,
            lp_locked=lp,
            volume_usd=r.uniform(500, 25_000),
            buys=r.randint(5, 400),
            sells=r.randint(5, 400),
            created_tick=self.tick,
            archetype=arch,          # <-- laten, tidak pernah dipakai agen
            p0=p0,
            liq0=liq0,
            hold0=hold0,
            lifetime_ticks=life,
            rug_tick=r.randint(25, max(26, life - 5)),
            spike_tick=spike_tick,
            spike_size=spike_size,
        )

    # ------------------------------------------------------------------- tick
    def step(self, tick: int) -> list[Token]:
        """Majukan pasar satu tick, kembalikan token baru yang tercipta."""
        self.tick = tick
        r = self.rng
        n = max(1, int(r.gauss(self.tokens_per_tick, 1.8)))
        fresh = [self._make_token() for _ in range(n)]
        for t in fresh:
            self.live[t.address] = t
        self.scanned += n

        for addr, tok in list(self.live.items()):
            self._advance(tok)
            if tok.dead:
                self.live.pop(addr, None)
        return fresh

    def _advance(self, t: Token) -> None:
        r = self.rng
        t.age_ticks += 1
        arch = t.archetype

        # ---- harga
        if arch == "pump":
            if t.age_ticks >= t.spike_tick + 12:
                drift, vol = -0.014, 0.052   # distribusi: yang telat kena dump
            elif t.age_ticks >= t.spike_tick:
                drift, vol = 0.003, 0.050
            elif t.age_ticks >= t.spike_tick - 8:
                drift, vol = 0.011, 0.021    # akumulasi: satu-satunya sinyal nyata
            else:
                drift, vol = 0.0005, 0.036
        elif arch == "solid":
            drift, vol = 0.0015, 0.030
        elif arch == "dead":
            drift, vol = -0.0025, 0.028
        else:  # rug
            drift = 0.0015 if t.age_ticks < t.rug_tick else -0.02
            vol = 0.048

        t.logprice = max(-8.0, min(9.0, t.logprice + drift + r.gauss(0, vol)))

        if arch == "pump" and t.age_ticks == t.spike_tick:
            t.logprice += t.spike_size
            t.volume_usd *= r.uniform(3, 8)

        if arch == "rug" and t.age_ticks == t.rug_tick:
            t.logprice -= r.uniform(2.4, 4.3)      # -91% s/d -98.6%
            t.rugged = True
            t.liquidity_usd *= 0.22
            t.dev_pct = max(t.dev_pct, 55.0)
            t.holders = int(t.holders * 0.55)

        t.price = t.p0 * math.exp(t.logprice)
        t._recent.append(t.logprice)
        if len(t._recent) > 6:
            t._recent.pop(0)
        if len(t._recent) >= 6:
            t.change_5_pct = (math.exp(t._recent[-1] - t._recent[0]) - 1.0) * 100.0

        # ---- likuiditas & holder: tumbuh organik seiring umur (attention),
        #      bukan semata mengikuti harga. Inilah kenapa pair "terlihat bagus"
        #      justru sering muncul SETELAH lonjakan selesai.
        attention = 1.0 + 0.020 * t.age_ticks + r.uniform(-0.04, 0.04)
        t.liquidity_usd = max(400.0, t.liq0 * attention)
        t.holders = int(max(20, t.hold0 * (1.0 + 0.028 * t.age_ticks)))
        t.volume_usd += t.liquidity_usd * r.uniform(0.004, 0.05)
        if r.random() < 0.5:
            t.buys += r.randint(1, 9)
        else:
            t.sells += r.randint(1, 9)

        if t.age_ticks >= t.lifetime_ticks or t.price < t.p0 * 0.012:
            t.dead = True

    def close(self) -> None:  # kompatibel dengan feed live
        pass


class DexscreenerFeed:
    """Feed live (data saja) dari Dexscreener — untuk dijalankan di mesin lokal.

    Bot tetap *paper trading*: tidak ada wallet, tidak ada order nyata.
    Butuh internet publik (sandbox Arena membatasi egress, jadi mode ini gagal
    di sandbox dan itu memang diharapkan).
    """

    SEARCH_URLS = (
        "https://api.dexscreener.com/token-profiles/latest/v1",
        "https://api.dexscreener.com/latest/dex/search?q=SOL/USDC",
    )

    def __init__(self, poll_seconds: float = 5.0, max_tokens: int = 60):
        self.poll_seconds = poll_seconds
        self.max_tokens = max_tokens
        self.tick = 0
        self.scanned = 0
        self.live: dict[str, Token] = {}
        self._seen: set[str] = set()
        self._pending: list[Token] = []
        self._lock = threading.Lock()
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._poll_loop, daemon=True)

    def start(self) -> None:
        self._thread.start()

    def close(self) -> None:
        self._stop.set()

    def _fetch(self) -> list[dict]:
        out: list[dict] = []
        for url in self.SEARCH_URLS:
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "pumpkin-terminal/1.0"})
                with urllib.request.urlopen(req, timeout=8) as resp:
                    payload = json.loads(resp.read().decode())
            except Exception:
                continue
            pairs = payload.get("pairs") or payload.get("data") or []
            if isinstance(pairs, list):
                out.extend([p for p in pairs if p.get("chainId") == "solana"])
        return out

    def _poll_loop(self) -> None:
        while not self._stop.is_set():
            for p in self._fetch():
                addr = str(p.get("pairAddress", ""))
                if not addr or addr in self._seen:
                    continue
                self._seen.add(addr)
                try:
                    price = float(p.get("priceUsd") or 0) or 1e-6
                    liq = float((p.get("liquidity") or {}).get("usd") or 0)
                    vol = float((p.get("volume") or {}).get("h24") or 0)
                    chg = float((p.get("priceChange") or {}).get("m5") or 0)
                except (TypeError, ValueError):
                    continue
                tok = Token(
                    address=addr,
                    symbol=str((p.get("baseToken") or {}).get("symbol", "?")),
                    name=str((p.get("baseToken") or {}).get("name", "?")),
                    price=price,
                    liquidity_usd=liq,
                    holders=0,           # tidak tersedia di endpoint publik
                    top10_pct=0.0,
                    dev_pct=0.0,
                    mint_revoked=False,  # tidak diketahui => FILTER menolak
                    lp_locked=False,
                    volume_usd=vol,
                    change_5_pct=chg,
                    created_tick=self.tick,
                )
                with self._lock:
                    self.live[addr] = tok
                    self._pending.append(tok)
                    self.scanned += 1
                if len(self.live) > self.max_tokens:
                    oldest = min(self.live.values(), key=lambda x: x.created_tick)
                    self.live.pop(oldest.address, None)
            self._stop.wait(self.poll_seconds)

    def step(self, tick: int) -> list[Token]:
        self.tick = tick
        with self._lock:
            fresh, self._pending = self._pending, []
        return fresh


def make_feed(cfg) -> Iterable:
    if cfg.sim.feed == "dexscreener":
        feed = DexscreenerFeed()
        feed.start()
        return feed
    return SimMarket(seed=cfg.sim.seed, tokens_per_tick=cfg.sim.tokens_per_tick,
                     edge_mode=cfg.sim.edge_mode)
