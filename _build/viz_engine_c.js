/* =====================================================================================
   VIZ ENGINE, part C  --  the GRID stage.
   Grid traversal (flood fill, BFS, multi-source) and the 2-D DP family, where the thing
   worth watching is a table or a board filling in. Loads after viz_engine.js.
   ===================================================================================== */
(function () {
  "use strict";
  var G = (typeof module !== "undefined" && module.exports)
        ? require("./viz_engine.js")
        : window.VIZGEN;
  var H = G.__helpers, Trace = H.Trace, merge = H.merge, strs = H.strs;

  var DIRS = [[1, 0], [-1, 0], [0, 1], [0, -1]];

  /* a grid Trace: data = {r, c, cells}; mark/ptr keys are "row,col" */
  function gridTrace(cells, code, caption) {
    var t = new Trace({ r: cells.length, c: cells[0].length, cells: cells }, code, "grid", caption);
    return t;
  }
  function K(r, c) { return r + "," + c; }
  function copyGrid(g) { return g.map(function (row) { return row.slice(); }); }
  function markAll(pred, g, state) {
    var m = {};
    for (var r = 0; r < g.length; r++)
      for (var c = 0; c < g[0].length; c++)
        if (pred(g[r][c], r, c)) m[K(r, c)] = state;
    return m;
  }

  /* ============================= GRID TRAVERSAL =================================== */

  G["gr-flood"] = {
    input: [{ id: "g", label: "grid rows of 0 / 1", type: "grid01", def: "11000 11000 00100 00011" }],
    check: function (v) {
      if (v.g.length > 7 || v.g[0].length > 10) return "keep the grid within 7 rows and 10 columns";
    },
    brute: function (v) {                 /* BFS components -- different traversal to run() */
      var g = copyGrid(v.g), R = g.length, C = g[0].length, n = 0;
      for (var r = 0; r < R; r++) for (var c = 0; c < C; c++) {
        if (g[r][c] !== 1) continue;
        n++;
        var q = [[r, c]]; g[r][c] = 0;
        while (q.length) {
          var cur = q.shift();
          for (var d = 0; d < 4; d++) {
            var nr = cur[0] + DIRS[d][0], nc = cur[1] + DIRS[d][1];
            if (nr >= 0 && nr < R && nc >= 0 && nc < C && g[nr][nc] === 1) { g[nr][nc] = 0; q.push([nr, nc]); }
          }
        }
      }
      return n;
    },
    run: function (v) {
      var g = copyGrid(v.g), R = g.length, C = g[0].length;
      var t = gridTrace(g.map(function (row) { return row.map(String); }),
                        ["for r in range(R):", "  for c in range(C):", "    if g[r][c] == 1:",
                         "      islands += 1; sink(r, c)", "",
                         "def sink(r, c):   # DFS", "    if out of bounds or g[r][c] != 1: return",
                         "    g[r][c] = 0                     # mark BEFORE recursing",
                         "    for each of the 4 neighbours: sink(...)"],
                        "count the islands — a grid IS a graph");
      var done = {}, islands = 0;
      t.snap(0, "Each cell is a node and each legal move is an edge. Scan for an unvisited 1; every time " +
                "you find one, a whole new region starts there.",
             { aux: [{ label: "islands", text: "0" }] });
      for (var r = 0; r < R; r++) {
        for (var c = 0; c < C; c++) {
          if (g[r][c] !== 1) continue;
          islands++;
          t.snap(3, "cell (" + r + "," + c + ") is land nobody has reached — island #" + islands +
                    " starts here. Now sink the whole thing so it is never counted twice.",
                 { ptr: { start: K(r, c) }, mark: merge(done, { [K(r, c)]: "pick" }),
                   aux: [{ label: "islands", text: String(islands) }] });
          var st = [[r, c]], sunk = 0;
          while (st.length) {
            var cur = st.pop();
            if (g[cur[0]][cur[1]] !== 1) continue;
            g[cur[0]][cur[1]] = 0;                       /* mark BEFORE recursing */
            done[K(cur[0], cur[1])] = "done";
            sunk++;
            t.snap(7, "sink (" + cur[0] + "," + cur[1] + ") — marked visited BEFORE looking at its " +
                      "neighbours. Mark after, and two adjacent cells call each other forever.",
                   { ptr: { at: K(cur[0], cur[1]) }, mark: merge(done, { [K(cur[0], cur[1])]: "pick" }),
                     aux: [{ label: "islands", text: String(islands) },
                           { label: "cells in this island", text: String(sunk) }] });
            for (var d = 0; d < 4; d++) {
              var nr = cur[0] + DIRS[d][0], nc = cur[1] + DIRS[d][1];
              if (nr >= 0 && nr < R && nc >= 0 && nc < C && g[nr][nc] === 1) st.push([nr, nc]);
            }
          }
        }
      }
      t.snap(3, "Answer " + islands + " island(s). Every cell was entered at most once, so the whole sweep " +
                "is O(rows · cols) no matter how tangled the shapes are.",
             { mark: done, aux: [{ label: "islands", text: String(islands) }] });
      return { trace: t, answer: islands };
    }
  };

  G["gr-bfs"] = {
    input: [{ id: "g", label: "grid (0 open, 1 wall)", type: "grid01", def: "00010 01010 01000 01110 00001" }],
    check: function (v) {
      if (v.g.length > 7 || v.g[0].length > 10) return "keep the grid within 7 rows and 10 columns";
      if (v.g[0][0] === 1) return "the top-left cell is a wall, so there is nowhere to start";
    },
    brute: function (v) {                 /* Dijkstra-with-equal-weights -- a different route */
      var g = v.g, R = g.length, C = g[0].length;
      var dist = g.map(function (row) { return row.map(function () { return Infinity; }); });
      dist[0][0] = 0;
      for (var it = 0; it < R * C; it++) {
        for (var r = 0; r < R; r++) for (var c = 0; c < C; c++) {
          if (g[r][c] === 1 || dist[r][c] === Infinity) continue;
          for (var d = 0; d < 4; d++) {
            var nr = r + DIRS[d][0], nc = c + DIRS[d][1];
            if (nr < 0 || nr >= R || nc < 0 || nc >= C || g[nr][nc] === 1) continue;
            if (dist[r][c] + 1 < dist[nr][nc]) dist[nr][nc] = dist[r][c] + 1;
          }
        }
      }
      return dist[R - 1][C - 1] === Infinity ? -1 : dist[R - 1][C - 1];
    },
    run: function (v) {
      var g = v.g, R = g.length, C = g[0].length;
      var show = g.map(function (row) { return row.map(function (x) { return x === 1 ? "■" : "·"; }); });
      var t = gridTrace(show,
                        ["q = deque([start]); seen = {start}", "while q:", "    for _ in range(len(q)):",
                         "        r, c = q.popleft()", "        if (r,c) == goal: return steps",
                         "        for each neighbour:", "            if open and not seen:",
                         "                seen.add(it); q.append(it)   # mark on PUSH",
                         "    steps += 1"],
                        "fewest steps from top-left to bottom-right");
      var seen = {}, q = [[0, 0]], steps = 0, found = -1;
      seen[K(0, 0)] = 0;
      var walls = markAll(function (x) { return x === 1; }, g, "bad");
      t.snap(0, "BFS finishes one whole distance ring before starting the next, which is exactly why it " +
                "returns the SHORTEST path. DFS would find a path, not the short one.",
             { ptr: { start: K(0, 0) }, mark: merge(walls, { [K(0, 0)]: "pick" }),
               aux: [{ label: "steps", text: "0" }, { label: "frontier", text: "1 cell" }] });
      while (q.length && found < 0) {
        var ring = q, nxt = [];
        for (var i = 0; i < ring.length && found < 0; i++) {
          var r = ring[i][0], c = ring[i][1];
          if (r === R - 1 && c === C - 1) { found = steps; break; }
          for (var d = 0; d < 4; d++) {
            var nr = r + DIRS[d][0], nc = c + DIRS[d][1];
            if (nr < 0 || nr >= R || nc < 0 || nc >= C) continue;
            if (g[nr][nc] === 1 || seen.hasOwnProperty(K(nr, nc))) continue;
            seen[K(nr, nc)] = steps + 1;                 /* mark on PUSH, never on pop */
            nxt.push([nr, nc]);
          }
        }
        if (found >= 0) break;
        var reached = {};
        Object.keys(seen).forEach(function (k2) { reached[k2] = "done"; });
        nxt.forEach(function (p) { reached[K(p[0], p[1])] = "pick"; });
        steps++;
        t.snap(7, nxt.length
               ? ("ring " + steps + ": " + nxt.length + " new cell(s) reached, each marked the moment it was " +
                  "PUSHED. Mark on pop instead and the same cell gets queued many times.")
               : ("ring " + steps + ": nothing new is reachable — the goal is walled off."),
               { mark: merge(walls, reached),
                 aux: [{ label: "steps", text: String(steps) }, { label: "frontier", text: nxt.length + " cells" }] });
        q = nxt;
      }
      var fin = {};
      Object.keys(seen).forEach(function (k2) { fin[k2] = "done"; });
      t.snap(4, found >= 0
             ? ("Reached the bottom-right in " + found + " steps. The first time a cell is dequeued, its " +
                "distance is already the smallest possible.")
             : "The goal is unreachable — every open cell was exhausted.",
             { mark: merge(walls, fin, found >= 0 ? { [K(R - 1, C - 1)]: "pick" } : {}),
               aux: [{ label: "answer", text: found >= 0 ? String(found) : "unreachable" }] });
      return { trace: t, answer: found };
    }
  };

  G["gr-multi"] = {
    input: [{ id: "g", label: "grid (1 = a source)", type: "grid01", def: "00100 00000 10000 00000 00001" }],
    check: function (v) {
      if (v.g.length > 7 || v.g[0].length > 10) return "keep the grid within 7 rows and 10 columns";
      var any = false;
      for (var r = 0; r < v.g.length; r++) for (var c = 0; c < v.g[0].length; c++) if (v.g[r][c] === 1) any = true;
      if (!any) return "mark at least one cell as 1 — those are the sources everything spreads from";
    },
    brute: function (v) {                 /* per-cell Manhattan scan to the nearest source */
      var g = v.g, R = g.length, C = g[0].length, worst = 0;
      for (var r = 0; r < R; r++) for (var c = 0; c < C; c++) {
        var best = Infinity;
        for (var sr = 0; sr < R; sr++) for (var sc = 0; sc < C; sc++)
          if (g[sr][sc] === 1) best = Math.min(best, Math.abs(sr - r) + Math.abs(sc - c));
        if (best > worst) worst = best;
      }
      return worst;
    },
    run: function (v) {
      var g = v.g, R = g.length, C = g[0].length, r, c;
      var show = g.map(function (row) { return row.map(function (x) { return x === 1 ? "S" : "·"; }); });
      var t = gridTrace(show,
                        ["q = deque()", "for every source cell:", "    dist = 0;  q.append(it)",
                         "while q:                      # ONE bfs, not one per source",
                         "    pop, and set each unvisited neighbour to dist + 1"],
                        "multi-source BFS — distance to the NEAREST source");
      var dist = {}, q = [];
      for (r = 0; r < R; r++) for (c = 0; c < C; c++) if (g[r][c] === 1) { dist[K(r, c)] = 0; q.push([r, c]); }
      var srcMark = markAll(function (x) { return x === 1; }, g, "done");
      t.snap(2, "All " + q.length + " source(s) go into the queue BEFORE the loop starts. That is the whole " +
                "trick: one source per BFS would be O(sources · cells) and time out.",
             { mark: srcMark, aux: [{ label: "sources", text: String(q.length) },
                                    { label: "round", text: "0" }] });
      var round = 0, worst = 0;
      while (q.length) {
        var nxt = [];
        for (var i = 0; i < q.length; i++) {
          r = q[i][0]; c = q[i][1];
          for (var d = 0; d < 4; d++) {
            var nr = r + DIRS[d][0], nc = c + DIRS[d][1];
            if (nr < 0 || nr >= R || nc < 0 || nc >= C || dist.hasOwnProperty(K(nr, nc))) continue;
            dist[K(nr, nc)] = round + 1;
            nxt.push([nr, nc]);
          }
        }
        if (!nxt.length) break;
        round++;
        worst = round;
        var m = {};
        Object.keys(dist).forEach(function (k2) { m[k2] = "done"; });
        nxt.forEach(function (p) { m[K(p[0], p[1])] = "pick"; });
        var cells2 = show.map(function (row) { return row.slice(); });
        nxt.forEach(function (p) { cells2[p[0]][p[1]] = String(round); });
        show = cells2;
        t.data.cells = show;
        t.snap(4, "round " + round + ": every fresh cell is reached from its NEAREST source, because all the " +
                  "fronts advance together. " + nxt.length + " cell(s) filled in at distance " + round + ".",
               { mark: m, aux: [{ label: "round", text: String(round) },
                                { label: "just filled", text: String(nxt.length) }] });
        q = nxt;
      }
      var all = {};
      Object.keys(dist).forEach(function (k2) { all[k2] = "done"; });
      t.snap(4, "Every cell now knows its distance to the closest source, and the furthest any cell sits is " +
                worst + ". One pass, however many sources there were.",
             { mark: all, aux: [{ label: "furthest", text: String(worst) }] });
      return { trace: t, answer: worst };
    }
  };

  /* =================================== 2-D DP ===================================== */

  G["dp-grid"] = {
    input: [{ id: "g", label: "cost grid rows", type: "gridnum", def: "131 151 422" }],
    check: function (v) {
      if (v.g.length > 6 || v.g[0].length > 8) return "keep the grid within 6 rows and 8 columns";
    },
    brute: function (v) {                 /* exhaustive over every right/down path */
      var g = v.g, R = g.length, C = g[0].length;
      var best = Infinity;
      (function go(r, c, s) {
        s += g[r][c];
        if (s >= best) return;
        if (r === R - 1 && c === C - 1) { best = Math.min(best, s); return; }
        if (r + 1 < R) go(r + 1, c, s);
        if (c + 1 < C) go(r, c + 1, s);
      })(0, 0, 0);
      return best;
    },
    run: function (v) {
      var g = v.g, R = g.length, C = g[0].length, r, c;
      var cells = g.map(function (row) { return row.map(String); });
      var t = gridTrace(cells,
                        ["for r in range(R):", "  for c in range(C):", "    if r == 0 and c == 0: dp = g[0][0]",
                         "    elif r == 0: dp[r][c] = dp[r][c-1] + g[r][c]   # top row: only from the left",
                         "    elif c == 0: dp[r][c] = dp[r-1][c] + g[r][c]   # left col: only from above",
                         "    else: dp[r][c] = min(above, left) + g[r][c]"],
                        "minimum path sum, moving only right and down");
      var dp = [];
      for (r = 0; r < R; r++) { dp.push([]); for (c = 0; c < C; c++) dp[r].push(0); }
      var done = {};
      t.snap(0, "The grid shows the COSTS. Each cell is about to be overwritten with the cheapest total " +
                "to reach it, which is why the first row and column need their own cases — they have " +
                "only one way in.", {});
      for (r = 0; r < R; r++) {
        for (c = 0; c < C; c++) {
          var line, why;
          if (r === 0 && c === 0) { dp[0][0] = g[0][0]; line = 2; why = "the start costs exactly its own value."; }
          else if (r === 0) {
            dp[r][c] = dp[r][c - 1] + g[r][c]; line = 3;
            why = "top row — the only way in is from the left: " + dp[r][c - 1] + " + " + g[r][c] + ".";
          } else if (c === 0) {
            dp[r][c] = dp[r - 1][c] + g[r][c]; line = 4;
            why = "left column — the only way in is from above: " + dp[r - 1][c] + " + " + g[r][c] + ".";
          } else {
            var up = dp[r - 1][c], lf = dp[r][c - 1];
            dp[r][c] = Math.min(up, lf) + g[r][c]; line = 5;
            why = "cheaper of above (" + up + ") and left (" + lf + ") is " + Math.min(up, lf) +
                  ", plus this cell's " + g[r][c] + " = " + dp[r][c] + ".";
          }
          cells[r][c] = String(dp[r][c]);
          done[K(r, c)] = "done";
          var look = {};
          if (r > 0 && c > 0) { look[K(r - 1, c)] = "pick"; look[K(r, c - 1)] = "pick"; }
          else if (r > 0) look[K(r - 1, c)] = "pick";
          else if (c > 0) look[K(r, c - 1)] = "pick";
          t.snap(line, "(" + r + "," + c + "): " + why,
                 { ptr: { at: K(r, c) }, mark: merge(done, look, { [K(r, c)]: "pick" }),
                   aux: [{ label: "dp here", text: String(dp[r][c]) }] });
        }
      }
      t.snap(5, "Answer " + dp[R - 1][C - 1] + " — every cell was computed once, so O(rows · cols) " +
                "instead of exploring every path.",
             { mark: merge(done, { [K(R - 1, C - 1)]: "pick" }),
               aux: [{ label: "answer", text: String(dp[R - 1][C - 1]) }] });
      return { trace: t, answer: dp[R - 1][C - 1] };
    }
  };

  G["dp-twostring"] = {
    input: [{ id: "a", label: "string A", type: "string", def: "abcde" },
            { id: "b", label: "string B", type: "string", def: "ace" }],
    check: function (v) {
      if (v.a.length > 7 || v.b.length > 7) return "keep both strings to 7 characters or fewer";
    },
    brute: function (v) {                 /* exhaustive over subsequences of A */
      var n = v.a.length, best = 0;
      for (var m = 0; m < (1 << n); m++) {
        var s = "";
        for (var i = 0; i < n; i++) if (m >> i & 1) s += v.a[i];
        /* is s a subsequence of b? */
        var j = 0;
        for (var k = 0; k < v.b.length && j < s.length; k++) if (v.b[k] === s[j]) j++;
        if (j === s.length && s.length > best) best = s.length;
      }
      return best;
    },
    run: function (v) {
      var a = v.a, b = v.b, n = a.length, m2 = b.length, i, j;
      /* row 0 / col 0 are the padding; headers live in row/col labels via the cell text */
      var cells = [];
      for (i = 0; i <= n; i++) { cells.push([]); for (j = 0; j <= m2; j++) cells[i].push("0"); }
      var t = gridTrace(cells,
                        ["dp = [[0] * (m+1) for _ in range(n+1)]   # the padding IS the base case",
                         "for i in 1..n:", "  for j in 1..m:", "    if a[i-1] == b[j-1]:",
                         "        dp[i][j] = dp[i-1][j-1] + 1      # match: consume both",
                         "    else:", "        dp[i][j] = max(dp[i-1][j], dp[i][j-1])"],
                        "longest common subsequence of \"" + a + "\" and \"" + b + "\"");
      var dp = [];
      for (i = 0; i <= n; i++) { dp.push([]); for (j = 0; j <= m2; j++) dp[i].push(0); }
      t.snap(0, "Row 0 and column 0 are padding, all zeros: an empty string shares nothing with anything. " +
                "Row i means 'the first i characters of \"" + a + "\"', column j the first j of \"" + b + "\". " +
                "That shift is why the code reads a[i-1], not a[i].",
             { mark: (function () {
                 var mm = {};
                 for (var q = 0; q <= m2; q++) mm[K(0, q)] = "done";
                 for (var p = 0; p <= n; p++) mm[K(p, 0)] = "done";
                 return mm;
               })() });
      var done = {};
      for (i = 0; i <= m2; i++) done[K(0, i)] = "done";
      for (i = 0; i <= n; i++) done[K(i, 0)] = "done";
      for (i = 1; i <= n; i++) {
        for (j = 1; j <= m2; j++) {
          var match = a[i - 1] === b[j - 1];
          if (match) dp[i][j] = dp[i - 1][j - 1] + 1;
          else dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
          cells[i][j] = String(dp[i][j]);
          done[K(i, j)] = "done";
          var look = match ? { [K(i - 1, j - 1)]: "pick" }
                           : merge({ [K(i - 1, j)]: "pick" }, { [K(i, j - 1)]: "pick" });
          t.snap(match ? 4 : 6,
                 "'" + a[i - 1] + "' vs '" + b[j - 1] + "': " +
                 (match ? ("they MATCH, so take the diagonal (" + dp[i - 1][j - 1] + ") and add one → " + dp[i][j] + ".")
                        : ("no match, so drop one character — the better of above (" + dp[i - 1][j] +
                           ") and left (" + dp[i][j - 1] + ") → " + dp[i][j] + ".")),
                 { ptr: { at: K(i, j) }, mark: merge(done, look, { [K(i, j)]: "pick" }),
                   aux: [{ label: "A[0:i]", text: a.slice(0, i) }, { label: "B[0:j]", text: b.slice(0, j) },
                         { label: "dp", text: String(dp[i][j]) }] });
        }
      }
      t.snap(6, "Answer " + dp[n][m2] + " — the bottom-right cell. Note a SUBSTRING problem would reset " +
                "to 0 on a mismatch instead of taking a max; that one character of difference is a whole " +
                "different problem.",
             { mark: merge(done, { [K(n, m2)]: "pick" }),
               aux: [{ label: "LCS length", text: String(dp[n][m2]) }] });
      return { trace: t, answer: dp[n][m2] };
    }
  };

  G["dp-knapsack"] = {
    input: [{ id: "w", label: "item weights", type: "ints", def: "1 3 4 5" },
            { id: "cap", label: "capacity", type: "int", def: 7 }],
    check: function (v) {
      if (v.w.length > 6) return "keep it to 6 items or fewer";
      if (v.cap < 0 || v.cap > 12) return "keep the capacity between 0 and 12";
      for (var i = 0; i < v.w.length; i++) if (v.w[i] < 1) return "weights must be at least 1";
    },
    brute: function (v) {                 /* exhaustive subsets */
      var n = v.w.length, best = 0;
      for (var m = 0; m < (1 << n); m++) {
        var s = 0;
        for (var i = 0; i < n; i++) if (m >> i & 1) s += v.w[i];
        if (s <= v.cap && s > best) best = s;
      }
      return best;
    },
    run: function (v) {
      var w = v.w, cap = v.cap, n = w.length, i, c;
      var cells = [];
      for (i = 0; i <= n; i++) { cells.push([]); for (c = 0; c <= cap; c++) cells[i].push("0"); }
      var t = gridTrace(cells,
                        ["dp[0][*] = 0                       # no items -> fill nothing",
                         "for i in 1..n:", "  for c in 0..cap:", "    skip = dp[i-1][c]",
                         "    take = dp[i-1][c - w[i-1]] + w[i-1]   if it fits",
                         "    dp[i][c] = max(skip, take)"],
                        "0/1 knapsack — rows are items, columns are capacity 0.." + cap);
      var dp = [];
      for (i = 0; i <= n; i++) { dp.push([]); for (c = 0; c <= cap; c++) dp[i].push(0); }
      var done = {};
      for (c = 0; c <= cap; c++) done[K(0, c)] = "done";
      t.snap(0, "Row 0 is 'no items available', so every capacity holds 0. Each later row adds exactly one " +
                "item to the choice set — which is what guarantees each item is used AT MOST ONCE.",
             { mark: done, aux: [{ label: "weights", items: strs(w) }] });
      for (i = 1; i <= n; i++) {
        for (c = 0; c <= cap; c++) {
          var skip = dp[i - 1][c];
          var fits = w[i - 1] <= c;
          var take = fits ? dp[i - 1][c - w[i - 1]] + w[i - 1] : -1;
          dp[i][c] = Math.max(skip, take);
          cells[i][c] = String(dp[i][c]);
          done[K(i, c)] = "done";
          var look = { [K(i - 1, c)]: "pick" };
          if (fits) look[K(i - 1, c - w[i - 1])] = "pick";
          t.snap(5, "item " + i + " (weight " + w[i - 1] + ") at capacity " + c + ": skip it → " + skip +
                    (fits ? ("; or take it → " + dp[i - 1][c - w[i - 1]] + " + " + w[i - 1] + " = " + take +
                             ". Both look at the row ABOVE, never this row — that is the one-use rule.")
                          : "; it does not fit in " + c + ", so skipping is the only option."),
                 { ptr: { at: K(i, c) }, mark: merge(done, look, { [K(i, c)]: "pick" }),
                   aux: [{ label: "best here", text: String(dp[i][c]) }] });
        }
      }
      t.snap(5, "Answer " + dp[n][cap] + " — the most weight that fits. The flattened 1-D version loops " +
                "capacity BACKWARD for exactly the reason you can see here: it must read the previous row, " +
                "not the one it is writing.",
             { mark: merge(done, { [K(n, cap)]: "pick" }),
               aux: [{ label: "answer", text: String(dp[n][cap]) }] });
      return { trace: t, answer: dp[n][cap] };
    }
  };

  G["dp-interval"] = {
    input: [{ id: "a", label: "balloon values", type: "ints", def: "3 1 5 8" }],
    check: function (v) {
      if (v.a.length > 5) return "keep it to 5 balloons or fewer — the table is n³ work";
      if (!v.a.length) return "give at least one balloon";
      for (var i = 0; i < v.a.length; i++) if (v.a[i] < 0) return "values cannot be negative";
    },
    brute: function (v) {                 /* try every popping order */
      var best = 0;
      (function go(arr, got) {
        if (!arr.length) { if (got > best) best = got; return; }
        for (var i = 0; i < arr.length; i++) {
          var l = i > 0 ? arr[i - 1] : 1, r = i < arr.length - 1 ? arr[i + 1] : 1;
          go(arr.slice(0, i).concat(arr.slice(i + 1)), got + l * arr[i] * r);
        }
      })(v.a.slice(), 0);
      return best;
    },
    run: function (v) {
      var pad = [1].concat(v.a, [1]), n = pad.length, l, r, k;
      var cells = [];
      for (l = 0; l < n; l++) { cells.push([]); for (r = 0; r < n; r++) cells[l].push("·"); }
      var t = gridTrace(cells,
                        ["a = [1] + nums + [1]          # virtual balloons at both ends",
                         "for length in 2..n-1:         # LENGTH on the outside",
                         "  for l in 0..n-length-1:", "    r = l + length",
                         "    for k in l+1..r-1:        # k = the LAST balloon popped in (l, r)",
                         "      dp[l][r] = max(dp[l][r], dp[l][k] + a[l]*a[k]*a[r] + dp[k][r])"],
                        "burst balloons — the table is dp[left][right]");
      var dp = [];
      for (l = 0; l < n; l++) { dp.push([]); for (r = 0; r < n; r++) dp[l].push(0); }
      t.snap(0, "Padded with 1s at both ends, so no boundary checks. dp[l][r] = the best you can get by " +
                "popping everything strictly BETWEEN l and r. Only the upper triangle is ever used.", {});
      t.snap(4, "The reframing that makes this work: k is the LAST balloon popped in the range, not the " +
                "first. Then its neighbours are exactly a[l] and a[r], which are still standing.", {});
      var done = {};
      for (var length = 2; length < n; length++) {
        for (l = 0; l + length < n; l++) {
          r = l + length;
          for (k = l + 1; k < r; k++) {
            var cand = dp[l][k] + pad[l] * pad[k] * pad[r] + dp[k][r];
            if (cand > dp[l][r]) dp[l][r] = cand;
          }
          cells[l][r] = String(dp[l][r]);
          done[K(l, r)] = "done";
          t.snap(5, "range (" + l + "," + r + "), width " + length + ": trying every balloon inside as the " +
                    "last one popped gives " + dp[l][r] + ". Every shorter range it reads is already filled — " +
                    "that is why LENGTH is the outer loop.",
                 { ptr: { l: K(l, r) }, mark: merge(done, { [K(l, r)]: "pick" }),
                   aux: [{ label: "dp[" + l + "][" + r + "]", text: String(dp[l][r]) }] });
        }
      }
      t.snap(5, "Answer " + dp[0][n - 1] + " — the whole range. Iterating l and r in the natural order " +
                "instead would read cells that have not been filled yet.",
             { mark: merge(done, { [K(0, n - 1)]: "pick" }),
               aux: [{ label: "answer", text: String(dp[0][n - 1]) }] });
      return { trace: t, answer: dp[0][n - 1] };
    }
  };

  G["bk-board"] = {
    input: [{ id: "n", label: "board size n", type: "int", def: 5 }],
    check: function (v) {
      if (v.n < 1 || v.n > 6) return "use a board between 1 and 6 — bigger boards make far too many frames";
    },
    brute: function (v) {                 /* count solutions by brute permutation check */
      var n = v.n, count = 0, col = [];
      (function go(r) {
        if (r === n) { count++; return; }
        for (var c = 0; c < n; c++) {
          var ok = true;
          for (var i = 0; i < r; i++)
            if (col[i] === c || Math.abs(col[i] - c) === r - i) { ok = false; break; }
          if (ok) { col[r] = c; go(r + 1); }
        }
      })(0);
      return count;
    },
    run: function (v) {
      var n = v.n, cells = [], r, c;
      for (r = 0; r < n; r++) { cells.push([]); for (c = 0; c < n; c++) cells[r].push("·"); }
      var t = gridTrace(cells,
                        ["def go(r):", "    if r == n: solutions += 1; return", "    for c in range(n):",
                         "        if c in cols or r-c in diag or r+c in anti: continue",
                         "        place(r, c);  go(r + 1);  remove(r, c)"],
                        "n-queens on a " + n + "×" + n + " board");
      var cols = {}, diag = {}, anti = {}, placed = [], solutions = 0, frames = 0;
      var LIMIT = 260;                       /* keep the trace watchable */
      function marks(extra) {
        var m = {};
        for (var i = 0; i < placed.length; i++) m[K(i, placed[i])] = "done";
        return merge(m, extra || {});
      }
      function go(r2) {
        if (r2 === n) {
          solutions++;
          if (frames < LIMIT) {
            frames++;
            t.snap(1, "all " + n + " queens placed with no two attacking — solution #" + solutions + ".",
                   { mark: marks(), aux: [{ label: "solutions", text: String(solutions) }] });
          }
          return;
        }
        for (var c2 = 0; c2 < n; c2++) {
          var clash = cols[c2] || diag[r2 - c2] || anti[r2 + c2];
          if (clash) {
            if (frames < LIMIT) {
              frames++;
              t.snap(3, "row " + r2 + ", column " + c2 + " is attacked — " +
                        (cols[c2] ? "same column" : (diag[r2 - c2] ? "same diagonal (r−c)" : "same anti-diagonal (r+c)")) +
                        ". Identifying diagonals by r−c and r+c makes this test O(1), which is the whole " +
                        "reason n-queens finishes.",
                     { ptr: { try: K(r2, c2) }, mark: marks({ [K(r2, c2)]: "bad" }),
                       aux: [{ label: "solutions", text: String(solutions) }] });
            }
            continue;
          }
          cols[c2] = 1; diag[r2 - c2] = 1; anti[r2 + c2] = 1; placed.push(c2);
          if (frames < LIMIT) {
            frames++;
            t.snap(4, "place a queen at row " + r2 + ", column " + c2 + ", then recurse into row " + (r2 + 1) + ".",
                   { ptr: { queen: K(r2, c2) }, mark: marks({ [K(r2, c2)]: "pick" }),
                     aux: [{ label: "solutions", text: String(solutions) }] });
          }
          go(r2 + 1);
          placed.pop(); delete cols[c2]; delete diag[r2 - c2]; delete anti[r2 + c2];
          if (frames < LIMIT) {
            frames++;
            t.snap(4, "that branch is exhausted — REMOVE the queen from row " + r2 + " and try the next " +
                      "column. Restoring exactly, in reverse order, is what keeps every later branch honest.",
                   { mark: marks({ [K(r2, c2)]: "gone" }),
                     aux: [{ label: "solutions", text: String(solutions) }] });
          }
        }
      }
      t.snap(0, "Place one queen per row, left to right. The only state you need is which columns and which " +
                "two diagonal families are already taken.", {});
      go(0);
      t.snap(1, "Answer " + solutions + " solution(s) on a " + n + "×" + n + " board" +
                (frames >= LIMIT ? " (the trace stopped recording after " + LIMIT + " frames, but the search ran to the end)." : "."),
             { aux: [{ label: "solutions", text: String(solutions) }] });
      return { trace: t, answer: solutions };
    }
  };
})();
