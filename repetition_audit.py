# -*- coding: utf-8 -*-
"""Ukur pengulangan di dalam bab, sebelum dan sesudah penyuntingan.

Dua ukuran, keduanya dihitung per bab (pengulangan antar-bab memang disengaja:
buku ini merujuk balik):

  1. Pasangan paragraf dengan kemiripan kosinus >= 0.40 (kata isi berbobot
     IDF). Ini menangkap paragraf yang membahas hal yang sama dengan kata-kata
     berbeda -- bukan plagiasi, tetapi pengulangan yang terasa bagi pembaca.
  2. Pasangan yang melibatkan paragraf PEMBUKA bab (>= 0.30), karena pola
     "vignette dibuka, lalu diceritakan ulang di studi kasus" adalah bentuk
     pengulangan yang paling sering ditemukan di naskah ini.

Pembanding "sebelum" diambil dari `git show HEAD:<file>`, sehingga angkanya
bisa diperiksa ulang kapan saja.

Jalankan: python repetition_audit.py [--write]
"""
import math
import re
import subprocess
import sys
from collections import Counter

import cite_numbers as C

CH = re.compile(r"^# (?:Chapter|Bab) (\d+):", re.M)
FILES = ["book.md", "book_id.md"]


def toks(text):
    return re.findall(r"[a-z\u00e0-\u00ff]{4,}", text.lower())


def chapters(text):
    marks = [(int(m.group(1)), m.start()) for m in CH.finditer(text)]
    out = []
    for i, (n, s) in enumerate(marks):
        e = marks[i + 1][1] if i + 1 < len(marks) else len(text)
        paras = [p for p in re.split(r"\n\s*\n", text[s:e]) if C.is_body(p)]
        out.append((n, paras))
    return out


def pairs(text):
    chap = chapters(text)
    df = Counter()
    for _n, ps in chap:
        for p in ps:
            for w in set(toks(p)):
                df[w] += 1
    total = max(1, sum(len(p) for _n, p in chap))
    weight = {w: math.log(total / (1 + c)) for w, c in df.items()}

    def vec(p):
        c = Counter(toks(p))
        v = {w: (1 + math.log(x)) * weight[w] for w, x in c.items()}
        nrm = math.sqrt(sum(x * x for x in v.values())) or 1.0
        return {w: x / nrm for w, x in v.items()}

    inner, opener = [], []
    for n, ps in chap:
        V = [vec(p) for p in ps]
        for a in range(len(ps)):
            for b in range(a + 1, len(ps)):
                s = sum(x * V[b].get(w, 0.0) for w, x in V[a].items())
                if a == 0 and s >= 0.30:
                    opener.append((round(s, 2), n, b, ps[a][:150], ps[b][:150]))
                elif s >= 0.40:
                    inner.append((round(s, 2), n, a, b, ps[a][:150], ps[b][:150]))
    inner.sort(reverse=True)
    opener.sort(reverse=True)
    return inner, opener


def main():
    lines = ["# Pengulangan di Dalam Bab", "",
             "Ukuran: kemiripan kosinus antarparagraf dalam bab yang sama, dengan",
             "bobot IDF. Dihitung sebelum dan sesudah pass penyuntingan; angka",
             "\"sebelum\" berasal dari `git show HEAD:` sehingga bisa diperiksa.",
             ""]
    rows = []
    for path in FILES:
        now = open(path, encoding="utf-8").read()
        old = subprocess.run(["git", "show", f"HEAD:{path}"],
                             capture_output=True, text=True).stdout
        i0, o0 = pairs(old)
        i1, o1 = pairs(now)
        rows.append((path, len(i0), len(i1), len(o0), len(o1)))
        print(f"{path}: paragraf-dalam-bab {len(i0)} -> {len(i1)} | "
              f"pembuka {len(o0)} -> {len(o1)}")
        lines += [f"## {path}", "",
                  f"- Paragraf dalam bab mirip >= 0.40: **{len(i0)} -> {len(i1)}**",
                  f"- Paragraf yang mengulang pembuka bab >= 0.30: "
                  f"**{len(o0)} -> {len(o1)}**", "",
                  "### Sisa (perlu dibaca manusia)", ""]
        for s, n, a, b, pa, pb in i1[:12]:
            lines.append(f"- **{s}** bab {n} · par {a + 1} ~ par {b + 1}")
            lines.append(f"  - {re.sub(chr(10), ' ', pa)}...")
            lines.append(f"  - {re.sub(chr(10), ' ', pb)}...")
        for s, n, b, pa, pb in o1[:12]:
            lines.append(f"- **{s}** bab {n} · pembuka ~ par {b + 1}")
            lines.append(f"  - {re.sub(chr(10), ' ', pa)}...")
        lines.append("")
    lines += ["## Ringkasan", "",
              "| Berkas | paragraf dalam bab | pembuka |", "|---|---|---|"]
    for path, a0, a1, b0, b1 in rows:
        lines.append(f"| `{path}` | {a0} -> {a1} | {b0} -> {b1} |")
    if "--write" in sys.argv:
        open("REPETISI.md", "w", encoding="utf-8").write("\n".join(lines))
        print("REPETISI.md ditulis")


if __name__ == "__main__":
    main()
