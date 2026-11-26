# Memahami Krisis — buku 17 bab

Turunan Bab 1 *Surviving the Future* yang dibedah menjadi 17 bab (5 bagian) + pengantar + sumber.

## Isi

| Bagian | Bab | Judul |
|---|---|---|
| — | Pengantar | Satu Kalimat yang Perlu Diperiksa |
| I — Diagnosis | 1 | Bahaya, Paparan, Kerentanan |
| | 2 | Krisis Tidak Datang sebagai Satu Pukulan |
| | 3 | Indonesia sebagai Pembaca, bukan Contoh |
| II — Kerentanan | 4 | Panas, Pembunuh yang Tidak Terlihat |
| | 5 | Air — Terlalu Banyak, Terlalu Sedikit, dan Tanah yang Menurun |
| | 6 | Pangan — Ketika Satu Panen Menjadi Harga di Tempat Lain |
| | 7 | Penyakit yang Berpindah karena Iklim Berpindah |
| III — Kapasitas | 8 | Uang — Asuransi, Bantuan, dan Siapa yang Layak Diselamatkan |
| | 9 | Infrastruktur sebagai Rantai Ketergantungan |
| | 10 | Modal Sosial — Hal yang Tidak Bisa Dibeli |
| | 11 | Pengetahuan — Ramalan yang Tidak Sampai |
| IV — Keputusan | 12 | Perpindahan — Pilihan yang Selalu Datang Terlambat |
| | 13 | Keadilan — Siapa Mengemisikan, Siapa Menanggung |
| | 14 | Ketidakpastian — Menunggu Kepastian Adalah Keputusan |
| V — Tindakan | 15 | Rumah Tangga — Yang Bisa Dikerjakan Minggu Ini |
| | 16 | Komunitas dan Kota — Kapasitas yang Dibangun Sebelum Hujan |
| | 17 | Menutup Buku, Membuka Pertanyaan |

Tiap bab ditutup kotak **"Apa yang akan membuktikan bab ini salah"** — satu atau dua pengamatan yang, bila terjadi, memaksa argumennya direvisi.

## Build

```bash
pip install --break-system-packages pypandoc_binary typst pypdf pymupdf
python3 book2/build.py --lang id          # -> book2/publish/id.pdf (6×9 in, 107 hlm)
python3 book2/build_extras.py --lang id   # -> cover JPG, EPUB, DOCX
```

Toolchain tidak persisten di sandbox; perlu dipasang ulang tiap sesi baru.

## Struktur

- `meta_id.json` — judul, subjudul, copyright, back cover, kata kunci
- `src/id/*.md` — 18 berkas (pengantar, 17 bab, sumber)
- `template/book.typ` — 6×9 in, margin 20/22 mm, Source Serif 4 + Source Sans 3
- `template/filter.lua` — kotak `::: {.box}`, `::: lead`, `::: hanging`, tabel, hyphenation ID
- `publish/` — PDF, EPUB, DOCX, cover

## Angka

20.365 kata; 107 halaman; PDF 6×9 in; EPUB + DOCX + sampul 6×9 in.

## Catatan

- Angka yang dipakai berasal dari sumber yang tercantum di `src/id/99-sumber.md`; angka yang tidak bisa dilacak tidak dipakai.
- Versi Inggris belum dibuat — terjemahan bab-per-bab menyusul bila diminta.
