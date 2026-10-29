#!/usr/bin/env bash
# session.sh — mesin state untuk alur kerja rea-workflow.
#
# State disimpan DI LUAR tracked tree: ${REA_SESSION_ROOT:-/tmp/rea-workflow}/<slug>/
# Tidak menyentuh Git, tidak mengakses jaringan, tidak menjalankan target.
#
#   bash session.sh init "apk aegis login" --target /path/app.apk
#   bash session.sh status
#   bash session.sh gate F2 --pass "APK -> inspect_android_package"
#   bash session.sh advance F3
#   bash session.sh log "inspect_android_package -> classes2.dex"
#   bash session.sh unknown "validasi native? cek lib*.so"
#   bash session.sh resolve U1 --evidence "E4: libnative.so memuat tabel"
#   bash session.sh report
#   bash session.sh list
#   bash session.sh path

set -u
if ! command -v python3 >/dev/null 2>&1; then echo "butuh python3" >&2; exit 2; fi
export REA_WORKFLOW_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python3 - "$@" <<'PY'
import json, os, re, sys, time
from pathlib import Path

ROOT = Path(os.environ.get("REA_SESSION_ROOT", "/tmp/rea-workflow"))
PHASES = ["F0","F1","F2","F3","F4","F5","F6","F7"]
NAMES = {
    "F0": "Intake & scope", "F1": "Environment", "F2": "Route",
    "F3": "Evidence", "F4": "Interpretasi", "F5": "Verifikasi",
    "F6": "Deliverable", "F7": "Catat & tutup",
}

def now(): return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
def slugify(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:60] or "sesi"

def sessions():
    if not ROOT.exists(): return []
    out = []
    for d in ROOT.iterdir():
        f = d / "state.json"
        if f.is_file():
            out.append((f.stat().st_mtime, d, json.loads(f.read_text(encoding="utf-8"))))
    return sorted(out, key=lambda x: x[0], reverse=True)

def latest(explicit=None):
    ss = sessions()
    if not ss: sys.exit("belum ada sesi — jalankan: init \"<label>\"")
    if explicit:
        for _, d, st in ss:
            if d.name == explicit: return d, st
        sys.exit(f"sesi '{explicit}' tidak ditemukan")
    return ss[0][1], ss[0][2]

def save(d, st):
    st["updated"] = now()
    (d / "state.json").write_text(json.dumps(st, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def gate_ok(st, ph): return st["gates"].get(ph, {}).get("status") == "pass"

def cmd_init(args):
    if not args: sys.exit("pakai: init \"<label>\" [--target X] [--slug S]")
    label = args[0]; target = None; slug = None
    rest = args[1:]
    i = 0
    while i < len(rest):
        if rest[i] == "--target" and i+1 < len(rest): target = rest[i+1]; i += 2
        elif rest[i] == "--slug" and i+1 < len(rest): slug = rest[i+1]; i += 2
        else: sys.exit(f"argumen tidak dikenal: {rest[i]}")
    slug = slug or slugify(label)
    d = ROOT / slug
    if (d / "state.json").exists(): sys.exit(f"sesi '{slug}' sudah ada — pakai slug lain atau `status --slug {slug}`")
    d.mkdir(parents=True, exist_ok=True)
    st = {"slug": slug, "label": label, "target": target, "phase": "F0",
          "created": now(), "updated": now(), "gates": {}, "evidence": [],
          "unknowns": [], "events": [{"ts": now(), "kind": "init", "text": label}]}
    save(d, st)
    (d / "findings.md").write_text(
        (Path(os.environ["REA_WORKFLOW_DIR"]) / "templates" / "finding.md").read_text(encoding="utf-8"),
        encoding="utf-8")
    print(f"sesi dibuat: {d}")
    print(f"target     : {target or '(belum ada)'}")
    print("fase       : F0 — Intake & scope (isi pertanyaan dulu, lalu `gate F0 --pass ...`)")

def cmd_status(args):
    explicit = None
    if args and args[0] == "--slug": explicit = args[1]
    d, st = latest(explicit)
    print(f"sesi   : {st['slug']}  ({st['label']})")
    print(f"target : {st['target'] or '(belum ada)'}")
    print(f"fase   : {st['phase']} — {NAMES[st['phase']]}")
    print()
    print(f"{'fase':<4} {'gate':<8} catatan")
    for ph in PHASES:
        g = st["gates"].get(ph)
        mark = "-" if not g else ("PASS" if g["status"] == "pass" else "FAIL")
        cur = " <" if ph == st["phase"] else ""
        print(f"{ph:<4} {mark:<8} {(g or {}).get('note','')}{cur}")
    print()
    print(f"evidence tercatat : {len(st['evidence'])}")
    for e in st["evidence"]: print(f"  - {e['ts']} {e['text']}")
    open_u = [u for u in st["unknowns"] if u["status"] == "open"]
    print(f"unknown terbuka   : {len(open_u)}")
    for u in open_u: print(f"  - {u['id']} {u['text']}")
    print()
    blocked = [p for p in PHASES if p != st["phase"] and not gate_ok(st, p)
               and PHASES.index(p) < PHASES.index(st["phase"])]
    if blocked: print(f"peringatan: gate belum lulus pada fase sebelumnya: {', '.join(blocked)}")
    nxt = PHASES[PHASES.index(st["phase"]) + 1] if st["phase"] != "F7" else None
    print(f"langkah: {'gate ' + st['phase'] + ' lalu advance' if not gate_ok(st, st['phase']) else ('advance ke ' + nxt if nxt else 'tutup sesi (F7 selesai)')}")
    print(f"path   : {d}")

def cmd_gate(args):
    if len(args) < 3: sys.exit("pakai: gate F2 --pass|--fail \"catatan\"")
    ph, flag, note = args[0].upper(), args[1], " ".join(args[2:])
    if ph not in PHASES: sys.exit(f"fase tidak dikenal: {ph}")
    if flag not in ("--pass", "--fail"): sys.exit("pakai --pass atau --fail")
    d, st = latest()
    st["gates"][ph] = {"status": "pass" if flag == "--pass" else "fail",
                       "note": note, "ts": now()}
    st["events"].append({"ts": now(), "kind": "gate", "text": f"{ph} {flag} {note}"})
    save(d, st)
    print(f"gate {ph}: {'PASS' if flag == '--pass' else 'FAIL'} — {note}")

def cmd_advance(args):
    d, st = latest()
    cur = st["phase"]
    if not gate_ok(st, cur):
        sys.exit(f"tidak bisa maju: gate {cur} belum PASS (pakai `gate {cur} --pass \"...\"`)")
    nxt = args[0].upper() if args else None
    want = PHASES[PHASES.index(cur) + 1] if cur != "F7" else None
    if nxt and nxt != want:
        sys.exit(f"lompat fase tidak diizinkan: dari {cur} hanya boleh ke {want}")
    if not want: sys.exit("sudah di fase terakhir (F7) — sesi selesai")
    st["phase"] = want
    st["events"].append({"ts": now(), "kind": "advance", "text": f"{cur} -> {want}"})
    save(d, st)
    print(f"fase sekarang: {want} — {NAMES[want]}")

def cmd_log(args):
    if not args: sys.exit("pakai: log \"<teks>\"")
    text = " ".join(args)
    d, st = latest()
    st["evidence"].append({"ts": now(), "text": text})
    st["events"].append({"ts": now(), "kind": "log", "text": text})
    save(d, st)
    print(f"dicatat (#{len(st['evidence'])}): {text}")

def cmd_unknown(args):
    if not args: sys.exit("pakai: unknown \"<pertanyaan terbuka>\"")
    text = " ".join(args)
    d, st = latest()
    uid = f"U{len(st['unknowns']) + 1}"
    st["unknowns"].append({"id": uid, "text": text, "status": "open", "ts": now()})
    st["events"].append({"ts": now(), "kind": "unknown", "text": f"{uid}: {text}"})
    save(d, st)
    print(f"{uid} dicatat: {text}")

def cmd_resolve(args):
    if not args: sys.exit("pakai: resolve U1 --evidence \"E4: ...\"")
    uid = args[0].upper()
    ev = None
    if "--evidence" in args:
        i = args.index("--evidence")
        ev = " ".join(args[i+1:]) or None
    if not ev: sys.exit("menutup unknown butuh --evidence \"<bukti>\"")
    d, st = latest()
    for u in st["unknowns"]:
        if u["id"] == uid:
            u.update(status="resolved", evidence=ev, resolved=now())
            st["events"].append({"ts": now(), "kind": "resolve", "text": f"{uid} <- {ev}"})
            save(d, st)
            print(f"{uid} ditutup dengan bukti: {ev}")
            return
    sys.exit(f"unknown {uid} tidak ditemukan")

def cmd_report(args):
    d, st = latest()
    print(f"# Sesi REA — {st['label']}\n")
    print(f"- target : {st['target'] or '(belum ada)'}")
    print(f"- fase   : {st['phase']} — {NAMES[st['phase']]}")
    print(f"- dibuat : {st['created']}  (update {st['updated']})")
    print("\n## Gate\n")
    for ph in PHASES:
        g = st["gates"].get(ph)
        if g: print(f"- {ph} {g['status'].upper()}: {g['note']}")
    print("\n## Evidence\n")
    for e in st["evidence"] or [{"text": "(kosong)"}]: print(f"- {e.get('ts','')} {e['text']}")
    print("\n## Unknown\n")
    if not st["unknowns"]: print("- (tidak ada yang dicatat)")
    for u in st["unknowns"]:
        tail = f" -> {u.get('evidence')}" if u["status"] == "resolved" else ""
        print(f"- {u['id']} [{u['status']}] {u['text']}{tail}")
    nxt = (PHASES[PHASES.index(st['phase']) + 1]
           if st['phase'] != 'F7' else None)
    print("\n## Langkah berikutnya\n")
    if not gate_ok(st, st["phase"]):
        print(f"1. lengkapi gate {st['phase']} (`gate {st['phase']} --pass \"...\"`)")
    elif nxt:
        print(f"1. `advance {nxt}` — {NAMES[nxt]}")
    else:
        print("1. sesi selesai; arsipkan folder ini bila perlu")
    print(f"2. findings: {d / 'findings.md'}")

def cmd_list(args):
    ss = sessions()
    if not ss: print("belum ada sesi"); return
    print(f"{'slug':<34} {'fase':<5} {'gate':<6} unknown  label")
    for _, d, st in ss:
        g = st["gates"].get(st["phase"], {}).get("status", "-")
        u = sum(1 for x in st["unknowns"] if x["status"] == "open")
        print(f"{d.name:<34} {st['phase']:<5} {g:<6} {u:<8} {st['label']}")

def cmd_path(args):
    d, st = latest()
    print(d); print(d / "state.json"); print(d / "findings.md")

def cmd_tools(args):
    tp = Path(os.environ["REA_WORKFLOW_DIR"]) / "references" / "re-toolchain.json"
    if not tp.is_file(): sys.exit(f"index tool tidak ditemukan: {tp}")
    data = json.loads(tp.read_text(encoding="utf-8"))
    tools = data["tools"]
    group = None; stage = None
    i = 0
    while i < len(args):
        if args[i] == "--group" and i+1 < len(args): group = args[i+1]; i += 2
        elif args[i] == "--stage" and i+1 < len(args): stage = int(args[i+1]); i += 2
        elif args[i] in ("--list","-l"): group = ""; i += 1
        else: sys.exit("pakai: tools [--group analysis-core|mobile|binary|network|rebuild] [--stage N]")
    if args == ["--list"] or (group == "" ):
        from collections import Counter
        for g, n in Counter(x["group"] for x in tools).items(): print(f"{g:<14} {n}")
        print(f"{'total':<14} {len(tools)}  (+4 tanpa tautan: REA workflows, clean-room loop)")
        print("\npipeline:", "; ".join(data["meta"].get("pipelines", [])))
        return
    rows = [x for x in tools if (group is None or x["group"] == group)
            and (stage is None or x.get("stage") == stage)]
    if not rows: print("tidak ada hasil"); return
    for x in rows:
        star = f"{x['stars']}★" if x.get("stars") else "—"
        print(f"[{x['group']:<13}] {x['label']}  ({star}, {x.get('license') or '?'}, {x['kind']}, tahap {x.get('stage')})")
        print(f"                {x['url']}")
        if x.get("note"): print(f"                catatan: {x['note']}")

CMD = {"init": cmd_init, "status": cmd_status, "gate": cmd_gate, "advance": cmd_advance,
       "log": cmd_log, "unknown": cmd_unknown, "resolve": cmd_resolve,
       "report": cmd_report, "tools": cmd_tools, "list": cmd_list, "path": cmd_path}

if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help", "help"):
    print(__doc__ or "")
    print("perintah: " + ", ".join(CMD))
    sys.exit(0)
cmd, rest = sys.argv[1], sys.argv[2:]
if cmd not in CMD:
    sys.exit(f"perintah tidak dikenal: {cmd} (pilihan: {', '.join(CMD)})")
CMD[cmd](rest)
PY
