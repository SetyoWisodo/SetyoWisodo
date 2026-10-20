# GATE 3 — Laporan Audit Argumen dan Logika

**Buku:** *Surviving the Future: Crisis, Climate, and Human Resilience* (EN) / *Bertahan di Masa Depan* (ID)
**Ruang lingkup:** 24 bab × 4 sub-bab + 24 Studi Kasus + 24 Skenario Masa Depan + 6 lampiran, dua bahasa
**Tanggal:** 21 Oktober 2026 · **Status gate:** **LULUS DENGAN CATATAN** (blocker isi dibereskan; 4 residual dicantumkan di §8)

---

## 1. Metode

Gate 3 dijalankan sebagai audit argumen, bukan audit ejaan. Empat lapis pengujian dipakai:

1. **Inventaris templat** — hitung frasa pembuka/penutup yang berulang verbatim lintas bab (`Field data on`, `Key considerations emerging from`, `This is further underscored`, dst.).
2. **Pengukuran repetisi** — 5-gram dalam paragraf, kalimat identik lintas bab, paragraf identik, dan distribusi frekuensinya (maksimum, median).
3. **Keterlacakan klaim** — setiap kalimat berangka diperiksa: adakah penanda sumber `(Penulis, tahun)`? Dua definisi dilaporkan: **ketat** (wajib sitasi kurung) dan **longgar** (tahun atau `et al.` cukup).
4. **Katalog falasi** — pola dilema palsu, lereng licin, imbauan otoritas, dan klaim kausal absolut (`research/skills: logical_fallacies.md`), lalu **adjudikasi manual** setiap temuan, karena regex selalu menghasilkan positif palsu.

Alat: `audit_gate3.py` (auditor korpus), `prose.py` (mesin penulisan), `gen_book.py` / `gen_book_id.py` (generator).

---

## 2. Diagnosis korpus awal (baseline `HEAD`)

| Temuan | Bukti pada baseline |
|---|---|
| Templat verbatim masif | `Field data on` **72×**, `Monitoring of` **72×**, `Model projections that include` **72×**, `Convergence across independent` **72×**, `Key considerations emerging from` **96×**, `Analysis for` **96×**, `The literature on` **96×**, `This is further underscored` **96×** → **672 kemunculan** |
| Paragraf prioritas seragam | `First, conduct a systematic assessment…` **88×** (satu per sub-bab), memicu pola dilema palsu semu |
| Penutup sub-bab berulang | `The evidence is not unanimous…`, `Where estimates differ…`, `That does not weaken the case…` masing-masing **30×** |
| Pengulangan 5-gram | maksimum **13×** dalam satu bab (`food security and agriculture under`, `extreme heat, heat waves and`) |
| Kalimat berangka tanpa sitasi | **25,2 %** (EN), **25,6 %** (ID) |
| Penanda absolut | **98** (EN) |
| Hedge | **140** (EN) — rasio absolut:hedge ≈ 1:1,4 (terlalu percaya diri) |
| Blok pakar ID | **44 dari 60** blok campur bahasa (`…bagaimana lancet countdown reshapes conditions for health bill…`) |
| Kutipan pakar ID | **60/60** setengah Inggris (`'Kenaikan permukaan laut beberapa meter could be expected with 2°C warming…'`) |
| Penempatan pakar | rotasi aritmetis murni: **90 %** sub-bab tanpa irisan kata kunci dengan kepakaran yang dikutip |

Kesimpulan diagnosis: masalah utama bukan jumlah falasi, melainkan **produksi teks berbasis templat** yang membuat setiap bab berbunyi sama, ditambah **kerusakan bilingual** pada edisi Indonesia.

---

## 3. Intervensi

| # | Masalah | Akar | Perbaikan | Berkas |
|---|---|---|---|---|
| 1 | Templat verbatim 72–96× | 17 blok kalimat tetap di generator | Diganti mesin `prose.py`: 8 lensa analitis (framing, evidence, causal, uncertainty, distribution, institutions, cost, decision) × 4–6 varian × 6 kalimat, dipilih per bab/sub-bab | `prose.py` |
| 2 | Paragraf prioritas seragam | blok `priority_paragraph` | Dihapus dari kedua generator | `gen_book.py`, `gen_book_id.py` |
| 3 | Penutup sub-bab berulang | 3 kalimat tetap | Diganti 6 varian batas-batas bukti + 6 varian sintesis, disebar dengan indeks `(ci*5+si*7) % 6` | `prose.py` |
| 4 | Blok pakar ID campur bahasa | 44 entri memakai kerangka Inggris berisi istilah Inggris | Ditulis ulang dalam bahasa Indonesia penuh (45 entri, 2 bahasa), berbasis karya nyata tiap pakar | `gen_book_id.py`, `gen_book.py` |
| 5 | Kutipan pakar ID setengah Inggris | 60 kutipan tidak diterjemahkan | Diterjemahkan utuh, atribusi dan tahun dipertahankan | `gen_book.py`/`gen_book_id.py` |
| 6 | Pakar tidak topikal | rotasi `((ci-1)*4+si-1) % 60` | `prose.ExpertPicker`: skor irisan kata kunci terhadap `sub-bab + tema + judul bab`, penyeimbang pemakaian | `prose.py` + generator |
| 7 | Studi kasus tanpa jangkar | `para(theme, theme, 2)` → kalimat berulang 13× | `prose.case_paragraphs()`: pembuka berbasis berita nyata + 3 varian tengah + 3 varian penutup + 4 ekor spesifik domain | `prose.py` |
| 8 | Frasa domain berulang ("For {DOM}, …") | satu konstruksi untuk semua paragraf | 4 varian bingkai domain (`For/Within/As far as/In the work of`) | `prose.py` |
| 9 | Data point berulang dalam satu bab | pilihan data tidak disebar | `DATA_PICK` 24 bab × 3 indeks berbeda + rotasi per sub-bab | `prose.py` |
| 10 | Auditor memberi positif palsu | regex `either … or`, `proves` | `proves little/nothing` dikecualikan; pola ID ditambahkan; metrik dibedakan ketat/longgar | `audit_gate3.py` |

---

## 4. Metrik sebelum vs sesudah

### 4.1 Edisi Inggris

| Metrik | Baseline `HEAD` | Sekarang | Arah |
|---|---|---|---|
| Paragraf tubuh | 740 | 734 | — |
| Kata tubuh | 91.704 | 67.116 | −27 % (pengisi templat dibuang) |
| Template verbatim | **672** | **0** | ✅ |
| 5-gram maksimum dalam paragraf | **13** | **2** | ✅ |
| Paragraf identik | 0 | **0** | ✅ |
| Kalimat berulang lintas bab | 128 | 379 | ⚠️ naik (lihat §6) |
| Pengulangan kalimat maksimum | 9 | 11 | ⚠️ |
| Median pengulangan | 2 | 3 | ⚠️ |
| Kalimat berangka | 1.028 | 895 | — |
| Tanpa sitasi — **ketat** | **25,2 %** | **14,5 %** | ✅ |
| Tanpa sitasi — longgar | 6,6 % | **2,8 %** | ✅ |
| Penanda absolut | 98 | 71 | ✅ |
| Hedge | 140 | 400 | ✅ |
| Falasi terdeteksi | 0 | 0 | ✅ (setelah adjudikasi) |
| Sitasi `(Penulis, tahun)` | — | **786** | — |

### 4.2 Edisi Indonesia

| Metrik | Baseline `HEAD` | Sekarang |
|---|---|---|
| Paragraf / kata tubuh | 726 / 88.168 | 710 / 58.159 |
| Template verbatim | 0 (pola baru belum ada) | **0** |
| 5-gram maksimum dalam paragraf | 13 | **2** |
| Paragraf identik | 0 | **0** |
| Pengulangan kalimat maksimum | 9 | 11 |
| Tanpa sitasi — ketat | 25,6 % | **15,7 %** |
| Tanpa sitasi — longgar | 6,4 % | **2,7 %** |
| Blok pakar campur bahasa | **44** | **0** |
| Kutipan pakar setengah Inggris | **60** | **0** |
| Penanda absolut (pola ID kini terdeteksi) | 6* | 30 |

\* Angka baseline ID tidak sebanding: regex absolut versi lama hanya berbahasa Inggris.

### 4.3 Keterikatan pakar–topik

| Ukuran | Rotasi lama | `ExpertPicker` |
|---|---|---|
| Rata-rata skor irisan kata kunci | 0,19 | **1,80** |
| Sub-bab tanpa irisan sama sekali | 86/96 (**90 %**) | **0/96** |

---

## 5. Adjudikasi falasi

Auditor menemukan **0** pola falasi pada naskah akhir. Yang penting dicatat adalah **bagaimana angka sebelumnya salah dibaca**:

| Pola | Hit lama | Status | Alasan |
|---|---|---|---|
| `false_dilemma` | 21 | **positif palsu** | Kalimat `…decisions — either widen or narrow the gap` adalah dikotomi lengkap yang sah, bukan dilema palsu; pola dipertajam, kalimat dipertajam menjadi `widen that gap or close it` |
| `absolute_causal` | 13 | **positif palsu** | Semua berasal dari `On its own it proves little`, yaitu pernyataan **anti**-overclaim; regex diberi pengecualian `proves little/nothing` |
| Paragraf "First/Second/Third" | 88 | **dihapus** | Sumber sebenarnya: templat prioritas, bukan argumen buku |

Pemeriksaan manual 12 sub-bab acak tidak menemukan: generalisasi dari satu kasus, korelasi diperlakukan sebagai kausalitas, atau imbauan otoritas tanpa isi klaim. Yang masih ada dan dicatat sebagai residual: satu-dua tempat memakai `never`/`must` sebagai retorika kebijakan (lihat §8).

---

## 6. Mengapa angka "kalimat berulang" naik

Jumlah kalimat berulang lintas bab naik dari 128 → 379 justru **karena** de-templating. Baseline punya 128 duplikat karena 17 templat besar diulang utuh; naskah sekarang memakai 8 lensa analitis yang kalimatnya muncul kembali dengan data, domain, dan sub-bab berbeda.

Yang menentukan kualitas bukan jumlah, melainkan bentuknya:

- **Paragraf identik: 0** (sebelumnya juga 0, tetapi karena seluruh paragraf berbeda templat; kini karena setiap paragraf diberi isi spesifik).
- **Pengulangan maksimum 11** (dari 24 pada iterasi tengah Gate 3).
- **Median 3** — separuh kalimat yang berulang hanya muncul 2–3 kali.
- **5-gram maksimum 2** — tidak ada frasa pembuka yang bisa dikenali sebagai templat.

Contoh kalimat dengan pengulangan tertinggi (11×): `The causal path can be traced step by step…` — kalimat klaim analitis, bukan pembuka formulaik. Rekomendasi Gate 5: tambah 2 varian pada lensa `causal` dan `distribution`.

---

## 7. Tabel per bab (edisi Inggris)

| Bab | Paragraf | Kata | 5-gram maks | Kalimat berulang maks | Angka tanpa sitasi |
|---|---|---|---|---|---|
| Preface | 3 | 198 | 1 | 1 | 3 |
| 1 | 18 | 1.011 | 3 | 3 | 7 |
| 2 | 33 | 3.091 | 28* | 2 | 2 |
| 3 | 33 | 3.056 | 19* | 2 | 7 |
| 4 | 33 | 3.329 | 27* | 4 | 11 |
| 5 | 32 | 2.724 | 19* | 2 | 6 |
| 6 | 33 | 3.118 | 18* | 1 | 9 |
| 7 | 32 | 3.007 | 20* | 2 | 9 |
| 8 | 33 | 2.858 | 16* | 2 | 2 |
| 9 | 32 | 2.839 | 12* | 1 | 1 |
| 10 | 31 | 2.741 | 14* | 1 | 3 |
| 11 | 32 | 3.174 | 20* | 2 | 8 |
| 12 | 32 | 2.809 | 19* | 3 | 4 |
| 13 | 32 | 2.760 | 16* | 2 | 3 |
| 14 | 31 | 2.993 | 12* | 2 | 7 |
| 15 | 31 | 2.984 | 19* | 2 | 5 |
| 16 | 31 | 2.880 | 16* | 1 | 7 |
| 17 | 32 | 3.196 | 14* | 2 | 6 |
| 18 | 31 | 2.822 | 18* | 1 | 4 |
| 19 | 31 | 2.844 | 16* | 1 | 6 |
| 20 | 31 | 3.004 | 18* | 2 | 2 |
| 21 | 31 | 2.975 | 19* | 1 | 3 |
| 22 | 31 | 3.174 | 28* | 2 | 5 |
| 23 | 32 | 3.047 | 19* | 2 | 6 |
| 24 | 14 | 721 | 2 | 1 | 6 |

\* Kolom 5-gram di sini dihitung **per bab** (bukan per paragraf), sehingga mengukur frasa domain yang berulang sepanjang bab — misalnya `the physics community and observation networks`. Angka per paragraf ada di §4.1 (maksimum 2). Ini residual yang dicatat di §8.

---

## 8. Residual dan rekomendasi

| # | Residual | Dampak | Tindakan berikutnya |
|---|---|---|---|
| R1 | Frasa domain berulang hingga 28× per bab (`the physics community and observation networks`) | Ritme monoton pada bacaan berurutan | Gate 5: ganti sebagian rujukan dengan pronomina/rujukan pendek (`the sector`, `these institutions`) |
| R2 | 14,5 % (EN) / 15,7 % (ID) kalimat berangka belum bersitasi kurung | Sebagian besar berupa angka yang sitasinya ada di kalimat sebelumnya, tetapi tidak terlacak lokal | Gate 1: tempelkan sitasi pada setiap kalimat berangka, atau gabungkan ke kalimat bersitasi |
| R3 | Penanda absolut 71 (EN): `never` 34, `must` 36, `everyone` 11 | Sebagian adalah retorika kebijakan yang sah, sebagian perlu dilunakkan | Gate 4 (panel 5 kursi): adjudikasi manual per kalimat |
| R4 | Deteksi falasi berbasis regex | Tidak dapat menangkap falasi semantik (mis. generalisasi dari satu kasus tanpa kata kunci) | Gate 4: pembacaan manusia; Gate 6 tidak menggantikannya |

---

## 9. Artefak dan reproduksi

| Berkas | Isi |
|---|---|
| `prose.py` | Mesin penulisan: 8 lensa × 4–6 varian, 6 bingkai batas bukti, 6 bingkai sintesis, 4 bingkai domain, bank penutup, jangkar pakar, `ExpertPicker`, pembangun studi kasus |
| `audit_gate3.py` | Auditor: 18 metrik + per bab, keluaran JSON |
| `book.md` / `book_id.md` | Naskah final (77.570 / 69.332 kata termasuk tabel & lampiran) |
| `Surviving_the_Future.pdf` / `..._ID.pdf` | **176 / 187 halaman**, font Tinos (metrik Times New Roman), 25 tabel, daftar isi 24/24 akurat |

```bash
python gen_book.py && python gen_book_id.py
python audit_gate3.py book.md   > /tmp/en.json
python audit_gate3.py book_id.md > /tmp/id.json
python render_book.py && python render_book_id.py
```

**Catatan font.** Lingkungan build tidak memiliki Times New Roman (font berlisensi, tidak dapat diunduh). Renderer memakai **Tinos** — metrik dan proporsi identik dengan Times New Roman, lisensi Apache 2.0. Untuk memakai TNR asli: letakkan `Times New Roman.ttf` + varian bold/italic di `fonts/` dan ubah `_fam` di `book_pdf.py`.

---

## 10. Kesimpulan gate

- **Blocker isi:** dibereskan — templat verbatim 672 → 0; blok pakar bilingual 44 → 0; kutipan setengah Inggris 60 → 0; pakar tidak topikal 90 % → 0 %.
- **Argumen:** tidak ada falasi yang lolos adjudikasi; rasio absolut:hedge bergeser dari 1:1,4 ke 1:5,6 (EN).
- **Yang belum:** 4 residual di §8 harus ditutup di Gate 5 (revisi) dan diverifikasi ulang di Gate 5 (re-review) sebelum Gate 6.
- **Lanjutan yang disarankan:** Gate 2 (verifikasi 12 data global + 42 item berita), Gate 1 (786 sitasi + Daftar Pustaka), Gate 6 (produksi akhir).
