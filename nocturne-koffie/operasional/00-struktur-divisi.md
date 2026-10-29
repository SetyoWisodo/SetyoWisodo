# Struktur Divisi — Nocturne Koffie Brand

Dokumen ini bukan teori organisasi. Isinya **siapa memutuskan apa, kapan, dan dengan bukti apa**.
Semua divisi dijalankan dari satu papan: `python3 tools/papan.py` → `dashboard/index.html`.

> Sebutan resmi: Nocturne adalah **brand kopi**. Sangrai dieksekusi **Ais Coffee Roastery**.
> Di dokumen internal, "produksi" berarti rantai: pilih biji → sangrai (mitra) → QC → kemas.

**Alur kerja & target lengkap tiap divisi ada di satu berkas per divisi:**
[`divisi/`](divisi/) → `D1-produksi-qc.md` … `D7-brand-legal.md`.
Target angkanya hidup di `data/divisi.json` — bukan di dokumen.

---

## 1. Tujuh divisi

| # | Divisi | Inti tugas | Pemilik awal | Alat / berkas |
| --- | --- | --- | --- | --- |
| D1 | **Produksi & QC** | Pilih green bean, jadwalkan sangrai, cicipi tiap batch, putuskan lolos/tolak, catat batch | Owner + mitra Ais | `data/batch-qc.csv`, `data/stok-lot.json` |
| D2 | **Penjualan & CRM** | Balas WhatsApp, konfirmasi order, follow-up, langganan, pipeline B2B | Owner | `data/pesanan.csv`, `komersial/pipeline-b2b.csv` |
| D3 | **Marketing & Pertumbuhan** | Pilih & jadwalkan konten, tulis caption, kelola marketplace & kampanye, ukur hasil | Owner dibantu agent | `data/konten-14hari.csv`, `data/kpi.csv` |
| D4 | **Kreatif & Media** | Rekam klip mentah, render aset (video/carousel/story), jaga standar visual | Owner (rekam) + agent (aset) | `tools/kreatif.py`, `data/kreatif.json`, `konten/` |
| D5 | **Operasional & Logistik** | Packing, ongkir, kirim, resi, retur, opname kemasan | Owner | `data/pesanan.csv` |
| D6 | **Keuangan** | Catat kas, hitung HPP & margin, jaga harga, break-even | Owner | `data/biaya.json`, papan |
| D7 | **Brand & Legal** | Konsistensi klaim, aset brand, dokumen usaha, izin petani & mitra | Owner | `data/legal.json`, brief 11.8 |

**Kenapa D3 dan D4 dipisah.** Sebelumnya satu divisi "Marketing & Konten" mengerjakan dua hal yang
berbeda jenis pekerjaan: *membuat* aset (keterampilan produksi visual) dan *mendistribusikan* aset
(keterampilan memilih kanal, menulis, mengukur). Digabung, salah satunya selalu dikorbankan —
biasanya pengukuran. Pemisahan ini juga membuat beban "rekam" (15 menit saat produksi) terpisah
dari beban "jadwalkan & ukur" (90 menit/minggu).

Satu orang boleh memegang beberapa divisi — yang **tidak boleh** adalah satu orang memegang
D1 dan D2 tanpa pemisahan peran saat memutuskan **batch ditolak**. Kalau batch ditolak,
keputusan berhenti di D1; D2 hanya menerima kabar "stok varian ini kosong minggu ini".

---

## 2. Hak memutuskan (RACI ringkas)

| Keputusan | Diputuskan | Dikonsultasi | Diberi tahu |
| --- | --- | --- | --- |
| Batch dikirim atau disangrai ulang | D1 | Mitra Ais | D2 (stok), D4 (bahan konten) |
| Harga jual & diskon | D6 + owner | D1 (biaya), D3 (persepsi) | semua |
| Produk ditambah / dipensiunkan | owner | D1, D6 | D2, D3, D4 |
| Status stok di situs | D1 | D5 | D2 |
| Order diterima / ditolak (stok habis) | D2 | D1 | D5 |
| Ongkir & kurir | D5 | D2 | — |
| Aset mana yang tayang | D3 | D7 | D4 |
| Standar visual & format aset | D4 | D7 | D3 |
| Klaim di situs, IG, marketplace | D7 | D3, D4 | semua |
| Nama petani tayang | D7 | D1 | D3, D4 |
| Anggaran iklan | owner | D6 | D3 |

---

## 3. Ritme kerja (total ±15 jam/minggu + 25 menit/hari)

### Harian — 25 menit, jam 08.30

| Menit | Kegiatan | Divisi |
| --- | --- | --- |
| 0–5 | Buka papan harian: baca "Perlu keputusan hari ini" + tabel **Target divisi** | owner |
| 5–15 | Balas WhatsApp, konfirmasi order, kirim resi | D2 |
| 15–20 | Cek stok SKU berstatus terbatas; perbarui kalau berubah | D1 |
| 20–25 | Cek konten hari ini; kalau kosong, ambil 1 aset siap dari `konten/` | D3 |

### Mingguan

| Hari | Blok | Divisi | Output |
| --- | --- | --- | --- |
| Senin | 60 mnt sangrai + catat batch | D1 | Baris baru di `batch-qc.csv` |
| Selasa | 90 mnt konten: pilih aset, tulis caption, jadwalkan | D3 | 7 aset terjadwal |
| Rabu | 30 mnt pipeline B2B (5 pesan baru / follow-up) | D2 | Update `pipeline-b2b.csv` |
| Kamis | 30 mnt cupping + gerbang klaim aset minggu depan | D1 → D7 | Status SKU akurat, aset lolos/ditahan |
| Jumat | 30 mnt keuangan: kas, margin, tagihan | D6 | Baris KPI minggu ini |
| Sabtu | 40 mnt packing + kirim + opname kemasan | D5 | Semua order terkirim |
| Sabtu | 20 mnt render aset minggu depan (`tools/kreatif.py`) | D4 | `data/kreatif.json` diperbarui |
| Minggu | 30 mnt review papan + rencana minggu depan | owner | 3 prioritas minggu depan |

### Bulanan

1. Tutup buku: omzet, HPP, laba kotor, biaya tetap, laba bersih (D6).
2. Evaluasi harga: bandingkan margin tiap ukuran (D6 + papan).
3. Perbarui `data/legal.json` dan cek masa berlaku izin (D7).
4. Tinjau 3 konten dengan performa terbaik → ulangi formatnya (D3).
5. Hitung aset siap vs terpakai; kurangi render bila > 40% tidak terpakai (D4).

---

## 4. Target divisi — cara membacanya

Tabel **Target divisi** di papan menjawab satu pertanyaan: *apakah divisi ini berjalan sesuai rencana bulan ini?*
Isinya datang dari dua tempat:

| Kolom | Sumber |
| --- | --- |
| Target | `data/divisi.json` → `kpi[].target[bulan_ke]` (Nov 2026 / Des 2026 / Jan 2027) |
| Aktual | dihitung `tools/papan.py` dari `pesanan.csv`, `batch-qc.csv`, `konten-14hari.csv`, `kpi.csv`, `kreatif.json`, `legal.json`, `biaya.json` |
| Status | `tercapai` / `di bawah` / `tanpa data` |

Ringkasan target 3 bulan (detail per divisi ada di masing-masing berkas):

| Divisi | Ukuran utama | Nov 2026 | Des 2026 | Jan 2027 |
| --- | --- | --- | --- | --- |
| D1 | Batch tercatat / skor min | 4 / 84 | 6 / 85 | 8 / 85 |
| D2 | Order retail / AOV | 25 / Rp130rb | 50 / Rp145rb | 85 / Rp155rb |
| D3 | Konten terbit / chat WA | 16 / 40 | 20 / 100 | 24 / 180 |
| D4 | Video jadi / aset siap | 8 / 12 | 12 / 18 | 16 / 24 |
| D5 | Kirim hari sama | 85% | 90% | 95% |
| D6 | Omzet / margin terburuk | Rp3,2 jt / 35% | Rp7,2 jt / 38% | Rp13,2 jt / 40% |
| D7 | Dokumen legal selesai | 5 | 7 | 8 |

**Aturan:** papan tidak boleh memuat angka yang tidak berasal dari berkas.
Kalau angka salah, perbaiki berkasnya, bukan papannya.

---

## 5. Cara memakai papan harian

```bash
python3 tools/papan.py              # tanggal hari ini
python3 tools/papan.py --tanggal 2026-11-03
python3 tools/papan.py --json       # ringkasan untuk skrip lain
```

Papan membaca 9 berkas dan menghitung sendiri:

| Bagian papan | Sumber data | Yang diputuskan dari situ |
| --- | --- | --- |
| Perlu keputusan hari ini | semua | urutan kerja hari ini (kritis dulu) |
| **Target divisi** | `divisi.json` + semua | divisi mana yang tertinggal bulan ini |
| Tujuh divisi | hitungan | siapa yang harus bergerak |
| Jadwal konten | `konten-14hari.csv` | posting atau tayangkan aset siap |
| Aset siap tayang | `kreatif.json` | aset mana yang belum dijadwalkan |
| Pesanan perlu diproses | `pesanan.csv` | kirim, tagih, atau follow-up |
| Stok per SKU | `stok-lot.json` + katalog | perbarui status di situs |
| Margin & break-even | `biaya.json` + katalog | ubah harga atau ubah ukuran |
| QC batch | `batch-qc.csv` | batch lolos / sangrai ulang |
| Legal | `legal.json` | apa yang menahan kampanye besar |

---

## 6. Eskalasi

| Keadaan | Tindakan | Batas waktu |
| --- | --- | --- |
| Batch ditolak | Tunda pengiriman varian itu, kabari pembeli yang sudah order | hari yang sama |
| Stok habis padahal situs "tersedia" | Ubah status di `catalog.json` + tawarkan produk serupa | hari yang sama |
| Pembeli komplain rasa | Tanya metode seduh & gilingan; minta kode batch; ganti hanya jika batch terbukti gagal | 1×24 jam |
| Chat belum dibalas > 6 jam | Prioritaskan; potensi closing turun tajam | segera |
| Klaim di konten melanggar brief 11.8 | Hapus/revisi dalam 1 jam; catat penyebabnya | 1 jam |
| Aset dirender dengan data yang salah | Tarik aset, perbaiki berkas sumber, render ulang | hari yang sama |
| Mitra sangrai tidak bisa produksi | Aktifkan mitra cadangan (jangan diumumkan di situs) | 3 hari |

---

## 7. Yang tidak boleh dilakukan divisi mana pun

1. Menyebut Nocturne sebagai roastery, atau mengklaim menyangrai sendiri.
2. Menjanjikan hal yang belum diputuskan (diskon member, tanggal lot, gratis ongkir).
3. Memberi diskon pada harga satuan — insentif hanya bonus produk atau ongkir.
4. Mempublikasikan foto petani atau titik lokasi kebun tanpa izin tertulis.
5. Mengubah harga di satu tempat tanpa mengubah `data/biaya.json` dan papan.
6. Menayangkan aset yang belum lewat gerbang klaim D7.
7. Mengetik angka target di dokumen — target hanya di `data/divisi.json`.
