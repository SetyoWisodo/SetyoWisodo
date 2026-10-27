# -*- coding: utf-8 -*-
"""Sisipkan paragraf uji-prediksi di akhir setiap subbab Future Scenarios.

Mengapa ada: pembaca memakai prediksi sebagai peringatan dini hanya kalau ia tahu
(a) tahunnya, (b) angkanya, (c) asumsinya, (d) apa yang membuktikannya salah, dan
(e) angka apa yang dipantau. `predictions.py` memuat paragraf itu per bab, dua
bahasa.

Aturan penyisipan:
  * paragraf ditaruh SEBELUM garis "---" penutup bab, sehingga tetap berada di
    dalam subbab Future Scenarios;
  * idempoten: kalau kalimat pertama paragraf sudah ada di bab itu, dilewati;
  * bab yang subbabnya tidak ditemukan dilaporkan, bukan ditebak.

Jalankan: python add_predictions.py [--dry-run]
"""
import re
import sys

from predictions import PRED, PRED_ID

SPEC = {"book.md": (PRED, re.compile(r"^# Chapter (\d+):", re.M)),
        "book_id.md": (PRED_ID, re.compile(r"^# Bab (\d+):", re.M))}


def insert(text, chapter_rx, n, para):
    lines = text.split("\n")
    start = None
    for i, line in enumerate(lines):
        m = chapter_rx.match(line)
        if m and int(m.group(1)) == n:
            start = i
            break
    if start is None:
        return text, "bab tidak ditemukan"
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if chapter_rx.match(lines[i]) or lines[i].startswith("# "):
            end = i
            break
    head = f"## {n}.12 "
    sec = None
    for i in range(start, end):
        if lines[i].startswith(head):
            sec = i
            break
    if sec is None:
        return text, "subbab 12 tidak ditemukan"
    stop = None
    for i in range(sec + 1, end):
        if lines[i].strip() == "---":
            stop = i
            break
    if stop is None:
        stop = end
    first = para.split(".")[0]
    if any(first[:60] in lines[i] for i in range(sec, stop)):
        return text, "sudah ada"
    # sisipkan paragraf sebagai blok sendiri: satu baris kosong sebelum dan
    # sesudahnya. Baris kosong pengikut lama dibuang dulu supaya tidak ada
    # baris kosong ganda, dan paragraf tidak menempel pada paragraf sebelumnya.
    j = stop
    while j - 1 > sec and lines[j - 1].strip() == "":
        j -= 1
    if j - 1 <= sec:
        return text, "subbab kosong"
    lines[j:stop] = ["", para, ""]
    return "\n".join(lines), "disisipkan"


def main():
    dry = "--dry-run" in sys.argv
    for path, (data, rx) in SPEC.items():
        text = open(path, encoding="utf-8").read()
        done = 0
        for n in sorted(data):
            text, status = insert(text, rx, n, data[n])
            if status == "disisipkan":
                done += 1
            elif status != "sudah ada":
                print(f"  ! {path} bab {n}: {status}")
        print(f"{path}: {done} paragraf disisipkan")
        if not dry and done:
            if text.count("\n\n\n"):
                raise SystemExit("ada baris kosong ganda")
            open(path, "w", encoding="utf-8").write(text)


if __name__ == "__main__":
    main()
