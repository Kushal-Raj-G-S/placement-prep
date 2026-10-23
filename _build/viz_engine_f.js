/* =====================================================================================
   VIZ ENGINE, part F  --  the last sixteen variants, so every variant in Pattern Radar
   has a trace. Uses the grid stage for anything needing two or more rows (merging,
   partitioning, matrices) and the row stage for the rest.
   ===================================================================================== */
(function () {
  "use strict";
  var G = (typeof module !== "undefined" && module.exports)
        ? require("./viz_engine.js")
        : window.VIZGEN;
  var H = G.__helpers, Trace = H.Trace, range = H.range, merge = H.merge, kv = H.kv, strs = H.strs;

  function K(r, c) { return r + "," + c; }
  function gridT(cells, code, caption) {
    return new Trace({ r: cells.length, c: cells[0].length, cells: cells }, code, "grid", caption);
  }
  function pad(rows) {                       /* rectangular grid from ragged rows */
    var w = 0, i;
    for (i = 0; i < rows.length; i++) w = Math.max(w, rows[i].length);
    return rows.map(function (r) {
      var out = r.slice();
      while (out.length < w) out.push("");
      return out;
    });
  }

  /* ============================ two rows: merging ================================= */

  G["tp-merge"] = {
    input: [{ id: "a", label: "sorted A", type: "ints", def: "1 2 4 7" },
            { id: "b", label: "sorted B", type: "ints", def: "2 4 5" }],
    prep: function (v) {
      var wasA = v.a.join(" "), wasB = v.b.join(" ");
      v.a = v.a.slice().sort(function (x, y) { return x - y; });
      v.b = v.b.slice().sort(function (x, y) { return x - y; });
      return (wasA === v.a.join(" ") && wasB === v.b.join(" ")) ? null
           : "sorted both inputs first — this variant walks two ALREADY sorted sequences";
    },
    check: function (v) {
      if (v.a.length > 8 || v.b.length > 8) return "keep each sequence to 8 numbers or fewer";
    },
    brute: function (v) {              /* set intersection, no pointers at all */
      var seen = {}, out = [], i;
      for (i = 0; i < v.b.length; i++) seen[v.b[i]] = (seen[v.b[i]] || 0) + 1;
      for (i = 0; i < v.a.length; i++) if (seen[v.a[i]] > 0) { out.push(v.a[i]); seen[v.a[i]]--; }
      return out.join(",");
    },
    run: function (v) {
      var a = v.a, b = v.b;
      var t = gridT(pad([a.map(String), b.map(String)]),
                    ["while i < len(a) and j < len(b):", "    if a[i] == b[j]: take it; i += 1; j += 1",
                     "    elif a[i] < b[j]: i += 1      # a[i] can never appear later in b",
                     "    else: j += 1"],
                    "one pointer per sequence — the intersection");
      var i = 0, j = 0, out = [];
      t.snap(0, "Top row is A, bottom row is B. Because both are sorted, whichever side is behind can be " +
                "advanced without ever having to look back.",
             { ptr: { i: K(0, 0), j: K(1, 0) }, mark: { [K(0, 0)]: "pick", [K(1, 0)]: "pick" } });
      while (i < a.length && j < b.length) {
        if (a[i] === b[j]) {
          out.push(a[i]);
          t.snap(1, a[i] + " = " + b[j] + " — a match. Take it and advance BOTH.",
                 { ptr: { i: K(0, i), j: K(1, j) },
                   mark: merge({ [K(0, i)]: "done" }, { [K(1, j)]: "done" }),
                   aux: [{ label: "output", items: strs(out) }] });
          i++; j++;
        } else if (a[i] < b[j]) {
          t.snap(2, a[i] + " < " + b[j] + ", and B only grows from here — so " + a[i] +
                    " can never appear later in B. Discard it and move i.",
                 { ptr: { i: K(0, i), j: K(1, j) },
                   mark: merge({ [K(0, i)]: "bad" }, { [K(1, j)]: "pick" }),
                   aux: [{ label: "output", items: strs(out) }] });
          i++;
        } else {
          t.snap(3, b[j] + " < " + a[i] + " — same argument the other way round. Move j.",
                 { ptr: { i: K(0, i), j: K(1, j) },
                   mark: merge({ [K(0, i)]: "pick" }, { [K(1, j)]: "bad" }),
                   aux: [{ label: "output", items: strs(out) }] });
          j++;
        }
      }
      t.snap(0, "One sequence ran out, so nothing more can match. Answer [" + out.join(", ") +
                "] in O(n + m) — and for a MERGE rather than an intersection, this is where you append " +
                "the leftover tail, which is the usual thing people forget.",
             { aux: [{ label: "output", items: strs(out) }] });
      return { trace: t, answer: out.join(",") };
    }
  };

  G["ll-merge"] = {
    input: [{ id: "a", label: "list A values", type: "ints", def: "1 2 4" },
            { id: "b", label: "list B values", type: "ints", def: "1 3 4" }],
    prep: function (v) {
      v.a = v.a.slice().sort(function (x, y) { return x - y; });
      v.b = v.b.slice().sort(function (x, y) { return x - y; });
      return null;
    },
    check: function (v) {
      if (v.a.length > 8 || v.b.length > 8) return "keep each list to 8 nodes or fewer";
    },
    brute: function (v) { return v.a.concat(v.b).sort(function (x, y) { return x - y; }).join(","); },
    run: function (v) {
      var a = v.a, b = v.b;
      var t = gridT(pad([a.map(String), b.map(String)]),
                    ["dummy = tail = ListNode(0)", "while a and b:",
                     "    pick the smaller head; tail.next = it", "    tail = tail.next",
                     "tail.next = a or b          # the leftover tail, attached WHOLE",
                     "return dummy.next"],
                    "merge two sorted lists onto a dummy head");
      var i = 0, j = 0, out = [];
      t.snap(0, "A dummy head means the real head needs no special case — you return dummy.next at the end " +
                "and never ask 'was this the first node'.",
             { ptr: { a: K(0, 0), b: K(1, 0) }, aux: [{ label: "merged", items: [] }] });
      while (i < a.length && j < b.length) {
        var takeA = a[i] <= b[j];
        out.push(takeA ? a[i] : b[j]);
        t.snap(2, (takeA ? ("A's head " + a[i] + " ≤ B's head " + b[j]) : ("B's head " + b[j] + " < A's head " + a[i])) +
                  " — append it and advance that side only. Using ≤ rather than < keeps the merge stable.",
               { ptr: { a: K(0, Math.min(i, a.length - 1)), b: K(1, Math.min(j, b.length - 1)) },
                 mark: merge({ [K(takeA ? 0 : 1, takeA ? i : j)]: "done" }),
                 aux: [{ label: "merged", items: strs(out) }] });
        if (takeA) i++; else j++;
      }
      var restRow = i < a.length ? 0 : 1, rest = i < a.length ? a.slice(i) : b.slice(j);
      if (rest.length) {
        for (var q = 0; q < rest.length; q++) out.push(rest[q]);
        t.snap(4, "one list is empty but the other still has " + rest.length + " node(s) — attach that tail " +
                  "WHOLE in one assignment. Forgetting this line silently truncates the result.",
               { mark: (function () {
                   var m = {};
                   var from = restRow === 0 ? i : j, len = restRow === 0 ? a.length : b.length;
                   for (var z = from; z < len; z++) m[K(restRow, z)] = "pick";
                   return m;
                 })(),
                 aux: [{ label: "merged", items: strs(out) }] });
      }
      t.snap(5, "Answer " + out.join(" → ") + ", in O(n + m) with no extra nodes allocated.",
             { aux: [{ label: "merged", items: strs(out) }] });
      return { trace: t, answer: out.join(",") };
    }
  };

  G["hp-merge"] = {
    input: [{ id: "rows", label: "k sorted lists (one per row)", type: "rows", def: "1,4,5 1,3,4 2,6" }],
    check: function (v) {
      if (!v.rows.length) return "give at least one list";
      if (v.rows.length > 5) return "keep it to 5 lists or fewer so the drawing stays readable";
      for (var i = 0; i < v.rows.length; i++) {
        if (v.rows[i].length > 7) return "keep each list to 7 numbers or fewer";
        for (var j = 1; j < v.rows[i].length; j++)
          if (v.rows[i][j] < v.rows[i][j - 1]) return "row " + (i + 1) + " is not sorted — every list must " +
                                                      "already be in order for this to work";
      }
      return null;
    },
    brute: function (v) {
      var all = [];
      for (var i = 0; i < v.rows.length; i++) all = all.concat(v.rows[i]);
      return all.sort(function (a, b) { return a - b; }).join(",");
    },
    run: function (v) {
      var rows = v.rows, k = rows.length;
      var t = gridT(pad(rows.map(function (r) { return r.map(String); })),
                    ["h = [(list[0], i, 0) for each non-empty list]", "heapify(h)", "while h:",
                     "    val, i, j = heappop(h)      # smallest live head",
                     "    out.append(val)", "    if j+1 < len(list i): push (list[i][j+1], i, j+1)"],
                    "merge " + k + " sorted lists with a heap of the current heads");
      var heap = [], out = [], used = {}, i;
      for (i = 0; i < k; i++) if (rows[i].length) heap.push([rows[i][0], i, 0]);
      var heads = function () {
        var m = {};
        for (var z = 0; z < heap.length; z++) m[K(heap[z][1], heap[z][2])] = "pick";
        return merge(used, m);
      };
      t.snap(1, "Seed the heap with one entry per list — its current head. The heap only ever holds " + k +
                " things, which is what makes this O(N log k) instead of O(N log N).",
             { mark: heads(),
               aux: [{ label: "heap", items: heap.map(function (x) { return x[0] + "@L" + (x[1] + 1); }) }] });
      while (heap.length) {
        heap.sort(function (x, y) { return x[0] - y[0] || x[1] - y[1]; });
        var top = heap.shift();
        out.push(top[0]);
        used[K(top[1], top[2])] = "done";
        t.snap(3, "smallest live head is " + top[0] + " from list " + (top[1] + 1) + " — pop it into the output.",
               { ptr: { out: K(top[1], top[2]) }, mark: merge(heads(), { [K(top[1], top[2])]: "pick" }),
                 aux: [{ label: "output", items: strs(out) }] });
        if (top[2] + 1 < rows[top[1]].length) {
          heap.push([rows[top[1]][top[2] + 1], top[1], top[2] + 1]);
          t.snap(5, "list " + (top[1] + 1) + " still has more, so push its next value (" +
                    rows[top[1]][top[2] + 1] + "). The index travels with the value — without it you " +
                    "could not find the successor.",
                 { mark: heads(),
                   aux: [{ label: "heap", items: heap.map(function (x) { return x[0] + "@L" + (x[1] + 1); }) }] });
        }
      }
      t.snap(4, "Answer " + out.join(", ") + ".",
             { mark: used, aux: [{ label: "output", items: strs(out) }] });
      return { trace: t, answer: out.join(",") };
    }
  };

  G["bs-partition"] = {
    input: [{ id: "a", label: "sorted A", type: "ints", def: "1 3 8" },
            { id: "b", label: "sorted B", type: "ints", def: "7 9 10 11" }],
    prep: function (v) {
      v.a = v.a.slice().sort(function (x, y) { return x - y; });
      v.b = v.b.slice().sort(function (x, y) { return x - y; });
      return null;
    },
    check: function (v) {
      if (!v.a.length || !v.b.length) return "both arrays need at least one number";
      if (v.a.length > 7 || v.b.length > 7) return "keep each array to 7 numbers or fewer";
    },
    brute: function (v) {              /* merge everything and read the middle */
      var all = v.a.concat(v.b).sort(function (x, y) { return x - y; });
      var n = all.length;
      return n % 2 ? String(all[(n - 1) / 2]) : String((all[n / 2 - 1] + all[n / 2]) / 2);
    },
    run: function (v) {
      var a = v.a, b = v.b;
      if (a.length > b.length) { var sw = a; a = b; b = sw; }
      var n = a.length, m = b.length, half = Math.floor((n + m + 1) / 2);
      var t = gridT(pad([a.map(String), b.map(String)]),
                    ["if len(a) > len(b): swap     # always search the SHORTER",
                     "lo, hi = 0, n", "while lo <= hi:", "    i = (lo + hi) // 2;  j = half - i",
                     "    if aL <= bR and bL <= aR: found the split",
                     "    elif aL > bR: hi = i - 1", "    else: lo = i + 1"],
                    "median of two sorted arrays — search the SPLIT, not an element");
      var lo = 0, hi = n, ans = null;
      t.snap(0, "Always binary search the shorter array (top row), or the partner index runs off the end. " +
                "We are not looking for a value here — we are looking for where to CUT.",
             { aux: [{ label: "left side must hold", text: half + " of " + (n + m) }] });
      while (lo <= hi) {
        var i = (lo + hi) >> 1, j = half - i;
        var aL = i > 0 ? a[i - 1] : -Infinity, aR = i < n ? a[i] : Infinity;
        var bL = j > 0 ? b[j - 1] : -Infinity, bR = j < m ? b[j] : Infinity;
        var mk = {};
        for (var z = 0; z < i; z++) mk[K(0, z)] = "done";
        for (z = 0; z < j; z++) mk[K(1, z)] = "done";
        var f = function (x) { return x === Infinity ? "+∞" : (x === -Infinity ? "−∞" : String(x)); };
        t.snap(3, "take " + i + " from A and " + j + " from B for the left side. Edges: A gives " + f(aL) +
                  " | " + f(aR) + ", B gives " + f(bL) + " | " + f(bR) + ". The ±∞ sentinels replace " +
                  "four boundary ifs — write them, do not branch.",
               { ptr: { i: K(0, Math.min(i, n - 1)), j: K(1, Math.min(j, m - 1)) }, mark: mk,
                 aux: [{ label: "take from A", text: String(i) }, { label: "take from B", text: String(j) }] });
        if (aL <= bR && bL <= aR) {
          ans = (n + m) % 2 ? Math.max(aL, bL) : (Math.max(aL, bL) + Math.min(aR, bR)) / 2;
          t.snap(4, "every left element is ≤ every right element — this is the correct cut. " +
                    ((n + m) % 2 ? "Odd total, so the median is the larger left edge: " + ans + "."
                                 : "Even total, so average the two inner edges: " + ans + "."),
                 { mark: mk, aux: [{ label: "median", text: String(ans) }] });
          break;
        }
        if (aL > bR) {
          t.snap(5, "A's left edge " + f(aL) + " is too big for B's right " + f(bR) +
                    " — we took too many from A, so move the cut left.",
                 { mark: mk });
          hi = i - 1;
        } else {
          t.snap(6, "B's left edge " + f(bL) + " is too big for A's right " + f(aR) +
                    " — we took too few from A, so move the cut right.",
                 { mark: mk });
          lo = i + 1;
        }
      }
      t.snap(4, "Answer " + ans + ", in O(log min(n, m)) — this one is worth memorising rather than " +
                "deriving under exam pressure.",
             { aux: [{ label: "median", text: String(ans) }] });
      return { trace: t, answer: String(ans) };
    }
  };

  /* ================================= matrices ===================================== */

  G["ps-2d"] = {
    input: [{ id: "g", label: "matrix rows", type: "gridnum", def: "312 151 422" },
            { id: "q", label: "rectangle  r1,c1,r2,c2", type: "quad", def: "1,0,2,1" }],
    check: function (v) {
      if (v.g.length > 5 || v.g[0].length > 6) return "keep the matrix within 5 rows and 6 columns";
      var q = v.q;
      if (q[0] > q[2] || q[1] > q[3]) return "the rectangle needs r1 ≤ r2 and c1 ≤ c2";
      if (q[2] >= v.g.length || q[3] >= v.g[0].length || q[0] < 0 || q[1] < 0)
        return "the rectangle must sit inside the matrix (rows 0.." + (v.g.length - 1) +
               ", cols 0.." + (v.g[0].length - 1) + ")";
      return null;
    },
    brute: function (v) {
      var s = 0;
      for (var r = v.q[0]; r <= v.q[2]; r++) for (var c = v.q[1]; c <= v.q[3]; c++) s += v.g[r][c];
      return s;
    },
    run: function (v) {
      var g = v.g, R = g.length, C = g[0].length, r, c;
      var cells = [];
      for (r = 0; r <= R; r++) { cells.push([]); for (c = 0; c <= C; c++) cells[r].push("0"); }
      var t = gridT(cells,
                    ["pre[i+1][j+1] = g[i][j] + pre[i][j+1] + pre[i+1][j] - pre[i][j]", "",
                     "rect(r1,c1,r2,c2) = pre[r2+1][c2+1]", "                  - pre[r1][c2+1]",
                     "                  - pre[r2+1][c1]", "                  + pre[r1][c1]"],
                    "2-D prefix sums (padded with a zero row and column)");
      var pre = [];
      for (r = 0; r <= R; r++) { pre.push([]); for (c = 0; c <= C; c++) pre[r].push(0); }
      var done = {};
      for (c = 0; c <= C; c++) done[K(0, c)] = "done";
      for (r = 0; r <= R; r++) done[K(r, 0)] = "done";
      t.snap(0, "The pad of zeros along the top and left removes every boundary check from the query. " +
                "pre[i][j] will hold the sum of the whole rectangle above-and-left of (i, j), exclusive.",
             { mark: done });
      for (r = 0; r < R; r++) {
        for (c = 0; c < C; c++) {
          pre[r + 1][c + 1] = g[r][c] + pre[r][c + 1] + pre[r + 1][c] - pre[r][c];
          cells[r + 1][c + 1] = String(pre[r + 1][c + 1]);
          done[K(r + 1, c + 1)] = "done";
          t.snap(0, "pre[" + (r + 1) + "][" + (c + 1) + "] = value " + g[r][c] + " + above " + pre[r][c + 1] +
                    " + left " + pre[r + 1][c] + " − corner " + pre[r][c] + " = " + pre[r + 1][c + 1] +
                    ". Inclusion–exclusion: the corner was counted twice, so subtract it once.",
                 { ptr: { at: K(r + 1, c + 1) },
                   mark: merge(done, { [K(r, c + 1)]: "pick" }, { [K(r + 1, c)]: "pick" }, { [K(r, c)]: "bad" },
                               { [K(r + 1, c + 1)]: "pick" }) });
        }
      }
      var q = v.q, r1 = q[0], c1 = q[1], r2 = q[2], c2 = q[3];
      var ans = pre[r2 + 1][c2 + 1] - pre[r1][c2 + 1] - pre[r2 + 1][c1] + pre[r1][c1];
      t.snap(2, "now the query (" + r1 + "," + c1 + ")–(" + r2 + "," + c2 + "): start from the big " +
                "rectangle pre[" + (r2 + 1) + "][" + (c2 + 1) + "] = " + pre[r2 + 1][c2 + 1] + ".",
             { span: [r1 + 1, c1 + 1, r2 + 1, c2 + 1], mark: merge(done, { [K(r2 + 1, c2 + 1)]: "pick" }) });
      t.snap(4, "subtract the strip above (" + pre[r1][c2 + 1] + ") and the strip to the left (" +
                pre[r2 + 1][c1] + ")...",
             { mark: merge(done, { [K(r1, c2 + 1)]: "bad" }, { [K(r2 + 1, c1)]: "bad" }) });
      t.snap(5, "...then ADD BACK the corner (" + pre[r1][c1] + "), which you just removed twice. " +
                "Answer " + ans + ", in O(1) however big the rectangle.",
             { span: [r1 + 1, c1 + 1, r2 + 1, c2 + 1],
               mark: merge(done, { [K(r1, c1)]: "pick" }),
               aux: [{ label: "rect sum", text: String(ans) }] });
      return { trace: t, answer: ans };
    }
  };

  G["sp-floyd"] = {
    input: [{ id: "n", label: "nodes", type: "int", def: 4 },
            { id: "edges", label: "edges  from,to,weight", type: "triples", def: "0,1,3 1,2,1 2,3,2 0,3,10" }],
    check: function (v) {
      if (v.n < 2 || v.n > 5) return "use between 2 and 5 nodes — the table is n³ work";
      if (!v.edges.length) return "give at least one edge";
      for (var i = 0; i < v.edges.length; i++) {
        var e = v.edges[i];
        if (e[0] < 0 || e[1] < 0 || e[0] >= v.n || e[1] >= v.n) return "edge uses a node outside 0.." + (v.n - 1);
        if (e.length < 3 || e[2] < 0) return "every edge needs a non-negative weight: from,to,weight";
      }
      return null;
    },
    brute: function (v) {              /* BFS/Dijkstra per source -- a different algorithm */
      var i, out = [];
      for (var s = 0; s < v.n; s++) {
        var dist = [];
        for (i = 0; i < v.n; i++) dist.push(Infinity);
        dist[s] = 0;
        for (var it = 0; it < v.n; it++)
          for (i = 0; i < v.edges.length; i++) {
            var e = v.edges[i];
            if (dist[e[0]] + e[2] < dist[e[1]]) dist[e[1]] = dist[e[0]] + e[2];
            if (dist[e[1]] + e[2] < dist[e[0]]) dist[e[0]] = dist[e[1]] + e[2];
          }
        out.push(dist.map(function (d) { return d === Infinity ? "i" : d; }).join("."));
      }
      return out.join("|");
    },
    run: function (v) {
      var n = v.n, i, j, k;
      var d = [];
      for (i = 0; i < n; i++) { d.push([]); for (j = 0; j < n; j++) d[i].push(i === j ? 0 : Infinity); }
      for (i = 0; i < v.edges.length; i++) {
        var e = v.edges[i];
        d[e[0]][e[1]] = Math.min(d[e[0]][e[1]], e[2]);
        d[e[1]][e[0]] = Math.min(d[e[1]][e[0]], e[2]);
      }
      var show = function () {
        return d.map(function (row) { return row.map(function (x) { return x === Infinity ? "∞" : String(x); }); });
      };
      var t = gridT(show(),
                    ["for k in range(n):          # k MUST be the outer loop", "    for i in range(n):",
                     "        for j in range(n):", "            if d[i][k] + d[k][j] < d[i][j]:",
                     "                d[i][j] = d[i][k] + d[k][j]"],
                    "Floyd-Warshall — the cells are the distance MATRIX d[i][j]");
      t.snap(0, "Start with the edges themselves and 0 on the diagonal; everything else is ∞. After round " +
                "k the table is optimal using only nodes {0..k} as intermediates — which is exactly why k " +
                "has to be the OUTER loop.", {});
      for (k = 0; k < n; k++) {
        t.snap(0, "round k = " + k + ": from now on, paths may route THROUGH node " + k + ".",
               { mark: (function () {
                   var m = {};
                   for (var z = 0; z < n; z++) { m[K(k, z)] = "pick"; m[K(z, k)] = "pick"; }
                   return m;
                 })() });
        for (i = 0; i < n; i++) {
          for (j = 0; j < n; j++) {
            if (d[i][k] + d[k][j] < d[i][j]) {
              var was = d[i][j];
              d[i][j] = d[i][k] + d[k][j];
              t.data.cells = show();
              t.snap(4, "d[" + i + "][" + j + "]: going " + i + "→" + k + " (" + d[i][k] + ") then " +
                        k + "→" + j + " (" + d[k][j] + ") costs " + d[i][j] + ", beating " +
                        (was === Infinity ? "∞" : was) + ".",
                     { ptr: { at: K(i, j) },
                       mark: merge({ [K(i, j)]: "pick" }, { [K(i, k)]: "done" }, { [K(k, j)]: "done" }) });
            }
          }
        }
      }
      t.data.cells = show();
      t.snap(4, "Every pair now holds its shortest distance. Four lines, O(n³) — and any other loop " +
                "order gives wrong answers that still look plausible. At n = 400 that is 64 million steps, " +
                "so check the bound before committing.",
             { aux: [{ label: "n³", text: String(n * n * n) + " steps" }] });
      return { trace: t, answer: d.map(function (row) { return row.map(function (x) { return x === Infinity ? "i" : x; }).join("."); }).join("|") };
    }
  };

  /* ================================== heaps ======================================= */

  G["hp-two"] = {
    input: [{ id: "a", label: "stream of numbers", type: "ints", def: "5 15 1 3 8" }],
    check: function (v) { if (v.a.length > 10) return "keep it to 10 numbers or fewer"; },
    brute: function (v) {              /* sort the whole prefix each time */
      var seen = [], out = [];
      for (var i = 0; i < v.a.length; i++) {
        seen.push(v.a[i]);
        var s = seen.slice().sort(function (x, y) { return x - y; });
        var n = s.length;
        out.push(n % 2 ? s[(n - 1) / 2] : (s[n / 2 - 1] + s[n / 2]) / 2);
      }
      return out.join(",");
    },
    run: function (v) {
      var a = v.a;
      var t = new Trace(a, ["heappush(lo, -x)                     # into the low half",
                            "heappush(hi, -heappop(lo))           # pass its biggest up",
                            "if len(hi) > len(lo):", "    heappush(lo, -heappop(hi))   # rebalance",
                            "median = lo[0] if sizes differ else average of both tops"],
                        "array", "running median from two heaps");
      var lo = [], hi = [], out = [];
      var med = function () {
        if (lo.length > hi.length) return lo[lo.length - 1];
        return (lo[lo.length - 1] + hi[0]) / 2;
      };
      t.snap(0, "A max-heap for the low half, a min-heap for the high half. Every low value ≤ every high " +
                "value, and the sizes never differ by more than one — so the middle is always sitting right " +
                "at the two tops.",
             { aux: [{ label: "low half", items: [] }, { label: "high half", items: [] }] });
      for (var i = 0; i < a.length; i++) {
        lo.push(a[i]); lo.sort(function (x, y) { return x - y; });
        t.snap(0, "push " + a[i] + " into the low half.",
               { ptr: { at: String(i) }, mark: merge(range(0, i - 1, "done"), { [String(i)]: "pick" }),
                 aux: [{ label: "low half", items: strs(lo) }, { label: "high half", items: strs(hi) }] });
        hi.push(lo.pop()); hi.sort(function (x, y) { return x - y; });
        t.snap(1, "immediately pass the low half's BIGGEST (" + hi[hi.length - 1 >= 0 ? hi.indexOf(hi[0]) : 0] +
                  ") up to the high half — push-then-transfer is what keeps 'every low ≤ every high' true. " +
                  "Pushing straight into the 'right' heap breaks that invariant.",
               { ptr: { at: String(i) }, mark: range(0, i, "done"),
                 aux: [{ label: "low half", items: strs(lo) }, { label: "high half", items: strs(hi) }] });
        if (hi.length > lo.length) {
          lo.push(hi.shift()); lo.sort(function (x, y) { return x - y; });
          t.snap(3, "the high half got too big, so hand its smallest back. Rebalance after EVERY insert, " +
                    "not at query time.",
                 { ptr: { at: String(i) }, mark: range(0, i, "done"),
                   aux: [{ label: "low half", items: strs(lo) }, { label: "high half", items: strs(hi) }] });
        }
        out.push(med());
        t.snap(4, "median after " + (i + 1) + " number(s) is " + med() + " — read straight off the tops in " +
                  "O(1), with no sorting.",
               { ptr: { at: String(i) }, mark: range(0, i, "done"),
                 aux: [{ label: "low half", items: strs(lo) }, { label: "high half", items: strs(hi) },
                       { label: "median", text: String(med()) }] });
      }
      t.snap(4, "Medians: " + out.join(", ") + ". A heap cannot delete from the middle, which is why the " +
                "SLIDING-window median needs lazy deletion on top of this.",
             { mark: range(0, a.length - 1, "done"), aux: [{ label: "medians", items: strs(out) }] });
      return { trace: t, answer: out.join(",") };
    }
  };

  G["hp-greedy"] = {
    input: [{ id: "iv", label: "meetings  start,end", type: "pairs", def: "1,4 2,5 7,9 4,8" }],
    check: function (v) {
      if (!v.iv.length) return "give at least one meeting";
      for (var i = 0; i < v.iv.length; i++) {
        if (v.iv[i][0] >= v.iv[i][1]) return "each meeting needs start < end";
        if (v.iv[i][0] < 1) return "start times must be 1 or more";
        if (v.iv[i][1] > 14) return "keep the clock within 14";
      }
      return null;
    },
    brute: function (v) {              /* peak concurrency by scanning the clock */
      var hi = 0, i, tt, best = 0;
      for (i = 0; i < v.iv.length; i++) hi = Math.max(hi, v.iv[i][1]);
      for (tt = 1; tt <= hi; tt++) {
        var c = 0;
        for (i = 0; i < v.iv.length; i++) if (v.iv[i][0] <= tt && tt < v.iv[i][1]) c++;
        best = Math.max(best, c);
      }
      return best;
    },
    run: function (v) {
      var iv = v.iv, hi = 0, i;
      for (i = 0; i < iv.length; i++) hi = Math.max(hi, iv[i][1]);
      var cells = [];
      for (i = 1; i <= hi; i++) cells.push(i);
      var t = new Trace(cells, ["intervals.sort()                 # by START time",
                                "for s, e in intervals:", "    if ends and ends[0] <= s:",
                                "        heappop(ends)            # a room has freed up",
                                "    heappush(ends, e)", "return len(ends)"],
                        "timeline", "minimum meeting rooms — a heap of end times");
      var order = iv.slice().sort(function (a, b) { return a[0] - b[0]; });
      var ends = [];
      t.snap(0, "Sort by start, then let the heap resolve the second dimension: it always tells you which " +
                "room frees up SOONEST.",
             { aux: [{ label: "by start", items: order.map(function (p) { return "[" + p[0] + "," + p[1] + "]"; }) }] });
      for (i = 0; i < order.length; i++) {
        var s = order[i][0], e = order[i][1];
        ends.sort(function (x, y) { return x - y; });
        if (ends.length && ends[0] <= s) {
          t.snap(3, "meeting [" + s + "," + e + "] starts at " + s + ", and the earliest room frees at " +
                    ends[0] + " — so reuse that room instead of opening a new one.",
                 { span: [s - 1, e - 1], mark: range(s - 1, e - 1, "pick"),
                   aux: [{ label: "rooms busy until", items: strs(ends) }] });
          ends.shift();
        } else {
          t.snap(4, "meeting [" + s + "," + e + "] starts at " + s + ", and " +
                    (ends.length ? "the earliest room is busy until " + ends[0] : "no room exists yet") +
                    " — open a new room.",
                 { span: [s - 1, e - 1], mark: range(s - 1, e - 1, "bad"),
                   aux: [{ label: "rooms busy until", items: strs(ends) }] });
        }
        ends.push(e);
        t.snap(4, "rooms in use: " + ends.length + ".",
               { span: [s - 1, e - 1],
                 aux: [{ label: "rooms busy until", items: strs(ends.slice().sort(function (x, y) { return x - y; })) },
                       { label: "rooms", text: String(ends.length) }] });
      }
      t.snap(5, "Answer " + ends.length + " room(s) — the peak. The same number falls out of a sweep line " +
                "of +1 / −1 events with no heap at all; know both.",
             { aux: [{ label: "rooms", text: String(ends.length) }] });
      return { trace: t, answer: ends.length };
    }
  };

  /* ============================== sorting & bits ================================== */

  G["iv-sortkey"] = {
    input: [{ id: "people", label: "people  height,k", type: "pairs", def: "7,0 4,4 7,1 5,0 6,1 5,2" }],
    check: function (v) {
      if (!v.people.length) return "give at least one person";
      if (v.people.length > 8) return "keep it to 8 people or fewer";
      for (var i = 0; i < v.people.length; i++) {
        if (v.people[i][0] < 1) return "heights must be at least 1";
        if (v.people[i][1] < 0 || v.people[i][1] >= v.people.length)
          return "k must be between 0 and " + (v.people.length - 1);
      }
      /* The real problem guarantees the input describes a queue that actually exists. Not every
         (height, k) list does, so check it here: run the construction and verify every k. */
      var ord = v.people.slice().sort(function (a, b) { return b[0] - a[0] || a[1] - b[1]; });
      var q = [];
      for (i = 0; i < ord.length; i++) q.splice(ord[i][1], 0, ord[i]);
      for (i = 0; i < q.length; i++) {
        var taller = 0;
        for (var j = 0; j < i; j++) if (q[j][0] >= q[i][0]) taller++;
        if (taller !== q[i][1])
          return "no queue can satisfy that input — person (" + q[i][0] + "," + q[i][1] + ") would end up " +
                 "with " + taller + " taller-or-equal people in front. The real problem guarantees a valid " +
                 "queue; try  7,0 4,4 7,1 5,0 6,1 5,2";
      }
      return null;
    },
    brute: function (v) {              /* verify by definition: count taller-or-equal in front */
      var n = v.people.length;
      var perm = [], used = [], out = null;
      for (var i = 0; i < n; i++) used.push(false);
      (function go() {
        if (out) return;
        if (perm.length === n) {
          for (var a = 0; a < n; a++) {
            var cnt = 0;
            for (var b = 0; b < a; b++) if (perm[b][0] >= perm[a][0]) cnt++;
            if (cnt !== perm[a][1]) return;
          }
          out = perm.map(function (p) { return p[0] + "," + p[1]; }).join(" ");
          return;
        }
        for (var j = 0; j < n; j++) {
          if (used[j]) continue;
          used[j] = true; perm.push(v.people[j]);
          go();
          perm.pop(); used[j] = false;
          if (out) return;
        }
      })();
      return out || "";
    },
    run: function (v) {
      var order = v.people.slice().sort(function (a, b) { return b[0] - a[0] || a[1] - b[1]; });
      var t = new Trace(order.map(function (p) { return p[0] + "/" + p[1]; }),
                        ["people.sort(key=lambda p: (-p[0], p[1]))   # TALLEST first, small k first",
                         "out = []", "for p in people:", "    out.insert(p[1], p)   # index k is safe:",
                         "    # everyone already placed is at least as tall"],
                        "array", "queue reconstruction — sorting by the right key is the whole trick");
      var out = [];
      t.snap(0, "Sorted tallest first, and among equal heights the smaller k first. Why that order: once " +
                "everyone already placed is at least as tall as you, inserting at index k puts exactly k " +
                "taller-or-equal people in front of you — and later, shorter inserts cannot change that count.",
             { aux: [{ label: "sorted", items: order.map(function (p) { return p[0] + "/" + p[1]; }) }] });
      for (var i = 0; i < order.length; i++) {
        var p = order[i];
        out.splice(p[1], 0, p);
        t.snap(3, "person " + p[0] + " wants " + p[1] + " taller-or-equal in front — insert at index " +
                  p[1] + ". Everyone already in the queue is ≥ " + p[0] + " tall, so the count is correct " +
                  "right now and stays correct.",
               { ptr: { at: String(i) }, mark: merge(range(0, i - 1, "done"), { [String(i)]: "pick" }),
                 aux: [{ label: "queue", items: out.map(function (q) { return q[0] + "/" + q[1]; }) }] });
      }
      t.snap(4, "Answer " + out.map(function (q) { return "(" + q[0] + "," + q[1] + ")"; }).join(" ") +
                ". The algorithm is two lines; the proof of the sort key is the whole problem.",
             { mark: range(0, order.length - 1, "done"),
               aux: [{ label: "queue", items: out.map(function (q) { return q[0] + "/" + q[1]; }) }] });
      return { trace: t, answer: out.map(function (q) { return q[0] + "," + q[1]; }).join(" ") };
    }
  };

  G["bt-tricks"] = {
    input: [{ id: "x", label: "a number", type: "int", def: 23 }],
    check: function (v) {
      if (v.x < 0 || v.x > 1023) return "use a number between 0 and 1023 so the bits stay readable";
    },
    brute: function (v) {              /* count by shifting, one bit at a time */
      var n = 0, x = v.x;
      while (x) { n += x & 1; x >>>= 1; }
      return n;
    },
    run: function (v) {
      var x = v.x, width = Math.max(4, x.toString(2).length);
      var bits = function (n2) {
        var s = (n2 >>> 0).toString(2);
        while (s.length < width) s = "0" + s;
        return s.split("");
      };
      var t = new Trace(bits(x), ["count = 0", "while x:", "    x &= x - 1      # clears the LOWEST set bit",
                                  "    count += 1", "return count"],
                        "array", "count the set bits of " + x + " with x & (x−1)");
      var cur = x, count = 0;
      t.snap(0, "There is nothing to traverse in a bit trick — except this one, which really is a loop. " +
                "x & (x−1) clears the lowest set bit, so the loop runs once per SET bit, not 32 times.",
             { mark: (function () {
                 var m = {}, b = bits(cur);
                 for (var i = 0; i < b.length; i++) if (b[i] === "1") m[String(i)] = "pick";
                 return m;
               })(),
               aux: [{ label: "x", text: String(cur) }, { label: "binary", text: bits(cur).join("") }] });
      while (cur) {
        var lowest = cur & -cur;
        var idx = width - 1 - Math.round(Math.log2(lowest));
        t.snap(2, "x = " + bits(cur).join("") + ", and x−1 = " + bits(cur - 1).join("") +
                  ". ANDing them clears exactly the lowest 1 (highlighted).",
               { mark: merge((function () {
                   var m = {}, b = bits(cur);
                   for (var i = 0; i < b.length; i++) if (b[i] === "1") m[String(i)] = "done";
                   return m;
                 })(), { [String(idx)]: "bad" }),
                 aux: [{ label: "x", text: String(cur) }, { label: "x − 1", text: String(cur - 1) },
                       { label: "count", text: String(count) }] });
        cur &= cur - 1;
        count++;
        t.snap(3, "one bit gone, count = " + count + ". x is now " + bits(cur).join("") + ".",
               { mark: (function () {
                   var m = {}, b = bits(cur);
                   for (var i = 0; i < b.length; i++) if (b[i] === "1") m[String(i)] = "pick";
                   return m;
                 })(),
                 aux: [{ label: "x", text: String(cur) }, { label: "count", text: String(count) }] });
      }
      t.snap(4, "Answer " + count + " set bit(s). Also worth memorising: x & -x ISOLATES the lowest set bit, " +
                "and x & (x-1) == 0 tests for a power of two.",
             { aux: [{ label: "count", text: String(count) }] });
      return { trace: t, answer: count };
    }
  };

  G["bt-dp"] = {
    input: [{ id: "cost", label: "cost rows (person per row)", type: "rows", def: "9,2,7 6,4,3 5,8,1" }],
    check: function (v) {
      var n = v.cost.length;
      if (n < 1 || n > 4) return "use between 1 and 4 people so the mask table stays readable";
      for (var i = 0; i < n; i++) if (v.cost[i].length !== n)
        return "the cost matrix must be square — row " + (i + 1) + " has " + v.cost[i].length +
               " entries but there are " + n + " people";
      return null;
    },
    brute: function (v) {              /* try every permutation */
      var n = v.cost.length, best = Infinity, used = [], perm = [];
      for (var i = 0; i < n; i++) used.push(false);
      (function go(p, s) {
        if (s >= best) return;
        if (p === n) { best = Math.min(best, s); return; }
        for (var j = 0; j < n; j++) if (!used[j]) {
          used[j] = true; go(p + 1, s + v.cost[p][j]); used[j] = false;
        }
      })(0, 0);
      return best;
    },
    run: function (v) {
      var cost = v.cost, n = cost.length, i, j;
      /* rows = masks, columns = the job each bit stands for */
      var cells = [];
      for (i = 0; i < (1 << n); i++) {
        var row = [];
        for (j = 0; j < n; j++) row.push((i >> j & 1) ? "1" : "0");
        cells.push(row);
      }
      var t = gridT(cells,
                    ["@lru_cache", "def go(mask):", "    i = popcount(mask)      # person i is next",
                     "    if i == n: return 0", "    for j where bit j is free:",
                     "        best = min(best, cost[i][j] + go(mask | 1<<j))"],
                    "assignment by bitmask DP — each ROW is a mask (which jobs are taken)");
      var memo = {};
      t.snap(1, "Each row of this table is one mask: a 1 means that job is already assigned. There are 2^" +
                n + " = " + (1 << n) + " of them, which is why n ≤ 20 is the signal for this pattern.",
             { aux: [{ label: "people", text: String(n) }, { label: "masks", text: String(1 << n) }] });
      t.snap(2, "The trick that halves the state: you do NOT store which person is next. popcount(mask) " +
                "already tells you — if three jobs are taken, person three is up.", {});
      function popcount(m) { var c = 0; while (m) { c += m & 1; m >>>= 1; } return c; }
      function go(mask) {
        if (memo.hasOwnProperty(mask)) return memo[mask];
        var person = popcount(mask);
        if (person === n) {
          var fullRow = {};
          for (var fz = 0; fz < n; fz++) fullRow[K(mask, fz)] = "done";
          t.snap(3, "mask " + mask.toString(2).padStart(n, "0") + ": every job is taken, so there is nothing " +
                    "left to pay. Return 0 — this is the base case.",
                 { ptr: { mask: K(mask, 0) }, mark: fullRow,
                   aux: [{ label: "mask", text: mask.toString(2).padStart(n, "0") }] });
          memo[mask] = 0;
          return 0;
        }
        var best = Infinity, bestJ = -1;
        for (var jj = 0; jj < n; jj++) {
          if (mask >> jj & 1) continue;
          var sub = go(mask | (1 << jj));
          var tot = cost[person][jj] + sub;
          if (tot < best) { best = tot; bestJ = jj; }
        }
        memo[mask] = best;
        var mk = {};
        for (var z = 0; z < n; z++) mk[K(mask, z)] = (mask >> z & 1) ? "done" : null;
        var clean = {};
        for (var kk in mk) if (mk[kk]) clean[kk] = mk[kk];
        if (bestJ >= 0) clean[K(mask, bestJ)] = "pick";
        t.snap(5, "mask " + mask.toString(2).padStart(n, "0") + " — person " + person +
                  " is next and the cheapest free job for them is job " + bestJ + " (cost " +
                  cost[person][bestJ] + "), giving " + best + " in total from here. Memoised, so this mask " +
                  "is never recomputed.",
               { ptr: { mask: K(mask, bestJ) }, mark: clean,
                 aux: [{ label: "mask", text: mask.toString(2).padStart(n, "0") },
                       { label: "person", text: String(person) },
                       { label: "best from here", text: String(best) }] });
        return best;
      }
      var ans = go(0);
      t.snap(5, "Answer " + ans + ". 2ⁿ states times n transitions — at n = 20 that is about 20 million, " +
                "fine in C++ and tight in Python.",
             { aux: [{ label: "answer", text: String(ans) },
                     { label: "states visited", text: String(Object.keys(memo).length) }] });
      return { trace: t, answer: ans };
    }
  };

  /* ============================== the row stragglers ============================== */

  G["ll-dummy"] = {
    input: [{ id: "a", label: "node values", type: "ints", def: "1 2 6 3 4 5 6" },
            { id: "val", label: "remove value", type: "int", def: 6 }],
    check: function (v) { if (v.a.length > 12) return "keep it to 12 nodes or fewer"; },
    brute: function (v) { return v.a.filter(function (x) { return x !== v.val; }).join(","); },
    run: function (v) {
      var a = v.a, val = v.val;
      var t = new Trace(a, ["dummy = ListNode(0, head)    # head now HAS a predecessor",
                            "prev = dummy", "while prev.next:", "    if prev.next.val == val:",
                            "        prev.next = prev.next.next   # unlink, do NOT advance",
                            "    else: prev = prev.next", "return dummy.next"],
                        "array", "remove every " + val + ", head included");
      var alive = a.map(function () { return true; });
      var at = -1;                               /* -1 represents the dummy */
      t.snap(0, "The dummy sits in front of the real head, so EVERY node has a predecessor and there is no " +
                "'what if it is the first one' branch anywhere.",
             { aux: [{ label: "prev", text: "dummy" }] });
      function nextLive(from) {
        for (var i = from + 1; i < a.length; i++) if (alive[i]) return i;
        return a.length;
      }
      while (true) {
        var nxt = nextLive(at);
        if (nxt >= a.length) break;
        var gone = {}, keep = {};
        for (var z = 0; z < a.length; z++) if (!alive[z]) gone[String(z)] = "gone";
        if (a[nxt] === val) {
          alive[nxt] = false;
          gone[String(nxt)] = "bad";
          t.snap(4, "prev.next holds " + val + " — unlink it by pointing prev past it. And do NOT advance " +
                    "prev: the node that just became prev.next has not been checked yet.",
                 { ptr: merge(at >= 0 ? { prev: String(at) } : {}), mark: gone,
                   aux: [{ label: "prev", text: at < 0 ? "dummy" : String(a[at]) },
                         { label: "list", items: a.filter(function (_, i2) { return alive[i2]; }).map(String) }] });
        } else {
          at = nxt;
          keep[String(nxt)] = "pick";
          t.snap(5, "prev.next holds " + a[nxt] + ", which stays — so advance prev onto it.",
                 { ptr: { prev: String(at) }, mark: merge(gone, keep),
                   aux: [{ label: "prev", text: String(a[at]) },
                         { label: "list", items: a.filter(function (_, i3) { return alive[i3]; }).map(String) }] });
        }
      }
      var out = a.filter(function (_, i4) { return alive[i4]; });
      t.snap(6, "Answer " + (out.length ? out.join(" → ") : "(empty list)") +
                ". Return dummy.next, never the original head — it may have been one of the removals.",
             { mark: (function () {
                 var m = {};
                 for (var z2 = 0; z2 < a.length; z2++) m[String(z2)] = alive[z2] ? "done" : "gone";
                 return m;
               })(),
               aux: [{ label: "result", items: strs(out) }] });
      return { trace: t, answer: out.join(",") };
    }
  };

  G["dsu-cycle"] = {
    input: [{ id: "n", label: "nodes", type: "int", def: 4 },
            { id: "edges", label: "edges  a,b", type: "pairs", def: "0,1 1,2 2,3 1,3" }],
    check: function (v) {
      if (v.n < 2 || v.n > 8) return "use between 2 and 8 nodes";
      if (!v.edges.length) return "give at least one edge";
      if (v.edges.length > 12) return "keep it to 12 edges or fewer";
      for (var i = 0; i < v.edges.length; i++) {
        var e = v.edges[i];
        if (e[0] < 0 || e[1] < 0 || e[0] >= v.n || e[1] >= v.n) return "edge uses a node outside 0.." + (v.n - 1);
        if (e[0] === e[1]) return "a self-loop (" + e[0] + "," + e[1] + ") is trivially a cycle";
      }
      return null;
    },
    brute: function (v) {              /* DFS with a parent check -- not DSU */
      var adj = [], i;
      for (i = 0; i < v.n; i++) adj.push([]);
      for (i = 0; i < v.edges.length; i++) { adj[v.edges[i][0]].push(i); adj[v.edges[i][1]].push(i); }
      var seen = [], bad = false;
      for (i = 0; i < v.n; i++) seen.push(false);
      function dfs(u, viaEdge) {
        seen[u] = true;
        for (var k = 0; k < adj[u].length; k++) {
          var ei = adj[u][k];
          if (ei === viaEdge) continue;
          var e = v.edges[ei], w = e[0] === u ? e[1] : e[0];
          if (seen[w]) { bad = true; return; }
          dfs(w, ei);
          if (bad) return;
        }
      }
      for (i = 0; i < v.n && !bad; i++) if (!seen[i]) dfs(i, -1);
      return bad ? 1 : 0;
    },
    run: function (v) {
      var n = v.n, edges = v.edges, i;
      var t = new Trace({ n: n, edges: edges, labels: null },
                        ["for a, b in edges:", "    if not union(a, b):",
                         "        return [a, b]      # both ends already connected",
                         "# a valid TREE also needs exactly n-1 edges"],
                        "graph", "find the edge that closes a loop");
      var p = [];
      for (i = 0; i < n; i++) p.push(i);
      function find(x) { while (p[x] !== x) { p[x] = p[p[x]]; x = p[x]; } return x; }
      var emark = {}, found = 0;
      t.snap(0, "Before adding an edge, its two ends are already in the same set exactly when a path " +
                "between them exists. So the first union that joins nothing is the edge closing a cycle.",
             { aux: [{ label: "edges", text: String(edges.length) },
                     { label: "a tree would need", text: String(n - 1) }] });
      for (i = 0; i < edges.length; i++) {
        var a = edges[i][0], b = edges[i][1];
        var ra = find(a), rb = find(b);
        if (ra === rb) {
          found = 1;
          emark[String(i)] = "bad";
          t.snap(2, "edge " + a + "–" + b + ": both ends already lead to root " + ra +
                    " — a path between them exists already, so this edge closes a LOOP. That is the " +
                    "redundant connection.",
                 { ptr: { a: String(a), b: String(b) },
                   mark: { [String(a)]: "bad", [String(b)]: "bad" }, emark: emark,
                   aux: [{ label: "verdict", text: "cycle found" }] });
          break;
        }
        p[rb] = ra;
        emark[String(i)] = "done";
        t.snap(1, "edge " + a + "–" + b + " joins two separate groups — accept it, no loop yet.",
               { ptr: { a: String(a), b: String(b) },
                 mark: { [String(a)]: "done", [String(b)]: "done" }, emark: emark });
      }
      if (!found) {
        t.snap(3, "Every edge joined two distinct groups, so there is no cycle. Note a valid TREE needs BOTH " +
                  "conditions: no cycle AND exactly n−1 = " + (n - 1) + " edges (there are " + edges.length +
                  "). Checking only one is the usual miss.",
               { emark: emark, aux: [{ label: "verdict", text: "no cycle" }] });
      }
      return { trace: t, answer: found };
    }
  };

  G["bk-subsets"] = {
    input: [{ id: "a", label: "items (sorted for you)", type: "ints", def: "1 2 2" }],
    prep: function (v) {
      var was = v.a.join(" ");
      v.a = v.a.slice().sort(function (x, y) { return x - y; });
      return was === v.a.join(" ") ? null
           : "sorted your input first — the duplicate-skipping rule only works on sorted input";
    },
    check: function (v) {
      if (v.a.length > 5) return "keep it to 5 items or fewer — 2ⁿ grows fast";
      if (!v.a.length) return "give at least one item";
    },
    brute: function (v) {              /* enumerate by mask, dedupe with a set */
      var n = v.a.length, seen = {}, cnt = 0;
      for (var m = 0; m < (1 << n); m++) {
        var s = [];
        for (var i = 0; i < n; i++) if (m >> i & 1) s.push(v.a[i]);
        var key = s.join(",");
        if (!seen[key]) { seen[key] = 1; cnt++; }
      }
      return cnt;
    },
    run: function (v) {
      var a = v.a;
      var t = new Trace(a, ["def go(start):", "    out.append(cur[:])        # COPY -- every node is an answer",
                            "    for i in range(start, n):", "        if i > start and a[i] == a[i-1]: continue",
                            "        cur.append(a[i])", "        go(i + 1)      # i+1: never reuse this item",
                            "        cur.pop()                 # UNDO"],
                        "array", "every distinct subset of [" + a.join(", ") + "]");
      var cur = [], out = [], chosen = {};
      function go(start) {
        out.push(cur.slice());
        t.snap(1, "record { " + (cur.length ? cur.join(", ") : "∅") + " } — every node of the " +
                  "recursion is itself an answer. Append a COPY, or every entry ends up identical and empty.",
               { mark: merge(chosen), aux: [{ label: "current", items: cur.length ? strs(cur) : [] },
                                            { label: "subsets", text: String(out.length) }] });
        for (var i = start; i < a.length; i++) {
          if (i > start && a[i] === a[i - 1]) {
            t.snap(3, "a[" + i + "] = " + a[i] + " repeats a[" + (i - 1) + "] at this level — skip it, or " +
                      "you emit the same set twice. Note the test is i > start, not i > 0.",
                   { ptr: { skip: String(i) }, mark: merge(chosen, { [String(i)]: "bad" }) });
            continue;
          }
          cur.push(a[i]); chosen[String(i)] = "pick";
          t.snap(4, "choose a[" + i + "] = " + a[i] + ", then recurse from " + (i + 1) +
                    " — i+1 is what stops an item being reused.",
                 { ptr: { at: String(i) }, mark: merge(chosen) });
          go(i + 1);
          cur.pop(); delete chosen[String(i)];
          t.snap(6, "un-choose a[" + i + "] — the UNDO that makes it backtracking rather than just recursion.",
                 { mark: merge(chosen), aux: [{ label: "current", items: cur.length ? strs(cur) : [] }] });
        }
      }
      go(0);
      t.snap(1, "Answer " + out.length + " distinct subset(s): " +
                out.map(function (s) { return "{" + s.join(",") + "}"; }).join(" ") + ".",
             { aux: [{ label: "subsets", text: String(out.length) }] });
      return { trace: t, answer: out.length };
    }
  };

  G["bk-perms"] = {
    input: [{ id: "a", label: "items (sorted for you)", type: "ints", def: "1 1 2" }],
    prep: function (v) {
      v.a = v.a.slice().sort(function (x, y) { return x - y; });
      return null;
    },
    check: function (v) {
      if (v.a.length > 4) return "keep it to 4 items or fewer — n! grows faster than anything else here";
      if (!v.a.length) return "give at least one item";
    },
    brute: function (v) {              /* generate all orderings, dedupe with a set */
      var seen = {}, cnt = 0, n = v.a.length, used = [], perm = [];
      for (var i = 0; i < n; i++) used.push(false);
      (function go() {
        if (perm.length === n) {
          var key = perm.join(",");
          if (!seen[key]) { seen[key] = 1; cnt++; }
          return;
        }
        for (var j = 0; j < n; j++) {
          if (used[j]) continue;
          used[j] = true; perm.push(v.a[j]); go(); perm.pop(); used[j] = false;
        }
      })();
      return cnt;
    },
    run: function (v) {
      var a = v.a, n = a.length;
      var t = new Trace(a, ["def go():", "    if len(cur) == n: out.append(cur[:]); return",
                            "    for i in range(n):", "        if used[i]: continue",
                            "        if i>0 and a[i]==a[i-1] and not used[i-1]: continue",
                            "        used[i] = True; cur.append(a[i])", "        go()",
                            "        cur.pop(); used[i] = False"],
                        "array", "every distinct permutation of [" + a.join(", ") + "]");
      var used = [], cur = [], out = [];
      for (var z = 0; z < n; z++) used.push(false);
      var paint = function () {
        var m = {};
        for (var i = 0; i < n; i++) if (used[i]) m[String(i)] = "pick";
        return m;
      };
      function go() {
        if (cur.length === n) {
          out.push(cur.slice());
          t.snap(1, "a complete arrangement: [" + cur.join(", ") + "].",
                 { mark: (function () { var m = {}; for (var i = 0; i < n; i++) m[String(i)] = "done"; return m; })(),
                   aux: [{ label: "current", items: strs(cur) }, { label: "permutations", text: String(out.length) }] });
          return;
        }
        for (var i = 0; i < n; i++) {
          if (used[i]) continue;
          if (i > 0 && a[i] === a[i - 1] && !used[i - 1]) {
            t.snap(4, "a[" + i + "] = " + a[i] + " duplicates a[" + (i - 1) + "], and that twin is NOT in use " +
                      "— so this branch would repeat one we already did. Skip. Note this rule differs " +
                      "from the subsets rule: here it is 'not used[i-1]'.",
                   { ptr: { skip: String(i) }, mark: merge(paint(), { [String(i)]: "bad" }) });
            continue;
          }
          used[i] = true; cur.push(a[i]);
          t.snap(5, "place a[" + i + "] = " + a[i] + " at position " + cur.length + ".",
                 { ptr: { at: String(i) }, mark: paint(),
                   aux: [{ label: "current", items: strs(cur) }] });
          go();
          cur.pop(); used[i] = false;
          t.snap(7, "take it back out — reset BOTH the flag and the list, in the reverse order you set them.",
                 { mark: paint(), aux: [{ label: "current", items: cur.length ? strs(cur) : [] }] });
        }
      }
      go();
      t.snap(1, "Answer " + out.length + " distinct permutation(s). At n = 11 there are 40 million — " +
                "always check the bound before writing this.",
             { aux: [{ label: "permutations", text: String(out.length) }] });
      return { trace: t, answer: out.length };
    }
  };

  G["tr-search"] = {
    input: [{ id: "g", label: "letter grid rows", type: "letters", def: "oaa eto ihk" },
            { id: "words", label: "words to find", type: "words", def: "oath pea eat rain" }],
    check: function (v) {
      if (v.g.length > 4 || v.g[0].length > 4) return "keep the board within 4 rows and 4 columns";
      if (!v.words.length) return "give at least one word to look for";
      if (v.words.length > 5) return "keep it to 5 words or fewer";
      for (var i = 0; i < v.words.length; i++)
        if (!/^[a-z]+$/.test(v.words[i])) return "lowercase letters only (got '" + v.words[i] + "')";
      for (i = 0; i < v.g.length; i++)
        if (v.g[i].length !== v.g[0].length) return "every board row must be the same length";
      return null;
    },
    brute: function (v) {              /* plain DFS per word, no trie */
      var g = v.g, R = g.length, C = g[0].length, found = [];
      function hunt(w) {
        var seen = {};
        function dfs(r, c, k) {
          if (k === w.length) return true;
          if (r < 0 || r >= R || c < 0 || c >= C) return false;
          if (seen[r + "," + c] || g[r][c] !== w[k]) return false;
          seen[r + "," + c] = 1;
          var ok = dfs(r + 1, c, k + 1) || dfs(r - 1, c, k + 1) || dfs(r, c + 1, k + 1) || dfs(r, c - 1, k + 1);
          delete seen[r + "," + c];
          return ok;
        }
        for (var r = 0; r < R; r++) for (var c = 0; c < C; c++) if (dfs(r, c, 0)) return true;
        return false;
      }
      /* dedupe: the same word listed twice is still one result, which is what run() reports */
      var uniq = {};
      for (var i = 0; i < v.words.length; i++) if (!uniq[v.words[i]] && hunt(v.words[i])) {
        uniq[v.words[i]] = 1;
        found.push(v.words[i]);
      }
      return found.sort().join(",");
    },
    run: function (v) {
      var g = v.g, R = g.length, C = g[0].length;
      /* trie */
      var ch = [{}], end = [false];
      for (var wi = 0; wi < v.words.length; wi++) {
        var node = 0, w = v.words[wi];
        for (var ci = 0; ci < w.length; ci++) {
          if (ch[node][w[ci]] == null) { ch.push({}); end.push(false); ch[node][w[ci]] = ch.length - 1; }
          node = ch[node][w[ci]];
        }
        end[node] = true;
      }
      var cells = g.map(function (row) { return row.split(""); });
      var t = gridT(cells,
                    ["for every start cell: dfs(r, c, root, \"\")", "", "def dfs(r, c, node, path):",
                     "    if board[r][c] not in node.ch: return    # DEAD END -- the whole point",
                     "    nxt = node.ch[board[r][c]]", "    if nxt.end: found.add(path + ch)",
                     "    mark visited; recurse on 4 neighbours; restore"],
                    "the trie prunes the grid search instantly");
      var found = {}, visited = {}, steps = 0, LIMIT = 220;
      t.snap(0, "Without a trie you would run one search per word. With it, a single walk of the board " +
                "carries all " + v.words.length + " words at once, and dies the moment no word continues " +
                "like the path so far.",
             { aux: [{ label: "words", items: v.words.slice() }] });
      function dfs(r, c, node, path) {
        if (r < 0 || r >= R || c < 0 || c >= C) return;
        if (visited[K(r, c)]) return;
        var letter = g[r][c];
        if (ch[node][letter] == null) {
          if (steps < LIMIT) {
            steps++;
            t.snap(3, "\"" + path + letter + "\" — no word in the trie continues like that, so this branch " +
                      "dies immediately. That pruning is why the trie is here.",
                   { ptr: { dead: K(r, c) }, mark: merge(visited, { [K(r, c)]: "bad" }),
                     aux: [{ label: "path", text: path + letter },
                           { label: "found", items: Object.keys(found) }] });
          }
          return;
        }
        var nxt = ch[node][letter];
        visited[K(r, c)] = "pick";
        path = path + letter;
        if (end[nxt]) found[path] = 1;
        if (steps < LIMIT) {
          steps++;
          t.snap(end[nxt] ? 5 : 4,
                 end[nxt] ? ("\"" + path + "\" is flagged END — a real word, recorded.")
                          : ("\"" + path + "\" is a live prefix — keep going."),
                 { ptr: { at: K(r, c) }, mark: merge(visited, { [K(r, c)]: end[nxt] ? "done" : "pick" }),
                   aux: [{ label: "path", text: path }, { label: "found", items: Object.keys(found) }] });
        }
        dfs(r + 1, c, nxt, path); dfs(r - 1, c, nxt, path);
        dfs(r, c + 1, nxt, path); dfs(r, c - 1, nxt, path);
        delete visited[K(r, c)];
      }
      for (var r2 = 0; r2 < R; r2++) for (var c2 = 0; c2 < C; c2++) dfs(r2, c2, 0, "");
      var list = Object.keys(found).sort();
      t.snap(5, "Answer " + (list.length ? list.join(", ") : "nothing found") +
                ". Restore each cell after recursing, or the board is destroyed for the next start square" +
                (steps >= LIMIT ? " (the trace stopped recording after " + LIMIT + " frames; the search ran to the end)" : "") + ".",
             { aux: [{ label: "found", items: list }] });
      return { trace: t, answer: list.join(",") };
    }
  };
})();
