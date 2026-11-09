# Kemasan 500 g flat-bottom — foto studio & rak

Dibuat 9 November 2026. Permintaan pemilik: *"aku kirimkan beserta dengan ukurannya.
kemasan yang aku kirimkan merupakan kemasan ukuran 500 gram. terdapat valve pada sisi depan
maka penempelan sticker aku letakkan pada sisi belakang … apakah kamu bisa menempelkan sticker
pada sisi tengah bagian belakang kemasan dan membuatnya menjadi sebuah foto produk commersil
eccomers khas foto studio pada brand brand besar"* — dan rak landing page (mengikuti referensi
VHS Archive / Leon Vasari) diganti dari kaset menjadi kemasan kopi.

| Hal | Isi |
| --- | --- |
| Berkas | `tools/pouch.py` (baru), `rak/rak.js`, `tools/rak.py`, `data/kemasan-katalog.json` |
| Aset | `assets/img/katalog/<id>-{0,18,40,hero}.jpg`, `assets/img/katalog/pasar/<id>-{1x1,4x5}.jpg`, `assets/img/pouch/<id>-{muka,sisi}.png`, `<id>-valve.jpg` |
| Laporan gambar | `laporan/katalog-render.png` (9 × 3 sudut), `laporan/pouch-spesimen.png` (stiker · valve · 3/4) |
| Pemeriksa | `python3 tools/pouch.py --cek`, `node tools/rak-uji.mjs`, `node tools/rak-spek.mjs`, `python3 tools/periksa.py` |

## 1 · Yang dikirim pemilik, dan yang saya asumsikan

| Hal | Angka | Sumber |
| --- | --- | --- |
| Ukuran kemasan | **135 × 260 mm** (13,5 × 26 cm) | **pemilik** — foto listing & pesan |
| Berat | 500 g | **pemilik** |
| Bentuk | flat-bottom (dasar persegi, panel depan-belakang + dua sisi + chamfer) | **pemilik** (foto) |
| Valve | ada, di **muka depan** | **pemilik** |
| Stiker | **120 × 170 mm**, di **tengah muka belakang** | **pemilik** |
| Ketebalan sisi | **45 mm** | asumsi bentuk flat-bottom 500 g |
| Gusset dasar | **90 mm** | asumsi (2 × sisi) |
| Chamfer sudut | **10 mm** | asumsi |
| Pita segel / zipper | 15 mm / 32 mm | asumsi dari bentuk sejenis |
| Warna & kilap bahan | `#1B1A18`, kilap 0,16 (doff) | asumsi dari foto produk yang dikirim |

Semua angka ada di satu tempat: `data/kemasan-katalog.json`. Mengganti angka di sana lalu
menjalankan `python3 tools/pouch.py` akan mengubah sembilan SKU sekaligus — tidak ada angka
kemasan yang ditanam di kode.

## 2 · Yang dibuat

1. **Geometri pouch** (`tools/pouch.py`): delapan titik penampang melintang (panel, chamfer,
   sisi gusset), menyempit ke atas karena zipper menarik kedua panel (72%), normal muka
   dihitung lalu muka yang membelakangi kamera dibuang. Tidak ada lagi kotak label lama.
2. **Stiker**: label merek yang sudah ada ditempel **di tengah muka belakang** seukuran
   12 × 17 cm, dengan bayangan tipis di bawah-tepi dan garis tepi — terbaca sebagai kertas
   yang menempel, bukan cetakan langsung di kain.
3. **Valve** di muka depan: dasar gelap, cincin logam, kubah, satu busur pantulan di sisi
   lampu, dan bayangan lembut. Ini muka yang dipakai untuk foto "valve".
4. **Foto komersial**: 3 sudut (0°, −18°, 40°) + hero 16:9 + dua rasio marketplace
   (1:1 1000 px dan 4:5 1080 × 1350) **latar putih murni tanpa bayangan** — syarat foto
   utama Tokopedia/Shopee. Kontrak nama berkas sama dengan `katalog.py`, jadi halaman
   `katalog/` dan versi luringnya ikut memakai foto baru tanpa diubah.
5. **Rak** (`rak/`): objek kaset diganti kemasan kopi. Dua muka datar per SKU
   (`<id>-muka.png` muka stiker, `<id>-sisi.png` sisi gusset) dipasang di mesin rak yang sama;
   rasio muka dibaca dari data (`FACE`), jadi animasi, pegas, tirai detail, kursor, dan
   spesifikasi template tidak disunting. Rak kini memuat **9 lot berlabel** — paket dan kartu
   member tidak berdiri di rak karena tidak punya kemasan.

## 3 · Hasil pemeriksaan

| Perintah | Keluaran |
| --- | --- |
| `python3 tools/pouch.py` | 9 SKU · 3 sudut + hero + valve + 2 muka rak · **6,0 MB** · lembar 594 KB |
| `python3 tools/pouch.py --cek` | **OK · 9 SKU kemasan 500 g flat-bottom, stiker belakang** |
| `node tools/rak-uji.mjs` | semua butir lolos · **27 kotak** (9 × 3 salinan) |
| `node tools/rak-spek.mjs` | **108 butir sesuai** · 0 penyimpangan |
| `node tools/katalog-uji.mjs` | semua butir lolos (halaman ikut memakai foto baru) |
| `python3 tools/katalog-luring.py` | 1.138 KB satu berkas · tanpa tautan luar |
| `python3 tools/periksa.py --ringkas` | **32 lolos · 0 gagal** |

## 4 · Batas yang tidak diklaim

| Hal | Status |
| --- | --- |
| Foto sebagai "foto produk asli" | **bukan** — ini render dari label + geometri sendiri, bukan pemotretan |
| Ketebalan, chamfer, warna bahan | **asumsi** (ukuran & stiker dari pemilik) |
| Lipatan kertas di sudut, jahitan, foil/spot-UV | tidak dimodelkan |
| Panel depan (muka valve) | bahan polos + valve; belum ada cetakan di muka depan |
| Tampilan rak & halaman katalog | **belum pernah dilihat** — tidak ada peramban; uji hanya memeriksa data, geometri, dan sambungan |
| Bentuk tutup atas | disederhanakan: pita segel + zipper, tanpa lipatan samping |

Kalau salah satu dari ini penting untuk produksi (mis. warna bahan sebenarnya silver, atau
ketebalan 60 mm), cukup kirim angkanya — satu berkas, satu render ulang.
