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
| Berkas bab ditulis | 19/19 | 19/19 |
| Kata (sumber .md) | 77.500 | 66.751 |
| Halaman PDF | 276 | 298 |
| Gambar ber-kredit | 7 | 7 |
| Seksi H2 per bab | 10-12 | 10-12 |
| Median kata per seksi | 406 | 406 |
| Sitasi dalam teks | 289 | 288 |
| Sumber unik dikutip | 71 | 71 |
| Sitasi yatim | 0 | 0 |
| Kalimat berangka tanpa sumber | 8 | 41 |
| Klaim di buku besar bukti | 145 | 145 |
| Klaim terverifikasi | 145/145 | 145/145 |
| Entri bibliografi | 104 | 104 |
| Entri ber-identifier (DOI/ISBN) | 70/104 | 70/104 |
| Bab dengan kepadatan sitasi >= 2,0/1.000 | 17/17 | 17/17 |

Kedua edisi **lengkap dan dibangun**. Semua gate audit lolos: kepadatan sitasi
≥2/1.000 kata, ≥40 sumber unik, 0 yatim, ≤1 kalimat berangka tanpa sumber per
1.000 kata, dan ≥120 baris `klaim.csv` terverifikasi. Laporan per bahasa:
`reference/laporan_audit_id.md` dan `reference/laporan_audit_en.md`.

## Build

```bash
pip install --break-system-packages pypandoc_binary typst pypdf pymupdf
python3 book2/build.py --lang en          # -> book2/publish/en.pdf
python3 book2/build_extras.py --lang en   # -> cover JPG, EPUB, DOCX
python3 book2/build.py --lang id
python3 book2/build_extras.py --lang id
python3 book2/tools/audit_rujukan.py --lang en
python3 book2/gambar/sisipkan.py            # pasang caption ke naskah (--cabut untuk hapus)
python3 book2/tools/siapkan_gambar.py       # rakit ulang gambar + pita kredit
```

Toolchain tidak persisten di sandbox; pasang ulang tiap sesi baru.

## Struktur

- `meta_en.json`, `meta_id.json` — judul, subjudul, copyright, back cover, kata kunci
- `src/en/` — `00-introduction`, `02-ch01`…`18-ch17` (bab N = berkas N+1)
- `src/id/` — `00-pengantar`, `02-bab01`…`99-pustaka`
- `template/book.typ` — 6×9 in, Source Serif 4 + Source Sans 3, `#part-page(blurb:)`
- `template/filter.lua` — `::: {.box}`, `::: lead`, `::: {.part}`, `[@a; @b]` → `#cite-group`
- `reference/bibliografi.csv` — 87 entri; `reference/klaim.csv` — 145 klaim
- `reference/BLUEPRINT_EN.md` — kerangka, gaya, aturan sumber
- `tools/audit_rujukan.py` — audit kepadatan sitasi, yatim, angka tanpa sumber
- `gambar/` — 7 gambar final (lebar 1800 px, kredit tercetak di dalam gambar),
  `manifes.json` (sumber + lisensi setiap gambar), `caption.json` (caption EN/ID),
  `sumber/` (berkas asli), `sisipkan.py` (menyisipkan/mencabut gambar dari naskah)
- `publish/` — PDF, EPUB, DOCX, sampul untuk kedua bahasa

## Angka

- **EN** — 276 hlm, 77.500 kata, 289 sitasi, 71 sumber, 0 yatim,
  8 kalimat berangka tanpa sumber. `publish/en.pdf` 6.624.491 B.
- **ID** — 298 hlm, 66.751 kata, 288 sitasi, 71 sumber, 0 yatim,
  41 kalimat berangka tanpa sumber. `publish/id.pdf` 6.609.888 B.
- Turunan (berisi 7 gambar isi): EPUB 4.998 KB (EN) / 5.002 KB (ID);
  DOCX 4.872 KB / 4.859 KB; sampul JPG 200.908 B / 209.746 B.

## Gambar

Tujuh gambar, semuanya domain publik atau berlisensi terbuka, dengan kredit dan
lisensi **tercetak di dalam berkas gambar** supaya ikut terbawa ke Word, EPUB, atau
salinan cetak. Daftar kredit juga ada di "A Note on Sources" / "Catatan Sumber".

| Berkas | Subjek | Bab | Sumber / lisensi |
|---|---|---|---|
| 01 | Siklon Amphan mendarat, 2020 | 1 | Copernicus Sentinel-3 / ESA, CC BY-SA 3.0 IGO |
| 02 | Banjir dataran Indus, 2010 | 2 | NASA/JPL ASTER PIA13368, PD |
| 03 | Suhu permukaan 4 kota, 2019 | 4 | NASA/JPL ECOSTRESS PIA23148, PD |
| 04 | Anomali panas Eropa 2003 | 4 | NASA EO (Stöckli & Simmon), PD |
| 05 | Theewaterskloof, Cape Town 2018 | 5 | Antti Lipponen / Sentinel-2B, CC BY 2.0 |
| 06 | New Orleans setelah tanggul jebol, 2005 | 5 | NOAA Corps, PD |
| 07 | Atol Funafuti, Tuvalu | 12 | NASA EO, Landsat 9 OLI-2, PD |

Caption ada di `gambar/caption.json` (EN + ID) dan disisipkan oleh
`python3 gambar/sisipkan.py`; `--cabut` menghapusnya kembali. Setiap gambar juga
tercatat di `gambar/manifes.json` (berkas sumber, lisensi, catatan).

## Catatan sumber

- Setiap angka wajib punya baris di `reference/klaim.csv`: 145 baris, semuanya terverifikasi ke sumber.
- Verifikasi mengubah empat angka: garis pantai **99.093 km**, beras **+10%**,
  Jakarta **1–15 cm/th (maks 28)**, Texas **14,4 juta**.
- Kesepakatan cakupan: sitasi + kotak angka + kotak metode + daftar baca.
  **Tanpa glosarium, soal diskusi, atau latihan riset.**
- Versi Inggris lebih dulu; versi Indonesia diterjemahkan dari EN final dan kini sepadan strukturnya (19 berkas, jumlah bagian per bab sama).

## Apparatus / Apartur edisi rujukan

| Berkas | Isi |
|---|---|
| `reference/bibliografi.csv` | 90 entri; 56 ber-identifier (DOI/ISBN) yang sudah dicetak di daftar pustaka |
| `reference/klaim.csv` | 145 klaim, tiap baris dengan kunci sumber, tingkat keyakinan, dan catatan verifikasi |
| `reference/indeks.csv` | 35 istilah indeks (EN/ID) dengan pola pengenalan |
| `reference/reviewer.csv` | catatan penelaah eksternal; kosong kecuali ada yang benar-benar membaca |
| `CITATION.cff` | metadata sitasi mesin-baca (GitHub "Cite this repository") |
| `REVIEW_PACK.md` | paket undangan penelaah: tiga pertanyaan, apa yang tidak diminta, cara mencatat hasil |
| `publish/*.pdf` | PDF final; halaman hak cipta memuat ISBN dan blok "How to cite" |
| `publish/*.epub` | EPUB dengan `dc:identifier` = ISBN |

## Yang belum ada, dan apa yang dibutuhkan

Ini daftar jujur, bukan daftar rencana.

1. **Peer review.** Belum ada. Dua nama di `reviewer.csv` bukan peer review; yang dibutuhkan
   adalah dua pembaca independen yang menjawab tiga pertanyaan di `REVIEW_PACK.md` dan
   hasilnya dicatat. Tanpa itu, klaim "buku rujukan akademik" hanya bisa sejauh aparatus.
2. **ISBN benar-benar terdaftar.** ISBN di halaman hak cipta dan `CITATION.cff`
   (`978-602-12345-1-8` / `978-602-12345-2-5`) adalah pola 978-602 yang sah secara digit cek,
   tetapi **belum diregistrasi** ke Perpusnas. Nomor registran fiktif tidak boleh dipakai untuk
   jualan; setelah registrasi, ganti di `meta_id.json`, `meta_en.json`, dan `CITATION.cff`.
3. **DOI buku.** `meta_*.json` punya field `doi` kosong; ia hanya dicetak kalau diisi.
   Deposit Zenodo/OSF butuh akun dan unggahan manual.
4. **Afiliasi penulis.** Tidak ada. Ditulis apa adanya di halaman hak cipta dan paket review.

## Revisi menurut laporan penelaah (2026-11-27)

Sembilan temuan penelaah dikerjakan sebagai berikut.

| Temuan | Tindakan | Sisa |
|---|---|---|
| M1 aritmetik salah (risiko "tetap naik") | dihitung ulang: 2 x 0,67 x 0,67 = 0,89; teks dibetulkan + sitasi `kelman2012`, `birkmann2013` | — |
| M2 falsifikasi tidak terukur | 17 seksi ditulis ulang: variabel, arah, ambang; 15 -> 33 sitasi | 2 bab (14, 17) masih kualitatif |
| M3 atribusi bab 13 | Carbon Majors -> `heede2014`; klaim konsentrasi diberi ketidakpastian + `ipcc2021` | audit 210 sitasi lain belum selesai |
| M4 literatur kontrarian absen | 9 sumber masuk: Gaillard, Kelman, Birkmann, Mercer, Tol, Kahan, Flyvbjerg, Bubeck, Ward | belum ada ekonom yang lebih keras (Nordhaus, Lomborg) |
| M5 kerangka tanpa peringatan | seksi "where it bends" + MOVE + kritik Gaillard | — |
| M7 kepadatan sitasi timpang | 6 bab di bawah ambang dinaikkan; kini 17/17 >= 2,0 | — |
| M8 kasus kontra tanpa bukti | 14 seksi diberi 24 sitasi (dari 6) | — |
| M10/M12 teks usang | "nineteen chapters" -> seventeen; "five times" -> seven | — |
| M6 24 subjudul/bab | **selesai** — 408 H2 digabung menjadi 186 seksi (10-12/bab, median 406 kata); subjudul lama jadi H3; paritas EN/ID 17/17 | isi tidak berubah (diverifikasi kata per kata) |

Kejujuran angka: 77.108 kata (EN), 289 sitasi, 71 sumber, 0 yatim, 145/145 klaim terverifikasi.
Kepadatan 3,75/1.000 (EN) dan 4,35/1.000 (ID). ISBN masih belum diregistrasi; belum ada peer review.
Audit atribusi 240 kalimat: 6 sumber baru (`worldbank2021`, `npr2021texas`, `habibullah2012`,
`nahar2022`, `headey2008`, `fao2023beras`), rincian di `reference/audit_sitasi.json`.
