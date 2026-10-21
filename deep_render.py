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


def _load_extra(lang, n):
    """Lapisan pendalaman bertanda tangan, terpisah dari modul bab.

    Kunci: nomor sub-bab ("4.3") atau "opening" / "case" / "future".
    Beberapa modul (depth, depth_b, ...) digabung agar pendalaman dapat
    ditambahkan bertahap tanpa menyunting berkas besar.
    """
    pkg = "content_id" if lang == "id" else "content"
    import pkgutil
    base = __import__(pkg, fromlist=["__path__"])
    names = sorted(m.name for m in pkgutil.iter_modules(base.__path__)
                   if m.name.startswith("depth"))
    merged = {}
    for name in names:
        try:
            mod = __import__(pkg + "." + name, fromlist=["EXTRA"])
        except ImportError:
            continue
        chunk = getattr(mod, "EXTRA", {}).get(n, {})
        for key, paras in chunk.items():
            merged.setdefault(key, []).extend(paras)
    return merged


def render_chapter(ch, chapter_label="Chapter", lang="en"):
    n = ch["num"]
    nsec = ch.get("nsec", len(ch["sections"]))
    theme_label = "Tema" if lang == "id" else "Theme"
    out = [f"# {chapter_label} {n}: {ch['title']}", "",
           f"*{theme_label}: {ch['theme']}*", ""]

    extra = _load_extra(lang, n)

    for p in ch["opening"]:
        out += [p, ""]
    for p in extra.get("opening", []):
        out += [p, ""]

    for s in ch["sections"]:
        out += [f"## {s['num']} {s['title']}", ""]
        for p in s["paras"]:
            out += [p, ""]
        for p in extra.get(s["num"], []):
            out += [p, ""]

    case = ch["case"]
    out += [f"## {n}.{nsec + 1} {case['title']}", ""]
    for p in case["paras"]:
        out += [p, ""]
    for p in extra.get("case", []):
        out += [p, ""]

    fut = ch["future"]
    out += [f"## {n}.{nsec + 2} {fut['title']}", ""]
    for p in fut["paras"]:
        out += [p, ""]
    for p in extra.get("future", []):
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
