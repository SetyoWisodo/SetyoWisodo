# OPERASI HARIAN — sistem kerja Cil, dari Senin sampai Minggu

Tanpa ini, semua dokumen lain hanya teori. Ini jadwal, templat, dan urutan
eksekusi yang bisa dijalankan tanpa berpikir ulang setiap hari.

---

# 1. Ritme mingguan

Satu minggu = satu bab. Empat Shorts + satu long-form + satu quote card.

| Hari | Kerja | Keluaran | Waktu |
|---|---|---|---|
| **Senin** | Baca bab di `03_kartu_klip.json`, pilih 4 beat | 4 hook terpilih | 60 mnt |
| **Selasa** | Tulis 4 naskah Short (155 kata @60 dtk) | 4 naskah | 90 mnt |
| **Rabu** | Render Short s1 + s2, jalankan gerbang | 2 Short siap | 90 mnt |
| **Kamis** | Render Short s3 + s4, tulis naskah long-form | 2 Short + 1 naskah | 90 mnt |
| **Jumat** | Render long-form, jalankan gerbang | 1 long-form | 120 mnt |
| **Sabtu** | Upload semua, tulis deskripsi + UTM | 5 video terbit | 60 mnt |
| **Minggu** | Baca dashboard, putuskan minggu depan | 1 keputusan | 30 mnt |

Total: sekitar 9 jam per minggu per bab. Untuk 24 bab: sekitar 216 jam, atau
6–9 bulan pada ritme ini.

**Aturan:** kalau Rabu sudah lewat dan dua Short belum jadi, **jangan**
mengejar ketertinggalan dengan menurunkan kualitas. Kurangi jumlah Short minggu
itu. Volume tidak pernah menyelamatkan hook yang lemah.

---

# 2. Alur per Short (checklist 11 langkah)

Jalankan berurutan. Jangan melompat.

```
[ 1 ] Ambil beat dari 03_kartu_klip.json  -> id, angle, hook, line, note
[ 2 ] Cek hook <= 12 kata                 -> kalau lebih, potong
[ 3 ] Tulis naskah 6 bagian               -> hook/peristiwa/angka/putaran/payoff/jembatan
[ 4 ] Hitung kata                          -> 60 dtk = 150-160 kata
[ 5 ] Pilih aset                           -> quote card dulu, citra PD kedua
[ 6 ] Cek satu angka saja                  -> cocokkan ke numbers[]
[ 7 ] Tulis kredit di layar (>=2 dtk)      -> outlet + tanggal
[ 8 ] Render 1080x1920
[ 9 ] Jalankan 10 gerbang (07 bagian 12)
[10 ] Tulis judul <=60, deskripsi, UTM
[11 ] Catat prediksi sebelum upload        -> lihat bagian 5
```

Langkah 11 tidak biasa, dan itu intinya. Lihat bagian 5.

---

# 3. Templat naskah Short

```
HOOK (0:00-0:02)     [<= 12 kata, angka atau kontradiksi]
PERISTIWA (0:02-0:12) [tempat + tanggal + satu kalimat]
BUKTI (0:12-0:28)     [SATU angka + sumber di layar]
PUTARAN (0:28-0:45)   [apa yang biasanya disalahpahami]
PAYOFF (0:45-1:05)    [1-3 langkah, imperatif]
JEMBATAN (1:05-1:15)  ["That's chapter N. The book is 457 pages."]
```

**Contoh jadi — Bab 13, beat s2 (koreksi):**

> **(0:00) HOOK:** "This was not a renewable energy problem."
> **(0:04) PERISTIWA:** "Texas, February 2021. Four million customers lost
> power in a week of record cold."
> **(0:12) BUKTI:** "The grid was built for summer peaks. On screen: FERC/NERC,
> 2021."
> **(0:22) PUTARAN:** "The failure started at the gas wells. Uninsulated
> wellheads froze, gas pressure dropped, and the plants that burn gas went
> offline. Wind was a small part of the shortfall."
> **(0:40) PAYOFF:** "So the fix isn't fewer turbines. It's insulation on the
> gas supply, backup power for clinics, and interconnections with neighbouring
> grids."
> **(1:02) JEMBATAN:** "That's chapter 13. The book is 457 pages of this."

Perhatikan: 8 detik narasi di hook dan peristiwa, 22 detik di putaran. Bagian
"putaran" **paling panjang**, karena di situlah nilainya.

---

# 4. Templat long-form (5–7 menit)

```
0:00-0:20  PERISTIWA      satu kalimat pembuka buku, dibacakan
0:20-0:50  KENAPA PENTING satu angka, satu kalimat tesis
0:50-2:30  BAGIAN 1       apa yang terjadi, dengan bukti
2:30-4:00  BAGIAN 2       mengapa hasilnya begitu (ini analisis)
4:00-5:30  BILA TERULANG  4-6 langkah, satu per 15-20 dtk
5:30-6:00  PENUTUP        satu kalimat + jembatan ke video berikutnya
```

**Aturan long-form:**
- Tidak ada intro, tidak ada "hai semuanya", tidak ada logo.
- Satu kesimpulan sudah muncul sebelum menit 1.
- Akhir video menunjuk ke video lain di seri, bukan layar kosong.
- Payoff tidak ditunda ke menit terakhir.

---

# 5. Protokol prediksi (ini yang membuat sistem belajar)

Sebelum upload, tulis tiga angka prediksi. Setelah 48 jam, bandingkan.

```json
{
  "video": "ch13-s2",
  "prediksi": {
    "viewed_vs_swiped": 0.72,
    "avg_pct_viewed": 0.78,
    "klik_utm": 4
  },
  "alasan": "hook kontradiksi + satu angka + payoff konkret"
}
```

Kenapa ini penting: tanpa prediksi, Cil hanya melihat angka dan tidak pernah
tahu **apakah keputusannya benar**. Dengan prediksi, setiap video menjadi
eksperimen, dan setelah 12 video Cil punya model sendiri tentang hook mana yang
bekerja untuk audiens ini — sesuatu yang tidak bisa diberikan oleh dokumen mana
pun.

Aturan: kalau prediksi meleset lebih dari 30% pada dua video berturut-turut,
**berhenti dan baca ulang bagian 8 di `09_ALGORITMA.md`**. Berarti model
mentalnya salah, bukan videonya.

---

# 6. Templat deskripsi (salin, jangan dikarang)

```
[Baris 1: satu kalimat isi video, memuat kata kunci alami]

[Baris 2: angka kunci + sumber]

[Baris 3 kosong]

Sources in this video:
- [Outlet], "[judul]", [tanggal]. [URL]

The book: 457 pages, 24 chapters, 152 cited sources.
https://setyowisodo.gumroad.com/l/surviving-the-future?utm_source=youtube&utm_medium=shorts&utm_campaign=chNN&utm_content=sN

Free 36-page sample: [URL sampel]

#climate #shorts #[topik spesifik]
```

**Aturan:** tiga baris pertama harus sudah menjelaskan isinya. Sebagian besar
penonton tidak membuka "selengkapnya". Kalimat pertama juga yang dibaca sistem
untuk search.

---

# 7. Templat komentar yang disematkan

Satu kalimat, satu tautan, satu pertanyaan. Jangan dua tautan.

```
The full sequence — warnings, drills, heat plans, water, drainage, social
protection before sea walls — is chapter 13 of Surviving the Future.
[UTM link]
Which one does your city actually have?
```

Pertanyaan di akhir bukan basa-basi: komentar adalah sinyal engagement, dan
pertanyaan spesifik menghasilkan komentar spesifik yang lebih berbobot daripada
"nice video".

---

# 8. Kalau kehabisan bahan

Tidak akan, tapi kalau terjadi:

1. **Angkat satu langkah** dari `steps_if_repeated[]` menjadi Short sendiri.
   Setiap bab punya 4–10 langkah; itu puluhan Short tambahan tanpa riset baru.
2. **Bandingkan dua bab.** "Chennai dan Cape Town: dua kota, satu kesalahan."
   Ini format yang paling kuat dan paling belum dipakai kanal lain.
3. **Koreksi liputan media.** Ambil satu berita iklim yang salah angka, bandingkan
   dengan sumber primer. Ini konten orisinal sepenuhnya, nol risiko hak cipta.

Ketiganya memakai bahan yang sudah ada di `03_kartu_klip.json`.

---

# 9. Yang tidak boleh dilakukan meski tergoda

- **Jangan** mengunggah 5 Shorts dalam satu hari untuk "mengejar algoritma".
  Itu pola yang justru dibaca sebagai produksi massal.
- **Jangan** mengubah hook video yang sudah terbit. Hapus dan upload ulang
  membuang riwayat sinyal.
- **Jangan** membuat Short tentang topik yang tidak ada di buku, sekadar karena
  sedang tren. Channel ini punya 24 bab; tidak perlu mengejar.
- **Jangan** menjawab komentar dengan templat. Satu balasan yang jelas lebih
  berharga daripada dua puluh "thanks for watching".
- **Jangan** membandingkan diri dengan channel lain. Yang dibandingkan adalah
  video ini dengan video sebelumnya di channel yang sama.

---

# 10. Ringkasan satu halaman (tempel di dinding)

```
SHORTS 45-75 dtk, vertikal
  hook <=12 kata, satu angka, ada putaran, payoff 1-3 langkah
  ukur: viewed-vs-swiped (>70%), % viewed (>80%), engaged views, klik

LONG-FORM 5-7 menit
  satu bab, satu tesis, payoff awal, akhir menunjuk video lain
  ukur: retention 0:30, avg view duration, jam tonton

SETIAP VIDEO
  satu angka, satu sumber, satu jembatan ke bab
  UTM wajib, kredit di layar, nol musik, nol harga di video
  tulis prediksi sebelum upload

SETIAP MINGGU
  baca 6 angka, pilih satu perbaikan, uji satu variabel

BERHENTI KALAU
  12 Shorts <50% viewed-vs-swiped -> ganti hook, bukan tambah volume
  20 Shorts 0 klik -> ganti CTA
  3 bulan 0 penjualan -> tinjau halaman produk
```
