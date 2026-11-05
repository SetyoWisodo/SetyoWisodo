---
name: gaya-gambar
description: Pustaka gaya gambar untuk Nocturne Koffie — 20 gaya dari fotografi produk sampai poster cetak, masing-masing dengan prompt, daftar negatif, rasio, dan cara membangunnya tanpa generator. Dipakai saat butuh gambar baru (hero, poster, kartu rasa, konten organik) atau saat menilai gambar hasil generator sebelum dipasang.
---

# Gaya Gambar — dari kata kunci sampai berkas jadi

Sumber gagasan, semuanya ≥ 3.000 bintang dan berlisensi jelas (diperiksa 5 Nov 2026):

| Repo | Bintang | Yang diambil | Yang **tidak** diambil |
| --- | --- | --- | --- |
| [`freestylefly/awesome-gpt-image-2`](https://github.com/freestylefly/awesome-gpt-image-2) (MIT) | 35.482 | taksonomi 22 template (product, poster, photography, illustration, 3D, character, infographic, brand, document) + pola **Guidance / Pitfalls** per template | 530 contoh gambar & berkas gambar repo (237 MB), akun & kredit API |
| [`willwulfken/MidJourney-Styles-and-Keywords-Reference`](https://github.com/willwulfken/MidJourney-Styles-and-Keywords-Reference) (tanpa lisensi — hanya dibaca sebagai referensi kata) | 12.314 | daftar kata medium, pencahayaan, dan gaya yang bisa dipakai ulang | teksnya tidak disalin; repo tanpa lisensi jadi **tidak boleh** dijadikan sumber kutipan |
| [`ZeroLu/awesome-nanobanana-pro`](https://github.com/ZeroLu/awesome-nanobanana-pro), [`jamez-bondos/awesome-gpt4o-images`](https://github.com/jamez-bondos/awesome-gpt4o-images) (MIT) | 10.377 · 8.157 | pola "prompt + hasil yang bisa dilihat" — prompt tanpa contoh hasil tidak dipercaya | prompt gaya yang bertumpu pada nama seniman hidup |
| `tools/gaya.py` (milik proyek ini) | — | empat perlakuan deterministik dari satu render: film gelap, warna polos, monokrom, arsir cetak | — |

Hasil: **`data/gaya-gambar.json`** — 20 gaya, enam kategori, tiap gaya punya `prompt`, `negatif`, `rasio`, `alat`
(`generator` / `pillow` / `keduanya`).

## Kapan dipakai

- Butuh gambar baru untuk hero, poster, kartu rasa, konten organik.
- Hasil generator terlihat "AI" dan perlu diperbaiki sebelum dipasang.
- Ingin gaya yang **bisa diulang**: kalau hasilnya harus sama tiap minggu, jangan pakai generator — pakai `pillow`.

Jangan pakai untuk: gambar yang memuat angka atau klaim (itu `tools/` yang menghitung), potret petani tanpa izin,
atau logo (itu `brand/`).

## 1 · Tiga jalur, dan kapan memilih yang mana

| Jalur | Cocok untuk | Risiko | Kendali |
| --- | --- | --- | --- |
| **Generator gambar** | fotografi produk, suasana, ilustrasi cat air | bentuk biji bisa salah, teks di gambar selalu rusak | sedang — perbaiki lewat prompt negatif |
| **Pillow deterministik** (`tools/gaya.py`) | arsir cetak, halftone, risograf, monokrom, tipografi | terbatas pada olahan dari render yang sudah ada | tinggi — hasil sama tiap dijalankan |
| **Vektor/CSS** | ikon, diagram, roda rasa, garis | butuh waktu menulis | tinggi |

Aturan yang dipakai proyek ini: **untuk apa pun yang muncul di halaman jual, pilih jalur yang bisa diperiksa** (Pillow atau vektor).
Generator hanya untuk gambar suasana dan fotografi, dan hasilnya harus lolos pemeriksaan di bagian 4.

## 2 · Anatomi prompt yang berhasil

Urutannya tetap, jangan diacak:

```
[objek tunggal + keadaannya] + [bahan/permukaan] + [sumber cahaya] + [latar]
+ [optik/rasio] + [palet] + [larangan]
```

Contoh nyata dari pustaka (gaya `produk-studio-gelap`):

> single roasted coffee bean standing upright on a matte black surface, dramatic low-key studio lighting
> from upper right, warm rim light on the crease, soft contact shadow, subtle film grain, dark brown and
> amber palette, centered composition, macro product photography, no text

Yang **tidak** boleh masuk prompt:

| Jangan | Kenapa |
| --- | --- |
| nama seniman hidup atau studio | hasil tidak bisa dipakai komersial dengan tenang |
| "8K, ultra HD, masterpiece" | tidak mengubah apa pun; yang mengubah adalah cahaya dan bahan |
| merek kamera | mengarahkan model ke tiruan yang salah, bukan ke hasil |
| lebih dari satu objek utama | perhatian pecah; pustaka ini menuntut satu protagonis |
| teks di dalam gambar | selalu rusak, dan teks harus jadi teks hidup di halaman |

## 3 · Enam kategori, satu kalimat pemakaian

| Kategori | Gaya | Dipakai untuk |
| --- | --- | --- |
| Fotografi | produk-studio-gelap, produk-kertas, makro-tekstur, seduh-aksi, ladang-dokumenter, potret-petani | hero, katalog, cerita asal-usul |
| Cetak | poster-arsir-2warna, halftone-koran, risograf-overprint, editorial-swiss, tipografi-ekspresif | poster, stiker, motto, pengumuman |
| Ilustrasi | garis-tinta, cat-air, potong-kertas, isometrik-teknis | diagram proses, konten lembut, rantai produksi |
| 3D | 3d-hiperrealis, 3d-tanah-liat | hero biji, stiker, fitur |
| Dokumen | identitas-brand-board, infografis-rasa | lembar brand, kartu rasa, materi B2B |

## 4 · Pemeriksaan sebelum gambar dipasang

Enam butir, semuanya bisa dijawab "ya/tidak" tanpa selera:

1. **Latar menyatu** — sudut gambar sama dengan kertas `#F5EFE4` (toleransi 3 per kanal) atau hitam `#16110D`.
2. **Satu protagonis** — tidak ada objek kedua yang menarik mata.
3. **Proporsi benar** — biji kopi sangrai: rasio panjang:lebar ≈ 1,35–1,5; alur tengah terlihat, tidak simetris sempurna.
4. **Tanpa teks di dalam gambar** — tidak ada huruf, angka, atau tanda air.
5. **Ukuran** — WebP q82, sisi terpanjang ≤ 1600 px, < 120 KB untuk gambar di atas lipatan.
6. **Berkas punya keterangan** — satu baris di `laporan/` menyebut prompt, alat, tanggal.

Butir 1, 3, dan 5 diukur mesin (`tools/biji_render.py`, `tools/verifikasi-biji.mjs`); butir 2 dan 4 oleh mata.

## 5 · Kalau hasilnya "jelek"

Urutan perbaikan — jangan langsung ganti prompt seluruhnya:

| Gejala | Perbaikan | Contoh |
| --- | --- | --- |
| terlihat seperti render plastik | ganti bahan jadi "matte", tambah "raking side light" | `3d-hiperrealis` → `3d-tanah-liat` |
| latar ramai | tambah "plain cream background", kurangi objek | semua gaya fotografi |
| gelap tapi mati | tambah satu sumber cahaya kedua: "warm rim light from behind" | `produk-studio-gelap` |
| ada kotak putih di atas kertas krem | jangan perbaiki prompt — olah di Pillow: ratakan latar ke `#F5EFE4` | `tools/biji_render.py` |

Catatan jujur: dua percobaan saya memakai generator untuk "gaya sinematik gelap" **ditolak pemilik** (dinilai jelek).
Sebabnya bukan prompt, tetapi bayangan asli ikut terekam sehingga muncul elips terang di bawah biji. Pelajaran:
**perbaiki latar dulu, baru gayanya.**

## 6 · Perintah

```bash
python3 tools/gaya.py                     # 4 gaya dari satu render → laporan/gaya-biji.png
python3 tools/gaya.py --pasang D          # pasang gaya pilihan
python3 tools/biji_render.py              # render ulang poster + cek 4 sudut
node tools/verifikasi-biji.mjs            # 12 butir (jalankan sebelum periksa.py)
```
