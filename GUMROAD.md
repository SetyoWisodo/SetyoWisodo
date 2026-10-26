# Menjual Buku di Gumroad

Semua yang dibutuhkan untuk membuka toko: produk apa saja, file mana yang diunggah,
setelan mana yang harus dinyalakan, dan batas perlindungannya.

Materi visual ada di `book/publish/gumroad/`, teks siap tempel di
`book/publish/gumroad/copy/`.

---

## 1. Kabar baik: Gumroad sudah punya penanda pembeli

Yang saya bangun sebelumnya (`personalize_pdf.py`) **tidak perlu dipakai di Gumroad**.
Gumroad melakukannya sendiri, otomatis, gratis:

| Fitur | Apa yang dilakukan |
|---|---|
| **PDF stamping** | Menempelkan email pembeli di pojok kanan bawah **halaman pertama** setiap PDF yang diunduh |
| **Unique download links** | Setiap tautan unduhan berbeda per pembeli |
| **IP + email check** | Kalau tautan dibuka dari lokasi lain, Gumroad meminta email pembeli |

Aktifkan di: **Produk → Content → tiap file PDF → toggle "Stamp PDFs with the buyer information"**.

> **PERINGATAN — jangan pakai `--protect` di sini.**
> Gumroad menyatakan terus terang: PDF yang dilindungi kata sandi **tidak bisa**
> distempel. Kalau Anda mengunggah versi berproteksi, stempel pembeli tidak akan
> pernah muncul. Unggah PDF bersih.

Efek samping yang perlu diketahui: kalau stempel PDF menyala, tombol **"Download all"**
tidak tersedia, dan pembeli mungkin melihat pesan "menyiapkan berkas" beberapa detik
sampai satu menit. Itu normal.

---

## 2. Yang tidak bisa dilindungi Gumroad

**EPUB dan DOCX tidak bisa distempel.** Gumroad hanya bisa menandai PDF. Jadi kalau
Anda menjual EPUB, berkas itulah yang paling mudah menyebar.

Tiga pilihan, urut dari paling aman:

1. **Jual PDF saja.** Paling aman, dan pembeli tetap bisa membacanya di mana saja.
2. **PDF + EPUB**, dengan EPUB sebagai "bonus kenyamanan". Terima bahwa ia bisa bocor.
3. **EPUB hanya di tier mahal.** Tidak disarankan — memindahkan risiko ke pembeli
   yang paling setia.

Saran saya: **paket standar = PDF + EPUB**, karena pembaca e-book memang mengharapkan
EPUB. Tetapi tahu di mana risikonya.

---

## 3. Empat produk

| # | Produk | File yang diunggah | Harga |
|---|---|---|---|
| 1 | Surviving the Future (EN) | PDF, EPUB, DOCX, `*_figures.zip` | **$45** |
| 2 | Bertahan Hidup di Masa Depan (ID) | PDF, EPUB, DOCX, `*_figures.zip` | **$29** |
| 3 | Bilingual bundle | kedelapan file di atas | **$59** |
| 4 | Free sample | `*_sample.pdf` (EN + ID) | **$0** (pay what you want) |

Produk 4 bukan pelengkap — ia mesin penjualannya. Sampel gratis mengumpulkan email,
masuk ke Gumroad Discover, dan menjadi tautan yang bisa Anda sebar di media sosial.

Beli-borong lebih murah dari beli terpisah ($45 + $29 = $74 vs $59) dan tetap
menguntungkan: biaya tetap $0,50 hanya dipotong sekali, bukan dua kali.

Alasan angka-angka ini ada di `HARGA_EN.md` — disusun dari harga pasar ebook
akademik ($19,99–$49,99), paperback Routledge sejenis ($34,99–$66,99), dan
harga per halaman penerbit universitas.

### Paket gambar — yang menopang harga $45

`python make_figure_pack.py` menghasilkan `*_figures.zip` per edisi: 11 gambar
300 dpi, keterangan dan baris sumbernya, plus README berisi hak pakai.

Ini bukan tambahan kosmetik. Pembaca di harga $45 hampir selalu orang yang akan
**memakai** bukunya: dosen yang butuh slide, perencana yang butuh bagan, jurnalis
yang butuh grafik. Gambar lepas membuat buku itu dipakai, bukan sekadar dibaca.
Tanpa ini, $45 hanya angka.

### Setelah dipotong biaya

Angka ini diambil dari halaman **Settings → Payments** akun Anda, bukan dari ringkasan
pemasaran Gumroad:

- **Penjualan langsung:** 10% + 50¢ (Gumroad) **+ 2,9% + 30¢** (biaya proses pembayaran)
- **Penjualan lewat Discover:** 30% (biaya proses sudah termasuk)

Artinya totalnya sekitar **12,9% + 80¢** per penjualan langsung, bukan 10%.

| Harga | Gumroad | Proses | Bersih | Persen |
|---|---|---|---|---|
| $29 | $3,40 | $1,14 | **$24,46** | 84,3% |
| $45 | $5,00 | $1,61 | **$38,40** | 85,3% |
| $59 | $6,40 | $2,01 | **$50,59** | 85,7% |
| $45 lewat Discover | $13,50 | termasuk | **$31,50** | 70% |

Perhatikan: persentase bersih **naik** seiring harga, karena biaya tetap 80¢
tidak ikut membesar. Di $45 Anda kehilangan 14,7%; di $14 Anda kehilangan 18,6%.

Discover tetap menguntungkan: 70% dari penjualan yang tanpa Discover tidak akan ada.

---

## 4. Uangnya masuk ke Indonesia bagaimana?

Kabar baiknya: **Indonesia termasuk negara yang dibayar langsung ke rekening bank,
dalam rupiah (IDR).** Tidak perlu Stripe — Stripe Connect memang tidak tersedia untuk
Indonesia.

- **Rekening bank lokal (IDR)** — cara utama, tanpa biaya perantara tambahan.
- **PayPal** — cadangan, dibayar dalam USD, ada biaya 2% + konversi.
- **Payoneer dan Wise tidak didukung.** Jangan direncanakan.
- **Saldo minimum pencairan untuk Indonesia adalah $100** dan angkanya terkunci —
  tidak bisa diturunkan. Di harga $45, dana pertama cair setelah **3 penjualan**;
  di harga $59, hanya **2 penjualan**. Ini keuntungan nyata dari harga tinggi.
- Jadwal pembayaran: mingguan. Penjualan ditahan sekitar 7 hari sebelum bisa dicairkan.

Karena Gumroad sejak 1 Januari 2025 berstatus **Merchant of Record**, PPN/VAT dan pajak
penjualan di seluruh dunia ditangani mereka. Anda tidak perlu mendaftar VAT. Pajak
penghasilan Anda di Indonesia tetap kewajiban Anda sendiri.

---

## 5. Langkah membuka toko

### A. Setelan akun (Settings)

1. **Payments** → tambahkan rekening bank Indonesia. Nama di rekening harus sama
   dengan nama di akun Gumroad, kalau tidak pencairan gagal.
2. **Settings** → nyalakan **Purchasing Power Parity**. Ini memberi diskon otomatis
   20–60% untuk pembeli di negara berpendapatan lebih rendah (data Bank Dunia,
   diperbarui tiap minggu). Untuk buku iklim yang ingin dibaca orang Indonesia,
   ini penting: pembeli lokal tidak dihukum kurs.
3. Pertimbangkan menyalakan **PayPal Connect** di checkout supaya pembeli tanpa kartu
   kredit bisa membayar.

### B. Buat produk 1 (EN)

1. **Products → New product** → Name: `Surviving the Future` → Type: Digital product
2. **Price**: $45
3. **Description**: tempel isi `book/publish/gumroad/copy/listing_en.txt`
4. **Cover**: unggah berurutan
   - `cover_en_1_hero.png`
   - `cover_en_2_inside.png`
   - `cover_en_3_quote.png`
5. **Thumbnail**: `thumb_en.png`
6. **Content**: unggah empat file (PDF, EPUB, DOCX, ZIP gambar) → **nyalakan
   stempel PDF pada file PDF**
7. **URL**: `surviving-the-future`
8. Simpan → **Publish**

### C. Ulangi untuk produk 2, 3, 4

Produk 3 memakai `cover_bundle_1_hero.png`, `cover_bundle_2_quote.png`, `thumb_bundle.png`.
Produk 4 memakai `cover_sample_1_hero.png`, `thumb_sample.png`, harga $0.

Kalau harga $0 ditolak, aktifkan **"Pay what you want"** dengan minimum $0 — efeknya
sama, dan pembeli boleh memberi tip.

**Buat produk 4 lebih dulu, sebelum yang berbayar.** Ia paling cepat jadi, paling
kecil risikonya, dan URL-nya dibutuhkan untuk ditempel ke deskripsi produk 1-3.

### D. Setelah terbit

- Buka halaman produk di jendela privat, lakukan pembelian uji dengan kode diskon 100%
  (Gumroad punya fitur **Test purchase** — pakai itu supaya tidak kena biaya).
- Periksa: apakah email Anda tercetak di halaman pertama PDF hasil unduhan?
  Kalau tidak, stempel belum menyala.
- Tempel tautan sampel gratis ke deskripsi produk berbayar.

---

## 6. Materi visual

`python make_gumroad.py` menghasilkan semuanya sekaligus dari render 3D dan PDF asli:

| File | Ukuran | Dipakai untuk |
|---|---|---|
| `cover_*_hero.png` | 2560×1440 | Sampul utama produk |
| `cover_*_inside.png` | 2560×1440 | Sampul kedua: halaman asli buku |
| `cover_*_quote.png` | 2560×1440 | Sampul ketiga: kutipan sampul belakang |
| `thumb_*.png` | 1600×1600 | Thumbnail Discover, perpustakaan, profil |
| `copy/listing_*.txt` | teks | Deskripsi siap tempel |

Spesifikasi Gumroad: sampul minimal 1280×720 (di sini 2560×1440 agar tajam di layar
retina, Gumroad menurunkan sendiri ke maksimal 4096 px), thumbnail minimal 600×600.
Maksimal 8 sampul per produk.

---

## 7. Daftar periksa sebelum mengumumkan

- [ ] Rekening bank sudah terhubung dan terverifikasi
- [ ] PPP menyala
- [ ] Stempel PDF menyala di produk 1, 2, 3
- [ ] PDF yang diunggah **bukan** versi `--protect`
- [ ] Pembelian uji berhasil, email muncul di halaman pertama PDF
- [ ] Sampel gratis bisa diunduh tanpa memasukkan email
- [ ] Tautan sampel sudah ditempel di deskripsi produk berbayar
- [ ] Deskripsi tidak memuat klaim yang tidak ada di buku
- [ ] Harga bundle lebih murah dari jumlah harga terpisah

---

## 8. Kalau ada yang membajak

Gumroad punya jalur pelaporan pembajakan (help/article/354). Karena setiap salinan
membawa email pembeli di halaman pertama, Anda bisa menunjukkan salinan mana yang
bocor dan kepada siapa ia diterbitkan. Itu bukti yang cukup kuat untuk DMCA.

Yang tidak boleh dilakukan: menyalahkan pembeli di depan umum. Satu pembeli yang
menyebarkan berkas bukan alasan memperlakukan seratus pembeli lain sebagai tersangka.

---

## 9. Yang masih harus Anda isi

Both listing files contain `[link to your free sample product]` /
`[tautan ke produk sampel]`. Setelah produk sampel jadi, ambil URL-nya
(`gumroad.com/l/xxxxx`) dan ganti penanda itu.
