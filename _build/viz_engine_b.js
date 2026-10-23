/* =====================================================================================
   VIZ ENGINE, part B  --  trace generators for linked lists, DP, greedy, DSU and
   topological sort. Registers onto the same object viz_engine.js created, so this file
   must load AFTER it. Same contract, same fuzz test: run() must agree with brute().
   ===================================================================================== */
(function () {
  "use strict";
  var G = (typeof module !== "undefined" && module.exports)
        ? require("./viz_engine.js")
        : window.VIZGEN;
  var H = G.__helpers, Trace = H.Trace, range = H.range, merge = H.merge, kv = H.kv, strs = H.strs;

  /* ================================= LINKED LISTS ================================= */

  G["ll-fastslow"] = {
    input: [{ id: "a", label: "node values", type: "ints", def: "1 2 3 4 5 6 7" }],
    brute: function (v) { return v.a[Math.floor(v.a.length / 2)]; },
    run: function (v) {
      var a = v.a;
      var t = new Trace(a, ["slow = fast = head", "while fast and fast.next:", "    slow = slow.next",
                            "    fast = fast.next.next", "return slow"],
                        "array", "find the middle without knowing the length");
      var slow = 0, fast = 0;
      t.snap(0, "Both start at the head. You cannot index a linked list, so the only way to find the middle " +
                "is to make two pointers move at different speeds.",
             { ptr: { slow: 0, fast: 0 }, mark: { 0: "pick" } });
      while (fast < a.length && fast + 1 < a.length) {
        slow += 1;
        fast += 2;
        t.snap(3, "slow steps once to index " + slow + ", fast steps twice to index " +
                  (fast < a.length ? fast : "past the end") +
                  ". fast covers exactly double the ground, so when it finishes slow is halfway.",
               { ptr: fast < a.length ? { slow: slow, fast: fast } : { slow: slow },
                 span: [0, Math.min(fast, a.length - 1)],
                 mark: merge({}, fast < a.length ? { } : { }) });
      }
      t.snap(4, "fast ran out, so slow is standing on the middle: " + a[slow] + " at index " + slow +
                ". One pass, no length, no second traversal.",
             { ptr: { slow: slow }, mark: { [slow]: "done" },
               aux: [{ label: "middle", text: String(a[slow]) }] });
      return { trace: t, answer: a[slow] };
    }
  };

  G["ll-reverse"] = {
    input: [{ id: "a", label: "node values", type: "ints", def: "1 2 3 4 5" }],
    brute: function (v) { return v.a.slice().reverse().join(","); },
    run: function (v) {
      var a = v.a, n = a.length;
      var t = new Trace(a, ["prev, cur = None, head", "while cur:", "    nxt = cur.next   # save FIRST",
                            "    cur.next = prev", "    prev = cur", "    cur = nxt", "return prev"],
                        "array", "reverse the list by rewiring, O(1) space");
      var out = [];                       /* the reversed list, built as we go */
      t.snap(0, "prev starts as None — it becomes the tail of the reversed list.",
             { ptr: { cur: 0 }, aux: [{ label: "reversed so far", items: [] }] });
      for (var i = 0; i < n; i++) {
        t.snap(2, "save nxt = " + (i + 1 < n ? String(a[i + 1]) : "None") +
                  " BEFORE touching cur.next. Overwrite the pointer first and the rest of the list is lost forever.",
               { ptr: merge({ cur: i }, i + 1 < n ? { nxt: i + 1 } : {}),
                 mark: { [i]: "pick" },
                 aux: [{ label: "reversed so far", items: strs(out) }] });
        out.unshift(a[i]);
        t.snap(3, "point node " + a[i] + " back at " + (i === 0 ? "None" : String(a[i - 1])) +
                  ". The arrow is now reversed.",
               { ptr: { cur: i }, mark: merge(range(0, i, "done")),
                 aux: [{ label: "reversed so far", items: strs(out) }] });
      }
      t.snap(6, "cur is None, so prev (" + a[n - 1] + ") is the new head. Return prev, never cur.",
             { mark: range(0, n - 1, "done"), aux: [{ label: "reversed", items: strs(out) }] });
      return { trace: t, answer: out.join(",") };
    }
  };

  /* ================================= 1-D DP ======================================= */

  G["dp-linear"] = {
    input: [{ id: "a", label: "house values", type: "ints", def: "2 7 9 3 1" }],
    check: function (v) {
      if (v.a.length > 12) return "keep it to 12 houses or fewer so the trace stays watchable";
      for (var i = 0; i < v.a.length; i++) if (v.a[i] < 0) return "house values cannot be negative here";
    },
    brute: function (v) {          /* exhaustive over every no-two-adjacent subset */
      var n = v.a.length, best = 0;
      for (var m = 0; m < (1 << n); m++) {
        if (m & (m << 1)) continue;             /* two adjacent bits -> illegal */
        var s = 0;
        for (var i = 0; i < n; i++) if (m >> i & 1) s += v.a[i];
        if (s > best) best = s;
      }
      return best;
    },
    run: function (v) {
      var a = v.a;
      var t = new Trace(a, ["prev2, prev1 = 0, 0", "for x in a:", "    take = prev2 + x",
                            "    skip = prev1", "    prev2, prev1 = prev1, max(take, skip)"],
                        "array", "house robber — no two adjacent");
      var prev2 = 0, prev1 = 0;
      t.snap(0, "State, as a sentence: prev1 = the best loot from the houses so far. " +
                "If you cannot say that sentence, you do not have a DP yet.",
             { aux: [{ label: "prev2", text: "0" }, { label: "prev1", text: "0" }] });
      for (var i = 0; i < a.length; i++) {
        var take = prev2 + a[i], skip = prev1;
        t.snap(2, "at house " + i + " (" + a[i] + "): TAKE it → " + prev2 + " + " + a[i] + " = " + take +
                  " (skipping its neighbour), or SKIP it → " + skip + ".",
               { ptr: { i: i }, mark: merge(i >= 2 ? { [i - 2]: "pick" } : {}, { [i]: "pick" },
                                            i >= 1 ? { [i - 1]: "bad" } : {}),
                 aux: [{ label: "take", text: String(take) }, { label: "skip", text: String(skip) }] });
        prev2 = prev1;
        prev1 = Math.max(take, skip);
        t.snap(4, (take >= skip ? "taking" : "skipping") + " wins: best so far = " + prev1 +
                  ". Only the last two values are ever read, so two variables replace the whole array.",
               { ptr: { i: i }, mark: range(0, i, "done"),
                 aux: [{ label: "prev2", text: String(prev2) }, { label: "prev1", text: String(prev1) }] });
      }
      t.snap(4, "Answer " + prev1 + ".", { aux: [{ label: "best", text: String(prev1) }] });
      return { trace: t, answer: prev1 };
    }
  };

  G["dp-kadane"] = {
    input: [{ id: "a", label: "array", type: "ints", def: "-2 1 -3 4 -1 2 1 -5 4" }],
    brute: function (v) {
      var best = -Infinity;
      for (var i = 0; i < v.a.length; i++) {
        var s = 0;
        for (var j = i; j < v.a.length; j++) { s += v.a[j]; if (s > best) best = s; }
      }
      return best;
    },
    run: function (v) {
      var a = v.a;
      var t = new Trace(a, ["cur = best = a[0]", "for x in a[1:]:", "    cur = max(x, cur + x)",
                            "    best = max(best, cur)"],
                        "array", "largest sum of a contiguous run");
      var cur = a[0], best = a[0], start = 0, bs = 0, be = 0;
      t.snap(0, "cur = the best run ENDING here. Seed from a[0], never 0 — seeding with 0 silently returns " +
                "0 for an all-negative array.",
             { mark: { 0: "pick" }, aux: [{ label: "cur", text: String(cur) }, { label: "best", text: String(best) }] });
      for (var i = 1; i < a.length; i++) {
        var fresh = a[i], extend = cur + a[i];
        if (fresh > extend) { cur = fresh; start = i; }
        else cur = extend;
        t.snap(2, "at " + a[i] + ": start fresh (" + fresh + ") or extend (" + extend + ")? " +
                  (fresh > extend ? "Start fresh — the run behind was dragging us down."
                                  : "Extend — the run behind still helps.") +
                  " That single comparison is the whole algorithm.",
               { ptr: { i: i }, span: [start, i], mark: { [i]: "pick" },
                 aux: [{ label: "cur", text: String(cur) }, { label: "best", text: String(best) }] });
        if (cur > best) { best = cur; bs = start; be = i; }
        t.snap(3, "best = " + best + ".",
               { ptr: { i: i }, span: [bs, be], mark: range(bs, be, "done"),
                 aux: [{ label: "cur", text: String(cur) }, { label: "best", text: String(best) }] });
      }
      t.snap(3, "Answer " + best + " — the run from index " + bs + " to " + be + ".",
             { span: [bs, be], mark: range(bs, be, "done"), aux: [{ label: "best", text: String(best) }] });
      return { trace: t, answer: best };
    }
  };

  G["dp-coin"] = {
    input: [{ id: "coins", label: "coin values", type: "ints", def: "1 3 4" },
            { id: "amount", label: "amount", type: "int", def: 6 }],
    check: function (v) {
      if (v.amount < 0 || v.amount > 14) return "keep the amount between 0 and 14 so the trace stays watchable";
      for (var i = 0; i < v.coins.length; i++) if (v.coins[i] < 1) return "coins must be at least 1";
    },
    brute: function (v) {              /* BFS over amounts -- a different implementation */
      var seen = {}, q = [0], d = 0;
      seen[0] = true;
      while (q.length) {
        var nxt = [];
        for (var i = 0; i < q.length; i++) {
          if (q[i] === v.amount) return d;
          for (var c = 0; c < v.coins.length; c++) {
            var t2 = q[i] + v.coins[c];
            if (t2 <= v.amount && !seen[t2]) { seen[t2] = true; nxt.push(t2); }
          }
        }
        q = nxt; d++;
      }
      return -1;
    },
    run: function (v) {
      var coins = v.coins, amount = v.amount, i, c;
      var cells = [];
      for (i = 0; i <= amount; i++) cells.push(i);
      var t = new Trace(cells, ["dp = [inf] * (amount + 1)", "dp[0] = 0", "for t in range(1, amount+1):",
                                "    for c in coins:", "        if c <= t:",
                                "            dp[t] = min(dp[t], dp[t-c] + 1)"],
                        "array", "fewest coins for " + amount + " — the cells are the AMOUNTS 0.." + amount);
      var dp = [];
      for (i = 0; i <= amount; i++) dp.push(Infinity);
      dp[0] = 0;
      var show = function () {
        return dp.map(function (x) { return x === Infinity ? "∞" : String(x); });
      };
      t.snap(1, "The cells are amounts, not coins. dp[0] = 0 because zero coins make zero — that seed is " +
                "what every other cell is eventually built from.",
             { mark: { 0: "done" }, aux: [{ label: "coins", items: strs(coins) }, { label: "dp", items: show() }] });
      for (var tt = 1; tt <= amount; tt++) {
        for (c = 0; c < coins.length; c++) {
          if (coins[c] > tt) continue;
          var cand = dp[tt - coins[c]] === Infinity ? Infinity : dp[tt - coins[c]] + 1;
          t.snap(5, "amount " + tt + " using coin " + coins[c] + ": look back at dp[" + (tt - coins[c]) + "] = " +
                    (dp[tt - coins[c]] === Infinity ? "∞" : dp[tt - coins[c]]) + " and add one coin → " +
                    (cand === Infinity ? "still unreachable" : cand) +
                    (cand < dp[tt] ? "  (better)" : "  (no better)"),
                 { ptr: { t: tt, from: tt - coins[c] }, span: [tt - coins[c], tt],
                   mark: merge({ [tt - coins[c]]: "pick" }, { [tt]: cand < dp[tt] ? "done" : "bad" }),
                   aux: [{ label: "dp", items: show() }] });
          if (cand < dp[tt]) dp[tt] = cand;
        }
      }
      var ans = dp[amount] === Infinity ? -1 : dp[amount];
      t.snap(5, ans < 0
             ? ("Amount " + amount + " cannot be made from these coins at all — report −1, not infinity.")
             : ("Answer " + ans + " coins. Note the greedy 'take the biggest coin first' is WRONG here: with " +
                "coins 1,3,4 and amount 6 it gives 4+1+1 = 3, while the DP finds 3+3 = 2."),
             { mark: { [amount]: "done" }, aux: [{ label: "dp", items: show() }] });
      return { trace: t, answer: ans };
    }
  };

  G["dp-lis"] = {
    input: [{ id: "a", label: "array", type: "ints", def: "10 9 2 5 3 7 101 18" }],
    check: function (v) { if (v.a.length > 12) return "keep it to 12 numbers or fewer so the trace stays watchable"; },
    brute: function (v) {              /* exhaustive over subsequences */
      var n = v.a.length, best = 0;
      for (var m = 0; m < (1 << n); m++) {
        var last = -Infinity, len = 0, ok = true;
        for (var i = 0; i < n; i++) {
          if (!(m >> i & 1)) continue;
          if (v.a[i] <= last) { ok = false; break; }
          last = v.a[i]; len++;
        }
        if (ok && len > best) best = len;
      }
      return best;
    },
    run: function (v) {
      var a = v.a;
      var t = new Trace(a, ["dp = [1] * n", "for i in range(n):", "    for j in range(i):",
                            "        if a[j] < a[i]:", "            dp[i] = max(dp[i], dp[j] + 1)"],
                        "array", "longest increasing subsequence, the O(n²) form");
      var dp = a.map(function () { return 1; });
      t.snap(0, "dp[i] = the longest increasing run that ENDS at i. Every element alone is a run of 1.",
             { aux: [{ label: "dp", items: strs(dp) }] });
      for (var i = 0; i < a.length; i++) {
        for (var j = 0; j < i; j++) {
          var better = a[j] < a[i] && dp[j] + 1 > dp[i];
          t.snap(3, "can " + a[i] + " extend the run ending at " + a[j] + "? " +
                    (a[j] < a[i]
                      ? (dp[j] + 1 > dp[i] ? "yes, and it is longer: dp[" + i + "] becomes " + (dp[j] + 1)
                                           : "yes, but it is not longer than what dp[" + i + "] already has")
                      : "no — " + a[j] + " is not smaller than " + a[i]),
                 { ptr: { i: i, j: j }, mark: merge({ [j]: a[j] < a[i] ? "pick" : "bad" }, { [i]: "pick" }),
                   aux: [{ label: "dp", items: strs(dp) }] });
          if (better) dp[i] = dp[j] + 1;
        }
      }
      var best = Math.max.apply(null, dp.concat([0]));
      t.snap(4, "Answer " + best + " — the biggest value in dp. At n ≤ 2500 this O(n²) form is fine; " +
                "at n = 10⁵ the constraint forces the O(n log n) tails version instead.",
             { mark: (function () { var m = {}; for (var k = 0; k < dp.length; k++) if (dp[k] === best) m[k] = "done"; return m; })(),
               aux: [{ label: "dp", items: strs(dp) }, { label: "best", text: String(best) }] });
      return { trace: t, answer: best };
    }
  };

  /* =================================== GREEDY ===================================== */

  G["gr-reach"] = {
    input: [{ id: "a", label: "jump lengths", type: "ints", def: "2 3 1 1 4" }],
    check: function (v) {
      for (var i = 0; i < v.a.length; i++) if (v.a[i] < 0) return "jump lengths cannot be negative";
    },
    brute: function (v) {              /* BFS reachability -- independent of the greedy */
      var n = v.a.length, seen = {}, q = [0];
      seen[0] = 1;
      while (q.length) {
        var i = q.pop();
        if (i >= n - 1) return 1;
        for (var s = 1; s <= v.a[i]; s++) {
          var j = i + s;
          if (j < n && !seen[j]) { seen[j] = 1; q.push(j); }
        }
      }
      return n === 1 ? 1 : 0;
    },
    run: function (v) {
      var a = v.a;
      var t = new Trace(a, ["reach = 0", "for i, x in enumerate(a):", "    if i > reach: return False",
                            "    reach = max(reach, i + x)", "return True"],
                        "array", "can you reach the last index?");
      var reach = 0, ok = 1;
      t.snap(0, "One variable is the entire state: the furthest index reachable so far. " +
                "No DP table, no recursion.",
             { ptr: { reach: 0 }, aux: [{ label: "reach", text: "0" }] });
      for (var i = 0; i < a.length; i++) {
        if (i > reach) {
          ok = 0;
          t.snap(2, "index " + i + " is past reach (" + reach + ") — there is a gap nothing can cross, " +
                    "so the end is unreachable.",
                 { ptr: { i: i, reach: reach }, mark: { [i]: "bad" },
                   aux: [{ label: "reach", text: String(reach) }] });
          break;
        }
        var nr = Math.max(reach, i + a[i]);
        t.snap(3, "from index " + i + " you can jump " + a[i] + ", landing as far as " + (i + a[i]) + ". " +
                  (nr > reach ? "reach improves to " + nr + "." : "that is no further than reach already is."),
               { ptr: { i: i, reach: Math.min(nr, a.length - 1) },
                 span: [0, Math.min(nr, a.length - 1)], mark: { [i]: "pick" },
                 aux: [{ label: "reach", text: String(nr) }] });
        reach = nr;
      }
      if (ok) {
        t.snap(4, "Every index stayed within reach, so the end is reachable. O(n), O(1) space — the DP " +
                  "version would be O(n²) for the same answer.",
               { span: [0, a.length - 1], mark: range(0, a.length - 1, "done"),
                 aux: [{ label: "reach", text: String(reach) }] });
      }
      return { trace: t, answer: ok };
    }
  };

  G["gr-pair"] = {
    input: [{ id: "people", label: "weights", type: "ints", def: "3 2 2 1" },
            { id: "limit", label: "boat limit", type: "int", def: 3 }],
    check: function (v) {
      for (var i = 0; i < v.people.length; i++) {
        if (v.people[i] < 1) return "weights must be at least 1";
        if (v.people[i] > v.limit) return "someone heavier than the limit can never board — weight " +
                                          v.people[i] + " > limit " + v.limit;
      }
    },
    brute: function (v) {              /* exhaustive matching for small n */
      var n = v.people.length;
      if (n > 8) return null;
      var p = v.people.slice().sort(function (a, b) { return a - b; });
      var best = n;
      var go = function (used, boats) {
        if (boats >= best) return;
        var first = -1;
        for (var i = 0; i < n; i++) if (!(used >> i & 1)) { first = i; break; }
        if (first < 0) { best = Math.min(best, boats); return; }
        go(used | (1 << first), boats + 1);                       /* alone */
        for (var j = first + 1; j < n; j++) {
          if (used >> j & 1) continue;
          if (p[first] + p[j] <= v.limit) go(used | (1 << first) | (1 << j), boats + 1);
        }
      };
      go(0, 0);
      return best;
    },
    run: function (v) {
      var people = v.people.slice().sort(function (a, b) { return a - b; }), limit = v.limit;
      var t = new Trace(people, ["people.sort()", "l, r = 0, len(people)-1", "while l <= r:",
                                 "    if people[l] + people[r] <= limit: l += 1",
                                 "    r -= 1; boats += 1"],
                        "array", "fewest boats, 2 people max, limit " + limit);
      var l = 0, r = people.length - 1, boats = 0;
      t.snap(0, "Sorted. Now the question is only ever 'can the lightest ride with the heaviest', because " +
                "the heaviest has to leave on this trip regardless.",
             { ptr: { l: l, r: r }, span: [l, r], aux: [{ label: "boats", text: "0" }] });
      while (l <= r) {
        var fits = people[l] + people[r] <= limit;
        if (l === r) {
          t.snap(3, "one person left (" + people[l] + ") — they get a boat to themselves.",
                 { ptr: { l: l }, mark: { [l]: "done" }, aux: [{ label: "boats", text: String(boats + 1) }] });
        } else {
          t.snap(3, people[l] + " + " + people[r] + " = " + (people[l] + people[r]) +
                    (fits ? " ≤ " + limit + " — they share a boat."
                          : " > " + limit + " — the heaviest goes alone."),
                 { ptr: { l: l, r: r }, span: [l, r],
                   mark: merge({ [r]: "pick" }, fits ? { [l]: "pick" } : { [l]: "bad" }),
                   aux: [{ label: "boats", text: String(boats + 1) }] });
        }
        if (fits) l += 1;
        r -= 1;
        boats += 1;
      }
      t.snap(4, "Answer " + boats + " boats. r drops EVERY round (the heaviest always leaves); l only advances " +
                "when the pairing actually fits.",
             { aux: [{ label: "boats", text: String(boats) }] });
      return { trace: t, answer: boats };
    }
  };

  /* ================================== UNION-FIND ================================== */

  G["dsu-connect"] = {
    input: [{ id: "n", label: "number of nodes", type: "int", def: 6 },
            { id: "edges", label: "edges  a,b", type: "pairs", def: "0,1 1,2 3,4" }],
    check: function (v) {
      if (v.n < 1 || v.n > 10) return "use between 1 and 10 nodes so the trace stays watchable";
      for (var i = 0; i < v.edges.length; i++) {
        var e = v.edges[i];
        if (e[0] < 0 || e[1] < 0 || e[0] >= v.n || e[1] >= v.n)
          return "edge " + e[0] + "," + e[1] + " uses a node outside 0.." + (v.n - 1);
      }
    },
    brute: function (v) {              /* flood fill over the adjacency -- not DSU */
      var adj = [], i;
      for (i = 0; i < v.n; i++) adj.push([]);
      for (i = 0; i < v.edges.length; i++) {
        adj[v.edges[i][0]].push(v.edges[i][1]);
        adj[v.edges[i][1]].push(v.edges[i][0]);
      }
      var seen = {}, comps = 0;
      for (i = 0; i < v.n; i++) {
        if (seen[i]) continue;
        comps++;
        var st = [i]; seen[i] = 1;
        while (st.length) {
          var u = st.pop();
          for (var k = 0; k < adj[u].length; k++) if (!seen[adj[u][k]]) { seen[adj[u][k]] = 1; st.push(adj[u][k]); }
        }
      }
      return comps;
    },
    run: function (v) {
      var n = v.n, edges = v.edges, i;
      var cells = [];
      for (i = 0; i < n; i++) cells.push(i);
      var t = new Trace(cells, ["p = list(range(n));  groups = n", "for a, b in edges:",
                                "    ra, rb = find(a), find(b)", "    if ra == rb: continue   # redundant",
                                "    p[rb] = ra;  groups -= 1"],
                        "array", "count groups as edges arrive (cells are the nodes)");
      var p = [];
      for (i = 0; i < n; i++) p.push(i);
      var groups = n;
      function find(x) { while (p[x] !== x) { p[x] = p[p[x]]; x = p[x]; } return x; }
      var roots = function () { var o = []; for (var k = 0; k < n; k++) o.push(String(find(k))); return o; };
      t.snap(0, "Everyone starts as their own group. The reason this beats a DFS sweep is that it answers " +
                "'are these two connected' while edges are STILL ARRIVING.",
             { mark: range(0, n - 1, "pick"),
               aux: [{ label: "parent", items: strs(p) }, { label: "groups", text: String(groups) }] });
      for (i = 0; i < edges.length; i++) {
        var a = edges[i][0], b = edges[i][1];
        var ra = find(a), rb = find(b);
        if (ra === rb) {
          t.snap(3, "edge " + a + "–" + b + ": both already lead to root " + ra +
                    " — this edge joins nothing, so it CLOSES A CYCLE. That is the whole redundant-edge test.",
                 { ptr: { a: a, b: b }, mark: merge({ [a]: "bad" }, { [b]: "bad" }),
                   aux: [{ label: "root of each", items: roots() }, { label: "groups", text: String(groups) }] });
          continue;
        }
        t.snap(2, "edge " + a + "–" + b + ": root of " + a + " is " + ra + ", root of " + b + " is " + rb +
                  ". Different, so this edge really merges two groups.",
               { ptr: { a: a, b: b }, mark: merge({ [a]: "pick" }, { [b]: "pick" },
                                                  { [ra]: "done" }, { [rb]: "done" }),
                 aux: [{ label: "root of each", items: roots() }] });
        p[rb] = ra;
        groups -= 1;
        t.snap(4, "hang " + rb + " under " + ra + ". One union, one fewer group → " + groups + ".",
               { ptr: { a: a, b: b }, mark: { [ra]: "done" },
                 aux: [{ label: "parent", items: strs(p) }, { label: "root of each", items: roots() },
                       { label: "groups", text: String(groups) }] });
      }
      t.snap(4, "Answer " + groups + " group(s). Always compare ROOTS, never the raw values.",
             { aux: [{ label: "root of each", items: roots() }, { label: "groups", text: String(groups) }] });
      return { trace: t, answer: groups };
    }
  };

  /* ============================== TOPOLOGICAL SORT ================================ */

  G["to-kahn"] = {
    input: [{ id: "n", label: "number of tasks", type: "int", def: 6 },
            { id: "edges", label: "a before b", type: "pairs", def: "0,1 0,2 1,3 2,3 3,4" }],
    check: function (v) {
      if (v.n < 1 || v.n > 10) return "use between 1 and 10 tasks so the trace stays watchable";
      for (var i = 0; i < v.edges.length; i++) {
        var e = v.edges[i];
        if (e[0] < 0 || e[1] < 0 || e[0] >= v.n || e[1] >= v.n)
          return "edge " + e[0] + "," + e[1] + " uses a task outside 0.." + (v.n - 1);
      }
    },
    brute: function (v) {              /* three-colour DFS cycle check -- not Kahn */
      var adj = [], i;
      for (i = 0; i < v.n; i++) adj.push([]);
      for (i = 0; i < v.edges.length; i++) adj[v.edges[i][0]].push(v.edges[i][1]);
      var color = [];
      for (i = 0; i < v.n; i++) color.push(0);
      var bad = false;
      var dfs = function (u) {
        if (color[u] === 1) { bad = true; return; }
        if (color[u] === 2) return;
        color[u] = 1;
        for (var k = 0; k < adj[u].length; k++) { dfs(adj[u][k]); if (bad) return; }
        color[u] = 2;
      };
      for (i = 0; i < v.n && !bad; i++) dfs(i);
      return bad ? 0 : 1;
    },
    run: function (v) {
      var n = v.n, edges = v.edges, i;
      var cells = [];
      for (i = 0; i < n; i++) cells.push(i);
      var t = new Trace(cells, ["indeg[b] += 1 for every edge a->b", "q = [i for i if indeg[i] == 0]",
                                "while q:", "    u = q.popleft(); order.append(u)",
                                "    for v in adj[u]: indeg[v] -= 1",
                                "        if indeg[v] == 0: q.append(v)",
                                "return order if len(order) == n else CYCLE"],
                        "array", "Kahn's algorithm — cells are the tasks");
      var adj = [], indeg = [];
      for (i = 0; i < n; i++) { adj.push([]); indeg.push(0); }
      for (i = 0; i < edges.length; i++) { adj[edges[i][0]].push(edges[i][1]); indeg[edges[i][1]] += 1; }
      t.snap(0, "indegree = how many prerequisites each task still has. Get the edge DIRECTION right: " +
                "'to do b you need a' is an edge a→b.",
             { aux: [{ label: "indegree", items: strs(indeg) }] });
      var q = [];
      for (i = 0; i < n; i++) if (indeg[i] === 0) q.push(i);
      t.snap(1, "everything at indegree 0 can start immediately: " + (q.length ? q.join(", ") : "nothing") +
                (q.length ? "." : " — and if nothing can start, every task is waiting on another one."),
             { mark: (function () { var m = {}; for (var k = 0; k < q.length; k++) m[q[k]] = "pick"; return m; })(),
               aux: [{ label: "queue", items: strs(q) }, { label: "indegree", items: strs(indeg) }] });
      var order = [];
      while (q.length) {
        var u = q.shift();
        order.push(u);
        t.snap(3, "task " + u + " has no prerequisites left — emit it.",
               { ptr: { u: u }, mark: merge((function () { var m = {}; for (var k = 0; k < order.length; k++) m[order[k]] = "done"; return m; })(), { [u]: "pick" }),
                 aux: [{ label: "order", items: strs(order) }, { label: "queue", items: strs(q) }] });
        for (i = 0; i < adj[u].length; i++) {
          var w = adj[u][i];
          indeg[w] -= 1;
          t.snap(4, "task " + w + " loses a prerequisite → indegree " + indeg[w] +
                    (indeg[w] === 0 ? ", which frees it. Into the queue." : ", still waiting."),
                 { ptr: { u: u, w: w }, mark: merge({ [u]: "done" }, { [w]: indeg[w] === 0 ? "pick" : "bad" }),
                   aux: [{ label: "indegree", items: strs(indeg) }, { label: "queue", items: strs(q) }] });
          if (indeg[w] === 0) q.push(w);
        }
      }
      var ok = order.length === n ? 1 : 0;
      t.snap(6, ok
             ? ("Emitted all " + n + " tasks, so a valid order exists: " + order.join(" → ") + ".")
             : ("Only " + order.length + " of " + n + " tasks came out. The leftovers all still have " +
                "prerequisites, which can only mean they depend on each other — a CYCLE. " +
                "The cycle check is just len(order) == n; there is no separate pass to write."),
             { mark: (function () {
                 var m = {};
                 for (var k = 0; k < n; k++) m[k] = order.indexOf(k) >= 0 ? "done" : "bad";
                 return m;
               })(),
               aux: [{ label: "order", items: strs(order) },
                     { label: "verdict", text: ok ? "possible" : "cycle" }] });
      return { trace: t, answer: ok };
    }
  };
})();
