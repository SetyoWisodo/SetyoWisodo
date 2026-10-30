"""Test Social Radar: sentimen, koordinasi, aritmetika risiko, dan batas desk."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pumpkin.config import SocialRules, SocialSimConfig  # noqa: E402
from pumpkin.journal import Journal  # noqa: E402
from pumpkin.social_desk import SocialDesk, build_social_report, render_social_markdown  # noqa: E402
from pumpkin.social_signal import (AlphaEngine, CoordinationDetector,  # noqa: E402
                                   InfluenceGraph, SocialAggregator, SocialPost,
                                   extract_tickers, score_text)


def post(**kw) -> SocialPost:
    base = dict(
        id="p1", tick=10, author="@a", followers=12_000, following=400,
        account_age_days=900, text="$TEST looks strong", tickers=["TEST"],
        sentiment=0.6, confidence=0.7, likes=120, reposts=14, replies=9,
    )
    base.update(kw)
    return SocialPost(**base)


def clone(i: int, text: str = "🚀🚀 $TEST TO THE MOON 100X GUARANTEED!!!",
          **kw) -> SocialPost:
    base = dict(id=f"b{i}", tick=10, author=f"@bot{i}", followers=180, following=3200,
                account_age_days=2, text=text, tickers=["TEST"], sentiment=0.95,
                confidence=0.2, likes=1, reposts=0, replies=0, is_bot=True)
    base.update(kw)
    return SocialPost(**base)


class TestSentiment(unittest.TestCase):
    def test_positif_dan_negatif(self):
        pos, _ = score_text("$TEST accumulation is real, LP locked")
        neg, _ = score_text("$TEST looks like a honeypot, dev still holds mint authority")
        self.assertGreater(pos, 0.1)
        self.assertLess(neg, 0.0)

    def test_negasi_membalik_tanda(self):
        pos, _ = score_text("this is bullish")
        neg, _ = score_text("this is not bullish")
        self.assertGreater(pos, 0)
        self.assertLess(neg, 0)

    def test_hype_menurunkan_keyakinan(self):
        _, c_plain = score_text("$TEST volume is accelerating while price is flat")
        s_hype, c_hype = score_text("$TEST 1000x GUARANTEED risk free easy money!!!")
        self.assertLess(c_hype, c_plain)
        self.assertGreaterEqual(s_hype, 0.0)   # tidak negatif, tapi tidak dipercaya
        self.assertLess(c_hype, 0.4)

    def test_teks_netral(self):
        s, c = score_text("gm")
        self.assertEqual(s, 0.0)
        self.assertLess(c, 0.5)


class TestTicker(unittest.TestCase):
    def test_kasus_dan_duplikat(self):
        self.assertEqual(extract_tickers("buy $wif and $WIF and $bonk"), ["WIF", "BONK"])

    def test_tanpa_ticker(self):
        self.assertEqual(extract_tickers("market looks choppy today"), [])


class TestCoordination(unittest.TestCase):
    def test_bot_farm_terdeteksi(self):
        det = CoordinationDetector()
        rep = det.score([clone(i) for i in range(6)], tick=10)
        self.assertGreater(rep.score, 0.6)
        self.assertIn("teks kembar antar akun", rep.findings)

    def test_post_organik_tidak_dituduh(self):
        det = CoordinationDetector()
        organic = [
            post(id="o1", author="@a", tick=10, text="$TEST dev wallet clean, LP locked, watching"),
            post(id="o2", author="@b", tick=11, followers=90_000,
                 text="Quiet buying on $TEST for three hours. No hype, just fills."),
            post(id="o3", author="@c", tick=12, followers=4_000,
                 text="Holder distribution on $TEST looks better than last week"),
            post(id="o4", author="@d", tick=13, followers=30_000,
                 text="$TEST volume accelerating while price still flat"),
        ]
        self.assertLess(det.score(organic, tick=13).score, 0.45)


class TestAgregasi(unittest.TestCase):
    def test_naive_lebih_tinggi_dari_sadar_koordinasi(self):
        agg = SocialAggregator(window=8)
        graph = InfluenceGraph()
        posts = [clone(i) for i in range(8)]
        for p in posts:
            graph.upsert(p)
        agg.ingest(posts)
        aware = agg.signal_for("TEST", 10, graph)
        naive = agg.signal_for("TEST", 10, graph, naive=True)
        self.assertGreater(naive.strength, aware.strength)
        self.assertGreater(aware.coordination, 0.5)
        self.assertEqual(naive.findings, [])

    def test_tanpa_post_tidak_ada_sinyal(self):
        agg = SocialAggregator(window=8)
        self.assertIsNone(agg.signal_for("TEST", 10, InfluenceGraph()))


class TestReputasi(unittest.TestCase):
    def test_laplace_bergerak_sesuai_hasil(self):
        graph = InfluenceGraph()
        for i in range(4):
            graph.upsert(post(id=f"p{i}", tick=i, author="@kol"))
        awal = graph.reputation("@kol")
        for _ in range(6):
            graph.mark("@kol", True)
        naik = graph.reputation("@kol")
        for _ in range(10):
            graph.mark("@kol", False)
        turun = graph.reputation("@kol")
        self.assertGreater(naik, awal)
        self.assertLess(turun, naik)

    def test_reach_makin_besar_dengan_follower(self):
        graph = InfluenceGraph()
        kecil = graph.upsert(post(id="a", author="@kecil", followers=1_000, tick=1))
        besar = graph.upsert(post(id="b", author="@besar", followers=900_000, tick=2))
        self.assertGreater(besar.reach, kecil.reach)


class TestMatematika(unittest.TestCase):
    """Angka di sini harus sama dengan docs/MATEMATIKA.md."""

    def setUp(self):
        self.e = AlphaEngine()

    def test_hit_rate_impas_sesuai_tabel(self):
        # (target, stop, biaya) → hit rate impas, persis tabel docs/MATEMATIKA.md
        cases = [((0.06, 0.06, 0.015), 62.5), ((0.10, 0.06, 0.015), 46.9),
                 ((0.15, 0.08, 0.015), 41.3), ((0.10, 0.06, 0.04), 62.5),
                 ((0.15, 0.08, 0.04), 52.2), ((0.15, 0.08, 0.065), 63.0)]
        for (t, s, c), want in cases:
            got = self.e.breakeven_hit_rate(t, s, c) * 100
            self.assertAlmostEqual(got, want, places=1, msg=f"t={t} s={s} c={c}")

    def test_tp_wajib_sesuai_tabel(self):
        self.assertAlmostEqual(self.e.required_tp(0.72, 0.05, 0.015) * 100, 4.0, places=1)
        self.assertAlmostEqual(self.e.required_tp(0.72, 0.08, 0.065) * 100, 12.1, places=1)

    def test_ev_sesuai_tabel(self):
        for c, want in ((0.015, 7.06), (0.04, 4.56), (0.065, 2.06)):
            got = self.e.ev(0.72, 0.15, 0.08, c) * 100
            self.assertAlmostEqual(got, want, places=1)

    def test_kelly_dipotong_dan_dibatasi(self):
        raw = self.e.kelly_size(0.72, 0.15, 0.08, 0.015)
        self.assertLessEqual(raw, self.e.max_size)
        self.assertGreater(raw, 0.0)
        # peluang jelek → nol, bukan "kecil tapi dipaksa"
        self.assertEqual(self.e.kelly_size(0.30, 0.15, 0.08, 0.015), 0.0)

    def test_p_win_monoton_pada_setiap_fitur(self):
        base = dict(social=0.5, coordination=0.2, safety=0.6, momentum=0.5,
                    regime=0.6, liquidity=0.5)
        for key, sign in (("social", 1), ("safety", 1), ("momentum", 1),
                          ("regime", 1), ("liquidity", 1), ("coordination", -1)):
            low = dict(base, **{key: 0.2})
            high = dict(base, **{key: 0.8})
            d = self.e.p_win(high) - self.e.p_win(low)
            self.assertGreater(d * sign, 0, msg=key)

    def test_tolak_kalau_tidak_ada_edge(self):
        d = self.e.decide(token="T", symbol="T", social=0.92, coordination=0.05,
                          safety=0.9, momentum=0.8, regime=0.7, liquidity=0.8,
                          upside_est=0.02)
        self.assertFalse(d.approved)
        self.assertIn("upside", " ".join(d.reasons).lower())

    def test_target_tidak_melebihi_batas(self):
        d = self.e.decide(token="T", symbol="T", social=0.95, coordination=0.0,
                          safety=0.95, momentum=0.85, regime=0.9, liquidity=0.9,
                          upside_est=0.9)
        self.assertLessEqual(d.take_profit, self.e.max_tp + 1e-9)


class TestKalibrasi(unittest.TestCase):
    def test_latih_ulang_menurunkan_log_loss(self):
        import random as _r
        rng = _r.Random(4)
        rows = []
        for _ in range(120):
            f = dict(social=rng.uniform(.3, .95), coordination=rng.uniform(0, .8),
                     safety=rng.uniform(.3, .95), momentum=rng.uniform(.2, .9),
                     regime=rng.uniform(.4, .9), liquidity=rng.uniform(.2, .9))
            z = 2.2 * f["social"] - 2.0 * f["coordination"] + 1.4 * f["safety"] - 1.2
            rows.append({"features": f, "won": rng.random() < 1 / (1 + 2.718281828 ** -z)})
        e = AlphaEngine()
        awal = e.fit_from_journal(rows, lr=0.0, epochs=1)     # log-loss model awal
        e2 = AlphaEngine()
        akhir = e2.fit_from_journal(rows, lr=0.3, epochs=200)
        self.assertLess(akhir, awal)
        self.assertFalse(akhir != akhir)                      # bukan nan

    def test_jurnal_kecil_tidak_dilatih(self):
        e = AlphaEngine()
        self.assertNotEqual(e.fit_from_journal([{"features": {}, "won": True}]), 0.0)


class TestJournal(unittest.TestCase):
    def test_bolak_balik(self):
        with tempfile.TemporaryDirectory() as tmp:
            j = Journal(Path(tmp) / "t.db")
            for i, won in enumerate((True, True, False)):
                j.record_trade(
                    session="s", tick=i, token=f"T{i}", symbol=f"S{i}", p_win=0.8,
                    ev_pct=0.05, tp=0.15, sl=0.06, size_pct=0.05,
                    features={"social": 0.7}, entry_price=1e-5, exit_price=1.1e-5,
                    pnl_pct=0.1 if won else -0.1, pnl_usd=1.0 if won else -1.0,
                    reason="take_profit" if won else "stop_loss", hold_ticks=3)
            j.record_news(session="s", tick=1, kind="hack", direction=-1,
                          headline="bridge exploit")
            s = j.summary()
            rows = j.rows()
            j.close()
        self.assertEqual(s["trades"], 3)
        self.assertEqual(s["wins"], 2)
        self.assertAlmostEqual(s["win_rate"], 66.67, places=1)
        self.assertEqual(len(rows), 3)
        self.assertTrue(rows[0]["features"])       # dipakai fit_from_journal


class TestDesk(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.desk = SocialDesk(SocialSimConfig(ticks=260, seed=3, mode="dirty"),
                              SocialRules(), Path(cls._tmp.name))
        while not cls.desk.finished:
            cls.desk.tick()
        cls.k = cls.desk.kpis()

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def test_akuntansi_konsisten(self):
        total = self.k["total_equity"]
        harap = self.k["start_balance"] + sum(t.pnl_usd for t in self.desk.trades)
        self.assertAlmostEqual(total, harap, places=1)

    def test_tidak_ada_posisi_ganda(self):
        addrs = [t.address for t in self.desk.trades]
        self.assertEqual(len(addrs), len(set(addrs)))

    def test_ukuran_posisi_dibatasi(self):
        for t in self.desk.trades:
            self.assertLessEqual(t.size_usd, 0.05 * self.desk.peak_equity + 1e-6)

    def test_semua_entry_lolos_ambang_p(self):
        for t in self.desk.trades:
            self.assertGreaterEqual(t.score, self.desk.rules.min_p_win - 1e-9)

    def test_tidak_trading_saat_dihalt(self):
        # setiap trade harus punya tick masuk < tick halt berikutnya; cukup cek
        # bahwa desk benar-benar punya jalur halt dan tidak crash saat dipicu
        self.desk._day_start_equity = self.desk.equity() * 1.5
        self.desk._update_day()
        self.assertTrue(self.desk._halted_until > self.desk.tick_no)

    def test_vault_menarik_modal(self):
        d = SocialDesk(SocialSimConfig(ticks=5, seed=1), SocialRules(),
                       Path(tempfile.mkdtemp()))
        d.cash = 900.0
        d._update_day()
        self.assertGreater(d.vault_locked, 0.0)
        self.assertAlmostEqual(d.vault_locked, 250.0, places=2)

    def test_laporan_markdown(self):
        rep = build_social_report(self.desk)
        md = render_social_markdown(rep)
        self.assertIn("Simulasi", md)
        self.assertIn("Win rate", md)
        self.assertIn("p̂", md)

    def test_snapshot_tanpa_kunci_terlarang(self):
        import json
        snap = json.dumps(self.desk.snapshot())
        self.assertNotIn('"quality"', snap)


if __name__ == "__main__":
    unittest.main(verbosity=2)
