# -*- coding: utf-8 -*-
"""Renderer buku: justify dua sisi, indent 12,7 mm, daftar isi & daftar tabel
dengan nomor halaman, judul bab tengah-atas HURUF BESAR 12 pt, dan tabel
bercaption (Table 3.1 ...).

Dipakai oleh render_book.py (EN) dan render_book_id.py (ID).
"""
import os
import re
from fpdf import FPDF

BODY_PT = 12.0
LINE_H = 5.1          # mm, ~1.2 x 12 pt
INDENT = 12.7         # mm, awal paragraf masuk
FONT_DIR = "/home/user/SetyoWisodo/fonts"
BOOK_DIR = "/home/user/SetyoWisodo"

L = {
    "en": {
        "toc": "TABLE OF CONTENTS",
        "lot": "LIST OF TABLES AND FIGURES",
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
        "meta_title": "Surviving the Future: Crisis, Climate, and Human Resilience",
        "meta_subject": "Climate change, disaster risk, and human resilience: a data-driven academic guide",
        "meta_keywords": "climate change; disaster risk reduction; adaptation; resilience; heat; flood; drought; preparedness",
        "meta_lang": "en-US",
    },
    "id": {
        "toc": "DAFTAR ISI",
        "lot": "DAFTAR TABEL DAN GAMBAR",
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
        "meta_title": "Surviving the Future: Krisis, Iklim, dan Ketahanan Manusia",
        "meta_subject": "Perubahan iklim, risiko bencana, dan ketahanan manusia: panduan akademik berbasis data",
        "meta_keywords": "perubahan iklim; pengurangan risiko bencana; adaptasi; ketahanan; panas; banjir; kekeringan; kesiapsiagaan",
        "meta_lang": "id-ID",
    },
}


# ------------------------------------------------------ edisi & hak cipta ----
RUNNING = {
    "en": "SURVIVING THE FUTURE",
    "id": "BERTAHAN HIDUP DI MASA DEPAN",
}

COPY = {
    "en": {
        "title": "SURVIVING THE FUTURE",
        "sub": "Crisis, Climate, and Human Resilience",
        "author": "Setyo Wisodo",
        "edition": "First edition, 2026",
        "published": "Published by Setyo Wisodo.",
        "rights": "Copyright \u00a9 2026 Setyo Wisodo. All rights reserved.",
        "legal": ("No part of this publication may be reproduced, distributed, or transmitted in any form "
                  "or by any means, including photocopying, recording, or other electronic or mechanical "
                  "methods, without the prior written permission of the author, except in the case of brief "
                  "quotations embodied in critical reviews and certain other noncommercial uses permitted "
                  "by copyright law."),
        "disclaimer": ("The information in this book is provided for general information and education. It is "
                       "not medical, legal, financial or engineering advice, and it does not replace the "
                       "judgement of a qualified professional. Death tolls, projections and risk estimates are "
                       "those reported by the cited sources at the time of writing; official statistics are "
                       "revised, sometimes for years, and readers should consult the original sources before "
                       "relying on any figure for a decision."),
        "credits": ("Cover design by the author. Set in Tinos, a metric-compatible alternative to Times New "
                    "Roman, 12/15 pt."),
    },
    "id": {
        "title": "BERTAHAN HIDUP DI MASA DEPAN",
        "sub": "Krisis, Iklim, dan Ketahanan Manusia",
        "author": "Setyo Wisodo",
        "edition": "Edisi pertama, 2026",
        "published": "Diterbitkan oleh Setyo Wisodo.",
        "rights": "Hak cipta \u00a9 2026 Setyo Wisodo. Seluruh hak dilindungi.",
        "legal": ("Tidak ada bagian dari publikasi ini yang boleh diperbanyak, didistribusikan, atau "
                  "ditransmisikan dalam bentuk atau dengan cara apa pun, termasuk fotokopi, rekaman, atau "
                  "metode elektronik dan mekanis lainnya, tanpa izin tertulis dari penulis, kecuali untuk "
                  "kutipan singkat dalam ulasan kritis dan penggunaan nonkomersial tertentu yang diizinkan "
                  "oleh undang-undang hak cipta."),
        "disclaimer": ("Informasi dalam buku ini disediakan untuk pengetahuan umum dan pendidikan. Buku ini "
                       "bukan nasihat medis, hukum, keuangan, atau teknik, dan tidak menggantikan pertimbangan "
                       "profesional yang berwenang. Angka kematian, proyeksi, dan estimasi risiko adalah angka "
                       "yang dilaporkan sumber yang dikutip pada saat penulisan; statistik resmi direvisi, "
                       "kadang selama bertahun-tahun, dan pembaca sebaiknya memeriksa sumber aslinya sebelum "
                       "memakai angka apa pun untuk mengambil keputusan."),
        "credits": ("Desain sampul oleh penulis. Disusun dengan Tinos, alternatif metrik yang setara Times New "
                    "Roman, 12/15 pt."),
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
_CUR_PT = BODY_PT      # ukuran huruf aktif, dipakai pengukur lebar kata


def word_width(pdf, word, style):
    pdf.set_font("TNR", style, _CUR_PT)
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


def make_hyphenator(lang):
    """Hyphenator pyphen untuk bahasa tertentu; None bila tidak tersedia."""
    try:
        import pyphen
    except ImportError:
        return None
    try:
        return pyphen.Pyphen(lang={"en": "en_US", "id": "id_ID"}.get(lang, "en_US"))
    except Exception:
        return None


def hyphen_prefix(pdf, word, style, avail):
    """Awalan berhubung yang masih muat di sisa baris, atau None.

    Aturan: hanya kata alfabet, minimal 6 huruf, bukan nama diri (huruf besar
    di awal), minimal 3 huruf sebelum dan sesudah tanda hubung.
    """
    hy = getattr(pdf, "_hyph", None)
    if hy is None or len(word) < 6 or not word.isalpha():
        return None
    if word[0].isupper():
        return None
    try:
        positions = hy.positions(word)
    except Exception:
        return None
    best = None
    for p in positions:
        if p < 3 or len(word) - p < 3:
            continue
        cand = word[:p] + "-"
        if word_width(pdf, cand, style) <= avail:
            best = p
        else:
            break
    if best is None:
        return None
    return word[:best] + "-", word[best:]


def layout_lines(pdf, tokens, first_width, width):
    """Bagi token menjadi baris-baris sesuai lebar (greedy + pemenggalan kata)."""
    lines, cur, cur_w = [], [], 0.0
    limit = first_width
    pending = []
    prev_hyphen = False
    hyphens_run = 0
    idx = 0

    def flush():
        nonlocal cur, cur_w, limit
        lines.append((cur, cur_w))
        cur, cur_w, limit = [], 0.0, width

    while idx < len(tokens) or pending:
        if pending:
            word, style = pending.pop(0)
        else:
            word, style = tokens[idx]
            idx += 1

        if word.isspace():
            if cur and not cur[-1][0].isspace():
                w = word_width(pdf, " ", style)
                cur.append((" ", style, w))
                cur_w += w
            continue

        w = word_width(pdf, word, style)
        if w > width:  # kata sangat panjang (mis. URL)
            if cur:
                flush()
            for part in break_long_word(pdf, word, style, width):
                pw = word_width(pdf, part, style)
                if cur_w + pw > limit and cur:
                    flush()
                cur.append((part, style, pw))
                cur_w += pw
            prev_hyphen = False
            continue

        if cur_w + w > limit and cur:
            last_word = not any(not t[0].isspace() for t in tokens[idx:]) and not pending
            split = (None if (hyphens_run >= 2 or last_word)
                     else hyphen_prefix(pdf, word, style, limit - cur_w))
            if split is not None:
                head, tail = split
                hw = word_width(pdf, head, style)
                cur.append((head, style, hw))
                cur_w += hw
                flush()
                prev_hyphen = True
                hyphens_run += 1
                pending.insert(0, (tail, style))
                continue
            flush()
            prev_hyphen = False
            hyphens_run = 0

        cur.append((word, style, w))
        cur_w += w

    if cur:
        lines.append((cur, cur_w))
    return lines


def draw_paragraph(pdf, text, indent=INDENT, align="J", size=BODY_PT,
                   line_h=LINE_H, left=0.0, right=0.0):
    """Paragraf rata kiri-kanan (justify) dengan baris pertama masuk 12,7 mm."""
    global _CUR_PT
    _CUR_PT = size
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
            if j > 0 and w_txt.strip(".,;:!?)]}") == "" and gap > 0:
                # tanda baca yang terpisah akibat batas run miring: rapatkan
                pdf.set_x(pdf.get_x() - gap)
            pdf.set_font("TNR", st, size)
            pdf.cell(w, line_h, w_txt, border=0, align="L")
            if j < n - 1:
                pdf.set_font("TNR", "", size)
                pdf.cell(gap, line_h, "", border=0)
        pdf.set_xy(pdf.l_margin, y + line_h)


def _bookmark(pdf, text, level):
    """Entri navigasi PDF (bookmark): bab = level 0, sub-bab = level 1."""
    if level > 2:
        return
    label = text.strip()
    if not label:
        return
    try:
        pdf.start_section(label, level=level - 1, strict=False)
    except Exception:
        pass


def draw_heading(pdf, text, level, chapter_no=None, lang="en"):
    """Judul: H1 tengah-atas HURUF BESAR 12 pt; H2/H3 kiri, tebal."""
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text).strip()
    _bookmark(pdf, text, level)
    size = BODY_PT
    h = LINE_H * 1.4
    if pdf.get_y() < pdf.t_margin:
        pdf.set_y(pdf.t_margin)
    if level == 1:
        if pdf.get_y() > pdf.t_margin + 2:
            pdf.add_page()
            pdf.set_y(pdf.t_margin)
        m = re.match(r"^(Chapter|Bab)\s+([0-9]+|[A-Z])\s*[:\u2013-]\s*(.+)$", text)
        if m and m.group(2).isdigit():
            # halaman pembuka bab: nomor bab, judul besar, lalu tema sebagai epigraf
            pdf.ln(20.0)
            try:
                pdf.set_char_spacing(1.8)
            except Exception:
                pass
            pdf.set_font("TNR", "", 10.5)
            pdf.multi_cell(0, 5.4, f"{m.group(1).upper()} {m.group(2)}", align="C")
            try:
                pdf.set_char_spacing(0)
            except Exception:
                pass
            pdf.ln(3.2)
            pdf.set_font("TNR", "B", 19.0)
            pdf.multi_cell(0, 8.2, m.group(3).strip().upper(), align="C")
            pdf.ln(5.0)
        else:
            pdf.ln(16.0)
            pdf.set_font("TNR", "B", 16.0)
            pdf.multi_cell(0, 7.2, text.upper(), align="C")
            pdf.ln(4.0)
        return
    need = h * (2 if level == 2 else 1) + 7
    if pdf.get_y() + need > pdf.page_break_trigger:
        pdf.add_page()
        pdf.set_y(pdf.t_margin)
    pdf.ln(4.2 if level == 2 else 1.6)
    pdf.set_font("TNR", "B" if level <= 2 else "BI", size)
    pdf.multi_cell(0, h, text, align="L")
    pdf.ln(2.0 if level == 2 else 0.8)


# ----------------------------------------------------------------- table -----
def draw_figure(pdf, path, caption, source, lang="en"):
    """Gambar satu blok gambar beserta caption dan baris sumber.

    Gambar tidak pernah dipisahkan dari captionnya: bila tinggi gambar plus
    caption plus sumber tidak muat, halaman baru dibuka lebih dulu.
    """
    if not os.path.isabs(path):
        path = os.path.join(BOOK_DIR, path)
    if not os.path.exists(path):
        print("PERINGATAN: gambar tidak ditemukan:", path)
        return None
    from PIL import Image
    with Image.open(path) as im:
        iw, ih = im.size
    width = pdf.epw
    height = width * ih / iw

    # pisahkan label ("Figure 2.1") dari teks caption bila sudah menyatu
    m = re.match(r"^(Figure|Gambar)\s+([0-9]+\.[0-9]+)\s*(.*)$", caption.strip())
    if m:
        lab, caption = m.group(1) + " " + m.group(2), m.group(3)
    else:
        lab = "Figure" if lang == "en" else "Gambar"
    lab = lab + " "
    # perkiraan tinggi caption + sumber pada lebar kolom
    pdf.set_font("TNR", "B", 9.5)
    cap_w = pdf.get_string_width(lab) + pdf.get_string_width(caption)
    cap_lines = 1 + int(cap_w // (width - 1))
    pdf.set_font("TNR", "", 8.0)
    src_lines = 1 + int(pdf.get_string_width(source) // (width - 1))
    cap_h = 4.6 * cap_lines
    src_h = 4.2 * src_lines
    need = height + 3.0 + cap_h + 1.6 + src_h

    if pdf.get_y() + need > pdf.page_break_trigger:
        pdf.add_page()
        pdf.set_y(pdf.t_margin)
    if pdf.get_y() + height > pdf.page_break_trigger:
        # gambar lebih tinggi daripada satu halaman: kecilkan
        height = pdf.page_break_trigger - pdf.get_y() - cap_h - 6.0
        width = height * iw / ih

    y = pdf.get_y()
    pdf.image(path, x=pdf.l_margin + (pdf.epw - width) / 2.0, y=y, w=width)
    pdf.set_y(y + height + 2.4)
    page = pdf.page

    # caption: label tebal + teks biasa, di tengah
    pdf.set_font("TNR", "B", 9.5)
    lw = pdf.get_string_width(lab)
    pdf.set_font("TNR", "", 9.5)
    tw = pdf.get_string_width(caption)
    if lw + tw <= width - 1:
        x = pdf.l_margin + (pdf.epw - (lw + tw)) / 2.0
        pdf.set_xy(x, pdf.get_y())
        pdf.set_font("TNR", "B", 9.5)
        pdf.cell(lw, 4.6, lab)
        pdf.set_font("TNR", "", 9.5)
        pdf.cell(tw + 1, 4.6, caption)
        pdf.set_xy(pdf.l_margin, pdf.get_y() + 4.6)
    else:
        pdf.set_font("TNR", "B", 9.5)
        pdf.multi_cell(0, 4.6, lab.strip(), align="C")
        pdf.set_font("TNR", "", 9.5)
        pdf.multi_cell(0, 4.6, caption, align="C")
    if source:
        pdf.set_font("TNR", "", 7.6)
        pdf.set_text_color(90, 90, 90)
        pdf.multi_cell(0, 3.9, source, align="C")
        pdf.set_text_color(0, 0, 0)
    pdf.ln(3.4)
    return page


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
    # Tabel utuh lebih disukai; bila tidak muat, tabel dipecah dengan header
    # yang diulang, asalkan setidaknya header + dua baris data muat.
    min_chunk = heights[0] + sum(heights[1:3])
    if pdf.get_y() + need > pdf.page_break_trigger and pdf.get_y() + cap_h + min_chunk > pdf.page_break_trigger:
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

    def draw_row(ri, r):
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

    for ri, r in enumerate(rows):
        avail = pdf.page_break_trigger - pdf.get_y()
        if heights[ri] > avail and ri > 1 and avail < min_chunk + heights[ri] * 0.5:
            pdf.add_page()
            pdf.set_y(pdf.t_margin)
            draw_row(0, rows[0])          # header diulang pada halaman lanjutan
        draw_row(ri, r)
    pdf.ln(2.2)
    return table_page


# ------------------------------------------------------------------ toc ------
ISBN = ""          # isi dengan ISBN 13 digit bila sudah terbit

SEE_ALSO = {
    "en": {
        "adaptation": ["Adaptive capacity", "Climate finance", "Disaster risk reduction"],
        "conflict": ["Displacement", "Food security"],
        "drought": ["Groundwater", "Irrigation", "Water stress"],
        "flood": ["Coastal protection", "Storm surge", "Zoning"],
        "food security": ["Irrigation", "Nutrition"],
        "grid": ["Renewable energy"],
        "heatwave": ["Heat action plan", "Heat mortality"],
        "insurance": ["Climate finance", "Disaster risk reduction"],
        "wildfire": ["Air pollution", "Heat action plan"],
    },
    "id": {
        "adaptasi": ["Kapasitas adaptif", "Pembiayaan iklim", "Pengurangan risiko bencana"],
        "konflik": ["Perpindahan", "Ketahanan pangan"],
        "kekeringan": ["Air tanah", "Irigasi", "Stres air"],
        "banjir": ["Perlindungan pesisir", "Gelombang badai", "Tata guna lahan"],
        "ketahanan pangan": ["Irigasi", "Gizi"],
        "jaringan listrik": ["Energi terbarukan"],
        "gelombang panas": ["Rencana aksi panas", "Kematian akibat panas"],
        "asuransi": ["Pembiayaan iklim", "Pengurangan risiko bencana"],
        "kebakaran": ["Polusi udara", "Rencana aksi panas"],
    },
}



def index_ranges(pages):
    """Rapatkan nomor halaman indeks menjadi rentang, atau 'passim' bila merata."""
    ps = sorted({int(x) for x in pages})
    if not ps:
        return ""
    if len(ps) >= 30:
        return "passim"
    out, i = [], 0
    while i < len(ps):
        j = i
        while j + 1 < len(ps) and ps[j + 1] == ps[j] + 1:
            j += 1
        if j == i:
            out.append(str(ps[i]))
        elif j == i + 1:
            out.append("%d, %d" % (ps[i], ps[j]))
        else:
            out.append("%d\u2013%d" % (ps[i], ps[j]))
        i = j + 1
    return ", ".join(out)


def draw_copyright(pdf, lang="en"):
    """Halaman hak cipta (verso halaman judul)."""
    c = COPY[lang]
    pdf.set_xy(pdf.l_margin, 92)
    pdf.set_font("TNR", "B", 11.5)
    pdf.cell(0, 6, c["title"], align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("TNR", "", 10.5)
    pdf.cell(0, 5.4, c["sub"], align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2.5)
    pdf.cell(0, 5.4, c["author"], align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(13)
    pdf.set_font("TNR", "", 9.5)
    blocks = [(c["edition"], 1.6), (c["published"], 1.6)]
    if ISBN:
        blocks.append(("ISBN " + ISBN, 1.6))
    blocks += [(c["rights"], 3.4), (c["legal"], 3.4), (c["disclaimer"], 3.4), (c["credits"], 0.0)]
    for txt, gap in blocks:
        pdf.multi_cell(0, 4.5, txt, align="L")
        if gap:
            pdf.ln(gap)


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


def draw_toc(pdf, entries, tables, lang="en", figures=None):
    """entries: [(label, page, indent)], tables/figures: [(caption, page)]."""
    cfg = L[lang]
    pdf.front = False
    pdf.running_fallback = cfg["toc"]
    pdf.add_page()
    pdf.ln(4)
    pdf.set_font("TNR", "B", BODY_PT)
    pdf.cell(0, 7, cfg["toc"], align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    first_toc_page = pdf.page
    for label, page_no, indent in entries:
        if pdf.get_y() + toc_line_height(pdf, label, indent) > pdf.page_break_trigger:
            pdf.add_page()
            pdf.set_y(pdf.t_margin)
            if pdf.page > first_toc_page:
                pdf.set_font("TNR", "I", BODY_PT)
                pdf.cell(0, 6, cfg["toc"] + (" (lanjutan)" if lang == "id" else " (continued)"),
                         align="C", new_x="LMARGIN", new_y="NEXT")
                pdf.ln(3)
        draw_toc_line(pdf, label, page_no, indent=indent, bold=(indent == 0.0))
    pdf.running_fallback = cfg["lot"]
    pdf.add_page()
    pdf.set_font("TNR", "B", BODY_PT)
    pdf.cell(0, 7, cfg["lot"], align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    for caption, page_no in tables:
        if pdf.get_y() + toc_line_height(pdf, caption) > pdf.page_break_trigger:
            pdf.add_page()
            pdf.set_y(pdf.t_margin)
        draw_toc_line(pdf, caption, page_no)
    if figures:
        pdf.ln(6)
        pdf.set_font("TNR", "B", BODY_PT)
        pdf.cell(0, 7, "LIST OF FIGURES" if lang == "en" else "DAFTAR GAMBAR",
                 align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2.0)
        for caption, page_no in figures:
            if pdf.get_y() + toc_line_height(pdf, caption, 4.0) > pdf.page_break_trigger:
                pdf.add_page()
                pdf.set_y(pdf.t_margin)
            draw_toc_line(pdf, caption, page_no, indent=4.0)


# ------------------------------------------------------------------ book -----
class Book(FPDF):
    def __init__(self, lang="en"):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.lang = lang
        self.book_lang = lang          # set_lang() menimpa self.lang dengan "en-US"
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
        # margin cermin (gutter) untuk buku jilid: dalam 34 mm, luar 26 mm,
        # sehingga lebar kolom tetap 150 mm dan paginasi tidak bergeser
        self.inner_margin = 34.0
        self.outer_margin = 26.0
        self.running_fallback = ""
        self._hyph = make_hyphenator(lang)
        # --- metadata dokumen (Gate 6) ---
        _cfg = L[lang]
        self.set_title(_cfg["meta_title"])
        self.set_author("Setyo Wisodo")
        self.set_subject(_cfg["meta_subject"])
        self.set_keywords(_cfg["meta_keywords"])
        self.set_creator("Setyo Wisodo")
        self.set_producer("fpdf2")
        self.set_lang(_cfg["meta_lang"])
        try:
            self.set_display_mode("useoutlines")
        except Exception:
            pass

    def _running_title(self):
        """Judul untuk kepala halaman recto: tanpa nomor bab, huruf besar."""
        t = self.chapter_title or self.running_fallback or RUNNING[self.book_lang]
        t = re.sub(r"^(Chapter|Bab)\s+\d+\s*[:.]\s*", "", t)
        t = t.upper()
        if len(t) > 58:
            t = t[:55].rstrip(" ,;:") + "\u2026"
        return t

    def header(self):
        """Kepala halaman berjalan, simetris dan di tengah pada setiap halaman.

        Blok teks memakai margin yang sama (30 mm) di semua halaman, sehingga
        letak teks tidak bergeser antara halaman ganjil dan genap. Halaman 1-2
        (judul dan hak cipta) tanpa kepala; halaman pembuka bab juga tanpa kepala.
        """
        self.set_left_margin(30)
        self.set_right_margin(30)
        self.x = self.l_margin
        if self.page <= 2:
            return
        if self.opening:
            self.opening = False
            return
        y = self.get_y()
        self.set_font("TNR", "", 8.5)
        self.set_xy(self.l_margin, 17.0)
        if self.page % 2 == 0:
            self.cell(self.epw, 5, RUNNING[self.book_lang], align="C")
        else:
            self.cell(self.epw, 5, self._running_title(), align="C")
        self.set_xy(self.l_margin, y)

    def footer(self):
        """Folio: tengah bawah pada halaman pembuka bab, kanan bawah pada sisanya."""
        if self.page <= 2:
            return
        y_saved = self.get_y()
        self.set_y(-14)
        self.set_font("TNR", "", BODY_PT)
        num = "%d" % self.page
        self.cell(0, 5, num, align="C" if self.page in self.chapter_starts else "R")
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


def typographic(s):
    """Kutip tipografis dan spasi satuan: tanda kutip lurus -> ‘ ’ / “ ”,
    dan "2°C" -> "2 °C" agar konsisten di seluruh buku."""
    if not s:
        return s
    out, prev = [], ""
    for ch in s:
        if ch == "'":
            out.append("\u2018" if prev in ("", " ", "\t", "(", "[", "\u2014", "\u2013", "/", "\u201c") else "\u2019")
        elif ch == '"':
            out.append("\u201c" if prev in ("", " ", "\t", "(", "[", "\u2014", "\u2013", "/", "\u2018") else "\u201d")
        else:
            out.append(ch)
        prev = ch
    s = "".join(out)
    s = re.sub(r"(\d)\s?°C", r"\1 °C", s)
    return s


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
            blocks.append(("h%d" % len(m.group(1)), typographic(m.group(2).strip()), ""))
            i += 1
            continue
        m = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)(?:\|\|(.+))?\s*$", s)
        if m:
            blocks.append(("figure", (m.group(2).strip(),
                                       typographic(m.group(1).strip()),
                                       typographic((m.group(3) or "").strip())), ""))
            i += 1
            continue
        m = re.match(r"^\[\[TABLE:\s*(.*?)\]\]\s*$", s)
        if m:
            blocks.append(("caption", typographic(m.group(1)), ""))
            i += 1
            continue
        if s.strip().startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
                    rows.append([typographic(c) for c in cells])
                i += 1
            blocks.append(("table", rows, ""))
            continue
        if s.strip().startswith("> "):
            blocks.append(("quote", typographic(s.strip()[2:].strip()), ""))
            i += 1
            continue
        if s.strip().startswith("- "):
            blocks.append(("li", typographic(s.strip()[2:].strip()), ""))
            i += 1
            continue
        m = re.match(r"^\d+\.\s+(.*)$", s.strip())
        if m:
            blocks.append(("li", typographic(m.group(1).strip()), ""))
            i += 1
            continue
        # paragraf: gabung baris berurutan
        para = [s.strip()]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(
                r"^(#{1,3}\s|\[\[TABLE:|!\[|\||- |> |\d+\.\s)", lines[i].strip()):
            para.append(lines[i].strip())
            i += 1
        blocks.append(("p", typographic(" ".join(para)), ""))
    return blocks


BACK_MATTER = (
    # EN
    "Checklists and Worksheets", "Glossary", "Analytical Caveats",
    "Notes on Event Sources", "References", "Index", "About the Author",
    # ID
    "Ceklis dan Panduan", "Glosarium", "Catatan Analitis",
    "Catatan Sumber Peristiwa", "Daftar Pustaka", "Indeks", "Tentang Penulis",
)


def render(md_path, out_pdf, lang="en", title=None):
    cfg = L[lang]
    blocks = split_blocks(parse_markdown(md_path))

    # --- istilah indeks: semua butir "li" di bawah lampiran indeks ---
    index_terms, in_index = [], False
    for b in blocks:
        if b[0] == "h1":
            in_index = bool(re.match(r"^(Index|Indeks)$", b[1]))
        elif b[0] == "li" and in_index:
            index_terms.append(b[1].strip())
    index_lookup = {t.lower(): t for t in index_terms}
    index_re = (re.compile(r"\b(" + "|".join(re.escape(t) for t in sorted(index_terms, key=len, reverse=True)) + r")\b", re.I)
                if index_terms else None)

    def build(page_map=None, table_map=None, index_map=None, fig_map=None):
        pdf = Book(lang)
        cright = COPY[lang]
        pdf._idx_letter = None
        if index_map is None:
            index_map = {}
        if fig_map is None:
            fig_map = {}
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
        pdf.set_auto_page_break(False)
        pdf.set_xy(pdf.l_margin, pdf.h - 42)
        pdf.set_font("TNR", "", 9.5)
        pdf.cell(0, 5.5, cright["published"], align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 5.5, cright["edition"], align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.set_auto_page_break(True, 40)

        # ---------- halaman hak cipta ----------
        pdf.add_page()
        draw_copyright(pdf, lang)

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
            elif b[0] == "h2":
                label = b[1]
                toc_entries.append((label, page_map.get(label, 0), 7.0))
        pdf.front = True
        draw_toc(pdf, toc_entries, [(c, table_map.get(c, 0)) for c in
                                    [b[1] for b in blocks if b[0] == "caption"]], lang,
                 [(b[1][1], (fig_map or {}).get(b[1][1], 0))
                  for b in blocks if b[0] == "figure"])
        pdf.front = False

        new_pages, new_tables, new_figs = {}, {}, {}
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
                if pdf.get_y() + 3 * LINE_H > pdf.page_break_trigger:
                    pdf.add_page()
                    pdf.set_y(pdf.t_margin)
                if getattr(pdf, "index_mode", False) and txt.strip().lower() in index_lookup:
                    term = txt.strip()
                    pgx = sorted(index_map.get(term, []))
                    if not pgx:
                        continue
                    letter = term[0].upper()
                    if letter != getattr(pdf, "_idx_letter", None):
                        pdf._idx_letter = letter
                        if pdf.get_y() > pdf.t_margin + 2:
                            pdf.ln(2.5)
                        pdf.set_font("TNR", "B", 11)
                        pdf.cell(0, 5.5, letter, new_x="LMARGIN", new_y="NEXT")
                        pdf.ln(1.0)
                    locs = index_ranges(pgx)
                    tail = ("**" + term + "**")
                    if locs:
                        tail = "**" + term + ",** " + locs
                    also = SEE_ALSO.get(pdf.book_lang, {}).get(term.lower())
                    if also:
                        tail += ". See also " + ", ".join(also) + "." if pdf.book_lang == "en" \
                                else ". Lihat juga " + ", ".join(also) + "."
                    draw_paragraph(pdf, tail, indent=-6.0, left=6.0, align="L",
                                   size=10.5, line_h=4.5)
                    pdf.ln(0.9)
                    continue
                if getattr(pdf, "ref_mode", False):
                    draw_paragraph(pdf, txt, indent=-8.0, left=8.0, align="L", size=10.5, line_h=4.5)
                    pdf.ln(2.6)
                    continue
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
                pdf.ref_mode = bool(re.match(
                    r"^(Notes on Event Sources|Catatan Sumber Peristiwa)$"
                    r"|^(References|Daftar Pustaka)$", title_txt))
                pdf.index_mode = bool(re.match(r"^(Index|Indeks)$", title_txt))
                pdf.chapter_title = title_txt
                pdf.opening = True
                pdf.add_page()
                pdf.chapter_starts.add(pdf.page)
                new_pages[title_txt] = pdf.page
                draw_heading(pdf, title_txt, 1, lang=lang)
                continue
            if kind == "h2":
                new_pages[val] = pdf.page
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
            elif kind == "figure":
                pg = draw_figure(pdf, val[0], val[1], val[2], lang=lang)
                if pg:
                    new_figs[val[1]] = pg
            elif kind == "quote":
                draw_paragraph(pdf, val, indent=0.0, left=8.0, right=8.0)
                pdf.ln(0.6)
            elif kind == "li":
                li_buf.append(val)
                if (index_re is not None and not getattr(pdf, "index_mode", False)
                        and not getattr(pdf, "ref_mode", False)
                        and (pdf.chapter_title or "") not in BACK_MATTER):
                    for m in index_re.finditer(val):
                        key = index_lookup.get(m.group(1).lower())
                        if key:
                            index_map.setdefault(key, set()).add(pdf.page)
            elif re.match(r"^\*(Theme|Tema):", val):
                pdf.set_font("TNR", "I", 10.5)
                pdf.multi_cell(0, 5.2, val.replace("*", ""), align="C")
                pdf.ln(4.0)
            else:
                start_pg = pdf.page
                draw_paragraph(pdf, val)
                if (index_re is not None and not getattr(pdf, "index_mode", False)
                        and not getattr(pdf, "ref_mode", False)
                        and (pdf.chapter_title or "") not in BACK_MATTER):
                    for key in {index_lookup[m.group(1).lower()] for m in index_re.finditer(val)}:
                        if key:
                            for pg_i in range(start_pg, pdf.page + 1):
                                index_map.setdefault(key, set()).add(pg_i)
        flush_li(pdf)
        return pdf, new_pages, new_tables, index_map, new_figs

    pdf, pages, tables, index_map, figs = build()
    # pass berikutnya dengan nomor halaman nyata; ulangi sampai paginasi stabil
    stable = False
    for _ in range(8):
        pdf2, pages2, tables2, index_map, figs2 = build(pages, tables, index_map, figs)
        pdf = pdf2
        if pages2 == pages and tables2 == tables and figs2 == figs:
            stable = True
            break
        pages, tables, figs = pages2, tables2, figs2
    if not stable:
        print("WARNING: pagination not fully stable; last pass used")

    pdf.output(out_pdf)
    return pdf.page, pages, tables
