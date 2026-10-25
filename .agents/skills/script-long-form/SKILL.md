---
name: script-long-form
description: Use when the user wants a long-form narration or documentary-style video script (roughly 20 to 60 minutes) on a history, economy, geopolitics, or explainer topic. Produces a beat outline, a timed script, and a claim register that feeds fact-check-sources before anything is published.
allowed-tools: Read, Write
version: 1.0.0
author: Setyo Wisodo (SetyoWisodo/SetyoWisodo)
license: MIT
inspiration: danjdewhurst/story-skills (MIT) — structure ideas only, no text copied
metadata:
  tags:
    - script
    - long-form
    - narration
    - documentary
---

# Script Long-Form

Turn a topic into a publishable long-form script in four stages. Do not skip stage 3: a script without a claim register is not ready to publish.

## Inputs to confirm first

1. Topic and the single question the video answers (for example: "why did this country's currency collapse in 1998?").
2. Target runtime in minutes and the audience (general Indonesian viewers, or English global viewers).
3. Tone: explainer (analytic, visuals-led) or narrative (story-led, character-led). Ask if unclear.
4. Source list the user already trusts. If none, mark every factual claim as `unverified` until checked.

## Stage 1 — Beat outline

Write 6 to 10 beats. Each beat has:
- `purpose`: one sentence (hook, context, mechanism, evidence, counter-argument, implication, close).
- `minutes`: target length. Sum must match the runtime within 10%.
- `visual`: what the viewer sees (diagram, map, archive still, animation, talking head).

Rule: the first 30 seconds must state the question and one surprising fact. Put the answer at the end of the first act, not at the end of the video.

## Stage 2 — Timed script

Write narration per beat, in the target language. Keep sentences short enough to read aloud in one breath. Mark each factual sentence with `[C1]`, `[C2]` and so on, matching the claim register.

Do not invent quotes, statistics, dates, or names. If a fact is needed but not known, write `[NEEDS SOURCE: ...]` and leave it there.

## Stage 3 — Claim register (required)

Table with columns: `id`, `claim (one sentence)`, `beat`, `type` (date, number, name, causal, quote, opinion), `status` (`unverified` by default), `source` (empty until checked).

Causal claims ("X caused Y") need two independent sources or must be phrased as one interpretation among several.

Opinions are labelled as opinion in the script, for example "menurut analisis ini".

Hand the register to `fact-check-sources` before the script is marked ready.

## Stage 4 — Readiness check

Output a short checklist:
- every `[C#]` has a status other than `unverified`, or is removed or rephrased as opinion;
- no `[NEEDS SOURCE]` markers remain;
- runtime estimate is within 10% of the target;
- visuals exist for every beat;
- sensitive topics (politics, religion, ethnicity, living persons, conspiracy theories) have a balance note.

Report the status as `READY`, `NOT READY`, or `READY WITH CAVEATS`, and list what is missing.

## Output files

- `scripts/<slug>/outline.md`
- `scripts/<slug>/script.md`
- `scripts/<slug>/claims.csv`
- `scripts/<slug>/readiness.md`

## Limits

This skill writes text and structure. It does not record narration, edit video, or choose footage. Footage and archive images need their own licence check before use.
