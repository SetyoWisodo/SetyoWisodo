---
name: search-intent-riset
description: >
  Riset mesin pencari untuk D3: Google, pencarian marketplace, pencarian TikTok, dan mesin jawaban AI.
  Mengubah daftar kata kunci menjadi prioritas kerja, menemukan celah antara yang dicari orang dan
  yang benar-benar tertulis di halaman kita, lalu menunjuk halaman mana yang harus diperbaiki.
  Membaca halaman target langsung (bukan menebak) dan tidak mengarang volume pencarian.
version: 1.0.0
author: Nocturne Koffie (D3 Marketing)
license: internal
metadata:
  dipakai_divisi: [D3]
  butuh_berkas: [data/riset-kata-kunci.csv, index.html, kampanye/index.html, komersial/penawaran-b2b.html]
  keluaran: [riset/index.html (bagian 5), riset/swipe-file.md]
  perintah: python3 tools/riset.py
  izin_akses: baca berkas lokal + tulis folder riset/
---

# Riset Niat Pencarian — Google, marketplace, TikTok, mesin jawaban

## Ikhtisar

Konten sosial memancing orang yang **belum** mencari. Mesin pencari menangkap orang yang **sudah**
mencari. Dua-duanya perlu, dan tugas skill ini yang kedua: memastikan saat orang mengetik
"kopi banyuwangi" atau "grosir kopi banyuwangi", ada halaman kita yang benar-benar menjawab.

Skill ini **tidak** mengarang angka volume pencarian. Yang dipakai adalah skala relatif 1–5 yang
diberi owner berdasarkan hasil lihat manual (autocomplete, jumlah hasil, jumlah review toko,
"pencarian terkait"), dan dicatat tanggalnya.

## Kapan dipakai

- sebelum menulis halaman baru (atau menambah bagian di halaman lama);
- saat ingin tahu mengapa halaman ada tapi tidak didatangi;
- saat menyusun judul listing marketplace;
- saat menyiapkan jawaban untuk mesin jawaban AI (ChatGPT/Perplexity/Google AI) yang menjawab
  pertanyaan orang tentang kopi Banyuwangi.

## Sumber data

`data/riset-kata-kunci.csv`:

| Kolom | Isi | Nilai yang dikenal |
| --- | --- | --- |
| `kata_kunci` | frasa yang dicari orang, apa adanya | `grosir kopi banyuwangi` |
| `mesin` | `google` · `marketplace` · `tiktok` · `wa` | `google` |
| `niat` | `beli` · `lokal` · `banding` · `info` | `beli` |
| `volume_skala` | **skala relatif 1–5**, bukan angka absolut | `3` |
| `kesulitan` | 1 (mudah) – 5 (sulit), dari lihat hasil teratas | `2` |
| `halaman_target` | berkas halaman yang harus menjawab | `index.html` |
| `catatan` | alasan / temuan manual | `kompetisi rendah` |

**Cara mengisi skala volume (5 menit per kata kunci):** ketik di Google/kolom pencarian marketplace,
lihat apakah autocomplete muncul, berapa hasil "beriklan", dan berapa toko yang menawarkan hal
serupa. 5 = sangat sering & banyak pemain; 1 = hampir tidak ada. Tulis tanggal riset di commit
atau `catatan`. Jangan menyalin angka dari tool berbayar tanpa menyebut sumbernya.

## Alur kerja

1. **Kumpulkan 10–20 frasa** dari tiga sumber: autocomplete Google, pencarian marketplace
   (Shopee/Tokopedia), pencarian TikTok; tambahkan frasa dari `skills/komentar-mining`
   (pertanyaan pembeli = kata kunci yang belum terlayani).
2. **Beri niat.** Niat menentukan bobot. "beli" dan "lokal" bernilai uang; "info" bernilai jangkauan.
3. **Tunjuk halaman target.** Kalau tidak ada halaman yang cocok, biarkan kosong — itu temuan,
   bukan kesalahan.
4. **Jalankan** `python3 tools/riset.py`. Skrip membuka berkas halaman target, membuang tag,
   lalu **mencocokkan kata kunci ke teks halaman**:
   - `tercakup` = frasa utuh muncul;
   - `sebagian` = ≥60% kata muncul (halaman menyebut topiknya, tapi tidak menjawab frasa itu);
   - `belum` = halaman tidak membahasnya;
   - `belum ada halaman` / `halaman tidak ditemukan`.
5. **Baca prioritas:** `prioritas = volume_skala × bobot_niat ÷ kesulitan`.
   Bobot: beli 1,4 · lokal 1,3 · banding 1,2 · info 0,8.
6. **Kerjakan yang celah + prioritas tinggi**, dengan urutan: perbaiki halaman yang sudah ada →
   tambah bagian → baru buat halaman baru (situs kecil jangan dipecah terlalu cepat).
7. **Tulis jawabannya di halaman, bukan di meta tag saja.** Halaman yang menjawab = ada harga,
   ada cara pesan, ada bukti (tanggal sangrai/kode batch), ada wilayah layanan.
8. **Ukur ulang bulanan.** Isi ulang `volume_skala`/`kesulitan` hanya bila ada perubahan nyata,
   dan catat tanggalnya.

## Peta kata kunci → halaman (yang berlaku sekarang)

| Frasa | Niat | Halaman | Status dihitung skrip |
| --- | --- | --- | --- |
| kopi banyuwangi | lokal | `index.html` | dicek |
| kopi arabika ijen | beli | `kampanye/index.html` | dicek |
| grosir kopi banyuwangi | beli | `komersial/penawaran-b2b.html` | dicek |
| kopi robusta 1 kg harga | banding | `komersial/harga-grosir.csv` | dicek (CSV dibaca sebagai teks) |
| cara menyimpan kopi | info | — | belum ada halaman → jawab lewat konten |

## Mesin jawaban AI (AEO) — tambahan, bukan pengganti SEO

Mesin jawaban mengutip halaman yang **tegas dan spesifik**. Untuk itu setiap halaman jual wajib punya:

| Elemen | Contoh yang benar | Contoh yang gagal |
| --- | --- | --- |
| Harga eksplisit | “Rp23.000 / 100 g · Rp152.000 / 1 kg” | “harga terjangkau” |
| Nama & tempat | “disangrai mingguan oleh Ais Coffee Roastery, Banyuwangi” | “roastery lokal” |
| Batas layanan | “kirim hari sama untuk order sebelum 15.00 WIB, Senin–Sabtu” | “pengiriman cepat” |
| Bukti yang bisa dicek | “tanggal sangrai + kode batch di tiap kantong” | “kualitas terjamin” |

Kalimat di atas sudah ada di `data/catalog.json` dan `kampanye/index.html` — tugas riset adalah
memastikan frasa yang dicari orang benar-benar **muncul** di sana, bukan hanya di file data.

## Format keluaran

- Tabel kata kunci dengan prioritas + status cakupan (bagian 5 dasbor).
- Daftar **celah**: kata kunci berniat beli yang belum dijawab halaman mana pun.
- Rekomendasi 3 tindakan pertama: perbaiki halaman X / tambah bagian Y / tunda Z.

## Jebakan

1. **Mengarang volume pencarian.** Tidak ada akses data resmi di sini; skala relatif wajib disebut
   sebagai perkiraan.
2. **Menulis untuk robot, bukan pembeli.** Halaman yang penuh kata kunci tapi tanpa harga akan
   ditinggalkan pembeli — dan itu tetap kalah.
3. **Membuat 6 halaman baru untuk 6 kata kunci.** Situs kecil kehilangan kekuatan; tambah bagian
   di halaman yang sudah ada lebih dulu.
4. **Lupa memperbarui halaman setelah harga berubah.** Harga usang merusak kepercayaan lebih cepat
   daripada tidak ada halaman.
5. **Menganggap marketplace sama dengan Google.** Di marketplace yang menang adalah judul + foto +
   ulasan, bukan panjang artikel.
6. **Menjanjikan peringkat.** Skill ini tidak bisa menjamin posisi di mesin pencari; yang bisa
   dijamin hanya bahwa halaman menjawab frasa yang dicari.

## Pemeliharaan

| Hal | Frekuensi |
| --- | --- |
| Tambah frasa baru (autocomplete + komentar) | bulanan, 20 menit |
| Jalankan `tools/riset.py` | setiap kali halaman/harga berubah |
| Tinjau celah | bulanan, sebelum memutuskan halaman baru |
| Perbarui skala volume | per kuartal (atau bila ada perubahan pasar) |
