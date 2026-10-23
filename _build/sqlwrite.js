  /* ---------- write-it: assessment-style tasks (injected by _build/build_sqlstudy.py) ---------- */
  V.w = { mode: "run", kind: "all", db: "all", tier: 0, id: null, out: null, verdict: null, checks: null, revealed: false, rubric: {}, t0: 0, schema: false };
  var TIERN = { 1: "easy", 2: "medium", 3: "hard" };
  var KINDN = { query: "query", ddl: "create tables", paper: "paper only" };
  var DBN = { co: "company db", shop: "shop db", empty: "empty db", none: "" };
  var RUBRIC = {
    query: ["Right tables and join conditions", "Right WHERE / HAVING conditions", "Right grouping, subquery or window logic", "Right columns, aliases and ordering", "Handles NULLs, ties and empty cases"],
    ddl: ["All tables and columns present with sensible types", "Primary keys, composite where needed", "Foreign keys with the right ON DELETE action", "NOT NULL / UNIQUE / CHECK / DEFAULT rules", "Junction or child tables designed correctly"]
  };

  function wTasks() { return MAT.write.tasks; }
  function wTask(id) { return wTasks().filter(function (t) { return t.id === id; })[0]; }
  function wDoneCount() { return wTasks().filter(function (t) { return state.wr.done[t.id]; }).length; }

  function wBytes(db) {
    if (db === "shop") {
      if (!V._shopBytes) { var d = new SQLmod.Database(); d.run(MAT.write.shopSql); V._shopBytes = d.export(); d.close(); }
      return V._shopBytes;
    }
    return db === "co" ? seedBytes : null;
  }
  function wOpen(db, pre) {
    var b = wBytes(db);
    var d = b ? new SQLmod.Database(b) : new SQLmod.Database();
    if (pre) d.run(pre);
    return d;
  }
  function lastResult(res) { return res.length ? res[res.length - 1] : { columns: [], values: [] }; }
  function wExec(task, sql) {
    var d = wOpen(task.db, task.pre);
    try {
      var res = d.exec(sql);
      if (task.verify) res = d.exec(task.verify);
      return lastResult(res);
    } finally { d.close(); }
  }

  function openWrite() { V.screen = "write"; V.w.id = null; render(); window.scrollTo(0, 0); }
  function openWTask(id, mode) {
    var t = wTask(id);
    V.screen = "wtask"; V.w.id = id; V.w.out = null; V.w.verdict = null; V.w.checks = null; V.w.revealed = false; V.w.rubric = {};
    V.w.mode = t.kind === "paper" ? "paper" : (mode || V.w.mode);
    V.w.t0 = Date.now(); V.w.schema = false;
    clearInterval(V.wtimer);
    V.wtimer = setInterval(function () {
      if (V.screen !== "wtask") { clearInterval(V.wtimer); return; }
      var n = document.getElementById("wclock");
      if (n) n.textContent = fmtClock(Math.round((Date.now() - V.w.t0) / 1000));
    }, 1000);
    render(); window.scrollTo(0, 0);
  }

  function wcrumbChip(label, on, fn) { return chip(label, on, fn); }

  function writeHome() {
    var f = document.createDocumentFragment();
    var tasks = wTasks();
    var hero = el("div", "hero");
    var h1 = el("h1"); h1.innerHTML = 'Write it. <em>Like the assessment.</em>';
    hero.appendChild(h1);
    hero.appendChild(el("p", null, tasks.length + " tasks. Query tasks run on a company database and a shop database and are graded on the result set. 'Create tables' tasks are graded by inserting good and bad rows into your schema. Paper tasks (triggers, procedures, normalization, theory) are written without running and checked against a model answer."));
    hero.appendChild(el("p", null, wDoneCount() + " of " + tasks.length + " passed. Paper marks count when you tick at least 80% of the rubric."));
    hero.appendChild(bar2(wDoneCount(), tasks.length));
    f.appendChild(hero);

    var box = el("div", "qbox");
    box.appendChild(el("div", "crumb", "how do you want to practise?"));
    var mw = el("div", "qchips");
    mw.appendChild(wcrumbChip("run it and get graded (online assessment)", V.w.mode === "run", function () { V.w.mode = "run"; render(); }));
    mw.appendChild(wcrumbChip("paper: no running, check against the model answer", V.w.mode === "paper", function () { V.w.mode = "paper"; render(); }));
    box.appendChild(mw);
    box.appendChild(el("div", "crumb", "filter"));
    var fw = el("div", "qchips");
    [["all", "all"], ["query", "queries"], ["ddl", "create tables"], ["paper", "paper only"]].forEach(function (k) { fw.appendChild(wcrumbChip(k[1], V.w.kind === k[0], function () { V.w.kind = k[0]; render(); })); });
    [["all", "any db"], ["co", "company"], ["shop", "shop"]].forEach(function (k) { fw.appendChild(wcrumbChip(k[1], V.w.db === k[0], function () { V.w.db = k[0]; render(); })); });
    [[0, "any level"], [1, "easy"], [2, "medium"], [3, "hard"]].forEach(function (k) { fw.appendChild(wcrumbChip(k[1], V.w.tier === k[0], function () { V.w.tier = k[0]; render(); })); });
    box.appendChild(fw);

    var list = tasks.filter(function (t) {
      return (V.w.kind === "all" || t.kind === V.w.kind) && (V.w.db === "all" || t.db === V.w.db) && (!V.w.tier || t.tier === V.w.tier);
    });
    var row = el("div", "runrow");
    var nxt = list.filter(function (t) { return !state.wr.done[t.id]; });
    var rb = el("button", "btn primary", nxt.length ? "random unsolved (" + nxt.length + ")" : "all solved here"); rb.type = "button"; rb.disabled = !nxt.length;
    rb.addEventListener("click", function () { openWTask(nxt[Math.floor(Math.random() * nxt.length)].id, V.w.mode); });
    row.appendChild(rb); row.appendChild(el("span", "sp"));
    row.appendChild(el("span", "kbd", list.length + " tasks shown"));
    box.appendChild(row);
    f.appendChild(box);

    var ul = el("div", "tier");
    list.forEach(function (t) {
      var b = el("button", "ex" + (state.wr.done[t.id] ? " done" : "")); b.type = "button";
      b.appendChild(el("span", "id", t.id));
      var tt = el("span", "t"); tt.appendChild(document.createTextNode(t.title));
      var meta = el("span", "wmeta", " " + t.tag + " · " + TIERN[t.tier] + " · " + (DBN[t.db] ? DBN[t.db] + " · " : "") + t.mins + " min");
      tt.appendChild(meta);
      b.appendChild(tt);
      var pm = state.wr.paper[t.id];
      b.appendChild(el("span", "tick" + (state.wr.done[t.id] ? " on" : ""), state.wr.done[t.id] ? "OK" : (pm ? pm.got + "/" + pm.of : "—")));
      b.addEventListener("click", function () { openWTask(t.id, V.w.mode); });
      ul.appendChild(b);
    });
    f.appendChild(ul);
    return f;
  }

  function schemaBox(db) {
    var tables = db === "shop" ? MAT.write.shopTables : SEED.tables;
    var sch = el("div", "schema");
    tables.forEach(function (t) {
      var b = el("div", "tbl");
      var h = el("div", "tbl-h"); h.appendChild(el("span", null, t.name)); b.appendChild(h);
      var cols = el("div", "cols");
      t.cols.forEach(function (c) { var r = el("div", "col"); r.appendChild(el("b", null, c[0])); r.appendChild(el("i", null, c[1])); cols.appendChild(r); });
      b.appendChild(cols); sch.appendChild(b);
    });
    return sch;
  }

  function wTaskScreen() {
    var t = wTask(V.w.id), f = document.createDocumentFragment();
    var paper = V.w.mode === "paper" || t.kind === "paper";
    var crumb = el("div", "crumb");
    crumb.appendChild(el("span", "now", t.id));
    crumb.appendChild(el("span", null, t.tag + " · " + TIERN[t.tier]));
    crumb.appendChild(el("span", "sp"));
    var clk = el("span", "qclock", "0:00"); clk.id = "wclock"; crumb.appendChild(clk);
    crumb.appendChild(el("span", null, "target " + t.mins + " min"));
    var back = el("button", "btn ghost", "all tasks"); back.type = "button";
    back.addEventListener("click", function () { clearInterval(V.wtimer); V.screen = "write"; render(); });
    crumb.appendChild(back);
    f.appendChild(crumb);

    var qb = el("div", "qbox");
    qb.appendChild(el("h2", null, t.id + " · " + t.title));
    var task = el("div", "task"); task.style.whiteSpace = "pre-wrap"; task.textContent = t.task; qb.appendChild(task);
    if (t.want) qb.appendChild(el("div", "want", "Expected: " + t.want));
    if (t.kind === "query") {
      var sb = el("button", "btn ghost", V.w.schema ? "hide the tables" : "show the tables (" + DBN[t.db] + ")"); sb.type = "button";
      sb.addEventListener("click", function () { V.w.schema = !V.w.schema; render(); });
      qb.appendChild(sb);
      if (V.w.schema) qb.appendChild(schemaBox(t.db));
    } else if (t.kind === "ddl") {
      qb.appendChild(el("div", "dialect", (t.pre ? "These already exist: " + t.pre : "The database starts empty.") + " Write portable SQL or MySQL (SQLite runs it here: CONCAT, IFNULL, YEAR, MONTH, DAY, DATEDIFF, DATE_FORMAT, CURDATE, NOW, LEFT, RIGHT, CHAR_LENGTH and LIMIT all work; INTERVAL arithmetic and GROUP_CONCAT ... SEPARATOR do not). Use exact table and column names from the task."));
    } else {
      qb.appendChild(el("div", "dialect", "Paper task: write your answer in the box (or on paper), then reveal the model answer and mark yourself against the checklist."));
    }

    var ta = document.createElement("textarea");
    ta.id = "editor"; ta.spellcheck = false;
    ta.placeholder = paper ? "Write your answer here (or on paper)..." : (t.kind === "ddl" ? "CREATE TABLE ..." : "SELECT ...");
    if (paper) ta.style.minHeight = "220px";
    var key = "w:" + t.id;
    ta.value = state.wr.drafts[key] || "";
    ta.addEventListener("input", function () { state.wr.drafts[key] = ta.value; });
    qb.appendChild(ta);

    var row = el("div", "runrow");
    if (!paper) {
      var rb = el("button", "btn primary", "run"); rb.type = "button"; rb.disabled = engine !== "ready";
      rb.addEventListener("click", wDoRun); row.appendChild(rb);
      var cb = el("button", "btn", "check answer"); cb.type = "button"; cb.disabled = engine !== "ready";
      cb.addEventListener("click", wDoCheck); row.appendChild(cb);
      row.appendChild(el("span", "kbd", "ctrl+enter to run"));
    }
    row.appendChild(el("span", "sp"));
    var hb = el("button", "btn ghost", V.w.revealed ? "hide the model answer" : (paper ? "reveal the model answer" : "reveal solution")); hb.type = "button";
    hb.addEventListener("click", function () { V.w.revealed = !V.w.revealed; render(); });
    row.appendChild(hb);
    qb.appendChild(row);

    if (V.w.verdict) {
      var v = el("div", "verdict " + V.w.verdict.kind); v.appendChild(el("b", null, V.w.verdict.head));
      var bd = el("div"); bd.style.whiteSpace = "pre-wrap"; bd.textContent = V.w.verdict.body; v.appendChild(bd); qb.appendChild(v);
    }
    if (V.w.checks) {
      var cl = el("div", "checks");
      V.w.checks.forEach(function (c) { var r = el("div", "chkrow " + (c.ok ? "ok" : "no")); r.appendChild(el("span", "cm", c.ok ? "✓" : "✗")); r.appendChild(el("span", null, c.label + (c.note ? "  —  " + c.note : ""))); cl.appendChild(r); });
      qb.appendChild(cl);
    }
    if (V.w.revealed) {
      var sol = el("div", "rpanel"); var sh = el("div", "rpanel-h"); sh.appendChild(el("span", null, "model answer")); sol.appendChild(sh);
      var pre = el("pre", "code"); pre.textContent = t.kind === "paper" ? t.model : t.ref; sol.appendChild(pre);
      if (t.hint) { var hn = el("div", "empty"); hn.style.whiteSpace = "pre-wrap"; hn.style.borderTop = "1px solid var(--edge)"; hn.textContent = t.hint; sol.appendChild(hn); }
      qb.appendChild(sol);
      if (paper) {
        var items = t.kind === "paper" ? t.rubric : RUBRIC[t.kind];
        var rbx = el("div", "rubric"); rbx.appendChild(el("b", null, "mark yourself honestly"));
        items.forEach(function (it, i) {
          var l = el("label", "rubrow"); var c = document.createElement("input"); c.type = "checkbox"; c.checked = !!V.w.rubric[i];
          c.addEventListener("change", function () { V.w.rubric[i] = c.checked; });
          l.appendChild(c); l.appendChild(el("span", null, it)); rbx.appendChild(l);
        });
        var sv = el("button", "btn primary", "save my mark"); sv.type = "button";
        sv.addEventListener("click", function () {
          var got = 0; items.forEach(function (it, i) { if (V.w.rubric[i]) got++; });
          state.wr.paper[t.id] = { got: got, of: items.length };
          if (got / items.length >= 0.8) state.wr.done[t.id] = 1; else delete state.wr.done[t.id];
          V.w.verdict = { kind: got / items.length >= 0.8 ? "pass" : "fail", head: "saved " + got + " / " + items.length, body: got / items.length >= 0.8 ? "Counts as done." : "Under 80%: re-read the model answer, then redo it from a blank page." };
          save(); render();
        });
        rbx.appendChild(sv);
        qb.appendChild(rbx);
      }
    }
    f.appendChild(qb);
    if (V.w.out) f.appendChild(resultTable(V.w.out, "your result"));
    return f;
  }

  function wSql() { var t = wTask(V.w.id); return (state.wr.drafts["w:" + t.id] || "").trim(); }

  function wDoRun() {
    var t = wTask(V.w.id), sql = wSql();
    if (!sql) { V.w.verdict = { kind: "err", head: "nothing to run", body: "Type something first." }; render(); return; }
    V.w.checks = null;
    try {
      if (t.kind === "ddl") {
        var d = wOpen("empty", t.pre);
        try { d.run(sql); var r = d.exec("SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%' ORDER BY name"); V.w.out = lastResult(r); }
        finally { d.close(); }
        V.w.verdict = { kind: "pass", head: "ran without errors", body: "These are the tables that now exist. Press check answer to test your rules." };
      } else {
        V.w.out = wExec(t, sql); V.w.verdict = null;
      }
    } catch (e) { V.w.out = null; V.w.verdict = { kind: "err", head: "sql error", body: String(e.message || e) }; }
    render();
  }

  function wDoCheck() {
    var t = wTask(V.w.id), sql = wSql();
    if (!sql) { V.w.verdict = { kind: "err", head: "nothing to check", body: "Type something first." }; render(); return; }
    V.w.checks = null;
    if (t.kind === "ddl") return wCheckDdl(t, sql);
    var got, want;
    try { got = wExec(t, sql); } catch (e) { V.w.out = null; V.w.verdict = { kind: "err", head: "sql error", body: String(e.message || e) }; render(); return; }
    try { want = wExec(t, t.ref); } catch (e2) { V.w.verdict = { kind: "err", head: "reference failed", body: "My reference errored (my bug): " + String(e2.message || e2) }; render(); return; }
    V.w.out = got;
    var r = compare(got, want, t.verify ? true : t.ordered);
    state.wr.tries[t.id] = (state.wr.tries[t.id] || 0) + 1;
    if (r.ok) {
      state.wr.done[t.id] = 1;
      V.w.verdict = { kind: "pass", head: "correct", body: "Matches the expected result. Time " + fmtClock(Math.round((Date.now() - V.w.t0) / 1000)) + " (target " + t.mins + " min). " + (t.hint || "") };
    } else {
      V.w.verdict = { kind: "fail", head: "not matching — " + r.why,
        body: "Expected " + want.values.length + " row(s) x " + want.columns.length + " column(s); you returned " + got.values.length + " x " + got.columns.length + "." + (t.ordered && !t.verify ? " Order matters here." : "") };
    }
    save(); render();
  }

  function wCheckDdl(t, sql) {
    var d, bytes;
    try { d = wOpen("empty", t.pre); d.run(sql); bytes = d.export(); d.close(); }
    catch (e) { V.w.out = null; V.w.verdict = { kind: "err", head: "sql error", body: String(e.message || e) }; render(); return; }
    var results = [], pass = 0;
    t.checks.forEach(function (c) {
      var db = new SQLmod.Database(bytes), res = { label: c.label, ok: false, note: "" };
      try {
        db.run("PRAGMA foreign_keys = ON;");
        var setupOk = true;
        if (c.setup) { try { db.run(c.setup); } catch (e1) { setupOk = false; res.note = "valid data was rejected: " + String(e1.message || e1); } }
        if (setupOk) {
          var ran = true, err = "";
          try { db.run(c.sql); } catch (e2) { ran = false; err = String(e2.message || e2); }
          if (ran !== c.ok) res.note = c.ok ? "this should have worked but failed: " + err : "this should have been rejected but was accepted";
          else if (c.after) {
            var rr = db.exec(c.after), val = rr.length && rr[0].values.length ? String(rr[0].values[0][0]) : "";
            if (val === c.expect) res.ok = true; else res.note = "expected " + c.expect + ", got " + val;
          } else res.ok = true;
        }
      } catch (e3) { res.note = String(e3.message || e3); }
      try { db.close(); } catch (e4) {}
      if (res.ok) pass++;
      results.push(res);
    });
    V.w.checks = results;
    state.wr.tries[t.id] = (state.wr.tries[t.id] || 0) + 1;
    if (pass === results.length) {
      state.wr.done[t.id] = 1;
      V.w.verdict = { kind: "pass", head: "all " + results.length + " checks passed", body: "Your schema accepts the good rows and rejects the bad ones. Time " + fmtClock(Math.round((Date.now() - V.w.t0) / 1000)) + " (target " + t.mins + " min)." };
    } else {
      V.w.verdict = { kind: "fail", head: pass + " of " + results.length + " checks passed", body: "Fix the lines marked with a cross. Names must match the task exactly." };
    }
    save(); render();
  }

  document.addEventListener("keydown", function (ev) {
    if ((ev.ctrlKey || ev.metaKey) && ev.key === "Enter" && V.screen === "wtask" && V.w.mode !== "paper") { wDoRun(); ev.preventDefault(); }
  });

