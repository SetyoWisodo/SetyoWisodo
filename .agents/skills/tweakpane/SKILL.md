---
name: tweakpane
description: Panel kontrol ringan untuk menyetel parameter scene, shader, atau animasi secara langsung pakai Tweakpane — binding angka, warna, pilihan, tombol, dan penyimpanan preset. Dipakai saat angka harus dicari dengan mata, bukan dengan menebak lalu render ulang.
license: MIT · cocopon/tweakpane · commit 50a18c3dba67
---

# Tweakpane — menyetel sambil melihat

| Fakta | Nilai |
| --- | --- |
| Repo | <https://github.com/cocopon/tweakpane> |
| Bintang saat dicatat | 4.703 |
| Lisensi | MIT |
| Commit yang dibaca | `50a18c3dba67` |
| Pasang | `npm i tweakpane` |

## 1. Kapan dipakai

**Pakai** saat mencari angka: sudut kamera, kekuatan cahaya, radius blur, easing, warna
material. Panel ini mengubah variabel hidup — hasilnya terlihat seketika, tanpa render ulang.

**Jangan** pakai sebagai UI produk. Tweakpane adalah alat dapur; keluarkan angka final ke
kode/dataset sebelum dikirim ke pembeli.

## 2. Kerangka minimum (v4)

```js
import { Pane } from 'tweakpane';

const pane = new Pane({ container: document.getElementById('panel'), title: 'Kamera' });

pane.addBinding(param, 'yaw', { min: -60, max: 60, step: 1, label: 'yaw' });
pane.addBinding(param, 'intensitas', { min: 0, max: 3, step: 0.01 });
pane.addBinding(param, 'warna', { view: 'color' });
pane.addBinding(param, 'preset', { options: { Rapat: 0.8, Longgar: 1.4 } });
pane.addButton({ title: 'Simpan' }).on('click', () => console.log(JSON.stringify(param)));

pane.on('change', () => terapkan(param));   // jangan panggil render di dalam onChange berulang
```

API v4 memakai `addBinding`; contoh lama di internet masih `addInput` (v3) — jangan dicampur.

## 3. Jebakan

| Gejala | Sebab | Perbaikan |
| --- | --- | --- |
| Panel tidak muncul | CSS Tweakpane tidak diimpor | `import 'tweakpane/dist/tweakpane.css'` (atau tema sendiri) |
| `addInput is not a function` | mengikuti contoh v3 | ganti ke `addBinding` |
| Perubahan tidak terlihat | objek di-clone ke dalam fungsi, bukan referensi | binding harus ke objek yang sama dengan yang dibaca render |
| Panel ikut ter-screenshot | panel di dalam kanvas/DOM yang direkam | pindahkan panel ke luar elemen target, atau sembunyikan saat render |
| Berat di halaman | dimuat di atas fold | muat dinamis, hanya di halaman lab |

## 4. Repo ini

Lab gerak (`motion/`) dan halaman demo 3D boleh memakai panel ini selama dimuat setelah
interaksi. Angka yang sudah disetujui dicatat di `data/` atau konstanta alat render —
bukan dibiarkan hidup di localStorage.
