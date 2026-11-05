---
name: pasangan-font
description: Memilih pasangan huruf, menerapkannya tanpa CDN, dan membuktikan bobotnya benar-benar ada. Dipakai saat memilih huruf untuk halaman/lembar baru, saat huruf terasa tidak pas, atau saat menambah satu bobot yang belum tersedia.
---

# Pasangan huruf — memilih, menerapkan, membuktikan

Sumber, semuanya ≥ 3.000 bintang, diperiksa 5 Nov 2026:

| Repo | Bintang | Isi nyata | Yang diambil | Yang ditolak |
| --- | --- | --- | --- | --- |
| [`nextlevelbuilder/ui-ux-pro-max-skill`](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) (MIT) | 145.433 | `typography.csv` **74 pasangan siap pakai** (judul + badan + suasana + CSS + Tailwind), `google-fonts.csv` **1.935 keluarga** dengan kategori, sumbu variabel, popularitas, `google-font-licenses.json` | cara membaca pasangan: kolom *Mood/Style Keywords* jadi penentu, bukan selera; daftar 1.935 keluarga untuk memastikan huruf yang dipilih memang ada varian variabelnya | pemasangan plugin npm & skrip pencariannya |
| [`google/fonts`](https://github.com/google/fonts) (tiap berkas OFL 1.1; repo sendiri tanpa berkas lisensi di akar) | 20.724 | keluarga variabel asli `.ttf` — sumber berkas yang dipakai situs ini | **berkas hurufnya**, lewat `tools/font.py` | mengunduh seluruh repo (3,3 GB) |
| [`rsms/inter`](https://github.com/rsms/inter) (OFL-1.1) | 20.042 | Inter, huruf antarmuka dengan angka tabular & fitur `ss01` | pilihan badan teks | — |
| [`fontsource/fontsource`](https://github.com/fontsource/fontsource) (MIT) | 6.263 | pemaketan huruf untuk **dilayani sendiri** (npm, subset per bahasa) | gagasan: subset latin + satu berkas per keluarga, bukan CDN | paket npm-nya (proyek ini tidak memakai npm di halaman) |
| [`ubuwaits/beautiful-web-type`](https://github.com/ubuwaits/beautiful-web-type) (MIT) | 7.345 | panduan huruf sumber terbuka + contoh pasangan di web sungguhan | kriteria: pasangan dinilai dari **kontras sumbu**, bukan dari nama | — |

## Kapan dipakai

- Memilih huruf untuk halaman, lembar brand, atau materi cetak baru.
- Halaman memakai bobot yang berkasnya tidak ada (peramban menyintesis tebal → huruf terlihat "kempes").
- Huruf dimuat dari CDN dan harus dipindahkan ke lokal.

## 1 · Aturan pemilihan: tiga peran, bukan tiga huruf

| Peran | Tugas | Boleh berapa | Contoh di proyek ini |
| --- | --- | --- | --- |
| **Display** | judul, angka besar, label kecil | satu keluarga | Bricolage Grotesque (600–800) |
| **Badan** | paragraf, tombol, tabel | satu keluarga sans | Inter (400–700) |
| **Aksen** | motto, kutipan, satu kata di judul | satu keluarga serif, **miring asli** | Fraunces (300–700, italic 300–400) |

Tiga peran itu sudah batas. Menambah peran keempat adalah tanda halaman akan terasa campur.

Kontras harus terjadi pada **sumbu**, bukan pada warna:

| Kontras yang bekerja | Kontras yang gagal |
| --- | --- |
| grotesque tebal rapat × serif tipis lebar | dua sans yang mirip (Inter × Roboto) |
| huruf besar dengan tracking negatif × teks 16 px renggang | dua huruf yang sama-sama ramai detail |
| serif miring × sans tegak di baris yang sama | script × script |

## 2 · Empat gerbang sebelum satu huruf dipakai

| Gerbang | Pertanyaan | Cara memeriksa |
| --- | --- | --- |
| **Lisensi** | OFL/Apache/MIT? boleh komersial & disematkan? | `assets/fonts/LISENSI.md`; OFL wajib menyertakan teks lisensi |
| **Rentang bobot** | semua bobot yang dipakai CSS ada di berkas? | `python3 tools/font.py --cek` + butir **Huruf lokal** di `tools/periksa.py` |
| **Cakupan glif** | huruf yang dipakai naskah ada? (é, —, →, ·, °) | uji cmap seperti di bagian 5 |
| **Berat** | < 120 KB per keluarga setelah subset latin? | `ls -la assets/fonts/*.woff2` |

Kalau bobot tidak ada, peramban **menyintesis** tebal dengan menggemukkan garis — hasilnya terlihat murah dan
lebar teks berubah. Ini kesalahan yang paling sering lolos: halaman meminta 700, berkas hanya punya 400 dan 600.

## 3 · Tangga ukuran (dipakai seluruh situs)

| Token | Ukuran | Tinggi baris | Huruf |
| --- | --- | --- | --- |
| `h1` | `clamp(2.2rem, 7.6vw, 4.6rem)` | 0,95–1 | display 800, tracking −0,03em |
| `h2` | `clamp(1.1rem, 2.6vw, 1.5rem)` | 1,1 | display 800 |
| lead | `clamp(14.5px, 1.5vw, 16.5px)` | 1,6 | badan 400 |
| badan | 16 px | 1,6–1,8 | badan 400 |
| label | 13 px | 1,3 | display 600, tracking +0,2em, kapital |
| catatan | 13 px **minimum** | 1,5 | badan 400 |

Aturan yang mengikat: tidak ada paragraf 14 px, tidak ada huruf di bawah 13 px, satu ukuran per jenis elemen,
angka pakai `font-variant-numeric: tabular-nums` di tabel harga.

## 4 · Menerapkan tanpa CDN

```bash
python3 tools/font.py          # unduh → kunci sumbu → iris → woff2 → fonts.css → pasang tautan
python3 tools/font.py --cek    # tak ada CDN · berkas ada · tiap halaman memuat fonts.css
```

Yang dilakukan skrip itu, berurutan:

1. Ambil keluarga **variabel** dari `google/fonts` lewat `gh api` (disimpan di `/tmp`, tidak masuk repo).
2. **Kunci sumbu yang tidak dipakai** — `wdth=100`, `SOFT=0`, `WONK=0` — supaya berkas tidak membawa variasi mati.
3. **Batasi rentang bobot** ke yang benar-benar dipakai: 600–800 / 300–700 / 300–400 / 400–700.
4. **Iris glif** ke Latin + Latin-1 + tanda baca tipografis + panah; simpan `woff2`.
5. Tulis `assets/css/fonts.css`: satu `@font-face` per keluarga dengan `font-weight: <a> <b>`.
6. Ganti tautan Google Fonts di setiap halaman dengan `<link rel="preload">` + `fonts.css`.

Hasil pada proyek ini (5 Nov 2026):

| Berkas | Bobot | Gaya | Berat |
| --- | --- | --- | --- |
| `bricolage.woff2` | 600–800 | normal | 60,3 KB |
| `fraunces.woff2` | 300–700 | normal | 62,6 KB |
| `fraunces-italic.woff2` | 300–400 | italic | 66,0 KB |
| `inter.woff2` | 400–700 | normal | 42,5 KB |
| **total** | | | **231 KB** |

Sebelumnya: 3 permintaan jaringan ke `fonts.googleapis.com`/`gstatic.com` per halaman (14 halaman), dan bobot
700 untuk Inter serta 600 untuk Bricolage **tidak pernah tersedia** di beberapa halaman → huruf sintetis.

## 5 · Memeriksa cakupan glif

```python
from fontTools.ttLib import TTFont
t = TTFont("assets/fonts/inter.woff2")
cmap = set().union(*(set(x.cmap) for x in t["cmap"].tables))
print("✕" in "".join(map(chr, cmap)))   # False → peramban pakai huruf sistem untuk glif itu
```

Hasil nyata: `→` ada di Inter, tidak di Fraunces; `✕` (U+2715) tidak ada di ketiganya — glif itu sudah jatuh ke
huruf sistem sejak sebelum pemindahan, jadi bukan kemunduran. Kalau suatu saat sebuah glif penting hilang,
tambahkan ke rentang `UNICODE` di `tools/font.py` lalu bangun ulang.

## 6 · Larangan

- Huruf dari CDN di halaman publik (melanggar batas "tanpa CDN").
- Bobot sintetis: memakai 700 saat berkas hanya 400–600.
- Huruf dekoratif untuk badan teks.
- Lebih dari satu keluarga display.
- Nama seniman/huruf berbayar yang lisensinya tidak jelas.
- Menyebut huruf "gratis" padahal ia hanya gratis untuk pemakaian pribadi.
