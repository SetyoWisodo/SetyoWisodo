# Brief 04 — Angka + daftar

> Dibuat 2026-10-30 oleh `tools/riset.py` dari `data/riset-referensi.csv` dan
> `data/riset-komentar.csv`. **Status data:** lihat kolom `status` di CSV. Selama barisnya
> masih `contoh`, angka di brief ini adalah contoh mekanisme — bukan bukti pasar.

**Dasar (bukti dari data):** 1 post pola “Angka / daftar” naik median 1,8× (ER median 9,6%) di carousel — n=1, indikatif

## Acuan yang dianalisis (adaptasi, bukan salin)
  - "Tiga tanda kopi sudah tidak layak diseduh"

## Sudut untuk Nocturne
**Angka + daftar** — Angka menghentikan gulir lebih cepat daripada kata sifat. Pakai angka yang benar-benar kita catat, bukan angka bulat karangan.

## Hook (3 detik pertama)
```
Tiga hal yang tercetak di tiap kantong: tanggal sangrai, kode batch, level roast
```

## Format & durasi
carousel · 7 detik untuk video, 3–4 slide untuk carousel · teks ≥ 80 px, aman dari UI bawah.

## Aset yang dipakai
`carousel-01c` — status: **siap**.
Kalau belum ada: jalankan `python3 tools/kreatif.py` atau tambahkan item di `data/kreatif.json`.

## Bukti yang wajib tampil
batch-qc.csv (skor & status batch) · catalog.json (harga) · label bertanggal sangrai

## Keberatan pembeli yang harus dijawab
  - "saya simpan di kulkas malah berbau kulkas"
  - "baru beli 2 minggu tapi rasanya hambar"

## CTA
Pesan via WhatsApp — sebutkan metode seduh & kotanya

## Larangan
jangan pakai kata promo/diskon/buruan; jangan klaim 'terbaik'; jangan sebut Nocturne sebagai roastery

## Selesai bila
Aset jadi (status `siap` di manifest), caption tertulis, jadwal tercatat di
`data/konten-14hari.csv`, dan brief ini dihapus dari folder `riset/brief/` **setelah** ditandai
`dipakai` di `riset/data.json`.
