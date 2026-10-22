# -*- coding: utf-8 -*-
"""Ganti satu paragraf (string literal multi-baris) di modul konten.

Paragraf di modul konten ditulis sebagai deret literal yang digabung implisit:

    "Kalimat pertama. "
    "Kalimat kedua.",

Alat ini mengambil deret itu, memastikan teks lamanya cocok, lalu menulis ulang
dengan pembungkusan baris yang rapi. Dipakai oleh skrip perbaikan paragraf.

Pemakaian sebagai modul:
    from para_tool import replace_paragraph
    replace_paragraph("content/depth_b.py", 334, "Teks baru yang lengkap.")
"""
import io
import re
import textwrap

WRAP = 96


def _literal_span(lines, start):
    """Kembalikan (i0, i1, teks) untuk literal yang memuat baris `start` (1-based)."""
    i = start - 1
    # naik ke awal paragraf: baris pertama setelah batas daftar (koma/kurawal)
    while i > 0:
        prev = lines[i - 1].rstrip()
        if prev.endswith(",") or prev.endswith("[") or prev.endswith("{") or prev.endswith(":"):
            break
        i -= 1
    j = i
    while j < len(lines):
        cur = lines[j].rstrip()
        if re.search(r'"\s*,$', cur):
            break
        if cur.endswith('"'):
            nxt = ""
            for k in range(j + 1, min(j + 4, len(lines))):
                if lines[k].strip():
                    nxt = lines[k].strip()
                    break
            if nxt[:1] in ("]", "}", ")"):
                break
        j += 1
    chunk = lines[i:j + 1]
    texts = []
    for ln in chunk:
        for m in re.finditer(r'"((?:[^"\\]|\\.)*)"', ln):
            texts.append(m.group(1))
    return i, j, "".join(texts)


def replace_paragraph(path, line_no, new_text, expect_prefix=None):
    lines = io.open(path, encoding="utf-8").read().split("\n")
    i0, i1, old = _literal_span(lines, line_no)
    if expect_prefix and not old.startswith(expect_prefix):
        raise AssertionError("%s:%d teks tak cocok.\n  ada : %s\n  minta: %s"
                             % (path, line_no, old[:90], expect_prefix[:90]))
    indent = re.match(r"\s*", lines[i0]).group(0)
    # baris terakhir mempertahankan koma penutup bila ada
    tail = lines[i1]
    comma = "," if tail.rstrip().endswith(",") else ""
    wrapped = textwrap.wrap(new_text, width=WRAP, break_long_words=False, break_on_hyphens=False)
    out = []
    for k, part in enumerate(wrapped):
        sep = "" if k == len(wrapped) - 1 else " "
        out.append('%s"%s%s"' % (indent, part, sep))
    out[-1] += comma
    lines[i0:i1 + 1] = out
    io.open(path, "w", encoding="utf-8").write("\n".join(lines))
    return len(old), len(new_text)


def find_paragraph(path, needle):
    """Baris (1-based) literal yang memuat `needle`."""
    for n, ln in enumerate(io.open(path, encoding="utf-8"), 1):
        if needle in ln:
            return n
    raise LookupError("%s: %r tidak ditemukan" % (path, needle[:60]))


def replace_by_needle(path, needle, new_text):
    """Cari paragraf lewat cuplikan teks, lalu ganti utuh (aman terhadap geseran baris)."""
    line = find_paragraph(path, needle)
    return replace_paragraph(path, line, new_text, expect_prefix=needle)
