# -*- coding: utf-8 -*-
"""Cari paragraf Indonesia yang sepadan dengan sebuah paragraf Inggris.

Dipakai saat menyunting: setiap kali satu paragraf Inggris ditulis ulang,
paragraf Indonesianya harus ikut. Pencocokan memakai sidik jari yang tidak
berubah saat diterjemahkan -- ANGKA dan NAMA DIRI -- bukan urutan paragraf,
karena kedua edisi tidak selalu sejajar.

    from locate_id import find
    for score, idx, text in find(13, "The failures cascaded."):
        ...
"""
import re
import subprocess

import cite_numbers as C
from align_citations import features, split_chapters, CH_EN, CH_ID
from apply_more import despell_id

EN = open("book.md", encoding="utf-8").read()
ID = open("book_id.md", encoding="utf-8").read()
EC, IC = split_chapters(EN, CH_EN), split_chapters(ID, CH_ID)
EN_OLD = split_chapters(subprocess.run(
    ["git", "show", "HEAD:book.md"], capture_output=True, text=True,
    check=True).stdout, CH_EN)


def _paras(seg):
    return [p for p in re.split(r"\n\s*\n", seg) if C.is_body(p)]


def find(chapter, starts_with, top=3):
    """Paragraf Inggris lama (dari git) -> kandidat paragraf Indonesia."""
    old = [p for p in _paras(EN_OLD.get(chapter, "")) if p.startswith(starts_with)]
    if len(old) != 1:
        raise SystemExit(f"jangkar Inggris tidak unik ({len(old)}): {starts_with[:60]}")
    names, nums = features(old[0])
    scored = []
    for idx, p in enumerate(_paras(IC.get(chapter, ""))):
        n2, u2 = features(p)
        score = len(names & n2) * 2 + len(nums & u2) * 3
        scored.append((score, idx, p))
    scored.sort(key=lambda x: (-x[0], x[1]))
    return scored[:top]


def cut(chapter, index):
    """Potong paragraf Indonesia ke-indeks pada bab tertentu."""
    ps = _paras(IC.get(chapter, ""))
    return ps[index]
