# -*- coding: utf-8 -*-
"""Sisipkan paragraf anjuran pelaksanaan di akhir setiap subbab Future Scenarios.

Paragraf ini diletakkan SESUDAH paragraf uji prediksi: pembaca lebih dulu tahu
apa yang membuktikan ramalan itu salah, lalu tahu apa yang harus dikerjakan
ketika tandanya muncul. Isinya di `advice.py`, dua bahasa.

Aturannya sama dengan `add_predictions.py`: paragraf menjadi blok sendiri, baris
kosong di sekitarnya dinormalkan (tidak boleh ada dua baris kosong berurutan),
dan penyisipan bersifat idempoten.

Jalankan: python add_advice.py [--dry-run]
"""
import re
import sys

from add_predictions import insert
from advice import ADVICE, ADVICE_ID

SPEC = {"book.md": (ADVICE, re.compile(r"^# Chapter (\d+):", re.M)),
        "book_id.md": (ADVICE_ID, re.compile(r"^# Bab (\d+):", re.M))}


def main():
    dry = "--dry-run" in sys.argv
    for path, (data, rx) in SPEC.items():
        text = open(path, encoding="utf-8").read()
        done = skipped = 0
        for n in sorted(data):
            text, status = insert(text, rx, n, data[n])
            if status == "disisipkan":
                done += 1
            elif status == "sudah ada":
                skipped += 1
            else:
                print(f"  ! {path} bab {n}: {status}")
        if "\n\n\n" in text:
            sys.exit(f"{path}: ada baris kosong ganda -- tidak ditulis")
        print(f"{path}: {done} paragraf anjuran disisipkan, {skipped} sudah ada")
        if not dry and done:
            open(path, "w", encoding="utf-8").write(text)


if __name__ == "__main__":
    main()
