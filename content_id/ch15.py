# -*- coding: utf-8 -*-
"""Bab 15 edisi Indonesia — Data, Statistik dan Misinformasi."""

CH = {
    "num": 15,
    "title": "Data, Statistik dan Misinformasi",
    "theme": "data iklim, penalaran statistik dan perebutan atas bukti",
    "nsec": 10,

    "opening": [
        "Pada 26 September 2024, Badai Helene mendarat di Big Bend, Florida, sebagai badai Kategori 4, "
        "lalu bergerak ke pedalaman sejauh ratusan kilometer, menumpahkan hujan ekstrem di Georgia, "
        "Carolina Selatan, Carolina Utara, dan Tennessee. Banjir di Pegunungan Appalachian selatan "
        "bersifat katastrofik: kota-kota terputus, Sungai French Broad di Asheville mencapai level "
        "yang tidak terlihat lebih dari satu abad, dan setidaknya 230 orang meninggal di enam negara "
        "bagian. Kerusakan diperkirakan melebihi US$78 miliar.",

        "Dalam hitungan jam setelah badai mendarat, peristiwa kedua berlangsung di dunia maya. Unggahan "
        "mengklaim bahwa pemerintah federal merekayasa badai itu, bahwa lembaga bantuan menyita "
        "donasi, bahwa tim penyelamat menolak membantu orang dengan pandangan politik tertentu, dan "
        "bahwa pejabat menyita tanah untuk penambangan litium. Tidak satu pun itu benar. Badan "
        "Manajemen Darurat Federal membuat halaman untuk membantah rumor; pejabat lokal memohon agar "
        "orang berhenti menyebarkannya; dan ahli meteorologi melaporkan ancaman terhadap staf mereka.",

        "Misinformasi tidak berhenti di dunia maya. Ia memengaruhi apakah orang mengungsi, apakah "
        "mereka mengajukan bantuan, dan apakah mereka memercayai peringatan yang datang sebelum badai "
        "berikutnya. Dalam bencana, informasi adalah infrastruktur: ia menentukan apakah orang "
        "bergerak, apakah mereka berlindung, dan apakah mereka menerima bantuan. Ketika informasi "
        "gagal, respons fisik ikut gagal.",

        "Bab ini membahas bagaimana pengetahuan iklim diproduksi, bagaimana ia salah dibaca, dan "
        "bagaimana ia sengaja dipelintirkan. Bab ini menjelaskan apa sebenarnya data iklim, bagaimana "
        "ilmuwan mengukur konsensus dan mengatribusikan peristiwa ekstrem, dan kesalahan statistik mana "
        "yang paling sering berulang. Bab ini kemudian beralih ke mekanika misinformasi dan apa yang "
        "benar-benar berhasil melawannya. Tujuannya bukan menjadikan setiap pembaca ahli statistik, "
        "tetapi membuat setiap pembaca lebih sulit ditipu.",
    ],

    "sections": [
        {
            "num": "15.1",
            "title": "Apa Arti Sebenarnya Sebuah Angka Iklim",
            "paras": [
                "Pernyataan bahwa 2024 adalah tahun kalender pertama yang lebih dari 1,5 °C di atas "
                "level praindustri hanya tepat dalam kaitannya dengan garis dasar, dan garis dasar itu "
                "adalah pilihan. Praindustri biasanya berarti 1850–1900, periode ketika cakupan "
                "instrumen menjadi cukup global untuk memperkirakan rata-rata planet. Ubah garis "
                "dasarnya dan angkanya berubah: relatif terhadap 1981–2010, 2024 sekitar 1,2 °C lebih "
                "hangat; relatif terhadap maksimum glasial terakhir, itu kuantitas yang sama sekali "
                "berbeda.",

                "Angka iklim biasanya dinyatakan sebagai anomali alih-alih suhu absolut, karena "
                "anomali lebih dapat dibandingkan antaruang dan waktu. Stasiun di Siberia dan stasiun "
                "di Indonesia memiliki suhu absolut yang sangat berbeda, tetapi perubahan "
                "tahun-ke-tahunnya dapat dirata-ratakan secara bermakna. Konvensi itu menghindari "
                "distorsi akibat sebaran stasiun cuaca yang tidak merata, tetapi juga membuat angkanya "
                "abstrak, yang merupakan salah satu alasan angka itu mudah disalahartikan.",

                "Setiap angka iklim juga membawa rentang ketidakpastian, dan rentang itu bukan tanda "
                "kelemahan. Ia mencerminkan cakupan yang tidak lengkap, kesalahan instrumen, dan "
                "pilihan metode. Suhu permukaan rata-rata global yang diperkirakan NASA, NOAA, Met "
                "Office, dan Berkeley Earth sepakat dalam beberapa perseratus derajat, sebuah "
                "konvergensi yang luar biasa mengingat mereka menggunakan jaringan stasiun dan metode "
                "interpolasi yang berbeda. Konvergensi metode independen adalah bukti terkuat yang "
                "dapat diminta pembaca.",
            ],
        },
        {
            "num": "15.2",
            "title": "Dari Mana Datanya Berasal",
            "paras": [
                "Rekaman instrumental dirakit dari stasiun darat, pelampung dan kapal laut, balon "
                "cuaca, pesawat, dan satelit. Masing-masing memiliki kekuatan dan kelemahan. Stasiun "
                "darat memberikan rekaman panjang tetapi sebarannya tidak merata, dengan cakupan padat "
                "di Eropa dan Amerika Utara serta jarang di sebagian Afrika dan Amerika Selatan. "
                "Pengukuran laut mencakup dua pertiga planet tetapi secara historis diambil oleh kapal "
                "dagang di sepanjang jalur pelayaran, meninggalkan celah yang harus diisi model.",

                "Satelit memberikan cakupan global tetapi hanya sejak akhir 1970-an, dan mereka "
                "mengukur hal yang berbeda: sounder gelombang mikro memperkirakan suhu troposfer "
                "bawah, altimeter radar mengukur muka laut, dan radiometer mengukur suhu permukaan "
                "laut. Rekaman satelit harus dikalibrasi lintas instrumen yang berurutan, dan "
                "perbedaan kecil dalam kalibrasi dapat menghasilkan tren yang tampak sebagai artefak "
                "alih-alih sinyal — fakta yang telah dimanfaatkan kampanye melawan data.",

                "Produk reanalisis seperti ERA5 menggabungkan observasi dengan model cuaca untuk "
                "menghasilkan rekonstruksi atmosfer yang konsisten secara fisik sejak 1940, dan "
                "rekaman proksi — cincin pohon, inti es, karang, sedimen — memperluas gambaran hingga "
                "ribuan tahun ke belakang. Proksi kurang presisi tetapi menetapkan konteks: pemanasan "
                "saat ini jauh lebih cepat daripada apa pun di Holosen, dan konsentrasi karbon "
                "dioksida lebih tinggi daripada titik mana pun dalam setidaknya 800.000 tahun, dan "
                "mungkin tiga juta tahun.",
            ],
        },
        {
            "num": "15.3",
            "title": "Mengukur Konsensus Ilmiah",
            "paras": [
                "Klaim bahwa sekitar 97 persen ilmuwan iklim sepakat bahwa aktivitas manusia "
                "memanaskan planet berasal dari beberapa studi independen. Doran dan Zimmerman (2009) "
                "mensurvei ilmuwan Bumi dan menemukan bahwa 97 persen dari mereka yang aktif "
                "menerbitkan riset iklim sepakat bahwa aktivitas manusia adalah faktor penyumbang "
                "signifikan. Cook dkk. (2013) memeriksa hampir 12.000 abstrak dan menemukan bahwa di "
                "antara yang menyatakan posisi, 97,1 persen mendukung konsensus, angka yang kemudian "
                "direvisi naik ketika sampel dikoreksi.",

                "Lynas dkk. (2021) meninjau 88.125 makalah terkait iklim yang diterbitkan antara 2012 "
                "dan 2020 dan menemukan bahwa lebih dari 99,9 persen mendukung konsensus. Itu adalah "
                "tingkat kesepakatan luar biasa untuk pertanyaan ilmiah apa pun, sebanding dengan "
                "konsensus tentang tektonik lempeng atau teori kuman penyakit. Itu tidak berarti sains "
                "selesai dalam setiap detail; itu berarti klaim utamanya tidak diperdebatkan secara "
                "serius oleh para spesialis.",

                "Celah antara konsensus ilmiah dan persepsi publik juga diukur. Survei di Amerika "
                "Serikat menemukan bahwa publik memperkirakan porsi ilmuwan yang sepakat sekitar 70 "
                "persen, jauh di bawah angka sebenarnya, dan bahwa perkiraan yang terlalu rendah itu "
                "terkait dengan dukungan kebijakan yang lebih rendah. Celah itu kadang disebut celah "
                "konsensus, dan ia dihasilkan mekanisme yang sama yang menghasilkan miskonsepsi lain: "
                "pengulangan, paparan selektif, dan menonjolnya suara yang berbeda pendapat secara "
                "tidak proporsional dengan jumlahnya.",
            ],
        },
        {
            "num": "15.4",
            "title": "Ilmu Atribusi",
            "paras": [
                "Atribusi peristiwa mengajukan pertanyaan kontrafaktual: seberapa besar kemungkinan "
                "gelombang panas, banjir, atau kekeringan ini terjadi di dunia tanpa pengaruh manusia? "
                "Metodenya membandingkan ansambel besar simulasi model iklim dengan dan tanpa emisi gas "
                "rumah kaca historis, dan kadang menggabungkannya dengan tren teramati. Ia tidak "
                "mengatakan bahwa perubahan iklim menyebabkan badai tertentu, karena cuaca selalu "
                "memiliki banyak penyebab; ia mengatakan bahwa probabilitas atau intensitas peristiwa "
                "itu telah bergeser.",

                "Bidang ini matang dengan cepat. World Weather Attribution, kolaborasi ilmuwan di "
                "Eropa dan Amerika Serikat, kini menghasilkan analisis cepat dalam hitungan hari atau "
                "pekan setelah suatu peristiwa. Studi menemukan bahwa gelombang panas Pasifik Barat "
                "Laut 2021 setidaknya 150 kali lebih mungkin akibat perubahan iklim, bahwa banjir "
                "Pakistan 2022 menjadi lebih intens karena pemanasan, dan bahwa panas Eropa 2024 "
                "menjadi jauh lebih mungkin dan lebih panas.",

                "Atribusi sangat kuat karena menghubungkan statistik global dengan pengalaman lokal, "
                "tetapi juga mudah disalahartikan. Temuan bahwa suatu peristiwa menjadi dua kali lebih "
                "mungkin tidak berarti peristiwa itu dua kali lebih parah, dan temuan bahwa tidak ada "
                "sinyal manusia yang terdeteksi dalam peristiwa tertentu tidak berarti perubahan iklim "
                "tidak terjadi. Ketiadaan atribusi untuk satu peristiwa bukan bukti melawan tren yang "
                "lebih luas, sebagaimana satu pekan dingin bukan bukti melawan iklim yang menghangat.",
            ],
        },
        {
            "num": "15.5",
            "title": "Kekeliruan Statistik yang Berulang",
            "paras": [
                "Kekeliruan paling umum adalah memilih garis dasar secara curang. Klaim yang banyak "
                "diulang bahwa pemanasan berhenti pada 1998 bergantung pada pemilihan tahun dengan El "
                "Niño yang sangat kuat sebagai titik awal. Mulai analisis tiga tahun lebih awal atau "
                "lebih akhir dan trennya jelas. Teknik yang sama digunakan untuk menyatakan bahwa es "
                "laut sedang pulih, bahwa 1930-an lebih panas, atau bahwa gletser tertentu sedang "
                "tumbuh: pilih jendela yang menghasilkan kemiringan yang diinginkan.",

                "Kekeliruan kedua adalah mencampuradukkan cuaca dengan iklim. Cuaca dingin di satu "
                "wilayah tidak membantah tren global, sebagaimana satu hari panas tidak membuktikannya. "
                "Pertanyaan yang relevan adalah apakah frekuensi dan intensitas peristiwa berubah "
                "selama beberapa dekade dan lintas wilayah, yang memerlukan agregasi data alih-alih "
                "memilih anekdot. Anekdot itu hidup dan statistik itu abstrak, itulah sebabnya "
                "kekeliruan ini bertahan.",

                "Kekeliruan ketiga adalah salah membaca korelasi dan kausalitas, biasanya dalam klaim "
                "bahwa karbon dioksida mengikuti suhu alih-alih menyebabkannya. Dalam rekaman inti es, "
                "karbon dioksida memang naik setelah suhu pada awal terminasi glasial, karena "
                "pemanasan awal didorong siklus orbit dan laut kemudian melepaskan karbon dioksida, "
                "yang memperkuat pemanasan. Itu umpan balik, bukan bantahan; fisika karbon dioksida "
                "yang menyerap radiasi inframerah telah ditetapkan pada abad kesembilan belas dan tidak "
                "diperdebatkan.",
            ],
        },
        {
            "num": "15.6",
            "title": "Misinformasi dalam Bencana",
            "paras": [
                "Bencana menciptakan kondisi ideal bagi misinformasi: ketidakpastian tinggi, informasi "
                "resmi lambat, emosi kuat, dan orang putus asa mencari penjelasan. Rumor mengisi "
                "kekosongan. Setelah Badai Katrina 2005, laporan tentang kekerasan luas dan ratusan "
                "kematian di Superdome beredar luas dan kemudian terbukti sebagian besar salah; setelah "
                "gempa Tōhoku 2011, klaim palsu tentang radiasi menyebar lebih cepat daripada imbauan "
                "resmi.",

                "Polanya menguat dengan media sosial. Selama Badai Helene 2024, klaim palsu tentang "
                "modifikasi cuaca, penyitaan tanah, dan pengalihan bantuan menjangkau jutaan orang, dan "
                "pejabat melaporkan bahwa klaim itu mengganggu bantuan. FEMA membuat halaman respons "
                "rumor, dan otoritas Carolina Utara memperingatkan bahwa misinformasi menghalangi orang "
                "mengajukan bantuan. Efeknya terukur: kepercayaan pada peringatan turun, dan pengambilan "
                "langkah evakuasi serta bantuan menurun.",

                "Kecerdasan buatan membuat masalahnya lebih sulit. Gambar hasil generasi tentang jalan "
                "tergenang atau permukiman hancur dapat dibuat dalam hitungan menit dan sulit dibedakan "
                "dari foto asli, terutama di layar ponsel saat darurat. Alat deteksi tertinggal dari "
                "pembuatannya, dan platform yang mendistribusikan konten itu memiliki insentif terbatas "
                "untuk memperlambatnya. Hasilnya adalah nilai pembuktian sebuah foto telah turun, yang "
                "merupakan masalah bagi jurnalis, perusahaan asuransi, dan pengadilan, serta bagi "
                "pengelola darurat.",
            ],
        },
        {
            "num": "15.7",
            "title": "Membaca Grafik dan Mengenali Trik",
            "paras": [
                "Banyak klaim iklim yang menyesatkan dibuat melalui grafik alih-alih kata-kata, karena "
                "grafik tampak objektif. Trik umumnya sederhana: memotong sumbu vertikal sehingga "
                "perubahan kecil tampak dramatis, atau memperpanjangnya sehingga perubahan besar tampak "
                "kecil; memilih tanggal mulai yang menguntungkan tren; memplot jendela pendek dan "
                "menarik kesimpulan panjang; dan membandingkan kumpulan data yang mengukur hal berbeda.",

                "Pembaca dapat menerapkan empat pemeriksaan. Pertama, apa garis dasar atau periode "
                "referensinya, dan mengapa dipilih? Kedua, apa sumbu vertikalnya, dan apakah ia dimulai "
                "dari nol atau dari nilai yang membesarkan perubahan? Ketiga, apa jendela waktunya, dan "
                "apakah cukup panjang untuk membedakan tren dari derau? Keempat, siapa yang menghasilkan "
                "data itu, dan apakah kumpulan datanya tersedia? Pertanyaan terakhir adalah yang paling "
                "kuat, karena grafik yang dimanipulasi jarang disertai data yang dapat diakses.",

                "Komunikasi ilmiah yang sah memiliki konvensi sendiri yang bisa tampak seperti "
                "kelemahan. Batang kesalahan, rentang, dan bahasa bersyarat adalah tanda kehati-hatian, "
                "bukan penghindaran. Ilmuwan yang mengatakan suatu hasil mungkin terjadi dalam skenario "
                "tertentu sedang bersikap presisi; komentator yang mengatakan itu pasti sedang bersikap "
                "ceroboh atau tidak jujur. Belajar membaca bahasa yang berhati-hati sebagai tanda "
                "ketelitian adalah salah satu keterampilan paling berguna yang dapat diperoleh warga.",
            ],
        },
        {
            "num": "15.8",
            "title": "Prabantahan, Bantahan dan Inokulasi",
            "paras": [
                "Bukti tentang mengoreksi misinformasi beragam tetapi tidak tanpa harapan. Membantah "
                "setelah fakta berhasil sebagian: ia mengurangi keyakinan di antara orang yang melihat "
                "koreksi, tetapi jarang menjangkau semua orang yang melihat klaim aslinya, dan "
                "mengulang kepalsuan dapat memperkuatnya di antara sebagian audiens. Implikasi "
                "praktisnya adalah memimpin dengan fakta, menjelaskan tekniknya alih-alih berlarut pada "
                "klaimnya, dan menghindari mengulang kepalsuan lebih dari yang diperlukan.",

                "Prabantahan — memperingatkan orang tentang teknik manipulasi sebelum mereka "
                "menemukannya — memiliki bukti yang lebih kuat. Teori inokulasi, yang dikembangkan "
                "William McGuire pada 1960-an, menyatakan bahwa memaparkan orang pada versi lemah dari "
                "argumen menyesatkan membangun ketahanan terhadap versi penuhnya. Eksperimen lapangan "
                "oleh van der Linden dan rekan menemukan bahwa video pendek yang menjelaskan teknik "
                "seperti manipulasi emosi, dikotomi palsu, dan pencarian kambing hitam meningkatkan "
                "kemampuan orang mengidentifikasi misinformasi lintas topik.",

                "Pertahanan paling tahan lama bersifat struktural: mengurangi pasokan misinformasi, "
                "meningkatkan salience sumber yang dapat dipercaya, dan membuat informasi akurat mudah "
                "ditemukan serta ditindaklanjuti. Itu berarti mendanai penyiaran publik, mewajibkan "
                "platform mengungkap bagaimana algoritmanya memperkuat konten, mendukung jurnalisme "
                "lokal, dan memastikan peringatan resmi tepat waktu, spesifik, dan konsisten. Literasi "
                "individu penting, tetapi ia tidak dapat menggantikan lingkungan informasi yang "
                "dirancang untuk membingungkan.",
            ],
        },
        {
            "num": "15.9",
            "title": "Data Terbuka, Reproduksibilitas dan Celah Data",
            "paras": [
                "Ilmu iklim luar biasa terbuka. Catatan suhu utama diterbitkan bersama metode dan "
                "kodenya; data satelit diarsipkan dan didistribusikan; keluaran model dikontribusikan "
                "ke Coupled Model Intercomparison Project dan tersedia bagi peneliti di seluruh dunia; "
                "dan laporan Panel Antarpemerintah tentang Perubahan Iklim ditinjau ratusan ilmuwan dan "
                "diterbitkan secara lengkap. Keterbukaan ini adalah jawaban terbaik yang tersedia atas "
                "klaim konspirasi, karena siapa pun yang memiliki keterampilan dapat mereproduksi "
                "analisisnya.",

                "Namun datanya tidak tersebar merata. Cakupan stasiun jarang di sebagian Afrika, "
                "Amerika Selatan, dan Asia Tenggara, yang berarti wilayah paling rentan terhadap "
                "perubahan iklim sering memiliki rekaman observasi paling lemah. Hasilnya adalah "
                "ketidakpastian lebih besar dalam proyeksi lokal tepat di tempat keputusan adaptasi "
                "paling mendesak. Program untuk mendigitalkan catatan historis, memperluas stasiun "
                "cuaca otomatis, dan mendukung layanan meteorologi nasional karena itu merupakan bentuk "
                "ketangguhan iklim.",

                "Reproduksibilitas juga merupakan praktik sosial. Kumpulan data yang diterbitkan tetapi "
                "tidak didokumentasikan tidak dapat digunakan; metode yang dijelaskan tetapi tidak "
                "dikodekan tidak dapat direplikasi. Institusi paling berharga di ruang ini adalah "
                "mereka yang memelihara rekaman panjang, mendokumentasikan metodenya, dan menanggapi "
                "kritik di depan publik. Reputasi mereka dibangun atas dasar dapat diperiksa, yang "
                "justru merupakan hal yang tidak dapat dilakukan teori konspirasi.",
            ],
        },
        {
            "num": "15.10",
            "title": "Mengomunikasikan Angka Secara Jujur",
            "paras": [
                "Angka itu persuasif tetapi mudah salah dibaca, sehingga komunikasi memerlukan "
                "kehati-hatian. Kenaikan suhu 1,5 °C terdengar kecil bagi orang yang mengalami 1,5 °C "
                "sebagai perbedaan antara hari sejuk dan hangat; perubahan yang sama pada rata-rata "
                "planet sangat besar, karena ia mewakili pergeseran distribusi panas, bukan kenaikan "
                "seragam. Menjelaskan perbedaan antara suhu lokal dan rata-rata global adalah salah "
                "satu hal paling berguna yang dapat dilakukan komunikator.",

                "Bahasa ketidakpastian juga penting. IPCC menggunakan istilah terkalibrasi: hampir "
                "pasti berarti probabilitas 99–100 persen, sangat mungkin 90–100 persen, mungkin 66–100 "
                "persen, kira-kira sama mungkinnya 33–66 persen. Istilah itu didefinisikan agar pembaca "
                "dapat menafsirkannya secara konsisten, tetapi sering dibaca sebagai keraguan yang "
                "kabur. Menerjemahkannya ke probabilitas sederhana, tanpa menghilangkan "
                "ketidakpastiannya, adalah keterampilan yang layak diajarkan.",

                "Akhirnya, komunikasi harus menghormati audiens. Orang bukan wadah kosong tempat fakta "
                "dituangkan; mereka memiliki pengalaman, nilai, dan sumber yang dipercaya. Pesan yang "
                "dimulai dengan pengalaman lokal, mengakui apa yang tidak pasti, dan menawarkan "
                "tindakan konkret lebih mungkin didengar daripada pesan yang dimulai dengan statistik "
                "global dan instruksi moral. Kejujuran tentang ketidakpastian bukan kelemahan dalam "
                "persuasi; ia adalah fondasi kepercayaan, dan kepercayaan adalah sumber daya yang "
                "paling penting ketika peringatan berikutnya datang.",
            ],
        },
    ],

    "case": {
        "title": "Studi Kasus: Badai Helene dan Darurat Informasi",
        "paras": [
            "Badai Helene mendarat pada 26 September 2024 sebagai badai Kategori 4 di dekat Perry, "
            "Florida, lalu bergerak cepat ke pedalaman. Medan anginnya luar biasa luas, dan "
            "kelembapannya ditarik dari Teluk Meksiko yang sangat hangat. Hasilnya adalah curah hujan "
            "ekstrem di Pegunungan Appalachian selatan, wilayah yang medannya curam menyalurkan air ke "
            "lembah sempit dan di mana komunitas sering hanya dapat diakses melalui satu jalan.",

            "Kerusakan fisiknya parah. Setidaknya 230 orang meninggal di enam negara bagian, "
            "menjadikan Helene badai daratan paling mematikan sejak Katrina pada 2005. Asheville dan "
            "kabupaten sekitarnya terputus; sistem air wilayah itu hancur; dan perkiraan kerusakan "
            "melebihi US$78 miliar. Listrik dan komunikasi gagal di wilayah luas, yang berarti banyak "
            "orang bergantung pada media sosial untuk informasi justru ketika media itu paling tidak "
            "dapat diandalkan.",

            "Lingkungan informasi runtuh lebih cepat daripada jalannya. Klaim bahwa pemerintah federal "
            "menciptakan atau mengarahkan badai, bahwa petugas bantuan menyita pasokan, dan bahwa "
            "pejabat menyita tanah untuk penambangan menyebar lintas platform dan diperkuat tokoh "
            "politik. FEMA menerbitkan halaman respons rumor; pejabat negara bagian mendesak warga "
            "memverifikasi sebelum membagikan; dan ahli meteorologi melaporkan ancaman. Survei kemudian "
            "menemukan bahwa keyakinan pada klaim palsu terkonsentrasi di antara orang yang tidak "
            "memercayai pemerintah secara umum.",

            "Konsekuensi praktisnya terukur. Pejabat melaporkan bahwa sebagian warga tidak mengajukan "
            "bantuan karena percaya bantuan itu akan diambil atau menimbulkan kewajiban; yang lain "
            "menunda evakuasi sebelum badai berikutnya. Organisasi bantuan menemukan bahwa mereka harus "
            "menghabiskan waktu membantah rumor alih-alih menyalurkan pasokan. Episode itu menunjukkan "
            "bahwa kepercayaan bukan variabel lunak: ia menentukan apakah peringatan dipatuhi dan "
            "apakah bantuan diterima.",

            "Pelajarannya spesifik. Peringatan harus datang melalui penyampai lokal yang dipercaya, "
            "bukan hanya melalui lembaga nasional. Koreksi harus cepat, konkret, dan berulang, karena "
            "rumor menyebar di celah antara peristiwa dan respons resmi. Dan platform harus diperlakukan "
            "sebagai bagian dari infrastruktur darurat, dengan kewajiban yang sesuai dengan "
            "pengaruhnya. Komunitas yang memiliki informasi akurat dan memercayainya pulih lebih cepat "
            "daripada komunitas dengan kerusakan fisik yang sama tetapi tanpa kepercayaan.",
        ],
    },

    "future": {
        "title": "Skenario dan Prediksi Masa Depan: Lingkungan Informasi pada 2050",
        "paras": [
            "Rekaman historis menunjukkan bahwa misinformasi bukan hal baru; yang baru adalah kecepatan "
            "dan skalanya. Rumor menyebar dari mulut ke mulut selama gempa Lisbon 1755; radio "
            "memperkuat propaganda pada abad kedua puluh; dan media sosial memampatkan siklusnya dari "
            "hari menjadi menit. Setiap transisi meningkatkan jangkauan dan mengurangi waktu yang "
            "tersedia untuk verifikasi.",

            "Kondisi sekarang menentukan titik awalnya. Sekitar 5 miliar orang menggunakan media "
            "sosial, dan survei di banyak negara menemukan bahwa mayoritas memperoleh setidaknya "
            "sebagian berita darinya. Kecerdasan buatan generatif telah membuat teks, gambar, dan audio "
            "sintetis menjadi murah; riset Reuters Institute dan lainnya menemukan bahwa audiens "
            "kesulitan membedakannya dari materi asli. Kepercayaan pada media berita telah menurun di "
            "sebagian besar demokrasi kaya, sementara kepercayaan pada ilmuwan relatif tinggi, yang "
            "menciptakan peluang bagi ilmuwan yang berkomunikasi langsung.",

            "Asumsi yang menggerakkan proyeksi adalah laju regulasi, biaya deteksi, dan ketangguhan "
            "institusi lokal. Dunia yang berinvestasi dalam infrastruktur verifikasi, literasi media, "
            "dan pelaporan lokal yang dipercaya dapat membatasi kerusakannya; dunia yang tidak akan "
            "menghadapi bencana di mana lingkungan informasi gagal bersamaan dengan lingkungan "
            "fisiknya. Tabel merangkum rentangnya.",
        ],
        "table": {
            "caption": "Tabel 15.1 Indikator lingkungan informasi, 2050",
            "head": ["Indikator", "Terfragmentasi", "Tren saat ini", "Tangguh", "Konsekuensi"],
            "rows": [
                ["Porsi berita dari platform sosial", "70%", "55%", "35%", "Kecepatan vs verifikasi"],
                ["Deteksi media sintetis", "Buruk", "Sedang", "Baik", "Kepercayaan bukti"],
                ["Media lokal", "Sedikit", "Menurun", "Stabil", "Akuntabilitas"],
                ["Kepercayaan pada peringatan resmi", "Rendah", "Sedang", "Tinggi", "Kepatuhan evakuasi"],
                ["Literasi media di sekolah", "20%", "45%", "80%", "Ketahanan terhadap manipulasi"],
                ["Aturan keterbukaan platform", "Tidak ada", "Sebagian", "Kuat", "Transparansi algoritma"],
            ],
        },
        "after_table": [
            "Dua kesimpulan mengikuti. Pertama, misinformasi adalah pengali risiko bencana: ia tidak "
            "menciptakan banjir, tetapi ia menentukan apakah orang melarikan diri darinya. Kedua, "
            "pertahanan yang berhasil bersifat lokal dan struktural — penyampai yang dipercaya, "
            "jurnalisme yang didanai, data terbuka, dan warga yang literat — bukan satu perbaikan "
            "teknologi tunggal.",

            "Apa yang dapat mengubah kesimpulan ini? Regulasi yang mewajibkan platform mengungkap "
            "bagaimana mereka memeringkat konten dapat mengurangi amplifikasi kepalsuan, meskipun "
            "penegakannya lintas batas sulit. Sistem provenans yang murah dan andal — tanda tangan "
            "kriptografis pada gambar dan video — dapat memulihkan sebagian nilai pembuktian sebuah "
            "foto. Dan investasi berkelanjutan dalam jurnalisme lokal dapat membangun kembali institusi "
            "yang dahulu menyaring rumor. Variabel terpenting tetap sama seperti di bab lain: laju "
            "perubahan iklim menentukan seberapa sering sistem informasi akan diuji, dan kualitas "
            "sistem itu menentukan berapa banyak orang selamat dari ujian tersebut.",
        ],
    },
}
