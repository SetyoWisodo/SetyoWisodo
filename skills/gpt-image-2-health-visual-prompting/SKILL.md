---
name: gpt-image-2-health-visual-prompting
description: Turn an approved health-video shot into a structured, non-graphic visual prompt and asset-manifest entry. Derived operationally from awesome-gpt-image-2's prompt/style methodology; prompt-only, not a rendering engine.
status: ready-for-planning-only
upstream:
  repository: https://github.com/freestylefly/awesome-gpt-image-2
  audited_commit: d4e4ac6
  upstream_license: MIT
---

# GPT Image Style Library — Health Visual Prompting

## Purpose

Convert a **source-card-approved** health scene into a precise image-generation brief for the channel's non-graphic anatomy and evidence-literacy visuals. This skill chooses a visual structure and writes prompts; it does **not** call an image API, select a model, download a model, or create an image.

The upstream repository's own agent skill supplies a method for matching visual templates, styles, and scene tags. This project wrapper narrows that method to health education and adds evidence, provenance, and PPU controls.

## Required inputs

Do not draft a render prompt until all are available:

```text
Content ID + Scene ID
Approved source-card claims and prohibited claims
Approved hook/payoff for the scene
Shot purpose and target duration
Target ratio/platform
Allowed asset type: own 3D / vector / licensed stock / approved AI visual
Source-card citation that supports the depicted mechanism
```

If any input is missing, mark the scene **HOLD** and ask Production to complete storyboard/asset register information.

## Template selection

Use the upstream library only as a prompt-structuring reference.

| Health production need | Appropriate upstream-style structure | Project rule |
|---|---|---|
| Anatomy/process explainer | `infographic-engine` or `scientific-scale-diagram` | Use simplified, non-photorealistic structures; explicitly label as educational illustration |
| Evidence/method explainer | `infographic-engine`, chart, or document structure | Use fictional cards/data; do not reproduce journal figures or logos |
| Citation/limitation card | document/infographic structure | Generate background only when needed; typeset citations separately for accuracy |
| Brand/end-card graphic | brand/infographic structure | No health-product promotion or authority symbols |
| Mock social-post literacy scene | UI/document structure | Create fictional UI, source, and DOI; no real account, post, or medical claim |

Do **not** select portrait, realistic photography, character, or commercial-product templates for the Batch 1 health scenes unless a new source card and PPU review explicitly permit them.

## Prompt-building procedure

1. Identify exactly one educational claim the scene must make.
2. Select the simplest template structure that can explain that claim.
3. Write the prompt in concrete blocks:
   - educational subject/process;
   - composition and camera/crop;
   - style/materials/light;
   - labels that will be overlaid later;
   - target ratio and export role;
   - constraints/negative details.
4. Add a separate **overlay plan**. Do not rely on generated small text, DOI, scientific labels, or statistics; those must be typeset and manually verified in post-production.
5. Enter the prompt and outputs into the asset register with Content ID, Scene ID, upstream template ID, prompt version, generator/model (if later used), and review status.

## Default health-safe prompt constraints

Append/adapt these constraints for every Batch 1 visual:

```text
non-photorealistic educational medical illustration;
clean studio background; non-graphic;
no patient, no human suffering, no clinician or medical authority figure;
no real organ tissue, blood, wounds, surgery, needles, scans, or medical records;
no disease diagnosis, treatment, product, before-after, or fear imagery;
no celebrity, public figure, creator, trademark, journal figure, or real social-media account;
no tiny generated text, citations, statistics, or logos.
```

Use arrows, color plus shape/pattern, and empty space for verified labels. Colors must not be the sole indicator of direction or category.

## Rights and provenance rules

- The upstream repository's MIT code/skill license does **not** grant commercial rights to its gallery images, community prompt examples, third-party inspirations, or the output of a future image model.
- Do not copy upstream image assets, case images, screenshots, third-party examples, or prompts as final commercial production assets.
- Create a new scene-specific prompt from the approved source card; record the chosen template only as a structural reference.
- A future image provider/model must undergo its own commercial-output and input/asset review. This skill cannot clear it.
- Never place API keys, provider credentials, private source material, or personally identifying images in Git.

## Required output: visual prompt manifest

```text
Content ID / Scene ID:
Asset ID / prompt version:
Selected prompt-template structure:
Scene claim and source-card support:
Copyable generation prompt:
Negative constraints:
Overlay plan (verified text/citation/labels added outside model):
Target ratio and intended duration:
Generator/model/provider: pending approval
Rights/provenance status: HOLD until model/provider is cleared
Anatomy/factual reviewer:
PPU status:
```

## Stop conditions

Do not pass a prompt to any generator when:

- the scene implies diagnosis, treatment, or a personal health outcome;
- anatomy/process direction cannot be verified against the source card;
- a real patient, creator, doctor, journal image, account, or third-party style is requested;
- model/provider output terms are missing or unsuitable for commercial channel use;
- the user has not authorized the specific asset-render scope;
- a request would cause generic AI text to stand in for verified labels/citations.

## Current project status

- This skill is installed as a planning wrapper only.
- It is suitable for Batch 1 infographic/diagram prompt manifests after a render scope is explicitly selected.
- No upstream assets or prompts have been copied into production; no image model/API has been called.
- See `projects/visual-skill-integration-audit.md` and `projects/health-visual-production-spec.md`.
