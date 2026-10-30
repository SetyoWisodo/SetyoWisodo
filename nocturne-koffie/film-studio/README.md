# film-studio — empat mesin motion, dipasang dan diuji

Folder ini berisi pemasangan **GSAP, Lottie, Remotion, dan HyperFrames** yang sebenarnya:
`package.json` dengan versi dipin, `package-lock.json`, dan skrip yang sudah dijalankan.
Bukan daftar tautan, bukan rencana.

```bash
cd film-studio
npm install                # 389 paket, ~700 MB (node_modules tidak masuk git)
npm run vendor             # salin GSAP/Lottie/font ke assets/ + tulis manifest versi
npm run lottie             # assets/lottie/nocturne-9s.json dari lembar film
npm run verifikasi         # GSAP + Lottie + berkas nyata (4 cek)
npm run hf:lint            # hyperframes lint → 0 error, 0 warning
npm run remotion:bundle    # bundel Remotion (tidak butuh Chrome)
```

## Apa yang benar-benar jalan di sini

| Mesin | Dipasang | Diuji di sandbox ini | Hasil |
| --- | --- | --- | --- |
| **GSAP** 3.15.0 | `node_modules/gsap` + `assets/vendor/gsap.min.js` (73 KB) | ya — timeline 4 cue di jsdom, `seek()` per cue, transform berubah | **lolos** |
| **ScrollTrigger** 3.15.0 | `assets/vendor/ScrollTrigger.min.js` (45 KB) | ya — dipakai memicu timeline di `/motion/` | **lolos** |
| **Lottie** lottie-web 5.13.0 | `node_modules/lottie-web` + `assets/vendor/lottie.min.js` (306 KB) | ya — JSON 9 detik dimuat, di-seek 4 cue, lapisan berganti | **lolos** |
| **HyperFrames** 0.8.221 | CLI + komposisi `hyperframes/` | `hyperframes lint` → **0 error, 0 warning** atas 5 berkas; `browser ensure` **gagal** (Chrome tidak bisa diunduh) | **lint lolos, render tidak** |
| **Remotion** 4.0.539 | `@remotion/cli` + komposisi React | `remotion bundle` **lolos**; `remotion render` **gagal** di `libnspr4.so` | **bundel lolos, render tidak** |

Ringkas dan jujur: **dua mesin berjalan penuh (GSAP, Lottie), dua mesin berhenti tepat di titik
yang butuh Chrome (HyperFrames, Remotion).**

## Kenapa render Remotion/HyperFrames gagal di sini

```
/tmp/chromium: error while loading shared libraries: libnspr4.so: cannot open shared object file
```

Chrome yang dipakai kedua perender butuh `libnss3`/`libnspr4`. Sandbox ini tidak punya paket itu,
dan repositori OS di luar jaringan yang diizinkan. Yang sudah dicoba, semuanya gagal:

| Cara | Hasil |
| --- | --- |
| `hyperframes browser ensure` | unduhan Chrome diblokir (`TLS socket disconnected`) |
| `@sparticuz/chromium` (Chromium 153 terpaket) | binernya terbongkar (209 MB) tetapi `libnspr4.so` tetap hilang |
| Remotion `--browser-executable` ke biner itu | gagal di pustaka yang sama |
| `npm` cari paket pembawa libnss | tidak ada paket yang membawa `libnss3` |

Karena itu **video jadi dibuat lewat jalur ketiga** yang tidak butuh Chrome:

```
motion/film-sheet.json → 540 frame PNG (Pillow) → ffmpeg (H.264, bt709)
```

Hasilnya `motion/out/klip-01-nocturne-9s.mp4` — 1080×1920, 60 fps, 9,00 detik, 341 KB.
Dibuat `tools/render_film.py`. Ini **bukan** Remotion dan **bukan** HyperFrames, dan tidak
saya klaim sebagai keduanya.

## Isi folder

| Path | Isi |
| --- | --- |
| `package.json` | versi dipin: gsap 3.15.0, lottie-web 5.13.0, remotion 4.0.539, hyperframes 0.8.221 |
| `scripts/vendor.mjs` | salin GSAP/Lottie/font ke `assets/`, tulis `assets/vendor/mesin.json` |
| `scripts/verifikasi.mjs` | uji GSAP + Lottie di jsdom + berkas nyata (bukan bukti visual — dicetak jelas) |
| `scripts/buat-hyperframes.mjs` | hasilkan `hyperframes/index.html` + 4 sub-komposisi dari lembar film |
| `lottie/buat-lottie.mjs` | hasilkan `assets/lottie/nocturne-9s.json` (9 lapisan, 4 penanda cue) |
| `remotion/Klip.jsx` | komposisi Remotion: 4 `Sequence`, spring damping tinggi, bilah kemajuan |
| `remotion/index.jsx` | `registerRoot` untuk `@remotion/cli` |
| `hyperframes/` | root + `compositions/cue-1..4.html` + `vendor/` (GSAP & font lokal) |
| `data/film-sheet.json` | salinan lembar film — satu sumber angka untuk semua mesin |
| `public/fonts/` | TTF brand untuk `staticFile()` di Remotion |

## Kalau nanti ada mesin dengan Chrome

```bash
cd film-studio
npm run remotion:render     # → out/remotion.mp4   (1080×1920, 60 fps, 540 frame)
npm run hf:render           # → komposisi HyperFrames jadi MP4
```

Keduanya **sudah dikonfigurasi** dan komposisinya sudah lolos lint/bundel. Yang kurang hanya
Chrome. Tidak ada perubahan kode yang perlu dilakukan saat pindah mesin.

## Aturan yang dipegang

1. **Tanpa CDN.** GSAP dan Lottie disalin ke `assets/vendor/`; komposisi HyperFrames memakai
   `vendor/gsap.min.js`. Halaman publik tidak memuat satu pun pustaka ini.
2. **Halaman awal tidak tersentuh.** Pustaka dimuat malas (`assets/js/mesin.js`) saat bagiannya
   masuk layar. Halaman awal tetap 89 KB.
3. **Versi dipin, bukan `^`.** `periksa.py` menolak rentang versi.
4. **Angka dari lembar film.** Keempat mesin membaca `film-sheet.json`; tidak ada durasi atau teks
   yang ditulis ulang di JSX/HTML.
5. **Tidak ada klaim render.** Selama `motion/out/*.mp4` yang ada hanya keluaran `render_film.py`,
   dokumentasi menyebutnya begitu.

## Lisensi

| Paket | Lisensi | Catatan |
| --- | --- | --- |
| GSAP | Standard "no charge" (gsap.com/standard-license) | gratis termasuk komersial; tidak boleh dijual ulang sebagai produk |
| ScrollTrigger | idem (kini satu paket dengan GSAP) | — |
| lottie-web | MIT | aman |
| HyperFrames | Apache-2.0 | aman |
| Remotion | Remotion License | **gratis untuk individu & perusahaan ≤ 3 orang**; di atas itu perlu lisensi berbayar |
| Font Bricolage / Fraunces / Inter | OFL-1.1 | lihat `assets/fonts/LISENSI.md` |

Catatan Remotion itu penting: kalau nanti Nocturne memakai Remotion untuk produksi komersial
dengan tim lebih dari 3 orang, lisensinya harus dibeli. Sekarang belum dipakai untuk render apa pun.
