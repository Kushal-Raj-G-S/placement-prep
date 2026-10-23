# -*- coding: utf-8 -*-
"""
The words a person might type when they name a pattern or a variant. Used by the Mock OA page to read a
free-text answer ("sliding window, longest, hashmap for last seen index") without any multiple choice and
without any network call.

How the page uses it (see MATCHER in build_mock.py):
  - text is lower-cased and stripped to letters/digits, so "Two-Pointers" and "two pointers" are the same
  - an alias scores its word count when it appears in the answer (a longer phrase is more specific)
  - pattern score = its pattern aliases + the best variant inside it; the best pattern wins
  - inside that pattern the variant with the highest score wins; no variant score means "pattern only"

An alias that is a single very common word is kept out of PATTERN lists and only allowed on variants,
where the pattern has already been chosen by then.
"""

PATTERN = {
    "two-pointers": ["two pointer", "two pointers", "2 pointers", "2 pointer", "two ptr", "left right pointers", "l r pointers", "converging pointers"],
    "sliding-window": ["sliding window", "window technique", "moving window", "variable window", "fixed window", "window of size"],
    "prefix-sum": ["prefix sum", "prefix sums", "cumulative sum", "running total", "running sum", "prefix array", "prefix"],
    "binary-search": ["binary search", "bisect", "bisection", "bin search", "bs on"],
    "hashing": ["hashing", "hash map", "hashmap", "hash set", "hashset", "hash table", "dictionary", "dict", "frequency map", "counter"],
    "monotonic-stack": ["monotonic stack", "monotone stack", "stack"],
    "heap": ["heap", "priority queue", "min heap", "max heap", "pq"],
    "intervals": ["intervals", "interval", "sweep line", "sweep", "line sweep", "sort and merge", "overlapping"],
    "bits": ["bit manipulation", "bitwise", "bit trick", "bitmask", "bit mask", "xor", "bits"],
    "linked-list": ["linked list", "linked lists", "list surgery", "singly linked", "node rewiring", "fast and slow pointers", "slow and fast pointers", "fast slow pointers", "tortoise and hare", "tortoise", "rewiring links"],
    "tree-dfs": ["tree dfs", "dfs on tree", "tree recursion", "binary tree", "bst", "recursion on tree", "tree traversal"],
    "tree-bfs": ["tree bfs", "level order", "level by level", "bfs on tree", "level order traversal"],
    "trie": ["trie", "prefix tree", "digital tree"],
    "grid": ["grid", "matrix traversal", "flood fill", "grid bfs", "grid dfs", "islands", "maze"],
    "toposort": ["topological sort", "topological", "topo sort", "toposort", "kahn", "dependency order", "course schedule"],
    "shortest-path": ["shortest path", "dijkstra", "bellman ford", "bellman", "floyd warshall", "floyd", "weighted graph"],
    "dsu": ["union find", "disjoint set", "dsu", "union by rank", "kruskal", "spanning tree", "mst"],
    "dp-1d": ["1d dp", "1 d dp", "one dimensional dp", "linear dp", "dp", "dynamic programming", "kadane", "knapsack", "coin change", "lis"],
    "dp-2d": ["2d dp", "2 d dp", "two dimensional dp", "dp table", "dp grid", "dynamic programming", "dp", "knapsack", "lcs", "edit distance"],
    "backtracking": ["backtracking", "backtrack", "try and undo", "recursion with undo", "choose explore unchoose", "brute force with pruning", "n queens", "sudoku", "board filling"],
    "greedy": ["greedy", "locally best", "local optimum", "always pick the best", "exchange argument"],
}

VARIANT = {
    # two pointers
    "tp-ends": ["opposite ends", "both ends", "from both ends", "closing in", "left and right", "start and end", "converge", "sorted two sum", "ends moving inward", "inward"],
    "tp-write": ["read and write", "reader writer", "slow and fast", "fast and slow", "write pointer", "read pointer", "same direction", "in place", "compact", "remove duplicates", "overwrite"],
    "tp-merge": ["one pointer per", "pointer per array", "pointer in each", "pointer on each", "walk both", "walk two", "two sorted arrays", "merge two sorted arrays", "merge two arrays"],
    "tp-partition": ["dutch flag", "dutch national flag", "three way partition", "three way", "3 way", "low mid high", "three regions", "partition in place"],
    # sliding window
    "sw-fixed": ["fixed size", "fixed k", "fixed length", "fixed window", "window of size k", "every window of", "size k", "k sized"],
    "sw-longest": ["longest", "longest valid", "maximum length", "max length", "expand and shrink", "variable size longest", "at most", "no repeat", "without repeating"],
    "sw-shortest": ["shortest", "smallest window", "minimum window", "min window", "minimum length", "shrink while valid", "smallest valid", "shortest valid"],
    "sw-exact": ["exactly k", "exactly", "atmost k minus atmost", "at most k minus", "at most minus at most", "atmost minus atmost", "atmost"],
    "sw-deque": ["monotonic deque", "deque", "window maximum", "window max", "sliding window maximum", "max in window", "deque of indices"],
    # prefix sum
    "ps-range": ["range sum", "range sums", "range query", "range queries", "plain prefix", "prefix array", "sum of a range", "many queries"],
    "ps-count": ["count subarrays", "count the subarrays", "number of subarrays", "count with hashmap", "prefix and hashmap", "prefix hashmap", "prefix frequency", "sum equals k", "count of ranges", "count segments"],
    "ps-longest": ["longest subarray", "longest with hashmap", "first occurrence", "earliest index", "first index of prefix", "longest zero sum", "longest range", "longest segment", "shortest subarray"],
    "ps-2d": ["2d prefix", "two dimensional prefix", "2 d prefix", "integral image", "summed area", "rectangle sum", "prefix on matrix", "submatrix sum"],
    "ps-diff": ["difference array", "diff array", "range update", "range updates", "add to a range", "lazy add", "bulk update", "delta array", "difference"],
    "ps-suffix": ["prefix and suffix", "prefix suffix", "left and right pass", "left pass right pass", "two passes", "product except self", "suffix", "from the left and from the right"],
    # binary search
    "bs-exact": ["find the value", "classic binary search", "exact search", "search in sorted", "find target", "search for the value", "plain binary search"],
    "bs-bound": ["lower bound", "upper bound", "bound", "first position", "first element not less", "insertion point", "boundary", "first true", "bisect left", "bisect right", "leftmost", "rightmost"],
    "bs-answer": ["on the answer", "on answer", "search the answer", "answer space", "minimise the maximum", "minimize the maximum", "maximise the minimum", "maximize the minimum", "feasibility", "feasible", "can we do it in", "monotonic predicate", "capacity", "binary search on answer"],
    "bs-rotated": ["rotated", "mountain", "peak", "bitonic", "pivot", "locally ordered", "rotated array", "half is sorted"],
    "bs-partition": ["partition", "median of two", "two sorted arrays median", "split point", "cut", "kth of two"],
    # hashing
    "hs-seen": ["seen before", "seen set", "visited set", "duplicate", "have we seen", "set of seen", "membership", "contains duplicate", "first repeat"],
    "hs-freq": ["frequency", "count occurrences", "counts", "tally", "frequency map", "counter", "count each", "anagram", "histogram"],
    "hs-index": ["value to index", "value index", "index map", "complement", "two sum", "store index", "map from value", "target minus", "need minus"],
    "hs-group": ["group by", "grouping", "canonical", "signature", "sorted key", "derived key", "bucket by", "group anagrams", "normal form"],
    "hs-cyclic": ["cyclic sort", "index as hash", "index as key", "place at index", "array as hash", "swap into place", "missing number", "negate", "mark visited in place"],
    # monotonic stack
    "ms-next": ["next greater", "next smaller", "next warmer", "next larger", "nearest greater", "nearest smaller", "previous smaller", "previous greater", "next element"],
    "ms-hist": ["histogram", "largest rectangle", "area between bars", "bars", "trapping", "trap water", "maximal rectangle", "span"],
    "ms-match": ["matching", "nesting", "parsing", "balanced", "brackets", "parentheses", "valid parentheses", "expression", "evaluate", "nested", "undo"],
    "ms-greedy": ["stack as greedy", "greedy builder", "remove k digits", "smallest subsequence", "lexicographically smallest", "pop while", "build the smallest", "build the largest"],
    # heap
    "hp-topk": ["top k", "k largest", "k smallest", "kth largest", "kth smallest", "heap of size k", "size k heap", "k most frequent", "k closest"],
    "hp-merge": ["merge k", "k sorted", "k way merge", "merge many sorted", "smallest range", "k lists", "kth smallest in sorted", "merge k sorted lists"],
    "hp-two": ["two heaps", "running median", "median", "balance two", "min heap and max heap", "max heap and min heap", "lower half upper half"],
    "hp-greedy": ["heap greedy", "priority queue greedy", "heap and greedy", "greedy with heap", "greedy with priority queue", "simulation", "always take the", "repeatedly take", "task scheduler", "cooldown", "pick the largest each time", "process in order of", "pq greedy"],
    # intervals
    "iv-merge": ["merge intervals", "merge overlapping", "union of intervals", "coalesce", "combine overlapping", "merge ranges"],
    "iv-insert": ["insert interval", "insert into", "insert a new interval", "disjoint sorted", "insert and merge", "already sorted and disjoint"],
    "iv-greedy": ["sort by end", "earliest end", "earliest finish", "activity selection", "non overlapping", "maximum non overlapping", "max meetings", "remove minimum intervals", "interval scheduling"],
    "iv-sweep": ["sweep line", "events", "start and end events", "plus one minus one", "+1 -1", "max overlap", "meeting rooms", "how many at once", "concurrent", "overlap count", "line sweep"],
    "iv-sortkey": ["sort cars", "sort by position", "by position", "sort by speed", "one pass after sorting", "sort by", "custom sort", "sort then", "sort key", "comparator", "sort and scan", "sort then one pass", "right key"],
    # bits
    "bt-xor": ["xor", "cancels", "cancel out", "single number", "xor all", "pairs cancel", "missing and duplicate"],
    "bt-subsets": ["bitmask subsets", "enumerate subsets", "all subsets", "subset enumeration", "2^n", "mask loop", "bitmask enumeration", "iterate masks"],
    "bt-dp": ["bitmask dp", "dp over masks", "mask dp", "state mask", "visited mask", "assignment", "travelling", "tsp", "dp on subsets", "used mask"],
    "bt-tricks": ["bit tricks", "power of two", "count set bits", "popcount", "lowest set bit", "n and n minus 1", "shift", "parity", "bit count", "x & (x-1)"],
    # linked list
    "ll-fastslow": ["fast and slow", "slow and fast", "tortoise", "hare", "floyd cycle", "cycle detection", "find the middle", "middle of the list", "fast slow", "detect cycle"],
    "ll-reverse": ["reverse", "reversal", "rewire", "reverse in groups", "reverse k group", "flip links", "reverse a list", "reverse the links"],
    "ll-dummy": ["dummy head", "dummy node", "sentinel", "dummy", "fake head", "remove nodes", "delete nodes", "head might change"],
    "ll-merge": ["merge sorted lists", "merge two lists", "merge two sorted lists", "merge two sorted linked lists", "merge sorted linked lists", "merge linked lists", "merge lists", "zip lists", "weave", "relink"],
    # tree dfs
    "td-up": ["post order", "postorder", "return a value up", "return up", "bottom up", "height", "diameter", "children report", "combine children", "return from children"],
    "td-down": ["top down", "pass down", "carry context", "carry down", "path sum", "preorder", "pre order", "pass the state down", "parameter down", "root to leaf"],
    "td-bst": ["bst", "in order", "inorder", "sorted order", "binary search tree", "validate bst", "kth smallest in bst", "bst property"],
    "td-lca": ["lca", "lowest common ancestor", "common ancestor", "nearest shared", "first node where paths meet", "join point"],
    # tree bfs
    "tb-levels": ["level order", "level by level", "one level per round", "queue per level", "breadth first", "bfs", "right side view", "zigzag", "level wise", "layer by layer"],
    # trie
    "tr-basic": ["insert search startswith", "starts with", "prefix lookup", "autocomplete", "dictionary of words", "insert and search", "prefix query", "prefix check", "word dictionary"],
    "tr-search": ["trie pruner", "search pruner", "pruner", "prune", "word search", "prune the search", "dfs with trie", "board words", "search with trie", "wildcard", "pruning"],
    # grid
    "gr-flood": ["flood fill", "connected components", "islands", "number of islands", "dfs on grid", "count regions", "connected regions", "paint", "region"],
    "gr-bfs": ["shortest path in grid", "fewest moves", "minimum steps", "bfs", "shortest route", "min moves", "level by level on grid", "maze shortest", "unweighted shortest"],
    "gr-multi": ["multi source", "multi source bfs", "all sources at once", "spread simultaneously", "rotting", "spreads from many", "time to spread", "distance to nearest", "nearest source", "simultaneous"],
    # toposort
    "to-kahn": ["kahn", "indegree", "in degree", "bfs topological", "topological order", "course order", "dependency order", "zero indegree", "queue of zero"],
    "to-dfs": ["dfs topological", "three colour", "three color", "white grey black", "post order dfs", "cycle check", "back edge", "dfs cycle", "finish order", "reverse post order"],
    # shortest path
    "sp-dijkstra": ["dijkstra", "non negative weights", "priority queue shortest", "cheapest route", "single source shortest", "min cost path", "weighted shortest"],
    "sp-bellman": ["bellman ford", "bellman", "negative weights", "negative edges", "at most k edges", "k stops", "relax k times", "negative cycle", "k edge"],
    "sp-floyd": ["floyd warshall", "floyd", "all pairs", "every pair", "all pairs shortest", "distance between every", "transitive closure", "n cubed"],
    # dsu
    "dsu-connect": ["the structure itself", "dsu structure", "connected", "same group", "merge groups", "components", "group membership", "are they connected", "friend circles", "provinces"],
    "dsu-cycle": ["redundant connection", "cycle detection", "extra edge", "already connected", "adds a cycle", "union returns false", "redundant", "detect cycle undirected"],
    "dsu-kruskal": ["kruskal", "minimum spanning tree", "mst", "spanning tree", "cheapest connect", "cheapest network", "sort edges", "connect everything cheapest"],
    # dp 1d
    "dp-linear": ["take or skip", "take skip", "house robber", "no two adjacent", "non adjacent", "linear dp", "skip or take", "include exclude", "pick or skip"],
    "dp-kadane": ["kadane", "best contiguous", "max subarray", "maximum subarray", "contiguous run", "best run", "max sum contiguous", "extend or restart"],
    "dp-coin": ["unbounded knapsack", "coin change", "coins", "unlimited", "ways to make", "fewest coins", "stairs", "climbing", "rod cutting", "unbounded"],
    "dp-lis": ["lis", "longest increasing subsequence", "increasing subsequence", "longest increasing", "patience", "nesting dolls", "envelopes", "tails array"],
    # dp 2d
    "dp-grid": ["grid paths", "grid dp", "unique paths", "min path sum", "paths in grid", "cost grid", "robot", "down or right", "dp on grid"],
    "dp-twostring": ["lcs", "longest common subsequence", "edit distance", "two strings", "two sequences", "levenshtein", "common subsequence", "align", "diff of two"],
    "dp-knapsack": ["0 1 knapsack", "01 knapsack", "knapsack", "subset sum", "partition equal", "each item once", "use each once", "capacity and value", "take at most once"],
    "dp-interval": ["interval dp", "range dp", "burst balloons", "matrix chain", "split the range", "dp over ranges", "build ranges from smaller", "palindrome partition", "merge stones", "dp on intervals"],
    # backtracking
    "bk-subsets": ["subsets", "combinations", "combination sum", "power set", "all combinations", "choose k", "generate subsets", "include or exclude"],
    "bk-perms": ["permutations", "permute", "orderings", "all orderings", "arrangements", "swap and recurse", "used array"],
    "bk-board": ["n queens", "nqueens", "sudoku", "board", "board filling", "grid filling", "board grid filling", "word search", "place pieces", "fill the board", "constraint board", "grid backtracking"],
    # greedy
    "gr-reach": ["furthest reach", "farthest reach", "jump game", "max reach", "reach so far", "gas station", "can we reach", "minimum jumps", "refuel", "farthest"],
    "gr-pair": ["sort and pair", "pair from the ends", "pair smallest with largest", "boats", "two ends pair", "sort then pair", "heaviest with lightest", "pair up"],
    "gr-local": ["spend the budget", "budget", "cheapest first", "best now", "best per cost", "ratio", "fractional", "buy the cheapest", "locally best", "take the best available"],
}
