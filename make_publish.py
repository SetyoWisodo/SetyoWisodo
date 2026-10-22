# -*- coding: utf-8 -*-
"""Bangun EPUB 3 dan DOCX dari book.md / book_id.md.

Renderer PDF tidak menghasilkan format yang dibutuhkan penerbit untuk
deadline naskah (EPUB untuk pembaca digital, DOCX untuk penyuntingan).
Skrip ini memakai blok yang sama dengan renderer PDF sehingga isinya identik.

Pemakaian: python make_publish.py
"""
import html
import os
import re

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Mm, Pt

import book_pdf

BOOKS = [
    {
        "md": "book.md",
        "img": "book/publish/Surviving_the_Future_EN_cover_front.jpg",
        "epub": "book/publish/Surviving_the_Future_EN.epub",
        "docx": "book/publish/Surviving_the_Future_EN.docx",
        "title": "Surviving the Future: Crisis, Climate, and Human Resilience",
        "lang": "en",
        "author": "Setyo Wisodo",
        "uid": "urn:uuid:sf-en-2026",
    },
    {
        "md": "book_id.md",
        "img": "book/publish/Bertahan_Hidup_di_Masa_Depan_ID_cover_front.jpg",
        "epub": "book/publish/Bertahan_Hidup_di_Masa_Depan_ID.epub",
        "docx": "book/publish/Bertahan_Hidup_di_Masa_Depan_ID.docx",
        "title": "Surviving the Future: Krisis, Iklim, dan Ketahanan Manusia",
        "lang": "id",
        "author": "Setyo Wisodo",
        "uid": "urn:uuid:sf-id-2026",
    },
]


def inline_html(text):
    """**tebal** -> <strong>, *miring* -> <em>, sisanya di-escape."""
    out, pos = [], 0
    for m in re.finditer(r"\*\*(.+?)\*\*|\*(.+?)\*", text):
        out.append(html.escape(text[pos:m.start()]))
        if m.group(1) is not None:
            out.append("<strong>%s</strong>" % html.escape(m.group(1)))
        else:
            out.append("<em>%s</em>" % html.escape(m.group(2)))
        pos = m.end()
    out.append(html.escape(text[pos:]))
    return "".join(out)


def blocks_of(md_path):
    return book_pdf.split_blocks(book_pdf.parse_markdown(md_path))


def split_chapters(blocks):
    """Kembalikan [(judul, [blok])]; blok sebelum h1 pertama masuk judul None."""
    chapters, cur_title, cur = [], None, []
    for kind, val, _ in blocks:
        if kind == "h1":
            if cur:
                chapters.append((cur_title, cur))
            cur_title, cur = val, [(kind, val)]
        else:
            cur.append((kind, val))
    if cur:
        chapters.append((cur_title, cur))
    return chapters


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:48] or "s"


def chapter_xhtml(title, blocks, is_first):
    parts = []
    first_h1 = True
    if title:
        parts.append("<h1>%s</h1>" % inline_html(title))
    for kind, val in blocks:
        if kind == "h1":
            continue    # judul bab sudah ditulis di atas
        elif kind == "h2":
            parts.append('<h2 id="%s">%s</h2>' % (slug(val), inline_html(val)))
        elif kind == "h3":
            parts.append("<h3>%s</h3>" % inline_html(val))
        elif kind == "table":
            if not val:
                continue
            head, body = val[0], val[1:]
            rows = ["<tr>%s</tr>" % "".join("<th>%s</th>" % inline_html(c) for c in head)]
            for r in body:
                rows.append("<tr>%s</tr>" % "".join("<td>%s</td>" % inline_html(c) for c in r))
            parts.append("<table>%s</table>" % "".join(rows))
        elif kind == "caption":
            parts.append('<p class="caption">%s</p>' % inline_html(val))
        elif kind == "quote":
            parts.append("<blockquote><p>%s</p></blockquote>" % inline_html(val))
        elif kind == "li":
            parts.append("<p class=\"li\">\u2022 %s</p>" % inline_html(val))
        else:
            if re.match(r"^\*(Theme|Tema):", val):
                parts.append('<p class="theme">%s</p>' % inline_html(val.strip("*")))
            else:
                parts.append("<p>%s</p>" % inline_html(val))
    body = "\n".join(parts)
    return ('<?xml version="1.0" encoding="utf-8"?>\n'
            '<html xmlns="http://www.w3.org/1999/xhtml"><head><title>%s</title>'
            '<link rel="stylesheet" href="style.css" type="text/css"/></head>'
            '<body>%s</body></html>' % (html.escape(title or ""), body))


CSS = """
body { font-family: "Times New Roman", serif; font-size: 1em; line-height: 1.45; margin: 0 4%; }
h1 { font-size: 1.35em; text-align: center; margin: 1.6em 0 0.4em 0; }
h2 { font-size: 1.12em; margin: 1.4em 0 0.35em 0; }
h3 { font-size: 1em; font-style: italic; margin: 1.1em 0 0.3em 0; }
p { text-align: justify; text-indent: 1.27em; margin: 0 0 0.35em 0; }
p.caption { text-align: center; font-weight: bold; text-indent: 0; margin-top: 1em; }
p.theme { font-style: italic; text-indent: 0; margin: 0.2em 0 0.9em 0; }
p.li { text-indent: 0; margin-left: 1.4em; text-align: left; }
blockquote { margin: 0.8em 1.6em; font-size: 0.96em; }
body.cover { margin: 0; padding: 0; text-align: center; }
body.cover img { max-width: 100%; height: auto; }
blockquote p { text-indent: 0; }
table { border-collapse: collapse; width: 100%; margin: 0.6em 0 1em 0; font-size: 0.78em; }
th, td { border: 1px solid #444; padding: 2px 4px; text-align: left; vertical-align: top; }
th { background: #eee; }
"""


def build_epub(cfg):
    """Tulis EPUB 3 langsung (zip): kendali penuh, tanpa ketergantungan quirks."""
    import uuid
    import zipfile

    blocks = blocks_of(cfg["md"])
    chapters = split_chapters(blocks)
    uid = "urn:uuid:" + str(uuid.uuid5(uuid.NAMESPACE_URL, cfg["uid"]))
    files = []          # (nama, bytes)
    manifest = []
    spine = []
    nav_items = []

    def add(name, data, mtype=None, item_id=None, in_spine=False):
        files.append((name, data if isinstance(data, bytes) else data.encode("utf-8")))
        manifest.append((item_id or name.replace(".", "-").replace("/", "-"), name, mtype))
        if in_spine:
            spine.append(item_id or name.replace(".", "-").replace("/", "-"))

    add("style.css", CSS, "text/css", "style")

    has_cover = os.path.exists(cfg["img"])
    if has_cover:
        with open(cfg["img"], "rb") as fh:
            add("cover.jpg", fh.read(), "image/jpeg", "cover-img")
        cover_html = ('<?xml version="1.0" encoding="utf-8"?>\n'
                      '<html xmlns="http://www.w3.org/1999/xhtml" '
                      'xmlns:epub="http://www.idpf.org/2007/ops"><head><title>Cover</title>'
                      '<link rel="stylesheet" href="style.css" type="text/css"/></head>'
                      '<body class="cover"><div><img src="cover.jpg" alt="%s"/></div></body></html>'
                      % html.escape(cfg["title"]))
        add("cover.xhtml", cover_html, "application/xhtml+xml", "cover", in_spine=True)

    for i, (title, blks) in enumerate(chapters):
        name = "c%03d.xhtml" % i
        add(name, chapter_xhtml(title, blks, i == 0), "application/xhtml+xml",
            "c%03d" % i, in_spine=True)
        subs = [(slug(v), v) for kk, v in blks if kk == "h2"]
        nav_items.append((title or cfg["title"], name, subs))

    # ---- nav.xhtml ----
    nl = ['<?xml version="1.0" encoding="utf-8"?>',
          '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">',
          '<head><title>Contents</title><link rel="stylesheet" href="style.css" type="text/css"/></head>',
          '<body><nav epub:type="toc" id="toc"><h1>Contents</h1><ol>']
    for title, name, subs in nav_items:
        nl.append('<li><a href="%s">%s</a>' % (name, html.escape(title)))
        if subs:
            nl.append("<ol>")
            for hid, label in subs:
                nl.append('<li><a href="%s#%s">%s</a></li>' % (name, hid, html.escape(label)))
            nl.append("</ol>")
        nl.append("</li>")
    nl.append("</ol></nav></body></html>")
    nav_xhtml = "\n".join(nl)
    add("nav.xhtml", nav_xhtml, "application/xhtml+xml", "nav", in_spine=True)

    # ---- content.opf ----
    opf = ['<?xml version="1.0" encoding="utf-8"?>',
           '<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid" '
           'xml:lang="%s">' % cfg["lang"],
           '<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">',
           '<dc:identifier id="bookid">%s</dc:identifier>' % uid,
           '<dc:title>%s</dc:title>' % html.escape(cfg["title"]),
           '<dc:creator>%s</dc:creator>' % html.escape(cfg["author"]),
           '<dc:language>%s</dc:language>' % cfg["lang"],
           '<dc:publisher>Setyo Wisodo</dc:publisher>',
           '<dc:date>2026</dc:date>',
           '<meta property="dcterms:modified">2026-10-22T00:00:00Z</meta>']
    if has_cover:
        opf.append('<meta name="cover" content="cover-img"/>')
    opf.append("</metadata><manifest>")
    opf.append('<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>')
    for item_id, name, mtype in manifest:
        opf.append('<item id="%s" href="%s" media-type="%s"/>' % (item_id, name, mtype))
    opf.append("</manifest><spine toc=\"ncx\">")
    for item_id in spine:
        opf.append('<itemref idref="%s"/>' % item_id)
    opf.append("</spine></package>")
    add("content.opf", "\n".join(opf), "application/oebps-package+xml", "opf")

    # ---- toc.ncx (kompatibilitas pembaca lama) ----
    nc = ['<?xml version="1.0" encoding="utf-8"?>',
          '<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">',
          '<head><meta name="dtb:uid" content="%s"/></head>' % uid,
          '<docTitle><text>%s</text></docTitle>' % html.escape(cfg["title"]),
          "<navMap>"]
    for n, (title, name, subs) in enumerate(nav_items, 1):
        nc.append('<navPoint id="n%d" playOrder="%d"><navLabel><text>%s</text></navLabel>'
                  '<content src="%s"/>' % (n, n, html.escape(title), name))
        for hid, label in subs:
            nc.append('<navPoint id="n%d-%s" playOrder="%d"><navLabel><text>%s</text></navLabel>'
                      '<content src="%s#%s"/></navPoint>'
                      % (n, hid, n, html.escape(label), name, hid))
        nc.append("</navPoint>")
    nc.append("</navMap></ncx>")
    add("toc.ncx", "\n".join(nc), "application/x-dtbncx+xml", "ncx")

    container = ('<?xml version="1.0" encoding="utf-8"?>\n'
                 '<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
                 '<rootfiles><rootfile full-path="OEBPS/content.opf" '
                 'media-type="application/oebps-package+xml"/></rootfiles></container>')

    with zipfile.ZipFile(cfg["epub"], "w") as z:
        z.writestr(zipfile.ZipInfo("mimetype"), "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml", container, compress_type=zipfile.ZIP_DEFLATED)
        for name, data in files:
            z.writestr("OEBPS/" + name, data, compress_type=zipfile.ZIP_DEFLATED)
    return len(chapters)


def build_docx(cfg):
    doc = Document()
    style = doc.styles["Normal"]
    style.font.name = "Times New Roman"
    style.font.size = Pt(12)
    pf = style.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf.first_line_indent = Mm(12.7)
    pf.space_after = Pt(0)
    pf.line_spacing = 1.15

    for kind, val in [(k, v) for k, v, _ in blocks_of(cfg["md"])]:
        if kind == "h1":
            doc.add_page_break()
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.first_line_indent = Mm(0)
            r = p.add_run(val.upper())
            r.bold = True
            r.font.name = "Times New Roman"
            r.font.size = Pt(12)
        elif kind == "h2":
            p = doc.add_paragraph()
            p.paragraph_format.first_line_indent = Mm(0)
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.bold = True
            r.font.size = Pt(12)
        elif kind == "h3":
            p = doc.add_paragraph()
            p.paragraph_format.first_line_indent = Mm(0)
            r = p.add_run(val)
            r.italic = True
            r.bold = True
        elif kind == "table":
            if not val:
                continue
            ncol = max(len(r) for r in val)
            t = doc.add_table(rows=0, cols=ncol)
            t.style = "Table Grid"
            for row in val:
                cells = t.add_row().cells
                for i, c in enumerate(row[:ncol]):
                    cells[i].text = c
                    for par in cells[i].paragraphs:
                        par.paragraph_format.first_line_indent = Mm(0)
                        for run in par.runs:
                            run.font.size = Pt(10)
                            run.font.name = "Times New Roman"
        elif kind == "caption":
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.first_line_indent = Mm(0)
            r = p.add_run(val)
            r.bold = True
        elif kind == "quote":
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Mm(12.7)
            p.paragraph_format.first_line_indent = Mm(0)
            p.add_run(val).italic = True
        elif kind == "li":
            p = doc.add_paragraph()
            p.paragraph_format.first_line_indent = Mm(0)
            p.paragraph_format.left_indent = Mm(8)
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            add_runs(p, "\u2022 " + val)
        else:
            p = doc.add_paragraph()
            add_runs(p, val)
    doc.save(cfg["docx"])


def add_runs(par, text):
    """Tambahkan teks dengan **tebal** dan *miring* sebagai run terpisah."""
    pos = 0
    for m in re.finditer(r"\*\*(.+?)\*\*|\*(.+?)\*", text):
        if m.start() > pos:
            par.add_run(text[pos:m.start()])
        if m.group(1) is not None:
            r = par.add_run(m.group(1))
            r.bold = True
        else:
            r = par.add_run(m.group(2))
            r.italic = True
        pos = m.end()
    if pos < len(text):
        par.add_run(text[pos:])


def main():
    for cfg in BOOKS:
        n = build_epub(cfg)
        build_docx(cfg)
        print("%s: %d bab -> %s, %s" % (cfg["lang"], n, cfg["epub"], cfg["docx"]))


if __name__ == "__main__":
    main()
