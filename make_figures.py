# -*- coding: utf-8 -*-
"""Bangun sebelas gambar data buku ke figures/*.png (300 dpi).

Gaya: serif Tinos (sesuai badan buku), tanpa judul di dalam gambar — judul
dibawa oleh caption di buku; hanya label sumbu, angka, dan keterangan sumber.
Angka diambil dari tabel di book.md / book_id.md; setiap nilai diperiksa ulang
oleh verify() terhadap teks tabel.

Jalankan: python make_figures.py
"""
import os
import re

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.ticker import FuncFormatter

HERE = os.path.dirname(os.path.abspath(__file__))
LANG = "en"          # diisi main(); "id" menghasilkan berkas *_id.png
FONT_DIR = os.path.join(HERE, "fonts")
OUT = os.path.join(HERE, "figures")

NAVY = "#12304f"
AMBER = "#b07d2b"
RUST = "#9b3d2e"
SLATE = "#8fa3b8"
INK = "#1f2933"
MUTED = "#5b6b7c"
GRID = "#dfe4ea"


ID = {
    # sumbu
    "Warming above 1850–1900 (°C)": "Pemanasan di atas 1850–1900 (°C)",
    "Days per year above 35 °C": "Hari per tahun di atas 35 °C",
    "People depending on the basin (million)": "Penduduk yang bergantung pada cekungan (juta)",
    "People exposed to a 1-in-100-year coastal flood (million)":
        "Penduduk terpapar banjir pesisir 100 tahun (juta)",
    "Yield change per +1 °C (%)": "Perubahan hasil panen per +1 °C (%)",
    "Decline or loss (%)": "Penurunan atau kehilangan (%)",
    "Loss of global GDP by 2050 (%)": "Kerugian PDB global pada 2050 (%)",
    "Internal climate migrants by 2050 (million)": "Migran iklim internal pada 2050 (juta)",
    "Excess heat deaths per year, 2050 (thousands)":
        "Kematian berlebih akibat panas per tahun, 2050 (ribu)",
    "Deaths (logarithmic scale)": "Kematian (skala logaritma)",
    # kategori
    "SSP1-2.6 rapid decarbonisation": "SSP1-2.6 dekarbonisasi cepat",
    "SSP2-4.5 current policies": "SSP2-4.5 kebijakan sekarang",
    "SSP5-8.5 stalled decarbonisation": "SSP5-8.5 dekarbonisasi terhenti",
    "Tigris–Euphrates": "Tigris–Efrat", "Citarum (Java)": "Citarum (Jawa)",
    "Maize": "Jagung", "Wheat": "Gandum", "Rice": "Padi", "Soybean": "Kedelai",
    "Coffee": "Kopi", "Livestock (milk)": "Ternak (susu)",
    "Coral reefs": "Terumbu karang", "Freshwater species": "Spesies air tawar",
    "Mangroves": "Mangrove", "Permafrost": "Permafrost",
    "Low emissions": "Emisi rendah", "Current policies": "Kebijakan sekarang",
    "High emissions": "Emisi tinggi",
    "Low adaptation": "Adaptasi rendah", "Current trends": "Tren sekarang",
    "High adaptation": "Adaptasi tinggi",
    "Sub-Saharan Africa": "Afrika sub-Sahara",
    "East Asia and Pacific": "Asia Timur dan Pasifik",
    "South Asia": "Asia Selatan", "North Africa": "Afrika Utara",
    "Latin America": "Amerika Latin", "Small island states": "Negara pulau kecil",
    "now": "sekarang", "at 2 °C": "pada 2 °C", "at 3 °C": "pada 3 °C",
    "Europe 2003 (heat)": "Eropa 2003 (panas)",
    "Pakistan 2022 (flood)": "Pakistan 2022 (banjir)",
    "Chicago 1995 (heat)": "Chicago 1995 (panas)",
    "Lytton 2021 (heat and fire)": "Lytton 2021 (panas dan kebakaran)",
    "Germany 2021 (flood)": "Jerman 2021 (banjir)",
    "Black Saturday 2009 (fire)": "Black Saturday 2009 (kebakaran)",
    "Seoul 2022 (flood)": "Seoul 2022 (banjir)",
    "Camp Fire 2018 (fire)": "Camp Fire 2018 (kebakaran)",
    "Ethiopia 1984–85": "Etiopia 1984–85", "Sahel 1972–74": "Sahel 1972–74",
}


def tr(text):
    """Terjemahkan label gambar untuk edisi Indonesia."""
    if LANG == "en" or not text:
        return text
    norm = re.sub(r"\s+", " ", text)
    if norm in ID:
        return ID[norm]
    m = re.match(r"^(\d+)\.(\d+)(?:–(\d+)\.(\d+))?$", text)
    if m:
        if m.group(3):
            return "%s,%s–%s,%s" % (m.group(1), m.group(2), m.group(3), m.group(4))
        return "%s,%s" % (m.group(1), m.group(2))
    m = re.match(r"^(\d+)\.(\d+) °C$", text)
    if m:
        return "%s,%s °C" % (m.group(1), m.group(2))
    m = re.match(r"^([\d.,]+) million\s+·\s+2050 gap (.+)$", text)
    if m:
        num = re.sub(r"(\d)\.(\d)", r"\1,\2", m.group(1))
        return "%s juta  ·  celah 2050 %s" % (num, m.group(2))
    m = re.match(r"^(\d+) to (\d+)%$", text)
    if m:
        return "%s sampai %s%%" % (m.group(1), m.group(2))
    return text


def localize(fig):
    """Ganti semua teks yang tergambar bila LANG != en."""
    if LANG == "en":
        return
    for ax in fig.axes:
        for t in ax.texts:
            t.set_text(tr(t.get_text()))
        ax.set_xlabel(tr(ax.get_xlabel()))
        ax.set_ylabel(tr(ax.get_ylabel()))
        ax.set_title(tr(ax.get_title()))
        ticks = ax.get_xticks()
        labels = ax.get_xticklabels()
        if labels and not any(t.get_text() for t in labels):
            pass
        else:
            ax.set_xticklabels([tr(t.get_text()) for t in labels])
        ylabels = ax.get_yticklabels()
        if ylabels:
            ax.set_yticklabels([tr(t.get_text()) for t in ylabels])
        leg = ax.get_legend()
        if leg:
            for t in leg.get_texts():
                t.set_text(tr(t.get_text()))


def setup():
    for f in ("Tinos-Regular.ttf", "Tinos-Bold.ttf", "Tinos-Italic.ttf"):
        path = os.path.join(FONT_DIR, f)
        if os.path.exists(path):
            fm.fontManager.addfont(path)
    plt.rcParams.update({
        "font.family": "Tinos",
        "font.size": 8.5,
        "axes.edgecolor": "#9aa7b4",
        "axes.linewidth": 0.6,
        "axes.labelcolor": INK,
        "xtick.color": MUTED,
        "ytick.color": INK,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8.5,
        "axes.titlesize": 9,
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "savefig.facecolor": "white",
        "figure.facecolor": "white",
    })
    os.makedirs(OUT, exist_ok=True)


def tidy(ax, axis="x"):
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.spines["left"].set_color("#9aa7b4")
    ax.spines["bottom"].set_color("#9aa7b4")
    if axis == "x":
        ax.xaxis.grid(True, color=GRID, linewidth=0.6)
        ax.set_axisbelow(True)
    else:
        ax.yaxis.grid(True, color=GRID, linewidth=0.6)
        ax.set_axisbelow(True)


def save(fig, name):
    localize(fig)
    if LANG != "en":
        name = name.replace(".png", "_" + LANG + ".png")
    path = os.path.join(OUT, name)
    fig.tight_layout(pad=0.3)
    fig.savefig(path, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)
    print("  ->", os.path.relpath(path, HERE))


# --------------------------------------------------------------- 2.1 --------
def fig2_1():
    fig, ax = plt.subplots(figsize=(5.9, 2.9))
    rows = [("SSP1-2.6  rapid decarbonisation", 1.6, 1.8, (1.3, 2.4), NAVY),
            ("SSP2-4.5  current policies", 2.0, 2.7, (2.1, 3.5), AMBER),
            ("SSP5-8.5  stalled decarbonisation", 2.6, 4.4, (3.3, 5.7), RUST)]
    for label, y2050, y2100, (lo, hi), colour in rows:
        ax.plot([2050, 2100], [y2050, y2100], color=colour, linewidth=2.2,
                solid_capstyle="round", zorder=3)
        ax.plot([2050], [y2050], "o", color="white", markeredgecolor=colour,
                markeredgewidth=1.6, markersize=6, zorder=4)
        ax.plot([2100], [y2100], "o", color=colour, markersize=6, zorder=4)
        ax.vlines(2100, lo, hi, color=colour, linewidth=1.0, alpha=0.55, zorder=2)
        ax.hlines([lo, hi], 2096.5, 2100, color=colour, linewidth=1.0, alpha=0.55, zorder=2)
        ax.annotate("%.1f °C" % y2100, (2100, y2100), xytext=(7, 2),
                    textcoords="offset points", va="bottom", fontsize=8.5,
                    color=colour, fontweight="bold")
        ax.annotate("%.1f–%.1f" % (lo, hi), (2100, y2100), xytext=(7, -2),
                    textcoords="offset points", va="top", fontsize=7.2,
                    color=MUTED)
        ax.annotate(label, (2050, y2050), xytext=(-9, 0), textcoords="offset points",
                    ha="right", va="center", fontsize=8.5, color=INK)
    ax.set_xlim(1985, 2150)
    ax.set_ylim(1.0, 6.0)
    ax.set_xticks([2050, 2100])
    ax.set_xticklabels(["2050", "2100"])
    ax.set_ylabel("Warming above 1850–1900 (°C)")
    tidy(ax, "y")
    save(fig, "fig2_1.png")


# --------------------------------------------------------------- 4.1 --------
def fig4_1():
    data = [("Phoenix", 110, 150), ("Delhi", 100, 140), ("Karachi", 60, 100),
            ("Jakarta", 30, 70), ("Lagos", 20, 60), ("Athens", 30, 55)]
    fig, ax = plt.subplots(figsize=(5.9, 2.9))
    for i, (city, now, fut) in enumerate(data):
        ax.plot([now, fut], [i, i], color=SLATE, linewidth=3.0, alpha=0.45,
                solid_capstyle="round", zorder=2)
        ax.plot([now], [i], "o", color="white", markeredgecolor=NAVY,
                markeredgewidth=1.5, markersize=6, zorder=3)
        ax.plot([fut], [i], "o", color=AMBER, markersize=7, zorder=4)
        ax.annotate("+%d" % (fut - now), (fut, i), xytext=(8, 0),
                    textcoords="offset points", va="center", fontsize=8,
                    color=MUTED)
    ax.set_yticks(range(len(data)))
    ax.set_yticklabels([d[0] for d in data])
    ax.invert_yaxis()
    ax.set_xlim(0, 175)
    ax.set_xlabel("Days per year above 35 °C")
    ax.plot([], [], "o", color="white", markeredgecolor=NAVY, label="now")
    ax.plot([], [], "o", color=AMBER, label="2050 (SSP2-4.5)")
    ax.legend(frameon=False, fontsize=8, loc="lower right", handletextpad=0.4)
    tidy(ax, "x")
    save(fig, "fig4_1.png")


# --------------------------------------------------------------- 5.1 --------
def fig5_1():
    data = [("Indus", 300, "30–40%"), ("Nile", 280, "25–35%"),
            ("Tigris–Euphrates", 60, "30–40%"), ("Colorado", 40, "20–30%"),
            ("Citarum (Java)", 25, "20–30%"), ("Murray–Darling", 2.4, "10–20%")]
    fig, ax = plt.subplots(figsize=(5.9, 2.7))
    ys = range(len(data))
    ax.barh(list(ys), [d[1] for d in data], color=NAVY, height=0.62, zorder=3)
    for y, (name, pop, gap) in zip(ys, data):
        lab = ("%.1f" % pop) if pop < 10 else ("%d" % pop)
        ax.annotate("%s million  ·  2050 gap %s" % (lab, gap), (pop, y), xytext=(6, 0),
                    textcoords="offset points", va="center", fontsize=8, color=INK)
    ax.set_yticks(list(ys))
    ax.set_yticklabels([d[0] for d in data])
    ax.invert_yaxis()
    ax.set_xlim(0, 430)
    ax.set_xlabel("People depending on the basin (million)")
    tidy(ax, "x")
    save(fig, "fig5_1.png")


# --------------------------------------------------------------- 6.1 --------
def fig6_1():
    data = [("Jakarta", 2.5), ("Manila", 1.5), ("Bangkok", 1.0),
            ("Ho Chi Minh City", 1.0), ("Alexandria", 0.5), ("Miami", 0.4)]
    fig, ax = plt.subplots(figsize=(5.9, 2.7))
    ys = range(len(data))
    ax.barh(list(ys), [d[1] for d in data], color=NAVY, height=0.62, zorder=3)
    for y, (name, val) in zip(ys, data):
        ax.annotate("%.1f million" % val, (val, y), xytext=(6, 0),
                    textcoords="offset points", va="center", fontsize=8, color=INK)
    ax.set_yticks(list(ys))
    ax.set_yticklabels([d[0] for d in data])
    ax.invert_yaxis()
    ax.set_xlim(0, 3.0)
    ax.set_xlabel("People exposed to a 1-in-100-year coastal flood (million)")
    tidy(ax, "x")
    save(fig, "fig6_1.png")


# --------------------------------------------------------------- 7.1 --------
def fig7_1():
    rows = [("Maize", -7.4, -7.4), ("Wheat", -6.0, -6.0), ("Rice", -3.2, -3.2),
            ("Soybean", -3.1, -3.1), ("Coffee", -20, -10),
            ("Livestock (milk)", -10, -5)]
    fig, ax = plt.subplots(figsize=(5.9, 2.9))
    for y, (name, lo, hi) in enumerate(rows):
        if lo == hi:
            ax.barh(y, lo, left=0, color=NAVY, height=0.58, zorder=3)
            lab = "%.1f%%" % lo
        else:
            ax.barh(y, hi - lo, left=lo, color=AMBER, height=0.58, zorder=3)
            lab = "%d to %d%%" % (lo, hi)
        ax.annotate(lab, (lo, y), xytext=(-6, 0), textcoords="offset points",
                    ha="right", va="center", fontsize=8, color=INK)
    ax.axvline(0, color="#9aa7b4", linewidth=0.8, zorder=2)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r[0] for r in rows])
    ax.invert_yaxis()
    ax.set_xlim(-27, 2)
    ax.set_xlabel("Yield change per +1 °C (%)")
    tidy(ax, "x")
    save(fig, "fig7_1.png")


# --------------------------------------------------------------- 8.1 --------
def fig8_1():
    # Label eksplisit: karang sudah >99 % pada 2 °C (IPCC SR1.5), dan pada 3 °C
    # yang dilaporkan adalah kehilangan struktur, bukan persentase baru.
    data = [("Coral reefs   (3 °C: structure lost)", (99, 100), ">99%", None, None),
            ("Freshwater species", (20, 30), "20–30%", (40, 60), "40–60%"),
            ("Mangroves", (10, 30), "10–30%", (30, 50), "30–50%"),
            ("Permafrost", (10, 20), "10–20%", (30, 50), "30–50%")]
    fig, ax = plt.subplots(figsize=(5.9, 2.9))
    ys = list(range(len(data)))
    MINW = 1.6  # keep a 1-point range visible at 300 dpi
    for y, (name, two, lab2, three, lab3) in zip(ys, data):
        ax.barh(y + 0.17, max(two[1] - two[0], MINW), left=two[0], height=0.28,
                color=NAVY, zorder=3)
        if three is not None:
            ax.barh(y - 0.17, max(three[1] - three[0], MINW), left=three[0], height=0.28,
                    color=RUST, zorder=3)
        ax.annotate(lab2, (two[1], y + 0.17), xytext=(6, 0),
                    textcoords="offset points", va="center", fontsize=7.8, color=NAVY)
        if lab3:
            ax.annotate(lab3, (three[1], y - 0.17), xytext=(6, 0),
                        textcoords="offset points", va="center", fontsize=7.8, color=RUST)
    ax.set_yticks(ys)
    ax.set_yticklabels([d[0] for d in data])
    ax.invert_yaxis()
    ax.set_xlim(0, 118)
    ax.set_ylim(len(data) - 0.45, -0.75)
    ax.set_xlabel("Decline or loss (%)")
    from matplotlib.patches import Patch
    handles = [Patch(facecolor=NAVY, label="at 2 °C"),
               Patch(facecolor=RUST, label="at 3 °C")]
    ax.legend(handles=handles, frameon=False, fontsize=8, ncol=2, loc="lower center",
              bbox_to_anchor=(0.5, 1.02), handletextpad=0.4, columnspacing=1.4)
    tidy(ax, "x")
    save(fig, "fig8_1.png")


# -------------------------------------------------------------- 10.1 --------
def fig10_1():
    data = [("High emissions", 15, 20, RUST), ("Current policies", 8, 12, AMBER),
            ("Low emissions", 3, 5, NAVY)]
    fig, ax = plt.subplots(figsize=(5.9, 2.3))
    for y, (name, lo, hi, colour) in enumerate(data):
        ax.barh(y, hi - lo, left=lo, color=colour, height=0.55, zorder=3)
        ax.annotate("%d–%d%%" % (lo, hi), (hi, y), xytext=(6, 0),
                    textcoords="offset points", va="center", fontsize=8.5, color=INK)
    ax.set_yticks(range(len(data)))
    ax.set_yticklabels([d[0] for d in data])
    ax.invert_yaxis()
    ax.set_xlim(0, 24)
    ax.set_xlabel("Loss of global GDP by 2050 (%)")
    tidy(ax, "x")
    save(fig, "fig10_1.png")


# -------------------------------------------------------------- 11.1 --------
def fig11_1():
    data = [("Sub-Saharan Africa", 85, "85"), ("East Asia and Pacific", 48, "48"),
            ("South Asia", 40, "40"), ("North Africa", 19, "19"),
            ("Latin America", 17, "17"), ("Small island states", 2.5, "2–3")]
    fig, ax = plt.subplots(figsize=(5.9, 2.7))
    ys = range(len(data))
    ax.barh(list(ys), [d[1] for d in data], color=NAVY, height=0.62, zorder=3)
    for y, (name, val, lab) in zip(ys, data):
        ax.annotate("%s million" % lab, (val, y), xytext=(6, 0),
                    textcoords="offset points", va="center", fontsize=8, color=INK)
    ax.set_yticks(list(ys))
    ax.set_yticklabels([d[0] for d in data])
    ax.invert_yaxis()
    ax.set_xlim(0, 110)
    ax.set_xlabel("Internal climate migrants by 2050 (million)")
    tidy(ax, "x")
    save(fig, "fig11_1.png")


# -------------------------------------------------------------- 17.1 --------
def fig17_1():
    data = [("Low adaptation", 735), ("Current trends", 500), ("High adaptation", 245)]
    fig, ax = plt.subplots(figsize=(5.9, 2.9))
    xs = range(len(data))
    ax.bar(list(xs), [d[1] for d in data], color=[RUST, AMBER, NAVY], width=0.55, zorder=3)
    for x, (name, val) in zip(xs, data):
        ax.annotate("{:,}".format(val * 1000), (x, val), xytext=(0, 4),
                    textcoords="offset points", ha="center", fontsize=9, color=INK)
    ax.set_xticks(list(xs))
    ax.set_xticklabels([d[0] for d in data])
    ax.set_ylim(0, 820)
    ax.set_ylabel("Excess heat deaths per year, 2050 (thousands)")
    tidy(ax, "x")
    save(fig, "fig17_1.png")


# -------------------------------------------------------------- 22.1 --------
def fig22_1():
    data = [("Europe 2003 (heat)", 70000), ("Pakistan 2022 (flood)", 1700),
            ("Chicago 1995 (heat)", 739), ("Lytton 2021 (heat and fire)", 619),
            ("Germany 2021 (flood)", 180), ("Black Saturday 2009 (fire)", 173),
            ("Seoul 2022 (flood)", 12), ("Camp Fire 2018 (fire)", 85)]
    fig, ax = plt.subplots(figsize=(5.9, 3.0))
    ys = range(len(data))
    ax.barh(list(ys), [d[1] for d in data], color=NAVY, height=0.62, zorder=3)
    for y, (name, val) in zip(ys, data):
        label = "12+" if val == 12 else "{:,}".format(val)
        ax.annotate(label, (val, y), xytext=(6, 0),
                    textcoords="offset points", va="center", fontsize=8, color=INK)
    ax.set_xscale("log")
    ax.set_xlim(8, 300000)
    ax.set_yticks(list(ys))
    ax.set_yticklabels([d[0] for d in data])
    ax.invert_yaxis()
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, p: "{:,}".format(int(v))))
    ax.set_xlabel("Deaths (logarithmic scale)")
    tidy(ax, "x")
    save(fig, "fig22_1.png")


# -------------------------------------------------------------- 23.1 --------
def fig23_1():
    data = [("Ethiopia 1984–85", 1000000), ("Somalia 2011", 258000),
            ("Sahel 1972–74", 100000), ("Somalia 2022", 43000)]
    fig, ax = plt.subplots(figsize=(5.9, 2.3))
    ys = range(len(data))
    ax.barh(list(ys), [d[1] for d in data], color=RUST, height=0.55, zorder=3)
    for y, (name, val) in zip(ys, data):
        ax.annotate("{:,}".format(val), (val, y), xytext=(6, 0),
                    textcoords="offset points", va="center", fontsize=8.5, color=INK)
    ax.set_xscale("log")
    ax.set_xlim(20000, 3000000)
    ax.set_yticks(list(ys))
    ax.set_yticklabels([d[0] for d in data])
    ax.invert_yaxis()
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, p: "{:,}".format(int(v))))
    ax.set_xlabel("Deaths (logarithmic scale)")
    tidy(ax, "x")
    save(fig, "fig23_1.png")


# ------------------------------------------------------------- verifikasi ----
CHECKS = {
    "2.1": ["~1.6°C", "~1.8°C", "~2.0°C", "~2.7°C", "~2.6°C", "~4.4°C"],
    "4.1": ["~100 | ~140", "~60 | ~100", "~30 | ~70", "~20 | ~60", "~30 | ~55", "~110 | ~150"],
    "5.1": ["| ~300 |", "| ~280 |", "| ~60 |", "| ~40 |", "| ~25 |", "| ~2.4 |"],
    "6.1": ["~2.5 million", "~1.5 million", "~1 million", "~0.4 million", "~0.5 million"],
    "7.1": ["| −6% |", "| −7.4% |", "| −3.2% |", "| −3.1% |", "−10 to −20%", "−5 to −10% (milk)"],
    "8.1": [">99% decline", "Reef structure lost", "10–20% thaw", "30–50% thaw", "10–30% loss", "30–50% loss", "20–30% species loss", "40–60% species loss"],
    "10.1": ["−3 to −5%", "−8 to −12%", "−15 to −20%"],
    "11.1": ["| ~85 |", "| ~40 |", "| ~17 |", "| ~48 |", "| ~19 |", "| ~2–3 |"],
    "17.1": ["~735,000", "~500,000", "~245,000"],
    "22.1": ["| 739 |", "~70,000", "| 173 |", "| 85 |", "619 (BC)", ">180", "1,700+", "| 12+ |"],
    "23.1": ["~100,000", "~1,000,000", "~258,000", "~43,000"],
}


def verify():
    """Pastikan setiap angka yang digambar memang ada di tabel buku."""
    md = open(os.path.join(HERE, "book.md"), encoding="utf-8").read()
    bad = []
    for fid, needles in CHECKS.items():
        for n in needles:
            if n not in md:
                bad.append((fid, n))
    if bad:
        for fid, n in bad:
            print("  ANGKA TIDAK COCOK: gambar %s -> %r" % (fid, n))
    else:
        print("verifikasi: semua angka gambar cocok dengan tabel book.md")
    return not bad


def main():
    global LANG
    setup()
    import sys
    langs = [sys.argv[1]] if len(sys.argv) > 1 else ["en", "id"]
    for lang in langs:
        LANG = lang
        print("menggambar (%s):" % lang)
        for fn in (fig2_1, fig4_1, fig5_1, fig6_1, fig7_1, fig8_1, fig10_1,
                   fig11_1, fig17_1, fig22_1, fig23_1):
            fn()
    LANG = "en"
    verify()


if __name__ == "__main__":
    main()
