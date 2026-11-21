# Rencana website komersial — jawaban jujur

Dibuat dari isi repo oleh `tools/rencana.py`. Semua angka di bawah dibaca dari disk, bukan diketik manual.

## 1. Yang sudah jadi — jangan dibuat ulang

| Halaman | Isi | Berat |
| --- | --- | --- |
| `index.html` — Beranda | hero rak + koleksi + langganan + member | 27.1 KB |
| `biji-sangrai/index.html` — Biji sangrai | halaman ala jiro.build, 9 lot | 28.8 KB |
| `katalog/index.html` — Katalog foto | bukti sesi foto, 9 SKU | 5.5 KB |
| `rak/index.html` — Rak 3D | rak kemasan 500 g, 9 lot | 4.9 KB |
| `kampanye/index.html` — Kampanye | landing kampanye | 20.9 KB |
| `komersial/penawaran-b2b.html` — Penawaran B2B | harga grosir & sampel | 9.1 KB |
| `motion/index.html` — Lab gerak | pustaka gerak & pratinjau | 28.5 KB |
| `brand/index.html` — Brand kit | logo, label, palet | 5.0 KB |

| Angka | Nilai |
| --- | --- |
| Lot yang sudah tayang | **9** |
| Ukuran kemasan | 1 kg, 100 g, 250 g, 500 g |
| Foto studio 2000 px | **36** |
| Foto marketplace putih | **18** |
| Berat aset gambar | 17.2 MB |
| Beranda | 27.1 KB · 6 tombol WhatsApp · kartu digambar dari `data/catalog.json`: ya |
| Dokumen legal selesai | **1 / 9** |

Artinya: **pondasi situsnya sudah ada**. Beranda, katalog, halaman lot, kampanye, B2B, foto 2000 px, dan data yang menggerakkan kartu semuanya sudah jalan tanpa framework dan tanpa CDN. Yang belum ada bukan pondasi, melainkan **lapisan jual**.

## 2. Yang belum ada (dan bisa dikerjakan sekarang)

| # | Pekerjaan | Skill yang dipakai | Ukuran |
| --- | --- | --- | --- |
| 1 | Beranda komersial (keranjang + ringkasan order) | `motion-web, landing-page-ai` | sedang |
| 2 | Halaman produk per lot (`/lot/<id>/`) | `katalog-render, landing-page-ai` | sedang |
| 3 | Halaman kebijakan (privasi, syarat, pengiriman) | `landing-page-ai` | kecil |
| 4 | Sitemap, robots.txt, 404, manifest | `motion-web` | kecil |
| 5 | Struktur data produk & FAQ (JSON-LD) | `search-intent-riset` | kecil |
| 6 | Gerak masuk halaman produk + transisi | `motion-web, gsap, motion-design` | sedang |
| 7 | Nada & teks halaman (bukan template) | `desain-prompt, studio-konten` | kecil |
| 8 | Hero 3D adegan (three.js + postprocessing) | `threejs, postprocessing, quarks-vfx, tweakpane` | besar |
| 9 | Fisika di halaman (biji jatuh, kotak bertumpuk) | `rapier-physics` | besar, opsional |
| 10 | Figure penjelas isometrik (proses sangrai) | `anatomy, anatomy-reveal` | sedang |
| 11 | Garis isometrik yang menjawab pointer | `hairline-create, hairline-adopt` | sedang |
| 12 | Video produk dari data katalog | `remotion, remotion-skills, ffmpeg-encode` | besar |
| 13 | Animasi diagram (rasio seduh, profil sangrai) | `manim` | sedang |
| 14 | Lottie penanda proses | `lottie` | kecil |
| 15 | Musik & SFX berlisensi | `openverse-audio, librosa-beat` | kecil |
| 16 | Caption animasi (bila ada narasi) | `whisperx-captions` | sedang |
| 17 | Aset 3D dari Blender (bila perlu mesh baru) | `blender-mcp` | besar, belum teruji |

Urutan yang saya sarankan (bukan semua sekaligus):

1. **Jalur beli yang tidak putus** — keranjang kecil di beranda + halaman ringkasan order yang menghasilkan satu pesan WhatsApp rapi — *sedang*
2. **Sitemap + robots + 404 + manifest** — memalukan kalau domain aktif tanpa ini — *kecil*
3. **Halaman produk per lot** — alamat sendiri (`/lot/gayo/`), bisa dibagikan, bisa diindeks — *sedang*
4. **JSON-LD Product + FAQ** — harga & stok terbaca mesin pencari — *kecil*
5. **Halaman kebijakan** — ditulis dari `data/legal.json`, bukan dikarang — *kecil*
6. Baru **gerak & aset berat** (three.js, anatomy, video) — kalau 1–5 sudah jalan

## 3. Yang TIDAK bisa saya tutup (butuh Anda)

| Butir | Status | Jalan keluarnya |
| --- | --- | --- |
| **Domain & email brand** | Belum dibeli. Situs masih `nocturnekoffie.id` sebagai canonical tanpa DNS; email memakai Gmail. | beli domain + email → ganti canonical, sitemap, OG URL |
| **Kebijakan privasi** | Belum ada. Wajib sebelum formulir member/analitik aktif. | tulis di halaman `/privasi/` dari `data/legal.json`, bukan dokumen baru |
| **Syarat & ketentuan** | Belum ada. Wajib memuat garansi & pengembalian. | tulis di `/syarat/`, rujuk ke `data/catalog.json` untuk klaim |
| **Kebijakan pengiriman & ongkir** | Butuh keputusan kurir dan tarif — keputusan Anda. | tabel kurir di `/pengiriman/` setelah keputusan |
| **Izin nama petani & Ais Coffee Roastery** | Nama sudah tayang, izin belum. | surat izin tertulis; bukan pekerjaan kode |
| **Pembayaran otomatis** | Belum ada gateway; semua order lewat WhatsApp. | butuh akun Midtrans/Xendit (NIB) — jangan dikarang |

Dokumen yang masih kosong menurut `data/legal.json`: NIB (perizinan berusaha), Sertifikat halal, Izin publikasi nama petani (7 nama), Izin pemakaian nama & logo Ais Coffee Roastery, Kebijakan privasi, Syarat & ketentuan, Kebijakan pengiriman & ongkir, Domain & email brand.

Saya tidak akan menulis kebijakan privasi seolah-olah itu fakta hukum, dan tidak akan memasang pembayaran yang belum ada akunnya. Keduanya bisa **disiapkan** (struktur halaman + tempat isinya), tapi isinya harus dari Anda.

## 4. Batas menguji tampilan — jujur

Di sandbox ini **tidak ada Chromium** (`playwright install chromium` gagal mengunduh). Artinya:

| Yang bisa diuji mesin | Yang tidak bisa |
| --- | --- |
| HTML seimbang, tautan tidak putus, ukuran berkas, isi data, latar putih foto, kontras teks, urutan judul, JSON-LD valid | **rupa sungguhan**: apakah section muat satu layar, apakah tombol nyaman di ponsel, apakah animasi halus |

Rencana saya untuk menutup celah ini: `tools/pratinjau.py` yang sudah ada diperluas jadi **lembar kontak**: tangkapan teks + ukuran per section, bukan tangkapan piksel. Kalau Anda mau menilai rupa, buka Live Preview port 8080 — di situ peramban Anda yang menjadi mesin uji, bukan saya.

## 5. Jawaban singkat

**Bisa mulai sekarang**, dan tidak perlu memasang apa pun: 22 skill gerak sudah ada di `.agents/skills/`, 12 skill konten di `skills/`, datanya lengkap. Tapi yang paling menentukan penjualan bukan efek 3D — melainkan **jalur beli yang tidak putus** dan **halaman produk yang bisa diindeks**. Keduanya bisa selesai tanpa satu baris WebGL.

