# Nocturne Koffie — Landing Page + Sistem Marketing

Landing page katalog + pintu masuk order WhatsApp untuk **Nocturne Koffie Brand**
(brand kopi Banyuwangi — bukan roastery; sangrai dikerjakan Ais Coffee Roastery).

Dibangun mengikuti **Brief Website FINAL 3.7 (4 Okt 2026)**. Panduan pengerjaan,
spesifikasi komponen, dan daftar data yang masih menunggu konfirmasi ada di
[`panduan/PANDUAN-LANDING-PAGE.md`](panduan/PANDUAN-LANDING-PAGE.md).

```
nocturne-koffie/
├── index.html                    landing page (10 seksi, sesuai brief bagian 05)
├── assets/
│   ├── css/site.css              Paper · Ink · Burnt Orange · Espresso · Roast Gold
│   ├── js/site.js                render katalog, marquee, filter, pesan WhatsApp
│   ├── js/motion.js              lapisan gerak (tanpa library): reveal, parallax, magnet, tilt
│   ├── css/motion.css            token & aturan animasi (situs utama)
│   ├── css/motion-ui.css         komponen gerak: spotlight, count, magnet, pin, ticker
│   ├── js/motion-ui.js           komponen vanilla (adaptasi react-bits) + loop rAF
│   ├── css/motion-3d.css         panggung 3D: kartu berlapis, silinder klip, kartu timbul
│   ├── js/motion-3d.js           kamera kursor + dolly gulir, korsel silinder (tanpa WebGL)
│   └── img/produk/               9 foto stiker kemasan (4:5, dari brief)
├── data/catalog.json             ← SATU-SATUNYA file yang perlu diubah rutin
├── brand/                        logo SVG, OG card, 9 label kantong + lembar A4, brand kit
├── komersial/                    harga grosir 4 tingkat, penawaran B2B, pipeline prospek
├── skills/                       8 skill: riset sosial, komentar, mesin pencari, studio konten,
│                                  motion-web, motion-film, desain-prompt, hero-3d
├── film-studio/                  GSAP · Lottie · Remotion · HyperFrames terpasang (npm, versi dipin)
├── assets/vendor/                gsap 3.15, ScrollTrigger, lottie-web 5.13 (lokal, tanpa CDN)
├── assets/lottie/                nocturne-9s.json — 9 lapisan, 540 frame, 4 penanda cue
├── riset/                        dasbor riset, swipe file, brief konten (hasil generate)
├── studio/                       studio konten 10 tahap: halaman, brief Senin, 5 skrip (hasil generate)
├── motion/                       lab gerak + 5 adegan 9:16 + timeline + lembar film (hasil generate)
├── operasional/                  7 divisi: struktur, alur kerja + target per divisi
│   ├── divisi/                   D1…D7 — satu berkas per divisi
│   └── arsip/                    SOP versi 6 divisi (rujukan sejarah, tidak dipakai)
├── konten/                       hub konten: 5 video 9:16, carousel, story, feed
├── kampanye/index.html           landing page kampanye (hasil generate)
├── tools/papan.py                generator papan harian + tabel target divisi
├── tools/brandkit.py             generator logo, OG card, label kantong (Pillow)
├── tools/komersial.py            generator harga grosir + penawaran B2B
├── tools/kreatif.py              generator video 9:16, carousel, story, hub konten
├── tools/kampanye.py             generator landing page kampanye
├── tools/riset.py                analisis konten ramai, komentar, kata kunci → brief
├── data/studio-niche.json        ceruk, 4 segmen audiens, tangga tawaran, kata terlarang
├── data/studio-hooks.csv         30 hook bertag struktur/pilar/aset + status dipakai
├── data/studio-industri.csv      catatan tren industri (diisi manual)
├── tools/studio.py               studio konten 10 tahap → halaman, brief Senin, 5 skrip
├── data/design-system.json       kontrak token: warna, tipografi, radius, gerak, pengecualian
├── tools/motion.py               lab gerak + 5 adegan 9:16 dari skrip studio
├── tools/film.py                 lembar film: 540 frame, 120 BPM, arc energi, cue suara
├── tools/render_film.py          perender klip 9:16 (540 frame Pillow → ffmpeg H.264)
├── tools/prompt.py               pustaka prompt kelas atas: validasi token → prompts/index.html
├── tools/biji.py                 validasi zona & senyawa biji (perender mesh: lama)
├── tools/biji_render.py          pasang render hiper-realistis → biji-3d-poster.jpg
├── tools/verifikasi-biji.mjs     uji data, poster, titik, markup — 12 butir tanpa peramban
├── tools/pratinjau.py            skema tata letak hero (1280 & 390 px) dari angka CSS
├── semua.html                    SATU pintu: semua halaman, angka gerbang, unduhan
├── biji-sangrai/                 landing roasted beans: toko.css, toko.js, index.html (generated)
├── prompts/                      8 prompt spesifikasi desain + galeri salin sekali klik
├── tools/slop.py                 audit anti-slop (29 aturan) → laporan/slop.md
├── tools/periksa.py              gerbang QA: 26 pemeriksaan konsistensi → laporan/periksa.md
├── tools/roasted.py              halaman penjualan biji sangrai dari katalog → biji-sangrai/
├── tools/luring.py               versi 1 berkas: CSS, JS, huruf & gambar disisipkan
├── tools/semua.py                pintu tunggal: semua.html (14 halaman + unduhan)
├── tools/laporan.py              satu halaman ringkasan → laporan/index.html
├── tools/jalankan.py             jalankan seluruh pipeline berurutan (~96 detik)
├── dashboard/index.html          papan harian hasil generate (jangan diedit manual)
├── panduan/PANDUAN-LANDING-PAGE.md
├── panduan/07-sistem-motion.md
└── marketing/                    strategi, kalender konten, copy, CRM, B2B
```

## Menjalankan

```bash
cd nocturne-koffie
python3 -m http.server 8080        # situs  → http://localhost:8080
                                   # papan  → http://localhost:8080/dashboard/
python3 tools/papan.py             # hitung ulang papan harian
python3 tools/brandkit.py          # buat ulang label + logo (butuh Pillow)
python3 tools/komersial.py         # buat ulang harga grosir + penawaran B2B
python3 tools/kreatif.py           # render 5 video + carousel + story (butuh ffmpeg)
python3 tools/kreatif.py --cepat    # hanya gambar (tanpa encode video)
python3 tools/kampanye.py          # buat ulang landing kampanye dari katalog + manifest
python3 tools/film.py              # lembar film 9 detik: frame, ketukan, arc energi
python3 tools/riset.py             # analisis riset → riset/index.html + swipe file + brief
python3 tools/riset.py --cek       # ringkasan riset tanpa menulis berkas
python3 tools/studio.py            # studio 10 tahap → brief Senin + 5 skrip siap rekam
python3 tools/studio.py --cek      # ringkasan 10 tahap di terminal
python3 tools/motion.py            # lab gerak + 5 adegan 9:16
python3 tools/slop.py              # audit anti-slop & kontrak desain
python3 tools/font.py              # huruf lokal: unduh → kunci sumbu → iris → woff2 → fonts.css
python3 tools/font.py --cek        # 14 halaman tanpa Google Fonts, rentang bobot cocok

python3 tools/jalankan.py          # ← SEMUA langkah di atas, berurutan, + periksa + laporan
python3 tools/jalankan.py --cepat  # lewati encode video (lebih cepat ~15 detik)
python3 tools/periksa.py           # gerbang QA saja (exit 1 bila ada temuan kritis)
```

**Dependensi Python:** `pillow`, `fonttools`, `brotli` (dipasang sekali; sandbox ini
mengosongkannya antar sesi). Tanpa Pillow, `tools/periksa.py` tetap jalan — butir yang butuh
piksel dilewati dengan catatan, bukan gagal. Uji asap `rak/` butuh `jsdom` (`npm i jsdom --prefix /tmp/jsdom`);
tanpa itu butirnya ditandai "dilewati".

`tools/kreatif.py` butuh ffmpeg. Di sandbox: `pip install --break-system-packages imageio-ffmpeg`
(FFmpeg biner tidak ikut tersimpan antar-sesi — generator akan gagal-soft ke gambar saja bila tidak ada,
dan itu dilaporkan di keluaran terminal serta di `data/kreatif.json` → `video_terencode`).

Halaman yang perlu dibuka: `/` (situs) · `/dashboard/` (papan harian) ·
`/kampanye/` (landing kampanye konten) · `/konten/` (hub aset, `noindex`) ·
`/riset/` (dasbor riset konten & kata kunci, `noindex`) ·
`/studio/` (studio konten 10 tahap + brief Senin, `noindex`) ·
`/motion/` (lab gerak + 5 adegan 9:16, `noindex`) ·
`/laporan/` (ringkasan otomatis + hasil pemeriksaan, `noindex`) ·
`/brand/` (brand kit) · `/komersial/penawaran-b2b.html` (proposal B2B).

Harus lewat server — katalog dimuat dengan `fetch`, dan `file://` akan diblokir browser.

## Huruf: dilayani sendiri, bukan dari CDN

Sampai 5 Nov 2026 ke-14 halaman memuat huruf dari `fonts.googleapis.com`. Sekarang
`assets/fonts/` memuat **4 berkas variabel woff2 (231 KB)** — Bricolage Grotesque 600–800,
Fraunces 300–700, Fraunces italic 300–400, Inter 400–700 — dan `assets/css/fonts.css`
mendeklarasikan rentang bobotnya. Dua bobot yang dulu tidak ada (Inter 700, Bricolage 600–700)
kini tersedia, jadi tidak ada lagi huruf tebal sintetis dari peramban.
Sumber: `github.com/google/fonts` (OFL 1.1) · dibangun oleh `tools/font.py`.

## Rak sangrai — hero rak 3D (`rak/`)

Halaman empat berkas: `rak/index.html`, `rak/rak.css`, `rak/rak.js`, `rak/data.js`.
Dua belas lot (9 kopi + 2 paket + kartu member) berdiri di rak; satu ditarik keluar
dan diputar −90° menghadap Anda. Panah, tab kategori, geser, roda, papan tombol,
kursor kustom (cincin → cakram "BUKA / OPEN"), dan lembar detail yang tumbuh dari
sampul dengan tinta menyebar.

| Bagian | Isi |
| --- | --- |
| `tools/rak.py` | membangun dua atlas dari `data/catalog.json`: `assets/img/rak/covers.webp` (1744×2336, 12 kotak 4×3) dan `spines.webp` (2688×1152, 12 kotak sebaris) + `rak/data.js` |
| `tools/rak-uji.mjs` | uji asap tanpa peramban (jsdom): 26 butir — galat JS, jarak punggung, sudut kotak aktif, tab, panah, buka/tutup, harga & WhatsApp dari katalog, tinta |
| `tools/rak-pratinjau.py` | pratinjau komposisi (`laporan/rak-pratinjau.png`, `…-detail.png`) — **perkiraan**, bukan tangkapan peramban |

Gerbang `tools/periksa.py` butir **Rak sangrai**: atlas ada & tidak terlalu berat, harga tidak
diketik di `rak.js`, satu `requestAnimationFrame`, tanpa `@keyframes`, dan uji asap dijalankan
(butir "dilewati" bila jsdom tidak ada).

```bash
python3 tools/rak.py            # bangun atlas + data.js
node tools/rak-uji.mjs          # 26 butir uji asap (butuh: npm i jsdom --prefix /tmp/jsdom)
python3 tools/rak-pratinjau.py  # gambar pratinjau komposisi
```

### Foto kemasan → kemasan 3D (pipa aset)

Foto kemasan **tidak pernah** dipasang langsung di halaman. Alurnya:

```
assets/img/kemasan/sumber/<id>.jpg     foto apa adanya (boleh masih berlatar)
        ↓  tools/kemasan.py
        · buang latar (banjir-warna dua ambang + gerus bayangan/halo)
        · rapikan ke isi, normalisasi tinggi 1200 px
        · bangun kotak bervolume: sisi kanan + sisi atas dari warna tepi kemasan,
          perspektif (tepi kanan memendek, sisi menyusul), cahaya kiri→kanan
        · serong 10° ke kiri, latar transparan, WebP q88
        ↓
assets/img/kemasan/<id>-depan.webp     bidang depan bersih
assets/img/kemasan/<id>-3d.webp        kotak 3D, serong 10° ke kiri, tanpa latar
        ↓  tools/rak.py (otomatis memakai bila ada)
rak (sampul + punggung) · lembar detail
```

| Berkas | Isi |
| --- | --- |
| `tools/kemasan.py` | pipa di atas; `--cek` memeriksa alfa 4 sudut, arah serong **diukur dari hasil** (`cek_serong`), piksel hampir-transparan berwarna menyala, ukuran |
| `assets/img/kemasan/sumber/` | tempat menjatuhkan foto; nama berkas = `id` katalog (`gayo.jpg`, `blue-mount-ijen.png`, …) |
| `data/kemasan.json` | catatan setiap kemasan: sumber, dua keluaran, ukuran, serong |
| `laporan/kemasan-3d.png` | lembar periksa semua kemasan 3D di atas kertas |

```bash
python3 tools/kemasan.py         # proses semua foto di folder sumber
python3 tools/kemasan.py --demo  # contoh dari label brand (tidak menyentuh aset situs)
```

**Batas yang jujur:** tidak ada model penghapus latar berbasis ML di sini. Latar dibuang
dengan banjir-warna, jadi foto berlatar polos (satu warna meja/karton) hasilnya bersih;
foto berlatar ramai akan menyisakan tepi. Efek "3D" adalah kotak bervolume (dua bidang sisi
dari warna tepi + perspektif + gradien cahaya), bukan model 3D sungguhan dengan tekstur.

Batas yang diakui: tidak ada peramban di sandbox, jadi tampilan 3D sungguhan — perspektif,
bayangan, ketajaman teks, kursor — **belum pernah saya lihat**. Uji asap membuktikan skrip,
geometri, dan sambungan, bukan rupa.

## Potong-buka — kemasan dibuka bagian demi bagian (`cutaway/`)

Halaman ini menerapkan metode skill **Cutaway** dari repositori
[`Nyxera0x/cutaway`](https://github.com/Nyxera0x/cutaway) (61 ★, MIT, 6 Nov 2026; isi post
`x.com/Nyxera0x/status/2118689860437315679` — halaman X-nya sendiri tidak bisa dibuka dari
sandbox, repo sumbernya yang terbaca). Metodenya: **satu gambar acuan diukur, ceklis bernomor
ditulis sebelum satu baris kode, objek dibangun ulang dari kode, setiap bagian punya kamera
sendiri, `render(t)` murni.**

Bedanya dari sumber: objeknya bukan mahluk robotik berwarna hijau, tapi **kemasan Nocturne
200 g** — 7 bagian, palet kertas Nocturne, dan angka isi dari `data/catalog.json`. Tidak ada
three.js/WebGL: sembilan transform CSS per bidang, satu fungsi `render(t)`.

```bash
python3 tools/cutaway.py          # ukur acuan → cutaway/data.js + laporan/cutaway-checklist.md
python3 tools/cutaway.py --cek    # angka data.js vs piksel acuan (rasio, tinta per pita)
python3 tools/cutaway-still.py    # lembar still skema → cutaway/still/lembar-still.png
node tools/cutaway-uji.mjs        # 38 butir tanpa peramban: murni, loop, 9 kamera, sambungan
python3 tools/cutaway-luring.py   # satu berkas HTML tanpa tautan luar
```

| Berkas | Isi |
| --- | --- |
| `cutaway/index.html` + `cutaway.css` | halaman: panggung 3D, daftar 7 bagian, kartu spesifikasi, rel waktu |
| `cutaway/cutaway.js` | `render(t)` murni: kamera per ketukan, bukaan bagian, goyang halus dari `t` |
| `cutaway/data.js` | dibangun `tools/cutaway.py` — `UKUR`, `BAGIAN`, `KAMERA`, `KETUKAN`, `CEKLIS`. Jangan disunting tangan |
| `laporan/cutaway-checklist.md` | ceklis 12 baris bernomor, setiap kata kabur diberi angka |
| `cutaway/still/lembar-still.png` | 3 frame skema (sampul, badan terbuka, isi sangrai) |

Angka yang dipegang: ketukan 2–3 s, bagian terbuka 1,0 s lalu menutup 0,55 s, objek 60–70%
tinggi panggung, satu aksen kobalt untuk bagian yang bergerak, porsi gelap ≥ 0,8 × acuan
(14,3% → 11,4%), dan **tidak ada dua ketukan memakai kamera yang sama**.

**Batas yang jujur.** Yang bisa dibuktikan: ukuran acuan, ceklis, geometri, kontrak `render(t)`,
sambungan tombol/rel — semuanya lewat uji tanpa peramban. Yang **tidak**: rupa halaman
(tidak ada Chromium) dan **film 60 fps + skor prosedural** (butuh Playwright + ffmpeg, tidak ada
di sini). Lembar still adalah **skema geometri** dari `cutaway-still.py`, bukan tangkapan layar.

## Impor skill dari luar (post X, artikel, repo)

Skill yang datang dari tautan luar (mis. post X) **tidak bisa saya buka sendiri** — X menolak
permintaan tanpa sesi login, dan sandbox ini hanya punya akses ke github/npm/pypi. Jadi isinya
harus datang dari Anda: teks tempelan atau tangkapan layar. Untuk itu ada satu jalur:

```bash
# setelah teks post-nya ditempel ke /tmp/post.txt
python3 tools/skill_impor.py --nama rak-gerak --dari /tmp/post.txt \
    --sumber "https://x.com/…/status/…" \
    --baris-tabel "| [\`rak-gerak\`](rak-gerak/SKILL.md) | D4 | kapan dipakai | keluaran |"

python3 tools/skill_impor.py --cek     # 12 skill · frontmatter · nama = folder · terdaftar di README
```

Yang dilakukan: menulis `skills/<slug>/SKILL.md` dengan frontmatter (`name`, `description`
ringkas dari paragraf pertama), menyisipkan baris tabel **setelah baris skill terakhir** di
`skills/README.md`, lalu memeriksa ulang. Yang **tidak** dilakukan: mengarang isi — kalau teks
sumbernya kosong, alat berhenti dan bilang begitu.

## Penelusuran skill GitHub (5 Nov 2026)

Ambang 3.000 bintang; hasil lengkap, termasuk yang ditolak dan alasannya, ada di
[`laporan/skill-github.md`](laporan/skill-github.md). Tiga skill baru:
[`landing-page-ai`](skills/landing-page-ai/SKILL.md),
[`gaya-gambar`](skills/gaya-gambar/SKILL.md) (20 gaya di `data/gaya-gambar.json`),
[`pasangan-font`](skills/pasangan-font/SKILL.md).

## Yang sudah jalan

- Hero headline 2 baris + **deretan kartu nama produk bergulir** (hanya nama, tanpa harga/foto)
- Klik nama di hero → meluncur ke kartu produk, tersorot 2 detik, URL berubah ke `#produk`
- Tombol jeda guliran, berhenti saat kursor menyentuh, hormati `prefers-reduced-motion`
- Katalog 9 SKU + 2 paket: foto 4:5, badge stok, nomor editorial, tasting notes,
  lima bulatan roast, **plakat petani** (nama, desa, elevasi, varietas), harga 4 ukuran
- Filter Jenis / Daerah / Ketersediaan yang menyaring grid **dan** rail editorial
- Pemilih ukuran & gilingan → harga dan pesan WhatsApp ikut berubah
- Status stok 4 tingkat: Tersedia · Terbatas · Habis · Menunggu panen
  (Habis/Menunggu panen → tombol berubah jadi "Kabari saya saat ada")
- Seksi Langganan (3 paket), Manifesto, Member (Nocturne Circle), penutup WA, footer poster
- Format pesan WhatsApp baku sesuai brief 6.2 (siap dibaca sistem di fase integrasi)
- JSON-LD `Brand`, meta OG, `noscript` dengan tautan WA
- Mobile: panel menu penuh, FAB WhatsApp, tanpa horizontal scroll
- **Motion layer**: intro berurutan, topeng headline, bar kemajuan gulir, reveal saat scroll,
  parallax hero/kartu/poster, tombol magnetik, tilt kartu, glow kursor, dan micro-feedback —
  semuanya mati otomatis pada `prefers-reduced-motion`

## Papan harian (menjalankan bisnis)

`tools/papan.py` membaca 10 berkas data lalu menulis `dashboard/index.html` + `dashboard/data.json`.
Sejak revisi 7 divisi, papan juga menampilkan **tabel target vs aktual per divisi** — target dibaca dari
`data/divisi.json`, aktual dihitung dari berkas data (tidak diketik).
Tanpa dependensi, tanpa server tambahan.

| Berkas | Isi | Siapa yang mengisi |
| --- | --- | --- |
| `data/catalog.json` | produk, harga, status stok yang tampil di situs | D1 |
| `data/biaya.json` | harga green bean, kemasan, upah, biaya tetap (**masih asumsi**) | D5 |
| `data/stok-lot.json` | lot green bean: masuk, terpakai, sisa | D1 |
| `data/batch-qc.csv` | catatan sangrai + skor cupping + lolos/tolak | D1 |
| `data/pesanan.csv` | satu baris per order | D2 |
| `data/konten-14hari.csv` | jadwal konten + status | D3 |
| `data/kpi.csv` | KPI mingguan (order, omzet, chat, followers) | D6 |
| `data/legal.json` | status dokumen usaha | D7 |
| `data/divisi.json` | **target & KPI 7 divisi, 3 bulan** — satu-satunya tempat angka target | owner |
| `data/kreatif.json` | manifest aset konten (video/carousel/story, status tayang) | D4 |
| `data/riset-referensi.csv` | tangkapan post sejenis (hook, format, metrik) — `status` contoh/asli | D3 |
| `data/riset-komentar.csv` | kutipan komentar pembeli → keberatan & FAQ | D3 |
| `data/riset-kata-kunci.csv` | kata kunci Google/marketplace/TikTok + halaman target | D3 |

Semua 9 SKU + 2 paket diset **tersedia** atas arahan pemilik (30 Okt 2026) sebagai asumsi kerja;
lot restock ditambahkan di `data/stok-lot.json`. Ganti angka lot saat penerimaan barang nyata —
papan akan menandai selisih status tanpa perlu mengubah kode.

Yang dihitung otomatis: margin tiap ukuran, HPP, break-even, sisa bungkus per SKU
(dari green bean × yield; blend dari komponennya), order terlambat, resi kosong,
restock jatuh tempo (H+18), konten terlambat, batch ditolak, dan selisih status stok
situs vs lot.

```bash
python3 tools/papan.py                       # hari ini (WIB)
python3 tools/papan.py --tanggal 2026-11-03  # tanggal lain
python3 tools/papan.py --json                # ringkasan untuk dibaca mesin
```

**Tujuh divisi** (alur kerja + target per divisi di `operasional/divisi/`): Produksi & QC ·
Penjualan & CRM · Marketing & Pertumbuhan · Kreatif & Media · Operasional & Logistik ·
Keuangan · Brand & Legal. Ritme: 25 menit/hari + ±15 jam/minggu untuk satu orang —
urutannya di `operasional/00-struktur-divisi.md`, mulai eksekusi dari
`operasional/07-runbook-minggu-1.md`. Angka target hanya di `data/divisi.json`.

## Yang WAJIB dikonfirmasi sebelum tayang

Daftar lengkap + alasannya ada di panduan bagian 8. Ringkasnya:

| # | Hal | Kenapa penting |
| --- | --- | --- |
| 1 | Tingkat sangrai per produk (dari file desain label) | Sekarang masih usulan; badge menampilkan tanda "konfirmasi" |
| 2 | Tasting notes 3 kata per produk | Hanya Raung yang berasal dari label |
| 3 | Izin publikasi 7 nama petani | Nama sudah tayang dengan data brief |
| 4 | Blue Mount Ijen: Andi Wijaya atau Ijen Coffee Collective | Dua-duanya ada di brief, harus dipilih satu |
| 5 | Status stok nyata per SKU + tanggal | Sekarang hanya Blue Mount Ijen yang "Terbatas" |
| 6 | Konflik angka elevasi (Semeru, Raung, Ijen) & varietas Gayo/Semeru | Katalog vs label kemasan berbeda |
| 7 | Nomor WhatsApp Business aktif | Sekarang `628988188800` dari brief |
| 8 | Jam operasional & target balas 2 jam | Janji layanan |
| 9 | Angka program Member | Belum ditampilkan karena belum diputuskan |
| 10 | Tautan marketplace resmi | Belum ada, jadi tidak ditautkan |

Selama butir 1–6 belum beres, footer menampilkan "Situs versi uji coba — sebagian data
menunggu konfirmasi pemilik." Jangan dihapus sebelum beres.

## Aturan yang tidak boleh dilanggar

1. Nocturne **bukan** roastery. Tulis "brand kopi"; sangrai oleh **Ais Coffee Roastery**.
2. Tidak ada klaim "terbaik", "satu-satunya", "fresh daily", atau klaim kesehatan.
3. Harga & produk hanya diubah di `data/catalog.json`, tidak di `index.html`.
4. Harga situs = harga marketplace (10.9). Jangan perang harga dengan diri sendiri.
5. Petani: nama boleh (dengan izin), foto & titik lokasi tidak.

## Dokumen marketing

| File | Isi |
| --- | --- |
| `panduan/PANDUAN-LANDING-PAGE.md` | **Panduan pembuatan landing page** — 13 bagian, 25 butir QA |
| `brand/README.md` | brand kit: logo, label 70×100 mm, aturan cetak & pemakaian logo |
| `komersial/01-panduan-grosir.md` | 4 tingkat harga grosir, aturan margin, alur jual B2B |
| `marketing/08-konten-siap-pakai.md` | 7 post + 3 skrip TikTok + 9 judul marketplace siap salin |
| `skills/README.md` | **4 skill** (social-media-riset, komentar-mining, search-intent-riset, studio-konten) + aturan etika & bukti |
| `skills/social-media-riset/SKILL.md` | outlier post, baseline median, taksonomi hook, swipe file, brief |
| `skills/komentar-mining/SKILL.md` | bahasa pembeli → keberatan/FAQ/copy, aturan kutipan ≤ 24 kata |
| `skills/search-intent-riset/SKILL.md` | Google/marketplace/TikTok/mesin jawaban AI, prioritas & celah halaman |
| `skills/studio-konten/SKILL.md` | 10 tahap / 50 slot: peta otomatis vs manual, hook → skrip 9 detik → brief Senin, aturan cek suara |
| `skills/motion-web/SKILL.md` | 7 repo desain → kontrak token, komponen vanilla, audit anti-slop, adegan 9:16, batas (tanpa Figma/Blender/encoder) |
| `marketing/09-media-kreator.md` | **playbook konten media kreator**: pipeline aset, bank 30 hook (versi mesin), jadwal, 3 angka ukur, aturan caption, studio 10 tahap |
| `operasional/00-struktur-divisi.md` | 7 divisi, RACI, ritme harian/mingguan, cara membaca tabel target |
| `operasional/divisi/README.md` | indeks 7 divisi + cara mengubah target di `data/divisi.json` |
| `operasional/divisi/D1-produksi-qc.md` | alur 10 langkah satu batch, gerbang QC, target & DoD |
| `operasional/divisi/D2-penjualan-crm.md` | chat→order→pelanggan, naskah wajib, alur B2B, target |
| `operasional/divisi/D3-marketing-pertumbuhan.md` | konten→chat, 7 kanal, ritme 90 menit, target |
| `operasional/divisi/D4-kreatif-media.md` | klip mentah vs aset render, spesifikasi teknis, target |
| `operasional/divisi/D5-operasional-logistik.md` | packing, cut-off 15.00, ongkir, opname, target |
| `operasional/divisi/D6-keuangan.md` | HPP, margin, break-even, tutup buku, target |
| `operasional/divisi/D7-brand-legal.md` | gerbang klaim 4 pertanyaan, izin, dokumen, target |
| `operasional/07-runbook-minggu-1.md` | rencana 10 hari pertama per divisi |
| `panduan/07-sistem-motion.md` | **Sistem gerak** — 5 skill motion teratas + 13 gerak yang dipasang, token, larangan, 10 butir uji |
| `marketing/00-strategi-90hari.md` | Strategi 90 hari (positioning, segmen, ritme 7 jam/minggu, KPI) |
| `marketing/01-kalender-konten-30hari.md` | 30 hari konten + aset yang direkam saat produksi |
| `marketing/02-copy-library.md` | Bio, caption, 6 template WhatsApp, 4 skrip B2B |
| `marketing/03-marketplace-dan-ads.md` | Judul & deskripsi listing, bundling, aturan iklan |
| `marketing/04-whatsapp-crm-dan-b2b.md` | Alur follow up H+0…H+60, langganan, pipeline kafe |
| `marketing/05-kpi-tracker.csv` | Tracker mingguan |
| `marketing/06-checklist-launch-14hari.md` | Checklist 14 hari |

> **Catatan:** file `marketing/` ditulis sebelum brief ini diterima. Dua hal perlu
> diselaraskan: (a) kata "roastery" untuk Nocturne harus diganti "brand kopi", dan
> (b) produk/harga di materi itu masih versi lama (6 SKU), sedangkan situs kini memakai
> 9 SKU dari brief bagian 10. Panduan landing page sudah memakai data brief.
