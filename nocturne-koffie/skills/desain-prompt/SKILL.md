# Prompt Kelas Atas — Halaman yang Terasa Dirancang

Sumber gagasan: dua pustaka prompt berbayar yang populer di kalangan *vibe coder*
(**motionsite.ai** dan **jiro.build**), ditambah lima repo GitHub berlisensi terbuka yang
isinya setara. Skill ini mengubah cara menulis brief desain: bukan "buatkan hero yang cantik",
melainkan spesifikasi yang tokennya bisa diperiksa mesin.

Hasil kerja: `prompts/pustaka.json` (9 prompt) → `prompts/index.html` (galeri, tombol salin).

## Kapan dipakai

- Membangun halaman baru (hero, katalog, produk, langganan, B2B, editorial, kampanye).
- Merombak halaman yang "terasa template" tanpa mengubah token brand.
- Menyiapkan brief untuk agen koding lain (Claude Code, Cursor, v0, Bolt, Lovable) supaya
  keluarannya bisa ditebak, bukan undian.
- Menolak permintaan "buat yang kayak di Instagram itu": referensi harus jadi spesifikasi.

Jangan pakai untuk: film/klip (`motion-film`), gerak di halaman (`motion-web`), atau desain
kemasan (`brand/`).

---

## 1 · Yang benar-benar bisa diambil dari dua platform itu

Keduanya menjual **prompt + source code**, bukan template gratis. Status nyata, diperiksa
30 Okt–5 Nov 2026:

| Platform | Isi publik | Harga | Yang bisa saya lakukan |
| --- | --- | --- | --- |
| **motionsite.ai** | 570+ item: template, section (hero), background. Halaman detail memuat deskripsi, kategori, tag (`#Dark`, `#Glassmorphism`, `#Luxury`), dan tombol "Access prompt and source" | $19/item · $99/tahun · $199 seumur hidup | Melihat **anatomi publik**: kategori, tag, dan bagaimana mereka mendeskripsikan gaya. Teks prompt-nya tidak terbuka |
| **jiro.build** | 1.317 komponen + 137 template, dikelompokkan per industri (Agency, Hospitality, Portfolio, Local Services…). Halaman detail **merender hasil jadinya** (header, hero, menu, CTA, footer) dengan tombol "Copy Prompt" dan "View Code" | $48/3 bulan · $99/tahun · $384→$179 seumur hidup | Melihat **struktur keluaran**: urutan bagian, ritme tipografi, pola CTA, cara mereka menyusun tabel menu. Teks prompt tetap di balik akun berbayar |

**Kenapa tidak saya salin.** Dua alasan, dan keduanya harus disebut terang-terangan:

1. **Teknis.** Prompt dirender di klien setelah akun terverifikasi. Tanpa akses mentah HTML/JS,
   yang bisa saya baca hanyalah teks halaman. Sandbox ini juga hanya punya jalan keluar ke
   GitHub/npm/PyPI, jadi tidak ada cara mengambil aset dari domain mereka.
2. **Etis.** Isinya produk berbayar. Menyalinnya lewat akun yang tidak dibayar berarti mengambil
   barang dagangan orang. Saya tidak melakukannya, dan tidak akan menyarankannya.

Pendaftaran akun pun tidak saya kerjakan: saya tidak punya alamat email Anda, verifikasi akun
butuh Anda mengeklik tautan di kotak masuk, dan akses premium butuh pembayaran. Kalau Anda mau
langganan, itu keputusan Anda — setelah itu prompt-nya bisa ditempel sendiri ke galeri ini.

## 2 · Penggantinya: lima repo terbuka yang benar-benar dipakai

Bentuk (bukan isi) pustaka di sini diambil dari repo berlisensi jelas. Semuanya sudah diperiksa
lisensinya, bukan ditebak dari README.

| Repo | Bintang | Lisensi | Yang diambil |
| --- | ---: | --- | --- |
| `superdesigndev/superdesign-prompts` | 38 | **prompt CC0**, kode MIT | Anatomi tujuh blok + tingkat kekhususan (hex persis, `clamp()`, easing bernama, aturan per bagian). 140 prompt, semuanya spesifikasi penuh — inilah padanan terbuka paling dekat dengan Jiro |
| `superdesigndev/superdesign-skill` | 945 | MIT | Alur "baca UI sekarang → cari spesifikasi → terapkan token" |
| `oil-oil/oil-ui` | 2.783 | MIT | Urutan kerja: fakta produk → struktur grayscale → implementasi → tinjau tangkapan layar nyata. Satu arah per brief, bukan lima |
| `Ilm-Alan/frontend-design` | 157 | MIT | "Satu jangkar estetika per brief": pilih satu wilayah visual dan taati tokennya; hibrida = kesalahan kategori |
| `ihlamury/design-skills` | 105 | MIT | Batasan UI yang diambil dari design system nyata (skala, jarak, kontras) |

Repo lain yang saya lihat tapi tidak dipakai, supaya tidak ada yang diklaim berlebih:
`vercel-labs/agent-skills` & `vercel-labs/design-systems-to-agent-skills` (rujukan struktur skill),
`edisonmbli/refactoring-ui-skill` (367 aturan, terlalu berat untuk dipakai harian),
`mistyhx/frontend-design-audit`, `wilwaldon/Claude-Code-Frontend-Design-Toolkit` (kumpulan tautan),
`Ghufrnainun/curated-design` (indeks, bukan prompt).

Pelajaran dari kedua platform berbayar yang **boleh** dipakai karena terlihat publik:
kategori per industri, urutan bagian yang konsisten (header → hero → bukti → penawaran → FAQ →
footer), satu ajakan utama per halaman, dan janji "keluaran identik di semua builder" yang hanya
bisa dicapai kalau prompt menyebut angka, bukan kata sifat.

## 3 · Anatomi tujuh blok

| Blok | Isi | Contoh buruk | Contoh yang dipakai di sini |
| --- | --- | --- | --- |
| `ringkasan` | Satu paragraf: apa, untuk siapa, kesan setelah 3 detik | "Hero modern dan elegan" | "Hero dua kolom yang menaruh nama kopi dan asalnya sebagai objek tipografis utama…" |
| `gaya` | Hex, keluarga font, skala `clamp()`, radius, tekstur | "warna hangat" | `--paper #F5EFE4`, Bricolage 800 `clamp(2.6rem,7.2vw,6.6rem)`, `letter-spacing -0.035em` |
| `tata_letak` | Per bagian, urutan, lebar kolom, perilaku mobile | "responsif" | "kolom 1.05fr / 0.95fr, jarak `clamp(24px,4vw,56px)`, di bawah 900 px satu kolom" |
| `komponen` | Elemen yang mudah dirusak agen | "kartu produk" | "pemilih gramasi sebagai radio asli, harga rata kanan `tabular-nums`" |
| `gerak` | Durasi, easing, properti, reduced-motion | "animasi halus" | `cubic-bezier(.16,1,.3,1)`, stagger 90 ms, hanya transform & opacity |
| `copy` | Teks yang harus muncul apa adanya + larangan klaim | "tulis copy menarik" | "Kopi dari petani." / "Disangrai mingguan oleh Ais Coffee Roastery di Banyuwangi." |
| `kriteria_terima` | Butir yang bisa diperiksa mesin | "harus bagus" | "9 baris produk identik dengan `data/catalog.json`; kontras ≥ 12:1" |

Aturan penguat: **satu jangkar estetika per prompt**, **satu ajakan utama per halaman**, dan
**tidak ada angka tanpa sumber**.

## 4 · Prosedur

1. Tentukan halaman & satu kalimat tujuan (`prompts/pustaka.json#prompts[].ringkas`).
2. Ambil token dari `data/design-system.json` dan angka dari `data/catalog.json`. Jangan
   mengetik ulang harga — salin dari katalog.
3. Pilih jangkar estetika. Untuk Nocturne jangkar itu sudah ditetapkan brief: kertas krem,
   tipografi editorial, satu aksen oranye. Variasi boleh pada komposisi, bukan pada token.
4. Tulis prompt dengan tujuh blok. Panjang wajar 1.800–2.200 karakter; di bawah 1.200
   hampir pasti kehilangan salah satu blok.
5. Jalankan `python3 tools/prompt.py --cek` — gerbang menolak warna di luar token, harga yang
   tidak ada di katalog, klaim terlarang, prompt terlalu pendek, kriteria terima kurang dari 4.
6. `python3 tools/prompt.py` → `prompts/prompts.json` + `prompts/index.html`.
7. Tempel ke agen koding, lalu **nilai hasilnya dengan mata di tangkapan layar**, bukan dari
   kode. Prompt yang lolos gerbang masih bisa menghasilkan halaman jelek.

## 5 · Larangan global (ikut semua prompt)

1. Jangan menyebut Nocturne sebagai roastery — penyangraian oleh Ais Coffee Roastery.
2. Jangan mengarang angka: harga, ketinggian, rating, jumlah pelanggan, tanggal sangrai.
3. Jangan menambah warna di luar `boleh_dipakai`.
4. Jangan memuat pustaka dari CDN.
5. Jangan membuat ulasan atau testimoni fiktif.
6. Jangan memakai hitung mundur, "stok terbatas", atau harga coret yang tidak bisa dihitung.
7. Jangan memakai foto orang minum kopi sebagai hero; hero memakai produk atau tipografi.

## 6 · Sembilan prompt yang ada sekarang

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

Nomor karakter dihitung ulang oleh `tools/prompt.py`; kalau berbeda sedikit, percayai berkas.

## 7 · Cara menambah prompt

1. Salin satu objek di `prompts/pustaka.json`.
2. Isi tujuh blok. `prompt` adalah satu paragraf panjang — itu yang disalin pengguna.
3. `python3 tools/prompt.py --cek`. Perbaiki sampai 0 masalah.
4. `python3 tools/prompt.py` lalu `python3 tools/periksa.py` (cek **Prompt kelas atas**).

## 8 · Bukti & batas

| Yang bisa dibuktikan | Perintah / berkas |
| --- | --- |
| 9 prompt, 7 blok, 0 masalah | `python3 tools/prompt.py --cek` |
| Token patuh (tidak ada hex liar) | `periksa.py` cek *Prompt kelas atas* |
| Harga di prompt ada di katalog | `tools/prompt.py` §harga |
| Galeri bisa disalin | `prompts/index.html`, tombol `Salin prompt` |

Yang **tidak** bisa dibuktikan di sini: hasil render halaman dari prompt (tidak ada browser),
dan isi prompt motionsite/jiro (berbayar). Jangan menulis di laporan mana pun bahwa keduanya
sudah dibaca isinya.
