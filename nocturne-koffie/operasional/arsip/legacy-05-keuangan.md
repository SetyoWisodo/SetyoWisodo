# D5 · Keuangan

**Tujuan:** tahu laba per bungkus, bukan hanya "ramai order".
**Pemilik:** owner · **Alat:** `data/biaya.json` + `python3 tools/papan.py`.

> ⚠️ **Penting:** seluruh angka di `data/biaya.json` masih **asumsi**. Papan menghitung dengan
> angka itu, jadi keputusan harga tidak boleh diambil sebelum angkanya diganti dengan angka nyata
> (harga green bean dari faktur, harga kemasan, upah, listrik, gas).

---

## 1. Rumus HPP per bungkus

```
HPP = (gram ÷ 1000) ÷ yield × harga_green_per_kg
      + kemasan + label + tenaga + lain-lain
margin kotor = (harga jual − HPP) ÷ harga jual
```

Asumsi awal: yield **0.80**, kemasan **Rp3.500**, label **Rp700**, tenaga **Rp1.500**,
lain-lain **Rp300** → **Rp6.000 per bungkus** + biaya kopi.

Contoh (Gayo, green Rp150.000/kg, 250 g):
`(0.25 ÷ 0.8) × 150.000 = 46.875` + `6.000` = **Rp52.875** → harga Rp99.000 → margin **47%**.

---

## 2. Target & aturan harga

| Aturan | Angka |
| --- | --- |
| Margin kotor minimum | **35%** (di bawah itu naikkan harga atau ubah ukuran) |
| Diskon | **tidak ada** diskon harga satuan |
| Insentif | bonus produk (100 g) atau gratis ongkir, maksimal senilai 8% order |
| Harga situs = harga marketplace | wajib sama |
| Perubahan harga | dicatat tanggal + alasan |

**Kenapa tidak diskon:** kopi segar premium kehilangan alasan untuk mahal kalau harganya
sering turun. Pembeli akan menunggu promo, dan margin habis.

---

## 3. Break-even

Dihitung papan otomatis:

```
biaya tetap bulanan ÷ laba kotor per order rata-rata = order minimum per bulan
```

Dengan asumsi biaya tetap Rp1.275.000 dan rata-rata laba Rp37.000/order → **35 order/bulan (±8/minggu)**.
Artinya: di bawah angka itu, bisnis belum menutup biaya tetap — bukan berarti rugi, tapi belum aman.

---

## 4. Pencatatan harian (5 menit)

Satu tempat: `data/pesanan.csv` untuk pemasukan (sudah dipakai D2). Pengeluaran dicatat di
buku kas sederhana (Sheets): tanggal, kategori, keterangan, nominal, bukti.

Kategori pengeluaran: `green bean`, `kemasan`, `jasa sangrai`, `kurir`, `iklan`, `peralatan`,
`domain/software`, `lain-lain`.

**Aturan:** setiap pengeluaran > Rp50.000 harus punya bukti (foto struk/faktur).

---

## 5. Tutup buku bulanan (45 menit)

| Baris | Rumus |
| --- | --- |
| Omzet | Σ total order (tanpa ongkir) |
| HPP | Σ (HPP per bungkus × qty) |
| Laba kotor | omzet − HPP |
| Biaya tetap | Σ biaya bulanan |
| Biaya variabel lain | iklan, kurir ditanggung, sampel |
| Laba bersih | laba kotor − biaya tetap − biaya variabel |
| Margin bersih | laba bersih ÷ omzet |

Simpan hasilnya di `data/kpi.csv` (kolom omzet) supaya tren terlihat di papan.

---

## 6. Tiga keputusan yang hanya boleh diambil dengan angka

1. **Menurunkan harga** — hanya jika margin setelah turun masih ≥ 35%.
2. **Membuka grosir/B2B** — hanya jika sisa kapasitas sangrai ≥ 25% dan margin B2B ≥ 25%.
3. **Menambah produk baru** — hanya jika ada green bean yang jelas, dan HPP-nya sudah dihitung
   (tambahkan baris di `biaya.json` sebelum produk tayang di situs).

---

## 7. KPI divisi

| KPI | Target |
| --- | --- |
| Margin kotor rata-rata | ≥ 40% |
| Margin terburuk (satu ukuran) | ≥ 35% |
| Order di bawah break-even | 0 bulan berturut-turut |
| Pengeluaran tanpa bukti | 0 |
| Waktu tutup buku | ≤ 45 menit/bulan |
