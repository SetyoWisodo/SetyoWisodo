import re
from fpdf import FPDF
from fpdf.html import HTML2FPDF

with open('/home/user/SetyoWisodo/book_id.md', 'r', encoding='utf-8') as f:
    raw = f.read()

footnotes = {}
body_lines = []
for line in raw.split('\n'):
    m = re.match(r'^\[\^(\d+)\]:\s*(.*)$', line.strip())
    if m:
        footnotes[int(m.group(1))] = m.group(2).strip()
        continue
    body_lines.append(line)
md = '\n'.join(body_lines)

def inline(text):
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    # Superscript footnote marker dihapus sesuai permintaan user
    text = re.sub(r'\[\^(\d+)\]', r'', text)
    return text

def md_to_html(md_text):
    lines = md_text.split('\n')
    html_parts = []
    in_ul = False
    in_table = False
    table_has_body = False
    for idx, line in enumerate(lines):
        s = line.rstrip()
        if s.strip() == '---':
            if in_ul:
                html_parts.append('</ul>'); in_ul = False
            html_parts.append('<hr>')
            continue
        if s.startswith('# '):
            if in_ul:
                html_parts.append('</ul>'); in_ul=False
            html_parts.append('<h1 style="line-height:1.4; margin-top:4mm; margin-bottom:3mm; text-align:center;">%s</h1>' % inline(s[2:].strip()))
            continue
        if s.startswith('## '):
            if in_ul:
                html_parts.append('</ul>'); in_ul=False
            html_parts.append('<h2 style="line-height:1.35; margin-top:3mm; margin-bottom:2mm;">%s</h2>' % inline(s[3:].strip()))
            continue
        if s.startswith('### '):
            if in_ul:
                html_parts.append('</ul>'); in_ul=False
            html_parts.append('<h3 style="line-height:1.5; margin-top:3mm; margin-bottom:2mm;">%s</h3>' % inline(s[4:].strip()))
            continue
        # --- Tabel markdown -> <table> HTML (fpdf2 mendukung table) ---
        if s.strip().startswith('|'):
            if in_ul:
                html_parts.append('</ul>'); in_ul = False
            if not in_table:
                nrows = 0
                for nxt in lines[idx:]:
                    if nxt.strip().startswith('|'):
                        nrows += 1
                    else:
                        break
                # lookahead: sertakan paragraf sesudah tabel agar tidak tersisa 1-2 baris di halaman baru
                after_words = 0
                seen_blank = 0
                for nxt in lines[idx + nrows:]:
                    st = nxt.strip()
                    if not st:
                        seen_blank += 1
                        if seen_blank > 2:
                            break
                        continue
                    if st.startswith('#') or st.startswith('|') or st == '---':
                        break
                    after_words += len(st.split())
                html_parts.append('<table border="1" width="100%%" align="center" data-rows="%d" data-after="%d">' % (nrows, after_words))
                in_table = True
            cells = [c.strip() for c in s.strip().strip('|').split('|')]
            if all(re.fullmatch(r':?-{2,}:?', c) for c in cells if c):
                continue  # baris separator |---|---|
            is_head = (not table_has_body)
            tag = 'th' if is_head else 'td'
            row = ''.join(
                '<%s width="%s" style="font-size:8.5pt; line-height:1.15; padding:0.6mm;" align="left"><b>%s</b></%s>' % (tag, "18%" if ci == 0 else "82%", inline(c), tag)
                if is_head else
                '<%s width="%s" style="font-size:8.5pt; line-height:1.15; padding:0.6mm;" align="left">%s</%s>' % (tag, "18%" if ci == 0 else "82%", inline(c), tag)
                for ci, c in enumerate(cells)
            )
            html_parts.append('<tr>%s</tr>' % row)
            if not is_head:
                table_has_body = True
            continue
        if in_table and not s.strip().startswith('|'):
            html_parts.append('</table>')
            in_table = False
            table_has_body = False
        if s.strip().startswith('- '):
            if not in_ul:
                html_parts.append('<ul>'); in_ul=True
            html_parts.append('<li style="line-height:1.25; text-align:justify;">%s</li>' % inline(s.strip()[2:].strip()))
            continue
        m = re.match(r'^\d+\.\s+(.*)', s.strip())
        if m:
            if not in_ul:
                html_parts.append('<ul>'); in_ul=True
            html_parts.append('<li style="line-height:1.25; text-align:justify;">%s</li>' % inline(m.group(1).strip()))
            continue
        if s.strip() == '':
            if in_ul:
                html_parts.append('</ul>'); in_ul=False
            if in_table:
                html_parts.append('</table>'); in_table=False; table_has_body=False
            html_parts.append('<div style="height:0.8mm;"></div>')
            continue
        if in_ul:
            html_parts.append('</ul>'); in_ul=False
        html_parts.append('<p style="text-align:justify; line-height:1.18; margin-bottom:2.0mm; text-indent:12.7mm;">%s</p>' % inline(s.strip()))
    if in_ul:
        html_parts.append('</ul>')
    if in_table:
        html_parts.append('</table>')
    return '\n'.join(html_parts)

chunks = re.split(r'(?=^# (?:Bab|Lampiran)\b)', md, flags=re.MULTILINE)

class TrackingHTML2PDF(HTML2FPDF):
    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            attrs_d = dict(attrs)
            try:
                rows = int(attrs_d.get('data-rows', 4))
            except (TypeError, ValueError):
                rows = 4
            try:
                after_words = int(attrs_d.get('data-after', 0))
            except (TypeError, ValueError):
                after_words = 0
            need = 5 + rows * 6.0 + (int(after_words / 11) + 1) * 5.0  # mm tabel + paragraf sesudahnya
            if self.pdf.get_y() + need > self.pdf.page_break_trigger and self.pdf.get_y() > self.pdf.t_margin + 4:
                self.pdf.add_page()
        super().handle_starttag(tag, attrs)

    def handle_data(self, data):
        super().handle_data(data)
        if 'sup' in self._tags_stack:
            num_str = data.strip()
            if num_str.isdigit():
                n = int(num_str)
                if n in footnotes:
                    self.pdf._record_fn(n)

class BookPDF(FPDF):
    HTML2FPDF_CLASS = TrackingHTML2PDF
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.page_fns = {}
        self._fn_seen = set()
        self._page_fn_start = set()
        self._rendered_fn_pages = set()
        self.chapter_starts = set()
    def _record_fn(self, n):
        self._fn_seen.add(n)
    def add_page(self, *a, **k):
        if self.page > 0:
            prev = self.page
            fns = self._fn_seen - self._page_fn_start
            if fns:
                self.page_fns[prev] = fns
        self._page_fn_start = set(self._fn_seen)
        super().add_page(*a, **k)
    def footer(self):
        p = self.page
        # Footnote di bawah halaman dinonaktifkan sesuai permintaan user (hapus blok footnote di margin bawah)
        # Hanya nomor halaman yang ditampilkan
        self.set_y(-12)
        self.set_font('TNR', '', 12)
        if p in self.chapter_starts:
            self.cell(0, 5, '%d' % p, align='C')
        else:
            self.cell(0, 5, '%d' % p, align='R')

pdf = BookPDF(orientation='P', unit='mm', format='A4')
pdf.set_margins(left=30, top=30, right=30)
pdf.set_auto_page_break(auto=True, margin=40)
pdf.add_font('TNR', '', '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf', uni=True)
pdf.add_font('TNR', 'B', '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf', uni=True)
pdf.set_font('TNR', '', 12)

pdf.add_page()
pdf.chapter_starts.add(pdf.page)
pdf.set_font('TNR', 'B', 12)
pdf.cell(0, 16, 'Bertahan Hidup di Masa Depan', new_x='LMARGIN', new_y='NEXT', align='C')
pdf.set_font('TNR', '', 12)
pdf.cell(0, 8, 'Krisis, Iklim, dan Resiliensi Manusia', new_x='LMARGIN', new_y='NEXT', align='C')
pdf.ln(4)
pdf.set_font('TNR', '', 12)
pdf.cell(0, 6, 'Panduan Berbasis Data dan Ilmiah', new_x='LMARGIN', new_y='NEXT', align='C')
pdf.cell(0, 6, 'Penulis: Setyo Wisodo   |   Tahun: 2026', new_x='LMARGIN', new_y='NEXT', align='C')

if chunks and chunks[0].strip():
    pdf.add_page()
    html = md_to_html(chunks[0])
    pdf.write_html(html)

for chunk in chunks[1:]:
    if not chunk.strip():
        continue
    pdf.add_page()
    pdf.chapter_starts.add(pdf.page)
    html = md_to_html(chunk)
    pdf.write_html(html)

if pdf.page > 0:
    fns = pdf._fn_seen - pdf._page_fn_start
    if fns:
        pdf.page_fns[pdf.page] = fns

pdf.output('/home/user/SetyoWisodo/Surviving_the_Future_ID.pdf')
print('PDF written; footnotes:', len(footnotes), 'pages:', pdf.page, 'format: A4 margins 30/30/30/40mm')

# blank page cleanup: hapus halaman kosong sisa page-break
try:
    import pymupdf as _pm
    _doc = _pm.open('/home/user/SetyoWisodo/Surviving_the_Future_ID.pdf')
    _blank = [i for i, _pg in enumerate(_doc) if len(_pg.get_text().strip().split()) <= 1]
    for _i in reversed(_blank):
        _doc.delete_page(_i)
    if _blank:
        _doc.saveIncr()
    print('blank pages removed:', _blank, '| final pages:', len(_doc))
    _doc.close()
except Exception as _e:
    print('blank cleanup skipped:', _e)
