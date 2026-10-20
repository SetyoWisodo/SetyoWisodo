# -*- coding: utf-8 -*-
"""Memuat analisis Future Scenarios yang unik untuk setiap bab."""
import glob
import json
import os

_DIR = os.path.dirname(os.path.abspath(__file__))
_entries = []
for _f in sorted(glob.glob(os.path.join(_DIR, "future_scenarios", "part_*.json"))):
    with open(_f, encoding="utf-8") as _fh:
        _entries.extend(json.load(_fh)["chapters"])

_entries.sort(key=lambda e: e["idx"])
FUTURE_SCENARIOS = _entries

if __name__ == "__main__":
    print(len(FUTURE_SCENARIOS), "entri; idx:", [e["idx"] for e in FUTURE_SCENARIOS])
