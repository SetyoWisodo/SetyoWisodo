# D2 · Penjualan & CRM — alur kerja & target

> **Mandat:** setiap chat berubah jadi order, setiap order jadi pelanggan yang kembali.
> **Pemilik:** owner · **Waktu:** 15 menit/hari + 60 menit/minggu.
> **Berkas kerja:** `data/pesanan.csv` · `data/katalog.json` → `data/catalog.json` · `komersial/pipeline-b2b.csv` · `marketing/04-whatsapp-crm-dan-b2b.md`.
> **Target & KPI:** `data/divisi.json` (D2).

D2 tidak memproduksi apa pun dan tidak membuat konten. D2 **mengubah perhatian menjadi uang**,
lalu mencatatnya supaya D6 bisa menghitung.

---

## 1. Alur kerja inti — dari chat ke pelanggan yang kembali

```
[1] Chat masuk (WA / IG DM / marketplace)
        │
        ▼
[2] Balas < 2 jam ─── pertanyaan wajib: produk? ukuran? gilingan? kota?
        │
        ├── tidak yakin ──► [3a] Kirim 3 pertanyaan penyaring (rasa, alat, budget)
        │
        ▼
[4] Kirim harga + stok + ongkir → tanya alamat & metode bayar
        │
        ▼
[5] Konfirmasi & minta bukti bayar ──► catat baris di pesanan.csv (status: dibayar)
        │
        ▼
[6] Serahkan ke D5 (packing & kirim) → kirim resi ke pembeli
        │
        ▼
[7] H+3: tanya "sudah dicoba?"  → H+21: tawarkan restock
        │
        ▼
[8] Minta kode batch + metode seduh bila ada komplain → eskalasi ke D1
```

### Naskah wajib (disalin, jangan dikarang ulang)

| Tahap | Kalimat | Kenapa |
| --- | --- | --- |
| Sapaan | "Halo, terima kasih sudah mampir. Mau saya bantu pilih kopi atau sudah ada yang dicari?" | membuka tanpa menekan |
| Penyaring | "Biasanya seduh pakai apa — V60, tubruk, moka pot, atau espresso? Sudah punya grinder?" | gilingan menentukan kepuasan |
| Stok jujur | "Untuk [SKU] batch terbaru tanggal [tgl]. Kalau mau yang lebih segar, sangrai berikutnya [tgl]." | kesegaran jadi alasan, bukan diskon |
| Penutup | "Saya kirim hari ini kalau sebelum jam 15.00. Resi saya kabari di chat ini." | janji yang bisa dicek |
| Restock | "Biasanya 250 g habis dalam 2–3 minggu. Mau saya siapkan [SKU] untuk tanggal [tgl]?" | tanpa diskon |

**Dilarang:** "promo", "buruan", "stok terbatas!!", memberi diskon satuan tanpa persetujuan D6.

---

## 2. Ritme kerja

### Harian — 15 menit (pagi 08.30, sore 16.00)
| Menit | Kegiatan | Bukti |
| --- | --- | --- |
| 0–8 | Balas semua chat; prioritas yang sudah tanya harga | semua chat terbaca |
| 8–12 | Update status order: `dibayar` / `dikirim` / `selesai` | `pesanan.csv` |
| 12–15 | Cek papan: "pesanan perlu diproses" & "restock jatuh tempo" | 0 order menggantung |

### Mingguan — 60 menit
1. **20 mnt** — susun 5 pesan B2B baru (kafe/resto/kantor) → `komersial/pipeline-b2b.csv`.
2. **15 mnt** — follow-up semua pipeline yang tanggalnya sudah lewat.
3. **15 mnt** — sapa 5 pembeli lama (bukan broadcast; sebut produk yang mereka beli).
4. **10 mnt** — isi baris KPI minggu ini di `data/kpi.csv` (order, omzet, AOV, langganan, B2B, chat).

### Bulanan — 40 menit
1. Hitung repeat rate: pembeli yang order ≥ 2× ÷ total pembeli.
2. Evaluasi AOV: kalau < target, dorong paket (Peta Rasa) dan ukuran 250 g, bukan diskon.
3. Tinjau 3 keberatan yang paling sering muncul → kirim ke D3 untuk dijadikan konten edukasi.
4. Cek pipeline: berapa yang jadi akun, berapa yang mati, dan alasannya.

---

## 3. Alur khusus — penawaran B2B (kafe/resto/kantor)

```
[1] Kualifikasi (5 menit): jenis usaha, kg/bulan, cara seduh, siapa pemutus
        │
        ▼
[2] Kirim komersial/penawaran-b2b.html + harga tier (5/10/20/30 kg)
        │
        ▼
[3] Sampel 2 × 250 g (dibayar, bukan gratis) → catat di pipeline
        │
        ▼
[4] Cupping bersama / feedback tertulis ≤ 14 hari
        │
        ▼
[5] Penawaran harga sesuai tier + termin → kesepakatan tertulis (WA cukup, isi 4 poin)
        │
        ▼
[6] Order pertama = uji: 5 kg. Bila lolos, baru 10 kg ke atas
```

**Pagar harga (dari `komersial/harga-grosir.csv`):** harga grosir tidak boleh di bawah HPP ÷ (1 − margin tier);
diskon satuan dilarang; ongkir grosir ditanggung pembeli atau dihitung ke harga.
Kalau calon minta harga di bawah tier 30 kg untuk volume 5 kg → jawab "tidak", tawarkan paket lebih kecil.

---

## 4. Target kerja 3 bulan

Dari `data/divisi.json` → D2.

| Ukuran | Nov 2026 | Des 2026 | Jan 2027 | Cara hitung | Arah |
| --- | --- | --- | --- | --- | --- |
| Order retail | 25 | 50 | 85 | baris `pesanan.csv` per bulan (tanpa batal) | naik |
| Nilai order rata-rata | Rp130.000 | Rp145.000 | Rp155.000 | omzet ÷ jumlah order | naik |
| Langganan aktif | 3 | 10 | 20 | pelanggan dengan siklus berjalan | naik |
| Akun B2B aktif | 1 | 2 | 4 | baris pipeline berstatus `aktif`/`deal` | naik |

Pendukung (dipantau, tidak dikartukan): repeat rate 15% → 25% → 35%; balas < 2 jam ≥ 90%.

## 5. Definisi selesai & kriteria gagal

| Rentang | Selesai bila… | Gagal bila… |
| --- | --- | --- |
| Satu chat | pelanggan tahu harga, stok, ongkir, dan tanggal kirim | tidak dibalas > 6 jam di jam kerja |
| Satu order | ada baris di `pesanan.csv` dengan status & total benar | order dikirim tanpa tercatat |
| Satu minggu | baris KPI terisi; 5 prospek B2B dihubungi | pipeline kosong 2 minggu berturut-turut |
| Satu bulan | target order & AOV dievaluasi dengan angka | target diganti di tengah bulan tanpa alasan |

## 6. Serah terima

| Dari | Kepada | Apa |
| --- | --- | --- |
| D1 | D2 | status stok & tanggal batch (jangan pernah diubah sendiri oleh D2) |
| D2 | D5 | order `dibayar` + alamat + ekspedisi yang diminta |
| D2 | D6 | omzet harian & biaya kirim aktual |
| D2 | D3 | keberatan pelanggan yang berulang → jadi bahan konten |
| D2 | D7 | keluhan yang menyangkut klaim/izin (mis. nama petani) |

## 7. Jebakan

1. **Menjanjikan stok yang belum lolos QC.** Selalu cek papan sebelum menjawab "tersedia".
2. **Menawar harga sendiri.** Satu diskon hari ini = harga baru selamanya di mata pembeli.
3. **Menumpuk chat lalu membalas borongan.** Waktu balas adalah bagian dari produk.
4. **Mencatat order "nanti saja".** Order tanpa baris = omzet yang tidak bisa dihitung D6.
5. **Memberi sampel gratis ke banyak kafe.** Sampel dibayar; yang gratis tidak dihargai.
