#!/usr/bin/env python3
"""Ganti seksi falsifikasi tiap bab dengan versi terukur (variabel, arah, ambang).

Dijalankan sekali; idempoten karena hanya mengganti isi seksi berjudul tetap.
"""
import pathlib
import re

EN = pathlib.Path("src/en")
ID_ = pathlib.Path("src/id")

TUJUAN = {
    "05": """This chapter argues that heat mortality is primarily a function of social and built-environment vulnerability rather than of temperature alone, and that modest, cheap interventions — registers, calls, cooling access — can move the death toll substantially.

The falsifier is a cross-city comparison with a stated coefficient. Take cities with heat-mortality records disaggregated by age and living arrangement, and regress excess deaths on temperature, on the share of the population living alone, and on the share aged over 75. The chapter is wrong if the social variables add less than five percentage points to explained variance once temperature is controlled for, or if the coefficient on living alone is indistinguishable from zero across every city in the sample.

The comparison has been run, and it has not gone the chapter's way: Klinenberg's Chicago neighbourhoods shared a temperature field and differed in death rate by a factor of ten [@klinenberg2002], and the British Columbia review found that 56 per cent of the dead lived alone and 98 per cent died indoors [@bccoroners2022]. A city that matched those figures and produced a flat mortality surface would refute the mechanism.

The second claim is testable by intervention. If registers, call lists, and cooling access did not move the death toll, a city that adopted them should show no decline relative to a matched city that did not. Ahmedabad's evaluation is the closest thing to that test in the literature, and it found a decline [@hess2018] — a single city, with the weaknesses of a before-and-after design, which is why this chapter states the result as suggestive rather than settled.""",
    "06": """This chapter argues that flood risk is set more by land use and drainage than by rainfall totals, that large defences create new risk by attracting development, and that distributed storage is systematically underfunded relative to structural defence.

The falsifier has a specific shape: a paired comparison. Take two catchments with similar rainfall climatology and different land-use trajectories, or one catchment before and after a change in its zoning, and compare damage per unit of exposed value per unit of rainfall. The chapter is wrong if damage tracks rainfall with an elasticity near one and land use adds no explanatory power.

The literature has run versions of this test. Paired-event studies that hold the hazard roughly constant find that the outcome depends on preparedness and land use, not on the return period of the rainfall alone [@bubeck2017]. A well-documented case of two comparable cities where the one that paved its catchment suffered no more damage would count against the chapter — and the search for such a case is the honest way to test it.

The levee-paradox claim is falsified differently: find a city that built a large defence, kept land-use rules unchanged, and saw real exposure behind the defence stop rising. The claim predicts that development follows the structure within a decade; a counter-example would need to show the land behind a new levee stayed vacant for that period, with the zoning record to prove it.""",
    "07": """This chapter argues that food crises are produced by market structure and policy response as much as by harvest outcomes, and that storage, market access, and anticipatory finance do more good per unit of cost than yield increases.

The falsifier is a decomposition. For a set of food-price spikes, separate the price change into the part explained by production shortfalls and the part explained by trade-policy changes, stock movements, and exchange rates. The chapter is wrong if the production term accounts for most of the variance — say, more than three-quarters across the episodes — and the policy terms add little.

The 2007–2008 and 2023 episodes are the natural test cases, and both go the chapter's way: prices moved far more than production did, and the largest single mover was export restriction [@fao2023]. A third episode in which a production shortfall of comparable size produced a proportionately smaller price rise, with no change in trade policy, would count against the chapter.

The claim about anticipatory finance is falsified by a controlled comparison: households that received a pre-harvest transfer should not differ from matched households that received the same sum after the harvest. If the timing made no difference to consumption, assets, or distress sales, the claim is empty. The test has been run in a handful of settings and the results are mixed enough that the chapter should be read as stating a plausible mechanism rather than an established effect [@fao2019].""",
    "08": """This chapter argues that climate-sensitive disease is primarily a function of health and water infrastructure, that climate change is one driver among several, and that generic infrastructure investment protects better than disease-specific campaigns.

The falsifier is a variance decomposition across places. Take dengue or cholera incidence by district, together with climate variables (temperature, rainfall), infrastructure variables (piped-water coverage, sanitation, surveillance capacity), and income. The chapter is wrong if climate variables explain most of the between-district variance and infrastructure adds little once climate is controlled for.

The evidence currently points the other way: districts with similar climates and different water and surveillance systems have very different burdens, and the 2024 dengue surge tracked health-system capacity as much as temperature [@mordecai2020; @who2023dengue]. A district that matched its climate twin on incidence, despite a decade of infrastructure divergence, would refute the claim.

The claim about generic investment is testable by trial: a water-supply or sanitation programme should reduce climate-sensitive disease more per dollar than a vector-control campaign in the same setting. If campaign spending outperformed infrastructure spending under comparable conditions, the chapter's policy conclusion would be wrong even if its diagnosis held.""",
    "09": """This chapter argues that the financial architecture of disaster response favours the legible and the insured, arrives after the decisions that determine recovery, and leaves a large category of loss uncovered.

The falsifier is a distributional test with a benchmark. Take post-disaster transfers by household and compare them with losses by household. If transfers were proportional to loss — regardless of title, income, documentation, or insurance — the chapter is wrong. The measurable version: regress transfer receipts on assessed loss and on tenure status. The chapter predicts a positive coefficient on tenure that survives controls for loss, and a negative coefficient on informality.

The finding is consistent across countries and event types, which is what makes the claim strong and also what would make a clean counter-example decisive [@undrr2022]. A country with a functioning presumptive-registration system that paid informal dwellers in proportion to loss would be that counter-example, and the chapter should name it if one exists.

The timing claim is falsified by dates: if the median household transfer arrived before the median household recovery decision — the decision to rebuild, to move, or to borrow — the claim fails. That is measurable from payment records and survey dates, and it is rarely measured, which is itself part of the argument.""",
    "13": """This chapter argues that displacement is inevitable in some places, that planned relocation fails when it ignores livelihoods and networks, and that the terms of migration should be negotiated before the site becomes uninhabitable.

The falsifier is a follow-up comparison. Take relocation schemes with documented livelihood support and schemes without, matched on hazard exposure and distance moved, and compare household income, employment, and return rates three to five years after the move. The chapter is wrong if the schemes with support performed no better than those without, once pre-move income is controlled for.

The evidence on Fiji and Vietnam points the chapter's way, and it is thin: the number of well-documented relocations with follow-up data is small enough that a single well-run study could move the conclusion [@iom2023]. That is the honest state of the claim.

The timing claim is testable against process records: schemes where terms were agreed before the site became uninhabitable should show lower rates of secondary displacement — households moving again within five years — than schemes negotiated under emergency conditions. If the rates were the same, the chapter's policy conclusion would be wrong.""",
    "14": """This chapter argues that the two climate inequalities are distinct, that the accounting basis determines the political conclusion, and that domestic injustice undermines adaptation effectiveness.

The first claim is falsified by showing that the two distributions coincide: that countries with the largest cumulative emissions are also, in rank order, the countries with the highest climate-attributable harm per capita. They plainly do not coincide at the top — the largest emitters are not the most harmed — but a demonstration that the correlation is near one across the whole distribution would collapse the distinction.

The second claim is arithmetic and political at once: change the accounting basis and the ranking of obligations changes. That is checkable, and the book's own box does the arithmetic; a basis that left the ranking of obligations unchanged across all plausible choices would refute the claim [@matthews2015; @heede2014].

The third claim is the one most likely to be wrong, and its falsifier is a comparison of programmes. If adaptation spending distributed regressively — concentrated on the better-off — produced the same reduction in vulnerability as an equal sum distributed progressively, then equity would have no independent effect on effectiveness and the claim fails. The evidence on cooperation and compliance suggests otherwise, but it is indirect, drawn mostly from settings other than climate adaptation, and the chapter should be read as arguing a mechanism rather than reporting a measured effect [@tol2018].""",
    "16": """This chapter argues that city adaptive capacity is determined by maintenance funding, land-use rules, and coordination rather than by the size of a climate plan or a single infrastructure project.

The falsifier is a prediction test. Take cities with a published climate plan and cities without, or cities with strong and weak maintenance records, and compare outcomes in actual events: deaths, days of service interruption, and damage per unit of exposed value. The chapter is wrong if plan size predicts outcomes better than the maintenance ratio — the share of the infrastructure budget spent on upkeep — once city income is controlled for.

The measurable version of the claim is a coefficient comparison: in a regression of event outcomes on both variables, the standardised coefficient on maintenance should exceed the one on plan expenditure. That test has not, to this book's knowledge, been run across a city sample; the chapter's evidence is case-based, drawn from drainage failures and land-use enforcement [@bubeck2017; @flyvbjerg2014]. A city with a large plan, no maintenance, and good outcomes in a real event would be the counter-example, and it should be named.

The claim about routines is falsified by audit: if cities that changed their maintenance schedule and permit review showed no improvement in outcome relative to cities that merely published a plan, the mechanism would be wrong.""",
    "17": """This chapter is a set of tests, not an argument, so the falsification question is different: what would show that the tests are wrong?

The first test is calibration. If the claims that survive the seven questions were no more accurate, on average, than the claims that fail them, the tests would be worthless. That is measurable: take a sample of climate claims, apply the tests, then score the claims against what later happened. The forecasting literature suggests that structured reasoning improves accuracy modestly and reliably, but the effect is small enough that a null result in a climate-specific sample would count against this chapter [@tetlock2015].

The second test is usability. If a reader with no climate training cannot apply tests one, two, and four to a newspaper article after reading this chapter, the tests fail as a reference tool regardless of their validity. That is testable with a small trial: give the chapter to two groups, give the article to both, and compare the quality of their written assessments.

The third test is the book's own. A reader who applies the seven questions to this book should find at least one place where the book fails its own standard. If the book passes all seven cleanly, the tests are too weak — a set of questions that never bites is decoration. The weakest point is the falsification sections of the earlier chapters: several of them state a direction without a threshold, and a reader is entitled to mark that down [@gaillard2019].""",
    "15": """This chapter argues that household preparation is valuable but limited, that social contact is the highest-value household intervention, and that the commercial preparedness model misallocates attention.

The falsifier is a household-level comparison with an outcome variable. Take households exposed to the same event, with equipment inventories and social-contact measures recorded before it, and compare outcomes after it: injury, property damage, days displaced, and recovery time. The chapter is wrong if equipment predicts outcomes better than contact does, once income and hazard exposure are controlled for.

The heat evidence is the strongest part of the case and also the narrowest: it comes from mortality, where the outcome is not ambiguous [@bccoroners2022; @klinenberg2002]. For floods and storms the evidence is weaker, and a study that found well-equipped but isolated households recovering faster than connected ones would refute the claim for those hazards.

The claim about the commercial model is falsified by price and effect together: if the equipment sold to households delivered measurable risk reduction per dollar comparable to the social measures, the charge of misallocation would fail. That comparison is almost never made, which is why the chapter states it as an argument rather than a finding.""",
}

INDO = {
    "05": """Bab ini berargumen bahwa kematian akibat panas terutama merupakan fungsi kerentanan sosial dan lingkungan terbangun, bukan semata-mata suhu, dan bahwa intervensi sederhana dan murah — daftar warga rentan, panggilan, akses pendinginan — dapat menggerakkan angka kematian secara berarti.

Falsifikasinya adalah perbandingan antarkota dengan koefisien yang dinyatakan. Ambil kota yang punya catatan kematian akibat panas terpilah menurut usia dan susunan tempat tinggal, lalu regresikan kematian berlebih terhadap suhu, terhadap proporsi penduduk yang tinggal sendiri, dan terhadap proporsi usia di atas 75 tahun. Bab ini salah kalau variabel sosial menambah kurang dari lima poin persentase varians terjelaskan setelah suhu dikendalikan, atau kalau koefisien tinggal sendiri tidak bisa dibedakan dari nol di semua kota dalam sampel.

Perbandingan ini pernah dijalankan, dan hasilnya tidak berpihak pada kebalikan bab ini: lingkungan-lingkungan di Chicago berbagi medan suhu yang sama dan berbeda angka kematian hingga sepuluh kali [@klinenberg2002], dan tinjauan British Columbia menemukan 56 persen korban tinggal sendiri dan 98 persen meninggal di dalam ruangan [@bccoroners2022]. Kota yang menyamai angka itu tetapi menghasilkan permukaan kematian yang datar akan membantah mekanismenya.

Klaim kedua bisa diuji lewat intervensi. Kalau daftar warga rentan, daftar panggilan, dan akses pendinginan tidak menggerakkan angka kematian, kota yang menerapkannya seharusnya tidak menunjukkan penurunan dibanding kota pembanding yang tidak menerapkannya. Evaluasi Ahmedabad adalah hal terdekat dengan uji itu dalam literatur, dan ia menemukan penurunan [@hess2018] — satu kota, dengan kelemahan desain sebelum-sesudah, yang karena itu bab ini menyatakan hasilnya sebagai petunjuk, bukan kesimpulan final.""",
    "06": """Bab ini berargumen bahwa risiko banjir lebih ditentukan oleh tata guna lahan dan drainase daripada oleh total curah hujan, bahwa pertahanan besar menciptakan risiko baru dengan menarik pembangunan, dan bahwa tampungan tersebar secara sistematis kekurangan dana dibandingkan pertahanan struktural.

Falsifikasinya punya bentuk spesifik: perbandingan berpasangan. Ambil dua daerah tangkapan dengan klimatologi hujan serupa dan lintasan tata guna lahan berbeda, atau satu daerah tangkapan sebelum dan sesudah perubahan zonasi, lalu bandingkan kerusakan per satuan nilai terpapar per satuan curah hujan. Bab ini salah kalau kerusakan mengikuti curah hujan dengan elastisitas mendekati satu dan tata guna lahan tidak menambah daya penjelas.

Literatur sudah menjalankan versi uji ini. Studi peristiwa berpasangan yang menahan bahaya relatif konstan menemukan bahwa hasilnya bergantung pada kesiapsiagaan dan tata guna lahan, bukan pada periode ulang curah hujannya saja [@bubeck2017]. Kasus terdokumentasi baik tentang dua kota sebanding, di mana kota yang menghabiskan daerah tangkapannya tidak menderita kerusakan lebih besar, akan melawan bab ini — dan mencari kasus seperti itu adalah cara jujur mengujinya.

Klaim paradoks tanggul difalsifikasi dengan cara lain: temukan kota yang membangun pertahanan besar, membiarkan aturan tata guna lahan tidak berubah, dan melihat paparan riil di belakang tanggul berhenti naik. Klaimnya memprediksi pembangunan mengikuti struktur itu dalam satu dekade; lawan-contohnya harus menunjukkan lahan di belakang tanggul baru tetap kosong selama periode itu, dengan bukti zonasinya.""",
    "07": """Bab ini berargumen bahwa krisis pangan dihasilkan oleh struktur pasar dan respons kebijakan sebesar hasil panen, dan bahwa penyimpanan, akses pasar, serta pembiayaan antisipatif berbuat lebih banyak per satuan biaya daripada peningkatan hasil panen.

Falsifikasinya adalah dekomposisi. Untuk sejumlah lonjakan harga pangan, pisahkan perubahan harga menjadi bagian yang dijelaskan oleh kekurangan produksi dan bagian yang dijelaskan oleh perubahan kebijakan perdagangan, pergerakan stok, dan nilai tukar. Bab ini salah kalau suku produksi menjelaskan sebagian besar varians — katakanlah lebih dari tiga per empat di seluruh episode — dan suku kebijakan menambah sedikit.

Episode 2007–2008 dan 2023 adalah kasus uji alaminya, dan keduanya berpihak pada bab ini: harga bergerak jauh lebih besar daripada produksi, dan penggerak tunggal terbesar adalah pembatasan ekspor [@fao2023]. Episode ketiga di mana kekurangan produksi sebesar itu menghasilkan kenaikan harga yang secara proporsional lebih kecil, tanpa perubahan kebijakan perdagangan, akan melawan bab ini.

Klaim tentang pembiayaan antisipatif difalsifikasi lewat perbandingan terkendali: rumah tangga yang menerima transfer sebelum panen seharusnya tidak berbeda dari rumah tangga sebanding yang menerima jumlah sama sesudah panen. Kalau waktunya tidak membuat perbedaan pada konsumsi, aset, atau penjualan aset terpaksa, klaimnya kosong. Uji ini sudah dijalankan di beberapa tempat dan hasilnya cukup campuran sehingga bab ini harus dibaca sebagai menyatakan mekanisme yang masuk akal, bukan efek yang sudah mapan [@fao2019].""",
    "08": """Bab ini berargumen bahwa penyakit yang peka iklim terutama merupakan fungsi infrastruktur kesehatan dan air, bahwa perubahan iklim adalah salah satu penggerak di antara beberapa, dan bahwa investasi infrastruktur generik melindungi lebih baik daripada kampanye khusus penyakit.

Falsifikasinya adalah dekomposisi varians antartempat. Ambil insiden demam berdarah atau kolera per distrik, bersama variabel iklim (suhu, curah hujan), variabel infrastruktur (cakupan air perpipaan, sanitasi, kapasitas surveilans), dan pendapatan. Bab ini salah kalau variabel iklim menjelaskan sebagian besar varians antardistrik dan infrastruktur menambah sedikit setelah iklim dikendalikan.

Bukti saat ini mengarah sebaliknya: distrik dengan iklim serupa dan sistem air serta surveilans berbeda memiliki beban yang sangat berbeda, dan lonjakan demam berdarah 2024 mengikuti kapasitas sistem kesehatan sebesar suhu [@mordecai2020; @who2023dengue]. Distrik yang menyamai kembaran iklimnya dalam hal insiden, meskipun infrastrukturnya menyimpang selama satu dekade, akan membantah klaim ini.

Klaim tentang investasi generik bisa diuji lewat uji coba: program air bersih atau sanitasi seharusnya menurunkan penyakit yang peka iklim lebih banyak per dolar daripada kampanye pengendalian vektor di tempat yang sama. Kalau belanja kampanye mengalahkan belanja infrastruktur pada kondisi sebanding, kesimpulan kebijakan bab ini salah meskipun diagnosisnya benar.""",
    "09": """Bab ini berargumen bahwa arsitektur keuangan respons bencana berpihak pada yang tercatat dan yang diasuransikan, datang setelah keputusan yang menentukan pemulihan, dan meninggalkan kategori kerugian besar yang tidak tertutup.

Falsifikasinya adalah uji distribusional dengan pembanding. Ambil transfer pascabencana per rumah tangga dan bandingkan dengan kerugian per rumah tangga. Kalau transfer proporsional terhadap kerugian — terlepas dari sertifikat tanah, pendapatan, dokumen, atau asuransi — bab ini salah. Versi terukurnya: regresikan penerimaan transfer terhadap kerugian yang dinilai dan terhadap status kepemilikan lahan. Bab ini memprediksi koefisien positif pada kepemilikan yang bertahan setelah kerugian dikendalikan, dan koefisien negatif pada sektor informal.

Temuannya konsisten lintas negara dan jenis peristiwa, yang membuat klaimnya kuat sekaligus membuat satu lawan-contoh yang bersih menjadi menentukan [@undrr2022]. Negara dengan sistem registrasi presumtif yang berfungsi dan membayar penghuni informal sebanding kerugian mereka akan menjadi lawan-contoh itu, dan bab ini seharusnya menyebutnya kalau ada.

Klaim tentang waktu difalsifikasi dengan tanggal: kalau median transfer rumah tangga tiba sebelum median keputusan pemulihan rumah tangga — keputusan untuk membangun ulang, pindah, atau berutang — klaimnya gugur. Itu terukur dari catatan pembayaran dan tanggal survei, dan jarang diukur, yang dengan sendirinya adalah bagian dari argumennya.""",
    "13": """Bab ini berargumen bahwa perpindahan tak terhindarkan di sejumlah tempat, bahwa relokasi terencana gagal bila mengabaikan mata pencaharian dan jaringan, dan bahwa syarat perpindahan harus dinegosiasikan sebelum lokasi menjadi tak layak huni.

Falsifikasinya adalah perbandingan tindak lanjut. Ambil skema relokasi dengan dukungan mata pencaharian terdokumentasi dan skema tanpa dukungan, dipasangkan pada paparan bahaya dan jarak pindah, lalu bandingkan pendapatan rumah tangga, pekerjaan, dan tingkat kembali tiga sampai lima tahun setelah pindah. Bab ini salah kalau skema berdampingan tidak berkinerja lebih baik daripada yang tanpa dukungan, setelah pendapatan sebelum pindah dikendalikan.

Bukti dari Fiji dan Vietnam berpihak pada bab ini, dan tipis: jumlah relokasi terdokumentasi baik dengan data tindak lanjut cukup kecil sehingga satu studi yang dijalankan rapi bisa menggeser kesimpulannya [@iom2023]. Itulah keadaan klaimnya secara jujur.

Klaim tentang waktu bisa diuji terhadap catatan proses: skema yang syaratnya disepakati sebelum lokasi tak layak huni seharusnya menunjukkan tingkat perpindahan sekunder — rumah tangga pindah lagi dalam lima tahun — lebih rendah daripada skema yang dinegosiasikan dalam kondisi darurat. Kalau tingkatnya sama, kesimpulan kebijakan bab ini salah.""",
    "14": """Bab ini berargumen bahwa dua ketidaksetaraan iklim itu berbeda, bahwa basis akuntansi menentukan kesimpulan politik, dan bahwa ketidakadilan domestik melemahkan keefektifan adaptasi.

Klaim pertama difalsifikasi dengan menunjukkan bahwa dua distribusi itu berimpit: bahwa negara dengan emisi kumulatif terbesar juga, dalam urutan peringkat, negara dengan kerugian iklim per kapita tertinggi. Keduanya jelas tidak berimpit di puncak — penghasil emisi terbesar bukan yang paling menderita — tetapi demonstrasi bahwa korelasinya mendekati satu di seluruh distribusi akan meruntuhkan pembedaan ini.

Klaim kedua bersifat aritmetis dan politis sekaligus: ubah basis akuntansi, berubahlah peringkat kewajiban. Itu bisa diperiksa, dan kotak di buku ini mengerjakan aritmetikanya; basis yang membiarkan peringkat kewajiban tidak berubah di semua pilihan yang masuk akal akan membantah klaim ini [@matthews2015; @heede2014].

Klaim ketiga adalah yang paling mungkin salah, dan falsifikasinya adalah perbandingan program. Kalau belanja adaptasi yang terdistribusi regresif — terkonsentrasi pada yang lebih mampu — menghasilkan penurunan kerentanan yang sama dengan jumlah yang sama yang terdistribusi progresif, maka keadilan tidak punya efek mandiri pada keefektifan dan klaimnya gugur. Bukti tentang kerja sama dan kepatuhan mengarah sebaliknya, tetapi tidak langsung, sebagian besar dari konteks selain adaptasi iklim, dan bab ini harus dibaca sebagai mengargumenkan mekanisme, bukan melaporkan efek terukur [@tol2018].""",
    "16": """Bab ini berargumen bahwa kapasitas adaptif kota ditentukan oleh dana pemeliharaan, aturan tata guna lahan, dan koordinasi, bukan oleh besarnya rencana iklim atau satu proyek infrastruktur tunggal.

Falsifikasinya adalah uji prediksi. Ambil kota dengan rencana iklim terbit dan kota tanpa, atau kota dengan catatan pemeliharaan kuat dan lemah, lalu bandingkan hasil pada peristiwa nyata: kematian, hari gangguan layanan, dan kerusakan per satuan nilai terpapar. Bab ini salah kalau besarnya rencana memprediksi hasil lebih baik daripada rasio pemeliharaan — porsi anggaran infrastruktur yang dibelanjakan untuk perawatan — setelah pendapatan kota dikendalikan.

Versi terukur dari klaim bab ini adalah perbandingan koefisien: dalam regresi hasil peristiwa terhadap kedua variabel, koefisien terstandardisasi pada pemeliharaan seharusnya melebihi koefisien pada belanja rencana. Sejauh yang diketahui buku ini, uji itu belum dijalankan lintas sampel kota; bukti bab ini berbasis kasus, dari kegagalan drainase dan penegakan tata guna lahan [@bubeck2017; @flyvbjerg2014]. Kota dengan rencana besar, tanpa pemeliharaan, dan hasil baik pada peristiwa nyata akan menjadi lawan-contohnya, dan ia harus disebut.

Klaim tentang rutinitas difalsifikasi lewat audit: kalau kota yang mengubah jadwal pemeliharaan dan peninjauan izin tidak menunjukkan perbaikan hasil dibanding kota yang hanya menerbitkan rencana, mekanismenya salah.""",
    "17": """Bab ini adalah seperangkat uji, bukan argumen, jadi pertanyaan falsifikasinya berbeda: apa yang akan menunjukkan bahwa ujinya salah?

Uji pertama adalah kalibrasi. Kalau klaim yang lolos tujuh pertanyaan ternyata tidak lebih akurat, rata-rata, daripada klaim yang gagal, ujinya tidak berharga. Itu terukur: ambil sampel klaim iklim, terapkan ujinya, lalu nilai klaim itu terhadap apa yang kemudian terjadi. Literatur peramalan menunjukkan penalaran terstruktur memperbaiki akurasi secara sederhana dan konsisten, tetapi efeknya cukup kecil sehingga hasil nol pada sampel khusus iklim akan melawan bab ini [@tetlock2015].

Uji kedua adalah kegunaan. Kalau pembaca tanpa pelatihan iklim tidak bisa menerapkan uji satu, dua, dan empat pada artikel koran setelah membaca bab ini, ujinya gagal sebagai alat rujukan terlepas dari validitasnya. Itu bisa diuji dengan percobaan kecil: berikan bab ini kepada dua kelompok, berikan artikelnya kepada keduanya, dan bandingkan mutu penilaian tertulis mereka.

Uji ketiga adalah uji buku ini sendiri. Pembaca yang menerapkan tujuh pertanyaan pada buku ini seharusnya menemukan setidaknya satu tempat di mana buku ini gagal memenuhi standarnya sendiri. Kalau buku ini lolos ketujuh-tujuhnya dengan bersih, ujinya terlalu lemah — seperangkat pertanyaan yang tidak pernah menggigit adalah hiasan. Titik terlemahnya adalah seksi falsifikasi bab-bab sebelumnya: beberapa di antaranya menyatakan arah tanpa ambang, dan pembaca berhak mencatatnya sebagai kekurangan [@gaillard2019].""",
    "15": """Bab ini berargumen bahwa persiapan rumah tangga bernilai tetapi terbatas, bahwa kontak sosial adalah intervensi rumah tangga dengan nilai tertinggi, dan bahwa model kesiapsiagaan komersial salah mengalokasikan perhatian.

Falsifikasinya adalah perbandingan tingkat rumah tangga dengan variabel hasil. Ambil rumah tangga yang terpapar peristiwa sama, dengan inventaris peralatan dan ukuran kontak sosial yang dicatat sebelumnya, lalu bandingkan hasil sesudahnya: cedera, kerusakan properti, hari mengungsi, dan waktu pemulihan. Bab ini salah kalau peralatan memprediksi hasil lebih baik daripada kontak, setelah pendapatan dan paparan bahaya dikendalikan.

Bukti panas adalah bagian terkuat dari kasus ini sekaligus yang paling sempit: ia berasal dari kematian, di mana hasilnya tidak ambigu [@bccoroners2022; @klinenberg2002]. Untuk banjir dan badai buktinya lebih lemah, dan studi yang menemukan rumah tangga berperalatan lengkap tetapi terisolasi pulih lebih cepat daripada yang terhubung akan membantah klaim ini untuk bahaya tersebut.

Klaim tentang model komersial difalsifikasi lewat harga dan efek sekaligus: kalau peralatan yang dijual ke rumah tangga memberikan pengurangan risiko terukur per dolar yang sebanding dengan tindakan sosial, tuduhan salah alokasi gugur. Perbandingan itu hampir tidak pernah dibuat, yang karena itu bab ini menyatakannya sebagai argumen, bukan temuan.""",
}

HEAD_EN = "## What would prove this chapter wrong"
HEAD_ID = "## Apa yang akan membuktikan bab ini salah"


def ganti(path: pathlib.Path, judul: str, baru: str) -> bool:
    t = path.read_text(encoding="utf-8")
    pola = re.compile(r"(?m)^" + re.escape(judul) + r"\s*\n(.*?)(?=^## |\Z)", re.S)
    m = pola.search(t)
    if not m:
        return False
    t = t[: m.start(1)] + "\n" + baru.strip() + "\n\n" + t[m.end(1):]
    path.write_text(t, encoding="utf-8")
    return True


def main() -> int:
    gagal = 0
    for k, isi in TUJUAN.items():
        f = next(EN.glob(f"{k}-*.md"))
        if not ganti(f, HEAD_EN, isi):
            print(f"GAGAL EN {k}"); gagal += 1
    for k, isi in INDO.items():
        f = next(ID_.glob(f"{k}-*.md"))
        if not ganti(f, HEAD_ID, isi):
            print(f"GAGAL ID {k}"); gagal += 1
    print("selesai; gagal:", gagal)
    return gagal


if __name__ == "__main__":
    raise SystemExit(main())
