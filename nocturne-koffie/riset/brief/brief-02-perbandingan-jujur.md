# Brief 02 — Perbandingan jujur

> Dibuat 2026-10-29 oleh `tools/riset.py` dari `data/riset-referensi.csv` dan
> `data/riset-komentar.csv`. **Status data:** lihat kolom `status` di CSV. Selama barisnya
> masih `contoh`, angka di brief ini adalah contoh mekanisme — bukan bukti pasar.

**Dasar (bukti dari data):** 2 post pola “Perbandingan A vs B” naik median 2,2× (ER median 7,5%) di carousel, reel

## Acuan yang dianalisis (adaptasi, bukan salin)
  - "Kopi Rp50 ribu vs Rp150 ribu — bedanya di mana?"
  - "Kopi 250 g vs 1 kg — mana yang lebih hemat?"

## Sudut untuk Nocturne
**Perbandingan jujur** — Perbandingan menaikkan simpan karena orang memakainya untuk memutuskan. Bandingkan hal yang bisa kita buktikan: ketinggian, proses, cara seduh — bukan 'enak vs tidak'.

## Hook (3 detik pertama)
```
Arabika Ijen vs robusta Raung: ketinggian, rasa, dan cara seduhnya
```

## Format & durasi
carousel, reel · 7 detik untuk video, 3–4 slide untuk carousel · teks ≥ 80 px, aman dari UI bawah.

## Aset yang dipakai
`carousel-02a` — status: **siap**.
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
