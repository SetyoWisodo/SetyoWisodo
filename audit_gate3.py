# -*- coding: utf-8 -*-
"""Gate 3 — audit argumen & logika naskah buku.

Metrik:
  1. pengulangan frasa (5-gram) di dalam satu paragraf
  2. kalimat identik yang muncul di lebih dari satu bab
  3. kalimat berangka tanpa sitasi
  4. frasa template yang berulang
  5. rasio klaim absolut vs hedging
  6. pola fallacy yang dapat dideteksi otomatis (dilema palsu, overclaim kausal)
"""

import json
import re
import sys
import collections

ABS = ("proves", "proven", "undeniable", "undeniably", "inevitable",
       "inevitably", "certainly", "without doubt", "no doubt", "always",
       "never", "everyone", "no one", "must ", "cannot be stopped",
       "tidak dapat dibantah", "pasti akan", "selalu", "tidak pernah",
       "semua orang", "tidak mungkin dihentikan", "mutlak")
HEDGE = ("may", "might", "could", "likely", "plausible", "plausibly",
         "suggest", "appears", "remains uncertain", "depends", "range",
         "conditional", "not known", "unclear", "estimate",
         "kemungkinan", "mungkin", "cenderung", "tergantung", "rentang",
         "perkiraan", "belum pasti", "tidak jelas", "bersyarat")
FALLACY_PAT = {
    "false_dilemma": r"\b(?:only two (?:options|choices|paths)|no (?:third|middle) (?:option|ground)|must be either|binary choice|hanya ada dua|pilihannya hanya|tidak ada jalan ketiga)\b",
    "slippery_slope": r"\bwill lead (inevitably|directly) to\b",
    "appeal_authority": r"\bexperts (agree|say)\b",
    "absolute_causal": r"\bstr(?:ongly )?proves\b|\b(terbukti menyebabkan|pasti menyebabkan)\b",
}


def split_book(path):
    raw = open(path, encoding="utf-8").read()
    blocks = re.split(r"\n# (?=Chapter \d+|Bab \d+|Appendix|Lampiran|Preface|Prakata)", raw)
    out = []
    for b in blocks:
        head = b.split("\n", 1)[0].strip()
        out.append((head, b))
    return out


def paragraphs(block):
    for p in block.split("\n\n"):
        p = p.strip()
        if len(p.split()) < 40 or p.startswith("|") or p.startswith(">"):
            continue
        lines = [l for l in p.split("\n") if l.strip()]
        if lines and sum(1 for l in lines if l.lstrip().startswith(("-", "*"))) > len(lines) / 2:
            continue          # daftar, bukan prosa
        if p.startswith("[["):
            continue
        yield re.sub(r"\s+", " ", p)


def sentences(text):
    for s in re.split(r"(?<=[.!?])\s+", text):
        s = s.strip()
        if s:
            yield s


def audit(path):
    blocks = split_book(path)
    paras, all_sents = [], []
    for head, b in blocks:
        for p in paragraphs(b):
            paras.append((head, p))
            for s in sentences(p):
                all_sents.append((head, s))

    # 1. pengulangan 5-gram dalam satu paragraf
    worst = []
    for head, p in paras:
        w = p.lower().split()
        grams = collections.Counter(" ".join(w[i:i + 5]) for i in range(max(0, len(w) - 4)))
        g, n = grams.most_common(1)[0] if grams else ("", 0)
        worst.append((n, head, g))
    worst.sort(reverse=True)

    # 2. kalimat identik lintas bab
    sent_heads = collections.defaultdict(set)
    for head, s in all_sents:
        if len(s.split()) >= 8:
            sent_heads[s].add(head)
    cross_dups = {s: h for s, h in sent_heads.items() if len(h) > 1}

    # 3. kalimat berangka tanpa sitasi
    CITE = re.compile(r"\([A-Z][^)]{0,80}\d{4}[a-z]?\)|\bet al\.|\b(?:19|20)\d{2}\b")
    numeric = [s for _, s in all_sents if re.search(r"\d", s) and len(s.split()) >= 8]
    uncited = [s for s in numeric if not CITE.search(s)]
    paras_num = [p for _, p in paras if re.search(r"\d", p)]
    paras_uncited = [p for p in paras_num if not CITE.search(p)]

    # 4. frasa template
    text = "\n".join(p for _, p in paras)
    templates = {}
    for pat in ("Field data on", "Monitoring of", "Model projections that include",
                "Convergence across independent", "Key considerations emerging from",
                "Analysis for", "The literature on", "This is further underscored",
                "Pembahasan tentang", "Yang diketahui tentang", "Klaim tentang"):
        templates[pat] = text.count(pat)

    # 5. absolut vs hedging
    low = text.lower()
    abs_hits = sum(low.count(a) for a in ABS)
    abs_hits -= len(re.findall(r"\bproves (?:little|nothing)\b", low))
    hedge_hits = sum(low.count(h) for h in HEDGE)

    # 6. fallacy
    fallacies = {k: len(re.findall(v, text, re.I)) for k, v in FALLACY_PAT.items()}

    # per bab
    per_chapter = {}
    for head, p in paras:
        d = per_chapter.setdefault(head, {"paragraf": 0, "kata": 0, "max5": 0,
                                          "dup": 0, "angka_tanpa_sitasi": 0})
        d["paragraf"] += 1
        d["kata"] += len(p.split())
        w = p.lower().split()
        grams = collections.Counter(" ".join(w[i:i + 5]) for i in range(max(0, len(w) - 4)))
        d["max5"] = max(d["max5"], grams.most_common(1)[0][1] if grams else 0)
        if re.search(r"\d", p):
            d["angka"] = d.get("angka", 0) + 1
            if not CITE.search(p):
                d["angka_tanpa_sitasi"] += 1

    # paragraf identik
    para_counter = collections.Counter(p for _, p in paras)
    dup_paras = [(p, c) for p, c in para_counter.items() if c > 1]

    # statistik pengulangan kalimat
    rep = sorted(len(h) for s, h in sent_heads.items() if len(h) > 1)
    sent_counts = [len(h) for s, h in sent_heads.items() if len(h) > 1]

    return {
        "file": path,
        "paragraf_identik": len(dup_paras),
        "paragraf_identik_contoh": [p[:120] for p, c in dup_paras[:2]],
        "kalimat_ulang_maks": max(sent_counts) if sent_counts else 0,
        "kalimat_ulang_median": (sorted(sent_counts)[len(sent_counts)//2] if sent_counts else 0),
        "paragraf": len(paras),
        "kata_paragraf": sum(len(p.split()) for _, p in paras),
        "max_ulang_5gram": worst[0] if worst else (0, "", ""),
        "top5": worst[:5],
        "kalimat_lintas_bab": len(cross_dups),
        "contoh_duplikat": list(cross_dups)[:3],
        "kalimat_berangka": len(numeric),
        "tanpa_sitasi": len(uncited),
        "tanpa_sitasi_ketat": len([s for s in numeric
                                   if not re.search(r"\([A-Z][^)]{0,80}\d{4}[a-z]?\)", s)]),
        "persen_tanpa_sitasi_ketat": round(
            100.0 * len([s for s in numeric
                         if not re.search(r"\([A-Z][^)]{0,80}\d{4}[a-z]?\)", s)])
            / max(1, len(numeric)), 1),
        "persen_tanpa_sitasi": round(100 * len(uncited) / max(len(numeric), 1), 1),
        "paragraf_berangka": len(paras_num),
        "paragraf_tanpa_sitasi": len(paras_uncited),
        "persen_paragraf_tanpa_sitasi": round(100 * len(paras_uncited) / max(len(paras_num), 1), 1),
        "template": templates,
        "absolut": abs_hits,
        "hedging": hedge_hits,
        "fallacies": fallacies,
        "per_bab": per_chapter,
    }


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "book.md"
    print(json.dumps(audit(path), indent=2, ensure_ascii=False))
