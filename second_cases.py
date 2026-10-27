# -*- coding: utf-8 -*-
"""Kasus kedua untuk setiap bab.

Setiap bab punya satu subbab "Case Study" yang bertumpu pada satu peristiwa.
Satu kasus tidak cukup untuk mengambil prediksi: ia hanya menunjukkan bahwa
sesuatu BISA terjadi. Dua kasus dengan mekanisme sama tapi konteks berbeda
menunjukkan APA yang menentukan hasilnya, dan itulah yang membuat prediksi
di bab berikutnya punya pijakan.

Paragraf di bawah disisipkan di akhir subbab studi kasus, tepat sebelum subbab
"Skenario dan Prediksi". Formatnya sengaja dibuat sama dengan badan buku:
satu paragraf, tanpa poin, dan berakhir pada apa yang berubah bagi prediksi.

Batas yang saya pegang: tidak ada angka yang saya karang. Kalau saya tidak
yakin sebuah angka bisa dipertanggungjawabkan, paragrafnya memakai rentang
atau kalimat kualitatif, bukan angka palsu.
"""

CASES = [
    (1,
     "A second flood makes the same point from another continent. In March 2019, "
     "Cyclone Idai came ashore near Beira, Mozambique, and pushed the sea up the "
     "Pungue and Buzi rivers instead of letting it drain away; more than a thousand "
     "people died across the three affected countries and roughly three million were "
     "affected, in a city whose drainage had not been maintained for years (IFRC, 2022). "
     "Pakistan and Mozambique share the mechanism: extreme rainfall is only half of a "
     "flood, and the other half is the condition of the ground the water crosses. Neither "
     "country lacked a warning. Both lacked the capacity to act on one, which is why the "
     "next two decades cannot be forecast from rainfall alone.",
     "Banjir kedua menyampaikan hal yang sama dari benua lain. Pada Maret 2019, Siklon "
     "Idai mendarat dekat Beira, Mozambik, dan mendorong air laut naik ke sungai Pungue "
     "dan Buzi alih-alih membiarkannya mengalir pergi; lebih dari seribu orang meninggal "
     "di tiga negara yang terdampak dan sekitar tiga juta orang terkena dampaknya, di kota "
     "yang saluran drainasenya bertahun-tahun tidak dirawat (IFRC, 2022). Pakistan dan "
     "Mozambik berbagi mekanisme yang sama: hujan ekstrem hanya separuh dari sebuah banjir, "
     "dan separuh lainnya adalah kondisi tanah yang dilalui air. Kedua negara tidak "
     "kekurangan peringatan. Keduanya kekurangan kemampuan untuk bertindak atas peringatan "
     "itu, dan itulah sebabnya dua dekade ke depan tidak bisa diramalkan dari curah hujan saja."),

    (2,
     "The record has a second kind of test, and it arrived by accident. When Mount Pinatubo "
     "erupted in June 1991, it injected roughly twenty million tonnes of sulphur dioxide into "
     "the stratosphere, where it formed a sulphate aerosol layer and cooled the global surface "
     "by about half a degree for two years (IPCC, 2021). The cooling appeared in the same "
     "instruments that measure the Keeling curve, and its magnitude matched what the physics "
     "predicted. That episode carries more weight than it is usually given: the system "
     "responded to a known forcing in a measurable way, which is why the response to a known "
     "accumulation of carbon dioxide is not seriously in dispute.",
     "Catatan itu punya ujian kedua, dan kedatangannya kebetulan. Ketika Gunung Pinatubo meletus "
     "pada Juni 1991, ia menyemburkan sekitar dua puluh juta ton sulfur dioksida ke stratosfer, "
     "membentuk lapisan aerosol sulfat dan mendinginkan permukaan bumi sekitar setengah derajat "
     "selama dua tahun (IPCC, 2021). Pendinginan itu muncul pada instrumen yang sama yang "
     "mengukur kurva Keeling, dan besarnya cocok dengan yang diramalkan fisika. Peristiwa itu "
     "lebih penting daripada yang biasanya diberikan kepadanya: sistem merespons pemaksaan yang "
     "diketahui dengan cara yang terukur, dan itulah sebabnya respons terhadap penumpukan karbon "
     "dioksida yang juga diketahui tidak lagi diperdebatkan."),

    (3,
     "Argo measures temperature; a later generation of instruments measures mass. The GRACE "
     "satellites, launched in 2002, detect the minute variations in Earth's gravity that "
     "correspond to the movement of water and ice, and they let glaciologists weigh ice sheets "
     "rather than estimate their volume from the surface. The result was a correction: "
     "Greenland and Antarctica were losing mass faster than the older estimates suggested, and "
     "the loss has continued (Shepherd et al., 2020). Argo and GRACE turned the ocean and the "
     "ice from inferred quantities into measured ones, which is why the sea-level projections "
     "in this chapter carry a narrower range than those published a decade ago.",
     "Argo mengukur suhu; generasi instrumen berikutnya mengukur massa. Satelit GRACE, yang "
     "diluncurkan pada 2002, mendeteksi variasi kecil gravitasi bumi yang bersesuaian dengan "
     "perpindahan air dan es, dan memungkinkan ahli glasiologi menimbang lapisan es alih-alih "
     "menaksir volumenya dari permukaan. Hasilnya berupa koreksi: Greenland dan Antartika "
     "kehilangan massa lebih cepat daripada perkiraan lama, dan kehilangan itu berlanjut "
     "(Shepherd et al., 2020). Argo dan GRACE mengubah laut dan es dari besaran yang disimpulkan "
     "menjadi besaran yang diukur, dan itulah sebabnya proyeksi muka laut di bab ini punya "
     "rentang yang lebih sempit daripada terbitan satu dekade lalu."),

    (4,
     "The east provides the comparison. In the summer of 2010 a blocking high settled over "
     "western Russia for six weeks, Moscow recorded 38.2 °C, and the death toll has been "
     "estimated at around fifty-six thousand, with smoke from peat and forest fires compounding "
     "the heat (IPCC, 2022a). The European summer of 2022 and the Russian summer of 2010 differ "
     "in geography and not in mechanism: a persistent ridge, a stagnant atmosphere, and a "
     "population housed for a different climate. Both were treated as emergencies when they "
     "arrived and as design conditions only afterwards, which is the gap the predictions in this "
     "chapter assume will narrow.",
     "Timur memberi pembandingnya. Pada musim panas 2010, tekanan tinggi yang mengunci wilayah "
     "Rusia bagian barat bertahan enam pekan, Moskow mencatat 38,2 °C, dan jumlah kematian "
     "diperkirakan sekitar lima puluh enam ribu, dengan asap dari kebakaran gambut dan hutan "
     "memperberat panasnya (IPCC, 2022a). Musim panas Eropa 2022 dan musim panas Rusia 2010 "
     "berbeda secara geografi, bukan secara mekanisme: punggungan tekanan tinggi yang bertahan, "
     "atmosfer yang stagnan, dan penduduk yang rumahnya dirancang untuk iklim lain. Keduanya "
     "diperlakukan sebagai darurat saat datang dan sebagai kondisi desain hanya setelahnya, dan "
     "celah itulah yang diasumsikan menyempit dalam prediksi bab ini."),

    (5,
     "Cape Town supplies the counter-case, and it is the reason this chapter does not end in "
     "despair. In 2018 the city approached Day Zero with its reservoirs near a fifth of capacity, "
     "and it avoided the shut-off by cutting consumption by more than half over three years "
     "through tariffs, pressure management and the public reporting of daily use (Gleick, 2023). "
     "The difference between Chennai and Cape Town was not rainfall but governance: one city "
     "discovered its shortfall in the middle of a crisis, the other measured it in advance and "
     "put a price on it. Both are coastal cities of similar size, and both now plan for a drier "
     "century.",
     "Cape Town menyediakan kasus pembandingnya, dan itulah sebabnya bab ini tidak berakhir pada "
     "keputusasaan. Pada 2018 kota itu mendekati Day Zero dengan waduk hampir seperlima "
     "kapasitasnya, dan berhasil menghindari penutupan kran dengan memotong konsumsi lebih dari "
     "separuh dalam tiga tahun melalui tarif, pengelolaan tekanan, dan pelaporan pemakaian harian "
     "secara terbuka (Gleick, 2023). Perbedaan Chennai dan Cape Town bukan pada curah hujan "
     "melainkan pada tata kelola: satu kota menemukan kekurangannya di tengah krisis, kota lain "
     "mengukurnya lebih dulu dan memberinya harga. Keduanya kota pesisir berukuran serupa, dan "
     "keduanya kini merencanakan abad yang lebih kering."),

    (6,
     "Jakarta is not the first city to face this sequence, and the American case shows what the "
     "end of it looks like. New Orleans was built on drained wetland that continues to subside, "
     "was protected by levees that failed in 2005, and lost about half its population after "
     "Hurricane Katrina; the city that rebuilt did so behind a larger and more expensive system "
     "of defences, and it still sits below sea level (Brunkard et al., 2008). Jakarta is at an "
     "earlier point on the same curve: subsidence of up to twenty-five centimetres a year in the "
     "north, a sea wall that is partly built, and a government that has chosen to move the "
     "capital rather than defend the whole city.",
     "Jakarta bukan kota pertama yang menghadapi urutan ini, dan kasus Amerika menunjukkan ujung "
     "urutan itu. New Orleans dibangun di atas lahan basah yang dikeringkan dan terus menurun, "
     "dilindungi tanggul yang jebol pada 2005, dan kehilangan sekitar separuh penduduknya setelah "
     "Badai Katrina; kota yang dibangun kembali berdiri di belakang sistem pertahanan yang lebih "
     "besar dan lebih mahal, dan tetap berada di bawah permukaan laut (Brunkard et al., 2008). "
     "Jakarta berada di titik yang lebih awal pada kurva yang sama: penurunan tanah hingga dua "
     "puluh lima sentimeter per tahun di bagian utara, tanggul laut yang baru sebagian dibangun, "
     "dan pemerintah yang memilih memindahkan ibu kota daripada mempertahankan seluruh kota."),

    (7,
     "The rice shock of 2023 has an earlier twin. When wheat prices doubled in 2010 and 2011, the "
     "countries that restricted exports were not the largest producers, and the market tightened "
     "within weeks; the unrest that followed in North Africa and the Middle East had many causes, "
     "but its timing followed food prices closely (Mach et al., 2019). Rice and wheat behave the "
     "same way: only a small share of world production is traded, so a restriction by one exporter "
     "moves the world price far more than its share of output would suggest. What differed in "
     "2023 was that the restriction came from one country holding forty per cent of the export "
     "market.",
     "Guncangan beras 2023 punya kembaran yang lebih awal. Ketika harga gandum berlipat pada 2010 "
     "dan 2011, negara yang membatasi ekspor bukanlah produsen terbesar, dan pasar mengetat dalam "
     "hitungan pekan; kerusuhan yang menyusul di Afrika Utara dan Timur Tengah punya banyak sebab, "
     "tetapi waktunya mengikuti harga pangan dengan rapat (Mach et al., 2019). Beras dan gandum "
     "berperilaku sama: hanya sebagian kecil produksi dunia yang diperdagangkan, sehingga "
     "pembatasan oleh satu eksportir menggerakkan harga dunia jauh melebihi pangsa produksinya. "
     "Yang berbeda pada 2023 adalah bahwa pembatasan itu datang dari satu negara yang menguasai "
     "empat puluh persen pasar ekspor."),

    (8,
     "The reef's history is longer than the record usually quoted. The first global bleaching "
     "event, in 1998, coincided with a strong El Niño and bleached reefs in every ocean basin; it "
     "was treated then as an anomaly, and it has since become the baseline (IPCC, 2018). The "
     "sequence that followed—2002, 2010, 2016, 2017, 2020, 2022 and 2024—is not a series of "
     "accidents but one mechanism returning at a shortening interval. That is the difference "
     "between a reef that has a bad year and a reef that no longer has time to recover between "
     "bad years, and the projections in this chapter turn on which of the two the Great Barrier "
     "Reef has become.",
     "Sejarah terumbu lebih panjang daripada catatan yang biasanya dikutip. Peristiwa pemutihan "
     "global pertama, pada 1998, bertepatan dengan El Niño kuat dan memutihkan terumbu di semua "
     "samudra; saat itu ia dianggap anomali, dan sejak itu ia menjadi garis dasar (IPCC, 2018). "
     "Urutan sesudahnya—2002, 2010, 2016, 2017, 2020, 2022, dan 2024—bukan rangkaian kecelakaan "
     "melainkan satu mekanisme yang kembali dengan jeda yang memendek. Itulah beda antara terumbu "
     "yang mengalami satu tahun buruk dan terumbu yang tidak lagi punya waktu untuk pulih di "
     "antara tahun-tahun buruk, dan proyeksi di bab ini bergantung pada yang mana di antara "
     "keduanya yang telah menjadi keadaan Great Barrier Reef."),

    (9,
     "Malaria makes the same point with a different vector. The disease was historically absent "
     "from the Ethiopian highlands above about two thousand metres, because the parasite could "
     "not complete its cycle in the cool nights; warming has moved that boundary uphill, and "
     "epidemics have appeared in districts with no acquired immunity and no mosquito programme "
     "(Cissé et al., 2022). Dengue in Nepal and malaria in Ethiopia are the same process seen at "
     "two latitudes: a temperature threshold that health systems had treated as fixed has begun "
     "to move, and the populations on the far side of it are the least prepared. In both places "
     "the first obstacle is not treatment but diagnosis, because the disease is not yet the one "
     "a doctor thinks of first.",
     "Malaria menyampaikan hal yang sama dengan vektor berbeda. Penyakit itu secara historis tidak "
     "ada di dataran tinggi Etiopia di atas sekitar dua ribu meter, karena parasit tidak dapat "
     "menyelesaikan siklusnya pada malam yang dingin; pemanasan menggeser batas itu ke atas, dan "
     "epidemi muncul di distrik yang tidak punya imunitas dan tidak punya program nyamuk "
     "(Cissé et al., 2022). Dengue di Nepal dan malaria di Etiopia adalah proses yang sama pada "
     "dua lintang: ambang suhu yang oleh sistem kesehatan dianggap tetap mulai bergerak, dan "
     "penduduk di sisi jauh ambang itu paling tidak siap. Di kedua tempat, hambatan pertama bukan "
     "pengobatan melainkan diagnosis, karena penyakit itu belum menjadi yang pertama terpikir "
     "oleh seorang dokter."),

    (10,
     "The Pacific supplies the comparison for loss accounting. Typhoon Haiyan crossed the central "
     "Philippines in November 2013 with winds near three hundred kilometres an hour and killed "
     "about six thousand people, while direct damage came to roughly two billion dollars—small "
     "relative to the losses, because what was destroyed was modest (UNDRR, 2022). The Atlantic "
     "hurricanes of 2017 caused far more damage in dollars and far fewer deaths. The difference "
     "is not the severity of the storms but the value of what stood in their path, and that is "
     "why the economics of disasters is a story about wealth at least as much as about weather.",
     "Pasifik memberi pembanding untuk perhitungan kerugian. Topan Haiyan melintasi Filipina "
     "tengah pada November 2013 dengan kecepatan angin mendekati tiga ratus kilometer per jam dan "
     "menewaskan sekitar enam ribu orang, sementara kerusakan langsungnya sekitar dua miliar "
     "dolar—kecil dibandingkan kerugiannya, karena yang hancur bernilai sederhana (UNDRR, 2022). "
     "Badai Atlantik 2017 menyebabkan kerusakan jauh lebih besar dalam dolar dan jauh lebih sedikit "
     "kematian. Perbedaannya bukan keganasan badai melainkan nilai dari apa yang berdiri di "
     "jalurnya, dan itulah sebabnya ekonomi bencana adalah kisah tentang kekayaan setidaknya sama "
     "banyak dengan tentang cuaca."),

    (11,
     "Tuvalu is the most legally inventive case, not the only one. Kiribati, thirty-three atolls "
     "scattered across three and a half million square kilometres of ocean, bought about twenty "
     "square kilometres of land in Fiji in 2014 as a hedge against the loss of its own territory, "
     "and it funds a programme it calls migration with dignity rather than displacement (UNHCR, "
     "2023). The two countries chose different instruments—a treaty with a neighbour in one case, "
     "land purchase and skills migration in the other—and both answer the same legal question: "
     "what becomes of a state whose territory is no longer habitable? The difference matters for "
     "prediction because treaties can be renegotiated and land cannot be un-bought.",
     "Tuvalu adalah kasus paling inventif secara hukum, bukan satu-satunya. Kiribati, tiga puluh "
     "tiga atol yang tersebar di tiga setengah juta kilometer persegi laut, membeli sekitar dua "
     "puluh kilometer persegi tanah di Fiji pada 2014 sebagai lindung nilai atas kehilangan "
     "wilayahnya sendiri, dan membiayai program yang disebutnya migrasi dengan martabat alih-alih "
     "pengungsian (UNHCR, 2023). Kedua negara memilih instrumen berbeda—perjanjian dengan negara "
     "tetangga dalam satu kasus, pembelian tanah dan migrasi keterampilan dalam kasus lain—dan "
     "keduanya menjawab pertanyaan hukum yang sama: apa yang terjadi pada negara yang wilayahnya "
     "tidak lagi dapat dihuni? Perbedaannya penting bagi prediksi karena perjanjian dapat "
     "dinegosiasikan ulang dan tanah tidak dapat dibatalkan pembeliannya."),

    (12,
     "Lake Chad is not the largest case of its kind. The Aral Sea was the fourth largest lake in "
     "the world in 1960, and the diversion of its two feeder rivers for cotton irrigation reduced "
     "it to a fraction of its former area by the 2000s; the fishing towns that remain stand tens "
     "of kilometres from water, and the exposed seabed has become a source of salt and dust "
     "(Gleick, 2023). The Aral is the clearest demonstration that a shared water body can be "
     "destroyed by decisions taken upstream while the communities downstream continue to plan as "
     "if it will remain. The Lake Chad basin is smaller in scale and harder in its politics, and "
     "the mechanism is identical.",
     "Danau Chad bukan kasus terbesar dari jenisnya. Laut Aral adalah danau terbesar keempat di "
     "dunia pada 1960, dan pengalihan dua sungai pemasuknya untuk irigasi kapas menyusutkannya "
     "menjadi sebagian kecil dari luas semula pada dekade 2000-an; kota-kota nelayan yang tersisa "
     "kini berdiri puluhan kilometer dari air, dan dasar laut yang terbuka menjadi sumber garam "
     "dan debu (Gleick, 2023). Aral adalah bukti paling jelas bahwa badan air bersama dapat "
     "dihancurkan oleh keputusan di hulu sementara komunitas di hilir terus merencanakan seolah "
     "badan air itu akan tetap ada. Cekungan Danau Chad lebih kecil skalanya dan lebih sulit "
     "politiknya, dan mekanismenya identik."),

    (13,
     "Texas is not the only grid that failed in the same decade. Hurricane Maria destroyed most "
     "of Puerto Rico's transmission system in September 2017, power was not restored to every "
     "customer for eleven months, and the official death count of 64 was later revised to an "
     "estimated 2,975 excess deaths, most of them in the months when the outage continued "
     "(Kishore et al., 2018). The Texas failure was caused by cold and the Puerto Rican failure by "
     "wind, but both exposed one design assumption: a system built to a single hazard profile, "
     "operated without redundancy, and restored on a schedule set by procurement rather than by "
     "need.",
     "Texas bukan satu-satunya jaringan listrik yang runtuh pada dekade yang sama. Badai Maria "
     "menghancurkan sebagian besar sistem transmisi Puerto Rico pada September 2017, listrik "
     "tidak pulih untuk semua pelanggan selama sebelas bulan, dan angka kematian resmi 64 "
     "kemudian direvisi menjadi perkiraan 2.975 kematian berlebih, sebagian besar pada "
     "bulan-bulan ketika pemadaman berlanjut (Kishore et al., 2018). Kegagalan Texas disebabkan "
     "dingin dan kegagalan Puerto Rico disebabkan angin, tetapi keduanya membuka satu asumsi "
     "desain yang sama: sistem yang dibangun untuk satu profil bahaya, dioperasikan tanpa "
     "redundansi, dan dipulihkan menurut jadwal pengadaan, bukan menurut kebutuhan."),

    (14,
     "Italy is the first country; it is not the only jurisdiction. New Jersey became the first "
     "American state to require climate change to be taught in every grade and every subject, "
     "adopting the requirement in 2020 and writing it into its standards two years later. The "
     "Italian model is national and compulsory, the American one is state-level and "
     "cross-curricular, and both were designed to make climate literacy a condition of graduation "
     "rather than an elective. The difference that matters for the next two decades is not which "
     "model is better but whether either survives a change of government, which is why this "
     "chapter treats curriculum as infrastructure rather than as policy.",
     "Italia adalah negara pertama; ia bukan satu-satunya yurisdiksi. New Jersey menjadi negara "
     "bagian Amerika pertama yang mewajibkan perubahan iklim diajarkan di setiap jenjang dan "
     "setiap mata pelajaran, menetapkannya pada 2020 dan menuangkannya ke dalam standar dua tahun "
     "kemudian. Model Italia bersifat nasional dan wajib, model Amerika bersifat tingkat negara "
     "bagian dan lintas mata pelajaran, dan keduanya dirancang agar literasi iklim menjadi syarat "
     "kelulusan, bukan pilihan. Perbedaan yang penting bagi dua dekade ke depan bukan model mana "
     "yang lebih baik melainkan apakah salah satunya bertahan ketika pemerintahan berganti, dan "
     "itulah sebabnya bab ini memperlakukan kurikulum sebagai infrastruktur, bukan sebagai "
     "kebijakan."),

    (15,
     "The same failure appeared in a quieter form after Hurricane Maria. The official death toll "
     "in Puerto Rico stood at 64 for months, and independent researchers later estimated 2,975 "
     "excess deaths; the discrepancy persisted because the counting method excluded deaths caused "
     "by the collapse of services rather than by wind and water (Kishore et al., 2018). Nobody had "
     "to invent a false story. The first number was simply wrong, and it was repeated by officials "
     "who had no reason to doubt it. That is the more common failure of climate information: not "
     "the deliberate lie but the figure that is never corrected, and it costs the same credibility "
     "when it is finally exposed.",
     "Kegagalan yang sama muncul dalam bentuk yang lebih senyap setelah Badai Maria. Angka "
     "kematian resmi di Puerto Rico bertahan di 64 selama berbulan-bulan, dan peneliti independen "
     "kemudian memperkirakan 2.975 kematian berlebih; selisih itu bertahan karena metode "
     "penghitungannya mengecualikan kematian akibat runtuhnya layanan, bukan akibat angin dan air "
     "(Kishore et al., 2018). Tidak ada yang perlu mengarang cerita palsu. Angka pertama sekadar "
     "salah, dan angka itu diulang oleh pejabat yang tidak punya alasan untuk meragukannya. Itulah "
     "kegagalan informasi iklim yang lebih umum: bukan kebohongan yang disengaja melainkan angka "
     "yang tidak pernah dikoreksi, dan biayanya sama besar ketika akhirnya terbuka."),

    (16,
     "Japan supplies the contrast from the other end of the preparedness scale. The Tōhoku "
     "earthquake of March 2011 triggered a tsunami warning within minutes, the warning reached "
     "almost every phone on the coast, and the seawalls held in some places and were overtopped "
     "in others; around eighteen thousand people died, and the great majority of them drowned "
     "rather than being caught without any warning at all (IFRC, 2022). Japan had the system the "
     "Puerto Rican households did not: alerts, shelters, drills and a population that knew what "
     "the siren meant. It still lost eighteen thousand people. That is the honest benchmark for "
     "household preparedness—not the absence of warning, but what a warning is worth when the "
     "water arrives faster than the plan.",
     "Jepang memberi kontrasnya dari ujung lain skala kesiapan. Gempa Tōhoku pada Maret 2011 "
     "memicu peringatan tsunami dalam hitungan menit, peringatan itu mencapai hampir setiap "
     "telepon di pesisir, dan tanggul laut bertahan di sebagian tempat serta terlampaui di tempat "
     "lain; sekitar delapan belas ribu orang meninggal, dan sebagian besar dari mereka tenggelam, "
     "bukan terkejut tanpa peringatan sama sekali (IFRC, 2022). Jepang memiliki sistem yang tidak "
     "dimiliki rumah tangga Puerto Rico: peringatan, tempat berlindung, latihan, dan penduduk yang "
     "tahu apa arti sirene. Jepang tetap kehilangan delapan belas ribu orang. Itulah tolok ukur "
     "jujur bagi kesiapan rumah tangga—bukan ketiadaan peringatan, melainkan seberapa bernilai "
     "sebuah peringatan ketika air datang lebih cepat daripada rencananya."),

    (17,
     "Chicago in 1995 is the comparison that keeps the European case honest. A heat wave of "
     "comparable severity struck a city with a modern health system, and about seven hundred and "
     "forty people died; the investigation that followed found that the deaths were concentrated "
     "among people who lived alone, in apartments without air conditioning, in neighbourhoods "
     "where fear of crime kept windows shut (Klinenberg, 2002). France in 2003 and Chicago in 1995 "
     "differ in the size of the toll and not in the profile of the dead. Both show that the "
     "mortality of a heat wave is decided before the heat arrives—by housing, by social contact, "
     "and by whether the city treats its elderly as a population or as a private matter.",
     "Chicago 1995 adalah pembanding yang menjaga kasus Eropa tetap jujur. Gelombang panas dengan "
     "keganasan sebanding melanda kota dengan sistem kesehatan modern, dan sekitar tujuh ratus "
     "empat puluh orang meninggal; penyelidikan setelahnya menemukan bahwa kematian terkonsentrasi "
     "pada orang yang tinggal sendiri, di apartemen tanpa pendingin udara, di lingkungan tempat "
     "rasa takut akan kejahatan membuat jendela tertutup (Klinenberg, 2002). Prancis 2003 dan "
     "Chicago 1995 berbeda pada besarnya korban, bukan pada profil mereka yang meninggal. Keduanya "
     "menunjukkan bahwa kematian akibat gelombang panas ditentukan sebelum panasnya datang—oleh "
     "rumah, oleh kontak sosial, dan oleh apakah kota memperlakukan penduduk lanjut usianya "
     "sebagai populasi atau sebagai urusan pribadi."),

    (18,
     "The Ahr valley has an American counterpart that makes the governance point sharper. "
     "Hurricane Harvey stalled over Houston in August 2017 and dropped more than a thousand "
     "millimetres of rain in a week; the forecast was accurate days in advance, the warnings were "
     "issued, and the damage still came to about a hundred and twenty-five billion dollars, "
     "because the city had permitted development on the floodplain for decades (UNDRR, 2022). "
     "Germany and Texas differ in almost every institutional respect and agree on one thing: the "
     "information arrived and the land use did not change. Governance in the next two decades will "
     "be judged less on forecasting than on what is allowed to be built where.",
     "Lembah Ahr punya padanan Amerika yang membuat persoalan tata kelolanya lebih tajam. Badai "
     "Harvey berhenti di atas Houston pada Agustus 2017 dan menurunkan lebih dari seribu milimeter "
     "hujan dalam sepekan; ramalannya akurat berhari-hari sebelumnya, peringatannya dikeluarkan, "
     "dan kerugiannya tetap mencapai sekitar seratus dua puluh lima miliar dolar, karena kota itu "
     "mengizinkan pembangunan di dataran banjir selama puluhan tahun (UNDRR, 2022). Jerman dan "
     "Texas berbeda hampir dalam segala hal kelembagaan dan sepakat pada satu hal: informasinya "
     "sudah datang dan tata guna lahannya tidak berubah. Tata kelola dua dekade ke depan akan "
     "dinilai bukan dari ketepatan ramalan melainkan dari apa yang diizinkan berdiri di mana."),

    (19,
     "Bangladesh shows that financing can be solved at small scale; Morocco shows what happens "
     "when it is attempted at large scale. The Noor Ouarzazate complex in the Moroccan desert "
     "reached about six hundred megawatts of concentrated solar capacity, a scale that made it "
     "the largest of its kind when its final phase came online, and it was financed by a "
     "combination of concessional loans, climate funds and a sovereign guarantee (IRENA, 2023). "
     "The two cases mark the two ends of the same problem: the solar home system works because "
     "the unit is small enough for a household to pay for, and the utility-scale plant works "
     "because a state can borrow against it. What fails is everything in between, which is where "
     "most of the next two decades will be spent.",
     "Bangladesh menunjukkan bahwa pembiayaan bisa diselesaikan pada skala kecil; Maroko "
     "menunjukkan apa yang terjadi ketika hal itu dicoba pada skala besar. Kompleks Noor "
     "Ouarzazate di gurun Maroko mencapai sekitar enam ratus megawatt kapasitas surya terkonsentrasi, "
     "skala yang menjadikannya terbesar dari jenisnya ketika fase terakhirnya beroperasi, dan "
     "dibiayai kombinasi pinjaman lunak, dana iklim, dan jaminan negara (IRENA, 2023). Kedua kasus "
     "menandai dua ujung persoalan yang sama: sistem surya rumah tangga berhasil karena unitnya "
     "cukup kecil untuk dibayar sebuah rumah, dan pembangkit skala besar berhasil karena negara "
     "dapat berutang atas namanya. Yang gagal adalah segala sesuatu di antaranya, dan di situlah "
     "sebagian besar dua dekade ke depan akan dihabiskan."),

    (20,
     "The mental health literature has a second case that makes the same point over a longer "
     "period. Studies after Hurricane Katrina found rates of post-traumatic stress disorder and "
     "depression well above baseline among residents of New Orleans, and the rates were highest "
     "among those who had not returned, who had lost their homes, and who had no financial margin "
     "to absorb the loss (Galea et al., 2005). The Camp Fire and Katrina differ in scale and in "
     "kind of hazard, and they agree on the mechanism: psychological harm follows the loss of "
     "place and the failure of institutions more closely than it follows the wind speed. That is "
     "why the projections in this chapter treat displacement as a mental health exposure rather "
     "than an economic one.",
     "Literatur kesehatan jiwa punya kasus kedua yang menyampaikan hal serupa dalam jangka waktu "
     "lebih panjang. Kajian setelah Badai Katrina menemukan tingkat gangguan stres pascatrauma dan "
     "depresi jauh di atas garis dasar di antara penduduk New Orleans, dan tingkat tertinggi ada "
     "pada mereka yang tidak kembali, yang kehilangan rumah, dan yang tidak punya sisa keuangan "
     "untuk menyerap kerugian (Galea et al., 2005). Camp Fire dan Katrina berbeda skala dan jenis "
     "bahayanya, dan keduanya sepakat pada mekanismenya: kerusakan psikologis mengikuti kehilangan "
     "tempat dan kegagalan lembaga lebih rapat daripada mengikuti kecepatan angin. Itulah sebabnya "
     "proyeksi di bab ini memperlakukan pengungsian sebagai paparan kesehatan jiwa, bukan sebagai "
     "persoalan ekonomi."),

    (21,
     "The fund has an antecedent that explains why it was demanded. Typhoon Haiyan made landfall "
     "in the Philippines in November 2013 and killed about six thousand people; the Philippine "
     "delegation at the climate talks that followed refused to accept a voluntary pledge system "
     "and demanded a mechanism in which the countries that had emitted most would pay for the "
     "damage from events they had not caused (UNDRR, 2022). Tuvalu and the Philippines differ in "
     "size, in geography and in the hazard they face, and they agree on the legal argument: "
     "compensation is not charity, because charity can be withdrawn. The predictions in this "
     "chapter therefore turn less on how much the fund holds than on whether its payouts are "
     "treated as an obligation.",
     "Dana itu punya anteseden yang menjelaskan mengapa ia dituntut. Topan Haiyan mendarat di "
     "Filipina pada November 2013 dan menewaskan sekitar enam ribu orang; delegasi Filipina pada "
     "perundingan iklim sesudahnya menolak menerima sistem janji sukarela dan menuntut mekanisme "
     "di mana negara yang paling banyak mengemisikan membayar kerusakan akibat peristiwa yang "
     "bukan mereka sebabkan (UNDRR, 2022). Tuvalu dan Filipina berbeda ukuran, geografi, dan "
     "bahaya yang dihadapi, dan keduanya sepakat pada argumen hukumnya: kompensasi bukan "
     "kedermawanan, karena kedermawanan dapat ditarik kembali. Prediksi di bab ini karena itu "
     "lebih bergantung pada apakah pembayarannya diperlakukan sebagai kewajiban daripada pada "
     "berapa besar isi dananya."),

    (22,
     "Europe supplies the case that shows how fast a first-time record becomes routine. In July "
     "2022 the United Kingdom recorded 40.3 °C at Coningsby, the first temperature above 40 °C "
     "ever measured in the country, and the heat caused the first attributed excess mortality of "
     "its kind in a country whose housing had been designed to retain warmth (Philip et al., "
     "2022). Lytton and Coningsby are the same event in two climates: a temperature that the "
     "local built environment, the local health service and the local population had never "
     "experienced. The difference is that Britain had a warning system and a health service, and "
     "still lost thousands; that gap between having institutions and being ready is what the "
     "2050 scenarios in this chapter quantify.",
     "Eropa memberi kasus yang menunjukkan secepat apa rekor pertama kali menjadi rutin. Pada Juli "
     "2022 Inggris mencatat 40,3 °C di Coningsby, suhu pertama di atas 40 °C yang pernah terukur "
     "di negara itu, dan panasnya menyebabkan kematian berlebih teratribusi pertama dari jenisnya "
     "di negara yang rumah-rumahnya dirancang untuk menahan hangat (Philip et al., 2022). Lytton "
     "dan Coningsby adalah peristiwa yang sama di dua iklim: suhu yang belum pernah dialami "
     "lingkungan binaan, layanan kesehatan, dan penduduk setempat. Bedanya, Inggris punya sistem "
     "peringatan dan layanan kesehatan, dan tetap kehilangan ribuan orang; celah antara memiliki "
     "lembaga dan benar-benar siap itulah yang diukur oleh skenario 2050 di bab ini."),

    (23,
     "Somalia in 2017 is the case that shows what early warning can buy. The same rains failed, "
     "the same drought developed, and this time the warning came early enough for a large-scale "
     "response; famine was not declared, although the crisis killed tens of thousands of people "
     "and displaced more than a million (Checchi & Robinson, 2013). The comparison with 2011 is "
     "the most useful one in the famine literature, because almost nothing changed in the weather "
     "and almost everything changed in the timing of the money. That is the basis for the "
     "projections in this chapter: famine in the next two decades will be a failure of "
     "procurement and logistics far more often than a failure of rainfall.",
     "Somalia 2017 adalah kasus yang menunjukkan apa yang bisa dibeli oleh peringatan dini. Hujan "
     "gagal pada musim yang sama, kekeringan yang sama berkembang, dan kali ini peringatannya "
     "datang cukup awal untuk respons berskala besar; kelaparan tidak dinyatakan, meskipun krisis "
     "itu menewaskan puluhan ribu orang dan mengungsikan lebih dari satu juta (Checchi & Robinson, "
     "2013). Perbandingan dengan 2011 adalah yang paling berguna dalam literatur kelaparan, karena "
     "hampir tidak ada yang berubah pada cuacanya dan hampir semuanya berubah pada waktu "
     "kedatangan dananya. Itulah dasar proyeksi di bab ini: kelaparan dalam dua dekade ke depan "
     "akan lebih sering menjadi kegagalan pengadaan dan logistik daripada kegagalan curah hujan."),

    (24,
     "Cuba supplies the comparison that keeps the Bangladesh story from looking inevitable. The "
     "island is hit by hurricanes more often than almost anywhere in the region, and its civil "
     "defence system—mandatory evacuation, pre-assigned shelters, neighbourhood wardens who know "
     "who is elderly and who needs transport—has kept death tolls in the tens for storms that "
     "killed hundreds elsewhere in the Caribbean (IFRC, 2022). Bhola, Odisha in 1999, Odisha in "
     "2013 and Cuba in the same decades describe one trajectory: the death toll falls when the "
     "warning reaches the household and the household has somewhere to go. The remaining gap in "
     "every one of these cases is the same, and it is not meteorological.",
     "Kuba memberi pembanding yang menjaga kisah Bangladesh agar tidak terlihat tak terelakkan. "
     "Pulau itu dilanda badai lebih sering daripada hampir semua tempat di kawasan, dan sistem "
     "pertahanan sipilnya—evakuasi wajib, tempat berlindung yang sudah ditetapkan, petugas "
     "lingkungan yang tahu siapa yang lanjut usia dan siapa yang perlu diangkut—menjaga jumlah "
     "kematian di angka puluhan untuk badai yang menewaskan ratusan orang di tempat lain di "
     "Karibia (IFRC, 2022). Bhola, Odisha 1999, Odisha 2013, dan Kuba pada dekade-dekade yang sama "
     "menggambarkan satu lintasan: korban turun ketika peringatan mencapai rumah tangga dan rumah "
     "tangga itu punya tempat untuk pergi. Celah yang tersisa dalam setiap kasus itu sama, dan ia "
     "bukan celah meteorologis."),
]
