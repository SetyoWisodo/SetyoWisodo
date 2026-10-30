# Review: "bot BTC 5 menit Polymarket" (@TGweb3333, 29 Okt 2026)

Sumber: [x.com/TGweb3333/status/2115889503814766874](https://x.com/TGweb3333/status/2115889503814766874)

Klaim intinya: hasil membongkar bot-bot paling profitable di Polymarket pada kontrak
naik/turun BTC 5 menit — "keuntungan jutaan", bisa direplikasi hanya dengan satu prompt
di Grok Bot.

Cara saya menilai: bukan dari nada bicaranya, tapi dari **apakah aritmetikanya masuk akal
dan apakah mekanismenya bisa bertahan**.

---

## 1. Yang benar, dan ini bagian paling berguna

Untuk kontrak biner yang membayar $1:

```
EV per kontrak = p_menang × (1 − harga) − (1 − p_menang) × harga
               = p_menang − harga
```

Jadi **harga yang kamu bayar adalah win rate yang kamu butuhkan**. Bukan 50%, bukan 70%:
harga itu sendiri.

| Harga beli | Win rate minimum | EV kalau win rate 53% |
|---|---|---|
| 30¢ | 30% | **+23,0¢** |
| 47¢ | 47% | +6,0¢ |
| 48¢ | 48% | +5,0¢ |
| 55¢ | 55% | **−2,0¢** |
| 70¢ | 70% | −17,0¢ |

Inilah kenapa kalimat penutupnya benar: **win rate 53% sambil agresif mengejar harga
memang bisa rugi** — kalau kamu membeli di 55¢, kamu butuh 55%, bukan 53%.

Dan ini bukan kebetulan: aturan yang sama dipakai sistem kita, hanya dalam bentuk lain.
Di Pumpkin Terminal, `EV ≥ 2× biaya` dan `t > ((1−p)s + c)/p` adalah versi umum dari
kalimat "harga adalah ambang". Matematikanya identik, instrumennya berbeda.

---

## 2. Tiga "permainan" — dinilai satu per satu

### a. Kunci 5¢: beli YES 47¢ + NO 48¢ = 95¢ → bayar $1

Aritmetikanya benar: 95¢ untuk klaim $1 = +5,26% per siklus. Masalahnya bukan aritmetika,
masalahnya **dua kaki itu tidak terisi bersamaan**.

Penyebabnya *legging risk*: begitu BTC bergerak, satu sisi menarik ordernya dan sisi lain
justru makin cepat terisi. Yang paling sering terjadi bukan "dua kaki terisi, profit
terkunci", tapi **satu kaki terisi lalu harga berbalik** — dan sekarang kamu memegang
posisi arah, bukan arbitrase.

Breakeven-nya bisa dihitung. Kalau satu kaki terisi saja biayanya −x%, dan lock-nya
+5,26%:

| Biaya satu kaki | Siklus yang harus terisi DUA kaki |
|---|---|
| −2% | 27,5% |
| −3% | **36,3%** |
| −4% | 43,2% |
| −5% | 48,7% |

Artinya: strategi ini bukan "profit tanpa risiko", tapi **menjual asuransi dan berharap
preminya lebih besar dari klaim**. Kalau kamu hanya terisi dua kaki 30% dari waktu, kamu
rugi.

Lalu ada uji kewajaran yang lebih keras. Kalau 5,26% per 5 menit benar-benar bisa
dikunci berulang:

```
(1,0526)^288 ≈ 2.581 × 10⁶
```

$181 menjadi $467 juta **dalam satu hari**, karena ada 288 siklus per hari. Tidak ada
pasar yang membiarkan itu bertahan lebih dari beberapa menit; spread akan ditutup oleh
orang pertama yang menemukannya. Jadi klaim "5¢ terkunci setiap putaran" secara
matematis membantah dirinya sendiri.

### b. Menangkap lag Binance → Polymarket ("beberapa detik")

Ini yang paling masuk akal secara teori — dan paling berbahaya secara praktik.

Kalau BTC naik $60 dan harga YES di Polymarket masih 55¢, membeli di situ memang
menguntungkan. Tapi konsekuensinya: setiap market maker yang menaruh ask 55¢ itu sedang
kalah cepat, dan **kamu adalah pihak yang menjual kepadanya** — atau sebaliknya, kamu
membeli dari orang yang belum tahu. Dalam pertukaran seperti ini, yang kalah adalah yang
infrastrukturnya lebih lambat.

"Beberapa detik" itu bahasa untuk pembaca retail. Bot yang benar-benar hidup bekerja
dalam milidetik, dan mereka berada di sisi yang sama denganmu — bukan melawanmu. Sisa
"lag beberapa detik" yang bisa kamu ambil adalah sisa setelah mereka kenyang, biasanya
di saat likuiditas paling tipis dan berita paling ambigu.

### c. Menangkap panic dump di 25–35¢ saat "masih 50:50"

Ini satu-satunya bagian yang punya inti benar: **opsi biner mendekati kedaluwarsa
memang sering salah harga**. Harga wajarnya bukan 50¢, tapi

```
P(naik) = Φ(d / σ)
```

dengan `d` = jarak spot ke strike dan `σ` = simpangan baku sisa waktu. Untuk BTC, sisa
2 menit, σ ≈ $120:

| d (spot − strike) | −60 | −30 | −15 | 0 | +15 | +30 | +60 |
|---|---|---|---|---|---|---|---|
| P(naik) | 30,9% | 40,1% | 45,0% | 50,0% | 55,0% | 59,9% | 69,1% |

Perhatikan: pada d = 0, harga wajar **50¢**. Jadi kalau benar-benar "50:50" dan ada
yang menjual di 30¢, itu hadiah 20¢ — terlalu besar untuk bertahan lebih dari beberapa
detik di pasar yang dipenuhi bot.

Yang lebih sering terjadi: quote 30¢ itu **benar**, karena spot-nya bukan 0, tapi sudah
−$60 dari strike. Dan justru di detik itu kamu sedang dipilih — *adverse selection*.
Penjual panik yang dikisahkan di thread itu adalah karakter yang sudah hampir punah di
pasar 2026; yang tersisa adalah pembuat pasar yang tahu persis `d` dan `σ`-nya.

---

## 3. Yang membuat saya berhenti percaya pada thread-nya

Bukan karena strateginya mustahil — sebagian masuk akal — tapi karena **produk yang
sebenarnya dijual bukan strategi itu**.

Balasan penulisnya sendiri di thread yang sama isinya: tautan pendaftaran Polymarket
dengan kode referral, tautan "bot copy-trading resmi" ke sebuah bot Telegram, dan tautan
grup Telegram berbahasa Mandarin.

Artinya: thread itu menghasilkan uang **dari volume orang yang mendaftar lewat
tautannya**, bukan dari bot yang dijelaskan. Ini juga menjelaskan klaim
"挂单吃单不用手续费，每天还能分到一部分平台手续费返佣" (tanpa fee, dan dapat bagi hasil
fee platform) — bagi hasil fee platform adalah **ekonomi referral**, bukan ekonomi
trading.

Tiga penanda lain:

1. Tidak ada satu pun tangkapan layar P&L dengan biaya, slippage, dan rentang waktu.
   "Keuntungan jutaan" tidak bisa diperiksa dan tidak bisa disalahkan.
2. "Cukup satu prompt di Grok Bot" — replikasi semudah itu bertentangan dengan klaim
   bahwa strateginya hasil membongkar bot terbaik. Kalau semudah menempel prompt, semua
   orang sudah melakukannya, dan edge-nya hilang.
3. Saran terakhirnya justru bagus (backtest 30 hari dengan fee nyata, 500 siklus
   simulasi, $10 per bet, stop harian $30). Sayangnya saran itu tidak pernah
   dihubungkan dengan angka mana pun dari strateginya sendiri.

Komentar yang paling tajam justru datang dari pembaca: *"288 kontrak sehari, artinya
tiap 5 menit ada settlement — slippage dan fee di frekuensi itu praktis jadi pajak tak
terlihat. Angka jutaan itu netto atau bruto?"* Pertanyaan itu tidak pernah dijawab.

---

## 4. Yang justru layak ditiru ke sistem kita

Empat hal dari thread ini **sudah** ada di Pumpkin Terminal, dan itu konfirmasi yang
bagus karena datang dari orang yang berbeda dengan instrumen yang berbeda:

| Prinsip di thread | Padanannya di sistem kita |
|---|---|
| "Harga adalah ambang win rate" | `t > ((1−p)s + c)/p` dan `EV ≥ 2× biaya` |
| "Hanya ambil kalau selisih >3¢ setelah fee" | Gerbang EV: menolak 60–70% kandidat |
| "Sebagian besar waktu, bot memilih tidak trading" | Desk menolak ~85% sinyal; 35 trade dari ratusan kandidat |
| "Jangan mengejar harga" | Band momentum + batas anti-chase 10–22% |

Satu hal yang **belum** kita punya dan layak dipertimbangkan: model biaya yang
memperhitungkan *fill probability*, bukan hanya slippage. Di thread itu, seluruh
masalahnya adalah "apakah order-ku terisi" — dan di memecoin, pertanyaan yang sama
berlaku: entry delay 1 tick kita mengasumsikan selalu dapat fill di harga mana pun.

Kalau kamu mau, saya bisa menambahkan simulasi dua kaki (legging risk) untuk mengukur
klaim #1 secara eksplisit: berapa `q` minimum agar "kunci 5¢" tidak rugi, dan bagaimana
distribusi hasilnya. Itu akan menjadi eksperimen yang jujur — dan kemungkinan besar
hasilnya: strategi itu rugi kecuali kamu punya latensi institusional.

---

## 5. Kesimpulan

**Sebagai matematika: setengah benar** — bagian biner dan bagian "53% masih rugi" itu
tepat dan berguna.

**Sebagai strategi: tidak bisa dipakai apa adanya** — play #1 adalah jebakan legging
yang membantah dirinya sendiri secara aritmetika, play #2 membutuhkan latensi yang
justru dimiliki lawanmu, play #3 punya inti benar tapi sudah dipanen oleh yang lebih
cepat.

**Sebagai konten: ini iklan.** Buktinya ada di balikannya sendiri, bukan di analisis
saya.

Dan yang paling penting, ini pengingat yang sama seperti thread "$80 → $5.432" dan
"10 repo kuant": **angka tanpa biaya, tanpa rentang waktu, dan tanpa jejak yang bisa
diperiksa bukan bukti.** Yang bisa diperiksa cuma satu — jalankan sendiri, ukur sendiri,
dan siap menerima kalau hasilnya negatif.
