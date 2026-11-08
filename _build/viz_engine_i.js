/* =====================================================================================
   VIZ ENGINE, part I  --  the traces added with the library audit: trees, graphs and grids.
   Same contract as the other parts (input, check, brute, run; gen supplies valid random input to the fuzz test).
   ===================================================================================== */
(function () {
  "use strict";
  var G = (typeof module !== "undefined" && module.exports) ? require("./viz_engine.js") : window.VIZGEN;
  var H = G.__helpers, Trace = H.Trace, merge = H.merge;

  function ri(rnd, lo, hi) { return lo + rnd(hi - lo + 1); }
  function J(a) { return a.join(","); }
  function aux() { var o = []; for (var i = 0; i < arguments.length; i += 2) o.push({ label: arguments[i], text: String(arguments[i + 1]) }); return o; }
  function copy(o) { return Object.assign({}, o); }
  function K(r, c) { return r + "," + c; }

  /* ---------- trees ---------- */
  function buildTree(level) {
    var nodes = [], queue = [], i = 1;
    if (!level.length || level[0] === null) return { nodes: [], root: -1 };
    nodes.push({ v: level[0], l: -1, r: -1 }); queue.push(0);
    while (queue.length && i < level.length) {
      var cur = queue.shift();
      if (i < level.length) { if (level[i] !== null) { nodes.push({ v: level[i], l: -1, r: -1 }); nodes[cur].l = nodes.length - 1; queue.push(nodes.length - 1); } i++; }
      if (i < level.length) { if (level[i] !== null) { nodes.push({ v: level[i], l: -1, r: -1 }); nodes[cur].r = nodes.length - 1; queue.push(nodes.length - 1); } i++; }
    }
    return { nodes: nodes, root: 0 };
  }
  function treeTrace(tree, code, caption) { return new Trace({ nodes: tree.nodes, root: tree.root }, code, "tree", caption); }
  function TF(label, def) { return { id: "t", label: label || "tree, level order (. = empty)", type: "tree", def: def || "3 9 20 . . 15 7" }; }
  function checkTree(v, max) {
    if (!v.t.length || v.t[0] === null) return "the tree needs a root value";
    if (buildTree(v.t).nodes.length > (max || 12)) return "keep it to " + (max || 12) + " nodes or fewer so the drawing stays readable";
    return null;
  }
  function genTree(rnd, maxLen, distinct) {
    var len = ri(rnd, 1, maxLen), lv = [], c = 1;
    for (var i = 0; i < len; i++) lv.push(rnd(5) === 0 && i > 0 ? null : (distinct ? c++ : ri(rnd, 1, 9)));
    lv[0] = distinct ? 0 : ri(rnd, 1, 9);
    if (distinct) { c = 1; for (i = 0; i < len; i++) if (lv[i] !== null) lv[i] = c++; }
    return lv;
  }
  function adj(tree) {
    var n = tree.nodes.length, g = []; for (var i = 0; i < n; i++) g.push([]);
    tree.nodes.forEach(function (nd, i) { if (nd.l >= 0) { g[i].push(nd.l); g[nd.l].push(i); } if (nd.r >= 0) { g[i].push(nd.r); g[nd.r].push(i); } });
    return g;
  }

  G["td-global"] = {
    input: [TF("tree, level order (. = empty)", "1 2 3 4 5")],
    check: function (v) { return checkTree(v, 15); },
    gen: function (rnd) { return { t: genTree(rnd, 9) }; },
    brute: function (v) {
      var tree = buildTree(v.t), g = adj(tree), n = g.length, best = 0;
      for (var s = 0; s < n; s++) {
        var d = {}, q = [s]; d[s] = 0;
        while (q.length) { var u = q.shift(); g[u].forEach(function (w) { if (!(w in d)) { d[w] = d[u] + 1; q.push(w); } }); }
        for (var k in d) best = Math.max(best, d[k]);
      }
      return best;
    },
    run: function (v) {
      var tree = buildTree(v.t), nodes = tree.nodes, best = 0, done = {};
      var t = treeTrace(tree, ["best = 0", "def depth(node):", "    if not node: return 0", "    l, r = depth(node.left), depth(node.right)", "    best = max(best, l + r)     # the path that BENDS at this node",
                               "    return 1 + max(l, r)        # only ONE arm can continue upward"], "diameter: the longest path may bend at any node");
      function go(i) {
        if (i < 0) return 0;
        var l = go(nodes[i].l), r = go(nodes[i].r);
        best = Math.max(best, l + r); done[String(i)] = "done";
        t.snap(4, "node " + nodes[i].v + ": left arm " + l + ", right arm " + r + ". A path bending here has " + (l + r) + " edges. Report only the longer arm (" + (1 + Math.max(l, r)) + ") upward.",
               { ptr: { at: String(i) }, mark: copy(done), aux: aux("best path", best) });
        return 1 + Math.max(l, r);
      }
      go(tree.root);
      t.snap(5, "Answer " + best + " edges. The best path did not have to pass through the root.", { mark: copy(done), aux: aux("diameter", best) });
      return { trace: t, answer: best };
    }
  };

  G["td-state"] = {
    input: [TF("tree of house values", "3 2 3 . 3 . 1")],
    check: function (v) { return checkTree(v, 12); },
    gen: function (rnd) { return { t: genTree(rnd, 9) }; },
    brute: function (v) {
      var tree = buildTree(v.t), nodes = tree.nodes, n = nodes.length, best = 0;
      for (var mask = 0; mask < (1 << n); mask++) {
        var ok = true, s = 0;
        for (var i = 0; i < n && ok; i++) if (mask >> i & 1) {
          s += nodes[i].v;
          if (nodes[i].l >= 0 && (mask >> nodes[i].l & 1)) ok = false;
          if (nodes[i].r >= 0 && (mask >> nodes[i].r & 1)) ok = false;
        }
        if (ok && s > best) best = s;
      }
      return best;
    },
    run: function (v) {
      var tree = buildTree(v.t), nodes = tree.nodes, done = {};
      var t = treeTrace(tree, ["def go(node):                       # returns (best if robbed, best if skipped)", "    if not node: return (0, 0)", "    l, r = go(node.left), go(node.right)",
                               "    take = node.val + l[1] + r[1]    # robbed: both children must be skipped", "    skip = max(l) + max(r)           # skipped: children are free", "    return (take, skip)"],
                        "house robber on a tree: each node returns TWO answers");
      function go(i) {
        if (i < 0) return [0, 0];
        var l = go(nodes[i].l), r = go(nodes[i].r);
        var take = nodes[i].v + l[1] + r[1], skip = Math.max(l[0], l[1]) + Math.max(r[0], r[1]);
        done[String(i)] = "done";
        t.snap(4, "node " + nodes[i].v + ": rob it = " + nodes[i].v + " + children skipped (" + l[1] + " + " + r[1] + ") = " + take + ".  Skip it = best of each child (" + Math.max(l[0], l[1]) + " + " + Math.max(r[0], r[1]) + ") = " + skip + ".",
               { ptr: { at: String(i) }, mark: copy(done), aux: aux("(take, skip)", "(" + take + ", " + skip + ")") });
        return [take, skip];
      }
      var res = go(tree.root), ans = Math.max(res[0], res[1]);
      t.snap(5, "Answer max(" + res[0] + ", " + res[1] + ") = " + ans + ".", { mark: copy(done), aux: aux("answer", ans) });
      return { trace: t, answer: ans };
    }
  };

  G["td-build"] = {
    input: [{ id: "pre", label: "preorder", type: "ints", def: "3 9 20 15 7" }, { id: "ino", label: "inorder", type: "ints", def: "9 3 15 20 7" }],
    check: function (v) {
      var n = v.pre.length;
      if (n < 1 || n > 9) return "1 to 9 nodes";
      if (v.ino.length !== n) return "both traversals need the same length";
      var s1 = v.pre.slice().sort(function (a, b) { return a - b; }), s2 = v.ino.slice().sort(function (a, b) { return a - b; });
      for (var i = 0; i < n; i++) { if (s1[i] !== s2[i]) return "both traversals must contain the same values"; if (i && s1[i] === s1[i - 1]) return "values must be distinct"; }
    },
    gen: function (rnd) {
      var n = ri(rnd, 1, 8), vals = [], i;
      for (i = 1; i <= n; i++) vals.push(i);
      for (i = n - 1; i > 0; i--) { var j = rnd(i + 1), tmp = vals[i]; vals[i] = vals[j]; vals[j] = tmp; }
      var pre = [];
      (function mk(lo, hi) { if (lo > hi) return; var r = ri(rnd, lo, hi); pre.push(vals[r]); mk(lo, r - 1); mk(r + 1, hi); })(0, n - 1);
      return { pre: pre, ino: vals };
    },
    brute: function (v) {
      function post(pre, ino) { if (!pre.length) return []; var r = pre[0], k = ino.indexOf(r); return post(pre.slice(1, k + 1), ino.slice(0, k)).concat(post(pre.slice(k + 1), ino.slice(k + 1)), [r]); }
      return J(post(v.pre, v.ino));
    },
    run: function (v) {
      var pre = v.pre, ino = v.ino, at = {}, next = 0, out = [], done = {};
      ino.forEach(function (x, i) { at[x] = i; });
      var t = new Trace(ino, ["at = {v: i for i, v in enumerate(inorder)}", "def go(lo, hi):                  # the slice of inorder this subtree owns", "    if lo > hi: return None",
                              "    root = preorder[next]; next += 1        # preorder says who the root is", "    mid = at[root]                          # inorder says what is left / right of it",
                              "    left = go(lo, mid - 1)                  # LEFT first: preorder is root, left, right", "    right = go(mid + 1, hi)"], "rebuild the tree from preorder + inorder (shown: the inorder row)", "array");
      function go(lo, hi) {
        if (lo > hi) return;
        var root = pre[next++], mid = at[root];
        t.snap(3, "next preorder value is " + root + ": it is the root of inorder[" + lo + ".." + hi + "]. In inorder it sits at " + mid + ", so " + (mid - lo) + " values form its left subtree and " + (hi - mid) + " its right.",
               { ptr: { root: mid }, span: [lo, hi], mark: copy(done), aux: aux("preorder used", next + " of " + pre.length) });
        go(lo, mid - 1); go(mid + 1, hi);
        out.push(root); done[mid] = "done";
        t.snap(5, "subtree rooted at " + root + " is finished (post-order output so far: " + out.join(" ") + ").", { ptr: { root: mid }, mark: copy(done), aux: aux("postorder", out.join(" ")) });
      }
      go(0, ino.length - 1);
      return { trace: t, answer: J(out) };
    }
  };

  G["td-parent"] = {
    input: [TF("tree with DISTINCT values", "3 5 1 6 2 0 8 . . 7 4"), { id: "target", label: "target value", type: "int", def: 5 }, { id: "k", label: "distance k", type: "int", def: 2 }],
    check: function (v) {
      var e = checkTree(v, 12); if (e) return e;
      var vals = buildTree(v.t).nodes.map(function (nd) { return nd.v; });      // only nodes that are really attached count
      for (var i = 0; i < vals.length; i++) if (vals.indexOf(vals[i]) !== i) return "values must be distinct so a node can be named by its value";
      if (vals.indexOf(v.target) < 0) return "the target must be a value in the tree";
      if (v.k < 0 || v.k > 8) return "k between 0 and 8";
    },
    gen: function (rnd) { var t = genTree(rnd, 9, true), m = t.filter(function (x) { return x !== null; }).length; return { t: t, target: ri(rnd, 1, m), k: ri(rnd, 0, 4) }; },
    brute: function (v) {
      var tree = buildTree(v.t), n = tree.nodes.length, d = [], i, j, k;
      for (i = 0; i < n; i++) { d.push([]); for (j = 0; j < n; j++) d[i].push(i === j ? 0 : 1e9); }
      adj(tree).forEach(function (ns, a) { ns.forEach(function (b) { d[a][b] = 1; }); });
      for (k = 0; k < n; k++) for (i = 0; i < n; i++) for (j = 0; j < n; j++) if (d[i][k] + d[k][j] < d[i][j]) d[i][j] = d[i][k] + d[k][j];
      var src = tree.nodes.findIndex(function (x) { return x.v === v.target; }), out = [];
      for (j = 0; j < n; j++) if (d[src][j] === v.k) out.push(tree.nodes[j].v);
      out.sort(function (a, b) { return a - b; });
      return out.length ? J(out) : "none";
    },
    run: function (v) {
      var tree = buildTree(v.t), nodes = tree.nodes, g = adj(tree);
      var src = nodes.findIndex(function (x) { return x.v === v.target; });
      var t = treeTrace(tree, ["parent = {root: None}; fill it with one DFS      # now every node can look UP as well as down", "q, seen = deque([(target, 0)]), {target}", "while q:", "    node, d = q.popleft()",
                               "    if d == k: out.append(node.val); continue", "    for nb in (node.left, node.right, parent[node]):", "        if nb and nb not in seen: seen.add(nb); q.append((nb, d + 1))"], "nodes at distance " + v.k + " from " + v.target);
      var dist = {}, q = [src], m = {}, out = [];
      dist[src] = 0; m[String(src)] = "pick";
      t.snap(0, "A tree only points downward. Adding a parent pointer for every node turns it into a graph you can walk in any direction.", { ptr: { at: String(src) }, mark: copy(m) });
      var level = 0;
      while (q.length) {
        var nq = [];
        q.forEach(function (u) { if (dist[u] === v.k) out.push(nodes[u].v); else g[u].forEach(function (w) { if (!(w in dist)) { dist[w] = dist[u] + 1; nq.push(w); } }); });
        t.snap(dist[q[0]] === v.k ? 4 : 5, "distance " + level + ": " + q.map(function (u) { return nodes[u].v; }).join(", ") + (level === v.k ? " — these are the answer." : "."), { mark: copy(m), aux: aux("found", out.join(" ") || "—") });
        nq.forEach(function (w) { m[String(w)] = "pick"; });
        q.forEach(function (u) { m[String(u)] = "done"; });
        q = level === v.k ? [] : nq; level++;
        if (level > v.k) break;
      }
      out.sort(function (a, b) { return a - b; });
      t.snap(4, "Answer: " + (out.join(", ") || "nobody") + ".", { aux: aux("answer", out.join(",") || "none") });
      return { trace: t, answer: out.length ? J(out) : "none" };
    }
  };

  G["tb-index"] = {
    input: [TF("tree, level order (. = empty)", "1 3 2 5 3 . 9")],
    check: function (v) { return checkTree(v, 14); },
    gen: function (rnd) { return { t: genTree(rnd, 10) }; },
    brute: function (v) {
      var tree = buildTree(v.t), lo = {}, hi = {}, best = 0;
      (function dfs(i, depth, idx) {
        if (i < 0) return;
        if (!(depth in lo) || idx < lo[depth]) lo[depth] = idx;
        if (!(depth in hi) || idx > hi[depth]) hi[depth] = idx;
        dfs(tree.nodes[i].l, depth + 1, 2 * idx); dfs(tree.nodes[i].r, depth + 1, 2 * idx + 1);
      })(tree.root, 0, 0);
      for (var d in lo) best = Math.max(best, hi[d] - lo[d] + 1);
      return best;
    },
    run: function (v) {
      var tree = buildTree(v.t), nodes = tree.nodes, best = 0, m = {};
      var t = treeTrace(tree, ["q = deque([(root, 0)])", "while q:", "    first, last = q[0][1], q[-1][1]", "    best = max(best, last - first + 1)", "    for _ in range(len(q)):",
                               "        node, i = q.popleft(); i -= first          # rebase so numbers stay small", "        children get 2*i and 2*i + 1"], "maximum width: number the slots as if the tree were complete");
      var q = [[tree.root, 0]], depth = 0;
      while (q.length) {
        var first = q[0][1], last = q[q.length - 1][1], w = last - first + 1;
        best = Math.max(best, w);
        var lm = copy(m); q.forEach(function (e) { lm[String(e[0])] = "pick"; });
        t.snap(3, "level " + depth + ": slot numbers " + q.map(function (e) { return e[1]; }).join(", ") + ". Width = last − first + 1 = " + w + " (empty gaps count).", { mark: lm, aux: aux("best width", best) });
        var nq = [];
        q.forEach(function (e) { var i = e[1] - first, nd = nodes[e[0]]; m[String(e[0])] = "done"; if (nd.l >= 0) nq.push([nd.l, 2 * i]); if (nd.r >= 0) nq.push([nd.r, 2 * i + 1]); });
        q = nq; depth++;
      }
      t.snap(3, "Answer " + best + ".", { mark: copy(m), aux: aux("answer", best) });
      return { trace: t, answer: best };
    }
  };

  G["ds-iter"] = {
    input: [TF("BST, level order (. = empty)", "7 3 15 . . 9 20")],
    check: function (v) { return checkTree(v, 12); },
    gen: function (rnd) { return { t: genTree(rnd, 9) }; },
    brute: function (v) { var tree = buildTree(v.t), out = []; (function io(i) { if (i < 0) return; io(tree.nodes[i].l); out.push(tree.nodes[i].v); io(tree.nodes[i].r); })(tree.root); return J(out); },
    run: function (v) {
      var tree = buildTree(v.t), nodes = tree.nodes, st = [], out = [], m = {};
      var t = treeTrace(tree, ["def push_left(n):", "    while n: stack.append(n); n = n.left        # dive down the left spine", "push_left(root)", "def next():",
                               "    n = stack.pop(); push_left(n.right)      # the top is always the next value", "    return n.val", "def hasNext(): return bool(stack)"], "iterator over the tree in order, one value per next() call");
      function marks() { var o = copy(m); st.forEach(function (i) { o[String(i)] = "pick"; }); return o; }
      function pushLeft(i) { while (i >= 0) { st.push(i); i = nodes[i].l; } }
      pushLeft(tree.root);
      t.snap(2, "constructor: push the whole left spine. Only O(height) nodes are held, not the whole tree.", { mark: marks(), aux: aux("stack (top last)", st.map(function (i) { return nodes[i].v; }).join(" ")) });
      while (st.length) {
        var i = st.pop(); out.push(nodes[i].v); m[String(i)] = "done"; pushLeft(nodes[i].r);
        t.snap(4, "next() returns " + nodes[i].v + ", then pushes the left spine of its right child.", { ptr: { at: String(i) }, mark: marks(), aux: aux("returned", out.join(" "), "stack (top last)", st.map(function (j) { return nodes[j].v; }).join(" ") || "empty") });
      }
      t.snap(6, "hasNext() is now false. The values came out in sorted order for a BST: " + out.join(", ") + ".", { mark: copy(m), aux: aux("answer", out.join(",")) });
      return { trace: t, answer: J(out) };
    }
  };

  /* ---------- graphs ---------- */
  function graphTrace(n, edges, code, caption) { return new Trace({ n: n, edges: edges, labels: null }, code, "graph", caption); }
  function edgeCheck(v, weighted) {
    if (v.n < 2 || v.n > 8) return "use between 2 and 8 nodes so the drawing stays readable";
    if (!v.edges.length) return "give at least one edge";
    if (v.edges.length > 12) return "keep it to 12 edges or fewer";
    for (var i = 0; i < v.edges.length; i++) {
      var e = v.edges[i];
      if (e[0] < 0 || e[1] < 0 || e[0] >= v.n || e[1] >= v.n) return "edge " + e[0] + "," + e[1] + " uses a node outside 0.." + (v.n - 1);
      if (e[0] === e[1]) return "self-loops are not useful here";
      if (weighted && (e.length < 3 || e[2] < 0)) return "every edge needs a non-negative weight, written  from,to,weight";
    }
    return null;
  }
  function genEdges(rnd, n, weighted, connected) {
    var edges = [], i;
    if (connected) for (i = 1; i < n; i++) edges.push(weighted ? [ri(rnd, 0, i - 1), i, ri(rnd, 1, 9)] : [ri(rnd, 0, i - 1), i]);
    var extra = ri(rnd, connected ? 0 : 1, 5);
    for (i = 0; i < extra && edges.length < 12; i++) { var a = rnd(n), b = rnd(n); if (a === b) b = (b + 1) % n; edges.push(weighted ? [a, b, ri(rnd, 0, 9)] : [a, b]); }
    return edges;
  }
  function neighbours(n, edges) { var g = []; for (var i = 0; i < n; i++) g.push([]); edges.forEach(function (e, idx) { g[e[0]].push([e[1], idx]); g[e[1]].push([e[0], idx]); }); return g; }

  G["gw-components"] = {
    input: [{ id: "n", label: "nodes", type: "int", def: 7 }, { id: "edges", label: "edges  a,b", type: "pairs", def: "0,1 1,2 3,4 5,6 4,3" }],
    check: function (v) { return edgeCheck(v, false); },
    gen: function (rnd) { var n = ri(rnd, 2, 8); return { n: n, edges: genEdges(rnd, n, false, false) }; },
    brute: function (v) {
      var p = []; for (var i = 0; i < v.n; i++) p.push(i);
      function f(x) { while (p[x] !== x) x = p[x]; return x; }
      v.edges.forEach(function (e) { p[f(e[0])] = f(e[1]); });
      var roots = {}; for (i = 0; i < v.n; i++) roots[f(i)] = 1;
      return Object.keys(roots).length;
    },
    run: function (v) {
      var n = v.n, g = neighbours(n, v.edges), seen = {}, m = {}, groups = 0;
      var t = graphTrace(n, v.edges, ["seen, groups = set(), 0", "for s in range(n):", "    if s in seen: continue            # already reached from an earlier start", "    groups += 1                      # a brand-new group begins here",
                                      "    DFS from s, marking everything it can reach", "return groups"], "count connected groups");
      for (var s = 0; s < n; s++) {
        if (seen[s]) continue;
        groups++;
        var stack = [s], comp = [s]; seen[s] = 1;
        while (stack.length) { var u = stack.pop(); g[u].forEach(function (w) { if (!seen[w[0]]) { seen[w[0]] = 1; stack.push(w[0]); comp.push(w[0]); } }); }
        var mm = copy(m); comp.forEach(function (x) { mm[String(x)] = "pick"; });
        t.snap(3, "node " + s + " was not reached yet, so it starts group " + groups + ". The search finds " + comp.join(", ") + ".", { ptr: { s: String(s) }, mark: mm, aux: aux("groups", groups) });
        comp.forEach(function (x) { m[String(x)] = "done"; });
      }
      t.snap(5, "Answer " + groups + ". Isolated nodes count as groups, which is why the loop runs over every node.", { mark: copy(m), aux: aux("answer", groups) });
      return { trace: t, answer: groups };
    }
  };

  G["gw-bipartite"] = {
    input: [{ id: "n", label: "nodes", type: "int", def: 4 }, { id: "edges", label: "edges  a,b", type: "pairs", def: "0,1 1,2 2,3 3,0" }],
    check: function (v) { return edgeCheck(v, false); },
    gen: function (rnd) { var n = ri(rnd, 2, 7); return { n: n, edges: genEdges(rnd, n, false, false) }; },
    brute: function (v) {
      for (var mask = 0; mask < (1 << v.n); mask++) if (v.edges.every(function (e) { return ((mask >> e[0]) & 1) !== ((mask >> e[1]) & 1); })) return true;
      return false;
    },
    run: function (v) {
      var n = v.n, g = neighbours(n, v.edges), col = {}, m = {}, em = {};
      var t = graphTrace(n, v.edges, ["colour = {}", "for s in range(n):", "    if s in colour: continue", "    colour[s] = 0; stack = [s]", "    while stack:", "        u = stack.pop()",
                                      "        for v in g[u]:", "            if v not in colour: colour[v] = 1 - colour[u]; stack.append(v)", "            elif colour[v] == colour[u]: return False   # an odd cycle", "return True"],
                        "two-colour the graph: every edge must join different colours");
      for (var s = 0; s < n; s++) {
        if (s in col) continue;
        col[s] = 0; m[String(s)] = "pick";
        var stack = [s];
        while (stack.length) {
          var u = stack.pop();
          for (var k = 0; k < g[u].length; k++) {
            var w = g[u][k][0], ei = g[u][k][1];
            if (!(w in col)) { col[w] = 1 - col[u]; m[String(w)] = col[w] ? "done" : "pick"; stack.push(w); em[String(ei)] = "done";
              t.snap(7, "colour " + w + " the opposite of " + u + ".", { ptr: { u: String(u), v: String(w) }, mark: copy(m), emark: copy(em) }); }
            else if (col[w] === col[u]) {
              m[String(u)] = "bad"; m[String(w)] = "bad"; em[String(ei)] = "bad";
              t.snap(8, "edge " + u + "–" + w + " joins two nodes of the SAME colour: the graph contains an odd cycle, so it cannot be split into two sides.", { mark: copy(m), emark: copy(em), aux: aux("answer", "false") });
              return { trace: t, answer: false };
            }
          }
        }
      }
      t.snap(9, "Every edge joins different colours: the nodes split into two sides.", { mark: copy(m), emark: copy(em), aux: aux("answer", "true") });
      return { trace: t, answer: true };
    }
  };

  G["sp-mod"] = {
    input: [{ id: "n", label: "nodes", type: "int", def: 5 }, { id: "edges", label: "edges  a,b,weight", type: "triples", def: "0,1,4 1,4,2 0,2,1 2,3,6 3,4,3 1,3,9" }],
    check: function (v) { return edgeCheck(v, true); },
    gen: function (rnd) { var n = ri(rnd, 2, 7); return { n: n, edges: genEdges(rnd, n, true, false) }; },
    brute: function (v) {
      var ws = []; v.edges.forEach(function (e) { if (ws.indexOf(e[2]) < 0) ws.push(e[2]); });
      ws.sort(function (a, b) { return a - b; });
      for (var i = 0; i < ws.length; i++) {
        var seen = { 0: 1 }, q = [0];
        while (q.length) { var u = q.pop(); v.edges.forEach(function (e) { if (e[2] > ws[i]) return; [[e[0], e[1]], [e[1], e[0]]].forEach(function (p) { if (p[0] === u && !seen[p[1]]) { seen[p[1]] = 1; q.push(p[1]); } }); }); }
        if (seen[v.n - 1]) return ws[i];
      }
      return "inf";
    },
    run: function (v) {
      var n = v.n, g = neighbours(n, v.edges), best = [], done = {}, m = {}, i;
      for (i = 0; i < n; i++) best.push(Infinity);
      best[0] = 0;
      var t = graphTrace(n, v.edges, ["best = {0: 0}; heap = [(0, 0)]               # (worst edge so far, node)", "while heap:", "    e, u = heappop(heap)", "    if u == target: return e",
                                      "    for v, w in graph[u]:", "        ne = max(e, w)                           # the cost is the BIGGEST edge, not the sum", "        if ne < best[v]: best[v] = ne; heappush(heap, (ne, v))"],
                        "path whose largest edge is as small as possible, from 0 to " + (n - 1));
      var heap = [[0, 0]];
      while (heap.length) {
        heap.sort(function (a, b) { return a[0] - b[0] || a[1] - b[1]; });
        var top = heap.shift(), e = top[0], u = top[1];
        if (done[u]) continue;
        done[u] = 1; m[String(u)] = "done";
        var upd = [];
        g[u].forEach(function (p) { var ne = Math.max(e, p[0] === u ? 0 : 0, v.edges[p[1]][2]); if (ne < best[p[0]]) { best[p[0]] = ne; heap.push([ne, p[0]]); upd.push(p[0] + "→" + ne); } });
        t.snap(5, "settle node " + u + " with worst edge " + e + ". " + (upd.length ? "Improved: " + upd.join(", ") + "." : "Nothing improved."), { ptr: { u: String(u) }, mark: copy(m),
               aux: aux("worst edge per node", best.map(function (b) { return b === Infinity ? "∞" : b; }).join(" ")) });
        if (u === n - 1) break;
      }
      var ans = best[n - 1] === Infinity ? "inf" : best[n - 1];
      t.snap(3, ans === "inf" ? "The target cannot be reached." : "Answer " + ans + ": the best route never uses an edge heavier than " + ans + ". Dijkstra still works because the 'cost' only grows along a path.", { aux: aux("answer", ans) });
      return { trace: t, answer: ans };
    }
  };

  G["dsu-prim"] = {
    input: [{ id: "n", label: "nodes", type: "int", def: 5 }, { id: "edges", label: "edges  a,b,cost", type: "triples", def: "0,1,2 1,2,3 0,3,6 1,3,8 2,4,7 3,4,9" }],
    check: function (v) {
      var e = edgeCheck(v, true); if (e) return e;
      var seen = { 0: 1 }, q = [0], g = neighbours(v.n, v.edges);
      while (q.length) { var u = q.pop(); g[u].forEach(function (p) { if (!seen[p[0]]) { seen[p[0]] = 1; q.push(p[0]); } }); }
      if (Object.keys(seen).length !== v.n) return "the graph must be connected for a spanning tree";
    },
    gen: function (rnd) { var n = ri(rnd, 2, 7); return { n: n, edges: genEdges(rnd, n, true, true) }; },
    brute: function (v) {
      var p = []; for (var i = 0; i < v.n; i++) p.push(i);
      function f(x) { while (p[x] !== x) x = p[x]; return x; }
      var total = 0;
      v.edges.slice().sort(function (a, b) { return a[2] - b[2]; }).forEach(function (e) { var a = f(e[0]), b = f(e[1]); if (a !== b) { p[a] = b; total += e[2]; } });
      return total;
    },
    run: function (v) {
      var n = v.n, inT = { 0: 1 }, m = { "0": "done" }, em = {}, total = 0;
      var t = graphTrace(n, v.edges, ["in_tree = {0}; total = 0", "while len(in_tree) < n:", "    pick the CHEAPEST edge with exactly one end in the tree        # the heap does this in O(log E)",
                                      "    add its far end to the tree; total += cost", "return total"], "minimum spanning tree by growing one tree from node 0 (Prim)");
      t.snap(0, "start the tree at node 0.", { mark: copy(m), aux: aux("total", 0) });
      while (Object.keys(inT).length < n) {
        var bi = -1;
        v.edges.forEach(function (e, i) { if (!!inT[e[0]] !== !!inT[e[1]] && (bi < 0 || e[2] < v.edges[bi][2])) bi = i; });
        var e = v.edges[bi], nw = inT[e[0]] ? e[1] : e[0];
        inT[nw] = 1; m[String(nw)] = "done"; em[String(bi)] = "done"; total += e[2];
        t.snap(3, "cheapest edge leaving the tree: " + e[0] + "–" + e[1] + " (cost " + e[2] + "). Add node " + nw + ".", { ptr: { new: String(nw) }, mark: copy(m), emark: copy(em), aux: aux("total", total) });
      }
      t.snap(4, "Answer " + total + ". Prim grows one tree; Kruskal merges many. Prim suits dense graphs and implicit edges.", { mark: copy(m), emark: copy(em), aux: aux("answer", total) });
      return { trace: t, answer: total };
    }
  };

  /* ---------- grids ---------- */
  function gridTrace(cells, code, caption) { return new Trace({ r: cells.length, c: cells[0].length, cells: cells }, code, "grid", caption); }
  function genGrid(rnd) { var R = ri(rnd, 1, 5), C = ri(rnd, 1, 6), g = []; for (var r = 0; r < R; r++) { var row = []; for (var c = 0; c < C; c++) row.push(rnd(2)); g.push(row); } return g; }
  var DIRS = [[1, 0], [-1, 0], [0, 1], [0, -1]];

  G["gr-border"] = {
    input: [{ id: "g", label: "grid (1 = land, 0 = water)", type: "grid01", def: "0100 1010 0110 0000" }],
    gen: function (rnd) { return { g: genGrid(rnd) }; },
    brute: function (v) {
      var g = v.g, R = g.length, C = g[0].length, cnt = 0;
      function reach(r, c, seen) {
        if (r < 0 || c < 0 || r >= R || c >= C) return true;       // walked off the grid
        if (g[r][c] !== 1 || seen[K(r, c)]) return false;
        seen[K(r, c)] = 1;
        return DIRS.some(function (d) { return reach(r + d[0], c + d[1], seen); });
      }
      for (var r = 0; r < R; r++) for (var c = 0; c < C; c++) if (g[r][c] === 1 && !reach(r, c, {})) cnt++;
      return cnt;
    },
    run: function (v) {
      var g = v.g, R = g.length, C = g[0].length, m = {}, q = [];
      var t = gridTrace(g.map(function (r) { return r.map(String); }), ["for each border cell that is land: flood from it     # these can reach the edge", "    mark everything the flood touches",
                                                                       "count the land cells the flood never reached          # they are enclosed"], "enclosed land: start from the border, not from the inside");
      for (var r = 0; r < R; r++) for (var c = 0; c < C; c++) if (g[r][c] === 1 && (r === 0 || c === 0 || r === R - 1 || c === C - 1) && !m[K(r, c)]) {
        var st = [[r, c]]; m[K(r, c)] = "gone"; var n0 = 1;
        while (st.length) { var p = st.pop(); DIRS.forEach(function (d) { var a = p[0] + d[0], b = p[1] + d[1]; if (a >= 0 && b >= 0 && a < R && b < C && g[a][b] === 1 && !m[K(a, b)]) { m[K(a, b)] = "gone"; st.push([a, b]); n0++; } }); }
        t.snap(0, "flood from border land (" + r + "," + c + "): it reaches " + n0 + " land cells. All of them can walk off the grid, so none is enclosed.", { ptr: { from: K(r, c) }, mark: copy(m) });
      }
      var cnt = 0, mm = copy(m);
      for (r = 0; r < R; r++) for (c = 0; c < C; c++) if (g[r][c] === 1 && !m[K(r, c)]) { cnt++; mm[K(r, c)] = "pick"; }
      t.snap(2, "Land the flood never touched is enclosed: " + cnt + " cell(s). Going backward from the border avoids testing every cell separately.", { mark: mm, aux: aux("enclosed", cnt) });
      return { trace: t, answer: cnt };
    }
  };

  G["sp-01bfs"] = {
    input: [{ id: "g", label: "grid (1 = costs 1 to enter, 0 = free)", type: "grid01", def: "00110 01010 01000" }],
    gen: function (rnd) { return { g: genGrid(rnd) }; },
    brute: function (v) {
      var g = v.g, R = g.length, C = g[0].length, d = {}, ch = true, r, c;
      d[K(0, 0)] = 0;
      while (ch) {
        ch = false;
        for (r = 0; r < R; r++) for (c = 0; c < C; c++) if (d[K(r, c)] !== undefined) DIRS.forEach(function (dd) {
          var a = r + dd[0], b = c + dd[1];
          if (a < 0 || b < 0 || a >= R || b >= C) return;
          var nd = d[K(r, c)] + g[a][b];
          if (d[K(a, b)] === undefined || nd < d[K(a, b)]) { d[K(a, b)] = nd; ch = true; }
        });
      }
      return d[K(R - 1, C - 1)];
    },
    run: function (v) {
      var g = v.g, R = g.length, C = g[0].length, dist = {}, m = {}, dq = [[0, 0]];
      var t = gridTrace(g.map(function (r) { return r.map(String); }), ["dq = deque([(0, 0)]); dist[(0, 0)] = 0", "while dq:", "    r, c = dq.popleft()", "    for each neighbour (x, y):", "        w = grid[x][y]               # 0 = free, 1 = costs one",
                                                                       "        if dist[r][c] + w < dist[x][y]:", "            dist[x][y] = dist[r][c] + w", "            free moves go to the FRONT, paid moves to the BACK"], "0-1 BFS: free moves jump the queue");
      dist[K(0, 0)] = 0;
      var frames = 0;
      while (dq.length) {
        var p = dq.shift(), r = p[0], c = p[1]; m[K(r, c)] = "done";
        var info = [];
        DIRS.forEach(function (d) {
          var a = r + d[0], b = c + d[1];
          if (a < 0 || b < 0 || a >= R || b >= C) return;
          var nd = dist[K(r, c)] + g[a][b];
          if (dist[K(a, b)] === undefined || nd < dist[K(a, b)]) { dist[K(a, b)] = nd; if (g[a][b] === 0) dq.unshift([a, b]); else dq.push([a, b]); info.push(K(a, b) + (g[a][b] ? " (+1, back)" : " (free, front)")); }
        });
        if (frames++ < 120) t.snap(5, "pop (" + r + "," + c + ") at cost " + dist[K(r, c)] + ". " + (info.length ? "Improved " + info.join("; ") + "." : "No neighbour improved."), { ptr: { at: K(r, c) }, mark: copy(m), aux: aux("queue size", dq.length) });
      }
      var ans = dist[K(R - 1, C - 1)];
      t.snap(1, "Answer " + ans + ": the fewest cells of cost 1 on any route to the far corner. O(cells), no heap.", { ptr: { goal: K(R - 1, C - 1) }, mark: copy(m), aux: aux("answer", ans) });
      return { trace: t, answer: ans };
    }
  };
})();
