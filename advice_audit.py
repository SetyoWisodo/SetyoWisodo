# -*- coding: utf-8 -*-
"""Periksa anjuran pelaksanaan di akhir tiap subbab Future Scenarios.

Prediksi menjawab "apakah ramalan ini benar". Anjuran menjawab "kalau tandanya
muncul, apa yang dikerjakan, oleh siapa, dalam urutan apa". Skrip ini memastikan
setiap bab benar-benar punya bagian itu, dengan lima syarat:

  1. pemicu     -- kalimat pembuka menyebut peristiwa/angka yang memulai,
  2. urutan     -- ada kata urutan ("the sequence", "the order", "urutannya"),
  3. langkah    -- sedikitnya lima kata kerja tindakan yang berbeda,
  4. pelaku     -- disebut siapa yang mengerjakan,
  5. larangan   -- ada satu hal yang justru tidak boleh dilakukan.

Menulis ADVICE_PER_BAB.md; keluar dengan kode 1 bila ada bab yang belum lulus.

Jalankan: python advice_audit.py [--write]
"""
import re
import sys

from prediction_audit import section

CH = ["book.md", "book_id.md"]
# pemicu: peristiwa/angka yang memulai tindakan, disebut pada dua kalimat pertama
TRIGGER = re.compile(r"\b(?:when|once|the day|during|after a disaster|"
                     r"on a coast|a threshold|an outbreak|an event|a forecast|"
                     r"ketika|begitu|pada hari|saat|di pesisir|"
                     r"setelah bencana|ambang|wabah|prakiraan)\b", re.I)
SEQ = re.compile(r"\b(the sequence|the order|falls? into an order|urutannya|urutan|"
                 r"urutan kerjanya)\b", re.I)
# kata kerja tindakan: dicocokkan pada batang katanya, karena bahasa Inggris
# memakai bentuk -s/-ed/-ing dan bahasa Indonesia memakai awalan me-/ber-.
# kata kerja tindakan. Inggris dicocokkan pada batang kata; Indonesia dinormalkan
# lebih dulu dengan `id_stem` karena bahasa ini memakai awalan me-/ber-/di-.
ACT_EN = re.compile(
    r"\b(?:stor\w*|check\w*|call\w*|mov\w*|open\w*|clos\w*|repair\w*|releas\w*|"
    r"publish\w*|train\w*|secur\w*|protect\w*|keep\w*|pay\w*|send\w*|cut\w*|"
    r"plant\w*|vaccinat\w*|screen\w*|map\w*|agree\w*|practi\w*|test\w*|hold\w*|"
    r"sign\w*|writ\w*|put\w*|buy\w*|add\w*|treat\w*|channel\w*|negotiat\w*|"
    r"invest\w*|restor\w*|clear\w*|shift\w*|giv\w*|record\w*|list\w*|rebuild\w*|"
    r"revis\w*|warn\w*|fund\w*|financ\w*|harden\w*|staff\w*|run\w*|extend\w*|"
    r"restrict\w*|allocat\w*|disburs\w*|assess\w*|install\w*|name\w*|"
    r"spend\w*|carry\w*|leave\w*|arrive\w*|remain\w*)\b", re.I)
STEM_ID = {
    "siap", "simpan", "periksa", "hubung", "pindah", "buka", "tutup", "perbaiki",
    "cair", "terbit", "latih", "aman", "lindung", "jaga", "bayar", "kirim",
    "potong", "tanam", "vaksin", "petak", "sepak", "praktik", "uji", "tanda",
    "tulis", "letak", "beli", "tambah", "tangan", "salur", "unding", "investasi",
    "pulih", "bersih", "geser", "pakai", "beri", "catat", "daftar", "susun",
    "revisi", "bangun", "bentang", "kelola", "jalankan", "tetap", "alokasi",
    "mulai", "utamakan", "pelihara", "gaji", "lepas", "isi", "hitung", "ukur",
    "bagi", "pilih", "pasang", "hentikan", "kurangi", "tambah",
}
PRE_ID = ("meny", "meng", "mem", "men", "me", "ber", "di", "ter", "per", "pe")


def id_stem(word):
    w = word.lower()
    for pre in PRE_ID:
        if w.startswith(pre) and len(w) - len(pre) >= 4:
            return w[len(pre):]
    return w


def actions(para):
    found = {m.group(0).lower() for m in ACT_EN.finditer(para)}
    found |= {id_stem(w) for w in re.findall(r"[A-Za-zÀ-ÿ]+", para)
              if id_stem(w) in STEM_ID}
    return found


# pelaku: siapa yang mengerjakan. Dicocokkan pada batang kata juga.
ACTOR = re.compile(
    r"\b(?:household\w*|cit\w*|town\w*|clinic\w*|hospital\w*|ministr\w*|"
    r"agenc\w*|utilit\w*|government\w*|communit\w*|volunteer\w*|official\w*|"
    r"school\w*|district\w*|insurer\w*|farm\w*|teacher\w*|planner\w*|"
    r"engineer\w*|utility|retailer\w*|trader\w*|union\w*|neighbour\w*|"
    r"authorit\w*|department\w*|operator\w*|manager\w*|ministry\w*|"
    r"rumah tangga|kota\w*|klinik\w*|rumah sakit|kementerian\w*|lembaga\w*|"
    r"dinas\w*|pemerintah\w*|komunitas\w*|relawan\w*|pejabat\w*|sekolah\w*|"
    r"distrik\w*|penanggung\w*|pengelola\w*|petugas\w*|guru\w*|petani\w*|"
    r"perencana\w*|pedagang\w*|warga\w*|kelompok\w*)\b", re.I)

MARK = re.compile(r"\b(what not to do|the mistake to avoid|"
                  r"yang tidak boleh dilakukan|kesalahan yang harus dihindari)\b", re.I)


def advice_para(text, n):
    body = section(text, n) if False else section(text, "book.md", n)
    if not body:
        return None
    paras = [p.strip() for p in body.split("\n\n")
             if p.strip() and set(p.strip()) != {"-"}
             and not p.strip().startswith(("##", "[[TABLE", "![", "|"))]
    for p in reversed(paras):
        if MARK.search(p):
            return re.sub(r"\s+", " ", p)
    return None


def check(para):
    sents = re.split(r"(?<=[.!?])\s+", para)
    first_two = " ".join(sents[:2])
    acts = actions(para)
    # langkah = butir yang dipisah titik koma sebelum kalimat larangan, atau
    # jumlah kata kerja tindakan yang berbeda -- mana yang lebih besar.
    cut = next((i for i, s in enumerate(sents) if MARK.search(s)), len(sents))
    clauses = " ".join(sents[:cut]).count(";") + 1
    return dict(
        trigger=bool(TRIGGER.search(first_two)),
        sequence=bool(SEQ.search(para)),
        steps=max(len(acts), clauses),
        actor=bool(ACTOR.search(para)),
        forbid=bool(MARK.search(para)),
        words=len(para.split()),
    )


def main():
    rows = []
    for path in CH:
        text = open(path, encoding="utf-8").read()
        for n in range(1, 25):
            body = section(text, path, n)
            paras = [re.sub(r"\s+", " ", p.strip()) for p in (body or "").split("\n\n")
                     if p.strip() and set(p.strip()) != {"-"}
                     and not p.strip().startswith(("##", "[[TABLE", "![", "|"))]
            para = next((p for p in reversed(paras) if MARK.search(p)), None)
            rows.append((path, n, check(para) if para else None))

    bad = [r for r in rows if r[2] is None
           or not all([r[2]["trigger"], r[2]["sequence"], r[2]["steps"] >= 5,
                       r[2]["actor"], r[2]["forbid"]])]
    lines = ["# Anjuran Pelaksanaan per Bab", "",
             "Yang diperiksa: pemicu, urutan, jumlah langkah, pelaku, dan larangan.",
             "Sebuah bab lulus bila kelimanya ada dan langkahnya sedikitnya lima.", ""]
    for path, name in (("book.md", "Inggris"), ("book_id.md", "Indonesia")):
        lines += [f"## Edisi {name}", "",
                  "| Bab | Pemicu | Urutan | Langkah | Pelaku | Larangan | Kata |",
                  "|---|---|---|---|---|---|---|"]
        for p_, n, r in rows:
            if p_ != path or not r:
                continue
            lines.append(f"| {n} | {'ya' if r['trigger'] else '—'} | "
                         f"{'ya' if r['sequence'] else '—'} | {r['steps']} | "
                         f"{'ya' if r['actor'] else '—'} | "
                         f"{'ya' if r['forbid'] else '—'} | {r['words']} |")
        lines.append("")
    if bad:
        lines += ["## Belum lulus", ""]
        for p_, n, r in bad:
            lines.append(f"- {p_} bab {n}: " + ("paragraf anjuran tidak ditemukan"
                                                if r is None else "syarat belum lengkap"))
        lines.append("")
    print(f"bab diperiksa: {len(rows)} | belum lulus: {len(bad)}")
    for p_, n, r in bad:
        print(f"  {p_} bab {n}: {r}")
    if "--write" in sys.argv:
        open("ADVICE_PER_BAB.md", "w", encoding="utf-8").write("\n".join(lines) + "\n")
        print("ADVICE_PER_BAB.md ditulis")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
