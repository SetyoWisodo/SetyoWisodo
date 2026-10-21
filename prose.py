# -*- coding: utf-8 -*-
"""Mesin prosa Gate 3.

Menggantikan template lama yang mengulang frasa topik belasan kali per paragraf.
Prinsip:
  * frasa topik ({S}) muncul sekali per paragraf, sisanya koreferensi;
  * setiap paragraf memuat satu angka bersitasi ({D});
  * klaim dikalibrasi (hedging), bukan absolut;
  * delapan lensa argumen, dua varian, dipilih deterministik per bab/seksi.
"""

import re

ACRO = ("IPCC", "AI", "PTSD", "CO2", "SSP", "UN", "WHO", "FAO", "WMO", "GDP",
        "UNDRR", "NOAA", "NASA", "UNHCR", "IFRC", "NGO", "PLN", "BMKG")

# ------------------------------------------------------------------ util ----
def _lower_title(t):
    out = []
    for i, w in enumerate(t.split()):
        parts = []
        for j, p in enumerate(w.split("-")):
            plain = p.strip("'\"(),.:;")
            if plain.upper() in ACRO or (len(plain) > 1 and plain.isupper()):
                parts.append(p)
            elif i == 0 and j == 0:
                parts.append(p[:1].lower() + p[1:])
            else:
                parts.append(p.lower())
        out.append("-".join(parts))
    return " ".join(out)


NP_SPECIAL = {
    "en": {
        "What Is Climate Literacy": "the meaning of climate literacy",
        "What Is Social Capital and Trust": "the meaning of social capital and trust",
        "Why Data Matters and Types of Data": "why data matter and which data are used",
        "Correlation vs Causation": "the difference between correlation and causation",
        "Renewable Energy Systems and Solar/Battery": "renewable energy, solar and battery systems",
        "Graphs, Charts and Misleading Statistics": "graphs, charts and misleading statistics",
    },
    "id": {
        "Apa Itu Literasi Iklim": "makna literasi iklim",
        "Apa Itu Modal Sosial dan Kepercayaan": "makna modal sosial dan kepercayaan",
        "Mengapa Data Penting dan Jenis Data": "mengapa data penting dan data apa yang dipakai",
        "Korelasi vs Kausalitas": "perbedaan korelasi dan kausalitas",
        "Sistem Energi Terbarukan dan Surya/Baterai": "energi terbarukan, surya dan baterai",
        "Grafik, Bagan dan Statistik Menyesatkan": "grafik, bagan dan statistik yang menyesatkan",
    },
}


def np_of(title, lang):
    key = title.strip()
    if key in NP_SPECIAL[lang]:
        return NP_SPECIAL[lang][key]
    return _lower_title(key)


# --------------------------------------------------------------- domains ----
DOMAINS = {
    "en": [
        "public communication about climate risk",
        "the physics community and observation networks",
        "monitoring agencies and forecasting services",
        "city health services and labour policy",
        "water utilities and irrigated agriculture",
        "coastal planning and flood defence",
        "food systems and rural livelihoods",
        "conservation and land management",
        "health systems and epidemiology",
        "finance ministries and insurers",
        "migration policy and urban services",
        "security services and local government",
        "infrastructure operators and utilities",
        "schools and adult education",
        "statistical agencies and the media",
        "households and community groups",
        "emergency services and clinics",
        "civil society and local associations",
        "energy planners and regulators",
        "mental-health services and schools",
        "courts, legislatures and civic organisations",
        "urban authorities in fire- and flood-prone regions",
        "rural authorities in drought-prone regions",
        "households, schools and local government",
    ],
    "id": [
        "komunikasi publik tentang risiko iklim",
        "komunitas fisika dan jaringan observasi",
        "lembaga pemantauan dan layanan prakiraan",
        "layanan kesehatan kota dan kebijakan ketenagakerjaan",
        "perusahaan air dan pertanian beririgasi",
        "perencanaan pesisir dan pertahanan banjir",
        "sistem pangan dan penghidupan pedesaan",
        "konservasi dan pengelolaan lahan",
        "sistem kesehatan dan epidemiologi",
        "kementerian keuangan dan perusahaan asuransi",
        "kebijakan migrasi dan layanan perkotaan",
        "layanan keamanan dan pemerintah lokal",
        "operator infrastruktur dan utilitas",
        "sekolah dan pendidikan orang dewasa",
        "lembaga statistik dan media",
        "rumah tangga dan kelompok warga",
        "layanan darurat dan klinik",
        "masyarakat sipil dan perkumpulan lokal",
        "perencana dan regulator energi",
        "layanan kesehatan jiwa dan sekolah",
        "pengadilan, legislatif dan organisasi warga",
        "pemerintah kota di kawasan rawan api dan banjir",
        "pemerintah daerah di kawasan rawan kekeringan",
        "rumah tangga, sekolah dan pemerintah lokal",
    ],
}

# lensa yang relevan per bab (menghindari lensa yang tidak nyambung dengan topik)
LENS_BY_CHAPTER = {
    2: ("framing", "evidence", "causal", "uncertainty"),
    3: ("evidence", "distribution", "institutions", "cost"),
    4: ("causal", "decision", "framing", "uncertainty"),
    5: ("distribution", "institutions", "cost", "decision"),
    6: ("institutions", "framing", "evidence", "causal"),
    7: ("cost", "uncertainty", "distribution", "decision"),
    8: ("evidence", "framing", "causal", "uncertainty"),
    9: ("distribution", "institutions", "cost", "decision"),
    10: ("cost", "framing", "evidence", "causal"),
    11: ("distribution", "uncertainty", "institutions", "decision"),
    12: ("institutions", "framing", "evidence", "causal"),
    13: ("causal", "uncertainty", "distribution", "cost"),
    14: ("framing", "decision", "evidence", "uncertainty"),
    15: ("distribution", "institutions", "cost", "decision"),
    16: ("cost", "framing", "evidence", "causal"),
    17: ("institutions", "uncertainty", "distribution", "decision"),
    18: ("uncertainty", "framing", "evidence", "causal"),
    19: ("decision", "distribution", "institutions", "cost"),
    20: ("framing", "evidence", "causal", "uncertainty"),
    21: ("cost", "distribution", "institutions", "decision"),
    22: ("uncertainty", "framing", "evidence", "causal"),
    23: ("causal", "distribution", "institutions", "cost"),
}

# data point yang relevan per bab (indeks pada DATA_POINTS)
DATA_PICK = [
    [0, 4, 6], [0, 1, 3], [0, 3, 2], [6, 0, 7], [9, 10, 8], [2, 4, 5],
    [8, 10, 4], [3, 8, 6], [6, 7, 4], [5, 4, 6], [11, 4, 6], [4, 5, 11],
    [5, 2, 4], [0, 4, 5], [0, 5, 4], [6, 9, 0], [6, 7, 5], [4, 6, 7],
    [1, 5, 4], [6, 4, 7], [5, 4, 6], [6, 5, 2], [8, 9, 10], [4, 6, 9],
]

# ------------------------------------------------------------------ lensa ---
LENS = {
    "en": {
        "framing": [
            [
                "Discussion of {S} usually begins as a technical question, and that framing hides the decisions underneath it.",
                "The technical part is real: measurement, modelling and attribution have improved sharply over two decades (IPCC, 2023).",
                "But the contested part is rarely the measurement; it is what the numbers imply for who acts, who pays and who is protected.",
                "One figure sets the scale: {D}.",
                "Read that way, the question for {DOM} is not whether the trend is real but which choices remain defensible across the plausible range.",
                "A framing that treats uncertainty as a reason to wait gets the logic backwards: uncertainty is what makes early, reversible decisions valuable.",
            ],
            [
                "Most disagreements about {S} are not disagreements about facts.",
                "They are disagreements about weight: which risks count, over what horizon, and for whom (IPCC, 2022).",
                "That is why the same evidence can support both alarm and complacency without either side misreading the data.",
                "The scale involved is not marginal: {D}.",
                "For {DOM}, clarity about the weighting matters as much as clarity about the measurement.",
                "Stating the criterion in advance is what separates analysis from advocacy.",
            ],
        ],
        "evidence": [
            [
                "Evidence on {S} rests on several independent lines rather than a single study.",
                "Satellites, ground stations, ocean measurements and model reanalyses now agree on direction, and disagree mainly on pace and regional detail (IPCC, 2021).",
                "One measure puts the magnitude in view: {D}.",
                "Confidence is highest where those lines converge and lowest where one method or a short record carries the claim.",
                "For {DOM}, that means planning against a range rather than a point.",
                "A decision built on the central estimate alone is a decision that will be surprised.",
            ],
            [
                "The record on {S} is now strong enough to be treated as a trend rather than an anomaly.",
                "The record is uneven — some regions and seasons move sharply, others barely — but the aggregate direction is consistent across methods (IPCC, 2023).",
                "The headline figure is blunt: {D}.",
                "What remains contested is attribution of individual events and the speed of future change, not whether the baseline has shifted.",
                "That distinction shapes how {DOM} should read the numbers: as a distribution to plan against, not a forecast to await.",
                "Where the evidence is thin, the honest response is a stated limitation rather than a confident sentence.",
            ],
        ],
        "causal": [
            [
                "The causal path can be traced step by step, which is why the broad direction is predictable even when individual events are not.",
                "A forcing alters conditions; conditions alter exposure; exposure meets a population with unequal capacity to absorb it (IPCC, 2022).",
                "Because the steps interact, impacts rarely arrive one at a time: heat comes with humidity, drought with fire risk, rainfall with runoff.",
                "The same pattern is visible in the numbers: {D}.",
                "For {DOM}, the practical implication is to plan for combinations rather than single hazards.",
                "Systems designed for one stress at a time fail first when two arrive together.",
            ],
            [
                "Why things behave as they do is a question with a traceable answer.",
                "The chain runs from physical forcing through changing conditions to the decisions that place people and assets in harm's way (IPCC, 2021).",
                "Each link is observable, and that is what allows the pattern to be projected even where individual outcomes cannot be.",
                "The magnitudes involved are not small: {D}.",
                "For {DOM}, there is more than one point of action, and the cheapest interventions are usually the earliest.",
                "Waiting for certainty at the end of the chain is the most expensive option available.",
            ],
        ],
        "distribution": [
            [
                "The resulting risk is distributed unevenly, and the unevenness is structural rather than accidental.",
                "Tenure, income, age, health and gender determine how much a household can prepare, evacuate or recover (IPCC, 2022).",
                "The aggregate numbers conceal this: {D}.",
                "Averages describe the size of the problem, not who carries it.",
                "Decisions taken by {DOM} — where to build, whom to insure, which services keep running — widen that gap or close it.",
                "A policy that protects the average household while leaving the most exposed unprotected has not solved the problem it claims to solve.",
            ],
            [
                "The burden falls first on people with the least room to manoeuvre.",
                "Those with insecure tenure, irregular income or caring responsibilities have less capacity to move, insure or wait for compensation (IPCC, 2022).",
                "The scale is not marginal: {D}.",
                "Because disadvantages compound, the same event can be an inconvenience for one family and a permanent loss for another.",
                "For {DOM}, equity is therefore a design criterion rather than a footnote.",
                "Measures that reach the most exposed first tend to perform better for everyone else as well.",
            ],
        ],
        "institutions": [
            [
                "Whether the problem remains manageable depends as much on institutions as on the underlying trend.",
                "Early warning, land-use rules, standards and social protection reduce harm, but only where authority and funding reach the level at which risk is felt (UNDRR, 2015).",
                "The common failure is fragmentation: overlapping mandates, unshared data, responsibility falling between agencies.",
                "Coordination is a design problem with measurable features — joint protocols, common baselines, clear triggers.",
                "For {DOM}, the test is whether its own arrangements have those features before the next event rather than after it.",
                "Where such arrangements exist, response times fall and losses follow.",
            ],
            [
                "Governance is tested at the seams between organisations.",
                "Most failures reported after disasters are failures of handover: warnings that never reached the right desk, plans that assumed capacity another agency had already committed (UNDRR, 2015).",
                "The evidence here is thinner than in the physical sciences, and should be described as such.",
                "One indication of the stakes: {D}.",
                "What the record does show is that authority, money and information have to move together; any one without the others stalls.",
                "For {DOM}, the test is whether a decision can be taken where the consequence is felt, with the resources to act on it.",
            ],
        ],
        "cost": [
            [
                "The economics favour early action, but the arithmetic is routinely misread.",
                "Damage functions show rising marginal losses with warming, while preventive spending delivers returns over decades (World Bank, 2022).",
                "The magnitudes are large: {D}.",
                "The obstacle is less the total than the distribution of costs and benefits: those who pay are rarely those who are protected.",
                "For {DOM}, the implication is to count avoided losses, not only capital outlays.",
                "Insurance can spread the residual risk; it cannot reduce the hazard itself.",
            ],
            [
                "Money spent before an event buys more protection than money spent after it.",
                "That claim rests on damage functions and on the repeated observation that recovery costs exceed prevention costs by a wide margin (World Bank, 2022).",
                "The order of magnitude is not in doubt: {D}.",
                "What is uncertain is how benefits are distributed and how quickly they appear, which is why appraisal methods matter.",
                "For {DOM}, the relevant question is not whether prevention pays but who captures the return.",
                "Financing arrangements that ignore that question tend to fund visible damage and neglect invisible capacity.",
            ],
        ],
        "uncertainty": [
            [
                "The strength of the claim about {S} varies, and that variation should be visible in the prose.",
                "Detection and attribution are well supported; regional projections carry wider bands; estimates of future damage depend on assumptions about emissions and adaptation (IPCC, 2021).",
                "A concrete example of the difference: {D}.",
                "A central estimate without its range is not more precise, only less honest.",
                "For {DOM}, the discipline is to keep scenarios labelled as scenarios and observations labelled as observations.",
                "Where the evidence is thin, the correct response is a stated limitation rather than a confident sentence.",
            ],
            [
                "Not all statements about {S} carry the same warrant.",
                "Some rest on direct measurement, some on models, some on expert judgement, and the three should not be written in the same voice (IPCC, 2021).",
                "The numbers are often firmer than the uses to which they are put: {D}.",
                "Misreading usually happens in translation — a global average applied to a locality, a scenario treated as a forecast.",
                "For {DOM}, the safeguard is to record the source, period and assumptions behind each figure used.",
                "Traceability is not bureaucracy; it is what allows a claim to be checked later.",
            ],
        ],
        "decision": [
            [
                "The next decade will show whether preparation or improvisation prevails.",
                "Three signals are worth tracking: how often events exceed design thresholds, how much public spending goes to prevention rather than repair, and whether the most exposed groups gain access before a disaster rather than after it (IPCC, 2023).",
                "The baseline is already shifting: {D}.",
                "None of those signals is a perfect measure, but together they indicate direction.",
                "For {DOM}, adaptation is not a state to be reached but a standing capacity to revise decisions as evidence changes.",
                "The test is whether the next surprise is met with a plan or with a scramble.",
            ],
            [
                "Any assessment of {S} will turn less on what is promised now than on what is in place when the next event arrives.",
                "Plans that exist only on paper, thresholds that trigger no action, and funds that cannot be released quickly are the recurring failure modes (UNDRR, 2015).",
                "The pressure is not hypothetical: {D}.",
                "Progress can be measured in lead times, in the share of exposed households covered by warning and insurance, and in how quickly services return.",
                "For {DOM}, reviewing those measures on a fixed cycle works better than reviewing them after each disaster.",
                "Iteration is the difference between adaptation and repeated recovery.",
            ],
        ],
    },
    "id": {
        "framing": [
            [
                "Pendekatan teknis terhadap {S} adalah titik awal yang wajar, tetapi cara membingkainya menyembunyikan keputusan di bawahnya.",
                "Bagian teknisnya nyata: pengukuran, pemodelan dan atribusi membaik tajam dalam dua dekade (IPCC, 2023).",
                "Namun yang diperdebatkan jarang pengukurannya; yang diperdebatkan adalah implikasi angka bagi siapa yang bertindak, siapa yang membayar dan siapa yang dilindungi.",
                "Satu angka memberi skala: {D}.",
                "Dibaca begitu, pertanyaan bagi {DOM} bukan apakah trennya nyata, melainkan pilihan mana yang tetap dapat dipertahankan pada seluruh rentang yang masuk akal.",
                "Cara bingkai yang memperlakukan ketidakpastian sebagai alasan menunggu membalik logikanya: ketidakpastian justru membuat keputusan dini yang dapat dibalik menjadi berharga.",
            ],
            [
                "Sebagian besar perbedaan pendapat tentang {S} bukan perbedaan tentang fakta.",
                "Perbedaan itu menyangkut bobot: risiko mana yang dihitung, dalam horizon apa, dan bagi siapa (IPCC, 2022).",
                "Karena itu bukti yang sama dapat menopang kewaspadaan maupun kelengahan tanpa ada pihak yang salah membaca data.",
                "Skalanya tidak kecil: {D}.",
                "Bagi {DOM}, kejelasan tentang pembobotan sama pentingnya dengan kejelasan tentang pengukuran.",
                "Menyatakan kriterianya lebih dulu adalah yang memisahkan analisis dari advokasi.",
            ],
        ],
        "evidence": [
            [
                "Bukti tentang {S} bertumpu pada beberapa jalur independen, bukan satu studi.",
                "Satelit, stasiun permukaan, pengukuran laut dan reanalisis model kini sepakat tentang arah, dan berbeda terutama soal laju serta rincian wilayah (IPCC, 2021).",
                "Satu ukuran menunjukkan besarnya: {D}.",
                "Keyakinan tertinggi ada pada titik temu jalur-jalur itu, dan terendah ketika satu metode atau catatan pendek menanggung seluruh klaim.",
                "Bagi {DOM}, artinya merencanakan pada rentang, bukan pada satu titik.",
                "Keputusan yang hanya bersandar pada nilai tengah adalah keputusan yang akan terkejut.",
            ],
            [
                "Catatan tentang {S} kini cukup kuat untuk diperlakukan sebagai tren, bukan anomali.",
                "Catatannya tidak rata — sebagian wilayah dan musim berubah tajam, sebagian lain nyaris tidak — tetapi arah agregatnya konsisten lintas metode (IPCC, 2023).",
                "Angka utamanya tegas: {D}.",
                "Yang masih diperdebatkan adalah atribusi peristiwa tunggal dan kecepatan perubahan mendatang, bukan apakah garis dasarnya sudah bergeser.",
                "Perbedaan itu membentuk cara {DOM} membaca angka: sebagai distribusi untuk direncanakan, bukan ramalan untuk ditunggu.",
                "Ketika buktinya tipis, jawaban jujurnya adalah batasan yang dinyatakan, bukan kalimat yang percaya diri.",
            ],
        ],
        "causal": [
            [
                "Jalur sebab-akibatnya dapat ditelusuri langkah demi langkah, itulah sebabnya arah besarnya dapat diprediksi meski peristiwa tunggalnya tidak.",
                "Pemaksaan mengubah kondisi; kondisi mengubah paparan; paparan bertemu populasi dengan kapasitas serap yang tidak setara (IPCC, 2022).",
                "Karena langkah-langkahnya saling terkait, dampaknya jarang datang sendiri: panas bersama kelembapan, kekeringan bersama risiko kebakaran, hujan bersama limpasan.",
                "Pola yang sama terlihat pada angkanya: {D}.",
                "Bagi {DOM}, implikasi praktisnya adalah merencanakan kombinasi, bukan satu bahaya.",
                "Sistem yang dirancang untuk satu tekanan pada satu waktu akan gagal lebih dulu ketika dua datang bersamaan.",
            ],
            [
                "Mengapa sesuatu berperilaku demikian adalah pertanyaan yang punya jawaban tertelusur.",
                "Rantainya berjalan dari pemaksaan fisik melalui perubahan kondisi hingga keputusan yang menempatkan orang dan aset di jalur bahaya (IPCC, 2021).",
                "Setiap mata rantai dapat diamati, dan itulah yang memungkinkan polanya diproyeksikan meski hasil individualnya tidak.",
                "Besaran yang terlibat tidak kecil: {D}.",
                "Bagi {DOM}, ada lebih dari satu titik tindakan, dan intervensi termurah biasanya yang paling awal.",
                "Menunggu kepastian di ujung rantai adalah pilihan termahal yang tersedia.",
            ],
        ],
        "distribution": [
            [
                "Risiko yang dihasilkan tersebar tidak merata, dan ketidakmerataannya struktural, bukan kebetulan.",
                "Kepemilikan lahan, pendapatan, usia, kesehatan dan gender menentukan seberapa mampu rumah tangga bersiap, mengungsi atau pulih (IPCC, 2022).",
                "Angka agregat menyembunyikan hal ini: {D}.",
                "Rata-rata menggambarkan besar masalah, bukan siapa yang menanggungnya.",
                "Keputusan yang diambil {DOM} — di mana membangun, siapa diasuransikan, layanan mana yang tetap hidup — melebarkan atau menyempitkan jurang itu.",
                "Kebijakan yang melindungi rumah tangga rata-rata tetapi membiarkan yang paling terpapar tetap terlindungi belum menyelesaikan masalah yang diklaimnya.",
            ],
            [
                "Bebannya jatuh lebih dulu pada orang dengan ruang gerak paling sempit.",
                "Mereka yang kepemilikan lahannya tidak aman, berpendapatan tidak tetap atau menanggung perawatan keluarga lebih kecil kapasitasnya untuk pindah, mengasuransikan diri atau menunggu ganti rugi (IPCC, 2022).",
                "Skalanya tidak marginal: {D}.",
                "Karena kerugian bertumpuk, peristiwa yang sama bisa menjadi gangguan bagi satu keluarga dan kehilangan permanen bagi keluarga lain.",
                "Bagi {DOM}, keadilan karena itu menjadi kriteria desain, bukan catatan kaki.",
                "Tindakan yang menjangkau yang paling terpapar lebih dulu cenderung bekerja lebih baik bagi semua orang.",
            ],
        ],
        "institutions": [
            [
                "Apakah masalah ini tetap terkelola bergantung sama besar pada institusi dan pada tren dasarnya.",
                "Peringatan dini, aturan tata guna lahan, standar dan perlindungan sosial mengurangi kerugian, tetapi hanya jika kewenangan dan dana mencapai tingkat tempat risiko dirasakan (UNDRR, 2015).",
                "Kegagalan yang umum adalah fragmentasi: mandat yang tumpang tindih, data yang tidak dibagi, tanggung jawab yang jatuh di antara lembaga.",
                "Koordinasi adalah masalah desain dengan ciri yang terukur — protokol bersama, garis dasar yang sama, pemicu yang jelas.",
                "Bagi {DOM}, ujiannya adalah apakah pengaturannya sendiri memiliki ciri itu sebelum peristiwa berikutnya, bukan sesudahnya.",
                "Di tempat pengaturan itu ada, waktu tanggap turun dan kerugian mengikuti.",
            ],
            [
                "Tata kelola diuji pada sambungan antarsorganisasi.",
                "Sebagian besar kegagalan yang dilaporkan setelah bencana adalah kegagalan serah terima: peringatan yang tak sampai ke meja yang tepat, rencana yang mengandaikan kapasitas yang sudah dipakai lembaga lain (UNDRR, 2015).",
                "Basis buktinya lebih tipis daripada ilmu fisik, dan harus disebut begitu.",
                "Satu petunjuk taruhannya: {D}.",
                "Yang ditunjukkan catatan adalah bahwa kewenangan, uang dan informasi harus bergerak bersama; salah satu tanpa yang lain akan macet.",
                "Bagi {DOM}, ujiannya sederhana: dapatkah keputusan diambil di tingkat tempat akibatnya dirasakan, dengan sumber daya untuk bertindak?",
            ],
        ],
        "cost": [
            [
                "Ekonomi mendukung tindakan dini, tetapi hitungannya sering salah dibaca.",
                "Fungsi kerugian menunjukkan kerugian marginal yang naik seiring pemanasan, sementara belanja pencegahan memberi imbal hasil dalam hitungan dekade (World Bank, 2022).",
                "Besarnya besar: {D}.",
                "Hambatannya bukan total, melainkan sebaran biaya dan manfaat: yang membayar jarang yang dilindungi.",
                "Bagi {DOM}, implikasinya adalah menghitung kerugian yang dihindari, bukan hanya belanja modal.",
                "Asuransi dapat menyebarkan risiko sisa; ia tidak dapat mengurangi bahayanya sendiri.",
            ],
            [
                "Uang yang dibelanjakan sebelum peristiwa memberi perlindungan lebih besar daripada uang yang dibelanjakan sesudahnya.",
                "Klaim itu bertumpu pada fungsi kerugian dan pada pengamatan berulang bahwa biaya pemulihan jauh melampaui biaya pencegahan (World Bank, 2022).",
                "Urutan besarnya tidak diragukan: {D}.",
                "Yang tidak pasti adalah bagaimana manfaatnya tersebar dan seberapa cepat muncul, karena itu metode penilaian penting.",
                "Bagi {DOM}, pertanyaannya bukan apakah pencegahan menguntungkan, melainkan siapa yang menangkap imbal hasilnya.",
                "Pengaturan pembiayaan yang mengabaikan pertanyaan itu cenderung membiayai kerusakan yang terlihat dan melupakan kapasitas yang tak terlihat.",
            ],
        ],
        "uncertainty": [
            [
                "Kekuatan klaim tentang {S} berbeda-beda, dan perbedaan itu harus terlihat dalam kalimatnya.",
                "Deteksi dan atribusi didukung baik; proyeksi wilayah membawa rentang lebih lebar; perkiraan kerugian masa depan bergantung pada asumsi emisi dan adaptasi (IPCC, 2021).",
                "Contoh nyata perbedaannya: {D}.",
                "Perkiraan titik tanpa rentangnya bukan lebih tepat, hanya kurang jujur.",
                "Bagi {DOM}, disiplinnya adalah menjaga skenario tetap disebut skenario dan observasi tetap disebut observasi.",
                "Ketika buktinya tipis, jawaban yang benar adalah batasan yang dinyatakan, bukan kalimat yang percaya diri.",
            ],
            [
                "Tidak semua pernyataan tentang {S} membawa dasar bukti yang sama.",
                "Sebagian bersandar pada pengukuran langsung, sebagian pada model, sebagian pada pertimbangan ahli, dan ketiganya tidak boleh ditulis dengan suara yang sama (IPCC, 2021).",
                "Angkanya sering lebih kukuh daripada penggunaannya: {D}.",
                "Salah baca biasanya terjadi dalam penerjemahan — rata-rata global diterapkan pada satu lokasi, skenario diperlakukan sebagai ramalan.",
                "Bagi {DOM}, pencegahannya adalah mencatat sumber, periode dan asumsi di balik setiap angka yang dipakai.",
                "Ketertelusuran bukan birokrasi; itulah yang memungkinkan klaim diperiksa kemudian.",
            ],
        ],
        "decision": [
            [
                "Dekade berikutnya akan menunjukkan apakah persiapan atau improvisasi yang menang.",
                "Tiga sinyal layak dipantau: seberapa sering peristiwa melampaui ambang desain, berapa besar belanja publik untuk pencegahan dibanding perbaikan, dan apakah kelompok paling terpapar memperoleh akses sebelum bencana, bukan sesudahnya (IPCC, 2023).",
                "Garis dasarnya sudah bergeser: {D}.",
                "Tak satu pun sinyal itu sempurna, tetapi bersama-sama menunjukkan arah.",
                "Bagi {DOM}, adaptasi bukan keadaan yang dicapai sekali, melainkan kapasitas tetap untuk merevisi keputusan saat bukti berubah.",
                "Ujiannya adalah apakah kejutan berikutnya dihadapi dengan rencana atau dengan kesibukan mendadak.",
            ],
            [
                "Penilaian atas {S} akan lebih bergantung pada apa yang sudah ada saat peristiwa berikutnya datang daripada pada janji sekarang.",
                "Rencana yang hanya ada di kertas, ambang yang tidak memicu tindakan, dan dana yang tidak dapat dicairkan cepat adalah pola kegagalan yang berulang (UNDRR, 2015).",
                "Tekanannya bukan hipotetis: {D}.",
                "Kemajuan dapat diukur dari waktu peringatan, proporsi rumah tangga terpapar yang tercakup peringatan dan asuransi, serta kecepatan layanan pulih.",
                "Bagi {DOM}, meninjau ukuran itu pada siklus tetap lebih baik daripada setelah setiap bencana.",
                "Iterasi adalah pembeda antara adaptasi dan pemulihan yang berulang.",
            ],
        ],
    },
}

# --------------------------------------------------------------- frames -----
FRAMES = {
    "en": {
        "expert_a": "As {name} ({year}) argues, {quote}",
        "expert_b": "{name} ({year}) puts it plainly: {quote}",
        "expert_close": [
            "The claim is about timing as much as magnitude.",
            "It is a warning about the cost of delay, not a prediction of doom.",
            "That is an argument about the shape of the risk, not only its size.",
            "Read carefully, it is a statement about what should be decided now.",
        ],
        "news": [
            "A recent marker points the same way: {news}.",
            "The news cycle supplies a concrete marker: {news}.",
            "Current reporting adds detail rather than a new direction: {news}.",
        ],
        "limit": [
            "The evidence is not unanimous on pace and regional detail, and the gaps should be named rather than smoothed over. Where estimates differ, the difference usually traces back to assumptions about emissions, adaptation and measurement. That does not weaken the case for action; it defines the range within which action has to be robust.",
            "Certainty is unevenly distributed across this literature. Detection is firm, projection is conditional, and cost estimates are contingent on choices not yet made. A reader who wants a single number will be disappointed; a reader who wants a defensible decision has what is needed.",
            "Two cautions apply to everything in this section. First, most figures are aggregates, and aggregates travel badly between countries and neighbourhoods. Second, published estimates lag the climate they describe. Both cautions argue for revisiting the numbers rather than treating them as fixed.",
            "Readers should know where this section stands on the evidence ladder. The direction of change is established; the pace is estimated; the local consequences are modelled. Statements that blur those levels are the ones most likely to mislead, and they are also the easiest to check.",
            "Two limits apply. The first is scale: global figures say little about a district, and district figures are often unavailable. The second is time: the record is long enough to detect a trend but not long enough to rule out rare extremes. Good planning treats both as design constraints rather than reasons to postpone.",
            "It is worth separating what would change the conclusion from what would merely add detail. A revision of the observed trend, or evidence that adaptation is failing faster than expected, would matter; another confirmation of the same direction would not. That test keeps attention on the claims that carry weight.",
        ],
        "synthesis": [
            "Taken together, the mechanism, the observed record and the institutional response describe a risk that is measurable but not fixed. The practical question is not whether the trend is real, but which decisions today remain defensible across the full range of projections — and those are usually the decisions that are cheap to reverse.",
            "The strands point in one direction: the physical signal is established, the human consequences depend on exposure and capacity, and the response depends on decisions taken before the event. That sequence is what makes the problem tractable, and what makes delay expensive.",
            "What emerges is less a prediction than a test. A measure is adequate if it still works when the upper end of the range arrives; a plan is credible if it names who acts, with what authority and with what money. Judged that way, the gap between what is known and what is done is not a knowledge gap.",
            "The argument, reduced to its shortest form, is this: the physical signal is robust, the human exposure is uneven, and the response is a choice. Each element rests on evidence of different strength, and the weakest link is not the science but the capacity to act before the event rather than after it.",
            "What the section establishes is narrower than a prediction and firmer than an opinion. It establishes that the direction is known, that the costs of inaction are concentrated on those least able to bear them, and that the available measures are known well enough to be tested.",
            "None of this settles the political question of how much to spend and who should pay. It does settle a prior question: whether there is anything worth spending on. The evidence says there is, and that the returns depend on acting while the options are still open.",
        ],
        "priority": [
            "Three priorities follow. First, {b1}. Second, {b2}. Third, {b3}.",
            "The practical agenda reduces to three moves. First, {b1}. Second, {b2}. Third, {b3}.",
            "If this section has an operational core, it is this. First, {b1}. Second, {b2}. Third, {b3}.",
        ],
        "chapter_open": [
            "This chapter examines {T}. It moves from mechanism to evidence to what can be done, and each section states its main claim before the supporting material. Where the evidence is uncertain, the text says so; where it is strong, the language is correspondingly direct.",
            "The subject of this chapter is {T}. The argument proceeds in three steps: what is happening, how we know, and what follows for decisions. Sources are cited as they are used, and contested points are marked as contested rather than presented as settled.",
            "This chapter deals with {T}. Each section opens with a claim, tests it against the evidence and draws out the implication for the people who have to act on it. The aim is not completeness but a defensible line through a large literature.",
            "What follows concerns {T}. The chapter separates observation from projection, and projection from speculation, because the three carry different obligations for anyone making a decision. Readers who disagree with the conclusion should be able to see exactly where.",
        ],
    },
    "id": {
        "expert_a": "Seperti dikemukakan {name} ({year}), {quote}",
        "expert_b": "{name} ({year}) menyatakannya lugas: {quote}",
        "expert_close": [
            "Klaimnya menyangkut waktu sama besar dengan besaran.",
            "Itu peringatan tentang mahalnya penundaan, bukan ramalan kehancuran.",
            "Itu argumen tentang bentuk risikonya, bukan hanya ukurannya.",
            "Dibaca cermat, itu pernyataan tentang apa yang harus diputuskan sekarang.",
        ],
        "news": [
            "Penanda terbaru mengarah ke hal yang sama: {news}.",
            "Pemberitaan terkini menambah rincian, bukan arah baru: {news}.",
            "Laporan terbaru memperkuat gambaran yang sudah ada: {news}.",
        ],
        "limit": [
            "Bukti tidak bulat soal laju dan rincian wilayah, dan celahnya harus disebut, bukan dihaluskan. Ketika perkiraan berbeda, perbedaannya biasanya kembali ke asumsi emisi, adaptasi dan pengukuran. Itu tidak melemahkan alasan bertindak; itu menetapkan rentang agar tindakan tetap kokoh.",
            "Kepastiannya tidak merata dalam literatur ini. Deteksi kukuh, proyeksi bersyarat, dan perkiraan biaya bergantung pada pilihan yang belum diambil. Pembaca yang mencari satu angka akan kecewa; pembaca yang mencari keputusan yang dapat dipertahankan sudah punya bahannya.",
            "Ada dua catatan untuk seluruh bagian ini. Pertama, sebagian besar angka adalah agregat, dan agregat tidak berpindah mulus antarnegara atau antarkelurahan. Kedua, perkiraan yang terbit selalu tertinggal dari iklim yang digambarkannya. Keduanya menuntut peninjauan ulang, bukan penerimaan sebagai angka tetap.",
            "Pembaca perlu tahu di mana bagian ini berdiri pada tangga bukti. Arah perubahannya mapan; lajunya diperkirakan; akibat lokalnya dimodelkan. Pernyataan yang mengaburkan tingkat-tingkat itu adalah yang paling mudah menyesatkan, dan juga paling mudah diperiksa.",
            "Ada dua batas. Pertama skala: angka global hanya sedikit berbicara tentang satu kecamatan, dan angka kecamatan sering tidak tersedia. Kedua waktu: catatannya cukup panjang untuk mendeteksi tren, tetapi tidak cukup untuk menyingkirkan ekstrem yang jarang. Perencanaan yang baik memperlakukan keduanya sebagai batasan desain, bukan alasan menunda.",
            "Ada baiknya memisahkan apa yang akan mengubah kesimpulan dari apa yang hanya menambah rincian. Revisi atas tren yang teramati, atau bukti bahwa adaptasi gagal lebih cepat dari perkiraan, akan penting; konfirmasi lain atas arah yang sama tidak. Ujian itu menjaga perhatian pada klaim yang berbobot.",
        ],
        "synthesis": [
            "Digabungkan, mekanisme, catatan pengamatan dan respons institusi menggambarkan risiko yang terukur tetapi tidak tetap. Pertanyaan praktisnya bukan apakah trennya nyata, melainkan keputusan mana hari ini yang tetap dapat dipertahankan pada seluruh rentang proyeksi — dan itu biasanya keputusan yang murah untuk dibalik.",
            "Semua helai itu menunjuk arah yang sama: sinyal fisiknya mapan, akibat manusianya bergantung pada paparan dan kapasitas, dan responsnya bergantung pada keputusan sebelum peristiwa. Urutan itulah yang membuat masalahnya dapat dikelola, dan yang membuat penundaan mahal.",
            "Yang muncul bukan sekadar ramalan, melainkan ujian. Sebuah tindakan memadai jika tetap bekerja saat ujung atas rentang tiba; sebuah rencana kredibel jika menyebut siapa bertindak, dengan kewenangan apa dan dengan uang apa. Dinilai begitu, jarak antara yang diketahui dan yang dikerjakan bukanlah jarak pengetahuan.",
            "Argumennya, dalam bentuk terpendek, adalah ini: sinyal fisiknya kukuh, paparan manusianya tidak merata, dan responsnya adalah pilihan. Setiap unsur bertumpu pada bukti dengan kekuatan berbeda, dan mata rantai terlemahnya bukan ilmu pengetahuan melainkan kapasitas untuk bertindak sebelum peristiwa, bukan sesudahnya.",
            "Yang ditetapkan bagian ini lebih sempit daripada ramalan dan lebih kukuh daripada pendapat. Ia menetapkan bahwa arahnya diketahui, bahwa biaya kelambanan terkonsentrasi pada mereka yang paling tidak mampu menanggungnya, dan bahwa tindakan yang tersedia cukup dikenal untuk diuji.",
            "Semua ini tidak menyelesaikan pertanyaan politik tentang berapa yang harus dibelanjakan dan siapa yang membayar. Yang diselesaikan adalah pertanyaan sebelumnya: apakah ada sesuatu yang layak dibiayai. Buktinya mengatakan ada, dan bahwa imbal hasilnya bergantung pada bertindak selagi pilihan masih terbuka.",
        ],
        "priority": [
            "Tiga prioritas mengikuti. Pertama, {b1}. Kedua, {b2}. Ketiga, {b3}.",
            "Agenda praktisnya menyusut menjadi tiga langkah. Pertama, {b1}. Kedua, {b2}. Ketiga, {b3}.",
            "Jika bagian ini punya inti operasional, inilah dia. Pertama, {b1}. Kedua, {b2}. Ketiga, {b3}.",
        ],
        "chapter_open": [
            "Bab ini membahas {T}. Pembahasannya bergerak dari mekanisme ke bukti lalu ke tindakan, dan setiap bagian menyatakan klaim utamanya sebelum bahan pendukung. Ketika buktinya tidak pasti, teks menyebutnya; ketika kuat, bahasanya sepadan.",
            "Pokok bahasan bab ini adalah {T}. Argumennya berjalan tiga langkah: apa yang terjadi, bagaimana kita tahu, dan apa akibatnya bagi keputusan. Sumber dikutip saat dipakai, dan titik yang diperdebatkan ditandai sebagai perdebatan, bukan disajikan sebagai kesepakatan.",
            "Bab ini membahas {T}. Setiap bagian dibuka dengan klaim, diuji terhadap bukti, lalu diturunkan implikasinya bagi pihak yang harus bertindak. Tujuannya bukan kelengkapan, melainkan garis yang dapat dipertahankan menembus literatur yang luas.",
            "Yang berikut menyangkut {T}. Bab ini memisahkan pengamatan dari proyeksi, dan proyeksi dari spekulasi, karena ketiganya membawa kewajiban berbeda bagi siapa pun yang mengambil keputusan. Pembaca yang tidak setuju dengan kesimpulannya seharusnya dapat melihat persis di mana.",
        ],
    },
}

# ------------------------------------------------ bab 1 (khusus, ditulis) ---
CH1 = {
    "en": [
        [
            "The case for this book is narrow and deliberately so. It does not argue that the future is known, only that the physical direction of warming is settled while the consequences remain a matter of decision, capacity and timing (IPCC, 2023). Most public argument treats those as one question, which is why debate oscillates between fatalism and delay.",
            "What follows from the distinction is a different kind of book. Rather than forecasting a single future, it sets out what is already measured, what is plausibly projected, and what can still be protected. Each chapter separates those registers so that a reader can see where the evidence is strong, where it is conditional and where it runs out.",
            "Success is not measured by agreement. It is measured by whether a reader can take a claim, check it against the cited source, and decide what to do in a household, a city or an institution. That is a lower ambition than prediction, and a more useful one.",
        ],
        [
            "'Survive' is used here in a plain sense: to keep the essentials of a life intact through disruption — water, food, shelter, health, income and the social ties that make recovery possible.",
            "That definition rules out two common shortcuts. One treats survival as individual stockpiling, which fails when systems fail together. The other treats it as purely collective, which leaves households unprepared for the days before help arrives. The disaster record shows that both matter, and that the difference between a bad week and a permanent loss is usually local capacity (UNDRR, 2015).",
            "Survival, on this account, is not a bunker. It is a set of arrangements — some physical, some institutional, some social — that keep options open when conditions change faster than expected.",
        ],
        [
            "The book can be read straight through or used as a reference. Chapters 1-3 establish the physical and institutional baseline; chapters 4-13 work through the main impact domains; chapters 14-21 turn to knowledge, preparedness and governance; chapters 22-23 examine regional cases; chapter 24 collects the practical material.",
            "Each chapter follows the same architecture: an opening claim, four analytical sections, a case study and a scenario table. The tables can be compared across chapters, and references are consolidated in Appendix D so that a claim can be traced without hunting through footnotes.",
            "Readers in a hurry can start with the scenario table at the end of a chapter and work backwards. Readers using the book for teaching can pair the case studies with the checklists in chapter 24. Neither route requires accepting the argument whole.",
        ],
        [
            "The scope is wide but not unlimited. The book deals with climate-driven risks to human welfare — heat, water, food, health, shelter, displacement, conflict and the fiscal capacity to respond — and with the measures that reduce them.",
            "It does not attempt a full account of every Earth-system change, nor a complete economics of decarbonisation. Those are treated where they bear on survival and cited rather than summarised at length.",
            "The boundary is deliberate: a book that tried to cover everything would explain nothing in usable detail. What is claimed here is narrower — that the risks are documented, the responses are known, and the gap between them is a decision rather than a mystery.",
        ],
    ],
    "id": [
        [
            "Alasan buku ini sempit, dan memang disengaja. Buku ini tidak berargumen bahwa masa depan sudah diketahui, hanya bahwa arah fisik pemanasan sudah pasti sementara akibatnya masih bergantung pada keputusan, kapasitas dan waktu (IPCC, 2023). Perdebatan publik sering mencampur keduanya, karena itu ia berayun antara fatalisme dan penundaan.",
            "Dari pembedaan itu lahir buku yang berbeda. Alih-alih meramalkan satu masa depan, buku ini memaparkan apa yang sudah terukur, apa yang plausibel diproyeksikan, dan apa yang masih dapat dilindungi. Setiap bab memisahkan ketiga lapis itu agar pembaca melihat di mana buktinya kuat, di mana bersyarat, dan di mana habis.",
            "Keberhasilan tidak diukur dari kesepakatan, melainkan dari apakah pembaca dapat mengambil satu klaim, memeriksanya pada sumber yang dikutip, dan memutuskan apa yang harus dilakukan di rumah tangga, kota atau institusinya. Ambisi itu lebih rendah daripada ramalan, dan lebih berguna.",
        ],
        [
            "'Bertahan' dipakai di sini dalam arti sederhana: menjaga hal-hal pokok kehidupan tetap utuh saat terjadi gangguan — air, pangan, hunian, kesehatan, pendapatan dan ikatan sosial yang memungkinkan pemulihan.",
            "Definisi itu menyingkirkan dua jalan pintas yang umum. Satu memperlakukan bertahan sebagai menimbun sendiri, yang gagal ketika sistem runtuh bersamaan. Yang lain memperlakukannya sebagai urusan kolektif semata, yang membuat rumah tangga tidak siap menghadapi hari-hari sebelum bantuan datang. Catatan bencana menunjukkan keduanya penting, dan bahwa pembeda antara seminggu yang buruk dan kehilangan permanen biasanya adalah kapasitas lokal (UNDRR, 2015).",
            "Bertahan, dalam pengertian ini, bukan bunker. Ia adalah seperangkat pengaturan — sebagian fisik, sebagian institusional, sebagian sosial — yang menjaga pilihan tetap terbuka ketika kondisi berubah lebih cepat dari perkiraan.",
        ],
        [
            "Buku ini dapat dibaca runtut atau dipakai sebagai rujukan. Bab 1-3 meletakkan dasar fisik dan institusional; bab 4-13 menelusuri ranah dampak utama; bab 14-21 beralih ke pengetahuan, kesiapsiagaan dan tata kelola; bab 22-23 menelaah kasus regional; bab 24 menghimpun bahan praktis.",
            "Setiap bab mengikuti arsitektur yang sama: klaim pembuka, empat bagian analitis, studi kasus dan tabel skenario. Tabelnya dapat dibandingkan antarbab, dan rujukannya dihimpun di Lampiran D sehingga klaim dapat ditelusuri tanpa mencari-cari catatan kaki.",
            "Pembaca yang tergesa dapat mulai dari tabel skenario di akhir bab lalu bergerak mundur. Pembaca yang memakai buku ini untuk mengajar dapat memasangkan studi kasus dengan daftar periksa di bab 24. Kedua jalur tidak menuntut penerimaan utuh atas argumennya.",
        ],
        [
            "Lingkupnya luas tetapi tidak tanpa batas. Buku ini membahas risiko iklim bagi kesejahteraan manusia — panas, air, pangan, kesehatan, hunian, pengungsian, konflik dan kapasitas fiskal untuk merespons — serta tindakan yang menguranginya.",
            "Buku ini tidak berusaha mencatat seluruh perubahan sistem Bumi, juga tidak menyajikan ekonomi dekarbonisasi secara lengkap. Hal-hal itu dibahas sejauh menyangkut bertahan hidup, dan dikutip ketimbang diringkas panjang lebar.",
            "Batasnya disengaja: buku yang mencoba mencakup segalanya akan menjelaskan apa pun tanpa rincian yang dapat dipakai. Yang diklaim di sini lebih sempit — bahwa risikonya terdokumentasi, responsnya diketahui, dan jarak di antaranya adalah keputusan, bukan misteri.",
        ],
    ],
}

# --------------------------------------------------- praktik (bab 24) ------
PRACTICE = {
    "en": [
        [
            "{S} is only useful if it can be executed under stress, and stress is exactly when detail is lost. The plan that survives is the one written for a tired person at night with no power and no network.",
            "The common failure is not ambition but vagueness. 'Prepare a kit' means nothing at 2 a.m.; 'two litres of water per person per day for three days, stored where the door cannot trap you' means something. Specificity is the difference between a document and a capability.",
            "Review matters more than design. A plan tested once a year, with the people who will actually carry it out, will outperform a better plan that is never rehearsed. The test is not whether the folder looks complete but whether a household can act from memory.",
        ],
        [
            "{S} works at the scale of a street or a building, not a municipality. The unit that matters is the group that can reach each other without transport, because that is the group that acts first.",
            "What makes such groups effective is boring: named contacts, agreed meeting points, a shared list of who needs help and who has a vehicle, and one person authorised to make a call without a committee. Trust is built by doing small things together before it is needed.",
            "Sustainability depends on rotating responsibility. Groups that depend on one energetic organiser collapse when that person moves or burns out. Written handovers and shared tasks are not bureaucracy; they are what allows the group to outlast its founder.",
        ],
        [
            "{S} should be short enough to use and specific enough to check. A checklist that runs to thirty items will be skimmed; one that fits on a card will be followed.",
            "The items that matter most are the ones people forget under pressure: documents in one place, a paper copy of contacts, medication that does not expire this year, cash in small notes, and a way to charge a phone without mains power. Each is cheap; each is routinely missing.",
            "Checklists also serve a social function. Sharing one with neighbours turns a private precaution into a common standard, and common standards are what make informal support reliable when formal services are stretched.",
        ],
        [
            "{S} are tools for thinking, not forms to file. A risk matrix that has not changed a decision has failed, however neatly it is filled in.",
            "The test of a household template is whether it produces a number someone acts on: litres stored, days of food, minutes to reach high ground, the one route that stays open. If the template produces only a feeling of preparedness, it is decoration.",
            "Templates should be revised after every real event and every near miss. The revision is the learning; the document is only its memory.",
        ],
    ],
    "id": [
        [
            "{S} hanya berguna jika dapat dijalankan saat tertekan, dan justru saat itulah rincian hilang. Rencana yang bertahan adalah rencana yang ditulis untuk orang lelah di malam hari tanpa listrik dan tanpa jaringan.",
            "Kegagalan yang umum bukan ambisi, melainkan kesamaran. 'Siapkan tas siaga' tidak berarti apa-apa pukul dua pagi; 'dua liter air per orang per hari untuk tiga hari, disimpan di tempat yang tidak menjebak pintu' berarti sesuatu. Kekhususan adalah pembeda antara dokumen dan kemampuan.",
            "Peninjauan lebih penting daripada desain. Rencana yang diuji setahun sekali bersama orang yang benar-benar akan menjalankannya akan mengalahkan rencana lebih bagus yang tidak pernah dilatih. Ujiannya bukan apakah foldernya terlihat lengkap, melainkan apakah sebuah rumah tangga dapat bertindak dari ingatan.",
        ],
        [
            "{S} bekerja pada skala gang atau gedung, bukan kotamadya. Unit yang penting adalah kelompok yang dapat saling menjangkau tanpa kendaraan, karena itulah yang bertindak lebih dulu.",
            "Yang membuat kelompok semacam itu efektif justru membosankan: kontak yang bernama, titik temu yang disepakati, daftar bersama tentang siapa perlu bantuan dan siapa punya kendaraan, serta satu orang yang berwenang memutuskan tanpa rapat. Kepercayaan dibangun dengan mengerjakan hal-hal kecil bersama sebelum dibutuhkan.",
            "Keberlanjutan bergantung pada rotasi tanggung jawab. Kelompok yang bergantung pada satu penggerak akan runtuh ketika orang itu pindah atau kehabisan tenaga. Serah terima tertulis dan tugas bersama bukan birokrasi; itulah yang membuat kelompok bertahan melampaui pendirinya.",
        ],
        [
            "{S} harus cukup singkat untuk dipakai dan cukup rinci untuk diperiksa. Daftar berisi tiga puluh item akan dipindai; daftar seukuran kartu akan diikuti.",
            "Butir yang paling penting adalah yang dilupakan orang saat tertekan: dokumen di satu tempat, salinan kontak di kertas, obat yang tidak kedaluwarsa tahun ini, uang tunai pecahan kecil, dan cara mengisi daya telepon tanpa listrik. Semuanya murah; semuanya rutin tidak ada.",
            "Daftar periksa juga berfungsi sosial. Membagikannya kepada tetangga mengubah kehati-hatian pribadi menjadi standar bersama, dan standar bersama itulah yang membuat dukungan informal dapat diandalkan ketika layanan formal sedang terbatas.",
        ],
        [
            "{S} adalah alat berpikir, bukan formulir untuk diarsipkan. Matriks risiko yang tidak mengubah satu keputusan pun telah gagal, seberapa rapi pun isinya.",
            "Ujian template rumah tangga adalah apakah ia menghasilkan angka yang ditindaklanjuti: liter yang tersimpan, hari pangan, menit menuju tanah tinggi, satu jalur yang tetap terbuka. Jika template hanya menghasilkan rasa siap, ia hiasan.",
            "Template harus direvisi setelah setiap peristiwa nyata dan setiap nyaris celaka. Revisinya adalah pembelajarannya; dokumennya hanya ingatan.",
        ],
    ],
}


# ---------------------------------------------------------------- builder ---
def _data_sentence(dp):
    return dp


def section_paragraphs(lang, ci, si, sec_title, theme, data_points, bullets,
                       n_variants=4):
    """Kembalikan daftar paragraf untuk satu sub-bab topik."""
    if ci == 1:
        return CH1[lang][si - 1]
    if ci == 24:
        text = PRACTICE[lang][si - 1]
        return [p.replace("{S}", np_of(sec_title, lang)) for p in text]

    lens_pool = LENS_BY_CHAPTER[ci]
    dom = DOMAINS[lang][ci - 1]
    np_ = np_of(sec_title, lang)
    picks = DATA_PICK[ci - 1]

    out = []
    for k in range(4):
        lens = lens_pool[(si - 1 + k) % len(lens_pool)]
        variant = (ci + si + k * 2) % len(LENS[lang][lens])
        dp = data_points[picks[(si + k) % len(picks)]]
        paras = LENS[lang][lens][variant]
        body = " ".join(p.format(S=np_, D=dp, DOM=dom) for p in paras)
        tag = "Bagi " + dom if lang == "id" else "For " + dom
        if tag in body:
            para = body             # paragraf sudah punya implikasi domain
        else:
            close = LENS_CLOSE[lang][(ci + si + k) % 4].format(DOM=dom)
            para = body + " " + close
        out.append(vary_dom(para, lang, dom, ci * 3 + si + k))
    return out


def expert_lead(lang, name, year, quote, ci, si):
    f = FRAMES[lang]
    tpl = f["expert_a"] if (ci + si) % 3 else f["expert_b"]
    return tpl.format(name=name, year=year, quote=quote)


NEWS_KEYS = {
    2: ("temperature", "hottest", "ice", "glacier", "record"),
    3: ("ice", "temperature", "record", "sea level", "ocean"),
    4: ("heat", "heatwave", "temperature"),
    5: ("drought", "water", "river", "rain"),
    6: ("flood", "sea level", "cyclone", "storm", "rain"),
    7: ("crop", "wheat", "food", "harvest", "olive"),
    8: ("coral", "wildfire", "forest", "ecosystem"),
    9: ("heat", "deaths", "disease", "health"),
    10: ("billion", "damage", "cost", "disaster"),
    11: ("displaced", "evacuat", "refugee", "people"),
    12: ("conflict", "displac", "food"),
    13: ("dam", "infrastructure", "power", "flood"),
    14: ("heat", "school", "record"),
    15: ("record", "data", "temperature"),
    16: ("heat", "water", "flood"),
    17: ("heat", "deaths", "health", "cyclone"),
    18: ("displaced", "community", "people"),
    19: ("solar", "energy", "power"),
    20: ("heat", "deaths", "anxiety"),
    21: ("damage", "billion", "finance"),
    22: ("heat", "fire", "flood", "cyclone", "storm"),
    23: ("drought", "food", "water", "conflict", "displaced"),
    24: ("heat", "water", "flood"),
}


def pick_news(ci, si, news_list):
    keys = NEWS_KEYS.get(ci, ())
    if not keys:
        return news_list[(ci * 4 + si) % len(news_list)]
    scored = []
    for i, n in enumerate(news_list):
        low = n.lower()
        score = sum(1 for k in keys if k in low)
        if score:
            scored.append((score, i))
    if not scored:
        return news_list[(ci * 4 + si) % len(news_list)]
    scored.sort(reverse=True)
    top = [i for s, i in scored if s == scored[0][0]]
    return news_list[top[(ci + si) % len(top)]]


NEWS_READ = {
    "en": [
        "Read against the longer record, it is an illustration rather than a proof.",
        "On its own it proves little; placed against the trend it shows the direction of travel.",
        "The value of such reports is that they date the change rather than explain it.",
        "Taken alone the episode is weather; taken with the record it is a data point on a slope.",
        "It matters less as a record than as evidence that the baseline has already moved.",
        "The item is useful because it fixes a date to a trend that otherwise drifts.",
        "Treated as a single observation it invites over-reading; treated as one of many it is informative.",
        "What the report adds is timing, not a new mechanism.",
        "It is one line in a longer ledger, and the ledger is what matters.",
        "The event is best read as a measurement, not as a verdict.",
        "Set beside the record, the episode indicates direction without fixing the rate.",
        "Reported in isolation the figure looks dramatic; reported against the baseline it looks consistent.",
    ],
    "id": [
        "Dibaca terhadap rekam yang lebih panjang, ia adalah ilustrasi, bukan bukti.",
        "Sendiri, laporan itu sedikit membuktikan; ditempatkan pada tren, ia menunjukkan arah perjalanan.",
        "Nilainya adalah menanggalkan perubahan pada tanggal tertentu, bukan menjelaskannya.",
        "Jika berdiri sendiri, peristiwanya adalah cuaca; jika dibaca bersama rekamannya, ia titik data pada sebuah lereng.",
        "Yang penting bukan rekornya, melainkan bukti bahwa garis dasar sudah bergerak.",
        "Berita itu berguna karena menambatkan tanggal pada tren yang jika tidak begitu akan mengambang.",
        "Sebagai satu pengamatan ia mengundang tafsir berlebih; sebagai satu dari banyak, ia informatif.",
        "Yang ditambahkan laporan itu adalah waktu, bukan mekanisme baru.",
        "Ia satu baris dalam buku catatan yang lebih panjang, dan buku catatan itulah yang penting.",
        "Peristiwa itu paling baik dibaca sebagai pengukuran, bukan sebagai putusan.",
        "Diletakkan di samping rekamannya, peristiwa itu menunjukkan arah tanpa memastikan lajunya.",
        "Dilaporkan sendiri, angkanya tampak dramatis; dibandingkan garis dasarnya, ia tampak konsisten.",
    ],
}

NEWS_CLOSE = {
    "en": [
        "For {DOM}, the report is a reminder that the response is being designed against a target that keeps moving.",
        "For {DOM}, what matters is not the record but the lead time it implies.",
        "For {DOM}, the item is useful mainly as a date stamp on a trend.",
    ],
    "id": [
        "Bagi {DOM}, laporan itu mengingatkan bahwa garis dasar bergerak selagi respons masih dirancang.",
        "Bagi {DOM}, yang penting bukan rekornya melainkan waktu peringatan yang tersirat di dalamnya.",
        "Bagi {DOM}, berita itu berguna terutama sebagai penanda tanggal pada sebuah tren.",
    ],
}


def news_paragraph(lang, news, ci, si):
    tpl = FRAMES[lang]["news"][(ci * 3 + si) % 3]
    read = NEWS_READ[lang][(ci + si * 2) % len(NEWS_READ[lang])]
    close = NEWS_CLOSE[lang][(ci + si) % 3].format(DOM=DOMAINS[lang][ci - 1])
    return " ".join([tpl.format(news=news), read, close])


def limit_paragraph(lang, ci, si):
    return (FRAMES[lang]["limit"][(ci * 5 + si * 7) % 6] + " "
            + DOM_CLOSE[lang]["limit"].format(DOM=DOMAINS[lang][ci - 1]))


def synthesis_paragraph(lang, ci, si):
    return (FRAMES[lang]["synthesis"][(ci * 5 + si * 7) % 6] + " "
            + DOM_CLOSE[lang]["synth"].format(DOM=DOMAINS[lang][ci - 1]))


def priority_paragraph(lang, bullets, ci, si):
    tpl = FRAMES[lang]["priority"][(ci + si) % 3]
    b = [x.lower().rstrip(".") for x in bullets[:3]]
    return tpl.format(b1=b[0], b2=b[1], b3=b[2])


def chapter_opening(lang, ci, theme):
    return FRAMES[lang]["chapter_open"][(ci - 1) % 4].format(T=theme)


# ------------------------------------------------ varian ketiga (Gate 3) ---
LENS["en"]["framing"].append([
    "It helps to ask what question {S} is really answering.",
    "Framed as a measurement problem, it invites better instruments; framed as a decision problem, it invites better institutions (IPCC, 2023).",
    "The difference is practical, because the second framing admits trade-offs that the first hides.",
    "The scale is already visible: {D}.",
    "For {DOM}, the choice of framing determines which options are considered at all.",
    "A question that excludes trade-offs will produce an answer that cannot be implemented.",
])
LENS["en"]["evidence"].append([
    "The evidence base for {S} is broad but uneven, and the unevenness is informative.",
    "Where many independent studies agree, confidence is high; where a single model family supplies the estimate, it is not (IPCC, 2021).",
    "One figure illustrates the state of knowledge: {D}.",
    "The appropriate response to a strong signal with weak local detail is not to wait for precision but to design for the range.",
    "For {DOM}, that means carrying uncertainty into the decision rather than resolving it beforehand.",
    "Plans that require certainty before acting are plans that act late.",
])
LENS["en"]["causal"].append([
    "The chain of causation is short enough to follow and long enough to intervene in.",
    "Physical change alters the frequency and intensity of events; exposure determines who meets them; capacity determines what happens next (IPCC, 2022).",
    "Because the links are separable, they can be addressed separately — and the cheapest link is usually exposure.",
    "The pattern is not hypothetical: {D}.",
    "For {DOM}, the lesson is to intervene where the leverage is greatest rather than where the damage is most visible.",
    "Response is necessary; prevention is cheaper.",
])
LENS["en"]["distribution"].append([
    "The distribution of harm is not a detail appended to the analysis; it is the analysis.",
    "Two households can face the same event and emerge with different futures, because what they own, owe and can claim determines recovery (IPCC, 2022).",
    "The aggregate picture obscures this: {D}.",
    "For that reason, average-based targets can be met while the most exposed end up worse off.",
    "For {DOM}, the measures that matter are those judged by their effect on the bottom of the distribution, not the middle.",
    "That is also the test of whether a policy is serious.",
])
LENS["en"]["institutions"].append([
    "Institutional capacity is what turns a warning into an evacuation and a budget line into a working shelter.",
    "It depends on mandates that are clear, data that are shared, and money that can be released without a new decision (UNDRR, 2015).",
    "Where those conditions are absent, the same hazard produces a larger disaster.",
    "The stakes are visible in the numbers: {D}.",
    "For {DOM}, capability is better tested in a drill than in a document.",
    "A plan that has never been exercised is a hypothesis.",
])
LENS["en"]["cost"].append([
    "The case for spending early rests on a comparison that is rarely made explicit: prevention against recovery, over decades rather than one budget cycle.",
    "Damage functions and observed recovery costs point the same way (World Bank, 2022).",
    "The order of magnitude is contested in detail but not in direction: {D}.",
    "Prevention loses politically because its benefits are invisible: the disaster that did not happen has no constituency.",
    "For {DOM}, the fix is institutional — budget rules that reserve funds for prevention, and appraisal that counts avoided losses.",
    "Otherwise the arithmetic is sound and the incentives are not.",
])
LENS["en"]["uncertainty"].append([
    "An honest account of {S} distinguishes three things: what has been measured, what has been modelled, and what has been assumed.",
    "Most public confusion comes from collapsing the three into one sentence (IPCC, 2021).",
    "The distinction is concrete: {D}.",
    "Numbers carry confidence intervals, and those intervals should travel with them into any decision.",
    "For {DOM}, the discipline is to write the interval next to the estimate whenever the estimate is used.",
    "A disclosed range can be planned against; an undisclosed point estimate cannot.",
])
LENS["en"]["decision"].append([
    "The relevant question for {S} is not what will happen but what to do while the answer is still forming.",
    "That favours measures that are cheap, reversible and useful across several futures.",
    "Early warning, insurance, redundant systems and protected water sources meet that test; megaprojects tied to one scenario do not (IPCC, 2023).",
    "Pressure is building regardless: {D}.",
    "For {DOM}, the portfolio matters more than any single measure.",
    "Robustness, not optimality, is the right criterion under uncertainty.",
])

LENS["id"]["framing"].append([
    "Ada baiknya bertanya: pertanyaan apa yang sebenarnya dijawab {S}.",
    "Sebagai masalah pengukuran, ia menuntut instrumen yang lebih baik; sebagai masalah keputusan, ia menuntut institusi yang lebih baik (IPCC, 2023).",
    "Perbedaannya praktis, karena bingkai kedua mengakui trade-off yang disembunyikan bingkai pertama.",
    "Skalanya sudah terlihat: {D}.",
    "Bagi {DOM}, pilihan bingkai menentukan opsi mana yang dipertimbangkan sama sekali.",
    "Pertanyaan yang menyingkirkan trade-off akan menghasilkan jawaban yang tidak dapat dijalankan.",
])
LENS["id"]["evidence"].append([
    "Basis bukti {S} luas tetapi tidak rata, dan ketidakrataannya informatif.",
    "Ketika banyak studi independen sepakat, keyakinannya tinggi; ketika satu keluarga model saja yang memasok perkiraan, tidak (IPCC, 2021).",
    "Satu angka menggambarkan keadaan pengetahuan: {D}.",
    "Jawaban yang tepat atas sinyal kuat dengan rincian lokal lemah bukan menunggu ketepatan, melainkan merancang untuk rentang.",
    "Bagi {DOM}, artinya membawa ketidakpastian ke dalam keputusan, bukan menyelesaikannya lebih dulu.",
    "Rencana yang menuntut kepastian sebelum bertindak adalah rencana yang bertindak terlambat.",
])
LENS["id"]["causal"].append([
    "Rantai sebab-akibatnya cukup pendek untuk diikuti dan cukup panjang untuk disela.",
    "Perubahan fisik mengubah frekuensi dan intensitas peristiwa; paparan menentukan siapa yang bertemu; kapasitas menentukan apa yang terjadi sesudahnya (IPCC, 2022).",
    "Karena mata rantainya terpisah, ia dapat ditangani terpisah — dan mata rantai termurah biasanya paparan.",
    "Polanya bukan hipotetis: {D}.",
    "Bagi {DOM}, pelajarannya adalah menyela di titik dengan daya ungkit terbesar, bukan di titik kerusakan paling terlihat.",
    "Respons perlu; pencegahan lebih murah.",
])
LENS["id"]["distribution"].append([
    "Sebaran kerugian bukan rincian tambahan pada analisis; ia adalah analisisnya.",
    "Dua rumah tangga dapat menghadapi peristiwa yang sama dan keluar dengan masa depan berbeda, karena apa yang dimiliki, diutang dan dapat diklaim menentukan pemulihan (IPCC, 2022).",
    "Gambaran agregat menyembunyikannya: {D}.",
    "Karena itu, target berbasis rata-rata dapat tercapai sementara yang paling terpapar justru memburuk.",
    "Bagi {DOM}, yang dibutuhkan adalah tindakan yang dinilai dari dampaknya pada ujung bawah sebaran, bukan tengahnya.",
    "Itu juga ujian apakah sebuah kebijakan serius.",
])
LENS["id"]["institutions"].append([
    "Kapasitas institusi adalah yang mengubah peringatan menjadi evakuasi dan baris anggaran menjadi tempat berlindung yang berfungsi.",
    "Itu bergantung pada mandat yang jelas, data yang dibagi, dan uang yang dapat dicairkan tanpa keputusan baru (UNDRR, 2015).",
    "Ketika syarat itu tidak ada, bahaya yang sama menghasilkan bencana yang lebih besar.",
    "Taruhannya terlihat pada angka: {D}.",
    "Bagi {DOM}, kemampuan lebih baik diuji dalam latihan daripada dalam dokumen.",
    "Rencana yang tidak pernah dilatih hanyalah hipotesis.",
])
LENS["id"]["cost"].append([
    "Alasan berbelanja lebih awal bertumpu pada perbandingan yang jarang dinyatakan: pencegahan melawan pemulihan, dalam hitungan dekade bukan satu siklus anggaran.",
    "Fungsi kerugian dan biaya pemulihan yang teramati menunjuk arah yang sama (World Bank, 2022).",
    "Urutan besarnya diperdebatkan dalam rincian, tetapi tidak dalam arah: {D}.",
    "Pencegahan kalah secara politik karena manfaatnya tak terlihat: bencana yang tidak terjadi tidak punya konstituen.",
    "Bagi {DOM}, perbaikannya institusional — aturan anggaran yang menyisihkan dana pencegahan, dan penilaian yang menghitung kerugian yang dihindari.",
    "Tanpa itu, hitungannya benar tetapi insentifnya tidak.",
])
LENS["id"]["uncertainty"].append([
    "Uraian yang jujur tentang {S} memisahkan tiga hal: yang sudah diukur, yang dimodelkan, dan yang diasumsikan.",
    "Sebagian besar kebingungan publik muncul dari mencampur ketiganya dalam satu kalimat (IPCC, 2021).",
    "Perbedaannya konkret: {D}.",
    "Angka membawa interval keyakinannya, dan interval itu harus ikut ke dalam setiap keputusan.",
    "Bagi {DOM}, disiplinnya adalah menuliskan interval di samping perkiraan setiap kali perkiraan dipakai.",
    "Rentang yang dinyatakan dapat direncanakan; perkiraan titik yang tidak dinyatakan tidak.",
])
LENS["id"]["decision"].append([
    "Pertanyaan relevan bagi {S} bukan apa yang akan terjadi, melainkan apa yang harus dilakukan selagi jawabannya belum terbentuk.",
    "Itu menguntungkan tindakan yang murah, dapat dibalik dan berguna pada beberapa masa depan sekaligus.",
    "Peringatan dini, asuransi, sistem redundan dan sumber air yang dilindungi lolos ujian itu; proyek raksasa yang terikat satu skenario tidak (IPCC, 2023).",
    "Tekanannya tetap membangun: {D}.",
    "Bagi {DOM}, portofolio lebih penting daripada satu tindakan.",
    "Ketangguhan, bukan keoptimalan, adalah kriteria yang tepat di bawah ketidakpastian.",
])

for _lang in ("en", "id"):
    for _lens_name in LENS[_lang]:
        assert len(LENS[_lang][_lens_name]) == 3, (_lang, _lens_name)


# --------------------------------------------------- varian lensa keempat --
VARIANT4 = {
    "en": {
        "framing": [
            "How a problem is framed decides what counts as a solution, and {S} is a case in point.",
            "Framed as an environmental issue, it invites a ministry and a budget line; framed as a development issue, it invites land use, housing and finance at once (IPCC, 2022).",
            "The second framing is harder to administer precisely because it cannot be assigned to a single department.",
            "The scale involved rules out a narrow frame: {D}.",
            "For {DOM}, the practical consequence is that the frame has to be chosen before the plan, not after it.",
            "Frames are cheap to change on paper and expensive to change in an institution.",
        ],
        "evidence": [
            "The evidence base behind {S} is larger than its public profile suggests, and more uneven.",
            "Satellite records, station data, insurance claims and household surveys answer different questions, and they rarely agree on the same decimal place (IPCC, 2021).",
            "Where they disagree, the disagreement is usually about coverage rather than about the direction of change.",
            "Confidence is highest on aggregates and lowest on localities: {D}.",
            "For {DOM}, the sensible use of the record is to establish direction and then test local plausibility rather than to import a global average wholesale.",
            "A number that cannot be traced to a source is not evidence; it is decoration.",
        ],
        "causal": [
            "Between the physical change and the harm there is a sequence, and each step can be examined on its own.",
            "A shift in the mean moves the tail of the distribution first; the tail meets exposure; exposure meets capacity; capacity fails at thresholds rather than gradually (IPCC, 2022).",
            "That is why impacts arrive in jumps and why the same event produces different outcomes in neighbouring districts.",
            "The arithmetic of the shift is blunt: {D}.",
            "For {DOM}, the useful question is which threshold comes first and what happens on the day it is crossed.",
            "Thresholds are where a gradual problem becomes a sudden one.",
        ],
        "uncertainty": [
            "Uncertainty in {S} is not a single quantity, and treating it as one is the most common analytic error in the field.",
            "Physical uncertainty, scenario uncertainty and model uncertainty behave differently: the first narrows with data, the second depends on choices, the third on structure (IPCC, 2021).",
            "Only the first is reduced by waiting; the other two are reduced by deciding.",
            "The range is wide enough to matter for planning: {D}.",
            "For {DOM}, the correct response to the wide part of the range is a decision that performs acceptably across it, not a postponement until it narrows.",
            "Plans that require certainty before they begin are plans that begin too late.",
        ],
        "distribution": [
            "The aggregate picture hides the distribution, and in {S} the distribution carries most of the policy content.",
            "Risk is concentrated by geography, tenure and income, and the concentration is produced by prior decisions about land, services and insurance (UNDRR, 2015).",
            "Because those decisions were made deliberately, they can be unmade deliberately.",
            "The unevenness is measurable: {D}.",
            "For {DOM}, averages are the wrong unit of account; the relevant figure is the burden carried by the group least able to carry it.",
            "A policy judged by its average effect will systematically miss the people it is meant to protect.",
        ],
        "institutions": [
            "Institutional performance in {S} depends less on formal authority than on whether mandates, money and information arrive together.",
            "Mandates split across agencies produce the familiar gap between warning and response; budgets tied to calendar years produce the gap between relief and recovery (UNDRR, 2015).",
            "Neither gap requires bad faith, only an ordinary division of labour.",
            "The strain is already visible in the numbers: {D}.",
            "For {DOM}, the design question is where to place the authority that can move money and people within the same week.",
            "Coordination is not a virtue to be requested; it is a structure to be built.",
        ],
        "cost": [
            "The economics of {S} are usually presented as a bill, which is the least useful form in which to present them.",
            "Costs arrive early and are budgeted, while benefits arrive late and are unassigned; the asymmetry systematically biases public investment toward response and away from preparation (World Bank, 2023).",
            "Insurance and credit then transmit that bias into private decisions about where to build and what to protect.",
            "The magnitude is not marginal: {D}.",
            "For {DOM}, the useful accounting separates the cost of preparing from the cost of not preparing, and prices both over the same horizon.",
            "A measure that is expensive against one budget year is often cheap against ten.",
        ],
        "decision": [
            "Anyone deciding about {S} is choosing under conditions that will not improve before the choice has to be made.",
            "That makes sequencing the central skill: measures that are cheap, reversible and useful under several futures go first, and irreversible commitments wait for better information (IPCC, 2022).",
            "The sequence matters because early options buy the time that later options need.",
            "The pressure is documented rather than projected: {D}.",
            "For {DOM}, the test of a plan is not whether it is optimal for one forecast but whether it survives several.",
            "Decisions taken now will be judged by events that were not in the forecast.",
        ],
    },
    "id": {
        "framing": [
            "Cara sebuah masalah dibingkai menentukan apa yang dihitung sebagai solusi, dan {S} adalah contohnya.",
            "Dibingkai sebagai isu lingkungan, ia mengundang satu kementerian dan satu pos anggaran; dibingkai sebagai isu pembangunan, ia mengundang tata guna lahan, perumahan dan keuangan sekaligus (IPCC, 2022).",
            "Bingkai kedua lebih sulit diadministrasikan justru karena tidak dapat ditugaskan kepada satu departemen.",
            "Skala yang terlibat menutup kemungkinan bingkai sempit: {D}.",
            "Bagi {DOM}, konsekuensi praktisnya adalah bingkai harus dipilih sebelum rencana, bukan sesudahnya.",
            "Bingkai murah diubah di atas kertas dan mahal diubah di dalam institusi.",
        ],
        "evidence": [
            "Basis bukti di balik {S} lebih besar daripada profil publiknya, dan lebih tidak rata.",
            "Catatan satelit, data stasiun, klaim asuransi dan survei rumah tangga menjawab pertanyaan berbeda, dan jarang sepakat pada desimal yang sama (IPCC, 2021).",
            "Ketika mereka berbeda, perbedaannya biasanya soal cakupan, bukan soal arah perubahan.",
            "Keyakinan paling tinggi pada agregat dan paling rendah pada lokalitas: {D}.",
            "Bagi {DOM}, penggunaan rekaman yang wajar adalah menetapkan arah lalu menguji kewajaran lokal, bukan mengimpor rata-rata global apa adanya.",
            "Angka yang tidak dapat ditelusuri sumbernya bukan bukti, melainkan hiasan.",
        ],
        "causal": [
            "Antara perubahan fisik dan kerugian ada urutan, dan setiap langkahnya dapat diperiksa sendiri.",
            "Pergeseran rata-rata menggerakkan ekor distribusi lebih dulu; ekor itu bertemu paparan; paparan bertemu kapasitas; kapasitas gagal pada ambang, bukan secara bertahap (IPCC, 2022).",
            "Itulah sebabnya dampak datang melonjak dan mengapa peristiwa yang sama menghasilkan akibat berbeda di distrik yang bersebelahan.",
            "Aritmetika pergeserannya lugas: {D}.",
            "Bagi {DOM}, pertanyaan bergunanya adalah ambang mana yang tiba lebih dulu dan apa yang terjadi pada hari ambang itu dilampaui.",
            "Ambang adalah tempat masalah bertahap berubah menjadi masalah mendadak.",
        ],
        "uncertainty": [
            "Ketidakpastian dalam {S} bukan satu besaran tunggal, dan memperlakukannya sebagai satu besaran adalah kesalahan analitis paling umum di bidang ini.",
            "Ketidakpastian fisik, skenario dan model berperilaku berbeda: yang pertama menyempit dengan data, yang kedua bergantung pada pilihan, yang ketiga pada struktur (IPCC, 2021).",
            "Hanya yang pertama berkurang dengan menunggu; dua lainnya berkurang dengan memutuskan.",
            "Rentangnya cukup lebar untuk mengubah perencanaan: {D}.",
            "Bagi {DOM}, respons yang benar terhadap bagian rentang yang lebar adalah keputusan yang berkinerja memadai di seluruh rentang, bukan penundaan sampai rentang menyempit.",
            "Rencana yang menuntut kepastian sebelum dimulai adalah rencana yang mulai terlambat.",
        ],
        "distribution": [
            "Gambaran agregat menyembunyikan distribusi, dan dalam {S} distribusi itulah yang memuat sebagian besar isi kebijakan.",
            "Risiko terkonsentrasi oleh geografi, status kepemilikan dan pendapatan, dan konsentrasi itu dihasilkan keputusan sebelumnya tentang lahan, layanan dan asuransi (UNDRR, 2015).",
            "Karena keputusan itu diambil dengan sengaja, ia juga dapat dibatalkan dengan sengaja.",
            "Ketidakrataannya terukur: {D}.",
            "Bagi {DOM}, rata-rata adalah satuan hitung yang keliru; angka yang relevan adalah beban yang dipikul kelompok yang paling tidak mampu memikulnya.",
            "Kebijakan yang dinilai dari efek rata-ratanya akan sistematis melewatkan orang yang seharusnya dilindungi.",
        ],
        "institutions": [
            "Kinerja institusi dalam {S} lebih bergantung pada apakah mandat, uang dan informasi tiba bersamaan daripada pada kewenangan formal.",
            "Mandat yang terbelah antarlembaga menghasilkan jurang yang akrab antara peringatan dan respons; anggaran yang terikat tahun kalender menghasilkan jurang antara bantuan dan pemulihan (UNDRR, 2015).",
            "Tidak satu pun jurang itu menuntut niat buruk, hanya pembagian kerja yang biasa.",
            "Tekanannya sudah terlihat pada angka: {D}.",
            "Bagi {DOM}, pertanyaan desainnya adalah di mana menempatkan kewenangan yang dapat menggerakkan uang dan orang dalam pekan yang sama.",
            "Koordinasi bukan kebaikan yang diminta; ia struktur yang dibangun.",
        ],
        "cost": [
            "Ekonomi {S} biasanya disajikan sebagai tagihan, dan itu bentuk penyajian yang paling tidak berguna.",
            "Biaya datang lebih awal dan masuk anggaran, sementara manfaat datang terlambat dan tidak bertuan; asimetri itu sistematis membiaskan investasi publik ke arah respons dan menjauh dari persiapan (World Bank, 2023).",
            "Asuransi dan kredit kemudian menyalurkan bias itu ke keputusan swasta tentang di mana membangun dan apa yang dilindungi.",
            "Besarannya bukan marginal: {D}.",
            "Bagi {DOM}, pembukuan yang berguna memisahkan biaya bersiap dari biaya tidak bersiap, dan menilai keduanya pada horizon yang sama.",
            "Ukuran yang mahal terhadap satu tahun anggaran sering murah terhadap sepuluh tahun.",
        ],
        "decision": [
            "Siapa pun yang memutuskan tentang {S} memilih dalam kondisi yang tidak akan membaik sebelum pilihan itu harus diambil.",
            "Karena itu urutan menjadi keterampilan utama: ukuran yang murah, dapat dibalik dan berguna pada beberapa masa depan berjalan lebih dulu, sedangkan komitmen yang tidak dapat dibalik menunggu informasi lebih baik (IPCC, 2022).",
            "Urutannya penting karena pilihan awal membeli waktu yang dibutuhkan pilihan berikutnya.",
            "Tekanannya terdokumentasi, bukan proyeksi: {D}.",
            "Bagi {DOM}, ujian sebuah rencana bukan apakah ia optimal untuk satu ramalan, melainkan apakah ia bertahan pada beberapa ramalan.",
            "Keputusan yang diambil hari ini akan dinilai oleh peristiwa yang tidak ada dalam ramalan.",
        ],
    },
}

for _l4, _blocks4 in VARIANT4.items():
    for _name4, _blk4 in _blocks4.items():
        LENS[_l4][_name4].append(_blk4)


# ------------------------------------------------- kasus & jangkar ahli ----
EXPERT_ANCHOR = {
    "en": [
        "Applied to {S}, the argument sets a test: does the measure still work when capacity is stretched?",
        "For {S}, the bearing is direct: the constraint is institutional as much as physical.",
        "Read against {S}, the point is that intention without capacity changes little.",
        "The implication for {S} is a question of sequence: what has to be in place before the event, not after it.",
        "In the terms of {S}, the claim shifts attention from prediction to preparation.",
        "For {S}, the practical consequence is to name the decision that would have to change.",
    ],
    "id": [
        "Diterapkan pada {S}, argumen itu memberi ujian: apakah tindakan tetap bekerja ketika kapasitas menipis?",
        "Bagi {S}, kaitannya langsung: kendalanya institusional sama besar dengan fisik.",
        "Dibaca terhadap {S}, intinya adalah niat tanpa kapasitas tidak mengubah banyak.",
        "Implikasi bagi {S} adalah soal urutan: apa yang harus ada sebelum peristiwa, bukan sesudahnya.",
        "Dalam kerangka {S}, klaim itu menggeser perhatian dari prediksi ke persiapan.",
        "Bagi {S}, konsekuensi praktisnya adalah menyebut keputusan mana yang harus berubah.",
    ],
}

CASE = {
    "en": {
        "open": "The case that anchors this chapter is documented and recent: {news}. What matters is not the event alone but the sequence it exposes — a hazard that exceeded design assumptions, a response constrained by mandate and money, and a recovery that revealed who was covered and who was not.",
        "mid": [
            "Cases of this kind are useful because they compress several mechanisms into a short period. Exposure, capacity and institutional reach become visible at once, and the gaps between them stop being abstract (UNDRR, 2015). For {DOM}, the episode works as a readiness test rather than a weather story.",
            "Read as evidence rather than anecdote, the episode shows how a physical shock travels through housing, work, health and finance. Damage does not stop where the water recedes; it continues through lost income, interrupted schooling and depleted savings — a sequence {DOM} can measure in its own records.",
            "The instructive part is the asymmetry between the event and its aftermath. Response times are measured in hours, recovery in years, and the difference between the two is usually decided before the event — by land use, insurance and local authority, all of which {DOM} controls.",
        ],
        "close": [
            "For {DOM}, the transferable lesson is procedural: identify which decision failed first, and fix that decision rather than the symptom.",
            "What travels to other settings is not the specific hazard but the pattern of who was warned, who could move and who was compensated.",
            "The test of any lesson drawn from the case is whether it changes a budget line, a standard or a protocol. If it changes none of the three, it remains a story.",
        ],
    },
    "id": {
        "open": "Kasus yang menjadi jangkar bab ini terdokumentasi dan masih baru: {news}. Yang penting bukan peristiwanya semata, melainkan urutan yang disingkapnya — bahaya yang melampaui asumsi desain, respons yang dibatasi mandat dan uang, serta pemulihan yang memperlihatkan siapa tercakup dan siapa tidak.",
        "mid": [
            "Kasus semacam ini berguna karena memadatkan beberapa mekanisme dalam waktu singkat. Paparan, kapasitas dan jangkauan institusi menjadi terlihat sekaligus, dan jarak di antaranya berhenti menjadi abstrak (UNDRR, 2015). Bagi {DOM}, peristiwa itu berfungsi sebagai uji kesiapan, bukan cerita cuaca.",
            "Dibaca sebagai bukti, bukan anekdot, peristiwa itu menunjukkan bagaimana guncangan fisik menjalar melalui hunian, pekerjaan, kesehatan dan keuangan. Kerusakan tidak berhenti saat air surut; ia berlanjut lewat pendapatan yang hilang, sekolah yang terputus dan tabungan yang terkuras — urutan yang dapat diukur {DOM} dalam catatannya sendiri.",
            "Bagian yang mendidik adalah ketimpangan antara peristiwa dan sesudahnya. Waktu tanggap diukur dalam jam, pemulihan dalam tahun, dan pembeda keduanya biasanya ditentukan sebelum peristiwa — oleh tata guna lahan, asuransi dan kewenangan lokal, yang semuanya dikendalikan {DOM}.",
        ],
        "close": [
            "Bagi {DOM}, pelajaran yang dapat dibawa bersifat prosedural: kenali keputusan mana yang gagal lebih dulu, lalu perbaiki keputusan itu, bukan gejalanya.",
            "Yang berpindah ke tempat lain bukan bahayanya, melainkan pola siapa yang diperingatkan, siapa yang dapat pindah dan siapa yang mendapat ganti rugi.",
            "Ujian setiap pelajaran dari kasus adalah apakah ia mengubah baris anggaran, standar atau protokol. Jika tidak mengubah ketiganya, ia tinggal cerita.",
        ],
    },
}


def short_topic(theme):
    """Tema tanpa daftar panjang: ambil klausa pertama."""
    return theme.split(",")[0].strip() if "," in theme else theme


def short_np(sec_title, lang):
    """NP pendek untuk sisipan dalam kalimat panjang."""
    np_ = np_of(sec_title, lang)
    if "," in np_:
        np_ = np_.split(",")[0].strip()
    return np_


def expert_anchor(lang, sec_title, ci, si):
    np_ = np_of(sec_title, lang)
    if "," in np_ or len(np_.split()) > 6:
        np_ = np_.split(",")[0].strip()
    i = (ci * 5 + si) % 6
    if np_.startswith("kerangka "):
        while "kerangka {" in EXPERT_ANCHOR[lang][i]:
            i = (i + 1) % 6
    return EXPERT_ANCHOR[lang][i].format(S=np_)


CASE_OPEN_TAIL = {
    "en": [
        "For {DOM}, the episode fixes the date at which the argument stops being hypothetical.",
        "For {DOM}, it is the clearest recent test of whether the arrangements on paper survive contact with an event.",
        "For {DOM}, the record supplies both the warning and the timetable.",
        "For {DOM}, the sequence is worth reconstructing before the next season rather than after it.",
    ],
    "id": [
        "Bagi {DOM}, peristiwa itu menetapkan tanggal ketika argumennya berhenti menjadi hipotetis.",
        "Bagi {DOM}, ia adalah uji terbaru yang paling jelas atas apakah pengaturan di atas kertas bertahan saat berhadapan dengan peristiwa.",
        "Bagi {DOM}, catatan itu menyediakan peringatan sekaligus jadwalnya.",
        "Bagi {DOM}, urutan peristiwanya layak direkonstruksi sebelum musim berikutnya, bukan sesudahnya.",
    ],
}


def case_paragraphs(lang, ci, theme, news, dom):
    c = CASE[lang]
    h = len(news) + news.count(",") + news.count(" ") % 7
    opener = (CASE_OPEN_VARIANTS[lang][ci % 3].format(news=news) + " "
              + CASE_OPEN_TAIL[lang][ci % 4].format(DOM=dom))
    return [
        opener,
        c["mid"][(ci + h) % 3].format(DOM=dom),
        c["close"][(ci + 2 * h) % 3].format(DOM=dom),
    ]


# --------------------------------------------- penutup spesifik domain -----
DOM_CLOSE = {
    "en": {
        "limit": "For {DOM}, the operational reading is to record which limit applies to each decision before the decision is taken.",
        "synth": "For {DOM}, the question is which of these decisions can be taken before the next event rather than during it.",
    },
    "id": {
        "limit": "Bagi {DOM}, bacaan operasionalnya adalah mencatat batas mana yang berlaku untuk tiap keputusan sebelum keputusan itu diambil.",
        "synth": "Bagi {DOM}, pertanyaannya adalah keputusan mana yang dapat diambil sebelum peristiwa berikutnya, bukan saat peristiwa berlangsung.",
    },
}

CASE_OPEN_VARIANTS = {
    "en": [
        "The case that anchors this chapter is documented and recent: {news}. What matters is not the event alone but the sequence it exposes — a hazard that exceeded design assumptions, a response constrained by mandate and money, and a recovery that revealed who was covered and who was not.",
        "One documented episode makes the argument concrete: {news}. It repays attention less as an outlier than as a chain of decisions — where the hazard was allowed to concentrate, how the response was organised, and who bore the residual loss.",
        "A single episode illustrates the mechanism: {news}. Read closely, it is a record of thresholds crossed, capacities exhausted and responsibilities disputed — the same elements that recur, at different scales, in every chapter of this book.",
    ],
    "id": [
        "Kasus yang menjadi jangkar bab ini terdokumentasi dan masih baru: {news}. Yang penting bukan peristiwanya semata, melainkan urutan yang disingkapnya — bahaya yang melampaui asumsi desain, respons yang dibatasi mandat dan uang, serta pemulihan yang memperlihatkan siapa tercakup dan siapa tidak.",
        "Satu peristiwa terdokumentasi membuat argumennya konkret: {news}. Ia layak diperhatikan bukan sebagai anomali, melainkan sebagai rangkaian keputusan — di mana bahaya dibiarkan menumpuk, bagaimana respons diorganisasi, dan siapa yang menanggung kerugian sisanya.",
        "Satu peristiwa menggambarkan mekanismenya: {news}. Dibaca cermat, ia adalah catatan tentang ambang yang terlampaui, kapasitas yang habis dan tanggung jawab yang diperdebatkan — unsur yang berulang, pada skala berbeda, di setiap bab buku ini.",
    ],
}


LENS_CLOSE_ALT = {
    "en": [
        "That is the test a plan either passes or fails, and it is easier to state than to meet.",
        "Everything else in the file is administration, and administration is not the hard part.",
        "The choice is narrower than the analysis that produced it, which is usually a good sign.",
        "What remains is to decide who is accountable when the test is failed.",
        "The rest is a matter of sequence rather than of ambition.",
        "Whether that happens is a decision, not a forecast, and decisions can be scheduled.",
        "A reader who wants a single recommendation will find one here, and it is a modest one.",
        "None of this requires new science, only the application of what is already known.",
    ],
    "id": [
        "Itulah ujian yang dilalui atau gagal oleh sebuah rencana, dan lebih mudah dinyatakan daripada dipenuhi.",
        "Sisanya dalam berkas itu adalah administrasi, dan administrasi bukan bagian yang sulit.",
        "Pilihannya lebih sempit daripada analisis yang menghasilkannya, dan itu biasanya tanda baik.",
        "Yang tersisa adalah memutuskan siapa yang bertanggung jawab ketika ujian itu gagal.",
        "Selebihnya soal urutan, bukan soal besarnya ambisi.",
        "Apakah itu terjadi adalah keputusan, bukan ramalan, dan keputusan dapat dijadwalkan.",
        "Pembaca yang menginginkan satu rekomendasi akan menemukannya di sini, dan rekomendasinya sederhana.",
        "Tidak satu pun dari ini menuntut ilmu baru, hanya penerapan yang sudah diketahui.",
    ],
}

LENS_CLOSE = {
    "en": [
        "For {DOM}, that is the difference between a plan that can be defended and one that merely exists.",
        "For {DOM}, the test is whether the arrangement survives contact with a bad week.",
        "For {DOM}, the practical question is what would have to change first.",
        "For {DOM}, the implication is a shorter list of decisions than the analysis suggests.",
    ],
    "id": [
        "Bagi {DOM}, itulah pembeda antara rencana yang dapat dipertahankan dan rencana yang hanya ada.",
        "Bagi {DOM}, ujiannya adalah apakah pengaturan itu bertahan saat menghadapi pekan yang buruk.",
        "Bagi {DOM}, pertanyaan praktisnya adalah apa yang harus berubah lebih dulu.",
        "Bagi {DOM}, implikasinya adalah daftar keputusan yang lebih pendek daripada yang tampak dari analisis.",
    ],
}


# ------------------------------------- varian lensa kausal kelima & keenam --
VARIANT56 = {
    "en": {
        "causal": [
            [
                "Impacts do not follow directly from a change in the average; they follow from the interaction between a shifting hazard and a fixed exposure.",
                "A house built to a hundred-year flood standard meets a twenty-five-year event with alarming regularity once the distribution has moved (IPCC, 2022).",
                "Nothing about the house changed; the standard it was designed against did.",
                "The shift is quantifiable: {D}.",
                "For {DOM}, the lesson is that design standards have a shelf life and need a review date attached to them.",
                "An unrevised standard is a decision to accept a higher level of risk than the one originally debated.",
            ],
            [
                "Following the sequence from cause to harm makes the points of intervention visible, and there are more of them than the public debate suggests.",
                "Emissions determine the forcing; land use and insurance determine exposure; income, health and warning determine capacity; each link can be altered by policy at a different scale (UNDRR, 2015).",
                "Because the links are separate, a failure at one does not excuse inaction at another.",
                "The scale at which the chain operates is large: {D}.",
                "For {DOM}, the practical value of thinking in a chain is that it shows which link is cheapest to move this year.",
                "Intervention points are political choices, not physical facts.",
            ],
        ],
    },
    "id": {
        "causal": [
            [
                "Dampak tidak mengikuti langsung perubahan rata-rata; ia mengikuti interaksi antara bahaya yang bergeser dan paparan yang tetap.",
                "Rumah yang dibangun dengan standar banjir seratus tahun akan menghadapi peristiwa dua puluh lima tahun dengan keteraturan yang mengkhawatirkan begitu distribusinya bergeser (IPCC, 2022).",
                "Tidak ada yang berubah pada rumah itu; yang berubah adalah standar yang menjadi acuan desainnya.",
                "Pergeserannya terukur: {D}.",
                "Bagi {DOM}, pelajarannya adalah standar desain memiliki masa berlaku dan perlu tanggal peninjauan.",
                "Standar yang tidak direvisi adalah keputusan menerima risiko lebih tinggi daripada yang semula diperdebatkan.",
            ],
            [
                "Menelusuri urutan dari sebab ke kerugian membuat titik intervensi terlihat, dan jumlahnya lebih banyak daripada yang tersirat dalam perdebatan publik.",
                "Emisi menentukan pemaksaan; tata guna lahan dan asuransi menentukan paparan; pendapatan, kesehatan dan peringatan menentukan kapasitas; setiap mata rantai dapat diubah kebijakan pada skala berbeda (UNDRR, 2015).",
                "Karena mata rantainya terpisah, kegagalan pada satu mata tidak menghapus kewajiban bertindak pada mata lain.",
                "Skala kerja rantai itu besar: {D}.",
                "Bagi {DOM}, nilai praktis berpikir dalam rantai adalah ia menunjukkan mata mana yang termurah digerakkan tahun ini.",
                "Titik intervensi adalah pilihan politik, bukan fakta fisik.",
            ],
        ],
    },
}
for _l5, _b5 in VARIANT56.items():
    for _n5, _bl5 in _b5.items():
        LENS[_l5][_n5].extend(_bl5)


DOM_FRAME = {
    "en": ["For {DOM}, ", "Within {DOM}, ",
           "As far as {DOM} is concerned, ", "In the work of {DOM}, "],
    "id": ["Bagi {DOM}, ", "Di dalam {DOM}, ",
           "Sejauh menyangkut {DOM}, ", "Dalam kerja {DOM}, "],
}


def vary_dom(text, lang, dom, seed):
    """Ganti pembuka 'For {DOM},' dengan variasi bingkai agar tidak berulang."""
    base = "For " + dom if lang == "en" else "Bagi " + dom
    frames = DOM_FRAME[lang]
    out, pos, i = [], 0, 0
    needle = base + ", "
    while True:
        k = text.find(needle, pos)
        if k < 0:
            out.append(text[pos:])
            break
        out.append(text[pos:k])
        out.append(frames[(seed + i) % len(frames)].format(DOM=dom))
        pos = k + len(needle)
        i += 1
    return "".join(out)


class ExpertPicker:
    """Pilih pakar yang topiknya cocok, dengan penyeimbangan pemakaian."""

    def __init__(self, keywords, n_experts):
        import collections as _c
        self.kw = keywords
        self.n = n_experts
        self.used = _c.Counter()

    def pick(self, text, default_idx):
        key = text.lower()
        cands = []
        for idx, kws in self.kw.items():
            score = sum(1 for k in kws if k.lower() in key)
            if score:
                cands.append((score, idx))
        if not cands:
            idx = default_idx
        else:
            top = max(s for s, _ in cands)
            pool = [i for s, i in cands if s >= max(1, top - 1)]
            idx = min(pool, key=lambda i: (self.used[i], abs(i - default_idx)))
        self.used[idx] += 1
        return idx
