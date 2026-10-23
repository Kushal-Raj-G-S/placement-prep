# -*- coding: utf-8 -*-
"""
Injects the pattern library (pattern_library.py) into "8 - Pattern Radar (name the pattern).html"
as a new LEARN half, and leaves the file self-contained and offline-capable.

    python build_radar.py

The first run stashes the untouched original in  .radar_src.html  and every later run rebuilds
from that stash, so editing the library and re-running never compounds patches.
"""
import json, os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)   # the materials folder (this file lives in _build/)
TARGET = os.path.join(ROOT, "8 - Pattern Radar (name the pattern).html")
SRC = os.path.join(HERE, ".radar_src.html")

sys.path.insert(0, HERE)
import pattern_library as PL

# ---------------------------------------------------------------- the styles ------
CSS = r"""
  /* ---------- learn half ---------- */
  .lead{color:var(--dim);font-size:14.5px;max-width:70ch;margin:0}
  .lead b{color:var(--txt);font-weight:600}
  .counts{display:flex;gap:18px;flex-wrap:wrap;font-family:var(--mono);font-size:11px;letter-spacing:.09em;
          text-transform:uppercase;color:var(--dim2)}
  .counts b{color:var(--cy);font-size:15px;font-weight:700;letter-spacing:0;margin-right:5px}

  .gblock{display:flex;flex-direction:column;gap:9px}
  .ghead{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;padding-top:4px}
  .ghead h3{margin:0;font-size:16px}
  .ghead .gn{font-family:var(--mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--dim2)}
  .ghead p{margin:0;color:var(--dim);font-size:13px;flex:1 1 240px}

  .pcards{display:grid;grid-template-columns:repeat(auto-fill,minmax(248px,1fr));gap:9px}
  .pcard{text-align:left;background:var(--panel);border:1px solid var(--edge);border-radius:11px;padding:13px 14px;
         cursor:pointer;display:flex;flex-direction:column;gap:7px;transition:border-color .12s ease,transform .08s ease}
  .pcard:hover{border-color:var(--cy);transform:translateY(-1px)}
  .pcard .pn{font-size:15.5px;font-weight:600}
  .pcard .pb{color:var(--dim);font-size:12.5px;line-height:1.45}
  .pcard .pm{display:flex;align-items:center;gap:8px;font-family:var(--mono);font-size:10px;letter-spacing:.07em;
             text-transform:uppercase;color:var(--dim2);margin-top:auto;padding-top:4px}
  .pcard .pm .done{color:var(--ok)}
  .pcard .pm .tcount{color:var(--vi)}
  .mini{flex:1 1 40px;height:3px;background:var(--edge);border-radius:2px;overflow:hidden;min-width:34px}
  .mini i{display:block;height:100%;background:var(--ok)}

  .phead{display:flex;flex-direction:column;gap:9px;padding:19px 18px;border:1px solid var(--edge);border-radius:13px;
         background:linear-gradient(160deg,var(--panel) 0%,var(--bg2) 100%)}
  .phead h2{margin:0;font-family:var(--mono);font-size:clamp(21px,4vw,28px);letter-spacing:-.01em}
  .phead .meta{display:flex;gap:8px;flex-wrap:wrap}
  .chipm{font-family:var(--mono);font-size:10px;letter-spacing:.08em;text-transform:uppercase;border:1px solid var(--edge2);
         border-radius:5px;padding:3px 8px;color:var(--dim)}
  .chipm b{color:var(--cy);font-weight:600}
  .phead .core{color:var(--txt);font-size:14.5px;line-height:1.62;max-width:72ch}
  .phead .core code{font-family:var(--mono);font-size:13px;color:var(--cy)}

  .nots{display:flex;flex-direction:column;gap:7px}
  .not{display:grid;grid-template-columns:16px 1fr;gap:9px;font-size:13.5px;color:var(--dim);line-height:1.55}
  .not .x{color:var(--no);font-family:var(--mono);font-weight:700}
  .not b{color:var(--txt);font-weight:600}
  .not code{font-family:var(--mono);font-size:12.5px;color:var(--cy)}

  .picks{display:flex;flex-direction:column;gap:0}
  .pick{display:grid;grid-template-columns:1fr auto;gap:10px;align-items:center;padding:9px 0;border-bottom:1px solid var(--edge);
        background:none;border-left:0;border-right:0;border-top:0;cursor:pointer;text-align:left;width:100%}
  .pick:last-child{border-bottom:0}
  .pick .cond{font-size:13.5px;color:var(--txt)}
  .pick .cond i{font-style:normal;color:var(--dim2);font-family:var(--mono);font-size:10px;letter-spacing:.1em;
                text-transform:uppercase;margin-right:7px}
  .pick .go{font-family:var(--mono);font-size:12px;color:var(--cy);white-space:nowrap}
  .pick:hover .go{text-decoration:underline}

  details.vr{background:var(--panel);border:1px solid var(--edge);border-radius:11px;overflow:hidden}
  details.vr[open]{border-color:var(--edge2)}
  details.vr summary{list-style:none;cursor:pointer;padding:13px 15px;display:flex;gap:11px;align-items:baseline;flex-wrap:wrap}
  details.vr summary::-webkit-details-marker{display:none}
  details.vr summary:hover{background:var(--panel2)}
  .vr .tw{font-family:var(--mono);font-size:11px;color:var(--dim2);transition:transform .15s ease}
  details.vr[open] .tw{transform:rotate(90deg);color:var(--cy)}
  .vr .vname{font-size:15.5px;font-weight:600;flex:0 0 auto}
  .vr .vwhen{color:var(--dim);font-size:13px;flex:1 1 180px}
  .vr .trace{font-family:var(--mono);font-size:9px;letter-spacing:.07em;text-transform:uppercase;color:var(--vi);
             border:1px solid var(--vi);background:var(--vi-dim);border-radius:4px;padding:2px 6px;flex:0 0 auto}
  .vr .tick{font-family:var(--mono);font-size:9.5px;letter-spacing:.09em;text-transform:uppercase;border:1px solid var(--edge2);
            border-radius:5px;padding:3px 8px;background:transparent;cursor:pointer;color:var(--dim2);white-space:nowrap}
  .vr .tick:hover{border-color:var(--ok);color:var(--ok)}
  .vr .tick.on{background:var(--ok-dim);border-color:var(--ok);color:var(--ok)}
  .vbody{padding:0 15px 15px;display:flex;flex-direction:column;gap:13px;border-top:1px solid var(--edge)}
  .vbody .lab{font-family:var(--mono);font-size:9.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--dim2);
              margin:3px 0 -6px}

  .facts{display:flex;flex-direction:column;gap:0;margin-top:13px}
  .fact{display:grid;grid-template-columns:104px 1fr;gap:12px;padding:7px 0;border-bottom:1px solid var(--edge);font-size:13.5px}
  .fact:last-child{border-bottom:0}
  .fact .fl{font-family:var(--mono);font-size:9.5px;letter-spacing:.11em;text-transform:uppercase;color:var(--dim2);padding-top:3px}
  .fact .fv{color:var(--txt);line-height:1.55}
  .fact .fv code{font-family:var(--mono);font-size:12.5px;color:var(--cy)}
  .fact.cxf .fv{font-family:var(--mono);font-size:12.5px;color:var(--cy)}

  pre.code{margin:0;background:#04080D;border:1px solid var(--edge2);border-radius:9px;padding:12px 13px;overflow-x:auto;
           font-family:var(--mono);font-size:12.5px;line-height:1.62;color:var(--txt);white-space:pre;tab-size:4}
  pre.code .cm{color:var(--dim2)}

  .asks{margin:0;padding:0;list-style:none;display:flex;flex-direction:column;gap:0;counter-reset:a}
  .asks li{display:grid;grid-template-columns:24px 1fr;gap:9px;padding:6px 0;border-bottom:1px solid var(--edge);
           font-size:13.5px;color:var(--txt);line-height:1.5}
  .asks li:last-child{border-bottom:0}
  .asks li::before{counter-increment:a;content:counter(a,decimal-leading-zero);font-family:var(--mono);font-size:10px;
                   color:var(--dim2);padding-top:3px}
  .asks li code{font-family:var(--mono);font-size:12.5px;color:var(--cy)}

  .exs{display:flex;flex-wrap:wrap;gap:6px}
  .ex{font-size:12.5px;background:var(--bg2);border:1px solid var(--edge);border-radius:7px;padding:6px 10px;color:var(--txt);
      text-decoration:none;display:inline-flex;align-items:baseline;gap:7px;transition:border-color .12s ease,background .12s ease}
  a.ex:hover{border-color:var(--cy);background:var(--panel2)}
  a.ex:hover .exn{text-decoration:underline}
  .ex .pl{font-family:var(--mono);font-size:9px;letter-spacing:.07em;text-transform:uppercase;border-radius:4px;padding:2px 5px;
          border:1px solid var(--edge2);color:var(--dim2);white-space:nowrap}
  .ex .pl.LeetCode{color:var(--am);border-color:var(--am-dim);background:var(--am-dim)}
  .ex .pl.GeeksforGeeks{color:var(--ok);border-color:var(--ok-dim);background:var(--ok-dim)}
  .ex .pl.HackerRank{color:var(--cy);border-color:var(--cy-dim);background:var(--cy-dim)}
  .ex .pl.Codeforces{color:var(--vi);border-color:var(--vi-dim);background:var(--vi-dim)}
  .ex .pl.HackerEarth{color:var(--no);border-color:var(--no-dim);background:var(--no-dim)}
  .ex .sfx{font-family:var(--mono);font-size:9.5px;color:var(--dim2)}
  .ex[hidden]{display:none!important}

  .pfilter{display:flex;gap:6px;flex-wrap:wrap;align-items:center}
  .pf{font-family:var(--mono);font-size:10px;letter-spacing:.07em;text-transform:uppercase;background:var(--bg2);
      border:1px solid var(--edge2);border-radius:6px;padding:5px 9px;cursor:pointer;color:var(--dim)}
  .pf:hover{border-color:var(--cy);color:var(--txt)}
  .pf.on{background:var(--cy);border-color:var(--cy);color:#04222A;font-weight:600}
  .pf .n{opacity:.6;margin-left:4px}

  .rail{display:flex;flex-wrap:wrap;gap:7px}
  .hub{display:inline-flex;align-items:center;gap:7px;font-family:var(--mono);font-size:11px;letter-spacing:.05em;
       background:var(--panel2);border:1px solid var(--edge2);border-radius:7px;padding:8px 11px;color:var(--txt);text-decoration:none}
  .hub:hover{border-color:var(--cy)}
  .hub .ar{color:var(--dim2)}
  .hub:hover .ar{color:var(--cy)}

  .traps{margin:0;padding:0;list-style:none;display:flex;flex-direction:column;gap:7px}
  .traps li{display:grid;grid-template-columns:16px 1fr;gap:9px;font-size:13.5px;color:var(--am);line-height:1.55}
  .traps li .w{font-family:var(--mono);font-weight:700}
  .traps li code{font-family:var(--mono);font-size:12.5px;color:var(--txt)}
  .traps li i{font-style:italic;color:var(--am)}

  /* ---------- the trace player ---------- */
  .viz{background:#04080D;border:1px solid var(--edge2);border-radius:10px;padding:12px 13px;display:flex;
       flex-direction:column;gap:11px}
  .viz .vcap{font-family:var(--mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--dim2)}
  .vform{display:flex;gap:8px;align-items:flex-end;flex-wrap:wrap;padding-bottom:3px;border-bottom:1px solid var(--edge)}
  .vf{display:flex;flex-direction:column;gap:4px;flex:1 1 150px;min-width:110px}
  .vfl{font-family:var(--mono);font-size:9px;letter-spacing:.09em;text-transform:uppercase;color:var(--dim2)}
  .vfi{background:var(--bg2);border:1px solid var(--edge2);border-radius:6px;padding:7px 9px;color:var(--txt);
       font-family:var(--mono);font-size:13px;width:100%}
  .vfi:focus{outline:none;border-color:var(--cy)}
  .vfi.num{flex:0 0 72px;max-width:84px}
  .vf:has(.num){flex:0 0 auto}
  .vb.go2{background:var(--am);border-color:var(--am);color:#332714}
  .vb.go2:hover{background:#FFD47A}
  .verr{font-size:12.5px;line-height:1.5;color:var(--no);background:var(--no-dim);border:1px solid var(--no);
        border-radius:6px;padding:7px 10px}
  .verr.soft{color:var(--am);background:var(--am-dim);border-color:var(--am)}
  .vmount{display:flex;flex-direction:column;gap:11px}
  .vpending{font-size:12.5px;line-height:1.55;color:var(--dim2);border:1px dashed var(--edge2);border-radius:8px;
            padding:9px 12px}
  .vpending b{color:var(--dim);font-weight:600}
  .vstageWrap{display:flex;flex-direction:column;gap:11px}

  /* grid stage */
  .gridwrap{display:inline-grid;gap:4px;min-width:min-content}
  .gcell{position:relative;display:flex;flex-direction:column;align-items:center;gap:2px}
  .gptr{height:13px;font-family:var(--mono);font-size:8.5px;letter-spacing:.03em;color:var(--cy);
        white-space:nowrap;display:flex;gap:3px}
  .gridwrap .cell{min-width:34px;height:32px;font-size:13px}

  /* tree stage */
  .treewrap{position:relative;min-width:min-content}
  .treewrap .cell{position:absolute;width:34px;min-width:34px;height:30px;font-size:13px;z-index:2}
  .tlines{position:absolute;left:0;top:0;overflow:visible}
  .tlines line{stroke:var(--edge2);stroke-width:1.5}
  .tptr{position:absolute;width:56px;text-align:center;font-family:var(--mono);font-size:8.5px;
        color:var(--cy);white-space:nowrap;z-index:3}

  /* graph stage */
  .graphwrap{position:relative;margin:0 auto;min-width:min-content}
  .graphwrap .cell{position:absolute;width:34px;min-width:34px;height:34px;border-radius:50%;font-size:13px;z-index:2}
  .glines{position:absolute;left:0;top:0;overflow:visible}
  .glines line{stroke:var(--edge2);stroke-width:1.5}
  .glines line.epick{stroke:var(--cy);stroke-width:3}
  .glines line.edone{stroke:var(--ok);stroke-width:3}
  .glines line.ebad{stroke:var(--no);stroke-width:2;stroke-dasharray:4 3}
  .glines line.egone{stroke:var(--edge);stroke-width:1;stroke-dasharray:2 4}
  .glines .gw{fill:var(--dim);font-family:var(--mono);font-size:10px;text-anchor:middle}
  .vstage{overflow-x:auto;padding-bottom:2px}
  .cells{display:flex;gap:4px;min-width:min-content}
  .cwrap{display:flex;flex-direction:column;align-items:center;gap:3px;min-width:34px}
  .ptrs{height:15px;display:flex;gap:3px;align-items:flex-end;font-family:var(--mono);font-size:9px;
        letter-spacing:.04em;color:var(--cy);white-space:nowrap}
  .cell{min-width:34px;height:36px;display:flex;align-items:center;justify-content:center;border-radius:7px;
        border:1px solid var(--edge2);background:var(--panel);font-family:var(--mono);font-size:14px;
        font-weight:600;color:var(--txt);padding:0 6px;transition:background .18s ease,border-color .18s ease,
        transform .18s ease,opacity .18s ease}
  .cell.span{background:var(--cy-dim);border-color:var(--cy)}
  .cell.pick{background:var(--cy);border-color:var(--cy);color:#04222A;transform:translateY(-3px)}
  .cell.done{background:var(--ok-dim);border-color:var(--ok);color:var(--ok)}
  .cell.bad{background:var(--no-dim);border-color:var(--no);color:var(--no)}
  .cell.gone{opacity:.3;border-style:dashed}
  .cidx{font-family:var(--mono);font-size:9px;color:var(--dim2)}
  .vaux{display:flex;flex-wrap:wrap;gap:7px}
  .ab{display:flex;align-items:baseline;gap:7px;background:var(--panel);border:1px solid var(--edge);
      border-radius:7px;padding:5px 9px;font-family:var(--mono);font-size:12px}
  .ab .al{font-size:9px;letter-spacing:.09em;text-transform:uppercase;color:var(--dim2)}
  .ab .av{color:var(--cy);font-weight:600}
  .ab .ai{display:flex;gap:3px;flex-wrap:wrap}
  .ab .ai span{background:var(--bg2);border:1px solid var(--edge2);border-radius:4px;padding:1px 6px;color:var(--txt)}
  .ab .ai .empty{color:var(--dim2);border-style:dashed}
  .vnote{font-size:13.5px;line-height:1.55;color:var(--txt);border-left:3px solid var(--am);
         background:rgba(0,0,0,.35);border-radius:6px;padding:8px 11px;min-height:38px}
  .vcode{font-family:var(--mono);font-size:12px;line-height:1.7;background:var(--bg);border:1px solid var(--edge);
         border-radius:7px;padding:7px 0;overflow-x:auto}
  .vcode .cl{padding:0 11px;color:var(--dim2);white-space:pre;border-left:2px solid transparent}
  .vcode .cl.on{color:var(--txt);background:var(--cy-dim);border-left-color:var(--cy)}
  .vctl{display:flex;gap:7px;align-items:center;flex-wrap:wrap}
  .vb{font-family:var(--mono);font-size:11px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;
      background:var(--panel2);border:1px solid var(--edge2);border-radius:6px;padding:7px 11px;cursor:pointer;color:var(--txt)}
  .vb:hover:not(:disabled){border-color:var(--cy)}
  .vb:disabled{opacity:.35;cursor:default}
  .vb.go{background:var(--cy);border-color:var(--cy);color:#04222A}
  .vstep{font-family:var(--mono);font-size:11px;color:var(--dim2);font-variant-numeric:tabular-nums}
  .vtrack{flex:1 1 80px;height:3px;background:var(--edge);border-radius:2px;overflow:hidden;min-width:60px}
  .vtrack i{display:block;height:100%;background:var(--cy);transition:width .18s ease}

  .pending{color:var(--dim2);font-size:13px;line-height:1.6;border:1px dashed var(--edge2);border-radius:10px;padding:12px 14px}
  .pending b{color:var(--dim);font-weight:600}

  @media(max-width:620px){
    .fact{grid-template-columns:1fr;gap:2px}
    .pick{grid-template-columns:1fr;gap:3px}
    .pick .go{text-align:left}
  }
"""

# ---------------------------------------------------------------- the script ------
JS = r"""
  /* ================= LEARN HALF (built by build_radar.py) ================= */
  /* Deep link from the Mock OA reveal:  ...#p=<pattern-id>&v=<variant-id>  opens that variant directly. */
  (function applyHash() {
    var h = (location.hash || "").replace(/^#/, ""), m = {};
    h.split("&").forEach(function (kv) { var i = kv.indexOf("="); if (i > 0) m[kv.slice(0, i)] = decodeURIComponent(kv.slice(i + 1)); });
    if (m.p) { V.screen = "pattern"; V.pat = m.p; V.focusV = m.v || null; }
  })();
  function focusVar() {
    if (!V.focusV) return;
    var d = document.getElementById("vr-" + V.focusV); V.focusV = null;
    if (d) { d.open = true; setTimeout(function () { d.scrollIntoView({ block: "start" }); }, 60); }
  }
  var LIB = JSON.parse(document.getElementById("lib").textContent);
  var LINKS = JSON.parse(document.getElementById("links").textContent);
  if (!state.known || typeof state.known !== "object") state.known = {};

  /* every problem link on a pattern page, rendered as a real anchor. Platform names come
     from verify_links.py, which only emits a link after it has answered 200 (or, for
     LeetCode and Codeforces, after their own API confirmed the problem exists). */
  function exRow(items) {
    var row = el("div", "exs");
    items.forEach(function (e) {
      var a;
      if (e.u) {
        a = el("a", "ex");
        a.href = e.u; a.target = "_blank"; a.rel = "noopener noreferrer";
        a.title = e.u;
      } else {
        a = el("span", "ex");
      }
      if (e.p) a.setAttribute("data-pl", e.p);
      a.appendChild(el("span", "exn", e.n));
      if (e.p) a.appendChild(el("span", "pl " + e.p.replace(/[^A-Za-z]/g, ""), e.p));
      if (e.s) a.appendChild(el("span", "sfx", e.s));
      row.appendChild(a);
    });
    return row;
  }
  function applyFilter() {
    var want = V.plat || "all";
    Array.prototype.forEach.call(document.querySelectorAll(".ex[data-pl]"), function (n) {
      n.hidden = !(want === "all" || n.getAttribute("data-pl") === want);
    });
    Array.prototype.forEach.call(document.querySelectorAll(".pf"), function (b) {
      b.classList.toggle("on", b.getAttribute("data-pl") === want);
    });
  }

  function allVariants() {
    var n = 0;
    LIB.patterns.forEach(function (p) { n += p.variants.length; });
    return n;
  }
  function allAsks() {
    var n = 0;
    LIB.patterns.forEach(function (p) {
      p.variants.forEach(function (v) { n += (v.asks || []).length; });
    });
    return n;
  }
  function knownIn(p) {
    return p.variants.filter(function (v) { return state.known[v.id]; }).length;
  }
  function patById(id) {
    var r = null;
    LIB.patterns.forEach(function (p) { if (p.id === id) r = p; });
    return r;
  }
  function rich(tag, cls, html) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    n.innerHTML = html;          /* library text only -- authored here, never user input */
    return n;
  }
  function codeBlock(src) {
    var pre = el("pre", "code");
    src.split("\n").forEach(function (line, i) {
      if (i) pre.appendChild(document.createTextNode("\n"));
      var h = line.indexOf("#");
      if (h === -1) { pre.appendChild(document.createTextNode(line)); return; }
      pre.appendChild(document.createTextNode(line.slice(0, h)));
      pre.appendChild(el("span", "cm", line.slice(h)));
    });
    return pre;
  }
  /* ---------- the trace player ----------
     The generators in viz_engine.js run RIGHT HERE in the browser, so the trace is built from
     whatever input you type. build_radar.py fuzz-tests every one of them against a brute-force
     implementation before shipping, so what you watch and what the code does cannot diverge. */
  /* one shared parser map, defined in viz_engine.js and used by viz_test.js too -- two copies
     is how you get a generator the fuzzer accepts and the page cannot parse. */
  var VPARSE = VIZGEN.__helpers.parse;

  function vizPlayer(vid) {
    var gen = VIZGEN[vid];
    var box = el("div", "viz");
    var cap = el("div", "vcap");
    box.appendChild(cap);

    /* --- your input --- */
    var form = el("div", "vform");
    var fields = {};
    gen.input.forEach(function (f) {
      var w = el("label", "vf");
      w.appendChild(el("span", "vfl", f.label));
      var inp = document.createElement("input");
      inp.type = "text";
      inp.className = "vfi" + (f.type === "int" ? " num" : "");
      inp.value = String(f.def);
      inp.spellcheck = false;
      inp.setAttribute("autocomplete", "off");
      inp.addEventListener("keydown", function (ev) {
        ev.stopPropagation();                       /* arrows/enter belong to the field here */
        if (ev.key === "Enter") { ev.preventDefault(); go(); }
      });
      w.appendChild(inp);
      fields[f.id] = inp;
      form.appendChild(w);
    });
    var runBtn = el("button", "vb go2", "run it"); runBtn.type = "button";
    var resetBtn = el("button", "vb", "example"); resetBtn.type = "button";
    resetBtn.title = "put the original example back";
    form.appendChild(runBtn); form.appendChild(resetBtn);
    box.appendChild(form);
    var err = el("div", "verr"); err.hidden = true;
    box.appendChild(err);

    var mount = el("div", "vmount");
    box.appendChild(mount);

    function go() {
      var vals = {}, note = null;
      err.hidden = true;
      try {
        gen.input.forEach(function (f) { vals[f.id] = VPARSE[f.type](fields[f.id].value); });
      } catch (e) {
        err.textContent = e.message; err.hidden = false; return;
      }
      if (gen.prep) note = gen.prep(vals);
      if (gen.check) {
        var bad = gen.check(vals);
        if (bad) { err.textContent = bad; err.hidden = false; return; }
      }
      var res;
      try { res = gen.run(vals); }
      catch (e) { err.textContent = "that input broke the trace: " + e.message; err.hidden = false; return; }
      if (gen.prep) {
        gen.input.forEach(function (f) {
          if (vals[f.id] instanceof Array && f.type === "ints") fields[f.id].value = vals[f.id].join(" ");
        });
      }
      if (note) { err.textContent = note; err.hidden = false; err.className = "verr soft"; }
      else err.className = "verr";
      cap.textContent = "watch it run — " + res.trace.caption;
      mount.textContent = "";
      mount.appendChild(buildStage(res.trace));
    }
    runBtn.addEventListener("click", go);
    resetBtn.addEventListener("click", function () {
      gen.input.forEach(function (f) { fields[f.id].value = String(f.def); });
      go();
    });
    go();
    return box;
  }

  /* ---------- the four stages ----------
     row    a line of cells, indexed 0..n-1          (arrays, strings, timelines)
     grid   r x c of cells, keyed "row,col"          (grids, DP tables, matrices)
     tree   nodes placed by depth, SVG edges          (binary trees, tries)
     graph  nodes on a circle, SVG edges with weights (weighted graphs, DSU)
     Every stage exposes the same two things to draw(): paint(key, className) and
     pointer(key, name), so the frame format does not change between them. */
  var SVGNS = "http://www.w3.org/2000/svg";
  function svg(tag, attrs) {
    var n = document.createElementNS(SVGNS, tag);
    for (var k in attrs) if (attrs.hasOwnProperty(k)) n.setAttribute(k, attrs[k]);
    return n;
  }

  function buildStage(tr) {
    var box = el("div", "vstageWrap");
    var stage = el("div", "vstage");
    var cellOf = {}, ptrOf = {}, edgeOf = {};

    if (tr.kind === "grid") {
      var g = el("div", "gridwrap");
      g.style.gridTemplateColumns = "repeat(" + tr.data.c + ", minmax(34px, auto))";
      for (var r = 0; r < tr.data.r; r++) {
        for (var c = 0; c < tr.data.c; c++) {
          var key = r + "," + c;
          var w = el("div", "gcell");
          var p = el("div", "gptr");
          var cell = el("div", "cell", String(tr.data.cells[r][c]));
          w.appendChild(p); w.appendChild(cell);
          g.appendChild(w);
          cellOf[key] = cell; ptrOf[key] = p;
        }
      }
      stage.appendChild(g);

    } else if (tr.kind === "tree") {
      var nodes = tr.data.nodes;
      var depth = [], order = [], seen = 0;
      (function walk(i, d) {               /* in-order x, depth y */
        if (i < 0 || i == null) return;
        walk(nodes[i].l, d + 1);
        depth[i] = d; order[i] = seen++;
        walk(nodes[i].r, d + 1);
      })(tr.data.root, 0);
      var maxD = 0, k;
      for (k = 0; k < nodes.length; k++) if (depth[k] > maxD) maxD = depth[k];
      var W = Math.max(seen, 1) * 56, HT = (maxD + 1) * 62;
      var holder = el("div", "treewrap");
      holder.style.width = W + "px"; holder.style.height = HT + "px";
      var lines = svg("svg", { width: W, height: HT, class: "tlines" });
      holder.appendChild(lines);
      var xy = function (i) { return [order[i] * 56 + 28, depth[i] * 62 + 20]; };
      for (k = 0; k < nodes.length; k++) {
        if (depth[k] == null) continue;
        ["l", "r"].forEach(function (side) {
          var ch = nodes[k][side];
          if (ch == null || ch < 0 || depth[ch] == null) return;
          var a = xy(k), b = xy(ch);
          lines.appendChild(svg("line", { x1: a[0], y1: a[1] + 2, x2: b[0], y2: b[1] - 2 }));
        });
      }
      for (k = 0; k < nodes.length; k++) {
        if (depth[k] == null) continue;
        var pos = xy(k);
        var nd = el("div", "cell tnode", String(nodes[k].v));
        nd.style.left = (pos[0] - 17) + "px"; nd.style.top = (pos[1] - 15) + "px";
        var tp = el("div", "tptr");
        tp.style.left = (pos[0] - 28) + "px"; tp.style.top = (pos[1] - 32) + "px";
        holder.appendChild(nd); holder.appendChild(tp);
        cellOf[String(k)] = nd; ptrOf[String(k)] = tp;
      }
      stage.appendChild(holder);

    } else if (tr.kind === "graph") {
      var n = tr.data.n, R = n <= 4 ? 70 : (n <= 7 ? 92 : 118);
      var SZ = (R + 40) * 2;
      var gw = el("div", "graphwrap");
      gw.style.width = SZ + "px"; gw.style.height = SZ + "px";
      var gl = svg("svg", { width: SZ, height: SZ, class: "glines" });
      gw.appendChild(gl);
      var at2 = function (i) {
        var ang = -Math.PI / 2 + (2 * Math.PI * i) / n;
        return [SZ / 2 + R * Math.cos(ang), SZ / 2 + R * Math.sin(ang)];
      };
      (tr.data.edges || []).forEach(function (e, ei) {
        var a = at2(e[0]), b = at2(e[1]);
        var ln = svg("line", { x1: a[0], y1: a[1], x2: b[0], y2: b[1] });
        gl.appendChild(ln);
        edgeOf[String(ei)] = ln;
        if (e.length > 2) {
          var tx = svg("text", { x: (a[0] + b[0]) / 2, y: (a[1] + b[1]) / 2 - 4, class: "gw" });
          tx.textContent = String(e[2]);
          gl.appendChild(tx);
        }
      });
      for (var i2 = 0; i2 < n; i2++) {
        var q = at2(i2);
        var gn = el("div", "cell gnode", String((tr.data.labels || [])[i2] != null ? tr.data.labels[i2] : i2));
        gn.style.left = (q[0] - 17) + "px"; gn.style.top = (q[1] - 17) + "px";
        var gp = el("div", "tptr");
        gp.style.left = (q[0] - 28) + "px"; gp.style.top = (q[1] - 34) + "px";
        gw.appendChild(gn); gw.appendChild(gp);
        cellOf[String(i2)] = gn; ptrOf[String(i2)] = gp;
      }
      stage.appendChild(gw);

    } else {
      var cells = el("div", "cells");
      var vals = (typeof tr.data === "string") ? tr.data.split("") : tr.data;
      vals.forEach(function (v, i) {
        var w2 = el("div", "cwrap");
        var p2 = el("div", "ptrs");
        var c2 = el("div", "cell", String(v));
        w2.appendChild(p2); w2.appendChild(c2); w2.appendChild(el("div", "cidx", String(i)));
        cells.appendChild(w2); cellOf[String(i)] = c2; ptrOf[String(i)] = p2;
      });
      stage.appendChild(cells);
    }
    box.appendChild(stage);

    var aux = el("div", "vaux");
    var note = el("div", "vnote");
    box.appendChild(aux); box.appendChild(note);

    var codeBox = el("div", "vcode");
    var lineNodes = [];
    tr.code.forEach(function (ln) {
      var d = el("div", "cl");
      var h = ln.indexOf("#");
      if (h === -1) d.appendChild(document.createTextNode(ln || " "));
      else {
        d.appendChild(document.createTextNode(ln.slice(0, h)));
        d.appendChild(el("span", "cm", ln.slice(h)));
      }
      codeBox.appendChild(d); lineNodes.push(d);
    });
    box.appendChild(codeBox);

    var ctl = el("div", "vctl");
    var bBack = el("button", "vb", "◀"); bBack.type = "button"; bBack.title = "previous step";
    var bPlay = el("button", "vb go", "▶ play"); bPlay.type = "button";
    var bNext = el("button", "vb", "▶"); bNext.type = "button"; bNext.title = "next step";
    var bRe = el("button", "vb", "↺"); bRe.type = "button"; bRe.title = "restart";
    var counter = el("div", "vstep");
    var track = el("div", "vtrack"); var fill = el("i"); track.appendChild(fill);
    [bBack, bPlay, bNext, bRe, counter, track].forEach(function (n) { ctl.appendChild(n); });
    box.appendChild(ctl);

    var at = 0, timer = null;

    var baseCls = (tr.kind === "tree") ? "cell tnode"
                : (tr.kind === "graph") ? "cell gnode" : "cell";

    function inSpan(key, span) {
      if (!span) return false;
      if (tr.kind === "grid") {
        var p = key.split(",");
        return +p[0] >= span[0] && +p[0] <= span[2] && +p[1] >= span[1] && +p[1] <= span[3];
      }
      if (tr.kind === "tree" || tr.kind === "graph") return false;   /* no span on those */
      return +key >= span[0] && +key <= span[1];
    }

    function draw() {
      var fr = tr.frames[at];
      Object.keys(cellOf).forEach(function (key) {
        var cls = baseCls;
        if (inSpan(key, fr.span)) cls += " span";
        var m = fr.mark[key];
        if (m) cls += " " + m;
        cellOf[key].className = cls;
        ptrOf[key].textContent = "";
      });
      Object.keys(edgeOf).forEach(function (key) {
        var em = (fr.emark || {})[key];
        edgeOf[key].setAttribute("class", em ? ("e" + em) : "");
      });
      Object.keys(fr.ptr).forEach(function (name) {
        var key = String(fr.ptr[name]);
        if (ptrOf[key]) ptrOf[key].appendChild(el("span", null, name));
      });
      aux.textContent = "";
      (fr.aux || []).forEach(function (a) {
        var b = el("div", "ab");
        b.appendChild(el("span", "al", a.label));
        if (a.items) {
          var box2 = el("div", "ai");
          if (!a.items.length) box2.appendChild(el("span", "empty", "empty"));
          else a.items.forEach(function (x) { box2.appendChild(el("span", null, x)); });
          b.appendChild(box2);
        } else {
          b.appendChild(el("span", "av", a.text));
        }
        aux.appendChild(b);
      });
      note.textContent = fr.note;
      lineNodes.forEach(function (d, i) { d.classList.toggle("on", i === fr.line); });
      counter.textContent = (at + 1) + " / " + tr.frames.length;
      fill.style.width = Math.round(((at + 1) / tr.frames.length) * 100) + "%";
      bBack.disabled = (at === 0);
      bNext.disabled = (at === tr.frames.length - 1);
    }
    function stop() {
      if (timer) { clearInterval(timer); timer = null; }
      bPlay.textContent = "▶ play"; bPlay.classList.add("go");
    }
    function step(d) {
      at = Math.max(0, Math.min(tr.frames.length - 1, at + d));
      draw();
      if (at === tr.frames.length - 1) stop();
    }
    bBack.addEventListener("click", function () { stop(); step(-1); V.vizActive = api2; });
    bNext.addEventListener("click", function () { stop(); step(1); V.vizActive = api2; });
    bRe.addEventListener("click", function () { stop(); at = 0; draw(); V.vizActive = api2; });
    bPlay.addEventListener("click", function () {
      V.vizActive = api2;
      if (timer) { stop(); return; }
      if (at === tr.frames.length - 1) at = 0;
      bPlay.textContent = "‖ pause"; bPlay.classList.remove("go");
      timer = setInterval(function () { step(1); }, 1150);
      draw();
    });
    var api2 = { step: step, stop: stop };
    VIZ_TIMERS.push(function () { stop(); });
    draw();
    return box;
  }
  var VIZ_TIMERS = [];
  function stopAllViz() {
    VIZ_TIMERS.forEach(function (f) { try { f(); } catch (e) {} });
    VIZ_TIMERS = []; V.vizActive = null;
  }

  function secBox(title, badge) {
    var box = el("div", "sheet");
    var h = el("div", "sheet-h");
    h.appendChild(el("h2", null, title));
    if (badge) h.appendChild(el("span", "badge", badge));
    box.appendChild(h);
    return box;
  }

  /* ---------- learn: the index ---------- */
  function learnScreen() {
    var f = document.createDocumentFragment();
    f.appendChild(el("div", "crumb", "learn — the whole map"));

    var hero = el("div", "hero");
    var h1 = el("h1");
    h1.innerHTML = 'The patterns are <em>countable</em>.<br>So are their variants.';
    hero.appendChild(h1);
    hero.appendChild(rich("p", "lead",
      "There are only so many data structures, only so many patterns that run on them, and inside each pattern " +
      "only so many <b>variants</b>. A variant fixes the template, and the template fixes the set of questions that " +
      "can be built on it. Learn the variant and you have pre-solved every question in its family — the story on " +
      "top is just wrapping paper."));
    var c = el("div", "counts");
    [[LIB.patterns.length, "patterns"], [allVariants(), "variants"], [allAsks(), "question families"]]
      .forEach(function (x) {
        var d = el("div");
        d.appendChild(el("b", null, String(x[0])));
        d.appendChild(el("span", null, x[1]));
        c.appendChild(d);
      });
    hero.appendChild(c);
    f.appendChild(hero);

    LIB.groups.forEach(function (g) {
      var ps = LIB.patterns.filter(function (p) { return p.group === g.id; });
      if (!ps.length) return;
      var block = el("div", "gblock");
      var gh = el("div", "ghead");
      gh.appendChild(el("span", "gn", g.id));
      gh.appendChild(el("h3", null, g.name));
      gh.appendChild(el("p", null, g.note));
      block.appendChild(gh);
      var grid = el("div", "pcards");
      ps.forEach(function (p) {
        var card = el("button", "pcard"); card.type = "button";
        card.appendChild(el("div", "pn", p.name));
        card.appendChild(el("div", "pb", p.buys));
        var m = el("div", "pm");
        var k = knownIn(p), tot = p.variants.length;
        m.appendChild(el("span", k === tot ? "done" : null, k + "/" + tot + " variants"));
        var nvz = p.variants.filter(function (v) { return VIZGEN[v.id]; }).length;
        if (nvz) m.appendChild(el("span", "tcount", "▶ " + nvz));
        var mini = el("div", "mini");
        var fill = el("i"); fill.style.width = Math.round((k / tot) * 100) + "%";
        mini.appendChild(fill); m.appendChild(mini);
        card.appendChild(m);
        card.addEventListener("click", function () { V.pat = p.id; V.screen = "pattern"; render(); });
        grid.appendChild(card);
      });
      block.appendChild(grid);
      f.appendChild(block);
    });

    var missing = LIB.groups.filter(function (g) {
      return !LIB.patterns.some(function (p) { return p.group === g.id; });
    });
    if (missing.length) {
      f.appendChild(rich("div", "pending",
        "<b>Not written yet:</b> " + missing.map(function (g) { return g.name.toLowerCase(); }).join(", ") +
        ". The drill below already covers them — only these Learn pages are pending."));
    }
    return f;
  }

  /* ---------- learn: one pattern ---------- */
  function patternScreen() {
    var p = patById(V.pat);
    var f = document.createDocumentFragment();
    if (!p) { V.screen = "learn"; return learnScreen(); }

    var cr = el("div", "crumb");
    var back = el("button", "btn ghost", "← all patterns"); back.type = "button";
    back.addEventListener("click", function () { V.screen = "learn"; render(); });
    cr.appendChild(back);
    cr.appendChild(el("span", "now", p.name));
    f.appendChild(cr);

    var head = el("div", "phead");
    head.appendChild(el("h2", null, p.name));
    var meta = el("div", "meta");
    meta.appendChild(rich("span", "chipm", "<b>lives on</b> &nbsp;" + p.lives));
    meta.appendChild(rich("span", "chipm", "<b>buys you</b> &nbsp;" + p.buys));
    meta.appendChild(rich("span", "chipm", "<b>" + p.variants.length + "</b> &nbsp;variants"));
    head.appendChild(meta);
    head.appendChild(rich("div", "core", p.core));
    f.appendChild(head);

    /* recognise */
    var rb = secBox("Recognise it", "the tells");
    var sec1 = el("div", "sec");
    var tells = el("div", "tells");
    p.recognise.forEach(function (r) {
      var t = el("div", "tell");
      t.appendChild(rich("div", "cue", r.cue));
      t.appendChild(rich("div", "pat", r.note));
      tells.appendChild(t);
    });
    sec1.appendChild(tells);
    rb.appendChild(sec1);
    if (p.notwhen && p.notwhen.length) {
      var sec2 = el("div", "sec");
      sec2.appendChild(el("div", "lab", "but NOT this pattern when"));
      var nots = el("div", "nots");
      p.notwhen.forEach(function (x) {
        var n = el("div", "not");
        n.appendChild(el("span", "x", "✕"));
        n.appendChild(rich("span", null, x));
        nots.appendChild(n);
      });
      sec2.appendChild(nots);
      rb.appendChild(sec2);
    }
    f.appendChild(rb);

    /* pick the variant */
    if (p.pick && p.pick.length) {
      var pb = secBox("Pick the variant", "decide in one line");
      var sec3 = el("div", "sec");
      var picks = el("div", "picks");
      p.pick.forEach(function (x) {
        var vr = null;
        p.variants.forEach(function (v) { if (v.id === x.then) vr = v; });
        var row = el("button", "pick"); row.type = "button";
        row.appendChild(rich("span", "cond", "<i>if</i>" + x["if"]));
        row.appendChild(el("span", "go", (vr ? vr.name : x.then) + " →"));
        row.addEventListener("click", function () {
          var d = document.getElementById("vr-" + x.then);
          if (d) { d.open = true; d.scrollIntoView({ block: "start", behavior: "smooth" }); }
        });
        picks.appendChild(row);
      });
      sec3.appendChild(picks);
      pb.appendChild(sec3);
      f.appendChild(pb);
    }

    /* which platform do you want to practise on */
    var pinfo = LINKS.patterns && LINKS.patterns[p.id];
    var counts = {}, total = 0;
    var tally = function (e) {
      if (!e.p) return;
      counts[e.p] = (counts[e.p] || 0) + 1; total++;
    };
    p.variants.forEach(function (v) {
      ((LINKS.variants && LINKS.variants[v.id]) || []).forEach(tally);
    });
    if (pinfo) pinfo.cf.forEach(tally);     /* the CF picks filter too, so they must count */
    if (total) {
      var fb2 = el("div", "pfilter");
      fb2.appendChild(el("span", "lab", "platform"));
      var mk = function (name, n) {
        var b = el("button", "pf"); b.type = "button";
        b.setAttribute("data-pl", name);
        b.appendChild(document.createTextNode(name === "all" ? "all" : name));
        b.appendChild(el("span", "n", String(n)));
        b.addEventListener("click", function () { V.plat = name; applyFilter(); });
        return b;
      };
      fb2.appendChild(mk("all", total));
      Object.keys(counts).sort(function (a, b) { return counts[b] - counts[a]; })
        .forEach(function (k) { fb2.appendChild(mk(k, counts[k])); });
      f.appendChild(fb2);
    }

    /* the variants */
    f.appendChild(el("div", "crumb", "the variants — this is the closed set"));
    p.variants.forEach(function (v, i) {
      var d = document.createElement("details");
      d.className = "vr"; d.id = "vr-" + v.id;
      if (i === 0) d.open = true;

      var s = document.createElement("summary");
      s.appendChild(el("span", "tw", "▶"));
      s.appendChild(el("span", "vname", v.name));
      if (VIZGEN[v.id]) s.appendChild(el("span", "trace", "▶ trace"));
      s.appendChild(el("span", "vwhen", v.when));
      var tick = el("button", "tick" + (state.known[v.id] ? " on" : ""),
                    state.known[v.id] ? "✓ got it" : "got it");
      tick.type = "button";
      tick.addEventListener("click", function (ev) {
        ev.preventDefault(); ev.stopPropagation();
        if (state.known[v.id]) delete state.known[v.id]; else state.known[v.id] = 1;
        save(); render();
        var re = document.getElementById("vr-" + v.id);
        if (re) re.open = true;
      });
      s.appendChild(tick);
      d.appendChild(s);

      var body = el("div", "vbody");
      var facts = el("div", "facts");
      [["tool", v.tool], ["invariant", v.invariant], ["complexity", v.cx]].forEach(function (pair) {
        if (!pair[1] || pair[1] === "—") return;
        var fa = el("div", "fact" + (pair[0] === "complexity" ? " cxf" : ""));
        fa.appendChild(el("div", "fl", pair[0]));
        fa.appendChild(rich("div", "fv", pair[1]));
        facts.appendChild(fa);
      });
      body.appendChild(facts);
      if (VIZGEN[v.id]) body.appendChild(vizPlayer(v.id));
      else if (VIZ_PENDING[v.id]) body.appendChild(rich("div", "vpending",
        "<b>No trace yet.</b> " + VIZ_PENDING[v.id]));
      body.appendChild(el("div", "lab", "the full template"));
      body.appendChild(codeBlock(v.code));

      if (v.asks && v.asks.length) {
        body.appendChild(el("div", "lab", "what can be asked on this — " + v.asks.length + " families"));
        var ul = el("ul", "asks");
        v.asks.forEach(function (a) { ul.appendChild(rich("li", null, a)); });
        body.appendChild(ul);
      }
      var exList = (LINKS.variants && LINKS.variants[v.id]) || v.examples || [];
      if (exList.length) {
        body.appendChild(el("div", "lab", "go solve the clean versions — " + exList.length + " problems"));
        body.appendChild(exRow(exList));
      }
      if (v.traps && v.traps.length) {
        body.appendChild(el("div", "lab", "what actually breaks it"));
        var tl = el("ul", "traps");
        v.traps.forEach(function (t) {
          var li = el("li");
          li.appendChild(el("span", "w", "!"));
          li.appendChild(rich("span", null, t));
          tl.appendChild(li);
        });
        body.appendChild(tl);
      }
      d.appendChild(body);
      f.appendChild(d);
    });

    /* practise this pattern anywhere */
    if (pinfo && (pinfo.hubs.length || pinfo.cf.length)) {
      var hb = secBox("Practise this anywhere", "every platform");
      if (pinfo.hubs.length) {
        var s4 = el("div", "sec");
        s4.appendChild(el("div", "lab", "topic hubs — whole problem lists for this pattern"));
        var rail = el("div", "rail");
        pinfo.hubs.forEach(function (h) {
          var a = el("a", "hub"); a.href = h.u; a.target = "_blank"; a.rel = "noopener noreferrer";
          a.appendChild(document.createTextNode(h.p));
          a.appendChild(el("span", "ar", "↗"));
          rail.appendChild(a);
        });
        s4.appendChild(rail);
        hb.appendChild(s4);
      }
      if (pinfo.cf.length) {
        var s5 = el("div", "sec");
        s5.appendChild(el("div", "lab",
          "codeforces — long narrative statements, the closest thing to a real OA (number is the rating)"));
        s5.appendChild(exRow(pinfo.cf));
        hb.appendChild(s5);
      }
      f.appendChild(hb);
    }

    var row = el("div", "cta");
    var dr = el("button", "btn primary", "drill all " + Q.length); dr.type = "button";
    dr.addEventListener("click", function () { start(shuffle(Q)); });
    row.appendChild(dr);
    var bk = el("button", "btn", "← all patterns"); bk.type = "button";
    bk.addEventListener("click", function () { V.screen = "learn"; render(); });
    row.appendChild(bk);
    f.appendChild(row);
    return f;
  }
"""

RENDER_OLD = '''    app.textContent = "";
    app.appendChild(bar());
    if (V.screen === "home") app.appendChild(home());
    else if (V.screen === "sheet") app.appendChild(sheetScreen());'''
RENDER_NEW = '''    stopAllViz();            /* the DOM is about to be replaced; kill any running trace */
    app.textContent = "";
    app.appendChild(bar());
    if (V.screen === "home") app.appendChild(home());
    else if (V.screen === "learn") app.appendChild(learnScreen());
    else if (V.screen === "pattern") { app.appendChild(patternScreen()); applyFilter(); focusVar(); }
    else if (V.screen === "sheet") app.appendChild(sheetScreen());'''

CTA_OLD = "    cta.appendChild(sheet);"
CTA_NEW = """    var lrn = el("button", "btn primary", "learn the patterns");
    lrn.type = "button";
    lrn.addEventListener("click", function () { V.screen = "learn"; render(); });
    cta.appendChild(lrn);
    sheet.className = "btn";
    cta.appendChild(sheet);"""

HERO_OLD = ('    p.textContent = "The tracker links 235 problems to solve. This is the skill underneath all of them: '
            'read a statement, look at the constraints, and know which of about twenty patterns it is — inside a minute. '
            'Every question here gives you the statement and the real constraint bounds, and every explanation names the tell '
            'that gave it away.";')
HERO_NEW = ('    p.textContent = "Two halves. LEARN is the map: every pattern, every variant inside it, the template, '
            'and the fixed list of questions that can be built on each one. DRILL is the test: a statement and its real '
            'constraint bounds, and you name the pattern before you write anything.";')

STATE_ANCHOR = '["seen", "wrong", "pat", "patok"].forEach(function (k) { if (!s[k]) s[k] = {}; });'
STATE_NEW = '["seen", "wrong", "pat", "patok", "known"].forEach(function (k) { if (!s[k]) s[k] = {}; });'


def main():
    if not os.path.exists(SRC):
        shutil.copy2(TARGET, SRC)
        print("stashed the original as .radar_src.html")
    html = open(SRC, encoding="utf-8").read()

    lib = json.dumps({"groups": PL.GROUPS, "patterns": PL.PATTERNS}, ensure_ascii=False, separators=(",", ":"))

    lpath = os.path.join(HERE, "links.json")
    if not os.path.exists(lpath):
        sys.exit("ERROR: links.json is missing. Run  python verify_links.py  first.")
    linkdata = json.load(open(lpath, encoding="utf-8"))
    links = json.dumps(linkdata, ensure_ascii=False, separators=(",", ":"))
    nlinks = (sum(len(v) for v in linkdata["variants"].values())
              + sum(len(d["hubs"]) + len(d["cf"]) for d in linkdata["patterns"].values()))

    # The trace generators are JavaScript, because they run live on whatever input the user
    # types. Node fuzz-tests them against brute force before any of it is allowed into the page.
    engine = chr(10).join(open(os.path.join(HERE, f), encoding="utf-8").read()
                          for f in ("viz_engine.js", "viz_engine_b.js",
                                    "viz_engine_c.js", "viz_engine_d.js", "viz_engine_e.js",
                                    "viz_engine_f.js"))
    print("fuzz-testing the trace generators ...")
    try:
        proc = subprocess.run(["node", os.path.join(HERE, "viz_test.js")], cwd=HERE,
                              capture_output=True, text=True, timeout=300)
    except FileNotFoundError:
        sys.exit("ERROR: node is not on PATH, so the generators cannot be verified. Install Node, "
                 "or run build_radar.py --skip-tests if you accept shipping unverified traces.")
    if proc.returncode != 0 and "--skip-tests" not in sys.argv:
        print(proc.stdout[-4000:]); print(proc.stderr[-2000:])
        sys.exit("ERROR: the trace generators FAILED their fuzz test (above). Nothing was written.")
    tail = [l for l in proc.stdout.strip().splitlines() if "generators," in l]
    print("  " + (tail[-1] if tail else "verified"))
    # take the count from the test itself rather than grepping the source, which also
    # matched the G["variant-id"] example in the file's own header comment
    m = re.search(r"(\d+) generators", tail[-1] if tail else "")
    ngen = int(m.group(1)) if m else 0

    for blob, what in ((lib, "library"), (links, "links")):
        if "</script>" in blob:
            sys.exit("ERROR: the %s contains a literal </script> and would break the page." % what)

    steps = []

    def sub(old, new, label):
        nonlocal html
        if html.count(old) != 1:
            sys.exit("ERROR: anchor %r found %d times (expected 1)." % (label, html.count(old)))
        html = html.replace(old, new, 1)
        steps.append(label)

    # fresh start, same as the hub serves: drop progress that was baked into the page
    html = re.sub(r'(<script type="application/json" id="state">).*?(</script>)',
                  r'\1{"rev":0}\2', html, count=1, flags=re.S)

    sub("\n</style>", CSS + "\n</style>", "css")
    sub(STATE_ANCHOR, STATE_NEW, "state key")
    sub(HERO_OLD, HERO_NEW, "hero copy")
    sub(CTA_OLD, CTA_NEW, "home button")
    sub(RENDER_OLD, RENDER_NEW, "render dispatch")
    sub("  document.addEventListener(\"keydown\"", JS + "\n  document.addEventListener(\"keydown\"", "learn screens")
    sub('''  document.addEventListener("keydown", function (ev) {
    if (V.screen === "quiz" && V.picked == null) {''',
        '''  document.addEventListener("keydown", function (ev) {
    if (V.screen === "pattern" && V.vizActive && (ev.key === "ArrowRight" || ev.key === "ArrowLeft")) {
      V.vizActive.stop(); V.vizActive.step(ev.key === "ArrowRight" ? 1 : -1); ev.preventDefault(); return;
    }
    if (V.screen === "quiz" && V.picked == null) {''',
        "arrow keys step the trace")
    # keep the cloud self-republish honest: carry the library across a republish too
    sub("""        o + ' type="application/json" id="state">' + JSON.stringify(state) + c + '\\n' +""",
        """        o + ' type="application/json" id="lib">' + document.getElementById("lib").textContent + c + '\\n' +
        o + ' type="application/json" id="links">' + document.getElementById("links").textContent + c + '\\n' +
        o + ' id="vizgen">' + document.getElementById("vizgen").textContent + c + '\\n' +
        o + ' type="application/json" id="state">' + JSON.stringify(state) + c + '\\n' +""",
        "republish carries lib + links")
    sub('<script id="code">',
        '<script type="application/json" id="lib">' + lib + '</script>\n'
        '<script type="application/json" id="links">' + links + '</script>\n'
        '<script id="vizgen">' + engine + '</script>\n<script id="code">',
        "library + links + the trace engine")

    open(TARGET, "w", encoding="utf-8").write(html)
    nv = sum(len(p["variants"]) for p in PL.PATTERNS)
    na = sum(len(v.get("asks", [])) for p in PL.PATTERNS for v in p["variants"])
    print("patched: " + ", ".join(steps))
    print("built %s\n  %d patterns, %d variants, %d question families, %d verified links,"
          "\n  %d live trace generators (fuzz-tested), %.0f KB"
          % (os.path.basename(TARGET), len(PL.PATTERNS), nv, na, nlinks,
             ngen, os.path.getsize(TARGET) / 1024))


if __name__ == "__main__":
    main()
