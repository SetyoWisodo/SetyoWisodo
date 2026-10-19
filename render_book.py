import re
from fpdf import FPDF
from fpdf.html import HTML2FPDF

with open('/home/user/SetyoWisodo/book.md', 'r', encoding='utf-8') as f:
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
    # Superscript footnote marker dihapus sesuai permintaan user (hilangkan angka superscript di seluruh buku)
    text = re.sub(r'\[\^(\d+)\]', r'', text)
    return text

def md_to_html(md_text):
    lines = md_text.split('\n')
    html_parts = []
    # Global style untuk line spacing dan justify - diterapkan via CSS yang didukung fpdf2
    # FPDF2 mendukung style pada tag melalui parsing CSS inline
    in_ul = False
    for line in lines:
        s = line.rstrip()
        if s.strip() == '---':
            if in_ul:
                html_parts.append('</ul>'); in_ul = False
            html_parts.append('<hr>')
            continue
        if s.startswith('# '):
            if in_ul:
                html_parts.append('</ul>'); in_ul=False
            html_parts.append('<h1 style="line-height:1.5; margin-top:6mm; margin-bottom:4mm; text-align:center;">%s</h1>' % inline(s[2:].strip()))
            continue
        if s.startswith('## '):
            if in_ul:
                html_parts.append('</ul>'); in_ul=False
            html_parts.append('<h2 style="line-height:1.5; margin-top:4mm; margin-bottom:3mm;">%s</h2>' % inline(s[3:].strip()))
            continue
        if s.startswith('### '):
            if in_ul:
                html_parts.append('</ul>'); in_ul=False
            html_parts.append('<h3 style="line-height:1.5; margin-top:3mm; margin-bottom:2mm;">%s</h3>' % inline(s[4:].strip()))
            continue
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
            html_parts.append('<div style="height:2mm;"></div>')
            continue
        if in_ul:
            html_parts.append('</ul>'); in_ul=False
        html_parts.append('<p style="text-align:justify; line-height:1.25; margin-bottom:4mm; text-indent:12.7mm;">%s</p>' % inline(s.strip()))
    if in_ul:
        html_parts.append('</ul>')
    return '\n'.join(html_parts)

# Split into chunks: each Chapter / Appendix starts new page
chunks = re.split(r'(?=^# (?:Chapter|Appendix)\b)', md, flags=re.MULTILINE)

class TrackingHTML2PDF(HTML2FPDF):
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
        # Footnote di bawah halaman dinonaktifkan sesuai permintaan user (hapus blok 15. Prof. Mark Howden... di screenshot)
        # Hanya tampilkan nomor halaman sesuai aturan penomoran
        # Nomor halaman: bab pertama tengah bawah, selain bab kanan bawah; margin sesuai 3/3/3/4 cm
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

# Cover page
pdf.add_page()
pdf.chapter_starts.add(pdf.page)
pdf.set_font('TNR', 'B', 12)
pdf.cell(0, 16, 'Surviving the Future', new_x='LMARGIN', new_y='NEXT', align='C')
pdf.set_font('TNR', '', 12)
pdf.cell(0, 8, 'Crisis, Climate, and Human Resilience', new_x='LMARGIN', new_y='NEXT', align='C')
pdf.ln(4)
pdf.set_font('TNR', '', 12)
pdf.cell(0, 6, 'A Data-Driven, Academically Grounded Guide', new_x='LMARGIN', new_y='NEXT', align='C')
pdf.cell(0, 6, 'Author: Setyo Wisodo   |   Year: 2026', new_x='LMARGIN', new_y='NEXT', align='C')

# Write chunks
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

pdf.output('/home/user/SetyoWisodo/Surviving_the_Future.pdf')
print('PDF written; footnotes:', len(footnotes), 'pages:', pdf.page, 'format: A4 margins 30/30/30/40mm')
