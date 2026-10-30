# D4 · Kreatif & Media — alur kerja & target

> **Mandat:** membuat aset visual yang layak dipakai brand kopi premium — tanpa menunggu fotografer.
> **Pemilik:** owner (merekam klip mentah) + agent (aset desain & video).
> **Waktu:** 20 menit/minggu (rekam) + 5 menit (jalankan generator).
> **Berkas kerja:** `data/kreatif.json` (manifest) · `konten/` (hasil) · `riset/brief/` (brief dari D3) · `tools/kreatif.py` · `tools/brandkit.py` · `brand/`.
> **Skill:** [`skills/social-media-riset`](../../skills/social-media-riset/SKILL.md#alur-kerja) — bagian akhirnya menghasilkan brief; brief itu yang jadi **daftar rekam** D4, bukan daftar keinginan.
> **Target & KPI:** `data/divisi.json` (D4).

D4 memegang dua hal yang sering dianggap sama padahal berbeda:
**klip mentah** (dari dunia nyata, direkam owner) dan **aset jadi** (dirender dari data, oleh agent).
Yang kedua tidak menggantikan yang pertama — ia menjaga ritme saat klip mentah belum ada.

---

## 1. Alur kerja inti — dari klip mentah ke aset siap tayang

```
[0] Brief dari riset (D3) — pola yang naik + sudut kita + aset yang diminta
        │        riset/brief/brief-NN-*.md
        ▼
[1] Produksi (D1) berjalan
        │
        ├── owner merekam 8–10 klip (30–60 detik, vertikal, tanpa wajah)
        │        └─ simpan: rekaman/<tanggal>/<nomor>.mp4
        ▼
[2] Pilih 5 klip terbaik minggu ini  → [3] Tulis hook 1 baris per klip
        │
        ▼
[4] Jalankan generator: python3 tools/kreatif.py
        │   ├─ video 9:16 (1080×1920, 24 fps, ±7 detik) → konten/reel-*.mp4
        │   ├─ poster tiap video                        → konten/reel-*-poster.jpg
        │   ├─ carousel 4:5 (1080×1350)                 → konten/carousel-*.jpg
        │   ├─ story 9:16 & feed 1:1                    → konten/story-*.jpg, post-*.jpg
        │   └─ hub pratinjau + caption                  → konten/index.html
        ▼
[5] Tulis manifest: data/kreatif.json (judul, platform, rasio, jadwal, status)
        │
        ▼
[6] Serahkan ke D3 untuk dijadwalkan & diterbitkan
        │
        ▼
[7] Setelah D3 menayangkan: ubah status di manifest → `tayang`
```

### Alat yang dipakai (dan batasnya)

| Alat | Menghasilkan | Batas yang harus diakui |
| --- | --- | --- |
| `tools/kreatif.py` | video 9:16 dari teks + label produk, poster, carousel, story, hub | **tidak** merekam dunia nyata; tidak ada footage sangrai asli |
| `tools/brandkit.py` | label 70×100 mm @300 dpi, OG image, sheet A4, logo | butuh data batch & tanggal sangrai yang benar |
| `tools/kampanye.py` | landing page kampanye dari katalog + manifest | harga & klaim ikut berkas; kalau berkas salah, halaman salah |
| `tools/riset.py` | analisis outlier, pola hook, brief konten | **tidak** mengambil data dari internet; isi CSV manual |

**Aturan jujur:** setiap video render diberi keterangan "dirender dari data", bukan "dokumentasi asli".
Kalau owner punya footage asli, footage asli **selalu menang** — render hanya jaring pengaman ritme.

### Spesifikasi teknis yang tidak boleh berubah

| Jenis | Ukuran | Rasio | Keterangan |
| --- | --- | --- | --- |
| Reel/TikTok | 1080 × 1920 | 9:16 | 24 fps, ±7 detik, teks ≥ 80 px, aman dari UI bawah |
| Carousel | 1080 × 1350 | 4:5 | maksimal 4 baris judul, body serif italik |
| Story | 1080 × 1920 | 9:16 | sisakan 250 px bawah untuk stiker |
| Feed | 1080 × 1080 | 1:1 | satu pesan, satu CTA |
| Label cetak | 827 × 1181 px | 70 × 100 mm @300 dpi | bleed 3 mm, zona aman 5 mm |

Palet & tipografi mengikuti `brand/` — **tidak** mengubah token warna/typografi brief.
Tanpa dependency CDN di aset; font lokal di `book/fonts`, semua gambar dirender lokal.

---

## 2. Ritme kerja

### Harian — 2 menit
Cek papan bagian **Kreatif & Media — aset siap tayang**: apakah ada aset berstatus `siap`
yang jadwalnya hari ini tapi belum dijadwalkan D3? Kalau ada, beri tahu D3.

### Mingguan — 40 menit
| Menit | Kegiatan | Output |
| --- | --- | --- |
| 10 | Baca brief di `riset/brief/`; pilih maksimal 3 yang asetnya bisa dikerjakan minggu ini | daftar rekam |
| 20 | Rekam 8–10 klip saat produksi/packing (tanpa menghentikan pekerjaan) | klip mentah |
| 5 | Pilih 5 klip, tulis hook 1 baris | daftar hook |
| 5 | `python3 tools/kreatif.py` → render aset | `konten/*` + manifest |
| 5 | `python3 tools/kampanye.py` bila harga/aset berubah | `kampanye/index.html` |
| 5 | Periksa 3 aset secara visual (jangan asal unggah) | aset disetujui |

### Bulanan — 45 menit
1. Hitung aset siap vs terpakai: kalau > 40% tidak terpakai, produksi terlalu banyak — kurangi.
2. Arsipkan klip mentah > 60 hari ke luar repo (jangan menambah bobot Git).
3. Perbarui label bila harga atau kode batch berubah (`brandkit.py`).
4. Cek ukuran folder `konten/`: target < 12 MB untuk seluruh aset yang di-commit.

---

## 3. Target kerja 3 bulan

Dari `data/divisi.json` → D4.

| Ukuran | Nov 2026 | Des 2026 | Jan 2027 | Cara hitung | Arah |
| --- | --- | --- | --- | --- | --- |
| Video jadi | 8 | 12 | 16 | item `format:"video"` di `data/kreatif.json` | naik |
| Carousel jadi | 4 | 6 | 8 | item `id` berawalan `carousel` | naik |
| Aset siap tayang | 12 | 18 | 24 | seluruh item manifest | naik |
| Klip mentah / bulan | 30 | 40 | 50 | dihitung manual saat merekam, dicatat mingguan | naik |
| Brief dari riset | 4 | 8 | 12 | item `brief` di `riset/data.json` | naik |

Pendukung: aset baru per minggu 3 → 4 → 5; waktu produksi 1 video ≤ 45 → 30 → 25 menit.
"Klip mentah" belum punya berkas pencatat — sampai ada, isinya tampil sebagai **tanpa data** di papan
(itu jujur, bukan bug). Bila ingin diisi: tambahkan kolom `klip_mentah` di `data/kpi.csv`.

---

## 4. Definisi selesai

| Rentang | Selesai bila… |
| --- | --- |
| Satu aset | file ada, ukuran sesuai spesifikasi, ada di manifest dengan status `siap` |
| Satu minggu | minimal 3 aset baru; manifest diperbarui; tidak ada aset tanpa judul |
| Satu bulan | video & carousel mencapai target; folder `konten/` < 12 MB |
| Satu kampanye | aset kampanye + landing page sinkron dengan harga katalog |

## 4b. Memakai brief riset (jangan mengarang arah sendiri)

`tools/riset.py` menulis `riset/brief/brief-NN-*.md`. Tiap brief memuat pola yang naik, sudut
untuk Nocturne, hook versi kita, aset yang dipakai, bukti yang wajib tampil, dan larangan.

| Langkah | Aturan |
| --- | --- |
| Pilih brief | maksimal 3 per minggu; utamakan yang asetnya sudah `siap` di manifest |
| Ubah jadi shot list | 3–5 klip per brief; tulis di kertas sebelum merekam |
| Aset baru | tambah ke `data/kreatif.json` dengan judul, platform, rasio, jadwal, status `siap` |
| Brief selesai | tandai `dipakai` di `riset/data.json` lewat `tools/riset.py` berikutnya; hapus berkasnya dari `riset/brief/` bila sudah usang |
| Tidak pakai brief | tulis alasannya satu baris — "tidak cocok karena X" |

**Jangan** mengambil hook, footage, audio, atau desain milik akun yang dianalisis. Yang diambil pola.
Angka yang tampil di konten harus berasal dari `batch-qc.csv`, `catalog.json`, atau `pesanan.csv`.

## 4c. Skrip 9 detik dari studio

`tools/studio.py` menulis 5 skrip ke `studio/skrip/`. Bedanya dengan brief: brief memberi **arah**,
skrip memberi **teks per detik** yang sudah lolos cek suara.

| Bagian | Isi | Durasi |
| --- | --- | ---: |
| Hook | satu kalimat dari `data/studio-hooks.csv` | 3 detik |
| Bukti 1 | angka/tanggal dari `batch-qc.csv` atau `catalog.json` | 2 detik |
| Bukti 2 | akibat atau perbandingan yang bisa dicek | 2 detik |
| CTA | WhatsApp + sebut metode seduh & kota | 2 detik |

Yang **tidak** boleh diubah saat merekam:

1. **Teks hook** — sudah dipilih berdasarkan lift median dan aset yang tersedia.
2. **Angka** — kalau angkanya berubah (batch baru), jalankan ulang `studio.py`; jangan diedit tangan.
3. **Sumber klaim** — baris `Sumber data` di tiap skrip wajib tetap ada saat review D7.

Yang **boleh** diubah: shot list, urutan pengambilan, pencahayaan, dan bunyi ruangan.
Setelah direkam, ubah `status` hook di `data/studio-hooks.csv` menjadi `dipakai`.

## 4d. Gerak & landing page (skill `motion-web`)

Tujuh repo desain dari post `@thegreatest_sv` (29 Okt 2026) dipakai sebagai **aturan + komponen**,
bukan library tambahan. Playbooknya `skills/motion-web/SKILL.md`; mesinnya `tools/motion.py`
dan `tools/slop.py`.

| Yang dipakai | Berkas | Untuk apa |
| --- | --- | --- |
| kontrak token | `data/design-system.json` | sumber warna/radius/ukuran/easing; audit memeriksa CSS terhadapnya |
| komponen gerak | `assets/js/motion-ui.js` + `assets/css/motion-ui.css` | spotlight, count-up, magnet, teks per kata, pin, bilah kemajuan |
| adegan 9:16 | `motion/frame-01..05.html` + `motion/timeline.json` | dari 5 skrip studio, siap direkam |
| audit anti-slop | `tools/slop.py` → `laporan/slop.md` | 29 aturan: slop, kualitas, gerak, kontrak desain |

Aturan kerja:

1. **Satu ide gerak per bagian.** Hero boleh punya teks per kata; bagian lain cukup reveal.
2. **Hanya transform/opacity.** Kalau butuh lebar/tinggi berubah, itu bukan animasi — itu layout.
3. **Reduced-motion mematikan semua gerak**, isi tetap terbaca.
4. **Kritis harus nol** sebelum aset jadi. Perhatian diputuskan, bukan diabaikan.
5. **Adegan HTML bukan video.** Rekam layar 1080×1920 atau render ffmpeg di mesin yang punya ffmpeg;
   sandbox ini tidak punya encoder dan tidak diklaim punya.
6. **Tidak ada Figma, Blender, atau GSAP** di lingkungan ini. Jangan menulis "sudah diimpor dari Figma".

## 4e. Panggung 3D (landing page gaya galeri award)

Post `@viktoroddy` (30 Okt 2026) mengumpulkan galeri desain: motionsites, land-book, landdding,
recent.design, 60fps, dan galeri award websites. Ciri yang diambil: **perspective, objek berlapis
di kedalaman berbeda, lantai berpetak, kamera yang bergerak halus.** Bukan WebGL, bukan three.js.

| Komponen | Berkas | Dipakai di |
| --- | --- | --- |
| panggung hero (3 kartu di 3 kedalaman + chip data) | `assets/css/motion-3d.css`, `assets/js/motion-3d.js` | `kampanye/index.html` hero |
| silinder klip (5 pane, 72° per langkah) | idem | galeri klip kampanye |
| kartu timbul (tilt 8°) | idem | 3 kartu produk di kampanye |

Aturan kerja:

1. **Satu panggung per halaman.** Hero saja. Bagian lain tetap datar.
2. **Kedalaman = hierarki.** Angka terpenting paling dekat kamera; penjelas di belakang.
3. **Hanya `transform` & `opacity`.** Tanpa `filter: blur` di lapisan bergerak.
4. **Jatuh datar wajib:** tanpa JS, di bawah 900 px, dan saat reduced-motion, semuanya datar dan
   terbaca. Korsel berubah menjadi grid.
5. **Angka di kartu harus berasal dari data**, bukan angka baru: 3 hal, 7–21 hari, ambang QC 83.
6. **Objek 3D bukan foto produk.** Ini ilustrasi CSS; label cetak tetap di `brand/`, jangan
   mengklaim panggung ini sebagai mockup kemasan final.

Gerbang: `python3 tools/periksa.py` punya cek **Panggung 3D** (berkas, gating, jatuh datar,
anggaran ≤ 24 KB).

## 4f. Lembar film: dari skrip ke frame (skill `motion-film`)

Post `@Mikadzyki_NFT` (28 Okt 2026) mengumpulkan 20 repo motion. Yang diambil hukum
produksinya, bukan library-nya: **durasi = bobot, arc energi, sinkron ketukan, larangan
angka karangan**. Mesinnya `tools/film.py`; playbooknya `skills/motion-film/SKILL.md`.

| Hasil | Berkas | Isi |
| --- | --- | --- |
| Lembar film | `motion/film-sheet.md` | cue → frame → ketukan → tier energi → kamera → SFX |
| Data mesin | `motion/film-sheet.json` | dipakai `tools/periksa.py` (cek "Film gerak") |
| Grid | 120 BPM · 60 fps | 1 ketukan 30 frame · 1 birama 120 frame · 9 s = 540 frame |

Aturan kerja:

1. **120 BPM bukan selera.** Batas cue studio (3/5/7 s) jatuh tepat di ketukan 6/10/14.
   Tempo lain membuat gerak berhenti "nyaris" pas.
2. **Arc energi per adegan:** `cold-open` — tier 4 / 2 / 3 / 5. Lembah di cue 2 wajib;
   tanpa lembah, payoff tidak terasa naik.
3. **Empat still sebelum render penuh** (`?t=0.5`, `3.2`, `5.2`, `7.2`). Yang gagal baca
   diperbaiki di still, bukan setelah render 540 frame.
4. **Cue yang memuat angka wajib menyebut sumber** (`data/`); cue CTA tanpa angka boleh kosong.
5. **Tanpa browser/ffmpeg, jangan klaim video jadi.** Rekam layar atau serahkan lembar ini
   ke mesin yang punya keduanya.

## 4g. Mesin film: empat pustaka, satu klip jadi (30 Okt 2026)

Divisi kreatif tidak lagi bergantung pada "nanti kalau ada tools". Empat mesin motion sudah
terpasang di `film-studio/` lewat npm, dengan versi dipin dan skrip yang bisa dijalankan ulang.

| Mesin | Versi | Status nyata | Dipakai untuk |
| --- | --- | --- | --- |
| GSAP + ScrollTrigger | 3.15.0 | jalan penuh, diuji | timeline ketukan di `/motion/` + komposisi HyperFrames |
| Lottie (lottie-web) | 5.13.0 | jalan penuh, diuji | pemutar 9 detik di `/motion/` |
| Remotion | 4.0.539 | bundel lolos, render **tidak** | komposisi React 4 cue, menunggu mesin ber-Chrome |
| HyperFrames | 0.8.221 | lint 0/0, render **tidak** | root + 4 sub-komposisi, menunggu mesin ber-Chrome |

**Untuk produksi harian sekarang, perender yang dipakai adalah `python3 tools/render_film.py`**
— 540 frame PNG dari lembar film + font brand asli, dienkode ffmpeg ke H.264 1080×1920/60 fps.
Keluaran terakhir: `motion/out/klip-01-nocturne-9s.mp4` (341 KB, 9,00 s) dengan
`motion/out/manifest.json` (sha256, encoder, sumber angka).

Aturan yang mengikat divisi:

1. **Jangan klaim output Remotion/HyperFrames** selama yang ada di `motion/out/` adalah keluaran
   `render_film.py`. Dua mesin itu baru dipakai saat render di mesin ber-Chrome.
2. **Angka dari `motion/film-sheet.json`.** Tidak ada durasi yang diketik ulang di JSX/HTML.
3. **Tanpa CDN** untuk pustaka JS; semuanya di `assets/vendor/` dengan lisensi tercatat.
4. **Halaman awal tidak boleh menyentuh pustaka mesin.** Dimuat malas di `/motion/` saja.
5. **QC visual wajib sebelum tayang:** `python3 tools/render_film.py --still 90` lalu periksa
   frame; jangan menilai dari kode.
6. **Lisensi Remotion** gratis untuk ≤ 3 orang; lebih dari itu perlu lisensi berbayar sebelum
   dipakai komersial (`laporan/mesin.md` §5).

Laporan lengkap: `laporan/mesin.md`. Proyek mesinnya: `film-studio/README.md`.

## 5. Serah terima

| Dari | Kepada | Apa |
| --- | --- | --- |
| D1 | D4 | angka batch, tanggal sangrai, skor (bahan teks video) |
| D7 | D4 | aturan klaim & izin (mana yang boleh ditampilkan) |
| D4 | D3 | aset siap + manifest + caption |
| D3 (riset) | D4 | brief: pola, sudut, aset yang harus dibuat |
| D4 | D2 | poster/label baru untuk katalog & marketplace |

## 6. Jebakan

1. **Merender sebelum data benar.** Video "skor 81,5 ditolak" hanya boleh ada bila baris itu ada di `batch-qc.csv`.
2. **Memakai aset render seolah footage asli.** Sebut sumbernya; jangan mengarang suasana sangrai.
3. **Menyimpan video berat di repo.** Repo bukan CDN. Batasi durasi & bitrate; arsipkan selebihnya.
4. **Mengubah token brand di aset.** Palet & huruf mengikuti brief; konsistensi adalah aset itu sendiri.
5. **Menumpuk 40 aset tanpa pernah tayang.** Aset yang tidak terbit = nol, bukan setengah.
6. **Merekam tanpa brief.** Rekaman tanpa arah menghasilkan 10 klip yang tidak dipakai minggu mana pun.
7. **Menyalin gaya visual akun lain.** Yang boleh dipelajari adalah pola hook & format; identitas visual kita tetap milik brief.
