# -*- coding: utf-8 -*-
# =====================================================================================
#  PLACEMENT HUB  --  one launcher for every tool in this folder.
#
#  RUN:   python app.py      (or double-click  start.bat)
#  Opens  http://127.0.0.1:8765  with a home screen: pick a tool, do it, come back.
#
#  * The HTML tools are served UNCHANGED from disk; only two things are patched on the way out:
#      1. their "swap links for the hosted claude.ai copy" logic is switched off, so every
#         cross-link stays local;
#      2. a tiny shim makes their browser-storage (ticks, scores, redo piles) save to
#         data/progress.json instead -- so progress is yours, survives any browser, and can be
#         backed up by copying the data/ folder.
#  * OA Solve (tool 11) is built in at /oa and logs to data/oa_records.md.
#  * Everything it remembers lives in  data/  next to this file. Nothing outside this folder.
#  * Standard library only. Stop with Ctrl+C.
# =====================================================================================
import importlib.util, json, os, re, sys, threading, webbrowser, datetime
from urllib.parse import urlparse, parse_qs, unquote

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
os.makedirs(DATA, exist_ok=True)
PROGRESS = os.path.join(DATA, "progress.json")   # browser-storage mirror (tick marks, scores...)
VISITS   = os.path.join(DATA, "visits.json")     # when each tool was last opened
OA_LOG   = os.path.join(DATA, "oa_records.md")   # every OA Solve attempt
PORT = 8765

# ---- pull in the OA Solve engine (judge, problem bank, page) without duplicating it ----
_spec = importlib.util.spec_from_file_location("oa_web", os.path.join(HERE, "11 - OA Solve (web).py"))
oa = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(oa)
oa.LOG = OA_LOG

# ---- the Clue Coach (optional). Loaded on first use so a missing key or a bad edit cannot stop the hub. ----
BUILD = os.path.join(HERE, "_build")
_coach = {"mod": None, "qs": None, "err": None}

def coach():
    """Return (llm_coach module, {question id: question}) or (None, None) with _coach["err"] set."""
    if _coach["mod"] is None and _coach["err"] is None:
        try:
            if BUILD not in sys.path: sys.path.insert(0, BUILD)
            import llm_coach, sc_check
            _coach["mod"] = llm_coach
            _coach["qs"] = {q["id"]: q for q in sc_check.load()}
        except Exception as e:
            _coach["err"] = "%s: %s" % (type(e).__name__, e)
    return _coach["mod"], _coach["qs"]

# ---- what shows on the home screen ----
TOOLS = [
    # (file, group, short name, one-liner)
    ("0 - READ ME FIRST.html", "ready", "Read Me First", "How every tool works, how Mock OA and the coach are marked, SQL practice links and the folder layout."),
    ("2 - Stdin Trainer (drill).html", "ready", "Stdin Trainer", "START HERE. 13 input shapes - pick the line that parses each. The gap that cost you Infosys."),
    ("1 - Twenty Weeks to AC (tracker).html", "ready", "Twenty Weeks Tracker", "The plan and your progress. Track 0 first, then CS fundamentals, then DSA patterns."),
    ("3 - Stdin Survival Kit (manual).html", "ready", "Stdin Survival Kit", "The written manual for reading input in Python / C++ / Java."),
    ("4 - Stdin Survival Kit.pdf", "ready", "Survival Kit (PDF)", "13 printable pages. Keep open during a real assessment."),
    ("6 - CS Core Drill (OS DBMS CN OOP C).html", "ready", "CS Core Drill", "68 MCQs + 35-minute exam mode. The gate at most of your target companies."),
    ("5 - SQL Lab (practice).html", "ready", "SQL Lab", "Study guide (DBMS theory, normal forms, DDL scenarios, triggers, PostgreSQL/MySQL, interview Q&A) with a test per topic, plus graded practice on a live SQLite."),
    ("7 - Aptitude Sprint (formulas + practice).html", "ready", "Aptitude Sprint", "Formula sheets + timed practice, optional negative marking."),
    ("8 - Pattern Radar (name the pattern).html", "ready", "Pattern Radar", "Read a statement + constraints, name the DSA pattern in under a minute."),
    ("9 - Decoder (read the story, name the pattern).html", "ready", "Decoder", "140 wordy OA-style stories - strip the story, name the pattern, learn why not the others."),
    ("10 - Mock OA (timed exam).html", "ready", "Mock OA (scenario decoding)", "156 OA-size stories with a task line and a sample. Explain the approach in your own words; the AI coach judges it and nudges you without giving the answer."),
]

def jload(path, default):
    try:
        with open(path, encoding="utf-8") as f: return json.load(f)
    except Exception: return default

def jsave(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f: json.dump(obj, f, indent=1, ensure_ascii=False)
    os.replace(tmp, path)

_lock = threading.Lock()

# ---- patches applied to every served page ----
SHIM = """<script>/*hub-shim*/(function(){
try{var x=new XMLHttpRequest();x.open('GET','/api/kv',false);x.send();var d=JSON.parse(x.responseText);
localStorage.clear();for(var k in d)localStorage.setItem(k,d[k]);}catch(e){}
var S=Storage.prototype,si=S.setItem,ri=S.removeItem,ci=S.clear;
function post(o){try{fetch('/api/kv',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(o),keepalive:true});}catch(e){}}
S.setItem=function(k,v){si.call(this,k,v);if(this===localStorage)post({k:String(k),v:String(v)});};
S.removeItem=function(k){ri.call(this,k);if(this===localStorage)post({k:String(k),v:null});};
S.clear=function(){ci.call(this);if(this===localStorage)post({clear:true});};
})();</script>"""
HOME_BTN = ('<a href="/" style="position:fixed;left:12px;bottom:12px;z-index:99999;background:#121A26;color:#3FD9EC;'
            'border:1px solid #2A3A4E;border-radius:8px;padding:7px 12px;font:600 12px ui-monospace,Menlo,monospace;'
            'text-decoration:none;opacity:.85">&#8962; Home</a>')

def patch_html(html):
    # keep cross-links local: make the "am I on file://?" checks behave as if we were
    html = re.sub(r'location\.protocol\s*===\s*"file:"', 'true', html)
    html = re.sub(r'location\.protocol\s*!==\s*"file:"', 'false', html)
    # fresh start: some files carry old progress baked into the page itself; serve them blank
    # (each page's own migrate() fills in defaults). Your real progress lives in data/progress.json.
    html = re.sub(r'(<script type="application/json" id="state">).*?(</script>)', r'\1{"rev":0}\2', html, count=1, flags=re.S)
    # Some pages are bare fragments (no <head>/<body>) and carry literal "<head>"/"<body>"/"</body>"
    # text inside their own JavaScript. So only look for real tags BEFORE the first <script>.
    cut = html.lower().find('<script'); pre = html if cut < 0 else html[:cut]
    mh = re.search(r'<head[^>]*>', pre, re.I)
    mb = re.search(r'<body[^>]*>', pre, re.I)
    edits = [(mh.end() if mh else 0, SHIM)]
    edits.append((mb.end(), HOME_BTN) if mb else (len(html), HOME_BTN))
    for pos, text in sorted(edits, reverse=True):
        html = html[:pos] + text + html[pos:]
    return html

def oa_stats():
    """Summarise data/oa_records.md for the home screen."""
    try: text = open(OA_LOG, encoding="utf-8").read()
    except Exception: return {"attempts": 0, "solved": 0, "last": None}
    heads = re.findall(r'^## (\d{4}-\d\d-\d\d \d\d:\d\d)\s+\|\s+(\S+) [^|]*\|\s+(SUBMIT|RUN\(sample\)|MOVED ON)\s*(?:best=)?(\w+)?', text, re.M)
    solved = {pid for _, pid, kind, v in heads if kind == "SUBMIT" and v == "AC"}
    return {"attempts": len(heads), "solved": len(solved), "last": heads[-1][0] if heads else None}

def home_data():
    visits = jload(VISITS, {})
    tools = []
    for fn, grp, name, blurb in TOOLS:
        if os.path.exists(os.path.join(HERE, fn)):
            v = visits.get(fn, {})
            tools.append({"file": fn, "group": grp, "name": name, "blurb": blurb,
                          "count": v.get("count", 0), "last": v.get("last")})
    return {"tools": tools, "oa": oa_stats(), "oa_bank": len(oa.IDS)}

HOME = r"""<!doctype html><html lang=en><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1"><title>Placement Hub</title>
<style>
:root{--bg:#070B11;--panel:#121A26;--panel2:#182231;--edge:#1E2A3A;--edge2:#2A3A4E;--txt:#E8EEF6;--dim:#8397AE;--dim2:#5B6E85;
--cy:#3FD9EC;--ok:#4BE08B;--am:#FFC44D;--mono:ui-monospace,Menlo,Consolas,monospace;--sans:"Segoe UI",system-ui,Arial,sans-serif}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--txt);font-family:var(--sans)}
.wrap{max-width:980px;margin:0 auto;padding:34px 20px 60px}
h1{font-family:var(--mono);font-size:30px;margin:0 0 4px}h1 em{font-style:normal;color:var(--cy)}
.sub{color:var(--dim);margin:0 0 26px;line-height:1.55}
h2{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--dim2);margin:30px 0 12px;font-weight:600}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:12px}
a.card{display:block;background:var(--panel);border:1px solid var(--edge);border-radius:12px;padding:15px 16px;text-decoration:none;color:var(--txt);transition:border-color .12s,transform .12s}
a.card:hover{border-color:var(--cy);transform:translateY(-1px)}
.card .t{font-weight:700;font-size:15.5px;display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.card .d{color:var(--dim);font-size:13px;line-height:1.5;margin-top:6px}
.card .m{font-family:var(--mono);font-size:10.5px;color:var(--dim2);margin-top:10px;letter-spacing:.04em}
.tag{font-family:var(--mono);font-size:9.5px;letter-spacing:.08em;text-transform:uppercase;border-radius:4px;padding:2px 6px}
.tag.new{background:#0c2630;color:var(--cy)}.tag.go{background:#332714;color:var(--am)}
.oa{border-color:#2d4a4f;background:linear-gradient(135deg,#0f1e2a,#121A26)}
.next{background:#0c2630;border:1px solid var(--cy);border-radius:12px;padding:14px 16px;margin-bottom:6px;display:flex;gap:14px;align-items:center;flex-wrap:wrap}
.next b{color:var(--cy)}.next a{color:var(--txt)}
.foot{margin-top:40px;color:var(--dim2);font-size:12px;font-family:var(--mono);line-height:1.7}
</style></head><body><div class=wrap>
<h1>Placement <em>Hub</em></h1>
<p class=sub>Target: 10-12 LPA. Pick a tool, do the work, come back here. Everything you do is saved in this folder's <code>data/</code> - not in the browser.</p>
<div id=next></div>
<h2>Get ready</h2><div class=grid id=ready></div>
<h2>Practice</h2><div class=grid id=practice></div>
<div class=foot id=foot></div>
</div>
<script>
function ago(s){if(!s)return'never opened';var d=(Date.now()-new Date(s))/1000;if(d<90)return'just now';if(d<5400)return Math.round(d/60)+' min ago';
 if(d<129600)return Math.round(d/3600)+' h ago';return Math.round(d/86400)+' days ago';}
function esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;');}
fetch('/api/home').then(r=>r.json()).then(function(D){
 var firstNew=D.tools.find(t=>!t.count);
 var nx=document.getElementById('next');
 if(firstNew)nx.innerHTML='<div class=next><span><b>Next up:</b> '+esc(firstNew.name)+' - '+esc(firstNew.blurb)+'</span><a class="tag go" href="/t/'+encodeURIComponent(firstNew.file)+'">Open &rarr;</a></div>';
 D.tools.forEach(function(t){
  var a=document.createElement('a');a.className='card';a.href='/t/'+encodeURIComponent(t.file);
  a.innerHTML='<div class=t>'+esc(t.name)+(t.count?'':' <span class="tag new">new</span>')+'</div><div class=d>'+esc(t.blurb)+'</div><div class=m>'+
   (t.count?('opened '+t.count+'x &middot; last '+ago(t.last)):'not opened yet')+'</div>';
  document.getElementById('ready').appendChild(a);});
 var o=D.oa,p=document.createElement('a');p.className='card oa';p.href='/oa';
 p.innerHTML='<div class=t>OA Solve <span class="tag go">real judge</span></div><div class=d>Write a real Python program, get a real AC / WA / TLE verdict on '+D.oa_bank+
  ' problems. You set the question count, minutes, and strict or relaxed timer.</div><div class=m>'+
  (o.attempts?(o.solved+' solved &middot; '+o.attempts+' attempts logged &middot; last '+ago(o.last.replace(' ','T'))):'no attempts yet')+'</div>';
 document.getElementById('practice').appendChild(p);
 document.getElementById('foot').innerHTML='data folder: '+esc(D.data_dir||'data/')+' &nbsp;|&nbsp; progress.json &middot; visits.json &middot; oa_records.md';
});
</script></body></html>"""

class Handler(oa.H):
    def _page(self, html):
        self._send(200, patch_html(html), "text/html; charset=utf-8")

    def do_GET(self):
        u = urlparse(self.path); q = parse_qs(u.query)
        if u.path in ("/", "/index.html"):
            return self._send(200, HOME, "text/html; charset=utf-8")
        if u.path == "/oa":
            return self._page(oa.PAGE)
        if u.path == "/api/home":
            d = home_data(); d["data_dir"] = DATA
            return self._send(200, json.dumps(d))
        if u.path == "/api/kv":
            with _lock: return self._send(200, json.dumps(jload(PROGRESS, {})))
        if u.path == "/api/coach":
            m, _ = coach()
            if m is None:
                return self._send(200, json.dumps({"on": False, "why": _coach["err"] or "not loaded"}))
            import llm_config
            on = llm_config.is_configured()
            return self._send(200, json.dumps({"on": on, "model": llm_config.load()["model"] if on else None,
                                               "why": None if on else "no NVIDIA_API_KEY in .env"}))
        if u.path.startswith("/t/"):
            name = unquote(u.path[3:])
            allowed = {t[0] for t in TOOLS}
            if name not in allowed or not os.path.isfile(os.path.join(HERE, name)):
                return self._send(404, "not found", "text/plain")
            with _lock:
                v = jload(VISITS, {}); e = v.setdefault(name, {"count": 0})
                e["count"] += 1; e["last"] = datetime.datetime.now().isoformat(timespec="seconds")
                jsave(VISITS, v)
            path = os.path.join(HERE, name)
            if name.endswith(".html"):
                return self._page(open(path, encoding="utf-8").read())
            return self._send(200, open(path, "rb").read(), "application/pdf" if name.endswith(".pdf") else "application/octet-stream")
        return super().do_GET()

    def do_POST(self):
        if self.path == "/api/kv":
            n = int(self.headers.get("Content-Length", "0"))
            try: d = json.loads(self.rfile.read(n) or "{}")
            except Exception: return self._send(400, "{}")
            with _lock:
                kv = jload(PROGRESS, {})
                if d.get("clear"): kv = {}
                elif "k" in d:
                    if d.get("v") is None: kv.pop(d["k"], None)
                    else: kv[d["k"]] = d["v"]
                jsave(PROGRESS, kv)
            return self._send(200, "{}")
        if self.path == "/api/coach":
            n = int(self.headers.get("Content-Length", "0"))
            try: d = json.loads(self.rfile.read(n) or "{}")
            except Exception: return self._send(400, json.dumps({"ok": False, "error": "bad request"}))
            m, qs = coach()
            if m is None:
                return self._send(200, json.dumps({"ok": False, "error": "the coach could not load (%s)" % _coach["err"]}))
            q = qs.get(d.get("qid"))
            if q is None:
                return self._send(200, json.dumps({"ok": False, "error": "unknown question id"}))
            try:
                if d.get("teach"):
                    return self._send(200, json.dumps(m.teach(q, (d.get("answer") or "").strip()[:4000])))
                out = m.judge(q, (d.get("answer") or "").strip()[:4000], hints=int(d.get("hints") or 0),
                              prior_verdict=d.get("verdict"), message=(d.get("message") or "").strip()[:2000] or None)
            except Exception as e:
                out = {"ok": False, "error": "%s: %s" % (type(e).__name__, e)}
            return self._send(200, json.dumps(out))
        return super().do_POST()

def main():
    from http.server import ThreadingHTTPServer
    try:
        srv = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    except OSError:
        print("Port %d is busy - is the hub (or OA Solve web) already running? Close it and retry." % PORT); return
    url = "http://127.0.0.1:%d/" % PORT
    print("Placement Hub running at " + url + "   (Ctrl+C to stop)")
    print("Your progress is saved in: " + DATA)
    threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try: srv.serve_forever()
    except KeyboardInterrupt: print("\nstopped. everything is saved in data/")

if __name__ == "__main__":
    main()
