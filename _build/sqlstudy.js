  /* ---------- study guide (injected by _build/build_sqlstudy.py) ---------- */
  var SQLmod = null, seedBytes = null;
  V.topic = null; V.tq = {}; V.runs = {}; V.done = {}; V.studyTab = "road";

  function rich(parent, s) {
    String(s).split(/(\*\*[^*]+\*\*|`[^`]+`)/g).forEach(function (p) {
      if (!p) return;
      if (p.length > 4 && p.slice(0, 2) === "**" && p.slice(-2) === "**") parent.appendChild(el("b", null, p.slice(2, -2)));
      else if (p.length > 2 && p.charAt(0) === "`" && p.slice(-1) === "`") parent.appendChild(el("code", "ic", p.slice(1, -1)));
      else parent.appendChild(document.createTextNode(p));
    });
    return parent;
  }
  function topicById(id) { return MAT.topics.filter(function (t) { return t.id === id; })[0]; }
  function topicIdx(id) { for (var i = 0; i < MAT.topics.length; i++) if (MAT.topics[i].id === id) return i; return -1; }
  function openTopic(id) { V.screen = "topic"; V.topic = id; V.runs = {}; render(); window.scrollTo(0, 0); }
  function studyDoneCount() { var n = 0; MAT.topics.forEach(function (t) { if (state.study[t.id]) n++; }); return n; }

  function studyReadCount() { var n = 0; MAT.topics.forEach(function (t) { if (state.read[t.id] || state.study[t.id]) n++; }); return n; }
  function isRead(id) { return !!(state.read[id] || state.study[id]); }
  function nextTopic() {
    for (var i = 0; i < MAT.plan.length; i++)
      for (var j = 0; j < MAT.plan[i].ids.length; j++) if (!isRead(MAT.plan[i].ids[j])) return topicById(MAT.plan[i].ids[j]);
    return null;
  }
  function bar2(done, total) {
    var b = el("div", "prog"), f = el("div", "prog-f");
    f.style.width = (total ? Math.round(100 * done / total) : 0) + "%";
    b.appendChild(f);
    return b;
  }
  function minutesOf(ids) { var m = 0; ids.forEach(function (id) { var t = topicById(id); m += t ? t.mins : 0; }); return m; }
  function fmtMin(m) { return m >= 60 ? (Math.round(m / 6) / 10) + " h" : m + " min"; }

  function studyCard() {
    var c = el("div", "scard");
    var l = el("div", "scard-l");
    l.appendChild(el("h2", null, "Study guide and roadmap"));
    var n = studyReadCount(), tot = MAT.topics.length, nx = nextTopic();
    l.appendChild(el("p", null, tot + " topics in " + MAT.plan.length + " stages, each ending with a short test. " + n + " of " + tot + " done." + (nx ? " Next up: " + nx.title + "." : " Everything ticked.")));
    l.appendChild(bar2(n, tot));
    c.appendChild(l);
    var b = el("button", "btn primary", n ? "continue the roadmap" : "open the roadmap");
    b.type = "button";
    b.addEventListener("click", function () { V.screen = "study"; V.studyTab = "road"; render(); window.scrollTo(0, 0); });
    c.appendChild(b);
    var qz = el("button", "btn", "mixed quiz"); qz.type = "button";
    qz.addEventListener("click", openQuiz);
    c.appendChild(qz);
    var wz = el("button", "btn", "write it (assessment practice)"); wz.type = "button";
    wz.addEventListener("click", openWrite);
    c.appendChild(wz);
    return c;
  }

  function toggleRead(id) {
    if (state.read[id]) delete state.read[id]; else state.read[id] = 1;
    save(); render();
  }

  function topicRow(t, num) {
    var r = el("div", "rrow" + (isRead(t.id) ? " done" : ""));
    var c = el("button", "chk" + (isRead(t.id) ? " on" : ""), isRead(t.id) ? "✓" : "");
    c.type = "button"; c.title = isRead(t.id) ? "mark as not done" : "mark as done";
    c.addEventListener("click", function () { toggleRead(t.id); });
    r.appendChild(c);
    var b = el("button", "rtitle"); b.type = "button";
    b.appendChild(el("span", "id", String(num)));
    var tt = el("span", "t"); tt.appendChild(document.createTextNode(t.title));
    if (t.star) tt.appendChild(el("span", "star", " must-know"));
    b.appendChild(tt);
    b.appendChild(el("span", "mins", t.mins + " min"));
    var s = state.study[t.id];
    b.appendChild(el("span", "tick" + (s ? " on" : ""), s ? s.best + "/" + s.of : "test"));
    b.addEventListener("click", function () { openTopic(t.id); });
    r.appendChild(b);
    return r;
  }

  function studyHome() {
    var f = document.createDocumentFragment();
    var hero = el("div", "hero");
    var h1 = el("h1"); h1.innerHTML = 'Work the plan. <em>Tick it off.</em>';
    hero.appendChild(h1);
    var n = studyReadCount(), tot = MAT.topics.length, nx = nextTopic();
    var mins = 0; MAT.topics.forEach(function (t) { if (!isRead(t.id)) mins += t.mins; });
    hero.appendChild(el("p", null, n + " of " + tot + " topics done" + (n < tot ? ", about " + fmtMin(mins) + " left." : ". Revise the weak ones and take the quiz.")));
    hero.appendChild(bar2(n, tot));
    var cta = el("div", "cta");
    if (nx) {
      var nb = el("button", "btn primary", "next up: " + nx.title); nb.type = "button";
      nb.addEventListener("click", function () { openTopic(nx.id); });
      cta.appendChild(nb);
    }
    var qzb = el("button", "btn", "mixed quiz"); qzb.type = "button";
    qzb.addEventListener("click", openQuiz);
    cta.appendChild(qzb);
    var wzb = el("button", "btn", "write it"); wzb.type = "button";
    wzb.addEventListener("click", openWrite);
    cta.appendChild(wzb);
    [["road", "roadmap"], ["all", "all topics / search"]].forEach(function (tb) {
      var on = (V.studyTab || "road") === tb[0];
      var x = el("button", "btn " + (on ? "tabon" : "ghost"), tb[1]); x.type = "button";
      x.addEventListener("click", function () { V.studyTab = tb[0]; render(); });
      cta.appendChild(x);
    });
    hero.appendChild(cta);
    f.appendChild(hero);

    var numOf = {}; MAT.topics.forEach(function (t, i) { numOf[t.id] = i + 1; });
    var wrap = el("div", "tiers");
    if ((V.studyTab || "road") === "road") {
      MAT.plan.forEach(function (st, si) {
        var done = st.ids.filter(isRead).length;
        var box = el("div", "tier stage" + (done === st.ids.length ? " complete" : ""));
        var h = el("div", "tier-h");
        h.appendChild(el("span", "n", "STAGE " + (si + 1)));
        h.appendChild(el("h3", null, st.name));
        h.appendChild(el("span", "c", done + " / " + st.ids.length + " · about " + fmtMin(minutesOf(st.ids))));
        box.appendChild(h);
        box.appendChild(el("div", "why-stage", st.why));
        st.ids.forEach(function (id) { box.appendChild(topicRow(topicById(id), numOf[id])); });
        wrap.appendChild(box);
      });
      var pr = el("div", "tier stage");
      var ph = el("div", "tier-h"); ph.appendChild(el("span", "n", "ALSO")); ph.appendChild(el("h3", null, "Practice on the live database"));
      pr.appendChild(ph);
      pr.appendChild(el("div", "why-stage", "After stage 5 or 6, do the graded exercises on the SQL Lab home screen. They run your query and compare the result."));
      var gb = el("button", "btn", "go to the exercises"); gb.type = "button"; gb.style.margin = "0 14px 14px";
      gb.addEventListener("click", function () { V.screen = "home"; render(); window.scrollTo(0, 0); });
      pr.appendChild(gb);
      wrap.appendChild(pr);
    } else {
      var q = document.createElement("input");
      q.type = "search"; q.className = "sfind"; q.placeholder = "find a topic: trigger, BCNF, window, join, isolation…";
      wrap.appendChild(q);
      var rows = [], seen = {}, groups = [];
      MAT.topics.forEach(function (t) { if (!seen[t.group]) { seen[t.group] = 1; groups.push(t.group); } });
      groups.forEach(function (g) {
        var list = MAT.topics.filter(function (t) { return t.group === g; });
        var box = el("div", "tier");
        var h = el("div", "tier-h");
        h.appendChild(el("h3", null, g));
        h.appendChild(el("span", "c", list.filter(function (t) { return isRead(t.id); }).length + " / " + list.length + " done"));
        box.appendChild(h);
        list.forEach(function (t) {
          var r = topicRow(t, numOf[t.id]);
          box.appendChild(r);
          rows.push({ node: r, text: (t.title + " " + t.group + " " + (t.kw || "")).toLowerCase() });
        });
        wrap.appendChild(box);
      });
      q.addEventListener("input", function () {
        var v = q.value.trim().toLowerCase();
        rows.forEach(function (r) { r.node.style.display = !v || r.text.indexOf(v) !== -1 ? "" : "none"; });
      });
    }
    f.appendChild(wrap);
    return f;
  }

  function codeBlock(b, key) {
    var w = el("div", "codew");
    var h = el("div", "codeh");
    h.appendChild(el("span", "lang " + (b.lang || "sql"), b.lang === "pg" ? "postgresql" : b.lang === "my" ? "mysql" : b.lang === "txt" ? "text" : "sql"));
    if (b.cap) h.appendChild(el("span", "cap", b.cap));
    h.appendChild(el("span", "sp"));
    if (b.run) {
      var rb = el("button", "mini", "run"); rb.type = "button";
      rb.disabled = engine !== "ready" || !SQLmod;
      rb.addEventListener("click", function () { runDemo(key, b.code); });
      h.appendChild(rb);
    }
    var cb = el("button", "mini", "copy"); cb.type = "button";
    cb.addEventListener("click", function () {
      try { navigator.clipboard.writeText(b.code); cb.textContent = "copied"; setTimeout(function () { cb.textContent = "copy"; }, 1200); } catch (e) {}
    });
    h.appendChild(cb);
    w.appendChild(h);
    w.appendChild(el("pre", "code", b.code));
    var r = V.runs[key];
    if (r) {
      if (r.err) { var e = el("div", "verdict err"); e.appendChild(el("b", null, "sql error")); e.appendChild(el("div", null, r.err)); w.appendChild(e); }
      else w.appendChild(resultTable(r, "result (on a throwaway copy of the sample database)"));
    }
    return w;
  }

  function runDemo(key, sql) {
    if (!SQLmod || !seedBytes) return;
    var tmp = new SQLmod.Database(seedBytes);
    try { var res = tmp.exec(sql); V.runs[key] = res.length ? res[res.length - 1] : { columns: [], values: [] }; }
    catch (e) { V.runs[key] = { err: String(e.message || e) }; }
    try { tmp.close(); } catch (e2) {}
    render();
  }

  function blockNode(b, key) {
    var k = b.k, n;
    if (k === "h") return el("h3", "bh", b.t);
    if (k === "p") return rich(el("p", "bp"), b.t);
    if (k === "ul" || k === "ol") {
      n = el(k, "bl");
      b.t.forEach(function (x) { n.appendChild(rich(el("li"), x)); });
      return n;
    }
    if (k === "code") return codeBlock(b, key);
    if (k === "table") {
      var sc = el("div", "tscroll bt"), t = document.createElement("table");
      var th = document.createElement("thead"), tr = document.createElement("tr");
      b.head.forEach(function (c) { var x = document.createElement("th"); x.textContent = c; tr.appendChild(x); });
      th.appendChild(tr); t.appendChild(th);
      var tb = document.createElement("tbody");
      b.rows.forEach(function (r) {
        var rr = document.createElement("tr");
        r.forEach(function (c) { var td = document.createElement("td"); td.style.whiteSpace = "normal"; rich(td, c); rr.appendChild(td); });
        tb.appendChild(rr);
      });
      t.appendChild(tb); sc.appendChild(t);
      return sc;
    }
    var labels = { note: "remember", pg: "postgresql", my: "mysql", trap: "trap", ask: "they ask", dif: "difference" };
    n = el("div", "call " + k);
    n.appendChild(el("b", null, labels[k] || k));
    rich(n.appendChild(el("div")), b.t);
    return n;
  }

  function topicScreen() {
    var f = document.createDocumentFragment();
    var t = topicById(V.topic), i = topicIdx(V.topic);
    var crumb = el("div", "crumb");
    crumb.appendChild(el("span", "now", "topic " + (i + 1) + " of " + MAT.topics.length));
    crumb.appendChild(el("span", null, t.group));
    crumb.appendChild(el("span", "sp"));
    var rd = el("button", "btn " + (isRead(t.id) ? "tabon" : "ghost"), isRead(t.id) ? "done \u2713" : "mark done"); rd.type = "button";
    rd.addEventListener("click", function () { toggleRead(t.id); });
    crumb.appendChild(rd);
    var pb = el("button", "btn ghost", "guide"); pb.type = "button";
    pb.addEventListener("click", function () { V.screen = "study"; render(); });
    crumb.appendChild(pb);
    if (i > 0) { var a = el("button", "btn ghost", "prev"); a.type = "button"; a.addEventListener("click", function () { openTopic(MAT.topics[i - 1].id); }); crumb.appendChild(a); }
    if (i < MAT.topics.length - 1) { var z = el("button", "btn ghost", "next"); z.type = "button"; z.addEventListener("click", function () { openTopic(MAT.topics[i + 1].id); }); crumb.appendChild(z); }
    f.appendChild(crumb);

    var box = el("div", "qbox topic");
    box.appendChild(el("h2", null, t.title));
    if (t.intro) box.appendChild(rich(el("p", "bp lead"), t.intro));
    t.blocks.forEach(function (b, j) { box.appendChild(blockNode(b, t.id + ":" + j)); });
    f.appendChild(box);
    if (t.test && t.test.length) f.appendChild(testBox(t));
    return f;
  }

  function testBox(t) {
    var ans = V.tq[t.id] = V.tq[t.id] || [];
    var box = el("div", "qbox stest");
    var h = el("div", "crumb"); h.appendChild(el("span", "now", "test yourself")); h.appendChild(el("span", null, t.test.length + " questions"));
    box.appendChild(h);
    t.test.forEach(function (q, qi) {
      var card = el("div", "tq");
      rich(card.appendChild(el("div", "tq-q")), (qi + 1) + ". " + q.q);
      var picked = ans[qi];
      q.o.forEach(function (o, oi) {
        var b = el("button", "opt"); b.type = "button";
        if (picked != null) {
          b.disabled = true;
          if (oi === q.a) b.className += " right";
          else if (oi === picked) b.className += " wrong";
        }
        b.appendChild(el("span", "ol", "ABCD".charAt(oi)));
        rich(b.appendChild(el("span", "ot")), o);
        b.addEventListener("click", function () { ans[qi] = oi; finishCheck(t); render(); });
        card.appendChild(b);
      });
      if (picked != null) {
        var ex = el("div", "why " + (picked === q.a ? "ok" : "no"));
        ex.appendChild(el("b", null, picked === q.a ? "correct" : "not quite"));
        rich(ex.appendChild(el("div")), q.w);
        card.appendChild(ex);
      }
      box.appendChild(card);
    });
    var got = 0, n = 0;
    t.test.forEach(function (q, qi) { if (ans[qi] != null) { n++; if (ans[qi] === q.a) got++; } });
    if (n === t.test.length) {
      var r = el("div", "verdict " + (got === n ? "pass" : "err"));
      r.appendChild(el("b", null, "score " + got + " / " + n));
      r.appendChild(el("div", null, got === n ? "Clean sheet. Move to the next topic." : "Re-read the sections behind the ones you missed, then retry."));
      box.appendChild(r);
      var rt = el("button", "btn", "retry"); rt.type = "button";
      rt.addEventListener("click", function () { V.tq[t.id] = []; V.done[t.id] = 0; render(); });
      box.appendChild(rt);
    }
    return box;
  }

  function finishCheck(t) {
    var ans = V.tq[t.id], got = 0, n = 0;
    t.test.forEach(function (q, qi) { if (ans[qi] != null) { n++; if (ans[qi] === q.a) got++; } });
    if (n === t.test.length && !V.done[t.id]) {
      V.done[t.id] = 1;
      state.read[t.id] = 1;
      var s = state.study[t.id];
      if (!s || got > s.best || s.of !== n) state.study[t.id] = { best: s && s.of === n ? Math.max(s.best, got) : got, of: n };
      save();
    }
  }

