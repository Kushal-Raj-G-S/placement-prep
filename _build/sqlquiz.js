  /* ---------- mixed quiz (injected by _build/build_sqlstudy.py) ---------- */
  V.quiz = null;

  function quizPool() {
    if (V._pool) return V._pool;
    var pool = [];
    MAT.topics.forEach(function (t) {
      t.test.forEach(function (q, i) { pool.push({ id: "t:" + t.id + ":" + i, area: t.group, topic: t.title, q: q.q, o: q.o, a: q.a, w: q.w }); });
    });
    (MAT.bank || []).forEach(function (q, i) { pool.push({ id: "g:" + i, area: q.area, topic: q.area, q: q.q, o: q.o, a: q.a, w: q.w }); });
    V._pool = pool;
    return pool;
  }
  function quizAreas() {
    var seen = {}, list = [];
    quizPool().forEach(function (q) { if (!seen[q.area]) { seen[q.area] = 0; list.push(q.area); } seen[q.area]++; });
    return list.map(function (a) { return { name: a, n: seen[a] }; });
  }
  function shuffled(arr) {
    var a = arr.slice();
    for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; }
    return a;
  }
  function missedIds() { return Object.keys(state.quiz.miss || {}); }

  function openQuiz() { V.screen = "quiz"; if (!V.quiz || V.quiz.phase === "run") V.quiz = { phase: "setup" }; render(); window.scrollTo(0, 0); }

  var QSET = { len: 20, timed: false, exam: false, mode: "all", areas: null };

  function startQuiz(list) {
    clearInterval(V.qtimer);
    V.quiz = { phase: "run", list: list, i: 0, ans: [], exam: QSET.exam, timed: QSET.timed, start: Date.now(), left: QSET.timed ? list.length * 60 : 0 };
    if (QSET.timed) {
      V.qtimer = setInterval(function () {
        if (V.screen !== "quiz" || !V.quiz || V.quiz.phase !== "run") { clearInterval(V.qtimer); return; }
        V.quiz.left--;
        var n = document.getElementById("qclock");
        if (n) n.textContent = fmtClock(V.quiz.left);
        if (V.quiz.left <= 0) { clearInterval(V.qtimer); finishQuiz(); }
      }, 1000);
    }
    render(); window.scrollTo(0, 0);
  }
  function fmtClock(s) { s = Math.max(0, s); return Math.floor(s / 60) + ":" + ("0" + (s % 60)).slice(-2); }

  function buildQuiz() {
    var pool = quizPool();
    if (!QSET.areas) { QSET.areas = {}; quizAreas().forEach(function (a) { QSET.areas[a.name] = true; }); }
    var miss = state.quiz.miss || {};
    var list = pool.filter(function (q) {
      if (!QSET.areas[q.area]) return false;
      if (QSET.mode === "missed") return !!miss[q.id];
      if (QSET.mode === "new") return !(state.quiz.seen || {})[q.id];
      return true;
    });
    list = shuffled(list);
    if (QSET.len > 0) list = list.slice(0, QSET.len);
    return list;
  }

  function finishQuiz() {
    clearInterval(V.qtimer);
    var Q = V.quiz; if (Q.phase === "done") return;
    var got = 0;
    Q.list.forEach(function (q, i) {
      var ok = Q.ans[i] === q.a;
      state.quiz.seen[q.id] = 1;
      if (Q.ans[i] != null) {
        if (ok) { got++; if (state.quiz.miss[q.id]) delete state.quiz.miss[q.id]; }
        else state.quiz.miss[q.id] = (state.quiz.miss[q.id] || 0) + 1;
      } else state.quiz.miss[q.id] = state.quiz.miss[q.id] || 1;
    });
    Q.got = got; Q.secs = Math.round((Date.now() - Q.start) / 1000); Q.phase = "done";
    state.quiz.hist.push({ d: new Date().toISOString().slice(0, 10), n: Q.list.length, got: got, secs: Q.secs });
    if (state.quiz.hist.length > 30) state.quiz.hist = state.quiz.hist.slice(-30);
    save(); render(); window.scrollTo(0, 0);
  }

  function chip(label, on, fn) {
    var b = el("button", "qchip" + (on ? " on" : ""), label); b.type = "button";
    b.addEventListener("click", fn);
    return b;
  }

  function quizSetup() {
    var f = document.createDocumentFragment();
    var hero = el("div", "hero");
    var h1 = el("h1"); h1.innerHTML = 'Mixed quiz. <em>No hints.</em>';
    hero.appendChild(h1);
    var pool = quizPool();
    hero.appendChild(el("p", null, pool.length + " questions across theory, keys and normal-form calculations, query-result prediction, scenario design and PostgreSQL vs MySQL. Answers are explained after you pick."));
    var hist = state.quiz.hist.slice(-5);
    if (hist.length) hero.appendChild(el("p", null, "Recent: " + hist.map(function (h) { return h.got + "/" + h.n; }).join("  ·  ")));
    f.appendChild(hero);

    var box = el("div", "qbox");
    if (!QSET.areas) { QSET.areas = {}; quizAreas().forEach(function (a) { QSET.areas[a.name] = true; }); }

    box.appendChild(el("div", "crumb", "areas"));
    var cw = el("div", "qchips");
    quizAreas().forEach(function (a) {
      cw.appendChild(chip(a.name + " (" + a.n + ")", !!QSET.areas[a.name], function () { QSET.areas[a.name] = !QSET.areas[a.name]; render(); }));
    });
    box.appendChild(cw);
    var all = el("div", "qchips");
    all.appendChild(chip("select all", false, function () { quizAreas().forEach(function (a) { QSET.areas[a.name] = true; }); render(); }));
    all.appendChild(chip("calculations + queries only", false, function () { quizAreas().forEach(function (a) { QSET.areas[a.name] = /calculate|Predict/.test(a.name); }); render(); }));
    box.appendChild(all);

    box.appendChild(el("div", "crumb", "questions"));
    var mw = el("div", "qchips");
    var nMiss = missedIds().length;
    [["all", "everything"], ["new", "not seen yet"], ["missed", "only ones I missed (" + nMiss + ")"]].forEach(function (m) {
      mw.appendChild(chip(m[1], QSET.mode === m[0], function () { QSET.mode = m[0]; render(); }));
    });
    box.appendChild(mw);

    box.appendChild(el("div", "crumb", "length"));
    var lw = el("div", "qchips");
    [[10, "10"], [20, "20"], [40, "40"], [0, "all"]].forEach(function (l) {
      lw.appendChild(chip(l[1], QSET.len === l[0], function () { QSET.len = l[0]; render(); }));
    });
    box.appendChild(lw);

    box.appendChild(el("div", "crumb", "rules"));
    var rw = el("div", "qchips");
    rw.appendChild(chip("timed: 60 s per question", QSET.timed, function () { QSET.timed = !QSET.timed; render(); }));
    rw.appendChild(chip("exam mode: answers only at the end", QSET.exam, function () { QSET.exam = !QSET.exam; render(); }));
    box.appendChild(rw);

    var list = buildQuiz();
    var go = el("button", "btn primary", list.length ? "start (" + list.length + " questions)" : "no questions match");
    go.type = "button"; go.disabled = !list.length;
    go.addEventListener("click", function () { startQuiz(list); });
    box.appendChild(go);

    var weak = {};
    missedIds().forEach(function (id) { var q = pool.filter(function (x) { return x.id === id; })[0]; if (q) weak[q.topic] = (weak[q.topic] || 0) + 1; });
    var wk = Object.keys(weak).sort(function (a, b) { return weak[b] - weak[a]; }).slice(0, 4);
    if (wk.length) {
      var wd = el("div", "call dif"); wd.appendChild(el("b", null, "weak spots so far"));
      wd.appendChild(el("div", null, wk.map(function (k) { return k + " (" + weak[k] + ")"; }).join(" · ")));
      box.appendChild(wd);
    }
    f.appendChild(box);
    return f;
  }

  function quizRun() {
    var Q = V.quiz, f = document.createDocumentFragment();
    var q = Q.list[Q.i], picked = Q.ans[Q.i];
    var crumb = el("div", "crumb");
    crumb.appendChild(el("span", "now", "question " + (Q.i + 1) + " of " + Q.list.length));
    crumb.appendChild(el("span", null, q.area));
    crumb.appendChild(el("span", "sp"));
    if (Q.timed) { var c = el("span", "qclock", fmtClock(Q.left)); c.id = "qclock"; crumb.appendChild(c); }
    var qb = el("button", "btn ghost", "quit"); qb.type = "button";
    qb.addEventListener("click", function () { clearInterval(V.qtimer); V.quiz = { phase: "setup" }; render(); });
    crumb.appendChild(qb);
    f.appendChild(crumb);
    f.appendChild(bar2(Q.i, Q.list.length));

    var box = el("div", "qbox");
    var card = el("div", "tq");
    var qt = el("div", "tq-q big"); qt.textContent = q.q; card.appendChild(qt);
    q.o.forEach(function (o, oi) {
      var b = el("button", "opt"); b.type = "button";
      var revealed = !Q.exam && picked != null;
      if (revealed) {
        b.disabled = true;
        if (oi === q.a) b.className += " right"; else if (oi === picked) b.className += " wrong";
      } else if (Q.exam && picked === oi) b.className += " chosen";
      b.appendChild(el("span", "ol", "ABCD".charAt(oi)));
      rich(b.appendChild(el("span", "ot")), o);
      b.addEventListener("click", function () { Q.ans[Q.i] = oi; render(); });
      card.appendChild(b);
    });
    if (!Q.exam && picked != null) {
      var ex = el("div", "why " + (picked === q.a ? "ok" : "no"));
      ex.appendChild(el("b", null, picked === q.a ? "correct" : "not quite"));
      rich(ex.appendChild(el("div")), q.w);
      card.appendChild(ex);
    }
    box.appendChild(card);
    var row = el("div", "runrow");
    if (Q.i > 0 && Q.exam) { var pv = el("button", "btn ghost", "previous"); pv.type = "button"; pv.addEventListener("click", function () { Q.i--; render(); }); row.appendChild(pv); }
    row.appendChild(el("span", "sp"));
    var last = Q.i === Q.list.length - 1;
    var nx = el("button", "btn primary", last ? "finish" : "next"); nx.type = "button";
    nx.disabled = !Q.exam && picked == null;
    nx.addEventListener("click", function () { if (last) finishQuiz(); else { Q.i++; render(); window.scrollTo(0, 0); } });
    row.appendChild(nx);
    box.appendChild(row);
    f.appendChild(box);
    return f;
  }

  function quizDone() {
    var Q = V.quiz, f = document.createDocumentFragment();
    var pct = Math.round(100 * Q.got / Q.list.length);
    var hero = el("div", "hero");
    var h1 = el("h1"); h1.innerHTML = Q.got + ' / ' + Q.list.length + ' <em>' + pct + '%</em>';
    hero.appendChild(h1);
    hero.appendChild(el("p", null, "Time " + fmtClock(Q.secs) + (pct >= 85 ? ". Interview-ready on this set." : pct >= 60 ? ". Decent; review the misses below." : ". Go back to the roadmap topics for the areas below, then retry.")));
    var cta = el("div", "cta");
    var wrongIdx = [];
    Q.list.forEach(function (q, i) { if (Q.ans[i] !== q.a) wrongIdx.push(i); });
    if (wrongIdx.length) {
      var rt = el("button", "btn primary", "retry the " + wrongIdx.length + " missed"); rt.type = "button";
      rt.addEventListener("click", function () { startQuiz(wrongIdx.map(function (i) { return Q.list[i]; })); });
      cta.appendChild(rt);
    }
    var nw = el("button", "btn", "new quiz"); nw.type = "button";
    nw.addEventListener("click", function () { V.quiz = { phase: "setup" }; render(); window.scrollTo(0, 0); });
    cta.appendChild(nw);
    var gd = el("button", "btn ghost", "back to the roadmap"); gd.type = "button";
    gd.addEventListener("click", function () { V.screen = "study"; render(); window.scrollTo(0, 0); });
    cta.appendChild(gd);
    hero.appendChild(cta);
    f.appendChild(hero);

    var byArea = {};
    Q.list.forEach(function (q, i) { var a = byArea[q.area] = byArea[q.area] || { n: 0, ok: 0 }; a.n++; if (Q.ans[i] === q.a) a.ok++; });
    var ab = el("div", "qbox");
    ab.appendChild(el("div", "crumb", "by area"));
    Object.keys(byArea).sort(function (x, y) { return byArea[x].ok / byArea[x].n - byArea[y].ok / byArea[y].n; }).forEach(function (k) {
      var r = el("div", "arow");
      r.appendChild(el("span", "an", k));
      r.appendChild(bar2(byArea[k].ok, byArea[k].n));
      r.appendChild(el("span", "ac", byArea[k].ok + "/" + byArea[k].n));
      ab.appendChild(r);
    });
    f.appendChild(ab);

    if (wrongIdx.length) {
      var wb = el("div", "qbox");
      wb.appendChild(el("div", "crumb", "review the misses"));
      wrongIdx.forEach(function (i) {
        var q = Q.list[i], card = el("div", "tq");
        var qt = el("div", "tq-q big"); qt.textContent = q.q; card.appendChild(qt);
        var yours = Q.ans[i] != null ? q.o[Q.ans[i]] : "(no answer)";
        var y = el("div", "why no"); y.appendChild(el("b", null, "you picked")); rich(y.appendChild(el("div")), yours); card.appendChild(y);
        var r = el("div", "why ok"); r.appendChild(el("b", null, "right answer")); rich(r.appendChild(el("div")), q.o[q.a] + "  —  " + q.w); card.appendChild(r);
        wb.appendChild(card);
      });
      f.appendChild(wb);
    }
    return f;
  }

  function quizScreen() {
    if (!V.quiz) V.quiz = { phase: "setup" };
    if (V.quiz.phase === "run") return quizRun();
    if (V.quiz.phase === "done") return quizDone();
    return quizSetup();
  }

