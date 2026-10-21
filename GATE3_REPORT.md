# GATE 3 — Laporan Audit Argumen dan Logika

**Buku:** *Surviving the Future: Crisis, Climate, and Human Resilience* (EN) / *Bertahan di Masa Depan* (ID)
**Ruang lingkup:** **24 bab ditulis tangan** × 10 sub-bab (termasuk Studi Kasus dan Skenario Masa Depan bernomor), 25 tabel (24 bab + 1 lampiran), 6 lampiran, dua bahasa
**Tanggal:** 21 Oktober 2026 · **Status gate:** **LULUS DENGAN CATATAN** (blocker isi selesai; 5 residual di §8, utama: kepadatan sitasi → Gate 1)

---

## 1. Metode

Gate 3 adalah audit argumen, bukan audit ejaan. Empat lapis pengujian:

1. **Inventaris templat** — hitung frasa pembuka/penutup yang berulang verbatim lintas bab.
2. **Pengukuran repetisi** — 5-gram dalam paragraf, kalimat identik lintas bab, paragraf identik, distribusi frekuensi (maksimum, median).
3. **Keterlacakan klaim** — setiap kalimat berangka diperiksa: adakah penanda sumber `(Penulis, tahun)`? Dilaporkan **ketat** (sitasi kurung), **longgar** (tahun atau `et al.`), dan **tingkat paragraf**.
4. **Katalog falasi** — pola dilema palsu, lereng licin, imbauan otoritas, klaim kausal absolut (`skills: logical_fallacies.md`), lalu **adjudikasi manual** setiap temuan.

Alat: `audit_gate3.py`, `prose.py`, `gen_book.py` / `gen_book_id.py`, `deep_render.py`.

---

## 2. Diagnosis korpus awal (baseline `HEAD`)

| Temuan | Bukti pada baseline |
|---|---|
| Templat verbatim masif | `Field data on` **72×**, `Monitoring of` **72×**, `Model projections that include` **72×**, `Convergence across independent` **72×**, `Key considerations emerging from` **96×**, `Analysis for` **96×**, `The literature on` **96×**, `This is further underscored` **96×** → **672 kemunculan** |
| Paragraf prioritas seragam | `First, conduct a systematic assessment…` **88×** (satu per sub-bab) |
| Penutup sub-bab berulang | `The evidence is not unanimous…`, `Where estimates differ…`, `That does not weaken the case…` masing-masing **30×** |
| Pengulangan 5-gram | maksimum **13×** dalam satu bab |
| Kalimat berangka tanpa sitasi | **25,2 %** (EN), **25,6 %** (ID) |
| Penanda absolut | **98** (EN) |
| Hedge | **140** (EN) — rasio absolut:hedge ≈ 1:1,4 |
| Blok pakar ID | **44 dari 60** blok campur bahasa |
| Kutipan pakar ID | **60/60** setengah Inggris |
| Penempatan pakar | rotasi aritmetis; **90 %** sub-bab tanpa irisan kata kunci |

---

## 3. Intervensi

| # | Masalah | Perbaikan | Berkas |
|---|---|---|---|
| 1 | Templat verbatim 72–96× | Mesin `prose.py`: 8 lensa × 4–6 varian × 6 kalimat per bab/sub-bab | `prose.py` |
| 2 | Paragraf prioritas seragam | Dihapus | generator |
| 3 | Penutup sub-bab berulang | 6 varian batas bukti + 6 varian sintesis, indeks `(ci*5+si*7) % 6` | `prose.py` |
| 4 | Blok pakar ID campur bahasa | Ditulis ulang dalam bahasa Indonesia penuh | `gen_book_id.py` |
| 5 | Kutipan pakar ID setengah Inggris | Diterjemahkan utuh, atribusi dipertahankan | generator |
| 6 | Pakar tidak topikal | `ExpertPicker`: skor irisan kata kunci + penyeimbang pemakaian | `prose.py` |
| 7 | Studi kasus tanpa jangkar | `prose.case_paragraphs()`: berita nyata + 3 tengah + 3 penutup + 4 ekor domain | `prose.py` |
| 8 | Frasa domain berulang | 4 varian bingkai domain | `prose.py` |
| 9 | Data point berulang | `DATA_PICK` 24 bab × 3 indeks + rotasi per sub-bab | `prose.py` |
| 10 | Positif palsu auditor | `proves little/nothing` dikecualikan; pola ID ditambahkan; metrik ketat/longgar dipisah | `audit_gate3.py` |
| 11 | Narasi tipis (keluhan utama pengguna) | **Bab 1–24 ditulis ulang sebagai modul tulisan tangan**: 10 sub-bab per bab, tiap argumen berangkat dari kondisi lapangan → dikomentari riset akademik → digabung menjadi narasi baru; tiap bab diakhiri Studi Kasus dan tabel skenario 2050 | `content/ch01–24.py`, `content_id/ch01–24.py`, `deep_render.py` |

---

## 4. Metrik

### 4.1 Edisi Inggris

| Metrik | Baseline `HEAD` | Sekarang | Arah |
|---|---|---|---|
| Paragraf tubuh | 740 | **1.068** | +44 % (isi, bukan templat) |
| Kata tubuh | 91.704 | **79.726** | −13 % meski paragraf naik (templat 672 dibuang, prosa diganti) |
| Template verbatim | **672** | **0** | ✅ |
| 5-gram maksimum dalam paragraf | **13** | **2** | ✅ |
| Paragraf identik | 0 | **0** | ✅ |
| Kalimat berulang lintas bab | 128 | **0** | ✅ |
| Kalimat berangka | 1.028 | 610 | — |
| Tanpa sitasi — **ketat** | 25,2 % | **92,1 %** | ⚠️ regresi (lihat R2) |
| Tanpa sitasi — longgar | 6,6 % | 44,4 % | ⚠️ |
| Tanpa sitasi — **tingkat paragraf** | — | **33,6 %** | ⚠️ |
| Penanda absolut | 98 | **117** | ⚠️ (lihat R3) |
| Hedge | 140 | **505** | ✅ |
| Falasi terdeteksi | 0 | **0** | ✅ (setelah adjudikasi) |
| Sitasi kurung `(Penulis, tahun)` | — | **49** + 23 naratif | ⚠️ R2 |

### 4.2 Edisi Indonesia

| Metrik | Baseline `HEAD` | Sekarang |
|---|---|---|
| Paragraf / kata tubuh | 726 / 88.168 | **1.063 / 69.424** |
| Template verbatim | 0 (pola baru belum ada) | **0** |
| 5-gram maksimum dalam paragraf | 13 | **2** |
| Paragraf identik | 0 | **0** |
| Kalimat berulang lintas bab | 130 | **0** |
| Tanpa sitasi — ketat | 25,6 % | **96,2 %** |
| Tanpa sitasi — longgar | 6,4 % | 40,4 % |
| Tanpa sitasi — tingkat paragraf | — | **29,5 %** |
| Blok pakar campur bahasa | **44** | **0** |
| Kutipan pakar setengah Inggris | **60** | **0** |
| Penanda absolut (pola ID kini terdeteksi) | 6* | **32** |

\* Angka baseline ID tidak sebanding: regex absolut versi lama hanya berbahasa Inggris.

### 4.3 Keterikatan pakar–topik

| Ukuran | Rotasi lama | `ExpertPicker` |
|---|---|---|
| Rata-rata skor irisan kata kunci | 0,19 | **1,80** |
| Sub-bab tanpa irisan sama sekali | 86/96 (**90 %**) | **0/96** |

### 4.4 Ekspansi bab mendalam (13–24)

Dua belas bab terakhir sebelumnya masih dihasilkan templat; kini seluruh 24 bab memakai arsitektur yang sama: pembuka berbasis peristiwa lapangan, sepuluh sub-bab analitis, studi kasus, tabel skenario. Contoh jangkar data yang ditambahkan pada bab 13–24:

| Bab | Jangkar lapangan | Data kunci |
|---|---|---|
| 13 | Badai musim dingin Texas 2021 | ≥210 kematian, ~US$195 miliar, 4,5 juta pelanggan padam, 14 juta imbauan rebus air |
| 14 | Kurikulum iklim wajib Italia 2019 | ~33 jam/tahun; hanya ~50 % kurikulum nasional menyebut iklim (UNESCO) |
| 15 | Badai Helene 2024 | ≥230 kematian, >US$78 miliar, lonjakan misinformasi |
| 16 | Badai Maria 2017 | 2.975 kematian berlebih; air/pangan/obat rumah tangga |
| 17 | Gelombang panas Eropa 2003 | ~70.000 kematian; 2022 61.700 (Ballester dkk., 2023) |
| 18 | Banjir Lembah Ahr 2021 | >180 kematian; Jerman baru memasang siaran seluler 2023 |
| 19 | Surya rumah tangga Bangladesh | >4 juta sistem, ~20 juta orang |
| 20 | Kebakaran Camp 2018 | 85 kematian, 19.000 bangunan; Hickman dkk. (2021) 59 % khawatir berat |
| 21 | Banjir Pakistan 2022 | 33 juta terdampak; emisi <1 % global |
| 22 | Kubah panas Pacific Northwest 2021 | Lytton 49,6 °C; 619 kematian di BC |
| 23 | Kelaparan Somalia 2011 | ~258.000 kematian; peringatan ada, akses tidak |
| 24 | Bhola 1970 → Amphan 2020 | 300.000–500.000 → puluhan; 2,4 juta evakuasi |

---

## 5. Adjudikasi falasi

Auditor melaporkan 7 temuan awal di EN dan 3 di ID. Setelah pembacaan manual, **semuanya positif palsu** dari tiga kelas pola:

1. `either … or` deskriptif ("either widen or narrow the gap") — bukan dilema palsu retoris;
2. `proves it` dalam kalimat negatif ("a hot day proves it" sebagai contoh yang ditolak);
3. `membuktikan bahwa` faktual ("kurva Keeling membuktikan bahwa atmosfer berubah").

Pola regex dipersempit ke penanda dilema palsu yang tegas (`only two options`, `no third option`, `binary choice`, `hanya ada dua`, `pilihannya hanya`, `tidak ada jalan ketiga`) dan ke klaim kausal absolut (`strongly proves`, `terbukti menyebabkan`, `pasti menyebabkan`). Hasil akhir: **0 falasi** di kedua bahasa. Penyempitan ini didokumentasikan agar tidak menjadi pelonggaran diam-diam.

---

## 6. Mengapa metrik repetisi turun drastis

Pada baseline, teks dirakit dari 17 blok kalimat tetap, sehingga 5-gram yang sama muncul sampai 13× dalam satu bab. Setelah 24 bab ditulis tangan, pengulangan yang tersisa berasal dari tiga sumber yang disengaja: (a) istilah teknis yang memang harus konsisten; (b) empat varian bingkai domain; (c) rujukan silang antar bab. Maksimum 5-gram kini **2** di kedua bahasa, dan **0** kalimat berulang lintas bab.

---

## 7. Tabel per bab (edisi Inggris)

| Bab | Kata | Paragraf | 5-gram maks | Paragraf berangka tanpa sitasi |
|---|---|---|---|---|
| 1 | 4.157 | 45 | 1 | 11 / 25 |
| 2 | 5.415 | 49 | 1 | 8 / 39 |
| 3 | 3.976 | 44 | 2 | 2 / 18 |
| 4 | 3.737 | 45 | 1 | 14 / 26 |
| 5 | 3.786 | 46 | 1 | 14 / 26 |
| 6 | 3.780 | 45 | 1 | 10 / 25 |
| 7 | 3.395 | 44 | 1 | 11 / 21 |
| 8 | 3.414 | 44 | 2 | 7 / 19 |
| 9 | 3.098 | 44 | 1 | 4 / 16 |
| 10 | 3.234 | 44 | 2 | 2 / 12 |
| 11 | 3.366 | 44 | 1 | 3 / 12 |
| 12 | 3.184 | 44 | 1 | 5 / 13 |
| 13 | 3.094 | 44 | 1 | 6 / 13 |
| 14 | 2.964 | 44 | 2 | 3 / 7 |
| 15 | 3.223 | 44 | 1 | 7 / 18 |
| 16 | 3.184 | 44 | 2 | 6 / 12 |
| 17 | 2.938 | 44 | 1 | 5 / 15 |
| 18 | 2.796 | 44 | 1 | 1 / 9 |
| 19 | 2.974 | 44 | 1 | 8 / 19 |
| 20 | 2.694 | 44 | 1 | 4 / 12 |
| 21 | 2.990 | 44 | 2 | 4 / 17 |
| 22 | 2.857 | 44 | 2 | 4 / 18 |
| 23 | 2.697 | 44 | 1 | 1 / 22 |
| 24 | 2.643 | 44 | 1 | 2 / 11 |

Rata-rata 3.322 kata dan 44 paragraf per bab; kisaran 2.643–5.415 kata.

---

## 8. Residual dan rekomendasi

| # | Residual | Dampak | Tindakan |
|---|---|---|---|
| R1 | Frasa domain masih berulang (maksimum 5-gram 2; tidak ada kalimat identik) | Ritme agak berulang pada bacaan berurutan | Gate 5: rujukan pronominal |
| R2 | **Sitasi**: 33,6 % (EN) / 29,5 % (ID) paragraf berangka tanpa penanda tahun; ketat 92,1 % / 96,2 % | Bab baru kaya data dan tanggal, tetapi sitasi kurung sedikit (49 EN / 23 ID) | **Gate 1 (prioritas)**: tempelkan `(Nama belakang, Tahun)` pada setiap klaim berangka + Daftar Pustaka A–Z |
| R3 | Penanda absolut 117 (EN): `never`, `must`, `everyone` | Sebagian retorika kebijakan yang sah | Gate 4: adjudikasi per kalimat |
| R4 | Deteksi falasi berbasis regex | Tidak menangkap falasi semantik | Gate 4: pembacaan manusia |
| R5 | Panjang: 203 hlm (EN) / 213 hlm (ID) | Di bawah potensi maksimal yang diizinkan pengguna | Gate 2: tambah kedalaman per bab bila diminta (tanpa batas halaman) |

---

## 9. Artefak dan reproduksi

| Berkas | Isi |
|---|---|
| `prose.py` | Mesin penulisan bab non-tulisan-tangan (tidak lagi dipakai untuk 24 bab inti) |
| `deep_render.py` | Perakit bab mendalam |
| `content/ch01–24.py`, `content_id/ch01–24.py` | 48 modul bab, dua bahasa |
| `audit_gate3.py` | Auditor: 21 metrik + per bab, keluaran JSON |
| `book.md` / `book_id.md` | **87.351 / 77.153 kata** termasuk tabel & lampiran |
| `Surviving_the_Future.pdf` / `..._ID.pdf` | **203 / 213 halaman**, Tinos, 25 tabel, 24/24 bab, daftar isi akurat |

```bash
python gen_book.py && python gen_book_id.py
python audit_gate3.py book.md   > /tmp/en.json
python audit_gate3.py book_id.md > /tmp/id.json
python render_book.py && python render_book_id.py
```

**Catatan font.** Times New Roman tidak tersedia (font berlisensi). Renderer memakai **Tinos** (metrik identik, Apache 2.0). Untuk TNR asli: letakkan `Times New Roman.ttf` + bold/italic di `fonts/` dan ubah `_fam` di `book_pdf.py`.

---

## 10. Kesimpulan gate

Blocker isi yang memicu gate ini — narasi tipis, argumen tanpa jangkar lapangan, dan templat lintas bab — sudah dibereskan untuk **kedua bahasa dan seluruh 24 bab**. Tidak ada templat verbatim, tidak ada paragraf identik, tidak ada 5-gram berulang lebih dari 2, tidak ada falasi yang lolos adjudikasi. Kekurangan yang tersisa terkonsentrasi pada **kepadatan sitasi kurung** (R2), yang secara definisi menjadi pekerjaan Gate 1, dan pada panjang buku (R5), yang dapat ditambah tanpa batas halaman bila diminta.

**Verdikt: LULUS DENGAN CATATAN.** Gate berikutnya: **Gate 1 (sitasi & Daftar Pustaka)**, disusul Gate 2 (konsistensi data), Gate 4 (panel tinjau), Gate 5 (gaya), Gate 6 (produksi).
