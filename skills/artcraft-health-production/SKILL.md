---
name: artcraft-health-production
description: Govern optional ArtCraft use for controlled 2D/3D composition and image-to-video production assets for the health channel. Requires an approved local workstation, provider/model rights review, asset register, and explicit per-batch render authorization.
status: blocked-pending-environment-and-provider-clearance
upstream:
  repository: https://github.com/storytold/artcraft
  audited_commit: 63e6176
  code_license: MIT OR Apache-2.0
---

# ArtCraft Health Production Skill

## Purpose

Use ArtCraft, if later approved and installed on the owner's own workstation, as a **controlled composition and asset-production environment** for non-graphic health visuals. Its useful roles are 2D/3D scene blocking, image compositing, image editing, and image-to-video shot drafts.

ArtCraft is not a licence clearance service and is not a production model itself. Its image/video result rights depend on the selected provider and model. This skill therefore remains blocked until the provider, model, account terms, asset storage, and render scope are all reviewed.

## What ArtCraft can be considered for

| Allowed candidate role | Batch 1 example |
|---|---|
| 2D/3D scene blocking | Place a simplified lung, alveoli cluster, arrows, and camera for H01 |
| Composition consistency | Reuse approved scene geometry, palette, and layout across crops |
| Image compositing/editing | Assemble creator-owned illustration layers with verified labels overlaid outside the model |
| Image-to-video draft | Subtle camera move, arrow travel, or layer motion after a static scene has passed visual QA |

## What it must not be used for

- Rendering a patient, doctor, clinical setting, surgery, blood, real organ tissue, medical imaging, injury, or fear-based health visual.
- Generating final scientific labels, citations, statistics, diagnosis, treatment, or health-product claims.
- Copying a journal figure, real social account, creator's visual identity, celebrity/public figure, or medical professional likeness.
- Sending reference material, private voice/audio, patient material, or credentials to an unreviewed provider.
- Switching providers/models silently after an asset has been approved.

## Environment gate

Do not install ArtCraft in the current sandbox. The audited upstream project is a Rust/Tauri desktop application and its development setup requires Rust, Node, npm, and Tauri; this sandbox has no Rust/Cargo, no GPU, and limited memory.

Only assess installation on a machine controlled by the owner after this record is completed:

```text
Machine/OS:
CPU, RAM, GPU/VRAM, free storage:
ArtCraft release/version/source:
Local data directory and backup/encryption plan:
Network and provider endpoints permitted:
Person responsible for updates/uninstall:
```

## Provider/model gate

ArtCraft can route image/video work through its own services and external providers such as fal or Midjourney. The code's `MIT OR Apache-2.0` licence does not grant rights for any provider, model, generated output, or uploaded input.

Before account login, API key entry, model download, or generation, record:

```text
Provider and exact model/version:
Official terms and commercial-output rights:
Input retention/training policy and data location:
Required attribution, disclosure, and prohibited uses:
Pricing/credit approval and spending limit:
API/account owner:
Asset download/deletion policy:
```

Never store provider keys in this repository, a prompt manifest, or chat. The owner enters credentials locally only after approving the provider.

## Production procedure after all gates PASS

1. Receive a source-card-approved scene and visual prompt manifest.
2. Build the composition from creator-owned/licensed layers or an approved generated still.
3. Add verified labels, arrows, subtitles, citations, and disclaimer in normal editing layers—not via generative text.
4. Render a **silent internal draft** first, tagged with Content ID, Scene ID, Asset ID, ArtCraft version, provider/model, and prompt version.
5. Review visual QA: anatomy direction, non-graphic standard, source-card boundaries, layout, rights, and disclosure.
6. Submit the exact output to PPU. Do not use a different export or change model/provider after review.

## Image-to-video rules

- Use restrained educational motion: camera move, zoom through a diagram, arrow flow, layer reveal, or rotating non-graphic 3D structure.
- Keep motion consistent with the source-card claim; a beautiful movement that reverses a pathway or adds unverified biology fails QA.
- Do not use video generation to hallucinate labels, physiology, symptoms, treatment results, or patient behavior.
- Render no voice, music, or public-ready complete video in this skill. Audio and final assembly have their own gates.

## Required ArtCraft asset record

```text
Content ID / Scene ID / Asset ID / version:
ArtCraft version and local project path (private):
Provider + exact model/version:
Input asset IDs and licences:
Prompt manifest version:
Animation/motion instruction:
Output filename/hash and ratio:
Commercial-output terms reviewed by:
Disclosure decision:
Visual QA result:
PPU result:
```

## Stop conditions

Set status to **HOLD** if ArtCraft is not installed on an owner-controlled workstation, a selected provider/model lacks verified commercial rights, a scene violates the non-graphic health visual rules, the user has not selected render scope, or any asset's provenance is incomplete.

## Current project status

- ArtCraft was assessed as an optional future desktop composition/video workflow only.
- It is not installed; no provider account, API key, model, project file, image, video, or local render exists.
- No render task may be dispatched through ArtCraft until explicit provider/model and batch scope approval.
- See `projects/visual-skill-integration-audit.md` for audit conclusions and activation gates.
