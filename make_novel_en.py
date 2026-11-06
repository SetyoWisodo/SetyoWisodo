# -*- coding: utf-8 -*-
"""Bangun BEFORE_THE_LIGHT_ARRIVES_EN.pdf — naskah bab 1 + rencana terbit Wattpad/Fizzo."""
import os
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import A5, A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Flowable, Frame, KeepTogether,
                                NextPageTemplate, PageBreak, PageTemplate,
                                Paragraph, Spacer, Table, TableStyle)
from reportlab.platypus.tableofcontents import TableOfContents

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "BEFORE_THE_LIGHT_ARRIVES_EN.pdf")
CH1 = os.path.join(HERE, "novel_en", "chapter_01.md")

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
INK = colors.HexColor("#15181A")
MUTED = colors.HexColor("#6B7280")
TINT = colors.HexColor("#EEF6F8")
RULE = colors.HexColor("#C8D6DB")

A4W, A4H = A4
ML = MR = 21 * mm
MT = 22 * mm
MB = 18 * mm
FRAME_W = A4W - ML - MR


def S(name, **kw):
    base = dict(fontName="Body", fontSize=10.4, leading=15.0, textColor=INK,
                alignment=TA_JUSTIFY, spaceAfter=6)
    base.update(kw)
    return ParagraphStyle(name, **base)


st_lead = S("lead", fontSize=11.4, leading=17.0, spaceAfter=10)
st_p = S("p")
st_h = S("h", fontName="Head-Bd", fontSize=9.6, leading=13, textColor=CYAN,
         alignment=TA_LEFT, spaceBefore=11, spaceAfter=5)
st_bullet = S("bul", leftIndent=11, bulletIndent=1, spaceAfter=4,
              bulletFontName="Head-Bd", bulletFontSize=7.4, bulletColor=CYAN)
st_ol = S("ol", leftIndent=15, bulletIndent=2, spaceAfter=4,
          bulletFontName="Head-Bd", bulletFontSize=8, bulletColor=CYAN)
st_tcell = S("tc", fontSize=8.4, leading=11.4, alignment=TA_LEFT, spaceAfter=0)
st_thead = S("th", fontName="Head-Bd", fontSize=7.5, leading=10.2,
             textColor=colors.white, alignment=TA_LEFT, spaceAfter=0)
st_quote = S("q", fontName="Body-It", fontSize=10.6, leading=15.6, leftIndent=10, spaceAfter=6)

# gaya bacaan (fiksi)
st_fict_title = S("ft", fontName="Head-Bd", fontSize=17, leading=21, textColor=NAVY,
                  alignment=TA_LEFT, spaceAfter=12)
st_fict = S("fx", fontSize=11.2, leading=16.6, alignment=TA_LEFT, spaceAfter=9,
            firstLineIndent=0)
st_fict_first = S("fx1", fontSize=11.2, leading=16.6, alignment=TA_LEFT, spaceAfter=9)
st_fict_mono = S("fm", fontName="Mono", fontSize=8.8, leading=13, alignment=TA_LEFT,
                 spaceAfter=0, textColor=colors.HexColor("#25303A"))


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def rich(text):
    s = esc(text)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", s)
    s = re.sub(r"`([^`]+)`", r'<font name="Mono" size="8.6">\1</font>', s)
    return s


class SectionHead(Flowable):
    def __init__(self, kicker, title, label=None):
        Flowable.__init__(self)
        self.kicker, self.title = kicker, title
        self.label = label or title
        self.width, self.height = FRAME_W, 58

    def wrap(self, aw, ah):
        return (self.width, self.height)

    def draw(self):
        c = self.canv
        c.setFillColor(CYAN)
        c.setFont("Head-Bd", 8.2)
        c.drawString(0, self.height - 8, self.kicker.upper())
        c.setFillColor(NAVY)
        c.setFont("Head-Bd", 18.5)
        c.drawString(0, self.height - 30, self.title)
        c.setStrokeColor(GLOW)
        c.setLineWidth(2)
        c.line(0, 12, 44, 12)
        c.setStrokeColor(RULE)
        c.setLineWidth(0.6)
        c.line(50, 12, self.width, 12)


class Rule(Flowable):
    """Jeda adegan."""
    def __init__(self):
        Flowable.__init__(self)
        self.width, self.height = FRAME_W, 20

    def wrap(self, aw, ah):
        return (self.width, self.height)

    def draw(self):
        c = self.canv
        c.setFillColor(CYAN)
        for i, x in enumerate((-8, 0, 8)):
            c.circle(FRAME_W / 2 + x, 10, 1.4, stroke=0, fill=1)


class Doc(BaseDocTemplate):
    def __init__(self, path, **kw):
        BaseDocTemplate.__init__(self, path, pagesize=A4, leftMargin=ML, rightMargin=MR,
                                 topMargin=MT, bottomMargin=MB,
                                 title="Before the Light Arrives — Chapter One & Publishing Plan",
                                 author="Setyo Wisodo",
                                 subject="English edition: sample chapter, blurbs, Wattpad/Fizzo plan",
                                 creator="make_novel_en.py", **kw)
        self.addPageTemplates([
            PageTemplate(id="cover", frames=[Frame(0, 0, A4W, A4H, 0, 0, 0, 0, id="c")],
                         onPage=draw_cover),
            PageTemplate(id="body", frames=[Frame(ML, MB, FRAME_W, A4H - MT - MB, id="b",
                                                  leftPadding=0, rightPadding=0,
                                                  topPadding=0, bottomPadding=0)],
                         onPage=draw_body),
        ])

    def afterFlowable(self, flowable):
        if isinstance(flowable, SectionHead):
            key = "s%d" % id(flowable)
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(flowable.label, key, level=0)


def draw_cover(canv, doc):
    import random
    canv.saveState()
    canv.setFillColor(NAVY)
    canv.rect(0, 0, A4W, A4H, stroke=0, fill=1)
    random.seed(11)
    for _ in range(230):
        x, y = random.uniform(0, A4W), random.uniform(A4H * 0.34, A4H)
        canv.setFillColor(colors.HexColor("#8FB6C4"))
        canv.circle(x, y, random.choice([0.3, 0.4, 0.5, 0.7]), stroke=0, fill=1)

    canv.setStrokeColor(GLOW)
    canv.setLineWidth(0.9)
    canv.line(ML, A4H * 0.30, A4W - MR, A4H * 0.30)

    canv.setFillColor(GLOW)
    canv.setFont("Head-Bd", 9.2)
    canv.drawString(ML, A4H - 34 * mm, "ENGLISH EDITION  ·  CHAPTER ONE  ·  PUBLISHING PLAN")

    canv.setFillColor(colors.white)
    canv.setFont("Head-Bd", 33)
    canv.drawString(ML, A4H - 54 * mm, "BEFORE")
    canv.drawString(ML, A4H - 68 * mm, "THE LIGHT")
    canv.drawString(ML, A4H - 82 * mm, "ARRIVES")

    canv.setFillColor(colors.HexColor("#9FD3DF"))
    canv.setFont("Body-It", 13)
    canv.drawString(ML, A4H - 95 * mm, "You may send love into the future.")
    canv.drawString(ML, A4H - 101 * mm, "The price is forgetting you ever sent it.")

    canv.setFillColor(colors.HexColor("#7FA6B3"))
    canv.setFont("Head", 8.2)
    canv.drawString(ML, A4H - 110 * mm,
                    "Science fiction  ·  romance  ·  Wattpad & Fizzo edition  ·  6,000 chapters planned")

    y = 76 * mm
    for tag, isi in [("CHAPTER 1", "Full text, 1,540 words — ready to paste"),
                     ("BLURB", "Short, long, tags, content notes"),
                     ("CH 2–10", "Titles and hooks in English"),
                     ("PLATFORM", "Wattpad vs Fizzo: specs and honest math")]:
        canv.setFillColor(GLOW)
        canv.setFont("Head-Bd", 7.8)
        canv.drawString(ML, y, tag)
        canv.setFillColor(colors.HexColor("#DCE9EE"))
        canv.setFont("Body", 9.8)
        canv.drawString(ML + 30 * mm, y, isi)
        y -= 9 * mm

    canv.setFillColor(colors.white)
    canv.setFont("Head-Bd", 11)
    canv.drawString(ML, 38 * mm, "Setyo Wisodo")
    canv.setFillColor(colors.HexColor("#7FA6B3"))
    canv.setFont("Head", 8)
    canv.drawString(ML, 32 * mm, "2026  ·  working document")
    canv.restoreState()


def draw_body(canv, doc):
    canv.saveState()
    canv.setStrokeColor(RULE)
    canv.setLineWidth(0.5)
    canv.line(ML, A4H - MT + 9 * mm, A4W - MR, A4H - MT + 9 * mm)
    canv.setFillColor(MUTED)
    canv.setFont("Head", 7)
    canv.drawString(ML, A4H - MT + 12 * mm, "BEFORE THE LIGHT ARRIVES")
    canv.drawRightString(A4W - MR, A4H - MT + 12 * mm, "Setyo Wisodo · 2026")
    canv.setFillColor(CYAN)
    canv.setFont("Head-Bd", 8)
    canv.drawCentredString(A4W / 2, MB - 10 * mm, "%02d" % doc.page)
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
        for i, it in enumerate(data, 1):
            story.append(Paragraph(rich(it), st_ol, bulletText=str(i)))
        story.append(Spacer(1, 4))
    elif kind == "table":
        widths, head, body = args[0], args[1], args[2]
        rows = [[Paragraph(rich(h), st_thead) for h in head]]
        rows += [[Paragraph(rich(c), st_tcell) for c in r] for r in body]
        t = Table(rows, colWidths=[w * FRAME_W for w in widths], repeatRows=1)
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


# ---------------------------------------------------------------- isi
BLURB = [
    ("h", "Logline"),
    ("p",
     "A relay engineer discovers a scheduled message signed with her own hand — dated forty years "
     "from now — and must decide whether to send it, knowing the price is the memory of the man she "
     "loves."),
    ("h", "Short blurb (Wattpad / Fizzo description, 62 words)"),
    ("p",
     "**Forty grams of memory.** That is what it costs to send a letter that says *I love you* and "
     "means it. Nara Adisurya has never sent one. So when a stolen core turns up carrying a message "
     "signed with her own hand — dated forty years from now — the only question left is who she "
     "loved enough to forget."),
    ("h", "Long blurb (150 words)"),
    ("p",
     "The year is 2183, and the nine systems are stitched together by relays that do not send "
     "messages faster than light. They **schedule** them. Every year you postpone costs you a day "
     "of your strongest memory; every gram of feeling you commit is weighed, stored, and burned. "
     "Only love is heavy enough to cross the dark."),
    ("p",
     "Nara keeps the relays alive on Kemuning, a station at the end of a supply line, where forty "
     "hundred people live on a wire and nobody has paid for anything in a century. Then a buoy "
     "comes in warm. The core has been opened, resealed, and put back for her to find, carrying a "
     "personal packet of exactly forty grams and her own signature on the seal."),
    ("p",
     "To send it, she will have to pay. To refuse, she will have to live with knowing that someone "
     "she cannot remember loved her enough to try."),
    ("h", "Who it is for"),
    ("table", [0.22, 0.78],
     ["Element", "Answer"],
     [["Genre", "Science fiction · romance (slow burn, second chance, memory loss)"],
      ["Heat level", "Closed door in Volume I; one open-door scene from Chapter 90"],
      ["Ending", "HEA — earned over 6,000 chapters"],
      ["Content notes", "grief, parental abandonment, memory loss, one non-graphic death of a parent, institutional coercion"],
      ["Reads like", "*The Seven Deaths of Evelyn Hardcastle* meets *Normal People*, in orbit"],
      ["Tags (Wattpad/Fizzo)", "science fiction, romance, sci-fi romance, slow burn, memory, time travel, space, dystopian, mystery, second chance"]]),
    ("note", "Why the blurb stops where it stops",
     "It names the price (forty grams), the impossibility (her own signature), and the question "
     "(who did she love enough to forget). It never explains the relay. Explanations belong in "
     "chapter one, after the reader has already decided to stay."),
]

CH_LATER = [
    ("lead",
     "Ten chapter titles and hooks in English, matched to the Indonesian plan but rewritten so they "
     "read naturally to a Wattpad reader. Each hook is the final line of the chapter."),
    ("table", [0.08, 0.28, 0.64],
     ["Ch.", "Title", "Hook"],
     [["1", "Buoy in Winter", "\"Oh,\" he said quietly, and it was not a word for a stranger. \"You're still here.\""],
      ["2", "Ash Protocol", "\"Log it,\" Vey said. \"Log it and forget it.\" I logged it. I did not forget."],
      ["3", "The Quarterly Ship", "He named a street on the moon where I grew up. He had never been there."],
      ["4", "Net Zero", "Four thousand one hundred messages left Kemuning. Zero payments. All of them addressed to one person."],
      ["5", "Two Ways to Read a File", "He knew my case number without opening the folder."],
      ["6", "The Taste at My Fingertips", "The grief was not a stranger's grief. It was my mother's."],
      ["7", "A Message That Does Not Exist Yet", "Post date: forty years from now. The handwriting was mine."],
      ["8", "The Charge", "I realized I could not remember the last three years clearly."],
      ["9", "Someone Who Has Been Here Before", "\"I came here once,\" he said. \"Three years ago. Under a different name.\""],
      ["10", "Nine Days", "There are nine days missing from my seventh year — and the file was signed by my father."]]),
]

PLATFORM = [
    ("lead",
     "The two platforms want different things, and the difference decides how long a chapter should "
     "be. Neither wants the 3,000-word chapters planned for print."),
    ("table", [0.22, 0.39, 0.39],
     ["", "Wattpad", "Fizzo"],
     [["Chapter length", "**1,500–2,500 words** is the platform sweet spot; above 4,000 shows higher mobile drop-off", "**Minimum 1,000 words** per chapter to count; daily update requires 1,000+ words published that day"],
      ["Paragraphs", "never longer than a phone screen — 4–6 sentences maximum", "same; mobile-first layout"],
      ["Cadence that ranks", "1–2 updates per week; long books stay ranked longer", "daily updates unlock the daily bonus; up to 4 days off per month"],
      ["Discovery", "tag search + algorithm by read velocity", "editorial ranking + paid promotion inside the app"],
      ["Money", "Paid Stories, invitation only", "contract with fixed fee + word-count bonus (**read the contract carefully**)"],
      ["What kills you", "inconsistent updates", "missing the daily word minimum"]]),
    ("note", "The contract warning, stated plainly",
     "Fizzo is owned by ByteDance and has been publicly criticised for one-sided contracts: writers "
     "have reported being asked to publish at least 1,000 words a day to earn a daily bonus, with "
     "fixed royalties in the low hundreds of dollars and long exclusivity terms. Writer Beware "
     "covered this in detail. **Read every clause before signing, especially the term length, "
     "exclusivity, and who owns the rights after the contract ends.**"),
    ("h", "The honest math for 6,000 chapters"),
    ("table", [0.34, 0.24, 0.42],
     ["Plan", "Total words", "Time at 1 chapter/day"],
     [["6,000 × 1,200", "7.2 million", "16.4 years"],
      ["6,000 × 1,500", "9.0 million", "16.4 years"],
      ["6,000 × 1,800", "10.8 million", "16.4 years"],
      ["6,000 × 2,000", "12 million", "16.4 years"]]),
    ("p",
     "Chapter length does not change the time; **chapter count does**. At one chapter a day, 6,000 "
     "chapters is sixteen years. At three a day, it is five and a half — still longer than most "
     "writers stay on one project."),
    ("h", "What I recommend instead"),
    ("ol", [
        "**Write 1,500-word chapters, not 3,000.** The story loses nothing; the mobile reader gains everything. Total falls to about 9 million words.",
        "**Publish Volume I (100 chapters) as a complete arc before deciding anything else.** That is 150,000 words — a real book, and enough to know whether readers stay.",
        "**Keep the 6,000-chapter map as the world, not as a promise.** Promise 100 chapters. Deliver 100 chapters. Then promise the next 100.",
        "**Do not sign an exclusivity contract until Volume I has readers.** A contract signed at chapter 12 binds a story you have not yet learned to write."]),
]

LAUNCH = [
    ("lead",
     "Thirty days. The first ten chapters decide whether chapters eleven to six thousand have any "
     "readers at all."),
    ("table", [0.10, 0.44, 0.46],
     ["Day", "Action", "Why"],
     [["−14", "Write chapters 1–10 (15,000 words) before publishing anything", "you cannot build momentum on one chapter"],
      ["−7", "Prepare 20 chapters of buffer", "the first month is when you will be slowest"],
      ["1", "Publish chapters 1–3 at once", "Wattpad readers check if a story has enough to read before starting"],
      ["3", "Publish 4–5; add the story to 20 tags", "tags are the only free discovery you get"],
      ["7", "Publish 6–7; post one quote card on social", "quote cards travel further than links"],
      ["14", "Publish 8–10; ask three readers what confused them", "chapter 10 is the decision point"],
      ["21", "Hold a steady 2/week cadence", "ranking rewards consistency more than volume"],
      ["30", "Read the retention numbers: where did readers stop?", "fix that chapter, not chapter one"]]),
    ("h", "Five rules that keep 6,000 chapters readable"),
    ("ol", [
        "**One question answered per 100 chapters, two planted.** Answer two and readers leave; answer zero and they feel cheated.",
        "**Every chapter ends on a line that opens something.** Never close.",
        "**Every twist carries three planted clues.** If a reader cannot find them on a re-read, it was not a twist — it was a trick.",
        "**No new rule of the world without a price paid on the page.** The relay is only frightening because it always charges.",
        "**Write the bible before the chapter.** If a fact exists only in your head, it does not exist."]),
    ("note", "What is already done, and what is next",
     "Done: the world (six eras, sixty volumes), the causal chain, twelve twists with planted clues, "
     "twenty real scientific discoveries as the rules of the world, chapter titles for 1–100, and "
     "chapter one in English. Next: chapters two to ten, using the hooks on page twelve."),
]

BODY = [
    ("STORY", "The story in one page", BLURB),
    ("CHAPTER ONE", "Buoy in Winter", None),
    ("CHAPTERS 2–10", "Titles and hooks", CH_LATER),
    ("PLATFORM", "Wattpad vs Fizzo", PLATFORM),
    ("LAUNCH", "Thirty days", LAUNCH),
]


def baca_bab(path):
    raw = open(path, encoding="utf-8").read()
    judul = raw.split("\n", 1)[0].lstrip("# ").strip()
    isi = raw.split("\n", 1)[1]
    return judul, isi


def render_bab(story, path):
    judul, isi = baca_bab(path)
    # judul sudah tampil di kepala bagian; jangan diulang
    paragraf = [p.strip() for p in isi.split("\n\n")]
    blok_mono = []
    for p in paragraf:
        if not p:
            continue
        if p.startswith("*Next:"):
            story.append(Spacer(1, 6))
            story.append(Paragraph(rich(p.strip("*")), ParagraphStyle(
                "nx", fontName="Body-It", fontSize=9.4, textColor=MUTED, spaceAfter=0)))
            continue
        if p.strip() == "---":
            story.append(Rule())
            continue
        # blok keluaran konsol: baris yang semuanya pendek dan berawalan kapital + ":"
        baris = p.split("\n")
        if len(baris) > 2 and all(re.match(r"^[A-Z][A-Za-z ]+:", b) for b in baris):
            blok_mono = [Paragraph(esc(b).replace(" ", "&nbsp;"), st_fict_mono) for b in baris]
            t = Table([[blok_mono]], colWidths=[FRAME_W * 0.62])
            t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F3F6F7")),
                                   ("LINEBEFORE", (0, 0), (0, -1), 2, CYAN),
                                   ("LEFTPADDING", (0, 0), (-1, -1), 8),
                                   ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                                   ("TOPPADDING", (0, 0), (-1, -1), 6),
                                   ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
            story.append(t)
            story.append(Spacer(1, 9))
            continue
        story.append(Paragraph(rich(p), st_fict))


def build(path):
    doc = Doc(path)
    story = [NextPageTemplate("body"), PageBreak()]
    n = 0
    for kicker, judul, isi in BODY:
        n += 1
        story.append(SectionHead("%02d · %s" % (n, kicker), judul,
                                 label="%02d · %s" % (n, judul)))
        story.append(Spacer(1, 8))
        if isi is None:
            render_bab(story, CH1)
        else:
            tambah(story, isi)
        story.append(PageBreak())
    doc.multiBuild(story)
    return doc.page


if __name__ == "__main__":
    n = build("/tmp/_en_pass1.pdf")
    print("pass 1:", n)
    n = build(OUT)
    print("pass 2:", n, "halaman ->", OUT)
    print("ukuran: %.2f MB" % (os.path.getsize(OUT) / 1048576))
