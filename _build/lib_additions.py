# -*- coding: utf-8 -*-
"""
The second pass over the pattern library: everything an audit against LeetCode's topic list and the classic problem sets
found missing, or found buried inside another variant's list.

  apply(PATTERNS, GROUPS)  adds the new variants and patterns, and gives EVERY variant its "keys":
                           the words and phrases in a question statement that point at that variant.

A variant marked rare=True is real but seldom asked at the 10-12 LPA level. It stays in the library as knowledge and is left out
of the threshold sets.
Every "code" block is exercised by test_additions.py.
"""


def V(id, name, when, tool, inv, cx, code, asks, ex, traps, keys, rare=False):
    examples = []
    for e in [x for x in ex.split(";") if x]:
        n, s = e.rsplit("|", 1)
        examples.append({"n": n.strip(), "s": "LC " + s.strip()})
    return {"id": id, "name": name, "when": when, "tool": tool, "invariant": inv, "cx": cx, "code": code.strip("\n"),
            "asks": asks, "examples": examples, "traps": traps, "keys": keys, "rare": rare}


# ---------------------------------------------------------------- added to existing patterns ------
ADD = {
"linked-list": ([
V("ll-gap", "Two pointers with a fixed gap", "Something is measured from the END of the list, and you cannot index from the end.",
  "two pointers exactly k nodes apart, walking together", "the distance between the two pointers never changes", "O(n) time, O(1) space",
  """
def remove_nth_from_end(head, n):
    dummy = ListNode(0, head)
    fast = slow = dummy
    for _ in range(n):               # open a gap of n nodes
        fast = fast.next
    while fast.next:                 # walk together until fast is on the last node
        fast, slow = fast.next, slow.next
    slow.next = slow.next.next       # slow is just BEFORE the node to remove
    return dummy.next
""",
  ["remove the n-th node from the end", "return the k-th node from the end", "rotate a list right by k (find the new tail with a gap)",
   "swap the k-th node from the start with the k-th from the end"],
  "Remove Nth Node From End of List|19;Rotate List|61;Swapping Nodes in a Linked List|1721",
  ["Start both at a dummy so that removing the head needs no special case.", "Rotate: reduce k with <code>k % length</code> first, or the gap walks off the list."],
  ["k-th from the end", "n-th node from the end", "last k nodes", "rotate the list"]),
V("ll-hash", "Hash map or set of nodes", "You must remember nodes you have seen, or map each original node to its copy.",
  "a dict keyed by the node object (not its value)", "the map holds exactly one entry for every node handled so far", "O(n) time, O(n) space",
  """
def copy_random_list(head):
    copy = {None: None}
    node = head
    while node:                      # pass 1: make every copy
        copy[node] = Node(node.val)
        node = node.next
    node = head
    while node:                      # pass 2: wire them, now every target exists
        copy[node].next = copy[node.next]
        copy[node].random = copy[node.random]
        node = node.next
    return copy[head]
""",
  ["deep-copy a list that has random pointers", "find where two lists intersect (set of nodes, or walk both and switch heads)",
   "detect a cycle when O(n) space is allowed", "delete every node whose value is in a given set", "count connected runs of listed values"],
  "Copy List with Random Pointer|138;Intersection of Two Linked Lists|160;Linked List Components|817;Delete Nodes From Linked List Present in Array|3217",
  ["Key on the node, not the value: two nodes can hold the same value.", "Put <code>None: None</code> in the map so null pointers need no check.",
   "Intersection in O(1) space: when a pointer falls off the end, restart it on the other head. Both walk a+b+c steps and meet."],
  ["deep copy", "clone", "random pointer", "visited nodes", "intersection point", "same node object"]),
], [{"cue": "<b>k-th from the end</b>, 'remove the n-th from the end'", "note": "two pointers with a fixed gap"},
    {"cue": "<b>deep copy</b>, random pointer, 'have I seen this node'", "note": "hash map of nodes"}],
   [{"if": "something is measured from the end of the list", "then": "ll-gap"}, {"if": "you must copy the list or remember visited nodes", "then": "ll-hash"}]),

"two-pointers": ([
V("tp-centre", "Expand around the centre", "A palindrome inside a string: the longest one, or how many there are.",
  "a left and right pointer starting at a centre and moving apart", "s[l..r] is a palindrome at every step of the expansion", "O(n²) time, O(1) space",
  """
def longest_palindrome(s):
    best = ""
    def grow(l, r):
        while l >= 0 and r < len(s) and s[l] == s[r]:
            l -= 1; r += 1
        return s[l + 1:r]            # the loop stopped one step too far
    for i in range(len(s)):
        for t in (grow(i, i), grow(i, i + 1)):   # odd centre, even centre
            if len(t) > len(best):
                best = t
    return best
""",
  ["longest palindromic substring", "count palindromic substrings", "longest palindrome after one change (with n small)"],
  "Longest Palindromic Substring|5;Palindromic Substrings|647",
  ["There are 2n−1 centres. Forgetting the even centre (i, i+1) is the classic bug.", "Substring means contiguous. Longest palindromic SUBSEQUENCE is DP, not this.", "Manacher's algorithm does this in O(n), but O(n²) is accepted for n up to a few thousand."],
  ["palindromic substring", "reads the same both ways", "mirror", "symmetric substring", "longest palindrome inside"]),
], [{"cue": "<b>palindromic substring</b>, longest or count", "note": "expand from every centre"}],
   [{"if": "a palindrome inside a string", "then": "tp-centre"}]),

"sliding-window": ([
V("sw-complement", "Take from both ends = window on what remains", "You remove or pick items only from the two ENDS, or the array is circular.",
  "a fixed or variable window over the part you do NOT take", "taken from the ends + the middle window = the whole array", "O(n) time, O(1) space",
  """
def max_points_from_ends(cards, k):
    n = len(cards)
    keep = n - k                     # the untouched middle has fixed length
    window = sum(cards[:keep])
    smallest = window
    for r in range(keep, n):
        window += cards[r] - cards[r - keep]
        smallest = min(smallest, window)
    return sum(cards) - smallest
""",
  ["maximum score taking k cards from either end", "fewest removals from the ends to reduce x to 0 (longest middle summing to total−x)", "circular array: fewest swaps to group all 1s"],
  "Maximum Points You Can Obtain from Cards|1423;Minimum Operations to Reduce X to Zero|1658;Minimum Swaps to Group All 1's Together II|2134",
  ["Circular window: walk indices with <code>% n</code> or double the array.", "Check the case where nothing remains in the middle (keep = 0)."],
  ["from either end", "from the beginning or the end", "first or last element", "circular", "wraps around"]),
], [{"cue": "take only from the <b>front or back</b>; <b>circular</b> array", "note": "slide a window over what remains"}],
   [{"if": "you may only take from the two ends", "then": "sw-complement"}]),

"hashing": ([
V("hs-moore", "Boyer-Moore majority vote", "An element appears more than n/2 (or n/3) times, and O(1) extra space is demanded.",
  "one candidate and one counter", "if a majority exists it survives every cancellation of pairs", "O(n) time, O(1) space",
  """
def majority(nums):
    cand, count = None, 0
    for x in nums:
        if count == 0:
            cand = x
        count += 1 if x == cand else -1
    return cand if nums.count(cand) > len(nums) // 2 else None   # verify
""",
  ["the element appearing more than n/2 times", "all elements appearing more than n/3 times (two candidates)", "does a majority exist at all"],
  "Majority Element|169;Majority Element II|229",
  ["If a majority is not guaranteed, verify the candidate with a second pass.", "For n/3 keep TWO candidates. There can be at most two such values."],
  ["majority", "more than half", "more than n/2 times", "more than n/3 times", "O(1) space"]),
], [{"cue": "<b>majority</b>, 'more than half the elements'", "note": "Boyer-Moore vote"}],
   [{"if": "more than n/2 and O(1) space", "then": "hs-moore"}]),

"monotonic-stack": ([
V("ms-contrib", "Contribution of each element", "SUM over all subarrays of their minimum, maximum or range.",
  "a monotonic stack giving each element's left and right reach", "element i is the minimum of exactly (i−left)·(right−i) subarrays", "O(n) time, O(n) space",
  """
def sum_subarray_mins(a):
    n, total, stack = len(a), 0, []
    for i in range(n + 1):
        cur = a[i] if i < n else float("-inf")   # sentinel flushes the stack
        while stack and a[stack[-1]] >= cur:
            m = stack.pop()
            left = stack[-1] if stack else -1
            total += a[m] * (m - left) * (i - m)
        stack.append(i)
    return total
""",
  ["sum of minimums of all subarrays", "sum of (max − min) of all subarrays", "maximum of min × sum across subarrays", "count subarrays in which a[i] is the maximum"],
  "Sum of Subarray Minimums|907;Sum of Subarray Ranges|2104;Maximum Subarray Min-Product|1856",
  ["Equal values: use &gt;= on one side and &gt; on the other, or duplicates are counted twice.", "Apply the modulo the question asks for, in languages without big integers."],
  ["sum over all subarrays", "sum of minimums", "for every subarray", "each element contributes"]),
], [{"cue": "<b>sum over all subarrays</b> of the min or max", "note": "count each element's contribution"}],
   [{"if": "sum, over all subarrays, of a min or max", "then": "ms-contrib"}]),

"heap": ([
V("hp-sorted", "Sorted container (ordered set / map)", "You need the nearest value above or below, or to delete arbitrary items, while the data changes.",
  "bisect on a sorted list (Python), TreeMap (Java), set / map (C++)", "the container is always sorted after each operation", "O(log n) search; list insert is O(n) in Python",
  """
import bisect

def contains_near(nums, index_diff, value_diff):
    window = []
    for i, x in enumerate(nums):
        pos = bisect.bisect_left(window, x - value_diff)
        if pos < len(window) and window[pos] <= x + value_diff:
            return True
        bisect.insort(window, x)
        if i >= index_diff:
            window.pop(bisect.bisect_left(window, nums[i - index_diff]))
    return False
""",
  ["nearest value within a window", "booking calendar: does a new interval overlap", "median of a sliding window", "smallest number currently in a container, with deletes"],
  "Contains Duplicate III|220;My Calendar I|729;Sliding Window Median|480;Design a Number Container System|2349",
  ["A heap cannot delete from the middle. If you need that, use this or a lazy-deleting heap.", "In Java and C++ this is built in; in Python use bisect (fine for n up to about 10^5)."],
  ["closest value", "nearest greater or equal", "ceiling / floor", "smallest value above", "add and remove", "book a slot"]),
], [{"cue": "<b>closest value</b>, floor or ceiling, with inserts and deletes", "note": "sorted container"}],
   [{"if": "nearest value, while items are added AND removed", "then": "hp-sorted"}]),

"bits": ([
V("bt-perbit", "Count each bit on its own", "A sum, AND, OR or XOR across all pairs or subsets, where n is too large to enumerate them.",
  "for each of the ~30 bits, a count of numbers having it set", "each bit contributes to the answer independently", "O(30·n) time, O(1) space",
  """
def total_hamming(nums):
    total = 0
    for bit in range(31):
        ones = sum((x >> bit) & 1 for x in nums)
        total += ones * (len(nums) - ones)   # pairs that differ at this bit
    return total
""",
  ["sum of XOR over all pairs", "total Hamming distance", "sum of all subset XOR totals (a set bit appears in 2^(n−1) subsets)", "best OR, AND or XOR reachable by operations"],
  "Total Hamming Distance|477;Sum of All Subset XOR Totals|1863;Bitwise XOR of All Pairings|2425;Maximum XOR After Operations|2317",
  ["The contribution of bit b is multiplied by 2^b unless the question only counts differing bits.", "Loop over all 31 bits (or 62 for long values)."],
  ["sum of XOR of all pairs", "for all pairs", "bitwise OR of all", "Hamming distance", "every subset XOR"]),
], [{"cue": "<b>all pairs / all subsets</b> combined with XOR, OR or AND", "note": "handle each bit separately"}],
   [{"if": "a bitwise total across all pairs or subsets", "then": "bt-perbit"}]),

"simulation": ([
V("sim-rules", "Follow the rules exactly", "The statement describes a process step by step and the constraints are small enough to just run it.",
  "the state in plain variables and a loop that performs one step", "after each loop the state equals the process after that many steps", "O(steps × cost of a step)",
  """
def zigzag(s, rows):
    if rows == 1 or rows >= len(s):
        return s
    lines = [""] * rows
    r, step = 0, 1
    for ch in s:
        lines[r] += ch
        if r == 0:
            step = 1
        elif r == rows - 1:
            step = -1
        r += step
    return "".join(lines)
""",
  ["robot moving on commands", "format text under exact rules", "game rounds played until a condition", "count-and-say style string generation", "queue at a counter, printer, elevator"],
  "Zigzag Conversion|6;Count and Say|38;Text Justification|68;Game of Life|289;Walking Robot Simulation|874",
  ["Check the constraint first: steps × step cost must fit roughly 10^8 operations. If the count of steps is huge, look for a cycle or formula.", "Read the tie-break and end-of-input rules twice. That is where the marks go."],
  ["simulate", "repeat until", "each round", "at each step", "in this order", "the robot", "after t seconds", "perform the following"]),
], [{"cue": "the statement lists <b>steps to perform</b>, constraints are small", "note": "just simulate it"}],
   [{"if": "a described process, and the step count is small", "then": "sim-rules"}]),

"tree-dfs": ([
V("td-global", "Post-order with a global best", "The best path bends at some node: it is not a single root-to-leaf chain.",
  "return the best single arm upward, update a global with both arms", "the return value is one arm; the answer may use two", "O(n) time, O(h) space",
  """
def diameter(root):
    best = 0
    def depth(node):
        nonlocal best
        if not node:
            return 0
        l, r = depth(node.left), depth(node.right)
        best = max(best, l + r)      # the path that bends here
        return 1 + max(l, r)         # only one arm can continue upward
    depth(root)
    return best
""",
  ["diameter", "maximum path sum between any two nodes", "longest path of equal values", "longest path where adjacent characters differ"],
  "Diameter of Binary Tree|543;Binary Tree Maximum Path Sum|124;Longest Univalue Path|687;Longest Path With Different Adjacent Characters|2246",
  ["Max path sum: clamp a negative arm to 0 with <code>max(0, arm)</code>.", "Never return l + r upward. A path cannot fork."],
  ["any two nodes", "diameter", "longest path between", "path may not pass through the root", "maximum path sum"]),
V("td-state", "Tree DP: return several values", "Each node has a choice (take / skip, covered / not), and the parent needs each outcome.",
  "a tuple returned from each child, one value per state", "the tuple is the best answer for the subtree in each state", "O(n) time, O(h) space",
  """
def rob(root):
    def go(node):                    # returns (best if robbed, best if skipped)
        if not node:
            return (0, 0)
        l, r = go(node.left), go(node.right)
        take = node.val + l[1] + r[1]
        skip = max(l) + max(r)
        return (take, skip)
    return max(go(root))
""",
  ["house robber on a tree", "fewest cameras to cover a tree", "longest zigzag path", "moves to balance coins across the tree"],
  "House Robber III|337;Binary Tree Cameras|968;Longest ZigZag Path in a Binary Tree|1372;Distribute Coins in Binary Tree|979",
  ["Write down in words what each tuple slot means before coding.", "Skip means children are free to be either state, so use max of the child's tuple."],
  ["adjacent nodes cannot both", "parent and child", "cover every node", "select nodes in a tree", "minimum to monitor"]),
V("td-build", "Build or serialize a tree", "You are given traversals or a string and must reconstruct the tree, or the reverse.",
  "a value→index map of the inorder, and a moving preorder pointer", "preorder gives the root, inorder splits left from right", "O(n) time, O(n) space",
  """
def build(preorder, inorder):
    at = {v: i for i, v in enumerate(inorder)}
    next_root = iter(preorder)
    def go(lo, hi):
        if lo > hi:
            return None
        node = TreeNode(next(next_root))
        mid = at[node.val]
        node.left = go(lo, mid - 1)  # left FIRST: preorder is root, left, right
        node.right = go(mid + 1, hi)
        return node
    return go(0, len(inorder) - 1)
""",
  ["build from preorder and inorder", "build from inorder and postorder (take roots from the back, build right first)", "serialize and deserialize", "balanced BST from a sorted array", "BST from preorder"],
  "Construct Binary Tree from Preorder and Inorder Traversal|105;Construct Binary Tree from Inorder and Postorder Traversal|106;Serialize and Deserialize Binary Tree|297;Construct Binary Search Tree from Preorder Traversal|1008",
  ["With postorder, build the RIGHT child first.", "Serialization must write null markers, or the shape is lost."],
  ["given inorder and preorder", "reconstruct the tree", "serialize", "deserialize", "construct the tree from"]),
V("td-parent", "Treat the tree as a graph", "Movement can go UP as well as down: distance from a given node, or spreading from a node.",
  "a parent map, then BFS with a visited set", "BFS reaches each node at its true distance from the start", "O(n) time, O(n) space",
  """
from collections import deque

def distance_k(root, target, k):
    parent = {root: None}
    stack = [root]
    while stack:
        n = stack.pop()
        for c in (n.left, n.right):
            if c:
                parent[c] = n
                stack.append(c)
    q, seen = deque([(target, 0)]), {target}
    out = []
    while q:
        n, d = q.popleft()
        if d == k:
            out.append(n.val)
            continue
        for m in (n.left, n.right, parent[n]):
            if m and m not in seen:
                seen.add(m)
                q.append((m, d + 1))
    return out
""",
  ["all nodes at distance k from a target", "time for infection to spread from a node", "time for news to pass down a company tree"],
  "All Nodes Distance K in Binary Tree|863;Amount of Time for Binary Tree to Be Infected|2385;Time Needed to Inform All Employees|1376",
  ["Key the maps on nodes, not values, unless values are guaranteed unique."],
  ["distance k from", "starting from a node, spreads", "infect", "burn the tree", "neighbours including parent"]),
V("td-reroot", "Rerooting DP", "You need the answer with EVERY node taken as the root.",
  "one DFS for root 0, a second that moves the root to each child", "moving the root across an edge changes the answer by a known amount", "O(n) time, O(n) space",
  """
def sum_of_distances(n, edges):
    g = [[] for _ in range(n)]
    for a, b in edges:
        g[a].append(b); g[b].append(a)
    size, ans = [1] * n, [0] * n
    def down(u, p):
        for v in g[u]:
            if v != p:
                down(v, u)
                size[u] += size[v]
                ans[u] += ans[v] + size[v]
    def reroot(u, p):
        for v in g[u]:
            if v != p:
                ans[v] = ans[u] - size[v] + (n - size[v])
                reroot(v, u)
    down(0, -1); reroot(0, -1)
    return ans
""",
  ["sum of distances from every node", "best root under some cost", "minimum height trees"],
  "Sum of Distances in Tree|834;Minimum Height Trees|310",
  ["In Python raise the recursion limit, or the recursion fails on a long chain."],
  ["for each node as root", "every node as the root", "sum of distances to all"], rare=True),
V("td-lift", "Binary lifting", "Many queries for the k-th ancestor or the LCA on a big tree.",
  "up[j][v] = the 2^j-th ancestor of v", "any jump of k decomposes into powers of two", "O(n log n) build, O(log n) per query",
  """
class Ancestor:
    def __init__(self, n, parent):
        self.up = [parent[:]]
        for j in range(1, 17):
            prev = self.up[-1]
            self.up.append([prev[prev[v]] if prev[v] != -1 else -1 for v in range(n)])
    def kth(self, v, k):
        for j in range(17):
            if k >> j & 1:
                v = self.up[j][v]
                if v == -1:
                    return -1
        return v
""",
  ["k-th ancestor queries", "LCA with many queries", "path aggregate queries on a tree"],
  "Kth Ancestor of a Tree Node|1483;Minimum Edge Weight Equilibrium Queries in a Tree|2846",
  ["The table needs about log2(n) levels. Keep -1 from being used as an index."],
  ["k-th ancestor", "many queries on a tree", "jump up"], rare=True),
], [{"cue": "the path <b>bends</b>: 'between any two nodes', diameter", "note": "post-order with a global best"},
    {"cue": "a <b>choice at each node</b> that constrains parent and child", "note": "return a tuple of states"},
    {"cue": "<b>given traversals</b>, serialize, reconstruct", "note": "build the tree"},
    {"cue": "<b>spreads from a node</b>, distance k from a target", "note": "add a parent map, BFS"}],
   [{"if": "the best path can bend at any node", "then": "td-global"}, {"if": "each node has take / skip style states", "then": "td-state"},
    {"if": "reconstruct from traversals", "then": "td-build"}, {"if": "you must also move upward", "then": "td-parent"},
    {"if": "answer needed for every node as root", "then": "td-reroot"}, {"if": "many ancestor queries", "then": "td-lift"}]),

"tree-bfs": ([
V("tb-index", "BFS with position numbers", "The answer depends on a node's horizontal position: width, vertical columns, completeness.",
  "the queue holds (node, index); children are 2i and 2i+1", "index gives a node's slot as in a heap array", "O(n) time, O(n) space",
  """
from collections import deque

def max_width(root):
    best, q = 0, deque([(root, 0)])
    while q:
        first = q[0][1]
        last = q[-1][1]
        best = max(best, last - first + 1)
        for _ in range(len(q)):
            node, i = q.popleft()
            i -= first               # rebase each level so numbers stay small
            if node.left:
                q.append((node.left, 2 * i))
            if node.right:
                q.append((node.right, 2 * i + 1))
    return best
""",
  ["maximum width of any level", "vertical order traversal (column = parent ∓ 1)", "top or bottom view", "is the tree complete"],
  "Maximum Width of Binary Tree|662;Vertical Order Traversal of a Binary Tree|987;Check Completeness of a Binary Tree|958",
  ["Rebase indexes on each level, or they overflow on deep trees.", "Vertical order ties are broken by row and then value. Read the statement."],
  ["width of the tree", "vertical", "column", "top view", "bottom view", "complete binary tree"]),
], [{"cue": "<b>width, column, vertical</b>, top / bottom view", "note": "BFS with position numbers"}],
   [{"if": "a node's horizontal position matters", "then": "tb-index"}]),

"trie": ([
V("tr-xor", "Bitwise trie (maximum XOR)", "Maximise XOR of a value against a set of numbers.",
  "a binary trie of the numbers from high bit to low", "at each bit, going to the opposite bit is always best if it exists", "O(30·n) time and space",
  """
def max_xor(nums):
    root = {}
    best = 0
    for x in nums:
        node = root
        for b in range(30, -1, -1):
            node = node.setdefault((x >> b) & 1, {})
        node, cur = root, 0
        for b in range(30, -1, -1):
            bit = (x >> b) & 1
            if 1 - bit in node:
                cur |= 1 << b
                node = node[1 - bit]
            else:
                node = node[bit]
        best = max(best, cur)
    return best
""",
  ["maximum XOR of two numbers in an array", "maximum XOR with a limit on the partner (sort queries offline)", "maximum XOR of a subarray (trie over prefix XORs)"],
  "Maximum XOR of Two Numbers in an Array|421;Maximum XOR With an Element From Array|1707;Maximum Strong Pair XOR II|2935",
  ["Always insert with the same fixed bit count, leading zeros included.", "Subarray XOR: insert prefix 0 before you start."],
  ["maximum XOR", "largest XOR", "XOR with a query value"]),
], [{"cue": "<b>maximum XOR</b> against a set of numbers", "note": "bitwise trie"}],
   [{"if": "maximise XOR", "then": "tr-xor"}]),

"grid": ([
V("gr-border", "Start from the border", "Cells are safe, or not captured, if they connect to the edge of the grid.",
  "a flood fill launched from every border cell", "anything the border flood does not reach is enclosed", "O(R·C) time and space",
  """
def solve_surrounded(board):
    R, C = len(board), len(board[0])
    def dfs(r, c):
        if 0 <= r < R and 0 <= c < C and board[r][c] == "O":
            board[r][c] = "#"
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                dfs(r + dr, c + dc)
    for r in range(R):
        dfs(r, 0); dfs(r, C - 1)
    for c in range(C):
        dfs(0, c); dfs(R - 1, c)
    for r in range(R):
        for c in range(C):
            board[r][c] = "O" if board[r][c] == "#" else "X"
    return board
""",
  ["surrounded regions", "water that can reach both oceans (flood from each border, intersect)", "land cells that cannot walk off the grid", "closed islands"],
  "Surrounded Regions|130;Pacific Atlantic Water Flow|417;Number of Enclaves|1020;Number of Closed Islands|1254",
  ["Going backward from the border is the trick: flow uphill from the ocean, instead of testing each cell.", "Use BFS or an iterative stack on big grids to avoid recursion limits."],
  ["surrounded", "enclosed", "cannot reach the boundary", "reach the edge", "both oceans"]),
], [{"cue": "<b>surrounded, enclosed</b>, 'reaches the edge'", "note": "flood from the border inward"}],
   [{"if": "the border decides which cells are safe", "then": "gr-border"}]),

"shortest-path": ([
V("sp-01bfs", "0-1 BFS", "Every edge costs 0 or 1, for example free moves and paid moves.",
  "a deque: 0-cost edges to the front, 1-cost edges to the back", "the deque stays sorted by distance", "O(V + E)",
  """
from collections import deque

def min_cost_grid(grid):
    R, C = len(grid), len(grid[0])
    dist = [[float("inf")] * C for _ in range(R)]
    dist[0][0] = 0
    q = deque([(0, 0)])
    while q:
        r, c = q.popleft()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            x, y = r + dr, c + dc
            if 0 <= x < R and 0 <= y < C:
                w = grid[x][y]        # 0 = free, 1 = costs one
                if dist[r][c] + w < dist[x][y]:
                    dist[x][y] = dist[r][c] + w
                    (q.appendleft if w == 0 else q.append)((x, y))
    return dist[R - 1][C - 1]
""",
  ["fewest obstacles to remove to reach the corner", "fewest arrows to change to make a valid path", "fewest walls to break"],
  "Minimum Cost to Make at Least One Valid Path in a Grid|1368;Minimum Obstacle Removal to Reach Corner|2290",
  ["Only push when the distance improves, or you revisit forever."],
  ["remove the fewest obstacles", "break walls", "free move", "cost 0 or 1"]),
V("sp-mod", "Dijkstra on a changed cost or state", "The path cost is not a simple sum (a bottleneck, a product), or the state needs extra information like time left.",
  "a heap of (cost, node, extra state)", "states pop in order of cost, so the first pop of a state is final", "O(E log V), times the number of extra states",
  """
import heapq

def min_effort(h):
    R, C = len(h), len(h[0])
    best = {(0, 0): 0}
    pq = [(0, 0, 0)]
    while pq:
        e, r, c = heapq.heappop(pq)
        if (r, c) == (R - 1, C - 1):
            return e
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            x, y = r + dr, c + dc
            if 0 <= x < R and 0 <= y < C:
                ne = max(e, abs(h[r][c] - h[x][y]))   # bottleneck, not a sum
                if ne < best.get((x, y), float("inf")):
                    best[(x, y)] = ne
                    heapq.heappush(pq, (ne, x, y))
""",
  ["path whose largest step is smallest", "path with maximum probability (use a max-heap on the product)", "cheapest route within a time limit (state: node, time)", "up to k free or discounted edges"],
  "Path With Minimum Effort|1631;Swim in Rising Water|778;Path with Maximum Probability|1514;Minimum Cost to Reach Destination in Time|1928",
  ["With extra state, the visited check is on (node, state), not node alone."],
  ["minimise the maximum", "bottleneck", "maximum probability", "within time limit", "up to k discounts"]),
], [{"cue": "edge costs are only <b>0 or 1</b>", "note": "0-1 BFS"}, {"cue": "<b>minimise the maximum</b> on a path, or the state has extras", "note": "Dijkstra on a changed cost"}],
   [{"if": "edges cost only 0 or 1", "then": "sp-01bfs"}, {"if": "cost is a bottleneck or product, or extra state is needed", "then": "sp-mod"}]),

"dsu": ([
V("dsu-prim", "Prim — minimum spanning tree with a heap", "Connect everything cheaply on a DENSE graph, or when the edges are implicit (all pairs of points).",
  "a heap of (edge cost, node) leaving the current tree", "the cheapest edge leaving the tree is always safe to add", "O(E log V)",
  """
import heapq

def min_cost_connect_points(points):
    n = len(points)
    seen, total = set(), 0
    pq = [(0, 0)]
    while len(seen) < n:
        cost, u = heapq.heappop(pq)
        if u in seen:
            continue
        seen.add(u)
        total += cost
        for v in range(n):
            if v not in seen:
                d = abs(points[u][0] - points[v][0]) + abs(points[u][1] - points[v][1])
                heapq.heappush(pq, (d, v))
    return total
""",
  ["connect all points at the least cost", "minimum spanning tree of a dense graph", "GfG style: give the MST weight"],
  "Min Cost to Connect All Points|1584",
  ["Check <code>seen</code> when you POP, since one node sits in the heap several times."],
  ["minimum spanning tree", "MST", "connect all", "minimum cost to connect"]),
], [], [{"if": "MST, dense graph or implicit edges", "then": "dsu-prim"}]),

"dp-1d": ([
V("dp-state", "State machine DP", "On each day you are in one of a few modes, and the rules restrict moves between them.",
  "one variable for each state, all updated per step", "each variable is the best result ending today in that state", "O(n·states) time, O(states) space",
  """
def max_profit_cooldown(prices):
    hold, sold, rest = float("-inf"), 0, 0
    for p in prices:
        hold, sold, rest = max(hold, rest - p), hold + p, max(rest, sold)
    return max(sold, rest)
""",
  ["stock trading with cooldown", "with a transaction fee", "with at most k transactions", "alternating sums or modes", "flip at most one segment"],
  "Best Time to Buy and Sell Stock II|122;Best Time to Buy and Sell Stock with Cooldown|309;Best Time to Buy and Sell Stock with Transaction Fee|714;Best Time to Buy and Sell Stock III|123;Best Time to Buy and Sell Stock IV|188",
  ["Update all the states at once, from the previous day's values.", "Draw the states and arrows first. The transitions then write themselves."],
  ["cooldown", "holding", "transaction", "buy and sell", "at most k transactions", "mode", "must rest after"]),
V("dp-partition", "Cut the string or array into pieces", "Split a sequence into consecutive pieces, each with a rule, and count or minimise.",
  "dp[i] = answer for the first i items; try every last piece", "dp[i] is correct for each prefix before it is used", "O(n²) or O(n·max piece)",
  """
def word_break(s, words):
    words = set(words)
    dp = [True] + [False] * len(s)
    for i in range(1, len(s) + 1):
        for j in range(max(0, i - 20), i):   # 20 = the longest word
            if dp[j] and s[j:i] in words:
                dp[i] = True
                break
    return dp[-1]
""",
  ["word break", "decode ways", "fewest cuts into palindromes", "split array into pieces of at most k, maximise the sum", "fewest extra characters left over"],
  "Word Break|139;Decode Ways|91;Palindrome Partitioning II|132;Partition Array for Maximum Sum|1043;Extra Characters in a String|2707",
  ["dp has n+1 slots, and dp[0] is the empty prefix.", "Decode ways: a '0' is never valid alone. That is the case to test."],
  ["segment the string", "split into", "partition into", "number of ways to decode", "cuts", "dictionary words", "consecutive groups"]),
], [{"cue": "<b>cooldown, holding, buy / sell</b>, a few named modes", "note": "state machine DP"},
    {"cue": "<b>split into pieces</b>, segment, number of decodings", "note": "dp over the last piece"}],
   [{"if": "a few modes with restricted switching", "then": "dp-state"}, {"if": "cut the sequence into pieces", "then": "dp-partition"}]),

"dp-2d": ([
V("dp-digit", "Digit DP", "Count numbers in [L, R] whose digits satisfy a rule, where R may be 10^9 to 10^18.",
  "recursion over positions with (pos, tight, state) memoised", "tight tracks whether the prefix still equals N's prefix", "O(digits · 10 · states)",
  """
from functools import lru_cache

def count_without_digit_4(n):            # how many of 0..n contain no digit 4
    s = str(n)
    @lru_cache(None)
    def go(i, tight):
        if i == len(s):
            return 1
        top = int(s[i]) if tight else 9
        return sum(go(i + 1, tight and d == top) for d in range(top + 1) if d != 4)
    return go(0, True)
""",
  ["how many numbers up to N have a digit rule", "count of a digit across 1..N", "numbers with unique or repeated digits", "digit sum between limits"],
  "Numbers At Most N Given Digit Set|902;Number of Digit One|233;Count Numbers with Unique Digits|357;Numbers With Repeated Digits|1012",
  ["Answer for [L, R] = f(R) − f(L−1).", "If leading zeros matter to the rule, add a 'started' flag to the state."],
  ["count numbers between L and R", "digits", "up to 10^18", "sum of digits", "no two adjacent digits"], rare=True),
], [{"cue": "count numbers <b>up to 10^18</b> with a <b>digit</b> rule", "note": "digit DP"}],
   [{"if": "count numbers in a huge range by a digit rule", "then": "dp-digit"}]),

"backtracking": ([
V("bk-partition", "Split a string every valid way", "Return all the ways to cut a string into valid pieces.",
  "a start index and a list of pieces so far", "the pieces so far exactly spell s[0..start)", "exponential, O(n·2^n) worst case",
  """
def palindrome_partitions(s):
    out, cur = [], []
    def go(start):
        if start == len(s):
            out.append(cur[:])
            return
        for end in range(start + 1, len(s) + 1):
            piece = s[start:end]
            if piece == piece[::-1]:
                cur.append(piece)
                go(end)
                cur.pop()
    go(0)
    return out
""",
  ["all palindrome partitions", "all valid IP addresses from digits", "maximum count of unique pieces", "all sentences from a dictionary"],
  "Palindrome Partitioning|131;Restore IP Addresses|93;Split a String Into the Max Number of Unique Substrings|1593",
  ["'All the ways' means backtrack. 'How many' or 'minimum' is usually DP."],
  ["all possible partitions", "all ways to split", "every valid way to segment", "restore", "list all"]),
V("bk-build", "Build a string under a rule", "Generate all strings of a fixed shape, one character at a time.",
  "the string built so far and the remaining budget", "every prefix built can still be completed validly", "exponential in the output length",
  """
def generate_parens(n):
    out = []
    def go(cur, opens, closes):
        if len(cur) == 2 * n:
            out.append(cur)
            return
        if opens < n:
            go(cur + "(", opens + 1, closes)
        if closes < opens:
            go(cur + ")", opens, closes + 1)
    go("", 0, 0)
    return out
""",
  ["all valid parentheses", "phone keypad letters", "strings with letter case changes", "k-th happy string"],
  "Letter Combinations of a Phone Number|17;Generate Parentheses|22;Letter Case Permutation|784;The k-th Lexicographical String of All Happy Strings of Length n|1415",
  ["Prune while building, not after. Generating everything and filtering will time out."],
  ["generate all", "all combinations of letters", "valid strings of length n", "phone keypad"]),
V("bk-bucket", "Assign items to k buckets", "Split n items (n ≤ ~16) into k groups to balance them or make them equal.",
  "a bucket array, trying each item in each bucket", "each bucket's total never exceeds the limit", "O(k^n) with heavy pruning",
  """
def can_partition_k(nums, k):
    total = sum(nums)
    if total % k:
        return False
    target = total // k
    nums.sort(reverse=True)              # biggest first fails fastest
    buckets = [0] * k
    def go(i):
        if i == len(nums):
            return True
        for b in range(k):
            if buckets[b] + nums[i] <= target:
                buckets[b] += nums[i]
                if go(i + 1):
                    return True
                buckets[b] -= nums[i]
            if buckets[b] == 0:          # empty buckets are all the same
                break
        return False
    return go(0)
""",
  ["partition into k equal-sum subsets", "form a square from matchsticks", "share jobs among k workers, minimise the maximum", "fair distribution of cookies"],
  "Partition to K Equal Sum Subsets|698;Matchsticks to Square|473;Find Minimum Time to Finish All Jobs|1723;Fair Distribution of Cookies|2305",
  ["Both prunes matter: sort descending, and stop after trying one empty bucket."],
  ["k subsets", "k groups", "k workers", "distribute among", "n ≤ 16", "equal sum"]),
], [{"cue": "<b>all the ways</b> to split a string", "note": "backtrack over cut positions"},
    {"cue": "<b>generate all</b> strings of a shape", "note": "build one character at a time"},
    {"cue": "<b>k groups</b> and very small n", "note": "assign items to buckets"}],
   [{"if": "list every way to cut a string", "then": "bk-partition"}, {"if": "generate all strings under a rule", "then": "bk-build"}, {"if": "put n items in k groups", "then": "bk-bucket"}]),

"greedy": ([
V("gr-twopass", "Left pass, right pass", "Each position has constraints against both of its neighbours.",
  "one pass applying the left rule, a second applying the right", "after both passes, both neighbour rules hold", "O(n) time, O(n) space",
  """
def candy(ratings):
    n = len(ratings)
    c = [1] * n
    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            c[i] = c[i - 1] + 1
    for i in range(n - 2, -1, -1):
        if ratings[i] > ratings[i + 1]:
            c[i] = max(c[i], c[i + 1] + 1)
    return sum(c)
""",
  ["candy distribution by ratings", "dominoes falling from both sides", "distance to the nearest character", "moves to bring all balls to each box"],
  "Candy|135;Push Dominoes|838;Shortest Distance to a Character|821;Minimum Number of Operations to Move All Balls to Each Box|1769",
  ["The second pass must take the max, so it keeps what the first established."],
  ["higher than its neighbours", "both neighbours", "left and right", "nearest on either side"]),
V("gr-balance", "Running balance", "A running total must never go negative, or must end at zero.",
  "one counter updated per element, with a reset or fix when it breaks", "the counter equals the surplus so far", "O(n) time, O(1) space",
  """
def can_complete_circuit(gas, cost):
    if sum(gas) < sum(cost):
        return -1
    start, tank = 0, 0
    for i in range(len(gas)):
        tank += gas[i] - cost[i]
        if tank < 0:                     # nothing up to i can be the start
            start, tank = i + 1, 0
    return start
""",
  ["gas station circuit", "fewest insertions to balance brackets", "valid parentheses with wildcards (track a min and max balance)", "fewest swaps to balance"],
  "Gas Station|134;Minimum Add to Make Parentheses Valid|921;Valid Parenthesis String|678;Minimum Number of Swaps to Make the String Balanced|1963",
  ["Gas station: total gas < total cost means no answer, whatever the start."],
  ["never goes negative", "balance", "circular route", "fuel", "starting point", "minimum to make valid"]),
], [{"cue": "constraints against <b>both neighbours</b>", "note": "one pass each way"}, {"cue": "a <b>running balance</b> that must stay non-negative", "note": "counter with a reset"}],
   [{"if": "each position is constrained by both neighbours", "then": "gr-twopass"}, {"if": "a running total must stay non-negative", "then": "gr-balance"}]),
}

# ---------------------------------------------------------------- brand-new patterns ------
NEW_GROUPS = [
    {"id": "maths", "name": "Maths & number theory", "note": "Small set of formulas. If you have not seen them, the question cannot be solved by thinking harder."},
    {"id": "design", "name": "Design a data structure", "note": "The question hands you a class with methods and a required speed. Combine two simple structures."},
]

NEW = [
{"id": "sort-dc", "group": "linear", "name": "Sorting algorithms & divide and conquer",
 "buys": "Sorting internals answer questions that a library sort cannot: counts during a merge, or the k-th element in linear time.",
 "lives": "arrays", "core": "A library sort gives you only the final order. When the question needs something that happens DURING the sort (how many pairs crossed over) or needs less than a full sort (only the k-th), use the algorithm itself.",
 "recognise": [{"cue": "<b>inversions</b>, 'how many smaller to the right'", "note": "count during merge sort"},
               {"cue": "<b>k-th largest</b> with O(n) average expected", "note": "quickselect"},
               {"cue": "values in a <b>small range</b>, or 'O(n), no comparison sort'", "note": "counting or bucket sort"},
               {"cue": "solve the left half, solve the right, <b>combine</b>", "note": "divide and conquer"}],
 "notwhen": ["The final sorted order is all you need → call the library sort."],
 "pick": [{"if": "count pairs (i<j) with a relation across the array", "then": "dc-mergecount"}, {"if": "only the k-th element matters", "then": "dc-quickselect"},
          {"if": "the value range is small or a frequency decides the order", "then": "dc-bucket"}, {"if": "the answer combines two halves", "then": "dc-split"}],
 "variants": [
V("dc-mergecount", "Count during merge sort", "Count pairs i<j with a relation, such as a[i] > a[j]. n is too big for O(n²).",
  "merge sort; at each merge, count the pairs crossing between halves", "each half is sorted, so crossing pairs are counted in one sweep", "O(n log n) time, O(n) space",
  """
def count_inversions(a):
    def sort(lo, hi):
        if hi - lo < 2:
            return 0
        mid = (lo + hi) // 2
        count = sort(lo, mid) + sort(mid, hi)
        merged, i, j = [], lo, mid
        while i < mid or j < hi:
            if j == hi or (i < mid and a[i] <= a[j]):
                merged.append(a[i]); i += 1
            else:
                count += mid - i             # every remaining left value is bigger
                merged.append(a[j]); j += 1
        a[lo:hi] = merged
        return count
    return sort(0, len(a))
""",
  ["count inversions", "how many smaller numbers after each element", "reverse pairs with a[i] > 2·a[j]", "range sums falling within limits"],
  "Sort an Array|912;Count of Smaller Numbers After Self|315;Reverse Pairs|493;Count of Range Sum|327",
  ["With a condition unlike the merge order (2·a[j]), count in a separate sweep before merging.", "Use a Fenwick tree as the alternative when values can be compressed."],
  ["inversions", "number of smaller elements to the right", "pairs i < j with", "how far from sorted"]),
V("dc-quickselect", "Quickselect", "You want only the k-th largest or smallest, not the whole order.",
  "partition around a random pivot, recurse into one side", "after a partition the pivot sits in its final position", "O(n) average, O(n²) worst",
  """
import random

def kth_largest(nums, k):
    target = len(nums) - k
    lo, hi = 0, len(nums) - 1
    while True:
        p = random.randint(lo, hi)
        nums[p], nums[hi] = nums[hi], nums[p]
        store = lo
        for i in range(lo, hi):
            if nums[i] < nums[hi]:
                nums[i], nums[store] = nums[store], nums[i]
                store += 1
        nums[store], nums[hi] = nums[hi], nums[store]
        if store == target:
            return nums[store]
        if store < target:
            lo = store + 1
        else:
            hi = store - 1
""",
  ["k-th largest element", "k closest points", "median in expected linear time"],
  "Kth Largest Element in an Array|215;K Closest Points to Origin|973;Wiggle Sort II|324",
  ["Use a random pivot, or sorted input hits the O(n²) worst case.", "In an exam, a heap or sort is usually accepted and safer."],
  ["k-th largest", "k-th smallest", "without sorting", "median", "k closest"]),
V("dc-bucket", "Counting and bucket sort", "The values lie in a small range, or the index itself can be a frequency.",
  "an array of counts or buckets indexed by value", "bucket b holds exactly the items that map to b", "O(n + range)",
  """
def top_k_frequent(nums, k):
    freq = {}
    for x in nums:
        freq[x] = freq.get(x, 0) + 1
    buckets = [[] for _ in range(len(nums) + 1)]   # index = frequency
    for x, c in freq.items():
        buckets[c].append(x)
    out = []
    for c in range(len(nums), 0, -1):
        out += buckets[c]
        if len(out) >= k:
            return out[:k]
""",
  ["sort by frequency", "h-index", "maximum gap in linear time", "top k frequent in O(n)", "sort a string of lowercase letters"],
  "H-Index|274;Maximum Gap|164;Sort Characters By Frequency|451;Top K Frequent Elements|347",
  ["Only useful when the range is small compared with n.", "Frequency is at most n, so n+1 buckets are always enough."],
  ["lowercase letters only", "values from 1 to 100", "sort by frequency", "linear time sort", "O(n) without comparison"]),
V("dc-split", "Divide and conquer", "The answer for a range can be built from the answers for two halves.",
  "a recursive function on (lo, hi) and a combine step", "each half is solved independently", "usually O(n log n)",
  """
def diff_ways(expr):
    if expr.isdigit():
        return [int(expr)]
    out = []
    for i, ch in enumerate(expr):
        if ch in "+-*":
            for a in diff_ways(expr[:i]):
                for b in diff_ways(expr[i + 1:]):
                    out.append(a + b if ch == "+" else a - b if ch == "-" else a * b)
    return out
""",
  ["all results of adding parentheses", "balanced BST from a sorted array", "sort a linked list", "closest pair idea", "build a permutation with a structural property"],
  "Different Ways to Add Parentheses|241;Convert Sorted Array to Binary Search Tree|108;Sort List|148;Beautiful Array|932",
  ["Memoise if the same range repeats. It then becomes interval DP."],
  ["split in half", "left half and right half", "every way of parenthesising", "recursively divide"]),
]},

{"id": "math", "group": "maths", "name": "Maths & number theory",
 "buys": "A formula turns an impossible loop into one line.",
 "lives": "integers, usually huge limits with a modulo", "core": "Answers 'modulo 1e9+7', limits up to 10^18, and words like prime, divisor, GCD or arrangements are all signs that the question is really one of a few standard formulas.",
 "recognise": [{"cue": "<b>modulo 1e9+7</b>, huge exponent", "note": "fast power"}, {"cue": "<b>prime, factors, divisors</b>", "note": "sieve or trial division"},
               {"cue": "<b>GCD, LCM</b>, 'equal groups', 'divides all'", "note": "Euclid"}, {"cue": "<b>number of ways to arrange / choose</b>", "note": "nCr"},
               {"cue": "<b>digits</b>, reverse a number, big-number strings", "note": "digit walking"}, {"cue": "two players <b>play optimally</b>", "note": "parity, game observation"},
               {"cue": "<b>points, lines, rectangles</b>", "note": "coordinate geometry"}],
 "notwhen": ["The count of ways depends on earlier choices with restrictions → it is DP rather than a formula."],
 "pick": [{"if": "GCD, LCM, equal grouping", "then": "ma-gcd"}, {"if": "primes or factors", "then": "ma-sieve"}, {"if": "powers, or anything modulo a prime", "then": "ma-modpow"},
          {"if": "count of arrangements or selections", "then": "ma-ncr"}, {"if": "work on the digits of a number", "then": "ma-digits"}, {"if": "two players, or a pattern in small cases", "then": "ma-game"}, {"if": "points and shapes", "then": "ma-geom"}],
 "variants": [
V("ma-gcd", "GCD and LCM", "Something must divide everything equally, or two periods must line up.",
  "Euclid's algorithm", "gcd(a, b) = gcd(b, a mod b)", "O(log min(a, b))",
  """
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return a // gcd(a, b) * b        # divide first to avoid overflow
""",
  ["GCD of an array", "can everything be split into equal groups", "when two cycles coincide (LCM)", "count subarrays with GCD = k", "is target reachable with two jugs (target divisible by gcd)"],
  "Greatest Common Divisor of Strings|1071;X of a Kind in a Deck of Cards|914;Water and Jug Problem|365;Nth Magical Number|878;Number of Subarrays With GCD Equal to K|2447",
  ["GCD of many numbers: fold from the left; it shrinks quickly.", "Slope as a fraction: divide dx and dy by their GCD."],
  ["GCD", "HCF", "LCM", "greatest common", "divides all", "equal groups", "coincide again", "at the same time again"]),
V("ma-sieve", "Primes and factorisation", "The question is about primes, prime factors or the count of divisors.",
  "a sieve array, or trial division up to √n", "every composite is crossed out by its smallest prime factor", "sieve O(n log log n); trial division O(√n)",
  """
def sieve(n):
    is_prime = [True] * (n + 1)
    is_prime[0:2] = [False, False][: n + 1]
    i = 2
    while i * i <= n:
        if is_prime[i]:
            for m in range(i * i, n + 1, i):
                is_prime[m] = False
        i += 1
    return [i for i, p in enumerate(is_prime) if p]

def factorise(x):
    out, p = {}, 2
    while p * p <= x:
        while x % p == 0:
            out[p] = out.get(p, 0) + 1
            x //= p
        p += 1
    if x > 1:
        out[x] = out.get(x, 0) + 1
    return out
""",
  ["count primes below n", "prime factors of each number", "number of divisors", "primes in a range", "connect numbers sharing a factor (with DSU)", "Euler totient"],
  "Count Primes|204;Largest Component Size by Common Factor|952;Distinct Prime Factors of Product of Array|2521;Closest Prime Numbers in Range|2523",
  ["1 is not prime.", "Start crossing out at i×i.", "After trial division, a leftover x > 1 is itself a prime factor."],
  ["prime", "divisors", "factors", "co-prime", "perfect square", "semi-prime"]),
V("ma-modpow", "Fast power and modular arithmetic", "A huge exponent, or an answer given modulo a prime.",
  "square-and-multiply; apply the modulo at each step", "result × base^n stays equal to the true answer", "O(log n)",
  """
MOD = 10**9 + 7

def power(base, n, mod=MOD):
    result = 1
    base %= mod
    while n:
        if n & 1:
            result = result * base % mod
        base = base * base % mod
        n >>= 1
    return result

def inverse(a, mod=MOD):             # division under a prime modulus
    return power(a, mod - 2, mod)
""",
  ["compute x^n", "count of strings of length n by digit rules", "division under a modulo", "polygon or circular arrangement counts", "matrix power for a recurrence with huge n"],
  "Pow(x, n)|50;Super Pow|372;Count Good Numbers|1922;Count Collisions of Monkeys on a Polygon|2550",
  ["You cannot divide under a modulus. Multiply by the inverse instead.", "A subtraction can go negative: write <code>(a - b + MOD) % MOD</code>.", "In Python, <code>pow(a, n, MOD)</code> is built in."],
  ["modulo 10^9+7", "1e9+7", "answer may be large", "raise to the power", "n up to 10^18"]),
V("ma-ncr", "Combinatorics (nCr)", "Count arrangements or selections where there are no sequential restrictions.",
  "precomputed factorials and inverse factorials", "nCr = n! / (r! (n−r)!)", "O(n) precompute, O(1) per query",
  """
MOD = 10**9 + 7

def build(n):
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD
    inv = [1] * (n + 1)
    inv[n] = pow(fact[n], MOD - 2, MOD)
    for i in range(n, 0, -1):
        inv[i - 1] = inv[i] * i % MOD
    def ncr(a, b):
        if b < 0 or b > a:
            return 0
        return fact[a] * inv[b] % MOD * inv[a - b] % MOD
    return ncr
""",
  ["paths in a grid by formula", "ways to reach a position in k steps", "arrangements with repeated items (n!/a!b!)", "distributing identical items (stars and bars)", "Pascal's triangle"],
  "Unique Paths|62;Pascal's Triangle|118;Number of Ways to Reach a Position After Exactly k Steps|2400;Count All Valid Pickup and Delivery Options|1359",
  ["Precompute up to the largest n once, not per query.", "Inclusion-exclusion: total minus the bad arrangements is often easier."],
  ["number of ways to choose", "arrangements", "permutations of", "how many ways to distribute", "select r from n"]),
V("ma-digits", "Digit walking and big numbers", "You work on individual digits, or numbers too large for an integer type.",
  "%10 and //10, or a carry over strings", "the number so far equals the digits consumed so far", "O(digits)",
  """
def add_strings(a, b):
    i, j, carry, out = len(a) - 1, len(b) - 1, 0, []
    while i >= 0 or j >= 0 or carry:
        d = carry
        if i >= 0:
            d += int(a[i]); i -= 1
        if j >= 0:
            d += int(b[j]); j -= 1
        out.append(str(d % 10))
        carry = d // 10
    return "".join(reversed(out))
""",
  ["reverse an integer", "palindrome number", "digit sum, digital root", "happy number (cycle detection)", "add or multiply numbers held as strings", "base conversion"],
  "Reverse Integer|7;Palindrome Number|9;Add Digits|258;Happy Number|202;Multiply Strings|43;Add Binary|67",
  ["Watch for overflow in Java and C++ when reversing.", "Remember the final carry."],
  ["digit", "sum of digits", "reverse the number", "as a string", "binary string", "base"]),
V("ma-game", "Observation and games", "Two players play optimally, or a process looks random but small cases show a pattern.",
  "work out n = 1..10 by hand and look for the pattern", "the outcome depends only on a simple quantity (parity, n mod k)", "usually O(1)",
  """
def nim_game(n):                     # take 1..3 stones: multiples of 4 lose
    return n % 4 != 0

def bulbs_on(n):                     # a bulb is toggled once per divisor
    return int(n ** 0.5)             # only perfect squares have odd divisors
""",
  ["who wins with optimal play", "XOR of pile sizes decides Nim", "toggling bulbs by divisors", "parity of a total decides feasibility"],
  "Nim Game|292;Bulb Switcher|319;Divisor Game|1025;Stone Game|877",
  ["Never guess from 2 or 3 cases. Check at least to n = 10.", "Many piles: the first player wins if the XOR of all piles is non-zero."],
  ["play optimally", "Alice and Bob", "who wins", "take turns", "toggle", "first player"]),
V("ma-geom", "Basic coordinate geometry", "Points, lines or rectangles on a plane.",
  "cross products, slopes as reduced fractions, interval overlap per axis", "two rectangles overlap iff they overlap on both axes", "O(n) to O(n²)",
  """
def rect_overlap(a, b):              # (x1, y1, x2, y2)
    return min(a[2], b[2]) > max(a[0], b[0]) and min(a[3], b[3]) > max(a[1], b[1])

def cross(o, a, b):                  # > 0 means a left turn
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
""",
  ["do two rectangles overlap", "most points on one line", "is it a valid square", "area and perimeter by formula", "convex hull"],
  "Rectangle Overlap|836;Max Points on a Line|149;Valid Square|593;Erect the Fence|587",
  ["Never store slopes as floats. Use a (dy, dx) pair reduced by the GCD.", "Check whether touching at an edge counts as overlap."],
  ["points on a plane", "coordinates", "rectangle", "lie on the same line", "distance between points"], rare=True),
]},

{"id": "design", "group": "design", "name": "Design a data structure",
 "buys": "Each operation hits its required speed by joining two simple structures, each covering the other's weakness.",
 "lives": "a class with several methods", "core": "The statement gives you methods and says O(1) or O(log n). Ask: what lookup do I need, and what order do I need? A hashmap gives lookup. A list, heap or second stack gives order. The answer is nearly always both together.",
 "recognise": [{"cue": "<b>LRU, LFU</b>, 'evict the least recently used'", "note": "hashmap + doubly linked list"},
               {"cue": "stack or queue that also reports <b>min / max / frequency</b>", "note": "store extra data per entry"},
               {"cue": "implement a <b>queue using stacks</b>, circular buffer", "note": "two stacks, or a ring"},
               {"cue": "insert, delete, <b>getRandom in O(1)</b>", "note": "array + value→index map"},
               {"cue": "<b>timestamp</b>, 'value at time t', snapshots", "note": "sorted history + binary search"},
               {"cue": "<b>next() / hasNext()</b>", "note": "iterator with a stack"}],
 "notwhen": ["The question has one function and no 'implement the class' → look at the other patterns."],
 "pick": [{"if": "evict by least recent or least frequent", "then": "ds-lru"}, {"if": "stack with a min / max / frequency", "then": "ds-aux"}, {"if": "build one container from another", "then": "ds-queue"},
          {"if": "uniform random in O(1)", "then": "ds-random"}, {"if": "values over time", "then": "ds-timekey"}, {"if": "next() and hasNext()", "then": "ds-iter"}],
 "variants": [
V("ds-lru", "LRU / LFU cache", "A fixed capacity, and evict the least recently or least frequently used.",
  "hashmap for lookup + doubly linked list for order (OrderedDict in Python)", "the list is in recency order at all times", "O(1) per operation",
  """
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.data = OrderedDict()
    def get(self, key):
        if key not in self.data:
            return -1
        self.data.move_to_end(key)
        return self.data[key]
    def put(self, key, value):
        if key in self.data:
            self.data.move_to_end(key)
        self.data[key] = value
        if len(self.data) > self.cap:
            self.data.popitem(last=False)   # oldest out
""",
  ["LRU cache", "LFU cache (a list per frequency + a min-frequency variable)", "browser history forward / back", "design a linked list"],
  "LRU Cache|146;LFU Cache|460;Design Browser History|1472;Design Linked List|707",
  ["An interviewer may forbid OrderedDict. Know the node-based version with sentinel head and tail.", "get counts as a use: move the key to the front."],
  ["least recently used", "least frequently used", "cache", "capacity", "evict"]),
V("ds-aux", "Stack with extra data per entry", "A stack must also report its minimum, maximum or most frequent item.",
  "a second stack or a tuple stored at each level", "each level remembers the answer for the stack up to that level", "O(1) per operation",
  """
class MinStack:
    def __init__(self):
        self.s = []                  # (value, minimum at this depth)
    def push(self, x):
        self.s.append((x, min(x, self.s[-1][1]) if self.s else x))
    def pop(self):
        self.s.pop()
    def top(self):
        return self.s[-1][0]
    def getMin(self):
        return self.s[-1][1]
""",
  ["min stack", "max frequency stack", "stock span online", "stack with increment over the bottom k"],
  "Min Stack|155;Maximum Frequency Stack|895;Online Stock Span|901;Design a Stack With Increment Operation|1381",
  ["The extra value belongs to the depth, so popping restores the old answer automatically."],
  ["retrieve the minimum in constant time", "getMin", "most frequent element pop", "stack that supports"]),
V("ds-queue", "One container built from another", "Implement a queue with stacks, a stack with queues, or a circular buffer.",
  "two stacks (in + out), or an array with head and size", "items in the out stack are older than anything in the in stack", "amortised O(1)",
  """
class MyQueue:
    def __init__(self):
        self.a, self.b = [], []
    def push(self, x):
        self.a.append(x)
    def peek(self):
        if not self.b:
            while self.a:
                self.b.append(self.a.pop())
        return self.b[-1]
    def pop(self):
        self.peek()
        return self.b.pop()
    def empty(self):
        return not self.a and not self.b
""",
  ["queue using two stacks", "stack using queues", "circular queue", "circular deque"],
  "Implement Queue using Stacks|232;Implement Stack using Queues|225;Design Circular Queue|622;Design Circular Deque|641",
  ["Refill the out stack only when it is EMPTY, or the order breaks.", "Circular buffer: use <code>(head + size) % cap</code> and hold the size."],
  ["implement a queue using", "using only stacks", "circular buffer", "ring buffer", "fixed-size queue"]),
V("ds-random", "O(1) insert, delete, getRandom", "Uniform random choice plus fast insert and delete.",
  "an array of values and a value→index map", "the map always gives each value's true position", "O(1) per operation",
  """
import random

class RandomizedSet:
    def __init__(self):
        self.a, self.at = [], {}
    def insert(self, x):
        if x in self.at:
            return False
        self.at[x] = len(self.a)
        self.a.append(x)
        return True
    def remove(self, x):
        if x not in self.at:
            return False
        i, last = self.at[x], self.a[-1]
        self.a[i], self.at[last] = last, i   # move the last value into the gap
        self.a.pop()
        del self.at[x]
        return True
    def getRandom(self):
        return random.choice(self.a)
""",
  ["insert / delete / getRandom in O(1)", "the same, with duplicates allowed (a set of indexes for each value)"],
  "Insert Delete GetRandom O(1)|380;Insert Delete GetRandom O(1) - Duplicates allowed|381",
  ["Swap with the last element, because popping from the end is the only O(1) delete on an array.", "Update the map BEFORE deleting x, or removing the last value breaks."],
  ["getRandom", "equal probability", "uniformly at random", "average O(1)"]),
V("ds-timekey", "History with binary search", "Look up a value as of some time or version.",
  "key → sorted list of (time, value)", "each list is sorted because times arrive in increasing order", "O(1) set, O(log n) get",
  """
import bisect

class TimeMap:
    def __init__(self):
        self.times, self.vals = {}, {}
    def set(self, key, value, t):
        self.times.setdefault(key, []).append(t)
        self.vals.setdefault(key, []).append(value)
    def get(self, key, t):
        i = bisect.bisect_right(self.times.get(key, []), t) - 1
        return self.vals[key][i] if i >= 0 else ""
""",
  ["time-based key-value store", "snapshot array", "stock price with corrections", "average journey times"],
  "Time Based Key-Value Store|981;Snapshot Array|1146;Stock Price Fluctuation|2034;Design Underground System|1396",
  ["Search with bisect_right then subtract one, to get the last time ≤ t."],
  ["timestamp", "at time t", "snapshot", "version", "most recent value before"]),
V("ds-iter", "Iterator with a stack", "Implement next() and hasNext() over a nested or tree structure, lazily.",
  "a stack holding the unexplored part", "the top of the stack is always the next item", "amortised O(1), O(depth) space",
  """
class BSTIterator:
    def __init__(self, root):
        self.s = []
        self.push_left(root)
    def push_left(self, n):
        while n:
            self.s.append(n)
            n = n.left
    def next(self):
        n = self.s.pop()
        self.push_left(n.right)
        return n.val
    def hasNext(self):
        return bool(self.s)
""",
  ["BST iterator", "flatten a nested list iterator", "peeking iterator"],
  "Binary Search Tree Iterator|173;Flatten Nested List Iterator|341;Peeking Iterator|284",
  ["Do the work lazily in next(). Flattening everything up front is what the question bans."],
  ["next()", "hasNext()", "iterator", "lazily", "nested list"]),
]},

{"id": "graph-walk", "group": "graph", "name": "Graph traversal (adjacency list)",
 "buys": "Turns a list of edges into components, colourings and shortest hops.",
 "lives": "nodes and edges, often hidden: cities, friends, words, lock states", "core": "If things connect to things, it is a graph, even when the word graph never appears. Build an adjacency list, keep a visited set, then choose DFS for reachability and BFS for fewest steps.",
 "recognise": [{"cue": "<b>connected</b>, provinces, friend circles, reachable", "note": "components"}, {"cue": "<b>two groups</b>, no enemies together", "note": "bipartite colouring"},
               {"cue": "<b>fewest moves</b> between states that are not cells", "note": "BFS over states"}, {"cue": "each node has <b>exactly one</b> outgoing edge", "note": "functional graph"},
               {"cue": "<b>critical</b> connection, removing it disconnects", "note": "bridges"}, {"cue": "<b>mutually reachable</b> groups in a directed graph", "note": "SCC"},
               {"cue": "use <b>every edge exactly once</b>", "note": "Euler path"}],
 "notwhen": ["Edges have different weights and you need the cheapest path → weighted shortest paths.", "Prerequisites or an ordering → topological sort."],
 "pick": [{"if": "reachability or number of groups", "then": "gw-components"}, {"if": "split into two conflict-free sides", "then": "gw-bipartite"}, {"if": "fewest moves through abstract states", "then": "gw-state"},
          {"if": "one outgoing edge per node", "then": "gw-functional"}, {"if": "edge whose removal disconnects", "then": "gw-bridges"}, {"if": "directed, mutual reachability", "then": "gw-scc"}, {"if": "use each edge once", "then": "gw-euler"}],
 "variants": [
V("gw-components", "Connected components / clone", "Who can reach whom, how many groups, or copy the graph.",
  "adjacency list + visited set", "a node is marked the moment it is discovered", "O(V + E)",
  """
def count_components(n, edges):
    g = [[] for _ in range(n)]
    for a, b in edges:
        g[a].append(b); g[b].append(a)
    seen, groups = set(), 0
    for s in range(n):
        if s in seen:
            continue
        groups += 1
        stack = [s]
        seen.add(s)
        while stack:
            for v in g[stack.pop()]:
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
    return groups
""",
  ["number of provinces / friend circles", "is there a path", "can all rooms be visited", "clone a graph (old → new map)", "count unreachable pairs"],
  "Number of Provinces|547;Keys and Rooms|841;Find if Path Exists in Graph|1971;Clone Graph|133;Count Unreachable Pairs of Nodes in an Undirected Graph|2316",
  ["Mark visited when you PUSH, or nodes are queued many times.", "Isolated nodes count as components: loop over all n."],
  ["connected", "provinces", "friend groups", "can reach", "clone the graph", "network", "cities connected by roads"]),
V("gw-bipartite", "Two-colouring (bipartite)", "Split nodes into two groups with no edge inside a group.",
  "a colour map, giving neighbours the opposite colour", "every edge joins two different colours", "O(V + E)",
  """
def is_bipartite(g):
    colour = {}
    for s in range(len(g)):
        if s in colour:
            continue
        colour[s] = 0
        stack = [s]
        while stack:
            u = stack.pop()
            for v in g[u]:
                if v not in colour:
                    colour[v] = 1 - colour[u]
                    stack.append(v)
                elif colour[v] == colour[u]:
                    return False
    return True
""",
  ["is the graph bipartite", "split people who dislike each other", "odd cycle detection"],
  "Is Graph Bipartite?|785;Possible Bipartition|886",
  ["Start from every uncoloured node: the graph may be disconnected."],
  ["two groups", "two teams", "dislike", "enemies", "no two adjacent", "bipartite"]),
V("gw-state", "BFS over states", "Fewest moves, but a node is a situation (a word, lock code or position + keys), not a cell.",
  "a queue of states + a visited set of states", "BFS reaches each state first by its fewest moves", "O(states × moves per state)",
  """
from collections import deque

def open_lock(deadends, target):
    dead = set(deadends)
    if "0000" in dead:
        return -1
    q, seen = deque([("0000", 0)]), {"0000"}
    while q:
        s, d = q.popleft()
        if s == target:
            return d
        for i in range(4):
            for step in (1, 9):
                t = s[:i] + str((int(s[i]) + step) % 10) + s[i + 1:]
                if t not in dead and t not in seen:
                    seen.add(t)
                    q.append((t, d + 1))
    return -1
""",
  ["word ladder", "open a lock", "shortest path with k obstacle removals (state: cell, k)", "snakes and ladders", "visit all nodes (state: node, bitmask)"],
  "Word Ladder|127;Open the Lock|752;Shortest Path in a Grid with Obstacles Elimination|1293;Snakes and Ladders|909;Shortest Path Visiting All Nodes|847",
  ["The visited set must contain the WHOLE state, including keys or remaining removals.", "Estimate the state count first."],
  ["minimum number of moves", "transform into", "one change at a time", "minimum steps to reach", "with at most k"]),
V("gw-functional", "Functional graph (one outgoing edge)", "Each node points to exactly one other: 'next', favourite, or an array used as pointers.",
  "follow pointers, stamping each visit with a step number", "a revisit within the same walk closes a cycle", "O(n)",
  """
def longest_cycle(edges):
    best, stamp = -1, {}
    clock = 0
    for s in range(len(edges)):
        start = clock
        u = s
        while u != -1 and u not in stamp:
            stamp[u] = clock
            clock += 1
            u = edges[u]
        if u != -1 and stamp[u] >= start:
            best = max(best, clock - stamp[u])
    return best
""",
  ["longest cycle", "closest meeting node of two walkers", "find the duplicate number (array as pointers)", "who ends up where after k jumps"],
  "Longest Cycle in a Graph|2360;Find Closest Node to Given Two Nodes|2359;Find the Duplicate Number|287;Maximum Employees to Be Invited to a Meeting|2127",
  ["A stamp from an EARLIER walk is not a new cycle; compare with this walk's start."],
  ["each node has at most one outgoing edge", "points to", "favorite person", "next[i]", "jump to a[i]"]),
V("gw-bridges", "Bridges and articulation points", "Which edge or node, if removed, disconnects the graph.",
  "DFS with discovery time and low-link", "low[v] is the earliest node reachable from v's subtree", "O(V + E)",
  """
def bridges(n, edges):
    g = [[] for _ in range(n)]
    for a, b in edges:
        g[a].append(b); g[b].append(a)
    disc, low, out = [-1] * n, [0] * n, []
    t = [0]
    def dfs(u, parent):
        disc[u] = low[u] = t[0]; t[0] += 1
        for v in g[u]:
            if v == parent:
                continue
            if disc[v] == -1:
                dfs(v, u)
                low[u] = min(low[u], low[v])
                if low[v] > disc[u]:
                    out.append([u, v])
            else:
                low[u] = min(low[u], disc[v])
    for i in range(n):
        if disc[i] == -1:
            dfs(i, -1)
    return out
""",
  ["critical connections", "articulation points", "single points of failure"],
  "Critical Connections in a Network|1192",
  ["Articulation point test is low[v] >= disc[u], and the root needs at least two children."],
  ["critical connection", "removing it disconnects", "single point of failure", "articulation"], rare=True),
V("gw-scc", "Strongly connected components", "Groups in a DIRECTED graph where everyone can reach everyone.",
  "Kosaraju: finish order, then DFS on the reversed graph", "in reverse finish order, each DFS on the reversed graph finds one SCC", "O(V + E)",
  """
def scc_count(n, edges):
    g = [[] for _ in range(n)]
    r = [[] for _ in range(n)]
    for a, b in edges:
        g[a].append(b); r[b].append(a)
    seen, order = [False] * n, []
    def d1(u):
        seen[u] = True
        for v in g[u]:
            if not seen[v]:
                d1(v)
        order.append(u)
    def d2(u):
        seen[u] = True
        for v in r[u]:
            if not seen[v]:
                d2(v)
    for i in range(n):
        if not seen[i]:
            d1(i)
    seen = [False] * n
    count = 0
    for u in reversed(order):
        if not seen[u]:
            count += 1
            d2(u)
    return count
""",
  ["count SCCs", "condense a graph into a DAG", "mutually reachable groups"],
  "",
  ["The second DFS must run on the REVERSED graph, in reverse finish order."],
  ["strongly connected", "mutually reachable", "directed", "reach each other"], rare=True),
V("gw-euler", "Euler path (use every edge once)", "A route that uses every edge exactly once.",
  "Hierholzer: DFS consuming edges, record nodes on the way back", "a node is appended only when all its edges are used", "O(E log E) with sorted edges",
  """
import heapq

def itinerary(tickets):
    g = {}
    for a, b in tickets:
        heapq.heappush(g.setdefault(a, []), b)
    route = []
    def go(u):
        while g.get(u):
            go(heapq.heappop(g[u]))
        route.append(u)
    go("JFK")
    return route[::-1]
""",
  ["reconstruct an itinerary from tickets", "valid arrangement of pairs", "can you draw it without lifting the pen"],
  "Reconstruct Itinerary|332;Valid Arrangement of Pairs|2097",
  ["Undirected: an Euler path exists only with 0 or 2 odd-degree nodes.", "The route comes out backward. Reverse it."],
  ["use every edge exactly once", "itinerary", "all tickets", "without lifting"], rare=True),
]},
]

# ---------------------------------------------------------------- keywords for the original 87 variants ------
KEYS = {
"tp-ends": ["sorted array", "pair with sum", "two numbers that add to", "palindrome check", "3sum", "container", "reverse in place"],
"tp-write": ["in place", "remove duplicates", "move zeroes", "O(1) extra space", "keep the relative order", "is subsequence"],
"tp-merge": ["two sorted arrays", "merge", "common elements", "intersection of sorted lists", "compare two versions"],
"tp-partition": ["three colours", "0s, 1s and 2s", "segregate", "partition around a pivot", "one pass"],
"sw-fixed": ["of size k", "every k consecutive", "window of length k", "anagram of", "permutation in string", "k consecutive days"],
"sw-longest": ["longest substring", "maximum length subarray", "at most k distinct", "without repeating", "at most k flips", "longest streak"],
"sw-shortest": ["minimum length", "shortest subarray", "smallest window", "containing all characters", "sum at least target"],
"sw-exact": ["exactly k", "count subarrays with k distinct", "number of subarrays having k odd"],
"sw-deque": ["maximum of every window", "sliding window maximum", "max minus min within limit", "each window of size k maximum"],
"ps-range": ["range sum query", "many queries", "sum from l to r", "array does not change"],
"ps-count": ["number of subarrays with sum k", "divisible by k", "count subarrays", "equal number of 0s and 1s", "subarray XOR equals k", "negatives allowed"],
"ps-longest": ["longest subarray with sum k", "contiguous array", "longest with equal counts", "shortest with sum, negatives"],
"ps-2d": ["submatrix sum", "matrix range query", "rectangle sum", "many rectangle queries"],
"ps-diff": ["add v to range", "range updates", "l r v operations", "bookings", "car pooling", "final array after updates"],
"ps-suffix": ["product except self", "left and right", "everything except itself", "trapping rain water", "best split point"],
"bs-exact": ["sorted, find target", "search in a sorted", "search a 2D matrix", "O(log n) required"],
"bs-bound": ["first occurrence", "last occurrence", "insert position", "count less than or equal", "first bad"],
"bs-answer": ["minimum possible maximum", "maximum possible minimum", "smallest speed such that", "ship within d days", "minimise the largest", "k-th smallest by counting"],
"bs-rotated": ["rotated sorted", "pivot", "mountain array", "peak element", "bitonic"],
"bs-partition": ["median of two sorted arrays", "k-th of two sorted", "partition two arrays"],
"hs-seen": ["contains duplicate", "first repeated", "already seen", "exists in", "longest consecutive sequence", "unique"],
"hs-freq": ["most frequent", "count occurrences", "anagram", "can be rearranged", "first unique", "frequency"],
"hs-index": ["two sum", "return indices", "distance between same values", "nearby duplicate", "last seen position"],
"hs-group": ["group anagrams", "group by", "same pattern", "isomorphic", "canonical form", "bucket by"],
"hs-cyclic": ["numbers from 1 to n", "first missing positive", "find the missing", "find the duplicate", "O(1) extra space and values in range"],
"ms-next": ["next greater", "next smaller", "days until warmer", "stock span", "previous smaller", "first taller to the right"],
"ms-hist": ["largest rectangle", "histogram", "maximal rectangle", "trapped water", "bars"],
"ms-match": ["valid parentheses", "balanced brackets", "evaluate expression", "decode string", "undo", "nested", "simplify path"],
"ms-greedy": ["remove k digits", "smallest possible after removing", "lexicographically smallest subsequence", "remove duplicate letters", "keep order"],
"hp-topk": ["top k", "k largest", "k most frequent", "k-th largest in a stream", "k closest"],
"hp-merge": ["merge k sorted", "k sorted lists", "smallest range covering k lists", "k-th smallest in sorted matrix"],
"hp-two": ["median of a stream", "running median", "data stream", "balance two halves"],
"hp-greedy": ["always pick the largest", "most urgent", "task scheduler", "reorganize string", "cheapest next", "minimum cost to connect ropes", "meeting rooms with a heap"],
"iv-merge": ["merge overlapping", "overlapping intervals", "combine ranges", "start and end times"],
"iv-insert": ["insert interval", "already sorted non-overlapping", "add a new interval"],
"iv-greedy": ["maximum non-overlapping", "minimum removals", "activity selection", "fewest arrows", "maximum meetings"],
"iv-sweep": ["how many at once", "maximum overlap", "meeting rooms needed", "platforms required", "peak", "population at any time"],
"iv-sortkey": ["custom sort", "form the largest number", "sort by", "assign in order", "after sorting becomes easy"],
"bt-xor": ["appears once", "every other appears twice", "single number", "missing number via XOR", "pairs cancel"],
"bt-subsets": ["n ≤ 20", "all subsets", "try every subset", "bitmask"],
"bt-dp": ["n ≤ 20", "visit all", "assign tasks to people", "which items have been used", "minimum cost permutation"],
"bt-tricks": ["count set bits", "power of two", "lowest set bit", "reverse bits", "without using + or −", "AND of range"],
"sm-kmp": ["pattern in text", "repeated substring", "longest prefix which is also suffix", "strStr", "occurrences of pattern"],
"sm-rabinkarp": ["rolling hash", "duplicate substring", "repeated DNA", "compare substrings fast"],
"sm-z": ["match with prefix", "prefix at every position", "z-function"],
"st-range": ["range query with updates", "update value at index", "range minimum", "point update"],
"st-fenwick": ["prefix sum with updates", "count smaller after updates", "binary indexed tree", "dynamic rank"],
"st-lazy": ["range update and range query", "add to range and query range", "lazy"],
"sim-spiral": ["spiral", "boundary", "layer by layer", "clockwise traversal", "diagonal order"],
"sim-rotate": ["rotate image", "rotate matrix 90", "transpose", "in place on a matrix"],
"sim-marking": ["set matrix zeroes", "entire row and column", "without using extra space", "update simultaneously"],
"ll-fastslow": ["cycle", "loop", "middle of the linked list", "palindrome linked list", "start of the loop"],
"ll-reverse": ["reverse the list", "reverse between", "reverse in groups of k", "swap pairs", "reorder list"],
"ll-dummy": ["delete node", "remove elements", "partition list", "head may change", "odd even"],
"ll-merge": ["merge two sorted lists", "merge k sorted lists", "sort a linked list", "add two numbers"],
"td-up": ["height", "depth", "balanced", "same tree", "subtree sum", "count nodes"],
"td-down": ["root to leaf", "path sum", "pass value to children", "good nodes", "maximum on the path"],
"td-bst": ["binary search tree", "BST", "k-th smallest in BST", "validate BST", "inorder is sorted"],
"td-lca": ["lowest common ancestor", "LCA", "first common parent", "distance between two nodes"],
"tb-levels": ["level order", "each level", "zigzag", "right side view", "minimum depth", "average of levels"],
"tr-basic": ["prefix", "startsWith", "dictionary", "autocomplete", "implement trie", "longest common prefix"],
"tr-search": ["word search II", "many words on a board", "wildcard dictionary", "search with '.'"],
"gr-flood": ["number of islands", "connected cells", "flood fill", "area of island", "regions"],
"gr-bfs": ["shortest path in a binary matrix", "minimum steps", "fewest moves", "maze", "knight moves"],
"gr-multi": ["rotting oranges", "distance to nearest", "spreads every minute", "all sources at once", "01 matrix", "simultaneously"],
"to-kahn": ["prerequisites", "course schedule", "order of tasks", "dependencies", "build order", "alien dictionary"],
"to-dfs": ["detect cycle in a directed graph", "safe states", "recursion stack", "topological order with DFS"],
"sp-dijkstra": ["shortest path", "minimum time", "network delay", "weighted edges", "non-negative weights"],
"sp-bellman": ["negative weights", "at most k stops", "cheapest flights", "negative cycle"],
"sp-floyd": ["every pair", "all pairs shortest", "n ≤ 400", "city with fewest neighbours"],
"dsu-connect": ["union", "merge groups", "accounts merge", "are they connected", "online connectivity", "number of components after each"],
"dsu-cycle": ["redundant connection", "extra edge", "cycle in an undirected graph", "edge that closes a loop"],
"dsu-kruskal": ["minimum spanning tree", "connect all cities at minimum cost", "sort edges by weight"],
"dp-linear": ["climbing stairs", "number of ways to reach", "no two adjacent", "house robber", "minimum cost to reach the top"],
"dp-kadane": ["maximum subarray", "largest sum contiguous", "maximum product subarray", "best contiguous"],
"dp-coin": ["unlimited supply", "coin change", "minimum coins", "number of combinations", "rod cutting", "perfect squares"],
"dp-lis": ["longest increasing subsequence", "longest chain", "Russian doll", "box stacking", "number of LIS"],
"dp-grid": ["only right or down", "unique paths", "minimum path sum", "triangle", "dungeon", "maximal square"],
"dp-twostring": ["longest common subsequence", "edit distance", "insert, delete, replace", "two strings", "shortest common supersequence", "distinct subsequences", "wildcard matching"],
"dp-knapsack": ["each item once", "subset sum", "partition equal", "capacity", "target sum", "0/1"],
"dp-interval": ["burst balloons", "matrix chain", "merge stones", "minimum cost to cut", "palindromic subsequence", "order of operations"],
"bk-subsets": ["all subsets", "all combinations", "combination sum", "power set", "choose k"],
"bk-perms": ["all permutations", "all arrangements", "next arrangement", "order matters"],
"bk-board": ["N-Queens", "sudoku", "word search", "rat in a maze", "place on the board"],
"gr-reach": ["jump game", "can you reach the end", "minimum jumps", "minimum refuels", "tap watering"],
"gr-pair": ["boats", "pair the heaviest with the lightest", "assign cookies", "minimum number of boats", "match from both ends"],
"gr-local": ["maximise profit by choosing", "IPO", "at each step take the best", "best immediate", "task with deadlines"],
}


def apply(PATTERNS, GROUPS):
    by = {p["id"]: p for p in PATTERNS}
    for pid, (variants, recog, picks) in ADD.items():
        p = by[pid]
        p["variants"] += variants
        p["recognise"] = p["recognise"] + recog
        p["pick"] = (p.get("pick") or []) + picks
    for g in NEW_GROUPS:
        GROUPS.append(g)
    for p in NEW:
        if p["id"] == "graph-walk":
            at = next(i for i, x in enumerate(PATTERNS) if x["id"] == "grid")
            PATTERNS.insert(at, p)
        else:
            PATTERNS.append(p)
    missing = []
    for p in PATTERNS:
        for v in p["variants"]:
            v.setdefault("rare", False)
            if v["id"] in KEYS:
                v["keys"] = KEYS[v["id"]]
            if not v.get("keys"):
                missing.append(v["id"])
    assert not missing, "variants without keywords: %s" % missing
