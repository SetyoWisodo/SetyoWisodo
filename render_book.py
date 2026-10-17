import re
from fpdf import FPDF

with open('/home/user/SetyoWisodo/book.md', 'r', encoding='utf-8') as f:
    md = f.read()

def inline(text):
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.+?)\*', r'\1', text)
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
    # first-line indent
    html_parts.append('<p>&nbsp;&nbsp;&nbsp;&nbsp;%s</p>' % inline(s.strip()))
    html_parts.append('<br>')

if in_ul:
    html_parts.append('</ul>')

html = '\n'.join(html_parts)

pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=7)
pdf.add_page()
pdf.add_font('DejaVu', '', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', uni=True)
pdf.add_font('DejaVu', 'B', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', uni=True)
pdf.set_font('DejaVu', '', 9.5)

pdf.set_font('DejaVu', 'B', 16)
pdf.cell(0, 16, 'Surviving the Future', ln=True, align='C')
pdf.set_font('DejaVu', '', 11)
pdf.cell(0, 8, 'Crisis, Climate, and Human Resilience', ln=True, align='C')
pdf.ln(4)
pdf.set_font('DejaVu', '', 9)
pdf.cell(0, 6, 'A Data-Driven, Academically Grounded Guide', ln=True, align='C')
pdf.cell(0, 6, 'Author: Setyo Wisodo   |   Year: 2026', ln=True, align='C')
pdf.add_page()

pdf.write_html(html)
pdf.output('/home/user/SetyoWisodo/Surviving_the_Future.pdf')
print('PDF written')
