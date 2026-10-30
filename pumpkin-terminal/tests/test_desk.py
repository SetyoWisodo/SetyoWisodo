"""Test dasar Pumpkin Terminal — fokus pada aturan yang tidak boleh bocor.

    python -m unittest discover -s tests -v
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pumpkin.agents import Analyst, Filter, Guard, Sniper  # noqa: E402
from pumpkin.config import Config, FilterRules, RiskRules, SimConfig  # noqa: E402
from pumpkin.engine import Desk  # noqa: E402
from pumpkin.models import Position, Token  # noqa: E402
from pumpkin.report import render_markdown, build_report  # noqa: E402


def tok(**kw) -> Token:
    base = dict(
        address=kw.pop("address", "0xabc"), symbol="TEST", name="Test",
        price=1e-5, liquidity_usd=50_000, holders=500, top10_pct=20.0, dev_pct=2.0,
        mint_revoked=True, lp_locked=True, age_ticks=10,
    )
    base.update(kw)
    return Token(**base)


class TestFilter(unittest.TestCase):
    def setUp(self):
        self.f = Filter(FilterRules())

    def test_token_sehat_lolos(self):
        ok, reason = self.f.check(tok())
        self.assertTrue(ok, reason)

    def test_likuiditas_tipis_ditolak(self):
        ok, reason = self.f.check(tok(liquidity_usd=5_000))
        self.assertFalse(ok)
        self.assertEqual(reason, "likuiditas_tipis")

    def test_holder_sedikit_ditolak(self):
        self.assertFalse(self.f.check(tok(holders=10))[0])

    def test_distribusi_konsentrat_ditolak(self):
        self.assertEqual(self.f.check(tok(top10_pct=70))[1], "top10_terlalu_besar")

    def test_wallet_dev_besar_ditolak(self):
        self.assertEqual(self.f.check(tok(dev_pct=30))[1], "wallet_dev_besar")

    def test_mint_authority_aktif_ditolak(self):
        self.assertEqual(self.f.check(tok(mint_revoked=False))[1], "mint_authority_aktif")

    def test_lp_tidak_terkunci_ditolak(self):
        self.assertEqual(self.f.check(tok(lp_locked=False))[1], "lp_tidak_terkunci")

    def test_token_baru_ditunda(self):
        self.assertEqual(self.f.check(tok(age_ticks=0))[1], "terlalu_baru")


class TestAnalyst(unittest.TestCase):
    def test_skor_dalam_rentang(self):
        a = Analyst(0.6)
        for liq in (1_000, 50_000, 2_000_000):
            s = a.score(tok(liquidity_usd=liq))
            self.assertGreaterEqual(s, 0.0)
            self.assertLessEqual(s, 1.0)

    def test_token_berkualitas_lebih_tinggi(self):
        a = Analyst(0.6)
        bagus = a.score(tok(liquidity_usd=300_000, holders=5_000, top10_pct=8, dev_pct=0,
                            change_5_pct=6))
        jelek = a.score(tok(liquidity_usd=20_000, holders=230, top10_pct=31, dev_pct=7.9,
                            change_5_pct=-2))
        self.assertGreater(bagus, jelek)

    def test_penalti_sudah_terbang(self):
        a = Analyst(0.6)
        segar = a.score(tok(change_5_pct=8))
        telat = a.score(tok(change_5_pct=140))
        self.assertLess(telat, segar)

    def test_mode_null_tidak_memakai_sinyal(self):
        a = Analyst(0.6, edge_mode="null")
        s1 = a.score(tok(address="0x1", liquidity_usd=1_000_000))
        s2 = a.score(tok(address="0x2", liquidity_usd=1_000))
        self.assertGreaterEqual(min(s1, s2), 0.0)
        self.assertLessEqual(max(s1, s2), 1.0)


class TestSniper(unittest.TestCase):
    def test_maksimal_8_persen_saldo(self):
        s = Sniper(RiskRules())
        usd, _ = s.size(100.0, tok(liquidity_usd=100_000_000))
        self.assertAlmostEqual(usd, 8.0, places=2)

    def test_dibatasi_likuiditas(self):
        s = Sniper(RiskRules())
        usd, _ = s.size(100_000.0, tok(liquidity_usd=20_000))
        self.assertAlmostEqual(usd, 100.0, places=2)   # 0.5% dari 20k

    def test_tidak_melebihi_saldo(self):
        s = Sniper(RiskRules())
        usd, _ = s.size(10.0, tok(liquidity_usd=100_000_000))
        self.assertLessEqual(usd, 10.0)


class TestGuard(unittest.TestCase):
    def setUp(self):
        self.g = Guard(RiskRules())
        self.pos = Position(id=1, address="0xabc", symbol="T", qty=100.0,
                            entry_price=1.0, entry_tick=0, cost_usd=100.0, score=0.7,
                            peak_price=1.0, last_price=1.0)

    def test_stop_loss_minus_6_persen(self):
        t = tok(price=0.939)
        self.assertEqual(self.g.decide(self.pos, t, 5), "stop_loss")

    def test_belum_stop_di_minus_5_persen(self):
        t = tok(price=0.95)
        for _ in range(6):
            self.g.update(self.pos, t)
        self.assertIsNone(self.g.decide(self.pos, t, 5))

    def test_trailing_aktif_setelah_12_persen(self):
        self.g.update(self.pos, tok(price=1.15))
        self.assertGreaterEqual(self.pos.peak_gain_pct, 0.12)
        t = tok(price=1.05)          # turun 8.7% dari puncak
        self.g.update(self.pos, t)
        self.assertEqual(self.g.decide(self.pos, t, 7), "trailing_stop")

    def test_trailing_tidak_aktif_sebelum_12_persen(self):
        self.g.update(self.pos, tok(price=1.08))
        t = tok(price=1.00)
        self.g.update(self.pos, t)
        self.assertIsNone(self.g.decide(self.pos, t, 7))

    def test_batas_waktu(self):
        r = RiskRules()
        t = tok(price=1.0)
        self.assertEqual(self.g.decide(self.pos, t, r.max_hold_ticks + 1), "max_hold")


class TestDeskInvariants(unittest.TestCase):
    def _run(self, ticks=150, edge="correlated"):
        cfg = Config()
        cfg.sim = SimConfig(ticks=ticks, seed=3, edge_mode=edge, tokens_per_tick=5)
        d = Desk(cfg, run_dir=Path(tempfile.mkdtemp()))
        while not d.finished:
            d.tick()
        return d

    def test_selalu_selesai_dan_tidak_bangkrut(self):
        d = self._run()
        k = d.kpis()
        self.assertTrue(d.finished)
        self.assertGreaterEqual(k["cash"], 0.0)
        self.assertGreaterEqual(k["equity"], 0.0)

    def test_batas_posisi_terbuka(self):
        cfg = Config()
        cfg.sim = SimConfig(ticks=400, seed=5, tokens_per_tick=8)
        d = Desk(cfg, run_dir=Path(tempfile.mkdtemp()))
        while not d.finished:
            d.tick()
            self.assertLessEqual(len(d.positions), cfg.risk.max_concurrent)

    def test_tidak_pernah_beli_token_sama_dua_kali(self):
        d = self._run(ticks=500)
        addrs = [t.address for t in d.trades]
        self.assertEqual(len(addrs), len(set(addrs)))

    def test_tidak_ada_aset_laten_bocor_ke_laporan(self):
        d = self._run(ticks=200)
        blob = str(build_report(d))
        for bocor in ("archetype", "spike_tick", "rug_tick", "spike_size"):
            self.assertNotIn(bocor, blob)

    def test_laporan_markdown_memuat_disclaimer(self):
        d = self._run(ticks=200)
        md = render_markdown(build_report(d))
        self.assertIn("simulasi", md.lower())
        self.assertIn("bukan bukti", md.lower())


if __name__ == "__main__":
    unittest.main(verbosity=2)
