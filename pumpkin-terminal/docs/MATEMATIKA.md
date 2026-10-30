# Matematika di balik "win rate 70%"

Dokumen ini menjelaskan **kenapa win rate saja tidak berarti apa-apa**, dan
aturan apa yang membuat target >70% tetap bisa profit. Semua angka dihitung
dengan rumus di bawah, bukan dikarang.

---

## 1. Tiga angka yang menentukan segalanya

- `c` = biaya round-trip (fee + slippage, dua arah)
- `t` = target take-profit
- `s` = stop-loss

Menang bersih = `t − c`. Kalah bersih = `s + c`.

## 2. Hit rate impas

```
p* = (s + c) / (t + s)
```

| Biaya | TP | SL | Hit rate impas |
|---|---|---|---|
| 1,5% | 6% | 6% | **62,5%** |
| 1,5% | 10% | 6% | 46,9% |
| 4,0% | 10% | 6% | 62,5% |
| 6,5% | 6% | 6% | **104,2%** ← mustahil |
| 6,5% | 10% | 6% | 78,1% ← win rate 70% **tetap rugi** |
| 6,5% | 15% | 8% | 63,0% |

**Bacaan yang keras tapi penting:** pada biaya meme coin 6,5%, target kecil 10%
dengan stop 6% menuntut win rate 78% hanya untuk balik modal. Jadi:

> **Win rate >70% tanpa target yang cukup besar = kekalahan yang terlihat seperti kemenangan.**

Inilah kenapa banyak "bot 90% win rate" di media sosial tetap menghabiskan modal.
Mereka menang kecil, kalah besar, dan biaya memakan selisihnya.

## 3. Target minimum agar EV positif pada p = 0,72

```
t > ((1 − p)·s + c) / p
```

| Biaya | SL | TP minimum |
|---|---|---|
| 1,5% | 5% | **4,0%** |
| 1,5% | 8% | 5,2% |
| 4,0% | 8% | 8,7% |
| 6,5% | 5% | 11,0% |
| 6,5% | 8% | 12,1% |

Sistem mengambil `t = max(t_min_user, required_tp(p̂, s, c) × 1,15)` — target
**diturunkan dari biaya**, bukan dari harapan. Kalau pasar tidak menawarkan
upside sebesar itu (dilihat dari likuiditas, pertumbuhan holder, dan kekuatan
narasi), trade **dilewati**. Ini persis permintaanmu: *jangan dipaksakan*.

## 4. Expectancy

```
E = p·(t − c) − (1 − p)·(s + c)
```

p = 0,72, TP 15%, SL 8%:

| Biaya | EV per trade |
|---|---|
| 1,5% | **+7,06%** |
| 4,0% | **+4,56%** |
| 6,5% | **+2,06%** |

## 5. Ukuran posisi: Kelly, lalu dipotong

```
b = (t − c) / (s + c)          f* = (p·b − q) / b
```

p = 0,72, TP 15%, SL 8%:

| Biaya | b | f* | ¼ Kelly |
|---|---|---|---|
| 1,5% | 1,42 | 52,3% | **13,1%** |
| 4,0% | 0,92 | 41,5% | **10,4%** |
| 6,5% | 0,59 | 24,2% | **6,1%** |

Sistem memakai **¼ Kelly** dan menambahkan dua batas keras:

- maksimum 5% ekuitas per posisi (sesuai spesifikasimu),
- maksimum 1% dari likuiditas pool.

Alasan memotong Kelly: `p̂` adalah **estimasi**, bukan kebenaran. Kalau estimasi
melenceng 10 poin persen, full-Kelly akan menghabisi akun. Quarter-Kelly menukar
sedikit pertumbuhan dengan kemungkinan bertahan yang jauh lebih besar.

## 6. Kenapa "profit kecil terus-menerus 24 jam" masuk akal

Dengan 20 trade/hari, EV +2% per trade, dan 5% ekuitas per posisi:

```
pertumbuhan harian ≈ (1 + 0,05 × 0,02)^20 − 1 ≈ +2,0% / hari
```

Setahun: `1,02^365 ≈ 1.370×`. Itu **jauh** lebih baik daripada mengejar satu
token 1000% yang peluangnya tidak pernah kamu ukur.

Tapi angka itu hanya berlaku kalau `EV` benar-benar positif **setelah** biaya.
Karena itu sistem menolak trade yang `EV < 2 × biaya` — margin keamanan, bukan
keserakahan.

## 7. Batas kerugian harian (survival)

```
berhenti trading jika drawdown harian ≤ −2% ekuitas
lanjut besok, bukan sekarang
```

Dengan p = 0,72, peluang 8 kekalahan beruntun = `0,28^8 ≈ 3,8 × 10⁻⁵`.
Tapi 8 kekalahan **bisa** terjadi, dan itulah yang membunuh akun tanpa batas
harian. Batas ini yang membuat sistem "menolak kalah" secara struktural,
bukan secara retoris.

## 8. Modal vs uang gratis (free trading)

- Modal awal dikunci di **vault**.
- Setiap kali ekuitas trading ≥ 2× modal awal, modal ditarik kembali ke vault.
- Setelah itu seluruh trading memakai **rumah** (house money) — kalau habis,
  kamu hanya kehilangan profit, bukan modal.

Ini bukan trik psikologis. Ini cara membuat *risk of ruin* terhadap modal = 0
secara matematis, bukan harapan.

---

## Yang tidak bisa dijanjikan

Tidak ada rumus di sini yang menjamin win rate >70% di pasar nyata. Yang bisa
dijamin secara matematis hanyalah:

1. jika `p̂` benar, EV positif mengikuti rumus di atas;
2. jika `p̂` salah, tidak ada ukuran posisi yang menyelamatkanmu;
3. karena itu `p̂` harus **diukur**, bukan diasumsikan — dan diukur ulang
   setiap kali kondisi pasar berubah.

Seluruh sistem ini dirancang untuk poin 3: setiap trade dicatat, setiap
prediksi dibandingkan dengan hasilnya, dan `p̂` diperbarui.
