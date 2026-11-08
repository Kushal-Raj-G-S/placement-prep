/* =====================================================================================
   VIZ ENGINE, part G  --  string matching, segment tree / Fenwick, simulation.
   Loads after the other parts. Follows the exact G["variant-id"] = {input, check, brute,
   run} contract from viz_engine.js's header comment.
   ===================================================================================== */
(function () {
  "use strict";
  var G = (typeof module !== "undefined" && module.exports)
        ? require("./viz_engine.js")
        : window.VIZGEN;
  var H = G.__helpers, Trace = H.Trace, merge = H.merge, strs = H.strs;

  function K(r, c) { return r + "," + c; }
  function gridTrace(cells, code, caption) {
    return new Trace({ r: cells.length, c: cells[0].length, cells: cells }, code, "grid", caption);
  }

  /* ============================== STRING MATCHING ================================== */

  G["sm-kmp"] = {
    input: [{ id: "text", label: "text", type: "string", def: "ababcabcabababd" },
            { id: "pat", label: "pattern", type: "string", def: "ababd" }],
    check: function (v) {
      if (!v.pat.length) return "pattern can't be empty";
      if (v.pat.length > v.text.length) return "pattern can't be longer than the text";
    },
    brute: function (v) {
      var text = v.text, pat = v.pat, res = [];
      for (var i = 0; i + pat.length <= text.length; i++) {
        var ok = true;
        for (var j = 0; j < pat.length; j++) if (text[i + j] !== pat[j]) { ok = false; break; }
        if (ok) res.push(i);
      }
      return res.join(",");
    },
    run: function (v) {
      var text = v.text, pat = v.pat;
      var t = new Trace(text,
        ["lps = build_failure_array(pat)", "k = 0", "for i, ch in enumerate(text):",
         "    while k and ch != pat[k]:", "        k = lps[k-1]", "    if ch == pat[k]: k += 1",
         "    if k == len(pat):", "        record match; k = lps[k-1]"],
        "string", "find '" + pat + "' inside '" + text + "'");
      var lps = [0], kk = 0;
      for (var i = 1; i < pat.length; i++) {
        while (kk && pat[i] !== pat[kk]) kk = lps[kk - 1];
        if (pat[i] === pat[kk]) kk++;
        lps.push(kk);
      }
      t.snap(0, "Built the failure array from the pattern alone: lps = [" + lps.join(",") + "]. " +
                "lps[j] says how far to fall back after a mismatch at pattern position j.",
             { aux: [{ label: "pattern", text: pat }, { label: "lps", text: "[" + lps.join(",") + "]" }] });
      var k = 0, matches = [];
      for (var idx = 0; idx < text.length; idx++) {
        var ch = text[idx];
        while (k && ch !== pat[k]) k = lps[k - 1];
        if (ch === pat[k]) k++;
        t.snap(5, "text[" + idx + "]='" + ch + "' " + (k > 0 ? "extends the match to k=" + k : "breaks the match, k=0") + ".",
               { ptr: { i: idx }, span: (k > 0 ? [idx - k + 1, idx] : null),
                 aux: [{ label: "matched so far (k)", text: String(k) }] });
        if (k === pat.length) {
          matches.push(idx - k + 1);
          t.snap(7, "k reached " + pat.length + " — match at index " + (idx - k + 1) + ". Fall back with lps " +
                    "instead of resetting to 0, so overlapping matches are not missed.",
                 { ptr: { i: idx }, span: [idx - k + 1, idx], mark: { [idx]: "pick" },
                   aux: [{ label: "matches", items: matches.map(String) }] });
          k = lps[k - 1];
        }
      }
      t.snap(matches.length ? 7 : 2, "Answer: matches at [" + matches.join(", ") + "]. " +
                text.length + " characters scanned once each.",
             { aux: [{ label: "matches", items: matches.map(String) }] });
      return { trace: t, answer: matches.join(",") };
    }
  };

  G["sm-rabinkarp"] = {
    input: [{ id: "text", label: "text", type: "string", def: "abazbabxab" },
            { id: "pat", label: "pattern", type: "string", def: "ab" }],
    check: function (v) {
      if (!v.pat.length) return "pattern can't be empty";
      if (v.pat.length > v.text.length) return "pattern can't be longer than the text";
    },
    brute: function (v) {
      var text = v.text, pat = v.pat, res = [];
      for (var i = 0; i + pat.length <= text.length; i++) {
        var ok = true;
        for (var j = 0; j < pat.length; j++) if (text[i + j] !== pat[j]) { ok = false; break; }
        if (ok) res.push(i);
      }
      return res.join(",");
    },
    run: function (v) {
      var text = v.text, pat = v.pat, m = pat.length, n = text.length;
      var BASE = 131, MOD = 1000000007;
      function code(ch) { return ch.charCodeAt(0); }
      function modpow(b, e, mod) {
        var r = 1; b = b % mod;
        while (e > 0) { if (e & 1) r = (r * b) % mod; e = Math.floor(e / 2); b = (b * b) % mod; }
        return r;
      }
      var t = new Trace(text,
        ["hPat = hash(pat); hTxt = hash(text[0:m])", "for i in range(n - m + 1):",
         "    if hPat == hTxt and text[i:i+m] == pat:", "        record match",
         "    hTxt = roll(hTxt, text[i], text[i+m])"],
        "string", "find '" + pat + "' inside '" + text + "' with a rolling hash");
      var pPow = modpow(BASE, m - 1, MOD);
      var hPat = 0, hTxt = 0;
      for (var i = 0; i < m; i++) { hPat = (hPat * BASE + code(pat[i])) % MOD; hTxt = (hTxt * BASE + code(text[i])) % MOD; }
      t.snap(0, "hash(pattern) = " + hPat + ", hash(first window) = " + hTxt + ". Equal hashes are a CANDIDATE, not proof.",
             { span: [0, m - 1], aux: [{ label: "pattern", text: pat }, { label: "hash(pat)", text: String(hPat) },
                                        { label: "hash(window)", text: String(hTxt) }] });
      var matches = [];
      for (var idx = 0; idx + m <= n; idx++) {
        var collide = (hPat === hTxt);
        var verified = collide && text.substr(idx, m) === pat;
        t.snap(2, collide
                 ? ("hashes match at window [" + idx + ".." + (idx + m - 1) + "] — verifying character by " +
                    "character: " + (verified ? "confirmed." : "a real collision, rejected."))
                 : ("hash(window) ≠ hash(pat) at [" + idx + ".." + (idx + m - 1) + "] — skip with no character comparison."),
               { span: [idx, idx + m - 1], mark: verified ? { [idx]: "pick" } : {},
                 aux: [{ label: "hash(window)", text: String(hTxt) }, { label: "matches", items: matches.map(String) }] });
        if (verified) matches.push(idx);
        if (idx + m < n) {
          hTxt = (((hTxt - code(text[idx]) * pPow) % MOD + MOD) * BASE + code(text[idx + m])) % MOD;
        }
      }
      t.snap(matches.length ? 2 : 1, "Answer: matches at [" + matches.join(", ") + "].",
             { aux: [{ label: "matches", items: matches.map(String) }] });
      return { trace: t, answer: matches.join(",") };
    }
  };

  G["sm-z"] = {
    input: [{ id: "s", label: "string", type: "string", def: "aabaabaab" }],
    check: function (v) { if (!v.s.length) return "type a string"; },
    brute: function (v) {
      var s = v.s, n = s.length, z = [];
      for (var i = 0; i < n; i++) {
        if (i === 0) { z.push(0); continue; }
        var k = 0;
        while (i + k < n && s[k] === s[i + k]) k++;
        z.push(k);
      }
      return z.join(",");
    },
    run: function (v) {
      var s = v.s, n = s.length;
      var t = new Trace(s,
        ["z = [0]*n; l = r = 0", "for i in range(1, n):", "    if i < r: z[i] = min(r-i, z[i-l])",
         "    while i+z[i] < n and s[z[i]] == s[i+z[i]]: z[i] += 1", "    if i+z[i] > r: l, r = i, i+z[i]"],
        "string", "every position's match length with the prefix of '" + s + "'");
      var z = new Array(n).fill(0), l = 0, r = 0;
      t.snap(0, "z[i] will hold how far s starting at i matches the prefix of s. z[0] is left 0 by convention.",
             { aux: [{ label: "z", text: "[" + z.join(",") + "]" }] });
      for (var i = 1; i < n; i++) {
        if (i < r) {
          z[i] = Math.min(r - i, z[i - l]);
          t.snap(2, "i=" + i + " is inside the window [" + l + "," + r + ") found earlier — reuse z[" + (i - l) +
                    "]=" + z[i - l] + " as a head start: z[" + i + "]=" + z[i] + ".",
                 { ptr: { i: i, l: l, r: r - 1 }, aux: [{ label: "z", text: "[" + z.join(",") + "]" }] });
        }
        var before = z[i];
        while (i + z[i] < n && s[z[i]] === s[i + z[i]]) z[i]++;
        if (z[i] > before) {
          t.snap(3, "extended by direct comparison: z[" + i + "] = " + z[i] + ".",
                 { ptr: { i: i }, span: (z[i] > 0 ? [i, i + z[i] - 1] : null), aux: [{ label: "z", text: "[" + z.join(",") + "]" }] });
        }
        if (i + z[i] > r) {
          l = i; r = i + z[i];
          t.snap(4, "this match reaches further right than any before — window becomes [" + l + "," + r + ").",
                 { ptr: { l: l, r: Math.max(r - 1, l) }, aux: [{ label: "z", text: "[" + z.join(",") + "]" }] });
        }
      }
      t.snap(1, "Answer: z = [" + z.join(",") + "].", { aux: [{ label: "z", text: "[" + z.join(",") + "]" }] });
      return { trace: t, answer: z.join(",") };
    }
  };

  /* ============================ SEGMENT TREE / FENWICK ============================== */

  G["st-range"] = {
    input: [{ id: "a", label: "array", type: "ints", def: "5 2 8 1 9 3" },
            { id: "idx", label: "update index", type: "int", def: 2 },
            { id: "val", label: "new value", type: "int", def: 10 },
            { id: "l", label: "query l", type: "int", def: 1 },
            { id: "r", label: "query r (exclusive)", type: "int", def: 5 }],
    check: function (v) {
      var n = v.a.length;
      if (v.idx < 0 || v.idx >= n) return "update index must be inside the array";
      if (v.l < 0 || v.r > n || v.l >= v.r) return "need 0 <= l < r <= n";
    },
    brute: function (v) {
      var arr = v.a.slice(); arr[v.idx] = v.val;
      var s = 0; for (var i = v.l; i < v.r; i++) s += arr[i];
      return s;
    },
    run: function (v) {
      var a = v.a, n = a.length;
      var tr = new Array(2 * n).fill(0);
      for (var i = 0; i < n; i++) tr[n + i] = a[i];
      for (i = n - 1; i >= 1; i--) tr[i] = tr[2 * i] + tr[2 * i + 1];
      var t = new Trace(a, ["build: t[n+i] = a[i]; combine upward",
                            "update(idx, val): t[idx+n] = val; climb, recombine",
                            "query(l, r): absorb boundary nodes while l < r"],
                        "array", "segment tree over [" + a.join(",") + "]");
      t.snap(0, "Built bottom-up: leaves are the array, each internal node the sum of its two children.",
             { aux: [{ label: "tree array", items: strs(tr) }] });
      var pos = v.idx + n;
      tr[pos] = v.val;
      t.snap(1, "a[" + v.idx + "] becomes " + v.val + " — update the leaf, then climb fixing every ancestor.",
             { span: [v.idx, v.idx], mark: { [v.idx]: "pick" }, aux: [{ label: "tree array", items: strs(tr) }] });
      pos = Math.floor(pos / 2);
      while (pos >= 1) {
        tr[pos] = tr[2 * pos] + tr[2 * pos + 1];
        t.snap(1, "ancestor fixed: t[" + pos + "] = t[" + (2 * pos) + "] + t[" + (2 * pos + 1) + "] = " + tr[pos] + ".",
               { span: [v.idx, v.idx], aux: [{ label: "tree array", items: strs(tr) }] });
        pos = Math.floor(pos / 2);
      }
      var l = v.l + n, r = v.r + n, res = 0;
      t.snap(2, "query [" + v.l + ", " + v.r + "): walk l and r inward, absorbing any node entirely outside.",
             { span: [v.l, v.r - 1], aux: [{ label: "running sum", text: "0" }] });
      while (l < r) {
        if (l & 1) { res += tr[l]; l++; }
        if (r & 1) { r--; res += tr[r]; }
        l = Math.floor(l / 2); r = Math.floor(r / 2);
        t.snap(2, "absorbed a node — running sum = " + res + ".",
               { span: [v.l, v.r - 1], aux: [{ label: "running sum", text: String(res) }] });
      }
      t.snap(2, "Answer " + res + ".", { span: [v.l, v.r - 1], aux: [{ label: "running sum", text: String(res) }] });
      return { trace: t, answer: res };
    }
  };

  G["st-fenwick"] = {
    input: [{ id: "a", label: "array", type: "ints", def: "4 1 7 3 9 2" },
            { id: "idx", label: "index to update", type: "int", def: 3 },
            { id: "delta", label: "add", type: "int", def: 5 },
            { id: "l", label: "query l", type: "int", def: 0 },
            { id: "r", label: "query r (exclusive)", type: "int", def: 4 }],
    check: function (v) {
      var n = v.a.length;
      if (v.idx < 0 || v.idx >= n) return "update index must be inside the array";
      if (v.l < 0 || v.r > n || v.l >= v.r) return "need 0 <= l < r <= n";
    },
    brute: function (v) {
      var arr = v.a.slice(); arr[v.idx] += v.delta;
      var s = 0; for (var i = v.l; i < v.r; i++) s += arr[i];
      return s;
    },
    run: function (v) {
      var a = v.a, n = a.length, fen = new Array(n + 1).fill(0);
      var t = new Trace(a, ["build: for each i, add(i+1, a[i])",
                            "add(idx+1, delta): i += i & (-i), climb",
                            "query: prefix(r) - prefix(l), each via i -= i & (-i)"],
                        "array", "Fenwick tree over [" + a.join(",") + "]");
      function add(pos, d) { for (; pos <= n; pos += pos & (-pos)) fen[pos] += d; }
      for (var i = 0; i < n; i++) add(i + 1, a[i]);
      t.snap(0, "Built by adding each element once. fen[i] covers (i & -i) elements ending at i (1-indexed).",
             { aux: [{ label: "fenwick array (1-indexed)", items: strs(fen) }] });
      var pos = v.idx + 1, touched = [];
      while (pos <= n) {
        fen[pos] += v.delta; touched.push(pos);
        t.snap(1, "fen[" + pos + "] += " + v.delta + " -> " + fen[pos] + ". Next: i += i & -i.",
               { span: [v.idx, v.idx], mark: { [v.idx]: "pick" },
                 aux: [{ label: "fenwick array (1-indexed)", items: strs(fen) }, { label: "touched", items: touched.map(String) }] });
        pos += pos & (-pos);
      }
      function prefixTrace(x) {
        var s = 0, j = x, path = [];
        while (j > 0) { s += fen[j]; path.push(j); j -= j & (-j); }
        t.snap(2, "prefix(" + x + ") = " + s + " (sum of a[0.." + (x - 1) + "])" +
                  (path.length ? ", via fen[" + path.join("], fen[") + "]." : " — empty prefix."),
               { span: x > 0 ? [0, x - 1] : null, aux: [{ label: "running prefix sum", text: String(s) }] });
        return s;
      }
      var pr = prefixTrace(v.r), pl = prefixTrace(v.l);
      var res = pr - pl;
      t.snap(2, "Answer: prefix(" + v.r + ") - prefix(" + v.l + ") = " + pr + " - " + pl + " = " + res + ".",
             { span: v.r > v.l ? [v.l, v.r - 1] : null, aux: [{ label: "answer", text: String(res) }] });
      return { trace: t, answer: res };
    }
  };

  G["st-lazy"] = {
    input: [{ id: "a", label: "array", type: "ints", def: "3 1 4 1 5 9 2 6" },
            { id: "l2", label: "range-add l", type: "int", def: 2 },
            { id: "r2", label: "range-add r (exclusive)", type: "int", def: 6 },
            { id: "delta", label: "add", type: "int", def: 3 },
            { id: "l", label: "query l", type: "int", def: 1 },
            { id: "r", label: "query r (exclusive)", type: "int", def: 7 }],
    check: function (v) {
      var n = v.a.length;
      if (v.l2 < 0 || v.r2 > n || v.l2 >= v.r2) return "need 0 <= l2 < r2 <= n for the range update";
      if (v.l < 0 || v.r > n || v.l >= v.r) return "need 0 <= l < r <= n for the query";
    },
    brute: function (v) {
      var arr = v.a.slice();
      for (var i = v.l2; i < v.r2; i++) arr[i] += v.delta;
      var s = 0; for (i = v.l; i < v.r; i++) s += arr[i];
      return s;
    },
    run: function (v) {
      var a = v.a, n = a.length;
      var sum = new Array(4 * n).fill(0), lazy = new Array(4 * n).fill(0);
      var t = new Trace(a, ["build(node,l,r)", "push(node,l,r): spread pending lazy to children",
                            "update(node,l,r,ql,qr,delta): add delta to [ql,qr)",
                            "query(node,l,r,ql,qr): sum of [ql,qr)"],
                        "array", "lazy segment tree over [" + a.join(",") + "]");
      function build(node, l, r) {
        if (l === r - 1) { sum[node] = a[l]; return; }
        var m = (l + r) >> 1;
        build(2 * node, l, m); build(2 * node + 1, m, r);
        sum[node] = sum[2 * node] + sum[2 * node + 1];
      }
      build(1, 0, n);
      t.snap(0, "Built bottom-up: each leaf is one array element, each internal node the sum of its range.",
             { aux: [{ label: "sum[] (tree)", items: strs(sum) }] });
      function push(node, l, r) {
        if (lazy[node]) {
          var m = (l + r) >> 1;
          lazy[2 * node] += lazy[node]; sum[2 * node] += lazy[node] * (m - l);
          lazy[2 * node + 1] += lazy[node]; sum[2 * node + 1] += lazy[node] * (r - m);
          t.snap(1, "node had a pending +" + lazy[node] + " — pushed down to both children before descending.",
                 { span: [l, r - 1], aux: [{ label: "sum[] (tree)", items: strs(sum) }, { label: "lazy[] (tree)", items: strs(lazy) }] });
          lazy[node] = 0;
        }
      }
      function update(node, l, r, ql, qr, delta) {
        if (qr <= l || r <= ql) return;
        if (ql <= l && r <= qr) {
          sum[node] += delta * (r - l); lazy[node] += delta;
          t.snap(2, "[" + l + "," + r + ") is fully inside the update range — apply here, do NOT recurse further.",
                 { span: [l, r - 1], mark: { [l]: "pick" }, aux: [{ label: "sum[] (tree)", items: strs(sum) }, { label: "lazy[] (tree)", items: strs(lazy) }] });
          return;
        }
        push(node, l, r);
        var m = (l + r) >> 1;
        update(2 * node, l, m, ql, qr, delta); update(2 * node + 1, m, r, ql, qr, delta);
        sum[node] = sum[2 * node] + sum[2 * node + 1];
      }
      update(1, 0, n, v.l2, v.r2, v.delta);
      t.snap(2, "range-add +" + v.delta + " applied to [" + v.l2 + "," + v.r2 + ").",
             { span: [v.l2, v.r2 - 1], aux: [{ label: "sum[] (tree)", items: strs(sum) }] });
      function query(node, l, r, ql, qr) {
        if (qr <= l || r <= ql) return 0;
        if (ql <= l && r <= qr) {
          t.snap(3, "[" + l + "," + r + ") is fully inside the query — take sum[node]=" + sum[node] + " directly.",
                 { span: [l, r - 1], aux: [{ label: "running total", text: String(sum[node]) }] });
          return sum[node];
        }
        push(node, l, r);
        var m = (l + r) >> 1;
        return query(2 * node, l, m, ql, qr) + query(2 * node + 1, m, r, ql, qr);
      }
      var res = query(1, 0, n, v.l, v.r);
      t.snap(3, "Answer " + res + " for range [" + v.l + "," + v.r + ").",
             { span: v.r > v.l ? [v.l, v.r - 1] : null, aux: [{ label: "answer", text: String(res) }] });
      return { trace: t, answer: res };
    }
  };

  /* ================================= SIMULATION ====================================== */

  G["sim-spiral"] = {
    input: [{ id: "g", label: "grid rows of single digits", type: "gridnum", def: "123 456 789" }],
    check: function (v) {
      if (v.g.length > 6 || v.g[0].length > 6) return "keep the grid within 6x6 so the spiral stays watchable";
    },
    brute: function (v) {
      var g = v.g, R = g.length, C = g[0].length;
      var visited = g.map(function (row) { return row.map(function () { return false; }); });
      var dirs = [[0, 1], [1, 0], [0, -1], [-1, 0]];
      var r = 0, c = 0, d = 0, out = [];
      for (var k = 0; k < R * C; k++) {
        out.push(g[r][c]); visited[r][c] = true;
        var nr = r + dirs[d][0], nc = c + dirs[d][1];
        if (nr < 0 || nr >= R || nc < 0 || nc >= C || visited[nr][nc]) {
          d = (d + 1) % 4; nr = r + dirs[d][0]; nc = c + dirs[d][1];
        }
        r = nr; c = nc;
      }
      return out.join(",");
    },
    run: function (v) {
      var g = v.g, R = g.length, C = g[0].length;
      var cells = g.map(function (row) { return row.map(String); });
      var t = gridTrace(cells, ["top,bot,left,right = bounds", "walk top row; top += 1",
                                "walk right col; right -= 1", "walk bottom row (if any); bot -= 1",
                                "walk left col (if any); left += 1"],
                        "spiral order of a " + R + "x" + C + " grid");
      var top = 0, bot = R - 1, left = 0, right = C - 1, out = [], mark = {};
      t.snap(0, "boundaries start at the full grid: top=" + top + " bot=" + bot + " left=" + left + " right=" + right + ".", {});
      while (top <= bot && left <= right) {
        for (var c = left; c <= right; c++) { out.push(g[top][c]); mark[K(top, c)] = "pick"; }
        t.snap(1, "walked the top row (row " + top + "). top becomes " + (top + 1) + ".",
               { ptr: { at: K(top, right) }, mark: merge(mark) });
        top++;
        for (var r = top; r <= bot; r++) { out.push(g[r][right]); mark[K(r, right)] = "pick"; }
        if (top <= bot)
          t.snap(2, "walked the right column (col " + right + "). right becomes " + (right - 1) + ".",
                 { ptr: { at: K(bot, right) }, mark: merge(mark) });
        right--;
        if (top <= bot) {
          for (var c2 = right; c2 >= left; c2--) { out.push(g[bot][c2]); mark[K(bot, c2)] = "pick"; }
          t.snap(3, "walked the bottom row (row " + bot + "). bot becomes " + (bot - 1) + ".",
                 { ptr: { at: K(bot, left) }, mark: merge(mark) });
          bot--;
        }
        if (left <= right) {
          for (var r2 = bot; r2 >= top; r2--) { out.push(g[r2][left]); mark[K(r2, left)] = "pick"; }
          t.snap(4, "walked the left column (col " + left + "). left becomes " + (left + 1) + ".",
                 { ptr: { at: K(top, left) }, mark: merge(mark) });
          left++;
        }
      }
      t.snap(0, "Answer: " + out.join(", ") + ".", { mark: merge(mark) });
      return { trace: t, answer: out.join(",") };
    }
  };

  G["sim-rotate"] = {
    input: [{ id: "g", label: "square matrix rows", type: "gridnum", def: "123 456 789" }],
    check: function (v) {
      if (v.g.length !== v.g[0].length) return "the matrix must be square to rotate in place";
      if (v.g.length > 6) return "keep it within 6x6 so the trace stays watchable";
    },
    brute: function (v) {
      var g = v.g, n = g.length, rotated = [];
      for (var c = 0; c < n; c++) {
        var row = [];
        for (var r = n - 1; r >= 0; r--) row.push(g[r][c]);
        rotated.push(row.join(""));
      }
      return rotated.join(",");
    },
    run: function (v) {
      var g = v.g.map(function (row) { return row.slice(); }), n = g.length;
      var cells = g.map(function (row) { return row.map(String); });
      var t = gridTrace(cells, ["transpose: swap g[i][j], g[j][i] for j>i", "reverse each row"],
                        "rotate a " + n + "x" + n + " matrix 90°");
      t.snap(0, "Transpose first: mirror everything across the main diagonal.", {});
      for (var i = 0; i < n; i++) {
        for (var j = i + 1; j < n; j++) {
          var tmp = g[i][j]; g[i][j] = g[j][i]; g[j][i] = tmp;
          t.snap(0, "swap (" + i + "," + j + ") with (" + j + "," + i + ").",
                 { mark: { [K(i, j)]: "pick", [K(j, i)]: "pick" } });
        }
      }
      t.snap(1, "transpose done — now reverse each row left-to-right.", {});
      for (i = 0; i < n; i++) {
        g[i].reverse();
        var rowMark = {};
        for (var cc = 0; cc < n; cc++) rowMark[K(i, cc)] = "pick";
        t.snap(1, "reversed row " + i + ".", { mark: rowMark });
      }
      var flat = [];
      for (i = 0; i < n; i++) flat.push(g[i].join(""));
      t.snap(1, "Answer: " + flat.join(" / ") + ".", {});
      return { trace: t, answer: flat.join(",") };
    }
  };

  G["sim-marking"] = {
    input: [{ id: "g", label: "grid rows of single digits", type: "gridnum", def: "102 030 405" }],
    check: function (v) {
      if (v.g.length > 6 || v.g[0].length > 6) return "keep the grid within 6x6 so the trace stays watchable";
    },
    brute: function (v) {
      var g = v.g.map(function (row) { return row.slice(); }), R = g.length, C = g[0].length;
      var rowZero = {}, colZero = {};
      for (var r = 0; r < R; r++) for (var c = 0; c < C; c++) if (g[r][c] === 0) { rowZero[r] = 1; colZero[c] = 1; }
      for (r = 0; r < R; r++) for (c = 0; c < C; c++) if (rowZero[r] || colZero[c]) g[r][c] = 0;
      return g.map(function (row) { return row.join(""); }).join(",");
    },
    run: function (v) {
      var g = v.g.map(function (row) { return row.slice(); }), R = g.length, C = g[0].length;
      var cells = g.map(function (row) { return row.map(String); });
      var t = gridTrace(cells, ["check if row 0 / col 0 themselves need zeroing",
                                "mark via row 0 / col 0 while scanning rows 1.. and cols 1..",
                                "apply the markers to rows 1.. and cols 1..",
                                "zero row 0 / col 0 if they were marked"],
                        R + "x" + C + " grid");
      var firstRow = false, firstCol = false;
      for (var c = 0; c < C; c++) if (g[0][c] === 0) firstRow = true;
      for (var r = 0; r < R; r++) if (g[r][0] === 0) firstCol = true;
      t.snap(0, "row 0 needs zeroing: " + firstRow + "; col 0 needs zeroing: " + firstCol +
                ". Remember this before row 0 / col 0 get reused as scratch space.", {});
      for (r = 1; r < R; r++) for (c = 1; c < C; c++) if (g[r][c] === 0) {
        g[r][0] = 0; g[0][c] = 0;
        t.snap(1, "cell (" + r + "," + c + ") is 0 — mark row " + r + " and column " + c + ".",
               { mark: { [K(r, c)]: "pick", [K(r, 0)]: "bad", [K(0, c)]: "bad" } });
      }
      for (r = 1; r < R; r++) for (c = 1; c < C; c++) if (g[r][0] === 0 || g[0][c] === 0) {
        g[r][c] = 0;
        t.snap(2, "row " + r + " or column " + c + " was marked — zero cell (" + r + "," + c + ").",
               { mark: { [K(r, c)]: "done" } });
      }
      if (firstRow) { for (c = 0; c < C; c++) g[0][c] = 0; t.snap(3, "row 0 itself needed zeroing.", {}); }
      if (firstCol) { for (r = 0; r < R; r++) g[r][0] = 0; t.snap(3, "column 0 itself needed zeroing.", {}); }
      var out = g.map(function (row) { return row.join(""); }).join(",");
      t.snap(3, "Answer: " + out + ".", {});
      return { trace: t, answer: out };
    }
  };
})();
