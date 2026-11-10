# Review: "4 repo GitHub ditempel ke Grok bot, $231,70 jadi $3.892,78 (16,8x) dalam 8j38m"

Sumber: [@savipww, 9 Nov 2026](https://x.com/savipww/status/2119800933961867280) — 345 like, 38 retweet.

Klaimnya: empat repo GitHub gratis ditempel ke "Grok bot", lalu bot itu trading memecoin
di sebuah app. Hasil dalam **8 jam 38 menit**: `$231,70 → $1.069,28 → $3.892,78`.
11 sell, 9 hijau, 2 merah, total merah **−$17,58** ("both cut by the -6% stop"),
best sell **+$1.049,96**. Tautan app-nya ada di balasan pertama:
`fomo.family/r/savipww` — sebuah **link referral**.

Empat repo yang disebut:

| # | Repo | Bintang (dicek 30 Okt 2026) | Isinya sebenarnya |
|---|---|---|---|
| 01 | `GMGNAI/gmgn-skills` | 701 (push 29 Okt) | skill OpenAPI GMGN: query token/wallet/market, eksekusi swap |
| 02 | `TauricResearch/TradingAgents` | **121.738** (push 4 Nov) | framework riset multi-agen LLM (bull vs bear) di atas data Yahoo Finance; eksekusinya ke **bursa simulasi** |
| 03 | `jup-ag/agent-skills` | 86 (push 7 Jul) | dokumen/skill untuk integrasi Jupiter |
| 04 | `xai-org/xai-sdk-python` | 606 (push 30 Okt) | SDK resmi xAI — klien HTTP |

Bintang TradingAgents memang benar **121K** (121.738 pada 4 Nov 2026). Tapi bintang
adalah ukuran popularitas, bukan rekam jejak — dan tidak satu pun dari empat repo itu
berisi strategi atau catatan hasil. Tiga di antaranya adalah pipa (data, eksekusi, klien
API); satu adalah alat riset yang bekerja pada bar harian, bukan medan 20 menit di
memecoin Solana. Bagian yang benar-benar mengambil keputusan — prompt-nya — justru
tidak ada di thread; ia ada di artikel berbayar/berlink.

---

## 1. Aritmetika yang benar

```
3.892,78 / 231,70 = 16,8009x        (klaim 16,80x: cocok)
leg 1  231,70 → 1.069,28 = 4,615x   (+361%)
leg 2  1.069,28 → 3.892,78 = 3,641x (+264%)
```

Sampai sini thread-nya jujur secara aritmetika. Yang menarik justru tiga angka
sampingnya: **9 hijau, 2 merah, total merah $17,58**. Ketiganya bisa dipakai untuk
menghitung mundur ukuran posisi — dan hasilnya memaksa kesimpulan yang tidak nyaman.

## 2. Yang tidak menutup: ukuran posisi

Stop −6% berarti kerugian satu trade = `6% × posisi`. Total dua merah = $17,58,
jadi rata-rata satu merah = $8,79.

```
posisi saat merah = 8,79 / 0,06 = $146,50
```

Padahal ekuitas mulai dari **$231,70** dan total kerugian sepanjang hari hanya $17,58 —
artinya ekuitas tidak pernah turun ke $146,50. Maka posisi **bukan** 100% ekuitas.
Batas atasnya:

```
0,06 × f × (E₁+E₂) = 17,58 ,  E ≥ 231,70 × 0,94² = 204,73
⇒ f ≤ 71,6% ekuitas per trade
```

Dan begitu `f` dibatasi, sisi pemenang ikut terpaksa:

| f (posisi/ekuitas) | rata-rata trade hijau yang dibutuhkan |
|---|---|
| 71,6% (batas atas) | **+53%** (1,53x) |
| 30% | +125% (2,25x) |
| 15% | +247% (3,47x) |
| 100% (mustahil di sini) | +39% (1,39x) |

Jadi buku itu mengklaim **9 trade berturut-turut naik 53% ke atas, tanpa satu pun
sempat mundur 6%**. Itu bukan mustahil untuk satu trade. Untuk sembilan berturut-turut,
peluangnya bisa dihitung persis, tanpa asumsi volatilitas:

```
P(kena target +53% sebelum stop −6%) = ln(0,94) / (ln(1,53) − ln(0,94)) = 12,70%
9 kali berturut-turut                     = 0,127^9 = 8,6 × 10⁻⁹  ≈ 1 dari 116 juta
```

Untuk target +100%: 8,20% per trade → 1,7 × 10⁻¹⁰. Untuk +254%: 4,67% → 1,1 × 10⁻¹².
Ini angka tanpa drift — drift positif menaikkannya (lihat §5), tapi tidak cukup
(lihat §4).

## 3. Dua angka yang saling mengunci: stop 6% vs volatilitas

Stop −6% adalah stop yang sangat rapat. Pada memecoin, 6% itu **noise**, bukan
informasi. Peluang satu trade menyentuh −6% selama holding (random walk, tanpa drift):

```
P(sentuh) = 2 × Φ( ln(0,94) / (σ√T) )
```

| σ per jam | holding | P(sentuh −6%) | harapan merah dari 11 | P(≤2 merah) |
|---|---|---|---|---|
| 5% | 20 mnt | 3,2% | 0,35 | 99,6% |
| 10% | 20 mnt | 28,4% | 3,12 | 35,6% |
| 15% | 20 mnt | 47,5% | 5,22 | 4,7% |
| **25%** | 20 mnt | **66,8%** | **7,35** | **0,13%** |
| 40% | 20 mnt | 78,9% | 8,68 | 0,00% |
| 60% | 20 mnt | 85,8% | 9,44 | 0,00% |

Membaliknya: supaya "2 merah dari 11" jadi hal yang wajar (P = 50%), volatilitasnya
harus **≤ 9% per jam**. Tapi pada σ = 9%/jam, peluang satu trade naik **+53% dalam
20 menit** adalah `2Φ(−8,1) ≈ 3 × 10⁻¹⁶` — nol.

Itulah jepitannya:

> Stop 6% yang hanya kena 2 kali dari 11 butuh koin **tenang**.
> Return 16,8x dalam 8 jam butuh koin yang **gila**.

Tidak ada satu buku yang bisa dua-duanya sekaligus.

Dua hal yang bisa melonggarkan analisis ini, dan sudah diperiksa:

* **Stop trailing, bukan stop tetap.** `gmgn-skills` memang punya trailing stop.
  Tapi trailing −6% justru **memperbanyak** exit, bukan mengurangi: trade yang
  berakhir +53% harus sudah mencapai +63% dulu dan tidak boleh mundur 6% dari puncak.
  Syarat "tidak pernah mundur 6% sebelum puncak" tetap berlaku.
* **Entry setelah momentum terkonfirmasi (drift).** Itu sudah dimodelkan di §4–§5:
  dengan drift 50%/jam pun 16,8x cuma 1 dari ~1.500; untuk membuatnya jadi *median*,
  drift-nya harus 0,89/jam.

## 4. Kalau modelnya dibuat netral, apakah 16,8x mungkin?

Model di `tools/agent_swarm_repost.py` sengaja tidak dibuat untuk membuat klaim ini
gagal:

* harga = geometric random walk, log-vol 25%/jam, holding 20 menit;
* stop −6% dimonitor kontinu, exit **di** barrier minus slippage 0,5%;
* biaya 3% per round trip (fee Fomo 0,5% × 2 sisi + impact 2%);
* **seluruh ekuitas** masuk tiap trade (paling menguntungkan untuk klaim), 11 trade.

Uji kejujurannya: tanpa drift dan tanpa biaya, exit di stopping time dari sebuah
martingale harus memberi `E[faktor] = 1,00` persis. Terukur: **1,006**. Modelnya
impas, bukan pesimis.

| drift/jam | median | rata² | P05 | P95 | untung | hijau/trade | ≥16,8x | 1 dari N | stop |
|---|---|---|---|---|---|---|---|---|---|
| 0% | 0,67 | 0,74 | 0,41 | 1,29 | 15,3% | 27,6% | 0,0000% | >20.000 | 66,7% |
| 5% | 0,75 | 0,83 | 0,43 | 1,49 | 23,3% | 30,9% | 0,0000% | >20.000 | 63,3% |
| 20% | 1,07 | 1,21 | 0,55 | 2,36 | 55,6% | 41,7% | 0,0000% | >20.000 | 53,1% |
| 50% | 2,71 | 3,20 | 1,10 | 6,97 | 96,5% | 62,8% | 0,0700% | 1.429 | 34,2% |
| 100% | 18,65 | 22,23 | 6,33 | 50,04 | 100% | 85,9% | 56,51% | 2 | 13,7% |

Dengan 400.000 percobaan: pada drift 0% **tidak ada satu pun** yang mencapai 16,8x
(`P < 1/400.000`), meski P(≥5x) = 1 dari 12.100. Bahkan pada drift 20%/jam (koin naik
~18% tiap 20 menit — fantasi) hasilnya masih `< 1/400.000`. Baru pada drift 50%/jam
(≈ ×1,65 tiap jam, terus-menerus 8 jam 38 menit) 16,8x baru jadi ≈1 dari 1.500.

Dan kombinasi yang diklaim — **9 hijau dan 2 merah dari 11**:

```
P(≥9 hijau) = 2,86 × 10⁻⁴      P(≤2 merah) = 1,37 × 10⁻³
gabungan    ≈ 3,9 × 10⁻⁷       (1 dari 2,6 juta percobaan)
```

## 5. Berapa "skill" yang dibutuhkan agar ini jadi normal?

Kalau pertanyaannya dibalik — bukan "apakah mungkin", tapi "seberapa hebat bot-nya
kalau angka ini tipikal" — jawabannya bisa dicari numerik:

> Supaya **median** dari 11 trade = 16,80x, log-drift harus **≈ 0,89 per jam**,
> yaitu harga **×2,4 tiap jam** selama 8 jam 38 menit, tanpa henti.

Tidak ada pasar yang membolehkan posisi penuh berulang kali di harga seperti itu.
Jadi angka 16,8x bukan bukti metode; ia adalah **ekor kanan** dari distribusi yang
median-nya 0,67. Satu tangkapan layar = satu sampel dari ekor itu.

## 6. Biaya: 11 round trip

Fee Fomo 0,5% per sisi = 1,0% per round trip (0,45% dengan referral). Gas ditanggung
platform; **price impact tidak**.

| biaya/round trip | drag 11 trade | gross yang dibutuhkan untuk net 16,8x |
|---|---|---|
| 1,0% (fee saja) | 10,5% | 18,8x |
| 2,0% | 19,9% | 21,0x |
| 3,0% | 28,5% | 23,5x |
| 5,0% | 43,1% | 29,5x |
| 10,0% | 68,6% | 53,5x |

Keluar $3.892 dari koin yang baru naik 3–5x adalah order besar di pool tipis. Impact
2% itu optimistis.

## 7. Yang sebenarnya bisa menghasilkan uang di thread ini

Yang bisa diperiksa: **tidak ada alamat wallet, tidak ada tx hash, tidak ada tautan
explorer, tidak ada riwayat 11 trade**, tidak ada screenshot P&L mentah di luar
tangkapan angka. Yang ada: link referral di balasan pertama, plus "prompt dan app-nya
ada di artikel saya".

Ekonomi referral Fomo (dari dokumentasi publik platform): perujuk dapat **25% dari fee
yang dibayar orang yang dirujuk, seumur akun**. Fee 0,5% per sisi. Dengan 345 like dan
38 retweet, bahkan konversi kecil pun memberi penghasilan yang **pasti**, sementara
16,8x dalam 8 jam adalah lotre. Insentif penulis dan pembaca tidak sejalan — sama
persis dengan dua thread sebelumnya di repo ini.

## 8. Verdict

| Pertanyaan | Jawaban |
|---|---|
| 16,80x secara aritmetika? | **Benar** (16,8009x) |
| Empat repo itu nyata? | **Nyata**, 701 / 121.738 / 86 / 606 bintang |
| Ada strategi di dalamnya? | **Tidak.** 3 pipa + 1 alat riset bar harian |
| Angka P&L bisa diverifikasi? | **Tidak.** Tanpa wallet/tx hash |
| Kombinasi 9 hijau + stop 6% mungkin? | **1 dari ~2,6 juta**, dengan model yang netral |
| Ada insentif lain? | **Ya.** Referral 25% fee seumur akun |

Bedanya dengan dua thread sebelumnya: yang ini **tidak salah secara mekanisme** —
menempelkan GMGN (data), Jupiter (eksekusi), dan SDK LLM memang arsitektur yang wajar.
Yang tidak ada adalah bagian yang menentukan **apa** yang dibeli, dan hasil 8 jam yang
diklaim berasal dari bagian itu. Arsitekturnya bisa ditiru; angkanya tidak bisa
diwarisi.

**Angka seperti ini tidak bisa dibuktikan dengan satu screenshot, tapi bisa dipatahkan
dengan satu pertanyaan: mana wallet-nya?** Sampai itu ada, yang diuji di sini adalah
aritmetikanya — dan aritmetikanya menolak.

## 9. Checklist verifikasi (10 menit, butuh jaringan)

1. Alamat wallet Solana + 11 signature → buka di Solscan. Tanpa ini, berhenti di sini.
2. P&L **30 hari**, bukan 8 jam. Satu window = satu lemparan koin.
3. Bandingkan harga entry/exit dengan harga pool saat itu (impact nyata, bukan quotes).
4. Ulangi dengan modal kertas 30 hari. Kalau edge-nya nyata, ia bertahan; kalau tidak,
   ia menghilang di bulan kedua — pola yang sudah terlihat di dua thread sebelumnya.

## 10. Lampiran: keempat repo dibuka, bukan cuma dihitung bintangnya

Dibaca langsung dari README masing-masing repo lewat GitHub API (30 Okt 2026):

| Repo | Bisa apa (dari README-nya sendiri) | Bisa menghasilkan 11 trade Solana? |
|---|---|---|
| `GMGNAI/gmgn-skills` | data on-chain SOL/BSC/Base/ETH, **market/limit order, take-profit/stop-loss, trailing stop, "cooking orders"**, manajemen wallet | **Ya** — ini satu-satunya yang menyentuh order nyata |
| `TauricResearch/TradingAgents` | riset multi-agen di atas ticker Yahoo Finance (`AAPL`, `0700.HK`, `BTC-USD`, …), keputusan dinilai "on final closes" | **Tidak.** Ticker memecoin Solana tidak ada di Yahoo Finance |
| `jup-ag/agent-skills` | installer plugin (`scripts/install_plugin.sh`) untuk Codex / Claude Code | **Tidak.** Isinya dokumen integrasi |
| `xai-org/xai-sdk-python` | klien gRPC Python untuk API xAI | **Tidak.** Ini HTTP/gRPC client |

Dan satu kalimat di README TradingAgents yang menutup seluruh cerita:

> "The Portfolio Manager approves/rejects the transaction proposal. If approved, the
> order will be sent to the **simulated exchange** and executed."

Jadi repo yang di thread itu disebut sebagai **"Analyst"** — yang katanya "bull vs bear
sebelum setiap beli" — (a) tidak bisa melihat token Solana, dan (b) eksekusinya
**simulasi**. Yang bisa menaruh order cuma `gmgn-skills`. Artinya: dari empat repo,
**satu** yang benar-benar trading, **satu** kerangka riset bar harian dengan bursa
simulasi, dan **dua** pipa. Keputusan "apa yang dibeli" tetap 100% milik prompt yang
tidak ditampilkan.

Itu bukan alasan untuk tidak memakai keempatnya — arsitekturnya justru wajar. Tapi
artinya angka 16,8x **tidak berasal dari repo-repo itu**. Repo hanya menyediakan
tangan; otaknya ada di tempat lain, dan otak itulah yang dijual lewat link.

## 11. Reproduksi

```bash
python tools/agent_swarm_repost.py                    # semua bagian
python tools/agent_swarm_repost.py --mode stops        # stop 6% vs volatilitas
python tools/agent_swarm_repost.py --mode swarm --attempts 400000
python tools/agent_swarm_repost.py --mode skill        # drift yang dibutuhkan
```

Tes: `python -m unittest tests.test_agent_swarm -v` — memeriksa bahwa harga barrier
konsisten dengan martingale, bahwa P(sentuh −6%) cocok dengan simulasi, bahwa biaya
monoton menurunkan hasil, dan bahwa 16,8x memang **bukan** hasil default model.
