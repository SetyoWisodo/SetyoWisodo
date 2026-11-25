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
| `validate_kartu_klip.py` | studio | validator: keluar kode 1 = jangan render |

Aturan penting: **JSON adalah sumber kebenaran.** Kalau `02` dan `03` berbeda,
JSON menang, dan `02` yang harus diperbaiki. Jangan biarkan mesin membaca
prosa bebas sebagai data.

---

## 2. Kontrak data

`03_kartu_klip.json` **v1.2** (schema 1.2, 25 Nov 2026). Field yang dipakai mesin:

```
chapters[].id                      int 1..24
chapters[].opening_line            kalimat buku, boleh dibacakan (TTS/host)
chapters[].event.{place,date,summary}
chapters[].numbers[]               {claim, value, source, verified}
chapters[].clips[]                 {outlet, item, date, url, format,
                                    speaker, affiliation, quote,
                                    quote_candidate, quote_status,
                                    quote_source, licence_note, use, note}
chapters[].shorts_beats[]          {id, angle, hook, line, note}
chapters[].beat_language           {spoken:"en", note:"id"}
shorts_spec.spoken_field           "line" 
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

**Aturan `quote` yang mengikat mesin:** `quote` hanya boleh terisi kalau
`quote_status` = `verbatim`. Kalimat kerja yang belum diverifikasi disimpan di
`quote_candidate` — jangan pernah dirender sebagai kutipan, dan jangan pernah
dipindahkan ke `quote` tanpa membuka sumbernya dulu. Field `quote_source`
mencatat URL yang dicek, tanggal cek, dan statusnya (`page_verbatim`,
`page_summary_verbatim`, `pending`, `pending_document`).

**Bahasa.** `beat_language.spoken` = `en`. Yang dibacakan TTS/host adalah
`line` (Inggris), **bukan** `hook`. Field `hook` adalah catatan produksi
berbahasa Indonesia untuk Cil — tidak pernah masuk audio, tidak pernah masuk
layar. Validator menolak `line` di atas 12 kata.

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
5. **Kata "AI" — dua arah, bukan satu.** Blokir klaim bahwa **buku** ditulis
   atau dibuat dengan AI ("dibuat dengan AI", "written by AI", "AI-generated
   book", nama model). Tapi **jangan** blokir, dan justru **wajibkan**,
   disclosure untuk video: setelan "AI use" di YouTube Studio dinyalakan bila
   ada suara sintetis yang meniru orang nyata, visual sintetis realistis, atau
   musik AI sebagai fokus. Narasi TTS untuk naskah sendiri tidak wajib
   dilabeli, tapi labelnya gratis dan menambah kepercayaan — nyalakan saja.
   Gerbang lama memindai kata "AI" lalu memblokir, dan itu bisa memblokir
   justru kalimat disclosure yang diwajibkan platform.
6. **Musik.** Tolak track apa pun yang tidak berasal dari YouTube Audio Library
   atau lisensi yang tersimpan di manifes aset.
7. **Templat — hash saja tidak cukup.** Hash struktur (urutan + panjang
   segmen) hanya menangkap variasi mekanis. YouTube secara eksplisit menyebut
   "AI-generated content made with generic or unoriginal templates giving the
   impression of mass production" sebagai inauthentic. Karena itu ada dua
   gerbang: (a) hash struktur berbeda dari 3 video terakhir — peringatan saja,
   dan (b) **gerbang manusia wajib**: setiap video harus punya minimal satu
   dari empat hal yang tidak bisa diulang mesin, dicatat di field
   `original_element` di manifes. Kalau kosong, video tidak boleh terbit.
8. **Atribusi.** Setiap aset di timeline harus punya baris atribusi di deskripsi
   yang dihasilkan. Aset tanpa atribusi = gagal render.
9. **Kode diskon.** Hanya `LAUNCH20` dan `KAMPUS25` yang boleh muncul. Apa pun
   selain itu, blokir.

10. **Bahasa beat.** Naskah Short wajib bahasa Inggris; field `line` adalah
    sumbernya. Kalau detektor bahasa menemukan kalimat Indonesia di naskah
    yang akan dibacakan, tolak.

11. **Klip belum siap.** Kalau bab masih punya klip `to_source` atau
    `paraphrase_check_before_use`, mesin menolak render bab itu. Jalankan
    `python3 validate_kartu_klip.py --siap` untuk daftar yang boleh.

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
4. **Satu hal yang tidak bisa diulang mesin.** Wajib, dan dicatat di manifes
   sebagai `original_element`: penilaian pribadi satu kalimat, koreksi terhadap
   liputan media, atau perbandingan lintas bab. Ini gerbang terakhir sebelum
   render. Tanpa ini, 96 Shorts dengan struktur sama akan lolos semua hash dan
   tetap terbaca sebagai pabrik oleh reviewer manusia — persis contoh yang
   disebut YouTube untuk konten inauthentic.

---

## 5. Pipeline yang saya sarankan

```
[0] cek siap             -> python3 validate_kartu_klip.py --siap

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

### Gerbang algoritma (bukan hak cipta — ini soal distribusi)

Mesin juga harus menolak render kalau:

11. **Hook tidak memuat angka, kontradiksi, atau nama tempat.** Hook generik
    ("iklim makin buruk") gagal di viewed-vs-swiped.
12. **Tidak ada bagian "putaran"** (koreksi terhadap anggapan umum). Ini satu-
    satunya bagian yang menghasilkan komentar substantif.
13. **Judul > 60 karakter** atau memuat huruf kapital semua.
14. **Tidak ada UTM** pada tautan, atau `utm_campaign` tidak cocok dengan bab.
15. **Tiga angka atau lebih** muncul di naskah Short (aturan: satu).

Dan mesin harus **mewajibkan prediksi** sebelum upload:

```json
{"video":"ch13-s2","prediksi":{"viewed_vs_swiped":0.72,
 "avg_pct_viewed":0.78,"klik_utm":4},"alasan":"..."}
```

Setelah 48 jam, dashboard membandingkan prediksi dengan hasil. Tanpa ini,
mesin hanya menghasilkan video; dengan ini, mesin menghasilkan **model** tentang
apa yang bekerja untuk audiens ini.

### Dashboard yang harus dihasilkan mesin

Satu baris per Short, diekspor mingguan:

```
tanggal | ch | beat | durasi | viewed_vs_swiped | avg_pct_viewed |
engaged_views | retention_0_30 | klik | utm_content | prediksi | selisih
```

Kolom `engaged_views` wajib ada dan **menggantikan** `views` sebagai angka
pembanding. Sejak 31 Maret 2025 satu view dihitung saat video mulai diputar,
jadi headline views tidak lagi sebanding antar waktu atau antar video.

Tiga keputusan yang diambil dari tabel ini:

- `retensi_3s < 60%` → hook salah, ganti (jangan perbaiki videonya)
- `retensi_akhir < 25%` → bagian putaran terlalu lemah
- `klik = 0` pada 20 Shorts → CTA atau audiens salah

---

## 5c. Dua sumber pendapatan — angka yang harus dipegang

Angka ini untuk keputusan, bukan untuk promosi. Semua angka di sini juga ada di
`03_kartu_klip.json` → `economics`, supaya mesin dan manusia tidak bisa berbeda.

**Buku.** $45. Direct: fee Gumroad 10% ($4,50) + $0,50, kartu 2,9% ($1,31) +
$0,30 → **bersih $38,40**. Discover (Gumroad yang menemukan pembeli): 30% flat,
proses termasuk → **bersih $31,50**. Kalau 80% penjualan direct dan 20%
Discover, angka campuran yang dipakai untuk perencanaan: **$37,02**. Pakai
$38,40 sebagai default, $31,50 untuk skenario konservatif.

**Shorts.** Bayaran iklan sekitar **$0,03–0,10 per 1.000 views**; laporan
industri 2026 (AIR Media-Tech, 274 kanal) memberi rentang tipikal $0,07–0,20
dan $0,33 untuk audiens AS. Itu laporan pihak ketiga, bukan angka YouTube —
pakai untuk perencanaan, jangan untuk janji.

Maka:

| Views Shorts | Pendapatan iklan | Setara buku (iklan saja) |
|---|---|---|
| 100.000 | $3–10 | 0,08–0,26 eksemplar |
| 1.000.000 | $30–100 | 0,8–2,6 eksemplar |
| 10.000.000 | $300–1.000 | 8–26 eksemplar |

**Kesimpulan operasional — dan ini yang berubah dari versi sebelumnya:** satu
penjualan buku setara **384.000–1.280.000 views iklan Shorts**, bukan
10.000–30.000. Angka lama itu salah hitung 30–40 kali lipat; ia tercampur
dengan asumsi funnel (lihat di bawah). Konsekuensinya keras, dan sebaiknya
dihadapi sekarang:

1. **Pendapatan iklan Shorts tidak akan pernah membiayai kanal ini.** Pada
   $0,07/1.000, satu juta views = $70. Satu buku = $38,40. Jadi buku jauh lebih
   bernilai per orang, dan seluruh desain kanal harus diarahkan ke klik.
2. **Funnel bisa masuk akal, tapi belum diukur.** Kalau 0,05–0,3% penonton
   mengklik dan 1–3% dari yang mengklik membeli, satu buku datang dari
   **11.000–200.000 views** (skenario dingin) atau **10.000–30.000** (skenario
   hangat, audiens yang sudah mengenal Anda). Angka lama adalah skenario
   hangat yang ditulis seolah hukum. `funnel_assumptions` di JSON menandainya
   sebagai asumsi; ganti dengan data 12 Shorts pertama.
3. **Long-form tetap wajib**, dan bukan karena aturan: 4.000 jam ≈ 100.000
   views long-form, dan long-form juga membayar jauh lebih baik — pada RPM
   $2,50–5,00, 100.000 views = **$250–500**, atau 6–13 buku setara iklan.
4. **Pendapatan Shorts struktural tidak stabil.** Setelah masuk YPP, penghasilan
   iklan Shorts mensyaratkan 10 juta views per 90 hari berjalan. Turun → berhenti
   (iklan long-form tetap). Jangan pernah menjadikannya tumpuan.

---

## 6. Spesifikasi keluaran

- **Video:** 1920×1080, 24–30 fps, H.264, audio −16 LUFS.
- **Shorts:** 1080×1920, **dibangun dari `shorts_beats` di
  `03_kartu_klip.json`, bukan dipotong dari long-form.** Empat beat per bab,
  masing-masing jadi satu Short. Memotong long-form dilarang — lihat
  `01_KIRIM_KE_CIL.md`.
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

**Status data per 25 November 2026 — baca ini sebelum mempercayai kartu.**
`verified: true` di `numbers[]` berarti **angka itu ada di dalam buku**, bukan
bahwa ia sudah dicek ulang ke sumber primer hari ini. 61 dari 72 angka masih
bersumber pada "buku bab N" tanpa nama lembaga atau nomor halaman. Untuk video,
itu cukup — buku adalah sumbernya, dan Anda penulisnya. Tapi untuk video yang
mengutip **lembaga**, buka dokumennya. Untuk kutipan, hanya `quote` dengan
`quote_status: verbatim` yang boleh diberi tanda kutip; sisanya ada di
`quote_candidate` dan **tidak boleh dirender sebagai kutipan**.

Validator akan mengingatkan ini setiap kali dijalankan (`warn W1`). Itu bukan
gangguan; itu daftar kerja.

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

## 8b. Perbaikan dari review Cil — 25 November 2026

Review eksternal menemukan tiga hal yang mengubah dokumen ini. Ringkasnya, supaya
tidak ada yang mengulang kesalahan yang sama:

| Temuan | Status |
|---|---|
| Ekonomi salah 30–40× ("1 buku = 10.000–30.000 views") | **Diperbaiki**: §5c dan `economics` di JSON. Ekuivalensi iklan = 384.000–1.280.000 views; 10.000–30.000 adalah asumsi funnel audiens hangat dan sekarang dilabeli begitu. |
| "Shorts dipotong dari long-form" bertentangan dengan larangan di `01` | **Diperbaiki**: §6. Shorts dibangun dari `shorts_beats`. |
| Target >70% / >80% tanpa dasar, bisa membunuh kanal baru | **Diperbaiki**: lihat §8c. Minggu 1–4 = baseline, bukan gerbang. |
| Hash struktur terlalu lemah untuk risiko inauthentic | **Diperbaiki**: gerbang manusia ke-4 (`original_element`) di §4, dan gerbang 7 dipecah dua. |
| Gerbang 5 memblokir kata "AI" termasuk disclosure yang diwajibkan | **Diperbaiki**: §3 gerbang 5, dua arah. |
| Versi skema 1.0 di sini vs 1.1 di JSON | **Diperbaiki**: v1.2 di keduanya, dengan validator. |
| Beat: hook Indonesia, line Inggris — ambigu | **Diperbaiki**: `beat_language`, `spoken_field: line`. |

Tiga hal yang review tidak bisa selesaikan dan tetap keputusan Anda: **siapa
host-nya** (§8d), **nama dan handle kanal** (§8e), dan **apakah semua klip
`to_source` akan diverifikasi atau diganti quote card** (validator memberi
daftarnya setiap kali dijalankan).

---

## 8c. Baseline sebelum target — mengapa angka 70% diturunkan

Versi sebelumnya menulis "viewed vs swiped > 70%" dan "avg % viewed > 80%"
sebagai target di minggu pertama. Itu keliru, dan bukan karena angkanya terlalu
tinggi — tapi karena **belum ada yang bisa dibandingkan**. Kanal ini belum
punya satu video pun, jadi tidak ada baseline.

Aturan yang berlaku sekarang:

1. **Minggu 1–4: ukur, jangan nilai.** Empat belas video pertama (12 Shorts + 2
   long-form) dijalankan tanpa ambang. Yang dikumpulkan: viewed-vs-swiped, avg %
   viewed, retensi 0:30, engaged views, klik UTM.
2. **Minggu 5: tetapkan baseline** = median dari 12 Shorts pertama. Itu angka
   Anda, bukan angka orang lain.
3. **Target = baseline + 10 poin persentase**, bukan 70%. Kalau baseline 41%,
   target 51%. Kalau baseline 68%, target 78%.
4. **70% / 80% tetap ada sebagai aspirasi**, dicetak di dinding, tapi bukan
   gerbang yang memicu "ganti hook". Yang memicu perbaikan adalah **tren**, bukan
   angka absolut.
5. **Aturan berhenti tetap 50%** — di bawah itu, hook-nya memang salah, bukan
   targetnya.

---

## 8d. Host dan disclosure — keputusan yang harus diambil sebelum video pertama

Ini satu-satunya keputusan di paket ini yang **tidak bisa** diselesaikan dengan
dokumen. Pilih satu, tulis di `00_BRIEF_CIL.md` §1.4, lalu jangan diubah lagi
selama 13 minggu:

**Pilihan A — host manusia.** Suara Anda, wajah opsional. Tidak ada label AI.
Jadwal 11–13 jam/minggu harus ditambah 60–90 menit rekaman per bab, dan itu berarti
ritme 1 bab/minggu menjadi 1 bab/10 hari. Kelebihan: kredibilitas, dan tiap video
otomatis punya `original_element`.

**Pilihan B — TTS.** Suara sintetis untuk naskah sendiri. Tidak wajib dilabeli
menurut halaman bantuan YouTube (label wajib untuk yang **realistis dan bisa
disalahartikan sebagai nyata** — meniru orang nyata, mengubah footage peristiwa
nyata, atau musik AI sebagai fokus). Tapi nyalakan saja setelan "AI use": biayanya
nol, dan risikonya kalau tidak dinyalakan lebih besar dari manfaatnya. Kelebihan:
ritme 1 bab/minggu realistis. Kekurangan: `original_element` harus disuntik
manual di setiap naskah, karena suara saja tidak lagi membuktikan kehadiran
manusia.

**Pilihan C — hybrid (rekomendasi).** TTS untuk 96 Shorts, suara Anda untuk 24
long-form. Yang dibaca TTS adalah `line` (Inggris) yang sudah Anda setujui; yang
direkam adalah analisis dan penilaian pribadi — bagian yang justru membuat
long-form layak ditonton 5–7 menit. Biaya: satu sesi rekaman per bab.

**Yang tidak boleh:** mencampur tanpa aturan. Kalau satu video TTS dan video
berikutnya suara manusia tanpa alasan di dalam cerita, penonton membaca itu
sebagai ketidakkonsistenan, dan YouTube membaca pola suara sebagai sinyal
otomasi.

---

## 8e. Yang masih kosong — isi sebelum upload pertama

Empat hal ini tidak ada di paket mana pun, dan semuanya dibutuhkan mesin:

| Yang kosong | Kenapa penting | Diisi di |
|---|---|---|
| Nama kanal + handle | UTM tidak bisa diaudit tanpa identitas tetap; nama juga muncul di deskripsi | `00_BRIEF_CIL.md` §1.4 |
| Jam upload (WIB → London/New York) | Audiens target AS/Eropa; mengunggah 03.00 WIB = 20.00 London sebelumnya | `10_OPERASI_HARIAN.md` §1 |
| Alat dashboard | Kolom sudah ditentukan, alatnya belum: spreadsheet 6 kolom atau skrip | keputusan Anda; format kolom ada di §5b |
| SOP komentar & koreksi | Video iklim akan dikoreksi orang; jawaban pertama menentukan nada seluruh komentar | `10_OPERASI_HARIAN.md` §10 |

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

---

## 10. Batas paket ini — yang tidak boleh dijanjikan ke siapa pun

Tiga hal ini sering dijanjikan orang yang membuat sistem seperti ini, dan
ketiganya tidak benar:

1. **"Kalau ikut sistem ini, kanal akan monen."** Tidak. Sistem ini
   memaksimalkan peluang: tidak ada klaim hak cipta, tidak ada pelanggaran
   inauthentic, dan setiap video punya alasan untuk ditonton. Distribusi tetap
   keputusan YouTube, per penonton, dan tidak bisa dijamin.
2. **"1 juta views = 30 buku."** Tidak. Satu juta views iklan = $30–100. Satu
   juta views dengan funnel yang bekerja mungkin menghasilkan 3–30 buku, tapi
   itu tergantung produk, harga, dan audiens — bukan pada views.
3. **"Short lebih penting daripada long-form."** Tidak. Shorts membawa
   jangkauan; long-form membayar dan memenuhi syarat monetisasi. Tanpa
   long-form, seluruh beban ada pada 10 juta views Shorts per 90 hari.

Yang boleh dijanjikan, dan cukup: **setiap video akan punya sumber yang bisa
ditunjuk, kutipan yang benar-benar diucapkan, satu hal yang tidak bisa diulang
mesin, dan angka yang bisa dibandingkan dengan video sebelumnya.**
