"""
Kemasan 3D — dari foto kemasan tampak depan menjadi objek tanpa latar, serong 10°.

Kenapa ada berkas ini
---------------------
Foto yang dikirim pemilik adalah foto biasa: ada meja, ada latar, kadang miring.
Memasukkannya apa adanya ke `rak/` akan merusak dua hal sekaligus — latar foto
memotong kertas halaman, dan perspektifnya tidak cocok dengan kotak 3D di rak.
Jadi foto tidak pernah dipasang langsung. Alurnya:

    foto mentah  →  buang latar  →  rapikan  →  bangun ketebalan (3D)  →  serong 10°
                 →  assets/img/kemasan/<id>-3d.webp   (PNG/WebP beralfa, TANPA latar)

Dua keluaran per kemasan:
    <id>-depan.webp : bidang depan saja, sudah dipotong & bersih (untuk punggung rak)
    <id>-3d.webp    : kotak kemasan dengan sisi kanan + sisi atas, cahaya dari kiri
                      atas, dimiringkan 10° ke kiri, latar transparan (untuk sampul
                      dan poster besar)

Semua deterministik: tidak ada model penghapus latar berbasis ML di sandbox ini,
jadi latar dibuang dengan banjir-warna dari tepi + toleransi, lalu tepinya
dihaluskan. Batasnya jujur: foto dengan latar ramai (banyak benda, gradasi kuat)
tidak akan bersih dengan cara ini — untuk itu perlu latar polos saat memotret.

Pakai
-----
    # 1. taruh foto kemasan di assets/img/kemasan/sumber/  (namanya = id katalog)
    #    contoh: gayo.jpg, kintamani.jpg, raung.png …
    python3 tools/kemasan.py                  # proses semua sumber → aset + data
    python3 tools/kemasan.py --demo           # contoh dari label brand (tanpa mengubah situs)
    python3 tools/kemasan.py --cek            # periksa keluaran & data
"""

from __future__ import annotations

import json
import os
import shutil
import sys

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUMBER = os.path.join(ROOT, "assets", "img", "kemasan", "sumber")
KELUAR = os.path.join(ROOT, "assets", "img", "kemasan")
DATA = os.path.join(ROOT, "data", "kemasan.json")
LAPORAN = os.path.join(ROOT, "laporan")

KERTAS = (237, 235, 230)      # #EDEBE6 — kertas halaman rujukan
TEBAL_SISI = 0.055            # ketebalan kotak: 5,5% lebar depan (karton, bukan balok)
TEBAL_ATAS = 0.014
YAW = 11                      # derajat: sisi kanan terlihat, tanpa menyimpang jauh
MIRING = 10                   # derajat. PIL: positif = berlawanan jarum jam, dan untuk
#                              kotak tegak itu berarti PUNCAK miring ke KIRI. Diukur, bukan
#                              dikira-kira: lihat cek_serong().
TINGGI = 1200                 # tinggi keluaran 3D (px)

EKST = (".jpg", ".jpeg", ".png", ".webp")


# --------------------------------------------------------------- latar ----
def buang_latar(im: Image.Image, langkah: int = 14, jauh: int = 96) -> Image.Image:
    """Buang latar lewat banjir-warna dari keempat tepi.

    Dua ambang, dan bedanya penting:
      · `langkah`  = selisih ke piksel **tetangga** yang merambat (menghadapi latar
                     bergradasi: meja yang makin gelap ke bawah tetap terhapus);
      · `jauh`     = selisih ke **warna latar median** (pagar supaya banjir tidak
                     merembes masuk ke kemasan lewat gradasi).

    Kalau gambar sudah punya alfa yang bermakna (lebih dari 2% piksel transparan),
    alfa itu dipakai apa adanya — tidak ada gunanya menebak.
    """
    im = im.convert("RGBA")
    alfa = im.getchannel("A")
    if alfa.getextrema()[0] < 250:
        transparan = sum(1 for v in alfa.getdata() if v < 16)
        if transparan > 0.02 * im.width * im.height:
            return im

    rgb = im.convert("RGB")
    px = rgb.load()
    W, H = rgb.size

    sudut = []
    for cx, cy in ((0, 0), (W - 6, 0), (0, H - 6), (W - 6, H - 6)):
        for dx in range(6):
            for dy in range(6):
                sudut.append(px[min(W - 1, cx + dx), min(H - 1, cy + dy)])
    sudut.sort(key=lambda c: c[0] + c[1] + c[2])
    latar = sudut[len(sudut) // 2]

    def jarak(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])

    from collections import deque

    topeng = Image.new("L", (W, H), 255)
    mp = topeng.load()
    sudah = bytearray(W * H)
    antre = deque()
    for x in range(W):
        antre.append((x, 0)); antre.append((x, H - 1))
    for y in range(H):
        antre.append((0, y)); antre.append((W - 1, y))
    while antre:
        x, y = antre.popleft()
        i = y * W + x
        if sudah[i]:
            continue
        sudah[i] = 1
        c = px[x, y]
        if jarak(c, latar) > jauh:
            continue
        mp[x, y] = 0
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < W and 0 <= ny < H and not sudah[ny * W + nx]:
                if jarak(px[nx, ny], c) <= langkah:
                    antre.append((nx, ny))
                elif jarak(px[nx, ny], latar) <= langkah:
                    antre.append((nx, ny))

    # bayangan & halo: foto selalu menyisakan bayangan jatuh dan pita tipis warna latar
    # di tepi kemasan. Dua-duanya dibuang dengan menggerus topeng ke dalam selama
    # pikselnya masih "mirip latar" atau "netral gelap" (ciri bayangan).
    def bayangan(c):
        r, g, b = c
        mx, mn = max(r, g, b), min(r, g, b)
        jenuh = (mx - mn) / 255
        return (jarak(c, latar) <= 150) or (jenuh < 0.14 and mn > 70)

    for _ in range(3):
        baru = topeng.copy()
        np_ = baru.load()
        for y in range(1, H - 1):
            for x in range(1, W - 1):
                if mp[x, y] == 0:
                    continue
                if (mp[x - 1, y] == 0 or mp[x + 1, y] == 0 or mp[x, y - 1] == 0 or mp[x, y + 1] == 0) \
                        and bayangan(px[x, y]):
                    np_[x, y] = 0
        topeng = baru
        mp = topeng.load()

    topeng = topeng.filter(ImageFilter.MedianFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
    im.putalpha(topeng)
    return im


def bersih_tepi(im: Image.Image, ambang: int = 24) -> Image.Image:
    """Warnai ulang piksel hampir-transparan dengan warna kemasan.

    Kenapa perlu: begitu gambar beralfa diperkecil (LANCZOS pada RGBA), Pillow
    meninggalkan warna aneh — pada percobaan pertama muncul pita MAGENTA di tepi
    kanan kemasan. Alfa-nya cuma 3/255, tapi kompresi WebP meniupkannya jadi
    terlihat. Jadi piksel dengan alfa < `ambang` diwarnai rata, alfa dibiarkan.
    """
    im = im.convert("RGBA")
    a = im.getchannel("A")
    if a.getextrema()[0] >= 250:
        return im
    rgb = im.convert("RGB")
    # warna wakil: rata-rata piksel yang benar-benar terlihat
    kumpulan = rgb.getcolors(maxcolors=1 << 24) or []
    total = sum(n for n, _ in kumpulan) or 1
    r = sum(c[0] * n for n, c in kumpulan) / total
    g = sum(c[1] * n for n, c in kumpulan) / total
    b = sum(c[2] * n for n, c in kumpulan) / total
    isi = Image.new("RGB", im.size, (int(r), int(g), int(b)))
    mask = a.point(lambda v: 255 if v < ambang else 0)
    hasil = Image.composite(isi, rgb, mask).convert("RGBA")
    hasil.putalpha(a)
    return hasil


def rapikan(im: Image.Image, sisa: int = 2) -> Image.Image:
    """Potong ke isi (bbox alfa), sisakan beberapa piksel."""
    bbox = im.getchannel("A").point(lambda v: 255 if v > 12 else 0).getbbox()
    if not bbox:
        return im
    x0, y0, x1, y1 = bbox
    x0, y0 = max(0, x0 - sisa), max(0, y0 - sisa)
    x1, y1 = min(im.width, x1 + sisa), min(im.height, y1 + sisa)
    return im.crop((x0, y0, x1, y1))


# ------------------------------------------------------- perspektif 8x8 ----
def _selesaikan(m, b):
    """Eliminasi Gauss untuk sistem 8x8 (dipakai perspektif)."""
    n = 8
    for i in range(n):
        p = max(range(i, n), key=lambda r: abs(m[r][i]))
        if abs(m[p][i]) < 1e-12:
            raise ValueError("perspektif singular")
        m[i], m[p] = m[p], m[i]
        b[i], b[p] = b[p], b[i]
        for r in range(i + 1, n):
            f = m[r][i] / m[i][i]
            for c in range(i, n):
                m[r][c] -= f * m[i][c]
            b[r] -= f * b[i]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = b[i] - sum(m[i][c] * x[c] for c in range(i + 1, n))
        x[i] = s / m[i][i]
    return x


def koef_perspektif(dst, src):
    """Koefisien Pillow (output→input) dari 4 pasangan titik."""
    m, b = [], []
    for (X, Y), (x, y) in zip(dst, src):
        m.append([X, Y, 1, 0, 0, 0, -x * X, -x * Y]); b.append(x)
        m.append([0, 0, 0, X, Y, 1, -y * X, -y * Y]); b.append(y)
    return _selesaikan(m, b)


def warp(im: Image.Image, quad, kanvas: tuple[int, int]) -> Image.Image:
    """Tempel `im` ke kanvas pada posisi quad (4 titik), dengan perspektif."""
    xs = [p[0] for p in quad]; ys = [p[1] for p in quad]
    x0, y0 = int(min(xs)), int(min(ys))
    x1, y1 = int(max(xs)) + 1, int(max(ys)) + 1
    bw, bh = max(2, x1 - x0), max(2, y1 - y0)
    dst = [(0, 0), (bw, 0), (bw, bh), (0, bh)]
    lokal = [(p[0] - x0, p[1] - y0) for p in quad]
    k = koef_perspektif(dst, lokal)
    wajah = im.transform((bw, bh), Image.Transform.PERSPECTIVE, k,
                         resample=Image.BICUBIC)
    kanvas.alpha_composite(wajah, (x0, y0))
    return kanvas


# --------------------------------------------------------------- 3D -------
def gelap(im: Image.Image, f: float) -> Image.Image:
    r, g, b, a = im.split()
    r = r.point(lambda v: int(v * f)); g = g.point(lambda v: int(v * f)); b = b.point(lambda v: int(v * f))
    return Image.merge("RGBA", (r, g, b, a))


def tiga_d(depan: Image.Image, tebal_sisi: float = TEBAL_SISI,
           tebal_atas: float = TEBAL_ATAS, yaw: float = YAW,
           miring: float = MIRING) -> Image.Image:
    """Bidang depan → kotak kemasan bervolume, lalu serong 10° ke kiri.

    Geometri (sebelum diputar), dengan k = yaw/90:
        depan  A(0,0) B(w, h·k/2) C(w, h−h·k/2) D(0,h)      ← tepi kanan memendek (menjauh)
        sisi   B E F C   dengan (E,F) = (B,C) + (lebar_sisi, −h·k·0.55)
        atas   A B E A'  dengan A' = A + (lebar_sisi, −h·k·0.55)

    Cahaya dari kiri atas-depan: depan dilewati gradien terang→gelap, sisi kanan
    0,55×, sisi atas 1,06×. Tanpa bayangan jatuh: pemilik meminta tanpa latar,
    dan bayangan akan bertabrakan dengan bayangan CSS di halaman.
    """
    depan = depan.convert("RGBA")
    W, H = depan.size
    k = yaw / 90.0
    ts = max(3, int(W * tebal_sisi))
    ta = max(2, int(H * tebal_atas))
    dy = -H * k * 0.55                      # arah kedalaman di layar (naik & kanan)
    dx = ts * 1.0

    pad_x = int(abs(dx) + W * 0.02 + 6)
    pad_y = int(abs(dy) + ta + H * k * 0.5 + 8)
    kanvas = Image.new("RGBA", (W + pad_x * 2, H + pad_y * 2), (0, 0, 0, 0))
    ox, oy = pad_x, pad_y + H * k * 0.5

    A = (ox, oy)
    B = (ox + W, oy - H * k * 0.5)
    C = (ox + W, oy + H - H * k * 0.5)
    D = (ox, oy + H)
    E = (B[0] + dx, B[1] + dy)
    F = (C[0] + dx, C[1] + dy)
    At = (A[0] + dx, A[1] + dy)

    # --- sisi & atas diwarnai dari tepi kemasan itu sendiri, bukan dari isi yang
    #     diregangkan: karton tebal terlihat sebagai bidang warna, bukan gambar gepeng
    def warna_rata(box, f: float):
        potongan = depan.crop(box)
        st = ImageStat.Stat(potongan.convert("RGB"))
        return tuple(min(255, int(c * f)) for c in st.mean)

    isi_sisi = depan.getpixel((W - 2, H // 2))[:3]
    isi_atas = tuple(int(c * 1.04) for c in depan.getpixel((W // 2, 2))[:3])

    # gambar belakang dulu: atas, lalu sisi, lalu depan — supaya sambungan tertutup bersih
    atas = Image.new("RGBA", (W, max(2, ta * 2)), isi_atas + (255,))
    kanvas = warp(atas, [A, B, (E[0], E[1] + ta), (At[0], At[1] + ta)], kanvas)

    sisi = Image.new("RGBA", (max(2, int(abs(dx))), int(H + abs(dy))), isi_sisi + (255,))
    gr = Image.linear_gradient("L").rotate(90).resize(sisi.size)
    gelap_kiri = Image.new("RGBA", sisi.size, (0, 0, 0, 255))
    gelap_kiri.putalpha(gr.point(lambda v: int(v * 0.28)))
    sisi.alpha_composite(gelap_kiri)
    kanvas = warp(sisi, [B, E, F, C], kanvas)

    # depan: gradien cahaya kiri→kanan
    depan2 = depan.copy()
    Wd, Hd = depan2.size
    gr2 = Image.linear_gradient("L").resize((Wd, 1)).resize((Wd, Hd))
    tirai = Image.new("RGBA", (Wd, Hd), (10, 7, 5, 255))
    tirai.putalpha(gr2.point(lambda v: int(v * 0.24)))
    depan2.alpha_composite(tirai)
    kanvas = warp(depan2, [A, B, C, D], kanvas)

    # garis sambung 1 px supaya bidang depan tidak menempel begitu saja pada sisinya
    d = ImageDraw.Draw(kanvas)
    d.line([B, C], fill=(255, 255, 255, 60), width=1)

    # serong ke kiri (berlawanan jarum jam)
    kanvas = kanvas.rotate(miring, resample=Image.BICUBIC, expand=True)
    return rapikan(kanvas, sisa=1)


def terang(im: Image.Image, f: float) -> Image.Image:
    r, g, b, a = im.split()
    potong = lambda v: min(255, int(v * f))
    return Image.merge("RGBA", (r.point(potong), g.point(potong), b.point(potong), a))


# -------------------------------------------------------------- proses ----
def daftar_sumber(folder: str) -> list[tuple[str, str]]:
    if not os.path.isdir(folder):
        return []
    hasil = []
    for nama in sorted(os.listdir(folder)):
        akar, ext = os.path.splitext(nama)
        if ext.lower() in EKST:
            hasil.append((akar.lower().replace(" ", "-"), os.path.join(folder, nama)))
    return hasil


def olah(id_item: str, path: str, keluar: str, tinggi: int = TINGGI) -> dict:
    asli = Image.open(path)
    bersih = rapikan(buang_latar(asli))
    # bidang depan dinormalkan ke tinggi tertentu
    rasio = bersih.height / bersih.width
    tinggi_depan = tinggi
    depan = bersih_tepi(bersih.resize((int(tinggi_depan / rasio), tinggi_depan), Image.LANCZOS))

    kotak = bersih_tepi(tiga_d(depan))
    if kotak.height > tinggi:
        kotak = kotak.resize((int(kotak.width * tinggi / kotak.height), tinggi), Image.LANCZOS)

    os.makedirs(keluar, exist_ok=True)
    p_depan = os.path.join(keluar, f"{id_item}-depan.webp")
    p_3d = os.path.join(keluar, f"{id_item}-3d.webp")
    depan.save(p_depan, "WEBP", quality=88, method=6)
    kotak.save(p_3d, "WEBP", quality=88, method=6, exact=True)
    return {
        "id": id_item,
        "sumber": os.path.relpath(path, ROOT).replace(os.sep, "/"),
        "depan": os.path.relpath(p_depan, ROOT).replace(os.sep, "/"),
        "tiga_d": os.path.relpath(p_3d, ROOT).replace(os.sep, "/"),
        "ukuran": [kotak.width, kotak.height],
        "serong_ke_kiri": MIRING,
        "tebal": TEBAL_SISI,
        "kb": round(os.path.getsize(p_3d) / 1024),
    }


def lembar(entri: list[dict], keluar: str) -> str:
    """Lembar periksa: semua kemasan 3D di atas kertas, untuk dilihat pemilik."""
    if not entri:
        return ""
    tinggi = 520
    kolom = 4
    baris = (len(entri) + kolom - 1) // kolom
    sel_w, sel_h = 420, 660
    im = Image.new("RGB", (kolom * sel_w + 80, baris * sel_h + 130), KERTAS)
    d = ImageDraw.Draw(im)
    from PIL import ImageFont
    f = ImageFont.truetype(os.path.join(ROOT, "assets", "fonts", "intertight.woff2"), 18)
    f2 = ImageFont.truetype(os.path.join(ROOT, "assets", "fonts", "newsreader.woff2"), 34)
    d.text((40, 34), "KEMASAN 3D · TANPA LATAR · SERONG 10° KE KIRI", font=f, fill=(20, 20, 20))
    for i, e in enumerate(entri):
        cx = 40 + (i % kolom) * sel_w
        cy = 100 + (i // kolom) * sel_h
        p = Image.open(os.path.join(ROOT, e["tiga_d"])).convert("RGBA")
        skala = min((sel_w - 60) / p.width, (tinggi) / p.height)
        p = p.resize((int(p.width * skala), int(p.height * skala)), Image.LANCZOS)
        im.paste(p, (cx + (sel_w - 60 - p.width) // 2, cy), p)
        d.text((cx + 30, cy + tinggi + 26), e["id"].upper(), font=f2, fill=(20, 20, 20))
        d.text((cx + 30, cy + tinggi + 70), f'{e["ukuran"][0]}×{e["ukuran"][1]} px · {e["kb"]} KB',
               font=f, fill=(109, 106, 99))
    im.save(keluar, "PNG", optimize=True)
    return keluar


def bangun(sumber: str = SUMBER, keluar: str = KELUAR, tulis_data: bool = True) -> list[dict]:
    daftar = daftar_sumber(sumber)
    if not daftar:
        print(f"  tidak ada foto di {os.path.relpath(sumber, ROOT)}")
        print("  taruh foto kemasan tampak depan di sana (nama berkas = id katalog),")
        print("  lalu jalankan lagi. Contoh id: gayo, kintamani, blue-mount-ijen, raung …")
        return []
    entri = []
    for id_item, path in daftar:
        e = olah(id_item, path, keluar)
        entri.append(e)
        print(f"  {id_item:<18} {e['ukuran'][0]}×{e['ukuran'][1]} · {e['kb']} KB · serong {e['serong_ke_kiri']}° ke kiri")
    if tulis_data:
        lama = {}
        if os.path.exists(DATA):
            try:
                lama = json.load(open(DATA, encoding="utf-8"))
            except json.JSONDecodeError:
                lama = {}
        gabung = {x["id"]: x for x in lama.get("kemasan", [])}
        for e in entri:
            gabung[e["id"]] = e
        isi = {
            "versi": 1,
            "sumber": "tools/kemasan.py",
            "serong_ke_kiri": MIRING,
            "catatan": "Foto mentah tidak pernah dipakai di halaman: selalu lewat tiga_d() dulu.",
            "kemasan": [gabung[k] for k in sorted(gabung)],
        }
        os.makedirs(os.path.dirname(DATA), exist_ok=True)
        with open(DATA, "w", encoding="utf-8") as f:
            json.dump(isi, f, ensure_ascii=False, indent=2)
        print(f"  data/kemasan.json · {len(isi['kemasan'])} kemasan")
    return entri


def demo() -> int:
    """Contoh: bikin 'foto' tiruan dari label brand, lalu jalankan pipa yang sama.

    Tujuannya membuktikan pipa bekerja hari ini, sebelum foto asli dikirim.
    Hasilnya masuk ke laporan/, tidak menyentuh aset situs.
    """
    sumber = "/tmp/kemasan-demo/sumber"
    keluar = "/tmp/kemasan-demo/keluar"
    shutil.rmtree("/tmp/kemasan-demo", ignore_errors=True)
    os.makedirs(sumber, exist_ok=True)
    label = [p for p in sorted(os.listdir(os.path.join(ROOT, "brand"))) if p.startswith("label-") and p.endswith(".png")]
    pilih = [p for p in label if "sheet" not in p][:4]
    for nama in pilih:
        id_item = nama.replace("label-", "").replace(".png", "")
        lab = Image.open(os.path.join(ROOT, "brand", nama)).convert("RGB")
        # "foto": label di atas meja krem, sedikit miring & bergradasi — meniru foto asli
        kanvas = Image.new("RGB", (int(lab.width * 2.1), int(lab.height * 1.7)), (214, 205, 189))
        gr = Image.linear_gradient("L").resize((1, kanvas.height)).resize(kanvas.size)
        kanvas = Image.composite(kanvas, Image.new("RGB", kanvas.size, (198, 188, 172)), gr)
        kecil = lab.resize((int(lab.width * 0.8), int(lab.height * 0.8)), Image.LANCZOS)
        kanvas.paste(kecil, ((kanvas.width - kecil.width) // 2, (kanvas.height - kecil.height) // 2))
        kanvas.save(os.path.join(sumber, f"{id_item}.jpg"), "JPEG", quality=92)
    entri = bangun(sumber, keluar, tulis_data=False)
    if entri:
        p = lembar(entri, os.path.join(LAPORAN, "kemasan-3d-demo.png"))
        print(f"  {os.path.relpath(p, ROOT)} · {os.path.getsize(p)/1024:.0f} KB")
    return 0 if entri else 1


def cek_serong(path: str) -> float | None:
    """Selisih tengah baris atas dan baris bawah pada aset 3D.

    Negatif = puncak lebih ke kiri (serong ke kiri). Ini mengukur hasil akhir,
    bukan argumen fungsi — kesalahan tanda di sini pernah lolos sekali.
    """
    im = Image.open(path).convert("RGBA")
    a = im.getchannel("A")
    W, H = im.size

    def tengah(y):
        xs = [x for x in range(W) if a.getpixel((x, y)) > 40]
        return sum(xs) / len(xs) if xs else None

    atas, bawah = tengah(int(H * 0.15)), tengah(int(H * 0.85))
    if atas is None or bawah is None:
        return None
    return atas - bawah


def cek() -> list[str]:
    m = []
    if not os.path.exists(DATA):
        m.append("data/kemasan.json belum ada (belum ada foto diproses)")
        return m
    isi = json.load(open(DATA, encoding="utf-8"))
    if not isi.get("kemasan"):
        m.append("data/kemasan.json kosong")
    for e in isi.get("kemasan", []):
        for kunci in ("depan", "tiga_d"):
            p = os.path.join(ROOT, e[kunci])
            if not os.path.exists(p):
                m.append(f'{e["id"]}: {e[kunci]} tidak ada')
                continue
            im = Image.open(p)
            if im.mode not in ("RGBA", "LA"):
                m.append(f'{e["id"]}: {e[kunci]} tidak beralfa — latar akan tampak')
            else:
                alfa = im.getchannel("A")
                tepi = [alfa.getpixel((0, 0)), alfa.getpixel((im.width - 1, 0)),
                        alfa.getpixel((0, im.height - 1)), alfa.getpixel((im.width - 1, im.height - 1))]
                if max(tepi) > 8:
                    m.append(f'{e["id"]}: sudut {kunci} tidak transparan ({max(tepi)}) — ada latar tersisa')
        if abs(e.get("serong_ke_kiri", 0) - 10) > 0.01:
            m.append(f'{e["id"]}: serong {e.get("serong_ke_kiri")}° bukan 10° ke kiri')
        piksel = Image.open(os.path.join(ROOT, e["tiga_d"])).convert("RGBA")
        alfa = piksel.getchannel("A")
        menyala = 0
        for y in range(0, piksel.height, 9):
          for x in range(0, piksel.width, 9):
            if alfa.getpixel((x, y)) < 24:
                r, g, b, _ = piksel.getpixel((x, y))
                if max(r, g, b) - min(r, g, b) > 120:
                    menyala += 1
        if menyala:
            m.append(f'{e["id"]}: {menyala} piksel hampir-transparan berwarna menyala (pita di tepi)')
        arah = cek_serong(os.path.join(ROOT, e["tiga_d"]))
        if arah is not None and arah >= 0:
            m.append(f'{e["id"]}: puncak kemasan miring ke kanan ({arah:+.1f} px)')
    return m


if __name__ == "__main__":
    if "--cek" in sys.argv:
        mm = cek()
        for x in mm:
            print("  ✗", x)
        print("  kesimpulan:", "OK" if not mm else f"{len(mm)} masalah")
        sys.exit(0 if not mm else 1)
    if "--demo" in sys.argv:
        sys.exit(demo())
    entri = bangun()
    if entri:
        p = lembar(entri, os.path.join(LAPORAN, "kemasan-3d.png"))
        print(f"  {os.path.relpath(p, ROOT)} · {os.path.getsize(p)/1024:.0f} KB")
    for x in cek():
        print("  ✗", x)
