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
