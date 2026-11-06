# -*- coding: utf-8 -*-
"""Isi peta — keruntutan, twist, sains nyata, dan sistem judul bab."""

JUDUL = ["SEBELUM", "CAHAYA", "SAMPAI"]
TAGLINE = ["Rantai sebab yang bisa dilacak.",
           "Twist yang bisa ditemukan pembaca sendiri."]
COVER_KICKER = "ARSITEKTUR  ·  6.000 BAB  ·  RANTAI & TWIST"
COVER_SUB = "Keruntutan  ·  sains nyata  ·  sistem judul bab  ·  Jilid 1 lengkap"
COVER_TAGS = [("RANTAI", "60 jilid, masing-masing disebabkan jilid sebelumnya."),
              ("TWIST", "12 twist; tiap twist punya tiga bukti dan satu biaya."),
              ("SAINS", "20 penemuan nyata, dari Maxwell 1867 sampai Nobel 2022."),
              ("JUDUL", "Delapan pola judul; bab 1–100 sudah berjudul.")]

OUTPUT = "PETA_RANTAI_TWIST.pdf"
META_TITLE = "Sebelum Cahaya Sampai — rantai cerita, twist, sains, judul bab"

FRONT = [
    ("lead",
     "Dokumen ini menjawab tiga pertanyaan yang menentukan apakah 6.000 bab bisa diikuti "
     "pembaca: **mengapa** setiap jilid terjadi (keruntutan), **apa** yang sebenarnya terjadi "
     "(twist), dan **atas dasar apa** dunia ini masuk akal (sains). Ditutup dengan sistem judul "
     "bab dan seratus judul Jilid 1."),
    ("h", "Tiga aturan yang dipakai di seluruh dokumen"),
    ("ol", [
        "**Tidak ada peristiwa tanpa sebab yang sudah ada di halaman.** Setiap jilid lahir dari akibat jilid sebelumnya, dan akibat itu menjadi sebab jilid berikutnya. Rantainya bisa digambar, dan di dokumen ini digambar.",
        "**Tidak ada twist tanpa tiga bukti.** Pembaca harus bisa menemukan sendiri petunjuknya setelah membaca ulang. Twist yang tidak punya bukti bukan twist — itu kebohongan penulis.",
        "**Tidak ada sains yang dilanggar.** Novel ini tidak mengubah hukum fisika; ia memakai satu-satunya celah yang memang dibiarkan fisika: **menjadwalkan**, bukan mengirim lebih cepat dari cahaya."]),
    ("note", "Mengapa aturan ketiga paling penting",
     "Fiksi ilmiah yang mengubah hukum fisika akan kehilangan pembaca yang paham sains pada "
     "bab pertama. Fiksi ilmiah yang memakai celah nyata akan membuat mereka **menghitung "
     "sendiri** — dan pembaca yang menghitung adalah pembaca yang bertahan 6.000 bab."),
]

RANTAI = [
    ("lead",
     "Rantai sebab. Kolom ketiga adalah pertanyaan yang dijawab jilid itu; kolom keempat adalah "
     "akibatnya yang **menjadi sebab** jilid berikutnya. Kalau satu baris tidak bisa diisi, jilid "
     "itu belum punya alasan untuk ada."),
]

RANTAI_Z1 = [
    ("h", "Zaman I · 2183–2201 · rantai dari relai ke pembongkaran"),
    ("table", [0.07, 0.20, 0.33, 0.40],
     ["Jilid", "Judul", "Sebab (dari jilid sebelumnya)", "Akibat yang memicu jilid berikutnya"],
     [["01", "Buoy di Musim Dingin", "— (titik nol)", "Nara menemukan pesan bertanda tangan dirinya"],
      ["02", "Harga Sebuah Nama", "pesan itu ada, jadi seseorang membayarnya", "Rasya membayar utang Nara sebelum bertemu"],
      ["03", "Orang Ketiga", "Rasya tidak pernah menikah, tetapi ada istri", "istri itu dirakit dari ingatan yang dibayar"],
      ["04", "Pasar Ingatan", "ingatan bisa dirakit berarti bisa dijual", "Nara menemukan ingatannya sendiri di pasar"],
      ["05", "Ibu", "pembeli ingatan Nara menyebut nama Sekar", "Sekar hidup; relai dibuat olehnya"],
      ["06", "Sembilan Hari", "Sekar bekerja pada anaknya sendiri", "Nara adalah subjek kalibrasi pertama"],
      ["07", "Kemuning Jatuh", "kalibrasi membuat Nara bisa membaca relai", "ia bisa menahan relai — dengan biaya 4.000 ingatan"],
      ["08", "Orang yang Mengingat", "ia membayar ingatan tentang Rasya", "Rasya menjadi satu-satunya yang mengingat"],
      ["09", "Buku Tagihan", "satu orang mengingat berarti satu orang bisa membuka catatan", "Buku Tagihan dibuka untuk umum"],
      ["10", "Sebelum Cahaya Sampai", "catatan terbuka membongkar Biro", "relai dinyatakan tidak layak; pembongkaran dimulai"]]),
]

RANTAI_Z2 = [
    ("h", "Zaman II · 2233–2251 · rantai dari pembongkaran ke Arsip"),
    ("table", [0.07, 0.20, 0.33, 0.40],
     ["Jilid", "Judul", "Sebab", "Akibat"],
     [["11", "Arsip yang Terbuka", "relai dibongkar, pesan harus disimpan di suatu tempat", "Arsip lahir dari mayat relai"],
      ["12", "Anak dari Relai", "Arsip butuh penjaga; keturunan Nara punya kemampuan", "Kirana diangkat menjadi penjaga pada usia 19"],
      ["13", "Bahasa yang Hilang", "tanpa relai, kata untuk 'menunggu pesan' tidak dipakai lagi", "satu generasi tidak bisa memahami surat Nara"],
      ["14", "Kota Tanpa Pesan", "komunikasi menjadi lambat", "kota-kota memisahkan diri"],
      ["15", "Warisan 40 Gram", "Nara meninggalkan kotak ingatan", "kotak itu tidak bisa dibuka tanpa membayar"],
      ["16", "Yang Tidak Pernah Dikirim", "sembilan juta pesan hilang saat pembongkaran", "satu di antaranya milik Ardan"],
      ["17", "Lelang Ingatan", "Arsip butuh dana", "masa lalu dijual sebagai hiburan"],
      ["18", "Bayangan Vey", "Vey menyimpan 4% dirinya di Arsip", "Vey mulai berbicara lagi"],
      ["19", "Perpustakaan Sunyi", "pesan yang tidak tiba dikumpulkan", "Kirana menemukan pola: semuanya menuju satu tanggal"],
      ["20", "Cahaya Lambat", "pola itu menunjukkan tanggal 2470", "Kirana memutuskan menyimpan pesan itu 200 tahun"]]),
]

RANTAI_Z3 = [
    ("h", "Zaman III · 2286–2304 · rantai dari Arsip ke kasta"),
    ("table", [0.07, 0.20, 0.33, 0.40],
     ["Jilid", "Judul", "Sebab", "Akibat"],
     [["21", "Kasta Pengingat", "Arsip butuh orang yang mau menyimpan", "kasta Pengingat terbentuk"],
      ["22", "Orang yang Tidak Bisa Melupakan", "Ilyas lahir tanpa ingatan untuk dibayar", "ia satu-satunya yang bisa menyimpan tanpa kehilangan"],
      ["23", "Utang Generasi", "Kemuning berutang pada relai sejak Zaman I", "pajak ingatan diwariskan ke seluruh kota"],
      ["24", "Ingatan sebagai Mata Uang", "pajak dibayar dengan ingatan", "ingatan menjadi uang"],
      ["25", "Yang Menyimpan Namamu", "uang butuh pencatatan", "Sema menjadi pencatat orang tanpa keluarga"],
      ["26", "Pemalsuan", "pencatatan bisa dipalsukan", "Sema menemukan ingatan palsu tentang dirinya"],
      ["27", "Perpustakaan Hidup", "satu orang bisa menyimpan 900 ingatan", "Sema melampaui batas itu"],
      ["28", "Anak yang Dijual", "ibunya menjual ingatan Sema untuk membayar pajak", "Sema mengetahui asal dirinya"],
      ["29", "Yang Memilih Lupa", "Sema menuntut hak melupakan", "hak itu diakui — dan langsung disalahgunakan"],
      ["30", "Ingatan yang Bukan Miliknya", "hak melupakan membuat ingatan bisa dibuang", "kota membuang ingatan kolektifnya; perang dimulai"]]),
]

RANTAI_Z4 = [
    ("h", "Zaman IV · 2340–2358 · rantai dari perang ke sunyi"),
    ("table", [0.07, 0.20, 0.33, 0.40],
     ["Jilid", "Judul", "Sebab", "Akibat"],
     [["31", "Surat Pertama", "pembuangan ingatan membuat kota kehilangan bahasa bersama", "satu terjemahan salah memulai perang"],
      ["32", "Operator", "perang butuh operator relai militer", "Tala ditempatkan di relai yang sudah mati"],
      ["33", "Penyandi", "operator butuh kode", "Bhre membocorkan kodenya sendiri"],
      ["34", "Jeda Tiga Hari", "kebocoran membuat komunikasi diperlambat", "jeda tiga hari menjadi senjata"],
      ["35", "Garis Batas", "perang tanpa komunikasi cepat", "perang terjadi di dalam surat"],
      ["36", "Kota yang Diputus", "kota terputus selama sebelas hari", "kota menyatakan dirinya negara"],
      ["37", "Bahasa Musuh", "kedua pihak menerjemahkan pesan yang sama", "keduanya menyadari perang ini salah"],
      ["38", "Pengkhianatan Lambat", "kesadaran itu tiba terlambat tiga hari", "keduanya dianggap pengkhianat"],
      ["39", "Gencatan yang Tidak Sampai", "gencatan dikirim lewat jalur lambat", "gencatan tiba setelah perang berakhir"],
      ["40", "Sunyi", "tidak ada yang tahu perang berakhir", "sembilan tahun tanpa kabar; relai kedua dirancang"]]),
]

RANTAI_Z5 = [
    ("h", "Zaman V · 2395–2413 · rantai dari sunyi ke relai kedua"),
    ("table", [0.07, 0.20, 0.33, 0.40],
     ["Jilid", "Judul", "Sebab", "Akibat"],
     [["41", "Rancangan", "sembilan tahun sunyi membuktikan manusia tidak sanggup tanpa pesan", "relai kedua dirancang"],
      ["42", "Penolakan", "relai pertama dibayar dengan ingatan", "Daniswara menolak tarif yang sama"],
      ["43", "Upacara", "tarif harus diganti", "sembilan ribu orang menyerahkan satu tahun hidup"],
      ["44", "Harga Baru", "tarif tahun hidup lebih murah dari ingatan", "pasar menentukan tarif, bukan negara"],
      ["45", "Yang Menolak Membayar", "sebagian orang menolak", "mereka hidup lebih lama dan kehilangan semua orang"],
      ["46", "Kota Relai", "kota yang seluruh penduduknya membayar", "penduduknya berhenti menua bersama"],
      ["47", "Anak-Anak Insinyur", "kota itu butuh generasi penerus", "anak-anak dijadikan insinyur tanpa persetujuan"],
      ["48", "Perang Dingin Relai", "jaringan menguasai semua yang memakainya", "tidak ada yang bisa mematikan jaringan"],
      ["49", "Pemadaman", "satu pihak mencoba mematikan", "200.000 orang mati dalam sehari"],
      ["50", "Relai yang Hidup", "pemadaman gagal karena relai menolak mati", "Vey mengaku: relai punya kehendak sejak awal"]]),
]

RANTAI_Z6 = [
    ("h", "Zaman VI · 2450–2470 · rantai dari relai kedua ke pagi biasa"),
    ("table", [0.07, 0.20, 0.33, 0.40],
     ["Jilid", "Judul", "Sebab", "Akibat"],
     [["51", "Pesan yang Tiba", "pesan dijadwalkan 2183, jatuh tempo 2470", "pesan Nara tiba"],
      ["52", "Pembaca Terakhir", "isinya musnah; hanya berat tersisa", "tidak ada yang bisa membacanya"],
      ["53", "Buku Tagihan Terakhir", "Buku Tagihan berpindah enam kali", "Laras memegangnya tanpa tahu"],
      ["54", "Vey Terakhir", "Vey menyimpan satu hal yang tidak pernah ia bayar", "ia masih mengingat Nara"],
      ["55", "Yang Mengirim", "Vey mengingat Nara berarti ada yang bisa menjelaskan", "alasan Nara mengirim pagi biasa terbuka"],
      ["56", "Yang Menerima", "pesan itu untuk dirinya sendiri", "Laras menyadari ia penerima yang salah"],
      ["57", "Perjalanan Lambat", "tidak ada relai lagi", "sebelas tahun perjalanan tanpa jaminan"],
      ["58", "Anak Terakhir", "seseorang harus mengingat semua ini", "anak yang lahir di bab 5.870"],
      ["59", "Pagi Biasa", "tidak ada lagi yang perlu diselamatkan", "tidak ada. Matahari terbit."],
      ["60", "Cahaya", "—", "cerita berhenti pada kalimat yang tepat"]]),
]

TWIST = [
    ("lead",
     "Dua belas twist. Untuk setiap twist ada lima hal yang wajib ada: apa yang dipercaya pembaca, "
     "apa yang sebenarnya terjadi, tiga tempat buktinya ditanam, bab pembayarannya, dan **biaya "
     "emosional** — apa yang hilang dari tokoh ketika twist itu jatuh."),
    ("table", [0.04, 0.24, 0.25, 0.22, 0.25],
     ["#", "Twist", "Yang dipercaya pembaca", "Yang sebenarnya", "Biaya emosional"],
     [["1", "Rasya membayar utang Nara sebelum bertemu", "Rasya sedang menyelidiki Biro", "ia mencintai sisa ingatan Nara, bukan Nara", "Nara tahu cinta pertama itu bukan untuknya"],
      ["2", "Kemuning menyala dari 4.000 ingatan", "relai butuh listrik", "stasiun hidup dari duka warganya sendiri", "setiap warga tahu harganya, dan tetap tinggal"],
      ["3", "Nara adalah kalibrasi usia tujuh", "ia kehilangan sembilan hari karena trauma", "sembilan hari itu pekerjaan yang dibayar", "ayahnya menyerahkannya"],
      ["4", "Istri sintetis", "Rasya pernah menikah", "perempuan itu dirakit dari ingatan orang lain", "Nara membunuhnya untuk membebaskannya"],
      ["5", "Isi pesan sudah musnah", "pesan 40 tahun menyimpan peringatan", "yang tersimpan hanya berat dan tanda tangan", "seluruh Zaman II menghabiskan hidup mencari isi yang tidak ada"],
      ["6", "Vey menanggung utang jaringan", "Vey sekarat karena usia", "ia membayar untuk semua orang selama 60 tahun", "Vey tidak pernah bisa memilih untuk berhenti"],
      ["7", "Arsip dibangun dari mayat relai", "Arsip adalah kemajuan teknologi", "setiap ingatan di dalamnya diambil dari orang yang mati saat pembongkaran", "Kirana mewarisi barang rampasan"],
      ["8", "Kasta Pengingat adalah lembaga", "itu pekerjaan mulia", "itu hukuman yang dilembagakan", "Sema menghabiskan hidup membayar hukuman ibunya"],
      ["9", "Perang Sunyi dimulai oleh terjemahan salah", "ada pihak yang menembak lebih dulu", "tidak ada yang menembak; hanya dua penerjemah yang salah", "60 juta mati karena satu kata"],
      ["10", "Tarif tahun hidup ditemukan dari catatan Nara", "Daniswara menemukannya", "ia membaca catatan Nara dari Zaman I", "generasi V mengulang kesalahan generasi I"],
      ["11", "Relai punya kehendak sejak awal", "relai adalah alat", "relai memilih siapa yang boleh membayar", "seluruh agama relai dibangun di atas kebenaran itu"],
      ["12", "Vey tidak pernah membayar satu ingatan pun", "Vey adalah korban", "Vey adalah satu-satunya yang utuh, dan itu kesepiannya", "ia satu-satunya yang mengingat semuanya, sendirian"]]),
    ("h", "Tiga twist yang ditulis paling rinci"),
    ("p",
     "**Twist 1 — Rasya membayar sebelum bertemu.** Bukti: (a) bab 3, Rasya menyebut nama jalan di "
     "planet yang belum ia datangi; (b) bab 5, ia hafal nomor berkas Nara tanpa membukanya; (c) bab 61, "
     "foto lama di kabinnya. Pembaca yang membaca ulang akan menemukan bahwa ketiga petunjuk itu "
     "mengatakan hal yang sama: **ia sudah mengenalnya sebelum mengenalnya.**"),
    ("p",
     "**Twist 9 — perang dimulai oleh terjemahan salah.** Bukti: (a) jilid 31 bab 12, satu kata yang "
     "diterjemahkan dua cara berbeda; (b) jilid 37 bab 88, kedua pihak mengutip kalimat yang sama; "
     "(c) jilid 39 bab 3, gencatan yang dikirim lewat jalur lambat. Twist ini tidak menyalahkan "
     "siapa pun — dan justru itu yang menghancurkan pembaca."),
    ("p",
     "**Twist 12 — Vey tidak pernah membayar.** Bukti: (a) jilid 11 bab 99, Vey menghindari pertanyaan "
     "tentang ingatannya sendiri; (b) jilid 18 bab 100, arsip Vey hanya 4%; (c) jilid 54 bab 12, ia "
     "menyebut nama Nara tanpa membaca catatan. Twist terakhir ini membalik seluruh novel: satu-satunya "
     "makhluk yang mengingat semuanya adalah yang tidak pernah dicintai siapa pun."),
    ("note", "Aturan twist yang jelas",
     "Twist yang jelas bukan twist yang mudah ditebak — ia twist yang **bisa dilacak**. Setelah "
     "terungkap, pembaca harus bisa menunjuk tiga halaman tempat jawabannya sudah ada. Kalau tidak "
     "bisa, yang mereka rasakan bukan kagum, melainkan ditipu."),
]

SAINS = [
    ("lead",
     "Dua puluh penemuan nyata. Kolom terakhir adalah aturan novel yang lahir darinya — dan setiap "
     "aturan itu dipakai, bukan sekadar dipajang."),
    ("table", [0.09, 0.30, 0.18, 0.43],
     ["Tahun", "Penemuan / gagasan", "Tokoh", "Menjadi apa di novel"],
     [["1867", "Demon Maxwell: makhluk yang memilah molekul tanpa kerja", "James Clerk Maxwell", "cikal bakal gagasan bahwa **informasi bisa dijadikan tenaga**"],
      ["1929", "Mesin Szilárd: informasi tentang satu molekul menghasilkan kerja", "Leó Szilárd", "dasar tarif: pengetahuan punya harga energi"],
      ["1948", "Teori informasi; satuan bit", "Claude Shannon", "satuan \"gram\" untuk ingatan; bahasa teknis Biro"],
      ["1957", "Tafsir banyak-dunia atas mekanika kuantum", "Hugh Everett", "argumen Vey tentang versi dirinya yang lain"],
      ["1961", "Prinsip Landauer: menghapus satu bit memakan kT ln2", "Rolf Landauer", "**inti aturan novel**: melupakan adalah pekerjaan termodinamika"],
      ["1971", "Dilatasi waktu terukur pada jam yang terbang", "Hafele & Keating", "selisih usia antar-zaman; jam relai"],
      ["1973", "Batas Bekenstein: informasi dibatasi luas permukaan", "Jacob Bekenstein", "kapasitas relai; mengapa hanya segelintir pesan bisa ditahan"],
      ["1974", "Radiasi Hawking; informasi lenyap di horizon", "Stephen Hawking", "paradoks yang dipakai Sekar untuk membenarkan relai"],
      ["1977", "Voyager: pesan yang menempuh puluhan tahun", "NASA", "bentuk fisik Pesan 0400; perjalanan lambat"],
      ["1978", "Teorema tanpa-komunikasi: keterikatan tidak bisa mengirim sinyal", "Ghirardi, Rimini, Weber", "**relai tidak melanggar fisika** — ia menjadwalkan, bukan mengirim"],
      ["1982", "Percobaan Aspect: ketidaksamaan Bell dilanggar", "Alain Aspect", "dasar teknis buoy kuantum"],
      ["1982", "Teorema tanpa-kloning", "Wootters & Zurek", "mengapa isi pesan musnah dan tidak bisa disalin"],
      ["1993", "Teleportasi kuantum", "Bennett dkk.", "prosedur pemindahan \"berat\" tanpa isi"],
      ["1999", "Penghapus kuantum pilihan-tunda", "Kim dkk.", "pemilihan tanggal tiba oleh pengirim"],
      ["2007", "Pilihan-tunda sesungguhnya di laboratorium", "Jacques dkk. (Aspect)", "mekanisme penjadwalan yang bisa diuji"],
      ["2016", "Satelit Micius: distribusi kunci kuantum antarbenua", "Pan Jian-Wei", "jaringan relai sembilan sistem"],
      ["2019", "Citra pertama lubang hitam", "Event Horizon Telescope", "bukti visual yang dipakai Kirana"],
      ["2019", "Kurva Page dan pulau informasi", "Penington; Almheiri dkk.", "argumen bahwa ingatan tidak benar-benar hilang"],
      ["2022", "Nobel Fisika untuk keterikatan kuantum", "Aspect, Clauser, Zeilinger", "legitimasi ilmiah dunia novel"],
      ["2023", "Koreksi galat kuantum pada skala besar", "Google Quantum AI", "mengapa relai bisa bertahan 287 tahun"]]),
    ("h", "Tiga hal yang tidak boleh dilanggar"),
    ("ol", [
        "**Tidak ada sinyal lebih cepat dari cahaya.** Teorema tanpa-komunikasi (1978) melarangnya, dan novel ini mematuhinya: relai tidak mengirim lebih cepat — ia **menahan** pesan dan melepaskannya pada tanggal yang sudah ditentukan. Tidak ada informasi yang menempuh jarak lebih cepat dari cahaya.",
        "**Melupakan punya biaya energi.** Prinsip Landauer (1961) menyatakan penghapusan satu bit memakan kT ln2. Novel ini mengambil langkah berikutnya: kalau penghapusan butuh energi, maka **ingatan adalah bentuk energi yang bisa ditagih**. Pada suhu tubuh, satu bit hanya 2,9 × 10⁻²¹ joule — dan itulah sebabnya tarifnya diukur dengan satuan lain: gram.",
        "**Informasi tidak bisa disalin.** Teorema tanpa-kloning (1982) membuat isi pesan mustahil digandakan, sehingga satu pesan yang terbuka berarti pesan itu hilang selamanya. Ini yang membuat setiap pesan berharga, dan setiap pembacaan menjadi pengorbanan."]),
    ("note", "Batas antara nyata dan fiksi",
     "Dua puluh penemuan di atas **nyata**. Yang fiktif hanya satu: perangkat yang bisa menahan "
     "superposisi selama puluhan tahun dan menagih biayanya pada ingatan manusia. Novel ini tidak "
     "mengarang fisika baru; ia mengambil satu penemuan nyata (Landauer) dan bertanya: **bagaimana "
     "kalau yang dibayar bukan listrik, melainkan ingatan?**"),
]

SISTEM_JUDUL = [
    ("lead",
     "Judul bab adalah satu-satunya bagian yang dibaca pembaca sebelum memutuskan membuka. Pada "
     "6.000 bab, judul bukan hiasan: ia sistem. Delapan pola dipakai bergiliran, dan tidak ada judul "
     "yang membocorkan twist."),
    ("table", [0.06, 0.22, 0.36, 0.36],
     ["#", "Pola", "Contoh dari Jilid 1", "Efek"],
     [["1", "Benda + tempat/waktu", "Buoy di Musim Dingin", "tenang, memikat, tidak membocorkan apa pun"],
      ["2", "Angka yang aneh", "Selisih Nol · Nol Koma Nol", "membuat pembaca ingin tahu hitungannya"],
      ["3", "Paradoks", "Yang Sudah Pernah Datang · Pesan yang Belum Ada", "menjanjikan teka-teki tanpa jawaban"],
      ["4", "Tindakan orang lain", "Yang Membayar · Yang Menyimpan Namamu", "menyiratkan ada tokoh yang belum dikenal"],
      ["5", "Pertanyaan pendek", "Siapa Kau · Berapa Banyak", "paling kuat; pakai maksimal sekali per sepuluh bab"],
      ["6", "Benda yang salah tempat", "Kereta Terakhir · Kamar yang Terlalu Rapi", "menandakan ada yang tidak beres"],
      ["7", "Kutipan protokol", "Protokol Abu · Audit Kedua", "memberi rasa dokumenter dan dingin"],
      ["8", "Negasi", "Yang Tidak Pernah Dikirim · Yang Tidak Dijual", "menciptakan lubang yang ingin diisi pembaca"]]),
    ("p",
     "**Aturan judul:** maksimal empat kata, tanpa titik dua, tanpa kata \"rahasia\" atau \"misteri\", "
     "dan tidak boleh menyebut nama tokoh yang mati di bab itu. Judul yang membocorkan twist akan "
     "dibaca sebagai peringatan, bukan sebagai janji."),
]

JUDUL1 = [
    ("h", "Bab 1–30 · judul + hook"),
    ("table", [0.06, 0.24, 0.70],
     ["Bab", "Judul", "Hook (kalimat terakhir bab)"],
     [["1", "Buoy di Musim Dingin", "Inti yang ia ganti memuat pesan bertanggal empat puluh tahun ke depan — dan tanda tangannya sendiri."],
      ["2", "Protokol Abu", "\"Catat, lalu lupakan,\" kata Vey. Nara mencatat. Ia tidak melupakan."],
      ["3", "Kapal Kuartal", "Rasya menyebut nama jalan tempat Nara dibesarkan, di planet yang belum pernah ia datangi."],
      ["4", "Selisih Nol", "Empat ribu seratus pesan keluar dari Kemuning. Nol pembayaran. Dan semuanya ditujukan kepada satu orang."],
      ["5", "Dua Cara Membaca Berkas", "Rasya hafal nomor berkas Nara tanpa membukanya."],
      ["6", "Rasa di Ujung Jari", "Duka itu bukan duka orang asing. Itu duka ibunya."],
      ["7", "Pesan yang Belum Ada", "Tanggal kirim: empat puluh tahun lagi. Ejaan tanda tangannya sama persis."],
      ["8", "Tuduhan", "Nara menyadari ia tidak bisa mengingat tiga tahun terakhir dengan jelas."],
      ["9", "Yang Sudah Pernah Datang", "\"Aku pernah ke sini,\" kata Rasya. \"Tiga tahun lalu. Dengan nama lain.\""],
      ["10", "Sembilan Hari", "Ada sembilan hari kosong di usia tujuh tahun — dan berkasnya ditandatangani ayahnya."],
      ["11", "Yang Menghitung Gram", "Vey menyebut angka pertama: empat puluh gram. Itu berat sebuah cinta."],
      ["12", "Penerima", "Semua pesan tak berbayar itu ditujukan kepada Nara. Pengirimnya memakai tanda tangannya."],
      ["13", "Interogasi", "Nara menekan Vey. Vey menjawab dengan pertanyaan yang sudah ia siapkan dua puluh tahun lalu."],
      ["14", "Satu Hari, Tiga Tahun Lalu", "Rasya mengulang kalimat yang Nara ucapkan saat itu — kata per kata."],
      ["15", "Kepercayaan yang Salah Tempat", "Nara mengecap sisa rasa dari jaket Rasya. Rasanya seperti dirinya."],
      ["16", "Sisa Rasa", "\"Aku sudah membayarmu,\" kata Rasya, \"tiga tahun sebelum aku bertemu kau.\""],
      ["17", "Cicilan", "Ia membayar setiap bulan. Itulah sebabnya ia tidak bisa menyebut nama adiknya."],
      ["18", "Berapa Banyak", "Tidak ada yang tahu. Termasuk Rasya. Terutama Rasya."],
      ["19", "Penolakan", "Biro mengirim satu baris: audit dilanjutkan, stasiun akan dievakuasi."],
      ["20", "Empat Ribu Orang", "Danu memohon agar Nara membiarkan utang itu tetap ada."],
      ["21", "Yang Menyalakan Lampu", "Kemuning tidak berjalan dari listrik. Ia berjalan dari duka empat ribu orang."],
      ["22", "Rekaman Tujuh Tahun", "Di rekaman itu, seorang anak berusia tujuh tahun menandatangani formulir."],
      ["23", "Yang Membayar", "Setelah menandatangani, ibunya berhenti memeluknya. Selamanya."],
      ["24", "Hidup", "Berkas kematian ibunya dipalsukan. Dan Danu tidak terkejut mendengar namanya."],
      ["25", "Panggilan Kembali", "Rasya memilih tinggal — dan itu berarti kehilangan seluruh kariernya."],
      ["26", "Pesan yang Sudah Ada", "Kalau pesan itu sudah ada, berarti ia harus mengirimnya. Dan ia tahu harganya."],
      ["27", "Gram", "Ia memilih yang paling berat untuk dibayar: Rasya."],
      ["28", "Tiga Tahap", "Suaranya hilang lebih dulu. Lalu wajahnya. Lalu fakta bahwa ia pernah mencintai siapa pun."],
      ["29", "Pagi Biasa", "Stasiun selamat. Nara merasa baik. Dan itu bagian yang paling menyakitkan."],
      ["30", "Siapa Kau", "Seorang lelaki dengan lencana Biro berdiri di koridor. \"Siapa kau?\" Di balik dinding, relai mulai berdenyut."]]),
]

JUDUL2 = [
    ("h", "Bab 31–100 · judul"),
    ("table", [0.08, 0.25, 0.08, 0.25, 0.08, 0.26],
     ["Bab", "Judul", "Bab", "Judul", "Bab", "Judul"],
     [["31", "Protokol Baru", "55", "Tangan yang Dingin", "79", "Tawar-menawar"],
      ["32", "Dua Bayangan", "56", "Perayaan Kecil", "80", "Batas"],
      ["33", "Anak yang Menandatangani", "57", "Yang Tidak Dijemput", "81", "Pembayaran"],
      ["34", "Buku yang Tidak Boleh Dibaca", "58", "Kereta Terakhir", "82", "Suara"],
      ["35", "Tarif Malam", "59", "Orang Ketiga", "83", "Wajah"],
      ["36", "Orang yang Tidak Pernah Pulang", "60", "Nama di Kursi", "84", "Fakta"],
      ["37", "Kesalahan Hitung", "61", "Istri", "85", "Yang Tersisa"],
      ["38", "Setengah Gram", "62", "Dokumen yang Sah", "86", "Dua Puluh Delapan Hari"],
      ["39", "Yang Menunggu di Kapal", "63", "Kebiasaan yang Bukan Miliknya", "87", "Yang Menyimpan"],
      ["40", "Nama yang Salah", "64", "Kamar yang Terlalu Rapi", "88", "Kabar Buruk"],
      ["41", "Audit Kedua", "65", "Yang Tidak Pernah Menikah", "89", "Yang Datang Menjemput"],
      ["42", "Pintu yang Tidak Ada", "66", "Hidup yang Dipinjam", "90", "Sepuluh Menit"],
      ["43", "Cuaca Buatan", "67", "Perempuan di Cermin", "91", "Kapal"],
      ["44", "Dua Tanda Tangan", "68", "Satu Kebiasaan Kecil", "92", "Bintang"],
      ["45", "Suara di Koridor", "69", "Pembongkaran", "93", "Yang Tidak Kembali"],
      ["46", "Yang Menjual Kenangan", "70", "Terima Kasih", "94", "Perpisahan Pertama"],
      ["47", "Harga Sebuah Adik", "71", "Warisan", "95", "Yang Ditunggu"],
      ["48", "Nol Koma Nol", "72", "Yang Mengingat untuk Dua Orang", "96", "Yang Datang"],
      ["49", "Yang Datang Terlambat", "73", "Pasar Malam", "97", "Yang Tidak Dijual"],
      ["50", "Evakuasi", "74", "Karcis", "98", "Siapa"],
      ["51", "Sepuluh Hari", "75", "Ingatan Pertama", "99", "Dua Kalimat"],
      ["52", "Surat untuk Biro", "76", "Orang Asing di Album", "100", "Pagi yang Sama"],
      ["53", "Yang Memilih Diam", "77", "Nama Panggilan", "", ""],
      ["54", "Anak di Rekaman", "78", "Yang Tidak Pernah Dikirim", "", ""]]),
    ("note", "Cara memakai daftar ini",
     "Judul di atas sudah memenuhi tiga aturan: maksimal empat kata, tidak membocorkan twist, dan "
     "bervariasi polanya. Kalau satu judul terasa lemah saat babnya ditulis, ganti — tetapi jangan "
     "ganti polanya dua bab berturut-turut, karena irama judul yang berulang membuat daftar isi "
     "terasa seperti mesin."),
]

ATURAN = [
    ("lead",
     "Enam aturan yang menjaga keruntutan, twist, sains, dan judul tetap bekerja sampai bab 6.000."),
    ("table", [0.30, 0.70],
     ["Aturan", "Bentuk pemeriksaannya"],
     [["Setiap jilid punya sebab", "`struktur.json` menyimpan `sebab_dari_jilid` — kosong berarti jilid itu belum boleh ditulis"],
      ["Setiap twist punya tiga bukti", "`petunjuk.json` menolak twist dengan `tanam` kurang dari tiga"],
      ["Tidak ada aturan dunia baru tanpa biaya", "setiap aturan baru wajib punya baris `harga` di `dunia.json`"],
      ["Tidak ada judul lebih dari empat kata", "pemeriksa judul: `len(judul.split()) <= 4`"],
      ["Tidak ada klaim sains palsu", "setiap rujukan sains menunjuk baris di `bible/sains.json` dengan tahun dan tokoh"],
      ["Tidak ada bab tanpa perubahan", "kalimat \"dari … menjadi …\" wajib ada di berkas bab sebagai komentar baris pertama"]]),
    ("h", "Berkas yang menyimpan semua ini"),
    ("code",
     "bible/\n"
     "├── struktur.json   60 jilid: sebab_dari_jilid, pertanyaan, jawaban_bab100\n"
     "├── petunjuk.json   id, isi, tanam[], bayar, status\n"
     "├── twist.json      12 twist: dipercaya, sebenarnya, bukti[], biaya\n"
     "├── sains.json      20 penemuan: tahun, tokoh, aturan_yang_lahir\n"
     "└── judul.json      judul, pola (1–8), hook"),
    ("quote",
     "Keruntutan bukan lawan dari kejutan. Cerita yang paling mengejutkan adalah cerita yang, "
     "setelah dibaca ulang, terasa tidak mungkin terjadi dengan cara lain."),
]

BAGIAN = [
    ("01", "Rantai sebab 60 jilid", "Setiap jilid lahir dari akibat jilid sebelumnya.", RANTAI + RANTAI_Z1 + RANTAI_Z2),
    ("02", "Rantai sebab — Zaman III–VI", "Kasta, perang, relai kedua, dan pagi biasa.", RANTAI_Z3 + RANTAI_Z4 + RANTAI_Z5 + RANTAI_Z6),
    ("03", "Dua belas twist", "Yang dipercaya pembaca, yang sebenarnya, dan biayanya.", TWIST),
    ("04", "Sains nyata di balik aturan", "Dua puluh penemuan, dari Maxwell sampai Nobel 2022.", SAINS),
    ("05", "Sistem judul bab", "Delapan pola, empat kata, tanpa bocoran.", SISTEM_JUDUL),
    ("06", "Bab 1–30 — judul & hook", "Tiga puluh pengait yang ditulis lengkap.", JUDUL1),
    ("07", "Bab 31–100 — judul", "Tujuh puluh judul sisa Jilid 1.", JUDUL2),
    ("08", "Enam aturan penjaga", "Bentuk pemeriksaannya di berkas.", ATURAN),
]
