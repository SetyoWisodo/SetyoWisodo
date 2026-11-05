#!/usr/bin/env python3
"""
D4 · Kreatif & Media — biji kopi 3D untuk hero (poster + validasi).

Kenapa ada dua perender
-----------------------
`assets/js/biji3d.js` merender biji dengan WebGL di browser pengguna. Sandbox ini
tidak punya browser, jadi tidak ada cara memeriksa hasilnya di sini. Karena itu
skrip ini membangun MESH YANG SAMA (parameter dari `data/biji3d.json`) dan
merendernya di CPU ke PNG. Poster itu:

  · dipakai sebagai gambar awal hero sebelum WebGL hidup (dan kalau WebGL mati),
  · jadi bukti visual yang benar-benar bisa dilihat — bukan klaim.

Rumus permukaan, proyeksi kamera, dan pencahayaan di sini adalah cermin dari
`assets/js/biji3d.js`. Kalau salah satunya diubah, ubah keduanya; cek
`tools/periksa.py` cek "Biji 3D" akan gagal kalau berkas ini tidak sinkron.

Pakai:
    python3 tools/biji.py             # poster + laporan
    python3 tools/biji.py --cek       # validasi data saja (cepat, tanpa render)
    python3 tools/biji.py --kecil     # (lama) poster mesh 420×525

  CATATAN 5 Nov 2026: perender mesh di skrip ini SUDAH TIDAK DIPAKAI untuk
  beranda. Pemilik menilai bentuknya "sangat aneh", jadi poster diganti render
  hiper-realistis lewat `tools/biji_render.py`. Skrip ini dipertahankan untuk
  `--cek` (validasi zona & senyawa) dan sebagai jejak cara lama.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tanggal import hari_ini  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "biji3d.json")
POSTER = os.path.join(ROOT, "assets", "img", "biji-3d-poster-mesh.png")
LAPORAN = os.path.join(ROOT, "laporan", "biji-3d.json")


# ── geometri ────────────────────────────────────────────────────────────────
# Semua fungsi di bawah ini disalin 1:1 ke JS. Jangan "memperbaiki" salah satu
# sisi tanpa yang lain.

def hex_rgb(h):
    h = h.lstrip("#")
    return [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]


def halus(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


class Biji:
    def __init__(self, d):
        g = d["geometri"]
        self.a = g["sumbu"]["a"]
        self.b = g["sumbu"]["b"]
        self.c = g["sumbu"]["c"]
        self.rata_faktor = g["ratakan"]["faktor"]
        self.rata_mulai = g["ratakan"]["mulai"]
        self.al = g["alur"]
        self.taper = g["ujung"]["taper"]
        self.tek = g["tekstur"]

    def alur_dalam(self, x, tp):
        """Kedalaman alur (0..1). Alur = kurva S di sisi +Z (tp = pi/2) sepanjang sumbu X.

        Dihitung dari SUDUT azimut, bukan dari z, karena z sudah diratakan dan
        tidak lagi monoton terhadap jarak ke alur.
        """
        if math.sin(tp) <= 0:
            return 0.0
        d = (tp - math.pi / 2 + math.pi) % (2 * math.pi) - math.pi
        pusat = self.al["amplitudo"] * math.sin(self.al["frekuensi"] * math.pi * x / self.a)
        sisa = d - pusat
        return self.al["dalam"] * math.exp(-(sisa * sisa) / (2 * self.al["lebar"] ** 2))

    def titik(self, tx, tp, radius=1.0):
        """tx = polar dari +Y (0..pi), tp = azimut (0..2pi). Radius 1.0 = permukaan."""
        st, ct = math.sin(tx), math.cos(tx)
        sp, cp = math.sin(tp), math.cos(tp)
        x = self.a * st * cp
        y = self.b * ct
        z = self.c * st * sp

        # ujung meruncing halus supaya tidak terasa bola
        ujung = abs(x) / self.a
        skala_ujung = 1.0 - self.taper * ujung ** 3
        y *= skala_ujung
        z *= skala_ujung
        x *= 1.0 - self.taper * 0.35 * ujung ** 4

        # sisi +Z (sisi alur) diratakan: biji kopi punya satu muka datar
        if sp > 0:
            f = self.rata_faktor + (1.0 - self.rata_faktor) * (1.0 - halus(sp / 0.55))
            z *= f
            z -= self.c * 0.04 * halus(sp / 0.55)

        # dua belahan menggelembung di sisi datar (bukan satu bidang rata)
        if sp > 0:
            d0 = (tp - math.pi / 2 + math.pi) % (2 * math.pi) - math.pi
            lobe = math.cos(min(1.0, abs(d0) / 1.15) * math.pi / 2)
            z += self.c * 0.2 * lobe * (1.0 - halus(abs(x) / self.a))

        # alur
        d = self.alur_dalam(x, tp)
        z -= d * self.c * 1.0
        ciut = 1.0 - d * 0.18
        x *= ciut
        y *= ciut

        # pitting halus (deterministik, fungsi sama di JS)
        n = (math.sin(x * self.tek["frekuensi"] + 1.7)
             * math.cos(y * self.tek["frekuensi"] * 1.13 - 0.4)
             * math.sin(z * self.tek["frekuensi"] * 0.87 + 2.1))
        tarik = 1.0 + n * self.tek["amplitudo"]
        return [x * tarik * radius, y * tarik * radius, z * tarik * radius]

    def normal(self, tx, tp, eps=1e-3):
        p0 = self.titik(tx, tp)
        p1 = self.titik(tx + eps, tp)
        p2 = self.titik(tx, tp + eps)
        u = [p1[i] - p0[i] for i in range(3)]
        v = [p2[i] - p0[i] for i in range(3)]
        n = [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]]
        L = math.sqrt(sum(c * c for c in n))
        if L < 1e-9:
            # kutub: turunan azimut nol, pakai arah radial sebagai normal
            r = math.sqrt(sum(c * c for c in p0)) or 1.0
            return [c / r for c in p0]
        n = [c / L for c in n]
        # pastikan normal menghadap KELUAR (titik pusat bidang = 0,0,0)
        if sum(n[i] * p0[i] for i in range(3)) < 0:
            n = [-c for c in n]
        return n

    def ao(self, x, tp):
        """Oklusi di dalam alur: makin dalam alur, makin gelap."""
        return 1.0 - 0.66 * min(1.0, self.alur_dalam(x, tp) / self.al["dalam"])

    def arah_ke_permukaan(self, arah):
        """Cari titik permukaan pada arah tertentu (untuk menaruh titik sentuh)."""
        L = math.sqrt(sum(c * c for c in arah)) or 1.0
        arah = [c / L for c in arah]
        lo, hi = 0.05, 2.2
        for _ in range(40):
            mid = (lo + hi) / 2
            p = [arah[i] * mid for i in range(3)]
            # di luar elipsoid termodifikasi?
            r = math.sqrt((p[0] / self.a) ** 2 + (p[1] / self.b) ** 2 + (p[2] / self.c) ** 2)
            if r > 1.0:
                hi = mid
            else:
                lo = mid
        return [arah[i] * lo for i in range(3)]


# ── kamera ──────────────────────────────────────────────────────────────────

def norm(v):
    L = math.sqrt(sum(c * c for c in v)) or 1.0
    return [c / L for c in v]


def sub(a, b):
    return [a[i] - b[i] for i in range(3)]


def dot(a, b):
    return sum(a[i] * b[i] for i in range(3))


def cross(a, b):
    return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]


class Kamera:
    def __init__(self, cam, lebar, tinggi):
        self.pos = cam["posisi"]
        self.target = cam["target"]
        self.fov = math.radians(cam["fov_deg"])
        self.w = lebar
        self.h = tinggi
        self.maju = norm(sub(self.target, self.pos))
        self.kanan = norm(cross(self.maju, [0, 1, 0]))
        self.atas = cross(self.kanan, self.maju)

    def proyeksi(self, p):
        d = sub(p, self.pos)
        z = dot(d, self.maju)
        if z <= 0.001:
            return None
        f = 1.0 / math.tan(self.fov / 2)
        x = dot(d, self.kanan) / z * f
        y = dot(d, self.atas) / z * f
        aspek = self.w / self.h
        return ((x / aspek * 0.5 + 0.5) * self.w, (0.5 - y * 0.5) * self.h, z)


def bangun_mesh(biji, cam, ukuran):
    """Hasilkan vertex & segitiga + proyeksi layar. Dipakai renderer CPU di bawah."""
    nt, np_ = ukuran
    titik, normals, aos, layar, kedalaman = [], [], [], [], []
    for i in range(nt + 1):
        tx = math.pi * i / nt
        for j in range(np_):
            tp = 2 * math.pi * j / np_
            p = biji.titik(tx, tp)
            n = biji.normal(tx, tp)
            titik.append(p)
            normals.append(n)
            aos.append(biji.ao(p[0], tp))
            layar.append(cam.proyeksi(p))
            kedalaman.append(dot(sub(p, cam.pos), cam.maju))
    return titik, normals, aos, layar, kedalaman


# ── shader (cermin dari biji3d.js) ─────────────────────────────────────────

def bayang(n, p, warna, cahaya, cam, kilau_pangkat=28, kilau_kekuatan=0.5, ao=1.0):
    kunci = norm(cahaya["kunci"])
    isi = norm(cahaya["isi"])
    v = norm(sub(cam.pos, p))
    h = norm([kunci[i] + v[i] for i in range(3)])

    lam = max(0.0, dot(n, kunci)) * cahaya["kekuatan_kunci"]
    fil = max(0.0, dot(n, isi)) * cahaya["kekuatan_isi"]
    spec = (max(0.0, dot(n, h)) ** kilau_pangkat) * kilau_kekuatan
    rim = (1.0 - max(0.0, dot(n, v))) ** 3 * 0.14

    t = halus(lam * 1.15)
    dasar = [warna["gelap"][i] + (warna["tengah"][i] - warna["gelap"][i]) * t for i in range(3)]
    # puncak terang medium roast: bagian atas biji lebih terbuka ke panas
    atas = halus((p[1] / 0.66 + 1) * 0.5)
    for i in range(3):
        dasar[i] += (warna["terang"][i] - dasar[i]) * (0.42 * t * atas)

    r = dasar[0] * (0.42 + 0.58 * lam) + fil * warna["tengah"][0] * 0.9
    g = dasar[1] * (0.42 + 0.58 * lam) + fil * warna["tengah"][1] * 0.9
    b = dasar[2] * (0.42 + 0.58 * lam) + fil * warna["tengah"][2] * 0.9
    r += spec * warna["kilau"][0]
    g += spec * warna["kilau"][1]
    b += spec * warna["kilau"][2]
    ao_k = 0.55 + 0.45 * ao
    r = r * ao_k + rim
    g = g * ao_k + rim
    b = b * ao_k + rim
    return (min(1.0, r) ** (1 / 1.05), min(1.0, g) ** (1 / 1.05), min(1.0, b) ** (1 / 1.05))


def bangun_bayangan(data, cam, lebar, tinggi):
    """Elips bayangan kontak di bawah biji, dihitung dari proyeksi titik terendah."""
    biji = Biji(data)
    bawah = 0.0
    kiri = kanan = 0.0
    for j in range(60):
        tp = 2 * math.pi * j / 60
        for i in range(1, 60):
            tx = math.pi * i / 60
            p = biji.titik(tx, tp)
            if p[1] < bawah:
                bawah = p[1]
            pr = cam.proyeksi(p)
            if pr:
                kiri = min(kiri, pr[0]) if kiri else pr[0]
                kanan = max(kanan, pr[0])
    if not kanan:
        return None
    pr_bawah = cam.proyeksi([0.0, bawah, 0.0])
    if not pr_bawah:
        return None
    bx = (kiri + kanan) / 2
    by = pr_bawah[1] + tinggi * 0.028
    brx = (kanan - kiri) * 0.52
    bry = max(10.0, brx * 0.16)
    return bx, by, brx, bry


def render_poster(data, lebar=640, tinggi=800):
    import numpy as np
    from PIL import Image

    biji = Biji(data)
    cam = Kamera(data["kamera"], lebar, tinggi)
    warna = {k: hex_rgb(v) for k, v in data["warna"].items()
             if k in ("gelap", "tengah", "terang", "kilau", "kertas")}
    ukuran = int(data["geometri"]["resolusi"]["poster"][0]), int(data["geometri"]["resolusi"]["poster"][1])
    titik, normals, aos, layar, _ = bangun_mesh(biji, cam, ukuran)

    nt, npp = ukuran
    # RGBA transparan: poster harus menyatu dengan latar halaman apa pun
    img = np.zeros((tinggi, lebar, 3), dtype=np.float32)
    alfa_img = np.zeros((tinggi, lebar), dtype=np.float32)
    zbuf = np.full((tinggi, lebar), 1e9, dtype=np.float32)

    # bayangan kontak di bawah biji — digambar lebih dulu, dengan alfa
    import numpy as _np
    ys, xs = _np.mgrid[0:tinggi, 0:lebar].astype(_np.float32)
    pusat_bayang = bangun_bayangan(data, cam, lebar, tinggi)
    if pusat_bayang:
        bx, by, brx, bry = pusat_bayang
        jarak = (((xs - bx) / brx) ** 2 + ((ys - by) / bry) ** 2)
        alfa = _np.clip(1.0 - jarak, 0.0, 1.0) ** 1.6 * 0.3
        gelap = _np.array([0.09, 0.06, 0.04], dtype=_np.float32)
        img[:] = gelap
        alfa_img[:] = alfa

    def indeks(i, j):
        return i * npp + (j % npp)

    segitiga = 0
    for i in range(nt):
        for j in range(npp):
            i0, i1 = indeks(i, j), indeks(i, j + 1)
            i2, i3 = indeks(i + 1, j), indeks(i + 1, j + 1)
            for tri in ((i0, i2, i1), (i1, i2, i3)):
                ps = [layar[k] for k in tri]
                if any(p is None for p in ps):
                    continue
                xs = [p[0] for p in ps]
                ys = [p[1] for p in ps]
                x0, x1 = int(max(0, math.floor(min(xs)))), int(min(lebar - 1, math.ceil(max(xs))))
                y0, y1 = int(max(0, math.floor(min(ys)))), int(min(tinggi - 1, math.ceil(max(ys))))
                if x1 < x0 or y1 < y0:
                    continue
                ax, ay = xs[0], ys[0]
                bx, by = xs[1] - ax, ys[1] - ay
                cx, cy = xs[2] - ax, ys[2] - ay
                det = bx * cy - by * cx
                if abs(det) < 1e-9:
                    continue
                segitiga += 1
                X = np.arange(x0, x1 + 1) + 0.5
                Y = np.arange(y0, y1 + 1) + 0.5
                gx, gy = np.meshgrid(X, Y)
                px, py = gx - ax, gy - ay
                w1 = (px * cy - py * cx) / det
                w2 = (py * bx - px * by) / det
                w0 = 1.0 - w1 - w2
                dalam = (w0 >= -1e-6) & (w1 >= -1e-6) & (w2 >= -1e-6)
                if not dalam.any():
                    continue
                # interpolasi atribut pada barycenter
                zs = [ps[k][2] for k in range(3)]
                zdaftar = zs[0] * w0 + zs[1] * w1 + zs[2] * w2
                sub_zbuf = zbuf[y0:y1 + 1, x0:x1 + 1]
                pas = dalam & (zdaftar < sub_zbuf)
                if not pas.any():
                    continue
                k0, k1, k2 = tri
                n = [normals[k0][c] * w0 + normals[k1][c] * w1 + normals[k2][c] * w2 for c in range(3)]
                p = [titik[k0][c] * w0 + titik[k1][c] * w1 + titik[k2][c] * w2 for c in range(3)]
                aa = aos[k0] * w0 + aos[k1] * w1 + aos[k2] * w2
                # satu warna per segitiga (barycenter) — cukup untuk bukti bentuk
                nb = norm([float(v.mean()) for v in n])
                pb = [float(v.mean()) for v in p]
                ab = float(aa.mean())
                rgb = bayang(nb, pb, warna, data["cahaya"], cam,
                             data["cahaya"]["kilau_pangkat"], data["cahaya"]["kilau_kekuatan"], ab)
                sub_zbuf[pas] = zdaftar[pas]
                blok = img[y0:y1 + 1, x0:x1 + 1]
                blok_a = alfa_img[y0:y1 + 1, x0:x1 + 1]
                for c in range(3):
                    blok[..., c][pas] = rgb[c]
                blok_a[pas] = 1.0

    # titik sentuh digambar sebagai cincin tipis + nomor
    from PIL import ImageDraw, ImageFont
    rgba = np.dstack([np.clip(img, 0, 1), np.clip(alfa_img, 0, 1)])
    out = Image.fromarray((rgba * 255).astype(np.uint8), "RGBA")
    d = ImageDraw.Draw(out)
    try:
        f = ImageFont.truetype(os.path.join(ROOT, "assets", "fonts", "inter-latin-600-normal.ttf"), max(11, lebar // 46))
    except Exception:
        f = ImageFont.load_default()

    posisi = []
    for i, z in enumerate(data["zona"], 1):
        p = biji.arah_ke_permukaan(z["arah"])
        n = norm(p)
        pr = cam.proyeksi(p)
        arah_lihat = norm(sub(cam.pos, p))
        tampak = dot(norm(n), arah_lihat) > 0.12
        if not pr:
            posisi.append({"id": z["id"], "x": 0, "y": 0, "tampak": False})
            continue
        sx, sy, _ = pr
        posisi.append({"id": z["id"], "x": round(sx / lebar * 100, 2), "y": round(sy / tinggi * 100, 2),
                       "tampak": tampak, "arah_permukaan": [round(v, 4) for v in p]})
        if tampak:
            r = max(9, lebar // 40)
            d.ellipse([sx - r, sy - r, sx + r, sy + r], outline=(245, 239, 228), width=2)
            d.ellipse([sx - r - 2, sy - r - 2, sx + r + 2, sy + r + 2], outline=(22, 17, 13), width=1)
            teks = str(i)
            tw = d.textlength(teks, font=f)
            d.text((sx - tw / 2, sy - f.size * 0.62), teks, font=f, fill=(22, 17, 13))

    os.makedirs(os.path.dirname(POSTER), exist_ok=True)
    out.save(POSTER, optimize=True)
    return posisi, segitiga


def validasi(data):
    masalah = []
    biji = Biji(data)

    if data["biji"]["spesies"] != "Coffea arabica":
        masalah.append("spesies bukan Coffea arabica")
    if "medium" not in data["biji"]["tingkat_sangrai"]["nama"].lower():
        masalah.append("tingkat sangrai bukan medium")

    # daftar token dibaca dari design-system, bukan disalin ke sini
    ds = json.loads(open(os.path.join(ROOT, "data", "design-system.json"), encoding="utf-8").read())
    warna_boleh = {h.lower() for h in ds["warna"]["boleh_dipakai"]}
    for k, v in data["warna"].items():
        if k.startswith("_"):
            continue
        if v.lower() not in warna_boleh:
            masalah.append(f"warna {k}={v} di luar token design-system")

    id_sumber = {s["id"] for s in data["sumber_angka"]}
    zona_id = set()
    for z in data["zona"]:
        if z["id"] in zona_id:
            masalah.append(f"zona ganda: {z['id']}")
        zona_id.add(z["id"])
        if not z.get("senyawa"):
            masalah.append(f"{z['id']}: tanpa senyawa")
        for s in z["senyawa"]:
            if s["sumber"] not in id_sumber:
                masalah.append(f"{z['id']}/{s['nama']}: sumber {s['sumber']} tidak ada di daftar")
            if not s.get("rentang"):
                masalah.append(f"{z['id']}/{s['nama']}: tanpa rentang")
            if s.get("keyakinan") not in ("kuat", "umum"):
                masalah.append(f"{z['id']}/{s['nama']}: keyakinan tidak ditandai")
        p = biji.arah_ke_permukaan(z["arah"])
        r = math.sqrt((p[0] / biji.a) ** 2 + (p[1] / biji.b) ** 2 + (p[2] / biji.c) ** 2)
        if not (0.55 < r < 1.25):
            masalah.append(f"{z['id']}: titik tidak menempel di permukaan (r={r:.2f})")

    if not data.get("kejujuran", {}).get("catatan_tampil"):
        masalah.append("catatan kejujuran untuk ditampilkan belum ada")
    return masalah


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cek", action="store_true")
    ap.add_argument("--kecil", action="store_true")
    args = ap.parse_args()

    with open(DATA, encoding="utf-8") as f:
        data = json.load(f)

    masalah = validasi(data)
    if args.cek:
        for m in masalah:
            print(f"  XX  {m}")
        print(f"  {len(data['zona'])} zona · {sum(len(z['senyawa']) for z in data['zona'])} senyawa · {len(masalah)} masalah")
        return 0 if not masalah else 1

    kosong = [z["id"] for z in data["zona"]
              if z["id"] not in (data.get("_terakhir_tampak") or [])] if data.get("_terakhir_tampak") else []
    del kosong
    posisi, segitiga = render_poster(data, 420, 525) if args.kecil else render_poster(data)
    tampak = [p for p in posisi if p["tampak"]]
    ukuran_kb = os.path.getsize(POSTER) / 1024

    laporan = {
        "dibuat": hari_ini().isoformat(),
        "berkas": os.path.relpath(POSTER, ROOT),
        "ukuran_kb": round(ukuran_kb, 1),
        "segitiga_tergambar": segitiga,
        "zona": len(data["zona"]),
        "senyawa": sum(len(z["senyawa"]) for z in data["zona"]),
        "titik_tampak": len(tampak),
        "posisi_layar_persen": posisi,
        "masalah": masalah,
        "catatan": "Poster dirender CPU oleh tools/biji.py dengan mesh & shader yang sama seperti "
                   "assets/js/biji3d.js. Bukan render WebGL.",
    }
    with open(LAPORAN, "w", encoding="utf-8") as f:
        json.dump(laporan, f, ensure_ascii=False, indent=2)

    print(f"  poster   : {laporan['berkas']} · {ukuran_kb:.0f} KB · {segitiga:,} segitiga")
    print(f"  titik    : {len(tampak)}/{len(posisi)} tampak dari kamera")
    for p in posisi:
        tanda = "ok" if p["tampak"] else "belakang"
        print(f"    {p['id']:12s} x={p['x']:6.2f}% y={p['y']:6.2f}%  {tanda}")
    print(f"  masalah  : {len(masalah)}")
    return 0 if not masalah else 1


if __name__ == "__main__":
    raise SystemExit(main())
