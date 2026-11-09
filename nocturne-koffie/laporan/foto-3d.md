# Foto 3D e-commerce — kemasan 500 g

Diperbarui 9 November 2026. Semua foto katalog dan marketplace sekarang keluar dari
`tools/foto.py`; `tools/pouch.py` hanya menyisakan lembar spesimen untuk dicocokkan ke
kemasan fisik.

## Apa yang berubah (dan kenapa)

Keluhan "semakin ngawur" datang dari rig lama yang mengisi tiap muka dengan **satu gradien
lurus**. Hasilnya kotak hitam berlabel, bukan foto studio. Rig baru memakai **permukaan 3D
sungguhan**: tiap muka punya fungsi (u, v) → titik ruang, normalnya dihitung dari turunan
fungsi itu, lalu dicahayai per piksel. Lengkung panel, lekuk gusset, dan flens segel ikut
memantulkan cahaya — itu yang membuat benda terbaca punya isi, bukan papan.

| Bagian | Cara kerja |
| --- | --- |
| Permukaan | panel menggembung 10,5% lebar; dinding gusset 90 mm berlekuk di lipatan; flens segel 15 mm melengkung 1,2 mm |
| Cahaya | ambient berarah (atas lebih terang) + softbox key di kiri-atas `(-0,40, −0,62, 0,67)` + pemantul kanan + lampu samping kiri + rim belakang |
| Kilau | pita softbox lebar `d⁵ × 0,10` + titik sempit `d⁴⁸ × 0,10` — sengaja lemah karena bahan doff |
| Bahan | `#1B1A18` + derau kain halus (grain, bukan garis) + sheen tepi |
| Label | stiker 120 × 170 mm ditempel dengan tepi kertas (atas terang, bawah gelap) + bayangan tempelan 0,4 |
| Valve | lubang gelap, dudukan, kubah silikon radial, cincin bayangan kontak |
| Crimp | gerigi 7 mm sepanjang kedalaman pada flens atas; garis jahit di bawah zipper; lipatan dasar |
| Latar | **putih murni** (marketplace, tanpa bayangan) atau **kertas studio** (turun ke lantai) dengan bayangan kontak + pantulan ber-fade |
| Anti-pecah | bahu lembut di atas 0,84 supaya label putih tidak jadi bidang rata |

## Keluaran per SKU

| Berkas | Ukuran | Latar | Untuk |
| --- | --- | --- | --- |
| `studio/<id>-depan.jpg` | 2000² | putih murni | foto utama |
| `studio/<id>-tiga-perempat.jpg` | 2000² | kertas studio | pandangan utama halaman brand |
| `studio/<id>-valve.jpg` | 2000² | putih murni | bukti valve |
| `studio/<id>-sisi.jpg` | 2000² | putih murni | dinding gusset 45° |
| `katalog/<id>-{0,18,40}.jpg` | 2000² | kertas studio | halaman katalog |
| `katalog/<id>-hero.jpg` | 2400 × 1350 | kertas studio | hero landing |
| `pasar/<id>-1x1.jpg` | 1000² | putih murni | Tokopedia / Shopee |
| `pasar/<id>-4x5.jpg` | 1080 × 1350 | putih murni | feed & katalog sosial |

`python3 tools/foto.py` menulis 9 SKU sekaligus: **8,2 MB**, ≈ 27 menit di sandbox
(≈ 20 detik per foto 2000 px). Lembar kontak 9 × 4 ada di `laporan/katalog-render.png`.

## Batas yang harus diucapkan

· Ini **render**, bukan pemotretan. Kejujuran ini penting sebelum dipakai sebagai "foto produk".
· Ukuran 135 × 260 mm dan stiker 120 × 170 mm dari pemilik. Ketebalan sisi 45 mm, chamfer 10 mm,
  warna dan kilap bahan masih **asumsi** (`data/kemasan-katalog.json`).
· Belum dimodelkan: foil/spot-UV, emboss, jendela transparan, lipatan kertas tajam, jahitan
  tepi, dan ketebalan nyata flens segel.
· Foto muka valve sengaja polos — desain Nocturne ada di stiker muka belakang.

## Tiga hal yang paling menahan hasil ini dari "foto studio brand besar"

1. **Serat kain**: derau sekarang masih terlalu halus; pada 2000 px badan terbaca rata.
   Perlu tekstur tenun terarah (dua arah silang) dengan variasi jarak.
2. **Kertas label**: stiker masih kaku sempurna. Foto asli memperlihatkan gelombang halus di
   tepi tempelan dan sedikit kilau kertas.
3. **Tepi siluet**: masih potongan tajam. Foto asli punya tepi 1–2 px yang lebih terang
   karena difraksi lensa.

Ketiganya bisa dikerjakan tanpa aset luar, tapi mengubah tampilan seluruh seri — jadi
menunggu keputusan sebelum dijalankan.
