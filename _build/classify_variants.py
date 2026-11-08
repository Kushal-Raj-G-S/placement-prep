# -*- coding: utf-8 -*-
"""
Decide which VARIANT of a pattern each non-LeetCode problem teaches, so threshold sets can be built from variants, not topics.

    python _build/classify_variants.py        (needs the key in .env and .other_cache.json; results go to .variant_cache.json)

For every block, the candidate problems (from fetch_other.py) are shown to the model together with the block's variants
(name, when it applies, typical questions). The model answers with one variant id per problem, or "none" when the problem does
not clearly teach one. Only confident answers are kept. A problem the model cannot place is simply not used in a threshold set.
"""
import json, os, re, sys, time
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import add_other_platforms as AOP
import llm_config
import make_thresholds as MT
import pattern_library as PL
from llm_check import call

CACHE = os.path.join(HERE, ".other_cache.json")
OUT = os.path.join(HERE, ".variant_cache.json")
VAR = {v["id"]: v for p in PL.PATTERNS for v in p["variants"]}

SYSTEM = """You classify programming practice problems by the technique VARIANT they teach.

You are given a list of VARIANTS (id, name, when it applies, typical questions) and a list of PROBLEMS (number, platform, title, topic tags, difficulty).
For each problem answer with the id of the ONE variant whose technique is the main idea needed to solve it, or "none".
Be strict. Answer "none" whenever the title and tags do not clearly point to one of the variants, or when the problem is really about something else (plain maths, simulation, ad-hoc observation, geometry).
Never invent an id. Output ONLY a JSON object mapping the problem number (as a string) to a variant id or "none". No explanations."""


def describe(vid):
    v = VAR[vid]
    asks = "; ".join(re.sub(r"<[^>]+>", "", a) for a in (v.get("asks") or [])[:5])
    return "- %s | %s | when: %s | typical: %s" % (vid, v["name"], re.sub(r"<[^>]+>", "", v["when"]), asks)


def ask(cfg, model, variants, batch):
    user = "VARIANTS\n" + "\n".join(describe(v) for v in variants) + "\n\nPROBLEMS\n" + "\n".join(
        "%d | %s | %s | tags: %s | %s" % (i, c["src"], c["name"], c.get("tags", ""), c["d"]) for i, c in enumerate(batch))
    payload = {"model": model, "temperature": 0.0, "max_tokens": 1500,
               "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}]}
    payload.update(llm_config.options_for(model))
    for attempt in range(6):
        try:
            out = call(cfg, "/chat/completions", payload, timeout=90)
            txt = (out["choices"][0]["message"].get("content") or "")
            m = re.search(r"\{.*\}", txt, re.S)
            return json.loads(m.group(0)) if m else {}
        except Exception:
            time.sleep(8 * (attempt + 1))
    return {}


def main():
    cache = json.load(open(CACHE, encoding="utf-8"))
    cands = AOP.candidates(cache)
    tagmap = {}
    for x in cache["hr"]:
        tagmap["https://www.hackerrank.com/challenges/%s/problem" % x["slug"]] = ", ".join([x.get("sub") or ""] + list(x.get("topics") or [])[:3])
    for x in cache["cc"]:
        tagmap["https://www.codechef.com/problems/%s" % x["code"]] = ", ".join(x["tags"][:5])
    for x in cache["gf"]:
        tagmap[x["url"]] = ", ".join(x["topics"][:5])
    for x in cache.get("he", []):
        tagmap[x["url"]] = ", ".join(x["tags"][:4])
    for lst in cands.values():
        for c in lst:
            c["tags"] = tagmap.get(c["url"], "")
    cfg = llm_config.load()
    model = cfg["model"]
    done = json.load(open(OUT, encoding="utf-8")) if os.path.exists(OUT) else {}
    jobs = []
    for bid, (keep, skip) in MT.PLAN.items():
        variants = keep + skip
        if not variants:
            continue
        pool = {}
        for c in cands.get(bid, []):
            pool.setdefault(c["src"], []).append(c)
        for src, lst in pool.items():
            lst = sorted(lst, key=lambda c: -c["pop"])[:160]
            for k in range(0, len(lst), 25):
                jobs.append((bid, variants, [c for c in lst[k:k + 25] if c["url"] not in done]))
    jobs = [j for j in jobs if j[2]]
    print("model:", model, "| batches:", len(jobs))

    def run(job):
        bid, variants, batch = job
        ans = ask(cfg, model, variants, batch)
        if not ans:
            return {}                     # the call failed (rate limit, timeout): do NOT record "none", so a re-run tries again
        res = {}
        for i, c in enumerate(batch):
            v = ans.get(str(i))
            res[c["url"]] = {"block": bid, "v": v if v in variants else "none", "name": c["name"], "src": c["src"]}
        return res
    kept = 0
    with ThreadPoolExecutor(2) as ex:
        for res in ex.map(run, jobs):
            done.update(res)
            kept += sum(1 for r in res.values() if r["v"] != "none")
            json.dump(done, open(OUT, "w", encoding="utf-8"), ensure_ascii=False)
    n = sum(1 for r in done.values() if r["v"] != "none")
    print("classified %d problems; %d placed on a variant, %d answered none" % (len(done), n, len(done) - n))
    from collections import Counter
    print("per variant:", dict(Counter(r["v"] for r in done.values() if r["v"] != "none")))


if __name__ == "__main__":
    main()
