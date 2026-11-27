#!/usr/bin/env python3
"""M6: gabungkan 22-27 H2 menjadi 9-12 seksi bab, EN dan ID dengan struktur identik.

Di HEAD, src/en/NN-chMM.md dan src/id/NN-babMM.md punya jumlah H2 yang sama persis
dan nol H3, jadi satu daftar grup indeks berlaku untuk kedua bahasa.

peta_m6.json:
  { "01": { "seksi": [ {"judul": "...", "judul_id": "...", "h2": [0,1], "tanpa_h3": false}, ... ] } }

Aturan keluaran:
  - H2 pertama tiap grup menjadi H2 baru (judul manual menggantikan judul lama).
  - H2 lain dalam grup menjadi H3 dengan judul lamanya.
  - Bila tanpa_h3 benar, judul lama H2 pertama tidak ditulis (teksnya sudah menyatu
    dengan judul manual).
"""
import json
import pathlib
import re
import sys

PETA = pathlib.Path("reference/peta_m6.json")
HANYA = [a for a in sys.argv[1:] if not a.startswith("--")]


def pecah(teks: str):
    bagian = re.split(r"(?m)^## ", teks)
    seksi = []
    for b in bagian[1:]:
        baris = b.split("\n")
        seksi.append((baris[0].strip(), "\n".join(baris[1:])))
    return bagian[0], seksi


def gabung(teks: str, peta: list[dict], lang: str) -> str:
    kepala, seksi = pecah(teks)
    n = len(seksi)
    dipakai = [i for s in peta for i in s["h2"]]
    assert sorted(dipakai) == list(range(n)), f"indeks tidak lengkap: {n} H2, peta {len(dipakai)}"
    keluar = [kepala.rstrip("\n")]
    for s in peta:
        judul = s["judul"] if lang == "en" else s.get("judul_id", s["judul"])
        keluar.append("## " + judul)
        for j, i in enumerate(s["h2"]):
            tulis_h3 = True
            if j == 0:
                if len(s["h2"]) == 1 or s.get("tanpa_h3"):
                    tulis_h3 = False
            if tulis_h3:
                keluar.append("### " + seksi[i][0])
            keluar.append(seksi[i][1].strip("\n"))
    t = "\n\n".join(keluar).rstrip("\n") + "\n"
    return re.sub(r"\n{4,}", "\n\n\n", t)


def main(aplikasi: bool) -> None:
    peta = json.loads(PETA.read_text(encoding="utf-8"))
    for ch, info in peta.items():
        if HANYA and ch not in HANYA:
            continue
        for lang, pola in (("en", f"{int(ch)+1:02d}-ch{ch}.md"), ("id", f"{int(ch)+1:02d}-bab{ch}.md")):
            p = pathlib.Path("src") / lang / pola
            baru = gabung(p.read_text(encoding="utf-8"), info["seksi"], lang)
            if aplikasi:
                p.write_text(baru, encoding="utf-8")
            h2 = sum(1 for l in baru.splitlines() if l.startswith("## "))
            h3 = sum(1 for l in baru.splitlines() if l.startswith("### "))
            print(f"{'TULIS' if aplikasi else 'CEK  '} {lang}/{pola}: H2={h2} H3={h3}")


if __name__ == "__main__":
    main(aplikasi="--tulis" in sys.argv)
