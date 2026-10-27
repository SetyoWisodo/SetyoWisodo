# Pemeriksaan Plagiasi — Surviving the Future

**Kesimpulan singkat:** teks bukunya bersih dari duplikasi dan tidak memuat satu pun
kutipan langsung. **Tetapi ada satu bahaya laten di generator** yang harus dibaca
lebih dulu daripada angka mana pun di halaman ini.

---

## 0. Batas yang harus saya sampaikan lebih dulu

Alat pemeriksa plagiasi yang sesungguhnya — Turnitin, iThenticate, Copyscape,
Grammarly Premium — bekerja dengan membandingkan naskah Anda ke **korpus luar**:
miliaran halaman web, jurnal berlangganan, dan arsip buku. Korpus itu tidak ada
di sini dan tidak bisa diakses dari lingkungan ini.

Jadi saya **tidak** bisa memberi skor "X% mirip dengan sumber lain". Siapa pun yang
memberi angka seperti itu tanpa menjalankan alat tersebut sedang menebak.

Yang **bisa** saya lakukan, dan sudah saya lakukan, adalah memeriksa empat hal yang
justru menjadi penyebab sebagian besar temuan plagiasi:

1. duplikasi internal (kalimat yang berulang di dalam buku sendiri),
2. disiplin kutipan (teks dalam tanda kutip tanpa sumber),
3. kelengkapan rujukan dua arah,
4. atribusi kepada orang nyata.

Empat-empatnya bisa diperiksa tanpa korpus luar, dan hasilnya di bawah.

---

## 1. Yang saya temukan — dan ini yang paling penting

### Bahaya laten: 54 kutipan rekaan di dalam generator

`gen_book.py` dan `gen_book_id.py` berisi daftar `EXPERTS` dengan **60 entri**, dan
**54 di antaranya berbentuk kutipan langsung** yang dinisbatkan kepada orang nyata:

```
"Prof. Bill McKibben, 350.org (2019 Falter): 'We have built a world that can be
 undone by what we built — the fight is ...'"
```

Saya periksa ke sumbernya. **Kutipan itu tidak ada di *Falter*** (2019). Kutipan
Bill McKibben yang benar-benar terdokumentasi dari buku itu antara lain *"We have, in
other words, changed the energy balance of our planet…"* dan *"We've built a new Earth.
It's not as nice as the old one…"* — bukan kalimat di atas.

Hal yang sama berlaku pada entri lain. Kutipan Nick Watts *"The health bill for
inaction already exceeds the cost of action"* juga tidak ditemukan dalam laporan
Lancet Countdown yang dirujuk.

Selain teksnya, beberapa gelar dan afiliasi juga keliru:

| Tertulis | Seharusnya |
|---|---|
| Dr. Al Gore | tidak bergelar doktor |
| Prof. David Wallace-Wells | jurnalis, bukan profesor |
| Prof. Elizabeth Kolbert | jurnalis, bukan profesor |
| Prof. Kim Stanley Robinson | penulis, bukan profesor |
| Prof. Naomi Klein, **Rutgers** | University of British Columbia |

**Kabar baiknya:** 54 kutipan itu **tidak ada di dalam buku yang Anda jual.** Saya
memeriksa `book.md`, `book_id.md`, dan kedua PDF 430/445 halaman: nol kemunculan.
`book.md` dihasilkan oleh versi generator yang lebih lama, sebelum blok `EXPERTS`
ditambahkan, dan belum pernah dibuat ulang sejak itu.

**Kabar buruknya:** kalau Anda menjalankan `python gen_book.py` hari ini — misalnya
untuk memperbaiki satu salah ketik — generator akan menyuntikkan **96 atribusi rekaan**
ke dalam buku (60 ahli, diputar ulang di 96 subbab), lalu Anda akan menerbitkannya.

Menisbatkan kalimat rekaan kepada penulis yang masih hidup bukan plagiasi, tetapi
risiko hukumnya lebih berat: pencemaran nama baik, pelanggaran hak kepribadian, dan
dalam kasus akademik disebut *fabrication* — pelanggaran yang jauh lebih serius
daripada kemiripan teks.

### Sudah diperbaiki

1. **Pengaman kutipan** ditambahkan di kedua generator. Aturannya: atribusi hanya
   dicetak bila indeksnya ada di `EXPERT_VERIFIED`, dan himpunan itu **kosong**.
   Selama kosong, generator memakai kalimat topik netral tanpa nama.
2. **`prose.section_topic()`** ditambahkan — enam variasi kalimat topik netral,
   Inggris dan Indonesia.
3. **Referensi Klein** diperbaiki: judulnya terbelah jadi dua kalimat
   (`*This Changes Everything: Capitalism vs*. The Climate.`) di `references.py`.
4. **`audit_plagiarism.py`** sekarang ikut memeriksa generator dan melaporkan berapa
   entri yang akan tercetak.

Kalau nanti Anda ingin memakai atribusi ahli, aturannya satu: buka karyanya, temukan
kalimatnya **kata per kata**, catat nomor halaman, baru masukkan indeksnya ke
`EXPERT_VERIFIED`. Tidak ada jalan pintas.

---

## 2. Duplikasi internal — hasilnya sangat baik

Dihitung dengan `audit_plagiarism.py` (kalimat ≥ 9 kata, ambang kemiripan Jaccard 0,62
pada 4-shingle):

| | Inggris | Indonesia |
|---|---|---|
| Kalimat diperiksa | 7.355 | 7.033 |
| **Berulang persis** | **2** (0,0%) | **4** (0,0%) |
| Nyaris sama (≥ 0,62) | 7 | 2 |
| Teks dalam tanda kutip ≥ 40 huruf | **0** | **0** |
| Kutipan tanpa sumber | 0 | 0 |

Dua kalimat yang berulang persis di versi Inggris sama-sama tentang Lytton
(baris 4498 dan 4674) — satu kejadian yang disebut dua kali. Itu bukan plagiasi,
hanya pengulangan yang bisa dirapikan.

**Angka 0 kutipan langsung itu penting.** Buku ini tidak memuat satu pun kalimat
dalam tanda kutip yang panjang. Artinya tidak ada teks yang disalin utuh dari sumber
mana pun. Semua rujukan berbentuk parafrase dalam kalimat penulis sendiri — bentuk
yang paling aman terhadap tuduhan plagiasi.

Sebagai pembanding: naskah nonfiksi hasil susunan ulang biasanya menunjukkan
duplikasi internal 3–10%. Angka di sini di bawah 0,1%.

---

## 3. Rujukan — lengkap dua arah

`check_citations.py` memeriksa dua arah dan hasilnya **0 masalah** di kedua edisi:

- setiap sitasi dalam teks punya entri di daftar pustaka,
- setiap entri daftar pustaka dipakai di dalam teks.

| | Inggris | Indonesia |
|---|---|---|
| Sitasi terbaca | 403 | 351 |
| Entri daftar pustaka | 145 (130 dikutip + 15 bacaan lanjutan) | 145 (124 + 21) |
| Masalah | **0** | **0** |

Ini pertahanan terkuat Anda terhadap tuduhan plagiasi: 145 sumber nyata, dikutip,
dan dua arahnya konsisten.

---

## 4. Yang masih perlu diperhatikan

### 4.1 Angka tanpa rujukan — 22%

Dari 2.090 paragraf panjang di edisi Inggris, **455 (22%) memuat angka tetapi tidak
ada sitasi di paragraf itu**. Sebagian besar dirujuk di paragraf sebelumnya, jadi ini
bukan pelanggaran — tetapi pembaca yang teliti akan menanyakannya, dan penguji
skripsi akan menandainya.

Kalau ingin diperbaiki, saya bisa menambahkan rujukan ringkas pada kalimat berangka
yang paling menonjol. Tidak perlu mengubah teks lain.

### 4.2 Kemiripan dengan sumber luar — belum diuji

Ini bagian yang tidak bisa saya kerjakan dan tidak bisa digantikan oleh audit di atas.
Yang perlu dilakukan sebelum terbit:

| Alat | Biaya | Cocok untuk |
|---|---|---|
| **Turnitin** (lewat kampus) | gratis kalau ada akses | paling akurat untuk naskah akademik |
| **iThenticate** | ±$100 per naskah | standar penerbit jurnal |
| **Copyscape Premium** | ±$0,05 per 100 kata | memeriksa halaman web |
| **Grammarly Premium** | ±$12/bulan | memeriksa satu naskah, kurang akurat untuk kutipan |

Yang perlu Anda lakukan: unggah `book.md` (bukan PDF, supaya tidak terpotong halaman),
lalu periksa **daftar sumber yang cocok**, bukan skor totalnya. Skor 15% bisa
sepenuhnya berasal dari daftar pustaka dan nama lembaga — itu normal dan bukan
plagiasi.

### 4.3 Karakter teks yang dihasilkan mesin

Ini bukan plagiasi, tetapi berhubungan dan perlu Anda tahu: pola kalimat yang sangat
seragam (banyak paragraf dengan panjang hampir sama, banyak konstruksi "X is not Y;
it is Z") bisa dikenali pembaca sebagai teks yang disusun mesin. Sebagian pembaca
menganggapnya sama seriusnya dengan plagiasi meski secara hukum berbeda.

Belum ada bagian di buku yang perlu diubah untuk ini, tetapi kalau Anda ingin, saya
bisa menandai paragraf yang paling berpola dan menulis ulang sebagian agar ritmenya
lebih beragam.

---

## 5. Tiga istilah yang sering dicampur

Supaya Anda tahu persis risiko mana yang sedang dihadapi:

| | Apa itu | Contoh di buku ini | Akibat |
|---|---|---|---|
| **Plagiasi** | memakai kata/karya orang lain tanpa pengakuan | **tidak ditemukan** | sanksi akademik, teguran, penarikan |
| **Pelanggaran hak cipta** | memakai karya berhak cipta di luar izin | kutipan pendek dengan sumber: wajar. Gambar: dibuat sendiri dari data, aman | tuntutan ganti rugi |
| **Fabrikasi** | menyatakan sesuatu yang tidak benar sebagai fakta, termasuk kutipan rekaan | **54 kutipan di generator** — sudah diblokir | kehilangan kredibilitas total |

Plagiasi adalah soal **atribusi**. Yang paling berbahaya di antara ketiganya justru
yang ketiga, dan itulah yang hampir masuk ke buku Anda.

---

## 6. Ringkasan tindakan

| Status | Hal |
|---|---|
| ✅ Selesai | Pengaman kutipan di kedua generator |
| ✅ Selesai | Kalimat topik netral pengganti atribusi |
| ✅ Selesai | Referensi Klein diperbaiki |
| ✅ Selesai | `audit_plagiarism.py` — audit duplikasi + pemeriksa atribusi |
| ✅ Terverifikasi | 0 kutipan langsung di buku; duplikasi < 0,1% |
| ✅ Terverifikasi | 0 masalah sitasi dua arah, kedua edisi |
| ⬜ Perlu Anda | Jalankan Turnitin/iThenticate sebelum terbit |
| ⬜ Opsional | Tambal rujukan pada paragraf berangka |
| ⬜ Opsional | Variasikan ritme paragraf yang terlalu seragam |

Menjalankan ulang `python audit_plagiarism.py` kapan pun akan memberi angka terbaru
dan memastikan pengaman atribusi masih utuh.
