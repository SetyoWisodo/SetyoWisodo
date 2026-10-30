# 🎃 Pumpkin Terminal

**Desk trading memecoin Solana dengan 6 agen AI — versi jujur, paper trading, tanpa wallet.**

Dibangun sebagai jawaban atas thread viral @Shelpid_WI3M ("$80 → $5.432 dalam semalam").
Arsitekturnya nyata dan bisa dijalankan; angka di thread itu tidak.

```bash
python run.py serve        # dashboard live → http://localhost:8000
python run.py sim          # satu sesi headless + laporan
python run.py bench        # uji jujur: apakah profit datang dari strategi?
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

## Hasil uji jujur

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
│   ├── server.py           dashboard (stdlib HTTP + SSE)
│   └── static/index.html   UI terminal
└── tests/test_desk.py      25 test: aturan filter, stop, trailing, invariant portofolio
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
