# -*- coding: utf-8 -*-
"""Sisipkan entri Daftar Pustaka baru pada posisi alfabetis. Idempoten."""
import re

import references as R
from new_refs import NEW_EN, NEW_ID


def insert_sorted(entries, new):
    out = list(entries)
    for entry in new:
        key = entry.lower()
        if any(e.lower() == key for e in out):
            continue
        pos = len(out)
        for i, e in enumerate(out):
            if e.lower() > key:
                pos = i
                break
        out.insert(pos, entry)
    return out


def render(path, refs):
    src = open(path, encoding="utf-8").read()
    start = src.index("REFS_EN = [") if "REFS_EN" in path else src.index("REFS_ID = [")
    head = src[:start]
    tail_start = src.index("]", src.index("[", start)) + 1
    tail = src[tail_start:]
    body = "".join(f'    "{e}",\n' for e in refs)
    return head + "[\n" + body + tail


def main():
    en = insert_sorted(R.REFS_EN, NEW_EN)
    idn = insert_sorted(R.REFS_ID, NEW_ID)
    print(f"EN {len(R.REFS_EN)} -> {len(en)} entri")
    print(f"ID {len(R.REFS_ID)} -> {len(idn)} entri")
    src = open("references.py", encoding="utf-8").read()
    i_en = src.index("REFS_EN = [")
    i_id = src.index("REFS_ID = [")
    # ganti dua blok secara terpisah
    def replace_block(text, marker, entries):
        s = text.index(marker)
        open_b = s + len(marker) - 1
        depth, j = 0, open_b
        while j < len(text):
            if text[j] == "[":
                depth += 1
            elif text[j] == "]":
                depth -= 1
                if depth == 0:
                    break
            j += 1
        body = "[\n" + "".join(f'    "{e}",\n' for e in entries) + "]"
        return text[:s] + marker.rstrip("[") + body + text[j + 1:]

    src = replace_block(src, "REFS_EN = [", en)
    src = replace_block(src, "REFS_ID = [", idn)
    open("references.py", "w", encoding="utf-8").write(src)
    print("references.py ditulis")


if __name__ == "__main__":
    main()
