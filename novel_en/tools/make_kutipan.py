#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""make_kutipan.py — render research/KUTIPAN_SAINS.md dari kutipan.json."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); R = os.path.join(ROOT, "research")

def main():
    d = json.load(open(os.path.join(R, "kutipan.json"), encoding="utf-8")); k = d["kartu"]
    o = ["# Buku Kutipan Sains — Volume I\n",
         "*Dirender dari `research/kutipan.json`. Jangan sunting berkas ini.*\n",
         "| ID | Klaim | Penulis | Tahun | DOI |", "|---|---|---|---:|---|"]
    for x in k:
        o.append("| %s | %s | %s | %d | `%s` |" % (x["id"], x["klaim"], x["penulis"], x["tahun"], x["doi"]))
    for x in k:
        o += ["\n---\n\n## %s — %s\n" % (x["id"], x["penulis"]),
              "**Klaim.** %s\n" % x["klaim"],
              "**Kutipan.** \u201c%s\u201d\n" % x["kutipan"],
              "**Sumber.** %s, *%s* %s.  \n**DOI.** https://doi.org/%s\n" % (x["penulis"], x["jurnal"], x["volume"], x["doi"]),
              "**Yang dibenarkan.** %s\n" % x["lisensi_klaim"],
              "**Yang TIDAK dibenarkan.** %s\n" % x["batas_klaim"]]
        if x.get("catatan"): o.append("**Catatan.** %s\n" % x["catatan"])
    o.append("\n## Fiksi yang tidak boleh diklaim sebagai sains\n")
    o += ["- %s" % y for y in d["fiksi_yang_tidak_boleh_diklaim_sebagai_sains"]]
    open(os.path.join(R, "KUTIPAN_SAINS.md"), "w", encoding="utf-8").write("\n".join(o) + "\n")

if __name__ == "__main__":
    main()
