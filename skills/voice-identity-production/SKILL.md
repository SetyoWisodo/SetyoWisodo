---
name: voice-identity-production
description: Safely maintain one consistent voice identity for evidence-based health videos. Use when a script needs narration, a VoiceStudio profile is evaluated, or voice assets require QA.
status: conditional
integration_candidate: VoiceStudio
---

# Voice Identity Production Skill

## Purpose

Maintain one recognisable, consistent narrator identity for the health channel without cloning an unverified person, implying medical credentials, or using models whose rights do not permit the intended commercial channel use.

This skill governs narration only. It never writes, expands, weakens, or changes an evidence-approved health claim.

## Non-negotiable gates

1. **No consent, no clone.** A real person's voice can be used only with explicit, recorded permission from that voice owner.
2. **No verified commercial terms, no production model.** Review the exact engine, model/weight revision, tokenizer/component terms, and output rights. An application license alone is insufficient.
3. **No approved Voice ID, no final narration.** Use only one approved, versioned profile such as `VOICE-ID-v1`.
4. **No audio generation before explicit approval.** Do not download models, launch a model backend, clone a voice, or synthesize audio until the owner approves that specific stage.
5. **No impersonation.** Never imitate a doctor, expert, celebrity, public figure, other creator, or a non-consenting person.
6. **No false authority.** The narrator must not claim or imply clinical credentials that the channel does not have.

## Required records

Before generation, find or create a private Voice Identity Card containing:

```text
Voice ID and status
Source: owner voice / licensed synthetic voice
Consent or license evidence
VoiceStudio/tool version
Exact engine/model/weight revision
License review: code + model + components + output use
Reference audio location and exact transcript (private, never Git)
Indonesian pronunciation test results
Audio QA results and approval date
```

## VoiceStudio procedure

1. Discover installed VoiceStudio backend and existing voice profiles first; do not overwrite profiles or guess IDs.
2. Preserve opt-in cloud/analytics choices. Do not answer consent prompts for the owner.
3. Ask before model downloads. State the exact model, source, download size, hardware expectation, license category, and unresolved risks.
4. If cloning is approved, record the owner/source, consent, recording transcript, and profile settings.
5. For a profile test, synthesize only the user-approved short test script using the authorized voice.
6. Save the resulting profile as a versioned Voice ID. Freeze engine, model revision, reference selection, speaking style, and normalization rules for the batch.
7. Re-test when the profile, engine, model version, reference audio, or pronunciation rules change.

## Indonesian narration QA

Generate a short test set before a batch and verify manually:

- everyday Indonesian phrasing is clear and natural;
- anatomical/scientific terms, acronyms, numerals, units, and English loanwords are pronounced as intended;
- tempo supports educational comprehension;
- no dropped words, clipping, metallic artefacts, false breaths, or unnatural pauses;
- the result sounds consistent with the approved Voice ID;
- the narrator does not sound like a doctor/person whose identity was not authorized.

Maintain a per-video pronunciation sheet. If a term is wrong, correct text normalization or a phonetic guide and regenerate; subtitles do not excuse inaccurate audio.

## Production hand-off

```text
Approved source card + approved script
→ pronunciation sheet
→ approved VOICE-ID-v1 narration draft
→ audio QA
→ visual/subtitle assembly
→ independent PPU review of exact final version
```

Attach Voice ID/version, model review status, and audio QA result to the PPU package.

## Stop conditions

Set status to **HOLD** and do not generate final audio if any of these occurs:

- consent, ownership, or source provenance is missing;
- a model's commercial inference/output rights are unknown, restricted, or not documented;
- the voice sounds materially like someone other than the authorized source;
- Indonesian pronunciation fails a health-safety-relevant phrase;
- the requested content exceeds the channel's education-not-advice boundaries;
- another producer attempts to replace the approved Voice ID without a new QA review.

## Current project status

- VoiceStudio was evaluated as a functional candidate only.
- The selected candidate route is the account owner's voice adapted into an AI narrator character; formal consent and persona choices are still pending.
- No profile, reference recording, model, backend, cloning, or generated audio has been created.
- The default VoiceStudio OmniVoice route must be treated as non-commercial/unapproved for this monetization-oriented channel until a separate exact-model review says otherwise.
- See `projects/voice-identity-production-plan.md` for governance, activation stages, and approval wording.
