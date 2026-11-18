---
name: lottie
description: Memutar animasi vektor Lottie di web pakai lottie-web — loadAnimation, kendali dari kode, dan cara menjaga berkas tetap ringan. Dipakai saat animasi ikon atau ilustrasi perlu jalan di semua peramban tanpa video dan tanpa JS animasi tambahan.
license: MIT · airbnb/lottie-web · commit bede03d25d23
---

# lottie-web — animasi vektor ringan

| Fakta | Nilai |
| --- | --- |
| Repo | <https://github.com/airbnb/lottie-web> |
| Bintang saat dicatat | 32.497 |
| Lisensi | MIT |
| Commit yang dibaca | `bede03d25d23` |
| Pasang | `npm i lottie-web` |

## 1. Kapan dipakai

**Pakai** untuk animasi ikon/ilustrasi yang rumit tapi kecil (< 100 KB), diputar sekali saat
masuk, atau berulang sebagai penanda proses.

**Jangan** pakai untuk teks yang harus bisa diseleksi (render SVG jadi jalur, bukan huruf),
atau untuk animasi interaktif rumit (→ `gsap`/`threejs`).

## 2. Kerangka minimum

```js
import lottie from 'lottie-web';

const anim = lottie.loadAnimation({
  container: document.getElementById('kopi'),
  renderer: 'svg',            // 'canvas' lebih cepat, tidak bisa di-CSS
  loop: false,
  autoplay: false,
  path: '/assets/lottie/seduh.json',   // aset lokal, bukan CDN
});
anim.setSpeed(0.9);
anim.addEventListener('DOMLoaded', () => anim.play());
anim.addEventListener('complete', () => anim.pause());
```

Kendali kode: `goToAndStop(frame, true)`, `playSegments([[0, 30]], true)`,
`setDirection(-1)` untuk memutar balik.

## 3. Jebakan

| Gejala | Sebab | Perbaikan |
| --- | --- | --- |
| Animasi tidak muncul | berkas JSON dari After Effects berisi `assets` gambar eksternal | sematkan gambar, atau ekstrak ke folder yang sama |
| Buram di layar retina | `renderer: 'canvas'` tanpa `devicePixelRatio` | pakai `svg`, atau set DPR |
| Gerak pertama tersendat | JSON diunduh saat animasi mulai | `preload` dan mulai setelah `DOMLoaded` |
| Tidak mau berhenti | `loop: true` | `loop: false` + event `complete` |
| Berat | JSON tanpa optimasi | buang layer tak terpakai (bodymovin), target < 100 KB |

## 4. Repo ini

Lottie dipakai untuk penanda kecil (sedang menyeduh, sedang memuat), bukan untuk hero.
Berkas di `assets/lottie/`, dimuat `lazy` setelah fold, dan tetap ada versi `prefers-reduced-motion`
(hentikan di frame akhir).
