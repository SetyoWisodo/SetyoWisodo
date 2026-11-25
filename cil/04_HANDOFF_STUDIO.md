# HANDOFF — integrasi ke studio clipper otomatis

Dokumen untuk Anda (pemilik), bukan untuk Cil. Isinya cara studio memakai
`03_kartu_klip.json`, gerbang yang harus dipaksakan mesin, dan spesifikasi
keluaran.

---

## 1. Berkas dan perannya

| Berkas | Untuk siapa | Sifat |
|---|---|---|
| `01_KIRIM_KE_CIL.md` | Cil (agen) | pesan siap tempel + daftar lampiran |
| `00_BRIEF_CIL.md` | Cil | aturan, struktur video, checklist |
| `02_SUMBER_KLIP_24_BAB.md` | Cil | versi manusia: narasi + sumber + langkah |
| `03_kartu_klip.json` | **studio** | sumber kebenaran terstruktur |
| `05_daftar_isi_24_bab.md` | Cil | daftar bab |
| `06_sampel_36_halaman.pdf` | Cil | sampel resmi |

Aturan penting: **JSON adalah sumber kebenaran.** Kalau `02` dan `03` berbeda,
JSON menang, dan `02` yang harus diperbaiki. Jangan biarkan mesin membaca
prosa bebas sebagai data.

---

## 2. Kontrak data

`03_kartu_klip.json` v1.0. Field yang dipakai mesin:

```
chapters[].id                      int 1..24
chapters[].opening_line            kalimat buku, boleh dibacakan (TTS/host)
chapters[].event.{place,date,summary}
chapters[].numbers[]               {claim, value, source, verified}
chapters[].clips[]                 {outlet, item, date, url, format,
                                    speaker, affiliation, quote,
                                    quote_status, use, note}
chapters[].steps_if_repeated[]     langkah bernomor, sudah urut prioritas
chapters[].cta                     satu kalimat penutup
chapters[].forbidden[]             larangan spesifik bab itu
```

`format` menentukan cara mesin mengambil materi:

- `audio` — klip audio dari podcast. Ambil 7–12 detik. Wajib transkrip dulu.
- `video` — footage video. Ambil 7–12 detik. Wajib cek lisensi kanal.
- `text` — **hanya teks**. Tidak ada audio untuk dipotong. Mesin **wajib**
  merender ini sebagai *quote card* (teks di layar + atribusi), bukan mencoba
  mengunduh atau membacakan dengan suara ahli. Membacakan kutipan teks dengan
  suara sintetis lalu menampilkannya seolah ahli yang bicara adalah misrepresentasi.

`quote_status` menentukan boleh-tidaknya menampilkan tanda kutip:

- `verbatim` — boleh ditampilkan sebagai kutipan, kata per kata.
- `paraphrase_check_before_use` — **tidak** boleh diberi tanda kutip sampai
  diverifikasi ke sumber aslinya.
- `to_source` — belum ada teks kutipan. Mesin harus mengambil dari `url`,
  mentranskrip, lalu manusia memilih potongannya.

**Jangan pernah** mengisi `quote` dengan hasil parafrase lalu memberi
`quote_status: verbatim`. Ini kesalahan yang paling merusak kredibilitas, dan
paling sulit diperbaiki setelah video terbit.

---

## 3. Gerbang keras (mesin harus menolak render)

Ini bukan saran; ini yang harus membuat pipeline berhenti.

1. **Durasi klip.** Total detik klip ÷ durasi video ≤ 0,20. Tidak ada satu klip
   > 12 detik.
2. **Tidak ada klip tanpa komentar.** Setiap klip harus diikuti segmen narasi
   ≥ 30 detik sebelum klip berikutnya.
3. **Angka.** Setiap angka yang muncul di naskah harus cocok dengan salah satu
   entri `numbers[]` di bab itu, ATAU membawa atribusi sumber di layar. Kalau
   tidak cocok, blokir.
4. **Larangan bab.** Cocokkan naskah terhadap `forbidden[]`; kalau ada
   substring yang cocok, tandai untuk review manusia — jangan auto-publish.
5. **Kata "AI".** Pindai naskah untuk "AI", "artificial intelligence", "model
   bahasa", "ChatGPT", "dibuat dengan". Kalau muncul dalam konteks penulisan
   buku, blokir. (Konteks topik AI boleh, tapi cek manual.)
6. **Musik.** Tolak track apa pun yang tidak berasal dari YouTube Audio Library
   atau lisensi yang tersimpan di manifes aset.
7. **Templat.** Hash struktur video (urutan segmen + panjang tiap segmen, tanpa
   isi) harus berbeda dari 3 video terakhir. Kalau sama, peringatkan.
8. **Atribusi.** Setiap aset di timeline harus punya baris atribusi di deskripsi
   yang dihasilkan. Aset tanpa atribusi = gagal render.
9. **Kode diskon.** Hanya `LAUNCH20` dan `KAMPUS25` yang boleh muncul. Apa pun
   selain itu, blokir.

---

## 4. Gerbang manusia (tidak bisa diotomatiskan)

Tiga hal ini tetap butuh mata manusia, dan sebaiknya memang begitu:

1. **Pemilihan detik klip.** Mesin bisa memotong di tengah kalimat yang secara
   gramatikal utuh tapi mengubah makna. Ini kesalahan paling umum dan paling
   merusak.
2. **Penilaian "apakah ini masih komentar atau sudah repost".** Tidak ada metrik
   yang bisa memutuskan ini. Kalau Anda menontonnya dan terasa seperti menonton
   orang lain, itu repost.
3. **Vonis akhir soal `forbidden[]`.** Mesin cocokkan string; manusia menilai
   konteks.

---

## 5. Pipeline yang saya sarankan

```
[1] pilih bab            -> baca 03_kartu_klip.json
[2] ambil aset           -> klip sesuai format; quote card untuk "text"
[3] transkrip klip       -> wajib, simpan .srt per aset
[4] pilih detik          -> aturan: kalimat utuh, mulai setelah napas, akhiri
                            setelah kata, bukan di tengah
[5] susun timeline       -> 6 segmen wajib (brief bagian 3)
[6] tulis naskah host    -> dari numbers[] + steps_if_repeated[]
[7] jalankan gerbang     -> bagian 3 di atas
[8] review manusia       -> bagian 4 di atas
[9] render + metadata    -> judul, deskripsi, atribusi, pinned comment
[10] arsip               -> simpan manifes aset per video
```

Manifes aset per video (JSON kecil) sebaiknya menyimpan: URL sumber, tanggal
akses, lisensi, nama file lokal, hash, dan baris atribusi yang dipakai. Kalau
ada klaim Content ID enam bulan kemudian, manifes inilah yang menyelamatkan Anda.

Contoh manifes:

```json
{
  "video_id": "ch04-eu-heat-2022",
  "assets": [
    {
      "file": "assets/pbs_2021_02_16_wara.mp4",
      "source_url": "https://www.pbs.org/newshour/show/...",
      "outlet": "PBS NewsHour",
      "licence": "fair_use_short",
      "clip_in": "00:01:42",
      "clip_out": "00:01:51",
      "attribution": "Interview clip: PBS NewsHour, 16 Feb 2021 — used for commentary, 9 seconds.",
      "accessed": "2026-10-18"
    }
  ]
}
```

---

## 5b. Pipeline Shorts (target utama)

Short dan long-form dibangun dari **beat berbeda**, bukan saling memotong. Detail
lengkap ada di `07_SISTEM_SHORTS.md`; di sini bagian yang menyangkut mesin.

```
[1] pilih bab + beat          -> dari 03_kartu_klip.json
[2] tulis naskah 45-75 dtk    -> 6 bagian wajib, anggaran 2,6 kata/detik
[3] pilih aset                -> utamakan quote card + citra PD/CC BY
[4] render vertikal           -> 1080x1920, teks aman di 15% tengah
[5] jalankan gerbang shorts   -> daftar di bawah
[6] review manusia            -> hook + potong detik
[7] upload + UTM              -> utm_campaign=chNN, utm_content=sN
[8] catat di dashboard        -> retensi 3 dtk, retensi akhir, klik
```

### Gerbang keras khusus Shorts

1. **Durasi** 45–75 detik (batas keras: 180 detik, tetapi di atas 90 hanya
   boleh dengan persetujuan manusia).
2. **Hook** ≤ 12 kata dan mulai di detik 0. Deteksi: tidak boleh ada kata
   "tahukah", "di video kali ini", "hai", "welcome back".
3. **Satu angka saja** dalam seluruh naskah. Kalau ada dua entri `numbers[]`
   yang muncul, tolak.
4. **Kredit di layar**, bukan hanya deskripsi — minimal 2 detik per aset.
5. **Tidak ada musik** sama sekali di track audio.
6. **Tidak ada harga** ("$45", "45 dollars", "forty-five") di naskah video.
7. **Tidak ada "link di deskripsi" lebih dari sekali.**
8. **Struktur 6 bagian** harus lengkap; bagian "putaran" tidak boleh kosong.
9. **Hash templat** berbeda dari 3 Shorts terakhir.
10. **Nama berkas dan metadata** memuat `ch{NN}` dan `s{N}` supaya UTM bisa
    dicocokkan otomatis.

### Dashboard yang harus dihasilkan mesin

Satu baris per Short, diekspor mingguan:

```
tanggal | ch | beat | durasi | retensi_3s | retensi_akhir | views | klik | utm_content
```

Tiga keputusan yang diambil dari tabel ini:

- `retensi_3s < 60%` → hook salah, ganti (jangan perbaiki videonya)
- `retensi_akhir < 25%` → bagian putaran terlalu lemah
- `klik = 0` pada 20 Shorts → CTA atau audiens salah

---

## 5c. Dua sumber pendapatan — angka yang harus dipegang

Angka ini untuk keputusan, bukan untuk promosi.

**Buku.** $45, fee Gumroad 10% + $0,50 → bersih sekitar **$40 per eksemplar**.

**Shorts.** Bayaran sekitar **$0,03–0,10 per 1.000 views** (bervariasi besar;
audiens AS/Eropa di ujung atas).

Maka:

| Views Shorts | Perkiraan pendapatan iklan | Setara buku |
|---|---|---|
| 100.000 | $3–10 | 0,1–0,25 eksemplar |
| 1.000.000 | $30–100 | 1–2,5 eksemplar |
| 10.000.000 | $300–1.000 | 8–25 eksemplar |

**Kesimpulan operasional:** satu penjualan buku setara 10.000–30.000 views
Shorts. Jadi:

1. **Buku adalah produk; YouTube adalah saluran.** Setiap keputusan produksi
   diuji dengan pertanyaan "apakah ini menambah klik ke Gumroad?"
2. **Jangan mengukur kanal dengan views.** Ukur dengan klik, lalu penjualan.
3. **Long-form tetap wajib**, bukan karena aturan, tapi karena 4.000 jam =
   240.000 menit ≈ 100.000 views long-form — jauh lebih mungkin dicapai
   daripada 10 juta views Shorts dalam 90 hari.
4. **Pendapatan Shorts struktural tidak stabil.** Setelah masuk YPP, penghasilan
   iklan Shorts mensyaratkan 10 juta views per 90 hari berjalan. Turun → berhenti
   (iklan long-form tetap). Jangan pernah menjadikannya tumpuan.

---

## 6. Spesifikasi keluaran

- **Video:** 1920×1080, 24–30 fps, H.264, audio −16 LUFS.
- **Shorts:** 1080×1920, potong dari versi panjang, bukan dibuat terpisah.
- **Judul:** max 70 karakter, memuat tempat atau angka, tanpa huruf kapital semua.
- **Deskripsi:** 3 baris atribusi (lihat `00_BRIEF_CIL.md` bagian 5.1), lalu
  tautan Gumroad, lalu kode.
- **Pinned comment:** satu kalimat CTA + tautan. Bukan dua tautan.
- **Thumbnail:** satu angka besar, satu wajah atau satu citra satelit. Jangan
  tiga-tiganya.

---

## 7. Kalau sumber hilang

Sumber bisa dihapus, diprivat, atau di-geoblock. Aturannya:

1. Jangan ganti dengan klip dari kanal reupload.
2. Kalau klipnya hilang, ganti dengan `quote card` dari `numbers[]` + sumber
   teks. Video tetap bisa terbit tanpa footage.
3. Kalau seluruh sumber hilang, tunda video. Kanal ini tidak kekurangan bahan;
   ia kekurangan alasan untuk buru-buru.

---

## 8. Contoh jadi — Bab 4, spesifikasi acuan

```
JUDUL     Europe's Hottest Summer Killed 61,672 People. Here's What Failed.
DURASI    5:40
------------------------------------------------------------------
0:00-0:22 PERISTIWA   "Heat is the deadliest climate hazard in most
                      years, and the least visible."  [opening_line]
0:22-0:34 QUOTE CARD  61.672 kematian, 30 Mei-4 Sep 2022
                      Ballester et al., Nature Medicine, 2023
0:34-1:50 ANALISIS     kenapa angka 2022 hampir menyamai 2003 padahal
                      lebih panas: rencana pencegahan sudah ada, tetapi
                      tidak menjangkau yang tidak terdaftar
1:50-2:02 NARASI       "2003 was not a missing warning. It was a missing
                      register."
2:02-3:40 LANGKAH      6 langkah, satu per 16 detik, teks di layar
3:40-4:10 ANGKA        apa yang TIDAK diukur: kematian akibat gangguan
                      layanan, bukan hanya suhu
4:10-5:10 KONTEKS      Eropa 2022 vs 2003, adaptasi per derajat
5:10-5:40 CTA          "Chapter 4 is where the book turns heat from
                      weather into arithmetic." + Gumroad
------------------------------------------------------------------
KLIP       0 detik footage berhak cipta (murni quote card +
           citra Copernicus CC BY). Ini yang membuat video ini
           tidak bisa diklaim siapa pun.
```

Perhatikan: contoh ini **tidak memakai satu pun klip berhak cipta**. Itu bukan
kebetulan. Untuk 24 video pertama, format yang paling aman dan paling cepat
adalah kombinasi quote card + citra domain publik/CC BY. Simpan klip podcast
untuk video yang memang butuh — supaya saat Anda memakainya, ada alasan yang
bisa Anda jelaskan.

---

## 9. Satu hal yang akan menentukan umur kanal ini

Studio otomatis akan mendorong Anda ke arah volume: 24 video, lalu 48, lalu
100. Mesin tidak pernah lelah dan tidak pernah bosan. Itu justru risiko
terbesarnya, karena YouTube menilai kanal dari pola, dan pola yang terlalu rapi
terbaca sebagai pabrik.

Peredamnya cuma satu: **biarkan tiap video punya satu hal yang tidak bisa
diulang mesin** — satu kalimat penilaian pribadi, satu koreksi terhadap liputan
media, satu perbandingan lintas bab yang tidak ada di naskah. Kalau pipeline
Anda menyisakan satu slot untuk itu di setiap video, studio ini akan terlihat
seperti karya manusia yang dibantu mesin, bukan sebaliknya.
