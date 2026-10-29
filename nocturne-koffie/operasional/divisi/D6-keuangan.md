# D6 · Keuangan — alur kerja & target

> **Mandat:** tahu laba per bungkus, bukan hanya ramai order.
> **Pemilik:** owner · **Waktu:** 30 menit/minggu + 60 menit/bulan.
> **Berkas kerja:** `data/biaya.json` · `data/catalog.json` · `komersial/harga-grosir.csv` · `data/pesanan.csv` · `data/kpi.csv`.
> **Alat:** `python3 tools/komersial.py` (harga grosir), `python3 tools/papan.py` (margin & break-even).
> **Target & KPI:** `data/divisi.json` (D6).

D6 tidak "mencatat pengeluaran". D6 menjawab tiga pertanyaan setiap bulan:
**berapa laba per bungkus, berapa order minimum agar tidak rugi, dan harga mana yang harus naik.**

---

## 1. Alur kerja inti — dari transaksi ke keputusan harga

```
[1] Order selesai (D2/D5)
        │
        ▼
[2] Catat: omzet, ongkir ditagih, ongkir dibayar, biaya packing
        │
        ▼
[3] Hitung HPP aktual per SKU: green ÷ yield + kemasan + label + tenaga
        │        └── yield aktual dari D1, bukan asumsi 0,79
        ▼
[4] Bandingkan margin aktual vs target ≥ 35%
        │
        ├── margin di bawah target ──► [5a] Tiga pilihan: naikkan harga · ubah ukuran · negosiasi green
        │
        ▼
[6] Bulanan: tutup buku (omzet, HPP, biaya tetap, laba)
        │
        ▼
[7] Bandingkan dengan break-even → berapa order lagi yang dibutuhkan
        │
        ▼
[8] Putuskan maksimal 1 perubahan harga per bulan (jangan bereksperimen sekaligus)
```

### Rumus yang dipakai (jangan diganti tanpa alasan tertulis)

| Ukuran | Rumus | Catatan |
| --- | --- | --- |
| HPP per bungkus | (green per kg ÷ yield × gram) + kemasan + label + tenaga | yield awal 0,79 — ganti dengan aktual D1 |
| Margin kotor | (harga jual − HPP) ÷ harga jual | target ≥ 35%, saat ini terburuk 42% |
| Break-even order | biaya tetap bulanan ÷ laba kotor per order | asumsi saat ini ± Rp1.275.000 ÷ ± Rp36.000 = **35 order/bulan** |
| AOV | omzet ÷ jumlah order | target Nov Rp130.000 |
| Biaya per chat | biaya iklan ÷ chat masuk | target ≤ Rp25.000 |

### Fakta yang harus diingat sebelum menurunkan harga

- Blend 70/30 dan 60/40 punya margin paling sempit. Harga retail 1 kg (Rp170.000 / Rp195.000)
  hampir menyentuh biaya komponennya — **jangan** dijadikan objek diskon.
- Diskon satuan dilarang di semua kanal. Insentif hanya berupa bonus produk atau ongkir.
- Harga grosir dihitung `min(HPP ÷ (1 − margin tier), retail × 0,92)`: dua pagar, bukan satu.
  Jika hasilnya menandai margin < 18%, harga itu tidak boleh dikirim ke calon pembeli.

---

## 2. Ritme kerja

### Mingguan — 30 menit (Jumat)
| Menit | Kegiatan | Bukti |
| --- | --- | --- |
| 10 | Rekap kas: uang masuk, uang keluar, sisa | catatan kas |
| 10 | Isi baris `data/kpi.csv` (omzet, order, AOV) | KPI mingguan |
| 5 | Cek order yang belum dibayar & biaya kirim yang belum diganti | daftar tagihan |
| 5 | Baca papan: margin terburuk & break-even | catatan tindakan |

### Bulanan — 60 menit
1. **Tutup buku:** omzet retail + grosir, HPP, biaya tetap, laba kotor, laba bersih.
2. Revisi HPP bila yield atau harga green berubah (≥ 2 poin).
3. Jalankan `python3 tools/komersial.py` → periksa ulang harga grosir 4 tier.
4. Hitung biaya per chat & bandingkan dengan nilai order rata-rata.
5. Tulis 3 baris keputusan: apa yang naik, apa yang ditahan, apa yang dihentikan.

### Tahunan (atau saat ada perubahan besar)
Perbarui `data/biaya.json` dengan angka nyata: sewa, listrik, internet, tenaga kerja, penyusutan alat.

---

## 3. Target kerja 3 bulan

Dari `data/divisi.json` → D6.

| Ukuran | Nov 2026 | Des 2026 | Jan 2027 | Cara hitung | Arah |
| --- | --- | --- | --- | --- | --- |
| Omzet retail | Rp3,2 jt | Rp7,2 jt | Rp13,2 jt | jumlah `total` order per bulan | naik |
| Margin terburuk | ≥ 35% | ≥ 38% | ≥ 40% | margin varian terendah di papan | naik |
| Break-even | 35 order/bln | 35 | 35 | biaya tetap ÷ laba kotor per order | turun |
| Biaya tetap | Rp1.275.000 | Rp1.275.000 | Rp1.275.000 | total biaya tetap bulanan | turun |

Pendukung: pengeluaran tanpa bukti = 0 (setiap rupiah punya catatan).

**Peringatan angka:** semua biaya di `data/biaya.json` masih **asumsi**. Selama belum diganti angka nyata,
target margin & break-even adalah latihan, bukan kenyataan. Ini harus disebut saat membahas target dengan siapa pun.

---

## 4. Definisi selesai

| Rentang | Selesai bila… |
| --- | --- |
| Satu minggu | kas direkap; baris KPI terisi; tidak ada order menggantung |
| Satu bulan | tutup buku selesai; HPP diperiksa; maksimal 1 keputusan harga diambil |
| Satu kuartal | `biaya.json` memakai angka nyata; harga grosir dihitung ulang |

## 5. Serah terima

| Dari | Kepada | Apa |
| --- | --- | --- |
| D2 | D6 | omzet & AOV harian |
| D5 | D6 | biaya kirim aktual per order |
| D1 | D6 | yield & HPP aktual per batch |
| D6 | D2 | batas bawah harga & aturan diskon |
| D6 | D3 | angka yang boleh dipakai di konten (jangan sebut margin internal) |

## 6. Jebakan

1. **Menghitung laba dari omzet.** Omzet tanpa HPP & biaya tetap bukan laba — hanya angka ramai.
2. **Menurunkan harga untuk mengejar target order.** Volume lebih tinggi dengan margin rusak = rugi lebih cepat.
3. **Memakai asumsi sebagai fakta.** Sebut "asumsi" selama `biaya.json` belum diverifikasi.
4. **Mengubah harga di situs tanpa memperbarui biaya/katalog.** Papan akan menandai selisih dan semua hitungan jadi salah.
5. **Mencampur uang pribadi dan uang usaha.** Satu rekening, satu catatan, tanpa pengecualian.
