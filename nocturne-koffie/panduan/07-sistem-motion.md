# Sistem Gerak (Motion) — Nocturne Koffie

Referensi: gaya situs seperti [motionsites.ai](https://motionsites.ai/) — hero bergerak,
scroll-driven reveal, tipografi besar yang masuk bertopeng, kursor yang bereaksi.
Dokumen ini mencatat **5 skill motion teratas** yang jadi acuan, apa yang diambil dari
masing-masing, dan **spesifikasi gerak yang benar-benar dipasang** di landing page.

Status: **terpasang** (`assets/css/motion.css` + `assets/js/motion.js`). Tanpa library,
tanpa build step.

---

## 1. Hasil pencarian: 5 skill motion teratas

Diverifikasi lewat GitHub API pada 29 Okt 2026 (bintang, lisensi, isi repo).

| # | Repo | ★ | Lisensi | Fokus | Yang saya ambil |
| --- | --- | --- | --- | --- | --- |
| 1 | [greensock/gsap-skills](https://github.com/greensock/gsap-skills) | 17.462 | MIT | Skill resmi GSAP: core, timeline, **ScrollTrigger**, performance, `matchMedia` | Semantik scroll-trigger (`start`/`end`, `scrub` = animasi "mengejar" posisi scroll), aturan **hanya animasikan transform & opacity**, `gsap.matchMedia()` untuk reduced-motion. Saya tidak memakai GSAP-nya (lihat §2), tapi perilakunya ditiru |
| 2 | [Jakubantalik/transitions.dev](https://github.com/Jakubantalik/transitions.dev) | 5.898 | source-available | 43 transisi UI siap tempel, tiap snippet membawa **guard `prefers-reduced-motion`** | Token durasi/easing, pola *origin-aware* untuk panel menu, transisi harga/teks (blur + geser), aturan "setiap transisi wajib punya versi statis" |
| 3 | [oil-oil/oil-motion](https://github.com/oil-oil/oil-motion) | 2.715 | MIT | Animasi web dari video/sequence: scroll, pointer, drag, sentuh, gyro | **Taksonomi driver** (`scroll \| pointer \| drag \| touch \| time`) dan tiga mode waktu (`scrub`, `segment-play`, `autonomous`). Ini yang membuat gerak saya punya "sebab", bukan sekadar diputar |
| 4 | [AThevon/genjutsu](https://github.com/AThevon/genjutsu) | 702 | source-available | Creative coding: motion, **micro-interaction**, design system di Web/GSAP/Motion/Three | Bahasa micro-interaction: tombol punya tekanan & kilau, chip "pop" saat dipilih, harga bergeser saat berubah, kursor sebagai lapisan suasana |
| 5 | [agiwhitelist/auteur](https://github.com/agiwhitelist/auteur) | 1.044 | MIT | "Mengarahkan website seperti film" + linter anti-slop | Disiplin arah: **satu ide gerak per seksi**, tidak ada animasi tanpa fungsi, dan linter anti-slop versi manual (daftar larangan di §6) |

Sebutan terhormat (tidak dipakai langsung): `freshtechbro/claudedesignskills` (1.168★, 3D/graphics),
`juliobsz/skills` (1.020★, "award-caliber websites"), `199-biotechnologies/motion-dev-animations-skill`
(215★, Motion.dev/spring), `MustBeSimo/web-design-studio` (50★, cinematic scroll).

> Catatan kejujuran: repo-repo itu adalah **skill untuk agent**, bukan kode yang bisa di-`npm install`.
> Isinya panduan cara mengerjakan animasi. Yang saya pakai adalah prinsip + spesifikasi teknisnya,
> lalu saya tulis ulang implementasinya untuk situs ini.

---

## 2. Kenapa tanpa GSAP / tanpa React

| Pilihan | Alasan ditolak |
| --- | --- |
| GSAP + ScrollTrigger via CDN | Menambah ±70 KB JS + satu titik gagal jaringan. Preview in-app memblokir sebagian sumber eksternal; kalau CDN gagal, halaman kehilangan seluruh geraknya |
| Framer Motion / Motion One | Butuh React atau bundler — brief 14 memilih situs statis ringan |
| Video/WebGL hero | Bertentangan dengan 5.8 brief: **hero sengaja tanpa gambar** agar cepat di HP. motionsites.ai banyak memakai video 3D; itu justru yang tidak boleh ditiru untuk brand ini |

Yang saya bangun: **mini-engine ±200 baris** (IntersectionObserver + satu loop `rAF`),
memakai properti yang sama dengan yang diajarkan gsap-skills. Kalau nanti butuh `pin` dan
`scrub` rumit, `motion.js` bisa diganti GSAP tanpa mengubah CSS (kelasnya sudah terpisah).

---

## 3. Token gerak (satu keluarga easing)

| Token | Nilai | Dipakai untuk |
| --- | --- | --- |
| `--ease-out` | `cubic-bezier(.16,1,.3,1)` (expo out) | Semua elemen **masuk** — cepat di awal, mendarat pelan |
| `--ease-in-out` | `cubic-bezier(.65,0,.35,1)` | Perubahan state (warna chip, filter) |
| `--ease-spring` | `cubic-bezier(.34,1.56,.64,1)` | Umpan balik sentuhan saja (chip, tombol) — **jangan** untuk elemen besar |
| `--d-fast` | 240 ms | Hover, chip, warna |
| `--d-mid` | 620 ms | Reveal teks & kartu |
| `--d-slow` | 900 ms | Topeng headline, media produk |
| `--d-intro` | 1100 ms | Rangkaian pembuka total |

Aturan: **maksimal dua durasi berbeda dalam satu layar**; stagger 55–90 ms.

---

## 4. Daftar gerak yang terpasang (M01–M13)

| Kode | Nama | Pemicu (driver) | Properti | Durasi | Tujuan |
| --- | --- | --- | --- | --- | --- |
| M01 | Intro berurutan | time (saat muat) | `opacity`, `translateY` | 240–900 ms, cascade 120→520 ms | Navbar → headline baris 1 → baris 2 → paragraf → kartu hero. Mata dibimbing dari kiri atas ke deretan produk |
| M02 | Topeng headline | time | `translateY(108%)` → 0, `overflow:hidden` | 900 ms | Tipografi terasa "tercetak", bukan muncul biasa |
| M03 | Bar kemajuan gulir | scroll | `scaleX` | kontinu | Umpan balik posisi; 2 px, warna orange→gold |
| M04 | Reveal seksi | scroll (IO) | `opacity`, `translateY 26px` | 620 ms | Tiap seksi masuk sekali, lalu diam |
| M05 | Topeng media produk | scroll (IO) | `clip-path inset()` + `scale 1.06→1` | 900 ms | Foto stiker terasa dibuka seperti halaman majalah |
| M06 | Stagger kartu | scroll (IO) | `opacity`, `translateY`, delay `(i%2)*80ms` | 620 ms | Dua kolom masuk bergilir, tidak serempak |
| M07 | Parallax hero | scroll | `translateY` judul/paragraf, `translateX` marquee, `opacity` hero | kontinu | Hero "tertinggal" saat digulir — kedalaman tanpa gambar |
| M08 | Parallax label & poster | scroll | `translateY/translateX` | kontinu | Judul koleksi melayang halus; poster footer bergeser 46 px |
| M09 | Quote manifesto | scroll | `opacity .35→1`, `translateY 16→0` | kontinu | Kutipan "menyala" saat pembaca sampai |
| M10 | Magnet tombol | pointer | `translate3d` ≤ 7 px | 260 ms | Tombol terasa "hidup" dan mudah diklik |
| M11 | Tilt kartu | pointer | `perspective(900px) rotateX/Y` ≤ 3,5° | lerp 0.14/frame | Media sedikit mengikuti kursor; bukan efek mainan karena kecil |
| M12 | Glow kursor hero | pointer | `translate3d` + radial gradient, lerp 0.09 | kontinu | Suasana hangat di hero; hilang di bagian lain supaya tidak norak |
| M13 | Umpan balik mikro | event | kilau tombol (`::after`), chip pop, harga geser, panel menu turun berurutan | 320–620 ms | Konfirmasi bahwa aksi diterima |

Ditambah yang sudah ada sebelumnya: marquee nama produk (otomatis, bisa dijeda),
marquee teks pemisah, garis rail yang tumbuh (`scaleX`), langkah manifesto & paket
langganan yang masuk bergilir.

---

## 5. Aturan yang dipegang (dari 5 skill di atas)

1. **Hanya `transform` dan `opacity`.** Tidak pernah `width`, `top`, `margin`, atau `filter: blur` besar — itu memicu layout/paint dan bikin scroll tersendat di HP kelas menengah.
2. **Satu sebab per gerak.** Scroll, pointer, atau waktu. Tidak ada animasi yang berjalan sendiri di luar viewport.
3. **Sekali jalan.** Reveal memakai `once` (`io.unobserve`) — kecuali bar kemajuan yang memang kontinu.
4. **Tidak ada gerak tanpa fungsi.** Kalau animasi tidak menuntun mata atau mengonfirmasi aksi, ia dihapus.
5. **Stagger, bukan serempak.** Maksimal 8 item per kelompok (lebih dari itu terasa lambat, bukan mewah).
6. **Reduced motion adalah lapis kedua.** CSS `@media` + kelas `html.no-motion` + `matchMedia` runtime (kalau pengguna mengubah setelan saat halaman terbuka).

### Performa

| Aturan | Angka |
| --- | --- |
| `will-change` | hanya saat animasi aktif, dilepas setelahnya (`.rv.is-in` mengembalikan `will-change:auto`) |
| Loop `rAF` | **satu** loop untuk semua parallax, di-throttle dengan flag `ticking` |
| Elemen yang diukur per frame | ≤ 10 (hero, poster, quote, layer ber-`data-parallax`) |
| Pointer handler | hanya `pointermove` yang di-lerp di dalam `rAF`, tidak menulis style langsung tiap event |
| Target | 60 fps di HP 2–4 juta rupiah; tidak ada pergeseran layout (CLS 0 dari gerak) |

---

## 6. Larangan (linter anti-slop versi manual)

| Jangan | Kenapa |
| --- | --- |
| Animasi `bounce`/`elastic` pada elemen besar atau teks | Terasa murah; simpan untuk umpan balik sentuhan kecil |
| Teks huruf-per-huruf (typewriter/scramble) | Mengganggu pembacaan, dan brand ini menjual ketenangan |
| Parallax pada teks body | Menyulitkan membaca; parallax hanya untuk judul, quote, poster |
| Kursor kustom yang menggantikan kursor asli | Risiko aksesibilitas & terasa norak di perangkat sentuh |
| Gerak berulang abadi selain marquee | Baterai & perhatian; marquee pun wajib bisa dijeda |
| Video/3D di hero | Melanggar keputusan brief 5.8 (hero ringan, tanpa gambar) |
| Animasi saat `prefers-reduced-motion: reduce` | Wajib mati total, bukan diperlambat |
| Lebih dari satu aksen warna dalam satu animasi | Melanggar aturan visual brief 12 |

---

## 7. Cara mengubah / menambah gerak

| Ingin | Lakukan |
| --- | --- |
| Ubah kecepatan semua reveal | Ubah `--d-mid` di `assets/css/motion.css` (`:root`) |
| Ubah intensitas parallax | Atribut `data-parallax="0.05"` di HTML; 0 = diam, 0.12 = kuat |
| Matikan satu efek | Hapus kelas/atribut terkait (`data-rv`, `data-parallax`) — tidak ada JS yang perlu diubah |
| Tambah elemen yang muncul saat digulir | Beri `data-rv` (dan `data-rv-delay="80ms"` bila perlu) |
| Tambah elemen parallax | Beri `data-parallax="0.06"` |
| Naik ke GSAP nanti | Ganti isi `motion.js`; CSS `.rv`, `.is-in`, `.lm` tetap dipakai |

---

## 8. Uji sebelum tayang (10 butir)

- [ ] 1. Muat ulang halaman: navbar → headline → paragraf → kartu hero masuk berurutan, tidak ada kedipan konten mentah.
- [ ] 2. Tidak ada elemen yang tetap tak terlihat setelah halaman selesai dimuat (uji juga dengan koneksi lambat / throttle 3G).
- [ ] 3. Gulir dari atas ke bawah: tiap seksi muncul **sekali**, tidak berkedip saat naik-turun.
- [ ] 4. Bar kemajuan gulir bergerak mulus sampai ujung halaman.
- [ ] 5. Hero memudar/melayang saat digulir, dan pulih saat kembali ke atas.
- [ ] 6. Kursor di hero memunculkan glow; keluar hero → glow hilang.
- [ ] 7. Tombol bergerak halus saat disentuh kursor, kembali ke posisi semula saat kursor pergi.
- [ ] 8. Tilt kartu maksimal terasa halus (tidak goyang), dan **mati** di perangkat sentuh.
- [ ] 9. Setelan OS "Reduce Motion" → semua statis, semua konten terbaca, tidak ada elemen hilang.
- [ ] 10. DevTools Performance saat scroll: tidak ada frame > 33 ms beruntun; tidak ada peringatan layout shift dari animasi.

---

## 9. Kalau ingin lebih agresif (opsi, belum dipasang)

| Opsi | Biaya | Risiko |
| --- | --- | --- |
| GSAP + ScrollTrigger (pin & scrub penuh) | ±70 KB JS | Titik gagal CDN; perlu fallback |
| Hero dengan canvas partikel/WebGL | 200 KB+, GPU berat di HP | Bertentangan dengan 5.8 (hero ringan) |
| Horizontal scroll untuk Our Collection | Sedang | Menyembunyikan 7 dari 9 produk; buruk untuk katalog |
| Page-transition ala motionsites | Sedang | Situs ini satu halaman; tidak ada halaman tujuan |
| Cursor kustom penuh | Rendah | Aksesibilitas & kesan "template" |

Rekomendasi: **jangan** tambah lagi sebelum ada data. Gerak yang ada sekarang sudah
"cukup hidup" untuk brand kopi premium; menambah efek berisiko menggeser kesan dari
*tenang-mahal* ke *ramai*.

---

## 8. Pembaruan 30 Okt 2026 — tujuh repo desain diterapkan

Post `@thegreatest_sv` (29 Okt 2026) menyebut tujuh repo. Yang diterapkan di sini, dan yang tidak:

| Repo | Status di repo ini |
| --- | --- |
| `nextlevelbuilder/ui-ux-pro-max-skill` | **dipakai prinsipnya** — disiplin token lewat `data/design-system.json` |
| `pbakaus/impeccable` | **dipakai** — 62 antipattern jadi 29 aturan di `tools/slop.py` |
| `GLips/Figma-Context-MCP` | **prinsip saja** — tidak ada akun Figma; kontrak JSON menggantikan perannya |
| `DavidHDev/react-bits` | **dipakai, ditulis ulang vanilla** — spotlight, count-up, magnet, teks per kata |
| `greensock/gsap-skills` | **aturan performa dipakai**, GSAP-nya tidak (lihat §2) |
| `heygen-com/hyperframes` | **dipakai idenya** — adegan 9:16 HTML + timeline, tanpa render server |
| `ahujasid/mcp-for-blender` | **tidak dipakai** — tidak ada Blender; 3D sebatas CSS tilt ≤ 3,5° |

Playbook lengkap: [`skills/motion-web/SKILL.md`](../skills/motion-web/SKILL.md).
Lab gerak (komponen hidup + 5 adegan): `/motion/index.html`.
Audit terakhir: `laporan/slop.md`.

**Yang berubah dari versi 1 dokumen ini:**

1. `--ease-spring` tidak lagi memantul: `cubic-bezier(.34,1.56,.64,1)` → `cubic-bezier(.2,.8,.2,1)`.
   Overshoot pada chip/tombol adalah salah satu penanda UI buatan mesin.
2. Denyut `pulseTarget` pada kartu target dihapus; diganti cincin statis 3 px.
3. Oranye tidak lagi dipakai untuk teks kecil (kontras 3,33:1 di atas kertas). Teks kecil memakai
   `--espresso` (11:1); oranye tetap untuk garis, panah, dan teks ≥ 24 px.
4. Tombol CTA berisi teks `--ink` di atas oranye (4,91:1) — sebelumnya putih (3,82:1).
5. `will-change` hanya dipasang pada lapisan yang bergerak terus (bilah gulir, glow kursor,
   poster footer, kutipan manifesto, ticker); elemen yang masuk sekali tidak lagi memakainya.
6. Label mikro minimum 10 px; sebelumnya ada 8,5 px.

## 9. Pembaruan 30 Okt 2026 (kedua) — landing page gaya 3D

Permintaan: *"gaya landing page-nya sangat 3D seperti website di postingan itu"* (post
`@viktoroddy`, 30 Okt 2026 — motionsites, land-book, landdding, recent.design, 60fps).

Yang dibaca dari galeri itu bukan warna atau layout tertentu (itu milik brand masing-masing),
melainkan **struktur panggung**: satu titik hilang, objek berlapis di `translateZ` berbeda,
petak lantai sebagai petunjuk kedalaman, dan kamera yang bergerak halus.

| Aspek | Keputusan | Alasan |
| --- | --- | --- |
| Teknologi | CSS 3D (`perspective`, `preserve-3d`, `translateZ`) | WebGL/three.js menambah ±600 KB dan menyulitkan audit token |
| Jumlah panggung | **satu per halaman** (hero kampanye) | dua panggung = halaman terasa demo, bukan katalog |
| Kedalaman | kartu depan `+44px`, belakang `-96px`, chip `+190px` | hierarki: angka terpenting paling dekat |
| Rotasi | kursor 14° (`rotateY`) / 8° (`rotateX`); kartu timbul 8°/6° | di atas 15° teks mulai sulit dibaca |
| Dolly gulir | maks 150 px | memberi "kamera mundur" tanpa efek parallax liar |
| Silinder klip | 5 pane, 72°, radius 292 px, perspective 1400 px | cukup untuk 5 aset 9:16; pane depan 1,26× |
| Jatuh datar | tanpa JS · < 900 px · reduced-motion | korsel jadi grid, kartu tidak miring, judul tanpa bayangan |
| Berat | 16,0 KB CSS+JS | naik dari 13,7 KB; batas audit 24 KB |

Tipografi judul memakai bayangan bertumpuk **tiga lapis tipis** (`0 1px`, `0 2px`, `0 3px`) plus
satu bayangan jauh, bukan gradien dan bukan glow — gradien teks adalah temuan kritis di `slop.py`.

Gerbang baru: `tools/periksa.py` cek **Panggung 3D** (berkas ada, `perspective`/`preserve-3d`/
`translateZ` terpakai, gerbang 900 px, listener pasif, reduced-motion, komponen `data-3d` dikenali,
berat ≤ 24 KB). Hasil terakhir: 19 lolos · 0 peringatan · 0 gagal.

## 10. Pembaruan 30 Okt 2026 (ketiga) — 20 repo motion → lembar film

Post `@Mikadzyki_NFT` (28 Okt 2026) mendaftar 20 repo motion design. Semua tautan dilacak ke
repo aslinya, lalu dipilah: **6 dipakai aturannya, 6 dipakai prinsipnya, 8 tidak dipakai**
karena menuntut Node/React/Chromium/ffmpeg/After Effects yang tidak ada di sandbox.

| Yang dipakai | Dari | Wujudnya di repo ini |
| --- | --- | --- |
| `seek(t)` deterministik, 2 rAF setelah seek, beat map, larangan angka karangan | `howseen-ai/claude-motion-design` | `motion/frame-0N.html` + lembar film |
| tabel durasi, hukum A1/A6/A18, matematika beat-sync | `t3knobox/klik-anim-skill-creation` | `motion/film-sheet.md` §1–2 |
| tabel durasi UI, 1/3 rule, anggaran stagger | `LottieFiles/motion-design-skill` | `skills/motion-film` hukum 5–6 |
| satu bentuk, transformasi bukan cut; spring damping ≥ 0,72 | `AbubakrChan/product-launch-motion`, `199-biotechnologies/motion-dev-animations-skill` | hukum 7–8 |

| Angka yang sekarang mengikat | Nilai |
| --- | --- |
| Tempo | 120 BPM (alasan aritmetika, bukan selera) |
| Grid | 30 frame/ketukan · 120 frame/birama · 540 frame/adegan |
| Arc | `cold-open`: tier 4 / 2 / 3 / 5 |
| Porsi lembah | 15–45% durasi adegan (sekarang 22%) |
| Durasi cue maksimum | 3,6 s (frasa kamera) |

Gerbang baru: `tools/periksa.py` cek **Film gerak** — 20 cue di ketukan, frame cocok durasi,
arc punya puncak dan lembah, tidak ada angka tanpa sumber, skill terdokumentasi.
Hasil terakhir: **20 lolos · 0 peringatan · 0 gagal**.
