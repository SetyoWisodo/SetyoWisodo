# Cara tempel (tanpa sunting)

Berkas di folder `isi/` sudah bersih: tanpa markdown, tanpa tanda bintang penekanan,
kutipan lengkung, satu baris kosong antarparagraf, pemisah scene `***`.

## Wattpad
1. Cerita → **Add new part**.
2. Kolom **Part title**: salin satu baris judul dari `00_daftar_judul.txt`
   (contoh: `Buoy in Winter` — tanpa nomor `01.`).
3. Kolom **Story text**: buka `isi/ch_01.txt`, pilih semua (Ctrl+A), tempel (Ctrl+V).
4. **Publish** → ulangi untuk bab berikutnya dengan berkas `ch_02.txt` dst.
5. Jangan menekan Enter di akhir tempelan; berkas sudah diakhiri satu baris kosong.

## Fizzo Novel
1. Write → **New chapter**.
2. Judul dari `00_daftar_judul.txt`, isi dari `isi/ch_XX.txt`.
3. Fizzo menuntut minimal 1.000 kata per hari unggah; setiap bab sudah 1.500+ kata,
   jadi satu bab per hari aman.

## Kalau perlu arsip atau cetak
`99_gabung_vol1.txt` memuat seluruh bab berurutan dengan pembatas `====`.

## Catatan
- Penekanan huruf miring hilang saat ditempel (Wattpad/Fizzo tidak menerima format dari
  tempelan teks). Kalimatnya tetap utuh; yang hilang hanya kemiringan huruf.
- Semua bab 1.500–2.500 kata dan di bawah 50.000 karakter (batas satu part Wattpad).
- Setelah bab baru ditulis, jalankan ulang `python3 novel_en/tools/build_tempel.py`.
