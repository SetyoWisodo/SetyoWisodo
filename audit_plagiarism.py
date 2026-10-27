# -*- coding: utf-8 -*-
"""Audit kemiripan teks internal (self-plagiarism) + disiplin kutipan.

Alat berbayar (Turnitin, iThenticate, Copyscape) membandingkan naskah dengan
korpus luar. Itu tidak bisa dilakukan di sini karena korpusnya tidak tersedia
offline. Yang BISA dan HARUS diperiksa lebih dulu ada di dalam naskah sendiri:

  1. Duplikasi internal   -- kalimat/paragraf yang berulang persis di dalam buku.
     Inilah yang paling sering memicu tuduhan "plagiasi diri" dan menurunkan
     skor orisinalitas di Turnitin.
  2. Kalimat nyaris sama  -- beda beberapa kata, sisa template.
  3. Disiplin kutipan     -- teks di dalam tanda kutip harus punya sumber.
  4. Kepadatan sitasi     -- paragraf yang memuat klaim angka tanpa rujukan.

Jalankan: python audit_plagiarism.py
Keluaran : laporan di layar + plagiarism_report.md
"""
import re
import sys
from collections import Counter, defaultdict

from cite_numbers import QUANTITY, is_body
from numeric_audit import figures, CITE as Q_CITE

FILES = [("book.md", "en"), ("book_id.md", "id")]
MIN_WORDS = 9          # kalimat lebih pendek dari ini diabaikan (terlalu umum)
JACCARD = 0.62         # ambang kalimat "nyaris sama" (4-shingle; 0,62 = sangat mirip)

STOP = set("""a an the of and or but in on at to for from by with as is are was were be been
being this that these those it its their there which who whom whose not no than then so such
can could may might will would shall should do does did have has had also more most very much
many some any all each both other into over under between within without about after before
during while if when where how what why s t d ll m re ve""".split())


def sentences(text):
    """Pecah jadi kalimat; simpan nomor baris untuk pelaporan."""
    out = []
    for lineno, line in enumerate(text.split("\n"), 1):
        if not line.strip() or line.startswith(("#", "-", "!", "[", "|")):
            continue
        for s in re.split(r"(?<=[.!?])\s+(?=[A-Z\u00c0-\u00de])", line):
            s = s.strip()
            if len(s.split()) >= MIN_WORDS:
                out.append((lineno, s))
    return out


def tokens(s):
    return re.findall(r"[a-z\u00e0-\u00ff0-9']+", s.lower())


def content_tokens(s):
    return [t for t in tokens(s) if t not in STOP]


def shingles(toks, n=4):
    return {tuple(toks[i:i + n]) for i in range(max(0, len(toks) - n + 1))}


CITE = re.compile(r"\((?:[A-Z][^()]{0,80})?(?:19|20)\d{2}[a-z]?(?:[;,][^()]{0,40})?\)")
# untuk atribusi paragraf: tahun telanjang "(2023)" BUKAN rujukan, jadi nama wajib ada
CITE_STRICT = re.compile(r"\([A-Z][^()]{0,80}?(?:19|20)\d{2}[a-z]?\)")
QUOTED = re.compile(r"[\u201c\"]([^\u201d\"]{40,})[\u201d\"]")


def audit(path, lang):
    text = open(path, encoding="utf-8").read()
    sents = sentences(text)
    print(f"\n{'='*70}\n{path}   {lang}   kalimat diperiksa: {len(sents)}\n{'='*70}")

    # ---- 1. duplikasi persis -------------------------------------------------
    norm = [re.sub(r"\s+", " ", s.lower().strip()) for _, s in sents]
    counts = Counter(norm)
    dup_idxs = [i for i, n in enumerate(norm) if counts[n] > 1]
    dup_words = sum(len(sents[i][1].split()) for i in dup_idxs)
    total_words = sum(len(s.split()) for _, s in sents)
    print(f"1. Kalimat berulang persis : {len(dup_idxs)} kalimat "
          f"({dup_words} kata, {dup_words/total_words*100:.1f}% dari teks)")
    seen = set()
    worst = []
    for i in dup_idxs:
        k = norm[i]
        if k in seen:
            continue
        seen.add(k)
        worst.append((counts[k], k, [sents[j][0] for j in dup_idxs if norm[j] == k][:6]))
    worst.sort(reverse=True)
    for c, s, lines in worst[:5]:
        print(f"   x{c:<3} baris {lines}  {s[:92]}...")

    # ---- 2. kalimat nyaris sama ---------------------------------------------
    sh = [shingles(content_tokens(s)) for _, s in sents]
    near_pairs = 0
    examples = []
    buckets = defaultdict(list)
    for i, s in enumerate(sh):
        for g in list(s)[:60]:
            buckets[g].append(i)
    checked = set()
    for g, idxs in buckets.items():
        if len(idxs) < 2 or len(idxs) > 40:
            continue
        for a in range(len(idxs)):
            for b in range(a + 1, len(idxs)):
                i, j = idxs[a], idxs[b]
                if (i, j) in checked:
                    continue
                checked.add((i, j))
                if not sh[i] or not sh[j]:
                    continue
                jac = len(sh[i] & sh[j]) / len(sh[i] | sh[j])
                if jac >= JACCARD and norm[i] != norm[j]:
                    near_pairs += 1
                    if len(examples) < 4:
                        examples.append((jac, sents[i], sents[j]))
    print(f"\n2. Pasangan kalimat nyaris sama (Jaccard >= {JACCARD}) : {near_pairs}")
    for jac, (la, sa), (lb, sb) in examples:
        print(f"   {jac:.2f}  baris {la} / {lb}")
        print(f"        {sa[:100]}")
        print(f"        {sb[:100]}")

    # ---- 3. kutipan tanpa sumber -------------------------------------------
    quotes = [(m.start(), m.group(1)) for m in QUOTED.finditer(text)]
    orphan = []
    for pos, q in quotes:
        window = text[max(0, pos - 260):pos + 300]
        if not CITE.search(window):
            orphan.append(q)
    print(f"\n3. Teks dalam tanda kutip (>= 40 huruf) : {len(quotes)}")
    print(f"   tanpa rujukan (Nama, Tahun) di sekitarnya : {len(orphan)}")
    for q in orphan[:3]:
        print(f"   - {q[:96]}...")

    # ---- 4. paragraf berkuantitas tanpa rujukan ---------------------------
    # Versi lama menghitung SETIAP digit, termasuk tahun ("pada 2023") dan
    # nomor bab, sehingga angkanya membengkak dan menyesatkan. Yang perlu
    # rujukan adalah BESARAN, bukan tahun. Dua-duanya dilaporkan supaya
    # pembaca bisa melihat selisihnya.
    paras = [p for p in re.split(r"\n\s*\n", text) if is_body(p)]
    any_num = [p for p in paras if re.search(r"\d", p) and not CITE_STRICT.search(p)]
    no_cite = [p for p in paras if figures(p) and not Q_CITE.search(p)]
    print(f"\n4. Paragraf panjang ({len(paras)}):")
    print(f"   memuat digit apa pun tanpa rujukan   : {len(any_num)} "
          f"({len(any_num)/max(1,len(paras))*100:.0f}%)")
    print(f"   memuat BESARAN tanpa rujukan         : {len(no_cite)} "
          f"({len(no_cite)/max(1,len(paras))*100:.1f}%)")

    return dict(lines=len(sents), dup=len(dup_idxs), dup_words=dup_words,
                total_words=total_words, near=near_pairs, quotes=len(quotes),
                orphan=len(orphan), paras=len(paras), nocite=len(no_cite),
                anynum=len(any_num),
                worst=worst[:5])


def fabrication_guard():
    """Periksa apakah generator akan mencetak atribusi yang belum diverifikasi."""
    import ast
    print(f"\n{'='*70}\nPENGAMAN ATRIBUSI  (gen_book.py / gen_book_id.py)\n{'='*70}")
    for path in ("gen_book.py", "gen_book_id.py"):
        try:
            src = open(path, encoding="utf-8").read()
        except FileNotFoundError:
            continue
        tree = ast.parse(src)
        exps, verified = None, set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for t in node.targets:
                    if getattr(t, "id", "") == "EXPERTS":
                        try:
                            exps = ast.literal_eval(node.value)
                        except Exception:
                            pass
                    if getattr(t, "id", "") == "EXPERT_VERIFIED":
                        try:
                            verified = set(ast.literal_eval(node.value))
                        except Exception:
                            verified = set()
        if not exps:
            print(f"  {path}: EXPERTS tidak terbaca")
            continue
        quoted = [i for i, e in enumerate(exps)
                  if e.count("'") >= 2 or e.count('"') >= 2]
        will_print = [i for i in range(len(exps)) if i in verified]
        print(f"  {path}")
        print(f"    entri EXPERTS            : {len(exps)}")
        print(f"    berbentuk kutipan langsung: {len(quoted)}")
        print(f"    ditandai terverifikasi    : {len(verified)}")
        print(f"    AKAN DICETAK              : {len(will_print)}")
        if quoted and not verified:
            print("    -> aman: kutipan tidak tercetak karena belum diverifikasi")
        elif quoted:
            print("    -> PERIKSA: ada kutipan yang akan tercetak, pastikan terverifikasi")


if __name__ == "__main__":
    res = {}
    for f, lang in FILES:
        try:
            res[f] = audit(f, lang)
        except FileNotFoundError:
            print("tidak ada:", f)

    with open("plagiarism_report.md", "w", encoding="utf-8") as fh:
        fh.write("# Laporan Kemiripan Teks (internal)\n\n")
        fh.write("Dihasilkan oleh `audit_plagiarism.py`.\n\n")
        fh.write("| Berkas | Kalimat | Berulang persis | Nyaris sama | "
                 "Kutipan | Tanpa sumber |\n|---|---|---|---|---|---|\n")
        for f, r in res.items():
            fh.write(f"| `{f}` | {r['lines']} | {r['dup']} | {r['near']} | "
                     f"{r['quotes']} | {r['orphan']} |\n")
        fh.write("\n## Kalimat yang paling sering berulang\n\n")
        for f, r in res.items():
            fh.write(f"### {f}\n\n")
            for c, s, lines in r["worst"]:
                fh.write(f"- **x{c}** (baris {lines[:4]}): {s[:160]}\n")
            fh.write("\n")
    fabrication_guard()
    print("\nlaporan ditulis: plagiarism_report.md")
