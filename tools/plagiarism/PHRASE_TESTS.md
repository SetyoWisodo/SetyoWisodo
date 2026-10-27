# Uji Frasa ke Web — 12 Kalimat, Kata per Kata

Metode: satu kalimat utuh dari tiap bab diambil apa adanya, diberi tanda kutip, lalu
dicari ke mesin pencari. Kalau susunan kata itu pernah ditulis orang lain di halaman
yang terindeks, hasilnya akan muncul **persis**.

Ini pengganti paling dekat untuk lapisan "internet" milik Turnitin, yang tidak bisa
diakses tanpa lisensi. Bedanya: Turnitin memindai miliaran halaman sekaligus, di sini
12 kalimat diuji satu per satu. Karena itu hasil ini disebut **sampel**, bukan skor penuh.

**Hasil: 0 dari 12 kalimat ditemukan kata per kata di web.**

| Bab | Kalimat yang diuji | Kecocokan |
|---|---|---|
| 1 — Introduction | The losses, adjusted for inflation, have grown by about 5 to 7 per cent a year, faster than exposure alone would predict. | **0** |
| 2 — Physical Science | The Greenland ice sheet is losing mass at roughly 250–300 gigatonnes a year, and Antarctica's contribution has grown as its outlet glaciers have accelerated (Shepherd et al., 2020). | **0** |
| 3 — Climate Systems | Satellite altimeters have measured sea level continuously since 1993, and the record shows a rise that has accelerated from about two millimetres a year to more than four (IPCC, 2019b). | **0** |
| 5 — Water and Drought | The 2022 Horn of Africa drought was declared after five consecutive failed rainy seasons, by which time more than twenty million people were acutely food insecure. | **0** |
| 7 — Food Security | Fungal pathogens that were once limited to warm regions are moving poleward and upward; coffee leaf rust, which devastated Central American plantations in 2012–2013, was associated with higher temperatures and more variable rainfall. | **0** |
| 9 — Health Impacts | Nepal, which historically had little dengue, recorded its first major outbreak in 2022, and cases have appeared in highland districts that were previously too cool (Cissé et al., 2022). | **0** |
| 11 — Migration | Fiji has become the most studied case, having relocated several villages from coastlines exposed to erosion and storm surge, starting with Vunidogoloa in 2014. | **0** |
| 12 — Conflict | Higher food prices can trigger urban unrest, as the 2007–2008 and 2010–2011 episodes demonstrated across several continents (FAO, 2023). | **0** |
| 16 — Household Prep. | When Hurricane Maria struck Puerto Rico on 20 September 2017, it did more than damage buildings (Kishore et al., 2018). | **0** |
| 17 — Emergency Response | Even lower wet-bulb temperatures, around 31 °C, can be dangerous for older adults and people with chronic illness. | **0** |
| 18 — Social Capital | After the 2017 Mexico City earthquake, civilian brigades known as topos dug survivors out of rubble before professional teams arrived. | **0** |
| 19 — Renewable Energy | Module prices have fallen by roughly ninety per cent since 2010, and the decline has tracked cumulative installed capacity rather than time. | **0** |

## Yang muncul di pencarian, dan kenapa itu bukan masalah

Setiap pencarian **memang** mengembalikan artikel tentang topik yang sama — NASA tentang
kehilangan massa lapisan es, WHO tentang wabah dengue Nepal, FEWS NET tentang musim hujan
Somalia yang gagal, *Foreign Policy Analysis* tentang harga pangan dan kerusuhan. Itu wajar
dan tidak bisa dihindari: fakta bersama harus muncul di banyak tempat.

Yang tidak ditemukan adalah **susunan kalimatnya**. Contohnya:

- Buku: *"losing mass at roughly 250–300 gigatonnes a year"*.
  NASA: *"losing mass at a rate of 283 gigatonnes per year"* dan *"about 264 billion tons
  per year"*. Angkanya sama-sama benar, kalimatnya berbeda.
- Buku: *"the 2007–2008 and 2010–2011 episodes demonstrated across several continents"*.
  Jurnal: *"The global commodity price spikes in 2007–08 corresponded with unrest in around
  50 countries"*. Sama peristiwanya, beda penyusunan.

Inilah sebabnya Turnitin sering memberi skor 10–20% pada naskah akademik yang sepenuhnya
orisinal: yang terdeteksi adalah **frasa baku, nama lembaga, dan deretan angka**, bukan
penyalinan.

## Frasa baku yang memang muncul di tempat lain

Ini bukan plagiasi dan tidak akan dikurangi, karena memang istilah resminya:

| Frasa di buku | Dipakai juga oleh |
|---|---|
| five consecutive failed rainy seasons | FEWS NET, OCHA, IPC |
| wet-bulb temperature | jurnal fisiologi dan klimatologi |
| civilian brigades known as topos | pemberitaan gempa Mexico City 2017 |
| track[ing] cumulative installed capacity | IEA, IRENA |

## Kalau ingin melakukannya sendiri

Uji ulang dengan kalimat lain, karena sampel 12 kalimat tidak mewakili 7.355:

```
python tools/plagiarism/check.py --picks 24
```

Lalu untuk tiap kalimat, cari di mesin pencari dengan tanda kutip:

```
"kalimat lengkap dari buku"
```

Yang **perlu dicurigai**: hasil yang memuat 8 kata atau lebih berturut-turut sama persis
tanpa tanda kutip atau sitasi.

Yang **tidak perlu dicurigai**: artikel dengan topik sama, angka sama, atau frasa teknis
baku yang sama.
