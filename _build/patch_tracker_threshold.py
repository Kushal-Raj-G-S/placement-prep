# -*- coding: utf-8 -*-
"""Teach the tracker page about threshold sets (flags written by make_thresholds.py). Idempotent."""
import io, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "1 - Twenty Weeks to AC (tracker).html")
h = io.open(P, encoding="utf-8").read()
if "/*TH*/" in h:
    print("already patched")
    raise SystemExit

def sub(a, b):
    global h
    assert h.count(a) == 1, (h.count(a), a[:70])
    h = h.replace(a, b, 1)

# 1. next up: stay inside the threshold sets first. Only when every threshold set is done does it hand out extra practice.
sub("""  function nextUp() {
    for (var i = 0; i < BLOCKS.length; i++) {
      var b = BLOCKS[i];
      if (ui.coreOnly && !b.core) continue;
      for (var j = 0; j < b.items.length; j++) if (st(key(b, j)) !== "ac") return { b: b, i: j, it: b.items[j], k: key(b, j) };
    }
    return null;
  }""", """  /*TH*/
  function thItems(b) {                       // threshold item indexes, in teaching order
    var out = [];
    b.items.forEach(function (it, i) { if (it.th) out.push(i); });
    out.sort(function (x, y) { return b.items[x].to - b.items[y].to; });
    return out;
  }
  function thStats(b) {
    var ix = thItems(b), done = 0;
    ix.forEach(function (i) { if (st(key(b, i)) === "ac") done++; });
    return { done: done, total: ix.length };
  }
  function nextUp() {
    for (var pass = 0; pass < 2; pass++) {    // pass 0: threshold problems only, in plan order. pass 1: everything else.
      for (var i = 0; i < BLOCKS.length; i++) {
        var b = BLOCKS[i];
        if (ui.coreOnly && !b.core) continue;
        var order = pass === 0 ? thItems(b) : b.items.map(function (_, j) { return j; });
        for (var q = 0; q < order.length; q++) { var j = order[q]; if (st(key(b, j)) !== "ac") return { b: b, i: j, it: b.items[j], k: key(b, j), th: pass === 0 }; }
      }
    }
    return null;
  }""")

# 2. the variant a threshold problem teaches
sub("""    row.appendChild(it.u ? link(it.u, it.t) : el("span", "plain", it.t));
    var right = el("div", "right");""", """    row.appendChild(it.u ? link(it.u, it.t) : el("span", "plain", it.t));
    if (it.th && it.v) row.appendChild(el("span", "vtag", it.v));
    var right = el("div", "right");""")

# 3. header pill on the block
sub("""    if (!b.core) nm.appendChild(el("span", "pill opt", "optional"));""", """    if (!b.core) nm.appendChild(el("span", "pill opt", "optional"));
    var ts = thStats(b);
    if (ts.total) nm.appendChild(el("span", "pill th" + (ts.done === ts.total ? " ok" : ""), ts.done === ts.total ? "threshold done \\u2713" : "threshold " + ts.done + "/" + ts.total));""")

# 4. the threshold section first, then the extra practice
sub("""    visible.forEach(function (i) { box.appendChild(itemRow(b, i)); });
    node.appendChild(box);""", """    var thVis = thItems(b).filter(function (i) { return visible.indexOf(i) >= 0; });
    var exVis = visible.filter(function (i) { return !b.items[i].th; });
    if (ts.total) {
      var thh = el("div", "th-head" + (ts.done === ts.total ? " ok" : ""));
      thh.appendChild(el("b", null, "Threshold set  " + ts.done + "/" + ts.total));
      thh.appendChild(el("span", null, ts.done === ts.total
        ? "You have met every common variant of this pattern. Move on to the next one."
        : "One or more problems for every common variant. Finish these, then move to the next pattern."));
      box.appendChild(thh);
      thVis.forEach(function (i) { box.appendChild(itemRow(b, i)); });
      if (b.thNote) box.appendChild(el("div", "th-note", b.thNote));
      if (exVis.length) box.appendChild(el("div", "ex-head", "Extra practice (after the threshold)"));
    }
    (ts.total ? exVis : visible).forEach(function (i) { box.appendChild(itemRow(b, i)); });
    node.appendChild(box);""")

# 5. styles
h = h.replace("</style>", """.pill.th{background:#10283a;color:#6fd3ff;border:1px solid #1f5f86}.pill.th.ok{background:#0e2c1d;color:#4be08b;border-color:#1f6b45}
.th-head{display:flex;flex-direction:column;gap:2px;margin:6px 0 4px;padding:9px 12px;background:#0d2230;border:1px solid #1f5f86;border-radius:8px;font-size:13px;color:#cfe6f5}
.th-head.ok{background:#0b2a1b;border-color:#1f6b45}.th-head b{color:#6fd3ff}.th-head.ok b{color:#4be08b}.th-head span{color:#8fb3c8;font-size:12.5px}
.th-note{margin:6px 0 2px;padding:6px 12px;font-size:12px;color:#9aa9b8;border-left:2px solid #33475b}
.ex-head{margin:14px 0 4px;padding:6px 2px;font-family:ui-monospace,Consolas,monospace;font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:#6b7d92;border-top:1px solid #1e2a3a}
.vtag{font-size:11px;color:#8fb3c8;background:#0d2230;border:1px solid #1f5f86;border-radius:5px;padding:1px 7px;margin-left:8px;white-space:nowrap}
</style>""", 1)
io.open(P, "w", encoding="utf-8", newline="\n").write(h)
print("tracker patched")
