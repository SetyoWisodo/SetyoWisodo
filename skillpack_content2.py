# -*- coding: utf-8 -*-
"""Isi Skill Pack — bagian 2: skill 07–13 + lampiran."""

SKILL_07 = [
    ("lead",
     "Satu naskah, tujuh berkas keluar. Di proyek asal urutan pembuatannya tidak boleh diubah, "
     "dan setiap tahap memeriksa hasil tahap sebelumnya. Urutan yang sama berlaku untuk novel."),
    ("h", "Urutan produksi"),
    ("table", [0.08, 0.34, 0.58],
     ["#", "Berkas", "Dari mana dan untuk apa"],
     [["1", "`interior.pdf`", "dari naskah; tanpa sampul; untuk percetakan"],
      ["2", "`ebook.pdf`", "interior + halaman sampul berwarna disisipkan di depan; untuk pembeli"],
      ["3", "`book.epub`", "navigasi bab, gambar, teks alternatif; untuk ponsel dan e-reader"],
      ["4", "`book.docx`", "naskah yang bisa disunting; untuk kutipan dan terjemahan"],
      ["5", "`cover_print.pdf`", "bungkus penuh: belakang + punggung + depan"],
      ["6", "`sample.pdf`", "sampul + sebagian awal; gratis, untuk menarik pembeli"],
      ["7", "`figures.zip` / `assets.zip`", "gambar terpisah 300 dpi, boleh dipakai ulang"]]),
    ("h", "Empat jebakan yang memakan waktu paling banyak"),
    ("ol", [
        "**Jumlah halaman dibaca setelah berkas ditutup.** Pada PyMuPDF, `page_count` yang dibaca setelah `close()` mengembalikan nilai yang tidak bisa dipercaya. Baca sebelum menyimpan.",
        "**Daftar isi bergeser setelah sampul disisipkan.** Menyisipkan satu halaman di depan menggeser seluruh penanda; nomornya harus dinaikkan manual, bukan diasumsikan ikut bergeser.",
        "**Gambar terduplikasi.** Menyalin halaman dari PDF buku jadi menggandakan setiap gambar di halaman itu. Bangun ulang dari `interior.pdf` dan sisipkan hanya halaman sampul.",
        "**Fonta tidak tertanam.** PDF terlihat benar di komputer Anda dan berubah di komputer pembeli. Periksa dengan penyunting PDF, bukan dengan mata.",
    ]),
    ("h", "Asersi: cara memastikan berkas tidak bohong"),
    ("p",
     "Setiap skrip produksi diakhiri dengan pemeriksaan yang **menghentikan skrip** kalau hasilnya "
     "tidak sesuai harapan. Bukan mencetak peringatan — berhenti."),
    ("code",
     "assert out.page_count == 458, out.page_count\n"
     "assert len(out.get_toc()) == 327, len(out.get_toc())\n"
     "assert abs(out[0].rect.width - 612) < 1      # 8,5 inci\n"
     "assert 'Setyo Wisodo' in out.metadata.get('author', '')"),
    ("p",
     "Ini satu-satunya cara membuat produksi bisa diulang. Tanpa asersi, setiap kali naskah "
     "berubah Anda harus memeriksa tujuh berkas dengan mata — dan pada percobaan kelima Anda "
     "akan melewatkan satu."),
    ("h", "Untuk novel: perintah yang sama, lebih sedikit berkas"),
    ("code",
     "python3 render_novel.py        # naskah -> interior.pdf + penanda bab\n"
     "python3 make_ebook.py          # + sampul -> ebook.pdf (458 hlm)\n"
     "python3 make_sample.py         # 3 bab pertama + sampul -> sample.pdf\n"
     "python3 make_cover.py          # bungkus cetak (belakang+punggung+depan)\n"
     "python3 make_epub.py           # EPUB 3 dengan nav + alt teks\n"
     "python3 make_listing.py        # teks deskripsi siap tempel\n"
     "python3 final_audit.py         # FAIL 0 WARN 0 OK n"),
    ("note", "Satu aturan yang tidak boleh dilanggar",
     "Berkas yang dijual dibangun ulang dari naskah **setiap kali naskah berubah**. Tidak ada "
     "berkas yang disimpan karena \"yang lama sudah benar\" — audit terakhir di proyek asal "
     "memang punya pemeriksaan khusus bernama _kesegaran_ untuk menangkap tepat kesalahan itu."),
]

SKILL_08 = [
    ("lead",
     "Sampul punya satu pekerjaan yang bisa diukur: pada ukuran 200 piksel, orang harus bisa "
     "membaca judulnya, mengenali jenis bukunya, dan tahu nama penulisnya. Kalau salah satu "
     "gagal, sampul itu belum selesai — seberapa pun indahnya pada ukuran penuh."),
    ("h", "Aturan yang lahir dari kesalahan nyata"),
    ("table", [0.34, 0.66],
     ["Aturan", "Sebabnya"],
     [["Nama penulis **dan** tahun di bagian bawah sampul depan", "di proyek asal, nama penulis sempat hilang dari sampul"],
      ["Tidak ada baris statistik di kaki sampul depan", "angka di kaki sampul tidak terbaca pada ukuran thumbnail dan membuat sampul terlihat seperti laporan"],
      ["Semua teks terbaca saat diperbesar 200%", "sampul belakang pernah dicetak dengan teks 7 pt yang hilang saat dicetak"],
      ["Tiga gambar produk, bukan satu", "pembeli tidak bisa menyentuh buku; tiga sudut menggantikan sentuhan"],
      ["Render 3D dengan tebal punggung yang benar", "buku 457 halaman yang dirender setipis 100 halaman terlihat palsu"]]),
    ("h", "Spesifikasi berkas"),
    ("table", [0.34, 0.30, 0.36],
     ["Berkas", "Ukuran", "Dipakai di"],
     [["Sampul produk", "2560 × 1440 px", "Gumroad, toko sendiri"],
      ["Thumbnail", "1600 × 1600 px", "Discover, daftar produk, profil"],
      ["Sampul cetak (bungkus)", "lebar = (2 × trim) + punggung + 0,125 inci bleed tiap sisi", "percetakan POD"],
      ["Render 3D", "6 sudut, 3000 px", "marketplace, iklan, media sosial"],
      ["Avatar profil", "800 × 800 px", "identitas penjual"]]),
    ("p",
     "Punggung dihitung dari jumlah halaman, bukan dikira-kira: `punggung = halaman ÷ 444` inci "
     "untuk kertas krem 60 lb. Buku 458 halaman berarti punggung 1,03 inci. Angka ini masuk ke "
     "berkas bungkus dan ke render 3D; kalau berbeda, gambar 3D-nya berbohong."),
    ("h", "Terjemahan untuk romance: sampul yang menjanjikan trope"),
    ("p",
     "Pembaca romance membeli **janji**, bukan kejutan. Sampul harus menyebut trope-nya tanpa "
     "kata-kata: ilustrasi kartun untuk rom-com, siluet dan langit senja untuk drama emosional, "
     "foto tubuh tanpa wajah untuk _steamy_, tipografi tangan untuk _small town_. Sampul yang "
     "ambigu mendapat klik dari orang yang salah — dan ulasan buruk dari mereka."),
    ("table", [0.26, 0.37, 0.37],
     ["Sinyal", "Kalau begini", "Pembaca menyimpulkan"],
     [["Palet", "pastel + ilustrasi", "rom-com, ringan, _closed door_"],
      ["Palet", "gelap + satu warna aksen", "drama, luka masa lalu, _slow burn_"],
      ["Tipografi", "serif tebal, huruf besar", "buku arus utama, toko buku"],
      ["Tipografi", "skrip/tangan", "small town, seri, penulis indie"],
      ["Figur", "dua orang berdekatan, wajah tidak terlihat", "fokus pada hubungan, bukan pada tokoh tunggal"],
      ["Objek", "satu benda besar (cangkir, kunci, gitar)", "satu tema, biasanya seri"]]),
    ("h", "Uji lima menit sebelum mengunci sampul"),
    ("ol", [
        "Perkecil sampul menjadi 200 px. Bisakah Anda membaca judulnya?",
        "Lihat dari jarak tiga meter. Apakah genre-nya masih terbaca?",
        "Ubah menjadi hitam-putih. Apakah masih ada hierarki: judul, lalu penulis, lalu gambar?",
        "Tutup separuh kanan. Apakah separuh kiri masih menjual?",
        "Tunjukkan pada lima orang yang membaca genre ini, tanpa menjelaskan apa pun. Tanyakan satu hal: \"buku ini tentang apa?\"",
    ]),
    ("note", "Kesalahan yang paling sering terjadi pada penulis pertama",
     "Menaruh terlalu banyak kata di sampul: tagline, kutipan pujian, tiga baris subjudul. "
     "Setiap elemen tambahan mengurangi ukuran judul. Judul adalah satu-satunya hal yang harus "
     "terbaca pada ukuran thumbnail."),
]

SKILL_09 = [
    ("lead",
     "Sampel gratis adalah mesin penjualan yang paling bekerja di proyek asal: ia memberi "
     "pembaca sesuatu yang benar-benar berguna, mengumpulkan alamat email, dan tidak memaksa "
     "siapa pun membayar sebelum tahu kualitas tulisannya."),
    ("h", "Spesifikasi sampel yang dipakai"),
    ("ul", [
        "**36 halaman** dari buku 457 halaman — sekitar 8%, cukup untuk satu bab utuh dan satu studi kasus.",
        "Dimulai dari **sampul berwarna**, bukan halaman judul telanjang.",
        "Setiap halaman diberi footer: _You have just read 12 of 457 pages_ — pembaca selalu tahu di mana ia berada.",
        "Berkasnya berasal dari **sumber yang sama** dengan berkas berbayar, sehingga tidak ada perbedaan kualitas.",
    ]),
    ("p",
     "Footer itu terlihat sepele dan justru paling berpengaruh: ia memberi tahu pembaca bahwa "
     "yang ia baca hanyalah 8%, tanpa satu kalimat promosi pun."),
    ("h", "Terjemahan untuk romance: sampel tiga bab"),
    ("table", [0.26, 0.74],
     ["Keputusan", "Alasan"],
     [["3 bab pertama, berhenti di **_hook_**", "bukan di tengah adegan; berhenti tepat setelah pertanyaan muncul"],
      ["Jangan beri adegan ciuman pertama", "itu alasan orang membeli; kalau sudah dapat gratis, tidak ada lagi yang dikejar"],
      ["Akhiri dengan satu halaman ajakan", "satu kalimat + satu tautan; bukan tiga paragraf penjualan"],
      ["Sertakan _content warning_", "menghindarkan ulasan buruk dari pembaca yang tidak menyukai tema berat"],
      ["Nama berkas jelas", "`Judul_Sampel_3_Bab.pdf` — bukan `final_final_v2.pdf`"]]),
    ("h", "Stempel pembeli — untuk berkas berbayar"),
    ("p",
     "Berkas berbayar di proyek asal dicap dengan alamat email pembeli pada halaman pertama saat "
     "pembelian. Ini bukan pelacakan, melainkan pengingat sopan bahwa berkas itu milik satu orang. "
     "Dua syarat teknis: PDF **tidak boleh terkunci** (kalau terkunci, tidak bisa dicap), dan "
     "toggle pencap harus dinyalakan pada berkas yang benar."),
    ("p",
     "**Untuk romance:** perlakuan yang sama masuk akal untuk buku berbayar, dan sama sekali "
     "tidak masuk akal untuk sampel gratis. Sampel yang dicap akan dibagikan orang — itu "
     "tujuannya."),
    ("note", "Uji yang wajib dilakukan sebelum peluncuran",
     "Beli produk Anda sendiri dengan kode diskon 100% (batas satu pemakaian), pakai alamat email "
     "yang berbeda, lalu buka berkasnya: halaman pertama harus sampul, cap harus memuat email itu, "
     "jumlah halaman harus benar. Setelah selesai, **hapus kodenya**. Kode 100% yang tertinggal "
     "adalah pintu gratis."),
]

SKILL_10 = [
    ("lead",
     "Harga di proyek asal diturunkan dari patokan pasar, bukan dari perasaan: tiga buku "
     "sejenis dibandingkan, lalu dipasang 10% di bawahnya. Metodenya bisa dipindahkan ke "
     "romance; **angkanya tidak**."),
    ("h", "Metode yang dipakai"),
    ("ol", [
        "Ambil tiga pembanding nyata di kategori yang sama, catat harganya hari itu.",
        "Hitung median.",
        "Pasang 10% di bawah median, lalu bulatkan ke angka yang enak dibaca.",
        "Tulis alasannya dalam satu kalimat yang bisa diucapkan: _karena buku sejenis dijual $50–55, dan saya sengaja di bawahnya_.",
        "Periksa hasil bersih setelah biaya, bukan harga di layar.",
    ]),
    ("h", "Mengapa angka $45 tidak boleh dibawa ke romance"),
    ("p",
     "$45 adalah harga buku akademik 457 halaman. Pembaca romance membeli 8–12 buku per bulan; "
     "pada $45 mereka membeli satu buku, bukan delapan. Memaksakan harga itu akan menghasilkan "
     "nol penjualan — bukan karena bukunya buruk, tetapi karena harganya keluar dari kebiasaan "
     "kategori."),
    ("table", [0.28, 0.30, 0.42],
     ["Bentuk", "Kisaran umum", "Catatan"],
     [["Novel tunggal (digital)", "$2,99–4,99", "titik terbanyak di $3,99; di atas $5,99 konversi turun tajam"],
      ["Seri, buku 1", "$0–0,99", "berfungsi sebagai iklan untuk buku 2–5"],
      ["Boxset 3–5 buku", "$7,99–12,99", "nilai per buku turun, total naik"],
      ["Edisi cetak POD", "$12,99–17,99", "mengikuti biaya cetak + margin toko"],
      ["Audiobook", "$7,99–14,99", "biaya produksi menentukan batas bawah"]]),
    ("p",
     "Angka di atas adalah kebiasaan pasar, bukan janji. Periksa sendiri di kategori Anda hari "
     "ini: urutkan 20 buku terlaris di subkategori Anda, catat harganya, ambil median. Metodenya "
     "sama seperti di proyek asal."),
    ("h", "Tangga diskon yang tidak merusak harga"),
    ("table", [0.24, 0.24, 0.22, 0.30],
     ["Kode", "Untuk siapa", "Diskon", "Batas"],
     [["_(tanpa kode)_", "pembeli biasa", "—", "harga penuh"],
      ["`LAUNCH20`", "pembaca awal", "20%", "50 pemakaian, 30 hari"],
      ["`KAMPUS25`", "dosen/mahasiswa", "25%", "tanpa batas waktu"],
      ["`ARC`", "pembaca pendahulu", "100%", "20 pemakaian, wajib ulasan jujur"]]),
    ("p",
     "Aturan yang tidak berubah dari proyek asal: **jangan pernah menurunkan harga di halaman "
     "produk**. Diskon adalah kesempatan, bukan harga baru. Harga yang tidak pernah dibayar "
     "siapa pun bukan harga."),
    ("h", "Tiga hal yang wajib dihitung sebelum menetapkan harga"),
    ("ul", [
        "**Biaya tetap per transaksi.** Di Gumroad 10% + $0,50 untuk trafik sendiri; 30% untuk penjualan dari Discover. Pada harga $3,99, biaya tetap itu setara 12% — jauh lebih terasa daripada pada $45.",
        "**Ambang payout.** Kalau ambang penarikan $100, pada $2,99 Anda butuh puluhan penjualan sebelum uang bisa ditarik. Rencanakan arus kasnya, bukan hanya marginnya.",
        "**Eksklusivitas.** Masuk program langganan (mis. Kindle Unlimited) menuntut eksklusivitas digital 90 hari. Itu pilihan strategi, bukan detail teknis — dan tidak bisa dibatalkan di tengah jalan.",
    ]),
    ("note", "Satu kalimat untuk diingat",
     "Harga bukan pernyataan tentang nilai buku Anda; ia pernyataan tentang siapa yang Anda "
     "ingin membacanya."),
]

SKILL_11 = [
    ("lead",
     "Halaman produk punya satu tugas: membuat orang yang sudah tertarik mengklik beli. Di "
     "proyek asal, deskripsi disusun dari enam bagian tetap, dan setiap bagian punya pekerjaan."),
    ("h", "Enam bagian deskripsi"),
    ("table", [0.06, 0.28, 0.66],
     ["#", "Bagian", "Isi dan pekerjaan"],
     [["1", "Satu kalimat pembuka", "satu angka atau satu pertanyaan yang membuat orang berhenti; bukan ringkasan"],
      ["2", "Apa isinya", "jumlah bab, halaman, gambar, tabel — nyata, bukan \"lengkap\""],
      ["3", "Mengapa berbeda", "satu hal yang tidak dilakukan buku sejenis"],
      ["4", "Apa yang didapat", "daftar berkas: PDF, EPUB, DOCX, paket gambar"],
      ["5", "Untuk siapa / bukan untuk siapa", "menyaring pembaca yang salah lebih berharga daripada menambah pembaca yang salah"],
      ["6", "FAQ", "tiga pertanyaan yang benar-benar ditanyakan: bisa dicetak? ada versi cetak? bagaimana kalau berkasnya rusak?"]]),
    ("h", "Jebakan teknis yang menghabiskan satu jam"),
    ("p",
     "Menempel teks dari dokumen lain ke kotak deskripsi Gumroad sering melebur semua paragraf "
     "menjadi satu blok. Penyebabnya: yang tersalin adalah teks polos. Solusinya bukan menyunting "
     "HTML, melainkan menyediakan **dua versi**: berformat (HTML) untuk disalin dari peramban, "
     "dan versi ringkas yang tetap enak dibaca kalau melebur."),
    ("p",
     "Aturan yang dipakai: setiap deskripsi punya versi cadangan tiga paragraf. Kalau versi "
     "berformat gagal, versi cadangan tetap layak dibaca — bukan bencana."),
    ("h", "Terjemahan untuk romance: blurb 150 kata"),
    ("p",
     "Blurb romance bukan sinopsis. Ia berhenti tepat sebelum hal yang ingin diketahui pembaca, "
     "dan menyebut trope tanpa menyebut kata \"trope\"."),
    ("code",
     "[Posisi tokoh A] punya satu aturan: [aturan yang ia pegang].\n"
     "[Posisi tokoh B] punya satu alasan untuk melanggarnya.\n"
     "\n"
     "Ketika [peristiwa pemicu] memaksa mereka [situasi bersama],\n"
     "[A] menemukan bahwa [konsekuensi emosional].\n"
     "\n"
     "Masalahnya bukan [rintangan luar]. Masalahnya [luka lama].\n"
     "\n"
     "[Judul] adalah [subgenre] tentang [tema]. Untuk pembaca yang menyukai\n"
     "[judul pembanding 1] dan [judul pembanding 2]."),
    ("table", [0.30, 0.70],
     ["Yang wajib ada", "Contoh isi"],
     [["Peringkat panas (_heat level_)", "\"closed door\" / \"one open-door scene\" / \"explicit\""],
      ["Peringatan isi", "kehilangan, kekerasan rumah tangga, gangguan makan — sebutkan, jangan disamarkan"],
      ["Janji akhir", "\"HEA\" atau \"HFN\" — pembaca romance menganggap ini kontrak, bukan kejutan"],
      ["Pembanding", "dua judul yang benar-benar mirip, bukan buku terkenal yang tidak berhubungan"]]),
    ("note", "Uji deskripsi dalam 30 detik",
     "Bacakan hanya tiga baris pertama kepada orang lain. Kalau ia bertanya \"jadi ini tentang "
     "apa?\", tiga baris itu belum bekerja. Kalau ia bertanya \"terus kenapa?\", tiga baris itu "
     "sudah bekerja."),
]

SKILL_12 = [
    ("lead",
     "Di proyek asal, peluncuran disusun sebagai urutan yang tidak boleh dibalik, dengan angka "
     "harapan yang jujur. Yang menjual bukan pengumuman, melainkan pesan pribadi."),
    ("h", "Urutan peluncuran"),
    ("table", [0.06, 0.50, 0.44],
     ["#", "Tindakan", "Hasil yang wajar diharapkan"],
     [["1", "Terbitkan sampel gratis **lebih dulu**", "satu tautan yang bisa dibagikan tanpa meminta uang"],
      ["2", "20 pesan pribadi, satu per satu, ke orang yang dikenal", "**2–3 penjualan** — hasil tertinggi dari seluruh bulan"],
      ["3", "Bagikan sampel di 3 komunitas yang tepat", "5–10 pengunduh, 0–1 penjualan, daftar email bertambah"],
      ["4", "10 surel ke pengajar/pengulas yang relevan", "1 penjualan, atau 1 kelas yang memakai buku"],
      ["5", "5 tawaran afiliasi 30%", "0–1 kerja sama, nilainya berkali-kali lipat"],
      ["6", "1 postingan publik", "trafik; jarang langsung menjadi penjualan"],
      ["7", "Baru setelah ada penjualan berbayar: nyalakan Discover", "bonus, bukan rencana"]]),
    ("h", "Pesan pribadi yang bekerja"),
    ("p",
     "Bukan pengumuman. Satu nama, satu detail tentang mereka, satu tautan sampel, satu "
     "pertanyaan yang bisa dijawab tanpa membeli."),
    ("code",
     "Subject: A book I finished — and a question\n"
     "\n"
     "Hi [Name],\n"
     "\n"
     "I finished the book I mentioned. [Satu kalimat tentang isinya.]\n"
     "\n"
     "There is a free sample here, no email wall: [tautan]\n"
     "\n"
     "One favour, and it is not a purchase: tell me which chapter you\n"
     "would skip. That answer is worth more to me than a sale this week."),
    ("p",
     "Kalimat terakhir itu yang membuat pesan dijawab. Ia mengubah permintaan menjadi pertanyaan, "
     "dan orang menjawab pertanyaan."),
    ("h", "Terjemahan untuk romance"),
    ("table", [0.26, 0.74],
     ["Saluran", "Yang benar-benar bekerja"],
     [["**ARC / pembaca pendahulu**", "20–30 pembaca yang mendapat buku gratis 2–3 minggu sebelum terbit, dengan kewajiban ulasan **jujur** — bukan ulasan positif"],
      ["**Newsletter sendiri**", "satu-satunya aset yang Anda miliki; sampel gratis adalah alat pengumpulnya"],
      ["**Seri, bukan buku tunggal**", "buku 1 murah atau gratis, buku 2–4 berbayar; pembaca romance membaca berurutan"],
      ["**BookTok / Instagram**", "satu adegan, satu kutipan, satu reaksi — bukan sinopsis; konsisten 3× seminggu selama 6 minggu"],
      ["**Tukar tautan antarpenulis**", "saling menyebut di newsletter; gratis dan paling efektif setelah ARC"],
      ["**Iklan berbayar**", "baru setelah ada 20+ ulasan dan Anda tahu kata kunci mana yang menghasilkan klik"]]),
    ("h", "Yang merusak peluncuran"),
    ("ul", [
        "**Broadcast ke ratusan alamat.** Nol penjualan, dan domain email Anda masuk daftar hitam.",
        "**Membeli ulasan atau menukarnya dengan imbalan.** Melanggar aturan toko dan merusak kepercayaan yang sedang dibangun.",
        "**Menjanjikan \"harga naik besok\" lalu tidak menaikkannya.** Sekali berbohong soal harga, semua angka Anda kehilangan arti.",
        "**Menunda peluncuran sampai sempurna.** Buku yang terbit dengan tiga kesalahan kecil selalu mengalahkan buku yang tidak pernah terbit."]),
    ("note", "Angka yang wajib dicatat setiap hari",
     "Empat saja: kunjungan halaman produk, jumlah penjualan, pendapatan bersih, dan dari mana "
     "kunjungan datang. Di akhir bulan hitung **pendapatan bersih per 100 kunjungan**. Di bawah "
     "$2, masalahnya harga atau audiens. Di atas $8, naikkan harga dan ulangi sebulan."),
]

SKILL_13 = [
    ("lead",
     "Daftar ini dijalankan **sebelum** tombol terbit ditekan, bukan sesudah. Di proyek asal, "
     "45 pemeriksaan otomatis dan satu daftar manusia harus lulus bersamaan."),
    ("h", "Naskah"),
    ("check", [
        "24 bab ada, masing-masing mengubah keadaan (kalimat \"dari … menjadi …\" terisi).",
        "Setiap bab berada dalam rentang panjang yang direncanakan; tidak ada bab 1,25× median.",
        "Tidak ada frasa klise dari daftar pantau.",
        "Nama tokoh konsisten; tidak ada varian ejaan.",
        "Timeline tidak melompat mundur; tanggal di bible cocok dengan naskah.",
        "Setiap adegan punya alasan; adegan yang bisa dihapus tanpa mengubah keadaan sudah dihapus.",
        "Tidak ada blok ringkasan di akhir bab; bab berhenti pada kalimat yang bekerja.",
    ]),
    ("h", "Berkas"),
    ("check", [
        "PDF dibangun ulang dari naskah terakhir, bukan dari berkas lama.",
        "Halaman pertama PDF = sampul berwarna; setelahnya halaman judul.",
        "Jumlah halaman sesuai; daftar isi menunjuk halaman yang benar.",
        "Fonta tertanam; tidak ada karakter rusak atau kotak kosong.",
        "EPUB terbuka di dua aplikasi berbeda; navigasi bab bekerja.",
        "DOCX tidak memuat komentar, catatan revisi, atau teks terlacak.",
        "Sampel berasal dari sumber yang sama dan berhenti di titik yang direncanakan.",
        "Judul berkas dapat dibaca manusia, bukan `final_final_v2`.",
    ]),
    ("h", "Halaman jual"),
    ("check", [
        "Harga terbaca benar, bukan $0.",
        "Tiga gambar produk tampil; thumbnail terbaca pada ukuran kecil.",
        "Deskripsi berformat, bukan satu blok melebur.",
        "Tidak ada teks cadangan seperti `[link to your free sample product]` yang tertinggal.",
        "Kategori dan tag terisi; tag memakai spasi, bukan tanda hubung.",
        "Kebijakan pengembalian tertulis dan konsisten dengan janji di deskripsi.",
        "Tombol beli bisa diklik sampai halaman pembayaran.",
    ]),
    ("h", "Etika"),
    ("check", [
        "Tidak ada klaim yang tidak bisa dibuktikan di halaman jual.",
        "Peringatan isi disebut jujur, bukan disamarkan.",
        "Ulasan tidak dibeli dan tidak ditukar dengan imbalan.",
        "Nama dan identitas orang nyata tidak dipakai tanpa izin.",
        "Hak cipta gambar dan kutipan jelas; sumber disebut.",
    ]),
    ("note", "Aturan terakhir",
     "Kalau ada satu kotak yang belum dicentang dan Anda tergoda menerbitkan juga: ingat bahwa "
     "satu-satunya hal yang lebih mahal daripada menunda seminggu adalah memperbaiki produk yang "
     "sudah dibeli orang."),
]

LAMPIRAN_A = [
    ("lead",
     "Struktur folder yang membuat semua skill di atas bisa dijalankan tanpa berpikir."),
    ("code",
     "novel/\n"
     "├── manuscript/\n"
     "│   ├── bab_01.md ... bab_24.md\n"
     "│   └── bonus/epilog.md\n"
     "├── bible/\n"
     "│   ├── tokoh.json          nama resmi + varian salah\n"
     "│   ├── timeline.json       [{\"bab\": 1, \"tanggal\": \"2026-03-02\"}, ...]\n"
     "│   └── kontinuitas.md      benda, cuaca, luka, uang\n"
     "├── tools/\n"
     "│   └── audit_novel.py\n"
     "├── render/\n"
     "│   ├── render_novel.py     naskah -> interior.pdf   (penanda bab)\n"
     "│   ├── make_ebook.py       + sampul -> ebook.pdf\n"
     "│   ├── make_sample.py      3 bab -> sample.pdf\n"
     "│   ├── make_cover.py       bungkus cetak\n"
     "│   ├── make_epub.py        EPUB 3 + nav + alt teks\n"
     "│   └── final_audit.py      FAIL/WARN/OK\n"
     "├── art/\n"
     "│   ├── cover_front.png      300 dpi\n"
     "│   ├── cover_back.png\n"
     "│   └── renders/             6 sudut, 3000 px\n"
     "└── publish/\n"
     "    ├── Judul_ebook.pdf\n"
     "    ├── Judul.epub\n"
     "    ├── Judul.docx\n"
     "    ├── Judul_sample.pdf\n"
     "    └── listing.txt"),
    ("h", "Urutan perintah, dari naskah kosong sampai siap jual"),
    ("code",
     "python3 tools/audit_novel.py            # 1. naskah lulus dulu\n"
     "python3 render/render_novel.py          # 2. interior.pdf\n"
     "python3 render/make_ebook.py            # 3. ebook.pdf (sampul + isi)\n"
     "python3 render/make_sample.py           # 4. sample.pdf\n"
     "python3 render/make_cover.py            # 5. bungkus cetak\n"
     "python3 render/make_epub.py             # 6. EPUB\n"
     "python3 render/final_audit.py           # 7. FAIL 0 WARN 0 OK n"),
    ("h", "Tiga aturan berkas"),
    ("ol", [
        "**Satu sumber.** Naskah di `manuscript/` adalah satu-satunya kebenaran. Semua berkas jual dibangun darinya.",
        "**Nama berkas = judul.** `Bertahan_di_Musim_Hujan_ebook.pdf`, bukan `buku_final2.pdf`.",
        "**Jangan menaruh berkas besar di riwayat versi.** Simpan di penyimpanan luar; yang masuk riwayat hanya naskah dan skrip.",
    ]),
]

LAMPIRAN_B = [
    ("lead",
     "Enam perintah yang bisa ditempel langsung ke asisten AI. Semuanya berbentuk permintaan "
     "yang hasilnya bisa diperiksa, bukan permintaan \"buatkan yang bagus\"."),
    ("h", "1 · Menyusun arsitektur"),
    ("code",
     "Saya menulis novel romance [subgenre], target 90.000 kata, 24 bab.\n"
     "Buat tabel 24 baris dengan kolom: bab, beat, satu kalimat\n"
     "\"X berubah dari ... menjadi ...\", target kata.\n"
     "Aturan: setiap bab harus mengubah keadaan hubungan. Kalau dua baris\n"
     "mengubah keadaan dengan cara yang sama, tandai dan usulkan penggantinya.\n"
     "Jangan menulis prosa."),
    ("h", "2 · Memeriksa bab"),
    ("code",
     "Baca bab ini. Laporkan hanya empat hal, dalam bentuk daftar:\n"
     "1. Kalimat yang bisa dihapus tanpa kehilangan informasi.\n"
     "2. Frasa klise romance, kutip persis.\n"
     "3. Perpindahan waktu/tempat yang membingungkan, sebut paragrafnya.\n"
     "4. Apakah keadaan hubungan berubah di bab ini? Jawab ya/tidak dan\n"
     "   tunjukkan kalimat yang membuktikannya.\n"
     "Jangan menulis ulang bab ini."),
    ("h", "3 · Menyamakan suara"),
    ("code",
     "Berikut kartu suara dua tokoh. Tulis ulang adegan ini dua kali, sekali\n"
     "dari POV masing-masing, maksimal 250 kata tiap versi.\n"
     "Syarat: kedua versi tidak boleh berbagi lebih dari tiga kata benda\n"
     "selain yang wajib (pintu, meja, hujan).\n"
     "[kartu suara A] [kartu suara B] [adegan]"),
    ("h", "4 · Menyusun blurb"),
    ("code",
     "Buat blurb 150 kata untuk novel ini dengan struktur: posisi A, posisi B,\n"
     "peristiwa pemicu, konsekuensi emosional, luka lama, janji akhir (HEA).\n"
     "Larangan: pertanyaan retoris di akhir, kata \"tak terduga\",\n"
     "kata \"mengubah hidupnya selamanya\", dan sinopsis bab 4 ke atas.\n"
     "Sertakan heat level dan content warning di luar blurb."),
    ("h", "5 · Mengaudit kontinuitas"),
    ("code",
     "Berikut 24 bab dan bible/timeline.json. Temukan:\n"
     "1. tanggal yang melompat mundur,\n"
     "2. benda yang hilang lalu muncul,\n"
     "3. luka yang sembuh terlalu cepat,\n"
     "4. cuaca/musim yang tidak konsisten.\n"
     "Untuk tiap temuan: bab, kutipan, dan usulan perbaikan satu baris.\n"
     "Kalau tidak ada temuan, katakan tidak ada — jangan mengarang."),
    ("h", "6 · Menyiapkan peluncuran"),
    ("code",
     "Buat 20 pesan pembuka yang berbeda untuk 20 orang yang saya kenal,\n"
     "masing-masing maksimal 80 kata, berisi: satu detail tentang mereka\n"
     "(saya isi sendiri), satu kalimat tentang buku, satu tautan sampel,\n"
     "satu pertanyaan yang bisa dijawab tanpa membeli.\n"
     "Larangan: kata \"promo\", \"diskon\" di dua kalimat pertama,\n"
     "dan kalimat pembuka yang sama di dua pesan."),
    ("h", "Mulai besok pagi"),
    ("ol", [
        "Buat folder `novel/` dengan tiga subfolder: `manuscript/`, `bible/`, `tools/`. Sepuluh menit.",
        "Tulis 24 kalimat \"dari … menjadi …\" (skill 01). Jangan menulis prosa sebelum ini selesai.",
        "Isi `bible/tokoh.json` dan `bible/timeline.json` untuk tiga tokoh utama dan lima titik waktu pertama.",
        "Tulis bab 1 sampai selesai, lalu jalankan `python3 tools/audit_novel.py`. Perbaiki FAIL-nya hari itu.",
        "Ulangi butir 4 dua puluh tiga kali. Semua yang lain di berkas ini menunggu di ujung sana.",
    ]),
    ("h", "Penutup"),
    ("p",
     "Sebelas dari tiga belas skill di berkas ini bisa dijalankan tanpa komputer. Yang butuh "
     "komputer hanya dua: audit otomatis dan produksi berkas. Itu bukan kebetulan — urutan, "
     "disiplin, dan pemeriksaanlah yang membuat sebuah naskah menjadi produk, dan semuanya "
     "bisa dikerjakan dengan pena."),
    ("quote",
     "Naskah yang selesai dengan tiga kesalahan kecil selalu mengalahkan naskah sempurna yang "
     "tidak pernah selesai."),
]
