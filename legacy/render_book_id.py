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
    text = re.sub(r'\[\^(\d+)\]', r'<sup>\1</sup>', text)
    return text

lines = md.split('\n')
html_parts = []
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
        html_parts.append('<h1>%s</h1>' % inline(s[2:].strip()))
        continue
    if s.startswith('## '):
        if in_ul:
            html_parts.append('</ul>'); in_ul=False
        html_parts.append('<h2>%s</h2>' % inline(s[3:].strip()))
        continue
    if s.startswith('### '):
        if in_ul:
            html_parts.append('</ul>'); in_ul=False
        html_parts.append('<h3>%s</h3>' % inline(s[4:].strip()))
        continue
    if s.strip().startswith('- '):
        if not in_ul:
            html_parts.append('<ul>'); in_ul=True
        html_parts.append('<li>%s</li>' % inline(s.strip()[2:].strip()))
        continue
    m = re.match(r'^\d+\.\s+(.*)', s.strip())
    if m:
        if not in_ul:
            html_parts.append('<ul>'); in_ul=True
        html_parts.append('<li>%s</li>' % inline(m.group(1).strip()))
        continue
    if s.strip() == '':
        if in_ul:
            html_parts.append('</ul>'); in_ul=False
        html_parts.append('<br>')
        continue
    if in_ul:
        html_parts.append('</ul>'); in_ul=False
    html_parts.append('<p>%s</p>' % inline(s.strip()))
    html_parts.append('<br>')

if in_ul:
    html_parts.append('</ul>')

html = '\n'.join(html_parts)

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
    def __init__(self):
        super().__init__()
        self.page_fns = {}
        self._fn_seen = set()
        self._page_fn_start = set()
        self._rendered_fn_pages = set()
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
        fns = sorted(self.page_fns.get(p, ()))
        if not fns:
            cur = self._fn_seen - self._page_fn_start
            if cur:
                fns = sorted(cur)
        if fns and p not in self._rendered_fn_pages:
            self._rendered_fn_pages.add(p)
            self.set_y(self.h - self.b_margin + 1)
            self.set_font('DejaVu', '', 7.5)
            for n in fns:
                txt = footnotes.get(n, '')
                self.set_x(self.l_margin)
                self.multi_cell(0, 3.0, '%d. %s' % (n, txt), new_x='LMARGIN', new_y='NEXT')
            self.set_font('DejaVu', '', 8)
        self.set_y(-5)
        self.set_font('DejaVu', '', 8)
        self.cell(0, 5, 'Halaman %d' % p, align='C')

pdf = BookPDF()
pdf.set_auto_page_break(auto=True, margin=7)
pdf.add_page()
pdf.add_font('DejaVu', '', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', uni=True)
pdf.add_font('DejaVu', 'B', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', uni=True)
pdf.set_font('DejaVu', '', 8.3)

pdf.set_font('DejaVu', 'B', 16)
pdf.cell(0, 16, 'Bertahan Hidup di Masa Depan', ln=True, align='C')
pdf.set_font('DejaVu', '', 11)
pdf.cell(0, 8, 'Krisis, Iklim, dan Resiliensi Manusia', ln=True, align='C')
pdf.ln(4)
pdf.set_font('DejaVu', '', 9)
pdf.cell(0, 6, 'Panduan Berbasis Data dan Ilmiah', ln=True, align='C')
pdf.cell(0, 6, 'Penulis: Setyo Wisodo   |   Tahun: 2026', ln=True, align='C')
pdf.add_page()

pdf.write_html(html)

if pdf.page > 0:
    fns = pdf._fn_seen - pdf._page_fn_start
    if fns:
        pdf.page_fns[pdf.page] = fns

pdf.output('/home/user/SetyoWisodo/Surviving_the_Future_ID.pdf')
print('PDF written; footnotes:', len(footnotes))
