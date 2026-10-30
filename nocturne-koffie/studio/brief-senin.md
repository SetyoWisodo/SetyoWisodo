# Brief Senin — 30 Oktober 2026

> Dibuat otomatis oleh `tools/studio.py` (2026-10-30). Semua angka berasal dari `data/riset-*.csv`,
> `data/studio-hooks.csv`, dan `data/kreatif.json`. Baca 5 menit, lalu putuskan.
>
> **Status data: belum ada data asli** — 27 baris referensi, belum ada yang `asli`.
> Keputusan di bawah adalah contoh penerapan aturan, bukan kesimpulan pasar. Isi baris asli dulu.

## 1 · Tabel 10 teratas (post yang naik, dalam ceruk)

| # | Hook | Platform/format | Lift | ER | Status data |
| ---: | --- | --- | ---: | ---: | --- |
| 1 | Kopi Rp50 ribu vs Rp150 ribu — bedanya di mana? | tiktok/reel | 2,9× | 6,0% | contoh |
| 2 | Barista jelasin kenapa kopi kafe terasa lebih kuat | tiktok/reel | 2,3× | 6,3% | contoh |
| 3 | Aku salah simpan kopi 3 bulan, ini yang terjadi | tiktok/reel | 1,8× | 6,9% | contoh |
| 4 | Tiga tanda kopi sudah tidak layak diseduh | instagram/carousel | 1,8× | 9,6% | contoh |
| 5 | Kopi 250 g vs 1 kg — mana yang lebih hemat? | instagram/carousel | 1,6× | 9,0% | contoh |
| 6 | Kenapa kopimu pahit padahal baru beli | tiktok/reel | 1,5× | 6,8% | contoh |
| 7 | Kami buang 3 kg kopi minggu ini | tiktok/reel | 1,3× | 9,0% | contoh |
| 8 | Jangan beli kopi yang cuma ada tanggal kedaluwarsanya | instagram/carousel | 1,0× | 10,1% | contoh |
| 9 | Barista jelasin kenapa kopi kafe terasa beda | instagram/reel | 1,0× | 8,2% | contoh |
| 10 | Jangan giling kopi di awal minggu | instagram/carousel | 1,0× | 8,8% | contoh |

## 2 · Putuskan: dobel, hentikan, uji

| Keputusan | Isi | Alasan |
| --- | --- | --- |
| **DOBEL** | pola “Perbandingan A vs B” | struktur dengan lift median tertinggi di data |
| **HENTIKAN** | Tiga kesalahan menyimpan kopi ; Proses sangrai 12 menit dalam 20 detik | lift < 0,9× — kalah dari kebiasaan akun |
| **UJI** | Kopi pahit padahal baru beli? Cek tiga hal ini. | satu eksperimen per minggu, bukan lima |

## 3 · Lima skrip siap rekam

- **Skrip 01** (Diagnosis masalah) — “Kopi pahit padahal baru beli? Cek tiga hal ini.” · suara 100/100 · aset `reel-tanggal-sangrai`
- **Skrip 02** (Diagnosis masalah) — “Kenapa kopi kafe terasa lebih kuat dari kopi rumahan.” · suara 100/100 · aset `carousel-02b`
- **Skrip 03** (Perbandingan A vs B) — “Rp23.000 vs Rp152.000: bedanya bukan cuma berat.” · suara 100/100 · aset `carousel-01c`
- **Skrip 04** (Perbandingan A vs B) — “Arabika Ijen vs robusta Raung, satu meja.” · suara 100/100 · aset `carousel-02a`
- **Skrip 05** (Angka / daftar) — “Tiga hal yang membuat kopi rumahan terasa hambar.” · suara 100/100 · aset `carousel-02b`

Berkas lengkap: `studio/skrip/`. Setelah direkam, ubah status hook di `data/studio-hooks.csv`
menjadi `dipakai` agar tidak dipilih lagi.

## 4 · Watchlist kreator

- (contoh) akun kopi spesialti ID — 2 outlier, 69.3 interaksi/1K views

## 5 · Catatan industri

- 2026-10-24 · Perubahan jangkauan konten video pendek di beranda → perkuat simpan & bagikan, bukan sekadar tayangan
- 2026-10-25 · Makin banyak brand lokal mencetak tanggal sangrai → pindah penekanan ke kode batch + catatan QC
- 2026-10-26 · Biaya iklan marketplace naik → uji organik dulu; iklan hanya bila biaya per chat <= Rp25.000
- 2026-10-27 · Permintaan kopi robusta lokal naik → siapkan stok Raung; jadikan pintu masuk termurah

## 6 · Yang tidak dikerjakan minggu ini

- Iklan berbayar: tunggu sampai biaya per chat organik terukur.
- Kanal baru: hanya setelah kanal berjalan stabil 4 minggu.
- 50 agent LLM: diganti 10 tahap deterministik di `tools/studio.py` (0 token per tahap).

**Batas:** brief ini merencanakan konten, bukan memposting. Unggahan, balas chat, dan pembayaran
tetap di tangan Anda.
