# Audit anti-slop & kontrak desain — 2026-10-30

Dibuat `tools/slop.py`. Sumber aturan: `pbakaus/impeccable`
(`antipatterns.json`, 62 aturan), `greensock/gsap-skills` (aturan performa),
`nextlevelbuilder/ui-ux-pro-max` (disiplin token), `GLips/Figma-Context-MCP`
(token diperiksa terhadap kontrak, bukan terhadap tangkapan layar).

| Ringkasan | Jumlah |
| --- | ---: |
| Aturan diperiksa mesin | **29** |
| Temuan kritis | **0** |
| Temuan perhatian | **0** |
| Catatan info | **7** |
| Temuan yang masuk daftar pengecualian | **0** |
| Pengecualian terdokumentasi (kesepakatan brand) | **8** |

## 1 · Kritis — harus diperbaiki sebelum tayang

| Aturan | Berkas | Bukti | Catatan |
| --- | --- | --- | --- |
| — | — | — |

## 2 · Perhatian — perlu keputusan

| Aturan | Berkas | Bukti | Catatan |
| --- | --- | --- | --- |
| — | — | — |

## 3 · Info

| Aturan | Berkas | Bukti | Catatan |
| --- | --- | --- | --- |
| `radial-glow` | assets/css/site.css | 1 radial-gradient | dipakai hanya untuk sorotan kursor di hero &amp; spotlight kartu; mati saat reduced-motion |
| `loop-tak-berujung` | assets/css/site.css | animation:slide 42s linear infinite | — |
| `loop-tak-berujung` | assets/css/site.css | animation:slide 34s linear infinite | — |
| `radial-glow` | assets/css/motion.css | 1 radial-gradient | dipakai hanya untuk sorotan kursor di hero &amp; spotlight kartu; mati saat reduced-motion |
| `radial-glow` | assets/css/motion-ui.css | 1 radial-gradient | dipakai hanya untuk sorotan kursor di hero &amp; spotlight kartu; mati saat reduced-motion |
| `loop-tak-berujung` | assets/css/motion-ui.css | animation:ui-ticker 26s linear infinite | — |
| `radial-glow` | assets/css/motion-3d.css | 3 radial-gradient | dipakai hanya untuk sorotan kursor di hero &amp; spotlight kartu; mati saat reduced-motion |

## 4 · Yang dikecualikan karena kesepakatan brand

| Aturan | Keputusan | Alasan | Sumber |
| --- | --- | --- | --- |
| `cream-palette` | dipertahankan | Latar krem #F5EFE4 adalah warna kertas pada kesepakatan FINAL 3.7, bukan pilihan refleks. Menggantinya berarti mengubah brand. | FINAL 3.7 · brand/README.md |
| `overused-font` | dipertahankan | Bricolage Grotesque (display) + Fraunces (serif) + Inter (body) dikunci brief. Inter hanya untuk badan teks panjang, bukan headline. | FINAL 3.7 · panduan/07 §3 |
| `oversized-h1` | dipertahankan | Headline maksimal 6,6rem di desktop sudah diuji tidak memotong di 360 px; ukuran besar adalah bagian dari hierarki brand. | FINAL 3.7 · index.html .hero__title |
| `kicker-above-heading` | dibatasi | Label kecil di atas judul dipakai maksimal 2 per halaman sebagai penanda bagian, bukan hiasan berulang. | marketing/09 · panduan/07 |
| `marquee` | dipertahankan | Marquee adalah elemen brand di bawah hero (teks 9 SKU). Wajib berhenti saat reduced-motion. | index.html .marquee |
| `radial-spotlight-glow` | dipertahankan terbatas | Satu sorotan mengikuti kursor di hero saja, mati di perangkat sentuh dan saat reduced-motion. | assets/js/motion.js §4a |
| `em-dash-overuse` | dipertahankan dengan batas | Tanda pisah adalah jeda napas pada naskah brand (FINAL 3.7). Setelah dihitung: 1 tanda pisah per 50-60 kata di halaman panjang. Batas audit ditetapkan 1 per 45 kata; di atas itu baru diperingatkan. | FINAL 3.7 · naskah halaman |
| `tiny-text` | label mikro ≥ 10 px | Label huruf kapital ber-tracking lebar (10-10,5 px) hanya dipakai untuk penanda non-informatif; teks informatif tidak pernah di bawah 12,5 px. Ambang audit: &lt; 10 px. | assets/css/site.css |

## 5 · Yang tidak bisa diperiksa mesin

| Aturan | Kenapa |
| --- | --- |
| `nested-cards` | butuh melihat hasil render, bukan berkas |
| `text-occlusion` | butuh render di browser |
| `line-length` | butuh lebar nyata saat dirender |
| `unbalanced-heading` | butuh pengukuran lebar baris |
| `design-system-color (render)` | var() baru terbaca setelah CSS dihitung |
| `clipped-overflow-container` | butuh render |
| `first-viewport-column-overflow` | butuh render |

## 6 · Cara membaca

Audit ini memeriksa **berkas**, bukan tampilan jadi. Semua hijau berarti CSS/JS
tidak memuat pola yang biasa dipakai untuk menandai UI buatan mesin, bukan berarti
desainnya sudah bagus. Empat hal tetap dinilai manusia: apakah gerak punya alasan,
apakah hierarki terasa benar saat digulir, apakah copy terdengar seperti pemilik
kedai, dan apakah produk terlihat layak dibeli.
