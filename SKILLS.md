# SKILLS.md — pustaka skill repo ini

Dua pustaka skill, dua sumber. Keduanya ada di `.agents/skills/`.

| Bagian | Sumber | Skill | Pintu masuk | Lokasi |
| --- | --- | --- | --- | --- |
| **A** | [@cabbitar — REA](https://x.com/cabbitar/status/2115467413953056921) + [@0xDeniAi](https://x.com/0xDeniAi/status/2114847015091794206) | 9 | [`rea-workflow`](.agents/skills/rea-workflow/SKILL.md) | bagian 1–5 di bawah |
| **B** | [@0xMovez — 20 repo motion studio](https://x.com/0xMovez/status/2121312707588583455) | **22** | [`motion-studio`](.agents/skills/motion-studio/SKILL.md) | bagian 6 di bawah |

Isi bagian A ditulis untuk pekerjaan reverse engineering; bagian B untuk gerak, 3D, suara, dan
encode video. Keduanya tidak saling bergantung.

---

## Bagian A — REA (@cabbitar)


Sumber: [@cabbitar — "STOP WASTING HOURS TRYING TO LEARN REA"](https://x.com/cabbitar/status/2115467413953056921) (2026-10-28).

| Item | Nilai |
| --- | --- |
| Postingan yang diadopsi | 2 — [@cabbitar (roadmap REA)](https://x.com/cabbitar/status/2115467413953056921) + [@0xDeniAi (20 repo toolchain)](https://x.com/0xDeniAi/status/2114847015091794206) |
| Link di postingan @cabbitar | 46 baris → **38 URL unik**, 37 terverifikasi, 1 mati |
| Repo di postingan @0xDeniAi | **20** (16 bertautan + 4 disebut tanpa tautan) — semua dikonfirmasi via GitHub API |
| Skill tersalin/dibuat | **9 skill** — 5 dari `morluto/rea`, 1 finder (MIT), 2 disusun di repo ini, 1 katalog (Awesome-REA, MIT) |
| Pintu masuk | [`rea-workflow`](.agents/skills/rea-workflow/SKILL.md) — satu loop 8 fase |
| Lokasi | [`.agents/skills/`](.agents/skills/) |
| Metode | `cp -r` verbatim untuk skill upstream; `rea-roadmap` ditulis dari hasil resolusi link; `rea-catalog` ditulis dari `AGENTS.md` + `data/README.md` + `scripts/validate.py` Awesome-REA |
| Tanggal verifikasi link | 2026-10-29 |

---

## 1. Skill yang aktif di repo ini

| # | Skill | Asal | Fungsi |
| --- | --- | --- | --- |
| 0 | **rea-workflow** | **baru** — penggabung semuanya | Pintu masuk tunggal: loop 8 fase + gate + kontrak Evidence + routing + state sesi |
| 1 | **rea-roadmap** | **baru** — dibuat dari 46 link postingan | Alur kerja 7 tahap + indeks semua resource + skrip cek kesiapan |
| 2 | **reverse-engineer-anything** (v55) | `morluto/rea` | Routing tool per jenis target, Evidence-first, 7 file referensi |
| 3 | **find-reverse-engineered** | `alexgaoth/awesome-reverse-engineered` | Cari tool open-source hasil RE (indeks 17.000+ proyek), plus MCP server di repo itu |
| 4 | **rea-analysis-optimization** | `morluto/rea` | Optimasi provider/workflow analisis |
| 5 | **rea-ci-tests-audit** | `morluto/rea` | Audit CI & test suite |
| 6 | **rea-tool-design** | `morluto/rea` | Desain tool investigasi & semantik Evidence |
| 7 | **rea-changelog-update** | `morluto/rea` | Release notes dari Git history terpin |
| 8 | **rea-catalog** | `reacher-z/Awesome-REA` (MIT, 1.999★) | Baca katalog 1.130 tool + 123 relasi REA + 235 paper dengan saringan `target`/`relationship`; periksa catatan baru terhadap format katalog sebelum diusulkan |

Front-matter `name` + `description` tiap skill adalah pemicunya: agent memilih
skill dari deskripsi itu, isi lengkap baru dimuat saat relevan.

---

## 2. Semua link postingan @cabbitar (sudah di-resolve dari `t.co`)

### START HERE

| Label | URL |
| --- | --- |
| REA Official Repository | <https://github.com/morluto/rea> |
| REA Official Website | <https://rea.tools/> |
| Installation & Agent Setup | <https://github.com/morluto/rea/blob/main/docs/installation.md> |
| Your First REA Investigation | <https://rea.tools/first-investigation/> |
| REA Guides | <https://rea.tools/guides/> |
| Guided MCP Prompts | <https://github.com/morluto/rea/blob/main/docs/mcp-prompts.md> |

### WATCH & FOLLOW ALONG

| Label | URL |
| --- | --- |
| How To Use REA To Clone Any Software In Minutes | <https://www.youtube.com/watch?v=FnB9tHKBJXQ> |
| REA + Pi Coding Agent Tutorial | <https://www.datacamp.com/tutorial/reverse-engineer-anything-rea-tutorial> |
| Ghidra Tutorial for Beginners | <https://www.youtube.com/watch?v=OFAxXXcLXbc> |
| Frida for Android Reverse Engineering | <https://www.youtube.com/watch?v=GHh9P-Dyq1w> |
| pwn.college: Reverse Engineering | <https://pwn.college/intro-re-pwn~5933fc84/reversing/> |
| Malware Unicorn RE101 | <https://malwareunicorn.org/workshops/re101#0> |

### REAL REA INVESTIGATIONS

| Label | URL |
| --- | --- |
| Notes Export | <https://rea.tools/first-investigation/> |
| Notion Clipboard | <https://rea.tools/showcase/notion/> |
| DX-Ball Reconstruction | <https://rea.tools/showcase/dx-ball/> |
| Aegis APK | <https://rea.tools/showcase/aegis/> |
| TH04 Bullet Patterns | <https://rea.tools/showcase/th04/> |
| (bonus, tidak di postingan) CTF showcase | <https://rea.tools/showcase/ctf/> |

### GITHUB REPOS

| Label | URL |
| --- | --- |
| REA | <https://github.com/morluto/rea> |
| Awesome Reverse Engineering | <https://github.com/morluto/awesome-reverse-engineering> |
| REA Gems | <https://github.com/sqwu/rea-gems> |
| Awesome Reverse-Engineered | <https://github.com/alexgaoth/awesome-reverse-engineered> |
| Ghidra | <https://github.com/NationalSecurityAgency/ghidra> |
| JADX | <https://github.com/skylot/jadx> |
| Frida | <https://github.com/frida/frida> |
| ILSpy | <https://github.com/icsharpcode/ILSpy> |
| x64dbg | <https://github.com/x64dbg/x64dbg> |

### BOOKS

| Label | URL | Catatan |
| --- | --- | --- |
| The Ghidra Book, 2nd Edition | <https://nostarch.com/ghidra-book-2e> | No Starch, berbayar |
| Reverse Engineering for Beginners | <https://go.yurichev.com/> | gratis (Dennis Yurichev); `beginners.re` = alias halaman yang sama |
| Practical Binary Analysis | <https://nostarch.com/binaryanalysis> | No Starch, berbayar |
| Practical Malware Analysis | <https://nostarch.com/malware> | No Starch, berbayar |
| The Android Malware Handbook | <https://nostarch.com/androidmalwarehandbook> | No Starch, berbayar |
| Reversing: Secrets of Reverse Engineering | shortlink → <https://www.wiley.com/en-sg> (locale Anda) | **mati**: halaman produk Wiley hilang, mendarat di beranda penerbit. ISBN `978-0764574818` |

### RESEARCH PAPERS

| Label | URL |
| --- | --- |
| LLM4Decompile | <https://arxiv.org/abs/2403.05286> |
| AutoDecompiler | <https://arxiv.org/abs/2606.16162> |
| SALT4Decompile | <https://arxiv.org/abs/2509.14646> (judul v2: *ALT4Decompile*) |
| Decomperson | <https://www.usenix.org/conference/usenixsecurity22/presentation/burk> |
| DIRTY | <https://www.usenix.org/system/files/sec22-chen-qibin.pdf> |
| Automatically Attacking Software RE Agents | <https://arxiv.org/abs/2605.30667> |
| Does Reverse Engineering Need a Bigger Model? | <https://rea.tools/blog/reverse-engineering-models/> |

### FREE COURSES & PRACTICE

| Label | URL |
| --- | --- |
| OpenSecurityTraining2: x86-64 Assembly | <https://p.ost2.fyi/courses/course-v1:OpenSecurityTraining2+Arch1001_x86-64_Asm+2021_v1/about> |
| pwn.college: Reverse Engineering | <https://pwn.college/intro-re-pwn~5933fc84/reversing/> |
| pwn.college: Reversing Hell | <https://pwn.college/reversing-hell/> |
| Malware Unicorn RE101 | <https://malwareunicorn.org/workshops/re101#0> |
| Nightmare | <https://github.com/guyinatuxedo/nightmare> |
| RPISEC Modern Binary Exploitation | <https://github.com/RPISEC/MBE> |
| OWASP Mobile Application Security | <https://mas.owasp.org/> |

### Sinkronisasi dengan daftar kanonik (paste user, 2026-10-29)

Daftar di atas sudah dicocokkan dengan URL yang Anda paste. Empat selisih, semua
sudah diperiksa ulang:

| Item | Hasil resolve awal | Daftar Anda | Status |
| --- | --- | --- | --- |
| Reverse Engineering for Beginners | `beginners.re` | `go.yurichev.com` | **sama** — halaman identik (judul & `content-length` 6256, Apache/2.4.52). Sekarang `go.yurichev.com` jadi URL utama, `beginners.re` alias |
| Reversing: Secrets of RE | `wiley.com/en-us` | `wiley.com/en-sg` | **sama-sama beranda Wiley**, beda locale → tetap `mati` |
| Malware Unicorn RE101 | tanpa anchor | `…/re101#0` | anchor slide pertama, sudah dipakai |
| GITHUB REPOS baris 2 | `morluto/awesome-reverse-engineering` | `github.com/morluto/rea` (dobel) | **belum pasti** — kemungkinan artefak display URL X saat copy; yang ter-resolve tetap `awesome-reverse-engineering` (judulnya cocok), dan keduanya dicatat |

Tabel per-baris lengkap dengan kode `t.co`, status verifikasi, dan catatan
metode ada di
[`.agents/skills/rea-roadmap/references/resources.md`](.agents/skills/rea-roadmap/references/resources.md).

---

## 2b. Alur kerja terpadu (`rea-workflow`)

Semua skill di atas tidak lagi dipakai sendiri-sendiri. `rea-workflow`
menggabungkannya jadi **satu loop 8 fase dengan gate**: fase tidak boleh maju
sebelum gate-nya lulus, dan gate hanya lulus kalau ada bukti.

```
F0 Intake & scope ──► F1 Environment ──► F2 Route ──► F3 Evidence
        ▲                                                  │
        │                                                  ▼
      F7 Catat & tutup ◄── F6 Deliverable ◄── F5 Verifikasi ◄── F4 Interpretasi
```

| Fase | Keluaran | Gate |
| --- | --- | --- |
| F0 | Pertanyaan satu kalimat + target + batas izin | Pertanyaan bisa dijawab; target konkret |
| F1 | `check_readiness.sh` + tool yang dipakai | Tool tersedia, atau klaim diturunkan |
| F2 | Rute + alasan + alternatif ditolak | Rute ada di matriks target |
| F3 | Evidence E1, E2, … | Tiap butir punya sumber |
| F4 | Fakta vs inferensi vs unknown | Tidak ada inferensi tanpa rujukan E |
| F5 | Hasil uji silang | Klaim utama punya status verifikasi |
| F6 | Jawaban 4 bagian | Tiap klaim punya penopang |
| F7 | Unknown + next step + arsip | Unknown tercatat |

Peta delegasi (siapa dipanggil di fase mana):

| Fase | Skill |
| --- | --- |
| F0, F1, F7 | `rea-roadmap` (antrean 7 tahap, readiness, resource) |
| F2–F6 | `reverse-engineer-anything` (routing resmi, tool, Evidence) |
| F3 (bila target tertutup) | `find-reverse-engineered` |
| F6 (deliverable = tool / notes) | `rea-tool-design` / `rea-changelog-update` |
| atas permintaan | `rea-analysis-optimization`, `rea-ci-tests-audit` |

Mesin state sesi (data di `/tmp/rea-workflow/`, bukan di Git):

```bash
S=.agents/skills/rea-workflow/scripts/session.sh
bash $S init "apk aegis login" --target /path/app.apk
bash $S status
bash $S gate F2 --pass "APK -> inspect_android_package"
bash $S advance          # ditolak kalau gate fase ini belum PASS
bash $S log "E1: classes2.dex -> LoginActivity"
bash $S unknown "validasi native? cek lib*.so"
bash $S report
```

Aturan repo yang mengikat semua agent ada di [`AGENTS.md`](AGENTS.md).

---


## 2c. Toolchain studio — 20 repo dari postingan @0xDeniAi

Postingan kedua ([@0xDeniAi](https://x.com/0xDeniAi/status/2114847015091794206))
menyusun 20 repo jadi "studio RE" dalam 5 grup. Semuanya sudah di-resolve dan
dimasukkan ke alur kerja:

| Grup | Repo | Dipakai di fase |
| --- | --- | --- |
| 01 analysis core | REA, Ghidra, GhidraMCP, ida-pro-mcp | F3 (static evidence) |
| 02 mobile & apps | jadx, Apktool, Frida, ILSpy | F3/F6 (tahap 4) |
| 03 binary & low-level | radare2, x64dbg, ImHex, angr | F3 (tahap 3/6) |
| 04 network & runtime | mitmproxy, dnSpy, rizin, raddebugger | F3 (capture/runtime) |
| 05 rebuild & verify | awesome-ai-reverse-engineering, awesome-reverse-engineering, *REA workflows*, *clean-room loop* | F5/F6/F7 |

Pipeline yang disebut postingan itu sekarang jadi **mode rebuild** resmi di F5–F7:

```
binary → REA → SPEC.md → rebuild → oracle → retry
```

Dipetakan ke fase: binary = F0–F2, REA = F3, SPEC.md = F4 (+`templates/spec.md`),
rebuild = F6, oracle = F5 (`verify_reconstruction` / uji hitung / diff),
retry = F7→F3 **hanya untuk selisih** yang ditemukan.

Enam prompt REA resmi juga dipasang ke fase:

| Prompt | Fase |
| --- | --- |
| `investigate_feature` | F3 |
| `compare_application_versions` | F3/F5 |
| `verify_reconstruction` | F5 (oracle) |
| `trace_crash` | F3 |
| `audit_residual_unknowns` | F7 |
| `prepare_bounded_process_capture` | F3 runtime (rancang dulu, eksekusi butuh izin) |

Query offline:

```bash
bash .agents/skills/rea-workflow/scripts/session.sh tools --list
bash .agents/skills/rea-workflow/scripts/session.sh tools --group mobile
bash .agents/skills/rea-workflow/scripts/session.sh tools --stage 6
```

### Selisih klaim postingan vs fakta

| Klaim | Temuan | Tindakan |
| --- | --- | --- |
| "awesome-ai-reverse-engineering: 122 repos" | README repo (2026-10-29) menulis **118 repos** (74 MCP + 17 mobile + 4 web + 19 skills + 4 kasus) | pakai 118, selisih dicatat |
| "dnSpy" | tautan → fork aktif `dnSpyEx/dnSpy`; repo asli `dnSpy/dnSpy` **archived** (29.7k★) | rekomendasikan fork, sebut status asli |
| "REA workflows" & "clean-room loop" | tidak ada tautan di postingan | dipetakan ke `mcp-prompts.md` + pipeline di atas |
| 16 tautan `t.co` | sebagian terpotong (`…`), redirect 404 | nama repo penuh + lisensi + star dikonfirmasi via GitHub API |

Detail per-repo (star, lisensi, peran, catatan): 
[`.agents/skills/rea-workflow/references/re-toolchain.md`](.agents/skills/rea-workflow/references/re-toolchain.md)
dan versi mesin `re-toolchain.json` (18 entri bertautan).

---

## 3. Antrean tahap (isi `rea-roadmap`)

```
Tahap 1 Setup → 2 Notes Export → 3 CTF binary → 4 Aegis APK
      → 5 Notion / DX-Ball / TH04 → 6 Ghidra + assembly → 7 Paper + tooling
```

Tiap tahap punya **tujuan, resource kanonik, prompt siap tempel, kriteria keluar,
dan jebakan** — detail di
[`learning-path.md`](.agents/skills/rea-roadmap/references/learning-path.md).

Urutan kerjanya sudah dipindahkan ke loop 8 fase di `rea-workflow` (bagian 2b).
Ringkasnya: F0 nyatakan pertanyaan → F1 cek alat → F2 pilih rute → F3 ambil
Evidence → F4 pisahkan fakta/dugaan → F5 uji silang → F6 jawab dengan sitasi →
F7 catat unknown. Roadmap hanya menentukan **target** sesi berikutnya.

### Hasil F1 (environment) di sandbox ini (2026-10-29)

```
OK     node                   v22.22.3
OK     npx                    10.9.8
TIDAK  rea CLI                belum terpasang
WARN   state ~/.rea           belum ada — setup belum pernah dijalankan
WARN   ghidra / jadx / java / frida / tshark   tidak terdeteksi
OK     python3                Python 3.11.2
```

Artinya: **posisi saat ini = Tahap 1 (setup) yang belum dijalankan**, dan
`ghidra` belum ada sehingga Tahap 3+ belum bisa dieksekusi di sini. State sesi
percakapan ini juga sudah dibuat:

```
sesi   : sesi-percakapan  (alur kerja REA percakapan ini)
target : (belum ada)
F0     FAIL   target artefak nyata belum diberikan
F1     PASS   readiness 2026-10-29 (rea CLI tidak ada -> klaim dibatasi)
langkah: gate F0 lalu advance
```

Artinya jujur: alur kerja aktif, tapi **F0 belum bisa lulus karena belum ada
target nyata**. Kirim satu artefak (APK/binary/HAR/bundle JS) dan F0 langsung
lulus. Semua skill siap sebagai metodologi; engine (Ghidra/JADX/Frida/MCP `rea`)
harus dipasang di mesin target — bisa juga saya jalankan
`npx rea-agents@latest setup` di sini **setelah Anda menyetujui**, meski MCP yang
terpasang tidak otomatis masuk ke sesi ini.

---

## 4. Cara mengaktifkan

**a. Sudah aktif dari repo (tanpa install)**
Semua skill ada di `.agents/skills/`; agent yang membaca folder itu langsung
menemukannya.

**b. Instalasi resmi (butuh Node, mendaftarkan MCP `rea`)**

```bash
npx rea-agents@latest setup     # rea-agents 6.8.0 saat verifikasi
rea doctor                      # cek setelah restart agent
```

**c. Plugin Claude Code / Codex**

```bash
/plugin marketplace add morluto/rea
/plugin install rea@rea
```

Untuk skill pencari tool: plugin `alexgaoth/awesome-reverse-engineered`
(`plugin/skills/find-reverse-engineered`), bisa dipakai langsung dengan
`python3 .agents/skills/find-reverse-engineered/scripts/re_index.py search tuya local`.

Ingat: **skill = instruksi, bukan engine.** Menyalin skill tidak memasang Ghidra,
JADX, Frida, Kuna, atau Node.

---

## 5. Prompt pemicu

| Tujuan | Prompt |
| --- | --- |
| Jalankan alur kerja | "Pakai `rea-workflow`: mulai sesi baru untuk `<target>`, tunjukkan fase dan gate-nya." |
| Bangun ulang fitur | "Mode rebuild: buat SPEC.md dari Evidence, lalu uji pakai oracle." |
| Pilih tool | "Tool apa yang dipakai untuk `<jenis target>`? Cek `session.sh tools`." |
| Mulai dari nol | "Jalankan roadmap REA dari awal, cek environment dulu." |
| Cek posisi | "Saya di tahap berapa? Jalankan check_readiness lalu simpulkan." |
| Rute target | "Target saya APK `<nama>`. Rute roadmap + tool-nya apa?" |
| Naik tahap | "Buktikan kriteria selesai Tahap 2, lalu lanjut ke Tahap 3." |
| Cari resource | "Resource roadmap untuk topik `<topik>` (paper/buku/kursus) yang mana?" |
| Cari tool | "Pakai `find-reverse-engineered`: cari tool open-source untuk `<produk>`." |
| Investigasi mendalam | "Pakai `reverse-engineer-anything` pada `<path>`; sertakan Evidence dan batasannya." |

---

## 6. Struktur file

```
.
├── AGENTS.md                                ← aturan kerja untuk semua agent
├── SKILLS.md                                ← dokumen ini
└── .agents/
    └── skills/
        ├── README.md                        ← atribusi & daftar skill
        ├── rea-workflow/                    ← penggabung, pintu masuk
        │   ├── SKILL.md
        │   ├── references/{phases,target-routing,evidence-contract,skill-map,re-toolchain}.md
        │   ├── references/re-toolchain.json
        │   ├── templates/{finding,spec}.md
        │   └── scripts/session.sh
        ├── rea-roadmap/                     ← BARU: alur kerja dari 46 link
        │   ├── SKILL.md
        │   ├── references/{resources.md,resources.json,learning-path,installation,mcp-prompts,source-verification}
        │   └── scripts/{check_readiness.sh,find_resource.sh}
        ├── find-reverse-engineered/         ← dari awesome-reverse-engineered (MIT)
        │   ├── SKILL.md, LICENSE
        │   └── scripts/re_index.py
        ├── reverse-engineer-anything/       ← dari morluto/rea
        │   ├── SKILL.md + references/ (7 file)
        ├── rea-analysis-optimization/       SKILL.md + references/ + agents/
        ├── rea-ci-tests-audit/              SKILL.md + references/ + agents/
        ├── rea-tool-design/                 SKILL.md
        └── rea-changelog-update/            SKILL.md
```

Sinkron ulang skill upstream:

```bash
git clone --depth 1 https://github.com/morluto/rea /tmp/rea
rsync -a /tmp/rea/.agents/skills/ .agents/skills/       # README.md lokal aman
git clone --depth 1 https://github.com/alexgaoth/awesome-reverse-engineered /tmp/are
rsync -a /tmp/are/plugin/skills/find-reverse-engineered/ .agents/skills/find-reverse-engineered/
```

---

## Bagian B — gerak, 3D, suara, encode (@0xMovez, 20 repo)

Sumber: [@0xMovez — "These 20 GitHub repos will turn your Fable 5.2 into a premier motion
studio"](https://x.com/0xMovez/status/2121312707588583455) (13 Nov 2026), 5.162 suka.
Semua 20 tautan `t.co` di-resolve 29 Okt 2026; tiap repo diverifikasi lewat GitHub API
(bintang, lisensi, commit, tanggal push). Urutan yang dipakai postingan itu sendiri:
**skill → scene → motion → sound → final cut** — itu juga urutan skill `motion-studio`.

### Tabel 20 item → skill

| # | Item di postingan | Repo (terverifikasi) | ★ | Lisensi | Skill di repo ini | Cara dibuat |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | `/motion-design-skill` | `LottieFiles/motion-design-skill` | 3.301 | MIT | [`motion-design`](.agents/skills/motion-design/SKILL.md) | **salinan verbatim** (`skills/motion-design/`, commit `2e1f3c052dd7`) |
| 02 | `ai-kit` | `motiondivision/ai-kit` | 123 | **tanpa LICENSE** | [`motion-ai-kit`](.agents/skills/motion-ai-kit/SKILL.md) | ditulis sendiri + tautan (tidak disalin) |
| 03 | Remotion Skills | `remotion-dev/skills` | 7.456 | **tanpa LICENSE** | [`remotion-skills`](.agents/skills/remotion-skills/SKILL.md) | indeks 13 skill, ditulis sendiri |
| 04 | `/hairline` | `lucasmarkes/hairline` | 3.995 | MIT | [`hairline-create`](.agents/skills/hairline-create/SKILL.md), [`hairline-adopt`](.agents/skills/hairline-adopt/SKILL.md) | **salinan verbatim** (`skills/`, commit `034f4bf9902c`) |
| 05 | `/anatomy` | `wheresryan22/anatomy` | 27.987 | MIT | [`anatomy`](.agents/skills/anatomy/SKILL.md) | **salinan verbatim** (SKILL + references + kit, commit `1482e8469b0a`) |
| 06 | `/anatomy-reveal` | `annnguyentt/anatomy-reveal-skill` | 117 | MIT | [`anatomy-reveal`](.agents/skills/anatomy-reveal/SKILL.md) | **salinan verbatim** (SKILL + references + template .mjs, commit `dd01e1c04559`) |
| 07 | `/blender-agents` | `scenario-labs/blender-plugin` | 1.046 | GPL-3.0-or-later | [`blender-mcp`](.agents/skills/blender-mcp/SKILL.md) | ditulis sendiri (upstream tak punya skill 3D) |
| 08 | Three.js | `mrdoob/three.js` | 118.797 | MIT | [`threejs`](.agents/skills/threejs/SKILL.md) | ditulis sendiri |
| 09 | react-three-rapier | `pmndrs/react-three-rapier` | 1.675 | MIT | [`rapier-physics`](.agents/skills/rapier-physics/SKILL.md) | ditulis sendiri |
| 10 | react-postprocessing | `pmndrs/react-postprocessing` | 1.651 | MIT | [`postprocessing`](.agents/skills/postprocessing/SKILL.md) | ditulis sendiri |
| 11 | three.quarks | `Alchemist0823/three.quarks` | 1.227 | MIT | [`quarks-vfx`](.agents/skills/quarks-vfx/SKILL.md) | ditulis sendiri |
| 12 | Tweakpane | `cocopon/tweakpane` | 4.703 | MIT | [`tweakpane`](.agents/skills/tweakpane/SKILL.md) | ditulis sendiri |
| 13 | GSAP | `greensock/GSAP` | 30.867 | GreenSock (bukan MIT) | [`gsap`](.agents/skills/gsap/SKILL.md) | ditulis sendiri |
| 14 | Remotion | `remotion-dev/remotion` | 73.999 | Remotion License (bukan MIT) | [`remotion`](.agents/skills/remotion/SKILL.md) | ditulis sendiri |
| 15 | Manim | `ManimCommunity/manim` | 42.657 | MIT | [`manim`](.agents/skills/manim/SKILL.md) | ditulis sendiri |
| 16 | Lottie | `airbnb/lottie-web` | 32.497 | MIT | [`lottie`](.agents/skills/lottie/SKILL.md) | ditulis sendiri |
| 17 | Openverse API | `WordPress/openverse` | 688 | MIT | [`openverse-audio`](.agents/skills/openverse-audio/SKILL.md) | ditulis sendiri |
| 18 | librosa | `librosa/librosa` | 9.005 | ISC | [`librosa-beat`](.agents/skills/librosa-beat/SKILL.md) | ditulis sendiri |
| 19 | WhisperX | `m-bain/whisperX` | 25.445 | BSD-2-Clause | [`whisperx-captions`](.agents/skills/whisperx-captions/SKILL.md) | ditulis sendiri |
| 20 | FFmpeg | `FFmpeg/FFmpeg` | 67.522 | LGPL/GPL | [`ffmpeg-encode`](.agents/skills/ffmpeg-encode/SKILL.md) | ditulis sendiri |

Pintu masuk: [`motion-studio`](.agents/skills/motion-studio/SKILL.md) — peta tahap → skill,
aturan tanpa CDN, dan urutan 6 langkah dari spesifikasi sampai encode.

### Bagian B, yang perlu diucapkan terang-terangan

1. **Hanya 5 skill yang disalin verbatim** — semuanya berlisensi MIT dan berkas `LICENSE`
   ikut disalin. Sepuluh entri lain adalah **panduan yang ditulis di repo ini**: cara pasang,
   API inti, dan jebakan, dengan commit upstream dicatat di kepala setiap `SKILL.md`.
2. **`ai-kit` dan `remotion-dev/skills` tidak punya berkas lisensi.** Menyalin isinya berarti
   mengambil hak yang tidak diberikan, jadi keduanya hanya ditautkan dan diringkas.
3. **Tujuh item di bawah ambang 3.000 bintang** yang biasa dipakai repo ini — `react-three-rapier`
   (1.675), `react-postprocessing` (1.651), `three.quarks` (1.227), `Openverse` (688),
   `blender-plugin` (1.046), `anatomy-reveal` (117), `ai-kit` (123). Tetap dimasukkan karena
   Anda meminta **semua** item di postingan; kolom ★ dibuat supaya kelihatan mana yang di bawah
   ambang. Kalau mau dibersihkan, hapus barisnya dari tabel dan foldernya dari `.agents/skills/`.
4. **Postingan menyebut "Openverse API 5,2 juta+"** — angka itu klaim postingan, bukan hasil
   ukur repo ini. Yang bisa saya pastikan: endpoint `api.openverse.org/v1/audio/` hidup dan
   memberi hasil dengan filter lisensi.

### Bagian B, yang belum pernah dijalankan di sini

Sandbox ini **tidak punya** Blender, GPU, FFmpeg, maupun pustaka Python/Node di atas — jadi
**tidak satu pun** dari 20 item sudah dijalankan di sini. Yang dikerjakan: 20 tautan
di-resolve, tiap repo diverifikasi lewat GitHub API (bintang, lisensi, commit, tanggal push),
lima skill MIT disalin verbatim beserta `LICENSE`, dan enam belas item lain ditulis dari
dokumentasi repo pada commit yang dicatat.

Batas per skill juga ditulis di dalam `SKILL.md` masing-masing, khususnya `blender-mcp`,
`rapier-physics`, `postprocessing`, `quarks-vfx`, `remotion`, `remotion-skills`,
`whisperx-captions`, dan `manim` — semuanya **belum diuji jalan** di mesin ini.
Kalau dipasang di mesin Anda, uji satu perintah kecil dulu sebelum satu proyek penuh.
