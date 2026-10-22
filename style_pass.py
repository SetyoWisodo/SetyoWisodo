# -*- coding: utf-8 -*-
"""Pemerataan pembuka Skenario Masa Depan dan koreksi angka yang lolos dari Gate 2.

Modul ini bekerja pada teks final (setelah gate1/gate1b) supaya kalimat yang
terpotong menjadi beberapa literal string di modul konten tetap bisa diganti.
Setiap penggantian bersifat idempoten: kalau teks lama tidak ada, tidak apa-apa.
"""
import re

# Pembuka Skenario Masa Depan yang dulu seragam ("The historical record ...").
# Setiap bab mendapat pembuka yang mengikuti subjeknya sendiri.
EN_FS = [
    ("The historical record provides the starting point. Since 1970, global surface temperature",
     "Everything that follows in this book rests on a trend that is already measurable. Since 1970, global surface temperature"),
    ("The historical record shows a clear trend. The number of days with extreme heat",
     "Heat is the hazard whose link to mortality is clearest. The number of days with extreme heat"),
    ("The historical data show a consistent trend. Global water withdrawals",
     "Freshwater is the resource where the gap between demand and supply is closing fastest. Global water withdrawals"),
    ("The historical record is unambiguous. Global mean sea level",
     "The ocean's rise is the slowest number in this book and the hardest to reverse. Global mean sea level"),
    ("The historical evidence is that warming has already reduced yields relative to what they would have been without it. A meta-analysis",
     "The effect of warming on food is no longer hypothetical. A meta-analysis"),
    ("The historical record shows that ecosystems are already changing. The Living Planet Index",
     "The natural world is where the cost of warming first becomes visible. The Living Planet Index"),
    ("The historical data show that the health effects of climate change are already measurable. Heat-related mortality",
     "The health effects of warming are already being counted, not forecast. Heat-related mortality"),
    ("The historical record shows that economic losses from climate-related disasters have increased. The total damage",
     "The bill for climate change is already being paid, and not evenly. The total damage"),
    ("The historical data show that climate shocks already move people. The Internal Displacement Monitoring Centre",
     "Migration is the oldest form of adaptation and the hardest to measure. The Internal Displacement Monitoring Centre"),
    ("The historical record does not show a simple trend of climate-driven war. The number of armed conflicts",
     "War is where climate explanations are most often oversold. The number of armed conflicts"),
    ("The historical record shows that infrastructure failures are increasing. The number of weather-related power outages",
     "Infrastructure fails at the moment it is needed most. The number of weather-related power outages"),
    ("The historical record shows that education has expanded dramatically over the past century: literacy rates",
     "The longest lever in this book is education: literacy rates"),
    ("The historical record shows that misinformation is not new; what is new is its speed and scale. Rumours",
     "A false claim travels faster than a correction, and always has. Rumours"),
    ("The historical record shows a widening gap between the length of disruptions and the length of household supplies. Average outage duration",
     "Preparedness is measured in the gap between how long a disruption lasts and how long a household can manage without help. Average outage duration"),
    ("The historical record shows a clear trend. Heat-related mortality among older adults",
     "The future of heat mortality depends less on temperature than on the response. Heat-related mortality among older adults"),
    ("The historical record shows that governance quality explains much of the variation in disaster mortality. Countries",
     "Disasters do not create governance; they reveal it. Countries"),
    ("The historical record shows a rapid shift. Renewables supplied",
     "The energy transition is the one forecast in this book that has been consistently too pessimistic. Renewables supplied"),
    ("The historical record shows that mental health consequences of disasters are large, persistent and under-measured. Studies",
     "The psychological cost of a disaster outlasts the physical damage. Studies"),
    ("The historical record shows that the gap between responsibility and harm has widened. Cumulative emissions",
     "The distance between who caused the warming and who suffers it is the defining political fact of the century. Cumulative emissions"),
    ("The historical record shows that extreme events are becoming more frequent and more intense. Heatwaves",
     "Extremes are becoming the ordinary condition of cities. Heatwaves"),
    ("The historical record shows that famines have become less frequent but not extinct. The number of people affected by food crises",
     "Famine is no longer mainly a story about food; it is a story about access, conflict and early warning. The number of people affected by food crises"),
    ("The historical record shows that preparedness can reduce disaster mortality dramatically, even when hazards intensify. Bangladesh's cyclone deaths",
     "Preparedness works, and the record shows how much. Bangladesh's cyclone deaths"),
]

ID_FS = [
    ("Rekaman historis memberikan titik awal. Sejak 1970, suhu permukaan global",
     "Semua yang menyusul dalam buku ini bertumpu pada tren yang sudah terukur. Sejak 1970, suhu permukaan global"),
    ("Rekaman historis menunjukkan tren yang jelas. Jumlah hari dengan panas ekstrem",
     "Panas adalah bahaya yang kaitannya dengan kematian paling jelas. Jumlah hari dengan panas ekstrem"),
    ("Data historis menunjukkan tren yang konsisten. Pengambilan air global",
     "Air tawar adalah sumber daya yang jarak antara permintaan dan pasokannya menutup paling cepat. Pengambilan air global"),
    ("Rekaman historis tidak ambigu. Muka laut rata-rata global",
     "Kenaikan muka laut adalah angka paling lambat di buku ini dan yang paling sulit dibalik. Muka laut rata-rata global"),
    ("Bukti historis menunjukkan bahwa pemanasan sudah mengurangi hasil panen relatif terhadap apa yang akan terjadi tanpanya. Meta-analisis",
     "Dampak pemanasan terhadap pangan bukan lagi hipotesis. Meta-analisis"),
    ("Rekaman historis menunjukkan bahwa ekosistem sudah berubah. Living Planet Index",
     "Dunia alami adalah tempat pertama biaya pemanasan menjadi terlihat. Living Planet Index"),
    ("Data historis menunjukkan bahwa efek kesehatan perubahan iklim sudah terukur. Kematian terkait panas",
     "Dampak kesehatan akibat pemanasan sudah dihitung, bukan diramalkan. Kematian terkait panas"),
    ("Rekaman historis menunjukkan bahwa kerugian ekonomi akibat bencana terkait iklim telah meningkat. Total kerusakan",
     "Tagihan perubahan iklim sudah dibayar, dan tidak merata. Total kerusakan"),
    ("Data historis menunjukkan bahwa guncangan iklim sudah memindahkan orang. Pusat Pemantauan",
     "Migrasi adalah adaptasi tertua dan yang paling sulit diukur. Pusat Pemantauan"),
    ("Rekaman historis tidak menunjukkan tren sederhana perang akibat iklim. Jumlah konflik bersenjata",
     "Perang adalah wilayah tempat penjelasan iklim paling sering dibesar-besarkan. Jumlah konflik bersenjata"),
    ("Rekaman historis menunjukkan bahwa kegagalan infrastruktur meningkat. Jumlah pemadaman listrik",
     "Infrastruktur gagal pada saat paling dibutuhkan. Jumlah pemadaman listrik"),
    ("Rekaman historis menunjukkan bahwa pendidikan telah meluas secara dramatis selama satu abad terakhir: tingkat melek huruf",
     "Tuas terpanjang dalam buku ini adalah pendidikan: tingkat melek huruf"),
    ("Rekaman historis menunjukkan bahwa misinformasi bukan hal baru; yang baru adalah kecepatan dan skalanya. Rumor",
     "Klaim palsu bergerak lebih cepat daripada koreksinya, dan selalu begitu. Rumor"),
    ("Rekaman historis menunjukkan jurang yang melebar antara lamanya gangguan dan lamanya persediaan rumah tangga. Durasi pemadaman",
     "Kesiapsiagaan diukur dari selisih antara lamanya gangguan dan lamanya rumah tangga bertahan tanpa bantuan. Durasi pemadaman"),
    ("Rekaman historis menunjukkan tren yang jelas. Kematian terkait panas di antara orang dewasa lanjut usia",
     "Masa depan kematian akibat panas lebih bergantung pada respons daripada pada suhu. Kematian terkait panas di antara orang dewasa lanjut usia"),
    ("Rekaman historis menunjukkan bahwa kualitas tata kelola menjelaskan banyak variasi kematian akibat bencana. Negara",
     "Bencana tidak menciptakan tata kelola; bencana mengungkapnya. Negara"),
    ("Rekaman historis menunjukkan pergeseran yang cepat. Energi terbarukan",
     "Transisi energi adalah satu-satunya ramalan dalam buku ini yang berulang kali terlalu pesimistis. Energi terbarukan"),
    ("Rekaman historis menunjukkan bahwa konsekuensi kesehatan mental bencana besar, persisten, dan kurang terukur. Studi",
     "Biaya psikologis bencana bertahan lebih lama daripada kerusakan fisiknya. Studi"),
    ("Rekaman historis menunjukkan bahwa jurang antara tanggung jawab dan kerugian telah melebar. Emisi kumulatif",
     "Jarak antara pihak yang menyebabkan pemanasan dan pihak yang menanggungnya adalah fakta politik utama abad ini. Emisi kumulatif"),
    ("Rekaman historis menunjukkan bahwa peristiwa ekstrem menjadi lebih sering dan lebih intens. Gelombang panas",
     "Cuaca ekstrem sedang menjadi kondisi biasa kota-kota. Gelombang panas"),
    ("Rekaman historis menunjukkan bahwa kelaparan menjadi lebih jarang tetapi belum punah. Jumlah orang",
     "Kelaparan bukan lagi terutama kisah tentang pangan; ia kisah tentang akses, konflik, dan peringatan dini. Jumlah orang"),
    ("Rekaman historis menunjukkan bahwa kesiapsiagaan dapat menurunkan kematian akibat bencana secara dramatis, bahkan ketika bahaya meningkat. Kematian akibat siklon",
     "Kesiapsiagaan berhasil, dan catatan menunjukkan seberapa besar. Kematian akibat siklon"),
]

# Angka lama yang masih tertinggal di Skenario Masa Depan setelah koreksi Gate 2.
NUM_FIX = {
    "en": [("have increased by about 70 per cent since the 1990s",
            "have increased by 167 per cent since the 1990s"),
           ("has increased by about 70 per cent since the 1990s",
            "has increased by 167 per cent since the 1990s")],
    "id": [("telah meningkat sekitar 70 persen sejak 1990-an",
            "telah meningkat 167 persen sejak 1990-an")],
}


# Kalimat "Two conclusions follow." / "Dua kesimpulan mengikuti." dipakai di
# hampir setiap bab dan terbaca sebagai templat. Varian dirotasi menurut urutan
# kemunculan sehingga tidak ada dua bab berurutan yang memakai kalimat sama.
EN_CONCL = [
    "The evidence supports two conclusions.",
    "Two lessons emerge from this.",
    "There are two consequences here.",
    "Two points deserve emphasis.",
    "The analysis points to two conclusions.",
]
ID_CONCL = [
    "Buktinya mendukung dua kesimpulan.",
    "Dua pelajaran muncul dari sini.",
    "Ada dua konsekuensi di sini.",
    "Dua hal perlu ditekankan.",
    "Analisisnya menunjuk pada dua kesimpulan.",
]


def _concl(text, lang):
    if lang == "en":
        for old, new in (("Two conclusions follow for decisions.",
                          "Two implications matter for decisions."),):
            c = text.count(old)
            if c:
                text = text.replace(old, new)
                return text, c
        base, variants = "Two conclusions follow.", EN_CONCL
    else:
        for old, new in (("Dua kesimpulan mengikuti dari tabel ini.",
                          "Dari tabel ini muncul dua kesimpulan."),
                         ("Dua kesimpulan mengikuti untuk pengambilan keputusan.",
                          "Dua implikasi penting untuk pengambilan keputusan.")):
            c = text.count(old)
            if c:
                text = text.replace(old, new)
                return text, c
        base, variants = "Dua kesimpulan mengikuti.", ID_CONCL
    if base not in text:
        return text, 0
    parts = text.split(base)
    out = [parts[0]]
    n = 0
    for chunk in parts[1:]:
        out.append(variants[n % len(variants)])
        out.append(chunk)
        n += 1
    return "".join(out), n


# "a world that does not will ..." adalah kependekan yang terulang di banyak
# bab. Diganti dengan varian yang menyebut apa yang tidak dilakukan.
EN_WORLD = [
    "a world that delays will",
    "a world that fails to act will",
    "a world that does nothing will",
    "a world that continues on the current path will",
    "a world that responds late will",
    "a world that leaves it to the market will",
]
ID_WORLD = [
    "dunia yang menunda akan",
    "dunia yang gagal bertindak akan",
    "dunia yang membiarkannya akan",
    "dunia yang tetap pada jalur sekarang akan",
    "dunia yang merespons terlambat akan",
    "dunia yang mengutamakan pasar akan",
]


def _world(text, lang):
    base = "a world that does not will" if lang == "en" else "dunia yang tidak akan"
    variants = EN_WORLD if lang == "en" else ID_WORLD
    if base not in text:
        return text, 0
    parts = text.split(base)
    out = [parts[0]]
    n = 0
    for chunk in parts[1:]:
        out.append(variants[n % len(variants)])
        out.append(chunk)
        n += 1
    return "".join(out), n


# "The most important variable remains the pace of ..." diulang di beberapa
# bab. Setiap bab mendapat rumusan yang mengikuti subjeknya.
EN_VAR = [
    ("The most important variable remains the pace of policy and investment, because",
     "What decides the outcome is the pace of policy and investment, because"),
    ("The most important variable remains the pace of climate change, because",
     "How fast the climate changes remains the decisive factor, because"),
    ("The most important variable remains the pace of warming, because",
     "How quickly the warming proceeds remains decisive, because"),
    ("The most important variable, as in other chapters, is the pace of emission reduction, because",
     "As in other chapters, the pace of emission reduction is what counts, because"),
]
ID_VAR = [
    ("Variabel terpenting tetap laju kebijakan dan investasi, karena",
     "Yang menentukan hasilnya adalah laju kebijakan dan investasi, karena"),
    ("Variabel terpenting tetap laju perubahan iklim, karena",
     "Seberapa cepat iklim berubah tetap menjadi faktor penentu, karena"),
    ("Variabel terpenting tetap laju pemanasan, karena",
     "Seberapa cepat pemanasan berlangsung tetap menentukan, karena"),
]


# Paragraf yang dibuka dengan pengulangan klaim paragraf sebelumnya. Lapisan
# pendalaman menambahkan paragraf yang kadang membuka dengan kalimat yang sama
# seperti paragraf di atasnya. Setiap entri menambahkan kalimat kedua sebagai
# jangkar supaya hanya kemunculan yang benar yang diganti.
DEDUP_EN = [
    ("The legal framework for climate migration is fragmented. The 1951 Refugee Convention",
     "The 1951 Refugee Convention"),
    ("State capacity is the most important variable in the climate-conflict relationship. A country with effective institutions",
     "A country with effective institutions"),
    ("Indigenous peoples are disproportionately affected and disproportionately effective as stewards. A large share",
     "A large share"),
    ("Heat is the deadliest climate hazard in most years, and it is the one with the least visible damage. A flood destroys",
     "A flood destroys"),
    ("Flash floods are the deadliest type of flood because they arrive with little warning. They occur when",
     "Flash floods occur when"),
    ("Most climate learning happens outside school, and the quality of that learning is decisive. A museum exhibit",
     "A museum exhibit"),
    ("The most cited global estimate of climate migration comes from the World Bank's Groundswell reports, which projected that 216 million people could move within their own countries by 2050 under a high-emission scenario, concentrated in sub-Saharan Africa, South Asia and Latin America (World Bank, 2021). The figure is a modelling result",
     "The 216 million figure is a modelling result"),
    ("Nutrition is the pathway with the largest long-term consequences and the least visibility. A child who is stunted",
     "A child who is stunted"),
    ("Syria is the case where attribution has been most contested, and the contest is instructive. A severe multi-year drought",
     "A severe multi-year drought"),
    ("The link between drought and food prices runs through expectations as much as through harvests. A poor harvest",
     "A poor harvest"),
    ("Water disputes are more often managed than resolved, and the record is more encouraging than the headlines. Thousands of treaties",
     "Thousands of treaties"),
    ("The pattern of mortality is remarkably consistent across countries. The largest excess",
     "The largest excess"),
    ("Air pollution and climate change share their sources, which makes them a single problem with two accounting systems. Burning fossil fuels",
     "Burning fossil fuels"),
    ("The health case for climate action is often stronger than the environmental case, because it is immediate and local. Phasing out coal",
     "Phasing out coal"),
    ("Children and young people carry a burden that is distinctive because it is anticipatory. Surveys across",
     "Surveys across"),
    ("Drought is defined four ways, and the definitions are not interchangeable. Meteorological drought",
     "Meteorological drought"),
    ("Clean cooking is the least glamorous energy transition and one of the most consequential for health. About 2.3 billion",
     "About 2.3 billion"),
    ("The build-neglect-rebuild cycle is a political economy, not an accident. New construction produces a ribbon",
     "Neglect is not an accident; it is what the incentive structure rewards. New construction produces a ribbon"),
    ("The build-neglect-rebuild cycle is a political economy problem more than an engineering one. A new bridge can be inaugurated",
     "The constraint is political rather than technical. A new bridge can be inaugurated"),
    ("The build-neglect-rebuild cycle is the most expensive pattern in public infrastructure, and it is produced by politics rather than by engineering. A new bridge is a ribbon-cutting",
     "The cost is deferred rather than avoided. A new bridge is a ribbon-cutting"),
    ("The pattern of who dies in a heatwave is remarkably consistent across countries and decades. Risk rises with age, with cardiovascular and renal disease, with living alone, with poor housing and top-floor flats, with lack of air conditioning, and with neighbourhood deprivation.",
     "Each of those factors is a mechanism as well as a marker: age reduces the capacity to sweat, cardiovascular disease reduces the capacity to compensate, living alone removes the person who would have noticed, and a top-floor flat turns a warm night into a lethal one."),
]

DEDUP_ID = [
    ("Banjir bandang adalah jenis banjir paling mematikan karena datang dengan sedikit peringatan. Ia terjadi ketika",
     "Banjir bandang terjadi ketika"),
    ("Kerangka hukum untuk migrasi iklim terfragmentasi. Konvensi Pengungsi 1951",
     "Konvensi Pengungsi 1951"),
    ("Kapasitas negara adalah variabel terpenting dalam hubungan iklim-konflik. Negara dengan institusi efektif",
     "Negara dengan institusi efektif"),
    ("Panas adalah bahaya iklim paling mematikan pada sebagian besar tahun, dan ia bahaya dengan kerusakan paling tidak terlihat. Banjir menghancurkan",
     "Banjir menghancurkan"),
    ("Masyarakat adat terkena secara tidak proporsional dan secara tidak proporsional efektif sebagai pengelola. Sebagian besar hutan",
     "Sebagian besar hutan"),
    ("Sebagian besar pembelajaran iklim terjadi di luar sekolah, dan mutunya menentukan. Pameran museum",
     "Pameran museum"),
    ("Siklus bangun–abaikan–bangun ulang adalah ekonomi politik, bukan kecelakaan. Konstruksi baru menghasilkan",
     "Kecenderungannya bukan kecelakaan; ia yang diberi imbalan oleh sistemnya. Konstruksi baru menghasilkan"),
    ("Kaitan kekeringan dan harga pangan berjalan melalui ekspektasi sama besarnya dengan melalui panen. Panen buruk",
     "Panen buruk"),
    ("Argumen kesehatan untuk aksi iklim sering lebih kuat daripada argumen lingkungan, karena ia segera dan lokal. Menghentikan batu bara",
     "Menghentikan batu bara"),
    ("Kekeringan didefinisikan dengan empat cara, dan definisinya tidak dapat dipertukarkan. Kekeringan meteorologis",
     "Kekeringan meteorologis"),
    ("Kaitan antara harga pangan dan ketidakstabilan politik adalah salah satu jalur yang paling baik terdokumentasi. Lonjakan harga 2007–2008",
     "Lonjakan harga 2007–2008"),
    ("Umpan balik adalah proses yang memperkuat atau meredam suatu perubahan, dan tandanya menentukan apakah iklimnya mengendap atau berlari. Uap air",
     "Uap air"),
    ("Remitansi adalah sumber keuangan eksternal terbesar bagi banyak negara rentan, dan ia berfungsi sebagai bentuk asuransi yang tidak dirancang lembaga mana pun. Rumah tangga yang punya kerabat",
     "Rumah tangga yang punya kerabat"),
    ("Perkiraan global migrasi iklim yang paling banyak dikutip berasal dari laporan Groundswell Bank Dunia, yang memproyeksikan 216 juta orang dapat berpindah di dalam negaranya sendiri pada 2050 dalam skenario emisi tinggi, terkonsentrasi di Afrika sub-Sahara, Asia Selatan dan Amerika Latin. Angka itu adalah hasil pemodelan",
     "Angka 216 juta itu adalah hasil pemodelan"),
    ("Gelombang panas adalah peristiwa korban massal yang datang perlahan, dan kedatangan lambatnya yang membuatnya diremehkan. Gempa menghasilkan",
     "Kedatangan yang lambat itu punya akibat operasional: tidak ada satu momen ketika sistem tahu bahwa ia sedang kewalahan. Gempa menghasilkan"),
]


# Gate 5: absolut yang tidak perlu. Hanya frasa yang membuat klaim empiris
# mutlak; retorika yang memang sengaja hiperbolis ("a false claim travels faster
# than a correction, and always has") dibiarkan.
GATE5_EN = [
    ("are the ones that a health-only surveillance will always detect late",
     "are the ones that a health-only surveillance tends to detect late"),
    ("explains why the counts are always underestimated",
     "explains why the counts are almost always underestimated"),
    ("the second is usually larger and always harder to measure",
     "the second is usually larger and harder to measure"),
    ("the tree-planting target was always a political slogan",
     "the tree-planting target was from the outset a political slogan"),
]
GATE5_ID = [
    ("adalah yang selalu terlambat dideteksi surveilans yang hanya menangani kesehatan manusia",
     "adalah yang cenderung terlambat dideteksi surveilans yang hanya menangani kesehatan manusia"),
    ("yang kedua biasanya lebih besar dan selalu lebih sulit diukur",
     "yang kedua biasanya lebih besar dan lebih sulit diukur"),
    ("menjelaskan mengapa hitungannya selalu diremehkan",
     "menjelaskan mengapa hitungannya hampir selalu diremehkan"),
]


def apply(text, lang):
    pairs = EN_FS if lang == "en" else ID_FS
    n = 0
    for old, new in pairs:
        c = text.count(old)
        if c:
            text = text.replace(old, new)
            n += c
    for old, new in NUM_FIX.get(lang, []):
        c = text.count(old)
        if c:
            text = text.replace(old, new)
            n += c
    text, n_present = _present(text, lang)
    n += n_present
    text, n_assume = _assume(text, lang)
    n += n_assume
    # Pertanyaan retoris yang sama di setiap bab dihapus; paragraf
    # kontrafaktualnya sudah spesifik per topik.
    q = ("What would change these conclusions? " if lang == "en"
         else "Apa yang dapat mengubah kesimpulan ini? ")
    c = text.count(q)
    if c:
        text = text.replace(q, "")
        n += c
    for _ in range(6):
        text, c = _concl(text, lang)
        n += c
        if not c:
            break
    text, c = _world(text, lang)
    n += c
    for old, new in (EN_VAR if lang == "en" else ID_VAR):
        c = text.count(old)
        if c:
            text = text.replace(old, new)
            n += c
    for old, new in (DEDUP_EN if lang == "en" else DEDUP_ID):
        c = text.count(old)
        if c:
            text = text.replace(old, new)
            n += c
    for old, new in (GATE5_EN if lang == "en" else GATE5_ID):
        c = text.count(old)
        if c:
            text = text.replace(old, new)
            n += c
    # Variasi pembuka paragraf lapis kedua (lihat style_variety.py).
    try:
        import style_variety
    except ImportError:
        pass
    else:
        text, c = style_variety.apply(text, lang)
        n += c
    return text, n


# Paragraf "Present conditions ..." yang membuka bagian kondisi sekarang di
# dalam Skenario Masa Depan. Dulu 20 bab memakai kalimat yang sama; sekarang
# setiap bab memberi transisi yang mengikuti datanya sendiri.
PRESENT_EN = {
    4: ("Present conditions vary enormously by place.", "The exposure is not uniform."),
    5: ("Present conditions give the baseline.", "Demand already exceeds reliable supply in many basins."),
    6: ("Present conditions show the scale of the exposure.", "The exposure is concentrated on the coasts."),
    7: ("Present conditions give the baseline.", "The food system rests on a narrowing margin."),
    8: ("Present conditions are a mixture of loss and resilience.", "The picture is not one of uniform decline."),
    9: ("Present conditions give the baseline.", "The disease burden is already global."),
    10: ("Present conditions give the baseline.", "The losses are large and still growing."),
    11: ("Present conditions give the baseline.", "Those who move are a minority of those exposed."),
    12: ("Present conditions give the baseline.", "Fragility is the common denominator."),
    13: ("Present conditions give the baseline.", "The infrastructure deficit is the binding constraint."),
    14: ("Present conditions give the baseline.", "The starting point is a learning gap."),
    15: ("Present conditions define the starting point.", "The information environment is the first line of defence."),
    16: ("Present conditions set the baseline.", "For billions of households, storage is not a choice but a necessity."),
    17: ("Present conditions set the baseline.", "The baseline is a health system already under strain."),
    18: ("Present conditions set the baseline.", "The baseline is a deficit of trust."),
    19: ("Present conditions set the baseline.", "The baseline is energy poverty inside a growing system."),
    20: ("Present conditions set the baseline.", "The baseline is a treatment gap."),
    21: ("Present conditions set the baseline.", "The baseline is a finance gap."),
    22: ("Present conditions set the baseline.", "The baseline is an urban century."),
    23: ("Present conditions set the baseline.", "The baseline is a hunger crisis that is already here."),
    24: ("Present conditions set the baseline.", "The baseline is unequal preparedness."),
}
PRESENT_ID = {
    2: ("Kondisi sekarang memberi titik awal yang jelas.", "Garis dasarnya sudah berubah."),
    4: ("Kondisi saat ini sangat bervariasi menurut tempat.", "Paparan itu tidak merata."),
    5: ("Kondisi sekarang memberikan garis dasar.", "Permintaan sudah melebihi pasokan yang andal di banyak cekungan."),
    6: ("Kondisi sekarang menunjukkan skala paparannya.", "Paparan terkonsentrasi di pesisir."),
    7: ("Kondisi sekarang memberikan garis dasar.", "Sistem pangan bertumpu pada margin yang menyempit."),
    8: ("Kondisi sekarang adalah campuran kehilangan dan ketangguhan.", "Gambaran ini bukan kemunduran yang merata."),
    9: ("Kondisi sekarang memberikan garis dasar.", "Beban penyakit sudah berskala global."),
    10: ("Kondisi sekarang memberikan garis dasar.", "Kerugiannya besar dan terus tumbuh."),
    11: ("Kondisi sekarang memberikan garis dasar.", "Mereka yang bergerak hanyalah sebagian kecil dari yang terpapar."),
    12: ("Kondisi sekarang memberikan garis dasar.", "Kerapuhan adalah penyebut yang sama."),
    13: ("Kondisi sekarang memberikan garis dasar.", "Defisit infrastruktur adalah kendalanya."),
    14: ("Kondisi sekarang memberikan garis dasar.", "Titik awalnya adalah kesenjangan belajar."),
    15: ("Kondisi sekarang menentukan titik awalnya.", "Lingkungan informasi adalah garis pertahanan pertama."),
    16: ("Kondisi sekarang menetapkan garis dasar.", "Bagi miliaran rumah tangga, persediaan bukan pilihan melainkan keharusan."),
    17: ("Kondisi sekarang menetapkan garis dasar.", "Garis dasarnya adalah sistem kesehatan yang sudah tertekan."),
    18: ("Kondisi sekarang menetapkan garis dasar.", "Garis dasarnya adalah defisit kepercayaan."),
    19: ("Kondisi sekarang menetapkan garis dasar.", "Garis dasarnya adalah kemiskinan energi di tengah sistem yang tumbuh."),
    20: ("Kondisi sekarang menetapkan garis dasar.", "Garis dasarnya adalah kesenjangan pengobatan."),
    21: ("Kondisi sekarang menetapkan garis dasar.", "Garis dasarnya adalah kesenjangan pendanaan."),
    22: ("Kondisi sekarang menetapkan garis dasar.", "Garis dasarnya adalah abad perkotaan."),
    23: ("Kondisi sekarang menetapkan garis dasar.", "Garis dasarnya adalah krisis kelaparan yang sudah berlangsung."),
    24: ("Kondisi sekarang menetapkan garis dasar.", "Garis dasarnya adalah kesiapsiagaan yang tidak merata."),
}
CHAP = re.compile(r"(?ms)^(# (?:Chapter|Bab) (\d+):.*?)(?=^# (?:Chapter|Bab) \d+:|\Z)")


def _present(text, lang):
    table = PRESENT_EN if lang == "en" else PRESENT_ID
    n = 0

    def rep(m):
        nonlocal n
        block, num = m.group(1), int(m.group(2))
        if num in table:
            old, new = table[num]
            if old in block:
                block = block.replace(old, new, 1)
                n += 1
        return block

    return CHAP.sub(rep, text), n


# Paragraf asumsi di Skenario Masa Depan: 20 bab membuka dengan kalimat yang
# sama ("The assumptions that drive the projections are ..."). Diganti dengan
# kalimat yang menyebut variabel bab itu sendiri.
ASSUME_EN = {
    3: ("The assumptions that drive the scenarios are therefore not only about emissions but about the response of these slow variables.",
        "The slow variables matter as much as emissions."),
    4: ("The assumptions that drive the projections are therefore about adaptation as much as about emissions.",
        "Adaptation will matter as much as emissions."),
    5: ("The assumptions that drive the projections are population, diet, technology and governance.",
        "Population, diet, technology and governance will decide the water balance."),
    6: ("The assumptions that drive the projections are the emission path, the response of ice sheets, and the rate of subsidence.",
        "The sea-level range depends on the emission path, the response of the ice sheets and the rate of subsidence."),
    7: ("The assumptions that drive the projections are population growth, diet, technology and trade.",
        "Population growth, diet, technology and trade will decide the harvest."),
    8: ("The assumptions that drive the projections are the emission path, the rate of land-use change and the effectiveness of conservation.",
        "Ecosystem outcomes will turn on the emission path, land-use change and conservation."),
    9: ("The assumptions that drive the projections are the emission path, population growth, ageing, urbanisation and the strength of health systems.",
        "The disease burden will follow the emission path, population growth, ageing, urbanisation and the strength of health systems."),
    10: ("The assumptions that drive the projections are the emission path, the rate of adaptation, and the discount rate used to compare present and future costs.",
         "The economic cost will depend on the emission path, adaptation and the discount rate used to compare present and future costs."),
    11: ("The assumptions that drive the projections are the emission path, the rate of adaptation, and the openness of receiving countries.",
         "Displacement will follow the emission path, adaptation and the openness of receiving countries."),
    12: ("The assumptions that drive the projections are the emission path, the rate of development and the quality of governance.",
         "Security risk will track the emission path, development and governance."),
    13: ("The assumptions that drive the projections are the emission path, the rate of retrofitting, and the standards that are adopted.",
         "Infrastructure outcomes will depend on the emission path, retrofitting and the standards adopted."),
    14: ("The assumptions that drive the projections are the rate of curriculum reform, the quality of teacher training, and the impact of climate shocks on schooling.",
         "The education outcome will turn on curriculum reform, teacher training and the impact of climate shocks on schooling."),
    15: ("The assumptions that drive the projections are the pace of regulation, the cost of detection, and the resilience of local institutions.",
         "The information environment will turn on the pace of regulation, the cost of detection and the resilience of local institutions."),
    16: ("The assumptions behind the projections are the frequency of disruption, the cost and availability of preparedness goods, and the strength of community networks.",
         "Household preparedness will depend on the frequency of disruption, the price of preparedness goods and the strength of community networks."),
    17: ("The assumptions behind the projections are the pace of warming, the level of investment in health systems, and the effectiveness of adaptation.",
         "Health outcomes will follow the pace of warming, investment in health systems and the effectiveness of adaptation."),
    18: ("The assumptions behind the projections are the trajectory of institutional quality, the level of finance, and the degree of international cooperation.",
         "Governance outcomes will track institutional quality, finance and international cooperation."),
    19: ("The assumptions behind the projections are the pace of cost decline, the rate of grid investment, and the strength of policy.",
         "The energy transition will turn on cost decline, grid investment and policy strength."),
    20: ("The assumptions behind the projections are the frequency of hazards, the availability of services, and the strength of social support.",
         "Mental health outcomes will follow the frequency of hazards, the availability of services and the strength of social support."),
    21: ("The assumptions behind the projections are the pace of climate change, the strength of international institutions and the level of civic pressure.",
         "Climate justice will depend on the pace of climate change, the strength of international institutions and the level of civic pressure."),
    22: ("The assumptions behind the projections are the pace of warming, the rate of urbanisation and the quality of urban governance.",
         "Urban outcomes will turn on the pace of warming, urbanisation and the quality of urban governance."),
    23: ("The assumptions behind the projections are the pace of warming, the level of investment in water and social protection, and the intensity of conflict.",
         "Hunger and water security will follow the pace of warming, investment in water and social protection, and the intensity of conflict."),
    24: ("The assumptions behind the projections are the pace of warming, the level of investment and the quality of governance.",
         "Preparedness will depend on the pace of warming, investment and governance quality."),
}
ASSUME_ID = {
    3: ("Asumsi yang menggerakkan skenario karena itu bukan hanya tentang emisi tetapi juga tentang respons variabel-variabel lambat ini.",
        "Variabel-variabel lambat itu sama pentingnya dengan emisi."),
    4: ("Asumsi yang menggerakkan proyeksi karena itu sama besarnya dengan asumsi tentang adaptasi seperti tentang emisi.",
        "Adaptasi sama pentingnya dengan emisi."),
    5: ("Asumsi yang menggerakkan proyeksi adalah populasi, pola makan, teknologi, dan tata kelola.",
        "Populasi, pola makan, teknologi, dan tata kelola akan menentukan neraca air."),
    6: ("Asumsi yang menggerakkan proyeksi adalah jalur emisi, respons lapisan es, dan laju penurunan tanah.",
        "Rentang muka laut bergantung pada jalur emisi, respons lapisan es, dan laju penurunan tanah."),
    7: ("Asumsi yang menggerakkan proyeksi adalah pertumbuhan penduduk, pola makan, teknologi, dan perdagangan.",
        "Pertumbuhan penduduk, pola makan, teknologi, dan perdagangan akan menentukan hasil panen."),
    8: ("Asumsi yang menggerakkan proyeksi adalah jalur emisi, laju perubahan penggunaan lahan, dan efektivitas konservasi.",
        "Nasib ekosistem akan bergantung pada jalur emisi, perubahan penggunaan lahan, dan efektivitas konservasi."),
    9: ("Asumsi yang menggerakkan proyeksi adalah jalur emisi, pertumbuhan penduduk, penuaan, urbanisasi, dan kekuatan sistem kesehatan.",
        "Beban penyakit akan mengikuti jalur emisi, pertumbuhan penduduk, penuaan, urbanisasi, dan kekuatan sistem kesehatan."),
    10: ("Asumsi yang menggerakkan proyeksi adalah jalur emisi, laju adaptasi, dan tingkat diskonto yang digunakan untuk membandingkan biaya sekarang dan masa depan.",
         "Biaya ekonomi akan bergantung pada jalur emisi, laju adaptasi, dan tingkat diskonto yang dipakai membandingkan biaya sekarang dan masa depan."),
    11: ("Asumsi yang menggerakkan proyeksi adalah jalur emisi, laju adaptasi, dan keterbukaan negara penerima.",
         "Perpindahan penduduk akan mengikuti jalur emisi, laju adaptasi, dan keterbukaan negara penerima."),
    12: ("Asumsi yang menggerakkan proyeksi adalah jalur emisi, laju pembangunan, dan kualitas tata kelola.",
         "Risiko keamanan akan mengikuti jalur emisi, laju pembangunan, dan kualitas tata kelola."),
    13: ("Asumsi yang menggerakkan proyeksi adalah jalur emisi, laju retrofit, dan standar yang diadopsi.",
         "Hasil infrastruktur akan bergantung pada jalur emisi, laju retrofit, dan standar yang diadopsi."),
    14: ("Asumsi yang menggerakkan proyeksi adalah laju reformasi kurikulum, kualitas pelatihan guru, dan dampak guncangan iklim terhadap persekolahan.",
         "Hasil pendidikan akan bergantung pada reformasi kurikulum, pelatihan guru, dan dampak guncangan iklim terhadap persekolahan."),
    15: ("Asumsi yang menggerakkan proyeksi adalah laju regulasi, biaya deteksi, dan ketangguhan institusi lokal.",
         "Lingkungan informasi akan bergantung pada laju regulasi, biaya deteksi, dan ketangguhan institusi lokal."),
    16: ("Asumsi di balik proyeksi adalah frekuensi gangguan, biaya dan ketersediaan barang kesiapsiagaan, serta kekuatan jaringan komunitas.",
         "Kesiapsiagaan rumah tangga akan bergantung pada frekuensi gangguan, harga barang kesiapsiagaan, dan kekuatan jaringan komunitas."),
    17: ("Asumsi di balik proyeksi adalah laju pemanasan, tingkat investasi dalam sistem kesehatan, dan efektivitas adaptasi.",
         "Hasil kesehatan akan mengikuti laju pemanasan, investasi dalam sistem kesehatan, dan efektivitas adaptasi."),
    18: ("Asumsi di balik proyeksi adalah lintasan kualitas institusi, tingkat pembiayaan, dan derajat kerja sama internasional.",
         "Hasil tata kelola akan mengikuti kualitas institusi, pembiayaan, dan kerja sama internasional."),
    19: ("Asumsi di balik proyeksi adalah laju penurunan biaya, tingkat investasi jaringan, dan kekuatan kebijakan.",
         "Transisi energi akan bergantung pada penurunan biaya, investasi jaringan, dan kekuatan kebijakan."),
    20: ("Asumsi di balik proyeksi adalah frekuensi bahaya, ketersediaan layanan, dan kekuatan dukungan sosial.",
         "Hasil kesehatan mental akan mengikuti frekuensi bahaya, ketersediaan layanan, dan kekuatan dukungan sosial."),
    21: ("Asumsi di balik proyeksi adalah laju perubahan iklim, kekuatan institusi internasional, dan tingkat tekanan warga.",
         "Keadilan iklim akan bergantung pada laju perubahan iklim, kekuatan institusi internasional, dan tingkat tekanan warga."),
    22: ("Asumsi di balik proyeksi adalah laju pemanasan, laju urbanisasi, dan kualitas tata kelola kota.",
         "Hasil perkotaan akan bergantung pada laju pemanasan, urbanisasi, dan kualitas tata kelola kota."),
    23: ("Asumsi di balik proyeksi adalah laju pemanasan, tingkat investasi dalam air dan perlindungan sosial, dan intensitas konflik.",
         "Ketahanan pangan dan air akan mengikuti laju pemanasan, investasi dalam air dan perlindungan sosial, serta intensitas konflik."),
    24: ("Asumsi di balik proyeksi adalah laju pemanasan, tingkat investasi, dan kualitas tata kelola.",
         "Kesiapsiagaan akan bergantung pada laju pemanasan, investasi, dan kualitas tata kelola."),
}


def _assume(text, lang):
    table = ASSUME_EN if lang == "en" else ASSUME_ID
    n = 0

    def rep(m):
        nonlocal n
        block, num = m.group(1), int(m.group(2))
        if num in table:
            old, new = table[num]
            if old in block:
                block = block.replace(old, new, 1)
                n += 1
        return block

    return CHAP.sub(rep, text), n
