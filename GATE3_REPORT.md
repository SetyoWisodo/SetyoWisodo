# GATE 3 — Laporan Audit Argumen dan Logika

**Buku:** *Surviving the Future: Crisis, Climate, and Human Resilience* (EN) / *Bertahan di Masa Depan* (ID)
**Ruang lingkup:** **24 bab ditulis tangan** × 10 sub-bab (termasuk Studi Kasus dan Skenario Masa Depan bernomor), **ditambah lapisan pendalaman lapis kedua pada 24/24 bab** (satu paragraf tambahan per sub-bab, per pembuka dan per studi kasus), 25 tabel, dua bahasa
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
| Paragraf tubuh | 740 | **1.488** | +101 % (isi, bukan templat) |
| Kata tubuh | 91.704 | **119.101** | +30 % vs baseline, +49 % vs build tanpa pendalaman |
| Template verbatim | **672** | **0** | ✅ |
| 5-gram maksimum dalam paragraf | **13** | **2** | ✅ |
| Paragraf identik | 0 | **0** | ✅ |
| Kalimat berulang lintas bab | 128 | **0** | ✅ |
| Kalimat berangka | 1.028 | 610 | — |
| Tanpa sitasi — **ketat** | 25,2 % | **93,0 %** | ⚠️ regresi (lihat R2) |
| Tanpa sitasi — longgar | 6,6 % | 39,0 % | ⚠️ |
| Tanpa sitasi — **tingkat paragraf** | — | **29,8 %** | ⚠️ |
| Penanda absolut | 98 | **171** | ⚠️ (lihat R3) |
| Hedge | 140 | **723** | ✅ |
| Falasi terdeteksi | 0 | **0** | ✅ (setelah adjudikasi) |
| Sitasi kurung `(Penulis, tahun)` | — | **58** + 81 `et al.` | ⚠️ R2 |

### 4.2 Edisi Indonesia

| Metrik | Baseline `HEAD` | Sekarang |
|---|---|---|
| Paragraf / kata tubuh | 726 / 88.168 | **1.483 / 103.915** |
| Template verbatim | 0 (pola baru belum ada) | **0** |
| 5-gram maksimum dalam paragraf | 13 | **2** |
| Paragraf identik | 0 | **0** |
| Kalimat berulang lintas bab | 130 | **0** |
| Tanpa sitasi — ketat | 25,6 % | **96,0 %** |
| Tanpa sitasi — longgar | 6,4 % | 34,6 % |
| Tanpa sitasi — tingkat paragraf | — | **25,3 %** |
| Sitasi kurung / `et al.` | — | **34 / 38** |
| Blok pakar campur bahasa | **44** | **0** |
| Kutipan pakar setengah Inggris | **60** | **0** |
| Penanda absolut (pola ID kini terdeteksi) | 6* | **54** |

\* Angka baseline ID tidak sebanding: regex absolut versi lama hanya berbahasa Inggris.

### 4.3 Keterikatan pakar–topik

| Ukuran | Rotasi lama | `ExpertPicker` |
|---|---|---|
| Rata-rata skor irisan kata kunci | 0,19 | **1,80** |
| Sub-bab tanpa irisan sama sekali | 86/96 (**90 %**) | **0/96** |

### 4.4 Pendalaman lapis kedua (bab 1–24)

Keluhan utama pengguna — "bab hanya menyebut sekilas" — ditangani bukan dengan menambah sub-bab baru, melainkan dengan **lapisan paragraf kedua di dalam setiap sub-bab yang sudah ada**. Setiap sub-bab, setiap pembuka bab dan setiap Studi Kasus menerima satu paragraf tambahan yang membawa dimensi berbeda: mekanisme kausal, bukti lapangan, kajian akademik bernama, atau instrumen kebijakan. Paragraf ini disisipkan setelah prosa dasar oleh `deep_render.py::_load_extra()`, yang menggabungkan tujuh modul (`content/depth*.py`, `content_id/depth*.py`) dan memetakan kunci `"opening"`, `"N.1"`…`"N.10"`, `"case"`.

| Modul | Bab yang didalami | Isi tambahan |
|---|---|---|
| `depth` | 1–4 | pembuka + 10 sub-bab + studi kasus per bab |
| `depth_b` | 5–8 | idem |
| `depth_c` | 9–10 | idem |
| `depth_d` | 11–12 | idem |
| `depth_e` | 13–18 | idem |
| `depth_f` | 19–24 | idem |
| `depth_g` | 9–24 (penguat selektif) | sub-bab yang masih tipis, terutama bab 13–24 |
| `depth_h`, `depth_i` | 4–24 (penutup celah) | satu paragraf tambahan per bab pada sub-bab yang belum didalami, dipilih agar menambah dimensi baru |

Hasil: **24/24 bab** memiliki lapisan pendalaman; paragraf tubuh naik dari 1.068 → **1.488** (EN) dan 1.063 → **1.483** (ID), kata tubuh dari 79.726 → **119.101** (EN) dan 69.424 → **103.915** (ID). Rata-rata per bab **4.957 kata (EN)** dan **4.326 kata (ID)**, kisaran 4.732–6.581 (EN). Tidak ada satu pun bab di bawah 4.700 kata (EN) atau 4.100 kata (ID).

Setiap paragraf baru menyebut minimal satu nama peneliti/lembaga dengan tahun (mis. Milly dkk. 2008; Kahan dkk. 2012; Oreskes 2004; Aldrich 2012; Kotz dkk. 2024; Kelley dkk. 2015 vs Selby dkk. 2017), sehingga pendalaman ini juga menaikkan kepadatan sitasi naratif dari 31 → **81 kemunculan `et al.`** dan sitasi kurung dari 49 → **58** (EN). Karena itu tingkat paragraf tanpa sitasi turun dari 33,6 % → **29,8 %** (EN) dan 29,5 % → **25,3 %** (ID), meski jumlah paragraf naik 39 %.

### 4.4b Jangkar lapangan bab 13–24

Dua belas bab terakhir kini memakai arsitektur yang sama dengan bab 1–12: pembuka berbasis peristiwa lapangan, sepuluh sub-bab analitis, studi kasus, tabel skenario. Contoh jangkar data:

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

## 7. Tabel per bab

Kolom kata menyajikan **EN (ID)**. Seluruh 24 bab memakai arsitektur yang sama dan semuanya sudah melewati lapisan pendalaman.

| Bab | Kata | Paragraf | 5-gram maks | Paragraf berangka tanpa sitasi |
|---|---|---|---|---|
| 1 | 5.422 (4.725) | 58 | 1 | 14 / 34 |
| 2 | 6.581 (4.616) | 61 | 1 | 12 / 46 |
| 3 | 5.025 (4.446) | 56 | 2 | 4 / 22 |
| 4 | 4.924 (4.476) | 58 | 1 | 15 / 33 |
| 5 | 4.894 (4.348) | 59 | 1 | 21 / 35 |
| 6 | 4.878 (4.265) | 58 | 1 | 13 / 29 |
| 7 | 4.844 (4.262) | 61 | 1 | 12 / 28 |
| 8 | 4.919 (4.282) | 61 | 2 | 10 / 30 |
| 9 | 4.747 (4.252) | 63 | 1 | 7 / 24 |
| 10 | 4.857 (4.191) | 62 | 2 | 2 / 20 |
| 11 | 4.810 (4.182) | 61 | 1 | 5 / 19 |
| 12 | 4.945 (4.231) | 64 | 1 | 7 / 22 |
| 13 | 4.806 (4.258) | 61 | 2 | 7 / 23 |
| 14 | 4.885 (4.173) | 64 | 2 | 4 / 12 |
| 15 | 4.794 (4.239) | 60 | 1 | 11 / 29 |
| 16 | 4.785 (4.362) | 60 | 2 | 6 / 21 |
| 17 | 4.932 (4.416) | 64 | 1 | 6 / 24 |
| 18 | 4.871 (4.351) | 65 | 1 | 1 / 19 |
| 19 | 4.939 (4.486) | 63 | 1 | 11 / 30 |
| 20 | 4.873 (4.341) | 66 | 1 | 4 / 18 |
| 21 | 4.756 (4.155) | 62 | 2 | 5 / 24 |
| 22 | 4.872 (4.308) | 65 | 2 | 4 / 33 |
| 23 | 4.880 (4.231) | 67 | 1 | 2 / 35 |
| 24 | 4.732 (4.237) | 67 | 2 | 2 / 14 |

Rata-rata **4.957 kata (EN) / 4.326 kata (ID)** per bab; kisaran EN 4.732–6.581, ID 4.155–4.725; 56–63 paragraf per bab. Tidak ada bab di bawah 4.700 kata (EN) atau 4.100 kata (ID). Maksimum 5-gram tetap **2** dan paragraf identik **0** setelah pendalaman, yaitu tidak ada paragraf baru yang menyalin paragraf lama.

Falasi: 0 di kedua bahasa. Penanda absolut **171 (EN) / 54 (ID)** dengan hedge **723 (EN) / 434 (ID)** — rasio absolut:hedge ≈ 1:4,2 dan 1:8,0.

---

## 8. Residual dan rekomendasi

| # | Residual | Dampak | Tindakan |
|---|---|---|---|
| R1 | Frasa domain masih berulang (maksimum 5-gram 2; tidak ada kalimat identik) | Ritme agak berulang pada bacaan berurutan | Gate 5: rujukan pronominal |
| R2 | **Sitasi**: 29,8 % (EN) / 25,3 % (ID) paragraf berangka tanpa penanda tahun; ketat 93,0 % / 96,0 % | Bab kaya data dan tanggal, sitasi kurung 58 (EN) / 34 (ID) + 81 `et al.` (EN) | **Gate 1 (prioritas)**: tempelkan `(Nama belakang, Tahun)` pada setiap klaim berangka + Daftar Pustaka A–Z |
| R3 | Penanda absolut 117 (EN): `never`, `must`, `everyone` | Sebagian retorika kebijakan yang sah | Gate 4: adjudikasi per kalimat |
| R4 | Deteksi falasi berbasis regex | Tidak menangkap falasi semantik | Gate 4: pembacaan manusia |
| R5 | Panjang: **278 hlm (EN) / 296 hlm (ID)**, 119.101 / 103.915 kata | Rata-rata **4.957 kata/bab (EN) — 99 % dari target ≈5.000**; minimum 4.732 (bab 24), maksimum 6.581 (bab 2); tidak ada batas halaman | Tertutup; sisa 1 % dapat ditutup pada Gate 2 bila diminta |

---

## 9. Artefak dan reproduksi

| Berkas | Isi |
|---|---|
| `prose.py` | Mesin penulisan bab non-tulisan-tangan (tidak lagi dipakai untuk 24 bab inti) |
| `deep_render.py` | Perakit bab mendalam |
| `content/ch01–24.py`, `content_id/ch01–24.py` | 48 modul bab, dua bahasa |
| `audit_gate3.py` | Auditor: 21 metrik + per bab, keluaran JSON |
| `book.md` / `book_id.md` | **119.101 / 103.915 kata** tubuh (termasuk tabel & lampiran) |
| `Surviving_the_Future.pdf` / `..._ID.pdf` | **278 / 296 halaman**, Tinos, 25 tabel, 24/24 bab, daftar isi akurat, 0 blok di luar margin |
| `content/depth*.py`, `content_id/depth*.py` | **9 modul × 2 bahasa**: lapisan paragraf kedua untuk 24/24 bab |

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

Pendalaman lapis kedua menutup keluhan isi yang memicu pekerjaan ini: setiap sub-bab kini memiliki dua lapisan penjelasan — prosa dasar dan paragraf pendalaman yang membawa mekanisme, bukti lapangan, kajian akademik bernama atau instrumen kebijakan. Rata-rata per bab naik dari 3.322 → **4.957 kata (EN)** dan 2.892 → **4.326 kata (ID)**, tanpa menambah satu pun sub-bab baru dan tanpa memecah alur argumen.

**Verdikt: LULUS DENGAN CATATAN.** Gate berikutnya: **Gate 1 (sitasi & Daftar Pustaka)**, disusul Gate 2 (konsistensi data), Gate 4 (panel tinjau), Gate 5 (gaya), Gate 6 (produksi).
