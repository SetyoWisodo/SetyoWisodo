# Skill: Open Generative AI (Anil-matcha) — prompt compiler untuk sampul buku

**Sumber:** https://github.com/Anil-matcha/Open-Generative-AI · MIT · 31.4k ★
**Diambil:** 24 Oktober 2026 · berkas yang dibaca: `README.md`, `project_knowledge.md`,
`src/lib/promptUtils.js`, `src/components/ImageStudio.js`
**Dipakai untuk:** seni sampul *Surviving the Future* / *Bertahan Hidup di Masa Depan*

---

## 1. Apa yang diambil dari repositori itu

Repositori ini bukan panduan menulis prompt, melainkan studio gambar/video yang di dalamnya
ada **prompt compiler** kecil dan bersih. Bagian yang berguna bagi buku ini ada empat:

| Komponen | Isi di repositori | Yang saya pakai |
|---|---|---|
| `buildNanoBananaPrompt()` | Menyusun prompt dari potongan: `basePrompt` + kamera + lensa + focal length + aperture + depth effect + `cinematic lighting, natural color science, high dynamic range` + tiga tag mutu | Struktur prompt sampul (lihat §3) |
| `ENHANCE_TAGS` | Empat keluarga tag: **quality** (professional photography, ultra-detailed, 8K, high dynamic range, award-winning), **lighting** (cinematic lighting, golden hour, volumetric rays, neon glow, soft diffused), **mood** (epic and dramatic, dark and mysterious, moody atmosphere), **style** (photorealistic, concept art, cyberpunk) | Kerangka tag untuk menjaga konsistensi antar-sampul |
| `CAMERA_MAP` / `LENS_MAP` / `FOCAL_PERSPECTIVE` / `APERTURE_EFFECT` | Peta istilah kamera ke frasa bahasa alami (`24` → “wide-angle dynamic perspective”, `f/4` → “balanced depth of field”) | Frasa kamera pada prompt sampul |
| Negative prompt + `QUICK_PROMPTS` | Jalur prompt negatif terpisah; pustaka prompt cepat per genre | Prompt negatif untuk menghapus teks palsu dan artefak |

## 2. Prinsip yang diadopsi

1. **Satu gambar = satu subjek utama.** Sampul harus terbaca pada 100 × 150 piksel di halaman toko.
2. **Ruang untuk tipografi direncanakan, bukan ditambahkan.** Komposisi meminta sepertiga atas
   langit gelap dan kosong; judul diletakkan di sana oleh `make_cover.py`, bukan oleh model gambar —
   model gambar menghasilkan teks yang cacat.
3. **Palet dikunci ke merek buku:** navy `#0E1A2A`, amber `#E8A33D`, putih gading `#F4F1EA`.
   Semua sampul (EN dan ID) memakai palet yang sama agar terbaca sebagai satu seri.
4. **Mood, bukan bencana.** Buku ini berargumen bahwa bencana tidak ditentukan takdir; gambar
   sampul harus menampilkan krisis **dan** kemampuan bertahan dalam satu bingkai.
5. **Tidak ada teks di dalam bitmap.** Semua huruf ditambahkan dengan Tinos/Inter di `make_cover.py`
   supaya tajam pada 300 dpi dan bisa diterjemahkan tanpa membuat ulang gambar.

## 3. Prompt final (compiled)

Struktur mengikuti `buildNanoBananaPrompt()`: kalimat adegan → kamera → lensa → focal → aperture →
lighting/color → tag mutu.

```
Epic cinematic book-cover artwork, vertical 2:3. A lone figure in a weathered rain jacket stands on
the flat roof of a stilted house above dark floodwater at dusk, back to camera, holding a lantern that
throws a warm pool of light. Behind, a half-submerged coastal megacity fades into a towering storm wall;
broken levees, mangrove roots and rooftop solar panels catch the last amber sun breaking through the
clouds. Figure low-centre, vast dramatic sky filling the upper third, deep navy near-black shadows,
single amber light source, rain-slick reflections, volumetric god rays, fine mist.
shot on a full-frame digital cinema camera, using a 24mm wide-angle lens (wide-angle dynamic
perspective), aperture f/4, balanced depth of field, cinematic lighting, natural color science,
high dynamic range, professional photography, ultra-detailed, 8K resolution, award-winning.
No text, no letters, no logos, no watermark.
```

Prompt negatif: `text, letters, watermark, logo, signature, frame, border, distorted hands,
extra limbs, oversaturated, HDR halo, plastic skin, low resolution`.

## 4. Alur produksi sampul

1. Seni mentah dihasilkan dari prompt di atas (dua kandidat, dipilih satu).
2. `make_cover.py` menambahkan judul, subjudul, nama penulis, dan garis aksen amber; hasilnya
   `*_cover_front.jpg` 1800 × 2700 (2:3, 300 dpi).
3. `make_cover.py` menyusun bungkus cetak: belakang + punggung + depan, bleed 0,125 inci,
   punggung dihitung dari jumlah halaman interior, zona barcode putih 2 × 1,2 inci.
4. Versi Indonesia memakai urutan tipografi yang sama dengan judul “BERTAHAN HIDUP DI MASA DEPAN”,
   sehingga kedua edisi tampil sebagai satu seri.

## 5. Catatan lisensi

Repositori sumber berlisensi MIT. Skill ini hanya mengadopsi **pola penyusunan prompt** (struktur
teks), bukan kode atau aset gambar; tidak ada berkas dari repositori itu yang disalin ke dalam buku.
