#!/usr/bin/env python3
"""Lanjutan: falsifikasi bab 1, 3, 9, 10, 11, 14, 17 (EN + ID)."""
import pathlib
import re

EN = pathlib.Path("src/en")
ID_ = pathlib.Path("src/id")

TEKS = {
"02": ("""This chapter argues that risk is the product of hazard, exposure, and vulnerability, and that over a 10–20 year horizon vulnerability is the most productive place to work.

The falsifier is a variance decomposition with a stated threshold. Take a sample of events with recorded hazard intensity, recorded exposure (people and value in the affected area), and recorded vulnerability proxies (income, housing quality, age structure, access to services). If hazard intensity alone explains more than 90 per cent of the variance in death rates, and the social terms together add less than five percentage points, the chapter is wrong and the argument of Chapters 8 to 11 collapses.

A weaker version is available with existing data and has not come out the other way: cyclones of comparable strength produce death tolls that differ by two orders of magnitude, and the difference tracks income and shelter rather than wind speed [@sammonds2021; @undrr2022]. A dataset in which that relationship vanished would refute the claim.

The budget implication is falsified by outcome, not by argument. If countries that spent the largest share of their climate finance on response had the same mortality trend as countries that spent it on adaptation, the claim that the allocation matters would fail. That comparison is possible with the finance data and the mortality series, and the fact that it is rarely made is part of why the claim survives.""",
"""Bab ini berargumen bahwa risiko adalah produk dari bahaya, paparan, dan kerentanan, dan bahwa dalam horison 10–20 tahun kerentanan adalah tempat bekerja yang paling produktif.

Falsifikasinya adalah dekomposisi varians dengan ambang yang dinyatakan. Ambil sampel peristiwa dengan intensitas bahaya tercatat, paparan tercatat (orang dan nilai di kawasan terdampak), dan proksi kerentanan tercatat (pendapatan, mutu perumahan, struktur usia, akses layanan). Kalau intensitas bahaya saja menjelaskan lebih dari 90 persen varians angka kematian, dan suku-suku sosial bersama-sama menambah kurang dari lima poin persentase, bab ini salah dan argumen Bab 8 sampai 11 runtuh.

Versi yang lebih lemah tersedia dengan data yang sudah ada dan tidak keluar ke arah sebaliknya: siklon dengan kekuatan sebanding menghasilkan angka kematian yang berbeda dua orde besaran, dan perbedaannya mengikuti pendapatan dan tempat perlindungan, bukan kecepatan angin [@sammonds2021; @undrr2022]. Himpunan data di mana hubungan itu lenyap akan membantah klaim ini.

Implikasi anggarannya difalsifikasi oleh hasil, bukan oleh argumen. Kalau negara yang membelanjakan porsi terbesar keuangan iklimnya untuk respons memiliki tren kematian yang sama dengan negara yang membelanjangkannya untuk adaptasi, klaim bahwa alokasinya penting akan gugur. Perbandingan itu mungkin dilakukan dengan data keuangan dan deret kematian, dan fakta bahwa ia jarang dibuat adalah sebagian alasan klaim ini bertahan."""),

"04": ("""This chapter argues that Indonesia's contribution to the framework is to show hazard, exposure, and vulnerability being produced simultaneously, and that subsidence makes the archipelago a case where the hazard itself is a policy variable.

The falsifier is a subsidence measurement with a threshold. The chapter's claim is that land subsidence in Jakarta and Semarang is driven mainly by groundwater extraction, not by tectonic motion or sea-level change. If GPS and InSAR records showed that extraction fell sharply while subsidence continued at the same rate, the causal claim would be wrong and the policy conclusion — that stopping extraction buys time — would fail.

That test is runnable and has partly been run: subsidence rates in north Jakarta have been measured against extraction volumes and against tidal flooding [@abidin2011]. A city that halted extraction and saw subsidence stop would confirm the mechanism; one that halted it and saw no change would refute it.

The second claim, about the archipelago as a reader rather than an exception, is falsified if the Indonesian cases fail to behave like the framework's cases elsewhere: if hazard, exposure, and vulnerability did not separate in the Indonesian record, or if the country's outcomes were explained entirely by the physical hazard. The comparison with Bangladesh and the Philippines on storm mortality is the natural test, and it has not been made systematically in this literature."""),

"10": ("""This chapter argues that infrastructure failure is primarily a property of dependencies rather than of individual components, and that redundancy and code enforcement are systematically underfunded because their benefits are invisible.

The falsifier is a comparison of failure modes. Take a sample of infrastructure failures in extreme events and classify each by proximate cause: component failure under load, or failure propagated through a dependency. The chapter is wrong if component failures predominate — say, more than two-thirds of outages and service failures — and dependency chains explain little.

The Texas 2021 case is the chapter's clearest evidence and also its limit: the grid failed because gas supply, water, and power were mutually dependent, and the sequence is documented [@ferc2021]. A system that failed in a heat wave with no dependency chain — a single transformer, a single pump — would not refute the claim, but a population of such failures would.

The funding claim is falsified by budget data: if utilities that spent more on redundancy had the same outage duration as those that did not, controlling for event severity, the claim fails. That comparison is available from utility reliability filings, and it is the kind of test this book should invite rather than avoid [@flyvbjerg2014]."""),

"11": ("""This chapter argues that social capital predicts disaster recovery better than material resources, and that the mechanism is the speed of informal mutual aid in the first 72 hours.

The falsifier is a recovery regression with a stated comparison. Take disaster-affected communities with measured social capital (association density, trust, network breadth) and measured material resources (income, aid received, damage), and compare recovery outcomes after three years. The chapter is wrong if material resources explain recovery better than social capital does, once damage is controlled for.

Aldrich's cross-national comparison is the direct test and it goes the chapter's way [@aldrich2012]. A replication in which the social-capital coefficient vanished once income was properly measured would refute the claim — and that replication is worth attempting, because the two variables are correlated and the measurement of social capital is contested.

The claim about the dark side is a boundary condition, not a separate hypothesis, and it is falsified if bonding capital never impeded recovery: if communities with dense inward-looking networks recovered as fast as communities with bridging ties, the distinction would be unnecessary [@putnam1993]. The Gotong royong case suggests the boundary is real, but it is one case."""),

"12": ("""This chapter argues that warning failure is a delivery and action problem rather than a detection problem, and that the last mile is a person rather than a channel.

The falsifier is a decomposition of warning failure by stage. Take documented failures and classify the point at which the chain broke: detection, forecasting, transmission, comprehension, or action. The chapter is wrong if most failures occur at detection or forecasting — the stages that technology serves — rather than at transmission and action.

The Ahr valley case is the chapter's strongest evidence and its clearest test: the forecast existed and the warning did not arrive as an instruction [@kreienkamp2021]. A comparable event in which the forecast was wrong, and the warning system performed as designed, would count against the chapter — and such events exist, which is why the claim is about prevalence rather than about every case.

The claim about the last mile is falsified by a delivery experiment: if a mass SMS to every registered phone produced the same evacuation rate as a door-to-door alert by a known person, the person would not be the mechanism. The evidence from Bangladesh points the other way [@sammonds2021], but it is observational, and a trial would settle it."""),

"14": ("""This chapter argues that the two climate inequalities are distinct, that the accounting basis determines the political conclusion, and that domestic injustice undermines adaptation effectiveness.

The first claim is falsified by showing that the two distributions coincide: that the countries with the largest cumulative emissions are also, in rank order, the countries with the highest climate-attributable harm per capita. They do not coincide at the top, but a demonstration that the rank correlation exceeds 0.9 across the whole distribution would collapse the distinction.

The second claim is arithmetic: change the accounting basis and the ranking of obligations changes. The book's own box does the arithmetic; a basis that left the ranking unchanged across every plausible choice would refute the claim [@matthews2015; @heede2014].

The third claim is the one most likely to be wrong, and its falsifier is a comparison of programmes. If adaptation spending distributed regressively — concentrated on the better-off — produced the same reduction in vulnerability as an equal sum distributed progressively, then equity would have no independent effect on effectiveness. The evidence is indirect, drawn mostly from settings other than climate adaptation, and the chapter should be read as arguing a mechanism rather than reporting a measured effect [@tol2018]."""),

"18": ("""This chapter is a set of tests, not an argument, so the falsification question is different: what would show that the tests are wrong?

The first test is calibration. If the claims that survive the seven questions were no more accurate, on average, than the claims that fail them, the tests would be worthless. That is measurable: take a sample of climate claims, apply the tests, then score the claims against what later happened. The forecasting literature suggests that structured reasoning improves accuracy modestly and reliably, but the effect is small enough that a null result in a climate-specific sample would count against this chapter [@tetlock2015].

The second test is usability. If a reader with no climate training cannot apply tests one, two, and four to a newspaper article after reading this chapter, the tests fail as a reference tool regardless of their validity. That is testable with a small trial: give the chapter to two groups, give the article to both, and compare the quality of their written assessments.

The third test is the book's own. A reader who applies the seven questions to this book should find at least one place where the book fails its own standard. If the book passes all seven cleanly, the tests are too weak — a set of questions that never bites is decoration. The weakest point is the falsification sections of the earlier chapters: several state a direction without a threshold, and a reader is entitled to mark that down [@gaillard2019]."""),
}

INDO = {
"02": """Bab ini berargumen bahwa risiko adalah produk dari bahaya, paparan, dan kerentanan, dan bahwa dalam horison 10–20 tahun kerentanan adalah tempat bekerja yang paling produktif.

Falsifikasinya adalah dekomposisi varians dengan ambang yang dinyatakan. Ambil sampel peristiwa dengan intensitas bahaya tercatat, paparan tercatat (orang dan nilai di kawasan terdampak), dan proksi kerentanan tercatat (pendapatan, mutu perumahan, struktur usia, akses layanan). Kalau intensitas bahaya saja menjelaskan lebih dari 90 persen varians angka kematian, dan suku-suku sosial bersama-sama menambah kurang dari lima poin persentase, bab ini salah dan argumen Bab 8 sampai 11 runtuh.

Versi yang lebih lemah tersedia dengan data yang sudah ada dan tidak keluar ke arah sebaliknya: siklon dengan kekuatan sebanding menghasilkan angka kematian yang berbeda dua orde besaran, dan perbedaannya mengikuti pendapatan dan tempat perlindungan, bukan kecepatan angin [@sammonds2021; @undrr2022]. Himpunan data di mana hubungan itu lenyap akan membantah klaim ini.

Implikasi anggarannya difalsifikasi oleh hasil, bukan oleh argumen. Kalau negara yang membelanjakan porsi terbesar keuangan iklimnya untuk respons memiliki tren kematian yang sama dengan negara yang membelanjangkannya untuk adaptasi, klaim bahwa alokasinya penting akan gugur. Perbandingan itu mungkin dilakukan dengan data keuangan dan deret kematian, dan fakta bahwa ia jarang dibuat adalah sebagian alasan klaim ini bertahan.""",
"04": """Bab ini berargumen bahwa sumbangan Indonesia pada kerangka ini adalah menunjukkan bahaya, paparan, dan kerentanan sedang diproduksi secara bersamaan, dan bahwa penurunan muka tanah menjadikan nusantara kasus di mana bahayanya sendiri adalah variabel kebijakan.

Falsifikasinya adalah pengukuran penurunan tanah dengan ambang. Klaim bab ini adalah bahwa penurunan tanah di Jakarta dan Semarang terutama digerakkan oleh penyedotan air tanah, bukan oleh gerak tektonik atau perubahan muka laut. Kalau catatan GPS dan InSAR menunjukkan penyedotan turun tajam sementara penurunan tanah berlanjut pada laju yang sama, klaim kausalnya salah dan kesimpulan kebijakannya — bahwa menghentikan penyedotan membeli waktu — akan gagal.

Uji itu bisa dijalankan dan sebagian sudah dijalankan: laju penurunan tanah di Jakarta utara sudah diukur terhadap volume penyedotan dan terhadap banjir pasang [@abidin2011]. Kota yang menghentikan penyedotan lalu penurunan tanahnya berhenti akan menegaskan mekanismenya; yang menghentikannya dan tidak melihat perubahan akan membantahnya.

Klaim kedua, tentang nusantara sebagai pembaca alih-alih pengecualian, difalsifikasi kalau kasus Indonesia tidak berperilaku seperti kasus kerangka ini di tempat lain: kalau bahaya, paparan, dan kerentanan tidak terpisah dalam catatan Indonesia, atau kalau hasilnya dijelaskan sepenuhnya oleh bahaya fisik. Perbandingan dengan Bangladesh dan Filipina dalam kematian akibat badai adalah uji alaminya, dan perbandingan itu belum dibuat secara sistematis dalam literatur ini.""",
"10": """Bab ini berargumen bahwa kegagalan infrastruktur terutama merupakan sifat ketergantungan, bukan sifat komponen individual, dan bahwa redundansi serta penegakan kode kekurangan dana secara sistematis karena manfaatnya tidak terlihat.

Falsifikasinya adalah perbandingan mode kegagalan. Ambil sampel kegagalan infrastruktur dalam peristiwa ekstrem dan klasifikasikan tiap kegagalan menurut penyebab langsungnya: kegagalan komponen di bawah beban, atau kegagalan yang menjalar lewat ketergantungan. Bab ini salah kalau kegagalan komponen mendominasi — katakanlah lebih dari dua per tiga gangguan dan kegagalan layanan — dan rantai ketergantungan menjelaskan sedikit.

Kasus Texas 2021 adalah bukti terjelas bab ini sekaligus batasnya: jaringan listrik gagal karena pasokan gas, air, dan listrik saling bergantung, dan urutannya terdokumentasi [@ferc2021]. Sistem yang gagal dalam gelombang panas tanpa rantai ketergantungan — satu transformator, satu pompa — tidak akan membantah klaimnya, tetapi populasi kegagalan semacam itu akan.

Klaim tentang pendanaan difalsifikasi oleh data anggaran: kalau utilitas yang membelanjakan lebih banyak untuk redundansi memiliki durasi gangguan yang sama dengan yang tidak, setelah keparahan peristiwa dikendalikan, klaimnya gugur. Perbandingan itu tersedia dari laporan keandalan utilitas, dan itulah jenis uji yang seharusnya buku ini undang, bukan hindari [@flyvbjerg2014].""",
"11": """Bab ini berargumen bahwa modal sosial memprediksi pemulihan bencana lebih baik daripada sumber daya material, dan bahwa mekanismenya adalah kecepatan gotong royong informal pada 72 jam pertama.

Falsifikasinya adalah regresi pemulihan dengan perbandingan yang dinyatakan. Ambil komunitas terdampak bencana dengan modal sosial terukur (kepadatan asosiasi, kepercayaan, keluasan jaringan) dan sumber daya material terukur (pendapatan, bantuan diterima, kerusakan), lalu bandingkan hasil pemulihan setelah tiga tahun. Bab ini salah kalau sumber daya material menjelaskan pemulihan lebih baik daripada modal sosial, setelah kerusakan dikendalikan.

Perbandingan lintas negara Aldrich adalah uji langsungnya dan ia berpihak pada bab ini [@aldrich2012]. Replikasi di mana koefisien modal sosial lenyap setelah pendapatan diukur dengan benar akan membantah klaimnya — dan replikasi itu layak diupayakan, karena kedua variabel berkorelasi dan pengukuran modal sosial diperdebatkan.

Klaim tentang sisi gelap adalah syarat batas, bukan hipotesis terpisah, dan ia difalsifikasi kalau modal sosial bonding tidak pernah menghambat pemulihan: kalau komunitas dengan jaringan inward-looking yang padat pulih secepat komunitas dengan ikatan bridging, pembedaannya tidak diperlukan [@putnam1993]. Kasus gotong royong menunjukkan batas itu nyata, tetapi ia satu kasus.""",
"12": """Bab ini berargumen bahwa kegagalan peringatan adalah masalah penyampaian dan tindakan, bukan masalah deteksi, dan bahwa mil terakhir adalah seorang manusia, bukan saluran.

Falsifikasinya adalah dekomposisi kegagalan peringatan menurut tahap. Ambil kegagalan terdokumentasi dan klasifikasikan titik di mana rantainya putus: deteksi, prakiraan, transmisi, pemahaman, atau tindakan. Bab ini salah kalau sebagian besar kegagalan terjadi pada deteksi atau prakiraan — tahap yang dilayani teknologi — bukan pada transmisi dan tindakan.

Kasus lembah Ahr adalah bukti terkuat bab ini dan ujinya terjelas: prakiraannya ada dan peringatannya tidak tiba sebagai instruksi [@kreienkamp2021]. Peristiwa sebanding di mana prakiraannya salah dan sistem peringatannya bekerja sesuai rancangan akan melawan bab ini — dan peristiwa semacam itu ada, yang karena itu klaimnya tentang prevalensi, bukan tentang setiap kasus.

Klaim tentang mil terakhir difalsifikasi oleh eksperimen penyampaian: kalau SMS massal ke setiap ponsel terdaftar menghasilkan tingkat evakuasi yang sama dengan pemberitahuan dari pintu ke pintu oleh orang yang dikenal, maka manusianya bukan mekanisme. Bukti dari Bangladesh mengarah sebaliknya [@sammonds2021], tetapi ia observasional, dan sebuah uji coba akan menyelesaikannya.""",
"14": """Bab ini berargumen bahwa dua ketidaksetaraan iklim itu berbeda, bahwa basis akuntansi menentukan kesimpulan politik, dan bahwa ketidakadilan domestik melemahkan keefektifan adaptasi.

Klaim pertama difalsifikasi dengan menunjukkan bahwa dua distribusi itu berimpit: bahwa negara dengan emisi kumulatif terbesar juga, dalam urutan peringkat, negara dengan kerugian iklim per kapita tertinggi. Keduanya tidak berimpit di puncak, tetapi demonstrasi bahwa korelasi peringkatnya melebihi 0,9 di seluruh distribusi akan meruntuhkan pembedaan ini.

Klaim kedua bersifat aritmetis: ubah basis akuntansi, berubahlah peringkat kewajiban. Kotak di buku ini mengerjakan aritmetikanya; basis yang membiarkan peringkat tidak berubah di semua pilihan yang masuk akal akan membantah klaim ini [@matthews2015; @heede2014].

Klaim ketiga adalah yang paling mungkin salah, dan falsifikasinya adalah perbandingan program. Kalau belanja adaptasi yang terdistribusi regresif — terkonsentrasi pada yang lebih mampu — menghasilkan penurunan kerentanan yang sama dengan jumlah yang sama yang terdistribusi progresif, maka keadilan tidak punya efek mandiri pada keefektifan. Buktinya tidak langsung, sebagian besar dari konteks selain adaptasi iklim, dan bab ini harus dibaca sebagai mengargumenkan mekanisme, bukan melaporkan efek terukur [@tol2018].""",
"18": """Bab ini adalah seperangkat uji, bukan argumen, jadi pertanyaan falsifikasinya berbeda: apa yang akan menunjukkan bahwa ujinya salah?

Uji pertama adalah kalibrasi. Kalau klaim yang lolos tujuh pertanyaan ternyata tidak lebih akurat, rata-rata, daripada klaim yang gagal, ujinya tidak berharga. Itu terukur: ambil sampel klaim iklim, terapkan ujinya, lalu nilai klaim itu terhadap apa yang kemudian terjadi. Literatur peramalan menunjukkan penalaran terstruktur memperbaiki akurasi secara sederhana dan konsisten, tetapi efeknya cukup kecil sehingga hasil nol pada sampel khusus iklim akan melawan bab ini [@tetlock2015].

Uji kedua adalah kegunaan. Kalau pembaca tanpa pelatihan iklim tidak bisa menerapkan uji satu, dua, dan empat pada artikel koran setelah membaca bab ini, ujinya gagal sebagai alat rujukan terlepas dari validitasnya. Itu bisa diuji dengan percobaan kecil: berikan bab ini kepada dua kelompok, berikan artikelnya kepada keduanya, dan bandingkan mutu penilaian tertulis mereka.

Uji ketiga adalah uji buku ini sendiri. Pembaca yang menerapkan tujuh pertanyaan pada buku ini seharusnya menemukan setidaknya satu tempat di mana buku ini gagal memenuhi standarnya sendiri. Kalau buku ini lolos ketujuh-tujuhnya dengan bersih, ujinya terlalu lemah — seperangkat pertanyaan yang tidak pernah menggigit adalah hiasan. Titik terlemahnya adalah seksi falsifikasi bab-bab sebelumnya: beberapa di antaranya menyatakan arah tanpa ambang, dan pembaca berhak mencatatnya sebagai kekurangan [@gaillard2019].""",
}

HEAD_EN = "## What would prove this chapter wrong"
HEAD_ID = "## Apa yang akan membuktikan bab ini salah"


def ganti(path, judul, baru):
    t = path.read_text(encoding="utf-8")
    pola = re.compile(r"(?m)^" + re.escape(judul) + r"\s*\n(.*?)(?=^## |\Z)", re.S)
    m = pola.search(t)
    if not m:
        return False
    path.write_text(t[: m.start(1)] + "\n" + baru.strip() + "\n\n" + t[m.end(1):], encoding="utf-8")
    return True


gagal = 0
for k, isi in TEKS.items():
    if isinstance(isi, tuple):
        isi = isi[0]
    if not ganti(next(EN.glob(f"{k}-*.md")), HEAD_EN, isi):
        print("GAGAL EN", k); gagal += 1
for k, isi in INDO.items():
    if not ganti(next(ID_.glob(f"{k}-*.md")), HEAD_ID, isi):
        print("GAGAL ID", k); gagal += 1
print("selesai; gagal:", gagal)
