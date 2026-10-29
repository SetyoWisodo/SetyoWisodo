# Swipe file — referensi konten & kata kunci

> Dibuat 2026-10-29 oleh `tools/riset.py`. 0 baris asli, 27 baris contoh.
> Confidence: **belum ada data asli** (27 post). Sampel kecil = arah, bukan kepastian.

## Post outlier

| # | Hook | Platform/format | Lift | ER | Label |
|---:|---|---|---:|---:|---|
| 1 | Kopi Rp50 ribu vs Rp150 ribu — bedanya di mana? | tiktok/reel | 2,9× | 6,0% | outlier kuat |
| 2 | Barista jelasin kenapa kopi kafe terasa lebih kuat | tiktok/reel | 2,3× | 6,3% | outlier kuat |
| 3 | Aku salah simpan kopi 3 bulan, ini yang terjadi | tiktok/reel | 1,8× | 6,9% | outlier ringan |
| 4 | Tiga tanda kopi sudah tidak layak diseduh | instagram/carousel | 1,8× | 9,6% | outlier ringan |
| 5 | Kami buang 4 kg blend bulan ini | instagram/carousel | 1,7× | 9,6% | outlier ringan |
| 6 | Kopi 250 g vs 1 kg — mana yang lebih hemat? | instagram/carousel | 1,6× | 9% | outlier ringan |
| 7 | Kenapa kopimu pahit padahal baru beli | tiktok/reel | 1,5× | 6,8% | normal |
| 8 | Kami tolak 2 batch bulan ini — ini alasannya | instagram/carousel | 1,4× | 9,7% | normal |
| 9 | Kami buang 3 kg kopi minggu ini | tiktok/reel | 1,3× | 9,0% | normal |
| 10 | Jangan beli kopi yang cuma ada tanggal kedaluwarsanya | instagram/carousel | 1,0× | 10,1% | normal |
| 11 | Barista jelasin kenapa kopi kafe terasa beda | instagram/reel | 1,0× | 8,2% | normal |
| 12 | Proses: 12 menit terakhir sebelum dikemas | instagram/reel | 1,0× | 7,4% | normal |

## Pola & sudut kita

### Diagnosis masalah — 1 post, lift median 2,3×

- Acuan: “Barista jelasin kenapa kopi kafe terasa lebih kuat”
- Sudut Nocturne: **Diagnosis masalah**
- Hook kita: `Kopi pahit padahal baru beli: cek tanggal sangrai, gilingan, lalu suhu air`
- Aset: `reel-tanggal-sangrai`

### Perbandingan A vs B — 2 post, lift median 2,2×

- Acuan: “Kopi Rp50 ribu vs Rp150 ribu — bedanya di mana?”; “Kopi 250 g vs 1 kg — mana yang lebih hemat?”
- Sudut Nocturne: **Perbandingan jujur**
- Hook kita: `Arabika Ijen vs robusta Raung: ketinggian, rasa, dan cara seduhnya`
- Aset: `carousel-02a`

### Larangan / peringatan — 1 post, lift median 1,8×

- Acuan: “Aku salah simpan kopi 3 bulan, ini yang terjadi”
- Sudut Nocturne: **Larangan yang bisa dibuktikan**
- Hook kita: `Jangan beli kopi yang cuma mencetak tanggal kedaluwarsa`
- Aset: `carousel-01a`

### Angka / daftar — 1 post, lift median 1,8×

- Acuan: “Tiga tanda kopi sudah tidak layak diseduh”
- Sudut Nocturne: **Angka + daftar**
- Hook kita: `Tiga hal yang tercetak di tiap kantong: tanggal sangrai, kode batch, level roast`
- Aset: `carousel-01c`

### Pengakuan / biaya nyata — 1 post, lift median 1,7×

- Acuan: “Kami buang 4 kg blend bulan ini”
- Sudut Nocturne: **Pengakuan biaya**
- Hook kita: `Minggu ini satu batch tidak lolos — skornya 81,5, ambang kami 83`
- Aset: `reel-batch-ditolak`

## Kalimat pembeli (dari komentar)

- *keberatan* — “saya simpan di kulkas malah berbau kulkas” → masuk konten: cara simpan + alasannya
- *pertanyaan* — “pahitnya karena gilingan atau suhu air?” → jadi slide edukasi gilingan
- *keberatan* — “baru beli 2 minggu tapi rasanya hambar” → jawab: tanggal sangrai + resting
- *pertanyaan* — “bedanya robusta sama arabika apa ya” → FAQ di caption + story
- *pujian* — “ini gue banget, grinder murah bikin pahit” → quote di story (tanpa nama)
- *harga* — “ada yang harganya di bawah 50 ribu?” → masuk caption Peta Rasa
- *pertanyaan* — “bisa kirim ke luar jawa?” → masuk FAQ + caption cut-off
- *permintaan* — “kafe saya butuh 10 kg per bulan, bisa?” → tindak lanjut B2B (D2)
- *pertanyaan* — “kok berani buang? rugi dong” → jadi konten bukti batch ditolak
- *harga* — “jadi harga wajar 250 g berapa?” → masuk tabel harga per gram
- *pertanyaan* — “bisa COD Banyuwangi kota?” → masuk FAQ pengiriman
- *permintaan* — “labelnya bagus, dijual juga?” → tidak dijawab dengan janji; catat saja

## Celah kata kunci

- **kopi 250 gram murah** (marketplace, niat beli, prioritas 1,4) → belum ada halaman · status: belum ada halaman
- **rekomendasi kopi untuk pemula** (tiktok, niat info, prioritas 1,1) → kampanye/index.html · status: belum
- **kopi robusta 1 kg harga** (marketplace, niat banding, prioritas 0,9) → komersial/harga-grosir.csv · status: belum
- **cara menyimpan kopi** (google, niat info, prioritas 0,8) → belum ada halaman · status: belum ada halaman
- **kopi tubruk enak** (google, niat info, prioritas 0,8) → belum ada halaman · status: belum ada halaman

## Brief

- **01. Diagnosis masalah** — `Kopi pahit padahal baru beli: cek tanggal sangrai, gilingan, lalu suhu air` → `riset/brief/brief-01-diagnosis-masalah.md`
- **02. Perbandingan jujur** — `Arabika Ijen vs robusta Raung: ketinggian, rasa, dan cara seduhnya` → `riset/brief/brief-02-perbandingan-jujur.md`
- **03. Larangan yang bisa dibuktikan** — `Jangan beli kopi yang cuma mencetak tanggal kedaluwarsa` → `riset/brief/brief-03-larangan-yang-bisa-dibuktikan.md`
- **04. Angka + daftar** — `Tiga hal yang tercetak di tiap kantong: tanggal sangrai, kode batch, level roast` → `riset/brief/brief-04-angka-daftar.md`
- **05. Pengakuan biaya** — `Minggu ini satu batch tidak lolos — skornya 81,5, ambang kami 83` → `riset/brief/brief-05-pengakuan-biaya.md`

## Aturan pakai

1. **Adaptasi, bukan salin.** Yang diambil adalah pola (angka, larangan, pengakuan), bukan kalimat,
   footage, atau audio milik akun lain.
2. **Jangan pakai angka orang lain sebagai klaim kita.** Gunakan angka dari `data/batch-qc.csv`,
   `data/catalog.json`, atau `pesanan.csv`.
3. **Sebutkan sumber saat mengutip komentar publik**, dan potong ≤ 24 kata.
4. **Refresh ≤ 30 hari.** Pola konten cepat basi; tanggal dibuat ada di atas.
