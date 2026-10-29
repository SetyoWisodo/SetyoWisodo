# Matriks kapabilitas (diuji, bukan diasumsikan)

Diuji pada **2026-10-29** di sandbox Debian 12, 2 vCPU, 3 GB RAM, 20 GB disk.
Kolom *Bukti* memuat perintah yang benar-benar dijalankan dan hasilnya.

## Yang berhasil dijalankan

| Kapabilitas | Perintah | Bukti |
| --- | --- | --- |
| REA CLI tersedia via npx | `npx -y rea-agents@latest --version` | `6.8.0` (warning `EBADENGINE`: butuh Node ≥22.23.4, tersedia 22.22.3 — tetap jalan) |
| Analisis JS/Electron penuh (graph + Evidence tersegel) | `npx -y rea-agents@latest analyze-javascript-application <dir> --json` | `evidence_id ev_d610…622c`, predicate `rea.javascript-application-analysis`, 20 fase progres, coverage/limitations lengkap |
| Inventory artefak (ZIP/APK/ASAR/DMG…) | `npx -y rea-agents@latest inspect-artifact <file>` | `ev_05a3…4e54`, format `zip`, provider `rea-artifact-graph` |
| Ekstraksi member artefak | `… extract-artifact` | provider `rea-artifact-graph` (available: true) |
| Layout ELF (segmen, symbol, relokasi, mitigasi) | `REA_PWNTOOLS_PYTHON=/tmp/reavenv/bin/python … inspect-binary-layout /bin/ls` | `ev_128b…a719`, provider `pwntools@4.15.0;pyelftools@0.33;unicorn@2.1.2`, `EM_X86_64`, `ET_DYN` |
| Manajer paket Python | `python3 -m pip install --user --break-system-packages …` | capstone 5.0.7, pyelftools 0.33, pwntools 4.15.0, unicorn 2.1.2 terpasang |
| Registry npm | `npm view rea-agents version` | `6.8.0` |
| Membangun target/fixture sendiri | `gcc`, `g++`, `make` | tersedia |
| Tool biner dasar | `objdump`, `readelf`, `nm`, `strings`, `unzip`, `zip` | tersedia |
| Compiler/paket JS | `node` 22.22.3, `npm` 10.9.8 | tersedia |

## Yang belum tersedia (dan penyebab persisnya)

| Kapabilitas | Perintah | Penyebab |
| --- | --- | --- |
| Decompile native (pseudocode) | `rea analyze /bin/ls` | `provider_unavailable`: Ghidra `not_configured` (tanpa `GHIDRA_INSTALL_DIR` + JRE), Hopper tidak ada, IDA/Kuna tanpa registrasi |
| APK → Java (dex) | `inspect-android-package` | butuh `REA_JADX_MCP_JAR` + Java (tidak ada JRE di image) |
| .NET decompile | — | ILSpy butuh runtime .NET; `inspect_managed_artifact` (metadata) belum diuji karena tidak ada sampel PE .NET |
| Runtime/hooking | Frida, x64dbg, gdb | tidak terpasang; `gdb` tidak ada di image |
| Capture jaringan | tshark, mitmproxy | tidak terpasang |
| Browser capture | Playwright | butuh unduhan browser dari host di luar allowlist sandbox |

## Cara menaikkan batas (butuh izin user)

1. **Decompile native** — pasang JDK + Ghidra di mesin user, lalu set
   `GHIDRA_INSTALL_DIR`. Di sandbox ini tidak bisa: unduhan JDK/Ghidra berasal
   dari host di luar allowlist.
2. **APK → Java** — set `REA_JADX_MCP_JAR` (dan Java) di mesin user.
3. **Runtime** — Frida/x64dbg/raddebugger hanya di mesin user, dan hanya dengan
   izin eksekusi eksplisit.
4. **Python venv** — untuk `inspect_binary_layout`, arahkan
   `REA_PWNTOOLS_PYTHON` ke venv yang berisi pwntools 4.15.0, pyelftools 0.33,
   unicorn 2.1.2 (user-site `/usr/bin/python3` **tidak** diterima REA).

## Konsekuensi untuk kontrak Evidence

| Fase | Di sandbox ini | Di mesin user (dengan engine) |
| --- | --- | --- |
| F3 JS/Electron | klaim penuh, Evidence tersegel | sama |
| F3 arsip/APK (inventori) | klaim struktur & integritas | sama + kode dex |
| F3 ELF layout | klaim struktur, symbol, mitigasi | sama + pseudocode |
| F3 perilaku runtime | **tidak boleh diklaim** | boleh, dengan izin + capture |
| F6 rebuild JS | bisa (SPEC.md + implementasi) | sama |
| F6 rebuild native | hanya spesifikasi dari layout/symbol | bisa sampai pseudocode |

Aturan yang tetap: keluaran `objdump`/`readelf`/`strings` **bukan** pengganti
pseudocode; kalau pseudocode tidak tersedia, tulis di "Belum diketahui".
