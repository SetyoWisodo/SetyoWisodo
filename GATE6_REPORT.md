# GATE 6 — Laporan Produksi

**Buku:** *Surviving the Future: Crisis, Climate, and Human Resilience* (EN) / edisi Indonesia (ID)
**Tanggal:** 22 Oktober 2026 · **Status gate:** **berjalan — tipografi dan metadata selesai; deduplikasi ID belum tuntas**

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
| P7 | Panjang buku dalam rentang yang diminta | 400–500 hlm | **403 (EN) / 422 (ID)** |
| P8 | Tidak ada duplikasi isi antarparagraf | 0 pasangan skor ≥ 5,0 | **7 (EN) / 19 (ID)** — **belum tuntas** |
| P9 | Aparatus bersih setelah semua penyuntingan | 0 masalah | **422 EN / 376 ID, 0** |

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
| Pasangan skor ≥ 6,0 | 16 | **0** | 23 | **2** |
| Pasangan skor ≥ 5,0 | 28 | **7** | 37 | **19** |
| Pasangan skor ≥ 3,2 | 121 | **95** | 155 | **125** |

Daftar sisa tersimpan di `DEDUP_STATUS.txt` untuk pekerjaan lanjutan.

### 2.5 Tabel yang terpotong halaman

Sebelum gate ini, tabel yang tidak muat pada sisa halaman dipindahkan seluruhnya ke halaman berikutnya, yang meninggalkan ruang kosong hingga 20 cm di dasar halaman. Tabel yang lebih tinggi daripada satu halaman penuh akan terpotong tanpa peringatan.

`draw_table` kini memecah tabel pada batas baris, mengulang baris header di halaman lanjutan, dan hanya memindahkan tabel bila header ditambah dua baris data tidak muat. Hasilnya terlihat pada Tabel 2.1 edisi Indonesia, yang kini dimulai di dasar halaman 38 dan berlanjut di halaman 39 dengan header yang diulang. Rata-rata ruang kosong di dasar halaman turun dari 29 halaman bermasalah menjadi 25 di EN dan 36 menjadi 29 di ID; sisanya adalah halaman penutup bab, yang memang berakhir lebih pendek karena bab berikutnya dimulai di halaman baru.

### 2.6 Margin panjang

Karena EN hanya 401 halaman pada pemeriksaan pertama — satu halaman di atas ambang — tiga lapisan pendalaman tambahan (`depth_zp` … `depth_zr`, EN dan ID) menambah sekitar 1.500 kata per edisi pada bab 2, 5, 6, 12, 13, 15, dan 19: beda stok dan aliran, defisit adaptasi dan klausul peninjauan standar, serah terima antara respons sukarela dan sistem formal, serta uji "tahun kering ketiga" untuk rencana air. EN kini 403 halaman dan ID 422, sehingga penyuntingan kecil tidak akan menjatuhkan EN di bawah 400.

---

## 3. Hasil pemeriksaan produksi

`audit_production.py` (alat baru) memeriksa kedua PDF secara menyeluruh:

| Butir | EN | ID |
|---|---|---|
| Halaman | **403** | **422** |
| Ukuran berkas | 2,22 MB | 2,02 MB |
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
| `check_citations.py` | 422 EN / 376 ID, **0 masalah** |
| `fact_check.py` | **0 gagal** |
| `data_consistency.py` | 2 kandidat EN / 2 ID (keduanya rasio yang disengaja) |
| Kata | **199.554 EN / 165.854 ID** |

---

## 4. Keterbatasan dan pekerjaan yang belum selesai

1. **Deduplikasi ID belum tuntas.** 19 pasangan masih berskor ≥ 5,0 (2 di antaranya ≥ 6,0). Penyebabnya bukan terjemahan yang tertinggal, melainkan modul ID yang ditulis terpisah dari modul EN, sehingga perbaikan paragraf EN tidak otomatis memperbaiki padanannya. Daftar kerjanya ada di `DEDUP_STATUS.txt`.
2. **7 pasangan EN yang berskor ≥ 5,0** sebagian besar sudah komplementer (satu paragraf memberi angka, yang lain memberi kerangka), bukan duplikasi. Dua di antaranya masih layak disunting: §17.8 (kolera Haiti/Yaman) dan §21.12 (skenario keadilan).
3. **Tingkat 3,2–5,0 belum disisir.** 94 pasangan EN / 125 ID pada ambang itu adalah campuran duplikasi ringan dan kesamaan topik yang wajar; penyisiran manual membutuhkan pemeriksaan satu per satu.
4. **Berkas terbit belum dibangun ulang.** `book/publish/` masih memuat build lama (19 bab, 149 halaman) dari pipeline Typst yang membutuhkan `typst` dan `pandoc`; pipeline itu tidak tersedia di lingkungan ini. PDF A4 401/419 halaman adalah hasil yang harus dipakai.

---

## 5. Keputusan

Metadata, outline, tipografi, kata pengantar, dan deduplikasi EN **selesai dan terverifikasi**. Gate 6 belum dapat dinyatakan lulus penuh karena deduplikasi edisi Indonesia baru sekitar 60 % selesai. Pekerjaan berikutnya: menyisir 19 pasangan ID yang tersisa, merapikan tujuh paragraf Ahr yang berulang di §22.7 dan §18.11 EN, memeriksa ulang §17.8 dan §21.12 EN, lalu menutup gate.
