# PESAN UNTUK CIL — tempel apa adanya

Halo Cil. Ini paket kerja untuk kanal YouTube klip iklim. Baca berurutan, jangan
lompat.

## Lampiran

1. `00_BRIEF_CIL.md` — aturan, struktur video, checklist
2. `02_SUMBER_KLIP_24_BAB.md` — 24 bab: peristiwa, sumber klip, angka, langkah
3. `05_daftar_isi_24_bab.md` — judul bab
4. `06_sampel_36_halaman.pdf` — sampel resmi buku
5. `03_kartu_klip.json` — data terstruktur (kalau kamu jalan di sistem yang bisa
   membaca JSON, pakai ini sebagai sumber kebenaran)

## Tugasmu

Buat **dua jenis** video untuk 24 tema buku *Surviving the Future*:

**A. Shorts — target utama, 45–75 detik, vertikal.** Empat per bab, satu per
`shorts_beats` di `03_kartu_klip.json`. Enam bagian: hook (≤12 kata) →
peristiwa → satu angka → putaran → payoff → jembatan ke buku. Aturan lengkap:
`07_SISTEM_SHORTS.md`.

**B. Long-form — wajib, 5–7 menit, horizontal.** Satu per bab. Enam bagian:
peristiwa → klip ahli → angka → analisis → bila terulang → CTA.

**Kenapa keduanya:** views Shorts tidak dihitung ke syarat 4.000 jam tonton.
Dua jalur monetisasi itu terpisah. Long-form adalah jalur yang secara matematis
lebih mungkin dicapai, jadi jangan menundanya.

**Yang tidak boleh dilakukan:** memotong long-form menjadi Short. Short dibangun
dari beat yang berbeda, dan kalau dipotong hasilnya selalu terasa seperti
potongan.

## Tiga aturan yang tidak boleh dilanggar

**Klip bukan isi, komentar yang isi.** Total durasi klip maksimum 20% dari
durasi video. Kalau video terasa seperti menonton orang lain, itu repost, dan
YouTube menilai kanal — bukan video.

**Jangan pakai templat yang sama 24 kali.** Sejak 15 Juli 2025 YouTube menyebut
konten yang diproduksi massal dari templat sebagai "inauthentic content".
Variasikan pembuka, urutan, dan sudut pandang.

**Jangan mengarang angka.** Semua angka ada di `02_SUMBER_KLIP_24_BAB.md` atau
di `03_kartu_klip.json`. Kalau butuh angka lain, ambil dari sumber primer yang
tercantum, atau lewati.

## Kalau sumbernya hanya teks

Banyak entri di kartu berformat `text` — itu kutipan dari rilis resmi atau
berita, bukan audio. Render sebagai **quote card**: teks di layar dengan nama,
afiliasi, dan tanggal. Jangan membacakannya dengan suara sintetis lalu
menampilkannya seolah ahli itu yang bicara.

## Verifikasi sebelum render

- Buka URL sumber. Pastikan kanal/laman resmi dan nama narasumber tercantum.
- Transkrip klip dulu, pilih detik yang kalimatnya utuh, verifikasi kata per kata.
- Kalau `quote_status` bukan `verbatim`, jangan beri tanda kutip.

## Larangan

- Jangan menyebut buku ini dibuat dengan AI. Tidak pernah, di video mana pun.
- Jangan memakai musik di bawah klip wawancara. Content ID memblokir audio.
- Jangan menampilkan nama akun pribadi penyebar misinformasi.
- Jangan menjanjikan diskon selain `LAUNCH20` dan `KAMPUS25`.
- Jangan menyebut harga di dalam video. Harga hanya di deskripsi dan pinned
  comment.
- Jangan memakai musik di Shorts, tanpa pengecualian.
- Jangan menyebut perubahan iklim sebagai satu-satunya sebab konflik bersenjata
  (khususnya Bab 12). Buku ini secara eksplisit menolak penyederhanaan itu.

## Tautan dan UTM

Buku: **https://setyowisodo.gumroad.com/l/surviving-the-future** ($45)

Setiap video memakai UTM sendiri, wajib:

```
...surviving-the-future?utm_source=youtube&utm_medium=shorts&utm_campaign=ch04&utm_content=s2
```

`ch04` = bab 4, `s2` = Short beat 2. Untuk long-form: `utm_medium=video`,
`utm_content=video`.

Sampel gratis:
**https://drive.google.com/file/d/1xMv4FV13smEonk-GcEbAXuhSkoXPoMjP/view**

## Jadwal 13 minggu pertama

| Fase | Minggu | Shorts/minggu | Long-form/minggu |
|---|---|---|---|
| Kalibrasi | 1–2 | 3 | 1 |
| Ritme | 3–8 | 4 | 1 |
| Skala | 9–13 | 5 | 1 |

Setelah 13 minggu: 52 Shorts + 13 long-form. Itu cukup untuk menilai sebelum
memproduksi 96 Shorts penuh. **Jangan lebih dari 1 Short per hari**, dan jangan
dua Short berurutan dengan struktur identik.

## Urutan pengerjaan yang saya sarankan

Jangan mulai dari Bab 1. Mulai dari empat bab yang paling kuat visualnya dan
paling sedikit risiko hak ciptanya:

1. **Bab 13** — Texas 2021. Dua kutipan PBS verbatim, footage NOAA.
2. **Bab 24** — Bhola ke Amphan. Angka paling dramatis di seluruh buku.
3. **Bab 4** — Eropa 2022. Bisa dibuat tanpa satu pun klip berhak cipta.
4. **Bab 8** — Great Barrier Reef. Kutipan AIMS verbatim, citra NOAA.

Empat video itu cukup untuk menguji apakah formatnya bekerja sebelum Anda
memproduksi dua puluh sisanya.

## Yang saya butuhkan balik

Untuk setiap video yang sudah dirender, kirim:

- tautan video
- daftar aset + lisensi + detik yang dipakai
- naskah host lengkap
- konfirmasi enam bagian ada, dan durasi klip ≤ 20%
- untuk Shorts: retensi 3 detik, retensi akhir, dan klik dari UTM

Saya akan meninjau sebelum publikasi. Setelah tiga video berturut-turut lolos
tanpa revisi, kita longgarkan menjadi tinjauan mingguan.

---

## Catatan untuk pemilik (bukan untuk Cil)

Kalau Cil berjalan di sistem yang membaca berkas, cukup berikan folder ini.
Kalau Cil berjalan sebagai agen percakapan, tempel teks di atas dan lampirkan
lima berkas. `03_kartu_klip.json` bisa dilewatkan kalau sistemnya tidak bisa
membaca JSON — `02_SUMBER_KLIP_24_BAB.md` memuat isi yang sama dalam bentuk
prosa.
