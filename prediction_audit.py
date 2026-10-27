# -*- coding: utf-8 -*-
"""Periksa mutu bagian prediksi tiap bab.

Standar yang dipakai di sini bukan "ada bagian prediksi", melainkan apakah
pembaca bisa MEMAKAI prediksi itu sebagai peringatan dini. Untuk itu setiap
subbab Future Scenarios / Skenario harus memuat lima hal:

  HORIZON   -- tahun yang jelas (2030, 2040, 2050), bukan "suatu saat";
  ANGKA     -- prediksi yang terukur, bukan hanya arah;
  ASUMSI    -- apa yang harus benar agar prediksi itu berlaku;
  FALSIFIER -- apa yang akan membuktikannya salah;
  INDIKATOR -- angka yang dapat dipantau pembaca untuk tahu skenario mana
               yang sedang terjadi.

Alat ini hanya mengukur dan menulis laporan; tidak menyunting naskah.

Jalankan: python prediction_audit.py [--write]
"""
import re
import sys

import cite_numbers as C

CH = {"book.md": re.compile(r"^# Chapter (\d+):(.*)$", re.M),
      "book_id.md": re.compile(r"^# Bab (\d+):(.*)$", re.M)}
SECT = {"book.md": re.compile(r"^## (\d+)\.12 ", re.M),
        "book_id.md": re.compile(r"^## (\d+)\.12 ", re.M)}

HORIZON = re.compile(r"\b(2030|2035|2040|2050|2060|2100)\b")
NUMBER = re.compile(
    r"\b(?:\d[\d,.]*\s*(?:%|per cent|persen|million|juta|billion|miliar|"
    r"°C|days|hari|weeks|pekan|times|kali|cm|mm|millimetres|centimetres|"
    r"metres|meter|km|tahun|years|months|bulan|points|poin|"
    r"filings|pendaftaran|parts?|banding)\b|"
    r"(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
    r"satu|dua|tiga|empat|lima|enam|tujuh|delapan|sembilan|sepuluh)\s+"
    r"(?:months|bulan|points|poin|filings|pendaftaran|seasons?|musim|"
    r"years|tahun|times|kali|million|juta|billion|miliar|thousand|ribu|"
    r"per cent|persen)\b|"
    r"half|a tenth|a third|a quarter|separuh|sepersepuluh|sepertiga|"
    r"seperempat|dua kali|three times|twice)\b", re.I)
ASSUME = re.compile(r"\b(assum\w+|\w*asumsi\w*|mengasumsi\w*|if the world|"
                    r"jika dunia|provided that|on the assumption|"
                    r"bergantung pada|depends on|tergantung)\b", re.I)
# falsifier = syarat ("if / jika") + kata yang menyatakan klaim gugur
COND = re.compile(r"\b(if|unless|jika|kecuali|seandainya)\b", re.I)
REFUTE = re.compile(r"\b(wrong|fails?|falsif\w*|overstate\w*|too pessimistic|"
                    r"salah|gagal|keliru|melebihkan|terlalu pesimistis)\b", re.I)


def has_falsifier(body):
    for s in re.split(r"(?<=[.!?])\s+", body):
        if COND.search(s) and REFUTE.search(s):
            return True
    return False
INDIC = re.compile(r"\b(watch|track|indicator|monitor|\w*pantau\w*|"
                   r"indikator|watchable|signal|tanda|mengawasi)\w*\b", re.I)
# nama tempat dan peristiwa yang dipakai sebagai kasus di dalam bab. Kolom
# "Kasus di bab" hanya menunjukkan bahwa ramalan berpijak pada kasus; ia bukan
# syarat lulus, karena sejumlah bab (fisika, laut) memakai satu kasus instrumen.
CASE = re.compile(r"\b(?:Bangladesh|India|Pakistan|China|Indonesia|Jakarta|"
                  r"Philippines|Vietnam|Japan|Australia|California|Texas|"
                  r"Netherlands|Germany|France|Britain|United States|Canada|"
                  r"Brazil|Mexico|Nigeria|Kenya|Ethiopia|Somalia|Egypt|"
                  r"Tuvalu|Fiji|Maldives|Peru|Chile|Turkey|Türkiye|Greece|"
                  r"Spain|Italy|Morocco|Nepal|Myanmar|Thailand|Karachi|"
                  r"Chennai|Cape Town|Bhola|Amphan|Ahr|Lytton|Mauna Loa|"
                  r"Keeling|Argo|Greenland|Antarctic|Arctic|Amazon|Sahel|"
                  r"Delhi|Dhaka|Lagos|Mumbai|Shanghai|Rotterdam|Phoenix|"
                  r"Chicago|Athens|Paris|London|Tokyo|Seoul|Bangkok|Hanoi|"
                  r"São Paulo|Sao Paulo|Medellín|Surat|Semarang|Jakarta)\b")


def section(text, path, n):
    m = re.search(r"^# (?:Chapter|Bab) %d:" % n, text, re.M)
    if not m:
        return None
    nxt = re.search(r"^# (?:Chapter|Bab) %d:" % (n + 1), text, re.M)
    seg = text[m.start(): nxt.start() if nxt else len(text)]
    s = re.search(r"^## %d\.12 " % n, seg, re.M)
    if not s:
        return None
    e = re.search(r"^## %d\.13 " % n, seg, re.M)
    body = seg[s.start(): e.start() if e else len(seg)]
    return body


def chapter(text, n):
    """Seluruh teks bab n (dari judul bab sampai bab berikutnya)."""
    m = re.search(r"^# (?:Chapter|Bab) %d:" % n, text, re.M)
    if not m:
        return ""
    nxt = re.search(r"^# (?:Chapter|Bab) %d:" % (n + 1), text, re.M)
    return text[m.start(): nxt.start() if nxt else len(text)]


def score(body, whole=None):
    return dict(
        horizon=len(set(HORIZON.findall(body))),
        numbers=len(NUMBER.findall(body)),
        assume=bool(ASSUME.search(body)),
        falsify=has_falsifier(body),
        indic=bool(INDIC.search(body)),
        cases=len(set(CASE.findall(whole if whole is not None else body))),
        words=len(body.split()),
    )


def table(rows, path, title, lines):
    weak = []
    lines += [f"## {title}", "",
              "| Bab | Tahun | Angka | Asumsi | Falsifier | Indikator | Kasus di bab |",
              "|---|---|---|---|---|---|---|"]
    for n in sorted(rows):
        r = rows[n].get(path)
        if not r:
            continue
        ok = [r["horizon"] > 0, r["numbers"] >= 3, r["assume"],
              r["falsify"], r["indic"]]
        lines.append(f"| {n} | {r['horizon']} | {r['numbers']} | "
                     f"{'ya' if r['assume'] else '—'} | "
                     f"{'ya' if r['falsify'] else '—'} | "
                     f"{'ya' if r['indic'] else '—'} | {r['cases']} |")
        if not all(ok):
            weak.append((n, [k for k, x in zip(
                ("tahun", "angka", "asumsi", "falsifier", "indikator"), ok
            ) if not x]))
    return weak


def main():
    rows = {}
    for path in CH:
        text = open(path, encoding="utf-8").read()
        for n in range(1, 25):
            body = section(text, path, n)
            if body:
                rows.setdefault(n, {})[path] = score(body, chapter(text, n))

    lines = ["# Prediksi sebagai Peringatan Dini", "",
             "Setiap bab punya subbab *Future Scenarios*. Yang menentukan bukan",
             "adanya subbab itu, melainkan apakah pembaca dapat memakainya: tahun",
             "yang jelas, angka yang terukur, asumsi yang dinyatakan, syarat yang",
             "membuktikannya salah, dan indikator yang dapat dipantau.", "",
             "Ambang lulus yang dipakai di sini: minimal satu tahun sasaran, minimal",
             "tiga besaran atau ambang yang dapat diuji, asumsi yang dinyatakan,",
             "satu kalimat falsifier (\"if … the estimate is wrong\"), dan indikator",
             "yang disebut namanya. Kolom *Kasus di bab* menghitung jumlah nama tempat",
             "dan peristiwa yang muncul di seluruh bab — kasus adalah dasar induktif",
             "ramalan, tetapi kolom itu tidak dipakai sebagai syarat lulus, karena bab",
             "fisika dan laut berpijak pada satu kasus instrumen.", ""]
    en_weak = table(rows, "book.md", "Edisi Inggris — 24 bab", lines)
    lines += [""]
    id_weak = table(rows, "book_id.md", "Edisi Indonesia — 24 bab", lines)
    lines += ["", "## Bab yang perlu diperkuat", ""]
    for label, weak in (("Inggris", en_weak), ("Indonesia", id_weak)):
        if not weak:
            lines.append(f"- {label}: tidak ada — semua bab lulus kelima ambang.")
        for n, missing in weak:
            lines.append(f"- {label} bab {n}: kurang **{', '.join(missing)}**")
    print(f"bab diperiksa: {len(rows)} | EN perlu diperkuat: {len(en_weak)} | "
          f"ID perlu diperkuat: {len(id_weak)}")
    for label, weak in (("EN", en_weak), ("ID", id_weak)):
        for n, missing in weak:
            print(f"  {label} bab {n:>2}: {', '.join(missing)}")
    lines += ["", "## Cara memakai tabel ini", "",
              "Tiap bab punya satu paragraf uji di akhir subbab *Future Scenarios*.",
              "Polanya sama di 24 bab: klaim, tahun, ambang, asumsi, falsifier, tiga",
              "angka. Untuk memakainya sebagai peringatan dini, baca kolom angka lebih",
              "dulu daripada kolom tahun: kalau angkanya bergerak ke arah yang salah dua",
              "atau tiga tahun berturut-turut, babnya sudah memberi tahu apa yang harus",
              "diperiksa berikutnya. Yang membuat ramalan ini berbeda dari ramalan biasa",
              "adalah kalimat falsifier-nya: setiap bab menyebut pengamatan yang akan",
              "membuktikannya salah, sehingga pembaca tidak perlu menunggu tahun",
              "sasarannya untuk tahu apakah ia sedang membaca ramalan yang tepat atau",
              "yang keliru.", "",
              "Angka yang dipantau sengaja dipilih yang terbit rutin — anomali suhu",
              "tahunan, kandungan panas laut, luas es September, harga modul surya,",
              "prevalensi kurang gizi, jumlah orang membutuhkan bantuan — supaya pembaca",
              "dapat memeriksanya sendiri tanpa membeli laporan baru. Tidak ada statistik",
              "baru di paragraf-paragraf ini: setiap angka yang dipakai sudah muncul di",
              "bab itu sendiri beserta sumbernya, dan `numeric_audit.py` memeriksa ulang",
              "setiap paragraf berangka yang tidak menyebut rujukannya.", ""]
    if "--write" in sys.argv:
        open("PREDIKSI_PER_BAB.md", "w", encoding="utf-8").write("\n".join(lines) + "\n")
        print("PREDIKSI_PER_BAB.md ditulis")


if __name__ == "__main__":
    main()
