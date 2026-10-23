# -*- coding: utf-8 -*-
"""
THE PATTERN LIBRARY  --  content for the Learn half of "8 - Pattern Radar".

The idea this encodes: the data structures are few, the patterns on them are few, and the
VARIANTS inside each pattern are a closed, listable set. Every question an OA can ask is one
of those variants wearing a story. So each variant here carries:

    when      the condition in the statement that selects THIS variant
    tool      the thing you hold while scanning (running sum, deque, hashmap, heap...)
    invariant what stays true every single step -- the reason it is correct
    code      the template, in Python, short enough to retype from memory
    asks      THE FIXED LIST of question families that can be built on this variant
    examples  real problems, named, so you can go solve the clean version
    traps     what actually breaks it in an exam

Edit this file, then run:  python build_radar.py
That injects the library into the HTML (which stays self-contained and works offline).
"""

GROUPS = [
    {"id": "linear", "name": "Arrays & strings",
     "note": "One index moving left to right. Nine patterns cover almost every OA question that is not a graph or a DP."},
    {"id": "list", "name": "Linked lists",
     "note": "Pointer surgery. Small, fixed, and heavily asked in interviews."},
    {"id": "tree", "name": "Trees",
     "note": "Recursion with a shape. Almost everything is one of two traversals."},
    {"id": "graph", "name": "Graphs & grids",
     "note": "A grid is a graph. Pick the traversal from the edge weights."},
    {"id": "dp", "name": "Dynamic programming",
     "note": "A choice at every step, with overlapping subproblems. The state is the whole battle."},
    {"id": "search", "name": "Search & greedy",
     "note": "When you must try everything, and when one pass of local choices is provably enough."},
]

PATTERNS = []

# =====================================================================================
#  BATCH 1 -- the linear core
# =====================================================================================

PATTERNS += [

# ---------------------------------------------------------------- two pointers ------
{
 "id": "two-pointers", "group": "linear", "name": "Two pointers",
 "buys": "O(n²) over every pair → O(n), by never looking at a pair you have already ruled out",
 "lives": "array, string, linked list",
 "core": "Two indices walk the sequence. Each step, what you read tells you which pointer to move "
         "— and moving it discards a whole block of pairs you now know cannot be the answer. "
         "Both pointers together travel at most 2n steps, so the scan is O(n).",
 "recognise": [
   {"cue": "the array is <b>already sorted</b> (or you are allowed to sort) and you want a pair / triplet",
    "note": "sortedness is what makes 'move left or right' a decision instead of a guess"},
   {"cue": "<b>palindrome</b>, reverse, or 'compare the two ends'", "note": "ends-inward is the whole pattern"},
   {"cue": "<b>in-place</b>: remove / move / dedupe without extra memory",
    "note": "a slow write pointer and a fast read pointer"},
   {"cue": "<b>two sorted sequences</b> to merge, intersect, or diff", "note": "one pointer per sequence"},
   {"cue": "cycle, middle, or k-th from the end of a <b>linked list</b>", "note": "slow and fast at different speeds"},
 ],
 "notwhen": [
   "Unsorted and you only need existence of a pair → <b>hashmap</b> in one pass beats sorting.",
   "You need the <b>count</b> of subarrays, not a pair → prefix sum + hashmap.",
   "The window must stay contiguous and you track an aggregate inside it → that is a <b>sliding window</b> "
   "(same two indices, different job: a window keeps a running state, two pointers just compare).",
 ],
 "pick": [
   {"if": "sorted, and you want a pair / triplet hitting a target", "then": "tp-ends"},
   {"if": "compare front against back (palindrome, reverse, container)", "then": "tp-ends"},
   {"if": "rewrite the array in place, keeping some elements", "then": "tp-write"},
   {"if": "two separate sorted lists", "then": "tp-merge"},
   {"if": "three buckets to segregate in one pass", "then": "tp-partition"},
 ],
 "variants": [
  {"id": "tp-ends", "name": "Opposite ends, closing in",
   "when": "The sequence is sorted (or symmetric) and the answer is a PAIR.",
   "tool": "l = 0, r = n-1; compare the pair's value against the target and move the end that can help",
   "invariant": "every pair outside [l, r] has already been proved impossible",
   "cx": "O(n) after sorting — O(n log n) overall if you had to sort",
   "code": """def two_sum_sorted(a, target):
    l, r = 0, len(a) - 1
    while l < r:
        s = a[l] + a[r]
        if s == target:
            return [l, r]
        if s < target:
            l += 1          # need bigger -> only the left can grow
        else:
            r -= 1          # need smaller -> only the right can shrink
    return []""",
   "asks": [
     "pair with a given sum in a sorted array",
     "3Sum / 4Sum — fix one index, two-pointer the rest",
     "3Sum closest — same walk, track the best difference",
     "count pairs with sum < / > / between targets",
     "valid palindrome (with or without skipping non-alphanumerics, with one deletion allowed)",
     "reverse an array / string / vowels in place",
     "container with most water, trapping rain water (two-pointer form)",
     "squares of a sorted array (largest magnitude sits at an end)",
     "backspace string compare (walk both from the back)",
   ],
   "examples": [
     {"n": "Two Sum II — Input Array Is Sorted", "s": "LC 167"},
     {"n": "3Sum", "s": "LC 15"}, {"n": "3Sum Closest", "s": "LC 16"},
     {"n": "Container With Most Water", "s": "LC 11"},
     {"n": "Trapping Rain Water", "s": "LC 42"},
     {"n": "Valid Palindrome II", "s": "LC 680"},
     {"n": "Squares of a Sorted Array", "s": "LC 977"},
   ],
   "traps": [
     "In 3Sum you must skip duplicates at <i>both</i> the fixed index and after a hit, or you emit the same triplet twice.",
     "Sorting destroys the original indices. If the answer wants indices, use a hashmap instead.",
     "<code>while l &lt; r</code>, not <code>&lt;=</code>, whenever an element may not pair with itself.",
   ]},

  {"id": "tp-write", "name": "Same direction — read fast, write slow",
   "when": "Rewrite the array in place: remove, dedupe, move, compact. O(1) extra space is demanded.",
   "tool": "write = 0 (next slot to fill); read scans everything and copies only the keepers",
   "invariant": "a[0:write] is the finished answer at all times; everything at or past write is scratch",
   "cx": "O(n) time, O(1) space",
   "code": """def remove_val(a, val):
    write = 0
    for read in range(len(a)):
        if a[read] != val:        # the keep-test is the ONLY thing that changes
            a[write] = a[read]
            write += 1
    return write                  # new logical length""",
   "asks": [
     "remove element / remove duplicates from a sorted array (keep 1, or keep at most 2)",
     "move zeroes to the end, keeping order",
     "sort array by parity, partition by a predicate",
     "compress / run-length encode a character array in place",
     "merge two sorted arrays in place from the BACK (write pointer starts at the end)",
     "is subsequence — one pointer per string, advance only on a match",
   ],
   "examples": [
     {"n": "Remove Duplicates from Sorted Array", "s": "LC 26"},
     {"n": "Remove Duplicates II (keep two)", "s": "LC 80"},
     {"n": "Move Zeroes", "s": "LC 283"},
     {"n": "Merge Sorted Array (in place)", "s": "LC 88"},
     {"n": "Is Subsequence", "s": "LC 392"},
     {"n": "String Compression", "s": "LC 443"},
   ],
   "traps": [
     "'Keep at most two duplicates' is the same template with the test <code>write &lt; 2 or a[read] != a[write-2]</code>.",
     "Merging into an array that already has room: fill from the back, or you overwrite unread values.",
     "Return the length, not the array — these problems grade the prefix only.",
   ]},

  {"id": "tp-merge", "name": "One pointer per sequence",
   "when": "Two (or k) sorted sequences, and you walk them together.",
   "tool": "i on the first, j on the second; advance whichever side is behind",
   "invariant": "everything before i and j has been consumed in sorted order",
   "cx": "O(n + m)",
   "code": """def intersect_sorted(a, b):
    i = j = 0
    out = []
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            out.append(a[i]); i += 1; j += 1
        elif a[i] < b[j]:
            i += 1            # a[i] can never appear later in b
        else:
            j += 1
    return out""",
   "asks": [
     "merge two sorted arrays / lists",
     "intersection or union of two sorted arrays",
     "find the median of two sorted arrays (small n — the O(log) version is binary search on partition)",
     "interval list intersections",
     "smallest range / closest pair across two arrays",
     "add two numbers stored as digit arrays",
   ],
   "examples": [
     {"n": "Merge Two Sorted Lists", "s": "LC 21"},
     {"n": "Intersection of Two Arrays II", "s": "LC 350"},
     {"n": "Interval List Intersections", "s": "LC 986"},
     {"n": "Find the Median of Two Sorted Arrays", "s": "LC 4 — see binary search on partition"},
   ],
   "traps": [
     "After the main loop, one sequence still has a tail. Append it, or you silently drop elements.",
     "Equal values: decide once whether you advance one pointer or both, and whether duplicates count.",
   ]},

  {"id": "tp-partition", "name": "Three-way partition (Dutch flag)",
   "when": "Segregate into three buckets in ONE pass, in place.",
   "tool": "low, mid, high — mid scans; swap to low or high depending on the bucket",
   "invariant": "[0,low) is bucket 0, [low,mid) is bucket 1, (high,n) is bucket 2, and [mid,high] is unknown",
   "cx": "O(n) time, O(1) space, one pass",
   "code": """def sort_colors(a):
    low = mid = 0
    high = len(a) - 1
    while mid <= high:
        if a[mid] == 0:
            a[low], a[mid] = a[mid], a[low]; low += 1; mid += 1
        elif a[mid] == 2:
            a[mid], a[high] = a[high], a[mid]; high -= 1   # do NOT advance mid
        else:
            mid += 1""",
   "asks": [
     "sort an array of 0s, 1s and 2s in one pass",
     "partition around a pivot (the quickselect / quicksort step)",
     "k-th largest element via quickselect, average O(n)",
     "segregate negatives and positives, evens and odds",
     "wiggle sort, partition-then-interleave problems",
   ],
   "examples": [
     {"n": "Sort Colors", "s": "LC 75"},
     {"n": "Kth Largest Element in an Array", "s": "LC 215 — quickselect"},
     {"n": "Partition Array According to Given Pivot", "s": "LC 2161"},
   ],
   "traps": [
     "After swapping with <code>high</code> you must NOT advance <code>mid</code> — the value you just pulled in is unexamined.",
     "<code>while mid &lt;= high</code>, not <code>&lt;</code>, or you leave the last element unsorted.",
   ]},
 ]},

# --------------------------------------------------------------- sliding window -----
{
 "id": "sliding-window", "group": "linear", "name": "Sliding window",
 "buys": "O(n²) over every subarray → O(n), by never rebuilding a window from scratch",
 "lives": "array, string — always CONTIGUOUS",
 "core": "A window [l, r] carries a running state (a sum, a count map, a deque). r always moves forward; "
         "l only moves forward too. Because neither pointer ever goes back, every index enters once and "
         "leaves once — 2n moves total, O(n), no matter how clever the condition inside is.",
 "recognise": [
   {"cue": "<b>contiguous</b> subarray or substring", "note": "the one non-negotiable tell"},
   {"cue": "<b>longest / shortest / maximum / minimum</b> such that a rule holds", "note": "variable size"},
   {"cue": "<b>at most K</b> / no more than K / at least K", "note": "the classic shrink condition"},
   {"cue": "<b>every window of size k</b>, 'exactly k consecutive'", "note": "fixed size"},
   {"cue": "<b>anagram / permutation</b> of a pattern inside a string", "note": "fixed size = len(pattern), compare count maps"},
 ],
 "notwhen": [
   "<b>Subsequence</b> (order kept, gaps allowed) — a window cannot skip. That is DP.",
   "The array has <b>negatives</b> and you want a sum equal to K — shrinking no longer makes the sum smaller, "
   "so the window logic collapses. Use <b>prefix sum + hashmap</b>.",
   "You may <b>reorder</b> the elements → sort / greedy / counting, not a window.",
 ],
 "pick": [
   {"if": "the length k is given to you", "then": "sw-fixed"},
   {"if": "longest window that satisfies a rule", "then": "sw-longest"},
   {"if": "shortest window that satisfies a rule", "then": "sw-shortest"},
   {"if": "count of subarrays with EXACTLY k of something", "then": "sw-exact"},
   {"if": "you need the max or min INSIDE each window", "then": "sw-deque"},
 ],
 "variants": [
  {"id": "sw-fixed", "name": "Fixed size k",
   "when": "The statement hands you the window length: 'of size k', 'every k consecutive', 'an anagram of p'.",
   "tool": "a running aggregate — add the entering element, remove the leaving one",
   "invariant": "the window is exactly k wide from index k-1 onward",
   "cx": "O(n) time; O(1) space for a sum, O(k) for a count map",
   "code": """def max_sum_k(a, k):
    s = sum(a[:k])              # build the first window once
    best = s
    for r in range(k, len(a)):
        s += a[r] - a[r - k]    # one in, one out
        best = max(best, s)
    return best""",
   "asks": [
     "maximum / minimum sum or average of a subarray of size k",
     "count windows of size k whose average or sum beats a threshold",
     "find all anagrams of p in s; permutation of p in s (k = len(p), compare frequency maps)",
     "maximum vowels in a substring of length k",
     "k-beauty of a number (substrings of length k that divide it)",
     "maximum points from k cards taken from either end (a fixed window on the WRAPPED array, or total minus a window of n-k)",
     "max consecutive ones / repeated DNA sequences of fixed length",
   ],
   "examples": [
     {"n": "Maximum Average Subarray I", "s": "LC 643"},
     {"n": "Find All Anagrams in a String", "s": "LC 438"},
     {"n": "Permutation in String", "s": "LC 567"},
     {"n": "Maximum Number of Vowels in a Substring of Given Length", "s": "LC 1456"},
     {"n": "Find the K-Beauty of a Number", "s": "LC 2269 — in your own notes"},
     {"n": "Maximum Points You Can Obtain from Cards", "s": "LC 1423"},
     {"n": "Number of Sub-arrays of Size K and Avg ≥ Threshold", "s": "LC 1343"},
   ],
   "traps": [
     "Build the first window BEFORE the loop, then slide — or handle r &lt; k-1 inside it. Mixing the two is the usual bug.",
     "Remove the leaving element <i>every</i> iteration, including when it does not change the answer.",
     "Guard k &gt; n.",
     "For anagrams compare counts, not sorted strings — sorting each window is O(n k log k).",
   ]},

  {"id": "sw-longest", "name": "Variable size — longest valid",
   "when": "'Longest / maximum length' subarray or substring such that some rule holds.",
   "tool": "grow r always; <code>while</code> the window is INVALID, shrink from l; record after it is valid again",
   "invariant": "after the while-loop the window is always valid, so r-l+1 is a legal candidate",
   "cx": "O(n) time, O(k) space for the state",
   "code": """def longest_at_most_k_distinct(s, k):
    from collections import defaultdict
    cnt = defaultdict(int)
    l = best = 0
    for r, ch in enumerate(s):
        cnt[ch] += 1
        while len(cnt) > k:            # WHILE, not if
            cnt[s[l]] -= 1
            if cnt[s[l]] == 0:
                del cnt[s[l]]
            l += 1
        best = max(best, r - l + 1)    # window is valid here
    return best""",
   "asks": [
     "longest substring without repeating characters",
     "longest substring with at most K distinct characters (K = 2 is 'fruit into baskets')",
     "longest substring with at most K replacements of one character (character replacement)",
     "max consecutive ones after flipping at most k zeroes",
     "longest subarray with sum ≤ S (positives only)",
     "longest subarray where max - min ≤ limit (needs two deques — see the deque variant)",
     "longest nice / balanced substring under a counting rule",
     "longest subarray of 1s after deleting exactly one element",
   ],
   "examples": [
     {"n": "Longest Substring Without Repeating Characters", "s": "LC 3"},
     {"n": "Longest Substring with At Most K Distinct Characters", "s": "LC 340"},
     {"n": "Longest Repeating Character Replacement", "s": "LC 424"},
     {"n": "Max Consecutive Ones III", "s": "LC 1004"},
     {"n": "Fruit Into Baskets", "s": "LC 904"},
     {"n": "Longest Subarray of 1's After Deleting One Element", "s": "LC 1493"},
     {"n": "Longest Continuous Subarray With Absolute Diff ≤ Limit", "s": "LC 1438"},
   ],
   "traps": [
     "<code>while</code>, never <code>if</code> — one entering element can force several exits.",
     "Record the answer AFTER shrinking, not during.",
     "Delete the key when its count hits zero, or <code>len(cnt)</code> lies to you.",
     "In 'character replacement' the window cost is <code>len - maxFreq</code>; keeping maxFreq stale is a known-safe shortcut, "
     "but only because the answer never shrinks.",
   ]},

  {"id": "sw-shortest", "name": "Variable size — shortest valid",
   "when": "'Minimum length' / 'shortest' subarray or substring that satisfies a rule.",
   "tool": "grow r; <code>while</code> the window IS valid, record the answer and shrink from l",
   "invariant": "you record only from valid windows, and you keep shrinking while it stays valid, so every "
                "recorded candidate is minimal for its right end",
   "cx": "O(n) time",
   "code": """def min_len_sum_at_least(a, target):
    l = s = 0
    best = float('inf')
    for r, x in enumerate(a):
        s += x
        while s >= target:              # valid -> try to make it smaller
            best = min(best, r - l + 1)
            s -= a[l]; l += 1
    return 0 if best == float('inf') else best""",
   "asks": [
     "minimum size subarray with sum ≥ target (positives only)",
     "minimum window substring containing all characters of t (with multiplicity)",
     "shortest subarray to remove to make the rest sorted",
     "minimum operations to reduce x to zero (rephrase as the LONGEST middle window with sum = total - x)",
     "smallest window containing all distinct characters of the string itself",
     "minimum swaps to group all 1s together (fixed window of size = count of ones)",
   ],
   "examples": [
     {"n": "Minimum Size Subarray Sum", "s": "LC 209"},
     {"n": "Minimum Window Substring", "s": "LC 76"},
     {"n": "Minimum Operations to Reduce X to Zero", "s": "LC 1658"},
     {"n": "Minimum Swaps to Group All 1's Together II", "s": "LC 2134"},
     {"n": "Shortest Subarray with Sum at Least K", "s": "LC 862 — has negatives, needs prefix + deque"},
   ],
   "traps": [
     "With NEGATIVE numbers 'sum ≥ K' is no longer a window problem — shrinking can increase the sum. "
     "Switch to prefix sums + a monotonic deque (LC 862).",
     "Minimum-window-substring needs a 'how many required chars are satisfied' counter, not a map comparison per step.",
     "Return 0 (or -1) for 'no valid window', not infinity.",
   ]},

  {"id": "sw-exact", "name": "Exactly K — atMost(K) − atMost(K−1)",
   "when": "You are asked to COUNT subarrays with exactly K of something.",
   "tool": "the longest-valid template, reused twice, counting windows instead of measuring them",
   "invariant": "for each r, <code>r - l + 1</code> is the number of valid windows ending at r — summing that counts them all",
   "cx": "O(n), two passes",
   "code": """def count_at_most(a, k, ok):            # ok = the 'at most' predicate's state update
    from collections import defaultdict
    cnt = defaultdict(int)
    l = total = 0
    for r, x in enumerate(a):
        cnt[x] += 1
        while len(cnt) > k:
            cnt[a[l]] -= 1
            if cnt[a[l]] == 0: del cnt[a[l]]
            l += 1
        total += r - l + 1              # every window ending at r is valid
    return total

def count_exactly(a, k):
    return count_at_most(a, k) - count_at_most(a, k - 1)""",
   "asks": [
     "subarrays with exactly K distinct integers",
     "binary subarrays with sum exactly equal to goal",
     "count 'nice' subarrays — exactly k odd numbers",
     "count substrings containing all three characters a, b, c (that is 'at least', = total − atMost(2 kinds))",
     "number of substrings with exactly k unique characters",
   ],
   "examples": [
     {"n": "Subarrays with K Different Integers", "s": "LC 992"},
     {"n": "Binary Subarrays With Sum", "s": "LC 930 — also solvable with prefix + hashmap, in your notes"},
     {"n": "Count Number of Nice Subarrays", "s": "LC 1248"},
     {"n": "Number of Substrings Containing All Three Characters", "s": "LC 1358"},
   ],
   "traps": [
     "You cannot maintain 'exactly K' with one window — it is not monotonic, so there is nothing to shrink on. "
     "The subtraction trick exists precisely because of that.",
     "<code>total += r - l + 1</code> counts windows; <code>best = max(best, r-l+1)</code> measures one. Do not mix them up.",
     "For a 0/1 array, prefix sum + hashmap gives the same answer in one pass — either is accepted.",
   ]},

  {"id": "sw-deque", "name": "Monotonic deque inside the window",
   "when": "You need the MAX or MIN of each window, and recomputing it is O(k) per step.",
   "tool": "a deque of INDICES whose values are monotonically decreasing (for max) — front is the answer",
   "invariant": "the deque holds exactly the indices that could still be the window max, newest last",
   "cx": "O(n) — each index is pushed once and popped once",
   "code": """from collections import deque
def max_sliding_window(a, k):
    dq, out = deque(), []            # dq holds INDICES, values decreasing
    for r, x in enumerate(a):
        while dq and a[dq[-1]] <= x:
            dq.pop()                 # x is newer AND bigger -> they can never win
        dq.append(r)
        if dq[0] <= r - k:
            dq.popleft()             # front fell out of the window
        if r >= k - 1:
            out.append(a[dq[0]])
    return out""",
   "asks": [
     "sliding window maximum / minimum",
     "longest subarray with max − min ≤ limit (one max-deque + one min-deque)",
     "shortest subarray with sum at least K, WITH negatives (deque over prefix sums)",
     "constrained subsequence sum, jump game VI (deque over a DP array)",
     "maximum of all subarrays of every size (histogram variant — monotonic stack instead)",
   ],
   "examples": [
     {"n": "Sliding Window Maximum", "s": "LC 239"},
     {"n": "Longest Continuous Subarray With Absolute Diff ≤ Limit", "s": "LC 1438"},
     {"n": "Shortest Subarray with Sum at Least K", "s": "LC 862"},
     {"n": "Jump Game VI", "s": "LC 1696"},
     {"n": "Constrained Subsequence Sum", "s": "LC 1425"},
   ],
   "traps": [
     "Store indices, not values — you cannot tell when a value expires otherwise.",
     "Pop the expired FRONT every iteration, and pop smaller elements from the BACK before pushing.",
     "<code>&lt;=</code> versus <code>&lt;</code> when popping the back only matters for duplicates and for which index you report.",
   ]},
 ]},

# ------------------------------------------------------------------- prefix sum -----
{
 "id": "prefix-sum", "group": "linear", "name": "Prefix sum",
 "buys": "O(n) per range query → O(1), after one O(n) precomputation",
 "lives": "array (numbers), and any string you can turn into ±1 or a bitmask",
 "core": "pre[i] = the total of everything BEFORE i. Then any range sum is one subtraction: "
         "sum(l..r) = pre[r+1] - pre[l]. The leap is the next step: if you want 'how many ranges sum to K', "
         "rearrange it to pre[r+1] - K = pre[l] and ask a HASHMAP how many earlier prefixes had that value.",
 "recognise": [
   {"cue": "<b>repeated range-sum queries</b> on a fixed array", "note": "plain prefix array"},
   {"cue": "contiguous + <b>sum equals K</b> + negatives allowed", "note": "prefix + hashmap — the signature combination"},
   {"cue": "<b>divisible by K</b>, 'multiple of k'", "note": "hash the remainder, not the sum"},
   {"cue": "<b>equal number of</b> two things", "note": "map one to +1 and the other to −1, then it is sum = 0"},
   {"cue": "<b>range updates</b>, many of them, queried only at the end", "note": "difference array"},
   {"cue": "product / min / max over a prefix, or 'everything except me'", "note": "prefix-and-suffix pass"},
 ],
 "notwhen": [
   "All values are positive and you want the LONGEST or SHORTEST range → a <b>sliding window</b> is simpler and O(1) space.",
   "The array changes between queries → you need a Fenwick / segment tree, not a static prefix.",
   "You want the max subarray sum → that is <b>Kadane</b> (or prefix minus running-min, same thing).",
 ],
 "pick": [
   {"if": "just answer range sums fast", "then": "ps-range"},
   {"if": "COUNT subarrays matching a sum rule", "then": "ps-count"},
   {"if": "find the LONGEST / shortest subarray matching a sum rule", "then": "ps-longest"},
   {"if": "the grid is 2-D", "then": "ps-2d"},
   {"if": "many range add operations, one read at the end", "then": "ps-diff"},
   {"if": "'product of all except self', or you need info from both sides", "then": "ps-suffix"},
 ],
 "variants": [
  {"id": "ps-range", "name": "Plain prefix array (range sums)",
   "when": "Many queries, array never changes.",
   "tool": "pre[0] = 0; pre[i+1] = pre[i] + a[i]",
   "invariant": "pre[i] is always the sum of a[0:i] — note the off-by-one is deliberate, it kills the l=0 special case",
   "cx": "O(n) build, O(1) per query",
   "code": """def build(a):
    pre = [0] * (len(a) + 1)
    for i, x in enumerate(a):
        pre[i + 1] = pre[i] + x
    return pre

def range_sum(pre, l, r):      # inclusive l..r
    return pre[r + 1] - pre[l]""",
   "asks": [
     "range sum query — immutable (1-D and 2-D)",
     "running sum of an array",
     "find the pivot / equilibrium index where left sum = right sum",
     "number of ways to split an array into parts with equal sums",
     "average of every prefix, 'minimum value to get positive step by step sum'",
   ],
   "examples": [
     {"n": "Range Sum Query — Immutable", "s": "LC 303"},
     {"n": "Find Pivot Index", "s": "LC 724"},
     {"n": "Running Sum of 1d Array", "s": "LC 1480"},
     {"n": "Minimum Value to Get Positive Step by Step Sum", "s": "LC 1413"},
   ],
   "traps": [
     "Use the size n+1 form with pre[0]=0. The size-n form forces an <code>if l == 0</code> branch everywhere.",
     "Inclusive vs exclusive ends — settle it once, write it in a comment, never re-derive mid-exam.",
   ]},

  {"id": "ps-count", "name": "Prefix + hashmap — COUNT the subarrays",
   "when": "'How many subarrays sum to K / are divisible by K / have equal counts.' Negatives allowed.",
   "tool": "a dict of prefix-value → how many times it has been seen, seeded with {0: 1}",
   "invariant": "when you are at r, the dict holds every prefix strictly before the current one, so each hit is a real subarray",
   "cx": "O(n) time, O(n) space",
   "code": """def subarray_sum_equals_k(a, k):
    seen = {0: 1}                  # the empty prefix -- this seed IS the pattern
    pre = res = 0
    for x in a:
        pre += x
        res += seen.get(pre - k, 0)      # how many earlier prefixes make the gap = k
        seen[pre] = seen.get(pre, 0) + 1
    return res""",
   "asks": [
     "count subarrays with sum exactly K (negatives allowed)",
     "count subarrays with sum divisible by K — hash <code>pre % k</code>, and in Python <code>%</code> already returns non-negative",
     "count binary subarrays with sum = goal",
     "count nice subarrays (k odd numbers) — map odd→1, even→0",
     "count subarrays with equal numbers of two symbols — map to +1 / −1 and count sum = 0",
     "count subarrays with a given XOR — identical template with xor in place of sum",
   ],
   "examples": [
     {"n": "Subarray Sum Equals K", "s": "LC 560 — in your own notes"},
     {"n": "Subarray Sums Divisible by K", "s": "LC 974"},
     {"n": "Binary Subarrays With Sum", "s": "LC 930 — in your own notes"},
     {"n": "Count Number of Nice Subarrays", "s": "LC 1248"},
     {"n": "Count Subarrays With Score Less Than K", "s": "LC 2302 — window, not prefix: compare the two"},
   ],
   "traps": [
     "<code>seen = {0: 1}</code> is not decoration — without it you miss every subarray that starts at index 0.",
     "Count the occurrences, do not just store a boolean, or you undercount repeats.",
     "Record <code>seen[pre]</code> AFTER reading the answer, or a zero-length subarray counts itself.",
   ]},

  {"id": "ps-longest", "name": "Prefix + hashmap — LONGEST / shortest subarray",
   "when": "Same rearrangement, but you want a length, not a count.",
   "tool": "a dict of prefix-value → its FIRST index (seeded {0: -1}); never overwrite",
   "invariant": "the earliest index for each prefix value gives the longest reach to the current r",
   "cx": "O(n) time, O(n) space",
   "code": """def longest_sum_k(a, k):
    first = {0: -1}                  # prefix value -> earliest index
    pre = best = 0
    for i, x in enumerate(a):
        pre += x
        if pre - k in first:
            best = max(best, i - first[pre - k])
        if pre not in first:         # FIRST occurrence only -> longest span
            first[pre] = i
    return best""",
   "asks": [
     "longest subarray with sum K (negatives allowed)",
     "contiguous array — longest subarray with equal 0s and 1s (map 0 → −1)",
     "longest subarray divisible by K; continuous subarray sum that is a multiple of k, length ≥ 2 (store the index of each remainder)",
     "longest substring where every vowel appears an even number of times (prefix of a 5-bit MASK)",
     "smallest subarray to remove so the rest is divisible by p (store the latest index instead, to get the shortest)",
     "maximum size subarray sum equals k",
   ],
   "examples": [
     {"n": "Contiguous Array", "s": "LC 525 — in your own notes"},
     {"n": "Continuous Subarray Sum", "s": "LC 523 — in your own notes"},
     {"n": "Find Longest Awesome Substring", "s": "LC 1542 — bitmask prefix"},
     {"n": "Find the Longest Substring Containing Vowels in Even Counts", "s": "LC 1371 — in your own notes"},
     {"n": "Make Sum Divisible by P", "s": "LC 1590 — in your own notes, shortest variant"},
     {"n": "Maximum Size Subarray Sum Equals k", "s": "LC 325"},
   ],
   "traps": [
     "LONGEST → keep the FIRST index. SHORTEST → keep the LATEST. Getting this backwards is the classic silent wrong answer.",
     "<code>{0: -1}</code> so a subarray starting at index 0 has the right length.",
     "The 'length ≥ 2' clause in LC 523 is why you store indices rather than counts.",
   ]},

  {"id": "ps-2d", "name": "2-D prefix sum (integral image)",
   "when": "A matrix, and repeated submatrix-sum queries.",
   "tool": "pre[i+1][j+1] = a[i][j] + pre[i][j+1] + pre[i+1][j] − pre[i][j]",
   "invariant": "pre[i][j] is the sum of the whole rectangle above-and-left of (i, j), exclusive",
   "cx": "O(rows·cols) build, O(1) per query",
   "code": """def build2d(g):
    R, C = len(g), len(g[0])
    pre = [[0] * (C + 1) for _ in range(R + 1)]
    for i in range(R):
        for j in range(C):
            pre[i+1][j+1] = g[i][j] + pre[i][j+1] + pre[i+1][j] - pre[i][j]
    return pre

def rect(pre, r1, c1, r2, c2):        # inclusive corners
    return pre[r2+1][c2+1] - pre[r1][c2+1] - pre[r2+1][c1] + pre[r1][c1]""",
   "asks": [
     "range sum query 2-D — immutable",
     "count submatrices that sum to a target (fix two rows, then it becomes the 1-D count problem)",
     "maximum side length of a square with sum ≤ threshold (binary search the side + 2-D prefix)",
     "matrix block sum, 'number of 1s in a submatrix'",
     "maximal square / largest all-ones rectangle (usually DP, but prefix sums also work)",
   ],
   "examples": [
     {"n": "Range Sum Query 2D — Immutable", "s": "LC 304"},
     {"n": "Number of Submatrices That Sum to Target", "s": "LC 1074"},
     {"n": "Maximum Side Length of a Square with Sum ≤ Threshold", "s": "LC 1292"},
     {"n": "Matrix Block Sum", "s": "LC 1314"},
   ],
   "traps": [
     "Inclusion–exclusion: subtract the two strips, then ADD BACK the corner you removed twice.",
     "Pad with a zero row and column. Without the pad every query needs boundary ifs.",
   ]},

  {"id": "ps-diff", "name": "Difference array (range updates)",
   "when": "Many 'add v to everything in [l, r]' operations, and you only read the array at the end.",
   "tool": "diff[l] += v; diff[r+1] -= v; then one prefix sum rebuilds the array",
   "invariant": "the prefix sum of diff is exactly the accumulated array at any point",
   "cx": "O(1) per update, O(n) once to materialise",
   "code": """def apply_ranges(n, ops):              # ops = [(l, r, v), ...]
    diff = [0] * (n + 1)
    for l, r, v in ops:
        diff[l] += v
        diff[r + 1] -= v               # the +1 slot is why diff has n+1 cells
    out, run = [], 0
    for i in range(n):
        run += diff[i]
        out.append(run)
    return out""",
   "asks": [
     "range addition, 'corporate flight bookings'",
     "car pooling / meeting rooms as a timeline of +1 and −1 events",
     "can all N bookings be served without exceeding capacity",
     "number of people in a building at each hour, 'maximum population year'",
     "'shift letters by ranges', apply many range increments to a string",
     "check if the array can be made all-zero with range decrements",
   ],
   "examples": [
     {"n": "Corporate Flight Bookings", "s": "LC 1109"},
     {"n": "Car Pooling", "s": "LC 1094"},
     {"n": "Range Addition", "s": "LC 370"},
     {"n": "Shifting Letters II", "s": "LC 2381"},
   ],
   "traps": [
     "Size the diff array n+1, or <code>diff[r+1]</code> overflows on the last range.",
     "This is the same object as a sweep line over +1 / −1 events — recognise them as one pattern.",
   ]},

  {"id": "ps-suffix", "name": "Prefix AND suffix pass",
   "when": "Each position needs to know about everything on its left AND everything on its right.",
   "tool": "two passes — one left to right carrying a running value, one right to left",
   "invariant": "after pass one, cell i holds the aggregate of everything strictly left of i",
   "cx": "O(n) time; O(1) extra if you write into the output array",
   "code": """def product_except_self(a):
    n = len(a)
    out = [1] * n
    left = 1
    for i in range(n):
        out[i] = left
        left *= a[i]
    right = 1
    for i in range(n - 1, -1, -1):
        out[i] *= right
        right *= a[i]
    return out""",
   "asks": [
     "product of array except self (no division allowed)",
     "trapping rain water via prefix-max and suffix-max",
     "candy distribution — one left pass, one right pass",
     "best time to buy and sell stock with two transactions",
     "'can this index be the split point' — compare prefix aggregate with suffix aggregate",
     "maximum sum of two non-overlapping subarrays",
   ],
   "examples": [
     {"n": "Product of Array Except Self", "s": "LC 238 — in your own notes"},
     {"n": "Trapping Rain Water", "s": "LC 42"},
     {"n": "Candy", "s": "LC 135"},
     {"n": "Best Time to Buy and Sell Stock III", "s": "LC 123"},
     {"n": "Maximum Sum of Two Non-Overlapping Subarrays", "s": "LC 1031"},
   ],
   "traps": [
     "Write the left pass straight into the output array and carry only a scalar — that is how you get O(1) extra space.",
     "With division you would have to special-case zeros; the two-pass form has no such hole.",
   ]},
 ]},
]

# =====================================================================================
#  BATCH 2 -- search, lookup, and the stack/heap families
# =====================================================================================

PATTERNS += [

# ---------------------------------------------------------------- binary search ----
{
 "id": "binary-search", "group": "linear", "name": "Binary search",
 "buys": "O(n) scan → O(log n); and for 'search the answer', O(huge) → O(n log(range))",
 "lives": "any ORDERED search space — a sorted array, or the range of possible answers",
 "core": "You do not need a sorted array. You need a space where one check can throw away half of it. "
         "That means a monotonic predicate: a line of FALSE FALSE FALSE TRUE TRUE TRUE, and you are hunting "
         "the boundary. Ask yourself only this: 'if X works, does every larger X also work?' If yes, binary search.",
 "recognise": [
   {"cue": "<b>sorted</b> array, find / first / last / insert position", "note": "the classic form"},
   {"cue": "<b>minimum X such that</b> … / maximum X such that …", "note": "binary search on the answer"},
   {"cue": "<b>minimum capacity / speed / time / largest minimum / smallest maximum</b>",
    "note": "the five words that give it away every time"},
   {"cue": "constraints are <b>huge</b> (10⁹, 10¹⁴) but the CHECK is cheap and O(n)",
    "note": "you cannot enumerate answers, so you search them"},
   {"cue": "<b>rotated</b> sorted array, or a mountain / peak", "note": "still enough order to halve"},
 ],
 "notwhen": [
   "The predicate is not monotonic (works at 5, fails at 6, works at 7) — halving is then simply wrong.",
   "n is small enough that a linear scan fits the budget — do not add bug surface for nothing.",
   "You want the k-th smallest in a stream → heap, not binary search.",
 ],
 "pick": [
   {"if": "a sorted array, exact value", "then": "bs-exact"},
   {"if": "first / last occurrence, insert position, 'count of elements ≤ x'", "then": "bs-bound"},
   {"if": "'minimum/maximum X such that', huge range, cheap feasibility check", "then": "bs-answer"},
   {"if": "rotated, mountain, or otherwise locally ordered", "then": "bs-rotated"},
   {"if": "two sorted arrays and you binary search the SPLIT, not an element", "then": "bs-partition"},
 ],
 "variants": [
  {"id": "bs-exact", "name": "Classic — find the value",
   "when": "Sorted array, is x here and where.",
   "tool": "lo, hi inclusive; mid = (lo + hi) // 2",
   "invariant": "if x exists, it is always inside [lo, hi]",
   "cx": "O(log n)",
   "code": """def search(a, x):
    lo, hi = 0, len(a) - 1
    while lo <= hi:                 # inclusive bounds -> <=
        mid = (lo + hi) // 2
        if a[mid] == x:
            return mid
        if a[mid] < x:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1""",
   "asks": [
     "search in a sorted array; search a 2-D matrix (treat it as one flat sorted array)",
     "guess number higher or lower; first bad version",
     "valid perfect square, sqrt(x) by integer search",
     "search in an unknown-length / infinite sorted stream (double the bound first, then search)",
   ],
   "examples": [
     {"n": "Binary Search", "s": "LC 704"},
     {"n": "Search a 2D Matrix", "s": "LC 74"},
     {"n": "First Bad Version", "s": "LC 278"},
     {"n": "Sqrt(x)", "s": "LC 69"},
   ],
   "traps": [
     "Pick ONE convention (inclusive hi with <code>&lt;=</code>, or exclusive hi with <code>&lt;</code>) and never mix them.",
     "<code>mid = lo + (hi - lo) // 2</code> in C++/Java to dodge overflow. Python integers do not overflow, so either is fine here.",
     "Every branch must shrink the range, or you loop forever.",
   ]},

  {"id": "bs-bound", "name": "Lower / upper bound (the boundary)",
   "when": "First occurrence, last occurrence, insert position, 'how many are ≤ x'.",
   "tool": "half-open [lo, hi); shrink toward the first index where the predicate turns TRUE",
   "invariant": "everything left of lo is FALSE, everything at or right of hi is TRUE — so lo lands on the boundary",
   "cx": "O(log n)",
   "code": """def lower_bound(a, x):              # first index with a[i] >= x
    lo, hi = 0, len(a)              # half-open: hi = n, loop while lo < hi
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return lo                       # == bisect_left(a, x)

# upper_bound: swap the test to  a[mid] <= x   -> bisect_right
# count of x  = upper_bound(a, x) - lower_bound(a, x)""",
   "asks": [
     "first and last position of an element in a sorted array",
     "search insert position",
     "count of occurrences of x; count of elements less than x",
     "find K closest elements (binary search the left edge of the window)",
     "smallest element greater than target ('ceiling' / 'successor')",
     "longest increasing subsequence in O(n log n) — lower_bound into the tails array",
     "'count pairs / count values ≤ mid' as the CHECK inside a binary search on the answer",
   ],
   "examples": [
     {"n": "Find First and Last Position in Sorted Array", "s": "LC 34"},
     {"n": "Search Insert Position", "s": "LC 35"},
     {"n": "Find K Closest Elements", "s": "LC 658"},
     {"n": "Longest Increasing Subsequence", "s": "LC 300 — the O(n log n) version"},
   ],
   "traps": [
     "In Python just use <code>bisect_left</code> / <code>bisect_right</code> unless the interviewer wants the loop.",
     "lower_bound returns n when every element is smaller — check the index before dereferencing it.",
     "'Last occurrence' = upper_bound − 1, not a separate search.",
   ]},

  {"id": "bs-answer", "name": "Binary search ON THE ANSWER",
   "when": "'Minimum / maximum X such that a condition holds', the range of X is huge, and checking one X is cheap.",
   "tool": "a <code>feasible(x)</code> function that is monotonic; binary search over the VALUE range, not the array",
   "invariant": "feasible is FALSE below the boundary and TRUE at and above it (or the mirror image)",
   "cx": "O(n log(range)) — the check is O(n), the search adds a log",
   "code": """def min_feasible(lo, hi, feasible):      # feasible: False...False True...True
    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            hi = mid                 # mid might be the answer -> keep it
        else:
            lo = mid + 1
    return lo

# example: minimum eating speed so that all bananas are gone within h hours
def min_speed(piles, h):
    import math
    def feasible(k):
        return sum(math.ceil(p / k) for p in piles) <= h
    return min_feasible(1, max(piles), feasible)""",
   "asks": [
     "minimum eating speed / minimum ship capacity to finish within D days",
     "split array into m parts, minimise the largest part sum",
     "minimum days to make m bouquets",
     "magnetic force between balls / aggressive cows — maximise the minimum gap",
     "minimum time to complete trips / to finish all jobs",
     "smallest divisor given a threshold",
     "maximum number of candies / pieces each child gets",
     "kth smallest element in a sorted matrix or in a multiplication table (count how many are ≤ mid)",
     "minimise the maximum distance to a gas station (real-valued — iterate a fixed 100 times instead of exact equality)",
   ],
   "examples": [
     {"n": "Koko Eating Bananas", "s": "LC 875"},
     {"n": "Capacity To Ship Packages Within D Days", "s": "LC 1011"},
     {"n": "Split Array Largest Sum", "s": "LC 410"},
     {"n": "Minimum Number of Days to Make m Bouquets", "s": "LC 1482"},
     {"n": "Magnetic Force Between Two Balls", "s": "LC 1552"},
     {"n": "Kth Smallest Element in a Sorted Matrix", "s": "LC 378"},
     {"n": "Smallest Divisor Given a Threshold", "s": "LC 1283"},
   ],
   "traps": [
     "State the monotonicity out loud before coding: 'a bigger ship can always carry what a smaller one could'. "
     "If you cannot say that sentence, this is the wrong pattern.",
     "Set lo and hi to real bounds — lo = max(weights) not 1, when one item must fit in one trip.",
     "'Maximise the minimum' is the mirror: move <code>lo = mid</code> and use <code>mid = (lo + hi + 1) // 2</code> to avoid an infinite loop.",
     "For 'largest minimum' problems the answer is the LAST true, not the first.",
   ]},

  {"id": "bs-rotated", "name": "Rotated / mountain — locally ordered",
   "when": "Not globally sorted, but each step still tells you which half to drop.",
   "tool": "compare a[mid] with an endpoint to learn which half is clean, then test whether the target lies inside it",
   "invariant": "at least one of the two halves is always perfectly sorted",
   "cx": "O(log n) (O(n) worst case with duplicates)",
   "code": """def search_rotated(a, x):
    lo, hi = 0, len(a) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if a[mid] == x:
            return mid
        if a[lo] <= a[mid]:                      # left half is sorted
            if a[lo] <= x < a[mid]: hi = mid - 1
            else:                   lo = mid + 1
        else:                                     # right half is sorted
            if a[mid] < x <= a[hi]: lo = mid + 1
            else:                   hi = mid - 1
    return -1""",
   "asks": [
     "search in a rotated sorted array (with and without duplicates)",
     "find the minimum in a rotated sorted array / how many times it was rotated",
     "peak element; peak of a mountain array",
     "find in a mountain array (locate the peak, then two ordinary searches)",
     "single element in a sorted array where everything else appears twice (search on index parity)",
     "first element greater than itself, 'find any local maximum'",
   ],
   "examples": [
     {"n": "Search in Rotated Sorted Array", "s": "LC 33"},
     {"n": "Find Minimum in Rotated Sorted Array", "s": "LC 153"},
     {"n": "Find Peak Element", "s": "LC 162"},
     {"n": "Peak Index in a Mountain Array", "s": "LC 852"},
     {"n": "Single Element in a Sorted Array", "s": "LC 540"},
   ],
   "traps": [
     "Duplicates break the 'which half is sorted' test (a[lo] == a[mid] == a[hi]); you must shrink lo/hi by one, which is O(n) worst case.",
     "For 'find the minimum' compare against <code>a[hi]</code>, not <code>a[lo]</code> — comparing to lo fails on an unrotated array.",
     "Peak-finding needs no sortedness at all, only that neighbours differ.",
   ]},

  {"id": "bs-partition", "name": "Binary search the PARTITION",
   "when": "Two sorted arrays, and the answer is a split point rather than an element.",
   "tool": "search how many elements of the SHORTER array go to the left side; derive the rest",
   "invariant": "left side always holds exactly half the total, and every left element ≤ every right element",
   "cx": "O(log min(n, m))",
   "code": """def median_two_sorted(a, b):
    if len(a) > len(b): a, b = b, a
    n, m = len(a), len(b)
    half = (n + m + 1) // 2
    lo, hi = 0, n
    while lo <= hi:
        i = (lo + hi) // 2            # take i from a, the rest from b
        j = half - i
        aL = a[i-1] if i > 0 else float('-inf')
        aR = a[i]   if i < n else float('inf')
        bL = b[j-1] if j > 0 else float('-inf')
        bR = b[j]   if j < m else float('inf')
        if aL <= bR and bL <= aR:
            if (n + m) % 2: return max(aL, bL)
            return (max(aL, bL) + min(aR, bR)) / 2
        if aL > bR: hi = i - 1
        else:       lo = i + 1""",
   "asks": [
     "median of two sorted arrays",
     "k-th smallest element across two sorted arrays",
     "k-th smallest in a sorted matrix (the counting form is usually easier)",
     "split two arrays so both halves are balanced",
   ],
   "examples": [
     {"n": "Median of Two Sorted Arrays", "s": "LC 4"},
     {"n": "Kth Smallest Element in a Sorted Matrix", "s": "LC 378"},
   ],
   "traps": [
     "Always search the SHORTER array, or j goes out of range.",
     "The ±infinity sentinels replace four boundary ifs — write them, do not branch.",
     "This one is worth memorising rather than deriving under exam pressure.",
   ]},
 ]},

# --------------------------------------------------------------------- hashing -----
{
 "id": "hashing", "group": "linear", "name": "Hashing (map & set)",
 "buys": "O(n) search per element → O(1); so O(n²) → O(n)",
 "lives": "anything you can use as a dict key — numbers, characters, tuples, frozensets, sorted strings",
 "core": "Trade memory for time. Walk once, and at each element ask the dict a question about the PAST: "
         "have I seen this, how many times, where was it. The whole art is choosing the key — the value, "
         "the remainder, the sorted letters, the (row, col) pair, the normalised shape.",
 "recognise": [
   {"cue": "<b>have I seen this before</b> / is there a duplicate", "note": "set"},
   {"cue": "<b>how many times</b> does each thing appear", "note": "Counter / frequency map"},
   {"cue": "<b>group together</b> things that share a property", "note": "dict of key → list"},
   {"cue": "you need the <b>index</b> of the partner, not just that it exists", "note": "dict value → index"},
   {"cue": "<b>unsorted</b> input and the question is about existence", "note": "sorting would waste your O(n) budget"},
 ],
 "notwhen": [
   "Values are a small dense range 1..n → an ARRAY is a faster hashmap; and if you may mutate the input, "
   "<b>cyclic sort / index-as-hash</b> solves it in O(1) space.",
   "Input is already sorted and you want a pair → two pointers, O(1) space.",
   "You need an ORDER (smallest, k-th) → heap or sorting; a hashmap has no order.",
 ],
 "pick": [
   {"if": "existence or duplicate detection only", "then": "hs-seen"},
   {"if": "counts, 'most frequent', anagram checks", "then": "hs-freq"},
   {"if": "you must return indices or distances", "then": "hs-index"},
   {"if": "bucket items by a derived key", "then": "hs-group"},
   {"if": "values are exactly 1..n and O(1) space is demanded", "then": "hs-cyclic"},
 ],
 "variants": [
  {"id": "hs-seen", "name": "Seen-before set",
   "when": "Existence, duplicates, membership tests.",
   "tool": "a set; add as you go, test before you add",
   "invariant": "the set holds exactly the elements strictly before the current index",
   "cx": "O(n) time, O(n) space",
   "code": """def has_duplicate(a):
    seen = set()
    for x in a:
        if x in seen:
            return True
        seen.add(x)
    return False""",
   "asks": [
     "contains duplicate; contains duplicate within distance k (set of the last k, or a dict of indices)",
     "happy number, cycle detection in a sequence of states",
     "longest consecutive sequence (set membership, start only where x-1 is absent — O(n))",
     "intersection of two arrays; missing / extra element between two arrays",
     "valid sudoku (sets per row, column and box)",
     "'is this word in the dictionary' lookups inside a DP",
   ],
   "examples": [
     {"n": "Contains Duplicate", "s": "LC 217"},
     {"n": "Contains Duplicate II", "s": "LC 219 — in your own notes"},
     {"n": "Longest Consecutive Sequence", "s": "LC 128"},
     {"n": "Happy Number", "s": "LC 202"},
     {"n": "Valid Sudoku", "s": "LC 36"},
   ],
   "traps": [
     "Longest-consecutive is only O(n) because you start a walk ONLY at sequence starts. Without that check it is O(n²).",
     "Sets are unordered — never rely on iteration order for an answer.",
   ]},

  {"id": "hs-freq", "name": "Frequency map",
   "when": "Counts drive the answer: most frequent, anagram, 'can we rearrange'.",
   "tool": "<code>collections.Counter</code>, or a 26-slot list for lowercase letters",
   "invariant": "the map is the exact multiset of what you have consumed",
   "cx": "O(n) time, O(k) space for k distinct keys",
   "code": """from collections import Counter
def is_anagram(s, t):
    return len(s) == len(t) and Counter(s) == Counter(t)

def top_k_frequent(a, k):
    cnt = Counter(a)
    return [x for x, _ in cnt.most_common(k)]      # or bucket sort for O(n)""",
   "asks": [
     "valid anagram; group anagrams (key = sorted word or the 26-count tuple)",
     "top K frequent elements / words (heap, or bucket sort by count for O(n))",
     "first unique character; find all duplicates",
     "ransom note, 'can string a be built from string b'",
     "longest palindrome you can build from the letters",
     "sort characters by frequency; reorganise a string so no two neighbours match (counts + heap)",
     "minimum window substring and all anagram windows (counts INSIDE a sliding window)",
     "check if two strings are k-anagrams / one edit apart",
   ],
   "examples": [
     {"n": "Valid Anagram", "s": "LC 242"},
     {"n": "Group Anagrams", "s": "LC 49"},
     {"n": "Top K Frequent Elements", "s": "LC 347"},
     {"n": "First Unique Character in a String", "s": "LC 387"},
     {"n": "Reorganize String", "s": "LC 767"},
     {"n": "Longest Palindrome", "s": "LC 409"},
   ],
   "traps": [
     "<code>Counter</code> returns 0 for missing keys but <code>dict</code> raises — use <code>.get(k, 0)</code> or defaultdict.",
     "Comparing whole Counters inside a sliding window is O(26) per step; a 'matched characters' counter makes it O(1).",
     "Deleting zero-count keys matters whenever you test <code>len(cnt)</code>.",
   ]},

  {"id": "hs-index", "name": "Value → index map",
   "when": "You must return positions, or measure a distance between occurrences.",
   "tool": "dict mapping the value (or a derived key) to where you last / first saw it",
   "invariant": "the map answers 'where was the partner' in O(1)",
   "cx": "O(n) time, O(n) space",
   "code": """def two_sum(a, target):
    pos = {}
    for i, x in enumerate(a):
        if target - x in pos:            # check BEFORE inserting, or x pairs with itself
            return [pos[target - x], i]
        pos[x] = i
    return []""",
   "asks": [
     "two sum (unsorted, indices required)",
     "contains duplicate within distance k",
     "prefix-sum lookups — subarray sum equals K, longest subarray with sum K (see Prefix sum)",
     "isomorphic strings / word pattern (two maps, one each way)",
     "minimum index sum of common restaurants",
     "LRU cache (dict + doubly linked list)",
     "first / last occurrence of each character for partitioning (partition labels)",
   ],
   "examples": [
     {"n": "Two Sum", "s": "LC 1"},
     {"n": "Isomorphic Strings", "s": "LC 205"},
     {"n": "Partition Labels", "s": "LC 763"},
     {"n": "LRU Cache", "s": "LC 146"},
   ],
   "traps": [
     "Test the partner BEFORE inserting the current element, or an element matches itself.",
     "Isomorphic / word-pattern needs a map in BOTH directions; one direction passes the samples and fails the tests.",
     "First index or last index — decide which, exactly as in the prefix-sum variants.",
   ]},

  {"id": "hs-group", "name": "Group by a derived key",
   "when": "Bucket items that share a normalised form.",
   "tool": "<code>defaultdict(list)</code>, keyed by the invariant you invent",
   "invariant": "two items land in the same bucket exactly when they are equivalent under your key",
   "cx": "O(n · cost-of-key)",
   "code": """from collections import defaultdict
def group_anagrams(words):
    g = defaultdict(list)
    for w in words:
        key = tuple(sorted(w))            # or a 26-length count tuple -> O(len) not O(len log len)
        g[key].append(w)
    return list(g.values())""",
   "asks": [
     "group anagrams; group shifted strings; group by the pattern of a word",
     "group people by birth year / by prefix / by domain",
     "find duplicate files by content hash",
     "number of boomerangs, lines through the most points (key = the normalised slope)",
     "group identical subtrees (key = the serialised subtree — same idea as your HackerEarth 'echo structure' question)",
     "bulls and cows, 'count matching pairs by key'",
   ],
   "examples": [
     {"n": "Group Anagrams", "s": "LC 49"},
     {"n": "Group Shifted Strings", "s": "LC 249"},
     {"n": "Find Duplicate Subtrees", "s": "LC 652"},
     {"n": "Max Points on a Line", "s": "LC 149"},
     {"n": "Find Duplicate File in System", "s": "LC 609"},
   ],
   "traps": [
     "Keys must be hashable and canonical — tuples not lists, and normalise the slope by dividing by gcd (and fix the sign).",
     "Floating point keys compare badly; use an exact fraction as a tuple instead.",
   ]},

  {"id": "hs-cyclic", "name": "Cyclic sort / index-as-hash",
   "when": "Values are exactly 1..n (or 0..n−1) and O(1) extra space is demanded.",
   "tool": "the array itself — put value v at index v−1, or mark presence by negating a[v−1]",
   "invariant": "after the pass, any index whose value does not match is exactly the anomaly",
   "cx": "O(n) time, O(1) space",
   "code": """def find_missing_and_duplicate(a):
    n = len(a)
    for i in range(n):
        while a[i] != a[a[i] - 1]:        # send a[i] home; while, not if
            j = a[i] - 1
            a[i], a[j] = a[j], a[i]
    for i in range(n):
        if a[i] != i + 1:
            return {"duplicate": a[i], "missing": i + 1}""",
   "asks": [
     "missing number / all numbers disappeared from the array",
     "find all duplicates in an array where 1 ≤ a[i] ≤ n",
     "set mismatch (one duplicate and one missing)",
     "first missing POSITIVE integer (the hard one — same template, ignore out-of-range values)",
     "find the duplicate number without modifying the array (that one is Floyd's cycle detection instead)",
   ],
   "examples": [
     {"n": "Missing Number", "s": "LC 268"},
     {"n": "Find All Numbers Disappeared in an Array", "s": "LC 448"},
     {"n": "Find All Duplicates in an Array", "s": "LC 442"},
     {"n": "First Missing Positive", "s": "LC 41"},
     {"n": "Find the Duplicate Number", "s": "LC 287 — fast & slow pointers"},
   ],
   "traps": [
     "Swap in a <code>while</code>, not an <code>if</code> — the value you receive may also be out of place.",
     "Guard the swap condition against an infinite loop when two equal values both want the same slot.",
     "LC 287 forbids modifying the array, which is why it becomes a cycle-detection problem, not this one.",
   ]},
 ]},

# -------------------------------------------------------------- monotonic stack ----
{
 "id": "monotonic-stack", "group": "linear", "name": "Stack & monotonic stack",
 "buys": "O(n²) 'scan right until I find a bigger one' → O(n)",
 "lives": "array (next-greater family), string (matching / parsing)",
 "core": "A plain stack remembers what is still OPEN — unmatched brackets, unfinished frames. "
         "A MONOTONIC stack goes further: it keeps only the candidates that can still win. "
         "The moment a new element arrives that beats one on the stack, that stacked element's answer is "
         "decided — so you pop it and resolve it. Every index is pushed once and popped once: O(n).",
 "recognise": [
   {"cue": "<b>next greater</b> / next smaller / previous greater / previous smaller", "note": "textbook monotonic stack"},
   {"cue": "<b>span</b>, 'days until warmer', 'how far until'", "note": "the same thing, reported as a distance"},
   {"cue": "<b>histogram</b>, largest rectangle, maximal area", "note": "previous-smaller and next-smaller on each bar"},
   {"cue": "<b>brackets</b>, nesting, 'valid parentheses', decode a nested string", "note": "plain stack"},
   {"cue": "<b>remove k digits</b> / smallest number after removals / lexicographically smallest",
    "note": "greedy + monotonic stack"},
 ],
 "notwhen": [
   "You need the max of a fixed WINDOW → monotonic <b>deque</b>, because elements also expire from the front.",
   "You need the k largest overall → heap.",
   "The relation is recursive over a tree → plain DFS.",
 ],
 "pick": [
   {"if": "'next/previous greater or smaller' or a distance to it", "then": "ms-next"},
   {"if": "area / rectangle / water trapped between bars", "then": "ms-hist"},
   {"if": "matching, nesting, undo, evaluate an expression", "then": "ms-match"},
   {"if": "build the lexicographically best sequence under a removal budget", "then": "ms-greedy"},
 ],
 "variants": [
  {"id": "ms-next", "name": "Next greater / smaller element",
   "when": "For every element, find the first element to its right (or left) that is bigger or smaller.",
   "tool": "a stack of INDICES whose values are monotonic; pop and resolve when the new element breaks the order",
   "invariant": "the stack holds indices still waiting for their answer, in decreasing value order (for next-greater)",
   "cx": "O(n) time, O(n) space",
   "code": """def next_greater(a):
    res = [-1] * len(a)
    st = []                            # indices, values DECREASING
    for i, x in enumerate(a):
        while st and a[st[-1]] < x:    # x resolves everything smaller
            res[st.pop()] = x
        st.append(i)
    return res                          # leftovers keep -1: nothing greater exists""",
   "asks": [
     "next greater element I / II (circular — loop the array twice, mod n)",
     "daily temperatures (report the index distance, not the value)",
     "stock span problem (previous greater)",
     "next smaller element, 'first smaller to the left'",
     "sum of subarray minimums / maximums (count how many subarrays each element dominates)",
     "number of visible people in a queue; buildings with an ocean view",
     "132 pattern",
   ],
   "examples": [
     {"n": "Daily Temperatures", "s": "LC 739"},
     {"n": "Next Greater Element II (circular)", "s": "LC 503"},
     {"n": "Online Stock Span", "s": "LC 901"},
     {"n": "Sum of Subarray Minimums", "s": "LC 907"},
     {"n": "Buildings With an Ocean View", "s": "LC 1762"},
     {"n": "132 Pattern", "s": "LC 456"},
   ],
   "traps": [
     "Store indices when the answer is a distance; values are enough only when the answer is the value.",
     "Decide <code>&lt;</code> versus <code>&lt;=</code> deliberately — it decides how DUPLICATES are attributed, "
     "which is the whole correctness of 'sum of subarray minimums'.",
     "Circular versions iterate <code>2n</code> times with <code>i % n</code>, pushing only in the first pass.",
   ]},

  {"id": "ms-hist", "name": "Histogram / area between bars",
   "when": "Largest rectangle, maximal area, water trapped — each bar needs its reach on BOTH sides.",
   "tool": "an increasing stack; when a shorter bar arrives, the popped bar's rectangle is finished",
   "invariant": "for a popped bar, the new index is its first smaller to the right and the stack top is its first smaller to the left",
   "cx": "O(n) time, O(n) space",
   "code": """def largest_rectangle(h):
    st, best = [], 0                     # indices, heights INCREASING
    for i, x in enumerate(h + [0]):      # the sentinel 0 flushes the stack
        while st and h[st[-1]] > x:
            height = h[st.pop()]
            left = st[-1] + 1 if st else 0
            best = max(best, height * (i - left))
        st.append(i)
    return best""",
   "asks": [
     "largest rectangle in a histogram",
     "maximal rectangle in a binary matrix (run the histogram row by row)",
     "trapping rain water (stack form, or prefix-max / two-pointer form)",
     "largest square / maximal area under constraints",
     "sum of subarray ranges (max minus min over all subarrays)",
     "remove duplicate letters while keeping order",
   ],
   "examples": [
     {"n": "Largest Rectangle in Histogram", "s": "LC 84"},
     {"n": "Maximal Rectangle", "s": "LC 85"},
     {"n": "Trapping Rain Water", "s": "LC 42"},
     {"n": "Sum of Subarray Ranges", "s": "LC 2104"},
   ],
   "traps": [
     "Append a sentinel 0 (or flush after the loop), or bars left on the stack never get measured.",
     "The width uses the NEW stack top after popping, not the popped index — this is the single most common bug here.",
     "Equal heights: popping on <code>&gt;</code> vs <code>&gt;=</code> changes which bar claims the width, but the maximum comes out the same.",
   ]},

  {"id": "ms-match", "name": "Plain stack — matching, nesting, parsing",
   "when": "Brackets, nested structures, undo, expression evaluation.",
   "tool": "push the opener (or the current frame), pop on the closer and check the pair",
   "invariant": "the stack is exactly the list of things still unclosed, innermost on top",
   "cx": "O(n) time, O(n) space",
   "code": """def valid_parentheses(s):
    pair = {')': '(', ']': '[', '}': '{'}
    st = []
    for ch in s:
        if ch in pair:
            if not st or st.pop() != pair[ch]:
                return False
        else:
            st.append(ch)
    return not st                       # anything left open = invalid""",
   "asks": [
     "valid parentheses; minimum add / remove to make parentheses valid",
     "longest valid parentheses substring (stack of indices, or a two-pass counter)",
     "decode string 'k[encoded]' — push the count and the partial string",
     "evaluate reverse Polish notation; basic calculator I / II / III",
     "simplify a unix path; remove all adjacent duplicates; backspace string compare",
     "asteroid collision; make the string great",
     "score of parentheses; maximum nesting depth",
     "baseball game, 'undo the last operation'",
   ],
   "examples": [
     {"n": "Valid Parentheses", "s": "LC 20"},
     {"n": "Decode String", "s": "LC 394"},
     {"n": "Evaluate Reverse Polish Notation", "s": "LC 150"},
     {"n": "Basic Calculator II", "s": "LC 227"},
     {"n": "Asteroid Collision", "s": "LC 735"},
     {"n": "Simplify Path", "s": "LC 71"},
     {"n": "Longest Valid Parentheses", "s": "LC 32"},
   ],
   "traps": [
     "Check the stack is non-empty BEFORE popping, and check it is EMPTY at the end. Both halves are graded.",
     "In Decode String push both the repeat count and the string built so far, then rebuild on ']'.",
     "Calculator problems: handle the final pending number after the loop ends.",
   ]},

  {"id": "ms-greedy", "name": "Monotonic stack as a greedy builder",
   "when": "'Smallest / largest possible sequence after removing k items', order must be preserved.",
   "tool": "build the answer on a stack; pop while the top is worse than the newcomer and you still have budget",
   "invariant": "the stack is the best possible prefix achievable so far with the removals already spent",
   "cx": "O(n) time",
   "code": """def remove_k_digits(num, k):
    st = []
    for ch in num:
        while k and st and st[-1] > ch:   # a bigger digit earlier is always worse
            st.pop(); k -= 1
        st.append(ch)
    st = st[:len(st) - k] if k else st    # budget unspent -> drop from the end
    return ''.join(st).lstrip('0') or '0'""",
   "asks": [
     "remove k digits to make the smallest number",
     "create the maximum number of length k (from one array, or merged from two)",
     "remove duplicate letters / smallest subsequence of distinct characters",
     "maximum swap, 'largest number after one exchange'",
     "find the most competitive subsequence of size k",
     "stamping / lexicographically smallest string after operations",
   ],
   "examples": [
     {"n": "Remove K Digits", "s": "LC 402"},
     {"n": "Remove Duplicate Letters", "s": "LC 316"},
     {"n": "Find the Most Competitive Subsequence", "s": "LC 1673"},
     {"n": "Create Maximum Number", "s": "LC 321"},
     {"n": "Maximum Swap", "s": "LC 670"},
   ],
   "traps": [
     "If the budget is unspent at the end, trim from the BACK — the input was already non-decreasing.",
     "Leading zeros, and the empty result, need an explicit fallback.",
     "'Distinct letters' versions also need a 'last occurrence' table so you never pop a letter you cannot get back.",
   ]},
 ]},

# ----------------------------------------------------------------- heap / top-k ----
{
 "id": "heap", "group": "linear", "name": "Heap (priority queue)",
 "buys": "O(n log n) full sort → O(n log k) when you only need the extremes",
 "lives": "any stream or collection where you repeatedly need the current best",
 "core": "A heap gives you the smallest (or largest) item in O(1) and lets you replace it in O(log n). "
         "You reach for it when the answer needs 'the best remaining' over and over — and crucially when "
         "the collection keeps CHANGING, which is exactly when sorting once is not enough.",
 "recognise": [
   {"cue": "<b>K largest / K smallest / K closest / K most frequent</b>", "note": "a heap of size K"},
   {"cue": "<b>streaming</b>, 'at any time', 'as numbers arrive'", "note": "you cannot re-sort per query"},
   {"cue": "<b>merge K sorted</b> lists or arrays", "note": "heap of the k current heads"},
   {"cue": "<b>median</b> of a stream", "note": "two heaps, balanced"},
   {"cue": "repeatedly 'take the biggest / cheapest and then update it'", "note": "greedy driven by a heap"},
 ],
 "notwhen": [
   "You need the k-th element ONCE from a static array → quickselect is O(n) average.",
   "Counts are small integers → bucket sort by count is O(n), beating O(n log k).",
   "You need arbitrary-position lookups or ordered traversal → a balanced BST / sorted list, not a heap.",
 ],
 "pick": [
   {"if": "'K largest / smallest / closest / most frequent'", "then": "hp-topk"},
   {"if": "k sorted sequences to interleave", "then": "hp-merge"},
   {"if": "a running median or a balanced split", "then": "hp-two"},
   {"if": "schedule / simulate 'always serve the most urgent next'", "then": "hp-greedy"},
 ],
 "variants": [
  {"id": "hp-topk", "name": "Heap of size K",
   "when": "Only the K extreme elements matter.",
   "tool": "a MIN-heap of size k for the k LARGEST (the weakest survivor sits on top, ready to be evicted)",
   "invariant": "the heap always holds the best k seen so far, and its root is the worst of those k",
   "cx": "O(n log k) time, O(k) space",
   "code": """import heapq
def k_largest(a, k):
    h = []
    for x in a:
        heapq.heappush(h, x)
        if len(h) > k:
            heapq.heappop(h)          # evict the smallest -> k largest survive
    return h                           # h[0] is the k-th largest

# Python has only a MIN-heap. For a max-heap push -x, or use heapq.nlargest(k, a).""",
   "asks": [
     "k-th largest / smallest element in an array or a stream",
     "top K frequent elements or words (count first, then heap by count)",
     "K closest points to the origin; K closest numbers to x",
     "k-th largest element in a stream (a class with add())",
     "last stone weight; maximum score after k operations",
     "minimum cost to connect sticks / ropes (always join the two cheapest)",
     "furthest building you can reach with ladders and bricks",
   ],
   "examples": [
     {"n": "Kth Largest Element in an Array", "s": "LC 215"},
     {"n": "Top K Frequent Elements", "s": "LC 347"},
     {"n": "K Closest Points to Origin", "s": "LC 973"},
     {"n": "Kth Largest Element in a Stream", "s": "LC 703"},
     {"n": "Last Stone Weight", "s": "LC 1046"},
     {"n": "Minimum Cost to Connect Sticks", "s": "LC 1167"},
     {"n": "Furthest Building You Can Reach", "s": "LC 1642"},
   ],
   "traps": [
     "K largest needs a MIN-heap, k smallest needs a MAX-heap. Getting this inverted is the classic slip.",
     "Python's heapq is min-only: negate for a max-heap, and remember to negate back.",
     "For tuples, ties compare the second field — push <code>(key, index, item)</code> so items never get compared directly.",
   ]},

  {"id": "hp-merge", "name": "Merge K sorted sequences",
   "when": "k sorted lists/arrays to combine, or a sorted matrix to walk in order.",
   "tool": "heap holding one entry per sequence: (value, which sequence, position)",
   "invariant": "the heap always contains the smallest unconsumed element of every live sequence",
   "cx": "O(N log k) for N total elements",
   "code": """import heapq
def merge_k(lists):
    h = [(l[0], i, 0) for i, l in enumerate(lists) if l]
    heapq.heapify(h)
    out = []
    while h:
        val, i, j = heapq.heappop(h)
        out.append(val)
        if j + 1 < len(lists[i]):
            heapq.heappush(h, (lists[i][j+1], i, j+1))
    return out""",
   "asks": [
     "merge k sorted lists / arrays",
     "smallest range covering elements from k lists",
     "k-th smallest element in a sorted matrix (heap form; binary search is the faster form)",
     "find k pairs with the smallest sums",
     "ugly number II / super ugly number (heap of generated candidates)",
     "k-th smallest sum of two arrays",
   ],
   "examples": [
     {"n": "Merge k Sorted Lists", "s": "LC 23"},
     {"n": "Smallest Range Covering Elements from K Lists", "s": "LC 632"},
     {"n": "Find K Pairs with Smallest Sums", "s": "LC 373"},
     {"n": "Kth Smallest Element in a Sorted Matrix", "s": "LC 378"},
   ],
   "traps": [
     "Push the index alongside the value, or you cannot find the successor.",
     "Skip empty lists when seeding, or you index [0] on nothing.",
     "For k-pairs, seed only the first row and expand — seeding every pair defeats the point.",
   ]},

  {"id": "hp-two", "name": "Two heaps (running median / balance)",
   "when": "You need the middle of a changing collection, or to balance two halves.",
   "tool": "a max-heap for the lower half, a min-heap for the upper half, sizes within one",
   "invariant": "every element in the low heap ≤ every element in the high heap, and |low| − |high| ∈ {0, 1}",
   "cx": "O(log n) per insert, O(1) per median",
   "code": """import heapq
class MedianFinder:
    def __init__(self):
        self.lo = []      # max-heap via negation (lower half)
        self.hi = []      # min-heap (upper half)
    def add(self, x):
        heapq.heappush(self.lo, -x)
        heapq.heappush(self.hi, -heapq.heappop(self.lo))   # pass the biggest up
        if len(self.hi) > len(self.lo):                     # rebalance
            heapq.heappush(self.lo, -heapq.heappop(self.hi))
    def median(self):
        if len(self.lo) > len(self.hi):
            return -self.lo[0]
        return (-self.lo[0] + self.hi[0]) / 2""",
   "asks": [
     "find the median from a data stream",
     "sliding window median (needs lazy deletion, or a sorted container)",
     "IPO / maximise capital (two structures: one by cost, one by profit)",
     "balance two halves by cost, 'minimum cost to move chips / to equal heights'",
     "schedule tasks so the load stays balanced",
   ],
   "examples": [
     {"n": "Find Median from Data Stream", "s": "LC 295"},
     {"n": "Sliding Window Median", "s": "LC 480"},
     {"n": "IPO", "s": "LC 502"},
   ],
   "traps": [
     "Always push-then-transfer so the ordering invariant holds; pushing straight into the 'right' heap breaks it.",
     "Rebalance after EVERY insert, not at query time.",
     "Heaps cannot delete from the middle — the sliding-window version needs lazy deletion with a counter.",
   ]},

  {"id": "hp-greedy", "name": "Heap-driven greedy / simulation",
   "when": "A process where each step you must serve 'the most urgent / cheapest / largest' and then update it.",
   "tool": "a heap as the ready-queue, often with a second ordering (time, then priority)",
   "invariant": "the heap top is always the correct next thing to serve under the greedy rule",
   "cx": "O(n log n)",
   "code": """import heapq
def min_meeting_rooms(intervals):
    intervals.sort()                      # by start time
    ends = []                             # min-heap of end times
    for s, e in intervals:
        if ends and ends[0] <= s:
            heapq.heappop(ends)           # a room has freed up
        heapq.heappush(ends, e)
    return len(ends)                      # rooms in use at the peak""",
   "asks": [
     "meeting rooms II — minimum number of rooms",
     "task scheduler with cooldown; reorganise string",
     "CPU / single-threaded scheduling by shortest job next",
     "maximum events that can be attended",
     "car fleet, 'process in sorted order but resolve by a second key'",
     "minimum number of refuelling stops",
     "network delay time, cheapest flights (Dijkstra-shaped — see Graphs)",
   ],
   "examples": [
     {"n": "Meeting Rooms II", "s": "LC 253"},
     {"n": "Task Scheduler", "s": "LC 621"},
     {"n": "Single-Threaded CPU", "s": "LC 1834"},
     {"n": "Maximum Number of Events That Can Be Attended", "s": "LC 1353"},
     {"n": "Minimum Number of Refueling Stops", "s": "LC 871"},
   ],
   "traps": [
     "Sort by the right key FIRST — the heap only resolves the second dimension.",
     "Meeting rooms also has a pure sweep-line solution with no heap; know both.",
     "When the rule is 'serve the largest, then it decays', push the updated value back.",
   ]},
 ]},

# ---------------------------------------------------------- sorting & intervals ----
{
 "id": "intervals", "group": "linear", "name": "Sorting, intervals & sweep line",
 "buys": "O(n²) all-pairs overlap checks → O(n log n)",
 "lives": "lists of intervals, events, or anything with a natural order you can impose",
 "core": "Sorting is not the answer — it is what makes the answer a single pass. Once intervals are in order, "
         "each one only ever has to be compared with the PREVIOUS one, and 'do these overlap' collapses to "
         "<code>start ≤ previous_end</code>. Choosing what to sort BY is the entire decision.",
 "recognise": [
   {"cue": "input is a list of <b>[start, end]</b> pairs", "note": "almost certainly this family"},
   {"cue": "<b>merge / overlap / conflict / double-booked</b>", "note": "sort by start"},
   {"cue": "<b>maximum number of non-overlapping</b> / minimum removals", "note": "sort by END — the classic greedy"},
   {"cue": "<b>how many are active at the same time</b> (rooms, CPUs, people)", "note": "sweep line of +1 / −1 events"},
   {"cue": "<b>two keys fight each other</b> (height and position, cost and profit)",
    "note": "sort by one, then handle the other with a heap or insertion"},
 ],
 "notwhen": [
   "Order is already given and must be PRESERVED → sorting destroys the answer (then it is a stack or a window).",
   "You need the k best only → heap, O(n log k) beats a full sort.",
   "Values are a small dense range → counting sort is O(n).",
 ],
 "pick": [
   {"if": "combine overlapping ranges into blocks", "then": "iv-merge"},
   {"if": "insert one interval into a sorted non-overlapping list", "then": "iv-insert"},
   {"if": "keep the most non-overlapping / remove the fewest", "then": "iv-greedy"},
   {"if": "count how many overlap at the busiest moment", "then": "iv-sweep"},
   {"if": "sorting by a clever key makes the problem one pass", "then": "iv-sortkey"},
 ],
 "variants": [
  {"id": "iv-merge", "name": "Merge overlapping intervals",
   "when": "Collapse a list of ranges into the smallest set of disjoint ranges.",
   "tool": "sort by start; extend the last block or start a new one",
   "invariant": "the output list is always disjoint and sorted",
   "cx": "O(n log n)",
   "code": """def merge(intervals):
    intervals.sort(key=lambda x: x[0])
    out = []
    for s, e in intervals:
        if out and s <= out[-1][1]:          # touching counts as overlapping
            out[-1][1] = max(out[-1][1], e)  # max(), not e -- the old one may be longer
        else:
            out.append([s, e])
    return out""",
   "asks": [
     "merge intervals; summary ranges; missing ranges",
     "employee free time (merge all busy intervals, report the gaps)",
     "interval list intersections (two pointers over two sorted lists)",
     "'can the person attend all meetings' (any overlap at all)",
     "partition labels (merge the first/last occurrence ranges of each letter)",
     "remove covered intervals",
   ],
   "examples": [
     {"n": "Merge Intervals", "s": "LC 56"},
     {"n": "Meeting Rooms", "s": "LC 252"},
     {"n": "Interval List Intersections", "s": "LC 986"},
     {"n": "Remove Covered Intervals", "s": "LC 1288"},
     {"n": "Employee Free Time", "s": "LC 759"},
   ],
   "traps": [
     "<code>out[-1][1] = max(out[-1][1], e)</code> — assigning <code>e</code> blindly shrinks a block that already reached further.",
     "Decide whether touching ends ([1,2] and [2,3]) count as overlapping; the statement always says, and the samples prove it.",
   ]},

  {"id": "iv-insert", "name": "Insert into a disjoint sorted list",
   "when": "The list is already non-overlapping and sorted; add one interval.",
   "tool": "three phases — everything strictly before, the merged middle, everything strictly after",
   "invariant": "the result stays sorted and disjoint without re-sorting",
   "cx": "O(n)",
   "code": """def insert(intervals, new):
    out, i, n = [], 0, len(intervals)
    while i < n and intervals[i][1] < new[0]:    # strictly before
        out.append(intervals[i]); i += 1
    while i < n and intervals[i][0] <= new[1]:   # overlapping -> absorb
        new = [min(new[0], intervals[i][0]), max(new[1], intervals[i][1])]
        i += 1
    out.append(new)
    out.extend(intervals[i:])                     # strictly after
    return out""",
   "asks": [
     "insert interval",
     "my calendar I / II / III (book if no conflict)",
     "range module — add, query, remove ranges",
     "data stream as disjoint intervals",
   ],
   "examples": [
     {"n": "Insert Interval", "s": "LC 57"},
     {"n": "My Calendar I", "s": "LC 729"},
     {"n": "Data Stream as Disjoint Intervals", "s": "LC 352"},
   ],
   "traps": [
     "Three loops, in order, no early return — skipping the tail copy is the usual miss.",
     "The merged interval keeps growing while it overlaps; update both ends every time.",
   ]},

  {"id": "iv-greedy", "name": "Sort by END — maximum non-overlapping",
   "when": "'Maximum number of activities', 'minimum removals to make them disjoint', 'fewest arrows'.",
   "tool": "sort by end time; greedily take an interval whenever it starts after the last taken end",
   "invariant": "finishing earliest always leaves the most room for everything after — the exchange argument",
   "cx": "O(n log n)",
   "code": """def max_non_overlapping(intervals):
    intervals.sort(key=lambda x: x[1])      # by END -- this is the whole trick
    count, last_end = 0, float('-inf')
    for s, e in intervals:
        if s >= last_end:
            count += 1
            last_end = e
    return count                             # removals = len(intervals) - count""",
   "asks": [
     "non-overlapping intervals — minimum number to remove",
     "maximum number of activities / events you can attend",
     "minimum number of arrows to burst balloons",
     "maximum length of a pair chain",
     "two-city / task selection where each job has a deadline",
     "video stitching, minimum taps to water a garden (reachability greedy)",
   ],
   "examples": [
     {"n": "Non-overlapping Intervals", "s": "LC 435"},
     {"n": "Minimum Number of Arrows to Burst Balloons", "s": "LC 452"},
     {"n": "Maximum Length of Pair Chain", "s": "LC 646"},
     {"n": "Video Stitching", "s": "LC 1024"},
   ],
   "traps": [
     "Sort by END, not start. Sorting by start passes the samples and fails the hidden tests — this is a graded trap.",
     "Whether <code>s &gt;= last_end</code> or <code>s &gt; last_end</code> depends on whether touching is allowed. Arrows allow touching.",
   ]},

  {"id": "iv-sweep", "name": "Sweep line (+1 / −1 events)",
   "when": "'How many are active at once', peak concurrency, population over time.",
   "tool": "turn each interval into two events, sort all events, run a counter",
   "invariant": "after processing every event up to time t, the counter is exactly the number active at t",
   "cx": "O(n log n)",
   "code": """def max_concurrent(intervals):
    ev = []
    for s, e in intervals:
        ev.append((s, 1))        # arrival
        ev.append((e, -1))       # departure
    ev.sort()                    # at equal times, -1 sorts first: a leaver frees the slot
    cur = best = 0
    for _, delta in ev:
        cur += delta
        best = max(best, cur)
    return best""",
   "asks": [
     "meeting rooms II (minimum rooms = peak concurrency)",
     "car pooling, 'can all passengers fit'",
     "maximum population year; number of people in a building",
     "the skyline problem (sweep + heap of active heights)",
     "minimum platforms at a railway station",
     "count of intersections / points covered by the most intervals",
     "range addition — the same object as a difference array",
   ],
   "examples": [
     {"n": "Meeting Rooms II", "s": "LC 253"},
     {"n": "Car Pooling", "s": "LC 1094"},
     {"n": "Maximum Population Year", "s": "LC 1854"},
     {"n": "The Skyline Problem", "s": "LC 218"},
   ],
   "traps": [
     "Tie-breaking at equal timestamps decides correctness: if an interval ending at t does not conflict with one "
     "starting at t, the −1 must be processed first. <code>(t, -1) &lt; (t, +1)</code> gives that for free.",
     "Small fixed time ranges (hours, years) need no sort at all — use a difference array over the range.",
   ]},

  {"id": "iv-sortkey", "name": "Sort by the right key, then one pass",
   "when": "The problem is hard in the given order and trivial in some other order.",
   "tool": "a custom sort key — often descending on one field and ascending on the tie-breaker",
   "invariant": "after sorting, each element's answer depends only on what came before it",
   "cx": "O(n log n)",
   "code": """# queue reconstruction: tallest first, and among equals, smaller k first.
# Then inserting at index k is safe, because everyone already placed is >= this height.
def reconstruct_queue(people):
    people.sort(key=lambda p: (-p[0], p[1]))
    out = []
    for p in people:
        out.insert(p[1], p)
    return out""",
   "asks": [
     "queue reconstruction by height",
     "largest number from a list of numbers (compare a+b vs b+a as strings)",
     "boats to save people, two-sum style after sorting",
     "minimum cost to connect / to hire k workers (sort by ratio, then heap)",
     "car fleet (sort by position descending, compare arrival times)",
     "assign cookies, 'maximum matching after sorting both sides'",
     "wiggle sort, 'rearrange so no two adjacent are equal' (sort then interleave)",
     "merge accounts / sort by multiple keys with a custom comparator",
   ],
   "examples": [
     {"n": "Queue Reconstruction by Height", "s": "LC 406"},
     {"n": "Largest Number", "s": "LC 179"},
     {"n": "Boats to Save People", "s": "LC 881"},
     {"n": "Car Fleet", "s": "LC 853"},
     {"n": "Assign Cookies", "s": "LC 455"},
   ],
   "traps": [
     "In Python use <code>key=</code> with a tuple; for a genuine comparator use <code>functools.cmp_to_key</code>.",
     "Negate to sort one field descending while another stays ascending: <code>(-h, k)</code>.",
     "Always be able to justify WHY that order makes the greedy safe; if you cannot, it is probably DP.",
   ]},
 ]},

# --------------------------------------------------------------------- bit ops -----
{
 "id": "bits", "group": "linear", "name": "Bit manipulation",
 "buys": "O(n) extra space → O(1); and subset enumeration becomes a simple counter",
 "lives": "integers, and any set of at most ~20–25 items",
 "core": "Two completely separate uses. One: XOR cancels duplicates (x ^ x = 0, x ^ 0 = x), which solves "
         "'find the odd one out' in O(1) space. Two: an integer IS a subset — bit i means 'item i is in' — "
         "which is why <code>n ≤ 20</code> in the constraints is a bitmask signal.",
 "recognise": [
   {"cue": "<b>every element appears twice except one</b>", "note": "XOR the whole array"},
   {"cue": "<b>n ≤ 20–25</b> with 'all subsets' or 'assign each item'", "note": "bitmask enumeration or bitmask DP"},
   {"cue": "<b>without extra memory / O(1) space</b> on a counting problem", "note": "XOR or bit counting"},
   {"cue": "'count set bits', 'power of two', 'swap without a temp'", "note": "direct bit tricks"},
   {"cue": "<b>maximum XOR pair</b>, 'two numbers with the largest xor'", "note": "binary trie"},
 ],
 "notwhen": [
   "n is large and you need subsets → 2ⁿ explodes; it is a DP or a greedy.",
   "The duplicate count is 3 (not 2) → plain XOR fails; count bits per position mod 3.",
 ],
 "pick": [
   {"if": "find the unique / missing element with O(1) space", "then": "bt-xor"},
   {"if": "enumerate every subset of ≤ 20 items", "then": "bt-subsets"},
   {"if": "'state = which items are used' inside a DP", "then": "bt-dp"},
   {"if": "arithmetic on the bits themselves", "then": "bt-tricks"},
 ],
 "variants": [
  {"id": "bt-xor", "name": "XOR cancellation",
   "when": "Pairs cancel and you want the survivor, in O(1) space.",
   "tool": "x ^ x = 0, x ^ 0 = x, and XOR is commutative — order does not matter",
   "invariant": "the running XOR is the XOR of everything unpaired so far",
   "cx": "O(n) time, O(1) space",
   "code": """def single_number(a):
    r = 0
    for x in a:
        r ^= x
    return r

def missing_number(a):                 # values 0..n with one gone
    r = len(a)
    for i, x in enumerate(a):
        r ^= i ^ x
    return r""",
   "asks": [
     "single number (everything else appears twice)",
     "missing number from 0..n; find the difference between two strings",
     "two numbers appear once, the rest twice (XOR all, then split by the lowest set bit)",
     "single number II — everything appears three times (count bits mod 3)",
     "find the duplicate and the missing number together",
     "maximum XOR of two numbers in an array (binary trie, or bit-by-bit greedy)",
     "XOR queries of a subarray (prefix XOR — the same template as prefix sum)",
   ],
   "examples": [
     {"n": "Single Number", "s": "LC 136"},
     {"n": "Single Number II", "s": "LC 137"},
     {"n": "Single Number III", "s": "LC 260"},
     {"n": "Missing Number", "s": "LC 268"},
     {"n": "Maximum XOR of Two Numbers in an Array", "s": "LC 421"},
     {"n": "XOR Queries of a Subarray", "s": "LC 1310"},
   ],
   "traps": [
     "XOR only cancels EVEN counts. Three-of-a-kind needs the mod-3 bit counting instead.",
     "<code>x &amp; -x</code> isolates the lowest set bit — that is how you split the two-singles case.",
     "Prefix XOR with <code>{0: 1}</code> seeding counts subarrays with a given XOR, exactly like prefix sum.",
   ]},

  {"id": "bt-subsets", "name": "Bitmask = subset enumeration",
   "when": "n ≤ ~20 and you must consider every subset.",
   "tool": "loop mask from 0 to 2ⁿ−1; bit i set means item i is chosen",
   "invariant": "each mask is exactly one subset, and every subset appears exactly once",
   "cx": "O(2ⁿ · n)",
   "code": """def all_subsets(a):
    n = len(a)
    out = []
    for mask in range(1 << n):               # 2^n masks
        out.append([a[i] for i in range(n) if mask >> i & 1])
    return out

# iterate over the SUBMASKS of a mask (needed in set-cover style DP):
#   sub = mask
#   while sub:
#       ...use sub...
#       sub = (sub - 1) & mask""",
   "asks": [
     "generate all subsets / the power set",
     "count subsets whose sum / XOR / product meets a condition",
     "partition into k subsets with equal sums (n ≤ 16)",
     "maximum compatibility score sum, optimal student–mentor assignment",
     "'the longest word chain among ≤ 20 words'",
     "meet in the middle — split 40 items into two halves of 20",
   ],
   "examples": [
     {"n": "Subsets", "s": "LC 78"},
     {"n": "Partition to K Equal Sum Subsets", "s": "LC 698"},
     {"n": "Maximum Compatibility Score Sum", "s": "LC 1947"},
     {"n": "Maximum Product of the Length of Two Palindromic Subsequences", "s": "LC 2002"},
   ],
   "traps": [
     "<code>1 &lt;&lt; n</code> is 2ⁿ; at n = 25 that is 33 million masks — check the budget before committing.",
     "Backtracking also enumerates subsets and is easier to prune; the mask form is for DP over subsets.",
     "<code>mask &gt;&gt; i &amp; 1</code> needs no parentheses in Python, but write them anyway for readability.",
   ]},

  {"id": "bt-dp", "name": "Bitmask DP (state = which items are used)",
   "when": "n ≤ ~20, and the answer depends on WHICH items you have consumed, not just how many.",
   "tool": "dp[mask] = the best value when exactly the items in mask are done",
   "invariant": "popcount(mask) tells you how many steps have been taken, so the order is implicit",
   "cx": "O(2ⁿ · n) or O(2ⁿ · n²)",
   "code": """def min_cost_assignment(cost):          # cost[person][job], n x n
    n = len(cost)
    FULL = (1 << n) - 1
    import functools
    @functools.lru_cache(None)
    def go(mask):
        i = bin(mask).count('1')        # person i is next -> no need to store it
        if i == n:
            return 0
        best = float('inf')
        for j in range(n):
            if not (mask >> j & 1):
                best = min(best, cost[i][j] + go(mask | 1 << j))
        return best
    return go(0)""",
   "asks": [
     "assignment problem — minimum cost to assign n people to n jobs",
     "travelling salesman on n ≤ ~18 cities (shortest path visiting all nodes)",
     "partition to k equal-sum subsets; fair distribution of cookies",
     "number of ways to wear different hats; 'beautiful arrangement'",
     "minimum number of work sessions to finish all tasks",
     "shortest superstring / shortest path visiting all nodes",
   ],
   "examples": [
     {"n": "Shortest Path Visiting All Nodes", "s": "LC 847"},
     {"n": "Number of Ways to Wear Different Hats to Each Other", "s": "LC 1434"},
     {"n": "Minimum Number of Work Sessions to Finish the Tasks", "s": "LC 1986"},
     {"n": "Find Minimum Time to Finish All Jobs", "s": "LC 1723"},
   ],
   "traps": [
     "Derive the step index from <code>popcount(mask)</code> instead of adding it to the state — it halves the state space.",
     "2ⁿ states × n transitions: at n = 20 that is ~20 million. Fine in C++, tight in Python — memoise and prune.",
     "The constraint <code>n ≤ 12–20</code> in a hard problem is almost always announcing this pattern.",
   ]},

  {"id": "bt-tricks", "name": "The bit tricks worth memorising",
   "when": "Direct manipulation of bits is the question.",
   "tool": "the standard identities",
   "invariant": "—",
   "cx": "O(1) or O(number of set bits)",
   "code": """x & 1              # odd?
x >> 1             # divide by 2
x << k             # multiply by 2^k
x & (x - 1)        # clear the lowest set bit  -> loop to COUNT set bits
x & -x             # isolate the lowest set bit
x | (x + 1)        # set the lowest zero bit
x and not (x & (x - 1))   # power of two
bin(x).count('1')  # popcount in Python
x ^ y              # differing bits; a ^ b ^ b == a
(1 << n) - 1       # a mask of n ones""",
   "asks": [
     "number of 1 bits (Hamming weight); counting bits for 0..n (DP: <code>f[i] = f[i &gt;&gt; 1] + (i &amp; 1)</code>)",
     "power of two / power of four",
     "reverse the bits of a 32-bit integer",
     "hamming distance between two numbers; total hamming distance of an array",
     "sum of two integers without + or −",
     "complement of a number, bitwise AND of a number range",
     "gray code generation",
   ],
   "examples": [
     {"n": "Number of 1 Bits", "s": "LC 191"},
     {"n": "Counting Bits", "s": "LC 338"},
     {"n": "Reverse Bits", "s": "LC 190"},
     {"n": "Sum of Two Integers", "s": "LC 371"},
     {"n": "Bitwise AND of Numbers Range", "s": "LC 201"},
     {"n": "Gray Code", "s": "LC 89"},
   ],
   "traps": [
     "Python integers are arbitrary precision and negatives are not two's complement at a fixed width — "
     "mask with <code>&amp; 0xFFFFFFFF</code> when a problem assumes 32 bits.",
     "Shifting a negative number right in Python keeps the sign forever; loop on a masked copy.",
     "<code>x &amp; (x-1)</code> counting is O(set bits), faster than looping 32 times.",
   ]},
 ]},
]

# =====================================================================================
#  The remaining groups live in their own modules so this file stays navigable.
#  Order here is the order the Learn index shows them in, within each group.
# =====================================================================================
import lib_list_tree, lib_graph, lib_dp_search
PATTERNS += lib_list_tree.PATTERNS
PATTERNS += lib_graph.PATTERNS
PATTERNS += lib_dp_search.PATTERNS
