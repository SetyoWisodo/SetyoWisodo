# -*- coding: utf-8 -*-
"""Bangun PETA_SEBELUM_CAHAYA_SAMPAI.pdf — peta novel 750.000 kata."""
import os
import re
import sys

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Flowable, Frame, KeepTogether,
                                NextPageTemplate, PageBreak, PageTemplate,
                                Paragraph, Spacer, Table, TableStyle)
from reportlab.platypus.tableofcontents import TableOfContents

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
MODUL = sys.argv[1] if len(sys.argv) > 1 else "peta_content"
_slug = MODUL.replace("-", "_")
import importlib  # noqa: E402
P = importlib.import_module("peta_novel." + _slug)

OUT = os.path.join(HERE, getattr(P, "OUTPUT", "PETA_SEBELUM_CAHAYA_SAMPAI.pdf"))

F = os.path.join(HERE, "fonts")
for n, f in (("Body", "Tinos-Regular.ttf"), ("Body-It", "Tinos-Italic.ttf"),
             ("Body-Bd", "Tinos-Bold.ttf"), ("Body-BdIt", "Tinos-BoldItalic.ttf")):
    pdfmetrics.registerFont(TTFont(n, os.path.join(F, f)))
pdfmetrics.registerFontFamily("Body", normal="Body", bold="Body-Bd",
                              italic="Body-It", boldItalic="Body-BdIt")
pdfmetrics.registerFont(TTFont("Head", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("Head-Bd", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Mono", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"))
pdfmetrics.registerFontFamily("Head", normal="Head", bold="Head-Bd")

NAVY = colors.HexColor("#0B1B2B")
CYAN = colors.HexColor("#0E7490")
GLOW = colors.HexColor("#22D3EE")
INK = colors.HexColor("#161A1D")
MUTED = colors.HexColor("#6B7280")
TINT = colors.HexColor("#EEF6F8")
CODEBG = colors.HexColor("#F1F4F2")
RULE = colors.HexColor("#C8D6DB")

PAGE_W, PAGE_H = A4
ML = MR = 21 * mm
MT = 23 * mm
MB = 19 * mm
FRAME_W = PAGE_W - ML - MR


def S(name, **kw):
    base = dict(fontName="Body", fontSize=10.4, leading=15.0, textColor=INK,
                alignment=TA_JUSTIFY, spaceAfter=6)
    base.update(kw)
    return ParagraphStyle(name, **base)


st_lead = S("lead", fontSize=11.4, leading=17.2, textColor=colors.HexColor("#232B30"), spaceAfter=10)
st_p = S("p")
st_h = S("h", fontName="Head-Bd", fontSize=9.6, leading=13, textColor=CYAN,
         alignment=TA_LEFT, spaceBefore=11, spaceAfter=5)
st_bullet = S("bul", leftIndent=11, bulletIndent=1, spaceAfter=4,
              bulletFontName="Head-Bd", bulletFontSize=7.4, bulletColor=CYAN)
st_code = S("code", fontName="Mono", fontSize=7.6, leading=11.2,
            textColor=colors.HexColor("#1F262A"), alignment=TA_LEFT, spaceAfter=0)
st_tcell = S("tc", fontSize=8.4, leading=11.4, alignment=TA_LEFT, spaceAfter=0)
st_thead = S("th", fontName="Head-Bd", fontSize=7.5, leading=10.2,
             textColor=colors.white, alignment=TA_LEFT, spaceAfter=0)
st_quote = S("q", fontName="Body-It", fontSize=10.6, leading=15.6, leftIndent=10, spaceAfter=6)


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def rich(text):
    parts, out = [], []
    for i, chunk in enumerate(re.split(r"`([^`]+)`", text)):
        if i % 2:
            parts.append(("code", chunk))
        else:
            parts.append(("text", chunk))
    for kind, chunk in parts:
        if kind == "code":
            out.append('<font name="Mono" size="8.5">%s</font>' % esc(chunk))
            continue
        s = esc(chunk)
        s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
        s = re.sub(r"(?<![\w_])_(.+?)_(?![\w_])", r"<i>\1</i>", s)
        out.append(s)
    return "".join(out)


class SectionHead(Flowable):
    def __init__(self, kicker, title, toc_level=0, label=None):
        Flowable.__init__(self)
        self.kicker, self.title = kicker, title
        self.toc_level = toc_level
        self.label = label or title
        self.width, self.height = FRAME_W, 62

    def wrap(self, aw, ah):
        return (self.width, self.height)

    def draw(self):
        c = self.canv
        c.setFillColor(CYAN)
        c.setFont("Head-Bd", 8.2)
        c.drawString(0, self.height - 10, self.kicker.upper())
        c.setFillColor(NAVY)
        c.setFont("Head-Bd", 19.5)
        c.drawString(0, self.height - 33, self.title)
        c.setStrokeColor(GLOW)
        c.setLineWidth(2)
        c.line(0, 13, 46, 13)
        c.setStrokeColor(RULE)
        c.setLineWidth(0.6)
        c.line(52, 13, self.width, 13)


class Doc(BaseDocTemplate):
    def __init__(self, path, **kw):
        BaseDocTemplate.__init__(self, path, pagesize=A4, leftMargin=ML, rightMargin=MR,
                                 topMargin=MT, bottomMargin=MB,
                                 title=getattr(P, "META_TITLE", "Sebelum Cahaya Sampai — peta novel"),
                                 author="Setyo Wisodo",
                                 subject="Fiksi ilmiah + romance, 10 volume, 300 bab",
                                 creator="make_peta.py", **kw)
        self.addPageTemplates([
            PageTemplate(id="cover", frames=[Frame(0, 0, PAGE_W, PAGE_H, 0, 0, 0, 0, id="c")],
                         onPage=draw_cover),
            PageTemplate(id="body", frames=[Frame(ML, MB, FRAME_W, PAGE_H - MT - MB, id="b",
                                                  leftPadding=0, rightPadding=0,
                                                  topPadding=0, bottomPadding=0)],
                         onPage=draw_body),
        ])

    def afterFlowable(self, flowable):
        if isinstance(flowable, SectionHead):
            key = "s%d" % id(flowable)
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(flowable.label, key, level=flowable.toc_level)
            self.notify("TOCEntry", (flowable.toc_level, flowable.label, self.page, key))


def draw_cover(canv, doc):
    canv.saveState()
    canv.setFillColor(NAVY)
    canv.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)

    # bintang halus
    import random
    random.seed(7)
    for _ in range(210):
        x, y = random.uniform(0, PAGE_W), random.uniform(PAGE_H * 0.36, PAGE_H)
        r = random.choice([0.3, 0.4, 0.5, 0.7])
        canv.setFillColor(colors.HexColor("#8FB6C4"))
        canv.circle(x, y, r, stroke=0, fill=1)

    # garis cakrawala
    canv.setStrokeColor(GLOW)
    canv.setLineWidth(0.9)
    canv.line(ML, PAGE_H * 0.335, PAGE_W - MR, PAGE_H * 0.335)

    canv.setFillColor(GLOW)
    canv.setFont("Head-Bd", 9.4)
    canv.drawString(ML, PAGE_H - 34 * mm, getattr(P, "COVER_KICKER", ""))

    judul = getattr(P, "JUDUL", ["SEBELUM", "CAHAYA", "SAMPAI"])
    canv.setFillColor(colors.white)
    canv.setFont("Head-Bd", 34 if len(judul) > 2 else 30)
    y0 = PAGE_H - 52 * mm
    for i, baris in enumerate(judul):
        canv.drawString(ML, y0 - i * 14 * mm, baris)

    tagline = getattr(P, "TAGLINE", [])
    canv.setFillColor(colors.HexColor("#9FD3DF"))
    canv.setFont("Body-It", 13.2)
    for i, baris in enumerate(tagline):
        canv.drawString(ML, PAGE_H - 92 * mm - i * 6 * mm, baris)

    canv.setFillColor(colors.HexColor("#7FA6B3"))
    canv.setFont("Head", 8.4)
    canv.drawString(ML, PAGE_H - 108 * mm, getattr(P, "COVER_SUB", ""))

    y = 96 * mm
    for tag, isi in getattr(P, "COVER_TAGS", []):
        canv.setFillColor(GLOW)
        canv.setFont("Head-Bd", 8.0)
        canv.drawString(ML, y, tag)
        canv.setFillColor(colors.HexColor("#DCE9EE"))
        canv.setFont("Body", 9.8)
        canv.drawString(ML + 26 * mm, y, isi)
        y -= 9 * mm

    canv.setFillColor(colors.white)
    canv.setFont("Head-Bd", 11)
    canv.drawString(ML, 40 * mm, "Setyo Wisodo")
    canv.setFillColor(colors.HexColor("#7FA6B3"))
    canv.setFont("Head", 8.2)
    canv.drawString(ML, 34 * mm, "2026  ·  dokumen kerja, bukan kutipan novel")
    canv.restoreState()


def draw_body(canv, doc):
    canv.saveState()
    canv.setStrokeColor(RULE)
    canv.setLineWidth(0.5)
    canv.line(ML, PAGE_H - MT + 9 * mm, PAGE_W - MR, PAGE_H - MT + 9 * mm)
    canv.setFillColor(MUTED)
    canv.setFont("Head", 7.2)
    canv.drawString(ML, PAGE_H - MT + 12 * mm, "SEBELUM CAHAYA SAMPAI — PETA NOVEL")
    canv.drawRightString(PAGE_W - MR, PAGE_H - MT + 12 * mm, "Setyo Wisodo · 2026")
    canv.setFillColor(CYAN)
    canv.setFont("Head-Bd", 8)
    canv.drawCentredString(PAGE_W / 2, MB - 11 * mm, "%02d" % doc.page)
    canv.restoreState()


def blok(item, story):
    kind, args = item[0], list(item[1:])
    data = args[0] if len(args) == 1 else args
    if kind == "lead":
        story.append(Paragraph(rich(data), st_lead))
    elif kind == "p":
        story.append(Paragraph(rich(data), st_p))
    elif kind == "h":
        story.append(Paragraph(rich(data), st_h))
    elif kind == "ul":
        for it in data:
            story.append(Paragraph(rich(it), st_bullet, bulletText="\u2022"))
        story.append(Spacer(1, 4))
    elif kind == "ol":
        st_ol = ParagraphStyle("ol", parent=st_bullet, leftIndent=15, bulletIndent=2,
                               spaceAfter=5, bulletFontSize=8.0)
        for i, it in enumerate(data, 1):
            story.append(Paragraph(rich(it), st_ol, bulletText=str(i)))
        story.append(Spacer(1, 4))
    elif kind == "table":
        widths, head, body = args[0], args[1], args[2]
        cw = [w * FRAME_W for w in widths]
        rows = [[Paragraph(rich(h), st_thead) for h in head]]
        rows += [[Paragraph(rich(c), st_tcell) for c in r] for r in body]
        t = Table(rows, colWidths=cw, repeatRows=1)
        style = [("BACKGROUND", (0, 0), (-1, 0), NAVY),
                 ("VALIGN", (0, 0), (-1, -1), "TOP"),
                 ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                 ("TOPPADDING", (0, 0), (-1, -1), 3.4), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.4),
                 ("LINEBELOW", (0, 0), (-1, -1), 0.4, RULE), ("BOX", (0, 0), (-1, -1), 0.5, RULE)]
        for r in range(1, len(rows)):
            if r % 2 == 0:
                style.append(("BACKGROUND", (0, r), (-1, r), TINT))
        t.setStyle(TableStyle(style))
        story.append(t)
        story.append(Spacer(1, 9))
    elif kind == "code":
        body = [Paragraph(esc(l).replace(" ", "&nbsp;") if l.strip() else "&nbsp;", st_code)
                for l in data.split("\n")]
        t = Table([[body]], colWidths=[FRAME_W])
        t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), CODEBG),
                               ("LINEBEFORE", (0, 0), (0, -1), 2.2, CYAN),
                               ("LEFTPADDING", (0, 0), (-1, -1), 7),
                               ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                               ("TOPPADDING", (0, 0), (-1, -1), 6),
                               ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
        story.append(t)
        story.append(Spacer(1, 9))
    elif kind == "note":
        title, text = args[0], args[1]
        inner = [Paragraph('<font name="Head-Bd" size="7.7" color="#0E7490">%s</font>'
                           % esc(title.upper()), ParagraphStyle("nt", leading=10, spaceAfter=3)),
                 Paragraph(rich(text), ParagraphStyle("nb", fontName="Body", fontSize=9.4,
                                                      leading=13.6, alignment=TA_JUSTIFY))]
        t = Table([[inner]], colWidths=[FRAME_W])
        t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), TINT),
                               ("LINEBEFORE", (0, 0), (0, -1), 2.2, NAVY),
                               ("LEFTPADDING", (0, 0), (-1, -1), 8),
                               ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                               ("TOPPADDING", (0, 0), (-1, -1), 7),
                               ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]))
        story.append(Spacer(1, 3))
        story.append(KeepTogether(t))
        story.append(Spacer(1, 9))
    elif kind == "quote":
        story.append(Paragraph(rich(data), st_quote))


def tambah(story, blocks):
    for b in blocks:
        blok(b, story)


BAGIAN = P.BAGIAN


def build(path):
    doc = Doc(path)
    story = [NextPageTemplate("body"), PageBreak()]

    story.append(Paragraph(rich("Sebelum satu kata ditulis"), ParagraphStyle(
        "t", fontName="Head-Bd", fontSize=19.5, leading=23, textColor=NAVY, spaceAfter=10)))
    tambah(story, P.FRONT)
    story.append(Spacer(1, 6))
    story.append(Paragraph("Daftar isi", ParagraphStyle(
        "t2", fontName="Head-Bd", fontSize=19.5, leading=23, textColor=NAVY, spaceAfter=2)))
    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle("t0", fontName="Head-Bd", fontSize=12.5, leading=18,
                       textColor=NAVY, spaceBefore=13, spaceAfter=2),
        ParagraphStyle("t1", fontName="Body", fontSize=10.3, leading=16.5,
                       leftIndent=16, textColor=INK),
    ]
    story.append(toc)
    story.append(PageBreak())

    for kicker, judul, sub, isi in BAGIAN:
        story.append(SectionHead(kicker, judul, label="%s · %s" % (kicker, judul)))
        story.append(Paragraph(rich(sub), ParagraphStyle(
            "sub", fontName="Body-It", fontSize=10.4, leading=14, textColor=MUTED, spaceAfter=6)))
        story.append(Spacer(1, 4))
        tambah(story, isi)
        story.append(PageBreak())

    story.append(SectionHead("11", "Mengapa cerita ini bekerja", label="11 · Mengapa cerita ini bekerja"))
    tambah(story, P.LANGKAH)
    doc.multiBuild(story)
    return doc.page


if __name__ == "__main__":
    n = build("/tmp/_peta_pass1.pdf")
    print("pass 1:", n)
    n = build(OUT)
    print("pass 2:", n, "halaman ->", OUT)
    print("ukuran: %.2f MB" % (os.path.getsize(OUT) / 1048576))
