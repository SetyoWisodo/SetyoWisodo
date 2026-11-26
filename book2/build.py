#!/usr/bin/env python3
"""Bangun PDF buku 17 bab dari berkas Markdown di src/<lang>/.

Alur: markdown --pandoc(filter.lua)--> typst --> main.typ --> PDF.
Jalankan dari mana saja: python3 book2/build.py [--lang id] [--out foo.pdf]
"""
from __future__ import annotations

import argparse
import csv
import json
import pathlib
import re
import sys

try:
    import pypandoc
    import typst
except ImportError as exc:  # pragma: no cover
    sys.exit("Butuh pypandoc + typst: pip install pypandoc_binary typst")

ROOT = pathlib.Path(__file__).resolve().parent
REF = ROOT / "reference"
TPL = ROOT / "template"
GEN = ROOT / ".gen"


def esc(s: str) -> str:
    out = []
    for ch in s:
        if ch in "\\\"#$":
            out.append("\\" + ch)
        elif ch in "[]@<>`*_":
            out.append("\\" + ch)
        else:
            out.append(ch)
    return "".join(out)


def convert(md_file: pathlib.Path, out_file: pathlib.Path, lang: str) -> None:
    out_file.parent.mkdir(parents=True, exist_ok=True)
    text = pypandoc.convert_file(
        str(md_file),
        "typst",
        format="markdown+smart+pipe_tables+footnotes",
        extra_args=[
            f"--lua-filter={TPL / 'filter.lua'}",
            f"--metadata=lang:{lang}",
            "--wrap=none",
        ],
    )
    out_file.write_text(
        '#import "../../template/book.typ": *\n' + text, encoding="utf-8")


def extract_title(md_file: pathlib.Path) -> str:
    for line in md_file.read_text(encoding="utf-8").splitlines():
        if line.startswith("# ") and "{.part" not in line:
            return re.sub(r"^#\s+", "", line).strip()
        if line.startswith("# ") and "{.part" in line:
            return re.sub(r"\s*\{\.part.*$", "", line[2:]).strip()
    return md_file.stem


def sitasi_dipakai(gen_dir: pathlib.Path) -> list[str]:
    """Kunci sitasi dalam urutan kemunculan, dari berkas typst hasil konversi."""
    found: list[str] = []
    for f in sorted(gen_dir.glob("*.typ")):
        for m in re.finditer(r'cite-ref\("([^"]+)"', f.read_text(encoding="utf-8")):
            k = m.group(1).lstrip("@")
            if k not in found:
                found.append(k)
    return found


def tulis_pustaka(gen_dir: pathlib.Path) -> int:
    csv_path = REF / "bibliografi.csv"
    if not csv_path.exists():
        return 0
    with csv_path.open(encoding="utf-8") as fh:
        bib = {r["kunci"]: r for r in csv.DictReader(fh)}
    urut = sitasi_dipakai(gen_dir)
    baris = []
    for i, k in enumerate(urut, 1):
        r = bib.get(k)
        if not r:
            baris.append(f'#bibentry(n: {i})[entri bibliografi tidak ditemukan: {k}]')
            continue
        nama = r.get("penulis") or r["nama"]
        tahun, judul, terbit = r["tahun"], r["judul"], r["penerbit"]
        nama_rapi = nama[:-1] if nama.endswith(".") else nama
        baris.append(
            f'#bibentry(n: {i})[{nama_rapi}. {tahun}. #emph[{judul}]. {terbit}.]')
    gen_dir.joinpath("zz-pustaka.typ").write_text(
        '#import "../../template/book.typ": *\n' + "\n".join(baris), encoding="utf-8")
    return len(urut)


def build(lang: str, out_pdf: pathlib.Path) -> pathlib.Path:
    meta = json.loads((ROOT / f"meta_{lang}.json").read_text(encoding="utf-8"))
    src = ROOT / "src" / lang
    files = sorted(src.glob("*.md"))
    if not files:
        sys.exit(f"Tidak ada berkas .md di {src}")

    gen = GEN / lang
    gen.mkdir(parents=True, exist_ok=True)

    # judul pendek per bab, untuk kepala halaman
    titles = []
    num = 0
    for f in files:
        for line in f.read_text(encoding="utf-8").splitlines():
            if not line.startswith("# "):
                continue
            if "{.unnumbered" in line:
                continue
            num += 1
            title = line[2:].split("{")[0].strip()
            titles.append((num, title.split("—")[0].strip()))

    short_typ = "(" + ", ".join(f'"{n}": "{esc(v)}"' for n, v in titles) + ",)"

    includes = []
    for f in files:
        typ = gen / (f.stem + ".typ")
        convert(f, typ, lang)
        includes.append(typ.relative_to(ROOT).as_posix())

    fonts = sorted({re.sub(r'-(Bold|BoldIt|It|Regular|Semibold|SemiboldIt|Light|Black)$', '', p.stem)
                    for p in (ROOT.parent / "book" / "fonts").glob("*.otf")})
    fontlist = "(" + ", ".join(f'"{f}"' for f in fonts) + ', "DejaVu Serif", "Serif")'
    fontlist = "(" + ", ".join(f'"{f}"' for f in fonts) + ", \"DejaVu Serif\", \"Serif\")" if fonts else "(\"DejaVu Serif\", \"Serif\")"
    n_bib = tulis_pustaka(gen)
    pustaka_isi = ""
    if n_bib:
        isi = (gen / "zz-pustaka.typ").read_text(encoding="utf-8")
        isi = "\n".join(l for l in isi.splitlines() if not l.startswith("#import"))
        judul = "Daftar Pustaka" if lang == "id" else "References"
        pustaka_isi = (f'\n#pagebreak(to: "odd", weak: true)\n'
                       f'#heading(level: 1, numbering: none, outlined: true)[{judul}]\n'
                       f'#v(6pt)\n{isi}\n')
        print(f"pustaka: {n_bib} entri")

    paruh_depan = [p for p in includes if "/99-" not in p]
    paruh_belakang = [p for p in includes if "/99-" in p]
    body = "\n".join(f'#include "{p}"' for p in paruh_depan)
    body += pustaka_isi
    body += "\n".join(f'\n#include "{p}"' for p in paruh_belakang)

    main = f'''#import "template/book.typ": *

#show: book.with(
  title: "{esc(meta["title"])}",
  subtitle: "{esc(meta["subtitle"])}",
  author: "{esc(meta["author"])}",
  year: "{esc(meta["year"])}",
  publisher: "{esc(meta["publisher"])}",
  lang: "{lang}",
  contents-label: "{esc(meta["contents_label"])}",
  index-label: "{esc(meta["index_label"])}",
  dedication: "{esc(meta["dedication"])}",
  keywords: ({", ".join(f'"{esc(k)}"' for k in meta["keywords"])}),
  chapter-short: {short_typ},
)

{body}
'''
    (ROOT / "main.typ").write_text(main, encoding="utf-8")
    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    typst.compile(str(ROOT / "main.typ"), output=str(out_pdf), root=str(ROOT),
                  font_paths=[str(ROOT.parent / "book" / "fonts")])
    return out_pdf


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", default="id")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    out = pathlib.Path(a.out) if a.out else ROOT / "publish" / f"{a.lang}.pdf"
    p = build(a.lang, out)
    print("OK", p, p.stat().st_size, "bytes")
