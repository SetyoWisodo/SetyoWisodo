---
name: remotion-skills
description: Indeks 13 skill resmi Remotion (create, captions, maps, markup, render, studio, license, dan lainnya) dengan urutan pemakaian dan tautan berkasnya. Dipakai saat mulai proyek video Remotion supaya tidak menulis ulang aturan resmi dari nol.
license: repo upstream TIDAK punya berkas lisensi → skill ini indeks + ringkasan, bukan salinan
---

# Remotion Skills — 13 skill resmi

| Fakta | Nilai |
| --- | --- |
| Repo | <https://github.com/remotion-dev/skills> |
| Bintang saat dicatat | 7.456 |
| Lisensi | **tidak ada `LICENSE` di repo** — isi tidak disalin, hanya diindeks |
| Commit yang dibaca | `3e20ac75161b` (16 Nov 2026) |
| Bentuk | 13 folder skill di `skills/<nama>/SKILL.md` |

## 1. Daftar dan kapan dipakai

| Skill upstream | Dipakai saat |
| --- | --- |
| `remotion-best-practices` | Pintu masuk: aturan dasar frame-based rendering, animasi, aset |
| `remotion-create` | Mulai proyek baru; layout video; Tailwind |
| `remotion-captions` | Subtitle: impor SRT, transkripsi, tampilan caption |
| `remotion-render` | Render batch, concurrency, codec, target platform |
| `remotion-studio` | Memakai Remotion Studio untuk menyetel |
| `remotion-multimedia` | Video/audio di dalam video, pemotongan, volume |
| `remotion-maps` | Peta dan geografi (Mapbox/MapLibre) |
| `remotion-markup` | Teks kaya: markdown, highlight kode |
| `remotion-interactivity` | Player di dalam aplikasi, kontrol waktu |
| `remotion-saas` | Render sebagai layanan (queue, storage, biaya) |
| `remotion-docs` | Merujuk dokumentasi resmi dengan benar |
| `remotion-license` | Batas lisensi Remotion per ukuran perusahaan |
| `remotion-upgrade` | Naik versi tanpa merusak komposisi |

## 2. Urutan yang masuk akal di repo ini

1. `remotion-license` **dulu** — pastikan pemakaiannya diizinkan sebelum menulis kode.
2. `remotion-best-practices` + `remotion-create` untuk kerangka.
3. `remotion-captions` bila ada narasi (bahan dari [`whisperx-captions`](../whisperx-captions/SKILL.md)).
4. `remotion-render` untuk keluaran; encode akhir tetap di [`ffmpeg-encode`](../ffmpeg-encode/SKILL.md).

## 3. Aturan yang sering dilanggar

- **Semua gerak harus fungsi dari `frame`.** `Date.now()`, `Math.random()`, dan animasi CSS
  berbasis waktu nyata membuat render tidak bisa diulang.
- **Aset lokal.** Font dan gambar di `public/`; tanpa CDN.
- **Ukuran komposisi = ukuran keluaran.** Jangan merender 1080×1920 lalu memotong dengan FFmpeg
  kalau bisa langsung menata untuk 9:16.
- **Kunci versi.** `remotion` dan `@remotion/cli` harus versi sama.

## 4. Kenapa tidak disalin

Upstream tidak menyertakan berkas lisensi, jadi salinan verbatim tidak boleh ditaruh di repo
ini. Yang diambil: nama, urutan, dan aturan penting yang ditulis ulang. Tautan langsung:
`https://github.com/remotion-dev/skills/tree/main/skills`.
