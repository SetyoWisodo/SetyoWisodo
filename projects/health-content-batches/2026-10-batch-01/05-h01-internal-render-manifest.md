# H01 — Manifest Render Draft Internal

**Content ID:** H01 — Alveoli dan pertukaran gas<br/>
**Mode:** Draft internal, tidak untuk publikasi<br/>
**Approval scope:** Pemilik akun memilih H01 sebagai pilot dengan scene image + klip motion silent.<br/>
**Tidak termasuk:** Naskah final, voice, musik, caption final, thumbnail publik, akun platform, jadwal, atau upload.

---

## 1. Tujuan pilot

Menguji bahasa visual non-grafis untuk penjelasan alveoli sebelum asset dibuat untuk H02–H04. Pilot harus membantu Production dan PPU menilai apakah arah visual dapat menunjukkan perjalanan udara dan konsep pertukaran gas tanpa menampilkan tubuh/organ nyata atau membuat klaim kesehatan personal.

Hasil render hanya bahan evaluasi internal. Ia tidak memperoleh clearance hak komersial/output final hanya karena dibuat sebagai draft.

## 2. Batas source card yang dikunci

| Boleh divisualkan | Tidak boleh divisualkan |
|---|---|
| Jalur udara menuju alveoli; alveolus sebagai unit pertukaran gas; kedekatan alveolus dan kapiler; arah umum O₂/CO₂ sebagai konsep | Paru sehat/tidak sehat, gejala, diagnosis, penyakit, kapasitas paru, latihan napas, rokok/asap sebagai klaim kesehatan, angka klinis, terapi |
| Struktur non-fotorealistik dan label “ilustrasi edukatif” pada assembly berikutnya | Pasien, tubuh manusia nyata, darah, jaringan/organ nyata, CT/MRI, operasi, luka, jarum, klinik, dokter |

**Source-card support:** `02-source-cards.md` H01, terutama klaim yang diizinkan dan batas visual/lisensi.

---

## 3. Output yang diotorisasi

| Output | Path lokal, diabaikan Git | Status |
|---|---|---|
| Enam PNG scene vertikal | `production-drafts/health/2026-10-batch-01/H01-alveoli/images/` | Diotorisasi sebagai draft internal |
| Satu GIF motion silent beresolusi preview | `production-drafts/health/2026-10-batch-01/H01-alveoli/video/` | Diotorisasi sebagai draft internal |
| Prompt/asset manifest | Dokumen ini + asset register | Ditinjau PPU sebelum output dapat berkembang menjadi final |

PNG dan GIF tidak dipublikasikan ke Git. GIF dipakai sebagai *motion preview*, bukan video final/siap upload. Tidak ada encoder video/provider ArtCraft yang diinstal atau dipakai.

---

## 4. Style lock pilot

```text
Format: vertical 9:16
Look: non-photorealistic 3D scientific illustration + clean motion-graphic composition
Palette provisional: midnight navy, teal/cyan, lavender, warm gold for incoming air
Background: clean studio gradient with empty space for later verified overlays
Anatomy level: simplified educational diagram, never real tissue
Typography: tidak dibuat oleh generator; overlay terverifikasi ditambahkan terpisah bila diperlukan
```

### Negative constraints seluruh scene

```text
no readable generated text, labels, logos, journal figures, social-media UI, data values, or citations;
no patient, clinician, hospital scene, human suffering, or health authority figure;
no photorealistic organ or tissue, blood, wound, surgery, needle, medical scan, x-ray, or CT;
no disease, diagnosis, treatment, medication, smoking, fear bait, or before-after health claim;
no celebrity, public figure, real brand, or real social-media account.
```

---

## 5. Scene & prompt manifest

> Prompt di bawah menggunakan skill `gpt-image-2-health-visual-prompting`. Generator dipakai hanya untuk draft internal; exact model/provider dan output rights belum diberi clearance untuk penggunaan final/komersial.

| Scene | Waktu draft | Tujuan visual | Prompt render internal | Overlay terverifikasi untuk assembly berikutnya |
|---|---:|---|---|---|
| **H01-S01** | 0–2 dtk | Hero visual: mengundang pertanyaan “di mana pertukaran terjadi?” | `Vertical 9:16 non-photorealistic 3D scientific explainer illustration, a pair of simplified translucent lungs floating on a clean midnight-navy studio gradient, elegant branching airway visible inside as smooth teal tubes, camera beginning a gentle push toward one lower branch, warm gold particles only suggesting inhaled air in the airway, premium educational motion-graphic composition, centered hero subject, clean empty upper and lower space, soft cyan rim light, simplified diagram aesthetic, no text, no labels, no arrows, no realistic tissue` | Hook text dan label “ilustrasi edukatif” ditambahkan di editor, bukan generator |
| **H01-S02** | 2–10 dtk | Menunjukkan jalur udara bercabang menuju bagian yang lebih kecil | `Vertical 9:16 clean non-photorealistic 3D medical education diagram, close journey inside a smooth stylized branching airway tunnel, warm gold airflow glow travelling forward through teal airway branches toward a distant cluster of soft abstract air sacs, polished simple geometry, deep navy and cyan palette, clear central path, generous negative space, modern science animation keyframe, no text, no labels, no arrows, no blood, no real anatomy texture` | Jalur udara dan kalimat penjelasan ditambahkan terpisah |
| **H01-S03** | 10–22 dtk | Memperkenalkan alveoli sebagai kumpulan kantung kecil | `Vertical 9:16 macro non-photorealistic scientific 3D illustration of a graceful cluster of rounded abstract alveoli-like air sacs, pale lavender and cyan translucent bubble forms connected to a minimal teal airway branch, clean dark navy studio backdrop, educational diagram style rather than biological tissue, elegant depth, soft light, composition leaves room for a verified label, no text, no labels, no arrows, no blood, no photorealism` | Label “alveoli” dan “ilustrasi edukatif” ditambahkan di editor |
| **H01-S04** | 22–40 dtk | Menunjukkan kedekatan alveolus dan kapiler tanpa darah | `Vertical 9:16 non-photorealistic educational cutaway diagram, one simplified translucent air sac on the left beside a smooth abstract capillary outline on the right, separated by a very thin clear membrane-like layer, elegant cyan lavender and soft gold color palette, clean geometry, diagramatic scientific style, symmetrical readable composition, no fluid, no red blood cells, no blood, no tissue texture, no text, no labels, no arrows` | Panah arah O₂/CO₂ dan label kapiler dibuat manual berdasarkan source card |
| **H01-S05** | 40–58 dtk | Rekap perjalanan konsep dari udara menuju area pertukaran | `Vertical 9:16 premium non-photorealistic scientific explainer composition showing a single continuous visual journey from a stylized lung airway at the top through branching teal tubes into a cluster of translucent abstract air sacs at the bottom, calm midnight blue backdrop, warm gold air glow leading the eye, minimal sophisticated infographic depth, clear empty regions for verified overlay arrows, no text, no labels, no arrows, no human body, no blood, no real organ tissue` | Garis perjalanan dan batas “proses nyata lebih kompleks” ditambahkan manual |
| **H01-S06** | 58–75 dtk | Latar end/citation visual untuk source/limitation card | `Vertical 9:16 minimal non-photorealistic scientific end-card background, small elegant simplified lung and alveoli motif in the lower corner, midnight navy to deep teal gradient, refined cyan rim lighting, large clean negative space for manually typeset source and limitation card, educational premium infographic style, no text, no numbers, no logos, no real anatomy, no patient, no blood` | Citation line, DOI, dan “edukasi, bukan diagnosis” diketik manual/terverifikasi |

---

## 6. Asset register awal

| Asset ID | Scene | Jenis | Asal saat ini | Hak/provenance | Status |
|---|---|---|---|---|---|
| H01-A01-v0 | H01-S01 | AI-generated image draft | Arena image generation service | Internal evaluation only; jangan gunakan sebagai final tanpa rights review | Render draft |
| H01-A02-v0 | H01-S02 | AI-generated image draft | Arena image generation service | Internal evaluation only; jangan gunakan sebagai final tanpa rights review | Render draft |
| H01-A03-v0 | H01-S03 | AI-generated image draft | Arena image generation service | Internal evaluation only; jangan gunakan sebagai final tanpa rights review | Render draft |
| H01-A04-v0 | H01-S04 | AI-generated image draft | Arena image generation service | Internal evaluation only; jangan gunakan sebagai final tanpa rights review | Render draft |
| H01-A05-v0 | H01-S05 | AI-generated image draft | Arena image generation service | Internal evaluation only; jangan gunakan sebagai final tanpa rights review | Render draft |
| H01-A06-v0 | H01-S06 | AI-generated image draft | Arena image generation service | Internal evaluation only; jangan gunakan sebagai final tanpa rights review | Render draft |
| H01-M01-v0 | H01-S01…S06 | Silent GIF motion preview | Susunan scene image lokal | Internal evaluation only; bukan video final | Setelah assembly |

---

## 7. Motion draft plan

| Bagian | Durasi | Gerak | Larangan |
|---|---:|---|---|
| S01 | 2 dtk | Push-in halus menuju cabang paru ilustratif | Tidak ada teks/voice/sensasi |
| S02 | 5 dtk | Zoom/pan sepanjang jalur udara | Tidak membalik arah proses |
| S03 | 4 dtk | Push-in halus pada cluster alveoli abstrak | Tidak ada jaringan/blood realism |
| S04 | 5 dtk | Gerak lateral lambat untuk memperlihatkan dua struktur berdekatan | Panah/label final belum dimasukkan |
| S05 | 5 dtk | Slow pan dari jalur ke cluster alveoli | Tidak menyiratkan paru individual/penyakit |
| S06 | 4 dtk | Subtle zoom-out end-card background | Citation final belum dimasukkan |

Motion preview dibuat sebagai GIF silent dari keyframe; video final MP4 hanya dapat dibuat setelah provider/composition tool dan output rights disetujui untuk tahap berikutnya.

---

## 8. QA sebelum hasil dipresentasikan

- [ ] Tidak ada darah, jaringan/organ nyata, pasien, dokter, atau operasi.
- [ ] Semua scene terasa sebagai diagram non-fotorealistik, bukan rekaman medis.
- [ ] Tidak ada generated text, citation, angka, atau diagnosis.
- [ ] S01–S05 tidak menyiratkan terapi, paru “sehat”, gejala, atau kondisi personal.
- [ ] H01-S04 cukup jelas untuk diberi overlay arah O₂/CO₂ yang akurat kemudian.
- [ ] Tidak ada referensi terhadap jurnal figure, akun sosial, merek, atau public figure.
- [ ] File diberi status `DRAFT — NOT FOR PUBLICATION` di metadata/manifest.

## 9. Gate setelah render

1. Production melakukan visual QA dan menandai scene: keep / revise / reject.
2. Jika ada scene yang dilanjutkan, buat layer label/arrow manual dan asset-rights review untuk jalur final.
3. PPU menilai exact version yang akan dipakai di video final.
4. Tidak ada scene draft yang langsung masuk upload atau dianggap siap monetisasi.
