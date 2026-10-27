# -*- coding: utf-8 -*-
"""Pasang gelombang kedua sitasi, di kedua edisi.

Edisi Inggris: jangkar dicocokkan persis; kalau jangkar tidak muncul tepat
sekali, entri dilaporkan dan TIDAK dipasang.

Edisi Indonesia: kalimatnya terjemahan, jadi jangkar Inggris tidak akan cocok.
Yang dipakai adalah ANGKA: untuk setiap entri, angka pada kalimat Inggris
diambil, lalu dicari kalimat Indonesia di bab yang sama yang memuat angka
tersebut. Pemasangan hanya dilakukan kalau kandidatnya tunggal. Kalau ada dua
atau lebih, entri dilewati dan dilaporkan -- lebih baik tidak ada rujukan
daripada rujukan salah.

Jalankan: python apply_more.py [--dry-run]
"""
import re
import sys

import cite_numbers as C
from more_citations import MORE, MORE_2, MORE_3, ID_MORE, ID_MORE_2, ID_MORE_3, MORE_4, ID_MORE_4, MORE_5, ID_MORE_5
MORE = MORE + MORE_2 + MORE_3 + MORE_4 + MORE_5
ID_MORE = ID_MORE + ID_MORE_2 + ID_MORE_3 + ID_MORE_4 + ID_MORE_5

CHAPTER_EN = re.compile(r"^# Chapter (\d+):", re.M)
CHAPTER_ID = re.compile(r"^# Bab (\d+):", re.M)


def chapters(text, rx):
    """Pecah teks per bab: {nomor: (awal, akhir)} dalam offset karakter."""
    out, marks = {}, []
    for m in rx.finditer(text):
        marks.append((int(m.group(1)), m.start()))
    for i, (num, start) in enumerate(marks):
        end = marks[i + 1][1] if i + 1 < len(marks) else len(text)
        out[num] = (start, end)
    return out


IDW = {"satu": 1, "dua": 2, "tiga": 3, "empat": 4, "lima": 5, "enam": 6,
       "tujuh": 7, "delapan": 8, "sembilan": 9, "sepuluh": 10, "sebelas": 11,
       "dua belas": 12, "dua puluh": 20, "tiga puluh": 30, "empat puluh": 40,
       "lima puluh": 50, "enam puluh": 60, "tujuh puluh": 70, "delapan puluh": 80,
       "sembilan puluh": 90, "seratus": 100, "dua ratus": 200, "tiga ratus": 300,
       "seribu": 1000, "dua ribu": 2000, "tiga ribu": 3000}


def despell_id(t):
    for word in sorted(IDW, key=len, reverse=True):
        t = re.sub(r"\b" + word + r"\b", str(IDW[word]), t, flags=re.I)
    return t


def keys(sent):
    """Kunci angka yang bisa dibandingkan lintas bahasa: '7 %', '619 kematian'."""
    out = []
    for m in C.FIG.finditer(despell_id(C.despell(sent))):
        num = m.group(1).replace(",", "").replace(".", "")
        if len(num) >= 2:
            out.append((len(num), num))
    out.sort(reverse=True)
    return [k for _, k in out]


PROPER = re.compile(r"\b([A-Z][a-z\u00e0-\u00ff]{4,})\b")
STOPW = {"there", "these", "those", "which", "where", "after", "before",
         "during", "between", "because", "although", "however", "another",
         "world", "other", "their", "about", "every", "first", "second"}


def proper_nouns(sent):
    return {w for w in PROPER.findall(sent) if w.lower() not in STOPW}


def insert_in_sentence(sent, cite):
    cite = C.normalise(cite)
    m = C.TERMINAL.search(sent)
    if not m or C.PAREN.search(sent):
        return None
    return sent[:m.start()] + f" ({cite})" + sent[m.start():]


def apply_en(text):
    blocks = text.split("\n\n")
    log, misses = [], []
    for anchor, cite in MORE:
        hits = 0
        for bi, b in enumerate(blocks):
            if anchor not in b or not C.is_body(b):
                continue
            sents = C.sentences(b)
            for si, s in enumerate(sents):
                if anchor in s:
                    hits += 1
                    new = insert_in_sentence(s, cite)
                    if new:
                        sents[si] = new
                        blocks[bi] = " ".join(sents)
                        log.append((anchor, cite, s[:90]))
        if hits != 1:
            misses.append((anchor, hits))
    return "\n\n".join(blocks), log, misses


def apply_id(text, en_text, en_log):
    """Cocokkan lewat angka, dalam bab yang sama."""
    ch_en = chapters(en_text, CHAPTER_EN)
    blocks = text.split("\n\n")
    cur, block_chapter = None, []
    for b in blocks:
        m = CHAPTER_ID.match(b.strip())
        if m:
            cur = int(m.group(1))
        block_chapter.append(cur)

    log, skipped = [], []
    for anchor, cite in MORE:
        target = None
        for n, (s, e) in ch_en.items():
            for sent in C.sentences(en_text[s:e]):
                if anchor in sent:
                    target = (n, sent)
                    break
            if target:
                break
        if not target:
            continue
        num, sent_en = target
        ks = keys(sent_en)
        if not ks:
            skipped.append((anchor, "tanpa angka"))
            continue
        key = ks[0]
        cands = []
        for j, b in enumerate(blocks):
            if block_chapter[j] != num or not C.is_body(b):
                continue
            for si, s in enumerate(C.sentences(b)):
                if key in keys(s) and not C.PAREN.search(s):
                    cands.append((j, si))
        if len(cands) != 1:
            # cadangan: nama diri yang bertahan melewati penerjemahan
            names = proper_nouns(sent_en)
            alt = []
            if names:
                for j, b in enumerate(blocks):
                    if block_chapter[j] != num or not C.is_body(b):
                        continue
                    for si, cc in enumerate(C.sentences(b)):
                        if C.PAREN.search(cc):
                            continue
                        if any(n in cc for n in names):
                            alt.append((j, si))
            if len(alt) == 1:
                cands = alt
            else:
                skipped.append((anchor, f"{len(cands)} kandidat"))
                continue
        if len(cands) != 1:
            skipped.append((anchor, "ambigu"))
            continue
        j, si = cands[0]
        sents = C.sentences(blocks[j])
        new_s = insert_in_sentence(sents[si], cite)
        if new_s:
            sents[si] = new_s
            blocks[j] = " ".join(sents)
            log.append((anchor, cite, new_s[:90]))
    return "\n\n".join(blocks), log, skipped


def apply_id_direct(text):
    blocks = text.split("\n\n")
    log, misses = [], []
    for anchor, cite in ID_MORE:
        hits = 0
        for bi, b in enumerate(blocks):
            if anchor not in b or not C.is_body(b):
                continue
            sents = C.sentences(b)
            for si, s in enumerate(sents):
                if anchor in s:
                    hits += 1
                    new = insert_in_sentence(s, cite)
                    if new:
                        sents[si] = new
                        blocks[bi] = " ".join(sents)
                        log.append((anchor, cite, s[:90]))
        if hits != 1:
            misses.append((anchor, hits))
    return "\n\n".join(blocks), log, misses


def main():
    dry = "--dry-run" in sys.argv
    en = open("book.md", encoding="utf-8").read()
    en_new, log, misses = apply_en(en)
    print(f"EN: {len(log)} sitasi dipasang; {len(misses)} jangkar bermasalah")
    for a, h in misses:
        print(f"   ! {h}x  {a[:70]}")
    idn = open("book_id.md", encoding="utf-8").read()
    id_new, log_id, skipped = apply_id(idn, en_new, log)
    id_new, log_direct, id_miss = apply_id_direct(id_new)
    log_id += log_direct
    for a, h in id_miss:
        print(f"   ! ID {h}x  {a[:60]}")
    print(f"ID: {len(log_id)} sitasi dipasang; {len(skipped)} dilewati")
    for a, why in skipped[:40]:
        print(f"   ~ {why:28} {a[:60]}")
    if not dry:
        open("book.md", "w", encoding="utf-8").write(en_new)
        open("book_id.md", "w", encoding="utf-8").write(id_new)
    open("/tmp/more_log.txt", "w", encoding="utf-8").write(
        "\n".join(f"[EN] {c:40} {s}" for a, c, s in log) + "\n" +
        "\n".join(f"[ID] {c:40} {s}" for a, c, s in log_id))
    print("log -> /tmp/more_log.txt")


if __name__ == "__main__":
    main()
