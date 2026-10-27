# -*- coding: utf-8 -*-
"""Segarkan bagian Daftar Pustaka tanpa membangun ulang seluruh naskah.

book.md dan book_id.md dihasilkan oleh gen_book.py / gen_book_id.py, dan daftar
pustakanya disusun saat pembangunan: hanya karya yang benar-benar dikutip masuk
"Works Cited", sisanya ke "Further Reading". Kalau rujukan baru ditambahkan ke
references.py tanpa membangun ulang seluruh naskah, daftar pustaka di dalam
naskah menjadi basi -- entri yang dikutip di badan tidak muncul di daftar.

Alat ini menyusun ulang HANYA bagian itu, memakai fungsi yang sama dengan
generator (`cited.split_refs`), sehingga naskah dan daftar tetap sinkron tanpa
menyentuh satu paragraf pun di badan buku.

Jalankan: python refresh_refs.py [--dry-run]
"""
import re
import sys

import cited as _cited
from references import REFS_EN, REFS_ID

SPEC = {
    "book.md": dict(refs=REFS_EN, head="# References",
                    cited="## Works Cited", further="## Further Reading",
                    note="These works informed the book's background but are "
                         "not cited in the text."),
    "book_id.md": dict(refs=REFS_ID, head="# Daftar Pustaka",
                       cited="## Karya yang Dikutip",
                       further="## Bacaan Lanjutan",
                       note="Karya-karya ini memperkaya latar buku tetapi tidak "
                            "dikutip di dalam teks."),
}


def main():
    dry = "--dry-run" in sys.argv
    for path, spec in SPEC.items():
        text = open(path, encoding="utf-8").read()
        start = text.index(spec["head"] + "\n")
        body = text[:start]
        rest = text[start:]
        # awal bagian berikutnya setelah daftar pustaka
        m = re.search(r"\n# (?:Index|Indeks)\n", rest)
        tail = rest[m.start():] if m else "\n"
        got, further = _cited.split_refs(spec["refs"],
                                         _cited.pairs(body))
        block = [spec["head"], "", spec["cited"], ""]
        block += [f"- {r}" for r in got]
        block += ["", spec["further"], "", spec["note"], ""]
        block += [f"- {r}" for r in further]
        new = body + "\n".join(block) + "\n\n" + tail.lstrip("\n")
        print(f"{path}: {len(got)} dikutip, {len(further)} bacaan lanjutan")
        if not dry:
            open(path, "w", encoding="utf-8").write(new)


if __name__ == "__main__":
    main()
