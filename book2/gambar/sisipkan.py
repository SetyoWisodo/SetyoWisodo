#!/usr/bin/env python3
"""Sisipkan gambar ke naskah EN + ID.

Caption dan kredit disimpan di gambar/caption.json, bukan di naskah, supaya
satu gambar punya satu caption per bahasa dan tidak ada teks yang digandakan.
Penanda yang disisipkan ke .md sengaja berupa komentar HTML agar bisa dicabut
kembali (lihat --cabut) tanpa menyentuh prosa.

    python3 gambar/sisipkan.py            # sisipkan
    python3 gambar/sisipkan.py --cabut    # hapus semua gambar yang disisipkan
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CAP = ROOT / "gambar" / "caption.json"
AWAL = "<!-- GAMBAR:"
AKHIR = "<!-- /GAMBAR -->"


def blok(cap, lang):
    """Bangun satu blok markdown gambar + caption, path relatif dari naskah."""
    rel = pathlib.PosixPath("..", "..", "gambar", cap["berkas"]).as_posix()
    # Caption adalah alt-text gambar: satu paragraf di bawah gambar, dengan
    # kredit dan lisensi di dalamnya supaya ikut tercetak bersama gambar.
    teks = cap["caption"][lang].strip()
    return (
        f"{AWAL}{cap['kunci']} -->\n"
        f"![{teks}]({rel}){{width=100%}}\n"
        f"\n"
        f"{AKHIR}"
    )


def cabut(teks):
    import re

    pola = re.compile(
        re.escape(AWAL) + r".*?" + re.escape(AKHIR), re.S
    )
    return pola.sub("", teks)


def main():
    caps = json.loads(CAP.read_text(encoding="utf-8"))
    batalkan = "--cabut" in sys.argv
    laporan = []

    # Dikelompokkan per naskah: satu naskah bisa memuat beberapa gambar, dan
    # setiap gambar harus disisipkan ke teks yang sudah dibersihkan sekali saja.
    for lang in ("en", "id"):
        per_naskah = {}
        for cap in caps:
            per_naskah.setdefault(cap["naskah"][lang], []).append(cap)
        for nama, daftar in per_naskah.items():
            sasaran = ROOT / nama
            teks = cabut(sasaran.read_text(encoding="utf-8"))
            if batalkan:
                sasaran.write_text(teks, encoding="utf-8")
                laporan.append(f"CABUT  {lang}/{nama}")
                continue
            for cap in daftar:
                jangkar = cap["jangkar"][lang]
                if jangkar not in teks:
                    laporan.append(f"GAGAL  {lang}/{cap['kunci']}: jangkar tidak ada")
                    continue
                blok_gambar = blok(cap, lang)
                if cap.get("posisi") == "sesudah":
                    # Jangkar berupa judul subbab: gambar diletakkan setelahnya,
                    # supaya pembaca bertemu judul lebih dulu.
                    teks = teks.replace(jangkar, jangkar + "\n\n" + blok_gambar, 1)
                else:
                    teks = teks.replace(jangkar, blok_gambar + "\n\n" + jangkar, 1)
                laporan.append(f"OK     {lang}/{cap['kunci']} -> {nama}")
            teks = re.sub(r"\n{3,}", "\n\n", teks).rstrip() + "\n"
            sasaran.write_text(teks, encoding="utf-8")

    for baris in laporan:
        print(baris)
    print(f"{len(caps)} gambar, mode {'cabut' if batalkan else 'sisip'}")


if __name__ == "__main__":
    main()
