"""
Cutaway Nocturne — ukur acuan, tulis ceklis, siapkan data untuk halaman potong-buka.

Metode ini diadaptasi dari skill **Cutaway** (Nyxera0x, MIT —
github.com/Nyxera0x/cutaway): satu gambar acuan → objek dibangun dari kode →
dibuka bagian demi bagian di depan kamera → diperiksa dengan ceklis bernomor.

Batasan yang diukur, bukan dikira — ada di README dan di laporan:

    tahap metode                      status di proyek ini
    --------------------------------  ------------------------------------------
    ukur acuan (proporsi, tinta)      YA · Pillow, angka masuk data
    ceklis 10–12 baris bernomor       YA · laporan/cutaway-checklist.md
    objek dibangun dari kode          YA · CSS 3D, tanpa WebGL, tanpa pustaka
    satu kamera per ketukan           YA · 9 ketukan, 9 kamera berbeda
    render(t) murni                   YA · semua dari t, tanpa Math.random/Date
    film 60 fps (Playwright + ffmpeg) TIDAK · sandbox tanpa Chromium & ffmpeg
    skor prosedural (Python)          TIDAK · hanya timeline yang ditulis

Pakai:
    python3 tools/cutaway.py          # ukur + tulis data + ceklis
    python3 tools/cutaway.py --cek    # periksa angka vs citra acuan
"""

from __future__ import annotations

import json
import os
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ACUAN = os.path.join(ROOT, "brand", "label-blue-mount-ijen.png")
DATA_JS = os.path.join(ROOT, "cutaway", "data.js")
LAPORAN = os.path.join(ROOT, "laporan", "cutaway-checklist.md")

AMBANG_GELAP = 80          # luma di bawah ini dihitung "tinta"

# Ketukan: satu bagian per ketukan, 2–3 s, sampul & tutup di kedua ujung.
KETUKAN = [
    ("hero", None, 0.0, 2.0),
    ("badan", "badan", 2.0, 5.0),
    ("punggung", "punggung", 5.0, 8.0),
    ("katup", "katup", 8.0, 11.0),
    ("segel", "segel", 11.0, 14.0),
    ("sisi", "sisi", 14.0, 17.0),
    ("biji", "biji", 17.0, 20.0),
    ("stiker", "stiker", 20.0, 23.0),
    ("tutup", None, 23.0, 25.0),
]
# Bagian yang ikut terbuka saat ketukan bagian lain — panel depan disingkirkan
# supaya isi sangrai benar-benar kelihatan, bukan tertutup.
BUKA_LAGI = {"biji": ["badan"]}


def ukur(path: str) -> dict:
    """Ukur acuan: rasio, tinta total, tinta per pita, aksen."""
    im = Image.open(path).convert("RGB")
    W, H = im.size
    abu = im.convert("L")
    data = abu.tobytes()
    gelap = sum(1 for v in data if v < AMBANG_GELAP) / len(data)
    pita = []
    for i in range(3):
        y0, y1 = int(H * i / 3), int(H * (i + 1) / 3)
        d = abu.crop((0, y0, W, y1)).tobytes()
        pita.append(round(sum(1 for v in d if v < AMBANG_GELAP) / len(d), 3))
    # aksen: piksel jenuh — dipakai untuk warna sorot di halaman
    aksen = 0
    for i in range(0, W * H, 97):
        r, g, b = im.getpixel(((i * 7) % W, (i * 13) % H))
        if max(r, g, b) - min(r, g, b) > 70:
            aksen += 1
    aksen_share = round(aksen / (W * H // 97), 3)
    return {
        "berkas": os.path.relpath(path, ROOT).replace(os.sep, "/"),
        "lebar": W, "tinggi": H,
        "rasio": round(W / H, 4),
        "gelap": round(gelap, 3),
        "gelap_per_pita": pita,
        "aksen": aksen_share,
    }


def bagian(u: dict) -> list[dict]:
    """Tujuh bagian kemasan. 100 satuan = lebar depan.

    Yang bisa diturunkan dari acuan diturunkan (rasio, tinggi); yang merupakan
    keputusan desain ditandai `asal: "desain"` supaya tidak ada angka yang
    mengaku "terukur" padahal bukan.
    """
    t = round(100 / u["rasio"], 2)   # tinggi bidang depan, satuan
    dasar = {
        "wajah": "kertas", "pos": [0, 0, 0], "arah": [0, 0, 60],
        "muka_ry": 0, "muka_rx": 0, "putar": 0, "jarak": 40, "kembar": False,
        "asal": "desain",
    }

    def b(**k):
        x = dict(dasar)
        x.update(k)
        return x

    return [
        b(id="badan", nama="Badan kemasan", peran="Bidang depan",
          wajah="label", w=100, h=t, pos=[0, 0, 0], arah=[96, 0, 26],
          jarak=38, putar=-30, asal="rasio acuan",
          spesifikasi="Kertas matte 120 gsm, cetak dua sisi",
          catatan=f'rasio acuan {u["rasio"]} → tinggi {t} satuan'),
        b(id="punggung", nama="Punggung", peran="Sisi belakang",
          w=100, h=t, pos=[0, 0, -9], muka_ry=180, arah=[0, 0, -70],
          jarak=62, putar=-38,
          spesifikasi="Info seduh, asal lot, kode batch",
          catatan="tebal kemasan 9 satuan; dibuka karena kamera berpindah ke belakang"),
        b(id="sisi", nama="Lipatan samping", peran="Gusset kiri & kanan",
          wajah="sisi", w=18, h=t, pos=[48, 0, 0], muka_ry=90,
          kembar=True, arah=[96, 0, 0], jarak=52, putar=-40,
          spesifikasi="Lipatan 18 satuan, dua lapis",
          catatan="dua bidang kembar, ±48 satuan dari tengah"),
        b(id="segel", nama="Segel atas", peran="Penutup kedap",
          wajah="segel", w=100, h=7, pos=[0, round(-t / 2, 2), 0],
          muka_rx=-62, arah=[0, -84, 0], jarak=46, putar=-34,
          spesifikasi="Segel panas 7 satuan + zipper",
          catatan="dibuka sekali, ditutup lagi dengan zipper"),
        b(id="katup", nama="Katup aroma", peran="Satu arah",
          wajah="katup", w=17, h=17, pos=[26, round(-t * 0.3, 2), 3],
          arah=[30, 0, 84], jarak=58, putar=26,
          spesifikasi="Katup silikon 17 satuan, satu arah",
          catatan="melepas CO₂ tanpa memasukkan udara"),
        b(id="biji", nama="Isi sangrai", peran="Biji di dalam",
          wajah="biji", w=70, h=46, pos=[0, 6, -4],
          arah=[0, 24, 90], jarak=30, putar=0,
          spesifikasi="250 g · sangrai 2/5 · Blue Mount Ijen",
          catatan="tujuh biji 7 × 10 satuan, tampil setelah panel depan disingkirkan"),
        b(id="stiker", nama="Stiker lot", peran="Tanggal & kode",
          wajah="stiker", w=34, h=13, pos=[-24, round(t * 0.2, 2), 4],
          arah=[-34, 22, 58], jarak=66, putar=22,
          spesifikasi="Stiker 34×13 satuan, tinta hitam",
          catatan="tanggal sangrai + kode lot, ditempel tangan"),
    ]


def kamera() -> dict:
    """Satu kamera per ketukan — tidak boleh ada angka yang sama di dua ketukan."""
    return {
        "hero":     {"ry": -26, "rx": 8,  "zoom": 1.00, "ty": 0},
        "badan":    {"ry": -8,  "rx": 2,  "zoom": 1.16, "ty": 0},
        "punggung": {"ry": 150, "rx": 6,  "zoom": 1.12, "ty": 0},
        "katup":    {"ry": 18,  "rx": -6, "zoom": 1.34, "ty": -22},
        "segel":    {"ry": 26,  "rx": 22, "zoom": 1.28, "ty": 26},
        "sisi":     {"ry": 52,  "rx": 6,  "zoom": 1.10, "ty": 0},
        "biji":     {"ry": -44, "rx": 14, "zoom": 1.22, "ty": 0},
        "stiker":   {"ry": -14, "rx": -8, "zoom": 1.40, "ty": 20},
        "tutup":    {"ry": -30, "rx": 10, "zoom": 1.05, "ty": -4},
    }


def ceklis(u: dict, b: list[dict]) -> list[str]:
    """Ceklis 12 baris; setiap kata kabur diberi angka (aturan metode)."""
    t = round(100 / u["rasio"], 2)
    return [
        f'1. Siluet & sudut: kemasan tegak, bidang depan 100 × {t} satuan '
        f'(rasio acuan {u["rasio"]} dari {u["berkas"]}), sampul 3/4 dari kiri.',
        '2. Ciri utama: stiker lot 34 × 13 satuan di kiri-bawah, 4 satuan di depan '
        'permukaan — bukan melayang, bukan rata.',
        f'3. Tinta: {u["gelap"]*100:.1f}% piksel acuan di bawah luma {AMBANG_GELAP}. '
        f'Pita atas {u["gelap_per_pita"][0]*100:.1f}%, tengah {u["gelap_per_pita"][1]*100:.1f}%, '
        f'bawah {u["gelap_per_pita"][2]*100:.1f}% — massa gelap tetap di pita bawah.',
        '4. Katup aroma: satu cakram 17 satuan di kanan-atas, NEVER dua atau lebih.',
        '5. Segel atas: pita 7 satuan selebar badan, NEVER lebih tipis dari 5 satuan.',
        '6. Lipatan samping: 2 bidang 18 satuan di ±48, keduanya terbuka bersamaan.',
        '7. Isi: 7 biji 7 × 10 satuan, muncul setelah panel depan bergeser 38 satuan.',
        '8. Warna: satu aksen (kobalt) menandai bagian yang sedang bergerak; sisanya '
        'kertas + tinta.',
        '9. Tidak ada bidang yang menembus bidang lain; setiap bagian kembali ke '
        'tempatnya dengan selisih 0 satuan.',
        '10. Kamera: 9 ketukan, 9 sudut berbeda (zoom 1,00–1,40; ry −44°…150°) — '
        'NEVER dua ketukan memakai kamera yang sama.',
        '11. Waktu: bagian terbuka 1,0 s, tahan, menutup 0,55 s; ketukan baru tiap 2–3 s; '
        'film 25 s.',
        f'12. Kepadatan: luas tinta model ≥ 0,8 × acuan '
        f'({u["gelap"]*100:.1f}% × 0,8 = {u["gelap"]*80:.1f}%).',
    ]


def tulis(ukur_: dict, parts: list[dict], kam: dict, cek: list[str]) -> None:
    os.makedirs(os.path.dirname(DATA_JS), exist_ok=True)
    isi = {
        "UKUR": ukur_,
        "BAGIAN": parts,
        "KAMERA": kam,
        "KETUKAN": [{"id": k[0], "bagian": k[1], "mulai": k[2], "selesai": k[3],
                     "bukaLagi": BUKA_LAGI.get(k[0], [])} for k in KETUKAN],
        "DURASI": KETUKAN[-1][3],
        "CEKLIS": cek,
    }
    baris = ",\n".join(f"  {json.dumps(k)}: {json.dumps(v, ensure_ascii=False)}" for k, v in isi.items())
    with open(DATA_JS, "w", encoding="utf-8") as f:
        f.write("/* Cutaway Nocturne — data potong-buka (dibangun tools/cutaway.py).\n"
                "   Angka ukur berasal dari citra acuan; bagian & kamera adalah keputusan\n"
                "   desain dan ditandai. Jangan sunting tangan. */\n"
                "window.CUTAWAY = {\n" + baris + "};\n")

    baris_md = ["# Ceklis Cutaway — kemasan Blue Mount Ijen", "",
                f'Acuan: `{ukur_["berkas"]}` ({ukur_["lebar"]}×{ukur_["tinggi"]} px). '
                "Metode: skill **Cutaway** (Nyxera0x, MIT).", "",
                "Angka ditulis sebelum satu baris kode halaman, lalu diukur ulang oleh "
                "`tools/cutaway.py --cek` dan `tools/cutaway-uji.mjs`.", ""]
    baris_md += cek
    baris_md += ["", "## Ukur ulang", "```bash", "python3 tools/cutaway.py --cek",
                 "node tools/cutaway-uji.mjs", "```"]
    with open(LAPORAN, "w", encoding="utf-8") as f:
        f.write("\n".join(baris_md) + "\n")


def cek() -> list[str]:
    m = []
    if not os.path.exists(DATA_JS):
        return ["cutaway/data.js belum ada — jalankan tools/cutaway.py"]
    teks = open(DATA_JS, encoding="utf-8").read()
    obj = json.loads(teks[teks.index("{"):teks.rindex("}") + 1])
    u_baru = ukur(ACUAN)
    if abs(obj["UKUR"]["rasio"] - u_baru["rasio"]) > 0.01:
        m.append(f'rasio di data.js {obj["UKUR"]["rasio"]} ≠ terukur {u_baru["rasio"]}')
    if abs(obj["UKUR"]["gelap"] - u_baru["gelap"]) > 0.02:
        m.append(f'tinta di data.js {obj["UKUR"]["gelap"]} ≠ terukur {u_baru["gelap"]}')
    ids = [b["id"] for b in obj["BAGIAN"]]
    if len(ids) != 7:
        m.append(f"{len(ids)} bagian, seharusnya 7")
    if len(set(ids)) != len(ids):
        m.append("ada id bagian ganda")
    for b in obj["BAGIAN"]:
        if not b.get("catatan"):
            m.append(f'{b["id"]}: tanpa catatan')
        if b["jarak"] <= 0 and b["id"] != "biji":
            m.append(f'{b["id"]}: jarak buka {b["jarak"]} — tidak akan terlihat')
        if b["id"] == "biji" and b["jarak"] <= 0:
            m.append("biji harus maju ke kamera, bukan diam di tempat")
    kam = obj["KAMERA"]
    if len(kam) != len(obj["KETUKAN"]):
        m.append(f'{len(kam)} kamera vs {len(obj["KETUKAN"])} ketukan — harus sama')
    nilai = {(k["ry"], k["rx"], k["zoom"]) for k in kam.values()}
    if len(nilai) != len(kam):
        m.append(f"hanya {len(nilai)} kamera berbeda dari {len(kam)} — ada ketukan yang parkir")
    for k in obj["KETUKAN"]:
        if k["id"] not in kam:
            m.append(f'ketukan {k["id"]} tanpa kamera')
        if k["selesai"] - k["mulai"] < 2 or k["selesai"] - k["mulai"] > 3:
            m.append(f'ketukan {k["id"]} {k["selesai"]-k["mulai"]} s — aturan metode 2–3 s')
    if {k["bagian"] for k in obj["KETUKAN"] if k["bagian"]} != set(ids):
        m.append("ada bagian yang tidak punya ketukan sendiri")
    if len(obj["CEKLIS"]) < 10 or len(obj["CEKLIS"]) > 12:
        m.append(f'ceklis {len(obj["CEKLIS"])} baris, harus 10–12')
    if "NEVER" not in " ".join(obj["CEKLIS"]):
        m.append('ceklis tanpa satu pun "NEVER" — aturan metode tidak terpenuhi')
    return m


if __name__ == "__main__":
    if "--cek" in sys.argv:
        mm = cek()
        for x in mm:
            print("  ✗", x)
        print("  kesimpulan:", "OK · angka cocok dengan citra acuan" if not mm else f"{len(mm)} masalah")
        sys.exit(0 if not mm else 1)
    u = ukur(ACUAN)
    b = bagian(u)
    k = kamera()
    c = ceklis(u, b)
    tulis(u, b, k, c)
    print(f'  acuan      {u["berkas"]} · {u["lebar"]}×{u["tinggi"]} · rasio {u["rasio"]}')
    print(f'  tinta      {u["gelap"]*100:.1f}% · pita {u["gelap_per_pita"]} · aksen {u["aksen"]*100:.1f}%')
    print(f'  bagian     {len(b)} · ketukan {len(KETUKAN)} · kamera {len(k)} · film {KETUKAN[-1][3]} s')
    print(f'  data       cutaway/data.js · {os.path.getsize(DATA_JS)/1024:.1f} KB')
    print(f'  ceklis     laporan/cutaway-checklist.md · {len(c)} baris')
    for x in cek():
        print("  ✗", x)
