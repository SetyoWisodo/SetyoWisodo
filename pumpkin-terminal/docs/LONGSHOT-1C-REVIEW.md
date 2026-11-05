# Review: "dompet yang beli kontrak 1¢ di BTC 5 menit, profit $604k"

Sumber: [@CDanielleD1997, 5 Nov 2026](https://x.com/CDanielleD1997/status/2118221212790722672)

Klaimnya: sebuah wallet membeli sisi "hampir mati" di pasar biner BTC 5 menit Polymarket
seharga 1–1,2¢, lalu dibayar $1 (≈80–96x). Tiga transaksi yang ditampilkan:

| Arah | Masuk | Keluar | Return |
|---|---|---|---|
| DOWN @1,2¢ | $156 | $13.450 | +8.520% |
| UP @1,1¢ | $93 | $8.434 | +8.999% |
| DOWN @1,0¢ | $68 | $6.564 | +9.514% |
| **Total 3 tiket** | **$317** | **$28.448** | **+8.873%** |

Lima transaksi terbaik di layar: ±$432 masuk, ±$38.434 keluar. Total profit yang
diklaim: **$604.000**.

---

## 1. Aritmetika yang benar

Untuk kontrak biner, `EV = p − harga`. Tiket 1,2¢:

```
break-even hit rate = 1,2%
```

Bukan 50%, bukan 30%. Jadi seluruh pertanyaan di thread itu menyusut jadi satu baris:
**saat harga menyentuh 1,2¢, apakah peluang sebenarnya di atas 1,2%?**

Itu pertanyaan yang bisa dijawab. Dan jawabannya tidak datang dari tangkapan layar
kemenangan.

## 2. Yang tidak ditampilkan: penyebutnya

Tiga tiket menang dengan odds ~89x. Yang tidak ada di thread: **berapa tiket yang
kalah**. Kalau dia membeli 250 tiket dan menang 3, hit rate-nya 1,2% — persis impas.
Kalau dia membeli 1.000 tiket dan menang 30, hit rate 3% — itu edge yang sangat besar.

Dari $317 menjadi $28.448 pada tiga tiket, kita tidak bisa membedakan **operator dengan
model volatilitas** dan **orang yang sedang beruntung**. Keduanya menghasilkan tangkapan
layar yang sama persis. Yang membedakan hanya satu: seluruh riwayat wallet, bukan
kemenangannya.

Dan ini bukan kecurigaan kosong: wallet address-nya **diberikan** di thread. Artinya
datanya bisa diperiksa — lihat §5.

## 3. Model: dari mana sebenarnya edge itu datang

Alatnya: [`tools/longshot_1c.py`](../tools/longshot_1c.py). 3.000 pasar, tiket $100,
bankroll $10.000.

Asumsinya satu variabel: `k` = seberapa salah pembuat pasar mengukur volatilitas
(`σ_true / σ_maker`). Kalau `k = 1`, pasar dihargai wajar; kalau `k = 1,2`, volatilitas
sebenarnya 20% lebih tinggi dari yang dipakai si pembuat harga.

| k | Sinyal muncul | Trade | Hit rate | EV/kontrak | ROI | Streak kalah terburuk | Max DD | Bangkrut? |
|---|---|---|---|---|---|---|---|---|
| 1,0 | 8,9% pasar | 266 | 0,75% | −0,45¢ | −37% | 161 | 100% | **YA** |
| 1,1 | 28,3% | 849 | 1,06% | −0,14¢ | −12% | 226 | 100% | **YA** |
| 1,2 | 100% | 3.000 | 1,87% | +0,67¢ | +56% | 200 | 70% | tidak |
| 1,5 | 100% | 3.000 | 5,10% | +3,90¢ | +325% | 134 | 40% | tidak |
| 2,0 | 100% | 3.000 | 12,20% | +11,0¢ | +917% | 51 | 12% | tidak |
| 3,0 | 100% | 3.000 | 20,67% | +19,5¢ | +1.622% | 31 | 8% | tidak |

Tiga hal yang penting dari tabel ini:

**(a) Pada harga yang wajar, membeli tiket 1,2¢ justru RUGI.** Hit rate-nya 0,75%,
bukan 1,2%. Kenapa? Karena kamu membeli **saat harga menembus** batas 1,2¢ — pada
detik itu nilai wajarnya sudah *di bawah* 1,2¢. Membeli di ekor dengan limit adalah
*adverse selection* murni: kamu hanya terisi ketika sisimu sedang paling buruk. Ini
kembaran dari pelajaran sebelumnya (cut di 35¢): harga yang kamu bayar adalah ambangnya,
dan membeli tepat di ambang berarti membayar lebih.

**(b) Edge-nya bukan "pasar lupa menaruh harga", tapi kesalahan mengukur volatilitas.**
Volatilitas 20% lebih tinggi saja sudah membalik ROI dari −37% menjadi +56%. Ini masuk
akal dengan cerita di thread: profitnya muncul saat "行情剧烈波动" — ketika harga bergerak
kasar dan pembuat pasar masih memakai σ tenang. Di ekor distribusi, kesalahan 20% pada σ
adalah kesalahan 2,5x pada probabilitas.

**(c) Variancenya brutal.** Bahkan pada `k = 1,2` yang menguntungkan, kalah
**200 kali berturut-turut** masih dalam rentang normal. Dengan tiket $100 dan bankroll
$10.000, kamu bangkrut sebelum menang. Ukuran tiket yang benar dari sisi Kelly: pada
p = 3% dan odds 82x, Kelly hanya menyarankan **1,8% bankroll** per tiket — sekitar $180
pada bankroll $10k. Kebetulan, angka itu sejajar dengan ukuran tiket di thread ($68–156).
Kalau itu memang sizing Kelly, berarti pelakunya disiplin; kalau bukan, dia beruntung.

## 4. Kenapa ini lebih jujur daripada dua thread sebelumnya

Bedanya penting: thread "$80 → $5.432" dan "bot Polymarket profit jutaan" tidak memberi
apa pun yang bisa diperiksa. Thread ini **memberikan alamat wallet**. Itu satu-satunya
jenis klaim yang bisa diuji, dan itu patut dihargai walaupun kita belum tahu hasilnya.

## 5. Cara memverifikasi dalam 10 menit (kalau kamu punya akses jaringan)

1. Ambil seluruh riwayat trade wallet itu dari API publik Polymarket
   (`data-api.polymarket.com/trades?user=<alamat>`), bukan dari tangkapan layar.
2. Hitung **semua** tiket yang dibeli dengan harga ≤2¢: jumlah, harga rata-rata, dan
   berapa yang menang. Bukan pemenangnya — semuanya.
3. Hitung hit rate. Bandingkan dengan harga rata-rata (ambang impas).
4. Pisahkan berdasarkan volatilitas 5 menit saat pembelian (BTC realized vol dari
   Binance). Kalau edge-nya benar, hit rate harus **jauh lebih tinggi saat vol tinggi**
   daripada saat vol rendah. Itu yang membedakan model dari keberuntungan.
5. Kalau hit rate > harga + biaya pada 1.000+ tiket, dan selisihnya terkonsentrasi di
   periode volatil → **edge-nya nyata**. Kalau tidak → itu satu sampel dari ribuan wallet.

Saya tidak bisa menjalankan langkah ini dari sini: lingkungan kerja saya tidak punya
akses ke domain Polymarket. Yang bisa saya lakukan adalah membangun modelnya dan
menunjukkan bahwa mekanismenya masuk akal — bukan bahwa klaimnya benar.

## 6. Kesimpulan

**Mekanismenya masuk akal.** Membeli ekor di pasar biner yang dihargai dengan σ yang
salah adalah strategi nyata, dan BTC 5 menit adalah tempat yang tepat untuk itu: expiry
cepat, volatilitas berubah mendadak, dan tick 1¢ membuat harga tidak bisa turun lebih
jauh.

**Klaimnya belum terbukti.** Yang ditampilkan adalah pembilang ($604k) tanpa penyebut
(berapa tiket yang hangus). Dua orang yang sangat berbeda bisa menghasilkan tangkapan
layar itu.

**Dan yang paling penting: ini bukan "beli 1¢ lalu tunggu".** Itu versi yang akan
menghabiskan bankroll dalam 200 tiket. Versi yang bekerja menuntut model volatilitas
yang lebih cepat dari pembuat pasar — pekerjaan yang sama sulitnya dengan semua hal lain
di repo ini, dan dengan variance yang jauh lebih kejam.

Aturan yang sama tetap berlaku, hanya sekarang dari dua arah:

| Thread | Bentuk | Win rate | EV |
|---|---|---|---|
| Cut yang kalah @35¢ | menang kecil sering, kalah besar jarang | 67,2% | **−2,84%** |
| Tiket ekor @1,2¢ (harga wajar) | kalah kecil sering, menang besar jarang | 0,75% | **−37%** |
| Tiket ekor @1,2¢ (vol salah 20%) | sama, tapi dengan edge | 1,87% | **+56%** |

Win rate yang tinggi bukan bukti untung. Win rate yang rendah bukan bukti rugi.
**Satu-satunya yang menentukan adalah p − harga.**
