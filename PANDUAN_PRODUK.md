# Panduan Unggah Gumroad — Layar demi Layar

Toko Anda: **setyowisodo.gumroad.com** · Halaman yang sedang terbuka: produk pertama (`/vbqmqo`), tab **Product** — masih kosong, ini yang pertama diisi.

**Status produk 1 (per 28 Oktober 2026):**

| Bagian | Status |
|---|---|
| Name | ✅ `Surviving the Future` |
| Description | ✅ terisi dan berformat |
| URL | ⬜ masih `surviving-thefuture` → ubah ke `surviving-the-future` |
| Cover (3 gambar) | ⬜ — berkas sudah diperbarui: 457 pages / 152 sources |
| Thumbnail + harga $45 | ⬜ |
| Content (4 berkas + stempel PDF) | ⬜ |
| Uji beli kode 100% | ⬜ |

> **Teks deskripsi tidak perlu dikarang.** Empat teks final sudah tersedia di halaman unduhan, bagian **Teks deskripsi siap tempel**: `/copy/en`, `/copy/id`, `/copy/bundle`, `/copy/sample`. Buka, tekan Ctrl+A, Ctrl+C, tempel ke kotak Description.
Semua isian di bawah sudah final. Ikuti berurutan; jangan lompat ke produk kedua sebelum produk pertama terbit dan diuji.

**Empat produk yang akan dibuat, dalam urutan ini:**

| # | Produk | Harga | Berkas isi |
|---|---|---|---|
| 1 | Surviving the Future (EN) | $45 | PDF + EPUB + DOCX + paket gambar |
| 2 | Free sample (EN) | $0 | 1 PDF sampel 35 hlm |
| 3 | Bertahan Hidup di Masa Depan (ID) | $29 | PDF + EPUB + DOCX + paket gambar |
| 4 | Bundle EN + ID | $59 | produk 1 + produk 3 |

---

# PRODUK 1 — Surviving the Future (EN, $45)

## Langkah 1 · Name

Sudah benar: `Surviving the Future`. **Jangan diubah** — ini yang muncul di judul halaman, struk, dan pustaka pembeli.

## Langkah 2 · Description

Kotak kosong besar itu yang paling menentukan penjualan. **Jangan tempel teks polos** — Gumroad membuang semua judul dan poin, hasilnya satu dinding paragraf.

**Cara yang benar:**

0. Kalau langkah 1–3 di bawah terasa rumit: buka **`DESKRIPSI_GUMROAD.md`** atau **`/copy/en-plain`**, salin semua teksnya, tempel ke kotak Description, selesai — tanpa menyentuh toolbar.

1. Buka **`/copy/en`** di halaman unduhan (tautan ada di panel *Live Preview* Arena, baris pertama "Teks deskripsi siap tempel"). Kalau panel itu tidak terbuka, buka berkas `book/publish/gumroad/copy/listing_en.html` dari salinan repo di komputer Anda.
2. Di halaman itu: **Ctrl+A**, lalu **Ctrl+C**.
3. Klik kotak **Description** di Gumroad, lalu **Ctrl+V**.

Yang ikut terbawa: subjudul, garis pemisah, daftar poin, tebal-miring. Kotak petunjuk abu-abu di atas tidak tersalin karena memang dikunci, dan baris judul besar sudah dibuang otomatis — judul produk sudah ada di kolom **Name**, tidak perlu diulang.

**Kalau hasil tempelannya berantakan:** tempel teks dari `listing_en.txt` per bagian, lalu rapikan dengan toolbar — dropdown **Text** → *Heading 2* untuk baris `WHAT MAKES THIS DIFFERENT`, `WHY $45`, dan seterusnya; tombol **bullet list** untuk baris berawalan `*`; sisanya biarkan *Paragraph*. Jangan pakai Heading 1: judul produk sudah ada di atas halaman.

**Setelah produk sampel terbit** (Langkah 20), kembali ke sini dan ganti teks `[link to your free sample product]` menjadi URL sampel.

## Langkah 3 · URL

Kolom URL sekarang berisi kode acak `vbqmqo`. Ganti menjadi:

```
surviving-the-future
```

Alamat lengkapnya menjadi `setyowisodo.gumroad.com/l/surviving-the-future`. Kalau ditolak karena sudah dipakai, tambahkan `-book` di belakangnya. **Jangan** biarkan kode acak — tautan itulah yang Anda sebar ke LinkedIn dan milis.

## Langkah 4 · Cover

Klik **Upload images or videos**, lalu unggah **tiga berkas ini, berurutan**:

| Urutan | Berkas | Isi |
|---|---|---|
| 1 | `book/publish/gumroad/cover_en_1_hero.png` | buku 3D + judul (tanpa baris angka) |
| 2 | `book/publish/gumroad/cover_en_2_inside.png` | halaman asli buku — membuktikan isinya nyata |
| 3 | `book/publish/gumroad/cover_en_3_quote.png` | kutipan sampul belakang |

Gambar pertama yang menentukan klik orang. Setelah terunggah, **seret** kalau urutannya tertukar.

Ukuran berkasnya **2560 × 1440** (rasio 16:9), sama dengan bingkai cover Gumroad — jadi tidak ada bagian judul yang terpotong. Thumbnail terpisah berukuran **1600 × 1600** (1:1), dipakai Gumroad di halaman toko dan hasil pencarian.

## Langkah 5 · Gulir ke bawah — isian produk

| Kolom | Isi |
|---|---|
| **Thumbnail** | `book/publish/gumroad/thumb_en.png` (1600×1600) — kalau Gumroad menawarkan "use first image", boleh dipakai |
| **Price** | `45` |
| **Currency** | USD |
| **Pay what you want** | **MATI** |
| **Quantity** | kosongkan (tak terbatas) |
| **Versions / tiers** | kosongkan |
| **Category** | `Education` → subkategori buku/academic bila ditawarkan |
| **Tags** | `climate change`, `disaster risk`, `adaptation`, `resilience`, `Indonesia` |
| **Call to action** | kosongkan |

## Langkah 6 · Simpan

Klik **Save and continue** di kanan atas. Kalau ada kotak kuning di panel kanan, biasanya berarti masih ada isian wajib yang kosong — paling sering harga atau berkas. Kotak itu hilang sendiri setelah semuanya lengkap.

---

## Langkah 7 · Tab Content — bagian paling penting

Klik tab **Content** di atas. Unggah **empat berkas** (tombol *Upload files*):

| # | Berkas | Catatan |
|---|---|---|
| 1 | `book/publish/Surviving_the_Future_EN_interior.pdf` | **nyalakan stempel PDF pada berkas ini** |
| 2 | `book/publish/Surviving_the_Future_EN.epub` | tidak bisa distempel |
| 3 | `book/publish/Surviving_the_Future_EN.docx` | tidak bisa distempel |
| 4 | `book/publish/Surviving_the_Future_EN_figures.zip` | 11 gambar 300 dpi |

**Nyalakan toggle "Stamp PDFs with the buyer information"** pada berkas PDF. Tanpa itu tidak ada penanda pembeli sama sekali, dan janji di deskripsi ("The PDF is watermarked with your email address at checkout") menjadi bohong.

Beri nama tiap bagian agar pembeli tahu apa yang dia unduh:

- `01 · The book (PDF, 457 pages)`
- `02 · The book (EPUB)`
- `03 · The book (DOCX)`
- `04 · Figure pack (11 figures, 300 dpi)`

> **Jangan unggah** `*_cover_print.pdf` — itu bungkus cetak untuk percetakan, bukan buku, dan akan membingungkan pembeli. Jangan juga memberi kata sandi pada PDF: Gumroad tidak bisa menstempel berkas terkunci.

## Langkah 8 · Tab Receipt

Boleh dikosongkan. Kalau ingin diisi, satu kalimat:

```
Thank you. Your files are in your Gumroad library — the PDF, the EPUB, the DOCX, and a figure pack you may reuse in your own slides and reports. If anything goes wrong, reply to this email.
```

## Langkah 9 · Tab Share

Tab ini menampilkan tautan pendek produk. Itu tautan yang Anda sebarkan. Salin, lalu simpan di catatan — dipakai di Langkah 20 dan di bio profil.

## Langkah 10 · Terbitkan

Tombol **Publish** (kanan atas). Setelah terbit, buka halamannya di jendela penyamaran (incognito) dan periksa sebagai orang awam:

- [ ] Judul, deskripsi berformat, tiga gambar tampil
- [ ] Harga terbaca $45, bukan $0
- [ ] Tombol beli bisa diklik sampai ke halaman pembayaran
- [ ] Tidak ada teks `[link to your free sample product]` yang tersisa (kalau sampel belum ada, biarkan dulu — diganti di Langkah 20)

---

## Langkah 11 · Uji beli dengan kode diskon 100%

Ini satu-satunya cara memastikan stempel pembeli benar-benar bekerja.

1. **Settings → Discounts → New discount** (atau dari halaman produk: *Checkout → Discounts*).
2. Kode: `TESTSENDIRI` · Diskon: **100%** · Batas pemakaian: **1**.
3. Beli produk Anda sendiri dengan kode itu memakai email yang berbeda dari email akun (mis. Gmail pribadi).
4. Unduh PDF dari email konfirmasi, buka halaman 1 — **email pembeli harus tercetak di sana**.
5. Hapus kode `TESTSENDIRI` setelah selesai.

Kalau stempel tidak muncul: toggle stempel di tab Content belum menyala, atau berkas yang diunggah bukan `*_interior.pdf`.

---

# PRODUK 2 — Free sample (EN, $0)

## Langkah 12 · Buat produk baru

**Products → New product → Digital product**. Name: `Surviving the Future — Free Sample`.

## Langkah 13 · Description

Sama seperti Langkah 2, tetapi berkasnya `listing_sample.html` (teks cadangan: `listing_sample.txt`).

## Langkah 14 · URL

```
surviving-the-future-sample
```

## Langkah 15 · Cover & harga

| Kolom | Isi |
|---|---|
| Cover | `book/publish/gumroad/cover_sample_1_hero.png` |
| Thumbnail | `book/publish/gumroad/thumb_sample.png` |
| **Price** | `0` — dengan harga 0 Gumroad menjadikannya unduhan gratis |
| Pay what you want | **MATI** (kalau dinyalakan, minimumnya harus 0) |
| Tags | `climate change`, `free sample`, `adaptation` |

## Langkah 16 · Content

Satu berkas: `book/publish/Surviving_the_Future_EN_sample.pdf` (35 halaman). Stempel pembeli: **tidak perlu** — sampel memang gratis dan boleh dibagikan.

## Langkah 17 · Terbitkan

Publish, lalu salin URL-nya. URL inilah yang ditempel ke deskripsi produk 1 dan produk 4.

---

# PRODUK 3 — Bertahan Hidup di Masa Depan (ID, $29)

## Langkah 18 · Buat produk baru

Name: `Bertahan Hidup di Masa Depan`. Deskripsi dari `listing_id.html` (cadangan: `listing_id.txt`). URL:

```
bertahan-hidup-di-masa-depan
```

## Langkah 19 · Cover, harga, berkas

| Kolom | Isi |
|---|---|
| Cover 1–3 | `cover_id_1_hero.png`, `cover_id_2_inside.png`, `cover_id_3_quote.png` |
| Thumbnail | `thumb_id.png` |
| Price | `29` · USD |
| Tab Content | `Bertahan_Hidup_di_Masa_Depan_ID_interior.pdf` (**stempel NYALA**), `..._ID.epub`, `..._ID.docx`, `..._ID_figures.zip` |
| Receipt | kalimat yang sama, diterjemahkan bebas, atau kosongkan |

Halaman buku ini 473 halaman — angka itu sudah tertulis di deskripsi, jangan diubah.

---

# PRODUK 4 — Bundle (EN + ID, $59)

## Langkah 20 · Tempel URL sampel lebih dulu

Kembali ke produk 1 dan produk 3, ganti baris sampel di deskripsi dengan URL sampel dari Langkah 17. Simpan.

## Langkah 21 · Buat bundle

Gumroad punya dua jalan. **Pakai jalan A kalau tersedia** — pembeli otomatis mendapat pembaruan kedua buku.

**Jalan A — produk bertipe Bundle.** *New product → Bundle*. Name: `Surviving the Future — Bilingual Bundle`. Pilih dua produk yang sudah terbit (produk 1 dan produk 3), lalu tetapkan harga `59`. Deskripsi dari `listing_bundle.html`. Cover: `cover_bundle_1_hero.png`, lalu `cover_bundle_2_quote.png`. Thumbnail: `thumb_bundle.png`. URL: `bilingual-bundle`.

**Jalan B — kalau Bundle tidak muncul di akun Anda.** Produk digital biasa, unggah delapan berkas sekaligus di tab Content (empat EN + empat ID), harga `59`, deskripsi tetap `listing_bundle.html`. Konsekuensinya: pembaruan buku harus diunggah ulang manual ke sini setiap edisi direvisi.

Jangan lupa: `$59` untuk dua buku yang jika dibeli terpisah `$74` — itu yang membuat bundle masuk akal.

---

# Langkah 22 · Kode diskon (bukan potongan harga di halaman)

Harga di halaman produk **tidak diturunkan**. Diskon hanya lewat kode, supaya harga normal tetap terjaga.

**Settings → Discounts → New discount**, tiga kali:

| Kode | Diskon | Untuk siapa | Batas |
|---|---|---|---|
| `LAUNCH20` | 20% | peluncuran, 14 hari pertama | 50 pemakaian |
| `KAMPUS25` | 25% | mahasiswa & dosen, verifikasi lewat email kampus | tanpa batas |
| `BUNDLEUP40` | 40% | pembeli produk 1 yang mau menambah edisi ID | 20 pemakaian |

Pasang `LAUNCH20` di bagian atas deskripsi selama masa peluncuran, lalu hapus kalimatnya setelah 14 hari. Kode tidak kedaluwarsa sendiri — matikan manual.

---

# Langkah 23 · Sebelum dianggap selesai

Untuk **setiap** produk:

- [ ] Name, URL bersih (bukan kode acak), deskripsi berformat
- [ ] Cover minimal satu gambar; urutan gambar benar
- [ ] Harga benar dan bukan $0 (kecuali sampel)
- [ ] Semua berkas terunggah, ukuran wajar (PDF isi ± 3 MB)
- [ ] Stempel PDF **menyala** pada kedua produk berbayar
- [ ] Tombol beli berfungsi di jendela penyamaran
- [ ] Uji beli 100% sudah dilakukan minimal sekali, stempel terbukti muncul

## Empat kesalahan yang paling sering terjadi

| Gejala | Sebab | Perbaikan |
|---|---|---|
| Deskripsi jadi satu blok tanpa judul | teks polos ditempel | tempel dari berkas `.html`, atau rapikan dengan toolbar |
| Pembeli mengeluh PDF tidak ada tanda dirinya | toggle stempel mati, atau yang diunggah `*_cover_print.pdf` | unggah `*_interior.pdf`, nyalakan stempel |
| Pembeli tidak menemukan berkas | tab Content kosong walau produk terbit | unggah ulang di tab Content, lalu **Save** |
| Kotak kuning di panel kanan tidak hilang | harga atau berkas belum diisi | isi harga dulu, simpan, lalu unggah berkas |

---

## Satu hal soal nama akun

Sidebar Anda menampilkan **Setyo Wisodo**, dan alamat toko `setyowisodo.gumroad.com` — sudah sesuai. Yang tetap perlu dipastikan: nama pada kolom **"Pay to the order of"** di *Settings → Payments* harus sama persis dengan nama pemilik rekening bank. Kalau berbeda, pencairan ditolak dan uang tertahan di saldo. Minimum pencairan **$100** (terkunci untuk rekening Indonesia): di harga $45, dana pertama cair setelah tiga penjualan; di bundle $59, setelah dua.
