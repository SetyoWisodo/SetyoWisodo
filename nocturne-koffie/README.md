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
├── operasional/                  6 divisi: struktur, SOP, KPI, runbook minggu 1
├── tools/papan.py                generator papan harian (stdlib, tanpa dependensi)
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
```

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

`tools/papan.py` membaca 7 berkas data lalu menulis `dashboard/index.html` + `dashboard/data.json`.
Tanpa dependensi, tanpa server tambahan.

| Berkas | Isi | Siapa yang mengisi |
| --- | --- | --- |
| `data/catalog.json` | produk, harga, status stok yang tampil di situs | D1 |
| `data/biaya.json` | harga green bean, kemasan, upah, biaya tetap (**masih asumsi**) | D5 |
| `data/stok-lot.json` | lot green bean: masuk, terpakai, sisa | D1 |
| `data/batch-qc.csv` | catatan sangrai + skor cupping + lolos/tolak | D1 |
| `data/pesanan.csv` | satu baris per order | D2 |
| `data/konten-14hari.csv` | jadwal konten + status | D3 |
| `data/kpi.csv` | KPI mingguan | D5 |
| `data/legal.json` | status dokumen usaha | D6 |

Yang dihitung otomatis: margin tiap ukuran, HPP, break-even, sisa bungkus per SKU
(dari green bean × yield; blend dari komponennya), order terlambat, resi kosong,
restock jatuh tempo (H+18), konten terlambat, batch ditolak, dan selisih status stok
situs vs lot.

```bash
python3 tools/papan.py                       # hari ini (WIB)
python3 tools/papan.py --tanggal 2026-11-03  # tanggal lain
python3 tools/papan.py --json                # ringkasan untuk dibaca mesin
```

**Enam divisi** (detail di `operasional/`): Produksi & QC · Penjualan & CRM ·
Marketing & Konten · Operasional & Logistik · Keuangan · Brand & Legal.
Ritme: 25 menit/hari + ±7 jam/minggu. Mulai dari `operasional/07-runbook-minggu-1.md`.

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
| `operasional/00-struktur-divisi.md` | 6 divisi, RACI, ritme harian/mingguan, eskalasi |
| `operasional/01-produksi-qc.md` | rantai produksi, kode batch, gerbang QC, aturan stok |
| `operasional/02-penjualan-crm.md` | alur order, template WA, langganan, pipeline B2B |
| `operasional/03-marketing-konten.md` | rekam saat produksi, ritme posting, aturan klaim |
| `operasional/04-operasional-logistik.md` | SOP packing, ongkir, retur, opname |
| `operasional/05-keuangan.md` | HPP, target margin, break-even, tutup buku |
| `operasional/06-brand-legal.md` | identitas, klaim terlarang, privasi petani, dokumen |
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
