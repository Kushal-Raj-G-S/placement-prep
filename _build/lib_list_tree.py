# -*- coding: utf-8 -*-
"""Learn content: linked lists and trees.  Imported by pattern_library.py."""

PATTERNS = [

# --------------------------------------------------------------- linked lists ------
{
 "id": "linked-list", "group": "list", "name": "Linked list surgery",
 "buys": "O(n) extra space for an array copy → O(1), by rewiring pointers in place",
 "lives": "singly linked list (and doubly, for LRU-style caches)",
 "core": "You cannot index a linked list, so every classic trick manufactures the index you need out of "
         "pointers: two pointers at different speeds find the middle and the cycle, a pointer k ahead finds "
         "the k-th from the end, and a dummy head removes every 'what if it is the first node' branch. "
         "Draw three nodes on paper before you write any of it.",
 "recognise": [
   {"cue": "<b>cycle</b>, 'does it loop', 'where does the loop start'", "note": "fast and slow pointers"},
   {"cue": "<b>middle</b> node, or the <b>k-th from the end</b>", "note": "you cannot index, so stagger two pointers"},
   {"cue": "<b>reverse</b> the list, part of it, or in groups of k", "note": "the three-pointer rewire"},
   {"cue": "<b>delete / insert</b> and the head itself might change", "note": "dummy head"},
   {"cue": "<b>merge</b> two or k sorted lists", "note": "dummy head + one pointer per list"},
 ],
 "notwhen": [
   "You may use O(n) memory and the problem is really about values → copy to an array and solve it there; "
   "say so out loud in an interview, then do the in-place version.",
   "You need random access or sorting by index → wrong data structure for the job.",
 ],
 "pick": [
   {"if": "find a position you cannot index (middle, k-th from end, cycle)", "then": "ll-fastslow"},
   {"if": "reverse the whole list, a sublist, or every k nodes", "then": "ll-reverse"},
   {"if": "delete or insert where the head may change", "then": "ll-dummy"},
   {"if": "combine sorted lists", "then": "ll-merge"},
 ],
 "variants": [
  {"id": "ll-fastslow", "name": "Fast and slow pointers",
   "when": "You need a position you cannot compute by index.",
   "tool": "slow moves 1 step, fast moves 2 — or fast starts k nodes ahead",
   "invariant": "when fast reaches the end, slow is exactly at the middle (or k from the end)",
   "cx": "O(n) time, O(1) space",
   "code": """def middle(head):
    slow = fast = head
    while fast and fast.next:        # guard BOTH, or you dereference None
        slow = slow.next
        fast = fast.next.next
    return slow                       # for even length this is the SECOND middle

def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            return True               # a 2x runner must lap a 1x runner inside a loop
    return False""",
   "asks": [
     "linked list cycle — detect it, and find where it starts (reset one pointer to the head, step both by 1)",
     "middle of the linked list",
     "remove the n-th node from the end (one pass, two pointers n apart)",
     "palindrome linked list (find the middle, reverse the second half, compare)",
     "happy number — the same cycle detection over a number sequence",
     "find the duplicate number in an array treated as a linked list",
     "reorder list — middle, reverse, interleave",
   ],
   "examples": [
     {"n": "Linked List Cycle", "s": "LC 141"},
     {"n": "Linked List Cycle II", "s": "LC 142"},
     {"n": "Middle of the Linked List", "s": "LC 876"},
     {"n": "Remove Nth Node From End of List", "s": "LC 19"},
     {"n": "Palindrome Linked List", "s": "LC 234"},
     {"n": "Find the Duplicate Number", "s": "LC 287"},
     {"n": "Reorder List", "s": "LC 143"},
   ],
   "traps": [
     "<code>while fast and fast.next</code> — checking only one of them crashes on even-length lists.",
     "Even length gives the SECOND middle. If you need the first, stop one step earlier.",
     "Cycle START needs a second phase: reset one pointer to the head and advance both by one. Knowing "
     "<i>that</i> there is a cycle is not knowing where it begins.",
   ]},

  {"id": "ll-reverse", "name": "Reverse by rewiring",
   "when": "Reverse the list, a sublist, or every group of k.",
   "tool": "prev, cur, nxt — save the next node BEFORE you overwrite the pointer",
   "invariant": "everything before cur is already reversed and ends at prev",
   "cx": "O(n) time, O(1) space",
   "code": """def reverse(head):
    prev, cur = None, head
    while cur:
        nxt = cur.next        # save it FIRST -- you are about to destroy it
        cur.next = prev
        prev = cur
        cur = nxt
    return prev               # prev is the new head""",
   "asks": [
     "reverse a linked list (iterative and recursive)",
     "reverse a sublist between positions m and n",
     "reverse nodes in k-group, and the 'leave the remainder alone' variant",
     "swap nodes in pairs",
     "palindrome check and reorder list — both need the second half reversed",
     "add two numbers stored in forward order (reverse, add, reverse back)",
     "rotate list by k places",
   ],
   "examples": [
     {"n": "Reverse Linked List", "s": "LC 206"},
     {"n": "Reverse Linked List II", "s": "LC 92"},
     {"n": "Reverse Nodes in k-Group", "s": "LC 25"},
     {"n": "Swap Nodes in Pairs", "s": "LC 24"},
     {"n": "Rotate List", "s": "LC 61"},
     {"n": "Add Two Numbers II", "s": "LC 445"},
   ],
   "traps": [
     "Saving <code>nxt</code> first is the whole trick. Overwrite <code>cur.next</code> before saving and the rest of the list is gone.",
     "Return <code>prev</code>, not <code>cur</code> — cur is None when the loop ends.",
     "For a sublist, keep a pointer to the node BEFORE the section and to the section's original head; those two get rewired at the end.",
   ]},

  {"id": "ll-dummy", "name": "Dummy head",
   "when": "Deleting or inserting, and the head itself might be affected.",
   "tool": "a fake node in front of the real head, so every node has a predecessor",
   "invariant": "every node you touch has a previous node — no special case for position 0",
   "cx": "O(n) time, O(1) space",
   "code": """def remove_all(head, val):
    dummy = ListNode(0, head)        # the whole point: head now has a predecessor
    prev = dummy
    while prev.next:
        if prev.next.val == val:
            prev.next = prev.next.next   # unlink, and do NOT advance
        else:
            prev = prev.next
    return dummy.next""",
   "asks": [
     "remove linked list elements by value",
     "remove duplicates from a sorted list (keep one, or remove every duplicated value entirely)",
     "partition list around a value (two dummy heads, then join)",
     "odd-even linked list",
     "insert into a sorted circular list",
     "delete the n-th node from the end without a length pass",
   ],
   "examples": [
     {"n": "Remove Linked List Elements", "s": "LC 203"},
     {"n": "Remove Duplicates from Sorted List II", "s": "LC 82"},
     {"n": "Partition List", "s": "LC 86"},
     {"n": "Odd Even Linked List", "s": "LC 328"},
   ],
   "traps": [
     "After unlinking, do NOT advance prev — the new <code>prev.next</code> has not been checked yet.",
     "Return <code>dummy.next</code>, never the original head: it may have been removed.",
     "Two dummy heads (one per bucket) turn 'partition' into two appends plus one join.",
   ]},

  {"id": "ll-merge", "name": "Merge sorted lists",
   "when": "Two (or k) sorted lists to combine, or a list to sort in place.",
   "tool": "dummy head + a tail pointer; always append the smaller head",
   "invariant": "everything behind tail is sorted and finished",
   "cx": "O(n + m) for two; O(N log k) for k with a heap",
   "code": """def merge_two(a, b):
    dummy = tail = ListNode(0)
    while a and b:
        if a.val <= b.val:
            tail.next, a = a, a.next
        else:
            tail.next, b = b, b.next
        tail = tail.next
    tail.next = a or b          # one list still has a tail -- attach it whole
    return dummy.next""",
   "asks": [
     "merge two sorted lists",
     "merge k sorted lists (heap of heads, or repeated pairwise merging)",
     "sort a linked list in O(n log n) and O(1) space — merge sort, using the fast/slow split",
     "intersection of two linked lists",
     "add two numbers as linked lists",
     "flatten a multilevel doubly linked list",
   ],
   "examples": [
     {"n": "Merge Two Sorted Lists", "s": "LC 21"},
     {"n": "Merge k Sorted Lists", "s": "LC 23"},
     {"n": "Sort List", "s": "LC 148"},
     {"n": "Intersection of Two Linked Lists", "s": "LC 160"},
     {"n": "Add Two Numbers", "s": "LC 2"},
   ],
   "traps": [
     "<code>tail.next = a or b</code> at the end — forgetting the leftover tail silently truncates the result.",
     "Merge sort beats quicksort on a list: the split is free with fast/slow and you never need random access.",
     "<code>&lt;=</code> rather than <code>&lt;</code> keeps the merge stable.",
   ]},
 ]},

# --------------------------------------------------------------------- trees -------
{
 "id": "tree-dfs", "group": "tree", "name": "Tree DFS (recursion with a shape)",
 "buys": "every node visited exactly once — O(n), with the recursion stack doing the bookkeeping",
 "lives": "binary tree, n-ary tree, BST",
 "core": "Almost every tree question is one of two shapes. Either information flows UP — each node asks its "
         "children for a value and combines them (height, sum, diameter) — or information flows DOWN, the "
         "parent handing the child context (the path so far, a valid range). Decide which direction you need "
         "before writing a line, because it decides your function's signature.",
 "recognise": [
   {"cue": "<b>height, depth, diameter, balanced, sum</b> of the tree", "note": "value flows UP — post-order"},
   {"cue": "<b>path from the root</b>, 'path sum equals target', 'good nodes'", "note": "value flows DOWN"},
   {"cue": "<b>BST</b>, and the question involves order or the k-th element", "note": "in-order traversal is sorted"},
   {"cue": "<b>lowest common ancestor</b>, 'the path between two nodes'", "note": "the post-order LCA shape"},
   {"cue": "'the best path <b>through</b> any node'", "note": "return one branch upward, record both branches locally"},
 ],
 "notwhen": [
   "You need everything at depth d together → that is <b>BFS</b>, not DFS.",
   "The structure has cycles → it is a graph; you need a visited set.",
   "Depth can reach 10⁵ → Python's recursion limit will blow; convert to an explicit stack.",
 ],
 "pick": [
   {"if": "the answer is built from the children's answers", "then": "td-up"},
   {"if": "each node needs to know about its ancestors", "then": "td-down"},
   {"if": "it is a BST and order matters", "then": "td-bst"},
   {"if": "two nodes, and the relationship between them", "then": "td-lca"},
 ],
 "variants": [
  {"id": "td-up", "name": "Post-order — return a value up",
   "when": "A node's answer depends only on its children's answers.",
   "tool": "recurse left, recurse right, combine, return",
   "invariant": "by the time you combine, both subtrees have already reported correctly",
   "cx": "O(n) time, O(h) stack",
   "code": """def height(node):
    if not node:
        return 0                       # the base case IS the empty tree
    return 1 + max(height(node.left), height(node.right))

# the 'best path THROUGH a node' shape -- note the two DIFFERENT values
best = 0
def gain(node):
    global best
    if not node: return 0
    l = max(gain(node.left), 0)        # a negative branch is worth skipping
    r = max(gain(node.right), 0)
    best = max(best, node.val + l + r) # record a path through this node
    return node.val + max(l, r)        # but return only ONE branch upward""",
   "asks": [
     "maximum depth / minimum depth of a binary tree",
     "diameter of a binary tree",
     "balanced binary tree (return height and a flag, or −1 as a sentinel)",
     "binary tree maximum path sum",
     "count nodes, sum of all nodes, count leaves",
     "same tree, symmetric tree, subtree of another tree",
     "invert a binary tree; merge two binary trees",
     "house robber III (return a pair: best-with-me, best-without-me)",
     "count good nodes, longest univalue path",
   ],
   "examples": [
     {"n": "Maximum Depth of Binary Tree", "s": "LC 104"},
     {"n": "Diameter of Binary Tree", "s": "LC 543"},
     {"n": "Balanced Binary Tree", "s": "LC 110"},
     {"n": "Binary Tree Maximum Path Sum", "s": "LC 124"},
     {"n": "Same Tree", "s": "LC 100"},
     {"n": "Symmetric Tree", "s": "LC 101"},
     {"n": "Invert Binary Tree", "s": "LC 226"},
     {"n": "House Robber III", "s": "LC 337"},
   ],
   "traps": [
     "The 'through a node' problems return ONE branch but record BOTH. Returning the two-branch value corrupts the parent.",
     "<code>max(child, 0)</code> is how you let the recursion drop a harmful branch.",
     "Returning a tuple (or a −1 sentinel) avoids recomputing height inside the balanced check, turning O(n²) into O(n).",
   ]},

  {"id": "td-down", "name": "Top-down — carry context into the children",
   "when": "A node's answer depends on where it sits, not on its subtree.",
   "tool": "extra parameters: the running path, the remaining target, the allowed range",
   "invariant": "the parameters always describe the path from the root to this node",
   "cx": "O(n) time, O(h) stack",
   "code": """def path_sum(node, target, path, out):
    if not node:
        return
    path.append(node.val)
    if not node.left and not node.right and node.val == target:
        out.append(list(path))         # COPY -- the list is mutated on the way back
    else:
        path_sum(node.left,  target - node.val, path, out)
        path_sum(node.right, target - node.val, path, out)
    path.pop()                          # undo before returning to the parent""",
   "asks": [
     "path sum I / II / III (root-to-leaf, all paths, any downward path)",
     "binary tree paths — print every root-to-leaf path",
     "sum root to leaf numbers",
     "count good nodes (the max value seen on the path so far)",
     "maximum difference between a node and an ancestor",
     "validate a BST by passing down the allowed (low, high) range",
     "smallest string starting from a leaf",
   ],
   "examples": [
     {"n": "Path Sum", "s": "LC 112"},
     {"n": "Path Sum II", "s": "LC 113"},
     {"n": "Binary Tree Paths", "s": "LC 257"},
     {"n": "Sum Root to Leaf Numbers", "s": "LC 129"},
     {"n": "Count Good Nodes in Binary Tree", "s": "LC 1448"},
     {"n": "Maximum Difference Between Node and Ancestor", "s": "LC 1026"},
   ],
   "traps": [
     "Append a COPY of the path, not the list itself — otherwise every answer ends up identical and empty.",
     "<code>path.pop()</code> on the way out. Forgetting it is the classic backtracking leak.",
     "'Leaf' means no left AND no right. A node with one child is not a leaf, and that check fails a lot of submissions.",
   ]},

  {"id": "td-bst", "name": "BST — in-order is sorted",
   "when": "A binary SEARCH tree, and the question is about order or searching.",
   "tool": "in-order traversal (left, node, right) emits values in ascending order",
   "invariant": "everything left is smaller and everything right is larger — at EVERY node, not just the parent",
   "cx": "O(h) for a search, O(n) for a full traversal",
   "code": """def kth_smallest(root, k):
    st, cur = [], root
    while st or cur:
        while cur:                 # go as far left as possible
            st.append(cur); cur = cur.left
        cur = st.pop()
        k -= 1
        if k == 0: return cur.val  # the k-th value popped is the k-th smallest
        cur = cur.right""",
   "asks": [
     "validate a binary search tree (range method, or 'is the in-order strictly increasing')",
     "k-th smallest / k-th largest element in a BST",
     "search, insert and delete in a BST",
     "convert a sorted array to a height-balanced BST",
     "lowest common ancestor in a BST (compare values — no need to recurse into both sides)",
     "minimum absolute difference in a BST; two sum on a BST",
     "range sum of a BST; trim a BST to a range",
     "recover a BST where two nodes were swapped",
   ],
   "examples": [
     {"n": "Validate Binary Search Tree", "s": "LC 98"},
     {"n": "Kth Smallest Element in a BST", "s": "LC 230"},
     {"n": "Lowest Common Ancestor of a Binary Search Tree", "s": "LC 235"},
     {"n": "Convert Sorted Array to Binary Search Tree", "s": "LC 108"},
     {"n": "Range Sum of BST", "s": "LC 938"},
     {"n": "Delete Node in a BST", "s": "LC 450"},
   ],
   "traps": [
     "Validating against only the parent is WRONG — the constraint covers the whole subtree. Pass a (low, high) range down.",
     "Equal values: the statement decides whether duplicates go left, right, or are forbidden. It always says.",
     "The iterative in-order with an explicit stack is worth memorising — it is also the 'BST iterator' answer.",
   ]},

  {"id": "td-lca", "name": "Lowest common ancestor",
   "when": "Two nodes, and you need the lowest node with both beneath it.",
   "tool": "post-order: if both sides report a hit, THIS node is the answer",
   "invariant": "a node returns non-null exactly when p or q lies in its subtree",
   "cx": "O(n) time, O(h) stack",
   "code": """def lca(node, p, q):
    if not node or node is p or node is q:
        return node                     # found one -- report it upward
    l = lca(node.left,  p, q)
    r = lca(node.right, p, q)
    if l and r:
        return node                     # p and q split here -> this IS the LCA
    return l or r                       # otherwise pass the single hit upward""",
   "asks": [
     "lowest common ancestor of a binary tree (and the easier BST version)",
     "distance between two nodes = depth(p) + depth(q) − 2·depth(lca)",
     "all nodes at distance K from a target (build a parent map, then BFS)",
     "the path between two nodes; step-by-step directions from one node to another",
     "lowest common ancestor of the deepest leaves",
     "LCA with parent pointers (walk up both and intersect, like two linked lists)",
   ],
   "examples": [
     {"n": "Lowest Common Ancestor of a Binary Tree", "s": "LC 236"},
     {"n": "All Nodes Distance K in Binary Tree", "s": "LC 863"},
     {"n": "Step-By-Step Directions From a Binary Tree Node to Another", "s": "LC 2096"},
     {"n": "Lowest Common Ancestor of Deepest Leaves", "s": "LC 1123"},
   ],
   "traps": [
     "This version assumes both nodes EXIST. If they might not, you must also count how many you found.",
     "'Distance K from a node' needs upward movement, so turn the tree into a graph with a parent map and run BFS.",
   ]},
 ]},

{
 "id": "tree-bfs", "group": "tree", "name": "Tree BFS (level order)",
 "buys": "the shallowest answer first — and whole levels as units, which DFS cannot give you",
 "lives": "binary tree, n-ary tree",
 "core": "A queue, and the one move that matters: before each round, record how many nodes are in the queue. "
         "That count IS the current level, so you process exactly one level per iteration. Everything "
         "'per level' falls out of that single line.",
 "recognise": [
   {"cue": "<b>level order</b>, 'level by level', 'each row'", "note": "the definition"},
   {"cue": "<b>right side view</b>, largest value per level, average per level", "note": "last / best of each level"},
   {"cue": "<b>minimum depth</b>, 'shallowest leaf'", "note": "BFS finds it first and can stop immediately"},
   {"cue": "<b>zigzag</b> / spiral order", "note": "level order, reversing alternate rows"},
   {"cue": "<b>connect next pointers</b>, 'width of the tree'", "note": "needs whole levels at once"},
 ],
 "notwhen": [
   "The answer is about a root-to-leaf path or a subtree → DFS carries that context naturally.",
   "You need the deepest thing — DFS is usually simpler there.",
 ],
 "pick": [
   {"if": "anything phrased per level", "then": "tb-levels"},
 ],
 "variants": [
  {"id": "tb-levels", "name": "Queue, one level per round",
   "when": "Any question phrased per level, or 'the shallowest'.",
   "tool": "a deque; snapshot <code>len(queue)</code> at the top of each round",
   "invariant": "each round of the outer loop handles exactly one complete level",
   "cx": "O(n) time, O(width) space",
   "code": """from collections import deque
def level_order(root):
    if not root: return []
    q, out = deque([root]), []
    while q:
        n = len(q)                 # THIS line is the whole pattern
        level = []
        for _ in range(n):
            node = q.popleft()
            level.append(node.val)
            if node.left:  q.append(node.left)
            if node.right: q.append(node.right)
        out.append(level)
    return out""",
   "asks": [
     "binary tree level order traversal, and bottom-up level order",
     "zigzag / spiral level order",
     "right side view, left side view",
     "average, maximum or sum of each level",
     "minimum depth of a binary tree (BFS returns the moment it meets a leaf)",
     "populating next right pointers in each node",
     "maximum width of a binary tree (index the nodes 2i / 2i+1)",
     "cousins in a binary tree; deepest leaves sum",
     "vertical order traversal (BFS plus a column index)",
   ],
   "examples": [
     {"n": "Binary Tree Level Order Traversal", "s": "LC 102"},
     {"n": "Binary Tree Zigzag Level Order Traversal", "s": "LC 103"},
     {"n": "Binary Tree Right Side View", "s": "LC 199"},
     {"n": "Minimum Depth of Binary Tree", "s": "LC 111"},
     {"n": "Populating Next Right Pointers in Each Node", "s": "LC 116"},
     {"n": "Maximum Width of Binary Tree", "s": "LC 662"},
     {"n": "Average of Levels in Binary Tree", "s": "LC 637"},
   ],
   "traps": [
     "Snapshot the length BEFORE the inner loop. Reading <code>len(q)</code> inside it mixes two levels together.",
     "Use <code>collections.deque</code>; <code>list.pop(0)</code> is O(n) and turns the whole thing into O(n²).",
     "Minimum depth via DFS must handle one-child nodes carefully; BFS sidesteps it entirely.",
   ]},
 ]},

{
 "id": "trie", "group": "tree", "name": "Trie (prefix tree)",
 "buys": "O(words · L) scanning everything → O(L) per query, independent of how many words you stored",
 "lives": "strings sharing prefixes; also bits, for XOR problems",
 "core": "One node per character position, children keyed by the next character. Walking down spells a word, "
         "so 'does any stored word start with this prefix' costs the length of the prefix and nothing else. "
         "The same structure over BITS (children 0 and 1) answers maximum-XOR questions.",
 "recognise": [
   {"cue": "<b>prefix</b>, autocomplete, 'words starting with'", "note": "the definition"},
   {"cue": "<b>a dictionary of many words</b> queried repeatedly", "note": "build once, query cheaply"},
   {"cue": "word search in a <b>grid with many target words</b>", "note": "trie + DFS prunes dead branches instantly"},
   {"cue": "<b>maximum XOR</b> pair, 'two numbers with the biggest xor'", "note": "binary trie, greedy from the top bit"},
 ],
 "notwhen": [
   "There is one word, or a handful → a set or direct comparison is simpler.",
   "You need suffixes or substring search → that is a suffix structure, or KMP / Z-algorithm.",
 ],
 "pick": [
   {"if": "insert, search, and prefix queries", "then": "tr-basic"},
   {"if": "wildcards, or pruning a search with a dictionary", "then": "tr-search"},
 ],
 "variants": [
  {"id": "tr-basic", "name": "Insert / search / startsWith",
   "when": "A dictionary queried by exact word or by prefix.",
   "tool": "a dict of children per node, plus an end-of-word flag",
   "invariant": "the path from the root to a node spells exactly that node's prefix",
   "cx": "O(L) per operation, O(total characters) space",
   "code": """class Trie:
    def __init__(self):
        self.ch = {}            # character -> Trie
        self.end = False        # a word ENDS here (not merely passes through)
    def insert(self, w):
        node = self
        for c in w:
            node = node.ch.setdefault(c, Trie())
        node.end = True
    def _walk(self, w):
        node = self
        for c in w:
            if c not in node.ch: return None
            node = node.ch[c]
        return node
    def search(self, w):
        node = self._walk(w)
        return node is not None and node.end
    def startsWith(self, p):
        return self._walk(p) is not None""",
   "asks": [
     "implement a trie — insert, search, startsWith",
     "autocomplete / search suggestions system",
     "longest common prefix of a list of words",
     "replace words with their shortest root (dictionary of roots)",
     "map sum pairs; index pairs of a string",
     "maximum XOR of two numbers (a trie over the bits, taking the opposite bit at each level)",
     "camelcase matching, prefix and suffix search",
   ],
   "examples": [
     {"n": "Implement Trie (Prefix Tree)", "s": "LC 208"},
     {"n": "Replace Words", "s": "LC 648"},
     {"n": "Search Suggestions System", "s": "LC 1268"},
     {"n": "Maximum XOR of Two Numbers in an Array", "s": "LC 421"},
     {"n": "Longest Common Prefix", "s": "LC 14"},
   ],
   "traps": [
     "The <code>end</code> flag is not optional: without it 'app' matches when only 'apple' was inserted.",
     "<code>setdefault</code> (or defaultdict) keeps insert to four lines.",
     "A dict of children beats a 26-slot array when the alphabet is large or sparse; the array wins when it is dense.",
   ]},

  {"id": "tr-search", "name": "Trie as a search pruner",
   "when": "Many candidate words, and a search that would otherwise explore dead ends.",
   "tool": "walk the trie alongside the search; the moment there is no child, stop",
   "invariant": "you only ever explore prefixes that at least one real word still matches",
   "cx": "O(cells · 4^L) worst case, but pruned enormously in practice",
   "code": """def find_words(board, words):
    root = Trie()
    for w in words: root.insert(w)
    out, R, C = set(), len(board), len(board[0])
    def dfs(r, c, node, path):
        ch = board[r][c]
        if ch not in node.ch: return          # DEAD END -- the whole point
        nxt = node.ch[ch]
        if nxt.end: out.add(path + ch)
        board[r][c] = "#"                      # mark visited
        for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and board[nr][nc] != "#":
                dfs(nr, nc, nxt, path + ch)
        board[r][c] = ch                       # restore
    for r in range(R):
        for c in range(C):
            dfs(r, c, root, "")
    return list(out)""",
   "asks": [
     "word search II — find every dictionary word in a grid",
     "add and search word with '.' wildcards (recurse over all children on a dot)",
     "word break / word break II with a large dictionary",
     "concatenated words; longest word in a dictionary built one letter at a time",
     "stream of characters — has any word just ended (store the words reversed)",
     "palindrome pairs",
   ],
   "examples": [
     {"n": "Word Search II", "s": "LC 212"},
     {"n": "Design Add and Search Words Data Structure", "s": "LC 211"},
     {"n": "Word Break II", "s": "LC 140"},
     {"n": "Stream of Characters", "s": "LC 1032"},
     {"n": "Concatenated Words", "s": "LC 472"},
   ],
   "traps": [
     "Restore the cell after recursing, or the grid is destroyed for the next start square.",
     "On a '.' wildcard you must try EVERY child, not just one.",
     "Use a set for the output — the same word can be reached by two different paths.",
     "For a stream, insert the words REVERSED and walk backwards from the newest character.",
   ]},
 ]},
]
