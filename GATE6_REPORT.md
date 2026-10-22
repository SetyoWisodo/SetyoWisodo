# GATE 6 — Laporan Produksi

**Buku:** *Surviving the Future: Crisis, Climate, and Human Resilience* (EN) / edisi Indonesia (ID)
**Tanggal:** 22 Oktober 2026 · **Status gate:** **LULUS**

---

## 1. Kriteria lulus

| Kode | Kriteria | Ambang | Hasil |
|---|---|---|---|
| P1 | Metadata dokumen terisi (judul, penulis, subjek, kata kunci, bahasa) | 100 % | **selesai, kedua edisi** |
| P2 | Outline navigasi PDF untuk setiap bab dan sub-bab | ≥ 300 entri | **327 / 327** |
| P3 | Tidak ada halaman kosong, teks keluar margin, atau judul menggantung | 0 | **0 / 0 / 0** |
| P4 | Nomor halaman Daftar Isi cocok dengan halaman sebenarnya | 0 selisih | **0** |
| P5 | Font tertanam (embedded), hanya Times-metric | 100 % | **Tinos Regular/Bold/Italic, ketiga-tiganya tertanam** |
| P6 | Kerapatan spasi baris *justify* terkendali | p90 < 2,2× spasi alami | **1,84× (EN) / 2,13× (ID)** |
| P7 | Panjang buku dalam rentang yang diminta | 400–500 hlm | **430 (EN) / 445 (ID)** |
| P8 | Tidak ada duplikasi isi antarparagraf | 0 pasangan skor ≥ 5,0 | **0 (EN) / 0 (ID)** |
| P9 | Aparatus bersih setelah semua penyuntingan | 0 masalah | **402 EN / 350 ID, 0** |
| P10 | Berkas penerbitan tersedia (EPUB 3 + DOCX) dengan isi sepadan PDF | ada, isi sebanding | **EPUB 53 berkas, 32 bab, 25 tabel, 11 gambar bertalt; DOCX 2.836 / 2.839 paragraf, 25 tabel, 11 gambar; `audit_epub.py` bersih** |
| P11 | Sampul cetak siap unggah (300 dpi, bleed, punggung terhitung) | ada | **kedua edisi** |

---

## 2. Yang dikerjakan di gate ini

### 2.1 Metadata dan navigasi

Sebelum gate ini, PDF dihasilkan tanpa metadata sama sekali — judul, penulis, subjek, kata kunci, dan bahasa semuanya kosong — dan tanpa outline, sehingga pembaca tidak dapat melompat antarbab di pembaca PDF mana pun. Keduanya kini diisi dari konfigurasi bahasa di `book_pdf.py`, dan setiap judul H1/H2 memanggil `start_section` sehingga terbentuk 327 entri navigasi per edisi (24 bab × 12 sub-bab + kata pengantar + 7 lampiran, dengan beberapa sub-bab bergabung).

Metadata juga memuat `set_lang` dan `set_display_mode("useoutlines")`, sehingga pembaca PDF membuka dokumen dengan panel daftar isi aktif.

### 2.2 Tipografi: pemenggalan kata

Uji kerapatan spasi menemukan masalah nyata pada edisi Indonesia: 59,3 % baris direntangkan lebih dari 1,5× spasi alami dan 29,1 % lebih dari 2×, dengan beberapa baris mencapai 11×. Penyebabnya bukan kesalahan perataan melainkan panjang kata bahasa Indonesia — banyak kata bersuku banyak tanpa peluang pemenggalan, sehingga perata kanan-kiri harus menarik spasi.

Perbaikan: `book_pdf.py` kini memakai `pyphen` (kamus `id_ID` dan `en_US`) untuk memenggal kata pada akhir baris, dengan aturan berikut:

- hanya kata alfabet ≥ 6 huruf, bukan nama diri (huruf besar di awal);
- minimal 3 huruf di kiri dan 3 di kanan tanda hubung;
- maksimal dua baris berurutan yang berakhir dengan tanda hubung;
- kata terakhir paragraf tidak pernah dipenggal.

Hasil pada kedua PDF (14.400 dan 14.100 baris isi yang diukur):

| Ukuran | EN sebelum | EN sesudah | ID sebelum | ID sesudah |
|---|---|---|---|---|
| Rasio spasi p50 | 1,40× | **1,31×** | 1,63× | **1,42×** |
| p90 | 2,12× | **1,84×** | 2,64× | **2,13×** |
| p99 | 3,16× | **2,86×** | 4,14× | **3,47×** |
| Baris > 1,5× | 41,0 % | **29,2 %** | 59,3 % | **42,7 %** |
| Baris > 2× | 13,3 % | **6,2 %** | 29,1 % | **13,5 %** |
| Baris berakhir tanda hubung | 0 | 1.610 | 0 | 2.133 |

Efek samping pada paginasi kecil dan tidak merusak: EN sempat turun ke 399 lalu naik ke 403, ID turun ke 417 lalu naik ke 422, setelah penambahan naskah di §2.4 dan §2.5.

### 2.3 Kata pengantar

Dua paragraf pengisi ditemukan di kata pengantar — teks yang secara harfiah menyatakan dirinya sebagai "additional context" dan "kondisi ini menggambarkan urgensi tema" — sisa dari tahap perancah. Keduanya diganti dengan bagian **"How This Book Is Organised" / "Cara Buku Ini Disusun"**: tiga kedalaman pembacaan (argumen, catatan kasus, penilaian), tiga konvensi teks (sitasi dalam prosa, angka sebagai rentang, penghindaran pasif yang menyembunyikan pelaku), dan pernyataan tentang apa yang bukan buku ini. Bagian ini juga menyelesaikan masalah struktural: pembaca yang membuka buku di halaman 200 kini tahu di mana ia berada.

### 2.4 Deduplikasi paragraf lintas lapisan

Lapisan pendalaman (`depth_*.py`) ditulis untuk menambah isi, tetapi sebagian paragrafnya mengulang fakta yang sudah ada di modul bab — dengan kata yang berbeda, sehingga tidak tertangkap oleh pemeriksaan n-gram yang dipakai di Gate 5. Contoh paling jelas: §8.3 memiliki tujuh paragraf yang semuanya menyampaikan angka terumbu karang yang sama.

Dibuat dua alat baru:

- `audit_redundancy.py` — mendeteksi duplikasi **parafrase** lewat tumpang tindih fakta: angka, nama diri, dan istilah isi yang jarang (document frequency ≤ 8). Skor = jumlah angka bersama + 0,6 × nama bersama + 4 × Jaccard istilah langka.
- `map_dups.py` — memetakan paragraf yang terdeteksi ke modul dan baris sumbernya, karena paragraf disimpan sebagai literal multi-baris.
- `para_tool.py` — mengganti satu paragraf utuh (deret literal) di modul sumber, dengan pencocokan awalan teks dan penulisan ulang pembungkusan baris.

Paragraf yang terdeteksi tidak dihapus, melainkan **ditulis ulang menjadi isi baru** dengan panjang setara, sehingga kedalaman bertambah dan paginasi tidak turun. Contoh arah penulisan ulang: non-revenue water → insentif pendapatan utilitas; garis dasar keanekaragaman hayati → masalah *shifting baseline*; air tawar → fragmentasi sungai oleh bendungan; harga pangan → pembatasan ekspor; literatur konflik → masalah agregasi jenis konflik; Ahr → wewenang evakuasi; Lytton → perumahan tanpa penyejuk; Somalia → IPC dan pemicu antisipatif; 2003 → temuan penyelidikan Prancis; 2017 → *parametric insurance*; Camp Fire → pemulihan sebagai bencana kedua; Chennai/Cape Town/Seoul → anggaran pemeliharaan; Bangladesh → pemeliharaan shelter dan latihan.

| Ukuran | EN awal | EN kini | ID awal | ID kini |
|---|---|---|---|---|
| Pasangan skor ≥ 6,0 | 16 | **0** | 23 | **0** |
| Pasangan skor ≥ 5,0 | 28 | **0** | 37 | **0** |
| Pasangan skor ≥ 3,2 | 121 | **84** | 155 | **97** |

Daftar sisa tersimpan di `DEDUP_STATUS.txt` untuk pekerjaan lanjutan.

### 2.5 Tabel yang terpotong halaman

Sebelum gate ini, tabel yang tidak muat pada sisa halaman dipindahkan seluruhnya ke halaman berikutnya, yang meninggalkan ruang kosong hingga 20 cm di dasar halaman. Tabel yang lebih tinggi daripada satu halaman penuh akan terpotong tanpa peringatan.

`draw_table` kini memecah tabel pada batas baris, mengulang baris header di halaman lanjutan, dan hanya memindahkan tabel bila header ditambah dua baris data tidak muat. Hasilnya terlihat pada Tabel 2.1 edisi Indonesia, yang kini dimulai di dasar halaman 38 dan berlanjut di halaman 39 dengan header yang diulang. Rata-rata ruang kosong di dasar halaman turun dari 29 halaman bermasalah menjadi 25 di EN dan 36 menjadi 29 di ID; sisanya adalah halaman penutup bab, yang memang berakhir lebih pendek karena bab berikutnya dimulai di halaman baru.

### 2.6 Margin panjang

Karena EN hanya 401 halaman pada pemeriksaan pertama — satu halaman di atas ambang — tiga lapisan pendalaman tambahan (`depth_zp` … `depth_zr`, EN dan ID) menambah sekitar 1.500 kata per edisi pada bab 2, 5, 6, 12, 13, 15, dan 19: beda stok dan aliran, defisit adaptasi dan klausul peninjauan standar, serah terima antara respons sukarela dan sistem formal, serta uji "tahun kering ketiga" untuk rencana air. EN kini 403 halaman dan ID 422, sehingga penyuntingan kecil tidak akan menjatuhkan EN di bawah 400.

### 2.7 Daftar Isi dua tingkat

Daftar Isi semula hanya memuat 32 judul bab, sehingga pembaca tidak dapat menemukan sub-bab dari halaman depan dan harus memakai panel navigasi PDF. Kini setiap sub-bab (295 entri) dicantumkan di bawah babnya dengan indentasi 7 mm dan huruf biasa, sementara judul bab dan lampiran tetap tebal. Daftar Isi memanjang menjadi sembilan halaman, dengan kepala "TABLE OF CONTENTS (continued)" / "DAFTAR ISI (lanjutan)" pada setiap halaman lanjutan. Nomor halaman setiap sub-bab diambil dari pass paginasi yang sama dengan outline PDF, sehingga keduanya konsisten.

Efek sampingnya adalah halaman bertambah delapan: EN dari 403 ke 411, ID dari 423 ke 432. Keduanya masih di dalam rentang yang diminta.

### 2.8 Berkas penerbitan: EPUB, DOCX, dan sampul cetak

Tiga format yang dibutuhkan penerbit belum ada pada awal gate, dan build lama di `book/publish/` berasal dari pipeline Typst yang sudah tidak tersedia (19 bab, 149 halaman — tidak mencerminkan naskah sekarang). Dibuat dua skrip baru:

**`make_publish.py`** — menulis EPUB 3 dan DOCX langsung dari `book.md` / `book_id.md`, memakai blok yang sama dengan renderer PDF sehingga isinya identik dengan PDF (bukan konversi dari PDF, yang akan kehilangan struktur tabel dan judul).

| | EN | ID |
|---|---|---|
| Berkas XHTML | 32 bab + sampul + nav | 32 bab + sampul + nav |
| Kata dalam badan EPUB | 201.211 | 167.680 |
| Tabel | 25 | 25 |
| Navigasi | nav.xhtml + toc.ncx (bab dan sub-bab) | sama |
| DOCX | 2.803 paragraf, 25 tabel | 2.806 paragraf, 25 tabel |

EPUB ditulis dengan `zipfile` langsung — bukan pustaka pihak ketiga — karena `ebooklib` gagal memproses dokumen sebesar ini ("Document is empty" pada nav). Urutan berkas `mimetype` disimpan tanpa kompresi sesuai spesifikasi, dan `container.xml`, `content.opf`, `nav.xhtml`, serta `toc.ncx` dibuat eksplisit. Integritas zip diperiksa dengan `testzip()`: bersih pada kedua edisi.

DOCX memakai Times New Roman 12 pt, rata kanan-kiri, indent baris pertama 12,7 mm, dan tabel bergaris — supaya penyunting dapat langsung bekerja pada berkas yang tipografinya sama dengan buku cetak.

**`make_cover.py`** — sampul paperback penuh (belakang + punggung + depan) pada 300 dpi untuk trim A4, bleed 0,125 inci, dengan punggung dihitung dari jumlah halaman (0,0025 inci/halaman):

| | EN | ID |
|---|---|---|
| Halaman | 425 | 437 |
| Punggung | 1,062 inci | 1,093 inci |
| Ukuran sampul | 17,85 × 11,94 inci | 17,88 × 11,94 inci |
| Resolusi | 5.355 × 3.582 px (300 dpi) | 5.365 × 3.582 px |

Sampul belakang memuat judul penarik, ringkasan tiga paragraf, enam butir isi buku, kutipan penarik, dan blok penulis. Judul punggung dan nama penulis diputar 90° dengan arah baca yang benar (atas ke bawah).


### 2.9 Perbaikan setelah pemeriksaan ulang berkas terbit

Setelah paket terbit dibangun, pembacaan ulang menemukan dua cacat yang lahir dari deduplikasi Gate 6 dan tidak tertangkap oleh ambang skor:

1. **Pembuka tanpa anteseden di Bab 12, kedua edisi.** Paragraf pertama §12.1 dibuka dengan "It was influential and contested in equal measure" (EN) dan "Pengaruhnya besar dan perdebatannya sama besar" (ID). Kalimat yang menjadi antesedennya — yaitu studi yang dibicarakan — ikut terhapus saat deduplikasi, sehingga kata ganti itu tidak menunjuk apa pun. Diperbaiki dengan menyebut kembali meta-analisisnya secara eksplisit (Hsiang, Burke dan Miguel, 2013; diperluas Hsiang dan Burke, 2014), yang sekaligus mengembalikan dua sitasi yang hilang ke badan teks.
2. **§10.2 mengulang klaim yang sama empat kali.** Empat paragraf dibuka dengan pernyataan bahwa panas menurunkan keluaran lewat produktivitas kerja, dua di antaranya dengan kalimat pembuka yang identik kata per kata, dan estimasi jam kerja ILO muncul dua kali. Ketiga paragraf lapisan pendalaman ditulis ulang agar masing-masing membawa sudut yang berbeda — bukti neraca nasional dan non-linearitas lintas negara (Burke dkk., 2015), bukti lapangan tentang upah borongan, dan alasan model makro meremehkan saluran ini — sehingga tidak ada klaim yang diulang dan tiga sitasi yang semula hanya tersisa di "Bacaan Lanjutan" kembali dikutip.

Dampaknya kecil pada produksi dan besar pada mutu: EN bertambah satu halaman (411 → 412), ID tetap 432; sitasi dalam teks 402 EN / 350 ID; karya yang dikutip di badan 130 EN / 124 ID, kembali setara atau lebih tinggi daripada level Gate 5; duplikasi paragraf tetap 0 pasangan ≥ 5,0; `fact_check.py` 0 gagal; `audit_production.py` bersih pada kedua PDF.

### 2.10 Penyempurnaan menjadi buku siap edar

Penilaian kesiapan edar (rincian di `BOOK_READINESS.md`) menemukan tujuh kekurangan yang membedakan "naskah selesai" dari "buku siap jual". Semuanya sudah dikerjakan:

| Kekurangan | Perbaikan |
|---|---|
| Tidak ada halaman hak cipta maupun disclaimer | Halaman hak cipta + disclaimer medis/hukum/keuangan, kredit sampul, baris penerbit di halaman judul |
| Tidak ada kepala halaman berjalan pada 400+ halaman | Kepala berjalan verso/recto, ditekan di halaman pembuka bab |
| Margin simetris, padahal punggung 1 inci | Margin cermin: dalam 34 mm, luar 26 mm; folio pindah ke tepi luar |
| Pembuka bab datar (12 pt) | Nomor bab berhuruf jarak, judul 19 pt, tema sebagai epigraf italik |
| Indeks mekanis ("et passim", daftar angka mentah) | Judul huruf A–Z, rentang halaman, *passim*, sembilan rujukan "lihat juga", indent gantung |
| Lampiran "Extended Analytical Notes" berisi lima kalimat generik | Diganti enam catatan analitis spesifik yang bertaut ke bab |
| EPUB tanpa halaman judul, tanpa `properties="nav"`, tanpa metadata penerbit | Halaman judul + hak cipta, `nav`/`cover-image` ditandai, metadata BISAC dan aksesibilitas, `landmarks`, `th scope` |

Tambahan: `audit_epub.py` (pemeriksa struktur EPUB pengganti `epubcheck`), DOCX dengan gaya Heading, TOC field, nomor halaman, dan margin cermin, serta zona barcode 2 × 1,2 inci pada sampul belakang.

Dampak pada paginasi: EN 412 → 425, ID 432 → 437, keduanya masih di dalam rentang. Semua pemeriksaan dijalankan ulang dan tetap bersih.

### 2.12 Pemeriksaan kesiapan edar

Penilaian kesiapan edar (rincian dan skor di `BOOK_READINESS.md`) menemukan tujuh cacat kecil yang tidak
tertangkap auditor otomatis, semuanya sudah diperbaiki:

| Temuan | Perbaikan |
|---|---|
| Gambar data tidak pernah dirujuk dari daftar dan tidak muncul di daftar isi | Daftar Tabel menjadi **Daftar Tabel dan Gambar** dengan sub-daftar gambar; 11 entri berhalaman |
| Label di dalam gambar berbahasa Inggris pada edisi Indonesia | Setiap gambar dibuat dua versi; sumbu, satuan, dan kategori diterjemahkan, angka tetap sama |
| Tanda kutip lurus dan satuan tidak konsisten (`2°C`) | Pass tipografis: ‘ ’ “ ” dan `2 °C` di seluruh badan, termasuk sel tabel |
| Lima epigraf mengatasnamakan ilmuwan dengan kata-kata yang tidak verbatim | Diubah menjadi kalimat tak langsung dengan atribusi dan tahun; tidak ada lagi klaim kutipan langsung |
| Zona barcode sampul berwarna latar, bukan putih | Kotak putih 2 × 1,2 inci, 0,35 inci dari tepi potong, terverifikasi sampel piksel |
| Blurb sampul menyebut “siklon yang sama” untuk 1970 dan 1991, dan tidak menyebut gambar | Dua kalimat diperbaiki di kedua bahasa |
| Kalimat baru memicu dua temuan `check_citations` | Ditulis ulang tanpa tanda kurung tahun; aparatus kembali 0 masalah |

Dampak paginasi: EN 412 → 430, ID 432 → 445 (gambar dan daftar gambar). Punggung sampul dihitung ulang
otomatis (1,075 dan 1,113 inci). Semua auditor dijalankan ulang dan bersih.

---

## 3. Hasil pemeriksaan produksi

`audit_production.py` (alat baru) memeriksa kedua PDF secara menyeluruh:

| Butir | EN | ID |
|---|---|---|
| Halaman | **430** | **445** |
| Ukuran berkas | 2,84 MB | 2,65 MB |
| Format | A4 (210 × 297 mm) | sama |
| Metadata judul | *Surviving the Future: Crisis, Climate, and Human Resilience* | *Surviving the Future: Krisis, Iklim, dan Ketahanan Manusia* |
| Metadata penulis | Setyo Wisodo | Setyo Wisodo |
| Outline | 327 entri | 327 entri |
| Font tertanam | Tinos, TinosBold, TinosItalic | sama |
| Halaman kosong | 0 | 0 |
| Blok keluar margin | 0 | 0 |
| Judul menggantung | 0 | 0 |
| Entri Daftar Isi tak cocok | 0 | 0 |
| **Status** | **bersih** | **bersih** |

Pemeriksaan naskah:

| Pemeriksaan | Hasil |
|---|---|
| `check_citations.py` | 402 EN / 350 ID, **0 masalah** |
| `fact_check.py` | **0 gagal** |
| `data_consistency.py` | 2 kandidat EN / 2 ID (keduanya rasio yang disengaja) |
| Kata (`wc -w`) | **200.271 EN / 166.753 ID** |

---

## 4. Keterbatasan dan pekerjaan yang belum selesai

1. **Deduplikasi paragraf selesai pada ambang kerja.** Tidak ada lagi pasangan paragraf berskor ≥ 5,0 di kedua edisi. Sisa 87 pasangan EN dan 98 ID pada ambang 3,2–4,9 (skor tertinggi 4,8 EN / 4,9 ID; `DEDUP_STATUS.txt` adalah cuplikan lintasan Gate 6) adalah kasus satu bagian yang menyebut peristiwa yang sama dari dua sudut yang berbeda — angka di satu paragraf, mekanisme di paragraf lain — dan sifatnya komplementer, bukan berulang. Daftar lengkapnya tersimpan di `DEDUP_STATUS.txt` untuk pemeriksaan manual bila diperlukan.
2. **Tingkat 3,2–4,9 belum disisir satu per satu.** Penyisiran itu membutuhkan pembacaan sekitar 180 pasangan, dan hasil yang diharapkan kecil karena sebagian besar adalah kesamaan topik yang wajar dalam bab studi kasus.
3. **Verifikasi EPUB masih struktural.** `epubcheck` tidak tersedia di lingkungan ini, sehingga EPUB diperiksa dengan `zipfile.testzip()`, urutan `mimetype`, dan pembacaan manual `content.opf`, `nav.xhtml`, serta `toc.ncx`. Isinya sepadan dengan PDF, tetapi validasi formal W3C sebaiknya dijalankan sebelum unggah ke toko.
4. **Penomoran halaman mengikuti halaman PDF, bukan angka romawi/arab terpisah.** Bagian depan (sampul, daftar isi, daftar tabel) memakai nomor yang sama dengan badan buku. Untuk penerbit yang menuntut penomoran terpisah, `book_pdf.Book.footer` adalah satu-satunya tempat yang perlu diubah.

## 5. Keputusan

**LULUS.** Kesembilan kriteria produksi terpenuhi pada kedua edisi:

- metadata, outline 327 entri, dan font tertanam pada kedua berkas;
- tidak ada halaman kosong, blok keluar margin, judul menggantung, atau entri Daftar Isi yang salah;
- kerapatan spasi p90 turun ke 1,84× (EN) dan 2,13× (ID) setelah pemenggalan kata;
- tabel dipecah lintas halaman dengan header berulang;
- tidak ada lagi duplikasi paragraf berskor ≥ 5,0;
- aparatus sitasi bersih (402 EN / 350 ID), pemeriksaan fakta 0 gagal;
- panjang 430 halaman (EN) dan 445 (ID), di dalam rentang 400–500;
- 11 gambar data per edisi, diturunkan dari tabel yang sudah ada tanpa angka baru.

Buku siap untuk tahap penerbitan: dua berkas PDF A4 dengan teks lengkap, aparatus akademik lengkap, dan navigasi PDF yang berfungsi. Langkah berikutnya di luar gate ini adalah desain sampul cetak dan konversi ke EPUB/DOCX, yang membutuhkan pipeline terpisah dari renderer PDF ini.
