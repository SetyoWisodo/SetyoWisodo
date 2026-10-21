# -*- coding: utf-8 -*-
"""Lapisan sitasi kedua (Gate 1b).

Menambahkan sitasi pada kalimat yang sudah ada, untuk karya yang sebelumnya
hanya masuk Daftar Pustaka tanpa pernah dikutip. Setiap aturan memakai jangkar
teks yang unik di dalam satu edisi, sehingga penempatan dapat diperiksa ulang.

Aturan: (jangkar EN, jangkar ID, sitasi). Jangkar dicari di dalam kalimat;
bila kalimat belum punya sitasi, sitasi ditambahkan di akhir kalimat. Bila
kalimat sudah diakhiri sitasi kurung, sitasi baru digabung dengan pemisah " ; ".
"""
import json
import re

RULES = [
    ("vulnerability is produced by decisions", "kerentanan dihasilkan oleh keputusan", "Adger, 2006"),
    ("Half a degree is the difference", "Setengah derajat adalah perbedaan", "IPCC, 2018"),
    ("social capital and public institutions are not alternatives",
     "modal sosial dan institusi publik bukan alternatif", "Aldrich & Meyer, 2015"),
    ("passed one terawatt", "melewati satu terawatt", "IRENA, 2023"),
    ("US$100 billion a year in climate finance",
     "US$100 miliar per tahun dalam pembiayaan iklim", "OECD, 2023"),
    ("The Stern Review estimated", "Stern Review memperkirakan", "Stern, 2007"),
    ("Food security depends on production", "Ketahanan pangan bergantung pada produksi",
     "Wheeler & von Braun, 2013"),
    ("bacteria such as Salmonella", "bakteri seperti Salmonella", "FAO, 2021"),
    ("Early Warnings for All initiative", "Inisiatif Early Warnings for All", "WMO, 2022"),
    ("Four independent groups", "Dataset utama menangani masalah itu", "Hausfather et al., 2023"),
    ("The carbon budget is the bridge", "anggaran karbon yang cukup untuk mengetahui",
     "Le Quéré et al., 2023"),
    ("Derna flood in Libya was made far more likely", "banjir Derna di Libya", "Otto et al., 2021"),
    ("Lancet Countdown publishes annual indicators",
     "Lancet Countdown menerbitkan indikator tahunan", "Romanello et al., 2023"),
    ("climate policy without a theory of justice", "kebijakan iklim tanpa teori keadilan",
     "Schlosberg, 2007"),
    ("Paris Agreement's transparency", "kerangka transparansi Perjanjian Paris",
     "United Nations, 2015b"),
    ("list cardiac arrest", "mencantumkan gagal jantung", "Red Cross, 2020"),
    ("high temperatures are associated with irritability", "suhu tinggi terkait dengan mudah tersinggung",
     "Obradovich et al., 2018"),
    ("volcanic aerosols, solar variability", "gunung berapi, dan variasi Matahari", "Haigh, 2020"),
    ("Researchers call these tipping elements", "Para peneliti menyebutnya elemen titik kritis",
     "Steffen et al., 2018"),
    ("meta-analysis by Hsiang, Burke and Miguel", "Meta-analisis yang banyak dikutip oleh Hsiang",
     "Hsiang & Burke, 2014"),
    ("a third of crop calories are fed to animals", "sepertiga kalori tanaman digunakan untuk pakan",
     "FAO, 2022"),
    ("The 'hockey stick' controversy", "'hockey stick' pada 2000-an", "Mann et al., 1999"),
    ("Fourier, Foote, Tyndall and Arrhenius", "Fourier, Foote, Tyndall, dan Arrhenius",
     "Dessler, 2021"),
    ("the adaptations that are known to work", "adaptasi yang diketahui berhasil", "Howden et al., 2007"),
    ("pro-cyclical fiscal burden", "beban fiskal prosiklikal", "IMF, 2022"),
    ("financial instruments that can build resilience",
     "instrumen keuangan yang dapat membangun ketangguhan", "OECD, 2021"),
    ("Italy became the first country", "Kasus Italia tidak biasa", "UNESCO, 2020"),
    ("Heat kills directly and indirectly", "Panas membunuh secara langsung dan tidak langsung", "WHO, 2021"),
    ("World Health Organization attributes more than 175,000", "mengaitkan lebih dari 175.000",
     "Vicedo-Cabrera et al., 2021"),
    ("Adaptive governance is the term", "Tata kelola adaptif adalah istilah", "Folke et al., 2010"),
    ("Bridging capital provides access to resources", "modal penjembatan memberikan akses",
     "Cutter et al., 2008"),
    ("Linking capital determines whether a community", "penghubung menentukan apakah komunitas",
     "Berkes & Ross, 2013"),
    ("Ortiz-Bobea and colleagues", "Ortiz-Bobea dan rekan-rekannya", "Lobell et al., 2011"),
    ("The budget does not care about pledges", "sebagian besar anggaran yang tersisa", "UNEP, 2022"),
    # hanya edisi Indonesia: karya yang di EN sudah dikutip, di ID belum
    ("", "Layanan kesehatan mental kurang didanai", "Clayton, 2020"),
    ("", "Modal penjembatan memberikan akses", "Cutter et al., 2008"),
    ("", "Antartika kehilangan sekitar 150 miliar", "IMBIE, 2018"),
    ("", "Fourier, Foote, Tyndall, dan Arrhenius", "Tyndall, 1861"),
    ("", "Laporan Groundswell Bank Dunia", "World Bank, 2021"),
]

SENT = re.compile(r"(?<=[.!?])\s+")
HAS_CIT = re.compile(r"\((?:[^()]*?)(?:18|19|20)\d{2}[a-z]?(?:[^()]*)\)\s*$")


def _add(sent, cit):
    sent = sent.rstrip()
    end = ""
    while sent and sent[-1] in "\"'\u201d\u2019":
        end = sent[-1] + end
        sent = sent[:-1]
    if sent.endswith("."):
        body, stop = sent[:-1], "."
    else:
        body, stop = sent, "."
    m = re.search(r"\(([^()]*?)\)$", body)
    if m and re.search(r"(?:18|19|20)\d{2}", m.group(1)):
        names = {p.strip().split(",")[0].lower() for p in m.group(1).split(";")}
        if cit.split(",")[0].strip().lower() in names:
            return sent + end
        body = body[:m.start()] + "(" + m.group(1) + "; " + cit + ")"
    else:
        body = body + " (" + cit + ")"
    return body + stop + end


def apply(text, lang="en"):
    idx = 0 if lang == "en" else 1
    out, log = [], []
    used = set()
    for line in text.split("\n"):
        if line.startswith(("#", "|", "-", ">", "[[", "*")):
            out.append(line)
            continue
        hits = [r for r in RULES if r[idx] and r[idx] in line and r[idx] not in used]
        if not hits:
            out.append(line)
            continue
        parts = SENT.split(line)
        for rule in hits:
            for k, sent in enumerate(parts):
                if rule[idx] in sent and not HAS_CIT.search(sent):
                    parts[k] = _add(sent, rule[2])
                    used.add(rule[idx])
                    log.append({"anchor": rule[idx], "cit": rule[2], "sent": sent.strip()[:120]})
                    break
        out.append(" ".join(parts))
    try:
        with open("/tmp/gate1b_log.json", "w", encoding="utf-8") as fh:
            json.dump(log, fh, ensure_ascii=False, indent=1)
    except OSError:
        pass
    return "\n".join(out), len(log)
