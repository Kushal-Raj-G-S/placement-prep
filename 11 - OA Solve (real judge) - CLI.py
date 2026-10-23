# -*- coding: utf-8 -*-
# =====================================================================================
#  OA SOLVE  -- your personal Online Assessment JUDGE  (tool #11)
#  Companion to "10 - Mock OA (timed exam).html".
#  That HTML trains you to DECODE + name the pattern. This one is the REAL deal:
#  you actually SOLVE the problem in Python and get a real AC / WA / TLE verdict,
#  checked against clean test cases (each expected output computed by a verified oracle).
#
#  HOW TO USE
#  1) Keep this file, oa_bank.json and oa_cases.json in the same folder.
#  2) Run:   python "11 - OA Solve (real judge).py"
#  3) Pick a timed mock (or practice one problem).
#  4) For each question, write a FULL program that reads from standard input and prints
#     the answer to standard output -- exactly like a real HackerRank/HackerEarth problem.
#     Put your program in  solution.py  (same folder). A starter solution.py is created
#     for you the first time.
#  5) Press ENTER to judge. You'll see AC / WA / TLE, and on a miss, the first failing case.
#  6) Every attempt is logged to  oa_records.md  so we can go through them together later.
#
#  No internet, no install -- just the Python you already have.
# =====================================================================================
import json, os, sys, subprocess, random, time, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
BANK  = os.path.join(HERE, "data", "oa_bank.json")
CASES = os.path.join(HERE, "data", "oa_cases.json")
SOL   = os.path.join(HERE, "solution.py")
LOG   = os.path.join(HERE, "oa_records.md")
TIME_LIMIT = 5.0   # seconds per test case (TLE guard)

STARTER = '''# Write your solution here. Read from input(), print the answer.
# Example skeleton (delete and write your own):
import sys
data = sys.stdin.read().split("\\n")
# first = data[0].split()
# ... parse, solve, print(answer)
'''

def load():
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
        print("ERROR: oa_bank.json / oa_cases.json not found next to this script."); sys.exit(1)
    return json.load(open(BANK, encoding="utf-8")), json.load(open(CASES, encoding="utf-8"))

def hr(c="-", n=70): print(c*n)

def show_problem(p, qno=None, total=None, mins=None):
    hr("=")
    tag = "Easy" if p["diff"]=="E" else ("Hard" if p["diff"]=="H" else "Medium")
    head = "QUESTION" if qno is None else f"QUESTION {qno}/{total}"
    extra = f"   [hard cap: {mins} min]" if mins else ""
    print(f"{head}   [{tag}]   id={p['id']}{extra}")
    hr("=")
    print(p["title"]); print()
    print(p["story"]); print()
    print("CONSTRAINTS");    [print("  - "+c) for c in p["cons"]]
    print("INPUT FORMAT");   [print("  - "+c) for c in p["inf"]]
    print("OUTPUT FORMAT");  [print("  - "+c) for c in p["outf"]]
    print("\nSAMPLE INPUT");  print("  " + p["sin"].replace("\n","\n  "))
    print("SAMPLE OUTPUT"); print("  " + str(p["sout"]).replace("\n","\n  "))
    print()
    print(f"Write your program in:  {SOL}")

def normalize(s):
    lines = s.replace("\r\n","\n").split("\n")
    while lines and lines[-1].strip()=="": lines.pop()
    return [ln.rstrip() for ln in lines]

def run_case(inp):
    try:
        r = subprocess.run([sys.executable, SOL], input=inp, capture_output=True,
                           text=True, timeout=TIME_LIMIT)
    except subprocess.TimeoutExpired:
        return ("TLE", "")
    if r.returncode != 0:
        return ("RE", (r.stderr or "").strip())
    return ("OK", r.stdout)

def judge(pid, cases):
    if not os.path.exists(SOL):
        open(SOL,"w",encoding="utf-8").write(STARTER)
    total=len(cases)
    for i,c in enumerate(cases, start=1):
        status,payload = run_case(c["in"])
        if status=="TLE":
            return ("TLE", i, c, "(timed out)")
        if status=="RE":
            return ("RE", i, c, payload)
        if normalize(payload)!=normalize(c["out"]):
            return ("WA", i, c, payload)
    return ("AC", total, None, None)

def verdict_report(pid, title, cases):
    print("\nJudging against", len(cases), "test case(s) ...")
    res, idx, case, got = judge(pid, cases)
    if res=="AC":
        print(f"  ✓ ACCEPTED  -- passed all {idx} test case(s).")
    elif res=="WA":
        print(f"  ✗ WRONG ANSWER on test case {idx}:")
        print("    input:    " + case['in'].replace('\n','\\n'))
        print("    expected: " + case['out'].replace('\n','\\n'))
        print("    your out: " + (got.strip().replace('\n','\\n') if got.strip() else "(empty)"))
    elif res=="TLE":
        print(f"  ✗ TIME LIMIT EXCEEDED on test case {idx} (> {TIME_LIMIT:.0f}s).")
    elif res=="RE":
        print(f"  ✗ RUNTIME ERROR on test case {idx}:")
        print("    " + (got.splitlines()[-1] if got else "(no message)"))
    return res

def log_attempt(p, res, secs):
    code = open(SOL,encoding="utf-8").read() if os.path.exists(SOL) else "(no solution.py)"
    with open(LOG,"a",encoding="utf-8") as f:
        f.write(f"\n## {datetime.datetime.now():%Y-%m-%d %H:%M}  |  {p['id']} {p['title']}  |  {res}  |  {secs}s\n")
        f.write(f"_Pattern (revealed after attempt): {p['ans']['pattern']}_\n\n")
        f.write("```python\n"+code+"\n```\n")

def reveal(p):
    a=p["ans"]
    print("\n--- INTENDED APPROACH (compare after you've committed) ---")
    print("Pattern:      "+a["pattern"])
    print("Brute force:  "+a["brute"])
    print("Optimal:      "+a["opt"])
    print("Complexity:   "+a["cx"])

def attempt(p, cases, qno=None, total=None, mins=None):
    show_problem(p, qno, total, mins)
    start=time.time()
    while True:
        print("\n[ENTER]=judge   r=reveal approach   s=skip   q=quit")
        cmd=input("> ").strip().lower()
        if cmd=="q": return "quit"
        if cmd=="s":
            log_attempt(p,"SKIPPED",int(time.time()-start)); return "skip"
        if cmd=="r": reveal(p); continue
        res=verdict_report(p["id"], p["title"], cases)
        secs=int(time.time()-start)
        log_attempt(p,res,secs)
        if res=="AC":
            print(f"  (time on this problem: {secs//60}m {secs%60}s)")
            reveal(p); return "ac"
        print("  Keep fixing solution.py and press ENTER to re-judge, or s to skip.")

def pick(bank, n):
    ids=list(bank.keys()); random.shuffle(ids); return ids[:n]

def main():
    bank, cases = load()
    print("\n"+"="*70)
    print(" OA SOLVE  --  real Python judge  ("+str(len(bank))+" problems)")
    print("="*70)
    print(" [1] Timed mock  (random problems, hard per-question cap)")
    print(" [2] Practice one problem by id")
    print(" [3] Quit")
    choice=input("> ").strip()
    if choice=="2":
        pid=input("problem id (e.g. b1, c3, h2): ").strip()
        if pid not in bank: print("no such id."); return
        attempt(bank[pid], cases.get(pid, [{"in":bank[pid]["sin"],"out":str(bank[pid]["sout"])}]))
    elif choice=="1":
        try:
            n=int(input("how many questions? ").strip() or "5")
            mins=int(input("minutes per question (hard cap, just a guide here)? ").strip() or "20")
        except ValueError:
            n,mins=5,20
        ids=pick(bank,n); acc=0
        for i,pid in enumerate(ids, start=1):
            r=attempt(bank[pid], cases.get(pid, [{"in":bank[pid]["sin"],"out":str(bank[pid]["sout"])}]), i, len(ids), mins)
            if r=="quit": break
            if r=="ac": acc+=1
        print("\n"+"="*70)
        print(f" TEST DONE.  Accepted {acc}/{len(ids)}.  Full log in oa_records.md")
        print(" Paste oa_records.md (or the parts you want) into the chat and we'll review together.")
        print("="*70)
    else:
        print("bye.")

if __name__=="__main__":
    try: main()
    except (KeyboardInterrupt, EOFError):
        print("\ninterrupted. progress saved in oa_records.md")
