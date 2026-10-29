# Brief 05 — Pengakuan biaya

> Dibuat 2026-10-30 oleh `tools/riset.py` dari `data/riset-referensi.csv` dan
> `data/riset-komentar.csv`. **Status data:** lihat kolom `status` di CSV. Selama barisnya
> masih `contoh`, angka di brief ini adalah contoh mekanisme — bukan bukti pasar.

**Dasar (bukti dari data):** 1 post pola “Pengakuan / biaya nyata” naik median 1,7× (ER median 9,6%) di carousel — n=1, indikatif

## Acuan yang dianalisis (adaptasi, bukan salin)
  - "Kami buang 4 kg blend bulan ini"

## Sudut untuk Nocturne
**Pengakuan biaya** — Mengakui kerugian nyata membangun kepercayaan lebih kuat daripada klaim kualitas. Sebut angkanya, sebut keputusannya.

## Hook (3 detik pertama)
```
Minggu ini satu batch tidak lolos — skornya 81,5, ambang kami 83
```

## Format & durasi
carousel · 7 detik untuk video, 3–4 slide untuk carousel · teks ≥ 80 px, aman dari UI bawah.

## Aset yang dipakai
`reel-batch-ditolak` — status: **siap**.
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
