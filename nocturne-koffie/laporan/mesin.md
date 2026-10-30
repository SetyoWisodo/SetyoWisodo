# Mesin film Nocturne — status pemasangan

Diperbarui 30 Oktober 2026 · sumber: `film-studio/package.json`, `assets/vendor/mesin.json`,
`motion/out/manifest.json`, `laporan/periksa.json`.

Permintaannya jelas: **HyperFrames, Remotion, GSAP, Lottie dipaksa pasang dengan berbagai cara.**
Keempatnya sekarang terpasang di repo ini — bukan dirujuk, bukan dikutip dari README orang.
Dokumen ini mencatat apa yang berhasil, apa yang mentok, dan bukti untuk masing-masing.

## 1 · Tabel mesin

| Mesin | Versi | Cara masuk | Terpasang | Terbukti jalan di sandbox | Yang tidak bisa |
| --- | --- | --- | --- | --- | --- |
| **GSAP** | 3.15.0 | `npm i gsap` → disalin ke `assets/vendor/gsap.min.js` (73 KB) | ya | timeline 4 cue, `seek()` per cue, durasi total 9,00 s, nilai `transform` benar-benar berubah (uji jsdom, `scripts/verifikasi.mjs`) | gerak di layar sungguhan tanpa browser |
| **ScrollTrigger** | 3.15.0 | satu paket dengan GSAP | ya | memicu timeline saat bagian masuk viewport di `/motion/`; jatuh ke `play()` biasa kalau tidak ada ScrollTrigger | — |
| **Lottie** | lottie-web 5.13.0 | `npm i lottie-web` → `assets/vendor/lottie.min.js` (306 KB) | ya | `assets/lottie/nocturne-9s.json` (6,8 KB, 9 lapisan, 540 frame, 4 penanda) dimuat renderer SVG, di-seek 4 cue, lapisan berpindah sesuai cue | rasterisasi piksel & metrik font (jsdom tidak punya) |
| **Remotion** | 4.0.539 | `npm i remotion @remotion/cli` (254 paket) | ya | **`remotion bundle` lolos** → `out/bundle`; komposisi `remotion/Klip.jsx` membaca `data/film-sheet.json` | `remotion render` → `libnspr4.so` tidak ada |
| **HyperFrames** | 0.8.221 | `npm i hyperframes` (70 paket) | ya | `hyperframes lint hyperframes` → **0 error, 0 warning** atas 5 berkas (root + 4 sub-komposisi) | `hyperframes browser ensure` (unduhan Chrome diblokir TLS) dan `render` |

Ringkas: **dua mesin berjalan penuh, dua mesin berhenti tepat di pintu Chrome.**

## 2 · Bukti yang bisa dibuka sendiri

| Bukti | Path | Angka |
| --- | --- | --- |
| GSAP lokal | `assets/vendor/gsap.min.js` | 72.927 B |
| ScrollTrigger lokal | `assets/vendor/ScrollTrigger.min.js` | 44.575 B |
| Lottie lokal | `assets/vendor/lottie.min.js` | 305.704 B |
| Manifest versi | `assets/vendor/mesin.json` | 7 paket, 3 berkas vendor, 4 font |
| Animasi Lottie | `assets/lottie/nocturne-9s.json` | 6,8 KB · 9 lapisan · 540 frame @ 60 fps · 4 penanda |
| Komposisi HyperFrames | `film-studio/hyperframes/index.html` + `compositions/cue-1..4.html` | 5 berkas, lint 0/0 |
| Komposisi Remotion | `film-studio/remotion/Klip.jsx` + bundel `out/bundle` | 4 `Sequence`, spring `damping 200` |
| Uji mesin | `npm run verifikasi` (di `film-studio/`) | **4 lolos · 0 gagal** |
| **Klip jadi** | `motion/out/klip-01-nocturne-9s.mp4` | 1080×1920 · 60 fps · 9,00 s · 341 KB · H.264 bt709 |
| Manifest klip | `motion/out/manifest.json` | sha256, encoder ffmpeg 7.0.2, sumber angka |

## 3 · Satu hal yang harus jujur disebut

`.mp4` di repo ini **tidak dirender oleh Remotion maupun HyperFrames.** Keduanya butuh Chrome,
dan Chrome di sandbox ini gagal start:

```
/tmp/chromium: error while loading shared libraries: libnspr4.so: cannot open shared object file
```

Yang sudah dicoba dan hasilnya:

| Cara | Hasil |
| --- | --- |
| `npx hyperframes browser ensure` | unduhan Chrome diblokir (`TLS socket disconnected`) |
| `npm i @sparticuz/chromium` | terunduh (67 MB), biner terbongkar (209 MB), **tetap** `libnspr4.so` hilang |
| Remotion `--browser-executable=/tmp/chromium` | gagal di pustaka yang sama (dibuktikan, bukan diduga) |
| cari paket pypi/npm pembawa `libnss3` | tidak ada (`libnss3`, `nss-binaries`, `nsslib` → 404) |

Jadi klipnya dibuat lewat jalur yang bisa dibuktikan di sini:

```
motion/film-sheet.json → 540 frame PNG (Pillow, font brand asli) → ffmpeg 7.0.2 → H.264
```

Perintahnya: `python3 tools/render_film.py`. Warna dari `data/design-system.json`, teks & waktu dari
`motion/film-sheet.json`, font Bricolage Grotesque 800 / Fraunces 300 / Inter 400 — font aslinya,
bukan pengganti.

Kalau nanti ada mesin ber-Chrome: `cd film-studio && npm run remotion:render` dan
`npm run hf:render` sudah siap, tidak perlu ubah kode.

## 4 · Yang masuk ke halaman publik

| Tempat | Mesin | Cara muat |
| --- | --- | --- |
| `/motion/` §6 "Mesin yang sekarang terpasang" | GSAP + ScrollTrigger | `assets/js/mesin.js` → `IntersectionObserver` → unduh GSAP saat bagian masuk layar |
| `/motion/` §6 "Lottie — pemutar 9 detik" | lottie-web | dimuat malas, penggaris waktu + penanda cue terbaca |
| `/motion/` §6 "Klip jadi" | — | `<video>` 341 KB, `preload="metadata"` |
| Halaman lain | tidak ada | halaman awal tetap **89 KB**, tanpa satu pun pustaka mesin |

Aturan yang dipegang: **tidak ada CDN**, versi **dipin tanpa `^`**, dan `prefers-reduced-motion`
membuat GSAP melompat ke keadaan akhir serta Lottie diparkir di frame cue terakhir.

## 5 · Lisensi (penting untuk produksi komersial)

| Paket | Lisensi | Konsekuensi |
| --- | --- | --- |
| GSAP + ScrollTrigger | Standard "no charge" | gratis, termasuk komersial; tidak boleh dijual ulang sebagai produk |
| lottie-web | MIT | aman |
| HyperFrames | Apache-2.0 | aman |
| **Remotion** | Remotion License | gratis untuk individu dan perusahaan **≤ 3 orang**; lebih dari itu **perlu lisensi berbayar** |
| Font | OFL-1.1 | aman, lihat `assets/fonts/LISENSI.md` |

Selama Remotion belum dipakai untuk merender apa pun, belum ada kewajiban lisensi. Begitu dipakai
produksi dan tim lebih dari 3 orang, lisensinya harus dibeli sebelum dipakai komersial.

## 6 · Perintah

```bash
cd film-studio
npm install                     # wajib tiap sesi: node_modules tidak masuk git
npm run vendor                  # salin GSAP/ScrollTrigger/Lottie/font + tulis manifest
npm run lottie                  # assets/lottie/nocturne-9s.json
npm run verifikasi              # uji GSAP + Lottie + berkas nyata (4 cek)
node scripts/buat-hyperframes.mjs
npx hyperframes lint hyperframes   # 0 error, 0 warning
npm run remotion:bundle            # bundel lolos tanpa Chrome
npm run remotion:render            # butuh Chrome → gagal di sandbox ini
```

```bash
# dari akar proyek
python3 tools/render_film.py             # 540 frame + MP4 (butuh Pillow & ffmpeg)
python3 tools/render_film.py --still 90  # satu still untuk QC visual
```

ffmpeg tidak ada di PATH sandbox ini; pasang tanpa root:
`pip install --break-system-packages imageio-ffmpeg`.
