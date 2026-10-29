# Panduan Unggah Gumroad — Layar demi Layar

Toko Anda: **setyowisodo.gumroad.com** · Halaman yang sedang terbuka: produk pertama (`/vbqmqo`), tab **Product** — masih kosong, ini yang pertama diisi.

**Status produk 1 (per 29 Oktober 2026):**

| Bagian | Status |
|---|---|
| Name | ✅ `Surviving the Future` |
| Description | ✅ terisi dan berformat |
| URL | ✅ `surviving-the-future` |
| Cover (3 gambar) | ✅ terunggah |
| Thumbnail + harga $45 | ⬜ harga belum diisi di panel kanan |
| Content (4 berkas + stempel PDF) | ✅ empat berkas masuk, stempel PDF menyala |
| Uji beli kode 100% | ⬜ |

**Keputusan 29 Oktober 2026: hanya edisi Inggris yang dijual.** Dua produk, dalam urutan ini:

| # | Produk | Harga | Berkas isi |
|---|---|---|---|
| 1 | Surviving the Future (EN) | $45 | PDF + EPUB + DOCX + paket gambar |
| 2 | Free sample (EN) | $0 | 1 PDF sampel 36 hlm (bersampul) |

Edisi Indonesia **tidak dijual dan tidak diunggah ke Gumroad**. Ia tetap dipakai sebagai alat koreksi silang — setiap angka dan setiap argumen di edisi Inggris diperiksa ulang lewat edisi Indonesia yang ditulis terpisah. Berkasnya tetap dirender hanya untuk keperluan itu; lihat bagian **Edisi Indonesia — internal** di bawah.

> **Teks deskripsi tidak perlu dikarang.** Teks final tersedia di halaman unduhan, bagian **Teks deskripsi siap tempel**: `/copy/en` dan `/copy/sample`. Buka, tekan Ctrl+A, Ctrl+C, tempel ke kotak Description.
Semua isian di bawah sudah final. Ikuti berurutan; jangan lompat ke produk kedua sebelum produk pertama terbit dan diuji.

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

**Setelah produk sampel terbit** (Langkah 17), kembali ke sini dan ganti teks `[link to your free sample product]` menjadi URL sampel.

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
| **Category** | `Education > Science` — pilihan terdekat untuk buku iklim/ketahanan; daftar Gumroad tidak punya "Environment" |
| **Tags** | sepuluh tag di Langkah 9: `climate change`, `sustainability`, `environment`, `science`, `resilience`, `nonfiction`, `ebook`, `book`, `disaster risk`, `Indonesia` |
| **Call to action** | kosongkan |

## Langkah 6 · Simpan

Klik **Save and continue** di kanan atas. Kalau ada kotak kuning di panel kanan, biasanya berarti masih ada isian wajib yang kosong — paling sering harga atau berkas. Kotak itu hilang sendiri setelah semuanya lengkap.

---

## Langkah 5b · Product info (Call to action · Summary · Additional details)

Bagian ini muncul setelah Thumbnail. Isinya pendek, tapi Summary ikut tampil di kartu produk dan hasil pencarian Gumroad — jadi jangan dikosongkan.

| Kolom | Isi | Alasan |
|---|---|---|
| **Call to action** | `I want this` — biarkan | Teks tombol beli; sudah wajar |
| **Summary** | lihat tabel di bawah | Satu kalimat, tampil di bawah tombol beli |
| **Additional details** | `Pages` → `457` · `Language` → `English` · `Format` → `PDF, EPUB, DOCX` | Muncul sebagai butir detail di halaman produk; membantu orang memutuskan sebelum membeli |
| **Integrations** (community chat) | **mati** | Chat butuh dijawab setiap hari; jangan dinyalakan kalau tidak ada waktu |

### Summary — empat kalimat final

| Produk | Summary |
|---|---|
| EN ($45) | `Why the same storm kills in one country and spares the next — and what a prepared community does differently. 24 chapters, 457 pages, 152 cited sources.` |
| ID ($29) | `Mengapa badai yang sama menewaskan di satu negeri dan tidak di negeri lain — dan apa yang dilakukan masyarakat yang siap. 24 bab, 473 halaman, 152 sumber.` |
| Sampel ($0) | `The full table of contents, the preface, and all of Chapter 1 — free, no email wall.` |
| Bundle ($59) | `Both editions, 930 pages, one purchase: the English and Indonesian books, written separately for each readership.` |

Kalau kotak Summary menolak karena terlalu panjang, potong bagian setelah tanda pisah — kalimat pertama saja sudah cukup.

### Additional details — cara mengisi

1. Klik dropdown yang sekarang terbaca **Pages** → pilih **Pages**, lalu isi kolom sebelahnya dengan `457`.
2. Klik **+ Add detail** untuk menambah baris: pilih **Language** → `English`.
3. **+ Add detail** lagi: pilih **Format** → `PDF, EPUB, DOCX`.
4. Kalau atribut yang Anda mau tidak ada di daftar, klik ikon **tong sampah** di kanan baris itu — lebih baik tidak ada detail daripada detail yang salah.

Untuk produk ID, ganti Language menjadi `Indonesian`; untuk bundle, tulis `English, Indonesian`.

---

## Langkah 6b · Harga (panel kanan)

Kolom harga tidak ada di tengah halaman — ia ada di **panel kanan**, di bawah tulisan *Price*. Ketik `45`, pastikan satuannya **USD**, lalu klik di luar kotak. Peringatan kuning *"Please enter a valid price"* akan hilang setelah angka masuk.

Jangan nyalakan **Pay what you want** dan jangan buat **variant**: satu harga, satu produk.

### Tiga toggle di bagian Pricing — semuanya MATI

| Toggle | Setelan | Sebab |
|---|---|---|
| Allow customers to pay what they want | **mati** | Produk berharga tetap; kalau nyala, pembeli bisa membayar $1 |
| Allow customers to pay in installments | **mati** | Nilai transaksi kecil; cicilan hanya menambah friksi dan biaya |
| Automatically apply discount code | **mati** | Diskon dipakai manual lewat kode; kalau nyala, semua orang dapat diskon |

### Bagian Versions — lewati

Kotak **+ Add version** dibiarkan kosong. Satu versi, empat berkas. Versi hanya berguna kalau Anda menjual paket berbeda (mis. PDF saja vs PDF + cetak).

---

## Langkah 6c · Settings (di bawah Versions)

Enam toggle. Hanya dua yang perlu disentuh.

| Toggle | Setelan | Sebab |
|---|---|---|
| **Limit product sales** | mati | Produk digital, stok tak terbatas. Menyalakan ini membuat produk berhenti terjual setelah batas tertentu |
| **Allow customers to choose a quantity** | mati | Buku tidak dijual per kodi; menyalakannya membuat pembeli bisa membeli 5 salinan sekaligus dan bingung soal lisensi |
| **Publicly show the number of sales on your product page** | mati (awal) | Di awal, angka "3 sales" justru melemahkan. Nyalakan nanti setelah lewat 50 penjualan — saat angka itu jadi bukti sosial |
| **Mark product as e-publication for VAT purposes** | **NYALA** | Ini buku elektronik. Dengan ini Gumroad memperlakukan produk sebagai e-publication, bukan layanan digital umum — relevan untuk perlakuan pajak di beberapa negara pembeli |
| **Let people join a waitlist on your product page** | mati | Produk digital tak pernah habis; waitlist hanya untuk stok terbatas |
| **Specify a refund policy for this product** | **NYALA** → **No refunds allowed** (keputusan penulis, 29 Okt 2026) | Kebijakan tertulis tetap wajib walau isinya "tidak ada refund" |
| **Custom domain** | kosongkan | Domain sendiri hanya perlu bila Anda punya situs. `setyowisodo.gumroad.com` sudah cukup |

### Refund policy — keputusan yang sudah diambil (29 Okt 2026)

**Status: `No refunds allowed`, fine print "all sales are final".** Kombinasi ini konsisten — dropdown dan tulisan tidak bertentangan, dan itu syarat utamanya. Pembeli melihat aturannya sebelum membayar, jadi tidak ada janji yang dilanggar.

Yang perlu disadari dari pilihan ini:

| Konsekuensi | Besarnya |
|---|---|
| Konversi | turun sedikit dibanding toko yang menawarkan jaminan uang kembali |
| Sengketa kartu | tetap mungkin — pemegang kartu bisa minta chargeback ke banknya, dan Anda tidak bisa menolaknya |
| Perlindungan Anda | kuat di mata Gumroad: kebijakan tertulis membalik beban pembuktian |
| Pengaman yang tersisa | klausul "working copy within 24 hours" di fine print — inilah yang menyelamatkan mayoritas keluhan, karena hampir semua keluhan buku digital adalah berkas gagal dibuka |

Kalau nanti angka refund terasa mengganggu penjualan, cukup ubah dropdown ke **14-day money back guarantee** dan ganti fine print-nya; perubahan hanya berlaku untuk penjualan berikutnya.

### Fine print yang dipakai untuk "No refunds"

```
Because this is a digital download, all sales are final. If a file will not open,
or you received the wrong edition, write to me and I will send a working copy
within 24 hours. A free 35-page sample is available so you can judge the book
before you buy.
```

### Kalau nanti berubah ke 14 hari, pakai fine print ini

Pilih `14-day money back guarantee`, lalu tempel:

```
Write to me within 14 days of purchase and I will refund you in full, no
questions asked. If a file will not open or you received the wrong edition, I
will send a working copy first, and refund you if that does not solve it. The
free 35-page sample exists so you can judge the book before you buy it.
```

**Kalau Anda tetap memilih "No refunds allowed",** fine print-nya harus berubah supaya tidak bertentangan dengan pilihan itu:

```
Because this is a digital download, all sales are final. If a file will not open,
or you received the wrong edition, write to me and I will send a working copy
within 24 hours. A free 35-page sample is available so you can judge the book
before you buy.
```

Yang tidak boleh: memilih "No refunds allowed" tapi menulis janji uang kembali di deskripsi. Itu kontradiksi yang justru memicu sengketa.

### Peringatan kuning di bawah halaman — bukan kesalahan

> *"This product has no files or content. Buyers who purchase it get an empty download page — add content in the Content tab."*

Ini normal dan **hilang sendiri setelah Langkah 7**. Artinya sederhana: harganya sudah, berkasnya belum. Klik **Save and continue**, lalu pindah ke tab **Content**.

---

## Langkah 7 · Tab Content — bagian paling penting

Klik tab **Content** di atas. Unggah **empat berkas** (tombol *Upload files*):

| # | Berkas | Catatan |
|---|---|---|
| 1 | `book/publish/Surviving_the_Future_EN_ebook.pdf` | **nyalakan stempel PDF pada berkas ini** — sudah bersampul |
| 2 | `book/publish/Surviving_the_Future_EN.epub` | tidak bisa distempel |
| 3 | `book/publish/Surviving_the_Future_EN.docx` | tidak bisa distempel |
| 4 | `book/publish/Surviving_the_Future_EN_figures.zip` | 11 gambar 300 dpi |

**Nyalakan toggle "Stamp PDFs with the buyer information"** pada berkas PDF. Tanpa itu tidak ada penanda pembeli sama sekali, dan janji di deskripsi ("The PDF is watermarked with your email address at checkout") menjadi bohong.

Nama berkas sudah terisi otomatis dari zip — biarkan apa adanya:

- `01 - The book (PDF, 457 pages)`
- `02 - The book (EPUB)`
- `03 - The book (DOCX)`
- `04 - Figure pack (11 figures, 300 dpi)`

**Description tiap berkas (opsional, tapi membantu pembeli di pustaka mereka):**

| Berkas | Description |
|---|---|
| PDF | `The complete book: cover, 457 numbered pages, 327 bookmarks, table of contents and index. Stamped with your purchase details at checkout.` |
| EPUB | `For phones, tablets and e-readers. All 24 chapters and 11 figures, reflowable text.` |
| DOCX | `Editable manuscript, A4, Times New Roman 12 pt — for quoting, excerpting or translating passages.` |
| ZIP | `Eleven figures at 300 dpi with captions and source lines. Cleared for use in your own slides, lectures and reports; please credit the book.` |

**ISBN: kosongkan.** Buku ini belum punya ISBN terdaftar, dan mengarang nomor justru merusak data perpustakaan. Kalau nanti ingin ISBN (untuk katalog perpustakaan atau toko ritel), Perpustakaan Nasional RI menerbitkannya gratis; setelah itu baru isi kolom ini.

**Toggle per berkas:**

| Toggle | PDF | EPUB/DOCX/ZIP |
|---|---|---|
| Stamp this PDF with buyer information | **NYALA** | tidak ada |
| Show "Send to Kindle" and "Read" buttons | nyala (berguna untuk PDF & EPUB) | nyala |
| Disable file downloads | **MATI** | **MATI** |

> **Jangan unggah** `*_cover_print.pdf` — itu bungkus cetak untuk percetakan, bukan buku. **Jangan juga** `*_interior.pdf` untuk pembeli: berkas itu untuk percetakan, halaman pertamanya halaman judul teks tanpa sampul. Yang dijual adalah `*_ebook.pdf`. Jangan beri kata sandi pada PDF — Gumroad tidak bisa menstempel berkas terkunci.

## Langkah 8 · Tab Receipt

Dua isian saja, keduanya sengaja pendek.

**Button text** (batas 26 karakter) — tombol yang diklik pembeli untuk membuka berkasnya:

```
Download your files
```

19 karakter. Jangan diganti "View content": kata *download* yang dicari pembeli.

**Custom message** (batas 500 karakter) — 301 karakter, ikut terkirim di email pembeli:

```
Thank you for buying Surviving the Future. Your four files are in your Gumroad library: the complete PDF (cover plus 457 pages), the EPUB, the DOCX, and a figure pack you may reuse in your own slides and reports. If a download fails, reply to this email and I will send a working copy within 24 hours.
```

Kalimat terakhir itu janji refund yang sama dengan kebijakan *No refunds allowed*: pengganti berkas dalam 24 jam, bukan uang kembali. Setelah menempel keduanya, klik **Save changes**.

## Langkah 9 · Tab Share

Empat bagian di satu halaman. Urutannya dari atas ke bawah.

**1. Share — tautan produk.** Klik **Copy URL**. Hasilnya:

```
https://setyowisodo.gumroad.com/l/surviving-the-future
```

Itu satu-satunya tautan yang disebar. Jangan pakai *Copy checkout URL* untuk promosi — tautan itu langsung membuka halaman bayar, terasa memaksa.

**2. Landing page — JANGAN DISENTUH.** Tombol **Copy prompt** di situ membangun halaman pengganti buatan AI yang **menggantikan seluruh halaman produk, termasuk tombol beli bawaan**. Selama halaman itu belum dipasang dan lolos uji, produk tidak bisa dibeli. Biarkan kosong; halaman bawaan Gumroad sudah rapi dan harga $45 tampil di sana.

**3. Profile.** Tulisan *"You currently have no sections in your profile to display this"* berarti produk ini belum muncul di halaman profil Anda. Klik **create one here**, beri nama bagian:

```
Books
```

Simpan, lalu produk ini masuk ke bagian itu. Tanpa langkah ini, orang yang membuka `gumroad.com/setyowisodo` tidak melihat buku Anda sama sekali.

**Di mana bagian profil itu diatur.** Bukan di halaman produk, dan bukan di tab *About*. Halaman `gumroad.com/settings/profile` punya empat tab — **About · Design · Pages · Share** — dan bagian-bagian profil tinggal di tab **Pages**. Tab *About* hanya memuat Name, Bio, dan Avatar.

Jadi: **Edit profile** → tab **Pages** → klik bagian yang ada (kalau kosong, klik **Add section**) → isi nama:

```
Books
```

lalu centang produk **Surviving the Future** di dalamnya → **Save**. Judul *Books* langsung muncul di atas kartu produk pada `gumroad.com/setyowisodo` setelah halaman di-refresh.

**Bio di tab About — pakai kalimat ini (201 karakter):**

```
Author of Surviving the Future — a book about what actually protects people when the water rises, the harvest fails, or the grid goes down. 24 chapters, 152 sources, eleven original figures, 457 pages.
```

Kalau bagian *Bio* dibiarkan kosong, halaman profil hanya menampilkan nama dan kartu buku tanpa satu pun penjelasan — pembeli yang masuk dari tautan tidak tahu siapa penulisnya. Toggle **Show your storefront on product pages** biarkan **nyala**.

**Harga tampil dalam Rupiah di layar Anda — itu wajar.** Gumroad mendeteksi mata uang pengunjung (pojok kanan bawah halaman profil: *Rp (Indonesian Rupiah) — detected*), lalu menampilkan harga yang sudah dikonversi. Pembeli di Amerika tetap melihat **$45**. Tidak ada yang perlu diubah, dan jumlah yang Anda terima tetap dihitung dari harga USD.

**4. Gumroad Discover.** Kategori masih `Other`; ganti, lalu isi tag. Persis lima tag ini:

| Kolom | Isi |
|---|---|
| Category | `Education > Science` |
| Tag 1 | `climate change` |
| Tag 2 | `sustainability` |
| Tag 3 | `environment` |
| Tag 4 | `science` |
| Tag 5 | `resilience` |
| Tag 6 | `nonfiction` |
| Tag 7 | `ebook` |
| Tag 8 | `book` |
| Tag 9 | `disaster risk` |
| Tag 10 | `Indonesia` |
| Display your product's 1-5 star rating | biarkan **nyala** |
| Content meant only for adults | **MATI** |

**Mengapa sepuluh tag ini.** Pencarian Discover mencocokkan **semua** kata yang diketik pembeli, dan kata itu boleh berasal dari nama, nama penulis, deskripsi, **atau** tag — bobotnya sama. Artinya tag adalah satu-satunya cara menjangkau kata yang tidak ada di judul dan deskripsi. Deskripsi produk ini memuat *resilience*, *future*, *book*, *climate*, *crisis*; ia **tidak** memuat *sustainability*, *environment*, *science*, *nonfiction*, *ebook*, *disaster*, *Indonesia*. Enam tag terakhir karena itu bukan hiasan: tanpa mereka, pencarian "sustainability" tidak akan pernah memunculkan buku ini.

Batasnya 10 tag, 2–20 karakter. **Pakai spasi, jangan tanda hubung** — filter Discover di Gumroad mengubah tanda hubung pada URL menjadi spasi, sehingga tag `climate-change` tidak akan pernah bisa dipilih sebagai filter.
Discover menahan biaya 30% **hanya** untuk penjualan yang datang lewat Discover; penjualan dari tautan Anda sendiri tetap 10% + biaya proses. Kategori dan tag hanya membuka pintunya — produk baru benar-benar tampil di Discover setelah ada satu penjualan berbayar dan Risk Review selesai. Uji beli 100% tidak dihitung sebagai penjualan berbayar.

Klik **Save changes** setelah empat bagian itu beres.

## Langkah 10 · Terbitkan

Tombol **Publish** (kanan atas). Setelah terbit, buka halamannya di jendela penyamaran (incognito) dan periksa sebagai orang awam:

- [ ] Judul, deskripsi berformat, tiga gambar tampil
- [ ] Harga terbaca $45, bukan $0
- [ ] Tombol beli bisa diklik sampai ke halaman pembayaran
- [ ] Sampai sampel terbit, teks `[link to your free sample product]` di deskripsi masih ada — ini **sengaja** ditunda; diganti dengan URL sampel tepat setelah produk sampel terbit

---

## Langkah 11 · Uji beli dengan kode diskon 100%

Ini satu-satunya cara membuktikan stempel pembeli benar-benar bekerja sebelum ada orang yang membayar $45.

### 11a · Membuat kode

1. Buka `gumroad.com/discounts` — kalau harus lewat menu: sidebar kiri **Everything else** → **Discounts**.
2. Klik **New discount**.
3. Isi persis:

| Kolom | Isi |
|---|---|
| Name (internal, tidak dilihat pembeli) | `Test purchase — hapus setelah selesai` |
| Code | `TESTSENDIRI` — **isi kolom ini**; kalau dibiarkan kosong, Gumroad membuat kode dari kolom Name (saat dicoba 29 Okt, kotak Code terlewat sehingga kode tersimpan menjadi `FIRSTBUYERFREE`) |
| Discount type | **Percentage** |
| Amount | `100` |
| Limit quantity of discounted products | `1` |
| Limit to product | **Surviving the Future** |
| Minimum quantity | kosongkan |
| Valid until | kosongkan — akan dihapus manual |

4. **Save**.

Batas `1` itu penting: kalau lupa, siapa pun yang menebak kode ini bisa mengambil buku gratis. "Limit to product" juga penting supaya kode tidak ikut berlaku di produk sampel nanti.

### 11b · Membeli

1. Buka jendela **incognito** (Ctrl+Shift+N) — supaya tidak memakai sesi akun Anda.
2. Buka `https://setyowisodo.gumroad.com/l/surviving-the-future`.
3. Klik **I want this**.
4. Kolom kode ada di **kolom kiri, tepat di atas bagian tip** — kadang sudah tampil sebagai kotak isian, kadang masih berupa tautan **Add discount code** / *Have a discount code?* yang harus diklik dulu. Kalau tidak terlihat, **gulir ke atas** di halaman itu. Tempel `TESTSENDIRI`, lalu **Apply**.
5. Total harus berubah menjadi **Rp 0** (halaman ini menampilkan Rupiah karena mata uang terdeteksi; $0 dan Rp 0 sama saja). Kalau total masih Rp 825.129, kodenya belum masuk — jangan lanjut mengisi kartu.
6. Isi email yang **berbeda** dari email akun Gumroad (mis. Gmail pribadi Anda). Ini bagian inti ujian: stempel akan mencetak email ini.
7. Selesaikan pembelian. Pada total $0 biasanya tidak perlu nomor kartu.

### 11c · Memeriksa hasilnya

1. Unduh **PDF** dari halaman terima kasih atau dari email konfirmasi.
2. Buka — halaman pertama harus **sampul berwarna**, bukan halaman judul teks.
3. Cari stempel: **email yang Anda pakai tadi harus tercetak** di halaman itu (biasanya di kaki halaman).
4. Jumlah halaman harus **458**.
5. Buka EPUB-nya sebentar: harus terbuka dan bergambar, walau tidak bisa distempel.

Kalau stempel tidak muncul: toggle **Stamp this PDF with buyer information** di tab Content belum menyala, atau berkas yang diunggah bukan `*_ebook.pdf`.

### 11d · Membersihkan

1. Kembali ke `gumroad.com/discounts`, hapus kode `TESTSENDIRI`. Jangan hanya dibiarkan tidak aktif — kode batas 1 yang lupa dihapus adalah pintu gratis kalau nanti batasnya dinaikkan.
2. Pembelian uji $0 boleh dibiarkan di daftar Sales; ia tidak dihitung sebagai penjualan berbayar dan tidak membuka Discover.

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

Satu berkas: `book/publish/Surviving_the_Future_EN_sample.pdf` (36 halaman, sudah bersampul). Stempel pembeli: **tidak perlu** — sampel memang gratis dan boleh dibagikan.

## Langkah 17 · Terbitkan

Publish, lalu salin URL-nya. URL inilah yang ditempel ke deskripsi produk 1 (dan ke bio/profil).

---

# Edisi Indonesia — internal, tidak dijual

Edisi Indonesia tetap hidup di repositori sebagai **pembanding**, bukan produk:

| Fungsi | Berkas |
|---|---|
| Koreksi silang angka & argumen | `book_id.md` dibandingkan dengan `book.md` |
| Bukti paritas isi | `python render_book_id.py` → `Surviving_the_Future_ID.pdf` (473 hlm) |
| Pemeriksaan mandiri per bab | `KASUS_PER_BAB.md`, `PREDIKSI_PER_BAB.md`, `ADVICE_PER_BAB.md` |

**Yang tidak dilakukan lagi:**

- Jangan membuat produk Gumroad untuk edisi ini.
- Jangan menyiapkan sampul jual, thumbnail, atau teks listing berbahasa Indonesia.
- Jangan menautkannya di halaman toko, bio, atau materi promosi mana pun.

Alasannya komersial: pasar buku akademik berbahasa Indonesia untuk topik ini terlalu kecil dibanding perhatian yang dibutuhkan untuk mengelolanya. Satu produk yang dirawat serius lebih baik daripada dua yang setengah dirawat.

> Berkas `book/publish/gumroad/cover_id_*.png`, `thumb_id.png`, `listing_id.txt`, dan `listing_bundle.txt` **tidak dipakai lagi** — jangan diunggah. Kalau suatu hari edisi Indonesia ingin dijual, berkas itu bisa dibuat ulang dengan `python make_gumroad.py`.

---

# Langkah 18 · Kode diskon (bukan potongan harga di halaman)

Harga di halaman produk **tidak diturunkan**. Diskon hanya lewat kode, supaya harga normal tetap terjaga.

**Settings → Discounts → New discount**, dua kali:

| Kode | Diskon | Untuk siapa | Batas |
|---|---|---|---|
| `LAUNCH20` | 20% | peluncuran, 14 hari pertama | 50 pemakaian |
| `KAMPUS25` | 25% | mahasiswa & dosen, verifikasi lewat email kampus | tanpa batas |

Kode `BUNDLEUP40` **tidak dipakai lagi** — ia hanya masuk akal kalau ada produk kedua.

Pasang `LAUNCH20` di bagian atas deskripsi selama masa peluncuran, lalu hapus kalimatnya setelah 14 hari. Kode tidak kedaluwarsa sendiri — matikan manual.

---

# Langkah 19 · Sebelum dianggap selesai

Untuk **setiap** produk:

- [ ] Name, URL bersih (bukan kode acak), deskripsi berformat
- [ ] Cover minimal satu gambar; urutan gambar benar
- [ ] Harga benar dan bukan $0 (kecuali sampel)
- [ ] Semua berkas terunggah, ukuran wajar (PDF isi ± 3 MB)
- [ ] Stempel PDF **menyala** pada produk berbayar (produk sampel tidak perlu)
- [ ] Tombol beli berfungsi di jendela penyamaran
- [ ] Uji beli 100% sudah dilakukan minimal sekali, stempel terbukti muncul

## Empat kesalahan yang paling sering terjadi

| Gejala | Sebab | Perbaikan |
|---|---|---|
| Deskripsi jadi satu blok tanpa judul | teks polos ditempel | tempel dari berkas `.html`, atau rapikan dengan toolbar |
| Pembeli mengeluh PDF tidak ada tanda dirinya | toggle stempel mati, atau yang diunggah `*_cover_print.pdf` / `*_interior.pdf` | unggah `*_ebook.pdf`, nyalakan stempel |
| Pembeli tidak menemukan berkas | tab Content kosong walau produk terbit | unggah ulang di tab Content, lalu **Save** |
| Kotak kuning di panel kanan tidak hilang | harga atau berkas belum diisi | isi harga dulu, simpan, lalu unggah berkas |

---

## Satu hal soal nama akun

Sidebar Anda menampilkan **Setyo Wisodo**, dan alamat toko `setyowisodo.gumroad.com` — sudah sesuai. Yang tetap perlu dipastikan: nama pada kolom **"Pay to the order of"** di *Settings → Payments* harus sama persis dengan nama pemilik rekening bank. Kalau berbeda, pencairan ditolak dan uang tertahan di saldo. Minimum pencairan **$100** (terkunci untuk rekening Indonesia): di harga $45, dana pertama cair setelah **tiga penjualan**.
