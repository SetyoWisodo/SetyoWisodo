# -*- coding: utf-8 -*-
"""Rapikan Daftar Pustaka: urutkan A–Z per subbagian, samakan bentuk nama.

Struktur yang dipertahankan:
    # References
    ## Works Cited / ## Karya yang Dikutip      -> entri yang dikutip di teks
    ## Further Reading / ## Bacaan Lanjutan      -> latar, tidak dikutip

`references.py` menyimpan gabungan keduanya, terurut, sehingga pemeriksa
sitasi tetap menemukan semua entri.

Jalankan: python sort_refs.py
"""
import re

import references as R

NAME_FIX = [
    ("Friedlingstein, Pierre et al.", "Friedlingstein, P. et al."),
    ("Friedlingstein, Pierre dkk.", "Friedlingstein, P. dkk."),
]

SUBS = {
    "book.md": ("# References", "# Index", ["## Works Cited", "## Further Reading"]),
    "book_id.md": ("# Daftar Pustaka", "# Indeks",
                   ["## Karya yang Dikutip", "## Bacaan Lanjutan"]),
}


def normalise(entry):
    for bad, good in NAME_FIX:
        entry = entry.replace(bad, good)
    return entry


def parse(path, start, end, subs):
    """Kembalikan (kepala, [(judul_sub, lede, [entri])], ekor)."""
    text = open(path, encoding="utf-8").read()
    i = text.find(start)
    j = text.find(end, i)
    head = text[:i + len(start)]
    tail = text[j:]
    seg = text[i + len(start):j]

    marks = [(seg.find(s), s) for s in subs]
    marks = sorted(m for m in marks if m[0] >= 0)
    if not marks:
        raise SystemExit("subbagian tidak ditemukan di %s" % path)

    out = []
    for k, (pos, title) in enumerate(marks):
        nxt = marks[k + 1][0] if k + 1 < len(marks) else len(seg)
        body = seg[pos + len(title):nxt]
        lede = []
        entries = []
        for line in body.split("\n"):
            if line.startswith("- "):
                entries.append(normalise(line[2:].strip()))
            elif line.strip() and not entries:
                lede.append(line.rstrip())
        out.append((title, lede, entries))
    return head, out, tail


def emit(path, head, blocks, tail):
    parts = [head.rstrip("\n")]
    for title, lede, entries in blocks:
        parts.append("\n" + title)
        if lede:
            parts.append("\n" + "\n".join(lede))
        parts.append("\n" + "\n".join("- " + e for e in sorted(set(entries), key=str.lower)))
    body = "\n".join(parts).rstrip("\n")
    tail = tail.lstrip("\n")
    # selalu sisakan satu baris kosong sebelum heading berikutnya (# Index / # Indeks)
    open(path, "w", encoding="utf-8").write(body + "\n\n" + tail)


def rewrite_py(entries_en, entries_id):
    src = open("references.py", encoding="utf-8").read()
    i = src.find("REFS_EN = [")
    j = src.find("REFS_ID = [")
    head = src[:i]
    close = src.find("]", j)
    tail = src[close + 1:]

    def block(name, entries):
        lines = ["%s = [" % name]
        for e in entries:
            lines.append('    "%s",' % e.replace('"', '\\"'))
        lines.append("]")
        return "\n".join(lines) + "\n"

    open("references.py", "w", encoding="utf-8").write(
        head + block("REFS_EN", entries_en) + "\n" + block("REFS_ID", entries_id) + tail)


def main():
    all_en, all_id = [], []
    for path in ("book.md", "book_id.md"):
        start, end, subs = SUBS[path]
        head, blocks, tail = parse(path, start, end, subs)
        emit(path, head, blocks, tail)
        for _title, _lede, entries in blocks:
            (all_en if path == "book.md" else all_id).extend(entries)
        counts = [(t.strip("# "), len(e)) for t, _l, e in blocks]
        print("%s: %s" % (path, counts))

    rewrite_py(sorted(set(all_en), key=str.lower), sorted(set(all_id), key=str.lower))

    # verifikasi
    import importlib
    importlib.reload(R)
    assert sorted(set(all_en), key=str.lower) == list(R.REFS_EN), "REFS_EN tidak sinkron"
    assert sorted(set(all_id), key=str.lower) == list(R.REFS_ID), "REFS_ID tidak sinkron"
    for path in ("book.md", "book_id.md"):
        start, end, subs = SUBS[path]
        _h, blocks, _t = parse(path, start, end, subs)
        for title, _l, entries in blocks:
            assert entries == sorted(entries, key=str.lower), "%s %s tidak A–Z" % (path, title)
    print("verifikasi: kedua subbagian A–Z, references.py sinkron (%d/%d entri)"
          % (len(R.REFS_EN), len(R.REFS_ID)))


if __name__ == "__main__":
    main()
