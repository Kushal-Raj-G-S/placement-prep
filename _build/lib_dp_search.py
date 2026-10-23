# -*- coding: utf-8 -*-
"""Learn content: dynamic programming, backtracking, greedy."""

PATTERNS = [

# ------------------------------------------------------------------- DP 1-D -------
{
 "id": "dp-1d", "group": "dp", "name": "1-D dynamic programming",
 "buys": "O(2ⁿ) exponential recursion → O(n) or O(n·k), by never solving the same subproblem twice",
 "lives": "a sequence, where the answer at i depends on a few earlier answers",
 "core": "Two questions, in order. First: WHAT IS THE STATE — what does dp[i] actually mean, said as a full "
         "English sentence? Second: what CHOICE do you make at i, and which earlier states does it read? "
         "If you cannot say the sentence, you do not have a DP yet, and writing code will not rescue you. "
         "Start from the recursion, add memoisation, then flatten it to a loop if you want.",
 "recognise": [
   {"cue": "<b>maximum / minimum / count the ways</b>, over a sequence of choices", "note": "the DP trio"},
   {"cue": "<b>take it or skip it</b> at each position", "note": "dp[i] = best(take, skip)"},
   {"cue": "<b>cannot use two adjacent</b> / a cooldown applies", "note": "dp[i] reads dp[i-2]"},
   {"cue": "<b>unlimited copies</b> of each item (coins, cuts)", "note": "unbounded knapsack — loop forward"},
   {"cue": "<b>longest increasing</b> subsequence, and n ≤ 2500 vs n ≤ 10⁵", "note": "O(n²) DP vs patience + binary search"},
   {"cue": "overlapping subproblems you can SEE when you draw the recursion tree", "note": "memoise it"},
 ],
 "notwhen": [
   "A local choice is provably safe at every step → <b>greedy</b>, which is O(n log n) and much shorter.",
   "The window is contiguous and you track an aggregate → sliding window, not DP.",
   "Each step depends on ALL previous states, not a few → you probably need a different state, or a tree / segment structure.",
 ],
 "pick": [
   {"if": "take-or-skip along a line, with an adjacency rule", "then": "dp-linear"},
   {"if": "the best CONTIGUOUS run (sum or product)", "then": "dp-kadane"},
   {"if": "unlimited copies of items hitting a target", "then": "dp-coin"},
   {"if": "the longest increasing / chain-like subsequence", "then": "dp-lis"},
 ],
 "variants": [
  {"id": "dp-linear", "name": "Linear take-or-skip",
   "when": "Walk the sequence; at each position you choose, and a rule limits adjacent choices.",
   "tool": "dp[i] = the best answer considering the first i items",
   "invariant": "dp[i] is final before dp[i+1] is computed, and only reads a fixed window behind it",
   "cx": "O(n) time, O(1) space once you keep only the last two values",
   "code": """def rob(nums):
    # state: best loot from the first i houses.  choice at i: rob it (+ dp[i-2]) or skip (dp[i-1])
    prev2, prev1 = 0, 0
    for x in nums:
        prev2, prev1 = prev1, max(prev1, prev2 + x)
    return prev1

def climb(n):
    # state: ways to reach step i.  choice: arrive from i-1 or i-2
    a, b = 1, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b""",
   "asks": [
     "climbing stairs; min cost climbing stairs; Fibonacci-shaped counting",
     "house robber I (line) and II (circle — run it twice, excluding one end each time)",
     "decode ways — count the ways to split a digit string into letters",
     "delete and earn (bucket by value, then it IS house robber)",
     "best time to buy and sell stock with cooldown / with a fee (a small state machine)",
     "maximum alternating subsequence sum; tiling a 2×n board; 'n-th tribonacci'",
     "jump game II when you want the fewest jumps as a DP (greedy is faster)",
     "partition into at most k groups along a line",
   ],
   "examples": [
     {"n": "Climbing Stairs", "s": "LC 70"},
     {"n": "Min Cost Climbing Stairs", "s": "LC 746"},
     {"n": "House Robber", "s": "LC 198"},
     {"n": "House Robber II", "s": "LC 213"},
     {"n": "Decode Ways", "s": "LC 91"},
     {"n": "Delete and Earn", "s": "LC 740"},
     {"n": "Best Time to Buy and Sell Stock with Cooldown", "s": "LC 309"},
   ],
   "traps": [
     "Write the state as a SENTENCE in a comment first. Most wrong DP is a wrong state, not wrong code.",
     "Decode Ways has nasty zeros: '0' alone decodes to nothing, and '10' / '20' only work as pairs.",
     "The circular version is two linear runs, not a clever single pass.",
     "Rolling two variables instead of an array is the standard O(1)-space move — do it last, after it works.",
   ]},

  {"id": "dp-kadane", "name": "Kadane — best contiguous run",
   "when": "Maximum (or minimum) sum or product of a CONTIGUOUS subarray.",
   "tool": "cur = best run ENDING here; answer = best cur ever seen",
   "invariant": "a run ending at i either extends the run ending at i-1 or starts fresh at i",
   "cx": "O(n) time, O(1) space",
   "code": """def max_subarray(a):
    cur = best = a[0]
    for x in a[1:]:
        cur = max(x, cur + x)      # start fresh, or extend -- that is the whole decision
        best = max(best, cur)
    return best

def max_product(a):
    # products need BOTH extremes: a big negative times a negative becomes the new maximum
    cur_hi = cur_lo = best = a[0]
    for x in a[1:]:
        cands = (x, cur_hi * x, cur_lo * x)
        cur_hi, cur_lo = max(cands), min(cands)
        best = max(best, cur_hi)
    return best""",
   "asks": [
     "maximum subarray sum (and returning the actual indices)",
     "maximum product subarray",
     "maximum sum circular subarray (total − minimum subarray, with the all-negative special case)",
     "best time to buy and sell stock (the same shape: track the min so far)",
     "maximum absolute sum of any subarray",
     "longest turbulent subarray; maximum ascending subarray sum",
     "K-concatenation maximum sum",
   ],
   "examples": [
     {"n": "Maximum Subarray", "s": "LC 53"},
     {"n": "Maximum Product Subarray", "s": "LC 152"},
     {"n": "Maximum Sum Circular Subarray", "s": "LC 918"},
     {"n": "Best Time to Buy and Sell Stock", "s": "LC 121"},
     {"n": "Maximum Absolute Sum of Any Subarray", "s": "LC 1749"},
   ],
   "traps": [
     "Start from a[0], not 0 — seeding with 0 silently returns 0 for an all-negative array.",
     "Products need the minimum tracked too, because two negatives make a maximum.",
     "The circular version's trap: if every number is negative, total − min is 0, which is not a legal non-empty answer.",
   ]},

  {"id": "dp-coin", "name": "Unbounded knapsack (coins, cuts, steps)",
   "when": "Unlimited copies of each item, and you must hit or fill a target.",
   "tool": "dp over the TARGET; loop items outside and amount inside (or the reverse — the order decides the meaning)",
   "invariant": "dp[t] is final for every t below the one you are filling",
   "cx": "O(items · target)",
   "code": """def coin_change(coins, amount):           # FEWEST coins
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0                                 # zero coins make zero
    for t in range(1, amount + 1):
        for c in coins:
            if c <= t:
                dp[t] = min(dp[t], dp[t - c] + 1)
    return -1 if dp[amount] == float('inf') else dp[amount]

def count_combinations(coins, amount):    # how many COMBINATIONS (order does not matter)
    dp = [0] * (amount + 1); dp[0] = 1
    for c in coins:                        # coins OUTSIDE -> combinations
        for t in range(c, amount + 1):     # forward -> a coin may be reused
            dp[t] += dp[t - c]
    return dp[amount]""",
   "asks": [
     "coin change — fewest coins to make the amount",
     "coin change II — how many combinations make the amount",
     "combination sum IV — how many PERMUTATIONS (swap the loops!)",
     "perfect squares — fewest squares summing to n",
     "rod cutting / integer break for maximum product",
     "minimum number of refuelling or rechargeable steps",
     "word break — can the string be cut into dictionary words",
     "number of ways to climb with a given set of step sizes",
   ],
   "examples": [
     {"n": "Coin Change", "s": "LC 322"},
     {"n": "Coin Change II", "s": "LC 518"},
     {"n": "Combination Sum IV", "s": "LC 377"},
     {"n": "Perfect Squares", "s": "LC 279"},
     {"n": "Word Break", "s": "LC 139"},
     {"n": "Integer Break", "s": "LC 343"},
   ],
   "traps": [
     "LOOP ORDER CHANGES THE ANSWER. Items outside counts combinations; target outside counts permutations. "
     "LC 518 and LC 377 are the same code with the loops swapped — know which one you need.",
     "Unbounded loops the amount FORWARD (reuse allowed); 0/1 knapsack loops it BACKWARD (one use only).",
     "dp[0] = 1 for counting and dp[0] = 0 for minimising. Mixing them up breaks everything downstream.",
     "Return −1 when the target is unreachable — do not report infinity.",
   ]},

  {"id": "dp-lis", "name": "Longest increasing subsequence",
   "when": "The longest chain where each item beats the previous by some rule.",
   "tool": "O(n²): dp[i] = best chain ending at i. O(n log n): a tails array + binary search",
   "invariant": "tails[k] holds the SMALLEST possible ending value of an increasing run of length k+1",
   "cx": "O(n²) or O(n log n) — and the constraint tells you which one is required",
   "code": """# O(n^2) -- fine for n <= 2500, and it lets you reconstruct the sequence
def lis_quadratic(a):
    dp = [1] * len(a)
    for i in range(len(a)):
        for j in range(i):
            if a[j] < a[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp, default=0)

# O(n log n) -- required once n hits 1e5.  tails is NOT the answer sequence, only its length is right
from bisect import bisect_left
def lis_fast(a):
    tails = []
    for x in a:
        i = bisect_left(tails, x)       # bisect_right for non-decreasing runs
        if i == len(tails): tails.append(x)
        else: tails[i] = x
    return len(tails)""",
   "asks": [
     "longest increasing subsequence (both complexities — Pattern Radar drills exactly this choice)",
     "number of longest increasing subsequences (needs the O(n²) form plus a count array)",
     "russian doll envelopes (sort by width, LIS on height, descending on ties)",
     "maximum length of a pair chain; longest string chain",
     "minimum number of removals to make an array sorted = n − LIS",
     "box stacking, 'maximum height by stacking'",
     "longest arithmetic subsequence (state becomes (index, difference))",
     "minimum number of increasing subsequences to cover the array (= longest DECREASING run)",
   ],
   "examples": [
     {"n": "Longest Increasing Subsequence", "s": "LC 300"},
     {"n": "Number of Longest Increasing Subsequence", "s": "LC 673"},
     {"n": "Russian Doll Envelopes", "s": "LC 354"},
     {"n": "Longest String Chain", "s": "LC 1048"},
     {"n": "Maximum Length of Pair Chain", "s": "LC 646"},
     {"n": "Longest Arithmetic Subsequence", "s": "LC 1027"},
   ],
   "traps": [
     "The tails array is NOT the subsequence. Its length is correct; its contents usually are not a real answer.",
     "Russian dolls: sort widths ascending but heights DESCENDING within equal widths, or one width pairs with itself.",
     "Strictly increasing uses bisect_left; non-decreasing uses bisect_right. One character, different problem.",
     "Read the bound. n ≤ 2500 permits O(n²); n ≤ 10⁵ demands the log version.",
   ]},
 ]},

# ------------------------------------------------------------------- DP 2-D -------
{
 "id": "dp-2d", "group": "dp", "name": "2-D dynamic programming",
 "buys": "exponential branching → O(n·m), filling a table once",
 "lives": "a grid, two sequences compared, or an item list against a budget",
 "core": "The second dimension appears for one of three reasons: you are moving on an actual grid, you are "
         "comparing TWO sequences (one index each), or you are tracking a BUDGET alongside your position. "
         "Name both axes in a sentence before you write anything — dp[i][j] = ... — and the transitions "
         "usually write themselves from the samples.",
 "recognise": [
   {"cue": "<b>grid</b>, and 'how many paths' or 'cheapest path'", "note": "dp[r][c] from the top and the left"},
   {"cue": "<b>two strings</b> compared, matched or transformed", "note": "dp[i][j] over the two prefixes"},
   {"cue": "<b>pick or skip</b> each item against a weight / sum budget", "note": "0/1 knapsack"},
   {"cue": "<b>split the array into k parts</b>, 'burst / merge in some order'", "note": "interval DP"},
   {"cue": "'the answer for a RANGE, built from smaller ranges'", "note": "interval DP — loop by length"},
 ],
 "notwhen": [
   "Only one index really matters → you are carrying a dimension you do not need; shrink the state.",
   "n·m exceeds about 10⁸ → the table will not fit in the time budget; look for a greedy or a different state.",
 ],
 "pick": [
   {"if": "movement on a grid", "then": "dp-grid"},
   {"if": "two sequences compared", "then": "dp-twostring"},
   {"if": "items against a capacity or target, each usable once", "then": "dp-knapsack"},
   {"if": "the answer for a range built from sub-ranges", "then": "dp-interval"},
 ],
 "variants": [
  {"id": "dp-grid", "name": "Grid paths & costs",
   "when": "Move through a grid, usually only right and down.",
   "tool": "dp[r][c] built from dp[r-1][c] and dp[r][c-1]",
   "invariant": "every cell is final before any cell that depends on it is computed",
   "cx": "O(rows · cols), reducible to O(cols) space with a rolling row",
   "code": """def min_path_sum(g):
    R, C = len(g), len(g[0])
    dp = [[0] * C for _ in range(R)]
    for r in range(R):
        for c in range(C):
            if r == 0 and c == 0: dp[r][c] = g[r][c]
            elif r == 0:          dp[r][c] = dp[r][c-1] + g[r][c]      # top row: only from the left
            elif c == 0:          dp[r][c] = dp[r-1][c] + g[r][c]      # left col: only from above
            else:                 dp[r][c] = min(dp[r-1][c], dp[r][c-1]) + g[r][c]
    return dp[R-1][C-1]""",
   "asks": [
     "unique paths; unique paths II (with obstacles)",
     "minimum path sum; maximum points / cherry pickup",
     "triangle minimum path sum",
     "dungeon game (fill BACKWARD from the princess — the direction is the trick)",
     "maximal square / maximal rectangle of ones",
     "count square submatrices with all ones",
     "number of paths with a falling-path constraint",
     "minimum falling path sum",
   ],
   "examples": [
     {"n": "Unique Paths", "s": "LC 62"},
     {"n": "Unique Paths II", "s": "LC 63"},
     {"n": "Minimum Path Sum", "s": "LC 64"},
     {"n": "Triangle", "s": "LC 120"},
     {"n": "Maximal Square", "s": "LC 221"},
     {"n": "Dungeon Game", "s": "LC 174"},
     {"n": "Minimum Falling Path Sum", "s": "LC 931"},
   ],
   "traps": [
     "Handle the first row and first column explicitly, or pad the table with a sentinel border. Half of grid-DP bugs live there.",
     "Dungeon Game must be filled from the END backwards: health needed later changes what is safe now.",
     "Maximal Square's transition is <code>min</code> of three neighbours plus one — not a sum.",
     "An obstacle makes the cell 0 ways, which must not be confused with 'not computed yet'.",
   ]},

  {"id": "dp-twostring", "name": "Two sequences (LCS / edit distance)",
   "when": "Two strings or arrays compared, matched, or transformed into each other.",
   "tool": "dp[i][j] over the first i of one and the first j of the other; a padded row and column of zeros",
   "invariant": "dp[i][j] only ever reads the cell diagonally up-left, up, and left",
   "cx": "O(n·m) time, O(min(n,m)) space with a rolling row",
   "code": """def lcs(a, b):
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]     # the padding row/col IS the base case
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i-1] == b[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1        # match: consume both
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])   # drop one or the other
    return dp[n][m]

def edit_distance(a, b):
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1): dp[i][0] = i            # delete everything
    for j in range(m + 1): dp[0][j] = j            # insert everything
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i-1] == b[j-1]: dp[i][j] = dp[i-1][j-1]
            else: dp[i][j] = 1 + min(dp[i-1][j-1],  # replace
                                     dp[i-1][j],     # delete
                                     dp[i][j-1])     # insert
    return dp[n][m]""",
   "asks": [
     "longest common subsequence; longest common substring (reset to 0 on a mismatch instead of taking a max)",
     "edit distance; one edit distance away; delete operations to make two strings equal",
     "distinct subsequences — count how many times t appears inside s",
     "wildcard matching and regular expression matching",
     "shortest common supersequence; minimum ASCII delete sum",
     "interleaving string; is one string a subsequence of another",
     "uncrossed lines (LCS wearing a different story)",
     "longest palindromic subsequence (LCS of the string and its reverse)",
   ],
   "examples": [
     {"n": "Longest Common Subsequence", "s": "LC 1143"},
     {"n": "Edit Distance", "s": "LC 72"},
     {"n": "Distinct Subsequences", "s": "LC 115"},
     {"n": "Regular Expression Matching", "s": "LC 10"},
     {"n": "Wildcard Matching", "s": "LC 44"},
     {"n": "Interleaving String", "s": "LC 97"},
     {"n": "Longest Palindromic Subsequence", "s": "LC 516"},
   ],
   "traps": [
     "The index shift: dp[i][j] uses a[i-1] and b[j-1]. Mixing the two conventions is the classic off-by-one here.",
     "SUBSTRING is not SUBSEQUENCE. A mismatch resets a substring run to zero; a subsequence takes the max.",
     "Edit distance needs the first row and column pre-filled with 0..n and 0..m, not zeros.",
     "Regex '*' matches zero or more of the PREVIOUS character — handle the zero case first and the rest follows.",
   ]},

  {"id": "dp-knapsack", "name": "0/1 knapsack & subset sum",
   "when": "Each item may be used AT MOST once, against a capacity or a target sum.",
   "tool": "dp over capacity, looping the capacity BACKWARD so each item is used once",
   "invariant": "when filling dp[t] for item i, dp already reflects items 0..i-1 only",
   "cx": "O(items · capacity)",
   "code": """def knapsack(weights, values, cap):
    dp = [0] * (cap + 1)
    for i in range(len(weights)):
        for t in range(cap, weights[i] - 1, -1):   # BACKWARD -- the one-use guarantee
            dp[t] = max(dp[t], dp[t - weights[i]] + values[i])
    return dp[cap]

def can_partition(nums):                  # equal-sum halves
    total = sum(nums)
    if total % 2: return False            # odd total can never split evenly
    target = total // 2
    dp = [False] * (target + 1); dp[0] = True
    for x in nums:
        for t in range(target, x - 1, -1):
            dp[t] = dp[t] or dp[t - x]
    return dp[target]""",
   "asks": [
     "partition equal subset sum; subset sum; target sum (assign + or − to each number)",
     "last stone weight II (minimise the difference = partition as evenly as possible)",
     "ones and zeroes (a knapsack with TWO capacities)",
     "profitable schemes; number of subsets with a given sum",
     "minimum difference between two subset sums",
     "tallest billboard; 'split into two groups with the closest totals'",
     "0/1 knapsack with a count limit (bounded knapsack — binary-split the copies)",
   ],
   "examples": [
     {"n": "Partition Equal Subset Sum", "s": "LC 416"},
     {"n": "Target Sum", "s": "LC 494"},
     {"n": "Last Stone Weight II", "s": "LC 1049"},
     {"n": "Ones and Zeroes", "s": "LC 474"},
     {"n": "Profitable Schemes", "s": "LC 879"},
   ],
   "traps": [
     "BACKWARD loop for 0/1, FORWARD for unbounded. This single direction is the difference between the two whole families.",
     "An odd total means 'partition into equal halves' is instantly false — check it before building any table.",
     "Target Sum converts to subset sum: picking a subset P to be positive means sum(P) = (total + target) / 2, and it must be a whole number.",
     "Two capacities means two dimensions, both looped backward.",
   ]},

  {"id": "dp-interval", "name": "Interval DP (build ranges from sub-ranges)",
   "when": "The answer for a range depends on splitting it, and the order of operations matters.",
   "tool": "loop by LENGTH, then by left end; try every split point inside",
   "invariant": "all shorter ranges are already solved before any longer range is attempted",
   "cx": "O(n³) — which is why n ≤ ~100–500 in these problems",
   "code": """def burst_balloons(nums):
    a = [1] + nums + [1]                 # virtual balloons at both ends
    n = len(a)
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n):            # LENGTH outside -- the key loop order
        for l in range(0, n - length):
            r = l + length
            for k in range(l + 1, r):     # k is the LAST balloon burst in (l, r)
                dp[l][r] = max(dp[l][r],
                               dp[l][k] + a[l]*a[k]*a[r] + dp[k][r])
    return dp[0][n-1]""",
   "asks": [
     "burst balloons; minimum cost to merge stones",
     "palindrome partitioning II — fewest cuts",
     "longest palindromic subsequence / substring (the range form)",
     "matrix chain multiplication; minimum score triangulation of a polygon",
     "stone game variants where you take from either end",
     "remove boxes; strange printer",
     "minimum cost to cut a stick",
   ],
   "examples": [
     {"n": "Burst Balloons", "s": "LC 312"},
     {"n": "Palindrome Partitioning II", "s": "LC 132"},
     {"n": "Longest Palindromic Subsequence", "s": "LC 516"},
     {"n": "Minimum Score Triangulation of Polygon", "s": "LC 1039"},
     {"n": "Minimum Cost to Cut a Stick", "s": "LC 1547"},
     {"n": "Stone Game", "s": "LC 877"},
   ],
   "traps": [
     "Loop by LENGTH first. Iterating l and r in the natural order reads cells that have not been filled.",
     "Burst Balloons only works if you think of k as the LAST balloon popped in the range, not the first. "
     "That reframing is the entire problem.",
     "The virtual 1s at both ends remove every boundary check.",
     "O(n³) with n = 500 is 125 million — borderline in Python, so check the bound first.",
   ]},
 ]},

# -------------------------------------------------------------- backtracking ------
{
 "id": "backtracking", "group": "search", "name": "Backtracking (try, recurse, undo)",
 "buys": "nothing asymptotically — it IS the exponential. What it buys is PRUNING, and a clean way to enumerate",
 "lives": "subsets, permutations, combinations, board puzzles; n is always small",
 "core": "One shape, three lines: choose, recurse, un-choose. The template never changes; what changes is the "
         "loop bounds and the pruning test. The constraint is the giveaway — n ≤ 10 means permutations are "
         "fine, n ≤ 20 means subsets are fine, and anything larger means this is the wrong pattern and you "
         "want DP or greedy instead.",
 "recognise": [
   {"cue": "<b>all</b> subsets / permutations / combinations, print THEM not just the count", "note": "you must enumerate"},
   {"cue": "<b>n ≤ 10 to 20</b> in the constraints", "note": "exponential is affordable, and intended"},
   {"cue": "<b>board puzzle</b> — n-queens, sudoku, word search", "note": "place, recurse, remove"},
   {"cue": "'<b>partition</b> into k groups', 'can these be split evenly'", "note": "backtracking with pruning"},
   {"cue": "<b>palindrome partitioning</b>, 'all ways to split'", "note": "cut, recurse on the rest"},
 ],
 "notwhen": [
   "You only need the COUNT or the BEST, not the list → that is usually DP, and vastly faster.",
   "n is large → 2ⁿ will not finish. Re-read the constraints; you have the wrong pattern.",
 ],
 "pick": [
   {"if": "subsets or combinations (order does not matter)", "then": "bk-subsets"},
   {"if": "permutations (order matters)", "then": "bk-perms"},
   {"if": "a grid or board to fill", "then": "bk-board"},
 ],
 "variants": [
  {"id": "bk-subsets", "name": "Subsets & combinations",
   "when": "Choose a set, where order does not matter.",
   "tool": "a start index, so you never look backwards — that is what prevents duplicate sets",
   "invariant": "every recursive call only considers items at or after `start`",
   "cx": "O(2ⁿ · n) for subsets, O(C(n,k) · k) for combinations",
   "code": """def subsets(nums):
    out, cur = [], []
    def go(start):
        out.append(cur[:])                  # every node is an answer -- copy it
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i-1]:
                continue                     # skip duplicates (needs nums sorted)
            cur.append(nums[i])
            go(i + 1)                        # i+1: never reuse this item
            cur.pop()                        # UNDO
    go(0)
    return out""",
   "asks": [
     "subsets; subsets II (with duplicates)",
     "combinations C(n, k); combination sum I / II / III",
     "palindrome partitioning — every way to cut into palindromes",
     "letter combinations of a phone number",
     "partition to k equal sum subsets",
     "generate parentheses (the choice is '(' or ')', with a validity rule)",
     "beautiful arrangement; splitting a string into unique substrings",
   ],
   "examples": [
     {"n": "Subsets", "s": "LC 78"},
     {"n": "Subsets II", "s": "LC 90"},
     {"n": "Combination Sum", "s": "LC 39"},
     {"n": "Combination Sum II", "s": "LC 40"},
     {"n": "Palindrome Partitioning", "s": "LC 131"},
     {"n": "Generate Parentheses", "s": "LC 22"},
     {"n": "Letter Combinations of a Phone Number", "s": "LC 17"},
   ],
   "traps": [
     "Append a COPY (<code>cur[:]</code>). Appending the live list gives you a result full of identical empty lists.",
     "<code>go(i + 1)</code> uses each item once; <code>go(i)</code> allows reuse. One character apart, two different problems.",
     "Duplicate skipping needs the input SORTED, and the test is <code>i > start</code>, not <code>i > 0</code>.",
     "Prune early: if the running sum already exceeds the target, return instead of recursing.",
   ]},

  {"id": "bk-perms", "name": "Permutations",
   "when": "Order matters — arrangements, not selections.",
   "tool": "a used[] flag array (or swap in place); every unused item is a candidate at every depth",
   "invariant": "cur always holds a valid partial arrangement with no repeats",
   "cx": "O(n! · n)",
   "code": """def permute(nums):
    nums.sort()                             # needed for duplicate skipping
    out, cur = [], []
    used = [False] * len(nums)
    def go():
        if len(cur) == len(nums):
            out.append(cur[:]); return
        for i in range(len(nums)):
            if used[i]: continue
            if i > 0 and nums[i] == nums[i-1] and not used[i-1]:
                continue                     # the duplicate rule for permutations
            used[i] = True;  cur.append(nums[i])
            go()
            cur.pop();       used[i] = False
    go()
    return out""",
   "asks": [
     "permutations; permutations II (with duplicates)",
     "next permutation (the O(n) in-place trick, not backtracking)",
     "n-queens, counted or listed",
     "letter case permutation; string permutations",
     "the travelling salesman for n ≤ 10 (brute force before you reach for bitmask DP)",
     "matchsticks to square; fair distribution of cookies",
   ],
   "examples": [
     {"n": "Permutations", "s": "LC 46"},
     {"n": "Permutations II", "s": "LC 47"},
     {"n": "Next Permutation", "s": "LC 31"},
     {"n": "Letter Case Permutation", "s": "LC 784"},
     {"n": "Matchsticks to Square", "s": "LC 473"},
   ],
   "traps": [
     "The duplicate rule here (<code>not used[i-1]</code>) differs from the subsets rule. Memorise both; they are not interchangeable.",
     "Reset BOTH the flag and the list on the way out, in the reverse order you set them.",
     "n = 11 already gives 40 million permutations. Check the bound before writing this.",
   ]},

  {"id": "bk-board", "name": "Board / grid filling",
   "when": "Place things on a grid under constraints.",
   "tool": "place a mark, recurse, remove the mark; keep fast 'is this legal' sets",
   "invariant": "the board is always in a legal state when you recurse, and restored when you return",
   "cx": "exponential, but pruning makes it tractable",
   "code": """def solve_n_queens(n):
    cols, diag, anti = set(), set(), set()
    board, out = [], []
    def go(r):
        if r == n:
            out.append(board[:]); return
        for c in range(n):
            if c in cols or (r - c) in diag or (r + c) in anti:
                continue                     # O(1) legality test -- this is the pruning
            cols.add(c); diag.add(r - c); anti.add(r + c); board.append(c)
            go(r + 1)
            board.pop(); anti.discard(r + c); diag.discard(r - c); cols.discard(c)
    go(0)
    return out""",
   "asks": [
     "n-queens I and II",
     "sudoku solver; valid sudoku",
     "word search (one word) and word search II (with a trie)",
     "rat in a maze, all paths through a grid",
     "unique paths III — walk over every empty square exactly once",
     "flood a grid under constraints; 'number of ways to colour'",
   ],
   "examples": [
     {"n": "N-Queens", "s": "LC 51"},
     {"n": "N-Queens II", "s": "LC 52"},
     {"n": "Sudoku Solver", "s": "LC 37"},
     {"n": "Word Search", "s": "LC 79"},
     {"n": "Unique Paths III", "s": "LC 980"},
   ],
   "traps": [
     "Diagonals are identified by <code>r - c</code> and anti-diagonals by <code>r + c</code>. That turns the legality test into O(1) and is the whole reason n-queens finishes.",
     "Restore the board EXACTLY, in reverse order. A missed restore corrupts every later branch silently.",
     "Word Search must mark the current cell before recursing and unmark after, or a path reuses a letter.",
   ]},
 ]},

# -------------------------------------------------------------------- greedy ------
{
 "id": "greedy", "group": "search", "name": "Greedy (one pass, locally best)",
 "buys": "O(2ⁿ) search or an O(n²) DP → O(n log n), usually just a sort and a loop",
 "lives": "anything where a local choice provably cannot hurt the future",
 "core": "Greedy is the cheapest pattern to code and the easiest to get silently wrong. The whole game is the "
         "JUSTIFICATION: you must be able to say, in one sentence, why taking the best thing now never costs you "
         "later (the exchange argument). If you cannot say that sentence, write the DP instead — a greedy that "
         "passes the samples and fails the hidden tests is the most expensive mistake in an OA.",
 "recognise": [
   {"cue": "<b>sort first</b>, then one pass, and the choice is obvious", "note": "the classic shape"},
   {"cue": "<b>maximum number of non-overlapping</b> / fewest removals", "note": "sort by END time"},
   {"cue": "<b>can you reach</b> the end, 'is it possible'", "note": "track the FURTHEST reach"},
   {"cue": "<b>always serve the most urgent / cheapest next</b>", "note": "greedy driven by a heap"},
   {"cue": "<b>two ends</b>, pair the biggest with the smallest", "note": "sort + two pointers"},
 ],
 "notwhen": [
   "A choice now can make a LATER choice impossible in a way you cannot bound → DP.",
   "Coin change with arbitrary denominations — the classic greedy TRAP. Taking the biggest coin first "
   "fails on coins [1, 3, 4] with amount 6 (greedy gives 4+1+1 = 3 coins, optimal is 3+3 = 2). Use DP.",
   "You need the count of ways, not one best answer → DP.",
 ],
 "pick": [
   {"if": "'can I get to the end' / reachability", "then": "gr-reach"},
   {"if": "pair items from both ends after sorting", "then": "gr-pair"},
   {"if": "spend a budget on the most valuable thing each step", "then": "gr-local"},
 ],
 "variants": [
  {"id": "gr-reach", "name": "Furthest reach",
   "when": "'Can you reach the end', or 'fewest jumps / refuels / taps'.",
   "tool": "one variable: the furthest index reachable so far",
   "invariant": "every index up to `reach` is reachable, so if i ever passes reach you are stuck",
   "cx": "O(n) time, O(1) space",
   "code": """def can_jump(nums):
    reach = 0
    for i, x in enumerate(nums):
        if i > reach:
            return False                 # a gap you cannot cross
        reach = max(reach, i + x)        # the only state you need
    return True

def min_jumps(nums):                     # fewest jumps: BFS-by-level, without a queue
    jumps = cur_end = furthest = 0
    for i in range(len(nums) - 1):
        furthest = max(furthest, i + nums[i])
        if i == cur_end:                 # the current jump's range is exhausted
            jumps += 1
            cur_end = furthest
    return jumps""",
   "asks": [
     "jump game I (can you reach the end) and II (fewest jumps)",
     "gas station — the unique valid start",
     "minimum number of taps to water a garden; video stitching",
     "minimum number of refuelling stops (heap-greedy)",
     "maximum distance you can travel, 'furthest building with ladders and bricks'",
     "can place flowers; candy distribution",
   ],
   "examples": [
     {"n": "Jump Game", "s": "LC 55"},
     {"n": "Jump Game II", "s": "LC 45"},
     {"n": "Gas Station", "s": "LC 134"},
     {"n": "Minimum Number of Taps to Open to Water a Garden", "s": "LC 1326"},
     {"n": "Video Stitching", "s": "LC 1024"},
     {"n": "Minimum Number of Refueling Stops", "s": "LC 871"},
   ],
   "traps": [
     "Jump Game II's loop stops at <code>len-1</code>. Including the last index counts one jump too many.",
     "Gas Station: if the total gas is less than the total cost there is NO answer; otherwise the answer is the index right after the lowest running deficit.",
     "'Fewest jumps' is really BFS by level — recognising that explains why the two variables are named end and furthest.",
   ]},

  {"id": "gr-pair", "name": "Sort, then pair from the ends",
   "when": "Match items against each other to minimise count or maximise value.",
   "tool": "sort, then two pointers from both ends",
   "invariant": "the current extremes are always each other's best available partner",
   "cx": "O(n log n)",
   "code": """def num_rescue_boats(people, limit):
    people.sort()
    l, r, boats = 0, len(people) - 1, 0
    while l <= r:
        if people[l] + people[r] <= limit:
            l += 1                        # the lightest rides along with the heaviest
        r -= 1                             # the heaviest always leaves, alone or paired
        boats += 1
    return boats""",
   "asks": [
     "boats to save people",
     "assign cookies to children; two city scheduling",
     "maximum number of pairs under a sum limit",
     "minimise the maximum pair sum in an array",
     "advantage shuffle (play your weakest card that still beats theirs)",
     "array partition, maximum sum of min pairs",
   ],
   "examples": [
     {"n": "Boats to Save People", "s": "LC 881"},
     {"n": "Assign Cookies", "s": "LC 455"},
     {"n": "Minimize Maximum Pair Sum in Array", "s": "LC 1877"},
     {"n": "Two City Scheduling", "s": "LC 1029"},
     {"n": "Advantage Shuffle", "s": "LC 870"},
   ],
   "traps": [
     "The heaviest person always leaves on this trip — so <code>r</code> decrements unconditionally, while <code>l</code> only advances if the pairing fits.",
     "<code>while l &lt;= r</code>, so the middle person still gets a boat.",
     "Two City Scheduling sorts by the DIFFERENCE between the two costs, not by either cost.",
   ]},

  {"id": "gr-local", "name": "Spend the budget on the best thing now",
   "when": "A sequence of steps, each consuming a resource, where the best immediate value is provably safe.",
   "tool": "sort or a heap, plus a running budget; sometimes a swap-out when something better appears",
   "invariant": "the set you hold is the best possible set of its size for the prefix seen so far",
   "cx": "O(n log n)",
   "code": """import heapq
def max_events(events):                  # attend the most events, one per day
    events.sort()                        # by start day
    h, day, i, count = [], 0, 0, 0
    while h or i < len(events):
        if not h:
            day = max(day, events[i][0])
        while i < len(events) and events[i][0] <= day:
            heapq.heappush(h, events[i][1]); i += 1     # all events open today
        heapq.heappop(h)                 # attend the one ending SOONEST
        count += 1; day += 1
        while h and h[0] < day:
            heapq.heappop(h)             # expired, can never be attended
    return count""",
   "asks": [
     "maximum number of events that can be attended",
     "task scheduler with cooldown; reorganise string",
     "IPO — maximise capital with k projects",
     "course schedule III — take the most courses before their deadlines (swap out the longest)",
     "minimum cost to hire k workers; maximum performance of a team",
     "candy, partition labels, remove k digits (the stack form)",
     "largest number from a list (custom comparator)",
   ],
   "examples": [
     {"n": "Maximum Number of Events That Can Be Attended", "s": "LC 1353"},
     {"n": "Task Scheduler", "s": "LC 621"},
     {"n": "IPO", "s": "LC 502"},
     {"n": "Course Schedule III", "s": "LC 630"},
     {"n": "Maximum Performance of a Team", "s": "LC 1383"},
     {"n": "Candy", "s": "LC 135"},
   ],
   "traps": [
     "'Swap out the worst thing I already took' (Course Schedule III) is a greedy that needs a heap — a plain sort cannot undo a choice.",
     "Say the exchange argument out loud before coding. If you cannot, write the DP.",
     "Sorting by the wrong key is the usual failure, and it still passes the samples. Decide the key from the proof, not from the example.",
   ]},
 ]},
]
