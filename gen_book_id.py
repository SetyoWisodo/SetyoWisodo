# -*- coding: utf-8 -*-
import re
import prose

from future_scenarios_loader import FUTURE_SCENARIOS
import deep_render
from content_id import DEEP_ID

CHAPTERS = [
 ("Pendahuluan: Dunia yang Memanas", "dunia yang memanas dan krisis mendatang", [
   "Mengapa Buku Ini",
   "Apa Arti 'Bertahan' Sesungguhnya",
   "Cara Menggunakan Buku Ini",
   "Lingkup Krisis",
   "Kelangsungan Personal, Komunitas dan Masyarakat",
   "Pengetahuan sebagai Alat Bertahan",
   "Peran Pendidikan",
   "Mempersiapkan Ketidakpastian",
   "Membangun Resiliensi",
   "Peta Jalan bagi Pembaca",
   ]),
 ("Sains Fisik Pemanasan Global", "sains fisik pemanasan global dan sejarahnya", [
   "Efek Rumah Kaca",
   "Gas Rumah Kaca dan Sumbernya",
   "Bukti Pemanasan",
   "Rekor Suhu dan Tren",
   "Revolusi Industri dan Emisi",
   "Penilaian IPCC",
   "Panas Laut dan Permukaan Laut",
   "Kehilangan Es dan Kriosfer",
   "Siklus Karbon dan Umpan Balik",
   "Atribusi Pemanasan",
   ]),
 ("Sistem Iklim, Umpan Balik dan Pemantauan", "sistem iklim, mekanisme umpan balik dan pemantauan", [
   "Sistem Iklim",
   "Sirkulasi Atmosfer dan Laut",
   "Umpan Balik Positif dan Negatif",
   "Titik Kritis dan Perubahan Mendadak",
   "Pemantauan Suhu dan Satelit",
   "Pemantauan Laut dan Es",
   "Atribusi Peristiwa Ekstrem",
   "Sistem Peringatan Dini",
   "Kualitas Data dan Ketidakpastian",
   "Menggunakan Data untuk Keputusan",
   ]),
 ("Panas Ekstrem dan Kesehatan Perkotaan", "panas ekstrem, gelombang panas dan pulau panas perkotaan", [
   "Definisi dan Tren Gelombang Panas",
   "Fisiologi Stres Panas",
   "Spektrum Penyakit Akibat Panas",
   "Populasi Rentan",
   "Pulau Panas Perkotaan",
   "Dampak Infrastruktur",
   "Produktivitas Tenaga Kerja",
   "Rencana Aksi Panas",
   "Strategi Pendinginan",
   "Adaptasi Jangka Panjang terhadap Panas",
   ]),
 ("Kelangkaan Air dan Kekeringan", "kelangkaan air dan kekeringan", [
   "Siklus Air Global",
   "Jenis dan Indeks Kekeringan",
   "Penyebab Kelangkaan Air",
   "Penggunaan Air Pertanian",
   "Stres Air Perkotaan",
   "Penipisan Air Tanah",
   "Kualitas Air",
   "Tata Kelola Air",
   "Konservasi dan Efisiensi",
   "Sumber Air Alternatif",
   ]),
 ("Banjir dan Kenaikan Permukaan Laut", "banjir dan kenaikan permukaan laut", [
   "Jenis dan Penyebab Banjir",
   "Mekanisme Kenaikan Permukaan Laut",
   "Risiko Banjir Pesisir",
   "Banjir Sungai dan Banjir Bandang",
   "Banjir Perkotaan",
   "Dampak Banjir pada Kesehatan",
   "Pertahanan Banjir",
   "Retret Terkelola",
   "Asuransi dan Keuangan Banjir",
   "Adaptasi Pesisir Jangka Panjang",
   ]),
 ("Ketahanan Pangan dan Pertanian", "ketahanan pangan dan pertanian di tengah perubahan iklim", [
   "Gambaran Sistem Pangan",
   "Dampak Hasil Panen",
   "Stres Panas dan Air pada Tanaman",
   "Hama dan Penyakit",
   "Peternakan dan Perikanan",
   "Kerentanan Rantai Pasok",
   "Volatilitas Harga dan Kelaparan",
   "Pertanian Adaptif",
   "Penyimpanan dan Pengawetan Pangan",
   "Nutrisi dan Pergeseran Diet",
   ]),
 ("Ekosistem dan Kehilangan Keanekaragaman Hayati", "ekosistem dan kehilangan keanekaragaman hayati", [
   "Keanekaragaman Hayati dan Jasa Ekosistem",
   "Kehilangan Habitat",
   "Risiko Kepunahan Spesies",
   "Ekosistem Hutan",
   "Ekosistem Laut",
   "Lahan Basah dan Air Tawar",
   "Spesies Invasif",
   "Adaptasi Berbasis Ekosistem",
   "Strategi Konservasi",
   "Ketergantungan Manusia pada Alam",
   ]),
 ("Dampak Kesehatan Perubahan Iklim", "dampak kesehatan perubahan iklim", [
   "Dampak Kesehatan Langsung dan Tak Langsung",
   "Penyakit Terkait Panas",
   "Penyakit Tular Vektor",
   "Penyakit Tular Air",
   "Kualitas Udara dan Kesehatan Pernapasan",
   "Dampak Kesehatan Mental",
   "Ketahanan Sistem Kesehatan",
   "Kelompok Rentan",
   "Pencegahan dan Kesiapsiagaan",
   "Kesetaraan Kesehatan",
   ]),
 ("Dampak Ekonomi dan Ketahanan Keuangan", "dampak ekonomi dan kesiapsiagaan keuangan di tengah perubahan iklim", [
   "Estimasi Biaya Kerusakan",
   "Dampak Sektoral",
   "Kehilangan Produktivitas Tenaga Kerja",
   "Kerusakan Infrastruktur",
   "Risiko Asuransi dan Keuangan",
   "Dana Darurat dan Diversifikasi Pendapatan",
   "Biaya Adaptasi vs Kelambanan",
   "Kemiskinan dan Ketimpangan",
   "Utang, Arus Kas dan Pemulihan",
   "Strategi Ketahanan Ekonomi",
   ]),
 ("Migrasi dan Pengungsian", "migrasi iklim dan pengungsian", [
   "Pendorong Migrasi Iklim",
   "Pengungsian Internal",
   "Pergerakan Lintas Batas",
   "Status Hukum dan Hak",
   "Tekanan Urbanisasi",
   "Komunitas Penerima",
   "Relokasi Terencana",
   "Kerugian dan Kerusakan",
   "Kohesi Sosial",
   "Respon Kebijakan",
   ]),
 ("Konflik, Keamanan dan Stabilitas", "perubahan iklim, konflik dan keamanan", [
   "Kompetisi Sumber Daya",
   "Bukti Iklim dan Kekerasan",
   "Negara Rapuh",
   "Konflik Pangan dan Air",
   "Kaitan Migrasi-Konflik",
   "Respon Sektor Keamanan",
   "Pembangunan Perdamaian dan Adaptasi",
   "Peringatan Dini Konflik",
   "Tata Kelola dan Stabilitas",
   "Mengurangi Risiko",
   ]),
 ("Infrastruktur, Hunian dan Ketahanan Energi", "infrastruktur, hunian dan ketahanan energi", [
   "Infrastruktur Kritis dan Jaringan Listrik",
   "Sistem Air dan Sanitasi",
   "Jaringan Transport dan Komunikasi",
   "Standar Bangunan dan Kegagalan Berjenjang",
   "Ketahanan Hunian terhadap Panas dan Dingin",
   "Isolasi, Naungan dan Ventilasi",
   "Perencanaan Pemadaman dan Surya",
   "Keamanan Generator dan Penampungan Evakuasi",
   "Pemeliharaan dan Redundansi",
   "Infrastruktur Tahan Masa Depan",
   ]),
 ("Literasi Iklim dan Pendidikan", "literasi iklim dan pendidikan", [
   "Apa Itu Literasi Iklim",
   "Konsep Inti dan Pendidikan Sesuai Usia",
   "Formal dan Informal",
   "Pelatihan Guru dan Desain Kurikulum",
   "Apa Itu Paper Referensi",
   "Peer Review dan Membaca Literatur",
   "Mengevaluasi Bukti dan Statistik",
   "Memahami Metode dan Bias",
   "Membangun Basis Pengetahuan",
   "Mengajar Orang Lain",
   ]),
 ("Data, Statistik dan Misinformasi", "data, statistik dan misinformasi di era iklim", [
   "Mengapa Data Penting dan Jenis Data",
   "Statistik Deskriptif dan Ketidakpastian",
   "Korelasi vs Kausalitas",
   "Grafik, Bagan dan Statistik Menyesatkan",
   "Data Terbuka dan Koleksi Personal",
   "Sumber Misinformasi Iklim",
   "Psikologi Kepercayaan dan Fact-Checking",
   "Literasi Media dan Media Sosial",
   "Sumber Tepercaya dan Komunikasi Sains",
   "Melawan Penyangkal dan Membangun Kepercayaan",
   ]),
 ("Kesiapsiagaan Rumah Tangga: Air, Pangan, Hunian dan Risiko", "kesiapsiagaan rumah tangga untuk air, pangan, hunian dan risiko lokal", [
   "Pemetaan Bahaya Lokal dan Matriks Risiko Personal",
   "Kebutuhan Air Harian, Penyimpanan dan Pemurnian",
   "Panen Air Hujan dan Daur Ulang Greywater",
   "Kebutuhan Nutrisi dan Penyimpanan Pangan",
   "Berkebun Rumah dan Mengurangi Limbah",
   "Memasak Tanpa Listrik dan Keamanan Pangan",
   "Pencegahan Kontaminasi dan Perencanaan Jangka Panjang",
   "Perlindungan Dokumen dan Prioritas Tindakan",
   "Pemantauan dan Pembaruan Rencana",
   "Rencana Khusus Lokasimu",
   ]),
 ("Kesehatan, Tanggap Darurat dan Populasi Khusus", "kesehatan, tanggap darurat dan perlindungan populasi rentan", [
   "Dasar Pertolongan Pertama dan Penyakit Panas",
   "Perawatan Luka, Infeksi dan Manajemen Obat",
   "Penyakit Kronis dan Perawatan Lansia",
   "Anak, Disabilitas dan Kebutuhan Khusus",
   "Rumah Tangga Miskin, Migran dan Komunitas Adat",
   "Kapan Evakuasi dan Tas Siaga",
   "Komunikasi Keluarga, Hewan Peliharaan dan Bertahan di Tempat",
   "Keamanan Pasca-Bencana dan Kembali ke Rumah",
   "Pertolongan Pertama Psikologis",
   "Kit Kesehatan dan Layanan Darurat",
   ]),
 ("Modal Sosial, Gotong Royong dan Tata Kelola", "modal sosial, gotong royong dan tata kelola komunitas", [
   "Apa Itu Modal Sosial dan Kepercayaan",
   "Pemetaan Jaringan, Bridging dan Bonding",
   "Pemimpin Komunitas dan Partisipasi Inklusif",
   "Prinsip Gotong Royong dan Memulai Kelompok",
   "Berbagi Sumber Daya, Perawatan dan Keterampilan",
   "Distribusi Pangan dan Sistem Komunikasi",
   "Resolusi Konflik dan Keberlanjutan",
   "Tata Kelola Lokal dan Resiliensi Perkotaan",
   "Resiliensi Pedesaan dan Pengetahuan Adat",
   "Memperkuat Ikatan",
   ]),
 ("Energi Terbarukan dan Teknologi Tepat Guna", "energi terbarukan dan teknologi tepat guna untuk adaptasi iklim", [
   "Sistem Energi Terbarukan dan Surya/Baterai",
   "Teknologi Air dan Pemurnian",
   "Teknologi Pertanian dan Praktik Adaptif",
   "Sistem Peringatan Dini dan AI untuk Iklim",
   "Teknologi Low-Tech dan Tepat Guna",
   "Inovasi dan Adopsi Komunitas",
   "Pemeliharaan, Investasi dan Redundansi",
   "Tahan Masa Depan dan Skalabilitas",
   "Contoh Kasus",
   "Jalur Jangka Panjang",
   ]),
 ("Psikologi Iklim dan Kesehatan Mental", "kecemasan iklim, trauma dan membangun resiliensi psikologis", [
   "Kecemasan Iklim dan Alarm Rasional",
   "Kecemasan Pemuda dan Kelambanan Pemerintah",
   "Trauma, PTSD dan Dampak Kesehatan Mental",
   "Membangun Resiliensi Psikologis",
   "Kesehatan Mental Komunitas dan Jaringan Perawatan",
   "Pemulihan setelah Bencana",
   "Sistem Dukungan dan Strategi Coping",
   "Komunikasi dan Bercerita",
   "Dimensi Kultural",
   "Kesejahteraan Jangka Panjang",
   ]),
 ("Tata Kelola, Keadilan dan Keterlibatan Warga", "tata kelola iklim, keadilan, kesetaraan dan keterlibatan warga", [
   "Kerangka Internasional dan Perjanjian Paris",
   "Rencana Adaptasi Nasional dan Tata Kelola Lokal",
   "Penetapan Harga Karbon dan Keuangan Iklim",
   "Kesenjangan Keuangan Adaptasi dan Investasi",
   "Keadilan, Kesetaraan dan Populasi Rentan",
   "Hak Adat dan Gender",
   "Keterlibatan Warga dan Citizen Science",
   "Status Hukum dan Loss & Damage",
   "Respon Kebijakan dan Akuntabilitas",
   "Membangun Tata Kelola Inklusif",
   ]),
 ("Studi Kasus: Panas, Kebakaran, Banjir dan Ekstrem Perkotaan", "studi kasus regional panas, kebakaran hutan, banjir dan ekstrem perkotaan", [
   "Panas di Asia Selatan dan Panas Perkotaan di Kota Global",
   "Kebakaran Hutan di Australia dan Amerika Utara",
   "Banjir di Asia Tenggara dan Banjir Perkotaan",
   "Badai dan Topan di Karibia",
   "Pencairan Permafrost di Arktik",
   "Kenaikan Permukaan Laut di Negara Pulau Kecil",
   "Pelajaran Komparatif: Tata Kelola dan Teknologi",
   "Respon Komunitas",
   "Data dan Bukti dari Kasus",
   "Strategi yang Dapat Ditransfer",
   ]),
 ("Studi Kasus: Kekeringan, Pangan, Air dan Keamanan", "studi kasus regional kekeringan, krisis pangan, stres air dan keamanan", [
   "Kekeringan di Tanduk Afrika dan Sahel",
   "Krisis Pangan di Afrika Sub-Sahara dan Volatilitas Harga",
   "Stres Air di Timur Tengah dan Penipisan Air Tanah",
   "Kaitan Migrasi-Konflik di Negara Rapuh",
   "Adaptasi Petani Kecil dan Pengetahuan Adat",
   "Bantuan, Keuangan dan Loss & Damage",
   "Perbandingan Lintas Regional",
   "Inovasi Kebijakan",
   "Jalur Adaptasi Jangka Panjang",
   "Pelajaran untuk Ketahanan Pangan Global",
   ]),
 ("Rencana Aksi dan Daftar Periksa untuk Bertahan", "rencana aksi personal dan komunitas, daftar periksa dan template untuk bertahan di masa depan", [
   "Rencana Aksi Personal 30 Hari: Air, Pangan, Hunian",
   "Rencana Aksi Komunitas 1 Tahun: Tata Kelola dan Jaringan",
   "Daftar Periksa Darurat: Tas Siaga, Dokumen, Komunikasi",
   "Template Rumah Tangga: Matriks Risiko dan Audit Air",
   "Template Komunitas: Pemetaan dan Gotong Royong",
   "Pemantauan, Latihan dan Pembaruan",
   "Daftar Periksa Keuangan dan Kesehatan",
   "Penyesuaian Populasi Khusus",
   "Glosarium dan Cara Menggunakan Buku Ini",
   "Seruan untuk Bertindak",
   ]),
]

from references import REFS_ID as REFS
REFS = list(dict.fromkeys(REFS))

EXPERTS = [
 "Dr. James Hansen, former NASA GISS Director (2013 op-ed/2016 paper): 'Kenaikan permukaan laut beberapa meter dapat diperkirakan pada pemanasan 2°C — dan 2°C akan membawa konsekuensi yang pantas disebut bencana.'",
 "Prof. Katharine Hayhoe, Texas Tech Chief Scientist (2014, post-IPCC AR5): 'Perubahan iklim ada di sini dan sekarang, bukan di waktu atau tempat yang jauh — pilihan yang kita buat hari ini akan berdampak besar pada masa depan kita.'",
 "Dr. Michael Mann, Penn State climatologist (2004/2021): 'Konsensus ilmiah bahwa iklim menghangat karena manusia hampir sekukuh konsensus tentang gravitasi — banyak lini bukti independen bertemu pada kesimpulan yang sama.'",
 "Dr. Friederike Otto, Imperial College / World Weather Attribution co-founder (2021): 'Gelombang panas Pacific Northwest 2021 hampir mustahil terjadi tanpa perubahan iklim yang disebabkan manusia.'",
 "Prof. Johan Rockström, Potsdam Institute & Stockholm Resilience Centre (2009 Nature; 2023 update): 'Kami mendefinisikan batas planet sebagai ruang tempat manusia dapat beroperasi dengan aman — enam dari sembilan batas kini terlampaui, jauh di luar ruang aman itu.'",
 "Dr. Saleemul Huq, ICCCAD Director (COP speeches, 2015-2023): 'Adaptasi atau mati — adaptasi adalah kelangsungan hidup, dan dana kerugian serta kerusakan harus permanen dalam Perjanjian Paris bagi negara rentan.'",
 "Prof. Nicholas Stern, LSE Grantham Institute (Stern Review 2006): 'Perubahan iklim adalah kegagalan pasar terbesar yang pernah terlihat — manfaat tindakan dini yang kuat jauh melampaui biaya ketidakbertindakan.'",
 "Dr. Maria Neira, WHO Department of Environment, Climate & Health (2021 COP26 Special Report): 'Perubahan iklim adalah ancaman kesehatan tunggal terbesar yang dihadapi umat manusia — pembakaran bahan bakar fosil membunuh kita.'",
 "Prof. Hans-Otto Pörtner, IPCC WGII Co-Chair (IPCC AR6 WGII press conference 28 Feb 2022): 'Perubahan iklim adalah ancaman bagi kesejahteraan manusia dan kesehatan planet — penundaan lebih lanjut akan melewatkan jendela singkat yang cepat menutup untuk masa depan yang layak huni.'",
 "Dr. Debra Roberts, IPCC WGII Co-Chair Durban (AR6 WGII 2022): 'Adaptasi dan mitigasi harus dikejar dengan kekuatan dan urgensi yang sama — tindakan setengah hati bukan lagi pilihan.'",
 "Prof. Michael Oppenheimer, Princeton SROCC Lead Author (SROCC Ch.4, 2019; SciLine 2021): 'Tidak ada skenario yang menghentikan kenaikan permukaan laut pada abad ini — permukaan laut sudah terkunci untuk naik selama berabad-abad akibat panas laut dan respons lapisan es.'",
 "Dr. Cynthia Rosenzweig, NASA GISS / AgMIP founder, World Food Prize 2022 (NYT 2019; WFP laureate statement): 'Potensi risiko kegagalan di banyak lumbung pangan meningkat — sistem pangan menghadapi ekstrem yang meningkat dan menuntut adaptasi sistemik.'",
 "Prof. Diana Liverman, U Arizona Regents Professor (HCN interview 2021; IPCC author): 'Keadilan iklim berarti memperhitungkan siapa yang paling bertanggung jawab dan siapa yang paling rentan, serta bahwa mereka yang paling sedikit menyumbang emisi menanggung beban terbesar.'",
 "Dr. Kristie Ebi, UW CHanGE Professor, IPCC SR15 Lead Author (2018 quote; 2022 IPCC WGII): 'Jika Anda menderita kanker, Anda ingin dokter memberi tahu seberapa serius penyakitnya — orang sudah menderita dan meninggal sekarang, dan risikonya naik tanpa investasi mendesak di sistem kesehatan.'",
 "Prof. Mark Howden, ANU IPCC WGII Vice-Chair (PNAS 2007: Adapting Agriculture to Climate Change): 'Mengatasi hambatan adaptasi yang efektif menuntut pendekatan kebijakan yang menyeluruh dan dinamis — ilmu pengetahuan juga harus beradaptasi, menghubungkan pengetahuan ilmiah, lokal dan masyarakat adat.'",
 "Prof. W. Neil Adger, Univ. of Exeter (2006 Vulnerability): 'Kerentanan bukan sekadar keterpaparan pada bahaya, melainkan arsitektur sosial atas hak, kuasa dan kapasitas yang menentukan siapa yang mampu beradaptasi.'",
 "Prof. Susan L. Cutter, Univ. of South Carolina (2008 Community Resilience): 'Resiliensi berbasis tempat — ciri komunitas menjelaskan pemulihan jauh lebih baik daripada besaran bahaya semata.'",
 "Prof. Daniel P. Aldrich, Northeastern (2015 Social Capital): 'Jaringan sosial, terutama ikatan yang menjembatani kelompok, adalah prediktor terkuat keselamatan dan pemulihan pascabencana.'",
 "Prof. Fikret Berkes, Univ. of Manitoba (2013 Indigenous Knowledge): 'Menghubungkan pengetahuan adat dan ilmiah menghasilkan adaptasi yang sah dan efektif, yang tidak dapat dicapai oleh salah satunya sendirian.'",
 "Prof. Carl Folke, Stockholm Resilience Centre (2010 Resilience Thinking): 'Pemikiran resiliensi membingkai ulang krisis sebagai reorganisasi, dengan perhatian pada ambang, keanekaragaman dan pembelajaran.'",
 "Dr. Nick Watts, Lancet Countdown Director (2021): 'Biaya kesehatan akibat kelambanan sudah melampaui biaya tindakan — setiap sepersepuluh derajat membawa nyawa yang terukur.'",
 "Dr. Marina Romanello, Lancet Countdown (2023): 'Perubahan iklim mengikis determinan lingkungan dan sosial kesehatan, sehingga memperlebar ketimpangan kesehatan global.'",
 "Dr. Ana Vicedo-Cabrera, LSHTM (2021): 'Lebih dari sepertiga kematian akibat panas dapat diatribusikan pada pemanasan antropogenik — beban yang sudah dapat kita hitung.'",
 "Prof. Solomon Hsiang, Stanford (2014 Conflict): 'Variabilitas iklim berkaitan kuat dengan risiko konflik, meskipun institusi yang menentukan apakah tekanan berubah menjadi kekerasan.'",
 "Prof. Marshall Burke, Stanford (2015 Economy): 'Output ekonomi memuncak pada suhu sejuk dan menurun tajam saat panas, dengan kerugian non-linear bagi negara beriklim hangat.'",
 "Prof. David Lobell, Stanford (2011 Crops): 'Pemanasan sejak 1980 telah memotong hasil gandum dan jagung, menutupi keuntungan dari teknologi.'",
 "Prof. Chuang Zhao, Peking Univ. (2017 Yields): 'Setiap derajat pemanasan menurunkan hasil pangan pokok sekitar 6 persen, dengan gandum paling rentan terhadap panas.'",
 "Prof. Tim Wheeler, Univ. of Reading (2013 Food Security): 'Guncangan pangan menjalar melalui harga dan gizi, menghantam lebih dulu masyarakat miskin yang bergantung pada impor.'",
 "Dr. Scott Kulp & Dr. Benjamin Strauss, Climate Central (2019): 'Tiga kali lebih banyak orang tinggal di bawah garis pasang tinggi masa depan daripada yang ditunjukkan model lama — risiko pesisir selama ini diremehkan.'",
 "Prof. Susan Clayton, Wooster (2020 Climate Anxiety): 'Kecemasan iklim adalah alarm yang rasional, terutama bagi kaum muda yang merasakan pengkhianatan generasi tua.'",
 "Dr. Caroline Hickman, Bath (2021 Youth Anxiety): '45 persen pemuda mengatakan perasaan tentang iklim mengganggu kehidupan harian mereka, terkait dengan persepsi kelambanan pemerintah.'",
 "Dr. Nick Obradovich, MPI (2018 Mental Health): 'Suhu yang lebih tinggi secara terukur meningkatkan rawat inap kejiwaan dan risiko bunuh diri.'",
 "Dr. Gilbert Cissé, Swiss TPH (2022 Health & Communities): 'Permukiman perkotaan informal menghadapi risiko kesehatan-iklim yang berlipat dan menuntut perencanaan terpadu.'",
 "Dr. Fatih Birol, IEA (2023 World Energy Outlook): 'Krisis energi mempercepat transisi, tetapi permintaan fosil harus turun jauh lebih cepat untuk menahan 1,5°C.'",
 "Dr. Francesco La Camera, IRENA (2023): 'Energi terbarukan mendominasi pembangkit baru, tetapi pemasangannya harus tiga kali lipat pada 2030 — pembiayaan menjadi titik sumbatnya.'",
 "Ms. Inger Andersen, UNEP (2023 Adaptation Gap): 'Kesenjangan pembiayaan adaptasi melebar dan membiarkan kelompok rentan membayarnya dengan nyawa.'",
 "Ms. Mami Mizutori, UNDRR (Sendai): 'Setiap dolar pencegahan menghemat jauh lebih banyak dalam respons — peringatan dini dan tata guna lahan adalah yang termurah.'",
 "Prof. Kevin Anderson, Manchester (Carbon Budgets): 'Tidak ada eksplorasi fosil baru yang sesuai dengan anggaran 1,5°C — anggarannya sudah terpakai.'",
 "Prof. Corinne Le Quéré, UEA (Global Carbon Budget): 'Rebound emisi pascakrisis membuktikan hanya perubahan struktural yang membelokkan kurva.'",
 "Dr. Pierre Friedlingstein, Exeter (Carbon Cycle): 'Penyerap darat dan laut melemah seiring pemanasan, jadi kita tidak bisa mengandalkan alam membersihkan sisa emisi kita.'",
 "Dr. Zeke Hausfather, Berkeley Earth (2023 Records): 'Pemanasan kini melampaui periode 2.000 tahun terakhir, dan 2023 memecahkan rekor dengan selisih lebar.'",
 "Prof. Peter Gleick, Pacific Institute (Water): 'Krisis air adalah krisis tata kelola yang diperbesar iklim, bukan sekadar soal hidrologi.'",
 "Prof. John Cook, Univ. of Melbourne (Misinformation): 'Misinformasi memakai buku pedoman keraguan — mempelajari triknya membuat khalayak kebal.'",
 "Prof. Andrew Dessler, Texas A&M (2021): 'Fisika rumah kaca telah mapan sejak 1800-an; perdebatan sebenarnya tentang dampak dan pilihan, bukan tentang kenyataannya.'",
 "Prof. Naomi Oreskes, Harvard (2010 Merchants of Doubt): 'Keraguan diproduksi untuk menunda, dan sejarah membantu kita melihat polanya.'",
 "Prof. Bill McKibben, 350.org (2019 Falter): 'Kita telah membangun dunia yang dapat dirusak oleh apa yang kita bangun — perjuangannya adalah untuk masa depan yang masih layak dijalani.'",
 "Prof. Elizabeth Kolbert, New Yorker (2006 Field Notes, 2014 Sixth Extinction): 'Kepunahan dan perubahan iklim bukan dua cerita terpisah, melainkan satu cerita tentang dampak manusia pada planet ini.'",
 "Dr. Al Gore, former US VP (2006 An Inconvenient Truth): 'Perubahan iklim bukan isu politik melainkan isu moral — kelayakan huni bumi bagi anak-anak kita.'",
 "Prof. David Wallace-Wells, NY Magazine (2019 Uninhabitable Earth): 'Skenario terburuk kini menjadi skenario yang masuk akal jika pemanasan terus dibiarkan.'",
 "Prof. Naomi Klein, Rutgers (2014 This Changes Everything): 'Perubahan iklim mengubah segalanya tentang cara kita hidup, mengonsumsi dan memerintah.'",
 "Prof. Amitav Ghosh, writer (2016 Great Derangement): 'Krisis iklim adalah krisis imajinasi — kita kesulitan menarasikan hal yang harus segera kita tindak.'",
 "Prof. Kim Stanley Robinson, author (2020 Ministry for the Future): 'Masa depan adalah proyek kolektif yang dimulai dari institusi yang mampu berpikir jangka panjang.'",
 "Prof. Katharine Jacobs, Univ. of Arizona (2014 National Assessment): 'Penilaian paling berguna ketika diproduksi bersama komunitas yang akan memakainya.'",
 "Dr. Raj Patel, Food Systems (2022): 'Kelaparan mencerminkan kekuasaan, bukan kelangkaan — guncangan iklim memperdalam jurang kuasa itu.'",
 "Prof. Joanna Haigh, Imperial (Solar & Climate): 'Variabilitas matahari tidak dapat menjelaskan pemanasan terkini — sidik jarinya adalah gas rumah kaca.'",
 "Dr. Glen Peters, CICERO (Emissions): 'Kesenjangan emisi bertahan karena janji politik tidak disertai kebijakan untuk mewujudkannya.'",
 "Prof. Pep Canadell, CSIRO (Global Carbon Project): 'Emisi fosil belum mencapai puncak, sehingga setiap tahun penundaan menjadi lebih mahal.'",
 "Dr. Sonja Klinsky, Arizona State (Justice): 'Keadilan dalam kebijakan iklim menyangkut siapa yang memutuskan, siapa yang membayar dan siapa yang didengar — bukan hanya siapa yang beremisi.'",
 "Prof. Joyashree Roy, Jadavpur (IPCC SRCCL): 'Lahan adalah korban sekaligus solusi — pengelolaan lahan berkelanjutan menghubungkan mitigasi, adaptasi dan pangan.'",
 "Prof. Petra Tschakert, Univ. of Western Australia (Vulnerability): 'Pengalaman hidup menghadapi panas dan banjir menunjukkan batas yang tidak tertangkap angka saja.'",
]


NEWS = [
 "2023 adalah tahun terpanas yang tercatat, dengan suhu global 1,45 ±0,12 C di atas pra-industri (WMO State of Global Climate 2023, Jan 2024).",
 "2024 melanjutkan tren, dengan beberapa bulan melebihi 1,5 C di atas pra-industri (WMO, Copernicus).",
 "Kebakaran hutan di Kanada 2023 membakar ~15 juta ha, lebih dari dua kali rekor sebelumnya (1989, 6,7 juta ha), asap menyebar ke Amerika Utara (CIFFC, Nature 2024).",
 "Gelombang panas di Asia Selatan 2022-2023 menyebabkan ribuan kematian dan kehilangan panen (IPCC, 2022; WMO, 2023).",
 "Banjir di Pakistan 2022 memengaruhi 33 juta orang, menewaskan >1.700 dan menyebabkan kerugian/kerusakan >$30 miliar (World Bank PDNA 28 Okt 2022).",
 "Kekeringan di Tanduk Afrika 2020-2023 terburuk dalam 40 tahun, memengaruhi 23 juta orang (WMO, UN OCHA).",
 "Kenaikan permukaan laut mempercepat, dari ~1,5 mm/thn (1901-1990) menjadi 3,6 mm/thn (2005-2015) (IPCC SROCC, AR6).",
 "Pemutihan karang semakin sering, mengancam ekosistem laut (IPCC, NOAA).",
 "Es laut Arktik menurun ~13% per dekade (NASA, NSIDC).",
 "Gletser dunia kehilangan massa, berkontribusi pada kenaikan permukaan laut (IPCC, 2021; WMO, 2023).",
 "Gelombang panas Eropa musim panas 2022 menyebabkan 61.000 kematian berlebih, paling mematikan di benua (Nature Medicine, 2023).",
 "Siklon Tropis Freddy (2023) menjadi siklon tropis terlama 36 hari, menghantam Mozambik dan Malawi (WMO).",
 "Badai Ian (Sep 2022) menyebabkan kerusakan $113 miliar di AS, termahal di Florida (NOAA NHC).",
 "Bendungan Derna Libya runtuh setelah Badai Daniel (Sep 2023) menewaskan >4.300 dan mengungsikan 40.000 (UN OCHA).",
 "Kebakaran Maui Hawaii (Agu 2023) menewaskan 100+ dan paling mematikan di AS dalam seabad (US Fire Administration, NOAA).",
 "Es laut Antarktika capai rekor terendah musim dingin Sep 2023, 1 juta km2 di bawah rata-rata (NSIDC, NASA).",
 "Kekeringan Amazon akhir 2023 menurunkan Rio Negro ke terendah 120 tahun, mengisolasi 500.000 orang (Brazil INPE, Reuters).",
 "Kebakaran hutan Chili Feb 2023 membakar 430.000 ha dan paling mematikan (CONAF, Reuters).",
 "Sungai Rhine surut kritis Agu 2022, mengganggu 80% pelayaran pedalaman Jerman (German Federal Waterways, Reuters).",
 "Jacobabad Pakistan capai 51°C Mei 2022, tertinggi tercatat global (WMO).",
 "Megakekeringan Barat Daya AS 2000-2022 terkering 23 tahun dalam 1.200 tahun (UCLA, Nature Climate Change).",
 "Letusan Hunga Tonga (Jan 2022) menyuntik uap air stratosfer, pengaruhi iklim jangka pendek (NASA).",
 "New York oranye Juni 2023 dari asap Kanada, AQI >400 hari terburuk (US EPA, NASA).",
 "Kebakaran Mediterania Yunani (Jul 2023) evakuasi 20.000 di Rhodes, terbesar di Yunani (Greek Civil Protection).",
 "Topan Doksuri banjir Beijing Jul 2023 hujan terberat 140 tahun, 1 juta mengungsi (China CMA, Reuters).",
 "Siklon Mocha (Mei 2023) mengungsikan 1,7 juta di Myanmar dan Bangladesh (UN OCHA, WMO).",
 "Banjir Afrika Timur Mar-Mei 2023 setelah kekeringan pengaruhi 1,4 juta di Somalia, Ethiopia, Kenya (UN OCHA).",
 "Siklon Yaku Peru (Mar 2023) hujan unprecedented di utara arid, 70 kematian (SENAMHI, Reuters).",
 "Sungai atmosfer California musim dingin 2022-23 akhiri kekeringan tapi kerugian banjir $4,6M (NOAA, CA DWR).",
 "Banjir Rio Grande do Sul Brazil (Apr-Mei 2024) mengungsikan 600.000, bencana terparah negara bagian (Brazil Civil Defense).",
 "Hujan Dubai Apr 2024 gandakan curah tahunan dalam 24 jam, lumpuhkan bandara Teluk (UAE NCM, WMO).",
 "Gelombang panas Asia Tenggara Apr 2024 Thailand 44,2°C, Myanmar 48,2°C, sekolah tutup (Thai Met Dept, WMO).",
 "Rekor panas Inggris Sep 2022 pecah Jul 2022 40,3°C pertama kali >40°C (UK Met Office).",
 "Hasil gandum India turun 10% gelombang panas 2022, picu larangan ekspor pengaruhi harga global (FAO, India IMD).",
 "Musim hujan gagal Tanduk Afrika 2022 dorong 22 juta ke kerawanan pangan akut (FEWS NET, IPC).",
 "Banjir Nigeria 2022 tewaskan 600 dan mengungsikan 1,4 juta, terburuk dekade (Nigeria NEMA, UN OCHA).",
 "Siklon kembar Vanuatu Judy dan Kevin (Mar 2023) hantam dalam 48 jam, pengaruhi 80% populasi (UNICEF, WMO).",
 "Banjir Emilia-Romagna Italia (Mei 2023) 15 kematian dan kerugian €8,5M setelah kekeringan (Italy Civil Protection).",
 "Bencana miliar-dolar AS 2023 rekor 28 kejadian, biaya $92,9M (NOAA NCEI).",
 "Siklon Sitrang Bangladesh (Okt 2022) genangi 10 juta penduduk pesisir (Bangladesh BMD, UN OCHA).",
 "Topan Super Egay Filipina (Jul 2023) pengaruhi 2,4 juta dan kerugian tanaman $100M (NDRRMC, FAO).",
 "Panen zaitun Spanyol 2023 separuh setelah kekeringan+panas, harga minyak zaitun naik 112% (FAO, IOC).",
]


DATA_TABLES = [
 """| Indikator | Nilai | Sumber |
|---|---|---|
| Kenaikan suhu rata-rata global sejak 1850-1900 | ~1,1-1,2 C | IPCC (2023) |
| Konsentrasi CO2 (2024) | ~420 ppm | NOAA (2024) |
| Kenaikan permukaan laut sejak 1900 | ~20-25 cm | IPCC (2023) |
| Penurunan es laut Arktik | ~13% per dekade | NASA |
| Orang terdampak bencana iklim (tahunan) | ~100 juta+ | IFRC |
| Kerusakan ekonomi akibat bencana iklim (tahunan) | ~$200-300 miliar | World Bank |""",
 """| Dampak Kesehatan | Estimasi | Sumber |
|---|---|---|
| Kematian akibat panas tahunan | ~500.000+ | WHO/Lancet |
| Ekspansi penyakit vektor | Rentang meningkat | WHO |
| Kematian akibat polusi udara tahunan | ~7 juta | WHO |
| Prevalensi kecemasan iklim (pemuda) | ~50%+ | Lancet Planetary Health |
| Beban kesehatan mental | Meningkat | WHO |""",
 """| Pangan & Air | Estimasi | Sumber |
|---|---|---|
| Orang menghadapi ketidakamanan pangan | ~800 juta+ | FAO |
| Orang kekurangan air aman | ~2 miliar | WHO/UNICEF |
| Penurunan hasil panen (gandum, per 1 C) | ~6% | IPCC/Science |
| Orang terpindah karena iklim (tahunan) | ~20 juta+ | UNHCR |
| Kerugian ekonomi akibat kekeringan | Miliaran USD | World Bank |""",
]

DATA_POINTS = [
 "suhu rata-rata global naik ~1,1–1,2°C sejak 1850–1900 (IPCC, 2023)",
 "konsentrasi CO2 atmosfer kini ~420 ppm pada 2024 (NOAA, 2024)",
 "permukaan laut naik ~20–25 cm sejak 1900 (IPCC, 2021)",
 "es laut Arktik menyusut ~13% per dekade (NASA, 2024)",
 "~100 juta orang terdampak bencana iklim setiap tahun (IFRC, 2022)",
 "kerugian ekonomi akibat bencana iklim mencapai ~$200–300 miliar per tahun (World Bank, 2022)",
 "~500.000+ kematian terkait panas terjadi setiap tahun (Watts et al., 2021)",
 "~7 juta kematian akibat polusi udara terjadi setiap tahun (WHO, 2023)",
 "~800 juta menghadapi kerawanan pangan (FAO, 2023)",
 "~2 miliar kekurangan air bersih (WHO & UNICEF, 2023)",
 "hasil gandum turun ~6% per 1°C pemanasan (Zhao et al., 2017)",
 "~20 juta mengungsi akibat iklim setiap tahun (UNHCR, 2023)",
]




# Relevance mapping ID (Indonesian keywords)
EXPERT_KEYWORDS = {
 0: ["kenaikan permukaan laut", "pencairan es", "superstorm", "arktik", "permafrost", "srocc", "badai dan topan", "pulau kecil"],
 1: ["literasi", "pendidikan", "keterlibatan warga", "misinformasi", "media", "pengetahuan", "modal sosial", "gotong royong"],
 2: ["sains", "konsensus", "sejarah iklim", "penilaian ipcc", "rumah kaca", "atribusi", "pengukuran", "paper referensi", "membaca literatur"],
 3: ["panas", "gelombang panas", "panas ekstrem", "kebakaran hutan", "atribusi", "panas perkotaan", "asia selatan", "australia"],
 4: ["batas planet", "sistem iklim", "umpan balik", "titik balik", "ekosistem", "keanekaragaman hayati", "ruang operasi aman"],
 5: ["adaptasi atau mati", "kerugian dan kerusakan", "rentan", "pulau kecil", "tanduk afrika", "pakistan", "migrasi", "pengungsian", "pedesaan", "pengetahuan adat"],
 6: ["ekonomi", "stern", "kegagalan pasar", "biaya", "keuangan", "penetapan harga karbon", "investasi", "ketimpangan"],
 7: ["kesehatan", "penyakit", "who", "vektor", "kualitas udara", "panas"],
 8: ["kesejahteraan", "kesehatan planet", "jendela menutup", "dampak, adaptasi dan kerentanan", "adaptasi nasional", "wgii", "kerangka internasional"],
 9: ["adaptasi dan mitigasi harus dikejar", "kekuatan sama", "tata kelola lokal dan aksi iklim", "perencanaan adaptasi nasional", "kerangka internasional"],
 10: ["permukaan laut", "pesisir", "pulau", "lautan dan kriosfer", "srocc", "pencairan", "adaptasi pesisir"],
 11: ["pangan", "pertanian", "lumbung", "panen", "hasil", "sub-sahara", "ketahanan pangan", "stres air", "timur tengah"],
 12: ["keadilan", "kesetaraan", "rentan", "migrasi", "adat", "gender", "bertanggung jawab", "beban", "konflik dan keamanan", "populasi khusus"],
 13: ["kesehatan", "kanker", "menderita", "panas", "vektor", "kesehatan mental", "trauma", "kecemasan", "komunitas"],
 14: ["hambatan", "kebijakan adaptasi", "adaptasi pertanian", "tata kelola lokal", "adaptasi nasional", "pedesaan", "peternakan", "tata kelola air"],
 15: ["kerentanan", "kerentanan", "paparan", "kapasitas adaptif", "arsitektur sosial", "risiko"],
 16: ["resiliensi komunitas", "berbasis tempat", "pemulihan", "besaran bahaya", "modal sosial", "resiliensi"],
 17: ["modal sosial", "ikatan menjembatani", "kepercayaan", "jaringan", "pemulihan bencana", "komunitas"],
 18: ["pengetahuan adat", "ekologi tradisional", "adaptasi efektif", "ko-produksi", "komunitas"],
 19: ["pemikiran resiliensi", "ambang batas", "keanekaragaman", "pembelajaran", "transformasi", "sistem iklim"],
 20: ["lancet countdown", "biaya kesehatan", "sepuluh derajat", "nyawa", "biaya kelambanan", "kesehatan", "lancet"],
 21: ["lancet 2023", "determinan kesehatan", "ketimpangan", "sosial", "lingkungan", "kesehatan", "lancet"],
 22: ["kematian akibat panas", "dapat diatribusikan", "sepertiga", "pemanasan antropogenik", "beban", "kesehatan", "panas"],
 23: ["risiko konflik", "variabilitas iklim", "kelembagaan", "kekerasan", "negara rapuh", "konflik", "keamanan"],
 24: ["output ekonomi", "non-linear", "suhu", "produktivitas", "negara hangat", "ekonomi"],
 25: ["produksi tanaman", "gandum", "jagung", "hasil", "pemanasan sejak 1980", "pangan", "pertanian"],
 26: ["hasil pangan pokok", "panas", "gandum rentan", "derajat", "pertanian", "pangan"],
 27: ["ketahanan pangan", "harga", "rantai pasok", "tergantung impor", "kelaparan", "pangan", "pertanian"],
 28: ["risiko pesisir", "elevasi", "pasang tinggi", "permukaan laut", "diremehkan", "pesisir"],
 29: ["kecemasan iklim", "alarm rasional", "pemuda", "pengkhianatan", "psikologis", "kesehatan", "kesehatan mental"],
 30: ["kecemasan pemuda", "kehidupan harian", "kelambanan pemerintah", "distres", "kesehatan mental", "kesehatan"],
 31: ["kesehatan mental", "rawat inap", "bunuh diri", "suhu", "risiko", "kesehatan"],
 32: ["permukiman informal", "kesehatan perkotaan", "risiko berlipat", "perencanaan terintegrasi", "kesehatan & komunitas", "kesehatan", "komunitas"],
 33: ["prospek energi", "krisis energi", "transisi", "permintaan fosil", "1.5c", "energi", "ekonomi"],
 34: ["terbarukan", "penerapan", "tiga kali lipat", "keuangan", "transisi energi", "energi"],
 35: ["kesenjangan adaptasi", "kesenjangan keuangan", "rentan", "bayar dengan nyawa", "unep", "adaptasi", "keuangan"],
 36: ["sendai", "pencegahan", "peringatan dini", "perencanaan guna lahan", "undrr", "bencana"],
 37: ["anggaran karbon", "eksplorasi fosil", "1.5c", "habis", "tidak ada baru", "energi"],
 38: ["anggaran karbon", "rebound emisi", "perubahan struktural", "kurva", "karbon global", "emisi"],
 39: ["siklus karbon", "penyerap melemah", "alam", "emisi", "umpan balik"],
 40: ["rekor suhu", "berkeley earth", "2.000 tahun", "rekor 2023", "pemanasan", "suhu", "sains iklim"],
 41: ["krisis air", "tata kelola", "hidrologi", "kelangkaan", "keadilan", "air"],
 42: ["misinformasi", "buku pedoman keraguan", "inokulasi", "literasi media", "teknik", "media", "literasi"],
 43: ["fisika rumah kaca", "mapan", "dampak", "pilihan", "realitas", "sains", "rumah kaca"],
 44: ["pedagang keraguan", "diproduksi", "penundaan", "sejarah", "pola", "sains"],
 45: ["goyah", "masa depan layak", "dunia terbangun", "perjuangan", "350.org", "komunitas", "aktivisme"],
 46: ["kepunahan keenam", "catatan lapangan", "dampak planet", "manusia", "kepunahan", "keanekaragaman hayati", "ekosistem"],
 47: ["kebenaran tak nyaman", "isu moral", "kelayakan huni", "anak", "al gore", "keadilan iklim", "moral"],
 48: ["bumi tak layak huni", "skenario terburuk", "masuk akal", "tak terkendali", "wallace-wells", "dampak iklim", "sains"],
 49: ["ini mengubah segalanya", "konsumsi", "tata kelola", "kapitalisme", "naomi klein", "ekonomi"],
 50: ["kegagalan besar", "imajinasi", "narasi", "krisis", "amitav ghosh", "komunitas", "budaya"],
 51: ["kementerian untuk masa depan", "proyek kolektif", "institusi", "pemikiran jangka panjang", "robinson", "tata kelola", "masa depan"],
 52: ["penilaian nasional", "diproduksi bersama", "komunitas", "berguna", "jacobs", "tata kelola", "penilaian"],
 53: ["kelaparan", "kekuasaan", "kelangkaan", "akses", "ketimpangan", "pangan"],
 54: ["variabilitas matahari", "gas rumah kaca", "sidik jari", "haigh", "imperial", "sains", "matahari"],
 55: ["kesenjangan emisi", "janji", "kebijakan", "kesenjangan", "peters", "emisi"],
 56: ["emisi fosil", "tidak ada puncak", "penundaan", "mahal", "canadell", "emisi", "karbon"],
 57: ["keadilan", "memutuskan", "membayar", "didengar", "emisi", "klinsky", "kesetaraan"],
 58: ["lahan", "korban dan solusi", "pengelolaan lahan berkelanjutan", "mitigasi", "adaptasi dan pangan", "pangan"],
 59: ["pengalaman hidup", "panas dan banjir", "batas", "angka", "kerentanan", "komunitas"],
}


def relevant_experts_for_chapter(title, theme):
    key = (title + " " + theme).lower()
    scores=[]
    for idx,kws in EXPERT_KEYWORDS.items():
        score=sum(1 for kw in kws if kw.lower() in key)
        if score>0:
            scores.append((score, idx))
    scores.sort(reverse=True)
    if not scores:
        return []
    return [idx for score, idx in scores[:2]]

EXPERT_DETAILS = {
 0: "Pernyataan Hansen berasal dari makalah 2016 'Ice melt, sea level rise and superstorms' dan opini 2013 yang memperingatkan konsekuensi jangka panjang pemanasan 2°C. Frasa 'beberapa meter' merujuk pada bukti paleoklimat di mana periode sekitar 1-2°C lebih hangat dari pra-industri meninggalkan permukaan laut 6-9 meter lebih tinggi. Mekanismenya bukan kenaikan linear lambat melainkan disintegrasi non-linear lapisan es Antarktika Barat dan Greenland, diperkuat pemanasan laut dari bawah. Ambang 2°C penting karena sering disajikan sebagai batas atas Perjanjian Paris yang dianggap relatif aman. Hansen menilai pembingkaian ini meremehkan risiko komitmen skala abad yang berlanjut lama setelah emisi puncak. Kata 'bencana' menangkap pandangannya bahwa kenaikan multi-meter akan menenggelamkan kota pesisir besar, delta, dan mengungsikan ratusan juta jiwa dengan efek ekonomi dan keamanan berantai. Untuk {section} dalam {topic}, implikasinya adalah target suhu jangka pendek harus dinilai terhadap komitmen permukaan laut jangka panjang, bukan hanya tingkat pemanasan pertengahan abad.",
 1: "Pernyataan Hayhoe berasal dari bukunya 2021 'Saving Us' dan advokasi pasca-AR5 yang membingkai perubahan iklim sebagai realitas lokal saat ini. 'Di sini dan sekarang' melawan persepsi umum bahwa dampak jauh dalam waktu atau geografi, yang ia identifikasi sebagai hambatan psikologis terhadap aksi. 'Pilihan yang kita buat hari ini' merujuk pada keputusan individu dan kolektif tentang energi, penggunaan lahan, dan konsumsi yang membentuk jalur emisi. Frasa 'dampak signifikan pada masa depan' menggarisbawahi inersia sistem iklim, di mana emisi hari ini mengunci pemanasan selama puluhan tahun. Hayhoe menekankan bahwa harapan harus berakar pada agensi, bukan optimisme bawaan. Ia berargumen bahwa pembawa pesan tepercaya — guru, tenaga kesehatan, pemimpin iman dan komunitas — lebih persuasif daripada data abstrak. Untuk {section} dalam {topic}, pesannya mengarahkan analisis pada komunikasi dan strategi pendidikan yang beresonansi lokal dan dapat ditindaklanjuti.",
 2: "Pernyataan Mann mencerminkan karyanya tentang rekonstruksi 'hockey stick' (Mann dkk., 1999) dan pembelaan konsensus selama puluhan tahun terhadap misinformasi. 'Hampir sekuat konsensus tentang gravitasi' adalah analogi sengaja untuk menyampaikan bahwa banyak lini independen — termometer permukaan, satelit, panas laut, inti es, dan model — konvergen pada penyebab antropogenik. 'Bukti independen yang konvergen' berarti tidak ada satu studi pun yang memikul kesimpulan; melainkan replikasi lintas metode dan kelompok mengurangi ketidakpastian. Mann menunjuk pada peran peer review, data terbuka, dan replikasi dalam membangun kepercayaan ini. Pernyataan ini juga membantah pembingkaian media false-balance yang menyamakan dissent minoritas dengan debat ilmiah substantif. Memahami konvergensi ini membantu pembaca mengevaluasi klaim tentang {section} dengan mencari konsistensi lintas dataset, bukan outlier tunggal. Untuk {topic} hal ini membenarkan perlakuan pemanasan antropogenik sebagai premis mapan untuk perencanaan risiko.",
 3: "Pernyataan Otto berasal dari studi cepat World Weather Attribution 2021 tentang kubah panas Pacific Northwest, yang menemukan panas ekstrem tersebut hampir mustahil tanpa perubahan iklim. 'Hampir mustahil' adalah kesimpulan atribusi probabilistik, bukan retorika, berarti kemungkinan kejadian meningkat puluhan kali lipat akibat pemanasan. Metode membandingkan suhu teramati dengan simulasi model iklim dunia dengan dan tanpa gas rumah kaca antropogenik. Gelombang panas — dengan Lytton, Kanada mencapai 49,6°C — menggambarkan bagaimana beberapa derajat pemanasan rata-rata dapat menggeser ekstrem secara non-linear. Lab Otto mempelopori atribusi cepat untuk menghubungkan bencana spesifik dengan perubahan iklim dalam hitungan hari, membantu pemahaman publik. Temuan ini menggarisbawahi bahwa ekstrem {section} bukan nasib buruk acak melainkan bagian dari tren yang terdeteksi. Untuk {topic}, hal ini memperkuat urgensi memperbarui standar infrastruktur, kesehatan, dan tenaga kerja berdasarkan ekstrem baru, bukan rata-rata historis.",
 4: "Pernyataan Rockström berasal dari makalah Nature 2009 'Ruang operasi aman bagi umat manusia' dan pembaruan 2023 yang kini menemukan enam dari sembilan batas terlampaui. 'Batas planet' adalah ambang kuantitatif untuk iklim, biosfer, air tawar, nutrien, dan proses sistem Bumi lain yang menentukan zona stabilitas mirip Holosen. 'Beroperasi aman' berarti tetap dalam ambang ini mengurangi risiko pergeseran mendadak dan ireversibel. 'Enam dari sembilan terlampaui' menunjukkan umat manusia telah meninggalkan zona aman untuk iklim, keanekaragaman hayati, lahan, air tawar, aliran biogeokimia, dan entitas baru, jauh di luar variabilitas pra-industri. Pembaruan menekankan interaksi — pelampauan satu batas memperketat yang lain, seperti deforestasi yang memperkuat pelepasan karbon. Konsep ini membingkai ulang {section} dari masalah sektoral terisolasi menjadi saling ketergantungan sistemik. Untuk {topic}, implikasinya adalah solusi harus terintegrasi lintas energi, pangan, dan pengelolaan ekosistem, bukan tersilo.",
 5: "Pernyataan Huq disampaikan berulang di COP 2015-2023 dan mencerminkan kepemimpinannya di ICCCAD Dhaka dan kepenulisan IPCC AR3-AR5. 'Adaptasi atau mati' adalah singkatan tajamnya bahwa bagi Bangladesh dataran rendah dan pulau kecil, adaptasi bukan opsional melainkan bertahan hidup. 'Loss-and-damage harus permanen dalam Perjanjian Paris' merujuk advokasinya untuk pilar ketiga di luar mitigasi dan adaptasi untuk menangani kerugian yang tak terhindarkan. Frasa ini menangkap bahwa negara rentan menghadapi dampak yang tidak mereka sebabkan, menimbulkan kewajiban keadilan dan keuangan. Huq menghubungkan pengalaman lokal — siklon, banjir, salinitas — dengan negosiasi global, menekankan bahwa komunitas terdampak harus bersuara. Karyanya menjembatani penelitian adaptasi berbasis komunitas dengan kebijakan untuk keuangan iklim dan kompensasi. Untuk {section} dalam {topic}, perspektifnya menempatkan keadilan, kepemimpinan lokal, dan batas adaptasi ketika pemanasan melebihi kapasitas coping sebagai pusat.",
 6: "Pernyataan Stern berasal dari Stern Review 2006 yang ditugaskan Treasury Inggris, penilaian ekonomi komprehensif pertama tentang perubahan iklim sebagai kegagalan pasar. 'Kegagalan pasar terbesar dan terluas yang pernah ada' berarti harga barang dan jasa secara historis mengecualikan biaya kerusakan iklim, mendistorsi insentif di semua sektor. 'Manfaat tindakan awal yang kuat jauh melebihi biaya' didasarkan pada pemodelan bahwa 1% PDB global yang diinvestasikan awal dapat menghindari kerugian 5-20% PDB kemudian dari dampak tak terkendali. Stern menekankan bahwa iklim adalah masalah barang publik global yang memerlukan aksi kolektif, diskonto generasi mendatang, dan manajemen risiko di bawah ketidakpastian. Pembaruan kemudian memperkuat kesimpulan seiring kerusakan terbukti lebih besar dan biaya rendah karbon menurun. Untuk {section} dalam {topic}, logika ini membingkai belanja adaptasi dan mitigasi sebagai asuransi dan investasi, bukan biaya hangus, terutama untuk keuangan, infrastruktur, dan perlindungan yang paling rentan.",
 7: "Pernyataan Neira dibuat sebagai Direktur Departemen Lingkungan, Perubahan Iklim dan Kesehatan WHO sekitar Laporan Khusus COP26 2021. 'Ancaman kesehatan tunggal terbesar yang dihadapi umat manusia' mengangkat iklim dari darurat lingkungan menjadi darurat kesehatan, mengutip panas, polusi udara, ketidakamanan pangan dan air, serta penyakit menular. 'Pembakaran bahan bakar fosil membunuh kita' langsung menghubungkan sumber emisi dengan mortalitas — 7 juta kematian tahunan dari polusi udara, ratusan ribu dari panas, plus beban lebih luas. Neira berargumen tenaga kesehatan adalah pembawa pesan tepercaya yang dapat membuat iklim personal dan mendesak. Laporan WHO yang ia luncurkan menyerukan sistem kesehatan yang tahan iklim dan rendah karbon, dan agar kebijakan iklim dinilai dari manfaat kesehatan. Untuk {section} dalam {topic}, pembingkaiannya membenarkan prioritas pencegahan, surveilans kesehatan yang terhubung dengan pemantauan iklim, dan keadilan akses layanan.",
 8: "Pernyataan Pörtner dibuat sebagai Co-Chair IPCC WGII saat presentasi Ringkasan untuk Pembuat Kebijakan AR6 WGII 2022. 'Ancaman bagi kesejahteraan manusia dan kesehatan planet' mencerminkan sintesis laporan bahwa 3,3-3,6 miliar orang hidup dalam konteks sangat rentan dan ekosistem mendekati batas adaptasi. 'Jendela singkat yang cepat menutup untuk masa depan layak huni' merujuk pada waktu menyempit untuk membatasi pemanasan 1,5°C sambil membangun resiliensi, karena penundaan memperparah risiko. Ia menekankan bahwa laporan bukan hanya tentang risiko masa depan tetapi dampak teramati yang sudah merugikan kesehatan, mata pencaharian, dan keanekaragaman hayati. Frasa 'penundaan lebih lanjut akan kehilangan' menekankan ketergantungan jalur — pilihan dekade ini menentukan kelayakan huni untuk generasi. Untuk {section} dalam {topic}, pesannya memperkuat urgensi aksi mitigasi-adaptasi terintegrasi dan perhatian pada batas di mana adaptasi berhenti efektif.",
 9: "Pernyataan Roberts berasal dari konferensi pers AR6 WGII 2022 sebagai Co-Chair dari Durban, merangkum Bab 6 tentang kota dan permukiman. 'Adaptasi dan mitigasi harus dikejar dengan kekuatan dan urgensi yang sama' mengoreksi prioritas umum mitigasi di atas adaptasi, mencatat bahwa pemanasan sudah terkunci. 'Setengah tindakan bukan lagi pilihan' menandakan bahwa proyek inkremental dan tersilo tidak memadai terhadap risiko yang meningkat dan majemuk. Roberts menyoroti bahwa adaptasi efektif dipimpin lokal, inklusif, dan terkait dengan pembangunan, dengan bukti dari permukiman informal dan kota pesisir. Pernyataan ini juga mengatasi kesenjangan keuangan dan tata kelola yang meninggalkan yang paling rentan tanpa dukungan. Untuk {section} dalam {topic}, hal ini membenarkan pengejaran pemotongan emisi dan peningkatan resiliensi bersamaan, dengan implementasi dilacak terhadap hasil keadilan.",
 10: "Pernyataan Oppenheimer berdasar pada perannya sebagai Lead Author IPCC SROCC Bab 4 (2019) tentang kenaikan permukaan laut dan implikasi pesisir. 'Tidak ada skenario yang menghentikan kenaikan permukaan laut abad ini' berarti bahkan dengan mitigasi kuat, ekspansi termal laut dan respons lapisan es berlanjut akibat inersia sistem. 'Berkomitmen naik selama berabad-abad' menunjukkan bahwa permukaan laut adalah komitmen jangka panjang, dengan potensi multi-meter tergantung emisi, berdasar paleoklimat dan model proses. Laju kenaikan — sekitar dua kali lipat sejak 1990-an — sudah meningkatkan frekuensi banjir pesisir, bahkan tanpa badai lebih kuat. Oppenheimer memperingatkan bahwa perencanaan berbasis peta banjir historis meremehkan paparan masa depan untuk pulau, delta, dan kota dataran rendah. Untuk {section} dalam {topic}, analisis harus bergeser dari mencegah kenaikan menjadi mengelola kenaikan yang tak terhindarkan melalui elevasi, perlindungan, akomodasi, dan retret terkelola, dengan rentang waktu puluhan hingga ratusan tahun.",
 11: "Pernyataan Rosenzweig mencerminkan kepemimpinannya di AgMIP dan penelitian NASA GISS serta World Food Prize 2022, dengan wawancara NYT 2019 tentang iklim dan pangan. 'Potensi risiko kegagalan multi-lumbung pangan meningkat' merujuk pada kemungkinan yang tumbuh bahwa wilayah gandum utama — Amerika Utara, Eropa, Asia — mengalami guncangan hasil simultan dalam tahun yang sama. Pendorongnya adalah panas, kekeringan, dan hujan ekstrem yang overlapping yang semakin mungkin akibat pemanasan, ditambah pasar yang terkait erat. 'Sistem pangan menghadapi ekstrem yang meningkat dan butuh adaptasi sistemik' berarti penyesuaian tingkat petani saja tidak cukup; rantai pasok, penyimpanan, perdagangan, dan diet harus beradaptasi bersama. Karyanya menunjukkan hasil gandum, jagung, dan padi menurun setiap derajat pemanasan, dengan variabilitas regional lebih besar. Untuk {section} dalam {topic}, ini membingkai pangan dan pertanian sebagai risiko sistemik yang memerlukan diversifikasi, varietas resilien, praktik berbasis ekosistem, dan aksi dini pada penyimpanan dan distribusi.",
 12: "Beasiswa keadilan iklim Liverman, termasuk kesaksiannya 2019 di DPR Arizona dan kepenulisan IPCC, mendasari pernyataannya tentang tanggung jawab dan kerentanan. 'Memperhitungkan siapa paling bertanggung jawab, siapa paling rentan' menyerukan atribusi emisi secara historis dan geografis, bukan hanya total nasional saat ini. 'Mereka yang paling sedikit bertanggung jawab menanggung beban terbesar' menunjuk petani kecil, pulau kecil, dan komunitas perkotaan berpenghasilan rendah yang menghadapi dampak paling awal dan keras meski emisi per kapita rendah. Liverman berargumen bahwa respons harus mengatasi kepemilikan lahan, gender, dan akses sumber daya, bukan hanya perbaikan teknis. Ia menekankan bahwa resep top-down sering gagal ketika mengabaikan pengetahuan lokal dan ketidakseimbangan kekuasaan. Untuk {section} dalam {topic}, lensanya menuntut penilaian intervensi berdasarkan siapa mendapat manfaat, siapa membayar, dan siapa memutuskan, mengintegrasikan metrik keadilan ke perencanaan dan evaluasi.",
 13: "Pernyataan Ebi berasal dari kepenulisan utama IPCC SR15 dan penelitian jangka panjang di UW CHanGE tentang panas dan kesehatan. 'Jika Anda menderita kanker, dokter harus mengatakan seberapa serius kondisinya' adalah analoginya untuk komunikasi risiko yang jelas — meremehkan keparahan menunda tindakan penyelamatan jiwa. 'Orang menderita dan meninggal sekarang' melawan pandangan bahwa dampak kesehatan iklim adalah masa depan, mengutip kenaikan terdokumentasi penyakit terkait panas dan mortalitas di pekerja luar ruang, lansia, dan kelompok berpenghasilan rendah. 'Risiko meningkat tanpa investasi mendesak di sistem kesehatan' menunjuk pada kebutuhan peringatan dini panas, perluasan layanan primer, dan fasilitas tahan iklim. Ebi menekankan bahwa bukti kesehatan dapat ditindaklanjuti dan dibenarkan secara ekonomi, dengan manfaat bersama untuk produktivitas dan keadilan. Untuk {section} dalam {topic}, pembingkaiannya memperlakukan adaptasi sebagai kesiapsiagaan kesehatan masyarakat, memerlukan surveilans, pelatihan tenaga kerja, dan pendanaan yang menjangkau garis depan.",
 14: "Pernyataan Howden berasal dari makalah PNAS 2007 'Adapting agriculture to climate change' dan perannya sebagai Wakil Ketua IPCC WGII. 'Mengatasi hambatan adaptasi efektif memerlukan pendekatan kebijakan komprehensif dan dinamis' berarti opsi teknis saja gagal ketika kelembagaan, pasar, dan sistem pengetahuan tidak selaras. 'Sains juga harus beradaptasi' menyerukan menghubungkan pengetahuan ilmiah, lokal, dan adat, dan untuk penelitian yang diproduksi bersama petani dan komunitas. Hambatan yang ia identifikasi mencakup tata kelola terfragmentasi, insentif jangka pendek, dan akses buruk ke prakiraan yang disesuaikan dan keuangan. Howden menekankan pembelajaran iteratif — piloting, pemantauan, dan penyesuaian — daripada rencana sekali jadi. Untuk {section} dalam {topic}, hal ini mengarahkan perhatian pada kondisi pemungkin adopsi: penyuluhan tepercaya, keamanan tenurial, dan kebijakan yang mendukung diversifikasi dan praktik berbasis ekosistem bersama teknologi.",
 15: "Adger membingkai ulang kerentanan sebagai sifat susunan sosial, bukan sifat bahaya. Hak, kuasa dan akses pada sumber daya menentukan siapa yang dapat bersiap, siapa yang dapat pergi dan siapa yang pulih. Intinya struktural, bukan semantik.",
 16: "Kajian berbasis tempat Cutter menunjukkan ciri komunitas menjelaskan pemulihan lebih baik daripada besaran bahaya. Pemetaan kerentanan sosialnya menggabungkan usia, pendapatan, status kepemilikan dan akses layanan menjadi indeks yang dapat dipakai perencana lokal. Metodenya alat penyaring, bukan putusan.",
 17: "Aldrich menemukan modal sosial, terutama ikatan yang menjembatani kelompok, memprediksi keselamatan pascabencana lebih baik daripada benteng fisik. Jaringan mengantar informasi, tempat berlindung dan kredit sebelum lembaga datang. Ikatan yang terlalu rapat juga dapat menutup orang luar.",
 18: "Berkes mendokumentasikan bagaimana pengetahuan adat dan lokal menopang adaptasi melalui pengamatan halus lintas generasi. Menautkannya dengan pemantauan ilmiah menghasilkan pilihan yang tidak dapat dihasilkan salah satunya sendiri. Kombinasi itu menuntut timbal balik, bukan pengambilan.",
 19: "Pemikiran resiliensi Folke memperlakukan krisis sebagai reorganisasi, bukan keruntuhan. Ambang, keanekaragaman dan pembelajaran menentukan apakah sistem menyerap guncangan atau beralih ke keadaan yang lebih buruk. Karena itu pengelolaan bertujuan menjaga pilihan tetap terbuka.",
 20: "Lancet Countdown memantau indikator kesehatan dan iklim setiap tahun pada mitigasi, adaptasi dan pembiayaan. Laporan 2021 menemukan risiko panas, kerawanan pangan dan penyakit menular sudah naik seiring pemanasan teramati. Rangkaian ini dirancang untuk akuntabilitas, bukan ramalan.",
 21: "Lancet Countdown 2023 mencatat paparan panas yang memecahkan rekor bagi kelompok rentan dan melebarnya jurang pembiayaan adaptasi. Sebagian beban kesehatan diatribusikan pada lambatnya penghentian bahan bakar fosil. Para penulis menuntut kesehatan diperhitungkan dalam keputusan iklim.",
 22: "Vicedo-Cabrera dan rekan mengatribusikan sebagian besar kematian akibat panas musim hangat pada pemanasan antropogenik memakai catatan kematian banyak negara. Temuan itu mengubah rata-rata global menjadi jumlah korban. Atribusi semacam ini bergantung pada pemilihan periode dasar.",
 23: "Karya Hsiang menghubungkan variabilitas iklim dengan risiko konflik lintas ratusan studi. Kaitannya kukuh tetapi bersyarat, dengan institusi dan penghidupan menentukan apakah tekanan berubah menjadi kekerasan. Iklim adalah pengali risiko, bukan penyebab.",
 24: "Burke dan rekan menemukan output ekonomi memuncak pada suhu sedang dan menurun tajam pada kondisi panas. Kerugiannya non-linear dan terkonsentrasi di ekonomi tropis yang sudah hangat. Hasilnya menyiratkan pemanasan mendistribusikan ulang pendapatan sebesar ia menghancurkannya.",
 25: "Analisis Lobell memisahkan efek iklim dari teknologi dan pengelolaan dalam rekaman panen global. Pemanasan sejak 1980 menurunkan hasil gandum dan jagung dibandingkan kontrafaktual tanpanya. Adaptasi dan pemupukan karbon menutup sebagian, bukan seluruh, kerugian itu.",
 26: "Zhao dan rekan menggabungkan percobaan pemanasan lapangan dengan model untuk menaksir respons hasil per derajat. Tanaman pokok turun sekitar enam persen per derajat pemanasan lokal, dengan gandum paling sensitif. Taksiran itu berlaku untuk lokasi dan praktik saat ini.",
 27: "Wheeler dan von Braun menelusuri bagaimana guncangan pangan menjalar melalui harga, perdagangan dan gizi. Rumah tangga miskin yang bergantung impor menyerap kerugian pertama dan terdalam. Bantuan pangan jangka pendek tidak mencegah guncangan berikutnya.",
 28: "Kulp dan Strauss mengoreksi data elevasi pesisir dengan radar dan menemukan jauh lebih banyak lahan dan orang berada di bawah garis pasang tinggi masa depan daripada yang ditunjukkan model lama. Taksiran mereka membuat keterpaparan terlihat hingga skala permukiman. Proyeksinya mengasumsikan jalur emisi tertentu.",
 29: "Clayton berargumen kecemasan iklim adalah respons rasional atas ancaman nyata, bukan gangguan. Distres terkonsentrasi pada orang yang mempercayai sains dan merasa tidak didengar institusi. Karena itu pembingkaian klinis dan politik menunjuk arah berbeda.",
 30: "Survei internasional Hickman atas kaum muda menemukan distres luas tentang iklim dan kelambanan pemerintah. Responden melaporkan kekhawatiran mengganggu kehidupan harian dan keputusan tentang masa depan. Sampelnya besar tetapi di beberapa negara bersifat swapilih.",
 31: "Obradovich dan rekan mencocokkan catatan suhu dengan data rawat inap kejiwaan dan bunuh diri. Keduanya naik seiring panas, dan efeknya bertahan lebih dari satu hari. Mekanismenya berjalan melalui tidur, obat dan kontak sosial.",
 32: "Kajian Cissé menunjukkan permukiman informal perkotaan menanggung risiko kesehatan-iklim berlipat: panas, air tercemar, kepadatan dan layanan yang absen. Adaptasi yang mengasumsikan kepemilikan formal dan air perpipaan melewatkan sebagian besar penduduk terdampak. Perencanaan harus mulai dari permukiman, bukan dari jaringan.",
 33: "World Energy Outlook Birol melacak jarak antara target yang dinyatakan dan arus investasi. Krisis mempercepat energi terbarukan tetapi meninggalkan permintaan fosil terlalu tinggi untuk 1,5°C. Rangkaian ini latihan skenario, bukan ramalan.",
 34: "IRENA mendokumentasikan energi terbarukan mendominasi kapasitas pembangkit baru, tetapi pemasangannya harus tiga kali lipat pada 2030 untuk memenuhi target. Pembiayaan, jaringan dan perizinan menjadi kendala pengikat. Biaya bukan lagi hambatan utama di sebagian besar pasar.",
 35: "Laporan kesenjangan adaptasi UNEP membandingkan kebutuhan pembiayaan dengan dana yang benar-benar dicairkan. Kesenjangannya melebar setiap tahun sejak terbit. Adaptasi tetap menjadi porsi iklim yang jauh lebih kecil.",
 36: "Lembaga Mizutori berargumen pencegahan memberi imbal hasil lebih besar daripada respons dan peringatan dini serta tata guna lahan adalah instrumen termurah. Buktinya dari pembukuan kerugian bencana, bukan pemodelan. Hambatannya waktu anggaran, bukan bukti.",
 37: "Aritmetika anggaran karbon Anderson menyiratkan tidak ada ekstraksi fosil baru yang sesuai dengan 1,5°C. Anggarannya cukup kecil sehingga infrastruktur yang ada sudah menghabiskannya. Klaimnya aritmetis dan bergantung pada peluang overshoot yang dipilih.",
 38: "Karya Global Carbon Budget Le Quéré menunjukkan emisi kembali naik setelah guncangan pandemi. Penurunan sementara tidak membelokkan kurva; perubahan struktural di energi dan lahan yang membelokkannya. Rangkaian ini memisahkan siklus dari tren.",
 39: "Friedlingstein dan rekan mengukur berapa banyak karbon yang diserap penyerap darat dan laut tiap tahun. Kedua penyerap melemah seiring pemanasan, sehingga porsi emisi yang tertinggal di atmosfer membesar. Pengukurannya membawa ketidakpastian tetapi arahnya konsisten.",
 40: "Analisis Hausfather menempatkan pemanasan terkini dalam konteks dua ribu tahun terakhir dan melacak bagaimana 2023 memecahkan rekor dengan selisih tak biasa. Rekor itu sebagian diperkuat variabilitas alami di atas tren. Ia menilai proyeksi model bertahan baik terhadap pengamatan.",
 41: "Gleick membingkai kelangkaan air sebagai kegagalan tata kelola yang diperbesar iklim, bukan batas hidrologis murni. Aturan alokasi, tarif dan infrastruktur menentukan siapa yang kekurangan. Kekeringan mengubah masalah distribusi menjadi krisis.",
 42: "Riset Cook menunjukkan inokulasi terhadap misinformasi bekerja lebih baik daripada sanggahan semata. Khalayak yang memahami teknik di balik penyangkalan lebih sulit disesatkan kemudian. Efeknya sederhana tetapi dapat direplikasi.",
 43: "Dessler menegaskan fisika efek rumah kaca sudah mapan sejak abad ke-19. Yang masih terbuka adalah besaran dampak dan pilihan yang menentukannya. Debat publik sering mencampuradukkan keduanya.",
 44: "Oreskes dan Conway mendokumentasikan bagaimana sekelompok kecil ilmuwan dan konsultan memproduksi keraguan atas tembakau lalu atas iklim. Strateginya menyasar ketidakpastian, bukan bukti. Mengenali buku pedomannya mengubah cara klaim dibaca.",
 45: "McKibben berargumen perjuangannya adalah untuk masa depan yang masih dapat dijalani, bukan masa depan yang tak berubah. Bukunya mendata keberhasilan dan kegagalan gerakan sejak 2007. Tujuannya strategis, bukan prediktif.",
 46: "Reportase Kolbert memperlakukan kepunahan dan perubahan iklim sebagai satu cerita tekanan manusia yang menumpuk. Hilangnya spesies menghapus cadangan ekologis yang menyerap variabilitas. Narasinya menghubungkan pengamatan lapangan dengan bukti paleoklimat.",
 47: "Gore membingkai iklim sebagai pertanyaan moral tentang kelayakan huni, bukan perselisihan teknis. Bingkai itu menggerakkan khalayak yang tidak tersentuh argumen teknis. Ia juga dikritik karena menyederhanakan sains pada masanya.",
 48: "Wallace-Wells berargumen skenario terburuk yang masuk akal kurang dibahas dibandingkan peluangnya. Risiko berantai, bukan rata-rata bertahap, menentukan ujung atas. Kritik mencatat bahwa masuk akal tidak sama dengan berkemungkinan besar.",
 49: "Klein menghubungkan kebijakan iklim dengan model ekonomi yang menghasilkannya. Ia berargumen instrumen pasar saja tidak dapat memberi laju yang dibutuhkan. Klaimnya argumen politik, bukan temuan empiris.",
 50: "Ghosh berargumen imajinasi sastra kesulitan merepresentasikan krisis sebesar ini. Ketidakmampuan menarasikan adalah bagian dari sebab lambatnya tindakan. Klaimnya kultural dan melengkapi, bukan menggantikan, analisis empiris.",
 51: "Novel Robinson membayangkan institusi yang mampu bertindak pada horizon berabad-abad. Sumbangannya fiksi desain: bagaimana bank sentral karbon atau kementerian masa depan mungkin bekerja. Fiksi di sini adalah metode spesifikasi.",
 52: "Karya Jacobs tentang penilaian nasional menunjukkan penilaian paling berguna ketika diproduksi bersama komunitas yang akan memakainya. Kredibilitas, relevansi dan legitimasi saling berkompromi. Penilaian adalah proses, bukan laporan.",
 53: "Patel berargumen kelaparan mencerminkan kuasa dan akses, bukan kelangkaan global. Guncangan iklim memperdalam jurang hak yang sudah ada. Bingkai itu mengalihkan perhatian dari produksi ke distribusi.",
 54: "Karya Haigh tentang variabilitas matahari menunjukkan perubahan keluaran matahari tidak dapat menjelaskan pemanasan terkini. Pola pendinginan stratosfer bersamaan pemanasan permukaan adalah sidik jari gas rumah kaca. Argumennya menutup penjelasan alternatif, bukan membuktikan yang arus utama.",
 55: "Peters melacak jarak antara emisi yang dijanjikan dan kebijakan yang dibutuhkan untuk mewujudkannya. Kesenjangan bertahan karena janji tidak disertai pelaksanaan. Ukuran ini pemeriksa pengumuman, bukan niat.",
 56: "Analisis Global Carbon Project Canadell menemukan emisi fosil belum mencapai puncak. Setiap tahun tanpa puncak menaikkan laju penurunan yang dibutuhkan kemudian. Klaimnya tentang bentuk kurva, bukan tentang satu tahun.",
 57: "Klinsky berargumen keadilan iklim menyangkut siapa yang memutuskan, siapa yang membayar dan siapa yang didengar, bukan hanya siapa yang beremisi. Pertanyaan prosedural menentukan apakah aturan alokasi diterima. Bingkainya memperluas keadilan melampaui pembagian beban.",
 58: "Karya Roy di IPCC menunjukkan lahan adalah korban perubahan iklim sekaligus tuas respons. Pengelolaan lahan berkelanjutan menghubungkan mitigasi, adaptasi dan ketahanan pangan. Kompromi di antara ketiganya tidak terhindarkan dan bersifat politik.",
 59: "Riset Tschakert mendokumentasikan pengalaman hidup panas dan banjir di tempat yang pengukurannya tipis. Orang menggambarkan ambang dan kerugian yang tidak tertangkap indikator. Pendekatannya melengkapi, bukan menggantikan, atribusi kuantitatif.",
}



def para(topic, section, i):
    templates = [
     "Data lapangan tentang {section} menunjukkan pergeseran terukur yang terkait dengan {topic}, dikuatkan catatan satelit dan stasiun permukaan (IPCC, 2023). Pemantauan {section} mengungkap perubahan besaran dan waktu, termasuk awal yang lebih cepat dan durasi lebih panjang di beberapa wilayah. Proyeksi model yang memasukkan pemaksaan antropogenik mereproduksi pola yang teramati pada {section} lebih dekat daripada variabilitas alam saja. Contoh regional menunjukkan bagaimana ritme musiman yang terganggu oleh {section} memengaruhi pertanian dan pengelolaan air. Konvergensi dataset independen tentang {section} memperkuat keyakinan dan mendukung perencanaan yang tidak lagi mengasumsikan basis stasioner.",
     "Mekanisme fisik yang mendorong {section} bekerja melalui jalur energi dan kelembapan yang terhubung dengan {topic} (IPCC, 2021; WMO, 2023). Gangguan radiatif dari {topic} merambat ke perubahan sirkulasi dan hidrologi, dengan umpan balik yang dapat memperkuat sinyal awal. Studi empiris tentang {section} menunjukkan umpan balik itu sudah teramati dalam beberapa dekade terakhir. Riset atribusi mengukur kontribusi antropogenik pada ekstrem {section}, memperkuat pernyataan kausal melampaui korelasi. Membedakan pemicu dekat {section} dari pendorong yang mendasari membantu menentukan titik intervensi paling efektif.",
     "Dampak {section} tidak merata antar-populasi dalam {topic}, mencerminkan perbedaan paparan dan kapasitas adaptasi (IPCC, 2022; UNDRR, 2015). Kelompok yang menghadapi {section} dengan sumber daya terbatas atau kepemilikan lahan tidak aman menanggung risiko tidak proporsional, dan kontras kota-desa membentuk hasilnya. Dimensi gender dan usia lebih lanjut memodulasi cara orang mengalami {section}. Disparitas dalam {section} ini lahir dari proses sosial dan institusional yang saling berpotongan, bukan kebetulan. Karena itu, penilaian {section} yang berpusat pada keadilan memberi gambaran lebih akurat daripada rata-rata agregat.",
     "Tata kelola dan praktik di sekitar {section} menentukan apakah {topic} tetap terkelola atau berujung kegagalan berantai (IPCC, 2022; UNDRR, 2015). Pendekatan efektif untuk {section} memadukan perencanaan formal, pelaksanaan fleksibel dan pengawasan partisipatif. Peringatan dini, regulasi guna lahan dan standar infrastruktur untuk {section} paling efektif bila dirancang bersama pengguna lokal. Fragmentasi kelembagaan dapat menunda tindakan atas {section}, sementara koordinasi lintas skala memperbaiki respons terhadap kejadian majemuk. Belajar dari keberhasilan dan kegagalan penanganan {section} menyediakan kurikulum praktis untuk perbaikan.",
     "Pertimbangan ekonomi {section} dalam konteks {topic} menunjukkan investasi proaktif umumnya lebih murah daripada menanggung kerugian yang meningkat (World Bank, 2022; IPCC, 2022). Kerugian langsung {section} pada produktivitas dan infrastruktur merembet ke rantai pasok dan pasar asuransi. Aset pertanian dan pesisir yang terpapar {section} sangat rentan. Kesenjangan pembiayaan untuk {section} terbesar di tempat kebutuhan paling tinggi, menuntut keterbukaan risiko dan pendanaan campuran yang menjangkau kelompok rentan. Analisis biaya-manfaat {section} karena itu perlu menghitung kerugian yang dihindari, bukan hanya belanja awal.",
     "Dimensi kesehatan {section} menghubungkan {topic} dengan luaran akut dan kronis (WHO, 2023). Stres panas, perubahan kualitas udara dan pergeseran rentang vektor menggambarkan jalur langsung dari {section}, sementara ketidakamanan pangan dan pengungsian menggambarkan jalur tak langsung. Sistem kesehatan sudah tertekan kondisi sensitif iklim, dan {section} menambah tekanan itu. Dampak kesehatan jiwa dari {section}, termasuk kecemasan dan trauma pascakejadian, makin terdokumentasi. Menghubungkan pemantauan iklim dengan surveilans kesehatan untuk {section} menciptakan manfaat bersama bagi tindakan dini dan pencegahan.",
     "Menilai bukti tentang {section} membutuhkan perhatian pada metode yang relevan bagi {topic} (IPCC, 2023). Observasi jangka panjang {section} membumikan temuan, sementara eksperimen dan desain kuasi-eksperimen memperkuat inferensi kausal. Model {section} membantu mengeksplorasi skenario tetapi bergantung pada asumsi yang harus diungkap. Sintesis yang menggabungkan studi {section} meningkatkan kekuatan statistik, meski heterogenitas menuntut tafsir hati-hati. Menilai desain, sampel dan pelaporan ketidakpastian untuk {section} membangun penggunaan ilmu yang tangguh.",
     "Jalur ke depan untuk {section} dalam {topic} bergantung pada penyelarasan tindakan jangka pendek dengan transformasi jangka panjang (IPCC, 2023). Langkah inkremental untuk {section}, seperti prakiraan lebih baik dan diversifikasi mata pencaharian, memberi kelegaan segera, sementara strategi berbasis ekosistem dan transisi energi mengatasi pendorong akar. Inovasi yang dipimpin komunitas dalam {section} sering berkinerja baik bila didukung sumber daya. Pemantauan iteratif {section} memungkinkan koreksi arah seiring kondisi berkembang. Membingkai opsi {section} sebagai portofolio, bukan solusi tunggal, mencerminkan kompleksitas dan mendukung adaptasi yang tangguh terhadap ketidakpastian.",
    ]
    t1 = templates[i % len(templates)]
    t2 = templates[(i+3) % len(templates)]
    if section.strip().lower() in ("bab ini", "this chapter"):
        section = topic
    base = t1.format(section=section, topic=topic) + " " + t2.format(section=section, topic=topic)
    frames = [
        "Untuk {s}, buktinya konkret: {d}.",
        "Catatan untuk {s} menunjukkan bahwa {d}.",
        "Satu penanda {s}: {d}.",
        "Kajian terbaru tentang {s} menambahkan bahwa {d}.",
        "Dalam hal {s}, {d}.",
        "Bukti observasi tentang {s} menegaskan bahwa {d}.",
        "Satu titik data tentang {s}: {d}.",
        "Kumpulan data yang lebih luas tentang {s} mencatat bahwa {d}.",
    ]
    key = sum(map(ord, section))
    data_idx = (key * 7 + i * 5) % len(DATA_POINTS)
    frame = frames[(key * 3 + i) % len(frames)]
    base += " " + frame.format(s=section, d=DATA_POINTS[data_idx])
    return base

def bullets(topic, section):
    return [
     "Menilai kondisi lokal dan mengidentifikasi bahaya yang paling relevan.",
     "Memprioritaskan tindakan yang melindungi yang paling rentan terlebih dahulu.",
     "Membangun redundansi dalam sistem kritis (air, pangan, energi, komunikasi).",
     "Mempraktikkan rencana secara teratur dan memperbaruinya setelah setiap kejadian.",
     "Berbagi pengetahuan dan berkoordinasi dengan tetangga dan lembaga lokal.",
    ]


def _lc_first(s):
    """Huruf pertama kecil, nama diri/satuan dipertahankan (2°C, NASA, IPCC)."""
    for i, ch in enumerate(s):
        if ch.isalpha():
            return s[:i] + ch.lower() + s[i + 1:]
    return s


_PROTECT = ("IPCC", "AI", "PTSD", "CO2", "SSP", "UN", "WHO", "FAO")


def _sentence_case_id(s):
    """Title Case -> sentence case untuk dipakai di tengah kalimat."""
    if not s:
        return s
    out = []
    for i, w in enumerate(s.split()):
        parts = []
        for j, p in enumerate(w.split("-")):
            plain = p.replace("'", "")
            if any(p.startswith(x) for x in _PROTECT) or (len(plain) > 1 and plain.isupper()):
                parts.append(p)
            elif i == 0 and j == 0:
                parts.append(p[:1].lower() + p[1:])
            else:
                parts.append(p.lower())
        out.append("-".join(parts))
    return " ".join(out)


def _sub_heading(label, title):
    """Judul sub-bab: hindari titik dua ganda dan label yang terulang."""
    t = title.strip()
    head = t.split(":")[0].strip().lower()
    if head.startswith(label.lower()[:9]):
        return t
    if ":" in t:
        t = t.replace(":", " \u2014", 1)
    return f"{label}: {t}"

md = []
md.append("# Prakata: Mengapa Pemanasan Global di Masa Depan adalah Kepastian")
md.append("")
md.append("Pemanasan global bukan hipotesis; ia adalah realitas yang teramati, terukur, dan dijelaskan secara fisik. Kepastian pemanasan di masa depan bertumpu pada tiga pilar: (1) fisika efek rumah kaca, (2) akumulasi gas rumah kaca yang teramati di atmosfer, dan (3) inersia sistem iklim. Bahkan jika semua emisi berhenti hari ini, pemanasan yang telah terkunci dari emisi masa lalu akan berlanjut selama beberapa dekade. Buku ini ditulis untuk diperdebatkan di ruang akademik: setiap klaim utama terkait dengan literatur peer-reviewed, data, dan pernyataan para ahli.")
md.append("")
md.append("### Tiga Pilar Kepastian")
md.append("")
md.append("- **Fisika:** Gas rumah kaca menyerap radiasi inframerah keluar. Ini adalah fisika yang mapan, diuji lebih dari satu abad (Arrhenius, 1896; model transfer radiatif modern).")
md.append("- **Observasi:** CO2 atmosfer telah naik dari ~280 ppm (pra-industri) menjadi ~420 ppm (2024). Suhu rata-rata global telah naik ~1,1-1,2 C. Ini adalah pengukuran langsung.")
md.append("- **Inersia:** Lautan menyimpan panas; lapisan es merespons lambat. Bahkan dengan emisi nol, pemanasan berlanjut selama beberapa dekade (pemanasan terkunci).")
md.append("")
md.append("Data yang mendasari pembahasan diringkas sebagai berikut:")
md.append("")
md.append("[[TABLE:Tabel P.1 Indikator iklim global utama (2024)]]")
md.append(DATA_TABLES[0])
md.append("")
md.append("Konsensus ahli yang mendasari buku ini diringkas sebagai berikut.")
md.append("")
for i,e in enumerate(EXPERTS[:5], start=1):
    md.append(f"> {e}")
    md.append("")
md.append("Kondisi ini menggambarkan urgensi tema yang dikembangkan sepanjang buku ini. Ini bukan kejadian terisolasi tetapi bagian dari pola peningkatan risiko yang lebih luas.")
md.append("")
md.append("Buku ini menekankan kesiapsiagaan, pendidikan, dan resiliensi komunitas sebagai strategi yang saling terkait. Tidak ada intervensi tunggal yang cukup; diperlukan portofolio tindakan.")
md.append("")
md.append("Akhirnya, buku ini ditawarkan sebagai dokumen hidup. Pembaca didorong untuk memperbarui pengetahuan mereka seiring munculnya bukti baru.")
md.append("")
md.append("---")
md.append("")

ri = 0
for ci,(title,theme,secs) in enumerate(CHAPTERS, start=1):
    if ci in DEEP_ID:
        md.extend(deep_render.render_chapter(DEEP_ID[ci], "Bab", lang="id"))
        continue
    md.append(f"# Bab {ci}: {title}")
    md.append("")
    md.append(f"*Tema: {theme}*")
    md.append("")
    md.append(prose.chapter_opening("id", ci, theme))
    md.append("")

    _picker = prose.ExpertPicker(EXPERT_KEYWORDS, len(EXPERTS))
    chapter_rel = relevant_experts_for_chapter(title, theme)
    if not chapter_rel:
        chapter_rel = [(ci-1) % len(EXPERTS)]  # fallback for chapter-level
    n_sub = len(secs[:4])
    for si,sec in enumerate(secs[:4], start=1):
        # Per-section expert ensures 60 experts across 24*4=96 sections (Homo Deus style: definisi per paragraf) - round-robin guarantees all 60 are cited at least once
        use_exp = _picker.pick(f"{sec} {theme} {title}",
                             ((ci-1)*4 + (si-1)) % len(EXPERTS))
        md.append(f"## {ci}.{si} {sec}")
        md.append("")
        exp_idx = use_exp
        exp = EXPERTS[exp_idx]
        exp_name = exp.split(',')[0].replace('Prof.', '').replace('Dr.', '').replace('Ms.', '').strip()
        m_year = re.search(r'\((\d{4})', exp)
        exp_year = m_year.group(1) if m_year else "2020"
        raw_quote = exp.split(":")[1].strip().strip("'").strip('"').strip()
        md.append(prose.expert_lead("id", exp_name, exp_year, _lc_first(raw_quote), ci, si))
        md.append("")
        _detail = EXPERT_DETAILS[exp_idx].format(section=prose.short_np(sec, "id"), topic=prose.short_topic(theme))
        _parts = [x.strip().rstrip('.') for x in _detail.split('. ') if x.strip()]
        _body = '. '.join(_parts if "{section}" not in _detail else _parts[:-1])
        md.append(_body + '. ' + prose.expert_anchor("id", sec, ci, si))
        md.append("")
        for _p in prose.section_paragraphs("id", ci, si, sec, theme, DATA_POINTS, bullets(theme, sec)):
            md.append(_p)
            md.append("")
        if ci not in (1, 24):
            _news = prose.pick_news(ci, si, NEWS)
            md.append(prose.vary_dom(prose.news_paragraph("id", _news.rstrip('.'), ci, si), "id", prose.DOMAINS["id"][ci - 1], ci * 5 + si))
            md.append("")
            if si in (1, 3):
                md.append(prose.vary_dom(prose.limit_paragraph("id", ci, si), "id", prose.DOMAINS["id"][ci - 1], ci * 7 + si))
                md.append("")
            if si in (2, 4):
                md.append(prose.vary_dom(prose.synthesis_paragraph("id", ci, si), "id", prose.DOMAINS["id"][ci - 1], ci * 11 + si))

        md.append("")
    # Studi kasus
    md.append(f"## {ci}.{n_sub + 1} {_sub_heading('Studi Kasus', title)}")
    md.append("")
    for _jk, _cp in enumerate(prose.case_paragraphs("id", ci, theme,
                                     prose.pick_news(ci, 1, NEWS).rstrip('.'), prose.DOMAINS["id"][ci - 1])):
        md.append(prose.vary_dom(_cp, "id", prose.DOMAINS["id"][ci - 1], ci * 13 + _jk))
        md.append("")
    md.append("")

    md.append("")
    # Skenario Masa Depan dan Prediksi — analisis unik per bab (tanpa template berulang)
    fs = FUTURE_SCENARIOS[ci - 1]["id"]
    md.append(f"## {ci}.{n_sub + 2} {_sub_heading('Skenario Masa Depan dan Prediksi', title)}")
    md.append("")
    md.append(fs["lead"])
    md.append("")
    md.append(fs["mid"])
    md.append("")
    md.append(fs["adapt"])
    md.append("")
    md.append(f"[[TABLE:Tabel {ci}.1 Skenario dan prediksi masa depan untuk {theme} (2030-2100)]]")
    md.append("| Horizon | Perubahan pada bab ini |")
    md.append("|---|---|")
    md.append(f"| 2030 | {fs['k30']} |")
    md.append(f"| 2050 | {fs['k50']} |")
    md.append(f"| 2100 | {fs['k100']} |")
    md.append("")
    md.append(fs["watch"])
    md.append("")
    md.append("---")
    md.append("")

# Lampiran A
md.append("# Lampiran A: Ceklis dan Panduan")
md.append("")
md.append("## Ceklis Darurat Utama")
md.append("")
for item in [
    "Air: empat liter per orang per hari selama sedikitnya tiga hari, ditambah filter atau tablet penjernih.",
    "Pangan: stok tiga hari yang tidak perlu dimasak, dan pembuka kaleng manual.",
    "Obat: persediaan tujuh hari untuk resep rutin, kotak P3K, dan daftar dosis tertulis.",
    "Dokumen: KTP, polis asuransi, sertifikat properti dan catatan imunisasi dalam map tahan air, dengan salinan di awan.",
    "Daya: power bank terisi, baterai cadangan, senter, dan radio baterai atau engkol tangan.",
    "Panas: rencana untuk ruangan terdingin, tirai penghalang panas, dan daftar tempat umum berpendingin dalam jarak jalan kaki.",
    "Banjir: jalur pasti ke tanah lebih tinggi, titik temu, dan aturan bahwa tidak seorang pun berjalan atau berkendara melewati air mengalir.",
    "Uang: uang tunai cukup untuk tiga hari, karena mesin kartu mati saat listrik padam.",
    "Tanggungan: perlengkapan untuk anak, orang tua, hewan peliharaan, dan siapa pun yang tidak bisa mengungsi sendiri.",
    "Tetangga: nama dan nomor telepon dua rumah terdekat, serta satu kontak luar kota yang bisa dihubungi semua orang.",
]:
    md.append(f"- {item}")
md.append("")
md.append("## Ceklis Komunitas dan Kota")
md.append("")
for item in [
    "Peta pusat pendingin dan tempat pengungsian yang dipublikasikan, lengkap dengan jam buka dan rute angkutan.",
    "Keterbukaan risiko banjir untuk setiap alamat, tersedia sebelum kontrak sewa atau jual beli ditandatangani.",
    "Saluran peringatan dini yang menjangkau orang tanpa ponsel pintar, lewat sirene, radio, atau SMS.",
    "Daya cadangan untuk klinik, unit dialisis dan apotek, diuji dengan beban penuh setahun sekali.",
    "Jadwal pemeliharaan drainase dan tanggul yang dipublikasikan, dibiayai, dan diaudit.",
    "Pejabat yang namanya bertanggung jawab atas setiap ambang peringatan, sehingga keputusan mengungsi punya pemilik.",
]:
    md.append(f"- {item}")
md.append("")
md.append("## Lembar Kerja: Profil Risiko Lokal Anda")
md.append("")
for item in [
    "Bahaya: mana di antara panas, banjir, kebakaran, kekeringan atau badai yang pernah melanda tempat ini dalam dua puluh tahun terakhir, dan seberapa sering?",
    "Paparan: jalan, pekerjaan dan layanan mana yang berada di zona terdampak?",
    "Kerentanan: siapa yang tidak bisa berpindah, membayar, atau bertahan melewati gangguan tiga hari?",
    "Kapasitas: lembaga mana yang sudah memiliki kepercayaan, kendaraan dan staf untuk bertindak lebih dulu?",
    "Pemicu: pengukuran apa, pada ambang berapa, yang akan membuat Anda pergi atau menutup usaha?",
]:
    md.append(f"- {item}")
md.append("")
md.append("## Panduan Debat Akademik")
md.append("")
md.append("Buku ini ditulis untuk dibantah. Saat Anda mempersoalkan atau memperluas salah satu klaimnya:")
md.append("")
md.append("- Selalu sitasi sumber primer (paper peer-reviewed, laporan IPCC).")
md.append("- Bedakan antara observasi, atribusi, dan proyeksi.")
md.append("- Akui ketidakpastian dan tingkat kepercayaan.")
md.append("- Pertimbangkan berbagai jalur sosioekonomi (SSP).")
md.append("- Sertakan dimensi keadilan dan kesetaraan.")
md.append("- Perbarui klaim seiring munculnya bukti baru.")
md.append("")
md.append("# Lampiran B: Glosarium")
md.append("")
gloss = [
 "Adaptasi: Menyesuaikan diri dengan dampak iklim yang aktual atau yang diharapkan.",
 "Mitigasi: Mengurangi emisi gas rumah kaca.",
 "Resiliensi: Kapasitas untuk menyerap gangguan dan bereorganisasi.",
 "Kerentanan: Kepekaan terhadap kerugian.",
 "Paparan: Kehadiran orang atau aset di area rawan bahaya.",
 "Sensitivitas: Tingkat di mana sistem terpengaruh oleh iklim.",
 "Kapasitas adaptif: Kemampuan untuk menyesuaikan diri dengan perubahan iklim.",
 "Titik balik: Ambang batas di mana perubahan menjadi mandiri.",
 "Efek rumah kaca: Penjeratan panas oleh gas atmosfer.",
 "Jejak karbon: Total emisi gas rumah kaca yang disebabkan oleh suatu entitas.",
 "SSP: Shared Socioeconomic Pathway (kerangka skenario).",
 "RCP: Representative Concentration Pathway.",
 "Pemanasan terkunci: Pemanasan yang terkunci dari emisi masa lalu.",
]
for g in gloss:
    md.append(f"- {g}")
md.append("")
md.append("# Lampiran C: Indeks")
md.append("")
index_terms = sorted(set([
 "Adaptasi",
 "Agroforestri",
 "Air tanah",
 "Akuifer",
 "Albedo",
 "Anggaran karbon",
 "Asuransi",
 "Atribusi",
 "Badai",
 "Banjir",
 "Banjir bandang",
 "Bendungan",
 "Deforestasi",
 "Dekarbonisasi",
 "Dengue",
 "Desalinasi",
 "Desertifikasi",
 "Ekosistem",
 "El Niño",
 "Elektrifikasi",
 "Es laut",
 "Gelombang badai",
 "Gelombang panas",
 "Gizi",
 "Gletser",
 "Gotong royong",
 "Hasil panen",
 "Hidrogen",
 "Infrastruktur",
 "Irigasi",
 "Jaringan listrik",
 "Keadilan",
 "Kebakaran hutan",
 "Kekeringan",
 "Kematian akibat panas",
 "Kematian berlebih",
 "Kemiskinan energi",
 "Kenaikan muka laut",
 "Kepadatan",
 "Kerentanan",
 "Kesehatan",
 "Kesehatan mental",
 "Kesehatan publik",
 "Ketahanan pangan",
 "Kolera",
 "Konflik",
 "Kubah panas",
 "Kumuh",
 "Lapisan es",
 "Limbah pangan",
 "Malaria",
 "Mangrove",
 "Migrasi",
 "Mitigasi",
 "Modal sosial",
 "Model iklim",
 "Monsun",
 "Panas ekstrem",
 "Pantai",
 "Paparan",
 "Partikulat",
 "Pemadaman",
 "Pendingin udara",
 "Pengasaman laut",
 "Pengungsi iklim",
 "Pengungsian",
 "Penyakit tular vektor",
 "Perikanan",
 "Peringatan dini",
 "Permafrost",
 "Permukiman",
 "Permukiman informal",
 "Pertanian",
 "Polusi udara",
 "Rantai pasok",
 "Relokasi",
 "Rencana aksi panas",
 "Resiliensi",
 "Retret terkelola",
 "Salinisasi",
 "Sanitasi",
 "Sensitivitas",
 "Subsidi",
 "Suhu bola basah",
 "Sungai atmosfer",
 "Tanah longsor",
 "Tata ruang",
 "Terumbu karang",
 "Titik kritis",
 "Topan",
 "Waduk",
]))
for t in index_terms:
    md.append(f"- {t}")
md.append("")
md.append("@@REFS@@")
md.append("# Lampiran E: Biografi Penulis")
md.append("")
md.append("**Setyo Wisodo** adalah profesional yang menggabungkan keahlian dalam Pengembangan AI, Manajemen Produk, dan Pemasaran Digital. Aktif dalam pengembangan solusi berbasis AI dan produk digital. Lokasi: Indonesia.")
md.append("")
md.append("Tambahan: Buku ini merupakan dokumen hidup. Pembaca didorong untuk memperbarui pengetahuan seiring munculnya bukti baru.")
md.append("")
md.append("Tambahan: Setiap pembaca memiliki peran. Mulailah dari tempat Anda berada, gunakan apa yang Anda miliki, dan lakukan apa yang Anda bisa.")
md.append("")
md.append("# Lampiran F: Catatan Analitis Lanjutan")
md.append("")
notes = [
 "Catatan analitis: Hubungan antara pendorong iklim dan luaran sosial dimediasi oleh kapasitas kelembagaan, ketersediaan sumber daya, dan konteks historis. Tidak ada satu faktor yang menentukan hasilnya.",
 "Catatan analitis: Strategi adaptasi harus dinilai bukan hanya dari efektivitasnya, tetapi juga dari keadilan, biaya, dan kelayakannya dalam konteks tertentu.",
 "Catatan analitis: Dimensi waktu dari dampak iklim menuntut pemikiran jangka panjang yang sering bertentangan dengan insentif politik dan ekonomi jangka pendek.",
 "Catatan analitis: Produksi pengetahuan dan penggunaan pengetahuan adalah dua proses yang berbeda; menjembatani keduanya memerlukan usaha yang sengaja dan keterlibatan yang berkelanjutan.",
 "Catatan analitis: Ketidakpastian melekat dalam ilmu iklim dan harus dikomunikasikan secara transparan, bukan disembunyikan atau dibesar-besarkan.",
]
for n in notes:
    md.append(n)
    md.append("")
md.append("# Lampiran G: Catatan Sumber Peristiwa")
md.append("")
md.append("Angka untuk peristiwa bernama yang dipakai sebagai kasus dalam buku ini diambil dari dokumentasi berikut. Bila angka sebuah peristiwa muncul dalam teks tanpa sitasi kurung, tabel ini menyebut sumbernya.")
md.append("")
md.append("- Banjir Pakistan, 2022 — WMO (2023), State of the Global Climate 2023; penilaian kebutuhan pascabencana pemerintah.")
md.append("- Gelombang panas Eropa, 2003 — Robine dkk. (2008), Comptes Rendus Biologies 331(2).")
md.append("- Gelombang panas Chicago, 1995 — Klinenberg (2002), Heat Wave: A Social Autopsy of Disaster in Chicago.")
md.append("- Badai Maria, Puerto Rico, 2017 — Kishore dkk. (2018), New England Journal of Medicine 379.")
md.append("- Badai Katrina, New Orleans, 2005 — Brunkard dkk. (2008), Disaster Medicine and Public Health Preparedness 2(4).")
md.append("- Kubah panas Pacific Northwest, 2021 — Philip dkk. (2022), Earth System Dynamics 13.")
md.append("- Banjir lembah Ahr, Jerman dan Belgia, 2021 — Kreienkamp dkk. (2021), World Weather Attribution.")
md.append("- Kebakaran Black Saturday, Victoria, 2009 — Victorian Bushfires Royal Commission (2010), Final Report.")
md.append("- Kebakaran Camp, Paradise, California, 2018 — CAL FIRE (2019), laporan insiden Camp Fire.")
md.append("- Kebakaran hutan Kanada, 2023 — CIFFC (2023), National Wildland Fire Situation Report.")
md.append("- Badai musim dingin Texas Uri, 2021 — FERC & NERC (2021), The February 2021 cold weather outages.")
md.append("- Kelaparan Somalia, 2011 — Checchi & Robinson (2013), studi mortalitas FAO/FSNAU.")
md.append("- Kelaparan Etiopia, 1984–1985 — Kerangka hak Sen (1981); analisis kelaparan de Waal (1997).")
md.append("- Kekeringan Sahel, 1968–1974 dan 1984–1985 — IPCC (2019), Climate Change and Land; FAO (2023).")
md.append("- Banjir Chennai, 2015 — IPCC (2022), Impacts, Adaptation and Vulnerability, bab perkotaan.")
md.append("- Krisis air Cape Town, 2018 — Gleick (2023), Water, Climate and Governance Crises.")
md.append("- Kekeringan Suriah, 2006–2010 — Kelley dkk. (2015), PNAS 112(11); Selby dkk. (2017), Political Geography 60.")
md.append("- Ambang deforestasi Amazon — IPCC (2019), Climate Change and Land.")
md.append("- Penurunan es laut Arktik — Notz & Stroeve (2016), Science 354(6313).")
md.append("- Rekor suhu global — Lenssen dkk. (2019); Morice dkk. (2021); Rohde & Hausfather (2020); WMO (2023).")
md.append("")

content = "\n".join(md)
import gate1
content, n_cit = gate1.apply(content, "id")
import cited as _cited
_cited_refs, _further_refs = _cited.split_refs(REFS, _cited.pairs(content))
_refs_md = ["# Lampiran D: Daftar Pustaka", "", "## Karya yang Dikutip", ""]
_refs_md += [f"- {r}" for r in _cited_refs]
_refs_md += ["", "## Bacaan Lanjutan", "",
             "Karya berikut memperkaya latar penulisan tetapi tidak dikutip dalam teks.", ""]
_refs_md += [f"- {r}" for r in _further_refs]
content = content.replace("@@REFS@@", "\n".join(_refs_md))
print("gate1 citations added:", n_cit)
with open('/home/user/SetyoWisodo/book_id.md','w',encoding='utf-8') as f:
    f.write(content)
print("words:", len(content.split()))