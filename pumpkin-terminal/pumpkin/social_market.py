"""Pasar simulasi yang digerakkan oleh media sosial + whale.

Yang dimodelkan, sesuai temuan riset:

* KOL asli (reach tinggi, reputasi naik-turun) memosting karena mereka melihat
  akumulasi whale → harga naik bertahap (social premium),
* dev membayar **bot farm** untuk memosting serempak dengan teks nyaris identik
  → token naik sebentar lalu rug (shill trap),
* berita makro (listing, partnership, hack, regulasi) mengubah rezim pasar,
* harga bereaksi dengan **lag**, jadi yang membaca lebih cepat menang sedikit,
  dan yang terlambat menjadi exit liquidity.

Mode ``clean`` mematikan bot farm: semua post jujur. Itu kontrol untuk mengukur
apakah lapisan deteksi koordinasi benar-benar berguna.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass

from .social_signal import SocialPost, extract_tickers
from .whale_market import MemeToken, WhaleMarket

_POS_TMPL = [
    "${sym} accumulation is real. Dev wallet clean, LP locked. Watching this one.",
    "Quiet buying on ${sym} for 3 hours straight. No hype, just fills.",
    "${sym} has the cleanest holder distribution I've seen this week. 🚀",
    "Loaded a bag of ${sym}. Bundles look clean, top 10 under 30%.",
    "${sym} volume is accelerating while price is still flat. Classic.",
    "Don't sleep on ${sym}. Organic growth, no coordinated shill.",
]
_NEG_TMPL = [
    "${sym} top wallets just moved out. Careful.",
    "${sym} looks like a honeypot, sell simulation fails.",
    "Avoid ${sym}: dev still holds mint authority.",
]
_BOT_TMPL = [
    "🚀🚀 ${sym} TO THE MOON 100X GUARANTEED!!!",
    "🔥 ${sym} 100x gem, dev based, LP locked, easy money!!!",
    "${sym} is the next 1000x, guaranteed, don't miss!!!",
    "GUARANTEED ${sym} 100x, risk free, buy now!!!",
]

_NEWS = [
    ("listing", 1, "Major exchange lists a memecoin pair — risk appetite up"),
    ("partnership", 1, "Ecosystem partnership announced — narrative strength up"),
    ("hack", -1, "Exploit on a bridge — risk appetite down"),
    ("regulation", -1, "Regulator signals tighter rules — risk appetite down"),
    ("rotation", 1, "Capital rotating from majors into memecoins"),
]


@dataclass
class Kol:
    handle: str
    followers: int
    following: int
    age_days: int
    skill: float          # peluang memosting token yang benar-benar akan naik
    kind: str = "kol"     # kol | bot | normie
    label: str = ""


@dataclass
class NewsEvent:
    tick: int
    kind: str
    direction: int
    headline: str

    def public(self) -> dict:
        return {"tick": self.tick, "kind": self.kind,
                "direction": self.direction, "headline": self.headline}


class SocialMarket(WhaleMarket):
    def __init__(self, seed: int = 21, tokens_per_tick: int = 6, n_whales: int = 48,
                 edge_mode: str = "informed", n_kols: int = 45, n_bots: int = 220,
                 bot_farms: bool = True):
        super().__init__(seed, tokens_per_tick, n_whales, edge_mode)
        self.bot_farms = bot_farms
        self.kols = self._make_kols(n_kols)
        self.bots = self._make_bots(n_bots)
        self.news: list[NewsEvent] = []
        self.regime = 0.6            # 0..1 — selera risiko pasar
        self._next_news = 90
        self.shill: set[str] = set()

    # ------------------------------------------------------------------ setup
    def _make_kols(self, n: int) -> list[Kol]:
        r = self.rng
        out = []
        for i in range(n):
            followers = int(10 ** r.uniform(3.4, 5.9))
            out.append(Kol(
                handle=f"@{r.choice(['ct', 'degen', 'sol', 'alpha', 'moon'])}{i:02d}",
                followers=followers,
                following=int(followers * r.uniform(0.02, 0.6)),
                age_days=int(r.uniform(120, 2200)),
                skill=min(0.95, max(0.05, r.betavariate(2.0, 2.2))),
                label=r.choice(["Trader", "On-chain sleuth", "Fund", "Anon", "KOL"]),
            ))
        return out

    def _make_bots(self, n: int) -> list[Kol]:
        r = self.rng
        return [Kol(handle=f"@bot{i:03d}", followers=int(r.uniform(20, 900)),
                    following=int(r.uniform(300, 4_000)), age_days=int(r.uniform(1, 9)),
                    skill=0.0, kind="bot", label="farm") for i in range(n)]

    # ------------------------------------------------------------------- tick
    def step(self, tick: int):
        self.tick = tick
        r = self.rng

        n = max(1, int(r.gauss(self.tokens_per_tick, 1.6)))
        fresh = [self._make_token() for _ in range(n)]
        for t in fresh:
            self.tokens[t.address] = t
            # sebagian token adalah jebakan: dev menyewa bot farm
            if self.bot_farms and t.is_rug and r.random() < 0.55:
                self.shill.add(t.address)
            elif self.bot_farms and not t.is_rug and r.random() < 0.18:
                # iklan bayar: token lumayan, tapi hype-nya dibeli — bukan organik
                self.shill.add(t.address)
        self.scanned += n

        self.txs = []
        self._whales_act()

        posts = self._social_activity(tick)
        self._apply_social_pressure(posts)

        for t in list(self.tokens.values()):
            self._advance(t)
            if t.dead:
                self.tokens.pop(t.address, None)

        self._maybe_news(tick)
        self.regime = min(1.0, max(0.0, self.regime + r.gauss(0, 0.01)))
        return fresh, self.txs, posts, list(self.news)

    # ----------------------------------------------------------------- sosial
    def _social_activity(self, tick: int) -> list[SocialPost]:
        r = self.rng
        posts: list[SocialPost] = []
        live = [t for t in self.tokens.values()
                if not t.dead and 1 <= t.age_ticks <= 40 and t.state in ("seed", "pump")]

        # 1. KOL asli: makin bagus tokennya, makin mungkin mereka menyebutnya
        for tok in live:
            if r.random() > 0.05 + 0.30 * tok.quality:
                continue
            kol = self.kols[int(r.random() * len(self.kols)) % len(self.kols)]
            informed = kol.skill > 0 and r.random() < kol.skill
            if not informed and r.random() < 0.65:
                continue                       # KOL tanpa info biasanya diam
            sym = tok.symbol
            text = r.choice(_POS_TMPL).replace("${sym}", "$" + sym)
            posts.append(SocialPost(
                id=f"p{tick}-{len(posts)}", tick=tick, author=kol.handle,
                followers=kol.followers, following=kol.following,
                account_age_days=kol.age_days, text=text,
                tickers=extract_tickers(text), sentiment=0.8, confidence=0.75,
                likes=int(kol.followers * r.uniform(0.01, 0.08)),
                reposts=int(kol.followers * r.uniform(0.002, 0.02)),
                replies=int(kol.followers * r.uniform(0.001, 0.01)),
            ))
            tok.social_boost = min(0.09, getattr(tok, "social_boost", 0.0)
                                   + 0.020 + 0.030 * kol.skill * tok.quality)
            tok.hype_age = 0
            tok.hype_peak = max(getattr(tok, "hype_peak", 0.0), tok.social_boost)

        # 2. Bot farm: serempak, teks kembar, akun baru
        for addr in list(self.shill):
            tok = self.tokens.get(addr)
            if tok is None:
                self.shill.discard(addr)
                continue
            if tok.age_ticks < tok.rug_at - 5 or tok.age_ticks > tok.rug_at:
                continue
            for _ in range(r.randint(4, 9)):
                bot = self.bots[int(r.random() * len(self.bots)) % len(self.bots)]
                text = _BOT_TMPL[0].replace("${sym}", "$" + tok.symbol)
                posts.append(SocialPost(
                    id=f"b{tick}-{len(posts)}", tick=tick, author=bot.handle,
                    followers=bot.followers, following=bot.following,
                    account_age_days=bot.age_days, text=text,
                    tickers=extract_tickers(text), sentiment=0.95, confidence=0.2,
                    likes=int(r.uniform(0, 12)), reposts=int(r.uniform(0, 4)),
                    replies=int(r.uniform(0, 3)), is_bot=True,
                ))
            # Iklan bayar tidak menciptakan permintaan nyata: harga naik 2-3 tick
            # karena bot, lalu jatuh. Pembeli terlambat menanggung selisihnya.
            tok.trap_ticks = r.randint(2, 3)
            tok.social_boost = min(0.03, getattr(tok, "social_boost", 0.0) + 0.015)
            tok.hype_age = 0
            tok.hype_peak = max(getattr(tok, "hype_peak", 0.0), tok.social_boost)

        # 3. Sesekali sentimen negatif jujur (on-chain sleuth)
        if r.random() < 0.03 and live:
            tok = live[int(r.random() * len(live))]
            kol = self.kols[0]
            text = _NEG_TMPL[0].replace("${sym}", "$" + tok.symbol)
            posts.append(SocialPost(
                id=f"n{tick}", tick=tick, author=kol.handle, followers=kol.followers,
                following=kol.following, account_age_days=kol.age_days, text=text,
                tickers=extract_tickers(text), sentiment=-0.9, confidence=0.8,
                likes=int(kol.followers * 0.01), reposts=3, replies=8,
            ))
            tok.social_boost = max(-0.05, getattr(tok, "social_boost", 0.0) - 0.02)

        return posts

    def _apply_social_pressure(self, posts: list[SocialPost]) -> None:
        """Post bot tidak menaikkan harga banyak — pasar tahu itu palsu."""
        for p in posts:
            for sym in p.tickers:
                tok = next((t for t in self.tokens.values() if t.symbol == sym), None)
                if tok and p.is_bot:
                    tok.social_boost = getattr(tok, "social_boost", 0.0) * 0.7

    def _advance(self, t: MemeToken) -> None:
        super()._advance(t)
        if t.dead:
            return
        r = self.rng
        trap = getattr(t, "trap_ticks", 0)
        if trap > 0:
            t.trap_ticks = trap - 1
            t.price *= 1.030
            if t.trap_ticks == 0:
                t.price *= r.uniform(0.74, 0.87)     # shill selesai, harga dikembalikan
            return
        boost = getattr(t, "social_boost", 0.0)
        age = getattr(t, "hype_age", 0)

        if boost > 0.005:
            # hype masih hidup: harga naik, tapi makin tipis tiap tick
            t.price *= 1.0 + boost * (0.6 + 0.8 * self.regime)
            t.social_boost = boost * 0.82
            t.hype_age = age + 1
            # hype tidak pernah jadi tangga lurus: ada candle merah di tengah jalan
            if r.random() < 0.06:
                t.price *= r.uniform(0.88, 0.95)
        elif age and age < 12:
            # "beli rumor, jual berita": pembeli terlambat menjadi exit liquidity
            fade = (0.008 + 0.014 * min(1.0, age / 8.0)) * (0.7 + 0.6 * self.regime)
            t.price *= 1.0 - fade * r.uniform(0.5, 1.5)
            t.social_boost = 0.0
            t.hype_age = age + 1
            if r.random() < 0.18:
                t.price *= r.uniform(0.82, 0.93)
        t.social_boost = getattr(t, "social_boost", 0.0)

    # ------------------------------------------------------------------ berita
    def _maybe_news(self, tick: int) -> None:
        if tick < self._next_news:
            return
        r = self.rng
        kind, direction, headline = _NEWS[int(r.random() * len(_NEWS)) % len(_NEWS)]
        self.news.append(NewsEvent(tick=tick, kind=kind, direction=direction,
                                   headline=headline))
        self.news = self.news[-20:]
        self.regime = min(1.0, max(0.0, self.regime + 0.25 * direction))
        self._next_news = tick + int(r.uniform(90, 220))

    # ------------------------------------------------------------------ util
    def upside_estimate(self, tok: MemeToken) -> float:
        """Perkiraan upside realistis (0..1) dari likuiditas + kualitas + umur.

        Ini yang mencegah "memaksakan" target yang tidak didukung pasar.
        """
        liq = math.log10(max(1.0, tok.liquidity_usd)) / 6.0
        base = 0.10 + 0.55 * tok.quality * min(1.0, liq)
        if tok.is_rug:
            base *= 0.55
        if tok.state == "dump":
            base *= 0.3
        cap = max(0.0, tok.cap_mult - 1.0)
        return max(0.02, min(1.2, base * (0.6 + 0.4 * cap)))
