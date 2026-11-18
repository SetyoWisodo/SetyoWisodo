---
name: gsap
description: Timeline animasi web pakai GSAP — tween, timeline, ScrollTrigger, dan aturan performa untuk DOM serta SVG. Dipakai saat urutan gerak perlu dikendalikan presisi (mulai, tahan, tumpang tindih, mundur) tanpa menulis state machine sendiri.
license: GreenSock Standard "No Charge" License · greensock/GSAP · commit 5e6c35ff8eed
---

# GSAP — timeline yang bisa dipegang

| Fakta | Nilai |
| --- | --- |
| Repo | <https://github.com/greensock/GSAP> |
| Bintang saat dicatat | 30.867 |
| Lisensi | GreenSock Standard License (**bukan** MIT) — gratis untuk pemakaian biasa, cek teksnya sebelum dipakai di produk berbayar |
| Commit yang dibaca | `5e6c35ff8eed` |
| Pasang | `npm i gsap` |

## 1. Kapan dipakai

**Pakai** untuk urutan gerak di DOM/SVG yang butuh kontrol: jeda, `stagger`, `repeat`,
`yoyo`, `timeScale`, dan ScrollTrigger untuk gerak yang mengikuti gulir.

**Jangan** pakai untuk CSS murni yang cukup dengan `transition` (hover, warna, opacity),
atau untuk video yang dirender per frame (→ `remotion`).

## 2. Kerangka minimum

```js
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
gsap.registerPlugin(ScrollTrigger);

const tl = gsap.timeline({ defaults: { ease: 'power3.out', duration: 0.6 } });
tl.from('.kartu', { y: 24, opacity: 0, stagger: 0.06 })
  .to('.label', { rotate: 2, duration: 0.3 }, '<0.1');

gsap.to('.rak', {
  xPercent: -50,
  scrollTrigger: { trigger: '.rak', start: 'top bottom', end: 'bottom top', scrub: 0.6 },
});

// hormati permintaan sistem
if (matchMedia('(prefers-reduced-motion: reduce)').matches) tl.progress(1).pause();
```

## 3. Jebakan

| Gejala | Sebab | Perbaikan |
| --- | --- | --- |
| Elemen "melompat" sebelum animasi | FOUC: state awal belum diset | set `opacity:0` di CSS lalu `gsap.set`/`from` |
| Animasi berebut properti | dua tween pada properti yang sama | satu timeline, atau `overwrite: 'auto'` |
| ScrollTrigger salah posisi | tinggi layout berubah setelah font/aset | `ScrollTrigger.refresh()` setelah `load` |
| Gerak tersendat | menganimasikan `width/top/left` | animasikan `transform` dan `opacity` |
| Memori naik | timeline dibuat ulang tanpa `kill()` | `tl.kill()` saat komponen dilepas |
| Tidak jalan di tes tanpa peramban | GSAP butuh DOM nyata | uji di jsdom = bukan bukti rupa |

## 4. Repo ini

Aturan repo: **tanpa CDN** (salin ke `assets/vendor/` atau bundler), halaman awal < 1,5 MB,
dan gerak harus punya versi `prefers-reduced-motion`. Token warna/tipografi brief tidak boleh
diubah oleh animasi — GSAP hanya menggerakkan posisi, skala, dan opasitas.
