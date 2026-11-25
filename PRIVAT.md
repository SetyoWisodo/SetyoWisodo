# Repo ini publik — jangan simpan aset komersial di sini

`SetyoWisodo/SetyoWisodo` adalah repo **publik**. Apa pun yang di-commit ke
sini bisa diunduh siapa pun, tanpa akun, tanpa membayar, dan tetap bisa dibaca
dari riwayat Git walaupun berkasnya nanti dihapus.

## Yang sudah dikeluarkan

| Isi | Ukuran | Commit |
|---|---|---|
| `book/publish/` — PDF, EPUB, DOCX, ZIP gambar, gambar 3D, foto marketplace | 92,3 MB, 69 berkas | `c7ad085` |
| `book.md` — naskah EN lengkap | 216.031 kata | `38cf8b8` |
| `book_id.md` — naskah ID lengkap | 213.000 kata | `38cf8b8` |

Keduanya sekarang ada di `.gitignore`, jadi tidak akan masuk lagi tanpa sengaja.

## Yang tetap ada di repo (dan boleh)

- `book/src/en/`, `book/src/id/` — naskah sumber yang dipakai `book/build.py`.
  Ini versi 149 halaman per edisi, bukan edisi 457 halaman yang dijual.
- `book/build.py`, `book/template/`, `book/fonts/` — mesin produksi.
- Dokumen panduan, angka, dan laporan (`.md`, `.json`).
- `novel_en/` — naskah serial; memang untuk diterbitkan, bukan produk berbayar.

## Kalau mau benar-benar privat

Menjadikan repo ini **private** adalah satu tombol di GitHub, tetapi tombolnya
tidak bisa ditekan dari sini: token yang dipakai sesi ini tidak punya izin
`Administration` (GitHub menolak dengan `403 Resource not accessible by
integration`). Caranya:

1. Buka `https://github.com/SetyoWisodo/SetyoWisodo/settings`.
2. Gulir ke paling bawah, **Danger Zone** → **Change repository visibility**.
3. Pilih **Make private**, ikuti konfirmasi.

Dua akibat yang perlu diketahui sebelum menekan tombol itu:

- **GitHub Pages** ikut mati kalau nanti diaktifkan — tidak ada halaman publik.
- **Repo profil** (README yang tampil di halaman profil) akan hilang dari
  tampilan publik. README di `main` adalah halaman profil Anda.
- Tautan `github.com/.../raw/...` yang pernah disebar akan berhenti bekerja.

Karena itu langkah yang lebih aman: biarkan repo publik untuk profil, dan
simpan aset komersial di Drive (atau repo privat terpisah). Itulah yang
sekarang berlaku.
