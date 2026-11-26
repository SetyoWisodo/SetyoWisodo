# Understanding Crisis — Blueprint

**Reference work on climate, vulnerability, and social capacity**
Target: ~75,000 words · 19 chapters · 5 parts · English first edition
Status: blueprint (agreed 2026-11-26)

---

## Why this book exists

Publishers produce two kinds of climate books: the physical-science survey (what the atmosphere
is doing) and the policy polemic (what governments should do). Both skip the middle layer — the
social machinery that converts a hazard into a death toll. This book occupies that layer and
stays there.

Its claim, stated once: **hazard is physics, exposure is history, vulnerability is social
structure — and in any window short enough to matter to a household, vulnerability is where the
work is.**

## What makes it a reference work rather than a trade book

| Requirement | Implementation |
|---|---|
| Traceable claims | Numbered in-text citations → auto-generated reference list |
| No unsourced numbers | Every figure carried in `reference/klaim.csv` with source + confidence |
| Explicit uncertainty | Three claim classes (observation / estimate / framework), stated per chapter |
| Reproducible audit | `tools/audit_rujukan.py` measures citation density, orphans, unsourced figures |
| Falsifiability | Every chapter closes with "What would prove this chapter wrong" |
| Method transparency | Every chapter has a *How the numbers are made* box |
| Guided next steps | Every chapter has an annotated *Further reading* list |

## Structure

### Part I — Diagnosis (ch 1–3)
Establishes the vocabulary and the failure mode.

1. **Hazard, Exposure, Vulnerability** — the three-term framework; why "natural disaster" is a category error; the arithmetic of risk.
2. **Crisis Does Not Arrive as a Single Blow** — disaster as a chain; four link types; non-linearity; slow-onset disasters; uncounted losses.
3. **Indonesia as Reader, Not Example** — the case that stresses the framework: subsidence as manufactured hazard, three-way flooding, peat fire, reef as infrastructure, 500+ local governments.

### Part II — Vulnerability (ch 4–7)
Who dies, and why the distribution is not random.

4. **Heat, the Invisible Killer** — excess mortality methods; wet-bulb physiology; the BC and Europe evidence; why heat plans work; adaptation that follows inequality.
5. **Water: Too Much, Too Little, and Sinking Ground** — three flood sources; why levees alone fail; drought as slow disaster; subsidence; store-don't-drain.
6. **Food: When One Harvest Becomes a Price Somewhere Else** — thin markets; the 2023 rice episode; why smallholders absorb the loss; post-harvest losses; anticipatory cash.
7. **Disease That Moves Because the Climate Moves** — vector range shifts; dengue's 30-fold rise; the infrastructure behind "climate disease"; mental health; health systems as the weakest link.

### Part III — Capacity (ch 8–11)
What makes a place able to absorb a shock.

8. **Money: Insurance, Aid, and Who Counts as Worth Saving** — rising losses with falling deaths; insurance retreat; who has no cover; anticipatory vs post-hoc aid; loss and damage.
9. **Infrastructure as a Chain of Dependencies** — Texas 2021 as the canonical case; sectoral planning vs systems planning; isolation and redundancy; building codes; community-scale infrastructure.
10. **Social Capital: The Thing That Cannot Be Bought** — Puerto Rico's 64 vs 4,645; bonding/bridging/linking; *gotong royong* and *smong*; what policy strengthens or destroys it; the limits.
11. **Knowledge: Forecasts That Do Not Arrive** — the Ahr valley failure; the four links of warning; message design; trust; local knowledge; climate literacy as a skill.

### Part IV — Decisions (ch 12–14)
The choices that cannot be avoided.

12. **Displacement: The Choice That Always Arrives Late** — Falepili Union; staged migration; why planned relocation fails; staying as a legitimate choice; new vulnerability after moving.
13. **Justice: Who Emits, Who Absorbs** — two distinct inequalities; attribution of responsibility; loss and damage as a test; justice inside countries; why unjust policy fails politically.
14. **Uncertainty: Waiting for Certainty Is Also a Decision** — three kinds of uncertainty; robust decision-making; option-preserving adaptation; the cost of delay.

### Part V — Action (ch 15–17)
What can be done, by whom, at what scale.

15. **Households: What Can Be Done This Week** — the checklist, with reasons; what not to buy; the loneliness problem in heat and flood.
16. **Communities and Cities: Capacity Built Before the Rain** — what adaptive capacity actually is; shelters that get used; land use as the real climate decision; open space as infrastructure; the budget test.
17. **Reading the Claims: How to Judge a Climate Promise** — three claim types; how to read a number; how to read a forecast range; how to audit a policy promise.

### Apparatus

Per the agreed scope, this edition carries **no glossary, no discussion questions, and no research
exercises**. Method notes live inside each chapter as boxes rather than in an appendix, so that the
method sits next to the number it qualifies.

- **Reference list** — auto-generated, numbered by first appearance, built from `bibliografi.csv`.
- **Chapter apparatus** — opening case, mechanism, evidence, method box, counter-case, falsification test, further reading.

## Chapter template (every chapter)

1. **Opening case** (400–600 w) — one concrete event, sourced.
2. **The mechanism** (900–1,200 w) — why the case generalises; the causal chain.
3. **The evidence** (900–1,200 w) — what studies show; where they disagree; what they cannot show.
4. **Box: How the numbers are made** (200–300 w) — method, denominator, known biases.
6. **The counter-case** (300–500 w) — a place or period where the pattern did *not* hold, and what that costs the argument.
7. **What would prove this chapter wrong** (150–250 w).
8. **Further reading** (5–8 annotated items).

Target: 3,500–4,000 words per chapter.

## House style

- **Numbers**: spell out under ten; numerals above. Always give the unit and the year.
- **Ranges**: never collapse a range to a point estimate. Write "1–15 cm/yr, up to 28 cm/yr in places."
- **Attribution**: "the study found" not "scientists say." Name the method when it matters.
- **Uncertainty**: use "estimate", "projection", "observation" precisely. Never "proven."
- **Currency**: give USD with the year of the exchange rate.
- **People**: full name on first mention, surname after. No honorifics.
- **Translation**: Indonesian terms italicised on first use, glossed in parentheses.

## Sourcing rules

1. Peer-reviewed article > institutional report > dataset > investigative journalism > news.
2. No claim enters the text unless it has a row in `klaim.csv`.
3. A claim marked `perlu-cek` may appear only with an explicit in-text hedge ("estimates vary"; "the figure is contested").
4. Government figures are attributed to the government, not presented as neutral measurement.
5. Advocacy-group figures (WWA, IFRC, etc.) are attributed as such, even when their method is sound.
6. Anything I cannot source does not go in the book — even if it is true.

## Verification ledger

`reference/klaim.csv` — 45 claims registered, 40 verified to primary source, 5 flagged.
Corrections already forced by verification:

| Claim | Was | Is |
|---|---|---|
| Indonesia coastline | 54,000 km | **99,093 km** (BIG 2013) |
| Rice price after India ban | +30% | **+10%** in a month, 15-yr high (FAO) |
| Jakarta subsidence | ">1 m in decades" | **1–15 cm/yr, up to 28 cm/yr, >3 m cumulative** |
| Texas water | "14 million lost supply" | **14.4 m under boil-water; 4.4 m peak outage** |
| Bangladesh Bhola | 300,000 | **300,000–500,000** |
| Simeulue | "far fewer deaths" | **7 deaths out of 78,128** |

## Open decisions

- Publisher/imprint line for the reference edition.
- Whether to include the Bahasa Indonesia edition as a parallel volume or a translation.
- Whether the methods appendix becomes a separate open-access PDF.
