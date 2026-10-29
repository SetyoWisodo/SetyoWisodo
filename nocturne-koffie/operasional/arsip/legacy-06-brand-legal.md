# D6 · Brand & Legal

**Tujuan:** brand yang konsisten dan bisa dipertanggungjawabkan — bukan yang paling berisik.
**Pemilik:** owner · **Bukti kerja:** `data/legal.json`.

---

## 1. Identitas yang tidak berubah

| Elemen | Aturan |
| --- | --- |
| Nama | "Nocturne Koffie" (lockup: kata *nocturne* + baris kecil *KOFFIE BRAND*) |
| Kategori | **Brand kopi** — bukan roastery, bukan pabrik, bukan vendor |
| Mitra sangrai | Ais Coffee Roastery (nama boleh disebut, posisi setara petani) |
| Warna | Paper `#F5EFE4` · Ink `#16110D` · Burnt Orange `#E1542B` · Espresso `#4A2C1A` · Roast Gold `#D9A441` |
| Tipografi | Bricolage Grotesque (display) · Fraunces (serif) · Inter (body) |
| Nada | hangat, jujur, tenang, sedikit playful — tanpa superlatif |

---

## 2. Klaim yang dilarang (mengikat semua kanal)

1. "Kami menyangrai sendiri" / "roastery kami" / "our own roastery".
2. "Roasted fresh daily" → pakai "disangrai mingguan".
3. "Terbaik", "satu-satunya", "nomor 1" tanpa bukti yang bisa diverifikasi.
4. Klaim kesehatan apa pun.
5. Menyebut petani sebagai "pemasok" atau menampilkan foto/titik lokasi kebun.
6. Klaim "membantu petani" tanpa angka atau perjanjian yang jelas.

---

## 3. Privasi petani (tidak bisa ditawar)

- Nama boleh tayang **hanya dengan izin** (tertulis atau screenshot chat).
- **Tidak** menampilkan foto petani, koordinat, atau peta lokasi presisi.
- Level wilayah maksimum: desa–kecamatan–kabupaten.
- Data pribadi pembeli (nomor WA, alamat) tidak dipakai untuk apa pun selain pengiriman.

---

## 4. Daftar dokumen (sinkron dengan `data/legal.json`)

| Dokumen | Kenapa perlu | Status awal |
| --- | --- | --- |
| NIB | verifikasi Meta/WhatsApp API, marketplace | belum |
| Sertifikat halal | kepercayaan di marketplace | belum |
| Izin publikasi nama petani | etika & hubungan jangka panjang | belum |
| Izin nama/logo Ais Coffee Roastery | nama mitra dipakai di situs | belum |
| Kebijakan privasi | wajib sebelum formulir member & analitik | belum |
| Syarat & ketentuan | garansi & pengembalian | belum |
| Kebijakan pengiriman & ongkir | mengurangi chat berulang | belum |
| Nomor WhatsApp Business | semua order masuk sini | selesai (perlu konfirmasi) |
| Domain & email brand | kredibilitas & pemulihan akun | belum |

**Aturan:** kampanye berbayar dan pendaftaran marketplace **ditahan** sampai NIB terbit.
Situs boleh tayang tanpa NIB, asalkan halaman legal minimal (privasi + pengiriman) tersedia.

---

## 5. Audit brand bulanan (15 menit)

1. Cari kata "roastery" di semua materi (situs, IG, marketplace, kartu nama).
2. Cek 5 caption terakhir: ada superlatif atau klaim kesehatan?
3. Cek foto: ada wajah/kebun petani yang tidak berizin?
4. Cek harga: situs vs marketplace sama?
5. Perbarui `data/legal.json` lalu jalankan `python3 tools/papan.py`.

---

## 6. KPI divisi

| KPI | Target |
| --- | --- |
| Pelanggaran klaim di materi publik | 0 |
| Dokumen legal selesai | 8/9 dalam 60 hari |
| Nama petani tayang tanpa izin | 0 |
| Selisih harga situs vs marketplace | 0 |
