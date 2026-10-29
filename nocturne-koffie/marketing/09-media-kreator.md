# D3 · Konten Media Kreator — playbook kampanye

> **Siapa:** D3 Marketing (memilih, menulis, menjadwalkan, mengukur) + D4 Kreatif (memproduksi aset).
> **Untuk apa:** mengubah proses produksi jadi konten yang membuat orang percaya, lalu masuk ke WhatsApp.
> **Aset:** `konten/` (hub), `data/kreatif.json` (manifest), `kampanye/index.html` (landing).
> **Target:** 16 → 20 → 24 konten terbit/bulan; 40 → 100 → 180 chat masuk/bulan.

Berkas ini bukan daftar ide. Isinya **sistem**: apa yang direkam, bagaimana dijadikan aset,
di mana ditaruh, dengan kalimat apa, dan bagaimana diukur.

---

## 1. Posisi: kenapa konten "proses" dan bukan konten "produk"

Sembilan SKU kopi dengan label bagus masih bisa dikalahkan brand yang lebih besar dan lebih murah.
Yang tidak bisa ditiru adalah **bukti**: catatan QC, batch yang ditolak, tanggal sangrai, jam cut-off.
Karena itu porsi konten:

| Pilar | Porsi | Isi | Contoh aset |
| --- | --- | --- | --- |
| **Bukti** | 30% | data & keputusan yang tidak menyenangkan | `reel-04-batch-ditolak`, `carousel-04a` |
| **Proses** | 30% | apa yang terjadi sebelum kopi dikemas | `reel-01-menit-terakhir`, `reel-03-first-crack` |
| **Edukasi** | 25% | cara memakai/menyimpan, tanpa menggurui | `carousel-02a`, `story-01` |
| **Jualan** | 15% | pintu masuk termurah + paket | `post-01-peta-rasa`, `carousel-03a` |

Aturan urutan: **tidak boleh dua konten jualan berurutan.** Jualan selalu didahului satu bukti.

---

## 2. Pipeline aset (D4 → D3)

```
rekam (owner, 20 mnt/minggu)      render (agent)                tayang (D3)
─────────────────────────────     ───────────────────────       ────────────────────
sangrai · cupping · packing  →    tools/kreatif.py        →     IG Reels · TikTok
8–10 klip @30–60 detik            video 9:16 + poster            Carousel · Story
                                  carousel 4:5 · feed 1:1        WA Status · Marketplace
                                  hub konten/index.html          landing kampanye
```

Jalankan:

```bash
python3 tools/kreatif.py          # render semua aset (±90 detik, butuh ffmpeg)
python3 tools/kreatif.py --cepat  # hanya gambar (tanpa encode video)
python3 tools/kampanye.py         # landing page kampanye dari katalog + manifest
```

**Batas yang harus diakui:** video yang dirender generator adalah **grafik + teks dari data**,
bukan footage sangrai. Jangan pernah menyebutnya dokumentasi. Kalau ada klip asli, klip asli menang.

---

## 3. Format yang dipakai (dan alasan durasinya)

| Format | Durasi / ukuran | Kenapa | Hook 3 detik pertama |
| --- | --- | --- | --- |
| Reel proses | 7 detik, 9:16 | loop bersih, tidak perlu audio | angka + tindakan ("12 menit terakhir…") |
| Reel bukti | 7 detik, 9:16 | satu klaim, satu bukti | pengakuan ("Minggu ini satu batch tidak lolos") |
| Carousel bukti | 3 slide, 4:5 | bisa disimpan & dibaca ulang | slide 1 = pertanyaan yang mengganggu |
| Carousel edukasi | 2 slide, 4:5 | satu ide per slide | kesalahan umum, bukan "tips" |
| Story jajak pendapat | 1 frame, 9:16 | menaikkan balasan DM | pertanyaan yang mudah dijawab |
| Feed jualan | 1:1 | harga + satu CTA | harga & isi paket langsung terlihat |

Tiga detik pertama menentukan. Semua judul di bawah sudah ditulis untuk 3 detik itu —
jangan menambahkan intro ("Halo semuanya, kali ini…").

---

## 4. Bank hook (dipakai bergiliran, jangan diulang dalam 2 minggu)

| # | Hook | Pilar | Pasangan aset |
| --- | --- | --- | --- |
| 1 | "12 menit terakhir sebelum kopi ini dikemas." | Proses | `reel-01` |
| 2 | "20 detik lebih lama, rasanya berubah." | Proses | `reel-01` (beat 3) |
| 3 | "Kami tidak mencetak tanggal kedaluwarsa." | Bukti | `reel-02` |
| 4 | "Rasa terbaiknya 7–21 hari setelah sangrai." | Edukasi | `reel-02` |
| 5 | "Minggu ini satu batch tidak lolos." | Bukti | `reel-04`, `carousel-04a` |
| 6 | "Skornya 81,5. Ambang kami 83." | Bukti | `reel-04` |
| 7 | "Order sebelum jam 15.00, dikirim hari itu." | Bukti | `reel-05` |
| 8 | "Biji utuh bertahan 3–4× lebih lama." | Edukasi | `carousel-02a` |
| 9 | "Belum punya grinder? Mulai dari sini." | Jualan | `carousel-03a` |
| 10 | "Tiga tanda kopi masih segar." | Edukasi | `story-01` |
| 11 | "Kopi di rumah Anda berapa lama?" | Story | `story-02` |
| 12 | "Dengar ini sekali." (first crack) | Proses | `reel-03` |

Hook yang **tidak boleh** dipakai: "promo", "buruan", "diskon", "termurah", "nomor satu",
"terbaik di Banyuwangi", "fresh from the roastery" tanpa tanggal.

### 4b. Bank hook versi mesin — `data/studio-hooks.csv`

12 hook di atas adalah yang sudah terjadwal. Bank lengkapnya sekarang **30 hook** di
`data/studio-hooks.csv` dengan kolom `struktur` (10 kategori), `pilar`, `aset`, dan `status`
(`dipakai` / `belum`). `tools/studio.py` membaca berkas ini, mengurutkan berdasarkan lift median
struktur, lalu memilih **satu film pertama** — hanya dari hook yang asetnya benar-benar ada di
`data/kreatif.json`.

Siklus yang dipakai (bukan 50 agent, tapi 4 perintah):

| Langkah | Perintah / berkas | Yang diputuskan |
| --- | --- | --- |
| pilih hook | `python3 tools/studio.py` → §05 | satu hook, satu struktur, satu aset |
| tulis skrip | `studio/skrip/skrip-01..05-*.md` | 9 detik: hook 3s + 2 baris bukti + CTA |
| cek suara | otomatis (`cek_suara`) | kata terlarang, superlatif, kalimat > 18 kata, angka, CTA |
| rekam | `studio/skrip/`, shot list per struktur | 8–10 klip sesuai 5 skrip |
| tandai | ubah `status` jadi `dipakai` | supaya tidak terpilih lagi minggu depan |

Aturan tambahan: **jangan menulis hook baru sebelum 18 hook `belum` habis.** Menambah bank lebih
cepat daripada memakai bank adalah cara paling umum membuat jadwal macet.

---

## 5. Jadwal batch 1 (3–20 Nov 2026)

| Tanggal | Kanal | Aset | Pilar | Status |
| --- | --- | --- | --- | --- |
| 3 Nov | IG Reels | `reel-01-menit-terakhir` | Proses | siap |
| 4 Nov | IG Carousel | `carousel-01a/b/c` | Bukti | siap |
| 5 Nov | TikTok | `reel-03-first-crack` | Proses | siap |
| 6 Nov | IG Story | `story-01`, `story-02` | Edukasi | siap |
| 7 Nov | IG Carousel | `carousel-04a` | Bukti | siap |
| 10 Nov | IG Post | `post-01-peta-rasa` | Jualan | siap |
| 11 Nov | TikTok | `reel-05-kirim-hari-ini` | Bukti | siap |
| 13 Nov | IG Reels | `reel-02-tanggal-sangrai` | Bukti | siap |

Sumber kebenaran jadwal tetap `data/konten-14hari.csv`; tabel ini ringkasan untuk dibaca cepat.
Setelah tayang, ubah `status` di CSV **dan** di `data/kreatif.json` (agar papan tidak menampilkan aset basi).

---

## 6. Caption & CTA — aturan penulisan

1. **Satu ide per konten.** Kalau ada dua, salah satunya jadi konten minggu depan.
2. **Angka lebih baik daripada kata sifat.** "81,5 dari ambang 83" > "kualitas terjaga".
3. **CTA tunggal.** Selalu menuju WhatsApp dengan pesan awal, bukan "link di bio" saja.
4. **Sebut kode batch** di caption bukti — itu satu-satunya bukti yang bisa dicek pembeli.
5. **Jangan menyebut margin, HPP, atau target internal.** Itu untuk papan, bukan publik.
6. **Panjang:** IG 400–700 karakter; TikTok 80–150; Story 1 kalimat.

Template CTA WhatsApp (teks otomatis, sudah dipakai di landing):

```
Halo, saya lihat konten [nama aset] di [kanal].
(utm: kampanye=kopi-jujur-soal-tanggal; kanal=<kanal>; halaman=kampanye)
```

---

## 7. Landing page kampanye — `kampanye/index.html`

Halaman ini adalah rumah kampanye "Kopi yang jujur soal tanggal". Dibuat oleh `tools/kampanye.py`
dari `data/catalog.json` (harga asli) + `data/kreatif.json` (aset). Isinya:

| Bagian | Fungsi | Bukti yang dipakai |
| --- | --- | --- |
| Hero | janji utama: tanggal sangrai, bukan kedaluwarsa | 3 angka (3 hal tercetak · 7–21 hari · 15.00 WIB) |
| Galeri 5 klip | memperlihatkan proses, bukan mengklaimnya | `konten/reel-*.mp4` (poster = frame asli) |
| Tiga bukti | QC tolak batch · titik henti sangrai · cut-off kirim | `batch-qc.csv`, alur D1/D5 |
| Tiga pintu masuk | Peta Rasa · Ijen 100 g · Raung 250 g | harga dari katalog, bukan karangan |
| Jadwal tayang | janji transparan: ini rencana, bukan klaim | manifest `data/kreatif.json` |
| Penutup | "Kalau ragu, tanya dulu" | — |

Setiap tautan keluar membawa `utm` di pesan WhatsApp (dan `utm_source` pada tautan internal),
sehingga D3 bisa memisahkan chat dari landing vs dari feed.

**Jangan** mengubah halaman ini manual. Ubah katalog/manifest lalu jalankan ulang generator —
kalau tidak, harga di halaman akan berbeda dari harga yang dijawab D2 di chat.

---

## 8. Distribusi lintas platform (tanpa menambah beban)

| Kanal | Cara memakai aset yang sama | Yang diubah |
| --- | --- | --- |
| IG Reels | unggah `reel-*.mp4` apa adanya | caption + cover (poster) |
| TikTok | unggah `reel-*.mp4` | caption lebih pendek, tambah audio asli bila ada |
| IG Carousel | `carousel-*.jpg` berurutan | slide akhir = CTA |
| IG Story | `story-*.jpg` + stiker jajak pendapat | 1 pertanyaan saja |
| WhatsApp Status | `carousel-04a` / foto batch | tambah 1 kalimat "batch hari ini: [tgl]" |
| Marketplace | `post-01` sebagai foto utama | judul & poin (lihat `08-konten-siap-pakai.md`) |
| Landing | 5 `reel-*` dalam galeri | — |

Satu aset → 3–5 kanal. Kalau satu aset hanya dipakai di satu kanal, aset itu belum selesai.

---

## 9. Ukur: tiga angka yang menentukan

| Angka | Cara ambil | Target Nov | Keputusan yang dipicu |
| --- | --- | --- | --- |
| Simpan per post (Bukti/Edukasi) | insight IG mingguan | ≥ 10 | di bawah 5 → ganti hook, bukan ganti aset |
| Chat yang menyebut konten | tanya "lihat di mana?" saat balas | 40/bulan | < 20 → CTA atau kanal salah |
| Biaya per chat (bila berbayar) | total biaya iklan ÷ chat | ≤ Rp25.000 | di atas → hentikan kanal, bukan tambah budget |

Tayangan **bukan** target. Tayangan tinggi tanpa simpan & tanpa chat = konten hiasan.
Catat ketiga angka di `data/kpi.csv` setiap Jumat; papan akan membandingkannya dengan target D3.

---

## 10. Ritme produksi konten (agar tidak menumpuk)

| Kapan | Aktivitas | Keluaran |
| --- | --- | --- |
| Senin 5 menit | baca `studio/brief-senin.md`, ambil 1 keputusan (dobel/hentikan/uji) | keputusan minggu |
| Saat produksi (Senin) | rekam 8–10 klip 30–60 detik, tanpa bicara | klip mentah |
| Sabtu 20 menit | `tools/kreatif.py` + pilih 5 klip terbaik | aset + manifest |
| Selasa 90 menit | tulis caption, jadwalkan 7 aset | CSV terisi |
| Setiap hari 10 menit | tayangkan yang terjadwal / ambil aset siap | status `terbit` |
| Jumat 20 menit | ukur 3 angka, tulis 1 ulang + 1 hentikan | baris KPI |

**Aturan stok:** selalu sisakan minimal **5 aset siap** yang belum tayang. Kalau stok < 5,
minggu itu prioritasnya merekam, bukan menjadwalkan.

---

## 11. Studio 10 tahap — dari angka ke skrip

Kerangka "full social media team" (10 folder, 50 agent) dijalankan `tools/studio.py` sebagai
**fungsi deterministik**: 46 slot otomatis, 2 manual, 2 sengaja tidak dipakai. Alasannya biaya —
50 agent LLM berarti 50 kali token untuk pekerjaan yang sebagian besar berupa median, lift, dan
pengecekan kata terlarang. Hitungan seperti itu lebih murah, lebih cepat, dan bisa diperiksa ulang.

| Tahap | Untuk D3 | Untuk D4 |
| ---: | --- | --- |
| 01 niche | pagar positioning & kata terlarang | bahasa yang boleh dipakai |
| 02 pesaing | siapa yang dipantau, catatan industri | rencana video jawaban |
| 03 outlier | pola yang naik, dead views | acuan struktur, bukan footage |
| 04 kreator | watchlist ≥2 outlier | referensi gaya, bukan tiruan |
| 05 hook | pilih film pertama | hook + aset siap |
| 06 format | format prioritas per platform | gaya rekam & shot list |
| 07 skrip | cek suara, CTA, sumber klaim | 5 skrip 9 detik siap rekam |
| 08 skala | pola yang disimpan | 3 remix per pemenang |
| 09 lapor | dobel / hentikan / uji | antrean rekam |
| 10 ops | jadwal mingguan | cek pemakaian ulang |

Batasnya jelas: studio **merencanakan**, tidak menayangkan. Semua keputusan dari baris `contoh`
masih berlabel contoh sampai `data/riset-referensi.csv` diisi baris `asli`.
