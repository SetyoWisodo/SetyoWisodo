# Runbook Minggu 1 — 30 Okt s.d. 8 Nov 2026

Rencana eksekusi per hari, per divisi, dengan durasi. Total **±6,5 jam** untuk 10 hari.
Tandai `[x]` saat selesai. Kalau satu hari terlewat, **jangan** menumpuk — lewati dan lanjut,
papan akan menandai yang tertinggal.

**Legenda pemilik:** 🧑 owner (fisik/lapangan) · 🤖 agent (bisa saya kerjakan di sesi berikutnya)

---

## Jumat 30 Okt — Fondasi (60 menit)

| ✔ | Divisi | Tugas | Waktu | Output |
| --- | --- | --- | --- | --- |
| [ ] | 🧑 D5 | Isi `data/biaya.json` dengan angka nyata: harga green bean per kg (dari faktur), kemasan, upah, listrik | 20 mnt | Biaya asli, bukan asumsi |
| [ ] | 🧑 D1 | Isi `data/stok-lot.json` dengan lot yang benar-benar ada | 15 mnt | Stok nyata |
| [ ] | 🧑 D2 | Pastikan nomor WhatsApp Business aktif + auto-reply WA-1 | 10 mnt | Chat masuk terjawab |
| [ ] | 🤖 D3 | Ganti `brand.whatsapp` di `data/catalog.json` + deploy situs (Netlify Drop) | 15 mnt | Situs bisa diakses publik |

**Selesai bila:** papan menampilkan stok & margin dari angka nyata, dan situs terbuka dari HP.

---

## Sabtu 31 Okt — Bukti (90 menit)

| ✔ | Divisi | Tugas | Waktu | Output |
| --- | --- | --- | --- | --- |
| [ ] | 🧑 D1 | Sangrai batch minggu ini + catat 1 baris di `data/batch-qc.csv` | 45 mnt | Batch terekam |
| [ ] | 🧑 D1 | Cupping H+1: skor + 3 kata rasa | 15 mnt | Skor batch |
| [ ] | 🧑 D3 | Ambil 8 klip saat sangrai/packing (tripod, tanpa bicara) | 20 mnt | 8 klip mentah |
| [ ] | 🧑 D6 | Minta izin tertulis 7 nama petani (chat WA) | 10 mnt | Izin / status |

**Selesai bila:** ada 1 batch dengan skor, dan 8 klip tersimpan di satu folder.

---

## Minggu 1 Nov — Kemasan & harga (45 menit)

| ✔ | Divisi | Tugas | Waktu | Output |
| --- | --- | --- | --- | --- |
| [ ] | 🤖 D5 | Jalankan `python3 tools/papan.py`, baca margin per ukuran; tandai yang < 35% | 10 mnt | Daftar harga perlu diperbaiki |
| [ ] | 🧑 D1 | Cetak stiker: tanggal sangrai + kode batch + 5 bulatan level roast | 25 mnt | 30 stiker siap |
| [ ] | 🧑 D6 | Tempel NIB/legal yang sudah ada ke `data/legal.json` | 10 mnt | Status legal akurat |

**Selesai bila:** setiap bungkus yang akan dijual punya tanggal sangrai + kode batch.

---

## Senin 2 Nov — Konten batch (90 menit)

| ✔ | Divisi | Tugas | Waktu | Output |
| --- | --- | --- | --- | --- |
| [ ] | 🤖 D3 | Tulis 7 caption dari `marketing/02-copy-library.md`, sesuaikan batch | 30 mnt | 7 caption |
| [ ] | 🧑 D3 | Edit 7 klip di CapCut (potong 3 detik pertama, teks besar) | 40 mnt | 7 video/visual |
| [ ] | 🧑 D3 | Jadwalkan 4 IG + 3 TikTok; isi `data/konten-14hari.csv` | 20 mnt | 7 post terjadwal |

**Selesai bila:** papan menampilkan konten untuk 3–4 Nov tanpa status "belum".

---

## Selasa 3 Nov — Buka (30 menit)

| ✔ | Divisi | Tugas | Waktu | Output |
| --- | --- | --- | --- | --- |
| [ ] | 🧑 D3 | Posting #1: "12 menit terakhir sebelum kopi dikemas" | 5 mnt | Post terbit |
| [ ] | 🧑 D2 | Broadcast WA ke 10 kontak yang pernah membeli (maks 1×) | 15 mnt | Chat masuk |
| [ ] | 🧑 D2 | Catat setiap order baru di `data/pesanan.csv` | 10 mnt | Data order |

**Selesai bila:** ada minimal 1 chat masuk dari konten atau broadcast.

---

## Rabu 4 Nov — B2B (60 menit)

| ✔ | Divisi | Tugas | Waktu | Output |
| --- | --- | --- | --- | --- |
| [ ] | 🧑 D2 | Daftar 30 kafe/kantor Banyuwangi (nama, kontak, jarak) | 30 mnt | 30 prospek |
| [ ] | 🤖 D2 | Tulis 15 pesan pertama dari template B2B-1 (personalisasi 1 kalimat) | 20 mnt | 15 pesan siap |
| [ ] | 🧑 D2 | Kirim 15 pesan | 10 mnt | 4–6 balasan (harapan) |

**Selesai bila:** 15 pesan terkirim dan dicatat tanggal follow-up H+4.

---

## Kamis 5 Nov — Stok & QC (45 menit)

| ✔ | Divisi | Tugas | Waktu | Output |
| --- | --- | --- | --- | --- |
| [ ] | 🧑 D1 | Cupping H+7 batch Sabtu lalu → lolos/tolak | 20 mnt | Keputusan batch |
| [ ] | 🧑 D1 | Perbarui `catalog.json` status + `stock_updated` | 15 mnt | Situs akurat |
| [ ] | 🤖 D4 | Cek kemasan: cukup untuk 20 paket? | 10 mnt | Daftar belanja |

**Selesai bila:** papan tidak menampilkan "beda status" untuk SKU mana pun.

---

## Jumat 6 Nov — Uang (45 menit)

| ✔ | Divisi | Tugas | Waktu | Output |
| --- | --- | --- | --- | --- |
| [ ] | 🧑 D5 | Catat semua pengeluaran minggu ini (kategori + bukti) | 15 mnt | Buku kas |
| [ ] | 🤖 D5 | Isi baris `data/kpi.csv` minggu 1 (order, omzet, AOV, chat) | 10 mnt | KPI mingguan |
| [ ] | 🧑 D5 | Putuskan: ada harga yang perlu naik? (maks 1 perubahan/bulan) | 20 mnt | Keputusan harga |

---

## Sabtu 7 Nov — Kirim (60 menit)

| ✔ | Divisi | Tugas | Waktu | Output |
| --- | --- | --- | --- | --- |
| [ ] | 🧑 D4 | Packing semua order (7 langkah SOP) | 30 mnt | Paket siap |
| [ ] | 🧑 D4 | Kirim + resi hari itu; update status di `pesanan.csv` | 20 mnt | Resi terkirim |
| [ ] | 🧑 D3 | Rekam 5 klip packing untuk konten minggu depan | 10 mnt | Stok klip |

**Selesai bila:** 0 order berstatus `baru`/`diproses`.

---

## Minggu 8 Nov — Review (30 menit)

| ✔ | Divisi | Tugas | Waktu | Output |
| --- | --- | --- | --- | --- |
| [ ] | 🤖 D5 | Jalankan papan, baca: order, omzet, margin, alert | 10 mnt | Gambaran minggu |
| [ ] | 🧑 owner | Pilih 3 prioritas minggu 2 (dari bagian "Perlu keputusan hari ini") | 10 mnt | 3 prioritas |
| [ ] | 🧑 D2 | Follow-up pelanggan yang order 18 hari lalu (WA-4) | 10 mnt | Repeat order |

---

## Yang TIDAK dikerjakan minggu ini (sengaja)

| Hal | Alasan | Kapan |
| --- | --- | --- |
| Iklan berbayar | belum ada data organik; budget bisa habis tanpa belajar | minggu 3–4 |
| Listing Shopee | butuh 5 review dulu | setelah 5 review |
| Panel admin / WhatsApp API | belum ada 20 order; mahal dibangun di atas alur yang belum terbukti | setelah 20 order |
| Formulir member mandiri | butuh email otomatis + kebijakan privasi | setelah legal dasar |
| Versi Inggris (EN · USD) | butuh terjemahan manusia | fase 4 brief |

---

## Cara membagi kerja dengan agent

| Saya kerjakan (🤖) | Anda kerjakan (🧑) |
| --- | --- |
| Menulis caption, judul, deskripsi listing | Merekam & mengedit video |
| Menyusun jadwal konten & mengisi CSV | Memposting di IG/TikTok |
| Menghitung margin, stok, break-even | Memasok angka biaya nyata |
| Menulis pesan B2B personalisasi | Mengirim WhatsApp & menelepon |
| Membuat laporan mingguan dari papan | Mencicipi kopi & memutuskan batch |
| Memperbaiki situs & teks | Packing, kirim, layani pembeli |

**Batas saya:** saya tidak bisa memposting ke akun sosial Anda, mengirim WhatsApp atas nama Anda,
menerima pembayaran, atau mencicipi kopi. Semua angka biaya di sistem ini masih asumsi sampai
Anda menggantinya.
