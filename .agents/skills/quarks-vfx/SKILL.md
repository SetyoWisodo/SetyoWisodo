---
name: quarks-vfx
description: Sistem partikel untuk three.js pakai three.quarks — asap, percikan, debu, jejak, dan cara memuat efek buatan editor tanpa kehilangan kendali atas draw call. Dipakai saat scene butuh VFX yang hidup, bukan tekstur berkedip.
license: MIT · Alchemist0823/three.quarks · commit 9d0445c5949c
---

# three.quarks — partikel dan VFX

| Fakta | Nilai |
| --- | --- |
| Repo | <https://github.com/Alchemist0823/three.quarks> |
| Bintang saat dicatat | 1.227 (**di bawah ambang 3.000**) |
| Lisensi | MIT |
| Commit yang dibaca | `9d0445c5949c` |
| Pasang | `npm i three.quarks` |

## 1. Kapan dipakai

**Pakai** untuk asap di kopi panas, debu saat kemasan jatuh, percikan, jejak gerak — dan
untuk mengimpor efek buatan Unity Shuriken atau editor quarks (JSON).

**Jangan** pakai untuk gerak objek tunggal (itu timeline), atau untuk partikel yang harus
terlihat identik di setiap frame render video tanpa dikunci waktunya.

## 2. Kerangka minimum

```js
import * as THREE from 'three';
import {
  BatchedRenderer, ParticleSystem, ConstantValue, IntervalValue, ConstantColor,
} from 'three.quarks';

const batched = new BatchedRenderer();
scene.add(batched);

const efek = new ParticleSystem({
  duration: 2,
  looping: true,
  startLife: new IntervalValue(0.6, 1.2),
  startSpeed: new IntervalValue(0.05, 0.25),
  startSize: new IntervalValue(0.02, 0.06),
  startColor: new ConstantColor(new THREE.Vector4(1, 1, 1, 0.35)),
  emissionOverTime: new ConstantValue(28),
  shape: new THREE.Vector3(0.05, 0, 0.05),
});
efek.position.set(0, 0.6, 0);
batched.addSystem(efek);

// tiap frame
batched.update(dt);
```

`BatchedRenderer` menggabungkan semua sistem jadi sedikit draw call — inilah alasan memilih
pustaka ini dibanding partikel `THREE.Points` buatan sendiri.

## 3. Jebakan

| Gejala | Sebab | Perbaikan |
| --- | --- | --- |
| Partikel tidak muncul | material butuh `transparent` + blending aditif | `material.transparent = true`, `depthWrite = false` |
| Semua partikel satu warna | `startColor` memakai `Color` bukan `Vector4` | `new THREE.Vector4(r,g,b,a)` |
| fps jatuh | ribuan partikel tanpa batas | `emissionOverTime` + tekstur kecil (64²) |
| Hasil render beda tiap frame | `dt` dari jam nyata | kunci `dt = 1/fps` saat render video |
| Efek dari editor tidak jalan | versi editor ≠ versi pustaka | catat versi, muat lewat `QuarksLoader` |

## 4. Repo ini

Partikel untuk halaman demo saja; halaman awal tanpa VFX. Kalau efek masuk ke video Remotion,
`dt` **wajib** `1/30` (fps keluaran), bukan waktu nyata — kalau tidak, dua render berbeda.
