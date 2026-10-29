# WhatsApp CRM & Pipeline B2B — Nocturne Koffie

WhatsApp adalah tempat uang masuk. Semua traffic (website, IG, marketplace)
bermuara ke sini. Modal awalnya: 1 nomor WhatsApp Business, 1 Google Sheet,
dan template di `02-copy-library.md`.

---

## 1. Setup WA Business (30 menit, sekali)

- [ ] Daftar **WhatsApp Business** (gratis) — bukan WA biasa.
- [ ] Profil: nama `Nocturne Koffie ☾`, kategori *Coffee Shop*, lokasi Banyuwangi,
      jam buka, dan link website.
- [ ] Katalog WhatsApp: isi 5 produk (foto + harga) — pembeli bisa lihat tanpa
      keluar chat.
- [ ] Pesan sambutan (auto-reply): pakai `WA-1` di copy library.
- [ ] Pesan di luar jam kerja: "Saya balas besok pagi sebelum 09.00".
- [ ] Label chat: `01-baru`, `02-order`, `03-dikirim`, `04-langganan`, `05-b2b`,
      `06-perlu-followup`, `07-keluhan`.
- [ ] Pesan cepat (shortcut): `halo`, `order`, `rekening`, `ongkir`, `grosir`.
- [ ] Balasan cepat FAQ: "Bisa COD?", "Bisa giling?", "Berapa lama sampai?"

**Aturan respons:** balas < 2 jam di jam kerja (08.00–21.00). Chat yang dibalas
> 6 jam kehilangan peluang closing jauh lebih besar — ini bukan soal sopan,
ini soal konversi.

---

## 2. Database pelanggan (Google Sheet, 12 kolom)

Buat sheet `Pelanggan` dengan header ini:

```
tanggal_order | nama | wa | kota | produk | ukuran | gilingan | qty |
total | sumber | tanggal_sangrai | status
```

`sumber` = `web`, `ig`, `tiktok`, `tokped`, `shopee`, `referral`, `walkin`.

**Turunan yang harus dihitung tiap minggu** (rumus spreadsheet, bukan manual):

| Metrik | Rumus | Kenapa penting |
| --- | --- | --- |
| Repeat rate | jumlah `wa` dengan >1 order ÷ total `wa` | Kesehatan produk |
| Nilai order rata-rata | total ÷ jumlah order | Efek upsell |
| Sumber terbaik (omzet) | SUMIF(sumber) | Tahu harus fokus ke mana |
| Hari sejak order terakhir | TODAY() − tanggal_order | Daftar follow up |
| Pelanggan langganan aktif | COUNTIF(status="langganan") | Prediksi produksi |

---

## 3. Alur follow up (jalankan 20 menit/hari, tidak lebih)

| Waktu | Aksi | Template |
| --- | --- | --- |
| H+0 | Konfirmasi order + total + tanggal sangrai | `WA-2` |
| H+1 | Kirim nomor resi | (tulis singkat) |
| H+3 | Tanya sudah sampai & minta kesan rasa | `WA-3` |
| H+10 | Kalau belum ada review: tanya sekali, sopan | `WA-3` versi pendek |
| H+18 | Tawarkan restock (jendela rasa terbaik habis) | `WA-4` |
| H+60 | Reaktivasi pelanggan pasif | `WA-5` |
| Kapan pun | Keluhan | `WA-6` |

**Aturan broadcast:** maksimal **1×/minggu**, hanya ke pelanggan yang pernah
order. Isi broadcast: 1 batch baru + 1 tips + 1 CTA. Jangan kirim ke nomor yang
belum pernah berinteraksi (kena blokir & nomor bisa dibatasi WhatsApp).

---

## 4. Langganan: buat semudah mungkin

1. Pembeli chat "LANGGANAN".
2. Kirim 3 pilihan (lihat `catalog.json` → `subscription`).
3. Catat di sheet: `status=langganan`, produk, qty, **tanggal kirim tetap**.
4. Buat **pengingat produksi** 5 hari sebelum tanggal kirim.
5. H-2 kirim konfirmasi: "Batch [tanggal] siap, kirim [tanggal]. Mau ganti
   varian atau lanjut yang sama?"
6. Jeda/berhenti: layani tanpa drama. Pelanggan yang bisa berhenti mudah justru
   lebih lama bertahan.

**Kenapa langganan penting untuk Anda:** Anda bisa **merencanakan produksi**
(green bean, jadwal sangrai) — ini keunggulan operasional, bukan cuma marketing.
Target: 20 pelanggan langganan = ±Rp 3,4 jt/bulan yang bisa diprediksi.

---

## 5. Pipeline B2B (kafe, kantor, reseller)

### Target realistis

| Minggu | Aksi | Target hasil |
| --- | --- | --- |
| 1 | Daftar 30 kafe/kantor di Banyuwangi & sekitar (nama, kontak, jenis) | 30 prospek |
| 2 | Kirim 15 pesan pertama (`B2B-1`) | 4–6 balasan |
| 3 | Kirim 2 sampel gratis ke yang berminat | 3–4 tes |
| 4 | Follow up (`B2B-2`), tawarkan harga | 1–2 negosiasi |
| 5–6 | Kirim proposal (`B2B-3`), batch percobaan | 1 akun aktif |

**Hitungan:** 30 prospek → 4 tes → 1 akun. Nilai 1 akun kafe 5 kg/bulan ≈
Rp 1,25 jt/bulan **berulang**. Jadi 4 akun ≈ Rp 5 jt/bulan, lebih besar dari
puluhan order retail — dan tidak butuh konten harian.

### Aturan B2B

1. **Satu area, satu partner.** Jangan jual ke 5 kafe di jalan yang sama —
   mereka saling berhadapan, dan harga Anda akan diperang-perangi.
2. **Selalu kirim sampel dulu.** Kafe membeli rasa, bukan deskripsi.
3. **Tawarkan kalibrasi.** Datang sekali, bantu setting grinder + rasio.
   Ini yang membuat kafe bertahan (dan sulit diganti kompetitor).
4. **Catat profil batch** yang disetujui; ulangi profil itu untuk order
   berikutnya. Konsistensi adalah produk B2B Anda.
5. **Private label** ditawarkan setelah 10 kg/bulan stabil — bukan sebagai
   daya tarik awal (mahal & merepotkan kalau volume belum ada).

### Template spreadsheet pipeline B2B

```
nama_tempat | jenis (kafe/kantor/reseller) | kontak | sumber | tanggal_kirim_pesan |
status (dikirim/dibalas/sampel/negosiasi/aktif/pass) | volume_target_kg |
harga_disepakati | tanggal_followup | catatan
```
