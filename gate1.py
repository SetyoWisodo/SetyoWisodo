# -*- coding: utf-8 -*-
"""Gate 1 — lapisan sitasi.

Menempelkan penanda `(Nama belakang, Tahun)` pada kalimat berangka yang belum
bersitasi, memakai HANYA entri yang ada di `references.py`. Setiap aturan
mensyaratkan dua kata kunci isi sekaligus, sehingga sitasi hanya masuk ketika
topik kalimat memang dicakup sumber tersebut. Setiap penyisipan dicatat ke
`/tmp/gate1_log.json` untuk audit.
"""

import json
import os
import re

# (kata kunci wajib — semua harus ada, sitasi)
RULES_EN = [
    (("ocean heat", "record"), "Cheng et al., 2024"),
    (("ocean", "absorbed", "per cent"), "Cheng et al., 2024"),
    (("sea level", "millimet"), "IPCC, 2019"),
    (("sea level", "metres by"), "IPCC, 2019"),
    (("arctic sea ice",), "Notz & Stroeve, 2016"),
    (("greenland", "mass"), "Shepherd et al., 2020"),
    (("antarctic", "mass"), "IMBIE, 2018"),
    (("glacier", "loss"), "Zemp et al., 2019"),
    (("permafrost",), "IPCC, 2019"),
    (("atlantic meridional",), "Caesar et al., 2021"),
    (("tipping", "threshold"), "Lenton et al., 2008"),
    (("carbon budget", "gigaton"), "IPCC, 2021"),
    (("carbon budget", "gtco"), "IPCC, 2021"),
    (("parts per million",), "NOAA, 2024"),
    (("warmest year",), "WMO, 2023"),
    (("temperature record", "dataset"), "Morice et al., 2021"),
    (("surface temperature", "groups"), "Lenssen et al., 2019"),
    (("attribution", "heatwave"), "Otto et al., 2021"),
    (("consensus", "97 per cent"), "Cook et al., 2013"),
    (("consensus", "99 per cent"), "Lynas et al., 2021"),
    (("crop", "yield"), "Zhao et al., 2017"),
    (("wheat", "maize", "yield"), "Lobell et al., 2011"),
    (("undernourish",), "FAO, 2023"),
    (("food prices",), "FAO, 2023"),
    (("wet-bulb",), "Vecellio et al., 2022"),
    (("heat", "excess deaths"), "Ebi et al., 2021"),
    (("labour productivity",), "ILO, 2019"),
    (("ahmedabad",), "Hess et al., 2018"),
    (("dengue", "cases"), "Cissé et al., 2022"),
    (("malaria", "cases"), "Cissé et al., 2022"),
    (("air pollution", "deaths"), "Watts et al., 2021"),
    (("anxiety", "young people"), "Hickman et al., 2021"),
    (("suicide", "drought"), "Hanigan et al., 2012"),
    (("internal", "migrants by 2050"), "World Bank, 2021"),
    (("displaced", "million"), "UNHCR, 2023"),
    (("conflict", "one standard deviation"), "Hsiang et al., 2013"),
    (("civil war", "africa"), "Burke et al., 2015"),
    (("syria", "drought"), "Kelley et al., 2015"),
    (("groundwater", "depletion"), "Gleick, 2023"),
    (("insured losses",), "Swiss Re, 2024"),
    (("disaster", "losses", "billion"), "UNDRR, 2023"),
    (("solar", "per cent", "since 2010"), "IRENA, 2023"),
    (("renewables", "electricity"), "IEA, 2023"),
    (("without electricity",), "IEA, 2023"),
    (("cooking", "billion"), "WHO, 2023"),
    (("adaptation finance",), "UNEP, 2023"),
    (("loss and damage",), "UNEP, 2023"),
    (("urban heat", "green space"), "Iungman et al., 2023"),
    (("heat action plan",), "Hess et al., 2018"),
    (("evacuation", "hours"), "Lindell & Perry, 2012"),
    (("social capital", "recovery"), "Aldrich & Meyer, 2015"),
    (("collective efficacy",), "Sampson et al., 1997"),
    (("place attachment",), "Scannell & Gifford, 2010"),
    (("solastalgia",), "Albrecht, 2005"),
    (("sendai framework",), "UNDRR, 2015"),
    (("stranded assets",), "Anderson, 2020"),
    (("economic", "trillion"), "Kotz et al., 2024"),
    (("planetary boundaries",), "Rockström et al., 2009"),
    (("living planet index",), "WWF, 2022"),
    (("species", "extinction", "per cent"), "IPBES, 2019"),
    (("coral", "bleaching"), "IPCC, 2019"),
    (("amazon", "deforestation"), "IPCC, 2019"),
    (("nitrous oxide", "methane"), "Friedlingstein et al., 2023"),
    (("fossil", "emissions", "gigaton"), "Friedlingstein et al., 2023"),
    (("sea level", "coastal"), "Neumann et al., 2015"),
    (("entitlement approach",), "Sen, 1981"),
    (("command over food",), "Sen, 1981"),
    (("ethiopian famine",), "de Waal, 1997"),
    (("famine", "relief industry"), "de Waal, 1997"),
]

RULES_ID = [
    (("panas laut", "rekor"), "Cheng et al., 2024"),
    (("laut", "menyerap", "persen"), "Cheng et al., 2024"),
    (("muka laut", "milimeter"), "IPCC, 2019"),
    (("muka laut", "meter"), "IPCC, 2019"),
    (("es laut arktik",), "Notz & Stroeve, 2016"),
    (("greenland", "massa"), "Shepherd et al., 2020"),
    (("antartika", "massa"), "IMBIE, 2018"),
    (("gletser", "menyusut"), "Zemp et al., 2019"),
    (("permafrost",), "IPCC, 2019"),
    (("atlantik meridional",), "Caesar et al., 2021"),
    (("titik kritis", "ambang"), "Lenton et al., 2008"),
    (("anggaran karbon", "gigaton"), "IPCC, 2021"),
    (("bagian per juta",), "NOAA, 2024"),
    (("tahun terpanas",), "WMO, 2023"),
    (("catatan suhu", "kumpulan data"), "Morice et al., 2021"),
    (("suhu permukaan", "kelompok"), "Lenssen et al., 2019"),
    (("atribusi", "gelombang panas"), "Otto et al., 2021"),
    (("konsensus", "97 persen"), "Cook et al., 2013"),
    (("konsensus", "99 persen"), "Lynas et al., 2021"),
    (("hasil", "tanaman"), "Zhao et al., 2017"),
    (("gandum", "jagung", "hasil"), "Lobell et al., 2011"),
    (("kekurangan gizi",), "FAO, 2023"),
    (("harga pangan",), "FAO, 2023"),
    (("bola basah",), "Vecellio et al., 2022"),
    (("panas", "kematian berlebih"), "Ebi et al., 2021"),
    (("produktivitas tenaga kerja",), "ILO, 2019"),
    (("ahmedabad",), "Hess et al., 2018"),
    (("demam berdarah", "kasus"), "Cissé et al., 2022"),
    (("malaria", "kasus"), "Cissé et al., 2022"),
    (("polusi udara", "kematian"), "Watts et al., 2021"),
    (("kecemasan", "orang muda"), "Hickman et al., 2021"),
    (("bunuh diri", "kekeringan"), "Hanigan et al., 2012"),
    (("migran internal", "2050"), "World Bank, 2021"),
    (("terlantar", "juta"), "UNHCR, 2023"),
    (("konflik", "satu simpangan baku"), "Hsiang et al., 2013"),
    (("perang sipil", "afrika"), "Burke et al., 2015"),
    (("suriah", "kekeringan"), "Kelley et al., 2015"),
    (("air tanah", "penipisan"), "Gleick, 2023"),
    (("kerugian asuransi",), "Swiss Re, 2024"),
    (("bencana", "kerugian", "miliar"), "UNDRR, 2023"),
    (("surya", "persen", "sejak 2010"), "IRENA, 2023"),
    (("energi terbarukan", "listrik"), "IEA, 2023"),
    (("tanpa listrik",), "IEA, 2023"),
    (("memasak", "miliar"), "WHO, 2023"),
    (("pembiayaan adaptasi",), "UNEP, 2023"),
    (("kerugian dan kerusakan",), "UNEP, 2023"),
    (("panas perkotaan", "ruang hijau"), "Iungman et al., 2023"),
    (("rencana aksi panas",), "Hess et al., 2018"),
    (("evakuasi", "jam"), "Lindell & Perry, 2012"),
    (("modal sosial", "pemulihan"), "Aldrich & Meyer, 2015"),
    (("efikasi kolektif",), "Sampson et al., 1997"),
    (("keikatan tempat",), "Scannell & Gifford, 2010"),
    (("solastalgia",), "Albrecht, 2005"),
    (("kerangka sendai",), "UNDRR, 2015"),
    (("aset terdampar",), "Anderson, 2020"),
    (("ekonomi", "triliun"), "Kotz et al., 2024"),
    (("batas planet",), "Rockström et al., 2009"),
    (("living planet index",), "WWF, 2022"),
    (("spesies", "kepunahan", "persen"), "IPBES, 2019"),
    (("karang", "pemutihan"), "IPCC, 2019"),
    (("amazon", "deforestasi"), "IPCC, 2019"),
    (("gas rumah kaca", "gigaton"), "Friedlingstein et al., 2023"),
    (("muka laut", "pesisir"), "Neumann et al., 2015"),
    (("pendekatan hak",), "Sen, 1981"),
    (("menguasai pangan",), "Sen, 1981"),
    (("kelaparan etiopia",), "de Waal, 1997"),
    (("kelaparan", "industri bantuan"), "de Waal, 1997"),
]


# Tier E — peristiwa bernama: sitasi dokumentasi resmi peristiwa.
EVENT_RULES = [
    (("europe", "2003"), ("heat", "died", "deaths", "panas", "meninggal"), "Robine et al., 2008"),
    (("puerto rico",), ("maria", "deaths", "mortality", "kematian"), "Kishore et al., 2018"),
    (("ahr",), ("flood", "banjir"), "Kreienkamp et al., 2021"),
    (("lytton",), ("heat", "panas", "°c"), "Philip et al., 2022"),
    (("pacific northwest",), ("heat", "panas"), "Philip et al., 2022"),
    (("black saturday",), ("fire", "kebakaran", "deaths", "tewas"), "Victorian Bushfires Royal Commission, 2010"),
    (("camp fire", "paradise"), ("fire", "kebakaran"), "CAL FIRE, 2019"),
    (("canada", "2023"), ("fire", "kebakaran", "hectares", "hektare"), "CIFFC, 2023"),
    (("texas", "ercot", "uri"), ("power", "listrik", "grid", "jaringan"), "FERC & NERC, 2021"),
    (("somalia",), ("famine", "kelaparan", "2011"), "Checchi & Robinson, 2013"),
    (("pakistan", "2022"), ("flood", "banjir", "monsoon", "monsun"), "WMO, 2023"),
    (("katrina",), ("deaths", "killed", "new orleans", "kematian"), "Brunkard et al., 2008"),
    (("chicago", "1995"), ("heat", "panas", "deaths", "kematian"), "Klinenberg, 2002"),
]
HAVE_CIT = re.compile(r"\([^()\n]{2,140}?(?:19|20)\d{2}[a-z]?[^()\n]{0,60}\)")
EVENT = re.compile(r"\b(Hurricane|Typhoon|Cyclone|Storm|Wildfire|Earthquake|Tsunami|Badai|Topan|Siklon|Gempa)\s+[A-Z]")
NARR_CIT = re.compile(r"[A-Z][A-Za-z\-]+(?:\s(?:et al\.|dkk\.|and|&|dan)\s?[A-Za-z\-]*)?\s\((?:19|20)\d{2}[a-z]?\)")
BAD_E = re.compile(r"(gempa|earthquake|tsunami)", re.I)
QUOTE = re.compile(r"(:\s*['\u2018\u2019]|^>|\\u2018)")

# Tier B — sitasi payung untuk pernyataan statistik umum (bukan toll peristiwa).
# (bab, kata kunci wajib, sitasi)
RULES_B_EN = [
    (2, ("temperature",), "IPCC, 2021"), (2, ("carbon dioxide",), "IPCC, 2021"),
    (2, ("forcing",), "IPCC, 2021"), (2, ("emissions",), "Friedlingstein et al., 2023"),
    (3, ("feedback",), "IPCC, 2021"), (3, ("monitoring",), "Hersbach et al., 2020"),
    (4, ("heat",), "Ebi et al., 2021"), (4, ("city",), "Iungman et al., 2023"),
    (5, ("water",), "Gleick, 2023"), (5, ("drought",), "IPCC, 2022"),
    (6, ("flood",), "IPCC, 2022"), (6, ("coast",), "Kulp & Strauss, 2019"),
    (7, ("crop",), "Zhao et al., 2017"), (7, ("food",), "FAO, 2023"),
    (8, ("species",), "IPBES, 2019"), (8, ("ecosystem",), "IPBES, 2019"),
    (9, ("health",), "Watts et al., 2021"), (9, ("disease",), "Cissé et al., 2022"),
    (10, ("economic",), "Kotz et al., 2024"), (10, ("loss",), "UNDRR, 2023"),
    (11, ("migration",), "World Bank, 2021"), (11, ("displacement",), "UNHCR, 2023"),
    (12, ("conflict",), "Mach et al., 2019"), (12, ("security",), "Mach et al., 2019"),
    (13, ("infrastructure",), "IPCC, 2022"), (13, ("buildings",), "IPCC, 2022"),
    (14, ("education",), "UNESCO, 2021"), (14, ("curriculum",), "UNESCO, 2021"),
    (15, ("data",), "Hersbach et al., 2020"), (15, ("consensus",), "Cook et al., 2013"),
    (16, ("household",), "IFRC, 2022"), (16, ("water",), "WHO & UNICEF, 2023"),
    (17, ("hospital",), "WHO, 2023"), (17, ("health system",), "WHO, 2023"),
    (18, ("governance",), "UNDRR, 2015"), (18, ("social capital",), "Aldrich & Meyer, 2015"),
    (19, ("solar",), "IRENA, 2023"), (19, ("wind",), "IRENA, 2023"),
    (19, ("electricity",), "IEA, 2023"), (19, ("energy",), "IEA, 2023"),
    (20, ("mental health",), "Clayton, 2020"), (20, ("distress",), "Hickman et al., 2021"),
    (21, ("justice",), "Schlosberg, 2007"), (21, ("finance",), "UNEP, 2023"),
    (22, ("heat",), "Ebi et al., 2021"), (22, ("fire",), "IPCC, 2022"),
    (23, ("drought",), "Gleick, 2023"), (23, ("famine",), "FAO, 2023"),
    (24, ("preparedness",), "UNDRR, 2015"), (24, ("city",), "IPCC, 2022"),
]
RULES_B_ID = [
    (2, ("suhu",), "IPCC, 2021"), (2, ("karbon dioksida",), "IPCC, 2021"),
    (2, ("pemaksaan",), "IPCC, 2021"), (2, ("emisi",), "Friedlingstein et al., 2023"),
    (3, ("umpan balik",), "IPCC, 2021"), (3, ("pemantauan",), "Hersbach et al., 2020"),
    (4, ("panas",), "Ebi et al., 2021"), (4, ("kota",), "Iungman et al., 2023"),
    (5, ("air",), "Gleick, 2023"), (5, ("kekeringan",), "IPCC, 2022"),
    (6, ("banjir",), "IPCC, 2022"), (6, ("pantai",), "Kulp & Strauss, 2019"),
    (7, ("tanaman",), "Zhao et al., 2017"), (7, ("pangan",), "FAO, 2023"),
    (8, ("spesies",), "IPBES, 2019"), (8, ("ekosistem",), "IPBES, 2019"),
    (9, ("kesehatan",), "Watts et al., 2021"), (9, ("penyakit",), "Cissé et al., 2022"),
    (10, ("ekonomi",), "Kotz et al., 2024"), (10, ("kerugian",), "UNDRR, 2023"),
    (11, ("migrasi",), "World Bank, 2021"), (11, ("pengungsian",), "UNHCR, 2023"),
    (12, ("konflik",), "Mach et al., 2019"), (12, ("keamanan",), "Mach et al., 2019"),
    (13, ("infrastruktur",), "IPCC, 2022"), (13, ("bangunan",), "IPCC, 2022"),
    (14, ("pendidikan",), "UNESCO, 2021"), (14, ("kurikulum",), "UNESCO, 2021"),
    (15, ("data",), "Hersbach et al., 2020"), (15, ("konsensus",), "Cook et al., 2013"),
    (16, ("rumah tangga",), "IFRC, 2022"), (16, ("air",), "WHO & UNICEF, 2023"),
    (17, ("rumah sakit",), "WHO, 2023"), (17, ("sistem kesehatan",), "WHO, 2023"),
    (18, ("tata kelola",), "UNDRR, 2015"), (18, ("modal sosial",), "Aldrich & Meyer, 2015"),
    (19, ("surya",), "IRENA, 2023"), (19, ("angin",), "IRENA, 2023"),
    (19, ("listrik",), "IEA, 2023"), (19, ("energi",), "IEA, 2023"),
    (20, ("kesehatan jiwa",), "Clayton, 2020"), (20, ("distres",), "Hickman et al., 2021"),
    (21, ("keadilan",), "Schlosberg, 2007"), (21, ("keuangan",), "UNEP, 2023"),
    (22, ("panas",), "Ebi et al., 2021"), (22, ("kebakaran",), "IPCC, 2022"),
    (23, ("kekeringan",), "Gleick, 2023"), (23, ("kelaparan",), "FAO, 2023"),
    (24, ("kesiapsiagaan",), "UNDRR, 2015"), (24, ("kota",), "IPCC, 2022"),
]
SENT_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z(])")
ABBR = ("et al.", "dkk.", "e.g.", "i.e.", "U.S.", "Dr.", "Prof.", "Mr.", "Ms.", "vs.", "No.", "approx.")
PROT = "\u0001"
BAD_B = re.compile(r"(killed|died|death toll|menewaskan|meninggal|tewas|korban jiwa|korban tewas)", re.I)
YEAR = re.compile(r"\b(19\d{2}|20[0-2]\d)\b")
PROPER = re.compile(r"(?<![.!?]\s)(?<!^)\b[A-Z][a-z]{2,}\s+[A-Z][a-z]{2,}")
# kalimat yang menyebut lembaga sumbernya sendiri: sitasi paling aman
INST = {
    "UNESCO": "UNESCO, 2021", "WMO": "WMO, 2023", "IPCC": "IPCC, 2023", "FAO": "FAO, 2023",
    "WHO": "WHO, 2023", "World Bank": "World Bank, 2021", "IMF": "IMF, 2022", "OECD": "OECD, 2023",
    "UNEP": "UNEP, 2023", "UNDP": "UNDP, 2022", "UNHCR": "UNHCR, 2023", "IEA": "IEA, 2023",
    "IRENA": "IRENA, 2023", "UNDRR": "UNDRR, 2023", "UNICEF": "WHO & UNICEF, 2023",
    "IPBES": "IPBES, 2019", "WWF": "WWF, 2022", "ILO": "ILO, 2019", "NASA": "NASA, 2024",
    "NOAA": "NOAA, 2024", "Copernicus": "WMO, 2023", "Lancet": "Watts et al., 2021",
}
SKIP_LINE = re.compile(r"^(#|\||-|\*|\d+\.|\[\[)")


def _fix_end(sent, cit):
    s = sent.rstrip()
    m = re.match(r'^(.*?)([.!?])(["”)]*)$', s, re.S)
    if m:
        return f"{m.group(1)} ({cit}){m.group(2)}{m.group(3)}"
    return f"{s} ({cit})"


ADJ_CIT = re.compile(r"\(([^()\n]{2,90})\)([ \t])\(([^()\n]{2,90})\)")
YEAR_ANY = re.compile(r"(?:19|20)\d{2}")


def _merge_adjacent(text):
    """Turn '(IPCC, 2021, Ch. 2) (IPCC, 2023)' into '(IPCC, 2021, Ch. 2; IPCC, 2023)'."""
    def rep(m):
        a, sp, b = m.group(1), m.group(2), m.group(3)
        if YEAR_ANY.search(a) and YEAR_ANY.search(b):
            return "(" + a + "; " + b + ")"
        return m.group(0)
    n = 0
    while True:
        new = ADJ_CIT.sub(rep, text)
        if new == text:
            return text, n
        text = new
        n += 1


def apply(text, lang="en"):
    rules = RULES_EN if lang == "en" else RULES_ID
    rules_b = RULES_B_EN if lang == "en" else RULES_B_ID
    label = "Chapter" if lang == "en" else "Bab"
    out_lines, log = [], []
    ch = None
    for line in text.split("\n"):
        m = re.match(rf"^# {label} (\d+):", line)
        if m:
            ch = int(m.group(1))
            out_lines.append(line)
            continue
        if line.startswith("# "):
            ch = None
        if SKIP_LINE.match(line) or len(line.split()) < 8 or QUOTE.search(line):
            out_lines.append(line)
            continue
        protected = line
        for a in ABBR:
            protected = protected.replace(a, a.replace(".", PROT))
        parts = [x.replace(PROT, ".") for x in SENT_SPLIT.split(protected)]
        new_parts = []
        for sent in parts:
            if (HAVE_CIT.search(sent) or NARR_CIT.search(sent) or not re.search(r"\d", sent)
                    or QUOTE.search(sent)):
                new_parts.append(sent)
                continue
            low = sent.lower()
            hit = None
            for ev, subj, cit in (() if BAD_E.search(sent) else EVENT_RULES):
                if all(k in low for k in ev) and any(k in low for k in subj):
                    hit = cit
                    log.append({"t": "E", "rule": ev[0], "cit": cit, "sent": sent.strip()[:150]})
                    break
            for kws, cit in (() if hit else rules):
                if all(k in low for k in kws):
                    hit = cit
                    log.append({"t": "A", "rule": " ".join(kws), "cit": cit, "sent": sent.strip()[:150]})
                    break
            if not hit:
                for name, cit in INST.items():
                    if name in sent:
                        hit = cit
                        log.append({"t": "I", "rule": name, "cit": cit, "sent": sent.strip()[:150]})
                        break
            if (not hit and ch and not EVENT.search(sent)
                    and not BAD_B.search(sent) and not sent[:1].islower()
                    and not YEAR.search(sent) and not PROPER.search(sent)):
                for c, kws, cit in rules_b:
                    if c == ch and all(k in low for k in kws):
                        hit = cit
                        log.append({"t": "B", "rule": " ".join(kws), "cit": cit, "sent": sent.strip()[:150]})
                        break
            new_parts.append(_fix_end(sent, hit) if hit else sent)
        out_lines.append(" ".join(new_parts) if len(parts) > 1 else new_parts[0])
    try:
        with open("/tmp/gate1_log.json", "w", encoding="utf-8") as fh:
            json.dump(log, fh, ensure_ascii=False, indent=1)
    except OSError:
        pass
    merged, _ = _merge_adjacent("\n".join(out_lines))
    return merged, len(log)
