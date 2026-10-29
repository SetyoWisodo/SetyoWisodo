# Routing target (ringkas & operasional)

Ini ringkasan eksekusi dari `reverse-engineer-anything/SKILL.md` bagian *"Route the
target first"*. Kalau ada perbedaan, file asli itu yang menang — buka
[`../../reverse-engineer-anything/SKILL.md`](../../reverse-engineer-anything/SKILL.md).

## Tabel utama

| Target yang diberikan user | Tool pertama | Engine/prasyarat | Lanjutan tipikal |
| --- | --- | --- | --- |
| Binary native (PE/ELF/Mach-O), DB analisis | `open_binary` | Ghidra (atau IDA/Kuna) | `binary_overview`, `analyze_function`, xref, string |
| APK/AAB (kode, kelas, method, xref) | `inspect_android_package` | engine Android (terpisah) | tool Android terfokus, `inspect_apk_signature` untuk signing |
| APK/ZIP sebagai arsip (isi member) | `open_binary` | — | `inspect_artifact`, inventory |
| ASAR / tree JavaScript / Electron | `analyze_javascript_application` | — | `inspect_analysis_view` (module, node) |
| Electron runtime hidup | `list_electron_targets` | app berjalan + fuses | `inspect_electron_fuses` sebelum coba `--inspect` |
| Paket Python (PyInstaller) | `open_binary` → `inspect_artifact` | — | ekstrak module, analisis JS/py |
| Bun `--compile` | `open_binary` → `inspect_artifact` | — | ekstrak module tersimpan |
| Apple bundle resources (plist, IB, asset) | `open_bundle_resources` | — | tool resource terpilih |
| Managed PE/CLI (.NET) | `inspect_managed_artifact` | — | decompile C# (ILSpy) |
| .NET NativeAOT | Ghidra native | Ghidra | workflow NativeAOT di `native-and-artifacts.md` |
| Firmware image | `inspect_firmware_regions` / `extract_firmware` | Binwalk/Unblob (Linux) | analisis filesystem hasil ekstrak |
| ESP32 app/bootloader (magic `0xE9`) | `inspect_artifact` | — | — |
| WebAssembly lokal | `inspect_wasm_artifact` | WABT 1.0.42 | WAT + glue JS |
| SQLite snapshot | `inspect_sqlite_database` | Node 24.x/26+ | schema dulu, lalu baris terpilih |
| ELF layout/symbol/mitigasi offline | `inspect_binary_layout` | pwntools | halaman terpilih |
| Core dump ELF x86-64 | `inspect_recorded_crash` | — | thread, register, note |
| PE resources / export | `inspect_pe_resources`, `inspect_native_exports` | — | — |
| EVM bytecode lokal | `inspect_evm_interface` | — | `detail: "summary"` |
| HAR/SAZ/mitmproxy/qlog tersimpan | `inspect_web_network_capture` | — | ordinal record, sidecar byte |
| pcap/pcapng | `inspect_packet_capture` / `inspect_pcap_capture` | TShark 4.x, Linux prlimit | field, filter, paging |
| Logic/signal recording | `decode_signal_recording` | sigrok-cli 0.7.2 | kelas anotasi, paging |
| Browser milik user (sudah terbuka) | `list_browser_targets` | browser debugging | aksi terfokus |
| Aksi browser yang harus agent lakukan | `capture_browser_scenario` | browser otomatis | rekam + hasil |
| AgentEnv bundle web app | `capture_browser_scenario` → `export_environment_bundle` | — | baca `environments.md` |
| Tidak ada API/SDK/spesifikasi | `find-reverse-engineered` | python3 | tool open-source + lisensi |

## Engine & tool pendukung (dari `references/re-toolchain.md`)

| Kebutuhan | Utama | Pendukung |
| --- | --- | --- |
| Decompiler native | Ghidra (atau IDA/Kuna) | radare2 / rizin untuk terminal, ImHex untuk format file |
| Agent mengendalikan decompiler | REA MCP | GhidraMCP, ida-pro-mcp |
| Android | engine Android REA / jadx | Apktool (resource), Frida (runtime, butuh izin) |
| .NET | `inspect_managed_artifact` | ILSpy, dnSpy (fork `dnSpyEx`) |
| Traffic | `inspect_web_network_capture` | mitmproxy untuk menangkap |
| Runtime native | tool runtime REA | x64dbg (Windows), raddebugger, Frida |
| "Input apa yang lolos" | analisis cabang manual | angr (symbolic execution) |
| Cari tool yang sudah ada | `find-reverse-engineered` | awesome-ai-reverse-engineering (118 entri tergrading) |

## Aturan pemilihan

1. **Pertanyaan menentukan tool.** "Bagaimana login divalidasi" → kode (APK/native),
   bukan inventaris arsip. "Apa saja isi paket" → inventory, bukan decompiler.
2. **Runtime ≠ statis.** `open_binary`/`analyze_function` tidak membuktikan
   perilaku eksekusi. Pertanyaan runtime butuh tool runtime + izin menjalankan.
3. **Summary dulu.** Target besar: `detail: "summary"`, lalu `inspect_analysis_view`.
4. **Jangan minta provider yang tidak ada.** Cek `binary_session {}` →
   `result.tool_availability` untuk alasan dan remediasi sebelum menyalahkan target.
5. **Target ambigu → tanya.** "App saya" tanpa nama/path bukan target; jangan
   memilih contoh dari dokumentasi.

## Tanpa MCP (kondisi sandbox ini)

Bila tool REA tidak tersedia, rute turun menjadi rantai tool lokal dan klaim
dibatasi:

| Pertanyaan | Rantai lokal | Batas klaim |
| --- | --- | --- |
| Jenis file, arsitektur, arsip | `file`, `unzip -l`, `python3 zipfile` | struktur, bukan kode |
| Identitas & integritas | `sha256sum`, `md5sum` | tingkat byte, deterministik |
| String/konstanta | `strings -n 6`, `python3` regex | literal, bukan alur logika |
| Android dasar | `unzip classes*.dex`, `dexdump`/`baksmali` bila ada | daftar kelas/method |
| JS bundle | `node --check`, `grep`, prettier | kode yang terlihat |
| Perilaku | **tidak bisa** tanpa eksekusi/izin | nyatakan sebagai unknown |

Jangan pernah menyajikan keluaran `strings` atau `grep` sebagai hasil decompiler.
