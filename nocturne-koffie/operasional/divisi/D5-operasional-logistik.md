# D5 · Operasional & Logistik — alur kerja & target

> **Mandat:** paket sampai utuh, di hari yang sama, dengan resi yang bisa dilacak.
> **Pemilik:** owner · **Waktu:** 30 menit/hari (Senin–Sabtu) + 45 menit/minggu.
> **Berkas kerja:** `data/pesanan.csv` · `data/catalog.json` · `komersial/harga-grosir.csv`.
> **Target & KPI:** `data/divisi.json` (D5).

D5 adalah divisi yang paling terlihat oleh pembeli meski tidak pernah berbicara:
kemasan penyok, label miring, atau resi kosong akan diingat lebih lama daripada caption yang bagus.

---

## 1. Alur kerja inti — dari "dibayar" ke "diterima"

```
[1] Order berstatus `dibayar` muncul di papan
        │
        ▼
[2] Cek ulang 3 hal: SKU & ukuran · gilingan · alamat lengkap + nomor WA
        │        └── ada yang kurang? tanya D2 hari itu, jangan menebak
        ▼
[3] Ambil bungkus dari lot yang benar (kode batch di label harus cocok)
        │
        ▼
[4] Packing: kopi → valve → bubble (bila perlu) → kardus → isi gap
        │
        ▼
[5] Timbang & foto bukti packing (opsional, untuk sengketa)
        │
        ▼
[6] Input ke ekspedisi sebelum jam 15.00 → simpan nomor resi
        │
        ▼
[7] Kirim resi ke pembeli di chat yang sama (bukan chat baru)
        │
        ▼
[8] Update `pesanan.csv`: status `dikirim` + kolom `resi`
        │
        ▼
[9] H+3 cek status kurir; bila gagal antar → hubungi pembeli, jangan tunggu komplain
```

**Batas kirim hari yang sama:** order **dibayar** sebelum **15.00 WIB, Senin–Sabtu**.
Di atas jam itu → kirim besok, dan katakan besok (jangan menjanjikan hari ini).

### Daftar cek packing (cetak, tempel di meja)

| # | Cek | Gagal bila |
| --- | --- | --- |
| 1 | SKU & ukuran sesuai order | salah varian / salah berat |
| 2 | Gilingan sesuai permintaan (utuh/bubuk + metode) | pembeli menyebut "bedanya jauh" |
| 3 | Label: tanggal sangrai + kode batch tercetak | label kosong atau salah bulan |
| 4 | Valve tidak tertutup selotip | bungkus menggelembung |
| 5 | Kardus tidak bisa digoyang | isi bergeser, kemasan penyok |
| 6 | Nama & nomor WA pembeli benar | paket kembali |
| 7 | Foto bukti (bila order > Rp250.000) | sengketa tanpa bukti |

### Ongkir (indikatif — perbarui bila tarif berubah)

| Tujuan | Perkiraan | Estimasi tiba |
| --- | --- | --- |
| Banyuwangi kota | Rp0–8.000 (COD area kota) | hari yang sama |
| Jawa Timur (Surabaya, Malang) | Rp15.000–20.000 | 1–2 hari |
| Jawa (luar Jatim) | Rp20.000–28.000 | 2–3 hari |
| Luar Jawa | Rp30.000–45.000 | 3–5 hari |

Angka di atas **indikatif**; yang mengikat adalah tarif ekspedisi saat transaksi. Jangan mengutip
angka ini sebagai janji — kutip "± Rp… tergantung ekspedisi".

---

## 2. Ritme kerja

### Harian — 30 menit (Senin–Sabtu, 13.00)
| Menit | Kegiatan | Bukti |
| --- | --- | --- |
| 5 | Buka papan: order `dibayar` & resi kosong | daftar kirim hari ini |
| 15 | Packing + input ekspedisi | resi tercatat |
| 5 | Kirim resi ke pembeli | chat terkirim |
| 5 | Update `pesanan.csv` | status & resi benar |

### Mingguan — 45 menit (Sabtu)
1. Opname kemasan: valve, kardus, bubble, stiker — cukup untuk 2 minggu ke depan?
2. Rekap: berapa order telat, berapa yang gagal antar, apa penyebabnya.
3. Cek retur/komplain kemasan; catat penyebab, bukan hanya jumlahnya.
4. Siapkan paket untuk order langganan minggu depan (jangan dadakan).

### Bulanan — 30 menit
1. Hitung % kirim hari yang sama & jumlah salah kirim.
2. Bandingkan biaya kirim aktual vs yang ditagihkan ke pembeli.
3. Evaluasi ekspedisi: mana yang paling banyak gagal antar di kota tujuan utama.

---

## 3. Target kerja 3 bulan

Dari `data/divisi.json` → D5.

| Ukuran | Nov 2026 | Des 2026 | Jan 2027 | Cara hitung | Arah |
| --- | --- | --- | --- | --- | --- |
| Order perlu diproses (antrean) | 0 | 0 | 0 | order `dibayar` yang belum dikirim | turun |
| Resi belum dikirim | 0 | 0 | 0 | order `dikirim` tanpa nomor resi | turun |
| Order telat > 1 hari | ≤ 2 | ≤ 1 | 0 | order dikirim > 1 hari setelah dibayar | turun |

Pendukung: kirim hari sama 85% → 90% → 95%; salah kirim 0; komplain kemasan ≤ 4% → 3% → 2%.

**Catatan kejujuran:** target "0 antrean" berarti *pada akhir hari kerja*. Antrean siang hari itu normal.

---

## 4. Definisi selesai

| Rentang | Selesai bila… |
| --- | --- |
| Satu order | status `dikirim` + resi + pembeli sudah menerima nomor resi |
| Satu hari | tidak ada order `dibayar` yang dibiarkan lewat cut-off tanpa kabar |
| Satu minggu | opname kemasan dilakukan; 0 salah kirim |
| Satu bulan | % kirim hari sama dihitung dari `pesanan.csv`, bukan dari ingatan |

## 5. Serah terima

| Dari | Kepada | Apa |
| --- | --- | --- |
| D2 | D5 | order `dibayar` + alamat + ekspedisi |
| D1 | D5 | bungkus berlabel (tanggal sangrai + kode batch) |
| D5 | D2 | nomor resi & status kirim |
| D5 | D6 | biaya kirim aktual per order |
| D5 | D4 | kemasan/label baru untuk konten "packing" |

## 6. Jebakan

1. **Packing sebelum pembayaran terkonfirmasi.** Sekali salah, kebiasaan jadi aturan.
2. **Menjanjikan "dikirim hari ini" untuk order jam 16.00.** Janji kecil yang meleset merusak seluruh klaim brand.
3. **Menutup valve dengan selotip.** Kopi butuh mengeluarkan CO₂; bungkus bisa menggelembung.
4. **Mengirim resi lewat chat baru.** Pembeli kehilangan konteks dan mengira belum diproses.
5. **Opname kemasan hanya saat habis.** Kehabisan kardus di tengah order = order telat tanpa alasan.
