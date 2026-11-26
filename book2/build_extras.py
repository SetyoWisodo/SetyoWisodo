#!/usr/bin/env python3
"""EPUB, DOCX, dan sampul untuk buku 17 bab.

Pemakaian: python3 book2/build_extras.py [--lang id]
Hasil di book2/publish/.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
import sys

import pypandoc

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / "src"
PUB = ROOT / "publish"
GEN = ROOT / ".gen"
FILTER = ROOT / "template" / "filter.lua"

ART = ROOT.parent / "book" / "cover" / "art.jpg"


def words(text: str) -> int:
    text = re.sub(r"[#*>|:{}\[\]-]", " ", text)
    return len(text.split())


def count(lang: str) -> int:
    return sum(words(p.read_text(encoding="utf-8")) for p in sorted((SRC / lang).glob("*.md")))


def meta_yaml(meta: dict, lang: str) -> pathlib.Path:
    GEN.mkdir(exist_ok=True)
    f = GEN / f"meta_{lang}.yaml"
    f.write_text(
        "---\n"
        f'title: "{meta["title"]}"\n'
        f'subtitle: "{meta["subtitle"]}"\n'
        f'author: "{meta["author"]}"\n'
        f'lang: {lang}\n'
        f'date: "{meta["year"]}"\n'
        f'publisher: "{meta["publisher"]}"\n'
        f'rights: "{meta["copyright"]["rights_short"]}"\n'
        f'description: "{meta["back_cover"]["paragraphs"][0]}"\n'
        f'subject: [{", ".join(json.dumps(k) for k in meta["keywords"])}]\n'
        f'toc-title: "{meta["contents_label"]}"\n'
        "---\n",
        encoding="utf-8",
    )
    return f


def build_epub_docx(lang: str) -> tuple[pathlib.Path, pathlib.Path]:
    meta = json.loads((ROOT / f"meta_{lang}.json").read_text(encoding="utf-8"))
    files = [str(p) for p in sorted((SRC / lang).glob("*.md"))]
    m = meta_yaml(meta, lang)
    common = [
        f"--lua-filter={FILTER}",
        f"--metadata=lang:{lang}",
        "--toc",
        "--toc-depth=1",
    ]
    PUB.mkdir(exist_ok=True)
    epub = PUB / f"{meta['slug']}_{lang}.epub"
    pypandoc.convert_file(
        [str(m)] + files,
        "epub3",
        format="markdown+smart",
        outputfile=str(epub),
        extra_args=common + ["--split-level=1", "--epub-title-page=true"],
    )
    docx = PUB / f"{meta['slug']}_{lang}.docx"
    pypandoc.convert_file(
        [str(m)] + files,
        "docx",
        format="markdown+smart",
        outputfile=str(docx),
        extra_args=common,
    )
    return epub, docx


COVER_TYP = r'''#let serif = ("DejaVu Serif",)
#let sans = ("DejaVu Sans",)
#let bg = rgb("#0d1f2d")
#let warm = rgb("#d9822b")
#let pale = rgb("#f3ece1")

#let cover(w, h, publisher: "", title: "", subtitle: "", author: "", year: "", lead: "") = block(width: w, height: h, clip: true, {
  place(rect(width: w, height: h, fill: bg))
  place(top + center, dy: 0.9in, box(width: w - 0.9in, align(center, {
    set par(leading: 0.4em)
    text(font: sans, size: 10pt, weight: "bold", tracking: 3.4pt, fill: rgb("#8fb3c9"), upper(publisher))
  })))
  place(center + horizon, box(width: w - 0.85in, align(center, {
    set par(leading: 0.42em)
    text(font: sans, size: 33pt, weight: "black", fill: pale, title)
    v(10pt)
    line(length: 30%, stroke: 2pt + warm)
    v(12pt)
    text(font: serif, size: 13.5pt, style: "italic", fill: rgb("#cbd7e0"), subtitle)
  })))
  place(bottom + center, dy: -1.5in, box(width: w - 0.9in, align(center, {
    set par(leading: 0.4em, justify: true)
    set text(hyphenate: false)
    text(font: serif, size: 11.5pt, style: "italic", fill: rgb("#9db3c4"), lead)
  })))
  place(bottom + center, dy: -0.72in, box(width: w - 0.9in, align(center, {
    text(font: sans, size: 12pt, weight: "bold", tracking: 2pt, fill: pale, upper(author))
  })))
  place(bottom + center, dy: -0.45in, box(width: w - 0.9in, align(center, {
    text(font: sans, size: 8.5pt, tracking: 1.2pt, fill: rgb("#7e95a7"), year)
  })))
})
'''


def typstr(v: str) -> str:
    return '"' + v.replace('\\', '\\\\').replace('"', '\\"') + '"'


def build_cover(lang: str) -> pathlib.Path:
    meta = json.loads((ROOT / f"meta_{lang}.json").read_text(encoding="utf-8"))
    GEN.mkdir(exist_ok=True)
    body = COVER_TYP + (
        "\n#set page(width: 6in, height: 9in, margin: 0pt)\n"
        "#cover(6in, 9in, "
        f"publisher: {typstr(meta['publisher'])}, "
        f"title: {typstr(meta['title'])}, "
        f"subtitle: {typstr(meta['subtitle'])}, "
        f"author: {typstr(meta['author'])}, "
        f"year: {typstr(meta['year'])}, "
        f"lead: {typstr(meta['back_cover']['headline'])})"
    )
    typ = GEN / f"cover_{lang}.typ"
    typ.write_text(body, encoding="utf-8")
    png = PUB / f"{meta['slug']}_cover_{lang}.png"
    import typst

    typst.compile(str(typ), output=str(png), format="png", ppi=300, root=str(ROOT))
    jpg = PUB / f"{meta['slug']}_cover_{lang}.jpg"
    subprocess.run(["convert", str(png), "-quality", "94", str(jpg)], check=True)
    png.unlink()
    return jpg


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", default="id")
    a = ap.parse_args()
    print("kata:", count(a.lang))
    jpg = build_cover(a.lang)
    print("cover:", jpg, jpg.stat().st_size)
    epub, docx = build_epub_docx(a.lang)
    print("epub:", epub, epub.stat().st_size)
    print("docx:", docx, docx.stat().st_size)
