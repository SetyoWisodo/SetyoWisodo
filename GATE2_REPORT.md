# GATE 2 — Laporan Konsistensi Data

**Buku:** *Surviving the Future: Crisis, Climate, and Human Resilience* (EN) / *Bertahan di Masa Depan* (ID)
**Ruang lingkup:** 24 bab × 2 bahasa; 23 fakta kanonis; audit angka lintas bab, lintas bagian, dan lintas edisi
**Tanggal:** 21 Oktober 2026 · **Status gate:** **LULUS** (tidak ada kontradiksi angka yang tersisa; lima koreksi data diterapkan)

---

## 1. Kriteria lulus

Gate 2 menguji empat hal, bukan sekadar "apakah angkanya benar":

| Kode | Kriteria | Ambang |
|---|---|---|
| K1 | Tidak ada dua angka berbeda untuk peristiwa, entitas, dan metrik yang sama di dalam satu edisi | 0 konflik tak terjelaskan |
| K2 | Setiap fakta kanonis muncul di kedua edisi dengan nilai yang sama | 100 % |
| K3 | Angka yang dipakai berulang memakai nilai, satuan, dan pembulatan yang sama | 0 varian tak disengaja |
| K4 | Koreksi data tidak merusak aparatus sitasi dan Daftar Pustaka | 0 masalah |

Verifikasi K4 dilakukan dengan `check_citations.py` setiap kali teks berubah.

---

## 2. Alat

### 2.1 `data_consistency.py` — penyapu konflik angka lintas bab

Cara kerja:

1. Kalimat diekstrak dari badan buku (appendiks dikeluarkan agar tabel audit tidak ikut dinilai).
2. Setiap angka beserta satuannya diambil dengan regex `NUM`; satuan yang dibandingkan: `%`, `per cent/persen`, `°C`, `cm/mm/m`, `million/billion/juta/miliar`, `ppm/ppb`, `Gt/tonnes`, `km`.
3. Angka dikelompokkan ke dalam kunci **(entitas, tahun, metrik, satuan)**. Metrik yang dilacak: korban tewas, terdampak, pengungsi, kerugian, laju muka laut, pemanasan, konsentrasi, hasil panen, biaya.
4. Bucket dengan lebih dari satu nilai berbeda diurutkan menurut rasio terbesar/terkecil, lalu dicetak dengan contoh kalimat.

Tiga perbaikan presisi yang dikerjakan di gate ini:

| Masalah | Gejala | Perbaikan |
|---|---|---|
| Desimal dibaca sebagai ribuan | `2.7 °C` menjadi `27`; `1.5` menjadi `15`; satu kalimat memunculkan "konflik" palsu | `norm_num()` sadar bahasa: EN memakai titik sebagai desimal dan koma sebagai ribuan; ID sebaliknya |
| Semua angka dalam kalimat dimasukkan ke metrik apa pun | "33 juta terdampak, 1.700 tewas, 2,2 juta rumah" dilaporkan sebagai konflik | Angka dipilih yang **paling dekat** dengan kata metrik (jendela 80 karakter ke belakang / 60 ke depan), bukan seluruh kalimat |
| Kata pembuka kalimat dianggap entitas | "About", "More", "By September", "Sekitar" menjadi nama entitas | Daftar `OPENERS` (EN + ID) menyingkirkan kata umum; kata yang tersisa harus berupa frasa bermodal |

Efek ketiga perbaikan: kandidat turun dari **17 (EN) / 25 (ID)** menjadi **2 (EN) / 2 (ID)**.

### 2.2 `fact_check.py` — tabel fakta kanonis dua bahasa

- **23 fakta** yang masing-masing menentukan satu nilai untuk satu peristiwa.
- Setiap fakta punya jangkar konteks EN dan ID yang berbeda (karena kedua edisi bukan terjemahan literal), plus daftar nilai yang diterima (termasuk angka yang dieja: *eighty-five*, *delapan puluh lima*, *one million*, *satu juta*).
- Pemeriksaan peka huruf besar/kecil setelah normalisasi; kalimat tabel dan baris yang dimulai `|`, `-`, `#`, `[[` tetap dilewati, sehingga yang diuji adalah prosa.
- Dijalankan pada **kedua** edisi; satu kegagalan saja membuat exit code 1.

---

## 3. Hasil audit lintas bab

### 3.1 Kandidat yang tersisa (setelah perbaikan parser)

| Edisi | Entitas · tahun | Nilai | Vonis |
|---|---|---|---|
| EN | Stern Review 2006 · biaya | 1 % vs 5–20 % | **Bukan konflik** — 1 % adalah biaya *bertindak*, 5–20 % biaya *tidak bertindak*; kontras yang disengaja |
| EN | Watts 2021 · korban tewas | 3,7 vs 4,0 juta | **Bukan konflik** — 4 juta polusi luar ruang, 3,7 juta polusi rumah tangga; dua kategori paparan |
| ID | Stern Review 2006 · biaya | 1 % vs 5–20 % | **Bukan konflik** — sama dengan EN |
| ID | IPCC 2021 · pemanasan | 1,5 vs 5 °C | **Bukan konflik** — anggaran 1,5 °C vs perhitungan Arrhenius untuk penggandaan CO₂; dua topik berbeda yang bertemu di satu bab |

Semua kandidat diperiksa manual satu per satu; tidak ada yang berubah menjadi koreksi.

### 3.2 Kandidat sebelum perbaikan parser (contoh yang dibuang)

| Pola | Contoh | Sebab |
|---|---|---|
| Desimal → puluhan | `1.5 °C` vs `2.7 °C` dilaporkan sebagai 15 vs 27 | normalisasi angka |
| Campuran metrik satu kalimat | 33 juta terdampak, 1.700 tewas, 2,2 juta rumah | pemilihan angka per metrik |
| Kata pembuka sebagai entitas | "About", "By September", "Sekitar", "Jumlahnya" | keyer entitas |
| Rentang sah | 5–20 %, 0,3–0,4 m, 200–500 miliar | dua ujung rentang dianggap dua klaim |

---

## 4. Temuan nyata dan koreksi

Lima koreksi diterapkan. Semua ditulis ulang di dalam narasi; tidak ada catatan metode yang ditempel di badan buku.

| # | Lokasi | Sebelum | Sesudah | Alasan |
|---|---|---|---|---|
| 1 | Bab 4 (EN + ID) | Dua klaim bertentangan untuk kematian akibat panas: "70 peratus" dan "167 peratus" (Lancet Countdown) | Klaim 70 % dihapus; angka 167 % tetap di dua tempat dengan atribusi yang benar (Romanello 2024) | Satu statistik tidak boleh muncul dengan dua nilai |
| 2 | Bab 2 (EN) | "remaining carbon budget is roughly 200 billion tonnes … about five years" | "roughly 250 billion tonnes … about six years" | ID sudah 250; AR6 SYR memberi 250 GtCO₂ dari 2023 untuk peluang 50 % pada 1,5 °C, setara ±6 tahun pada ±40 Gt/tahun |
| 3 | Bab 9 (EN + ID) | Polusi udara rumah tangga "3 million or more" / "3 juta lebih" | "3.7 million" / "3,7 juta" | Bertentangan dengan bagian lain yang memakai 3,7 juta untuk kategori yang sama |
| 4 | Bab 4 pembuka (EN + ID) | "The World Health Organization attributes more than 175,000 deaths a year to heat" (tersirat global) | "In Europe alone, … more than 175,000 deaths a year" / "Di Eropa saja, …" | Angka 175.000 adalah angka **kawasan Eropa** WHO (36 % dari 489.000 global), bukan angka global |
| 5 | Bab 4 (EN + ID) | "The 2021 Lancet Countdown estimated that more than 500,000 deaths a year are associated with heat" | "The World Health Organization estimates about 489,000 heat-related deaths a year between 2000 and 2019 (WHO, 2023)" | Laporan 2021 memperkirakan ±345.000 kematian pada usia >65 (2019), bukan 500.000; angka 489.000 adalah estimasi WHO 2000–2019 yang juga dipakai di bab lain |

Koreksi tambahan pada Bab 1 (EN + ID): angka WHO "150.000 kematian per tahun" yang sudah usang dan bertabrakan skalanya dengan angka panas 500.000 diganti dengan proyeksi WHO yang dipakai di bab 9 — **250.000 kematian tambahan per tahun antara 2030 dan 2050** — dengan daftar jalur yang disamakan (panas, diare, malaria, kurang gizi). Angka panas 500.000 dihapus dari Bab 1 karena sudah dinyatakan di Bab 4; yang tersisa adalah 61.700 kematian musim panas Eropa 2022 dan 7 juta kematian akibat polusi udara, keduanya berdiri sendiri tanpa klaim aritmetika yang salah.

Setelah koreksi, angka panas yang dipakai konsisten di seluruh buku:

| Angka | Arti | Lokasi |
|---|---|---|
| 489.000 / tahun | Kematian terkait panas global, rata-rata 2000–2019 (WHO) | Bab 4 |
| 175.000 / tahun | Kematian terkait panas kawasan Eropa (WHO) | Bab 4 pembuka |
| 167 % | Kenaikan mortalitas panas pada usia >65 dibanding 1990-an (Lancet Countdown 2024) | Bab 4, Bab 17 |
| 61.700 | Kematian musim panas Eropa 2022 | Bab 1, studi kasus, Bab 9 |
| 500.000 | **Tidak lagi dipakai sebagai klaim kematian panas global**; angka ini masih muncul untuk Bhola 1970 dan tabel skenario 2050 Bab 17 | — |

---

## 5. Fact check kedua edisi

23 fakta × 2 edisi = **46 pemeriksaan**, semuanya lolos.

| Fakta | Nilai kanonis | EN | ID |
|---|---|---|---|
| CO₂ 2024 | 424 ppm | OK | OK |
| CH₄ | 1.934 ppb | OK | OK |
| Laju muka laut | 4,5 mm/tahun | OK | OK |
| Pemanasan sampai 2024 | 1,1–1,3 °C | OK | OK |
| Katrina 2005 | ±1.800 tewas | OK | OK |
| Maria 2017 | 2.975 kematian berlebih | OK | OK |
| Eropa 2003 | 70.000 tewas | OK | OK |
| Black Saturday 2009 | 173 tewas | OK | OK |
| Camp Fire 2018 | 85 tewas | OK | OK |
| Bhola 1970 | 300.000–500.000 tewas | OK | OK |
| Somalia 2011 | 258.000 tewas | OK | OK |
| Etiopia 1984 | satu juta tewas | OK | OK |
| Sahel 1968 | 100.000 tewas | OK | OK |
| Pakistan 2022 — terdampak | 33 juta | OK | OK |
| Pakistan 2022 — tewas | 1.700 | OK | OK |
| Pakistan 2022 — kerugian | US$30 miliar | OK | OK |
| Lembah Ahr 2021 | 134 tewas | OK | OK |
| Kematian panas global | 489.000/tahun | OK | OK |
| Kematian panas Eropa | 175.000/tahun | OK | OK |
| Anggaran 1,5 °C | 250 GtCO₂ | OK | OK |
| Proyeksi WHO | 250.000/tahun (2030–2050) | OK | OK |
| Panas Eropa 2022 | 61.700 tewas | OK | OK |
| Polusi udara | 7 juta/tahun | OK | OK |

Keluaran akhir: **TOTAL GAGAL: 0**.

---

## 6. Sapuan peristiwa manual

Selain alat, 14 peristiwa disapu manual pada kedua edisi — mencari angka yang sama yang muncul dengan nilai berbeda di bab berbeda:

| Peristiwa | Nilai yang dicek | Hasil |
|---|---|---|
| Pakistan 2022 | 33 juta / 1.700 / US$30 miliar / US$16 miliar pemulihan | Konsisten; 30 dan 16 adalah kerusakan vs kebutuhan pemulihan, bukan kontradiksi |
| Katrina 2005 | ±1.800 | Konsisten |
| Maria 2017 | 2.975 kematian berlebih | Konsisten |
| Eropa 2003 | 70.000 | Konsisten |
| Black Saturday 2009 | 173 | Konsisten |
| Bhola 1970 | 300.000–500.000 | Konsisten (rentang, bukan dua nilai) |
| Somalia 2011 | 258.000 | Konsisten |
| Somalia 2022 | 43.000 | Konsisten |
| Etiopia 1984 | satu juta | Konsisten |
| Sahel 1968 | 100.000 | Konsisten |
| Lembah Ahr 2021 | 134 | Konsisten |
| Camp Fire 2018 | 85 | Konsisten |
| Panas Eropa 2022 | 61.700 | Konsisten di semua kemunculan |
| Kematian panas global | 489.000 vs 500.000 | **Dikoreksi** (lihat #5) |

---

## 7. Aparatus dan integritas

| Pemeriksaan | Hasil |
|---|---|
| `check_citations.py` | **377 sitasi EN / 336 ID**, 0 `NO-ENTRY`, 0 `YEAR` |
| Daftar Pustaka | 145 entri per edisi |
| Works Cited | 130 EN / 123 ID |
| Further Reading | 15 EN / 22 ID |
| Kata (termasuk appendiks) | 131.263 EN / 115.723 ID |
| Bab | 24 per edisi |
| Tabel | 25 |

Koreksi #4 dan #5 menambah satu sitasi `(WHO, 2023)` di masing-masing edisi; entri WHO 2023 sudah ada di Daftar Pustaka, sehingga tidak ada entri baru dan tidak ada entri menggantung.

---

## 8. Keterbatasan dan residual

1. **Bukan pembuktian numerik menyeluruh.** Yang diuji adalah 23 fakta kanonis dan 14 peristiwa yang disapu manual. Angka lain di buku tidak diverifikasi ulang terhadap sumber primer di gate ini; verifikasi sumber dilakukan pada lapisan riset sebelumnya.
2. **Penyapu angka adalah alat bantu baca, bukan hakim.** Keyer entitas masih heuristik; kandidat yang tersisa (Stern, Watts, IPCC 2021) sengaja dibiarkan karena merupakan kontras yang benar.
3. **Baris tabel tidak dipindai** oleh kedua alat. Tabel skenario Bab 17 memakai rentang 700.000 / 500.000 / 250.000 kematian panas pada 2050; itu proyeksi skenario, bukan klaim hari ini, dan tidak diubah.
4. **Pembulatan disengaja.** 61.672 → 61.700; 489.000 → "sekitar 489.000"; 1.934 ppb. Varian pembulatan dicatat sebagai nilai yang diterima di `fact_check.py`.
5. **Batas sumber.** Angka WHO 489.000 (2000–2019), 175.000 (Eropa), dan proyeksi 250.000 (2030–2050) berasal dari lembar fakta dan laporan WHO; angka 167 % dari Romanello et al. 2024. Tidak ada angka yang dipakai tanpa atribusi di badan teks.

---

## 9. Keputusan gate

**LULUS.** Tidak ada kontradiksi angka yang tersisa; lima koreksi data diterapkan di kedua edisi; 46 pemeriksaan fakta kanonis lolos; aparatus sitasi tetap bersih pada 377/336 sitasi.

Gate berikutnya: **Gate 4 — panel tinjau** (enam sudut pandang: iklim, kebijakan, ekonomi, kesehatan, etika, dan praktisi lapangan), dilanjutkan Gate 5 (gaya) dan Gate 6 (produksi).
