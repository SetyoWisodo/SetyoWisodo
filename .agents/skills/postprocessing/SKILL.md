---
name: postprocessing
description: Efek lensa dan film untuk scene React Three Fiber pakai @react-three/postprocessing — bloom, depth of field, film grain, chromatic aberration, vignette, dan urutan render yang mahal. Dipakai saat scene 3D sudah benar dan tinggal diberi rasa kamera.
license: MIT · pmndrs/react-postprocessing · commit e07ef9a890c8
---

# @react-three/postprocessing — rasa kamera

| Fakta | Nilai |
| --- | --- |
| Repo | <https://github.com/pmndrs/react-postprocessing> |
| Bintang saat dicatat | 1.651 (**di bawah ambang 3.000**) |
| Lisensi | MIT |
| Commit yang dibaca | `e07ef9a890c8` |
| Pasang | `npm i @react-three/postprocessing postprocessing` |

## 1. Kapan dipakai

**Pakai** setelah scene selesai: bloom untuk lampu/valve logam, DOF untuk memisahkan depan
dan belakang, grain untuk menghindari gambar "plastik", vignette secukupnya.

**Jangan** pakai sebagai penutup cacat pencahayaan. Bloom tidak memperbaiki lampu yang salah
arah; ia hanya mempertebal kesalahannya.

## 2. Kerangka minimum

```jsx
import { EffectComposer, Bloom, DepthOfField, Vignette, Noise } from '@react-three/postprocessing';
import { BlendFunction, KernelSize } from 'postprocessing';

<EffectComposer multisampling={4} disableNormalPass>
  <DepthOfField focusDistance={0.02} focalLength={0.04} bokehScale={3} />
  <Bloom intensity={0.45} luminanceThreshold={0.85} mipmapBlur kernelSize={KernelSize.LARGE} />
  <Noise opacity={0.03} blendFunction={BlendFunction.OVERLAY} />
  <Vignette darkness={0.35} offset={0.35} />
</EffectComposer>
```

Urutan penting: DOF → bloom → grain → vignette. Membalik urutan membuat bloom ikut kabur.

## 3. Biaya dan jebakan

| Gejala | Sebab | Perbaikan |
| --- | --- | --- |
| fps jatuh separuh | `multisampling={8}` + bloom mipmap di layar 3× | `multisampling={2..4}`, `dpr` dibatasi 1,5 |
| Bloom di mana-mana | `luminanceThreshold` terlalu rendah | 0,8–0,9; naikkan material yang memang terang |
| Tepi benda berkedip | DOF `bokehScale` besar di resolusi rendah | turunkan ke 2–3 |
| Gambar kelabu | `Noise` + `Vignette` dobel di scene gelap | pakai salah satu |
| Render video beda dari live | composer membaca waktu nyata | kunci `useFrame` ke `clock` deterministik (Remotion: `useCurrentFrame`) |

## 4. Repo ini

Halaman awal harus **< 1,5 MB** dan tanpa CDN: efek ini hanya dipakai di halaman demo 3D,
dimuat `import()` setelah interaksi pertama. Untuk foto katalog, efek lensa sudah dikerjakan
`tools/foto.py` (sheen tepi, kilau softbox) — jangan menggandakannya di browser.
