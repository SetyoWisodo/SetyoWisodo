#!/usr/bin/env bash
# check_readiness.sh — pemeriksaan read-only untuk skill rea-roadmap.
#
# Tidak memasang, tidak mengubah, tidak menjalankan target apa pun.
# Pemakaian:
#   bash scripts/check_readiness.sh            # ringkasan environment
#   bash scripts/check_readiness.sh /path/file # + cek file target
#
# Keluaran: tabel status per komponen, lalu rekomendasi tahap awal roadmap.

set -u

TARGET="${1:-}"
ok=0
warn=0
no=0

row() { # row <status> <nama> <detail>
  printf '%-6s %-22s %s\n' "$1" "$2" "$3"
  case "$1" in
    OK)   ok=$((ok+1)) ;;
    WARNA|WARN) warn=$((warn+1)) ;;
    TIDAK) no=$((no+1)) ;;
  esac
}

have() { command -v "$1" >/dev/null 2>&1; }

echo "== rea-roadmap readiness =="
printf 'waktu: %s\n' "$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
printf 'host : %s (%s)\n\n' "$(uname -s)" "$(uname -m)"
printf '%-6s %-22s %s\n' STATUS KOMPONEN DETAIL
printf '%-6s %-22s %s\n' ------ -------- ------

# --- runtime agent ---------------------------------------------------------
if have node; then
  v=$(node -v 2>/dev/null)
  major=${v#v}; major=${major%%.*}
  if [ "${major:-0}" -ge 20 ] 2>/dev/null; then
    row OK "node" "$v"
  else
    row WARN "node" "$v (disarankan >= 20 untuk rea-agents terbaru)"
  fi
else
  row TIDAK "node" "tidak ada — setup REA butuh Node.js"
fi

if have npx; then row OK "npx" "$(npx --version 2>/dev/null)"; else row TIDAK "npx" "tidak ada — jalur 'npx rea-agents' tidak bisa dipakai"; fi

# --- REA ------------------------------------------------------------------
if have rea; then
  row OK "rea CLI" "$(command -v rea)"
  if rea --version >/dev/null 2>&1; then row OK "rea --version" "$(rea --version 2>/dev/null | head -1)"; fi
else
  row TIDAK "rea CLI" "belum terpasang (opsional: npx rea-agents@latest setup)"
fi
if [ -d "$HOME/.rea" ]; then row OK "state ~/.rea" "ada"; else row WARN "state ~/.rea" "belum ada — setup belum pernah dijalankan"; fi

# --- engine ---------------------------------------------------------------
if have ghidra || have analyzeHeadless || [ -n "${GHIDRA_INSTALL_DIR:-}" ]; then
  row OK "ghidra" "${GHIDRA_INSTALL_DIR:-ada di PATH}"
else
  row WARN "ghidra" "tidak terdeteksi (dibutuhkan tahap 3, 5, 6)"
fi
if have jadx; then row OK "jadx" "$(command -v jadx)"; else row WARN "jadx" "tidak ada (tahap 4, bisa dilewati bila engine Android REA tersedia)"; fi
if have java; then row OK "java" "$(java -version 2>&1 | head -1)"; else row WARN "java" "tidak ada (Ghidra/JADX butuh JRE)"; fi
if have frida; then row OK "frida" "$(frida --version 2>/dev/null)"; else row WARN "frida" "tidak ada (hanya untuk analisis runtime tahap 4/7)"; fi
if have tshark; then row OK "tshark" "$(tshark -v 2>/dev/null | head -1)"; else row WARN "tshark" "tidak ada (hanya bila menganalisis pcap)"; fi
if have python3; then row OK "python3" "$(python3 -V 2>&1)"; else row TIDAK "python3" "tidak ada (dipakai beberapa latihan & scripts)"; fi

# --- target ---------------------------------------------------------------
if [ -n "$TARGET" ]; then
  if [ -e "$TARGET" ]; then
    row OK "target" "$TARGET"
    if [ -f "$TARGET" ] && have sha256sum; then
      row OK "sha256" "$(sha256sum "$1" 2>/dev/null | cut -d' ' -f1)"
    fi
    if [ -f "$TARGET" ] && have file; then row OK "file(1)" "$(file -b "$1" 2>/dev/null | cut -c1-70)"; fi
  else
    row TIDAK "target" "$TARGET tidak ditemukan"
  fi
else
  row WARN "target" "tidak diberikan (opsional)"
fi

echo
echo "ringkasan: OK=$ok WARN=$warn TIDAK=$no"

cat <<'EOF'

Saran tahap awal (lihat references/learning-path.md):
  - node/npx TIDAK ada          -> Tahap 1 (prasyarat), jangan lompat
  - rea CLI / state belum ada   -> Tahap 1 (setup, butuh izin user)
  - setup ada, ghidra tidak ada -> Tahap 2 (Notes Export) dulu
  - ghidra ada, belum CTF       -> Tahap 3
  - target .apk                 -> Tahap 4
  - target Electron/game        -> Tahap 5
Catatan: skrip ini TIDAK memasang apa pun dan TIDAK menjalankan target.
EOF
