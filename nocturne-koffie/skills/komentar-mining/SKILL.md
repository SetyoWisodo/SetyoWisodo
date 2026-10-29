---
name: komentar-mining
description: >
  Menambang komentar publik untuk menemukan bahasa pembeli: keberatan, pertanyaan yang berulang,
  permintaan, dan kalimat yang bisa langsung dipakai jadi caption atau FAQ. Menghasilkan rekap
  jenis komentar + daftar tindakan. Dipakai D3 saat butuh copy yang terdengar seperti pembeli,
  bukan brosur. Kutipan dipotong ≤ 24 kata dan tanpa identitas.
version: 1.0.0
author: Nocturne Koffie (D3 Marketing)
license: internal
metadata:
  dipakai_divisi: [D3, D2]
  butuh_berkas: [data/riset-komentar.csv]
  keluaran: [riset/index.html (bagian 4), riset/swipe-file.md]
  perintah: python3 tools/riset.py
  izin_akses: baca berkas lokal + tulis folder riset/
---

# Komentar Mining — bahasa pembeli → copy

## Ikhtisar

Caption yang bagus memakai kata yang sudah dipakai pembeli. Komentar publik adalah satu-satunya
tempat kata itu muncul tanpa disaring. Skill ini mengubah komentar menjadi tiga keluaran kerja:
**keberatan** (untuk dijawab), **pertanyaan** (untuk FAQ & slide), **permintaan** (untuk dijual/ditolak).

## Kapan dipakai

- sebelum menulis batch caption mingguan (Selasa, 90 menit);
- saat ada 3+ komentar bernada sama dalam seminggu;
- saat ingin tahu kenapa orang **tidak** membeli;
- saat menyusun FAQ WhatsApp otomatis atau jawaban marketplace.

## Sumber data

`data/riset-komentar.csv` — diisi manual, satu baris = satu kutipan bermakna.

| Kolom | Isi | Nilai yang dikenal |
| --- | --- | --- |
| `tanggal` | kapan komentar diambil | `2026-10-16` |
| `platform` | asal komentar | `tiktok`, `instagram`, `marketplace`, `whatsapp` |
| `sumber` | label post/akun, boleh disamarkan | `(contoh) kolom komentar reel pahit` |
| `kutipan` | kalimat pembeli, **apa adanya**, ≤ 24 kata | `pahitnya karena gilingan atau suhu air?` |
| `jenis` | `keberatan` `pertanyaan` `pujian` `permintaan` `harga` | `pertanyaan` |
| `produk` | SKU/paket yang disebut, bila ada | `gilingan` |
| `tindakan` | apa yang akan kita lakukan dengan kalimat ini | `jadi slide edukasi gilingan` |

**Jangan** menyalin seluruh komentar panjang, nama akun, nomor telepon, atau alamat. Ambil
kalimatnya saja. Ini bukan riset identitas orang.

## Alur kerja

1. **Kumpulkan 10–15 komentar** dari 3–5 post (post kita dan post sejenis). Prioritaskan komentar
   yang mengandung pertanyaan, keluhan, atau angka.
2. **Pendekkan ke inti.** Buang basa-basi; sisakan kalimat yang bisa dijawab.
3. **Beri `jenis`.** Satu baris satu jenis. Kalau ragu antara keberatan dan pertanyaan: pertanyaan
   meminta informasi, keberatan menolak membeli.
4. **Tulis `tindakan`.** Harus berupa kerja nyata: "jadi slide 2", "masuk FAQ", "tindak lanjut B2B".
   Kalau tidak ada tindakannya, hapus barisnya — komentar tanpa tindakan hanya jadi arsip.
5. **Jalankan** `python3 tools/riset.py` → rekap jenis + kutipan di bagian 4 dasbor.
6. **Terjemahkan:**
   - setiap **keberatan** → satu slide carousel atau satu beat video;
   - setiap **pertanyaan** yang muncul ≥2× → FAQ WhatsApp + satu Story;
   - setiap **harga** → sebut harga per gram di caption;
   - setiap **permintaan** grosir → serahkan ke D2 (jangan dijawab dengan janji di kolom publik).
7. **Perbarui** `.md` FAQ/WhatsApp yang terkait, bukan hanya CSV.

## Aturan pengutipan

| Aturan | Alasan |
| --- | --- |
| ≤ 24 kata (dipotong otomatis oleh `riset.py`) | mengambil inti, bukan menyalin percakapan |
| Tanpa nama, foto, nomor, alamat | privasi pembeli |
| Tidak menampilkan komentar sebagai bahan olok-olok | reputasi jangka panjang |
| Boleh menyebut "banyak yang bertanya…" | pola, bukan individu |

## Format keluaran

- **Rekap jenis** — berapa keberatan, pertanyaan, permintaan, harga.
- **Kutipan bertindak** — maksimal 3 per jenis di dasbor, semuanya di swipe file.
- **Umpan ke brief** — brief D4 otomatis memuat 3 keberatan terbaru yang harus dijawab.
- **Rekomendasi FAQ** — pertanyaan berulang dipakai menyusun balasan WhatsApp.

## Jebakan

1. **Mengarang kutipan** agar caption terasa hidup. Kalau tidak ada kalimatnya, jangan dibuat.
2. **Mengambil komentar dari akun pesaing lalu menyerangnya.** Boleh belajar, tidak boleh menyerang.
3. **Menjawab keluhan di kolom publik dengan janji.** Semua janji lewat WhatsApp, setelah dicek.
4. **Menganggap "pujian" sebagai data.** Pujian tidak butuh tindakan; simpan maksimal 1 baris/bulan.
5. **Menumpuk 60 komentar tanpa mengubah satu pun caption.** Ukur keberhasilan skill ini dari
   perubahan aset, bukan dari jumlah baris CSV.

## Keterkaitan

| Ke | Apa |
| --- | --- |
| `skills/social-media-riset` | sumber komentar (post yang dianalisis) |
| `skills/search-intent-riset` | pertanyaan berulang → kata kunci yang dicari orang |
| `marketing/02-copy-library.md` | tempat kalimat pembeli dipindahkan |
| `operasional/divisi/D2-penjualan-crm.md` | tempat keberatan dijawab (chat, bukan publik) |
