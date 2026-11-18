---
name: motion-studio
description: Pintu masuk tunggal untuk 20 repo gerak dari postingan @0xMovez — dari skill gerak, scene 3D, animasi, efek, suara, sampai encode akhir. Dipakai saat tugasnya "bikin video/animasi/3D/efek suara" dan perlu memilih alat yang tepat dulu, bukan langsung menulis kode.
license: ditulis di repo ini (bukan salinan upstream)
---

# Motion Studio — satu loop dari ide ke potongan akhir

Postingan sumber: [@0xMovez — "These 20 GitHub repos will turn your Fable 5.2 into a
premier motion studio"](https://x.com/0xMovez/status/2121312707588583455) (13 Nov 2026).
Urutan yang dipakai postingan itu sendiri: **skill → scene → motion → sound → final cut**.
Skill ini memilih alat per tahap; detail tiap alat ada di skill masing-masing.

## 1. Aturan yang mengikat seluruh alur

| Aturan | Kenapa |
| --- | --- |
| **Pilih alat sebelum menulis kode.** Satu tahap = satu alat utama. | Dua mesin animasi dalam satu bidikan menghasilkan timing yang bertengkar. |
| **Tanpa CDN.** Semua pustaka dipasang lokal, font dari `assets/fonts/`. | Aturan repo: halaman awal < 1,5 MB, tanpa permintaan ke domain luar. |
| **Aset sendiri.** Musik/SFX dari Openverse boleh, tapi lisensinya dicatat per berkas. | Jangan pernah menaruh aset pihak lain tanpa atribusi di halaman jualan. |
| **Angka dari repo, bukan dari rasa.** Durasi, fps, rasio, resolusi ditulis di awal dan diuji di akhir. | Hasil yang "kira-kira" tidak bisa dipakai dua kali. |
| **Jangan klaim hasil tanpa melihatnya.** Kalau tidak ada peramban/ffmpeg, katakan. | Repo ini sudah pernah menolak hasil yang hanya "kelihatan benar di kode". |

## 2. Peta tahap → skill

| Tahap | Pertanyaan | Skill | Alat |
| --- | --- | --- | --- |
| 0 · Skill gerak | "Bagaimana rasanya bergerak?" | [`motion-design`](../motion-design/SKILL.md) | 12 prinsip Disney, tabel timing/easing |
| 0 · Springs & audit | "Pegas CSS berapa, dan apakah geraknya benar?" | [`motion-ai-kit`](../motion-ai-kit/SKILL.md) | Motion AI Kit (`npx motion-ai`) |
| 0 · Skill video resmi | "Remotion: apa aturan resminya?" | [`remotion-skills`](../remotion-skills/SKILL.md) | 13 skill resmi Remotion |
| 1 · Scene 3D | "Objeknya di ruang 3D" | [`threejs`](../threejs/SKILL.md) | three.js |
| 1 · Fisika | "Benda harus jatuh, menabrak, berguling" | [`rapier-physics`](../rapier-physics/SKILL.md) | @react-three/rapier |
| 1 · Cahaya & lensa | "Bloom, DOF, grain, chromatic" | [`postprocessing`](../postprocessing/SKILL.md) | @react-three/postprocessing |
| 1 · Partikel | "Asap, percikan, debu, jejak" | [`quarks-vfx`](../quarks-vfx/SKILL.md) | three.quarks |
| 1 · Panel kontrol | "Saya mau memutar parameter sambil melihat" | [`tweakpane`](../tweakpane/SKILL.md) | Tweakpane |
| 1 · Blender | "Butuh mesh/adegan dari Blender" | [`blender-mcp`](../blender-mcp/SKILL.md) | Scenario Blender MCP |
| 2 · Timeline web | "Animasi DOM/SVG dengan kontrol penuh" | [`gsap`](../gsap/SKILL.md) | GSAP |
| 2 · Video React | "Video = komponen React, bisa render batch" | [`remotion`](../remotion/SKILL.md) | Remotion |
| 2 · Diagram | "Grafik/rumus harus bergerak persis" | [`manim`](../manim/SKILL.md) | Manim |
| 2 · Ikon/vektor | "Animasi ringan yang diputar di mana saja" | [`lottie`](../lottie/SKILL.md) | lottie-web |
| 2 · Figure penjelas | "Isometrik yang bisa ditunjuk dan dibongkar" | [`anatomy`](../anatomy/SKILL.md), [`anatomy-reveal`](../anatomy-reveal/SKILL.md) | Anatomy |
| 2 · Figure garis | "Satu gambar garis yang menjawab pointer" | [`hairline-create`](../hairline-create/SKILL.md), [`hairline-adopt`](../hairline-adopt/SKILL.md) | Hairline |
| 3 · Musik & SFX | "Bunyinya dari mana, lisensinya apa?" | [`openverse-audio`](../openverse-audio/SKILL.md) | Openverse API |
| 3 · Beat | "Potong di ketukan, bukan di detik bulat" | [`librosa-beat`](../librosa-beat/SKILL.md) | librosa |
| 3 · Teks waktu | "Kapan tiap kata muncul" | [`whisperx-captions`](../whisperx-captions/SKILL.md) | WhisperX |
| 4 · Encode | "Mp4 yang benar-benar bisa diputar" | [`ffmpeg-encode`](../ffmpeg-encode/SKILL.md) | FFmpeg |

## 3. Urutan kerja yang dipakai di repo ini

1. **Tetapkan spesifikasi** — rasio (9:16 / 4:5 / 1:1 / 16:9), fps, durasi, ukuran, warna
   dari token brand. Tulis di catatan, bukan di kepala.
2. **Pilih satu mesin per tahap** dari tabel di atas. Kalau butuh dua (mis. three.js untuk
   scene + Remotion untuk potongan), batasnya jelas: three.js menggambar, Remotion menyusun waktu.
3. **Bangun bidikan tunggal dulu.** Satu frame yang benar lebih berharga daripada 10 detik
   yang salah. Simpan frame itu sebagai pembanding.
4. **Uji di mesin nyata** — buka di peramban atau putar mp4-nya. Kalau tidak bisa, tulis
   "belum dilihat" di laporan.
5. **Encode sekali di akhir** dengan [`ffmpeg-encode`](../ffmpeg-encode/SKILL.md), lalu
   periksa durasi, fps, dan ukuran berkas hasil `ffprobe`.
6. **Catat** alat, versi, commit, dan lisensi yang dipakai — tabel di
   [`../README.md`](../README.md) sudah menyediakannya.

## 4. Jebakan yang sudah terbukti

- **Memasang 20 repo sekaligus.** Berat, dan sebagian tidak terpakai. Pasang yang dipakai
  tahap itu saja; repo ini mencatat perintah pasang per skill.
- **Merender video di dalam sandbox tanpa GPU.** Render per frame ke PNG lalu encode;
  WebGL di kepala tanpa peramban tidak bisa diverifikasi.
- **Font dari Google Fonts.** Dilarang di repo ini; pakai `assets/fonts/`.
- **Menaruh audio Openverse tanpa mencatat lisensi.** Setiap berkas butuh judul, pembuat,
  lisensi, dan URL sumbernya.

## 5. Batas skill ini

Skill ini **tidak** menyalin kode pustaka mana pun. Lima belas entri adalah panduan yang
ditulis di repo ini (cara pasang, API inti, jebakan); lima entri adalah salinan verbatim
skill upstream berlisensi MIT (`motion-design`, `hairline-create`, `hairline-adopt`,
`anatomy`, `anatomy-reveal`). Repo tanpa berkas lisensi (`ai-kit`, `remotion-dev/skills`)
**tidak** disalin — hanya ditautkan dan diringkas.
