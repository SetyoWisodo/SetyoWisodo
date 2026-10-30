# Skrip 01 — Diagnosis masalah · Edukasi

> Dibuat 2026-10-30 oleh `tools/studio.py` · status **siap rekam** ·
> skor suara 100/100 · struktur ini naik 2,3× di data referensi.

**Hook (0–3 detik):**
```
Kopi pahit padahal baru beli? Cek tiga hal ini.
```

| # | Durasi | Teks di layar | Sumber klaim |
| ---: | ---: | --- | --- |
| 1 | 3s | Kopi pahit padahal baru beli? Cek tiga hal ini. | catalog.json |
| 2 | 2s | Pertama: gilingan terlalu halus untuk alat Anda. Kedua: air di atas 94°C. | catalog.json |
| 3 | 2s | Ketiga: kopi sudah lewat 21 hari dari tanggal sangrai. | batch-qc.csv |
| 4 | 2s | Pesan lewat WhatsApp — sebutkan metode seduh & kota Anda. | — |

**Visual (shot list):** Tangan menimbang kopi → close-up gilingan → cangkir di meja

**Aset:** `reel-tanggal-sangrai` — ada di manifest.

**Sumber data:** `batch-qc.csv`, `catalog.json`

**Cek suara:** 100/100

- tidak ada

**Aturan:** adaptasi pola dari data referensi — jangan menyalin hook, footage, atau audio akun lain.
Jangan menyebut Nocturne sebagai roastery. Semua angka wajib bisa dilacak ke berkas di atas.
