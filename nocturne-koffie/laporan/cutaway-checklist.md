# Ceklis Cutaway — kemasan Blue Mount Ijen

Acuan: `brand/label-blue-mount-ijen.png` (827×1181 px). Metode: skill **Cutaway** (Nyxera0x, MIT).

Angka ditulis sebelum satu baris kode halaman, lalu diukur ulang oleh `tools/cutaway.py --cek` dan `tools/cutaway-uji.mjs`.

1. Siluet & sudut: kemasan tegak, bidang depan 100 × 142.8 satuan (rasio acuan 0.7003 dari brand/label-blue-mount-ijen.png), sampul 3/4 dari kiri.
2. Ciri utama: stiker lot 34 × 13 satuan di kiri-bawah, 4 satuan di depan permukaan — bukan melayang, bukan rata.
3. Tinta: 14.3% piksel acuan di bawah luma 80. Pita atas 4.7%, tengah 0.5%, bawah 37.7% — massa gelap tetap di pita bawah.
4. Katup aroma: satu cakram 17 satuan di kanan-atas, NEVER dua atau lebih.
5. Segel atas: pita 7 satuan selebar badan, NEVER lebih tipis dari 5 satuan.
6. Lipatan samping: 2 bidang 18 satuan di ±48, keduanya terbuka bersamaan.
7. Isi: 7 biji 7 × 10 satuan, muncul setelah panel depan bergeser 38 satuan.
8. Warna: satu aksen (kobalt) menandai bagian yang sedang bergerak; sisanya kertas + tinta.
9. Tidak ada bidang yang menembus bidang lain; setiap bagian kembali ke tempatnya dengan selisih 0 satuan.
10. Kamera: 9 ketukan, 9 sudut berbeda (zoom 1,00–1,40; ry −44°…150°) — NEVER dua ketukan memakai kamera yang sama.
11. Waktu: bagian terbuka 1,0 s, tahan, menutup 0,55 s; ketukan baru tiap 2–3 s; film 25 s.
12. Kepadatan: luas tinta model ≥ 0,8 × acuan (14.3% × 0,8 = 11.4%).

## Ukur ulang
```bash
python3 tools/cutaway.py --cek
node tools/cutaway-uji.mjs
```
