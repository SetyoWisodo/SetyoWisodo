#!/usr/bin/env python3
"""Baca katalog reacher-z/Awesome-REA dari sini, dan periksa catatan baru sebelum ditambahkan.

Kenapa ada berkas ini: katalog itu disimpan sebagai JSON besar di repo lain
(`data/tool-resources.json` 3,5 MB, `data/papers.json` 1,3 MB). Untuk menjawab
"ada alat untuk target protokol?" tidak perlu mengkloning 54 MB — cukup ambil
satu berkas lewat GitHub API, simpan di cache, lalu saring dengan field yang
memang dipakai repo itu sendiri: `kind`, `relationship`, `category`, `targets`.

Dua mode:

    cari    → baca katalog (butuh jaringan ke api.github.com)
    periksa → periksa satu berkas catatan lokal terhadap aturan format katalog
              (luring; ini yang dipakai sebelum mengusulkan entri)

Aturan yang ditegakkan `periksa` diambil dari `data/README.md` + `scripts/validate.py`
upstream, bukan dikarang: field wajib, kosakata `relationship`/`kind`/`targets`/`class`,
`verification` harus `source-reviewed`, tanggal tinjauan tidak di masa depan,
tautan bukti bukan akar repo dan tautan `blob`/`tree` GitHub wajib menyebut commit,
`reconstruction_method` hanya untuk case study game, dan `requirements` tidak boleh
berisi kalimat tentang tinjauan katalog itu sendiri.

Pakai:
    python3 scripts/rea_catalog.py cari ghidra
    python3 scripts/rea_catalog.py cari --target protocol --relasi foundation
    python3 scripts/rea_catalog.py cari --target app --kategori agent-mcp --batas 10
    python3 scripts/rea_catalog.py cari --rea --relasi official-skill
    python3 scripts/rea_catalog.py cari --kertas "code reconstruction"
    python3 scripts/rea_catalog.py periksa catatan-saya.json
"""

from __future__ import annotations

import datetime as dt
import json
import os
import re
import subprocess
import sys

REPO = "reacher-z/Awesome-REA"
CACHE = os.path.join(os.environ.get("TMPDIR", "/tmp"), "rea-cache")
BERKAS = {"alat": "data/tool-resources.json", "rea": "data/rea-resources.json",
          "kertas": "data/papers.json"}

# --- kosakata upstream (RELATIONSHIPS, KINDS, TARGETS, CLASSES di build_readme.py) ---
RELASI = {
    "official-core", "official-skill", "official-documentation", "official-guide",
    "official-case-study", "community-integration", "community-learning-resource",
    "community-reported-mixed-workflow", "upstream-maintainer-companion-list",
    "independent-agent-integration", "independent-reconstruction", "foundation", "learning",
}
JENIS = {"project", "tool", "integration", "case-study", "collection", "documentation",
         "learning-resource", "research"}
TARGET = {"website", "game", "app", "binary", "firmware", "protocol"}
KELAS = {"software", "game", "apps", "website", "science", "hardware"}
METODE = {"matching-decompilation", "decompilation", "static-recompilation", "port",
          "engine-reimplementation", "other"}
WAJIB = ["id", "name", "url", "category", "kind", "targets", "relationship",
         "description_en", "description_zh", "evidence_url", "verified_at",
         "verification", "requirements"]
OPSIONAL = ["additional_evidence_urls", "added_at", "class", "requirement_facets",
            "reconstruction_method"]


# ------------------------------------------------------------------ jaringan ---
def ambil(nama: str) -> list:
    """Ambil satu berkas JSON katalog lewat GitHub API; cache 12 jam."""
    os.makedirs(CACHE, exist_ok=True)
    jalur = os.path.join(CACHE, nama)
    segar = os.path.exists(jalur) and (
        dt.datetime.now().timestamp() - os.path.getmtime(jalur) < 12 * 3600)
    if not segar:
        p = subprocess.run(
            ["gh", "api", f"repos/{REPO}/contents/{BERKAS[nama]}",
             "-H", "Accept: application/vnd.github.raw"],
            capture_output=True, text=True, timeout=180)
        if p.returncode != 0:
            if os.path.exists(jalur):
                print(f"  · GitHub API gagal ({p.stderr.strip()[:90]}); memakai cache lama",
                      file=sys.stderr)
            else:
                print(f"  XX GitHub API gagal: {p.stderr.strip()[:160]}", file=sys.stderr)
                print("     coba: gh auth status  · atau unduh manual ke " + jalur, file=sys.stderr)
                sys.exit(2)
        else:
            with open(jalur, "w", encoding="utf-8") as f:
                f.write(p.stdout)
    with open(jalur, encoding="utf-8") as f:
        return json.load(f)


def cari(args: list[str]) -> int:
    kata = [a for a in args if not a.startswith("-") and not a.startswith("--")
            and a != nilai(args, "--target") and a != nilai(args, "--relasi")
            and a != nilai(args, "--kategori") and a != nilai(args, "--batas")]
    target = nilai(args, "--target")
    relasi = nilai(args, "--relasi")
    kategori = nilai(args, "--kategori")
    batas = int(nilai(args, "--batas") or 20)
    kertas = "--kertas" in args or nilai(args, "--kertas") is not None
    # tiga berkas katalog: alat (tool-resources), rea (rea-resources: relasi resmi
    # ke proyek REA), kertas (papers). Satu perintah bisa menyebut salah satunya.
    nama = "kertas" if kertas else ("rea" if "--rea" in args else "alat")
    data = ambil(nama)

    hasil = []
    for r in data:
        teks = json.dumps(r, ensure_ascii=False).lower()
        if kata and not all(k.lower() in teks for k in kata):
            continue
        if target and target not in (r.get("targets") or []):
            continue
        if relasi and r.get("relationship") != relasi:
            continue
        if kategori and r.get("category") != kategori:
            continue
        hasil.append(r)

    if not hasil:
        print("  tidak ada yang cocok. Cek kosakata: --target "
              + "/".join(sorted(TARGET)) + " · --relasi " + "/".join(sorted(RELASI))[:60] + "…")
        return 0
    print(f"  {len(hasil)} dari {len(data)} catatan ({BERKAS[nama]}) · menampilkan {min(batas, len(hasil))}")
    print()
    for r in hasil[:batas]:
        judul = r.get("name", r.get("id"))
        baris2 = [r.get("kind", ""), r.get("relationship", "")]
        if r.get("category"):
            baris2.append(r["category"])
        if r.get("targets"):
            baris2.append("target: " + ",".join(r["targets"]))
        if r.get("year"):
            baris2.insert(0, str(r["year"]))
        print(f"  {judul}")
        print(f"    {' · '.join(x for x in baris2 if x)}")
        print(f"    {r.get('url')}")
        print(f"    diperiksa {r.get('verified_at', '?')} · {r.get('verification', '?')}")
        ringkas = re.sub(r"\s+", " ", (r.get("description_en") or r.get("summary_en") or ""))[:220]
        if ringkas:
            print(f"    {ringkas}")
        print()
    if len(hasil) > batas:
        print(f"  … {len(hasil) - batas} lagi (naikkan --batas)")
    return 0


# ------------------------------------------------------------------- periksa ---
def periksa(jalur: str) -> int:
    if not os.path.exists(jalur):
        print(f"  XX berkas tidak ada: {jalur}")
        return 2
    with open(jalur, encoding="utf-8") as f:
        isi = json.load(f)
    catatan = isi if isinstance(isi, list) else isi.get("records", [isi])
    m: list[str] = []
    hari = dt.date.today()
    for r in catatan:
        rid = r.get("id", "?")
        for k in WAJIB:
            if k not in r or r[k] in ("", [], None):
                m.append(f"{rid}: field wajib `{k}` kosong")
        if not re.match(r"^[a-z0-9][a-z0-9-]*$", str(rid)):
            m.append(f"{rid}: id harus slug huruf kecil/angka/strip")
        if r.get("kind") not in JENIS:
            m.append(f'{rid}: kind "{r.get("kind")}" di luar kosakata')
        if r.get("relationship") not in RELASI:
            m.append(f'{rid}: relationship "{r.get("relationship")}" di luar kosakata')
        t = r.get("targets") or []
        if not isinstance(t, list) or not t:
            m.append(f"{rid}: targets harus daftar tidak kosong")
        for x in t:
            if x not in TARGET:
                m.append(f'{rid}: target "{x}" di luar kosakata')
        if r.get("verification") != "source-reviewed":
            m.append(f'{rid}: verification harus "source-reviewed" (bukan klaim dijalankan)')
        if "class" in r:
            if r["class"] not in KELAS:
                m.append(f'{rid}: class "{r["class"]}" di luar kosakata')
            if r.get("kind") != "case-study":
                m.append(f"{rid}: `class` hanya untuk record data (case-study)")
        if "reconstruction_method" in r:
            if r["reconstruction_method"] not in METODE:
                m.append(f'{rid}: reconstruction_method "{r["reconstruction_method"]}" tak dikenal')
            if "game" not in t:
                m.append(f"{rid}: reconstruction_method hanya untuk case study game")
        bukti = r.get("evidence_url", "")
        if bukti and re.match(r"^https://github\.com/[^/]+/[^/]+/?$", bukti):
            m.append(f"{rid}: tautan bukti tidak boleh akar repo — tautkan README/tree di commit")
        if "/blob/" in bukti or "/tree/" in bukti:
            if not re.search(r"/(?:blob|tree)/[0-9a-f]{7,40}/", bukti):
                m.append(f"{rid}: tautan bukti GitHub harus menyebut commit yang ditinjau")
        v = r.get("verified_at", "")
        if not re.match(r"^\d{4}-\d{2}-\d{2}", str(v)):
            m.append(f"{rid}: verified_at bukan tanggal ISO")
        else:
            try:
                tgl = dt.date.fromisoformat(str(v)[:10])
                if tgl > hari + dt.timedelta(days=1):
                    m.append(f"{rid}: verified_at {tgl} di masa depan")
            except ValueError:
                m.append(f"{rid}: verified_at tidak bisa dibaca")
        req = r.get("requirements")
        if not isinstance(req, list) or not req or any(not str(x).strip() for x in req):
            m.append(f"{rid}: requirements harus daftar tidak kosong")
        else:
            panjang = sum(len(str(x)) for x in req)
            if panjang > 1500:
                m.append(f"{rid}: requirements {panjang} karakter (anjuran ≤ 1500)")
            for x in req:
                if re.search(r"\b(this catalog|katalog ini|did not run|nor reproduced)\b", str(x), re.I):
                    m.append(f'{rid}: requirements menyebut tinjauan katalog sendiri — hapus, itu bukan fakta proyek')
        facet = r.get("requirement_facets")
        if facet is not None:
            if not isinstance(facet, list) or len(facet) != len(req or []):
                m.append(f"{rid}: requirement_facets harus sepanjang requirements")
            else:
                for x in facet:
                    if x not in {"prerequisites", "scope", "limits", "testing", "license", "attribution"}:
                        m.append(f'{rid}: facet "{x}" di luar kosakata')
        for k in r:
            if k not in WAJIB and k not in OPSIONAL:
                m.append(f"{rid}: field asing `{k}` (bukan bagian format katalog)")
        if r.get("name") and len(str(r["name"])) > 100 and r.get("kind") == "case-study":
            m.append(f"{rid}: nama case study > 100 karakter")
    for x in m:
        print("  ✗", x)
    print(f"  kesimpulan: {len(catatan)} catatan · "
          + ("format katalog terpenuhi" if not m else f"{len(m)} masalah"))
    return 0 if not m else 1


# ------------------------------------------------------------------- bantuan ---
def nilai(args: list[str], kunci: str) -> str | None:
    if kunci in args:
        i = args.index(kunci)
        if i + 1 < len(args):
            return args[i + 1]
    return None


def utama() -> int:
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help", "bantuan"):
        print(__doc__)
        return 0
    if args[0] == "cari":
        return cari(args[1:])
    if args[0] == "periksa":
        if len(args) < 2:
            print("  XX sebutkan berkas JSON yang diperiksa")
            return 2
        return periksa(args[1])
    print(f"  XX perintah tidak dikenal: {args[0]} (pakai: cari / periksa)")
    return 2


if __name__ == "__main__":
    sys.exit(utama())
