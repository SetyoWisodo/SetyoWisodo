# -*- coding: utf-8 -*-
"""Sisipkan kasus kedua ke akhir subbab studi kasus setiap bab.

Paragrafnya ada di `second_cases.py`. Alat ini hanya menaruhnya di tempat yang
benar: tepat sebelum subbab "Skenario dan Prediksi" pada bab yang sama, supaya
kasus tambahan menjadi bagian dari blok studi kasus, bukan bagian dari prediksi.

Idempoten: kalau paragrafnya sudah ada, tidak disisipkan dua kali.

Jalankan: python add_second_cases.py [--dry-run]
"""
import re
import sys

from second_cases import CASES

TARGETS = [("book.md", r"^## %d\.12 Future Scenarios", "en"),
           ("book_id.md", r"^## %d\.12 Skenario", "id")]


def insert(text, chapter, paragraph, pattern):
    marker = paragraph.strip()[:60]
    if marker in text:
        return text, False
    lines = text.split("\n")
    rx = re.compile(pattern % chapter)
    for i, line in enumerate(lines):
        if rx.match(line.strip()):
            block = [paragraph.strip(), ""]
            lines[i:i] = block
            return "\n".join(lines), True
    return text, None


def main():
    dry = "--dry-run" in sys.argv
    for path, pattern, which in TARGETS:
        text = open(path, encoding="utf-8").read()
        added, missing = 0, []
        for chapter, en, idn in CASES:
            paragraph = en if which == "en" else idn
            text, ok = insert(text, chapter, paragraph, pattern)
            if ok is True:
                added += 1
            elif ok is None:
                missing.append(chapter)
        if not dry:
            open(path, "w", encoding="utf-8").write(text)
        print(f"{which}: {added} kasus disisipkan"
              + (f" | bab tidak ketemu: {missing}" if missing else ""))


if __name__ == "__main__":
    main()
