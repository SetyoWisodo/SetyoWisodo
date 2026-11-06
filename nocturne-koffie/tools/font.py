"""
Huruf lokal: dari keluarga variabel Google Fonts (OFL) ke woff2 yang dilayani sendiri.

Kenapa ada berkas ini
---------------------
Sampai 5 Nov 2026 ke-14 halaman memuat huruf dari `fonts.googleapis.com`. Itu
melanggar dua aturan kerja proyek: "tanpa CDN" dan "halaman awal < 1,5 MB tanpa
jaringan luar". Selain itu setiap halaman meminta potongan bobot yang berbeda
(600/700/800 di satu halaman, 600/800 di halaman lain), sehingga halaman yang
meminta bobot tidak tersedia mendapat huruf sintetis dari peramban.

Jalan keluarnya: satu berkas variabel per keluarga, diiris ke rentang bobot yang
benar-benar dipakai, lalu disajikan dari `assets/fonts/`. Empat berkas woff2
menggantikan 3 permintaan jaringan + 1 stylesheet pihak ketiga di tiap halaman.

Sumber berkas (lisensi OFL 1.1, teks lengkap: `assets/fonts/LISENSI.md`):
    github.com/google/fonts — ofl/inter, ofl/fraunces, ofl/bricolagegrotesque

Pemakaian
---------
    python3 tools/font.py            # unduh (bila belum ada), iris, tulis woff2 + fonts.css, pasang tautan
    python3 tools/font.py --cek      # periksa: tak ada CDN, berkas ada, tiap halaman memuat fonts.css

Unduhan memakai `gh api` (butuh `gh` yang sudah masuk) dan disimpan di
`/tmp/nocturne-fonts`, bukan di repo: berkas sumber 2 MB, tidak perlu ikut versi.
"""

from __future__ import annotations

import base64
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_DIR = os.path.join(ROOT, "assets", "fonts")
CSS = os.path.join(ROOT, "assets", "css", "fonts.css")
CACHE = os.path.join(tempfile.gettempdir(), "nocturne-fonts")

# Karakter yang dipakai situs: Latin dasar + Latin-1 + tanda baca tipografis +
# panah dan mata uang. Di luar ini, peramban memakai huruf sistem (tidak apa-apa
# untuk satu-dua glif aksidental).
UNICODE = (
    "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,"
    "U+2000-206F,U+20AC,U+2122,U+2190-2193,U+2212"
)

KELUARGA = [
    {
        "id": "bricolage",
        "nama": "Bricolage Grotesque",
        "gaya": "normal",
        "sumber": "ofl/bricolagegrotesque/BricolageGrotesque%5Bopsz%2Cwdth%2Cwght%5D.ttf",
        "sumber_terbaca": "ofl/bricolagegrotesque/BricolageGrotesque[opsz,wdth,wght].ttf",
        "pin": {"wdth": 100, "wght": (600, 800)},
        "berat": (600, 800),
        "keterangan": "judul: 600 label kecil, 700 subjudul, 800 hero",
    },
    {
        "id": "fraunces",
        "nama": "Fraunces",
        "gaya": "normal",
        "sumber": "ofl/fraunces/Fraunces%5BSOFT%2CWONK%2Copsz%2Cwght%5D.ttf",
        "sumber_terbaca": "ofl/fraunces/Fraunces[SOFT,WONK,opsz,wght].ttf",
        "pin": {"SOFT": 0, "WONK": 0, "wght": (300, 700)},
        "berat": (300, 700),
        "keterangan": "serif: 300 untuk kalimat pembuka, 400/700 untuk penekanan",
    },
    {
        "id": "fraunces-italic",
        "nama": "Fraunces",
        "gaya": "italic",
        "sumber": "ofl/fraunces/Fraunces-Italic%5BSOFT%2CWONK%2Copsz%2Cwght%5D.ttf",
        "sumber_terbaca": "ofl/fraunces/Fraunces-Italic[SOFT,WONK,opsz,wght].ttf",
        "pin": {"SOFT": 0, "WONK": 0, "wght": (300, 400)},
        "berat": (300, 400),
        "keterangan": "motto & kutipan: miring asli, bukan miring buatan peramban",
    },
    {
        "id": "newsreader",
        "nama": "Newsreader",
        "gaya": "normal",
        "sumber": "ofl/newsreader/Newsreader%5Bopsz%2Cwght%5D.ttf",
        "sumber_terbaca": "ofl/newsreader/Newsreader[opsz,wght].ttf",
        "pin": {"wght": 400},
        "berat": (400, 400),
        "keterangan": "judul katalog & sinopsis (rak sangrai)",
    },
    {
        "id": "newsreader-italic",
        "nama": "Newsreader",
        "gaya": "italic",
        "sumber": "ofl/newsreader/Newsreader-Italic%5Bopsz%2Cwght%5D.ttf",
        "sumber_terbaca": "ofl/newsreader/Newsreader-Italic[opsz,wght].ttf",
        "pin": {"wght": 400},
        "berat": (400, 400),
        "keterangan": "baris kredit miring (rak sangrai)",
    },
    {
        "id": "intertight",
        "nama": "Inter Tight",
        "gaya": "normal",
        "sumber": "ofl/intertight/InterTight%5Bwght%5D.ttf",
        "sumber_terbaca": "ofl/intertight/InterTight[wght].ttf",
        "pin": {"wght": (500, 600)},
        "berat": (500, 600),
        "keterangan": "label kecil, tab, tombol (rak sangrai)",
    },
    {
        "id": "inter",
        "nama": "Inter",
        "gaya": "normal",
        "sumber": "ofl/inter/Inter%5Bopsz%2Cwght%5D.ttf",
        "sumber_terbaca": "ofl/inter/Inter[opsz,wght].ttf",
        "pin": {"wght": (400, 700)},
        "berat": (400, 700),
        "keterangan": "teks isi: 400 paragraf, 500 tautan, 600 label, 700 tebal",
    },
]

HALAMAN_DILEWATI = ("biji-sangrai/", "film-studio/", "node_modules/")
# biji-sangrai memakai toko.css dengan @font-face ttf sendiri: berkas tunggalnya
# dibangun tools/luring.py yang hanya menyisipkan url(.ttf). Jangan dicampur.


def baca(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()


def tulis(path: str, teks: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(teks)


def unduh(entri: dict) -> str:
    """Ambil TTF variabel dari google/fonts lewat API GitHub; simpan di cache /tmp."""
    os.makedirs(CACHE, exist_ok=True)
    tujuan = os.path.join(CACHE, entri["id"] + ".ttf")
    if os.path.exists(tujuan) and os.path.getsize(tujuan) > 100_000:
        return tujuan
    perintah = [
        "gh", "api", f"repos/google/fonts/contents/{entri['sumber']}",
        "--jq", ".content",
    ]
    hasil = subprocess.run(perintah, capture_output=True, text=True)
    if hasil.returncode != 0:
        raise SystemExit(
            "gagal mengunduh %s — butuh `gh` yang sudah masuk.\n%s"
            % (entri["sumber_terbaca"], hasil.stderr.strip()[:400])
        )
    with open(tujuan, "wb") as f:
        f.write(base64.b64decode(hasil.stdout.strip()))
    return tujuan


def iris(entri: dict, sumber: str) -> str:
    """Kunci sumbu yang tak dipakai, batasi rentang bobot, iris glif, tulis woff2."""
    from fontTools.ttLib import TTFont
    from fontTools.varLib.instancer import instantiateVariableFont

    font = TTFont(sumber)
    ada = {a.axisTag for a in font["fvar"].axes} if "fvar" in font else set()
    pin = {k: v for k, v in entri["pin"].items() if k in ada}
    if pin:
        instantiateVariableFont(font, pin, inplace=True)
    antara = os.path.join(CACHE, entri["id"] + "-iris.ttf")
    font.save(antara)

    keluaran = os.path.join(FONT_DIR, entri["id"] + ".woff2")
    os.makedirs(FONT_DIR, exist_ok=True)
    perintah = [
        sys.executable, "-m", "fontTools.subset", antara,
        f"--unicodes={UNICODE}",
        "--layout-features=kern,liga,calt,ccmp,locl,mark,mkmk",
        "--no-hinting", "--flavor=woff2",
        f"--output-file={keluaran}",
    ]
    subprocess.run(perintah, check=True, capture_output=True)
    os.remove(antara)
    return keluaran


def tulis_css() -> None:
    baris = [
        "/* Huruf Nocturne Koffie — dilayani sendiri, tanpa CDN.",
        "   Dibangun oleh tools/font.py dari keluarga variabel Google Fonts (OFL 1.1).",
        "   Jangan sunting tangan: jalankan `python3 tools/font.py` untuk membangun ulang. */",
        "",
    ]
    for e in KELUARGA:
        a, b = e["berat"]
        bobot = f"{a} {b}" if a != b else f"{a}"
        baris += [
            "@font-face{",
            f'  font-family:"{e["nama"]}";',
            f'  src:url("../fonts/{e["id"]}.woff2") format("woff2");',
            f"  font-weight:{bobot};",
            f'  font-style:{e["gaya"]};',
            "  font-display:swap;",
            "}",
        ]
    tulis(CSS, "\n".join(baris) + "\n")


def halaman() -> list[str]:
    keluaran = []
    for akar, _, berkas in os.walk(ROOT):
        rel = os.path.relpath(akar, ROOT).replace(os.sep, "/")
        if rel != "." and any(rel.split("/")[0] == x.strip("/") for x in HALAMAN_DILEWATI):
            continue
        for b in berkas:
            if b.endswith(".html"):
                path = os.path.join(akar, b)
                if os.path.relpath(path, ROOT).replace(os.sep, "/") in ("semua.html",):
                    continue
                keluaran.append(path)
    return sorted(keluaran)


def pasang(cek_saja: bool = False) -> dict:
    """Ganti tautan Google Fonts dengan fonts.css lokal; idempoten."""
    laporan = {"diganti": [], "sudah": [], "dilewati": []}
    for path in halaman():
        teks = baca(path)
        rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
        dalam = os.path.relpath(os.path.dirname(path), ROOT).replace(os.sep, "/")
        awalan = "" if dalam == "." else "../" * dalam.count("/") + "../"
        if "fonts.googleapis.com" not in teks and "fonts.css" in teks:
            laporan["sudah"].append(rel)
            continue
        if "fonts.googleapis.com" not in teks:
            # halaman tanpa tautan Google (lembar brand, penawaran cetak): sisipkan saja
            if not cek_saja and "fonts.css" not in teks:
                sisip = (
                    f'<link rel="stylesheet" href="{awalan}assets/css/fonts.css" />'
                )
                teks = teks.replace("</head>", sisip + "\n</head>", 1)
                tulis(path, teks)
                laporan["diganti"].append(rel + " (disisipkan)")
            else:
                laporan["dilewati"].append(rel)
            continue
        if not cek_saja:
            # buang preconnect ke gstatic/googleapis
            teks = re.sub(
                r'[ \t]*<link[^>]*rel="preconnect"[^>]*fonts\.(googleapis|gstatic)\.com[^>]*>\s*\n?',
                "", teks)
            sisip = (
                f'<link rel="preload" href="{awalan}assets/fonts/bricolage.woff2" '
                'as="font" type="font/woff2" crossorigin />\n'
                f'<link rel="stylesheet" href="{awalan}assets/css/fonts.css" />'
            )
            teks = re.sub(
                r'[ \t]*<link[^>]*href="https://fonts\.googleapis\.com/css2[^>]*>\s*\n?',
                sisip + "\n", teks, count=1)
            tulis(path, teks)
        laporan["diganti"].append(rel)
    return laporan


def cek() -> list[str]:
    masalah = []
    for path in halaman():
        teks = baca(path)
        rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
        if "fonts.googleapis.com" in teks or "fonts.gstatic.com" in teks:
            masalah.append(f"{rel}: masih memuat huruf dari CDN")
        elif "fonts.css" not in teks:
            masalah.append(f"{rel}: tidak memuat fonts.css — huruf jatuh ke sistem")
    if not os.path.exists(CSS):
        masalah.append("assets/css/fonts.css tidak ada")
    else:
        for m in re.finditer(r'url\("\.\./fonts/([^"]+)"\)', baca(CSS)):
            berkas = os.path.join(FONT_DIR, m.group(1))
            if not os.path.exists(berkas) or os.path.getsize(berkas) < 20_000:
                masalah.append(f"berkas huruf hilang/terlalu kecil: {m.group(1)}")
    return masalah


def main() -> int:
    for e in KELUARGA:
        sumber = unduh(e)
        keluaran = iris(e, sumber)
        print(f"  {e['id']:<18} {os.path.getsize(keluaran)/1024:6.1f} KB · "
              f"bobot {e['berat'][0]}–{e['berat'][1]} · {e['gaya']}")
    tulis_css()
    total = sum(os.path.getsize(os.path.join(FONT_DIR, e["id"] + ".woff2")) for e in KELUARGA)
    print(f"  total huruf: {total/1024:.1f} KB · CSS: {os.path.getsize(CSS)} B")
    laporan = pasang()
    print(f"  halaman dipasang: {len(laporan['diganti'])} · sudah: {len(laporan['sudah'])} · "
          f"tanpa tautan Google: {len(laporan['dilewati'])}")
    masalah = cek()
    for m in masalah:
        print("  ✗", m)
    print("  kesimpulan:", "OK" if not masalah else f"{len(masalah)} masalah")
    return 0 if not masalah else 1


if __name__ == "__main__":
    if "--cek" in sys.argv:
        masalah = cek()
        for m in masalah:
            print("  ✗", m)
        print("  kesimpulan:", "OK · semua halaman memakai huruf lokal" if not masalah
              else f"{len(masalah)} masalah")
        sys.exit(0 if not masalah else 1)
    sys.exit(main())
