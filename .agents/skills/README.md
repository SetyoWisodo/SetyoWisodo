# Agent Skills — salinan dari REA

Folder ini berisi **salinan utuh (verbatim)** semua agent skill yang ada di
repository GitHub yang dirujuk postingan
[@cabbitar](https://x.com/cabbitar/status/2115467413953056921):

- Upstream: <https://github.com/morluto/rea>
- Path asal: `.agents/skills/`
- Commit yang disalin: `bf115be2cd900724a5bbd59a5cefc7af1dc2576f` (branch `main`, 2026-10-29)
- Lisensi/atribusi: ikuti `LICENSE` upstream di <https://github.com/morluto/rea>

Tidak ada isi skill yang diubah, supaya `git diff` terhadap upstream tetap bersih
saat nanti mau sinkron ulang.

## Daftar skill

| Skill | Kapan dipakai |
| --- | --- |
| [`reverse-engineer-anything`](reverse-engineer-anything/SKILL.md) | Skill utama. Reverse engineering binary native, managed (.NET), Electron/JavaScript, APK/Android, firmware, packaged app (PyInstaller/Bun), browser, dan capture jaringan/paket/signal — plus membangun AgentEnv bundle dari web app. |
| [`rea-analysis-optimization`](rea-analysis-optimization/SKILL.md) | Optimasi provider REA & workflow analisis (context, latency, CPU, memory) tanpa merusak kebenaran hasil dan Evidence. |
| [`rea-ci-tests-audit`](rea-ci-tests-audit/SKILL.md) | Audit CI dan test suite: false pass, fixture drift, biaya/performa, workflow investigation. |
| [`rea-tool-design`](rea-tool-design/SKILL.md) | Merancang/mengubah tool investigasi, kontrak CLI/MCP, capability provider, semantik Evidence. |
| [`rea-changelog-update`](rea-changelog-update/SKILL.md) | Menyusun release notes/changelog dari riwayat Git yang sudah dipin, plus atribusi kontributor. |

Setiap skill memakai pola **progressive disclosure**: `SKILL.md` adalah pintu masuk
yang ringkas, detail berat ada di subfolder `references/` dan dibaca hanya saat
pertanyaan benar-benar membutuhkannya.

## Catatan link

Beberapa link relatif di dalam `SKILL.md` menunjuk ke file upstream yang bukan
bagian dari paket skill, misalnya `../../../docs/tool-design.md`,
`../../../AGENTS.md`, dan `../../../CONTRIBUTING.md`. Kalau link itu tidak
resolve di checkout ini, buka versi upstream-nya di
`https://github.com/morluto/rea/blob/main/<path>` (mis.
<https://github.com/morluto/rea/blob/main/docs/tool-design.md>).

Ringkasan cara pakai dan penerapannya di percakapan ini ada di
[`../../SKILLS.md`](../../SKILLS.md).
