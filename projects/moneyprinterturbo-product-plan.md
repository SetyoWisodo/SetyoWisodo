<div align="center">

# 🚀 Product Plan: **VideoKilat** *(working name)*

### 🤖 AI Short-Video Automation berbasis [MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo)

**Dari topik → naskah → suara → footage → subtitle → video siap posting — dalam hitungan menit.**

<sub>Disusun oleh: Setyo Wisodo — AI Development • Product Management • Growth Marketing · Banyuwangi, Jawa Timur 🇮🇩</sub>

</div>

---

## 🧭 TL;DR (English)

- **What:** A managed + self-serve AI short-video product for the Indonesian market, powered by the open-source **MoneyPrinterTurbo** engine (MIT license — free to build on and sell).
- **Why now:** Short-form video is the #1 growth channel; Indonesia is TikTok's largest market (~108–157M users, 2026 estimates), yet daily video production is a bottleneck for creators, UMKM, and agencies. MoneyPrinterTurbo (~120K GitHub stars) proves global demand for the automation — but it remains a developer's DIY tool, not a product.
- **The wedge:** Service-first (done-for-you) → productize learnings into a self-serve SaaS with **Bahasa Indonesia quality, local billing (QRIS/Midtrans), WhatsApp-native support, and vertical templates** (UMKM kuliner, affiliate, edukasi, properti).
- **Pricing (indicative):** Free / Pro ±Rp149rb ($9) / Business ±Rp499rb ($29) / Agency+API Rp1,5jt+ ($99+); done-for-you packages Rp3,5–25jt/month. Undercuts InVideo (~$17–20+/mo) and OpusClip ($15–29/mo) with localized value.
- **Unit economics:** Stock-based video COGS ≈ **$0.05–0.20**; AI-footage video ≈ **$0.50–2.00**. Gross margin 70–90% on SaaS tiers is realistic.
- **Moat:** Localization depth, vertical templates & brand kits, human-in-the-loop QA, publish-and-measure loop, and a data flywheel on what actually gets posted — not the base generation code (which is open to everyone).
- **90-day goal:** 3–5 paying done-for-you clients + 2–3 dogfooding proof channels + a soft-launched SaaS MVP with billing.

---

## 📌 Daftar Isi

1. [🎯 Ringkasan Eksekutif](#-ringkasan-eksekutif-executive-summary)
2. [💡 Peluang & Masalah](#-peluang--masalah-opportunity--problem)
3. [⚙️ Mesin Produk: MoneyPrinterTurbo](#-mesin-produk-moneyprinterturbo-the-engine)
4. [🧭 Visi, Positioning & Strategi Produk](#-visi-positioning--strategi-produk-product-strategy)
5. [👥 Target Pelanggan (ICP)](#-target-pelanggan-icp)
6. [🗺️ Roadmap Produk](#-roadmap-produk)
7. [📣 Go-To-Market (GTM)](#-go-to-market-gtm)
8. [💰 Monetisasi & Harga](#-monetisasi--harga-pricing)
9. [📊 Unit Economics](#-unit-economics)
10. [🥊 Lanskap Kompetitif & Moat](#-lanskap-kompetitif--moat)
11. [⚠️ Risiko & Mitigasi](#-risiko--mitigasi)
12. [📈 KPI & OKR](#-kpi--okr)
13. [🚦 Rencana 90 Hari](#-rencana-90-hari)
14. [📎 Lampiran: Sumber & Catatan Teknis](#-lampiran-sumber--catatan-teknis)

---

## 🎯 Ringkasan Eksekutif (Executive Summary)

**Peluang.** Permintaan konten video pendek meledak secara global dan di Indonesia — pasar TikTok terbesar di dunia dengan perkiraan **108–157 juta pengguna** dan rata-rata pemakaian **±72 menit/hari** ([TikTok Statistics 2026](https://houseofmarketers.com/tiktok-users-statistics-demographic-data/), [TikTok Marketing Statistics Indonesia 2026](https://data.stateglobe.com/indonesia/tiktok-marketing-statistics), [Countries with the Most TikTok Users 2026](https://businesstats.com/countries-with-the-most-tiktok-users/)). Di sisi lain, produksi video harian (naskah, voice-over, footage, subtitle, editing, posting) masih menyita waktu berjam-jam — dan mahal jika dikerjakan editor.

**Mesin.** [MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo) (MPT) adalah open-source **MIT-licensed** yang mengotomatiskan seluruh pipeline tersebut: topik → naskah (LLM) → suara (TTS) → footage (stok / AI) → subtitle → musik → video final → auto-publish ke TikTok, Instagram, dan YouTube Shorts. Popularitasnya (**±120.000 GitHub stars, ±18.000 forks** per September 2026) membuktikan kebutuhan pasar yang masif ([Wavect MPT Review 2026](https://wavect.io/blog/moneyprinterturbo-review-2026/)). Lisensi MIT memungkinkan kita membangun produk komersial di atasnya secara legal, termasuk menjual layanan dan memodifikasi kode.

**Strategi.** Jangan langsung jual "SaaS ke semua orang". Mulai dari **layanan done-for-you (DFY)** untuk segmen ber-urgensi tinggi (kreator affiliate TikTok Shop, UMKM, agensi kecil) — ini memberi *cash flow*, data nyata, dan *case study*. Pelajaran dari layanan dijadikan bahan bakar untuk **SaaS self-serve** berbahasa Indonesia, lalu **API/workflow** untuk agensi & MCN.

**Model bisnis.** Tiga lapis: (A) DFY packages Rp3,5–25jt/bulan, (B) SaaS freemium Rp0–499rb/bulan, (C) Agency/API Rp1,5jt+/bulan. COGS per video sangat rendah (lihat [Unit Economics](#-unit-economics)) karena komponen inti gratis (Edge TTS, footage Pexels/Pixabay, Whisper lokal) — margin kotor SaaS 70–90% realistis.

**Kunci menang.** Bukan kode generasi videonya (itu terbuka untuk semua), melainkan **kedalaman lokalisasi** (kualitas naskah & suara Bahasa Indonesia, template vertikal, budaya konten lokal), **alur kerja yang mulus** (brand kit → batch → review → publish → laporan), dan **distribution advantage** di komunitas kreator/UMKM Indonesia.

---

## 💡 Peluang & Masalah (Opportunity & Problem)

### Masalah yang kita pecahkan

| Pihak | Masalah hari ini | Biaya masalah |
|---|---|---|
| **Kreator & affiliate** (TikTok Shop, Shopee Video) | Butuh 1–5 video/hari untuk menjaga algoritma & komisi; produksi manual 1–3 jam/video | Kehilangan konsistensi = kehilangan *reach* & komisi |
| **UMKM** (±65 juta usaha, data yang umum dikutip Kemenkop UKM) | Tidak mampu bayar editor/agency (Rp3–10jt/video); pemilik mengerjakan sendiri | Kehadiran digital lemah vs kompetitor yang sudah video-first |
| **Agensi & freelancer kreatif** | Margin habis untuk editing berulang; skala terbatas orang | Tidak bisa menerima lebih banyak klien |
| **Media/publisher & brand** | Butuh volume konten multi-akun, multi-bahasa, on-brand setiap hari | Biaya tim produksi besar & lambat |

### Kenapa sekarang (Why Now)

1. **Video pendek adalah kanal pertumbuhan #1** — TikTok, Reels, dan Shorts mendominasi *attention*; Indonesia adalah pasar TikTok #1 dunia ([businesstats.com](https://businesstats.com/countries-with-the-most-tiktok-users/)). Belanja iklan TikTok di Indonesia diperkirakan **±USD 600 juta** dan pasar influencer **±Rp2,8 triliun** di 2026 ([data.stateglobe.com](https://data.stateglobe.com/indonesia/tiktok-marketing-statistics)).
2. **AI sudah cukup matang untuk pipeline ini** — LLM menulis naskah, TTS gratis (Edge TTS) bersuara natural, Whisper men-*generate* subtitle, MoviePy/FFmpeg merakit video. Yang tersisa adalah *productization*.
3. **Validasi demand dari open-source** — MPT mencapai ±120K bintang & ±18K fork ([Wavect](https://wavect.io/blog/moneyprinterturbo-review-2026/)), bahkan pernah #1 GitHub Trending dengan +1.742 bintang dalam sehari ([aifruit.app](https://aifruit.app/blog/moneyprinterturbo-alternative)). Artinya: jutaan orang *mencoba* alat ini — dan banyak yang gagal pada tahap setup API keys, konfigurasi, dan *hardening* produksi ([Wavect](https://wavect.io/blog/moneyprinterturbo-review-2026/)). **Di sinilah celah produk kami:** hasil instan, tanpa setup, terlokalisasi.
4. **Gap kompetitor di Indonesia** — pemain global (InVideo, OpusClip, Pictory) mahal dalam USD, minim lokalisasi Bahasa Indonesia (suara, gaya naskah, template UMKM), dan tidak mendukung pembayaran lokal.

### Ukuran pasar (indicative, bottom-up)

- **SAM Indonesia (jangka pendek):** ±500K–1M kreator aktif + puluhan ribu UMKM/agensi yang sudah beriklan di TikTok/Meta. Pada harga rata-rata blended Rp200rb/bulan → pasar terlayani **Rp1,2–2,4 triliun/tahun** skala konservatif.
- **Ekspansi:** pasar SEA serupa (Filipina, Vietnam, Thailand) + pasar global berbahasa Inggris via lapisan API/white-label.

---

## ⚙️ Mesin Produk: MoneyPrinterTurbo (The Engine)

### Apa yang sudah diberikan MPT secara gratis (MIT)

| Tahap pipeline | Kemampuan MPT | Biaya untuk kita |
|---|---|---|
| 📝 **Naskah (Script)** | Generate/rewrite naskah multi-bahasa via GPT, Claude, Gemini, DeepSeek, Kimi, Qwen, Ollama, dll. | ±$0.01–0.05/video (LLM API) |
| 🎙️ **Suara (Voice)** | **Edge TTS gratis** (suara `id-ID` tersedia), Azure, ElevenLabs, MiniMax, Gemini TTS, dll. | $0 (Edge TTS) → +$0.1–0.3 (premium) |
| 🎞️ **Footage** | Stok gratis **Pexels / Pixabay / Coverr**, unggah lokal, atau AI video (Seedance, MiniMax H3, WaveSpeed, dll.) | $0 (stok) → +$0.1–1.0 (AI footage) |
| 💬 **Subtitle** | Timing otomatis (faster-whisper lokal), styling font/posisi/warna | $0 (komputasi lokal) |
| 🎵 **Musik latar** | BGM random/lokal/AI + kontrol volume | $0 |
| 🎬 **Komposisi** | MoviePy/FFmpeg; output 9:16 (1080×1920), 16:9, 1:1; batch multi-varian | Komputasi render |
| 🚀 **Publish** | Auto-upload ke **TikTok, Instagram, YouTube Shorts** | $0 |
| 🖥️ **Antarmuka** | WebUI (Streamlit), **REST API** (FastAPI), CLI, dan workflow AI-Agent | — |

> ⚠️ Realitas biaya: *"Gratis kode, tidak gratis operasional"* — tetap ada biaya LLM/TTS/media API, komputasi, storage, review, dan operasi ([Wavect Review 2026](https://wavect.io/blog/moneyprinterturbo-review-2026/)). Ini justru kabar baik bagi model bisnis kami: nilai yang kita jual adalah **hasil + orkestrasi + lokalisasi**, bukan akses kode.

### Celah yang harus kita tutup (productization gaps)

1. **Multi-tenant, akun, billing** — MPT adalah *single-user tool*; kita perlu auth, kuota, payment gateway lokal (Midtrans/Xendit/QRIS).
2. **Lokalisasi mendalam** — template naskah & *tone* Bahasa Indonesia (formal/kasual/daerah), voice `id-ID` terbaik, referensi budaya lokal, template vertikal (kuliner, hijab, properti, edukasi).
3. **Brand kit & konsistensi** — logo, warna, font, CTA per klien; watermark opsional.
4. **Human-in-the-loop QA** — review cepat sebelum publish (cegah "AI slop", halusinasi naskah, footage yang tidak nyambung).
5. **Analytics loop** — performa posting (views, engagement) → rekomendasi topik berikutnya (*flywheel* data).
6. **Reliability** — *job queue*, retry, *error handling*, monitoring untuk produksi batch (MPT sudah punya task/batch; kita perkuat untuk SLA komersial).

**Catatan hukum & kontribusi:** Lisensi **MIT** mengizinkan penggunaan komersial, modifikasi, dan redistribusi dengan tetap mencantumkan *copyright notice* ([LICENSE](https://github.com/harry0703/MoneyPrinterTurbo/blob/main/LICENSE), [Wavect](https://wavect.io/blog/moneyprinterturbo-review-2026/)). Strategi kami: **kontribusi upstream** untuk perbaikan umum (membangun reputasi & mengurangi beban *fork*), simpan *patch* privat hanya untuk diferensiasi komersial.

---

## 🧭 Visi, Positioning & Strategi Produk (Product Strategy)

### Visi produk

> **"Setiap UMKM & kreator Indonesia bisa punya tim video AI sendiri."**
> Membuat produksi video pendek semudah menulis status — dari topik jadi video siap posting, dalam bahasa dan gaya Indonesia.

### Positioning statement

> **Untuk** kreator, UMKM, dan agensi di Indonesia yang butuh video pendek konsisten setiap hari,
> **VideoKilat** adalah layanan & platform AI yang **mengubah satu topik menjadi video siap posting** (naskah, suara Indonesia, footage, subtitle, musik) dan langsung mempublikasikannya —
> **berbeda dari** InVideo/Pictory/OpusClip yang mahal dan kurang lokal, maupun MPT mentah yang butuh keahlian teknis,
> **karena** kami menggabungkan engine open-source terbaik dengan lokalisasi mendalam, template vertikal, QA manusia, dan dukungan WhatsApp.

### Strategi tiga lapis (Service → SaaS → API)

| Lapis | Produk | Untuk siapa | Fungsi strategis |
|---|---|---|---|
| **A. Done-for-You (DFY)** | Tim kami memproduksi & memposting video klien (paket bulanan) | UMKM, brand, affiliate serius | 💵 *Cash flow* sejak hari pertama, validasi PMF, studi kasus |
| **B. SaaS self-serve** | Web app: topik → video → publish; freemium | Kreator individual, tim kecil | 📈 *Scale* & *margin*; basis data perilaku |
| **C. API & Automation** | REST API + n8n/Make/Zapier + white-label | Agensi, MCN, developer | 🔒 *Lock-in* & kontrak bernilai tinggi |

**Prinsip keputusan:** fitur yang tidak melayani minimal dua lapis tidak masuk roadmap 12 bulan pertama.

### Opsi yang dipertimbangkan

| Opsi | Kelebihan | Kekurangan | Keputusan |
|---|---|---|---|
| 1. Agensi DFY murni | Cepat, margin bagus | Tidak scalable, *founder-dependent* | ✅ Fase 1 saja (jembatan) |
| 2. SaaS langsung (pure self-serve) | Skala besar | Butuh modal & *brand*; churn tinggi tanpa onboarding | ⏳ Fase 2 |
| 3. Open-core + hosting | Cinta komunitas dev | Monetisasi lambat | 🔧 Sebagai kanal akuisisi (GitHub), bukan model utama |
| 4. Vertikal penuh (mis. agen video properti) | Nilai per akun tinggi | Pasar lebih kecil dulu | 🎯 Masuk sebagai *template & paket*, bukan produk terpisah |

---

## 👥 Target Pelanggan (ICP)

### Peta segmen (fokus: Indonesia dahulu)

| Segmen | Profil & pain | Pekerjaan yang harus dikerjakan (JTBD) | Kesiapan bayar | Channel utama | Prioritas |
|---|---|---|---|---|---|
| 🛍️ **Kreator & affiliate TikTok Shop** | Butuh 1–5 video/hari; komisi bergantung konsistensi | "Buat video produk yang *nggak* kelihatan iklan banget, tiap hari" | Tinggi (langsung ada ROI komisi) | Komunitas seller, KOL, TikTok Ads | **P1** |
| 🏪 **UMKM naik kelas** (kuliner, fashion, jasa) | Tidak punya tim konten; takut ribet | "Tampil profesional di TikTok/IG tanpa hire editor" | Sedang (harga sensitif) | Workshop Pemda/HIPMI/kampus, FB Groups, WhatsApp | **P1** |
| 🎨 **Agensi & freelancer kreatif** | Editing berulang menghabiskan margin | "Perbanyak output tanpa tambah editor" | Tinggi (nilai per klien besar) | LinkedIn, komunitas agensi, event | **P2** |
| 📰 **Media/publisher niche** | Volume konten multi-akun harian | "Produksi massal terkontrol & on-brand" | Tinggi (kontrak) | Direct sales | **P2** |
| 🌏 **Global creators / dev** | MPT terlalu teknis; mereka butuh hasil instan | "Ship shorts daily without ops" | Tinggi (USD) | Product Hunt, SEO, YouTube | **P3** (setelah PMF lokal) |

### Ideal Customer Profile #1 (beachhead)

> **Rani, 29 tahun** — kreator affiliate TikTok Shop di Surabaya. Punya 3 akun, jualan skincare & hijab. Butuh 2–3 video/hari per akun. Saat ini menghabiskan malam hari mengedit di CapCut sampai jam 1 pagi, sering bolong posting. **Bersedia bayar Rp150–500rb/bulan** untuk "tim video" yang hasilnya tinggal review & post — asal suara Indonesia-nya natural dan footage-nya *nyambung*.

---

## 🗺️ Roadmap Produk

### Fase 0 — Fondasi (Bulan 0–1)
- Fork & deploy MPT (Docker), hardening produksi (queue, storage, monitoring).
- Riset kualitas: benchmark suara `id-ID` (Edge TTS vs ElevenLabs vs MiniMax), kualitas naskah per provider LLM, relevansi footage Pexels untuk topik Indonesia.
- Tetapkan 3 **template vertikal** pertama: *Kuliner/UMKM*, *Affiliate Produk*, *Edukasi/Tips*.
- Standar QA: checklist review 60 detik sebelum publish.

### Fase 1 — DFY Service (Bulan 1–3) ✅ *cash flow + learning*
- Paket jasa bulanan (20/60/120 video), proses onboarding (brief, brand kit, akses akun).
- 3–5 klien pilot dari jaringan personal; kumpulkan *case study* (views, waktu hemat, komisi).
- Internal ops toolkit: *dashboard order*, template library, SOP produksi.

### Fase 2 — SaaS MVP (Bulan 3–6) 📈 *productization*
- Web app multi-tenant: signup → pilih template → topik → preview → render → auto-publish.
- Billing lokal (Midtrans/Xendit, QRIS, VA) + kartu internasional (Stripe/Paddle untuk pasar global).
- Freemium (kuota + watermark), brand kit, riwayat task, impor/ekspor pengaturan.
- Analytics dasar: video terbit/minggu, performa ringan.

### Fase 3 — Scale & API (Bulan 6–12) 🔒 *moat & expansion*
- REST API + integrasi n8n/Make; akses white-label untuk agensi.
- Analytics loop: performa konten → rekomendasi topik & jam posting (*data flywheel*).
- Multi-bahasa (EN) untuk pasar global; kolaborasi tim (seat, role).
- Eksperimen AI footage (Seedance/MiniMax) sebagai *upsell* "Premium Visual".

---

## 📣 Go-To-Market (GTM)

### Prinsip utama: **"Use the product to market the product" (dogfooding)**

Engine yang sama yang kita jual dipakai untuk menjalankan **3–5 kanal bukti (proof channels)** faceless di topik Indonesia (fakta unik, tips UMKM, edukasi karier, quotes). Fungsi ganda:
1. Bukti langsung bahwa mesin menghasilkan konten yang layak tayang (portofolio hidup).
2. Kanal akuisisi organik murah → trafik ke landing page.
3. Laboratorium untuk meningkatkan kualitas pipeline & template.

### Strategi per fase

| Fase | Kanal | Taktik | Target |
|---|---|---|---|
| **1. Launch lembut** | Jaringan personal, WhatsApp/Telegram, komunitas FB seller & UMKM | Tawaran pilot berdiskon untuk 5 klien pertama (syarat: testimonial & studi kasus) | 5 klien DFY, 2 studi kasus |
| | Proof channels TikTok/IG/YT Shorts | 2–3 posting/hari per kanal, CTA ke bio link | 1.000+ followers/kanal, 50+ leads |
| **2. Launch publik** | **Product Hunt** + GitHub (README profesional, demo video) | "Open-core AI video factory for Indonesian creators" | Awareness global + backlink SEO |
| | Komunitas & KOL | Program afiliasi 20–30% recurring; webinar "Trik konten UMKM naik omzet" | 500+ signup, 50+ pembayar |
| | SEO & Content marketing | Kata kunci: "cara buat video otomatis", "tools video AI", "cara jualan di TikTok" | 100+ artikel/halaman dalam 6 bulan |
| | TikTok/Meta Ads (performance) | Iklan demo "before/after" proses produksi; retargeting | CAC < Rp300rb untuk tier Pro |
| **3. Scale** | Kemitraan | MCN, agensi kreatif, TikTok Shop Partner, program digitalisasi UMKM (kampus/Pemda) | 3–5 kemitraan aktif |
| | Event & komunitas offline | Workshop di Jawa Timur (Banyuwangi–Surabaya) → kredibilitas lokal | Pipeline B2B |

### Strategi konten pemasaran (contoh pilar)

1. **Demo proses** — screen recording "topik → video jadi dalam 3 menit" (konversi terbaik untuk produk visual).
2. **Bukti sosial** — laporan jujur performa proof channels ("1 juta views dari video AI" + transparansi label AI).
3. **Edukasi UMKM** — tips jualan video-first; soft-sell.
4. **Perbandingan** — "CapCut manual vs VideoKilat otomatis", "harga editor vs harga langganan".

---

## 💰 Monetisasi & Harga (Pricing)

### Harga indikatif (validasi di riset pelanggan Fase 1)

| Paket | Harga (IDR/bln) | ≈ USD | Isi | Sasaran |
|---|---|---|---|---|
| **Free** | Rp0 | $0 | 5 video/bln, watermark, 720p, tanpa auto-publish | Akuisisi & trial |
| **Pro** | Rp149.000 | ±$9 | 60 video/bln, 1080p, tanpa watermark, 3 brand kit, auto-publish 3 akun | Kreator individual |
| **Business** | Rp499.000 | ±$29 | 250 video/bln, 3 seat, brand kit unlimited, prioritas render, analytics | Tim & UMKM serius |
| **Agency / API** | mulai Rp1.500.000 | ±$99 | Kuota volume, REST API, white-label, SLA & support prioritas | Agensi, MCN, developer |

### Layanan Done-for-You (Fase 1 — mesin kas)

| Paket | Harga | Isi |
|---|---|---|
| **Starter** | Rp3.500.000/bln | 20 video, 1 akun, revisi 1×, laporan bulanan |
| **Growth** | Rp8.500.000/bln | 60 video, 3 akun, revisi 2×, riset konten, laporan mingguan |
| **Scale** | mulai Rp25.000.000/bln | 120+ video, multi-akun, strategi konten, tim khusus |

### Anchor harga kompetitor (2026)

- **OpusClip:** Free (berwatermark) / Starter **$15/bln** / Pro **$29/bln** (±$14,5 saat tahunan) / Business custom ([checkthat.ai](https://checkthat.ai/brands/opusclip/pricing), [costbench.com](https://costbench.com/software/ai-video-editing-saas/opus-clip/)).
- **InVideo AI:** mulai **±$17–20/bln** hingga tier tinggi ±$900/bln ([costbench.com](https://costbench.com/software/ai-video-editing-saas/opus-clip/)).
- **Keunggulan kami:** harga lokal (IDR, QRIS/VA — tanpa gesekan kartu USD), nilai lebih tinggi per rupiah (kuota video lebih besar), lokalisasi & support WhatsApp.

### Aturan monetisasi

1. **Freemium sebagai corong**, bukan biaya: batasi *kuota & watermark*, bukan kualitas suara/naskah (agar "aha moment" tetap kuat).
2. **AI footage sebagai upsell** (biaya COGS naik signifikan) — "Standard" vs "Premium Visual".
3. **Kontrak DFY minimal 3 bulan** untuk arus kas yang sehat.
4. **Pertahankan margin:** jika COGS > 25% harga paket, negosiasi ulang harga provider atau alihkan ke jalur stok/Edge TTS.

---

## 📊 Unit Economics

### Estimasi COGS per video (60 detik, 1080p)

| Komponen | Jalur Stok (utama) | Jalur AI Footage (premium) |
|---|---|---|
| LLM (naskah + keyword) | $0.01–0.05 | $0.01–0.05 |
| TTS (Edge TTS `id-ID`) | $0.00 | $0.00 |
| TTS premium (opsional, ElevenLabs dkk.) | — | +$0.10–0.30 |
| Footage (Pexels/Pixabay) | $0.00 | — |
| Footage AI (Seedance/MiniMax dkk.) | — | +$0.10–1.00 |
| Subtitle (faster-whisper lokal) | ±$0.00 (komputasi) | ±$0.00 |
| Render (FFmpeg/MoviePy, 2–5 menit CPU) | $0.01–0.03 | $0.01–0.03 |
| Storage + delivery | <$0.01 | <$0.01 |
| **Total COGS / video** | **±$0.05–0.20** (±Rp800–3.300) | **±$0.50–2.00** (±Rp8.000–33.000) |

> Estimasi berdasarkan komponen gratis/berbayar yang didukung MPT dan harga API umum 2026; **wajib divalidasi** dengan produksi nyata di Fase 0–1 (angka aktual bisa berbeda per provider & resolusi).

### Contoh ekonomi SaaS (skenario 100 pelanggan berbayar)

| Metrik | Skenario konservatif |
|---|---|
| Komposisi | 70 Pro (Rp149rb) + 25 Business (Rp499rb) + 5 Agency (Rp1,5jt) |
| **MRR** | ±Rp37,5 juta (±$2.300) |
| Rata-rata pemakaian | 25 video/bln × 100 akun = 2.500 video |
| COGS total (jalur stok, ±$0.12/video) | ±Rp5 juta (±$300) |
| **Margin kotor** | **±87%** (sebelum gaji & infrastruktur) |
| Break-even kas | ±20–30 pelanggan Pro-Business (dengan founder sebagai tenaga utama) |

### Contoh ekonomi DFY (paket Growth Rp8,5jt)

| Metrik | Nilai |
|---|---|
| 60 video × COGS ±$0.15 | ±$9 (±Rp150rb) — *nyaris nol vs harga* |
| Waktu operasi (review + koordinasi) | ±6–10 jam/bulan |
| **Margin kotor layanan** | **±75–85%** setelah waktu kerja |

---

## 🥊 Lanskap Kompetitif & Moat

### Peta persaingan

| Solusi | Kelebihan mereka | Kelemahan vs kami | Harga |
|---|---|---|---|
| **CapCut** (manual) | Gratis, familiar, template banyak | Masih manual; tidak ada pipeline topik→video→post | Gratis / Pro kecil |
| **InVideo AI** | Merek kuat, fitur lengkap | Harga USD, lokalisasi ID terbatas, tidak ada model DFY lokal | ±$17–20+/bln ([costbench](https://costbench.com/software/ai-video-editing-saas/opus-clip/)) |
| **Opus Clip** | *Clipping* video panjang→pendek terbaik | Fokus repurpose, bukan generasi dari topik; *credit shock* dikeluhkan agensi ([checkthat.ai](https://checkthat.ai/brands/opusclip/pricing)) | $15–29/bln |
| **Pictory / Veed / Zebracat** | Fitur beragam | Mahal, generik untuk pasar ID | $12–50+/bln |
| **MPT mentah (DIY)** | Gratis, fleksibel, paling murah | Butuh keahlian teknis; setup API keys & operasi sulit bagi non-teknis ([aifruit](https://aifruit.app/blog/moneyprinterturbo-alternative), [Wavect](https://wavect.io/blog/moneyprinterturbo-review-2026/)) | Biaya API saja |
| **Editor manusia** | Kreativitas & nuansa | Mahal (Rp500rb–3jt/video), lambat, sulit skala | Per video/proyek |

### Moat kami (urut kekuatan)

1. 🇮🇩 **Kedalaman lokalisasi** — naskah & suara `id-ID` yang natural, gaya bahasa per segmen (kasual TikTok, formal B2B), template vertikal Indonesia. Ini paling sulit ditiru pemain global.
2. 🔄 **Data flywheel** — ratusan ribu siklus *topik → video → performa posting* menghasilkan rekomendasi konten yang makin tajam (model ML sederhana pun cukup di awal).
3. 🧩 **Workflow terintegrasi + QA manusia** — brand kit, batch, review, publish, laporan — pengalaman "tinggal pakai", bukan "alat generasi".
4. 🤝 **Distribusi & komunitas lokal** — komunitas UMKM/kreator, kemitraan, kepercayaan lewat studi kasus nyata, support bahasa lokal.
5. ⚡ **Struktur biaya** — engine open-source + komponen gratis (Edge TTS, stok) memungkinkan harga yang tidak bisa diikuti SaaS berlisensi berat — asal dijaga disiplin COGS.
6. 🧱 **Kontribusi & relasi upstream** — kontribusi ke MPT memberi *early access* fitur & reputasi; versi di-*pin* + lapisan hardening milik kami.

> 🚫 **Bukan moat:** kode generasi video itu sendiri (MIT, terbuka untuk semua), penggunaan satu LLM/TTS provider saja, atau harga murah tanpa diferensiasi (mudah diperang harga).

---

## ⚠️ Risiko & Mitigasi

| Risiko | Dampak | Mitigasi |
|---|---|---|
| **Kebijakan label konten AI** platform (YouTube/TikTok mewajibkan penandaan; perdebatan kebijakan sedang berlangsung — [aifruit](https://aifruit.app/blog/moneyprinterturbo-alternative)) | Video diturunkan / akun kena penalti | Patuhi & bantu klien *declare* konten AI; jaga kualitas di atas ambang "AI slop"; edukasi praktik terbaik |
| **Kualitas "AI slop"** (footage tidak nyambung, naskah datar) | Churn tinggi, reputasi buruk | Human-in-the-loop QA, template ketat per vertikal, kurasi footage, opsent "Premium Visual" |
| **Perubahan upstream MPT** (fitur/struktur) | Biaya integrasi berulang | *Pin* versi, kontribusi upstream, lapisan abstraksi antara engine & produk |
| **Ketergantungan API** (LLM/TTS naik harga / limit) | COGS naik, layanan terganggu | Multi-provider (MPT sudah dukung banyak), prioritas jalur murah (Edge TTS, DeepSeek/Ollama), kontrak volume |
| **Hak cipta & suara** | Klaim legal | Gunakan stok berlisensi bebas (Pexels/Pixabay), musik berlisensi jelas; **jangan** clone suara tanpa izin tertulis |
| **Perang harga vs CapCut (gratis) & big tech** | Tekanan harga | Jual hasil & waktu (DFY, workflow, hasil terbukti), bukan "fitur edit" |
| **Pembayaran & adopsi lokal** | Konversi rendah | QRIS/VA/e-wallet via Midtrans/Xendit; coba-bayar mudah; WhatsApp sebagai kanal support & sales |
| **Satu orang (founder-dependent)** | Eksekusi lambat | SOP sejak Fase 1, otomasi ops, rekrut operator produksi saat MRR cukup |

---

## 📈 KPI & OKR

### North Star Metric

> **Jumlah video yang benar-benar terbit per tim aktif per minggu** (bukan sekadar "video digenerate" — nilai kami adalah *published output*).

### OKR Contoh — 2 Kuartal Pertama

| Objective | Key Results |
|---|---|
| **O1: Buktikan PMF lewat DFY** | KR1: 5 klien DFY aktif · KR2: 2 studi kasus dengan hasil terukur (contoh: +30% views/konsistensi posting) · KR3: NPS ≥ 40 |
| **O2: Luncurkan SaaS yang diadopsi** | KR1: 500 pendaftar · KR2: **Aktivasi ≥ 40%** (video pertama terbit < 15 menit setelah signup) · KR3: 25 pelanggan berbayar · KR4: Konversi free→paid ≥ 5% |
| **O3: Bangun mesin akuisisi murah** | KR1: 3 proof channels aktif (≥2 video/hari) · KR2: 100 leads/bulan dari organik · KR3: CAC blended < Rp300rb |
| **O4: Jaga kesehatan bisnis** | KR1: Margin kotor ≥ 70% · KR2: Retensi M1→M3 ≥ 60% · KR3: Churn bulanan < 8% |

### Funnel metrics yang dipantau mingguan

Aktivasi (waktu ke video pertama) → Publish rate (video dirender vs terbit) → Free→Paid → Retensi/Churn → Expansion (upgrade tier/kuota) → Referral/afiliasi.

---

## 🚦 Rencana 90 Hari

### Minggu 1–2 — Fondasi teknis & produk
- [ ] Fork MPT → deploy production (Docker/uv), pin versi, siapkan domain & server.
- [ ] Setup provider: LLM (DeepSeek/Kimi/GPT untuk benchmark), Edge TTS `id-ID`, Pexels/Pixabay.
- [ ] Uji kualitas 20 video contoh di 3 template vertikal; catat waktu & COGS aktual.
- [ ] Tulis SOP QA 60 detik + brand kit template.

### Minggu 3–4 — Tawaran DFY & pilot
- [ ] Rancang 1 halaman penawaran (harga, contoh hasil, garansi revisi).
- [ ] Pitch ke jaringan personal → target **3 klien pilot** (harga pengenalan, kontrak 3 bulan).
- [ ] Launch **2 proof channels** (topik: tips UMKM + fakta/edukasi) — posting konsisten harian.

### Minggu 5–8 — Validasi & mulai produk
- [ ] Kumpulkan testimoni & studi kasus pertama; dokumentasikan proses "topik→video terbit".
- [ ] Bangun wrapper: halaman web + auth + kuota + billing Midtrans/Xendit (paling sederhana yang bisa jalan).
- [ ] Daftar tunggu publik via proof channels & komunitas; ukur minat (konversi landing page).
- [ ] Uji harga dengan 10 calon pelanggan (wawancara singkat).

### Minggu 9–12 — Soft launch SaaS
- [ ] Buka beta terbatas (50 pengguna) dari daftar tunggu; pantau aktivasi & churn mingguan.
- [ ] Siapkan aset launch publik: demo video, halaman Product Hunt, README GitHub profesional.
- [ ] Program afiliasi (20–30% recurring) untuk KOL & komunitas.
- [ ] Review OKR kuartal: putuskan fokus Fase 2 (SaaS) vs perluas DFY berdasarkan data.

---

## 📎 Lampiran: Sumber & Catatan Teknis

### Sumber data

1. [MoneyPrinterTurbo — GitHub Repository](https://github.com/harry0703/MoneyPrinterTurbo) (fitur, lisensi MIT, dokumentasi resmi)
2. [Wavect — MoneyPrinterTurbo Review 2026](https://wavect.io/blog/moneyprinterturbo-review-2026/) — ±120K stars / ±18K forks (snapshot Sept 2026), realitas biaya produksi, lisensi MIT
3. [aifruit — MoneyPrinterTurbo Alternatives 2026](https://aifruit.app/blog/moneyprinterturbo-alternative) — momentum GitHub Trending (62K stars, Mei 2026), tantangan setup, isu kebijakan label AI
4. [pyshine — MoneyPrinterTurbo Overview](https://pyshine.com/MoneyPrinterTurbo-AI-Powered-Video-Generation/) — arsitektur pipeline (LLM → TTS → stok → MoviePy/FFmpeg)
5. [checkthat.ai — OpusClip Pricing 2026](https://checkthat.ai/brands/opusclip/pricing) & [costbench — OpusClip vs InVideo](https://costbench.com/software/ai-video-editing-saas/opus-clip/) — harga kompetitor
6. [houseofmarketers — TikTok Statistics 2026](https://houseofmarketers.com/tiktok-users-statistics-demographic-data/) — Indonesia ±108 juta pengguna TikTok
7. [data.stateglobe — TikTok Marketing Statistics Indonesia 2026](https://data.stateglobe.com/indonesia/tiktok-marketing-statistics) — ±150 juta pengguna aktif, 72 menit/hari, belanja iklan ±USD 600 juta, pasar influencer ±Rp2,8T
8. [businesstats — Countries with the Most TikTok Users 2026](https://businesstats.com/countries-with-the-most-tiktok-users/) — Indonesia peringkat #1 (±157 juta pengguna)

### Catatan teknis (untuk tim teknis)

- **Stack MPT:** Python 3.11+, MoviePy 2.x + FFmpeg, Streamlit (WebUI), FastAPI (API), faster-whisper (subtitle), edge-tts (TTS gratis), multi-provider LLM (OpenAI-compat, LiteLLM, Ollama).
- **Jalur deploy:** Docker Compose (ada varian GPU), `uv` untuk macOS/Linux, paket Windows satu-klik, Google Colab untuk demo.
- **Integrasi publish:** layanan `upload_post` (TikTok, Instagram, YouTube) — perlu konfigurasi API key per akun klien.
- **Prioritas hardening komersial:** job queue & retry, storage object (S3-compatible), isolasi multi-tenant, observability (logging/alert), rate limiting per paket.

---

<div align="center">

*"Kami tidak menjual generator video — kami menjual konsistensi konten yang sebelumnya hanya mungkin bagi brand besar."* 💸

</div>
