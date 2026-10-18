# Surviving the Future / Bertahan Hidup di Masa Depan

*Crisis, Climate, and Human Resilience* · *Krisis, Iklim, dan Resiliensi Manusia*
Setyo Wisodo, 2026. Two editions: English (EN) and Indonesian (ID).

The book is a practical, evidence-based guide to climate change for families and communities,
with a focus on Indonesia and Southeast Asia. It has 19 chapters in 5 parts, two appendices
(checklists and emergency contacts), a glossary, a reference list (38 sources, mainly IPCC, WMO,
*Lancet* Countdown, peer-reviewed journals and Indonesian government sources) and an index.

## Ready-to-publish files (`publish/`)

| File | Purpose |
|---|---|
| `*_interior.pdf` | Print interior: 6 × 9 in trim, embedded fonts, no bleed |
| `*_cover_print.pdf` | Full paperback cover wrap (back + spine + front, 0.125 in bleed) |
| `*_cover_front.jpg` | Front cover, 1800 × 2700 px, for the ebook and marketplaces |
| `*.epub` | EPUB 3 ebook |
| `*.docx` | Editable manuscript for editors and publishers |
| `build_report.json` | Page count, word count and spine width per edition |

Current builds: **EN 149 pages, about 29,100 words; ID 153 pages, about 27,600 words.**

## Building

Requirements: Python 3.10+ with `typst`, `pypandoc_binary`, `pypdf` and `pillow`.

```bash
python -m venv .venv && . .venv/bin/activate
pip install typst pypandoc_binary pypdf pillow
python book/build.py          # both editions
python book/build.py id       # Indonesian only
```

Pipeline: Markdown (`src/<lang>/*.md`) → pandoc + `template/filter.lua` → Typst (`.gen/`, ignored by git)
→ `template/book.typ` → PDF. The same Markdown also produces the EPUB and DOCX.

## Source layout

```
book/
  build.py               build script (interior, covers, EPUB, DOCX)
  template/book.typ      page design: typography, running heads, boxes, index
  template/filter.lua    pandoc filter (parts, callout boxes, Indonesian soft hyphens)
  template/epub.css      ebook styles
  src/en/, src/id/       meta.json (title, back cover, copyright, index terms) + chapters
  cover/art.jpg          cover artwork (no text; title is typeset on top)
  fonts/                 Source Serif 4 + Source Sans 3 (SIL Open Font License)
```

Markdown conventions: `# Title {.part number="II"}` starts a part;
`::: {.box title="…" kind="note|action|local"}` makes a callout box; `::: lead` is the chapter opening;
`::: plain` / `::: hanging` are for back matter (the `#` heading must come first).

## Before you publish: checklist

- [ ] **ISBN.** Get ISBNs (in Indonesia: Perpusnas, through a publisher; or the free ISBN from KDP)
      and fill them into `copyright.lines` in `src/<lang>/meta.json`. Then rebuild.
- [ ] **Barcode.** The print cover has a white 2 × 1.2 in box on the back. KDP places the barcode
      there automatically; other printers need the barcode image added.
- [ ] **Spine width.** It is calculated as pages × 0.002252 in (KDP white paper). For cream paper
      (0.0025 in per page) or another printer, change `PAPER_IN_PER_PAGE` in `build.py`.
- [ ] **Proofread.** Have a native-speaker editor proofread both editions, especially the ID edition.
- [ ] **Facts.** Climate figures were checked against sources available in October 2026
      (WMO *State of the Global Climate 2025*, Indicators of Global Climate Change 2024,
      *Lancet* Countdown 2025, Indonesia's Second NDC). Update them for later reprints.
- [ ] **Cover art.** It is AI-generated and was upscaled to about 300 dpi. For an offset print run,
      consider commissioning original art at full resolution.

### KDP settings (paperback)

Trim 6 × 9 in · Interior: black & white (the blue and orange accents print as grey; choose colour printing to keep them) · Paper: white · Bleed: **No bleed** (interior) ·
Cover finish: matte or glossy · Upload `*_interior.pdf` and `*_cover_print.pdf`.
For the ebook (Kindle), upload the `.epub` with `*_cover_front.jpg`.
