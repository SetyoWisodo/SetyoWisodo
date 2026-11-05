# Pustaka prompt kelas atas — status & asal-usul

Diperbarui 5 November 2026 · sumber: `prompts/pustaka.json`, `prompts/prompts.json`,
`skills/desain-prompt/SKILL.md`, `data/catalog.json`, `data/design-system.json`.

Permintaannya: **jelajahi motionsite.ai dan jiro.build untuk prompt pembuatan website yang sangat
berkelas; kalau tidak bisa disalin, cari gaya prompt itu di GitHub dan platform terkait.**

Jawaban singkat: **halaman-halamannya bisa saya baca, isi prompt-nya tidak.** Keduanya menaruh
prompt di balik akun berbayar. Yang saya lakukan: memetakan anatomi publiknya, lalu membangun
pustaka prompt sendiri dengan bentuk yang sama, memakai repo berlisensi CC0/MIT, dan mengisinya
dengan data Nocturne. Hasilnya 9 prompt, 17.542 karakter, 0 masalah di gerbang.

## 1 · Apa yang benar-benar ada di dua platform itu

| | motionsite.ai | jiro.build |
| --- | --- | --- |
| Isi | 570+ item: template, section (hero), background | 1.317 komponen + 137 template, dikelompokkan per industri |
| Yang dijual | prompt + source code | prompt + source code (+ ekstensi Chrome, MCP) |
| Harga | $19/item · $99/tahun · $199 seumur hidup | $48/3 bulan · $99/tahun · $384→$179 seumur hidup |
| Yang terbuka untuk publik | deskripsi, kategori, tag (`#Dark`, `#Glassmorphism`, `#Luxury`), daftar "perfect for" | **hasil render** tiap template: header, hero, menu, CTA, footer |
| Yang tertutup | teks prompt | teks prompt + kode |

Contoh yang saya buka: `motionsite.ai/templates/basilico-restaurant` (deskripsi gaya: dark mode,
glassmorphism, tipografi mewah) dan `jiro.build/templates/local-services/restaurant-landing-page-rumindo`
(susunan nyata: nama besar bertumpuk, label berulang untuk efek gerak, tabel menu 60 item, dua kartu
promo, CTA di kepala dan kaki). Keduanya memberi **bentuk**, bukan teks.

## 2 · Kenapa tidak saya salin, dan kenapa akun tidak saya buat

| Alasan | Keterangan |
| --- | --- |
| Teknis | Prompt dirender setelah akun terverifikasi; tanpa akses mentah HTML/JS, yang terbaca hanya teks halaman. Sandbox ini juga hanya punya jalan keluar ke GitHub/npm/PyPI |
| Etis | Isinya produk berbayar. Menyalin lewat akun yang tidak dibayar = mengambil barang dagangan orang |
| Praktis | Saya tidak punya alamat email Anda, verifikasi butuh Anda mengeklik tautan, dan premium butuh pembayaran. Saya tidak bisa membayar, dan tidak akan memakai kartu siapa pun |

Kalau Anda berlangganan nanti, prompt-nya bisa ditempel ke `prompts/pustaka.json` dan galeri
langsung menampilkannya.

## 3 · Repo yang saya jelajahi (dan yang dipakai)

| Repo | Bintang | Lisensi | Status |
| --- | ---: | --- | --- |
| `superdesigndev/superdesign-prompts` | 38 | **prompt CC0**, kode MIT | **dipakai** — anatomi 7 blok, 140 prompt spesifikasi penuh; padanan terbuka terdekat dengan Jiro |
| `superdesigndev/superdesign-skill` | 945 | MIT | **dipakai** — alur baca UI → cari spesifikasi → terapkan token |
| `oil-oil/oil-ui` | 2.783 | MIT | **dipakai** — urutan: fakta produk → grayscale → implementasi → tinjau tangkapan layar |
| `Ilm-Alan/frontend-design` | 157 | MIT | **dipakai** — satu jangkar estetika per brief |
| `ihlamury/design-skills` | 105 | MIT | **dipakai** — batasan dari design system nyata |
| `vercel-labs/agent-skills`, `vercel-labs/design-systems-to-agent-skills` | 33.562 / 46 | MIT | rujukan struktur skill, tidak disalin |
| `edisonmbli/refactoring-ui-skill` | 367 | — | dilihat; terlalu berat untuk harian |
| `mistyhx/frontend-design-audit` | 99 | — | dilihat; untuk audit, bukan penulisan prompt |
| `wilwaldon/Claude-Code-Frontend-Design-Toolkit` | 1.270 | — | kumpulan tautan, bukan prompt |
| `Ghufrnainun/curated-design` | — | — | indeks sumber, bukan prompt |

Pencarian GitHub untuk `"jiro.build"` menemukan 185 berkas — sebagian besar artikel dan daftar
tautan, bukan salinan prompt. Tidak ada yang saya pakai sebagai bahan prompt.

## 4 · Sembilan prompt yang dihasilkan

| # | id | Halaman | Karakter | Inti |
| ---: | --- | --- | ---: | --- |
| 01 | `hero-beranda` | `index.html` | 2.064 | Tipografi raksasa + satu foto produk |
| 02 | `hero-biji-3d` | `index.html` | 2.607 | Satu biji 3D yang bisa diputar & disentuh |
| 03 | `menu-katalog` | `katalog.html` | 2.322 | Sembilan SKU sebagai tabel editorial |
| 04 | `produk-gayo` | `produk/gayo.html` | 1.971 | Data petani sebagai keterangan teknis |
| 05 | `cerita-ais` | `cerita.html` | 1.719 | Esai + garis waktu, Ais sebagai mitra |
| 06 | `langganan` | `langganan.html` | 1.782 | Ritme kirim, aritmetika terlihat |
| 07 | `b2b-grosir` | `grosir.html` | 1.680 | Tabel harga bertingkat yang bisa diaudit |
| 08 | `panduan-seduh` | `seduh.html` | 1.667 | Tiga metode, siap dicetak |
| 09 | `kampanye-ongkir` | `kampanye/ongkir.html` | 1.730 | Satu tawaran, satu tombol |

Total 17.542 karakter · rata-rata 1.949 · semua lolos gerbang.

## 5 · Gerbang yang menjaga mutu

`python3 tools/prompt.py --cek` menolak:

| Uji | Kenapa penting |
| --- | --- |
| prompt < 1.200 karakter | di bawah itu hampir pasti satu blok hilang |
| hex di luar `boleh_dipakai` | mencegah warna baru menyusup lewat prompt |
| harga Rp yang tidak ada di katalog | mencegah angka karangan |
| klaim terlarang (`roastery kami`, `termurah`, diskon tanpa sumber) | menjaga kejujuran brand |
| kata kosong (`seamless`, `unleash`, `crafted with love`) | mencegah prompt bergaya iklan |
| kriteria terima < 4 atau tanpa `reduced_motion` | memastikan hasilnya bisa diperiksa |

Catatan penting: pemindaian dilakukan **per kalimat afirmatif** — prompt memang boleh menulis
"jangan sebut roastery kami" karena itu instruksi, bukan klaim.

## 6 · Batas

- **Tidak ada hasil render.** Prompt belum pernah dijalankan ke agen koding di sandbox ini (tidak ada
  browser). Yang bisa dibuktikan: strukturnya lengkap, tokennya patuh, angkanya dari katalog.
- **Prompt motionsite & jiro tidak dibaca.** Jangan menulis di materi mana pun bahwa keduanya sudah
  diambil isinya.
- **Galeri memakai Google Fonts** untuk tampilan, sama seperti halaman lain di repo ini. Halaman
  publik (`index.html`) tetap tanpa pustaka mesin.

## 7 · Perintah

```bash
python3 tools/prompt.py --cek    # validasi 9 prompt
python3 tools/prompt.py          # tulis prompts/prompts.json + prompts/index.html
python3 tools/periksa.py         # gerbang penuh, termasuk cek "Prompt kelas atas"
```
