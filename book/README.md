# Surviving the Future / Bertahan Hidup di Masa Depan

*Crisis, Climate, and Human Resilience* · *Krisis, Iklim, dan Resiliensi Manusia*
Setyo Wisodo, 2026. Two editions: English (EN) and Indonesian (ID).

A data-rich, academically grounded guide to living through the crises caused by global warming:
24 chapters, 25 data tables, 24 case studies, appendices (checklists, glossary, index, references,
notes on event sources), and **145 references** per edition. Every chapter closes with a numbered
Case Study and a Future Scenarios section that states what would falsify its own predictions.

## Current build

| | EN | ID |
|---|---|---|
| Pages (A4, 12 pt Tinos) | **412** | **432** |
| Words (`wc -w`) | **199,787** | **166,362** |
| In-text citations | 402 | 350 |
| References | 145 (130 cited in text) | 145 (124 cited in text) |
| PDF outline entries | 327 | 327 |

## Ready-to-publish files (`publish/`)

| File | Purpose |
|---|---|
| `Surviving_the_Future.pdf` (repo root) | A4 reading/print PDF, 412 pp |
| `Surviving_the_Future_ID.pdf` (repo root) | A4 reading/print PDF, 432 pp |
| `*_cover_print.pdf` | Full paperback wrap (back + spine + front), 300 dpi, 0.125 in bleed, spine sized from the page count |
| `*_cover_front.jpg` | Front cover, for ebook and marketplaces |
| `*.epub` | EPUB 3 ebook (nav + NCX, XHTML tables, cover page) |
| `*.docx` | Editable manuscript, Times New Roman 12 pt, justified, 12.7 mm first-line indent |
| `*_interior.pdf` | Byte-identical copy of the A4 interior PDF (412 / 432 pp) for uploading with the cover |
| `build_report.json` | Page count, trim, bleed, spine width, cover size, dpi and file paths per edition |

The interior PDFs are A4 with 30 mm margins, and `book/publish/*_interior.pdf` are byte-identical
copies of the same files, kept beside the cover and ebook so a printer can take the interior and the
wraparound from one folder.

## Building

Requirements: Python 3.10+ with `fpdf2`, `pyphen`, `pymupdf`, `python-docx`, `pillow`.

```bash
pip install --break-system-packages fpdf2 pyphen pymupdf python-docx pillow

python gen_book.py && python gen_book_id.py      # book.md, book_id.md
python check_citations.py && python fact_check.py
python render_book.py && python render_book_id.py  # the two A4 PDFs
cp Surviving_the_Future.pdf book/publish/Surviving_the_Future_EN_interior.pdf
cp Surviving_the_Future_ID.pdf book/publish/Bertahan_Hidup_di_Masa_Depan_ID_interior.pdf
python make_publish.py                             # EPUB + DOCX
python make_cover.py                               # print covers + build_report.json
```

`make_cover.py` reads the page count from the interior PDFs, so run the copy step before it. If those
files are missing it prints a warning and falls back to the page count stored in the script, which may
be out of date by a page or two.

## Verification tools

| Script | What it checks |
|---|---|
| `check_citations.py` | every in-text citation has a reference entry, and every entry is cited; no year mismatches |
| `fact_check.py` | ~46 canonical facts (figures, dates, death tolls) agree across the prose |
| `data_consistency.py` | numbers of the same kind do not contradict each other between sentences |
| `audit_production.py` | PDF metadata, outline, blank pages, margin overflow, dangling headings, TOC/page agreement, embedded fonts |
| `audit_redundancy.py` | paragraphs that restate the same facts in different words (scores by shared numbers, names, rare terms) |
| `map_dups.py`, `para_tool.py` | locate and rewrite those paragraphs at their source module |

## Source layout

```
gen_book.py, gen_book_id.py     assemble the manuscripts (gate1 -> gate1b -> style_pass)
content/chNN.py, content_id/    chapter text: sections x.1-x.10, case study, future scenarios
content/depth*.py               layered additions loaded by deep_render.py
deep_render.py                  chapter assembler
book_pdf.py                     PDF renderer (justification, hyphenation, tables, TOC, outline)
style_pass.py, style_variety.py post-generation style transforms (de-templating, dedup)
references.py                   REFS_EN / REFS_ID, 145 entries each
GATE2..GATE6_REPORT.md          gate reports
```

## Design decisions

- **Type:** Tinos (Times-metric, embedded) 12 pt throughout, justified, 12.7 mm first-line indent,
  A4 with 30 mm margins, ~1.2 line spacing.
- **Hyphenation:** `pyphen` (en_US, id_ID), 3 letters minimum each side, no more than two consecutive
  hyphenated lines, never the last word of a paragraph.
- **Page numbers:** centred at the foot of a chapter's opening page, right-aligned elsewhere.
- **Chapter openers:** "CHAPTER n" and the title as two centred lines; the chapter line is not
  repeated on later pages. Every chapter's Case Study and Future Scenarios are numbered sub-chapters.
- **No closing summary blocks:** In sum / Key takeaways / Sources cited / For reflection were removed
  permanently; the narrative carries the argument.
