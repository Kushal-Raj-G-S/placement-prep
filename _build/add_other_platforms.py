# -*- coding: utf-8 -*-
"""
Add problems from HackerRank, CodeChef, GeeksforGeeks and HackerEarth to the Twenty Weeks tracker.

    python _build/fetch_other.py            # once: pulls the real lists into .other_cache.json
    python _build/add_other_platforms.py    # adds them to the tracker (safe to re-run: it replaces its own earlier additions)

Rules
  - Medium and Hard first (what OAs actually ask), and one or two Easy ones per block as confidence builders.
  - Every problem comes from the platform's own API, so the link exists. A random sample is also fetched as a check.
  - Nothing already in a block is added twice. Existing items keep their position, so tick marks do not shift.
  - HackerEarth has no problem listing (its pages are rendered by JavaScript), so it gets its verified topic pages instead.
"""
import json, os, random, re, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TRACKER = os.path.join(ROOT, "1 - Twenty Weeks to AC (tracker).html")
CACHE = os.path.join(HERE, ".other_cache.json")

# ---------------------------------------------------------------------------------------------- block -> topic words
# Matching is on lower-case substrings of each source's own topic labels. DP is split by words in the problem name.
B = {
 "a1":  dict(cc=["hashmap", "maps", "sets", "frequency", "hashing"], gf=["hash", "map", "set"], hr=[], hrsub=[]),
 "a2":  dict(cc=["two pointers", "two-pointers"], gf=["two-pointer", "two pointer"], hr=[], hrsub=[]),
 "a3":  dict(cc=["sliding"], gf=["sliding"], hr=[], hrsub=[]),
 "a4":  dict(cc=["prefix"], gf=["prefix sum", "prefix-sum"], hr=[], hrsub=[]),
 "a5":  dict(cc=["sorting"], gf=["sorting", "interval"], hr=[], hrsub=["arrays-and-sorting"]),
 "a6":  dict(cc=["binary search", "binary-search"], gf=["binary search", "binary-search"], hr=[], hrsub=["search"]),
 "a7":  dict(cc=["stack"], gf=["stack", "monotonic"], hr=[], hrsub=[]),
 "a8":  dict(cc=["string"], gf=["string", "pattern searching"], hr=[], hrsub=["strings", "implementation"]),
 "b2":  dict(cc=["trees"], gf=["tree", "bst", "trie"], hr=[], hrsub=["trees", "balanced-trees"]),
 "n1":  dict(cc=[], gf=["linked list"], hr=[], hrsub=["linked-lists"]),
 "b5":  dict(cc=["bfs", "dfs", "graphs"], gf=["graph", "bfs", "dfs"], hr=[], hrsub=["graph-theory"]),
 "b3":  dict(cc=["heap", "priority"], gf=["heap", "priority"], hr=[], hrsub=["heap"]),
 "b4":  dict(cc=["greedy"], gf=["greedy"], hr=[], hrsub=["greedy"]),
 "n2":  dict(cc=["2d arrays"], gf=["matrix"], hr=[], hrsub=[]),
 "n3":  dict(cc=[], gf=["cyclic"], hr=[], hrsub=[]),
 "n4":  dict(cc=["design"], gf=["design", "lru"], hr=[], hrsub=[]),
 "b13": dict(cc=["bitwise", "bit manipulation", "bitmask", "number theory", "gcd", "modular", "sieve", "prime"], gf=["bit", "number-theory", "gcd", "prime", "modular"], hr=[], hrsub=["number-theory", "fundamentals"]),
 "b1":  dict(cc=["brute force", "permutations"], gf=["backtracking", "recursion", "permutation"], hr=[], hrsub=["recursion"]),
 "b6":  dict(cc=["disjoint", "shortest", "dijkstra", "topological", "minimum spanning"], gf=["topological", "dijkstra", "shortest", "union", "disjoint", "spanning"], hr=[], hrsub=["disjoint-set"]),
}
DP_BLOCKS = ["b7", "b8", "b9", "b10", "b11", "b12"]
DP_WORDS = {
 "b8":  ["knapsack", "subset", "partition", "coin", "change", "sum", "bag"],
 "b9":  ["grid", "path", "matrix", "maze", "robot", "chessboard", "route"],
 "b10": ["string", "subsequence", "palindrom", "edit", "common", "word", "substring", "child", "interleav"],
 "b12": ["stock", "buy", "sell", "profit", "cooldown", "state"],
 "b11": ["increasing", "envelope", "lis", "bitonic", "chain"],
}
GRAPH_HARD_WORDS = ["dijkstra", "shortest", "spanning", "topolog", "union", "disjoint", "cycle", "bellman", "floyd", "mst", "road", "cost"]
# pattern in links.json -> blocks, for the HackerEarth topic pages
HE_MAP = {"hashing": ["a1"], "two-pointers": ["a2"], "sliding-window": ["a3"], "prefix-sum": ["a4"], "intervals": ["a5"], "binary-search": ["a6"],
          "monotonic-stack": ["a7"], "tree-dfs": ["b2"], "tree-bfs": ["b2"], "trie": ["b2"], "linked-list": ["n1"], "grid": ["b5"], "heap": ["b3"],
          "greedy": ["b4"], "bits": ["b13"], "backtracking": ["b1"], "toposort": ["b6"], "shortest-path": ["b6"], "dsu": ["b6"],
          "dp-1d": ["b7", "b8"], "dp-2d": ["b9", "b10"]}


HE_TAG_BLOCK = {
 "a1": ["hash maps", "hash tables", "hashing algorithm", "maps", "sets", "multiset"], "a5": ["sorting", "merge sort", "quick sort"],
 "a6": ["binary search", "searching"], "a7": ["stacks", "queue"], "a8": ["string manipulation"],
 "b2": ["trees", "binary tree", "binary search tree", "tries"], "n1": ["linked list"],
 "b5": ["breadth first search", "depth first search", "graphs"], "n2": ["matrix", "2-d array"], "b3": ["heaps", "priority queue"],
 "b4": ["greedy algorithms"], "b13": ["bit manipulation", "number theory", "math"], "b1": ["backtracking", "recursion", "permutation and combination"],
 "b6": ["dijkstra's algorithm", "bellman ford algorithm", "floyd warshall algorithm", "kruskal's algorithm", "minimum spanning tree",
        "shortest path algorithm", "disjoint set", "disjoint data structures"],
}


def dp_block(name):
    n = name.lower()
    for blk, words in DP_WORDS.items():
        if any(w in n for w in words):
            return blk
    return "b7"


def graph_block(name):
    n = name.lower()
    return "b6" if any(w in n for w in GRAPH_HARD_WORDS) else "b5"


def has(hay, words):
    hay = hay.lower()
    return any(w in hay for w in words)


# ------------------------------------------------------------------------------------------------- source -> candidates
def candidates(cache):
    """{block: [candidate, ...]} with candidate = dict(src, name, url, d, pop, note, builder)."""
    out = {b: [] for b in list(B) + DP_BLOCKS}

    def add(blk, src, name, url, d, pop, note, builder=False):
        if blk in out:
            out[blk].append(dict(src=src, name=name, url=url, d=d, pop=pop, note=note, builder=builder))

    # HackerRank: the platform's own track/subdomain decides the block
    for x in cache["hr"]:
        if x["diff"] == "Expert":
            continue
        d = {"Easy": "E", "Medium": "M"}.get(x["diff"], "H")
        url = "https://www.hackerrank.com/challenges/%s/problem" % x["slug"]
        note = "%s, solved by %s" % (x["diff"], format(x["solved"], ","))
        sub, name = x["sub"], x["name"]
        if sub == "dynamic-programming":
            add(dp_block(name), "HackerRank", name, url, d, x["solved"], note)
        elif sub == "graph-theory":
            add(graph_block(name), "HackerRank", name, url, d, x["solved"], note)
        elif sub == "search" and has(name, ["grid", "cells", "connected", "region", "castle"]):
            add("b5", "HackerRank", name, url, d, x["solved"], note)
        elif sub == "queues" and has(name, ["castle", "grid", "bfs", "shortest"]):
            add("b5", "HackerRank", name, url, d, x["solved"], note)
        elif sub == "implementation" and has(name, ["matrix", "grid", "spiral", "queen", "board", "rotation", "layer"]):
            add("n2", "HackerRank", name, url, d, x["solved"], note)
        elif sub == "data-structures":
            nm = name.lower()
            blk = "b3" if has(nm, ["heap", "median", "priority"]) else "a7" if has(nm, ["stack", "bracket", "queue", "parenthes"]) else "b2" if has(nm, ["tree", "trie", "bst"]) else None
            if blk:
                add(blk, "HackerRank", name, url, d, x["solved"], note)
        else:
            for blk, cfg in B.items():
                if sub in cfg["hrsub"]:
                    add(blk, "HackerRank", name, url, d, x["solved"], note)
                    break

    # CodeChef: rating decides the difficulty, user_tags decide the block
    for x in cache["cc"]:
        r = x["rating"]
        if r >= 2300:
            continue
        d = "E" if r < 1300 else "M" if r < 1800 else "H"
        tags = " | ".join(x["tags"]).lower()
        url = "https://www.codechef.com/problems/%s" % x["code"]
        note = "rated %d, solved by %s" % (r, format(x["solved"], ","))
        placed = False
        if has(tags, ["dynamic programming", "dynamic-programming", "dp approach", "bottom-up"]):
            add(dp_block(x["name"]), "CodeChef", x["name"], url, d, x["solved"], note, builder=(d == "E")); placed = True
        else:
            for blk, cfg in B.items():
                if cfg["cc"] and has(tags, cfg["cc"]):
                    add(blk, "CodeChef", x["name"], url, d, x["solved"], note, builder=(d == "E")); placed = True
                    break

    # GeeksforGeeks: its own topic and difficulty labels
    for x in cache["gf"]:
        if x["diff"] not in ("Easy", "Medium", "Hard") or x["subs"] < 20000:
            continue
        d = {"Easy": "E", "Medium": "M", "Hard": "H"}[x["diff"]]
        tags = " | ".join(x["topics"]).lower()
        note = "%s, accuracy %s%%" % (x["diff"], int(x["acc"]))
        comp = (" - asked at " + ", ".join(x["companies"][:3])) if x["companies"] else ""
        if has(tags, ["dynamic programming", "dp"]):
            add(dp_block(x["name"]), "GeeksforGeeks", x["name"], x["url"], d, x["subs"], note + comp, builder=(d == "E")); continue
        if has(tags, ["backtracking"]) or has(x["name"], ["sudoku", "n-queen", "queens", "rat in a maze"]):
            add("b1", "GeeksforGeeks", x["name"], x["url"], d, x["subs"], note + comp, builder=(d == "E")); continue
        for blk, cfg in B.items():
            if not (cfg["gf"] and has(tags, cfg["gf"])):
                continue
            if blk in ("a6", "a1", "a5") and has(tags + " " + x["name"], ["tree", "bst", "linked list", "graph"]):
                continue                    # "binary search tree" is a tree problem; keep it out of the array blocks
            add(blk, "GeeksforGeeks", x["name"], x["url"], d, x["subs"], note + comp, builder=(d == "E"))
            break
    # HackerEarth: the tag it was listed under decides the block, its own easy/medium/hard decides the difficulty
    for x in cache.get("he", []):
        d = {"easy": "E", "medium": "M", "hard": "H"}.get(x["diff"])
        if not d:
            continue
        tags = set(x["tags"])
        note = "%s, %s%% success" % (x["diff"].capitalize(), int(x["rate"]))
        if tags & {"dynamic programming", "memoization"}:
            add(dp_block(x["name"]), "HackerEarth", x["name"], x["url"], d, x["attempted"], note, builder=(d == "E")); continue
        for blk, words in HE_TAG_BLOCK.items():
            if tags & set(words):
                add(blk, "HackerEarth", x["name"], x["url"], d, x["attempted"], note, builder=(d == "E"))
                break
    return out


def choose(cands, have_urls):
    """Per block: Medium/Hard first by popularity, spread over the sources, plus one Easy per source as a confidence builder."""
    quota = {"HackerRank": (3, 1), "HackerEarth": (3, 1), "GeeksforGeeks": (4, 1), "CodeChef": (3, 1)}      # (medium-hard, easy)
    picked = []
    for src, (nmh, ne) in quota.items():
        mine = [c for c in cands if c["src"] == src and c["url"] not in have_urls]
        mh = sorted([c for c in mine if c["d"] in ("M", "H")], key=lambda c: -c["pop"])
        # keep one Hard in the mix when there is one, since the Medium ones are the most popular by far
        hard = [c for c in mh if c["d"] == "H"][:1]
        med = [c for c in mh if c["d"] == "M"][:max(0, nmh - len(hard))]
        easy = sorted([c for c in mine if c["d"] == "E"], key=lambda c: -c["pop"])[:ne]
        picked += med + hard + easy
    order = {"M": 0, "H": 1, "E": 2}
    return sorted(picked, key=lambda c: (order[c["d"]], c["src"]))


def check_sample(items, n=24):
    """Fetch a random sample of the chosen links. HackerRank/CodeChef answer 404 for a missing page."""
    bad = []
    pool = [i for i in items if i["src"] in ("HackerRank", "CodeChef", "HackerEarth")]
    for it in random.sample(pool, min(n, len(pool))):
        try:
            req = urllib.request.Request(it["url"], headers={"User-Agent": "Mozilla/5.0"})
            code = urllib.request.urlopen(req, timeout=25).status
        except Exception as e:
            code = getattr(e, "code", 0)
        if code != 200:
            bad.append((it["url"], code))
    return len(pool) and min(n, len(pool)), bad


def main():
    cache = json.load(open(CACHE, encoding="utf-8"))
    links = json.load(open(os.path.join(HERE, "links.json"), encoding="utf-8"))
    html = open(TRACKER, encoding="utf-8").read()
    head, rest = html.split('<script type="application/json" id="plan">', 1)
    body, tail = rest.split("</script>", 1)
    plan = json.loads(body)

    cands = candidates(cache)
    he = {}
    for pat, blks in HE_MAP.items():
        for h in links["patterns"].get(pat, {}).get("hubs", []):
            if h["p"] == "HackerEarth":
                for b in blks:
                    he.setdefault(b, (pat, h["u"]))

    total = {"HackerRank": 0, "CodeChef": 0, "GeeksforGeeks": 0, "HackerEarth": 0, "HackerEarth topic pages": 0}
    levels = {"E": 0, "M": 0, "H": 0}
    report, allpicked = [], []
    for tr in plan["tracks"]:
        if tr["id"] != "td":
            continue
        for ph in tr["phases"]:
            for blk in ph["blocks"]:
                bid = blk["id"]
                blk["items"] = [i for i in blk["items"] if i.get("x") != "other"]        # drop my earlier additions, keep yours
                have = {i["u"] for i in blk["items"]}
                picked = choose(cands.get(bid, []), have) if bid in cands else []
                for c in picked:
                    label = "builder" if c["d"] == "E" else {"M": "medium", "H": "hard"}[c["d"]]
                    title = "%s: %s  (%s)" % (c["src"], c["name"], c["note"])
                    if c["d"] == "E":
                        title += " - confidence builder"
                    blk["items"].append({"t": title, "u": c["url"], "d": c["d"], "x": "other"})
                    total[c["src"]] += 1
                    levels[c["d"]] += 1
                    allpicked.append(c)
                if bid in he:
                    pat, url = he[bid]
                    blk["items"].append({"t": "HackerEarth: browse the %s practice problems and filter to Medium / Hard (verified topic page)" % pat.replace("-", " "),
                                         "u": url, "d": "", "x": "other"})
                    total["HackerEarth topic pages"] += 1
                report.append((bid, blk["name"][:46], sum(1 for c in picked)))

    n, bad = check_sample(allpicked)
    new_body = json.dumps(plan, ensure_ascii=False, indent=2)
    if "</script" in new_body.lower():
        sys.exit("a title contains </script>")
    open(TRACKER, "w", encoding="utf-8", newline="\n").write(head + '<script type="application/json" id="plan">' + new_body + "</script>" + tail)

    print("added per source:", total, "| by difficulty:", levels)
    for r in report:
        print("  %-4s %-46s +%d" % r)
    print("sampled %d HackerRank/CodeChef links, %d not 200: %s" % (n, len(bad), bad[:5]))


if __name__ == "__main__":
    main()
