# D1 · Produksi & QC — alur kerja & target

> **Mandat:** tidak ada satu bungkus pun keluar tanpa pernah dicicipi.
> **Pemilik:** owner (pilih biji, putuskan lolos/tolak). **Pelaksana sangrai:** Ais Coffee Roastery, Banyuwangi.
> **Waktu:** ±2 jam/minggu (sangrai + cupping) + 10 menit/hari (stok & catatan).
> **Berkas kerja:** `data/batch-qc.csv` · `data/stok-lot.json` · `data/biaya.json` · `data/catalog.json`.
> **Target & KPI:** hidup di `data/divisi.json` (D1). Jangan mengetik ulang angka target di dokumen ini.

Nocturne **bukan roastery**. Kami memilih biji, menetapkan standar, memeriksa hasil, dan menanggung
keputusan tolak. Kalimat itu dipakai apa adanya di semua kanal.

---

## 1. Alur kerja inti — satu batch, dari biji ke keputusan

```
[1] Cek stok lot        → [2] Tetapkan rencana batch   → [3] Kirim brief ke Ais
        │                        │                              │
        ▼                        ▼                              ▼
  stok-lot.json          target rasa + volume          jadwal sangrai (Senin)
                                                                 │
[4] Sangrai oleh Ais → [5] Istirahat 12–24 jam → [6] Cupping & skor
                                                                 │
                       ┌─────────────────────────────────────────┴───────────┐
                       ▼                                                     ▼
              skor ≥ 83 → [7] LOLOS                              skor < 83 → [8] TOLAK
                       │                                                     │
              kemas + label batch                                sangrai ulang / jual sebagai
              (tools/brandkit.py)                                "eksperimen" TIDAK diperbolehkan
                       │                                                     │
                       ▼                                                     ▼
              [9] Update stok & status di situs                  [10] Catat alasan di batch-qc.csv
```

**Aturan keras:** barang tidak boleh masuk daftar jual sebelum langkah 7 selesai.
Kalau stok di situs bilang "tersedia" tapi lot belum lolos, itu kesalahan D1 — bukan D2.

### Rincian tiap langkah

| # | Langkah | Pemicu | Yang dikerjakan | Bukti (berkas) | Batas waktu |
| --- | --- | --- | --- | --- | --- |
| 1 | Cek stok lot | Harian 15 menit | Hitung sisa green bean per SKU (kg → bungkus pakai yield) | `stok-lot.json` | setiap hari |
| 2 | Rencana batch | Senin pagi | Tentukan SKU + volume 1–3 kg; pilih satu SKU "uji" bila ada lot baru | catatan batch | Senin 09.00 |
| 3 | Brief ke mitra | Senin | Kirim: SKU, kg, profil sangrai, tenggat kemas | chat/WA ke Ais | Senin 10.00 |
| 4 | Sangrai | Sesuai jadwal Ais | Catat green kg, roasted kg, lama sangrai, first crack | `batch-qc.csv` (draf) | hari sangrai |
| 5 | Resting | 12–24 jam | Jangan dikemas; jangan dicicipi panas | — | minimal 12 jam |
| 6 | Cupping | H+1 | Skor 5 atribut (aroma, acidity, body, sweetness, aftertaste), tulis catatan rasa | `batch-qc.csv` | H+1, 30 mnt |
| 7 | Lolos | skor ≥ 83 | Kemas, cetak label dengan kode batch + tanggal sangrai | `brand/label-*.png` | H+2 |
| 8 | Tolak | skor < 83 | Tulis alasan spesifik (bukan "kurang enak"), putuskan sangrai ulang | `batch-qc.csv` | hari itu |
| 9 | Sinkron stok | setelah kemas | Ubah status SKU di `catalog.json` + `stok-lot.json` | papan: 0 selisih | hari itu |
| 10 | Evaluasi | Mingguan | Lihat tren skor & % tolak 4 minggu terakhir | papan bagian QC | Jumat |

**Format kode batch:** `NK-<KODE>-<YYMM>-<A|B|C>`
contoh `NK-IJN-2610-B` = Blue Mount Ijen, Oktober 2026, batch kedua bulan itu.
Kode ini dicetak di label, disebut di konten, dan dipakai saat pembeli komplain.

---

## 2. Ritme kerja

### Harian — 10 menit (setelah buka papan)
1. Baca bagian **Produksi — stok per SKU** di `dashboard/index.html`.
2. Ada SKU berstatus "terbatas" padahal sisa > 20 bungkus? Perbaiki statusnya.
3. Ada order yang menunggu varian berstatus "habis"? Beri tahu D2 hari itu.

### Mingguan — 120 menit
| Blok | Menit | Output |
| --- | --- | --- |
| Cek stok & rencana batch | 15 | daftar SKU yang disangrai minggu ini |
| Brief + koordinasi Ais | 10 | jadwal sangrai tertulis |
| Sangrai (hadir/telepon) | 45 | angka green/roasted kg |
| Cupping + isi `batch-qc.csv` | 30 | skor + catatan rasa |
| Kemas + label (`tools/brandkit.py`) | 20 | label bertanggal, kode batch |

### Bulanan — 45 menit
1. Rekap: batch tercatat, % ditolak, skor rata-rata (papan).
2. Bandingkan yield aktual vs asumsi 0,79 di `data/biaya.json` → kalau beda > 2 poin, koreksi HPP.
3. Pilih satu SKU untuk "uji lot baru" bulan depan.
4. Arsipkan label bulan lalu; simpan 2 bungkus per batch sebagai sampel (untuk komplain).

---

## 3. Target kerja 3 bulan

Diambil dari `data/divisi.json` → D1. Kolom "cara hitung" adalah yang dipakai papan.

| Ukuran | Nov 2026 | Des 2026 | Jan 2027 | Cara hitung | Arah |
| --- | --- | --- | --- | --- | --- |
| Batch tercatat | 4 | 6 | 8 | baris baru di `batch-qc.csv` per bulan | naik |
| Batch ditolak | ≤ 15% | ≤ 12% | ≤ 10% | batch ditolak ÷ batch tercatat | turun |
| Skor cupping rata-rata | 84 | 85 | 85 | rata-rata `skor_cupping` | naik |
| Selisih status stok situs | 0 | 0 | 0 | jumlah SKU yang statusnya beda dari hitungan lot | turun |

Target tambahan (tidak tampil sebagai kartu papan): yield ≥ 79% tiap bulan.
**Ambang tolak minimum:** skor 83. Ambang ini tidak diturunkan untuk mengejar target volume.

---

## 4. Definisi selesai

| Rentang | Selesai bila… |
| --- | --- |
| Satu batch | ada baris di `batch-qc.csv` + keputusan lolos/tolak + label tercetak (bila lolos) |
| Satu hari | tidak ada SKU dengan status situs yang berbeda dari hitungan lot |
| Satu minggu | minimal 1 batch baru tercatat; label bertanggal benar |
| Satu bulan | rekap QC dibuat; HPP di `biaya.json` disesuaikan bila yield melenceng |

## 5. Serah terima

| Ke | Apa | Kapan | Lewat |
| --- | --- | --- | --- |
| D2 | varian yang habis / siap kirim | segera setelah keputusan | WA internal + `catalog.json` |
| D4 | angka batch nyata (skor, kg, tanggal) untuk konten | saat cupping | `batch-qc.csv` |
| D5 | tanggal kemas + jumlah bungkus | setelah kemas | label + catatan batch |
| D6 | yield & HPP aktual | bulanan | `biaya.json` |

## 6. Jebakan yang sudah terbukti

1. **Mencicipi kopi yang masih panas.** Rasa manis belum muncul; batch bagus bisa terlihat gagal.
2. **Menurunkan ambang karena stok kosong.** Lebih baik menolak order daripada mengirim batch 81.
3. **Mengetik stok tanpa mengecek lot.** Papan akan menandai selisih; jangan dimatikan alarmnya.
4. **Mengemas sebelum resting 12 jam.** Valve bisa menggelembung dan label jadi basah.
5. **Menyebut "kami menyangrai sendiri".** Itu klaim palsu dan merusak kepercayaan yang jadi modal utama kami.
