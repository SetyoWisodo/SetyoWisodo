---
name: blender-mcp
description: Menghubungkan agent ke Blender lewat server MCP lokal (Scenario Blender plugin) untuk membuat atau mengubah mesh, material PBR, dan adegan 3D dari perintah teks. Dipakai saat aset 3D harus lahir di Blender, bukan digambar di peramban.
license: GPL-3.0-or-later upstream · skill ini ditulis sendiri (tidak menyalin berkas GPL)
---

# Blender MCP — tim 3D di dalam Blender

| Fakta | Nilai |
| --- | --- |
| Repo | <https://github.com/scenario-labs/blender-plugin> |
| Bintang saat dicatat | 1.046 (**di bawah ambang 3.000**) |
| Lisensi | GPL-3.0-or-later (ekstensi Blender) |
| Commit yang dibaca | `885bfbabfdf8` (12 Nov 2026) |
| Isi | ekstensi Blender 5.0+ (gambar/video/3D/material PBR di viewport) + **server MCP lokal** untuk agent |
| Isi `.agents/skills` upstream | hanya skill perawatan repo (`pr-summary`, `pr-handle-comments`, `blender-download-artifacts`, `blender-knowledge-refresh`) — **bukan** skill membuat 3D |

## 1. Kapan dipakai

**Pakai** kalau butuh mesh yang rapi (produk, properti adegan), material PBR, atau bake yang
kemudian diekspor ke `.glb` untuk [`threejs`](../threejs/SKILL.md).

**Jangan** pakai kalau hasil akhirnya bisa dicapai dengan geometri parametrik (seperti
`nocturne-koffie/tools/foto.py`) — Blender menambah dependensi berat tanpa menambah mutu.

## 2. Menyambung

1. Pasang ekstensi di Blender 5.0+ (file `.zip` rilis terbaru dari repo).
2. Aktifkan **local MCP server** di panel ekstensi. Server mengikat ke loopback dan memeriksa
   `Host`/`Origin`; versi terbaru tidak memakai token untuk koneksi lokal.
3. Daftarkan di klien MCP (contoh `.mcp.json` upstream mendaftarkan server `scenario-blender`).
   Untuk layanan hosted, token dibaca dari `SCENARIO_BLENDER_TOKEN` — **jangan** simpan token di repo.
4. Uji satu perintah kecil (buat kubus, ubah material) sebelum menyuruh satu adegan penuh.

## 3. Alur kerja yang aman

```text
brief angka (dimensi mm)  →  mesh kasar  →  cek skala 1 unit = 1 m  →  material  →  ekspor .glb
```

- Simpan berkas `.blend` di luar repo (ukurannya besar); yang masuk repo hanya `.glb` final
  dan tangkapan layar bukti.
- Ekspor: `File → Export → glTF 2.0 (.glb)`, aktifkan *Apply Modifiers*, kompresi Draco hanya
  kalau dekodernya juga lokal.
- Verifikasi hasil `.glb` di penampil (Blender sendiri atau three.js), lalu catat jumlah
  segitiga: target < 60k untuk produk yang diputar di web.

## 4. Jebakan

| Gejala | Sebab | Perbaikan |
| --- | --- | --- |
| Agent tidak bisa menyambung | server belum aktif / port beda | aktifkan panel, cocokkan port di konfigurasi MCP |
| Semua perintah host ditolak | header `Origin` tidak cocok | jalankan dari klien lokal, bukan proksi |
| Model raksasa saat diimpor | satuan Blender (cm vs m) | set `Unit Scale = 1.0`, `Metric`, meter |
| Tekstur hilang di `.glb` | tekstur di luar folder ekspor | *Pack Resources* dulu, atau ekspor `gltf` + folder tekstur |
| Repo jadi berat | `.blend` ikut di-commit | simpan di luar repo, commit hanya `.glb` |

## 5. Batas jujur

Tidak ada Blender di sandbox ini, jadi skill ini **belum pernah dijalankan** di sini. Semua
langkah di atas berasal dari dokumentasi repo upstream pada commit yang tercatat; kalau
dipakai di mesin yang punya Blender, uji langkah 2 dulu dan laporkan hasilnya.
