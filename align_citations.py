# -*- coding: utf-8 -*-
"""Pindahkan sitasi dari edisi Inggris ke edisi Indonesia lewat penjajaran paragraf.

Edisi Indonesia bukan terjemahan baris-per-baris: urutan dan pembagian
paragrafnya berbeda, jadi nomor paragraf tidak bisa dipakai. Yang dipakai di
sini adalah sidik jari yang tidak berubah saat diterjemahkan: NAMA DIRI dan
ANGKA.

Aturan kehati-hatian:
  * paragraf Indonesia hanya dicocokkan dengan paragraf di bab yang sama;
  * skor minimal 3 (tiga nama/angka yang sama), dan pemenangnya harus tunggal;
  * paragraf Inggris harus punya TEPAT SATU sitasi berbeda -- kalau ada dua,
    tidak ada yang dipindahkan karena tidak jelas mana yang berlaku;
  * sitasi ditaruh pada kalimat Indonesia yang memuat angka yang cocok.

Kalau ragu, alat ini tidak melakukan apa pun. Lebih baik kosong daripada salah.

Jalankan: python align_citations.py [--dry-run]
"""
import re
import sys

import cite_numbers as C
from apply_more import despell_id

PROPER = re.compile(r"\b([A-Z][a-z\u00e0-\u00ff]{3,})\b")
STOPW = {"the", "this", "that", "these", "those", "there", "their", "which",
         "where", "after", "before", "during", "between", "because",
         "although", "however", "another", "world", "other", "about", "every",
         "first", "second", "third", "some", "when", "what", "with", "from",
         "into", "over", "than", "then", "they", "have", "were", "will"}
CH_EN = re.compile(r"^# Chapter (\d+):", re.M)
CH_ID = re.compile(r"^# Bab (\d+):", re.M)
STRICT_CITE = re.compile(r"^\(?[A-Z][^()]{0,80}?, (?:19|20)\d{2}[a-z]?\)?$")
# pasangan kata Indonesia <-> Inggris yang setara, untuk mendeteksi atribusi
# yang sudah ditulis di dalam kalimat ("Bank Dunia memperkirakan ...")
INST = (("bank dunia", "world bank"), ("who", "who"), ("ipcc", "ipcc"),
        ("fao", "fao"), ("iea", "iea"), ("unhcr", "unhcr"),
        ("undrr", "undrr"), ("organisasi kesehatan dunia", "world health"),
        ("badan energi internasional", "international energy"))


def features(text):
    names = {w.lower() for w in PROPER.findall(text) if w.lower() not in STOPW}
    peeled = despell_id(C.despell(text))
    nums = {m.replace(",", "").replace(".", "")
            for m in re.findall(r"\d[\d,.]*", peeled) if len(m) >= 2}
    return names, nums


def split_chapters(text, rx):
    marks = [(int(m.group(1)), m.start()) for m in rx.finditer(text)]
    out = {}
    for i, (n, s) in enumerate(marks):
        e = marks[i + 1][1] if i + 1 < len(marks) else len(text)
        out[n] = text[s:e]
    return out


def paragraphs(seg):
    return [b for b in re.split(r"\n\s*\n", seg) if C.is_body(b)]


def main():
    dry = "--dry-run" in sys.argv
    en = open("book.md", encoding="utf-8").read()
    idn = open("book_id.md", encoding="utf-8").read()
    en_ch, id_ch = split_chapters(en, CH_EN), split_chapters(idn, CH_ID)

    # kalimat Inggris bersitasi, per bab
    en_sents = {}
    for n, seg in en_ch.items():
        rows = []
        for s in C.sentences(seg):
            if not C.PAREN.search(s):
                continue
            cites = {c for c in C.PAREN.findall(s) if STRICT_CITE.match(c.strip("()"))}
            if len(cites) != 1:
                continue
            names, nums = features(s)
            rows.append((names, nums, next(iter(cites)), s))
        en_sents[n] = rows

    moved, skipped = [], 0
    id_out = {}
    for n, seg in id_ch.items():
        blocks = re.split(r"\n\s*\n", seg)
        for i, b in enumerate(blocks):
            if not C.is_body(b) or C.PAREN.search(b) or not C.QUANTITY.search(b):
                continue
            sents = C.sentences(b)
            for j, s in enumerate(sents):
                if C.PAREN.search(s) or not C.QUANTITY.search(s):
                    continue
                names, nums = features(s)
                if not nums:
                    continue
                best, best_score, second = None, 0, 0
                for en_names, en_nums, cite, _src in en_sents.get(n, []):
                    if not (names & en_names) and not (nums & en_nums):
                        continue
                    score = len(names & en_names) + 2 * len(nums & en_nums)
                    if score > best_score:
                        second, best, best_score = best_score, cite, score
                    elif score > second:
                        second = score
                prose_attr = False
                if best:
                    low_s, low_c = s.lower(), best.lower()
                    prose_attr = any(a in low_s and b in low_c for a, b in INST)
                    prose_attr = prose_attr or any(
                        n.lower() in low_s for n in names if len(n) > 3 and n.lower() in low_c)
                if best and best_score >= 3 and best_score > second and not prose_attr:
                    new_s = C.insert_cite(s, best)
                    if new_s:
                        sents[j] = new_s
                        moved.append((n, best, new_s[:80]))
                else:
                    skipped += 1
            blocks[i] = " ".join(sents)
        id_out[n] = "\n\n".join(blocks)

    print(f"ID: {len(moved)} sitasi dipindahkan, {skipped} kalimat dilewati")
    for n, c, s in moved:
        print(f"   bab {n:>2} {c:30} {s[:60]}")
    if not dry:
        out = idn
        for n, seg in id_ch.items():
            out = out.replace(seg, id_out[n])
        open("book_id.md", "w", encoding="utf-8").write(out)


if __name__ == "__main__":
    main()
