# Memahami Krisis / Understanding Crisis

Buku rujukan dua bahasa. Edisi Inggris lebih dulu (keputusan 2026-11-26), edisi Indonesia
menyusul. Turunan Bab 1 *Surviving the Future* yang dibedah menjadi 17 bab dalam 5 bagian.

## Isi

| Bagian | Bab | Inggris | Indonesia |
|---|---|---|---|
| — | Pengantar | The Sentence Under Test | Satu Kalimat yang Perlu Diperiksa |
| I — Diagnosis | 1 | Hazard, Exposure, Vulnerability | Bahaya, Paparan, Kerentanan |
| | 2 | Crisis Does Not Arrive as a Single Blow | Krisis Tidak Datang sebagai Satu Pukulan |
| | 3 | Indonesia as Reader, Not Example | Indonesia sebagai Pembaca, bukan Contoh |
| II — Vulnerability | 4 | Heat, the Invisible Killer | Panas, Pembunuh yang Tidak Terlihat |
| | 5 | Water: Too Much, Too Little, and Sinking Ground | Air — Terlalu Banyak, Terlalu Sedikit |
| | 6 | Food: When One Harvest Becomes a Price Somewhere Else | Pangan — Ketika Satu Panen Menjadi Harga |
| | 7 | Disease That Moves Because the Climate Moves | Penyakit yang Berpindah |
| III — Capacity | 8 | Money: Insurance, Aid, and Who Counts as Worth Saving | Uang — Asuransi, Bantuan |
| | 9 | Infrastructure as a Chain of Dependencies | Infrastruktur sebagai Rantai |
| | 10 | Social Capital: The Thing That Cannot Be Bought | Modal Sosial |
| | 11 | Knowledge: Forecasts That Do Not Arrive | Pengetahuan — Ramalan yang Tidak Sampai |
| IV — Decisions | 12 | Displacement: The Choice That Always Arrives Late | Perpindahan |
| | 13 | Justice: Who Emits, Who Absorbs | Keadilan |
| | 14 | Uncertainty: Waiting for Certainty Is Also a Decision | Ketidakpastian |
| V — Action | 15 | Households: What Can Be Done This Week | Rumah Tangga |
| | 16 | Communities and Cities: Capacity Built Before the Rain | Komunitas dan Kota |
| | 17 | Reading the Claims: How to Judge a Climate Promise | Membaca Klaim |

Tiap bab: kasus pembuka → mekanisme → bukti → **kotak metode** → kontra-kasus →
**"What would prove this chapter wrong"** → daftar baca.

## Status

| | Inggris | Indonesia |
|---|---|---|
| Berkas bab ditulis | 18/18 | 4/18 ditulis ulang ber-sitasi |
| Kata | 26.259 | 20.212 |
| Halaman PDF | 123 | 111 |
| Sitasi dalam teks | 86 | 29 |
| Sumber unik dikutip | 47 | 26 |
| Sitasi yatim | 0 | 0 |

Edisi Inggris **lengkap dan dibangun**. Edisi Indonesia masih memakai bab lama
(ber-sitasi baru 4 bab) dan perlu diselaraskan dengan struktur Inggris.

## Build

```bash
pip install --break-system-packages pypandoc_binary typst pypdf pymupdf
python3 book2/build.py --lang en          # -> book2/publish/en.pdf
python3 book2/build_extras.py --lang en   # -> cover JPG, EPUB, DOCX
python3 book2/build.py --lang id
python3 book2/build_extras.py --lang id
python3 book2/tools/audit_rujukan.py --lang en
```

Toolchain tidak persisten di sandbox; pasang ulang tiap sesi baru.

## Struktur

- `meta_en.json`, `meta_id.json` — judul, subjudul, copyright, back cover, kata kunci
- `src/en/` — `00-introduction`, `02-ch01`…`18-ch17` (bab N = berkas N+1)
- `src/id/` — `00-pengantar`, `02-bab01`…`99-pustaka`
- `template/book.typ` — 6×9 in, Source Serif 4 + Source Sans 3, `#part-page(blurb:)`
- `template/filter.lua` — `::: {.box}`, `::: lead`, `::: {.part}`, `[@a; @b]` → `#cite-group`
- `reference/bibliografi.csv` — 79 entri; `reference/klaim.csv` — 45 klaim
- `reference/BLUEPRINT_EN.md` — kerangka, gaya, aturan sumber
- `tools/audit_rujukan.py` — audit kepadatan sitasi, yatim, angka tanpa sumber
- `publish/` — PDF, EPUB, DOCX, sampul untuk kedua bahasa

## Angka

- **EN** — 123 hlm, 26.259 kata, 86 sitasi, 47 sumber, 0 yatim,
  5 kalimat berangka tanpa sumber. PDF 778.573 B.
- **ID** — 111 hlm, 20.212 kata, 29 sitasi, 26 sumber, 0 yatim, 12 kalimat berangka.
  PDF 643.874 B.

## Catatan sumber

- Setiap angka wajib punya baris di `reference/klaim.csv`: 40/45 terverifikasi ke sumber primer.
- Verifikasi mengubah empat angka: garis pantai **99.093 km**, beras **+10%**,
  Jakarta **1–15 cm/th (maks 28)**, Texas **14,4 juta**.
- Kesepakatan cakupan: sitasi + kotak angka + kotak metode + daftar baca.
  **Tanpa glosarium, soal diskusi, atau latihan riset.**
- Versi Inggris lebih dulu; versi Indonesia menyusul.
