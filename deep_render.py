# -*- coding: utf-8 -*-
"""Perakit bab "dalam" (deep chapter) dari modul konten per bab.

Struktur satu bab (dict):
    num, title, theme, nsec
    opening  : list paragraf
    sections : list {num, title, paras: [..]}
    case     : {title, paras}
    future   : {title, paras, table:{caption, head, rows}, after_table:[..]}

Semua prosa ditulis tangan di modul konten; perakit ini hanya menata
markdown agar konsisten dengan renderer PDF (judul ##, tabel [[TABLE:...]]).
"""


def render_chapter(ch, chapter_label="Chapter", lang="en"):
    n = ch["num"]
    nsec = ch.get("nsec", len(ch["sections"]))
    theme_label = "Tema" if lang == "id" else "Theme"
    out = [f"# {chapter_label} {n}: {ch['title']}", "",
           f"*{theme_label}: {ch['theme']}*", ""]

    for p in ch["opening"]:
        out += [p, ""]

    for s in ch["sections"]:
        out += [f"## {s['num']} {s['title']}", ""]
        for p in s["paras"]:
            out += [p, ""]

    case = ch["case"]
    out += [f"## {n}.{nsec + 1} {case['title']}", ""]
    for p in case["paras"]:
        out += [p, ""]

    fut = ch["future"]
    out += [f"## {n}.{nsec + 2} {fut['title']}", ""]
    for p in fut["paras"]:
        out += [p, ""]

    tab = fut.get("table")
    if tab:
        out += [f"[[TABLE:{tab['caption']}]]",
                "| " + " | ".join(tab["head"]) + " |",
                "|" + "|".join(["---"] * len(tab["head"])) + "|"]
        for row in tab["rows"]:
            out += ["| " + " | ".join(row) + " |"]
        out += [""]

    for p in fut.get("after_table", []):
        out += [p, ""]

    out += ["---", ""]
    return out
