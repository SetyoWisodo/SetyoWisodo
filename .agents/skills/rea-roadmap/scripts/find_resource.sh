#!/usr/bin/env bash
# find_resource.sh — cari resource roadmap dari references/resources.json
#
# Pemakaian:
#   bash scripts/find_resource.sh "apk"            # cari kata bebas
#   bash scripts/find_resource.sh --stage 4        # filter tahap belajar
#   bash scripts/find_resource.sh --category paper # start|watch|investigation|repo|book|paper|course
#   bash scripts/find_resource.sh --list           # ringkasan per kategori
#   bash scripts/find_resource.sh --check          # cek integritas index
#
# Butuh python3. Tidak mengakses jaringan, tidak mengubah file.

set -u
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
JSON="$DIR/../references/resources.json"

if [ ! -f "$JSON" ]; then
  echo "index tidak ditemukan: $JSON" >&2
  exit 2
fi
if ! command -v python3 >/dev/null 2>&1; then
  echo "butuh python3" >&2
  exit 2
fi

python3 - "$JSON" "$@" <<'PY'
import json, sys

path, args = sys.argv[1], sys.argv[2:]
data = json.load(open(path, encoding="utf-8"))
items = data["resources"]

def show(rows):
    if not rows:
        print("tidak ada hasil — coba kata yang lebih pendek atau --list")
        return
    for r in rows:
        flags = []
        if r.get("stage"): flags.append(f"tahap {r['stage']}")
        flags.append(r["status"])
        if r.get("paid") is True: flags.append("berbayar")
        if r.get("paid") is False: flags.append("gratis")
        if r.get("local"): flags.append("lokal: " + r["local"])
        print(f"[{r['category']:<13}] {r['label']}")
        print(f"                {r['url']}")
        print(f"                {' · '.join(flags)}")
        if r.get("note"): print(f"                catatan: {r['note']}")

if not args:
    args = ["--list"]

mode = args[0]
if mode == "--list":
    from collections import Counter
    c = Counter(r["category"] for r in items)
    for cat, n in c.items():
        print(f"{cat:<14} {n}")
    print(f"{'total':<14} {len(items)}  (meta: {data['meta']['counts']})")
elif mode == "--check":
    urls = {r["url"] for r in items}
    dead = [r["label"] for r in items if r["status"] == "dead"]
    print(f"entri index : {len(items)} (postingan: {data['meta']['counts']['rows_in_post']} baris)")
    print(f"url unik    : {len(urls)}")
    print(f"mati        : {len(dead)} -> {dead}")
    tco = [t for r in items for t in r.get("tco", [])]
    print(f"shortlink   : {len(tco)} (unik {len(set(tco))})")
    print(f"dengan stage: {sum(1 for r in items if r.get('stage'))}")
elif mode == "--stage":
    n = args[1]
    show([r for r in items if str(r.get("stage")) == n])
elif mode == "--category":
    cat = args[1].lower()
    show([r for r in items if r["category"] == cat])
else:
    q = " ".join(a.lower() for a in args)
    def hit(r):
        blob = " ".join([r["label"], r["url"], r.get("note",""), r["category"]] + r.get("aliases", [])).lower()
        return all(w in blob for w in q.split())
    show([r for r in items if hit(r)])
PY
