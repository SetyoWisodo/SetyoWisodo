# SKILLS.md — REA: semua link postingan @cabbitar, sudah jadi skill & alur kerja

Sumber: [@cabbitar — "STOP WASTING HOURS TRYING TO LEARN REA"](https://x.com/cabbitar/status/2115467413953056921) (2026-10-28).

| Item | Nilai |
| --- | --- |
| Link di postingan | 46 baris → **38 URL unik**, 37 terverifikasi, 1 mati |
| Skill tersalin/dibuat | **8 skill** — 5 dari `morluto/rea`, 1 finder (MIT), 2 disusun di repo ini |
| Pintu masuk | [`rea-workflow`](.agents/skills/rea-workflow/SKILL.md) — satu loop 8 fase |
| Lokasi | [`.agents/skills/`](.agents/skills/) |
| Metode | `cp -r` verbatim untuk skill upstream; `rea-roadmap` ditulis dari hasil resolusi link |
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

Front-matter `name` + `description` tiap skill adalah pemicunya: agent memilih
skill dari deskripsi itu, isi lengkap baru dimuat saat relevan.

---

## 2. Semua link postingan (sudah di-resolve dari `t.co`)

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
        ├── rea-workflow/                    ← BARU: penggabung, pintu masuk
        │   ├── SKILL.md
        │   ├── references/{phases,target-routing,evidence-contract,skill-map}.md
        │   ├── templates/finding.md
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
