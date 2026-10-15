<div align="center">

# 🧩 Audit & Integrasi Skill Image/Video untuk Divisi Produksi

### **awesome-gpt-image-2 + ArtCraft · Kanal sains kesehatan berbasis bukti**

*Audit: 15 Oktober 2026 · Status: skill workflow ditambahkan, rendering tetap terkunci sampai gate production dipenuhi*

</div>

---

## Keputusan ringkas

| Kandidat | Peran yang diterima | Status | Tidak digunakan untuk |
|---|---|---|---|
| [awesome-gpt-image-2](https://github.com/freestylefly/awesome-gpt-image-2) | Metode *prompt-as-code*, pemilihan struktur infographic/diagram, dan prompt manifest | ✅ Diintegrasikan sebagai planning skill | Engine render, sumber asset final, atau bukti hak komersial output |
| [ArtCraft](https://github.com/storytold/artcraft) | Kandidat aplikasi desktop untuk composition 2D/3D dan image-to-video draft | 🟡 Skill workflow ditambahkan; runtime **HOLD** | Instalasi sandbox, provider default, atau render tanpa model/provider clearance |

**Tidak ada** aplikasi yang diinstal, dependency yang diunduh, API key yang dimasukkan, model yang diunduh, gambar/video yang dihasilkan, atau asset upstream yang disalin.

---

## 1. Temuan `awesome-gpt-image-2`

| Area | Hasil audit |
|---|---|
| Commit yang diperiksa | `d4e4ac6` (shallow audit clone di luar repository proyek) |
| Lisensi kode/skill | MIT |
| Bentuk tool | Koleksi prompt/template dan agent skill `gpt-image-2-style-library`; bukan generator lokal mandiri |
| Kapabilitas berguna | Struktur prompt untuk infographic, scientific scale diagram, document, UI/mockup, dan layout visual |
| Generation upstream | Website/API upstream menggunakan konfigurasi layanan eksternal, termasuk `APIMART_API_KEY` dan Supabase; tidak dikonfigurasi/dipakai di proyek ini |
| Risiko komersial | Disclaimer upstream menyatakan contoh prompt/gambar komunitas dan konten pihak ketiga tidak otomatis dapat dipakai secara komersial |

### Keputusan penggunaan

Gunakan **metodologi**, bukan asset upstream:

- Boleh memakai struktur template seperti `infographic-engine` atau `scientific-scale-diagram` untuk menulis prompt baru dari source card.
- Jangan menyalin gallery image, screenshot, prompt case, logo, atau contoh komunitas sebagai asset produksi kesehatan.
- Prompt produksi harus baru, dicatat dengan Content ID/Scene ID, dan memakai batas visual kesehatan proyek ini.
- Hak penggunaan output tetap mengikuti model/provider yang benar-benar dipilih kelak, bukan lisensi MIT repository prompt.

**Skill yang ditambahkan:** [`skills/gpt-image-2-health-visual-prompting/SKILL.md`](../skills/gpt-image-2-health-visual-prompting/SKILL.md)

---

## 2. Temuan `ArtCraft`

| Area | Hasil audit |
|---|---|
| Commit yang diperiksa | `63e6176` (shallow audit clone di luar repository proyek) |
| Lisensi kode | Deklarasi package utama `MIT OR Apache-2.0`; repository memuat `LICENSE-MIT`, `LICENSE-APACHE`, dan NOTICE |
| Bentuk tool | Aplikasi desktop Rust/Tauri untuk interactive image/video crafting, 2D/3D composition, editing, dan image-to-video |
| Kapabilitas berguna | Scene blocking, layout/camera consistency, compositing, controlled image editing, dan motion draft dari scene yang telah disetujui |
| Provider/model | Dokumentasi/kode menunjukkan provider/layanan terpisah, termasuk ArtCraft/OmniGen, fal, dan Midjourney; kemampuan/terms dapat berbeda per provider dan model |
| Setup | Upstream meminta Rust, Node, npm, dan Tauri untuk development; sandbox saat ini tidak memiliki Rust/Cargo, tidak memiliki GPU, dan memori terbatas |

### Keputusan penggunaan

ArtCraft **bukan** tool yang diinstal sekarang. Ia menjadi kandidat untuk workstation pemilik akun setelah:

1. Mesin lokal/workstation ditentukan dan memenuhi kebutuhan tool/model.
2. Exact provider dan model image/video dipilih.
3. Terms penggunaan komersial, hak output, input retention, lokasi data, attribution/disclosure, biaya, serta larangan penggunaan diperiksa.
4. Pemilik akun menyetujui instalasi dan provider spesifik.
5. Scope render per batch/scene sudah disetujui.

**Skill yang ditambahkan:** [`skills/artcraft-health-production/SKILL.md`](../skills/artcraft-health-production/SKILL.md)

> Lisensi ArtCraft hanya mengatur kode aplikasi. Lisensi tersebut tidak memberi izin otomatis untuk provider, model, video output, atau input yang diunggah ke provider.

---

## 3. Skill stack Divisi Produksi

```text
Source Card + Hook + Visual Requirements
                ↓
GPT Image Health Visual Prompting Skill
(pilih struktur diagram, tulis prompt manifest, negative constraints)
                ↓
Model/provider + output rights review
                ↓
Approved generator atau ArtCraft composition workspace
                ↓
Asset register + visual QA
                ↓
Silent internal draft
                ↓
PPU → owner approval → final assembly/publish gate
```

### Pembagian tugas

| Layer | Skill/tool | Tanggung jawab |
|---|---|---|
| Prompt/scene planning | `gpt-image-2-health-visual-prompting` | Prompt baru berbasis source card, struktur infographic, negative constraints, overlay plan |
| Composition/video draft | `artcraft-health-production` | Hanya setelah aplikasi + provider diizinkan; scene blocking, layer, dan motion edukatif terbatas |
| Evidence/health safety | Source card + PPU | Memastikan mekanisme, label, dan batas klaim benar |
| Rights/provenance | Asset register + PPU | Menyimpan asal, lisensi, model/provider, prompt, asset version, dan disclosure |

---

## 4. Gerbang sebelum rendering

| Gate | Pertanyaan | Status sekarang |
|---|---|---|
| **G0 — Skill audit** | Apakah fungsi, lisensi kode, risiko upstream, dan batas tool didokumentasikan? | ✅ Selesai |
| **G1 — Scope** | Apakah pemilik akun memilih Batch/Content ID, format, dan jenis draft yang akan dirender? | 🟡 Mode **draft internal** dipilih; Content ID dan format output masih menunggu pilihan |
| **G2 — Scene authority** | Apakah scene berasal dari source card, hook, dan shot list yang disetujui? | ✅ Untuk shot list Batch 1; naskah/storyboard final tetap belum dibuat |
| **G3 — Generator/provider** | Apakah exact model/provider, hak komersial output, input retention, biaya, dan disclosure disetujui? | 🔒 Belum ada generator/provider yang cleared |
| **G4 — Generate/render** | Apakah prompt manifest, asset register, dan authorization per scene tersedia? | 🔒 Terkunci |
| **G5 — Visual QA/PPU** | Apakah output exact version lulus akurasi, non-graphic, asset-rights, dan platform checks? | 🔒 Terkunci |

---

## 5. Aturan produksi yang ditambahkan

1. Gambar AI tidak menghasilkan label ilmiah, DOI, angka, atau citation yang dianggap benar secara otomatis. Semua overlay teks dibuat dan diverifikasi di luar generator.
2. Tidak ada penggunaan photo-real patient, doctor, surgery, blood, wound, organ tissue, medical scan, journal figure, social account, atau public-figure likeness.
3. Image-to-video dipakai untuk gerak edukatif yang terkendali—zoom diagram, panah proses, layer reveal, atau rotasi 3D sederhana—bukan untuk mengarang fisiologi/hasil pengobatan.
4. Model/provider dapat berubah, tetapi setiap perubahan membutuhkan rights review dan QA ulang. Tidak ada provider/model default.
5. API key, credentials, personal reference, dan project cache bersifat privat dan tidak boleh masuk Git.
6. Semua output bersifat draft internal sampai PPU menandatangani versi file yang persis sama.

---

## 6. Langkah berikutnya setelah pemilik akun memilih scope render

1. Tetapkan Content ID awal—disarankan H01 sebagai pilot karena paling visual dan berisiko rendah.
2. Pilih format: scene image saja atau image + klip motion **silent**.
3. Buat prompt manifest dan asset register untuk enam scene; belum generate.
4. Pilih generator/provider hanya bila hak output untuk channel monetisasi jelas dan disetujui.
5. Buat output draft yang minimal, audit visual, lalu minta PPU menilai.

Tidak ada asset publik, video lengkap, narasi, musik, koneksi akun, jadwal, atau upload dalam tahap ini.

---

## Referensi internal

- [Spesifikasi Visual untuk Divisi Produksi](health-visual-production-spec.md)
- [Shot list Batch 1](health-content-batches/2026-10-batch-01/04-visual-production-requirements.md)
- [Rencana Konten Sains Kesehatan Berbasis Bukti](health-evidence-content-plan.md)
- [Skill prompt visual kesehatan](../skills/gpt-image-2-health-visual-prompting/SKILL.md)
- [Skill ArtCraft kesehatan](../skills/artcraft-health-production/SKILL.md)
