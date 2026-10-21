#!/usr/bin/env python3
"""Build the publication files for "Surviving the Future" (EN) and
"Bertahan Hidup di Masa Depan" (ID).

Outputs (book/publish/):
  <slug>_interior.pdf      print-ready interior, 6x9 in, fonts embedded
  <slug>_cover_print.pdf   full-wrap cover (back + spine + front) incl. bleed
  <slug>_cover_front.jpg   front cover for ebook stores / marketplaces
  <slug>.epub              EPUB 3 ebook
  <slug>.docx              editable manuscript for editors / publishers

Usage:  python book/build.py [en|id ...]      (default: both)
Requires: pip install typst pypandoc_binary pypdf pillow
"""
import json
import pathlib
import re
import shutil
import sys

import pypandoc
import typst
from pypdf import PdfReader

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / "src"
GEN = ROOT / ".gen"
PUB = ROOT / "publish"
FONTS = [str(ROOT / "fonts")]
FILTER = str(ROOT / "template" / "filter.lua")

# Paper thickness (inches per page) for spine width; KDP/IngramSpark white paper.
PAPER_IN_PER_PAGE = 0.002252
BLEED_IN = 0.125


def tstr(s: str) -> str:
    """Escape a Python string as a Typst string literal."""
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def md_to_typst(md_path: pathlib.Path, lang: str) -> str:
    return pypandoc.convert_file(
        str(md_path), "typst", format="markdown+smart",
        extra_args=[f"--lua-filter={FILTER}", f"--metadata=lang:{lang}", "--wrap=none"],
    )


def build_interior(lang: str, meta: dict) -> pathlib.Path:
    src = SRC / lang
    out = GEN / lang
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    sections = {"front": [], "main": [], "back": []}
    for md in sorted(src.glob("*.md")):
        name = md.stem
        kind = "front" if name.startswith("0") else "back" if name.startswith("9") else "main"
        (out / f"{name}.typ").write_text(
            '#import "../../template/book.typ": *\n' + md_to_typst(md, lang), encoding="utf-8")
        sections[kind].append(name)

    rxf = shy_tolerant if lang == "id" else (lambda r: r)
    terms = ",\n  ".join(f"({tstr(k)}, {tstr(rxf(rx))})" for k, rx in meta["index_terms"])
    inc = lambda names: "\n".join(f'#include "{n}.typ"' for n in names)
    c = meta["copyright"]
    copyright_lines = "\n\n".join(c["lines"])

    main = f'''#import "../../template/book.typ": *
#show: book.with(lang: "{lang}", title: {tstr(meta["title"])}, subtitle: {tstr(meta["subtitle"])},
  author: {tstr(meta["author"])}, year: {tstr(meta["year"])}, keywords: ({", ".join(tstr(k) for k in meta["keywords"])},))

#show: frontmatter

// ---------- half-title ----------
#v(32%)
#align(center, text(font: sans, size: 17pt, weight: "bold", {tstr(meta["title"])}))
#pagebreak()
// ---------- also by / blank verso ----------
#v(1fr)
#pagebreak()

// ---------- title page ----------
#v(18%)
#align(center)[
  #set par(justify: false, first-line-indent: 0pt, leading: 0.45em)
  #text(font: sans, size: 27pt, weight: "bold", {tstr(meta["title"])})
  #v(8pt)
  #text(font: serif, size: 13pt, style: "italic", fill: muted, {tstr(meta["subtitle"])})
  #v(18pt)
  #line(length: 20%, stroke: 1.2pt + warm)
  #v(18pt)
  #text(font: sans, size: 13pt, tracking: 1.5pt, upper({tstr(meta["author"])}))
]
#v(1fr)
#align(center, text(font: sans, size: 9pt, fill: muted, {tstr(meta["publisher"])}))
#pagebreak()

// ---------- copyright page ----------
#set par(first-line-indent: 0pt, justify: false, spacing: 0.9em)
#set text(size: 7.9pt)
#v(1fr)
{copyright_lines}
#pagebreak()
#set par(first-line-indent: 1.2em, justify: true, spacing: 0.68em)
#set text(size: 10.4pt)

// ---------- dedication ----------
#v(30%)
#align(center, text(style: "italic", size: 10.5pt, {tstr(meta["dedication"])}))
#pagebreak(to: "odd")

// ---------- contents ----------
#[
  #show outline.entry.where(level: 1): it => {{
    let el = it.element
    if el.supplement == [Part] {{
      v(0.9em)
      let lbl = query(selector(<partpage>).before(el.location())).last().value
      block(text(font: sans, weight: "bold", size: 9.4pt, fill: accent, upper(lbl + " · ") + upper(el.body)))
    }} else {{
      let num = if el.numbering != none {{ numbering("1", ..counter(heading).at(el.location())) + "  " }} else {{ "" }}
      block(above: 0.55em, link(el.location(), grid(columns: (1.6em, 1fr, auto), column-gutter: 4pt,
        text(fill: muted, num), [#el.body #box(width: 1fr, repeat[ . ])], it.page())))
    }}
  }}
  #heading(level: 1, numbering: none, outlined: false)[{meta["contents_label"]}]
  #set text(size: 9.6pt)
  #outline(title: none, depth: 1)
]
#state("hdr", false).update(true)

{inc(sections["front"])}

#show: mainmatter
#[
#show: idx-marks.with((
  {terms},
))
{inc(sections["main"])}
]

#show: backmatter
{inc(sections["back"])}

#heading(level: 1, numbering: none)[{meta["index_label"]}]
#make-index(lang: "{lang}")
'''
    (out / "main.typ").write_text(main, encoding="utf-8")
    PUB.mkdir(exist_ok=True)
    pdf = PUB / f'{meta["slug"]}_interior.pdf'
    typst.compile(str(out / "main.typ"), output=str(pdf), root=str(ROOT), font_paths=FONTS)
    # pad to an even page count (printers require it)
    return pdf


def build_cover(lang: str, meta: dict, pages: int) -> None:
    spine = max(pages * PAPER_IN_PER_PAGE, 0.06)
    out = GEN / lang
    art = "../../cover/art.jpg"
    blurb = "\n\n".join(meta["back_cover"]["paragraphs"])
    bullets = "\n".join(f"- {b}" for b in meta["back_cover"]["bullets"])
    common = f'''#let serif = ("Source Serif 4",)
#let sans = ("Source Sans 3",)
#let bg = rgb("#0e2233")
#let warm = rgb("#e08a2c")
#let front(w, h) = block(width: w, height: h, clip: true, {{
  place(image("{art}", width: w, height: h, fit: "cover"))
  place(rect(width: w, height: h, fill: gradient.linear(rgb(14,34,51,10), rgb(14,34,51,0), rgb(14,34,51,215), angle: 90deg)))
  place(top + center, dy: 0.62in, box(width: w - 0.9in, align(center)[
    #text(font: sans, size: 12pt, weight: "semibold", tracking: 4pt, fill: white, upper({tstr(meta["author"])}))
  ]))
  place(bottom + center, dy: -0.75in, box(width: w - 0.8in, align(center)[
    #set par(leading: 0.35em)
    #text(font: sans, size: 37pt, weight: "black", fill: white, upper({tstr(meta["title"])}))
    #v(4pt)
    #line(length: 28%, stroke: 2pt + warm)
    #v(6pt)
    #text(font: serif, size: 13pt, style: "italic", fill: rgb("#f1e6d6"), {tstr(meta["subtitle"])})
  ]))
}})
'''
    # ---- front cover only (ebook / marketplace) ----
    (out / "cover_front.typ").write_text(common + '''
#set page(width: 6in, height: 9in, margin: 0pt)
#front(6in, 9in)
''', encoding="utf-8")
    png = PUB / f'{meta["slug"]}_cover_front.png'
    typst.compile(str(out / "cover_front.typ"), output=str(png), format="png", ppi=300, root=str(ROOT), font_paths=FONTS)
    from PIL import Image
    Image.open(png).convert("RGB").save(PUB / f'{meta["slug"]}_cover_front.jpg', quality=92, dpi=(300, 300))
    png.unlink()

    # ---- full wrap (print) ----
    W = 2 * 6 + spine + 2 * BLEED_IN
    H = 9 + 2 * BLEED_IN
    spine_text = spine >= 0.3
    spine_code = ('place(center + horizon, rotate(90deg, reflow: true, text(font: sans, size: 10pt, weight: "bold", '
                  'fill: white, tracking: 1pt, upper(' + tstr(meta["title"]) + ') + h(16pt) + '
                  'text(weight: "regular", fill: warm, ' + tstr(meta["author"]) + '))))') if spine_text else ""
    (out / "cover_print.typ").write_text(common + f'''
#set page(width: {W:.4f}in, height: {H:.4f}in, margin: 0pt, fill: bg)
#set text(font: serif, fill: white)
// back cover
#place(top + left, dx: {BLEED_IN}in, dy: {BLEED_IN}in, block(width: 6in, height: 9in, inset: (x: 0.6in, top: 0.75in, bottom: 0.6in), {{
  set par(justify: true, leading: 0.6em, spacing: 0.9em)
  text(font: sans, size: 15pt, weight: "bold", fill: warm, {tstr(meta["back_cover"]["headline"])})
  v(6pt)
  set text(size: 10pt)
  [{blurb}]
  v(4pt)
  set text(size: 9.6pt)
  [{bullets}]
  v(1fr)
  line(length: 100%, stroke: 0.4pt + rgb("#7d93a8"))
  grid(columns: (1fr, auto), column-gutter: 12pt,
    {{ set par(justify: false); set text(hyphenate: false); text(size: 8.6pt, fill: rgb("#c9d5e0"), [{meta["back_cover"]["about"]}]) }},
    box(width: 2in, height: 1.2in, fill: white, inset: 6pt, align(center + horizon, text(font: sans, size: 7pt, fill: rgb("#555"), [ISBN / barcode area\\ 2 × 1.2 in]))))
}}))
// spine
#place(top + left, dx: {BLEED_IN + 6:.4f}in, dy: 0in, block(width: {spine:.4f}in, height: {H:.4f}in, fill: rgb("#0a1824"), {{
  {spine_code}
}}))
// front cover (with bleed on right/top/bottom)
#place(top + left, dx: {BLEED_IN + 6 + spine:.4f}in, dy: 0in, front({6 + BLEED_IN:.4f}in, {H:.4f}in))
''', encoding="utf-8")
    typst.compile(str(out / "cover_print.typ"), output=str(PUB / f'{meta["slug"]}_cover_print.pdf'),
                  root=str(ROOT), font_paths=FONTS)
    return spine


def build_epub_docx(lang: str, meta: dict) -> None:
    files = [str(p) for p in sorted((SRC / lang).glob("*.md"))]
    md_meta = ROOT / ".gen" / lang / "epub_meta.yaml"
    md_meta.write_text(
        "---\n"
        f'title: "{meta["title"]}"\nsubtitle: "{meta["subtitle"]}"\nauthor: "{meta["author"]}"\n'
        f'lang: {lang}\ndate: "{meta["year"]}"\npublisher: "{meta["publisher"]}"\n'
        f'rights: "{meta["copyright"]["rights_short"]}"\n'
        f'description: "{meta["back_cover"]["paragraphs"][0]}"\n'
        f'subject: [{", ".join(json.dumps(k) for k in meta["keywords"])}]\n'
        "toc-title: \"" + meta["contents_label"] + "\"\n---\n", encoding="utf-8")
    common = [f"--lua-filter={FILTER}", f"--metadata=lang:{lang}", "--toc", "--toc-depth=1"]
    pypandoc.convert_file([str(md_meta)] + files, "epub3", format="markdown+smart",
        outputfile=str(PUB / f'{meta["slug"]}.epub'),
        extra_args=common + ["--split-level=1", f"--css={ROOT / 'template' / 'epub.css'}",
                             f"--epub-cover-image={PUB / (meta['slug'] + '_cover_front.jpg')}",
                             *[f"--epub-embed-font={f}" for f in (ROOT / 'fonts').glob('SourceSerif4-*.otf')]])
    pypandoc.convert_file([str(md_meta)] + files, "docx", format="markdown+smart",
        outputfile=str(PUB / f'{meta["slug"]}.docx'), extra_args=common)


def words(lang: str) -> int:
    txt = " ".join(p.read_text(encoding="utf-8") for p in (SRC / lang).glob("*.md"))
    txt = re.sub(r"[#*>|:{}\[\]-]", " ", txt)
    return len(txt.split())


def shy_tolerant(rx):
    """Allow an optional soft hyphen (inserted by filter.lua for Indonesian) after each letter."""
    prefix = ""
    if rx.startswith("(?i)"):
        prefix, rx = "(?i)", rx[4:]
    out, i = [], 0
    while i < len(rx):
        ch = rx[i]
        if ch == "\\" and i + 1 < len(rx):
            out.append(rx[i:i + 2]); i += 2; continue
        out.append(ch)
        if ch.isalpha() and i + 1 < len(rx) and rx[i + 1].isalpha():
            out.append("\u00ad?")
        i += 1
    return prefix + "".join(out)


def main(langs):
    rp = PUB / "build_report.json"
    report = json.loads(rp.read_text(encoding="utf-8")) if rp.exists() else {}
    for lang in langs:
        meta = json.loads((SRC / lang / "meta.json").read_text(encoding="utf-8"))
        pdf = build_interior(lang, meta)
        pages = len(PdfReader(str(pdf)).pages)
        spine = build_cover(lang, meta, pages)
        build_epub_docx(lang, meta)
        report[lang] = {"pages": pages, "words": words(lang), "spine_in": round(spine, 3)}
        print(f"[{lang}] {pages} pages, {report[lang]['words']} words, spine {spine:.3f} in -> {PUB}")
    (PUB / "build_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv[1:] or ["en", "id"])
