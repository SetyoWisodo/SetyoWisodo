"""Test model harga biner di tools/polymarket_dual_wallet.py.

Yang diuji bukan "apakah strateginya untung" — tapi apakah modelnya jujur:
harga wajar harus 50% saat d=0, naik monoton terhadap d, dan strategi tanpa edge
harus menghasilkan EV ≈ −spread.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from polymarket_dual_wallet import HALF_SPREAD, fair_up, run  # noqa: E402


class TestFairValue(unittest.TestCase):
    def test_lima_puluh_persen_saat_seri(self):
        self.assertAlmostEqual(fair_up(0.0, 120.0), 0.5, places=6)

    def test_monoton_terhadap_jarak(self):
        vals = [fair_up(d, 120.0) for d in (-80, -40, -10, 0, 10, 40, 80)]
        self.assertEqual(vals, sorted(vals))

    def test_ujung_waktu_jadi_biner(self):
        self.assertAlmostEqual(fair_up(10.0, 0.0), 1.0, places=6)
        self.assertAlmostEqual(fair_up(-10.0, 0.0), 0.0, places=6)

    def test_up_dan_down_berjumlah_satu(self):
        for d in (-50, -5, 0, 5, 50):
            self.assertAlmostEqual(fair_up(d, 60.0) + (1 - fair_up(d, 60.0)), 1.0, places=9)


class TestDuaDompet(unittest.TestCase):
    def test_tanpa_aksi_rugi_sebesar_spread(self):
        r = run(3000, "hold", 0.0)
        biaya = 100 * (2 * HALF_SPREAD) / (2 * (0.5 + HALF_SPREAD))
        self.assertAlmostEqual(r["ev_pct"], -biaya, delta=0.3)
        self.assertEqual(r["win_rate"], 0.0)

    def test_cut_tidak_menghasilkan_profit(self):
        for level in (0.45, 0.35, 0.20):
            r = run(3000, "cut", level)
            self.assertLess(r["ev_pct"], 0.0, msg=f"cut {level} tidak boleh EV positif")
            self.assertGreater(r["win_rate"], 50.0)   # menang sering...
            self.assertGreater(r["loss_gt_30pct"], 10.0)  # ...tapi ada ekor besar

    def test_cut_level_rendah_menaikkan_win_rate_dan_ekor(self):
        rendah = run(3000, "cut", 0.20)
        tinggi = run(3000, "cut", 0.45)
        self.assertGreater(rendah["win_rate"], tinggi["win_rate"])
        self.assertLess(rendah["p05_pct"], tinggi["p05_pct"])

    def test_martingale_lebih_buruk(self):
        add = run(3000, "add", 0.35)
        cut = run(3000, "cut", 0.35)
        self.assertLess(add["ev_pct"], cut["ev_pct"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
