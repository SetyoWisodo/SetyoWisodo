# Nocturne Koffie — Website + Sistem Marketing

Website katalog + mesin penjualan untuk roastery kopi. Tanpa framework, tanpa
build step, tanpa biaya hosting. Semua order masuk ke **WhatsApp** (tempat Anda
paling mudah closing), jadi tidak perlu payment gateway di tahap awal.

```
nocturne-koffie/
├── index.html               halaman tunggal (hero, produk, QC, proses, langganan, grosir, FAQ)
├── assets/
│   ├── css/style.css        desain: midnight + amber, Fraunces + Inter
│   ├── js/app.js            render katalog, keranjang, checkout WhatsApp
│   └── img/                 3 foto placeholder (ganti dengan foto asli)
├── data/catalog.json        ← SATU-SATUNYA file yang perlu Anda ubah
└── marketing/               strategi, kalender konten, copy, marketplace, CRM
```

## Cara menjalankan

```bash
cd nocturne-koffie
python3 -m http.server 8080     # buka http://localhost:8080
```

Harus lewat server (bukan dobel-klik `index.html`) karena katalog dimuat via
`fetch`. Kalau dibuka langsung dari file, browser memblokir `fetch` dan katalog
tidak muncul.

## Yang WAJIB diganti sebelum dipakai

Buka `data/catalog.json`:

| Field | Isi sekarang | Ganti jadi |
| --- | --- | --- |
| `brand.whatsapp` | `62812XXXXXXXX` | nomor WA asli, format `62…` tanpa `+` dan tanpa spasi |
| `brand.instagram` | `instagram.com/nocturnekoffie` | URL IG asli |
| `brand.city` | Banyuwangi | kota asli |
| `products[].variants[].price` | harga contoh | harga asli Anda |
| `products[].notes` / `origin` | contoh | sesuai green bean yang benar-benar ada |

Harga, nama, ukuran, dan pilihan gilingan otomatis muncul di website dan ikut
dihitung di keranjang. Setelah mengubah file, cukup refresh browser.

Ganti 3 gambar di `assets/img/` dengan foto asli (nama file sama, atau ubah
`img` per produk). Ukuran ideal: hero 1600×900, produk 1200×750, format JPG
< 300 KB supaya cepat di HP.

## Cara deploy (gratis)

| Platform | Langkah | Catatan |
| --- | --- | --- |
| **Netlify Drop** | buka app.netlify.com/drop, tarik folder `nocturne-koffie` | paling cepat, gratis, HTTPS otomatis |
| **GitHub Pages** | push repo, Settings → Pages → root | cocok karena proyek ini sudah di Git |
| **Vercel** | import repo, framework "Other" | gratis untuk hobby |

Setelah punya domain, arahkan ke hosting tersebut (Netlify/Vercel memberi
petunjuk DNS). Update `canonical` di `index.html` kalau domain berbeda.

## Fitur yang sudah jalan

- Katalog 6 produk dengan filter kategori (espresso/filter/decaf/bundle)
- Varian ukuran (250 g / 500 g / 1 kg) + pilihan gilingan per produk
- Harga berubah otomatis saat varian diganti
- Keranjang tersimpan di browser (localStorage) — tidak hilang saat refresh
- Checkout menyusun pesan WhatsApp lengkap: item, qty, subtotal, nama & alamat
- Tombol WhatsApp di hero, CTA, grosir, dan footer dengan pesan berbeda per konteks
- Langganan bulanan (klik → chat WA dengan paket terisi)
- JSON-LD `LocalBusiness` untuk SEO + meta OG untuk preview saat dibagikan
- Mobile-first, tombol keranjang melayang, animasi reveal yang menghormati
  `prefers-reduced-motion`

## Yang sengaja TIDAK dibuat (dan alasannya)

- **Payment gateway**: belum perlu. Transfer/QRIS via WA lebih murah dan
  pembeli tahap awal biasanya tanya dulu sebelum bayar.
- **Login/akun**: menambah friksi, tidak menambah penjualan di skala ini.
- **Blog**: SEO lokal lebih efektif lewat Google Business Profile dulu.
- **Keranjang multi-halaman**: satu modal cukup dan lebih cepat di HP.

## Dokumen marketing (baca berurutan)

| File | Isi | Waktu baca |
| --- | --- | --- |
| `marketing/00-strategi-90hari.md` | positioning, ICP, tangga harga, ritme 7 jam/minggu, target 90 hari | 12 mnt |
| `marketing/06-checklist-launch-14hari.md` | langkah konkret 2 minggu sampai siap jualan | 8 mnt |
| `marketing/02-copy-library.md` | bio, 15 caption, template WA, skrip B2B | 15 mnt |
| `marketing/01-kalender-konten-30hari.md` | 30 hari konten dengan hook & aset | 10 mnt |
| `marketing/03-marketplace-dan-ads.md` | judul & deskripsi listing, bundling, aturan iklan | 10 mnt |
| `marketing/04-whatsapp-crm-dan-b2b.md` | alur follow up, langganan, pipeline kafe | 10 mnt |
| `marketing/05-kpi-tracker.csv` | tracker mingguan (buka di Sheets) | — |

## Prinsip yang dipakai di semua materi

1. **Anda jual kesegaran + bukti QC**, bukan harga murah atau "kopi enak".
2. **Satu pesan, empat pintu**: konten → website/WA/marketplace.
3. **Jangan diskon harga satuan** — pakai bonus atau gratis ongkir.
4. **B2B lebih besar daripada retail** (1 kafe 5 kg ≈ 15 order retail 250 g),
   tapi retail membangun bukti sosial yang dipakai saat jualan B2B.
5. **Waktu Anda dibatasi 7 jam/minggu.** Kalau sebuah aktivitas tidak masuk
   ritme itu, jangan dikerjakan.
