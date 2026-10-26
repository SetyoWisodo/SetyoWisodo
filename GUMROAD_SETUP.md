# Menyiapkan Akun Gumroad — Langkah demi Langkah

Panduan isi-layar. Ikuti berurutan; jangan lompat ke produk sebelum pembayaran beres,
karena produk yang terbit tanpa rekening tidak bisa dibayar.

Halaman yang sedang Anda buka: **Settings → Payments**.

---

## 0. Dua koreksi dari panduan saya sebelumnya

Saya membaca angka langsung dari halaman Anda, dan dua hal di `GUMROAD.md` ternyata
salah. Sudah diperbaiki di sana, tapi ini yang benar:

| Yang saya tulis | Yang sebenarnya |
|---|---|
| Biaya 10% + $0,50 | **10% + 50¢ + 2,9% + 30¢** biaya proses |
| Minimum pencairan $10 | **$100, terkunci untuk Indonesia** |

Artinya perhitungan bersih Anda sekitar **12,9% + 80¢** per penjualan langsung,
bukan 10%. Tabel lengkapnya sudah diperbarui di `GUMROAD.md`.

---

## 1. Payout schedule (bagian atas halaman)

| Kolom | Isi | Alasan |
|---|---|---|
| **Schedule** | `Weekly` — biarkan | Harian hanya untuk pemilik rekening bank AS |
| **Minimum payout threshold** | `$100` — biarkan | **Terkunci untuk Indonesia.** Tidak bisa diturunkan |
| **Pause payouts** | **MATI** (posisi kiri) | Kalau menyala, dana tidak akan pernah cair |

**Konsekuensi yang perlu Anda sadari:** uang baru cair setelah saldo mencapai $100.

| Harga produk | Bersih per penjualan | Penjualan untuk $100 |
|---|---|---|
| $49 (EN) | $41,88 | **3** |
| $69 (bundle) | $59,30 | **2** |

Di harga $49, dana pertama Anda cair setelah tiga penjualan. Jangan turunkan harga
hanya agar "cepat laku" — yang menentukan bukan harga, melainkan dari mana
kunjungan datang.

---

## 2. Product pages

| Toggle | Setelan | Alasan |
|---|---|---|
| **Show buyers their local currency** | **NYALA** | Pembeli Indonesia melihat harga dalam rupiah, tidak perlu menghitung kurs |
| **Keep price endings in local currency** | **NYALA** | Harga tampil Rp 199.000, bukan Rp 197.423 — terlihat rapi, bukan hasil konversi |

Anda tetap dibayar dalam USD; yang berubah hanya tampilan untuk pembeli.

---

## 3. Payout method — bagian paling penting

Sudah terpilih **Bank Account**. Ini isian yang menentukan apakah uang Anda sampai
atau hilang di tengah jalan.

| Kolom | Yang harus diisi |
|---|---|
| **Pay to the order of** | Nama **persis seperti di rekening bank Anda** — huruf besar/kecil tidak masalah, ejaan harus sama |
| **Bank code** | Kode bank 3 digit (lihat tabel di bawah) |
| **Account #** | Nomor rekening, tanpa spasi dan tanpa tanda hubung |
| **Confirm account #** | Ulangi nomor yang sama |
| **Account type** | **Individual** — pilih ini selama Anda menjual sebagai diri sendiri, bukan PT/CV |
| **First name** | Nama depan sesuai KTP |
| **Last name** | Nama belakang sesuai KTP |
| **Address** | Alamat sesuai KTP |
| **City** | Kota sesuai KTP |
| **Postal code** | Kode pos 5 digit |
| **Country** | `Indonesia` |
| **Phone number** | `+62` lalu nomor tanpa angka 0 di depan. Contoh: 0812-3456-7890 → `+6281234567890` |
| **Date of Birth** | Tanggal lahir sebenarnya. Anda harus berusia 18+ |

Catatan: pembayaran akan dikirim dalam **IDR**.

### ⚠️ Tiga kesalahan yang paling sering membuat pencairan gagal

1. **Nama tidak sama dengan rekening.** "Pay to the order of" harus identik dengan
   nama pemilik rekening. Kalau rekening atas nama orang lain (misalnya istri atau
   orang tua), pencairan akan ditolak. Gunakan rekening atas nama Anda sendiri.
2. **Nomor rekening salah ketik.** Isi dua kali dan cocokkan digit per digit. Uang
   yang sudah terkirim ke nomor salah hampir tidak mungkin ditarik kembali.
3. **Kode bank salah.** Uang dikirim ke bank yang berbeda dan memantul.

### Kode bank Indonesia yang umum

| Bank | Kode | Bank | Kode |
|---|---|---|---|
| BCA | `014` | CIMB Niaga | `022` |
| Mandiri | `008` | Permata | `013` |
| BNI | `009` | Danamon | `011` |
| BRI | `002` | BSI | `451` |
| BTN | `200` | OCBC NISP | `028` |
| Bank Jatim | `114` | Panin | `019` |
| Bank Jateng | `113` | Bank Mega | `426` |
| Bank DKI | `111` | Bukopin | `441` |

**Cocokkan dengan aplikasi bank Anda sebelum mengisi.** Kalau bank Anda tidak ada di
daftar (bank digital baru sering berbeda), buka aplikasinya atau telepon call center
dan tanyakan "kode bank BI" — jangan menebak.

### Kalau nama Anda hanya satu kata

Isi kata itu di **First name** dan ulangi di **Last name**. Kalau sistem menolak,
jangan paksa — hubungi dukungan Gumroad sebelum ada dana masuk, karena pencairan ke
nama yang tidak cocok akan terus gagal.

---

## 4. Setelah menekan "Update settings"

Gumroad biasanya meminta **verifikasi identitas (KYC)**: foto KTP atau paspor, dan
kadang selfie. Siapkan:

- KTP yang masih berlaku dan terbaca jelas
- Nama di KTP **harus sama** dengan nama di formulir tadi
- Foto diambil di tempat terang, tanpa pantulan

Verifikasi bisa makan waktu beberapa jam sampai beberapa hari. **Lakukan sekarang**,
jangan menunggu sampai ada penjualan pertama — kalau tidak, uang tertahan di saldo
dan Anda tidak bisa mencairkannya.

---

## 5. Tab Settings (bukan Payments)

Buka **Settings → Settings** (tab paling kiri), lalu nyalakan:

| Toggle | Setelan | Alasan |
|---|---|---|
| **Purchasing Power Parity** | **NYALA** | Pembeli di Indonesia otomatis dapat diskon 20–60% (data Bank Dunia). Ini yang membuat buku Anda terjangkau di dalam negeri tanpa menurunkan harga global |

Kotak **"Products to exclude"** biarkan kosong.
**"Card country and IP verification"** biarkan menyala — ia mencegah orang memalsukan
lokasi untuk mendapat diskon.

Efeknya untuk buku Anda: harga $49 di Amerika tetap $49, sementara pembeli Indonesia
membayar sekitar $20–39 tergantung penilaian Bank Dunia saat itu (diskon 20–60%).
Rupiahnya jadi lebih masuk akal tanpa Anda harus mengorbankan harga internasional.

**Jujur soal ini:** edisi Indonesia sengaja dipasang lebih murah ($29, bukan $49)
karena pembeli lokal membandingkannya dengan buku berbahasa Indonesia, bukan dengan
ebook akademik internasional. Dengan diskon PPP, pembeli Indonesia turun lagi ke
sekitar $12–23. Itu bukan menggembosi harga — itu menyesuaikan daya beli pasar yang
berbeda, dan buku akademik berbahasa Inggris memang lazim dihargai lebih tinggi
daripada edisi lokalnya.

---

## 6. Tab Billing

Isi data pajak Anda sendiri. Yang perlu diketahui: Gumroad adalah **Merchant of Record**
sejak 1 Januari 2025, jadi PPN/VAT dan pajak penjualan seluruh dunia ditangani mereka.
Anda tidak perlu mendaftar VAT di negara mana pun.

Kewajiban pajak penghasilan Anda di Indonesia tetap milik Anda sendiri — catat setiap
pencairan sebagai penghasilan.

---

## 7. Baru setelah itu: buat produk

Urutannya penting:

1. **Produk sampel gratis dulu.** Harga $0. Ini yang paling cepat jadi dan paling
   kecil risikonya kalau ada yang salah.
2. Salin URL-nya (`gumroad.com/l/xxxxx`).
3. **Produk EN $49**, tempel URL sampel ke deskripsi.
4. **Produk ID $29**, sama.
5. **Produk bundle $69**, sama.

Deskripsi dan sampulnya sudah siap di `book/publish/gumroad/`. Langkah per produk ada
di `GUMROAD.md` bagian 5.

---

## 8. Pembelian uji — jangan lewatkan

Sebelum mengumumkan ke siapa pun:

1. Buka halaman produk di jendela privat (mode incognito).
2. Gunakan **kode diskon 100%** atau fitur *Test purchase* supaya tidak kena biaya.
3. Unduh PDF-nya.
4. **Periksa halaman pertama:** apakah alamat email Anda tercetak di pojok kanan bawah?

Kalau tidak ada, stempel PDF belum menyala — buka **Content** dan nyalakan
"Stamp PDFs with the buyer information" pada file PDF.

---

## 9. Daftar periksa

- [ ] Schedule `Weekly`, threshold `$100`, Pause payouts **mati**
- [ ] Nama "Pay to the order of" identik dengan nama rekening
- [ ] Nomor rekening diketik dua kali dan cocok
- [ ] Kode bank sudah dicocokkan dengan aplikasi bank
- [ ] Account type `Individual`
- [ ] Nomor telepon diawali `+62`, tanpa `0` di depan
- [ ] Verifikasi KTP sudah diselesaikan
- [ ] PPP menyala di tab Settings
- [ ] Produk sampel gratis terbit lebih dulu
- [ ] Stempel PDF menyala di setiap produk berbayar
- [ ] Pembelian uji berhasil dan email muncul di halaman pertama PDF
