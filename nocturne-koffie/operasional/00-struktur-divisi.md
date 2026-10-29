# Struktur Divisi — Nocturne Koffie Brand

Dokumen ini bukan teori organisasi. Isinya **siapa memutuskan apa, kapan, dan dengan bukti apa**.
Semua divisi dijalankan dari satu papan: jalankan `python3 tools/papan.py`, buka `dashboard/index.html`.

> Sebutan resmi: Nocturne adalah **brand kopi**. Sangrai dieksekusi **Ais Coffee Roastery**.
> Di dokumen internal, "produksi" berarti rantai: pilih biji → sangrai (mitra) → QC → kemas.

---

## 1. Enam divisi

| # | Divisi | Inti tugas | Pemilik awal | Alat |
| --- | --- | --- | --- | --- |
| D1 | **Produksi & QC** | Pilih green bean, jadwalkan sangrai, cicipi tiap batch, putuskan lolos/tolak, catat batch | Owner + mitra Ais | `data/batch-qc.csv`, `data/stok-lot.json` |
| D2 | **Penjualan & CRM** | Balas WhatsApp, konfirmasi order, follow-up, langganan, pipeline B2B | Owner | `data/pesanan.csv`, `marketing/04-*` |
| D3 | **Marketing & Konten** | Rekam aset saat produksi, jadwalkan 4 IG + 3 TikTok/minggu, kelola marketplace | Owner dibantu agent | `data/konten-14hari.csv`, `marketing/01-*` |
| D4 | **Operasional & Logistik** | Packing, hitung ongkir, kirim, resi, retur, opname kemasan | Owner | `data/pesanan.csv` |
| D5 | **Keuangan** | Catat kas, hitung HPP & margin, jaga harga, break-even | Owner | `data/biaya.json`, `dashboard` |
| D6 | **Brand & Legal** | Konsistensi klaim, aset brand, dokumen usaha, izin petani & mitra | Owner | `data/legal.json`, brief 11.8 |

Satu orang boleh memegang beberapa divisi — yang **tidak boleh** adalah satu orang memegang
D1 dan D2 tanpa pemisahan peran saat memutuskan **batch ditolak**. Kalau batch ditolak,
keputusan berhenti di D1; D2 hanya menerima kabar "stok varian ini kosong minggu ini".

---

## 2. Hak memutuskan (RACI ringkas)

| Keputusan | Diputuskan | Dikonsultasi | Diberi tahu |
| --- | --- | --- | --- |
| Batch dikirim atau disangrai ulang | D1 | Mitra Ais | D2 (stok), D3 (konten) |
| Harga jual & diskon | D5 + owner | D1 (biaya), D3 (persepsi) | semua |
| Produk ditambah / dipensiunkan | owner | D1, D5 | D2, D3 |
| Status stok di situs | D1 | D4 | D2 |
| Order diterima / ditolak (stok habis) | D2 | D1 | D4 |
| Ongkir & kurir | D4 | D2 | — |
| Klaim di situs, IG, marketplace | D6 | D3 | semua |
| Nama petani tayang | D6 | D1 | D3 |
| Anggaran iklan | owner | D5 | D3 |

---

## 3. Ritme kerja (total ±7 jam/minggu + 25 menit/hari)

### Harian — 25 menit, jam 08.30

| Menit | Kegiatan | Divisi |
| --- | --- | --- |
| 0–5 | Buka papan harian, baca bagian "Perlu keputusan hari ini" | owner |
| 5–15 | Balas WhatsApp, konfirmasi order, kirim resi | D2 |
| 15–20 | Cek stok SKU yang berstatus terbatas; perbarui kalau berubah | D1 |
| 20–25 | Cek konten hari ini; kalau kosong, ambil 1 klip saat produksi | D3 |

### Mingguan

| Hari | Blok | Divisi | Output |
| --- | --- | --- | --- |
| Senin | 60 mnt sangrai + catat batch | D1 | Baris baru di `batch-qc.csv` |
| Selasa | 90 mnt batch konten (rekam + jadwalkan) | D3 | 7 post terjadwal |
| Rabu | 30 mnt pipeline B2B (5 pesan baru / follow-up) | D2 | Update pipeline |
| Kamis | 30 mnt cupping + update stok situs | D1 | Status SKU akurat |
| Jumat | 30 mnt keuangan: kas, margin, tagihan | D5 | Baris KPI minggu ini |
| Sabtu | 40 mnt packing + kirim + opname kemasan | D4 | Semua order terkirim |
| Minggu | 30 mnt review papan + rencana minggu depan | owner | 3 prioritas minggu depan |

### Bulanan

1. Tutup buku: omzet, HPP, laba kotor, biaya tetap, laba bersih.
2. Evaluasi harga: bandingkan margin tiap ukuran (papan bagian Keuangan).
3. Perbarui `data/legal.json` dan cek masa berlaku izin.
4. Tinjau 3 konten dengan performa terbaik → ulangi formatnya.

---

## 4. Cara memakai papan harian

```bash
python3 tools/papan.py              # tanggal hari ini
python3 tools/papan.py --tanggal 2026-11-03
```

Papan membaca 7 berkas data dan menghitung sendiri:

| Bagian papan | Sumber data | Yang diputuskan dari situ |
| --- | --- | --- |
| Perlu keputusan hari ini | semua | Urutan kerja hari ini (kritis dulu) |
| Enam divisi | hitungan | Siapa yang harus bergerak |
| Jadwal konten | `konten-14hari.csv` | Posting atau rekam hari ini |
| Pesanan perlu diproses | `pesanan.csv` | Kirim, tagih, atau follow-up |
| Stok per SKU | `stok-lot.json` + katalog | Perbarui status di situs |
| Margin & break-even | `biaya.json` + katalog | Ubah harga atau ubah ukuran |
| QC batch | `batch-qc.csv` | Batch lolos / ulang |
| Legal | `legal.json` | Apa yang menahan kampanye besar |

**Aturan:** papan tidak boleh memuat angka yang tidak berasal dari berkas. Kalau angka salah,
perbaiki berkasnya, bukan papannya.

---

## 5. Eskalasi

| Keadaan | Tindakan | Batas waktu |
| --- | --- | --- |
| Batch ditolak | Tunda pengiriman varian itu, kabari pembeli yang sudah order | hari yang sama |
| Stok habis padahal situs "tersedia" | Ubah status di `catalog.json` + tawarkan produk serupa | hari yang sama |
| Pembeli komplain rasa | Tanya metode seduh & gilingan; tawarkan panduan; penggantian hanya jika batch terbukti gagal | 1×24 jam |
| Chat belum dibalas > 6 jam | Prioritaskan; potensi closing turun tajam | segera |
| Klaim di konten melanggar aturan brief 11.8 | Hapus/revisi dalam 1 jam | 1 jam |
| Mitra sangrai tidak bisa produksi | Aktifkan mitra cadangan (jangan diumumkan di situs) | 3 hari |

---

## 6. Yang tidak boleh dilakukan divisi mana pun

1. Menyebut Nocturne sebagai roastery, atau mengklaim menyangrai sendiri.
2. Menjanjikan hal yang belum diputuskan (diskon member, tanggal lot, gratis ongkir).
3. Memberi diskon pada harga satuan — insentif hanya bonus produk atau ongkir.
4. Mempublikasikan foto petani atau titik lokasi kebun.
5. Mengubah harga di satu tempat tanpa mengubah `data/biaya.json` dan papan.
