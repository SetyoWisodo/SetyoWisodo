# Mengisi Halaman Produk Gumroad — Langkah demi Langkah

Untuk produk pertama: **Surviving the Future**. Semua isian di bawah sudah final —
tinggal tempel dan unggah.

---

## Yang sudah benar

| Kolom | Status |
|---|---|
| **Name** — `Surviving the Future` | sudah benar, biarkan |

---

## 1. Description

Kotak kosong besar itu yang paling menentukan penjualan. **Jangan tempel teks
polos** — Gumroad membuang semua judul dan poin, hasilnya satu dinding paragraf
yang tidak ada yang membaca sampai habis.

### Cara yang benar

1. Buka berkas **`book/publish/gumroad/copy/listing_en.html`** di browser
   (klik dua kali, atau seret ke jendela Chrome)
2. **Ctrl+A** lalu **Ctrl+C**
3. Klik kotak Description di Gumroad, lalu **Ctrl+V**

Judul, garis pemisah, dan daftar poinnya akan ikut terbawa. Kotak petunjuk kecil
di atas halaman itu tidak akan tersalin.

### Kalau hasil tempelannya berantakan

Tempel teksnya per bagian (`listing_en.txt`), lalu rapikan dengan tombol di toolbar:

| Bagian | Tombol toolbar |
|---|---|
| `WHAT MAKES THIS DIFFERENT`, `WHY $45`, dst. | dropdown **Text** → *Heading 2* |
| Baris berawalan `*` | tombol **bullet list** |
| Sisa paragraf | biarkan sebagai *Paragraph* |

---

## 2. URL

Sekarang terbaca `vbqmqo` — kode acak. Ganti menjadi:

```
surviving-the-future
```

Alamat lengkapnya menjadi `victory.gumroad.com/l/surviving-the-future`.

Kalau Gumroad menolak karena sudah dipakai, tambahkan `-book` atau `-en` di
belakangnya. **Jangan** biarkan kode acak: tautan itu yang Anda sebarkan ke
LinkedIn dan milis.

> Catatan: alamat toko Anda sekarang **victory.gumroad.com**. Kalau ingin
> `setyowisodo.gumroad.com`, ubah di **Settings → Profile → Username**. Bisa
> dilakukan kapan pun; tautan produk lama tetap berfungsi.

---

## 3. Cover

Klik **Upload images or videos**, lalu unggah **tiga berkas ini, berurutan**:

| Urutan | Berkas | Isi |
|---|---|---|
| 1 | `cover_en_1_hero.png` | buku 3D + judul + angka (24 / 145 / 430) |
| 2 | `cover_en_2_inside.png` | halaman asli buku, membuktikan isinya nyata |
| 3 | `cover_en_3_quote.png` | kutipan sampul belakang |

Urutan penting: gambar pertama yang menentukan klik. Setelah terunggah, seret
kalau urutannya tertukar.

---

## 4. Isian di bawah Cover

| Kolom | Isi |
|---|---|
| **Thumbnail** | `thumb_en.png` (1600×1600) |
| **Price** | `45` |
| **Currency** | USD |
| **Pay what you want** | **MATI** — ini produk berbayar |
| **Quantity** | biarkan kosong (tak terbatas) |
| **Versions / tiers** | biarkan kosong |
| **Call to action** | biarkan kosong |

---

## 5. Tab Content — bagian paling penting

Klik tab **Content** di atas, lalu unggah **empat berkas**:

| # | Berkas | Keterangan |
|---|---|---|
| 1 | `Surviving_the_Future_EN_interior.pdf` | **nyalakan stempel PDF pada berkas ini** |
| 2 | `Surviving_the_Future_EN.epub` | tidak bisa distempel |
| 3 | `Surviving_the_Future_EN.docx` | tidak bisa distempel |
| 4 | `Surviving_the_Future_EN_figures.zip` | 11 gambar 300 dpi |

**Nyalakan toggle "Stamp PDFs with the buyer information"** pada berkas PDF.
Tanpa itu, tidak ada penanda pembeli sama sekali.

> **Jangan unggah** `*_cover_print.pdf` (itu bungkus cetak, bukan buku) dan
> jangan unggah versi yang sudah dikunci kata sandi — Gumroad tidak bisa
> menstempelnya.

---

## 6. Tab Receipt

Boleh dikosongkan. Kalau ingin diisi, cukup satu kalimat:

```
Thank you. Your files are in your Gumroad library — the PDF, the EPUB, the DOCX,
and a figure pack you may reuse in your own slides and reports. If anything goes
wrong, reply to this email.
```

---

## 7. Tab Share

Setelah disimpan, tab ini menampilkan tautan pendek produk. Itu tautan yang Anda
sebarkan — bukan alamat panjangnya.

---

## 8. Sebelum menekan Publish

Tombol di kanan atas berbunyi **Save and continue**. Klik itu dulu untuk menyimpan,
lalu periksa daftar ini:

- [ ] Name: `Surviving the Future`
- [ ] Description terisi dan berformat (ada judul dan poin, bukan satu blok teks)
- [ ] URL: `surviving-the-future`
- [ ] Tiga gambar cover, urutan benar
- [ ] Thumbnail terunggah
- [ ] Price `45`, currency USD, Pay-what-you-want mati
- [ ] Empat berkas di tab Content
- [ ] Stempel PDF **menyala** pada berkas PDF
- [ ] Kotak kuning peringatan di panel kanan sudah hilang

Kotak kuning di panel kanan biasanya berarti masih ada isian wajib yang kosong —
paling sering harga atau berkas. Ia akan hilang sendiri setelah semuanya lengkap.

---

## 9. Urutan yang benar untuk sisa produk

Jangan lanjut ke produk kedua sebelum yang ini terbit dan diuji.

1. **Produk ini** (EN, $45) → terbitkan
2. **Uji beli** dengan kode diskon 100% → cek email Anda tercetak di halaman
   pertama PDF
3. **Produk sampel** (gratis) → terbitkan, salin URL-nya
4. Tempel URL sampel ke deskripsi produk ini, lalu simpan
5. **Produk ID** ($29)
6. **Produk bundle** ($59)

Sampel dibuat setelah produk berbayar karena URL-nya dibutuhkan untuk deskripsi —
bukan sebaliknya.

---

## 10. Satu hal soal nama akun

Sidebar Anda menunjukkan nama **Victor**, dan alamat tokonya `victory.gumroad.com`.
Itu tidak masalah untuk tampilan. Yang perlu dipastikan: **nama pada kolom "Pay to
the order of" di Settings → Payments harus sama persis dengan nama pemilik rekening
bank** — kalau berbeda, pencairan ditolak, dan uang tertahan di saldo.

Nama yang tampil di halaman produk (Setyo Wisodo) boleh berbeda dari nama akun.
Itu wajar untuk penulis yang memakai nama pena.
