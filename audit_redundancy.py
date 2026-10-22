# -*- coding: utf-8 -*-
"""Deteksi paragraf yang menyampaikan isi yang sama dengan kata berbeda.

Dipakai sebagai pemeriksaan Gate 5/6: duplikasi parafrase tidak tertangkap
oleh n-gram, tetapi tertangkap oleh tumpang tindih *fakta* — angka, nama diri,
dan istilah isi yang jarang dipakai di seluruh buku.

Pemakaian: python audit_redundancy.py book.md [book_id.md] [--top N]
"""
import io
import re
import sys
from collections import Counter, defaultdict
from itertools import combinations

STOP_EN = set("""a an the and or but if while because of to in on at by for with from as is are was were be been
being it its this that these those they them their there here which who whom whose what when where how not no
than then so such can could may might must will would should do does did done have has had more most much
many some any each other another own same very just also only even still yet both either neither one two
three four five six seven eight nine ten however therefore thus moreover furthermore nevertheless although
though about above after again against all almost along already among around before behind below beside
between during into over under through throughout toward towards upon within without whose said says
first second third new old good great less least well back even now then us we our you your he she his her
""".split())
STOP_ID = set("""yang dan di ke dari untuk dengan pada adalah ini itu tidak akan juga sudah telah dapat bisa
atau karena tetapi namun sehingga dalam oleh sebagai lebih paling sangat masih harus antara setelah sebelum
ketika saat jika bila maka hanya saja para setiap semua banyak beberapa tersebut hal cara orang tahun
ia mereka kita kami anda dia nya pun lah kah itu begini begitu sedang belum bukan tanpa agar supaya
bagi terhadap secara serta maupun bahkan justru hanya memang masih akan sudah""".split())

NUM = re.compile(r"\b\d[\d.,]*\s?(?:%|°c|mm|cm|m|km|ha|juta|miliar|triliun|billion|million|trillion|thousand|"
                 r"people|orang|deaths|kematian|pages|pp)\b|\b\d[\d.,]*\b", re.I)
NAME = re.compile(r"\b(?:[A-ZÄÖÜ][a-zäöüß'’\-]{2,})(?:\s+(?:of|de|van|von|al\.?)?\s*[A-ZÄÖÜ][a-zäöüß'’\-]{2,})*")


def sentence_split(text):
    return [s for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


def tokens(text, lang):
    low = text.lower()
    words = re.findall(r"[a-zà-ÿ']{4,}", low)
    stop = STOP_ID if lang == "id" else STOP_EN
    return [w for w in words if w not in stop]


def signature(text, lang):
    nums = {n.strip().lower() for n in NUM.findall(text)}
    names = {m.strip().lower() for m in NAME.findall(text)
             if m.strip().lower() not in ("the", "this", "that")}
    toks = set(tokens(text, lang))
    return nums, names, toks


def scan(path, lang, top=25):
    raw = io.open(path, encoding="utf-8").read()
    lines = raw.split("\n")
    paras, heads, cur = [], [], ""
    for ln in lines:
        if ln.startswith("#"):
            cur = ln.lstrip("# ").strip()
            continue
        if ln.startswith(("-", "|", ">", "[[", "---")) or len(ln.split()) < 25:
            continue
        paras.append((cur, ln.strip()))

    # document frequency untuk istilah isi
    df = Counter()
    for _, p in paras:
        for w in set(tokens(p, lang)):
            df[w] += 1
    rare = {w for w, c in df.items() if c <= 8 and len(w) > 5}

    sig = []
    for head, p in paras:
        nums, names, toks = signature(p, lang)
        sig.append({"head": head, "text": p, "nums": nums, "names": names,
                    "rare": toks & rare, "toks": toks})

    by_head = defaultdict(list)
    for i, s in enumerate(sig):
        by_head[s["head"]].append(i)

    hits = []
    for head, ids in by_head.items():
        for a, b in combinations(ids, 2):
            A, B = sig[a], sig[b]
            shared_nums = A["nums"] & B["nums"]
            shared_names = A["names"] & B["names"]
            jr = (len(A["rare"] & B["rare"]) / max(1, min(len(A["rare"]), len(B["rare"]))))
            score = len(shared_nums) + 0.6 * len(shared_names) + 4 * jr
            if score >= 3.2 and (len(shared_nums) + len(shared_names)) >= 2:
                hits.append((score, jr, sorted(shared_nums)[:6], sorted(shared_names)[:6], a, b))
    hits.sort(reverse=True)
    return sig, hits[:top]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(sys.argv) > 1 and sys.argv[-1].startswith("--top="):
        top = int(sys.argv[-1].split("=")[-1])
    top = 20
    for a in sys.argv[1:]:
        if a.startswith("--top="):
            top = int(a.split("=")[-1])
    for path in args:
        lang = "id" if "id" in path.replace("book_id", "id").lower() and "book.md" not in path else "en"
        sig, hits = scan(path, lang, top)
        print("=" * 72)
        print("%s — %d paragraf, %d pasangan mencurigakan" % (path, len(sig), len(hits)))
        for score, jr, nums, names, a, b in hits:
            print("\n  skor %.1f (rare-Jaccard %.2f)  §%s" % (score, jr, sig[a]["head"]))
            print("    angka : %s" % ", ".join(nums))
            print("    nama  : %s" % ", ".join(names))
            print("    A: %s" % sig[a]["text"][:150])
            print("    B: %s" % sig[b]["text"][:150])


if __name__ == "__main__":
    main()
