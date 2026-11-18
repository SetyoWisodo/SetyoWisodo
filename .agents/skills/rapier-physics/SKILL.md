---
name: rapier-physics
description: Fisika nyata untuk scene React Three Fiber pakai @react-three/rapier — gravitasi, tumbukan, sendi, dan cara menahan biaya simulasi. Dipakai saat objek harus jatuh, menabrak, berguling, atau menumpuk, bukan bergerak di jalur yang sudah dipatok.
license: MIT · pmndrs/react-three-rapier · commit ae5c3fede5ca
---

# @react-three/rapier — fisika untuk React Three Fiber

| Fakta | Nilai |
| --- | --- |
| Repo | <https://github.com/pmndrs/react-three-rapier> |
| Bintang saat dicatat | 1.675 (**di bawah ambang 3.000 yang biasa dipakai repo ini**) |
| Lisensi | MIT |
| Commit yang dibaca | `ae5c3fede5ca` |
| Pasang | `npm i @react-three/rapier` |

## 1. Kapan dipakai

**Pakai** kalau gerak harus *muncul* dari aturan (gravitasi, pantulan, gesekan) — biji kopi
yang tumpah ke meja, tutup yang jatuh dan berputar, kotak yang ditumpuk.

**Jangan** pakai kalau geraknya sudah ditentukan sutradara: timeline GSAP atau Remotion
lebih murah dan deterministik (simulasi fisika tidak identik di dua mesin).

## 2. Kerangka minimum

```jsx
import { Canvas } from '@react-three/fiber';
import { Physics, RigidBody, CuboidCollider, useRapier } from '@react-three/rapier';

<Canvas shadows camera={{ position: [0, 1.4, 4], fov: 38 }}>
  <Physics gravity={[0, -9.81, 0]} timeStep="vary" interpolate>
    <RigidBody type="fixed"><CuboidCollider args={[4, 0.1, 4]} position={[0, -0.1, 0]} /></RigidBody>
    <RigidBody colliders="hull" restitution={0.2} friction={0.9} position={[0, 2, 0]}>
      <mesh castShadow>{/* geometry + material */}</mesh>
    </RigidBody>
  </Physics>
</Canvas>
```

- `colliders`: `"cuboid" | "ball" | "capsule" | "trimesh" | "convexHull" | "hull"`.
  Trimesh mahal dan hanya untuk benda diam bertopografi rumit.
- `type`: `"dynamic" | "fixed" | "kinematicPosition" | "kinematicVelocity"`.
- `timeStep="vary"` mengikuti fps; `timeStep={1/60}` untuk hasil yang bisa diulang.

## 3. Jebakan

| Gejala | Sebab | Perbaikan |
| --- | --- | --- |
| Benda tembus lantai | benda terlalu kecil/cepat, collider tipis | `ccd` di `RigidBody`, lantai `fixed` yang tebal |
| Fisika "meledak" | massa/ukuran tidak wajar (satuan meter, bukan cm) | patuhi 1 unit = 1 m |
| Animasi tersendat | simulasi jalan tiap frame tanpa batas | `paused` saat `useFrame` di luar viewport |
| Benda diam terus | `type="fixed"` pada yang harus bergerak | ganti ke `dynamic` |
| Hasil render video beda dari layar | `timeStep="vary"` | pakai `timeStep={1/60}` + `interpolate` |
| Posisi berkedip saat React re-render | posisi ditulis lewat state tiap frame | tulis lewat `ref` ke `setNextKinematicTranslation` |

## 4. Untuk repo ini

Kalau nanti dipakai di `rak/`, angka pitch/yaw harus tetap sama dengan `rak/data.js` supaya
kamera CSS dan kamera WebGL tidak melompat saat scene dimuat. Fisika **tidak** dipakai untuk
foto katalog (foto dirender `tools/foto.py`, deterministik).
