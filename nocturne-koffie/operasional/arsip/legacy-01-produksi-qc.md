# D1 · Produksi & QC

**Tujuan:** tidak ada satu bungkus pun keluar tanpa pernah dicicipi.
**Pemilik:** owner (pilih biji, putuskan lolos/tolak) · **Pelaksana sangrai:** Ais Coffee Roastery.
**Bukti kerja:** `data/batch-qc.csv` + `data/stok-lot.json`.

---

## 1. Rantai produksi (7 langkah)

| # | Langkah | Siapa | Bukti yang dicatat |
| --- | --- | --- | --- |
| 1 | Terima & periksa green bean (kadar air, defect, ukuran) | Nocturne | Lot ID, kg masuk, harga/kg |
| 2 | Tentukan profil & target rasa per produk | Nocturne | Profil acuan per produk |
| 3 | Sangrai (batch mingguan) | Ais | Tanggal, batch ID, kg green → kg roasted |
| 4 | Cupping H+1 (cek pembentukan profil) | Nocturne | Skor awal, catatan |
| 5 | Cupping H+7 (penilaian akhir: lolos / tolak) | Nocturne | Skor akhir + keputusan |
| 6 | Kemas + tandai level roast (5 bulatan) + tanggal sangrai | Nocturne | Nomor batch di stiker |
| 7 | Serah ke D4 untuk pengiriman | Nocturne | Batch siap kirim |

**Aturan:** langkah 5 tidak boleh dilewati. Kalau tidak sempat cupping, batch itu **belum** boleh dijual.

---

## 2. Kode batch

Format: `NK-<KODE PRODUK>-<YYMM>-<A/B/C…>`
Contoh: `NK-IJN-2610-B` = Blue Mount Ijen, Oktober 2026, sangrai kedua bulan itu.

Kode ini dicetak/ditulis di kemasan dan dicatat di `batch-qc.csv`. Kalau ada komplain,
satu kode cukup untuk melacak: biji apa, kapan sangrai, skor berapa, siapa yang mencicipi.

---

## 3. Gerbang QC (lolos / tolak)

| Kriteria | Ambang lolos | Kalau gagal |
| --- | --- | --- |
| Skor cupping | ≥ 83.0 | Tolak |
| Cacat rasa (pahit tajam, ferment, smoky berlebih) | tidak ada | Tolak |
| Yield sangrai | ≥ 0.78 (0.80 ideal) | Periksa profil; catat penyimpangan |
| Berat bersih kemasan | ±2 g dari label | Timbang ulang |
| Konsistensi dengan batch sebelumnya | profil sama | Tahan, cicip ulang H+2 |

Batch ditolak **tidak dikirim, tidak didiskon, tidak "tetap dijual murah"**. Disangrai ulang
atau dijual sebagai batch uji internal (dengan label jelas, bukan lewat situs).

---

## 4. Cupping: form minimal

Catat 5 hal, skala 1–10: **sweetness · acidity · body · aftertaste · cleanliness**.
Skor akhir = rata-rata × 10 (maks 100) + catatan 3 kata rasa.

Contoh baris CSV:

```
2026-10-24,NK-GYO-2610-A,gayo,2.0,1.60,0.800,81.5,ditolak,"Aftertaste pahit, manis tidak muncul; sangrai ulang"
```

---

## 5. Stok: dari green bean, bukan dari tumpukan kopi jadi

Rumus yang dipakai papan:

```
roasted_g   = sisa_green_kg × yield × 1000
bungkus     = floor(roasted_g ÷ gramase ukuran)
status      = habis (0) · terbatas (≤20% hasil awal) · tersedia
blend       = min(sisa komponen ÷ proporsi)   # 70/30 → min(Raung/0.7, Ijen/0.3)
```

**Tugas mingguan:** setiap Kamis, setelah cupping, perbarui
1. `data/stok-lot.json` → `terpakai_kg` lot yang disangrai minggu itu,
2. `data/catalog.json` → `status` tiap produk (tersedia / terbatas / habis / menunggu-panen),
3. `brand.stock_updated` → tanggal hari itu.

Kalau lupa, papan akan menandai **"beda status"** sebagai kritis — itu bukan gangguan, itu alarm.

---

## 6. KPI divisi

| KPI | Target | Cara ukur |
| --- | --- | --- |
| Batch ditolak | < 10% per bulan | baris `ditolak` ÷ total batch |
| Skor cupping rata-rata | ≥ 84 | kolom `skor_cupping` |
| Yield rata-rata | ≥ 0.79 | kolom `yield` |
| Selisih status situs vs lot | 0 | kolom "Beda" di papan |
| Batch tercatat | 100% | setiap sangrai punya baris |

---

## 7. Kesalahan yang paling sering terjadi

| Kesalahan | Akibat | Pencegahan |
| --- | --- | --- |
| Menjual batch tanpa cupping H+7 | Komplain rasa, reputasi turun | Batch tanpa skor akhir = belum boleh tayang |
| Menghitung stok dari kopi jadi | Situs menjanjikan stok yang tak ada | Selalu dari sisa green × yield |
| Mencetak level roast tanpa menandai batch | Tidak bisa dilacak | Kode batch wajib di kemasan |
| Menyebut "roastery kami" saat menjelaskan proses | Melanggar brief 11.8 | Kalimat baku: "disangrai mingguan oleh Ais Coffee Roastery" |
| Menerima order 1 kg padahal sisa 300 g | Harus membatalkan | Cek papan sebelum konfirmasi order besar |
