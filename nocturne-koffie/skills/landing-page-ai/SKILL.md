---
name: landing-page-ai
description: Prosedur membangun landing page kelas atas dengan agen AI — dari brief, DESIGN.md, rencana layar, sampai gerbang kualitas yang bisa diperiksa mesin. Dipakai saat membuat halaman baru, merombak halaman yang terasa template, atau meminta agen lain (Claude Code, Cursor, v0, Lovable) membangun halaman Nocturne.
---

# Landing page dengan agen AI — yang menentukan hasil, dan yang harus ditolak

Sumber, semuanya ≥ 3.000 bintang, diperiksa 5 Nov 2026:

| Repo | Bintang | Isi nyata (bukan klaim) | Yang diambil | Yang ditolak |
| --- | --- | --- | --- | --- |
| [`nextlevelbuilder/ui-ux-pro-max-skill`](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) (MIT) | 145.433 | 80 gaya UI, 192 palet produk, **74 pasangan huruf**, 119 pedoman UX, 105 ikon, 25 tipe grafik, 22 stack; data CSV lokal + skrip pencarian Python tanpa dependensi | urutan prioritas: aksesibilitas → sentuh → performa → gaya → tata letak → huruf/warna; `typography.csv` & `google-fonts.csv` (1.935 keluarga) sebagai rujukan pemilihan huruf | pemasangan plugin & CLI npm; skrip `search.py` (datanya saya baca langsung dari CSV) |
| [`Leonxlnx/taste-skill`](https://github.com/Leonxlnx/taste-skill) (MIT) | 110.288 | skill anti-slop dengan **9 aturan rumah**: satu bagian per layar, tepi kiri-kanan sama, satu sistem (satu tombol, satu radius, satu hairline), foto nyata, hover 2px, alamat tanpa nomor rumah; plus pemeriksa `consistency.mjs` di peramban sungguhan | 9 aturan rumah, tabel tinggi bagian (495–708 px = satu layar), larangan **efek shader untuk kafe/toko** — "kafe lokal dapat foto, bukan efek", aturan huruf 16 px minimum | pemeriksa berbasis Chromium (tidak ada Chromium di sandbox ini), 1.648 berkas aset & shader GLSL |
| [`VoltAgent/awesome-design-md`](https://github.com/VoltAgent/awesome-design-md) (MIT) | 125.697 | 84 berkas `DESIGN.md` hasil analisis situs nyata (Claude, ElevenLabs, Runway, …): token, aturan, pola | gagasan **satu berkas DESIGN.md di akar proyek** yang dibaca agen sebelum menulis apa pun | berkas DESIGN.md milik merek lain — menyalinnya berarti menyalin identitas |
| [`coreyhaines31/marketingskills`](https://github.com/coreyhaines31/marketingskills) (MIT) | 58.612 | 51 skill marketing: **cro**, copywriting, offers, pricing, seo-audit, schema, launch | urutan diagnosis CRO: nilai → judul → tawaran → bukti → gesekan; disiplin "uji dulu, baru ubah desain" | integrasi akun iklan, analitik, dan kredensial berbayar |
| [`nateherkai/scroll-craft`](https://github.com/nateherkai/scroll-craft) (MIT) | 4.555 | skill situs scroll-driven | pola scroll yang tenang (satu gerak per bagian) | animasi scroll panjang per kartu |

## Kapan dipakai

- Membangun halaman baru: hero, katalog, produk, B2B, kampanye.
- Merombak halaman yang "terasa template" tanpa mengubah token brand.
- Menulis brief untuk agen koding lain supaya keluarannya bisa ditebak.
- Menolak permintaan "buat kayak di Instagram itu" — referensi harus jadi spesifikasi.

## 1 · Urutan kerja yang tidak boleh dibalik

```
brief (satu paragraf, jenis situs)  →  DESIGN.md (token + aturan)
   →  rencana layar (daftar bagian + tinggi)  →  copy (kata dulu, gambar kemudian)
   →  bangun (satu sistem CSS)  →  gerbang (mesin)  →  mata (foto, tepi, layar)
```

Alasan: agen tanpa `DESIGN.md` akan mengarang token baru di tengah jalan — itu penyebab nomor satu halaman
terasa campur-campur. Proyek ini sudah punya DESIGN.md dalam bentuk `assets/css/site.css` (`:root`) — jangan
membuat sistem kedua.

## 2 · Tentukan jenis halaman sebelum apa pun

| Brief | Jenis | Yang memimpin tata letak | Yang **dilarang** |
| --- | --- | --- | --- |
| Kopi biji dijual daring, tanpa pintu fisik | **produk** | render/foto produk besar, satu gambar berbeda per bagian | efek shader, grain, gradien dekoratif |
| Kafe/pintu fisik | **tempat** | 12–20 foto, blok kunjungan di layar kedua, jam buka | efek, loop, diagram, korsel |
| Layanan/jasa | **layanan** | orang, ruang, pekerjaan; ikon asli; satu diagram diam | adegan WebGL |
| Perangkat lunak/alat AI | **teknis** | UI produk sendiri sebagai HTML hidup | — (efek boleh, maksimal satu) |

Nocturne = **produk** (biji sangrai, dikirim). Konsekuensinya tegas: **tanpa shader, tanpa grain, tanpa gradien
dekoratif**; yang bekerja adalah foto/render, kertas, huruf besar, dan satu garis.

## 3 · Rencana layar (angka, bukan selera)

| Ukuran | Aturan | Angka acuan |
| --- | --- | --- |
| Tinggi bagian | tepat 1 atau 2 layar, tidak boleh `min-height` saja | 708 px = satu layar pada 1440×900 |
| Isi terlalu pendek | < 360 px → gabung ke bagian sebelumnya atau tambahkan gambarnya | |
| Isi 360–495 px | masih satu layar, tapi beri peringatan: bagian ini kurang gambar | |
| Isi 708–1.320 px | tidak ada tinggi yang pas → potong ke 708, pecah dua, atau pakai dua kolom | |
| Teks | minimal 16 px untuk teks yang dibaca, tinggi baris 1,5–1,8, maksimal 62 karakter per baris | |
| Ritme | 4, 8, 12, 16, 24, 32, 48, 64, 96, 128 — tidak ada angka lain | |
| Satu sistem | satu bentuk tombol, satu keluarga radius, satu hairline, satu gaya tautan | |
| Gerak | kartu terangkat 2 px, foto zoom 1,02–1,03, garis bawah menggambar; tanpa tilt, korsel, tab berwaktu | |
| Huruf | satu pasangan untuk seluruh situs, 4 gerbang | lihat skill `pasangan-font` |

## 4 · Copy dulu, gambar kemudian

Urutan diagnosis CRO (dari `marketingskills/skills/cro`, diurut menurut dampak):

| # | Yang diperiksa | Pertanyaan yang harus dijawab di layar pertama |
| --- | --- | --- |
| 1 | Kejelasan nilai | Apa yang dijual dan kenapa peduli — dalam 5 detik |
| 2 | Judul | Spesifik, menyebut biji/asal/penyangrai, bukan "kopi terbaik" |
| 3 | Tawaran | Ukuran, harga, ongkir, jaminan — terlihat sebelum scroll |
| 4 | Bukti | Nama petani, desa, ketinggian, tanggal sangrai (data `catalog.json`) |
| 5 | Gesekan | Jumlah langkah ke pesan, jumlah isian formulir |

Aturan copy yang mengikat proyek ini: kalimat pendek, kata benda konkret, tanpa superlatif kosong, tanpa
angka karangan, tanpa "roastery" (penyangraian oleh Ais Coffee Roastery Banyuwangi).

## 5 · Gerbang: yang diperiksa mesin, dan yang tidak

| Diperiksa mesin | Alat |
| --- | --- |
| tautan lokal mati, tag tak seimbang | `tools/periksa.py` (27 butir) |
| bobot huruf tanpa berkas (huruf sintetis) | `tools/periksa.py` butir **Huruf lokal** |
| berat halaman awal < 1.500 KB, tanpa CDN | `tools/periksa.py` |
| klaim terlarang, angka vs `catalog.json` | `tools/periksa.py`, `tools/verifikasi-biji.mjs` |
| poster menyatu dengan kertas, 4 sudut | `tools/biji_render.py` |

| **Tidak bisa** diperiksa mesin di sini | Cara menutupnya |
| --- | --- |
| satu bagian per layar pada 390/768/1440 sungguhan | tidak ada peramban di sandbox — diperiksa mata pemilik; sediakan `semua.html` |
| foto terasa hidup | hanya foto nyata; render hanya untuk produk |
| huruf terasa pas | skill `pasangan-font` + halaman contoh |

## 6 · Yang harus ditolak dari agen AI

Tanda keluaran mesin yang paling sering lolos tanpa diperiksa:

- Tiga gradien ungu-biru di hero, atau "glow" di belakang judul.
- Ikon emoji sebagai ikon.
- Korsel, tab berwaktu, popup newsletter, tombol "back to top".
- Angka bulat karangan: "10.000+ pelanggan", "99% suka".
- Huruf script untuk badan teks, atau dua pasangan huruf berbeda di satu halaman.
- Teks di dalam gambar (tidak terbaca mesin pencari, tidak bisa diterjemahkan).
- Bagian yang tingginya diatur JavaScript.

## 7 · Perintah

```bash
python3 tools/periksa.py        # gerbang 27 butir
python3 tools/semua.py          # pintu tunggal 14 halaman
python3 tools/pratinjau.py      # tangkapan hero jadi PNG (bisa dibuka tanpa peramban)
```
