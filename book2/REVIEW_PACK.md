# Reviewer invitation package / Paket undangan penelaah

This folder contains what an external reviewer needs in order to give a
substantive opinion on the book, and what the author needs in order to record
that opinion afterwards. Nothing here is a substitute for peer review; it is
the apparatus that makes an external read auditable.

## What to send

| Item | Path | Why |
|---|---|---|
| Full PDF (EN) | `publish/en.pdf` | the object under review |
| Full PDF (ID) | `publish/id.pdf` | the translation, checked against the same claims |
| Evidence ledger | `reference/klaim.csv` | 145 claims, each with a source key, a confidence grade, and a verification note |
| Bibliography | `reference/bibliografi.csv` | every citation, with DOI/ISBN where one exists |
| Audit report | `reference/laporan_audit_en.md`, `laporan_audit_id.md` | density, orphans, unsourced numerals, claim coverage |
| This file | `REVIEW_PACK.md` | the questions the reviewer is asked to answer |

## The three questions

A reviewer is not asked to endorse the argument. A reviewer is asked to answer
three questions, in writing, with page references.

1. **Is any factual claim wrong, or attributed to a source that does not say
   it?** Quote the sentence, give the page, and name the source that contradicts
   it. This is the highest-value finding and the only one that blocks
   publication.
2. **Is any chapter's falsification section decorative?** That is: does the
   chapter state an observation that *could* occur and that the chapter would
   not survive? Name the chapter and say what the falsifier should have been.
3. **Is the evidence base skewed in a way the text does not admit?** The book
   states its skew toward Europe and North America in the note on sources. If a
   further skew is visible — by discipline, by method, by publisher — name it.

## What the reviewer is not asked to do

- Not to agree with the argument.
- Not to rewrite prose.
- Not to check every one of the 145 claims. A sample of twenty, chosen by the
  reviewer, is more useful than a promise to check all of them.

## Recording the outcome

Reviews are recorded in `reference/reviewer.csv`, one row per reviewer:

```
nama,afiliasi,bidang,tanggal,peran,hasil,catatan
```

- `peran`: `reviewer` (read the whole book) or `reader` (read one part).
- `hasil`: `tanpa-temuan` / `temuan-minor` / `temuan-mayor` / `menolak`.
- `catatan`: one line; the detail goes in `reference/reviewer/<nama>.md`.

Two readers who are not reviewers do not make a peer review. The point of the
file is that the claim "reviewed by X" can be checked, not that the number of
names is impressive.

## Affiliation, stated honestly

The author has no institutional affiliation. This is recorded on the copyright
page and in `CITATION.cff` rather than hidden, because a reference work's
authority rests on its sources and its falsifiers, not on a letterhead. A
reviewer who wants to know who wrote this, and on what basis, should be told:
one author, no institution, sources cited so they can be checked.
