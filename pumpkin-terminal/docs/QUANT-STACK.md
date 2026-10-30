# Stack kuant dari thread X — apa yang saya ambil, apa yang saya buang

Sumber: [@carm1nee, 29 Okt 2026](https://x.com/carm1nee/status/2115936358003052667) —
"these 10 github repos are the most DANGEROUS quant stack on the internet", klaim
**329k+ bintang**.

Saya cek sendiri lewat GitHub API pada 30 Oktober 2026. Angka bintangnya **benar**
(total 329.414). Jadi yang perlu diuji bukan jumlah bintangnya, tapi satu pertanyaan:
**dari 10 repo itu, apa yang bisa masuk ke sistem ini tanpa membuatnya lebih buruk?**

Batas keras sistem ini: Python stdlib saja, tanpa `pip install`, tanpa GPU, tanpa data
pasar berbayar, dan semuanya paper trading. Itu memotong sebagian besar stack — dan
memotong itu justru bagian yang jujur.

---

## 1. Peta 10 repo → keputusan

| # | Repo | ★ (30 Okt 2026) | Isinya | Keputusan | Alasan |
|---|---|---|---|---|---|
| 1 | [OpenBB](https://github.com/OpenBB-finance/OpenBB) | 74.898 | data platform: harga, opsi, makro | **tidak diambil** | Butuh dependency berat & kunci API berbayar. Konektor read-only Helius/Dexscreener yang sudah ada memainkan peran yang sama untuk memecoin. |
| 2 | [TradingAgents](https://github.com/TauricResearch/TradingAgents) | 118.558 | analis → bull vs bear → trader → tim risiko | **diambil strukturnya** | Bukan LLM-nya, tapi **kursinya**: ada pihak yang tugasnya mencari alasan menolak. → `pumpkin/committee.py` |
| 3 | [qlib](https://github.com/microsoft/qlib) | 49.832 | platform riset faktor | **diambil metodenya** | IC (information coefficient) per fitur + pruning faktor. → `pumpkin/analytics.py` |
| 4 | [RD-Agent](https://github.com/microsoft/RD-Agent) | 15.142 | agen penambang faktor otomatis | **diambil disiplinnya** | "70% fewer factors": buang fitur yang tidak lolos uji, jangan menumpuk. Di sini dipakai untuk memangkas keberatan komite kita sendiri. |
| 5 | [gs-quant](https://github.com/goldmansachs/gs-quant) | 13.832 | pricing & risk math | **diambil sebagian** | CVaR / expected shortfall + risk of ruin. Pricing opsi tidak relevan untuk token tanpa derivatif. |
| 6 | [nautilus_trader](https://github.com/nautechsystems/nautilus_trader) | 31.064 | engine event-driven deterministik | **sudah setara** | Desk ini memang event-driven per tick; yang belum ada justru *determinisme*, dan itu sudah diperbaiki (seed + urutan terurut, ada test-nya). |
| 7 | [Chronos](https://github.com/amazon-science/chronos-forecasting) | 6.209 | model time-series pretrained | **diambil idenya, bukan modelnya** | Tanpa torch tidak mungkin. Diganti proyeksi drift 3-tick vs target → `_forecast_gate`. |
| 8 | [QuantLib](https://github.com/lballabio/QuantLib) | 7.722 | pricing opsi/bond/swap | **tidak diambil** | Memecoin tidak punya leg opsi. Memaksakannya hanya menambah kompleksitas tanpa edge. |
| 9 | [skfolio](https://github.com/skfolio/skfolio) | 2.562 | optimasi portofolio + batas drawdown | **diambil sebagian** | *portfolio heat*: total uang yang benar-benar dipertaruhkan, bukan jumlah posisi. Optimasi mean-variance tidak masuk — jumlah aset yang layak di satu waktu cuma 0–4. |
| 10 | [vectorbt](https://github.com/polakowo/vectorbt) | 9.595 | backtest ribuan ide sekaligus | **tidak diambil (belum)** | Kami tidak punya data historis memecoin berlabel. Backtest massal di pasar sintetis hanya akan mengukur generator, bukan strategi. |

---

## 2. Yang benar-benar masuk ke kode

### a. Komite risiko (`pumpkin/committee.py`)

Urutan keputusan sekarang punya lawan bicara:

```
AlphaEngine (p̂, target, EV) → BearResearcher (keberatan + skor)
                             → RiskCommittee (tolak / perkecil / setujui)
                             → SNIPER beli
```

Delapan keberatan yang dihitung dari data teramati (bukan opini LLM):
`hype_tanpa_substansi`, `percakapan_dipesan`, `kejar_harga`, `rezim_lemah`,
`likuiditas_tipis`, `target_tidak_terjangkau`, `margin_tipis`, `portofolio_panas`.

Komite **tidak punya kewenangan memperbesar** posisi — hanya menolak atau memperkecil.
Itu disengaja: kalau tidak, ia berubah jadi mesin leverage.

### b. Pengukuran (`pumpkin/analytics.py`)

| Fungsi | Asal | Gunanya |
|---|---|---|
| `point_biserial` / `feature_ic` | qlib | IC per fitur + interval kepercayaan bootstrap 95% |
| `prune_features` | RD-Agent | pisahkan fitur yang terbukti dari derau |
| `cvar` | gs-quant | rata-rata kerugian di 5% ekor terburuk |
| `portfolio_heat` | skfolio | total risiko terbuka sebagai % ekuitas |
| `risk_of_ruin` | gs-quant | peluang menyentuh drawdown 30% (Monte Carlo) |

---

## 3. Hasil pengukuran — dan ini bagian yang penting

Saya tidak menambahkan fitur lalu mengklaimnya bagus. Setiap lapisan baru diuji
terhadap dirinya sendiri.

### a. Komite agregat: **tidak membantu** → default MATI

4 sesi × 450 tick, aturan lain identik:

| Lengan | Median PnL | Win rate | Trade | CVaR 95% | Max DD |
|---|---|---|---|---|---|
| Komite ON (veto 0,62 / perkecil 0,50) | +5,83% | 69,8% | 19,0 | **−15,30%** | 1,18% |
| Komite OFF | **+6,63%** | 69,8% | 21,2 | −14,07% | 1,40% |

Win rate sama, PnL lebih rendah, CVaR lebih buruk. Kesimpulannya: veto berdasarkan
*skor gabungan* tidak menambah informasi di atas filter yang sudah ada. Kode tetap ada
(`use_committee=True`) sebagai alat riset, tapi **bukan default**.

### b. IC tiap keberatan: 8 → 1 yang layak diuji

52 trade, IC point-biserial keberatan terhadap hasil:

| Keberatan | IC | CI 95% | Lolos? |
|---|---|---|---|
| `target_tidak_terjangkau` | −0,22 | [−0,41 … 0,00] | **batas** |
| `kejar_harga` | −0,14 | [−0,40 … 0,18] | tidak |
| `rezim_lemah` | −0,09 | [−0,41 … 0,15] | tidak |
| skor bear gabungan | −0,09 | [−0,38 … 0,18] | tidak |
| `percakapan_dipesan` | +0,13 | [0,00 … 0,22] | tidak (arah salah) |
| `hype_tanpa_substansi` | +0,17 | [−0,12 … 0,40] | tidak (arah salah) |
| `portofolio_panas` | 0,00 | — | tidak pernah aktif |

### c. Gerbang ramalan (dari Chronos): **netral** → default MATI

5 sesi × 450 tick:

| Lengan | Median PnL | Win rate | Trade | CVaR 95% |
|---|---|---|---|---|
| Gerbang ON | +6,29% | **69,2%** | 18,4 | −13,96% |
| Gerbang OFF | +6,39% | 68,3% | 18,6 | −13,70% |

Selisihnya di dalam derau. Jadi ia disimpan sebagai opsi (`use_forecast_gate=True`),
bukan dijalankan diam-diam.

### d. IC fitur inti — temuan yang paling berguna

127 trade (6 sesi), dihitung **hanya pada trade yang benar-benar dieksekusi**:

| Fitur | IC | CI 95% | Terbukti? |
|---|---|---|---|
| `momentum` | **+0,24** | [+0,05 … +0,43] | **ya** |
| `regime` | +0,05 | [−0,15 … +0,21] | belum |
| `social` | +0,04 | [−0,13 … +0,24] | belum |
| `coordination` | +0,03 | [−0,17 … +0,19] | belum |
| `safety` | −0,04 | [−0,21 … +0,11] | belum |
| `liquidity` | −0,05 | [−0,22 … +0,12] | belum |

Kenapa `social` dan `coordination` tidak terbukti padahal keduanya dipakai sebagai
filter? Karena **restriction of range**: semua trade yang lolos sudah punya social
tinggi dan koordinasi rendah, jadi variasi di dalam sampel tinggal sedikit. Fitur itu
sudah dipakai untuk *menyaring*, bukan lagi untuk *mengurutkan*. Momentum tidak pernah
jadi filter keras — karena itu ia masih membawa informasi.

**Dan justru di sinilah jebakan tuning:** memakai tabel ini untuk menaikkan bobot
`momentum` adalah overfitting pada 127 sampel. Tabel ini ditulis sebagai temuan,
bukan sebagai instruksi. Kalau mau diuji, pakai sesi yang tidak dipakai menghitungnya.

---

## 4. Yang tidak saya ambil dari resep 9 langkah di thread itu

Resepnya berakhir dengan kalimat yang saya setuju sepenuhnya:
*"paper trade the winner for 2 weeks, if it doesn't beat buy-and-hold, you don't have an edge yet."*

Tapi ada empat hal yang resep itu lewati:

1. **Bintang bukan bukti.** Repo dengan 118k bintang tetap tidak memberi tahu apa pun
   tentang biaya eksekusi di pasar yang kamu incar. Komentar di thread itu sendiri
   menulisnya: *"329k stars is a loud headline, not a proven hedge fund."*
2. **RD-Agent "2× annualized return" itu hasil backtest**, di paper NeurIPS, pada data
   yang dipakai untuk mencari faktornya. Itu in-sample, bukan hasil trading.
3. **Stack itu untuk ekuitas/opsi**, bukan token tanpa fundamentals, tanpa jam tutup,
   dan dengan slippage 2 digit persen. OpenBB/QuantLib/gs-quant pricing tidak
   menjawab satu pun masalah memecoin.
4. **"10.000 versi strategi" adalah cara tercepat menipu diri sendiri** kalau
   pemilihan versinya dilakukan pada data yang sama dengan pengujiannya. Kami belum
   punya data historis berlabel, jadi kami tidak berpura-pura punya `vectorbt`-nya.

---

## 5. Ringkas

| Diambil | Tidak diambil |
|---|---|
| struktur komite (TradingAgents) | LLM debat, OpenBB, QuantLib |
| IC + pruning faktor (qlib, RD-Agent) | qlib/RD-Agent sebagai dependency |
| CVaR, heat, risk of ruin (gs-quant, skfolio) | optimasi mean-variance |
| ide forecast sebagai gerbang (Chronos) | model Chronos itu sendiri |
| disiplin "ukur dulu, baru klaim" | klaim 2× return dari paper |

Dua lapisan (komite agregat, gerbang ramalan) **diukur lalu dimatikan** karena tidak
membayar dirinya sendiri. Itu bukan kegagalan — itu cara kerja yang benar.
