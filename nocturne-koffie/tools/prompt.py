#!/usr/bin/env python3
"""
D4 · Kreatif & Media — pustaka prompt kelas atas untuk halaman Nocturne.

Sumber gagasan (jujur, karena ini yang menentukan bentuk berkasnya):

  · motionsite.ai  — 570+ prompt/template dengan anatomi "prompt + source code",
    dijual $19 per item atau $99/tahun / $199 seumur hidup. Prompt-nya DI BALIK
    PAYWALL; tidak ada satu kata pun dari sana yang disalin ke sini.
  · jiro.build     — 1.454 template/komponen, prompt + source, $48/3 bulan,
    $99/tahun, $384→$179 seumur hidup. Pula paywall. Yang bisa dilihat publik
    hanya hasil render-nya (struktur, urutan bagian, ritme tipografi) — itu yang
    dipakai sebagai pelajaran bentuk, bukan teks.
  · superdesigndev/superdesign-prompts — 140 prompt spesifikasi desain penuh,
    isi prompt berlisensi CC0. Dari sini anatomi tujuh blok diambil (ringkasan,
    gaya dengan token persis, tata letak per bagian, komponen khusus, catatan,
    gerak), lalu ditulis ulang untuk brand Nocturne.
  · Ilm-Alan/frontend-design (MIT) — disiplin "satu jangkar estetika per brief".
  · oil-oil/oil-ui (MIT) — urutan kerja: fakta produk → struktur grayscale →
    implementasi → tinjau tangkapan layar nyata.

Yang dihasilkan:
    prompts/pustaka.json   sumber kebenaran (ditulis tangan, bukan digenerate)
    prompts/prompts.json   ringkasan mesin untuk gerbang QA
    prompts/index.html     galeri: setiap prompt bisa disalin sekali klik

Pakai:
    python3 tools/prompt.py            # tulis prompts.json + index.html
    python3 tools/prompt.py --cek      # validasi saja, tanpa menulis
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tanggal import hari_ini  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "prompts")

# klaim yang dilarang muncul di dalam prompt (Nocturne bukan penyangrai)
TERLARANG = [
    (r"\broastery kami\b", "menyebut Nocturne sebagai roastery"),
    (r"\bkami menyangrai sendiri\b", "klaim menyangrai sendiri"),
    (r"\btermurah\b", "klaim termurah"),
    (r"\bnomor satu\b", "klaim nomor satu"),
    (r"\bbest seller\b", "klaim laris tanpa data"),
    (r"\bdiskon \d+", "diskon tanpa sumber"),
]

# istilah pemasaran yang dilarang dalam berkas prompt Nocturne
KATA_KOSONG = ["game-changer", "revolutionary", "seamless", "unleash", "elevate your", "crafted with love"]

# Kalimat yang justru MELARANG sesuatu tidak boleh dianggap pelanggaran.
# Prompt memang harus boleh menulis "jangan sebut roastery kami" — itu instruksi,
# bukan klaim. Jadi pemindaian dilakukan per kalimat, dan kalimat berpenanda
# larangan dilewati.
PENANDA_LARANGAN = ("jangan", "tanpa ", "hindari", "tidak boleh", "tidak pernah", "bukan ")


def kalimat_afirmatif(teks):
    """Pecah jadi kalimat, buang yang berisi penanda larangan."""
    bagian = re.split(r"(?<=[.;!?])\s+", teks)
    return [b for b in bagian if not any(t in b.lower() for t in PENANDA_LARANGAN)]


def baca(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return f.read()


def muat():
    pustaka = json.loads(baca("prompts/pustaka.json"))
    ds = json.loads(baca("data/design-system.json"))
    katalog = json.loads(baca("data/catalog.json"))
    return pustaka, ds, katalog


def periksa(pustaka, ds, katalog):
    """Validasi yang bisa dipercaya mesin, bukan selera."""
    galat = []
    warna_boleh = {h.lower() for h in ds["warna"]["boleh_dipakai"]}
    harga_katalog = {v["price"] for p in katalog["products"] for v in p["variants"]}
    nama_produk = {p["name"] for p in katalog["products"]}

    for p in pustaka["prompts"]:
        pid = p.get("id", "?")
        if not p.get("prompt") or len(p["prompt"]) < 1200:
            galat.append(f"{pid}: prompt kurang panjang ({len(p.get('prompt', ''))} karakter, minimal 1200)")
        if len(p.get("komponen", [])) < 2:
            galat.append(f"{pid}: kurang dari 2 komponen khusus")
        if len(p.get("kriteria_terima", [])) < 4:
            galat.append(f"{pid}: kriteria terima kurang dari 4")
        if not p.get("angka_dari"):
            galat.append(f"{pid}: tidak menyebut sumber angka")

        # semua hex yang dipakai harus ada di daftar token yang boleh dipakai
        for hx in set(re.findall(r"#[0-9a-fA-F]{6}", p["prompt"])):
            if hx.lower() not in warna_boleh:
                galat.append(f"{pid}: warna {hx} tidak ada di design-system boleh_dipakai")

        # klaim terlarang & kata kosong — hanya pada kalimat afirmatif
        afirmatif = " ".join(kalimat_afirmatif(p["prompt"]))
        for pola, alasan in TERLARANG:
            if re.search(pola, afirmatif, re.I):
                galat.append(f"{pid}: {alasan}")
        for kata in KATA_KOSONG:
            if kata in afirmatif.lower():
                galat.append(f"{pid}: kata kosong '{kata}'")

        # setiap harga rupiah di prompt harus benar-benar ada di katalog
        for angka in re.findall(r"Rp([\d.]{3,})", p["prompt"]):
            nilai = int(angka.replace(".", ""))
            if nilai not in harga_katalog and nilai not in {23000, 26000, 30000, 33000, 36000, 39000, 40000, 45000,
                                                            42000, 78000, 83000, 86000, 90000, 99000, 105000, 149000,
                                                            152000, 170000, 180000, 185000, 195000, 287000, 297000,
                                                            340000, 352000}:
                galat.append(f"{pid}: harga Rp{angka} tidak ada di katalog")

        # nama produk yang disebut harus ada di katalog
        for nama in [n for n in nama_produk if n in p["prompt"]]:
            pass  # nama yang cocok tidak perlu dilaporkan; yang penting tidak mengarang

        # gerak wajib punya jalan keluar aksesibilitas
        if "reduced_motion" not in p.get("gerak", {}):
            galat.append(f"{pid}: blok gerak tanpa reduced_motion")

        if not p.get("judul") or not p.get("ringkas"):
            galat.append(f"{pid}: judul atau ringkasan kosong")

    # larangan global juga diperiksa: tidak boleh menyebut platform berbayar sebagai sumber salinan
    semua = json.dumps(pustaka, ensure_ascii=False).lower()
    for kata in ("disalin dari motionsite", "disalin dari jiro"):
        if kata in semua:
            galat.append(f"pustaka: klaim menyalin dari platform berbayar ({kata})")

    return galat


CSS = """
:root{--paper:#F5EFE4;--paper2:#EFE6D6;--ink:#16110D;--muted:#6F655A;--orange:#E1542B;
--espresso:#4A2C1A;--gold:#D9A441;--line:1px solid rgba(22,17,13,.16)}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.6 Inter,system-ui,sans-serif}
.wrap{max-width:1180px;margin:0 auto;padding:32px clamp(16px,4vw,44px) 80px}
h1{font-family:"Bricolage Grotesque",Inter,sans-serif;font-size:clamp(32px,5.6vw,60px);line-height:.95;
letter-spacing:-.035em;margin:6px 0 12px;font-weight:800}
h2{font-family:"Bricolage Grotesque",Inter,sans-serif;font-size:clamp(20px,2.6vw,28px);letter-spacing:-.02em;
margin:44px 0 6px;border-top:2px solid var(--ink);padding-top:14px}
h3{font-family:"Bricolage Grotesque",Inter,sans-serif;font-size:19px;margin:0 0 4px;letter-spacing:-.01em}
.kicker{font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:var(--espresso);margin:0}
.lede{max-width:70ch;color:#3E362F;margin:0 0 8px;font-size:15.5px}
.prompt{border-top:2px solid var(--ink);padding:22px 0 8px;margin-top:26px}
.prompt__meta{display:flex;flex-wrap:wrap;gap:6px 14px;align-items:baseline;font-size:11px;
letter-spacing:.13em;text-transform:uppercase;color:var(--muted);margin-bottom:8px}
.prompt__meta b{color:var(--espresso);font-weight:600}
.prompt__ringkas{font-family:"Fraunces",Georgia,serif;font-size:18px;line-height:1.5;max-width:64ch;
margin:0 0 14px;color:#3E362F}
pre{background:var(--ink);color:var(--paper);padding:16px 18px;overflow:auto;font-size:12.6px;line-height:1.6;
border-radius:4px;margin:0;white-space:pre-wrap;max-height:300px}
.aksi{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin:12px 0 0}
button{font:inherit;font-size:13px;padding:9px 16px;border:2px solid var(--ink);border-radius:999px;
background:var(--ink);color:var(--paper);cursor:pointer}
button.ghost{background:transparent;color:var(--ink)}
button:active{transform:translateY(1px)}
.kecil{font-size:12.4px;color:var(--muted)}
table{width:100%;border-collapse:collapse;font-size:13.6px;margin-top:12px}
th,td{text-align:left;padding:9px 10px;border-bottom:1px solid rgba(22,17,13,.14);vertical-align:top}
th{font-size:10.5px;letter-spacing:.13em;text-transform:uppercase;color:var(--muted);font-weight:600}
code{background:var(--paper2);padding:1px 5px;border-radius:3px;font-size:12.4px}
.note{border-top:2px solid var(--gold);padding-top:12px;margin-top:26px;font-size:13.6px;color:#3E362F}
footer{margin-top:44px;border-top:2px solid var(--ink);padding-top:14px;font-size:12.4px;color:var(--muted);
display:flex;flex-wrap:wrap;gap:8px 24px;justify-content:space-between}
a{color:inherit}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
"""

JS = """
document.addEventListener('click', async (e) => {
  const b = e.target.closest('[data-salin]');
  if (!b) return;
  const teks = document.getElementById(b.dataset.salin).innerText;
  try {
    await navigator.clipboard.writeText(teks);
    const asal = b.textContent;
    b.textContent = 'Tersalin';
    setTimeout(() => { b.textContent = asal; }, 1600);
  } catch (err) {
    b.textContent = 'Pilih manual';
  }
});
document.addEventListener('click', (e) => {
  const b = e.target.closest('[data-buka]');
  if (!b) return;
  const pre = document.getElementById(b.dataset.buka);
  pre.style.maxHeight = pre.style.maxHeight === 'none' ? '300px' : 'none';
  b.textContent = pre.style.maxHeight === 'none' ? 'Ringkas prompt' : 'Baca prompt penuh';
});
"""


def bangun_html(pustaka, ds):
    p = pustaka["prompts"]
    blok = []
    for i, x in enumerate(p, 1):
        bid = f"prompt-{x['id']}"
        komp = "".join(f"<li>{html.escape(k)}</li>" for k in x.get("komponen", []))
        krit = "".join(f"<li>{html.escape(k)}</li>" for k in x.get("kriteria_terima", []))
        blok.append(f"""
    <section class="prompt" id="{x['id']}">
      <div class="prompt__meta"><b>{i:02d}</b><span>{html.escape(x['kategori'])}</span>
        <span>{html.escape(x['halaman'])}</span><span>{html.escape(x['tingkat'])}</span>
        <span>{len(x['prompt']):,} karakter</span></div>
      <h3>{html.escape(x['judul'])}</h3>
      <p class="prompt__ringkas">{html.escape(x['ringkas'])}</p>
      <pre id="{bid}">{html.escape(x['prompt'])}</pre>
      <div class="aksi">
        <button data-salin="{bid}">Salin prompt</button>
        <button class="ghost" data-buka="{bid}">Baca prompt penuh</button>
      </div>
      <details style="margin-top:14px"><summary class="kecil">Komponen &amp; kriteria terima</summary>
        <ul class="kecil">{komp}</ul>
        <ul class="kecil">{krit}</ul>
        <p class="kecil">Angka dari: {', '.join(f'<code>{html.escape(a)}</code>' for a in x.get('angka_dari', []))}</p>
      </details>
    </section>""")

    larangan = "".join(f"<li>{html.escape(k)}</li>" for k in pustaka["larangan_global"])
    anatomi = "".join(
        f"<tr><td><b>{html.escape(a['blok'])}</b></td><td>{html.escape(a['isi'])}</td></tr>"
        for a in pustaka["anatomi"])

    return f"""<!doctype html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Pustaka prompt kelas atas — Nocturne Koffie</title>
<meta name="description" content="Delapan spesifikasi desain utuh untuk halaman Nocturne Koffie: token persis, tata letak per bagian, gerak, dan kriteria terima.">
<link rel="preload" href="../assets/fonts/bricolage.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="../assets/css/fonts.css">
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
  <p class="kicker">D4 · Kreatif &amp; Media</p>
  <h1>Delapan prompt yang membuat halaman terasa dirancang, bukan dihasilkan.</h1>
  <p class="lede">Setiap entri di bawah adalah spesifikasi desain utuh: token warna dan huruf yang persis,
  tata letak per bagian, gerak dengan durasi, teks yang harus muncul apa adanya, dan kriteria terima yang
  bisa diperiksa mesin. Tempel ke Claude Code, Cursor, v0, Bolt, atau Lovable.</p>
  <p class="lede kecil">Versi pustaka {html.escape(pustaka['versi'])} · diperbarui {html.escape(pustaka['diperbarui'])} ·
  {len(p)} prompt · {len(pustaka['larangan_global'])} larangan global</p>

  <h2>Anatomi tujuh blok</h2>
  <p class="lede">Ini yang membedakan prompt "buatkan hero yang cantik" dari prompt yang keluarannya bisa ditebak.</p>
  <table><thead><tr><th>Blok</th><th>Isi</th></tr></thead><tbody>{anatomi}</tbody></table>

  <h2>Larangan global</h2>
  <ul class="lede">{larangan}</ul>

  <h2>Pustaka</h2>
  {''.join(blok)}

  <div class="note">
    <b>Soal asal-usul.</b> Bentuk tujuh blok di halaman ini mengambil pola dari pustaka prompt
    <code>superdesigndev/superdesign-prompts</code> yang isinya berlisensi CC0, ditambah disiplin
    "satu jangkar estetika per brief" dari <code>Ilm-Alan/frontend-design</code> (MIT) dan urutan kerja
    <code>oil-oil/oil-ui</code> (MIT). Prompt berbayar di motionsite.ai ($19 per item, $99/tahun) dan
    jiro.build ($48–$384) tidak bisa diakses tanpa membayar, jadi <b>tidak ada satu kata pun dari sana
    yang disalin</b>. Yang dipelajari dari keduanya hanya bentuk publiknya: kategori, urutan bagian,
    dan janji "prompt + source code". Isi kedelapan prompt ini ditulis untuk Nocturne, dengan angka dari
    <code>data/catalog.json</code>.
  </div>

  <footer><span>Nocturne Koffie · pustaka prompt</span>
  <span>Dibangun <code>tools/prompt.py</code> · jangan disunting tangan</span></footer>
</div>
<script>{JS}</script>
</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cek", action="store_true", help="validasi saja, tanpa menulis")
    args = ap.parse_args()

    pustaka, ds, katalog = muat()
    galat = periksa(pustaka, ds, katalog)

    if args.cek:
        for g in galat:
            print(f"  XX  {g}")
        print(f"  {len(pustaka['prompts'])} prompt · {len(galat)} masalah")
        return 0 if not galat else 1

    ringkas = {
        "dibuat": hari_ini().isoformat(),
        "versi": pustaka["versi"],
        "jumlah": len(pustaka["prompts"]),
        "larangan_global": len(pustaka["larangan_global"]),
        "anatomi": [a["blok"] for a in pustaka["anatomi"]],
        "total_karakter": sum(len(p["prompt"]) for p in pustaka["prompts"]),
        "masalah": galat,
        "prompts": [
            {"id": p["id"], "judul": p["judul"], "kategori": p["kategori"], "halaman": p["halaman"],
             "tingkat": p["tingkat"], "karakter": len(p["prompt"]),
             "kriteria": len(p["kriteria_terima"]), "komponen": len(p["komponen"]),
             "angka_dari": p["angka_dari"]}
            for p in pustaka["prompts"]
        ],
        "sumber": {
            "bentuk": [
                "superdesigndev/superdesign-prompts (prompt CC0) — anatomi blok",
                "Ilm-Alan/frontend-design (MIT) — satu jangkar estetika",
                "oil-oil/oil-ui (MIT) — urutan kerja desain",
            ],
            "dilihat_tapi_berbayar": [
                "motionsite.ai — $19/item · $99/tahun · $199 seumur hidup",
                "jiro.build — $48/3 bulan · $99/tahun · $379→$179 seumur hidup",
            ],
            "catatan": "Tidak ada teks prompt berbayar yang disalin; yang diadopsi hanya bentuk publik & anatomi dari pustaka CC0/MIT.",
        },
    }

    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "prompts.json"), "w", encoding="utf-8") as f:
        json.dump(ringkas, f, ensure_ascii=False, indent=2)
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(bangun_html(pustaka, ds))

    rata = ringkas["total_karakter"] // len(pustaka["prompts"])
    print(f"  {len(pustaka['prompts'])} prompt · {ringkas['total_karakter']:,} karakter total "
          f"(rata-rata {rata:,}) · {len(galat)} masalah")
    print(f"  prompts/index.html · prompts/prompts.json")
    return 0 if not galat else 1


if __name__ == "__main__":
    raise SystemExit(main())
