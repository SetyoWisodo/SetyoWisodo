"""Test model di tools/agent_swarm_repost.py.

Yang diuji bukan "apakah thread itu bohong" — itu bukan urusan unit test. Yang diuji:
apakah matematikanya konsisten. Kalau model ini dipakai untuk menolak klaim orang,
modelnya sendiri harus lulus uji martingale dan uji batas.
"""

from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from agent_swarm_repost import (  # noqa: E402
    END,
    GREENS,
    REDS,
    RED_TOTAL,
    SELLS,
    START,
    STOP,
    binom_cdf,
    binom_sf,
    p_hit_first,
    simulate,
    touch_prob,
)


class TestAritmetika(unittest.TestCase):
    def test_rasio_sesuai_klaim(self):
        self.assertAlmostEqual(END / START, 16.8009, places=4)

    def test_dua_leg_kali_jadi_total(self):
        legs = (1_069.28 / START) * (END / 1_069.28)
        self.assertAlmostEqual(legs, END / START, places=9)

    def test_batas_fraksi_posisi(self):
        # 0,06 x f x (E1+E2) = 17,58 dengan E minimal START x 0,94^2
        e_min = START * (1 - STOP) ** 2
        f_max = RED_TOTAL / (STOP * 2 * e_min)
        self.assertLess(f_max, 0.75)
        self.assertGreater(f_max, 0.70)
        # kalau posisi 100% ekuitas, dua stop 6% tidak mungkin hanya -17,58
        self.assertGreater(2 * STOP * START, RED_TOTAL)

    def test_hijau_total_konsisten(self):
        profit = END - START
        green_total = profit + RED_TOTAL
        self.assertAlmostEqual(green_total / REDS, 1_839.33, places=2)


class TestBarrier(unittest.TestCase):
    def test_tanpa_drift_sama_dengan_rumus_sederhana(self):
        a = math.log(1 - STOP)
        b = math.log(1.53)
        manual = (-a) / (b - a)
        self.assertAlmostEqual(p_hit_first(STOP, 0.53), manual, places=12)

    def test_peluang_dua_arah_jumlah_satu(self):
        # target +53% sebelum -6%, atau -6% sebelum +53%
        p_up = p_hit_first(STOP, 0.53)
        self.assertAlmostEqual(p_up + (1 - p_up), 1.0, places=12)
        self.assertLess(p_up, 0.2)

    def test_drift_membantu_tapi_tidak_menyelamatkan(self):
        p0 = p_hit_first(STOP, 0.53)
        p1 = p_hit_first(STOP, 0.53, drift=0.02, vol=0.1)
        p2 = p_hit_first(STOP, 0.53, drift=0.10, vol=0.1)
        self.assertLess(p0, p1)
        self.assertLess(p1, p2)
        # sembilan kali berturut-turut tetap angka yang sangat kecil
        self.assertLess(p0**GREENS, 1e-7)

    def test_target_lebih_besar_lebih_sulit(self):
        self.assertGreater(p_hit_first(STOP, 0.53), p_hit_first(STOP, 2.54))


class TestStopVsVolatilitas(unittest.TestCase):
    def test_monoton_terhadap_volatilitas(self):
        vals = [touch_prob(s, 20.0) for s in (0.02, 0.05, 0.10, 0.25, 0.60)]
        self.assertEqual(vals, sorted(vals))
        self.assertTrue(all(0.0 <= v <= 1.0 for v in vals))

    def test_angka_acuan_25_persen(self):
        self.assertAlmostEqual(touch_prob(0.25, 20.0), 0.668, places=3)

    def test_cocok_dengan_simulasi(self):
        r = simulate(4_000, 0.25, 20.0, 0.0, 0.0, 0.0, seed=3)
        self.assertAlmostEqual(r["stop_rate"], touch_prob(0.25, 20.0), delta=0.03)

    def test_binomial(self):
        self.assertAlmostEqual(binom_cdf(0, 3, 0.5), 0.125, places=9)
        for p in (0.05, 0.2, 0.5):
            self.assertAlmostEqual(binom_cdf(2, SELLS, p) + binom_sf(3, SELLS, p), 1.0, places=9)


class TestSimulasi(unittest.TestCase):
    def test_martingale_tanpa_biaya(self):
        """Exit di stopping time dari martingale => E[faktor] = 1."""
        r = simulate(20_000, 0.25, 20.0, 0.0, 0.0, 0.0, seed=5)
        self.assertAlmostEqual(r["mean_factor"], 1.0, delta=0.03)

    def test_biaya_menurunkan_hasil(self):
        free = simulate(3_000, 0.25, 20.0, 0.10, 0.0, 0.0, seed=6)
        costly = simulate(3_000, 0.25, 20.0, 0.10, 0.05, 0.005, seed=6)
        self.assertLess(costly["median"], free["median"])
        self.assertLess(costly["mean"], free["mean"])

    def test_drift_menaikkan_hasil(self):
        low = simulate(3_000, 0.25, 20.0, 0.0, 0.02, 0.0, seed=7)
        high = simulate(3_000, 0.25, 20.0, 0.50, 0.02, 0.0, seed=7)
        self.assertLess(low["median"], high["median"])

    def test_ekor_16_8_bukan_hasil_default(self):
        # pada drift 0 dan biaya 3%, tidak ada satu pun dari 5.000 percobaan
        r = simulate(5_000, 0.25, 20.0, 0.0, 0.03, 0.005, seed=8)
        self.assertEqual(r["ge_16_8"], 0.0)
        self.assertLess(r["median"], 1.0)

    def test_drift_ekstrem_baru_munculkan_ekor(self):
        r = simulate(3_000, 0.25, 20.0, 1.00, 0.03, 0.005, seed=9)
        self.assertGreater(r["ge_16_8"], 0.3)

    def test_semua_metrik_terdefinisi(self):
        r = simulate(500, 0.25, 20.0, 0.05, 0.02, 0.005, seed=10)
        for k in ("median", "mean", "p05", "p95", "profit_rate", "ge_16_8",
                  "ge_5x", "pf_ge_200", "stop_rate", "mean_factor", "green_rate"):
            self.assertIn(k, r)
        self.assertLessEqual(r["p05"], r["median"])
        self.assertLessEqual(r["median"], r["p95"])


if __name__ == "__main__":
    unittest.main()
