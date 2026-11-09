# -*- coding: utf-8 -*-
"""
Build the THRESHOLD SET for every pattern block in the Twenty Weeks tracker.

A pattern has variants (Pattern Radar). The threshold set is the set of problems that gives you real experience of every
variant you could realistically be asked, so finishing it is your signal to move to the next pattern. It is sized by the
variants, not by a fixed number. Rare or very hard variants are left out on purpose (listed on the block).

    python _build/classify_variants.py      # once: which variant does each GfG / HackerRank / HackerEarth / CodeChef problem teach
    python _build/make_thresholds.py        # build the sets (safe to re-run: it rebuilds its own flags)

Per common variant:  2 LeetCode problems from the verified library (a classic first, then a second one), plus problems from the
other platforms that were matched to THAT variant. Main variants (asked most) get more. Nothing here is matched by topic alone.
Flags written into each block's items:  th=1, to=order, v=the variant that problem teaches. Existing items never move.
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
 "a1": (["hs-seen", "hs-freq", "hs-index", "hs-group", "hs-moore"], []),
 "a2": (["tp-ends", "tp-write", "tp-merge", "tp-partition", "tp-centre"], []),
 "a3": (["sw-fixed", "sw-longest", "sw-shortest", "sw-complement"], ["sw-exact", "sw-deque"]),
 "a4": (["ps-range", "ps-count", "ps-longest", "ps-diff", "ps-suffix"], ["ps-2d"]),
 "a5": (["iv-merge", "iv-insert", "iv-greedy", "iv-sweep", "iv-sortkey", "dc-mergecount", "dc-quickselect", "dc-bucket"], ["dc-split"]),
 "a6": (["bs-exact", "bs-bound", "bs-answer", "bs-rotated"], ["bs-partition"]),
 "a7": (["ms-match", "ms-next", "ms-greedy", "ms-contrib"], ["ms-hist"]),
 "b2": (["td-up", "td-down", "td-bst", "td-lca", "tb-levels", "td-global", "td-state", "td-build", "td-parent", "tb-index"], ["tr-basic", "tr-search", "tr-xor", "td-reroot", "td-lift"]),
 "n1": (["ll-fastslow", "ll-reverse", "ll-dummy", "ll-merge", "ll-gap", "ll-hash"], []),
 "n4": (["ds-lru", "ds-aux", "ds-queue", "ds-random", "ds-timekey"], ["ds-iter"]),
 "b5": (["gr-flood", "gr-bfs", "gr-multi", "gr-border", "gw-components", "gw-bipartite", "gw-state"], []),
 "b3": (["hp-topk", "hp-merge", "hp-two", "hp-greedy", "hp-sorted"], []),
 "b7": (["dp-linear", "dp-kadane", "dp-partition"], []),
 "b8": (["dp-knapsack", "dp-coin"], []),
 "b9": (["dp-grid"], []),
 "b10": (["dp-twostring"], ["dp-interval", "dp-digit"]),
 "b11": (["dp-lis"], []),
 "b12": (["dp-state"], []),
 "b4": (["gr-reach", "gr-pair", "gr-local", "gr-twopass", "gr-balance"], []),
 "b13": (["bt-xor", "bt-tricks", "bt-perbit", "ma-gcd", "ma-sieve", "ma-modpow", "ma-ncr", "ma-digits", "ma-game"], ["bt-subsets", "bt-dp", "ma-geom"]),
 "b1": (["bk-subsets", "bk-perms", "bk-partition", "bk-build", "bk-bucket"], ["bk-board"]),
 "b6": (["to-kahn", "sp-dijkstra", "sp-01bfs", "sp-mod", "dsu-connect", "dsu-cycle", "dsu-kruskal", "dsu-prim", "gw-functional"], ["to-dfs", "sp-bellman", "sp-floyd", "gw-bridges", "gw-scc", "gw-euler"]),
 "n3": (["hs-cyclic"], []),
 "n2": (["sim-spiral", "sim-rotate", "sim-marking", "sim-rules"], []),
 "a8": ([], []),                          # no variant list of its own: the block's own problems, easier to harder
}
MAIN = {"hs-freq", "hs-index", "tp-ends", "tp-write", "sw-longest", "ps-count", "bs-answer", "bs-exact", "ms-next", "hp-topk", "iv-merge",
        "ll-fastslow", "ll-reverse", "td-up", "td-down", "gr-flood", "gr-bfs", "dp-linear", "dp-knapsack", "dp-grid", "dp-twostring", "dp-lis",
        "gr-local", "bk-subsets", "sp-dijkstra", "dsu-connect", "to-kahn", "bt-xor", "dp-kadane", "dp-coin", "hs-cyclic"}
LC_PER_VARIANT = 2                       # a classic, then a second one
OTHER_MAIN, OTHER_MINOR = 2, 1           # problems from the other platforms matched to this exact variant
TARGET_MAIN, TARGET_MINOR = 4, 3         # if another platform has too few for a variant, more LeetCode fills the gap up to this
THIN_BLOCK = 8                           # a pattern with very few variants still has to give enough experience


def slug(u):
    m = re.search(r"leetcode\.com/problems/([^/?#]+)", u or "")
    return m.group(1) if m else None


def lc_difficulty():
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
    import add_other_platforms as AOP
    lib = json.load(open(os.path.join(HERE, "links.json"), encoding="utf-8"))["variants"]
    cache = json.load(open(os.path.join(HERE, ".other_cache.json"), encoding="utf-8"))
    vc_path = os.path.join(HERE, ".variant_cache.json")
    vc = json.load(open(vc_path, encoding="utf-8")) if os.path.exists(vc_path) else {}
    pool = {}                                                         # url -> candidate dict (src, name, url, d, pop, note)
    for lst in AOP.candidates(cache).values():
        for c in lst:
            pool.setdefault(c["url"], c)
    by_variant = {}                                                   # variant -> other-platform problems matched to it
    for url, r in vc.items():
        if r["v"] != "none" and url in pool:
            by_variant.setdefault(r["v"], []).append(pool[url])
    diff = lc_difficulty()

    html = open(TRACKER, encoding="utf-8").read()
    head, rest = html.split('<script type="application/json" id="plan">', 1)
    body, tail = rest.split("</script>", 1)
    plan = json.loads(body)

    # blocks that exist only because a pattern was added later (new ids, so no existing tick moves)
    for tr in plan["tracks"]:
        if tr["id"] == "td":
            for ph in tr["phases"]:
                if ph["id"] == "p2" and not any(b["id"] == "n4" for b in ph["blocks"]):
                    at = next(i for i, b in enumerate(ph["blocks"]) if b["id"] == "n1") + 1
                    ph["blocks"].insert(at, {"id": "n4", "name": "Design a data structure", "core": True, "isNew": True,
                                             "why": "A class with methods and a required speed. Asked often in interviews, and it needs a hashmap joined to a list, stack or array.", "items": []})

    report = []
    remap = {}
    for tr in plan["tracks"]:                                  # variant names are not shown on problems (the user finds the variant)
        for ph in tr.get("phases", []):
            for blk in ph.get("blocks", []):
                for it in blk.get("items", []):
                    if it.get("x") != "other" and "  (" in it.get("t", ""):
                        it["t"] = it["t"].split("  (")[0]
    for tr in plan["tracks"]:
        if tr["id"] != "td":
            continue
        for ph in tr["phases"]:
            for blk in ph["blocks"]:
                bid = blk["id"]
                for it in blk["items"]:
                    for k in ("th", "to", "v"):
                        it.pop(k, None)
                blk.pop("thNote", None)
                if bid not in PLAN:
                    continue
                keep, skip = PLAN[bid]
                by_url = {it.get("u"): i for i, it in enumerate(blk["items"]) if it.get("u")}
                by_slug = {slug(it.get("u")): i for i, it in enumerate(blk["items"]) if slug(it.get("u"))}
                used, groups = set(), []                              # groups: [(variant label, [item indexes])]

                def flag(idx, label, group):
                    blk["items"][idx]["th"] = 1
                    blk["items"][idx]["v"] = label
                    used.add(idx)
                    group.append(idx)

                def other_item(c):                                    # make sure an other-platform problem exists in the block
                    if c["url"] in by_url:
                        return by_url[c["url"]]
                    blk["items"].append({"t": "%s: %s  (%s)" % (c["src"], c["name"], c["note"]), "u": c["url"], "d": c["d"], "x": "other"})
                    by_url[c["url"]] = len(blk["items"]) - 1
                    return by_url[c["url"]]

                def lc_item(x, v):
                    s = slug(x["u"])
                    if s in by_slug:
                        return by_slug[s]
                    blk["items"].append({"t": x["n"], "u": x["u"], "d": diff.get(s, "M")})
                    by_slug[s] = len(blk["items"]) - 1
                    return by_slug[s]

                thin = len(keep) * (LC_PER_VARIANT + 1) < THIN_BLOCK
                for v in keep:
                    group = []
                    label = VNAME[v]
                    main = v in MAIN
                    want_other = (OTHER_MAIN if main else OTHER_MINOR) + (1 if thin else 0)
                    target = (TARGET_MAIN if main else TARGET_MINOR) + (1 if thin else 0)
                    # (1) other platforms, matched to this variant: Medium first, easy ones as builders, different platforms before the same one twice
                    oth = sorted([c for c in by_variant.get(v, []) if c["d"] in ("M", "E")], key=lambda c: ({"M": 0, "E": 1}[c["d"]], -c["pop"]))
                    chosen, srcs = [], set()
                    for c in oth:
                        if len(chosen) >= want_other:
                            break
                        if c["src"] in srcs and len(set(x["src"] for x in oth)) > len(srcs):
                            continue
                        chosen.append(c); srcs.add(c["src"])
                    for c in oth:
                        if len(chosen) >= want_other:
                            break
                        if c not in chosen:
                            chosen.append(c)
                    # (2) LeetCode from the verified library: a classic first, then more until the variant has enough experience
                    lc_all = [x for x in lib.get(v, []) if x["p"] == "LeetCode"]
                    lc = [x for x in lc_all if diff.get(slug(x["u"]), "M") != "H"]
                    if len(lc) < LC_PER_VARIANT:                                       # a variant must never be empty: fall back to a Hard one
                        lc += [x for x in lc_all if x not in lc][:LC_PER_VARIANT - len(lc)]
                    need_lc = max(LC_PER_VARIANT, target - len(chosen))
                    lcs = []
                    for x in lc:                                                       # ones already in the block first, so ticks carry over
                        if len(lcs) >= need_lc:
                            break
                        if slug(x["u"]) in by_slug and by_slug[slug(x["u"])] not in used:
                            lcs.append(x)
                    for x in lc:
                        if len(lcs) >= need_lc:
                            break
                        if x not in lcs and not (slug(x["u"]) in by_slug and by_slug[slug(x["u"])] in used):
                            lcs.append(x)
                    for x in lcs:
                        i = lc_item(x, v)
                        if i not in used:
                            flag(i, label, group)
                    for c in chosen:
                        i = other_item(c)
                        if i not in used:
                            flag(i, label, group)
                    # easier first inside the variant, so it reads as a ramp
                    group.sort(key=lambda i: ({"E": 0, "M": 1, "H": 2}.get(blk["items"][i].get("d"), 1)))
                    groups.append((label, group))

                if not keep:                                                           # variant-less blocks: their own problems, easier to harder
                    group = []
                    pool_b = [i for i, it in enumerate(blk["items"]) if it.get("d") in ("E", "M")]
                    if bid == "b12":
                        pool_b = [i for i in pool_b if re.search(r"stock|buy|sell|cooldown|fee", blk["items"][i]["t"], re.I)] or pool_b
                    pool_b.sort(key=lambda i: ({"E": 0, "M": 1}[blk["items"][i]["d"]], 0 if not blk["items"][i].get("x") else 1))
                    for i in pool_b[:6]:
                        flag(i, "core practice", group)
                    groups.append(("core practice", group))

                rank = 0
                for _, g in groups:
                    for idx in g:
                        blk["items"][idx]["to"] = rank
                        rank += 1
                if skip:
                    blk["thNote"] = "Left out of the threshold on purpose (rare, or very hard for a first pass): " + ", ".join(VNAME[v] for v in skip) + ". They are in the extra practice below."
                # The other platforms' problems (and library additions) belong in the threshold set only, never in the normal practice list.
                def removable(it):
                    return not it.get("th") and (it.get("x") == "other" or "(library" in it.get("t", ""))
                kept_ix = [i for i, it in enumerate(blk["items"]) if not removable(it)]
                remap[bid] = {old: new for new, old in enumerate(kept_ix)}
                blk["items"] = [blk["items"][i] for i in kept_ix]
                report.append((bid, blk["name"][:42], len(keep), rank, sum(1 for it in blk["items"] if it.get("th") and it.get("x") == "other"), len(blk["items"])))

    # tick marks are stored as "blockId:index", so when an item moves its tick must move with it
    pp = os.path.join(ROOT, "data", "progress.json")
    if os.path.exists(pp):
        kv = json.load(open(pp, encoding="utf-8"))
        raw = kv.get("oa-tracker-state-v3")
        stt = json.loads(raw) if isinstance(raw, str) and raw else None
        if stt:
            import shutil
            shutil.copy(pp, pp + ".bak")
            moved = lost = 0
            for field in ("s", "d"):
                new = {}
                for k, val in stt.get(field, {}).items():
                    bid, _, idx = k.rpartition(":")
                    m = remap.get(bid)
                    if m is None:
                        new[k] = val
                    elif int(idx) in m:
                        new["%s:%d" % (bid, m[int(idx)])] = val
                        moved += (m[int(idx)] != int(idx))
                    else:
                        lost += 1
                stt[field] = new
            stt["rev"] = int(stt.get("rev", 0)) + 1
            kv["oa-tracker-state-v3"] = json.dumps(stt, separators=(",", ":"))
            json.dump(kv, open(pp, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
            print("ticks carried to their new positions: %d moved, %d belonged to removed items" % (moved, lost // 2))
    for tr in plan["tracks"]:                                  # variant names are not shown on problems
        for ph in tr.get("phases", []):
            for blk in ph.get("blocks", []):
                for it in blk.get("items", []):
                    if it.get("x") != "other" and "  (" in it.get("t", ""):
                        it["t"] = it["t"].split("  (")[0]
    new_body = json.dumps(plan, ensure_ascii=False, indent=2)
    open(TRACKER, "w", encoding="utf-8", newline="\n").write(head + '<script type="application/json" id="plan">' + new_body + "</script>" + tail)
    print("block  name                                        variants  threshold  (from other platforms)  block total")
    for r in report:
        print("  %-4s %-42s %5d %9d %14d %17d" % r)
    print("threshold problems in total:", sum(r[3] for r in report), "| from other platforms:", sum(r[4] for r in report))


if __name__ == "__main__":
    main()
