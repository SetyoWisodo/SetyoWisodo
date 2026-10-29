# Brand Kit — Nocturne Koffie

Semua berkas di folder ini **dihasilkan** oleh `python3 tools/brandkit.py`. Jangan diedit manual —
kalau ada yang salah, perbaiki generatornya atau datanya (`data/catalog.json`, `data/batch-qc.csv`).

Buka `brand/index.html` untuk melihat semuanya sekaligus.

| Berkas | Ukuran | Dipakai untuk |
| --- | --- | --- |
| `logo-mark.svg` | vektor | favicon, avatar, watermark, stempel |
| `logo-lockup.svg` | vektor (420×120) | header situs, kop surat, kartu nama, invoice |
| `logo-lockup-dark.svg` | vektor | latar Ink/Espresso (kemasan hitam, poster) |
| `favicon.svg` · `apple-touch-icon.png` | 64 / 180 px | tab browser, ikon HP |
| `og-1200x630.jpg` | 1200×630 | kartu saat tautan dibagikan (WA, IG, X, FB) |
| `label-<produk>.png` | 827×1181 px (70×100 mm @300 dpi) | stiker kantong per SKU |
| `label-sheet-a4.png` | A4 @300 dpi | 8 label per lembar + tanda potong |

## Cara membuat ulang label

```bash
python3 tools/brandkit.py                            # tanggal hari ini, batch A
python3 tools/brandkit.py --tanggal 2026-11-03 --batch B
```

- `--tanggal` = tanggal sangrai yang dicetak di label (bukan tanggal cetak).
- `--batch` = huruf batch pada bulan itu (A = sangrai pertama, B = kedua, dst).
- Stempel QC (angka + "DIPERIKSA · QC") hanya muncul jika produk punya batch **lolos** di
  `data/batch-qc.csv`. Produk yang belum pernah dicicipi tidak diberi stempel — itu disengaja.

Format kode batch: `NK-<KODE>-<YYMM>-<A>`, contoh `NK-IJN-2610-A` (Blue Mount Ijen, Okt 2026, batch 1).

## Cara cetak

| Kebutuhan | Berkas | Catatan |
| --- | --- | --- |
| Stiker roll (label per bungkus) | `label-<produk>.png` | minta cetak 70×100 mm, bahan vinyl matte / kertas sticker |
| Cetak sendiri di rumah/kantor | `label-sheet-a4.png` | kertas sticker A4, skala 100% (**jangan** "fit to page"), potong di tanda |
| Kantong | — | black matte standing pouch + one-way valve, jendela kosong (label ditempel) |

## Aturan pemakaian logo

1. Berkas gelap hanya di latar terang (Paper), berkas terang hanya di latar gelap (Ink/Espresso).
2. Jangan memberi warna lain, gradien, bayangan, atau mengubah proporsi.
3. Ruang aman minimal setinggi simbol di semua sisi.
4. Ukuran minimum: lockup ≥ 120 px lebar · simbol ≥ 24 px. Di bawah itu pakai simbol saja.
5. Kalau logo diletakkan di atas foto, beri bidang Paper/Ink di belakangnya.

## Isi label (mengapa begitu)

| Elemen | Alasan |
| --- | --- |
| Nama produk besar | Orang membeli nama, bukan kode SKU |
| Nama petani + desa + elevasi | Pembeda utama; tidak bisa ditiru kompetitor |
| Varietas | Bukti teknis, dipakai pembeli serius |
| Catatan rasa (serif italic) | Bahasa rasa, bukan jargon |
| Rekomendasi seduh | Mengurangi pertanyaan berulang di WhatsApp |
| **Tanggal sangrai + kode batch** | Bukti kesegaran yang bisa diverifikasi |
| 5 bulatan level roast | Sama dengan sistem di kemasan & situs |
| Stempel QC | Hanya jika batch benar-benar dicicipi dan lolos |
| "Disangrai mingguan oleh Ais Coffee Roastery" | Wajib — Nocturne bukan roastery (brief 11.8) |

## Yang belum ada di kit ini (butuh Anda/desainer)

- Foto produk asli (label di atas kemasan + kopi di mangkuk) — 3 foto per SKU.
- Berkas vektor master logo dari desainer (yang ada di sini adalah rekonstruksi siap pakai).
- Stiker "kartu ucapan" & hangtag hadiah.
- Kemasan fisik: pilih pouch 250 g dengan valve, warna hitam matte.
