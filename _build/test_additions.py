# -*- coding: utf-8 -*-
"""Runs every template added in lib_additions.py on known answers.   python test_additions.py"""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.setrecursionlimit(5000)
import lib_additions as A


class ListNode:
    def __init__(self, val=0, next=None):
        self.val, self.next, self.random = val, next, None
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right
class Node:
    def __init__(self, val=0):
        self.val, self.next, self.random = val, None, None


def ll(a):
    d = ListNode()
    c = d
    for x in a:
        c.next = ListNode(x); c = c.next
    return d.next
def arr(h):
    o = []
    while h:
        o.append(h.val); h = h.next
    return o
def tree(a):                                # level order with None
    if not a:
        return None
    ns = [TreeNode(x) if x is not None else None for x in a]
    kids = ns[1:][::-1]
    for n in ns:
        if n:
            if kids: n.left = kids.pop()
            if kids: n.right = kids.pop()
    return ns[0]


CODE = {}
for vs, _, _ in A.ADD.values():
    for v in vs:
        CODE[v["id"]] = v["code"]
for p in A.NEW:
    for v in p["variants"]:
        CODE[v["id"]] = v["code"]


def ns(vid):
    g = {"ListNode": ListNode, "TreeNode": TreeNode, "Node": Node}
    exec(CODE[vid], g)
    return g


fails = []
tested = set()
def t(vid, got, want):
    tested.add(vid)
    if got != want:
        fails.append("%s: got %r, want %r" % (vid, got, want))


t("ll-gap", arr(ns("ll-gap")["remove_nth_from_end"](ll([1,2,3,4,5]), 2)), [1,2,3,5])
t("ll-gap", arr(ns("ll-gap")["remove_nth_from_end"](ll([1]), 1)), [])
h = ll([1,2,3]); h.random = h.next.next
c = ns("ll-hash")["copy_random_list"](h); t("ll-hash", (arr(c), c.random.val, c is not h), ([1,2,3], 3, True))
t("tp-centre", ns("tp-centre")["longest_palindrome"]("cbbd"), "bb")
t("tp-centre", len(ns("tp-centre")["longest_palindrome"]("babad")), 3)
t("sw-complement", ns("sw-complement")["max_points_from_ends"]([1,2,3,4,5,6,1], 3), 12)
t("sw-complement", ns("sw-complement")["max_points_from_ends"]([9,7,7,9,7,7,9], 7), 55)
t("hs-moore", ns("hs-moore")["majority"]([2,2,1,1,1,2,2]), 2)
t("hs-moore", ns("hs-moore")["majority"]([1,2,3]), None)
t("ms-contrib", ns("ms-contrib")["sum_subarray_mins"]([3,1,2,4]), 17)
t("ms-contrib", ns("ms-contrib")["sum_subarray_mins"]([11,81,94,43,3]), 444)
t("hp-sorted", ns("hp-sorted")["contains_near"]([1,2,3,1], 3, 0), True)
t("hp-sorted", ns("hp-sorted")["contains_near"]([1,5,9,1,5,9], 2, 3), False)
t("bt-perbit", ns("bt-perbit")["total_hamming"]([4,14,2]), 6)
t("sim-rules", ns("sim-rules")["zigzag"]("PAYPALISHIRING", 3), "PAHNAPLSIIGYIR")
t("td-global", ns("td-global")["diameter"](tree([1,2,3,4,5])), 3)
t("td-state", ns("td-state")["rob"](tree([3,2,3,None,3,None,1])), 7)
r = ns("td-build")["build"]([3,9,20,15,7], [9,3,15,20,7]); t("td-build", (r.val, r.left.val, r.right.val, r.right.left.val), (3,9,20,15))
root = tree([3,5,1,6,2,0,8,None,None,7,4])
t("td-parent", sorted(ns("td-parent")["distance_k"](root, root.left, 2)), [1,4,7])
t("td-reroot", ns("td-reroot")["sum_of_distances"](6, [[0,1],[0,2],[2,3],[2,4],[2,5]]), [8,12,6,10,10,10])
an = ns("td-lift")["Ancestor"](7, [-1,0,0,1,1,2,2]); t("td-lift", (an.kth(3,1), an.kth(5,2), an.kth(6,3)), (1,0,-1))
t("tb-index", ns("tb-index")["max_width"](tree([1,3,2,5,3,None,9])), 4)
t("tr-xor", ns("tr-xor")["max_xor"]([3,10,5,25,2,8]), 28)
b = [list(x) for x in ["XXXX","XOOX","XXOX","XOXX"]]
t("gr-border", ["".join(x) for x in ns("gr-border")["solve_surrounded"](b)], ["XXXX","XXXX","XXXX","XOXX"])
t("sp-01bfs", ns("sp-01bfs")["min_cost_grid"]([[0,1,1],[1,1,0],[1,1,0]]), 2)
t("sp-mod", ns("sp-mod")["min_effort"]([[1,2,2],[3,8,2],[5,3,5]]), 2)
t("dsu-prim", ns("dsu-prim")["min_cost_connect_points"]([[0,0],[2,2],[3,10],[5,2],[7,0]]), 20)
t("dp-state", ns("dp-state")["max_profit_cooldown"]([1,2,3,0,2]), 3)
t("dp-partition", ns("dp-partition")["word_break"]("leetcode", ["leet","code"]), True)
t("dp-partition", ns("dp-partition")["word_break"]("catsandog", ["cats","dog","sand","and","cat"]), False)
t("dp-digit", ns("dp-digit")["count_without_digit_4"](50), sum("4" not in str(i) for i in range(51)))
t("dp-digit", ns("dp-digit")["count_without_digit_4"](1000), sum("4" not in str(i) for i in range(1001)))
t("bk-partition", sorted(ns("bk-partition")["palindrome_partitions"]("aab")), [["a","a","b"],["aa","b"]])
t("bk-build", ns("bk-build")["generate_parens"](3), ["((()))","(()())","(())()","()(())","()()()"])
t("bk-bucket", ns("bk-bucket")["can_partition_k"]([4,3,2,3,5,2,1], 4), True)
t("bk-bucket", ns("bk-bucket")["can_partition_k"]([1,2,3,4], 3), False)
t("gr-twopass", ns("gr-twopass")["candy"]([1,0,2]), 5)
t("gr-balance", ns("gr-balance")["can_complete_circuit"]([1,2,3,4,5],[3,4,5,1,2]), 3)
t("dc-mergecount", ns("dc-mergecount")["count_inversions"]([2,4,1,3,5]), 3)
for _ in range(200):
    a = [random.randint(0, 20) for _ in range(random.randint(0, 30))]
    w = sum(a[i] > a[j] for i in range(len(a)) for j in range(i+1, len(a)))
    t("dc-mergecount", ns("dc-mergecount")["count_inversions"](a[:]), w)
    if a:
        k = random.randint(1, len(a))
        t("dc-quickselect", ns("dc-quickselect")["kth_largest"](a[:], k), sorted(a)[-k])
t("dc-bucket", sorted(ns("dc-bucket")["top_k_frequent"]([1,1,1,2,2,3], 2)), [1,2])
t("dc-split", sorted(ns("dc-split")["diff_ways"]("2-1-1")), [0,2])
g = ns("ma-gcd"); t("ma-gcd", (g["gcd"](12,18), g["lcm"](4,6)), (6,12))
g = ns("ma-sieve"); t("ma-sieve", (g["sieve"](20), g["sieve"](1), g["factorise"](360), g["factorise"](97)), ([2,3,5,7,11,13,17,19], [], {2:3,3:2,5:1}, {97:1}))
g = ns("ma-modpow"); t("ma-modpow", (g["power"](2,10), g["power"](3,10**18)==pow(3,10**18,g["MOD"]), g["inverse"](2)*2%g["MOD"]), (1024,True,1))
c = ns("ma-ncr")["build"](100); t("ma-ncr", (c(5,2), c(10,0), c(3,5), c(100,50)), (10,1,0,__import__('math').comb(100,50)%(10**9+7)))
t("ma-digits", (ns("ma-digits")["add_strings"]("999","1"), ns("ma-digits")["add_strings"]("0","0")[-1]), ("1000","0"))
g = ns("ma-game"); t("ma-game", (g["nim_game"](4), g["nim_game"](5), g["bulbs_on"](10)), (False,True,3))
g = ns("ma-geom"); t("ma-geom", (g["rect_overlap"]((0,0,2,2),(1,1,3,3)), g["rect_overlap"]((0,0,1,1),(1,0,2,1)), g["cross"]((0,0),(1,0),(0,1))>0), (True,False,True))
c = ns("ds-lru")["LRUCache"](2); c.put(1,1); c.put(2,2); a=c.get(1); c.put(3,3); t("ds-lru", (a,c.get(2),c.get(3)), (1,-1,3))
s = ns("ds-aux")["MinStack"](); s.push(-2); s.push(0); s.push(-3); a=s.getMin(); s.pop(); t("ds-aux", (a,s.top(),s.getMin()), (-3,0,-2))
q = ns("ds-queue")["MyQueue"](); q.push(1); q.push(2); a=q.peek(); b=q.pop(); t("ds-queue", (a,b,q.empty()), (1,1,False))
r = ns("ds-random")["RandomizedSet"]()
t("ds-random", (r.insert(1), r.remove(2), r.insert(2), r.getRandom() in (1,2), r.remove(1), r.insert(2), r.getRandom()), (True,False,True,True,True,False,2))
r = ns("ds-random")["RandomizedSet"](); r.insert(5); r.remove(5); t("ds-random", (r.a, r.at), ([], {}))
m = ns("ds-timekey")["TimeMap"](); m.set("a","x",1); m.set("a","y",4); t("ds-timekey", (m.get("a",0),m.get("a",1),m.get("a",3),m.get("a",9),m.get("b",1)), ("","x","x","y",""))
it = ns("ds-iter")["BSTIterator"](tree([2,1,3])); o=[]
while it.hasNext(): o.append(it.next())
t("ds-iter", o, [1,2,3])
t("gw-components", ns("gw-components")["count_components"](5, [[0,1],[1,2],[3,4]]), 2)
t("gw-bipartite", (ns("gw-bipartite")["is_bipartite"]([[1,3],[0,2],[1,3],[0,2]]), ns("gw-bipartite")["is_bipartite"]([[1,2,3],[0,2],[0,1,3],[0,2]])), (True,False))
t("gw-state", (ns("gw-state")["open_lock"](["0201","0101","0102","1212","2002"],"0202"), ns("gw-state")["open_lock"](["0000"],"8888")), (6,-1))
t("gw-functional", (ns("gw-functional")["longest_cycle"]([3,3,4,2,3]), ns("gw-functional")["longest_cycle"]([2,-1,3,1])), (3,-1))
t("gw-bridges", sorted(sorted(e) for e in ns("gw-bridges")["bridges"](4, [[0,1],[1,2],[2,0],[1,3]])), [[1,3]])
t("gw-scc", ns("gw-scc")["scc_count"](5, [[1,0],[0,2],[2,1],[0,3],[3,4]]), 3)
t("gw-euler", ns("gw-euler")["itinerary"]([["MUC","LHR"],["JFK","MUC"],["SFO","SJC"],["LHR","SFO"]]), ["JFK","MUC","LHR","SFO","SJC"])

untested = sorted(set(CODE) - tested)
print("%d templates, %d tested, %d failures" % (len(CODE), len(tested), len(fails)))
if untested:
    print("NOT TESTED:", untested)
for f in fails[:30]:
    print("FAIL", f)
sys.exit(1 if fails or untested else 0)
