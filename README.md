# Surviving the Future

**Crisis, Climate, and Human Resilience** — Setyo Wisodo, 2026
*Bertahan Hidup di Masa Depan* — edisi bahasa Indonesia

A data-rich, academically grounded account of how societies survive the crises caused by global
warming, written for general readers who want the evidence rather than the slogan.

| | English | Bahasa Indonesia |
|---|---|---|
| PDF | `Surviving_the_Future.pdf` (**430 pp**) | `Surviving_the_Future_ID.pdf` (**445 pp**) |
| EPUB | `book/publish/Surviving_the_Future_EN.epub` | `book/publish/Bertahan_Hidup_di_Masa_Depan_ID.epub` |
| DOCX | `book/publish/Surviving_the_Future_EN.docx` | `book/publish/Bertahan_Hidup_di_Masa_Depan_ID.docx` |
| Print cover | `book/publish/Surviving_the_Future_EN_cover_print.pdf` | `book/publish/Bertahan_Hidup_di_Masa_Depan_ID_cover_print.pdf` |
| 3D marketplace image | `book/publish/3d/Surviving_the_Future_EN_3d_square.png` | `book/publish/3d/Bertahan_Hidup_di_Masa_Depan_ID_3d_square.png` |
| Words | 200,465 | 166,917 |
| References | 145 (130 cited in text) | 145 (124 cited in text) |
| In-text citations | 402 | 350 |

## What the book contains

24 chapters, each with numbered sections, a **Case Study** and a **Future Scenarios and Predictions**
section that states which observation would prove the chapter wrong. Plus 25 data tables and 11 data
figures drawn from those tables, appendices
with checklists and worksheets, a glossary, an index, 145 references, and notes on event sources.

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

`check_citations.py` (402/350 citations, 0 problems), `fact_check.py` (0 failures),
`data_consistency.py`, `audit_production.py` (both PDFs clean: metadata, 327-entry outline, no blank
pages or margin overflow, embedded fonts), `audit_redundancy.py` (0 paragraph pairs scoring ≥ 5.0 in
either edition), `audit_epub.py` (EPUB 3 structure, both editions clean). See `BOOK_READINESS.md`
for the publication-readiness assessment and the short list of decisions only the author can make. Gate reports: `GATE2_REPORT.md` … `GATE6_REPORT.md`.
