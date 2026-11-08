# -*- coding: utf-8 -*-
"""
Build the THRESHOLD SET for every pattern block in the Twenty Weeks tracker.

Idea: a pattern has several variants (Pattern Radar). The threshold set is the smallest set of problems that gives you real
experience of every variant you could realistically be asked, so you can move to the next pattern with confidence. It is
sized by the variants, not by a fixed number. Rare or very hard variants are left out on purpose (listed on the block) and
live in the extra practice instead.

    python _build/make_thresholds.py        (safe to re-run: it rebuilds its own flags)

What it writes into each block's items:  th=1 (in the threshold), to=order, v=the variant it teaches.
It may append a few library problems to a block when the block has none for a variant. Existing items never move,
so tick marks stay where they are.
"""
import json, os, re, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TRACKER = os.path.join(ROOT, "1 - Twenty Weeks to AC (tracker).html")
sys.path.insert(0, HERE)
import pattern_library as PL

VNAME = {v["id"]: v["name"] for p in PL.PATTERNS for v in p["variants"]}

# block -> the variants worth experiencing, and the ones left out on purpose (rare, or very hard for a first pass)
PLAN = {
 "a1": (["hs-seen", "hs-freq", "hs-index", "hs-group"], []),
 "a2": (["tp-ends", "tp-write", "tp-merge", "tp-partition"], []),
 "a3": (["sw-fixed", "sw-longest", "sw-shortest"], ["sw-exact", "sw-deque"]),
 "a4": (["ps-range", "ps-count", "ps-longest", "ps-diff", "ps-suffix"], ["ps-2d"]),
 "a5": (["iv-merge", "iv-insert", "iv-greedy", "iv-sweep", "iv-sortkey"], []),
 "a6": (["bs-exact", "bs-bound", "bs-answer", "bs-rotated"], ["bs-partition"]),
 "a7": (["ms-match", "ms-next", "ms-greedy"], ["ms-hist"]),
 "b2": (["td-up", "td-down", "td-bst", "td-lca", "tb-levels"], ["tr-basic", "tr-search"]),
 "n1": (["ll-fastslow", "ll-reverse", "ll-dummy", "ll-merge"], []),
 "b5": (["gr-flood", "gr-bfs", "gr-multi"], []),
 "b3": (["hp-topk", "hp-merge", "hp-two", "hp-greedy"], []),
 "b7": (["dp-linear", "dp-kadane"], []),
 "b8": (["dp-knapsack", "dp-coin"], []),
 "b9": (["dp-grid"], []),
 "b10": (["dp-twostring"], ["dp-interval"]),
 "b11": (["dp-lis"], []),
 "b4": (["gr-reach", "gr-pair", "gr-local"], []),
 "b13": (["bt-xor", "bt-tricks"], ["bt-subsets", "bt-dp"]),
 "b1": (["bk-subsets", "bk-perms"], ["bk-board"]),
 "b6": (["to-kahn", "sp-dijkstra", "dsu-connect", "dsu-cycle", "dsu-kruskal"], ["to-dfs", "sp-bellman", "sp-floyd"]),
 "n3": (["hs-cyclic"], []),
 "a8": ([], []), "n2": ([], []), "b12": ([], []),        # no variant list in the library: platform picks + the block's own mediums
}
# variants asked most often get two problems, so one problem never has to carry a whole variant
MAIN = {"hs-freq", "hs-index", "tp-ends", "tp-write", "sw-longest", "ps-count", "bs-answer", "bs-exact", "ms-next", "hp-topk", "iv-merge",
        "ll-fastslow", "ll-reverse", "td-up", "td-down", "gr-flood", "gr-bfs", "dp-linear", "dp-knapsack", "dp-grid", "dp-twostring", "dp-lis",
        "gr-local", "bk-subsets", "sp-dijkstra", "dsu-connect", "to-kahn", "bt-xor", "dp-kadane", "dp-coin", "hs-cyclic"}
MIN_BLOCK = 4                                           # a block with fewer variants than this gets deeper on the main ones
PLATFORMS = ("GeeksforGeeks", "HackerRank", "HackerEarth", "CodeChef")


def slug(u):
    m = re.search(r"leetcode\.com/problems/([^/?#]+)", u or "")
    return m.group(1) if m else None


def lc_difficulty():
    """slug -> E/M/H for every LeetCode problem (public list, paged)."""
    q = "query($c:String!,$l:Int,$s:Int){problemsetQuestionList:questionList(categorySlug:$c,limit:$l,skip:$s,filters:{}){questions:data{titleSlug difficulty}}}"
    def page(s):
        for _ in range(3):
            try:
                r = urllib.request.Request("https://leetcode.com/graphql", data=json.dumps({"query": q, "variables": {"c": "", "l": 100, "s": s}}).encode(),
                                           headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0", "Referer": "https://leetcode.com/problemset/"})
                return json.loads(urllib.request.urlopen(r, timeout=40).read().decode())["data"]["problemsetQuestionList"]["questions"]
            except Exception:
                pass
        return []
    with ThreadPoolExecutor(6) as ex:
        pages = list(ex.map(page, range(0, 4200, 100)))
    return {x["titleSlug"]: {"Easy": "E", "Medium": "M", "Hard": "H"}[x["difficulty"]] for pg in pages for x in pg}


def main():
    lib = json.load(open(os.path.join(HERE, "links.json"), encoding="utf-8"))["variants"]
    diff = lc_difficulty()
    html = open(TRACKER, encoding="utf-8").read()
    head, rest = html.split('<script type="application/json" id="plan">', 1)
    body, tail = rest.split("</script>", 1)
    plan = json.loads(body)

    report = []
    for tr in plan["tracks"]:
        if tr["id"] != "td":
            continue
        for ph in tr["phases"]:
            for blk in ph["blocks"]:
                bid = blk["id"]
                for it in blk["items"]:                         # rebuild from scratch each run
                    for k in ("th", "to", "v"):
                        it.pop(k, None)
                blk.pop("thNote", None)
                if bid not in PLAN:
                    continue
                keep, skip = PLAN[bid]
                by_slug = {slug(it.get("u")): i for i, it in enumerate(blk["items"]) if slug(it.get("u"))}
                used, order = set(), []

                def add_flag(idx, label):
                    blk["items"][idx]["th"] = 1
                    blk["items"][idx]["v"] = label
                    order.append(idx)
                    used.add(idx)

                per_variant = {v: 2 if v in MAIN else 1 for v in keep}
                if keep and sum(per_variant.values()) < MIN_BLOCK:                 # thin block (few variants): go deeper on the main ones
                    for v in keep:
                        per_variant[v] = 3 if v in MAIN else 2
                for v in keep:
                    cands = [x for x in lib.get(v, []) if x["p"] == "LeetCode" and diff.get(slug(x["u"]), "M") != "H"]
                    got = 0
                    for x in cands:                                                   # canonical first (library order); prefer ones already in the block
                        if got >= per_variant[v]:
                            break
                        s = slug(x["u"])
                        if s in by_slug and by_slug[s] not in used:
                            add_flag(by_slug[s], VNAME[v]); got += 1
                    for x in cands:                                                   # not enough in the block: append verified library problems
                        if got >= per_variant[v]:
                            break
                        s = slug(x["u"])
                        if s in by_slug:
                            continue
                        blk["items"].append({"t": "%s  (library: %s)" % (x["n"], VNAME[v]), "u": x["u"], "d": diff.get(s, "M")})
                        by_slug[s] = len(blk["items"]) - 1
                        add_flag(by_slug[s], VNAME[v]); got += 1
                # one from each other platform: Medium first (the block is already ordered Medium/Hard/Easy by popularity)
                for src in PLATFORMS:
                    pick = None
                    for i, it in enumerate(blk["items"]):
                        if i in used or it.get("x") != "other" or not it["t"].startswith(src + ":") or it.get("d") not in ("M", "E"):
                            continue
                        if it["d"] == "M":
                            pick = i; break
                    if pick is not None:
                        add_flag(pick, "mixed practice (" + src + ")")
                if not keep:                                                           # variant-less blocks: add two of the block's own mediums
                    n = 0
                    for i, it in enumerate(blk["items"]):
                        if i not in used and it.get("d") == "M" and not it.get("x"):
                            add_flag(i, "core practice"); n += 1
                            if n == 2:
                                break
                for rank, idx in enumerate(order):
                    blk["items"][idx]["to"] = rank
                if skip:
                    blk["thNote"] = "Left out of the threshold on purpose (rare, or very hard for a first pass): " + ", ".join(VNAME[v] for v in skip) + ". They are in the extra practice below."
                report.append((bid, blk["name"][:44], len(keep), len(order), len(blk["items"])))

    new_body = json.dumps(plan, ensure_ascii=False, indent=2)
    open(TRACKER, "w", encoding="utf-8", newline="\n").write(head + '<script type="application/json" id="plan">' + new_body + "</script>" + tail)
    print("block  name                                          variants  threshold  (block total)")
    for r in report:
        print("  %-4s %-44s %5d %9d   (%d)" % r)
    print("threshold problems in total:", sum(r[3] for r in report))


if __name__ == "__main__":
    main()
