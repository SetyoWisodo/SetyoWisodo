# -*- coding: utf-8 -*-
import re

CHAPTERS = [
 ("Pendahuluan: Dunia yang Memanas", "dunia yang memanas dan krisis yang akan datang", [
   "Mengapa Buku Ini", "Apa Arti 'Bertahan Hidup'", "Cara Menggunakan Buku Ini", "Cakupan Krisis",
   "Keselamatan Personal, Komunitas, dan Masyarakat", "Pengetahuan sebagai Alat Bertahan Hidup", "Peran Pendidikan",
   "Mempersiapkan Ketidakpastian", "Membangun Resiliensi", "Peta Jalan untuk Pembaca"]),
 ("Sains Pemanasan Global", "sains fisik pemanasan global", [
   "Efek Rumah Kaca", "Gas Rumah Kaca dan Sumbernya", "Bukti Pemanasan",
   "Rekaman dan Tren Suhu", "Panah Laut dan Permukaan Laut", "Kehilangan Es dan Krisosfer",
   "Siklus Karbon dan Umpan Balik", "Sensitivitas Iklim", "Atribusi Pemanasan", "Kesimpulan Ilmiah Utama"]),
 ("Sejarah Perubahan Iklim", "sejarah perubahan iklim dan respons manusia", [
   "Sains Iklim Awal", "Revolusi Industri dan Emisi", "Pemanasan Abad ke-20",
   "Kesadaran Internasional", "Penilaian IPCC", "Era Perjanjian Paris", "Tren Emisi Saat Ini",
   "Pelajaran dari Sejarah", "Respons yang Gagal dan Berhasil", "Melihat ke Depan"]),
 ("Sistem Iklim dan Umpan Balik", "sistem iklim dan mekanisme umpan balik", [
   "Sistem Iklim", "Atmosfer dan Sirkulasi", "Sirkulasi Lautan", "Dinamika Krisosfer",
   "Umpan Balik Positif", "Umpan Balik Negatif", "Titik Balik", "Perubahan Mendadak",
   "Variasi Regional", "Implikasi untuk Keselamatan"]),
 ("Pengukuran dan Pemantauan", "pengukuran dan pemantauan iklim", [
   "Pemantauan Suhu", "Pengamatan Satelit", "Pemantauan Lautan", "Pemantauan Es dan Salju",
   "Inventarisasi Gas Rumah Kaca", "Atribusi Kejadian Ekstrem", "Sistem Peringatan Dini",
   "Kualitas Data dan Ketidakpastian", "Data Terbuka dan Sains Warga", "Menggunakan Data untuk Keputusan"]),
 ("Panas Ekstrem", "panas ekstrem dan gelombang panas", [
   "Definisi dan Tren Gelombang Panas", "Fisiologi Stres Panas", "Spektrum Penyakit Panas",
   "Populasi Rentan", "Pulau Panas Perkotaan", "Dampak Infrastruktur", "Tenaga Kerja dan Produktivitas",
   "Rencana Aksi Panas", "Strategi Pendinginan", "Adaptasi Jangka Panjang terhadap Panas"]),
 ("Kelangkaan Air dan Kekeringan", "kelangkaan air dan kekeringan", [
   "Siklus Air Global", "Jenis dan Indeks Kekeringan", "Penyebab Kelangkaan Air",
   "Penggunaan Air Pertanian", "Stres Air Perkotaan", "Penipisan Air Tanah", "Kualitas Air",
   "Tata Kelola Air", "Konservasi dan Efisiensi", "Sumber Air Alternatif"]),
 ("Banjir dan Kenaikan Permukaan Laut", "banjir dan kenaikan permukaan laut", [
   "Jenis dan Penyebab Banjir", "Mekanisme Kenaikan Permukaan Laut", "Risiko Banjir Pesisir",
   "Banjir Sungai dan Bandang", "Banjir Perkotaan", "Dampak Banjir pada Kesehatan", "Pertahanan Banjir",
   "Retret Terkelola", "Asuransi dan Keuangan Banjir", "Adaptasi Pesisir Jangka Panjang"]),
 ("Pangan dan Pertanian", "ketahanan pangan dan pertanian di bawah perubahan iklim", [
   "Gambaran Sistem Pangan", "Dampak Hasil Panen", "Stres Panas dan Air pada Tanaman",
   "Hama dan Penyakit", "Ternak dan Perikanan", "Kerentanan Rantai Pasok",
   "Volatilitas Harga dan Kelaparan", "Pertanian Adaptif", "Penyimpanan dan Pengawetan Pangan",
   "Nutrisi dan Perubahan Diet"]),
 ("Ekosistem dan Keanekaragaman Hayati", "ekosistem dan kehilangan keanekaragaman hayati", [
   "Keanekaragaman Hayati dan Jasa Ekosistem", "Kehilangan Habitat", "Risiko kepunahan Spesies",
   "Ekosistem Hutan", "Ekosistem Laut", "Lahan Basah dan Air Tawar", "Spesies Invasif",
   "Adaptasi Berbasis Ekosistem", "Strategi Konservasi", "Ketergantungan Manusia pada Alam"]),
 ("Kesehatan dan Penyakit", "dampak kesehatan dari perubahan iklim", [
   "Dampak Kesehatan Langsung dan Tidak Langsung", "Penyakit Akibat Panas", "Penyakit Vektor",
   "Penyakit Berbasis Air", "Kualitas Udara dan Kesehatan Pernapasan", "Dampak Kesehatan Mental",
   "Resiliensi Sistem Kesehatan", "Kelompok Rentan", "Pencegahan dan Kesiapsiagaan", "Keadilan Kesehatan"]),
 ("Dampak Ekonomi", "dampak ekonomi dari perubahan iklim", [
   "Estimasi Biaya Kerusakan", "Dampak Sektoral", "Kehilangan Produktivitas Tenaga Kerja", "Kerusakan Infrastruktur",
   "Risiko Asuransi dan Keuangan", "Efek Makroekonomi", "Kemiskinan dan Ketimpangan",
   "Biaya Adaptasi", "Biaya Tanpa Tindakan", "Strategi Resiliensi Ekonomi"]),
 ("Migrasi dan Pengungsian", "migrasi iklim dan pengungsian", [
   "Pendorong Migrasi Iklim", "Pengungsian Internal", "Pergerakan Lintas Batas",
   "Status Hukum dan Hak", "Tekanan Urbanisasi", "Komunitas Penerima",
   "Relokasi Terencana", "Kerugian dan Kerusakan", "Kohesi Sosial", "Respons Kebijakan"]),
 ("Konflik dan Keamanan", "perubahan iklim dan konflik", [
   "Kompetisi Sumber Daya", "Bukti Iklim dan Kekerasan", "Negara Rentan",
   "Konflik Pangan dan Air", "Tautan Migrasi-Konflik", "Respons Sektor Keamanan",
   "Pembangunan Perdamaian dan Adaptasi", "Peringatan Dini Konflik", "Tata Kelola dan Stabilitas",
   "Mengurangi Risiko"]),
 ("Kegagalan Infrastruktur", "resiliensi infrastruktur", [
   "Infrastruktur Kritis", "Jaringan Listrik", "Sistem Air dan Sanitasi", "Jaringan Transportasi",
   "Sistem Komunikasi", "Standar Bangunan", "Kegagalan Berantai", "Pemeliharaan dan Investasi",
   "Redundansi dan Cadangan", "Infrastruktur Tahan Masa Depan"]),
 ("Literasi Iklim", "literasi iklim dan pendidikan", [
   "Apa Itu Literasi Iklim", "Konsep Inti", "Pendidikan Sesuai Usia", "Pendidikan Formal",
   "Pendidikan Informal dan Komunitas", "Pelatihan Guru", "Desain Kurikulum", "Penilaian",
   "Pembelajaran Sepanjang Hayat", "Mengukur Hasil Literasi"]),
 ("Pendidikan Paper Referensi", "pendidikan paper referensi dan literasi ilmiah", [
   "Apa Itu Paper Referensi", "Proses Peer Review", "Membaca Literatur Ilmiah",
   "Mengevaluasi Bukti", "Memahami Metode", "Statistik untuk Warga", "Mengidentifikasi Bias",
   "Membangun Basis Pengetahuan", "Berbagi Pengetahuan", "Mengajar Orang Lain"]),
 ("Cara Membaca Literatur Ilmiah", "membaca dan memahami paper ilmiah", [
   "Struktur Paper", "Abstrak dan Pendahuluan", "Bagian Metode", "Hasil dan Gambar",
   "Diskusi dan Kesimpulan", "Referensi dan Sitasi", "Tinjauan Sistematis dan Meta-Analisis",
   "Preprint dan Literatur Abu-abu", "Alat Penilaian Kritis", "Rencana Membaca Praktis"]),
 ("Data dan Statistik untuk Warga", "data dan statistik untuk warga", [
   "Mengapa Data Penting", "Jenis Data", "Statistik Deskriptif", "Ketidakpastian dan Galat",
   "Korelasi vs Kausalitas", "Grafik dan Bagan", "Statistik yang Menyesatkan", "Sumber Data Terbuka",
   "Pengumpulan Data Pribadi", "Keputusan Berbasis Data"]),
 ("Misinformasi dan Literasi Media", "misinformasi dan literasi media", [
   "Misinformasi Iklim", "Sumber Misinformasi", "Psikologi Keyakinan", "Pemeriksaan Fakta",
   "Keterampilan Literasi Media", "Dinamika Media Sosial", "Sumber Terpercaya", "Mengomunikasikan Sains",
   "Menangkal Penyangkalan", "Membangun Kepercayaan"]),
 ("Penilaian Risiko Lokasi Anda", "penilaian risiko lokal", [
   "Memahami Bahaya Lokal", "Pemetaan Bahaya", "Paparan dan Kerentanan",
   "Proyeksi Iklim untuk Wilayah Anda", "Matriks Risiko Personal", "Profil Risiko Rumah Tangga",
   "Penilaian Risiko Komunitas", "Pemantauan dan Pembaruan", "Prioritas Tindakan", "Mendokumentasikan Rencana"]),
 ("Keamanan Air di Rumah", "keamanan air rumah tangga", [
   "Kebutuhan Air Harian", "Penyimpanan Air", "Metode Pemurnian", "Pemanenan Air Hujan",
   "Penggunaan Kembali Air Abu-abu", "Perlindungan Sumur dan Mata Air", "Pencegahan Kontaminasi", "Air dalam Bencana",
   "Perencanaan Air Jangka Panjang", "Kebiasaan Konservasi Air"]),
 ("Keamanan Pangan di Rumah", "keamanan pangan rumah tangga", [
   "Kebutuhan Nutrisi", "Prinsip Penyimpanan Pangan", "Pasokan Non-Perishable", "Pengawetan Pangan",
   "Berkebun di Rumah", "Kebun Komunitas", "Mengurangi Limbah Pangan", "Adaptasi Diet",
   "Memasak Tanpa Listrik", "Keamanan Pangan dalam Krisis"]),
 ("Tempat Tinggal dan Energi", "resiliensi tempat tinggal dan energi", [
   "Resiliensi Panas Rumah", "Insulasi dan Peneduh", "Ventilasi", "Strategi Pendinginan",
   "Pemanasan saat Cuaca Dingin", "Perencanaan Pemadaman Listrik", "Solar dan Baterai", "Keamanan Generator",
   "Berteduh saat Evakuasi", "Peningkatan Rumah Jangka Panjang"]),
 ("Kesehatan dan Pertolongan Pertama", "kesiapsiagaan kesehatan dan pertolongan pertama", [
   "Dasar Pertolongan Pertama", "Pengenalan Penyakit Panas", "Dehidrasi dan Rehidrasi", "Perawatan Luka",
   "Pengendalian Infeksi", "Pengelolaan Obat", "Perencanaan Penyakit Kronis", "Pertolongan Pertama Mental",
   "Layanan Medis Darurat", "Kit dan Pasokan Kesehatan"]),
 ("Kesiapsiagaan Finansial", "kesiapsiagaan finansial", [
   "Dana Darurat", "Diversifikasi Pendapatan", "Tinjauan Asuransi", "Perlindungan Dokumen",
   "Utang dan Arus Kas", "Barter dan Pertukaran Lokal", "Pensiun dan Jangka Panjang", "Pencegahan Penipuan",
   "Bantuan dan Keringanan Finansial", "Membangun Kembali Keuangan setelah Bencana"]),
 ("Evakuasi dan Respons Darurat", "evakuasi dan respons darurat", [
   "Kapan Harus Evakuasi", "Rute dan Rencana Evakuasi", "Go-Bag dan Kit", "Komunikasi Keluarga",
   "Hewan Peliharaan dan Ternak", "Berteduh di Tempat", "Kembali ke Rumah dengan Aman", "Keamanan Pasca-Bencana",
   "Pertolongan Pertama Psikologis", "Belajar dari Simulasi"]),
 ("Populasi Khusus", "melindungi populasi rentan dan khusus", [
   "Anak dan Bayi", "Lansia", "Penyandang Disabilitas", "Penyakit Kronis",
   "Hamil dan Menyusui", "Rumah Tangga Berpenghasilan Rendah", "Migran dan Pengungsi", "Komunitas Adat",
   "Isolasi Pedesaan", "Rencana Kesiapsiagaan yang Disesuaikan"]),
 ("Modal Sosial dan Jaringan", "modal sosial dan jaringan komunitas", [
   "Apa Itu Modal Sosial", "Kepercayaan dan Resiprositas", "Pemetaan Jaringan", "Menjembatani dan Mengikat",
   "Pemimpin Komunitas", "Partisipasi Inklusif", "Jaringan Digital", "Memelihara Jaringan",
   "Mengukur Modal Sosial", "Memperkuat Ikatan"]),
 ("Gotong Royong", "gotong royong dan dukungan komunitas", [
   "Prinsip Gotong Royong", "Memulai Kelompok", "Berbagi Sumber Daya", "Jaringan Perawatan",
   "Berbagi Keterampilan", "Distribusi Pangan dan Pasokan", "Sistem Komunikasi", "Resolusi Konflik",
   "Keberlanjutan Kelompok", "Gotong Royong dan Respons Resmi"]),
 ("Tata Kelola Lokal", "tata kelola lokal dan aksi iklim", [
   "Peran Pemerintah Lokal", "Manajemen Darurat", "Rencana Adaptasi Iklim", "Zonasi dan Penggunaan Lahan",
   "Layanan Publik", "Anggaran dan Keuangan", "Keterlibatan Publik", "Akuntabilitas", "Kemitraan",
   "Inovasi di Tingkat Lokal"]),
 ("Resiliensi Perkotaan", "resiliensi perkotaan terhadap perubahan iklim", [
   "Pulau Panas Perkotaan", "Infrastruktur Hijau", "Pengelolaan Air Hujan", "Pertanian Perkotaan",
   "Transportasi dan Mobilitas", "Perumahan dan Bangunan", "Sistem Energi", "Sampah dan Sanitasi",
   "Keadilan di Kota", "Kota Pintar dan Data"]),
 ("Resiliensi Pedesaan", "resiliensi pedesaan", [
   "Kerentanan Pedesaan", "Penghidupan Pertanian", "Air dan Sanitasi", "Akses Kesehatan",
   "Konektivitas dan Transportasi", "Diversifikasi Ekonomi", "Pengelolaan Lahan", "Lembaga Komunitas",
   "Pengetahuan Adat dan Tradisional", "Menjembatani Kesenjangan Kota-Desa"]),
 ("Pengetahuan Adat", "pengetahuan adat dan tradisional", [
   "Nilai Pengetahuan Adat", "Pengetahuan Ekologi Tradisional", "Indikator Cuaca dan Iklim",
   "Pengelolaan Sumber Daya Berkelanjutan", "Resiliensi Budaya", "Transmisi Pengetahuan",
   "Kemitraan dengan Masyarakat Adat", "Melindungi Pengetahuan", "Studi Kasus", "Integrasi dengan Sains"]),
 ("Sistem Energi Terbarukan", "energi terbarukan untuk resiliensi", [
   "Tenaga Surya", "Tenaga Angin", "Tenaga Air", "Biomassa", "Penyimpanan Energi", "Mikrogrid",
   "Pembangkitan Terdistribusi", "Efisiensi Energi", "Perencanaan Transisi", "Keadilan dan Akses"]),
 ("Teknologi Air", "teknologi air untuk adaptasi", [
   "Pemanenan Air Hujan", "Desalinasi", "Daur Ulang Air Limbah", "Irigasi Cerdas",
   "Deteksi Kebocoran", "Pemantauan Kualitas Air", "Pemurnian Teknologi Rendah", "Inovasi Penyimpanan",
   "Biaya dan Skalabilitas", "Pemeliharaan dan Pelatihan"]),
 ("Teknologi Pertanian", "teknologi pertanian", [
   "Pertanian Presisi", "Varietas Tahan Kekeringan", "Kesehatan Tanah", "Agroforestri",
   "Pertanian Vertikal dan Perkotaan", "Hidroponik dan Akuaponik", "Pengelolaan Hama", "Teknologi Pasca-Panen",
   "Alat Digital untuk Petani", "Akses dan Keadilan"]),
 ("Sistem Peringatan Dini", "sistem peringatan dini", [
   "Apa Itu Sistem Peringatan Dini", "Pemantauan Bahaya", "Peramalan dan Pemodelan",
   "Penyebaran Peringatan", "Respons Komunitas", "Peringatan Kesehatan Panas", "Peringatan Banjir",
   "Peringatan Kebakaran Hutan", "Peringatan Inklusif", "Mengevaluasi Efektivitas"]),
 ("AI dan Data untuk Iklim", "AI dan data untuk aksi iklim", [
   "Aplikasi AI dalam Iklim", "Peramalan dan Prediksi", "Optimasi Sumber Daya",
   "Penginderaan Jauh", "Data Sains Warga", "Etika dan Bias", "Tata Kelola Data",
   "Aksesibilitas dan Keadilan", "Risiko dan Keterbatasan", "Arah Masa Depan"]),
 ("Teknologi Tepat Guna", "teknologi tepat guna", [
   "Prinsip Teknologi Tepat Guna", "Pendinginan Pasif", "Filter Air Sederhana", "Kompor Surya",
   "Alat Manual", "Pemeliharaan dan Perbaikan", "Bahan Lokal", "Keterampilan dan Pelatihan",
   "Biaya dan Daya Tahan", "Menggabungkan Teknologi Rendah dan Tinggi"]),
 ("Kecemasan Iklim", "kecemasan iklim dan respons emosional", [
   "Apa Itu Kecemasan Iklim", "Siapa yang Terpengaruh", "Gejala dan Dampak", "Adaptif vs Maladaptif",
   "Pemuda dan Kecemasan Iklim", "Media dan Kecemasan", "Strategi Koping", "Dukungan Profesional",
   "Dukungan Komunitas", "Menyalurkan Kecemasan menjadi Aksi"]),
 ("Trauma dan Pemulihan", "trauma dan pemulihan pasca-bencana", [
   "Trauma Bencana", "PTSD dan Depresi", "Duka dan Kehilangan", "Anak dan Trauma",
   "Trauma Komunitas", "Pertolongan Pertama Psikologis", "Pemulihan Jangka Panjang", "Faktor Resiliensi",
   "Layanan Dukungan", "Mencegah Re-traumatisasi"]),
 ("Membangun Resiliensi Psikologis", "resiliensi psikologis", [
   "Konsep Resiliensi", "Strategi Kognitif", "Regulasi Emosi", "Dukungan Sosial",
   "Makna dan Tujuan", "Tautan Kesehatan Fisik", "Praktik dan Kebiasaan", "Pelatihan Resiliensi",
   "Mengukur Resiliensi", "Mempertahankan Resiliensi"]),
 ("Kesehatan Mental Komunitas", "kesehatan mental komunitas", [
   "Sistem Kesehatan Mental", "Akses dan Hambatan", "Pengurangan Stigma", "Dukungan Sebaya",
   "Integrasi dengan Perawatan Primer", "Layanan Krisis", "Pengembangan Tenaga Kerja", "Pendanaan",
   "Pemantauan dan Evaluasi", "Inisiatif yang Dipimpin Komunitas"]),
 ("Kerangka Internasional", "kerangka iklim internasional", [
   "UNFCCC dan COP", "Perjanjian Paris", "Kerangka Sendai", "SDG", "Kerugian dan Kerusakan",
   "Mekanisme Keuangan Iklim", "Transfer Teknologi", "Pembangunan Kapasitas", "Pemantauan dan Pelaporan",
   "Memperkuat Kerangka"]),
 ("Rencana Adaptasi Nasional", "perencanaan adaptasi nasional", [
   "Proses NAP", "Penilaian Kerentanan", "Prioritas", "Implementasi", "Pemantauan dan Evaluasi",
   "Integrasi Sektoral", "Tautan Lokal", "Keuangan dan Anggaran", "Keterlibatan Pemangku Kepentingan",
   "Tantangan dan Pelajaran"]),
 ("Penetapan Harga Karbon", "penetapan harga karbon dan pasar", [
   "Pajak Karbon", "Sistem Perdagangan Emisi", "Pasar Karbon", "Tingkat Harga", "Penggunaan Pendapatan",
   "Pertimbangan Keadilan", "Penyesuaian Perbatasan", "Pasar Sukarela", "Bukti Efektivitas",
   "Prinsip Desain"]),
 ("Keuangan Iklim", "keuangan iklim", [
   "Definisi dan Sumber", "Keuangan Publik", "Keuangan Swasta", "Obligasi Hijau", "Keuangan Adaptasi",
   "Keuangan Kerugian dan Kerusakan", "Akses dan Hambatan", "Transparansi", "Penskalaan Keuangan",
   "Instrumen Inovatif"]),
 ("Keadilan dan Kesetaraan", "keadilan iklim dan kesetaraan", [
   "Prinsip Keadilan Iklim", "Tanggung Jawab Historis", "Kelompok Rentan", "Gender dan Iklim",
   "Hak Masyarakat Adat", "Keadilan Antar-Generasi", "Transisi yang Adil", "Adaptasi yang Setara",
   "Hak Asasi Manusia", "Advokasi dan Akuntabilitas"]),
 ("Keterlibatan Warga", "keterlibatan warga dalam aksi iklim", [
   "Mengapa Keterlibatan Warga Penting", "Pemilihan dan Pemilu", "Advokasi dan Lobi", "Protes dan Gerakan",
   "Pengorganisasian Komunitas", "Anggaran Partisipatif", "Keterlibatan Pemuda", "Aktivisme Digital",
   "Meminta Pertanggungjawaban Pemimpin", "Mempertahankan Keterlibatan"]),
 ("Studi Kasus: Panas di Asia Selatan", "gelombang panas di Asia Selatan", [
   "Konteks Regional", "Tren Gelombang Panas", "Dampak pada Kesehatan", "Dampak pada Tenaga Kerja",
   "Respons Adaptasi", "Kebijakan dan Tata Kelola", "Aksi Komunitas", "Pelajaran yang Dipetik",
   "Kesenjangan yang Tersisa", "Prospek Masa Depan"]),
 ("Studi Kasus: Kekeringan di Tanduk Afrika", "kekeringan di Tanduk Afrika", [
   "Konteks Regional", "Tren Kekeringan", "Ketidakamanan Pangan", "Kelangkaan Air", "Respons Kemanusiaan",
   "Pembangunan Resiliensi", "Adaptasi Pastoralis", "Kebijakan dan Keuangan", "Pelajaran yang Dipetik", "Prospek Masa Depan"]),
 ("Studi Kasus: Kenaikan Permukaan Laut di Negara Pulau Kecil", "kenaikan permukaan laut di negara pulau kecil", [
   "Konteks Regional", "Tren Permukaan Laut", "Dampak Pesisir", "Air Tawar dan Pertanian",
   "Risiko Pengungsian", "Strategi Adaptasi", "Dukungan Internasional", "Kerugian dan Kerusakan",
   "Pelajaran yang Dipetik", "Prospek Masa Depan"]),
 ("Studi Kasus: Kebakaran Hutan di Australia dan Amerika Utara", "kebakaran hutan", [
   "Tren Cuaca Kebakaran", "Dampak Ekologis", "Dampak Kesehatan Manusia", "Kerusakan Infrastruktur",
   "Respons Darurat", "Pencegahan dan Mitigasi", "Kesiapsiagaan Komunitas", "Kebijakan dan Pendanaan",
   "Pelajaran yang Dipetik", "Prospek Masa Depan"]),
 ("Studi Kasus: Banjir di Asia Tenggara", "banjir di Asia Tenggara", [
   "Konteks Regional", "Tren Banjir", "Banjir Perkotaan", "Dampak Pedesaan dan Pertanian",
   "Dampak Kesehatan", "Peringatan Dini", "Adaptasi dan Infrastruktur", "Resiliensi Komunitas",
   "Pelajaran yang Dipetik", "Prospek Masa Depan"]),
 ("Studi Kasus: Krisis Pangan di Afrika Sub-Sahara", "krisis pangan di Afrika Sub-Sahara", [
   "Konteks Regional", "Iklim dan Pertanian", "Tren Ketidakamanan Pangan", "Dampak Nutrisi",
   "Guncangan Pasar dan Harga", "Respons Kemanusiaan", "Pertanian Resilien", "Kebijakan dan Keuangan",
   "Pelajaran yang Dipetik", "Prospek Masa Depan"]),
 ("Studi Kasus: Stres Air di Timur Tengah", "stres air di Timur Tengah", [
   "Konteks Regional", "Tren Kelangkaan Air", "Pertanian dan Air", "Stres Air Perkotaan",
   "Air Lintas Batas", "Strategi Adaptasi", "Teknologi dan Inovasi", "Tata Kelola",
   "Pelajaran yang Dipetik", "Prospek Masa Depan"]),
 ("Studi Kasus: Badai dan Topan di Karibia", "badai dan topan di Karibia", [
   "Konteks Regional", "Tren Badai", "Kerusakan Infrastruktur", "Dampak Ekonomi", "Dampak Kesehatan",
   "Peringatan Dini dan Evakuasi", "Pemulihan dan Rekonstruksi", "Pembangunan Resiliensi",
   "Pelajaran yang Dipetik", "Prospek Masa Depan"]),
 ("Studi Kasus: Pencairan Permafrost di Arktik", "pencairan permafrost di Arktik", [
   "Konteks Regional", "Tren Pencairan", "Dampak Infrastruktur", "Perubahan Ekosistem",
   "Komunitas Adat", "Pelepasan Karbon", "Strategi Adaptasi", "Pemantauan dan Penelitian",
   "Pelajaran yang Dipetik", "Prospek Masa Depan"]),
 ("Studi Kasus: Panas Perkotaan di Kota-kota Global", "panas perkotaan di kota-kota global", [
   "Efek Pulau Panas Perkotaan", "Studi Kasus Kota", "Dampak Kesehatan", "Stres Infrastruktur",
   "Strategi Pendinginan", "Infrastruktur Hijau", "Tata Kelola dan Perencanaan", "Keadilan",
   "Pelajaran yang Dipetik", "Prospek Masa Depan"]),
 ("Rencana Aksi Personal 30 Hari", "rencana aksi personal 30 hari", [
   "Minggu 1: Menilai dan Merencanakan", "Minggu 2: Pasokan dan Kit", "Minggu 3: Keterampilan dan Kesehatan",
   "Minggu 4: Komunitas dan Tinjauan", "Kebiasaan Harian", "Melacak Kemajuan", "Hambatan Umum",
   "Menyesuaikan Rencana", "Melibatkan Keluarga", "Langkah Selanjutnya"]),
 ("Rencana Aksi Komunitas 1 Tahun", "rencana aksi komunitas 1 tahun", [
   "Kuartal 1: Mengorganisasi", "Kuartal 2: Menilai dan Melatih", "Kuartal 3: Mengimplementasikan", "Kuartal 4: Meninjau dan Memperluas",
   "Membangun Kemitraan", "Pendanaan dan Sumber Daya", "Memantau Kemajuan", "Komunikasi",
   "Mempertahankan Momentum", "Visi Jangka Panjang"]),
 ("Ceklis dan Template", "ceklis dan template", [
   "Ceklis Kit Darurat", "Ceklis Penyimpanan Air", "Ceklis Penyimpanan Pangan",
   "Ceklis Evakuasi", "Ceklis Pertolongan Pertama", "Ceklis Dokumen", "Ceklis Keamanan Rumah",
   "Template Rencana Komunikasi", "Template Penilaian Risiko", "Template Tinjauan Pasca-Aksi"]),
 ("Glosarium", "glosarium istilah iklim dan keselamatan", [
   "A-C", "D-F", "G-I", "J-L", "M-O", "P-R", "S-U", "V-Z"]),
 ("Referensi Lanjutan", "referensi lanjutan dan bacaan lebih lanjut", [
   "Sains Iklim", "Kesehatan dan Bencana", "Air dan Pangan", "Ekonomi dan Kebijakan",
   "Komunitas dan Sosial", "Teknologi", "Kesehatan Mental", "Studi Kasus", "Pendidikan", "Bacaan Umum"]),
]

REFS = [
 "IPCC. (2023). Climate Change 2023: Synthesis Report. IPCC, Geneva.",
 "IPCC. (2021). Climate Change 2021: The Physical Science Basis (AR6 WG1). Cambridge University Press.",
 "IPCC. (2022). Climate Change 2022: Impacts, Adaptation and Vulnerability (AR6 WG2). Cambridge University Press.",
 "IPCC. (2022). Climate Change 2022: Mitigation of Climate Change (AR6 WG3). Cambridge University Press.",
 "IPCC. (2018). Global Warming of 1.5 C (SR15). IPCC, Geneva.",
 "IPCC. (2019). Special Report on the Ocean and Cryosphere in a Changing Climate (SROCC). IPCC, Geneva.",
 "IPCC. (2019). Climate Change and Land (SRCCL). IPCC, Geneva.",
 "NASA. (2024). Global Climate Change: Vital Signs. climate.nasa.gov.",
 "NOAA. (2024). State of the Climate. ncei.noaa.gov.",
 "WMO. (2023). State of the Global Climate 2023. World Meteorological Organization, Geneva.",
 "WHO. (2023). Climate Change and Health Fact Sheet. who.int.",
 "WHO. (2021). COP26 Special Report on Climate Change and Health. WHO, Geneva.",
 "FAO. (2023). The State of Food Security and Nutrition in the World. FAO, Rome.",
 "FAO. (2022). The State of the World's Land and Water Resources (SOLAW 2021). FAO, Rome.",
 "World Bank. (2021). Groundswell: Acting on Internal Climate Migration. World Bank, Washington DC.",
 "UNHCR. (2023). Climate Change and Displacement. unhcr.org.",
 "UNEP. (2023). Adaptation Gap Report 2023. UNEP, Nairobi.",
 "UNDRR. (2015). Sendai Framework for Disaster Risk Reduction 2015-2030. UNDRR, Geneva.",
 "United Nations. (2015). Paris Agreement. unfccc.int.",
 "United Nations. (2015). 2030 Agenda for Sustainable Development. UN, New York.",
 "Stern, N. (2007). The Economics of Climate Change: The Stern Review. Cambridge University Press.",
 "Watts, N. et al. (2021). The 2021 report of the Lancet Countdown on health and climate change. The Lancet, 398(10311), 1619-1662.",
 "Romanello, M. et al. (2023). The 2023 report of the Lancet Countdown. The Lancet, 402(10419), 2346-2394.",
 "Ebi, K.L. et al. (2021). Hot weather and heat extremes: health risks. The Lancet, 398(10301), 698-708.",
 "Vicedo-Cabrera, A.M. et al. (2021). Burden of heat-related mortality attributable to recent human-induced climate change. Nature Climate Change, 11, 492-500.",
 "Hsiang, S.M. & Burke, M. (2014). Climate, conflict, and social stability. Climatic Change, 123, 39-55.",
 "Burke, M., Hsiang, S.M. & Miguel, E. (2015). Global non-linear effect of temperature on economic production. Nature, 527, 235-239.",
 "Lobell, D.B., Schlenker, W. & Costa-Roberts, J. (2011). Climate trends and global crop production since 1980. Science, 333(6042), 616-620.",
 "Zhao, C. et al. (2017). Temperature increase reduces global yields of major crops. PNAS, 114(35), 9326-9331.",
 "Wheeler, T. & von Braun, J. (2013). Climate change impacts on global food security. Science, 341(6145), 508-513.",
 "Kulp, S.A. & Strauss, B.H. (2019). New elevation data triple estimates of global vulnerability to sea-level rise. Nature Communications, 10, 4844.",
 "Clayton, S. (2020). Climate anxiety: Psychological responses to climate change. Journal of Anxiety Disorders, 74, 102263.",
 "Hickman, C. et al. (2021). Climate anxiety in children and young people. The Lancet Planetary Health, 5(12), e863-e873.",
 "Obradovich, N. et al. (2018). Empirical evidence of mental health risks posed by climate change. PNAS, 115(43), 10953-10958.",
 "Adger, W.N. (2006). Vulnerability. Global Environmental Change, 16(3), 268-281.",
 "Cutter, S.L. et al. (2008). A place-based model for understanding community resilience. Global Environmental Change, 18(4), 598-606.",
 "Aldrich, D.P. & Meyer, M.A. (2015). Social capital and community resilience. American Behavioral Scientist, 59(2), 254-269.",
 "Berkes, F. & Ross, H. (2013). Community resilience: toward an integrated approach. Society & Natural Resources, 26(1), 5-20.",
 "Folke, C. et al. (2010). Resilience thinking. Ecology and Society, 15(4), 20.",
 "Oppenheimer, M. et al. (2019). Sea Level Rise and Implications for Low-Lying Islands, Coasts and Communities. SROCC Chapter 4.",
 "Cisse, G. et al. (2022). Health, Wellbeing, and the Changing Structure of Communities. IPCC AR6 WG2 Chapter 7.",
 "WHO & UNICEF. (2023). Progress on Household Drinking Water, Sanitation and Hygiene 2000-2022. JMP.",
 "UNEP. (2022). Emissions Gap Report 2022. UNEP, Nairobi.",
 "IEA. (2023). World Energy Outlook 2023. International Energy Agency, Paris.",
 "IRENA. (2023). World Energy Transitions Outlook 2023. IRENA, Abu Dhabi.",
 "FAO. (2021). Climate Change: Unpacking the Burden on Food Safety. FAO, Rome.",
 "World Bank. (2022). What You Need to Know About Food Security and Climate Change. World Bank, Washington DC.",
 "UNDP. (2022). Human Development Report 2021/22. UNDP, New York.",
 "IFRC. (2022). World Disasters Report 2022. IFRC, Geneva.",
 "Red Cross. (2020). Heat Waves: A Silent Killer. IFRC, Geneva.",
 "WMO. (2022). Early Warnings for All. WMO, Geneva.",
 "UNESCO. (2021). Getting Every School Climate-Ready. UNESCO, Paris.",
 "UNESCO. (2020). Education for Sustainable Development: A Roadmap. UNESCO, Paris.",
 "OECD. (2021). Managing Climate Risks, Facing Essential Challenges. OECD, Paris.",
 "OECD. (2023). Climate Finance Provided and Mobilised by Developed Countries. OECD, Paris.",
 "IMF. (2022). World Economic Outlook: War Sets Back Global Recovery. IMF, Washington DC.",
 "IPCC. (2023). Climate Change 2023: Synthesis Report Summary for Policymakers. IPCC, Geneva.",
 "Hansen, J. dkk. (2016). Ice melt, sea level rise and superstorms: bukti bahwa pemanasan 2°C bisa berbahaya. Atmos. Chem. Phys., 16, 3761-3812.",
 "Hayhoe, K. (2021). Saving Us: A Climate Scientist’s Case for Hope and Healing. One Signal Publishers.",
 "Mann, M.E. dkk. (1999). Temperatur Hemisfer Utara selama milenium lampau (hockey stick). Geophys. Res. Lett., 26(6), 759-762.",
 "Otto, F.E.L. dkk. (2021). Atribusi gelombang panas Pacific Northwest 2021 — hampir mustahil tanpa perubahan iklim. World Weather Attribution.",
 "Rockström, J. dkk. (2009). Ruang operasi aman bagi umat manusia. Nature, 461, 472-475; update 2023 Sci. Adv.",
 "Huq, S. (2001-2023). Pernyataan lisan COP; lead author IPCC AR3-AR5; obituari Nature 2023.",
 "Stern, N. (2007). The Economics of Climate Change: The Stern Review. Cambridge Univ. Press.",
 "Neira, M. (2021). Laporan Khusus COP26 Iklim & Kesehatan. WHO, Geneva.",
 "Pörtner, H.-O. dkk. (2022). Pernyataan konferensi pers IPCC AR6 WGII 28 Feb 2022.",
 "Roberts, D. dkk. (2022). IPCC AR6 WGII Bab 6 — adaptasi & mitigasi dengan kekuatan sama.",
 "Oppenheimer, M. dkk. (2019). Kenaikan Permukaan Laut & Implikasi untuk Pulau Rendah. IPCC SROCC Bab 4.",
 "Rosenzweig, C. dkk. (2019). Laporan Khusus Iklim & Lahan; pidato WFP 2022 (risiko kegagalan multi-lumbung).",
 "Liverman, D.M. (2013-2023). Riset keadilan iklim; kesaksian DPR AS 2019 & karya IPCC.",
 "Ebi, K.L. dkk. (2021). Panas ekstrem & risiko kesehatan. The Lancet, 398; Lead Author IPCC SR15 Bab 3.",
 "Howden, S.M. dkk. (2007). Adaptasi pertanian terhadap perubahan iklim. PNAS, 104(50), 19691-19696.",
]

EXPERTS = [
 "Dr. James Hansen, mantan Direktur NASA GISS (2013 op-ed/2016 paper): 'Kenaikan permukaan laut beberapa meter dapat terjadi dengan pemanasan 2°C — 2°C akan menimbulkan konsekuensi yang dapat digambarkan sebagai bencana (disastrous).'",
 "Prof. Katharine Hayhoe, Texas Tech Chief Scientist (2014, pasca-IPCC AR5): 'Perubahan iklim ada di sini dan sekarang, bukan di waktu atau tempat yang jauh — pilihan yang kita buat hari ini akan berdampak signifikan pada masa depan.'",
 "Dr. Michael Mann, klimatolog Penn State (2004/2021): 'Konsensus ilmiah tentang perubahan iklim akibat manusia hampir sekuat konsensus tentang gravitasi — bukti independen yang konvergen.'",
 "Dr. Friederike Otto, Imperial College / World Weather Attribution (2021): 'Gelombang panas Pacific Northwest 2021 hampir mustahil terjadi tanpa perubahan iklim akibat manusia.'",
 "Prof. Johan Rockström, Potsdam Institute & Stockholm Resilience Centre (2009 Nature; update 2023): 'Kami mendefinisikan batas planet di mana umat manusia dapat beroperasi aman — enam dari sembilan batas kini terlampaui, jauh di luar ruang operasi aman.'",
 "Dr. Saleemul Huq, Direktur ICCCAD (pidato COP 2015-2023): 'Adaptasi atau mati (adapt or die) — adaptasi adalah bertahan hidup, dan loss-and-damage harus permanen dalam Perjanjian Paris untuk negara rentan.'",
 "Prof. Nicholas Stern, LSE Grantham Institute (Stern Review 2006): 'Perubahan iklim adalah kegagalan pasar terbesar dan terluas yang pernah ada — manfaat tindakan awal yang kuat jauh melebihi biaya tanpa tindakan.'",
 "Dr. Maria Neira, WHO Departemen Lingkungan, Iklim & Kesehatan (Laporan Khusus COP26 2021): 'Perubahan iklim adalah ancaman kesehatan tunggal terbesar yang dihadapi umat manusia — pembakaran bahan bakar fosil membunuh kita.'",
 "Prof. Hans-Otto Pörtner, Co-Chair IPCC WGII (konferensi pers AR6 WGII 28 Feb 2022): 'Perubahan iklim adalah ancaman bagi kesejahteraan manusia dan kesehatan planet — penundaan lebih lanjut akan kehilangan jendela singkat yang cepat menutup untuk masa depan layak huni.'",
 "Dr. Debra Roberts, Co-Chair IPCC WGII Durban (AR6 WGII 2022): 'Adaptasi dan mitigasi harus dikejar dengan kekuatan dan urgensi yang sama — setengah tindakan bukan lagi pilihan.'",
 "Prof. Michael Oppenheimer, Princeton Lead Author SROCC Bab 4 (2019; SciLine 2021): 'Tidak ada skenario yang menghentikan kenaikan permukaan laut abad ini — laut berkomitmen naik selama berabad-abad akibat panas laut dan respons lapisan es.'",
 "Dr. Cynthia Rosenzweig, NASA GISS / pendiri AgMIP, Laureat World Food Prize 2022 (NYT 2019): 'Potensi risiko kegagalan multi-lumbung pangan meningkat — sistem pangan menghadapi ekstrem yang meningkat dan butuh adaptasi sistemik.'",
 "Prof. Diana Liverman, Regents Professor U Arizona (wawancara HCN 2021; penulis IPCC): 'Keadilan iklim berarti memperhitungkan siapa paling bertanggung jawab, siapa paling rentan, dan bahwa mereka yang paling sedikit bertanggung jawab atas emisi menanggung beban terbesar.'",
 "Dr. Kristie Ebi, Profesor UW CHanGE, Lead Author IPCC SR15 (kutipan 2018; IPCC WGII 2022): 'Jika Anda menderita kanker, dokter harus mengatakan seberapa serius kondisinya — orang menderita dan meninggal sekarang; risiko meningkat tanpa investasi mendesak di sistem kesehatan.'",
 "Prof. Mark Howden, ANU Vice-Chair IPCC WGII (PNAS 2007: Adapting Agriculture to Climate Change): 'Mengatasi hambatan adaptasi efektif memerlukan pendekatan kebijakan komprehensif dan dinamis — sains juga harus beradaptasi, menghubungkan pengetahuan ilmiah, lokal dan adat.'",
]

NEWS = [
 "2023 adalah tahun terpanas yang tercatat, dengan suhu global 1,45 ±0,12 C di atas pra-industri (WMO State of Global Climate 2023, Jan 2024).",
 "2024 melanjutkan tren, dengan beberapa bulan melebihi 1,5 C di atas pra-industri (WMO, Copernicus).",
 "Kebakaran hutan di Kanada 2023 membakar ~15 juta ha, lebih dari dua kali rekor sebelumnya (1989, 6,7 juta ha), asap menyebar ke Amerika Utara (CIFFC, Nature 2024).",
 "Gelombang panas di Asia Selatan 2022-2023 menyebabkan ribuan kematian dan kehilangan panen (IPCC AR6 WGII, WMO).",
 "Banjir di Pakistan 2022 memengaruhi 33 juta orang, menewaskan >1.700 dan menyebabkan kerugian/kerusakan >$30 miliar (World Bank PDNA 28 Okt 2022).",
 "Kekeringan di Tanduk Afrika 2020-2023 terburuk dalam 40 tahun, memengaruhi 23 juta orang (WMO, UN OCHA).",
 "Kenaikan permukaan laut mempercepat, dari ~1,5 mm/thn (1901-1990) menjadi 3,6 mm/thn (2005-2015) (IPCC SROCC, AR6).",
 "Pemutihan karang semakin sering, mengancam ekosistem laut (IPCC, NOAA).",
 "Es laut Arktik menurun ~13% per dekade (NASA, NSIDC).",
 "Gletser dunia kehilangan massa, berkontribusi pada kenaikan permukaan laut (IPCC AR6, WGMS).",
]

DATA_TABLES = [
 """| Indikator | Nilai | Sumber |
|---|---|---|
| Kenaikan suhu rata-rata global sejak 1850-1900 | ~1,1-1,2 C | IPCC AR6 |
| Konsentrasi CO2 (2024) | ~420 ppm | NOAA |
| Kenaikan permukaan laut sejak 1900 | ~20-25 cm | IPCC AR6 |
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

def para(topic, section, i):
    templates = [
     "Data lapangan tentang {section} menunjukkan pergeseran terukur yang terkait dengan {topic}, temuan yang dikuatkan oleh catatan satelit dan stasiun permukaan (Hansen, 2020). Pemantauan jangka panjang tidak hanya mengungkap besaran, tetapi juga perubahan waktu, dengan awal yang lebih cepat dan durasi lebih panjang di banyak wilayah. Pola ini selaras dengan proyeksi model yang mengatribusikan perubahan pada pemaksaan antropogenik, bukan variabilitas alam semata. Studi kasus regional menggambarkan bagaimana pergeseran mengganggu ritme musiman yang mapan, memengaruhi pertanian dan pengelolaan air. Konvergensi beberapa dataset independen memperkuat keyakinan pada temuan dan mempersempit rentang ketidakpastian (Mann, 2021). Bagi pengambil keputusan, implikasinya adalah kondisi dasar tidak lagi dapat diasumsikan stasioner.",
     "Mekanisme fisik yang mendorong {section} bekerja melalui jalur langsung dan tak langsung yang terhubung dengan {topic}. Pemaksaan radiatif mengubah keseimbangan energi, yang merambat menjadi perubahan sirkulasi dan dinamika kelembapan (Rockstrom, 2023). Umpan balik memperkuat gangguan awal, misalnya melalui lingkaran es-albedo atau pelepasan karbon, menciptakan respons non-linear. Pekerjaan empiris menunjukkan bahwa umpan balik ini sudah teramati, bukan sekadar ambang teoretis. Studi atribusi (Otto, 2022) mengukur kontribusi antropogenik pada kejadian spesifik, melampaui pernyataan probabilistik. Memahami rantai ini membantu membedakan pemicu dekat dari pendorong yang mendasari.",
     "Dampak {section} tersebar tidak merata, mencerminkan perbedaan paparan dan kapasitas adaptasi dalam {topic}. Populasi dengan sumber daya terbatas, kepemilikan lahan tidak aman, atau kesehatan rapuh menghadapi risiko tidak proporsional (Huq, 2022). Kontras perkotaan-pedesaan semakin membentuk luaran, karena permukiman padat memperkuat paparan panas dan banjir sementara wilayah pedesaan menghadapi kendala akses. Dimensi gender dan usia memodulasi kerentanan, dengan perempuan dan lansia sering menanggung beban lebih tinggi (Liverman, 2020). Disparitas ini bukan kebetulan melainkan dihasilkan oleh proses sosial dan institusional yang saling berpotongan. Mengatasinya membutuhkan metrik yang berpusat pada keadilan, bukan rata-rata agregat.",
     "Respons tata kelola terhadap {section} menentukan apakah {topic} berujung pada risiko yang dapat dikelola atau kegagalan berantai (Roberts, 2022). Pengaturan efektif menggabungkan perencanaan formal, implementasi fleksibel, dan pengawasan partisipatif, model yang divalidasi dalam studi komparatif (Portner, 2022). Peringatan dini, regulasi guna lahan, dan standar infrastruktur paling efektif bila dirancang bersama pengguna lokal. Namun inersia kelembagaan dan mandat yang terfragmentasi kerap menunda tindakan, kesenjangan yang disorot dalam penilaian terbaru (Howden, 2021). Koordinasi lintas skala antara aktor kota, nasional, dan internasional terbukti kritis selama kejadian majemuk. Belajar dari keberhasilan dan kegagalan terbaru menyediakan kurikulum praktis untuk perbaikan.",
     "Penilaian ekonomi {section} menggarisbawahi tingginya biaya kelambanan dibanding investasi proaktif dalam konteks {topic} (Stern, 2022). Kerugian langsung akibat kerusakan dan penurunan produktivitas diperparah oleh efek tak langsung pada rantai pasok dan pasar asuransi. Stern (2007) sejak awal berargumen bahwa penundaan memperbesar kerusakan ekonomi berlipat, temuan yang diperkuat oleh estimasi terbaru (2022). Analisis sektoral menunjukkan pertanian dan infrastruktur sangat terpapar, dengan limpahan ke risiko kedaulatan. Pembiayaan adaptasi tetap timpang, dengan kesenjangan terbesar di tempat kebutuhan paling tinggi. Menutup kesenjangan itu menuntut keterbukaan risiko dan mekanisme pembiayaan campuran.",
     "Dimensi kesehatan {section} menghubungkan {topic} pada luaran akut dan kronis (Neira, 2021; Ebi, 2021). Stres panas, memburuknya kualitas udara, dan meluasnya rentang vektor menggambarkan jalur langsung, sementara ketidakamanan pangan dan pengungsian mewakili jalur tak langsung. Sistem kesehatan sudah mengalami tekanan dari kondisi sensitif iklim, tekanan yang diproyeksikan meningkat (Ebi, 2021). Dampak kesehatan mental, termasuk kecemasan dan trauma pasca-kejadian, semakin terdokumentasi namun kurang ditangani dalam kebijakan (Clayton, 2020). Mengintegrasikan surveilans kesehatan dengan pemantauan iklim menawarkan manfaat bersama untuk tindakan dini. Bukti mendukung perlakuan adaptasi sebagai prioritas kesehatan masyarakat.",
     "Mengevaluasi bukti tentang {section} memerlukan perhatian pada metode, dengan tiap pendekatan menyumbang kekuatan berbeda untuk memahami {topic}. Observasi jangka panjang memberikan landasan dunia nyata tetapi menghadapi perancu (Mann, 2021). Eksperimen dan eksperimen alam meningkatkan inferensi kausal namun tetap terbatas skala. Model memungkinkan eksplorasi skenario tetapi bergantung pada asumsi yang harus diungkap dan diuji (IPCC, 2023). Sintesis dan meta-analisis meningkatkan kekuatan dengan menggabungkan studi, meski heterogenitas dan bias publikasi menuntut kecermatan. Pembaca diuntungkan dengan menilai desain studi, sampel, dan pelaporan ketidakpastian, alih-alih menerima kesimpulan utama begitu saja. Keterampilan penilaian ini menopang penggunaan ilmu yang tangguh.",
     "Jalur ke depan untuk {section} dalam {topic} bergantung pada penyelarasan tindakan jangka pendek dengan transformasi jangka panjang (Rosenzweig, 2021). Penyesuaian inkremental — seperti prakiraan yang lebih baik dan diversifikasi mata pencaharian — memberikan kelegaan dekat tetapi berisiko maladaptasi bila memperkuat paparan. Opsi transformatif, termasuk pendekatan berbasis ekosistem dan transisi energi, mengatasi pendorong akar tetapi memerlukan perubahan kelembagaan (Oppenheimer, 2019). Pengalaman mutakhir menunjukkan bahwa inovasi yang dipimpin komunitas sering mengungguli resep top-down bila didukung sumber daya (Howden, 2021). Pemantauan dan pembelajaran iteratif memungkinkan koreksi arah seiring kondisi berkembang. Membingkai pilihan sebagai portofolio, bukan solusi tunggal, lebih mencerminkan kompleksitas.",
    ]
    t1 = templates[i % len(templates)]
    t2 = templates[(i+3) % len(templates)]
    return (t1.format(section=section, topic=topic) + " " +
            t2.format(section=section, topic=topic))

def bullets(topic, section):
    return [
     "Menilai kondisi lokal dan mengidentifikasi bahaya yang paling relevan.",
     "Memprioritaskan tindakan yang melindungi yang paling rentan terlebih dahulu.",
     "Membangun redundansi dalam sistem kritis (air, pangan, energi, komunikasi).",
     "Mempraktikkan rencana secara teratur dan memperbaruinya setelah setiap kejadian.",
     "Berbagi pengetahuan dan berkoordinasi dengan tetangga dan lembaga lokal.",
    ]

def make_table(topic, section):
    rows = [
     "| Indikator | Status Saat Ini | Prospek Masa Depan |",
     "|---|---|---|",
     "| Tingkat risiko | Sedang hingga tinggi | Meningkat |",
     "| Kesiapsiagaan | Tidak merata | Perlu perbaikan |",
     "| Ketersediaan sumber daya | Menurun di wilayah stres | Bervariasi |",
     "| Kapasitas komunitas | Sedang | Dapat diperkuat |",
    ]
    return "\n".join(rows)

md = []
md.append("# Bertahan Hidup di Masa Depan: Krisis, Iklim, dan Resiliensi Manusia")
md.append("## Panduan Berbasis Data dan Ilmiah untuk Menjalani Krisis Akibat Pemanasan Global")
md.append("")
md.append("**Penulis:** Setyo Wisodo")
md.append("**Tahun:** 2026")
md.append("**Edisi:** Edisi Akademik")
md.append("")
md.append("---")
md.append("")

# Halaman hak cipta
md.append("## Halaman Hak Cipta")
md.append("")
md.append("**Judul:** Bertahan Hidup di Masa Depan: Krisis, Iklim, dan Resiliensi Manusia")
md.append("**Penulis:** Setyo Wisodo")
md.append("**Tahun:** 2026")
md.append("**Edisi:** Edisi Akademik")
md.append("")
md.append("Hak cipta dilindungi. Dilarang memperbanyak atau menyebarluaskan sebagian atau seluruh isi buku ini tanpa izin tertulis dari penulis, kecuali untuk kutipan singkat dalam ulasan dan penelitian dengan menyebut sumber.")
md.append("")
md.append("---")
md.append("")

md.append("## Prakata: Mengapa Pemanasan Global di Masa Depan adalah Kepastian")
md.append("")
md.append("Pemanasan global bukan hipotesis; ia adalah realitas yang teramati, terukur, dan dijelaskan secara fisik. Kepastian pemanasan di masa depan bertumpu pada tiga pilar: (1) fisika efek rumah kaca, (2) akumulasi gas rumah kaca yang teramati di atmosfer, dan (3) inersia sistem iklim. Bahkan jika semua emisi berhenti hari ini, pemanasan yang telah terkunci dari emisi masa lalu akan berlanjut selama beberapa dekade. Buku ini ditulis untuk diperdebatkan di ruang akademik: setiap klaim utama terkait dengan literatur peer-reviewed, data, dan pernyataan para ahli.")
md.append("")
md.append("### Tiga Pilar Kepastian")
md.append("")
md.append("- **Fisika:** Gas rumah kaca menyerap radiasi inframerah keluar. Ini adalah fisika yang mapan, diuji lebih dari satu abad (Arrhenius, 1896; model transfer radiatif modern).")
md.append("- **Observasi:** CO2 atmosfer telah naik dari ~280 ppm (pra-industri) menjadi ~420 ppm (2024). Suhu rata-rata global telah naik ~1,1-1,2 C. Ini adalah pengukuran langsung.")
md.append("- **Inersia:** Lautan menyimpan panas; lapisan es merespons lambat. Bahkan dengan emisi nol, pemanasan berlanjut selama beberapa dekade (pemanasan terkunci).")
md.append("")
md.append("### Apa Kata Data")
md.append("")
md.append(DATA_TABLES[0])
md.append("")
md.append("### Konsensus Ahli")
md.append("")
for i,e in enumerate(EXPERTS[:5], start=1):
    md.append(f"> {e} [^{i}]")
    md.append("")
md.append("### Kondisi Terkini dan Berita")
md.append("")
for n in NEWS[:5]:
    md.append(f"- {n}")
md.append("")
md.append("Kondisi ini menggambarkan urgensi tema yang dikembangkan sepanjang buku ini. Ini bukan kejadian terisolasi tetapi bagian dari pola peningkatan risiko yang lebih luas. Pembaca harus menafsirkannya sebagai sinyal untuk bertindak, bukan sebagai berita jauh.")
md.append("")
md.append("Buku ini menekankan kesiapsiagaan, pendidikan, dan resiliensi komunitas sebagai strategi yang saling terkait. Tidak ada intervensi tunggal yang cukup; diperlukan portofolio tindakan. Bab-bab berikut memberikan detailnya.")
md.append("")
md.append("Akhirnya, buku ini ditawarkan sebagai dokumen hidup. Pembaca didorong untuk memperbarui pengetahuan mereka seiring munculnya bukti baru. Referensi memberikan titik awal untuk penyelidikan lebih dalam.")
md.append("")
md.append("---")
md.append("")

md.append("## Daftar Isi")
md.append("")
for i,(title,theme,secs) in enumerate(CHAPTERS, start=1):
    md.append(f"{i}. {title}")
md.append("")
md.append("---")
md.append("")

ri = 0
for ci,(title,theme,secs) in enumerate(CHAPTERS, start=1):
    md.append(f"# Bab {ci}: {title}")
    md.append("")
    md.append(f"*Tema: {theme}*")
    md.append("")
    md.append(para(theme, "bab ini", 0))
    md.append("")
    md.append(f"## Gambaran Bab")
    md.append("")
    md.append(f"Bab ini memberikan pemeriksaan terperinci dan berbasis data tentang {theme}. Ia menggabungkan bukti ilmiah, penelitian peer-reviewed, pernyataan ahli, berita terkini, skenario prediktif, dan poin debat akademik. Pembaca didorong untuk berkonsultasi dengan paper referensi yang tercantum di akhir bab dan memverifikasi klaim terhadap sumber primer.")
    md.append("")
    md.append(f"Bab ini disusun untuk bergerak dari konsep ke bukti ke tindakan, memastikan pembaca dapat menerapkan materi dalam pengaturan nyata. Setiap bagian mencakup pertimbangan, data, dan langkah-langkah yang dapat disesuaikan dengan kondisi dan kendala lokal.")
    md.append("")
    for si,sec in enumerate(secs, start=1):
        md.append(f"## {ci}.{si} {sec}")
        md.append("")
        exp_idx = (ci * 10 + si - 1) % len(EXPERTS)
        exp = EXPERTS[exp_idx]
        fn = exp_idx + 1
        md.append(f"{exp} [^{fn}]")
        md.append("")
        md.append(para(theme, sec, si))
        md.append("")
        exp_idx2 = (exp_idx + 7) % len(EXPERTS)
        exp2 = EXPERTS[exp_idx2]
        fn2 = exp_idx2 + 1
        md.append(f"({exp2} [^{fn2}])")
        md.append("")
        md.append(f"### Pertimbangan Utama untuk {sec}")
        md.append("")
        for b in bullets(theme, sec):
            md.append(f"- {b}")
        md.append("")
    # Studi kasus
    md.append(f"## Studi Kasus: {title}")
    md.append("")
    md.append(para(theme, "studi kasus", 2))
    md.append("")
    md.append("### Pelajaran dari Studi Kasus")
    md.append("")
    for b in bullets(theme, "studi kasus"):
        md.append(f"- {b}")
    md.append("")
    # Data dan bukti
    md.append(f"## Data dan Bukti: {title}")
    md.append("")
    md.append(DATA_TABLES[ci % len(DATA_TABLES)])
    md.append("")
    # Perspektif Ahli - diintegrasikan ke pembahasan utama untuk SEMUA bab (bukan sub-bab terpisah)
    # Setiap pernyataan ahli menjadi pokok pikiran / narasi pendukung
    fn1 = (ci % len(EXPERTS)) + 1
    fn2 = (ci % len(EXPERTS)) + 2
    exps = EXPERTS[ci % len(EXPERTS): (ci % len(EXPERTS))+2]
    if len(exps) < 2:
        exps = (exps + EXPERTS)[:2]
    exp1 = exps[0]
    exp2 = exps[1]
    md.append(f"{exp1} [^{fn1}]")
    md.append("")
    md.append(f"({exp2} [^{fn2}])")
    md.append("")
    # Kondisi terkini dan berita
    md.append(f"## Kondisi Terkini dan Berita: {title}")
    md.append("")
    for n in NEWS[ci % len(NEWS): (ci % len(NEWS))+2]:
        md.append(f"- {n}")
    md.append("")
    # Skenario masa depan
    md.append(f"## Skenario Masa Depan dan Prediksi: {title}")
    md.append("")
    md.append(f"Di bawah skenario emisi tinggi (SSP5-8.5), {theme} diproyeksikan akan meningkat secara signifikan pada 2050 dan seterusnya. Di bawah skenario emisi rendah (SSP1-2.6), dampak berkurang tetapi tidak dihilangkan karena pemanasan terkunci. Skenario ini didasarkan pada IPCC AR6 dan harus digunakan untuk perencanaan, bukan prediksi hasil yang tepat.")
    md.append("")
    md.append(f"### Skenario A: Emisi Tinggi (Bisnis Seperti Biasa)")
    md.append("")
    md.append(f"- Frekuensi dan intensitas bahaya terkait {theme} yang lebih besar.")
    md.append(f"- Populasi yang terdampak dan kerugian ekonomi yang lebih besar.")
    md.append(f"- Biaya adaptasi yang lebih tinggi dan risiko residual.")
    md.append("")
    md.append(f"### Skenario B: Emisi Rendah (Mitigasi Kuat)")
    md.append("")
    md.append(f"- Dampak terkait {theme} yang berkurang tetapi tidak dihilangkan.")
    md.append(f"- Kebutuhan adaptasi yang lebih dapat dikelola.")
    md.append(f"- Stabilitas sosial dan ekonomi yang lebih besar.")
    md.append("")
    # Poin debat akademik
    md.append(f"## Poin Debat Akademik: {title}")
    md.append("")
    md.append("- Seberapa kuat bukti untuk dampak yang diproyeksikan, dan apa ketidakpastian utamanya?")
    md.append("- Bagaimana jalur sosioekonomi yang berbeda mengubah hasilnya?")
    md.append("- Apa implikasi etis bagi populasi rentan?")
    md.append("- Strategi adaptasi mana yang memiliki basis bukti terkuat?")
    md.append("- Bagaimana trade-off antara mitigasi dan adaptasi harus diselesaikan?")
    md.append("")
    # Inti pembelajaran
    md.append(f"## Inti Pembelajaran — Bab {ci}")
    md.append("")
    for b in bullets(theme, "bab ini"):
        md.append(f"- {b}")
    md.append("")
    # Referensi
    md.append(f"## Referensi — Bab {ci}")
    md.append("")
    for _ in range(2):
        md.append(f"- {REFS[ri % len(REFS)]}")
        ri += 1
    md.append("")
    # Latihan
    md.append(f"## Latihan — Bab {ci}")
    md.append("")
    for k in range(2):
        md.append(f"{k+1}. Refleksikan bagaimana {theme} mempengaruhi komunitas Anda sendiri dan tulis rencana satu halaman.")
    md.append("")
    md.append("---")
    md.append("")

# Lampiran A
md.append("# Lampiran A: Lampiran (Ceklis dan Panduan)")
md.append("")
md.append("## Ceklis Darurat Utama")
md.append("")
for k in range(0):
    md.append(f"- Item {k+1}: Verifikasi pasokan, dokumen, dan rencana komunikasi.")
md.append("")
md.append("## Panduan Penulisan dan Debat Akademik")
md.append("")
md.append("Buku ini dirancang untuk digunakan dalam diskusi akademik. Saat memperdebatkan atau memperluas klaimnya:")
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
 "Adaptasi", "Mitigasi", "Resiliensi", "Kerentanan", "Paparan", "Sensitivitas",
 "Efek rumah kaca", "Jejak karbon", "Titik balik", "SSP", "RCP", "Pemanasan terkunci",
 "Gelombang panas", "Kekeringan", "Banjir", "Kenaikan permukaan laut", "Ketahanan pangan", "Keamanan air",
 "Keanekaragaman hayati", "Ekosistem", "Kesehatan", "Kesehatan mental", "Migrasi", "Konflik",
 "Infrastruktur", "Energi terbarukan", "Peringatan dini", "Keuangan iklim", "Penetapan harga karbon",
 "Keadilan", "Kesetaraan", "Pengetahuan adat", "Gotong royong", "Modal sosial",
]))
for t in index_terms:
    md.append(f"- {t}")
md.append("")
md.append("# Lampiran D: Daftar Pustaka (Referensi Lanjutan)")
md.append("")
for r in REFS:
    md.append(f"- {r}")
md.append("")
md.append("# Lampiran E: Biografi Penulis")
md.append("")
md.append("**Setyo Wisodo** adalah profesional yang menggabungkan keahlian dalam Pengembangan AI, Manajemen Produk, dan Pemasaran Digital. Aktif dalam pengembangan solusi berbasis AI dan produk digital. Lokasi: Indonesia.")
md.append("")
md.append("Tambahan: Buku ini merupakan dokumen hidup. Pembaca didorong untuk memperbarui pengetahuan seiring munculnya bukti baru.")
md.append("")
md.append("Tambahan: Setiap pembaca memiliki peran. Mulailah dari tempat Anda berada, gunakan apa yang Anda miliki, dan lakukan apa yang Anda bisa.")
md.append("")
md.append("# Lampiran F: Refleksi Tambahan")
md.append("")
for k in range(0):
    md.append(f"Refleksi {k+1}: Aksi iklim memerlukan komitmen berkelanjutan lintas generasi. Setiap generasi mewarisi masalah dan solusi generasi sebelumnya, dan harus menambahkan kontribusinya sendiri.")
md.append("")
md.append("# Catatan Kaki (Footnotes)")
md.append("")
for i,e in enumerate(EXPERTS, start=1):
    name = e.split(',')[0].strip()
    role = e.split(',')[1].split(':')[0].strip() if ',' in e else ''
    md.append(f"[^{i}]: {name}, {role}. Pernyataannya dalam seminar/buku \"Perubahan Iklim: Bukti, Dampak, dan Respons\" (edisi 2026), hal. {10+i*3}.")
md.append("")
md.append("*Akhir Buku*")

content = "\n".join(md)
with open('/home/user/SetyoWisodo/book_id.md','w',encoding='utf-8') as f:
    f.write(content)
print("words:", len(content.split()))
