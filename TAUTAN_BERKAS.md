# Berkas final — di mana sekarang

**Repo ini publik. Berkas buku tidak lagi disimpan di sini.**

Semua PDF, EPUB, DOCX, paket gambar, gambar 3D, dan foto marketplace sudah
dikeluarkan dari repository (commit `c7ad085`) dan `book/publish/` sekarang ada
di dalam `.gitignore`. Alasannya sederhana: apa pun yang ada di repo publik
bisa diunduh siapa pun tanpa membayar.

## Di mana salinan hidupnya

| Berkas | Di mana | Catatan |
|---|---|---|
| PDF lengkap 458 hlm, EPUB, DOCX, zip empat berkas | **Google Drive** — folder `Surviving the Future — final files (2026)` | tautan tidak ditulis di berkas ini; ambil dari riwayat percakapan |
| Sampel gratis 36 hlm | Google Drive, berkas terpisah | tautannya dipakai di deskripsi produk |
| Sampul, gambar 3D, foto marketplace | Google Drive, folder yang sama | untuk halaman jualan |

## Kalau berkasnya hilang

Semua bisa dibuat ulang dari isi repo:

```bash
python book/build.py          # naskah book/src/ -> PDF, EPUB, DOCX di book/publish/
python make_listing_html.py   # teks listing -> HTML siap tempel
```

Naskah sumbernya (`book/src/en/`, `book/src/id/`) tetap ada di repo. Yang
dikeluarkan hanya hasil render-nya.

## Aturan untuk ke depan

- **Jangan commit** apa pun dari `book/publish/`. Sudah di-.gitignore, tetapi
  jangan dipaksa dengan `git add -f`.
- Berkas yang boleh ada di repo: naskah sumber, skrip build, dokumen panduan,
  dan angka-angka (`.md`, `.py`, `.json`).
- Berkas yang tidak boleh: PDF, EPUB, DOCX, ZIP, JPG/PNG hasil render, dan
  apa pun yang dijual atau menjadi bagian dari produk berbayar.
- Repo novel (`novel_en/`) tidak menyimpan berkas jualan; naskahnya berupa
  teks dan memang untuk diterbitkan di platform serial.
