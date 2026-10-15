# Batch 1 — Visual Production Requirements

**Status:** 🟡 Perencanaan visual Divisi Produksi. Tidak ada gambar, asset berbayar, image generation, render, atau upload yang dibuat/diizinkan oleh dokumen ini.

## Tujuan

Menerjemahkan source card dan hook Batch 1 menjadi kebutuhan scene yang dapat diperiksa sebelum produksi. Setiap scene harus membantu menjawab janji hook dan tidak menambah klaim kesehatan baru.

**Standar global:** lihat [Spesifikasi Visual untuk Divisi Produksi](../../health-visual-production-spec.md).

---

## Ringkasan kebutuhan batch

| Content ID | Hook rekomendasi | Estimasi scene | Hero visual | Estimasi asset unik | Risiko visual utama |
|---|---|---:|---|---:|---|
| H01 | “Oksigen yang kamu hirup tidak langsung masuk ke darah.” | 6 | Paru ilustratif menuju alveoli | 8–10 | Jangan memakai darah/organ nyata atau klaim kesehatan paru personal |
| H02 | “Mengapa cahaya bisa memberi sinyal waktu kepada tubuh?” | 6 | Cahaya → mata → jalur sinyal → SCN | 8–10 | Jangan menjadi tips/terapi tidur atau menampilkan otak nyata |
| H03 | “Satu jurnal bisa menarik. Tapi apakah satu jurnal cukup untuk sebuah klaim kesehatan?” | 6 | Satu kartu studi → beberapa studi → review | 8–10 | Jangan memakai figure jurnal atau menganggap meta-analysis selalu unggul |
| H04 | “Sebelum percaya klaim kesehatan viral, jangan mulai dari views-nya—mulai dari sumbernya.” | 6 | Angka views berubah ke ikon sumber | 8–10 | Gunakan mockup fiktif; jangan menyerang kreator/produk nyata |

**Shared asset awal:** citation bar, source/limitation card, end card/CTA, caption style, lower-third label, dan template scene “ilustrasi edukatif”. Semua tetap harus memiliki asset ID dan status review.

---

## H01 — Alveoli dan pertukaran gas

**Source-card boundary:** anatomi/fisiologi umum saja. Tidak membahas penyakit, kapasitas paru, latihan napas, atau “membersihkan paru-paru”.

| Scene | Waktu indikatif | Kebutuhan gambar/animasi | Teks/label yang diizinkan | QA khusus |
|---|---:|---|---|---|
| H01-S01 | 0–2 dtk | Hero: paru ilustratif non-fotorealistik; kamera bergerak mendekat ke jalur udara | “Oksigen tidak langsung masuk ke darah” | Tidak ada tubuh/pasien nyata; hook harus terjawab kemudian |
| H01-S02 | 2–10 dtk | Diagram jalur udara sederhana: hidung/mulut → saluran napas → cabang kecil | “Udara bergerak makin jauh ke dalam paru” | Jangan menyebut angka atau fungsi klinis tambahan |
| H01-S03 | 10–22 dtk | Kumpulan alveoli 3D sederhana, seperti kantung kecil berlabel | “Alveoli” · “unit pertukaran gas” | Bentuk diberi label sebagai ilustrasi edukatif |
| H01-S04 | 22–40 dtk | Potongan diagram alveolus di samping outline kapiler; panah O₂ dan CO₂ bergerak berlawanan | “O₂ menuju darah” · “CO₂ menuju udara” | Gunakan garis/panah, bukan darah atau jaringan nyata; arah wajib benar |
| H01-S05 | 40–58 dtk | Rekap jalur visual: udara → alveoli → penghalang udara-darah | “Proses nyata lebih kompleks dari ilustrasi ini” | Jangan berubah menjadi evaluasi “paru sehat” |
| H01-S06 | 58–75 dtk | Citation/limitation card dengan paru ilustratif kecil sebagai elemen latar | Sumber + “edukasi, bukan diagnosis” | DOI/source line terbaca dan tidak menutupi disclaimer |

### Paket asset H01

- `H01-A01` paru/percabangan saluran napas ilustratif.
- `H01-A02` cluster alveoli 3D/diagram.
- `H01-A03` potongan penghalang udara-darah dengan outline kapiler.
- `H01-A04` panah O₂/CO₂ dan label arah.
- `H01-A05` indikator zoom/transisi dari paru ke alveoli.
- `H01-A06` citation/limitation card.

**Dilarang:** CT scan, foto organ/paru nyata, darah, rokok/asap sebagai klaim kesehatan, before–after, atau visual yang menyiratkan penyakit.

---

## H02 — Cahaya, retina, dan pusat waktu SCN

**Source-card boundary:** penjelasan ritme sirkadian umum; bukan panduan jam tidur atau terapi insomnia.

| Scene | Waktu indikatif | Kebutuhan gambar/animasi | Teks/label yang diizinkan | QA khusus |
|---|---:|---|---|---|
| H02-S01 | 0–2 dtk | Berkas cahaya lembut masuk ke mata ilustratif | “Cahaya bisa memberi sinyal waktu?” | Hindari cahaya yang terlihat mengobati/memperbaiki kondisi |
| H02-S02 | 2–12 dtk | Mata samping + retina sederhana menerima sinyal cahaya | “Retina menerima cahaya” | Bukan foto mata/pasien; jangan mendramatisasi pupil |
| H02-S03 | 12–25 dtk | Garis sinyal bergerak dari mata ke siluet otak non-fotorealistik | “Sinyal menuju pusat waktu” | Jalur disederhanakan dan diberi label ilustrasi |
| H02-S04 | 25–42 dtk | Close-up hipotalamus stylized dengan titik/area SCN yang disorot | “SCN · pusat waktu di hipotalamus” | Lokasi/label harus diperiksa terhadap source card; jangan menunjukkan pembedahan otak |
| H02-S05 | 42–60 dtk | Jam 24 jam + ikon terang/gelap dan node ritme tubuh abstrak | “Membantu menyelaraskan ritme” | Hindari “mengatur semua hal” atau klaim solusi tidur |
| H02-S06 | 60–90 dtk | Citation/limitation card, diagram cahaya–SCN kecil | Sumber + “bukan panduan terapi tidur” | Tidak ada saran personal tersirat |

### Paket asset H02

- `H02-A01` mata/retina ilustratif.
- `H02-A02` beam cahaya dan garis sinyal non-dramatis.
- `H02-A03` siluet otak/hypothalamus stylized.
- `H02-A04` marker SCN dan label.
- `H02-A05` jam 24 jam serta ikon terang/gelap.
- `H02-A06` node ritme tubuh abstrak dan citation card.

**Dilarang:** visual insomnia, orang terjaga di ranjang, pil tidur, alarm sebagai solusi, rekomendasi jam tidur, atau otak/pembedahan nyata.

---

## H03 — Satu studi, systematic review, dan meta-analysis

**Source-card boundary:** literasi metode. Meta-analysis hanya bila studi cukup sesuai untuk digabung; bukan otomatis bukti terbaik.

| Scene | Waktu indikatif | Kebutuhan gambar/animasi | Teks/label yang diizinkan | QA khusus |
|---|---:|---|---|---|
| H03-S01 | 0–2 dtk | Satu kartu “1 studi” di pusat layar; kartu lain belum terlihat | “Satu studi cukup?” | Kartu fiktif tanpa logo jurnal/angka hasil nyata |
| H03-S02 | 2–15 dtk | Kartu studi fiktif muncul dengan perbedaan populasi/metode/outcome | “Desain” · “populasi” · “outcome” | Jangan menilai satu studi “tidak berguna” |
| H03-S03 | 15–30 dtk | Flow: pencarian → seleksi → systematic review | “Systematic review” | Flow dibuat sendiri, bukan screenshot PRISMA/jurnal tanpa lisensi |
| H03-S04 | 30–45 dtk | Gerbang keputusan: “cukup sesuai untuk digabung?” → ya/tidak | “Tidak selalu bisa digabung” | Keputusan visual harus bersyarat, bukan memutlakkan |
| H03-S05 | 45–62 dtk | Forest plot ilustratif buatan sendiri yang hanya menunjukkan konsep agregasi | “Meta-analysis bila sesuai” | Tidak memakai figure/angka studi nyata; jangan menyatakan hasil klinis |
| H03-S06 | 62–90 dtk | Recap tiga tingkatan + citation/limitation card | “Kualitas & kesesuaian tetap penting” | Sumber Cochrane terlihat dan terbaca |

### Paket asset H03

- `H03-A01` kartu studi fiktif dan variasi tag metodologi.
- `H03-A02` flow pencarian/seleksi buatan sendiri.
- `H03-A03` gerbang heterogeneity/kesesuaian.
- `H03-A04` forest plot konseptual buatan sendiri.
- `H03-A05` recap hierarchy non-mutu mutlak.
- `H03-A06` citation/limitation card.

**Dilarang:** screenshot jurnal, logo jurnal, figure forest plot dari artikel, angka efek kesehatan nyata, atau visual yang menempatkan meta-analysis di puncak absolut.

---

## H04 — Checklist klaim kesehatan viral

**Source-card boundary:** literasi informasi awal. Bukan vonis kebenaran klaim tertentu dan bukan debunk produk/terapi spesifik.

| Scene | Waktu indikatif | Kebutuhan gambar/animasi | Teks/label yang diizinkan | QA khusus |
|---|---:|---|---|---|
| H04-S01 | 0–2 dtk | Angka views besar pada postingan fiktif berubah menjadi ikon dokumen/sumber | “Mulai dari sumber, bukan views” | Tidak menggunakan UI/akun nyata atau klaim viral berbahaya |
| H04-S02 | 2–12 dtk | Mockup postingan fiktif dengan judul generik dan tombol “lihat sumber” | “1. Cari sumber asli” | Tidak pakai screenshot jurnal/brand; DOI/URL fiktif |
| H04-S03 | 12–25 dtk | Kaca pembesar bergerak dari headline ke isi/method/limitasi mockup | “2. Baca lebih dari judul” | Judul tetap fiktif dan tidak memberi info kesehatan salah |
| H04-S04 | 25–42 dtk | Tiga kartu checklist: analisis fakta, cek konteks visual, cek error | “3. Analisis” · “4. Cek visual” · “5. Waspadai error” | Adaptasi SHARE harus mudah dibaca; jangan menjanjikan kepastian |
| H04-S05 | 42–58 dtk | Tombol share fiktif berubah menjadi ikon jeda, lalu arah ke sumber | “Berhenti sejenak sebelum share” | Tidak mempermalukan pengguna/kreator |
| H04-S06 | 58–75 dtk | Recap checklist dan citation card | “Checklist membantu, bukan pengganti nasihat kesehatan” | WHO source line terbaca |

### Paket asset H04

- `H04-A01` mockup postingan dan angka views fiktif.
- `H04-A02` ikon dokumen/sumber, kaca pembesar, dan tombol jeda/share fiktif.
- `H04-A03` lima kartu checklist berlabel bahasa Indonesia.
- `H04-A04` mockup halaman sumber/DOI fiktif.
- `H04-A05` recap checklist.
- `H04-A06` citation/limitation card.

**Dilarang:** screenshot akun/kreator/jurnal nyata, tuduhan misinformation, before–after, klaim produk, atau pengulangan klaim kesehatan berbahaya sebagai contoh.

---

## Asset register dan approval

Sebelum satu pun scene dibuat, Production harus mengisi asset register berikut untuk setiap item `H01-Axx` sampai `H04-Axx`:

```text
Content ID / Asset ID / Versi:
Scene tujuan:
Jenis aset:
Klaim/label yang divisualkan:
Source-card dasar:
Pembuat/vendor:
Lokasi file sumber privat:
Lisensi atau bukti kepemilikan:
AI/tool/prompt (jika ada):
Reviewer akurasi dan hak:
Status: draft / revise / approved / hold
```

## Gate berikutnya

| Tahap | Status |
|---|---|
| COB, source card, dan hook | ✅ Selesai |
| Kebutuhan scene/asset | ✅ Disusun; belum ada aset dibuat |
| Naskah final + storyboard visual | ⏳ Memerlukan approval untuk tahap produksi awal |
| Asset register + proof lisensi | ⏳ |
| Render/audio/video | 🔒 Tidak diizinkan |
| PPU dan approval publikasi | 🔒 Tidak diizinkan |
