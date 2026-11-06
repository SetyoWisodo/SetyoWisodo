#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cek_kontinuitas.py — pastikan jangkar cerita ada di babnya."""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(ROOT, "bible"); V = os.path.join(ROOT, "vol1")

def main():
    d = json.load(open(os.path.join(B, "kontinuitas.json"), encoding="utf-8"))
    gagal = total = 0
    for j in d["jangkar"]:
        for n in j["bab"]:
            p = os.path.join(V, "ch_%03d.md" % n)
            if not os.path.exists(p): continue
            total += 1
            t = open(p, encoding="utf-8").read().lower()
            if not any(k.lower() in t for k in j["kata"]):
                print("FAIL %-5s bab %3d tidak memuat %s" % (j["id"], n, j["objek"])); gagal += 1
    print("\njangkar: %d titik | gagal: %d" % (total, gagal))
    return 1 if gagal else 0

if __name__ == "__main__":
    sys.exit(main())
