# GATE 5 — Laporan Gaya

**Buku:** *Surviving the Future: Crisis, Climate, and Human Resilience* (EN) / *Bertahan di Masa Depan* (ID)
**Ruang lingkup:** kedua edisi, 24 bab, 25 tabel, 12 appendiks
**Tanggal:** 22 Oktober 2026 · **Status gate:** **LULUS**

---

## 1. Kriteria lulus

| Kode | Kriteria | Ambang | Hasil |
|---|---|---|---|
| S1 | Tidak ada templat pembuka paragraf yang berulang lintas bab | 0 templat tersisa | **0** |
| S2 | Tidak ada kalimat penutup/pembuka identik yang berulang lebih dari 2× | ≤ 2 kemunculan | **lolos** (lihat §3) |
| S3 | Kalimat absolut (*always/never/inevitable*) hanya dipakai bila memang klaim retoris, bukan klaim empiris mutlak | Tidak ada absolut tak sengaja | **4 + 3 koreksi** |
| S4 | Kalimat tidak berlebihan panjang | rata-rata < 30 kata, maksimum < 90 | **24,1 / 76 kata (EN)**; **20,2 / 70 (ID)** |
| S5 | Paragraf tidak berukuran ekstrem | maksimum < 250 kata | **186 (EN) / 141 (ID)** |
| S6 | Tata letak: Times/Tinos 12 pt, *justify*, indent 12,7 mm, nomor halaman tengah-bawah lalu kanan-bawah | 100 % paragraf | **100 %** |
| S7 | Aparatus sitasi bersih setelah semua perubahan gaya | 0 masalah | **422 EN / 376 ID, 0** |

---

## 2. Alat dan letak perbaikan

Semua perbaikan gaya dilakukan **pada teks final** lewat `style_pass.py` (dan modul turunannya), bukan pada berkas konten. Alasannya praktis: kalimat di modul konten terpotong menjadi beberapa literal string, sehingga penggantian langsung sering gagal tanpa suara. Karena transformasi ini idempoten, hasilnya bertahan pada setiap regenerasi.

| Berkas | Isi |
|---|---|
| `style_pass.py` | transformasi lama (FS openers, `NUM_FIX`, present-condition, assumption frames) + de-templating Gate 4 + tabel dedup dan absolut Gate 5 |
| `style_variety.py` | 102 pasangan EN + 22 pasangan ID untuk variasi pembuka paragraf (modul baru di gate ini) |
| `content/ch17.py`, `content_id/ch17.py` | catatan arah pada Tabel 17.1 |
| `content/depth_zj` … `depth_zo` (EN+ID) | paragraf penutup yang menambah kedalaman bab 1, 10, 16, 18, 22, 23, 24 |

---

## 3. Temuan dan perbaikan

### 3.1 Templat yang masih berulang (ditutup di gate ini)

| Templat | Kemunculan | Perbaikan | Sisa |
|---|---|---|---|
| `Two conclusions follow.` / `Dua kesimpulan mengikuti.` | 22 / 23 | dirotasi menjadi 5 rumusan berbeda (masing-masing 4–5×) | **0** |
| `a world that does not will …` / `dunia yang tidak akan …` | 10 / 10 | diganti varian yang menyebut apa yang tidak dilakukan | **0** |
| `The most important variable remains the pace of …` | 4 | rumusan per bab | **0** |
| `The indicators worth watching are …` | 12 | 5 pembuka berbeda di berkas sumber | **0** |
| `The lessons are specific.` / `Pelajarannya spesifik.` | 5 / 5 | diberi subjek (*for importers, for warning systems, …*) | **0** |
| `The case shows / illustrates …` | 16 | diganti rumusan yang menyebut objeknya | ≤ 2 |

### 3.2 Pembuka paragraf yang bertabrakan

Lapisan pendalaman menambahkan paragraf ke dalam sub-bab yang sudah ada, dan sebagian membuka dengan kalimat yang mengulang klaim paragraf sebelumnya (paling parah di studi kasus, yang seluruhnya dimulai dengan "The …"). Audit dilakukan dengan membandingkan **kalimat pertama** setiap paragraf terhadap paragraf sebelumnya dalam sub-bab yang sama, memakai Jaccard kata isi (ambang 0,45–0,55).

| Ukuran | Sebelum gate | Sesudah gate |
|---|---|---|
| Pasangan paragraf berurutan dengan pembuka mirip (EN) | 45 | **2** |
| Pasangan paragraf berurutan dengan pembuka mirip (ID) | 34 | **0** |
| Paragraf berurutan dengan kata pertama sama (EN) | 33,5 % | **28,3 %** |
| Paragraf berurutan dengan kata pertama sama (ID) | 16,7 % | **16,5 %** |
| Rentetan terpanjang kata pertama sama (EN / ID) | 8 / 6 | **6 / 6** |

Sisa 28,3 % di EN bukan cacat: kata pertama yang sama sebagian besar adalah artikel "The" pada kalimat yang berbeda subjek dan predikat, dan pemakaiannya wajar dalam prosa akademik berbahasa Inggris. Yang diperbaiki adalah pengulangan **klaim**, bukan pengulangan artikel.

### 3.3 Kalimat absolut

Daftar pendek, bukan sapuan menyeluruh, karena banyak pemakaian *never* dan *always* memang retoris dan tepat ("a false claim travels faster than a correction, and always has"). Yang diubah hanya frasa yang membuat klaim empiris mutlak:

| Sebelum | Sesudah |
|---|---|
| a health-only surveillance **will always** detect late | … **tends to** detect late |
| the counts **are always** underestimated | … **almost always** underestimated |
| usually larger **and always** harder to measure | usually larger **and** harder to measure |
| the tree-planting target **was always** a political slogan | … **was from the outset** a political slogan |
| (ID) yang **selalu** terlambat dideteksi | yang **cenderung** terlambat dideteksi |
| (ID) biasanya lebih besar **dan selalu** lebih sulit diukur | biasanya lebih besar **dan** lebih sulit diukur |
| (ID) hitungannya **selalu** diremehkan | hitungannya **hampir selalu** diremehkan |

Kata *inevitable* tinggal 4 kemunculan, dan tiga di antaranya adalah penyangkalan ("these vulnerabilities are not inevitable"), yang justru pesan buku.

### 3.4 Tabel 17.1 — kolom "Current trends"

Gate 4 mencatat bahwa kolom tengah tabel indikator kesehatan 2050 tidak menjelaskan arahnya. Ditambahkan satu paragraf tepat di bawah tabel, di kedua edisi: kolom itu bukan ramalan, melainkan lintasan yang mengikuti kebijakan yang sudah diundangkan, belanja adaptasi yang sudah dijanjikan, dan investasi kesehatan yang sudah dianggarkan, dengan jalur emisi pada kasus menengah — yaitu kolom yang didapat pemerintah bila tidak mengubah apa pun.

---

## 4. Tata letak (S6)

Tidak ada perubahan pada gate ini. Verifikasi ulang pada PDF hasil render:

| Butir | EN | ID |
|---|---|---|
| Font isi | Tinos 12 pt (metrik Times) | Tinos 12 pt |
| Perataan | *justify* + indent baris pertama 12,7 mm | sama |
| Nomor halaman | tengah-bawah pada halaman pembuka bab, kanan-bawah selebihnya | sama |
| Baris judul bab | "CHAPTER n" + judul, dua baris tengah; tidak diulang di halaman berikutnya | "BAB n" + judul |
| Daftar Isi & Daftar Tabel | dengan nomor halaman | sama |
| Jumlah halaman | **401** | **419** |

---

## 5. Hasil pemeriksaan

| Pemeriksaan | Hasil |
|---|---|
| `check_citations.py` | **422 EN / 376 ID**, 0 `NO-ENTRY`, 0 `YEAR` |
| `fact_check.py` | **46/46, 0 gagal** |
| `data_consistency.py` | 2 kandidat EN / 2 ID — keduanya kontras yang disengaja |
| Pemindaian CJK | 0 berkas |
| Kata | **197.411 EN / 164.129 ID** |
| Paragraf naratif | 2.072 EN / 2.067 ID |
| Rata-rata panjang kalimat | 24,1 kata (EN) / 20,2 (ID) |

---

## 6. Keterbatasan

1. **Audit pembuka paragraf memakai heuristik** (Jaccard kata isi). Ia menangkap pengulangan klaim, tidak menangkap pengulangan irama kalimat yang lebih halus.
2. **Panjang kalimat tidak dipangkas secara mekanis.** Lima belas kalimat EN melebihi 60 kata dan semuanya berupa daftar berstilistika dengan titik koma (paralelisme), bukan kalimat berlapis anak kalimat; kalimat terpanjang 76 kata. Memecahnya akan merusak retorika tanpa menambah kejelasan.
3. **Tidak ada uji keterbacaan otomatis** (Flesch-Kincaid) yang dilaporkan; untuk prosa akademik berbahasa Indonesia skor itu tidak terkalibrasi.
4. **Style pass bekerja pada teks, bukan pada PDF.** Perubahan tata letak tetap menjadi wewenang `render_book.py` dan `render_book_id.py`.

---

## 7. Keputusan gate

**LULUS.** Enam templat lintas bab ditutup, 47 paragraf dengan pembuka yang bertabrakan diperbaiki, tujuh absolut yang tidak perlu dilunakkan, dan Tabel 17.1 mendapat catatan arah. Kedua edisi tetap bersih pada seluruh pemeriksaan aparatus, dan keduanya berada dalam rentang panjang yang diminta: **401 halaman (EN)** dan **419 halaman (ID)**.

Gate berikutnya: **Gate 6 — produksi** (metadata PDF, penomoran halaman, keterbacaan cetak, pemeriksaan akhir berkas pratinjau).
