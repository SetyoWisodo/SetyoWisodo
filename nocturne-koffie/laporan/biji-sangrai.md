# Halaman "Biji sangrai" — landing penjualan roasted beans

Dibuat 5 November 2026. Permintaan pemilik: *"buat website seperti
[template portfolio motion artist di jiro.build] dan hanya menyesuaikan ke
jualan roasted beans, based in Banyuwangi Indonesia."*

| Hal | Isi |
| --- | --- |
| Berkas | `biji-sangrai/index.html` (hasil generate), `biji-sangrai/toko.css`, `biji-sangrai/toko.js` |
| Pembuat | `python3 tools/roasted.py` — membaca `data/catalog.json`, tidak ada angka yang diketik tangan |
| Pemeriksa | `python3 tools/roasted.py --cek` + gerbang `python3 tools/periksa.py` (cek *Biji sangrai*) |
| Alamat lokal | `http://localhost:8080/biji-sangrai/index.html` |

## 1 · Soal "masuk pakai akun Gmail saya"

Ini yang bisa dan tidak bisa saya lakukan, tanpa dibungkus:

| Yang diminta | Kenyataan |
| --- | --- |
| Masuk ke jiro.build dengan akun Gmail pemilik | **Tidak dikerjakan.** Saya tidak punya sandi akun itu, tidak akan memintanya, dan tidak akan memakai kredensial yang tidak diberikan. |
| Melihat isi template | **Bisa.** Halaman itu ternyata terbuka untuk publik tanpa login — struktur, urutan bagian, dan ritme tipografinya terbaca. |
| "View Code" / "Copy Prompt" | **Tidak dibuka.** Itu bagian berbayar (lifetime $384 → $179). Saya tidak melewati paywall. |

Jadi yang saya pakai adalah **pelajaran bentuk dari halaman publiknya**, bukan
kode atau prompt di balik paywall. Tidak ada satu kata, satu gambar, atau satu
baris kode dari sana yang disalin. Yang ditiru adalah urutan bagiannya — dan itu
memang hal yang lazim dipelajari dari halaman mana pun yang terbuka.

## 2 · Struktur: apa yang dipinjam, apa yang diganti

Template itu portofolio motion artist: nama besar, portrait, layanan, proses,
penghargaan, angka, pengalaman kerja, testimoni, lalu ajakan kerja sama. Untuk
toko biji kopi, bagian yang tidak punya datanya saya buang — bukan diisi karangan.

| Bagian template | Di halaman ini | Alasan |
| --- | --- | --- |
| Nama besar + portrait reveal | **NOCTURNE / Koffie** + label Blue Mount Ijen yang tersibak | Bahan asli brand, bukan foto sewaan |
| Pernyataan panjang menyala kata demi kata | Kutipan `brand.intro` dari katalog | Sumbernya data, bukan copy baru |
| "What I offer" 5 layanan | 5 hal yang benar-benar dikirim: single origin, blend, giling, langganan, paket & grosir | Semua ada di katalog |
| "How I work" 4 langkah | Pesan → sangrai → kemas → kirim | Mengikuti alur nyata, penyangraian oleh Ais Coffee Roastery |
| **Awards** (tabel penghargaan) | **Tabel biji & harga** 9 SKU | Nocturne belum punya penghargaan. Mengarang penghargaan = berbohong. |
| Angka besar: 12+ tahun, 96%, 3,7× | 9 biji · 4 ukuran · 5 level sangrai · mulai Rp23.000 | Semua dihitung dari katalog |
| Pengalaman kerja (timeline) | Tidak dipakai | Tidak ada riwayat yang bisa dibuktikan |
| **Testimoni** (carousel) | **Catatan rasa** 9 biji, bisa digeser | Testimoni tanpa pembeli nyata = palsu. Interaksinya tetap ada, isinya jujur. |
| Galeri video | Pita label 9 biji | Aset yang memang ada |
| "Let's work together" + jam lokal | "Pilih biji. Kami sangrai." + jam Banyuwangi (WIB) | Jamnya nyata, `Asia/Jakarta` |

## 3 · Yang berubah dari brief brand

| Hal | Sebelum | Di halaman ini |
| --- | --- | --- |
| Latar | kertas `#F5EFE4` | ink `#16110D` — **token yang sama, dibalik** |
| Teks | ink | paper |
| Aksen | burnt orange | burnt orange + roast gold (tidak berubah) |
| Huruf | Bricolage / Fraunces / Inter | sama, kali ini **lokal** dari `assets/fonts/` |
| Motto | "Terjaga untuk rasa yang sesungguhnya." | tetap di beranda; halaman ini menjual biji, jadi judulnya nama brand |

Tidak ada token warna baru. Warna di `toko.css` diperiksa gerbang: setiap hex
harus ada di `data/design-system.json#warna.boleh_dipakai`.

## 4 · Yang diperiksa mesin

`python3 tools/periksa.py` → cek **Biji sangrai**:

| Butir | Cara |
| --- | --- |
| Nama & harga setiap biji tampil | dicocokkan ke `catalog.json` |
| Tidak ada harga asing | semua `Rp…` di halaman harus ada di katalog |
| Tidak ada klaim terlarang | "roastery kami", "termurah", "best seller", "diskon" |
| Warna hanya token | hex di `toko.css` ⊆ `design-system.json` |
| Tanpa CDN | tolak `fonts.googleapis`, `cdn.`, `unpkg`, `jsdelivr` |
| Hormat reduced-motion | `prefers-reduced-motion` wajib ada di CSS |
| **Judul hero tidak meluap** | lebar "NOCTURNE" diukur dengan font asli pada 360–1920 px |
| Berkas tidak basi | hasil halaman dibandingkan dengan hasil generate ulang |

Uji negatif yang sudah dijalankan:

| Percobaan | Hasil |
| --- | --- |
| Ganti `Rp23.000` → `Rp19.000` | gagal: "harga mulai Raung (Rp23.000) tidak tampil" + "harga Rp19.000 tidak ada di katalog" |
| Naikkan judul ke `11vw` | gagal di 860/1024/1280/1440/1920 px ("judul hero meluap") |

Ukuran judul karena itu bukan selera: Bricolage 800 menulis "NOCTURNE" selebar
**5,6 × ukuran huruf**. Kolom kiri pada 1440 px hanya 673 px → batas 118 px.
Dipakai `clamp(3rem, 8.15vw, 7.3rem)`; di ponsel `clamp(3rem, 15vw, 5.2rem)`.

## 5 · Isi halaman

| # | Bagian | Isi |
| --- | --- | --- |
| 1 | Hero | label mikro, judul besar, satu paragraf, 2 tombol, label Blue Mount Ijen tersibak, jam WIB |
| 2 | Pita | 9 label biji bergulir (dua kali untuk putaran mulus, berhenti saat disentuh) |
| 3 | Tentang | `brand.intro`, kata menyala saat digulir; 3 kolom: yang dijual / dijaga / tidak diklaim |
| 4 | Yang dikirim | 5 baris bernomor |
| 5 | Proses | 4 langkah |
| 6 | Biji & harga | tabel 9 SKU: daerah, ketinggian, proses, catatan rasa, harga mulai, tombol pesan WA per biji |
| 7 | Angka | 4 angka berjalan, semuanya dari katalog |
| 8 | Catatan rasa | 9 kutipan rasa dari label asli, geser dengan tombol/panah usap |
| 9 | Penutup | ajakan, WhatsApp + email, jam WIB, tautan ke beranda/kampanye/B2B |

Tombol pesan menyusun pesan WhatsApp otomatis: *"Halo Nocturne, saya mau pesan
Blue Mount Ijen (Single Origin). Boleh info stok dan tanggal sangrai terbaru?"*

## 6 · Berat & gerak

| Hal | Angka |
| --- | --- |
| CSS | 22 KB |
| JS | 7 KB (tanpa pustaka) |
| Huruf | 5 berkas TTF lokal, `font-display:swap` |
| Gambar di atas lipatan | 1 label, 166 KB |
| Total di atas lipatan (perkiraan) | ± 460 KB, batas 1.500 KB |

Gerak: judul naik dari topeng, label tersibak, kata menyala, angka berjalan,
pita bergulir, kutipan bergeser. Semuanya berhenti kalau
`prefers-reduced-motion: reduce` — termasuk pita yang berubah jadi bisa digeser
manual, dan kata yang langsung menyala penuh.

## 7 · Batas jujur

1. **Tidak ada tangkapan layar browser.** Chromium tidak bisa dipasang di sandbox
   (`libnspr4.so` hilang) dan WeasyPrint pun gagal karena Pango tidak ada. Jadi
   yang saya punya: ukuran huruf yang diukur, struktur HTML yang lolos parser,
   13 uji jsdom, dan gerbang 24 cek. Tampilan akhir tetap harus dilihat di browser
   pemilik.
2. **Tidak boleh dipakai sebagai janji.** Halaman menyebut "disangrai mingguan",
   "giling dekat waktu kirim" — ini mengikuti dokumen operasional, bukan hasil
   audit. Kalau jadwalnya berubah, teks di `tools/roasted.py` yang harus diubah.
3. **Testimoni dan penghargaan tidak dibuat.** Dua bagian yang paling mudah
   dipalsukan di template semacam ini justru saya kosongkan lalu isi dengan data.
4. **Harga mengikuti katalog.** Kalau `data/catalog.json` berubah, jalankan
   `python3 tools/roasted.py` lalu `python3 tools/periksa.py`.

## 8 · Versi satu berkas untuk dibuka dari folder unduhan

Gejala yang dilaporkan pemilik (5 Nov 2026): halaman dibuka dari
`file:///C:/Users/…/Downloads/ssddw.html` dan tampil sebagai HTML mentah —
tanpa gaya, tanpa gerak, gambar rusak.

Sebabnya bukan CSS-nya hilang, tapi **berkasnya terpisah**: `index.html`
menautkan `toko.css`, `toko.js`, dan `../assets/…`. Begitu HTML-nya diunduh
sendirian ke folder Downloads, ketiga tautan itu menunjuk ke tempat kosong.

Solusi: `python3 tools/luring.py` → **`biji-sangrai/biji-sangrai-luring.html`**
(975 KB), satu berkas yang berisi:

| Isi | Cara disisipkan |
| --- | --- |
| `toko.css` | `<style>` di dalam berkas |
| Huruf | `data:font/ttf;base64` — dipangkas ke karakter yang dipakai |
| `toko.js` | `<script>` di akhir `<body>` |
| 9 label biji | `data:image/jpeg;base64`, diperkecil ke 340 px, kualitas 68 |
| favicon | `data:image/svg+xml;base64` |
| Tautan antar-halaman | diubah ke `https://nocturnekoffie.id/…` supaya tetap bisa diklik |

Berkas ini **hanya untuk pratinjau/berbagi**. Situs sesungguhnya tetap memakai
berkas terpisah (`index.html` + `toko.css` + `toko.js` + `assets/`), karena
versi tunggal mengubah gambar jadi base64 yang tidak bisa di-cache peramban.

Dua cara membuka yang benar:

| Cara | Perintah / langkah |
| --- | --- |
| Berkas tunggal | klik dua kali `biji-sangrai-luring.html` — cukup, tidak butuh server |
| Situs asli | `python3 -m http.server 8080` di folder proyek, buka `localhost:8080/biji-sangrai/` |

Gerbang: cek **Berkas luring** di `periksa.py` menolak bila masih ada aset
bertautan relatif, CSS/JS belum disisipkan, `@font-face` hilang,
`prefers-reduced-motion` hilang, tautan WhatsApp hilang, ada biji yang lenyap,
atau ukuran melewati 2 MB.

