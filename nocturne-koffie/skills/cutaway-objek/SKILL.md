---
name: cutaway-objek
description: Kemasan atau objek dipotong-buka di depan kamera: satu gambar acuan diukur, ceklis 12 baris ditulis sebelum satu baris kode, lalu objek dibangun dari kode dengan satu kamera per bagian. Dipakai D4 saat butuh produk yang bagian dalamnya bisa diperiksa, bukan foto kemasan dari satu sudut.
---

# Kemasan Dipotong-Buka — Satu Acuan, Sembilan Kamera

**Sumber:** https://github.com/Nyxera0x/cutaway (61★, MIT) — dari post x.com/Nyxera0x/status/2118689860437315679

Kemasan atau objek dipotong-buka di depan kamera: satu gambar acuan diukur, ceklis 12 baris ditulis sebelum satu baris kode, lalu objek dibangun dari kode dengan satu kamera per bagian. Dipakai D4 saat butuh produk yang bagian dalamnya bisa diperiksa, bukan foto kemasan dari satu sudut. Menghasilkan cutaway/index.html, laporan/cutaway-checklist.md, dan lembar still skema.

# Kemasan Dipotong-Buka — Satu Acuan, Sembilan Kamera

**Posisi skill ini.** `skills/hero-3d` mengurus hero objek hiper-realistis (satu sudut, satu
momen). Skill ini mengurus kebalikannya: objek yang **dibongkar** — bagian demi bagian, tiap
bagian dengan kamera sendiri. Yang dijual bukan kemasannya, tapi keputusan yang kelihatan di
dalamnya: katup aroma, zipper, stiker lot, biji yang benar-benar 250 g.

Sumbernya satu repo, dibaca 7 Nov 2026: **[`Nyxera0x/cutaway`](https://github.com/Nyxera0x/cutaway)**
(61 ★, MIT, 93 berkas, push 6 Nov 2026). Isinya: satu gambar referensi mahluk → objek robotik
yang seluruhnya ditulis dari kode (three.js), halaman dengan satu tombol per bagian, film
60 fps + skor prosedural Python. Contohnya tarantula, piranha, dan wasp — masing-masing tiga
versi (`-shared`, `-film`, `-demo`).

**Yang diambil:** metode kerjanya (ukur acuan → ceklis → still → film), kontrak `render(t)`
murni, aturan satu kamera per ketukan, dan angka seleranya.
**Yang dibuang:** tema robotik, palet hijau, three.js/WebGL, dan pembuatan film
Playwright + ffmpeg — karena di sini tidak ada keduanya. Objeknya juga bukan mahluk, tapi
**kemasan Nocturne** (200 g, label Blue Mount Ijen).

## Kapan dipakai

- Halaman produk yang harus menjelaskan isi kemasan, bukan hanya menjual tampak depan.
- Halaman penawaran B2B: pembeli melihat segel, zipper, katup, dan stiker lot sebelum memutuskan.
- Menjawab pertanyaan pembeli berulang ("apakah ada katup aroma?", "250 g atau 200 g?") dengan
  satu halaman yang bisa diputar, bukan pesan WhatsApp yang diketik ulang.
- **Jangan** dipakai untuk foto produk asli: user minta kemasan dibuat 3D dulu, bukan foto
  ditempel. Juga bukan pengganti `rak/index.html` — rak memilih lot, halaman ini membongkar satu lot.

## Metode tujuh tahap (urutan ini yang membuat hasilnya tidak mengarang)

| # | Tahap | Aturan yang mengikat | Di repo ini jadi |
| ---: | --- | --- | --- |
| 1 | Satu acuan | satu gambar saja, **jangan diimpor** — bangun ulang dari kode | `brand/label-blue-mount-ijen.png` |
| 2 | Ukur gambar | tinggi, lebar, porsi piksel gelap (luma < 80); **ukur, jangan kira-kira** | `tools/cutaway.py` → `UKUR` di `cutaway/data.js` |
| 3 | Ceklis dulu | 10–12 baris bernomor **sebelum** baris kode pertama; setiap kata kabur diberi angka; tulis `NEVER` di samping default yang dilawan | `laporan/cutaway-checklist.md` |
| 4 | Putaran still | masih pose acuan; nilai tiap baris ya/sebagian/tidak; **berhenti setelah putaran 2** dan minta persetujuan user | `cutaway/still/lembar-still.png` |
| 5 | Kamera per ketukan | satu sudut baru untuk tiap bagian, tidak ada yang "parkir" | `KAMERA` (9 entri, 9 sudut) |
| 6 | Kontrak `render(t)` | murni: tanpa `Math.random`/`Date`, state tidak dibawa antar frame; frame 0 = sampul yang sudah bergerak | `cutaway/cutaway.js` |
| 7 | Film + skor | timeline dibaca juga oleh suara; film 60 fps di sini **tidak** dirender | `KETUKAN` (9 ketukan, 25 s) |

## Angka selera yang dipakai apa adanya

| Aturan | Angka | Asal |
| --- | --- | --- |
| Ketukan | tiap 2–3 s | metode Cutaway |
| Bagian terbuka | 1,0 s buka · tahan · 0,55 s tutup | metode Cutaway |
| Objek mengisi jendela | 60–70% tinggi panggung | metode Cutaway |
| Warna aksen | **satu** warna menandai bagian yang bergerak | metode Cutaway (di sini kobalt) |
| Kepadatan tinta | ≥ 0,8 × porsi gelap acuan (14,3% × 0,8 = 11,4%) | ukur acuan |
| Jumlah bagian | 7 (badan, punggung, lipatan ×2, segel, katup, isi, stiker) | desain |

Semua angka di atas masuk `cutaway/data.js` **dan** dicek ulang: `tools/cutaway.py --cek`
membandingkannya dengan citra acuan, `tools/cutaway-uji.mjs` memeriksa kontrak geraknya.

## Kontrak `render(t)` — satu fungsi, semua kebenaran

```js
render(t) → { t, i, ketukan, kamera, terbuka, terbanyak, bukaan }   // murni
```

- `t` yang sama **wajib** menghasilkan keadaan yang sama, urutan pemanggilan tidak berpengaruh.
- `render(0)` harus sama dengan `render(25)` — loop tanpa lompat.
- Semua yang bergerak (kamera, bukaan, goyang halus) adalah fungsi dari `t`; tidak ada timer
  yang menyimpan state. Animasi hanya menjalankan `t` maju.
- Bukaan bagian: `0 → 1` dalam 1,0 s, tahan, lalu `→ 0` dalam 0,55 s. Satu bagian boleh
  terbuka di dua ketukan — saat panel depan disingkirkan supaya isi sangrai kelihatan.

Yang memeriksa semuanya tanpa peramban:

```bash
node tools/cutaway-uji.mjs --verbose   # 38 butir: murni, 9 sudut, loop, tombol, rel
python3 tools/cutaway.py --cek         # angka data.js vs citra acuan
python3 tools/cutaway.py               # bangun ulang data + ceklis
python3 tools/cutaway-still.py         # lembar still skema (PIL, bukan tangkapan layar)
python3 tools/cutaway-luring.py        # satu berkas HTML tanpa tautan luar
```

## Menulis ceklis 12 baris

Urutannya tetap: **siluet & sudut → ciri utama → material → warna aksen → kepadatan**.
Contoh nyata dari repo sumber: ceklis piranha ditulis 12 baris, setelah putaran 2 hasilnya
malah keluar sebagai buaya (rahang 0,52 panjang badan); baris 1 & 3 ditambahkan, putaran 3
dengan angka 0,35 keluar benar. Artinya: **ceklis yang tidak punya angka tidak akan menahan
apa pun.** Baris terakhir selalu porsi gelap.

Ceklis kemasan Nocturne (12 baris, lihat `laporan/cutaway-checklist.md`) memuat: bidang depan
100 × 142,79 satuan, stiker 34 × 13 satuan di 4 satuan depan permukaan, katup 17 satuan
**NEVER** dua, segel 7 satuan **NEVER** lebih tipis dari 5, lipatan 2 × 18 satuan di ±48,
7 biji 7 × 10 satuan, 9 kamera **NEVER** sama, dan 0,8 × tinta.

## Jebakan yang sudah dibayar di repo sumber

- Warna glow HDR > 1 merusak `getHSL` — jangan menaruh > 1 di material.
- Warna yang ditulis ulang pose tiap frame akan kembali ke nilai semula: warna bagian = data.
- Warna di atribut vertex mengabaikan material.
- `smoothstep(a, b, x)` dengan `a > b` berbalik hasilnya di Windows/ANGLE.
- Satu piksel NaN menghitamkan seluruh frame lewat bloom — clamp basis `pow()`.
- Di CSS: nilai bersatuan karangan (`translate3d(30u, …)`) **tidak sah**; kalikan ke piksel
  di JS. Ini pernah lolos di sini dan tertangkap uji, bukan oleh mata.
- Sortir kedalaman mudah terbalik: `perspective` CSS punya kamera di +z, jadi z besar = dekat.

## Batas yang tidak boleh diklaim

| Tahap | Status |
| --- | --- |
| ukur acuan, ceklis, geometri, kontrak `render(t)` | **bisa dibuktikan** — angka + uji tanpa peramban |
| still | **skema** dari `cutaway-still.py`, bukan piksel halaman (rendering teks/bayangan peramban tak bisa ditangkap) |
| film 60 fps + skor | **tidak dirender** — sandbox tanpa Chromium dan tanpa ffmpeg |

Kalau nanti ada peramban + ffmpeg, urutan yang sudah disiapkan repo sumber tetap bisa dipakai:
`node sims/build.mjs <name>-film` → `node sims/capture.mjs … --stills beats --cols 4` →
`python run_sfx.py <score.py>` → gabung `ffmpeg -crf 16 -c:a aac -b:a 256k +faststart`.
