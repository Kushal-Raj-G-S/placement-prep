/* =====================================================================================
   VIZ ENGINE, part H  --  the traces added with the library audit: arrays, strings, maths, DP, greedy,
   divide and conquer, backtracking and the "design a data structure" variants.
   Same contract as viz_engine.js: G["variant-id"] = {input, check, brute, run}. A generator may also carry
   gen(rnd), which gives the fuzz test valid random inputs (so it does not have to guess).
   ===================================================================================== */
(function () {
  "use strict";
  var G = (typeof module !== "undefined" && module.exports) ? require("./viz_engine.js") : window.VIZGEN;
  var H = G.__helpers, Trace = H.Trace;

  function A(data, code, cap, kind) { return new Trace(data, code, kind || "array", cap); }
  function ri(rnd, lo, hi) { return lo + rnd(hi - lo + 1); }
  function ints(rnd, n, lo, hi) { var o = []; for (var i = 0; i < n; i++) o.push(ri(rnd, lo, hi)); return o; }
  function str(rnd, n, letters) { var s = ""; for (var i = 0; i < n; i++) s += letters.charAt(rnd(letters.length)); return s; }
  function gcd(a, b) { while (b) { var t = a % b; a = b; b = t; } return a; }
  function J(a) { return a.join(","); }
  function rng(lo, hi) { var o = []; for (var i = lo; i <= hi; i++) o.push(i); return o; }
  function aux() { var o = []; for (var i = 0; i < arguments.length; i += 2) o.push({ label: arguments[i], text: String(arguments[i + 1]) }); return o; }

  /* ================================ TWO POINTERS: centre ================================ */
  G["tp-centre"] = {
    input: [{ id: "s", label: "string", type: "string", def: "babad" }],
    check: function (v) { if (!v.s.length || v.s.length > 14) return "use 1 to 14 characters"; },
    gen: function (rnd) { return { s: str(rnd, ri(rnd, 1, 9), "abc") }; },
    brute: function (v) {
      var s = v.s, best = 0;
      for (var i = 0; i < s.length; i++) for (var j = i; j < s.length; j++) {
        var p = true;
        for (var a = i, b = j; a < b; a++, b--) if (s[a] !== s[b]) { p = false; break; }
        if (p && j - i + 1 > best) best = j - i + 1;
      }
      return best;
    },
    run: function (v) {
      var s = v.s, n = s.length, best = 0, bl = 0;
      var t = A(s, ["for i in range(len(s)):", "    for (l, r) in ((i, i), (i, i+1)):   # odd and even centre",
                    "        while l >= 0 and r < len(s) and s[l] == s[r]:", "            l -= 1; r += 1", "        best = max(best, r - l - 1)"],
                "longest palindromic substring, grown from every centre", "string");
      for (var i = 0; i < n; i++) {
        for (var e = 0; e < 2; e++) {
          var l = i, r = i + e;
          while (l >= 0 && r < n && s[l] === s[r]) { l--; r++; }
          var len = r - l - 1;
          if (len > best) { best = len; bl = l + 1; }
          t.snap(4, "centre " + (e ? "between " + i + " and " + (i + 1) : "on " + i) + " grows to length " + len + ". Best so far " + best + ".",
                 len > 0 ? { ptr: { centre: i }, span: [l + 1, r - 1], aux: aux("best", best) } : { ptr: { centre: i }, aux: aux("best", best) });
        }
      }
      t.snap(4, "Answer: length " + best + ", the substring '" + s.substr(bl, best) + "'. " + (2 * n - 1) + " centres, each grown at most n steps.",
             best > 0 ? { span: [bl, bl + best - 1], aux: aux("best", best) } : {});
      return { trace: t, answer: best };
    }
  };

  /* ================================ SLIDING WINDOW: complement ================================ */
  G["sw-complement"] = {
    input: [{ id: "a", label: "card points", type: "ints", def: "1 2 3 4 5 6 1" }, { id: "k", label: "take k from the ends", type: "int", def: 3 }],
    check: function (v) { if (v.k < 1 || v.k > v.a.length) return "k must be between 1 and the array length"; },
    gen: function (rnd) { var n = ri(rnd, 1, 8); return { a: ints(rnd, n, 1, 9), k: ri(rnd, 1, n) }; },
    brute: function (v) {
      var best = -1, n = v.a.length;
      for (var i = 0; i <= v.k; i++) {
        var s = 0, j;
        for (j = 0; j < i; j++) s += v.a[j];
        for (j = 0; j < v.k - i; j++) s += v.a[n - 1 - j];
        if (s > best) best = s;
      }
      return best;
    },
    run: function (v) {
      var a = v.a, k = v.k, n = a.length, keep = n - k, total = 0, i;
      for (i = 0; i < n; i++) total += a[i];
      var t = A(a, ["keep = len(a) - k            # the middle you do NOT take", "window = sum(a[:keep]); smallest = window",
                    "for r in range(keep, len(a)):", "    window += a[r] - a[r-keep]", "    smallest = min(smallest, window)", "return sum(a) - smallest"],
                "take k cards from the ends = leave the cheapest window of " + keep + " in the middle");
      if (keep === 0) {
        t.snap(5, "k equals the array length, so nothing stays behind: take everything = " + total + ".", { aux: aux("total", total) });
        return { trace: t, answer: total };
      }
      var w = 0;
      for (i = 0; i < keep; i++) w += a[i];
      var small = w;
      t.snap(0, "Taking k from the ends is the same as leaving a block of length " + keep + " untouched. Minimise what is left behind.",
             { span: [0, keep - 1], aux: aux("window", w, "smallest", small, "total", total) });
      for (var r = keep; r < n; r++) {
        w += a[r] - a[r - keep];
        if (w < small) small = w;
        t.snap(4, "slide: a[" + r + "]=" + a[r] + " in, a[" + (r - keep) + "]=" + a[r - keep] + " out. Window = " + w + ". Smallest = " + small + ".",
               { span: [r - keep + 1, r], aux: aux("window", w, "smallest", small, "total", total) });
      }
      t.snap(5, "Answer = total " + total + " − smallest middle " + small + " = " + (total - small) + ".", { aux: aux("answer", total - small) });
      return { trace: t, answer: total - small };
    }
  };

  /* ================================ HASHING: Boyer-Moore ================================ */
  G["hs-moore"] = {
    input: [{ id: "a", label: "array", type: "ints", def: "2 2 1 1 1 2 2" }],
    check: function (v) { if (v.a.length > 14) return "keep it to 14 elements"; },
    gen: function (rnd) { return { a: ints(rnd, ri(rnd, 1, 9), 1, 3) }; },
    brute: function (v) {
      var c = {}, i;
      v.a.forEach(function (x) { c[x] = (c[x] || 0) + 1; });
      for (var k in c) if (c[k] > v.a.length / 2) return Number(k);
      return "none";
    },
    run: function (v) {
      var a = v.a, cand = null, count = 0;
      var t = A(a, ["cand, count = None, 0", "for x in nums:", "    if count == 0: cand = x", "    count += 1 if x == cand else -1",
                    "return cand if nums.count(cand) > len(nums)//2 else None   # verify"],
                "Boyer-Moore vote: pairs of different values cancel");
      for (var i = 0; i < a.length; i++) {
        var x = a[i], note;
        if (count === 0) { cand = x; note = "count is 0, so " + x + " becomes the candidate."; } else note = "";
        count += (x === cand) ? 1 : -1;
        t.snap(3, "a[" + i + "]=" + x + ". " + note + (x === cand ? " Same as the candidate: count up." : " Different: it cancels one vote.") + " count = " + count + ".",
               { ptr: { x: i }, mark: (function () { var m = {}; m[i] = x === cand ? "pick" : "gone"; return m; })(), aux: aux("candidate", cand, "count", count) });
      }
      var occ = a.filter(function (x) { return x === cand; }).length;
      var ans = occ > a.length / 2 ? cand : "none";
      t.snap(4, "Verify: " + cand + " appears " + occ + " times of " + a.length + (occ > a.length / 2 ? " — more than half, so it is the majority." : " — not more than half, so there is NO majority.") + " Verification matters when a majority is not guaranteed.",
             { aux: aux("candidate", cand, "occurrences", occ, "answer", ans) });
      return { trace: t, answer: ans };
    }
  };

  /* ================================ MONOTONIC STACK: contribution ================================ */
  G["ms-contrib"] = {
    input: [{ id: "a", label: "array", type: "ints", def: "3 1 2 4" }],
    check: function (v) { if (v.a.length > 12) return "keep it to 12 elements"; },
    gen: function (rnd) { return { a: ints(rnd, ri(rnd, 1, 8), 1, 6) }; },
    brute: function (v) {
      var s = 0, n = v.a.length;
      for (var i = 0; i < n; i++) { var m = Infinity; for (var j = i; j < n; j++) { m = Math.min(m, v.a[j]); s += m; } }
      return s;
    },
    run: function (v) {
      var a = v.a, n = a.length, total = 0, st = [], done = {};
      var t = A(a, ["for i in range(n + 1):                 # i == n is a sentinel that flushes the stack", "    cur = a[i] if i < n else -inf",
                    "    while stack and a[stack[-1]] >= cur:", "        m = stack.pop(); left = stack[-1] if stack else -1",
                    "        total += a[m] * (m - left) * (i - m)   # a[m] is the minimum of that many subarrays", "    stack.append(i)"],
                "sum of the minimum of every subarray, counted element by element");
      for (var i = 0; i <= n; i++) {
        var cur = i < n ? a[i] : -Infinity;
        while (st.length && a[st[st.length - 1]] >= cur) {
          var m = st.pop(), left = st.length ? st[st.length - 1] : -1;
          var add = a[m] * (m - left) * (i - m);
          total += add; done[m] = "done";
          t.snap(4, "a[" + m + "]=" + a[m] + " is the minimum for " + (m - left) + " choices of left end × " + (i - m) + " choices of right end = " + (m - left) * (i - m) +
                    " subarrays, contributing " + add + ".",
                 { ptr: { m: m, i: i }, mark: Object.assign({}, done), span: [left + 1, Math.min(i, n) - 1 < left + 1 ? left + 1 : Math.min(i, n) - 1],
                   aux: aux("stack", "[" + st.join(",") + "]", "total", total) });
        }
        st.push(i);
        if (i < n) t.snap(5, "push index " + i + ". The stack keeps values increasing, so the left reach of each element is the one below it.",
                          { ptr: { i: i }, mark: Object.assign({}, done), aux: aux("stack", "[" + st.join(",") + "]", "total", total) });
      }
      t.snap(5, "Answer " + total + ". Each element was pushed and popped once, so O(n) instead of O(n²).", { mark: Object.assign({}, done), aux: aux("total", total) });
      return { trace: t, answer: total };
    }
  };

  /* ================================ HEAP: sorted container ================================ */
  G["hp-sorted"] = {
    input: [{ id: "a", label: "array", type: "ints", def: "1 5 9 1 5 9" }, { id: "k", label: "index gap k", type: "int", def: 2 },
            { id: "d", label: "value gap d", type: "int", def: 3 }],
    check: function (v) { if (v.k < 1 || v.d < 0) return "k must be at least 1 and d at least 0"; if (v.a.length > 12) return "keep it to 12 elements"; },
    gen: function (rnd) { return { a: ints(rnd, ri(rnd, 1, 8), 0, 20), k: ri(rnd, 1, 4), d: ri(rnd, 0, 4) }; },
    brute: function (v) {
      for (var i = 0; i < v.a.length; i++) for (var j = i + 1; j < v.a.length && j - i <= v.k; j++) if (Math.abs(v.a[i] - v.a[j]) <= v.d) return true;
      return false;
    },
    run: function (v) {
      var a = v.a, win = [];
      var t = A(a, ["window = []                         # kept SORTED", "for i, x in enumerate(nums):", "    pos = bisect_left(window, x - d)   # first value >= x - d",
                    "    if pos < len(window) and window[pos] <= x + d: return True", "    insort(window, x)", "    if i >= k: window.remove(nums[i - k])", "return False"],
                "is there a pair within index gap " + v.k + " and value gap " + v.d + "?");
      for (var i = 0; i < a.length; i++) {
        var x = a[i], pos = 0;
        while (pos < win.length && win[pos] < x - v.d) pos++;
        var hit = pos < win.length && win[pos] <= x + v.d;
        t.snap(3, "x=" + x + ": look for a value in [" + (x - v.d) + ", " + (x + v.d) + "] inside the sorted window. " + (hit ? "Found " + win[pos] + "." : "None there."),
               { ptr: { x: i }, aux: aux("window", "[" + win.join(", ") + "]") });
        if (hit) { t.snap(3, "A pair exists: " + win[pos] + " and " + x + ". Return True.", { ptr: { x: i }, aux: aux("answer", "true") }); return { trace: t, answer: true }; }
        win.push(x); win.sort(function (p, q) { return p - q; });
        if (i >= v.k) win.splice(win.indexOf(a[i - v.k]), 1);
        t.snap(5, "insert " + x + " in its sorted place" + (i >= v.k ? ", and drop a[" + (i - v.k) + "]=" + a[i - v.k] + " which is now too far back" : "") + ".",
               { ptr: { x: i }, aux: aux("window", "[" + win.join(", ") + "]") });
      }
      t.snap(6, "No pair found. Return False.", { aux: aux("answer", "false") });
      return { trace: t, answer: false };
    }
  };

  /* ================================ BITS: each bit on its own ================================ */
  G["bt-perbit"] = {
    input: [{ id: "a", label: "numbers", type: "ints", def: "4 14 2" }],
    check: function (v) { if (v.a.length > 10) return "keep it to 10 numbers"; for (var i = 0; i < v.a.length; i++) if (v.a[i] < 0 || v.a[i] > 63) return "use numbers from 0 to 63"; },
    gen: function (rnd) { return { a: ints(rnd, ri(rnd, 1, 8), 0, 31) }; },
    brute: function (v) {
      var s = 0;
      for (var i = 0; i < v.a.length; i++) for (var j = i + 1; j < v.a.length; j++) { var x = v.a[i] ^ v.a[j]; while (x) { s += x & 1; x >>= 1; } }
      return s;
    },
    run: function (v) {
      var a = v.a, n = a.length, total = 0;
      var t = A(a, ["total = 0", "for bit in range(6):", "    ones = sum((x >> bit) & 1 for x in nums)", "    total += ones * (n - ones)   # pairs that differ at this bit"],
                "total Hamming distance over all pairs, one bit at a time");
      for (var b = 0; b < 6; b++) {
        var m = {}, ones = 0;
        for (var i = 0; i < n; i++) if ((a[i] >> b) & 1) { ones++; m[i] = "pick"; }
        total += ones * (n - ones);
        t.snap(3, "bit " + b + ": " + ones + " numbers have it set, " + (n - ones) + " do not. Every set/unset pair differs here: " + ones + " × " + (n - ones) + " = " + ones * (n - ones) + ".",
               { mark: m, aux: aux("bit", b, "differing pairs", ones * (n - ones), "total", total) });
      }
      t.snap(3, "Answer " + total + ". n²/2 pairs would have been too slow; 6 passes over the array are not.", { aux: aux("total", total) });
      return { trace: t, answer: total };
    }
  };

  /* ================================ SIMULATION: follow the rules ================================ */
  G["sim-rules"] = {
    input: [{ id: "s", label: "text", type: "string", def: "paypalishiring" }, { id: "rows", label: "rows", type: "int", def: 3 }],
    check: function (v) { if (v.rows < 1 || v.rows > 6) return "rows between 1 and 6"; if (!v.s.length || v.s.length > 16) return "1 to 16 characters"; },
    gen: function (rnd) { return { s: str(rnd, ri(rnd, 1, 12), "abcdefgh"), rows: ri(rnd, 1, 5) }; },
    brute: function (v) {
      var s = v.s, r = v.rows;
      if (r === 1) return s;
      var cyc = 2 * r - 2, rowsOut = [], i;
      for (i = 0; i < r; i++) rowsOut.push("");
      for (i = 0; i < s.length; i++) { var p = i % cyc; rowsOut[Math.min(p, cyc - p)] += s[i]; }
      return rowsOut.join("");
    },
    run: function (v) {
      var s = v.s, R = v.rows;
      var t = A(s, ["lines = [''] * rows", "r, step = 0, 1", "for ch in s:", "    lines[r] += ch", "    if r == 0: step = 1", "    elif r == rows - 1: step = -1",
                    "    r += step", "return ''.join(lines)"], "zigzag over " + R + " rows, then read row by row", "string");
      var lines = [], i;
      for (i = 0; i < R; i++) lines.push("");
      if (R === 1) { t.snap(7, "One row: the text is unchanged.", {}); return { trace: t, answer: s }; }
      var r = 0, step = 1;
      for (i = 0; i < s.length; i++) {
        lines[r] += s[i];
        t.snap(3, "'" + s[i] + "' goes on row " + r + ".", { ptr: { ch: i }, aux: lines.map(function (l, k) { return { label: "row " + k, text: l || "·" }; }) });
        if (r === 0) step = 1; else if (r === R - 1) step = -1;
        r += step;
      }
      var out = lines.join("");
      t.snap(7, "Read the rows top to bottom: " + out + ".", { aux: aux("answer", out) });
      return { trace: t, answer: out };
    }
  };

  /* ================================ LINKED LIST: fixed gap ================================ */
  G["ll-gap"] = {
    input: [{ id: "a", label: "list", type: "ints", def: "1 2 3 4 5" }, { id: "n", label: "remove n-th from the end", type: "int", def: 2 }],
    check: function (v) { if (v.n < 1 || v.n > v.a.length) return "n must be between 1 and the list length"; if (v.a.length > 12) return "keep the list to 12 nodes"; },
    gen: function (rnd) { var n = ri(rnd, 1, 8); return { a: ints(rnd, n, 1, 9), n: ri(rnd, 1, n) }; },
    brute: function (v) { var r = v.a.slice(); r.splice(v.a.length - v.n, 1); return r.length ? J(r) : "empty"; },
    run: function (v) {
      var a = v.a, n = v.n, L = a.length;
      var t = A(a, ["dummy = ListNode(0, head); fast = slow = dummy", "for _ in range(n): fast = fast.next        # open a gap of n", "while fast.next:",
                    "    fast, slow = fast.next, slow.next", "slow.next = slow.next.next               # slow sits just BEFORE the target"],
                "remove the " + n + "-th node from the end in ONE pass");
      function P(f, s) { var p = {}; if (f >= 0) p.fast = f; if (s >= 0) p.slow = s; return p; }
      var f = -1, s = -1;
      t.snap(0, "Both pointers start on a dummy node in front of the list.", {});
      for (var i = 0; i < n; i++) f++;
      t.snap(1, "fast walks " + n + " steps ahead. The gap between fast and slow is now " + n + " and never changes.", { ptr: P(f, s) });
      while (f + 1 < L) {
        f++; s++;
        t.snap(3, "move both: fast is " + (L - 1 - f) + " node(s) from the end.", { ptr: P(f, s), span: s >= 0 ? [s, f] : [0, f] });
      }
      var kill = s + 1, out = a.slice();
      out.splice(kill, 1);
      var m = {}; m[kill] = "gone";
      t.snap(4, "fast is on the last node, so slow is just before the target. Unlink a[" + kill + "]=" + a[kill] + ".", { ptr: P(f, s), mark: m });
      return { trace: t, answer: out.length ? J(out) : "empty" };
    }
  };

  /* ================================ LINKED LIST: set of nodes ================================ */
  G["ll-hash"] = {
    input: [{ id: "a", label: "list A (node ids)", type: "ints", def: "1 2 8 4 5" }, { id: "b", label: "list B (node ids)", type: "ints", def: "6 7 4 5" }],
    check: function (v) { if (v.a.length + v.b.length > 14) return "keep both lists to 14 nodes in total"; },
    gen: function (rnd) { return { a: ints(rnd, ri(rnd, 1, 5), 1, 9), b: ints(rnd, ri(rnd, 1, 5), 1, 9) }; },
    brute: function (v) { for (var i = 0; i < v.b.length; i++) if (v.a.indexOf(v.b[i]) >= 0) return v.b[i]; return "none"; },
    run: function (v) {
      var a = v.a, b = v.b, seen = {}, m = {}, i;
      var t = A(a.concat(b), ["seen = set()", "for node in headA: seen.add(node)         # remember every node of A", "for node in headB:",
                              "    if node in seen: return node           # first node of B that A already has", "return None"],
                "intersection of two lists with a set of nodes (same id = same node)");
      for (i = 0; i < a.length; i++) { seen[a[i]] = 1; m[i] = "done"; }
      t.snap(1, "Pass 1: put every node of list A in a set. The set answers 'have I seen this node?' in O(1).", { mark: Object.assign({}, m), span: [0, a.length - 1] });
      for (i = 0; i < b.length; i++) {
        var at = a.length + i;
        if (seen[b[i]]) {
          m[at] = "pick";
          t.snap(3, "node " + b[i] + " from B is already in the set: that is where the lists meet.", { ptr: { b: at }, mark: Object.assign({}, m), aux: aux("answer", b[i]) });
          return { trace: t, answer: b[i] };
        }
        m[at] = "gone";
        t.snap(2, "node " + b[i] + " from B is not in the set. Keep walking.", { ptr: { b: at }, mark: Object.assign({}, m) });
      }
      t.snap(4, "Walked all of B without a hit: the lists never meet.", { mark: Object.assign({}, m), aux: aux("answer", "none") });
      return { trace: t, answer: "none" };
    }
  };

  /* ================================ DP: state machine ================================ */
  G["dp-state"] = {
    input: [{ id: "p", label: "prices", type: "ints", def: "1 2 3 0 2" }],
    check: function (v) { if (v.p.length > 12) return "keep it to 12 days"; for (var i = 0; i < v.p.length; i++) if (v.p[i] < 0) return "prices cannot be negative"; },
    gen: function (rnd) { return { p: ints(rnd, ri(rnd, 1, 9), 0, 9) }; },
    brute: function (v) {
      var memo = {}, p = v.p;
      function go(i, hold, cool) {          // best profit from day i on
        if (i >= p.length) return 0;
        var key = i + "," + hold + "," + cool;
        if (key in memo) return memo[key];
        var best = go(i + 1, hold, 0);
        if (hold) best = Math.max(best, p[i] + go(i + 1, 0, 1));
        else if (!cool) best = Math.max(best, -p[i] + go(i + 1, 1, 0));
        return (memo[key] = best);
      }
      return go(0, 0, 0);
    },
    run: function (v) {
      var p = v.p, hold = -1e9, sold = 0, rest = 0;
      var t = A(p, ["hold, sold, rest = -inf, 0, 0", "for price in prices:", "    hold, sold, rest = (max(hold, rest - price),   # keep, or buy (only from rest)",
                    "                        hold + price,           # sell what we hold", "                        max(rest, sold))        # idle, or cool down after a sale", "return max(sold, rest)"],
                "stock with a one-day cooldown: three states updated together");
      for (var i = 0; i < p.length; i++) {
        var nh = Math.max(hold, rest - p[i]), ns = hold + p[i], nr = Math.max(rest, sold);
        hold = nh; sold = ns; rest = nr;
        t.snap(2, "day " + i + " (price " + p[i] + "): holding " + (hold < -1e8 ? "−∞" : hold) + ", just sold " + (sold < -1e8 ? "−∞" : sold) + ", resting " + rest + ". All three come from YESTERDAY's values.",
               { ptr: { day: i }, aux: aux("hold", hold < -1e8 ? "−∞" : hold, "sold", sold < -1e8 ? "−∞" : sold, "rest", rest) });
      }
      var ans = Math.max(sold, rest);
      t.snap(5, "Answer " + ans + " = max(sold, rest). Ending while still holding is never better.", { aux: aux("answer", ans) });
      return { trace: t, answer: ans };
    }
  };

  /* ================================ DP: cut into pieces (word break) ================================ */
  G["dp-partition"] = {
    input: [{ id: "s", label: "string", type: "string", def: "leetcode" }, { id: "words", label: "dictionary", type: "words", def: "leet code" }],
    check: function (v) { if (!v.s.length || v.s.length > 14) return "1 to 14 characters"; if (v.words.length > 6) return "at most 6 words"; },
    gen: function (rnd) {
      var w = [], n = ri(rnd, 1, 4); for (var i = 0; i < n; i++) w.push(str(rnd, ri(rnd, 1, 3), "ab"));
      var s = ""; var k = ri(rnd, 1, 4); for (i = 0; i < k; i++) s += rnd(4) ? w[rnd(n)] : str(rnd, ri(rnd, 1, 2), "ab");
      return { s: s, words: w };
    },
    brute: function (v) {
      var set = v.words;
      function go(rest) { if (!rest.length) return true; for (var i = 0; i < set.length; i++) if (rest.indexOf(set[i]) === 0 && go(rest.slice(set[i].length))) return true; return false; }
      return go(v.s);
    },
    run: function (v) {
      var s = v.s, n = s.length, W = v.words, dp = [true], m = {};
      for (var q = 1; q <= n; q++) dp.push(false);
      var t = A(s.split(""), ["dp = [True] + [False] * len(s)        # dp[i]: can the first i characters be cut into words?", "for i in range(1, len(s) + 1):",
                              "    for j in range(i):", "        if dp[j] and s[j:i] in words:", "            dp[i] = True; break", "return dp[-1]"],
                "word break: dp[i] = some earlier cut j works and s[j:i] is a word");
      for (var i = 1; i <= n; i++) {
        var found = -1;
        for (var j = 0; j < i; j++) if (dp[j] && W.indexOf(s.slice(j, i)) >= 0) { found = j; break; }
        if (found >= 0) {
          dp[i] = true; m[i - 1] = "done";
          t.snap(4, "prefix of length " + i + ": cut at " + found + " (prefix " + found + " works) and '" + s.slice(found, i) + "' is a word, so dp[" + i + "] = True.",
                 { ptr: { i: i - 1 }, span: [found, i - 1], mark: Object.assign({}, m) });
        } else {
          t.snap(2, "prefix of length " + i + ": no cut j with dp[j] true leaves a dictionary word. dp[" + i + "] stays False.", { ptr: { i: i - 1 }, mark: Object.assign({}, m) });
        }
      }
      t.snap(5, "Answer " + dp[n] + ": the whole string " + (dp[n] ? "can" : "cannot") + " be cut into dictionary words.", { mark: Object.assign({}, m), aux: aux("answer", dp[n]) });
      return { trace: t, answer: dp[n] };
    }
  };

  /* ================================ BACKTRACKING: partitions ================================ */
  G["bk-partition"] = {
    input: [{ id: "s", label: "string", type: "string", def: "aab" }],
    check: function (v) { if (!v.s.length || v.s.length > 7) return "1 to 7 characters"; },
    gen: function (rnd) { return { s: str(rnd, ri(rnd, 1, 6), "ab") }; },
    brute: function (v) {
      var s = v.s, n = s.length, pal = function (x) { return x === x.split("").reverse().join(""); }, f = [1], i, j;
      for (i = 1; i <= n; i++) { f[i] = 0; for (j = 0; j < i; j++) if (pal(s.slice(j, i))) f[i] += f[j]; }
      return f[n];
    },
    run: function (v) {
      var s = v.s, n = s.length, cur = [], out = [];
      var t = A(s.split(""), ["def go(start):", "    if start == len(s): out.append(cur[:]); return", "    for end in range(start + 1, len(s) + 1):",
                              "        piece = s[start:end]", "        if piece == piece[::-1]:", "            cur.append(piece); go(end); cur.pop()"], "every way to cut '" + s + "' into palindromes");
      function go(start) {
        if (start === n) { out.push(cur.join("|")); t.snap(1, "reached the end: record the cut  " + cur.join(" | ") + ".  (" + out.length + " so far)", { aux: aux("found", out.length) }); return; }
        for (var e = start + 1; e <= n; e++) {
          var piece = s.slice(start, e), ok = piece === piece.split("").reverse().join("");
          t.snap(4, "try '" + piece + "' — " + (ok ? "a palindrome, so keep it and cut the rest." : "not a palindrome, skip."), { span: [start, e - 1], aux: aux("cut so far", cur.join(" | ") || "—", "found", out.length) });
          if (ok) { cur.push(piece); go(e); cur.pop(); }
        }
      }
      go(0);
      t.snap(1, "Answer: " + out.length + " ways. Backtracking lists every one; if only the COUNT were asked, a DP would do it faster.", { aux: aux("ways", out.length) });
      return { trace: t, answer: out.length };
    }
  };

  /* ================================ BACKTRACKING: build a string ================================ */
  G["bk-build"] = {
    input: [{ id: "n", label: "pairs n", type: "int", def: 3 }],
    check: function (v) { if (v.n < 1 || v.n > 3) return "n between 1 and 3 keeps the trace watchable"; },
    gen: function (rnd) { return { n: ri(rnd, 1, 3) }; },
    brute: function (v) { var c = 1, n = v.n; for (var i = 0; i < n; i++) c = c * 2 * (2 * i + 1) / (i + 2); return Math.round(c); },
    run: function (v) {
      var n = v.n, out = 0;
      var t = A(rng(0, 2 * n - 1), ["def go(cur, opens, closes):", "    if len(cur) == 2 * n: out.append(cur); return", "    if opens < n:   go(cur + '(', opens + 1, closes)",
                                    "    if closes < opens: go(cur + ')', opens, closes + 1)"], "valid parentheses with " + n + " pairs, one character at a time");
      function mk(len) { var m = {}; for (var i = 0; i < len; i++) m[i] = "done"; return m; }
      function go(cur, o, c) {
        if (cur.length === 2 * n) { out++; t.snap(1, "complete: " + cur + "  (" + out + " found)", { mark: mk(cur.length), aux: aux("built", cur, "found", out) }); return; }
        if (o < n) { t.snap(2, "opens used " + o + " < " + n + ": add '('.", { ptr: { next: cur.length }, mark: mk(cur.length), aux: aux("built", cur + "(") }); go(cur + "(", o + 1, c); }
        if (c < o) { t.snap(3, "closes " + c + " < opens " + o + ": adding ')' is still valid.", { ptr: { next: cur.length }, mark: mk(cur.length), aux: aux("built", cur + ")") }); go(cur + ")", o, c + 1); }
      }
      go("", 0, 0);
      t.snap(1, "Answer: " + out + " valid strings. Pruning at each step meant no invalid string was ever built.", { aux: aux("found", out) });
      return { trace: t, answer: out };
    }
  };

  /* ================================ BACKTRACKING: k buckets ================================ */
  G["bk-bucket"] = {
    input: [{ id: "a", label: "numbers", type: "ints", def: "4 3 2 3 5 2 1" }, { id: "k", label: "groups k", type: "int", def: 4 }],
    check: function (v) { if (v.a.length > 6 || v.a.length < 1) return "1 to 6 numbers"; if (v.k < 1 || v.k > 3) return "k between 1 and 3"; for (var i = 0; i < v.a.length; i++) if (v.a[i] < 1) return "positive numbers only"; },
    gen: function (rnd) { return { a: ints(rnd, ri(rnd, 1, 6), 1, 5), k: ri(rnd, 1, 3) }; },
    brute: function (v) {
      var n = v.a.length, k = v.k, total = v.a.reduce(function (s, x) { return s + x; }, 0);
      var asg = [];
      function all(i) {
        if (i === n) { var sums = []; for (var b = 0; b < k; b++) sums.push(0); for (var j = 0; j < n; j++) sums[asg[j]] += v.a[j]; return sums.every(function (x) { return x * k === total; }); }
        for (var b2 = 0; b2 < k; b2++) { asg[i] = b2; if (all(i + 1)) return true; }
        return false;
      }
      return all(0);
    },
    run: function (v) {
      var nums = v.a.slice().sort(function (p, q) { return q - p; }), k = v.k, n = nums.length, total = nums.reduce(function (s, x) { return s + x; }, 0), frames = 0;
      var t = A(nums, ["if sum(nums) % k: return False", "target = sum(nums) // k; nums.sort(reverse=True)", "def go(i):", "    if i == len(nums): return True",
                       "    for b in range(k):", "        if buckets[b] + nums[i] <= target:", "            buckets[b] += nums[i]", "            if go(i + 1): return True", "            buckets[b] -= nums[i]",
                       "        if buckets[b] == 0: break          # empty buckets are all the same"], "split into " + k + " groups of equal sum");
      if (total % k) { t.snap(0, "The total " + total + " is not divisible by " + k + ", so equal groups are impossible.", { aux: aux("total", total) }); return { trace: t, answer: false }; }
      var target = total / k, bk = []; for (var b = 0; b < k; b++) bk.push(0);
      t.snap(1, "each group must sum to " + target + ". Sort descending: big items fail fastest.", { aux: aux("target", target, "groups", "[" + bk.join(",") + "]") });
      var ok = (function go(i) {
        if (i === n) return true;
        for (var b2 = 0; b2 < k; b2++) {
          if (bk[b2] + nums[i] <= target) {
            bk[b2] += nums[i];
            if (frames++ < 400) t.snap(6, "put " + nums[i] + " in group " + b2 + ".", { ptr: { item: i }, aux: aux("target", target, "groups", "[" + bk.join(",") + "]") });
            if (go(i + 1)) return true;
            bk[b2] -= nums[i];
            if (frames++ < 400) t.snap(8, "dead end below — take " + nums[i] + " back out of group " + b2 + ".", { ptr: { item: i }, aux: aux("target", target, "groups", "[" + bk.join(",") + "]") });
          }
          if (bk[b2] === 0) break;
        }
        return false;
      })(0);
      t.snap(1, "Answer " + ok + ".", { aux: aux("answer", ok) });
      return { trace: t, answer: ok };
    }
  };

  /* ================================ GREEDY: left pass, right pass ================================ */
  G["gr-twopass"] = {
    input: [{ id: "r", label: "ratings", type: "ints", def: "1 0 2" }],
    check: function (v) { if (v.r.length > 12) return "keep it to 12 children"; },
    gen: function (rnd) { return { r: ints(rnd, ri(rnd, 1, 9), 1, 5) }; },
    brute: function (v) {
      var n = v.r.length, c = [], i, ch = true; for (i = 0; i < n; i++) c.push(1);
      while (ch) {
        ch = false;
        for (i = 0; i < n; i++) {
          if (i > 0 && v.r[i] > v.r[i - 1] && c[i] <= c[i - 1]) { c[i] = c[i - 1] + 1; ch = true; }
          if (i < n - 1 && v.r[i] > v.r[i + 1] && c[i] <= c[i + 1]) { c[i] = c[i + 1] + 1; ch = true; }
        }
      }
      return c.reduce(function (s, x) { return s + x; }, 0);
    },
    run: function (v) {
      var r = v.r, n = r.length, c = [], i;
      for (i = 0; i < n; i++) c.push(1);
      var t = A(r, ["c = [1] * n", "for i in range(1, n):            # left rule", "    if r[i] > r[i-1]: c[i] = c[i-1] + 1", "for i in range(n-2, -1, -1):  # right rule",
                    "    if r[i] > r[i+1]: c[i] = max(c[i], c[i+1] + 1)", "return sum(c)"], "fewest candies so a higher rating than a neighbour gets more");
      t.snap(0, "everyone starts with 1 candy.", { aux: aux("candies", "[" + c.join(",") + "]") });
      for (i = 1; i < n; i++) if (r[i] > r[i - 1]) { c[i] = c[i - 1] + 1; t.snap(2, "left pass: r[" + i + "]=" + r[i] + " > its left neighbour, so c[" + i + "] = " + c[i] + ".", { ptr: { i: i }, aux: aux("candies", "[" + c.join(",") + "]") }); }
      for (i = n - 2; i >= 0; i--) if (r[i] > r[i + 1]) {
        c[i] = Math.max(c[i], c[i + 1] + 1);
        t.snap(4, "right pass: r[" + i + "]=" + r[i] + " > its right neighbour, so c[" + i + "] = max(old, " + (c[i + 1] + 1) + ") = " + c[i] + ". The max keeps what the left pass set.", { ptr: { i: i }, aux: aux("candies", "[" + c.join(",") + "]") });
      }
      var s = c.reduce(function (a, b) { return a + b; }, 0);
      t.snap(5, "Answer " + s + " candies.", { aux: aux("candies", "[" + c.join(",") + "]", "total", s) });
      return { trace: t, answer: s };
    }
  };

  /* ================================ GREEDY: running balance (gas station) ================================ */
  G["gr-balance"] = {
    input: [{ id: "gas", label: "gas at each station", type: "ints", def: "1 2 3 4 5" }, { id: "cost", label: "cost to the next", type: "ints", def: "3 4 5 1 2" }],
    check: function (v) { if (v.gas.length !== v.cost.length) return "gas and cost need the same length"; if (v.gas.length > 12) return "keep it to 12 stations"; },
    gen: function (rnd) { var n = ri(rnd, 1, 7); return { gas: ints(rnd, n, 0, 6), cost: ints(rnd, n, 0, 6) }; },
    brute: function (v) {
      var n = v.gas.length;
      for (var s = 0; s < n; s++) { var tank = 0, ok = true; for (var k = 0; k < n; k++) { var i = (s + k) % n; tank += v.gas[i] - v.cost[i]; if (tank < 0) { ok = false; break; } } if (ok) return s; }
      return -1;
    },
    run: function (v) {
      var g = v.gas, c = v.cost, n = g.length, tg = 0, tc = 0, i;
      for (i = 0; i < n; i++) { tg += g[i]; tc += c[i]; }
      var t = A(g, ["if sum(gas) < sum(cost): return -1", "start, tank = 0, 0", "for i in range(n):", "    tank += gas[i] - cost[i]", "    if tank < 0: start, tank = i + 1, 0", "return start"],
                "gas station: where can the loop start?");
      if (tg < tc) { t.snap(0, "Total gas " + tg + " is less than total cost " + tc + ": no starting point can work.", { aux: aux("gas", tg, "cost", tc) }); return { trace: t, answer: -1 }; }
      var start = 0, tank = 0;
      for (i = 0; i < n; i++) {
        tank += g[i] - c[i];
        if (tank < 0) { start = i + 1; tank = 0; t.snap(4, "tank would go negative at station " + i + ", so no start up to " + i + " can work. Restart from " + (i + 1) + " with an empty tank.", { ptr: { i: i, start: Math.min(start, n - 1) }, aux: aux("tank", 0, "start", start) }); }
        else t.snap(3, "station " + i + ": +" + g[i] + " −" + c[i] + ", tank " + tank + ".", { ptr: { i: i, start: start }, aux: aux("tank", tank, "start", start) });
      }
      t.snap(5, "Total gas covers total cost, so the last restart point works: station " + start + ".", { ptr: { start: Math.min(start, n - 1) }, aux: aux("answer", start) });
      return { trace: t, answer: start };
    }
  };

  /* ================================ DIVIDE & CONQUER ================================ */
  G["dc-mergecount"] = {
    input: [{ id: "a", label: "array", type: "ints", def: "2 4 1 3 5" }],
    check: function (v) { if (v.a.length > 10) return "keep it to 10 elements"; },
    gen: function (rnd) { return { a: ints(rnd, ri(rnd, 1, 9), 0, 9) }; },
    brute: function (v) { var s = 0; for (var i = 0; i < v.a.length; i++) for (var j = i + 1; j < v.a.length; j++) if (v.a[i] > v.a[j]) s++; return s; },
    run: function (v) {
      var a = v.a.slice(), orig = v.a.slice();
      var t = A(orig, ["def sort(lo, hi):", "    if hi - lo < 2: return 0", "    count = sort(lo, mid) + sort(mid, hi)", "    while merging:", "        if left <= right: take left",
                       "        else: count += mid - i; take right   # every remaining left value is bigger", "    return count"], "count inversions while merge-sorting");
      var total = 0;
      function sort(lo, hi) {
        if (hi - lo < 2) return 0;
        var mid = (lo + hi) >> 1, cnt = sort(lo, mid) + sort(mid, hi), merged = [], i = lo, j = mid, here = 0;
        while (i < mid || j < hi) {
          if (j === hi || (i < mid && a[i] <= a[j])) merged.push(a[i++]);
          else { here += mid - i; merged.push(a[j++]); }
        }
        for (var k = 0; k < merged.length; k++) a[lo + k] = merged[k];
        total += here;
        t.snap(5, "merged [" + lo + ".." + (hi - 1) + "] into " + merged.join(" ") + ". Pairs that crossed over in this merge: " + here + ".", { span: [lo, hi - 1], aux: aux("this merge", here, "total", total) });
        return cnt + here;
      }
      var ans = sort(0, a.length);
      t.snap(6, "Answer " + ans + " inversions in O(n log n), without comparing every pair.", { aux: aux("inversions", ans) });
      return { trace: t, answer: ans };
    }
  };

  G["dc-quickselect"] = {
    input: [{ id: "a", label: "array", type: "ints", def: "3 2 1 5 6 4" }, { id: "k", label: "k-th largest", type: "int", def: 2 }],
    check: function (v) { if (v.k < 1 || v.k > v.a.length) return "k between 1 and the array length"; if (v.a.length > 12) return "keep it to 12 elements"; },
    gen: function (rnd) { var n = ri(rnd, 1, 9); return { a: ints(rnd, n, 0, 9), k: ri(rnd, 1, n) }; },
    brute: function (v) { return v.a.slice().sort(function (p, q) { return q - p; })[v.k - 1]; },
    run: function (v) {
      var a = v.a.slice(), target = a.length - v.k, lo = 0, hi = a.length - 1;
      var t = A(v.a.slice(), ["target = len(a) - k            # its place in sorted order", "while True:", "    partition a[lo..hi] around the pivot a[hi]", "    if pivot lands on target: return it",
                              "    lo = store + 1  or  hi = store - 1       # keep only the side holding target"], "k-th largest without sorting everything");
      while (true) {
        var piv = a[hi], store = lo, i;
        for (i = lo; i < hi; i++) if (a[i] < piv) { var tmp = a[i]; a[i] = a[store]; a[store] = tmp; store++; }
        tmp = a[store]; a[store] = a[hi]; a[hi] = tmp;
        t.snap(2, "partition [" + lo + ".." + hi + "] around pivot " + piv + ": it lands at position " + store + ". Target position is " + target + ".",
               { span: [lo, hi], aux: aux("array now", a.join(" "), "pivot at", store, "target", target) });
        if (store === target) { t.snap(3, "pivot is exactly at the target position: the answer is " + a[store] + ".", { aux: aux("answer", a[store]) }); return { trace: t, answer: a[store] }; }
        if (store < target) lo = store + 1; else hi = store - 1;
        t.snap(4, "target is on the " + (store < target ? "right" : "left") + " side, so discard the other side entirely. That is why the average cost is O(n).", { span: [lo, hi], aux: aux("array now", a.join(" ")) });
      }
    }
  };

  G["dc-bucket"] = {
    input: [{ id: "a", label: "numbers (1 to 9)", type: "ints", def: "1 1 1 2 2 3" }, { id: "k", label: "top k", type: "int", def: 2 }],
    check: function (v) { if (v.a.length > 14) return "keep it to 14 numbers"; for (var i = 0; i < v.a.length; i++) if (v.a[i] < 1 || v.a[i] > 9) return "use numbers from 1 to 9"; },
    gen: function (rnd) { return { a: ints(rnd, ri(rnd, 1, 10), 1, 6), k: ri(rnd, 1, 3) }; },
    brute: function (v) {
      var c = {}; v.a.forEach(function (x) { c[x] = (c[x] || 0) + 1; });
      var e = Object.keys(c).map(Number).sort(function (p, q) { return (c[q] - c[p]) || (p - q); });
      return J(e.slice(0, v.k));
    },
    run: function (v) {
      var a = v.a, n = a.length, freq = {}, i;
      for (i = 0; i < n; i++) freq[a[i]] = (freq[a[i]] || 0) + 1;
      var t = A(a, ["count = Counter(nums)", "buckets = [[] for _ in range(n + 1)]       # index = frequency", "for x, c in count.items(): buckets[c].append(x)",
                    "for c in range(n, 0, -1):          # most frequent bucket first", "    out += buckets[c]; stop once k are collected"], "top k frequent in O(n): the frequency itself is the bucket index");
      var m = {}; for (i = 0; i < n; i++) m[i] = "done";
      t.snap(0, "counts: " + Object.keys(freq).map(function (x) { return x + "×" + freq[x]; }).join(", ") + ".", { mark: m, aux: aux("max possible frequency", n) });
      var buckets = []; for (i = 0; i <= n; i++) buckets.push([]);
      Object.keys(freq).map(Number).sort(function (p, q) { return p - q; }).forEach(function (x) { buckets[freq[x]].push(x); });
      var out = [];
      for (var c = n; c >= 1 && out.length < v.k; c--) {
        if (!buckets[c].length) continue;
        out = out.concat(buckets[c]);
        t.snap(4, "bucket " + c + " holds " + buckets[c].join(" ") + " (they occur " + c + " times). Collected so far: " + out.join(" ") + ".", { aux: aux("frequency bucket", c, "collected", out.join(" ")) });
      }
      out = out.slice(0, v.k);
      t.snap(4, "Answer: " + out.join(", ") + ". No sorting at all: just a pass over counts.", { aux: aux("answer", out.join(",")) });
      return { trace: t, answer: J(out) };
    }
  };

  G["dc-split"] = {
    input: [{ id: "e", label: "expression (single digits)", type: "string", def: "2-1-1" }],
    check: function (v) { if (!/^\d([+\-*]\d){0,3}$/.test(v.e)) return "write single digits and + - * only, like 2-1-1 (at most 4 numbers)"; },
    gen: function (rnd) { var n = ri(rnd, 1, 4), s = "" + rnd(10); for (var i = 1; i < n; i++) s += "+-*".charAt(rnd(3)) + rnd(10); return { e: s }; },
    brute: function (v) {
      var tok = v.e.match(/\d|[+\-*]/g), nums = [], ops = [];
      tok.forEach(function (x, i) { if (i % 2 === 0) nums.push(Number(x)); else ops.push(x); });
      var n = nums.length, dp = [], i, len, k;
      for (i = 0; i < n; i++) { dp.push([]); for (var j = 0; j < n; j++) dp[i].push([]); dp[i][i] = [nums[i]]; }
      for (len = 2; len <= n; len++) for (i = 0; i + len - 1 < n; i++) {
        var j2 = i + len - 1, res = [];
        for (k = i; k < j2; k++) dp[i][k].forEach(function (x) { dp[k + 1][j2].forEach(function (y) { res.push(ops[k] === "+" ? x + y : ops[k] === "-" ? x - y : x * y); }); });
        dp[i][j2] = res;
      }
      return J(dp[0][n - 1].slice().sort(function (p, q) { return p - q; }));
    },
    run: function (v) {
      var e = v.e, memoOut = [];
      var t = A(e, ["def ways(expr):", "    if expr.isdigit(): return [int(expr)]", "    for each operator at position i:", "        for a in ways(left): for b in ways(right): out.append(a op b)"],
                "every result of putting parentheses in the expression", "string");
      function ways(lo, hi) {
        var s = e.slice(lo, hi + 1);
        if (/^\d$/.test(s)) { t.snap(1, "'" + s + "' is a single number: the only result is " + s + ".", { span: [lo, hi] }); return [Number(s)]; }
        var out = [];
        for (var i = lo + 1; i < hi; i += 2) {
          t.snap(2, "split '" + s + "' at the operator '" + e[i] + "': solve the left half and the right half independently.", { span: [lo, hi], ptr: { op: i } });
          var L = ways(lo, i - 1), R = ways(i + 1, hi);
          L.forEach(function (x) { R.forEach(function (y) { out.push(e[i] === "+" ? x + y : e[i] === "-" ? x - y : x * y); }); });
        }
        t.snap(3, "'" + s + "' can give: " + out.slice().sort(function (p, q) { return p - q; }).join(", ") + ".", { span: [lo, hi] });
        return out;
      }
      var res = ways(0, e.length - 1).sort(function (p, q) { return p - q; });
      t.snap(3, "Answer: " + res.join(", ") + ".", { aux: aux("results", res.join(", ")) });
      return { trace: t, answer: J(res) };
    }
  };

  /* ================================ MATHS ================================ */
  G["ma-gcd"] = {
    input: [{ id: "a", label: "numbers", type: "ints", def: "12 18 30" }],
    check: function (v) { if (v.a.length < 1 || v.a.length > 8) return "1 to 8 numbers"; for (var i = 0; i < v.a.length; i++) if (v.a[i] < 1) return "positive numbers only"; },
    gen: function (rnd) { return { a: ints(rnd, ri(rnd, 1, 5), 1, 40) }; },
    brute: function (v) { var m = Math.min.apply(null, v.a); for (var d = m; d >= 1; d--) if (v.a.every(function (x) { return x % d === 0; })) return d; },
    run: function (v) {
      var a = v.a, g = a[0];
      var t = A(a, ["def gcd(a, b):", "    while b: a, b = b, a % b", "    return a", "g = nums[0]", "for x in nums[1:]: g = gcd(g, x)    # fold from the left"], "GCD of the whole array, one Euclid at a time");
      t.snap(3, "start with g = " + g + ".", { ptr: { g: 0 }, aux: aux("g", g) });
      for (var i = 1; i < a.length; i++) {
        var x = g, y = a[i], steps = [];
        while (y) { steps.push(x + " mod " + y + " = " + (x % y)); var tm = x % y; x = y; y = tm; }
        g = x;
        t.snap(4, "gcd(" + (x === g && steps.length ? "…" : g) + ", " + a[i] + "): " + (steps.join("; ") || "already divides") + ". New g = " + g + ". The answer can only shrink.", { ptr: { x: i }, aux: aux("g", g) });
      }
      t.snap(4, "Answer " + g + ".", { aux: aux("gcd", g) });
      return { trace: t, answer: g };
    }
  };

  G["ma-sieve"] = {
    input: [{ id: "n", label: "count primes up to n", type: "int", def: 30 }],
    check: function (v) { if (v.n < 2 || v.n > 50) return "n between 2 and 50"; },
    gen: function (rnd) { return { n: ri(rnd, 2, 50) }; },
    brute: function (v) { var c = 0; for (var x = 2; x <= v.n; x++) { var p = true; for (var d = 2; d * d <= x; d++) if (x % d === 0) { p = false; break; } if (p) c++; } return c; },
    run: function (v) {
      var n = v.n, comp = {}, m = {};
      var t = A(rng(0, n), ["is_prime = [True] * (n + 1)", "i = 2", "while i * i <= n:", "    if is_prime[i]:", "        for m in range(i * i, n + 1, i): is_prime[m] = False",
                            "    i += 1", "return count of True from 2"], "sieve of Eratosthenes up to " + n);
      m[0] = "gone"; m[1] = "gone";
      t.snap(0, "0 and 1 are not prime. Everything else starts as a candidate.", { mark: Object.assign({}, m) });
      for (var i = 2; i * i <= n; i++) {
        if (comp[i]) continue;
        for (var k = i * i; k <= n; k += i) { comp[k] = 1; m[k] = "gone"; }
        t.snap(4, i + " is prime: cross out its multiples starting at " + i + "×" + i + " = " + i * i + " (smaller ones were crossed by smaller primes).", { ptr: { p: i }, mark: Object.assign({}, m) });
      }
      var cnt = 0;
      for (var x = 2; x <= n; x++) if (!comp[x]) { cnt++; m[x] = "done"; }
      t.snap(6, "Everything left standing is prime: " + cnt + " primes up to " + n + ". You only needed to sieve up to √n = " + Math.floor(Math.sqrt(n)) + ".", { mark: Object.assign({}, m), aux: aux("primes", cnt) });
      return { trace: t, answer: cnt };
    }
  };

  G["ma-modpow"] = {
    input: [{ id: "b", label: "base", type: "int", def: 3 }, { id: "e", label: "exponent", type: "int", def: 13 }, { id: "m", label: "modulo", type: "int", def: 1000 }],
    check: function (v) { if (v.e < 1 || v.e > 60) return "exponent between 1 and 60"; if (v.m < 2 || v.m > 1000) return "modulo between 2 and 1000"; if (v.b < 0) return "base cannot be negative"; },
    gen: function (rnd) { return { b: ri(rnd, 0, 20), e: ri(rnd, 1, 40), m: ri(rnd, 2, 100) }; },
    brute: function (v) { var r = 1 % v.m; for (var i = 0; i < v.e; i++) r = (r * v.b) % v.m; return r; },
    run: function (v) {
      var bits = [], e = v.e; while (e) { bits.push(e & 1); e >>= 1; }
      var t = A(bits, ["result, base = 1, base % mod", "while n:", "    if n & 1: result = result * base % mod       # this bit of the exponent is set", "    base = base * base % mod                      # base^1, ^2, ^4, ^8 ...",
                       "    n >>= 1"], v.b + "^" + v.e + " mod " + v.m + ": read the exponent in binary (lowest bit first)");
      var res = 1 % v.m, base = v.b % v.m, m = {};
      for (var i = 0; i < bits.length; i++) {
        var used = bits[i] === 1;
        if (used) res = (res * base) % v.m;
        m[i] = used ? "pick" : "gone";
        t.snap(used ? 2 : 3, "bit " + i + " = " + bits[i] + (used ? ": multiply the result by base^(2^" + i + ") = " + base + "." : ": skip.") + " Result so far " + res + ".",
               { ptr: { bit: i }, mark: Object.assign({}, m), aux: aux("base", base, "result", res) });
        base = (base * base) % v.m;
      }
      t.snap(4, "Answer " + res + " after only " + bits.length + " squarings instead of " + v.e + " multiplications.", { aux: aux("answer", res) });
      return { trace: t, answer: res };
    }
  };

  G["ma-ncr"] = {
    input: [{ id: "n", label: "n", type: "int", def: 10 }, { id: "r", label: "r", type: "int", def: 3 }],
    check: function (v) { if (v.n < 0 || v.n > 12) return "n between 0 and 12"; if (v.r < 0 || v.r > v.n) return "r between 0 and n"; },
    gen: function (rnd) { var n = ri(rnd, 0, 12); return { n: n, r: ri(rnd, 0, n) }; },
    brute: function (v) {
      var row = [1];
      for (var i = 1; i <= v.n; i++) { var nx = [1]; for (var j = 1; j < i; j++) nx.push(row[j - 1] + row[j]); nx.push(1); row = nx; }
      return row[v.r];
    },
    run: function (v) {
      var n = v.n, r = v.r, f = [1], i;
      for (i = 1; i <= n; i++) f.push(f[i - 1] * i);
      var t = A(rng(0, n), ["fact = [1] * (n + 1)", "for i in range(1, n + 1): fact[i] = fact[i-1] * i", "nCr = fact[n] / (fact[r] * fact[n - r])"], "C(" + n + ", " + r + ") from factorials");
      var m = {};
      for (i = 0; i <= n; i++) { m[i] = "done"; if (i % 3 === 0 || i === n) t.snap(1, i + "! = " + f[i] + ".", { ptr: { i: i }, mark: Object.assign({}, m) }); }
      var ans = f[n] / (f[r] * f[n - r]);
      t.snap(2, "C(" + n + "," + r + ") = " + f[n] + " / (" + f[r] + " × " + f[n - r] + ") = " + ans + ". Under a modulus you would multiply by modular inverses instead of dividing.", { ptr: { r: r }, aux: aux("answer", ans) });
      return { trace: t, answer: ans };
    }
  };

  G["ma-digits"] = {
    input: [{ id: "a", label: "first number", type: "digits", def: "9987" }, { id: "b", label: "second number", type: "digits", def: "245" }],
    check: function (v) { if (v.a.length > 8 || v.b.length > 8) return "up to 8 digits each"; },
    gen: function (rnd) { return { a: str(rnd, ri(rnd, 1, 6), "0123456789"), b: str(rnd, ri(rnd, 1, 6), "0123456789") }; },
    brute: function (v) { return (BigInt(v.a) + BigInt(v.b)).toString(); },
    run: function (v) {
      var L = Math.max(v.a.length, v.b.length) , a = v.a, b = v.b;
      while (a.length < L) a = "0" + a;
      while (b.length < L) b = "0" + b;
      var t = A(a.split("").map(Number), ["i, j, carry, out = len(a)-1, len(b)-1, 0, []", "while i >= 0 or j >= 0 or carry:", "    d = carry + digit of a + digit of b", "    out.append(d % 10)",
                                         "    carry = d // 10", "return reversed digits"], "add two numbers digit by digit, right to left (top row: first number, padded)");
      var carry = 0, out = [], m = {};
      for (var i = L - 1; i >= 0; i--) {
        var d = carry + Number(a[i]) + Number(b[i]);
        out.unshift(d % 10);
        t.snap(3, "column " + i + ": " + Number(a[i]) + " + " + Number(b[i]) + " + carry " + carry + " = " + d + " → write " + d % 10 + ", carry " + Math.floor(d / 10) + ".",
               { ptr: { col: i }, mark: Object.assign({}, m), aux: aux("second number", b, "written", out.join(""), "carry", Math.floor(d / 10)) });
        carry = Math.floor(d / 10); m[i] = "done";
      }
      if (carry) out.unshift(carry);
      var res = out.join("").replace(/^0+(?=\d)/, "");
      t.snap(5, "Answer " + res + (carry ? " (the final carry became a new leading digit)." : "."), { mark: Object.assign({}, m), aux: aux("answer", res) });
      return { trace: t, answer: res };
    }
  };

  G["ma-game"] = {
    input: [{ id: "n", label: "stones n (take 1 to 3)", type: "int", def: 10 }],
    check: function (v) { if (v.n < 1 || v.n > 30) return "n between 1 and 30"; },
    gen: function (rnd) { return { n: ri(rnd, 1, 30) }; },
    brute: function (v) { return v.n % 4 !== 0; },
    run: function (v) {
      var n = v.n, win = [false], m = {};
      var t = A(rng(0, n), ["win[0] = False                         # no stones left on your turn: you lost", "for i in range(1, n + 1):", "    win[i] = any(not win[i - t] for t in (1, 2, 3) if i - t >= 0)",
                            "# a position is winning if some move leaves the opponent in a losing one", "# look at the losing positions: 0, 4, 8, 12 ... — multiples of 4"], "who wins with optimal play: Nim with moves 1, 2 or 3");
      m[0] = "gone";
      t.snap(0, "0 stones on your turn: you cannot move, so you lose.", { mark: Object.assign({}, m) });
      for (var i = 1; i <= n; i++) {
        var w = false;
        for (var k = 1; k <= 3; k++) if (i - k >= 0 && !win[i - k]) w = true;
        win.push(w); m[i] = w ? "done" : "gone";
        t.snap(2, i + " stones: " + (w ? "winning — some move leaves the opponent on a losing count." : "losing — every move leaves the opponent a winning count."), { ptr: { i: i }, mark: Object.assign({}, m) });
      }
      t.snap(4, "Pattern: the losing counts are exactly the multiples of 4. So the answer is simply n % 4 != 0, no table needed. First player " + (win[n] ? "wins" : "loses") + " with n = " + n + ".", { mark: Object.assign({}, m), aux: aux("first player wins", win[n]) });
      return { trace: t, answer: win[n] };
    }
  };

  /* ================================ DESIGN ================================ */
  G["ds-lru"] = {
    input: [{ id: "a", label: "keys accessed in order", type: "ints", def: "1 2 1 3 2 4" }, { id: "cap", label: "capacity", type: "int", def: 2 }],
    check: function (v) { if (v.cap < 1 || v.cap > 5) return "capacity between 1 and 5"; if (v.a.length > 14) return "keep it to 14 accesses"; },
    gen: function (rnd) { return { a: ints(rnd, ri(rnd, 1, 12), 1, 5), cap: ri(rnd, 1, 4) }; },
    brute: function (v) {
      var last = {}, hits = 0;
      v.a.forEach(function (x, t) {
        if (x in last) hits++;
        else if (Object.keys(last).length === v.cap) { var old = Object.keys(last).sort(function (p, q) { return last[p] - last[q]; })[0]; delete last[old]; }
        last[x] = t;
      });
      return hits;
    },
    run: function (v) {
      var order = [], hits = 0, m = {};
      var t = A(v.a, ["cache = OrderedDict()                # oldest first, most recent last", "for key in accesses:", "    if key in cache: hit; cache.move_to_end(key)",
                      "    else: miss; cache[key] = ...; if len(cache) > cap: cache.popitem(last=False)   # evict the oldest"], "LRU cache of capacity " + v.cap + ": count the hits");
      for (var i = 0; i < v.a.length; i++) {
        var x = v.a[i], at = order.indexOf(x), note;
        if (at >= 0) { order.splice(at, 1); order.push(x); hits++; m[i] = "done"; note = "key " + x + " is in the cache: HIT. Move it to the most-recent end."; }
        else {
          order.push(x); m[i] = "gone"; note = "key " + x + " is not cached: MISS. Add it.";
          if (order.length > v.cap) { note += " Over capacity, so evict " + order.shift() + ", the least recently used."; }
        }
        t.snap(1, note, { ptr: { key: i }, mark: Object.assign({}, m), aux: aux("cache (oldest → newest)", "[" + order.join(", ") + "]", "hits", hits) });
      }
      t.snap(1, "Answer: " + hits + " hits out of " + v.a.length + " accesses. A hashmap finds the entry; the ordered list tells you whom to evict. Both are O(1).", { aux: aux("hits", hits) });
      return { trace: t, answer: hits };
    }
  };

  G["ds-aux"] = {
    input: [{ id: "a", label: "operations (a number pushes it, 0 pops)", type: "ints", def: "5 3 7 0 1 0 0" }],
    check: function (v) { if (v.a.length > 14) return "keep it to 14 operations"; for (var i = 0; i < v.a.length; i++) if (v.a[i] < 0) return "use 0 to pop and positive numbers to push"; },
    gen: function (rnd) { return { a: ints(rnd, ri(rnd, 1, 10), 0, 6) }; },
    brute: function (v) {
      var st = [], out = [];
      v.a.forEach(function (x) { if (x === 0) { if (st.length) st.pop(); } else st.push(x); out.push(st.length ? Math.min.apply(null, st) : "-"); });
      return J(out);
    },
    run: function (v) {
      var st = [], out = [];
      var t = A(v.a, ["stack = []                            # each entry: (value, minimum of everything at or below it)", "push x: stack.append((x, min(x, stack[-1][1]) if stack else x))", "pop:    stack.pop()      # the minimum below is already stored",
                      "get_min: stack[-1][1]                 # O(1)"], "a stack that always knows its minimum");
      for (var i = 0; i < v.a.length; i++) {
        var x = v.a[i], note;
        if (x === 0) { if (st.length) { var g = st.pop(); note = "pop " + g[0] + ". The minimum under it was stored, so it is simply the new top's second value."; } else note = "pop on an empty stack: nothing to do."; }
        else { st.push([x, st.length ? Math.min(x, st[st.length - 1][1]) : x]); note = "push " + x + " together with the minimum so far, " + st[st.length - 1][1] + "."; }
        out.push(st.length ? st[st.length - 1][1] : "-");
        t.snap(x === 0 ? 2 : 1, note + " getMin = " + out[out.length - 1] + ".", { ptr: { op: i }, aux: aux("stack (value,min)", st.map(function (e) { return "(" + e[0] + "," + e[1] + ")"; }).join(" ") || "empty", "getMin", out[out.length - 1]) });
      }
      t.snap(3, "getMin after each operation: " + out.join(", ") + ".", { aux: aux("answer", out.join(",")) });
      return { trace: t, answer: J(out) };
    }
  };

  G["ds-queue"] = {
    input: [{ id: "a", label: "operations (a number enqueues it, 0 dequeues)", type: "ints", def: "1 2 0 3 0 0" }],
    check: function (v) { if (v.a.length > 14) return "keep it to 14 operations"; for (var i = 0; i < v.a.length; i++) if (v.a[i] < 0) return "0 to dequeue, positive numbers to enqueue"; },
    gen: function (rnd) { return { a: ints(rnd, ri(rnd, 1, 10), 0, 6) }; },
    brute: function (v) { var q = [], out = []; v.a.forEach(function (x) { if (x) q.push(x); else if (q.length) out.push(q.shift()); }); return out.length ? J(out) : "none"; },
    run: function (v) {
      var inn = [], out = [], got = [];
      var t = A(v.a, ["in_stack, out_stack = [], []", "enqueue x: in_stack.append(x)", "dequeue:", "    if not out_stack:                # refill ONLY when empty, or the order breaks",
                      "        while in_stack: out_stack.append(in_stack.pop())", "    return out_stack.pop()"], "a queue built from two stacks");
      for (var i = 0; i < v.a.length; i++) {
        var x = v.a[i], note;
        if (x) { inn.push(x); note = "enqueue " + x + ": push on the IN stack."; }
        else if (inn.length || out.length) {
          note = "dequeue: ";
          if (!out.length) { note += "OUT stack is empty, so pour the IN stack into it (this reverses the order, putting the oldest on top). "; while (inn.length) out.push(inn.pop()); }
          var g = out.pop(); got.push(g); note += "pop " + g + " from OUT.";
        } else note = "dequeue on an empty queue: nothing to do.";
        t.snap(x ? 1 : 3, note, { ptr: { op: i }, aux: aux("IN stack", "[" + inn.join(",") + "]", "OUT stack", "[" + out.join(",") + "]", "dequeued", got.join(",") || "—") });
      }
      t.snap(5, "Each item moves between stacks at most once, so dequeue is O(1) amortised. Dequeued in order: " + (got.join(", ") || "nothing") + ".", { aux: aux("answer", got.join(",") || "none") });
      return { trace: t, answer: got.length ? J(got) : "none" };
    }
  };

  G["ds-random"] = {
    input: [{ id: "a", label: "ops (positive = insert x, negative = remove |x|)", type: "ints", def: "1 2 3 -2 4 -1" }],
    check: function (v) { if (v.a.length > 14) return "keep it to 14 operations"; for (var i = 0; i < v.a.length; i++) if (v.a[i] === 0) return "no zeros: use positive to insert and negative to remove"; },
    gen: function (rnd) { var a = ints(rnd, ri(rnd, 1, 10), -5, 5).map(function (x) { return x === 0 ? 1 : x; }); return { a: a }; },
    brute: function (v) { var s = {}; v.a.forEach(function (x) { if (x > 0) s[x] = 1; else delete s[-x]; }); var k = Object.keys(s).map(Number).sort(function (p, q) { return p - q; }); return k.length ? J(k) : "empty"; },
    run: function (v) {
      var arr = [], at = {};
      var t = A(v.a, ["arr, at = [], {}                       # at[x] = index of x in arr", "insert x: at[x] = len(arr); arr.append(x)", "remove x: i = at[x]; last = arr[-1]",
                      "         arr[i], at[last] = last, i       # move the LAST value into the gap", "         arr.pop(); del at[x]       # popping the end is O(1)", "get_random: random.choice(arr)   # uniform, because arr has no holes"], "O(1) insert, delete and getRandom");
      for (var i = 0; i < v.a.length; i++) {
        var x = v.a[i], note;
        if (x > 0) { if (x in at) note = "insert " + x + ": already present."; else { at[x] = arr.length; arr.push(x); note = "insert " + x + " at the end of the array."; } }
        else {
          var y = -x;
          if (!(y in at)) note = "remove " + y + ": not present.";
          else { var idx = at[y], last = arr[arr.length - 1]; arr[idx] = last; at[last] = idx; arr.pop(); delete at[y]; note = "remove " + y + ": the last value " + last + " takes its place, then the end is popped. No shifting."; }
        }
        t.snap(x > 0 ? 1 : 3, note, { ptr: { op: i }, aux: aux("array", "[" + arr.join(", ") + "]", "index map", Object.keys(at).map(function (k) { return k + "→" + at[k]; }).join(" ") || "empty") });
      }
      var k = arr.slice().sort(function (p, q) { return p - q; });
      t.snap(5, "Final contents " + (k.join(", ") || "none") + ". getRandom picks any array index, and every element is equally likely.", { aux: aux("answer", k.join(",") || "empty") });
      return { trace: t, answer: k.length ? J(k) : "empty" };
    }
  };

  G["ds-timekey"] = {
    input: [{ id: "a", label: "timestamps", type: "ints", def: "1 4 4 9 12" }, { id: "q", label: "query time", type: "int", def: 10 }],
    prep: function (v) { v.a = v.a.slice().sort(function (p, q) { return p - q; }); },
    check: function (v) { if (v.a.length > 14) return "keep it to 14 timestamps"; },
    gen: function (rnd) { return { a: ints(rnd, ri(rnd, 1, 9), 1, 20), q: ri(rnd, 0, 22) }; },
    brute: function (v) { var best = -1; for (var i = 0; i < v.a.length; i++) if (v.a[i] <= v.q) best = i; return best < 0 ? "none" : best; },
    run: function (v) {
      var a = v.a, lo = 0, hi = a.length;
      var t = A(a, ["lo, hi = 0, len(times)", "while lo < hi:                          # bisect_right: first index with time > t", "    mid = (lo + hi) // 2",
                    "    if times[mid] <= t: lo = mid + 1", "    else: hi = mid", "return lo - 1                          # last time <= t, or none"], "latest value at or before time " + v.q + " (timestamps arrive in order, so they are sorted)");
      while (lo < hi) {
        var mid = (lo + hi) >> 1;
        t.snap(2, "check times[" + mid + "] = " + a[mid] + (a[mid] <= v.q ? " ≤ " : " > ") + v.q + (a[mid] <= v.q ? ": the answer is here or to the right." : ": too late, look left."), { ptr: { lo: lo, mid: mid, hi: hi }, span: [lo, hi - 1] });
        if (a[mid] <= v.q) lo = mid + 1; else hi = mid;
      }
      var ans = lo - 1;
      t.snap(5, ans >= 0 ? "Answer: index " + ans + " (time " + a[ans] + ") is the last one not after " + v.q + "." : "Every timestamp is after " + v.q + ": no value yet.", ans >= 0 ? { ptr: { answer: ans } } : {});
      return { trace: t, answer: ans < 0 ? "none" : ans };
    }
  };

  /* ================================ FUNCTIONAL GRAPH (array view) ================================ */
  G["gw-functional"] = {
    input: [{ id: "a", label: "next[i] for each node (-1 = none)", type: "ints", def: "3 3 4 2 3" }],
    check: function (v) { var n = v.a.length; if (n > 12) return "keep it to 12 nodes"; for (var i = 0; i < n; i++) if (v.a[i] < -1 || v.a[i] >= n || v.a[i] === i) return "each value must be -1 or another node's index"; },
    gen: function (rnd) { var n = ri(rnd, 2, 9), a = []; for (var i = 0; i < n; i++) { var x = ri(rnd, -1, n - 1); if (x === i) x = -1; a.push(x); } return { a: a }; },
    brute: function (v) {
      var n = v.a.length, best = -1;
      for (var s = 0; s < n; s++) {
        var u = s, k = 0;
        while (u !== -1 && k < n) { u = v.a[u]; k++; }
        if (u === -1) continue;
        var len = 1, w = v.a[u];
        while (w !== u) { w = v.a[w]; len++; }
        if (len > best) best = len;
      }
      return best;
    },
    run: function (v) {
      var e = v.a, n = e.length, stamp = {}, clock = 0, best = -1, m = {};
      var t = A(e, ["for s in range(n):", "    start = clock; u = s", "    while u != -1 and u not in stamp:", "        stamp[u] = clock; clock += 1; u = edges[u]",
                    "    if u != -1 and stamp[u] >= start:        # we re-entered THIS walk: a new cycle", "        best = max(best, clock - stamp[u])"], "longest cycle when every node has at most one outgoing edge");
      for (var s = 0; s < n; s++) {
        var start = clock, u = s;
        while (u !== -1 && !(u in stamp)) { stamp[u] = clock++; m[u] = "pick"; u = e[u]; }
        var cyc = u !== -1 && stamp[u] >= start;
        if (cyc) { best = Math.max(best, clock - stamp[u]); }
        for (var k in m) if (m[k] === "pick") m[k] = "done";
        t.snap(5, "walk from " + s + (cyc ? " re-entered itself: a cycle of length " + (clock - stamp[u]) + "." : u === -1 ? " fell off the end: no cycle." : " ran into an earlier walk: nothing new.") + " Best " + best + ".",
               { ptr: { s: s }, mark: Object.assign({}, m), aux: aux("best", best) });
      }
      t.snap(5, "Answer " + best + ". Every node is stamped once, so O(n).", { mark: Object.assign({}, m), aux: aux("answer", best) });
      return { trace: t, answer: best };
    }
  };

  /* ================================ STATE BFS (broken calculator) ================================ */
  G["gw-state"] = {
    input: [{ id: "x", label: "start number", type: "int", def: 3 }, { id: "y", label: "target number", type: "int", def: 10 }],
    check: function (v) { if (v.x < 1 || v.y < 1 || v.x > 20 || v.y > 20) return "numbers between 1 and 20"; },
    gen: function (rnd) { return { x: ri(rnd, 1, 20), y: ri(rnd, 1, 20) }; },
    brute: function (v) { var y = v.y, ops = 0; while (y > v.x) { y = y % 2 === 0 ? y / 2 : y + 1; ops++; } return ops + v.x - y; },
    run: function (v) {
      var L = 2 * Math.max(v.x, v.y), dist = {}, q = [v.x], m = {};
      var t = A(rng(0, L), ["from collections import deque", "q, seen = deque([(x, 0)]), {x}", "while q:", "    s, d = q.popleft()", "    if s == target: return d",
                            "    for t in (s * 2, s - 1):            # the only two moves", "        if t not in seen: seen.add(t); q.append((t, d + 1))"], "fewest moves from " + v.x + " to " + v.y + " using ×2 or −1 (each number is a state)");
      dist[v.x] = 0; m[v.x] = "pick";
      t.snap(1, "start state " + v.x + " at distance 0.", { ptr: { start: v.x }, mark: Object.assign({}, m) });
      var head = 0;
      while (head < q.length) {
        var s = q[head++], d = dist[s];
        m[s] = "done";
        if (s === v.y) { t.snap(4, "reached " + v.y + " in " + d + " moves. BFS reaches each state by its fewest moves first, so this is optimal.", { ptr: { s: s }, mark: Object.assign({}, m), aux: aux("answer", d) }); return { trace: t, answer: d }; }
        var added = [];
        [s * 2, s - 1].forEach(function (nx) { if (nx >= 1 && nx <= L && !(nx in dist)) { dist[nx] = d + 1; q.push(nx); m[nx] = "pick"; added.push(nx); } });
        t.snap(5, "pop " + s + " (distance " + d + "): new states " + (added.join(", ") || "none") + " at distance " + (d + 1) + ".", { ptr: { s: s }, mark: Object.assign({}, m), aux: aux("queue length", q.length - head) });
      }
      t.snap(4, "target unreachable.", {});
      return { trace: t, answer: -1 };
    }
  };

  G["tr-xor"] = {
    input: [{ id: "a", label: "numbers (0 to 15)", type: "ints", def: "3 10 5 2 8" }],
    check: function (v) { if (v.a.length > 10) return "keep it to 10 numbers"; for (var i = 0; i < v.a.length; i++) if (v.a[i] < 0 || v.a[i] > 15) return "numbers from 0 to 15"; },
    gen: function (rnd) { return { a: ints(rnd, ri(rnd, 1, 8), 0, 15) }; },
    brute: function (v) { var b = 0; for (var i = 0; i < v.a.length; i++) for (var j = i + 1; j < v.a.length; j++) b = Math.max(b, v.a[i] ^ v.a[j]); return b; },
    run: function (v) {
      var a = v.a, best = 0, set = {};
      var t = A(a, ["trie = {}  # insert every number, high bit first", "for x in nums:", "    walk the trie: at each bit, go to the OPPOSITE bit if it exists", "    best = max(best, the XOR built along the way)"], "maximum XOR of two numbers with a binary trie (4 bits here)");
      a.forEach(function (x) { set[x] = 1; });
      for (var i = 0; i < a.length; i++) {
        var x = a[i], cur = 0, node = a.slice();
        for (var b = 3; b >= 0; b--) {
          var bit = (x >> b) & 1;
          var want = node.filter(function (y) { return ((y >> b) & 1) === 1 - bit; });
          if (want.length) { cur |= 1 << b; node = want; } else node = node.filter(function (y) { return ((y >> b) & 1) === bit; });
        }
        var partner = node[0];
        if (a.length > 1 || true) best = Math.max(best, cur);
        var pi = a.indexOf(partner), p = { x: i }; if (pi !== i) p.partner = pi;
        t.snap(3, "x=" + x + " (binary " + ("0000" + x.toString(2)).slice(-4) + "): at every bit steer toward the opposite bit. Best partner " + partner + ", XOR " + cur + ". Best overall " + best + ".", { ptr: p, aux: aux("best", best) });
      }
      t.snap(3, "Answer " + best + ". Only 4 steps per number, whatever the array size.", { aux: aux("answer", best) });
      return { trace: t, answer: best };
    }
  };

  G["__h_loaded"] = undefined; delete G["__h_loaded"];
})();
