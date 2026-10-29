# Surviving the Future / Bertahan Hidup di Masa Depan

*Crisis, Climate, and Human Resilience* · *Krisis, Iklim, dan Ketahanan Manusia*
Setyo Wisodo, 2026. Two editions: English (EN) and Indonesian (ID).

**Sold edition: English only** (decision of 29 October 2026). The Indonesian edition is
kept as a cross-check for copy-editing — every number and argument is verified against
it — and is not published, promoted, or sold.

A data-rich, academically grounded guide to living through the crises caused by global warming:
24 chapters, 25 data tables, 24 case studies, appendices (checklists, glossary, index, references,
notes on event sources), and **152 works cited plus 23 further reading** per edition. Every chapter closes with a numbered
Case Study and a Future Scenarios section that states what would falsify its own predictions.

## Current build

| | EN | ID |
|---|---|---|
| Pages (A4, 12 pt Tinos) | **457** | **473** |
| Words (`wc -w`) | **212,489** | **176,674** |
| In-text citations | 698 | 662 |
| References | 152 works cited + 23 further reading | 152 works cited + 27 further reading |
| PDF outline entries | 327 | 327 |
| Data figures | 11 | 11 |

## Ready-to-publish files (`publish/`)

| File | Purpose |
|---|---|
| `Surviving_the_Future.pdf` (repo root) | A4 reading/print PDF, 457 pp |
| `Surviving_the_Future_ID.pdf` (repo root) | A4 reading/print PDF, 473 pp |
| `*_cover_print.pdf` | Full paperback wrap (back + spine + front), 300 dpi, 0.125 in bleed, spine sized from the page count, with a white 2 × 1.2 in retail barcode area |
| `*_cover_front.jpg` | Front cover at the trim ratio (2550 × 3608, 300 dpi): artwork, typography, quote |
| `*_cover_ebook.jpg` | Ebook cover at the 1:1.6 ratio stores ask for (1600 × 2560), used inside the EPUB |
| `3d/*_3d_square.png` | 3D book render, 2000 × 2000, white background, for marketplace listings |
| `3d/*_3d_transparent.png` | Same render on a transparent background, for banners and composites |
| `3d/*_3d_front.png` | 3D render at a shallower angle, for product galleries |
| `3d/*_3d_back.png` | 3D render from behind: the real back panel, barcode box removed |
| `3d/*_3d_front_back.png` | Front and back in one frame, for stores that allow one gallery image |
| `3d/pair_3d_square.png` | Both editions side by side in one frame |
| `marketplace/` | Six 3000 px angles per edition, for Amazon/Etsy/Gumroad; the pair lineup is only for a bundle that is not offered |
| `*_sample.pdf` | Free sample: full contents, preface, all of Chapter 1, one figure spread, closing page |
| `sold/*.pdf` | Per-buyer copies with a licence page and a name on every page (git-ignored) |
| `gumroad/` | Marketplace covers (2560×1440), thumbnails (1600×1600), profile avatar (800×800) and paste-ready listing copy |
| `*_figures.zip` | Figure pack sold with the book: 11 figures at 300 dpi, captions, source lines, licence |
| `book/cover/art_cover_v1.png` | Raw artwork for the front cover; `make_cover_front.py` composites artwork + typography |
| `book/cover/SKILL_open_generative_ai.md` | The prompt-compiler skill (from Anil-matcha/Open-Generative-AI, MIT) used to write the cover prompt |
| `*.epub` | EPUB 3 ebook (title and copyright pages, nav + NCX + landmarks, accessibility metadata, XHTML tables with `th scope`, `<figure>` blocks with alternative text) |
| `*.docx` | Editable manuscript: A4, Times New Roman 12 pt, justified, 12.7 mm indent, Heading styles, TOC field, running heads, page numbers, figures at 150 mm with `descr` alt text |
| `*_interior.pdf` | Byte-identical copy of the A4 interior PDF (457 / 473 pp) for uploading with the cover |
| `build_report.json` | Page count, trim, bleed, spine width, cover size, dpi and file paths per edition |

The interior PDFs are A4 with 30 mm margins, and `book/publish/*_interior.pdf` are byte-identical
copies of the same files, kept beside the cover and ebook so a printer can take the interior and the
wraparound from one folder.

## Building

Requirements: Python 3.10+ with `fpdf2`, `pyphen`, `pymupdf`, `python-docx`, `pillow`, `matplotlib`.

```bash
pip install --break-system-packages fpdf2 pyphen pymupdf python-docx pillow matplotlib

python make_figures.py                             # figures/*.png (EN + *_id.png)
python gen_book.py && python gen_book_id.py      # book.md, book_id.md (figures inserted)
python tools/plagiarism/check.py                  # internal similarity + citation discipline
python check_citations.py && python fact_check.py
python render_book.py && python render_book_id.py  # the two A4 PDFs
cp Surviving_the_Future.pdf book/publish/Surviving_the_Future_EN_interior.pdf
cp Surviving_the_Future_ID.pdf book/publish/Bertahan_Hidup_di_Masa_Depan_ID_interior.pdf
python make_publish.py                             # EPUB + DOCX
python make_cover_front.py                         # front + ebook covers from the artwork
python make_3d.py                                  # 3D renders for marketplaces
python make_marketplace.py                         # final 3000 px marketplace photos
python make_sample.py                              # free samples (36 / 38 pages)
python personalize_pdf.py --edition id --name "Nama Pembeli" --order INV-001
python make_gumroad.py                               # Gumroad covers + thumbnails
python make_figure_pack.py                           # figure packs for buyers (11 PNG each)
python make_cover.py                               # print wraps + build_report.json
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
| `audit_epub.py` | EPUB 3 structure without `epubcheck`: mimetype, container, manifest/spine, link and anchor targets, nav vs NCX, well-formedness |
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
references.py                   REFS_EN / REFS_ID, 175 entries each
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
