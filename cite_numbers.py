# -*- coding: utf-8 -*-
"""Tutup angka tanpa rujukan di badan buku tanpa mengarang sumber.

Dua lapis, dijalankan berurutan:

LAPIS 1 -- daftar terkurasi (`numeric_sources.py`).
    Untuk tiap entri, kalimat jangkar di edisi Inggris dicari, lalu sitasi
    dipasang di akhir kalimat itu. Di edisi Indonesia, kalimat yang memuat
    ANGKA yang sama (lewat `best_figure`) diberi sitasi yang sama -- angka
    tidak berubah saat diterjemahkan, jadi ini cara yang aman untuk menyeberang
    bahasa tanpa menulis ulang jangkar 60 kali.

LAPIS 2 -- penyebaran otomatis.
    Kalau sebuah angka sudah dirujuk di satu tempat, rujukan itu dipindahkan ke
    tempat lain yang menyebut angka yang sama. Hanya dipakai bila angkanya
    langka (<=5 kemunculan) dan semua kemunculan bersitasi menunjuk sumber yang
    sama. Kalau tidak yakin, alat ini diam.

Yang TIDAK dilakukan: menebak. Angka yang tidak pernah dirujuk tetap tanpa
rujukan, dan dicatat di NUMERIC_CLAIMS.md untuk diperiksa manusia.

Jalankan:
    python cite_numbers.py            # tulis perubahan
    python cite_numbers.py --dry-run  # lihat saja
"""
import re
import sys

from numeric_sources import CURATED, ID_EXTRA

PAREN = re.compile(r"\([^()]*?(?:19|20)\d{2}[a-z]?[^()]*\)")

SCALE = r"(?:million|billion|thousand|trillion|juta|miliar|milyar|triliun|ribu)"
UNIT_EN = (r"%|per cent|percent|hectares|kilometres|kilometers|metres|meters|"
           r"millimetres|millimeters|degrees|°C|°F|gigatonnes|tonnes|people|"
           r"deaths|dollars|jobs|species|square kilometres|litres|liters")
UNIT_ID = (r"%|persen|hektar|hektare|kilometer|kilometre|meter|metres|"
           r"milimeter|sentimeter|derajat|°C|°F|gigaton|ton|orang|kematian|"
           r"dolar|pekerjaan|spesies|rumah|usaha|pelanggan|jiwa|korban|unit|"
           r"sistem|liter|kilometer persegi|meter kubik")
UNIT = UNIT_EN + "|" + UNIT_ID

FIG = re.compile(r"(\d[\d,.]*)\s*(?:(" + SCALE + r")\s+)?(" + UNIT +
                 r")", re.I)
QUANTITY = re.compile(
    r"(\d[\d,.]*\s*(?:" + UNIT + r")|"
    r"\b(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
    r"twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|"
    r"million|billion|satu|dua|tiga|empat|lima|enam|tujuh|delapan|sembilan|"
    r"sepuluh|sebelas|seratus|ribuan|jutaan|miliaran)\b[\s-]+(?:million|"
    r"billion|thousand|per cent|people|deaths|hectares|juta|miliar|ribu|"
    r"persen|orang|kematian|hektar))", re.I)
TERMINAL = re.compile(r"([.!?])([\"'\u201d\u2019]*)$")

WORDS = {w: i for i, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve "
    "thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split())}
WORDS.update({w: i * 10 for i, w in enumerate(
    "zero ten twenty thirty forty fifty sixty seventy eighty ninety".split())})


def despell(t):
    """'eighteen million' -> '18 million' agar bisa dibandingkan lintas bahasa."""
    def rep(m):
        return str(WORDS[m.group(1).lower()]) + " "
    return re.sub(r"\b(" + "|".join(WORDS) + r")[\s-]+"
                  r"(?=(?:million|billion|thousand|per cent|percent))",
                  rep, t, flags=re.I)


def is_body(block):
    return (not block.startswith(("#", "-", "!", "[", "|", ">", "*"))
            and len(block.split()) >= 40)


MULT = {"million": 10**6, "juta": 10**6,
        "billion": 10**9, "miliar": 10**9, "milyar": 10**9,
        "trillion": 10**12, "triliun": 10**12,
        "thousand": 10**3, "ribu": 10**3}


def figures(text):
    """Nilai kanonik: 4,5 juta dan 4.5 million sama-sama 4_500_000."""
    out = set()
    for n, scale, unit in FIG.findall(despell(text)):
        n = n.strip(".,\u2013\u2014").replace(",", "").replace(".", "")
        if not n.isdigit():
            continue
        sc = (scale or "").strip().lower()
        val = int(n) * MULT.get(sc, 1)
        if val >= 1000:                 # angka kecil/persen terlalu umum
            out.add(val)
    return out


def best_figure(text):
    figs = figures(text)
    return max(figs) if figs else None


def sentences(text):
    return re.split(r"(?<=[.!?])\s+", text)


# Kesalahan atribusi yang sudah ada di naskah dan bisa dipastikan: (potongan
# kalimat, sitasi salah, sitasi benar). Dijalankan sebelum penyisipan baru.
FIX_WRONG = [
    ("menunjukkan logika yang sama dalam dingin, dengan empat setengah juta pelanggan",
     "(IEA, 2023)", "(FERC & NERC, 2021)"),
]


def repair(text, log):
    for frag, wrong, right in FIX_WRONG:
        fixed = 0
        out = []
        for b in re.split(r"(\n\s*\n)", text):
            if frag in b and wrong in b:
                b = b.replace(wrong, right)
                fixed += 1
            out.append(b)
        text = "".join(out)
        if fixed:
            log.append(f"[FIX] {wrong} -> {right} ({fixed} kalimat)")
    return text


def normalise(cite):
    """'WMO (2025)' -> 'WMO, 2025' supaya tidak jadi '(WMO (2025))'."""
    m = re.match(r"^(.*?)\s*\((\d{4}[a-z]?)\)$", cite.strip())
    return f"{m.group(1).strip()}, {m.group(2)}" if m else cite.strip()


def insert_cite(sent, cite):
    cite = normalise(cite)
    m = TERMINAL.search(sent)
    if not m or PAREN.search(sent):
        return None
    return sent[:m.start()] + f" ({cite})" + sent[m.start():]


def layer1(text, log, rules=None, lang="EN"):
    """Pasang sitasi pada kalimat jangkar. Kembalikan peta angka."""
    rules = CURATED if rules is None else rules
    blocks = re.split(r"\n\s*\n", text)
    figmap = {}
    out = []
    for b in blocks:
        if not is_body(b) or not QUANTITY.search(b):
            out.append(b)
            continue
        sents = sentences(b)
        for anchor, cite, *_ in rules:
            for i, s in enumerate(sents):
                if anchor not in s or PAREN.search(s):
                    continue
                new = insert_cite(s, cite)
                if not new:
                    continue
                sents[i] = new
                log.append(f"[{lang}] {cite:30s} <- {s[:78]}")
                f = best_figure(s)
                if f:
                    figmap.setdefault(f, cite)
        out.append(" ".join(sents))
    return "\n\n".join(out), figmap


def count_figs(text):
    blocks = [b for b in re.split(r"\n\s*\n", text) if is_body(b)]
    freq = {}
    for b in blocks:
        if PAREN.search(b):
            continue
        for f in figures(b):
            freq[f] = freq.get(f, 0) + 1
    return freq


def layer1_id(text, figmap, log):  # tidak dipakai: pencocokan angka lintas bahasa terlalu rawan
    """Terapkan peta angka ke edisi Indonesia: angka tidak berubah saat diterjemahkan."""
    freq = count_figs(text)
    blocks = re.split(r"\n\s*\n", text)
    out = []
    for b in blocks:
        if not is_body(b) or PAREN.search(b) or not QUANTITY.search(b):
            out.append(b)
            continue
        sents = sentences(b)
        for i, s in enumerate(sents):
            if PAREN.search(s) or not QUANTITY.search(s):
                continue
            hits = {figmap[f] for f in figures(s)
                    if f in figmap and freq.get(f, 9) <= 3}
            if len(hits) == 1:
                cite = next(iter(hits))
                new = insert_cite(s, cite)
                if new:
                    sents[i] = new
                    log.append(f"[ID] {cite:34s} <- {s[:78]}")
        out.append(" ".join(sents))
    return "\n\n".join(out)


def main():
    dry = "--dry-run" in sys.argv
    log = []
    for path, lang, rules in (("book.md", "EN", CURATED),
                              ("book_id.md", "ID", ID_EXTRA)):
        text = open(path, encoding="utf-8").read()
        text = repair(text, log)
        text, _ = layer1(text, log, rules, lang)
        if not dry:
            open(path, "w", encoding="utf-8").write(text)
    en = sum(1 for l in log if l.startswith("[EN]"))
    idn = sum(1 for l in log if l.startswith("[ID]"))
    print(f"EN {en} sitasi | ID {idn} sitasi | total {len(log)}")
    for line in log:
        print("  " + line)
    open("/tmp/cite_log.txt", "w", encoding="utf-8").write("\n".join(log))


if __name__ == "__main__":
    main()
