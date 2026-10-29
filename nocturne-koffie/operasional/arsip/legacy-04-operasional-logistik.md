# D4 · Operasional & Logistik

**Tujuan:** paket sampai dalam kondisi utuh, dengan resi hari yang sama.
**Pemilik:** owner · **Alat:** `data/pesanan.csv`.

---

## 1. SOP packing (7 langkah, 4 menit/paket)

| # | Langkah | Cek |
| --- | --- | --- |
| 1 | Cocokkan order dengan papan (produk, ukuran, gilingan, qty) | salah gilingan = retur |
| 2 | Timbang kopi sesuai ukuran (toleransi ±2 g) | timbangan digital |
| 3 | Tutup valve, tekan keluar udara, segel | valve tidak boleh terlipat |
| 4 | Tempel label: tanggal sangrai + kode batch | wajib, bukan opsional |
| 5 | Bubble wrap 1 lapis + kardus | aman untuk 1–3 bungkus |
| 6 | Sisipkan kartu ucapan bila diminta | catat di kolom `catatan` |
| 7 | Foto paket + resi sebelum diserahkan ke kurir | bukti kalau ada sengketa |

---

## 2. Ongkir (aturan, bukan tebakan)

| Zona | Contoh | Estimasi | Catatan |
| --- | --- | --- | --- |
| Banyuwangi kota | COD / ambil | Rp 0–10.000 | bisa same-day |
| Jawa Timur | Surabaya, Malang | Rp 15.000–20.000 | 1–2 hari |
| Jawa | Jakarta, Bandung | Rp 20.000–28.000 | 2–3 hari |
| Luar Jawa | Makassar, Medan | Rp 30.000–45.000 | 3–5 hari |

**Aturan:** gratis ongkir hanya (a) di marketplace, atau (b) minimum belanja Rp 150.000,
atau (c) area Banyuwangi. Order 100 g senilai Rp23.000 tidak boleh gratis ongkir — habis oleh ongkir.

---

## 3. Pengiriman

1. Kirim **hari yang sama** untuk order sebelum 15.00 WIB (Senin–Sabtu).
2. Resi dikirim ke pembeli hari itu juga; status di `pesanan.csv` → `dikirim`.
3. Bila paket > 3 hari tidak bergerak, proaktif kabari pembeli (jangan tunggu ditanya).
4. Paket hilang/rusak: ganti sesuai kebijakan garansi, catat sebagai biaya operasional.

---

## 4. Retur & komplain

| Jenis | Tindakan |
| --- | --- |
| Salah gilingan / salah produk | Ganti, biaya kita |
| Kemasan rusak / bocor | Ganti, minta foto |
| Rasa tidak cocok | **Bukan** alasan penggantian; bantu carikan metode/profil lain |
| Batch terbukti gagal (ada catatan QC) | Ganti + catat batch di laporan |

Semua komplain dicatat di `pesanan.csv` kolom `catatan` — supaya pola terlihat.

---

## 5. Opname mingguan (Sabtu, 15 menit)

| Barang | Cara cek |
| --- | --- |
| Kemasan 100/250/500/1 kg | hitung sisa; habis = order tertahan |
| Stiker label | cukup untuk 2 minggu? |
| Bubble wrap & kardus | cukup untuk 20 paket? |
| Kopi roasted belum terjual | cocokkan dengan papan; kalau > 10 hari, prioritaskan |

---

## 6. KPI divisi

| KPI | Target |
| --- | --- |
| Order dikirim hari yang sama | ≥ 90% |
| Resi terkirim hari itu | 100% |
| Salah kirim | 0 |
| Komplain kemasan | < 3% |
| Stok kemasan habis tanpa peringatan | 0 |
