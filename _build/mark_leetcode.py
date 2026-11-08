# -*- coding: utf-8 -*-
"""
Mark LeetCode problems you have solved as done ("ac") in the Twenty Weeks tracker.

    python _build/mark_leetcode.py            # public: your 20 most recent accepted submissions
    python _build/mark_leetcode.py --file     # also reads data/leetcode_solved.json  (a JSON list of title slugs)

Why two sources: LeetCode only makes your most recent 20 accepted submissions public. The full list needs you to be logged in,
so you export it yourself from your own browser (the snippet is in the README / printed below) and drop the file in data/.
No password, cookie or token is ever needed here or shared with anyone.

The ticks are written to data/progress.json under the tracker's own key, the same place the hub saves them.
"""
import datetime, json, os, re, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TRACKER = os.path.join(ROOT, "1 - Twenty Weeks to AC (tracker).html")
PROGRESS = os.path.join(ROOT, "data", "progress.json")
SOLVED_FILE = os.path.join(ROOT, "data", "leetcode_solved.json")
KEY = "oa-tracker-state-v3"
USER = "Kushal-Raj-G-S"

CONSOLE_SNIPPET = """fetch('/graphql',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({query:`query($c:String!,$l:Int,$s:Int,$f:QuestionListFilterInput){problemsetQuestionList:questionList(categorySlug:$c,limit:$l,skip:$s,filters:$f){total:totalNum questions:data{titleSlug}}}`,variables:{c:'',l:3000,s:0,f:{status:'AC'}}})}).then(r=>r.json()).then(j=>{const s=j.data.problemsetQuestionList.questions.map(q=>q.titleSlug);copy(JSON.stringify(s));console.log(s.length+' solved problems copied to your clipboard')})"""


def recent_public():
    q = "query($u:String!,$l:Int){recentAcSubmissionList(username:$u,limit:$l){title titleSlug timestamp}}"
    req = urllib.request.Request("https://leetcode.com/graphql", data=json.dumps({"query": q, "variables": {"u": USER, "l": 50}}).encode(),
                                 headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0", "Referer": "https://leetcode.com/u/%s/" % USER})
    d = json.loads(urllib.request.urlopen(req, timeout=30).read().decode())
    return (d.get("data") or {}).get("recentAcSubmissionList") or []


def main():
    use_file = "--file" in sys.argv
    solved = {}                                   # slug -> date (or "" when unknown)
    for r in recent_public():
        solved[r["titleSlug"]] = datetime.date.fromtimestamp(int(r["timestamp"])).isoformat()
    from_public = len(solved)
    if use_file:
        if not os.path.exists(SOLVED_FILE):
            sys.exit("no %s yet. Run this in the console of a logged-in leetcode.com tab, then save the clipboard there:\n\n%s\n" % (SOLVED_FILE, CONSOLE_SNIPPET))
        for slug in json.load(open(SOLVED_FILE, encoding="utf-8")):
            solved.setdefault(slug, "")

    html = open(TRACKER, encoding="utf-8").read()
    plan = json.loads(html.split('<script type="application/json" id="plan">', 1)[1].split("</script>", 1)[0])
    where = {}                                    # slug -> [item keys]
    for tr in plan["tracks"]:
        for ph in tr["phases"]:
            for blk in ph["blocks"]:
                for i, it in enumerate(blk["items"]):
                    m = re.search(r"leetcode\.com/problems/([^/?#]+)", it.get("u", ""))
                    if m:
                        where.setdefault(m.group(1), []).append("%s:%d" % (blk["id"], i))

    kv = json.load(open(PROGRESS, encoding="utf-8")) if os.path.exists(PROGRESS) else {}
    raw = kv.get(KEY)
    st = json.loads(raw) if isinstance(raw, str) and raw else (raw or {})
    st.setdefault("v", 3); st.setdefault("rev", 0); st.setdefault("s", {}); st.setdefault("d", {}); st.setdefault("log", {}); st.setdefault("start", "")

    matched, already, missing = 0, 0, []
    for slug, day in solved.items():
        keys = where.get(slug)
        if not keys:
            missing.append(slug)
            continue
        for k in keys:
            if st["s"].get(k) == "ac":
                already += 1
                continue
            st["s"][k] = "ac"
            matched += 1
            if day:
                st["d"][k] = day
                st["log"][day] = st["log"].get(day, 0) + 1
    st["rev"] = int(st.get("rev", 0)) + 1
    kv[KEY] = json.dumps(st, separators=(",", ":"))
    os.makedirs(os.path.dirname(PROGRESS), exist_ok=True)
    tmp = PROGRESS + ".tmp"
    json.dump(kv, open(tmp, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    os.replace(tmp, PROGRESS)

    print("solved problems read: %d (%d public recent%s)" % (len(solved), from_public, ", + data/leetcode_solved.json" if use_file else ""))
    print("ticked in the tracker: %d new, %d already ticked" % (matched, already))
    print("solved on LeetCode but not in the tracker's list: %d" % len(missing))
    if missing:
        print("   " + ", ".join(sorted(missing)[:40]) + (" ..." if len(missing) > 40 else ""))
    if not use_file:
        print("\nTo add the rest of your %s solved problems: run this in the console of a logged-in leetcode.com tab, save the clipboard to\n%s\nthen run:  python _build/mark_leetcode.py --file\n\n%s\n" % ("122", SOLVED_FILE, CONSOLE_SNIPPET))


if __name__ == "__main__":
    main()
