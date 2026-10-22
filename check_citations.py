# -*- coding: utf-8 -*-
"""Audit silang sitasi dalam teks vs Daftar Pustaka.

Memeriksa dua edisi:
  book.md    -> REFS_EN
  book_id.md -> REFS_ID

Untuk setiap sitasi (kurung maupun naratif) ia mencocokkan nama belakang
dengan entri Daftar Pustaka, lalu membandingkan TAHUN. Keluaran:
  * tahun salah  : nama ada, tahun tidak ada  -> harus diperbaiki
  * nama tak ada : tidak ada entri sama sekali -> harus diperbaiki
  * entri tak dikutip: informasi, bukan error

Jalankan:  python check_citations.py [--verbose]
Keluar dengan kode 1 bila ada ketidakcocokan.
"""
import collections
import re
import sys

import references as R

PAIRS = [("book.md", R.REFS_EN, "# References", "en"),
         ("book_id.md", R.REFS_ID, "# Daftar Pustaka", "id")]

YEAR = r"(?:18|19|20)\d{2}[a-z]?"
# "Nama", "Nama et al.", "Nama dkk.", "Nama & Nama", "Nama, Nama and Nama"
BASE = r"[A-Z][A-Za-z\u00c0-\u00ff\-'\.]+"
WORD = BASE + r"(?:\s+" + BASE + r"){0,4}"
NAME = (WORD + r"(?:\s(?:et al\.?|dkk\.?))?"
        r"(?:\s*[&,]\s*" + WORD + r")*"
        r"(?:\s(?:and|dan)\s" + WORD + r")*")
PAREN = re.compile(r"\(([^()]{2,240})\)")
COMP = re.compile(r"^\s*(" + NAME + r")[,\s]+(" + YEAR + r")\b")
# catatan: sitasi boleh diikuti keterangan, mis. "(Arrhenius, 1896; model radiatif)"
NARR = re.compile(r"\b(" + NAME + r")\s\((" + YEAR + r")\)")


def ref_index(refs):
    """(segmen penulis huruf kecil, tahun) untuk setiap entri."""
    rows = []
    for entry in refs:
        m = re.search(r"\b" + YEAR + r"\b", entry)
        if not m:
            continue
        authors = entry[:m.start()].lower()
        rows.append((authors, m.group(0)))
    return rows


def ok_year(year, years):
    """Tahun di teks cocok bila persis, atau tanpa huruf dan ada varian berhuruf."""
    if year in years:
        return True
    if year[-1].isdigit():
        return year in {y.rstrip("abcdefgh") for y in years}
    return False


def resolve(first, rows):
    years = {y for authors, y in rows
             if re.search(r"(?<![a-z])" + re.escape(first) + r"(?![a-z])", authors)}
    return years or None


def scan(path, refs, cut_marker):
    rows = ref_index(refs)
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    # keluarkan hanya bagian Daftar Pustaka; lampiran lain ikut diperiksa
    if cut_marker in text:
        start = text.index(cut_marker)
        nxt = text.find("\n# ", start + len(cut_marker))
        text = text[:start] + (text[nxt:] if nxt > 0 else "")
    hits, bad = 0, []
    for m in PAREN.finditer(text):
        for part in m.group(1).split(";"):
            c = COMP.search(part)
            if not c:
                continue
            hits += 1
            first = c.group(1).split()[0].lower().rstrip(".,")
            year = c.group(2)
            years = resolve(first, rows)
            if years is None:
                bad.append(("NO-ENTRY", c.group(1), year, part.strip()[:110]))
            elif not ok_year(year, years):
                bad.append(("YEAR", c.group(1), year, sorted(years), part.strip()[:110]))
    for m in NARR.finditer(text):
        hits += 1
        first = m.group(1).split()[0].lower().rstrip(".,")
        year = m.group(2)
        years = resolve(first, rows)
        if years is None:
            bad.append(("NO-ENTRY", m.group(1), year, m.group(0)[:110]))
        elif not ok_year(year, years):
            bad.append(("YEAR", m.group(1), year, sorted(years), m.group(0)[:110]))
    cited = {b[1].split()[0].lower().rstrip(".,") for b in bad}
    for m in PAREN.finditer(text):
        for part in m.group(1).split(";"):
            c = COMP.search(part)
            if c:
                cited.add(c.group(1).split()[0].lower().rstrip(".,"))
    uncited = sorted({a.split()[0].strip(".,") for a, _ in rows
                      if len(a.split()[0]) > 2 and not any(k in a for k in cited)})
    return hits, bad, uncited


def main():
    verbose = "--verbose" in sys.argv
    total_bad = 0
    for path, refs, cut, lang in PAIRS:
        hits, bad, uncited = scan(path, refs, cut)
        total_bad += len(bad)
        print("=" * 70)
        print(f"{path}  ({lang})  sitasi terbaca: {hits}  masalah: {len(bad)}")
        for b in bad:
            if b[0] == "NO-ENTRY":
                print(f"  [tanpa entri] {b[1]}, {b[2]}   <- {b[3]}")
            else:
                print(f"  [tahun]  {b[1]}, {b[2]}  (Daftar Pustaka: {', '.join(b[3])})  <- {b[4]}")
        if verbose:
            print(f"  entri tak dikutip di badan: {len(uncited)}")
            for u in uncited[:40]:
                print("    -", u)
    print("=" * 70)
    print("TOTAL MASALAH:", total_bad)
    return 1 if total_bad else 0


if __name__ == "__main__":
    sys.exit(main())
