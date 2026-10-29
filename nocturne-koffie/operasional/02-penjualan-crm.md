# D2 · Penjualan & CRM

**Tujuan:** setiap chat dibalas < 2 jam, setiap order tercatat, setiap pembeli punya alasan kembali.
**Pemilik:** owner · **Alat:** WhatsApp Business + `data/pesanan.csv` + `marketing/02-copy-library.md`.

---

## 1. Alur order (6 langkah, baku)

| # | Langkah | SLA | Bukti |
| --- | --- | --- | --- |
| 1 | Chat masuk (dari situs/IG/TikTok/marketplace) | balas < 2 jam (09.00–21.00) | label `01-baru` |
| 2 | Tanya 3 hal: metode seduh, ukuran, kota kirim | 1 balasan | — |
| 3 | Cek stok di papan harian, lalu kirim rincian + ongkir | < 30 menit | — |
| 4 | Pembeli transfer/QRIS → kirim bukti | — | label `02-order` |
| 5 | Konfirmasi pembayaran, teruskan ke D4 untuk packing | hari yang sama | baris baru di `pesanan.csv` |
| 6 | Kirim resi + follow-up H+3, H+18, H+60 | terjadwal | label `03-dikirim` |

**Aturan stok:** order 1 kg atau lebih **wajib** dicek di papan sebelum dijanjikan.
Stok ditahan 24 jam setelah total dikirim, supaya tidak terjual dua kali.

---

## 2. Format pesan (jangan dikarang ulang)

Semua template ada di `marketing/02-copy-library.md`:

| Kode | Dipakai saat |
| --- | --- |
| WA-1 | Balasan pertama / auto-reply |
| WA-2 | Konfirmasi order + total + ongkir |
| WA-3 | H+3 setelah diterima (minta kesan rasa) |
| WA-4 | H+18 restock (jendela rasa terbaik habis) |
| WA-5 | H+60 pelanggan pasif |
| WA-6 | Keluhan |

Pesan order dari situs sudah berformat baku (`— Produk / — Berat / — Grind / — Jumlah`),
jadi tinggal dibalas dengan WA-2 tanpa mengetik ulang.

---

## 3. Pencatatan (satu baris per order)

`data/pesanan.csv`

```
tanggal,nomor,nama,wa,kota,produk,ukuran,qty,total,ongkir,status,sumber,resi,catatan
```

- `nomor` = `NK-MMDD-NN` (contoh `NK-1030-01`).
- `status` = `baru` → `diproses` → `dikirim` → `selesai` (atau `batal`).
- `sumber` = `web`, `instagram`, `tiktok`, `tokopedia`, `shopee`, `whatsapp`, `referral`.
- **Jangan pernah menghapus baris.** Order batal tetap dicatat — itu data, bukan sampah.

Papan harian otomatis menandai: order menunggu > 1 hari, resi kosong, dan pelanggan yang
jatuh tempo restock (H+18).

---

## 4. Langganan

| Paket | Isi | Harga |
| --- | --- | --- |
| Solo | 1 × 250 g / siklus | Rp42.000–99.000 (tergantung kopi) |
| Duo | 2 × 250 g / siklus | Rp84.000–198.000 |
| Rumah/Kantor | 1 kg / siklus | Rp148.000–352.000 |

Alur: chat "LANGGANAN" → kirim 3 pilihan → catat tanggal kirim tetap → pengingat produksi H-5 →
konfirmasi H-2 → kirim setelah sangrai mingguan. Boleh jeda/berhenti kapan saja.

**Kenapa penting:** 20 pelanggan langganan ≈ Rp 3,4 jt/bulan yang bisa **direncanakan** produksinya.

---

## 5. Pipeline B2B (kafe, kantor, reseller)

| Minggu | Aksi | Target |
| --- | --- | --- |
| 1 | Daftar 30 kafe/kantor (nama, kontak, jarak) | 30 prospek |
| 2 | Kirim 15 pesan pertama (B2B-1) | 4–6 balasan |
| 3 | Kirim 2 sampel 100 g gratis | 3–4 tes |
| 4 | Follow-up (B2B-2) + tawarkan harga | 1–2 negosiasi |
| 5–6 | Proposal (B2B-3) + batch percobaan | 1 akun aktif |

Hitungan realistis: 30 prospek → 4 tes → 1 akun. Satu kafe 5 kg/bulan ≈ Rp 1,25 jt **berulang**.
Aturan: **satu area, satu partner** — jangan jual ke 5 kafe di jalan yang sama.

---

## 6. KPI divisi

| KPI | Target bulan 1 |
| --- | --- |
| Waktu balas pertama | < 2 jam (90% chat) |
| Chat → order | ≥ 20% |
| Order terlambat diproses | 0 |
| Repeat rate | 15% |
| Nilai order rata-rata | Rp 130.000 |
| Akun B2B aktif | 0–1 |

---

## 7. Larangan

1. Menjanjikan stok tanpa cek papan.
2. Memberi diskon harga satuan (pakai bonus produk / gratis ongkir).
3. Menyimpan nomor pelanggan di luar `pesanan.csv` (hilang saat ganti HP).
4. Menjawab keluhan dengan defensif — pakai WA-6.
5. Mengirim broadcast ke nomor yang belum pernah bertransaksi.
