"""Test Whale Radar: forensics, reputasi whale, agregasi aliran, dan batas risiko."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pumpkin.config import ScalpRules  # noqa: E402
from pumpkin.forensics import DevLedger, Forensics  # noqa: E402
from pumpkin.whale_desk import WhaleDesk, build_whale_report, render_whale_markdown  # noqa: E402
from pumpkin.whale_market import MemeToken, WhaleTx  # noqa: E402
from pumpkin.whales import FlowAggregator, WhaleRegistry  # noqa: E402


def mk(**kw) -> MemeToken:
    base = dict(
        address="T1", symbol="TEST", name="Test", price=1e-5, p0=1e-5,
        liquidity_usd=30_000, holders=300, top10_pct=20.0, dev_pct=2.0,
        bundle_pct=2.0, mint_revoked=True, lp_locked=True, dev_address="D1",
    )
    base.update(kw)
    return MemeToken(**base)


class TestScalpMath(unittest.TestCase):
    def test_hit_rate_impas(self):
        r = ScalpRules()
        # menang = 50% - 6.5%, kalah = 20% + 6.5%
        # impas = rugi / (untung + rugi) = 0,145 / (0,435 + 0,145)
        self.assertAlmostEqual(r.breakeven_hit_rate, 0.145 / 0.58, places=6)
        self.assertGreater(r.breakeven_hit_rate, 0.20)

    def test_biaya_menaikkan_ambang(self):
        murah = ScalpRules(entry_fee_pct=0.0, exit_fee_pct=0.0,
                           entry_slippage_pct=0.0, exit_slippage_pct=0.0)
        self.assertAlmostEqual(murah.breakeven_hit_rate, 0.08 / 0.58, places=6)
        self.assertLess(murah.breakeven_hit_rate, ScalpRules().breakeven_hit_rate)


class TestForensics(unittest.TestCase):
    def test_token_bersih_risiko_rendah(self):
        f = Forensics()
        r = f.analyze(mk())
        self.assertLess(r.rug_risk, 0.42)
        self.assertTrue(r.safe)

    def test_token_berbahaya_risiko_tinggi(self):
        f = Forensics()
        r = f.analyze(mk(dev_pct=38, bundle_pct=48, top10_pct=75,
                         mint_revoked=False, lp_locked=False))
        self.assertGreater(r.rug_risk, 0.42)
        self.assertFalse(r.safe)
        self.assertTrue(any("dev" in x for x in r.findings))

    def test_riwayat_dev_dari_ledger(self):
        ledger = DevLedger()
        for _ in range(3):
            ledger.register("D9")
            ledger.mark_rug("D9")
        f = Forensics(ledger)
        r = f.analyze(mk(dev_address="D9"))
        self.assertEqual(r.dev_prior_rugs, 3)
        self.assertGreater(r.rug_risk, Forensics().analyze(mk(dev_address="DX")).rug_risk)

    def test_latency_terukur(self):
        f = Forensics()
        for _ in range(20):
            f.analyze(mk())
        st = f.latency_stats()
        self.assertEqual(st["n"], 20)
        self.assertGreater(st["p95"], 0.0)
        # "dalam hitungan detik" — bahkan jauh di bawah 1 detik
        self.assertLess(st["p95"], 50.0)


class TestWhaleRegistry(unittest.TestCase):
    def _tx(self, whale="W1", usd=5000.0, tick=1):
        return WhaleTx(tick=tick, whale=whale, label="Test", token="T1",
                       symbol="TEST", side="buy", usd=usd, price=1e-5)

    def test_reputasi_awal_setengah(self):
        r = WhaleRegistry()
        r.touch(self._tx())
        self.assertAlmostEqual(r.reputation("W1"), 0.5)

    def test_hit_menaikkan_reputasi(self):
        r = WhaleRegistry()
        r.touch(self._tx())
        for _ in range(3):
            r.mark("W1", True)
        self.assertGreater(r.reputation("W1"), 0.7)

    def test_miss_menurunkan_reputasi(self):
        r = WhaleRegistry()
        r.touch(self._tx())
        for _ in range(3):
            r.mark("W1", False)
        self.assertLess(r.reputation("W1"), 0.35)

    def test_leaderboard_urut(self):
        r = WhaleRegistry()
        for w, hits in (("W1", 4), ("W2", 0), ("W3", 2)):
            r.touch(self._tx(whale=w))
            for _ in range(hits):
                r.mark(w, True)
            r.mark(w, False)
        lb = r.leaderboard(3)
        self.assertEqual(lb[0]["address"], "W1")


class TestFlowAggregator(unittest.TestCase):
    def _buy(self, whale, usd, tick=1, token="T1"):
        return WhaleTx(tick=tick, whale=whale, label="x", token=token,
                       symbol="TEST", side="buy", usd=usd, price=1e-5)

    def test_tanpa_aliran_tanpa_sinyal(self):
        a, r = FlowAggregator(), WhaleRegistry()
        self.assertIsNone(a.signal_for("T1", 1, r))

    def test_lebih_banyak_whale_sinyal_lebih_kuat(self):
        a, r = FlowAggregator(window_ticks=6), WhaleRegistry()
        for w in ("W1", "W2", "W3"):
            tx = self._buy(w, 20_000)
            r.touch(tx)
            a.ingest(tx)
        kuat = a.signal_for("T1", 2, r).signal

        b, r2 = FlowAggregator(window_ticks=6), WhaleRegistry()
        tx = self._buy("W9", 20_000)
        r2.touch(tx)
        b.ingest(tx)
        lemah = b.signal_for("T1", 2, r2).signal
        self.assertGreater(kuat, lemah)

    def test_besar_dana_menaikkan_sinyal(self):
        r = WhaleRegistry()
        a = FlowAggregator(window_ticks=6)
        kecil, besar = FlowAggregator(window_ticks=6), FlowAggregator(window_ticks=6)
        tx1 = self._buy("W1", 2_000); tx2 = self._buy("W1", 200_000)
        r.touch(tx1); kecil.ingest(tx1)
        r.touch(tx2); besar.ingest(tx2)
        self.assertGreater(besar.signal_for("T1", 1, r).signal,
                           kecil.signal_for("T1", 2, r).signal)

    def test_prune_membuang_jendela_lama(self):
        a, r = FlowAggregator(window_ticks=3), WhaleRegistry()
        tx = self._buy("W1", 50_000, tick=1)
        r.touch(tx); a.ingest(tx)
        a.prune(10)
        self.assertIsNone(a.signal_for("T1", 10, r))

    def test_sell_tidak_menambah_sinyal(self):
        a, r = FlowAggregator(), WhaleRegistry()
        a.ingest(WhaleTx(tick=1, whale="W1", label="x", token="T1", symbol="TEST",
                         side="sell", usd=99_999, price=1e-5))
        self.assertIsNone(a.signal_for("T1", 1, r))


class TestWhaleDeskInvariants(unittest.TestCase):
    def _run(self, ticks=260, mode="informed", seed=4):
        from pumpkin.config import WhaleSimConfig
        d = WhaleDesk(WhaleSimConfig(ticks=ticks, seed=seed, edge_mode=mode),
                      run_dir=Path(tempfile.mkdtemp()))
        while not d.finished:
            d.tick()
        return d

    def test_selesai_semua_posisi_ditutup(self):
        d = self._run()
        self.assertTrue(d.finished)
        self.assertEqual(len(d.positions), 0)
        self.assertEqual(sum(1 for t in d.trades if t.reason == "session_end"),
                         sum(1 for t in d.trades if t.reason == "session_end"))

    def test_ukuran_posisi_maks_5_persen(self):
        d = self._run(ticks=200)
        for t in d.trades:
            self.assertLessEqual(t.size_usd, d.start_balance * 0.05 * 3 + 1e-6)

    def test_satu_token_satu_kali(self):
        d = self._run(ticks=300)
        addrs = [t.address for t in d.trades]
        self.assertEqual(len(addrs), len(set(addrs)))

    def test_ekuitas_tidak_negatif(self):
        d = self._run()
        self.assertGreaterEqual(d.kpis()["equity"], 0.0)
        self.assertGreaterEqual(d.kpis()["cash"], -1e-9)

    def test_tidak_ada_data_laten_bocor(self):
        d = self._run(ticks=200)
        blob = str(build_whale_report(d))
        for bocor in ("is_rug", "quality", "cap_mult", "pump_rate", "rug_at"):
            self.assertNotIn(bocor, blob)

    def test_laporan_memuat_hit_rate_impas(self):
        d = self._run(ticks=200)
        md = render_whale_markdown(build_whale_report(d))
        self.assertIn("Hit rate impas", md)
        self.assertIn("Simulasi", md)


if __name__ == "__main__":
    unittest.main(verbosity=2)
