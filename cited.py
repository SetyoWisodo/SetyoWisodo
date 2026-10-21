# -*- coding: utf-8 -*-
"""Pemisah Daftar Pustaka: karya yang benar-benar dikutip vs bacaan lanjutan.

Dipakai oleh gen_book.py / gen_book_id.py agar tidak ada entri menggantung:
entri yang tidak pernah muncul sebagai sitasi di badan dipindahkan ke bagian
"Further Reading" / "Bacaan Lanjutan", bukan dibiarkan bercampur.
"""
import re

from check_citations import COMP, NARR, PAREN

YEAR_ANY = re.compile(r"\b(?:18|19|20)\d{2}[a-z]?\b")


def pairs(text):
    """Himpunan (nama-depan huruf kecil, tahun) dari seluruh sitasi."""
    out = set()
    for m in PAREN.finditer(text):
        for part in m.group(1).split(";"):
            c = COMP.search(part)
            if c:
                out.add((c.group(1).split()[0].lower().rstrip(".,"), c.group(2)))
    for m in NARR.finditer(text):
        out.add((m.group(1).split()[0].lower().rstrip(".,"), m.group(2)))
    return out


def is_cited(entry, seen):
    m = YEAR_ANY.search(entry)
    if not m:
        return False
    author = entry[:m.start()].lower()
    year = m.group(0)
    first = entry.split(",")[0].split()[0].lower().rstrip(".,")
    for name, cited_year in seen:
        if cited_year.rstrip("abcdefgh") != year.rstrip("abcdefgh"):
            continue
        if name == first:
            return True
        if re.search(r"(?<![a-z])" + re.escape(name) + r"(?![a-z])", author):
            return True
    return False


def split_refs(refs, seen):
    ordered = sorted(refs, key=lambda x: x.lower())
    cited = [r for r in ordered if is_cited(r, seen)]
    further = [r for r in ordered if not is_cited(r, seen)]
    return cited, further
