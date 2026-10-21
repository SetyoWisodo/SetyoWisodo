# -*- coding: utf-8 -*-
"""Renderer buku: justify dua sisi, indent 12,7 mm, daftar isi & daftar tabel
dengan nomor halaman, judul bab tengah-atas HURUF BESAR 12 pt, dan tabel
bercaption (Table 3.1 ...).

Dipakai oleh render_book.py (EN) dan render_book_id.py (ID).
"""
import re
from fpdf import FPDF

BODY_PT = 12.0
LINE_H = 5.1          # mm, ~1.2 x 12 pt
INDENT = 12.7         # mm, awal paragraf masuk
FONT_DIR = "/home/user/SetyoWisodo/fonts"

L = {
    "en": {
        "toc": "TABLE OF CONTENTS",
        "lot": "LIST OF TABLES",
        "chapter": "Chapter",
        "page": "page",
        "contents_hint": "",
        "table_word": "Table",
        "cover_title": "Surviving the Future",
        "cover_sub": "Crisis, Climate, and Human Resilience",
        "cover_tag": "A Data-Driven, Academically Grounded Guide to Living Through the Crises Caused by Global Warming",
        "cover_author": "Setyo Wisodo",
        "cover_year": "2026",
        "cover_edition": "Academic Edition",
    },
    "id": {
        "toc": "DAFTAR ISI",
        "lot": "DAFTAR TABEL",
        "chapter": "Bab",
        "page": "hal.",
        "contents_hint": "",
        "table_word": "Tabel",
        "cover_title": "Surviving the Future",
        "cover_sub": "Krisis, Iklim, dan Ketahanan Manusia",
        "cover_tag": "Panduan Berbasis Data dan Akademik untuk Melewati Krisis Akibat Pemanasan Global",
        "cover_author": "Setyo Wisodo",
        "cover_year": "2026",
        "cover_edition": "Edisi Akademik",
    },
}


# ----------------------------------------------------------------- inline ----
def parse_runs(text):
    """Pecah teks menjadi run (teks, style) dengan style '', 'B', 'I'."""
    runs = []
    pattern = re.compile(r"\*\*(.+?)\*\*|\*(.+?)\*|_(.+?)_", re.DOTALL)
    pos = 0
    for m in pattern.finditer(text):
        if m.start() > pos:
            runs.append((text[pos:m.start()], ""))
        if m.group(1) is not None:
            runs.append((m.group(1), "B"))
        elif m.group(2) is not None:
            runs.append((m.group(2), "I"))
        else:
            runs.append((m.group(3), "I"))
        pos = m.end()
    if pos < len(text):
        runs.append((text[pos:], ""))
    # buang penanda sisa
    cleaned = []
    for txt, st in runs:
        txt = txt.replace("**", "").replace("`", "")
        txt = re.sub(r"\[\^\d+\]", "", txt)
        if txt:
            cleaned.append((txt, st))
    return cleaned or [("", "")]


def tokenize(pdf, text):
    """Ubah run menjadi token kata & spasi: (word, style)."""
    tokens = []
    for txt, style in parse_runs(text):
        for piece in re.split(r"(\s+)", txt):
            if not piece:
                continue
            tokens.append((piece, style))
    return tokens


# ------------------------------------------------------------------ text -----
def word_width(pdf, word, style):
    pdf.set_font("TNR", style, BODY_PT)
    return pdf.get_string_width(word)


def break_long_word(pdf, word, style, width):
    """Potong kata yang lebih lebar dari satu baris (mis. URL panjang)."""
    parts, cur = [], ""
    for ch in word:
        if word_width(pdf, cur + ch, style) <= width:
            cur += ch
        else:
            parts.append(cur)
            cur = ch
    if cur:
        parts.append(cur)
    return parts


def layout_lines(pdf, tokens, first_width, width):
    """Bagi token menjadi baris-baris sesuai lebar (greedy)."""
    lines, cur, cur_w = [], [], 0.0
    limit = first_width
    for word, style in tokens:
        if word.isspace():
            if cur and not cur[-1][0].isspace():
                w = word_width(pdf, " ", style)
                cur.append((" ", style, w))
                cur_w += w
            continue
        w = word_width(pdf, word, style)
        if w > width:  # kata sangat panjang
            for part in break_long_word(pdf, word, style, width):
                pw = word_width(pdf, part, style)
                if cur_w + pw > limit and cur:
                    lines.append((cur, cur_w))
                    cur, cur_w, limit = [], 0.0, width
                cur.append((part, style, pw))
                cur_w += pw
            continue
        if cur_w + w > limit and cur:
            lines.append((cur, cur_w))
            cur, cur_w, limit = [], 0.0, width
        cur.append((word, style, w))
        cur_w += w
    if cur:
        lines.append((cur, cur_w))
    return lines


def draw_paragraph(pdf, text, indent=INDENT, align="J", size=BODY_PT,
                   line_h=LINE_H, left=0.0, right=0.0):
    """Paragraf rata kiri-kanan (justify) dengan baris pertama masuk 12,7 mm."""
    tokens = tokenize(pdf, text.strip())
    if not tokens:
        return
    epw = pdf.epw - left - right
    lines = layout_lines(pdf, tokens, epw - indent, epw)
    if not lines:
        return
    # hindari 1-2 baris menggantung di dasar halaman
    if pdf.get_y() + min(len(lines), 3) * line_h > pdf.page_break_trigger:
        pdf.add_page()
        pdf.set_y(pdf.t_margin)
    for i, (line, _used) in enumerate(lines):
        if pdf.get_y() + line_h > pdf.page_break_trigger:
            pdf.add_page()
            pdf.set_y(pdf.t_margin)
        words = [(txt, st, w) for (txt, st, w) in line if not txt.isspace()]
        if not words:
            continue
        y = pdf.get_y()
        first = (i == 0)
        x = pdf.l_margin + left + (indent if first else 0.0)
        avail = epw - (indent if first else 0.0)
        is_last = (i == len(lines) - 1)
        pdf.set_font("TNR", "", size)
        space_w = pdf.get_string_width(" ")
        n = len(words)
        total = sum(w for _, _, w in words)
        extra = 0.0
        if align == "J" and not is_last and n > 1:
            extra = max(0.0, avail - total - space_w * (n - 1))
        gap = space_w + (extra / (n - 1) if n > 1 else 0.0)
        pdf.set_xy(x, y)
        for j, (w_txt, st, w) in enumerate(words):
            pdf.set_font("TNR", st, size)
            pdf.cell(w, line_h, w_txt, border=0, align="L")
            if j < n - 1:
                pdf.set_font("TNR", "", size)
                pdf.cell(gap, line_h, "", border=0)
        pdf.set_xy(pdf.l_margin, y + line_h)


def draw_heading(pdf, text, level, chapter_no=None, lang="en"):
    """Judul: H1 tengah-atas HURUF BESAR 12 pt; H2/H3 kiri, tebal."""
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text).strip()
    size = BODY_PT
    h = LINE_H * 1.4
    if pdf.get_y() < pdf.t_margin:
        pdf.set_y(pdf.t_margin)
    if level == 1:
        if pdf.get_y() > pdf.t_margin + 2:
            pdf.add_page()
            pdf.set_y(pdf.t_margin)
        pdf.ln(1.0)
        pdf.set_font("TNR", "B", size)
        m = re.match(r"^(Chapter|Bab)\s+([0-9]+|[A-Z])\s*[:\u2013-]\s*(.+)$", text)
        if m and m.group(2).isdigit():
            # halaman pembuka bab: "CHAPTER 1" satu baris, judul bab di baris bawahnya
            pdf.multi_cell(0, 5.6, f"{m.group(1).upper()} {m.group(2)}", align="C")
            pdf.ln(1.4)
            pdf.multi_cell(0, h, m.group(3).strip().upper(), align="C")
        else:
            pdf.multi_cell(0, h, text.upper(), align="C")
        pdf.ln(2.0)
        return
    need = h * (2 if level == 2 else 1) + 7
    if pdf.get_y() + need > pdf.page_break_trigger:
        pdf.add_page()
        pdf.set_y(pdf.t_margin)
    pdf.ln(1.8 if level == 2 else 1.2)
    pdf.set_font("TNR", "B" if level <= 2 else "BI", size)
    pdf.multi_cell(0, h, text, align="L")
    pdf.ln(1.0 if level == 2 else 0.6)


# ----------------------------------------------------------------- table -----
def draw_table(pdf, rows, caption=None, lang="en", col_widths=None):
    """Gambar tabel bergaris dengan caption di atas (Table 3.1 ...)."""
    from fpdf.fonts import FontFace
    if not rows:
        return
    ncol = max(len(r) for r in rows)
    rows = [r + [""] * (ncol - len(r)) for r in rows]
    total_w = pdf.epw
    pad = 1.3
    if col_widths is None:
        if ncol == 2:
            col_widths = [0.22, 0.78]
        else:
            # Lebar adaptif: penuhi dulu kata terpanjang tiap kolom,
            # lalu bagi sisa ruang sesuai panjang rata-rata isi.
            pdf.set_font("TNR", "", BODY_PT * 0.85)
            longest, avg = [], []
            for ci in range(ncol):
                toks = []
                for r in rows:
                    toks += [t.strip() for t in str(r[ci]).split() if t.strip()]
                longest.append(max([pdf.get_string_width(t) for t in toks] or [0]) + 2 * pad + 0.6)
                avg.append(sum(len(t) for t in toks) / max(1, len(toks)))
            mins = longest
            if sum(mins) > total_w * 0.92:
                scale = (total_w * 0.92) / sum(mins)
                mins = [m * scale for m in mins]
            spare = max(0.0, total_w - sum(mins))
            weight = [max(1.0, a) ** 0.7 for a in avg]
            tot_w = sum(weight) or 1.0
            widths = [mins[i] + spare * weight[i] / tot_w for i in range(ncol)]
            col_widths = None
    if col_widths is not None:
        widths = [total_w * f for f in col_widths]
    cell_h = 4.9

    def cell_lines(txt, width):
        return layout_lines(pdf, tokenize(pdf, txt), width - 2 * pad, width - 2 * pad)

    heights = []
    for r in rows:
        hs = [len(cell_lines(c, widths[i])) or 1 for i, c in enumerate(r)]
        heights.append(max(hs) * cell_h + 2 * pad)

    cap_h = (cell_h * 2 + 3.0) if caption else 0.0
    need = cap_h + sum(heights) + 2
    if pdf.get_y() + need > pdf.page_break_trigger:
        pdf.add_page()
        pdf.set_y(pdf.t_margin)

    if pdf.get_y() < pdf.t_margin:
        pdf.set_y(pdf.t_margin)
    if caption:
        pdf.ln(1.4)
        pdf.set_font("TNR", "B", BODY_PT)
        pdf.multi_cell(0, cell_h, caption, align="C")
        pdf.ln(1.2)
    table_page = pdf.page

    y0 = pdf.get_y()
    for ri, r in enumerate(rows):
        x = pdf.l_margin
        y = pdf.get_y()
        hh = heights[ri]
        for ci, txt in enumerate(r):
            w = widths[ci]
            is_head = (ri == 0)
            pdf.set_draw_color(60, 60, 60)
            pdf.set_line_width(0.2)
            pdf.rect(x, y, w, hh)
            pdf.set_xy(x + pad, y + pad)
            pdf.set_font("TNR", "B" if is_head else "", BODY_PT * 0.85)
            for ln, _ in cell_lines(txt, w):
                line_txt = "".join(t for t, _, _ in ln).strip()
                pdf.set_x(x + pad)
                pdf.cell(w - 2 * pad, cell_h, line_txt, border=0, align="L")
                pdf.ln(cell_h)
            x += w
        pdf.set_xy(pdf.l_margin, y + hh)
    pdf.ln(2.2)
    return table_page


# ------------------------------------------------------------------ toc ------
def toc_line_height(pdf, label, indent=0.0):
    """Perkirakan tinggi satu entri daftar isi (mm) untuk cegah terpotong."""
    h = 5.8
    pdf.set_font("TNR", "", BODY_PT)
    page_w = pdf.get_string_width("000") + 2.0
    avail_label = pdf.epw - indent - page_w - 4.0
    words, lines, cur = label.split(), [], ""
    for w in words:
        cand = (cur + " " + w).strip()
        if pdf.get_string_width(cand) <= avail_label or not cur:
            cur = cand
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return max(1, len(lines)) * h


def draw_toc_line(pdf, label, page_no, indent=0.0, bold=False):
    """Baris daftar isi: judul ... nomor halaman; judul panjang dibungkus."""
    h = 5.8
    x0 = pdf.l_margin + indent
    page_txt = str(page_no)
    pdf.set_font("TNR", "B" if bold else "", BODY_PT)
    page_w = pdf.get_string_width("000") + 2.0
    avail_label = pdf.epw - indent - page_w - 4.0
    words = label.split()
    lines, cur = [], ""
    for w in words:
        cand = (cur + " " + w).strip()
        if pdf.get_string_width(cand) <= avail_label or not cur:
            cur = cand
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    for i, ln in enumerate(lines):
        last = (i == len(lines) - 1)
        pdf.set_x(x0)
        pdf.set_font("TNR", "B" if bold else "", BODY_PT)
        pdf.cell(pdf.get_string_width(ln) + 0.6, h, ln, border=0, align="L")
        if last:
            dot_w = pdf.get_string_width(".")
            lab_w = pdf.get_string_width(ln)
            space = pdf.epw - indent - lab_w - page_w - 1.0
            n_dots = max(3, int(space / dot_w)) if dot_w else 3
            pdf.set_font("TNR", "", BODY_PT)
            dots = "." * n_dots
            pdf.cell(pdf.get_string_width(dots) + 0.6, h, dots, border=0)
            pdf.cell(page_w, h, page_txt, border=0, align="R")
        pdf.ln(h)


def draw_toc(pdf, entries, tables, lang="en"):
    """entries: [(label, page, indent)], tables: [(caption, page)]."""
    cfg = L[lang]
    pdf.add_page()
    pdf.front = False
    pdf.ln(4)
    pdf.set_font("TNR", "B", BODY_PT)
    pdf.cell(0, 7, cfg["toc"], align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    for label, page_no, indent in entries:
        if pdf.get_y() + toc_line_height(pdf, label, indent) > pdf.page_break_trigger:
            pdf.add_page()
            pdf.set_y(pdf.t_margin)
        draw_toc_line(pdf, label, page_no, indent=indent)
    pdf.add_page()
    pdf.set_font("TNR", "B", BODY_PT)
    pdf.cell(0, 7, cfg["lot"], align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    for caption, page_no in tables:
        if pdf.get_y() + toc_line_height(pdf, caption) > pdf.page_break_trigger:
            pdf.add_page()
            pdf.set_y(pdf.t_margin)
        draw_toc_line(pdf, caption, page_no)


# ------------------------------------------------------------------ book -----
class Book(FPDF):
    def __init__(self, lang="en"):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.lang = lang
        self.set_margins(left=30, top=30, right=30)
        self.set_auto_page_break(auto=True, margin=40)
        import os
        _tinos = FONT_DIR + "/Tinos-Regular.ttf"
        if os.path.exists(_tinos):
            _fam = ("Tinos-Regular", "Tinos-Bold", "Tinos-Italic", "Tinos-BoldItalic")
        else:
            _fam = ("DejaVuSerif", "DejaVuSerif-Bold", "DejaVuSerif-Italic",
                    "DejaVuSerif-BoldItalic")
        self.add_font("TNR", "", FONT_DIR + "/%s.ttf" % _fam[0], uni=True)
        self.add_font("TNR", "B", FONT_DIR + "/%s.ttf" % _fam[1], uni=True)
        self.add_font("TNR", "I", FONT_DIR + "/%s.ttf" % _fam[2], uni=True)
        self.add_font("TNR", "BI", FONT_DIR + "/%s.ttf" % _fam[3], uni=True)
        self.set_font("TNR", "", BODY_PT)
        self.chapter_title = None
        self.front = True          # cover + TOC
        self.opening = False       # halaman pembuka bab
        self.chapter_starts = set()

    def header(self):
        """Tanpa header berjalan: judul bab hanya dicetak di halaman pembuka bab."""
        return

    def footer(self):
        if self.page == 1:
            return
        y_saved = self.get_y()
        self.set_y(-14)
        self.set_font("TNR", "", BODY_PT)
        num = "%d" % self.page
        if self.page in self.chapter_starts:
            self.cell(0, 5, num, align="C")
        else:
            self.cell(0, 5, num, align="R")
        self.set_y(y_saved)


def parse_markdown(path):
    with open(path, encoding="utf-8") as fh:
        raw = fh.read()
    lines = []
    for ln in raw.split("\n"):
        if re.match(r"^\[\^\d+\]:", ln.strip()):
            continue
        lines.append(ln.rstrip())
    return lines


def split_blocks(lines):
    """Ubah baris markdown menjadi blok terstruktur."""
    blocks, i = [], 0
    while i < len(lines):
        s = lines[i]
        if not s.strip():
            i += 1
            continue
        if s.strip() == "---":
            i += 1
            continue
        m = re.match(r"^(#{1,3})\s+(.*)$", s)
        if m:
            blocks.append(("h%d" % len(m.group(1)), m.group(2).strip(), ""))
            i += 1
            continue
        m = re.match(r"^\[\[TABLE:\s*(.*?)\]\]\s*$", s)
        if m:
            blocks.append(("caption", m.group(1), ""))
            i += 1
            continue
        if s.strip().startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
                    rows.append(cells)
                i += 1
            blocks.append(("table", rows, ""))
            continue
        if s.strip().startswith("> "):
            blocks.append(("quote", s.strip()[2:].strip(), ""))
            i += 1
            continue
        if s.strip().startswith("- "):
            blocks.append(("li", s.strip()[2:].strip(), ""))
            i += 1
            continue
        m = re.match(r"^\d+\.\s+(.*)$", s.strip())
        if m:
            blocks.append(("li", m.group(1).strip(), ""))
            i += 1
            continue
        # paragraf: gabung baris berurutan
        para = [s.strip()]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(
                r"^(#{1,3}\s|\[\[TABLE:|\||- |> |\d+\.\s)", lines[i].strip()):
            para.append(lines[i].strip())
            i += 1
        blocks.append(("p", " ".join(para), ""))
    return blocks


def render(md_path, out_pdf, lang="en", title=None):
    cfg = L[lang]
    blocks = split_blocks(parse_markdown(md_path))

    def build(page_map=None, table_map=None):
        pdf = Book(lang)
        # ---------- cover ----------
        pdf.add_page()
        pdf.ln(38)
        pdf.set_font("TNR", "B", BODY_PT)
        for _ in range(2):
            pdf.ln(7)
        pdf.set_font("TNR", "B", BODY_PT)
        pdf.multi_cell(0, 9, cfg["cover_title"].upper(), align="C")
        pdf.ln(5)
        pdf.set_font("TNR", "", BODY_PT)
        pdf.multi_cell(0, 7, cfg["cover_sub"], align="C")
        pdf.ln(3)
        pdf.set_font("TNR", "I", BODY_PT)
        pdf.multi_cell(0, 6.4, cfg["cover_tag"], align="C")
        pdf.ln(30)
        pdf.set_font("TNR", "", BODY_PT)
        pdf.cell(0, 7, cfg["cover_author"], align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 7, cfg["cover_year"], align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 7, cfg["cover_edition"], align="C", new_x="LMARGIN", new_y="NEXT")

        # ---------- daftar isi (2 pass) ----------
        if page_map is None:
            page_map = {}
        if table_map is None:
            table_map = {}
        toc_entries = []
        for b in blocks:
            if b[0] == "h1":
                label = b[1]
                toc_entries.append((label, page_map.get(label, 0), 0.0))
        pdf.front = True
        draw_toc(pdf, toc_entries, [(c, table_map.get(c, 0)) for c in
                                    [b[1] for b in blocks if b[0] == "caption"]], lang)
        pdf.front = False

        new_pages, new_tables = {}, {}
        caption_pending = None
        li_buf = []

        def flush_li(pdf):
            while li_buf:
                txt = li_buf.pop(0)
                pdf.set_font("TNR", "", BODY_PT)
                bullet_w = pdf.get_string_width("\u2022") + 3.0
                if pdf.get_y() + LINE_H > pdf.page_break_trigger:
                    pdf.add_page()
                    pdf.set_y(pdf.t_margin)
                y = pdf.get_y()
                pdf.set_xy(pdf.l_margin + 2.0, y)
                pdf.cell(bullet_w, LINE_H, "\u2022", border=0)
                draw_paragraph(pdf, txt, indent=0.0, left=bullet_w + 2.0)
                pdf.ln(0.5)

        for kind, val, _ in blocks:
            if kind != "li":
                flush_li(pdf)
            if kind == "h1":
                title_txt = val
                pdf.chapter_title = title_txt
                pdf.add_page()
                pdf.chapter_starts.add(pdf.page)
                new_pages[title_txt] = pdf.page
                draw_heading(pdf, title_txt, 1, lang=lang)
                continue
            if kind == "h2":
                draw_heading(pdf, val, 2)
            elif kind == "h3":
                draw_heading(pdf, val, 3)
            elif kind == "caption":
                caption_pending = val
            elif kind == "table":
                pg = draw_table(pdf, val, caption=caption_pending, lang=lang)
                if caption_pending:
                    new_tables[caption_pending] = pg
                caption_pending = None
            elif kind == "quote":
                draw_paragraph(pdf, val, indent=0.0, left=8.0, right=8.0)
                pdf.ln(0.6)
            elif kind == "li":
                li_buf.append(val)
            elif re.match(r"^\*(Theme|Tema):", val):
                draw_paragraph(pdf, val, indent=0.0, align="L")
                pdf.ln(0.8)
            else:
                draw_paragraph(pdf, val)
        flush_li(pdf)
        return pdf, new_pages, new_tables

    pdf, pages, tables = build()
    # pass berikutnya dengan nomor halaman nyata; ulangi sampai paginasi stabil
    stable = False
    for _ in range(8):
        pdf2, pages2, tables2 = build(pages, tables)
        pdf = pdf2
        if pages2 == pages and tables2 == tables:
            stable = True
            break
        pages, tables = pages2, tables2
    if not stable:
        print("WARNING: pagination not fully stable; last pass used")

    pdf.output(out_pdf)
    return pdf.page, pages, tables
