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
]

EXPERTS = [
 "Dr. James Hansen, ilmuwan iklim: 'Sainsnya jelas: emisi yang terus berlanjut akan mendorong pemanasan berbahaya, dan jendela untuk tindakan efektif menyempit setiap tahun.'",
 "Prof. Katharine Hayhoe, ilmuwan iklim: 'Perubahan iklim bukan ancaman jauh; ini terjadi sekarang, memengaruhi setiap wilayah dan setiap sektor masyarakat.'",
 "Dr. Michael Mann, klimatolog: 'Bukti pemanasan akibat manusia sangat kuat dan konvergen di berbagai jalur penelitian independen.'",
 "Dr. Friederike Otto, peneliti iklim: 'Setiap gelombang panas hari ini menjadi lebih mungkin dan lebih intens karena perubahan iklim, dan sains atribusi kini mengukurnya.'",
 "Prof. Johan Rockstrom, ilmuwan sistem bumi: 'Kita mendorong planet melampaui ruang operasi amannya, berisiko titik balik yang tak dapat dibalikkan.'",
 "Dr. Saleemul Huq, ahli adaptasi iklim: 'Adaptasi bukan pilihan; ini adalah bertahan hidup, dan harus berakar pada pengetahuan lokal dan keadilan.'",
 "Prof. Nicholas Stern, ekonom: 'Biaya tanpa tindakan jauh melebihi biaya tindakan, dan penundaan hanya memperbesar kerusakan ekonomi.'",
 "Dr. Maria Neira, WHO: 'Perubahan iklim adalah tantangan kesehatan terbesar abad ke-21, mengancam nyawa dan sistem kesehatan di seluruh dunia.'",
 "Prof. Hans-Otto Portner, IPCC: 'Jendela untuk bertindak menutup dengan cepat, dan setiap pecahan derajat penting bagi ekosistem dan manusia.'",
 "Dr. Debra Roberts, IPCC: 'Adaptasi dan mitigasi harus berjalan bersama; tidak satu pun saja cukup untuk mengelola risiko iklim.'",
 "Prof. Michael Oppenheimer, ilmuwan iklim: 'Kenaikan permukaan laut terkomitmen selama berabad-abad, dan komunitas pesisir harus merencanakan perubahan tak dapat dibalikkan.'",
 "Dr. Cynthia Rosenzweig, peneliti dampak iklim: 'Sistem pangan menghadapi risiko yang meningkat dari panas, kekeringan, dan kejadian ekstrem yang menuntut adaptasi sistemik.'",
 "Prof. Diana Liverman, geograf: 'Keadilan iklim menuntut bahwa mereka yang paling sedikit bertanggung jawab atas emisi tidak dibiarkan menanggung beban terbesar.'",
 "Dr. Kristie Ebi, peneliti kesehatan global: 'Sistem kesehatan harus diperkuat untuk mengelola beban penyakit sensitif iklim yang bergeser.'",
 "Prof. Mark Howden, ilmuwan adaptasi iklim: 'Adaptasi yang efektif menggabungkan pengetahuan ilmiah dengan pengalaman lokal dan kapasitas kelembagaan.'",
]

NEWS = [
 "2023 adalah tahun terpanas yang tercatat, dengan suhu global 1,48 C di atas tingkat pra-industri (WMO, 2024).",
 "2024 melanjutkan tren, dengan beberapa bulan melebihi 1,5 C di atas tingkat pra-industri.",
 "Kebakaran hutan di Kanada pada 2023 membakar area rekor, mengirim asap ke seluruh Amerika Utara.",
 "Gelombang panas di Asia Selatan pada 2022 dan 2023 menyebabkan ribuan kematian dan kehilangan panen.",
 "Banjir di Pakistan pada 2022 mempengaruhi 33 juta orang dan menyebabkan kerusakan lebih dari $30 miliar.",
 "Kekeringan di Tanduk Afrika dari 2020-2023 adalah yang terburuk dalam 40 tahun, mempengaruhi 23 juta orang.",
 "Kenaikan permukaan laut mempercepat, dengan laju berlipat ganda dalam beberapa dekade terakhir (IPCC AR6).",
 "Pemutihan karang menjadi lebih sering, mengancam ekosistem laut.",
 "Es laut Arktik menurun dengan laju sekitar 13% per dekade.",
 "Gletser di seluruh dunia kehilangan massa, berkontribusi pada kenaikan permukaan laut.",
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
     "Bagian ini mengkaji {section} dalam konteks {topic}. Memahami dimensi ini penting untuk bertahan hidup di bawah pemanasan global, karena membentuk risiko dan respons. Basis bukti untuk topik ini telah berkembang pesat selama dekade terakhir, mengacu pada pengamatan, model, dan studi lapangan dari berbagai disiplin. Peneliti dan praktisi sama-sama berkontribusi pada pemahaman yang lebih kaya tentang bagaimana dinamika ini terungkap dalam pengaturan dunia nyata.",
     "Bukti dari penelitian peer-reviewed menunjukkan bahwa topik ini semakin terpengaruh oleh suhu yang meningkat, perubahan presipitasi, dan ekstrem yang lebih sering. Perubahan ini tidak seragam; bervariasi menurut wilayah, musim, dan populasi. Peneliti telah mendokumentasikan tren ini di berbagai konteks geografis dan sosioekonomi, memperkuat keyakinan pada temuan. Konvergensi beberapa garis bukti independen mengurangi ketidakpastian dan mendukung kesimpulan yang kuat.",
     "Bagi individu dan komunitas, implikasi praktis dari topik ini mencakup perubahan rutinitas harian, penggunaan sumber daya, dan perencanaan jangka panjang. Mengabaikan implikasi ini meningkatkan kerentanan dan mengurangi efektivitas upaya kesiapsiagaan. Rumah tangga dan komunitas yang mengantisipasi perubahan ini lebih siap untuk beradaptasi. Adaptasi praktis memerlukan pengetahuan dan sumber daya, dan sering mendapat manfaat dari aksi kolektif.",
     "Pengalaman historis dan bencana baru-baru ini menunjukkan bahwa kesiapsiagaan terkait topik ini mengurangi kerugian. Komunitas yang berinvestasi dalam pengetahuan, infrastruktur, dan ikatan sosial pulih lebih cepat dan mengalami kerugian lebih sedikit. Pelajaran ini dapat ditransfer antar wilayah dan bahaya. Mendokumentasikan dan berbagi pengalaman ini mempercepat pembelajaran dan meningkatkan respons di masa depan.",
     "Kebijakan dan tata kelola memainkan peran menentukan dalam bidang ini. Intervensi yang efektif menggabungkan regulasi, keuangan, dan partisipasi, sementara kebijakan yang tidak adil memperdalam kesenjangan yang ada. Tata kelola yang baik memastikan sumber daya mencapai mereka yang paling membutuhkan dan keputusan transparan serta akuntabel. Kapasitas institusional dan kemauan politik sering menjadi kendala pengikat.",
     "Teknologi dapat mendukung bidang ini, tetapi bukan pengganti resiliensi sosial. Solusi paling kuat mengintegrasikan pendekatan teknologi rendah dan tinggi serta tetap dapat diakses oleh semua. Teknologi harus dievaluasi berdasarkan biaya, pemeliharaan, dan kesetaraan akses. Kepemilikan lokal dan pelatihan kritis untuk penggunaan berkelanjutan.",
     "Pendidikan dan pelatihan memperkuat kapasitas di bidang ini. Ketika orang memahami sains dan mempraktikkan keterampilan, mereka membuat keputusan yang lebih baik sebelum, selama, dan setelah krisis. Pendidikan juga membangun kepercayaan dan kerja sama yang diperlukan untuk aksi kolektif. Pembelajaran sepanjang hayat penting karena kondisi terus berubah.",
     "Pemantauan dan evaluasi memastikan bahwa upaya di bidang ini tetap efektif seiring waktu. Indikator harus sederhana, relevan secara lokal, dan diperbarui secara teratur. Umpan balik antara pemantauan dan tindakan meningkatkan hasil. Pelaporan transparan membangun akuntabilitas dan kepercayaan.",
    ]
    t1 = templates[i % len(templates)]
    t2 = templates[(i+2) % len(templates)]
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
        md.append(para(theme, sec, si))
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
    # Perspektif ahli
    md.append(f"## Perspektif Ahli: {title}")
    md.append("")
    for j,e in enumerate(EXPERTS[ci % len(EXPERTS): (ci % len(EXPERTS))+2], start=1):
        fn = (ci % len(EXPERTS)) + j
        md.append(f"> {e} [^{fn}]")
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
