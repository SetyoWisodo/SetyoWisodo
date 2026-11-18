---
name: motion-ai-kit
description: Memakai Motion AI Kit (motiondivision/ai-kit) untuk memilih pegas CSS, menerjemahkan gerak desain ke parameter, dan mengaudit performa animasi di halaman. Dipakai saat gerak UI harus terasa benar dan terukur, bukan sekadar "halus".
license: repo upstream TIDAK punya berkas lisensi → skill ini ditulis sendiri, upstream hanya ditautkan
---

# Motion AI Kit — pegas, audit, dan kosakata gerak

| Fakta | Nilai |
| --- | --- |
| Repo | <https://github.com/motiondivision/ai-kit> |
| Bintang saat dicatat | 123 (**di bawah ambang 3.000**) |
| Lisensi | **tidak ada `LICENSE` di repo** — karena itu isi skill ini tidak disalin, hanya ditautkan |
| Commit yang dibaca | `1e424943582c` (26 Okt 2026) |
| Isi upstream | plugin Cursor + `plugins/motion/skills/motion/` (`css-spring/`, `performance-audit/`, `transition-preview/`, `best-practices/`, `insert/`, `codex/`) |
| Pasang | `npx motion-ai` (memasang server MCP Motion); varian `--plus` hanya untuk anggota |

## 1. Kapan dipakai

**Pakai** saat pertanyaannya berbentuk: "pegas CSS yang pas untuk ini berapa?", "kenapa
animasi ini tersendat di ponsel?", "ubah gerak ini dari easing linear ke spring".

**Jangan** pakai sebagai mesin animasi: ini kumpulan aturan + server MCP, bukan pustaka runtime.

## 2. Terjemahan angka: easing vs spring

| Kebutuhan | Setelan |
| --- | --- |
| Elemen masuk, ringan | `cubic-bezier(0.22, 1, 0.36, 1)` (ease-out kuat), 180–260 ms |
| Keluar | `cubic-bezier(0.4, 0, 1, 1)`, 120–180 ms (keluar lebih cepat dari masuk) |
| Ada massa/berat | spring: `stiffness 180–260`, `damping 22–30`, `mass 1` |
| Pegas tanpa "memantul" | `damping ≥ 2·√stiffness·mass` (kritis) |
| Gerak berantai (daftar) | stagger 40–70 ms, jangan > 100 ms |

Aturan yang selalu berlaku: **jangan** memulai animasi dari `opacity: 1` laten; set state
awal di CSS. **Jangan** menganimasikan properti layout (`top`, `width`, `left`).

## 3. Audit performa — daftar periksa

1. Buka Performance panel, rekam 3 detik animasi, cari *long task* > 50 ms.
2. Pastikan hanya `transform` dan `opacity` yang berubah; kalau ada `filter: blur` besar,
   turunkan radius atau pindahkan ke gambar.
3. Cek layer: `will-change` hanya pada elemen yang benar-benar beranimasi, dilepas setelahnya.
4. Hormati `prefers-reduced-motion: reduce` → ganti gerak dengan perubahan warna.
5. Ukur di perangkat kelas bawah atau throttle CPU 4×.

## 4. Kenapa tidak disalin

Repo ini hanya menyalin skill upstream yang punya berkas lisensi (MIT). `ai-kit` tidak punya,
jadi yang diambil adalah **tautannya** dan ringkasan aturan yang ditulis ulang di sini.
Kalau kelak upstream menambahkan lisensi, skill ini bisa diganti dengan salinan verbatim.
