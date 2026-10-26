# -*- coding: utf-8 -*-
"""Bangun sampul cetak (punggung + belakang + depan) dari artwork sampul depan.

Trim 6 x 9 inci, bleed 0,125 inci, punggung dihitung dari jumlah halaman
(0,0025 inci per halaman, kertas offset 60 lb) — angka yang dipakai printer
print-on-demand. Hasil: PDF 300 dpi siap unggah.

Pemakaian: python make_cover.py
"""
import json

from PIL import Image, ImageDraw, ImageFont

DPI = 300
TRIM_W, TRIM_H = 8.27, 11.69   # A4, sesuai PDF isi
BLEED = 0.125
PER_PAGE = 0.0025

FONT_DIR = "book/fonts"
SERIF_B = FONT_DIR + "/SourceSerif4-Semibold.otf"
SERIF_R = FONT_DIR + "/SourceSerif4-Regular.otf"
SERIF_I = FONT_DIR + "/SourceSerif4-It.otf"
SANS = FONT_DIR + "/SourceSans3-Regular.otf"

BOOKS = [
    {
        "front": "book/publish/Surviving_the_Future_EN_cover_front.jpg",
        "out_pdf": "book/publish/Surviving_the_Future_EN_cover_print.pdf",
        "pages": 412,
        "title": "SURVIVING THE FUTURE",
        "subtitle": "Crisis, Climate, and Human Resilience",
        "author": "SETYO WISODO",
        "blurb": [
            "Five of the warmest years ever measured. A cyclone that killed 138,000 people in 1991 and a "
            "cyclone that killed dozens in 2020, on the same coastline. A heatwave that killed 70,000 "
            "Europeans in 2003 and a hotter one that killed 61,700 in 2022 because the institutions "
            "had changed.",
            "This book reads the record of the past two decades closely enough to show why the next "
            "disaster will fall on some places and not others, and it argues that the difference is "
            "usually a decision rather than a fate.",
            "Twenty-four chapters, twenty-five data tables, eleven data figures, twenty-four case studies "
            "and a reference list of 145 sources. Written for readers who want the evidence rather than "
            "the slogan.",
        ],
        "back_head": "WHAT THE RECORD SHOWS",
        "pull": "A prepared world is not a world without disasters. It is a world in which the same event kills fewer people.",
        "inside": [
            "Why a cyclone killed 500,000 people in 1970 and dozens in 2020 on the same coastline",
            "The heatwave that killed 70,000 Europeans in 2003 — and the hotter one that killed 61,700 in 2022",
            "The Ahr valley, where the forecast was right and 180 people died anyway",
            "What a heat action plan, a shelter register and a protected budget line actually cost",
            "The four clocks of climate policy: emissions, concentration, temperature, sea level",
            "How to read a death toll, a loss estimate and a warning that never reached its street",
        ],
        "bio": "Setyo Wisodo holds a degree in history education from Universitas Negeri Malang. "
               "He reads the past for patterns, tests them against present-day data, and writes about "
               "what that comparison implies for disaster risk adaptation and community resilience.",
        "spine_title": "SURVIVING THE FUTURE",
    },
    {
        "front": "book/publish/Bertahan_Hidup_di_Masa_Depan_ID_cover_front.jpg",
        "out_pdf": "book/publish/Bertahan_Hidup_di_Masa_Depan_ID_cover_print.pdf",
        "pages": 432,
        "title": "BERTAHAN HIDUP DI MASA DEPAN",
        "subtitle": "Krisis, Iklim, dan Resiliensi Manusia",
        "author": "SETYO WISODO",
        "blurb": [
            "Lima tahun terpanas yang pernah terukur. Siklon yang menewaskan 138.000 orang pada 1991 dan "
            "siklon yang menewaskan puluhan orang pada 2020, di pesisir yang sama. Gelombang panas yang "
            "menewaskan 70.000 orang Eropa pada 2003 dan gelombang yang lebih panas pada 2022 tetapi "
            "menewaskan 61.700 orang karena lembaganya sudah berubah.",
            "Buku ini membaca catatan dua dekade terakhir cukup dekat untuk menunjukkan mengapa bencana "
            "berikutnya akan menimpa sebagian tempat dan bukan yang lain, dan berargumen bahwa "
            "perbedaannya biasanya sebuah keputusan, bukan takdir.",
            "Dua puluh empat bab, dua puluh lima tabel data, sebelas gambar data, dua puluh empat studi "
            "kasus, dan daftar pustaka 145 sumber. Ditulis untuk pembaca yang menginginkan bukti, bukan "
            "slogan.",
        ],
        "back_head": "APA YANG DITUNJUKKAN CATATAN",
        "pull": "Dunia yang siap bukan dunia tanpa bencana. Ia dunia tempat peristiwa yang sama menewaskan lebih sedikit orang.",
        "inside": [
            "Mengapa sebuah siklon menewaskan 500.000 orang pada 1970 dan puluhan pada 2020 di pesisir yang sama",
            "Gelombang panas yang menewaskan 70.000 orang Eropa pada 2003, dan yang lebih panas tetapi menewaskan 61.700 pada 2022",
            "Lembah Ahr, ketika prakiraannya benar dan 180 orang tetap meninggal",
            "Berapa biaya sebenarnya sebuah rencana aksi panas, daftar warga rentan, dan pos anggaran yang dilindungi",
            "Empat jam kebijakan iklim: emisi, konsentrasi, suhu, permukaan laut",
            "Cara membaca jumlah kematian, taksiran kerugian, dan peringatan yang tidak pernah sampai ke jalannya",
        ],
        "bio": "Setyo Wisodo adalah sarjana pendidikan sejarah lulusan Universitas Negeri Malang. "
               "Ia membaca masa lalu untuk menemukan pola, mengujinya dengan data hari ini, dan menulis "
               "tentang apa yang tersirat bagi adaptasi risiko bencana dan ketahanan komunitas.",
        "spine_title": "BERTAHAN HIDUP DI MASA DEPAN",
    },
]

BACK_RGB = (14, 26, 42)
ACCENT = (232, 163, 61)


def px(inches):
    return int(round(inches * DPI))



INTERIORS = {
    "en": "book/publish/Surviving_the_Future_EN_interior.pdf",
    "id": "book/publish/Bertahan_Hidup_di_Masa_Depan_ID_interior.pdf",
}


def page_count(path, fallback):
    """Jumlah halaman nyata dari PDF interior; pakai angka cadangan bila belum ada."""
    try:
        import pymupdf
        n = len(pymupdf.open(path))
        if n:
            return n
        print("PERINGATAN: %s kosong; memakai %d halaman" % (path, fallback))
    except Exception:
        print("PERINGATAN: %s belum ada; memakai %d halaman" % (path, fallback))
    return fallback


def wrap(draw, text, font, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        cand = (cur + " " + w).strip()
        if draw.textlength(cand, font=font) <= width or not cur:
            cur = cand
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def build(cfg):
    spine = cfg["pages"] * PER_PAGE
    total_w = BLEED * 2 + TRIM_W * 2 + spine
    total_h = BLEED * 2 + TRIM_H
    W, H = px(total_w), px(total_h)

    canvas = Image.new("RGB", (W, H), BACK_RGB)
    draw = ImageDraw.Draw(canvas)

    front = Image.open(cfg["front"]).convert("RGB")
    tw, th = px(TRIM_W), px(TRIM_H)
    # skala "cover": penuhi bidang, pangkas kelebihannya, jangan diregangkan
    scale = max(tw / front.width, th / front.height)
    fw, fh = int(front.width * scale + 0.5), int(front.height * scale + 0.5)
    front = front.resize((fw, fh), Image.LANCZOS)
    left = (fw - tw) // 2
    top = (fh - th) // 2
    front = front.crop((left, top, left + tw, top + th))
    canvas.paste(front, (px(BLEED + TRIM_W + spine), px(BLEED)))

    # ---------- spine ----------
    spine_x0 = px(BLEED + TRIM_W)
    spine_w = px(spine)
    draw.rectangle([spine_x0, 0, spine_x0 + spine_w, H], fill=(10, 19, 32))
    f_spine = ImageFont.truetype(SERIF_B, px(0.155))
    label = cfg["spine_title"]
    tw = draw.textlength(label, font=f_spine)
    while tw > H * 0.72 and f_spine.size > 20:
        f_spine = ImageFont.truetype(SERIF_B, f_spine.size - 2)
        tw = draw.textlength(label, font=f_spine)
    tmp = Image.new("RGBA", (int(tw) + 8, int(f_spine.size * 1.6)), (0, 0, 0, 0))
    d2 = ImageDraw.Draw(tmp)
    d2.text((4, 0), label, font=f_spine, fill=(240, 240, 240))
    tmp = tmp.rotate(-90, expand=True)
    canvas.paste(tmp, (spine_x0 + (spine_w - tmp.width) // 2, int(H * 0.30)), tmp)

    f_author = ImageFont.truetype(SANS, px(0.105))
    at = cfg["author"]
    aw = draw.textlength(at, font=f_author)
    tmp2 = Image.new("RGBA", (int(aw) + 8, int(f_author.size * 1.6)), (0, 0, 0, 0))
    d3 = ImageDraw.Draw(tmp2)
    d3.text((4, 0), at, font=f_author, fill=(210, 210, 210))
    tmp2 = tmp2.rotate(-90, expand=True)
    canvas.paste(tmp2, (spine_x0 + (spine_w - tmp2.width) // 2, int(H * 0.66)), tmp2)

    # ---------- back ----------
    margin = px(0.55)
    x = px(BLEED) + margin
    y = px(BLEED) + px(0.62)
    col_w = px(TRIM_W) - 2 * margin

    f_head = ImageFont.truetype(SERIF_B, px(0.225))
    draw.text((x, y), cfg["back_head"], font=f_head, fill=ACCENT)
    y += px(0.50)
    draw.line([x, y, x + px(0.7), y], fill=ACCENT, width=px(0.014))
    y += px(0.30)

    f_body = ImageFont.truetype(SERIF_R, px(0.158))
    line_h = px(0.242)
    for para in cfg["blurb"]:
        for ln in wrap(draw, para, f_body, col_w):
            draw.text((x, y), ln, font=f_body, fill=(240, 241, 244))
            y += line_h
        y += px(0.15)

    # ---------- zona barcode ritel (dibiarkan kosong) ----------
    bc_w, bc_h = 2.0, 1.2                      # inci, ukuran minimum EAN-13
    bc_x0 = px(BLEED + TRIM_W - 0.35 - bc_w)
    bc_y1 = px(BLEED + TRIM_H - 0.35)
    bc_y0 = bc_y1 - px(bc_h)
    draw.rectangle([bc_x0, bc_y0, bc_x0 + px(bc_w), bc_y1], fill=(255, 255, 255))

    # blok penulis: kolom menyempit agar tidak menabrak zona barcode
    f_bio = ImageFont.truetype(SERIF_R, px(0.132))
    bio = cfg["bio"]
    bio_w = bc_x0 - x - px(0.25)
    yb0 = H - px(BLEED) - px(1.42) - len(wrap(draw, bio, f_bio, bio_w)) * px(0.178)
    draw.line([x, yb0 - px(0.2), x + px(0.6), yb0 - px(0.2)], fill=ACCENT, width=px(0.012))
    yb = yb0
    for ln in wrap(draw, bio, f_bio, bio_w):
        draw.text((x, yb), ln, font=f_bio, fill=(214, 220, 229))
        yb += px(0.178)

    # isi buku, sebagai butir pendek di kolom belakang
    y += px(0.10)
    draw.line([x, y, x + col_w, y], fill=(70, 88, 110), width=px(0.005))
    y += px(0.22)
    f_bul = ImageFont.truetype(SERIF_R, px(0.140))
    for item in cfg["inside"]:
        draw.text((x, y), "\u2022", font=f_bul, fill=ACCENT)
        for i, ln in enumerate(wrap(draw, item, f_bul, col_w - px(0.26))):
            draw.text((x + px(0.26), y), ln, font=f_bul, fill=(234, 237, 242))
            y += px(0.216)
        y += px(0.075)

    # kutipan penarik di tengah sampul belakang
    f_q = ImageFont.truetype(SERIF_I, px(0.238))
    qlines = wrap(draw, cfg["pull"], f_q, col_w - px(0.9))
    qh = len(qlines) * px(0.330)
    qy = int((y + (H - px(BLEED) - px(1.9) - qh)) / 2)
    draw.line([x, qy - px(0.28), x + px(0.9), qy - px(0.28)], fill=ACCENT, width=px(0.014))
    for ln in qlines:
        draw.text((x + px(0.15), qy), ln, font=f_q, fill=(245, 247, 250))
        qy += px(0.330)

    f_sub = ImageFont.truetype(SERIF_I, px(0.140))
    yb = H - px(BLEED) - px(0.7)
    for ln in wrap(draw, cfg["subtitle"], f_sub, col_w):
        draw.text((x, yb), ln, font=f_sub, fill=(170, 178, 190))
        yb += px(0.15)

    canvas.save("/tmp/_cover.png", dpi=(DPI, DPI))
    canvas.save(cfg["out_pdf"], "PDF", resolution=DPI)
    return total_w, total_h, spine


def main():
    report = {}
    for cfg in BOOKS:
        key = "en" if "EN" in cfg["out_pdf"] else "id"
        pages = page_count(INTERIORS[key], cfg["pages"])
        cfg = dict(cfg, pages=pages)
        w, h, spine = build(cfg)
        report[key] = {
            "pages": pages,
            "trim_in": [TRIM_W, TRIM_H],
            "bleed_in": BLEED,
            "spine_in": round(spine, 3),
            "cover_in": [round(w, 3), round(h, 3)],
            "dpi": DPI,
            "barcode_area_in": {"width": 2.0, "height": 1.2,
                                "from_bottom_trim": 0.35, "from_right_trim": 0.35},
            "interior_pdf": INTERIORS[key],
            "cover_pdf": cfg["out_pdf"],
        }
        print("%s: %d pp, cover %.2f x %.2f in, spine %.3f in -> %s"
              % (key, pages, w, h, spine, cfg["out_pdf"]))
    with open("book/publish/build_report.json", "w") as fh:
        json.dump(report, fh, indent=2)


if __name__ == "__main__":
    main()
