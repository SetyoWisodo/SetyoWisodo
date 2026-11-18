---
name: threejs
description: Panduan memakai three.js untuk scene dan gerak kamera di web — renderer, mesh, material, GLTF, bayangan, dan loop animasi yang tidak bocor memori. Dipakai saat tugas butuh objek 3D sungguhan di peramban, bukan gambar tempelan.
license: MIT · mrdoob/three.js · commit 43678c04423a
---

# three.js — scene dan gerak kamera

| Fakta | Nilai |
| --- | --- |
| Repo | <https://github.com/mrdoob/three.js> |
| Bintang saat dicatat | 118.797 |
| Lisensi | MIT |
| Commit yang dibaca | `43678c04423a` (18 Nov 2026) |
| Pasang | `npm i three` |

## 1. Kapan dipakai, kapan jangan

**Pakai** kalau objeknya harus benar-benar 3D (bisa diputar, punya kedalaman, kena cahaya),
atau kamera yang bergerak di ruang.

**Jangan** pakai untuk: animasi DOM/SVG (→ `gsap`), video berbasis komponen (→ `remotion`),
diagram isometrik statis (→ `anatomy`), atau satu gambar produk diam (render offline lebih murah).

## 2. Kerangka minimum yang benar

```js
import * as THREE from 'three';

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));   // 3 = biang lambat di ponsel
renderer.setSize(w, h);
renderer.outputColorSpace = THREE.SRGBColorSpace;        // warna jangan pucat
renderer.toneMapping = THREE.ACESFilmicToneMapping;      // kalau ada lampu kuat
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;

const scene = new THREE.Scene();
const kamera = new THREE.PerspectiveCamera(38, w / h, 0.1, 100);

// satu key + satu fill: lebih mudah dikontrol daripada banyak lampu kecil
const key = new THREE.DirectionalLight(0xffffff, 2.4);
key.position.set(-3, 5, 4);
key.castShadow = true;
scene.add(key);
scene.add(new THREE.HemisphereLight(0xffffff, 0x444444, 0.6));

renderer.setAnimationLoop((t) => {
  mesh.rotation.y = t * 0.0004;
  renderer.render(scene, kamera);
});
```

`setAnimationLoop` dipakai, bukan `requestAnimationFrame` sendiri: itu yang membuat render
berhenti bersih saat tab disembunyikan dan saat XR.

## 3. Hal yang paling sering salah

| Gejala | Sebab | Perbaikan |
| --- | --- | --- |
| Gambar buram | `setPixelRatio` tidak diset / kanvas CSS beda ukuran | `setPixelRatio(min(dpr,2))` + `resize` saat `ResizeObserver` |
| Warna pucat atau terlalu kontras | ruang warna tidak diset | `outputColorSpace = SRGBColorSpace`, tekstur `.colorSpace = SRGBColorSpace` |
| Bayangan bergerigi | peta bayangan kecil | `key.shadow.mapSize.set(2048,2048)`, `shadow.bias = -0.0005` |
| Objek hilang sebagian | material `side:FrontSide` pada bidang tipis | `side: THREE.DoubleSide` untuk bidang |
| Memori naik terus | `geometry`/`material`/`texture` tidak di-`dispose()` | buang di akhir: `.dispose()` untuk ketiganya |
| Model GLTF gelap | tanpa environment | `RoomEnvironment` + `PMREMGenerator`, atau `HemisphereLight` |
| Siluet bergerigi di tepi | tanpa AA/MSAA | `antialias: true` dan hindari `pixelRatio` pecahan |

## 4. Aset dan lisensi

- Model: `GLTFLoader` dari `three/addons/loaders/GLTFLoader.js`; kompresi pakai
  `DRACOLoader` — dekoder **wajib lokal**, bukan dari CDN.
- Tekstur: `.ktx2` untuk GPU, bukan `.png` 4 MB.
- Repo ini melarang CDN: salin `three.module.js` ke `assets/vendor/` atau pakai bundler.

## 5. Mencocokkan dengan repo ini

- Kamera produk: `fov` 30–40°, jarak 3–4× tinggi objek, pitch −4° — angka yang sama dengan
  `nocturne-koffie/tools/foto.py`, supaya model 3D di web dan foto katalog tidak bertengkar.
- Cahaya: key dari kiri-atas `(-0.40, -0.62, 0.67)` dinormalkan, pemantul kanan `(0.74, 0.06, 0.67)`.
- Ukuran muat: satu scene produk < 400 KB total (json + bin + tekstur).
