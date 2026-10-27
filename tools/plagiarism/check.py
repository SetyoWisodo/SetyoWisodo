# -*- coding: utf-8 -*-
"""Pemeriksa kemiripan lengkap untuk Surviving the Future.

Menjalankan tiga lapis pemeriksaan dan menuliskan satu laporan:

  lapis 1  internal   -- semua bab dibandingkan satu sama lain (winnowing)
  lapis 2  kalimat    -- kalimat nyaris sama + duplikasi persis (audit_plagiarism)
  lapis 3  eksternal  -- daftar kalimat khas per bab untuk diuji ke web

Lapis 3 tidak bisa diotomatiskan di sini: mesin pencari membutuhkan kunci API
atau akses jaringan penuh. Skrip ini MENYIAPKAN kalimatnya, lalu hasil
penelusurannya dicatat manual di PHRASE_TESTS.md. Itu bukan kelemahan --
justru itu satu-satunya cara jujur menyebut sumbernya satu per satu.

Pemakaian:
    python tools/plagiarism/check.py                 # jalankan semua lapis
    python tools/plagiarism/check.py --picks 24      # ambil 24 kalimat uji
"""
import argparse
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)

import winnow  # noqa: E402

WORK = "/tmp/plagiarism_work"


def split_chapters(src, tag):
    d = os.path.join(WORK, "chapters")
    os.makedirs(d, exist_ok=True)
    s = open(os.path.join(ROOT, src), encoding="utf-8").read()
    parts = re.split(r"(?m)^# ", s)
    n = 0
    for p in parts[1:]:
        head = p.split("\n", 1)[0].strip()
        if not re.match(r"(Chapter|Bab)\s+\d+", head):
            continue
        n += 1
        body = p.split("\n", 1)[1] if "\n" in p else ""
        open(os.path.join(d, f"{tag}_ch{n:02d}.txt"), "w", encoding="utf-8").write(body)
    return n


def pick_sentences(src, per_chapter=1, lo=18, hi=38):
    """Ambil kalimat paling khas tiap bab: kaya kata unik, mengandung angka."""
    s = open(os.path.join(ROOT, src), encoding="utf-8").read()
    chaps = re.split(r"(?m)^# Chapter (\d+)[^\n]*\n", s)

    def score(t):
        w = re.findall(r"[a-z]+", t.lower())
        if not w:
            return 0
        return len(set(w)) / len(w) + (0.5 if re.search(r"\d", t) else 0)

    out = []
    for i in range(1, len(chaps) - 1, 2):
        num = int(chaps[i])
        sents = [x.strip() for x in re.split(r"(?<=[.!?])\s+", chaps[i + 1])
                 if lo <= len(x.split()) <= hi]
        for t in sorted(sents, key=score, reverse=True)[:per_chapter]:
            out.append((num, t))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--picks", type=int, default=12)
    a = ap.parse_args()

    os.makedirs(WORK, exist_ok=True)
    print("=" * 74)
    print("LAPIS 1 — KEMIRIPAN INTERNAL (winnowing, k=8 kata)")
    print("=" * 74)
    for src, tag in (("book.md", "EN"), ("book_id.md", "ID")):
        split_chapters(src, tag)

    rows, score = winnow.run([os.path.join(WORK, "chapters")],
                             [os.path.join(WORK, "chapters")],
                             k=8, window=4, floor=0.02)

    print()
    print("=" * 74)
    print("LAPIS 2 — DUPLIKASI KALIMAT & DISIPLIN KUTIPAN")
    print("=" * 74)
    subprocess.run([sys.executable, os.path.join(ROOT, "audit_plagiarism.py")])

    print()
    print("=" * 74)
    print("LAPIS 3 — KALIMAT UNTUK DIUJI KE WEB (kata per kata, dengan tanda kutip)")
    print("=" * 74)
    picks = pick_sentences("book.md", per_chapter=1)[:a.picks]
    for n, t in picks:
        print(f"CH{n:02d}  {t}")
    print(f"\n{len(picks)} kalimat siap diuji. Catat hasilnya di PHRASE_TESTS.md.")

    print()
    print("=" * 74)
    print(f"SKOR INTERNAL: {score*100:.2f}%  (cakupan kata terhadap korpus 48 bab)")
    print("=" * 74)


if __name__ == "__main__":
    main()
