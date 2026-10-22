# -*- coding: utf-8 -*-
"""Gambar data buku: definisi, penyisipan ke markdown, dan metadata.

Setiap gambar diletakkan tepat setelah tabel yang menjadi sumbernya, sehingga
pembaca melihat angka dan bentuknya berdekatan. Penyisipan dilakukan sebelum
book.md / book_id.md ditulis, jadi ketiga renderer (PDF, EPUB, DOCX) menerima
blok yang sama.

Sintaks blok: ![caption](berkas)||Source: ...
"""
import re

# id, tabel sumber, berkas, caption (en/id), sumber (en/id), alt (en/id)
FIGURES = [
    dict(id="2.1", table="2.1", file="figures/fig2_1.png",
         cap_en="Warming in 2050 and 2100 under three emission trajectories",
         cap_id="Pemanasan 2050 dan 2100 pada tiga lintasan emisi",
         src_en="Table 2.1. Bars show the 2100 range; SSP scenarios as summarised in IPCC (2021, 2023).",
         src_id="Tabel 2.1. Garis tegak menunjukkan rentang 2100; skenario SSP sebagaimana dirangkum IPCC (2021, 2023).",
         alt_en="Slope chart: warming rises from about 1.6, 2.0 and 2.6 degrees in 2050 to 1.8, 2.7 and 4.4 degrees in 2100 for the three trajectories.",
         alt_id="Grafik lereng: pemanasan naik dari sekitar 1,6, 2,0 dan 2,6 derajat pada 2050 menjadi 1,8, 2,7 dan 4,4 derajat pada 2100 untuk tiga lintasan."),
    dict(id="4.1", table="4.1", file="figures/fig4_1.png",
         cap_en="Days above 35 °C now and in 2050 in six cities",
         cap_id="Hari di atas 35 °C sekarang dan pada 2050 di enam kota",
         src_en="Table 4.1; SSP2-4.5 for the 2050 column.",
         src_id="Tabel 4.1; SSP2-4.5 untuk kolom 2050.",
         alt_en="Dumbbell chart: Delhi rises from 100 to 140 hot days, Phoenix from 110 to 150, Karachi from 60 to 100, Jakarta from 30 to 70, Lagos from 20 to 60 and Athens from 30 to 55.",
         alt_id="Grafik dumbbell: Delhi naik dari 100 ke 140 hari panas, Phoenix dari 110 ke 150, Karachi dari 60 ke 100, Jakarta dari 30 ke 70, Lagos dari 20 ke 60 dan Athena dari 30 ke 55."),
    dict(id="5.1", table="5.1", file="figures/fig5_1.png",
         cap_en="People depending on six stressed basins, and the supply gap they face in 2050",
         cap_id="Penduduk yang bergantung pada enam cekungan tertekan, dan kesenjangan pasokan pada 2050",
         src_en="Table 5.1; gap is the shortfall against projected demand under SSP2-4.5.",
         src_id="Tabel 5.1; kesenjangan adalah kekurangan terhadap permintaan terproyeksi pada SSP2-4.5.",
         alt_en="Horizontal bar chart of basin population: Indus 300 million, Nile 280, Tigris-Euphrates 60, Colorado 40, Citarum 25, Murray-Darling 2.4, each labelled with its 2050 gap.",
         alt_id="Grafik batang horizontal populasi cekungan: Indus 300 juta, Nil 280, Tigris-Efrat 60, Colorado 40, Citarum 25, Murray-Darling 2,4, masing-masing dengan kesenjangan 2050."),
    dict(id="6.1", table="6.1", file="figures/fig6_1.png",
         cap_en="People exposed to a 1-in-100-year coastal flood in six cities",
         cap_id="Penduduk yang terpapar banjir pesisir periode ulang 100 tahun di enam kota",
         src_en="Table 6.1; exposure counts include subsidence where reported.",
         src_id="Tabel 6.1; jumlah terpapar mencakup penurunan tanah bila dilaporkan.",
         alt_en="Bar chart of exposed people: Jakarta 2.5 million, Manila 1.5 million, Bangkok and Ho Chi Minh City 1 million each, Alexandria 0.5 million, Miami 0.4 million.",
         alt_id="Grafik batang penduduk terpapar: Jakarta 2,5 juta, Manila 1,5 juta, Bangkok dan Ho Chi Minh City masing-masing 1 juta, Aleksandria 0,5 juta, Miami 0,4 juta."),
    dict(id="7.1", table="7.1", file="figures/fig7_1.png",
         cap_en="Yield change per additional degree of warming, by crop",
         cap_id="Perubahan hasil panen per tambahan satu derajat pemanasan, menurut tanaman",
         src_en="Table 7.1. Bars for coffee and livestock show the reported range.",
         src_id="Tabel 7.1. Batang untuk kopi dan ternak menunjukkan rentang yang dilaporkan.",
         alt_en="Bar chart of yield change per degree: maize minus 7.4 per cent, wheat minus 6, rice minus 3.2, soybean minus 3.1, coffee between minus 10 and minus 20, livestock between minus 5 and minus 10.",
         alt_id="Grafik batang perubahan hasil per derajat: jagung minus 7,4 persen, gandum minus 6, padi minus 3,2, kedelai minus 3,1, kopi antara minus 10 dan minus 20, ternak antara minus 5 dan minus 10."),
    dict(id="8.1", table="8.1", file="figures/fig8_1.png",
         cap_en="Decline at 2 °C and at 3 °C for four systems with measurable thresholds",
         cap_id="Penurunan pada 2 °C dan 3 °C untuk empat sistem dengan ambang terukur",
         src_en="Table 8.1. Coral value at 3 °C is the reported “greater than 99 per cent”.",
         src_id="Tabel 8.1. Nilai terumbu pada 3 °C adalah “lebih dari 99 persen” yang dilaporkan.",
         alt_en="Grouped range bars: coral reefs decline 70–90 per cent at 2 degrees and more than 99 per cent at 3; permafrost thaws 10–20 against 30–50; mangroves lose 10–30 against 30–50; freshwater species lose 20–30 against 40–60.",
         alt_id="Batang rentang berkelompok: terumbu karang turun 70–90 persen pada 2 derajat dan lebih dari 99 persen pada 3; permafrost mencair 10–20 berbanding 30–50; mangrove hilang 10–30 berbanding 30–50; spesies air tawar hilang 20–30 berbanding 40–60."),
    dict(id="10.1", table="10.1", file="figures/fig10_1.png",
         cap_en="Global GDP loss by 2050 under three emission paths",
         cap_id="Kerugian PDB global hingga 2050 pada tiga jalur emisi",
         src_en="Table 10.1; loss is measured against a no-climate baseline.",
         src_id="Tabel 10.1; kerugian diukur terhadap garis dasar tanpa perubahan iklim.",
         alt_en="Range bars: low emissions 3 to 5 per cent of GDP, current policies 8 to 12, high emissions 15 to 20.",
         alt_id="Batang rentang: emisi rendah 3 sampai 5 persen PDB, kebijakan sekarang 8 sampai 12, emisi tinggi 15 sampai 20."),
    dict(id="11.1", table="11.1", file="figures/fig11_1.png",
         cap_en="Internal climate migrants by 2050, by region of origin",
         cap_id="Migran iklim internal pada 2050, menurut kawasan asal",
         src_en="Table 11.1; estimates are internal movements, not cross-border refugees.",
         src_id="Tabel 11.1; estimasi adalah perpindahan internal, bukan pengungsi lintas batas.",
         alt_en="Bar chart: Sub-Saharan Africa 85 million, East Asia and Pacific 48, South Asia 40, North Africa 19, Latin America 17, small island states 2 to 3.",
         alt_id="Grafik batang: Afrika sub-Sahara 85 juta, Asia Timur dan Pasifik 48, Asia Selatan 40, Afrika Utara 19, Amerika Latin 17, negara pulau kecil 2 sampai 3."),
    dict(id="17.1", table="17.1", file="figures/fig17_1.png",
         cap_en="Annual excess heat deaths in 2050 under three adaptation paths",
         cap_id="Kematian berlebih akibat panas per tahun pada 2050 di bawah tiga jalur adaptasi",
         src_en="Table 17.1.",
         src_id="Tabel 17.1.",
         alt_en="Bar chart: 700,000 deaths with low adaptation, 500,000 with current trends, 250,000 with high adaptation.",
         alt_id="Grafik batang: 700.000 kematian dengan adaptasi rendah, 500.000 dengan tren sekarang, 250.000 dengan adaptasi tinggi."),
    dict(id="22.1", table="22.1", file="figures/fig22_1.png",
         cap_en="Deaths in eight urban and wildfire disasters, on a logarithmic scale",
         cap_id="Kematian pada delapan bencana perkotaan dan kebakaran, pada skala logaritma",
         src_en="Table 22.1. Lytton shows deaths for British Columbia in 2021.",
         src_id="Tabel 22.1. Lytton menunjukkan kematian di British Columbia pada 2021.",
         alt_en="Logarithmic bar chart: Europe 2003 about 70,000 deaths, Pakistan 2022 1,700, Chicago 1995 739, Lytton 619, Germany 2021 more than 180, Black Saturday 173, Seoul 141, Camp Fire 85.",
         alt_id="Grafik batang logaritma: Eropa 2003 sekitar 70.000 kematian, Pakistan 2022 1.700, Chicago 1995 739, Lytton 619, Jerman 2021 lebih dari 180, Black Saturday 173, Seoul 141, Camp Fire 85."),
    dict(id="23.1", table="23.1", file="figures/fig23_1.png",
         cap_en="Deaths in four drought and famine crises, on a logarithmic scale",
         cap_id="Kematian pada empat krisis kekeringan dan kelaparan, pada skala logaritma",
         src_en="Table 23.1. Syria 2006–10 is omitted because the table records displacement, not deaths.",
         src_id="Tabel 23.1. Suriah 2006–10 tidak dimasukkan karena tabel mencatat perpindahan, bukan kematian.",
         alt_en="Logarithmic bar chart: Ethiopia 1984–85 about 1,000,000 deaths, Somalia 2011 258,000, Sahel 1972–74 about 100,000, Somalia 2022 about 43,000.",
         alt_id="Grafik batang logaritma: Ethiopia 1984–85 sekitar 1.000.000 kematian, Somalia 2011 258.000, Sahel 1972–74 sekitar 100.000, Somalia 2022 sekitar 43.000."),
]

PREFIX = {"en": "Table", "id": "Tabel"}
LABEL = {"en": "Figure", "id": "Gambar"}


def path(fig, lang):
    """Berkas PNG untuk bahasa tertentu (label di dalam gambar ikut diterjemahkan)."""
    return fig["file"].replace(".png", "_%s.png" % lang) if lang == "id" else fig["file"]


def block(fig, lang):
    return "![%s %s %s](%s)||%s: %s" % (
        LABEL[lang], fig["id"], fig["cap_" + lang], path(fig, lang),
        "Source" if lang == "en" else "Sumber", fig["src_" + lang])


def insert(md, lang):
    """Sisipkan setiap gambar tepat setelah tabel sumbernya."""
    lines = md.split("\n")
    out, used = [], 0
    pending = {}          # indeks baris -> blok gambar
    for fig in FIGURES:
        marker = "[[TABLE:%s %s" % (PREFIX[lang], fig["table"])
        for i, ln in enumerate(lines):
            if ln.startswith(marker):
                j = i
                while j + 1 < len(lines) and lines[j + 1].startswith("|"):
                    j += 1
                pending.setdefault(j, []).append(fig)
                used += 1
                break
        else:
            print("PERINGATAN: tabel %s tidak ditemukan untuk gambar %s"
                  % (fig["table"], fig["id"]))
    for i, ln in enumerate(lines):
        out.append(ln)
        for fig in pending.get(i, []):
            out.append("")
            out.append(block(fig, lang))
    print("figures inserted: %d" % used)
    return "\n".join(out)


def alt(fig, lang):
    return fig["alt_" + lang]


def caption(fig, lang):
    return "%s %s %s" % (LABEL[lang], fig["id"], fig["cap_" + lang])


def source(fig, lang):
    return ("Source" if lang == "en" else "Sumber") + ": " + fig["src_" + lang]
