/* Fuzz-tests every generator in viz_engine.js.  Run:  node viz_test.js
 *
 *   1. the declared default input must run and agree with brute force
 *   2. ~300 random inputs per generator must also agree with brute force
 *   3. every frame must point at a real code line and real cell indices
 *
 * build_radar.py runs this and refuses to build if anything fails, which is what makes
 * "watch it run" trustworthy: the animation and the answer come from the same code, and
 * the answer is checked against an independent implementation.
 */
var G = require("./viz_engine.js");
require("./viz_engine_b.js");
require("./viz_engine_c.js");
require("./viz_engine_d.js");
require("./viz_engine_e.js");
require("./viz_engine_f.js");          // each batch registers onto the same object
require("./viz_engine_g.js");

var PARSE = G.__helpers.parse;   // the SAME parsers the page uses

function defaults(spec) {
  var v = {};
  spec.forEach(function (f) {
    v[f.id] = (typeof f.def === "string") ? PARSE[f.type](f.def) : f.def;
  });
  return v;
}

var rnd = (function () {            /* deterministic, so a failure is reproducible */
  var s = 20261020;
  return function (n) { s = (s * 1103515245 + 12345) & 0x7fffffff; return s % n; };
})();

function randomInput(id, spec) {
  var v = {};
  spec.forEach(function (f) {
    if (f.type === "ints") {
      var n = 1 + rnd(8), arr = [];
      for (var i = 0; i < n; i++) {
        if (id === "tp-partition") arr.push(rnd(3));
        else if (id === "hs-cyclic") arr.push(1 + rnd(n));
        else if (id === "ms-hist" || id === "bs-answer") arr.push(1 + rnd(9));
        else if (id === "sw-shortest") arr.push(1 + rnd(9));
        else if (id === "bt-subsets") arr.push(1 + rnd(20));
        else arr.push(rnd(13) - 4);
      }
      if (id === "bt-xor") {                       /* needs pairs + exactly one single */
        arr = [];
        var single = 1 + rnd(30);
        var pairs = rnd(4);
        for (var p = 0; p < pairs; p++) { var x = 1 + rnd(30); if (x === single) x = single + 31; arr.push(x, x); }
        arr.push(single);
        for (var sh = arr.length - 1; sh > 0; sh--) { var j = rnd(sh + 1), tmp = arr[sh]; arr[sh] = arr[j]; arr[j] = tmp; }
      }
      if (id === "bt-subsets") arr = arr.slice(0, 1 + rnd(5));
      v[f.id] = arr;
    } else if (f.type === "string") {
      var len = 1 + rnd(10), s = "";
      for (var k = 0; k < len; k++) {
        s += (id === "ms-match") ? "()[]{}".charAt(rnd(6))
                                 : "abcab".charAt(rnd(5));
      }
      v[f.id] = s;
    } else if (f.type === "digits") {
      var dl = 1 + rnd(7), d = "";
      for (var q = 0; q < dl; q++) d += String(rnd(10));
      v[f.id] = d;
    } else if (f.type === "pairs") {
      var m = 1 + rnd(5), out = [];
      for (var z = 0; z < m; z++) { var a = 1 + rnd(8); out.push([a, a + 1 + rnd(4)]); }
      v[f.id] = out;
    } else if (f.type === "triples") {
      var tn = 1 + rnd(4), to = [];
      for (var w = 0; w < tn; w++) { var l = rnd(6); to.push([l, l + rnd(3), 1 + rnd(5)]); }
      v[f.id] = to;
    } else if (f.type === "rows") {
      var rn = 1 + rnd(4), rr = [];
      for (var ri = 0; ri < rn; ri++) {
        var rl = 1 + rnd(4), one = [];
        for (var rj = 0; rj < rl; rj++) one.push(1 + rnd(9));
        rr.push(one);
      }
      v[f.id] = rr;
    } else if (f.type === "quad") {
      v[f.id] = [0, 0, 0, 0];
    } else if (f.type === "letters") {
      var ln = 1 + rnd(3), lr = [], lw = 1 + rnd(3);
      for (var lj = 0; lj < ln; lj++) {
        var s3 = "";
        for (var lk = 0; lk < lw; lk++) s3 += "abc".charAt(rnd(3));
        lr.push(s3);
      }
      v[f.id] = lr;
    } else if (f.type === "tree") {
      var len2 = 1 + rnd(9), lv = [];
      for (var q2 = 0; q2 < len2; q2++) lv.push(rnd(6) === 0 && q2 > 0 ? null : 1 + rnd(20));
      lv[0] = 1 + rnd(20);
      v[f.id] = lv;
    } else if (f.type === "words") {
      var wn = 1 + rnd(3), ws = [];
      for (var wi = 0; wi < wn; wi++) {
        var wl = 1 + rnd(4), w2 = "";
        for (var wj = 0; wj < wl; wj++) w2 += "abc".charAt(rnd(3));
        ws.push(w2);
      }
      v[f.id] = ws;
    } else if (f.type === "word") {
      var ql = rnd(4), qw = "";
      for (var qi = 0; qi < ql; qi++) qw += "abc".charAt(rnd(3));
      v[f.id] = qw;
    } else if (f.type === "grid01" || f.type === "gridnum") {
      var rows = 1 + rnd(5), colsN = 1 + rnd(6), gg = [];
      for (var gr = 0; gr < rows; gr++) {
        var row = [];
        for (var gc = 0; gc < colsN; gc++) row.push(f.type === "grid01" ? rnd(2) : 1 + rnd(9));
        gg.push(row);
      }
      v[f.id] = gg;
    } else if (f.type === "int") {
      v[f.id] = 1 + rnd(9);
    }
  });
  /* Second pass: make the scalar fields VALID against the array that was just generated.
     Without this most cases are thrown out by check() and the fuzzer barely tests anything. */
  var n = v.a ? v.a.length : 0;
  if (id === "sw-fixed" || id === "sw-deque" || id === "hp-topk") v.k = 1 + rnd(n);
  if (id === "sw-exact") v.k = 1 + rnd(3);
  if (id === "ps-range") { v.l = rnd(n); v.r = v.l + rnd(n - v.l); }
  if (id === "ps-diff") {
    v.n = 1 + rnd(8);
    v.ops = v.ops.map(function (o) { var l = rnd(v.n); return [l, l + rnd(v.n - l), o[2]]; });
  }
  if (id === "bs-answer") v.h = v.piles.length + rnd(12);
  if (id === "sw-shortest") {
    var tot = v.a.reduce(function (s, x) { return s + x; }, 0);
    v.target = 1 + rnd(Math.max(1, tot + 3));
  }
  if (id === "tp-ends" || id === "hs-index") {
    v.target = (rnd(2) && n > 1) ? v.a[rnd(n)] + v.a[rnd(n)] : rnd(15) - 3;
  }
  if (id === "bs-exact" || id === "bs-bound" || id === "bs-rotated") {
    v.x = rnd(2) ? v.a[rnd(n)] : rnd(15) - 4;
  }
  if (id === "tp-write") v.drop = rnd(2) ? v.a[rnd(n)] : 0;
  if (id === "ms-greedy") v.k = rnd(v.num.length + 1);
  if (id === "dp-coin") v.amount = rnd(15);
  if (id === "dp-knapsack") v.cap = rnd(13);
  if (id === "bk-board") v.n = 1 + rnd(6);
  if (id === "sp-dijkstra" || id === "sp-bellman" || id === "dsu-kruskal" || id === "to-dfs") {
    v.n = 2 + rnd(7);
    var mk = [];
    for (var ge = 0; ge < 1 + rnd(9); ge++) {
      var ga = rnd(v.n), gb = rnd(v.n);
      if (ga === gb) gb = (gb + 1) % v.n;
      mk.push(id === "to-dfs" ? [ga, gb] : [ga, gb, rnd(9)]);
    }
    v.edges = mk;
    if (id === "sp-bellman") v.k = rnd(v.n + 1);
  }
  if (id === "iv-insert") {
    var base = [], at = 1 + rnd(3);
    for (var ii = 0; ii < 1 + rnd(3); ii++) {
      var en = at + rnd(3);
      if (en > 14) break;
      base.push([at, en]);
      at = en + 1 + rnd(3);
    }
    if (!base.length) base = [[1, 2]];
    v.iv = base;
    var ns = 1 + rnd(10);
    v.neu = [[ns, Math.min(14, ns + rnd(4))]];
  }
  if (id === "gr-local") { v.cool = rnd(5); }
  if (id === "ps-2d" && v.g) {
    var gr2 = rnd(v.g.length), gc2 = rnd(v.g[0].length);
    v.q = [gr2, gc2, gr2 + rnd(v.g.length - gr2), gc2 + rnd(v.g[0].length - gc2)];
  }
  if (id === "sp-floyd") {
    v.n = 2 + rnd(4);
    var fe = [];
    for (var fi = 0; fi < 1 + rnd(6); fi++) {
      var fa = rnd(v.n), fb = rnd(v.n);
      if (fa === fb) fb = (fb + 1) % v.n;
      fe.push([fa, fb, rnd(9)]);
    }
    v.edges = fe;
  }
  if (id === "dsu-cycle") {
    v.n = 2 + rnd(7);
    var ce = [];
    for (var cj = 0; cj < 1 + rnd(8); cj++) {
      var ca = rnd(v.n), cb = rnd(v.n);
      if (ca === cb) cb = (cb + 1) % v.n;
      ce.push([ca, cb]);
    }
    v.edges = ce;
  }
  if (id === "bt-dp" && v.cost) {              /* must be square */
    var sz = Math.min(4, v.cost.length), sq = [];
    for (var si = 0; si < sz; si++) {
      var rowq = [];
      for (var sj = 0; sj < sz; sj++) rowq.push(1 + rnd(9));
      sq.push(rowq);
    }
    v.cost = sq;
  }
  if (id === "hp-merge" && v.rows) {
    v.rows = v.rows.map(function (r) { return r.slice().sort(function (x, y) { return x - y; }); });
  }
  if (id === "tr-search" && v.g) {
    var wmax = v.g[0].length;
    v.g = v.g.map(function (r) { return r.slice(0, wmax); }).filter(function (r) { return r.length === wmax; });
    if (!v.g.length) v.g = ["ab"];
  }
  if (id === "iv-sortkey" && v.people) {
    /* build a REAL queue, then read off each person's true k -- the input is valid by construction */
    var np = 1 + rnd(6), heights = [];
    for (var pi = 0; pi < np; pi++) heights.push(1 + rnd(9));
    var pp = [];
    for (pi = 0; pi < np; pi++) {
      var taller = 0;
      for (var pj = 0; pj < pi; pj++) if (heights[pj] >= heights[pi]) taller++;
      pp.push([heights[pi], taller]);
    }
    for (var sh = pp.length - 1; sh > 0; sh--) {       /* shuffle: order must not matter */
      var sj = rnd(sh + 1), tmp2 = pp[sh]; pp[sh] = pp[sj]; pp[sj] = tmp2;
    }
    v.people = pp;
  }
  if (id === "ll-dummy" && v.a && v.a.length) v.val = rnd(2) ? v.a[rnd(v.a.length)] : 99;
  if (id === "bt-tricks") v.x = rnd(1024);
  if (id === "td-down") {
    var vals = (v.t || []).filter(function (x) { return x !== null; });
    v.target = rnd(2) && vals.length ? vals[rnd(vals.length)] * (1 + rnd(2)) : 1 + rnd(30);
  }
  if (id === "td-bst") {                       /* build a real BST, then level-order it */
    var pool = [], used = {};
    while (pool.length < 1 + rnd(7)) { var x2 = 1 + rnd(30); if (!used[x2]) { used[x2] = 1; pool.push(x2); } }
    pool.sort(function (a, b) { return a - b; });
    var lvl = [];
    (function build(lo, hi, idx) {
      if (lo > hi) return;
      var mid = (lo + hi) >> 1;
      lvl[idx] = pool[mid];
      build(lo, mid - 1, 2 * idx + 1);
      build(mid + 1, hi, 2 * idx + 2);
    })(0, pool.length - 1, 0);
    for (var z = 0; z < lvl.length; z++) if (lvl[z] === undefined) lvl[z] = null;
    v.t = lvl;
    v.k = 1 + rnd(pool.length);
  }
  if (id === "td-lca") {                      /* LCA needs distinct values to be well defined */
    var nxtV = 1, lv2 = (v.t || []).slice();
    for (var li = 0; li < lv2.length; li++) if (lv2[li] !== null) lv2[li] = nxtV++;
    if (lv2.length && lv2[0] === null) lv2[0] = nxtV++;
    v.t = lv2;
    var vv = lv2.filter(function (x) { return x !== null; });
    if (vv.length >= 2) {
      v.p = vv[rnd(vv.length)];
      do { v.q = vv[rnd(vv.length)]; } while (v.q === v.p && vv.length > 1);
    }
  }
  if (id === "tr-basic" && v.words && v.words.length) {
    v.query = rnd(2) ? v.words[rnd(v.words.length)] : v.query;
  }
  if (id === "gr-pair") {
    v.limit = Math.max.apply(null, v.people) + rnd(5);
  }
  if (id === "dsu-connect" || id === "to-kahn") {
    v.n = 1 + rnd(8);
    v.edges = v.edges.map(function (e) { return [rnd(v.n), rnd(v.n)]; });
  }
  if (id === "ps-count" || id === "ps-longest") v.k = rnd(13) - 4;
  if (id === "bs-rotated") {           /* actually rotate a sorted array */
    v.a = v.a.slice().sort(function (p, q) { return p - q; });
    var cut = rnd(v.a.length);
    v.a = v.a.slice(cut).concat(v.a.slice(0, cut));
  }
  if ((id === "sm-kmp" || id === "sm-rabinkarp") && v.text && v.pat) {
    if (v.pat.length > v.text.length) { var tmp3 = v.pat; v.pat = v.text; v.text = tmp3; }
    if (rnd(2) && v.text.length >= v.pat.length) {       /* half the time, make it a REAL match */
      var start = rnd(v.text.length - v.pat.length + 1);
      v.pat = v.text.substr(start, v.pat.length);
    }
  }
  if ((id === "st-range" || id === "st-fenwick" || id === "st-lazy") && v.a) {
    var nn = v.a.length;
    v.idx = rnd(nn);
    v.val = 1 + rnd(9);
    v.delta = rnd(13) - 6;
    v.l = rnd(nn);
    v.r = v.l + 1 + rnd(nn - v.l);
    v.l2 = rnd(nn);
    v.r2 = v.l2 + 1 + rnd(nn - v.l2);
  }
  if (id === "sim-rotate" && v.g) {               /* truncate to a square so check() doesn't reject it */
    var szr = Math.min(v.g.length, v.g[0].length);
    v.g = v.g.slice(0, szr).map(function (row) { return row.slice(0, szr); });
  }
  if (id === "sim-marking" && v.g) {              /* force at least one real zero to exercise the marking */
    var mr = rnd(v.g.length), mc = rnd(v.g[0].length);
    v.g[mr][mc] = 0;
  }
  return v;
}

function keySpace(tr) {
  if (tr.kind === "grid") {
    var ok = {};
    for (var r = 0; r < tr.data.r; r++) for (var c = 0; c < tr.data.c; c++) ok[r + "," + c] = 1;
    return ok;
  }
  if (tr.kind === "tree" || tr.kind === "graph") {
    var n2 = (tr.kind === "tree") ? tr.data.nodes.length : tr.data.n, o = {};
    for (var i = 0; i < n2; i++) o[String(i)] = 1;
    return o;
  }
  var len = tr.data.length, p = {};
  for (var k = 0; k < len; k++) p[String(k)] = 1;
  return p;
}

function structural(id, res, inp) {
  var tr = res.trace;
  var space = keySpace(tr);
  var n = (tr.kind === "grid" || tr.kind === "tree" || tr.kind === "graph")
        ? Object.keys(space).length : tr.data.length;
  if (!tr.frames.length) return "produced no frames";
  for (var i = 0; i < tr.frames.length; i++) {
    var f = tr.frames[i];
    if (!(f.line >= 0 && f.line < tr.code.length)) return "frame " + i + " points at code line " + f.line + " of " + tr.code.length;
    if (!f.note) return "frame " + i + " has no note";
    if (f.span && tr.kind !== "grid" && (f.span[0] < 0 || f.span[1] >= n || f.span[0] > f.span[1]))
      return "frame " + i + " span " + JSON.stringify(f.span) + " outside 0.." + (n - 1);
    for (var key in f.mark) {
      if (!space[key]) return "frame " + i + " marks " + key + ", which is not a cell on this stage";
    }
    for (var ek in (f.emark || {})) {
      var en = (tr.data.edges || []).length;
      if (!(Number(ek) >= 0 && Number(ek) < en)) return "frame " + i + " marks edge " + ek + ", outside 0.." + (en - 1);
    }
    for (var pk in f.ptr) {
      var pkey = String(f.ptr[pk]);
      /* On a row stage a pointer may sit ONE past the end: that is what a half-open bound
         (hi = n) means, and the renderer draws nothing for it. Anything further out, or any
         off-stage key on a grid/tree/graph, is a real bug. */
      if (space[pkey]) continue;
      if (tr.kind !== "grid" && tr.kind !== "tree" && tr.kind !== "graph" && Number(pkey) === n) continue;
      return "frame " + i + " pointer " + pk + " points at " + f.ptr[pk] + ", not a cell";
    }
  }
  return null;
}

var ids = Object.keys(G).filter(function (k) { return k.indexOf("__") !== 0; }).sort();
var fails = [], totalCases = 0, totalFrames = 0;

ids.forEach(function (id) {
  var g = G[id];
  var cases = [defaults(g.input)];
  for (var i = 0; i < 300; i++) cases.push(randomInput(id, g.input));

  var ran = 0;
  cases.forEach(function (inp, ci) {
    var v = JSON.parse(JSON.stringify(inp));
    if (g.prep) g.prep(v);
    if (g.check && g.check(v)) return;             /* input legitimately rejected -- skip */
    var res, err = null;
    try { res = g.run(JSON.parse(JSON.stringify(v))); }
    catch (e) { err = "threw: " + e.message; }
    if (err) { fails.push(id + " #" + ci + " " + JSON.stringify(v) + " -> " + err); return; }
    var expect;
    try { expect = g.brute(JSON.parse(JSON.stringify(v))); }
    catch (e) { fails.push(id + " #" + ci + " brute threw: " + e.message); return; }
    if (String(res.answer) !== String(expect)) {
      fails.push(id + " #" + ci + " " + JSON.stringify(v) +
                 " -> run says " + JSON.stringify(res.answer) + ", brute force says " + JSON.stringify(expect));
      return;
    }
    var se = structural(id, res, v);
    if (se) { fails.push(id + " #" + ci + " " + JSON.stringify(v) + " -> " + se); return; }
    ran++; totalFrames += res.trace.frames.length;
  });

  if (ran === 0) fails.push(id + ": every generated case was rejected by check() -- the fuzzer cannot test it");
  totalCases += ran;
  var defRes = (function () {
    var v = defaults(g.input);
    if (g.prep) g.prep(v);
    try { return g.run(v); } catch (e) { return null; }
  })();
  console.log("  " + (fails.length ? " " : " ") + id.padEnd(14) +
              String(ran).padStart(4) + " cases ok" +
              (defRes ? ("   default: " + defRes.trace.frames.length + " frames, answer " +
                         JSON.stringify(defRes.answer)) : "   DEFAULT FAILED"));
});

console.log("\n" + ids.length + " generators, " + totalCases + " cases, " + totalFrames + " frames checked");
if (fails.length) {
  console.log("\nFAILURES (" + fails.length + "):");
  fails.slice(0, 25).forEach(function (f) { console.log("  " + f); });
  if (fails.length > 25) console.log("  ... and " + (fails.length - 25) + " more");
  process.exit(1);
}
console.log("all generators agree with brute force");
