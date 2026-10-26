# Menjual Buku Tanpa Membagikan Naskahnya

Panduan singkat untuk dua hal yang Anda tanyakan:

1. pembaca yang **belum membeli** hanya mendapat beberapa lembar, cukup untuk penasaran;
2. pembaca yang **sudah membeli** tidak bisa menyebarkannya dengan leluasa.

Isinya jujur soal batas teknis, karena janji "tidak bisa disebar" yang tidak benar
lebih berbahaya daripada tidak ada janji sama sekali.

---

## 1. Sampel gratis

`python make_sample.py` → `book/publish/*_sample.pdf`

Sampel bukan "10 halaman pertama". Potongan seperti itu berhenti di daftar isi dan
tidak menjual apa pun. Sampel di sini disusun untuk menunjukkan tiga hal yang
membuat orang membeli:

| Bagian | Halaman | Yang dibuktikan |
|---|---|---|
| Judul, hak cipta, **daftar isi penuh** | 1–13 | skala dan kedalaman: 24 bab, 25 tabel, 11 gambar |
| Prakata | 14–16 | suara penulis dan alasan buku ini ada |
| **Bab 1 utuh** | 17–32 | mutu tulisan, bukan cuplikan acak |
| Sepasang halaman Bab 2 bergambar | 33–34 | klaim "data" benar-benar ada |
| Halaman penutup sampel | 35 | apa yang belum dibaca + cara membeli |

Halaman terakhir sampel menyebut: *"Anda baru membaca 35 dari 430 halaman"* — lalu
merinci apa saja yang ada di 395 halaman sisanya. Ini yang memicu rasa penasaran:
bukan menggoda dengan teka-teki, tetapi menunjukkan bahwa yang belum dibaca itu
memang berisi.

Edisi Indonesia: 37 halaman dari 445.

**Setiap halaman sampel membawa catatan kaki** `FREE SAMPLE · Surviving the Future ·
full edition: 430 pages`. Kalau sampel tersebar, ia menyebar bersama alamat pembeliannya.

---

## 2. Salinan pembeli: tanda pemilik

```
python personalize_pdf.py --edition id --name "Budi Santoso" --order "INV-2026-0142"
python personalize_pdf.py --edition en --name "Budi Santoso" --order "INV-2026-0142" --protect
```

Yang dilakukan pada setiap salinan:

1. **Halaman lisensi di depan** — nama pembeli, nomor lisensi, tanggal, jumlah halaman.
2. **Stempel kaki di setiap halaman** — `Licensed copy · INV-2026-0142 · Budi Santoso`.
3. **Metadata PDF** — subject dan keywords memuat nomor lisensi.

Keluaran: `book/publish/sold/<judul>_<nama>.pdf`

### Mengapa ini bekerja

Tujuannya bukan membuat penyalinan mustahil — itu tidak mungkin untuk PDF. Tujuannya
mengubah perhitungan orang yang mau menyebarkan:

- berkas yang beredar **membawa nama pembeli aslinya**;
- Anda bisa melacak kebocoran ke pesanan tertentu;
- pembeli tahu salinannya bertanda namanya, jadi ia berpikir dua kali sebelum
  mengunggahnya ke grup WhatsApp.

Ini pendekatan yang sama dipakai penerbit akademik besar.

### Lapisan tambahan (opsional, `--protect`)

Mengunci izin PDF: boleh **cetak** dan **salin teks** (dibutuhkan untuk aksesibilitas
dan kutipan), tidak boleh **ubah** dan **anotasi**. Sudah diuji: bookmark 327 entri
tetap utuh, tidak ada kata sandi yang diminta saat dibuka.

Sadarilah batasnya: alat gratis di internet bisa menghapus kunci ini dalam hitungan
detik. Nilainya mencegah penyalinan iseng, bukan pembajakan serius. **Jangan** pakai
kata sandi buka (`user_pw`) — pembeli akan mengeluh dan menganggap berkasnya rusak.

---

## 3. Jalur yang benar-benar aman

Kalau tujuannya benar-benar mencegah penyebaran, PDF bukan jawabannya. Urutannya:

| Jalur | Pembeli bisa salin? | Catatan |
|---|---|---|
| **Cetak (POD)** | bisa difoto, tapi tidak nyaman | paling aman; tidak ada berkas untuk disebar |
| **Amazon KDP / Google Play Books** | sulit — DRM dikelola platform | platform menangani lisensi; Anda tidak bisa mengatur sendiri |
| **Toko sendiri + tanda pemilik** | bisa, tapi terlacak | yang sekarang dibangun di repo ini |
| **PDF tanpa tanda apa pun** | bebas | jangan dijual begini |

Rekomendasi praktis: **jual cetak sebagai produk utama**, EPUB/PDF bertanda pemilik
sebagai pelengkap, sampel gratis sebagai umpan di media sosial.

---

## 4. Hak yang tetap Anda pegang

Anda tidak perlu menyerahkan hak cipta untuk melindungi penjualan. Cukup lisensi
terbatas untuk pembeli perorangan:

> Pembeli memperoleh lisensi **non-eksklusif, tidak dapat dipindahtangankan**, untuk
> membaca salinan ini secara pribadi. Dilarang menggandakan, menjual ulang, atau
> menyebarluaskan berkas ini, baik utuh maupun sebagian.

Kalimat ini sudah tercetak di halaman lisensi dan di halaman penutup sampel. Untuk
perlindungan formal di Indonesia, pencatatan ciptaan dapat dilakukan melalui DJKI
(gratis untuk perorangan); itu bukan syarat untuk memiliki hak, tetapi mempermudah
pembuktian bila terjadi sengketa.

---

## 5. Yang harus Anda isi sendiri

Sampel masih memuat penanda `[ isi alamat toko Anda di sini ]`. Ganti di
`make_sample.py` (kunci `cta_url`) lalu jalankan ulang, atau kirimkan alamat toko
Anda dan saya isikan.
