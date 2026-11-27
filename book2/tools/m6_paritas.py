#!/usr/bin/env python3
"""Petakan H3 (subjudul lama) EN -> ID berdasarkan posisi bagian dalam bab.

Masalahnya: jumlah H2 EN dan ID sama, tetapi beberapa seksi ID menggabungkan dua
subjudul EN menjadi satu H2. Akibatnya pemetaan berbasis indeks H2 menggeser H3.

Pendekatan di sini: pakai penanda isi yang tidak diterjemahkan (angka, nama tempat,
sitasi) untuk menyelaraskan seksi, lalu laporkan pasangan yang tidak yakin.
"""
import pathlib
import re
import sys


def kepala_dan_h2(teks: str):
    bagian = re.split(r"(?m)^## ", teks)
    out = []
    for b in bagian[1:]:
        baris = b.split("\n")
        out.append((baris[0].strip(), "\n".join(baris[1:])))
    return bagian[0], out


TANDA = re.compile(r"@[a-z]+\d{4}|[\d][\d.,]*\s?(?:per cent|persen|juta|million|miliar|billion)?|"
                   r"[A-Z][a-z]+(?:\s[A-Z][a-z]+)?")


def sidik(isi: str) -> set[str]:
    return {t.lower() for t in TANDA.findall(isi) if len(t) > 3}


def main() -> None:
    for i in range(1, 18):
        en = pathlib.Path(f"src/en/{i+1:02d}-ch{i:02d}.md")
        idp = pathlib.Path(f"src/id/{i+1:02d}-bab{i:02d}.md")
        _, a = kepala_dan_h2(en.read_text(encoding="utf-8"))
        _, b = kepala_dan_h2(idp.read_text(encoding="utf-8"))
        print(f"### bab {i:02d}: EN {len(a)} H2 / ID {len(b)} H2")
        for j, (judul, isi) in enumerate(a):
            sa = sidik(isi)
            skor = [(len(sa & sidik(isib)) / max(1, len(sa)), k) for k, (_, isib) in enumerate(b)]
            skor.sort(reverse=True)
            best = skor[0] if skor else (0, -1)
            tanda = "" if best[0] > 0.4 else "  <-- ragam"
            print(f"  {j:2} -> ID {best[1]:2} ({best[0]:.2f}) {judul[:46]}{tanda}")


if __name__ == "__main__":
    main()
