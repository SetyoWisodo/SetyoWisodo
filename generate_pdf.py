import sys
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

# --- Numbered Canvas for Two-Pass Page Numbering ---
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, total_pages):
        self.saveState()
        # Do not draw on the cover page (page 1)
        if self._pageNumber > 1:
            # Running Header
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor("#64748b"))
            self.drawString(45, A4[1] - 35, "PACDORA 3D — DOKUMENTASI TEKNIS & PANDUAN LENGKAP MOCKUP KEMASAN")
            self.setFont("Helvetica", 8)
            self.drawRightString(A4[0] - 45, A4[1] - 35, "STUDIO V2.0")
            
            # Header line
            self.setStrokeColor(colors.HexColor("#e2e8f0"))
            self.setLineWidth(0.75)
            self.line(45, A4[1] - 40, A4[0] - 45, A4[1] - 40)

            # Running Footer
            self.line(45, 42, A4[0] - 45, 42)
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#94a3b8"))
            self.drawString(45, 30, "Hak Cipta © 2026 Setyo Wisodo. Dikompilasi untuk Penggunaan Produksi & Percetakan.")
            page_text = f"Halaman {self._pageNumber} dari {total_pages}"
            self.drawRightString(A4[0] - 45, 30, page_text)

        self.restoreState()


def build_pdf(filename="Panduan_Lengkap_Pacdora_3D_Mockup.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=45,
        rightMargin=45,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    # Custom Colors
    c_primary = colors.HexColor("#4f46e5")    # Indigo
    c_dark = colors.HexColor("#0f172a")       # Slate 900
    c_body = colors.HexColor("#334155")       # Slate 700
    c_accent = colors.HexColor("#d97706")     # Amber
    c_bg_light = colors.HexColor("#f8fafc")   # Slate 50
    c_border = colors.HexColor("#e2e8f0")

    # Typography Styles
    title_cover = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=26,
        leading=32,
        textColor=colors.white,
        alignment=1, # Center
        spaceAfter=10
    )

    subtitle_cover = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#c7d2fe"),
        alignment=1,
        spaceAfter=20
    )

    h1 = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=c_dark,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2 = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=c_primary,
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )

    h3 = ParagraphStyle(
        'Heading3_Custom',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=c_dark,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=c_body,
        spaceAfter=6
    )

    body_bold = ParagraphStyle(
        'Body_Bold',
        parent=body,
        fontName='Helvetica-Bold'
    )

    bullet = ParagraphStyle(
        'Bullet_Custom',
        parent=body,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=4
    )

    code_text = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#0f172a")
    )

    callout_text = ParagraphStyle(
        'Callout_Custom',
        parent=body,
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#1e293b")
    )

    elements = []

    # =========================================================================
    # 1. COVER PAGE
    # =========================================================================
    elements.append(Spacer(1, 30))

    # Cover Header Card
    cover_table_data = [
        [
            Paragraph("<b>PACDORA 3D MOCKUP & DIELINE STUDIO</b>", title_cover)
        ],
        [
            Paragraph("Buku Panduan Teknis Komprehensif, Spesifikasi CAD 9 Model Kemasan,<br/>Alur Kerja Dieline Percetakan, dan Dokumentasi Kode Program Lengkap", subtitle_cover)
        ],
        [
            Paragraph("<font size=9 color='#a5b4fc'>Versi Dokumen 2.0 • Tanggal Rilis: 19 September 2026 • Penulis: Setyo Wisodo</font>", ParagraphStyle('CoverMeta', alignment=1))
        ]
    ]
    cover_table = Table(cover_table_data, colWidths=[A4[0] - 90])
    cover_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#1e1b4b")),
        ('TOPPADDING', (0, 0), (-1, -1), 32),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 32),
        ('LEFTPADDING', (0, 0), (-1, -1), 24),
        ('RIGHTPADDING', (0, 0), (-1, -1), 24),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('CORNERPAD', (0, 0), (-1, -1), 12)
    ]))
    elements.append(cover_table)

    elements.append(Spacer(1, 25))

    # Executive Summary Card on Cover
    summary_html = """
    <b>RINGKASAN EKSEKUTIF (EXECUTIVE SUMMARY):</b><br/>
    Dokumen ini menyajikan dokumentasi lengkap dan menyeluruh atas perancangan, implementasi, dan pengoperasian 
    <b>Pacdora 3D Mockup & Dieline Generator</b>. Sistem ini merupakan platform berbasis WebGL dan Three.js 
    yang memungkinkan perancang grafis, produsen UMKM, percetakan kemasan (<i>packaging converter</i>), 
    dan agensi merek untuk merancang, menguji buka-tutup (<i>hinged opening</i>), mensimulasikan material realistis (PBR), 
    serta mengekspor pola jaring-jaring pisau pond (<i>CAD Dieline</i>) berstandar industri secara presisi.
    """
    summary_card = Table([[Paragraph(summary_html, body)]], colWidths=[A4[0] - 90])
    summary_card.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f1f5f9")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
        ('LEFTPADDING', (0, 0), (-1, -1), 16),
        ('RIGHTPADDING', (0, 0), (-1, -1), 16),
        ('TOPPADDING', (0, 0), (-1, -1), 14),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 14),
    ]))
    elements.append(summary_card)

    elements.append(Spacer(1, 20))

    # Key Features List on Cover
    feat_data = [
        [Paragraph("<b>Fitur Inti</b>", body_bold), Paragraph("<b>Deskripsi Teknis</b>", body_bold)],
        [Paragraph("Katalog Kemasan 3D", body), Paragraph("9 model parametrik: Kotak Mailer, Tuck Box, Kaleng Aluminium, Botol Pipet, Stand-up Pouch, Gelas Kopi, Tas Belanja, Tube, Jar.", body)],
        [Paragraph("2D Dieline Engine", body), Paragraph("Kanvas interaktif 2048x2048 px dengan garis Cut (Merah), Crease (Biru putus-putus), Bleed (Hijau), & teks CAD.", body)],
        [Paragraph("Sinkronisasi Real-time", body), Paragraph("Setiap ketukan tombol dan pergeseran elemen 2D seketika memicu pembaruan tekstur Three.js tanpa jeda waktu.", body)],
        [Paragraph("Animasi Buka/Tutup", body), Paragraph("Slider interaktif menggerakkan engsel tutup kotak atau membuka pipet dari 0% hingga 100%.", body)],
        [Paragraph("Ekspor Beragam Format", body), Paragraph("Render 4K Ultra HD (PNG transparan), Pola Vektor SVG CAD, Video Putaran 360° WebM, dan model 3D glTF/GLB.", body)],
    ]
    t_feat = Table(feat_data, colWidths=[130, A4[0] - 90 - 130])
    t_feat.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(t_feat)

    elements.append(PageBreak())

    # =========================================================================
    # 2. DAFTAR ISI & BAB 1: PENGENALAN
    # =========================================================================
    elements.append(Paragraph("DAFTAR ISI LENGKAP", h1))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=c_primary, spaceBefore=4, spaceAfter=12))

    toc_items = [
        ("BAB 1: Pengenalan & Gambaran Umum Sistem", "Halaman 2"),
        ("BAB 2: Arsitektur Website & Alur Kerja Perancangan", "Halaman 3"),
        ("BAB 3: Spesifikasi Teknis 9 Model Kemasan 3D Parametrik", "Halaman 4"),
        ("BAB 4: Panduan Editor Jaring-Jaring 2D & Standar CAD Dieline", "Halaman 6"),
        ("BAB 5: Fisika Material (PBR), Tekstur Alami, & Studio Cahaya", "Halaman 7"),
        ("BAB 6: Mekanisme Interaktif, Animasi Buka/Tutup & Turntable", "Halaman 8"),
        ("BAB 7: Suite Ekspor Lengkap (Render 4K, Vector SVG, Video 360, glTF)", "Halaman 9"),
        ("BAB 8: Preset Desain Merek Siap Pakai (Brand Showcase)", "Halaman 10"),
        ("BAB 9: Pedoman Teknis Percetakan & Produksi Massal (Converter Guide)", "Halaman 11"),
        ("BAB 10: Dokumentasi Kode Program Standalone (pacdora-template.html)", "Halaman 12"),
        ("BAB 11: Lembar Pintasan Keyboard & Panduan Pemecahan Masalah", "Halaman 14"),
    ]

    toc_table_data = [[Paragraph(f"<b>{title}</b>", body), Paragraph(f"<font color='#6366f1'><b>{page}</b></font>", ParagraphStyle('R', alignment=2, fontName='Helvetica'))] for title, page in toc_items]
    t_toc = Table(toc_table_data, colWidths=[A4[0] - 160, 70])
    t_toc.setStyle(TableStyle([
        ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.HexColor("#f1f5f9")),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    elements.append(t_toc)

    elements.append(Spacer(1, 14))

    elements.append(Paragraph("BAB 1: Pengenalan & Gambaran Umum Sistem", h1))
    elements.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=10))

    elements.append(Paragraph(
        "Platform <b>Pacdora 3D Mockup Studio</b> dirancang untuk mengatasi kesenjangan mendasar antara "
        "desain grafis kemasan dua dimensi (2D flat artwork) dengan realitas fisik kotak kemasan tiga dimensi (3D). "
        "Secara konvensional, desainer kemasan harus menggunakan software 3D terpisah yang rumit seperti Blender, "
        "Maya, atau Cinema4D hanya untuk melihat bagaimana logo dan teks melengkung pada kaleng atau terlipat pada sudut kotak karton. "
        "Dengan platform ini, perancangan dilakukan secara langsung di dalam peramban web (browser) dengan presisi teknis setara CAD.",
        body
    ))

    elements.append(Paragraph(
        "<b>Kelebihan Platform Dibandingkan Perangkat Lunak Konvensional:</b>",
        body_bold
    ))
    elements.append(Paragraph("• <b>Tanpa Instalasi Berat:</b> Berjalan sepenuhnya di peramban web modern menggunakan WebGL dan akselerasi kartu grafis bawaan perangkat.", bullet))
    elements.append(Paragraph("• <b>Presisi Dimensi Pabrik:</b> Menggunakan satuan milimeter (mm) riil yang langsung terhubung ke rumus bentangan CAD kemasan standar FEFCO dan ECMA.", bullet))
    elements.append(Paragraph("• <b>Dual-Engine Synchronization:</b> Mengintegrasikan kanvas 2D HTML5 beresolusi tinggi dengan Three.js MeshPhysicalMaterial PBR shader.", bullet))
    elements.append(Paragraph("• <b>Bilingual Support:</b> Antarmuka intuitif dengan dukungan dwibahasa (Bahasa Indonesia & Bahasa Inggris).", bullet))

    elements.append(PageBreak())

    # =========================================================================
    # 3. BAB 2: ARSITEKTUR WEBSITE & ALUR KERJA
    # =========================================================================
    elements.append(Paragraph("BAB 2: Arsitektur Website & Alur Kerja Perancangan", h1))
    elements.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=10))

    elements.append(Paragraph(
        "Arsitektur aplikasi dibangun dengan pola modular modern yang memisahkan State Management, "
        "3D Viewport Engine, 2D Graphic Canvas Engine, serta I/O Exporter. "
        "Hal ini memastikan bahwa penambahan model kemasan baru atau aset grafis tidak membebani performa aplikasi.",
        body
    ))

    arch_data = [
        [Paragraph("<b>Komponen Sistem</b>", body_bold), Paragraph("<b>Teknologi / Modul</b>", body_bold), Paragraph("<b>Fungsi Utama</b>", body_bold)],
        [Paragraph("Top Navigation Bar", body), Paragraph("Navbar.tsx", body), Paragraph("Ganti model cepat, indikator ukuran (mm), Undo/Redo, Switch View, Ekspor modal.", body)],
        [Paragraph("Left Studio Sidebar", body), Paragraph("SidebarLeft.tsx", body), Paragraph("5 Tab: Katalog Model, Dimensi Parametrik, Bahan Permukaan, Studio Cahaya, Preset Merek.", body)],
        [Paragraph("3D WebGL Viewport", body), Paragraph("Viewport3D.tsx (Three.js)", body), Paragraph("OrbitControls 360°, rendering bayangan kontak, kalkulasi engsel lid lipat, snapshot camera.", body)],
        [Paragraph("2D Dieline Editor", body), Paragraph("DielineEditor.tsx (Canvas)", body), Paragraph("Garis panduan CAD (Crease/Cut), layer teks kustom, logo uploader, barcode & QR generator.", body)],
        [Paragraph("Right Inspector", body), Paragraph("SidebarRight.tsx", body), Paragraph("Panel kontrol posisi (X, Y), rotasi, transparansi, warna teks, susunan lapisan (Z-index).", body)],
        [Paragraph("State Store", body), Paragraph("usePackagingStudio.ts", body), Paragraph("Single source of truth dengan tumpukan riwayat Undo/Redo (25 langkah).", body)],
    ]
    t_arch = Table(arch_data, colWidths=[110, 120, A4[0] - 90 - 230])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#e0e7ff")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    elements.append(t_arch)

    elements.append(Spacer(1, 10))

    elements.append(Paragraph("Diagram Alur Kerja Desain Kemasan (Packaging Workflow):", h2))
    workflow_steps = [
        ("Langkah 1: Pemilihan Model Kemasan", "Pengguna memilih tipe kotak atau botol dari katalog (contoh: Tuck Box atau Mailer Box). Dimensi standar langsung dimuat."),
        ("Langkah 2: Penyesuaian Dimensi Parametrik", "Menentukan Lebar (W), Tinggi (H), dan Panjang (D) dalam milimeter. Tampilan 3D dan jaring-jaring 2D menyesuaikan proporsi secara otomatis."),
        ("Langkah 3: Perancangan Grafis 2D Dieline", "Menambahkan teks merek, mengunggah logo berlatar transparan, menambahkan barcode EAN-13, QR Code resmi, atau stempel sertifikasi (Halal/Organik)."),
        ("Langkah 4: Konfigurasi Material & Finishing", "Memilih jenis kertas (Kraft Cokelat, Karton Doff, Kilap UV, Foil Emas, Kaca Amber) serta efek khusus embun air dingin."),
        ("Langkah 5: Simulasi Interaktif & Inspeksi", "Menggeser slider buka-tutup kotak untuk melihat bagian dalam, memutar sudut 360°, dan memeriksa kesesuaian posisi grafis."),
        ("Langkah 6: Ekspor Hasil Cetak & Presentasi", "Mengunduh file cetak Vector SVG untuk pisau pond percetakan serta merender gambar 4K Ultra HD untuk promosi katalog."),
    ]
    for step_num, step_desc in workflow_steps:
        elements.append(Paragraph(f"<b>{step_num}</b>: {step_desc}", bullet))

    elements.append(PageBreak())

    # =========================================================================
    # 4. BAB 3: SPESIFIKASI TEKNIS 9 MODEL KEMASAN 3D
    # =========================================================================
    elements.append(Paragraph("BAB 3: Spesifikasi Teknis 9 Model Kemasan 3D Parametrik", h1))
    elements.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=10))

    elements.append(Paragraph(
        "Aplikasi menyediakan 9 model kemasan parametrik yang mencakup lebih dari 90% kebutuhan industri ritel, e-commerce, "
        "makanan & minuman, serta kosmetik. Setiap model memiliki karakteristik geometri dan mapping UV yang spesifik:",
        body
    ))

    models_data = [
        [
            Paragraph("<b>Model & Kategori</b>", body_bold),
            Paragraph("<b>Dimensi Bawaan</b>", body_bold),
            Paragraph("<b>Estimasi Isi</b>", body_bold),
            Paragraph("<b>Struktur Mekanisme & Fitur Unik</b>", body_bold)
        ],
        [
            Paragraph("<b>1. Standing Pouch (Doypack)</b><br/><font size=7 color='#7c3aed'>Model ID: 604050 (Pacdora)</font>", body),
            Paragraph("75 × 130 × 225 mm", body),
            Paragraph("500 - 1.000 g", body),
            Paragraph("Kemasan fleksibel paling populer dengan segel ziplock atas, lengkungan bottom gusset oval, dan zona upload grafis 491×733 px.", body)
        ],
        [
            Paragraph("<b>2. Stand-up Coffee Pouch</b><br/><font size=7 color='#7c3aed'>Pouches & Bags</font>", body),
            Paragraph("100 × 70 × 220 mm", body),
            Paragraph("250 - 500 g", body),
            Paragraph("Pouch kopi spesialti dengan katup aroma (degassing valve) satu arah dan perekat tin-tie segel udara.", body)
        ],
        [
            Paragraph("<b>3. Zipper Snack & Tea Pouch</b><br/><font size=7 color='#7c3aed'>Pouches & Bags</font>", body),
            Paragraph("120 × 60 × 180 mm", body),
            Paragraph("200 - 350 g", body),
            Paragraph("Pouch kemasan camilan dan bubuk teh hijau matcha dengan ziplock berulang dan lapisan metalik anti-lembab.", body)
        ],
        [
            Paragraph("<b>4. Paper Coffee Bag</b><br/><font size=7 color='#7c3aed'>Pouches & Bags</font>", body),
            Paragraph("120 × 80 × 250 mm", body),
            Paragraph("1.000 g", body),
            Paragraph("Kantong kertas kraft cokelat dengan lipatan samping (side gusset) dan dasar balok lipat (block bottom).", body)
        ],
        [
            Paragraph("<b>5. Kotak Mailer E-Commerce</b><br/><font size=7 color='#7c3aed'>Kotak & Kardus</font>", body),
            Paragraph("200 × 60 × 150 mm", body),
            Paragraph("1.800 ml", body),
            Paragraph("Kardus berengsel belakang dengan lid penutup depan dan dua lid debu samping. Slider buka-tutup berputar hingga 115°.", body)
        ],
        [
            Paragraph("<b>6. Tuck Box Karton Standar</b><br/><font size=7 color='#7c3aed'>Kotak Lipat</font>", body),
            Paragraph("75 × 130 × 75 mm", body),
            Paragraph("731 ml", body),
            Paragraph("Standar kemasan farmasi & kosmetik. 4 panel sisi bersambung (Kiri, Depan, Kanan, Belakang) dengan flap tuck atas yang dapat dibuka.", body)
        ],
        [
            Paragraph("<b>7. Kaleng Minuman Aluminium</b><br/><font size=7 color='#7c3aed'>Botol & Kaleng</font>", body),
            Paragraph("Ø66 × 145 mm", body),
            Paragraph("330 - 500 ml", body),
            Paragraph("Aluminium silinder dengan lekukan tapered rim atas, tab pembuka logam, dan dasar cekung. Label melingkar 360°.", body)
        ],
        [
            Paragraph("<b>8. Botol Pipet Serum Kosmetik</b><br/><font size=7 color='#7c3aed'>Botol Kaca Mewah</font>", body),
            Paragraph("Ø42 × 115 mm", body),
            Paragraph("30 - 50 ml", body),
            Paragraph("Badan kaca amber/bening dengan transmisi optik, cincin collar logam emas, dan pipet tetes karet yang dapat diangkat ke atas.", body)
        ],
        [
            Paragraph("<b>9. Gelas Kopi Kertas Takeaway</b><br/><font size=7 color='#7c3aed'>Gelas & Cup</font>", body),
            Paragraph("Ø90 × 135 mm", body),
            Paragraph("12 oz (350 ml)", body),
            Paragraph("Kerucut terpancung (tapered cylinder) dengan bibir rolled rim dan tutup plastik sipping lid yang dapat dilepas terangkat.", body)
        ],
    ]

    t_models = Table(models_data, colWidths=[105, 95, 75, A4[0] - 90 - 275])
    t_models.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e293b")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(t_models)

    elements.append(PageBreak())

    # =========================================================================
    # 5. BAB 4: PANDUAN EDITOR 2D & STANDAR CAD DIELINE
    # =========================================================================
    elements.append(Paragraph("BAB 4: Panduan Editor Jaring-Jaring 2D & Standar CAD Dieline", h1))
    elements.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=10))

    elements.append(Paragraph(
        "Jaring-jaring kemasan (<i>dieline</i>) adalah pola bentangan datar yang menjadi cetak biru fisik pisau pemotong "
        "dan penekuk pada pabrik percetakan kemasan (<i>packaging converter</i>). "
        "Aplikasi menerapkan standar warna CAD industri internasional:",
        body
    ))

    cad_color_data = [
        [Paragraph("<b>Jenis Garis</b>", body_bold), Paragraph("<b>Warna Standar CAD</b>", body_bold), Paragraph("<b>Tipe Garis</b>", body_bold), Paragraph("<b>Fungsi Manufaktur</b>", body_bold)],
        [Paragraph("Garis Potong (Cut Line)", body), Paragraph("<font color='#ef4444'><b>Merah (#EF4444)</b></font>", body), Paragraph("Solid (Garis Penuh)", body), Paragraph("Jalur pisau baja tajam untuk memotong lembaran kertas/karton.", body)],
        [Paragraph("Garis Lipatan (Crease Line)", body), Paragraph("<font color='#0284c7'><b>Biru (#0284C7)</b></font>", body), Paragraph("Dashed (Putus-putus)", body), Paragraph("Jalur pisau tumpul/rel untuk menekan garis lipatan agar karton tidak sobek.", body)],
        [Paragraph("Batas Aman (Bleed Margin)", body), Paragraph("<font color='#10b981'><b>Hijau (#10B981)</b></font>", body), Paragraph("Dotted (Titik-titik)", body), Paragraph("Kelebihan warna latar sebesar 3mm keluar dari garis potong menghindari tepi putih.", body)],
        [Paragraph("Label & Dimensi", body), Paragraph("<font color='#475569'><b>Abu-abu (#475569)</b></font>", body), Paragraph("Teks Keterangan", body), Paragraph("Keterangan nama panel (Depan, Belakang, Tutup) dan ukuran dalam milimeter.", body)],
    ]
    t_cad = Table(cad_color_data, colWidths=[110, 100, 100, A4[0] - 90 - 310])
    t_cad.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    elements.append(t_cad)

    elements.append(Spacer(1, 10))

    elements.append(Paragraph("Fitur Editor Grafis 2D yang Tersedia:", h2))
    editor_feats = [
        ("Teks Kustom & Tipografi", "Mendukung berbagai jenis font branding (Montserrat, Inter, Poppins, Playfair Display, Bebas Neue, Space Grotesk) dengan kontrol ukuran, bobot ketebalan (300 hingga 800), spasi antar huruf (letter-spacing), dan multiline text."),
        ("Upload Logo & Ilustrasi", "Mendukung file gambar PNG (transparan), JPG, dan WebP. Gambar secara otomatis dihitung aspect ratio-nya dan dapat diposisikan di muka depan maupun samping kemasan."),
        ("Generator Barcode EAN-13 & UPC-A", "Menghasilkan kode batang produk ritel asli lengkap dengan guard pattern dan nomor identifikasi produk standar GS1."),
        ("Generator QR Code Dinamis", "Menghasilkan QR Code matriks berbasis tautan URL atau teks yang dapat langsung dipindai oleh kamera smartphone konsumen."),
        ("Stempel Sertifikasi Kemasan", "Tersedia ikon vektor sertifikasi: Halal Indonesia, 100% Recyclable, Certified Organic, Cruelty Free, FSC Mix Paper, dan Netto Weight."),
        ("Palet Warna Bahan Dasar", "Color picker dinamis untuk mengubah warna dasar karton kemasan yang belum tertutup grafis."),
    ]
    for feat_title, feat_desc in editor_feats:
        elements.append(Paragraph(f"• <b>{feat_title}</b>: {feat_desc}", bullet))

    elements.append(PageBreak())

    # =========================================================================
    # 6. BAB 5: MATERIAL PBR & STUDIO PENCAHAYAAN
    # =========================================================================
    elements.append(Paragraph("BAB 5: Fisika Material (PBR), Tekstur Alami, & Studio Cahaya", h1))
    elements.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=10))

    elements.append(Paragraph(
        "Kunci utama dari fotorealisme pada Pacdora 3D adalah penerapan <i>Physically Based Rendering</i> (PBR) "
        "melalui Three.js <code>MeshPhysicalMaterial</code>. Karakteristik pantulan, kekasaran mikroskopis, "
        "dan lapisan vernis dihitung berdasarkan persamaan pencahayaan fisik nyata:",
        body
    ))

    mat_table_data = [
        [Paragraph("<b>Nama Material</b>", body_bold), Paragraph("<b>Roughness</b>", body_bold), Paragraph("<b>Metalness</b>", body_bold), Paragraph("<b>Clearcoat</b>", body_bold), Paragraph("<b>Karakteristik & Aplikasi</b>", body_bold)],
        [Paragraph("Kraft Paper (Brown)", body), Paragraph("0.88", body), Paragraph("0.00", body), Paragraph("0.00", body), Paragraph("Kardus bergelombang serat kayu alami dengan tekstur procedural noise bump map.", body)],
        [Paragraph("Kraft White", body), Paragraph("0.82", body), Paragraph("0.00", body), Paragraph("0.00", body), Paragraph("Kertas kraft putih berserat lembut ramah lingkungan (eco-friendly).", body)],
        [Paragraph("Matte Coated", body), Paragraph("0.42", body), Paragraph("0.02", body), Paragraph("0.15", body), Paragraph("Karton ivory laminasi doff elegan, tidak memantulkan silau lampu studio.", body)],
        [Paragraph("Ultra Gloss UV", body), Paragraph("0.12", body), Paragraph("0.05", body), Paragraph("0.90", body), Paragraph("Lapisan vernis UV kilap tinggi dengan efek cermin pantul jernih.", body)],
        [Paragraph("Metallic Foil", body), Paragraph("0.22", body), Paragraph("0.85", body), Paragraph("0.40", body), Paragraph("Lapisan foil emas, perak, atau kaleng aluminium dengan kilap logam tinggi.", body)],
        [Paragraph("Kaca Amber", body), Paragraph("0.08", body), Paragraph("0.00", body), Paragraph("Transmission 0.82", body), Paragraph("Kaca botol kosmetik/serum cokelat penyaring sinar UV dengan indeks bias IOR 1.54.", body)],
        [Paragraph("Kaca Bening", body), Paragraph("0.05", body), Paragraph("0.00", body), Paragraph("Transmission 0.92", body), Paragraph("Kaca kristal bening tembus pandang dengan refraksi cahaya realistis.", body)],
    ]
    t_mat = Table(mat_table_data, colWidths=[90, 55, 55, 75, A4[0] - 90 - 275])
    t_mat.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(t_mat)

    elements.append(Spacer(1, 10))

    elements.append(Paragraph("Studio Pencahayaan (Lighting Rigs):", h2))
    light_info = [
        ("Studio Minimal", "Kombinasi dual softbox 5500K netral dan fill light lembut. Menghasilkan pencahayaan merata ideal untuk katalog foto produk e-commerce."),
        ("Warm Commercial", "Sinar utama hangat keemasan (warm keylight 3200K) yang memberikan kesan produk artisan, makanan, kopi, dan nuansa alami."),
        ("Dramatic Rim", "Latar studio gelap dengan dua lampu sorot tepi berlawanan (rim lighting biru dan magenta), menonjolkan siluet dan lekukan badan botol mewah."),
        ("Neon Cyberpunk", "Pencahayaan futuristik dengan warna kontras cyan terang dan magenta neon untuk produk minuman energi atau produk berani."),
        ("Pure Catalog", "Latar putih murni tanpa bayangan kasar dengan pencahayaan overhead diffuse untuk listing marketplace (Tokopedia, Shopee, Amazon)."),
    ]
    for l_title, l_desc in light_info:
        elements.append(Paragraph(f"• <b>{l_title}</b>: {l_desc}", bullet))

    elements.append(PageBreak())

    # =========================================================================
    # 7. BAB 6 & BAB 7: INTERAKSI, ANIMASI & EKSPOR
    # =========================================================================
    elements.append(Paragraph("BAB 6: Mekanisme Interaktif, Animasi Buka/Tutup & Turntable", h1))
    elements.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=8))

    elements.append(Paragraph(
        "Salah satu keunggulan terbesar Pacdora adalah kemampuan melihat kemasan tidak hanya sebagai benda mati statis, "
        "melainkan benda lipat yang dapat digerakkan secara interaktif:",
        body
    ))
    elements.append(Paragraph("• <b>Slider Buka / Tutup Lid:</b> Menggerakkan engsel tutup kotak secara mulus dari 0% (tertutup rapat) hingga 100% (terbuka lebar hingga sudut 115°). Pada botol pipet dan tube, slider mengangkat tutup keluar wadah.", bullet))
    elements.append(Paragraph("• <b>Turntable 360° Otomatis:</b> Kemasan berputar secara kontinu dengan kecepatan rotasi yang dapat diatur untuk keperluan presentasi showcase dinamis.", bullet))
    elements.append(Paragraph("• <b>Preset Sudut Kamera Cepat:</b> Tombol cepat untuk mengubah sudut pandang seketika: Tampak Depan, Tampak Atas, Tampak Kanan, Sudut Hero 45°, dan Isometrik.", bullet))

    elements.append(Spacer(1, 10))

    elements.append(Paragraph("BAB 7: Suite Ekspor Lengkap", h1))
    elements.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=8))

    export_options = [
        [Paragraph("<b>Format Ekspor</b>", body_bold), Paragraph("<b>Resolusi / Tipe</b>", body_bold), Paragraph("<b>Kegunaan Utama</b>", body_bold)],
        [
            Paragraph("Render 4K Snapshot", body),
            Paragraph("Up to 3840 × 2160 px<br/>(PNG Transparan / JPG)", body),
            Paragraph("Foto produk resolusi tinggi bebas watermark untuk banner billboard, marketplace, dan poster promosi cetak.", body)
        ],
        [
            Paragraph("Dieline CAD (SVG)", body),
            Paragraph("Scalable Vector Graphics<br/>(Satuan Milimeter)", body),
            Paragraph("File master pisau pond die-cutting percetakan, siap dibuka langsung di Adobe Illustrator, CorelDRAW, dan mesin laser CNC.", body)
        ],
        [
            Paragraph("Video 360° Turntable", body),
            Paragraph("WebM Video 30 FPS<br/>(Durasi ~4.5 Detik)", body),
            Paragraph("Animasi video berputar mulus (looping seamless) untuk konten Instagram Reels, TikTok, atau etalase e-commerce.", body)
        ],
        [
            Paragraph("Model 3D (.GLB)", body),
            Paragraph("glTF 2.0 Binary<br/>(Embedded UV Texture)", body),
            Paragraph("Model 3D standar industri untuk integrasi ke Blender, Unity, Unreal Engine, Figma, dan Augmented Reality (AR).", body)
        ],
    ]
    t_export = Table(export_options, colWidths=[120, 110, A4[0] - 90 - 230])
    t_export.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#e0e7ff")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    elements.append(t_export)

    elements.append(PageBreak())

    # =========================================================================
    # 8. BAB 8 & BAB 9: PRESET DESAIN & PANDUAN PERCETAKAN
    # =========================================================================
    elements.append(Paragraph("BAB 8: Preset Desain Merek Siap Pakai (Brand Showcase)", h1))
    elements.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=8))

    elements.append(Paragraph(
        "Aplikasi telah dilengkapi preset desain siap pakai dengan estetika komersial premium:",
        body
    ))
    presets_list = [
        ("1. Kopi Nusantara Roasters (Tuck Box)", "Kardus cokelat kraft alami, pita emas vertikal, tipografi serif mewah, stempel Halal Indonesia & Certified Organic, serta barcode ritel EAN-13."),
        ("2. Luxe Botanicals Serum (Dropper Bottle)", "Botol pipet kaca amber cokelat gelap dengan tipografi apotek modern Prancis, teks komposisi 10% Niacinamide, dan QR Code verifikasi keaslian batch."),
        ("3. Volt Surge Energy (Beverage Can)", "Kaleng minuman aluminium hitam metalik dengan tipografi bold cyberpunk, aksen pendar neon biru, dan informasi nutrisi kaleng."),
        ("4. Urban Kicks Mailer Box (Mailer Box)", "Kotak kardus berengsel pengiriman e-commerce dengan grafis gaya streetwear, stempel daur ulang 100%, stempel FSC Paper, dan pesan unboxing di dalam tutup."),
        ("5. Zen Ceremonial Matcha (Stand-up Pouch)", "Pouch hijau hutan doff dengan aksen emas foil, kaligrafi kanji Jepang, dan segel ziplock kedap udara."),
    ]
    for p_title, p_desc in presets_list:
        elements.append(Paragraph(f"• <b>{p_title}</b>: {p_desc}", bullet))

    elements.append(Spacer(1, 10))

    elements.append(Paragraph("BAB 9: Pedoman Teknis Percetakan & Produksi Massal (Converter Guide)", h1))
    elements.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=8))

    elements.append(Paragraph(
        "Untuk memastikan hasil cetak fisik di pabrik percetakan kemasan identik 100% dengan tampilan 3D di layar, "
        "perhatikan pedoman teknis berikut:",
        body
    ))

    print_guidelines = [
        ("Kerapatan Resolusi (DPI)", "Gunakan resolusi minimal 300 DPI saat mengekspor gambar dieline untuk menghindari pikselasi teks berukuran kecil."),
        ("Margin Bleed (Lebihan Cetak)", "Pastikan warna latar belakang ditarik melewati garis potong merah sejauh 3 mm (area hijau). Hal ini mengantisipasi pergeseran pisau pond saat die-cutting massal."),
        ("Area Bebas Lem (Glue Flap)", "Panel pengeleman (glue tab) pada sisi kanan kotak karton tidak boleh terkena lapisan laminasi doff, gloss, atau vernis UV agar lem kemasan dapat merekat kuat."),
        ("Spot UV & Hot Foil Stamping", "Jika menggunakan efek emas metalik pada teks merk, buatlah layer terpisah berwarna hitam 100% (K=100) sebagai acuan pelat klise tembaga hot-stamping."),
        ("Ketebalan Karton (Gramatur)", "Untuk Tuck Box kecil gunakan Ivory / Dupleks 250 - 310 gsm. Untuk Mailer Box e-commerce gunakan Corrugated Flute E atau B (ketebalan 1.5 - 3 mm)."),
    ]
    for g_title, g_desc in print_guidelines:
        elements.append(Paragraph(f"• <b>{g_title}</b>: {g_desc}", bullet))

    elements.append(PageBreak())

    # =========================================================================
    # 9. BAB 10: DOKUMENTASI KODE PROGRAM STANDALONE HTML
    # =========================================================================
    elements.append(Paragraph("BAB 10: Dokumentasi Kode Program Standalone (pacdora-template.html)", h1))
    elements.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=8))

    elements.append(Paragraph(
        "File <code>pacdora-template.html</code> adalah implementasi mandiri (single-file HTML) lengkap yang dapat disalin-tempel "
        "langsung ke lingkungan kerja Anda (VS Code, WordPress, WebView aplikasi mobile) tanpa ketergantungan pada server Node.js. "
        "Di bawah ini adalah ringkasan arsitektur kode dan logika utama program:",
        body
    ))

    code_snippet = """<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <title>Pacdora 3D — Generator & Editor Mockup Kemasan 3D</title>
  <!-- Three.js & OrbitControls via CDN -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
  <style>
    /* CSS Styling Dark Studio Theme, Flexbox Split View, Custom Scrollbar */
    body { background: #0b0d14; color: #f1f5f9; font-family: 'Inter', sans-serif; }
  </style>
</head>
<body>
  <!-- Layout: Top Navbar, 3D Canvas Viewport, 2D Dieline Drawing Canvas -->
  <div id="threeContainer"></div>
  <canvas id="dielineCanvas" width="1024" height="1024"></canvas>

  <script>
    // 1. Inisialisasi Three.js Scene, Camera, WebGLRenderer, Shadows
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(40, width / height, 0.1, 100);
    const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });

    // 2. Dynamic Texture Mapping dari Canvas 2D
    const dielineCanvas = document.getElementById('dielineCanvas');
    const packagingTexture = new THREE.CanvasTexture(dielineCanvas);
    const packagingMaterial = new THREE.MeshPhysicalMaterial({ map: packagingTexture });

    // 3. Rekonstruksi Geometri Parametrik (Tuck Box, Mailer, Can, Bottle, Pouch)
    function rebuild3DModel() { ... }

    // 4. Penggambaran Kanvas 2D Dieline (Teks, Barcode, QR Code, Stempel Halal)
    function drawDieline() {
      // Menggambar garis CAD Crease / Cut
      // Menggambar layer teks & gambar pengguna
      packagingTexture.needsUpdate = true; // Sinkronisasi seketika ke 3D
    }

    // 5. Animasi Loop & Slider Buka/Tutup
    function animate() {
      requestAnimationFrame(animate);
      controls.update();
      renderer.render(scene, camera);
    }
  </script>
</body>
</html>"""

    t_code = Table([[Paragraph(f"<pre>{code_snippet.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')}</pre>", code_text)]], colWidths=[A4[0] - 90])
    t_code.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#0f172a")),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#334155")),
    ]))
    elements.append(t_code)

    elements.append(Spacer(1, 10))
    elements.append(Paragraph(
        "<b>Petunjuk Penyalinan:</b> Buka berkas <code>pacdora-template.html</code> di direktori root repositori, "
        "tekan <b>Ctrl+A</b> lalu <b>Ctrl+C</b>, dan tempelkan ke file baru di komputer Anda. File tersebut mandiri dan langsung berfungsi.",
        callout_text
    ))

    elements.append(PageBreak())

    # =========================================================================
    # 10. BAB 11: SHORTCUT KEYBOARD & TROUBLESHOOTING
    # =========================================================================
    elements.append(Paragraph("BAB 11: Lembar Pintasan Keyboard & Panduan Pemecahan Masalah", h1))
    elements.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=8))

    elements.append(Paragraph("Daftar Pintasan Keyboard (Shortcut Keys):", h2))

    kb_data = [
        [Paragraph("<b>Tombol Pintas</b>", body_bold), Paragraph("<b>Fungsi pada Studio</b>", body_bold), Paragraph("<b>Keterangan</b>", body_bold)],
        [Paragraph("<font color='#4f46e5'><b>Ctrl + Z / Cmd + Z</b></font>", body), Paragraph("Undo (Batal Perubahan)", body), Paragraph("Mengembalikan kondisi teks, logo, atau susunan layer ke langkah sebelumnya (hingga 25 langkah).", body)],
        [Paragraph("<font color='#4f46e5'><b>Ctrl + Y / Cmd + Shift + Z</b></font>", body), Paragraph("Redo (Ulangi)", body), Paragraph("Memulihkan langkah perubahan yang sebelumnya di-undo.", body)],
        [Paragraph("<font color='#ef4444'><b>Delete / Backspace</b></font>", body), Paragraph("Hapus Objek Terpilih", body), Paragraph("Menghapus layer teks, logo, atau bentuk yang sedang aktif di kanvas.", body)],
        [Paragraph("<b>Klik Kiri Drag</b>", body), Paragraph("Rotasi Sudut Pandang 3D", body), Paragraph("Memutar kamera mengelilingi kemasan 360 derajat secara bebas.", body)],
        [Paragraph("<b>Scroll Wheel Mouse</b>", body), Paragraph("Zoom In / Zoom Out", body), Paragraph("Memperbesar dan memperkecil jarak pandang ke detail kemasan.", body)],
        [Paragraph("<b>Klik Kanan Drag / Alt + Drag</b>", body), Paragraph("Pan Kamera (Geser Posisi)", body), Paragraph("Menggeser posisi kemasan ke kiri, kanan, atas, atau bawah layar.", body)],
    ]
    t_kb = Table(kb_data, colWidths=[125, 120, A4[0] - 90 - 245])
    t_kb.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    elements.append(t_kb)

    elements.append(Spacer(1, 10))

    elements.append(Paragraph("Panduan Pemecahan Masalah (Troubleshooting):", h2))
    trouble_items = [
        ("Gambar Logo Tidak Muncul", "Pastikan file berformat PNG, JPG, atau WebP yang valid. Gunakan format PNG dengan transparansi alpha untuk hasil logo yang menyatu dengan latar belakang kemasan."),
        ("Teks Pecah Saat Dicetak", "Ekspor dieline dalam format Vector SVG. File SVG menggunakan kurva matematis tak terhingga sehingga teks akan tajam sempurna pada resolusi percetakan berapa pun."),
        ("Model 3D Tampak Terlalu Gelap", "Ubah preset studio pencahayaan ke 'Pure Catalog' atau 'Studio Minimal', dan naikkan warna latar kemasan ke warna yang lebih terang."),
        ("File HTML Tidak Menampilkan 3D Saat Dibuka", "Pastikan komputer Anda terkoneksi ke internet saat pertama kali membuka file pacdora-template.html untuk memuat Three.js CDN, atau gunakan file pacdora-studio.html yang sudah 100% offline."),
    ]
    for tr_title, tr_desc in trouble_items:
        elements.append(Paragraph(f"• <b>{tr_title}</b>: {tr_desc}", bullet))

    elements.append(Spacer(1, 14))

    # Concluding Box
    concl_html = """
    <b>PENGESAHAN DOKUMEN:</b><br/>
    Buku panduan ini merupakan dokumentasi resmi implementasi perangkat lunak <b>Pacdora 3D Packaging Mockup Studio</b>.
    Seluruh model 3D, algoritma UV projection, dieline CAD vector exporter, dan kode sumber telah diuji secara komprehensif
    dan dinyatakan siap untuk produksi desain kemasan profesional.
    <br/><br/>
    <i>Banyuwangi, Jawa Timur, Indonesia — 19 September 2026 • Penulis: Setyo Wisodo</i>
    """
    t_concl = Table([[Paragraph(concl_html, body)]], colWidths=[A4[0] - 90])
    t_concl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#e0e7ff")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#6366f1")),
        ('LEFTPADDING', (0, 0), (-1, -1), 14),
        ('RIGHTPADDING', (0, 0), (-1, -1), 14),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))
    elements.append(t_concl)

    # Build PDF with NumberedCanvas
    doc.build(elements, canvasmaker=NumberedCanvas)
    print(f"PDF berhasil dibuat: {filename}")


if __name__ == '__main__':
    output_pdf = "Panduan_Lengkap_Pacdora_3D_Mockup.pdf"
    build_pdf(output_pdf)
