# Penilaian Ahli: Kelayakan Terbit *Surviving the Future*

**Peran penilai:** profesor bidang ilmu iklim dan risiko bencana, bertindak sebagai
auditor naskah (bukan penyunting bahasa).
**Naskah yang dinilai:** `book.md` (EN) dan `book_id.md` (ID); versi pertama
commit `8847077`, versi perbaikan commit `e68778c`; interior PDF 457 dan 473 halaman.
**Metode:** dua belas pemeriksaan otomatis (angka, sitasi, tabel, gambar, indeks,
glosarium, rujukan silang, atribusi, panjang bab, kepadatan sitasi, pengulangan,
metadata) ditambah pembacaan manual ±60 halaman yang paling padat angka, yaitu
seluruh tabel, seluruh catatan kaki gambar, Bab 22–24, dan bagian belakang buku.

---

## 1. Putusan

**Layak terbit.** Putusan ini berlaku setelah sepuluh butir perbaikan di §3–§5
dikerjakan, dan seluruhnya sudah dikerjakan serta diukur ulang (§8). Sebelum
perbaikan itu, putusan saya adalah *belum layak terbit*, karena yang menghambat
bukan mutu argumen melainkan **disiplin dokumentasi pada tabel** dan **lima angka
yang salah atau salah diatribusikan** — dua hal yang paling mudah ditangkap
pengulas mana pun, dan yang paling merusak kredibilitas karena muncul di tempat
pembaca paling percaya: tabel data.

Yang berubah sejak penilaian pertama: 24 tabel kini punya catatan sumber,
seluruh angka yang salah sudah diganti dengan angka yang dapat dilacak, aparatus
belakang dilengkapi, dan setiap tabel serta gambar kini dirujuk dari dalam prosa.
Isi dan argumennya tidak diubah, karena di situlah kekuatan naskah ini.

| Dimensi | Nilai | Catatan |
|---|---|---|
| Ketepatan isi (fakta, angka, satuan) | 8,0 → **9,5**/10 | lima kesalahan sudah diganti angka yang dapat dilacak |
| Aparatus akademik (sitasi, pustaka, atribusi) | 8,5 → **9,5**/10 | 698/662 sitasi terbaca, 0 masalah; 175/175 entri pustaka |
| Keterlacakan angka tabel | **4,0 → 9,5**/10 | 24 tabel kini bersumber; Table P.1 sudah punya kolom Source |
| Struktur dan keterbacaan | 9,0/10 | 24 bab, subbab bernomor, kasus + prediksi + anjuran |
| Kejujuran prediksi | 9,5/10 | 24/24 bab punya falsifier dan indikator |
| Kelengkapan aparatus belakang | 6,5 → **9,0**/10 | glosarium 13 → 64 istilah; catatan peristiwa 18 → 30 |
| Kesiapan produksi (PDF, EPUB, DOCX, sampul) | 9,0/10 | semua gate bersih, termasuk audit produksi |

**Ringkasnya:** argumennya lulus, dan dokumentasinya kini menyusul.

---

## 2. Yang sudah benar dan tidak boleh diubah

1. **Setiap bab diakhiri pengamatan yang membuktikannya salah.** Ini praktik yang
   jarang ada di buku sejenis dan merupakan kekuatan utama naskah. Pertahankan
   polanya; jangan pernah melunakkan falsifier menjadi "dapat berubah".
2. **Prediksi memakai ambang yang terukur, bukan arah.** Contoh Bab 1 (rata-rata
   lima tahun 2026–2030 = 1,35–1,5 °C) dan Bab 21 (rasio dana Loss & Damage
   dicairkan < 1/10 kebutuhan) dapat diperiksa pembaca tanpa membeli laporan baru.
3. **Paragraf anjuran pelaksanaan memberi urutan kerja, pelaku, dan larangan.**
   Ini yang membuat buku dapat dipakai pada hari kejadian, bukan hanya dibaca.
4. **Catatan Analitis** (heat deaths sebagai estimasi, atribusi sebagai
   perubahan kemungkinan, pengungsi dihitung per perpindahan) sudah menyatakan
   batas metodenya sebelum pengulas menanyakannya — langkah yang tepat.
5. **Perbandingan lintas negara dipakai sebagai dasar induktif**, bukan hiasan:
   Bhola 1970 → Amphan 2020, Eropa 2003 → 2022, Ahr 2021, Lytton 2021.
6. **Nol kemunculan klaim peran AI**, nol kutipan langsung tanpa verifikasi,
   nol duplikasi kalimat, kemiripan internal 0,38%.

---

## 3. Temuan wajib (P1) — penghambat terbit

*(Seluruh butir di bagian ini sudah dikerjakan dan diukur ulang; status per butir di §7, hasil verifikasi di §8.)*

### P1-1. Dua puluh empat dari dua puluh lima tabel tidak punya catatan sumber

Ini temuan terbesar. Hanya **Table P.1** yang punya kolom *Source*. Tabel 1.1
sampai 24.1 menyajikan angka 2050 — "200 million displaced", "−15 to −20 % GDP",
"~700,000 excess heat deaths" — tanpa satu baris pun yang menyebut asalnya.
Gambar sudah benar: setiap caption berakhir `||Source: Table 4.1; SSP2-4.5 …`,
tetapi rantainya berhenti di tabel yang tidak bersumber.

Akibatnya dua hal sekaligus: (a) pembaca tidak dapat memeriksa angka yang justru
paling ingin ia periksa; (b) klaim buku bahwa "setiap angka dapat ditelusuri ke
sumber bernama" menjadi tidak benar pada bagian yang paling menonjol. Pengulas
pertama akan membuka tabel, bukan paragraf.

**Perbaikan:** setiap tabel diberi baris sumber di bawahnya, menyebut karya yang
benar-benar memuat angkanya (penulis, tahun — judulnya ada di Daftar Pustaka),
dan menyatakan terus terang kolom 2050 sebagai pembulatan penulis atas sumber itu,
bukan sebagai estimasi titik.

### P1-2. Table 8.1 bertentangan dengan teks Bab 8 dan dengan IPCC

Tabel menulis: *70–90 % decline at 2 °C; >99 % at 3 °C*. Teks Bab 8.3 menulis
benar: *"At 1.5 °C … about 70 to 90 per cent …; at 2 °C, more than 99 per cent
(IPCC, 2018)"*. Satu tabel menggeser ambang karang satu tingkat pemanasan penuh.
Ini kesalahan yang akan langsung ditangkap setiap ahli terumbu.

**Perbaikan:** ubah baris karang menjadi 1,5 °C → 70–90 %, 2 °C → >99 %, dan
samakan kolomnya dengan ambang di teks.

### P1-3. Table 6.1 bertentangan dengan teks Bab 6 tentang penurunan tanah Jakarta

Tabel: *subsidence 1–15 cm/yr*. Teks Bab 6: *"subsidence of up to twenty-five
centimetres a year in the north"*. Dua angka untuk besaran yang sama dalam satu
bab.

**Perbaikan:** samakan menjadi "1–25 cm/yr (north Jakarta highest)" dan sebutkan
di catatan bahwa laju bergantung lokasi.

### P1-4. Angka Seoul 2022 keliru urutan besarnya

Teks: *"Record rainfall in August 2022 … killing at least 141 people (CRED, 2023)"*,
dan Table 22.1 mengulanginya. Banjir Agustus 2022 di Korea Selatan menewaskan
sekitar belasan orang (korban terbanyak di apartemen semi-basement Seoul); 141
tidak sesuai dengan catatan mana pun yang dapat saya periksa untuk peristiwa itu.
Angka sebesar itu milik peristiwa lain.

**Perbaikan:** turunkan menjadi kualitatif ("more than a dozen"), atau ganti dengan
angka yang dapat dipertahankan beserta sumbernya. Sesuai aturan yang sudah dipakai
di buku ini: yang tidak terbukti diturunkan, bukan dibiarkan.

### P1-5. Lima atribusi angka yang salah alamat

| Lokasi | Yang tertulis | Masalah | Perbaikan |
|---|---|---|---|
| Bab 1 | 2,7 °C pada 2100 "according to the International Energy Agency" | IEA tidak menerbitkan angka 2,7 °C; angka itu estimasi IPCC AR6 untuk SSP2-4.5, dan kebetulan juga angka yang dipakai Tabel 2.1 | sitasi → IPCC (2021) |
| Bab 10 | kerugian Irma US$77 miliar dan Maria US$90 miliar "(Kishore et al., 2018)" | Kishore et al. adalah studi **kematian**; angka kerugian berasal dari NOAA | pisahkan: kematian → Kishore; kerugian → NOAA NCEI (2024) |
| Bab 13 | Katrina "about 1,800 people and more than US$125 billion (Brunkard et al., 2008)" | Brunkard melaporkan kematian Louisiana saja; kerugian bukan dari studi itu | "more than 1,400 deaths in Louisiana alone (Brunkard…); damage → NOAA" |
| Bab 13 | Uri "US$195 billion … costliest disaster in Texas history (NOAA NCEI, 2024)" | NOAA menaksir kerusakan langsung sekitar US$26 miliar; US$195 miliar adalah estimasi ekonomi independen, dan badai termahal Texas tetap Harvey | pisahkan kedua angka dan buang klaim "termahal" |
| Bab 22 | Seoul 2022, 141 (lihat P1-4) | — | — |

Pola kesalahannya satu: **angka kerugian ditempelkan pada makalah yang mengukur
kematian**, karena keduanya muncul di paragraf yang sama. Ini jenis kesalahan yang
paling mudah diperbaiki dan paling mahal jika lolos.

### P1-6. Judul tabel memakai "2050" padahal isinya bukan proyeksi 2050

Sepuluh judul berakhiran ", 2050": Table 13.1, 16.1, 18.1, 19.1, 20.1, 21.1,
22.1, 23.1, 24.1 — dan yang paling jelas salah adalah **Table 22.1 "Comparative
disaster cases, 2050"** dan **Table 23.1 "Slow-onset cases, 2050"**, yang isinya
peristiwa 1995–2022 tanpa satu pun nilai 2050. Pembaca akan menyimpulkan tabel itu
berisi proyeksi, lalu menemukan Chicago 1995.

**Perbaikan:** buang akhiran ", 2050" pada tabel yang tidak memuat nilai 2050.

---

## 4. Temuan mayor (P2)

*(Seluruh butir di bagian ini sudah dikerjakan dan diukur ulang; status per butir di §7, hasil verifikasi di §8.)*

### P2-7. Dua belas tabel dan sebelas gambar tidak pernah disebut di dalam teks

Tidak ada satu pun kalimat di badan naskah yang menulis "Table 9.1" atau
"Figure 4.1". Tabel dan gambar muncul dengan caption, lalu teks berjalan lagi.
Pada buku yang menjual diri sebagai "data-rich", ini melemahkan dua hal: pembaca
tidak diberi tahu kapan harus berhenti membaca untuk melihat tabel, dan Daftar
Tabel/Gambar kehilangan fungsinya sebagai alat navigasi.

**Perbaikan:** satu kalimat penunjuk sebelum setiap tabel dan gambar ("Table 9.1
sets out the ranges used here"; "Figure 4.1 shows the same measure across the six
cities") — dua belas tabel dan sebelas gambar.

### P2-8. Glosarium 13 istilah untuk indeks 90 entri

Glosarium memuat hanya istilah paling dasar (adaptation, mitigation, resilience…)
sementara teks memakai *wet-bulb* 26 kali, *attribution* 64 kali, *loss and damage*
29 kali, *managed retreat* 10 kali, *polycentric* 10 kali, *solastalgia* 9 kali,
*climate velocity* 5 kali, *deoxygenation* 5 kali — tidak satu pun didefinisikan.
Pembaca awam yang menjadi sasaran buku ini akan mencari justru istilah-istilah itu.

**Perbaikan:** perluas glosarium ke seluruh istilah teknis yang dipakai berulang
(minimal 50 entri), satu sampai dua baris per istilah, dan samakan dengan istilah
yang muncul di indeks.

### P2-9. "Notes on Event Sources" tidak mencakup semua kasus yang dijanjikan

Pembukanya menjanjikan sumber "for the named events used as cases in this book",
tetapi daftarnya berhenti pada 18 peristiwa. Tidak ada Bhola 1970/Amphan 2020
(kasus penutup, Bab 24), Tuvalu/Falepili (Bab 11), Lake Chad (Bab 12), Italia
(Bab 14), Helene 2024 (Bab 15), program solar Bangladesh (Bab 19), Dana Loss &
Damage (Bab 21), Jakarta (Bab 6), dengue 2024 (Bab 9), atau guncangan beras 2023
(Bab 7).

**Perbaikan:** tambahkan entri untuk kasus yang hilang, dengan sumber yang sudah
ada di Daftar Pustaka.

---

## 5. Temuan minor (P3)

*(Seluruh butir di bagian ini sudah dikerjakan dan diukur ulang; status per butir di §7, hasil verifikasi di §8.)*

1. **Table 23.1, kolom "Deaths"** berisi nilai bukan-kematian: "Cholera" (Yaman)
   dan "Displacement" (Suriah). Kolom angka tidak boleh diisi kategori; ganti
   judul kolom menjadi "Outcome" atau isi dengan angka kematian.
2. **Table 6.1, header "2050 sea level"** memberi angka berbeda per kota
   (+0,15 m Jakarta, +0,18 m Miami). Nilai global sama untuk semua kota; yang
   berbeda adalah muka laut **relatif** terhadap tanah yang turun. Ganti header.
3. **Table 1.1, asumsi "Emissions peak before 2025"** sudah menjadi kontrafaktual
   pada buku bertanggal 2026. Beri catatan bahwa skenario itu tidak terwujud dan
   karena itu baris kedua yang berlaku.
4. **Table 22.1/23.1** mencampur kematian langsung dan estimasi berlebih
   (Lytton 619 adalah kematian berlebih seluruh British Columbia, bukan kematian
   di Lytton). Tambahkan keterangan di catatan tabel.
5. **Kepadatan sitasi tidak merata antar bab** (terendah Bab 14, tertinggi Bab 2);
   bukan kesalahan, tetapi Bab 14 dan Bab 16 sebaiknya ditambah dua-tiga rujukan
   pada klaim kebijakan.

---

## 6. Batas penilaian ini (harus dinyatakan)

- Saya tidak memeriksa naskah terhadap korpus berlangganan (Turnitin/iThenticate);
  skor 0,38 % yang dilaporkan adalah kemiripan **internal**, bukan skor eksternal.
- Sejumlah angka 2024–2025 (rekor suhu, luas es, harga modul) akan berubah setelah
  terbit; buku sudah menanganinya dengan memberi tahun pada setiap angka, dan itu
  praktik yang benar.
- Saya tidak menilai mutu terjemahan baris per baris; yang diperiksa adalah
  kesetaraan angka dan struktur antara kedua edisi (25 tabel, 11 gambar, 24/24
  bab lulus audit prediksi dan audit anjuran di kedua bahasa).

---

## 7. Daftar perbaikan yang harus dikerjakan sebelum terbit

| # | Perbaikan | Cakupan | Status | Bukti |
|---|---|---|---|---|
| 1 | Catatan sumber untuk 24 tabel | EN + ID | **selesai** | 24 baris `Source:` / `Sumber:` tercetak (dihitung ulang dari PDF) |
| 2 | Baris karang Table 8.1 | EN + ID | **selesai** | 1,5 °C: 70–90 %; 2 °C: >99 %; kolom ketiga menjadi akibat struktural |
| 3 | Penurunan tanah Jakarta Table 6.1 | EN + ID | **selesai** | 1–15 → 1–25 cm/tahun, sesuai teks Bab 6 |
| 4 | Angka Seoul 2022 | EN + ID | **selesai** | 141 → "setidaknya selusin"; tabel dan gambar kini memakai **12+** dan menandainya sebagai minimum, karena angka kota yang dapat dilacak hanya berada di kisaran belasan |
| 5 | Lima atribusi angka | EN + ID | **selesai** | IEA → IPCC (2021); Irma/Maria → NOAA NCEI; Katrina → Brunkard (Louisiana) + NOAA (kerusakan); Uri → TSDSHS + NOAA + analisis independen; Seoul |
| 6 | Akhiran ", 2050" pada 9 judul tabel | EN + ID | **selesai** | 13.1, 16.1, 18.1, 19.1, 20.1, 21.1, 22.1, 23.1, 24.1 tidak lagi berakhiran tahun |
| 7 | Kalimat penunjuk tabel + gambar | EN + ID | **selesai** | 24/24 tabel dan 11/11 gambar dirujuk dari prosa (0 tersisa) |
| 8 | Glosarium 13 → 55+ istilah | EN + ID | **selesai** | 64 entri (EN) / 65 entri (ID), A–Z |
| 9 | Catatan Sumber Peristiwa dilengkapi | EN + ID | **selesai** | 18 → 30 peristiwa; sepuluh kasus yang diminta sudah masuk |
| 10 | Kolom "Deaths" Table 23.1, header Table 6.1, catatan Table 1.1 | EN + ID | **selesai** | kolom menjadi "Outcome"/"Dampak"; header "2050 relative sea level"; catatan asumsi puncak emisi ditambahkan |

**Putusan akhir:** kesepuluh butir dikerjakan, diukur ulang, dan diverifikasi pada
PDF hasil render. Naskah **layak terbit** sebagai buku non-fiksi akademik-populer
dalam dua bahasa.

---

## 8. Verifikasi ulang setelah perbaikan

Semua angka di bawah diambil dari berkas hasil render terakhir, bukan dari
perkiraan.

| Pemeriksaan | Sebelum | Sesudah |
|---|---|---|
| Halaman interior | 451 / 470 | **457 / 473** |
| Kata badan | 209.718 / 174.428 | **212.489 / 176.674** |
| Sitasi terbaca | 629 / 594 | **698 / 662**, masalah **0** |
| Entri pustaka | 172 / 172 | **175 / 175** |
| Tabel dengan catatan sumber | 1 / 25 | **25 / 25** (PDF, EPUB, DOCX) |
| Tabel dirujuk dari prosa | 0 / 24 | **24 / 24** |
| Gambar dirujuk dari prosa | 0 / 11 | **11 / 11** |
| Glosarium | 13 | **64 / 65** |
| Paragraf berangka tanpa rujukan (EN) | 13 | **9** |
| Catatan peristiwa | 18 | **30 / 30** |
| Indeks | 90 entri, berhalaman | **90 entri, berhalaman, *see also*, *passim*** |
| Kemiripan internal | 0,35 % | **0,38 %** (korpus 48 bab, 389.163 kata) |
| Prediksi / anjuran | 24/24 · 48/48 | **24/24 · 48/48** |
| Audit produksi | bersih | **bersih, 0 judul menggantung, 0 blok keluar margin** |
| Gambar vs tabelnya | 8.1, 17.1, 22.1 tidak lagi cocok | **digambar ulang dan cocok** |

Dua catatan jujur tentang batas verifikasi ini. Pertama, skor 0,38 % tetap
kemiripan **internal**: tidak ada korpus berlangganan yang diakses, jadi angka itu
tidak boleh disebut skor Turnitin. Kedua, perbaikan dokumentasi tidak menambah
pembacaan ahli baru; yang saya periksa ulang adalah kesepuluh butir dan seluruh
tabel, bukan naskah 457 halaman dari awal. Untuk terbit, sisa pekerjaan bersifat
produksi (ISBN, unggah, harga), bukan naskah.

---

## 9. Temuan pada pemeriksaan kedua (dan perbaikannya)

Setelah perbaikan pertama, saya memeriksa ulang **konsistensi silang**: apakah
angka yang saya ubah di tabel masih sama dengan angka yang digambar, dengan yang
dikutip di prosa, dan dengan yang tertulis di caption. Enam ketidakcocokan
ditemukan, semuanya akibat perbaikan pertama yang tidak menjalar ke seluruh
lapisan:

| # | Temuan | Akibat bila dibiarkan | Perbaikan |
|---|---|---|---|
| 1 | Figure 8.1 masih menggambar karang 70–90 % di 2 °C | Gambar membantah tabel yang baru dikoreksi — kesalahan yang lebih sulit dimaafkan daripada salah angka | Digambar ulang: karang >99 % di 2 °C, dan barisnya diberi keterangan "3 °C: structure lost" |
| 2 | Figure 17.1 masih 700.000 / 500.000 / 250.000 | Tabel 17.1 sudah 735/500/245 | Data gambar dan teks alternatifnya disamakan |
| 3 | Table 22.1 dan Figure 22.1 masih memuat Seoul 141 | Angka yang sudah dicabut dari prosa hidup lagi di tabel dan grafik | Menjadi **12+** di keduanya, ditandai sebagai minimum |
| 4 | Prosa menyebut "nine disasters" untuk tabel berisi delapan baris | Kesalahan hitung yang mudah terlihat | Menjadi "eight" / "delapan" |
| 5 | Lytton 619 tidak dijelaskan di tabel | Pembaca membandingkan kematian desa dengan kematian provinsi | Catatan tabel: 619 = kematian berlebih seluruh British Columbia, jadi kolom dibaca sebagai orde besaran |
| 6 | Kalimat Bab 8 masih menyebut karang "bertahan dalam bentuk berkurang" di 2 °C | Bertentangan dengan >99 % pada 2 °C | Kalimat ditulis ulang: 1,5 °C vs 2 °C adalah 70–90 % vs praktis hilang |

Selain itu, klaim "emisi 2024–2025 masih pada rekor" di catatan Table 1.1
diperhalus menjadi klaim yang benar-benar dimuat sumbernya: penilaian anggaran
karbon 2024 menempatkan emisi pada tingkat rekor tanpa penurunan berkelanjutan
(Friedlingstein et al., 2024). Setelah render ulang: **457 dan 473 halaman**,
24 baris sumber tabel di PDF, EPUB, dan DOCX, dan seluruh gate bersih.

Pada pass yang sama, empat paragraf berangka yang tadinya hanya menyebut
sumber di dalam kalimat diberi sitasi kurung supaya dapat diperiksa: banjir
1995–2015 (CRED & UNISDR, 2015), pergeseran wilayah spesies (Chen et al., 2011),
rasio manfaat mitigasi (National Institute of Building Sciences, 2019), dan
pemberitahuan air mendidih Texas (Texas Comptroller of Public Accounts, 2021).
Klaim "US$195 miliar" untuk Uri diganti dengan **US$80–130 miliar** dari
Texas Comptroller (2021) — angka yang benar-benar dimuat sumbernya — dan label
"bencana termahal dalam sejarah Texas" dihapus karena NOAA sendiri menempatkan
kerusakan langsung Uri di sekitar US$26 miliar, jauh di bawah Harvey. Paragraf
berangka tanpa rujukan di edisi Inggris turun dari 13 menjadi 9, dan daftar
pustaka menjadi 175 entri di kedua edisi.

**Pelajaran yang saya catat untuk naskah ini:** setiap kali sebuah angka diubah
di tabel, tiga tempat lain harus ikut diperiksa — gambar, caption/teks alternatif,
dan kalimat prosa yang menyebutnya. Itu sekarang menjadi bagian dari daftar
pemeriksaan di `BOOK_READINESS.md`.
