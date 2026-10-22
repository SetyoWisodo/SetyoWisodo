# -*- coding: utf-8 -*-
"""Gate 6 — audit produksi PDF (EN & ID).

Memeriksa: metadata dokumen, outline navigasi, halaman kosong, teks yang
melewati margin, judul yang menggantung di dasar halaman, kecocokan nomor
halaman Daftar Isi dengan outline, dan font tertanam.

Pemakaian: python audit_production.py
"""
import os
import re
import sys

import pymupdf

BOOKS = [
    ("Surviving_the_Future.pdf", "en"),
    ("Surviving_the_Future_ID.pdf", "id"),
]
MARGIN_MM = 30.0          # margin halaman simetris (halaman 1-2)
INNER_MM = 30.0           # margin kiri (simetris)
OUTER_MM = 30.0           # margin kanan (simetris)
HEAD_ZONE_MM = 24.0       # kepala halaman berjalan boleh di atas margin atas
MM = 72.0 / 25.4
TOL = 1.5 * MM  # toleransi 1,5 mm untuk huruf miring/berlebih optik


def mm(v):
    return v / MM


def audit(path):
    doc = pymupdf.open(path)
    out = {"file": path, "pages": len(doc), "problems": []}
    meta = doc.metadata or {}
    out["meta"] = {k: meta.get(k, "") for k in ("title", "author", "subject", "keywords")}
    for k in ("title", "author"):
        if not meta.get(k):
            out["problems"].append("metadata '%s' kosong" % k)

    toc = doc.get_toc()
    out["toc_entries"] = len(toc)
    if not toc:
        out["problems"].append("tidak ada outline navigasi")

    w, h = doc[0].rect.width, doc[0].rect.height
    out["size_mm"] = (round(mm(w), 1), round(mm(h), 1))
    sym_l, sym_r = MARGIN_MM * MM - TOL, w - MARGIN_MM * MM + TOL

    blank, overflow, outside = [], [], []
    for i, page in enumerate(doc):
        text = page.get_text().strip()
        body = [ln for ln in text.split("\n") if ln.strip() and not ln.strip().isdigit()]
        if not body:
            blank.append(i + 1)
            continue
        if i < 2:
            left_lim, right_lim = sym_l, sym_r
        elif (i + 1) % 2 == 1:      # recto: punggung di kiri
            left_lim, right_lim = INNER_MM * MM - TOL, w - OUTER_MM * MM + TOL
        else:                       # verso: punggung di kanan
            left_lim, right_lim = OUTER_MM * MM - TOL, w - INNER_MM * MM + TOL
        for b in page.get_text("blocks"):
            x0, y0, x1, y1, txt = b[0], b[1], b[2], b[3], b[4].strip()
            if not txt:
                continue
            if y1 < HEAD_ZONE_MM * MM:      # kepala halaman berjalan
                continue
            if x1 > right_lim + 2 or x0 < left_lim - 2:
                outside.append((i + 1, round(mm(x0), 1), round(mm(x1), 1), txt[:40]))
            if y1 > h - 8:
                overflow.append((i + 1, round(mm(y1), 1), txt[:40]))

    out["blank_pages"] = blank
    out["text_outside_margin"] = outside[:10]
    out["text_below_bottom"] = overflow[:10]
    if blank:
        out["problems"].append("halaman kosong: %s" % blank[:10])
    if outside:
        out["problems"].append("%d blok teks melewati margin" % len(outside))
    if overflow:
        out["problems"].append("%d blok teks jatuh di bawah margin bawah" % len(overflow))

    # --- judul menggantung: blok terakhir berukuran besar & pendek, lalu halaman baru ---
    dangling = []
    for i in range(len(doc) - 1):
        page = doc[i]
        blocks = [b for b in page.get_text("blocks") if b[4].strip() and not b[4].strip().isdigit()]
        if not blocks:
            continue
        last = blocks[-1]
        spans = [s for blk in page.get_text("dict")["blocks"] for ln in blk.get("lines", [])
                 for s in ln.get("spans", [])]
        size = max((s["size"] for s in spans), default=0)
        # blok terakhir pendek (< 70 char), berada di 25 % bawah halaman, dan seukuran teks isi
        if len(last[4].strip()) < 70 and last[3] > h * 0.72 and abs(last[3] - last[1]) < 10:
            nxt = doc[i + 1].get_text().strip().split("\n")
            nxt = [x for x in nxt if x.strip() and not x.strip().isdigit()]
            if nxt and _is_heading_like(last[4].strip()) and size <= 12.5:
                dangling.append((i + 1, last[4].strip()[:50]))
    out["possible_dangling_headings"] = dangling

    # --- kecocokan Daftar Isi dengan outline ---
    mism = []
    if toc:
        # halaman daftar isi = halaman sebelum entri outline pertama
        first = toc[0][2]
        toc_pages = [p for p in range(1, min(first, 12)) ]
        found = {}
        for p in toc_pages:
            for ln in doc[p - 1].get_text().split("\n"):
                ln = ln.strip()
                m = re.match(r"^(.*?)[\s.…]{2,}(\d{1,3})$", ln)
                if m:
                    found[m.group(1).strip()] = int(m.group(2))
        for level, title, page in toc:
            key = title.strip()
            if key in found and found[key] != page:
                mism.append((key[:40], found[key], page))
    out["toc_mismatches"] = mism
    if mism:
        out["problems"].append("%d entri Daftar Isi tidak cocok dengan halaman aslinya" % len(mism))

    fonts = set()
    for i in range(0, len(doc), 25):
        for f in doc[i].get_fonts():
            fonts.add(f[3])
    out["fonts"] = sorted(fonts)
    if any("Tinos" not in f for f in fonts):
        out["problems"].append("font tak terduga: %s" % sorted(fonts))

    out["size_mb"] = round(os.path.getsize(path) / 1e6, 2)
    return out


def _is_heading_like(txt):
    t = txt.strip()
    if not t or t.endswith("."):
        return False
    words = t.split()
    return 1 <= len(words) <= 9 and (t[0].isupper() or t[0].isdigit())


def main():
    bad = 0
    for path, lang in BOOKS:
        if not os.path.exists(path):
            print("MISSING", path)
            bad += 1
            continue
        r = audit(path)
        print("=" * 66)
        print("%s  [%s]  %d halaman, %.2f MB, %s mm" %
              (r["file"], lang, r["pages"], r["size_mb"], r["size_mm"]))
        print("  metadata :", r["meta"])
        print("  outline  :", r["toc_entries"], "entri")
        print("  font     :", ", ".join(r["fonts"]))
        print("  kosong   :", r["blank_pages"] or "tidak ada")
        print("  keluar margin:", len(r["text_outside_margin"]), "blok", r["text_outside_margin"][:3])
        print("  judul menggantung:", len(r["possible_dangling_headings"]), r["possible_dangling_headings"][:4])
        print("  TOC tak cocok:", len(r["toc_mismatches"]), r["toc_mismatches"][:4])
        if r["problems"]:
            bad += 1
            print("  MASALAH:", "; ".join(r["problems"]))
        else:
            print("  STATUS   : bersih")
    print("=" * 66)
    print("Buku dengan masalah: %d" % bad)
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
