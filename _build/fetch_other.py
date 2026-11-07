# -*- coding: utf-8 -*-
"""
Fetch REAL problem lists (with difficulty and popularity) from HackerRank and CodeChef into .other_cache.json.
Nothing here is guessed: every problem comes from the platform's own API, so every link exists.

    python _build/fetch_other.py

HackerRank  rest/contests/master/tracks/<track>/challenges   -> slug, name, difficulty, solved_count, success_ratio, track/topic
CodeChef    api/list/problems/<easy|medium|hard>              -> code, name, difficulty_rating, successful_submissions
            api/contests/PRACTICE/problems/<code>             -> user_tags (the topics)
HackerEarth and GeeksforGeeks do not expose a listing (HackerEarth renders it with JavaScript, GfG answers 200 to any
slug), so those come from the already-verified links.json instead.
"""
import json, os, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, ".other_cache.json")


def get(url, tries=3, timeout=40):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode("utf-8", "replace"))
        except Exception:
            time.sleep(1.5 * (i + 1))
    return None


def hackerrank():
    out = []
    for track in ("algorithms", "data-structures", "mathematics"):
        off = 0
        while True:
            d = get("https://www.hackerrank.com/rest/contests/master/tracks/%s/challenges?offset=%d&limit=100" % (track, off))
            if not d or not d.get("models"):
                break
            for m in d["models"]:
                out.append({"slug": m["slug"], "name": m["name"], "diff": m.get("difficulty_name"), "solved": m.get("solved_count", 0),
                            "ratio": round(m.get("success_ratio") or 0, 3), "track": track,
                            "sub": (m.get("track") or {}).get("slug"), "subname": (m.get("track") or {}).get("name"),
                            "topics": m.get("tag_names") or []})
            off += 100
            if off >= d.get("total", 0):
                break
    return out


def codechef():
    """The level in the URL is ignored by CodeChef, so page through everything, most-solved first, and keep the problems
    that are actually rated medium or hard (1300+) and that real people have solved."""
    def page(n):
        d = get("https://www.codechef.com/api/list/problems/easy?limit=50&page=%d&sort_by=successful_submissions&sort_order=desc" % n, tries=2)
        return (d or {}).get("data") or []
    rows = {}
    with ThreadPoolExecutor(8) as ex:
        for plist in ex.map(page, range(0, 140)):
            for p in plist:
                r = int(p.get("difficulty_rating") or -1)
                s = int(p.get("successful_submissions") or 0)
                if r >= 1300 and r < 9000 and s >= 150:
                    rows[p["code"]] = {"code": p["code"], "name": p["name"], "rating": r, "solved": s}
    # a little confidence-builder band too (rated 800-1100, very widely solved)
    with ThreadPoolExecutor(8) as ex:
        for plist in ex.map(page, range(0, 40)):
            for p in plist:
                r = int(p.get("difficulty_rating") or -1)
                s = int(p.get("successful_submissions") or 0)
                if 800 <= r <= 1100 and s >= 5000 and len([1 for x in rows.values() if x["rating"] < 1300]) < 120:
                    rows[p["code"]] = {"code": p["code"], "name": p["name"], "rating": r, "solved": s}

    def tags(code):
        j = get("https://www.codechef.com/api/contests/PRACTICE/problems/" + code, tries=2)
        return code, (j or {}).get("user_tags") or [], (j or {}).get("problem_name")
    with ThreadPoolExecutor(8) as ex:
        for code, tg, nm in ex.map(tags, list(rows)):
            rows[code]["tags"] = tg
            if nm:
                rows[code]["name"] = nm
    return list(rows.values())


def gfg():
    """GeeksforGeeks practice problems from its own API (problem_url is the real page)."""
    out, seen = [], set()
    def page(n):
        d = get("https://practiceapi.geeksforgeeks.org/api/latest/problems/?page=%d&pageMode=explore" % n, tries=2)
        return (d or {}).get("results") or []
    with ThreadPoolExecutor(6) as ex:
        for plist in ex.map(page, range(1, 161)):
            for p in plist:
                if p["slug"] in seen:
                    continue
                seen.add(p["slug"])
                tg = p.get("tags") or {}
                try:
                    acc = float(str(p.get("accuracy", "0")).strip("%"))
                except Exception:
                    acc = 0.0
                out.append({"name": p["problem_name"], "url": p["problem_url"], "diff": p.get("difficulty"), "subs": p.get("all_submissions", 0),
                            "acc": acc, "topics": tg.get("topic_tags") or [], "companies": tg.get("company_tags") or []})
    return out


HE_TAGS = ["hash maps", "hash tables", "hashing algorithm", "maps", "sets", "multiset", "sorting", "merge sort", "quick sort", "binary search", "searching",
           "stacks", "queue", "string manipulation", "trees", "binary tree", "binary search tree", "tries", "linked list", "breadth first search",
           "depth first search", "graphs", "matrix", "2-d array", "heaps", "priority queue", "greedy algorithms", "bit manipulation", "number theory",
           "math", "backtracking", "recursion", "permutation and combination", "dijkstra's algorithm", "bellman ford algorithm",
           "floyd warshall algorithm", "kruskal's algorithm", "minimum spanning tree", "shortest path algorithm", "disjoint set", "disjoint data structures",
           "dynamic programming", "memoization", "arrays", "1-d array"]


def hackerearth():
    """HackerEarth practice problems from the site's own API, one tag at a time (10 per page). Difficulty is easy/medium/hard."""
    import urllib.parse
    rows = {}
    def one(tag):
        got = []
        for pg in range(1, 13):                          # up to 120 per tag
            d = get("https://www.hackerearth.com/api/practice/problems/?tag=%s&page=%d" % (urllib.parse.quote(tag), pg), tries=2)
            plist = ((d or {}).get("problems") or {}).get("algorithm") or []
            if not plist:
                break
            got += plist
        return tag, got
    with ThreadPoolExecutor(6) as ex:
        for tag, plist in ex.map(one, HE_TAGS):
            for p in plist:
                u = "https://www.hackerearth.com" + p["url"]
                r = rows.setdefault(u, {"name": p["title"], "url": u, "diff": p.get("difficulty"), "rate": p.get("success_rate", 0),
                                        "attempted": p.get("attempted_by", 0), "tags": []})
                r["tags"].append(tag)
    return list(rows.values())


if __name__ == "__main__":
    t = time.time()
    if len(sys.argv) > 1 and sys.argv[1] == "he":
        c = json.load(open(OUT, encoding="utf-8")); c["he"] = hackerearth()
        json.dump(c, open(OUT, "w", encoding="utf-8"), ensure_ascii=False)
        print("HackerEarth: %d problems (%s) in %.0fs" % (len(c["he"]), ", ".join("%s %d" % (k, sum(1 for x in c["he"] if x["diff"] == k)) for k in ("easy", "medium", "hard")), time.time() - t)); sys.exit(0)
    hr = hackerrank()
    print("HackerRank: %d challenges (%s)" % (len(hr), ", ".join("%s %d" % (k, sum(1 for x in hr if x["diff"] == k)) for k in ("Easy", "Medium", "Hard", "Advanced", "Expert"))))
    cc = codechef()
    print("CodeChef:   %d problems with tags" % len(cc))
    gf = gfg()
    print("GfG:        %d problems (%s)" % (len(gf), ", ".join("%s %d" % (k, sum(1 for x in gf if x["diff"] == k)) for k in ("Basic", "Easy", "Medium", "Hard"))))
    he = hackerearth()
    print("HackerEarth: %d problems" % len(he))
    json.dump({"hr": hr, "cc": cc, "gf": gf, "he": he, "when": time.strftime("%Y-%m-%d")}, open(OUT, "w", encoding="utf-8"), ensure_ascii=False)
    print("saved in %.0fs -> %s" % (time.time() - t, OUT))
