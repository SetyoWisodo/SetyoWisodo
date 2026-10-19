// =====================================================================
//  Book template — "Surviving the Future" / "Bertahan Hidup di Masa Depan"
//  Trim 6 x 9 in (152.4 x 228.6 mm), print-ready interior for POD/offset.
// =====================================================================

#let serif = ("Times New Roman", "DejaVu Serif", "Times", "Serif")
#let sans = ("Times New Roman", "DejaVu Serif", "Times", "Serif")
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

#let lead(body) = block(above: 0.2em, below: 1.4em)[
  #set par(first-line-indent: 0pt)
  #text(size: 12pt, style: "italic", fill: muted, body)
]

#let part-page(number: "", title: "", lang: "en") = {
  [#metadata("part-pad") <chend>]
  pagebreak(to: "odd", weak: true)
  [#metadata(L.at(lang).part + " " + number) <partpage>]
  v(30%)
  align(center)[
    #text(font: sans, size: 12pt, weight: "bold", tracking: 3pt, fill: accent, upper(L.at(lang).part + " " + number))
    #v(10pt)
    #line(length: 22%, stroke: 0.7pt + accent)
    #v(12pt)
    #heading(level: 1, numbering: none, supplement: [Part], outlined: true, bookmarked: true)[#title]
  ]
  [#metadata("part-end") <partend>]
  pagebreak(to: "odd")
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
  keywords: (), body,
) = {
  set document(title: title + ": " + subtitle, author: author, keywords: keywords)
  set text(font: serif, size: 12pt, lang: lang, fill: ink, hyphenate: true,
           number-type: "lining", costs: (hyphenation: 60%, runt: 120%, widow: 200%, orphan: 200%))
  set par(justify: true, leading: 0.68em, first-line-indent: 1.2em, spacing: 0.68em)
  set page(
    width: 6in, height: 9in,
    margin: (inside: 0.85in, outside: 0.62in, top: 0.78in, bottom: 0.82in),
    header-ascent: 38%, footer-descent: 35%,
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

  // ---- headings ----
  set heading(numbering: "1")
  show heading: set text(font: sans, fill: ink, hyphenate: false)
  show heading: set par(justify: false)

  show heading.where(level: 1): it => {
    if it.supplement == [Part] {
      // part title (placed inside part-page)
      text(font: sans, size: 12pt, weight: "bold", fill: ink, it.body)
    } else {
      [#metadata("chapter-end") <chend>]
      pagebreak(to: "odd", weak: true)
      v(0.9in)
      if it.numbering != none {
        block(below: 6pt, text(font: sans, size: 12pt, weight: "bold", tracking: 2.5pt, fill: accent,
          upper(L.at(lang).chapter + " " + counter(heading).display("1"))))
      }
      block(below: 10pt, text(font: sans, size: 12pt, weight: "bold", it.body))
      block(below: 1.6em, line(length: 18%, stroke: 1.2pt + warm))
    }
  }
  show heading.where(level: 2): it => block(above: 1.6em, below: 0.75em, sticky: true,
    text(size: 12pt, weight: "bold", fill: accent.darken(10%), it.body))
  show heading.where(level: 3): it => block(above: 1.2em, below: 0.6em, sticky: true,
    text(size: 12pt, weight: "bold", it.body))
  show heading.where(level: 4): it => block(above: 1em, below: 0.5em, sticky: true,
    text(size: 12pt, weight: "bold", style: "italic", it.body))

  // ---- running heads ----
  let is-blank(p) = {
    // a page strictly between the end of a chapter/part and the next opener is a padding page
    let ends = query(<chend>).map(m => m.location().page()) + query(<partend>).map(m => m.location().page())
    let starts = query(heading.where(level: 1)).map(h => h.location().page())
    let blank = false
    for e in ends {
      let nxt = starts.filter(s => s > e)
      if nxt.len() > 0 and e < p and p < nxt.first() { blank = true }
    }
    blank
  }
  set page(
    header: context {
      let p = here().page()
      let on-opener = query(heading.where(level: 1)).any(h => h.location().page() == p)
      let on-part = query(<partpage>).any(h => h.location().page() == p)
      if on-opener or on-part or is-blank(p) or state("hdr", false).get() == false { return }
      let num = counter(page).display()
      let prev = query(heading.where(level: 1).before(here())).filter(h => h.supplement != [Part])
      let chap = if prev.len() > 0 { prev.last().body } else { [] }
      set text(font: sans, size: 12pt, fill: muted, tracking: 0.8pt, number-type: "lining")
      if calc.even(p) {
        grid(columns: (auto, 1fr), column-gutter: 12pt, text(weight: "semibold", fill: ink, num), upper(title))
      } else {
        grid(columns: (1fr, auto), column-gutter: 12pt, align(right, upper(chap)), text(weight: "semibold", fill: ink, num))
      }
      v(-4pt)
      line(length: 100%, stroke: 0.35pt + muted.lighten(40%))
    },
    footer: context {
      let p = here().page()
      let on-opener = query(heading.where(level: 1)).any(h => h.location().page() == p and h.supplement != [Part])
      if on-opener and state("hdr", false).get() {
        align(center, text(font: sans, size: 12pt, fill: muted, number-type: "lining", counter(page).display()))
      }
    },
  )

  body
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
