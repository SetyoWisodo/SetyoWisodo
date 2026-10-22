# -*- coding: utf-8 -*-
"""Audit konsistensi data (Gate 2).

Mencari klaim berangka yang bertentangan di dalam satu edisi: entitas dan
metrik yang sama, tetapi angkanya berbeda. Keluaran berupa daftar konflik yang
diurutkan menurut tingkat keparahan.

Jalankan: python data_consistency.py book.md [--json out.json]
"""
import collections
import json
import re
import sys

# satuan yang dibandingkan
UNIT = (r"(?:%|per cent|persen|°C|degrees?|cm|centimetres?|sentimeter|mm|milimeter|"
        r"million|billion|trillion|juta|miliar|ppm|ppb|gigatonnes?|gigaton|"
        r"tonnes?|ton|metres?|meter|kilometres?|km)")
NUM = r"(\d[\d.,]*)\s*(" + UNIT + r")"

# metrik yang sering muncul dengan angka
METRICS = [
    ("death toll", r"\b(killed|died|deaths?|meninggal|tewas|menewaskan|kematian)\b"),
    ("affected", r"\b(affected|terdampak|terkena)\b"),
    ("displaced", r"\b(displaced|tergusur|mengungsi|pengungsi)\b"),
    ("damage", r"\b(damage|kerugian|kerusakan)\b"),
    ("sea level rate", r"\b(sea level|muka laut|permukaan laut)\b"),
    ("warming", r"\b(warm(?:ed|ing)?|pemanasan|menghangat)\b"),
    ("concentration", r"\b(concentration|konsentrasi|parts per)\b"),
    ("yield", r"\b(yield|produktivitas|panen)\b"),
    ("cost", r"\b(cost|costs|biaya)\b"),
]


def sentences(text):
    out = []
    for line in text.split("\n"):
        if line.startswith(("#", "|", "-", "[[", ">")):
            continue
        out += [s.strip() for s in re.split(r"(?<=[.!?])\s+", line) if len(s.split()) > 7]
    return out


def norm_num(raw, is_id=False):
    """Baca angka dengan pemisah desimal/ribuan sesuai bahasa.

    EN: koma = ribuan, titik = desimal. ID: titik = ribuan, koma = desimal.
    Angka seperti "2.7" pada edisi Inggris harus tetap 2.7, bukan 27.
    """
    s = raw.strip().rstrip(".,")
    if not s:
        return None
    if "," in s and "." in s:
        # pemisah terakhir adalah desimal
        sep = "," if s.rfind(",") > s.rfind(".") else "."
        thou = "." if sep == "," else ","
        s = s.replace(thou, "").replace(sep, ".")
    elif is_id and "," in s:
        s = s.replace(".", "").replace(",", ".")
    else:
        s = s.replace(",", "")
    try:
        return float(s)
    except ValueError:
        return None


OPENERS = {"the", "this", "that", "these", "those", "chapter", "table", "about", "around",
           "more", "most", "some", "many", "nearly", "almost", "by", "in", "at", "on", "for",
           "from", "under", "over", "after", "before", "between", "during", "within", "when",
           "while", "if", "it", "they", "there", "here", "both", "each", "every", "no", "not",
           "sekitar", "lebih", "pada", "dari", "dalam", "dengan", "untuk", "jika", "ketika",
           "setelah", "sebelum", "antara", "selama", "jumlahnya", "kedua", "rata", "banyak",
           "sebagian", "hampir", "tidak", "ini", "itu", "dan", "tetapi", "namun", "kota",
           "warming", "pemanasan", "suhu", "temperature"}


def key_entities(sent):
    """Entitas: nama diri + tahun, dipakai sebagai kunci topik.

    Kata pembuka kalimat ("About", "Sekitar") bukan entitas; hanya frasa
    bermodal yang bukan kata umum yang dipakai sebagai kunci.
    """
    names = re.findall(r"\b([A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+){0,2})\b", sent)
    years = re.findall(r"\b(?:19|20)\d{2}\b", sent)
    kept = [n for n in names
            if n.lower() not in OPENERS and n.split()[0].lower() not in OPENERS and len(n) > 3]
    if not kept:
        return None
    return (kept[0].lower(), years[0] if years else "")


def audit(path):
    text = open(path, encoding="utf-8").read()
    is_id = "_id" in path
    body = text
    for marker in ("# References", "# Daftar Pustaka", "# Appendix D", "# Lampiran D"):
        if marker in body:
            i = body.index(marker)
            j = body.find("\n# ", i + len(marker))
            body = body[:i] + (body[j:] if j > 0 else "")
    buckets = collections.defaultdict(list)
    for sent in sentences(body):
        ents = key_entities(sent)
        if not ents:
            continue
        for label, pat in METRICS:
            if not re.search(pat, sent, re.I):
                continue
            nums = [(m.start(), m.end(), m) for m in re.finditer(NUM, sent)]
            if not nums:
                continue
            for mm in re.finditer(pat, sent, re.I):
                # angka yang paling dekat dengan kata metrik, bukan semua angka
                before = [n for n in nums if n[1] <= mm.start() + 1]
                after = [n for n in nums if n[0] >= mm.end() - 1]
                pick = before[-1] if before else (after[0] if after else None)
                if pick is None:
                    continue
                if before and mm.start() - pick[1] > 80:
                    continue
                if not before and after and pick[0] - mm.end() > 60:
                    continue
                val = norm_num(pick[2].group(1), is_id)
                if val is None:
                    continue
                unit = pick[2].group(2).lower()
                buckets[(ents[0], ents[1], label, unit)].append((val, sent[:170]))
    conflicts = []
    for key, vals in buckets.items():
        distinct = sorted({round(v, 4) for v, _ in vals})
        if len(distinct) > 1:
            biggest = max(distinct)
            smallest = min(distinct)
            if smallest == 0:
                continue
            ratio = biggest / smallest
            conflicts.append({
                "entity": key[0], "year": key[1], "metric": key[2], "unit": key[3],
                "values": distinct[:6], "ratio": round(ratio, 2),
                "examples": [s for _, s in vals][:3],
            })
    conflicts.sort(key=lambda c: -c["ratio"])
    return conflicts


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "book.md"
    out = sys.argv[3] if len(sys.argv) > 3 and sys.argv[2] == "--json" else None
    conf = audit(path)
    if out:
        json.dump(conf, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{path}: {len(conf)} kandidat konflik angka")
    for c in conf[:25]:
        print(f"\n[{c['entity']} {c['year']} · {c['metric']} · {c['unit']}] "
              f"nilai: {c['values']} (rasio {c['ratio']})")
        for e in c["examples"]:
            print("   -", e.replace("\n", " ")[:170])
    return 0


if __name__ == "__main__":
    sys.exit(main())
