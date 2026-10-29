# D4 · Kreatif & Media — alur kerja & target

> **Mandat:** membuat aset visual yang layak dipakai brand kopi premium — tanpa menunggu fotografer.
> **Pemilik:** owner (merekam klip mentah) + agent (aset desain & video).
> **Waktu:** 20 menit/minggu (rekam) + 5 menit (jalankan generator).
> **Berkas kerja:** `data/kreatif.json` (manifest) · `konten/` (hasil) · `tools/kreatif.py` · `tools/brandkit.py` · `brand/`.
> **Target & KPI:** `data/divisi.json` (D4).

D4 memegang dua hal yang sering dianggap sama padahal berbeda:
**klip mentah** (dari dunia nyata, direkam owner) dan **aset jadi** (dirender dari data, oleh agent).
Yang kedua tidak menggantikan yang pertama — ia menjaga ritme saat klip mentah belum ada.

---

## 1. Alur kerja inti — dari klip mentah ke aset siap tayang

```
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

## 5. Serah terima

| Dari | Kepada | Apa |
| --- | --- | --- |
| D1 | D4 | angka batch, tanggal sangrai, skor (bahan teks video) |
| D7 | D4 | aturan klaim & izin (mana yang boleh ditampilkan) |
| D4 | D3 | aset siap + manifest + caption |
| D4 | D2 | poster/label baru untuk katalog & marketplace |

## 6. Jebakan

1. **Merender sebelum data benar.** Video "skor 81,5 ditolak" hanya boleh ada bila baris itu ada di `batch-qc.csv`.
2. **Memakai aset render seolah footage asli.** Sebut sumbernya; jangan mengarang suasana sangrai.
3. **Menyimpan video berat di repo.** Repo bukan CDN. Batasi durasi & bitrate; arsipkan selebihnya.
4. **Mengubah token brand di aset.** Palet & huruf mengikuti brief; konsistensi adalah aset itu sendiri.
5. **Menumpuk 40 aset tanpa pernah tayang.** Aset yang tidak terbit = nol, bukan setengah.
