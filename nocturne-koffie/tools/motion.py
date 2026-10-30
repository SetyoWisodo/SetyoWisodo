#!/usr/bin/env python3
"""
Lab gerak — menerapkan tujuh repo dari post @thegreatest_sv ke D4.

Repo → yang benar-benar dipakai di repo ini:

  nextlevelbuilder/ui-ux-pro-max   disiplin token & "design taste" → data/design-system.json
  pbakaus/impeccable               62 antipattern → tools/slop.py (29 aturan diperiksa mesin)
  GLips/Figma-Context-MCP          spesifikasi layout sebagai sumber → kontrak JSON, bukan tangkapan layar
  DavidHDev/react-bits             komponen animasi → ditulis ulang vanilla di assets/js/motion-ui.js
  greensock/gsap-skills            semantik pin/scrub & aturan performa → loop rAF + aturan audit
  heygen-com/hyperframes           HTML → video → motion/frame-*.html (adegan 9:16 + timeline JSON)
  ahujasid/mcp-for-blender         3D → TIDAK dipakai (tidak ada Blender); diganti bidang CSS 3D

Menulis:
    motion/index.html              lab: komponen hidup, tabel repo, ringkasan audit
    motion/frame-01..05.html       adegan 9:16 dari 5 skrip studio, dengan timeline
    motion/timeline.json           definisi waktu tiap adegan (bahan perekaman)
    motion/data.json               ringkasan untuk papan & laporan

Pakai:
    python3 tools/motion.py
    python3 tools/motion.py --cek
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from html import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tanggal import hari_ini  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "motion")

REPO = [
    {
        "no": 1, "nama": "UI UX Pro Max", "repo": "nextlevelbuilder/ui-ux-pro-max-skill",
        "klaim": "rasa desain untuk agent: 192 palet, 74 pasangan font, aturan per industri",
        "dipakai": "Disiplin token: warna, radius, ukuran font, keluarga font dikunci di "
                   "data/design-system.json lalu dipakai sebagai sumber audit. Palet & font "
                   "tidak diambil dari repo (brand sudah dikunci FINAL 3.7).",
        "tidak": "Instalasi CLI/plugin, katalog palet siap pakai, pencarian font otomatis.",
        "bukti": "data/design-system.json · tools/slop.py (ds-warna, ds-radius, ds-ukuran-font)",
    },
    {
        "no": 2, "nama": "Impeccable", "repo": "pbakaus/impeccable",
        "klaim": "menangkap 'AI slop' sejak ditulis; perintah critique / polish / bolder",
        "dipakai": "62 antipattern-nya jadi daftar periksa audit: 29 di antaranya bisa diukur "
                   "dari berkas (garis sisi tebal, teks gradien, easing memantul, denyut status, "
                   "spasi seragam, label kicker, tanda pisah berlebihan). Temuan nyata langsung diperbaiki.",
        "tidak": "Plugin untuk Claude/Cursor/Copilot, browser-bundle, agen review otomatis.",
        "bukti": "tools/slop.py · laporan/slop.md",
    },
    {
        "no": 3, "nama": "Framelink Figma MCP", "repo": "GLips/Figma-Context-MCP",
        "klaim": "tempel tautan Figma → layout jadi kode, tanpa menebak dari tangkapan layar",
        "dipakai": "Prinsipnya: layout punya sumber yang bisa dibaca mesin. Di sini peran Figma "
                   "digantikan data/design-system.json, dan output tree ringkas dipakai sebagai "
                   "bentuk keluaran audit (satu baris per temuan, bukan tangkapan layar).",
        "tidak": "Server MCP & token Figma: tidak ada akun Figma di lingkungan ini, jadi tidak diklaim.",
        "bukti": "data/design-system.json · laporan/slop.json",
    },
    {
        "no": 4, "nama": "React Bits", "repo": "DavidHDev/react-bits",
        "klaim": "215+ komponen animasi siap tempel",
        "dipakai": "Empat pola ditulis ulang tanpa React: SpotlightCard, CountUp, MagneticButton, "
                   "TextReveal per kata, plus pola pin. Semuanya di assets/js/motion-ui.js, "
                   "dipanggil lewat atribut data-ui.",
        "tidak": "Paket React/Next, registry shadcn, komponen WebGL/three (berat, di atas fold).",
        "bukti": "assets/js/motion-ui.js · assets/css/motion-ui.css · motion/index.html",
    },
    {
        "no": 5, "nama": "GSAP Skills", "repo": "greensock/gsap-skills",
        "klaim": "skill resmi GSAP: timeline, ScrollTrigger, teks, performa",
        "dipakai": "Semantik ScrollTrigger (pin, scrub, start/end) ditiru mini-engine satu loop rAF. "
                   "Aturan performa repo itu jadi gerbang audit: hanya transform/opacity, listener "
                   "pasif, will-change tidak permanen, reduced-motion wajib.",
        "tidak": "GSAP sendiri (≈70 KB + CDN). Belum perlu selama adegan tanpa pin rumit; "
                 "kelas CSS-nya sudah dipisah supaya bisa ditukar nanti.",
        "bukti": "assets/js/motion.js · assets/js/motion-ui.js · tools/slop.py (animasi-layout, listener-pasif)",
    },
    {
        "no": 6, "nama": "HyperFrames", "repo": "heygen-com/hyperframes",
        "klaim": "tulis HTML, dapat video jadi — tanpa After Effects",
        "dipakai": "Adegan 9:16 ditulis sebagai HTML dengan timeline waktu eksplisit "
                   "(motion/frame-01..05.html + motion/timeline.json). Tiap adegan bisa "
                   "diseek (?t=3.2) dan direkam layar, atau dirender ffmpeg di mesin yang punya ffmpeg.",
        "tidak": "Runtime HyperFrames, render server, AI voice/avatar. Encode video tidak "
                 "dijalankan di sandbox ini (tidak ada ffmpeg) — dan tidak diklaim ada.",
        "bukti": "motion/frame-*.html · motion/timeline.json",
    },
    {
        "no": 7, "nama": "MCP for Blender", "repo": "ahujasid/mcp-for-blender",
        "klaim": "Claude membangun adegan 3D nyata dari teks",
        "dipakai": "Tidak ada Blender di lingkungan ini, jadi **tidak dipakai**. Penggantinya: "
                   "bidang miring CSS 3D sederhana (kartu produk) yang tetap ringan, dengan "
                   "batas putar 3,5° — lebih dari itu terasa mainan.",
        "tidak": "Blender, MCP server, Meshy/Tripo (berbayar), aset GLB.",
        "bukti": "assets/js/motion.js §4c (tilt kartu)",
    },
]

CSS = """
:root{--paper:#F5EFE4;--paper2:#EFE6D6;--ink:#16110D;--muted:#6F655A;--orange:#E1542B;
--espresso:#4A2C1A;--gold:#D9A441;--line:1px solid rgba(22,17,13,.16)}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.6 Inter,system-ui,sans-serif}
.wrap{max-width:1180px;margin:0 auto;padding:32px clamp(16px,4vw,44px) 80px}
h1{font-family:"Bricolage Grotesque",Inter,sans-serif;font-size:clamp(34px,6vw,64px);line-height:.94;
letter-spacing:-.04em;margin:8px 0 10px;font-weight:800}
h2{font-family:"Bricolage Grotesque",Inter,sans-serif;font-size:clamp(22px,3vw,32px);letter-spacing:-.025em;
margin:48px 0 6px;border-top:2px solid var(--ink);padding-top:14px}
h3{font-family:"Bricolage Grotesque",Inter,sans-serif;font-size:18px;margin:0 0 6px;letter-spacing:-.01em}
.kicker{font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:var(--muted);margin:0}
.lede{max-width:72ch;color:#3E362F;margin:0 0 10px;font-size:15.5px}
.grid{display:grid;gap:14px}
.kpi{grid-template-columns:repeat(auto-fit,minmax(160px,1fr));margin-top:18px}
.kpi div{border:var(--line);padding:14px 16px;background:#fff8}
.kpi span{display:block;font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
.kpi b{display:block;font-family:"Bricolage Grotesque",Inter,sans-serif;font-size:28px;line-height:1.05;margin:4px 0}
.kpi em{font-style:normal;font-size:11.5px;color:var(--muted)}
table{width:100%;border-collapse:collapse;font-size:13.6px;margin-top:12px}
th,td{text-align:left;padding:9px 10px;border-bottom:1px solid rgba(22,17,13,.14);vertical-align:top}
th{font-size:10.5px;letter-spacing:.13em;text-transform:uppercase;color:var(--muted);font-weight:600}
td b{font-weight:600}
.pill{display:inline-block;font-size:10.5px;padding:2px 8px;border:1px solid var(--espresso);border-radius:99px;
color:var(--espresso);white-space:nowrap}
.pill.no{border-color:rgba(22,17,13,.3);color:var(--muted)}
.pill.ok{background:var(--espresso);color:var(--paper);border-color:var(--espresso)}
.demo{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px;margin-top:18px}
.box{border:2px solid var(--ink);padding:20px;background:rgba(255,255,255,.4)}
.box .num{font-family:"Bricolage Grotesque",Inter,sans-serif;font-size:38px;line-height:1;letter-spacing:-.03em}
.box p{font-size:13.4px;margin:8px 0 0;color:#3E362F}
.box .src{font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin-top:12px}
.btn{display:inline-block;background:var(--orange);color:var(--ink);font-weight:700;text-decoration:none;
padding:14px 22px;border-radius:999px;border:2px solid var(--orange)}
.quote{border-top:2px solid var(--ink);padding-top:12px;margin-top:22px;font-family:"Fraunces",Georgia,serif;
font-style:italic;font-size:19px;line-height:1.5;max-width:60ch}
.lm{display:block;overflow:hidden}
.lm > span{display:block}
.angka{font-variant-numeric:tabular-nums}
.pin{display:grid;grid-template-columns:1.1fr .9fr;gap:24px;margin-top:18px;align-items:start}
@media(max-width:800px){.pin{grid-template-columns:1fr}}
.pin__steps{display:grid;gap:12px}
.pin__step{border-left:0;border-top:1px solid rgba(22,17,13,.18);padding-top:10px}
.pin__step h3{font-size:16px}
.pin__step p{font-size:13.6px;margin:0;color:#3E362F}
.frames{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:14px;margin-top:16px}
.frame{display:block;text-decoration:none;color:inherit}
.frame__media{position:relative;aspect-ratio:9/16;background:var(--ink);overflow:hidden;border-radius:4px}
.frame__media img{width:100%;height:100%;object-fit:cover;display:block;opacity:.9}
.frame__play{position:absolute;inset:auto 0 0 0;padding:10px 12px;background:linear-gradient(transparent,rgba(22,17,13,.85));
color:var(--paper);font-size:11.5px;letter-spacing:.06em}
.frame figcaption{font-size:12.6px;margin-top:8px;line-height:1.45}
code{background:var(--paper2);padding:1px 5px;border-radius:3px;font-size:12.4px}
pre{background:var(--ink);color:var(--paper);padding:14px 16px;overflow:auto;font-size:12.4px;line-height:1.55;
border-radius:4px;margin:12px 0 0}
.note{border-top:2px solid var(--gold);padding-top:12px;margin-top:18px;font-size:13.6px;color:#3E362F}
footer{margin-top:44px;border-top:2px solid var(--ink);padding-top:14px;font-size:12.4px;color:var(--muted);
display:flex;flex-wrap:wrap;gap:8px 24px;justify-content:space-between}
a{color:inherit}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
"""


def baca(*p, default=None):
    q = os.path.join(ROOT, *p)
    if not os.path.exists(q):
        return default
    with open(q, encoding="utf-8", errors="ignore") as f:
        return f.read()


def baca_json(*p, default=None):
    t = baca(*p)
    if t is None:
        return default if default is not None else {}
    return json.loads(t)


# ─────────────────────── adegan 9:16 (gaya HyperFrames) ────────────────────
def baca_skrip():
    """Ambil 5 skrip dari studio/skrip/*.md (dibuat tools/studio.py)."""
    d = os.path.join(ROOT, "studio", "skrip")
    if not os.path.isdir(d):
        return []
    hasil = []
    for f in sorted(os.listdir(d)):
        if not f.endswith(".md"):
            continue
        t = baca("studio", "skrip", f)
        judul = re.search(r"^# Skrip (\d+) — (.+)$", t, re.M)
        hook = re.search(r"```\n(.+?)\n```", t, re.S)
        visual = re.search(r"\*\*Visual \(shot list\):\*\* (.+)", t)
        aset = re.search(r"\*\*Aset:\*\* `([^`]+)`", t)
        sumber = re.search(r"\*\*Sumber data:\*\* (.+)", t)
        cues = []
        mulai = 0.0
        for m in re.finditer(r"^\| (\d+) \| (\d+)s \| (.+?) \| (.+?) \|$", t, re.M):
            dur = float(m.group(2))
            cues.append({"mulai": round(mulai, 2), "durasi": dur,
                         "selesai": round(mulai + dur, 2),
                         "teks": m.group(3).strip(),
                         "sumber": None if m.group(4).strip() in ("—", "-", "") else m.group(4).strip()})
            mulai += dur
        hasil.append({
            "no": int(judul.group(1)) if judul else len(hasil) + 1,
            "berkas": f,
            "judul": hook.group(1).strip() if hook else (judul.group(2) if judul else f),
            "pilar": judul.group(2).split("·")[-1].strip() if judul else "—",
            "visual": visual.group(1).strip() if visual else "—",
            "aset": aset.group(1) if aset else "",
            "sumber": sumber.group(1).strip() if sumber else "—",
            "cues": cues,
            "durasi": round(mulai, 2),
        })
    return hasil


def poster_untuk(aset, kreatif):
    for it in kreatif.get("items", []):
        if it.get("id") == aset:
            for kunci in ("poster", "file"):
                f = it.get(kunci)
                if f and os.path.exists(os.path.join(ROOT, "konten", f)):
                    return "../konten/" + f
    return None


FRAME_CSS = """
:root{--paper:#F5EFE4;--ink:#16110D;--orange:#E1542B;--gold:#D9A441;--espresso:#4A2C1A;--muted:#B8AC9C}
*{box-sizing:border-box}
html,body{margin:0;height:100%;background:#0B0908;color:var(--paper);font-family:Inter,system-ui,sans-serif}
#panggung{position:fixed;inset:0;display:grid;place-items:center}
#kanvas{position:relative;width:1080px;height:1920px;transform-origin:center center;overflow:hidden;
background:radial-gradient(120% 90% at 50% 0%,#241A14 0%,#16110D 58%,#0D0A08 100%)}
#latar{position:absolute;inset:0;background-size:cover;background-position:center;opacity:.22;filter:saturate(.85)}
#butir{position:absolute;inset:0;background:radial-gradient(60% 50% at 50% 70%,rgba(225,84,43,.16),transparent 70%)}
.isi{position:absolute;inset:0;padding:200px 92px 240px;display:block}
.beat{position:absolute;left:92px;right:92px;top:290px;bottom:300px;display:flex;flex-direction:column;
gap:26px;opacity:0;transform:translate3d(0,34px,0);
transition:opacity .42s cubic-bezier(.16,1,.3,1),transform .52s cubic-bezier(.16,1,.3,1)}
.beat.on{opacity:1;transform:none}
.beat--hook{font-family:"Bricolage Grotesque",Inter,sans-serif;font-weight:800;font-size:104px;line-height:.94;
letter-spacing:-.045em;text-wrap:balance}
.beat--isi{font-family:"Bricolage Grotesque",Inter,sans-serif;font-weight:600;font-size:66px;line-height:1.06;
letter-spacing:-.025em;text-wrap:pretty}
.beat--cta{font-family:"Inter",sans-serif;font-weight:600;font-size:42px;line-height:1.25;color:var(--gold);
letter-spacing:-.01em;justify-content:flex-end}
.sumber{font-size:24px;letter-spacing:.08em;color:var(--muted);text-transform:uppercase}
/* versi reduced-motion: semua teks ditumpuk, tidak ada yang disembunyikan */
body.redup .beat{position:static;opacity:1;transform:none;font-size:42px;line-height:1.2;letter-spacing:-.02em;
margin-bottom:22px;font-family:Inter,sans-serif;font-weight:600;color:var(--paper)}
body.redup .beat--cta{color:var(--gold)}
body.redup .isi{justify-content:flex-start;padding-top:190px}
body.redup .beat .sumber{font-size:20px}
.merk{position:absolute;left:92px;top:92px;display:flex;align-items:center;gap:16px}
.merk i{width:22px;height:22px;border-radius:50%;background:var(--gold);box-shadow:inset -2px 0 0 0 #16110D;display:block}
.merk b{font-family:"Bricolage Grotesque",Inter,sans-serif;font-size:30px;letter-spacing:-.02em}
.merk span{font-size:16px;letter-spacing:.26em;text-transform:uppercase;color:var(--muted);display:block;margin-top:2px}
.pilar{position:absolute;right:92px;top:100px;font-size:20px;letter-spacing:.2em;text-transform:uppercase;color:var(--muted)}
.bilah{position:absolute;left:92px;right:92px;bottom:120px;height:4px;background:rgba(245,239,228,.18);overflow:hidden}
.bilah i{display:block;height:100%;width:100%;background:var(--orange);transform:scaleX(0);transform-origin:0 50%}
.kendali{position:fixed;left:50%;bottom:22px;transform:translateX(-50%);display:flex;gap:10px;align-items:center;
background:rgba(22,17,13,.86);border:1px solid rgba(245,239,228,.18);padding:10px 14px;border-radius:999px;
font-size:13px;color:#F5EFE4;z-index:10}
.kendali button{font:inherit;background:transparent;border:1px solid rgba(245,239,228,.35);color:inherit;
padding:6px 12px;border-radius:999px;cursor:pointer}
.kendali button:hover{background:rgba(245,239,228,.12)}
.kendali .waktu{font-variant-numeric:tabular-nums;letter-spacing:.04em;color:#C9BFB2}
@media (prefers-reduced-motion:reduce){.beat{transition:none}}
"""

FRAME_JS = """
(function(){
  var data = window.__ADEgan;
  var beats = Array.prototype.slice.call(document.querySelectorAll('.beat'));
  var bilah = document.querySelector('.bilah i');
  var waktu = document.querySelector('.kendali .waktu');
  var tombol = document.querySelector('.kendali button');
  var mulai = 0, jalan = true, terakhir = 0, t = 0;
  var kurangi = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (kurangi) document.body.classList.add('redup');
  var total = data.durasi;

  function skala() {
    var k = Math.min(window.innerWidth / 1080, (window.innerHeight - 90) / 1920);
    document.getElementById('kanvas').style.transform = 'scale(' + k.toFixed(4) + ')';
  }
  window.addEventListener('resize', skala, { passive: true });
  skala();

  function gambar() {
    beats.forEach(function (b, i) {
      var c = data.cues[i];
      if (!c) return;
      var nyala = kurangi ? true : (t >= c.mulai && t < c.selesai + 0.001);
      b.classList.toggle('on', nyala);
    });
    if (bilah) bilah.style.transform = 'scaleX(' + Math.min(1, t / total).toFixed(4) + ')';
    if (waktu) waktu.textContent = t.toFixed(1) + 's / ' + total.toFixed(1) + 's';
  }

  function loop(ts) {
    if (!terakhir) terakhir = ts;
    var dt = (ts - terakhir) / 1000;
    terakhir = ts;
    if (jalan) {
      t += dt;
      if (t > total) { t = total; jalan = false; if (tombol) tombol.textContent = 'Ulang'; }
      gambar();
    }
    requestAnimationFrame(loop);
  }

  tombol.addEventListener('click', function () {
    if (t >= total) { t = 0; jalan = true; tombol.textContent = 'Jeda'; }
    else { jalan = !jalan; tombol.textContent = jalan ? 'Jeda' : 'Main'; }
    gambar();
  });

  var q = new URLSearchParams(location.search).get('t');
  if (q !== null && !isNaN(parseFloat(q))) { t = Math.min(total, parseFloat(q)); jalan = false; tombol.textContent = 'Main'; }
  gambar();
  if (!kurangi) requestAnimationFrame(loop);
})();
"""


def frame_html(s, poster, tgl):
    beats = []
    for i, c in enumerate(s["cues"]):
        kelas = "beat beat--hook" if i == 0 else ("beat beat--cta" if i == len(s["cues"]) - 1 else "beat beat--isi")
        sumber = f'<div class="sumber">sumber: {escape(c["sumber"])}</div>' if c.get("sumber") else ""
        beats.append(f'<div class="{kelas}" data-i="{i}"><div>{escape(c["teks"])}</div>{sumber}</div>')
    latar = f'<div id="latar" style="background-image:url({escape(poster)})"></div>' if poster else ""
    adegan = {"no": s["no"], "judul": s["judul"], "durasi": s["durasi"], "cues": s["cues"]}
    return f"""<!DOCTYPE html>
<html lang="id"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Adegan {s['no']:02d} — {escape(s['judul'])}</title>
<meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,800&family=Inter:wght@400;600&display=swap" rel="stylesheet">
<style>{FRAME_CSS}</style></head>
<body>
<div id="panggung"><div id="kanvas">
  {latar}<div id="butir"></div>
  <div class="merk"><i></i><div><b>Nocturne</b><span>Koffie · Banyuwangi</span></div></div>
  <div class="pilar">{escape(s['pilar'])}</div>
  <div class="isi">{''.join(beats)}</div>
  <div class="bilah"><i></i></div>
</div></div>
<div class="kendali" role="group" aria-label="Kendali adegan">
  <button type="button">Jeda</button>
  <span class="waktu">0,0s / {s['durasi']:.1f}s</span>
  <span style="color:#8C8175">adegan {s['no']:02d} · {escape(s['judul'][:38])}</span>
</div>
<script>window.__ADEgan = {json.dumps(adegan, ensure_ascii=False)};</script>
<script>{FRAME_JS}</script>
</body></html>
"""


# ───────────────────────────── lab gerak ───────────────────────────────────
def lab(frames, slop, kreatif, tgl):
    berat = (os.path.getsize(os.path.join(ROOT, "assets/css/motion-ui.css"))
             + os.path.getsize(os.path.join(ROOT, "assets/js/motion-ui.js"))) / 1024
    kritis = slop.get("kritis", 0)
    perhatian = slop.get("perhatian", 0)
    aturan = slop.get("aturan_diperiksa", 0)

    baris_repo = "".join(f"""<tr>
      <td><b>{r['no']}. {escape(r['nama'])}</b><br><span class="lede" style="font-size:12px">{escape(r['repo'])}</span></td>
      <td>{escape(r['dipakai'])}</td>
      <td><span class="pill no">{escape(r['tidak'])}</span></td>
      <td><code>{escape(r['bukti'])}</code></td>
    </tr>""" for r in REPO)

    kartu_frame = ""
    for s in frames:
        poster = poster_untuk(s["aset"], kreatif)
        thumb = (f'<img src="{escape(poster)}" alt="Poster adegan {s["no"]:02d}">' if poster
                 else '<div style="height:100%"></div>')
        kartu_frame += f"""<figure class="frame" style="margin:0">
          <a href="frame-{s['no']:02d}.html" class="frame__media" aria-label="Putar adegan {s['no']:02d}">
            {thumb}<span class="frame__play">▶ {s['durasi']:.0f} detik · {len(s['cues'])} beat</span>
          </a>
          <figcaption><b>{escape(s['judul'])}</b><br><span class="lede" style="font-size:12px">{escape(s['pilar'])} · {escape(s['aset'] or "tanpa aset")}</span></figcaption>
        </figure>"""

    cue_rows = ""
    for s in frames:
        for c in s["cues"]:
            cue_rows += (f'<tr><td>{s["no"]:02d}</td><td class="angka">{c["mulai"]:.1f}–{c["selesai"]:.1f}s</td>'
                         f'<td>{escape(c["teks"])}</td><td>{escape(c["sumber"] or "—")}</td></tr>')

    aturan_rows = ""
    for t in slop.get("temuan", []):
        if t["tingkat"] == "info":
            continue
        aturan_rows += (f'<tr><td><code>{escape(t["aturan"])}</code></td><td>{escape(t["berkas"])}</td>'
                        f'<td>{escape(t["bukti"])}</td></tr>')
    if not aturan_rows:
        aturan_rows = '<tr><td colspan="3">Tidak ada temuan kritis maupun perhatian pada audit terakhir.</td></tr>'

    return f"""<!DOCTYPE html><html lang="id"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Lab Gerak — Nocturne Koffie</title>
<meta name="description" content="Komponen gerak dan adegan 9:16 untuk konten D4: spotlight, hitung angka, tombol magnet, pin bertahap, dan audit anti-slop.">
<meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&family=Fraunces:ital,opsz,wght@0,9..144,300;1,9..144,300&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/css/site.css">
<link rel="stylesheet" href="../assets/css/motion-ui.css">
<style>{CSS}</style></head><body>
<div class="ui-progress"><i></i></div>
<div class="wrap">
  <p class="kicker">Divisi D4 · kreatif &amp; media · dibuat {tgl.day} {['Januari','Februari','Maret','April','Mei','Juni','Juli','Agustus','September','Oktober','November','Desember'][tgl.month-1]} {tgl.year}</p>
  <h1 data-ui="words">Lab gerak</h1>
  <p class="lede">Tujuh repo dari post <b>@thegreatest_sv</b> (29 Okt 2026) diterapkan di sini — bukan
  dipasang sebagai plugin, tapi dipakai sebagai <b>aturan dan komponen</b> yang bisa diperiksa ulang.
  Dua di antaranya tidak bisa dipakai di lingkungan ini (Figma dan Blender tidak ada), dan itu ditulis
  apa adanya di kolom kanan.</p>

  <div class="grid kpi">
    <div><span>Repo</span><b>4 + 1</b><em>dipakai utuh + prinsipnya (Figma)</em></div>
    <div><span>Aturan audit</span><b>{aturan}</b><em>{kritis} kritis · {perhatian} perhatian</em></div>
    <div><span>Adegan 9:16</span><b>{len(frames)}</b><em>dari 5 skrip studio</em></div>
    <div><span>Komponen</span><b>6</b><em>vanilla, tanpa React</em></div>
    <div><span>Berat tambahan</span><b>{f"{berat:.1f}".replace(".", ",")} KB</b><em>CSS + JS komponen, tanpa CDN</em></div>
  </div>

  <h2>1 · Tujuh repo, apa yang benar-benar dipakai</h2>
  <p class="lede">Kolom terakhir menunjuk berkas di repo ini — kalau tidak ada bukti, jangan percaya
  klaimnya.</p>
  <table><thead><tr><th>Repo</th><th>Yang dipakai</th><th>Yang tidak</th><th>Bukti</th></tr></thead>
  <tbody>{baris_repo}</tbody></table>

  <h2>2 · Komponen gerak (hidup di halaman ini)</h2>
  <p class="lede">Semua komponen ditulis ulang dari React ke vanilla JS dan dipanggil lewat atribut
  <code>data-ui</code>. Coba: gerakkan kursor di kartu, klik tombol, gulir ke blok pin di bawah.</p>
  <div class="demo">
    <div class="box" data-ui="spotlight">
      <p class="kicker">Spotlight kartu</p>
      <h3>Kartu produk yang menyala di bawah kursor</h3>
      <p>Sorotan mengikuti pointer, mati di perangkat sentuh dan saat reduced-motion — bukan cahaya
      yang berdenyut sendiri.</p>
      <p class="src">react-bits · SpotlightCard → motion-ui.js</p>
    </div>
    <div class="box">
      <p class="kicker">Hitung angka</p>
      <div class="num angka" data-ui="count" data-to="83" data-duration="1100">83</div>
      <p>Ambang QC tampil sebagai angka yang berjalan saat masuk layar. Tanpa overshoot, tanpa
      angka berkedip.</p>
      <p class="src">react-bits · CountUp → motion-ui.js</p>
    </div>
    <div class="box">
      <p class="kicker">Tombol magnet</p>
      <a class="btn" href="frame-01.html" data-ui="magnet">Putar adegan 01 →</a>
      <p style="margin-top:14px">Geseran maksimal 6 px. Lebih dari itu terasa seperti mainan.</p>
      <p class="src">react-bits · MagneticButton → motion-ui.js</p>
    </div>
  </div>

  <div class="pin" data-ui="pin">
    <div>
      <h3 style="margin-bottom:10px">Pin bertahap (semantik ScrollTrigger)</h3>
      <p class="lede">Tiga langkah menyala mengikuti posisi gulir — satu loop <code>requestAnimationFrame</code>,
      listener pasif, tanpa GSAP. Ini yang dipakai untuk menjelaskan proses sangrai di landing page.</p>
      <pre>data-ui="pin"
  .ui-pin__step  ×3   → menyala saat progres 0 → 1</pre>
    </div>
    <div class="pin__steps">
      <div class="pin__step"><h3>01 · Drum mulai</h3><p>Suhu masuk, biji berubah warna.</p></div>
      <div class="pin__step"><h3>02 · First crack</h3><p>Bunyi retak pertama — titik yang menentukan.</p></div>
      <div class="pin__step"><h3>03 · Berhenti di catatan</h3><p>Bukan di perasaan: berhenti saat development tercapai.</p></div>
    </div>
  </div>

  <div class="quote" data-ui="reveal">Gerak yang baik tidak terlihat sebagai gerak.<br>Ia hanya membuat mata tahu ke mana harus pergi.</div>

  <h2>3 · Adegan 9:16 — menulis HTML, bukan merender video</h2>
  <p class="lede">Tiap adegan adalah halaman HTML dengan timeline waktu eksplisit. Bisa diputar,
  dijeda, dan diseek (<code>?t=3.2</code>). Untuk jadi video: rekam layar, atau render ffmpeg di
  mesin yang punya ffmpeg — di sandbox ini tidak ada, dan tidak diklaim ada.</p>
  <div class="frames">{kartu_frame}</div>

  <h3 style="margin-top:26px">Timeline (bahan perekaman)</h3>
  <table><thead><tr><th>Adegan</th><th>Waktu</th><th>Teks</th><th>Sumber klaim</th></tr></thead>
  <tbody>{cue_rows}</tbody></table>
  <p class="lede" style="margin-top:8px">Berkas mesin: <code>motion/timeline.json</code> ·
  satu baris per cue, tanpa angka yang tidak dilacak ke <code>data/</code>.</p>

  <h2>4 · Audit anti-slop terakhir</h2>
  <p class="lede">{aturan} aturan diperiksa mesin dari 62 antipattern Impeccable + aturan performa
  GSAP Skills + kontrak token. Hasil sekarang: <b>{kritis} kritis · {perhatian} perhatian</b>.</p>
  <table><thead><tr><th>Aturan</th><th>Berkas</th><th>Bukti</th></tr></thead><tbody>{aturan_rows}</tbody></table>
  <p class="lede" style="margin-top:8px">Laporan penuh: <a href="../laporan/slop.md">laporan/slop.md</a> ·
  kontrak: <a href="../data/design-system.json">data/design-system.json</a>.</p>

  <h2>5 · Batas yang tidak saya tutupi</h2>
  <div class="note">
    <p style="margin:0 0 8px"><b>Figma MCP</b> — tidak ada akun Figma di sini. Yang diambil prinsipnya:
    layout punya sumber mesin. Sumber itu kini <code>data/design-system.json</code>.</p>
    <p style="margin:0 0 8px"><b>MCP for Blender</b> — Blender tidak ada, aset 3D tidak dibuat.
    Penggantinya bidang miring CSS 3D maksimal 3,5°, bukan model GLB.</p>
    <p style="margin:0 0 8px"><b>HyperFrames</b> — runtime dan render server tidak dipasang. Yang ada:
    adegan HTML deterministik + timeline. Encode video tetap di luar sandbox.</p>
    <p style="margin:0"><b>GSAP</b> — tidak dipasang (≈70 KB + CDN). Semantiknya ditiru; kelas CSS
    dipisah supaya bisa ditukar bila nanti butuh pin/scrub rumit.</p>
  </div>

  <footer>
    <span>Dibuat <code>tools/motion.py</code> · audit <code>tools/slop.py</code> ·
      komponen <code>assets/js/motion-ui.js</code></span>
    <span><a href="../index.html">situs</a> · <a href="../kampanye/index.html">landing kampanye</a> ·
      <a href="../studio/index.html">studio konten</a> · <a href="../konten/index.html">hub konten</a></span>
  </footer>
</div>
<script src="../assets/js/motion-ui.js"></script>
</body></html>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cek", action="store_true")
    args = ap.parse_args()

    tgl = hari_ini()
    frames = baca_skrip()
    kreatif = baca_json("data", "kreatif.json")
    slop = baca_json("laporan", "slop.json", default={})

    print(f"Lab gerak — {tgl.isoformat()}")
    print(f"  repo             : {len(REPO)} (5 dipakai · 1 diganti · 1 tidak dipakai)")
    print(f"  adegan 9:16      : {len(frames)}")
    for s in frames:
        print(f"    {s['no']:02d} {s['durasi']:.0f}s · {len(s['cues'])} beat · {s['judul'][:52]}")
    print(f"  audit            : {slop.get('aturan_diperiksa', 0)} aturan · "
          f"{slop.get('kritis', '—')} kritis · {slop.get('perhatian', '—')} perhatian")

    if args.cek:
        return

    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):
        if f.startswith("frame-") and f.endswith(".html"):
            os.remove(os.path.join(OUT, f))

    timeline = []
    for s in frames:
        poster = poster_untuk(s["aset"], kreatif)
        with open(os.path.join(OUT, f"frame-{s['no']:02d}.html"), "w", encoding="utf-8") as f:
            f.write(frame_html(s, poster, tgl))
        timeline.append({
            "adegan": s["no"], "berkas": f"frame-{s['no']:02d}.html",
            "judul": s["judul"], "pilar": s["pilar"], "durasi": s["durasi"],
            "aset": s["aset"], "poster": poster.replace("../", "") if poster else None,
            "shot_list": s["visual"], "sumber_data": s["sumber"],
            "cues": s["cues"],
        })

    with open(os.path.join(OUT, "timeline.json"), "w", encoding="utf-8") as f:
        json.dump({"dibuat": tgl.isoformat(), "fps_saran": 30,
                   "catatan": "Satu baris per cue. Rekam layar 1080×1920 atau render ffmpeg.",
                   "adegan": timeline}, f, ensure_ascii=False, indent=2)
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(lab(frames, slop, kreatif, tgl))

    ringkas = {
        "dibuat": tgl.isoformat(),
        "repo_total": len(REPO),
        "repo_dipakai_utuh": 4,
        "repo_prinsip_saja": 1,
        "repo_tidak_dipakai": 1,
        "adegan": [{"no": s["no"], "judul": s["judul"], "durasi": s["durasi"],
                    "beat": len(s["cues"]), "berkas": f"motion/frame-{s['no']:02d}.html"} for s in frames],
        "audit": {"aturan": slop.get("aturan_diperiksa", 0),
                  "kritis": slop.get("kritis", 0), "perhatian": slop.get("perhatian", 0)},
        "batas": ["Figma MCP: tanpa akun Figma", "Blender: tidak ada, 3D diganti CSS 3D",
                  "HyperFrames: tanpa render server", "GSAP: tidak dipasang"],
    }
    with open(os.path.join(OUT, "data.json"), "w", encoding="utf-8") as f:
        json.dump(ringkas, f, ensure_ascii=False, indent=2)

    print(f"  halaman          : motion/index.html · timeline.json · data.json · {len(frames)} adegan")


if __name__ == "__main__":
    main()
