# Studio Anomali v2 — Nasional + Clipper Network
## Revisi dari `PROJECT_STUDIO_ANOMALI_UMKM_2026.md` (target Jatim → seluruh Indonesia)

> **Owner:** Setyo Wisodo — Banyuanyar, East Java
> **Status:** Spec v2 + prototype interaktif `skill-lab/src/AnomalyStudio.jsx` (`#studio-anomali`, data mock). Belum ada data live.
> **Perubahan utama:** (1) target UMKM seluruh Indonesia, bukan Jatim saja; (2) menambahkan model **clipper** sebagai mesin akuisisi dan sumber pendapatan kedua.

---

## 1. Ringkasan Perubahan

| Aspek | v1 (Jatim) | v2 (Nasional + Clipper) |
|-------|-----------|--------------------------|
| Target | UMKM Jatim, 5 pilot | UMKM seluruh Indonesia, diprioritaskan kota besar dengan ekosistem TikTok Shop dan pasar kuliner/fashion |
| Layanan | Retainer konten + ads (Starter/Growth/Scale) | Retainer tetap + **Clipper Network** (klip per views) + paket campaign per posting |
| Eksekusi | Tim kecil lokal | Remote-first: clipper bekerja dari mana saja, UMKM dilayani via WA dan video call |
| Pendapatan | Retainer + affiliate | Retainer + fee platform/marketplace + komisi affiliate + layanan kreatif untuk brand |

---

## 2. Kenapa Clipper Masuk Akal

**Clipper** = orang yang memotong video panjang (podcast, livestream, webinar, konten brand) jadi klip pendek lalu memposting ke akun sendiri dan dibayar per 1.000 views yang terverifikasi.

Alasan Studio Anomali sebaiknya memakai model ini:
1. **Mesin uji hook murah.** Satu video panjang bisa menghasilkan 10–30 klip dengan hook berbeda. Klip yang menang di clipper langsung dipakai ulang untuk UMKM. Ini memperkuat riset outlier yang sudah ada.
2. **Pasokan kreator tanpa followers.** Clipper tidak perlu followers. Ini cocok untuk merekrut ribuan orang di luar Jawa yang tidak punya akses ke agency.
3. **Pendapatan terukur.** Bayaran hanya untuk views yang sudah terverifikasi. Risiko bagi Studio kecil, karena biaya baru muncul saat hasil ada.
4. **Pelengkap, bukan pengganti.** Retainer UMKM tetap menjadi pendapatan utama yang stabil. Clipper adalah jalur tambahan dan jalur uji.

**Batasan yang harus diakui:**
- Tarif per 1.000 views rendah dan bergantung pada algoritma. Banyak klip tidak mencapai minimum pencairan.
- TikTok Creator Rewards **belum tersedia di Indonesia** per September 2026 (sumber: klipaja.id). Jalur TikTok dari Indonesia hanya LIVE Gifts, TikTok Shop, afiliasi, dan kolaborasi brand.
- Clipper dengan tarif tinggi bisa mencapai puluhan dolar per 1.000 views, tetapi itu kampanye langka. Jangan jadikan angka ini dasar proyeksi.

---

## 3. Data Tarif Clipper di Indonesia (sumber dicek 2026)

| Marketplace / Program | Tarif per 1.000 views | Potongan platform | Catatan |
|-----------------------|-----------------------|-------------------|---------|
| **Konten.com** (platform clipping lokal, berdiri 20 Mei 2026 menurut Republika) | Rp1.000 – Rp5.000 pada kartu campaign (12 Okt 2026). Satu campaign tercatat Rp7.500 | 20% dari kotor | Minimum 50.000 views untuk klaim, maksimum 1.000.000 views per video, validasi 7 hari. Khusus pengguna Indonesia |
| **Rentang pasar lokal** (JawaPos, detik, Sep 2026) | Rp2.000 – Rp7.000 | Tergantung campaign | Dilaporkan media sebagai rentang umum |
| **Whop Content Rewards** | Rata-rata ~$1, umumnya $1–5. Rate YouTube $1,25 | 10% | Budget dan cap per klip berbeda tiap campaign |
| **YouTube Shorts (Creator Pool)** | Bagi hasil 45% dari pool | — | Mulai 1 Feb 2027 syarat minimal 10 juta views Shorts dalam 90 hari. Sumber: klipdong, belum diverifikasi ke halaman resmi |
| **YouTube Partner Program** | Bagi hasil iklan | — | 1.000 subscriber + 10 juta views Shorts/90 hari, atau 1.000 subscriber + 4.000 jam tonton/12 bulan |
| **TikTok Creator Rewards** | — | — | **Tidak tersedia untuk Indonesia** |

**Simulasi (Rp5.000 per 1.000 views, potongan 20% Konten.com):**

| Views terverifikasi | Gross | Setelah potongan 20% |
|---------------------|-------|----------------------|
| 50.000 (batas minimum klaim) | Rp250.000 | Rp200.000 |
| 500.000 | Rp2.500.000 | Rp2.000.000 |
| 1.000.000 (batas maksimum per video) | Rp5.000.000 | Rp4.000.000 |

Catatan: angka ini dihitung dari tarif yang dilaporkan, bukan janji. Banyak klip tidak mencapai minimum. Rata-rata nyata untuk klipper pemula bisa jauh di bawah ini.

---

## 4. Model Bisnis Gabungan

### Lapis 1 — Retainer UMKM (pendapatan utama)
- Starter, Growth, Scale seperti v1, sekarang bisa dipesan dari seluruh Indonesia.
- Kontrak berbasis hasil tetap dipakai: 1 video minimal 3× median dalam 30 hari, atau dua video gratis.

### Lapis 2 — Clipper Network (mesin volume dan uji hook)
- Studio mengambil campaign dari brand, UMKM, atau kreator besar. Video panjang disediakan.
- Clipper memotong dan memposting dari akun yang sudah disetujui.
- Studio menjaga kualitas: approval klip, pengecekan hook, dan laporan views.
- Studio mengambil margin dari selisih tarif brand dengan tarif clipper.

**Contoh margin (asumsi, perlu dibuktikan):** brand membayar Rp7.000 per 1.000 views, clipper dibayar Rp4.000 per 1.000 views, Studio ambil Rp3.000 — ini hanya berlaku jika Studio menjual kampanye langsung ke brand, bukan hanya sebagai marketplace.

### Lapis 3 — Paket Campaign per Posting
- Brand membayar tarif tetap per kiriman atau retainer mingguan, bukan per views.
- Lebih stabil bagi clipper dan lebih mudah diprediksi bagi Studio.
- Sesuai dengan perubahan Content Rewards V2 di Whop (19 Agustus 2026) yang juga memakai tarif per posting dan retainer.

### Lapis 4 — Hasil Riset sebagai Produk
- Data outlier dan hook dari Lapis 1–2 dijual sebagai laporan niche bulanan (contoh: "Kuliner Nasional Oktober 2026").

---

## 5. Strategi Nasional — Urutan Kota

Tidak semua kota perlu sekaligus. Urutan yang disarankan berdasarkan ekosistem TikTok Shop dan jumlah UMKM:

| Fase | Wilayah | Alasan |
|------|---------|--------|
| 1 (bulan 1–2) | Jatim (Banyuanyar, Surabaya, Malang) | Basis lokal, bisa datang langsung ke UMKM |
| 2 (bulan 3–4) | Jabodetabek, Bandung, Yogyakarta | Konsentrasi kreator dan brand |
| 3 (bulan 5–6) | Medan, Makassar, Denpasar | Ekspansi kuliner dan wisata |
| 4 (bulan 7+) | Seluruh Indonesia, remote | Clipper bekerja online, layanan via WA |

**Catatan:** TikTok Shop, Shopee, dan Tokopedia dipakai sebagai kanal jualan. Pembayaran clipper hanya ke rekening atau e-wallet Indonesia (syarat Konten.com).

---

## 6. Peta Skill Repo untuk v2 (46 skill, sama seperti v1 + klipping)

| Fungsi baru | Skill | Peran |
|-------------|-------|-------|
| Pilih video sumber panjang | `outlier-post-finder`, `trend-discovery` | Cari video panjang dan hook yang sudah terbukti |
| Ambil hook dari transkrip | `transcript-intelligence` | Tandai momen klip dari transkrip |
| Ubah 1 video jadi banyak klip | `content-repurposing` | 8 atoms per sumber, sekarang per klip |
| Rekrut clipper | `influencer-prospecting`, `creator-profile-teardown` | Cari dan nilai calon clipper |
| Kontrol kualitas views | `ads-monitor`, `ads-report` | Lacak views dan performa tiap klip |
| Budget campaign | `ads-budget`, `ads-math` | Hitung margin per 1.000 views |

Sisa skill tetap dipakai seperti di v1.

---

## 7. Risiko Khusus Clipper

| Risiko | Mitigasi |
|--------|----------|
| Klip tidak mencapai minimum pencairan | Batasi jumlah klip per clipper, pilih campaign dengan minimum rendah |
| Clipper pindah ke platform lain | Kontrak eksklusif per campaign, pembayaran hanya setelah klip disetujui |
| Akun clipper dibatasi platform | Pilih akun aktif dan sesuai aturan platform, jangan pakai bot atau views palsu |
| Views dipalsukan | Verifikasi views langsung dari dashboard platform, bukan klaim clipper |
| Tarif marketplace berubah | Tetapkan tarif Studio sendiri dengan margin minimum |
| Ketergantungan pada satu marketplace | Gunakan lebih dari satu sumber campaign |

---

## 8. Roadmap 90 Hari (ringkas)

- **Bulan 1:** Pilot 5 UMKM Jatim (retainer Starter). Rekrut 20 clipper uji dari Jatim. Uji 3 campaign klip di Konten.com atau Whop.
- **Bulan 2:** Ukur CPM efektif per klip, margin per 1.000 views, dan rasio klip yang mencapai minimum. Tentukan tarif Studio sendiri.
- **Bulan 3:** Buka kampanye di Jabodetabek dan Bandung. Jual paket campaign per posting ke 2 brand.

**Target awal yang harus dibuktikan (bukan janji):**
- Minimal 30% klip mencapai minimum pencairan.
- Margin per 1.000 views minimal Rp1.500 setelah potongan platform.
- Minimal 1 campaign dengan rasio hook 3× median.

---

## 9. Yang Perlu Dicek Sebelum Pitch

- Angka CPM TikTok Indonesia: sumber berbeda memberi angka sangat berbeda (klipaja.id menyebut $0,005–0,01 per 1.000 views, sedangkan riset induk memakai CPM sekitar $4). Verifikasi dengan data akun sendiri.
- Jumlah klien UMKM nasional dan harga Starter/Growth/Scale: masih asumsi, belum dibandingkan dengan pasar.
- Aturan YouTube Creator Pool 2027: sumber sekunder, cek halaman resmi YouTube.
- Potongan Konten.com 20% dan batas 1.000.000 views per video: sumber campaign, cek ulang sebelum daftar.

---

## 10. Sumber

- klipaja.id — "Platform yang Bayar Clipper Pakai Dolar dari Indonesia 2026"; "Cara Ngeklip di Whop & Cuan Dolar 2026"; "Berapa Bayaran Clipper Whop per 1.000 Views"
- qlipper.id — "Konten.com untuk Clipper: Cara Daftar dan Cara Kerjanya" (dikutip Republika 19 Sep 2026)
- jawapos.com — "Gen Z Raup Jutaan dari Clipping, Sulianto Indria Putra Hadirkan Konten.com sebagai Marketplace" (18 Sep 2026)
- inet.detik.com — "Profesi Clipper Makin Dilirik Anak Muda" (13 Sep 2026)
- klipdong.id — "Gaji Clipper per Platform: Rate Resmi vs Estimasi"
- reap.video — "Whop Clipping: How to Make Money with Content Rewards (2026)"
- luminaclippers.com — "How Much Do Clippers Make?" (rujukan OpenClip, CreatorDB, NPR)
- YouTube Help — YouTube Partner Program overview & eligibility (dikutip sumber di atas, belum dicek langsung)


---

## 12. Status Implementasi (25 Okt 2026)

- Prototype `AnomalyStudio.jsx` dibangun: radar outlier, hook transkrip, VOC komentar, trend, nano matcher, simulator ads, dan kalender 8 atom.
- Data masih mock. Ganti dengan data ScrapeCreators saat API key tersedia.
- Skill yang dipakai untuk spek ini: `script-long-form` dan `fact-check-sources` untuk naskah video panjang, ditambah 46 skill dari v1.
