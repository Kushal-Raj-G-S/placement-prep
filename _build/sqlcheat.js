
  /* ---------- syntax cheat sheet: syntax + example on the left, the real tables on the right ---------- */
  var cheatBytes = null;
  function openCheat() { V.screen = "cheat"; render(); window.scrollTo(0, 0); }

  function cheatDb() {                         // a throw-away copy every time, so a DELETE in an example never sticks
    if (!cheatBytes) {
      var d = new SQLmod.Database(seedBytes); d.run(MAT.write.shopSql); d.run(MAT.cheatSql);
      cheatBytes = d.export(); d.close();
    }
    return new SQLmod.Database(cheatBytes);
  }
  function cheatTable(cols, rows, limit) {
    var wrap = el("div", "cres"), t = document.createElement("table"), th = document.createElement("tr");
    cols.forEach(function (c) { th.appendChild(el("th", null, c)); }); t.appendChild(th);
    rows.slice(0, limit).forEach(function (r) {
      var tr = document.createElement("tr");
      r.forEach(function (v) { tr.appendChild(el("td", v === null ? "nul" : null, v === null ? "NULL" : String(v))); });
      t.appendChild(tr);
    });
    wrap.appendChild(t);
    if (rows.length > limit) wrap.appendChild(el("div", "small", "showing " + limit + " of " + rows.length + " rows"));
    return wrap;
  }
  function cheatRun(host, sql) {
    host.textContent = "";
    var d = null;
    try {
      d = cheatDb();
      var res = d.exec(sql.replace(/--.*$/gm, "").trim());   // sql.js fails on a comment after the last statement
      if (!res.length) { host.appendChild(el("div", "cok", "ran without error. It returns no rows (it ran on a throw-away copy, so the demo data is unchanged).")); return; }
      var last = res[res.length - 1];
      host.appendChild(el("div", "clabel", last.values.length + " row" + (last.values.length === 1 ? "" : "s") + " returned"));
      host.appendChild(cheatTable(last.columns, last.values, 40));
    } catch (e) { if (window.console) console.error("cheat run failed", e && e.stack); host.appendChild(el("div", "cerr", "error: " + e.message)); }
    finally { if (d) d.close(); }
  }

  function cheatData() {
    var pane = el("div", "dpane");
    pane.appendChild(el("div", "lab", "the real tables (the Run buttons use exactly these)"));
    var chips = el("div", "chcheat"), view = el("div", "dview");
    var names = [];
    try {
      var d0 = cheatDb();
      var r0 = d0.exec("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name");
      names = r0.length ? r0[0].values.map(function (v) { return v[0]; }) : [];
      d0.close();
    } catch (e) {}
    var order = ["employees", "departments", "projects", "assignments", "logins", "customers", "products", "orders", "order_items", "sales", "yearly", "person", "seat", "station", "stock", "accounts"];
    names.sort(function (a, b) { var i = order.indexOf(a), j = order.indexOf(b); return (i < 0 ? 99 : i) - (j < 0 ? 99 : j); });
    function show(n, btn) {
      [].forEach.call(chips.children, function (c) { c.classList.remove("on"); });
      btn.classList.add("on");
      view.textContent = "";
      var d = cheatDb();
      try {
        var info = d.exec("PRAGMA table_info(" + n + ")")[0];
        view.appendChild(el("div", "cols", n + "(" + info.values.map(function (v) { return v[1] + " " + String(v[2]).toLowerCase() + (v[5] ? " pk" : ""); }).join(", ") + ")"));
        var r = d.exec("SELECT * FROM " + n)[0];
        view.appendChild(cheatTable(r.columns, r.values, 60));
      } catch (e) { view.appendChild(el("div", "cerr", String(e.message))); }
      d.close();
    }
    names.forEach(function (n, i) {
      var b = el("button", "chipj", n); b.type = "button";
      b.addEventListener("click", function () { show(n, b); });
      chips.appendChild(b);
      if (i === 0) setTimeout(function () { show(n, b); }, 0);
    });
    pane.appendChild(chips); pane.appendChild(view);
    pane.appendChild(el("div", "small", "Pick a table to see its rows. These are SQLite tables, so an example that needs a real MySQL server shows its syntax and has no Run button."));
    return pane;
  }

  function cheatScreen() {
    var f = document.createDocumentFragment();
    var hero = el("div", "hero");
    var back = el("button", "btn ghost", "← back to the roadmap"); back.type = "button";
    back.addEventListener("click", function () { V.screen = "study"; render(); window.scrollTo(0, 0); });
    hero.appendChild(back);
    var h1 = el("h1"); h1.innerHTML = "SQL syntax. <em>See it run.</em>"; h1.style.marginTop = "12px"; hero.appendChild(h1);
    hero.appendChild(el("p", null, "Left: the syntax and an example on the real tables, with a Run button. Right: the tables themselves, so you can check the result by eye. MySQL first, with the PostgreSQL / SQL Server spelling only where it differs."));
    var q = document.createElement("input"); q.type = "search"; q.className = "sfind";
    q.placeholder = "search: join, window, trigger, DATEDIFF, LIMIT, upsert, NULL…";
    hero.appendChild(q);
    var chips = el("div", "chcheat"); hero.appendChild(chips);
    f.appendChild(hero);

    var split = el("div", "split2"), left = el("div", "lcol"), right = el("div", "rcol");
    var blocks = [];
    MAT.cheat.forEach(function (sec) {
      var c = el("a", "chipj", sec.title); c.href = "#cs-" + sec.id;
      c.addEventListener("click", function (e) { e.preventDefault(); var t = document.getElementById("cs-" + sec.id); if (t) t.scrollIntoView({ behavior: "smooth", block: "start" }); });
      chips.appendChild(c);
      var box = el("div", "tier stage cheatsec"); box.id = "cs-" + sec.id;
      var h = el("div", "tier-h"); h.appendChild(el("h3", null, sec.title)); h.appendChild(el("span", "c", sec.items.length + " items")); box.appendChild(h);
      var rows = [];
      sec.items.forEach(function (it) {
        var row = el("div", "citem");
        row.appendChild(el("div", "chead")).appendChild(el("span", "clab", it.l));
        if (it.s) { row.appendChild(el("div", "ctag", "syntax")); row.appendChild(el("pre", "ccode syn", it.s)); }
        row.appendChild(el("div", "ctag", it.s ? "example (MySQL)" : "syntax and example (MySQL)"));
        row.appendChild(el("pre", "ccode", it.c));
        var actions = el("div", "cacts"), out = el("div", "cout");
        var cp = el("button", "btn ghost cpy", "copy"); cp.type = "button";
        cp.addEventListener("click", function () { try { navigator.clipboard.writeText(it.c); cp.textContent = "copied"; setTimeout(function () { cp.textContent = "copy"; }, 1200); } catch (e) { cp.textContent = "select it"; } });
        actions.appendChild(cp);
        if (it.rc) {
          var rb = el("button", "btn primary cpy", "▶ run this"); rb.type = "button";
          rb.addEventListener("click", function () { cheatRun(out, it.c); });
          actions.appendChild(rb);
          row.appendChild(actions);
        } else if (it.t) {
          actions.appendChild(el("span", "cnote", "MySQL-only spelling, and the demo database is SQLite. Same idea, runnable:"));
          row.appendChild(actions);
          row.appendChild(el("pre", "ccode demo", it.t));
          var a2 = el("div", "cacts"), rb2 = el("button", "btn primary cpy", "▶ run the demo version"); rb2.type = "button";
          rb2.addEventListener("click", function () { cheatRun(out, it.t); });
          a2.appendChild(rb2); row.appendChild(a2);
        } else {
          actions.appendChild(el("span", "cnote", "syntax only: needs a real MySQL server, or there is nothing to show"));
          row.appendChild(actions);
        }
        row.appendChild(out);
        box.appendChild(row);
        rows.push({ node: row, hay: (it.l + " " + it.c + " " + it.s + " " + (it.t || "")).toLowerCase() });
      });
      left.appendChild(box);
      blocks.push({ box: box, rows: rows, title: sec.title.toLowerCase() });
    });
    var none = el("div", "small", "Nothing matches that. Try a shorter word."); none.style.display = "none"; none.style.padding = "16px"; left.appendChild(none);
    right.appendChild(cheatData());
    split.appendChild(left); split.appendChild(right); f.appendChild(split);

    q.addEventListener("input", function () {
      var s = q.value.trim().toLowerCase(), any = false;
      blocks.forEach(function (b) {
        var shown = 0;
        b.rows.forEach(function (r) { var ok = !s || r.hay.indexOf(s) >= 0 || b.title.indexOf(s) >= 0; r.node.style.display = ok ? "" : "none"; if (ok) shown++; });
        b.box.style.display = shown ? "" : "none";
        if (shown) any = true;
      });
      none.style.display = any ? "none" : "";
    });
    return f;
  }
