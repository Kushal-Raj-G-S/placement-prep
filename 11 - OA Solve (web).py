# -*- coding: utf-8 -*-
# =====================================================================================
#  OA SOLVE (WEB)  -- a real-deal Online Assessment, served by your own Python.
#  You configure the exam (how many questions, minutes each, lock mode); it serves random
#  problems (NO names, NO picking, no "already solved" marks -- re-solving is good practice).
#  Judging runs in THIS Python process, so your code really executes: real AC/WA/TLE.
#
#  Left rail lists the questions (Q1 . Hard, Q2 . Medium ...) -- collapse/expand it, and in
#  the relaxed (no-lock) mode click any question to JUMP to it; each question keeps its own
#  code and its own accumulated time. In strict (auto-lock) mode the rail is read-only.
#
#  RUN:   python "11 - OA Solve (web).py"
#  Opens http://127.0.0.1:8765 in your browser. Needs oa_bank.json + oa_cases.json here.
#  Every attempt is logged to oa_records.md. Stop with Ctrl+C. Stdlib only, no internet.
# =====================================================================================
import json, os, sys, subprocess, tempfile, threading, webbrowser, datetime, random
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
BANK  = os.path.join(HERE, "data", "oa_bank.json")
CASES = os.path.join(HERE, "data", "oa_cases.json")
LOG   = os.path.join(HERE, "oa_records.md")
PORT  = 8765
TIME_LIMIT = 5.0

def _ensure_data():
    if not (os.path.exists(BANK) and os.path.exists(CASES)):
        mock_html = os.path.join(HERE, "10 - Mock OA (timed exam).html")
        if os.path.exists(mock_html):
            try:
                with open(mock_html, "r", encoding="utf-8") as f:
                    content = f.read()
                start = content.find('id="bank">') + len('id="bank">')
                end = content.find('</script>', start)
                data = json.loads(content[start:end])
                probs = data.get("problems", [])
                b_dict = {p["id"]: p for p in probs}
                c_dict = {p["id"]: [{"in": p["sin"], "out": str(p["sout"])}] for p in probs}
                if not os.path.exists(BANK):
                    with open(BANK, "w", encoding="utf-8") as f:
                        json.dump(b_dict, f, indent=2, ensure_ascii=False)
                if not os.path.exists(CASES):
                    with open(CASES, "w", encoding="utf-8") as f:
                        json.dump(c_dict, f, indent=2, ensure_ascii=False)
            except Exception:
                pass
    if not (os.path.exists(BANK) and os.path.exists(CASES)):
        print("ERROR: oa_bank.json / oa_cases.json must sit next to this file."); sys.exit(1)

_ensure_data()
BANKD  = json.load(open(BANK, encoding="utf-8"))
CASESD = json.load(open(CASES, encoding="utf-8"))
IDS = list(BANKD.keys())

def normalize(s):
    lines = s.replace("\r\n","\n").split("\n")
    while lines and lines[-1].strip()=="": lines.pop()
    return [ln.rstrip() for ln in lines]

def run_case(code, inp):
    fd, path = tempfile.mkstemp(suffix=".py", dir=HERE); os.close(fd)
    open(path,"w",encoding="utf-8").write(code)
    try:
        r = subprocess.run([sys.executable, path], input=inp, capture_output=True, text=True, timeout=TIME_LIMIT)
    except subprocess.TimeoutExpired:
        return ("TLE","")
    finally:
        try: os.remove(path)
        except OSError: pass
    if r.returncode != 0: return ("RE", (r.stderr or "").strip())
    return ("OK", r.stdout)

def judge(pid, code, sample_only):
    cases = CASESD.get(pid) or [{"in":BANKD[pid]["sin"],"out":str(BANKD[pid]["sout"])}]
    if sample_only: cases = cases[:1]
    for i,c in enumerate(cases, start=1):
        st,payload = run_case(code, c["in"])
        if st=="TLE": return {"verdict":"TLE","case":i,"total":len(cases),"in":c["in"],"exp":c["out"],"got":""}
        if st=="RE":  return {"verdict":"RE","case":i,"total":len(cases),"in":c["in"],"exp":c["out"],"got":payload}
        if normalize(payload)!=normalize(c["out"]):
            return {"verdict":"WA","case":i,"total":len(cases),"in":c["in"],"exp":c["out"],"got":payload}
    return {"verdict":"AC","case":len(cases),"total":len(cases),"in":"","exp":"","got":""}

def fmt_secs(s):
    s=int(s); return "%dm %02ds"%(s//60, s%60)

def log_line(text):
    with open(LOG,"a",encoding="utf-8") as f: f.write(text)

def log_attempt(pid, verdict, secs, code, sample):
    p=BANKD[pid]; mode="RUN(sample)" if sample else "SUBMIT"
    log_line("\n## %s  |  %s %s  |  %s %s  |  %s\n_Pattern: %s_\n\n```python\n%s\n```\n"%(
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), p["id"], p["title"], mode, verdict, fmt_secs(secs),
        p["ans"]["pattern"], code))

def log_advance(pid, best, secs, over, code):
    p=BANKD[pid]; ov = "  (OVER limit by %s)"%fmt_secs(over) if over>0 else ""
    log_line("\n## %s  |  %s %s  |  MOVED ON  best=%s  time=%s%s\n_Pattern: %s_\n\n```python\n%s\n```\n"%(
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), p["id"], p["title"], best, fmt_secs(secs), ov,
        p["ans"]["pattern"], code))

PAGE = r"""<!doctype html><html lang=en><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1"><title>OA Solve</title>
<style>
:root{--bg:#070B11;--bg2:#0C121B;--panel:#121A26;--panel2:#182231;--edge:#1E2A3A;--edge2:#2A3A4E;
--txt:#E8EEF6;--dim:#8397AE;--dim2:#5B6E85;--cy:#3FD9EC;--ok:#4BE08B;--ok2:#0E2C1D;--no:#FF7A6B;--no2:#331612;
--am:#FFC44D;--am2:#332714;--mono:"IBM Plex Mono",ui-monospace,Menlo,monospace;--sans:"IBM Plex Sans",Arial,sans-serif}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--txt);font-family:var(--sans);font-size:15px;height:100vh;display:flex;flex-direction:column;overflow:hidden}
.logo{font-family:var(--mono);font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--cy);font-size:13px}
.btn{font-family:var(--mono);font-size:11.5px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;background:var(--panel2);border:1px solid var(--edge2);border-radius:7px;padding:9px 14px;cursor:pointer;color:var(--txt)}
.btn:hover{border-color:var(--cy)} .btn.primary{background:var(--cy);border-color:var(--cy);color:#04222A}
.btn.run{background:var(--am);border-color:var(--am);color:#332714} .btn.ghost{background:transparent}
.sp{flex:1 1 auto}
/* setup */
#setup{flex:1;overflow:auto;display:flex;justify-content:center}
.card{max-width:640px;width:100%;padding:30px 24px;display:flex;flex-direction:column;gap:20px}
.card h1{font-family:var(--mono);font-size:28px;margin:0} .card h1 em{font-style:normal;color:var(--cy)}
.card p{margin:0;color:var(--dim);line-height:1.6}
.grp{background:var(--panel);border:1px solid var(--edge);border-radius:12px;padding:15px 16px}
.grp .lab{font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--dim2);margin-bottom:10px}
.chips{display:flex;gap:8px;flex-wrap:wrap}
.chip{font-family:var(--mono);font-size:13px;font-weight:600;background:var(--bg2);border:1px solid var(--edge2);border-radius:8px;padding:9px 15px;cursor:pointer;color:var(--txt)}
.chip:hover{border-color:var(--cy)} .chip.on{background:var(--cy);border-color:var(--cy);color:#04222A}
.mode{display:flex;flex-direction:column;gap:9px}
.mopt{display:flex;gap:11px;align-items:flex-start;background:var(--bg2);border:1px solid var(--edge2);border-radius:10px;padding:12px 14px;cursor:pointer}
.mopt.on{border-color:var(--cy);background:#0c2630}
.mopt .dot{width:16px;height:16px;border-radius:50%;border:2px solid var(--dim2);margin-top:2px;flex:0 0 auto}
.mopt.on .dot{border-color:var(--cy);background:var(--cy)}
.mopt .t{font-family:var(--mono);font-size:13px;font-weight:600;color:var(--txt)}
.mopt .d{font-size:12.5px;color:var(--dim);line-height:1.5;margin-top:3px}
/* exam */
#exam{flex:1;display:none;flex-direction:column;min-height:0}
.bar{display:flex;align-items:center;gap:12px;padding:9px 14px;background:var(--panel);border-bottom:1px solid var(--edge);flex-wrap:wrap}
.qn{font-family:var(--mono);font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--cy)}
.pdiff{font-family:var(--mono);font-size:9.5px;letter-spacing:.08em;border:1px solid var(--edge2);border-radius:4px;padding:2px 6px;color:var(--dim2)}
.clock{font-family:var(--mono);font-size:22px;font-weight:700;font-variant-numeric:tabular-nums;color:var(--cy);min-width:120px;text-align:right}
.clock.warn{color:var(--am)} .clock.crit{color:var(--no)} .clock.over{color:var(--no)}
.body{flex:1 1 auto;display:flex;min-height:0}
.nav{width:180px;flex:0 0 auto;background:var(--panel);border-right:1px solid var(--edge);display:flex;flex-direction:column;transition:width .12s}
.nav.collapsed{width:44px}
.nhead{display:flex;align-items:center;gap:6px;padding:9px 9px;border-bottom:1px solid var(--edge)}
.ntitle{font-family:var(--mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--dim2);flex:1}
.nav.collapsed .ntitle{display:none}
.navtoggle{background:var(--bg2);border:1px solid var(--edge2);border-radius:6px;color:var(--txt);cursor:pointer;font-family:var(--mono);padding:3px 9px}
.nlist{overflow:auto;padding:8px;display:flex;flex-direction:column;gap:6px} .nav.collapsed .nlist{padding:8px 5px}
.nitem{display:flex;align-items:center;gap:8px;background:var(--bg2);border:1px solid var(--edge2);border-radius:8px;padding:8px 9px;cursor:pointer;font-family:var(--mono);font-size:12px;color:var(--txt)}
.nitem:hover{border-color:var(--cy)} .nitem.cur{border-color:var(--cy);background:#0c2630}
.nitem.locked{cursor:default;opacity:.55} .nitem.locked:hover{border-color:var(--edge2)}
.nitem .st{width:9px;height:9px;border-radius:50%;background:var(--dim2);flex:0 0 auto}
.nitem .st.AC{background:var(--ok)} .nitem .st.WA,.nitem .st.TLE,.nitem .st.RE{background:var(--no)}
.nitem .nlabel{flex:1;display:flex;flex-direction:column;gap:1px} .nav.collapsed .nlabel{display:none}
.nitem .ndiff{color:var(--dim2);font-size:9.5px;letter-spacing:.05em;text-transform:uppercase}
.main{flex:1 1 auto;min-width:0;display:grid;grid-template-columns:1fr 1fr;min-height:0}
.left{overflow:auto;padding:18px 20px;border-right:1px solid var(--edge)}
.left .story{line-height:1.65;color:var(--txt);white-space:pre-wrap;font-size:14.5px;margin:2px 0 12px}
.sec{margin-top:14px}.sec .lab{font-family:var(--mono);font-size:9.5px;letter-spacing:.11em;text-transform:uppercase;color:var(--dim2);margin-bottom:6px}
.sec ul{margin:0;padding-left:18px;color:var(--dim);font-size:13.5px;line-height:1.6}
.exptext{color:var(--dim);font-size:13.5px;line-height:1.6;background:var(--bg);border:1px solid var(--edge2);border-left:3px solid var(--am);border-radius:8px;padding:9px 12px}
pre.io{margin:0;background:var(--bg);border:1px solid var(--edge2);border-radius:8px;padding:10px 12px;font-family:var(--mono);font-size:13px;white-space:pre;overflow-x:auto;color:var(--txt)}
.right{display:flex;flex-direction:column;min-height:0}
.edwrap{flex:1 1 auto;display:flex;flex-direction:column;min-height:0;padding:10px 12px}
.edtools{display:flex;gap:8px;align-items:center;margin-bottom:8px;flex-wrap:wrap}
textarea#code{flex:1 1 auto;width:100%;background:#04080D;color:var(--txt);border:1px solid var(--edge2);border-radius:9px;padding:12px;font-family:var(--mono);font-size:14px;line-height:1.55;resize:none;tab-size:4;white-space:pre;overflow:auto}
textarea#code:focus{outline:none;border-color:var(--cy)}
.verdict{padding:12px;border-top:1px solid var(--edge);font-family:var(--mono);font-size:13px;max-height:32%;overflow:auto}
.vhead{font-weight:700;letter-spacing:.06em}.ac{color:var(--ok)}.bad{color:var(--no)}.pend{color:var(--dim2)}
.vbox{margin-top:8px;background:var(--bg);border-radius:8px;padding:9px 11px;border-left:3px solid var(--no);white-space:pre-wrap;font-size:12.5px;color:var(--dim)}
.hint{color:var(--dim2);font-size:11.5px}
/* results */
#results{flex:1;display:none;overflow:auto;justify-content:center}
.rwrap{max-width:720px;width:100%;padding:26px 22px;display:flex;flex-direction:column;gap:12px}
.big{font-family:var(--mono);font-size:40px;font-weight:700;text-align:center;color:var(--cy)}
.ritem{background:var(--panel);border:1px solid var(--edge);border-radius:11px;padding:13px 15px}
.ritem h3{margin:0 0 4px;font-size:15px;display:flex;gap:10px;align-items:baseline;flex-wrap:wrap}
.ritem .rt{font-family:var(--mono);font-size:11px;color:var(--dim2)}
.ritem details{margin-top:7px} .ritem summary{cursor:pointer;font-family:var(--mono);font-size:11px;letter-spacing:.05em;text-transform:uppercase;color:var(--am)}
.ritem .ans{margin-top:7px;font-size:13px;color:var(--dim);line-height:1.6} .ritem .ans b{color:var(--cy)}
.vb{font-family:var(--mono);font-size:11px;padding:2px 7px;border-radius:5px}
.vb.AC{background:var(--ok2);color:var(--ok)} .vb.WA,.vb.TLE,.vb.RE{background:var(--no2);color:var(--no)} .vb.NONE{background:var(--panel2);color:var(--dim2)}
@media(max-width:820px){.main{grid-template-columns:1fr;overflow:auto}.left{border-right:0;border-bottom:1px solid var(--edge)}.right{min-height:62vh}}
</style></head><body>

<!-- SETUP -->
<div id=setup><div class=card>
 <h1>OA&nbsp;<em>Solve</em></h1>
 <p>A real assessment. Random problems only &mdash; no picking, no names, no "already solved" marks (re-solving is good practice). Set your own rules, then start.</p>
 <div class=grp><div class=lab>How many questions</div><div class=chips id=qCount></div></div>
 <div class=grp><div class=lab>Minutes per question</div><div class=chips id=qMins></div></div>
 <div class=grp><div class=lab>When the timer runs out</div>
  <div class=mode>
   <div class="mopt on" data-mode=lock><div class=dot></div><div><div class=t>Auto-lock &amp; advance (strict)</div><div class=d>At 0:00 it saves whatever you have and jumps to the next question. No working past the buzzer, and no jumping between questions.</div></div></div>
   <div class="mopt" data-mode=soft><div class=dot></div><div><div class=t>No lock &mdash; log overtime (relaxed)</div><div class=d>The timer is just a reminder. At 0:00 it keeps counting into overtime (red) and records the extra minutes. You can jump freely between questions and finish when you like.</div></div></div>
  </div>
 </div>
 <button class="btn primary" id=startBtn style="padding:13px;font-size:13px">Start assessment</button>
</div></div>

<!-- EXAM -->
<div id=exam>
 <div class=bar>
  <span class=logo>oa_solve</span>
  <span class=qn id=qn>Question 1 / 5</span>
  <span class=pdiff id=pdiff>Medium</span>
  <span class=sp></span>
  <span class=clock id=clock>20:00</span>
  <button class=btn id=nextBtn>Save &amp; Next</button>
  <button class=btn id=finishBtn style="display:none">Finish</button>
 </div>
 <div class=body>
  <div class=nav id=nav>
   <div class=nhead><span class=ntitle>Questions</span><button class=navtoggle id=navToggle title="collapse / expand">&#9776;</button></div>
   <div class=nlist id=nlist></div>
  </div>
  <div class=main>
   <div class=left id=left></div>
   <div class=right>
    <div class=edwrap>
     <div class=edtools>
      <button class="btn run" id=runBtn>Run (sample)</button>
      <button class="btn primary" id=subBtn>Submit (all cases)</button>
      <span class=sp></span><span class=hint>full program: read stdin, print output</span>
     </div>
     <textarea id=code spellcheck=false></textarea>
    </div>
    <div class=verdict id=verdict><span class="vhead pend">No submission yet.</span></div>
   </div>
  </div>
 </div>
</div>

<!-- RESULTS -->
<div id=results><div class=rwrap>
 <div class=big id=score>DONE</div>
 <p class=hint style="text-align:center">Full log saved to oa_records.md &mdash; paste it into the chat and we'll go through your reads together.</p>
 <div id=rlist></div>
 <button class="btn primary" id=againBtn style="padding:12px">New assessment</button>
</div></div>

<script>
var CFG={n:5,mins:20,mode:'lock'};
var picks=[],idx=-1,states=[],PROBS={},segStart=0,tid=null;
function fmt(s){var neg=s<0;s=Math.abs(Math.floor(s));var m=Math.floor(s/60),x=s%60;return (neg?'+':'')+m+':'+(x<10?'0':'')+x;}
function esc(s){return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;');}
function TMPL(){return 'import sys\ndata = sys.stdin.read().split("\\n")\n# solve and print the answer\n';}
// ---- setup chips ----
function chip(host,val,label,onpick,on){var b=document.createElement('button');b.className='chip'+(on?' on':'');b.textContent=label;
 b.onclick=function(){[].forEach.call(host.children,function(c){c.classList.remove('on');});b.classList.add('on');onpick(val);};host.appendChild(b);}
var qc=document.getElementById('qCount');[3,5,10,15,20,'All'].forEach(function(v){chip(qc,v,String(v),function(x){CFG.n=x;},v===5);});
var qm=document.getElementById('qMins');[10,15,20,30,45,60].forEach(function(v){chip(qm,v,v+' min',function(x){CFG.mins=x;},v===20);});
[].forEach.call(document.querySelectorAll('.mopt'),function(o){o.onclick=function(){document.querySelectorAll('.mopt').forEach(function(x){x.classList.remove('on');});o.classList.add('on');CFG.mode=o.dataset.mode;};});
// ---- timer (per current question) ----
function curEl(){return states[idx].accum + (Date.now()-segStart)/1000;}
function tick(){var rem=CFG.mins*60-curEl();var c=document.getElementById('clock');c.textContent=fmt(rem);
 if(rem<0){c.className='clock over';if(CFG.mode=='lock'){nextSeq();}}
 else c.className='clock'+(rem<=60?' crit':(rem<=180?' warn':''));}
function startTimer(){stopTimer();segStart=Date.now();tick();tid=setInterval(tick,1000);}
function stopTimer(){if(tid){clearInterval(tid);tid=null;}}
function saveCurrent(){if(idx<0)return;states[idx].accum+=(Date.now()-segStart)/1000;segStart=Date.now();states[idx].code=document.getElementById('code').value;}
// ---- flow ----
async function begin(){
 var n=(CFG.n==='All')?9999:CFG.n;
 picks=await (await fetch('/api/pick?n='+n)).json();
 states=picks.map(function(){return {code:null,accum:0,best:'NONE',started:false};});
 idx=-1;
 document.getElementById('setup').style.display='none';
 document.getElementById('results').style.display='none';
 document.getElementById('exam').style.display='flex';
 document.getElementById('finishBtn').style.display=(CFG.mode=='soft')?'':'none';
 go(0);
}
async function fetchProblem(id){if(PROBS[id])return PROBS[id];PROBS[id]=await (await fetch('/api/problem?id='+id)).json();return PROBS[id];}
async function go(j){
 if(idx>=0)saveCurrent();
 idx=j;states[j].started=true;
 var p=await fetchProblem(picks[j].id);
 document.getElementById('qn').textContent='Question '+(j+1)+' / '+picks.length;
 document.getElementById('pdiff').textContent=(p.diff=='E'?'Easy':p.diff=='H'?'Hard':'Medium');
 var h='<div class=story>'+esc(p.story)+'</div>';
 h+='<div class=sec><div class=lab>Constraints</div><ul>'+p.cons.map(function(c){return '<li>'+esc(c)+'</li>';}).join('')+'</ul></div>';
 h+='<div class=sec><div class=lab>Input format</div><ul>'+p.inf.map(function(c){return '<li>'+esc(c)+'</li>';}).join('')+'</ul></div>';
 h+='<div class=sec><div class=lab>Output format</div><ul>'+p.outf.map(function(c){return '<li>'+esc(c)+'</li>';}).join('')+'</ul></div>';
 h+='<div class=sec><div class=lab>Sample input</div><pre class=io>'+esc(p.sin)+'</pre></div>';
 h+='<div class=sec><div class=lab>Sample output</div><pre class=io>'+esc(p.sout)+'</pre></div>';
 if(p.exp)h+='<div class=sec><div class=lab>Sample explanation (how that output is reached)</div><div class=exptext>'+esc(p.exp)+'</div></div>';
 var L=document.getElementById('left');L.innerHTML=h;L.scrollTop=0;
 document.getElementById('code').value=(states[j].code!=null)?states[j].code:TMPL();
 var st=states[j];
 document.getElementById('verdict').innerHTML=(st.best=='NONE')?'<span class="vhead pend">No submission yet.</span>':'<span class="vhead pend">Last verdict here: '+st.best+' &mdash; resubmit to re-check.</span>';
 document.getElementById('nextBtn').textContent=(j+1>=picks.length)?'Save & Finish':'Save & Next';
 startTimer();renderNav();
}
function renderNav(){
 var host=document.getElementById('nlist');host.innerHTML='';
 var locked=(CFG.mode=='lock');
 picks.forEach(function(pk,i){
  var it=document.createElement('div');
  it.className='nitem'+(i===idx?' cur':'')+(locked?' locked':'');
  var diff=pk.diff=='E'?'Easy':pk.diff=='H'?'Hard':'Medium';
  it.innerHTML='<span class="st '+states[i].best+'"></span><span class=nlabel><span>Q'+(i+1)+'</span><span class=ndiff>'+diff+'</span></span>';
  if(!locked)it.onclick=function(){if(i!==idx)go(i);};
  host.appendChild(it);
 });
}
var RANK={NONE:0,RE:1,TLE:1,WA:1,AC:2};
async function submit(sample){
 var code=document.getElementById('code').value;
 var v=document.getElementById('verdict');v.innerHTML='<span class="vhead pend">Judging...</span>';
 var r=await fetch('/api/judge',{method:'POST',headers:{'Content-Type':'application/json'},
  body:JSON.stringify({id:picks[idx].id,code:code,sample:sample,secs:Math.round(curEl())})});
 var d=await r.json();var vv=d.verdict;
 if(!sample && RANK[vv]>RANK[states[idx].best]){states[idx].best=vv;renderNav();}
 if(vv=='AC'){v.innerHTML='<span class="vhead ac">\u2713 ACCEPTED</span> <span class=hint>passed all '+d.total+' case(s)'+(sample?' (sample only)':'')+'</span>';}
 else{var name={WA:'WRONG ANSWER',TLE:'TIME LIMIT EXCEEDED',RE:'RUNTIME ERROR'}[vv]||vv;
  var b='<span class="vhead bad">\u2717 '+name+'</span> <span class=hint>on case '+d.case+'/'+d.total+'</span>';
  if(vv=='WA')b+='<div class=vbox><b>input:</b>\n'+esc(d.in)+'\n\n<b>expected:</b>\n'+esc(d.exp)+'\n\n<b>your output:</b>\n'+esc(d.got||'(empty)')+'</div>';
  if(vv=='RE')b+='<div class=vbox>'+esc(d.got||'(no message)')+'</div>';
  if(vv=='TLE')b+='<div class=vbox>exceeded '+d.tl+'s on this case</div>';
  v.innerHTML=b;}
}
function nextSeq(){saveCurrent();if(idx+1>=picks.length)finish();else go(idx+1);}
async function finish(){
 stopTimer();saveCurrent();
 for(var i=0;i<picks.length;i++){if(states[i].started){var over=Math.max(0,Math.round(states[i].accum-CFG.mins*60));
  try{await fetch('/api/save',{method:'POST',headers:{'Content-Type':'application/json'},
   body:JSON.stringify({id:picks[i].id,best:states[i].best,secs:Math.round(states[i].accum),over:over,code:states[i].code||''})});}catch(e){}}}
 showResults();
}
function showResults(){
 document.getElementById('exam').style.display='none';
 document.getElementById('results').style.display='flex';
 var started=[];for(var i=0;i<picks.length;i++)if(states[i].started)started.push(i);
 var ac=started.filter(function(i){return states[i].best=='AC';}).length;
 document.getElementById('score').textContent=ac+' / '+started.length+' AC';
 var host=document.getElementById('rlist');host.innerHTML='';
 started.forEach(function(i){
  var p=PROBS[picks[i].id],st=states[i];var over=Math.max(0,Math.round(st.accum-CFG.mins*60));
  var d=document.createElement('div');d.className='ritem';
  var ov=over>0?(' &middot; <span style="color:var(--no)">over by '+fmt(over)+'</span>'):'';
  d.innerHTML='<h3>Q'+(i+1)+'. '+esc(p.title)+' <span class="vb '+st.best+'">'+st.best+'</span><span class=rt>'+fmt(Math.round(st.accum)).replace('+','')+ov+'</span></h3>'+
   '<details><summary>Reveal intended approach</summary><div class=ans>loading...</div></details>';
  host.appendChild(d);
  d.querySelector('details').addEventListener('toggle',async function(e){if(!e.target.open)return;var box=d.querySelector('.ans');if(box.dataset.done)return;
   var a=await (await fetch('/api/reveal?id='+picks[i].id)).json();
   box.innerHTML='<b>Pattern:</b> '+esc(a.pattern)+'<br><b>Brute:</b> '+esc(a.brute)+'<br><b>Optimal:</b> '+esc(a.opt)+'<br><b>Complexity:</b> '+esc(a.cx);box.dataset.done='1';});
 });
}
document.getElementById('startBtn').onclick=begin;
document.getElementById('againBtn').onclick=function(){document.getElementById('results').style.display='none';document.getElementById('setup').style.display='flex';};
document.getElementById('runBtn').onclick=function(){submit(true);};
document.getElementById('subBtn').onclick=function(){submit(false);};
document.getElementById('nextBtn').onclick=nextSeq;
document.getElementById('finishBtn').onclick=finish;
document.getElementById('navToggle').onclick=function(){document.getElementById('nav').classList.toggle('collapsed');};
document.getElementById('code').addEventListener('keydown',function(e){if(e.key=='Tab'){e.preventDefault();
 var t=this,s=t.selectionStart,en=t.selectionEnd;t.value=t.value.slice(0,s)+'    '+t.value.slice(en);t.selectionStart=t.selectionEnd=s+4;}});
</script></body></html>"""

class H(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json"):
        b = body.encode("utf-8") if isinstance(body,str) else body
        self.send_response(code); self.send_header("Content-Type",ctype)
        self.send_header("Content-Length",str(len(b))); self.end_headers(); self.wfile.write(b)
    def log_message(self,*a): pass
    def do_GET(self):
        from urllib.parse import urlparse, parse_qs
        u=urlparse(self.path); q=parse_qs(u.query)
        if u.path in ("/","/index.html"): return self._send(200, PAGE, "text/html; charset=utf-8")
        if u.path=="/api/pick":
            n=int(q.get("n",["5"])[0]); pool=IDS[:]; random.shuffle(pool)
            chosen=pool[:max(1,min(n,len(pool)))]
            return self._send(200, json.dumps([{"id":i,"diff":BANKD[i]["diff"]} for i in chosen]))
        if u.path=="/api/problem":
            p=BANKD.get(q.get("id",[""])[0]);
            if not p: return self._send(404,"{}")
            return self._send(200, json.dumps({k:p[k] for k in ("id","pat","diff","title","story","cons","inf","outf","sin","sout","exp")}))
        if u.path=="/api/reveal":
            p=BANKD.get(q.get("id",[""])[0]);
            if not p: return self._send(404,"{}")
            return self._send(200, json.dumps(p["ans"]))
        return self._send(404,"{}")
    def do_POST(self):
        n=int(self.headers.get("Content-Length","0")); data=json.loads(self.rfile.read(n) or "{}")
        if self.path=="/api/judge":
            pid=data.get("id"); code=data.get("code",""); sample=bool(data.get("sample"))
            if pid not in BANKD: return self._send(404,"{}")
            res=judge(pid, code, sample); res["tl"]=TIME_LIMIT
            try: log_attempt(pid, res["verdict"], int(data.get("secs",0)), code, sample)
            except Exception: pass
            return self._send(200, json.dumps(res))
        if self.path=="/api/save":
            pid=data.get("id")
            if pid in BANKD:
                try: log_advance(pid, data.get("best","NONE"), int(data.get("secs",0)), int(data.get("over",0)), data.get("code",""))
                except Exception: pass
            return self._send(200, "{}")
        return self._send(404,"{}")

def main():
    srv=ThreadingHTTPServer(("127.0.0.1",PORT), H); url="http://127.0.0.1:%d/"%PORT
    print("OA Solve (web) running at "+url+"  --  Ctrl+C to stop.")
    threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try: srv.serve_forever()
    except KeyboardInterrupt: print("\nstopped. records in oa_records.md")

if __name__=="__main__": main()
