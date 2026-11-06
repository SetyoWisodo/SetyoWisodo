# Taruh foto kemasan di folder ini

Nama berkas = `id` katalog, huruf kecil, spasi jadi tanda hubung. Contoh:

```
gayo.jpg            kintamani.jpg      blue-mount-ijen.jpg
semeru.png          arjuno.jpg         raung.jpg
ijen-excelsa.jpg    blend-7030.jpg     blend-6040.jpg
peta-rasa.jpg       jelajah-arabika.jpg
```

Jenis berkas: `.jpg`, `.jpeg`, `.png`, `.webp`. Foto boleh besar (2000 px ke atas), boleh
masih ada latar — pipa `tools/kemasan.py` yang membuang latarnya.

Sesudah menaruh berkas:

```bash
python3 tools/kemasan.py       # buang latar → bangun 3D → serong 10° ke kiri
python3 tools/kemasan.py --cek # periksa: alfa di 4 sudut, arah serong, ukuran
python3 tools/rak.py           # pakai otomatis di rak (sampul + punggung)
```

Keluaran: `assets/img/kemasan/<id>-depan.webp` (bidang depan bersih) dan
`<id>-3d.webp` (kotak bervolume, serong 10° ke kiri, latar transparan).

Foto mentah **tidak pernah** dipakai di halaman — selalu lewat pipa ini dulu.
Untuk hasil terbaik saat memotret: latar polos satu warna (karton/meja), cahaya dari satu
arah, kemasan tegak lurus kamera, tanpa bayangan benda lain.
