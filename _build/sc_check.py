# -*- coding: utf-8 -*-
"""
Validates the scenario questions (sc_*.py). The questions are stories only: no samples, no tests, no judge.
What CAN go wrong without tests is a mislabelled or leaky question, so this guards exactly that:

  - every id is unique and the variant exists
  - every clue phrase and decoy phrase is a VERBATIM substring of the story (the page highlights them)
  - the story does not contain a technique word that names the pattern (it would answer the question)
  - length, vocabulary and domain are sane, and no two stories share a long run of words
  - the glossary words really appear in the story, and every 'why' names a real variant

Run directly for a report:  python sc_check.py
"""
import importlib, glob, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pattern_library as PL

VARIANTS = {v["id"]: p["id"] for p in PL.PATTERNS for v in p["variants"]}

# Words that would hand over the pattern. Natural English words that merely sound technical
# (set, window, range, stack of crates) are handled with the narrower phrases below, not banned outright.
BANNED = [
    "sliding window", "two pointer", "prefix sum", "binary search", "hash map", "hashmap", "hash set", "hashing",
    "priority queue", "min-heap", "max-heap", "heap", "monotonic", "union-find", "union find", "disjoint set",
    "dijkstra", "bellman", "floyd", "kruskal", "topological", "bfs", "dfs", "breadth-first", "depth-first",
    "dynamic programming", "memoiz", "knapsack", "backtrack", "greedy", "trie", "prefix tree", "xor", "bitmask",
    "bit mask", "kadane", "subarray", "substring", "algorithm", "data structure", "time complexity", "o(n",
    "stack", "queue", "deque", "recursion", "recursive", "pointer",
]

REQUIRED = ("id", "v", "dom", "diff", "title", "story", "clues", "decoys", "core", "gloss", "why", "tell")


def load():
    qs = []
    for path in sorted(glob.glob(os.path.join(HERE, "sc_[0-9]*.py"))):
        mod = importlib.import_module(os.path.basename(path)[:-3])
        for q in mod.QUESTIONS:
            q["_file"] = os.path.basename(path)
            qs.append(q)
    return qs


def words(s):
    return re.findall(r"[a-z0-9']+", s.lower())


def check(qs):
    errs, warns = [], []
    seen_id, seen_title = {}, {}
    grams = {}
    for q in qs:
        qid = q.get("id", "?")
        where = "%s (%s)" % (qid, q.get("_file", "?"))
        for k in REQUIRED:
            if k not in q or q[k] in (None, "", []):
                if k == "decoys":                      # a question with no decoy is allowed
                    q.setdefault("decoys", [])
                    continue
                errs.append("%s: missing field '%s'" % (where, k))
        if q.get("id") in seen_id:
            errs.append("%s: duplicate id (also in %s)" % (where, seen_id[q["id"]]))
        seen_id[q.get("id")] = q.get("_file")
        if q.get("v") not in VARIANTS:
            errs.append("%s: unknown variant %r" % (where, q.get("v")))
        for a in q.get("alt", []):
            if a not in VARIANTS:
                errs.append("%s: unknown alt variant %r" % (where, a))
        for w in q.get("why", {}):
            if w not in VARIANTS:
                errs.append("%s: 'why' names unknown variant %r" % (where, w))
        if q.get("v") in q.get("why", {}):
            errs.append("%s: 'why' explains the CORRECT variant as wrong" % where)
        story = q.get("story", "")
        if q.get("title") in seen_title:
            errs.append("%s: duplicate title %r" % (where, q["title"]))
        seen_title[q.get("title")] = qid
        for ph in q.get("clues", []):
            if ph not in story:
                errs.append("%s: clue is not verbatim in the story: %r" % (where, ph))
        for ph in q.get("decoys", []):
            if ph not in story:
                errs.append("%s: decoy is not verbatim in the story: %r" % (where, ph))
        if len(q.get("clues", [])) < 2:
            errs.append("%s: needs at least 2 clues" % where)
        low = story.lower() + " " + q.get("title", "").lower()
        for b in BANNED:
            if re.search(r"(?<![a-z])" + re.escape(b), low):
                errs.append("%s: story/title contains the giveaway word %r" % (where, b))
        n = len(words(story))
        if n < 300:
            errs.append("%s: story is %d words; every scenario must be OA-size (300 minimum, ~400 is the target)"
                        % (where, n))
        if n > 520:
            warns.append("%s: story is %d words (very long)" % (where, n))
        for g in q.get("gloss", []):
            if len(g) != 3:
                errs.append("%s: gloss entries are (word, meaning, safe_to_define)" % where)
            elif g[0].lower() not in story.lower():
                errs.append("%s: glossary word %r is not in the story" % (where, g[0]))
        ws = words(" ".join(p for p in story.split(chr(10)) if not re.match(r"\s*(input|output|constraints)", p, re.I)))
        for i in range(len(ws) - 7):
            gram = " ".join(ws[i:i + 8])
            if "up to" in gram and sum(1 for w in ws[i:i + 8] if w.isdigit()) >= 2:
                continue                      # repeated bounds like "(N up to 10^5, times up to 10^9)" are not copying
            if gram in grams and grams[gram] != qid:
                warns.append("%s: shares an 8-word run with %s: %r" % (where, grams[gram], gram))
                break
            grams[gram] = qid
    return errs, warns


def main():
    qs = load()
    errs, warns = check(qs)
    per_variant = {}
    for q in qs:
        per_variant[q.get("v")] = per_variant.get(q.get("v"), 0) + 1
    doms = {}
    for q in qs:
        doms[q.get("dom")] = doms.get(q.get("dom"), 0) + 1
    print("%d questions, %d variants covered of %d, %d domains" % (len(qs), len(per_variant), len(VARIANTS), len(doms)))
    missing = [v for v in VARIANTS if v not in per_variant]
    if missing and "--quiet" not in sys.argv:
        print("variants with no question yet (%d): %s" % (len(missing), " ".join(missing)))
    for w in warns[:15]:
        print("  warn:", w)
    for e in errs[:40]:
        print("  ERROR:", e)
    if len(errs) > 40:
        print("  ... and %d more errors" % (len(errs) - 40))
    print("%d errors, %d warnings" % (len(errs), len(warns)))
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
