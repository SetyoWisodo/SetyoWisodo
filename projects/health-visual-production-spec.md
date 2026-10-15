<div align="center">

# 🖼️ Spesifikasi Visual untuk Divisi Produksi

### **Kanal sains kesehatan nasional · anatomi non-grafis · visual sebagai bukti penjelasan**

*Status: rencana aset dan QA. Dokumen ini tidak mengotorisasi pembuatan gambar, render, pembelian aset, koneksi akun, atau publikasi.*

</div>

---

## Ringkasan keputusan

| Area | Standar produksi |
|---|---|
| **Fungsi gambar** | Menjelaskan mekanisme atau metode secara visual; bukan hiasan stok atau pemancing rasa takut |
| **Gaya inti** | Ilustrasi/3D non-fotorealistik, diagram bergerak, data visual, dan motion graphic yang mudah dibaca |
| **Aset prioritas** | Dibuat sendiri atau memakai aset dengan lisensi komersial yang terdokumentasi |
| **AI image/video** | Boleh sebagai alat bantu konsep/aset hanya setelah review anatomi, provenance, hak komersial, dan disclosure yang relevan; lihat [Audit & Integrasi Skill Image/Video](visual-skill-integration-audit.md) |
| **Yang tidak dipakai** | Foto pasien, rekam medis, CT/MRI, operasi, luka, darah/organ nyata, visual penyakit yang mengejutkan, dan screenshot akun/jurnal tanpa hak jelas |
| **Gate** | Source card → storyboard/asset register → Production draft → PPU → approval pemilik akun |

> **Aturan sederhana:** jika visual tidak membuat penonton lebih memahami klaim yang diizinkan source card, visual itu tidak diperlukan.

---

## 1. Hierarki aset yang diizinkan

| Prioritas | Jenis aset | Penggunaan | Bukti yang disimpan di asset register |
|---:|---|---|---|
| 1 | Diagram, ikon, shape, data visual, atau 3D yang dibuat sendiri | Pilihan utama untuk proses tubuh dan metode penelitian | File sumber/proyek, pembuat, tanggal, dan versi |
| 2 | Aset stok/3D dengan lisensi komersial | Hanya bila lisensi mencakup platform, monetisasi, turunan, dan wilayah penggunaan | URL/vendor, invoice/receipt, teks lisensi, asset ID, batas penggunaan |
| 3 | Gambar/visual AI | Hanya sebagai aset yang ditinjau manusia; anatomy harus diverifikasi dan prosesnya tidak boleh mengaburkan sumber | Tool/model, prompt/setting, tanggal, versi, keputusan disclosure, review anatomy/hak |
| 4 | Gambar dari jurnal/open licence | Terbatas; cek lisensi artikel **dan** gambar spesifik, atribusi, serta hak komersial/adaptasi | URL sumber, lisensi, atribusi, perubahan yang dibuat |
| — | Screenshot jurnal, social post, foto pasien, footage prosedur, gambar hasil pencarian | Tidak dipakai secara default | Tidak lolos tanpa clearance khusus dan PPU |

**Sitasi bukan izin penggunaan gambar.** DOI/judul jurnal dapat menjadi sumber pengetahuan, tetapi tidak memberi izin otomatis untuk memakai figure atau screenshot dari artikel tersebut.

---

## 2. Paket visual minimum per video short

Target awal adalah video 60–90 detik. Production tidak membuat slideshow gambar statis; scene harus berubah untuk mengikuti penjelasan.

| Komponen | Jumlah minimum | Fungsi |
|---|---:|---|
| **Hook visual** | 1 scene / 1 hero asset | Muncul pada 0–2 detik dan langsung menjawab pertanyaan pembuka secara visual |
| **Progressive explanation** | 3–5 scene | Memecah proses menjadi langkah yang benar, bukan satu visual yang diputar ulang |
| **Label/callout** | 3–6 elemen | Nama struktur, arah, perbandingan, atau syarat yang perlu dibaca penonton |
| **Evidence/limitation card** | 1–2 scene | Sumber ringkas dan batas penting yang relevan dengan klaim |
| **CTA/end card** | 1 scene | CTA edukatif yang konsisten; bukan dorongan diagnosis atau produk |
| **Thumbnail/keyframe** | 1 versi per rasio | Ringkas, non-grafis, tidak memakai bait ketakutan |

**Estimasi awal:** 6–8 scene dan sekitar 8–12 aset visual unik per short, di luar caption. Asset yang sama boleh dipakai ulang sebagai elemen brand hanya bila tetap relevan dan tidak membuat konten menjadi template berulang tanpa nilai baru.

---

## 3. Format dan layout lintas platform

| Output | Ukuran kerja/rilis | Aturan layout |
|---|---|---|
| **Vertical short** | 1080 × 1920, 9:16 | Master awal untuk Reels, TikTok, dan YouTube Shorts; sisakan area aman dari UI platform di atas/bawah |
| **Landscape YouTube** | 1920 × 1080, 16:9 | Buat dari scene sumber yang sama; susun ulang elemen, jangan meregangkan hasil vertical |
| **Thumbnail YouTube** | 1280 × 720, 16:9 | Satu konsep visual, teks sangat singkat, anatomi non-grafis |
| **Source files** | Vector/3D/project file + export lossless bila tersedia | Simpan privat dan versioned agar revisi/crop dapat dibuat tanpa mengambil gambar acak baru |

### Prinsip layout

- Satu gagasan utama per scene; teks besar dan tidak bertumpuk pada organ/diagram penting.
- Gunakan kontras tinggi, label jelas, dan tanda kedua selain warna—misalnya panah, pola, atau teks—agar tetap terbaca oleh audiens dengan perbedaan persepsi warna.
- Tidak ada logo intro panjang. Hero visual dan hook hadir pada frame pertama.
- Caption/subtitle bukan pengganti visual yang benar; bila visual menggambarkan arah/proses secara salah, scene harus direvisi.
- Template warna/font baru boleh dikunci setelah identitas brand disetujui; sebelum itu gunakan gaya provisional yang bersih dan konsisten.

---

## 4. Bahasa visual kesehatan yang aman

### Wajib dilakukan

- Gunakan siluet, organ 3D sederhana, diagram lapis, garis jalur, ikon, dan panah untuk menunjukkan **fungsi**.
- Tampilkan label “ilustrasi edukatif” ketika model menyederhanakan struktur kompleks.
- Tunjukkan batas bukti secara visual, misalnya label “tidak selalu bisa digabung” pada video meta-analysis.
- Gunakan mockup fiktif untuk contoh postingan/DOI/headline, bukan akun atau pasien nyata.
- Sertakan citation line singkat yang dapat dibaca pada scene sumber atau caption/deskripsi.

### Tidak boleh dilakukan

- Memperlihatkan darah, luka, operasi, jaringan/organ nyata, pemindaian medis, pasien kesakitan, atau before–after tubuh.
- Membuat organ menggelembung/rusak sebagai dramatisasi tanpa dasar dari source card.
- Menggambarkan proses umum sebagai indikator penyakit penonton.
- Menambahkan klaim penyembuhan, angka klinis, atau label diagnosis ke visual.
- Memakai wajah/voice/avatar yang terlihat seperti dokter atau ahli medis bila tidak ada kredensial yang sesuai.

---

## 5. Asset register — wajib sebelum scene dipakai

Setiap aset menerima ID dan dicatat sebelum masuk render draft.

```text
Content ID:
Asset ID / versi:
Scene dan fungsi penjelasan:
Jenis: 3D / diagram / vector / stock / AI / open-licence
Klaim/label yang divisualkan:
Dasar fakta: source card + bagian sumber yang relevan
Pembuat atau vendor:
Lokasi file sumber privat:
Lisensi/receipt/URL dan hak penggunaan komersial:
Apakah AI digunakan? Tool/model/prompt/setting/disclosure:
Rasio/crop yang disiapkan:
Reviewer anatomi/hak:
Status: draft / revise / approved / retired
```

Aset tanpa asal, lisensi, atau kaitan source-card yang jelas mendapat status **HOLD**.

---

## 6. Workflow Divisi Produksi

```text
COB + source card + hook yang disetujui
                ↓
Visual proof: daftar scene yang diperlukan untuk menjawab hook
                ↓
Storyboard + asset register + daftar lisensi
                ↓
Editor cek anatomi, label, dan batas klaim
                ↓
Draft motion/animasi + caption + source card visual
                ↓
Audio QA + visual QA
                ↓
PPU memeriksa versi video final yang persis sama
```

### Handoff yang harus diterima PPU

- Naskah final dan source card yang dipakai.
- Storyboard/shot list dan daftar semua asset ID.
- Bukti lisensi untuk aset yang tidak dibuat sendiri.
- Bukti review anatomi/fakta visual dan perubahan yang dilakukan.
- Keputusan disclosure AI bila ada.
- Export final per platform, caption, source line, dan thumbnail.

---

## 7. Visual QA sebelum PPU

| Pemeriksaan | Pertanyaan lulus |
|---|---|
| **Akurasi** | Apakah label, letak, arah panah, urutan proses, dan skala naratif cocok dengan source card? |
| **Batas klaim** | Apakah visual dapat disalahpahami sebagai diagnosis, terapi, atau janji hasil personal? |
| **Non-grafis** | Apakah semua elemen aman untuk edukasi umum dan tidak menampilkan tubuh/cedera nyata? |
| **Hak aset** | Apakah semua asset ID mempunyai asal dan hak komersial yang dapat dibuktikan? |
| **Kejelasan** | Apakah scene dapat dipahami tanpa teks panjang atau audio yang menjelaskan kebalikan visual? |
| **Orisinalitas** | Apakah ada nilai animasi/diagram/penjelasan baru, bukan kompilasi stok atau slideshow? |
| **AI transparency** | Bila AI membuat/mengubah visual realistis secara signifikan, apakah disclosure platform telah diputuskan? |
| **Platform fit** | Apakah crop, subtitle, citation, dan thumbnail terbaca pada ratio tujuan? |

Kegagalan pada akurasi, keselamatan visual, atau hak aset bersifat **red violation** dan langsung HOLD di PPU.

---

## 8. Kebutuhan Batch 1

Shot list konkret untuk H01–H04 tersedia di [Batch 1 — Visual Production Requirements](health-content-batches/2026-10-batch-01/04-visual-production-requirements.md). Dokumen tersebut hanya mengatur kebutuhan scene/aset dan tidak mengizinkan render atau pembuatan gambar.

---

## 9. Apa yang dibutuhkan dari pemilik akun

Tidak diperlukan foto pasien, foto pribadi, atau footage operasi dari pemilik akun.

Yang kelak perlu diputuskan pemilik akun sebelum produksi visual dimulai:

1. Nama brand, logo, palet warna, dan font yang boleh digunakan.
2. Apakah aset dibuat sendiri, dibeli dengan lisensi komersial, atau memakai tool AI yang telah ditinjau.
3. Anggaran/lisensi bila memakai 3D stock atau font berbayar.
4. Persetujuan storyboard dan asset register per batch.
5. Persetujuan PPU dan approval final sebelum render/upload.

---

## Referensi internal

- [Rencana Konten Sains Kesehatan Berbasis Bukti](health-evidence-content-plan.md)
- [Batch 1 — Content Opportunity Briefs](health-content-batches/2026-10-batch-01/01-content-opportunity-briefs.md)
- [Batch 1 — Source Cards](health-content-batches/2026-10-batch-01/02-source-cards.md)
- [Batch 1 — Hook & Retention Options](health-content-batches/2026-10-batch-01/03-hook-retention-options.md)
