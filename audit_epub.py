# -*- coding: utf-8 -*-
"""Pemeriksa struktur EPUB 3 tanpa epubcheck (tidak butuh Java).

Yang diperiksa:
  * mimetype: entri pertama, tanpa kompresi, isi tepat
  * container.xml -> rootfile ada di dalam zip
  * content.opf: dc:identifier/title/language, id unik, semua href ada,
    tepat satu item properties="nav" dan satu "cover-image"
  * spine: semua idref ada di manifest, tidak ada duplikat
  * nav.xhtml: <nav epub:type="toc">, semua tautan (berkas#anchor) resolve
  * toc.ncx: jumlah navPoint sejajar dengan daftar isi
  * setiap XHTML: well-formed, punya <title> dan atribut bahasa

Jalankan: python audit_epub.py book/publish/*.epub
Keluar dengan kode 1 bila ada masalah.
"""
import posixpath
import re
import sys
import zipfile

from lxml import etree

NS = {
    "opf": "http://www.idpf.org/2007/opf",
    "dc": "http://purl.org/dc/elements/1.1/",
    "x": "http://www.w3.org/1999/xhtml",
    "ncx": "http://www.daisy.org/z3986/2005/ncx/",
    "c": "urn:oasis:names:tc:opendocument:xmlns:container",
}
XHTML = "http://www.w3.org/1999/xhtml"


def audit(path):
    problems, notes = [], []
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        infos = z.infolist()

        # ---- mimetype ----
        if not names or names[0] != "mimetype":
            problems.append("mimetype bukan entri pertama")
        if infos and infos[0].compress_type != zipfile.ZIP_STORED:
            problems.append("mimetype terkompresi (harus STORED)")
        if b"mimetype" in z.namelist() and z.read("mimetype") != b"application/epub+zip":
            problems.append("isi mimetype salah")

        # ---- container ----
        root = etree.fromstring(z.read("META-INF/container.xml"))
        rootfile = root.find(".//c:rootfile", NS)
        if rootfile is None:
            problems.append("container.xml tanpa rootfile")
            return problems, notes
        opf_path = rootfile.get("full-path")
        if opf_path not in names:
            problems.append("rootfile %s tidak ada" % opf_path)
            return problems, notes
        base = posixpath.dirname(opf_path)

        # ---- package ----
        opf = etree.fromstring(z.read(opf_path))
        for tag in ("identifier", "title", "language"):
            if opf.find(".//dc:%s" % tag, NS) is None:
                problems.append("dc:%s tidak ada" % tag)

        manifest = {}
        for item in opf.findall(".//opf:manifest/opf:item", NS):
            iid, href = item.get("id"), item.get("href")
            if iid in manifest:
                problems.append("id manifest ganda: %s" % iid)
            if not item.get("media-type"):
                problems.append("media-type kosong: %s" % href)
            target = posixpath.normpath(posixpath.join(base, href))
            if target not in names:
                problems.append("berkas manifest hilang: %s" % href)
            manifest[iid] = (href, item.get("properties") or "", target)

        navs = [k for k, v in manifest.items() if "nav" in v[1].split()]
        covers = [k for k, v in manifest.items() if "cover-image" in v[1].split()]
        if len(navs) != 1:
            problems.append("harus tepat satu item properties='nav' (ada %d)" % len(navs))
        if len(covers) > 1:
            problems.append("lebih dari satu cover-image")

        spine_ids = [ref.get("idref") for ref in opf.findall(".//opf:spine/opf:itemref", NS)]
        if len(spine_ids) != len(set(spine_ids)):
            problems.append("itemref ganda di spine")
        for iid in spine_ids:
            if iid not in manifest:
                problems.append("idref tanpa manifest: %s" % iid)
        notes.append("spine %d dokumen" % len(spine_ids))

        # ---- dokumen xhtml ----
        ids_cache = {}
        for iid, (href, props, target) in manifest.items():
            if not target.endswith((".xhtml", ".html")):
                continue
            data = z.read(target)
            try:
                doc = etree.fromstring(data)
            except etree.XMLSyntaxError as exc:
                problems.append("%s tidak well-formed: %s" % (href, exc))
                continue
            if doc.find(".//x:title", NS) is None:
                problems.append("%s tanpa <title>" % href)
            if not (doc.get("lang") or doc.get("{http://www.w3.org/XML/1998/namespace}lang")):
                problems.append("%s tanpa atribut bahasa" % href)
            ids_cache[target] = {el.get("id") for el in doc.iter() if el.get("id")}

        # ---- tautan di nav ----
        def check_links(doc, label):
            for a in doc.iter("{%s}a" % XHTML):
                href = a.get("href") or ""
                if href.startswith(("http:", "https:", "mailto:")):
                    continue
                frag = None
                if "#" in href:
                    href, frag = href.split("#", 1)
                target = posixpath.normpath(posixpath.join(base, href)) if href else None
                if target and target not in names:
                    problems.append("%s: tautan mati %s" % (label, href))
                if target and frag and target not in ids_cache:
                    if target.endswith((".xhtml", ".html")):
                        problems.append("%s: target tidak diperiksa %s" % (label, target))
                if target and frag and target in ids_cache and frag not in ids_cache[target]:
                    problems.append("%s: anchor hilang %s#%s" % (label, href, frag))

        if navs:
            nav_target = manifest[navs[0]][2]
            nav_doc = etree.fromstring(z.read(nav_target))
            check_links(nav_doc, "nav.xhtml")
            toc_navs = [n for n in nav_doc.iter("{%s}nav" % XHTML)
                        if n.get("{http://www.idpf.org/2007/ops}type") == "toc"]
            if not toc_navs:
                problems.append("nav.xhtml tanpa <nav epub:type='toc'>")
            else:
                top = toc_navs[0].findall("x:ol/x:li", NS)
                notes.append("nav: %d entri tingkat pertama" % len(top))
                if any(n.get("{http://www.idpf.org/2007/ops}type") == "landmarks"
                       for n in nav_doc.iter("{%s}nav" % XHTML)):
                    notes.append("landmarks ada")
                else:
                    problems.append("landmarks tidak ada")

        # ---- NCX ----
        ncx_id = opf.find(".//opf:spine", NS).get("toc")
        if ncx_id and ncx_id in manifest:
            ncx = etree.fromstring(z.read(manifest[ncx_id][2]))
            top_ncx = ncx.findall(".//ncx:navMap/ncx:navPoint", NS)
            notes.append("NCX: %d navPoint teratas" % len(top_ncx))
            if navs:
                top_nav = len(top)
                if top_ncx and abs(len(top_ncx) - top_nav) > 0:
                    problems.append("NCX (%d) dan nav (%d) tidak sejajar"
                                    % (len(top_ncx), top_nav))
            for src in ncx.findall(".//ncx:content", NS):
                s = src.get("src") or ""
                f = s.split("#")[0]
                if f and posixpath.normpath(posixpath.join(base, f)) not in names:
                    problems.append("NCX: target hilang %s" % s)

        # ---- berkas tak terpakai ----
        used = {posixpath.normpath(posixpath.join(base, v[0])) for v in manifest.values()}
        used |= {opf_path, "META-INF/container.xml", "mimetype"}
        extra = [n for n in names if n not in used]
        if extra:
            notes.append("tidak dirujuk: %s" % ", ".join(extra[:5]))
    return problems, notes


def main(paths):
    bad = 0
    for path in paths:
        problems, notes = audit(path)
        print("=" * 70)
        print(path)
        for n in notes:
            print("   .", n)
        for p in problems:
            print("   !", p)
        print("   STATUS:", "bersih" if not problems else "%d masalah" % len(problems))
        bad += len(problems)
    print("=" * 70)
    print("TOTAL MASALAH:", bad)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
