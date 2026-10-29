# SKILLS.md — Reverse Engineering Agent Skills (dari postingan @cabbitar)

Dokumen ini adalah hasil menyalin **seluruh skill GitHub** yang ada di postingan
[@cabbitar — "STOP WASTING HOURS TRYING TO LEARN REA"](https://x.com/cabbitar/status/2115467413953056921),
lalu menerapkannya sebagai cara kerja di percakapan ini.

| Item | Nilai |
| --- | --- |
| Sumber skill | <https://github.com/morluto/rea> → folder `.agents/skills/` |
| Commit yang disalin | `bf115be2cd900724a5bbd59a5cefc7af1dc2576f` (branch `main`) |
| Tanggal salin | 2026-10-29 |
| Lokasi di repo ini | [`.agents/skills/`](.agents/skills/) |
| Jumlah skill | 5 skill, 17 file, ~220 KB |
| Metode | `cp -r` verbatim (tidak ada isi yang diubah) |

---

## 1. Skill yang sudah dicopy

| # | Skill | Fungsi inti | File |
| --- | --- | --- | --- |
| 1 | **reverse-engineer-anything** (v55) | Skill utama REA: menentukan rute tool yang benar untuk tiap jenis target, mengumpulkan *Evidence*, lalu menjawab pertanyaan analis — dari APK, binary native, .NET, Electron/JS, firmware, sampai capture jaringan. | [`SKILL.md`](.agents/skills/reverse-engineer-anything/SKILL.md) + 7 file `references/` (android, javascript, native & artifact, runtime observation, environment, evidence workflow, connection & recovery) |
| 2 | **rea-analysis-optimization** | Mencari sumber pekerjaan yang tidak perlu di provider/workflow analisis, mengubahnya di tempat yang benar, dan memverifikasi investigasi tetap setara. Termasuk studi kasus Kuna. | [`SKILL.md`](.agents/skills/rea-analysis-optimization/SKILL.md) + `references/kuna-case-study.md` |
| 3 | **rea-ci-tests-audit** | Audit CI & test suite: mana check yang masih menangkap regresi nyata, mana biaya yang bisa dipotong, mendeteksi false pass dan fixture drift. | [`SKILL.md`](.agents/skills/rea-ci-tests-audit/SKILL.md) + `references/measurement-and-ci.md` |
| 4 | **rea-tool-design** | Merancang/mengubah tool investigasi: batas tool, kontrak CLI/MCP, capability provider, semantik Evidence. | [`SKILL.md`](.agents/skills/rea-tool-design/SKILL.md) |
| 5 | **rea-changelog-update** | Menyusun changelog / release notes dari Git history yang dipin, dengan atribusi kontributor yang terverifikasi. | [`SKILL.md`](.agents/skills/rea-changelog-update/SKILL.md) |

Semua skill memakai format `SKILL.md` berisi front-matter `name` + `description`:
deskripsi itu yang dibaca agent untuk memutuskan *kapan* skill diaktifkan,
sedangkan isi lengkapnya baru dimuat saat relevan (progressive disclosure).

---

## 2. GitHub & resource lain di postingan yang sama

**Repo/GitHub yang disebut** (yang bisa diverifikasi):

| Nama di postingan | Repo | Keterangan |
| --- | --- | --- |
| REA | [morluto/rea](https://github.com/morluto/rea) | Sumber 5 skill di atas; `npx rea-agents@latest setup` |
| Awesome Reverse Engineering | [morluto/awesome-reverse-engineering](https://github.com/morluto/awesome-reverse-engineering) | Kurasi tool & materi RE (binary, app, firmware, format, protokol) — tidak memuat agent skill |
| REA Gems | [sqwu/rea-gems](https://github.com/sqwu/rea-gems) | Galeri kasus RE nyata yang dibangun dengan REA, auto-update harian — bukan skill |
| Ghidra | [NationalSecurityAgency/ghidra](https://github.com/NationalSecurityAgency/ghidra) | SRE framework (decompiler) |
| JADX | [skylot/jadx](https://github.com/skylot/jadx) | Dex → Java decompiler |
| Frida | [frida/frida](https://github.com/frida/frida) | Dynamic instrumentation |
| ILSpy | [icsharpcode/ILSpy](https://github.com/icsharpcode/ILSpy) | .NET decompiler |
| x64dbg | [x64dbg/x64dbg](https://github.com/x64dbg/x64dbg) | Debugger user-mode Windows |

> Repo "Awesome Reverse-Engineered" dan beberapa link lain di postingan memakai
> shortlink `t.co` yang tidak bisa di-resolve dari sandbox ini, jadi tidak saya
> cantumkan URL-nya supaya tidak salah tebak.

**Buku:** The Ghidra Book (2nd ed.), Reverse Engineering for Beginners, Practical
Binary Analysis, Practical Malware Analysis, The Android Malware Handbook,
Reversing: Secrets of Reverse Engineering.

**Paper:** LLM4Decompile, AutoDecompiler, SALT4Decompile, Decomperson, DIRTY,
"Automatically Attacking Software RE Agents", "Does Reverse Engineering Need a
Bigger Model?".

**Kursus gratis:** OpenSecurityTraining2 x86-64 Assembly, reversing.zone
(Reverse Engineering / Reversing Hell), Malware Unicorn RE101, Nightmare, RPISEC
Modern Binary Exploitation, OWASP MAS.

**Urutan belajar yang direkomendasikan postingan:**
Install REA → Notes Export → Notion → CTF binary → Aegis APK → DX-Ball → baru
Ghidra, assembly, dan paper-paper.

---

## 3. Cara mengaktifkan skill

Tiga jalur, pilih satu:

**a. Sudah aktif di repo ini (tanpa install apa pun)**
Skill ada di `.agents/skills/`. Agent yang membaca `.agents/skills/` (Codex-style,
Claude Code, dsb.) akan menemukannya otomatis. Saya di percakapan ini juga sudah
membaca dan memakai isinya.

**b. Install resmi via npm (butuh Node.js, mengikat MCP server `rea`)**

```bash
npx rea-agents@latest setup     # daftarkan server + pasang skill
rea doctor                      # cek kesehatan instalasi
```

**c. Plugin Claude Code / Codex**

```bash
# Claude Code
/plugin marketplace add morluto/rea
/plugin install rea@rea

# Codex
codex plugin install morluto/rea
```

Ingat: **skill = instruksi, bukan engine.** Meng-copy skill tidak otomatis
memasang Ghidra/JADX/Frida/Kuna atau mendaftarkan MCP `rea`. Jadi di sandbox ini
skill-nya aktif sebagai metodologi, tapi tool `rea` (open_binary,
analyze_function, inspect_android_package, dst.) tidak tersedia untuk dieksekusi.

---

## 4. Aturan yang saya terapkan mulai sekarang di percakapan ini

Diambil langsung dari isi skill (terutama `reverse-engineer-anything`):

1. **Evidence-first, no hand-waving.** Setiap klaim tentang artefak harus punya
   jejak: digest/byte range, path, tool, dan batasannya. Kalau belum ada bukti,
   saya tulis "belum diketahui", bukan menebak.
2. **Route target dulu, baru pilih tool.** Jenis target menentukan jalur:
   ASAR/JS tree → `analyze_javascript_application`; APK → `inspect_android_package`;
   archive/PyInstaller → `open_binary` + `inspect_artifact`; native → `open_binary`;
   capture HAR/SAZ/qlog → `inspect_web_network_capture`; packet capture → TShark
   path; firmware → Binwalk/Unblob; WASM → `inspect_wasm_artifact`; dsb.
3. **Summary-first.** Mulai dari `detail: "summary"`, baru page bagian tertentu via
   `inspect_analysis_view`. Jangan minta hasil lengkap kalau tidak perlu.
4. **Tidak mengulang call yang identik.** Kalau gagal, penyebabnya harus berubah
   atau blocker-nya harus sudah dibereskan dulu.
5. **Batas otorisasi dipertahankan.** Investigasi ≠ izin mengubah/menjalankan
   target. Menjalankan target, menulis output, publish, merge, atau install
   software baru selalu butuh izin eksplisit.
6. **Investigasi vs implementasi dipisah.** "Analisa dulu" artinya tidak ada edit
   kode; "perbaiki" artinya scope tetap dijaga.
7. **Recovery bertahap.** MCP timeout ≠ pekerjaan berhenti; retry sekali untuk
   call yang aman diulang, lalu lapor dan minta restart client. `rea doctor` hanya
   untuk registrasi milik `setup`, bukan install plugin.
8. **Build vs source.** Untuk repo sumber yang lengkap, pakai tool repo biasa —
   jangan pura-pura menjalankan RE atas binary yang tidak ada.
9. **Skill optimasi & audit tidak dipakai untuk kerja rutin.** Butuh pertanyaan
   performa/regresi yang konkret dulu, bukan sekadar "biar cepat".

---

## 5. Contoh prompt pemicu

| Tujuan | Prompt |
| --- | --- |
| Investigasi app/binary | "Pakai `reverse-engineer-anything`: jelaskan bagaimana fitur export di `<path/app.apk>` bekerja, lampirkan Evidence dan bagian yang belum diketahui." |
| Bandingkan versi | "Bandingkan `app-v1.apk` vs `app-v2.apk` di jalur auth, tunjukkan fungsi yang berubah." |
| Capture jaringan | "Analisa `capture.har` ini: endpoint apa saja, field mana yang dikirim, dan apa yang tidak bisa disimpulkan." |
| Audit CI | "Pakai `rea-ci-tests-audit`: cek workflow mana yang false pass dan mana yang bisa dipangkas tanpa kehilangan proteksi." |
| Optimasi analisis | "Pakai `rea-analysis-optimization`: kenapa analisis JS tree ini lambat, dan di mana perbaikan paling murah?" |
| Desain tool | "Pakai `rea-tool-design`: rancang tool untuk membaca signature APK beserta semantik Evidence-nya." |
| Changelog | "Pakai `rea-changelog-update`: susun release notes dari tag `rea-agents-X` sampai SHA Y." |

---

## 6. Struktur file

```
.
├── SKILLS.md                          ← dokumen ini (index + cara pakai)
└── .agents/
    └── skills/                        ← salinan verbatim dari morluto/rea
        ├── README.md                  ← catatan sumber & atribusi
        ├── reverse-engineer-anything/ SKILL.md + references/ (7 file)
        ├── rea-analysis-optimization/ SKILL.md + references/ + agents/
        ├── rea-ci-tests-audit/        SKILL.md + references/ + agents/
        ├── rea-tool-design/           SKILL.md
        └── rea-changelog-update/      SKILL.md
```

Untuk sinkron ulang di masa depan:

```bash
git clone --depth 1 https://github.com/morluto/rea /tmp/rea
rsync -a /tmp/rea/.agents/skills/ .agents/skills/   # README.md lokal tetap aman
```
