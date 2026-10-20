# Daftar Lengkap Skill — Repositori GitHub untuk Publikasi Buku

Disusun: 2026-10-21 · Branch `arena/3b1aa1ad-setyowisodo`
Konteks: publikasi *Surviving the Future* (EN 299 hlm) dan *Bertahan Hidup di Masa Depan* (ID 311 hlm).
Semua skill di bawah ini adalah **instruksi/protokol kerja** (Markdown), bukan layanan berjalan — jadi bisa langsung saya terapkan pada `book.md`, `book_id.md`, dan Daftar Pustaka.

---

## 0. Ringkasan

| Kelompok | Jumlah | Isi |
|---|---|---|
| Skill inti ARS | **5** | `deep-research`, `academic-paper`, `academic-paper-reviewer`, `academic-pipeline`, `sr-screener` |
| Agen di dalamnya | **41** | 13 + 12 + 7 + 5 + 4 |
| Perintah `/ars-*` | **16** | pintasan mode (full, reviewer, citation-check, dll.) |
| Stack deep research (repo ini) | **8** | GPT Researcher, Open Deep Research, STORM, NVIDIA, Tongyi, Vane, MindSearch, Open WebUI |
| Skill produk digital (README repo ini) | **8** | Autonomous Research Pipeline … LLM Workspace & Deployment |
| Mesin pencari pendukung | **1** | Vane (37.5k★) |

Sumber utama:

1. **Imbad0202/academic-research-skills** — v3.23.1, **53.160★**, 2.846 file.
   *Academic Research Skills for Claude Code: research → write → review → revise → finalize.*
   Disalin ke `skills/ars/` (di-`.gitignore`, `--depth 1 --sparse`).
2. **ItzCrazyKns/Vane** — **37.525★**, *AI-powered answering engine* (self-hosted, SearXNG, mode deep research iteratif).
3. Delapan stack deep research pada `README.md` repo ini.

---

## 1. Lima Skill Inti ARS

| # | Skill | Versi | Agen | Mode | Keluaran utama | Peran untuk buku ini |
|---|---|---|---|---|---|---|
| 1 | `deep-research` | 2.12.1 | 13 | 8 | Laporan APA 7 / brief / anotasi / PRISMA | Riset, verifikasi sumber, fact-check, sintesis lintas sumber |
| 2 | `academic-paper` | 3.3.1 | 12 | 11 | Draf paper MD/DOCX/LaTeX/PDF | Menulis & merevisi bab, sitasi, abstrak, format |
| 3 | `academic-paper-reviewer` | 1.11.1 | 7 | 6 | 5 laporan review + keputusan editorial | Panel review simulasi (5 kursi) sebelum terbit |
| 4 | `academic-pipeline` | 3.23.1 | 5 | 10 tahap | Artefak per tahap + integrity gate | Orkestrasi seluruh proses sampai final |
| 5 | `sr-screener` | 1.0.0 | 4 | 8 | Protokol + log screening + PRISMA 2020 | Penyaringan sumber/rujukan secara sistematis |

### 1.1 `deep-research` — 13 agen, 8 mode

Agen: `research_question` (FINER), `research_architect` (metodologi), `bibliography` (APA 7), `source_verification` (grading bukti, deteksi jurnal predator, konflik kepentingan), `synthesis` (kontradiksi & gap), `report_compiler`, `editor_in_chief` (verdict Q1), `devils_advocate` (uji asumsi + logical fallacy), `ethics_review`, `socratic_mentor`, `risk_of_bias`, `meta_analysis`, `monitoring`.

| Mode | Agen aktif | Keluaran | Panjang |
|---|---|---|---|
| `full` (default) | 9 inti | Laporan APA 7 lengkap | 3.000–8.000 kata |
| `quick` | RQ + Biblio + Verifikasi + Report | Research brief | 500–1.500 |
| `review` | Editor + Devil's Advocate + Etika | Reviewer report atas teks yang diberikan | — |
| `lit-review` | Biblio + Verifikasi + Sintesis | Anotasi + sintesis | 1.500–4.000 |
| `three-way-scan` | Biblio + Verifikasi | Shortlist paper WHY/HOW/WHAT | 800–2.000 |
| `fact-check` | Verifikasi sumber | Laporan verifikasi | 300–800 |
| `socratic` | Mentor + RQ + Devil's Advocate | Research plan summary (iteratif) | — |
| `systematic-review` | 11 agen | Laporan PRISMA 2020 + data forest plot + tabel GRADE | 5.000–15.000 |

Referensi kunci: `argumentation_reasoning_framework.md`, `logical_fallacies.md`, `source_quality_hierarchy.md`, `systematic_review_protocol.md`, `methodology_patterns.md`, `socratic_questioning_framework.md`.

### 1.2 `academic-paper` — 12 agen, 11 mode

Agen: `intake`, `literature_strategist`, `structure_architect`, `argument_builder`, `draft_writer`, `citation_compliance`, `abstract_bilingual`, `peer_reviewer`, `formatter`, `socratic_mentor`, `visualization`, `revision_coach`.

| Mode | Pemicu | Keluaran |
|---|---|---|
| `full` | "tulis paper" | Draf lengkap (opsional gambar) |
| `plan` | "guide my paper" | Chapter plan + INSIGHT collection |
| `outline-only` | "outline paper" | Outline detail + evidence map |
| `revision` | "revisi paper" / komentar reviewer | Patch + draf revisi + apply report |
| `revision-coach` | "parse reviews" / "roadmap" | Roadmap + skeleton respons |
| `abstract-only` | "tulis abstrak" | Abstrak bilingual + keyword |
| `lit-review` | "literature review" | Bibliografi anotasi + sintesis |
| `format-convert` | "convert ke LaTeX/IEEE" | Dokumen terformat (APA 7 / Chicago / MLA / IEEE / Vancouver) |
| `citation-check` | "cek sitasi" | Laporan galat sitasi |
| `disclosure` | "AI disclosure" | Pernyataan disclosure sesuai venue |
| `rebuttal-audit` | "audit rebuttal" | QA draf bantahan |

Referensi kunci: `academic_writing_style.md`, `anti_leakage_protocol.md`, `writing_quality_check.md`, `writing_judgment_framework.md`, `statistical_visualization_standards.md`, `vlm_figure_verification.md`.

### 1.3 `academic-paper-reviewer` — 7 agen, panel 5 kursi, 6 mode

Kursi panel: **Journal-Fit Reviewer** (`eic_agent`) + **Peer Reviewer 1 metodologi** + **Peer Reviewer 2 domain/literatur** + **Peer Reviewer 3 lintas disiplin/dampak** + **Devil's Advocate** (tetap, mendeteksi logical fallacy & argumen lawan terkuat). `editorial_synthesizer_agent` merangkum konsensus/ketidaksepakatan.

Mode: `full`, `re-review` (verifikasi pasca-revisi), `quick`, `methodology-focus`, `guided` (Socratic), `calibration`.

Referensi kunci: `review_criteria_framework.md`, `quality_rubrics.md`, `editorial_decision_standards.md`, `statistical_reporting_standards.md`, `review_quality_thinking.md`.

### 1.4 `academic-pipeline` — 10 tahap

| Tahap | Nama | Skill | Keluaran |
|---|---|---|---|
| 1 | RESEARCH | `deep-research` | RQ brief, metodologi, bibliografi, sintesis |
| 2 | WRITE | `academic-paper` | Draf |
| **2.5** | **INTEGRITY** | `integrity_verification_agent` | Laporan integritas + koreksi (**wajib**) |
| 3 | REVIEW | `academic-paper-reviewer` | 5 laporan + keputusan + roadmap |
| 4 | REVISE | `academic-paper` | Draf revisi + respons |
| **3′** | **RE-REVIEW** | `academic-paper-reviewer` | Checklist verifikasi + isu sisa |
| **4′** | **RE-REVISE** | `academic-paper` | Draf kedua bila perlu |
| **4.5** | **FINAL INTEGRITY** | `integrity_verification_agent` | Laporan final (**wajib**) |
| 5 | FINALIZE | `academic-paper` | Final MD/DOCX/LaTeX/PDF |
| 6 | PROCESS SUMMARY | orchestrator | Rekaman proses + skor kolaborasi |

Agen: `pipeline_orchestrator`, `state_tracker`, `integrity_verification`, `collaboration_depth` (advisory), `claim_ref_alignment_audit` (opt-in).

### 1.5 `sr-screener` — 4 agen, 8 mode

Dua reviewer *blinded* (hanya Read/Grep, tanpa memori satu sama lain), satu adjudicator, QC auditor (seed study, near-miss, kappa/PABAK), reporter. Membaca RIS, PubMed `.nbib`, Web of Science, CSV; menghasilkan PRISMA 2020, log Excel, grup RIS, draf metode, dan `literature_corpus[]`.

Mode: `protocol`, `quick`, `pilot`, `ta-screen`, `ft-screen`, `adjudicate`, `audit`, `report`.

---

## 2. Enam belas Perintah `/ars-*`

| Perintah | Fungsi |
|---|---|
| `/ars-full` | Pipeline penuh: research → write → review → revise → finalize |
| `/ars-plan` | Perencanaan bab demi bab (Socratic) |
| `/ars-outline` | Outline detail + evidence map |
| `/ars-3w` | Bandingkan paper dengan kerangka WHY / HOW / WHAT |
| `/ars-lit-review` | Literatur review beranotasi |
| `/ars-abstract` | Abstrak bilingual + keyword |
| `/ars-revision` | Draf revisi + respons R&R |
| `/ars-revision-coach` | Roadmap dari komentar reviewer |
| `/ars-rebuttal-audit` | Audit draf bantahan terhadap komentar |
| `/ars-reviewer` | Panel review simulasi (mode `full`) |
| `/ars-citation-check` | Laporan galat sitasi |
| `/ars-format-convert` | Konversi LaTeX / DOCX / PDF / Markdown |
| `/ars-disclosure` | Pernyataan AI disclosure sesuai venue |
| `/ars-mark-read` | Tandai sinyal "sudah dibaca" untuk kunci sitasi |
| `/ars-unmark-read` | Cabut tanda tersebut |
| `/ars-cache-invalidate` | Hapus cache verifikasi untuk satu kunci sitasi |

---

## 3. "Logical Thinking" — di mana letaknya

Ini bukan satu skill terpisah, melainkan **lapisan penalaran** yang tersebar dan dipakai berkali-kali:

| Aset | Isi | Dipakai oleh |
|---|---|---|
| `deep-research/references/argumentation_reasoning_framework.md` | Model Toulmin (claim, ground, warrant, backing, qualifier, rebuttal) + cara menilai kekuatan argumen | `deep-research`, `academic-paper` |
| `deep-research/references/logical_fallacies.md` | Katalog **30+ logical fallacy** (formal: affirming the consequent, undistributed middle, false dilemma; informal: relevansi, kausalitas, generalisasi) | `devils_advocate_agent` |
| `shared/references/claim_strength_ladder.md` | Tangga kekuatan klaim: klaim tidak boleh lebih kuat daripada bukti | `academic-paper` (revisi) |
| `shared/references/protected_hedging_phrases.md` | Frasa hedging ("may", "preliminary", "in this context") dilindungi dari pemadatan | `report_compiler` |
| `shared/references/per_source_method_weaknesses.md` | Kelemahan metode per jenis sumber | `deep-research` |
| `academic-pipeline/references/claim_verification_protocol.md` | Fase A–E: verifikasi klaim numerik/faktual terhadap sumber | `integrity_verification_agent` |
| `academic-pipeline/agents/claim_ref_alignment_audit_agent.md` | Audit klaim ↔ rujukan, mendeteksi `claim_drift`, `uncited_assertions`, `constraint_violations` | pipeline (opt-in) |
| `devils_advocate_agent` (3 skill) | Uji asumsi, cari penjelasan alternatif, cek bias konfirmasi | deep-research, reviewer, pipeline |
| `two_stage_review_protocol.md` + gate 2.5/4.5 | Review dua tahap + integritas wajib sebelum & sesudah revisi | pipeline |

---

## 4. Delapan Stack Deep Research (dari `README.md` repo ini)

| # | Tool | Repo | Kegunaan |
|---|---|---|---|
| 1 | GPT Researcher | `assafelovic/gpt-researcher` | Agen riset otonom, laporan bersitasi |
| 2 | Open Deep Research | `langchain-ai/open_deep_research` | Orkestrasi LangGraph, eval |
| 3 | STORM | `stanford-oval/storm` | Outline multi-perspektif (cocok untuk struktur buku) |
| 4 | NVIDIA Deep Researcher | `NVIDIA-AI-Blueprints/deep-researcher-agent` | Riset enterprise, konektor aman |
| 5 | Tongyi DeepResearch | `Alibaba-NLP/DeepResearch` | Model agen 30B MoE, hemat biaya |
| 6 | Vane | `ItzCrazyKns/Vane` | Answering engine privat, deep research iteratif |
| 7 | MindSearch | `InternLM/MindSearch` | Multi-agent web search |
| 8 | Open WebUI | `open-webui/open-webui` | Workspace LLM lokal, RAG, pipeline |

**Vane** (37.525★): SearXNG multi-engine, pilihan sumber (web / diskusi / akademik), mode Speed–Balanced–Quality, widget, unggah dokumen — dipakai sebagai mesin verifikasi silang, bukan penulis.

---

## 5. Delapan Skill Produk Digital (README repo ini)

1. Autonomous Research Pipeline (GPT Researcher)
2. LangGraph Orchestration & Evals (Open Deep Research)
3. Multi-Perspective Knowledge Curation (STORM)
4. Enterprise Trusted Insights (NVIDIA)
5. Cost-Efficient MoE Research Agent (Tongyi)
6. Private Answering Engine (Vane)
7. Human-Mind Search Framework (MindSearch)
8. LLM Workspace & Deployment (Open WebUI)

---

## 6. Penerapan pada Buku — 7 Gate Publikasi

| Gate | Nama | Skill/protokol | Masukan | Keluaran | Blokir? |
|---|---|---|---|---|---|
| 0 | Inventaris | — | `book.md`, `book_id.md`, `REFS` | Daftar bab, sub-bab, tabel, klaim, rujukan | Tidak |
| 1 | Integritas sumber & sitasi | `claim_verification` + `citation-check` | Semua sitasi dalam teks vs Appendix D | Daftar sitasi hilang/berlebih, DOI/tahun salah | **Ya** |
| 2 | Audit fakta & angka | `deep-research` mode `fact-check` | 24 tabel skenario + DATA_POINTS | Setiap angka ↔ sumber; klaim tanpa sumber | **Ya** |
| 3 | Audit argumen & logika | `logical_fallacies` + Toulmin + `claim_strength_ladder` | Paragraf argumentatif tiap bab | Fallacy, klaim berlebih, generalisasi, kausalitas palsu | **Ya** |
| 4 | Panel review 5 kursi | `academic-paper-reviewer` mode `full` | Draf per bab / seluruh buku | 5 laporan + keputusan + roadmap | Tidak (advisory) |
| 5 | Revisi & re-review | `academic-paper` `revision` + reviewer `re-review` | Temuan Gate 1–4 | Patch + verifikasi | **Ya** |
| 6 | Produksi & format | `format-convert` + `citation-check` | Naskah final | PDF/EPUB/DOCX, APA 7, daftar isi/tabel | **Ya** |
| 7 | Pra-terbit | `disclosure` + `plagiarism_detection` + `reproducibility_audit` | Naskah final | Pernyataan AI, similaritas, audit reproduksi | **Ya** |

Catatan: pada buku ini, "daftar pustaka" adalah **Appendix D**, dan setiap bab memakai sitasi `Nama (Tahun)`. Gate 1 dan 2 karena itu bisa dijalankan otomatis dari `book.md` + `GEN` + `REFS`.

---

## 7. Status 75% → 100%

Sudah selesai (terverifikasi): struktur 24 bab, 24 tabel skenario, 96 sub-bab + 48 sub-bab baru (N.5/N.6), tata letak (justify, indent 12,7 mm, judul 2 baris, Daftar Isi & Daftar Tabel akurat 24/24), tipografi, akronim, tanda baca, halaman 299/311.

Sisa pekerjaan menurut gate:

- **Gate 1** — audit 99 entri Daftar Pustaka + seluruh sitasi dalam teks (belum pernah dijalankan penuh).
- **Gate 2** — verifikasi angka pada 24 tabel + 12 `DATA_POINTS` terhadap sumber primer.
- **Gate 3** — sapuan 24 bab untuk fallacy, klaim absolut, dan pengulangan template yang masih tersisa (mis. frasa tema yang diulang belasan kali per paragraf).
- **Gate 4–5** — panel review + revisi.
- **Gate 6–7** — produksi final, disclosure, similaritas.

Urutan yang disarankan karena urgent: **Gate 3 → Gate 2 → Gate 1 → Gate 6** (logika dulu karena memengaruhi redaksi; angka dan sitasi setelah redaksi stabil, lalu produksi).

---

## 8. Catatan Operasional

- Salinan skill: `skills/ars/` (di-`.gitignore`, tidak masuk repo). Segarkan dengan:
  `git -C skills/ars pull --depth 1` atau clone ulang `--depth 1 --filter=blob:none --sparse`.
- Skill ARS berbahasa Inggris; keluaran buku tetap Inggris/Indonesia sesuai naskah.
- Vane memerlukan instance (Docker) untuk dipakai sebagai mesin pencari; untuk audit naskah, protokol ARS + verifikasi silang referensi sudah cukup.
- Semua gate di atas bisa saya jalankan langsung di repo ini dan hasilnya ditulis sebagai laporan Markdown + perbaikan naskah.
