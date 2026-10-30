"""Sinyal sosial-media: dari postingan mentah ke probabilitas menang.

Lapisan, dari bawah ke atas:

1. ``score_text``        — lexicon finansial/meme, sadar negasi & intensifier
2. ``InfluenceGraph``    — reach + reputasi empiris per akun
3. ``CoordinationDetector`` — 5 fitur untuk memisahkan orang asli dari bot bayaran
4. ``SocialAggregator``  — velocity, akselerasi, konsentrasi, reach tertimbang
5. ``AlphaEngine``       — gabungkan semuanya menjadi p̂ (probabilitas menang),
                           EV, target minimum yang diturunkan dari biaya, dan sizing

Semua angka 0..1 kecuali dinyatakan lain. Tidak ada dependensi eksternal;
``score_text`` adalah satu-satunya tempat yang perlu diganti kalau kamu mau
memakai model FinBERT/LLM.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, field

# --------------------------------------------------------------------------- #
# 1. Lexicon
# --------------------------------------------------------------------------- #
_POS = {
    "moon": 1.0, "mooning": 1.0, "pump": 0.8, "pumping": 0.9, "send": 0.6, "sending": 0.7,
    "bullish": 1.0, "bull": 0.7, "gem": 1.0, "undervalued": 0.8, "breakout": 0.9,
    "ath": 0.8, "buy": 0.6, "buying": 0.7, "accumulate": 0.8, "accumulating": 0.8,
    "hodl": 0.6, "diamond": 0.5, "based": 0.6, "alpha": 0.7, "listing": 0.9,
    "partnership": 0.8, "launch": 0.5, "trending": 0.7, "volume": 0.4, "organic": 0.7,
    "rugproof": 0.8, "locked": 0.6, "burned": 0.7, "burn": 0.6, "airdrop": 0.7,
    "🚀": 0.9, "🔥": 0.7, "💎": 0.6, "📈": 0.8, "🌕": 0.9, "🙌": 0.4, "🟢": 0.6,
}
_NEG = {
    "rug": -1.0, "rugged": -1.0, "rugpull": -1.0, "scam": -1.0, "honeypot": -1.0,
    "dump": -0.8, "dumping": -0.9, "sell": -0.6, "selling": -0.7, "bearish": -1.0,
    "dead": -0.8, "jeet": -0.7, "exit": -0.5, "unlocked": -0.8, "mintable": -0.9,
    "bundled": -0.8, "dev": -0.2, "insider": -0.6, "exploit": -1.0, "hack": -1.0,
    "lawsuit": -0.8, "delist": -0.9, "warning": -0.6, "avoid": -0.7, "trap": -0.9,
    "📉": -0.8, "🔴": -0.6, "💀": -0.7, "⚠️": -0.5, "🧻": -0.5,
}
_INTENS = {"very": 1.5, "super": 1.6, "extremely": 1.7, "insanely": 1.8,
           "totally": 1.4, "literally": 1.3, "really": 1.25, "so": 1.2, "big": 1.3}
_NEGATORS = {"not", "no", "never", "don't", "dont", "isn't", "isnt", "won't", "wont",
             "can't", "cant", "avoid", "without", "stopped"}
_HYPE_RE = re.compile(r"(100x|1000x|10000x|next\s*100x|guaranteed|risk\s*free|"
                      r"can'?t\s*lose|easy\s*money|free\s*money)", re.I)
_CASH_RE = re.compile(r"\$([A-Za-z][A-Za-z0-9]{1,11})")


def score_text(text: str) -> tuple[float, float]:
    """Kembalikan (sentimen −1..1, keyakinan 0..1).

    Aturan yang membuat ini lebih baik dari hitung kata naif:
    * negasi membalik tanda kata berikutnya ("not bullish" ≠ bullish),
    * intensifier menaikkan magnitudo,
    * klaim berlebihan (guaranteed, 1000x) **menurunkan** keyakinan — dalam data
      historis, bahasa seperti itu justru penanda shill, bukan kualitas.
    """
    words = re.findall(r"[$#]?[A-Za-z']+|[\U0001F300-\U0001FAFF\u2600-\u27BF]", text)
    total, hits = 0.0, 0
    negate = False
    mult = 1.0

    for w in words:
        lw = w.lower()
        if lw in _NEGATORS:
            negate = True
            continue
        if lw in _INTENS:
            mult = _INTENS[lw]
            continue
        val = _POS.get(lw, 0.0) or _NEG.get(lw, 0.0)
        if val:
            total += (-val if negate else val) * mult
            hits += 1
        negate, mult = False, 1.0

    if not hits:
        return 0.0, 0.2

    raw = total / (hits ** 0.6)
    sentiment = max(-1.0, min(1.0, raw / 2.0))
    confidence = min(1.0, 0.35 + 0.25 * hits)

    if _HYPE_RE.search(text):
        confidence *= 0.55          # bahasa iklan = sinyal lemah
    if text.count("!") >= 3 or text.upper() == text and len(text) > 20:
        confidence *= 0.7           # teriakan bukan analisis
    return sentiment, round(confidence, 3)


def extract_tickers(text: str) -> list[str]:
    out = [m.group(1).upper() for m in _CASH_RE.finditer(text)]
    out += [m.group(0)[1:].upper() for m in re.finditer(r"#\$?[A-Za-z][A-Za-z0-9]{1,11}", text)]
    seen, uniq = set(), []
    for t in out:
        if t not in seen and len(t) >= 2:
            seen.add(t)
            uniq.append(t)
    return uniq


# --------------------------------------------------------------------------- #
# 2. Post & akun
# --------------------------------------------------------------------------- #
@dataclass
class SocialPost:
    id: str
    tick: int
    author: str
    followers: int
    following: int
    account_age_days: int
    text: str
    tickers: list[str]
    sentiment: float
    confidence: float
    likes: int = 0
    reposts: int = 0
    replies: int = 0
    is_bot: bool = False

    @property
    def engagement(self) -> int:
        return self.likes + 3 * self.reposts + self.replies

    @property
    def engagement_rate(self) -> float:
        return self.engagement / max(1, self.followers)

    def shingles(self, k: int = 3) -> set[str]:
        words = re.findall(r"[a-z0-9]+", self.text.lower())
        return {" ".join(words[i:i + k]) for i in range(max(0, len(words) - k + 1))}


@dataclass
class InfluenceAccount:
    handle: str
    followers: int
    following: int
    account_age_days: int
    kind: str = "kol"            # kol | normie | bot
    hits: int = 0
    misses: int = 0

    @property
    def reputation(self) -> float:
        return (self.hits + 1.0) / (self.hits + self.misses + 2.0)

    @property
    def reach(self) -> float:
        """Reach ternormalisasi: log follower, dipotong, dikali rasio sehat."""
        base = math.log10(max(10, self.followers)) / 6.0          # 10 → 0, 1e6 → 1
        ratio = self.following / max(1, self.followers)
        healthy = 1.0 if ratio < 0.5 else (0.55 if ratio < 2 else 0.25)
        age = 1.0 if self.account_age_days >= 90 else (
            0.6 if self.account_age_days >= 30 else 0.25)
        return max(0.0, min(1.0, base * healthy * age))

    def public(self) -> dict:
        return {"handle": self.handle, "followers": self.followers, "kind": self.kind,
                "reputation": round(self.reputation, 3), "reach": round(self.reach, 3),
                "hits": self.hits, "misses": self.misses}


class InfluenceGraph:
    def __init__(self) -> None:
        self.accounts: dict[str, InfluenceAccount] = {}

    def upsert(self, post: SocialPost) -> InfluenceAccount:
        acc = self.accounts.get(post.author)
        if acc is None:
            acc = InfluenceAccount(
                handle=post.author, followers=post.followers, following=post.following,
                account_age_days=post.account_age_days,
                kind="bot" if post.is_bot else ("kol" if post.followers >= 20_000 else "normie"),
            )
            self.accounts[post.author] = acc
        return acc

    def mark(self, handle: str, hit: bool) -> None:
        acc = self.accounts.get(handle)
        if acc is None:
            return
        if hit:
            acc.hits += 1
        else:
            acc.misses += 1

    def reputation(self, handle: str) -> float:
        acc = self.accounts.get(handle)
        return acc.reputation if acc else 0.5

    def reach(self, handle: str) -> float:
        acc = self.accounts.get(handle)
        return acc.reach if acc else 0.2

    def leaderboard(self, n: int = 10) -> list[dict]:
        rows = [a for a in self.accounts.values() if a.hits + a.misses >= 1]
        rows.sort(key=lambda a: (-a.reputation, -a.reach))
        return [a.public() for a in rows[:n]]

    def stats(self) -> dict:
        acc = list(self.accounts.values())
        kol = [a for a in acc if a.kind == "kol"]
        return {
            "accounts": len(acc),
            "kols": len(kol),
            "bots": sum(1 for a in acc if a.kind == "bot"),
            "avg_reputation": round(sum(a.reputation for a in acc) / len(acc), 3) if acc else 0.5,
        }


# --------------------------------------------------------------------------- #
# 3. Deteksi koordinasi
# --------------------------------------------------------------------------- #
@dataclass
class CoordinationReport:
    score: float
    duplicate_ratio: float
    burst_ratio: float
    new_account_ratio: float
    bad_follower_ratio: float
    concentration: float
    findings: list[str] = field(default_factory=list)

    def public(self) -> dict:
        return {
            "score": round(self.score, 3),
            "duplicate": round(self.duplicate_ratio, 2),
            "burst": round(self.burst_ratio, 2),
            "new_accounts": round(self.new_account_ratio, 2),
            "bad_follow_ratio": round(self.bad_follower_ratio, 2),
            "concentration": round(self.concentration, 2),
            "findings": self.findings,
        }


class CoordinationDetector:
    """Lima fitur, semuanya O(n) dan dihitung di bawah 1 ms untuk n kecil."""

    W_DUP, W_BURST, W_NEW, W_RATIO, W_CONC = 0.30, 0.24, 0.18, 0.14, 0.14

    def score(self, posts: list[SocialPost], tick: int, window: int = 3) -> CoordinationReport:
        if not posts:
            return CoordinationReport(0.0, 0, 0, 0, 0, 0)

        # 1. duplikasi teks (klon) — Jaccard terhadap median shingle set
        shingle_sets = [p.shingles() for p in posts]
        dup = 0
        for i, a in enumerate(shingle_sets):
            for b in shingle_sets[i + 1:]:
                if not a or not b:
                    continue
                j = len(a & b) / len(a | b)
                if j >= 0.72:
                    dup += 1
        pairs = max(1, len(posts) * (len(posts) - 1) / 2)
        duplicate_ratio = min(1.0, dup / pairs * 2.0)

        # 2. burst: semua muncul dalam ≤ window tick
        recent = [p for p in posts if tick - p.tick <= window]
        burst_ratio = len(recent) / len(posts)

        # 3. akun baru
        new_ratio = sum(1 for p in posts if p.account_age_days < 7) / len(posts)

        # 4. rasio follower/following tidak wajar
        bad_ratio = sum(1 for p in posts
                        if p.following > max(50, p.followers * 2)) / len(posts)

        # 5. konsentrasi: satu ticker mendominasi
        counter: dict[str, int] = {}
        for p in posts:
            for t in p.tickers:
                counter[t] = counter.get(t, 0) + 1
        top = max(counter.values()) if counter else 0
        concentration = top / len(posts)

        score = (self.W_DUP * duplicate_ratio + self.W_BURST * burst_ratio
                 + self.W_NEW * new_ratio + self.W_RATIO * bad_ratio
                 + self.W_CONC * concentration)

        findings = []
        if duplicate_ratio > 0.35:
            findings.append("teks kembar antar akun")
        if new_ratio > 0.4:
            findings.append("banyak akun baru")
        if concentration > 0.8 and len(posts) >= 6:
            findings.append("semua menempel satu ticker")
        if bad_ratio > 0.35:
            findings.append("rasio follower tidak wajar")

        return CoordinationReport(min(1.0, score), duplicate_ratio, burst_ratio,
                                  new_ratio, bad_ratio, concentration, findings)


# --------------------------------------------------------------------------- #
# 4. Agregasi
# --------------------------------------------------------------------------- #
@dataclass
class SocialSignal:
    token: str
    symbol: str
    posts: int = 0
    unique_authors: int = 0
    reach: float = 0.0
    sentiment: float = 0.0
    velocity: float = 0.0          # post per tick (jendela)
    acceleration: float = 0.0      # perubahan velocity vs jendela sebelumnya
    coordination: float = 0.0
    bot_share: float = 0.0
    reputation: float = 0.5
    strength: float = 0.0          # 0..1 gabungan
    findings: list[str] = field(default_factory=list)

    def public(self) -> dict:
        return {
            "symbol": self.symbol, "posts": self.posts, "authors": self.unique_authors,
            "reach": round(self.reach, 2), "sentiment": round(self.sentiment, 2),
            "velocity": round(self.velocity, 2), "accel": round(self.acceleration, 2),
            "coordination": round(self.coordination, 2), "bots": round(self.bot_share, 2),
            "reputation": round(self.reputation, 2), "strength": round(self.strength, 2),
            "findings": self.findings,
        }


class SocialAggregator:
    """Mengubah daftar post menjadi satu kekuatan sinyal per token.

    Yang dipakai adalah **turunan** (velocity, akselerasi, konsentrasi), bukan
    level mentah — karena level mudah dibeli, turunan butuh biaya lebih besar.
    """

    def __init__(self, window: int = 8, detector: CoordinationDetector | None = None):
        self.window = window
        self.detector = detector or CoordinationDetector()
        self.posts: list[SocialPost] = []
        self.max_posts = 4_000

    def ingest(self, posts: list[SocialPost]) -> None:
        self.posts.extend(posts)
        if len(self.posts) > self.max_posts:
            self.posts = self.posts[-self.max_posts:]

    def prune(self, tick: int) -> None:
        cutoff = tick - self.window * 3
        self.posts = [p for p in self.posts if p.tick >= cutoff]

    def signal_for(self, token: str, tick: int, graph: InfluenceGraph,
                   naive: bool = False) -> SocialSignal | None:
        """``naive=True`` = trader yang tidak punya detektor koordinasi.

        Dipakai sebagai lengan pembanding di benchmark: kalau angka naive tidak
        lebih buruk, berarti lapisan deteksi ini tidak layak dipakai.
        """
        recent = [p for p in self.posts if token in p.tickers and tick - p.tick <= self.window]
        if not recent:
            return None
        prev = [p for p in self.posts if token in p.tickers
                and self.window < tick - p.tick <= self.window * 2]

        authors = {p.author for p in recent}
        reach = sum(graph.reach(p.author) * (0.5 + p.confidence) for p in recent)
        reach_norm = min(1.0, reach / 3.0)
        sentiment = sum(p.sentiment * p.confidence for p in recent) / max(1e-9, sum(p.confidence for p in recent))
        velocity = len(recent) / self.window
        acceleration = velocity - (len(prev) / self.window)
        report = self.detector.score(recent, tick)
        coordination = 0.0 if naive else report.score
        bot_share = 0.0 if naive else sum(1 for p in recent if p.is_bot) / len(recent)
        reputation = sum(graph.reputation(a) for a in authors) / len(authors)

        strength = (
            0.34 * min(1.0, velocity / 1.2)
            + 0.22 * reach_norm
            + 0.16 * max(0.0, min(1.0, (acceleration + 0.3) / 0.9))
            + 0.16 * ((sentiment + 1) / 2)
            + 0.12 * reputation
        ) * (1.0 - 0.65 * coordination) * (1.0 - 0.5 * bot_share)
        reputation = 0.5 if naive else reputation

        return SocialSignal(
            token=token, symbol=token,
            posts=len(recent), unique_authors=len(authors), reach=reach_norm,
            sentiment=sentiment, velocity=velocity, acceleration=acceleration,
            coordination=coordination, bot_share=bot_share, reputation=reputation,
            strength=max(0.0, min(1.0, strength)),
            findings=[] if naive else list(report.findings),
        )

    def top(self, tick: int, graph: InfluenceGraph, n: int = 8,
            naive: bool = False) -> list[SocialSignal]:
        tokens = {t for p in self.posts if tick - p.tick <= self.window for t in p.tickers}
        # urutan harus deterministik: set string punya urutan acak antar-proses
        out = [s for s in (self.signal_for(t, tick, graph, naive) for t in sorted(tokens)) if s]
        out.sort(key=lambda s: -s.strength)
        return out[:n]


# --------------------------------------------------------------------------- #
# 5. Alpha engine
# --------------------------------------------------------------------------- #
@dataclass
class AlphaDecision:
    token: str
    symbol: str
    p_win: float
    ev_pct: float
    take_profit: float
    stop_loss: float
    required_tp: float
    upside_est: float
    size_pct: float
    approved: bool
    reasons: list[str] = field(default_factory=list)

    def public(self) -> dict:
        return {
            "symbol": self.symbol, "p_win": round(self.p_win, 3),
            "ev_pct": round(self.ev_pct * 100, 2), "tp": round(self.take_profit * 100, 1),
            "sl": round(self.stop_loss * 100, 1), "required_tp": round(self.required_tp * 100, 1),
            "upside": round(self.upside_est * 100, 1), "size_pct": round(self.size_pct * 100, 2),
            "approved": self.approved, "reasons": self.reasons,
        }


class AlphaEngine:
    """Mengubah fitur menjadi probabilitas, lalu keputusan.

    ``p̂`` adalah **model logistik** dengan bobot yang bisa dikalibrasi ulang dari
    jurnal (lihat ``fit_from_journal``): setiap trade dicatat, dan bobotnya
    diperbarui dengan gradient descent sederhana. Tanpa itu, p̂ cuma tebakan.
    """

    FEATURES = ("social", "coordination", "safety", "momentum", "regime", "liquidity")

    def __init__(
        self,
        *,
        weights: dict[str, float] | None = None,
        bias: float = -1.10,
        cost_round_trip: float = 0.040,
        min_p_win: float = 0.72,
        max_coordination: float = 0.45,
        min_ev_multiple: float = 2.0,
        max_size_pct: float = 0.05,
        stop_loss: float = 0.06,
        min_tp: float = 0.06,
        max_tp: float = 0.35,
        kelly_fraction: float = 0.25,
    ):
        self.w = dict(weights or {
            "social": 1.10, "coordination": -1.60, "safety": 0.90,
            "momentum": 0.50, "regime": 0.50, "liquidity": 0.30,
        })
        self.bias = bias
        self.cost = cost_round_trip
        self.min_p = min_p_win
        self.max_coordination = max_coordination
        self.min_ev_multiple = min_ev_multiple
        self.max_size = max_size_pct
        self.stop_loss = stop_loss
        self.min_tp = min_tp
        self.max_tp = max_tp
        self.kelly = kelly_fraction

    # ---------------------------------------------------------------- model
    def p_win(self, f: dict[str, float]) -> float:
        z = self.bias + sum(self.w.get(k, 0.0) * f.get(k, 0.0) for k in self.FEATURES)
        return 1.0 / (1.0 + math.exp(-max(-30.0, min(30.0, z))))

    def required_tp(self, p: float, s: float | None = None, c: float | None = None) -> float:
        """TP minimum agar EV > 0:  t > ((1−p)·s + c) / p."""
        s = self.stop_loss if s is None else s
        c = self.cost if c is None else c
        p = max(0.01, min(0.99, p))
        return ((1 - p) * s + c) / p

    def breakeven_hit_rate(self, t: float, s: float | None = None,
                           c: float | None = None) -> float:
        s = self.stop_loss if s is None else s
        c = self.cost if c is None else c
        return (s + c) / (t + s)

    def ev(self, p: float, t: float, s: float | None = None, c: float | None = None) -> float:
        s = self.stop_loss if s is None else s
        c = self.cost if c is None else c
        return p * (t - c) - (1 - p) * (s + c)

    def kelly_size(self, p: float, t: float, s: float | None = None,
                   c: float | None = None) -> float:
        s = self.stop_loss if s is None else s
        c = self.cost if c is None else c
        b = (t - c) / (s + c)
        if b <= 0:
            return 0.0
        f = (p * b - (1 - p)) / b
        return max(0.0, min(self.max_size, f * self.kelly))

    # -------------------------------------------------------------- keputusan
    def decide(
        self,
        *,
        token: str,
        symbol: str,
        social: float,
        coordination: float,
        safety: float,
        momentum: float,
        regime: float,
        liquidity: float,
        upside_est: float,
    ) -> AlphaDecision:
        f = {"social": social, "coordination": coordination, "safety": safety,
             "momentum": momentum, "regime": regime, "liquidity": liquidity}
        p = self.p_win(f)
        reasons: list[str] = []

        s_, c_ = self.stop_loss, self.cost
        required = self.required_tp(p)
        # target juga harus menghasilkan EV minimal, bukan cuma EV>0
        target_ev = c_ * self.min_ev_multiple
        tp_for_ev = (target_ev + (1 - p) * (s_ + c_)) / max(1e-6, p) + c_
        tp = max(self.min_tp, required * 1.15, tp_for_ev)
        feasible = tp <= self.max_tp
        tp = min(tp, self.max_tp)
        ev = self.ev(p, tp)
        size = self.kelly_size(p, tp)

        approved = True
        if coordination > self.max_coordination:
            approved = False
            reasons.append(f"koordinasi {coordination:.2f} > {self.max_coordination:.2f} (bot farm)")
        if p < self.min_p:
            approved = False
            reasons.append(f"p̂ {p:.2f} < {self.min_p:.2f}")
        if ev < self.cost * self.min_ev_multiple:
            approved = False
            reasons.append(f"EV {ev*100:.2f}% < {self.min_ev_multiple:g}× biaya")
        if upside_est * 0.7 < tp:
            approved = False
            reasons.append(f"upside realistis {upside_est*100:.0f}% < target {tp*100:.0f}%")
        if size * 100 < 0.1:
            approved = False
            reasons.append("ukuran Kelly terlalu kecil")
        if regime < 0.35:
            approved = False
            reasons.append("rezim pasar buruk")
        if not feasible:
            approved = False
            reasons.append("target yang dibutuhkan melebihi batas wajar")

        return AlphaDecision(
            token=token, symbol=symbol, p_win=p, ev_pct=ev, take_profit=tp,
            stop_loss=self.stop_loss, required_tp=required, upside_est=upside_est,
            size_pct=size if approved else 0.0, approved=approved, reasons=reasons,
        )

    # ------------------------------------------------------- kalibrasi online
    def fit_from_journal(self, rows: list[dict], lr: float = 0.08, epochs: int = 200) -> float:
        """Latih ulang bobot dari jurnal trade nyata (logistic regression).

        ``rows`` = [{"features": {...}, "won": bool}]. Mengembalikan log-loss
        akhir supaya kamu bisa memantau apakah model makin baik atau makin buruk.
        """
        if len(rows) < 30:
            return float("nan")
        for _ in range(epochs):
            grads = {k: 0.0 for k in self.FEATURES}
            gb = 0.0
            for r in rows:
                f = r["features"]
                y = 1.0 if r["won"] else 0.0
                p = self.p_win(f)
                err = p - y
                for k in self.FEATURES:
                    grads[k] += err * f.get(k, 0.0)
                gb += err
            n = len(rows)
            for k in self.FEATURES:
                self.w[k] -= lr * grads[k] / n
            self.bias -= lr * gb / n

        loss = 0.0
        for r in rows:
            p = min(1 - 1e-9, max(1e-9, self.p_win(r["features"])))
            y = 1.0 if r["won"] else 0.0
            loss -= y * math.log(p) + (1 - y) * math.log(1 - p)
        return loss / len(rows)
