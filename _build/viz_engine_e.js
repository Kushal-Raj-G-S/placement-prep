/* =====================================================================================
   VIZ ENGINE, part E  --  the GRAPH stage, plus the last row-stage variants.
   Nodes sit on a circle, edges are drawn with their weights, and edges light up as they
   are relaxed, accepted or rejected.  Loads after viz_engine.js.
   ===================================================================================== */
(function () {
  "use strict";
  var G = (typeof module !== "undefined" && module.exports)
        ? require("./viz_engine.js")
        : window.VIZGEN;
  var H = G.__helpers, Trace = H.Trace, range = H.range, merge = H.merge, kv = H.kv, strs = H.strs;

  function graphTrace(n, edges, code, caption, labels) {
    return new Trace({ n: n, edges: edges, labels: labels || null }, code, "graph", caption);
  }
  function edgeCheck(v, weighted) {
    if (v.n < 2 || v.n > 8) return "use between 2 and 8 nodes so the drawing stays readable";
    if (!v.edges.length) return "give at least one edge";
    if (v.edges.length > 12) return "keep it to 12 edges or fewer";
    for (var i = 0; i < v.edges.length; i++) {
      var e = v.edges[i];
      if (e[0] < 0 || e[1] < 0 || e[0] >= v.n || e[1] >= v.n)
        return "edge " + e[0] + "," + e[1] + " uses a node outside 0.." + (v.n - 1);
      if (e[0] === e[1]) return "self-loops (" + e[0] + "," + e[1] + ") are not useful here";
      if (weighted && (e.length < 3 || e[2] < 0))
        return "every edge needs a non-negative weight, written  from,to,weight";
    }
    return null;
  }

  /* ================================== DIJKSTRA ==================================== */

  G["sp-dijkstra"] = {
    input: [{ id: "n", label: "nodes", type: "int", def: 6 },
            { id: "edges", label: "edges  from,to,weight", type: "triples", def: "0,1,4 0,2,1 2,1,2 1,3,1 2,3,5 3,4,3" }],
    check: function (v) { return edgeCheck(v, true); },
    brute: function (v) {              /* Bellman-Ford: a different algorithm, same answer */
      var dist = [], i, k;
      for (i = 0; i < v.n; i++) dist.push(Infinity);
      dist[0] = 0;
      for (k = 0; k < v.n; k++)
        for (i = 0; i < v.edges.length; i++) {
          var e = v.edges[i];
          if (dist[e[0]] + e[2] < dist[e[1]]) dist[e[1]] = dist[e[0]] + e[2];
          if (dist[e[1]] + e[2] < dist[e[0]]) dist[e[0]] = dist[e[1]] + e[2];
        }
      return dist.map(function (d) { return d === Infinity ? "inf" : d; }).join(",");
    },
    run: function (v) {
      var n = v.n, edges = v.edges, i;
      var t = graphTrace(n, edges,
                         ["dist[src] = 0;  h = [(0, src)]", "while h:", "    d, u = heappop(h)",
                          "    if d > dist[u]: continue      # a stale copy -- skip it",
                          "    for v, w in adj[u]:", "        if d + w < dist[v]:",
                          "            dist[v] = d + w;  heappush(h, (dist[v], v))"],
                         "shortest distance from node 0 (undirected, weights shown)");
      var adj = [];
      for (i = 0; i < n; i++) adj.push([]);
      for (i = 0; i < edges.length; i++) {
        adj[edges[i][0]].push([edges[i][1], edges[i][2], i]);
        adj[edges[i][1]].push([edges[i][0], edges[i][2], i]);
      }
      var dist = [];
      for (i = 0; i < n; i++) dist.push(Infinity);
      dist[0] = 0;
      var settled = {}, heap = [[0, 0]];
      var show = function () {
        return dist.map(function (d, j) { return j + ":" + (d === Infinity ? "∞" : d); });
      };
      t.snap(0, "Dijkstra is BFS with a priority queue. The invariant that makes it work: the FIRST time a " +
                "node is popped, its distance is already final — nothing cheaper can turn up later.",
             { ptr: { src: "0" }, mark: { 0: "pick" },
               aux: [{ label: "dist", items: show() }, { label: "heap", items: heap.map(function (x) { return x[0] + "@" + x[1]; }) }] });
      while (heap.length) {
        heap.sort(function (a, b) { return a[0] - b[0]; });
        var top = heap.shift(), d = top[0], u = top[1];
        if (d > dist[u]) {
          t.snap(3, "popped a stale copy of node " + u + " (" + d + " > the " + dist[u] + " we already have) " +
                    "— skip it. Python has no decrease-key, so you push duplicates and ignore the old ones. " +
                    "Without this line the complexity degrades.",
                 { ptr: { stale: String(u) }, mark: merge(settled, { [String(u)]: "bad" }),
                   aux: [{ label: "dist", items: show() }] });
          continue;
        }
        settled[String(u)] = "done";
        t.snap(2, "node " + u + " comes off the heap at distance " + d + " — SETTLED. It is now the nearest " +
                  "unfinished node, so no route found later can beat it.",
               { ptr: { settled: String(u) }, mark: merge(settled, { [String(u)]: "pick" }),
                 aux: [{ label: "dist", items: show() }] });
        for (i = 0; i < adj[u].length; i++) {
          var to = adj[u][i][0], w = adj[u][i][1], ei = adj[u][i][2];
          var nd = d + w;
          if (nd < dist[to]) {
            dist[to] = nd;
            heap.push([nd, to]);
            t.snap(6, "relax edge " + u + "–" + to + " (weight " + w + "): " + d + " + " + w + " = " + nd +
                      " beats " + (dist[to] === nd ? "the old value" : String(dist[to])) + ", so node " + to +
                      " improves to " + nd + ".",
                   { ptr: { from: String(u), to: String(to) },
                     mark: merge(settled, { [String(to)]: "pick" }), emark: { [String(ei)]: "pick" },
                     aux: [{ label: "dist", items: show() },
                           { label: "heap", items: heap.map(function (x) { return x[0] + "@" + x[1]; }) }] });
          } else {
            t.snap(5, "edge " + u + "–" + to + " (weight " + w + ") gives " + nd + ", which does not beat " +
                      (dist[to] === Infinity ? "∞" : dist[to]) + " — leave it alone.",
                   { ptr: { from: String(u), to: String(to) },
                     mark: merge(settled), emark: { [String(ei)]: "gone" },
                     aux: [{ label: "dist", items: show() }] });
          }
        }
      }
      t.snap(2, "Final distances: " + show().join("  ") + ". Dijkstra is WRONG with negative edges — " +
                "the 'settled is final' invariant simply does not hold there.",
             { mark: settled, aux: [{ label: "dist", items: show() }] });
      return { trace: t, answer: dist.map(function (dd) { return dd === Infinity ? "inf" : dd; }).join(",") };
    }
  };

  /* ================================= BELLMAN-FORD ================================= */

  G["sp-bellman"] = {
    input: [{ id: "n", label: "nodes", type: "int", def: 4 },
            { id: "edges", label: "flights  from,to,price", type: "triples", def: "0,1,100 1,2,100 2,3,100 0,2,500" },
            { id: "k", label: "max stops", type: "int", def: 1 }],
    check: function (v) {
      var e = edgeCheck(v, true);
      if (e) return e;
      if (v.k < 0 || v.k > v.n) return "stops must be between 0 and " + v.n;
    },
    brute: function (v) {              /* BFS over (node, edges used) -- a different route */
      var best = Infinity;
      var q = [[0, 0, 0]];             /* node, cost, edges used */
      while (q.length) {
        var cur = q.shift();
        if (cur[0] === v.n - 1) { best = Math.min(best, cur[1]); continue; }
        if (cur[2] === v.k + 1) continue;
        for (var i = 0; i < v.edges.length; i++)
          if (v.edges[i][0] === cur[0]) q.push([v.edges[i][1], cur[1] + v.edges[i][2], cur[2] + 1]);
      }
      return best === Infinity ? -1 : best;
    },
    run: function (v) {
      var n = v.n, edges = v.edges, k = v.k, i, j;
      var t = graphTrace(n, edges,
                         ["dist = [inf] * n;  dist[src] = 0", "for _ in range(k + 1):   # k stops = k+1 edges",
                          "    snap = dist[:]        # LAST round's values only",
                          "    for u, v, w in edges:", "        if snap[u] + w < dist[v]:",
                          "            dist[v] = snap[u] + w", "return dist[dst]"],
                         "cheapest 0 → " + (n - 1) + " using at most " + k + " stop(s)");
      var dist = [];
      for (i = 0; i < n; i++) dist.push(Infinity);
      dist[0] = 0;
      var show = function () {
        return dist.map(function (d, q2) { return q2 + ":" + (d === Infinity ? "∞" : d); });
      };
      t.snap(1, "k stops means k+1 EDGES, so the loop runs " + (k + 1) + " time(s). Off by one here is the " +
                "single most common failure on this problem.",
             { ptr: { src: "0" }, mark: { 0: "pick", [String(n - 1)]: "pick" },
               aux: [{ label: "dist", items: show() }, { label: "rounds", text: String(k + 1) }] });
      for (var round = 1; round <= k + 1; round++) {
        var snap = dist.slice();
        t.snap(2, "round " + round + ": take a SNAPSHOT of the distances first. Relaxing in place would let " +
                  "one round use two edges in a chain, which breaks the stop limit entirely.",
               { mark: {}, aux: [{ label: "snapshot", items: snap.map(function (d, q3) { return q3 + ":" + (d === Infinity ? "∞" : d); }) }] });
        var changed = false;
        for (j = 0; j < edges.length; j++) {
          var u = edges[j][0], to = edges[j][1], w = edges[j][2];
          if (snap[u] === Infinity) continue;
          if (snap[u] + w < dist[to]) {
            dist[to] = snap[u] + w;
            changed = true;
            t.snap(5, "edge " + u + "→" + to + " costs " + w + ": " + snap[u] + " + " + w + " = " +
                      dist[to] + " improves node " + to + ". Read from the snapshot, written to dist.",
                   { ptr: { from: String(u), to: String(to) },
                     mark: { [String(u)]: "done", [String(to)]: "pick" }, emark: { [String(j)]: "pick" },
                     aux: [{ label: "dist", items: show() }] });
          }
        }
        if (!changed) {
          t.snap(4, "round " + round + " improved nothing — everything reachable within " + round +
                    " edge(s) is already optimal.", { aux: [{ label: "dist", items: show() }] });
        }
      }
      var ans = dist[n - 1] === Infinity ? -1 : dist[n - 1];
      t.snap(6, ans < 0
             ? ("Node " + (n - 1) + " cannot be reached within " + k + " stop(s) — report −1.")
             : ("Answer " + ans + ". Unlike Dijkstra this survives NEGATIVE weights, and an extra round that " +
                "still improves something proves a negative cycle."),
             { mark: { [String(n - 1)]: ans < 0 ? "bad" : "done" },
               aux: [{ label: "dist", items: show() }, { label: "answer", text: String(ans) }] });
      return { trace: t, answer: ans };
    }
  };

  /* ================================== KRUSKAL ===================================== */

  G["dsu-kruskal"] = {
    input: [{ id: "n", label: "nodes", type: "int", def: 5 },
            { id: "edges", label: "edges  from,to,cost", type: "triples", def: "0,1,2 1,2,3 0,3,6 1,3,8 2,4,7 3,4,9" }],
    check: function (v) { return edgeCheck(v, true); },
    brute: function (v) {              /* Prim's -- a different MST algorithm */
      var inTree = [0], seen = {}, total = 0, used = 1;
      seen[0] = 1;
      while (used < v.n) {
        var best = null;
        for (var i = 0; i < v.edges.length; i++) {
          var e = v.edges[i];
          var a = seen[e[0]], b = seen[e[1]];
          if (a && !b || b && !a) if (best === null || e[2] < best[2]) best = e;
        }
        if (best === null) return -1;
        seen[best[0]] = 1; seen[best[1]] = 1;
        total += best[2]; used++;
      }
      return total;
    },
    run: function (v) {
      var n = v.n, i;
      var order = v.edges.map(function (e, idx) { return { e: e, i: idx }; })
                         .sort(function (a, b) { return a.e[2] - b.e[2] || a.i - b.i; });
      var t = graphTrace(n, v.edges,
                         ["edges.sort(key=weight)          # cheapest first", "for w, u, v in edges:",
                          "    if union(u, v):             # only if it joins two groups",
                          "        total += w;  used += 1", "        if used == n - 1: break",
                          "return total if used == n - 1 else -1   # -1: disconnected"],
                         "minimum spanning tree — connect everything, cheaply");
      var p = [];
      for (i = 0; i < n; i++) p.push(i);
      function find(x) { while (p[x] !== x) { p[x] = p[p[x]]; x = p[x]; } return x; }
      var total = 0, used = 0, emark = {}, roots = function () {
        var o = []; for (var k = 0; k < n; k++) o.push(String(find(k))); return o;
      };
      t.snap(0, "Sorted by weight: " + order.map(function (o) { return o.e[2]; }).join(", ") +
                ". The greedy claim is the cut property — the cheapest edge crossing any cut is always " +
                "safe to take.",
             { aux: [{ label: "sorted costs", items: order.map(function (o) { return String(o.e[2]); }) }] });
      for (i = 0; i < order.length; i++) {
        var e = order[i].e, ei = order[i].i;
        var ra = find(e[0]), rb = find(e[1]);
        if (ra === rb) {
          emark[String(ei)] = "bad";
          t.snap(2, "edge " + e[0] + "–" + e[1] + " (cost " + e[2] + "): both ends already lead to root " +
                    ra + ", so taking it would just close a loop. Reject it.",
                 { ptr: { a: String(e[0]), b: String(e[1]) },
                   mark: { [String(e[0])]: "bad", [String(e[1])]: "bad" },
                   emark: merge(emark, { [String(ei)]: "bad" }),
                   aux: [{ label: "total", text: String(total) }, { label: "edges used", text: used + " / " + (n - 1) }] });
          continue;
        }
        p[rb] = ra;
        total += e[2]; used++;
        emark[String(ei)] = "done";
        t.snap(3, "edge " + e[0] + "–" + e[1] + " (cost " + e[2] + ") really merges two groups — take it. " +
                  "Running total " + total + ".",
               { ptr: { a: String(e[0]), b: String(e[1]) },
                 mark: { [String(e[0])]: "done", [String(e[1])]: "done" },
                 emark: merge(emark, { [String(ei)]: "pick" }),
                 aux: [{ label: "total", text: String(total) }, { label: "edges used", text: used + " / " + (n - 1) },
                       { label: "root of each", items: roots() }] });
        if (used === n - 1) {
          t.snap(4, "a spanning tree has exactly n−1 = " + (n - 1) + " edges, so we can stop here.",
                 { emark: emark, aux: [{ label: "total", text: String(total) }] });
          break;
        }
      }
      var ans = used === n - 1 ? total : -1;
      t.snap(5, ans < 0
             ? ("Only " + used + " of the needed " + (n - 1) + " edges could be used — the graph is " +
                "DISCONNECTED, so report that rather than a partial total.")
             : ("Answer " + total + ". Remember an MST is not a shortest path: it connects everything " +
                "cheaply, it does not give the shortest route between two particular nodes."),
             { emark: emark, aux: [{ label: "answer", text: String(ans) }] });
      return { trace: t, answer: ans };
    }
  };

  /* ============================ THREE-COLOUR DFS ================================== */

  G["to-dfs"] = {
    input: [{ id: "n", label: "nodes", type: "int", def: 5 },
            { id: "edges", label: "directed a,b", type: "pairs", def: "0,1 1,2 2,3 3,1 0,4" }],
    check: function (v) { return edgeCheck(v, false); },
    brute: function (v) {              /* Kahn's indegree method -- a different algorithm */
      var indeg = [], adj = [], i;
      for (i = 0; i < v.n; i++) { indeg.push(0); adj.push([]); }
      for (i = 0; i < v.edges.length; i++) { adj[v.edges[i][0]].push(v.edges[i][1]); indeg[v.edges[i][1]]++; }
      var q = [];
      for (i = 0; i < v.n; i++) if (!indeg[i]) q.push(i);
      var out = 0;
      while (q.length) {
        var u = q.shift(); out++;
        for (i = 0; i < adj[u].length; i++) if (--indeg[adj[u][i]] === 0) q.push(adj[u][i]);
      }
      return out === v.n ? 1 : 0;
    },
    run: function (v) {
      var n = v.n, i;
      var t = graphTrace(n, v.edges,
                         ["color = [0] * n    # 0 new, 1 on this path, 2 finished", "def dfs(u):",
                          "    if color[u] == 1: return False    # back edge -> CYCLE",
                          "    if color[u] == 2: return True     # already settled",
                          "    color[u] = 1", "    for v in adj[u]: if not dfs(v): return False",
                          "    color[u] = 2;  order.append(u)    # post-order", "return order[::-1]"],
                         "three colours — is there a cycle? (edges are directed a→b)");
      var adj = [], ei = {};
      for (i = 0; i < n; i++) adj.push([]);
      for (i = 0; i < v.edges.length; i++) {
        adj[v.edges[i][0]].push(v.edges[i][1]);
        ei[v.edges[i][0] + ">" + v.edges[i][1]] = i;
      }
      var color = [];
      for (i = 0; i < n; i++) color.push(0);
      var order = [], bad = false, emark = {};
      var paint = function () {
        var m = {};
        for (var k = 0; k < n; k++) m[String(k)] = color[k] === 1 ? "pick" : (color[k] === 2 ? "done" : null);
        var o = {};
        for (var k2 in m) if (m[k2]) o[k2] = m[k2];
        return o;
      };
      t.snap(0, "Two states are not enough: 'visited' alone cannot tell a cross edge from a back edge. " +
                "The third colour is what makes cycle detection correct.", {});
      function dfs(u) {
        if (color[u] === 1) {
          bad = true;
          t.snap(2, "node " + u + " is ALREADY on the current path (colour 1) — we have walked in a " +
                    "circle. That is a back edge, and a back edge is a cycle.",
                 { ptr: { cycle: String(u) }, mark: merge(paint(), { [String(u)]: "bad" }), emark: emark });
          return false;
        }
        if (color[u] === 2) {
          t.snap(3, "node " + u + " is already finished (colour 2) — nothing below it can be a cycle, " +
                    "so stop here. This is the cross edge that two states would confuse.",
                 { ptr: { at: String(u) }, mark: paint(), emark: emark });
          return true;
        }
        color[u] = 1;
        t.snap(4, "enter node " + u + " — paint it 1: it is on the path we are currently walking.",
               { ptr: { at: String(u) }, mark: paint(), emark: emark });
        for (var j = 0; j < adj[u].length; j++) {
          var w = adj[u][j];
          emark[String(ei[u + ">" + w])] = "pick";
          if (!dfs(w)) return false;
          emark[String(ei[u + ">" + w])] = "done";
        }
        color[u] = 2;
        order.push(u);
        t.snap(6, "every edge out of node " + u + " is exhausted — paint it 2 and append it to the " +
                  "post-order list.",
               { ptr: { done: String(u) }, mark: paint(), emark: emark,
                 aux: [{ label: "post-order", items: strs(order) }] });
        return true;
      }
      for (i = 0; i < n && !bad; i++) if (color[i] === 0) dfs(i);
      t.snap(7, bad
             ? "A cycle exists, so no valid ordering is possible."
             : ("No cycle. The answer is the post-order REVERSED: " + order.slice().reverse().join(" → ") +
                ". Forgetting that reverse gives a valid-looking but wrong order."),
             { mark: paint(), emark: emark,
               aux: [{ label: "post-order", items: strs(order) },
                     { label: "topological order", items: bad ? [] : strs(order.slice().reverse()) },
                     { label: "verdict", text: bad ? "cycle" : "possible" }] });
      return { trace: t, answer: bad ? 0 : 1 };
    }
  };

  /* ========================= the last row-stage variants ========================== */

  G["gr-local"] = {
    input: [{ id: "tasks", label: "task letters", type: "word", def: "aaabbc" },
            { id: "cool", label: "cooldown", type: "int", def: 2 }],
    check: function (v) {
      if (!/^[a-z]+$/.test(v.tasks)) return "use lowercase letters, one per task";
      if (v.tasks.length > 14) return "keep it to 14 tasks or fewer";
      if (v.cool < 0 || v.cool > 6) return "cooldown must be between 0 and 6";
    },
    brute: function (v) {              /* the closed-form bound, proven for this problem */
      var cnt = {}, i, mx = 0, atMax = 0;
      for (i = 0; i < v.tasks.length; i++) cnt[v.tasks[i]] = (cnt[v.tasks[i]] || 0) + 1;
      for (var k in cnt) if (cnt[k] > mx) mx = cnt[k];
      for (k in cnt) if (cnt[k] === mx) atMax++;
      return Math.max(v.tasks.length, (mx - 1) * (v.cool + 1) + atMax);
    },
    run: function (v) {
      var tasks = v.tasks.split(""), cool = v.cool;
      var t = new Trace(tasks, ["cnt = Counter(tasks)", "while anything is left:",
                                "    for each of the cool+1 slots:", "        run the most-frequent task",
                                "        that is off cooldown", "    (idle if nothing is available)"],
                        "array", "task scheduler, cooldown " + cool + " — serve the most frequent first");
      var cnt = {}, i;
      for (i = 0; i < tasks.length; i++) cnt[tasks[i]] = (cnt[tasks[i]] || 0) + 1;
      var timeline = [], time = 0, placed = 0;
      t.snap(0, "The greedy claim: always run whatever has the MOST left. Starving the common task is what " +
                "forces idle slots later, so spending them first is provably safe.",
             { aux: [{ label: "counts", items: kv(cnt, function (k, c) { return k + "×" + c; }) }] });
      while (placed < tasks.length) {
        var cooldown = {};
        for (var slot = 0; slot <= cool && placed < tasks.length; slot++) {
          var pick = null, bestN = 0;
          for (var k in cnt) {
            if (cnt[k] > 0 && !cooldown[k] && cnt[k] > bestN) { bestN = cnt[k]; pick = k; }
          }
          if (pick === null) {
            timeline.push("—");
            time++;
            t.snap(5, "nothing is off cooldown — the CPU idles. Idle slots are the whole cost of the " +
                      "cooldown rule.",
                   { aux: [{ label: "timeline", items: timeline.slice() },
                           { label: "counts", items: kv(cnt, function (k2, c) { return k2 + "×" + c; }) }] });
            continue;
          }
          cnt[pick]--; cooldown[pick] = 1; placed++; timeline.push(pick); time++;
          t.snap(3, "run '" + pick + "' — it had the most left (" + bestN + "). " + (cnt[pick]) +
                    " of them remain, and it is now on cooldown for " + cool + " slot(s).",
                 { mark: range(0, placed - 1, "done"),
                   aux: [{ label: "timeline", items: timeline.slice() },
                         { label: "counts", items: kv(cnt, function (k3, c) { return k3 + "×" + c; }) }] });
        }
      }
      t.snap(3, "Answer " + time + " slots: " + timeline.join(" ") + ". The closed form (max-1)·(cool+1) + " +
                "ties gives the same number without simulating — but only because this greedy is provable.",
             { mark: range(0, tasks.length - 1, "done"),
               aux: [{ label: "timeline", items: timeline.slice() }, { label: "slots", text: String(time) }] });
      return { trace: t, answer: time };
    }
  };

  G["iv-insert"] = {
    input: [{ id: "iv", label: "sorted, disjoint  start,end", type: "pairs", def: "1,3 6,9" },
            { id: "neu", label: "insert  start,end", type: "pairs", def: "2,5" }],
    check: function (v) {
      if (!v.iv.length) return "give at least one existing interval";
      if (v.neu.length !== 1) return "give exactly one interval to insert, like  2,5";
      var all = v.iv.concat(v.neu);
      for (var i = 0; i < all.length; i++) {
        if (all[i][0] > all[i][1]) return "every interval needs start ≤ end";
        if (all[i][0] < 1) return "start times must be 1 or more (the clock starts at 1)";
        if (all[i][1] > 14) return "keep the clock within 14";
      }
      for (i = 1; i < v.iv.length; i++) {
        if (v.iv[i][0] <= v.iv[i - 1][1]) return "the existing list must be SORTED and non-overlapping — " +
                                                 "[" + v.iv[i - 1] + "] and [" + v.iv[i] + "] break that";
      }
      return null;
    },
    brute: function (v) {              /* merge everything from scratch */
      var all = v.iv.concat(v.neu).sort(function (a, b) { return a[0] - b[0]; });
      var out = [];
      for (var i = 0; i < all.length; i++) {
        if (out.length && all[i][0] <= out[out.length - 1][1])
          out[out.length - 1][1] = Math.max(out[out.length - 1][1], all[i][1]);
        else out.push([all[i][0], all[i][1]]);
      }
      return out.map(function (x) { return x[0] + "-" + x[1]; }).join(",");
    },
    run: function (v) {
      var iv = v.iv, neu = [v.neu[0][0], v.neu[0][1]], i;
      var hi = 0;
      for (i = 0; i < iv.length; i++) if (iv[i][1] > hi) hi = iv[i][1];
      if (neu[1] > hi) hi = neu[1];
      var cells = [];
      for (i = 1; i <= hi; i++) cells.push(i);
      var t = new Trace(cells, ["while existing ends BEFORE the new one starts:", "    copy it across",
                                "while existing starts at or before the new END:",
                                "    absorb it into the new interval", "append the new interval",
                                "copy the rest across"],
                        "timeline", "insert [" + neu[0] + "," + neu[1] + "] into a sorted, disjoint list");
      var out = [], k = 0;
      var paint = function (extra) {
        var m = {};
        for (var a = 0; a < out.length; a++) for (var x = out[a][0]; x <= out[a][1]; x++) m[x - 1] = "done";
        return merge(m, extra || {});
      };
      t.snap(0, "Three phases in order, no early return: everything strictly BEFORE, then the overlapping " +
                "middle absorbed into one, then everything strictly AFTER.",
             { span: [neu[0] - 1, neu[1] - 1], mark: range(neu[0] - 1, neu[1] - 1, "pick") });
      while (k < iv.length && iv[k][1] < neu[0]) {
        out.push([iv[k][0], iv[k][1]]);
        t.snap(1, "[" + iv[k][0] + "," + iv[k][1] + "] ends before " + neu[0] + " — it cannot touch the new " +
                  "interval, so copy it straight across.",
               { mark: paint(range(iv[k][0] - 1, iv[k][1] - 1, "done")),
                 aux: [{ label: "output", items: out.map(function (x) { return "[" + x[0] + "," + x[1] + "]"; }) }] });
        k++;
      }
      while (k < iv.length && iv[k][0] <= neu[1]) {
        var before = "[" + neu[0] + "," + neu[1] + "]";
        neu[0] = Math.min(neu[0], iv[k][0]);
        neu[1] = Math.max(neu[1], iv[k][1]);
        t.snap(3, "[" + iv[k][0] + "," + iv[k][1] + "] overlaps, so absorb it: " + before + " grows to [" +
                  neu[0] + "," + neu[1] + "]. BOTH ends can move, and it keeps growing while it overlaps.",
               { span: [neu[0] - 1, neu[1] - 1], mark: paint(range(neu[0] - 1, neu[1] - 1, "pick")),
                 aux: [{ label: "growing", text: "[" + neu[0] + "," + neu[1] + "]" }] });
        k++;
      }
      out.push(neu);
      t.snap(4, "drop the merged interval [" + neu[0] + "," + neu[1] + "] into place.",
             { mark: paint(range(neu[0] - 1, neu[1] - 1, "pick")),
               aux: [{ label: "output", items: out.map(function (x) { return "[" + x[0] + "," + x[1] + "]"; }) }] });
      while (k < iv.length) {
        out.push([iv[k][0], iv[k][1]]);
        t.snap(5, "[" + iv[k][0] + "," + iv[k][1] + "] starts after the new end — copy it across. Skipping " +
                  "this tail copy is the usual miss.",
               { mark: paint(range(iv[k][0] - 1, iv[k][1] - 1, "done")),
                 aux: [{ label: "output", items: out.map(function (x) { return "[" + x[0] + "," + x[1] + "]"; }) }] });
        k++;
      }
      t.snap(5, "Answer " + out.map(function (x) { return "[" + x[0] + "," + x[1] + "]"; }).join(" ") +
                " — still sorted and still disjoint, with no re-sorting anywhere.",
             { mark: paint(),
               aux: [{ label: "output", items: out.map(function (x) { return "[" + x[0] + "," + x[1] + "]"; }) }] });
      return { trace: t, answer: out.map(function (x) { return x[0] + "-" + x[1]; }).join(",") };
    }
  };

  G["hs-group"] = {
    input: [{ id: "words", label: "words", type: "words", def: "eat tea tan ate nat bat" }],
    check: function (v) {
      if (!v.words.length) return "give at least one word";
      if (v.words.length > 8) return "keep it to 8 words or fewer";
      for (var i = 0; i < v.words.length; i++)
        if (!/^[a-z]+$/.test(v.words[i])) return "lowercase letters only (got '" + v.words[i] + "')";
    },
    brute: function (v) {              /* pairwise comparison, no keys at all */
      var used = [], groups = 0, i, j;
      for (i = 0; i < v.words.length; i++) used.push(false);
      var isAna = function (a, b) {
        return a.split("").sort().join("") === b.split("").sort().join("");
      };
      for (i = 0; i < v.words.length; i++) {
        if (used[i]) continue;
        groups++;
        for (j = i; j < v.words.length; j++) if (!used[j] && isAna(v.words[i], v.words[j])) used[j] = true;
      }
      return groups;
    },
    run: function (v) {
      var words = v.words;
      var t = new Trace(words, ["g = defaultdict(list)", "for w in words:",
                                "    key = tuple(sorted(w))      # the invariant you invent",
                                "    g[key].append(w)", "return list(g.values())"],
                        "array", "group the anagrams — the art is choosing the KEY");
      var g = {}, order = [];
      t.snap(0, "Two items belong together exactly when your key makes them equal. Pick the key and the " +
                "problem is already solved.",
             { aux: [{ label: "buckets", items: [] }] });
      for (var i = 0; i < words.length; i++) {
        var key = words[i].split("").sort().join("");
        t.snap(2, "\"" + words[i] + "\" sorted is \"" + key + "\" — that is its normalised form. Any anagram " +
                  "of it normalises to exactly the same string.",
               { ptr: { at: String(i) }, mark: merge(range(0, i - 1, "done"), { [String(i)]: "pick" }),
                 aux: [{ label: "key", text: key },
                       { label: "buckets", items: order.map(function (k2) { return k2 + ": " + g[k2].join(","); }) }] });
        if (!g[key]) { g[key] = []; order.push(key); }
        g[key].push(words[i]);
        t.snap(3, g[key].length > 1
               ? ("bucket \"" + key + "\" already existed — \"" + words[i] + "\" joins " +
                  g[key].slice(0, -1).join(", ") + ".")
               : ("bucket \"" + key + "\" is new — \"" + words[i] + "\" founds it."),
               { ptr: { at: String(i) }, mark: range(0, i, "done"),
                 aux: [{ label: "buckets", items: order.map(function (k3) { return k3 + ": " + g[k3].join(","); }) }] });
      }
      t.snap(4, "Answer " + order.length + " group(s). Keys must be hashable and canonical — a tuple, not " +
                "a list. Sorting each word is O(len·log len); a 26-slot count tuple makes it O(len).",
             { mark: range(0, words.length - 1, "done"),
               aux: [{ label: "buckets", items: order.map(function (k4) { return k4 + ": " + g[k4].join(","); }) }] });
      return { trace: t, answer: order.length };
    }
  };
})();
