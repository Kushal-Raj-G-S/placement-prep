"""Merge the generated aptitude questions into '7 - Aptitude Sprint'. Run: python _build/build_aptitude.py
The first run snapshots the original bank to _build/apt_base_bank.json; later runs rebuild from that snapshot,
so the original questions keep their indices (saved progress is keyed by index) and reruns never duplicate."""
import json
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
PAGE = os.path.join(ROOT, "7 - Aptitude Sprint (formulas + practice).html")
BASE = os.path.join(HERE, "apt_base_bank.json")

import apt_gen_a1, apt_gen_a2, apt_gen_b1, apt_gen_b2

html = open(PAGE, encoding="utf8").read()
m = re.search(r'(<script type="application/json" id="bank">)(.*?)(</script>)', html, re.S)
if not os.path.exists(BASE):
    shutil.copy(PAGE, os.path.join(HERE, "apt_page_backup.html"))
    open(BASE, "w", encoding="utf8").write(m.group(2))
bank = json.loads(open(BASE, encoding="utf8").read())

new = apt_gen_a1.build() + apt_gen_a2.build() + apt_gen_b1.build() + apt_gen_b2.build()
sheets = set(bank["sheets"])
have = {q["q"] for q in bank["q"]}
errs, out = [], []
for q in new:
    if q["s"] not in sheets:
        errs.append(f"unknown sheet {q['s']}")
    if len(set(q["o"])) != 4 or not 0 <= q["a"] < 4:
        errs.append(f"bad options: {q['q'][:60]}")
    if q["q"] in have:
        continue
    have.add(q["q"])
    out.append(q)
if errs:
    sys.exit("\n".join(errs))
bank["q"] = bank["q"] + out
body = json.dumps(bank, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
html = html[:m.start(2)] + "\n" + body + "\n" + html[m.end(2):]
open(PAGE, "w", encoding="utf8").write(html)

by = {}
for q in bank["q"]:
    by[q["s"]] = by.get(q["s"], 0) + 1
print(len(bank["q"]), "questions;", len(out), "added")
for s, n in by.items():
    print(f"  {s}: {n}")
