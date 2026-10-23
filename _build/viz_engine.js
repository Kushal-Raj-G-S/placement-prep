/* =====================================================================================
   VIZ ENGINE  --  the trace generators for Pattern Radar's "watch it run".

   These run IN THE BROWSER, so they work on whatever input you type, not just a canned
   example. Each generator declares:

      input   the fields to show (array / string / number / interval pairs) + defaults
      prep    optional: normalise the input (e.g. binary search needs it sorted) + say so
      check   optional: return an error string if the input cannot be run
      run     produce {trace, answer} -- recording a frame at every interesting step
      brute   the same answer computed a DIFFERENT, obviously-correct way

   build_radar.py runs this file under Node and fuzzes every generator: hundreds of random
   inputs, asserting run().answer === brute() each time, plus a structural check that every
   frame points at a real code line and real cell indices. A generator that lies fails the
   build. That is why the animation can be trusted.

   Add one: write G["variant-id"] = {...} and rebuild.
   ===================================================================================== */
(function () {
  "use strict";

  function Trace(data, code, kind, caption) {
    this.kind = kind || "array";
    this.data = data;
    this.code = code;
    this.caption = caption || "";
    this.frames = [];
  }
  Trace.prototype.snap = function (line, note, o) {
    o = o || {};
    /* A span is what to shade: [lo, hi] on a row, [r1, c1, r2, c2] on a grid. Once a search
       range empties out it can arrive inverted or past the ends -- that means "nothing to
       shade", so normalise instead of drawing nonsense. Trees and graphs have no span. */
    var span = o.span || null;
    if (span && this.kind !== "grid" && this.kind !== "tree" && this.kind !== "graph") {
      var n = this.data.length;
      var a = Math.max(0, span[0]), b = Math.min(n - 1, span[1]);
      span = (a > b) ? null : [a, b];
    }
    this.frames.push({
      line: line, note: note,
      ptr: o.ptr || {},
      span: span,
      mark: o.mark || {},
      emark: o.emark || {},
      aux: o.aux || []
    });
  };
  /* mark every index in [a,b] with one state */
  function range(a, b, state) {
    var m = {};
    for (var i = a; i <= b; i++) m[i] = state;
    return m;
  }
  function merge() {
    var out = {};
    for (var i = 0; i < arguments.length; i++) {
      var o = arguments[i] || {};
      for (var k in o) if (o.hasOwnProperty(k)) out[k] = o[k];
    }
    return out;
  }
  function kv(obj, fmt) {
    var out = [], ks = Object.keys(obj);
    ks.sort(function (a, b) { return (a - b) || (a < b ? -1 : 1); });
    for (var i = 0; i < ks.length; i++) out.push((fmt ? fmt(ks[i], obj[ks[i]]) : ks[i] + " → " + obj[ks[i]]));
    return out;
  }
  function strs(a) { return a.map(function (x) { return String(x); }); }

  var G = {};

  /* ================================ SLIDING WINDOW ================================ */

  G["sw-fixed"] = {
    input: [{ id: "a", label: "array", type: "ints", def: "2 1 5 1 3 2" },
            { id: "k", label: "window k", type: "int", def: 3 }],
    check: function (v) {
      if (v.k > v.a.length) return "k must be ≤ the array length";
      if (v.k < 1) return "k must be at least 1";
    },
    brute: function (v) {
      var best = -Infinity;
      for (var i = 0; i + v.k <= v.a.length; i++) {
        var s = 0;
        for (var j = i; j < i + v.k; j++) s += v.a[j];
        if (s > best) best = s;
      }
      return best;
    },
    run: function (v) {
      var a = v.a, k = v.k;
      var t = new Trace(a, ["s = sum(a[:k])", "best = s", "for r in range(k, len(a)):",
                            "    s += a[r] - a[r-k]", "    best = max(best, s)"],
                        "array", "k = " + k + ", biggest window sum");
      var s = 0, i;
      for (i = 0; i < k; i++) s += a[i];
      t.snap(0, "Build the first window once: " + a.slice(0, k).join(" + ") + " = " + s +
                ". Everything after this is one add and one remove.",
             { span: [0, k - 1], aux: [{ label: "sum", text: String(s) }] });
      var best = s;
      t.snap(1, "best = " + best + " so far.",
             { span: [0, k - 1], aux: [{ label: "sum", text: String(s) }, { label: "best", text: String(best) }] });
      for (var r = k; r < a.length; r++) {
        t.snap(3, "a[" + r + "]=" + a[r] + " enters, a[" + (r - k) + "]=" + a[r - k] +
                  " leaves. One in, one out — that is why this is O(n), not O(n·k).",
               { ptr: { "in": r, out: r - k }, span: [r - k, r], mark: { [r - k]: "gone" },
                 aux: [{ label: "sum", text: s + " − " + a[r - k] + " + " + a[r] },
                       { label: "best", text: String(best) }] });
        s += a[r] - a[r - k];
        if (s > best) best = s;
        t.snap(4, "window [" + (r - k + 1) + ".." + r + "] sums to " + s + ". best = " + best + ".",
               { span: [r - k + 1, r],
                 aux: [{ label: "sum", text: String(s) }, { label: "best", text: String(best) }] });
      }
      t.snap(4, "Answer " + best + ". " + a.length + " elements, " + a.length + " steps.",
             { aux: [{ label: "best", text: String(best) }] });
      return { trace: t, answer: best };
    }
  };

  G["sw-longest"] = {
    input: [{ id: "s", label: "string", type: "string", def: "abcabcbb" }],
    brute: function (v) {
      var best = 0;
      for (var i = 0; i < v.s.length; i++) {
        var seen = {};
        for (var j = i; j < v.s.length; j++) {
          if (seen[v.s[j]]) break;
          seen[v.s[j]] = 1;
          if (j - i + 1 > best) best = j - i + 1;
        }
      }
      return best;
    },
    run: function (v) {
      var s = v.s;
      var t = new Trace(s, ["for r, ch in enumerate(s):", "    while ch in window:",
                            "        window.remove(s[l]); l += 1", "    window.add(ch)",
                            "    best = max(best, r - l + 1)"],
                        "string", "longest substring with no repeated character");
      var win = {}, l = 0, best = 0;
      for (var r = 0; r < s.length; r++) {
        var ch = s[r];
        t.snap(0, "r reaches '" + ch + "'.",
               { ptr: { l: l, r: r }, span: [l, r],
                 aux: [{ label: "window", items: Object.keys(win) }, { label: "best", text: String(best) }] });
        while (win[ch]) {
          t.snap(2, "'" + ch + "' is already inside, so the window is invalid. Drop s[" + l + "]='" + s[l] +
                    "' and move l forward. l NEVER goes back — that is the whole O(n) argument.",
                 { ptr: { l: l, r: r }, span: [l, r], mark: { [l]: "bad" },
                   aux: [{ label: "window", items: Object.keys(win) }] });
          delete win[s[l]]; l++;
        }
        win[ch] = 1;
        if (r - l + 1 > best) best = r - l + 1;
        t.snap(4, "valid again: \"" + s.slice(l, r + 1) + "\", length " + (r - l + 1) + ". best = " + best + ".",
               { ptr: { l: l, r: r }, span: [l, r],
                 aux: [{ label: "window", items: Object.keys(win) }, { label: "best", text: String(best) }] });
      }
      t.snap(4, "Answer " + best + ". Note it was a WHILE, not an if — one new character can force several exits.",
             { aux: [{ label: "best", text: String(best) }] });
      return { trace: t, answer: best };
    }
  };

  G["sw-shortest"] = {
    input: [{ id: "a", label: "array (positive)", type: "ints", def: "2 3 1 2 4 3" },
            { id: "target", label: "target sum", type: "int", def: 7 }],
    check: function (v) {
      for (var i = 0; i < v.a.length; i++) if (v.a[i] <= 0) return "this variant needs POSITIVE numbers — with negatives, shrinking can raise the sum, so the window logic collapses (use prefix sum + deque)";
    },
    brute: function (v) {
      var best = 0;
      for (var i = 0; i < v.a.length; i++) {
        var s = 0;
        for (var j = i; j < v.a.length; j++) {
          s += v.a[j];
          if (s >= v.target) { if (!best || j - i + 1 < best) best = j - i + 1; break; }
        }
      }
      return best;
    },
    run: function (v) {
      var a = v.a, target = v.target;
      var t = new Trace(a, ["for r, x in enumerate(a):", "    s += x", "    while s >= target:",
                            "        best = min(best, r - l + 1)", "        s -= a[l]; l += 1"],
                        "array", "shortest window with sum ≥ " + target);
      var l = 0, s = 0, best = Infinity;
      for (var r = 0; r < a.length; r++) {
        s += a[r];
        t.snap(1, "a[" + r + "]=" + a[r] + " joins; sum = " + s + ".",
               { ptr: { l: l, r: r }, span: [l, r],
                 aux: [{ label: "sum", text: String(s) },
                       { label: "best", text: best === Infinity ? "—" : String(best) }] });
        while (s >= target) {
          if (r - l + 1 < best) best = r - l + 1;
          t.snap(3, "sum " + s + " ≥ " + target + ", so this window is VALID — record length " +
                    (r - l + 1) + ", then try to shrink it.",
                 { ptr: { l: l, r: r }, span: [l, r],
                   aux: [{ label: "sum", text: String(s) }, { label: "best", text: String(best) }] });
          s -= a[l]; l++;
          t.snap(4, "drop a[" + (l - 1) + "]; sum = " + s +
                    ". Shortest means: record WHILE valid, then shrink.",
                 { ptr: { l: l, r: r }, span: l <= r ? [l, r] : null, mark: { [l - 1]: "gone" },
                   aux: [{ label: "sum", text: String(s) }] });
        }
      }
      var ans = best === Infinity ? 0 : best;
      t.snap(3, ans ? ("Answer " + ans + ". Compare with 'longest': there you record AFTER shrinking, here BEFORE.")
                    : "No window ever reached the target, so the answer is 0.",
             { aux: [{ label: "best", text: String(ans) }] });
      return { trace: t, answer: ans };
    }
  };

  G["sw-deque"] = {
    input: [{ id: "a", label: "array", type: "ints", def: "1 3 -1 -3 5 3" },
            { id: "k", label: "window k", type: "int", def: 3 }],
    check: function (v) {
      if (v.k > v.a.length) return "k must be ≤ the array length";
      if (v.k < 1) return "k must be at least 1";
    },
    brute: function (v) {
      var out = [];
      for (var i = 0; i + v.k <= v.a.length; i++) {
        var m = -Infinity;
        for (var j = i; j < i + v.k; j++) if (v.a[j] > m) m = v.a[j];
        out.push(m);
      }
      return out.join(",");
    },
    run: function (v) {
      var a = v.a, k = v.k;
      var t = new Trace(a, ["for r, x in enumerate(a):", "    while dq and a[dq[-1]] <= x: dq.pop()",
                            "    dq.append(r)", "    if dq[0] <= r - k: dq.popleft()",
                            "    if r >= k-1: out.append(a[dq[0]])"],
                        "array", "k = " + k + ", maximum of every window");
      var dq = [], out = [];
      for (var r = 0; r < a.length; r++) {
        var x = a[r];
        while (dq.length && a[dq[dq.length - 1]] <= x) {
          t.snap(1, "a[" + dq[dq.length - 1] + "]=" + a[dq[dq.length - 1]] + " is newer AND not bigger than " +
                    x + ", so it can never be a maximum again. Pop it from the BACK.",
                 { ptr: { r: r }, mark: { [dq[dq.length - 1]]: "bad" },
                   aux: [{ label: "deque (indices)", items: strs(dq) }] });
          dq.pop();
        }
        dq.push(r);
        t.snap(2, "push index " + r + ". The deque now holds only the still-possible maxima, biggest first.",
               { ptr: { r: r }, aux: [{ label: "deque (indices)", items: strs(dq) },
                                      { label: "values", items: dq.map(function (i) { return String(a[i]); }) }] });
        if (dq[0] <= r - k) {
          t.snap(3, "front index " + dq[0] + " has fallen out of the window — drop it from the FRONT.",
                 { ptr: { r: r }, span: [r - k + 1, r], mark: { [dq[0]]: "gone" },
                   aux: [{ label: "deque (indices)", items: strs(dq) }] });
          dq.shift();
        }
        if (r >= k - 1) {
          out.push(a[dq[0]]);
          t.snap(4, "window [" + (r - k + 1) + ".." + r + "] → maximum " + a[dq[0]] +
                    ", read straight off the front. No rescanning.",
                 { ptr: { r: r }, span: [r - k + 1, r], mark: { [dq[0]]: "pick" },
                   aux: [{ label: "deque (indices)", items: strs(dq) }, { label: "output", items: strs(out) }] });
        }
      }
      t.snap(4, "Answer [" + out.join(", ") + "]. Each index was pushed once and popped once — O(n), not O(n·k).",
             { aux: [{ label: "output", items: strs(out) }] });
      return { trace: t, answer: out.join(",") };
    }
  };

  G["sw-exact"] = {
    input: [{ id: "a", label: "array", type: "ints", def: "1 2 1 2 3" },
            { id: "k", label: "exactly k distinct", type: "int", def: 2 }],
    check: function (v) { if (v.k < 1) return "k must be at least 1"; },
    brute: function (v) {
      var n = 0;
      for (var i = 0; i < v.a.length; i++) {
        var seen = {}, c = 0;
        for (var j = i; j < v.a.length; j++) {
          if (!seen[v.a[j]]) { seen[v.a[j]] = 1; c++; }
          if (c === v.k) n++;
        }
      }
      return n;
    },
    run: function (v) {
      var a = v.a, k = v.k;
      var t = new Trace(a, ["def at_most(k):", "    for r, x in enumerate(a):", "        cnt[x] += 1",
                            "        while len(cnt) > k: shrink from l", "        total += r - l + 1",
                            "exactly(k) = at_most(k) - at_most(k-1)"],
                        "array", "COUNT subarrays with exactly " + k + " distinct values");
      function atMost(kk, label) {
        var cnt = {}, l = 0, total = 0, distinct = 0;
        t.snap(0, "Pass for at_most(" + kk + "). You cannot hold 'exactly k' with one window — it is not " +
                  "monotonic, so there is nothing to shrink on. That is why the subtraction trick exists.",
               { aux: [{ label: "pass", text: "at_most(" + kk + ")" }] });
        if (kk <= 0) {
          t.snap(4, "at_most(0) is 0 by definition — no subarray has zero distinct values.",
                 { aux: [{ label: label, text: "0" }] });
          return 0;
        }
        for (var r = 0; r < a.length; r++) {
          if (!cnt[a[r]]) { cnt[a[r]] = 0; distinct++; }
          cnt[a[r]]++;
          t.snap(2, "a[" + r + "]=" + a[r] + " joins; " + distinct + " distinct in the window.",
                 { ptr: { l: l, r: r }, span: [l, r],
                   aux: [{ label: "counts", items: kv(cnt) }, { label: label, text: String(total) }] });
          while (distinct > kk) {
            cnt[a[l]]--;
            if (cnt[a[l]] === 0) { delete cnt[a[l]]; distinct--; }
            t.snap(3, "too many distinct — drop a[" + l + "]=" + a[l] + " and move l.",
                   { ptr: { l: l, r: r }, span: [l, r], mark: { [l]: "bad" },
                     aux: [{ label: "counts", items: kv(cnt) }] });
            l++;
          }
          total += r - l + 1;
          t.snap(4, "every window ending at " + r + " is valid, and there are " + (r - l + 1) +
                    " of them — so ADD that, do not take a max. Counting, not measuring.",
                 { ptr: { l: l, r: r }, span: [l, r],
                   aux: [{ label: "+", text: String(r - l + 1) }, { label: label, text: String(total) }] });
        }
        return total;
      }
      var hi = atMost(k, "at_most(" + k + ")");
      var lo = atMost(k - 1, "at_most(" + (k - 1) + ")");
      var ans = hi - lo;
      t.snap(5, "exactly(" + k + ") = " + hi + " − " + lo + " = " + ans +
                ". The windows with at most k, minus those with at most k−1, are exactly those with k.",
             { aux: [{ label: "answer", text: String(ans) }] });
      return { trace: t, answer: ans };
    }
  };

  /* ================================= TWO POINTERS ================================= */

  G["tp-ends"] = {
    input: [{ id: "a", label: "array (sorted for you)", type: "ints", def: "1 3 4 6 8 11" },
            { id: "target", label: "target", type: "int", def: 14 }],
    prep: function (v) {
      var was = v.a.join(" ");
      v.a = v.a.slice().sort(function (x, y) { return x - y; });
      return was === v.a.join(" ") ? null : "sorted your input first — this variant needs order to decide which pointer to move";
    },
    brute: function (v) {
      for (var i = 0; i < v.a.length; i++)
        for (var j = i + 1; j < v.a.length; j++)
          if (v.a[i] + v.a[j] === v.target) return 1;
      return 0;
    },
    run: function (v) {
      var a = v.a, target = v.target;
      var t = new Trace(a, ["l, r = 0, len(a)-1", "while l < r:", "    s = a[l] + a[r]",
                            "    if s == target: return [l, r]", "    if s < target: l += 1", "    else: r -= 1"],
                        "array", "sorted array, find a pair summing to " + target);
      var l = 0, r = a.length - 1, found = 0;
      t.snap(0, "Start at both ends. Sortedness is what makes 'move left or right' a decision instead of a guess.",
             { ptr: { l: l, r: r }, span: [l, r] });
      while (l < r) {
        var s = a[l] + a[r];
        t.snap(2, a[l] + " + " + a[r] + " = " + s,
               { ptr: { l: l, r: r }, span: [l, r],
                 aux: [{ label: "sum", text: String(s) }, { label: "target", text: String(target) }] });
        if (s === target) {
          found = 1;
          t.snap(3, "Found it: " + a[l] + " + " + a[r] + " = " + target + ".",
                 { ptr: { l: l, r: r }, mark: { [l]: "pick", [r]: "pick" } });
          break;
        }
        if (s < target) {
          t.snap(4, s + " is too small. Only the LEFT can grow, so l moves — and every pair using a[" + l +
                    "] is ruled out in one step.",
                 { ptr: { l: l, r: r }, span: [l, r], mark: { [l]: "gone" } });
          l++;
        } else {
          t.snap(5, s + " is too big. Only the RIGHT can shrink, so r moves — ruling out every pair using a[" +
                    r + "].",
                 { ptr: { l: l, r: r }, span: [l, r], mark: { [r]: "gone" } });
          r--;
        }
      }
      if (!found) t.snap(1, "The pointers met with no pair found. Every pair was eliminated in " +
                            a.length + " steps, not " + (a.length * (a.length - 1) / 2) + ".", {});
      return { trace: t, answer: found };
    }
  };

  G["tp-write"] = {
    input: [{ id: "a", label: "array", type: "ints", def: "0 1 0 3 12" },
            { id: "drop", label: "value to remove", type: "int", def: 0 }],
    brute: function (v) {
      return v.a.filter(function (x) { return x !== v.drop; })
               .concat(v.a.filter(function (x) { return x === v.drop; })).join(",");
    },
    run: function (v) {
      var arr = v.a.slice(), drop = v.drop;
      var t = new Trace(v.a, ["write = 0", "for read in range(len(a)):", "    if a[read] != " + drop + ":",
                              "        a[write] = a[read]; write += 1", "# then fill the tail"],
                        "array", "move every " + drop + " to the end, in place");
      var write = 0;
      t.snap(0, "write = the next slot to fill, read scans everything. a[0:write] is the finished answer at all times.",
             { ptr: { write: 0, read: 0 } });
      for (var read = 0; read < arr.length; read++) {
        if (arr[read] !== drop) {
          arr[write] = arr[read];
          t.snap(3, "a[" + read + "]=" + arr[read] + " is a keeper → copy it to slot " + write + ", advance write.",
                 { ptr: { write: write, read: read }, mark: merge(range(0, write - 1, "done"), { [write]: "pick" }),
                   aux: [{ label: "array", items: strs(arr) }] });
          write++;
        } else {
          t.snap(2, "a[" + read + "]=" + drop + " fails the keep-test, so write stays put. Only the test ever " +
                    "changes in this template.",
                 { ptr: { write: write, read: read }, mark: { [read]: "bad" },
                   aux: [{ label: "array", items: strs(arr) }] });
        }
      }
      for (var i = write; i < arr.length; i++) arr[i] = drop;
      t.snap(4, write + " keeper(s) sit in front; fill the rest. O(1) extra space, one pass.",
             { mark: range(0, write - 1, "done"), aux: [{ label: "array", items: strs(arr) }] });
      return { trace: t, answer: arr.join(",") };
    }
  };

  G["tp-partition"] = {
    input: [{ id: "a", label: "array of 0 / 1 / 2", type: "ints", def: "2 0 2 1 1 0" }],
    check: function (v) {
      for (var i = 0; i < v.a.length; i++) if (v.a[i] < 0 || v.a[i] > 2) return "this one segregates three buckets, so values must be 0, 1 or 2";
    },
    brute: function (v) { return v.a.slice().sort(function (a, b) { return a - b; }).join(","); },
    run: function (v) {
      var arr = v.a.slice();
      var t = new Trace(v.a, ["while mid <= high:", "    if a[mid] == 0: swap(low, mid); low += 1; mid += 1",
                              "    elif a[mid] == 2: swap(mid, high); high -= 1", "    else: mid += 1"],
                        "array", "Dutch flag — sort 0s, 1s, 2s in ONE pass");
      var low = 0, mid = 0, high = arr.length - 1, sw;
      t.snap(0, "Three regions: [0,low) are 0s, [low,mid) are 1s, (high,n) are 2s. [mid,high] is unknown.",
             { ptr: { low: low, mid: mid, high: high }, aux: [{ label: "array", items: strs(arr) }] });
      while (mid <= high) {
        if (arr[mid] === 0) {
          sw = arr[low]; arr[low] = arr[mid]; arr[mid] = sw;
          t.snap(1, "a[mid]=0 → swap it down to the 0-region. Both low and mid advance.",
                 { ptr: { low: low, mid: mid, high: high }, mark: { [low]: "done", [mid]: "pick" },
                   aux: [{ label: "array", items: strs(arr) }] });
          low++; mid++;
        } else if (arr[mid] === 2) {
          sw = arr[high]; arr[high] = arr[mid]; arr[mid] = sw;
          t.snap(2, "a[mid]=2 → swap it up to the 2-region. high shrinks, and mid does NOT advance: the " +
                    "value just pulled in has not been examined yet.",
                 { ptr: { low: low, mid: mid, high: high }, mark: { [high]: "done", [mid]: "pick" },
                   aux: [{ label: "array", items: strs(arr) }] });
          high--;
        } else {
          t.snap(3, "a[mid]=1 is already home. Step over it.",
                 { ptr: { low: low, mid: mid, high: high }, mark: { [mid]: "done" },
                   aux: [{ label: "array", items: strs(arr) }] });
          mid++;
        }
      }
      t.snap(0, "Sorted in one pass, no counting, no second loop.",
             { aux: [{ label: "array", items: strs(arr) }] });
      return { trace: t, answer: arr.join(",") };
    }
  };

  /* =================================== PREFIX SUM ================================== */

  G["ps-range"] = {
    input: [{ id: "a", label: "array", type: "ints", def: "2 4 1 5 3" },
            { id: "l", label: "query l", type: "int", def: 1 },
            { id: "r", label: "query r", type: "int", def: 3 }],
    check: function (v) {
      if (v.l < 0 || v.r >= v.a.length) return "l and r must be indices inside the array (0 to " + (v.a.length - 1) + ")";
      if (v.l > v.r) return "l must be ≤ r";
    },
    brute: function (v) {
      var s = 0;
      for (var i = v.l; i <= v.r; i++) s += v.a[i];
      return s;
    },
    run: function (v) {
      var a = v.a;
      var t = new Trace(a, ["pre[0] = 0", "for i, x in enumerate(a):", "    pre[i+1] = pre[i] + x",
                            "", "range_sum(l, r) = pre[r+1] - pre[l]"],
                        "array", "build once, then any range sum is one subtraction");
      var pre = [0];
      t.snap(0, "pre has n+1 cells and pre[0]=0. That padding is what removes the 'if l == 0' special case.",
             { aux: [{ label: "pre", items: strs(pre) }] });
      for (var i = 0; i < a.length; i++) {
        pre.push(pre[i] + a[i]);
        t.snap(2, "pre[" + (i + 1) + "] = " + pre[i + 1] + " — the sum of everything BEFORE index " + (i + 1) + ".",
               { ptr: { i: i }, span: [0, i], aux: [{ label: "pre", items: strs(pre) }] });
      }
      var ans = pre[v.r + 1] - pre[v.l];
      t.snap(4, "sum(" + v.l + ".." + v.r + ") = pre[" + (v.r + 1) + "] − pre[" + v.l + "] = " +
                pre[v.r + 1] + " − " + pre[v.l] + " = " + ans + ". O(1), however long the range.",
             { span: [v.l, v.r], mark: range(v.l, v.r, "pick"),
               aux: [{ label: "pre", items: strs(pre) },
                     { label: "sum(" + v.l + ".." + v.r + ")", text: String(ans) }] });
      return { trace: t, answer: ans };
    }
  };

  G["ps-count"] = {
    input: [{ id: "a", label: "array (negatives fine)", type: "ints", def: "3 4 7 2 -3 1 4 2" },
            { id: "k", label: "target sum k", type: "int", def: 7 }],
    brute: function (v) {
      var n = 0;
      for (var i = 0; i < v.a.length; i++) {
        var s = 0;
        for (var j = i; j < v.a.length; j++) { s += v.a[j]; if (s === v.k) n++; }
      }
      return n;
    },
    run: function (v) {
      var a = v.a, k = v.k;
      var t = new Trace(a, ["seen = {0: 1}", "for x in a:", "    pre += x", "    res += seen.get(pre - k, 0)",
                            "    seen[pre] = seen.get(pre, 0) + 1"],
                        "array", "count subarrays summing to " + k);
      var seen = { 0: 1 }, pre = 0, res = 0;
      t.snap(0, "Seed {0: 1} — the empty prefix. Without it you miss every subarray that starts at index 0.",
             { aux: [{ label: "seen", items: kv(seen) }] });
      for (var i = 0; i < a.length; i++) {
        pre += a[i];
        t.snap(2, "prefix after a[" + i + "] is " + pre + ".",
               { ptr: { i: i }, span: [0, i],
                 aux: [{ label: "prefix", text: String(pre) }, { label: "seen", items: kv(seen) }] });
        var hit = seen[pre - k] || 0;
        res += hit;
        t.snap(3, hit ? ("need an earlier prefix of " + (pre - k) + "; found " + hit + " of them, so " + hit +
                         " more subarray(s) end here. This is the rearrangement: pre_r − pre_l = k.")
                      : ("need an earlier prefix of " + (pre - k) + "; none seen, so nothing ends here."),
               { ptr: { i: i }, span: [0, i],
                 aux: [{ label: "looking for", text: String(pre - k) }, { label: "count", text: String(res) }] });
        seen[pre] = (seen[pre] || 0) + 1;
        t.snap(4, "record prefix " + pre + ". Recorded AFTER the lookup, or a zero-length subarray counts itself.",
               { ptr: { i: i }, aux: [{ label: "seen", items: kv(seen) }] });
      }
      t.snap(3, "Answer " + res + " subarray(s). A sliding window cannot do this when negatives are present — " +
                "shrinking no longer reliably lowers the sum.",
             { aux: [{ label: "count", text: String(res) }] });
      return { trace: t, answer: res };
    }
  };

  G["ps-longest"] = {
    input: [{ id: "a", label: "array (negatives fine)", type: "ints", def: "1 -1 5 -2 3" },
            { id: "k", label: "target sum k", type: "int", def: 3 }],
    brute: function (v) {
      var best = 0;
      for (var i = 0; i < v.a.length; i++) {
        var s = 0;
        for (var j = i; j < v.a.length; j++) {
          s += v.a[j];
          if (s === v.k && j - i + 1 > best) best = j - i + 1;
        }
      }
      return best;
    },
    run: function (v) {
      var a = v.a, k = v.k;
      var t = new Trace(a, ["first = {0: -1}", "for i, x in enumerate(a):", "    pre += x",
                            "    if pre - k in first: best = max(best, i - first[pre-k])",
                            "    if pre not in first: first[pre] = i"],
                        "array", "LONGEST subarray summing to " + k);
      var first = { 0: -1 }, pre = 0, best = 0;
      t.snap(0, "Same rearrangement as the counting version, but the map stores the FIRST index of each prefix, " +
                "never overwritten — earliest index means longest reach.",
             { aux: [{ label: "first seen", items: kv(first) }] });
      for (var i = 0; i < a.length; i++) {
        pre += a[i];
        t.snap(2, "prefix after a[" + i + "] is " + pre + ".",
               { ptr: { i: i }, span: [0, i],
                 aux: [{ label: "prefix", text: String(pre) }, { label: "first seen", items: kv(first) }] });
        if (first.hasOwnProperty(pre - k)) {
          var from = first[pre - k];
          if (i - from > best) best = i - from;
          t.snap(3, "prefix " + (pre - k) + " was first seen at index " + from + ", so a[" + (from + 1) + ".." + i +
                    "] sums to " + k + " — length " + (i - from) + ". best = " + best + ".",
                 { ptr: { i: i }, span: [from + 1, i], mark: range(from + 1, i, "pick"),
                   aux: [{ label: "best", text: String(best) }] });
        } else {
          t.snap(3, "no earlier prefix of " + (pre - k) + ", so nothing ends here.",
                 { ptr: { i: i }, aux: [{ label: "looking for", text: String(pre - k) }] });
        }
        if (!first.hasOwnProperty(pre)) {
          first[pre] = i;
          t.snap(4, "prefix " + pre + " is new — record index " + i + ". LONGEST keeps the FIRST index; " +
                    "SHORTEST would keep the latest. Getting that backwards is a silent wrong answer.",
                 { ptr: { i: i }, aux: [{ label: "first seen", items: kv(first) }] });
        } else {
          t.snap(4, "prefix " + pre + " was already seen at index " + first[pre] +
                    " — do NOT overwrite it, or you shorten every future span.",
                 { ptr: { i: i }, aux: [{ label: "first seen", items: kv(first) }] });
        }
      }
      t.snap(3, "Answer " + best + ".", { aux: [{ label: "best", text: String(best) }] });
      return { trace: t, answer: best };
    }
  };

  G["ps-diff"] = {
    input: [{ id: "n", label: "array length", type: "int", def: 7 },
            { id: "ops", label: "range adds  l,r,v", type: "triples", def: "1,3,2 2,5,3 0,6,1" }],
    check: function (v) {
      if (v.n < 1) return "length must be at least 1";
      for (var i = 0; i < v.ops.length; i++) {
        var o = v.ops[i];
        if (o[0] < 0 || o[1] >= v.n) return "range " + o[0] + "," + o[1] + " is outside 0.." + (v.n - 1);
        if (o[0] > o[1]) return "each range needs l ≤ r";
      }
    },
    brute: function (v) {
      var out = [], i, j;
      for (i = 0; i < v.n; i++) out.push(0);
      for (i = 0; i < v.ops.length; i++)
        for (j = v.ops[i][0]; j <= v.ops[i][1]; j++) out[j] += v.ops[i][2];
      return out.join(",");
    },
    run: function (v) {
      var n = v.n, ops = v.ops, i;
      var cells = [];
      for (i = 0; i < n; i++) cells.push(0);
      var t = new Trace(cells, ["diff = [0] * (n + 1)", "for l, r, val in ops:", "    diff[l] += val",
                                "    diff[r+1] -= val", "run = 0; for i in range(n):", "    run += diff[i]"],
                        "array", ops.length + " range-add operations, read once at the end");
      var diff = [];
      for (i = 0; i <= n; i++) diff.push(0);
      t.snap(0, "diff has n+1 cells. The extra slot is what lets r+1 be written for the very last range.",
             { aux: [{ label: "diff", items: strs(diff) }] });
      for (i = 0; i < ops.length; i++) {
        var l = ops[i][0], r = ops[i][1], val = ops[i][2];
        diff[l] += val;
        t.snap(2, "add " + val + " over [" + l + ".." + r + "]: mark the START with +" + val +
                  ". O(1), however wide the range.",
               { span: [l, r], mark: { [l]: "pick" }, aux: [{ label: "diff", items: strs(diff) }] });
        diff[r + 1] -= val;
        t.snap(3, "and mark one PAST the end with −" + val + ", so the effect stops there.",
               { span: [l, r], mark: merge({ [l]: "pick" }, r + 1 < n ? { [r + 1]: "bad" } : {}),
                 aux: [{ label: "diff", items: strs(diff) }] });
      }
      var run = 0, out = [];
      t.snap(4, "Now one prefix sum over diff rebuilds the whole array.",
             { aux: [{ label: "diff", items: strs(diff) }] });
      for (i = 0; i < n; i++) {
        run += diff[i];
        out.push(run);
        t.snap(5, "running total at index " + i + " is " + run + ".",
               { ptr: { i: i }, mark: merge(range(0, i - 1, "done"), { [i]: "pick" }),
                 aux: [{ label: "result", items: strs(out) }] });
      }
      t.snap(5, "Answer [" + out.join(", ") + "]. " + ops.length + " updates cost O(1) each instead of O(n) — " +
                "this is the same object as a sweep line of +1 / −1 events.",
             { mark: range(0, n - 1, "done"), aux: [{ label: "result", items: strs(out) }] });
      return { trace: t, answer: out.join(",") };
    }
  };

  G["ps-suffix"] = {
    input: [{ id: "a", label: "array", type: "ints", def: "1 2 3 4" }],
    brute: function (v) {
      var out = [];
      for (var i = 0; i < v.a.length; i++) {
        var p = 1;
        for (var j = 0; j < v.a.length; j++) if (j !== i) p *= v.a[j];
        out.push(p);
      }
      return out.join(",");
    },
    run: function (v) {
      var a = v.a, i;
      var t = new Trace(a, ["left = 1", "for i in range(n): out[i] = left; left *= a[i]",
                            "right = 1", "for i in reversed(range(n)): out[i] *= right; right *= a[i]"],
                        "array", "product of everything except me — no division");
      var out = [];
      for (i = 0; i < a.length; i++) out.push(1);
      t.snap(0, "Each cell needs to know about BOTH sides, so: one pass left-to-right, one back.",
             { aux: [{ label: "out", items: strs(out) }] });
      var left = 1;
      for (i = 0; i < a.length; i++) {
        out[i] = left;
        t.snap(1, "out[" + i + "] = " + left + " — the product of everything strictly LEFT of " + i + ".",
               { ptr: { i: i }, span: i > 0 ? [0, i - 1] : null, mark: { [i]: "pick" },
                 aux: [{ label: "left", text: String(left) }, { label: "out", items: strs(out) }] });
        left *= a[i];
      }
      var right = 1;
      t.snap(2, "Now sweep back, carrying the product of everything to the RIGHT.",
             { aux: [{ label: "out", items: strs(out) }] });
      for (i = a.length - 1; i >= 0; i--) {
        out[i] *= right;
        t.snap(3, "out[" + i + "] × " + right + " = " + out[i] +
                  " — left side times right side, and a[" + i + "] itself was never used.",
               { ptr: { i: i }, span: i < a.length - 1 ? [i + 1, a.length - 1] : null, mark: { [i]: "done" },
                 aux: [{ label: "right", text: String(right) }, { label: "out", items: strs(out) }] });
        right *= a[i];
      }
      t.snap(3, "Answer [" + out.join(", ") + "]. The left pass wrote straight into the output and carried only " +
                "a scalar — that is how you get O(1) extra space.",
             { mark: range(0, a.length - 1, "done"), aux: [{ label: "out", items: strs(out) }] });
      return { trace: t, answer: out.join(",") };
    }
  };

  /* ================================= BINARY SEARCH ================================= */

  G["bs-exact"] = {
    input: [{ id: "a", label: "array (sorted for you)", type: "ints", def: "1 3 5 7 9 11 13" },
            { id: "x", label: "find", type: "int", def: 11 }],
    prep: function (v) {
      var was = v.a.join(" ");
      v.a = v.a.slice().sort(function (p, q) { return p - q; });
      return was === v.a.join(" ") ? null : "sorted your input first — binary search needs an ordered space";
    },
    brute: function (v) { return v.a.indexOf(v.x) >= 0 ? 1 : 0; },
    run: function (v) {
      var a = v.a, x = v.x;
      var t = new Trace(a, ["lo, hi = 0, len(a)-1", "while lo <= hi:", "    mid = (lo + hi) // 2",
                            "    if a[mid] == x: return mid", "    if a[mid] < x: lo = mid + 1",
                            "    else: hi = mid - 1"],
                        "array", "find " + x);
      var lo = 0, hi = a.length - 1, steps = 0, found = 0;
      while (lo <= hi) {
        var mid = (lo + hi) >> 1;
        steps++;
        t.snap(2, "range [" + lo + ".." + hi + "], mid = " + mid + ", a[mid] = " + a[mid] + ".",
               { ptr: { lo: lo, mid: mid, hi: hi }, span: [lo, hi], mark: { [mid]: "pick" },
                 aux: [{ label: "still possible", text: (hi - lo + 1) + " cells" }] });
        if (a[mid] === x) {
          found = 1;
          t.snap(3, "Found " + x + " at index " + mid + " — " + steps + " check(s) instead of " + a.length + ".",
                 { ptr: { mid: mid }, mark: { [mid]: "done" } });
          break;
        }
        if (a[mid] < x) {
          t.snap(4, a[mid] + " < " + x + ", so every cell at or left of mid is dead. Half the range gone in one check.",
                 { ptr: { lo: lo, mid: mid, hi: hi }, span: [lo, hi], mark: range(lo, mid, "gone") });
          lo = mid + 1;
        } else {
          t.snap(5, a[mid] + " > " + x + ", so everything at or right of mid is dead.",
                 { ptr: { lo: lo, mid: mid, hi: hi }, span: [lo, hi], mark: range(mid, hi, "gone") });
          hi = mid - 1;
        }
      }
      if (!found) t.snap(1, "lo passed hi, so " + x + " is not here — proved in " + steps + " checks.", {});
      return { trace: t, answer: found };
    }
  };

  G["bs-bound"] = {
    input: [{ id: "a", label: "array (sorted for you)", type: "ints", def: "1 2 2 2 5 7" },
            { id: "x", label: "lower bound of", type: "int", def: 2 }],
    prep: function (v) {
      var was = v.a.join(" ");
      v.a = v.a.slice().sort(function (p, q) { return p - q; });
      return was === v.a.join(" ") ? null : "sorted your input first";
    },
    brute: function (v) {
      for (var i = 0; i < v.a.length; i++) if (v.a[i] >= v.x) return i;
      return v.a.length;
    },
    run: function (v) {
      var a = v.a, x = v.x;
      var t = new Trace(a, ["lo, hi = 0, len(a)      # half-open", "while lo < hi:", "    mid = (lo + hi) // 2",
                            "    if a[mid] < x: lo = mid + 1", "    else: hi = mid", "return lo"],
                        "array", "first index with a[i] ≥ " + x + "  (lower_bound)");
      var lo = 0, hi = a.length;
      t.snap(0, "Half-open: hi = n, and the loop is while lo < hi. The boundary form, not the find-it form — " +
                "pick one convention and never mix them.",
             { span: [0, a.length - 1] });
      while (lo < hi) {
        var mid = (lo + hi) >> 1;
        t.snap(2, "range [" + lo + ".." + (hi - 1) + "], mid = " + mid + ", a[mid] = " + a[mid] + ".",
               { ptr: { lo: lo, mid: mid, hi: hi }, span: [lo, hi - 1], mark: { [mid]: "pick" } });
        if (a[mid] < x) {
          t.snap(3, a[mid] + " < " + x + " → mid cannot be the boundary, and nor can anything left of it.",
                 { ptr: { lo: lo, mid: mid, hi: hi }, span: [lo, hi - 1], mark: range(lo, mid, "gone") });
          lo = mid + 1;
        } else {
          t.snap(4, a[mid] + " ≥ " + x + " → mid MIGHT be the boundary, so hi = mid, not mid−1. " +
                    "That one character is the whole difference.",
                 { ptr: { lo: lo, mid: mid, hi: hi }, span: [lo, hi - 1], mark: range(mid + 1, hi - 1, "gone") });
          hi = mid;
        }
      }
      t.snap(5, "Answer " + lo + ". Everything left of it is < " + x + ", everything from it on is ≥ " + x +
                ". upper_bound is the same loop with <= ; count of " + x + " = upper − lower.",
             { mark: lo < a.length ? { [lo]: "done" } : {}, aux: [{ label: "lower_bound", text: String(lo) }] });
      return { trace: t, answer: lo };
    }
  };

  G["bs-answer"] = {
    input: [{ id: "piles", label: "banana piles", type: "ints", def: "3 6 7 11" },
            { id: "h", label: "hours allowed", type: "int", def: 8 }],
    check: function (v) {
      if (v.h < v.piles.length) return "with " + v.piles.length + " piles you need at least " + v.piles.length + " hours — no speed can work";
      for (var i = 0; i < v.piles.length; i++) if (v.piles[i] < 1) return "every pile needs at least 1 banana";
    },
    brute: function (v) {
      var hi = Math.max.apply(null, v.piles);
      for (var k = 1; k <= hi; k++) {
        var hrs = 0;
        for (var i = 0; i < v.piles.length; i++) hrs += Math.ceil(v.piles[i] / k);
        if (hrs <= v.h) return k;
      }
      return hi;
    },
    run: function (v) {
      var piles = v.piles, h = v.h;
      var top = Math.max.apply(null, piles), i;
      var cells = [];
      for (i = 1; i <= top; i++) cells.push(i);
      var t = new Trace(cells, ["lo, hi = 1, max(piles)", "while lo < hi:", "    mid = (lo + hi) // 2",
                                "    if feasible(mid): hi = mid", "    else: lo = mid + 1", "return lo"],
                        "array", "minimum eating speed — the cells are CANDIDATE ANSWERS 1.." + top);
      function hours(k) {
        var s = 0;
        for (var j = 0; j < piles.length; j++) s += Math.ceil(piles[j] / k);
        return s;
      }
      t.snap(0, "The array being searched is the ANSWER RANGE 1.." + top + ", not the piles. That is the whole " +
                "leap of this variant.",
             { span: [0, top - 1], aux: [{ label: "piles", items: strs(piles) },
                                         { label: "hours allowed", text: String(h) }] });
      t.snap(0, "Monotonic? A faster speed can always finish what a slower one could. Say that sentence out loud " +
                "before coding — if you cannot, this is the wrong pattern.",
             { span: [0, top - 1] });
      var lo = 1, hi = top;
      while (lo < hi) {
        var mid = (lo + hi) >> 1, hrs = hours(mid), ok = hrs <= h;
        t.snap(2, "try speed " + mid + " → needs " + hrs + " hours → " + (ok ? "fits" : "too slow") + ".",
               { ptr: { lo: lo - 1, mid: mid - 1, hi: hi - 1 }, span: [lo - 1, hi - 1],
                 mark: { [mid - 1]: ok ? "pick" : "bad" },
                 aux: [{ label: "speed", text: String(mid) }, { label: "hours", text: hrs + " / " + h }] });
        if (ok) {
          t.snap(3, "speed " + mid + " works, so nothing faster needs testing — but " + mid +
                    " itself might be the answer, so hi = mid.",
                 { ptr: { lo: lo - 1, mid: mid - 1, hi: hi - 1 }, span: [lo - 1, hi - 1],
                   mark: range(mid, hi - 1, "gone") });
          hi = mid;
        } else {
          t.snap(4, "speed " + mid + " is too slow, so every slower speed is too. lo = mid + 1.",
                 { ptr: { lo: lo - 1, mid: mid - 1, hi: hi - 1 }, span: [lo - 1, hi - 1],
                   mark: range(lo - 1, mid - 1, "gone") });
          lo = mid + 1;
        }
      }
      t.snap(5, "Answer " + lo + " bananas/hour, in about log₂(" + top + ") checks — and the same handful " +
                "would do for a range of 10⁹.",
             { mark: { [lo - 1]: "done" }, aux: [{ label: "answer", text: String(lo) }] });
      return { trace: t, answer: lo };
    }
  };

  G["bs-rotated"] = {
    input: [{ id: "a", label: "rotated sorted array", type: "ints", def: "4 5 6 7 0 1 2" },
            { id: "x", label: "find", type: "int", def: 0 }],
    brute: function (v) { return v.a.indexOf(v.x) >= 0 ? 1 : 0; },
    run: function (v) {
      var a = v.a, x = v.x;
      var t = new Trace(a, ["while lo <= hi:", "    mid = (lo + hi) // 2", "    if a[mid] == x: return mid",
                            "    if a[lo] <= a[mid]:      # left half is sorted",
                            "        go left if a[lo] <= x < a[mid]", "    else:  # right half is sorted",
                            "        go right if a[mid] < x <= a[hi]"],
                        "array", "not globally sorted — but half of it always is");
      var lo = 0, hi = a.length - 1, found = 0;
      while (lo <= hi) {
        var mid = (lo + hi) >> 1;
        t.snap(1, "range [" + lo + ".." + hi + "], mid = " + mid + ", a[mid] = " + a[mid] + ".",
               { ptr: { lo: lo, mid: mid, hi: hi }, span: [lo, hi], mark: { [mid]: "pick" } });
        if (a[mid] === x) {
          found = 1;
          t.snap(2, "Found " + x + " at index " + mid + ".", { ptr: { mid: mid }, mark: { [mid]: "done" } });
          break;
        }
        if (a[lo] <= a[mid]) {
          var inLeft = a[lo] <= x && x < a[mid];
          t.snap(3, "a[lo]=" + a[lo] + " ≤ a[mid]=" + a[mid] + ", so the LEFT half is clean. " +
                    (inLeft ? ("and " + x + " lies inside it — search there.")
                            : (x + " is not in its range — so it must be in the messy right half.")),
                 { ptr: { lo: lo, mid: mid, hi: hi }, span: inLeft ? [lo, mid - 1] : [mid + 1, hi],
                   mark: inLeft ? range(mid, hi, "gone") : range(lo, mid, "gone") });
          if (inLeft) hi = mid - 1; else lo = mid + 1;
        } else {
          var inRight = a[mid] < x && x <= a[hi];
          t.snap(5, "a[lo]=" + a[lo] + " > a[mid]=" + a[mid] + ", so the RIGHT half is clean. " +
                    (inRight ? ("and " + x + " lies inside it — search there.")
                             : (x + " is not in its range — so go left.")),
                 { ptr: { lo: lo, mid: mid, hi: hi }, span: inRight ? [mid + 1, hi] : [lo, mid - 1],
                   mark: inRight ? range(lo, mid, "gone") : range(mid, hi, "gone") });
          if (inRight) lo = mid + 1; else hi = mid - 1;
        }
      }
      if (!found) t.snap(0, x + " is not in the array. Still O(log n) — at least one half is always sorted, " +
                            "which is all binary search needs.", {});
      return { trace: t, answer: found };
    }
  };

  /* ==================================== HASHING ==================================== */

  G["hs-seen"] = {
    input: [{ id: "a", label: "array", type: "ints", def: "1 2 3 1" }],
    brute: function (v) {
      for (var i = 0; i < v.a.length; i++)
        for (var j = i + 1; j < v.a.length; j++) if (v.a[i] === v.a[j]) return 1;
      return 0;
    },
    run: function (v) {
      var a = v.a;
      var t = new Trace(a, ["seen = set()", "for x in a:", "    if x in seen: return True",
                            "    seen.add(x)", "return False"],
                        "array", "is there any duplicate?");
      var seen = {}, keys = [], dup = 0;
      t.snap(0, "The set holds exactly the elements strictly before the current index. Trade memory for time: " +
                "every question about the past becomes O(1).",
             { aux: [{ label: "seen", items: [] }] });
      for (var i = 0; i < a.length; i++) {
        if (seen[a[i]]) {
          dup = 1;
          t.snap(2, a[i] + " is already in the set — duplicate found, stop. No sorting needed, so the O(n) " +
                    "budget survives.",
                 { ptr: { i: i }, mark: { [i]: "bad" }, aux: [{ label: "seen", items: strs(keys) }] });
          break;
        }
        t.snap(2, a[i] + " is not in the set yet.",
               { ptr: { i: i }, mark: { [i]: "pick" }, aux: [{ label: "seen", items: strs(keys) }] });
        seen[a[i]] = 1; keys.push(a[i]);
        t.snap(3, "add " + a[i] + ".",
               { ptr: { i: i }, mark: merge(range(0, i, "done")), aux: [{ label: "seen", items: strs(keys) }] });
      }
      if (!dup) t.snap(4, "Reached the end with no repeat — no duplicates.",
                       { aux: [{ label: "seen", items: strs(keys) }] });
      return { trace: t, answer: dup };
    }
  };

  G["hs-freq"] = {
    input: [{ id: "s", label: "string", type: "string", def: "aabbbc" }],
    brute: function (v) {
      var best = "", bn = 0, c = {};
      for (var i = 0; i < v.s.length; i++) c[v.s[i]] = (c[v.s[i]] || 0) + 1;
      for (var k in c) if (c[k] > bn) { bn = c[k]; best = k; }
      return best + bn;
    },
    run: function (v) {
      var s = v.s;
      var t = new Trace(s, ["cnt = Counter()", "for ch in s:", "    cnt[ch] += 1",
                            "most_common = max(cnt, key=cnt.get)"],
                        "string", "frequency map → the most common character");
      var cnt = {};
      t.snap(0, "The map is the exact multiset of what has been consumed so far.", { aux: [{ label: "counts", items: [] }] });
      for (var i = 0; i < s.length; i++) {
        cnt[s[i]] = (cnt[s[i]] || 0) + 1;
        t.snap(2, "'" + s[i] + "' → " + cnt[s[i]] + ".",
               { ptr: { i: i }, mark: merge(range(0, i - 1, "done"), { [i]: "pick" }),
                 aux: [{ label: "counts", items: kv(cnt, function (k, n) { return k + " × " + n; }) }] });
      }
      var best = "", bn = 0;
      for (var k in cnt) if (cnt[k] > bn) { bn = cnt[k]; best = k; }
      t.snap(3, "'" + best + "' wins with " + bn + ". One pass, and the same map answers anagram checks, " +
                "'can we rearrange', and top-K.",
             { mark: range(0, s.length - 1, "done"),
               aux: [{ label: "counts", items: kv(cnt, function (kk, n) { return kk + " × " + n; }) },
                     { label: "most common", text: best + " (" + bn + ")" }] });
      return { trace: t, answer: best + bn };
    }
  };

  G["hs-index"] = {
    input: [{ id: "a", label: "array", type: "ints", def: "2 7 11 15" },
            { id: "target", label: "target", type: "int", def: 9 }],
    brute: function (v) {
      for (var i = 0; i < v.a.length; i++)
        for (var j = i + 1; j < v.a.length; j++)
          if (v.a[i] + v.a[j] === v.target) return i + "," + j;
      return "";
    },
    run: function (v) {
      var a = v.a, target = v.target;
      var t = new Trace(a, ["pos = {}", "for i, x in enumerate(a):", "    if target - x in pos:",
                            "        return [pos[target-x], i]", "    pos[x] = i"],
                        "array", "two sum, unsorted — INDICES required");
      var pos = {}, ans = "";
      t.snap(0, "Sorting would find the pair but destroy the indices. A map keeps both.",
             { aux: [{ label: "value → index", items: [] }] });
      for (var i = 0; i < a.length; i++) {
        var need = target - a[i];
        t.snap(2, "a[" + i + "]=" + a[i] + " needs a partner of " + need + ".",
               { ptr: { i: i }, mark: { [i]: "pick" },
                 aux: [{ label: "value → index", items: kv(pos) }, { label: "looking for", text: String(need) }] });
        if (pos.hasOwnProperty(need)) {
          ans = pos[need] + "," + i;
          t.snap(3, "found it at index " + pos[need] + " — answer [" + ans + "]. Tested BEFORE inserting, " +
                    "or an element could pair with itself.",
                 { ptr: { i: i }, mark: { [i]: "done", [pos[need]]: "done" },
                   aux: [{ label: "answer", text: "[" + ans + "]" }] });
          break;
        }
        pos[a[i]] = i;
        t.snap(4, "no partner yet — record " + a[i] + " → " + i + " so a later element can find IT.",
               { ptr: { i: i }, aux: [{ label: "value → index", items: kv(pos) }] });
      }
      if (!ans) t.snap(1, "No pair sums to " + target + ".", {});
      return { trace: t, answer: ans };
    }
  };

  G["hs-cyclic"] = {
    input: [{ id: "a", label: "values in 1..n", type: "ints", def: "4 3 2 7 8 2 3 1" }],
    check: function (v) {
      for (var i = 0; i < v.a.length; i++)
        if (v.a[i] < 1 || v.a[i] > v.a.length) return "every value must be between 1 and " + v.a.length + " (the array length) — that is what lets the array be its own hashmap";
    },
    brute: function (v) {
      var out = [], seen = {};
      for (var i = 0; i < v.a.length; i++) seen[v.a[i]] = 1;
      for (var k = 1; k <= v.a.length; k++) if (!seen[k]) out.push(k);
      return out.join(",");
    },
    run: function (v) {
      var arr = v.a.slice(), n = arr.length, i;
      var t = new Trace(v.a, ["for i in range(n):", "    while a[i] != a[a[i]-1]:",
                              "        swap a[i] with a[a[i]-1]", "for i in range(n):",
                              "    if a[i] != i+1: anomaly"],
                        "array", "values are 1.." + n + " — the array IS the hashmap");
      t.snap(0, "No extra memory allowed. The trick: value v belongs at index v−1, so the array can store " +
                "its own lookup table.",
             { aux: [{ label: "array", items: strs(arr) }] });
      for (i = 0; i < n; i++) {
        while (arr[i] !== arr[arr[i] - 1]) {
          var j = arr[i] - 1, sw = arr[j];
          t.snap(2, "a[" + i + "]=" + arr[i] + " belongs at index " + j + ". Swap it home. A WHILE, not an if — " +
                    "the value you receive may also be out of place.",
                 { ptr: { i: i, home: j }, mark: { [i]: "pick", [j]: "bad" },
                   aux: [{ label: "array", items: strs(arr) }] });
          arr[j] = arr[i]; arr[i] = sw;
        }
      }
      t.snap(3, "Every value that can be home is home.", { aux: [{ label: "array", items: strs(arr) }] });
      var missing = [], mk = {};
      for (i = 0; i < n; i++) if (arr[i] !== i + 1) { missing.push(i + 1); mk[i] = "done"; }
      t.snap(4, missing.length
               ? ("Any index whose value does not match is the anomaly: " + missing.join(", ") +
                  " missing, and the values sitting there are the duplicates.")
               : "Every index matches — the array was a clean permutation of 1.." + n + ".",
             { mark: mk, aux: [{ label: "array", items: strs(arr) },
                                { label: "missing", items: missing.length ? strs(missing) : [] }] });
      return { trace: t, answer: missing.join(",") };
    }
  };

  /* =============================== STACK / HEAP ================================== */

  G["ms-next"] = {
    input: [{ id: "a", label: "temperatures", type: "ints", def: "73 74 75 71 69 76" }],
    brute: function (v) {
      var out = [];
      for (var i = 0; i < v.a.length; i++) {
        var d = 0;
        for (var j = i + 1; j < v.a.length; j++) if (v.a[j] > v.a[i]) { d = j - i; break; }
        out.push(d);
      }
      return out.join(",");
    },
    run: function (v) {
      var a = v.a;
      var t = new Trace(a, ["for i, x in enumerate(a):", "    while st and a[st[-1]] < x:",
                            "        res[st.pop()] = i - that", "    st.append(i)"],
                        "array", "days until it gets warmer");
      var st = [], res = [], i;
      for (i = 0; i < a.length; i++) res.push(0);
      for (i = 0; i < a.length; i++) {
        t.snap(0, "day " + i + ", temperature " + a[i] + ".",
               { ptr: { i: i }, aux: [{ label: "stack (indices)", items: strs(st) },
                                      { label: "waiting", items: st.map(function (j) { return String(a[j]); }) }] });
        while (st.length && a[st[st.length - 1]] < a[i]) {
          var j = st.pop();
          res[j] = i - j;
          t.snap(2, a[i] + " finally beats day " + j + "'s " + a[j] + " — that day is settled: " + (i - j) +
                    " day(s). Each index resolves exactly once, which is why this is O(n).",
                 { ptr: { i: i }, mark: { [j]: "done", [i]: "pick" },
                   aux: [{ label: "stack (indices)", items: strs(st) }, { label: "answers", items: strs(res) }] });
        }
        st.push(i);
        t.snap(3, "day " + i + " has no answer yet, so it waits on the stack. The stack is always decreasing — " +
                  "it holds only the days that could still be waiting.",
               { ptr: { i: i }, aux: [{ label: "stack (indices)", items: strs(st) },
                                      { label: "temperatures", items: st.map(function (k) { return String(a[k]); }) }] });
      }
      t.snap(3, "Leftovers keep 0 — it never gets warmer for them.",
             { aux: [{ label: "answers", items: strs(res) }] });
      return { trace: t, answer: res.join(",") };
    }
  };

  G["ms-hist"] = {
    input: [{ id: "h", label: "bar heights", type: "ints", def: "2 1 5 6 2 3" }],
    check: function (v) {
      for (var i = 0; i < v.h.length; i++) if (v.h[i] < 0) return "heights cannot be negative";
    },
    brute: function (v) {
      var best = 0;
      for (var i = 0; i < v.h.length; i++) {
        var m = v.h[i];
        for (var j = i; j < v.h.length; j++) {
          if (v.h[j] < m) m = v.h[j];
          if (m * (j - i + 1) > best) best = m * (j - i + 1);
        }
      }
      return best;
    },
    run: function (v) {
      var h = v.h;
      var t = new Trace(h, ["for i, x in enumerate(h + [0]):", "    while st and h[st[-1]] > x:",
                            "        height = h[st.pop()]", "        left = st[-1] + 1 if st else 0",
                            "        best = max(best, height * (i - left))", "    st.append(i)"],
                        "array", "largest rectangle in a histogram");
      var st = [], best = 0;
      for (var i = 0; i <= h.length; i++) {
        var x = (i === h.length) ? 0 : h[i];
        if (i === h.length) t.snap(0, "The sentinel 0 arrives — it exists only to flush whatever is still " +
                                      "on the stack.", { ptr: { i: i } });
        while (st.length && h[st[st.length - 1]] > x) {
          var height = h[st.pop()];
          var left = st.length ? st[st.length - 1] + 1 : 0;
          var area = height * (i - left);
          if (area > best) best = area;
          t.snap(4, "bar " + height + " is finished: a shorter bar appeared at " + i + ". Width spans [" + left +
                    ".." + (i - 1) + "] → " + height + " × " + (i - left) + " = " + area +
                    ". The width uses the NEW stack top, not the popped index — the classic bug here.",
                 { ptr: { i: i }, span: [left, i - 1], mark: range(left, i - 1, "pick"),
                   aux: [{ label: "stack (indices)", items: strs(st) },
                         { label: "area", text: height + " × " + (i - left) + " = " + area },
                         { label: "best", text: String(best) }] });
        }
        st.push(i);
        if (i < h.length) {
          t.snap(5, "push bar " + i + " (height " + x + "). The stack stays increasing.",
                 { ptr: { i: i }, aux: [{ label: "stack (indices)", items: strs(st) }] });
        }
      }
      t.snap(4, "Answer " + best + ".", { aux: [{ label: "best", text: String(best) }] });
      return { trace: t, answer: best };
    }
  };

  G["ms-match"] = {
    input: [{ id: "s", label: "brackets", type: "string", def: "([{}])()" }],
    check: function (v) {
      if (!/^[()\[\]{}]*$/.test(v.s)) return "use only ( ) [ ] { }";
    },
    brute: function (v) {
      var s = v.s, prev = null;
      while (s !== prev) { prev = s; s = s.replace(/\(\)|\[\]|\{\}/g, ""); }
      return s === "" ? 1 : 0;
    },
    run: function (v) {
      var s = v.s;
      var t = new Trace(s, ["for ch in s:", "    if ch is a closer:", "        if not st or st.pop() != match: False",
                            "    else: st.append(ch)", "return not st"],
                        "string", "valid parentheses");
      var pair = { ")": "(", "]": "[", "}": "{" };
      var st = [], ok = 1;
      t.snap(0, "The stack is exactly the list of things still unclosed, innermost on top.",
             { aux: [{ label: "stack", items: [] }] });
      for (var i = 0; i < s.length; i++) {
        var ch = s[i];
        if (pair[ch]) {
          if (!st.length) {
            ok = 0;
            t.snap(2, "'" + ch + "' closes something that was never opened — and checking the stack is " +
                      "non-empty BEFORE popping is half the grade.",
                   { ptr: { i: i }, mark: { [i]: "bad" }, aux: [{ label: "stack", items: strs(st) }] });
            break;
          }
          var top = st.pop();
          if (top !== pair[ch]) {
            ok = 0;
            t.snap(2, "'" + ch + "' does not match the open '" + top + "' — wrong kind of bracket.",
                   { ptr: { i: i }, mark: { [i]: "bad" }, aux: [{ label: "stack", items: strs(st) }] });
            break;
          }
          t.snap(2, "'" + ch + "' matches the open '" + top + "' — pop it, that pair is resolved.",
                 { ptr: { i: i }, mark: { [i]: "done" }, aux: [{ label: "stack", items: strs(st) }] });
        } else {
          st.push(ch);
          t.snap(3, "'" + ch + "' opens — push it and wait.",
                 { ptr: { i: i }, mark: { [i]: "pick" }, aux: [{ label: "stack", items: strs(st) }] });
        }
      }
      if (ok) {
        ok = st.length ? 0 : 1;
        t.snap(4, st.length ? ("Reached the end but " + st.length + " bracket(s) are still open — invalid. " +
                               "The empty-at-the-end check is the other half of the grade.")
                            : "Reached the end with an empty stack — valid.",
               { aux: [{ label: "stack", items: strs(st) }] });
      }
      return { trace: t, answer: ok };
    }
  };

  G["ms-greedy"] = {
    input: [{ id: "num", label: "digits", type: "digits", def: "1432219" },
            { id: "k", label: "remove k", type: "int", def: 3 }],
    check: function (v) {
      if (v.k < 0) return "k cannot be negative";
      if (v.k > v.num.length) return "k must be ≤ the number of digits";
    },
    brute: function (v) {
      var best = null;
      var pick = function (idx, left, acc) {
        if (left === 0) { acc += v.num.slice(idx); if (best === null || cmp(acc, best) < 0) best = acc; return; }
        if (idx >= v.num.length) return;
        pick(idx + 1, left - 1, acc);
        pick(idx + 1, left, acc + v.num[idx]);
      };
      var cmp = function (x, y) {
        var a = x.replace(/^0+/, "") || "0", b = y.replace(/^0+/, "") || "0";
        if (a.length !== b.length) return a.length - b.length;
        return a < b ? -1 : (a > b ? 1 : 0);
      };
      pick(0, v.k, "");
      return (best || "").replace(/^0+/, "") || "0";
    },
    run: function (v) {
      var num = v.num, k = v.k, budget = k;
      var t = new Trace(num, ["for ch in num:", "    while k and st and st[-1] > ch:", "        st.pop(); k -= 1",
                              "    st.append(ch)", "st = st[:len(st)-k]  # budget unspent"],
                        "string", "remove " + k + " digits to make the smallest number");
      var st = [];
      t.snap(0, "The stack holds the best prefix achievable with the removals spent so far.",
             { aux: [{ label: "removals left", text: String(budget) }, { label: "stack", items: [] }] });
      for (var i = 0; i < num.length; i++) {
        var ch = num[i];
        while (budget > 0 && st.length && st[st.length - 1] > ch) {
          t.snap(1, "'" + st[st.length - 1] + "' sits before the smaller '" + ch +
                    "' — a bigger digit earlier is always worse, so drop it.",
                 { ptr: { i: i }, mark: { [i]: "pick" },
                   aux: [{ label: "removals left", text: String(budget) }, { label: "stack", items: st.slice() }] });
          st.pop(); budget--;
        }
        st.push(ch);
        t.snap(3, "keep '" + ch + "'.",
               { ptr: { i: i }, mark: { [i]: "done" },
                 aux: [{ label: "removals left", text: String(budget) }, { label: "stack", items: st.slice() }] });
      }
      if (budget > 0) {
        t.snap(4, "budget still has " + budget + " left, and what remains is non-decreasing — so trim from " +
                  "the BACK.",
               { aux: [{ label: "stack", items: st.slice() }] });
        st = st.slice(0, st.length - budget);
      }
      var ans = st.join("").replace(/^0+/, "") || "0";
      t.snap(4, "Answer " + ans + ". Leading zeros and the empty result both need an explicit fallback.",
             { aux: [{ label: "answer", text: ans }] });
      return { trace: t, answer: ans };
    }
  };

  G["hp-topk"] = {
    input: [{ id: "a", label: "array", type: "ints", def: "3 2 1 5 6 4" },
            { id: "k", label: "k", type: "int", def: 3 }],
    check: function (v) {
      if (v.k < 1 || v.k > v.a.length) return "k must be between 1 and the array length";
    },
    brute: function (v) {
      var s = v.a.slice().sort(function (x, y) { return y - x; });
      return s[v.k - 1];
    },
    run: function (v) {
      var a = v.a, k = v.k;
      var t = new Trace(a, ["for x in a:", "    heappush(h, x)", "    if len(h) > k:", "        heappop(h)",
                            "return h[0]  # the k-th largest"],
                        "array", "k = " + k + ", keep only the " + k + " largest");
      var h = [];
      function push(x) { h.push(x); h.sort(function (p, q) { return p - q; }); }
      t.snap(0, "A MIN-heap for the k LARGEST — the weakest survivor sits on top, ready to be evicted. " +
                "Inverting this is the classic slip.",
             { aux: [{ label: "heap", items: [] }] });
      for (var i = 0; i < a.length; i++) {
        push(a[i]);
        t.snap(1, "push " + a[i] + ".",
               { ptr: { i: i }, mark: { [i]: "pick" }, aux: [{ label: "heap (min on top)", items: strs(h) }] });
        if (h.length > k) {
          t.snap(3, "heap holds " + h.length + " > k, so evict the smallest (" + h[0] +
                    ") — it can no longer be one of the " + k + " largest.",
                 { ptr: { i: i }, aux: [{ label: "heap (min on top)", items: strs(h) },
                                        { label: "evicting", text: String(h[0]) }] });
          h.shift();
          t.snap(3, "heap back to size " + k + ".",
                 { ptr: { i: i }, aux: [{ label: "heap (min on top)", items: strs(h) }] });
        }
      }
      t.snap(4, "Answer: the " + k + "-th largest is " + h[0] + ". Space O(k), time O(n log k) — beating a " +
                "full O(n log n) sort.",
             { aux: [{ label: "heap", items: strs(h) }, { label: "answer", text: String(h[0]) }] });
      return { trace: t, answer: h[0] };
    }
  };

  /* ================================== INTERVALS =================================== */

  function clockCells(iv) {
    var hi = 0;
    for (var i = 0; i < iv.length; i++) if (iv[i][1] > hi) hi = iv[i][1];
    var cells = [];
    for (var j = 1; j <= hi; j++) cells.push(j);
    return cells;
  }

  G["iv-greedy"] = {
    input: [{ id: "iv", label: "meetings  start,end", type: "pairs", def: "1,3 2,5 4,6 6,8 7,9" }],
    check: function (v) {
      if (!v.iv.length) return "give at least one meeting";
      for (var i = 0; i < v.iv.length; i++) {
        /* a meeting must occupy time: with start == end the 'next may start at my end'
           rule lets you take unlimited copies of it, which is not a real problem */
        if (v.iv[i][0] >= v.iv[i][1]) return "each meeting needs start < end";
        if (v.iv[i][0] < 1) return "start times must be 1 or more (the clock starts at 1)";
      }
    },
    brute: function (v) {
      var best = 0;
      var go = function (i, lastEnd, n) {
        if (i === v.iv.length) { if (n > best) best = n; return; }
        go(i + 1, lastEnd, n);
        if (v.iv[i][0] >= lastEnd) go(i + 1, v.iv[i][1], n + 1);
      };
      var srt = v.iv.slice().sort(function (a, b) { return a[0] - b[0]; });
      v = { iv: srt };
      go(0, -Infinity, 0);
      return best;
    },
    run: function (v) {
      var iv = v.iv;
      var t = new Trace(clockCells(iv), ["intervals.sort(key=lambda x: x[1])", "for s, e in intervals:",
                                         "    if s >= last_end:", "        count += 1; last_end = e"],
                        "timeline", "maximum non-overlapping meetings (cells are the clock)");
      var order = iv.slice().sort(function (a, b) { return a[1] - b[1]; });
      t.snap(0, "Sort by END time. Sorting by start passes the samples and fails the hidden tests — this is " +
                "a graded trap.",
             { aux: [{ label: "sorted by end", items: order.map(function (p) { return "[" + p[0] + "," + p[1] + "]"; }) }] });
      var count = 0, lastEnd = -Infinity, taken = [];
      for (var i = 0; i < order.length; i++) {
        var s = order[i][0], e = order[i][1];
        if (s >= lastEnd) {
          count++; lastEnd = e; taken.push("[" + s + "," + e + "]");
          t.snap(3, "take [" + s + "," + e + "] — finishing earliest always leaves the most room for " +
                    "everything after: that is the exchange argument.",
                 { span: [s - 1, e - 1], mark: range(s - 1, e - 1, "pick"),
                   aux: [{ label: "taken", items: taken.slice() }, { label: "count", text: String(count) }] });
        } else {
          t.snap(2, "skip [" + s + "," + e + "] — it starts before " + lastEnd + ", so it clashes with what " +
                    "we already took.",
                 { span: [s - 1, e - 1], mark: range(s - 1, e - 1, "bad"),
                   aux: [{ label: "taken", items: taken.slice() }, { label: "count", text: String(count) }] });
        }
      }
      t.snap(3, "Answer " + count + " meeting(s). Removals = " + iv.length + " − " + count + " = " +
                (iv.length - count) + ".",
             { aux: [{ label: "count", text: String(count) }] });
      return { trace: t, answer: count };
    }
  };

  G["iv-merge"] = {
    input: [{ id: "iv", label: "intervals  start,end", type: "pairs", def: "1,3 2,6 8,10 15,18" }],
    check: function (v) {
      if (!v.iv.length) return "give at least one interval";
      for (var i = 0; i < v.iv.length; i++) {
        if (v.iv[i][0] > v.iv[i][1]) return "each interval needs start ≤ end";
        if (v.iv[i][0] < 1) return "start times must be 1 or more (the clock starts at 1)";
      }
    },
    brute: function (v) {
      /* Independent check: union-find over PAIRWISE overlap, then each component's extent.
         (Cell coverage would be wrong here -- it fuses [1,1] and [2,2], which are adjacent
         but do not overlap, and the standard definition keeps those separate.) */
      var n = v.iv.length, p = [], i, j;
      for (i = 0; i < n; i++) p.push(i);
      function find(x) { while (p[x] !== x) { p[x] = p[p[x]]; x = p[x]; } return x; }
      for (i = 0; i < n; i++)
        for (j = i + 1; j < n; j++)
          if (v.iv[i][0] <= v.iv[j][1] && v.iv[j][0] <= v.iv[i][1]) p[find(i)] = find(j);
      var comp = {};
      for (i = 0; i < n; i++) {
        var r = find(i);
        if (!comp[r]) comp[r] = [v.iv[i][0], v.iv[i][1]];
        else {
          comp[r][0] = Math.min(comp[r][0], v.iv[i][0]);
          comp[r][1] = Math.max(comp[r][1], v.iv[i][1]);
        }
      }
      var out = [];
      for (var k in comp) out.push(comp[k]);
      out.sort(function (a, b) { return a[0] - b[0]; });
      return out.map(function (x) { return x[0] + "-" + x[1]; }).join(",");
    },
    run: function (v) {
      var iv = v.iv;
      var t = new Trace(clockCells(iv), ["intervals.sort(key=lambda x: x[0])", "for s, e in intervals:",
                                         "    if out and s <= out[-1][1]:",
                                         "        out[-1][1] = max(out[-1][1], e)", "    else: out.append([s, e])"],
                        "timeline", "merge overlapping intervals");
      var order = iv.slice().sort(function (a, b) { return a[0] - b[0]; });
      t.snap(0, "Sort by START. Once they are in order, each interval only ever has to be compared with the " +
                "PREVIOUS one — that is what turns O(n²) into one pass.",
             { aux: [{ label: "sorted by start", items: order.map(function (p) { return "[" + p[0] + "," + p[1] + "]"; }) }] });
      var out = [];
      for (var i = 0; i < order.length; i++) {
        var s = order[i][0], e = order[i][1];
        if (out.length && s <= out[out.length - 1][1]) {
          var old = out[out.length - 1][1];
          out[out.length - 1][1] = Math.max(old, e);
          t.snap(3, "[" + s + "," + e + "] starts at or before the open block's end (" + old +
                    ") — so extend it to " + out[out.length - 1][1] + ". max(), not e: assigning e blindly " +
                    "would SHRINK a block that already reached further.",
                 { span: [out[out.length - 1][0] - 1, out[out.length - 1][1] - 1],
                   mark: range(out[out.length - 1][0] - 1, out[out.length - 1][1] - 1, "pick"),
                   aux: [{ label: "merged", items: out.map(function (p) { return "[" + p[0] + "," + p[1] + "]"; }) }] });
        } else {
          out.push([s, e]);
          t.snap(4, "[" + s + "," + e + "] does not touch the previous block — start a new one.",
                 { span: [s - 1, e - 1], mark: range(s - 1, e - 1, "done"),
                   aux: [{ label: "merged", items: out.map(function (p) { return "[" + p[0] + "," + p[1] + "]"; }) }] });
        }
      }
      var mk = {}, ans = [];
      for (i = 0; i < out.length; i++) {
        for (var j = out[i][0]; j <= out[i][1]; j++) mk[j - 1] = "done";
        ans.push(out[i][0] + "-" + out[i][1]);
      }
      t.snap(3, "Answer " + out.map(function (p) { return "[" + p[0] + "," + p[1] + "]"; }).join(" ") +
                ". Whether touching ends count as overlapping is always stated — check the samples.",
             { mark: mk, aux: [{ label: "merged", items: ans.slice() }] });
      return { trace: t, answer: ans.join(",") };
    }
  };

  G["iv-sweep"] = {
    input: [{ id: "iv", label: "bookings  start,end", type: "pairs", def: "1,4 2,6 3,5 7,9" }],
    check: function (v) {
      if (!v.iv.length) return "give at least one booking";
      for (var i = 0; i < v.iv.length; i++) {
        if (v.iv[i][0] > v.iv[i][1]) return "each booking needs start ≤ end";
        if (v.iv[i][0] < 1) return "start times must be 1 or more";
      }
    },
    brute: function (v) {
      var hi = 0, i, tt;
      for (i = 0; i < v.iv.length; i++) if (v.iv[i][1] > hi) hi = v.iv[i][1];
      var best = 0;
      for (tt = 1; tt <= hi; tt++) {
        var c = 0;
        for (i = 0; i < v.iv.length; i++) if (v.iv[i][0] <= tt && tt < v.iv[i][1]) c++;
        if (c > best) best = c;
      }
      return best;
    },
    run: function (v) {
      var iv = v.iv;
      var t = new Trace(clockCells(iv), ["for s, e in intervals:", "    ev.append((s, +1)); ev.append((e, -1))",
                                         "ev.sort()      # at equal times, -1 first", "for time, delta in ev:",
                                         "    cur += delta; best = max(best, cur)"],
                        "timeline", "peak concurrency — how many rooms are needed");
      var ev = [];
      for (var i = 0; i < iv.length; i++) { ev.push([iv[i][0], 1]); ev.push([iv[i][1], -1]); }
      t.snap(1, "Every interval becomes TWO events: an arrival (+1) and a departure (−1).",
             { aux: [{ label: "events", items: ev.map(function (e) { return e[0] + (e[1] > 0 ? "+" : "−"); }) }] });
      ev.sort(function (a, b) { return (a[0] - b[0]) || (a[1] - b[1]); });
      t.snap(2, "Sort them. At an equal timestamp the −1 sorts first, so someone leaving at t frees the slot " +
                "for someone arriving at t — that tie-break IS the correctness.",
             { aux: [{ label: "sorted events", items: ev.map(function (e) { return e[0] + (e[1] > 0 ? "+" : "−"); }) }] });
      var cur = 0, best = 0;
      for (i = 0; i < ev.length; i++) {
        cur += ev[i][1];
        if (cur > best) best = cur;
        t.snap(4, "t = " + ev[i][0] + ": " + (ev[i][1] > 0 ? "someone arrives" : "someone leaves") +
                  " → " + cur + " active. peak = " + best + ".",
               { span: [ev[i][0] - 1, ev[i][0] - 1], mark: { [ev[i][0] - 1]: ev[i][1] > 0 ? "pick" : "gone" },
                 aux: [{ label: "active", text: String(cur) }, { label: "peak", text: String(best) }] });
      }
      t.snap(4, "Answer " + best + ". Same object as a difference array — recognise them as one pattern.",
             { aux: [{ label: "peak", text: String(best) }] });
      return { trace: t, answer: best };
    }
  };

  /* ===================================== BITS ===================================== */

  G["bt-xor"] = {
    input: [{ id: "a", label: "array (pairs + one single)", type: "ints", def: "4 1 2 1 2" }],
    brute: function (v) {
      var c = {};
      for (var i = 0; i < v.a.length; i++) c[v.a[i]] = (c[v.a[i]] || 0) + 1;
      for (var k in c) if (c[k] % 2 === 1) return Number(k);
      return 0;
    },
    run: function (v) {
      var a = v.a;
      var width = Math.max(3, Math.max.apply(null, a.concat([1])).toString(2).length);
      function bin(x) {
        var s = (x >>> 0).toString(2);
        while (s.length < width) s = "0" + s;
        return s;
      }
      var t = new Trace(a, ["r = 0", "for x in a:", "    r ^= x", "return r"],
                        "array", "everything appears twice except one");
      var r = 0;
      t.snap(0, "Two facts do all the work: x ^ x = 0, and x ^ 0 = x. So pairs erase themselves.",
             { aux: [{ label: "r", text: "0" }, { label: "binary", text: bin(0) }] });
      for (var i = 0; i < a.length; i++) {
        var prev = r;
        r ^= a[i];
        t.snap(2, "r = " + prev + " ^ " + a[i] + " = " + r + "   (" + bin(prev) + " ^ " + bin(a[i]) + " = " + bin(r) + ")",
               { ptr: { i: i }, mark: { [i]: "pick" },
                 aux: [{ label: "r", text: String(r) }, { label: "binary", text: bin(r) }] });
      }
      t.snap(3, "Answer " + r + ". Order never mattered — XOR is commutative, so pairs cancel wherever they " +
                "sit. O(1) space, no hashmap.",
             { aux: [{ label: "r", text: String(r) }] });
      return { trace: t, answer: r };
    }
  };

  G["bt-subsets"] = {
    input: [{ id: "a", label: "items (keep it small)", type: "ints", def: "5 7 9" }],
    check: function (v) {
      if (v.a.length > 5) return "2ⁿ grows fast — keep it to 5 items or fewer so the trace stays watchable";
      if (!v.a.length) return "give at least one item";
    },
    brute: function (v) { return Math.pow(2, v.a.length); },
    run: function (v) {
      var a = v.a, n = a.length;
      var t = new Trace(a, ["for mask in range(1 << n):", "    pick = [a[i] for i in range(n)",
                            "            if mask >> i & 1]"],
                        "array", "an integer IS a subset — bit i means 'item i is in'");
      t.snap(0, "n = " + n + ", so there are 2^" + n + " = " + Math.pow(2, n) + " masks, and each one is exactly " +
                "one subset. 'n ≤ 20' in the constraints is announcing this.",
             { aux: [{ label: "masks", text: "0 .. " + (Math.pow(2, n) - 1) }] });
      var count = 0;
      for (var mask = 0; mask < (1 << n); mask++) {
        var pick = [], mk = {}, bits = "";
        for (var i = 0; i < n; i++) {
          if (mask >> i & 1) { pick.push(a[i]); mk[i] = "pick"; }
          bits = ((mask >> i & 1) ? "1" : "0") + bits;
        }
        count++;
        t.snap(1, "mask " + mask + " = " + bits + " → { " + (pick.join(", ") || "∅") + " }",
               { mark: mk, aux: [{ label: "mask", text: mask + " = " + bits },
                                 { label: "subset", items: pick.length ? strs(pick) : [] }] });
      }
      t.snap(2, "All " + count + " subsets, no recursion and no bookkeeping — just a counter.",
             { aux: [{ label: "subsets", text: String(count) }] });
      return { trace: t, answer: count };
    }
  };

  /* ---------------------------------------------------------------------------------
     INPUT PARSERS -- defined ONCE here and used by BOTH the page and viz_test.js. Keeping
     two copies is how you end up with a generator the fuzzer accepts and the page cannot
     parse, which is exactly the bug this consolidation removes. Each throws a message meant
     to be shown to the user as-is.
     --------------------------------------------------------------------------------- */
  var parse = {
    ints: function (s) {
      var parts = String(s).trim().split(/[\s,]+/).filter(function (x) { return x.length; });
      var out = [];
      for (var i = 0; i < parts.length; i++) {
        var n = Number(parts[i]);
        if (!isFinite(n) || parts[i].indexOf(".") >= 0) throw new Error("'" + parts[i] + "' is not a whole number");
        out.push(n);
      }
      if (!out.length) throw new Error("give me some numbers, separated by spaces");
      if (out.length > 16) throw new Error("keep it to 16 numbers or fewer so the trace stays watchable");
      return out;
    },
    string: function (s) {
      var t = String(s).trim();
      if (!t.length) throw new Error("type a string");
      if (t.length > 18) throw new Error("keep it to 18 characters or fewer");
      return t;
    },
    digits: function (s) {
      var t = String(s).trim();
      if (!/^\d+$/.test(t)) throw new Error("digits only");
      if (t.length > 14) throw new Error("keep it to 14 digits or fewer");
      return t;
    },
    int: function (s) {
      var n = Number(String(s).trim());
      if (!isFinite(n) || String(s).trim() === "") throw new Error("that is not a number");
      return Math.round(n);
    },
    pairs: function (s) {
      var groups = String(s).trim().split(/\s+/).filter(function (x) { return x.length; });
      if (!groups.length) throw new Error("give pairs like  1,3 2,5");
      if (groups.length > 12) throw new Error("keep it to 12 pairs or fewer");
      return groups.map(function (g) {
        var p = g.split(",").map(Number);
        if (p.length !== 2 || !isFinite(p[0]) || !isFinite(p[1])) throw new Error("'" + g + "' should look like  2,5");
        return p;
      });
    },
    triples: function (s) {
      var groups = String(s).trim().split(/\s+/).filter(function (x) { return x.length; });
      if (!groups.length) throw new Error("give triples like  1,3,2");
      if (groups.length > 12) throw new Error("keep it to 12 entries or fewer");
      return groups.map(function (g) {
        var p = g.split(",").map(Number);
        if (p.length !== 3 || !isFinite(p[0]) || !isFinite(p[1]) || !isFinite(p[2]))
          throw new Error("'" + g + "' should look like  1,3,2  (three numbers)");
        return p;
      });
    },
    quad: function (s) {
      var p = String(s).trim().split(",").map(Number);
      if (p.length !== 4 || p.some(function (x) { return !isFinite(x); }))
        throw new Error("give four numbers like  1,0,2,1  (r1,c1,r2,c2)");
      return p;
    },
    rows: function (s) {
      var groups = String(s).trim().split(/\s+/).filter(function (x) { return x.length; });
      if (!groups.length) throw new Error("give one comma-separated list per row, like  1,4,5 1,3,4");
      if (groups.length > 6) throw new Error("keep it to 6 rows or fewer");
      return groups.map(function (g) {
        var p = g.split(",").map(Number);
        if (!p.length || p.some(function (x) { return !isFinite(x); }))
          throw new Error("'" + g + "' should be numbers separated by commas, like  1,4,5");
        return p;
      });
    },
    tree: function (s) {
      var parts = String(s).trim().split(/[\s,]+/).filter(function (x) { return x.length; });
      if (!parts.length) throw new Error("give the tree in level order, like  3 9 20 . . 15 7  (. = empty)");
      if (parts.length > 20) throw new Error("keep it to 20 slots or fewer so the drawing stays readable");
      return parts.map(function (x) {
        if (x === "." || x.toLowerCase() === "null") return null;
        var n = Number(x);
        if (!isFinite(n)) throw new Error("'" + x + "' is neither a number nor '.' for empty");
        return n;
      });
    },
    words: function (s) {
      var w = String(s).trim().toLowerCase().split(/[\s,]+/).filter(function (x) { return x.length; });
      if (!w.length) throw new Error("give one or more words, separated by spaces");
      return w;
    },
    word: function (s) { return String(s).trim().toLowerCase(); },
    letters: function (s) {
      var rows = String(s).trim().toLowerCase().split(/\s+/).filter(function (x) { return x.length; });
      if (!rows.length) throw new Error("give one row of letters per board row, like  oaa eto ihk");
      return rows;
    },
    grid01: function (s) {
      var rows = String(s).trim().split(/\s+/).filter(function (x) { return x.length; });
      if (!rows.length) throw new Error("give one row per line of the grid, like  1100 0010");
      var w = rows[0].length;
      return rows.map(function (row) {
        if (row.length !== w) throw new Error("every row must be the same length (got '" + row + "')");
        return row.split("").map(function (ch) {
          if (ch !== "0" && ch !== "1") throw new Error("use only 0 and 1 (got '" + ch + "')");
          return ch === "1" ? 1 : 0;
        });
      });
    },
    gridnum: function (s) {
      var rows = String(s).trim().split(/\s+/).filter(function (x) { return x.length; });
      if (!rows.length) throw new Error("give one row of single digits per line, like  131 151 422");
      var w = rows[0].length;
      return rows.map(function (row) {
        if (row.length !== w) throw new Error("every row must be the same length (got '" + row + "')");
        return row.split("").map(function (ch) {
          var n = Number(ch);
          if (!isFinite(n)) throw new Error("use single digits 0-9 (got '" + ch + "')");
          return n;
        });
      });
    }
  };

  /* viz_engine_b.js registers more generators onto this same object, so it needs the
     helpers. Keys starting with __ are plumbing, not generators; the test skips them. */
  G.__helpers = { Trace: Trace, range: range, merge: merge, kv: kv, strs: strs, parse: parse };

  if (typeof module !== "undefined" && module.exports) module.exports = G;
  if (typeof window !== "undefined") window.VIZGEN = G;
})();
