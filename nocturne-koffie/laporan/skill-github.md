# Skill GitHub untuk landing page AI, gambar, dan huruf

**Tanggal pemeriksaan:** 5 November 2026 · **ambang:** ≥ 3.000 bintang · **sumber angka:** GitHub Search API
(`gh api search/repositories`, urut bintang) lalu metadata tiap repo (`stars`, `license`, `pushed_at`, ukuran)
dan isi pohon berkas (`git/trees?recursive=1`). Yang belum saya buka isinya saya tandai **belum diperiksa** —
tidak saya karang.

---

## 1 · Ringkasan keputusan

| Kebutuhan | Skill terpilih | Bintang | Status |
| --- | --- | --- | --- |
| Landing page kelas atas, anti-template | `nextlevelbuilder/ui-ux-pro-max-skill` + `Leonxlnx/taste-skill` | 145.433 · 110.288 | **dipakai** (aturan & data), alat pemeriksa Chromium tidak |
| Arah visual & berkas DESIGN.md | `VoltAgent/awesome-design-md` | 125.697 | **dipakai** gagasannya, berkas merek lain tidak |
| Konversi & copy halaman jual | `coreyhaines31/marketingskills` | 58.612 | **dipakai** urutan diagnosis CRO |
| Gaya gambar semua kategori | `freestylefly/awesome-gpt-image-2` | 35.482 | **dipakai** taksonomi 22 template → 20 gaya di `data/gaya-gambar.json` |
| Kata kunci gaya gambar | `willwulfken/MidJourney-Styles-and-Keywords-Reference` | 12.314 | **dibaca** sebagai rujukan kata, tidak disalin (repo tanpa lisensi) |
| Pasangan huruf | `ui-ux-pro-max` (`typography.csv` 74 pasangan, `google-fonts.csv` 1.935 keluarga) | 145.433 | **dipakai** |
| Berkas huruf & lisensi | `google/fonts` (OFL 1.1) + `fontsource/fontsource` | 20.724 · 6.263 | **dipakai** — 4 berkas woff2, 231 KB |
| Panduan huruf | `ubuwaits/beautiful-web-type` | 7.345 | dibaca sebagai kriteria penilaian |

Tiga skill baru ditulis dari hasil ini: [`skills/landing-page-ai`](../skills/landing-page-ai/SKILL.md),
[`skills/gaya-gambar`](../skills/gaya-gambar/SKILL.md), [`skills/pasangan-font`](../skills/pasangan-font/SKILL.md).

---

## 2 · Landing page & arah visual

| Repo | ★ | Lisensi | Push terakhir | Isi nyata | Keputusan |
| --- | --- | --- | --- | --- | --- |
| `nextlevelbuilder/ui-ux-pro-max-skill` | 145.433 | MIT | 2026-11-05 | 80 gaya UI (51 aktif), 192 palet produk, 74 pasangan huruf, 119 pedoman UX, 105 ikon, 25 grafik, 22 stack; data CSV + `search.py` Python tanpa dependensi | **Dipakai**: urutan prioritas 1–10 (aksesibilitas → sentuh → performa → gaya → tata letak → huruf/warna), CSV huruf. Ditolak: pemasangan plugin/CLI npm |
| `VoltAgent/awesome-design-md` | 125.697 | MIT | 2026-10-28 | 84 `DESIGN.md` hasil analisis situs nyata | **Dipakai gagasannya**: satu berkas DESIGN.md dibaca agen sebelum menulis. Berkas milik merek lain tidak dipakai |
| `Leonxlnx/taste-skill` | 110.288 | MIT | 2026-11-05 | SKILL.md 278 baris + 18 referensi (`layout-v4`, `system`, `copy`, `photos`, `effects-usage`) + 9 skrip `.mjs`; 1.648 berkas; **9 aturan rumah** | **Dipakai**: 9 aturan rumah, tabel tinggi bagian, larangan efek untuk kafe/toko, huruf 16 px minimum. Ditolak: `consistency.mjs` (butuh Chromium) |
| `nexu-io/open-design` | 106.028 | Apache-2.0 | 2026-11-05 | ruang kerja agen desain (motion, prototipe, situs) | **Ditolak**: repo 3,6 GB, butuh aplikasi + akun |
| `coreyhaines31/marketingskills` | 58.612 | MIT | 2026-11-04 | 51 skill: cro, copywriting, offers, pricing, schema, seo-audit, launch…; tiap skill punya `SKILL.md` + `references/` + `evals/` | **Dipakai**: urutan diagnosis CRO + disiplin uji. Ditolak: integrasi akun iklan/analitik |
| `VoltAgent/awesome-agent-skills` | 36.873 | MIT | 2026-11-02 | 1.000+ skill pihak ketiga | Daftar rujukan; tidak dipakai langsung |
| `op7418/guizang-ppt-skill` | 29.321 | **AGPL-3.0** | 2026-10-30 | skill dek HTML editorial/Swiss + prompt gambar | **Ditolak**: AGPL menyebar ke karya turunan; tidak sepadan untuk lembar brand internal |
| `HugoBlox/kit` | 9.786 | belum diperiksa | — | "jelaskan situs, AI membangunnya" berbasis blok Tailwind | Ditolak: menambah rantai alat |
| `Jakubantalik/transitions.dev` | 6.090 | belum diperiksa | — | 43+ transisi UI siap pakai + skill | Ditolak: gerak tambahan tanpa kebutuhan |
| `arthelokyo/astrowind` | 6.117 | belum diperiksa | — | tema Astro + Tailwind | Ditolak: proyek ini HTML/CSS tanpa build |
| `nateherkai/scroll-craft` | 4.555 | MIT | 2026-09-30 | skill situs scroll-driven | Sebagian: prinsip satu gerak per bagian |
| `cruip/open-react-template` · `cruip/tailwind-landing-page-template` | 4.717 · 4.529 | belum diperiksa | — | template landing React/Next | Ditolak: lisensi template ≠ lisensi kode; tidak dipakai |
| `ant-design/ant-design` | 100.086 | MIT | aktif | pustaka UI React | Ditolak: 100+ KB CSS, bukan halaman statis |

**Pelajaran dari tabel ini:** yang paling berguna bukan yang paling banyak bintang, melainkan yang
**menyebut angka** (tinggi bagian 708 px, ritme 4→128, 16 px minimum) karena angka bisa diperiksa.

---

## 3 · Gambar & gaya

| Repo | ★ | Lisensi | Isi nyata | Keputusan |
| --- | --- | --- | --- | --- |
| `AUTOMATIC1111/stable-diffusion-webui` | 165.249 | AGPL | antarmuka Stable Diffusion lokal | **Ditolak**: butuh GPU; sandbox ini CPU |
| `huggingface/diffusers` · `invoke-ai/InvokeAI` | 34.866 · 28.989 | Apache-2.0 · Apache-2.0 | pustaka & mesin difusi | Ditolak: tidak ada model berbobot di sini |
| `freestylefly/awesome-gpt-image-2` | 35.482 | MIT | **22 template** (product, poster, photography, illustration, 3D, character, infographic, brand, document) dengan blok *Guidance* & *Pitfalls*; 530 contoh; repo 237 MB | **Dipakai taksonominya** → `data/gaya-gambar.json` (20 gaya). Repo & gambarnya tidak disalin |
| `Evolink-AI/awesome-gpt-image-2-API-Prompts` | 17.382 | belum diperiksa | prompt + API berbayar | Dibaca; API tidak dipakai |
| `YouMind-OpenLab/awesome-nano-banana-pro-prompts` | 13.738 | belum diperiksa | 10.000+ prompt, 16 bahasa | Dibaca sebagai pembanding struktur |
| `willwulfken/MidJourney-Styles-and-Keywords-Reference` | 12.314 | **tanpa lisensi** | daftar kata gaya/medium/pencahayaan | **Dibaca saja** — tanpa lisensi tidak boleh dikutip; hanya dipakai sebagai daftar kata umum |
| `ZeroLu/awesome-nanobanana-pro` | 10.377 | belum diperiksa | prompt + hasil yang bisa dilihat | Pola "prompt tanpa contoh hasil tidak dipercaya" |
| `jamez-bondos/awesome-gpt4o-images` | 8.157 | MIT | contoh prompt + hasil | idem |
| `ai-boost/awesome-image-video-prompts` | 3.444 | belum diperiksa | prompt gambar & video | Dibaca |
| `op7418/guizang-ppt-skill` | 29.321 | AGPL-3.0 | juga memuat prompt gambar | Ditolak karena AGPL |

**Temuan penting:** semua pustaka prompt ini hanya memberi **kata**, bukan jaminan hasil. Dua percobaan
generator untuk gaya sinematik gelap di proyek ini ditolak pemilik ("jelek"). Karena itu skill
`gaya-gambar` memisahkan jalur **deterministik** (`tools/gaya.py`, Pillow) dari jalur generator, dan
menaruh pemeriksaan enam butir sebelum gambar dipasang.

---

## 4 · Huruf

| Repo | ★ | Lisensi | Isi nyata | Keputusan |
| --- | --- | --- | --- | --- |
| `google/fonts` | 20.724 | tiap berkas OFL 1.1 (repo tanpa berkas lisensi di akar) | keluarga variabel `.ttf` resmi | **Dipakai**: Bricolage Grotesque, Fraunces, Inter |
| `rsms/inter` | 20.042 | OFL-1.1 | Inter + fitur OpenType | Dipakai (lewat `google/fonts`) |
| `ubuwaits/beautiful-web-type` | 7.345 | MIT | panduan huruf sumber terbuka + contoh pasangan | Dibaca sebagai kriteria |
| `fontsource/fontsource` | 6.263 | MIT | pemaketan huruf untuk dilayani sendiri | Gagasan subset latin dipakai |
| `uswds/public-sans` · `TrionesType/zhuque` | 4.755 · 3.603 | belum diperiksa | huruf sumber terbuka | Tidak dipakai (tidak cocok dengan nada brand) |
| `JetBrains/JetBrainsMono` · `githubnext/monaspace` · `subframe7536/maple-font` | 13.149 · 19.789 · 29.661 | OFL | huruf monospace untuk kode | Tidak dipakai: situs ini tidak menampilkan kode |
| `simplefocus/FlowType.JS` | 4.551 | belum diperiksa | ukuran huruf mengikuti lebar elemen | Ditolak: dijalankan JavaScript; situs ini pakai `clamp()` |
| `arrowtype/recursive` · `github/mona-sans` · `iaolo/iA-Fonts` | 3.918 · 4.186 · 4.188 | OFL | keluarga variabel lain | Kandidat cadangan |

**Data pemilihan:** `typography.csv` (74 pasangan) memberi pola yang bisa dibaca sebagai tabel, misalnya:

| No | Nama pasangan | Judul | Badan | Suasana |
| --- | --- | --- | --- | --- |
| 1 | Classic Elegant | Playfair Display | Inter | elegan, mewah, editorial |
| 2 | Modern Professional | Poppins | Open Sans | modern, bersih, korporat |
| 3 | Tech Startup | Space Grotesk | DM Sans | teknologi, berani |

Untuk Nocturne saya tidak mengambil ketiganya: Playfair terlalu pernikahan, Poppins terlalu SaaS, Space Grotesk
terlalu startup. Yang dipakai tetap Bricolage Grotesque (grotesque rapat untuk judul) × Fraunces (serif dengan
kontras tinggi untuk motto) × Inter (badan teks) — tiga peran, kontras pada sumbu.

---

## 5 · Yang benar-benar diterapkan hari ini

| Perubahan | Angka |
| --- | --- |
| Huruf dari CDN dipindahkan ke lokal | 14 halaman · `fonts.googleapis.com` → 0 permintaan |
| Berkas huruf baru | 4 woff2 variabel · **231 KB** total |
| Bobot yang sebelumnya tidak ada | Inter 700 (dulu hanya 400–600), Bricolage 600–700 (dulu hanya 800) |
| Butir gerbang baru | **Huruf lokal** — `tools/periksa.py` naik dari 26 → **27 butir, 0 gagal** |
| Pustaka gaya gambar | `data/gaya-gambar.json` · **20 gaya**, 6 kategori, tiap gaya punya prompt + negatif + rasio |
| Skill baru | `skills/landing-page-ai`, `skills/gaya-gambar`, `skills/pasangan-font` |
| Alat baru | `tools/font.py` (bangun & periksa huruf, bisa diulang) |

---

## 6 · Yang belum diterapkan, dan kenapa

| Gagal / belum | Alasan jujur | Jalan keluarnya nanti |
| --- | --- | --- |
| `consistency.mjs` (pemeriksa tata letak `taste-skill` di peramban) | butuh Node 22 + Chromium; sandbox ini tidak punya peramban | dijalankan di mesin pemilik: `npm i` lalu `node scripts/consistency.mjs --rhythms` |
| Pustaka prompt gambar berbayar (`motionsite.ai`, `jiro.build`) | di balik akun berbayar; tidak saya lewati | tetap pakai taksonomi terbuka |
| Generator gambar untuk gaya sinematik | hasil sebelumnya ditolak pemilik | jalur Pillow `tools/gaya.py` (4 gaya) sampai ada pilihan pemilik |
| Model difusi lokal (ComfyUI/diffusers) | tidak ada GPU di sandbox | hanya bila ada mesin dengan GPU |
| Repo AGPL | lisensi menyebar ke karya turunan | hanya dibaca, tidak disalin |

---

## 7 · Catatan risiko

1. **Bintang bukan jaminan mutu.** Repo paling populer di daftar ini (`stable-diffusion-webui`, 165 ribu) sama
   sekali tidak berguna tanpa GPU. Yang menentukan adalah *apakah isinya menyebut angka yang bisa diperiksa*.
2. **Bintang bisa dibeli.** Tiga repo desain di daftar ini tumbuh > 100 ribu bintang dalam hitungan bulan —
   pola yang tidak wajar. Yang saya percaya adalah isi berkasnya, bukan angkanya.
3. **Lisensi berubah.** Repo tanpa berkas lisensi (misalnya referensi MidJourney) saya perlakukan sebagai
   "tidak boleh dipakai", bukan "boleh karena terkenal".
4. **Tautan bisa mati.** Semua pengambilan berkas tercatat di `tools/font.py` dan bisa diulang; angka di
   laporan ini berlaku pada 5 November 2026.
