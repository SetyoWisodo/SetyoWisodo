# Brief 03 — Larangan yang bisa dibuktikan

> Dibuat 2026-10-29 oleh `tools/riset.py` dari `data/riset-referensi.csv` dan
> `data/riset-komentar.csv`. **Status data:** lihat kolom `status` di CSV. Selama barisnya
> masih `contoh`, angka di brief ini adalah contoh mekanisme — bukan bukti pasar.

**Dasar (bukti dari data):** 1 post pola “Larangan / peringatan” naik median 1,8× (ER median 6,9%) di reel — n=1, indikatif

## Acuan yang dianalisis (adaptasi, bukan salin)
  - "Aku salah simpan kopi 3 bulan, ini yang terjadi"

## Sudut untuk Nocturne
**Larangan yang bisa dibuktikan** — Larangan bekerja karena menantang kebiasaan, bukan karena menakut-nakuti. Setelah melarang, wajib langsung menjelaskan alasannya.

## Hook (3 detik pertama)
```
Jangan beli kopi yang cuma mencetak tanggal kedaluwarsa
```

## Format & durasi
reel · 7 detik untuk video, 3–4 slide untuk carousel · teks ≥ 80 px, aman dari UI bawah.

## Aset yang dipakai
`carousel-01a` — status: **siap**.
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
