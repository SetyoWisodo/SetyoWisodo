# SKILLS.md — REA: semua link postingan @cabbitar, sudah jadi skill & alur kerja

Sumber: [@cabbitar — "STOP WASTING HOURS TRYING TO LEARN REA"](https://x.com/cabbitar/status/2115467413953056921) (2026-10-28).

| Item | Nilai |
| --- | --- |
| Link di postingan | 46 baris → **38 URL unik**, 37 terverifikasi, 1 mati |
| Skill tersalin/dibuat | **7 skill** (18 file REA + 1 skill roadmap + 1 skill finder) |
| Lokasi | [`.agents/skills/`](.agents/skills/) |
| Metode | `cp -r` verbatim untuk skill upstream; `rea-roadmap` ditulis dari hasil resolusi link |
| Tanggal verifikasi link | 2026-10-29 |

---

## 1. Skill yang aktif di repo ini

| # | Skill | Asal | Fungsi |
| --- | --- | --- | --- |
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

## 3. Alur kerja yang dijalankan (isi skill `rea-roadmap`)

```
Tahap 1 Setup → 2 Notes Export → 3 CTF binary → 4 Aegis APK
      → 5 Notion / DX-Ball / TH04 → 6 Ghidra + assembly → 7 Paper + tooling
```

Tiap tahap punya **tujuan, resource kanonik, prompt siap tempel, kriteria keluar,
dan jebakan** — detail di
[`learning-path.md`](.agents/skills/rea-roadmap/references/learning-path.md).

Cara kerjanya di percakapan ini:

| Langkah | Yang saya lakukan |
| --- | --- |
| 0. Tetapkan posisi | Jalankan `bash .agents/skills/rea-roadmap/scripts/check_readiness.sh` → tahu Node/`rea`/engine/target |
| 0b. Ambil resource | `bash …/scripts/find_resource.sh --stage 4` (atau `--category paper`) → URL terverifikasi, bukan dari ingatan |
| 1. Rute target | Klasifikasikan target lewat skill `reverse-engineer-anything` (APK? native? Electron? pcap?) |
| 2. Jalankan tahap | Ambil tahap aktif, beri prompt siap tempel, dampingi hasilnya |
| 3. Evidence dulu | Setiap klaim disertai path/digest/byte range/tool + daftar "belum diketahui" |
| 4. Uji kriteria | Naik tahap hanya kalau bukti keluar tahap ini ada |
| 5. Tutup | Sebut tahap sekarang + satu aksi berikutnya + resource yang dipakai |

### Hasil eksekusi Langkah 0 di sandbox ini (2026-10-29)

```
OK     node                   v22.22.3
OK     npx                    10.9.8
TIDAK  rea CLI                belum terpasang
WARN   state ~/.rea           belum ada — setup belum pernah dijalankan
WARN   ghidra / jadx / java / frida / tshark   tidak terdeteksi
OK     python3                Python 3.11.2
```

Artinya: **posisi saat ini = Tahap 1 (setup) yang belum dijalankan**, dan
`ghidra` belum ada sehingga Tahap 3+ belum bisa dieksekusi di sini. Skill
`rea-roadmap` siap sebagai metodologi; engine-nya harus dipasang di mesin Anda
(atau saya jalankan `npx rea-agents@latest setup` di sini **setelah Anda
menyetujui**, meski MCP yang terpasang tidak otomatis masuk ke sesi ini).

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
├── SKILLS.md                                ← dokumen ini
└── .agents/
    └── skills/
        ├── README.md                        ← atribusi & daftar skill
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
