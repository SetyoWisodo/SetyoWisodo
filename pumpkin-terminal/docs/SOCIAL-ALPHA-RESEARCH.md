# Riset: sinyal sosial-media untuk trading meme coin

Riset ini dilakukan 30 Oktober 2026 lewat GitHub Search API (bintang & deskripsi
diambil saat itu). Tujuannya bukan mengumpulkan repo, tapi **mengambil teknik yang
bisa dipertanggungjawabkan secara matematis** dan membuang yang cuma jualan mimpi.

---

## 1. Sentimen finansial yang mengerti bahasa pasar

| Repo | ★ | Yang diambil |
|---|---|---|
| [ProsusAI/finBERT](https://github.com/ProsusAI/finBERT) | 2.267 | Model BERT yang di-fine-tune pada teks finansial jauh mengalahkan lexicon umum. **Pelajaran:** kamus sentimen umum salah membaca "the dev dumped" sebagai netral. |
| [valuesimplex/FinBERT](https://github.com/valuesimplex/FinBERT) · [yya518/FinBERT](https://github.com/yya518/FinBERT) | 943 · 667 | Varian & benchmark; menunjukkan akurasi klasifikasi sentimen finansial ~0,80–0,85 F1 pada korpus berita. **Batas atas realistis** untuk sinyal teks murni. |
| [louisowen6/SENN](https://github.com/louisowen6/SENN) | 76 | Ensemble: sentimen + fitur historis dijadikan satu model, bukan sinyal tunggal. **Pelajaran:** jangan pernah mengambil keputusan dari satu skor sentimen. |

**Keputusan implementasi:** tanpa torch/GPU, saya tidak bisa menjalankan BERT.
Jadi dipakai lexicon finansial/meme yang sadar konteks (negasi, intensifier, sarkasme
pola tetap, emoji, cashtag) + skor kepercayaan. Di README ditulis jelas bahwa ini
**bukan** FinBERT; kalau kamu punya GPU, `social_signal.py` punya satu titik
`score_text()` yang bisa diganti model apa pun.

---

## 2. Metrik sosial, bukan cuma sentimen

| Repo | ★ | Yang diambil |
|---|---|---|
| [danilobatson/ai-trading-agent-gemini](https://github.com/danilobatson/ai-trading-agent-gemini) | 467 | Pipeline 7 langkah: tarik metrik sosial (LunarCrush: social volume, engagement, Galaxy Score, AltRank) → LLM → sinyal BUY/SELL/HOLD + confidence. **Pelajaran:** yang memprediksi bukan "positif/negatif", tapi **perubahan kecepatan** volume & engagement. |
| [Drabble/TwitterSentimentAndCryptocurrencies](https://github.com/Drabble/TwitterSentimentAndCryptocurrencies) | 107 | Studi korelasi sentimen Twitter ↔ harga kripto. Kesimpulannya tipis dan lag-nya tidak stabil. **Pelajaran:** korelasi mentah ≠ edge; butuh konfirmasi lintas-lapisan. |
| [StephanAkkerman/fintwit-bot](https://github.com/StephanAkkerman/fintwit-bot) | 164 | Ingesti media sosial → alert → sinyal. **Pelajaran:** arsitektur ingest → skor → rute jauh lebih penting daripada modelnya. |

**Keputusan implementasi:** skor sosial dibangun dari **turunan** (velocity,
akselerasi, rasio engagement/follower, konsentrasi akun), bukan level mentah.
Level mentah mudah dimanipulasi; turunan butuh biaya lebih besar untuk dipalsukan.

---

## 3. Siapa yang bicara: bobot pengaruh & reputasi

| Repo | ★ | Yang diambil |
|---|---|---|
| [nirholas/kol-quest](https://github.com/nirholas/kol-quest) | 26 | Leaderboard KOL multi-sumber, filter win-rate, deteksi wash wallet, feed real-time. **Pelajaran:** ikuti akun yang **terbukti** menggerakkan harga, bukan yang paling ramai. |
| [CabalSpy/CabalSpy-MCP-Server](https://github.com/CabalSpy/CabalSpy-MCP-Server) · [wtfspiff/KOLTracker](https://github.com/wtfspiff/KOLTracker) | — | Pelacakan dompet KOL + deteksi wash trading. |

**Keputusan implementasi:** `InfluenceGraph` menyimpan reach (follower × engagement
rate) dan **reputasi empiris** per akun: setiap panggilan dinilai setelah 20 tick.
Reputasi memakai Laplace smoothing, jadi akun baru tidak langsung dipercaya.
Ini identik dengan `WhaleRegistry` di modul Whale Radar — satu mekanisme, dua sumber.

---

## 4. Deteksi koordinasi (senjata utama melawan rugpull bersponsor)

| Repo | ★ | Yang diambil |
|---|---|---|
| [srishtimotwani3/social-media-bot-detection-graph-analytics](https://github.com/srishtimotwani3/social-media-bot-detection-graph-analytics) | — | Graph analytics (GraphFrames) untuk mendeteksi perilaku inautentik terkoordinasi. Pola: komponen terhubung padat, akun baru, posting serempak. |
| [alex-maclaren/authenticity-toolkit](https://github.com/alex-maclaren/authenticity-toolkit) | — | Toolkit astroturfing: kemiripan teks, akun dibuat berdekatan, rasio follower/following. |
| [sudhakardev/social-bot-anomaly-detection](https://github.com/sudhakardev/social-bot-anomaly-detection) | — | Anomali berbasis SQL: burst waktu, entropi teks rendah. |

**Keputusan implementasi — 5 fitur, semuanya bisa dihitung < 1 ms:**
1. **Kemiripan teks** (Jaccard shingle 3-gram) → >0,72 = klon.
2. **Burst** — jumlah akun berbeda dalam jendela 3 tick; entropi waktu rendah.
3. **Akun baru** — umur akun < 7 hari.
4. **Rasio follower/following** ekstrem.
5. **Konsentrasi kashtag** — semua menempel satu token dalam jendela sempit.

Skor koordinasi 0–1 menggabungkan kelimanya. **Ini bukan kemewahan: inilah yang
memisahkan "orang benar-benar bicara" dari "dev membayar 200 bot".**

---

## 5. Eksekusi & mekanika on-chain

| Repo | ★ | Yang diambil |
|---|---|---|
| [chainstacklabs/pumpfun-bonkfun-bot](https://github.com/chainstacklabs/pumpfun-bonkfun-bot) | 1.044 | Bot pump.fun tanpa API pihak ketiga: pantau pembuatan token, beli, keluar sesuai strategi. **Pelajaran:** exit harus ditentukan sebelum entry, bukan sesudah. |
| [rckprtr/pumpdotfun-sdk](https://github.com/rckprtr/pumpdotfun-sdk) | 817 | SDK bonding curve. Harga bergerak di sepanjang kurva — slippage bukan angka tetap. |
| [cicere/pumpfun-bundler](https://github.com/cicere/pumpfun-bundler) | 443 | Bundler 25 buy di blok pertama. **Pelajaran:** kalau kamu membeli setelah bundle, kamu adalah exit liquidity-nya. Ini alasan `bundle_pct` masuk forensics. |
| [mortdeus/solana-copy-sniper-mev-trading-bot](https://github.com/mortdeus/solana-copy-sniper-mev-trading-bot) | 4.509 | Copy-trading & MEV. **Pelajaran:** keunggulan latency adalah milik infra, bukan milik strategi. Jangan bersaing di sana dengan VPS rumahan. |

---

## Yang **tidak** saya ambil, dan kenapa

- **Bot sniper MEV / bundler**: butuh validator/gRPC shred stream dan modal besar.
  Bersaing latency dengan mereka = kekalahan yang sudah pasti.
- **"AI agent" yang langsung mengeksekusi tanpa batas risiko**: semua repo yang
  serius menaruh risk-management di depan, bukan di belakang.
- **Klaim win rate 90%+ di README**: tidak ada satu pun repo di atas yang
  mempublikasikan hasil audited dengan angka seperti itu. Yang ada: backtest
  dengan periode terpilih, tanpa biaya, tanpa slippage.

---

## Kesimpulan riset → keputusan desain

1. **Sentimen mentah lemah** (korelasi tipis, mudah dimanipulasi).
   → pakai turunan: velocity, akselerasi, konsentrasi, reputasi akun.
2. **Deteksi koordinasi adalah edge yang paling bisa dipertahankan.**
   → jadi gerbang wajib, bukan opsional.
3. **Reputasi harus dipelajari online**, bukan dari daftar "KOL top" statis.
   → Laplace-smoothed reputation, sama seperti modul whale.
4. **Eksekusi menanggung biaya terbesar.** Round-trip meme coin 4–7%.
   → target profit harus dihitung dari biaya, bukan dari harapan.
5. **Exit ditentukan sebelum entry.** → ladder TP + stop keras + time stop.
6. **High win rate bukan tujuan; expectancy yang positiflah tujuan.**
   → lihat `docs/MATEMATIKA.md`.

---

### Batasan riset ini (jujur)

- Bintang GitHub mengukur popularitas, bukan kualitas hasil trading.
- Tidak ada satu pun repo di atas yang mempublikasikan track record live yang
  diaudit pihak ketiga. Termasuk yang punya 4.509 bintang.
- Semua angka performa di repo ini berasal dari **simulasi** yang saya tulis
  sendiri. Itu mengukur mesinnya, bukan pasar.
