"""
Impor skill dari teks tempelan → `skills/<slug>/SKILL.md` yang patuh konvensi.

Kenapa ada berkas ini
---------------------
Beberapa skill di proyek ini lahir dari post X, artikel, atau repo yang isinya
disalin pemilik ke chat. Menyalinnya dengan tangan setiap kali menghasilkan tiga
kesalahan berulang: frontmatter lupa, nama di frontmatter tidak sama dengan nama
folder, dan skill-nya tidak pernah masuk daftar di `skills/README.md` — jadi tidak
pernah dipakai lagi.

Alat ini menutup ketiganya: menulis berkas, menyisipkan baris tabel di README,
lalu memeriksa ulang semuanya dengan `--cek`. Yang TIDAK dilakukan: mengarang isi.
Kalau teks sumbernya kosong, alat ini berhenti dan bilang begitu.

Pakai
-----
    # dari berkas
    python3 tools/skill_impor.py --nama rak-gerak --dari /tmp/post.txt \
        --sumber "https://x.com/…/status/…" --judul "Rak Gerak"

    # dari stdin
    pbpaste | python3 tools/skill_impor.py --nama rak-gerak --dari - --sumber "…"

    # periksa seluruh pustaka skill
    python3 tools/skill_impor.py --cek
"""

from __future__ import annotations

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(ROOT, "skills")
README = os.path.join(SKILLS, "README.md")
MIN_DESKRIPSI, MAX_DESKRIPSI = 60, 320


# ------------------------------------------------------------------ baca ----
def baca(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    with open(path, encoding="utf-8") as f:
        return f.read()


def baca_berkas(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()


def tulis(path: str, teks: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(teks)


# --------------------------------------------------------------- frontmatter ---
FM = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)


def punya_frontmatter(teks: str) -> bool:
    return bool(FM.match(teks.lstrip()))


def ambil_frontmatter(teks: str) -> dict:
    m = FM.match(teks.lstrip())
    if not m:
        return {}
    hasil = {}
    kunci = None
    for baris in m.group(1).splitlines():
        if re.match(r"^\w[\w-]*:", baris):
            kunci, nilai = baris.split(":", 1)
            hasil[kunci.strip()] = nilai.strip().strip('"')
        elif kunci and baris.strip():
            hasil[kunci] = (hasil[kunci] + " " + baris.strip()).strip()
    return hasil


def ringkas_deskripsi(teks: str) -> str:
    """Ambil satu-dua kalimat pertama dari isi sebagai `description`."""
    bersih = re.sub(r"\A---.*?---", "", teks, flags=re.S)
    bersih = re.sub(r"^#.*$", "", bersih, flags=re.M)
    paragraf = [p.strip() for p in re.split(r"\n\s*\n", bersih) if p.strip()]
    for p in paragraf:
        satu = re.sub(r"\s+", " ", p)
        if len(satu) >= MIN_DESKRIPSI:
            kalimat = [k for k in re.split(r"(?<=[.!?])\s", satu)
                       if not re.search(r"\b(sumber|gagasan|sumbernya)\b", k, re.I)] or \
                      re.split(r"(?<=[.!?])\s", satu)
            hasil = kalimat[0]
            for k in kalimat[1:]:
                if len(hasil) + len(k) > MAX_DESKRIPSI:
                    break
                hasil += " " + k
            return hasil[:MAX_DESKRIPSI].strip()
    return ""


# ---------------------------------------------------------------- daftar ----
def daftar_skill() -> list[str]:
    if not os.path.isdir(SKILLS):
        return []
    return sorted(d for d in os.listdir(SKILLS)
                  if os.path.isfile(os.path.join(SKILLS, d, "SKILL.md")))


def terdaftar_di_readme(slug: str) -> bool:
    if not os.path.exists(README):
        return False
    return f"({slug}/SKILL.md)" in baca_berkas(README)


# ------------------------------------------------------------------ tulis ---
def impor(nama: str, dari: str, sumber: str = "", judul: str = "",
          deskripsi: str = "", baris_tabel: str = "") -> int:
    slug = re.sub(r"[^a-z0-9-]+", "-", nama.lower()).strip("-")
    if not slug:
        print("XX --nama kosong atau tidak bisa dijadikan slug")
        return 1
    isi = baca(dari).strip()
    if not isi:
        print("XX teks sumber kosong. Tidak ada yang bisa diterapkan — "
              "salin isi post-nya dulu (teks atau tangkapan layar).")
        return 1

    # kalau tempelan sudah punya frontmatter, pakai apa adanya
    if punya_frontmatter(isi):
        fm = ambil_frontmatter(isi)
        if fm.get("name") and fm["name"] != slug:
            print(f"  catatan: frontmatter menamai '{fm['name']}', folder jadi '{slug}'")
            slug = re.sub(r"[^a-z0-9-]+", "-", fm["name"].lower()).strip("-") or slug
        badan = isi[FM.match(isi).end():].lstrip()
        desk = fm.get("description", "")
    else:
        badan = isi
        desk = deskripsi or ringkas_deskripsi(isi)

    if not desk:
        print("XX tidak bisa menyimpulkan `description`. Kirim ulang dengan --deskripsi \"…\"")
        return 1
    if len(desk) > MAX_DESKRIPSI:
        print(f"  catatan: description {len(desk)} karakter, dipotong ke {MAX_DESKRIPSI}")
        desk = desk[:MAX_DESKRIPSI].rsplit(" ", 1)[0]

    judul_akhir = judul or badan.splitlines()[0].lstrip("# ").strip() or slug
    if badan.lstrip().startswith("#"):
        badan = badan.lstrip().split("\n", 1)[1].lstrip("\n")

    kepala = [
        "---",
        f"name: {slug}",
        f"description: {desk}",
        "---",
        "",
        f"# {judul_akhir}",
        "",
    ]
    if sumber:
        kepala += [f"**Sumber:** {sumber}", ""]
    kepala += [badan.rstrip(), ""]

    path = os.path.join(SKILLS, slug, "SKILL.md")
    tulis(path, "\n".join(kepala))

    # daftar di README
    if baris_tabel and not terdaftar_di_readme(slug):
        teks_readme = baca_berkas(README)
        baris = baris_tabel.strip()
        if not baris.startswith("|"):
            baris = f"| [`{slug}`]({slug}/SKILL.md) | D3 + D4 | {baris} |"
        elif f"({slug}/SKILL.md)" not in baris:
            # baris dikirim sudah berbentuk tabel tetapi tanpa kolom nama: sisipkan
            # kolom tautan di depan, jangan menimpa kolom divisi ("D4") — dulu baris
            # seperti ini lolos tapi tidak dianggap terdaftar, dan divisinya hilang.
            sel = baris.split("|")
            baris = "|".join(sel[:1] + [f" [`{slug}`]({slug}/SKILL.md) "] + sel[1:])
        # sisipkan SETELAH baris tabel skill terakhir, bukan di awal berkas
        baris_tabel_skill = list(re.finditer(
            r"^\|\s*\[`[a-z0-9-]+`\]\([a-z0-9-]+/SKILL\.md\)[^\n]*$", teks_readme, flags=re.M))
        if baris_tabel_skill:
            i = baris_tabel_skill[-1].end()
            teks_readme = teks_readme[:i] + "\n" + baris + teks_readme[i:]
        else:
            teks_readme = teks_readme.rstrip() + "\n" + baris + "\n"
        tulis(README, teks_readme)
        print("  skills/README.md · baris tabel ditambahkan")
    elif not terdaftar_di_readme(slug):
        print("  catatan: belum terdaftar di skills/README.md — kirim --baris-tabel \"…\"")

    print(f"  {os.path.relpath(path, ROOT)} · {len(badan.split()):,} kata")
    return 0


# ------------------------------------------------------------------- cek ----
def cek() -> list[str]:
    masalah = []
    daftar = daftar_skill()
    if not daftar:
        masalah.append("tidak ada skill di skills/*/SKILL.md")
    for slug in daftar:
        path = os.path.join(SKILLS, slug, "SKILL.md")
        teks = baca_berkas(path)
        if not punya_frontmatter(teks):
            masalah.append(f"{slug}: tanpa frontmatter (name + description)")
            continue
        fm = ambil_frontmatter(teks)
        if fm.get("name") != slug:
            masalah.append(f"{slug}: name '{fm.get('name')}' ≠ nama folder")
        d = fm.get("description", "")
        if len(d) < MIN_DESKRIPSI:
            masalah.append(f"{slug}: description terlalu pendek ({len(d)} < {MIN_DESKRIPSI})")
        elif len(d) > MAX_DESKRIPSI:
            masalah.append(f"{slug}: description terlalu panjang ({len(d)} > {MAX_DESKRIPSI})")
        bagian = re.findall(r"^## ", teks, flags=re.M)
        if len(bagian) < 3:
            masalah.append(f"{slug}: hanya {len(bagian)} bagian '##' — skill harus bisa dijalankan, bukan cuma ringkasan")
        if not terdaftar_di_readme(slug):
            masalah.append(f"{slug}: tidak terdaftar di skills/README.md")
    # tidak boleh ada catatan kosong / tempat sampah
    for akar, _, berkas in os.walk(SKILLS):
        for b in berkas:
            if b.lower() in ("temp.md", "catatan.md", "untitled.md"):
                masalah.append(f"{os.path.relpath(os.path.join(akar, b), ROOT)}: berkas sementara")
    return masalah


def main() -> int:
    args = sys.argv[1:]
    if "--cek" in args:
        m = cek()
        for x in m:
            print("  ✗", x)
        print(f"  kesimpulan: {len(daftar_skill())} skill · " + ("semua patuh konvensi" if not m else f"{len(m)} masalah"))
        return 0 if not m else 1

    def nilai(kunci, bawaan=""):
        if kunci in args:
            i = args.index(kunci)
            if i + 1 < len(args):
                return args[i + 1]
        return bawaan

    nama = nilai("--nama")
    dari = nilai("--dari")
    if not nama or not dari:
        print(__doc__)
        return 2
    return impor(nama, dari, nilai("--sumber"), nilai("--judul"),
                 nilai("--deskripsi"), nilai("--baris-tabel"))


if __name__ == "__main__":
    sys.exit(main())
