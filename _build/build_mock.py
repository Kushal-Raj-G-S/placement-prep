# -*- coding: utf-8 -*-
"""
Builds "10 - Mock OA (timed exam).html" from the scenario questions (sc_*.py).

    python build_mock.py

The page asks you to READ a long scenario, find the clues, and name the pattern and the variant. Nothing is coded
and nothing is judged by running anything. The reveal highlights the clue phrases inside the story, strikes the
decoys, lists the hard words, and links to the matching Learn page.
"""
import json, os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)   # the materials folder (this file lives in _build/)
sys.path.insert(0, HERE)
import pattern_library as PL
import sc_check

TARGET = os.path.join(ROOT, "10 - Mock OA (timed exam).html")

TEMPLATE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Mock OA</title>
<style>
:root{--bg:#070B11;--bg2:#0C121B;--panel:#121A26;--panel2:#182231;--edge:#1E2A3A;--edge2:#2A3A4E;--txt:#E8EEF6;
--dim:#8397AE;--dim2:#5B6E85;--cy:#3FD9EC;--cy-dim:#12333D;--ok:#4BE08B;--ok-dim:#0E2C1D;--no:#FF7A6B;--no-dim:#331612;
--am:#FFC44D;--am-dim:#332714;--vi:#B98CF0;--vi-dim:#241A38;
--mono:ui-monospace,Menlo,Consolas,monospace;--sans:"Segoe UI",system-ui,Arial,sans-serif}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--txt);font-family:var(--sans);font-size:15px;line-height:1.55}
button{font-family:inherit;color:inherit}
.wrap{max-width:900px;margin:0 auto;padding:20px 16px 90px;display:flex;flex-direction:column;gap:14px}
.bar{display:flex;align-items:center;gap:12px;flex-wrap:wrap;padding:11px 14px;background:var(--panel);border:1px solid var(--edge);border-radius:10px}
.logo{font-family:var(--mono);font-weight:700;font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:var(--cy)}
.sp{flex:1 1 auto}.stat{font-family:var(--mono);font-size:12px;color:var(--dim)}.stat b{color:var(--ok);font-size:15px}
.btn{font-family:var(--mono);font-size:11.5px;font-weight:600;letter-spacing:.07em;text-transform:uppercase;background:var(--panel2);
 border:1px solid var(--edge2);border-radius:7px;padding:9px 14px;cursor:pointer}
.btn:hover:not(:disabled){border-color:var(--cy)}.btn:disabled{opacity:.4;cursor:default}
.btn.primary{background:var(--cy);border-color:var(--cy);color:#04222A}.btn.ghost{background:transparent}
.hero,.card{background:var(--panel);border:1px solid var(--edge);border-radius:12px;padding:18px}
.hero h1{margin:0 0 6px;font-family:var(--mono);font-size:clamp(22px,4.5vw,30px)}.hero h1 em{font-style:normal;color:var(--cy)}
.hero p,.lead{color:var(--dim);margin:6px 0}.lab{font-family:var(--mono);font-size:9.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--dim2);margin:12px 0 7px}
.chips{display:flex;gap:7px;flex-wrap:wrap}
.chip{font-family:var(--mono);font-size:12px;background:var(--bg2);border:1px solid var(--edge2);border-radius:7px;padding:8px 12px;cursor:pointer}
.chip:hover{border-color:var(--cy)}.chip.on{background:var(--cy);border-color:var(--cy);color:#04222A;font-weight:600}
.row{display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.qhead{display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.qhead h2{margin:0;font-size:20px}.tag{font-family:var(--mono);font-size:9.5px;letter-spacing:.09em;text-transform:uppercase;border:1px solid var(--edge2);border-radius:5px;padding:3px 7px;color:var(--dim)}
.clock{font-family:var(--mono);font-size:20px;font-weight:700;color:var(--cy);font-variant-numeric:tabular-nums}
.clock.warn{color:var(--am)}.clock.crit{color:var(--no)}
.wrap.wide{max-width:1500px}
.split{display:grid;grid-template-columns:minmax(0,6fr) minmax(380px,5fr);gap:16px;align-items:start}
.col{display:flex;flex-direction:column;gap:14px;min-width:0}
.split .col{max-height:calc(100vh - 150px);overflow-y:auto;padding-right:4px}
.split .side textarea{min-height:220px}
@media(max-width:1000px){.split{grid-template-columns:1fr}.split .col{max-height:none;overflow:visible}.split .story-col{order:-1}}
.story{font-size:15.5px;line-height:1.7;max-width:74ch}.story>p{margin:0 0 16px}
.sec{margin:20px 0 0;padding:12px 14px;background:var(--bg2);border:1px solid var(--edge);border-left:3px solid var(--cy);border-radius:8px}
.sec p{margin:0;font-size:14.5px;color:var(--txt)}.sec.constraints{border-left-color:var(--am)}.sec.output{border-left-color:var(--ok)}
.sec.task{border-left-color:var(--vi)}.sec.sample{border-left-color:var(--dim2)}
.sec pre{margin:0 0 10px;padding:8px 10px;background:var(--bg);border:1px solid var(--edge);border-radius:6px;font-family:var(--mono);font-size:13px;white-space:pre-wrap}
.sech{font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--dim);margin-bottom:6px}
mark.clue{background:var(--ok-dim);color:var(--ok);border-bottom:2px solid var(--ok);border-radius:3px;padding:0 2px}
mark.decoy{background:transparent;color:var(--dim2);text-decoration:line-through;text-decoration-color:var(--no)}
.gp{font-family:var(--mono);font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--dim2);margin:12px 0 6px}
.pbtn,.vbtn{font-size:13px;background:var(--bg2);border:1px solid var(--edge);border-radius:8px;padding:8px 11px;cursor:pointer;text-align:left}
.pbtn:hover,.vbtn:hover{border-color:var(--cy)}.pbtn.open{border-color:var(--cy);background:var(--cy-dim)}
.vbtn.sel{background:var(--cy);border-color:var(--cy);color:#04222A;font-weight:600}
.vrow{background:var(--bg2);border:1px solid var(--edge);border-radius:10px;padding:10px;margin-top:8px}
textarea{width:100%;min-height:74px;background:var(--bg2);border:1px solid var(--edge2);border-radius:8px;color:var(--txt);font:inherit;padding:10px;resize:vertical}
textarea:focus{outline:none;border-color:var(--cy)}
.verd{border-radius:10px;padding:12px 14px;border:1px solid}.verd.ok{background:var(--ok-dim);border-color:var(--ok)}
.verd.part{background:var(--am-dim);border-color:var(--am)}.verd.no{background:var(--no-dim);border-color:var(--no)}
.verd b{font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase}
.box{background:var(--bg2);border:1px solid var(--edge);border-left:3px solid var(--am);border-radius:8px;padding:10px 12px;margin-top:8px;font-size:14px}
.box i{display:block;font-style:normal;font-family:var(--mono);font-size:9.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--am);margin-bottom:3px}
.gl{display:grid;grid-template-columns:auto 1fr;gap:4px 14px;font-size:14px}.gl dt{font-family:var(--mono);color:var(--cy)}.gl dd{margin:0;color:var(--dim)}
a.lnk{color:var(--cy)}.res{padding:12px 0;border-bottom:1px solid var(--edge)}.res:last-child{border:0}
.small{font-size:12.5px;color:var(--dim)}.hide{display:none}
@media(max-width:620px){.wrap{padding:12px 10px 80px}}
</style></head><body><div class="wrap" id="app"></div>
<script type="application/json" id="data">__DATA__</script>
<script>
(function () {
"use strict";
var D = JSON.parse(document.getElementById("data").textContent);
var Q = D.questions, PATS = D.patterns, VNAME = {}, VPAT = {}, PNAME = {};
PATS.forEach(function (p) { PNAME[p.id] = p.name; p.variants.forEach(function (v) { VNAME[v.id] = v.name; VPAT[v.id] = p.id; }); });
var LS = "mock-oa-v2";
var ST = { rev: 0, seen: {}, vstat: {}, words: {}, hist: [] };
try { var raw = localStorage.getItem(LS); if (raw) { var o = JSON.parse(raw); for (var k in ST) if (o[k] != null) ST[k] = o[k]; } } catch (e) {}
function save() { ST.rev++; try { localStorage.setItem(LS, JSON.stringify(ST)); } catch (e) {} }

var app = document.getElementById("app");
function el(t, c, x) { var n = document.createElement(t); if (c) n.className = c; if (x != null) n.textContent = x; return n; }
var V = { screen: "setup", cfg: { n: 5, mins: 12, mode: "practice", focus: "unseen" }, run: null, at: 0, open: null, tid: null };

function shuffle(a) { var r = a.slice(); for (var i = r.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = r[i]; r[i] = r[j]; r[j] = t; } return r; }
function pick(cfg) {
  var pool = Q.slice();
  if (cfg.focus === "unseen") pool.sort(function (a, b) { return (ST.seen[a.id] || 0) - (ST.seen[b.id] || 0) || Math.random() - .5; });
  else if (cfg.focus === "weak") {
    var acc = function (q) { var s = ST.vstat[q.v]; return s && s.n ? s.ok / s.n : 0.5; };
    pool.sort(function (a, b) { return acc(a) - acc(b) || Math.random() - .5; });
  } else pool = shuffle(pool);
  var n = cfg.n === "all" ? pool.length : Math.min(cfg.n, pool.length);
  return shuffle(pool.slice(0, n));
}
function fmt(s) { s = Math.max(0, Math.floor(s)); var m = Math.floor(s / 60), x = s % 60; return m + ":" + (x < 10 ? "0" : "") + x; }

/* ---- the coach: the model reads what you typed, judges it, and nudges you toward what you missed.
        It runs on the hub's server, so the API key never reaches this page. Opened without the hub,
        or with no key in .env, the page still works: you read the reveal and mark yourself. ---- */
var COACH = { on: false, why: "open this page from the hub (python app.py) to use the coach" };
function coachStatus() {
  try {
    fetch("/api/coach").then(function (r) { return r.json(); }).then(function (d) {
      COACH = { on: !!d.on, model: d.model, why: d.why };
      if (V.screen === "quiz") renderKeep();
    }).catch(function () {});
  } catch (e) {}
}
function askCoach(it, message, teach) {
  it.busy = true; it.cerr = null; it.t0 = Date.now(); renderKeep();
  var body = { qid: it.q.id, answer: it.ans, hints: it.hints || 0, verdict: it.cv || null, message: message || null, teach: !!teach };
  fetch("/api/coach", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) })
    .then(function (r) { return r.json(); })
    .then(function (d) {
      it.busy = false; it.log = it.log || [];
      if (message) it.log.push({ who: "me", text: message });
      if (d.verdict) it.cv = d.verdict;
      if (d.reply) it.log.push({ who: "coach", text: d.reply, v: teach ? null : (d.verdict || it.cv), fallback: !teach && d.source !== "model", teach: !!teach });
      if (teach && d.ok) it.taught = true;
      it.cerr = d.ok ? null : (d.error || "the coach is unavailable");
      it.hints = (it.hints || 0) + 1;
      save(); renderKeep();
    })
    .catch(function () { it.busy = false; it.cerr = "could not reach the coach - is the hub still running?"; renderKeep(); });
}

var VLAB = { right: "that is it", close: "right neighbourhood", wrong: "not this one", unclear: "not enough to judge" };
var VCLS = { right: "ok", close: "part", wrong: "no", unclear: "" };

/* ---- grading: the coach's verdict, which you can overrule on the reveal if you disagree ---- */
function grade(q, it) {
  if (it.ovr != null) return { pts: it.ovr, kind: it.ovr === 1 ? "ok" : it.ovr === 0.5 ? "pattern" : "no" };
  if (it.taught) return { pts: 0, kind: "taught" };
  if (it.cv === "right") return { pts: 1, kind: "ok" };
  if (it.cv === "close") return { pts: 0.5, kind: "pattern" };
  if (it.cv === "wrong") return { pts: 0, kind: "no" };
  if (it.cv === "unclear") return { pts: 0, kind: "unclear" };
  return { pts: 0, kind: (it.ans || "").trim() ? "ungraded" : "none" };
}

/* ---- highlight clue / decoy phrases inside the story without ever using innerHTML ---- */
/* ---- the story, laid out like a HackerRank statement: short paragraphs, then Input Format / Output Format /
        Constraints as their own labelled blocks. `marked` adds the green clue / struck-through decoy marks. ---- */
var SECS = { "Input:": "Input Format", "Output:": "Output Format", "Constraints:": "Constraints" };
function paintStory(q, marked) {
  var story = q.story, marks = [];
  if (marked) {
    (q.clues || []).forEach(function (p) { var i = story.indexOf(p); if (i >= 0) marks.push([i, i + p.length, "clue"]); });
    (q.decoys || []).forEach(function (p) { var i = story.indexOf(p); if (i >= 0) marks.push([i, i + p.length, "decoy"]); });
    marks.sort(function (a, b) { return a[0] - b[0]; });
  }
  var box = el("div", "story"), off = 0, taskShown = false;
  story.split("\n\n").forEach(function (para) {
    var start = off, end = off + para.length; off = end + 2;
    if (!taskShown && para.indexOf("Input:") === 0 && q.task) { taskShown = true; box.appendChild(taskBox(q)); }
    var label = null, key = Object.keys(SECS).filter(function (k) { return para.indexOf(k) === 0; })[0];
    var host;
    if (key) { label = SECS[key]; start += key.length; while (story.charAt(start) === " ") start++;
      host = el("div", "sec " + label.split(" ")[0].toLowerCase()); host.appendChild(el("div", "sech", label)); }
    else host = box;
    var p = el("p"), pos = start;
    marks.forEach(function (m) {
      if (m[0] < pos || m[1] > end) return;
      p.appendChild(document.createTextNode(story.slice(pos, m[0])));
      p.appendChild(el("mark", m[2], story.slice(m[0], m[1])));
      pos = m[1];
    });
    p.appendChild(document.createTextNode(story.slice(pos, end)));
    if (key && p.firstChild && !marks.length) p.firstChild.textContent = p.firstChild.textContent.charAt(0).toUpperCase() + p.firstChild.textContent.slice(1);
    host.appendChild(p);
    if (key) box.appendChild(host);
  });
  if (!taskShown && q.task) box.appendChild(taskBox(q));
  if (q.sample) box.appendChild(sampleBox(q.sample));
  return box;
}
function taskBox(q) {
  var h = el("div", "sec task"); h.appendChild(el("div", "sech", "Your task")); h.appendChild(el("p", null, q.task)); return h;
}
function sampleBox(sm) {
  var h = el("div", "sec sample");
  h.appendChild(el("div", "sech", "Sample Input")); var a = el("pre", null, sm["in"]); h.appendChild(a);
  h.appendChild(el("div", "sech", "Sample Output")); var b = el("pre", null, sm.out || " "); h.appendChild(b);
  h.appendChild(el("div", "sech", "Explanation")); h.appendChild(el("p", null, sm.why));
  return h;
}
function highlighted(q) { return paintStory(q, true); }
function plainStory(q) { return paintStory(q, false); }

function bar() {
  var b = el("div", "bar"); b.appendChild(el("div", "logo", "mock_oa")); b.appendChild(el("div", "sp"));
  var done = ST.hist.length, s = el("div", "stat"); s.appendChild(document.createTextNode(Q.length + " scenarios · " + done + " sittings"));
  b.appendChild(s);
  if (V.screen !== "setup") { var m = el("button", "btn ghost", "menu"); m.type = "button"; m.onclick = function () { stopT(); V.screen = "setup"; render(); }; b.appendChild(m); }
  return b;
}

/* ---------------- setup ---------------- */
function chipRow(host, vals, key, labels) {
  vals.forEach(function (v, i) {
    var c = el("button", "chip" + (V.cfg[key] === v ? " on" : ""), labels ? labels[i] : String(v)); c.type = "button";
    c.onclick = function () { V.cfg[key] = v; render(); }; host.appendChild(c);
  });
}
function setup() {
  var f = document.createDocumentFragment(), h = el("div", "hero");
  var h1 = el("h1"); h1.innerHTML = "Read the story.<br>Find the <em>clues</em>."; h.appendChild(h1);
  h.appendChild(el("p", null, "Real assessments hide a pattern you already know under unfamiliar words. Each scenario here is written in that voice. " +
    "Read it, then type the pattern and the variant in your own words and say which words pushed you. There are no options to pick from and nothing is coded. The reveal highlights the clues you were meant to find."));
  f.appendChild(h);
  var c = el("div", "card");
  c.appendChild(el("div", "lab", "how many scenarios")); var r1 = el("div", "chips"); chipRow(r1, [3, 5, 10, 15, "all"], "n", ["3", "5", "10", "15", "all"]); c.appendChild(r1);
  c.appendChild(el("div", "lab", "minutes per scenario")); var r2 = el("div", "chips"); chipRow(r2, [5, 8, 12, 20, 0], "mins", ["5", "8", "12", "20", "no limit"]); c.appendChild(r2);
  c.appendChild(el("div", "lab", "mode")); var r3 = el("div", "chips"); chipRow(r3, ["practice", "exam"], "mode", ["practice: reveal after each", "exam: reveal at the end, hard lock"]); c.appendChild(r3);
  c.appendChild(el("div", "lab", "which scenarios")); var r4 = el("div", "chips"); chipRow(r4, ["unseen", "weak", "random"], "focus", ["unseen first", "my weak variants", "random"]); c.appendChild(r4);
  var go = el("button", "btn primary", "begin"); go.type = "button"; go.style.marginTop = "16px";
  go.onclick = function () { V.run = pick(V.cfg).map(function (q) { return { q: q, ans: "", cv: null, hints: 0, log: [], secs: 0, done: false }; }); V.at = 0; V.screen = "quiz"; V.open = null; startT(); render(); };
  c.appendChild(go); f.appendChild(c);
  var wl = Object.keys(ST.words);
  if (wl.length) {
    var w = el("div", "card"); w.appendChild(el("div", "lab", "hard words you have met and missed (" + wl.length + ")"));
    var dl = el("dl", "gl");
    wl.slice(-14).reverse().forEach(function (k) { dl.appendChild(el("dt", null, k)); dl.appendChild(el("dd", null, ST.words[k].meaning)); });
    w.appendChild(dl); f.appendChild(w);
  }
  return f;
}

/* ---------------- timer ---------------- */
var t0 = 0;
function stopT() { if (V.tid) { clearInterval(V.tid); V.tid = null; } }
function startT() {
  stopT(); t0 = Date.now();
  V.tid = setInterval(function () {
    if (V.screen !== "quiz" || !V.run) return;
    var it = V.run[V.at], used = it.secs + (Date.now() - t0) / 1000, lim = V.cfg.mins * 60;
    var ck = document.getElementById("clock");
    if (ck) {
      if (lim) { var rem = lim - used; ck.textContent = fmt(rem); ck.className = "clock" + (rem <= 30 ? " crit" : rem <= 90 ? " warn" : ""); }
      else ck.textContent = fmt(used);
    }
    if (lim && used >= lim) submit(true);
  }, 500);
}

/* ---------------- quiz ---------------- */
function quiz() {
  var it = V.run[V.at], q = it.q, f = document.createDocumentFragment();
  var head = el("div", "qhead"); head.appendChild(el("h2", null, q.title));
  head.appendChild(el("span", "tag", q.diff === "E" ? "easy" : q.diff === "H" ? "hard" : "medium"));
  head.appendChild(el("span", "tag", (V.at + 1) + " / " + V.run.length)); head.appendChild(el("div", "sp"));
  var ck = el("div", "clock", V.cfg.mins ? fmt(V.cfg.mins * 60) : "0:00"); ck.id = "clock"; head.appendChild(ck);
  f.appendChild(head);
  var split = el("div", "split"), story = el("div", "col story-col"), side = el("div", "col side");
  var c = el("div", "card"); c.appendChild(plainStory(q)); story.appendChild(c);

  var pk = el("div", "card");
  pk.appendChild(el("div", "lab", "your answer, in your own words"));
  pk.appendChild(el("div", "small", "Write 3 short things, in plain words: (1) what must come out at the end, "
    + "(2) which words in the story told you what kind of problem it is, (3) what you would do with the data to get it. "
    + "No technical name is needed."));
  var ta = document.createElement("textarea"); ta.value = it.ans || ""; ta.spellcheck = false;
  ta.style.minHeight = "150px"; ta.style.marginTop = "8px";
  ta.placeholder = "e.g. it wants the longest run of barrels standing next to each other with no more than three kinds of grape, "
    + "so I would stretch a run to the right while it is still allowed and pull the back end forward when it breaks, remembering the biggest length";
  var ask = el("button", "btn primary", "check my answer");
  function sync() { it.ans = ta.value; ask.disabled = !ta.value.trim() || !!it.busy || !COACH.on; }
  ta.oninput = sync; pk.appendChild(ta);

  var row = el("div", "row"); row.style.marginTop = "12px";
  ask.type = "button"; ask.onclick = function () { askCoach(it, null); };
  if (!COACH.on) ask.textContent = "coach unavailable";
  var rv = el("button", "btn", "show me the answer"); rv.type = "button"; rv.onclick = function () { submit(false); };
  var sk = el("button", "btn ghost", "skip"); sk.type = "button"; sk.onclick = function () { it.ans = ""; it.cv = null; submit(false); };
  row.appendChild(ask); row.appendChild(rv); row.appendChild(sk); pk.appendChild(row);
  if (!COACH.on) pk.appendChild(el("div", "small", COACH.why || "the coach is off - read the reveal and mark yourself"));
  sync();
  side.appendChild(pk);
  if ((it.log || []).length || it.busy || it.cerr) side.appendChild(coachPanel(it));
  split.appendChild(story); split.appendChild(side); f.appendChild(split);
  return f;
}

/* ---- the conversation with the coach, under the answer box ---- */
function coachPanel(it) {
  var c = el("div", "card");
  c.appendChild(el("div", "lab", "the coach"));
  (it.log || []).forEach(function (m, i) {
    if (m.who === "me") {
      var y = el("div", "box"); y.style.borderLeftColor = "var(--dim2)";
      y.appendChild(el("i", null, "you")); y.appendChild(document.createTextNode(m.text)); c.appendChild(y);
      return;
    }
    if (i === it.log.length - 1 && m.v) {
      var vd = el("div", "verd " + (VCLS[m.v] || "")); vd.style.marginBottom = "8px";
      vd.appendChild(el("b", null, VLAB[m.v] || m.v));
      var note = m.v === "right" ? "A full point for this one. Open the answer when you want to compare your reading against the clues."
        : m.v === "close" ? "Half a point as it stands. Rewrite your answer above and check again to go for the full point."
        : "Rewrite your answer above and check again, or write back to the coach below.";
      vd.appendChild(el("div", null, note));
      c.appendChild(vd);
    }
    var b = el("div", "box"); b.appendChild(el("i", null, m.teach ? "coach - the full explanation" : "coach"));
    if (m.teach) b.style.borderLeftColor = "var(--ok)";
    b.appendChild(document.createTextNode(m.text));
    if (m.fallback) b.appendChild(el("div", "small", "(a standard hint: the AI's first reply would have given the answer away, so this safe one was used)"));
    c.appendChild(b);
  });
  if (it.busy) {
    var w = el("div", "box"); w.appendChild(el("i", null, "coach"));
    w.appendChild(document.createTextNode("reading your answer against the story. "));
    var tick = el("span", null, "0s"); w.appendChild(tick);
    w.appendChild(el("div", "small", "Usually 15 to 40 seconds; longer if the first reply gave too much away and has to be asked again."));
    var t0 = it.t0 || Date.now();
    var iv = setInterval(function () {
      if (!it.busy || !tick.isConnected) { clearInterval(iv); return; }
      tick.textContent = Math.round((Date.now() - t0) / 1000) + "s";
    }, 1000);
    c.appendChild(w);
  }
  if (it.cerr) {
    var e = el("div", "box"); e.style.borderLeftColor = "var(--no)";
    e.appendChild(el("i", null, "coach unavailable")); e.appendChild(document.createTextNode(it.cerr));
    e.appendChild(el("div", "small", "You can still open the answer and mark yourself."));
    c.appendChild(e);
  }
  if (!it.busy && !it.taught && (it.hints || 0) >= 3) {
    var tb = el("button", "btn", "I still cannot see it - teach me"); tb.type = "button"; tb.style.margin = "6px 0 10px";
    tb.onclick = function () { askCoach(it, null, true); }; c.appendChild(tb);
    c.appendChild(el("div", "small", "This gives the full explanation, so the question will not score."));
  }
  if (!it.busy && !it.taught && (it.log || []).length) {
    c.appendChild(el("div", "lab", "write back, or ask for another nudge"));
    var mi = document.createElement("input"); mi.type = "text"; mi.autocomplete = "off";
    mi.placeholder = "e.g. the second sentence says the run cannot skip any barrel, so does that rule out what I said?";
    mi.style.cssText = "width:100%;background:var(--bg2);border:1px solid var(--edge2);border-radius:8px;color:var(--txt);font:inherit;padding:11px 12px";
    var send = el("button", "btn", "send"); send.type = "button"; send.style.marginTop = "10px";
    send.onclick = function () { var t = mi.value.trim(); if (t) askCoach(it, t); };
    mi.onkeydown = function (ev) { if (ev.key === "Enter") send.onclick(); };
    c.appendChild(mi); c.appendChild(send);
  }
  return c;
}

function renderKeep() { var y = window.scrollY; render(); window.scrollTo(0, y); }

function submit(timedOut) {
  var it = V.run[V.at]; it.secs += (Date.now() - t0) / 1000; it.done = true; it.timedOut = !!timedOut;
  ST.seen[it.q.id] = (ST.seen[it.q.id] || 0) + 1;
  var g = grade(it.q, it); it.gpts = g.pts; var vs = ST.vstat[it.q.v] || { n: 0, ok: 0 };
  vs.n++; vs.ok += g.pts; ST.vstat[it.q.v] = vs;
  if (g.pts < 1) (it.q.gloss || []).forEach(function (w) { ST.words[w[0]] = { meaning: w[1] }; });
  save();
  if (V.cfg.mode === "practice") { stopT(); V.screen = "reveal1"; render(); }
  else advance();
}
function advance() {
  if (V.at + 1 >= V.run.length) { finish(); return; }
  V.at++; V.open = null; startT(); V.screen = "quiz"; render();
}
function finish() {
  stopT();
  var pts = 0; V.run.forEach(function (it) { pts += grade(it.q, it).pts; });
  ST.hist.push({ when: Date.now(), n: V.run.length, pts: pts, mode: V.cfg.mode }); save();
  V.screen = "result"; render();
}

/* ---------------- reveal ---------------- */
function learnHref(vid) { return "./8%20-%20Pattern%20Radar%20%28name%20the%20pattern%29.html#p=" + VPAT[vid] + "&v=" + vid; }
function reveal(it) {
  var q = it.q, g = grade(q, it), f = document.createElement("div"); f.style.display = "flex"; f.style.flexDirection = "column"; f.style.gap = "12px";
  var vd = el("div", "verd " + (g.kind === "ok" || g.kind === "alt" ? "ok" : g.kind === "pattern" ? "part" : "no"));
  var vt = { ok: "right", alt: "also valid", pattern: "half - the right neighbourhood", no: "not this one", none: "skipped", taught: "the coach taught this one", unclear: "not enough to judge", ungraded: "not checked - mark yourself" }[g.kind];
  vd.appendChild(el("b", null, vt));
  var line = el("div"); line.style.marginTop = "4px";
  line.textContent = "Answer: " + VNAME[q.v] + "  (" + PNAME[VPAT[q.v]] + ")";
  vd.appendChild(line);
  if ((it.ans || "").trim()) { var ya = el("div", "box"); ya.style.borderLeftColor = "var(--dim2)";
    ya.appendChild(el("i", null, "what you wrote")); ya.appendChild(document.createTextNode(it.ans.trim())); f.appendChild(ya); }
  var ov = el("div", "small"); ov.style.marginTop = "8px"; ov.appendChild(document.createTextNode("Disagree with the coach, or it never ran? Mark yourself:  "));
  [["right", 1], ["pattern only", 0.5], ["wrong", 0]].forEach(function (o) {
    var b = el("button", "btn ghost", o[0]); b.type = "button"; b.style.cssText = "padding:4px 8px;margin-right:6px";
    b.onclick = function () {
      var vs = ST.vstat[q.v] || { n: 0, ok: 0 }; vs.ok += o[1] - (it.gpts != null ? it.gpts : g.pts); ST.vstat[q.v] = vs;
      it.gpts = o[1]; it.ovr = o[1]; save(); var host = vd.parentNode; host.replaceWith(reveal(it));
    };
    ov.appendChild(b);
  });
  vd.appendChild(ov); f.appendChild(vd);
  var c = el("div", "card"); c.appendChild(el("div", "lab", "the story, with the clues marked")); c.appendChild(highlighted(q));
  c.appendChild(el("div", "small", "green = the clues you were meant to find.  struck through = flavour that changes nothing.")); f.appendChild(c);
  var b1 = el("div", "box"); b1.appendChild(el("i", null, "strip the story down")); b1.appendChild(document.createTextNode(q.core)); f.appendChild(b1);
  var b2 = el("div", "box"); b2.appendChild(el("i", null, "what the clues add up to")); b2.appendChild(document.createTextNode(q.tell)); f.appendChild(b2);
  if (q.why && Object.keys(q.why).length) {
    var b3 = el("div", "box"); b3.appendChild(el("i", null, "the neighbours that tempt, and why they are not it"));
    Object.keys(q.why).forEach(function (k) {
      var d = el("div"); d.style.marginTop = "4px";
      d.appendChild(el("b", null, (VNAME[k] || k) + ": ")); d.appendChild(document.createTextNode(q.why[k]));
      b3.appendChild(d);
    });
    f.appendChild(b3);
  }
  if ((q.alt || []).length) { var b4 = el("div", "box"); b4.appendChild(el("i", null, "also valid")); b4.appendChild(document.createTextNode(q.alt.map(function (a) { return VNAME[a]; }).join(", "))); f.appendChild(b4); }
  if ((q.gloss || []).length) {
    var gc = el("div", "card"); gc.appendChild(el("div", "lab", "the hard words"));
    var dl = el("dl", "gl");
    q.gloss.forEach(function (w) { dl.appendChild(el("dt", null, w[0])); dl.appendChild(el("dd", null, w[1] + (w[2] ? "" : "   (this word was itself a clue)"))); });
    gc.appendChild(dl); f.appendChild(gc);
  }
  var lk = el("a", "lnk", "Open the Learn page and the trace for: " + VNAME[q.v]); lk.href = learnHref(q.v); lk.target = "_blank"; lk.rel = "noopener";
  f.appendChild(lk);
  return f;
}
function reveal1() {
  var it = V.run[V.at], f = document.createDocumentFragment();
  f.appendChild(reveal(it));
  var nx = el("button", "btn primary", V.at + 1 >= V.run.length ? "finish" : "next scenario"); nx.type = "button"; nx.style.alignSelf = "flex-start";
  nx.onclick = advance; f.appendChild(nx);
  return f;
}

/* ---------------- result ---------------- */
function result() {
  var f = document.createDocumentFragment(), pts = 0;
  V.run.forEach(function (it) { pts += grade(it.q, it).pts; });
  var h = el("div", "hero"); var h1 = el("h1"); h1.textContent = pts + " / " + V.run.length; h.appendChild(h1);
  h.appendChild(el("p", null, "A full point for the right variant, half for the right pattern. Open each scenario to see which words you were meant to catch."));
  f.appendChild(h);
  var c = el("div", "card");
  V.run.forEach(function (it, i) {
    var g = grade(it.q, it), row = el("div", "res");
    var d = document.createElement("details"), s = document.createElement("summary"); s.style.cursor = "pointer";
    s.textContent = (i + 1) + ". " + it.q.title + "   [" + (g.pts === 1 ? "right" : g.pts === 0.5 ? "pattern only" : "missed") + "]";
    d.appendChild(s); var lazy = false;
    d.addEventListener("toggle", function () { if (d.open && !lazy) { lazy = true; d.appendChild(reveal(it)); } });
    row.appendChild(d); c.appendChild(row);
  });
  f.appendChild(c);
  var cp = el("button", "btn", "copy my answers"); cp.type = "button"; cp.style.alignSelf = "flex-start";
  cp.onclick = function () {
    var t = V.run.map(function (it, i) { return (i + 1) + ". " + it.q.title + " | I wrote: " + (it.ans || "-") + " | answer: " + VNAME[it.q.v] + ""; }).join("\n");
    try { navigator.clipboard.writeText(t); cp.textContent = "copied"; } catch (e) { cp.textContent = "copy failed"; }
  };
  f.appendChild(cp);
  var again = el("button", "btn primary", "new sitting"); again.type = "button"; again.style.alignSelf = "flex-start"; again.onclick = function () { V.screen = "setup"; render(); };
  f.appendChild(again);
  return f;
}

function render() {
  app.textContent = ""; app.className = "wrap" + (V.screen === "quiz" ? " wide" : ""); app.appendChild(bar());
  if (V.screen === "setup") app.appendChild(setup());
  else if (V.screen === "quiz") app.appendChild(quiz());
  else if (V.screen === "reveal1") app.appendChild(reveal1());
  else app.appendChild(result());
}
coachStatus();
render();
})();
</script></body></html>
"""


def main():
    errs, warns = sc_check.check(sc_check.load())
    if errs:
        for e in errs[:30]:
            print("ERROR:", e)
        sys.exit("The scenario questions have errors; nothing was built.")
    qs = sc_check.load()
    clean = [{k: v for k, v in q.items() if not k.startswith("_")} for q in qs]
    import re as _re, tasks as _T
    for q in clean:
        t = _T.TASKS.get(q["id"])
        if not t: sys.exit("no task/sample for " + q["id"])
        q["task"], q["sample"] = t[0], {"in": t[1], "out": t[2], "why": t[3]}
    for q in clean:                        # Input and Output often share a paragraph: give each its own block
        q["story"] = q["story"].replace(" Output:", chr(10) * 2 + "Output:")
        for ph in q.get("clues", []) + q.get("decoys", []):
            assert ph in q["story"], ("a clue spans the Input/Output split", q["id"], ph)
    patterns = []
    for p in PL.PATTERNS:
        g = [x for x in PL.GROUPS if x["id"] == p["group"]][0]
        patterns.append({"id": p["id"], "name": p["name"], "group": p["group"], "groupName": g["name"],
                         "variants": [{"id": v["id"], "name": v["name"]} for v in p["variants"]]})
    data = json.dumps({"questions": clean, "patterns": patterns}, ensure_ascii=False, separators=(",", ":"))
    if "</script>" in data:
        sys.exit("data contains </script>")
    html = TEMPLATE.replace("__DATA__", data)
    open(TARGET, "w", encoding="utf-8").write(html)
    cov = len({q["v"] for q in clean})
    print("built Mock OA: %d scenarios, %d of 78 variants covered, %.0f KB" % (len(clean), cov, os.path.getsize(TARGET) / 1024))


if __name__ == "__main__":
    main()
