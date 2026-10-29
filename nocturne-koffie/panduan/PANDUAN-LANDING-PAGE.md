# Panduan Pembuatan Landing Page — Nocturne Koffie Brand

Turunan langsung dari **Brief Website FINAL 3.7 (4 Okt 2026)**, bagian 04, 05, 06, 10, 11.8, 12, 13, 18.
Dokumen ini bukan ringkasan brief. Isinya **cara mengerjakan landing page**: urutan, spesifikasi yang
mengikat, cara uji, dan daftar yang harus dikonfirmasi sebelum tayang.

Lapisan gerak (animasi) dijelaskan terpisah di [`07-sistem-motion.md`](07-sistem-motion.md) —
dokumen itu memuat 5 skill motion yang jadi acuan dan 13 gerak yang terpasang.

Status pekerjaan: **landing page versi uji coba sudah dibangun** dan mengikuti aturan di sini
(`index.html`, `assets/`, `data/catalog.json`). Yang berstatus sementara ditandai di bagian 8.

---

## 1. Cara memakai panduan ini

| Aturan | Artinya |
| --- | --- |
| Kerjakan berurutan | Bagian 2 (gerbang) → 3 (struktur) → 4 (visual) → 5 (komponen) → 6 (copy) → 7 (data) → 10 (uji) → 11 (tayang). |
| Satu seksi selesai = satu centang | Jangan menumpuk revisi di akhir; tiap seksi punya kriteria lulus sendiri. |
| Jangan menebak | Data yang belum ada ditulis "menunggu konfirmasi" di bagian 8, bukan dikarang di halaman. |
| Brief menang atas selera | Kalau ada yang "terasa lebih bagus" tapi melanggar aturan larangan (bagian 6), brief yang dipakai. |

---

## 2. Gerbang keputusan sebelum mulai

Landing page tidak boleh dibangun di atas data yang belum dikunci. Tujuh gerbang ini yang
berhubungan langsung dengan halaman depan (dari 18.2 brief):

| # | Harus dikunci | Kalau ditunda |
| --- | --- | --- |
| 1 | Katalog final: 9 SKU tayang + harga 4 ukuran (10.3) | Harga salah tayang, harus diulang di kartu, schema, dan format WA |
| 2 | Nama petani yang boleh tayang + izin publikasi (9.5) | Nama tayang tanpa izin = risiko hubungan dengan petani |
| 3 | Tingkat sangrai per produk (1–5) dari file desain label | Badge roast salah → filter dan ekspektasi rasa salah |
| 4 | Tasting notes 3 kata per produk | Kartu produk kosong atau berisi tebakan |
| 5 | Nomor WhatsApp Business aktif (+62 898-8188-800) | Semua tombol order mati |
| 6 | Jam operasional & target balas < 2 jam | Janji layanan di situs tidak bisa dipegang |
| 7 | Status stok per SKU + tanggal pembaruan | Situs menjanjikan kopi yang tidak ada |

**Lulus bila:** ketujuh baris punya isi atau tanggal janji yang tertulis. Tidak ada yang bertuliskan
"belum tahu".

---

## 3. Peta seksi landing page (urutan mengikat)

Urutan ini mengikuti 05 dan 06 brief. Jangan menambah seksi jualan di antara hero dan koleksi —
jarak itu yang membuat merek terasa tenang.

| # | Seksi | Tujuan | Isi wajib | Larangan |
| --- | --- | --- | --- | --- |
| 1 | Promo bar | Pintu masuk langganan | Satu kalimat tenang + tautan ke #langganan | Kata "diskon", hitung mundur, huruf berteriak |
| 2 | Navbar | Navigasi & aksi | Logo, menu, Member bertitik emas, tombol "Pesan via WhatsApp" | Menu > 5 item, "Promo"/"Sale" di menu |
| 3 | Hero | Kesan pertama | Headline 2 baris kiri, paragraf kanan, deretan kartu nama produk | Harga, foto, tasting notes di kartu hero |
| 4 | Marquee teks | Pemisah seksi | "SINGLE ORIGIN · DISANGRAI MINGGUAN · NAMA PETANI TERCANTUM" | Klaim yang tidak bisa dibuktikan |
| 5 | Our Collection | Etalase utama | Filter + 3 rail bernomor + grid detail penuh | Mega-menu, halaman katalog terpisah |
| 6 | Langganan | Mesin pertumbuhan | 3 paket + cara kerja + CTA WA | Menjanjikan diskon yang belum diputuskan |
| 7 | Manifesto | Alasan memilih | Peran brand + mitra sangrai + privasi petani | Klaim "roastery kami sendiri" |
| 8 | Member | Retensi | 4 langkah Nocturne Circle + CTA | Mencantumkan angka diskon yang belum dikunci |
| 9 | Penutup | Konversi | Ajakan WA + jam operasional | Menjanjikan balasan 24 jam kalau tidak sanggup |
| 10 | Footer | Kepercayaan & legal | Kontak, jam, tautan bantuan, © | Tautan ke halaman yang belum ada (kecuali ditandai "segera") |

### 3.1 Yang sengaja belum ditampilkan di landing page

| Elemen brief | Alasan belum ada di versi ini | Ditampilkan kapan |
| --- | --- | --- |
| Journal di menu | Belum ada 3 artikel — menu ke halaman kosong membuat brand terasa belum siap (04.3) | Setelah artikel mitra sangrai + 2 artikel lain siap |
| Pil bahasa ID·Rp / EN·$ | Butuh terjemahan manusia untuk seluruh copy + harga USD (bagian 08) | Fase 4 brief |
| Halaman produk terpisah | Landing page sudah memuat semua detail terbuka (05.7) | Setelah katalog melewati ±20 SKU |
| Formulir member mandiri | Butuh email otomatis & penyimpanan data (bagian 07) | Fase 5, setelah panel/mailer siap |
| Tautan marketplace | Tautan toko resmi belum diberikan | Begitu tautan ada — harga wajib sama dengan situs (10.9) |

---

## 4. Token desain (jangan diganti tanpa alasan tertulis)

### 4.1 Warna — 12

| Nama | Hex | Dipakai untuk |
| --- | --- | --- |
| Paper | `#F5EFE4` | Latar utama, teks di atas Ink |
| Paper-2 | `#EFE6D6` | Latar seksi Member, dasar media |
| Ink | `#16110D` | Teks, plakat petani, tombol pil, footer poster |
| Burnt Orange | `#E1542B` | Satu-satunya aksen CTA & nomor seksi |
| Espresso | `#4A2C1A` | Baris kedua headline, promo bar, ujung gradient |
| Roast Gold | `#D9A441` | Titik Member, label plakat, badge Terbatas |
| Gradient 1 | `#E1542B → #4A2C1A` | Kartu hero varian 1 |
| Gradient 2 | `#D9A441 → #7A4A1E` | Kartu hero varian 2 |
| Gradient 3 | `#93381F → #16110D` | Kartu hero varian 3 |
| Gradient 4 | `#B4703A → #3A2013` | Kartu hero varian 4 |

Aturan: maksimal **satu** aksen kuat per layar. Tidak ada gradien neon, tidak ada warna tambahan.

### 4.2 Tipografi — 3 peran

| Peran | Font | Ukuran | Catatan |
| --- | --- | --- | --- |
| Display / headline / nama produk | Bricolage Grotesque 700–800 (alt: Archivo Black) | `clamp(2.6rem, 8.4vw, 6.6rem)` untuk hero | Letter-spacing −0.03em; nama produk di kartu hero uppercase |
| Serif editorial | Fraunces 300/400 italic | 1.3–1.7rem | Kutipan manifesto & tasting notes |
| Body | Inter 400/500 | 17px, line-height 1.6 | Paragraf maksimal 52ch |

### 4.3 Spasi, garis, radius

| Token | Nilai | Dipakai untuk |
| --- | --- | --- |
| `--pad` | `clamp(18px, 4vw, 44px)` | Padding horizontal semua seksi |
| `--wrap` | 1240px | Lebar maksimum konten |
| `--nav-h` | 66px | Tinggi navbar; dipakai untuk `scroll-margin` kartu |
| Garis seksi | `2px solid Ink` | Pemisah rail, koleksi, footer |
| Garis item | `1px rgba(22,17,13,.16)` | Daftar rail, footer |
| Radius | 20px kartu hero · 6px media · 4px plakat · 999px tombol | Konsisten, jangan menambah radius lain |

Tekstur kertas: noise SVG halus `opacity .055`, `mix-blend-mode: multiply`, `pointer-events: none`.
Alasannya: latar krem polos terlihat seperti template; noise membuatnya terasa dicetak.

---

## 5. Spesifikasi komponen (kriteria lulus per komponen)

### 5.1 Navbar

- Transparan di atas hero, **solid setelah scroll > 12px** (kelas `is-solid`).
- Logo: simbol bulatan bercelah + kata "Nocturne" + baris kecil "KOFFIE BRAND".
- Menu desktop: Our Collection · Langganan · Manifesto. Member + tombol WA di kanan.
- Mobile (< 900px): hamburger → panel penuh berisi nomor 01–05, tombol WA, jam operasional.
- `aria-expanded` pada hamburger, `Esc` menutup panel, klik tautan menutup panel.
- **Lulus bila:** navbar tidak menutupi judul saat berpindah anchor (kartu memakai `scroll-margin-top`).

### 5.2 Hero + kartu bergulir

| Aspek | Spesifikasi | Cara uji |
| --- | --- | --- |
| Tinggi | 88–100vh desktop; lebih pendek di HP agar kartu tetap terlihat | Periksa di 360×740 dan 1440×900 |
| Headline | 2 baris, baris kedua berwarna Espresso | — |
| Paragraf | 2–3 baris, rata kanan kolom (desktop), maks 44ch | — |
| Isi kartu | **Nama produk saja** + label kategori/daerah kecil + panah ↗ | Cari kata "Rp" di dalam `.hcard` → harus nol |
| Gradient | 4 varian, bergilir `i % 4` | Hitung kartu 1–4 warnanya berbeda |
| Mekanisme | Track diduplikasi 2×, `translate3d(0 → −50%)`, 42 detik, linear, tanpa henti | Tidak ada lompatan saat loop |
| Kursor menyentuh | Animasi berhenti (`:hover`, `:focus-within`) | — |
| Tombol jeda | ▶ / ❚❚, `aria-pressed` berubah, label ikut berubah | Klik → berhenti; klik lagi → jalan |
| Keyboard | Tab mencapai kartu, fokus menghentikan guliran, Enter = klik | Tab 9 kali, guliran berhenti |
| Klik | Gulir ke `#kartu-<id>`, sorotan garis aksen 2 detik, URL jadi `#<id>` | Bagikan URL, muat ulang → posisi sama |
| Hemat gerak | `prefers-reduced-motion` → statis & bisa digeser manual | Aktifkan Reduce Motion di OS |

> Catatan implementasi: duplikat kartu diberi `aria-hidden="true"` dan `tabindex="-1"` supaya
> pembaca layar tidak membaca nama produk dua kali.

### 5.3 Bilah filter

- Kelompok: **Jenis** (Semua / Single Origin / Blend / Paket) · **Daerah** (Semua / Banyuwangi /
  Malang / Aceh / Bali) · **Ketersediaan** (Semua / Tersedia / Terbatas).
- Menempel di bawah navbar (`position: sticky; top: var(--nav-h)`).
- Menyaring **grid dan rail sekaligus**; rail yang kosong disembunyikan.
- Ada baris kecil "Stok diperbarui [tanggal]" dan keadaan kosong dengan tombol reset.
- Filter **tingkat sangrai** menyusul setelah gerbang #3 (data roast per produk) dikunci — jangan
  menampilkan filter yang tidak bisa menghasilkan apa pun.

### 5.4 Rail editorial bernomor

- 01 Single Origin · 02 Blends · 03 Paket & Lot Terbatas (05.9).
- Tiap item: nama, status, satu baris keterangan (origin · elevasi, atau isi paket · harga).
- Klik item = lompat ke kartu produk di grid (bukan halaman baru).
- Desktop 2 kolom, HP 1 kolom, garis pemisah antar item.

### 5.5 Kartu produk

| Elemen | Aturan |
| --- | --- |
| Foto | Rasio **4:5**, foto stiker kemasan, `loading="lazy"`, `width/height` eksplisit |
| Badge stok | Elemen paling atas media — Tersedia / Terbatas / Habis / Menunggu panen |
| Nomor editorial | Pojok kanan bawah media (01–09) |
| Eyebrow | `nomor · kategori origin · proses` |
| Nama | Display 1.55–2.15rem |
| Tasting notes | Chip serif italic, 3 kata |
| Roast | 5 bulatan; yang terisi = level; label `3/5 · Medium` |
| Plakat petani | Blok gelap: nama petani/kolektif, wilayah, elevasi, varietas |
| Harga | Nilai aktif + `/ ukuran`; 4 tombol ukuran; harga berubah saat diklik |
| Gilingan | Select: Biji utuh / Bubuk sesuai metode |
| Jumlah | − / + , batas 1–20 |
| Tombol | "Pesan via WhatsApp" — aksen Ink |
| Status Terbatas | Kalimat tenang + perkiraan lot berikutnya (tanpa "buruan!") |
| Status Habis / Menunggu panen | Tombol berubah jadi "Kabari saya saat ada" ke pesan WA berbeda |

**Aturan blend:** plakat menampilkan **komposisi** (70% Robusta Raung Natural · 30% Arabika Ijen
Full Wash), **bukan** nama petani, varietas, atau elevasi (keputusan 4 Okt 2026).

### 5.6 Pesan WhatsApp (format baku — jangan diubah gaya penulisannya)

```
Halo Nocturne Koffie! Saya mau order:
— Produk: Gayo
— Berat: 250g
— Grind: Biji utuh
— Jumlah: 1

Mohon info stok & ongkirnya ya. Terima kasih!
```

Alasan format ini baku: kelak sistem membaca pesan masuk dan mengubahnya jadi draf pesanan (6.2).
Mengubah urutan baris = merusak pembacaan otomatis.

### 5.7 Langganan & Member

- Langganan: 3 paket (Solo · Duo · Rumah/Kantor). Harga ditulis **rentang** ("Mulai Rp42.000 –
  Rp99.000 per siklus") karena bergantung kopi yang dipilih (10.8). Jangan mengarang angka tunggal.
- Member: 4 langkah tanpa akun; CTA "Jadi Member" ke WhatsApp dengan pesan berisi nama/domisili/
  email. Angka diskon **tidak** ditampilkan sampai diputuskan (gerbang 8 brief).

### 5.8 Footer

- Tiga kolom tautan: Koleksi · Brand · Kunjungi.
- Poster tipografi "NOCTURNE" selebar layar.
- Baris bawah: jam operasional, pernyataan versi uji coba, © tahun berjalan.
- Tautan yang belum ada halaman ditandai "(segera)" — bukan tautan mati tanpa keterangan.

---

## 6. Aturan copy (wajib, dari 11.8 dan 13)

| Jangan menulis | Tulis |
| --- | --- |
| "Kami menyangrai sendiri" / "our own roastery" | "Disangrai mingguan oleh Ais Coffee Roastery di Banyuwangi" |
| Menyebut Nocturne sebagai roastery | "Brand kopi" / "coffee brand" |
| "Roasted fresh daily" | "Disangrai mingguan" |
| Menyebut mitra sebagai pabrik/vendor | "Mitra sangrai" atau namanya: Ais Coffee Roastery |
| "Satu-satunya / terbaik di Indonesia" tanpa dasar | Fakta: lokasi, jadwal sangrai, nama petani, elevasi |
| Foto petani, nama desa + titik lokasi, angka kompensasi | Nama petani (dengan izin), desa–kabupaten, elevasi |
| Klaim kesehatan ("bikin fokus", "menyehatkan") | Deskripsi rasa & proses |
| Nada diskon agresif, "buruan", hitung mundur | Kalimat tenang: "Stok lot ini terbatas — lot berikutnya ±Desember" |

Nada: hangat, jujur, percaya diri tanpa sok eksklusif, sedikit playful. Nama diri brand
("Our Collection", "Journal", "Manifesto", "Member") **tidak diterjemahkan**.

Headline & paragraf hero yang dipakai:
- **ID:** "Kopi dari petani. Diseduh untukmu."
- **Paragraf:** "Setiap kemasan menyebut nama petani, desa, dan ketinggian kebunnya. Disangrai mingguan oleh Ais Coffee Roastery di Banyuwangi. Dikemas dan dikirim dari kota yang sama."
- **EN (untuk fase bilingual):** "Grown by farmers. Brewed for you." / "Every bag names the farmer, their village, and the altitude of their farm…"

---

## 7. Struktur data: satu file mengatur seluruh halaman

Semua yang berubah ada di `data/catalog.json`. Tidak ada teks produk yang ditulis dua kali di HTML.

| Field | Isi | Dipakai di |
| --- | --- | --- |
| `brand.headline` | 2 baris headline | Hero |
| `brand.intro` | paragraf hero | Hero |
| `brand.whatsapp` | nomor format `62…` tanpa `+` | Semua tombol WA, JSON-LD, noscript |
| `brand.promo_bar` | teks + CTA promo bar | Atas halaman |
| `brand.stock_updated` | tanggal pembaruan stok | Bilah filter |
| `roast_scale` | 5 tingkat (1 Light → 5 Dark) | Titik roast & label |
| `stock_states` | 4 status + kalimatnya | Badge & catatan stok |
| `products[]` | 9 SKU tayang | Hero, rail, grid, WA |
| `products[].variants[]` | 4 ukuran × harga × SKU | Tombol ukuran, harga, pesan WA |
| `bundles[]` | 2 paket (Peta Rasa, Jelajah Arabika) | Rail 03, grid |
| `subscription` | 3 paket | Seksi Langganan |
| `member` | 4 langkah | Seksi Member |

### 7.1 Menambah produk baru (±10 menit, tanpa developer)

1. Siapkan foto 4:5 (760×950 px, JPG < 200 KB), simpan di `assets/img/produk/<id>.jpg`.
2. Tambahkan satu objek ke `products[]` dengan 9 isian: `id`, `no`, `name`, `category`, `process`,
   `region`, `elevation`, `farmer`, `farmer_type`, `notes`, `roast_level`, `status`, `img`, `variants`.
3. Muat ulang halaman. Nama otomatis muncul di hero, rail, grid, dan filter.

### 7.2 Mencopot produk

- **Habis sementara:** ubah `status` → `"habis"` atau `"menunggu-panen"`. Produk **tetap tayang**
  (baik untuk SEO dan pembeli lama), tombol berubah jadi "Kabari saya saat ada".
- **Dipensiunkan:** hapus dari `products`, tapi **jangan** pakai id itu lagi untuk produk lain
  (tautan lama dan hasil pencarian akan menunjuk produk yang salah).

### 7.3 Cara mengubah status stok

Ubah `status` per produk, lalu perbarui `brand.stock_updated` ke tanggal hari itu. Tidak ada
pengurangan otomatis — pengurangan terjadi saat admin menutup order di WhatsApp (6.6).

---

## 8. Gerbang data: yang masih sementara di versi ini

Sepuluh field berikut **wajib dikonfirmasi pemilik** sebelum halaman dinyatakan tayang. Semuanya
ada di `data/catalog.json`, jadi perbaikannya cepat (tanpa menyentuh HTML/CSS).

| # | Field | Nilai sekarang | Sumber/risiko |
| --- | --- | --- | --- |
| 1 | `products[].roast_level` | 1–5 per produk | **Usulan**, bukan dari file desain label. Brief 10.6: ambil dari berkas asli |
| 2 | `products[].roast_confirmed` | `false` | Menampilkan tanda "· konfirmasi" di kartu |
| 3 | `products[].notes` | 2–3 kata per produk | Hanya Raung ("Dark Chocolate and Caramel") yang berasal dari label; sisanya usulan |
| 4 | `products[].village` / `district` | Kosong di 5 produk | Brief: desa & kecamatan baru tersedia untuk 5 origin |
| 5 | `products[].farmer` | Nama lengkap dari brief 10.4 | **Butuh izin publikasi** (gerbang 6) |
| 6 | Blue Mount Ijen: nama tayang | Andi Wijaya (perorangan) | Brief 10.4: pilih perorangan atau kolektif Ijen Coffee Collective |
| 7 | `products[].status` | Terbatas hanya di Blue Mount Ijen | Status stok nyata per hari |
| 8 | Empat konflik angka (elevasi Semeru, Raung, Ijen, kabupaten Kec. Ijen) | Memakai angka katalog | Brief 10.4: uji silang peta belum selesai |
| 9 | Varietas Gayo & Semeru | Katalog ("Lini S · Catimor" / "Andung Sari · Yellow Caturra") | Label kemasan menulis lain ("USDA, Lini's, Cobra" / "Lini S-795") |
| 10 | `subscription[].price_note` | Rentang dari 10.8 | Konfirmasi bahwa rentang ini yang dipakai, bukan harga tunggal |

Selama masih `false`/kosong, footer menampilkan "Situs versi uji coba — sebagian data menunggu
konfirmasi pemilik." Kalimat itu **tidak boleh dihapus** sebelum kesepuluh baris di atas beres.

---

## 9. Aksesibilitas & performa (syarat, bukan bonus)

| Area | Target | Cara uji |
| --- | --- | --- |
| Kontras teks | ≥ 4.5:1 untuk body; ≥ 3:1 untuk teks besar | Cek Ink di Paper (≈15:1, aman), Paper di Orange (≈3.6:1 — hanya untuk teks ≥ 24px/tebal) |
| Fokus keyboard | Semua kontrol terjangkau Tab, ada cincin fokus jelas | Tab dari awal sampai footer |
| Konten bergerak | Ada tombol jeda + hormati `prefers-reduced-motion` | Wajib (syarat aksesibilitas, 5.5) |
| Teks alternatif | `alt` deskriptif: "Kemasan Raung — Robusta Origin · Banyuwangi" | Baca `alt` tiap gambar |
| Struktur | Satu `h1`, heading berurutan, `<main>`, `<nav aria-label>` | Cek dengan pembaca layar / ekstensi heading map |
| Bahasa | `<html lang="id">` | — |
| Berat halaman awal | Hero tanpa gambar → LCP cepat; total < 1,5 MB saat pertama dibuka | Lihat tab Network |
| Gambar produk | 4:5, < 200 KB, `lazy`, `width`/`height` | — |
| Tanpa JS | Pesan + tautan WA tetap muncul (`<noscript>`) | Matikan JS, muat ulang |

---

## 10. QA sebelum tayang (25 butir)

**Struktur & konten**
- [ ] 1. Hero hanya memuat nama produk — tidak ada harga/foto di kartu.
- [ ] 2. Klik nama di hero mendarat tepat di kartu produk, tersorot ±2 detik, URL berubah.
- [ ] 3. Muat ulang URL `#raung` → langsung ke kartu Raung (bukan ke atas halaman).
- [ ] 4. Tombol jeda marquee berfungsi; ikon dan `aria-pressed` berubah.
- [ ] 5. Filter Jenis/Daerah/Ketersediaan menyaring grid **dan** rail.
- [ ] 6. Kombinasi filter kosong menampilkan pesan + tombol reset yang bekerja.
- [ ] 7. Semua 9 SKU muncul; jumlah kartu = 9 produk + 2 paket.
- [ ] 8. Harga tiap produk cocok dengan brief 10.3 (cek 4 ukuran per produk).
- [ ] 9. Klik ukuran 100 g / 1 kg → harga dan isi pesan WA ikut berubah.
- [ ] 10. Ganti gilingan → pesan WA ikut berubah.
- [ ] 11. Jumlah 1 → 3 → pesan WA menulis "Jumlah: 3".
- [ ] 12. Blend tidak menampilkan nama petani/elevasi; hanya komposisi.
- [ ] 13. Badge Terbatas muncul di Blue Mount Ijen + kalimat lot berikutnya.
- [ ] 14. Tidak ada kata "roastery" yang menunjuk Nocturne di mana pun (cari teks "roastery").
- [ ] 15. Tidak ada klaim kesehatan, "terbaik", "satu-satunya", atau hitung mundur.

**Tautan & data**
- [ ] 16. Nomor WA benar: `wa.me/628988188800` (buka di HP, pesan terisi).
- [ ] 17. Semua tautan berkas 200: CSS, JS, katalog, 9 gambar.
- [ ] 18. Tidak ada tautan mati tanpa keterangan "(segera)".
- [ ] 19. Email & Instagram di footer mengarah ke alamat benar.
- [ ] 20. JSON-LD valid (Rich Results Test) dan memuat nama, telepon, kota.

**Tampilan**
- [ ] 21. 360 px: tidak ada horizontal scroll; marquee tetap terlihat; FAB WA tidak menutupi tombol.
- [ ] 22. 768 px & 1440 px: grid 2 kolom, rail 2 kolom, tidak ada teks terpotong.
- [ ] 23. Navbar berubah solid saat digulir, tidak menutupi judul seksi.
- [ ] 24. Menu mobile bisa dibuka, ditutup (✕, Esc, klik tautan), dan mengunci scroll latar.
- [ ] 25. `prefers-reduced-motion` aktif → tidak ada animasi gulir, konten tetap terbaca.

---

## 11. Menayangkan (gratis, ±30 menit)

| Langkah | Perintah/Tindakan | Lulus bila |
| --- | --- | --- |
| 1 | Deploy folder `nocturne-koffie/` ke Netlify Drop (atau GitHub Pages) | URL HTTPS terbuka |
| 2 | Uji dari HP, bukan hanya desktop | Semua tombol WA membuka WhatsApp |
| 3 | Pasang domain (mis. `nocturnekoffie.id`), perbarui `canonical` & OG | `https://domain/` memuat halaman |
| 4 | Google Search Console: verifikasi + submit sitemap | Status "Berhasil" |
| 5 | Analytics: catat event `wa_click` per konteks | Event muncul di realtime |
| 6 | Google Business Profile (profil brand, bukan alamat pabrik) | Muncul di pencarian "kopi Banyuwangi" |

**Jangan** memasang analytics di pratinjau, dan jangan menayangkan selama gerbang 5–7 (nomor WA,
jam operasional, status stok) belum beres.

---

## 12. Sesudah landing page: urutan yang benar

| Fase brief | Isi | Prasyarat |
| --- | --- | --- |
| 3 | Halaman produk (`/produk/<nama>`) + tautan dari kartu | 9 SKU stabil, data petani lengkap |
| 4 | Bilingual ID/EN + harga USD (kurs + 25%, label "International price") | Terjemahan manusia siap |
| 5 | Formulir member mandiri + email kode | Mailer & penyimpanan data |
| 6 | Panel admin "Hari Ini" (stok, pesanan, member) | Database |
| 7 | WhatsApp Coexistence (pesan masuk → draf pesanan) | Nomor WA Business + BSP |
| 9 | SEO lanjutan: sitemap, schema produk, hreflang | Halaman produk ada |

Jangan mengerjakan fase 6–7 sebelum ada minimal 20 order nyata lewat WhatsApp — panel mahal
dibangun di atas alur yang belum terbukti.

---

## 13. Definisi selesai (landing page)

Landing page dinyatakan selesai bila **semua** ini benar:

1. Sepuluh seksi di bagian 3 ada dan berurutan.
2. 25 butir QA di bagian 10 lulus, dengan tangkapan layar disimpan di `Bukti-Nocturne/`.
3. Sepuluh field di bagian 8 sudah dikonfirmasi atau sengaja dibiarkan bertanda "uji coba".
4. Tidak ada satu pun kalimat yang melanggar tabel larangan di bagian 6.
5. Halaman dibuka dari HP dalam < 3 detik pada jaringan 4G.
6. Pemilik brand bisa mengganti harga/produk sendiri dengan mengedit satu file JSON.
