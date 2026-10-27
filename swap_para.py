# -*- coding: utf-8 -*-
"""Ganti satu paragraf badan menurut nomor bab + nomor urut paragraf.

Dipanggil lewat skrip sunting agar setiap perubahan punya jangkar yang bisa
diperiksa: paragraf baru hanya ditulis kalau paragraf lama masih dimulai dengan
awalan yang disebutkan. Tanpa awalan yang cocok, skrip berhenti -- bukan
menimpa paragraf yang salah secara diam-diam.

Pemakaian:
    from swap_para import swap
    swap("book.md", 13, 75, "The failures cascaded.", "teks baru ...")
"""
import re

import cite_numbers as C

CH = {"book.md": re.compile(r"^# Chapter (\d+):", re.M),
      "book_id.md": re.compile(r"^# Bab (\d+):", re.M)}


def _chapter_span(text, path, n):
    marks = [(int(m.group(1)), m.start()) for m in CH[path].finditer(text)]
    hit = [i for i, (k, _) in enumerate(marks) if k == n]
    if not hit:
        raise SystemExit(f"bab {n} tidak ditemukan di {path}")
    i = hit[0]
    s = marks[i][1]
    e = marks[i + 1][1] if i + 1 < len(marks) else len(text)
    return s, e


def swap(path, chapter, index, starts_with, new, expect_words_min=40):
    text = open(path, encoding="utf-8").read()
    s, e = _chapter_span(text, path, chapter)
    blocks = re.split(r"\n\s*\n", text[s:e])
    body = [i for i, b in enumerate(blocks) if C.is_body(b)]
    if index >= len(body):
        raise SystemExit(f"{path} bab {chapter}: hanya {len(body)} paragraf badan")
    bi = body[index]
    old = blocks[bi]
    if not old.startswith(starts_with):
        raise SystemExit(f"{path} bab {chapter} paragraf {index} tidak cocok:\n"
                         f"  diharapkan: {starts_with[:70]}\n"
                         f"  ditemukan : {old[:70]}")
    if len(new.split()) < expect_words_min:
        raise SystemExit(f"paragraf baru terlalu pendek ({len(new.split())} kata)")
    blocks[bi] = new.strip()
    out = text[:s] + "\n\n".join(blocks) + text[e:]
    if out.count("\n\n\n"):
        raise SystemExit("ada baris kosong ganda")
    open(path, "w", encoding="utf-8").write(out)
    return old


def drop(path, chapter, index, starts_with):
    """Buang satu paragraf badan (hanya untuk pengulangan, bukan studi kasus)."""
    text = open(path, encoding="utf-8").read()
    s, e = _chapter_span(text, path, chapter)
    blocks = re.split(r"\n\s*\n", text[s:e])
    body = [i for i, b in enumerate(blocks) if C.is_body(b)]
    bi = body[index]
    if not blocks[bi].startswith(starts_with):
        raise SystemExit(f"{path} bab {chapter} paragraf {index} tidak cocok")
    gone = blocks[bi]
    del blocks[bi]
    out = text[:s] + "\n\n".join(blocks) + text[e:]
    if out.count("\n\n\n"):
        raise SystemExit("ada baris kosong ganda")
    open(path, "w", encoding="utf-8").write(out)
    return gone


def show(path, chapter, index, width=1400):
    text = open(path, encoding="utf-8").read()
    s, e = _chapter_span(text, path, chapter)
    blocks = re.split(r"\n\s*\n", text[s:e])
    body = [i for i, b in enumerate(blocks) if C.is_body(b)]
    return blocks[body[index]][:width]
