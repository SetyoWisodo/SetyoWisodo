---
name: social-media-riset
description: >
  Riset konten sosial yang ramai untuk dijadikan acuan D3 & D4. Gunakan saat ingin tahu post/video
  sejenis mana yang naik di atas kebiasaan akunnya, kenapa ia bekerja, pola hook apa yang berulang,
  dan format apa yang menyimpan. Menghasilkan swipe file + brief konten siap dikerjakan dari
  data/riset-referensi.csv. Tidak melakukan scraping dan tidak memakai API berbayar.
version: 1.0.0
author: Nocturne Koffie (D3 Marketing × D4 Kreatif)
license: internal
metadata:
  dipakai_divisi: [D3, D4]
  butuh_berkas:
    - data/riset-referensi.csv
    - data/kreatif.json
  keluaran:
    - riset/index.html
    - riset/swipe-file.md
    - riset/brief/brief-*.md
    - riset/data.json
  perintah: python3 tools/riset.py
  izin_akses: baca berkas lokal + tulis folder riset/
---

# Riset Konten Sosial — Outlier & Pola

## Ikhtisar

Tujuan skill ini bukan "cari video yang views-nya besar". Tujuannya menjawab satu pertanyaan yang
bisa dipakai kerja: **pola apa yang membuat konten sejenis naik, dan pola mana yang bisa kita
kerjakan dengan bukti yang kita punya?**

Urutannya: tangkap → normalisasi → baseline → lift → pola → terjemahkan ke sudut kita → brief.

## Kapan dipakai

Pakai saat:

- ingin tahu konten kopi/roastery/kuliner lokal mana yang ramai bulan ini;
- butuh alasan yang bisa dipertanggungjawabkan sebelum membuat 7 konten berikutnya;
- ingin menghentikan format yang sudah 3× tidak menghasilkan chat;
- butuh bahan untuk rapat mingguan D4 (apa yang direkam minggu depan).

Jangan pakai untuk: menyalin konten, mengunduh video orang lain, atau membenarkan klaim
("kompetitor bilang begitu, jadi kita juga").

## Sumber data (dan batasnya)

| Sumber | Status | Catatan |
| --- | --- | --- |
| Tangkapan manual ke `data/riset-referensi.csv` | **aktif** | 10–15 menit/minggu; ambil metrik yang terlihat di layar |
| API pihak ketiga (ScrapeCreators dkk.) | **belum aktif** | butuh kunci berbayar; lihat "Modus API" di bawah |
| Scraping otomatis (Playwright/request ke IG/TikTok) | **tidak dipakai** | melanggar ToS platform dan rapuh |
| Data internal (`data/kpi.csv`, `data/konten-14hari.csv`) | aktif | untuk pembanding performa kita sendiri |

### Kolom `data/riset-referensi.csv`

| Kolom | Isi | Contoh |
| --- | --- | --- |
| `tanggal` | tanggal unggah | `2026-10-12` |
| `platform` | `tiktok`, `instagram`, `marketplace`, `youtube` | `tiktok` |
| `akun` | nama akun (boleh disamarkan) | `(contoh) akun kopi spesialti ID` |
| `url` | tautan post (boleh kosong) | |
| `format` | `reel`, `carousel`, `post`, `story`, `short` | `reel` |
| `hook` | **teks 3 detik pertama / kalimat pertama**, apa adanya | `Kami buang 3 kg kopi minggu ini` |
| `topik` | label bebas | `pengakuan` |
| `detik` | durasi video | `24` |
| `views` | tayangan/plays | `186000` |
| `likes` `komentar` `simpan` `bagikan` | metrik mentah, isi 0 bila tidak terlihat | |
| `followers_akun` | pengikut akun saat itu | `48000` |
| `status` | `contoh` atau `asli` | `asli` |
| `catatan` | kenapa menarik | `kejujuran + angka; komentar banyak bertanya` |

**Aturan pengisian:** satu baris = satu post. Jangan memperkirakan metrik yang tidak tampil —
lebih baik dikosongkan daripada dikarang. Isi minimal 8 baris per platform sebelum menyimpulkan apa pun.

## Alur kerja

1. **Tentukan pertanyaan.** "Format apa yang menyimpan?" berbeda dari "hook apa yang menahan 3 detik?".
   Satu sesi riset = satu pertanyaan.
2. **Kumpulkan 10–20 post** dari 3–5 akun sejenis (bukan hanya akun terbesar — akun kecil yang
   meledak justru lebih informatif).
3. **Normalisasi metrik.** `tools/riset.py` menghitung:
   `ER = (likes + komentar + simpan + bagikan) / views × 100` dan `save rate = simpan / views × 100`.
4. **Hitung baseline per akun × format** memakai **median**, bukan rata-rata (satu post viral tidak
   boleh menggeser patokan). Bila sampel < 3, baseline naik ke level platform, lalu global.
5. **Skor lift.** `lift = views ÷ baseline`. Label: ≥5× outlier besar · 2–5× kuat · 1,5–2× ringan.
6. **Baca polanya, bukan post-nya.** Kelompokkan hook ke taksonomi (angka, larangan, pengakuan,
   diagnosis, banding, pov, tutorial, otoritas, harga, proses). Pola baru dianggap pola bila
   muncul ≥ 2×; bila n=1, brief menandainya *indikatif*.
7. **Terjemahkan ke sudut kita.** Setiap pola dipetakan ke bukti yang kita punya (batch QC, label
   bertanggal, cut-off kirim, harga katalog). Kalau tidak ada buktinya, **jangan pakai pola itu**.
8. **Hasilkan brief** (`riset/brief/brief-NN-*.md`): hook, format, aset dari `data/kreatif.json`,
   bukti yang wajib tampil, keberatan pembeli yang dijawab, CTA, larangan.
9. **Serahkan ke D3** untuk dijadwalkan; ubah status aset di manifest setelah tayang.

```bash
python3 tools/riset.py --cek   # lihat angka dulu, tanpa menulis berkas
python3 tools/riset.py         # tulis dasbor + swipe file + brief
```

## Aturan hitung (deterministik, jangan diubah tanpa alasan tertulis)

| Ukuran | Rumus | Ambang |
| --- | --- | --- |
| Baseline | median views per (akun × format), fallback platform → global bila n < 3 | — |
| Lift | views ÷ baseline | 1,5 · 2 · 5 |
| ER | (like + komentar + simpan + bagikan) ÷ views × 100 | bandingkan antar-format, bukan antar-platform |
| Save rate | simpan ÷ views × 100 | sinyal niat: pilar bukti & edukasi |
| Confidence | dari jumlah baris `asli` saja | <5 sangat rendah · 5–9 rendah · 10–19 sedang · ≥20 tinggi · 0 = belum ada data asli |

Angka tayangan mentah **tidak pernah** dipakai untuk memilih pemenang; hanya lift.

## Format keluaran

```
riset/index.html        dasbor: outlier, pola, matriks format, brief
riset/swipe-file.md     ringkasan untuk dibaca cepat / dikirim ke WA
riset/brief/*.md        satu berkas per brief, siap dikerjakan D4
riset/data.json         ringkasan mesin (dibaca papan harian)
```

## Modus API (opsional, belum aktif)

Bila kelak ada kunci API riset, atur sebagai adapter terpisah:

```
SCRAPECREATORS_API_KEY=...  → scripts/tarik-referensi.py (belum ada)
```

Aturannya tetap: hasil tarikan **ditulis ke CSV yang sama** dan diberi `status=asli` hanya setelah
diperiksa manusia. Selama adapter belum ada, **jangan** menulis di dokumen bahwa kita "mengambil data
otomatis". Ketidaktersediaan alat adalah keputusan, bukan kesuksesan: turunkan klaimnya, jangan
mengarang angka.

## Jebakan

1. **Menilai dari views mentah.** Akun 500 ribu pengikut selalu menang di angka mentah; itu bukan pelajaran.
2. **Mencampur platform dalam satu baseline.** ER TikTok dan carousel IG tidak sebanding.
3. **Menyimpulkan dari n < 5.** Tulis "indikatif", jangan "terbukti".
4. **Menyalin hook persis.** Hook orang lain adalah milik mereka, dan audiens kita bukan audiens mereka.
5. **Memakai pola yang tidak bisa kita buktikan.** "Kami buang 3 kg" hanya boleh kalau ada barisnya di `batch-qc.csv`.
6. **Menganggap contoh sebagai data.** Selama `status=contoh`, seluruh keluaran berlabel peringatan.
7. **Riset tanpa keputusan.** Setiap sesi harus menghasilkan maksimal 3 brief; selebihnya ditunda.

## Etika & kepatuhan

- Hanya konten publik. Tidak ada akun privat, tidak ada data pribadi, tidak ada penyalinan database.
- Kutipan komentar ≤ 24 kata, tanpa nama/akun, untuk memahami bahasa — bukan untuk mempermalukan.
- Tidak mengunggah ulang video/audio/foto pihak lain; tidak memakai musik berhak cipta sebagai aset kita.
- Sebut sumber saat merujuk tren di dokumen internal (nama akun boleh disamarkan).
- Klaim yang lahir dari riset tetap harus lolos gerbang D7 sebelum tayang.

## Pemeliharaan

| Hal | Frekuensi |
| --- | --- |
| Tambah baris referensi | 10–15 menit setiap Sabtu (setelah produksi) |
| Jalankan ulang `tools/riset.py` | setiap ada baris baru |
| Tinjau taksonomi hook | bulanan — tambah pola bila 3 post tidak terklasifikasi |
| Hapus baris lebih tua dari 90 hari | bulanan (pola basi) |
