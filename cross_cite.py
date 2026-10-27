# -*- coding: utf-8 -*-
"""Isi rujukan yang hilang dengan memakai rujukan yang sudah ada di buku ini.

Banyak angka muncul dua kali: sekali di tempat asalnya (dengan rujukan) dan
sekali lagi di ringkasan atau studi kasus (tanpa rujukan). Alat ini mencari
kalimat bertanda rujukan yang memuat ANGKA YANG SAMA, lalu memakai rujukan itu
lagi -- bukan menambah sumber baru.

Batas keamanan (sengaja ketat, karena salah sumber lebih buruk daripada kosong):
  * bekerja per paragraf; judul, tabel, dan kotak tidak disentuh;
  * tahun (1900-2099) tidak dihitung sebagai angka pembanding;
  * minimal DUA angka berbeda (panjang >= 3 karakter) yang sama;
  * hanya rujukan tunggal, bukan gabungan "(A, 2021; B, 2022)";
  * satu kandidat harus menang jelas: selisih skor >= 2; kandidat dari bab
    yang sama diberi bobot lebih.

Jalankan: python cross_cite.py [--dry-run]
"""
import re
import sys

import cite_numbers as C

STRICT = re.compile(r"^\s*([A-Z][^();]{0,80}?),\s*(?:19|20)\d{2}[a-z]?\s*$")
SKIP_START = ("#", "[[TABLE", "|", "**Table", "**Tabel", "**Case", "**Kasus",
              ">", "-", "*", "1.", "2.", "3.", "4.")
CH = {"book.md": re.compile(r"^# Chapter (\d+):", re.M),
      "book_id.md": re.compile(r"^# Bab (\d+):", re.M)}


def numkeys(text):
    out = set()
    for m in re.findall(r"\d[\d,.]*\d|\d{3,}", text):
        t = m.replace(",", "").replace(".", "")
        if 1900 <= int(t) <= 2099 and len(t) == 4:
            continue          # tahun, bukan besaran
        if len(t) >= 3:
            out.add(t)
    return out


def paragraphs(text):
    return re.split(r"\n\s*\n", text)


def main():
    dry = "--dry-run" in sys.argv
    for path in ("book.md", "book_id.md"):
        text = open(path, encoding="utf-8").read()
        paras = paragraphs(text)

        # kumpulkan kalimat bertanda rujukan -> (angka, sitasi, bab)
        corpus = []
        ch, ch_pos = 0, 0
        marks = [(int(m.group(1)), m.start()) for m in CH[path].finditer(text)]
        for para in paras:
            for s in C.sentences(para):
                hits = [STRICT.match(c.strip("()")) for c in C.PAREN.findall(s)]
                cites = {c for c in C.PAREN.findall(s)
                         if STRICT.match(c.strip("()"))}
                if len(cites) == 1 and C.QUANTITY.search(s):
                    corpus.append((numkeys(s), next(iter(cites))))

        # bab per paragraf (berdasarkan posisi awal paragraf)
        ch_of = []
        pos = 0
        ci = 0
        for para in paras:
            start = text.find(para, pos)
            pos = (start + len(para)) if start >= 0 else pos
            while ci < len(marks) and marks[ci][1] <= (start if start >= 0 else 0):
                ch = marks[ci][0]
                ci += 1
            ch_of.append(ch)

        added, skipped, out = [], 0, []
        for idx, para in enumerate(paras):
            head = para.strip()
            if not head or head.startswith(SKIP_START) or not C.is_body(para):
                out.append(para)
                continue
            sents = C.sentences(para)
            touched = False
            for j, s in enumerate(sents):
                if C.PAREN.search(s) or not C.QUANTITY.search(s):
                    continue
                k = numkeys(s)
                if len(k) < 2:
                    skipped += 1
                    continue
                best, best_score, second = None, 0, 0
                for k2, cite in corpus:
                    shared = len(k & k2)
                    if shared < 2:
                        continue
                    score = shared * 2
                    if best and cite == best:
                        score += 1
                    if score > best_score:
                        second, best, best_score = best_score, cite, score
                    elif score > second:
                        second = score
                if best and best_score >= 4 and best_score - second >= 2:
                    new = C.insert_cite(s, best)
                    if new and new != s:
                        sents[j] = new
                        added.append((ch_of[idx], best, s[:70]))
                        touched = True
            out.append(" ".join(sents) if touched else para)

        # paragraf yang tidak berubah dikembalikan apa adanya
        print(f"{path}: {len(added)} rujukan dipasang ulang, {skipped} kalimat dilewati")
        for n, c, s in added:
            print(f"   bab {n:>2} {c:28} | {s[:64]}")
        if not dry and added:
            open(path, "w", encoding="utf-8").write("\n\n".join(out))


if __name__ == "__main__":
    main()
