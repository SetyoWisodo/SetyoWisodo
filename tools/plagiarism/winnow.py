# -*- coding: utf-8 -*-
"""Pemeriksa kemiripan prosa berbasis winnowing — algoritma yang sama
dipakai MOSS dan, pada prinsipnya, Turnitin untuk sidik jari dokumen.

Rujukan algoritma: Schleimer, Wilkerson & Aiken (2003), "Winnowing: Local
Algorithms for Document Fingerprinting", SIGMOD.

Bedanya dengan copydetect (yang mencoba dulu): copydetect memakai tokenizer
Pygments untuk kode sumber. Pada prosa, lexer "text" menggabungkan seluruh
berkas menjadi satu token sehingga sidik jarinya degenerasi dan tidak ada
satu pun pasangan yang cocok. Di sini tokenisasinya di tingkat kata, dan
sidik jarinya k-gram kata — satuan yang memang dipakai untuk mendeteksi
penyalinan kalimat.

Skor yang dihasilkan BUKAN skor Turnitin. Turnitin membandingkan naskah
dengan korpus miliaran halaman yang tidak tersedia publik. Skor di sini
dihitung terhadap korpus yang Anda berikan, dan selalu dilaporkan bersama
definisi korpusnya.

Pemakaian:
    python winnow.py --test DIR --ref DIR [--k 8] [--window 4]
"""
import argparse
import os
import re
import sys
from collections import defaultdict

STOP_SHINGLE = re.compile(r"^\W*$")


def words(text):
    """Token kata huruf kecil; tanda baca dibuang, angka dipertahankan."""
    return re.findall(r"[a-z0-9\u00c0-\u024f]+", text.lower())


def hashes(tokens, k):
    """Hash setiap k-gram kata (FNV-1a 64-bit, deterministik)."""
    out = []
    for i in range(len(tokens) - k + 1):
        h = 0xCBF29CE484222325
        for t in tokens[i:i + k]:
            for ch in t:
                h ^= ord(ch)
                h = (h * 0x100000001B3) & 0xFFFFFFFFFFFFFFFF
            h ^= 0x2F          # pemisah antar kata
            h = (h * 0x100000001B3) & 0xFFFFFFFFFFFFFFFF
        out.append(h)
    return out


def winnow(hashes_list, window):
    """Ambil minimum pada tiap jendela — sidik jari dokumen.

    Mengembalikan set hash beserta peta hash -> posisi k-gram pertama,
    supaya cakupan kata bisa dihitung, bukan hanya jumlah fingerprint.
    """
    fp = set()
    pos = {}
    n = len(hashes_list)
    if n < window:
        for i, h in enumerate(hashes_list):
            fp.add(h)
            pos.setdefault(h, i)
        return fp, pos
    for i in range(n - window + 1):
        seg = hashes_list[i:i + window]
        m = min(seg)
        idx = i + seg.index(m)
        fp.add(m)
        pos.setdefault(m, idx)
    return fp, pos


class Doc:
    def __init__(self, name, text, k, window):
        self.name = name
        self.tokens = words(text)
        self.k = k
        self.h = hashes(self.tokens, k)
        self.fp, self.pos = winnow(self.h, window)
        self.n = len(self.tokens)

    def coverage_vs(self, other):
        """Fraksi kata dokumen ini yang tercakup k-gram milik dokumen lain."""
        if not self.fp or not self.n:
            return 0.0, 0
        shared = self.fp & other.fp
        if not shared:
            return 0.0, 0
        covered = bytearray(self.n)
        for h in shared:
            i = self.pos.get(h)
            if i is None:
                continue
            for j in range(i, min(i + self.k, self.n)):
                covered[j] = 1
        hit = sum(covered)
        return hit / self.n, hit


def load(dirs, k, window, exts=(".txt", ".md")):
    docs = []
    for d in dirs:
        for root, _dirs, files in os.walk(d):
            for f in sorted(files):
                if not f.lower().endswith(exts):
                    continue
                p = os.path.join(root, f)
                text = open(p, encoding="utf-8", errors="ignore").read()
                docs.append(Doc(os.path.relpath(p, os.path.commonpath(dirs or ["."])),
                                text, k, window))
    return docs


def run(test_dirs, ref_dirs, k=8, window=4, floor=0.005):
    print(f"winnowing: k={k} kata, jendela={window}, "
          f"ambang lapor={floor*100:.1f}% cakupan")
    test = load(test_dirs, k, window)
    ref = load(ref_dirs if ref_dirs else test_dirs, k, window)
    print(f"dokumen diuji: {len(test)}  |  dokumen pembanding: {len(ref)}")

    rows = []
    for t in test:
        best, best_doc, best_hit = 0.0, None, 0
        for r in ref:
            if r.name == t.name:
                continue
            cov, hit = t.coverage_vs(r)
            if cov > best:
                best, best_doc, best_hit = cov, r.name, hit
        rows.append((t.name, t.n, best, best_doc, best_hit))

    rows.sort(key=lambda x: -x[2])
    total_words = sum(r[1] for r in rows)
    matched_words = sum(r[4] for r in rows)
    overall = matched_words / total_words if total_words else 0.0

    shown = [r for r in rows if r[2] >= floor]
    print(f"\n{'dokumen':<34}{'kata':>8}{'mirip':>9}  terdekat")
    print("-" * 78)
    for name, n, cov, other, _h in shown[:25]:
        print(f"{name[:33]:<34}{n:>8}{cov*100:>8.2f}%  {(other or '-')[:30]}")
    if len(shown) > 25:
        print(f"... {len(shown)-25} dokumen lain di atas ambang")

    print("-" * 78)
    print(f"{'TOTAL':<34}{total_words:>8}{overall*100:>8.2f}%")
    print(f"\nSkor kemiripan (cakupan kata): {overall*100:.2f}%")
    print(f"Korpus pembanding: {len(ref)} dokumen, "
          f"{sum(d.n for d in ref)} kata")
    return rows, overall


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--test", nargs="+", required=True)
    ap.add_argument("--ref", nargs="*", default=None)
    ap.add_argument("--k", type=int, default=8)
    ap.add_argument("--window", type=int, default=4)
    ap.add_argument("--floor", type=float, default=0.005)
    a = ap.parse_args()
    run(a.test, a.ref, a.k, a.window, a.floor)
