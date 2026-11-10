#!/usr/bin/env python3
"""Bedah klaim: "4 repo GitHub ditempel ke Grok bot, $231,70 jadi $3.892,78 (16,8x) dalam 8j38m".

Yang bisa diuji dari thread itu cuma dua hal:

1. **Aritmetika internal.** $3.892,78 / $231,70 = 16,80x (benar). Tapi 11 sell,
   9 hijau, 2 merah, total merah −$17,58, stop −6% di setiap beli. Dari tiga angka
   itu posisi (fraksi ekuitas) bisa dihitung mundur — dan hasilnya memaksa
   kesimpulan yang tidak nyaman.
2. **Apakah urutan hasil itu mungkin terjadi.** Stop −6% pada trade yang berakhir
   +50% ke atas berarti harga **tidak pernah** mundur 6% lebih dulu. Untuk
   random walk tanpa drift, peluangnya bisa dihitung persis (barrier/martingale),
   tidak perlu opini.

Model di file ini sengaja dibuat **netral dan terbuka**:

* Harga: geometric random walk, log-vol `sigma` per jam, horizon tiap trade `hold`
  menit, drift opsional (supaya "skill" tidak otomatis dianggap nol).
* Stop: level −6% dibanding harga beli, monitoring kontinu, exit tepat di barrier
  dikurangi `slip` (bukan exit di harga yang lebih bagus).
* Biaya: `cost` per round trip (fee platform 0,5%/sisi = 1,0% + impact).
* Ukuran posisi: seluruh ekuitas per trade (paling **menguntungkan** untuk klaim:
  compounding maksimal), 11 trade per percobaan.

Karena exit di stopping time dari martingale, **E[faktor per trade] = 1** saat
drift = 0 dan biaya = 0. Artinya model ini tidak "dibuat supaya rugi": tanpa
biaya, rata-ratanya impas. Yang membuat rugi adalah biaya, dan yang membuat
16,8x adalah ekor distribusi — bukan metode.

Jalankan:
    python tools/agent_swarm_repost.py                 # semua bagian
    python tools/agent_swarm_repost.py --mode stops    # stop vs winner
    python tools/agent_swarm_repost.py --mode swarm --attempts 60000
"""

from __future__ import annotations

import argparse
import math
import random
from statistics import NormalDist

N = NormalDist()

# ---- angka dari thread (dikutip apa adanya) ----
START = 231.70
MID = 1_069.28
END = 3_892.78
SELLS = 11
GREENS = 9
REDS = 2
RED_TOTAL = 17.58          # total kerugian dua trade merah
BEST_WIN = 1_049.96        # "best sell: +$1.049,96 at 3:50am"
STOP = 0.06                # "-6% stop under every buy"
HOURS = 8 + 38 / 60        # 8 jam 38 menit

# ---- asumsi biaya (Fomo: 0,5% per sisi; impact di memecoin tipis) ----
FEE_ROUND_TRIP = 0.010     # 0,5% beli + 0,5% jual
IMPACT_ROUND_TRIP = 0.020  # konservatif untuk pool tipis; bisa 5-20% saat exit besar
SLIP_STOP = 0.005          # stop tidak kena tepat di -6%


# ---------------------------------------------------------------- barrier math
def touch_prob(sigma_hour: float, hold_min: float, stop: float = STOP) -> float:
    """P(harga menyentuh stop) selama holding, random walk tanpa drift.

    Untuk log-price Brownian tanpa drift, P(min <= a) = 2 * Phi(a / (sigma*sqrt(T)))
    dengan a = ln(1 - stop) < 0.
    """
    if sigma_hour <= 0:
        return 1.0
    a = math.log(1.0 - stop)
    s = sigma_hour * math.sqrt(hold_min / 60.0)
    return min(1.0, 2.0 * N.cdf(a / s))


def p_hit_first(stop: float, target: float, drift: float = 0.0, vol: float = 1.0) -> float:
    """P(kena target +target dulu, sebelum stop -stop). Drift = log-drift per periode.

    Formula standar BM dengan drift:
        P(hit b before a) = (1 - e^(-2*mu*a/v^2)) / (e^(2*mu*b/v^2) - e^(-2*mu*a/v^2))
    dengan a = ln(1-stop) < 0 < b = ln(1+target). mu = 0 -> |a| / (b + |a|).
    """
    a = math.log(1.0 - stop)
    b = math.log(1.0 + target)
    if abs(drift) < 1e-12:
        return (-a) / (b - a)
    k = 2.0 * drift / (vol * vol)
    ea = math.exp(-k * a)      # > 1 karena a < 0
    eb = math.exp(-k * b)      # < 1 karena b > 0
    # u(0) = (1 - e^(-k a)) / (e^(-k b) - e^(-k a)); keduanya negatif -> positif
    return (1.0 - ea) / (eb - ea)


def binom_sf(k: int, n: int, p: float) -> float:
    """P(X >= k) untuk X ~ Binomial(n, p)."""
    return sum(math.comb(n, i) * p**i * (1 - p) ** (n - i) for i in range(k, n + 1))


def binom_cdf(k: int, n: int, p: float) -> float:
    """P(X <= k) untuk X ~ Binomial(n, p)."""
    if p <= 0.0:
        return 1.0
    if p >= 1.0:
        return 0.0 if k < n else 1.0
    return sum(math.comb(n, i) * p**i * (1 - p) ** (n - i) for i in range(0, k + 1))


# ---------------------------------------------------------------- simulasi
def simulate(attempts: int, sigma_hour: float = 0.25, hold_min: float = 20.0,
             drift_hour: float = 0.0, cost: float = 0.0, slip: float = 0.0,
             seed: int = 7) -> dict:
    """11 trade per percobaan, seluruh ekuitas per trade, stop -6%.

    Mengembalikan statistik distribusi multiple akhir, bukan satu angka.
    """
    rng = random.Random(seed)
    T = hold_min / 60.0
    vol = sigma_hour * math.sqrt(T)
    var = vol * vol
    a = math.log(1.0 - STOP)
    keep = 1.0 - cost
    mults: list[float] = []
    pfs: list[float] = []
    stops_total = 0
    factor_sum = 0.0
    green_trades = 0
    for _ in range(attempts):
        eq = 1.0
        win = 0.0
        loss = 0.0
        for _ in range(SELLS):
            x = drift_hour * T + vol * rng.gauss(0.0, 1.0)
            if x <= a:
                f = 1.0 - STOP - slip
                stops_total += 1
            else:
                p = math.exp(-2.0 * a * (a - x) / var)
                if rng.random() < p:
                    f = 1.0 - STOP - slip
                    stops_total += 1
                else:
                    f = math.exp(x)
            f *= keep
            factor_sum += f
            if f > 1.0:
                green_trades += 1
            eq *= f
            if f > 1.0:
                win += f - 1.0
            else:
                loss += 1.0 - f
        mults.append(eq)
        pfs.append(win / loss if loss > 0 else math.inf)
    out = _summarise(mults, pfs, stops_total / (attempts * SELLS))
    out["mean_factor"] = factor_sum / (attempts * SELLS)
    out["green_rate"] = green_trades / (attempts * SELLS)
    return out


def _quant(vals: list[float], q: float) -> float:
    s = sorted(vals)
    i = min(len(s) - 1, max(0, int(round(q * (len(s) - 1)))))
    return s[i]


def _summarise(mults: list[float], pfs: list[float], stop_rate: float) -> dict:
    n = len(mults)
    return {
        "n": n,
        "median": _quant(mults, 0.50),
        "mean": sum(mults) / n,
        "p05": _quant(mults, 0.05),
        "p95": _quant(mults, 0.95),
        "profit_rate": sum(1 for m in mults if m > 1.0) / n,
        "ge_16_8": sum(1 for m in mults if m >= END / START) / n,
        "ge_5x": sum(1 for m in mults if m >= 5.0) / n,
        "pf_ge_200": sum(1 for p in pfs if p >= 200.0) / n,
        "stop_rate": stop_rate,
    }


def p_reach(mults: list[float], target: float) -> float:
    return sum(1 for m in mults if m >= target) / len(mults)


# ---------------------------------------------------------------- bagian-bagian
def section_consistency() -> None:
    """Aritmetika internal thread — tidak butuh model, hanya aljabar."""
    ratio = END / START
    leg1 = MID / START
    leg2 = END / MID
    profit = END - START
    green_total = profit + RED_TOTAL
    pf = green_total / RED_TOTAL
    avg_green = green_total / GREENS
    avg_red = RED_TOTAL / REDS
    implied_equity = avg_red / STOP       # kalau posisi = 100% ekuitas

    print("=" * 78)
    print("1. ARITMETIKA INTERNAL")
    print("=" * 78)
    print(f"  {END:,.2f} / {START:,.2f}            = {ratio:.4f}x  (klaim 16,80x: {'cocok' if abs(ratio-16.8)<0.01 else 'TIDAK'})")
    print(f"  leg 1  {START:,.2f} -> {MID:,.2f}   = {leg1:.3f}x  (+{(leg1-1)*100:.0f}%)")
    print(f"  leg 2  {MID:,.2f} -> {END:,.2f}  = {leg2:.3f}x  (+{(leg2-1)*100:.0f}%)")
    print(f"  total profit            = ${profit:,.2f}")
    print(f"  total hijau (9)          = ${green_total:,.2f}  (rata-rata ${avg_green:,.2f})")
    print(f"  total merah (2)          = ${RED_TOTAL:,.2f}  (rata-rata ${avg_red:,.2f})")
    print(f"  profit factor            = {pf:,.1f}x  (hijau/merah)")
    print(f"  avg win / avg loss       = {avg_green/avg_red:,.1f} R  (1R = 6% stop)")
    print()
    print("  Konsekuensi 1 — ukuran posisi dipaksa kecil:")
    print(f"    kalau stop = 6% dan posisi = 100% ekuitas, tiap merah = 6% x ekuitas.")
    print(f"    rata-rata ${avg_red:,.2f} per merah  =>  ekuitas saat itu = ${implied_equity:,.2f}")
    print(f"    Padahal ekuitas mulai ${START:,.2f} dan tidak pernah turun (total merah cuma $17,58).")
    print(f"    => posisi BUKAN 100% ekuitas. Batas atas fraksi f:")
    # 0.06*f*(E1+E2) = 17.58 ; E1,E2 >= START*(1-0.06)^2 (worst case penuh)
    e_min = START * (1 - STOP) ** 2
    f_max = RED_TOTAL / (STOP * 2 * e_min)
    print(f"       0,06 x f x (E1+E2) = 17,58 dengan E >= ${e_min:,.2f}")
    print(f"       => f <= {f_max:.2%} dari ekuitas per trade")
    print()
    print("  Konsekuensi 2 — pemenang dipaksa besar:")
    for f in (f_max, 0.30, 0.15, 1.0):
        if f > f_max:
            continue
        # (1 + f*(g-1))^9 * (1-0.06f)^2 = 16.8008
        need = (ratio / (1 - STOP * f) ** 2) ** (1.0 / GREENS)
        g = 1.0 + (need - 1.0) / f
        print(f"    f = {f:5.1%}  =>  rata-rata pemenang harus {g:5.2f}x  (+{(g-1)*100:6.0f}%) per trade")
    print()
    print("  Konsekuensi 3 — harga dari 'rata-rata pemenang +254%':")
    print("    Untuk menang +254% dengan stop -6%, harga harus naik 3,5x TANPA")
    print("    pernah mundur 6%. Di random walk tanpa drift peluangnya:")
    for g in (0.53, 1.0, 2.54):
        p = p_hit_first(STOP, g)
        print(f"      target +{g*100:5.0f}% : P(kena target dulu) = {p:6.2%}  => 9 kali berturut = {p**GREENS:.2e}")
    print()


def section_stops(hold_min: float = 20.0) -> None:
    """Stop -6% vs volatilitas: berapa merah yang WAJAR, dan sisa peluang '2 merah'."""
    print("=" * 78)
    print(f"2. STOP -6% vs VOLATILITAS MEMECOIN (holding {hold_min:.0f} menit)")
    print("=" * 78)
    print("  P(sentuh -6%) = 2*Phi(ln(0,94)/(sigma*sqrt(T)))   [random walk, no drift]")
    print()
    print("  sigma/jam | P(sentuh -6%) | harapan merah dari 11 | P(<=2 merah) | P(0 merah)")
    print("  ----------+---------------+-----------------------+--------------+----------")
    for sig in (0.02, 0.05, 0.10, 0.15, 0.25, 0.40, 0.60):
        p = touch_prob(sig, hold_min)
        print(f"    {sig*100:5.0f}%  |    {p:6.1%}     |        {p*SELLS:5.2f}        |"
              f"   {binom_cdf(2, SELLS, p):8.2%}   |  {(1-p)**SELLS:7.2%}")
    print()
    print("  Membalik pertanyaannya: kalau 2 dari 11 memang wajar (P=50%),")
    p_target = 0.5
    # cari p dengan binom_cdf(2,11,p) = 0.5
    lo, hi = 0.0, 1.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if binom_cdf(2, SELLS, mid) > p_target:
            lo = mid
        else:
            hi = mid
    p = (lo + hi) / 2
    # balik ke sigma: p = 2*Phi(a/(sigma*sqrt(T))) => sigma
    a = math.log(1 - STOP)
    z = N.inv_cdf(p / 2)
    sig = (a / z) / math.sqrt(hold_min / 60.0)
    print(f"    maka P(sentuh) harus {p:.1%}  =>  sigma <= {sig*100:.1f}% per jam.")
    b = math.log(1.53)
    zt = -b / (sig * math.sqrt(hold_min / 60.0))
    print(f"  Pada sigma itu, peluang satu trade naik +53% dalam {hold_min:.0f} menit:")
    print(f"    z = ln(1,53)/sigma_20m = {zt:.1f}  =>  P ~ 2*Phi(z) = {2*N.cdf(zt):.1e}  (praktis nol).")
    print(f"  Memecoin yang naik 3-5x dalam satu sesi tidak punya sigma {sig*100:.0f}%/jam.")
    print("  Jadi '9 hijau dengan stop 6%' dan '16,8x' saling mengunci: yang satu")
    print("  butuh koin tenang, yang lain butuh koin gila.")
    print()


def section_swarm(attempts: int) -> None:
    """Distribusi hasil 11 trade, beberapa level drift."""
    print("=" * 78)
    print("3. DISTRIBUSI 11 TRADE (posisi = 100% ekuitas, stop -6%, fee 1% + impact 2%)")
    print("=" * 78)
    print(f"  {attempts:,} percobaan x 11 trade; sigma 25%/jam; holding 20 menit")
    print("  drift = log-drift per jam (50% = harga x1,65 tiap jam; 100% = x2,72 tiap jam)")
    print()
    hdr = ("  drift/jam | median |  rata2  |  P05   |  P95   | untung | hijau/trade | >=16,8x | 1 dari N  | stop rate")
    print(hdr)
    print("  ----------+--------+---------+--------+--------+--------+-------------+---------+-----------+----------")
    rows = []
    for drift in (0.0, 0.05, 0.20, 0.50, 1.00):
        r = simulate(attempts, 0.25, 20.0, drift, FEE_ROUND_TRIP + IMPACT_ROUND_TRIP, SLIP_STOP, seed=11)
        n = 1 / r["ge_16_8"] if r["ge_16_8"] > 0 else math.inf
        rows.append((drift, r))
        ntxt = f"{n:,.0f}" if n != math.inf else f">{attempts:,}"
        print(f"   {drift*100:6.0f}%   | {r['median']:6.2f} | {r['mean']:7.2f} | {r['p05']:6.2f} |"
              f" {r['p95']:6.2f} | {r['profit_rate']:6.1%} |    {r['green_rate']:6.1%}   |"
              f" {r['ge_16_8']:7.4%} | {ntxt:>9} | {r['stop_rate']:7.1%}")
    print()
    print("  Uji kejujuran model: tanpa drift & tanpa biaya, exit di stopping time dari")
    print("  martingale => E[faktor per trade] = 1,00 persis.")
    z = simulate(attempts, 0.25, 20.0, 0.0, 0.0, 0.0, seed=12)
    print(f"    terukur: E[faktor] = {z['mean_factor']:.3f} | median multiple {z['median']:.3f}"
          f" | untung {z['profit_rate']:.1%} | stop {z['stop_rate']:.1%}")
    print("    -> model tidak dibuat supaya rugi: rata-ratanya impas, mediannya negatif.")
    print("    -> yang membalik rata-rata jadi minus adalah biaya, bukan asumsi drift.")
    print()
    r0 = rows[0][1]
    pg, pr = r0["green_rate"], r0["stop_rate"]
    p9 = binom_sf(9, SELLS, pg)
    p2 = binom_cdf(2, SELLS, pr)
    print("  Kombinasi yang diklaim: 9 hijau DAN 2 merah dari 11 trade.")
    print(f"    model drift 0 + biaya 3%: hijau/trade {pg:.1%}, merah/trade {pr:.1%}")
    print(f"    P(>=9 hijau) = {p9:.2e}   P(<=2 merah) = {p2:.2e}   gabungan ~ {p9*p2:.2e}")
    print("    (independen; korelasinya justru membuat gabungan ini makin mustahil)")
    print()
    print(f"  Klaim thread: 9 hijau / 2 merah, profit factor {209.3:.0f}x, 1 dari ? percobaan")
    for drift, r in rows:
        txt = f"{r['pf_ge_200']:.2e}" if r["pf_ge_200"] > 0 else "< 1/{:,}".format(attempts)
        print(f"    drift {drift*100:5.0f}%/jam -> P(PF >= 200) {txt}")
    print()


def section_costs() -> None:
    """Biaya round trip x 11 trade."""
    print("=" * 78)
    print("4. BIAYA 11 ROUND TRIP")
    print("=" * 78)
    print("  Fomo: 0,5% per sisi (0,45% kalau pakai referral) = 1,0% per round trip,")
    print("  gas ditanggung platform. Yang tidak ditanggung: price impact saat keluar.")
    print()
    print("  biaya/round trip | drag 11 trade | gross yang perlu untuk net 16,8x")
    print("  -----------------+---------------+--------------------------------")
    for c in (0.010, 0.020, 0.030, 0.050, 0.100):
        keep = (1 - c) ** SELLS
        need = (END / START) / keep
        print(f"       {c*100:4.1f}%        |    {(1-keep)*100:5.1f}%     |  {need:8.1f}x")
    print()
    print("  Catatan: exit $3.892 dari koin yang baru naik 3-5x adalah exit besar")
    print("  di pool tipis. Impact 2% itu optimistis; 5-10% lebih realistis.")
    print()


def section_skill(attempts: int) -> None:
    """Drift yang dibutuhkan supaya MEDIAN percobaan = 16,8x."""
    print("=" * 78)
    print("5. BERAPA 'SKILL' YANG DIBUTUHKAN AGAR INI JADI NORMAL?")
    print("=" * 78)
    target = END / START
    lo, hi = 0.0, 6.0
    for _ in range(18):
        mid = (lo + hi) / 2
        r = simulate(max(4000, attempts // 8), 0.25, 20.0, mid, 0.0, 0.0, seed=13)
        if r["median"] < target:
            lo = mid
        else:
            hi = mid
    need = (lo + hi) / 2
    print("  sigma 25%/jam, holding 20 menit, tanpa biaya. Drift = log-drift per jam.")
    print(f"  Supaya MEDIAN 11 trade = {target:.2f}x, log-drift harus ~{need:.2f}/jam,")
    print(f"  yaitu harga x{math.exp(need):.1f} tiap jam, terus-menerus selama 8j38m.")
    print("  Itu bukan edge; itu pasar yang salah harga total — dan tidak ada likuiditas")
    print("  yang membiarkan posisi penuh berulang kali di harga seperti itu.")
    print()
    print("  Kesimpulan: 16,8x bukan hasil 'metode yang bekerja', tapi ekor kanan")
    print("  dari distribusi yang median-nya negatif. Satu screenshot = satu sampel.")
    print()


def section_verdict() -> None:
    print("=" * 78)
    print("6. YANG BISA DIPERIKSA (dan yang tidak ada di thread)")
    print("=" * 78)
    print("  Tidak ada: alamat wallet, tx hash, tautan explorer, riwayat 11 trade,")
    print("             screenshot P&L mentah, atau rekaman layar selain 'watch 0:22'.")
    print("  Ada:       tautan referral fomo.family/r/savipww di balasan pertama,")
    print("             + 'prompt dan app-nya ada di artikel saya'.")
    print()
    print("  Ekonomi referral Fomo: perujuk dapat 25% dari fee yang dibayar yang")
    print("  dirujuk, seumur akun. 345 like x konversi kecil pun lebih pasti daripada")
    print("  16,8x dalam 8 jam. Insentif penulis dan pembaca TIDAK sejalan.")
    print()
    print("  Checklist kalau mau benar-benar memverifikasi (10 menit):")
    print("    1. alamat wallet Solana + 11 signature; buka di Solscan")
    print("    2. total P&L 30 hari, bukan 8 jam (satu window = satu lemparan koin)")
    print("    3. bandingkan entry/exit dengan harga pool saat itu (impact nyata)")
    print("    4. ulangi dengan modal kertas 30 hari; kalau edge-nya nyata, ia bertahan")
    print()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--mode", default="all",
                    choices=["all", "consistency", "stops", "swarm", "costs", "skill"])
    ap.add_argument("--attempts", type=int, default=40_000)
    ap.add_argument("--hold", type=float, default=20.0, help="holding menit per trade")
    args = ap.parse_args()

    if args.mode in ("all", "consistency"):
        section_consistency()
    if args.mode in ("all", "stops"):
        section_stops(args.hold)
    if args.mode in ("all", "swarm"):
        section_swarm(args.attempts)
    if args.mode in ("all", "costs"):
        section_costs()
    if args.mode in ("all", "skill"):
        section_skill(args.attempts)
    if args.mode == "all":
        section_verdict()


if __name__ == "__main__":
    main()
