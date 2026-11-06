#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fix_typography.py — rapikan tanda baca naskah. python3 novel_en/tools/fix_typography.py [nomor...]"""
import glob, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOL = os.path.join(ROOT, "vol1")

def rapikan(t):
    t = t.replace("...", "\u2026")
    t = re.sub(r"(?<=[A-Za-z])'(?=[A-Za-z])", "\u2019", t)
    t = re.sub(r"'(?=\w)", "\u2018", t)
    t = re.sub(r"(?<=\w)'", "\u2019", t)
    out = []
    for baris in t.split("\n"):
        buf, buka = [], True
        for ch in baris:
            if ch == '"':
                buf.append("\u201c" if buka else "\u201d"); buka = not buka
            else:
                buf.append(ch)
        out.append("".join(buf))
    t = "\n".join(out)
    t = re.sub(r"[ \t]{2,}", " ", t)
    t = re.sub(r"\s+([,.;:!?])", r"\1", t)
    return t

def main():
    mau = sys.argv[1:]
    berkas = sorted(glob.glob(os.path.join(VOL, "ch_*.md")))
    if mau:
        berkas = [b for b in berkas if os.path.basename(b)[3:6] in mau]
    n = 0
    for p in berkas:
        lama = open(p, encoding="utf-8").read()
        baru = rapikan(lama)
        if baru != lama:
            open(p, "w", encoding="utf-8").write(baru); print("dirapikan:", os.path.basename(p)); n += 1
    print("%d diubah dari %d" % (n, len(berkas)))

if __name__ == "__main__":
    main()
