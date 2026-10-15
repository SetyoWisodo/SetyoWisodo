# H01 — Internal Draft Visual QA

**Content ID:** H01 — Alveoli dan pertukaran gas<br/>
**Versi yang diperiksa:** `H01-A01-v0` s.d. `H01-A06-v0` dan `H01-M01-v0`<br/>
**Mode:** Draft internal, bukan PPU final dan bukan izin publikasi<br/>
**Tanggal:** 15 Oktober 2026

---

## Material yang diperiksa

| Asset | File lokal (diabaikan Git) | Bentuk | Hasil awal |
|---|---|---|---|
| H01-A01-v0 | `images/H01-S01-hero-lungs-v0.png` | Hero paru ilustratif | ✅ Keep untuk draft |
| H01-A02-v0 | `images/H01-S02-airway-journey-v0.png` | Perjalanan jalur udara | ✅ Keep untuk draft |
| H01-A03-v0 | `images/H01-S03-alveoli-cluster-v0.png` | Cluster alveoli abstrak | ✅ Keep untuk draft |
| H01-A04-v0 | `images/H01-S04-air-blood-barrier-v0.png` | Kedekatan alveolus–outline kapiler | 🟡 Revise sebelum final |
| H01-A05-v0 | `images/H01-S05-pathway-recap-v0.png` | Rekap jalur ke alveoli | ✅ Keep untuk draft |
| H01-A06-v0 | `images/H01-S06-end-card-bg-v0.png` | Latar citation/end card | ✅ Keep untuk draft |
| H01-M01-v0 | `video/H01-alveoli-silent-motion-preview-v0.gif` | GIF silent, 18 frame, 540×960 | ✅ Keep sebagai preview internal |

> Semua path berada di bawah `production-drafts/health/2026-10-batch-01/H01-alveoli/`; folder tersebut sengaja diabaikan Git.

---

## Hasil pemeriksaan visual awal

| Kriteria | Hasil | Catatan |
|---|---|---|
| Non-grafis | ✅ PASS | Tidak ada pasien, tubuh nyata, darah, luka, operasi, scan, atau jaringan fotorealistik. |
| Tidak ada teks/angka buatan generator | ✅ PASS | Semua scene bebas dari citation, diagnosis, label, angka, dan logo hasil generator. |
| Konsistensi visual | ✅ PASS | Palet navy–teal–lavender dan bentuk diagram konsisten untuk pilot H01. |
| Source-card boundary | ✅ PASS bersyarat | Tidak ada penyakit, gejala, terapi, rokok/asap, klaim paru personal, atau angka klinis. |
| Jalur udara → alveoli | ✅ PASS untuk draft | S01, S02, S03, dan S05 cukup menunjukkan transisi konseptual; narasi/label final belum diuji. |
| Pertukaran gas | 🟡 REVISE | S04 hanya boleh dipakai sebagai background. Tambahkan panah O₂ dan CO₂ serta label alveolus/kapiler secara manual, lalu verifikasi arahnya terhadap source card. Jangan gunakan visual ini sendirian untuk mengajar pertukaran gas. |
| End/source card | ✅ PASS untuk background | S06 menyediakan ruang untuk citation dan limitation card yang akan diketik manual/terverifikasi. |
| Motion preview | ✅ PASS untuk ritme internal | GIF hanya memakai pan/zoom ringan pada keyframe. Tidak memiliki audio, caption final, atau gerak fisiologis buatan yang dapat menambah klaim. |
| Hak output final | 🔒 HOLD | Asset dibuat untuk evaluasi internal. Tidak ada clearance hak komersial/final provider-model yang dicatat untuk penggunaan publik. |

---

## Keputusan internal

**Status visual language:** `CONDITIONALLY KEEP — INTERNAL DRAFT ONLY`

Pilot menunjukkan bahwa arah 3D non-fotorealistik cocok untuk H01. Namun tidak ada file yang boleh masuk naskah/video publik atau dianggap PPU PASS.

### Revisi wajib sebelum assembly video final

1. Buat overlay manual: panah O₂ dari alveolus menuju kapiler dan panah CO₂ dari kapiler menuju alveolus.
2. Tambahkan label terverifikasi untuk `alveoli`, `kapiler`, dan batas “ilustrasi edukatif”; jangan memakai tulisan yang digenerate model.
3. Ketik source line/DOI serta “edukasi, bukan diagnosis” pada S06 melalui editor biasa.
4. Review ulang susunan scene bersama naskah final agar tiap visual memenuhi hook dan tidak menyederhanakan mekanisme secara menyesatkan.
5. Selesaikan review rights/model/provider sebelum asset diangkat dari draft internal menuju asset produksi final.
6. Ajukan versi final yang persis sama ke PPU.

### Yang tetap tidak diizinkan

- Menambah voice, musik, subtitle final, thumbnail publik, akun platform, jadwal, atau upload.
- Menggunakan output ini sebagai klaim tentang kesehatan paru penonton.
- Mengganti generator/model atau mengedit anatomy tanpa asset-register update dan QA ulang.

---

## Handoff berikutnya

```text
Internal draft visual QA
        ↓ conditionally keep
Naskah final + overlay terverifikasi + rights review
        ↓
Visual QA ulang
        ↓
PPU pada exact final file
        ↓ PASS + approval pemilik akun
Assembly/publish gate yang terpisah
```
