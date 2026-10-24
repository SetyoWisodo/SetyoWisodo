# Kesiapan Edar — Penilaian dan Daftar Perbaikan

**Buku:** *Surviving the Future: Crisis, Climate, and Human Resilience* (EN) / *Bertahan Hidup di Masa Depan* (ID)
**Tanggal penilaian:** 23 Oktober 2026 · **Status:** **siap edar dengan catatan** — 9,1 / 10
**Artefak yang dinilai:** `Surviving_the_Future.pdf` (430 hlm), `Surviving_the_Future_ID.pdf` (445 hlm),
EPUB, DOCX, sampul cetak, `build_report.json`

---

## 1. Skor

| Aspek | Bobot | Skor | Catatan |
|---|---|---|---|
| Isi dan struktur | 20 % | 9,5 | 24 bab; setiap bab punya Case Study dan Future Scenarios bernomor; 25 tabel; 11 gambar data |
| Penyuntingan dan konsistensi angka | 15 % | 9,0 | aparatus sitasi bersih; `fact_check` 0 gagal; 0 pasangan paragraf ≥ 5,0 |
| Tipografi dan tata letak cetak | 15 % | 9,5 | margin simetris 30 mm di setiap halaman, kepala berjalan terpusat, folio kanan-bawah (tengah pada pembuka bab), pemenggalan kata, tanda kutip tipografis, spasi satuan |
| Aparatus akademik | 15 % | 9,5 | 402/351 sitasi, daftar pustaka 145 entri, indeks A–Z dengan rentang halaman, *see also*, dan *passim* |
| Kelengkapan pra-cetak | 10 % | 8,0 | halaman judul + hak cipta + disclaimer ada; **ISBN belum ada**; belum ada halaman persembahan/ucapan terima kasih |
| Sampul dan kesiapan ritel | 10 % | 9,2 | seni generatif baru (krisis dan ketahanan dalam satu bingkai), dua rasio: potong A4 1800 × 2546 dan ebook 1600 × 2560; punggung terhitung otomatis, bleed 0,125 in, zona barcode putih 2 × 1,2 inci; **barcode EAN-13 belum ditempel** (menunggu ISBN) |
| EPUB | 7,5 % | 9,0 | 53 berkas, nav + NCX + landmarks, metadata aksesibilitas, 11 gambar bertalt; **belum divalidasi epubcheck** (butuh Java) |
| DOCX | 5 % | 9,0 | A4, margin simetris 30 mm, TNR 12 pt, gaya Heading, field TOC, kepala berjalan, 11 gambar dengan `descr` |
| Aksesibilitas | 2,5 % | 8,0 | EPUB punya ringkasan aksesibilitas; **PDF belum bertag** (tidak bisa lewat fpdf2) |
| **Total** | **100 %** | **9,1** | |

Angka 9,1 berarti: tidak ada cacat yang menghalangi penjualan, tetapi ada tiga hal yang hanya bisa
diselesaikan pemilik buku (ISBN, imprint/harga, izin kutipan) dan dua keterbatasan alat (epubcheck, PDF bertag).

---

## 2. Yang diperbaiki pada pass ini

| Temuan | Perbaikan | Bukti |
|---|---|---|
| 11 gambar data tidak pernah dirujuk dari prosa | Gambar ditempatkan tepat setelah tabel sumbernya, diberi caption, baris sumber, dan entri di **Daftar Gambar**; alasan pemilihan angka ditulis di `GATE6_REPORT.md` §2.11 | 11 gambar di kedua PDF, 11 entri Daftar Gambar |
| Daftar Tabel tidak memuat gambar | Judul menjadi **Daftar Tabel dan Gambar / List of Tables and Figures**, dengan sub-judul Daftar Gambar | p12–13 (EN), p13–14 (ID) |
| Label gambar berbahasa Inggris di edisi Indonesia | Setiap gambar dibuat dua kali (`figX_Y.png` dan `figX_Y_id.png`) dengan sumbu, satuan, dan kategori diterjemahkan; angka identik | `figures/*_id.png` |
| Tanda kutip lurus dan satuan `2°C` | Pass tipografis di `book_pdf.typographic()`: ‘ ’ “ ”, dan `2 °C` konsisten | 0 tanda kutip lurus di badan PDF |
| `angstrom`/`°C` campur pada tabel | Normalisasi yang sama berlaku untuk sel tabel | — |
| Kutipan langsung atas nama lima ilmuwan tanpa sumber verbatim | Diubah menjadi kalimat tak langsung dengan atribusi dan tahun — tidak ada lagi tanda kutip yang mengklaim kata-kata persis | hlm. 15 (EN), 15 (ID) |
| Zona barcode sampul berwarna sama dengan latar | Kotak putih 2 × 1,2 inci, 0,35 inci dari tepi potong | sampel piksel (255,255,255) |
| Blurb sampul tidak menyebut gambar dan salah menyebut “siklon yang sama” untuk 1970 dan 1991 | Diperbaiki di kedua bahasa | sampul belakang |
| Sampul lama terbaca sebagai buku tentang satu kawasan, bukan abad krisis | Sampul baru dari seni generatif: krisis dan ketahanan dalam satu bingkai, tipografi terpisah, kalimat penutup, kaki sampul bersih tanpa baris statistik; dua rasio keluaran | `book/publish/*_cover_front.jpg`, `*_cover_ebook.jpg` |
| Aparatus sitasi terganggu oleh tahun di dalam kalimat baru | Kalimat Hansen ditulis ulang tanpa tanda kurung tahun | `check_citations` 0 masalah |

### Angka akhir

| | EN | ID |
|---|---|---|
| Halaman | **430** | **445** |
| Kata (`wc -w`) | 200.271 | 166.753 |
| Sitasi dalam teks | 402 | 351 |
| Tabel / gambar | 25 / 11 | 25 / 11 |
| EPUB | 53 berkas | 53 berkas |
| DOCX | 2.836 paragraf, 25 tabel, 11 gambar | 2.839 paragraf, 25 tabel, 11 gambar |
| Punggung sampul | 1,075 inci | 1,113 inci |
| Ukuran sampul | 17,865 × 11,94 inci | 17,902 × 11,94 inci |

---

## 3. Yang harus Anda kerjakan sendiri (tidak bisa dikerjakan dari sini)

### 3.1 Wajib sebelum unggah

1. **ISBN.** Beli satu ISBN untuk versi cetak dan satu untuk EPUB (atau pakai ISBN gratis KDP — tetapi
   penerbitnya lalu tercatat “Independently published”). Setelah ada:
   - isi `ISBN = "978-…"` di `book_pdf.py` (baris 557) agar tercetak di halaman hak cipta;
   - letakkan barcode EAN-13 di kotak putih sampul belakang (2 × 1,2 inci; KDP menempelkannya otomatis
     bila Anda mengunggah sampul tanpa barcode).
2. **Nama penerbit/imprint.** Saat ini halaman judul berbunyi “Published by Setyo Wisodo”. Ganti bila Anda
   memakai imprint sendiri (`COPY[lang]["published"]` di `book_pdf.py`).
3. **Harga dan mata uang.** Tidak pernah tercetak di dalam buku; diisi di dasbor penjual.
4. **Izin kutipan.** Buku mengutip frasa pendek dari sumber akademik dan laporan (fair use untuk tinjauan),
   dan lima epigraf kini berupa kalimat tak langsung. Bila Anda mengembalikan kutipan langsung, verifikasi
   kata-katanya dari sumber asli dan simpan buktinya.
5. **Pemeriksaan hukum disclaimer.** Halaman hak cipta memuat disclaimer medis, hukum, keuangan, dan
   teknik. Untuk pasar tertentu (mis. Uni Eropa) minta tinjauan hukum singkat.
6. **Validasi EPUB.** Jalankan `epubcheck` (butuh Java) pada kedua berkas sebelum unggah:
   `java -jar epubcheck.jar book/publish/*.epub`. Audit internal sudah bersih, tetapi validasi W3C adalah
   syarat sebagian toko.

### 3.2 Sebaiknya

7. **Proof copy cetak.** Pesan satu salinan; periksa punggung, posisi folio, dan ketajaman gambar 300 dpi.
8. **Ukuran trim.** Buku ini A4 (210 × 297 mm). Untuk pasar non-fiksi dagang, 6 × 9 inci lebih lazim dan
   lebih murah dicetak. Mengubahnya berarti mengubah `Book` (format) + `make_cover.py` + render ulang.
9. **PDF bertag (PDF/UA).** fpdf2 belum menghasilkan PDF bertag; bila Anda menjual ke perpustakaan atau
   institusi yang menuntut aksesibilitas, ekspor ulang dari Word (DOCX sudah bergaya Heading).
10. **Halaman persembahan dan ucapan terima kasih.** Belum ada; tambahkan bila diinginkan.
11. **Rujukan gambar dari prosa.** Tabel dan gambar kini diletakkan di titik pembahasan tanpa kalimat
    penunjuk (“lihat Gambar 2.1”). Bila ingin gaya jurnal, tambahkan satu klausa di paragraf sebelum
    setiap tabel — 25 tempat per edisi.

---

## 4. Urutan unggah yang disarankan (KDP)

1. Isi ISBN di `book_pdf.py`, render ulang: `python render_book.py && python render_book_id.py`.
2. `cp Surviving_the_Future*.pdf book/publish/*_interior.pdf` (nama berkas lihat `book/README.md`).
3. `python make_publish.py` lalu `python make_cover.py` (punggung dihitung dari halaman sebenarnya).
4. Unggah `*_interior.pdf` dan `*_cover_print.pdf`; pilih 6 × 9 atau A4 sesuai keputusan Anda.
5. Unggah EPUB; jalankan pratinjau KDP dan periksa 11 gambar serta daftar isi.
6. Pesan proof; setujui setelah pemeriksaan fisik.

---

## 5. Ringkasan

Buku ini **sudah berada pada tahap siap edar**: tipografi cetak lengkap (margin simetris 30 mm, kepala
berjalan terpusat, folio kanan-bawah, pemenggalan kata, tanda kutip tipografis), aparatus akademik bersih, 25 tabel dan 11 gambar
data dalam dua bahasa, EPUB dan DOCX yang lolos audit, serta sampul dengan punggung terhitung dan zona
barcode. Yang tersisa bukan pekerjaan penyuntingan, melainkan data milik penerbit: ISBN, imprint, harga,
izin, dan validasi eksternal.
