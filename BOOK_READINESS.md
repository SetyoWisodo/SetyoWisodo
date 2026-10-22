# Kesiapan Edar — Penilaian dan Perbaikan

**Buku:** *Surviving the Future* (EN) / *Bertahan Hidup di Masa Depan* (ID)
**Tanggal penilaian:** 23 Oktober 2026 · **Status:** siap cetak dan siap unggah, dengan empat keputusan pemilik yang tersisa (lihat §4)

---

## 1. Ringkasan penilaian

Dinilai dari sudut pandang penerbit yang menerima paket ini untuk diterbitkan, bukan dari sudut pandang penulis.

| Dimensi | Sebelum putaran ini | Sesudah | Catatan |
|---|---|---|---|
| Isi dan struktur | 9,0 | **9,0** | 24 bab, 25 tabel, 24 studi kasus, semua bab punya Case Study + Future Scenarios bernomor |
| Penyuntingan bahasa | 8,0 | **8,0** | Lolos semua pemeriksaan otomatis; proofread manusia tetap perlu |
| Tipografi dan tata letak | 6,5 | **9,0** | Kepala halaman berjalan, margin cermin, pembuka bab bertingkat, folio tepi luar, indent gantung |
| Halaman depan dan belakang | 5,5 | **8,5** | Halaman hak cipta, lampiran A–D, Daftar Pustaka, Indeks, Tentang Penulis |
| Indeks | 6,0 | **7,5** | 90 istilah, judul huruf, rentang halaman, *passim*, rujukan "lihat juga"; belum ada subentri |
| Ebook (EPUB 3) | 6,5 | **8,5** | Metadata lengkap, aksesibilitas, *landmarks*, `th scope`, lolos `audit_epub.py` |
| Dokumen sunting (DOCX) | 6,0 | **8,5** | A4, margin cermin, gaya Heading, TOC field, nomor halaman, kepala berjalan |
| Kesiapan cetak | 6,0 | **8,5** | Bleed, punggung terhitung, zona barcode, 300 dpi; belum PDF/X dan belum CMYK |
| Kesiapan jual | 4,0 | **5,5** | Belum ada ISBN, harga, identitas penerbit, dan metadata ritel |

**Nilai keseluruhan: 8,3/10.** Buku ini sudah berada di atas ambang "layak diterbitkan"; yang tersisa bukan perbaikan naskah, melainkan keputusan penerbitan yang hanya bisa diambil pemilik.

---

## 2. Yang diperbaiki di putaran ini

### 2.1 Halaman depan

- **Halaman hak cipta** (hal. 2) yang sebelumnya tidak ada sama sekali: pernyataan hak cipta, larangan memperbanyak, **disclaimer** (buku ini bukan nasihat medis/hukum/keuangan/teknik), kredit sampul, dan keterangan tipografi. Nomor ISBN otomatis tercetak bila diisi (`ISBN` di `book_pdf.py`).
- **Baris penerbit** di kaki halaman judul.

### 2.2 Tipografi cetak

- **Kepala halaman berjalan**: verso = judul buku, recto = judul bab, ditekan pada halaman pembuka bab, halaman judul, dan halaman hak cipta. Sebelumnya tidak ada sama sekali pada 425 halaman.
- **Margin cermin**: dalam 34 mm, luar 26 mm. Lebar kolom tetap 150 mm sehingga tidak ada reflow, hanya pergeseran blok — persis yang dibutuhkan buku jilid 1 inci.
- **Folio di tepi luar** (kanan di recto, kiri di verso) dan tetap **tengah bawah** di halaman pembuka bab, sesuai permintaan semula.
- **Pembuka bab** kini bertingkat: nomor bab berhuruf jarak, judul 19 pt, lalu tema sebagai epigraf italik di tengah.
- **Indent gantung** untuk Daftar Pustaka dan Indeks.
- **Perbaikan bug pengukuran**: lebar kata diukur pada 12 pt walau teksnya disetel 10,5 pt, sehingga Indeks dan Daftar Pustaka tampak berjarak renggang. Kini ukuran huruf aktif dipakai.

### 2.3 Halaman belakang

- Lampiran disusun ulang menjadi urutan terbit: **A** Ceklis, **B** Glosarium, **C** Catatan Analitis, **D** Catatan Sumber Peristiwa, lalu **Daftar Pustaka**, **Indeks**, dan **Tentang Penulis** — dua yang terakhir tanpa huruf lampiran, sebagaimana lazim.
- **"Extended Analytical Notes" yang berisi lima kalimat generik diganti** dengan enam **catatan analitis** yang spesifik dan bertaut ke bab: estimasi vs hitungan kematian panas, makna atribusi, penghitungan ganda pengungsi, perdebatan literatur konflik, neraca pangan nasional, dan ketergantungan estimasi kerugian pada tingkat diskonto.
- **Tentang Penulis** dipindah ke halaman terakhir dan ditulis ulang (dua paragraf, tanpa klaim yang tidak dapat diverifikasi).

### 2.4 Indeks

Sebelumnya: 88 istilah dengan daftar halaman mentah dan "et passim" (penggunaan Latin yang salah). Sekarang: 90 istilah, **judul huruf A–Z**, **rentang halaman** (41–43, bukan 41, 42, 43), ***passim*** untuk topik yang tersebar, **sembilan rujukan "lihat juga"**, dan indent gantung.

### 2.5 EPUB 3

- Halaman **judul** dan **hak cipta** di dalam spine (sebelumnya langsung ke daftar isi).
- Metadata: `dc:publisher`, `dc:rights`, `dc:date`, `dc:description`, tiga `dc:subject` (BISAC), dan enam properti aksesibilitas (`schema:accessMode`, `accessibilityFeature`, `accessibilityHazard`, `accessibilitySummary`).
- `<nav epub:type="landmarks">`, `properties="nav"` pada item nav, `properties="cover-image"` pada sampul — dua hal yang wajib di EPUB 3 dan sebelumnya tidak ada.
- `scope="col"` pada semua kepala tabel, atribut bahasa pada setiap berkas XHTML.
- **`audit_epub.py`** (baru): pemeriksa struktur pengganti `epubcheck` — mimetype, container, manifest/spine, tautan dan anchor, nav vs NCX, well-formedness. Kedua edisi **bersih**.

### 2.6 DOCX

A4 dengan margin cermin, kepala halaman ganjil/genap, nomor halaman otomatis (field PAGE), **daftar isi otomatis (field TOC)**, gaya Heading 1–3 Times New Roman sehingga panel navigasi Word berfungsi, kepala tabel berulang di 25 tabel, properti dokumen, dan bahasa `en-GB`/`id-ID`.

### 2.7 Sampul cetak

- **Zona barcode ritel** 2 × 1,2 inci di kanan-bawah sampul belakang (0,35 inci dari tepi trim) dibiarkan kosong — syarat KDP/IngramSpark. Blok bio penulis menyempit agar tidak menabrak zona itu.
- Punggung dihitung ulang dari halaman sebenarnya: **1,062 inci (EN, 425 hlm)** dan **1,093 inci (ID, 437 hlm)**.
- `build_report.json` kini juga mencatat `barcode_area_in`.

---

## 3. Angka terbit sekarang

| | EN | ID |
|---|---|---|
| Halaman A4 | **425** | **437** |
| Kata (`wc -w`) | **200.023** | **166.515** |
| Sitasi dalam teks | 402 | 350 |
| Karya dikutip / total rujukan | 130 / 145 | 124 / 145 |
| Tabel | 25 | 25 |
| Entri outline PDF | 327 | 327 |
| Istilah indeks | 90 | 90 |
| EPUB | 42 berkas, 32 bab | 42 berkas, 32 bab |
| DOCX | 2.803 paragraf, 25 tabel | 2.806 paragraf, 25 tabel |
| Sampul | 17,85 × 11,94 in, punggung 1,062 in | 17,88 × 11,94 in, punggung 1,093 in |

Pemeriksaan: `check_citations` 0 masalah · `fact_check` 0 gagal · `audit_production` bersih (kedua PDF) · `audit_redundancy` 0 pasangan ≥ 5,0 · `audit_epub` bersih (kedua EPUB).

---

## 4. Yang harus Anda kerjakan sendiri (tidak bisa saya lakukan di sini)

Diurutkan dari yang paling menghambat penerbitan.

| # | Hal | Kenapa tidak bisa saya kerjakan | Cara |
|---|---|---|---|
| 1 | **ISBN 13 digit** | Harus dibeli/didaftarkan atas nama penerbit; saya tidak boleh mengarang nomor | Beli di Perpusnas/ISBN Indonesia atau pakai ISBN gratis KDP. Isi `ISBN` di `book_pdf.py`, lalu render ulang; nomor itu otomatis masuk halaman hak cipta |
| 2 | **Identitas penerbit** | Saya memakai "Setyo Wisodo" sebagai penerbit agar berkas tidak kosong; nama imprint adalah keputusan Anda | Ubah `COPY["en"|"id"]["published"]` di `book_pdf.py` dan `publisher` di `make_publish.py` |
| 3 | **Harga dan metadata ritel** | Keputusan komersial | KDP: harga, kategori (3 BISAC), 7 kata kunci, deskripsi toko, A+ content |
| 4 | **Barcode EAN-13** | Dibuat penerbit dari ISBN | KDP/IngramSpark menaruhnya otomatis di zona kosong yang sudah disediakan |
| 5 | **Proofread manusia** | Pemeriksaan otomatis tidak menangkap selera bahasa, idiom, dan konsistensi istilah | Satu editor bahasa Inggris + satu Indonesia, fokus Bab 1–5 dan 24 |
| 6 | **Review indeks profesional** | Indeks saya dihasilkan otomatis dari 90 istilah; indeks berbayar punya 250+ entri dengan subentri | Indexer lepas, atau tambah subentri manual untuk 20 istilah utama |
| 7 | **Uji cetak (proof copy)** | Tebal punggung bergantung pada jenis kertas printer | Pesan satu eksemplar; rumus saya 0,0025 in/halaman (kertas krem). Kertas putih 0,002252 in/halaman → punggung 0,957 in (EN) |
| 8 | **Keputusan trim A4** | A4 tidak lazim untuk non-fiksi dagang (umumnya 6×9 in) | Bila ingin 6×9, seluruh pipeline harus dirender ulang; beri tahu saya dan saya kerjakan |
| 9 | **Izin kutipan** | Kutipan tokoh (Mann, Otto, Rockström, Ghosh) sebaiknya diperiksa dari sisi hak kutip | Cek fair-use/kutipan singkat; dokumentasikan sumber di Catatan Sumber Peristiwa |
| 10 | **Hak atas sampul** | Gambar sampul dibuat AI | Pastikan lisensi/atribusi sesuai platform; pertimbangkan desainer sampul profesional |
| 11 | **`epubcheck` resmi** | Butuh Java, tidak tersedia di lingkungan ini | Jalankan `epubcheck` sekali di komputer Anda sebelum unggah; `audit_epub.py` sudah menyaring kesalahan struktural |
| 12 | **PDF/X untuk offset** | Renderer tidak menghasilkan CMYK/PDF-X | Bila cetak offset (bukan POD), minta percetakan mengonversi; untuk KDP file sekarang sudah memadai |

---

## 5. Checklist unggah (KDP paperback)

1. Isi ISBN → `python render_book.py && python render_book_id.py` → `python make_publish.py && python make_cover.py`.
2. Unggah `book/publish/*_interior.pdf` sebagai interior dan `*_cover_print.pdf` sebagai sampul bungkus.
3. Pilih ukuran trim A4 (8,27 × 11,69 in) — pastikan tersedia di printer yang dipakai; bila tidak, keputusan #8 berlaku.
4. Periksa pratinjau KDP: punggung, garis potong, dan zona barcode.
5. Unggah `*_cover_front.jpg` untuk versi ebook dan `*.epub` sebagai interior ebook.
6. Isi kategori dan kata kunci; jalankan pratinjau EPUB di KDP (Kindle Previewer) untuk memastikan tabel tidak terpotong di layar kecil.

---

## 6. Yang saya sarankan sebagai langkah berikutnya (opsional, bukan penghambat)

1. **8–12 gambar data.** Buku ini punya 25 tabel dan **nol gambar**. Untuk non-fiksi dagang, satu grafik per bab besar akan menaikkan daya jual lebih dari apa pun yang tersisa. Bisa saya kerjakan dari angka yang sudah ada di tabel.
2. **Subentri indeks** untuk 20 istilah utama (Adaptation, Flood, Heatwave, Food security, …).
3. **Trim 6×9 in** bila menyasar pasar buku dagang internasional.
4. **Halaman dedikasi/epigraf** di halaman depan (satu halaman, keputusan penulis).
