"""Inject the study guide into '5 - SQL Lab (practice).html'. Run: python _build/build_sqlstudy.py
Always rebuilds from _build/sqllab_base.html (the original page, snapshotted on the first run).
Also executes every runnable SQL block on the sample database with Python's sqlite3, so a broken example fails the build."""
import json
import os
import shutil
import sqlite3
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
PAGE = os.path.join(ROOT, "5 - SQL Lab (practice).html")
BASE = os.path.join(HERE, "sqllab_base.html")

if not os.path.exists(BASE):
    shutil.copy(PAGE, BASE)
html = open(BASE, encoding="utf8").read()

import importlib

topics = []
for name in ("mat_01_dbms", "mat_02_design", "mat_03_sql", "mat_03b_queries", "mat_03c_dml", "mat_04_adv", "mat_05_rdbms"):
    try:
        topics += importlib.import_module(name).build()
    except ModuleNotFoundError as e:
        if e.name != name:
            raise
        print("skipping missing module", name)

from mat_plan import PLAN
_planned = sorted(i for st in PLAN for i in st["ids"])
if _planned != sorted(t["id"] for t in topics):
    sys.exit("roadmap and topics disagree: " + str(set(_planned) ^ {t["id"] for t in topics}))
for t in topics:
    t["mins"] = max(5, int(round((6 + 0.9 * len(t["blocks"]) + 1.2 * len(t["test"])) / 5.0)) * 5)

# ---- shuffle options (seeded) so the right answer is not predictable by position ----
import random
_rng = random.Random(20261023)
for t in topics:
    for q in t["test"]:
        right = q["o"][q["a"]]
        _rng.shuffle(q["o"])
        q["a"] = q["o"].index(right)

# ---- checks ----
errs = []
ids = [t["id"] for t in topics]
if len(set(ids)) != len(ids):
    errs.append("duplicate topic ids")
seed = json.loads(html.split('<script type="application/json" id="seed">')[1].split("</script>")[0])["sql"]
nrun = 0
for t in topics:
    for i, q in enumerate(t["test"]):
        if len(q["o"]) != 4 or not 0 <= q["a"] < 4 or len(set(q["o"])) != 4:
            errs.append(f"{t['id']} test {i + 1}: bad options")
    for j, b in enumerate(t["blocks"]):
        if b["k"] == "code" and b.get("run"):
            nrun += 1
            con = sqlite3.connect(":memory:")
            try:
                con.executescript(seed)
                con.executescript(b["code"])
            except Exception as e:
                errs.append(f"{t['id']} block {j}: {e}\n{b['code'][:200]}")
            con.close()
if errs:
    sys.exit("\n".join(errs))

import mat_quiz, mat_write_q, mat_write_d
WRITE = mat_write_q.build() + mat_write_d.build()
_wids = [t["id"] for t in WRITE]
if len(set(_wids)) != len(_wids):
    sys.exit("duplicate write-task ids")
for t in WRITE:
    if t["kind"] == "query":
        con = sqlite3.connect(":memory:")
        con.executescript(seed if t["db"] == "co" else mat_write_q.SHOP_SQL)
        try:
            if t.get("verify"):
                try:
                    before = con.execute(t["verify"]).fetchall()
                except Exception:
                    before = None  # the task creates the table itself
                con.executescript(t["ref"])
                after = con.execute(t["verify"]).fetchall()
                if before == after:
                    errs.append(f"{t['id']}: reference changes nothing")
            else:
                rows = con.execute(t["ref"]).fetchall()
                if not rows:
                    errs.append(f"{t['id']}: reference returns no rows")
        except Exception as e:
            errs.append(f"{t['id']}: reference fails: {e}")
        con.close()
    elif t["kind"] == "ddl":
        for c in t["checks"]:
            con = sqlite3.connect(":memory:")
            try:
                if t["pre"]:
                    con.executescript(t["pre"])
                con.executescript(t["ref"])
                con.execute("PRAGMA foreign_keys = ON")
                if c["setup"]:
                    con.executescript(c["setup"])
                try:
                    con.executescript(c["sql"]); ran = True
                except Exception:
                    ran = False
                if ran != c["ok"]:
                    errs.append(f"{t['id']}: check '{c['label']}' disagrees with the reference")
                elif c["after"] and str(con.execute(c["after"]).fetchone()[0]) != c["expect"]:
                    errs.append(f"{t['id']}: check '{c['label']}' after-value disagrees")
            except Exception as e:
                errs.append(f"{t['id']}: check '{c['label']}' setup failed: {e}")
            con.close()
if errs:
    sys.exit("\n".join(errs))
BANK = mat_quiz.build(seed)
for q in BANK:
    if len(q["o"]) != 4 or len(set(q["o"])) != 4 or not 0 <= q["a"] < 4:
        sys.exit("bad quiz question: " + q["q"][:80])
mat = json.dumps({"topics": topics, "plan": PLAN, "bank": BANK, "write": {"tasks": WRITE, "shopSql": mat_write_q.SHOP_SQL, "shopTables": mat_write_q.SHOP_TABLES}}, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
css = open(os.path.join(HERE, "sqlstudy.css"), encoding="utf8").read()
js = open(os.path.join(HERE, "sqlstudy.js"), encoding="utf8").read() + open(os.path.join(HERE, "sqlquiz.js"), encoding="utf8").read() + open(os.path.join(HERE, "sqlwrite.js"), encoding="utf8").read()


def sub(s, old, new, count=1):
    if s.count(old) != count:
        sys.exit(f"patch point not found {count}x: {old[:70]!r} (found {s.count(old)})")
    return s.replace(old, new)


html = sub(html, "</style>", css + "</style>")
html = sub(html, '<script type="application/json" id="state">',
           '<script type="application/json" id="mat">' + mat + '</script>\n\n<script type="application/json" id="state">')
html = sub(html, 'var EX = JSON.parse(document.getElementById("ex").textContent);',
           'var EX = JSON.parse(document.getElementById("ex").textContent);\n  var MAT = JSON.parse(document.getElementById("mat").textContent);')
html = sub(html, "if (!s.drafts) s.drafts = {};", "if (!s.drafts) s.drafts = {};\n    if (!s.study) s.study = {};\n    if (!s.read) s.read = {};\n    if (!s.quiz) s.quiz = {};\n    if (!s.quiz.hist) s.quiz.hist = [];\n    if (!s.quiz.miss) s.quiz.miss = {};\n    if (!s.quiz.seen) s.quiz.seen = {};\n    if (!s.wr) s.wr = {};\n    if (!s.wr.done) s.wr.done = {};\n    if (!s.wr.paper) s.wr.paper = {};\n    if (!s.wr.drafts) s.wr.drafts = {};\n    if (!s.wr.tries) s.wr.tries = {};")
html = sub(html, "o + ' type=\"application/json\" id=\"ex\">' + JSON.stringify(EX) + c + '\\n' +",
           "o + ' type=\"application/json\" id=\"ex\">' + JSON.stringify(EX) + c + '\\n' +\n        o + ' type=\"application/json\" id=\"mat\">' + JSON.stringify(MAT) + c + '\\n' +")
html = sub(html, "db = new SQL.Database();\n        db.run(SEED.sql);",
           "SQLmod = SQL;\n        db = new SQL.Database();\n        db.run(SEED.sql);\n        seedBytes = db.export();")
html = sub(html, '"all exercises"', '"home"')
html = sub(html, "    f.appendChild(hero);\n\n    if (engine === \"failed\")", "    f.appendChild(hero);\n    f.appendChild(studyCard());\n\n    if (engine === \"failed\")")
html = sub(html, "  function open(id, preset) {", js + "  function open(id, preset) {")
html = sub(html, 'app.appendChild(V.screen === "home" ? home() : exScreen());',
           'app.appendChild(V.screen === "home" ? home() : V.screen === "study" ? studyHome() : V.screen === "topic" ? topicScreen() : V.screen === "quiz" ? quizScreen() : V.screen === "write" ? writeHome() : V.screen === "wtask" ? wTaskScreen() : exScreen());')
html = sub(html, "<title>SQL Lab</title>", "<title>SQL Lab</title>")
open(PAGE, "w", encoding="utf8").write(html)

nq = sum(len(t["test"]) for t in topics) + len(BANK)
print(f"{len(WRITE)} write-it tasks: {sum(t['kind'] == 'query' for t in WRITE)} query, {sum(t['kind'] == 'ddl' for t in WRITE)} create-table, {sum(t['kind'] == 'paper' for t in WRITE)} paper")
import collections
pos = collections.Counter(q["a"] for t in topics for q in t["test"])
print("answer positions:", dict(sorted(pos.items())))
print(f"{len(topics)} topics, {nq} test questions, {nrun} runnable blocks verified; {len(html) // 1024} KB")
