# Alur kerja 7 tahap

Urutan ini diambil dari bagian **"BEST ORDER TO LEARN"** di postingan, lalu
diberi kriteria masuk/keluar supaya bisa dieksekusi dan diuji, bukan cuma dibaca.

```
Tahap 1 Setup → 2 Investigasi pertama (Notes Export) → 3 CTF binary
      → 4 APK Android (Aegis) → 5 Electron/game (Notion, DX-Ball, TH04)
      → 6 Ghidra + assembly → 7 Paper + tooling lanjutan
```

Aturan umum:

- Satu tahap = satu target. Jangan mencampur dua target dalam satu sesi belajar.
- Setiap tahap berakhir dengan **Evidence**, bukan dengan "sudah nonton".
- Jika kriteria keluar gagal, diagnosis penyebabnya dulu (environment? skill
  routing? engine belum ada?) sebelum mengulang.

---

## Tahap 1 — Setup dan kesiapan

**Tujuan:** agent bisa memanggil tool REA pada satu target, dan engine yang
dibutuhkan tahap ini sudah ada.

**Resource:** Installation & Agent Setup (docs), REA Official Website,
`npx rea-agents@latest setup`, video "How To Use REA To Clone Any Software In
Minutes".

**Langkah:**

1. Cek prasyarat: Node.js tersedia, agent (Claude Code / Codex / Cursor / Pi)
   sudah bisa menjalankan MCP.
2. Jalankan `npx rea-agents@latest setup`. Baca rencana perubahan yang
   ditampilkan (path config tiap client, path skill, paket eksternal) lalu
   setujui. Untuk versi tanpa TUI: lihat `references/installation.md`.
3. Restart agent yang disebut di pesan selesai.
4. Verifikasi: minta daftar tool `rea` (mis. `binary_session` dengan `{}`), atau
   `rea doctor` untuk registrasi milik setup.

**Kriteria keluar:** agent menampilkan tool REA yang tersedia, dan `rea doctor`
tidak melaporkan `configuration_invalid`.

**Jebakan:** mengira skill = engine. Meng-copy `SKILL.md` tidak memasang MCP.
Juga: `rea setup` tidak meng-install Node, Java, Ghidra, IDA, JADX, atau Kuna.

---

## Tahap 2 — Investigasi pertama: Notes Export

**Tujuan:** merasakan siklus penuh *pertanyaan → Evidence → jawaban* pada target
paling kecil.

**Resource:** <https://rea.tools/first-investigation/>

**Prompt siap tempel:**

> Use REA to inspect the Notes app on this machine. Where do exported notes go,
> and what does the CSV formatter do to a title that contains a comma or a quote?
> Show the code path and the Evidence, then tell me what is still unknown.

**Langkah:** baca `first-investigation` sekali sebagai panduan; ulangi pada mesin
user. Perhatikan tiga hal yang harus muncul di jawaban: (a) lokasi file hasil
export, (b) fungsi formatter, (c) batas seperti encoding/quoting.

**Kriteria keluar:** user bisa menjelaskan sendiri (tanpa membaca ulang halaman)
di mana hasil export ditulis dan bagaimana quoting bekerja, dengan merujuk
potongan kode/fungsi yang dikembalikan tool.

**Jebakan:** menerima ringkasan tanpa Evidence; bertanya "jelaskan semua fitur
app ini" (terlalu luas, hasilnya dangkal).

---

## Tahap 3 — Binary kecil: CTF

**Tujuan:** bisa membaca alur program native tanpa pseudocode yang sempurna.

**Resource:** <https://rea.tools/showcase/ctf/>, pwn.college *Reverse
Engineering*, OpenSecurityTraining2 *Arch1001 x86-64 Assembly* (mulai bagian
register + calling convention), Nightmare (latihan bertingkat),
RPISEC MBE (untuk latihan memory corruption).

**Prompt siap tempel:**

> Use REA on `/path/to/challenge`. Find the check that decides success, explain
> the comparison in terms of registers and stack layout, and give me the exact
> instructions with addresses. Do not run the program.

**Langkah:** pilih satu binary kecil (≤100 KB). Minta `binary_overview` dulu,
lalu `analyze_function` pada fungsi yang memanggil `strcmp`/`memcmp`. Baru
setelah itu minta pseudocode.

**Kriteria keluar:** user bisa menuliskan aturan pengecekan (mis. "input byte ke-i
di-XOR 0x5a lalu dibandingkan dengan tabel di `.rodata`") **tanpa** menjalankan
program, dan tahu di mana Evidence-nya.

**Jebakan:** langsung minta decompile seluruh binary; tidak mencatat alamat.
Debugger (x64dbg/GDB) dipakai hanya kalau pertanyaannya memang runtime —
dan skill ini tidak mengizinkan eksekusi target tanpa izin.

---

## Tahap 4 — Android: Aegis APK

**Tujuan:** menguasai rute APK (engine Android terpisah) dan membaca kode
aplikasi mobile.

**Resource:** <https://rea.tools/showcase/aegis/>, JADX, OWASP MASTG,
video "Frida for Android Reverse Engineering", buku *The Android Malware
Handbook*.

**Prompt siap tempel:**

> Use REA to inspect `/path/app.apk`. Find how the login code is validated, show
> the smali/dex evidence and any native library involved, and list what you could
> not determine.

**Langkah:** `inspect_android_package` → fokus kelas login → cek apakah validasi
ada di Java/Kotlin atau jatuh ke `lib*.so` (kalau native, lanjut ke Ghidra di
tahap 6). Untuk analisis runtime, Frida butuh perangkat/emulator dan izin user.

**Kriteria keluar:** user bisa menjelaskan alur validasi login dan menyebut
dengan tepat bagian mana yang Jawa vs native, plus batas analisis statis.

**Jebakan:** lupa bahwa engine Android di-install terpisah — kalau tool tidak
tersedia, jangan mengulang call yang sama; cek kesiapan engine dulu.

---

## Tahap 5 — Desktop/Electron/game: Notion, DX-Ball, TH04

**Tujuan:** bekerja pada target yang lebih besar dan berlapis (Electron
JavaScript, game DOS/x86, data-driven bullet patterns).

**Resource:** <https://rea.tools/showcase/notion/>,
<https://rea.tools/showcase/dx-ball/>, <https://rea.tools/showcase/th04/>,
REA Guides (native/javascript/browser), DataCamp tutorial REA + Pi Coding Agent,
buku *The Ghidra Book* (bab awal sebagai pendamping).

**Prompt siap tempel (Electron):**

> Use REA to inspect the Notion desktop app. Explain how the clipboard handler
> works for a copied block, show the loaded modules you inspected, and separate
> what is proven from what is inferred.

**Prompt siap tempel (game):**

> Use REA on the DX-Ball executable. Recover the rule that decides sound panning
> for a ball hit, show the branch and constants, then describe how I would
> rebuild that rule in my own code.

**Kriteria keluar:** satu fitur dijelaskan end-to-end (input → branch → efek) dengan
konstanta dan alamat/nama modul, plus satu paragraf "yang belum diketahui".

**Jebakan:** mencampur bukti hasil baca kode dengan tebakan desain; jangan
mengklaim versi lain berperilaku sama tanpa membandingkan versi.

---

## Tahap 6 — Ghidra + assembly

**Tujuan:** bisa bekerja mandiri di dalam decompiler, tidak bergantung pada
ringkasan agent.

**Resource:** *The Ghidra Book 2nd Edition*, video "Ghidra Tutorial for
Beginners", Ghidra repo, OpenSecurityTraining2 *Arch1001*, *Reverse Engineering
for Beginners*.

**Langkah:** buka binary tahap 3/5 di Ghidra, ulangi satu analisis yang tadi
dikerjakan agent, bandingkan hasilnya. Fokus latihan: rename variabel, tipe
struct, xref, calling convention (SysV vs Windows x64), lalu pola switch/jump
table.

**Kriteria keluar:** user bisa menghasilkan pseudocode yang bisa dibaca untuk satu
fungsi, dan menunjukkan perbedaan hasilnya dengan pseudocode agent (siapa yang
lebih benar dan kenapa).

**Jebakan:** menghafal hotkey tapi tidak paham ABI; membaca assembly tanpa
menuliskan asumsi tipe.

---

## Tahap 7 — Paper + tooling lanjutan

**Tujuan:** mengikuti state of the art dan memakai tool khusus (Frida, ILSpy,
x64dbg, JADX CLI, MCP/Iindex).

**Resource:** semua paper (LLM4Decompile, AutoDecompiler/ALT4Decompile,
Decomperson, DIRTY, *Automatically Attacking Software RE Agents*, *Does RE Need a
Bigger Model?*), *Practical Binary Analysis*, *Practical Malware Analysis*,
*Reversing: Secrets of RE*, REA Gems, Awesome Reverse Engineering, serta skill
`find-reverse-engineered` untuk mencari tool open-source pengganti API tertutup.

**Langkah:** pilih satu paper, identifikasi (a) klaim, (b) dataset/metrik, (c)
batasan yang penulis akui. Lalu uji satu klaim itu pada target nyata memakai
tool yang ada. Tulis hasilnya di catatan, bukan di repo.

**Kriteria keluar:** satu catatan 1 halaman: klaim paper → uji → hasil → apakah
relevan untuk target user.

**Jebakan:** memperlakukan benchmark paper sebagai jaminan performa tool;
menganggap semua binary cocok dengan decompiler LLM.

---

## Tabel ringkas

| Tahap | Target | Engine/tool yang perlu siap | Bukti keluar |
| --- | --- | --- | --- |
| 1 | Setup | Node, agent, MCP `rea` | tool list + `rea doctor` bersih |
| 2 | Notes app | REA dasar | lokasi export + fungsi formatter |
| 3 | CTF binary kecil | Ghidra (atau Kuna/IDA) | aturan validasi + alamat |
| 4 | Aegis APK | engine Android (JADX/REA Android) | alur login, Jawa vs native |
| 5 | Notion / DX-Ball / TH04 | JS + native | satu fitur end-to-end |
| 6 | Ghidra mandiri | Ghidra GUI | pseudocode buatan sendiri |
| 7 | Paper + tool khusus | Frida/ILSpy/x64dbg/MCP | catatan uji klaim |

## Kalau user ingin mempercepat

Postingan mengurutkan begini; mempercepat hanya masuk akal bila user sudah punya
latar. Tetap pertahankan Tahap 1 dan 2 (siklus Evidence) — melewatinya membuat
semua tahap berikutnya jadi tebakan.
