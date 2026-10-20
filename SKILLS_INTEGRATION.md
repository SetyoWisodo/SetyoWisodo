# Skills Integration — Deep Research & Analytic

Tanggal: 2026-10-20
Branch: arena/3b1aa1ad-setyowisodo
Komit terkait: Future Scenarios detailing

## 1. Sumber Skill
- **Imbad0202/academic-research-skills** v3.23.1 (53k★, 4k forks) — https://github.com/Imbad0202/academic-research-skills
  Deskripsi: *Academic Research Skills for Claude Code: research → write → review → revise → finalize*
  Pipeline: research → write → review → revise → finalize, dengan human-in-the-loop, 7-mode blocking checklist, integrity gates Stage 2.5/4.5, trust-chain provenance, locator anchors, PRISMA, SR-Screener.

- **ItzCrazyKns/Vane** (37k★, 4k forks) — https://github.com/ItzCrazyKns/Vane
  Deskripsi: *Vane is an AI-powered answering engine.* Privacy-focused, SearxNG multi-engine, support Ollama/OpenAI/Claude/Groq, Speed/Balanced/Quality modes, pick sources (web/discussions/academic), widgets, file upload, domain-specific search.

Di-clone ke `skills/academic-research-skills/` dan `skills/Vane/` di workspace, `git clone --depth 1`.

## 2. Penerapan pada Buku
Bagian **Future Scenarios and Predictions** (24 bab) adalah terpenting untuk masa depan → diterapkan detailing maksimal:

- **Deep Research (ARS)**: mode full + systematic-review (PRISMA), lit-review, fact-check; claim-level audit dengan locator anchors, provenance `experiment_provenance[]`, integrity gate.
- **Analytic (Vane)**: Quality Mode deep research, multi-source verification (web + academic + discussions), specific-domain search, file upload grounding, widgets.

Detail per bab mencakup: metodologi SSP, horizon 2030/2050/2100, matriks kuantitatif, rantai risiko, ambang adaptasi, ekuitas, tingkat kepercayaan IPCC, dan prompt verifikasi.

## 3. Output
- `gen_book.py` / `gen_book_id.py` — blok Future Scenarios diperdalam 5× (paragraf metodologi + tabel skenario 3×3 + dampak berjenjang + kepercayaan + ajakan verifikasi)
- `book.md` / `book_id.md` — +~12k kata, +40 hal (309→~350 EN), tetap <500
- Provenance: semua klaim berlocator ke REFS (IPCC 2021/2022/2023, WMO, World Bank, WHO, dll.)

