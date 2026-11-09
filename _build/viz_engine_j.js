/* =====================================================================================
   VIZ ENGINE, part J  --  the seven rare variants: rerooting, binary lifting, bridges, SCC, Euler path, digit DP,
   coordinate geometry. Same contract as the other parts (input, check, brute, run, optional gen).
   Needs the helpers that part I publishes on H.I.
   ===================================================================================== */
(function () {
  "use strict";
  var G = (typeof module !== "undefined" && module.exports) ? require("./viz_engine.js") : window.VIZGEN;
  var H = G.__helpers, Trace = H.Trace, I = H.I;
  if (!I) throw new Error("viz_engine_i.js must load before viz_engine_j.js");
  var ri = I.ri, J = I.J, aux = I.aux, copy = I.copy, buildTree = I.buildTree, treeTrace = I.treeTrace, TF = I.TF, checkTree = I.checkTree,
      genTree = I.genTree, adj = I.adj, graphTrace = I.graphTrace, edgeCheck = I.edgeCheck;
  function A(data, code, cap, kind) { return new Trace(data, code, kind || "array", cap); }
  function rng(lo, hi) { var o = []; for (var i = lo; i <= hi; i++) o.push(i); return o; }

  /* ================================ rerooting DP ================================ */
  G["td-reroot"] = {
    input: [TF("tree, level order (. = empty)", "1 2 3 . . 4 5")],
    check: function (v) { return checkTree(v, 12); },
    gen: function (rnd) { return { t: genTree(rnd, 9) }; },
    brute: function (v) {
      var g = adj(buildTree(v.t)), n = g.length, out = [];
      for (var s = 0; s < n; s++) {
        var d = {}, q = [s], tot = 0; d[s] = 0;
        while (q.length) { var u = q.shift(); g[u].forEach(function (w) { if (!(w in d)) { d[w] = d[u] + 1; q.push(w); } }); }
        for (var k in d) tot += d[k];
        out.push(tot);
      }
      return J(out);
    },
    run: function (v) {
      var tree = buildTree(v.t), g = adj(tree), n = g.length, size = [], ans = [], m = {}, i;
      for (i = 0; i < n; i++) { size.push(1); ans.push(0); }
      var t = treeTrace(tree, ["def down(u, parent):                    # pass 1: answers for the subtree below u", "    for v in children(u): down(v, u); size[u] += size[v]; ans[u] += ans[v] + size[v]",
                               "def reroot(u, parent):                  # pass 2: slide the root one edge down", "    for v in children(u):", "        ans[v] = ans[u] - size[v] + (n - size[v])     # size[v] nodes get 1 closer, the other n-size[v] get 1 farther",
                               "        reroot(v, u)"], "sum of distances from EVERY node: two passes instead of n searches");
      function down(u, p) {
        g[u].forEach(function (w) { if (w !== p) { down(w, u); size[u] += size[w]; ans[u] += ans[w] + size[w]; } });
        m[String(u)] = "pick";
        t.snap(1, "pass 1, node " + tree.nodes[u].v + ": its subtree has " + size[u] + " node(s); the distances from it to everything BELOW are " + ans[u] + ".", { ptr: { at: String(u) }, mark: copy(m), aux: aux("size", size.join(" "), "ans so far", ans.join(" ")) });
      }
      down(tree.root, -1);
      m = {}; m[String(tree.root)] = "done";
      t.snap(2, "The root's number is already final: " + ans[tree.root] + ". Everything else will be derived from it, one edge at a time.", { ptr: { at: String(tree.root) }, mark: copy(m), aux: aux("ans", ans.join(" ")) });
      function reroot(u, p) {
        g[u].forEach(function (w) {
          if (w === p) return;
          ans[w] = ans[u] - size[w] + (n - size[w]);
          m[String(w)] = "done";
          t.snap(4, "move the root from " + tree.nodes[u].v + " to " + tree.nodes[w].v + ": " + size[w] + " node(s) get 1 closer, " + (n - size[w]) + " get 1 farther. " + ans[u] + " − " + size[w] + " + " + (n - size[w]) + " = " + ans[w] + ".",
                 { ptr: { from: String(u), to: String(w) }, mark: copy(m), aux: aux("ans", ans.join(" ")) });
          reroot(w, u);
        });
      }
      reroot(tree.root, -1);
      t.snap(5, "Answer (by node, in level order): " + ans.join(", ") + ". Two linear passes, no search per root.", { mark: copy(m), aux: aux("answer", ans.join(",")) });
      return { trace: t, answer: J(ans) };
    }
  };

  /* ================================ binary lifting ================================ */
  G["td-lift"] = {
    input: [{ id: "a", label: "parent of each node (-1 = root)", type: "ints", def: "-1 0 0 1 1 2 2 3 7" }, { id: "v", label: "start at node", type: "int", def: 8 }, { id: "k", label: "go up k steps", type: "int", def: 3 }],
    check: function (v) {
      var n = v.a.length; if (n < 2 || n > 12) return "use 2 to 12 nodes";
      if (v.a[0] !== -1) return "node 0 is the root, so its parent must be -1";
      for (var i = 1; i < n; i++) if (v.a[i] < -1 || v.a[i] >= i) return "the parent of node " + i + " must be -1 or a smaller node number (so there are no cycles)";
      if (v.v < 0 || v.v >= n) return "the start node must be between 0 and " + (n - 1);
      if (v.k < 1 || v.k > 15) return "k between 1 and 15";
    },
    gen: function (rnd) { var n = ri(rnd, 2, 10), a = [-1]; for (var i = 1; i < n; i++) a.push(rnd(6) === 0 ? -1 : ri(rnd, 0, i - 1)); return { a: a, v: ri(rnd, 0, n - 1), k: ri(rnd, 1, 15) }; },
    brute: function (v) { var u = v.v; for (var s = 0; s < v.k && u !== -1; s++) u = v.a[u]; return u; },
    run: function (v) {
      var n = v.a.length, up = [v.a.slice()], j, x;
      var t = A(rng(0, n - 1), ["up[0] = parent                                   # the 1-step jump", "for j in 1..3:", "    up[j][x] = up[j-1][ up[j-1][x] ]          # two jumps of 2^(j-1) make one jump of 2^j",
                                 "for j in range(4):                              # answer a query by the bits of k", "    if k >> j & 1: v = up[j][v]               # jump 2^j", "    if v == -1: return -1"], "k-th ancestor in O(log k): jump by powers of two");
      t.snap(0, "level 0 is the parent list itself: up[0][x] is the ancestor 1 step above x (−1 = none).", { aux: aux("up[0]", up[0].join(" ")) });
      for (j = 1; j <= 3; j++) {
        var prev = up[j - 1], cur = [];
        for (x = 0; x < n; x++) cur.push(prev[x] === -1 ? -1 : prev[prev[x]]);
        up.push(cur);
        t.snap(2, "level " + j + ": jump 2^" + (j - 1) + " twice = jump " + (1 << j) + ". Built from the level below, never from scratch.", { aux: aux("up[" + (j - 1) + "]", prev.join(" "), "up[" + j + "]", cur.join(" ")) });
      }
      var u = v.v;
      t.snap(3, "query: go up " + v.k + " from node " + u + ". " + v.k + " in binary is " + v.k.toString(2) + ", so jump by exactly those powers of two.", { ptr: { v: u }, aux: aux("k (binary)", v.k.toString(2)) });
      for (j = 0; j <= 3 && u !== -1; j++) {
        if (!((v.k >> j) & 1)) continue;
        var from = u; u = up[j][u];
        t.snap(4, "bit " + j + " is set: jump " + (1 << j) + " from node " + from + (u === -1 ? ", which runs off the top of the tree. Answer −1." : " to node " + u + "."), u === -1 ? { aux: aux("answer", -1) } : { ptr: { v: u, from: from }, aux: aux("answer so far", u) });
      }
      t.snap(5, "Answer " + u + ". Each query costs about log2(k) jumps; the table costs n log n once.", u === -1 ? { aux: aux("answer", -1) } : { ptr: { answer: u }, aux: aux("answer", u) });
      return { trace: t, answer: u };
    }
  };

  /* ================================ bridges (low-link) ================================ */
  G["gw-bridges"] = {
    input: [{ id: "n", label: "nodes", type: "int", def: 6 }, { id: "edges", label: "edges  a,b", type: "pairs", def: "0,1 1,2 2,0 1,3 3,4 4,5 5,3" }],
    check: function (v) { return edgeCheck(v, false); },
    gen: function (rnd) { var n = ri(rnd, 2, 8), e = []; for (var i = 0, c = ri(rnd, 1, 10); i < c; i++) { var a = rnd(n), b = rnd(n); if (a === b) b = (b + 1) % n; e.push([a, b]); } return { n: n, edges: e }; },
    brute: function (v) {
      function comps(skip) {
        var p = []; for (var i = 0; i < v.n; i++) p.push(i);
        function f(x) { while (p[x] !== x) x = p[x]; return x; }
        v.edges.forEach(function (e, idx) { if (idx !== skip) p[f(e[0])] = f(e[1]); });
        var r = {}; for (i = 0; i < v.n; i++) r[f(i)] = 1; return Object.keys(r).length;
      }
      var base = comps(-1), out = [];
      v.edges.forEach(function (e, idx) { if (comps(idx) > base) out.push(idx); });
      return out.length ? J(out) : "none";
    },
    run: function (v) {
      var n = v.n, g = I.neighbours(n, v.edges), disc = [], low = [], m = {}, em = {}, timer = 0, out = [], i;
      for (i = 0; i < n; i++) { disc.push(-1); low.push(0); }
      var t = graphTrace(n, v.edges, ["disc, low = {}, {}", "def dfs(u, parent_edge):", "    disc[u] = low[u] = timer; timer += 1", "    for v in g[u]:                            # skip the edge we came by",
                                      "        if disc[v] == -1:                    # tree edge: go down", "            dfs(v, this edge); low[u] = min(low[u], low[v])", "            if low[v] > disc[u]: BRIDGE             # nothing below can climb back past u",
                                      "        else: low[u] = min(low[u], disc[v])  # back edge: a way around"], "bridges: an edge no cycle passes through");
      function dfs(u, pe) {
        disc[u] = low[u] = timer++; m[String(u)] = "pick";
        t.snap(2, "visit node " + u + " at time " + disc[u] + ". low starts equal to disc.", { ptr: { u: String(u) }, mark: copy(m), emark: copy(em), aux: aux("disc", disc.map(function (d) { return d < 0 ? "-" : d; }).join(" "), "low", low.join(" ")) });
        g[u].forEach(function (p) {
          var w = p[0], ei = p[1];
          if (ei === pe) return;
          if (disc[w] === -1) {
            em[String(ei)] = "done"; dfs(w, ei);
            low[u] = Math.min(low[u], low[w]);
            var br = low[w] > disc[u];
            if (br) { out.push(ei); em[String(ei)] = "bad"; }
            t.snap(br ? 6 : 5, "back at " + u + " from " + w + ": low[" + w + "] = " + low[w] + (br ? " > disc[" + u + "] = " + disc[u] + ". Nothing in that subtree can climb back above " + u + ", so edge " + u + "–" + w + " is a BRIDGE." : " ≤ disc[" + u + "] = " + disc[u] + ", a cycle gives another way around, so " + u + "–" + w + " is not a bridge."),
                   { ptr: { u: String(u), child: String(w) }, mark: copy(m), emark: copy(em), aux: aux("low", low.join(" "), "bridges", out.length)  });
          } else {
            var old = low[u]; low[u] = Math.min(low[u], disc[w]);
            t.snap(7, "edge " + u + "–" + w + " goes to an already-visited node (time " + disc[w] + "): a cycle. low[" + u + "] " + (low[u] < old ? "drops from " + old + " to " + low[u] : "stays " + low[u]) + ".",
                   { ptr: { u: String(u), seen: String(w) }, mark: copy(m), emark: copy(em), aux: aux("low", low.join(" ")) });
          }
        });
        m[String(u)] = "done";
      }
      for (i = 0; i < n; i++) if (disc[i] === -1) dfs(i, -1);
      out.sort(function (a, b) { return a - b; });
      t.snap(1, out.length ? "Answer: " + out.length + " bridge(s), shown in red. Removing any of them splits the graph." : "No bridges: every edge lies on a cycle.", { mark: copy(m), emark: copy(em), aux: aux("answer", out.length ? J(out) + " (edge numbers)" : "none") });
      return { trace: t, answer: out.length ? J(out) : "none" };
    }
  };

  /* ================================ strongly connected components (Kosaraju) ================================ */
  G["gw-scc"] = {
    input: [{ id: "n", label: "nodes", type: "int", def: 6 }, { id: "edges", label: "DIRECTED edges  from,to", type: "pairs", def: "0,1 1,2 2,0 1,3 3,4 4,3 4,5" }],
    check: function (v) { return edgeCheck(v, false); },
    gen: function (rnd) { var n = ri(rnd, 2, 8), e = []; for (var i = 0, c = ri(rnd, 1, 11); i < c; i++) { var a = rnd(n), b = rnd(n); if (a === b) b = (b + 1) % n; e.push([a, b]); } return { n: n, edges: e }; },
    brute: function (v) {
      var n = v.n, r = [], i, j, k;
      for (i = 0; i < n; i++) { r.push([]); for (j = 0; j < n; j++) r[i].push(i === j); }
      v.edges.forEach(function (e) { r[e[0]][e[1]] = true; });
      for (k = 0; k < n; k++) for (i = 0; i < n; i++) for (j = 0; j < n; j++) if (r[i][k] && r[k][j]) r[i][j] = true;
      var comp = [], c = 0;
      for (i = 0; i < n; i++) { if (comp[i] !== undefined) continue; for (j = 0; j < n; j++) if (r[i][j] && r[j][i]) comp[j] = c; c++; }
      return c;
    },
    run: function (v) {
      var n = v.n, f = [], b = [], i, m = {};
      for (i = 0; i < n; i++) { f.push([]); b.push([]); }
      v.edges.forEach(function (e) { f[e[0]].push(e[1]); b[e[1]].push(e[0]); });
      var t = graphTrace(n, v.edges, ["PASS 1: DFS on the graph; write each node down when it FINISHES", "PASS 2: take nodes in reverse finish order;", "    each unvisited one starts a DFS on the REVERSED graph", "    everything that DFS reaches is one strongly connected component"],
                         "strongly connected groups (edges a,b mean a→b; the picture draws them as plain lines)");
      var seen = {}, order = [];
      function d1(u) {
        seen[u] = 1;
        f[u].forEach(function (w) { if (!seen[w]) d1(w); });
        order.push(u); m[String(u)] = "pick";
        t.snap(0, "pass 1: node " + u + " finished (everything reachable from it is already done). Finish order so far: " + order.join(", ") + ".", { ptr: { u: String(u) }, mark: copy(m), aux: aux("finish order", order.join(" ")) });
      }
      for (i = 0; i < n; i++) if (!seen[i]) d1(i);
      seen = {}; m = {};
      var count = 0, done = {};
      for (i = order.length - 1; i >= 0; i--) {
        var s = order[i]; if (seen[s]) continue;
        count++;
        var st = [s], comp = [s]; seen[s] = 1;
        while (st.length) { var u = st.pop(); b[u].forEach(function (w) { if (!seen[w]) { seen[w] = 1; st.push(w); comp.push(w); } }); }
        var mm = copy(done); comp.forEach(function (x) { mm[String(x)] = "pick"; });
        t.snap(2, "pass 2: " + s + " is the latest-finishing unvisited node, so search BACKWARD from it. It reaches " + comp.join(", ") + ": component " + count + ". The backward search cannot leak into other groups.", { ptr: { s: String(s) }, mark: mm, aux: aux("components", count, "this one", comp.join(" ")) });
        comp.forEach(function (x) { done[String(x)] = "done"; });
      }
      t.snap(3, "Answer " + count + " component(s). A single node with no cycle counts as a component by itself.", { mark: copy(done), aux: aux("answer", count) });
      return { trace: t, answer: count };
    }
  };

  /* ================================ Euler path (Hierholzer) ================================ */
  function eulerBrute(v) {
    var out = [], used = [], E = v.edges.length, best = null;
    function dfs(u, path) {
      if (best) return;
      if (path.length === E + 1) { best = path.slice(); return; }
      var opts = [];
      v.edges.forEach(function (e, i) { if (!used[i] && e[0] === u) opts.push(i); });
      opts.sort(function (x, y) { return v.edges[x][1] - v.edges[y][1]; });
      for (var k = 0; k < opts.length && !best; k++) { used[opts[k]] = true; path.push(v.edges[opts[k]][1]); dfs(v.edges[opts[k]][1], path); path.pop(); used[opts[k]] = false; }
    }
    dfs(v.s, [v.s]);
    return best;
  }
  G["gw-euler"] = {
    input: [{ id: "n", label: "nodes", type: "int", def: 5 }, { id: "s", label: "start node", type: "int", def: 0 },
            { id: "edges", label: "DIRECTED edges  from,to  (each used exactly once)", type: "pairs", def: "0,1 1,2 2,0 0,3 3,4 4,0" }],
    check: function (v) {
      var e = edgeCheck(v, false); if (e) return e;
      if (v.s < 0 || v.s >= v.n) return "the start must be a node from 0 to " + (v.n - 1);
      if (!eulerBrute(v)) return "no route from node " + v.s + " uses every edge exactly once. Try a different start, or change the edges.";
    },
    gen: function (rnd) { var n = ri(rnd, 2, 6), cur = 0, e = []; for (var i = 0, c = ri(rnd, 2, 9); i < c; i++) { var nx = rnd(n); if (nx === cur) nx = (cur + 1) % n; e.push([cur, nx]); cur = nx; } return { n: n, s: 0, edges: e }; },
    brute: function (v) { return J(eulerBrute(v)); },
    run: function (v) {
      var n = v.n, g = [], i, m = {}, em = {}, route = [];
      for (i = 0; i < n; i++) g.push([]);
      v.edges.forEach(function (e, idx) { g[e[0]].push([e[1], idx]); });
      g.forEach(function (l) { l.sort(function (x, y) { return x[0] - y[0] || x[1] - y[1]; }); });
      var t = graphTrace(n, v.edges, ["def go(u):", "    while u has an unused edge:", "        take the smallest one, mark it used; go(its far end)", "    route.append(u)                  # only when u is STUCK",
                                      "go(start); route.reverse()"], "use every edge once (Hierholzer). Edges are directed from → to; the picture draws plain lines");
      function go(u) {
        m[String(u)] = "pick";
        while (g[u].length) {
          var p = g[u].shift(); em[String(p[1])] = "done";
          t.snap(2, "at " + u + ": take the smallest unused edge " + u + "→" + p[0] + " and keep walking.", { ptr: { at: String(u), to: String(p[0]) }, mark: copy(m), emark: copy(em), aux: aux("route (backward)", route.join(" ") || "empty") });
          go(p[0]);
        }
        route.push(u); m[String(u)] = "done";
        t.snap(3, "node " + u + " has no unused edges left: it is stuck, so write it at the END of the route. The route is built backward.", { ptr: { at: String(u) }, mark: copy(m), emark: copy(em), aux: aux("route (backward)", route.join(" ")) });
      }
      go(v.s);
      route.reverse();
      t.snap(4, "Reverse it: " + route.join(" → ") + ". Every edge is used exactly once.", { mark: copy(m), emark: copy(em), aux: aux("answer", route.join(" → ")) });
      return { trace: t, answer: J(route) };
    }
  };

  /* ================================ digit DP ================================ */
  G["dp-digit"] = {
    input: [{ id: "n", label: "count the numbers 0..N that contain no digit 4;  N =", type: "int", def: 5471 }],
    check: function (v) { if (v.n < 0 || v.n > 99999) return "N between 0 and 99999"; },
    gen: function (rnd) { return { n: ri(rnd, 0, 99999) }; },
    brute: function (v) { var c = 0; for (var x = 0; x <= v.n; x++) if (String(x).indexOf("4") < 0) c++; return c; },
    run: function (v) {
      var s = String(v.n), L = s.length, total = 0, alive = true;
      var t = A(s, ["s = str(N); total = 0", "for i, d in enumerate(s):               # follow N's own digits: the 'tight' path", "    smaller = digits below d that are allowed", "    total += smaller * 9**(L-i-1)       # those can't touch N; the rest of the digits are FREE",
                     "    if d == 4: break                     # the tight path itself is now invalid", "else: total += 1                       # N itself survived"], "digit DP: count by the first place where a number drops below N", "string");
      for (var i = 0; i < L; i++) {
        var d = +s[i], less = d - (d > 4 ? 1 : 0), free = Math.pow(9, L - i - 1);
        total += less * free;
        if (d === 4) {
          alive = false;
          t.snap(4, "position " + i + ": " + less + " allowed digit(s) below 4, each leaves " + (L - i - 1) + " free place(s) (9 choices each): +" + less * free + ". But N's own digit here is 4, so staying on N's path is impossible. Stop.", { ptr: { i: i }, span: [0, i], mark: { 0: "pick" }, aux: aux("total", total) });
          break;
        }
        t.snap(3, "position " + i + " (digit " + d + "): put a smaller allowed digit here (" + less + " choice" + (less === 1 ? "" : "s") + "), and the remaining " + (L - i - 1) + " place(s) are free, 9 choices each (no 4): " + less + " × " + free + " = " + less * free + ".", { ptr: { i: i }, span: [0, i], aux: aux("total", total) });
      }
      if (alive) { total++; t.snap(5, "all of N's digits were allowed, so N itself counts: +1.", { span: [0, L - 1], aux: aux("total", total) }); }
      t.snap(5, "Answer " + total + " numbers in 0.." + v.n + " have no digit 4. For a range [L, R] compute f(R) − f(L−1).", { aux: aux("answer", total) });
      return { trace: t, answer: total };
    }
  };

  /* ================================ coordinate geometry ================================ */
  G["ma-geom"] = {
    input: [{ id: "a", label: "rectangle A then B:  x1 y1 x2 y2   x1 y1 x2 y2   (bottom-left, top-right)", type: "ints", def: "0 0 4 3 2 1 6 5" }],
    check: function (v) {
      if (v.a.length !== 8) return "give exactly 8 numbers: four for rectangle A, four for rectangle B";
      for (var i = 0; i < 8; i++) if (v.a[i] < 0 || v.a[i] > 20) return "keep every number between 0 and 20";
      if (v.a[0] >= v.a[2] || v.a[1] >= v.a[3] || v.a[4] >= v.a[6] || v.a[5] >= v.a[7]) return "each rectangle needs x1 < x2 and y1 < y2 (bottom-left first, then top-right)";
    },
    gen: function (rnd) {
      function rect() { var x = ri(rnd, 0, 18), y = ri(rnd, 0, 18); return [x, y, ri(rnd, x + 1, 20), ri(rnd, y + 1, 20)]; }
      return { a: rect().concat(rect()) };
    },
    brute: function (v) {
      var a = v.a;
      for (var x = 0; x < 20; x++) for (var y = 0; y < 20; y++)
        if (x >= a[0] && x + 1 <= a[2] && y >= a[1] && y + 1 <= a[3] && x >= a[4] && x + 1 <= a[6] && y >= a[5] && y + 1 <= a[7]) return true;
      return false;
    },
    run: function (v) {
      var a = v.a;
      var t = A(a, ["# two rectangles overlap only if their shadows overlap on BOTH axes", "w = min(ax2, bx2) - max(ax1, bx1)        # width of the shared x-range", "if w <= 0: return False                  # the x-shadows miss, so they cannot touch",
                     "h = min(ay2, by2) - max(ay1, by1)        # height of the shared y-range", "return h > 0                            # touching along an edge (0) does not count"], "rectangle overlap: compare shadows, one axis at a time");
      var lox = Math.max(a[0], a[4]), hix = Math.min(a[2], a[6]), w = hix - lox;
      t.snap(1, "x-shadows: A covers " + a[0] + ".." + a[2] + ", B covers " + a[4] + ".." + a[6] + ". Shared part runs from max(" + a[0] + ", " + a[4] + ") = " + lox + " to min(" + a[2] + ", " + a[6] + ") = " + hix + ": width " + w + ".",
             { mark: { 0: "pick", 2: "pick", 4: "pick", 6: "pick" }, aux: aux("x overlap", w) });
      if (w <= 0) {
        t.snap(2, "width " + w + " is not positive: the shadows do not overlap (zero means they only touch). No need to look at y. Answer false.", { aux: aux("answer", "false") });
        return { trace: t, answer: false };
      }
      var loy = Math.max(a[1], a[5]), hiy = Math.min(a[3], a[7]), h = hiy - loy;
      t.snap(3, "y-shadows: A covers " + a[1] + ".." + a[3] + ", B covers " + a[5] + ".." + a[7] + ". Shared part runs from " + loy + " to " + hiy + ": height " + h + ".",
             { mark: { 1: "pick", 3: "pick", 5: "pick", 7: "pick" }, aux: aux("x overlap", w, "y overlap", h) });
      var ans = h > 0;
      t.snap(4, ans ? "Both shadows overlap, so the rectangles share an area of " + w + " × " + h + " = " + w * h + ". Answer true." : "height " + h + " is not positive: they only touch or miss on y. Answer false.", { aux: aux("answer", ans ? "true" : "false") });
      return { trace: t, answer: ans };
    }
  };
})();
