/* =====================================================================================
   VIZ ENGINE, part D  --  the TREE stage.
   Tree DFS (up, down, BST, LCA), tree BFS, and the trie. The tree is entered as a
   level-order list with "." for a missing child, the same way judges print them.
   ===================================================================================== */
(function () {
  "use strict";
  var G = (typeof module !== "undefined" && module.exports)
        ? require("./viz_engine.js")
        : window.VIZGEN;
  var H = G.__helpers, Trace = H.Trace, merge = H.merge, strs = H.strs;

  /* Build {nodes, root} from a level-order array with nulls, LeetCode style. */
  function buildTree(level) {
    var nodes = [], queue = [], i = 0;
    if (!level.length || level[0] === null) return { nodes: [], root: -1 };
    nodes.push({ v: level[0], l: -1, r: -1 });
    queue.push(0);
    i = 1;
    while (queue.length && i < level.length) {
      var cur = queue.shift();
      if (i < level.length) {
        if (level[i] !== null) { nodes.push({ v: level[i], l: -1, r: -1 }); nodes[cur].l = nodes.length - 1; queue.push(nodes.length - 1); }
        i++;
      }
      if (i < level.length) {
        if (level[i] !== null) { nodes.push({ v: level[i], l: -1, r: -1 }); nodes[cur].r = nodes.length - 1; queue.push(nodes.length - 1); }
        i++;
      }
    }
    return { nodes: nodes, root: 0 };
  }
  function treeTrace(tree, code, caption) {
    return new Trace({ nodes: tree.nodes, root: tree.root }, code, "tree", caption);
  }
  function allMark(n, state) { var m = {}; for (var i = 0; i < n; i++) m[String(i)] = state; return m; }

  var TREE_FIELD = { id: "t", label: "tree, level order (. = empty)", type: "tree", def: "3 9 20 . . 15 7" };

  function checkTree(v) {
    if (!v.t.length || v.t[0] === null) return "the tree needs a root value";
    var t = buildTree(v.t);
    if (t.nodes.length > 15) return "keep it to 15 nodes or fewer so the drawing stays readable";
    return null;
  }

  /* =================================== TREE DFS =================================== */

  G["td-up"] = {
    input: [TREE_FIELD],
    check: checkTree,
    brute: function (v) {              /* height by repeated level counting -- not recursion */
      var t = buildTree(v.t);
      if (!t.nodes.length) return 0;
      var layer = [t.root], h = 0;
      while (layer.length) {
        h++;
        var nxt = [];
        for (var i = 0; i < layer.length; i++) {
          var nd = t.nodes[layer[i]];
          if (nd.l >= 0) nxt.push(nd.l);
          if (nd.r >= 0) nxt.push(nd.r);
        }
        layer = nxt;
      }
      return h;
    },
    run: function (v) {
      var tree = buildTree(v.t), nodes = tree.nodes;
      var t = treeTrace(tree, ["def height(node):", "    if not node: return 0        # the base case IS the empty tree",
                               "    l = height(node.left)", "    r = height(node.right)",
                               "    return 1 + max(l, r)         # combine, then report upward"],
                        "height — information flows UP from the children");
      var settled = {};
      t.snap(0, "Post-order: ask both children first, combine their answers, then report one value upward. " +
                "By the time you combine, both subtrees have already answered correctly.", {});
      function go(i) {
        if (i < 0) return 0;
        t.snap(2, "descend into node " + nodes[i].v + " — nothing can be decided here until both children report.",
               { ptr: { at: String(i) }, mark: merge(settled, { [String(i)]: "pick" }) });
        var l = go(nodes[i].l), r = go(nodes[i].r);
        var h = 1 + Math.max(l, r);
        settled[String(i)] = "done";
        t.snap(4, "node " + nodes[i].v + ": left reported " + l + ", right reported " + r +
                  " → height here is 1 + max(" + l + ", " + r + ") = " + h + ". Report that up.",
               { ptr: { at: String(i) }, mark: merge(settled, { [String(i)]: "pick" }),
                 aux: [{ label: "left", text: String(l) }, { label: "right", text: String(r) },
                       { label: "returns", text: String(h) }] });
        return h;
      }
      var ans = go(tree.root);
      t.snap(4, "Answer " + ans + ". Each node was visited once, so O(n), and the recursion stack did all " +
                "the bookkeeping for free.",
             { mark: allMark(nodes.length, "done"), aux: [{ label: "height", text: String(ans) }] });
      return { trace: t, answer: ans };
    }
  };

  G["td-down"] = {
    input: [TREE_FIELD, { id: "target", label: "target path sum", type: "int", def: 12 }],
    check: checkTree,
    brute: function (v) {              /* enumerate every root-to-leaf path */
      var t = buildTree(v.t), found = 0;
      (function go(i, s) {
        if (i < 0) return;
        s += t.nodes[i].v;
        if (t.nodes[i].l < 0 && t.nodes[i].r < 0) { if (s === v.target) found++; return; }
        go(t.nodes[i].l, s); go(t.nodes[i].r, s);
      })(t.root, 0);
      return found;
    },
    run: function (v) {
      var tree = buildTree(v.t), nodes = tree.nodes, target = v.target;
      var t = treeTrace(tree, ["def go(node, remaining, path):", "    if not node: return",
                               "    path.append(node.val)", "    if leaf and node.val == remaining:",
                               "        record a copy of path", "    go(node.left,  remaining - node.val, path)",
                               "    go(node.right, remaining - node.val, path)",
                               "    path.pop()                   # undo on the way out"],
                        "root-to-leaf paths summing to " + target);
      var onPath = {}, found = 0, hits = [];
      t.snap(0, "Top-down: the parent hands the child its context — here, how much target is left. " +
                "Compare with the height trace, where the value flowed the other way.", {});
      function go(i, remaining, path) {
        if (i < 0) return;
        path.push(nodes[i].v);
        onPath[String(i)] = "pick";
        var isLeaf = nodes[i].l < 0 && nodes[i].r < 0;
        t.snap(2, "at node " + nodes[i].v + ": path so far [" + path.join(", ") + "], still need " +
                  remaining + (isLeaf ? ". This is a LEAF — no left AND no right." : "."),
               { ptr: { at: String(i) }, mark: merge(onPath),
                 aux: [{ label: "path", items: strs(path) }, { label: "need", text: String(remaining) }] });
        if (isLeaf && nodes[i].v === remaining) {
          found++;
          hits.push(path.join("→"));
          t.snap(4, "the leaf exactly finishes the target — record a COPY of the path. Recording the live " +
                    "list instead would leave you with identical empty answers.",
                 { ptr: { at: String(i) }, mark: merge(onPath, { [String(i)]: "done" }),
                   aux: [{ label: "found", text: String(found) }, { label: "paths", items: hits.slice() }] });
        } else if (!isLeaf) {
          go(nodes[i].l, remaining - nodes[i].v, path);
          go(nodes[i].r, remaining - nodes[i].v, path);
        }
        path.pop();
        delete onPath[String(i)];
        t.snap(7, "leaving node " + nodes[i].v + " — pop it off the path before returning to the parent. " +
                  "Forgetting this pop is the classic backtracking leak.",
               { mark: merge(onPath), aux: [{ label: "path", items: strs(path) }] });
      }
      go(tree.root, target, []);
      t.snap(4, "Answer " + found + " path(s)" + (hits.length ? ": " + hits.join("  |  ") : "") + ".",
             { aux: [{ label: "found", text: String(found) }] });
      return { trace: t, answer: found };
    }
  };

  G["td-bst"] = {
    input: [{ id: "t", label: "BST, level order (. = empty)", type: "tree", def: "5 3 7 2 4 6 8" },
            { id: "k", label: "k-th smallest", type: "int", def: 3 }],
    check: function (v) {
      var e = checkTree(v);
      if (e) return e;
      var t = buildTree(v.t);
      if (v.k < 1 || v.k > t.nodes.length) return "k must be between 1 and the number of nodes (" + t.nodes.length + ")";
      /* must actually be a BST, or the in-order claim is a lie */
      var vals = [], ok = true;
      (function walk(i) {
        if (i < 0) return;
        walk(t.nodes[i].l); vals.push(t.nodes[i].v); walk(t.nodes[i].r);
      })(t.root);
      for (var i = 1; i < vals.length; i++) if (vals[i] <= vals[i - 1]) ok = false;
      if (!ok) return "that is not a valid BST — its in-order walk is not strictly increasing, so the " +
                      "whole premise of this variant does not hold. Try  5 3 7 2 4 6 8";
      return null;
    },
    brute: function (v) {              /* collect everything and sort -- ignores the BST property */
      var t = buildTree(v.t), vals = [];
      for (var i = 0; i < t.nodes.length; i++) vals.push(t.nodes[i].v);
      vals.sort(function (a, b) { return a - b; });
      return vals[v.k - 1];
    },
    run: function (v) {
      var tree = buildTree(v.t), nodes = tree.nodes, k = v.k;
      var t = treeTrace(tree, ["st, cur = [], root", "while st or cur:", "    while cur:          # go as far LEFT as possible",
                               "        st.append(cur); cur = cur.left", "    cur = st.pop()",
                               "    k -= 1", "    if k == 0: return cur.val", "    cur = cur.right"],
                        "the " + k + "-th smallest, by in-order walk");
      var seen = {}, emitted = [], left = k, ans = null;
      var st = [], cur = tree.root;
      t.snap(0, "In a BST the in-order walk (left, node, right) comes out SORTED. So the k-th value you " +
                "emit is the k-th smallest — no sorting, and you can stop early.", {});
      while ((st.length || cur >= 0) && ans === null) {
        while (cur >= 0) {
          st.push(cur);
          t.snap(3, "push " + nodes[cur].v + " and keep going left — everything smaller lives down there.",
                 { ptr: { cur: String(cur) }, mark: merge(seen, { [String(cur)]: "pick" }),
                   aux: [{ label: "stack", items: st.map(function (i) { return String(nodes[i].v); }) }] });
          cur = nodes[cur].l;
        }
        cur = st.pop();
        left--;
        emitted.push(nodes[cur].v);
        seen[String(cur)] = "done";
        t.snap(5, "nothing smaller is left, so emit " + nodes[cur].v + " — that is number " +
                  (k - left) + " in sorted order." + (left === 0 ? " Which is the k we wanted." : ""),
               { ptr: { out: String(cur) }, mark: merge(seen, { [String(cur)]: "pick" }),
                 aux: [{ label: "emitted", items: strs(emitted) }, { label: "k remaining", text: String(left) }] });
        if (left === 0) { ans = nodes[cur].v; break; }
        cur = nodes[cur].r;
      }
      t.snap(6, "Answer " + ans + ". The walk stopped as soon as k ran out — the rest of the tree was " +
                "never touched.",
             { mark: seen, aux: [{ label: "emitted", items: strs(emitted) },
                                 { label: k + "-th smallest", text: String(ans) }] });
      return { trace: t, answer: ans };
    }
  };

  G["td-lca"] = {
    input: [TREE_FIELD,
            { id: "p", label: "first value", type: "int", def: 9 },
            { id: "q", label: "second value", type: "int", def: 15 }],
    check: function (v) {
      var e = checkTree(v);
      if (e) return e;
      var t = buildTree(v.t), hasP = false, hasQ = false;
      for (var i = 0; i < t.nodes.length; i++) {
        if (t.nodes[i].v === v.p) hasP = true;
        if (t.nodes[i].v === v.q) hasQ = true;
      }
      if (!hasP) return "the value " + v.p + " is not in this tree";
      if (!hasQ) return "the value " + v.q + " is not in this tree";
      if (v.p === v.q) return "give two different values";
      /* LCA is defined on NODES. With a repeated value, "the node holding 9" is ambiguous and
         the answer is not well defined -- which is exactly why the real problems all promise
         unique values. */
      var seenV = {};
      for (var j = 0; j < t.nodes.length; j++) {
        if (seenV[t.nodes[j].v]) return "the value " + t.nodes[j].v + " appears twice. LCA is defined on " +
                                        "NODES, so repeated values make the answer ambiguous — give the " +
                                        "tree distinct values.";
        seenV[t.nodes[j].v] = 1;
      }
      return null;
    },
    brute: function (v) {              /* deepest common node on the two root paths */
      var t = buildTree(v.t);
      function pathTo(val) {
        var out = null;
        (function go(i, acc) {
          if (i < 0 || out) return;
          acc = acc.concat([i]);
          if (t.nodes[i].v === val) { out = acc; return; }
          go(t.nodes[i].l, acc); go(t.nodes[i].r, acc);
        })(t.root, []);
        return out || [];
      }
      var a = pathTo(v.p), b = pathTo(v.q), best = null;
      for (var i = 0; i < Math.min(a.length, b.length); i++) if (a[i] === b[i]) best = a[i];
      return best === null ? null : t.nodes[best].v;
    },
    run: function (v) {
      var tree = buildTree(v.t), nodes = tree.nodes;
      var t = treeTrace(tree, ["def lca(node, p, q):", "    if not node or node is p or node is q:",
                               "        return node                 # found one -- report upward",
                               "    l = lca(node.left,  p, q)", "    r = lca(node.right, p, q)",
                               "    if l and r: return node         # they split HERE",
                               "    return l or r                   # pass the single hit up"],
                        "lowest common ancestor of " + v.p + " and " + v.q);
      var hit = {}, answer = null;
      t.snap(0, "A node reports non-null exactly when " + v.p + " or " + v.q + " is somewhere beneath it. " +
                "The moment BOTH sides report, you are standing on the split point.", {});
      function go(i) {
        if (i < 0) return -1;
        if (nodes[i].v === v.p || nodes[i].v === v.q) {
          hit[String(i)] = "done";
          t.snap(2, "node " + nodes[i].v + " IS one of the two targets — report it upward and stop " +
                    "descending this branch.",
                 { ptr: { found: String(i) }, mark: merge(hit, { [String(i)]: "pick" }) });
          return i;
        }
        var l = go(nodes[i].l), r = go(nodes[i].r);
        if (l >= 0 && r >= 0) {
          if (answer === null) answer = nodes[i].v;
          t.snap(5, "node " + nodes[i].v + ": the left subtree reported " + nodes[l].v + " and the right " +
                    "reported " + nodes[r].v + ". They split here, so THIS is the lowest common ancestor.",
                 { ptr: { lca: String(i) }, mark: merge(hit, { [String(i)]: "pick" }) });
          hit[String(i)] = "done";
          return i;
        }
        var up = l >= 0 ? l : r;
        if (up >= 0) {
          t.snap(6, "node " + nodes[i].v + ": only one side reported a hit, so this is not the split point " +
                    "yet — pass that single hit straight up.",
                 { ptr: { at: String(i) }, mark: merge(hit, { [String(i)]: "pick" }) });
        }
        return up;
      }
      var res = go(tree.root);
      t.snap(5, answer !== null
             ? ("Answer " + answer + ". Note this version assumes both values EXIST — if they might not, " +
                "you also have to count how many you actually found.")
             : ("Both targets sit on one branch, so the answer is the higher of the two: " +
                (res >= 0 ? nodes[res].v : "none") + "."),
             { mark: hit, aux: [{ label: "LCA", text: String(answer !== null ? answer : (res >= 0 ? nodes[res].v : "none")) }] });
      return { trace: t, answer: answer !== null ? answer : (res >= 0 ? nodes[res].v : null) };
    }
  };

  /* =================================== TREE BFS =================================== */

  G["tb-levels"] = {
    input: [TREE_FIELD],
    check: checkTree,
    brute: function (v) {              /* count levels by depth labelling, not by queue */
      var t = buildTree(v.t);
      if (!t.nodes.length) return "";
      var depth = [], maxd = 0;
      (function go(i, d) {
        if (i < 0) return;
        depth[i] = d; if (d > maxd) maxd = d;
        go(t.nodes[i].l, d + 1); go(t.nodes[i].r, d + 1);
      })(t.root, 0);
      var out = [];
      for (var d = 0; d <= maxd; d++) {
        var row = [];
        for (var i = 0; i < t.nodes.length; i++) if (depth[i] === d) row.push(t.nodes[i].v);
        out.push(row.join("."));
      }
      return out.join("|");
    },
    run: function (v) {
      var tree = buildTree(v.t), nodes = tree.nodes;
      var t = treeTrace(tree, ["q = deque([root])", "while q:", "    n = len(q)        # <-- THIS line is the pattern",
                               "    level = []", "    for _ in range(n):", "        node = q.popleft()",
                               "        level.append(node.val)", "        push its children",
                               "    out.append(level)"],
                        "level order — one complete level per round");
      var q = [tree.root], out = [], done = {};
      t.snap(2, "Snapshot how many nodes are in the queue BEFORE the inner loop. That count IS the current " +
                "level — read len(q) inside the loop instead and two levels bleed together.",
             { mark: { [String(tree.root)]: "pick" },
               aux: [{ label: "queue", items: q.map(function (i) { return String(nodes[i].v); }) }] });
      while (q.length) {
        var n = q.length, level = [], nxt = [];
        var cur = {};
        for (var i = 0; i < n; i++) cur[String(q[i])] = "pick";
        t.snap(2, "this round handles exactly " + n + " node(s) — the whole of level " + out.length + ".",
               { mark: merge(done, cur),
                 aux: [{ label: "len(q)", text: String(n) },
                       { label: "queue", items: q.map(function (i2) { return String(nodes[i2].v); }) }] });
        for (var j = 0; j < n; j++) {
          var node = q[j];
          level.push(nodes[node].v);
          done[String(node)] = "done";
          if (nodes[node].l >= 0) nxt.push(nodes[node].l);
          if (nodes[node].r >= 0) nxt.push(nodes[node].r);
        }
        out.push(level);
        var nmark = {};
        nxt.forEach(function (i3) { nmark[String(i3)] = "pick"; });
        t.snap(8, "level " + (out.length - 1) + " = [" + level.join(", ") + "]" +
                  (nxt.length ? ", and its " + nxt.length + " child(ren) are now queued for the next round."
                              : ", and nothing is left to queue."),
               { mark: merge(done, nmark),
                 aux: [{ label: "levels", items: out.map(function (L) { return "[" + L.join(",") + "]"; }) }] });
        q = nxt;
      }
      t.snap(8, "Answer " + out.map(function (L) { return "[" + L.join(",") + "]"; }).join(" ") +
                ". Everything 'per level' — right side view, averages, zigzag, minimum depth — " +
                "falls out of this one snapshot line.",
             { mark: done, aux: [{ label: "levels", items: out.map(function (L) { return "[" + L.join(",") + "]"; }) }] });
      return { trace: t, answer: out.map(function (L) { return L.join("."); }).join("|") };
    }
  };

  /* ===================================== TRIE ===================================== */

  G["tr-basic"] = {
    input: [{ id: "words", label: "words to insert", type: "words", def: "cat car dog" },
            { id: "query", label: "search for", type: "word", def: "car" }],
    check: function (v) {
      if (!v.words.length) return "give at least one word";
      var total = 0;
      for (var i = 0; i < v.words.length; i++) {
        if (!/^[a-z]+$/.test(v.words[i])) return "use lowercase letters only (got '" + v.words[i] + "')";
        total += v.words[i].length;
      }
      if (total > 18) return "keep the total length of all words to 18 or fewer so the tree stays readable";
      if (!/^[a-z]*$/.test(v.query)) return "the search word must be lowercase letters";
    },
    brute: function (v) { return v.words.indexOf(v.query) >= 0 ? 1 : 0; },
    run: function (v) {
      /* build the trie as a drawable binary-ish tree: first child on the left, sibling on the right */
      var nodes = [{ v: "●", l: -1, r: -1, ch: {}, end: false }];
      function insert(w) {
        var cur = 0;
        for (var i = 0; i < w.length; i++) {
          var c = w[i];
          if (cur !== null && nodes[cur].ch[c] == null) {
            nodes.push({ v: c, l: -1, r: -1, ch: {}, end: false });
            var fresh = nodes.length - 1;
            nodes[cur].ch[c] = fresh;
            if (nodes[cur].l < 0) nodes[cur].l = fresh;
            else {
              var sib = nodes[cur].l;
              while (nodes[sib].r >= 0) sib = nodes[sib].r;
              nodes[sib].r = fresh;
            }
          }
          cur = nodes[cur].ch[c];
        }
        nodes[cur].end = true;
        return cur;
      }
      var i2;
      for (i2 = 0; i2 < v.words.length; i2++) insert(v.words[i2]);

      var t = new Trace({ nodes: nodes, root: 0 },
                        ["node = root", "for c in word:", "    if c not in node.ch: return False",
                         "    node = node.ch[c]", "return node.end          # a word ENDS here?"],
                        "tree", "searching for \"" + v.query + "\" (drawn: first child left, sibling right)");
      t.snap(0, "The trie is built from " + v.words.join(", ") + ". Walking down spells a word, so a prefix " +
                "query costs the length of the prefix — not the number of words stored.",
             { ptr: { root: "0" }, mark: { 0: "pick" },
               aux: [{ label: "words", items: v.words.slice() }] });
      var cur = 0, path = {}, ok = 1;
      for (i2 = 0; i2 < v.query.length; i2++) {
        var c = v.query[i2];
        if (cur === null || nodes[cur].ch[c] == null) {
          ok = 0;
          t.snap(2, "no child '" + c + "' from here — nothing stored continues like that, so the search " +
                    "stops immediately.",
                 { mark: merge(path, { [String(cur)]: "bad" }),
                   aux: [{ label: "matched", text: v.query.slice(0, i2) || "(nothing)" }] });
          break;
        }
        cur = nodes[cur].ch[c];
        path[String(cur)] = "pick";
        t.snap(3, "follow '" + c + "' — matched \"" + v.query.slice(0, i2 + 1) + "\" so far.",
               { ptr: { at: String(cur) }, mark: merge(path),
                 aux: [{ label: "matched", text: v.query.slice(0, i2 + 1) }] });
      }
      if (ok) {
        ok = nodes[cur].end ? 1 : 0;
        t.snap(4, nodes[cur].end
               ? ("we are standing on a node flagged END, so \"" + v.query + "\" really was inserted.")
               : ("we reached the end of \"" + v.query + "\", but this node is NOT flagged END — it is only " +
                  "a prefix of something longer. Without that flag, 'app' would match when only 'apple' was stored."),
               { mark: merge(path, { [String(cur)]: nodes[cur].end ? "done" : "bad" }),
                 aux: [{ label: "verdict", text: nodes[cur].end ? "found" : "prefix only" }] });
      }
      return { trace: t, answer: ok };
    }
  };
})();
