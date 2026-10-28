# Surviving the Future

**Crisis, Climate, and Human Resilience** — Setyo Wisodo, 2026
*Bertahan Hidup di Masa Depan* — edisi bahasa Indonesia

A data-rich, academically grounded account of how societies survive the crises caused by global
warming, written for general readers who want the evidence rather than the slogan.

| | English | Bahasa Indonesia |
|---|---|---|
| PDF | `Surviving_the_Future.pdf` (**456 pp**) | `Surviving_the_Future_ID.pdf` (**472 pp**) |
| EPUB | `book/publish/Surviving_the_Future_EN.epub` | `book/publish/Bertahan_Hidup_di_Masa_Depan_ID.epub` |
| DOCX | `book/publish/Surviving_the_Future_EN.docx` | `book/publish/Bertahan_Hidup_di_Masa_Depan_ID.docx` |
| Print cover | `book/publish/Surviving_the_Future_EN_cover_print.pdf` | `book/publish/Bertahan_Hidup_di_Masa_Depan_ID_cover_print.pdf` |
| 3D marketplace image | `book/publish/3d/Surviving_the_Future_EN_3d_square.png` | `book/publish/3d/Bertahan_Hidup_di_Masa_Depan_ID_3d_square.png` |
| Words | 212,313 | 176,514 |
| References | 172 (149 cited in text) | 172 (145 cited in text) |
| In-text citations | 694 | 659 |

## What the book contains

24 chapters, each with numbered sections, a **Case Study** and a **Future Scenarios and Predictions**
section. Every one of those 24 sections now ends with a paragraph a reader can act on: a target year,
a number or threshold that can be measured, the assumption behind it, the observation that would prove
it wrong, and three indicators to watch. The case studies are the inductive base for those calls — the
more countries a chapter compares, the tighter its forecast. `PREDIKSI_PER_BAB.md` collects all 24 in a
table; `prediction_audit.py` scores them and fails any chapter missing a year, a number, an assumption,
a falsifier, or indicators. Each prediction is followed by an **implementation paragraph**: the trigger
named in the forecast, the order of work once it happens, who does each step, and the one thing not to do.
`ADVICE_PER_BAB.md` collects them; `advice_audit.py` refuses any chapter without a trigger, an order, at
least five steps, a named actor and a prohibition. Plus 25 data tables and 11 data
figures drawn from those tables, appendices
with checklists and worksheets, a glossary, an index, 172 references, and notes on event sources.

The cases are the argument: Bhola 1970 against Amphan 2020 on the same coastline; Europe 2003 against
Europe 2022 at higher temperatures with fewer deaths; the Ahr valley, where the forecast was right and
180 people died anyway; Lytton, where the temperature record and the fire arrived in the same week.

## Building

```bash
pip install --break-system-packages fpdf2 pyphen pymupdf python-docx pillow matplotlib
python make_figures.py                             # the 11 figures, EN and ID
python gen_book.py && python gen_book_id.py
python render_book.py && python render_book_id.py
python make_cover_front.py && python make_cover.py && python make_publish.py
```

See `book/README.md` for the pipeline, the verification tools, and the typographic specification.

## Verification

`check_citations.py` (694/659 citations, 0 problems), `fact_check.py` (0 failures),
`prediction_audit.py` (24/24 chapters pass in both editions), `advice_audit.py` (24/24 implementation
paragraphs pass in both editions), `repetition_audit.py` (EN 48 / ID 57 similar paragraph pairs, down
from 66/70),
`data_consistency.py`, `audit_production.py` (both PDFs clean: metadata, 327-entry outline, no blank
pages or margin overflow, embedded fonts), `audit_redundancy.py` (0 paragraph pairs scoring ≥ 5.0 in
either edition), `audit_epub.py` (EPUB 3 structure, both editions clean). See `BOOK_READINESS.md`
for the publication-readiness assessment and the short list of decisions only the author can make. Gate reports: `GATE2_REPORT.md` … `GATE6_REPORT.md`.
