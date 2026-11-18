# Agent Skills — dua pustaka: REA (@cabbitar) dan gerak (@0xMovez)

Folder ini berisi dua pustaka:

- **REA** — salinan utuh (verbatim) semua agent skill yang dirujuk postingan
  [@cabbitar](https://x.com/cabbitar/status/2115467413953056921), plus `rea-roadmap` dan
  `rea-workflow` yang dibangun dari seluruh link postingan.
- **Gerak** — 20 repo dari postingan
  [@0xMovez](https://x.com/0xMovez/status/2121312707588583455). Lima skill upstream berlisensi
  MIT disalin verbatim; enam belas item lain adalah panduan yang ditulis di repo ini karena
  upstream bukan skill (pustaka) atau tidak punya berkas lisensi.

| Asal | Path upstream | Commit/branch | Lisensi |
| --- | --- | --- | --- |
| <https://github.com/morluto/rea> | `.agents/skills/` | `bf115be2cd900724a5bbd59a5cefc7af1dc2576f` (main) | ikuti `LICENSE` upstream |
| <https://github.com/alexgaoth/awesome-reverse-engineered> | `plugin/skills/find-reverse-engineered/` | `main` | MIT © 2026 Alex Gao (`find-reverse-engineered/LICENSE`) |
| <https://rea.tools/> | `docs/installation.md`, `docs/mcp-prompts.md` (dari repo REA) | commit yang sama | sama dengan upstream |
| <https://github.com/reacher-z/Awesome-REA> | `AGENTS.md`, `data/README.md`, `scripts/validate.py`, `CONTRIBUTING.md` | dibaca di `a1a6b24` (main, 8 Nov 2026) | MIT © reacher-z — **tidak ada berkas upstream yang disalin** |

Isi skill upstream tidak diubah supaya `diff` terhadap upstream tetap bersih saat
sinkron ulang. Satu-satunya skill yang ditulis tangan di sini adalah
`rea-roadmap`.

## Daftar skill

| Skill | Asal | Kapan dipakai |
| --- | --- | --- |
| [`rea-workflow`](rea-workflow/SKILL.md) | **baru** — penggabung 7 skill | **Pintu masuk tunggal.** Loop 8 fase (F0 intake → F7 tutup) dengan gate, kontrak Evidence, routing target, mesin state sesi, dan peta delegasi ke skill lain. |
| [`rea-roadmap`](rea-roadmap/SKILL.md) | **baru**, disusun dari 46 link postingan | Menjalankan roadmap 7 tahap (setup → Notes Export → CTF → APK → Electron/game → Ghidra → paper) sebagai alur kerja yang bisa diuji, plus indeks semua resource. |
| [`reverse-engineer-anything`](reverse-engineer-anything/SKILL.md) | `morluto/rea` | Skill utama REA: memilih tool per jenis target (native, managed, Electron/JS, APK, firmware, packaged, browser, capture jaringan/paket/signal), Evidence-first. |
| [`find-reverse-engineered`](find-reverse-engineered/SKILL.md) | `alexgaoth/awesome-reverse-engineered` | Mencari tool open-source hasil reverse engineering untuk app/API/protokol/format tertutup; indeks 17.000+ proyek lewat `scripts/re_index.py`. |
| [`rea-analysis-optimization`](rea-analysis-optimization/SKILL.md) | `morluto/rea` | Optimasi provider/workflow analisis (context, latency, CPU, memory) tanpa merusak Evidence. |
| [`rea-ci-tests-audit`](rea-ci-tests-audit/SKILL.md) | `morluto/rea` | Audit CI & test suite: false pass, fixture drift, biaya. |
| [`rea-tool-design`](rea-tool-design/SKILL.md) | `morluto/rea` | Merancang/mengubah tool investigasi, kontrak CLI/MCP, semantik Evidence. |
| [`rea-changelog-update`](rea-changelog-update/SKILL.md) | `morluto/rea` | Menyusun release notes/changelog dari Git history terpin. |
| [`rea-catalog`](rea-catalog/SKILL.md) | **baru** — dari `reacher-z/Awesome-REA` (MIT) | Mencari tool/paper RE di katalog 1.130 + 123 + 235 catatan lewat GitHub API, dan memeriksa satu catatan baru terhadap format katalog (field wajib, kosakata `relationship`/`targets`/`class`, bukti terpin, `verified_at`, larangan kalimat tinjauan) sebelum diusulkan. |

Mulai dari `rea-workflow`; skill lain adalah rujukan yang dipanggil per fase
(lihat `rea-workflow/references/skill-map.md`).

Setiap skill memakai **progressive disclosure**: `SKILL.md` adalah pintu masuk,
detail berat di `references/` dibaca hanya saat dibutuhkan.

## Isi `rea-workflow`

```
rea-workflow/
├── SKILL.md                     loop 8 fase + gate + aturan + format jawaban
├── references/
│   ├── phases.md                detail per fase: masuk, lakukan, gate, salah umum
│   ├── target-routing.md        matriks target → tool pertama (termasuk mode tanpa MCP)
│   ├── evidence-contract.md     isi minimum satu butir Evidence + larangan
│   ├── skill-map.md             skill mana dipakai di fase mana, plus non-goal
│   ├── re-toolchain.md          20 repo toolchain (@0xDeniAi): 5 grup, lisensi, peran
│   └── re-toolchain.json        versi mesin untuk `session.sh tools`
├── templates/{finding,spec}.md  lembar temuan + SPEC.md mode rebuild
└── scripts/session.sh           state machine: init/status/gate/advance/log/unknown/tools/report
```

## Isi `rea-roadmap`

```
rea-roadmap/
├── SKILL.md                      alur kerja 5 langkah + aturan turunan
├── references/
│   ├── resources.md              semua 46 link postingan yang sudah di-resolve
│   ├── resources.json            versi mesin (43 entri) untuk query offline
│   ├── learning-path.md          7 tahap: prompt, kriteria keluar, jebakan
│   ├── installation.md           salinan docs/installation.md upstream
│   ├── mcp-prompts.md            salinan docs/mcp-prompts.md upstream
│   └── source-verification.md    prosedur resolve t.co + bukti yang disimpan
└── scripts/
    ├── check_readiness.sh        cek read-only: node, rea, Ghidra, JADX, Frida, target
    └── find_resource.sh          query resources.json per tahap/kategori/kata
```

## Catatan link relatif

Beberapa `SKILL.md` upstream menunjuk ke file di luar paket skill
(`../../../docs/…`, `../../../AGENTS.md`). Kalau tidak resolve di checkout ini,
buka versi upstream: `https://github.com/morluto/rea/blob/main/<path>`.

Ringkasan lengkap + tabel link ada di [`../../SKILLS.md`](../../SKILLS.md).

---

## Pustaka gerak — @0xMovez (20 repo, 22 skill)

Sumber: <https://x.com/0xMovez/status/2121312707588583455> (13 Nov 2026).
Semua tautan `t.co` di-resolve dan tiap repo diverifikasi lewat GitHub API pada 29 Okt 2026.
Tabel lengkap 20 item ada di [`../../SKILLS.md`](../../SKILLS.md) bagian B.

| Skill | Path upstream | Commit | Lisensi | Cara dibuat |
| --- | --- | --- | --- | --- |
| `motion-design` | `LottieFiles/motion-design-skill` → `skills/motion-design/` | `2e1f3c052dd7` | MIT © LottieFiles | salinan verbatim + `LICENSE` |
| `hairline-create` | `lucasmarkes/hairline` → `skills/hairline-create/` | `034f4bf9902c` | MIT © Lucas Markes | salinan verbatim + `LICENSE` |
| `hairline-adopt` | `lucasmarkes/hairline` → `skills/hairline-adopt/` | `034f4bf9902c` | MIT © Lucas Markes | salinan verbatim + `LICENSE` |
| `anatomy` | `wheresryan22/anatomy` → `SKILL.md`, `references/`, `kit/`, `agents/` | `1482e8469b0a` | MIT © Ryan | salinan verbatim (contoh PDF/HTML besar tidak disalin) + `LICENSE` |
| `anatomy-reveal` | `annnguyentt/anatomy-reveal-skill` → `SKILL.md`, `references/`, `scripts/`, `template/*.mjs` | `dd01e1c04559` | MIT © annnguyentt | salinan verbatim (demo mp4/png tidak disalin) + `LICENSE` |
| `motion-ai-kit` | `motiondivision/ai-kit` → `plugins/motion/skills/motion/` | `1e424943582c` | **tidak ada LICENSE** | ditulis sendiri; upstream hanya ditautkan |
| `remotion-skills` | `remotion-dev/skills` → 13 folder `skills/remotion-*` | `3e20ac75161b` | **tidak ada LICENSE** | indeks + ringkasan, ditulis sendiri |
| `blender-mcp` | `scenario-labs/blender-plugin` (ekstensi + MCP lokal) | `885bfbabfdf8` | GPL-3.0-or-later | ditulis sendiri; tidak menyalin berkas GPL |
| `threejs` | `mrdoob/three.js` | `43678c04423a` | MIT | ditulis sendiri |
| `rapier-physics` | `pmndrs/react-three-rapier` | `ae5c3fede5ca` | MIT | ditulis sendiri |
| `postprocessing` | `pmndrs/react-postprocessing` | `e07ef9a890c8` | MIT | ditulis sendiri |
| `quarks-vfx` | `Alchemist0823/three.quarks` | `9d0445c5949c` | MIT | ditulis sendiri |
| `tweakpane` | `cocopon/tweakpane` | `50a18c3dba67` | MIT | ditulis sendiri |
| `gsap` | `greensock/GSAP` | `5e6c35ff8eed` | GreenSock Standard | ditulis sendiri |
| `remotion` | `remotion-dev/remotion` | `8919b283f361` | Remotion License | ditulis sendiri |
| `manim` | `ManimCommunity/manim` | `ab7f9527fa2b` | MIT | ditulis sendiri |
| `lottie` | `airbnb/lottie-web` | `bede03d25d23` | MIT | ditulis sendiri |
| `openverse-audio` | `WordPress/openverse` | `6a3bd6cb07f8` | MIT | ditulis sendiri |
| `librosa-beat` | `librosa/librosa` | `76f10b8d2d00` | ISC | ditulis sendiri |
| `whisperx-captions` | `m-bain/whisperX` | `b904f02b7e1f` | BSD-2-Clause | ditulis sendiri |
| `ffmpeg-encode` | `FFmpeg/FFmpeg` | `3a78197c4c96` | LGPL/GPL | ditulis sendiri |
| `motion-studio` | — | — | ditulis di repo ini | pintu masuk: peta tahap → skill |

**Kenapa tidak semua disalin.** Empat repo skill upstream punya `LICENSE` MIT → disalin apa
adanya. `ai-kit` dan `remotion-dev/skills` **tidak punya berkas lisensi**; menyalin isinya
berarti mengambil hak yang tidak diberikan, jadi keduanya hanya ditautkan. Tujuh repo di bawah
ambang 3.000 bintang yang biasa dipakai repo ini tetap dimasukkan karena Anda meminta semua
item di postingan — kolom ★ di `SKILLS.md` membuatnya kelihatan.

**Sinkron ulang skill yang disalin verbatim:**

```bash
S=$(mktemp -d)
curl -sL https://codeload.github.com/LottieFiles/motion-design-skill/tar.gz/refs/heads/main | tar xz -C $S
rsync -a --delete $S/motion-design-skill-main/skills/motion-design/ .agents/skills/motion-design/ --exclude LICENSE

curl -sL https://codeload.github.com/lucasmarkes/hairline/tar.gz/refs/heads/main | tar xz -C $S
rsync -a $S/hairline-main/skills/hairline-create/ .agents/skills/hairline-create/ --exclude LICENSE
rsync -a $S/hairline-main/skills/hairline-adopt/  .agents/skills/hairline-adopt/  --exclude LICENSE

curl -sL https://codeload.github.com/wheresryan22/anatomy/tar.gz/refs/heads/main | tar xz -C $S
rsync -a $S/anatomy-main/SKILL.md $S/anatomy-main/references/ .agents/skills/anatomy/

curl -sL https://codeload.github.com/annnguyentt/anatomy-reveal-skill/tar.gz/refs/heads/main | tar xz -C $S
rsync -a $S/anatomy-reveal-skill-main/{SKILL.md,references,scripts} .agents/skills/anatomy-reveal/
```
