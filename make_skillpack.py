# -*- coding: utf-8 -*-
"""Bangun SKILL_PACK_NOVEL_ROMANCE.pdf dari skillpack_content*.py."""
import os
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Flowable, Frame, KeepTogether,
                                NextPageTemplate, PageBreak, PageTemplate,
                                Paragraph, Spacer, Table, TableStyle)
from reportlab.platypus.tableofcontents import TableOfContents

import skillpack_content as C1
import skillpack_content2 as C2

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "SKILL_NOVEL_ROMANCE.pdf")

# ---------------------------------------------------------------- fonta
F = os.path.join(HERE, "fonts")
pdfmetrics.registerFont(TTFont("Body", os.path.join(F, "Tinos-Regular.ttf")))
pdfmetrics.registerFont(TTFont("Body-It", os.path.join(F, "Tinos-Italic.ttf")))
pdfmetrics.registerFont(TTFont("Body-Bd", os.path.join(F, "Tinos-Bold.ttf")))
pdfmetrics.registerFont(TTFont("Body-BdIt", os.path.join(F, "Tinos-BoldItalic.ttf")))
pdfmetrics.registerFontFamily("Body", normal="Body", bold="Body-Bd",
                              italic="Body-It", boldItalic="Body-BdIt")
os.path.exists(os.path.join(F, "Tinos-Bold.ttf"))

pdfmetrics.registerFont(TTFont("Head", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("Head-Bd", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Mono", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"))
pdfmetrics.registerFontFamily("Head", normal="Head", bold="Head-Bd")

# ---------------------------------------------------------------- warna
PLUM = colors.HexColor("#5A1B34")
ROSE = colors.HexColor("#A8436B")
INK = colors.HexColor("#1C1C1C")
MUTED = colors.HexColor("#6E6E73")
TINT = colors.HexColor("#F7F1F3")
CODEBG = colors.HexColor("#F2F2EF")
RULE = colors.HexColor("#D9C9CF")

PAGE_W, PAGE_H = A4
ML = MR = 21 * mm
MT = 23 * mm
MB = 19 * mm
FRAME_W = PAGE_W - ML - MR

TITLE = "SKILL PACK"
SUBTITLE = "Metode kerja 457 halaman, disusun ulang untuk novel romance"

# ---------------------------------------------------------------- gaya
def S(name, **kw):
    base = dict(fontName="Body", fontSize=10.4, leading=15.0, textColor=INK,
                alignment=TA_JUSTIFY, spaceAfter=6)
    base.update(kw)
    return ParagraphStyle(name, **base)


st_lead = S("lead", fontSize=11.4, leading=17.2, textColor=colors.HexColor("#2B2B2B"),
            spaceAfter=10)
st_p = S("p")
st_h = S("h", fontName="Head-Bd", fontSize=9.6, leading=13, textColor=PLUM,
         alignment=TA_LEFT, spaceBefore=11, spaceAfter=5)
st_bullet = S("bul", leftIndent=11, bulletIndent=1, spaceAfter=4,
              bulletFontName="Head-Bd", bulletFontSize=7.4, bulletColor=ROSE)
st_code = S("code", fontName="Mono", fontSize=7.7, leading=11.4,
            textColor=colors.HexColor("#22221F"), alignment=TA_LEFT, spaceAfter=0)
st_tcell = S("tc", fontSize=8.5, leading=11.6, alignment=TA_LEFT, spaceAfter=0)
st_thead = S("th", fontName="Head-Bd", fontSize=7.6, leading=10.4,
             textColor=colors.white, alignment=TA_LEFT, spaceAfter=0)
st_cap = S("cap", fontSize=7.8, leading=10, textColor=MUTED, alignment=TA_LEFT,
           spaceBefore=2, spaceAfter=10)
st_quote = S("q", fontName="Body-It", fontSize=10.4, leading=15.4, leftIndent=10,
             spaceAfter=6)
st_skillnum = S("sn", fontName="Head-Bd", fontSize=8.4, leading=10, textColor=ROSE,
                alignment=TA_LEFT, spaceAfter=3)
st_skilltitle = S("st", fontName="Head-Bd", fontSize=19.5, leading=23, textColor=PLUM,
                  alignment=TA_LEFT, spaceAfter=10)
st_partnum = S("pn", fontName="Head-Bd", fontSize=9, leading=12, textColor=ROSE,
               alignment=TA_LEFT, spaceAfter=4)
st_parttitle = S("pt", fontName="Head-Bd", fontSize=24, leading=28, textColor=PLUM,
                 alignment=TA_LEFT, spaceAfter=14)

ARROW = '<font name="Head">\u2192</font>'
BOX = '<font name="Head">\u25a1</font>'


def esc(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def rich(text):
    """**tebal**  _miring_  `kode`  ->  markup reportlab."""
    parts, out = [], []
    for i, chunk in enumerate(re.split(r"`([^`]+)`", text)):
        if i % 2:
            parts.append(("code", chunk))
        else:
            parts.append(("text", chunk))
    for kind, chunk in parts:
        if kind == "code":
            out.append('<font name="Mono" size="8.6">%s</font>' % esc(chunk))
            continue
        s = esc(chunk)
        s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
        s = re.sub(r"(?<![\w_])_(.+?)_(?![\w_])", r"<i>\1</i>", s)
        out.append(s)
    return "".join(out)


def bullet_para(text, marker="\u2022"):
    return Paragraph(rich(text), st_bullet, bulletText=marker)


# ---------------------------------------------------------------- flowable kustom
class HRule(Flowable):
    def __init__(self, width=FRAME_W, thickness=0.7, color=RULE, space=6):
        Flowable.__init__(self)
        self.width, self.thickness, self.color, self.space = width, thickness, color, space

    def wrap(self, aw, ah):
        return (self.width, self.thickness + self.space)

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, self.space, self.width, self.space)


class SectionHead(Flowable):
    """Judul skill dengan garis aksen dan entri TOC."""

    def __init__(self, kicker, title, toc_level=1, key=None, label=None):
        Flowable.__init__(self)
        self.kicker, self.title = kicker, title
        self.toc_level, self.key = toc_level, key or title
        nomor = kicker.split()[-1].lstrip("0") or kicker.split()[-1]
        self.label = label or ("%s · %s" % (nomor, title))
        self.width = FRAME_W
        self.height = 66

    def wrap(self, aw, ah):
        return (self.width, self.height)

    def draw(self):
        c = self.canv
        c.setFillColor(ROSE)
        c.setFont("Head-Bd", 8.2)
        c.drawString(0, self.height - 10, self.kicker.upper())
        c.setFillColor(PLUM)
        c.setFont("Head-Bd", 20)
        c.drawString(0, self.height - 34, self.title)
        c.setStrokeColor(ROSE)
        c.setLineWidth(2)
        c.line(0, 14, 46, 14)
        c.setStrokeColor(RULE)
        c.setLineWidth(0.6)
        c.line(52, 14, self.width, 14)

    def toc(self):
        return (self.toc_level, self.label, 0)


# ---------------------------------------------------------------- dokumen
class Doc(BaseDocTemplate):
    def __init__(self, path, **kw):
        BaseDocTemplate.__init__(self, path, pagesize=A4,
                                 leftMargin=ML, rightMargin=MR,
                                 topMargin=MT, bottomMargin=MB,
                                 title="Skill Pack — Novel Romance",
                                 author="Setyo Wisodo",
                                 subject="Metode kerja buku 457 halaman, diterjemahkan untuk novel romance",
                                 creator="make_skillpack.py", **kw)
        frame_cover = Frame(0, 0, PAGE_W, PAGE_H, 0, 0, 0, 0, id="cover")
        frame_body = Frame(ML, MB, FRAME_W, PAGE_H - MT - MB, id="body",
                           leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates([
            PageTemplate(id="cover", frames=[frame_cover], onPage=draw_cover),
            PageTemplate(id="body", frames=[frame_body], onPage=draw_body),
        ])

    def afterFlowable(self, flowable):
        if isinstance(flowable, SectionHead):
            level, text, _ = flowable.toc()
            key = "sec%d" % id(flowable)
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(text, key, level=level, closed=(level > 0))
            self.notify("TOCEntry", (level, text, self.page, key))
        elif isinstance(flowable, PartDivider):
            key = "part%d" % id(flowable)
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(flowable.title, key, level=0)
            self.notify("TOCEntry", (0, flowable.title, self.page, key))


class PartDivider(Flowable):
    def __init__(self, number, title, blurb):
        Flowable.__init__(self)
        self.number, self.title, self.blurb = number, title, blurb
        self.width, self.height = FRAME_W, 132

    def wrap(self, aw, ah):
        return (self.width, self.height)

    def draw(self):
        c = self.canv
        c.setFillColor(ROSE)
        c.rect(0, self.height - 3, 46, 3, stroke=0, fill=1)
        c.setFillColor(ROSE)
        c.setFont("Head-Bd", 9)
        c.drawString(0, self.height - 34, self.number.upper())
        c.setFillColor(PLUM)
        c.setFont("Head-Bd", 26)
        c.drawString(0, self.height - 68, self.title)
        c.setFillColor(colors.HexColor("#3A3A3A"))
        c.setFont("Body-It", 11)
        c.drawString(0, self.height - 96, self.blurb)


TOTAL_PAGES = [0]


def draw_cover(canv, doc):
    canv.saveState()
    # panel atas
    canv.setFillColor(PLUM)
    canv.rect(0, PAGE_H - 118 * mm, PAGE_W, 118 * mm, stroke=0, fill=1)
    canv.setFillColor(ROSE)
    canv.rect(0, PAGE_H - 121 * mm, PAGE_W, 3 * mm, stroke=0, fill=1)

    canv.setFillColor(colors.HexColor("#E9C9D4"))
    canv.setFont("Head-Bd", 9.6)
    canv.drawString(ML, PAGE_H - 30 * mm, "SKILL PACK  ·  13 SKILL  ·  6 PROMPT")

    canv.setFillColor(colors.white)
    canv.setFont("Head-Bd", 52)
    canv.drawString(ML, PAGE_H - 58 * mm, TITLE)

    canv.setFillColor(colors.HexColor("#F3DCE4"))
    canv.setFont("Body-It", 15.5)
    canv.drawString(ML, PAGE_H - 72 * mm, "Metode kerja 457 halaman,")
    canv.drawString(ML, PAGE_H - 79 * mm, "disusun ulang untuk novel romance")

    canv.setStrokeColor(colors.HexColor("#8F5470"))
    canv.setLineWidth(0.8)
    canv.line(ML, PAGE_H - 89 * mm, PAGE_W - MR, PAGE_H - 89 * mm)

    canv.setFillColor(colors.HexColor("#E9C9D4"))
    canv.setFont("Head", 8.6)
    canv.drawString(ML, PAGE_H - 96 * mm,
                    "Diekstrak dari proyek Surviving the Future: Crisis, Climate, and Human Resilience")

    # blok bawah
    y = 96 * mm
    baris = [
        ("01–06", "Arsitektur · Riset · Suara · Audit otomatis · Bible · Tata letak"),
        ("07–09", "Produksi berkas · Sampul · Sampel & stempel pembeli"),
        ("10–13", "Harga · Halaman jual · Peluncuran · Kontrol mutu"),
        ("A–B", "Struktur folder & perintah · Enam prompt siap tempel"),
    ]
    for tag, isi in baris:
        canv.setFillColor(ROSE)
        canv.setFont("Head-Bd", 8.2)
        canv.drawString(ML, y, tag)
        canv.setFillColor(colors.HexColor("#2B2B2B"))
        canv.setFont("Body", 10.2)
        canv.drawString(ML + 24 * mm, y, isi)
        y -= 9.5 * mm

    canv.setFillColor(PLUM)
    canv.setFont("Head-Bd", 11.5)
    canv.drawString(ML, 40 * mm, "Setyo Wisodo")
    canv.setFillColor(MUTED)
    canv.setFont("Head", 8.4)
    canv.drawString(ML, 34 * mm, "2026  ·  Dokumen kerja, bukan kutipan buku")
    canv.restoreState()


def draw_body(canv, doc):
    canv.saveState()
    canv.setStrokeColor(RULE)
    canv.setLineWidth(0.5)
    canv.line(ML, PAGE_H - MT + 9 * mm, PAGE_W - MR, PAGE_H - MT + 9 * mm)
    canv.setFillColor(MUTED)
    canv.setFont("Head", 7.2)
    canv.drawString(ML, PAGE_H - MT + 12 * mm, "SKILL PACK — NOVEL ROMANCE")
    canv.drawRightString(PAGE_W - MR, PAGE_H - MT + 12 * mm, "Setyo Wisodo · 2026")

    n = doc.page
    canv.setFillColor(ROSE if n % 2 else MUTED)
    canv.setFont("Head-Bd", 8)
    canv.drawCentredString(PAGE_W / 2, MB - 11 * mm, "%02d" % n)
    canv.restoreState()


# ---------------------------------------------------------------- render blok
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
            story.append(bullet_para(it))
        story.append(Spacer(1, 4))
    elif kind == "ol":
        st_ol = ParagraphStyle("ol", parent=st_bullet, leftIndent=15, bulletIndent=2,
                               spaceAfter=5, bulletFontSize=8.0)
        for i, it in enumerate(data, 1):
            story.append(Paragraph(rich(it), st_ol, bulletText=str(i)))
        story.append(Spacer(1, 4))
    elif kind == "check":
        rows = [[Paragraph(BOX, ParagraphStyle("bx", fontName="Head", fontSize=8.6,
                                               leading=11.5)),
                 Paragraph(rich(it), st_tcell)] for it in data]
        t = Table(rows, colWidths=[7 * mm, FRAME_W - 7 * mm])
        t.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (0, -1), 2),
            ("TOPPADDING", (0, 0), (-1, -1), 2.2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2),
            ("TEXTCOLOR", (0, 0), (0, -1), ROSE),
        ]))
        story.append(t)
        story.append(Spacer(1, 8))
    elif kind == "table":
        widths, head, body = args[0], args[1], args[2]
        cw = [w * FRAME_W for w in widths]
        rows = [[Paragraph(rich(h), st_thead) for h in head]]
        rows += [[Paragraph(rich(c), st_tcell) for c in r] for r in body]
        t = Table(rows, colWidths=cw, repeatRows=1)
        style = [
            ("BACKGROUND", (0, 0), (-1, 0), PLUM),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ("TOPPADDING", (0, 0), (-1, -1), 3.6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3.6),
            ("LINEBELOW", (0, 0), (-1, -1), 0.4, RULE),
            ("BOX", (0, 0), (-1, -1), 0.5, RULE),
        ]
        for r in range(1, len(rows)):
            if r % 2 == 0:
                style.append(("BACKGROUND", (0, r), (-1, r), TINT))
        t.setStyle(TableStyle(style))
        story.append(t)
        story.append(Spacer(1, 9))
    elif kind == "code":
        txt = data
        body = []
        for line in txt.split("\n"):
            body.append(Paragraph(esc(line).replace(" ", "&nbsp;") if line.strip() else "&nbsp;",
                                   st_code))
        t = Table([[body]], colWidths=[FRAME_W])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), CODEBG),
            ("LINEBEFORE", (0, 0), (0, -1), 2.2, ROSE),
            ("LEFTPADDING", (0, 0), (-1, -1), 7),
            ("RIGHTPADDING", (0, 0), (-1, -1), 7),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        story.append(t)
        story.append(Spacer(1, 9))
    elif kind == "note":
        title, text = args[0], args[1]
        inner = [Paragraph('<font name="Head-Bd" size="7.8" color="#A8436B">%s</font>'
                           % esc(title.upper()), ParagraphStyle("nt", leading=10, spaceAfter=3)),
                 Paragraph(rich(text), ParagraphStyle("nb", fontName="Body", fontSize=9.4,
                                                      leading=13.6, alignment=TA_JUSTIFY))]
        t = Table([[inner]], colWidths=[FRAME_W])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), TINT),
            ("LINEBEFORE", (0, 0), (0, -1), 2.2, PLUM),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ]))
        story.append(Spacer(1, 3))
        story.append(KeepTogether(t))
        story.append(Spacer(1, 9))
    elif kind == "quote":
        story.append(Paragraph(rich(data), st_quote))


def tambah_isi(story, blocks):
    for b in blocks:
        blok(b, story)


SKILLS = [
    ("SKILL 01", "Arsitektur 24 bab", C1.SKILL_01),
    ("SKILL 02", "Riset yang bisa diperiksa", C1.SKILL_02),
    ("SKILL 03", "Suara, adegan, dialog", C1.SKILL_03),
    ("SKILL 04", "Mesin audit otomatis", C1.SKILL_04),
    ("SKILL 05", "Bible & konsistensi", C1.SKILL_05),
    ("SKILL 06", "Tata letak & tipografi", C1.SKILL_06),
    ("SKILL 07", "Produksi berkas", C2.SKILL_07),
    ("SKILL 08", "Sampul & gambar jual", C2.SKILL_08),
    ("SKILL 09", "Sampel & stempel", C2.SKILL_09),
    ("SKILL 10", "Harga & paket", C2.SKILL_10),
    ("SKILL 11", "Halaman jual", C2.SKILL_11),
    ("SKILL 12", "Peluncuran", C2.SKILL_12),
    ("SKILL 13", "Kontrol mutu akhir", C2.SKILL_13),
]


def daftar_isi(story):
    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle("t0", fontName="Head-Bd", fontSize=12.5, leading=18,
                       textColor=PLUM, spaceBefore=13, spaceAfter=2),
        ParagraphStyle("t1", fontName="Body", fontSize=10.3, leading=16.5,
                       leftIndent=16, textColor=INK),
    ]
    toc.dotsMinLevel = 0
    story.append(toc)


def build(path, total=None):
    doc = Doc(path)
    story = []
    story.append(NextPageTemplate("body"))
    story.append(PageBreak())

    # --- halaman pembuka
    story.append(Paragraph(rich("Cara memakai berkas ini"), st_skilltitle))
    tambah_isi(story, C1.FRONT)
    story.append(Spacer(1, 6))
    story.append(Paragraph("Daftar isi", st_skilltitle))
    story.append(Spacer(1, 2))
    daftar_isi(story)
    story.append(PageBreak())

    # --- bagian I
    story.append(Spacer(1, 14))
    story.append(PartDivider("Bagian I", "Lima prinsip",
                             "Yang membuat tiga belas skill di bawah bisa selesai."))
    story.append(Spacer(1, 2))
    tambah_isi(story, C1.PRINSIP)
    story.append(PageBreak())

    # --- skill
    for kicker, title, blocks in SKILLS:
        story.append(SectionHead(kicker, title))
        story.append(Spacer(1, 8))
        tambah_isi(story, blocks)
        story.append(PageBreak())

    # --- lampiran
    story.append(SectionHead("LAMPIRAN A", "Struktur folder & perintah",
                             toc_level=0, key="lamp-A", label="Lampiran A · Struktur folder & perintah"))
    story.append(Spacer(1, 8))
    tambah_isi(story, C2.LAMPIRAN_A)
    story.append(PageBreak())

    story.append(SectionHead("LAMPIRAN B", "Enam prompt siap tempel",
                             toc_level=0, key="lamp-B", label="Lampiran B · Enam prompt siap tempel"))
    story.append(Spacer(1, 8))
    tambah_isi(story, C2.LAMPIRAN_B)

    doc.multiBuild(story)
    return doc.page


if __name__ == "__main__":
    n = build("/tmp/_skillpack_pass1.pdf")
    print("pass 1:", n, "halaman")
    n2 = build(OUT)
    print("pass 2:", n2, "halaman ->", OUT)
    print("ukuran: %.2f MB" % (os.path.getsize(OUT) / 1048576))
