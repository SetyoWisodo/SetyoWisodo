# JAWABAN ATAS REVIEW CIL — 25 November 2026

Dokumen ini menjawab `review-sistem-kerja.pdf` (Cil/Muse, 25 Nov 2026, 10
halaman). Untuk pemilik, bukan untuk Cil. Bagian 1–3 adalah penilaian saya atas
review itu sendiri; bagian 4 menjawab delapan pertanyaan; bagian 5 adalah daftar
perubahan yang sudah dikerjakan di paket ini.

---

## 1. Ringkas: review ini benar di hampir semua hal, dan salah di satu hal

Dari 11 temuan, **sepuluh saya terima dan sudah diperbaiki**. Satu saya tolak
sebagian, dan itu justru yang paling penting untuk dipahami.

**Yang diterima:** P0-1 (matematika ekonomi), P0-3 (kontradiksi Shorts), P1-1
(bersih per buku), P1-2 (host dan disclosure), P1-3 (hash templat), P1-4
(target tanpa dasar), P1-5 (jam kerja), P2-1 (bahasa beat), P2-2 (validator dan
versi skema), P2-3 (kode diskon belum diverifikasi), P2-4 (yang hilang: nama
kanal, jam upload, dashboard, SOP komentar).

**Yang saya tolak sebagian — P0-2.** Review menulis "30 dari 39 klip masih
`to_source`" lalu menyimpulkan "data klip belum siap render". Hitungannya benar,
diagnosisnya kurang tepat. Dari 30 klip itu, **21 berformat `text`** — dan klip
`text` memang **tidak pernah** dimaksudkan untuk "dipotong". Ia dirender sebagai
quote card, dan untuk itu yang dibutuhkan hanya teks + atribusi, bukan
timecode. Yang benar-benar menunggu transkrip adalah **9 klip** (7 audio + 1
audio `paraphrase` + 1 audio yang sudah verbatim), bukan 30.

Artinya: sistem ini bukan "72% belum siap". Ia **siap untuk 4 bab** (1, 2, 8,
13) dan **hampir siap untuk 4 bab lain** yang hanya butuh mengganti satu klip
audio dengan quote card. Itu perbedaan antara "tunda semuanya" dan "mulai
minggu ini sambil memverifikasi".

Satu koreksi kecil untuk review: review menyebut "8 verbatim dari 39". Yang
benar **9** (7 text + 2 video), plus 1 audio verbatim setelah perbaikan hari
ini = 10.

---

## 2. Kesalahan hitung yang review temukan — dan yang masih tersisa

Review benar: "1 buku = 10.000–30.000 views" salah 30–40 kali lipat **sebagai
ekuivalensi iklan**. Sudah diganti di semua berkas menjadi **384.000–1.280.000
views iklan** per buku.

Tapi angka 10.000–30.000 tidak muncul dari udara, dan penting untuk tahu dari
mana asalnya sebelum membuangnya sepenuhnya. Itu angka **funnel**, bukan angka
iklan:

| Asumsi | Angka |
|---|---|
| Klik dari views Shorts | 0,05–0,3% |
| Klik → pembelian | 1–3% |
| Hasil: views per 1 buku | **11.000–200.000** (dingin) |
| Hasil: views per 1 buku, audiens yang sudah mengenal Anda | 10.000–30.000 |

Jadi yang salah bukan angkanya, tapi **labelnya**. Sekarang keduanya ditulis
terpisah di `04_HANDOFF_STUDIO.md` §5c dan di `economics` JSON, dan asumsinya
ditandai eksplisit sebagai asumsi yang belum diukur. Aturan: ganti dengan data
12 Shorts pertama, jangan biarkan asumsi jadi kebijakan.

## 3. Satu hal yang review lewat, dan akibatnya besar

Review memverifikasi tiga klaim kebijakan YouTube dan menandai satu sebagai
"tidak dicek" — perluasan definisi view 24 Agustus 2026. Saya cek hari ini ke
halaman **"How engagement metrics are counted"**. Isinya:

> "Views are counted the moment a video starts to play across all formats,
> including Shorts, long-form videos (VODs), and live streams."

Jadi **perluasannya benar**, tapi **tanggal 24 Agustus 2026 tidak ada di halaman
itu** dan tidak bisa saya buktikan dari sumber resmi. Karena itu tanggalnya
saya hapus dari `09_ALGORITMA.md`, dan diganti kalimat yang bisa ditunjuk.
Konsekuensi praktisnya tidak berubah: pakai engaged views untuk semua
perbandingan.

Satu temuan tambahan yang belum ada di sistem mana pun: halaman yang sama
menulis bahwa **sejak November 2026**, view publik di halaman tonton memasukkan
estimasi **co-viewing** di layar TV. Artinya headline views sekarang bahkan
tidak sebanding antar perangkat. Ini memperkuat aturan "jangan pakai headline
views" dari alasan yang berbeda.

---

## 4. Delapan pertanyaan review

### 4.1 Ekonomi: berapa views untuk 10 penjualan pertama?

Dengan bersih $38,40 (direct) / $31,50 (Discover), campuran 80:20 = **$37,02
per buku**. Untuk 10 buku = **$370**.

| Sumber | Views yang dibutuhkan untuk $370 |
|---|---|
| Iklan Shorts @ $0,07/1.000 | **5,3 juta** |
| Iklan Shorts @ $0,328/1.000 (audiens AS) | **1,1 juta** |
| Iklan long-form @ $2,50–5,00/1.000 | **74.000–148.000** |
| Funnel Shorts @ 0,05–0,3% klik, 1–3% beli | **110.000–2.000.000** |

Kesimpulan yang harus dipegang: **jangan mengejar 10 penjualan lewat iklan
Shorts.** 5,3 juta views Shorts untuk $370 bukan target; itu hukuman. Yang
masuk akal: 13 minggu dipakai untuk membangun **audiens yang mengenal Anda**,
lalu menjual ke mereka. Funnel bekerja pada audiens hangat, bukan pada penonton
acak dari feed.

**Apakah 52 Shorts + 13 long-form dalam 13 minggu masuk akal?** Sebagai
eksperimen, ya — dengan tiga syarat: (a) minggu 1–4 tanpa target angka, (b)
verifikasi klip selesai untuk minimal 4 bab sebelum render pertama, (c) ritme
diturunkan jadi 2 Shorts + 1 long-form per minggu kalau jam kerja nyata melebihi
13 jam. 52 Shorts sebelum ada data adalah taruhan; 12 Shorts + 3 long-form
adalah eksperimen. Mulai dari yang kedua.

### 4.2 Monetisasi: apakah lolos "inauthentic content"?

Jawaban jujur: **96 Shorts dengan 6 bagian yang sama berisiko, dan hash struktur
tidak menyelamatkan.** Halaman kebijakan YouTube menyebut contoh yang persis
menggambarkan pola ini:

> "AI-generated content made with generic or unoriginal templates giving the
> impression of mass production without adding the creator's original,
> authentic insights or perspective."

Perhatikan dua kata terakhir: **insights** dan **perspective**. Yang dinilai
bukan struktur, tapi apakah ada sesuatu yang hanya bisa datang dari Anda.

Bukti terkuat yang harus disiapkan, berurutan:

1. **Satu `original_element` per video**, dicatat di manifes: penilaian pribadi,
   koreksi terhadap liputan media, atau perbandingan lintas bab. Ini yang
   membedakan "template" dari "seri".
2. **Variasi yang bersubstansi, bukan kosmetik.** Nama kanal yang sama boleh;
   pembuka yang identik kata per kata, tidak.
3. **Jejak editorial**: naskah tersimpan, tanggal, catatan kenapa sudut itu
   dipilih. Kalau ada review manual, ini yang Anda kirim.
4. **Metadata yang tidak seragam**: judul, deskripsi, dan thumbnail yang benar-
   benar berbeda — bukan hasil mail-merge.
5. **Bukti kehadiran manusia di komentar**: balasan yang spesifik, bukan templat.

Yang **tidak** perlu: hash struktur sebagai bukti. Hash hanya berguna sebagai
peringatan internal.

### 4.3 Hak cipta: klip mana yang paling berisiko?

Urutan risiko, dari paling tinggi:

| Peringkat | Klip | Kenapa |
|---|---|---|
| 1 | **BBC audio** (ch 4, 6, 7, 9, 11, 18) | BBC agresif soal audio; episode penuh tersedia di platform mereka, jadi klaim mudah dibuktikan. Klip 8–12 detik dengan komentar dominan masih bisa dipertahankan, tapi ini yang paling mungkin diklaim. |
| 2 | **NPR audio** (ch 9, 10) | Sama, plus NPR menyediakan transkrip publik — bagus untuk verifikasi, tapi juga memudahkan orang mengenali potongannya. |
| 3 | **PBS video** (ch 13) | Dua klip ini sudah `verbatim` dan paling siap, tapi tetap footage berhak cipta. Komentar harus jelas lebih panjang. |
| 4 | **Al Jazeera, Reuters, CNN, dll.** (teks) | Rendah — kalau dirender sebagai quote card, tidak ada audio/video yang diambil. |

**Rekomendasi konkret:** untuk 7 klip audio yang masih `to_source`, jangan
transkrip semuanya. Ganti **4 di antaranya** dengan quote card + citra domain
publik sejak awal (ch 6 Jakarta, ch 11 Tuvalu, ch 18 Ahr, ch 24 Bhola). Simpan
klip audio hanya untuk bab di mana suara ahli benar-benar menambah sesuatu:
ch 4 (pendinginan pasif), ch 9 (nyamuk), ch 13 (grid — tapi ini video, sudah
siap). Itu memotong pekerjaan verifikasi dari 9 menjadi 5, dan menurunkan
risiko di bab yang paling sering dibagikan.

### 4.4 Fair use: apakah 7–12 detik + ≤20% + komentar lebih panjang cukup?

Cukup sebagai **postur**, tidak cukup sebagai **jaminan**. Tiga hal yang sistem
ini remehkan:

1. **Fair use adalah hukum AS.** Kalau kanal ditonton dari Inggris, Kanada, atau
   Uni Eropa, kerangka yang berlaku berbeda. YouTube menyelesaikan lewat sistem
   klaim, bukan pengadilan — dan sistem klaim tidak membaca "empat faktor", ia
   membaca kecocokan audio. Klip 10 detik tetap bisa diklaim.
2. **BBC dan DW punya kebijakan penggunaan yang lebih ketat** daripada rata-rata
   penyiar AS, dan keduanya aktif mengajukan klaim. Untuk dua sumber ini,
   perlakukan sebagai "pinjam dengan izin", bukan "fair use".
3. **Angka 20% itu tinggi.** Untuk video 5 menit, 20% = 60 detik klip. Itu bukan
   komentar lagi. Aturan yang lebih aman: **maksimal 3 klip × 10 detik = 30
   detik per video long-form**, dan **0 detik klip berhak cipta** di Shorts
   (quote card saja). Shorts terlalu pendek untuk menampung komentar yang
   mengalahkan klip.

Yang harus ada di setiap manifes aset, dan sekarang diwajibkan: URL, tanggal
akses, lisensi, detik masuk/keluar, baris atribusi, dan **`licence_basis`**
(`public_domain` / `cc_by` / `fair_use_commentary` / `permission`).

### 4.5 Algoritma: apakah 70% / 80% realistis?

Tidak — bukan karena terlalu tinggi, tapi karena **tidak ada pembanding**.
Kanal ini belum punya satu video. Angka 70% berasal dari kanal lain dengan
audiens lain, dan review benar bahwa jarak 70% (target) ke 50% (ambang berhenti)
tidak dijelaskan oleh dokumen mana pun.

Yang sudah diubah:

- Minggu 1–4: **ukur, jangan nilai**. 12 Shorts + 2 long-form tanpa ambang.
- Minggu 5: baseline = **median 12 Shorts pertama**.
- Target = **baseline + 10 poin persentase**, bukan 70%.
- 70% / 80% tetap ada sebagai aspirasi, bukan gerbang.
- Aturan berhenti tetap 50%, karena di bawah itu masalahnya bukan target.

Satu tambahan yang tidak ada di review: **jangan menilai apa pun dari 3 video
pertama.** Median dari 3 angka adalah noise. Dua belas adalah minimum untuk
melihat pola.

### 4.6 AI disclosure vs "jangan sebut buku dibuat dengan AI"

Dua hal yang berbeda, dan sistem lama mencampurnya. Gerbang 5 memindai kata
"AI" lalu memblokir — yang bisa memblokir justru kalimat disclosure yang
diwajibkan platform.

Yang benar, dari halaman bantuan YouTube "Disclosing use of GenAI content":

**Wajib dilabeli** (setelan "AI use" → Yes): membuat orang nyata tampak
mengatakan sesuatu yang tidak ia katakan; mengubah footage peristiwa/tempat
nyata; membuat adegan realistis yang tidak terjadi; **musik AI yang menjadi
fokus video**.

**Tidak wajib dilabeli:** bantuan produksi seperti menulis kerangka/naskah,
judul, thumbnail, infografik; caption; perbaikan audio; **mengkloning suara
sendiri** untuk voice-over.

**Untuk kasus Anda:** narasi TTS dari naskah sendiri, dengan suara generik yang
tidak meniru orang nyata, **tidak masuk kategori wajib label**. Tapi:

- kalau TTS-nya meniru suara tokoh nyata → wajib;
- kalau video menampilkan klip ahli, suara ahli **tidak boleh** diganti TTS →
  itu misrepresentasi, terlepas dari label;
- labelnya gratis. Nyalakan. Tidak ada kerugian distribusi (halaman bantuan
  menyatakan label tidak membatasi audiens atau kelayakan monetisasi).

**Wording untuk deskripsi kalau memilih TTS:**
> "Narration in this video is synthesized from my own script. No expert voice
> has been generated or imitated; quotes from experts appear as on-screen text
> with source attribution."

Kalimat itu memisahkan tiga hal sekaligus: suara narator sintetis, tidak ada
pemalsuan suara ahli, dan kutipan tetap kutipan. Larangan "jangan sebut buku
dibuat dengan AI" tetap berlaku dan tidak bertentangan — yang dilarang adalah
klaim tentang **buku**, bukan disclosure tentang **video**.

### 4.7 Operasi: berapa jam sebenarnya?

Review benar: 9 jam/minggu tidak memuat pekerjaan yang sistem ini sendiri
wajibkan. Hitungan ulang, per bab:

| Kerja | Waktu |
|---|---|
| Pilih 4 beat + tulis 4 naskah | 2,5 jam |
| Verifikasi klip (buka URL, transkrip, pilih detik, cek lisensi) | 2–3 jam |
| Render 4 Shorts + jalankan gerbang | 2,5 jam |
| Naskah + render 1 long-form (5–7 mnt) | 3 jam |
| Manifes aset, metadata, UTM, unggah | 1,5 jam |
| Review manusia + `original_element` | 0,5–1 jam |
| **Total** | **12–13 jam** |

Untuk bab yang klipnya sudah bersih, 11 jam. Untuk bab yang klipnya masih
`to_source`, tambah 3–5 jam pada minggu pertama bab itu. **24 bab = 264–312
jam**, atau **7–11 bulan** pada satu bab per minggu.

**Apakah ritme harus diturunkan?** Ya, sampai backlog verifikasi habis: **2
Shorts + 1 long-form per minggu** selama 4–6 minggu pertama, sambil
memverifikasi 4 bab berikutnya. Setelah itu kembali ke 4 Shorts + 1 long-form.
Ini bukan penurunan ambisi; ini supaya bulan keenam masih ada kanal yang bisa
dilanjutkan.

### 4.8 Strategi: apakah Bab 13 → 24 → 4 → 8 urutan terbaik?

Tidak lagi — dan ini salah satu tempat review memberi koreksi yang benar.
Urutan harus ditentukan oleh **apa yang bisa dirender hari ini**, bukan oleh
kekuatan isi. Validator memberi jawabannya:

```
python3 validate_kartu_klip.py --siap
→ SIAP RENDER: [1, 2, 8, 13]
```

Urutan yang dipakai sekarang: **13 → 8 → 2 → 1**. Bab 13 (Texas) dan 8 (Reef)
tetap, ditambah Bab 2 (Keeling, citra NASA/NOAA) dan Bab 1 (Pakistan, dua
kutipan Al Jazeera verbatim + citra satelit).

**Bab 16 (kesiapan rumah tangga) tidak masuk empat pertama**, walau review
mengusulkannya. Alasannya: dua klipnya (NIST dan NEJM) keduanya `to_source`,
dan yang satu adalah PDF teknis 100+ halaman. Untuk video pertama, itu bukan
"paling sedikit butuh footage" — itu paling banyak butuh riset. Bab 16 masuk
gelombang kedua, setelah sprint verifikasi.

**Bab 24 (Bhola–Amphan)** juga tidak masuk empat pertama meski paling dramatis:
tiga klipnya `to_source`, dan review sendiri menandai angka Bhola sebagai yang
paling sering salah kutip. Satu klipnya sudah saya perbaiki hari ini (BBC
Future, kutipan John Harding, verbatim), jadi bab 24 sekarang butuh dua
verifikasi, bukan tiga — masih gelombang kedua.

---

## 5. Perubahan yang sudah dikerjakan

| # | Berkas | Perubahan |
|---|---|---|
| 1 | `03_kartu_klip.json` | schema **1.2**; `economics` ditulis ulang (net direct/Discover/blended, views per buku, funnel terpisah, RPM laporan industri); `beat_language` per bab; `quote_candidate` + `quote_source` untuk 39 klip; 6 `line` dipendekkan ke ≤12 kata; URL 14 klip diperbaiki (bukan halaman depan); 1 klip tanpa URL diperbaiki |
| 2 | `validate_kartu_klip.py` | **baru** — 11 pemeriksaan (E1–E8, W1–W2), keluar kode 1 kalau ada error; `--siap` mencetak bab yang boleh dirender |
| 3 | `04_HANDOFF_STUDIO.md` | §2 kontrak v1.2 + aturan `quote`; §3 gerbang 5 (AI dua arah), 7 (hash + manusia), 10–11 baru; §4 gerbang manusia ke-4 (`original_element`); §5 pipeline mulai dari cek siap; §5c ekonomi ditulis ulang; §6 Shorts **tidak** dipotong; §8b–8e baru (perbaikan, baseline, host, yang kosong); §10 batas paket |
| 4 | `00_BRIEF_CIL.md` | §1.3 pemisahan AI-buku vs disclosure-video; §1.4 **baru** — tiga pilihan host + kewajiban mencatat pilihan |
| 5 | `01_KIRIM_KE_CIL.md` | jadwal 13 minggu dengan fase baseline; urutan mulai dari validator; larangan AI diperjelas |
| 6 | `02_SUMBER_KLIP_24_BAB.md` | status verifikasi jujur; angka Bhola (300.000 WMO) dan Amphan (26, bukan "sekitar seratus"); 76.000 relawan CPP |
| 7 | `07_SISTEM_SHORTS.md` | §10 ditulis ulang (baseline, tiga aturan berhenti); checklist + `original_element` + bahasa + label AI |
| 8 | `09_ALGORITMA.md` | tanggal 24 Agu 2026 dihapus, diganti kutipan resmi; co-viewing Nov 2026; tabel target jadi aspirasi |
| 9 | `10_OPERASI_HARIAN.md` | ritual verifikasi sebelum produksi; 11–13 jam; jam upload WIB; dashboard; SOP komentar; protokol koreksi |
| 10 | `README_CARA_PAKAI.txt` | ekonomi, metrik baseline, larangan baru |
| 11 | `11_JAWABAN_REVIEW.md` | **baru** — dokumen ini |

**Yang belum diperbaiki, dan tidak bisa dari sini:**

1. Nama kanal dan handle — keputusan Anda (`00` §1.4).
2. Host: manusia, TTS, atau hybrid — keputusan Anda (`00` §1.4).
3. Kode `LAUNCH20` / `KAMPUS25` — perlu dicek di Gumroad; tidak ada akses dari
   sini, dan review juga tidak memverifikasinya.
4. 21 klip `text` masih berstatus `to_source` — itu **normal** untuk quote card,
   tapi teks kutipannya harus diambil dari sumber sebelum dirender. Validator
   menandainya sebagai "belum siap", yang memang benar.
5. 37 angka masih bersumber "buku bab N" tanpa nama lembaga — peringatan W1,
   bukan error. Buku adalah sumber yang sah untuk video Anda sendiri.

---

## 6. Satu hal yang saya tidak setujui dari semangat review ini

Review menulis: *"Sistem ini kuat sebagai sistem editorial dan lemah sebagai
pipeline render otomatis."* Itu benar sebagai deskripsi, tapi berbahaya sebagai
rekomendasi kalau ditafsirkan sebagai "tambahkan lebih banyak otomasi".

Otomasi bukan yang kurang. Yang kurang justru **sisi manusia**: satu penilaian
per video, satu verifikasi per klip, satu balasan per komentar. Menambah
otomasi di atas kekurangan itu menghasilkan lebih banyak video yang lebih cepat
terbaca sebagai pabrik — dan itulah satu-satunya kegagalan yang tidak bisa
diperbaiki setelah terjadi, karena YouTube menilai **kanal**, bukan video.

Karena itu seluruh revisi ini bergerak ke arah sebaliknya: lebih sedikit
gerbang mesin, lebih banyak gerbang manusia yang harus dilewati dengan sadar.
Validator ada bukan untuk mempercepat render, tapi untuk memastikan render
tidak dimulai sebelum bahannya siap.
