# Agent Skills — hasil salinan dari postingan @cabbitar

Folder ini berisi **salinan utuh (verbatim)** semua agent skill yang dirujuk
postingan [@cabbitar](https://x.com/cabbitar/status/2115467413953056921), plus
satu skill baru (`rea-roadmap`) yang dibangun dari seluruh link postingan.

| Asal | Path upstream | Commit/branch | Lisensi |
| --- | --- | --- | --- |
| <https://github.com/morluto/rea> | `.agents/skills/` | `bf115be2cd900724a5bbd59a5cefc7af1dc2576f` (main) | ikuti `LICENSE` upstream |
| <https://github.com/alexgaoth/awesome-reverse-engineered> | `plugin/skills/find-reverse-engineered/` | `main` | MIT © 2026 Alex Gao (`find-reverse-engineered/LICENSE`) |
| <https://rea.tools/> | `docs/installation.md`, `docs/mcp-prompts.md` (dari repo REA) | commit yang sama | sama dengan upstream |

Isi skill upstream tidak diubah supaya `diff` terhadap upstream tetap bersih saat
sinkron ulang. Satu-satunya skill yang ditulis tangan di sini adalah
`rea-roadmap`.

## Daftar skill

| Skill | Asal | Kapan dipakai |
| --- | --- | --- |
| [`rea-roadmap`](rea-roadmap/SKILL.md) | **baru**, disusun dari 46 link postingan | Menjalankan roadmap 7 tahap (setup → Notes Export → CTF → APK → Electron/game → Ghidra → paper) sebagai alur kerja yang bisa diuji, plus indeks semua resource. |
| [`reverse-engineer-anything`](reverse-engineer-anything/SKILL.md) | `morluto/rea` | Skill utama REA: memilih tool per jenis target (native, managed, Electron/JS, APK, firmware, packaged, browser, capture jaringan/paket/signal), Evidence-first. |
| [`find-reverse-engineered`](find-reverse-engineered/SKILL.md) | `alexgaoth/awesome-reverse-engineered` | Mencari tool open-source hasil reverse engineering untuk app/API/protokol/format tertutup; indeks 17.000+ proyek lewat `scripts/re_index.py`. |
| [`rea-analysis-optimization`](rea-analysis-optimization/SKILL.md) | `morluto/rea` | Optimasi provider/workflow analisis (context, latency, CPU, memory) tanpa merusak Evidence. |
| [`rea-ci-tests-audit`](rea-ci-tests-audit/SKILL.md) | `morluto/rea` | Audit CI & test suite: false pass, fixture drift, biaya. |
| [`rea-tool-design`](rea-tool-design/SKILL.md) | `morluto/rea` | Merancang/mengubah tool investigasi, kontrak CLI/MCP, semantik Evidence. |
| [`rea-changelog-update`](rea-changelog-update/SKILL.md) | `morluto/rea` | Menyusun release notes/changelog dari Git history terpin. |

Setiap skill memakai **progressive disclosure**: `SKILL.md` adalah pintu masuk,
detail berat di `references/` dibaca hanya saat dibutuhkan.

## Isi `rea-roadmap`

```
rea-roadmap/
├── SKILL.md                      alur kerja 5 langkah + aturan turunan
├── references/
│   ├── resources.md              semua 46 link postingan yang sudah di-resolve
│   ├── learning-path.md          7 tahap: prompt, kriteria keluar, jebakan
│   ├── installation.md           salinan docs/installation.md upstream
│   ├── mcp-prompts.md            salinan docs/mcp-prompts.md upstream
│   └── source-verification.md    prosedur resolve t.co + bukti yang disimpan
└── scripts/
    └── check_readiness.sh        cek read-only: node, rea, Ghidra, JADX, Frida, target
```

## Catatan link relatif

Beberapa `SKILL.md` upstream menunjuk ke file di luar paket skill
(`../../../docs/…`, `../../../AGENTS.md`). Kalau tidak resolve di checkout ini,
buka versi upstream: `https://github.com/morluto/rea/blob/main/<path>`.

Ringkasan lengkap + tabel link ada di [`../../SKILLS.md`](../../SKILLS.md).
