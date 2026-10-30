---
name: motion-web
description: >
  Skill gerak & landing page untuk D4 (Kreatif & Media). Gunakan saat membuat atau mengubah
  animasi halaman, merancang landing page kampanye, atau memeriksa apakah sebuah halaman terlihat
  "buatan mesin". Menyatukan tujuh repo desain (UI UX Pro Max, Impeccable, Framelink Figma MCP,
  React Bits, GSAP Skills, HyperFrames, MCP for Blender) menjadi komponen vanilla, kontrak token,
  audit anti-slop, dan adegan 9:16 berbasis HTML. Tanpa React, tanpa CDN library, tanpa render server.
version: 1.0.0
author: Nocturne Koffie (D4 Kreatif & Media × D3)
license: internal
metadata:
  dipakai_divisi: [D4, D3]
  butuh_berkas:
    - data/design-system.json
    - assets/css/site.css
    - assets/css/motion.css
    - assets/css/motion-ui.css
    - assets/js/motion.js
    - assets/js/motion-ui.js
    - studio/skrip/*.md
    - data/kreatif.json
  keluaran:
    - motion/index.html
    - motion/frame-01..05.html
    - motion/timeline.json
    - laporan/slop.md
  perintah: python3 tools/motion.py && python3 tools/slop.py
  izin_akses: baca berkas lokal + tulis folder motion/ dan laporan/
---

# Gerak & Landing Page — 7 Repo, 1 Sistem

## Ikhtisar

Post `@thegreatest_sv` (29 Okt 2026) menyebut tujuh repo desain. Kalau ketujuhnya dipasang
apa adanya, hasilnya situs React dengan tiga library animasi, satu server MCP, dan satu render
video — berat, dan sebagian tidak bisa jalan di lingkungan ini. Skill ini mengambil **yang bisa
diverifikasi** dan meninggalkan sisanya dengan alasan tertulis.

| # | Repo | Yang dipakai | Yang tidak | Bukti |
| ---: | --- | --- | --- | --- |
| 1 | `nextlevelbuilder/ui-ux-pro-max-skill` | disiplin token: warna/radius/ukuran/font terkunci di kontrak | katalog palet & font siap pakai (brand dikunci FINAL 3.7) | `data/design-system.json` |
| 2 | `pbakaus/impeccable` | 62 antipattern → **29 aturan** yang bisa diukur mesin | plugin Claude/Cursor, browser-bundle | `tools/slop.py`, `laporan/slop.md` |
| 3 | `GLips/Figma-Context-MCP` | prinsip "layout punya sumber mesin", keluaran ringkas | server MCP & token Figma (tidak ada akun) | kontrak JSON + `laporan/slop.json` |
| 4 | `DavidHDev/react-bits` | 4 komponen ditulis ulang vanilla + pola pin | React/Next, registry, komponen WebGL | `assets/js/motion-ui.js` |
| 5 | `greensock/gsap-skills` | semantik pin/scrub + aturan performa jadi gerbang audit | GSAP sendiri (≈70 KB + CDN) | `assets/js/motion.js`, aturan `animasi-layout` |
| 6 | `heygen-com/hyperframes` | HTML → adegan 9:16 dengan timeline eksplisit | runtime & render server | `motion/frame-*.html`, `motion/timeline.json` |
| 7 | `ahujasid/mcp-for-blender` | tidak dipakai; diganti bidang CSS 3D ≤ 3,5° | Blender, MCP, Meshy/Tripo | `assets/js/motion.js` §4c |

## Kapan dipakai

- menambah animasi atau interaksi di situs / landing page;
- membuat landing page kampanye baru (`tools/kampanye.py`) dan ingin geraknya konsisten;
- memeriksa halaman sebelum tayang: "apakah ini terlihat seperti template AI?";
- membuat adegan 9:16 untuk konten D4 dari skrip studio.

Jangan pakai untuk: membuat video jadi (tidak ada encoder di sini), mengimpor desain Figma,
atau membuat model 3D.

## Empat lapisan sistem

| Lapisan | Berkas | Peran |
| --- | --- | --- |
| 1 · Kontrak | `data/design-system.json` | satu-satunya sumber token: warna, tipografi, radius, spasi, easing, aturan gerak, pengecualian brand |
| 2 · Gerak halaman | `assets/css/motion.css` + `assets/js/motion.js` | reveal, parallax, topeng media, tilt — dipakai situs utama |
| 3 · Komponen | `assets/css/motion-ui.css` + `assets/js/motion-ui.js` | komponen lepas: spotlight, count-up, magnet, teks per kata, pin, bilah kemajuan |
| 4 · Adegan | `motion/frame-*.html` + `motion/timeline.json` | adegan 9:16 dari skrip studio, siap direkam |

Audit (`tools/slop.py`) memeriksa lapisan 1–3, lalu memeriksa halaman publik.

## Cara memakai komponen

```html
<!-- teks masuk per kata -->
<h1 data-ui="words">Kopi yang jujur soal tanggal.</h1>

<!-- angka berjalan: 7–21 hari -->
<b data-ui="count" data-from="7" data-to="21" data-prefix="7–" data-suffix=" hari">7–21 hari</b>

<!-- kartu dengan sorotan kursor -->
<a class="pilih" data-ui="spotlight" href="…">…</a>

<!-- tombol magnet (maks 6 px) -->
<a class="btn btn--orange" data-ui="magnet" href="…">Pesan via WhatsApp</a>

<!-- pin bertahap: anak .ui-pin__step menyala mengikuti gulir -->
<div class="bukti" data-ui="pin">
  <article class="ui-pin__step">…</article>
</div>
```

Aturan pemakaian:

1. **Satu ide gerak per bagian.** Dua efek di satu blok membuat mata tidak tahu harus ke mana.
2. **Jangan pakai `words` pada elemen bermarkup** (`<em>`, `<strong>`). Skrip mendeteksinya dan
   hanya memberi fade utuh, supaya tipografi brief tidak hilang.
3. **Tanpa JS halaman tetap terbaca.** Keadaan awal disembunyikan hanya jika `html.ui-motion`
   sudah dipasang skrip.
4. **`prefers-reduced-motion` mematikan semuanya**, bukan memperlambat.
5. **Efek pointer mati di perangkat sentuh.**

## Aturan yang tidak boleh dilanggar (gerbang audit)

| Aturan | Kenapa | Konsekuensi bila dilanggar |
| --- | --- | --- |
| hanya `transform` & `opacity` | properti layout memicu reflow | audit gagal (`animasi-layout`) |
| listener gulir `{passive:true}` | gulir tersendat di HP | audit gagal (`listener-pasif`) |
| setiap file beranimasi punya blok `prefers-reduced-motion` | aksesibilitas | audit gagal (`reduced-motion`) |
| `will-change` hanya untuk lapisan yang bergerak terus | memori GPU | audit perhatian (`will-change`) |
| tanpa easing overshoot | pantulan = penanda slop | audit perhatian (`bounce-easing`) |
| tanpa denyut/kedip tak berujung | mengalihkan perhatian dari produk | audit perhatian |
| oranye hanya untuk teks ≥ 24 px | kontras 3,33:1 di atas kertas | audit gagal (`kontras-rendah`) |

## Alur kerja landing page

1. **Kontrak dulu.** Buka `data/design-system.json`. Kalau butuh warna/ukuran baru, tambahkan di
   sana — kalau tidak, audit akan menandainya.
2. **Susun halaman.** Kalau halaman dibuat generator, ubah generatornya (`tools/kampanye.py`),
   bukan HTML hasilnya.
3. **Pasang gerak minimal:** bilah kemajuan, reveal per bagian, satu `words` di hero,
   `magnet` di CTA utama, `spotlight` di kartu pilihan. Tidak lebih.
4. **Jalankan audit:** `python3 tools/slop.py` → `laporan/slop.md`. Kritis harus nol.
5. **Periksa gerbang:** `python3 tools/periksa.py` (cek kontrak desain, anti-slop, komponen, adegan).

## Alur kerja adegan 9:16

1. `python3 tools/studio.py` → 5 skrip 9 detik di `studio/skrip/`.
2. `python3 tools/motion.py` → `motion/frame-01..05.html` + `motion/timeline.json`.
3. Buka adegan di browser; putar, jeda, atau seek (`frame-01.html?t=3.2`).
4. Rekam: **rekam layar** jendela 1080×1920, atau render `ffmpeg` di mesin yang punya ffmpeg
   (tidak ada di sandbox ini). Timecode tiap beat ada di `timeline.json`.
5. Unggah lewat kanal seperti biasa — sistem ini tidak memposting apa pun.

## Batas yang harus diingat

- **Tidak ada Figma.** Figma-Context-MCP hanya dipakai prinsipnya; token di repo ini adalah sumbernya.
- **Tidak ada Blender.** Tidak ada aset 3D, tidak ada GLB; 3D sebatas CSS `rotateX/rotateY` kecil.
- **Tidak ada encoder video.** Adegan HTML deterministik; video jadi dibuat di luar sandbox.
- **GSAP tidak dipasang.** Semantiknya ditiru; kalau nanti butuh pin/scrub rumit, `motion.js`
  bisa ditukar tanpa mengubah kelas CSS.
- **Audit memeriksa berkas, bukan rasa.** Semua hijau berarti "tidak ada pola slop yang bisa diukur",
  bukan "desainnya sudah bagus".
