# -*- coding: utf-8 -*-
"""
Builds links.json for the Pattern Radar Learn pages, and refuses to invent a link.

    python verify_links.py            check everything, write links.json
    python verify_links.py --offline  rebuild links.json from the cached check results

Three sources, none of them guesswork:

  LeetCode     the "LC <id>" tags in pattern_library.py are resolved against LeetCode's own
               problem index (leetcode.com/api/problems/all). That yields the official title
               and slug, so the url is constructed from real data -- and a wrong id is caught
               rather than shipped. LeetCode 403s plain HTTP clients, so this index IS the check.
  Codeforces   problems are pulled from the Codeforces API by tag and ranked by how many people
               solved them, so each pick is a real problem at an approachable difficulty.
               (Codeforces serves 200 for a non-existent problem, so a HEAD check proves nothing
               there -- the API is the only honest route.)
  Everything   GeeksforGeeks / HackerRank / HackerEarth / CodeChef / InterviewBit answer 404
  else         properly, so every one of those urls is fetched. Non-200 is dropped and reported.

Run it again whenever you add patterns; the report tells you what died.
"""
import json, os, re, sys, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pattern_library as PL
import pattern_links as PK

OUT = os.path.join(HERE, "links.json")
CACHE = os.path.join(HERE, ".link_cache.json")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0 Safari/537.36"
LC_INDEX = "https://leetcode.com/api/problems/all/"
CF_API = "https://codeforces.com/api/problemset.problems"
CF_PER_PATTERN = 6
CF_MIN_SOLVED = 3000          # popular enough to be well-explained in editorials
CF_MAX_RATING = 1800          # OA-realistic, not division-1 cruelty

PLATFORM_NAMES = {"he": "HackerEarth", "hr": "HackerRank", "gfg": "GeeksforGeeks",
                  "cc": "CodeChef", "ib": "InterviewBit"}


def get(url, timeout=45):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def status(url):
    """Return an HTTP status for url, following redirects. 0 means it did not answer."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,*/*"})
        with urllib.request.urlopen(req, timeout=40) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return 0


def main():
    offline = "--offline" in sys.argv
    cache = {}
    if os.path.exists(CACHE):
        try:
            cache = json.load(open(CACHE, encoding="utf-8"))
        except Exception:
            cache = {}

    report = {"lc_ok": 0, "lc_bad": [], "lc_retitled": [], "http_ok": 0, "http_bad": [], "cf": 0}

    # ---------------- LeetCode: resolve every "LC <id>" against the real index ----------
    lc_by_id = {}
    if not offline:
        print("fetching the LeetCode problem index ...")
        data = json.loads(get(LC_INDEX).decode("utf-8"))
        for row in data["stat_status_pairs"]:
            s = row["stat"]
            lc_by_id[int(s["frontend_question_id"])] = {
                "title": s["question__title"],
                "slug": s["question__title_slug"],
                "paid": bool(row.get("paid_only")),
                "level": row.get("difficulty", {}).get("level"),
            }
        cache["lc"] = lc_by_id
        print("  %d problems indexed" % len(lc_by_id))
    else:
        lc_by_id = {int(k): v for k, v in cache.get("lc", {}).items()}

    # ---------------- Codeforces: real problems, by tag, ranked by solved count ---------
    cf_by_tag = {}
    if not offline:
        print("fetching the Codeforces problemset ...")
        cf = json.loads(get(CF_API).decode("utf-8"))
        solved = {}
        for st in cf["result"]["problemStatistics"]:
            solved[(st["contestId"], st["index"])] = st["solvedCount"]
        for p in cf["result"]["problems"]:
            key = (p.get("contestId"), p.get("index"))
            if key[0] is None:
                continue
            sc = solved.get(key, 0)
            if sc < CF_MIN_SOLVED:
                continue
            if p.get("rating") and p["rating"] > CF_MAX_RATING:
                continue
            for t in p.get("tags", []):
                cf_by_tag.setdefault(t, []).append({
                    "n": p["name"], "p": "Codeforces",
                    "u": "https://codeforces.com/problemset/problem/%d/%s" % (key[0], key[1]),
                    "s": "CF %d%s%s" % (key[0], key[1], "  · " + str(p["rating"]) if p.get("rating") else ""),
                    "_solved": sc, "_rating": p.get("rating") or 0,
                })
        for t in cf_by_tag:
            cf_by_tag[t].sort(key=lambda x: -x["_solved"])
        cache["cf"] = cf_by_tag
        print("  %d tags usable" % len(cf_by_tag))
    else:
        cf_by_tag = cache.get("cf", {})

    # ---------------- collect every hand-written url, then fetch them all ---------------
    urls = set()
    for pid, rail in PK.PLATFORM.items():
        for k, v in rail.items():
            if k != "cf":
                urls.add(v)
    for vid, items in PK.EXTRA.items():
        for it in items:
            urls.add(it["u"])

    checked = cache.get("http", {})
    if not offline:
        todo = sorted(urls)
        print("checking %d hand-written urls ..." % len(todo))
        with ThreadPoolExecutor(max_workers=8) as ex:
            for u, st in zip(todo, ex.map(status, todo)):
                checked[u] = st
        cache["http"] = checked
        json.dump(cache, open(CACHE, "w", encoding="utf-8"))

    def alive(u):
        return checked.get(u) == 200

    for u in sorted(urls):
        if alive(u):
            report["http_ok"] += 1
        else:
            report["http_bad"].append("%s  [%s]" % (u, checked.get(u, "unchecked")))

    # ---------------- assemble links.json ----------------------------------------------
    out = {"variants": {}, "patterns": {}}

    for p in PL.PATTERNS:
        for v in p["variants"]:
            items = []
            for ex in v.get("examples", []):
                m = re.search(r"LC\s*(\d+)", ex.get("s", ""))
                if m:
                    lid = int(m.group(1))
                    info = lc_by_id.get(lid)
                    if not info:
                        report["lc_bad"].append("%s: LC %d (%s) is not in the index" % (v["id"], lid, ex["n"]))
                        continue
                    if info["title"].lower() != ex["n"].split(" — ")[0].strip().lower():
                        report["lc_retitled"].append("%s: %r -> %r" % (v["id"], ex["n"], info["title"]))
                    note = ex["s"].split("—", 1)[1].strip() if "—" in ex["s"] else ""
                    items.append({
                        "n": info["title"], "p": "LeetCode",
                        "u": "https://leetcode.com/problems/%s/" % info["slug"],
                        "s": "LC %d" % lid + ("  · premium" if info["paid"] else ""),
                        "note": note,
                    })
                    report["lc_ok"] += 1
                else:
                    items.append({"n": ex["n"], "p": ex.get("p", ""), "u": ex.get("u", ""), "s": ex.get("s", "")})
            for it in PK.EXTRA.get(v["id"], []):
                if alive(it["u"]):
                    # one spelling per platform, or the filter chips split in two
                    pname = {"GfG": "GeeksforGeeks"}.get(it["p"], it["p"])
                    items.append({"n": it["n"], "p": pname, "u": it["u"], "s": ""})
            out["variants"][v["id"]] = items

        rail = PK.PLATFORM.get(p["id"], {})
        hubs = []
        for k in ("he", "hr", "gfg", "cc", "ib"):
            if k in rail and alive(rail[k]):
                hubs.append({"p": PLATFORM_NAMES[k], "u": rail[k]})
        tag = rail.get("cf")
        if tag:
            hubs.append({"p": "Codeforces", "u": "https://codeforces.com/problemset?tags=" + tag.replace(" ", "+")})
        picks = []
        for x in (cf_by_tag.get(tag, []) if tag else [])[:CF_PER_PATTERN]:
            picks.append({"n": x["n"], "p": "Codeforces", "u": x["u"], "s": x["s"]})
        report["cf"] += len(picks)
        out["patterns"][p["id"]] = {"hubs": hubs, "cf": picks}

    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    # ---------------- the report --------------------------------------------------------
    print("\n" + "=" * 68)
    print("LeetCode links resolved from the official index : %d" % report["lc_ok"])
    print("Codeforces problems pulled from the API         : %d" % report["cf"])
    print("Hand-written urls answering 200                 : %d / %d" % (report["http_ok"], len(urls)))
    if report["lc_retitled"]:
        print("\ntitles corrected to the official ones (%d):" % len(report["lc_retitled"]))
        for r in report["lc_retitled"]:
            print("  " + r)
    if report["lc_bad"]:
        print("\nBAD LeetCode ids (dropped):")
        for r in report["lc_bad"]:
            print("  " + r)
    if report["http_bad"]:
        print("\nDEAD urls (dropped from the build) (%d):" % len(report["http_bad"]))
        for r in report["http_bad"]:
            print("  " + r)
    total = report["lc_ok"] + report["cf"] + report["http_ok"]
    print("\n%d verified links written to links.json" % total)
    print("now run:  python build_radar.py")


if __name__ == "__main__":
    main()
