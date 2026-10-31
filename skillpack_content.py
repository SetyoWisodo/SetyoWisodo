# -*- coding: utf-8 -*-
"""Isi Skill Pack — bagian 1: prinsip + skill 01–06.

Blok ditulis sebagai tuple supaya make_skillpack.py tinggal merender.
Markup mini:  **tebal**   _miring_   `kode`
"""

FRONT = [
    ("lead",
     "Berkas ini memuat cara kerja yang dipakai untuk membangun satu buku non-fiksi "
     "457 halaman — dari naskah kosong sampai produk yang dijual, lengkap dengan "
     "pemeriksa otomatis, sampul, harga, dan peluncuran — lalu diterjemahkan untuk "
     "proyek novel romance. Yang dipindahkan bukan topiknya, melainkan **urutannya**."),
    ("h", "Untuk siapa"),
    ("p",
     "Untuk penulis yang akan menulis novel romance dan tidak ingin mengulang kesalahan "
     "yang paling mahal: menulis dulu, bereskan nanti. Di proyek asal, urutan kerja yang "
     "benar menghemat dua kali lipat waktu dibanding menulis bebas lalu memperbaiki."),
    ("h", "Tiga cara memakai berkas ini"),
    ("ol", [
        "**Sebagai daftar periksa manusia.** Buka satu skill setiap kali Anda masuk ke tahap itu. Jangan dibaca sekaligus.",
        "**Sebagai lampiran proyek AI.** Unggah berkas ini ke proyek (Claude Projects, ChatGPT Projects, NotebookLM). Kalimat perintah di dalamnya sudah ditulis supaya bisa diikuti mesin, bukan hanya dipahami manusia.",
        "**Sebagai spesifikasi teknis.** Lampiran A memuat struktur folder dan urutan perintah; Lampiran B memuat enam prompt siap tempel.",
    ]),
    ("h", "Aturan satu: jangan pakai semuanya sekaligus"),
    ("p",
     "Tiga belas skill ini bukan tiga belas pekerjaan paralel. Urutannya berurutan karena "
     "setiap tahap mengunci tahap sebelumnya: arsitektur mengunci panjang bab, panjang bab "
     "mengunci tata letak, tata letak mengunci jumlah halaman, jumlah halaman mengunci harga. "
     "Mengerjakan mundur dari harga ke arsitektur selalu berakhir dengan naskah yang dipotong."),
    ("table", [0.17, 0.48, 0.35],
     ["Tahap", "Yang dikerjakan", "Skill"],
     [["1. Pondasi", "Arsitektur 24 bab, bible tokoh, timeline", "01, 05"],
      ["2. Menulis", "Suara, adegan, dialog; riset yang bisa diperiksa", "02, 03"],
      ["3. Sunting", "Audit otomatis sampai nol, baru baca ulang manusia", "04, 05"],
      ["4. Produksi", "Tata letak, PDF/EPUB/DOCX, sampul, sampel", "06–09"],
      ["5. Menjual", "Harga, halaman jual, peluncuran", "10–12"],
      ["6. Menutup", "Kontrol mutu akhir sebelum tombol terbit", "13"]]),
    ("h", "Yang tidak ada di berkas ini"),
    ("p",
     "Tidak ada jaminan laku, tidak ada angka penjualan yang dikarang, dan tidak ada saran "
     "menulis yang hanya terdengar bagus. Setiap skill menyebut **bukti di proyek asal** — "
     "apa yang benar-benar dikerjakan dan apa yang benar-benar gagal — lalu **terjemahannya "
     "untuk romance**. Kalau sebuah praktik tidak bisa dibuktikan, ia tidak masuk."),
    ("note", "Satu berkas kode disertakan",
     "`tools/audit_novel.py` di repositori proyek adalah versi umum dari pemeriksa yang "
     "dipakai di sini. Ia membaca folder `manuscript/`, memeriksa 24 bab, panjang bab, frasa "
     "klise, ejaan nama tokoh, tipografi, variasi pembuka, POV, dan urutan timeline — lalu "
     "keluar dengan kode galat kalau ada yang gagal. Skill 04 menjelaskannya."),
]

PRINSIP = [
    ("lead",
     "Lima aturan ini yang membuat tiga belas skill di bawah bekerja. Tanpa mereka, "
     "skill-nya tetap masuk akal tetapi tidak akan pernah selesai."),
    ("h", "1 · Satu jalur, tanpa opsi"),
    ("p",
     "Di proyek asal, setiap kali saya menawarkan tiga pilihan, pekerjaan berhenti sampai "
     "pengguna memilih. Setiap kali saya memberi satu langkah dengan satu hasil yang bisa "
     "dicek, pekerjaan selesai. Karena itu semua instruksi di berkas ini berbentuk perintah "
     "dengan hasil yang terlihat: _klik ini, hasilnya harus begitu_."),
    ("p",
     "**Untuk romance:** jangan menulis tiga versi pembukaan bab lalu menimbang. Tulis satu, "
     "ukur dengan audit, perbaiki yang terukur. Ragu adalah bentuk penundaan yang paling mahal."),
    ("h", "2 · Setiap angka punya sumber"),
    ("p",
     "Sepuluh angka di proyek asal pernah salah dan harus dicabut. Yang menyelamatkan bukan "
     "ketelitian, melainkan berkas `NUMERIC_CLAIMS.md` — daftar setiap angka, nilainya, dan "
     "sumbernya. Setiap kali naskah menyebut angka, ia harus ada di daftar."),
    ("p",
     "**Untuk romance:** angka jarang menjadi masalah, tetapi fakta sering. Jam kerja perawat, "
     "prosedur kepolisian, biaya sewa apartemen di kota tertentu, umur SIM, hukum waris. Semua "
     "itu butuh daftar yang sama bentuknya: **klaim · nilai · sumber · dipakai di bab**."),
    ("h", "3 · Jangan pangkas yang berguna"),
    ("p",
     "Godaan terbesar saat menyunting adalah membuang bagian yang paling padat karena terasa "
     "berat. Di proyek asal, bagian anjuran pelaksanaan di akhir setiap bab tidak boleh "
     "dipangkas — dan ada pemeriksa khusus untuk memastikan tidak ada yang hilang."),
    ("p",
     "**Untuk romance:** yang tidak boleh dipangkas adalah **adegan yang mengubah keadaan**. "
     "Kalau sebuah adegan dihapus dan hubungan kedua tokoh tetap sama, adegan itu memang "
     "boleh dibuang. Kalau keadaan berubah, ia wajib tinggal walau terasa lambat."),
    ("h", "4 · Audit sampai nol, bukan sampai cukup baik"),
    ("p",
     "Pemeriksa akhir di proyek asal menjalankan 45 pemeriksaan dan menuntut hasil "
     "**FAIL 0 · WARN 0 · OK 45**. Bukan \"sebagian besar lulus\". Nol. Selama masih ada satu "
     "peringatan, produk tidak diterbitkan."),
    ("p",
     "**Untuk romance:** buku yang diterbitkan dengan tiga kesalahan kontinuitas akan mendapat "
     "tiga ulasan yang menyebutnya. Ambangnya nol, bukan sedikit."),
    ("h", "5 · Teks siap tempel, bukan instruksi samar"),
    ("p",
     "Setiap kali pengguna diminta mengetik sesuatu — deskripsi produk, nama bagian, kode "
     "diskon — teksnya disediakan lengkap dengan jumlah karakternya, bukan \"tulis deskripsi "
     "yang menarik\". Instruksi samar memindahkan pekerjaan menulis kepada orang yang justru "
     "sedang meminta bantuan."),
    ("p",
     "**Untuk romance:** blurb, bio penulis, dan jawaban atas ulasan buruk semuanya disiapkan "
     "sebagai teks jadi. Kalau Anda memakai asisten AI, minta teks jadi, bukan saran."),
]

SKILL_01 = [
    ("lead",
     "Buku asal punya 24 bab, masing-masing dengan subbab bernomor, satu studi kasus, dan "
     "satu skenario masa depan. Struktur itu bukan hiasan: ia yang membuat 457 halaman bisa "
     "dibaca tidak berurutan, dikutip per bab, dan diuji satu per satu."),
    ("h", "Yang benar-benar dikerjakan"),
    ("ul", [
        "24 bab, tiap bab 3–5 subbab bernomor (`10.1`, `10.2`, `10.3`).",
        "Dua subbab wajib di setiap bab: **studi kasus** dan **skenario masa depan**, keduanya bernomor, bukan kotak sampingan.",
        "Pembuka bab berupa dua baris rata tengah — `CHAPTER 7` lalu judul — dan **tidak diulang** di halaman berikutnya.",
        "Tanpa blok penutup bab. Tidak ada _Key takeaways_, _In sum_, _Sources cited_, atau _For reflection_. Bab berhenti ketika argumennya selesai.",
        "Tanpa label `Appendix A–D`. Bagian tambahan memakai judul telanjang.",
    ]),
    ("p",
     "Pemeriksa otomatis menegakkan tiga hal ini secara harfiah — jumlah bab, keberadaan subbab "
     "bernomor, dan ketiadaan blok penutup — karena ketiganya paling mudah rusak tanpa disadari."),
    ("h", "Mengapa blok penutup dibuang"),
    ("p",
     "Blok penutup terasa membantu penulis, bukan pembaca. Ia memaksa setiap bab menyimpulkan "
     "dirinya sendiri, sehingga bab berikutnya harus mengulang kesimpulan itu agar berdiri "
     "sendiri. Hasilnya pengulangan yang membuat buku terasa lebih tebal daripada isinya. "
     "Setelah dibuang, setiap bab harus **berakhir pada kalimat yang bekerja**, bukan pada "
     "ringkasan."),
    ("h", "Terjemahan untuk romance: peta 24 bab"),
    ("p",
     "Struktur 24 bab cocok untuk romance kontemporer 85.000–110.000 kata. Tabel ini "
     "memetakan fungsi dramatik ke nomor bab, sehingga setiap bab punya pekerjaan yang bisa "
     "diperiksa."),
    ("table", [0.09, 0.30, 0.37, 0.24],
     ["Bab", "Beat", "Yang harus berubah", "Kata"],
     [["1", "Meet / world", "Dua orang ada di ruang yang sama; salah satu ingin pergi", "4.000"],
      ["2", "Inciting", "Ada alasan mereka tidak bisa saling menghindar", "3.800"],
      ["3", "First friction", "Ketertarikan bertabrakan dengan alasan menolak", "3.600"],
      ["4", "Bond 1", "Satu hal kecil yang membuat mereka sekutu", "3.600"],
      ["5", "Complication", "Sekutu tadi menciptakan masalah baru", "3.800"],
      ["6", "Turn 1", "Salah satu mengungkap sesuatu yang tidak seharusnya", "3.800"],
      ["7", "Retreat", "Jarak; salah satu menarik diri", "3.400"],
      ["8", "Return", "Kembali karena keadaan, bukan karena keinginan", "3.600"],
      ["9", "Intimacy 1", "Kedekatan yang tidak bisa ditarik kembali", "4.000"],
      ["10", "Fault line", "Perbedaan nilai yang tidak bisa dikompromikan muncul", "3.800"],
      ["11", "Escalation", "Pihak ketiga memperbesar tekanan", "3.800"],
      ["12", "Midpoint", "Mereka memilih satu sama lain — dengan syarat", "4.200"],
      ["13", "Aftermath", "Harga dari pilihan itu mulai ditagih", "3.600"],
      ["14", "Secret", "Yang disembunyikan mulai terlihat", "3.800"],
      ["15", "Crack", "Salah satu berbohong untuk melindungi", "3.800"],
      ["16", "Discovery", "Kebohongan terbongkar di tempat terburuk", "4.000"],
      ["17", "Rupture", "Perpisahan pertama", "3.800"],
      ["18", "Alone", "Hidup tanpa yang lain terasa lebih buruk", "3.400"],
      ["19", "Ghost", "Masa lalu menjelaskan mengapa ia menolak", "3.600"],
      ["20", "Proof", "Tindakan yang membuktikan perubahan, tanpa imbalan", "3.800"],
      ["21", "Return 2", "Bertemu lagi; syaratnya berbeda", "3.800"],
      ["22", "Dark moment", "Pilihan terakhir: harga yang harus dibayar", "4.200"],
      ["23", "Choice", "Ia memilih — dan kehilangan sesuatu", "3.800"],
      ["24", "HEA", "Keadaan baru yang tidak bisa dibatalkan", "4.000"]]),
    ("p",
     "Tabel di atas adalah **rencana**, bukan hukum. Yang wajib adalah kolom ketiga: setiap bab "
     "harus mengubah sesuatu. Kalau satu baris kolom ketiga berbunyi sama dengan baris "
     "sebelumnya, bab itu belum punya alasan."),
    ("h", "Latihan yang memakan waktu satu jam dan menghemat satu bulan"),
    ("p",
     "Tulis satu kalimat per bab dengan pola: _X berubah dari ... menjadi ..._. Dua puluh empat "
     "kalimat. Kalau ada dua kalimat yang isinya sama, arsitektur Anda sedang mengulang dan "
     "itu akan terasa oleh pembaca sebagai bab yang membosankan."),
    ("code",
     "Bab 1  Alya berubah dari orang yang menghindari kota itu menjadi orang yang\n"
     "       terpaksa tinggal di dalamnya.\n"
     "Bab 2  Alya berubah dari penyewa biasa menjadi orang yang berutang pada Bima.\n"
     "Bab 3  ..."),
    ("note", "Kesalahan yang paling mahal di tahap ini",
     "Menulis bab 1 dengan sangat bagus sebelum 23 kalimat lain ada. Bab 1 yang bagus membuat "
     "Anda ingin mempertahankannya, padahal sering ia satu-satunya bab yang bisa dipindah ke "
     "belakang. Tulis 24 kalimat dulu, baru prosa."),
]

SKILL_02 = [
    ("lead",
     "Di proyek asal, setiap klaim angka harus bisa ditelusuri ke sumber bernama. Aturan itu "
     "tidak lahir dari kehati-hatian akademik, melainkan dari kegagalan: sepuluh angka "
     "sempat salah dan lolos ke naskah karena tidak ada satu pun tempat yang menyimpannya."),
    ("h", "Bentuk yang dipakai: buku besar klaim"),
    ("p",
     "Satu berkas teks dengan satu baris per klaim. Bukan catatan kaki, bukan ingatan, bukan "
     "tab di peramban. Bentuknya harus bisa dibaca lima bulan kemudian tanpa penjelasan."),
    ("table", [0.30, 0.18, 0.34, 0.18],
     ["Klaim", "Nilai", "Sumber", "Dipakai di"],
     [["Kematian akibat polusi udara rumah tangga", "2,9 juta/tahun", "WHO fact sheet, 2025", "bab 9"],
      ["Kerugian badai Uri", "$80–130 miliar", "Texas Comptroller, 2021", "bab 14"],
      ["Korban badai Katrina", "1.833", "NOAA", "bab 14"],
      ["Harga ebook romance kategori indie", "$2,99–4,99", "pantau sendiri, 2026", "skill 10"]]),
    ("p",
     "Kolom terakhir yang membuat berkas ini berguna. Tanpa kolom itu, daftar berubah menjadi "
     "gudang yang tidak pernah dibuka."),
    ("h", "Terjemahan untuk romance"),
    ("p",
     "Novel romance lebih banyak memuat fakta daripada yang diakui penulisnya. Empat jenis "
     "yang paling sering salah:"),
    ("ul", [
        "**Profesi.** Jam kerja perawat ICU, wewenang polisi saat menahan, apa yang benar-benar dikerjakan arsitek pada minggu pertama proyek.",
        "**Tempat.** Jarak yang bisa ditempuh dalam satu malam, nama jalan yang benar, arah matahari terbenam di kota itu.",
        "**Hukum dan uang.** Warisan tanpa surat wasiat, uang muka rumah, biaya perceraian, batas usia.",
        "**Cedera dan pengobatan.** Berapa lama patah tulang sembuh, apa yang benar-benar dilakukan dokter di ruang gawat darurat.",
    ]),
    ("p",
     "Aturan satu menit: kalau sebuah adegan bergantung pada prosedur nyata dan Anda belum "
     "memeriksanya, **ganti nama institusinya** atau ubah satu syaratnya sehingga tidak bisa "
     "digugat. Pembaca romansa memaafkan banyak hal, tetapi tidak memaafkan profesi yang "
     "ditulis sembarangan — dan profesi itu justru kelompok pembaca paling setia."),
    ("h", "Tiga sumber yang cukup untuk 90% kebutuhan"),
    ("ol", [
        "**Satu orang yang benar-benar bekerja di bidang itu.** Satu pesan singkat, tiga pertanyaan spesifik. Lebih akurat daripada sepuluh artikel.",
        "**Satu dokumen resmi.** Situs instansi, undang-undang, panduan perusahaan. Simpan tautan dan tanggal aksesnya.",
        "**Satu pengalaman yang bisa diverifikasi.** Bukan \"kata orang\", tetapi satu artikel berita dengan nama dan tanggal.",
    ]),
    ("note", "Jangan mengarang angka",
     "Kalau dua sumber berbeda, pilih satu dan **cantumkan sumbernya di teks**. Pembaca lebih "
     "menghargai \"sekitar 1.800 orang (NOAA)\" daripada angka bulat tanpa asal yang ternyata "
     "salah di dua ulasan pertama."),
]

SKILL_03 = [
    ("lead",
     "Dua hal membuat prosa terasa ditulis mesin: kalimat yang dibuka dengan cara yang sama, "
     "dan frasa yang sudah pernah dibaca pembaca seratus kali. Keduanya bisa diukur."),
    ("h", "Mesin yang dipakai"),
    ("ul", [
        "**Audit pengulangan** — menghitung kata yang muncul berulang dalam satu bab dan membandingkan sebelum–sesudah suntingan.",
        "**Audit variasi** — membandingkan kata pembuka paragraf; kalau terlalu banyak paragraf dibuka dengan subjek, variasi dipaksa.",
        "**Daftar frasa terlarang** — frasa yang langsung membuat pembaca tahu ini tulisan pemula.",
        "**Tipografi** — elipsis tipografis (…), tanpa spasi ganda, tanpa tanda hubung ganda.",
    ]),
    ("p",
     "Hasil yang dikejar bukan \"bagus\", melainkan **tidak ada yang bisa ditunjuk**. Selama "
     "sebuah kalimat bisa ditunjuk sebagai klise, ia akan ditunjuk."),
    ("h", "Dua belas frasa yang harus hilang dari naskah romance"),
    ("table", [0.52, 0.48],
     ["Frasa", "Gantinya"],
     [["a breath she didn't know she was holding", "satu tindakan: ia menahan napas, lalu melepasnya karena sesuatu terjadi"],
      ["shiver down her spine", "satu detail fisik lain: bulu lengan, suhu ruangan, suara"],
      ["butterflies in her stomach", "reaksi tubuh yang spesifik dan bukan perut"],
      ["their eyes locked", "apa yang dilihatnya, bukan bahwa mereka saling melihat"],
      ["electricity shot through her", "sentuhan + akibatnya pada tindakan berikutnya"],
      ["he smirked", "satu gerakan mulut yang spesifik, atau dialog yang menggantikannya"],
      ["she rolled her eyes", "satu reaksi lain, atau hilangkan sama sekali"],
      ["little did they know", "hilangkan; pembaca benci diberi tahu bahwa mereka tidak tahu"],
      ["only time would tell", "hilangkan; itu tugas bab berikutnya"],
      ["her heart skipped a beat", "satu tanda fisik yang belum dipakai di bab ini"],
      ["he let out a breath he didn't know he was holding", "sama seperti baris pertama, dan lebih buruk"],
      ["and then everything changed", "tunjukkan perubahannya, jangan mengumumkannya"]]),
    ("h", "Teknik yang paling berguna: filter POV"),
    ("p",
     "Satu ruangan, dua orang, dua deskripsi yang tidak boleh berbagi satu kata benda pun "
     "selain yang wajib. Ini bukan latihan gaya, melainkan cara membangun dua suara yang bisa "
     "dibedakan tanpa label bab."),
    ("code",
     "ALYA (arsitek, kontrol, detail):\n"
     "  \"Ruangan itu tiga meter terlalu lebar untuk perabot yang ada di dalamnya.\"\n\n"
     "BIMA (pemadam kebakaran, gerak, tubuh):\n"
     "  \"Pintunya membuka ke dalam. Kalau ada apa-apa, dua puluh orang akan berebut\n"
     "   di mulut pintu yang sama.\""),
    ("p",
     "Perhatikan: keduanya melihat ruangan yang sama, dan keduanya memperlihatkan pekerjaannya "
     "tanpa satu kalimat pun menjelaskan bahwa mereka bekerja."),
    ("h", "Kartu suara — isi sekali, pakai sepanjang buku"),
    ("table", [0.28, 0.72],
     ["Kolom", "Isi"],
     [["Panca indera utama", "indera mana yang paling dulu menangkap ruangan (Alya: penglihatan dan ukuran; Bima: bau dan suhu)"],
      ["Kalimat terpanjang", "berapa kata maksimal; satu tokoh boleh 45 kata, yang lain 18"],
      ["Kata yang tidak pernah dipakai", "tiga kata yang tidak akan diucapkan tokoh ini"],
      ["Cara berbohong", "bagaimana ia mengalihkan pembicaraan saat terdesak"],
      ["Benda yang selalu diperhatikan", "satu kategori benda yang selalu ia lihat lebih dulu"],
      ["Lelucon", "jenis humor yang ia pakai, dan yang tidak"],
      ["Yang tidak ia akui", "satu hal yang tidak pernah ia katakan, bahkan kepada dirinya"]]),
    ("note", "Aturan satu metafora",
     "Satu halaman, satu metafora. Metafora kedua di halaman yang sama selalu melemahkan yang "
     "pertama, dan yang ketiga membuat pembaca berhenti membaca untuk mengagumi penulisnya."),
]

SKILL_04 = [
    ("lead",
     "Ini skill yang paling mudah diremehkan dan paling besar hasilnya. Di proyek asal ada 45 "
     "pemeriksaan otomatis yang menuntut nol kegagalan sebelum produk boleh terbit. Yang "
     "dilakukan pemeriksaan itu bukan hal-hal besar, melainkan hal-hal kecil yang tidak "
     "mungkin diperiksa manusia sebanyak 45 kali."),
    ("h", "Prinsipnya satu kalimat"),
    ("p",
     "**Setiap klaim tentang naskah harus punya pemeriksa yang bisa gagal.** \"Saya rasa semua "
     "bab sudah ada\" bukan klaim; \"skrip menghitung 24 berkas dan berhenti kalau kurang\" "
     "adalah klaim."),
    ("h", "Skrip yang disertakan"),
    ("p",
     "`tools/audit_novel.py` membaca `manuscript/bab_*.md` dan `bible/*.json`. Tujuh "
     "pemeriksaan, masing-masing menghasilkan FAIL (memblokir terbit), WARN (perlu dilihat "
     "manusia), atau OK. Skrip keluar dengan kode 1 kalau ada FAIL, sehingga bisa dipakai di "
     "pre-commit hook atau CI."),
    ("table", [0.22, 0.48, 0.30],
     ["Pemeriksaan", "Yang ditangkap", "Ambang"],
     [["struktur", "jumlah bab bukan 24", "wajib 24"],
      ["panjang", "bab terlalu pendek/panjang, atau satu bab 1,25x median", "1.500–5.000 kata"],
      ["klise", "frasa romance dari daftar pantau", "> 8 = FAIL"],
      ["nama", "ejaan tokoh yang salah (Alia vs Alya) via `bible/tokoh.json`", "nol"],
      ["tipografi", "spasi ganda, elipsis tiga titik", "nol"],
      ["variasi", "pembuka bab yang mirip (Jaccard > 0,45)", "peringatan"],
      ["timeline", "tanggal di `bible/timeline.json` melompat mundur", "nol"],
      ["pov", "sudut pandang berganti terlalu sering", "peringatan"]]),
    ("h", "Cara memakainya"),
    ("code",
     "python3 tools/audit_novel.py\n"
     "\n"
     "FAIL panjang    bab_05.md hanya 976 kata (minimum 1500)\n"
     "FAIL timeline   bab 3 (2026-03-04) mendahului bab 2 (2026-03-09)\n"
     "WARN klise      shiver down her spine (1)\n"
     "WARN tipografi  elipsis tiga titik; pakai karakter …\n"
     "\n"
     "FAIL 9 | WARN 5 | OK 1"),
    ("p",
     "Baca keluarannya dari atas. FAIL diperbaiki hari itu; WARN diperiksa; OK tidak perlu "
     "dibaca. Jangan pernah menaikkan ambang agar lulus — itu satu-satunya cara membuat alat "
     "ini berhenti berguna."),
    ("h", "Dua pemeriksaan yang paling sering menyelamatkan"),
    ("p",
     "**Timeline.** Satu tanggal yang melompat mundur menghancurkan kepercayaan pembaca lebih "
     "dari sepuluh kalimat jelek. Karena tanggal di `timeline.json` hanya ditulis sekali, satu "
     "perubahan di bab 9 langsung terlihat efeknya di bab 14."),
    ("p",
     "**Nama.** Varian ejaan (`Alia`, `Alliya`) hampir tidak mungkin ditemukan dengan membaca "
     "ulang 90.000 kata, tetapi ditemukan dalam sekejap oleh pencarian pola kata utuh."),
    ("h", "Yang tidak bisa diperiksa mesin"),
    ("p",
     "Apakah adegan itu menyentuh. Apakah dua tokoh punya alasan untuk saling mencintai. "
     "Apakah akhirnya memuaskan. Untuk tiga pertanyaan itu, mesin hanya bisa memberi tanda: "
     "hitung berapa adegan yang **mengubah keadaan** dan bandingkan dengan jumlah bab. Kalau "
     "kurang dari dua pertiga, masalahnya bukan gaya, melainkan arsitektur — kembali ke skill 01."),
    ("note", "Kebiasaan yang membuat ini bekerja",
     "Jalankan audit **setelah setiap bab selesai**, bukan setelah buku selesai. Satu FAIL yang "
     "ditemukan di bab 5 memakan dua menit; kesalahan yang sama ditemukan setelah 24 bab "
     "memakan dua hari."),
]

SKILL_05 = [
    ("lead",
     "Buku asal dirender dalam dua bahasa dari satu sumber. Setiap kali satu angka berubah, ia "
     "harus berubah di dua tempat, dan pemeriksa memastikan keduanya masih sama: jumlah bab "
     "sama, jumlah tabel sama, jumlah gambar sama, kata badan sebanding."),
    ("p",
     "Prinsip yang sama dipakai untuk novel: **satu sumber kebenaran**, semua turunannya "
     "diperiksa terhadap sumber itu."),
    ("h", "Tiga berkas bible"),
    ("table", [0.24, 0.76],
     ["Berkas", "Isi"],
     [["`bible/tokoh.json`", "nama resmi + varian salah yang harus ditangkap; satu tokoh satu entri"],
      ["`bible/timeline.json`", "satu titik waktu peristiwa per bab, format `YYYY-MM-DD`"],
      ["`bible/kontinuitas.md`", "benda, cuaca, musim, luka, dan ponsel: apa yang berubah di bab berapa"]]),
    ("h", "Kartu tokoh yang benar-benar dipakai"),
    ("p",
     "Bukan biografi. Hanya tujuh hal yang akan Anda butuhkan di tengah bab 14 ketika lupa:"),
    ("code",
     "NAMA        Alya Prameswari            UMUR 31 (lahir 1995-04-11)\n"
     "KERJA       arsitek, kantor 9 orang   GAJI  cukup, tidak longgar\n"
     "LUKA        ayahnya menjual rumah keluarga tanpa bertanya\n"
     "INGIN       membeli kembali rumah itu  BUTUH  memaafkan ayahnya\n"
     "RAHASIA     ia yang menandatangani surat penjualan itu\n"
     "TUBUH       bekas luka 4 cm di lengan kiri, tidak pernah dibahas sampai bab 19\n"
     "SUARA       kalimat pendek; tidak pernah memakai kata \"feel\""),
    ("h", "Kontinuitas yang paling sering bocor"),
    ("ul", [
        "**Cuaca dan musim.** Hujan di bab 6, lalu di bab 9 disebut \"musim kemarau\".",
        "**Benda.** Ponsel yang mati di bab 12 lalu dipakai menelepon di bab 13.",
        "**Luka.** Pergelangan tangan yang patah dan sudah sembuh dalam tiga hari.",
        "**Pakaian.** Jas yang dilepas di lift lalu masih dipakai di lobi.",
        "**Uang.** Tokoh yang tidak punya uang lalu membayar taksi lintas kota.",
    ]),
    ("p",
     "Semua ini disimpan di `bible/kontinuitas.md` dengan bentuk satu baris per benda: "
     "`ponsel mati — bab 12 — hidup lagi bab 14 karena diisi di mobil`. Kalau tidak ada baris "
     "itu, kemungkinan besar ia akan lupa."),
    ("note", "Aturan yang mengikat semuanya",
     "Kalau sebuah fakta hanya ada di kepala Anda, ia belum ada. Tulis di bible, baru tulis di "
     "naskah — bukan sebaliknya."),
]

SKILL_06 = [
    ("lead",
     "Tata letak bukan pekerjaan akhir; ia mengunci jumlah halaman, dan jumlah halaman mengunci "
     "harga. Di proyek asal, satu keputusan tata letak — margin dan indent — menentukan bahwa "
     "naskah menjadi 457 halaman, bukan 380 atau 520."),
    ("h", "Spesifikasi yang dipakai di proyek asal"),
    ("table", [0.30, 0.70],
     ["Parameter", "Nilai"],
     [["Jenis huruf", "Times New Roman 12 pt (badan), 10 pt (tabel), 9 pt (catatan)"],
      ["Perataan", "rata kiri-kanan (_justify_), tanpa pemenggalan kata"],
      ["Indentasi baris pertama", "12,7 mm, hanya untuk paragraf lanjutan"],
      ["Spasi baris", "1,15"],
      ["Folio", "tengah bawah pada halaman pembuka bab, kanan bawah pada halaman berikutnya"],
      ["Margin cermin", "**ditolak** — margin harus sama di semua halaman"],
      ["Daftar isi", "di depan, dengan nomor halaman yang benar-benar dicocokkan ke PDF"],
      ["Judul bab", "dua baris rata tengah: `CHAPTER 7` lalu judulnya; baris itu tidak diulang di halaman berikutnya"]]),
    ("h", "Terjemahan untuk novel romance"),
    ("table", [0.30, 0.34, 0.36],
     ["Parameter", "Cetak (POD)", "Digital"],
     [["Ukuran halaman", "5,5 × 8,5 inci (paling umum) atau 6 × 9", "mengikuti perangkat"],
      ["Badan", "11,5–12 pt, _leading_ 15–16 pt", "dapat diubah pembaca"],
      ["Indentasi", "5–6 mm; paragraf pertama tiap adegan tanpa indentasi", "sama"],
      ["Pembuka bab", "selalu halaman baru; di cetak, halaman kanan", "halaman baru"],
      ["Jeda adegan", "satu ornamen atau tiga bintang, bukan baris kosong", "sama"],
      ["Folio", "tengah bawah; hilangkan di halaman pembuka bab dan halaman judul", "tanpa folio"],
      ["Widow / orphan", "dilarang; satu baris yatim di puncak halaman adalah cacat", "tidak berlaku"],
      ["Fonta yang dijual", "harus tertanam (_embedded_), bukan dirujuk", "tertanam di EPUB"]]),
    ("h", "Urutan halaman depan (front matter)"),
    ("ol", [
        "Halaman setengah judul — judul saja.",
        "Halaman judul — judul, subjudul, nama penulis.",
        "Halaman hak cipta — tahun, nama, pernyataan fiksi (\"tokoh dan peristiwa dalam buku ini adalah fiksi\").",
        "Halaman persembahan — satu baris, boleh kosong.",
        "Daftar isi — untuk novel, cukup judul bab.",
        "Bab 1 — dimulai di halaman kanan (cetak).",
    ]),
    ("p",
     "Halaman hak cipta punya satu kalimat yang tidak boleh dilupakan pada romance: pernyataan "
     "bahwa tokoh, tempat, dan peristiwa adalah fiksi. Tanpa itu, seorang pembaca yang mengenali "
     "dirinya di dalam buku punya dasar untuk mengeluh — dan itu pernah terjadi pada penulis "
     "yang jauh lebih besar."),
    ("note", "Uji tata letak dalam lima menit",
     "Cetak dua halaman berturut-turut di kertas A4 dengan skala 100%, lalu baca sambil berdiri. "
     "Kalau mata harus bergerak lebih dari dua kali per baris, ukuran halaman atau margin terlalu "
     "lebar untuk romance — pembaca romance membaca cepat, dan baris panjang memperlambat mereka."),
]
