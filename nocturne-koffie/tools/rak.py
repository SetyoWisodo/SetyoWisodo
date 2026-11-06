"""
Rak Sangrai — dua atlas gambar untuk hero "shelf" bergaya VHS.

Kenapa ada berkas ini
---------------------
Halaman `rak/` memuat 12 kotak yang bisa berputar dalam 3D: 12 sampul di depan,
12 punggung di sisi. Kalau tiap kotak memakai berkas gambar sendiri, itu 24
permintaan jaringan + 24 berkas untuk dikelola. Solusinya sama seperti lembar
generator: **satu atlas per jenis**, lalu tiap kotak memotong bagiannya dengan
`background-position`. Jadi hanya 2 berkas.

Atlas dibangun deterministik dari `data/catalog.json`, bukan dari generator
gambar: hasilnya sama tiap dijalankan, angkanya bisa diperiksa, dan tidak ada
risiko bentuk biji salah. Seni yang dipakai adalah **potongan tengah poster
produk** yang sudah ada (`assets/img/produk/*.jpg`), diolah jadi dua tinta —
tinta gelap `#16110D` di atas kertas `#F2E9D8` — lalu digabung tipografi.

Geometri atlas sengaja memakai angka yang sama dengan lembar rujukan
(halaman contoh VHS): sampul 1744 × 2336 dengan 12 kotak 4 × 3, punggung
2688 × 1152 dengan 12 kotak sebaris. Dengan begitu rumus `background-size` /
`background-position` di JS berlaku apa adanya.

Pakai:
    python3 tools/rak.py            # tulis kedua atlas + rak/data.js
    python3 tools/rak.py --cek      # periksa atlas, potongan, dan angka katalog
"""

from __future__ import annotations

import json
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps, ImageStat

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets", "img", "rak")
DATA = os.path.join(ROOT, "rak", "data.js")
FONT = os.path.join(ROOT, "assets", "fonts")

# ---------------------------------------------------------------- geometri ---
COVERS = (1744, 2336)
SPINES = (2688, 1152)
# kotak sampul 4 x 3 (x, y, w, h) — sama dengan lembar rujukan
KOTAK_SAMPUL = [
    (74, 72, 347, 659), (497, 72, 344, 659), (914, 72, 342, 659), (1332, 72, 344, 659),
    (74, 813, 344, 676), (497, 815, 344, 674), (915, 815, 342, 675), (1331, 815, 345, 675),
    (74, 1571, 345, 681), (496, 1577, 343, 678), (913, 1579, 343, 676), (1331, 1579, 344, 677),
]
# kotak punggung: 12 kotak sebaris, tinggi & lebar seragam
SPINE_W, SPINE_H, SPINE_Y = 188, 1089, 31
SPINE_X0, SPINE_STEP = 36, 212
KOTAK_PUNGGUNG = [
    (SPINE_X0 + i * SPINE_STEP, SPINE_Y, SPINE_W, SPINE_H) for i in range(12)
]

KERTAS = (242, 233, 216)
TINTA = (22, 17, 13)
KOBALT = (31, 63, 176)
MERAH = (200, 62, 40)

# ------------------------------------------------------------------- muat ----
def muat_katalog() -> dict:
    with open(os.path.join(ROOT, "data", "catalog.json"), encoding="utf-8") as f:
        return json.load(f)


def baris_tab(kind: str) -> str:
    if kind == "Arabika":
        return "arabika"
    if kind == "Robusta":
        return "robusta"
    if kind == "Excelsa":
        return "excelsa"
    return "racikan"


def siapkan_item(kat: dict) -> list[dict]:
    """12 kotak: 9 kopi + 2 paket + kartu member, urut nomor katalog."""
    item: list[dict] = []
    for p in kat["products"]:
        v = p["variants"][0]
        besaran = " · ".join(f'{x["weight"]} Rp{x["price"]:,}'.replace(",", ".") for x in p["variants"])
        item.append({
            "id": p["id"],
            "no": p["no"],
            "name": p["name"],
            "line": f'{p["region"].upper()} · {p["process"].upper()}',
            "meta": f'{p["elevation"]} · {p["kind"].upper()} · SANGGAI {p["roast_level"]}/5',
            "kind": p["kind"],
            "tab": baris_tab(p["kind"]),
            "notes": p["notes"],
            "farmer": p["farmer"],
            "status": p["status"],
            "sumber": "katalog",
            "harga": v["price"],
            "harga_teks": f'Rp{v["price"]:,}'.replace(",", "."),
            "ukuran": " · ".join(x["weight"] for x in p["variants"]),
            "ukuran_teks": besaran,
            "synopsis": (
                f'{p["name"]} dari {p["region"]}, {p["elevation"]}, proses {p["process"]}.'
                + ("" if "belum" in p["variety"].lower() else f' Varietas {p["variety"]}.')
                + f' Petani {p["farmer"]}. Catatan rasa '
                  f'{", ".join(x.lower() for x in p["notes"])}.'
            ),
            "art": p["img"],
        })
    for b in kat["bundles"]:
        item.append({
            "id": b["id"],
            "no": b["no"],
            "name": b["name"],
            "line": f'PAKET · {b["contents"].upper()}',
            "meta": f'{b["contents"]} · HEMAT Rp{b["price_normal"] - b["price"]:,}'.replace(",", "."),
            "kind": "Paket",
            "tab": "racikan",
            "notes": [],
            "farmer": "",
            "status": b["status"],
            "sumber": "katalog",
            "harga": b["price"],
            "harga_teks": f'Rp{b["price"]:,}'.replace(",", "."),
            "ukuran": b["contents"],
            "ukuran_teks": f'Normal Rp{b["price_normal"]:,}'.replace(",", "."),
            "synopsis": b["desc"],
            "art": b["img"],
        })
    m = kat["member"]
    item.append({
        "id": "circle",
        "no": "12",
        "name": "Nocturne Circle",
        "line": "KARTU MEMBER · TANPA AKUN",
        "meta": "DAFTAR SEKALI · KODE LEWAT EMAIL",
        "kind": "Member",
        "tab": "racikan",
        "notes": [],
        "farmer": "",
        "status": "tersedia",
        "sumber": "katalog › member",
        "harga": 0,
        "harga_teks": "Gratis",
        "ukuran": "Kartu digital",
        "ukuran_teks": m["intro"],
        "synopsis": " ".join(s["text"] for s in m["steps"]),
        "art": "",
    })
    return item


# ------------------------------------------------------------------ warna ----
def warna_aksen(path: str) -> tuple[int, int, int]:
    """Ambil satu warna paling pekat dari potongan seni poster."""
    im = Image.open(os.path.join(ROOT, path)).convert("RGB").crop((60, 60, 700, 620))
    kecil = im.resize((80, 70))
    hasil = kecil.quantize(colors=6, method=Image.Quantize.MEDIANCUT).convert("RGB")
    terbaik, skor = (200, 60, 40), -1
    for jumlah, (r, g, b) in hasil.getcolors():
        mx, mn = max(r, g, b), min(r, g, b)
        jenuh = (mx - mn) / 255
        terang = (r + g + b) / 765
        s = jenuh * 1.0 + (1 - abs(terang - 0.45)) * 0.25 + min(jumlah / 4000, 0.4)
        if s > skor:
            skor, terbaik = s, (r, g, b)
    return terbaik


def dua_tinta(im: Image.Image, aksen: tuple[int, int, int]) -> Image.Image:
    """Peta terang-gelap ke dua tinta: tinta gelap → aksen → kertas."""
    abu = ImageOps.grayscale(im)
    abu = ImageOps.autocontrast(abu, cutoff=1)
    # tiga titik: gelap = TINTA, tengah = aksen, terang = KERTAS
    r = abu.point(lambda v: int(TINTA[0] + (aksen[0] - TINTA[0]) * (v / 128)) if v < 128
                  else int(aksen[0] + (KERTAS[0] - aksen[0]) * ((v - 128) / 127)))
    g = abu.point(lambda v: int(TINTA[1] + (aksen[1] - TINTA[1]) * (v / 128)) if v < 128
                  else int(aksen[1] + (KERTAS[1] - aksen[1]) * ((v - 128) / 127)))
    b = abu.point(lambda v: int(TINTA[2] + (aksen[2] - TINTA[2]) * (v / 128)) if v < 128
                  else int(aksen[2] + (KERTAS[2] - aksen[2]) * ((v - 128) / 127)))
    return Image.merge("RGB", (r, g, b))


def butir(im: Image.Image, kuat: float = 0.05) -> Image.Image:
    """Derau halus supaya terasa dicetak, bukan render."""
    n = Image.effect_noise(im.size, 26).convert("L")
    n = n.filter(ImageFilter.GaussianBlur(0.4))
    noise = Image.merge("RGB", (n, n, n))
    return Image.blend(im, Image.blend(im, noise, 0.5), kuat)


def font(nama: str, ukuran: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(os.path.join(FONT, nama), ukuran)


def tengah(d: ImageDraw.ImageDraw, xy, teks, f, isi=TINTA, spasi: float = 0.0):
    """Tulis teks dengan jarak huruf manual (Pillow tidak punya letter-spacing)."""
    if not spasi:
        d.text(xy, teks, font=f, fill=isi, anchor="mm")
        return
    lebar = sum(d.textlength(c, font=f) + spasi for c in teks) - spasi
    x = xy[0] - lebar / 2
    for c in teks:
        d.text((x, xy[1]), c, font=f, fill=isi, anchor="lm")
        x += d.textlength(c, font=f) + spasi


# -------------------------------------------------------------- sampul ------
def potong_seni(path: str, ukuran: tuple[int, int]) -> Image.Image:
    im = Image.open(os.path.join(ROOT, path)).convert("RGB")
    # hanya pita ilustrasi poster (lingkaran + gunung), tanpa bingkai & judul poster:
    # judul besar di dalam seni akan bertabrakan dengan judul kotak
    sisa = im.crop((118, 205, 642, 560))
    return ImageOps.fit(sisa, ukuran, Image.LANCZOS, centering=(0.5, 0.5))


def gambar_sampul(item: dict, ukuran: tuple[int, int], aksen, ukuran_judul: int) -> Image.Image:
    """Sampul 1 : 1,9 — seni dua tinta di atas, judul serif, pita kobalt di bawah."""
    w, h = ukuran
    S = 2                                            # supersample
    W, H = w * S, h * S
    im = Image.new("RGB", (W, H), KERTAS)
    d = ImageDraw.Draw(im)
    pad = int(W * 0.045)

    # --- seni di bagian atas
    seni_h = int(H * 0.50)
    if item["art"]:
        seni = dua_tinta(potong_seni(item["art"], (W - 2 * pad, seni_h)), aksen)
    else:
        seni = Image.new("RGB", (W - 2 * pad, seni_h), KERTAS)
        ds = ImageDraw.Draw(seni)
        r = int(seni_h * 0.34)
        ds.ellipse([seni.width // 2 - r, seni_h // 2 - r, seni.width // 2 + r, seni_h // 2 + r],
                   fill=aksen)
        ds.ellipse([seni.width // 2 - r // 3, seni_h // 2 - r // 3,
                    seni.width // 2 + r // 3, seni_h // 2 + r // 3], fill=KERTAS)
    im.paste(seni, (pad, int(H * 0.085)))
    d.rectangle([pad, int(H * 0.085), W - pad, int(H * 0.085) + seni_h], outline=TINTA, width=max(1, S))

    # --- kepala
    tengah(d, (W // 2, int(H * 0.045)), "A NOCTURNE KOFFIE LOT", font("intertight.woff2", int(H * 0.019)),
           TINTA, spasi=H * 0.004)
    # --- judul
    judul = item["name"].upper()
    f_judul = font("fraunces.woff2", ukuran_judul)
    tengah(d, (W // 2, int(H * 0.635)), judul, f_judul, TINTA, spasi=-H * 0.001)

    # --- garis + baris asal
    y = int(H * 0.685)
    d.line([pad * 2, y, W - pad * 2, y], fill=TINTA, width=max(1, S))
    tengah(d, (W // 2, y + int(H * 0.032)), item["line"], font("intertight.woff2", int(H * 0.0175)),
           TINTA, spasi=H * 0.0035)

    # --- catatan rasa (kopi saja)
    if item["notes"]:
        tengah(d, (W // 2, y + int(H * 0.062)), " · ".join(n.upper() for n in item["notes"]),
               font("intertight.woff2", int(H * 0.016)), TINTA, spasi=H * 0.003)

    # --- pita bawah
    yb = int(H * 0.795)
    d.rectangle([0, yb, W, H], fill=TINTA)
    warna_pita = aksen if sum(aksen) > 210 else KERTAS
    tengah(d, (pad + (W - 2 * pad) * 0.21, yb + int(H * 0.060)), "NOCTURNE", font("fraunces.woff2", int(H * 0.032)),
           warna_pita, spasi=H * 0.002)
    tengah(d, (pad + (W - 2 * pad) * 0.28, yb + int(H * 0.112)), "KOFFIE · BANYUWANGI",
           font("intertight.woff2", int(H * 0.0135)), KERTAS, spasi=H * 0.0022)
    badge = "PAKET" if item["kind"] == "Paket" else ("MEMBER" if item["kind"] == "Member" else "250 G")
    bw, bh = int(W * 0.28), int(H * 0.062)
    bx, by = W - pad - bw, yb + int(H * 0.045)
    d.rectangle([bx, by, bx + bw, by + bh], outline=KERTAS, width=max(1, S))
    tengah(d, (bx + bw / 2, by + bh / 2), badge, font("intertight.woff2", int(H * 0.027)), KERTAS, spasi=H * 0.0035)
    tengah(d, (bx + bw / 2, by + bh + int(H * 0.032)), f'LOT {item["no"]}',
           font("intertight.woff2", int(H * 0.0165)), KERTAS, spasi=H * 0.003)

    # --- aus: hanya derau halus di bawah (goresan garis terbaca sebagai artefak)
    im = im.filter(ImageFilter.GaussianBlur(0.4))
    im = butir(im, 0.055)
    return im.resize((w, h), Image.LANCZOS)


# ------------------------------------------------------------- punggung ------
def gambar_punggung(item: dict, ukuran: tuple[int, int], aksen, ukuran_judul: int) -> Image.Image:
    """Punggung 1 : 5,8. Digambar mendatar (judul bisa dibaca), lalu diputar 90°.

    Mendatar: [ilustrasi persegi][judul serif][blok tinta: brand + badge].
    Setelah diputar, judul terbaca tegak seperti punggung kaset.
    """
    w, h = ukuran
    S = 2
    w, h = w * S, h * S
    Wl, Hl = h, w                     # kanvas mendatar: panjang = tinggi punggung
    dasar = tuple(int(KERTAS[i] * 0.93 + aksen[i] * 0.07) for i in range(3))
    im = Image.new("RGB", (Wl, Hl), dasar)
    d = ImageDraw.Draw(im)

    # --- ilustrasi di ujung kanan (setelah diputar 90° jadi ujung atas)
    sisi = Hl
    if item["art"]:
        kecil = dua_tinta(potong_seni(item["art"], (sisi, sisi)), aksen)
    else:
        kecil = Image.new("RGB", (sisi, sisi), dasar)
        dk = ImageDraw.Draw(kecil)
        r = int(sisi * 0.30)
        dk.ellipse([sisi // 2 - r, sisi // 2 - r, sisi // 2 + r, sisi // 2 + r], fill=aksen)
        dk.ellipse([sisi // 2 - r // 3, sisi // 2 - r // 3,
                    sisi // 2 + r // 3, sisi // 2 + r // 3], fill=KERTAS)
    im.paste(kecil, (Wl - sisi, 0))
    d.rectangle([Wl - sisi, 0, Wl - 1, Hl - 1], outline=TINTA, width=max(1, S))

    # --- judul
    blok = int(Wl * 0.27)
    ruang = Wl - sisi - blok
    geser = blok
    f = font("fraunces.woff2", ukuran_judul)
    judul = item["name"].upper()
    spasi = Hl * 0.03
    lebar = sum(d.textlength(c, font=f) + spasi for c in judul) - spasi
    x = geser + (ruang - lebar) / 2
    for c in judul:
        d.text((x, Hl * 0.52), c, font=f, fill=TINTA, anchor="lm")
        x += d.textlength(c, font=f) + spasi

    # --- blok tinta di ujung kiri kanvas → ujung bawah punggung sesudah diputar
    B = int(Wl * 0.27)
    d.rectangle([0, 0, B - 1, Hl - 1], fill=TINTA)
    cx = B / 2
    tengah(d, (cx, Hl * 0.28), "NOCTURNE", font("intertight.woff2", int(Hl * 0.175)), KERTAS, spasi=Hl * 0.012)
    tengah(d, (cx, Hl * 0.52), "BANYUWANGI", font("intertight.woff2", int(Hl * 0.135)), KERTAS, spasi=Hl * 0.012)
    badge = "PKT" if item["kind"] == "Paket" else ("MBR" if item["kind"] == "Member" else "250G")
    bw, bh = B * 0.62, Hl * 0.24
    bx, by = cx - bw / 2, Hl * 0.70
    d.rectangle([bx, by, bx + bw, by + bh], outline=KERTAS, width=max(1, S))
    tengah(d, (cx, by + bh / 2), badge, font("intertight.woff2", int(Hl * 0.125)), KERTAS, spasi=Hl * 0.008)

    im = im.rotate(90, expand=True)   # mendatar → tegak (judul terbaca dari atas ke bawah)
    im = im.filter(ImageFilter.GaussianBlur(0.3))
    im = butir(im, 0.06)
    return im.resize((w // S, h // S), Image.LANCZOS)


# ------------------------------------------------------------------ tulis ----
def data_js(item: list[dict]) -> str:
    peta_sampul = {it["id"]: KOTAK_SAMPUL[i] for i, it in enumerate(item)}
    peta_punggung = {it["id"]: KOTAK_PUNGGUNG[i] for i, it in enumerate(item)}
    crop = {}
    for it in item:
        crop[f'cover-{it["id"]}'] = ["covers", *peta_sampul[it["id"]]]
        crop[f'spine-{it["id"]}'] = ["spines", *peta_punggung[it["id"]]]
    ringkas = []
    for it in item:
        ringkas.append({k: it[k] for k in (
            "id", "no", "name", "line", "meta", "kind", "tab", "notes", "farmer",
            "status", "harga", "harga_teks", "ukuran", "ukuran_teks", "synopsis")})
    tab = [
        {"id": "semua", "label": "SEMUA", "sub": "semua lot"},
        {"id": "arabika", "label": "ARABIKA", "sub": "4 lot"},
        {"id": "robusta", "label": "ROBUSTA", "sub": "2 lot"},
        {"id": "excelsa", "label": "EXCELSA", "sub": "1 lot"},
        {"id": "racikan", "label": "RACIKAN", "sub": "blend · paket"},
    ]
    isi = {
        "SHEET": {
            "covers": ["../assets/img/rak/covers.webp", *COVERS],
            "spines": ["../assets/img/rak/spines.webp", *SPINES],
        },
        "CROP": crop,
        "ITEMS": ringkas,
        "TABS": tab,
        "START": 5,
    }
    baris = ",\n".join(f'  {json.dumps(k)}: {json.dumps(v, ensure_ascii=False)}' for k, v in isi.items())
    return ("/* Rak sangrai — data untuk hero rak (dibangun tools/rak.py dari data/catalog.json).\n"
            "   Jangan sunting tangan: angka, harga, dan potongan gambar berasal dari katalog. */\n"
            "window.RAK = {\n" + baris + "\n};\n")


def bangun() -> None:
    kat = muat_katalog()
    item = siapkan_item(kat)
    assert len(item) == 12, f"butuh 12 kotak, dapat {len(item)}"
    os.makedirs(IMG, exist_ok=True)
    os.makedirs(os.path.dirname(DATA), exist_ok=True)

    # satu ukuran judul untuk kedua atlas: ukuran yang muat untuk nama terpanjang,
    # dipakai semua kotak (kolom ukuran tidak boleh berbeda-beda antar kotak)
    ukur = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    nama = [it["name"].upper() for it in item]
    w_sampul = KOTAK_SAMPUL[0][2] * 2
    uk_sampul = int(KOTAK_SAMPUL[0][3] * 2 * 0.083)
    while max(ukur.textlength(n, font=font("fraunces.woff2", uk_sampul)) for n in nama) > w_sampul * 0.86:
        uk_sampul = int(uk_sampul * 0.96)
    hl = KOTAK_PUNGGUNG[0][3] * 2            # tinggi punggung = lebar kanvas mendatar
    ruang_p = hl * (1 - SPINE_W * 2 / hl) if False else hl * (1 - 0.27) - SPINE_W * 2
    uk_punggung = int(hl * 0.42)
    jarak_p = SPINE_W * 2 * 0.03
    while max(sum(ukur.textlength(c, font=font("fraunces.woff2", uk_punggung)) + jarak_p for c in n) - jarak_p
              for n in nama) > ruang_p * 0.92:
        uk_punggung = int(uk_punggung * 0.96)

    # --- atlas sampul
    lembar = Image.new("RGB", COVERS, KERTAS)
    for i, it in enumerate(item):
        aksen = warna_aksen(it["art"]) if it["art"] else KOBALT
        it["_aksen"] = aksen
        x, y, w, h = KOTAK_SAMPUL[i]
        lembar.paste(gambar_sampul(it, (w, h), aksen, uk_sampul), (x, y))
    jalur = os.path.join(IMG, "covers.webp")
    lembar.save(jalur, "WEBP", quality=80, method=6)

    # --- atlas punggung
    lembar2 = Image.new("RGB", SPINES, (236, 227, 210))
    for i, it in enumerate(item):
        x, y, w, h = KOTAK_PUNGGUNG[i]
        lembar2.paste(gambar_punggung(it, (w, h), it["_aksen"], uk_punggung), (x, y))
    jalur2 = os.path.join(IMG, "spines.webp")
    lembar2.save(jalur2, "WEBP", quality=80, method=6)

    with open(DATA, "w", encoding="utf-8") as f:
        f.write(data_js(item))

    print(f"  covers.webp  {COVERS[0]}×{COVERS[1]} · {os.path.getsize(jalur)/1024:.0f} KB")
    print(f"  spines.webp  {SPINES[0]}×{SPINES[1]} · {os.path.getsize(jalur2)/1024:.0f} KB")
    print(f"  rak/data.js  {os.path.getsize(DATA)/1024:.1f} KB · 12 kotak · "
          f"{len({it['tab'] for it in item})} tab")
    for it in item:
        print(f"    {it['no']} {it['id']:<16} {it['name']:<17} aksen {it['_aksen']}")


def cek() -> list[str]:
    masalah = []
    kat = muat_katalog()
    item = siapkan_item(kat)
    for nama, ukuran in (("covers.webp", COVERS), ("spines.webp", SPINES)):
        p = os.path.join(IMG, nama)
        if not os.path.exists(p):
            masalah.append(f"{nama} belum ada — jalankan tools/rak.py")
            continue
        im = Image.open(p)
        if im.size != ukuran:
            masalah.append(f"{nama} {im.size} ≠ {ukuran}")
        if os.path.getsize(p) > 900_000:
            masalah.append(f"{nama} {os.path.getsize(p)/1024:.0f} KB terlalu berat")
    if not os.path.exists(DATA):
        masalah.append("rak/data.js belum ada")
    else:
        teks = open(DATA, encoding="utf-8").read()
        for it in item:
            if f'"cover-{it["id"]}"' not in teks or f'"spine-{it["id"]}"' not in teks:
                masalah.append(f'potongan {it["id"]} tidak ada di data.js')
            if it["harga_teks"] not in teks:
                masalah.append(f'harga {it["id"]} ({it["harga_teks"]}) tidak ada di data.js')
        # tiap kotak harus di dalam batas atlas
        crop = json.loads(teks[teks.index("{"):teks.rindex("}") + 1]) if False else None
        for kunci, kotak in [("sampul", KOTAK_SAMPUL), ("punggung", KOTAK_PUNGGUNG)]:
            W, H = COVERS if kunci == "sampul" else SPINES
            for i, (x, y, w, h) in enumerate(kotak):
                if x + w > W or y + h > H:
                    masalah.append(f"kotak {kunci} #{i} keluar dari atlas")
                for j in range(i):
                    x2, y2, w2, h2 = kotak[j]
                    if x < x2 + w2 and x2 < x + w and y < y2 + h2 and y2 < y + h:
                        masalah.append(f"kotak {kunci} #{i} menimpa #{j}")
    return masalah


if __name__ == "__main__":
    if "--cek" in sys.argv:
        m = cek()
        for x in m:
            print("  ✗", x)
        print("  kesimpulan:", "OK" if not m else f"{len(m)} masalah")
        sys.exit(0 if not m else 1)
    bangun()
    m = cek()
    for x in m:
        print("  ✗", x)
    sys.exit(0 if not m else 1)
