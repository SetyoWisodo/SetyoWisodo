# 🎃 Pumpkin Terminal

**Desk trading memecoin Solana dengan 6 agen AI — versi jujur, paper trading, tanpa wallet.**

Dibangun sebagai jawaban atas thread viral @Shelpid_WI3M ("$80 → $5.432 dalam semalam").
Arsitekturnya nyata dan bisa dijalankan; angka di thread itu tidak.

```bash
python run.py serve        # dashboard live → localhost:8000  ( /  /whale  /social )
python run.py sim          # sesi headless scan-desk + laporan
python run.py whale        # sesi headless Whale Radar + laporan
python run.py bench        # uji jujur: apakah profit datang dari strategi?
python run.py whale-bench  # uji jujur: informed whales vs whale acak
python run.py social       # sesi headless Social Radar + laporan
python run.py social-bench # uji jujur: dengan vs tanpa detektor koordinasi
```

Tanpa dependency. Python 3.10+ saja. Tidak ada `pip install`, tidak ada API key.

---

## ⚠️ Baca ini dulu

Thread aslinya berbunyi:

> *"I Gave My Grok Bot $80 ... By 7:30 AM, It Had Turned $80 Into $5,432."*

Di bagian bawah thread yang sama tertulis: **"These Are Simulated Results, Not Verified Live Trading Profits."**
Itu paper trading — simulasi. "Pumpkin Terminal" juga bukan produk resmi xAI/Grok, dan
akun @Shelpid_WI3M bukan akun resmi apa pun. $80 → $5.432 = **+6.690% dalam satu malam**
sambil tidur.

Repo ini membangun *hal yang benar-benar ada di balik thread itu*: enam agen dengan aturan
risiko yang bisa diuji. Lalu repo ini menunjukkan, dengan angka, kenapa hasil di thread itu
tidak boleh kamu jadikan ekspektasi.

Yang tidak ada di repo ini, dan tidak akan ditambahkan tanpa permintaan eksplisitmu:
private key, koneksi wallet, signing transaksi, atau order on-chain. Semua eksekusi
adalah **fill simulasi**.

---

## Enam agen

| Agen | Tugas | Aturan yang ditegakkan |
|---|---|---|
| **SCOUT** | memindai pair baru dari feed | dedup, inventarisasi, tanpa menilai |
| **FILTER** | menolak sebelum uang keluar | liq ≥ $18k, holder ≥ 220, top-10 ≤ 32%, wallet dev ≤ 8%, mint authority dicabut, LP terkunci |
| **ANALYST** | memberi skor 0–1 | komposit likuiditas, distribusi, keamanan, momentum; masuk hanya jika ≥ **0,60**; token yang sudah terbang didiskon |
| **SNIPER** | menentukan ukuran | maks **8%** saldo per posisi, maks 3 posisi, maks 0,5% dari likuiditas pool, satu entry per 2 tick |
| **GUARD** | keluar sebelum terlambat | stop-loss keras **−6%**, trailing setelah **+12%** (jarak 8%), keluar paksa setelah 240 tick, keluar jika likuiditas lenyap |
| **SCRIBE** | mencatat semuanya | setiap entry, exit, dan **penolakan** → `runs/<sesi>/events.jsonl` |

Setiap penolakan tercatat dengan alasannya. Kalau kamu ingin mengaudit filter, datanya ada.

**Biaya yang dimodelkan** (inilah yang membunuh sebagian besar "strategi" memecoin):

```
fee masuk 1,0% + slippage masuk 1,5% + fee keluar 1,0% + slippage keluar 2,0%
= round-trip 5,5% sebelum kamu untung satu sen pun
```

Slippage naik otomatis untuk token yang sedang lari. Stop-loss pada token yang rug
ditembus (gap), bukan dieksekusi rapi di −6%.

---

## 🐋 Whale Radar — mengikuti aliran dompet

Modul kedua menjawab permintaan yang berbeda: **bukan memindai semua token,
tapi mengikuti uang orang yang lebih tahu.**

```
dompet whale → agregasi aliran (jendela 6 tick)
             → sinyal per token (jumlah whale × dolar × reputasi)
             → forensics < 1 detik (dev %, bundle %, top-10, LP, mint, riwayat dev)
             → SNIPER: 5% ekuitas per posisi, target +50%
             → GUARD: stop, trailing, batas waktu 12 tick
             → SCRIBE: semua keputusan, termasuk yang ditolak
```

Lapisan yang membuat ini lebih dari sekadar "copy trade":

| Lapisan | Fungsi |
|---|---|
| **WhaleRegistry** | merekam setiap panggilan whale, menandai berhasil/gagal, menghitung reputasi dengan Laplace smoothing |
| **FlowAggregator** | menggabungkan transaksi jadi satu skor 0–1 per token (jumlah whale, dolar bersih, reputasi rata-rata, recency) |
| **DevLedger** | riwayat dev yang berakhir rug — repeat offender langsung terlihat |
| **Forensics** | `rug_risk` 0–1 + temuan konkret, dieksekusi ~0,003 ms per token |
| **Disiplin "jangan kejar"** | tolak entry kalau harga sudah lari >10% dari harga saat sinyal terlihat |

### Hasil (10 sesi per mode, target +50%, stop −8%, 5% ekuitas/posisi)

| Mode | Median PnL | IQR | Sesi profit | Trade | Hit rate | Impas |
|---|---|---|---|---|---|---|
| `informed` (whale punya informasi) | **+10,2%** | +5,2% .. +16,8% | 8/10 | 34 | **44,8%** | 33,0% (empiris) |
| `noise` (whale memilih acak) | **−0,8%** | −2,8% .. −0,6% | 1/10 | 2 | 16,7% | — |

Tiga hal yang penting dari angka ini:

1. **Kualitas sinyal mentah → 40,4%** dari token yang diikuti benar-benar mencapai
   +50% dalam ≤12 tick (mode informed). Itu edge yang nyata di dalam simulasi.
2. **Tapi hasil bersihnya cuma +10%**, karena entry selalu tertunda 1 tick,
   stop kena gap saat dump, dan round-trip cost 6,5%.
3. **Mode noise berhenti sendiri.** Saat whale-nya acak, reputasi mereka jatuh di
   bawah ambang dan desk hanya melakukan 2 trade dalam 10 sesi. Itu fitur:
   lebih baik tidak trading daripada ikut omong kosong.

### Kenapa "profit 50% dalam hitungan detik" itu jebakan

Dengan target +50% dan stop −8% plus biaya 6,5%, kamu butuh hit rate **>25%**
hanya untuk impas — dan **~33%** setelah memperhitungkan gap saat dump.
Artinya kemenangan +50% harus cukup sering untuk membayar semua kerugian kecil.
Uji `whale-bench` memperlihatkan bahwa tanpa informasi whale, angka itu tidak tercapai.

Yang paling mengubah hasil bukan sinyalnya, tapi **aturan "jangan kejar"**:
tanpa aturan itu median PnL jatuh dari +10,2% ke ~0%.

### Menjalankan

```bash
python run.py serve                 # buka http://localhost:8000/whale
python run.py whale --ticks 2400    # headless + laporan markdown
python run.py whale --whale-edge noise   # kontrol: whale acak
python run.py whale-bench           # bandingkan informed vs noise
```

### Memakai data sungguhan

```bash
export HELIUS_API_KEY=xxxx          # gratis di helius.dev
python run.py whale-watch --wallets wallets.json --poll 6
```

`whale-watch` hanya **membaca** aktivitas dompet publik dan mencetak aliran masuk/keluar.
Tidak ada private key, tidak ada penandatanganan transaksi, tidak ada order.

Batasan data publik yang harus kamu tahu: endpoint gratis memberi tahu *token apa*
yang dibeli sebuah dompet, tapi **tidak** memberi porsi supply dev, bundle %, status
LP lock, atau riwayat rug. Untuk forensics kelas produksi kamu butuh indexer
berbayar (Helius DAS, Birdeye, Solscan Pro) atau mem-parse sendiri akun token & pool.
Selama data itu tidak ada, FILTER menolak — dan itu memang seharusnya.

### Menaikkan Whale Radar ke kenyataan (urutan yang aman)

1. **Kumpulkan dulu, jangan trading.** Jalankan `whale-watch` 2–4 minggu. Simpan
   setiap aliran ke database. Bangun reputasi whale dari data nyata, bukan asumsi.
2. **Forensics sendiri.** Tanpa data holder/dev, seluruh lapisan risiko ini buta.
   Ambil dari indexer berbayar atau parse `getTokenLargestAccounts` + pool state.
3. **Shadow trade.** Hitung fill hipotetis dari harga pool nyata (bukan mid price),
   bandingkan dengan simulasi. Ukur slippage sungguhan vs 2%.
4. **Baru uang receh.** Wallet terpisah, ukuran ≤1% ekuitas, dan anggap uangnya
   hangus saat kamu menekan enter.

---

## 📡 Social Radar — berita, KOL, dan bot farm

Modul ketiga menjawab permintaan yang paling eksplisit: **"win rate di atas 70%,
masukkan semua berita, dan harga yang bergerak karena postingan orang berpengaruh —
dengan logika matematika yang kelihatan."**

```
post X/Telegram → sentimen + ticker + engagement
                → graf pengaruh (reputasi empiris per akun, bukan daftar statis)
                → deteksi koordinasi (5 fitur: teks klon, burst, akun baru,
                  rasio follower, konsentrasi ticker)
                → agregasi: velocity, akselerasi, reach  (turunan, bukan level)
                → p̂ = σ(bias + Σ wᵢ·fiturᵢ)
                → target diturunkan dari biaya, EV ≥ 2× biaya, Kelly ¼, cap 5%
                → GUARD: separuh keluar di 60% target, stop keras, trailing, time stop
                → JOURNAL (SQLite): setiap trade & setiap penolakan
```

### Tiga permintaan, tiga penyesuaian yang jujur

**1. "Win rate >70%" tidak bisa berdiri sendiri — ia harus dibandingkan dengan impas.**
Hit rate impas untuk target `t`, stop `s`, biaya `c` adalah `(s+c)/(t+s)`:

| Target | Stop | Biaya | Hit rate impas |
|---|---|---|---|
| 6% | 6% | 1,5% | **62,5%** |
| 10% | 6% | 1,5% | **46,9%** |
| 15% | 8% | 1,5% | **41,3%** |
| 15% | 8% | 4,0% | **52,2%** |
| 10% | 6% | 6,5% | **78,1%** ← menang 70% masih rugi |

Jadi target 70% baru masuk akal kalau biayanya kecil dan targetnya tidak serakah.
Desk ini memakai biaya 4,0% (fee + slippage dua arah) dan mengunci p̂ ≥ 0,72.

**2. "Kalau tidak mendukung 1000% dalam satu koin, jangan dipaksa" → jadi aturan keras.**
Target minimum dihitung dari biaya, bukan dari harapan:

```
t > ((1 − p)·s + c) / p
```

Pada p = 0,72, s = 6%, c = 4% → target ≥ 17,1%; sistem lalu juga menuntut
`EV ≥ 2× biaya`, dan menolak trade kalau `upside_est × 0,7 < target`.
Frasa "jangan dipaksa" sekarang punya kode dan angka, bukan niat.

**3. "Modal + free trading" → aturan vault.** Saat ekuitas mencapai 2× modal,
desk menarik modal awal ke vault dan **berhenti mempertaruhkan uangmu**. Setelah itu
semua trading memakai uang profit. Itu batas struktural atas risiko kehilangan modal —
bukan janji, dan bukan jaminan.

### Hasil uji — diukur, bukan diklaim

**10 sesi per lengan, 800 tick, $250 awal, p̂ ≥ 0,72, target 8–30%, stop 6%, 5% ekuitas/posisi.**

| Lengan | Median PnL | IQR | Sesi profit | Win rate | Trade | Expectancy/trade |
|---|---|---|---|---|---|---|
| **Pasar kotor + detektor koordinasi** | **+13,4%** | +5,1% .. +17,7% | **10/10** | **73,5%** | 35 | +6,41% |
| Pasar kotor, **tanpa** detektor (naif) | **−2,1%** | −2,6% .. −1,6% | 0/10 | 44,6% | 78 | −2,58% |
| Pasar bersih (tanpa bot farm) + detektor | **+14,1%** | +3,2% .. +20,6% | 9/10 | 74,8% | 32 | +7,36% |

Yang boleh kamu simpulkan dari tabel itu, dan yang tidak:

- **Win rate 73,5% diukur dari trade yang benar-benar dieksekusi**, dengan expectancy
  +6,41% per trade setelah fee dan slippage. Ambang impas empiris dihitung di setiap
  laporan sesi (`empirical_breakeven`) dari rata-rata menang vs kalah yang sungguh
  terjadi — bukan angka 70% yang ditempel di atas kertas.
- **Tanpa detektor koordinasi, median berbalik negatif** (−2,1%) dan 0 dari 10 sesi
  profit, meski win rate-nya masih 44,6%. Trade-nya 78 vs 35: trader naif terus membeli
  shill trap. Selisih **+15,5 poin** itulah nilai lapisan tersebut.
- **Pasar bersih lebih untung** (+14,1%) karena tidak ada jebakan. Artinya filtrasi
  tidak membuang alpha; ia membuang kerugian.
- **Rata-rata p̂ saat entry 0,736 vs win rate 73,5%** → model hampir persis terkalibrasi
  (selisih 0,1 poin), yang berarti ambang 0,72 memang bekerja sebagai ambang, bukan hiasan.
- **Bench ini deterministik**: seed tetap + urutan pemrosesan terurut, jadi menjalankannya
  dua kali memberi angka yang sama. Kalau kamu ubah aturan, angkanya berubah — dan itu
  memang tujuannya.
- **Semua ini di pasar sintetis.** Harga di sini benar-benar bereaksi pada sinyal.
  Di pasar nyata kamu adalah orang terakhir yang membaca postingan itu.

Detail mentah: `runs/social-bench.json`.

### Kenapa lapisan koordinasi itu inti, bukan hiasan

Bot farm membuat token naik 2–3 tick lalu menjatuhkannya. Trader yang hanya menghitung
jumlah mention akan membeli tepat di puncak — dan dialah yang jadi exit liquidity.
Detektor di sini memakai lima fitur yang semuanya murah dihitung:

| Fitur | Bobot | Yang ditangkap |
|---|---|---|
| Duplikasi teks (Jaccard 3-gram ≥ 0,72) | 0,30 | templateshilling yang sama persis |
| Burst (semua post ≤ 3 tick) | 0,24 | serangan serempak, bukan diskusi |
| Akun baru (< 7 hari) | 0,18 | farm yang baru dibuat |
| Rasio follower/following tidak wajar | 0,14 | akun beli follower |
| Konsentrasi satu ticker | 0,14 | semua menempel satu token |

Reputasi akun **tidak** berasal dari daftar statis: setiap akun ditandai berhasil kalau
token yang ia sebut naik ≥25% setelah disebut, gagal kalau tidak, lalu dihitung dengan
Laplace smoothing `(hit+1)/(hit+miss+2)`.

### Yang modul ini bukan

- **Bukan data X/Telegram sungguhan.** Postingan, KOL, bot, dan berita dihasilkan
  generator di `social_market.py`. `docs/SOCIAL-ALPHA-RESEARCH.md` memetakan tooling
  nyata (FinBERT, CIB graph analytics, KOL tracker) dan apa yang sengaja tidak diambil.
- **Bukan bukti strategi ini profit di Solana.** Yang diukur adalah mesinnya: apakah
  aturan risiko, kalibrasi p̂, dan filter koordinasi bekerja seperti yang dirancang.
- **Bukan jaminan win rate 70% di pasar nyata.** Di simulasi, harga benar-benar
  bergerak sesuai sinyal. Di pasar nyata kamu membeli setelah postingan itu dibaca
  semua orang.

### Sudah dibaca dan diuji, bukan ditiru

Dua thread lain yang beredar juga saya bedah, dan hasilnya ditulis apa adanya:

- [`docs/QUANT-STACK.md`](docs/QUANT-STACK.md) — 10 repo kuant (329k bintang, dicek
  lewat API). Empat metodenya dipakai; dua lapisan yang dibangun dari situ **diukur
  lalu dimatikan** karena tidak membayar dirinya sendiri.
- [`docs/POLYMARKET-BOT-REVIEW.md`](docs/POLYMARKET-BOT-REVIEW.md) — "bot BTC 5 menit"
  yang katanya profit jutaan. Aritmetikanya setengah benar, mekanismenya tidak bisa
  dipakai, dan produk yang sebenarnya dijual adalah tautan referral.

### Menjalankan

```bash
python run.py social --ticks 1200 --mode dirty    # sesi headless + laporan
python run.py social-bench --ticks 800 --seeds 10 # dengan vs tanpa detektor koordinasi
python run.py serve                              # → /social
```

Hasil mentah tersimpan di `runs/social-bench.json`; laporan per sesi ada di
`runs/<session>/social-report.md`. Matematikanya di `docs/MATEMATIKA.md`,
riset tooling-nya di `docs/SOCIAL-ALPHA-RESEARCH.md`.

---

## 🧪 Dari "10 repo kuant paling berbahaya di internet"

Ada thread X ([@carm1nee, 29 Okt 2026](https://x.com/carm1nee/status/2115936358003052667))
yang menyusun 10 repo kuant jadi satu stack: OpenBB, TradingAgents, qlib, RD-Agent,
gs-quant, nautilus_trader, Chronos, QuantLib, skfolio, vectorbt — klaim **329k+ bintang**.

Saya cek angkanya lewat GitHub API: **329.414 bintang, benar**. Jadi yang diuji bukan
bintangnya, tapi satu pertanyaan: *apa yang bisa masuk ke sistem ini tanpa membuatnya
lebih buruk?* Batasnya keras — stdlib, tanpa GPU, tanpa data berbayar, paper trading.

Ringkasan lengkap (termasuk angka tiap uji) ada di
[`docs/QUANT-STACK.md`](docs/QUANT-STACK.md). Yang masuk ke kode:

| Diambil | Jadi apa |
|---|---|
| struktur *TradingAgents* (bull vs bear → tim risiko) | `committee.py`: 8 keberatan + veto/perkecil, **tanpa** LLM |
| IC & pruning faktor (*qlib*, *RD-Agent*) | `analytics.py`: IC point-biserial + CI bootstrap 95% |
| CVaR, heat, risk of ruin (*gs-quant*, *skfolio*) | KPI risiko di laporan, dashboard, dan snapshot |
| ide forecast sebagai gerbang (*Chronos*) | `_forecast_gate`: proyeksi drift 3-tick vs target |

Yang **tidak** diambil: OpenBB (butuh dependency & API key), QuantLib (memecoin tanpa
opsi), model Chronos (butuh torch), vectorbt (kami tidak punya data historis berlabel —
backtest massal di pasar sintetis hanya mengukur generator). nautilus_trader tidak perlu:
desk ini sudah event-driven per tick, dan determinisme yang belum ada sudah ditambahkan.

### Yang penting: dua lapisan diukur, lalu dimatikan

| Uji | Hasil | Keputusan |
|---|---|---|
| **Komite veto agregat** (4 sesi × 450 tick) | median **+5,83%** vs **+6,63%** tanpa komite; CVaR **−15,30%** vs −14,07%; win rate sama (69,8%) | **default MATI** |
| **Gerbang ramalan** (5 sesi × 450 tick) | median +6,29% vs +6,39%; win rate 69,2% vs 68,3%; trade 18,4 vs 18,6 | **default MATI** (opsional) |
| **IC 8 keberatan komite** (52 trade) | hanya `target_tidak_terjangkau` yang mendekati signifikan (IC −0,22, CI −0,41…0,00). Skor gabungan: IC −0,09, CI melewati nol | skor gabungan tidak dipakai sebagai veto |

Lalu IC fitur inti pada 127 trade yang benar-benar dieksekusi:

| Fitur | IC | CI 95% | Terbukti? |
|---|---|---|---|
| `momentum` | **+0,24** | +0,05 … +0,43 | **ya** |
| `regime` | +0,05 | −0,15 … +0,21 | belum |
| `social` | +0,04 | −0,13 … +0,24 | belum |
| `coordination` | +0,03 | −0,17 … +0,19 | belum |
| `safety` | −0,04 | −0,21 … +0,11 | belum |
| `liquidity` | −0,05 | −0,22 … +0,12 | belum |

`social` dan `coordination` tidak terbukti **karena restriction of range**: keduanya
sudah dipakai menyaring, jadi variasi yang tersisa di dalam sampel tinggal sedikit.
Momentum tidak pernah jadi filter keras — karena itu ia masih membawa informasi.

Dan justru di sini jebakan tuning-nya: menaikkan bobot momentum berdasarkan tabel ini
adalah overfitting pada 127 sampel. Tabelnya ditulis sebagai temuan, bukan instruksi.

---

## Hasil uji jujur — scan desk

`python run.py bench` menjalankan 10 sesi per mode, saldo awal $80, 1.000 tick:

| Mode | Median PnL | Rentang IQR | Sesi profit | Trade/sesi | Fee |
|---|---|---|---|---|---|
| `correlated` (desk lengkap) | **+173,7%** | +1,4% .. +429,9% | 8/10 | 74 | $16,79 |
| `null` (tanpa keahlian) | **−45,9%** | −59,6% .. −20,0% | 1/10 | 270 | $23,85 |

Cara membacanya:

- **`correlated`** — generator pasar sengaja menciptakan akumulasi harga sebelum lonjakan,
  jadi momentum yang dibaca ANALYST *benar-benar* punya arti. Angka +174% ini mengukur
  apakah pipeline-nya bekerja. **Bukan** bukti strategi ini profit di pasar nyata, karena
  di pasar nyata tidak ada yang memberitahu agen mana token yang akan melonjak.
- **`null`** — semua keahlian dimatikan: FILTER dilewati, skor ANALYST jadi acak. Ini
  setara melempar panah ke papan. Hasilnya **−46% dengan 270 trade** — bukan karena
  sial, tapi karena 5,5% round-trip cost dikali 270 trade, ditambah rug yang menembus
  stop-loss. Inilah baseline yang harus kamu kalahkan sebelum bicara profit.
- **+6.690%** di thread ada jauh di luar ekor distribusi bahkan dari simulasi yang
  *ramah* ini (maksimum 10 sesi: +564%). Itu satu undian paper-trading, bukan nilai
  harapan. Perhatikan IQR mode `correlated` saja: +1,4% sampai +430% — satu sesi yang
  kebetulan kena beberapa lonjakan bisa terlihat seperti mesin uang.

Angka di tabel ini akan berubah kalau kamu mengubah aturan di `config.py`. Itu memang
tujuannya: jalankan ulang `bench` setiap kali mengubah parameter.

---

## Menjalankan

### Dashboard live (paper trading)

```bash
python run.py serve --port 8000
```

Buka `http://localhost:8000`. Yang kamu lihat:

- kurva ekuitas real-time, PnL, win-rate, expectancy, max drawdown, fee terakumulasi
- 6 kartu agen dengan hitungan dan pesan terakhirnya
- log SCRIBE yang berisi **penolakan** juga, bukan cuma trade
- posisi terbuka dengan unrealized PnL dan puncak tertinggi
- kontrol: pause/lanjut, sesi baru, kecepatan 1×/2×/4×, unduh laporan

Endpoint: `GET /api/state`, `GET /api/stream` (SSE), `POST /api/control`,
`GET /api/report`, `GET /api/report.md`.

### Sesi headless + laporan

```bash
python run.py sim --ticks 1800 --balance 80
python run.py sim --edge null            # kontrol: skor acak
python run.py sim --threshold 0.75       # lebih selektif
python run.py sim --seed 42              # sesi lain
```

Output: `runs/<sesi>/report.md`, `report.json`, `events.jsonl`.

### Data pasar sungguhan (tetap paper trading)

```bash
python run.py sim --feed dexscreener
```

Menarik pair Solana dari API publik Dexscreener. Ini **hanya data** — tidak ada wallet
dan tidak ada order. Jalankan di mesinmu sendiri; sandbox Arena membatasi egress jaringan
sehingga mode ini gagal di sini, dan itu memang diharapkan.

Catatan: endpoint publik Dexscreener tidak menyediakan data holder/keamanan kontrak,
jadi FILTER akan menolak hampir semuanya (field keamanan dianggap `false`). Itu perilaku
yang benar: **menolak saat tidak tahu** lebih baik daripada menebak.

---

## Konfigurasi

Semua aturan ada di `pumpkin/config.py` dan dipakai apa adanya oleh agen:

```python
FilterRules(min_liquidity_usd=18_000, min_holders=220, max_top10_pct=32,
            max_dev_pct=8.0, require_mint_revoked=True, require_lp_locked=True)

RiskRules(max_position_pct=0.08, max_concurrent=3, stop_loss_pct=0.06,
          trail_after_pct=0.12, trail_distance_pct=0.08, max_hold_ticks=240,
          entry_fee_pct=0.010, exit_fee_pct=0.010,
          entry_slippage_pct=0.015, exit_slippage_pct=0.020, min_score=0.60)
```

Kalau kamu mengubah aturan ini, jalankan `python run.py bench` lagi — hasil lama tidak
berlaku untuk aturan baru.

---

## Struktur

```
pumpkin-terminal/
├── run.py                  CLI: serve | sim | bench
├── pumpkin/
│   ├── config.py           aturan filter & risiko
│   ├── models.py           Token, Position, Trade, Event
│   ├── feed.py             SimMarket (sintetis) + DexscreenerFeed (data live)
│   ├── agents.py           SCOUT, FILTER, ANALYST, SNIPER, GUARD, SCRIBE
│   ├── engine.py           loop tick, portofolio, eksekusi
│   ├── report.py           laporan JSON + Markdown
│   ├── whale_desk.py       Whale Radar: aliran whale + forensics
│   ├── whales.py           reputasi whale (Laplace) + agregasi aliran
│   ├── forensics.py        rug_risk & latency
│   ├── social_signal.py    sentimen, graf pengaruh, deteksi koordinasi, p̂ & Kelly
│   ├── social_market.py    pasar sintetis: KOL, bot farm, berita, rezim
│   ├── social_desk.py      Social Radar: entry, exit bertingkat, vault, KPI
│   ├── committee.py        komite risiko: 8 keberatan, veto/perkecil (default mati)
│   ├── analytics.py        IC + CI bootstrap, CVaR, heat, risk of ruin
│   ├── journal.py          SQLite: trade, keputusan, berita
│   ├── server.py           dashboard (stdlib HTTP + SSE)
│   └── static/             index.html · whale.html · social.html
├── docs/MATEMATIKA.md      hit-rate impas, required TP, EV, Kelly, survival
├── docs/SOCIAL-ALPHA-RESEARCH.md  riset tooling sosial + apa yang tidak diambil
├── docs/QUANT-STACK.md     10 repo kuant dari thread X: diambil/dibuang + hasil uji
└── tests/                  92 test: filter, stop, trailing, invariant, p̂, Kelly, IC, CVaR
```

```bash
python -m unittest discover -s tests -v
```

Test yang paling penting: `test_tidak_ada_aset_laten_bocor_ke_laporan` memastikan agen
tidak pernah "mengintip" variabel internal generator (archetype, jadwal lonjakan) —
kalau bocor, seluruh simulasi jadi tidak bermakna.

---

## Kalau nanti mau live

Jangan lompat. Urutannya:

1. **Paper + data nyata** (`--feed dexscreener`) minimal beberapa minggu. Catat
   slippage nyata vs asumsi.
2. **Shadow mode**: hitung fill hipotetis dari order book nyata, bandingkan dengan
   simulasi.
3. **Live dengan ukuran receh** yang kamu rela hanguskan 100%, wallet terpisah,
   `max_position_pct` ≤ 1%.
4. Baru bicara soal menambah ukuran.

Dan yang paling penting: **tidak ada angka di README ini yang boleh masuk ke keputusan
keuanganmu.** Semua ini alat untuk memahami biaya dan risiko, bukan ramalan.

---

## Lisensi & atribusi

Kode di repo ini bebas kamu pakai dan ubah. Thread aslinya milik @Shelpid_WI3M; repo ini
tidak berafiliasi dengan xAI, Grok, pump.fun, Raydium, atau Dexscreener.
