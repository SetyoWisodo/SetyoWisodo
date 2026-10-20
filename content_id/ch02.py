# -*- coding: utf-8 -*-
"""Bab 2 edisi Indonesia — sains fisik pemanasan global."""

CH = {
    "num": 2,
    "title": "Sains Fisik Pemanasan Global",
    "theme": "sains fisik pemanasan global dan sejarahnya",
    "nsec": 10,

    "opening": [
        "Pada Maret 1958, seorang geokimiawan berusia tiga puluh tahun bernama Charles David "
        "Keeling menurunkan alat pengukur gas ke lereng utara Mauna Loa, gunung berapi di Hawaii, "
        "dan mulai mengukur kandungan karbon dioksida di udara Pasifik yang bersih. Bacaan "
        "pertama menunjukkan sekitar 315 bagian per juta. Keeling memilih lokasi itu karena "
        "alasan yang sama dengan para meteorologi yang memilih puncak gunung: udara di sana telah "
        "melintasi ribuan kilometer samudra dan tidak membawa asap lokal, lalu lintas kota, atau "
        "gas buang pabrik. Yang dibawanya adalah komposisi latar atmosfer. Dalam dua tahun, "
        "pengukuran itu menunjukkan sesuatu yang belum pernah ditunjukkan eksperimen laboratorium: "
        "latar itu sendiri meningkat, tahun demi tahun.",

        "Satu instrumen tersebut mengubah argumen fisika abad kesembilan belas menjadi persoalan "
        "pembukuan. Fourier, Foote, Tyndall, dan Arrhenius telah membuktikan bahwa karbon dioksida "
        "menyerap radiasi inframerah dan bahwa penambahan gas itu akan menghangatkan permukaan. "
        "Keeling menetapkan sisi lain dari pembukuan tersebut: seberapa cepat manusia "
        "menambahkannya. Pada 2024, rangkaian yang sama menunjukkan sekitar 424 bagian per juta, "
        "sekitar lima puluh persen di atas nilai pra-industri, dan laju kenaikannya masih "
        "dipercepat (NOAA Global Monitoring Laboratory, 2025). Tidak ada angka lain dalam buku ini "
        "yang diukur secara langsung begitu lama oleh begitu sedikit instrumen.",

        "Fisika ini penting bagi seluruh buku karena ia menetapkan batas bagi segala hal lainnya. "
        "Gelombang panas di Karachi, kegagalan panen di Cerrado Brasil, penarikan polis asuransi "
        "di Florida, dan banjir di Emilia-Romagna adalah peristiwa yang berbeda dengan penyebab "
        "langsung yang berbeda, tetapi semuanya memiliki penyebut yang sama: atmosfer yang menahan "
        "lebih banyak energi dan lebih banyak uap air daripada satu abad lalu. Bab ini menjelaskan "
        "penyebut itu, mekanisme yang menghangatkan permukaan, gas yang menggerakkannya, bukti "
        "bahwa pemanasan itu nyata, pembukuan yang menghubungkannya dengan manusia, dan rangkaian "
        "kemungkinan masa depan yang konsisten dengan apa yang sudah ada di atmosfer.",

        "Bab ini juga menunjukkan di mana kepastian berhenti. Arah perubahan tidak diperdebatkan "
        "secara serius; besarnya respons terhadap konsentrasi tertentu masih berada dalam batas "
        "yang sangat berarti bagi kebijakan. Perbedaan antara iklim yang menghangat 1,8 °C dan "
        "yang menghangat 4,4 °C pada 2100 bukanlah perbedaan selera ilmiah. Itu adalah perbedaan "
        "antara dunia di mana adaptasi mahal dan dunia di mana sebagian adaptasi menjadi mustahil, "
        "dan perbedaan itu bergantung pada asumsi emisi yang tidak dapat ditetapkan oleh model "
        "fisika mana pun.",
    ],

    "sections": [
        {
            "num": "2.1",
            "title": "Efek Rumah Kaca",
            "paras": [
                "Argumen ini dimulai dari sebuah teka-teki tentang suhu. Pada 1824, Joseph Fourier "
                "menghitung bahwa benda pada jarak Bumi dari Matahari seharusnya lebih dingin "
                "daripada Bumi yang sebenarnya, lalu mengusulkan bahwa atmosfer memperlambat "
                "pelepasan panas — sebuah selimut, dalam bayangannya, meskipun ia belum tahu dari "
                "apa selimut itu dibuat. Tiga puluh dua tahun kemudian, Eunice Foote melakukan "
                "eksperimen sederhana dengan silinder kaca di bawah sinar matahari dan menemukan "
                "bahwa tabung berisi karbon dioksida lebih panas daripada tabung berisi udara "
                "biasa. Pada 1859, John Tyndall mengukur penyerapan inframerah oleh berbagai gas "
                "dan menunjukkan bahwa uap air dan karbon dioksida adalah penyerap terkuat di antara "
                "gas-gas yang ada di atmosfer.",

                "Svante Arrhenius memberikan bentuk kuantitatifnya pada 1896. Dengan perhitungan "
                "tangan yang memakan waktu berbulan-bulan, ia memperkirakan bahwa penggandaan "
                "karbon dioksida akan menaikkan suhu global sekitar 5 °C, dan bahwa pembakaran batu "
                "bara akan menghasilkan pemanasan yang dapat diukur dalam beberapa abad. Angka itu "
                "lebih tinggi daripada perkiraan modern — sebagian karena ia mengabaikan beberapa "
                "umpan balik yang kemudian diketahui — tetapi arah dan mekanismenya benar. Pada "
                "1938, Guy Callendar mengumpulkan catatan suhu dari sekitar dua ratus stasiun dan "
                "menunjukkan bahwa pemanasan yang diamati konsisten dengan kenaikan karbon dioksida "
                "yang dihitungnya sendiri.",

                "Yang perlu dipahami dari sejarah ini adalah bahwa mekanismenya sudah diketahui "
                "sebelum ada komputer, satelit, atau model iklim. Yang belum ada adalah dua hal: "
                "data global yang cukup untuk memisahkan sinyal dari variasi cuaca, dan anggaran "
                "karbon yang cukup untuk mengetahui seberapa besar tambahan gas itu dibandingkan "
                "dengan kapasitas atmosfer. Keduanya baru tersedia setelah Perang Dunia Kedua, dan "
                "keduanya menjelaskan mengapa bab ini bergerak dari fisikawan abad kesembilan belas "
                "ke stasiun pengukuran di Hawaii dan stasiun satelit di orbit.",
            ],
        },
        {
            "num": "2.2",
            "title": "Gas Rumah Kaca dan Sumbernya",
            "paras": [
                "Empat kelompok gas bertanggung jawab atas hampir seluruh pemanasan yang disebabkan "
                "manusia. Karbon dioksida menyumbang sekitar tiga perempatnya; ia dilepaskan oleh "
                "pembakaran batu bara, minyak dan gas, oleh produksi semen, dan oleh perubahan "
                "penggunaan lahan, terutama deforestasi. Metana menyumbang sekitar seperenam dan "
                "memiliki daya pemanasan sekitar delapan puluh kali lebih kuat daripada karbon "
                "dioksida selama dua puluh tahun pertama, meskipun ia bertahan di atmosfer hanya "
                "sekitar satu dekade. Dinitrogen oksida berasal dari pupuk, limbah, dan pembakaran "
                "biomassa. Gas fluorinasi — hidrofluorokarbon, perfluorokarbon, sulfur heksafluorida "
                "— hadir dalam konsentrasi sangat kecil tetapi menangkap panas ribuan kali lebih "
                "kuat per molekul.",

                "Konsentrasi karbon dioksida telah meningkat dari sekitar 278 bagian per juta pada "
                "1750 menjadi 424 bagian per juta pada 2024, sebuah kenaikan yang lebih cepat "
                "daripada apa pun dalam catatan inti es selama 800.000 tahun. Metana telah naik "
                "dari sekitar 722 bagian per miliar menjadi lebih dari 1.900, dan dinitrogen "
                "oksida dari 270 menjadi sekitar 336 bagian per miliar. Yang penting bukan hanya "
                "angka absolutnya, tetapi lajunya: kenaikan karbon dioksida selama dua abad terakhir "
                "setara dengan kenaikan yang biasanya memerlukan ribuan tahun dalam catatan "
                "geologis (IPCC, 2021, Bab 5).",

                "Sumbernya dapat dihitung dengan cukup presisi. Global Carbon Budget "
                "memperkirakan emisi fosil pada 2023 sekitar 37,4 miliar ton karbon dioksida, "
                "ditambah sekitar 4 miliar ton dari perubahan penggunaan lahan, sementara sekitar "
                "setengah dari total itu diserap oleh laut dan daratan. Artinya, dari setiap dua "
                "molekul yang dilepaskan, satu tetap di atmosfer. Angka ini penting karena "
                "menghubungkan tindakan di satu tempat dengan konsentrasi di seluruh dunia: emisi "
                "dari satu pembangkit batu bara di Jawa, satu penerbangan dari Eropa, dan satu "
                "hektar hutan yang dibuka di Kalimantan semuanya masuk ke kolam atmosfer yang sama.",
            ],
        },
        {
            "num": "2.3",
            "title": "Bukti Pemanasan",
            "paras": [
                "Bukti pemanasan datang dari banyak arah, dan justru karena itu sulit dibantah. "
                "Termometer menunjukkan kenaikan suhu permukaan sekitar 1,1 sampai 1,2 °C sejak "
                "1850–1900. Gletser di Pegunungan Alpen, Himalaya, dan Andes telah menyusut "
                "selama lebih dari satu abad, dan laju penyusutannya meningkat sejak 1980-an. "
                "Lubang bor di batuan menunjukkan suhu masa lalu yang konsisten dengan pemanasan "
                "permukaan, bukan dengan perubahan lokal. Satelit mengukur bahwa lapisan bawah "
                "atmosfer menghangat sementara stratosfer mendingin — pola yang sesuai dengan "
                "penambahan gas rumah kaca, bukan dengan peningkatan radiasi Matahari.",

                "Makhluk hidup juga mencatatnya. Tanggal berbunga dan bertelur bergeser lebih awal "
                "di banyak belahan dunia; garis pohon di pegunungan naik; spesies laut bergerak ke "
                "arah kutub; dan musim tanam di lintang tinggi memanjang. Catatan fenologi ini "
                "berharga karena independen dari termometer dan karena mencerminkan apa yang "
                "sebenarnya dialami ekosistem, bukan hanya angka di stasiun cuaca. Ketika ratusan "
                "indikator yang berbeda bergerak ke arah yang sama, penjelasan yang paling "
                "sederhana adalah bahwa sistemnya memang menghangat.",

                "Yang paling meyakinkan adalah kombinasi antara data permukaan dan data lautan. "
                "Sekitar sembilan puluh satu persen dari kelebihan energi yang terperangkap berada "
                "di laut, dan kandungan panas laut telah meningkat setiap dekade sejak pengukuran "
                "sistematis dimulai. Karena laut memiliki kapasitas panas yang sangat besar, "
                "kenaikan itu tidak dapat dijelaskan oleh variasi internal jangka pendek. Ia "
                "memerlukan sumber energi tambahan yang masuk ke sistem dan tidak keluar lagi, dan "
                "satu-satunya kandidat yang cukup besar adalah peningkatan gaya radiasi akibat gas "
                "rumah kaca (Cheng et al., 2024).",
            ],
        },
        {
            "num": "2.4",
            "title": "Rekaman Suhu dan Tren",
            "paras": [
                "Rekaman suhu global disusun oleh empat kelompok independen — HadCRUT di Inggris, "
                "NOAA di Amerika Serikat, GISS di NASA, dan Berkeley Earth — yang menggunakan "
                "metode berbeda untuk mengoreksi perubahan instrumen, lokasi stasiun, dan "
                "penutupan wilayah. Keempatnya menghasilkan tren yang hampir identik: sekitar "
                "0,08 °C per dekade sejak 1880, dan sekitar 0,18 sampai 0,20 °C per dekade sejak "
                "1970. Kesamaan itu bukan kebetulan; ia menunjukkan bahwa hasilnya tidak bergantung "
                "pada satu pilihan metodologis.",

                "Tahun 2023 mencatat suhu rata-rata sekitar 1,45 °C di atas periode 1850–1900, "
                "dan 2024 menjadi tahun pertama yang melampaui 1,5 °C dalam satu tahun kalender, "
                "menurut Organisasi Meteorologi Dunia. Angka itu tidak berarti ambang Paris telah "
                "dilanggar, karena Perjanjian Paris mengacu pada rata-rata jangka panjang, bukan "
                "satu tahun. Tetapi angka itu menunjukkan bahwa dunia sudah berada di wilayah yang "
                "dianggap berbahaya oleh negosiasi iklim, dan bahwa El Niño 2023–2024 menambahkan "
                "dorongan di atas tren yang sudah ada.",

                "Membaca rekaman ini dengan benar memerlukan perhatian pada tiga hal. Pertama, "
                "tahun-tahun individual dipengaruhi El Niño dan La Niña, letusan gunung berapi, dan "
                "variasi Matahari, sehingga tren harus dihitung dalam periode beberapa dekade. "
                "Kedua, pemanasan tidak seragam: Arktik menghangat tiga sampai empat kali lebih "
                "cepat daripada rata-rata global, sementara sebagian Samudra Selatan dan Atlantik "
                "utara menghangat lebih lambat. Ketiga, rata-rata global menyembunyikan apa yang "
                "dialami manusia: kenaikan 1,2 °C dalam rata-rata tahunan dapat berarti gelombang "
                "panas yang jauh lebih sering di satu kota dan kekeringan yang lebih panjang di "
                "satu lembah.",
            ],
        },
        {
            "num": "2.5",
            "title": "Revolusi Industri dan Emisi",
            "paras": [
                "Sebelum 1750, atmosfer mengandung karbon dioksida yang berubah sangat lambat, "
                "berkisar antara 180 dan 280 bagian per juta selama siklus glasial dan interglasial. "
                "Revolusi Industri mengubah laju itu. Mesin uap yang membakar batu bara, kemudian "
                "kereta api, kapal, pembangkit listrik, dan kendaraan bermotor, memindahkan karbon "
                "dari kerak bumi ke atmosfer dalam jumlah yang terus meningkat. Pada 1950, emisi "
                "global masih sekitar 6 miliar ton karbon dioksida per tahun; pada 2023, angkanya "
                "lebih dari enam kali lipat.",

                "Emisi kumulatif adalah ukuran yang lebih penting daripada emisi tahunan, karena "
                "pemanasan bergantung pada total karbon yang telah dilepaskan, bukan pada laju "
                "pelepasan pada tahun tertentu. Sejak 1750, manusia telah melepaskan sekitar 2.500 "
                "miliar ton karbon dioksida, dan sekitar dua pertiganya berasal dari periode setelah "
                "1950. Negara-negara industri awal menyumbang bagian yang tidak proporsional "
                "terhadap total itu, sementara negara-negara berkembang menyumbang bagian yang "
                "lebih besar terhadap emisi tahunan saat ini — sebuah ketegangan yang menjadi inti "
                "perdebatan keadilan iklim.",

                "Anggaran karbon yang tersisa menghubungkan sains dengan kebijakan secara langsung. "
                "Untuk mempertahankan peluang lima puluh persen membatasi pemanasan pada 1,5 °C, "
                "dunia hanya dapat melepaskan sekitar 250 miliar ton karbon dioksida lagi — sekitar "
                "enam tahun pada laju emisi saat ini. Untuk 2 °C, anggarannya sekitar 1.150 miliar "
                "ton. Angka-angka ini tidak menentukan kebijakan, tetapi mereka membuat biaya "
                "penundaan menjadi eksplisit: setiap tahun tanpa pengurangan berarti anggaran yang "
                "tersisa menyusut lebih cepat daripada yang dapat digantikan oleh teknologi baru.",
            ],
        },
        {
            "num": "2.6",
            "title": "Penilaian IPCC",
            "paras": [
                "Panel Antarpemerintah tentang Perubahan Iklim (IPCC) didirikan pada 1988 oleh "
                "Organisasi Meteorologi Dunia dan Program Lingkungan Perserikatan Bangsa-Bangsa. "
                "Tugasnya bukan melakukan penelitian baru, melainkan menilai penelitian yang sudah "
                "ada melalui proses yang melibatkan ratusan ilmuwan dan perwakilan pemerintah. "
                "Laporan Penilaian Pertama pada 1990 menyimpulkan bahwa pemanasan yang diamati "
                "kemungkinan besar disebabkan manusia; laporan kelima pada 2013 menyebutnya "
                "sangat mungkin; dan laporan keenam pada 2021 menyatakan bahwa pengaruh manusia "
                "terhadap atmosfer, laut, dan daratan tidak diragukan lagi.",

                "Laporan keenam juga memberikan rentang sensitivitas iklim yang lebih sempit "
                "daripada laporan sebelumnya: pemanasan jangka panjang akibat penggandaan karbon "
                "dioksida kemungkinan besar antara 2,5 dan 4 °C, dengan perkiraan terbaik sekitar "
                "3 °C. Penyempitan itu penting karena mengurangi ruang bagi argumen bahwa "
                "ketidakpastian dapat dijadikan alasan untuk menunda tindakan. Ketidakpastian yang "
                "tersisa lebih besar pada dampak regional dan pada titik kritis daripada pada "
                "respons global terhadap gas rumah kaca.",

                "Laporan IPCC juga memiliki batas. Ia tidak membuat proyeksi tentang kebijakan, "
                "tidak menilai kelayakan politik, dan tidak memberi rekomendasi. Ia menggambarkan "
                "konsekuensi dari berbagai lintasan emisi, lalu menyerahkan pilihan kepada "
                "pembuat kebijakan. Bagi pembaca buku ini, nilai laporan tersebut terletak pada "
                "fungsinya sebagai ringkasan konsensus: jika sebuah klaim bertentangan dengan "
                "laporan IPCC tanpa bukti baru yang kuat, klaim itu memerlukan penjelasan mengapa "
                "ribuan peneliti salah dan pengklaim benar.",
            ],
        },
        {
            "num": "2.7",
            "title": "Panas Laut dan Kenaikan Muka Laut",
            "paras": [
                "Laut adalah penyerap utama panas dan karbon dioksida, dan konsekuensinya terlihat "
                "dalam dua angka. Pertama, kandungan panas laut mencapai rekor tertinggi pada 2023, "
                "dengan kenaikan tahunan yang setara dengan sekitar sepuluh kali konsumsi energi "
                "manusia. Kedua, permukaan laut telah naik sekitar 20 sampai 25 sentimeter sejak "
                "1880, dan lajunya meningkat dari sekitar 1,4 milimeter per tahun pada awal abad "
                "kedua puluh menjadi 3,4 milimeter per tahun pada periode 1993–2022, lalu mendekati "
                "4,5 milimeter per tahun pada dekade terakhir.",

                "Kenaikan itu berasal dari dua sumber yang hampir sama besarnya. Air laut memuai "
                "ketika menghangat, dan sekitar sepertiga kenaikan berasal dari ekspansi termal. "
                "Sisanya berasal dari lelehan gletser dan lapisan es. Karena laut memuai dengan "
                "lambat dan es membutuhkan waktu untuk mengalir, kenaikan muka laut adalah "
                "konsekuensi yang tidak dapat dibalik dalam skala waktu manusia: bahkan jika emisi "
                "berhenti besok, laut akan terus naik selama berabad-abad.",

                "Bagi kota pesisir, yang penting bukan hanya rata-rata kenaikan, tetapi kombinasi "
                "antara kenaikan itu, pasang tertinggi, gelombang badai, dan hujan ekstrem. Banjir "
                "rob yang dulu terjadi sekali dalam beberapa dekade kini terjadi beberapa kali "
                "setahun di Jakarta, Semarang, dan banyak kota lain. Infrastruktur yang dirancang "
                "untuk kondisi 1980-an menjadi tidak memadai bukan karena dibangun dengan buruk, "
                "tetapi karena kondisi yang menjadi dasar desainnya telah berubah.",
            ],
        },
        {
            "num": "2.8",
            "title": "Kehilangan Es dan Kriosfer",
            "paras": [
                "Kriosfer — es di darat dan di laut — adalah bagian sistem iklim yang paling cepat "
                "berubah. Lapisan es Greenland kehilangan sekitar 250 miliar ton massa per tahun "
                "pada periode 2006–2018, dan Antartika kehilangan sekitar 150 miliar ton per tahun "
                "pada periode yang sama. Gletser gunung kehilangan massa di hampir semua wilayah, "
                "dengan total sekitar 1.000 miliar ton per dekade. Setiap miliar ton air yang "
                "masuk ke laut menaikkan permukaan laut sekitar 0,0028 milimeter, sehingga "
                "kehilangan tahunan Greenland dan Antartika bersama-sama menambah sekitar satu "
                "milimeter per tahun.",

                "Es laut Arktik menyusut sekitar 13 persen per dekade pada bulan September, akhir "
                "musim leleh. Ketebalannya berkurang lebih cepat daripada luasnya, karena es tua "
                "yang tebal digantikan oleh es muda yang tipis dan mudah meleleh pada musim "
                "berikutnya. Hilangnya es laut tidak menaikkan permukaan laut secara langsung, "
                "tetapi ia memperkuat pemanasan Arktik melalui umpan balik albedo dan mengubah "
                "cuaca di lintang menengah.",

                "Permafrost — tanah beku yang menutupi sekitar seperempat belahan bumi utara — "
                "menyimpan karbon dalam jumlah yang jauh lebih besar daripada seluruh karbon yang "
                "dilepaskan manusia sejak 1750. Ketika tanah itu mencair, mikroba menguraikan bahan "
                "organik dan melepaskan karbon dioksida dan metana. Laju pelepasannya masih menjadi "
                "subjek penelitian intensif, tetapi arahnya sudah jelas: pemanasan tambahan dari "
                "permafrost akan memperkuat, bukan melemahkan, pemanasan yang disebabkan manusia.",
            ],
        },
        {
            "num": "2.9",
            "title": "Siklus Karbon dan Umpan Balik",
            "paras": [
                "Dari sekitar 40 miliar ton karbon dioksida yang dilepaskan manusia setiap tahun, "
                "sekitar seperempat diserap laut dan seperempat lagi diserap daratan, terutama "
                "hutan yang tumbuh. Sisanya tetap di atmosfer. Penyerapan ini adalah jasa yang "
                "sangat besar — tanpa itu, konsentrasi atmosfer akan naik dua kali lebih cepat — "
                "tetapi jasa itu tidak gratis dan tidak tak terbatas. Laut menjadi lebih asam, "
                "dengan pH turun sekitar 0,1 unit sejak era pra-industri, dan kapasitas "
                "penyerapannya menurun ketika suhu naik.",

                "Umpan balik karbon adalah proses yang dapat mengubah penyerap menjadi sumber. "
                "Pemanasan mempercepat respirasi tanah, meningkatkan kebakaran hutan, dan mencairkan "
                "permafrost. Kekeringan melemahkan pertumbuhan hutan dan membuatnya lebih rentan "
                "terhadap kebakaran. Di laut, pemanasan mengurangi kelarutan karbon dioksida dan "
                "memperlambat sirkulasi yang membawa karbon ke kedalaman. Setiap proses ini kecil "
                "secara individual, tetapi bersama-sama mereka dapat menambah puluhan bagian per "
                "juta pada konsentrasi akhir abad ini.",

                "Umpan balik fisik dan biologis inilah yang membuat pemanasan tidak sepenuhnya "
                "dapat diprediksi dari emisi saja. Sebagian besar model iklim sepakat bahwa umpan "
                "balik karbon akan memperkuat pemanasan, tetapi besarnya masih menjadi sumber "
                "ketidakpastian. Yang tidak ambigu adalah arahnya: semakin lama karbon berada di "
                "atmosfer, semakin besar kemungkinan bahwa sistem alam akan melepaskan karbon "
                "tambahan, bukan menyerapnya.",
            ],
        },
        {
            "num": "2.10",
            "title": "Atribusi Pemanasan",
            "paras": [
                "Atribusi adalah proses memisahkan penyebab perubahan iklim dari variasi alami. "
                "Metodenya membandingkan pola yang diamati dengan pola yang dihasilkan model ketika "
                "hanya faktor alami dimasukkan, dan ketika faktor manusia ditambahkan. Jika pola "
                "yang diamati hanya muncul dalam simulasi yang menyertakan gas rumah kaca, maka "
                "faktor manusia diperlukan untuk menjelaskannya. Pola yang dimaksud bukan hanya "
                "suhu rata-rata, tetapi juga pola vertikal — pemanasan troposfer dan pendinginan "
                "stratosfer — yang tidak dapat dihasilkan oleh perubahan Matahari.",

                "Kesimpulan IPCC adalah bahwa pengaruh manusia telah menaikkan suhu global sekitar "
                "1,1 °C sejak 1850–1900, dan bahwa seluruh pemanasan yang diamati sejak 1950-an "
                "dapat dijelaskan oleh faktor manusia. Faktor alami — Matahari, gunung berapi, "
                "variasi internal — tidak cukup besar untuk menjelaskan kenaikan yang diamati. "
                "Atribusi juga telah diterapkan pada peristiwa individual: gelombang panas Eropa "
                "2003, gelombang panas Rusia 2010, banjir Pakistan 2022, dan kebakaran hutan "
                "Kanada 2023 semuanya dianalisis dengan metode yang sama, dan dalam banyak kasus "
                "kesimpulannya adalah bahwa perubahan iklim meningkatkan probabilitas atau "
                "intensitasnya.",

                "Atribusi tidak menjawab pertanyaan tentang tanggung jawab. Ia dapat menunjukkan "
                "bahwa suatu peristiwa menjadi lebih mungkin karena emisi, tetapi ia tidak dapat "
                "menunjukkan siapa yang harus membayar atau seberapa besar kompensasi yang adil. "
                "Pertanyaan-pertanyaan itu bersifat politik dan etis, dan sains hanya dapat "
                "memberikan salah satu dari banyak masukan. Memahami batas ini penting agar "
                "atribusi tidak digunakan sebagai pengganti argumen keadilan, atau sebaliknya, "
                "agar ketidakpastian ilmiah tidak digunakan sebagai alasan untuk menolak keadilan.",
            ],
        },
    ],

    "case": {
        "title": "Studi Kasus: Kurva Keeling",
        "paras": [
            "Kurva Keeling adalah salah satu grafik paling terkenal dalam sains, dan salah satu "
            "yang paling sering disalahpahami. Grafik itu menunjukkan karbon dioksida di Mauna "
            "Loa sejak 1958, naik dari sekitar 315 menjadi lebih dari 424 bagian per juta, dengan "
            "gigi gergaji tahunan yang disebabkan oleh pertumbuhan tanaman di belahan bumi utara "
            "pada musim panas dan pembusukan pada musim dingin. Naiknya garis adalah sinyal "
            "antropogenik; gigi gergajinya adalah napas biosfer.",

            "Ketelitian pengukuran itu bukan kebetulan. Keeling menetapkan prosedur kalibrasi yang "
            "ketat, menolak data yang tercemar angin lokal, dan mempertahankan instrumen yang sama "
            "selama bertahun-tahun. Ketika anggaran penelitiannya dipotong pada 1960-an, ia "
            "melanjutkan pengukuran dengan dana yang lebih kecil dan tim yang lebih kecil, karena "
            "ia memahami bahwa nilai rangkaian terletak pada kesinambungannya. Rangkaian yang "
            "terputus selama satu tahun akan kehilangan kemampuannya untuk memisahkan tren dari "
            "variasi musiman.",

            "Hasilnya adalah bukti yang sangat kuat karena tiga alasan. Pertama, pengukuran itu "
            "dilakukan di lokasi yang jauh dari sumber lokal, sehingga mewakili atmosfer global. "
            "Kedua, metode dan instrumennya konsisten, sehingga perubahan yang terdeteksi bukan "
            "artefak peralatan. Ketiga, rangkaian itu cukup panjang untuk melewati banyak siklus "
            "El Niño dan letusan gunung berapi, sehingga tren jangka panjangnya tidak dapat "
            "dijelaskan oleh peristiwa tunggal.",

            "Kurva itu juga menunjukkan bagaimana sains bekerja secara institusional. Pengukuran "
            "Keeling awalnya didanai oleh program penelitian geofisika Amerika Serikat, kemudian "
            "berpindah ke lembaga lain ketika prioritas politik berubah. Kesinambungannya "
            "bergantung pada sekelompok kecil orang yang bersedia mempertahankan pengukuran jangka "
            "panjang meskipun tidak ada hasil cepat yang dapat dipublikasikan. Hari ini, data "
            "Mauna Loa menjadi rujukan bagi pemerintah, pasar karbon, dan negosiasi iklim, tetapi "
            "nilainya berasal dari keputusan untuk terus mengukur ketika belum ada yang peduli.",

            "Bagi Indonesia, kurva ini memiliki implikasi langsung. Sebagai negara kepulauan dengan "
            "hutan tropis yang luas, Indonesia adalah bagian dari penyerap daratan yang menyerap "
            "seperempat emisi global. Ketika hutan dibuka atau terbakar, penyerap itu melemah dan "
            "karbon yang tersimpan dilepaskan. Kebijakan iklim Indonesia karena itu bukan hanya "
            "tentang mengurangi emisi dari energi, tetapi juga tentang mempertahankan fungsi "
            "penyerapan yang sudah ada — sebuah pelajaran yang sering hilang dalam perdebatan yang "
            "hanya berfokus pada batu bara.",

            "Kurva Keeling tidak membuktikan bahwa manusia menyebabkan pemanasan; bukti itu datang "
            "dari kombinasi isotop, anggaran karbon, dan pola pemanasan vertikal. Tetapi kurva itu "
            "membuktikan bahwa atmosfer berubah, bahwa perubahan itu berlangsung cepat, dan bahwa "
            "perubahan itu dapat diukur dengan presisi yang cukup untuk menuntut penjelasan. Dalam "
            "sejarah sains, sering kali itu sudah cukup: ketika sebuah fenomena dapat diukur, "
            "argumen tentang apakah fenomena itu ada akan segera berubah menjadi argumen tentang "
            "apa yang menyebabkannya.",
        ],
    },

    "future": {
        "title": "Skenario dan Prediksi Masa Depan: Lintasan Fisik hingga 2100",
        "paras": [
            "Masa depan iklim bukan satu angka, melainkan sekumpulan lintasan bersyarat. Syaratnya "
            "adalah emisi kumulatif karbon dioksida, karena pemanasan jangka panjang sebanding "
            "dengan total karbon yang dilepaskan, bukan dengan laju pelepasan pada tahun tertentu. "
            "Skenario yang digunakan IPCC — Shared Socioeconomic Pathways — menggabungkan asumsi "
            "tentang populasi, pertumbuhan ekonomi, teknologi, dan kebijakan menjadi lima jalur "
            "yang berbeda. Yang paling relevan bagi pembaca adalah tiga: lintasan percepatan "
            "dekarbonisasi, lintasan kebijakan saat ini yang diperkuat, dan lintasan yang "
            "mempertahankan dominasi fosil.",

            "Data historis menunjukkan mengapa lintasan itu penting. Selama 10.000 tahun terakhir, "
            "sebelum Revolusi Industri, konsentrasi karbon dioksida tidak pernah melebihi 300 "
            "bagian per juta. Sejak 1750, konsentrasi naik menjadi 424 bagian per juta, dan "
            "sekitar setengah kenaikan itu terjadi sejak 1980. Jika emisi terus meningkat pada "
            "laju saat ini, konsentrasi pada 2100 dapat mencapai 700 sampai 800 bagian per juta, "
            "sebuah tingkat yang terakhir terjadi lebih dari tiga juta tahun lalu, ketika "
            "permukaan laut beberapa meter lebih tinggi daripada sekarang.",

            "Kondisi sekarang memberi titik awal yang jelas. Dunia telah menghangat sekitar 1,2 °C, "
            "permukaan laut naik 20 sampai 25 sentimeter, dan sekitar 1,2 triliun ton karbon "
            "dioksida telah dilepaskan sejak 1750. Anggaran karbon yang tersisa untuk 1,5 °C "
            "sekitar 250 miliar ton, atau sekitar enam tahun pada laju emisi saat ini. Angka ini "
            "bukan ramalan; ia adalah konsekuensi aritmetika dari fisika yang sudah dijelaskan di "
            "bagian sebelumnya, dan ia menunjukkan bahwa pilihan yang tersedia menyempit setiap "
            "tahun penundaan.",

            "Asumsi yang mendasari ketiga lintasan berbeda secara mendasar. Lintasan percepatan "
            "mengasumsikan bahwa emisi mencapai puncak sebelum 2030, turun setengahnya pada 2030, "
            "dan mencapai nol bersih sekitar 2060. Lintasan kebijakan saat ini mengasumsikan bahwa "
            "komitmen yang ada dilaksanakan tetapi tidak diperluas secara signifikan, sehingga "
            "emisi turun lambat dan nol bersih baru tercapai menjelang akhir abad. Lintasan fosil "
            "mengasumsikan bahwa batu bara, minyak, dan gas tetap mendominasi hingga 2100. Ketiga "
            "lintasan itu bukan prediksi tentang apa yang akan dilakukan pemerintah; mereka adalah "
            "alat untuk menguji apa yang terjadi jika dunia memilih salah satunya.",
        ],
        "table": {
            "caption": "Tabel 2.1 Tiga lintasan fisik hingga 2100 (relatif terhadap 1850–1900)",
            "head": ["Lintasan", "Asumsi kebijakan", "2050", "2100", "Penanda yang dapat diamati"],
            "rows": [
                ["Dekarbonisasi cepat (SSP1-2.6)",
                 "Emisi turun setengah pada 2030, nol bersih sekitar 2060",
                 "~1,6 °C", "~1,8 °C (1,3–2,4)",
                 "CO2 atmosfer memuncak di bawah 450 ppm; kenaikan muka laut sekitar 0,4 m"],
                ["Kebijakan saat ini diperkuat (SSP2-4.5)",
                 "Penguatan lambat, nol bersih akhir abad",
                 "~2,0 °C", "~2,7 °C (2,1–3,5)",
                 "CO2 mendekati 500 ppm pada 2060; Arktik bebas es musim panas sebelum 2050"],
                ["Dekarbonisasi terhenti (SSP5-8.5)",
                 "Dominasi fosil berlanjut hingga 2100",
                 "~2,6 °C", "~4,4 °C (3,3–5,7)",
                 "CO2 di atas 700 ppm; kenaikan muka laut di atas 0,8 m dan semakin cepat"],
            ],
        },
        "after_table": [
            "Dua kesimpulan mengikuti dari tabel ini. Pertama, perbedaan antara lintasan terendah "
            "dan tertinggi pada 2100 adalah sekitar 2,6 °C — lebih besar daripada seluruh "
            "pemanasan yang telah terjadi sejak Revolusi Industri. Kedua, perbedaan itu tidak "
            "muncul secara merata: lintasan tinggi menghasilkan gelombang panas yang jauh lebih "
            "sering, kekeringan yang lebih panjang, dan kenaikan muka laut yang lebih cepat, "
            "sementara lintasan rendah masih menghasilkan konsekuensi yang serius tetapi lebih "
            "dapat dikelola.",

            "Apa yang dapat mengubah kesimpulan ini? Perubahan besar dalam teknologi penyimpanan "
            "energi atau dalam biaya energi surya dapat mempercepat dekarbonisasi lebih cepat "
            "daripada yang diasumsikan dalam lintasan menengah. Sebaliknya, umpan balik karbon "
            "yang lebih kuat daripada perkiraan, atau pelepasan metana dari permafrost, dapat "
            "membuat lintasan tinggi lebih buruk daripada angka di atas. Yang tidak dapat diubah "
            "oleh teknologi adalah karbon yang sudah berada di atmosfer: ia akan tetap di sana "
            "selama berabad-abad, dan pemanasan yang telah terjadi tidak dapat dibatalkan dalam "
            "skala waktu satu generasi.",
        ],
    },
}
