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
import shutil

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Mm, Pt, RGBColor

import book_pdf
from pypdf import PdfReader
import figures as figmod

BOOKS = [
    {
        "md": "book.md",
        "pdf": "Surviving_the_Future.pdf",
        "interior": "book/publish/Surviving_the_Future_EN_interior.pdf",
        "img": "book/publish/Surviving_the_Future_EN_cover_ebook.jpg",
        "epub": "book/publish/Surviving_the_Future_EN.epub",
        "docx": "book/publish/Surviving_the_Future_EN.docx",
        "title": "Surviving the Future: Crisis, Climate, and Human Resilience",
        "lang": "en",
        "author": "Setyo Wisodo",
        "publisher": "Setyo Wisodo",
        "rights": "Copyright \u00a9 2026 Setyo Wisodo. All rights reserved.",
        "subjects": ["SCIENCE / Global Warming & Climate Change",
                     "NATURE / Natural Disasters",
                     "SOCIAL SCIENCE / Disasters & Disaster Relief"],
        "description": "How societies survive the crises caused by global warming: 24 chapters, 25 data tables, 11 data figures, 24 case studies, and the evidence behind each prediction.",
        "a11y": "Reflowable text with a two-level table of contents and structural navigation; tables are marked up with column headers and every data figure carries alternative text. No audio or video, no flashing content.",
        "uid": "urn:uuid:sf-en-2026",
    },
    {
        "md": "book_id.md",
        "pdf": "Surviving_the_Future_ID.pdf",
        "interior": "book/publish/Bertahan_Hidup_di_Masa_Depan_ID_interior.pdf",
        "img": "book/publish/Bertahan_Hidup_di_Masa_Depan_ID_cover_ebook.jpg",
        "epub": "book/publish/Bertahan_Hidup_di_Masa_Depan_ID.epub",
        "docx": "book/publish/Bertahan_Hidup_di_Masa_Depan_ID.docx",
        "title": "Surviving the Future: Krisis, Iklim, dan Ketahanan Manusia",
        "lang": "id",
        "author": "Setyo Wisodo",
        "publisher": "Setyo Wisodo",
        "rights": "Hak cipta \u00a9 2026 Setyo Wisodo. Seluruh hak dilindungi.",
        "subjects": ["SCIENCE / Global Warming & Climate Change",
                     "NATURE / Natural Disasters",
                     "SOCIAL SCIENCE / Disasters & Disaster Relief"],
        "description": "Bagaimana masyarakat bertahan dari krisis akibat pemanasan global: 24 bab, 25 tabel data, 11 gambar data, 24 studi kasus, dan bukti di balik setiap prediksi.",
        "a11y": "Teks reflowable dengan daftar isi dua tingkat dan navigasi struktural; tabel ditandai dengan kepala kolom dan setiap gambar data memiliki teks alternatif. Tanpa audio atau video, tanpa konten berkedip.",
        "uid": "urn:uuid:sf-id-2026",
    },
]


def split_caption(caption):
    """'Figure 2.1 Teks' -> ('Figure 2.1', 'Teks')."""
    m = re.match(r"^(Figure|Gambar)\s+([0-9]+\.[0-9]+)\s*(.*)$", caption.strip())
    if not m:
        return "", caption
    return m.group(1) + " " + m.group(2), m.group(3)


def figure_alt(caption, lang):
    """Teks alternatif untuk pembaca layar, diambil dari figures.py."""
    for f in figmod.FIGURES:
        if caption == figmod.caption(f, lang):
            return f["alt_" + lang]
    return caption


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
    for kind, val, extra in blocks:
        if kind == "h1":
            if cur:
                chapters.append((cur_title, cur))
            cur_title, cur = val, [(kind, val, extra)]
        else:
            cur.append((kind, val, extra))
    if cur:
        chapters.append((cur_title, cur))
    return chapters


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:48] or "s"


_LANG = "en"        # diisi build_epub()


def chapter_xhtml(title, blocks, is_first):
    parts = []
    first_h1 = True
    if title:
        parts.append("<h1>%s</h1>" % inline_html(title))
    for b in blocks:
        kind, val = b[0], b[1]
        extra = b[2] if len(b) > 2 else ""
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
            rows = ["<tr>%s</tr>" % "".join('<th scope="col">%s</th>' % inline_html(c) for c in head)]
            for r in body:
                rows.append("<tr>%s</tr>" % "".join("<td>%s</td>" % inline_html(c) for c in r))
            parts.append("<table>%s</table>" % "".join(rows))
        elif kind == "caption":
            parts.append('<p class="caption">%s</p>' % inline_html(val))
            if extra:
                parts.append('<p class="tablesource">%s</p>' % inline_html(extra))
        elif kind == "figure":
            path, caption, source = val
            alt = figure_alt(caption, _LANG)
            src_html = ('<br/><span class="figsrc">%s</span>' % inline_html(source)
                        if source else "")
            flabel, ftext = split_caption(caption)
            parts.append('<figure class="fig"><img src="%s" alt="%s"/>'
                         '<figcaption><span class="figlabel">%s</span> %s%s</figcaption></figure>'
                         % (html.escape(path), html.escape(alt),
                            html.escape(flabel), inline_html(ftext), src_html))
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
            '<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="%s" lang="%s">'
            '<head><title>%s</title>'
            '<link rel="stylesheet" href="style.css" type="text/css"/></head>'
            '<body>%s</body></html>' % (_LANG, _LANG, html.escape(title or ""), body))


CSS = """
body { font-family: "Times New Roman", serif; font-size: 1em; line-height: 1.45; margin: 0 4%; }
h1 { font-size: 1.35em; text-align: center; margin: 1.6em 0 0.4em 0; }
h2 { font-size: 1.12em; margin: 1.4em 0 0.35em 0; }
h3 { font-size: 1em; font-style: italic; margin: 1.1em 0 0.3em 0; }
p { text-align: justify; text-indent: 1.27em; margin: 0 0 0.35em 0; }
p.caption { text-align: center; font-weight: bold; text-indent: 0; margin-top: 1em; }
p.tablesource { font-style: italic; font-size: 0.85em; color: #444; text-indent: 0; margin: 0.2em 0 0.4em 0; }
figure.fig { margin: 1.2em 0 1.4em 0; text-align: center; page-break-inside: avoid; }
figure.fig img { max-width: 100%; height: auto; }
figure.fig figcaption { font-size: 0.9em; margin-top: 0.5em; text-indent: 0; }
span.figlabel { font-weight: bold; }
span.figsrc { color: #555; font-size: 0.92em; }
p.theme { font-style: italic; text-indent: 0; margin: 0.2em 0 0.9em 0; }
p.li { text-indent: 0; margin-left: 1.4em; text-align: left; }
blockquote { margin: 0.8em 1.6em; font-size: 0.96em; }
body.cover { margin: 0; padding: 0; text-align: center; }
body.cover img { max-width: 100%; height: auto; }
body.titlepage { text-align: center; margin-top: 22%; }
h1.booktitle { font-size: 2em; letter-spacing: 0.04em; margin: 0 0 0.6em 0; }
p.subtitle { font-size: 1.15em; text-indent: 0; text-align: center; margin: 0 0 3em 0; }
p.author { font-size: 1.15em; text-indent: 0; text-align: center; margin: 0 0 5em 0; }
p.imprint { text-indent: 0; text-align: center; font-size: 0.9em; }
body.copyright { margin-top: 30%; }
body.copyright p { text-indent: 0; text-align: left; font-size: 0.86em; margin: 0 0 0.7em 0; }
table { border-collapse: collapse; width: 100%; margin: 0.8em 0; font-size: 0.86em; }
th, td { border: 1px solid #999; padding: 0.25em 0.35em; text-align: left; vertical-align: top; }
th { font-weight: bold; }
blockquote p { text-indent: 0; }
table { border-collapse: collapse; width: 100%; margin: 0.6em 0 1em 0; font-size: 0.78em; }
th, td { border: 1px solid #444; padding: 2px 4px; text-align: left; vertical-align: top; }
th { background: #eee; }
"""


def build_epub(cfg):
    """Tulis EPUB 3 langsung (zip): kendali penuh, tanpa ketergantungan quirks."""
    import uuid
    import zipfile

    global _LANG
    _LANG = cfg["lang"]

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

    # ---- gambar data: berkas PNG ikut masuk ke dalam EPUB ----
    seen_fig = set()
    for _title, blks in chapters:
        for kind, val in [(b[0], b[1]) for b in blks]:
            if kind != "figure":
                continue
            rel = val[0].replace("\\", "/")
            if rel in seen_fig:
                continue
            seen_fig.add(rel)
            full = rel if os.path.isabs(rel) else os.path.join(book_pdf.BOOK_DIR, rel)
            if not os.path.exists(full):
                print("PERINGATAN: gambar hilang:", full)
                continue
            with open(full, "rb") as fh:
                add(rel, fh.read(), "image/png",
                    "fig-" + os.path.basename(rel).replace(".png", "").replace("_", "-"))
    print("epub figures:", len(seen_fig))

    has_cover = os.path.exists(cfg["img"])
    if has_cover:
        with open(cfg["img"], "rb") as fh:
            add("cover.jpg", fh.read(), "image/jpeg", "cover-img")
        cover_html = ('<?xml version="1.0" encoding="utf-8"?>\n'
                      '<html xmlns="http://www.w3.org/1999/xhtml" '
                      'xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="%s" lang="%s">'
                      '<head><title>Cover</title>'
                      '<link rel="stylesheet" href="style.css" type="text/css"/></head>'
                      '<body class="cover" epub:type="cover"><div><img src="cover.jpg" alt="%s"/></div>'
                      '</body></html>'
                      % (cfg["lang"], cfg["lang"], html.escape(cfg["title"])))
        add("cover.xhtml", cover_html, "application/xhtml+xml", "cover", in_spine=True)

    copy = book_pdf.COPY[cfg["lang"]]
    title_html = ('<?xml version="1.0" encoding="utf-8"?>\n'
                  '<html xmlns="http://www.w3.org/1999/xhtml" '
                  'xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="%s" lang="%s">'
                  '<head><title>%s</title><link rel="stylesheet" href="style.css" type="text/css"/></head>'
                  '<body class="titlepage"><section epub:type="titlepage">'
                  '<h1 class="booktitle">%s</h1><p class="subtitle">%s</p>'
                  '<p class="author">%s</p><p class="imprint">%s<br/>2026</p>'
                  '</section></body></html>'
                  % (cfg["lang"], cfg["lang"], html.escape(cfg["title"]),
                     html.escape(copy["title"]), html.escape(copy["sub"]),
                     html.escape(copy["author"]), html.escape(copy["published"])))
    add("titlepage.xhtml", title_html, "application/xhtml+xml", "titlepage", in_spine=True)

    copyright_html = ('<?xml version="1.0" encoding="utf-8"?>\n'
                      '<html xmlns="http://www.w3.org/1999/xhtml" '
                      'xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="%s" lang="%s">'
                      '<head><title>%s</title><link rel="stylesheet" href="style.css" type="text/css"/></head>'
                      '<body class="copyright"><section epub:type="copyright-page">'
                      '<p><strong>%s</strong><br/>%s<br/>%s</p>'
                      '<p>%s</p><p>%s</p><p>%s</p><p>%s</p><p>%s</p><p>%s</p>'
                      '</section></body></html>'
                      % (cfg["lang"], cfg["lang"], html.escape(copy["title"]),
                         html.escape(copy["title"]), html.escape(copy["sub"]),
                         html.escape(copy["author"]), html.escape(copy["edition"]),
                         html.escape(copy["published"]), html.escape(copy["rights"]),
                         html.escape(copy["legal"]), html.escape(copy["disclaimer"]),
                         html.escape(copy["credits"])))
    add("copyright.xhtml", copyright_html, "application/xhtml+xml", "copyright", in_spine=True)

    for i, (title, blks) in enumerate(chapters):
        name = "c%03d.xhtml" % i
        add(name, chapter_xhtml(title, blks, i == 0), "application/xhtml+xml",
            "c%03d" % i, in_spine=True)
        subs = [(slug(b[1]), b[1]) for b in blks if b[0] == "h2"]
        nav_items.append((title or cfg["title"], name, subs))

    # ---- nav.xhtml ----
    nl = ['<?xml version="1.0" encoding="utf-8"?>',
          '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops"'
          ' xml:lang="%s" lang="%s">' % (cfg["lang"], cfg["lang"]),
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
    nl.append("</ol></nav>")
    nl.append('<nav epub:type="landmarks" id="landmarks" hidden="hidden"><h2>Landmarks</h2><ol>')
    nl.append('<li><a epub:type="cover" href="cover.xhtml">Cover</a></li>')
    nl.append('<li><a epub:type="toc" href="nav.xhtml">Contents</a></li>')
    nl.append('<li><a epub:type="bodymatter" href="c000.xhtml">%s</a></li>'
              % ("Start" if cfg["lang"] == "en" else "Mulai"))
    nl.append("</ol></nav></body></html>")
    nav_xhtml = "\n".join(nl)
    add("nav.xhtml", nav_xhtml, "application/xhtml+xml", "nav", in_spine=True)
    # daftar isi dibaca setelah halaman hak cipta, bukan di akhir buku
    if "nav" in spine:
        spine.remove("nav")
        spine.insert(min(3, len(spine)), "nav")

    # ---- content.opf ----
    opf = ['<?xml version="1.0" encoding="utf-8"?>',
           '<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid" '
           'xml:lang="%s">' % cfg["lang"],
           '<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">',
           '<dc:identifier id="bookid">%s</dc:identifier>' % uid,
           '<dc:title>%s</dc:title>' % html.escape(cfg["title"]),
           '<dc:creator>%s</dc:creator>' % html.escape(cfg["author"]),
           '<dc:language>%s</dc:language>' % cfg["lang"],
           '<dc:publisher>%s</dc:publisher>' % html.escape(cfg["publisher"]),
           '<dc:date>2026-01-01</dc:date>',
           '<dc:rights>%s</dc:rights>' % html.escape(cfg["rights"]),
           '<dc:description>%s</dc:description>' % html.escape(cfg["description"]),
           '<dc:subject>%s</dc:subject>' % html.escape(cfg["subjects"][0]),
           '<dc:subject>%s</dc:subject>' % html.escape(cfg["subjects"][1]),
           '<dc:subject>%s</dc:subject>' % html.escape(cfg["subjects"][2]),
           '<meta property="dcterms:modified">2026-10-22T00:00:00Z</meta>',
           '<meta property="schema:accessMode">textual</meta>',
           '<meta property="schema:accessModeSufficient">textual</meta>',
           '<meta property="schema:accessibilityFeature">structuralNavigation</meta>',
           '<meta property="schema:accessibilityFeature">tableOfContents</meta>',
           '<meta property="schema:accessibilityHazard">none</meta>',
           '<meta property="schema:accessibilitySummary">%s</meta>'
           % html.escape(cfg["a11y"])]
    if has_cover:
        opf.append('<meta name="cover" content="cover-img"/>')
    opf.append("</metadata><manifest>")
    opf.append('<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>')
    PROPS = {"nav": "nav", "cover-img": "cover-image"}
    for item_id, name, mtype in manifest:
        extra = (' properties="%s"' % PROPS[item_id]) if item_id in PROPS else ""
        opf.append('<item id="%s" href="%s" media-type="%s"%s/>' % (item_id, name, mtype, extra))
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


def _field(par, instr, placeholder=None):
    """Sisipkan field Word (PAGE, TOC, ...) ke dalam paragraf."""
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    r1 = par.add_run()._r
    fc = OxmlElement("w:fldChar"); fc.set(qn("w:fldCharType"), "begin"); r1.append(fc)
    r2 = par.add_run()._r
    it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve")
    it.text = instr; r2.append(it)
    r3 = par.add_run()._r
    sep = OxmlElement("w:fldChar"); sep.set(qn("w:fldCharType"), "separate"); r3.append(sep)
    if placeholder:
        par.add_run(placeholder)
    r4 = par.add_run()._r
    end = OxmlElement("w:fldChar"); end.set(qn("w:fldCharType"), "end"); r4.append(end)


def _lang(par, code):
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    for run in par.runs:
        rpr = run._r.get_or_add_rPr()
        el = OxmlElement("w:lang"); el.set(qn("w:val"), code); rpr.append(el)


def _tbl_header_repeat(row):
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    trpr = row._tr.get_or_add_trPr()
    el = OxmlElement("w:tblHeader"); el.set(qn("w:val"), "true"); trpr.append(el)


def build_docx(cfg):
    """Naskah DOCX siap sunting: A4, margin cermin, gaya Heading, TOC field."""
    from docx.shared import Cm
    from docx.enum.section import WD_SECTION
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn

    doc = Document()
    copy = book_pdf.COPY[cfg["lang"]]
    lang_code = "en-GB" if cfg["lang"] == "en" else "id-ID"

    style = doc.styles["Normal"]
    style.font.name = "Times New Roman"
    style.font.size = Pt(12)
    pf = style.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf.first_line_indent = Mm(12.7)
    pf.space_after = Pt(0)
    pf.line_spacing = 1.15
    rpr = style.element.get_or_add_rPr()
    lang_el = OxmlElement("w:lang"); lang_el.set(qn("w:val"), lang_code); rpr.append(lang_el)

    # ---- gaya judul bawaan, disetel ulang ke Times New Roman ----
    for name, size, align, italic in (("Heading 1", 20, WD_ALIGN_PARAGRAPH.CENTER, False),
                                      ("Heading 2", 12, WD_ALIGN_PARAGRAPH.LEFT, False),
                                      ("Heading 3", 11, WD_ALIGN_PARAGRAPH.LEFT, True)):
        st = doc.styles[name]
        st.font.name = "Times New Roman"
        st.font.size = Pt(size)
        st.font.bold = not italic
        st.font.italic = italic
        st.font.color.rgb = None
        st.paragraph_format.alignment = align
        st.paragraph_format.first_line_indent = Mm(0)
        st.paragraph_format.space_before = Pt(18 if name == "Heading 1" else 12)
        st.paragraph_format.space_after = Pt(10 if name == "Heading 1" else 6)
        st.paragraph_format.keep_with_next = True
        st.paragraph_format.line_spacing = 1.0

    # ---- halaman: A4, margin simetris 30 mm (sama dengan PDF) ----
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Mm(210), Mm(297)
    sec.left_margin, sec.right_margin = Mm(30), Mm(30)
    sec.top_margin, sec.bottom_margin = Mm(30), Mm(40)
    sec.header_distance, sec.footer_distance = Mm(15), Mm(14)

    # ---- kepala & kaki halaman berjalan ----
    def _hdr(container, text, align):
        p = container.paragraphs[0]
        p.text = ""
        p.alignment = align
        p.paragraph_format.first_line_indent = Mm(0)
        r = p.add_run(text)
        r.font.name = "Times New Roman"; r.font.size = Pt(8.5)

    _hdr(sec.header, RUNNING_FOR(cfg), WD_ALIGN_PARAGRAPH.CENTER)
    for footer, align in ((sec.footer, WD_ALIGN_PARAGRAPH.RIGHT),):
        p = footer.paragraphs[0]
        p.text = ""
        p.alignment = align
        p.paragraph_format.first_line_indent = Mm(0)
        _field(p, " PAGE ", "1")

    # ---- halaman judul ----
    for _ in range(6):
        doc.add_paragraph()
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.first_line_indent = Mm(0)
    r = p.add_run(copy["title"]); r.bold = True; r.font.size = Pt(26)
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.first_line_indent = Mm(0)
    r = p.add_run(copy["sub"]); r.font.size = Pt(14)
    for _ in range(6):
        doc.add_paragraph()
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.first_line_indent = Mm(0)
    r = p.add_run(copy["author"]); r.font.size = Pt(14)
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.first_line_indent = Mm(0)
    r = p.add_run(copy["published"] + "  \u00b7  " + copy["edition"]); r.font.size = Pt(10)

    # ---- halaman hak cipta ----
    doc.add_page_break()
    for txt, size in ((copy["title"], 11.5), (copy["sub"], 10.5), (copy["author"], 10.5)):
        p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.first_line_indent = Mm(0)
        r = p.add_run(txt); r.font.size = Pt(size); r.bold = (size == 11.5)
    for txt in (copy["edition"], copy["published"], copy["rights"],
                copy["legal"], copy["disclaimer"], copy["credits"]):
        p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.first_line_indent = Mm(0)
        p.paragraph_format.space_before = Pt(8)
        r = p.add_run(txt); r.font.size = Pt(9.5)

    # ---- daftar isi otomatis ----
    doc.add_page_break()
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.first_line_indent = Mm(0)
    r = p.add_run("Contents" if cfg["lang"] == "en" else "Daftar Isi")
    r.bold = True; r.font.size = Pt(14)
    p = doc.add_paragraph(); p.paragraph_format.first_line_indent = Mm(0)
    _field(p, ' TOC \\o "1-2" \\h \\z \\u ',
           "Update this field (Ctrl+A, F9) to build the contents."
           if cfg["lang"] == "en" else
           "Perbarui field ini (Ctrl+A, F9) untuk menyusun daftar isi.")

    for kind, val, extra in blocks_of(cfg["md"]):
        if kind == "h1":
            p = doc.add_paragraph(style="Heading 1")
            p.paragraph_format.page_break_before = True
            p.add_run(val)
        elif kind == "h2":
            doc.add_paragraph(val, style="Heading 2")
        elif kind == "h3":
            doc.add_paragraph(val, style="Heading 3")
        elif kind == "table":
            if not val:
                continue
            ncol = max(len(r) for r in val)
            t = doc.add_table(rows=0, cols=ncol)
            t.style = "Table Grid"
            for ri, row in enumerate(val):
                cells = t.add_row().cells
                if ri == 0:
                    _tbl_header_repeat(t.rows[-1])
                for i, c in enumerate(row[:ncol]):
                    cells[i].text = c
                    for par in cells[i].paragraphs:
                        par.paragraph_format.first_line_indent = Mm(0)
                        par.paragraph_format.line_spacing = 1.0
                        for run in par.runs:
                            run.font.size = Pt(9.5)
                            run.font.name = "Times New Roman"
                            if ri == 0:
                                run.bold = True
        elif kind == "caption":
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.first_line_indent = Mm(0)
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.keep_with_next = True
            r = p.add_run(val); r.bold = True; r.font.size = Pt(10)
            if extra:
                p2 = doc.add_paragraph()
                p2.alignment = WD_ALIGN_PARAGRAPH.LEFT
                p2.paragraph_format.first_line_indent = Mm(0)
                p2.paragraph_format.space_before = Pt(1)
                p2.paragraph_format.keep_with_next = True
                r2 = p2.add_run(extra); r2.italic = True; r2.font.size = Pt(8.5)
        elif kind == "figure":
            path, caption, source = val
            full = path if os.path.isabs(path) else os.path.join(book_pdf.BOOK_DIR, path)
            if os.path.exists(full):
                p = doc.add_paragraph()
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p.paragraph_format.first_line_indent = Mm(0)
                p.paragraph_format.space_before = Pt(8)
                p.paragraph_format.keep_with_next = True
                run = p.add_run()
                run.add_picture(full, width=Mm(150))
                try:
                    doc.inline_shapes[-1]._inline.docPr.set(
                        "descr", figure_alt(caption, cfg["lang"]))
                except Exception:
                    pass
            else:
                print("PERINGATAN: gambar hilang:", full)
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.first_line_indent = Mm(0)
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.keep_with_next = bool(source)
            flabel, ftext = split_caption(caption)
            r = p.add_run(flabel + " "); r.bold = True; r.font.size = Pt(9.5)
            r = p.add_run(ftext); r.font.size = Pt(9.5)
            if source:
                p = doc.add_paragraph()
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p.paragraph_format.first_line_indent = Mm(0)
                p.paragraph_format.space_after = Pt(10)
                r = p.add_run(source)
                r.italic = True; r.font.size = Pt(8)
                r.font.color.rgb = RGBColor(0x5A, 0x5A, 0x5A)
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

    cp = doc.core_properties
    cp.title = cfg["title"]
    cp.author = cfg["author"]
    cp.subject = copy["sub"]
    cp.comments = cfg["description"]
    cp.keywords = "; ".join(cfg["subjects"])
    cp.category = cfg["subjects"][0]
    cp.language = lang_code
    cp.last_modified_by = cfg["author"]
    doc.save(cfg["docx"])


def RUNNING_FOR(cfg):
    return book_pdf.RUNNING[cfg["lang"]]


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
        # Interior yang dipakai sampul harus yang terbaru: sampul menghitung
        # tebal punggung dari jumlah halaman PDF ini. Interior basi = spine salah.
        shutil.copyfile(cfg["pdf"], cfg["interior"])
        print("%s: interior %d halaman -> %s"
              % (cfg["lang"], len(PdfReader(cfg["pdf"]).pages), cfg["interior"]))
        n = build_epub(cfg)
        build_docx(cfg)
        print("%s: %d bab -> %s, %s" % (cfg["lang"], n, cfg["epub"], cfg["docx"]))


if __name__ == "__main__":
    main()
