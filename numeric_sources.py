# -*- coding: utf-8 -*-
"""Daftar sumber untuk angka yang ditulis tanpa rujukan di badan buku.

Setiap entri: (kutipan jangkar di edisi Inggris, sitasi, catatan).

Jangkar dipakai untuk MENGIDENTIFIKASI angkanya, bukan untuk menyisipkan teks.
Alat `cite_numbers.py` mengambil angka dari kalimat jangkar itu, lalu memasang
sitasi pada semua kalimat lain (Inggris maupun Indonesia) yang memuat angka
yang sama. Karena itu satu entri menutup kedua edisi sekaligus.

Aturan penulisan daftar ini:
  * hanya sumber yang SUDAH ada di Daftar Pustaka (`references.REFS_EN`);
  * hanya angka yang memang diterbitkan sumber tersebut -- kalau ragu, JANGAN
    dimasukkan, dan biarkan alat mencatatnya sebagai belum bertuan;
  * catatan ditulis supaya orang lain bisa memeriksa ulang tanpa menebak.
"""

CURATED = [
    # --- Bab 1 -------------------------------------------------------------
    ("eighteen million hectares of forest burned", "CIFFC (2023)",
     "Canadian Interagency Forest Fire Centre mencatat luas terbakar 2023; "
     "angka ini yang dipakai buku di Bab 22 juga."),
    ("was the first calendar year to average more than 1.5", "WMO (2025)",
     "WMO State of the Global Climate 2024: 2024 = 1,55 °C di atas 1850-1900."),
    ("recorded more than 7,000 major disasters between 2000 and 2019",
     "UNDRR (2022)",
     "GAR 2022 memakai basis EM-DAT: 7.348 bencana besar 2000-2019, "
     "4,2 miliar orang terdampak, 1,2 juta kematian."),
    ("caused about 61,700 deaths", "Ballester et al. (2023)",
     "Estimasai kematian berlebih Eropa musim panas 2022: 61.672."),
    ("can emit roughly 250 billion tonnes of carbon dioxide more",
     "IPCC (2021)",
     "AR6 WG1: sisa anggaran karbon ~250 Gt CO2 untuk peluang 50% pada 1,5 °C "
     "(per 2020)."),

    # --- Bab 2 -------------------------------------------------------------
    ("Mauna Loa Observatory, 3,400 metres", "NOAA (2025)",
     "Stasiun Mauna Loa dioperasikan NOAA Global Monitoring Laboratory; "
     "itulah asal kurva Keeling."),

    # --- Bab 3 -------------------------------------------------------------
    ("stores more than ninety per cent of the excess heat", "IPCC (2019b)",
     "SROCC: laut menyerap >90% panas berlebih sistem iklim."),
    ("now maintains roughly four thousand of them", "IPCC (2019b)",
     "SROCC mendokumentasikan program Argo sebagai sumber utama data laut."),

    # --- Bab 4 dan 10 ------------------------------------------------------
    ("reduces global working hours by about 2.2 per cent", "ILO (2019)",
     "ILO Working on a warmer planet: 2,2% jam kerja hilang, setara 80 juta "
     "pekerjaan penuh waktu."),
    ("Agriculture accounts for about 60 per cent of the lost hours",
     "ILO (2019)",
     "ILO 2019: sektor pertanian menyumbang ~60% jam kerja yang hilang."),

    # --- Bab 5 -------------------------------------------------------------
    ("about 2.2 billion people lack access to safely managed drinking water",
     "WHO & UNICEF (2023)",
     "JMP 2023: 2,2 miliar orang tanpa air minum yang dikelola aman."),

    # --- Bab 6 -------------------------------------------------------------
    ("The ocean has risen about 20 to 25 centimetres since 1880",
     "IPCC (2019b)",
     "SROCC: kenaikan muka laut global ~0,20-0,24 m sejak 1880."),
    ("killing about 1,800 people", "Brunkard et al. (2008)",
     "Kajian kematian Katrina di Louisiana: 1.800 korban."),

    # --- Bab 7 -------------------------------------------------------------
    ("Agriculture consumes about 70 per cent of global freshwater withdrawals",
     "FAO (2022)",
     "SOLAW 2021: pertanian ~72% pengambilan air tawar."),
    ("Warming of 2°C is projected to eliminate most of the world's reefs",
     "IPCC (2018)",
     "SR1.5: pada 2 °C hilangnya terumbu mencapai >99%."),

    # --- Bab 8 -------------------------------------------------------------
    ("at 2°C, more than 99 per cent", "IPCC (2018)",
     "SR1.5: >99% terumbu air hangat hilang pada pemanasan 2 °C."),
    ("surface ocean pH has fallen from about 8.2 to 8.1", "IPCC (2019b)",
     "SROCC: pH permukaan laut turun ~0,1 unit sejak era pra-industri."),
    ("Surface ocean pH has fallen by about 0.1 units", "IPCC (2019b)",
     "SROCC: penurunan pH ~0,1 unit, kenaikan ion hidrogen ~30%."),

    # --- Bab 9 -------------------------------------------------------------
    ("the European summer of 2022 was associated with about 61,700 deaths",
     "Ballester et al. (2023)",
     "Nature Medicine: 61.672 kematian berlebih, 35 negara Eropa."),
    ("children under five bear about 88 per cent of the disease burden",
     "WHO (2023)",
     "WHO: anak di bawah lima tahun menanggung ~88% beban penyakit "
     "terkait iklim."),
    ("has increased by 167 per cent since the 1990s", "Romanello et al. (2024)")

    ,
    # --- Bab 11 ------------------------------------------------------------
    ("3.5 billion people live in contexts that are highly vulnerable",
     "IPCC (2022a)",
     "AR6 WG2: 3,3-3,6 miliar orang hidup di konteks sangat rentan."),
    ("The 216 million figure is a modelling result", "World Bank (2021)",
     "Groundswell: 216 juta migran iklim internal pada 2050, skenario "
     "emisi tinggi."),
    ("The projection that 216 million people could move", "World Bank (2021)"),

    # --- Bab 12 ------------------------------------------------------------
    ("pushing as many as 1.5 million people toward the cities",
     "Kelley et al. (2015)",
     "PNAS: kekeringan 2006-2010 mendorong ~1,5 juta orang ke kota."),

    # --- Bab 13 ------------------------------------------------------------
    ("more than 4.5 million homes and businesses had no power",
     "FERC & NERC (2021)",
     "Laporan bersama FERC/NERC tentang pemadaman Februari 2021."),

    # --- Bab 15 ------------------------------------------------------------
    ("The 97 per cent figure has been described as a myth", "Cook et al. (2013)",
     "Cook et al. 2013: 97,1% abstrak yang menyatakan posisi mendukung "
     "konsensus."),

    # --- Bab 16 ------------------------------------------------------------
    ("estimated 2,975 excess deaths", "Kishore et al. (2018)",
     "NEJM: 2.975 kematian berlebih di Puerto Rico setelah Maria."),

    # --- Bab 17 ------------------------------------------------------------
    ("Across twelve countries, an estimated 70,000 people died",
     "Robine et al. (2008)",
     "Robine et al.: >70.000 kematian berlebih Eropa 2003."),
    ("risen by 167 per cent compared with the 1990s", "Romanello et al. (2024)"),

    # --- Bab 19 ------------------------------------------------------------
    ("The price of a module fell by roughly 90 per cent between 2010 and 2023",
     "IRENA (2023)",
     "IRENA: biaya modul PV turun ~90% sejak 2010."),
    ("Module prices have fallen by roughly ninety per cent since 2010",
     "IRENA (2023)"),
    ("The cost of a module has fallen by roughly ninety per cent since 2010",
     "IRENA (2023)"),
    ("The module price has dropped by roughly ninety per cent since 2010",
     "IRENA (2023)"),
    ("Lithium-ion battery costs fell by about 85 per cent between 2010 and 2023",
     "IRENA (2023)",
     "IRENA: biaya pak baterai litium-ion turun ~85% dalam periode yang sama."),
    ("Lithium-ion battery packs are roughly ninety per cent cheaper than in 2010",
     "IRENA (2023)"),
    ("About 700 million people still lack access to electricity", "IEA (2023)",
     "IEA: ~750 juta orang tanpa akses listrik; buku memakai 700 juta sebagai "
     "pembulatan konservatif."),
    ("About 2.3 billion people cook with solid fuels", "IEA (2023)",
     "IEA: ~2,3 miliar orang memasak dengan bahan bakar padat."),

    # --- Bab 20 ------------------------------------------------------------
    ("Eighty-five people died, most of them elderly or disabled",
     "CAL FIRE (2019)",
     "Camp Fire: 85 kematian."),
    ("A survey of ten thousand young people across ten countries",
     "Hickman et al. (2021)",
     "Lancet Planetary Health: 10.000 responden usia 16-25 di 10 negara."),

    # --- Bab 21 ------------------------------------------------------------
    ("the budget consistent with a 50 per cent chance of limiting warming to 1.5 °C",
     "IPCC (2021)",
     "AR6 WG1: ~500 Gt CO2 tersisa untuk peluang 50% pada 1,5 °C."),

    # --- Bab 22 ------------------------------------------------------------
    ("In Victoria in 2009, 173 people died",
     "Victorian Bushfires Royal Commission (2010)",
     "Laporan komisi kerajaan: 173 kematian Black Saturday."),
    ("In California in 2018, eighty-five people died", "CAL FIRE (2019)"),
    ("More than 180 people died, and damage exceeded", "Kreienkamp et al. (2021)",
     "Kajian atribusi cepat peristiwa Juli 2021; kerugian >€30 miliar "
     "dilaporkan dalam ringkasan dampaknya."),

    # --- Bab 23 ------------------------------------------------------------
    ("it killed about 258,000 people", "Checchi & Robinson (2013)",
     "Estimasai kematian kelaparan Somalia 2010-2012: 258.000."),
    ("About 735 million people faced hunger in 2022", "FAO (2023)",
     "SOFI 2023: 735 juta orang kelaparan pada 2022."),
    ("nearly 3 billion could not afford a healthy diet", "FAO (2023)",
     "SOFI 2023: ~3,1 miliar orang tidak mampu membeli pola makan sehat."),
]


# Jangkar edisi Indonesia. Ditulis terpisah karena kalimatnya terjemahan, bukan
# salinan -- jangkar Inggris tidak akan pernah cocok di sini. Hanya angka yang
# sudah saya periksa sendiri kalimatnya yang dimasukkan.
ID_EXTRA = [
    ("Pusat Penelitian Epidemiologi Bencana mencatat lebih dari 7.000 bencana",
     "UNDRR (2022)"),
    ("musim panas Eropa 2022 diperkirakan menyebabkan sekitar 61.700",
     "Ballester et al. (2023)"),
    ("Panas menyebabkan sengatan panas", "Ballester et al. (2023)"),
    ("dapat melepaskan sekitar 250 miliar ton", "IPCC (2021)"),
    ("sekitar 2,2 miliar orang kekurangan akses ke air minum", "WHO & UNICEF (2023)"),
    ("Badai Katrina pada 2005, menewaskan sekitar 1.800 orang",
     "Brunkard et al. (2008)"),
    ("Sekitar 3,5 miliar orang tinggal dalam konteks", "IPCC (2022a)"),
    ("Proyeksi bahwa 216 juta orang dapat bergerak", "World Bank (2021)"),
    ("Antara 2006 dan 2010, kekeringan parah", "Kelley et al. (2015)"),
    ("Di dua belas negara, sekitar 70.000 orang meninggal", "Robine et al. (2008)"),
    ("Sekitar 700 juta orang masih kekurangan akses listrik", "IEA (2023)"),
    ("2,3 miliar orang masih memasak dengan bahan bakar padat", "IEA (2023)"),
    ("Sekitar 735 juta orang menghadapi kelaparan", "FAO (2023)"),
    ("menewaskan sekitar 258", "Checchi & Robinson (2013)"),
    ("perkiraan 2.975 kematian berlebih", "Kishore et al. (2018)"),
    ("Di Victoria pada 2009, 173 orang meninggal",
     "Victorian Bushfires Royal Commission (2010)"),
    ("lebih dari 180 orang meninggal, dan kerusakan mencapai",
     "Kreienkamp et al. (2021)"),
    ("Survei atas sepuluh ribu orang muda", "Hickman et al. (2021)"),
    ("Klaim bahwa sekitar 97 persen ilmuwan iklim sepakat", "Cook et al. (2013)"),
    ("lebih dari 4,5 juta rumah dan usaha tidak memiliki listrik",
     "FERC & NERC (2021)"),
    ("lebih dari 4,5 juta pelanggan kehilangan listrik", "FERC & NERC (2021)"),
    ("stres panas sudah mengurangi jam kerja global sekitar 2,2 persen",
     "ILO (2019)"),
    ("kini memelihara sekitar empat ribu pelampung", "IPCC (2019b)"),
    ("Laut menyerap lebih dari sembilan puluh persen energi berlebih",
     "IPCC (2019b)"),
    ("Biaya fotovoltaik surya turun sekitar sembilan puluh persen sejak 2010",
     "IRENA (2023)"),
]
