// =====================================================================
//  Book template — "Surviving the Future" / "Bertahan Hidup di Masa Depan"
//  A4 (210 x 297 mm), margins top 30mm bottom 40mm left 30mm right 30mm
//  line spacing 1.25 within para, 1.5 between para, headings 1.5
// =====================================================================

#let serif = ("Source Serif 4", "DejaVu Serif", "Serif")
#let sans = ("Source Sans 3", "DejaVu Sans", "Sans Serif")
#let accent = rgb("#1f5f8b")
#let warm = rgb("#c26a1b")
#let ink = rgb("#1b1b1b")
#let muted = rgb("#5b6470")

// ---------- labels / strings per language ----------
#let L = (
  en: (chapter: "Chapter", part: "Part", contents: "Contents", index: "Index",
       blank: ""),
  id: (chapter: "Bab", part: "Bagian", contents: "Daftar Isi", index: "Indeks",
       blank: ""),
)

// ---------- helpers used by generated content ----------
#let callout(title: none, kind: "note", body) = {
  let col = if kind == "action" { warm } else if kind == "local" { rgb("#2e7d4f") } else { accent }
  block(
    width: 100%, breakable: true, inset: (x: 11pt, y: 9pt), radius: 2pt,
    fill: col.lighten(92%), stroke: (left: 2.4pt + col),
    above: 1.1em, below: 1.1em,
  )[
    #if title != none {
      block(below: 0.6em, text(font: sans, weight: "semibold", size: 12pt, fill: col.darken(15%), upper(title)))
    }
    #set text(size: 12pt)
    #set par(first-line-indent: 0pt, spacing: 0.75em)
    #body
  ]
}

// ---------- sitasi ----------
#let cite-group(keys) = {
  context {
    let marks = query(<citekey>)
    let nums = ()
    for k in keys {
      let pos = marks.position(m => m.value == k)
      if pos != none { nums.push(pos + 1) }
    }
    if nums.len() > 0 {
      text(size: 7pt, baseline: 0.34em, fill: accent, nums.map(str).join(","))
    } else {
      text(size: 7pt, baseline: 0.34em, fill: warm, "?")
    }
  }
  for k in keys { [#metadata(k) <citekey>] }
}

#let bibentry(n: 0, body) = block(breakable: true, below: 0.42em, [
  #grid(columns: (2.2em, 1fr), column-gutter: 2pt,
    text(size: 9pt, fill: muted, [#n]),
    text(size: 9pt, body))
])

#let lead(body) = block(above: 0.2em, below: 1.4em)[
  #set par(first-line-indent: 0pt)
  #text(size: 12pt, style: "italic", fill: muted, body)
]

#let part-page(number: "", title: "", blurb: "", lang: "en") = {
  [#metadata("part-pad") <chend>]
  pagebreak(to: "odd", weak: true)
  [#metadata(L.at(lang).part + " " + number) <partpage>]
  v(34%)
  align(center)[
    #text(font: sans, size: 11pt, weight: "bold", tracking: 3pt, fill: accent, upper(L.at(lang).part + " " + number))
    #v(10pt)
    #line(length: 22%, stroke: 0.7pt + accent)
    #v(16pt)
    #heading(level: 1, numbering: none, supplement: [Part], outlined: true, bookmarked: true)[#title]
    #if blurb != "" [
      #v(18pt)
      #block(width: 76%, align(center, text(font: serif, size: 11pt, style: "italic", fill: muted, blurb)))
    ]
    #v(16pt)
  ]
  [#metadata("part-end") <partend>]
}

#let idx-marks(terms, body) = {
  // terms: array of (key, regex)
  let out = body
  for t in terms {
    out = {
      show regex(t.at(1)): it => [#metadata(t.at(0))<idx>#it]
      out
    }
  }
  out
}

#let compress-pages(nums) = {
  let s = nums.dedup().sorted()
  let parts = ()
  let i = 0
  while i < s.len() {
    let a = s.at(i)
    let j = i
    while j + 1 < s.len() and s.at(j + 1) == s.at(j) + 1 { j += 1 }
    if j > i { parts.push(str(a) + "–" + str(s.at(j))) } else { parts.push(str(a)) }
    i = j + 1
  }
  parts.join(", ")
}

#let make-index(lang: "en", max-pages: 14) = context {
  let marks = query(<idx>)
  let d = (:)
  for m in marks {
    let k = m.value
    let pg = counter(page).at(m.location()).first()
    if k in d { d.at(k).push(pg) } else { d.insert(k, (pg,)) }
  }
  let keys = d.keys().sorted(key: k => lower(k))
  set par(first-line-indent: 0pt, justify: false, spacing: 0.32em, hanging-indent: 1em)
  set text(size: 12pt)
  columns(2, gutter: 14pt)[
    #let last = ""
    #for k in keys {
      let first = upper(k.first())
      if first != last {
        v(0.5em)
        text(font: sans, weight: "bold", fill: accent, first)
        parbreak()
        last = first
      }
      let pages = d.at(k).dedup().sorted()
      if pages.len() > max-pages { pages = pages.slice(0, max-pages) }
      [#k, #compress-pages(pages)]
      parbreak()
    }
  ]
}

// =====================================================================
//  Main setup
// =====================================================================
#let book(
  lang: "en", title: "", subtitle: "", author: "", year: "",
  keywords: (), contents-label: "Contents", index-label: "Index",
  publisher: "", dedication: none,
  chapter-short: ("1": "",),
  copyright-lines: (), cite-label: "How to cite this book",
  how-to-cite: none, isbn: "", doi: "", review-status: none,
  page-w: 6in, page-h: 9in,
  font: serif,
  margin: (top: 22mm, bottom: 24mm, left: 20mm, right: 20mm),
  body,
) = {
  set document(title: title + ": " + subtitle, author: author, keywords: keywords)
  set text(font: font, size: 11pt, lang: lang, fill: ink, hyphenate: true,
           number-type: "lining", costs: (hyphenation: 60%, runt: 120%, widow: 200%, orphan: 200%))
  // Format: Times New Roman 12, A4, justify, first line indent 12.7mm, line spacing 1.25, antar paragraf 1.5
  set par(justify: true, leading: 0.32em, first-line-indent: (amount: 1.1em, all: false), spacing: 0.85em)
  set page(
    width: page-w, height: page-h,
    margin: margin,
    header-ascent: margin.top - 9mm, footer-descent: 11mm,
  )
  set list(indent: 0.6em, body-indent: 0.5em, spacing: 0.55em, marker: ([•], [–]))
  set enum(indent: 0.6em, body-indent: 0.5em, spacing: 0.55em)
  set footnote.entry(separator: line(length: 25%, stroke: 0.4pt + muted), indent: 0pt, gap: 0.45em)
  show footnote.entry: set text(size: 12pt)
  show quote.where(block: true): it => block(inset: (left: 1.4em, right: 1.0em), above: 1em, below: 1em)[
    #set text(size: 12pt, style: "italic")
    #set par(first-line-indent: 0pt)
    #it.body
    #if it.attribution != none { align(right, text(style: "normal", size: 12pt, [— ] + it.attribution)) }
  ]

  // ---- tables ----
  set table(stroke: none, inset: (x: 5pt, y: 4pt), fill: (x, y) => if y == 0 { accent.lighten(85%) } else if calc.odd(y) { luma(247) })
  show table: set text(size: 12pt, number-type: "lining")
  show table: set par(justify: false, first-line-indent: 0pt)
  show table.cell.where(y: 0): set text(font: sans, weight: "semibold")
  show figure.where(kind: table): set block(breakable: true)
  show figure: set block(above: 1.1em, below: 1.1em)
  // Gambar: caption tanpa nomor, lebih kecil, rapat dengan gambarnya, karena
  // kredit sumber sudah tercetak di dalam gambar itu sendiri.
  set figure(numbering: none)
  show figure.where(kind: image): set text(size: 9.5pt, fill: ink.lighten(20%))
  show figure.where(kind: image): set par(justify: false, leading: 0.58em)
  show figure.caption: set par(first-line-indent: 0pt)

  // ---- headings ----
  set heading(numbering: (..nums) => if nums.pos().len() == 1 { numbering("1", ..nums) } else { none })
  show heading: set text(font: sans, fill: ink, hyphenate: false)
  show heading: set par(justify: false)

  show heading.where(level: 1): it => {
    if it.supplement == [Part] {
      // part title (placed inside part-page)
      text(font: sans, size: 26pt, weight: "bold", fill: ink, it.body)
    } else {
      [#metadata("chapter-end") <chend>]
      pagebreak(to: "odd", weak: true)
      v(0.9in)
      if it.numbering != none {
        block(below: 8pt, text(font: sans, size: 10pt, weight: "bold", tracking: 2.2pt, fill: accent,
          upper(L.at(lang).chapter + " " + counter(heading).display("1"))))
      }
      block(below: 10pt, text(font: sans, size: 20pt, weight: "bold", it.body))
      block(below: 1.6em, line(length: 18%, stroke: 1.2pt + warm))
    }
  }
  show heading.where(level: 2): it => block(above: 1.6em, below: 0.75em, sticky: true,
    text(size: 12pt, weight: "bold", fill: accent.darken(10%), it.body))
  show heading.where(level: 3): it => block(above: 1.35em, below: 0.5em, sticky: true,
    text(size: 11pt, weight: "bold", fill: ink.lighten(8%), it.body))
  show heading.where(level: 4): it => block(above: 1em, below: 0.5em, sticky: true,
    text(size: 12pt, weight: "bold", style: "italic", it.body))

  // ---- running heads ----
  // Judul bab yang panjang dipotong pada pisahan "—" supaya kepala halaman
  // tidak membungkus menjadi dua baris.
  let short-title(h) = {
    // Judul tanpa nomor (pengantar, daftar pustaka, catatan sumber) tidak
    // menaikkan counter heading; pakai judulnya sendiri, bukan judul bab terakhir.
    if h.numbering == none { return h.body }
    let n = str(counter(heading).at(h.location()).first())
    let cand = chapter-short.at(n, default: "")
    if cand != "" { cand } else { h.body }
  }
  let is-blank(p) = {
    let ends = query(<chend>).map(m => m.location().page()) + query(<partend>).map(m => m.location().page())
    let starts = query(heading.where(level: 1)).map(h => h.location().page())
    let blank = false
    for e in ends {
      let nxt = starts.filter(s => s > e)
      if nxt.len() > 0 and e < p and p < nxt.first() { blank = true }
    }
    // halaman sebelum halaman pembuka (daftar isi, pembuka bagian) juga kosong
    let e = ends.filter(e => e < p)
    if e.len() > 0 {
      let nxt = starts.filter(s => s > e.last() and s >= p)
      if nxt.len() > 0 and nxt.first() == p { blank = true }
    }
    blank
  }
  set page(
    header: context {
      let p = here().page()
      let on-opener = query(heading.where(level: 1)).any(h => h.location().page() == p)
      let on-part = query(<partpage>).any(h => h.location().page() == p)
      if is-blank(p) or state("hdr", false).get() == false or on-part { return }
      if on-opener { return }
      let num = counter(page).display()
      let prev = query(heading.where(level: 1).before(here())).filter(h => h.supplement != [Part])
      let chap = if prev.len() > 0 { short-title(prev.last()) } else { none }
      set text(font: sans, size: 10pt, fill: muted, tracking: 0.8pt, number-type: "lining")
      if calc.even(p) {
        grid(columns: (auto, 1fr), column-gutter: 12pt, text(weight: "semibold", fill: ink, num), text(size: 9pt, upper(title)))
      } else {
        grid(columns: (1fr, auto), column-gutter: 12pt, align(right, text(size: 9pt, upper(if chap == none { "" } else { chap }))), text(weight: "semibold", fill: ink, num))
      }
      v(-4pt)
      line(length: 100%, stroke: 0.35pt + muted.lighten(40%))
    },
    footer: context {
      let p = here().page()
      if state("hdr", false).get() and not is-blank(p) {
        align(center, text(font: sans, size: 12pt, fill: muted, number-type: "lining", counter(page).display()))
      }
    },
  )

  // ---- front matter ----
  counter(page).update(0)
  set page(numbering: "i")
  state("hdr", false).update(false)
  page(header: none, numbering: none)[
    #v(36%)
    #align(center)[
      #text(font: sans, size: 10pt, tracking: 3pt, fill: accent, upper(publisher))
      #v(18pt)
      #text(font: sans, size: 22pt, weight: "bold", title)
      #v(9pt)
      #line(length: 24%, stroke: 1pt + warm)
      #v(9pt)
      #text(size: 12pt, style: "italic", fill: muted, subtitle)
      #v(28pt)
      #text(font: sans, size: 11pt, tracking: 1.5pt, author)
      #v(5pt)
      #text(font: sans, size: 10pt, fill: muted, year)
    ]
  ]
  page(header: none, footer: none)[
    #v(18%)
    #set par(first-line-indent: 0pt, justify: false)
    #text(size: 11pt, style: "italic", fill: muted, dedication)
  ]
  page(header: none, footer: none)[
    #v(0.5in)
    #set par(first-line-indent: 0pt, justify: false)
    #set text(size: 9.5pt)
    #for ln in copyright-lines [
      #if ln == "" { parbreak() } else { eval(ln, mode: "markup")
        parbreak() }
    ]
    #v(1.2em)
    #if isbn != "" [
      #text(font: sans, size: 9pt, weight: "semibold", [ISBN #isbn])
      #parbreak()
    ]
    #if doi != "" [
      #text(font: sans, size: 9pt, weight: "semibold", [DOI #doi])
      #parbreak()
    ]
    #if how-to-cite != none [
      #v(1.4em)
      #block(below: 6pt, text(font: sans, size: 9pt, weight: "bold", tracking: 1.2pt, fill: accent, upper(cite-label)))
      #text(size: 9.5pt, eval(how-to-cite, mode: "markup"))
      #parbreak()
    ]
    #if review-status != none [
      #v(1.0em)
      #text(size: 8.5pt, style: "italic", fill: muted, review-status)
    ]
  ]
  page(header: none, footer: none)[
    #v(0.35in)
    #block(below: 10pt, text(font: sans, size: 12pt, weight: "bold", fill: ink, contents-label))
    #block(below: 1.6em, line(length: 18%, stroke: 1.2pt + warm))
    #show outline.entry.where(level: 1): it => {
      let el = it.element
      if el.supplement == [Part] {
        v(0.75em)
        block(above: 0.4em, below: 0.35em,
          text(font: sans, size: 9.5pt, weight: "bold", tracking: 1.6pt, fill: accent,
            upper(L.at(lang).part) + " " + upper(el.body)))
      } else {
        block(above: 0.3em,
          link(el.location(), grid(columns: (2.5em, 1fr, auto), column-gutter: 6pt,
            text(size: 9.2pt, fill: muted, if el.numbering != none { numbering("1", ..counter(heading).at(el.location())) } else { "" }),
            text(size: 9.2pt, hyphenate: false)[#el.body #box(width: 1fr, repeat[.])],
            text(size: 9.2pt, fill: muted, it.page()))))
      }
    }
    #outline(depth: 1, indent: auto, title: none)
  ]
  // ---- main matter ----
  [#metadata("front-end") <chend>]
  pagebreak(to: "odd", weak: true)
  set page(numbering: "1")
  counter(page).update(1)
  state("hdr", true).update(true)
  body
  // ---- indeks subjek (opsional; tidak dicetak bila tidak ada istilah) ----
  context {
    let n = query(<idx>).len()
    if n > 0 {
      heading(level: 1, numbering: none, outlined: true, bookmarked: true, index-label)
      v(6pt)
      make-index(lang: lang)
    }
  }
}

// ---------- matter switches ----------
#let frontmatter(body) = {
  set page(numbering: "i")
  counter(page).update(1)
  state("hdr", false).update(false)
  body
}
#let mainmatter(body) = {
  [#metadata("front-end") <chend>]
  pagebreak(to: "odd", weak: true)
  set page(numbering: "1")
  counter(page).update(1)
  state("hdr", true).update(true)
  body
}
#let backmatter(body) = {
  set heading(numbering: none)
  body
}
