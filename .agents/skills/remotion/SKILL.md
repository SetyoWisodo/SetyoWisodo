---
name: remotion
description: Mesin video berbasis React pakai Remotion — komponen sebagai frame, interpolate/spring, Sequence, dan render mp4 yang bisa diulang. Dipakai saat video harus dibuat dari data (katalog, harga, label) dan dirender banyak versi secara otomatis.
license: Remotion License (bukan MIT; gratis untuk individu & perusahaan kecil) · remotion-dev/remotion · commit 8919b283f361
---

# Remotion — video sebagai komponen

| Fakta | Nilai |
| --- | --- |
| Repo | <https://github.com/remotion-dev/remotion> |
| Bintang saat dicatat | 73.999 |
| Lisensi | Remotion License — **bukan MIT**; baca `LICENSE.md` sebelum dipakai komersial |
| Commit yang dibaca | `8919b283f361` |
| Pasang | `npx create-video@latest` atau `npm i remotion @remotion/cli react react-dom` |

## 1. Kapan dipakai

**Pakai** kalau video harus lahir dari data yang sama dengan situs: sembilan lot, harga dari
`data/catalog.json`, label yang sudah dirender. Satu komposisi, sembilan keluaran, tanpa
menyunting manual di editor video.

**Jangan** pakai untuk gerak UI di situs (→ `gsap`) atau animasi 3D penuh (→ `three.js`
di dalam komposisi tetap mungkin, tapi render per frame berat).

## 2. Kerangka minimum

```jsx
import { Composition, useCurrentFrame, useVideoConfig, interpolate, spring, Sequence, AbsoluteFill } from 'remotion';

const Lot = ({ data }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const masuk = spring({ frame, fps, config: { damping: 18, stiffness: 120 } });
  const keluar = interpolate(frame, [durationInFrames - 20, durationInFrames], [1, 0], {
    extrapolateLeft: 'clamp',
  });
  return (
    <AbsoluteFill style={{ backgroundColor: '#EDEBE6' }}>
      <div style={{ opacity: masuk * keluar, transform: `translateY(${(1 - masuk) * 24}px)` }}>
        {data.name}
      </div>
    </AbsoluteFill>
  );
};

export const Root = () => (
  <Composition id="Lot" component={Lot} durationInFrames={90} fps={30} width={1080} height={1350}
    defaultProps={{ data: { name: 'Gayo' } }} />
);
```

Render: `npx remotion render Lot out/lot.mp4 --props=lot.json` (batch: `--concurrency`).

## 3. Jebakan

| Gejala | Sebab | Perbaikan |
| --- | --- | --- |
| Animasi tidak deterministik | memakai `Date.now()`/`Math.random()` | turunkan dari `frame` dan `random(seed)` bawaan |
| Render lambat | aset dari jaringan, font dari CDN | font lokal di `public/`, gambar lokal |
| Hasil beda antar versi | versi `remotion` dan `@remotion/cli` tidak sama | samakan versi, kunci di `package.json` |
| Video tersendat | animasi berat di luar `useCurrentFrame` | hitung semua di render, tanpa `setTimeout` |
| Teks terpotong | ukuran font tetap untuk rasio berbeda | ukur dari `width`/`height` komposisi |

## 4. Repo ini

Butuh ffmpeg lokal untuk render (lihat `ffmpeg-encode`). Jangan merender video ke dalam
halaman web; simpan mp4 di `assets/` dan muat sebagai `<video>` biasa dengan poster gambar.
