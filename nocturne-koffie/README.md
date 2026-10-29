# Nocturne Koffie — Landing Page + Sistem Marketing

Landing page katalog + pintu masuk order WhatsApp untuk **Nocturne Koffie Brand**
(brand kopi Banyuwangi — bukan roastery; sangrai dikerjakan Ais Coffee Roastery).

Dibangun mengikuti **Brief Website FINAL 3.7 (4 Okt 2026)**. Panduan pengerjaan,
spesifikasi komponen, dan daftar data yang masih menunggu konfirmasi ada di
[`panduan/PANDUAN-LANDING-PAGE.md`](panduan/PANDUAN-LANDING-PAGE.md).

```
nocturne-koffie/
├── index.html                    landing page (10 seksi, sesuai brief bagian 05)
├── assets/
│   ├── css/site.css              Paper · Ink · Burnt Orange · Espresso · Roast Gold
│   ├── js/site.js                render katalog, marquee, filter, pesan WhatsApp
│   ├── js/motion.js              lapisan gerak (tanpa library): reveal, parallax, magnet, tilt
│   ├── css/motion.css            token & aturan animasi
│   └── img/produk/               9 foto stiker kemasan (4:5, dari brief)
├── data/catalog.json             ← SATU-SATUNYA file yang perlu diubah rutin
├── brand/                        logo SVG, OG card, 9 label kantong + lembar A4, brand kit
├── komersial/                    harga grosir 4 tingkat, penawaran B2B, pipeline prospek
├── operasional/                  7 divisi: struktur, alur kerja + target per divisi
│   ├── divisi/                   D1…D7 — satu berkas per divisi
│   └── arsip/                    SOP versi 6 divisi (rujukan sejarah, tidak dipakai)
├── konten/                       hub konten: 5 video 9:16, carousel, story, feed
├── kampanye/index.html           landing page kampanye (hasil generate)
├── tools/papan.py                generator papan harian + tabel target divisi
├── tools/brandkit.py             generator logo, OG card, label kantong (Pillow)
├── tools/komersial.py            generator harga grosir + penawaran B2B
├── tools/kreatif.py              generator video 9:16, carousel, story, hub konten
├── tools/kampanye.py             generator landing page kampanye
├── dashboard/index.html          papan harian hasil generate (jangan diedit manual)
├── panduan/PANDUAN-LANDING-PAGE.md
├── panduan/07-sistem-motion.md
└── marketing/                    strategi, kalender konten, copy, CRM, B2B
```

## Menjalankan

```bash
cd nocturne-koffie
python3 -m http.server 8080        # situs  → http://localhost:8080
                                   # papan  → http://localhost:8080/dashboard/
python3 tools/papan.py             # hitung ulang papan harian
python3 tools/brandkit.py          # buat ulang label + logo (butuh Pillow)
python3 tools/komersial.py         # buat ulang harga grosir + penawaran B2B
python3 tools/kreatif.py           # render 5 video + carousel + story (butuh ffmpeg)
python3 tools/kreatif.py --cepat    # hanya gambar (tanpa encode video)
python3 tools/kampanye.py          # buat ulang landing kampanye dari katalog + manifest
```

`tools/kreatif.py` butuh ffmpeg. Di sandbox: `pip install --break-system-packages imageio-ffmpeg`
(FFmpeg biner tidak ikut tersimpan antar-sesi — generator akan gagal-soft ke gambar saja bila tidak ada,
dan itu dilaporkan di keluaran terminal serta di `data/kreatif.json` → `video_terencode`).

Halaman yang perlu dibuka: `/` (situs) · `/dashboard/` (papan harian) ·
`/kampanye/` (landing kampanye konten) · `/konten/` (hub aset, `noindex`) ·
`/brand/` (brand kit) · `/komersial/penawaran-b2b.html` (proposal B2B).

Harus lewat server — katalog dimuat dengan `fetch`, dan `file://` akan diblokir browser.

## Yang sudah jalan

- Hero headline 2 baris + **deretan kartu nama produk bergulir** (hanya nama, tanpa harga/foto)
- Klik nama di hero → meluncur ke kartu produk, tersorot 2 detik, URL berubah ke `#produk`
- Tombol jeda guliran, berhenti saat kursor menyentuh, hormati `prefers-reduced-motion`
- Katalog 9 SKU + 2 paket: foto 4:5, badge stok, nomor editorial, tasting notes,
  lima bulatan roast, **plakat petani** (nama, desa, elevasi, varietas), harga 4 ukuran
- Filter Jenis / Daerah / Ketersediaan yang menyaring grid **dan** rail editorial
- Pemilih ukuran & gilingan → harga dan pesan WhatsApp ikut berubah
- Status stok 4 tingkat: Tersedia · Terbatas · Habis · Menunggu panen
  (Habis/Menunggu panen → tombol berubah jadi "Kabari saya saat ada")
- Seksi Langganan (3 paket), Manifesto, Member (Nocturne Circle), penutup WA, footer poster
- Format pesan WhatsApp baku sesuai brief 6.2 (siap dibaca sistem di fase integrasi)
- JSON-LD `Brand`, meta OG, `noscript` dengan tautan WA
- Mobile: panel menu penuh, FAB WhatsApp, tanpa horizontal scroll
- **Motion layer**: intro berurutan, topeng headline, bar kemajuan gulir, reveal saat scroll,
  parallax hero/kartu/poster, tombol magnetik, tilt kartu, glow kursor, dan micro-feedback —
  semuanya mati otomatis pada `prefers-reduced-motion`

## Papan harian (menjalankan bisnis)

`tools/papan.py` membaca 10 berkas data lalu menulis `dashboard/index.html` + `dashboard/data.json`.
Sejak revisi 7 divisi, papan juga menampilkan **tabel target vs aktual per divisi** — target dibaca dari
`data/divisi.json`, aktual dihitung dari berkas data (tidak diketik).
Tanpa dependensi, tanpa server tambahan.

| Berkas | Isi | Siapa yang mengisi |
| --- | --- | --- |
| `data/catalog.json` | produk, harga, status stok yang tampil di situs | D1 |
| `data/biaya.json` | harga green bean, kemasan, upah, biaya tetap (**masih asumsi**) | D5 |
| `data/stok-lot.json` | lot green bean: masuk, terpakai, sisa | D1 |
| `data/batch-qc.csv` | catatan sangrai + skor cupping + lolos/tolak | D1 |
| `data/pesanan.csv` | satu baris per order | D2 |
| `data/konten-14hari.csv` | jadwal konten + status | D3 |
| `data/kpi.csv` | KPI mingguan (order, omzet, chat, followers) | D6 |
| `data/legal.json` | status dokumen usaha | D7 |
| `data/divisi.json` | **target & KPI 7 divisi, 3 bulan** — satu-satunya tempat angka target | owner |
| `data/kreatif.json` | manifest aset konten (video/carousel/story, status tayang) | D4 |

Yang dihitung otomatis: margin tiap ukuran, HPP, break-even, sisa bungkus per SKU
(dari green bean × yield; blend dari komponennya), order terlambat, resi kosong,
restock jatuh tempo (H+18), konten terlambat, batch ditolak, dan selisih status stok
situs vs lot.

```bash
python3 tools/papan.py                       # hari ini (WIB)
python3 tools/papan.py --tanggal 2026-11-03  # tanggal lain
python3 tools/papan.py --json                # ringkasan untuk dibaca mesin
```

**Tujuh divisi** (alur kerja + target per divisi di `operasional/divisi/`): Produksi & QC ·
Penjualan & CRM · Marketing & Pertumbuhan · Kreatif & Media · Operasional & Logistik ·
Keuangan · Brand & Legal. Ritme: 25 menit/hari + ±15 jam/minggu untuk satu orang —
urutannya di `operasional/00-struktur-divisi.md`, mulai eksekusi dari
`operasional/07-runbook-minggu-1.md`. Angka target hanya di `data/divisi.json`.

## Yang WAJIB dikonfirmasi sebelum tayang

Daftar lengkap + alasannya ada di panduan bagian 8. Ringkasnya:

| # | Hal | Kenapa penting |
| --- | --- | --- |
| 1 | Tingkat sangrai per produk (dari file desain label) | Sekarang masih usulan; badge menampilkan tanda "konfirmasi" |
| 2 | Tasting notes 3 kata per produk | Hanya Raung yang berasal dari label |
| 3 | Izin publikasi 7 nama petani | Nama sudah tayang dengan data brief |
| 4 | Blue Mount Ijen: Andi Wijaya atau Ijen Coffee Collective | Dua-duanya ada di brief, harus dipilih satu |
| 5 | Status stok nyata per SKU + tanggal | Sekarang hanya Blue Mount Ijen yang "Terbatas" |
| 6 | Konflik angka elevasi (Semeru, Raung, Ijen) & varietas Gayo/Semeru | Katalog vs label kemasan berbeda |
| 7 | Nomor WhatsApp Business aktif | Sekarang `628988188800` dari brief |
| 8 | Jam operasional & target balas 2 jam | Janji layanan |
| 9 | Angka program Member | Belum ditampilkan karena belum diputuskan |
| 10 | Tautan marketplace resmi | Belum ada, jadi tidak ditautkan |

Selama butir 1–6 belum beres, footer menampilkan "Situs versi uji coba — sebagian data
menunggu konfirmasi pemilik." Jangan dihapus sebelum beres.

## Aturan yang tidak boleh dilanggar

1. Nocturne **bukan** roastery. Tulis "brand kopi"; sangrai oleh **Ais Coffee Roastery**.
2. Tidak ada klaim "terbaik", "satu-satunya", "fresh daily", atau klaim kesehatan.
3. Harga & produk hanya diubah di `data/catalog.json`, tidak di `index.html`.
4. Harga situs = harga marketplace (10.9). Jangan perang harga dengan diri sendiri.
5. Petani: nama boleh (dengan izin), foto & titik lokasi tidak.

## Dokumen marketing

| File | Isi |
| --- | --- |
| `panduan/PANDUAN-LANDING-PAGE.md` | **Panduan pembuatan landing page** — 13 bagian, 25 butir QA |
| `brand/README.md` | brand kit: logo, label 70×100 mm, aturan cetak & pemakaian logo |
| `komersial/01-panduan-grosir.md` | 4 tingkat harga grosir, aturan margin, alur jual B2B |
| `marketing/08-konten-siap-pakai.md` | 7 post + 3 skrip TikTok + 9 judul marketplace siap salin |
| `marketing/09-media-kreator.md` | **playbook konten media kreator**: pipeline aset, bank 12 hook, jadwal, 3 angka ukur, aturan caption |
| `operasional/00-struktur-divisi.md` | 7 divisi, RACI, ritme harian/mingguan, cara membaca tabel target |
| `operasional/divisi/README.md` | indeks 7 divisi + cara mengubah target di `data/divisi.json` |
| `operasional/divisi/D1-produksi-qc.md` | alur 10 langkah satu batch, gerbang QC, target & DoD |
| `operasional/divisi/D2-penjualan-crm.md` | chat→order→pelanggan, naskah wajib, alur B2B, target |
| `operasional/divisi/D3-marketing-pertumbuhan.md` | konten→chat, 7 kanal, ritme 90 menit, target |
| `operasional/divisi/D4-kreatif-media.md` | klip mentah vs aset render, spesifikasi teknis, target |
| `operasional/divisi/D5-operasional-logistik.md` | packing, cut-off 15.00, ongkir, opname, target |
| `operasional/divisi/D6-keuangan.md` | HPP, margin, break-even, tutup buku, target |
| `operasional/divisi/D7-brand-legal.md` | gerbang klaim 4 pertanyaan, izin, dokumen, target |
| `operasional/07-runbook-minggu-1.md` | rencana 10 hari pertama per divisi |
| `panduan/07-sistem-motion.md` | **Sistem gerak** — 5 skill motion teratas + 13 gerak yang dipasang, token, larangan, 10 butir uji |
| `marketing/00-strategi-90hari.md` | Strategi 90 hari (positioning, segmen, ritme 7 jam/minggu, KPI) |
| `marketing/01-kalender-konten-30hari.md` | 30 hari konten + aset yang direkam saat produksi |
| `marketing/02-copy-library.md` | Bio, caption, 6 template WhatsApp, 4 skrip B2B |
| `marketing/03-marketplace-dan-ads.md` | Judul & deskripsi listing, bundling, aturan iklan |
| `marketing/04-whatsapp-crm-dan-b2b.md` | Alur follow up H+0…H+60, langganan, pipeline kafe |
| `marketing/05-kpi-tracker.csv` | Tracker mingguan |
| `marketing/06-checklist-launch-14hari.md` | Checklist 14 hari |

> **Catatan:** file `marketing/` ditulis sebelum brief ini diterima. Dua hal perlu
> diselaraskan: (a) kata "roastery" untuk Nocturne harus diganti "brand kopi", dan
> (b) produk/harga di materi itu masih versi lama (6 SKU), sedangkan situs kini memakai
> 9 SKU dari brief bagian 10. Panduan landing page sudah memakai data brief.
