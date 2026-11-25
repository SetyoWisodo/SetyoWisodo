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
