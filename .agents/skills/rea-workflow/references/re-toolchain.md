# Toolchain studio — 20 repo dari postingan @0xDeniAi

Sumber: [x.com/0xDeniAi/status/2114847015091794206](https://x.com/0xDeniAi/status/2114847015091794206)
("REA creator just dropped 20 GitHub repos to build a reverse engineering
studio", 2026-10-26).

Semua tautan `t.co` di-resolve pada **2026-10-29**. Catatan metode: sebagian
tautan di postingan terpotong (`…`), sehingga redirect mendarat di URL yang juga
terpotong (mis. `github.com/LaurieWired/Gh`). Untuk kasus itu, repo dikonfirmasi
lewat GitHub API — nama lengkap, deskripsi, lisensi, dan jumlah star diambil dari
API, bukan dari tebakan.

## Peta 5 grup

### 01 · Analysis core

| Tool | Repo | ★ | Lisensi | Peran di alur kerja |
| --- | --- | --- | --- | --- |
| REA | <https://github.com/morluto/rea> | — | lihat upstream | MCP tunggal yang menyatukan semuanya; sumber 5 skill di repo ini |
| Ghidra | <https://github.com/NationalSecurityAgency/ghidra> | 95.7k | Apache-2.0 | Decompiler/disassembler gratis; provider native utama (F3) |
| GhidraMCP | <https://github.com/LaurieWired/GhidraMCP> | 11.6k | Apache-2.0 | Membuat agent bisa mengendalikan Ghidra lewat MCP |
| ida-pro-mcp | <https://github.com/mrexodia/ida-pro-mcp> | 13.2k | MIT | Menghubungkan agent ke IDA Pro (butuh lisensi IDA) |

### 02 · Mobile & apps

| Tool | Repo | ★ | Lisensi | Peran |
| --- | --- | --- | --- | --- |
| jadx | <https://github.com/skylot/jadx> | 51.4k | Apache-2.0 | Dex → Java; rute APK (F3, tahap 4) |
| Apktool | <https://github.com/iBotPeaches/Apktool> | 26.8k | Apache-2.0 | Bongkar/pasang ulang APK, termasuk resource (F6 rebuild) |
| Frida | <https://github.com/frida/frida> | 22.5k | wxWindows (LGPL-like) | Hook saat app berjalan; hanya dengan izin eksekusi (F3 runtime) |
| ILSpy | <https://github.com/icsharpcode/ILSpy> | 26.9k | MIT | Decompiler .NET (rute managed) |

### 03 · Binary & low-level

| Tool | Repo | ★ | Lisensi | Peran |
| --- | --- | --- | --- | --- |
| radare2 | <https://github.com/radareorg/radare2> | 25.2k | LGPL-3.0 (GitHub: NOASSERTION) | Framework RE di terminal; alternatif tanpa GUI |
| x64dbg | <https://github.com/x64dbg/x64dbg> | 50.1k | GPL-3.0 | Debugger Windows; pertanyaan runtime (F3 runtime) |
| ImHex | <https://github.com/WerWolv/ImHex> | — | lihat upstream | Hex editor + pattern language; bedah format file |
| angr | <https://github.com/angr/angr> | — | BSD-2-Clause | Symbolic execution; menjawab "input apa yang lolos" (F3 lanjut) |

### 04 · Network & runtime

| Tool | Repo | ★ | Lisensi | Peran |
| --- | --- | --- | --- | --- |
| mitmproxy | <https://github.com/mitmproxy/mitmproxy> | 46.5k | MIT | Intersepsi TLS/HTTP; menghasilkan capture → `inspect_web_network_capture` |
| dnSpy | <https://github.com/dnSpyEx/dnSpy> | — | GPL-3.0 | Debug + edit assembly .NET. **Tautan postingan menunjuk fork aktif `dnSpyEx`**, bukan `dnSpy/dnSpy` yang sudah **archived** |
| rizin | <https://github.com/rizinorg/rizin> | — | LGPL-3.0 | Fork radare2; CLI/kerangka RE |
| raddebugger | <https://github.com/EpicGames/raddebugger> | 8.7k | MIT | Debugger user-mode dari Epic Games |

### 05 · Rebuild & verify

| Tool | Repo | ★ | Lisensi | Peran |
| --- | --- | --- | --- | --- |
| awesome-ai-reverse-engineering | <https://github.com/zhuyansen/awesome-ai-reverse-engineering> | 24 | NOASSERTION | Indeks tool RE berbasis AI, tiap entri dinilai |
| awesome-reverse-engineering | <https://github.com/morluto/awesome-reverse-engineering> | 1.4k | CC0-1.0 | Kurasi tool & materi RE |
| REA workflows | — (tidak ada tautan) | — | — | "Prompt investigasi siap pakai yang ikut terpasang bersama REA" → lihat `references/mcp-prompts.md` |
| clean-room loop | — (tidak ada tautan) | — | — | Metode `SPEC.md → oracles → checks`; dioperasionalkan di bawah |

## Pipeline yang disebut postingan

```
binary → REA → SPEC.md → rebuild → oracle → retry
```

Dipetakan ke fase `rea-workflow`:

| Tahap pipeline | Fase | Alat/prompt |
| --- | --- | --- |
| binary | F0–F2 | routing target; GhidraMCP / ida-pro-mcp / jadx / radare2 |
| REA | F3 | `investigate_feature`, `compare_application_versions`, `trace_crash` |
| SPEC.md | F4 | template `templates/finding.md` → disusun jadi spesifikasi perilaku |
| rebuild | F6 | Apktool (APK), kode sendiri (JS/py), `rea-tool-design` bila jadi tool |
| oracle | F5 | `verify_reconstruction` + uji hitung manual + perbandingan Evidence |
| retry | F7→F3 | catat selisih sebagai `unknown` baru, ulangi F3 hanya untuk selisih itu |

Aturan: **rebuild tanpa oracle bukan rebuild**, hanya tebakan. Setiap iterasi
wajib menyebut oracle mana yang dipakai dan hasilnya.

## Prompt REA yang tersedia (dari `docs/mcp-prompts.md`)

| Prompt | Untuk fase | Kegunaan |
| --- | --- | --- |
| `investigate_feature` | F3 | Menelusuri satu fitur sampai Evidence fungsi |
| `compare_application_versions` | F3/F5 | Bandingkan dua artefak, dengan tindak lanjut statis/runtime |
| `verify_reconstruction` | F5 | Uji spesifikasi rekonstruksi terhadap Evidence pembanding |
| `trace_crash` | F3 | Hubungkan gejala crash ke jalur statis + capture proses |
| `audit_residual_unknowns` | F7 | Audit unknown yang tersisa beserta kualitas resolusinya |
| `prepare_bounded_process_capture` | F3 runtime | Rancang eksperimen proses terbatas **sebelum** eksekusi |

## Selisih & catatan jujur

| Klaim postingan | Temuan | Tindakan |
| --- | --- | --- |
| "awesome-ai-reverse-engineering: 122 repos" | README repo (2026-10-29) menyebut **118 repos**, dengan rincian 74 MCP + 17 mobile + 4 web + 19 skills + 4 kasus | Pakai angka 118 (sumbernya sendiri), catat selisihnya |
| "dnSpy" | tautan mengarah ke fork `dnSpyEx/dnSpy`; repo asli `dnSpy/dnSpy` **archived**, 29.7k★ | Rekomendasikan fork; sebut status repo asli |
| "20 repos" | 16 tautan unik + 4 repo disebut tanpa tautan (`rea`, `ghidra`, dua awesome list) — total 20 | Cocok |
| "REA workflows" & "clean-room loop" | tidak ada tautan di postingan | Dipetakan ke `mcp-prompts.md` dan pipeline di atas |
| Sebagian tautan terpotong (`…`) | redirect mendarat di URL terpotong; 404 | Repo dikonfirmasi via GitHub API (nama, lisensi, star) |

## Cara memakainya tanpa memasang semuanya

1. **Mulai dari yang sudah ada.** REA + satu decompiler (Ghidra) menutup 80%
   pekerjaan statis. Jangan pasang 20 tool di hari pertama.
2. **Pilih per jenis target** (lihat `target-routing.md`): APK → jadx/Apktool,
   .NET → ILSpy/dnSpy, Electron → REA JS, traffic → mitmproxy, runtime →
   Frida/x64dbg/raddebugger, symbolic → angr.
3. **Satu tool, satu pertanyaan.** Setiap tool yang dipasang harus menjawab satu
   jenis pertanyaan di F3; kalau tidak, jangan dipasang.
4. **Lisensi dicek sebelum dipakai komersial** — x64dbg GPL-3.0 dan radare2/rizin
   LGPL punya konsekuensi distribusi; Ghidra/jadx/Apktool Apache-2.0 lebih longgar.
5. **Semua tool ini tetap tunduk pada aturan scope**: eksekusi target (Frida,
   debugger) butuh izin eksplisit.
