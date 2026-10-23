# -*- coding: utf-8 -*-
"""Learn content: graphs, grids, ordering, shortest paths, union-find."""

PATTERNS = [

# ------------------------------------------------------------------ grids ---------
{
 "id": "grid", "group": "graph", "name": "Grid traversal (a grid IS a graph)",
 "buys": "the brute-force 'try every path' blow-up → O(rows · cols), each cell visited once",
 "lives": "2-D grid of cells, where neighbours are up/down/left/right (sometimes the 8 diagonals too)",
 "core": "Stop seeing a matrix and start seeing a graph: each cell is a node, each legal move is an edge. "
         "Then the only question left is which traversal. DFS or BFS both label connected regions; BFS alone "
         "gives you SHORTEST, because it finishes a whole distance ring before starting the next one.",
 "recognise": [
   {"cue": "<b>islands</b>, regions, connected blobs, flood fill, 'how many groups'", "note": "DFS or BFS, either works"},
   {"cue": "<b>fewest steps</b> / shortest path / minimum moves on a grid", "note": "BFS — and only BFS"},
   {"cue": "<b>everything spreads at once</b> (rot, fire, water, infection)", "note": "multi-source BFS"},
   {"cue": "<b>distance to the nearest</b> X for every cell", "note": "multi-source BFS from all the X's"},
   {"cue": "'can I reach the edge', 'surrounded regions'", "note": "flood fill INWARD from the border"},
 ],
 "notwhen": [
   "Moves have different COSTS → plain BFS is wrong; use Dijkstra (or 0-1 BFS with a deque).",
   "You may revisit cells with a different budget → the state is (cell, budget), not just the cell.",
   "The answer is a count of paths rather than a reachability → that is grid DP.",
 ],
 "pick": [
   {"if": "label or count connected regions", "then": "gr-flood"},
   {"if": "fewest moves from ONE start", "then": "gr-bfs"},
   {"if": "many sources spreading together, or 'distance to nearest'", "then": "gr-multi"},
 ],
 "variants": [
  {"id": "gr-flood", "name": "Flood fill / connected components",
   "when": "Count or label regions of connected cells.",
   "tool": "DFS (or BFS) from each unvisited cell, sinking the whole region as you go",
   "invariant": "once a cell is marked, it belongs to exactly one region and is never counted again",
   "cx": "O(rows · cols) — every cell is entered at most once",
   "code": """DIRS = ((1,0), (-1,0), (0,1), (0,-1))
def num_islands(g):
    R, C = len(g), len(g[0])
    def sink(r, c):
        if r < 0 or r >= R or c < 0 or c >= C or g[r][c] != "1":
            return                       # one guard, at the TOP -- not at every call site
        g[r][c] = "0"                    # mark BEFORE recursing, or you loop forever
        for dr, dc in DIRS:
            sink(r + dr, c + dc)
    n = 0
    for r in range(R):
        for c in range(C):
            if g[r][c] == "1":
                n += 1                   # a new region starts here
                sink(r, c)
    return n""",
   "asks": [
     "number of islands; max area of an island; count sub-islands",
     "flood fill / paint bucket",
     "surrounded regions (flood INWARD from the border, then flip the rest)",
     "number of closed islands, number of enclaves",
     "island perimeter; number of distinct islands (normalise each shape)",
     "pacific atlantic water flow (two floods, one from each ocean)",
     "making a large island (flip one 0 — label regions, then test each 0's neighbours)",
     "count of connected components in a matrix of friends / provinces",
   ],
   "examples": [
     {"n": "Number of Islands", "s": "LC 200"},
     {"n": "Max Area of Island", "s": "LC 695"},
     {"n": "Flood Fill", "s": "LC 733"},
     {"n": "Surrounded Regions", "s": "LC 130"},
     {"n": "Pacific Atlantic Water Flow", "s": "LC 417"},
     {"n": "Number of Closed Islands", "s": "LC 1254"},
     {"n": "Making A Large Island", "s": "LC 827"},
   ],
   "traps": [
     "Mark the cell visited BEFORE recursing into neighbours, or two adjacent cells call each other forever.",
     "Put the bounds check at the top of the function, not at each of the four call sites — four chances to get it wrong.",
     "A 1000×1000 grid can blow Python's recursion limit; use an explicit stack or BFS.",
     "'Surrounded regions' is solved by flooding from the BORDER inward, not by scanning the middle.",
   ]},

  {"id": "gr-bfs", "name": "BFS — fewest moves from one start",
   "when": "Minimum number of steps, and every step costs the same.",
   "tool": "a queue plus a visited set; count distance by level, exactly like tree BFS",
   "invariant": "when a cell is first dequeued, the distance recorded is the shortest possible",
   "cx": "O(rows · cols)",
   "code": """from collections import deque
def shortest(g, start, goal):
    R, C = len(g), len(g[0])
    q = deque([start]); seen = {start}; steps = 0
    while q:
        for _ in range(len(q)):          # one whole ring per round = one step
            r, c = q.popleft()
            if (r, c) == goal: return steps
            for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < R and 0 <= nc < C and g[nr][nc] != "#" and (nr,nc) not in seen:
                    seen.add((nr, nc))   # mark on PUSH, never on pop
                    q.append((nr, nc))
        steps += 1
    return -1""",
   "asks": [
     "shortest path in a binary matrix (8 directions)",
     "minimum knight moves on a board",
     "word ladder (each word is a node, one-letter changes are edges)",
     "open the lock / minimum genetic mutation — BFS over states, not cells",
     "shortest path in a grid with obstacle elimination (the state is (r, c, remaining))",
     "jump game III, minimum jumps to reach the end",
     "sliding puzzle (the board layout is the node)",
     "escape a maze, nearest exit from the entrance",
   ],
   "examples": [
     {"n": "Shortest Path in Binary Matrix", "s": "LC 1091"},
     {"n": "Word Ladder", "s": "LC 127"},
     {"n": "Open the Lock", "s": "LC 752"},
     {"n": "Shortest Path in a Grid with Obstacles Elimination", "s": "LC 1293"},
     {"n": "Nearest Exit from Entrance in Maze", "s": "LC 1926"},
     {"n": "Sliding Puzzle", "s": "LC 773"},
   ],
   "traps": [
     "Mark visited when you PUSH, not when you pop — otherwise the same cell is queued many times and the queue explodes.",
     "DFS cannot answer 'shortest' on an unweighted graph. It finds <i>a</i> path, not the short one.",
     "When you may revisit a cell with a different budget, the visited key must include the budget.",
     "A 'state' need not be a cell: a word, a lock combination, or a whole board can be the node.",
   ]},

  {"id": "gr-multi", "name": "Multi-source BFS",
   "when": "Several things spread simultaneously, or every cell needs its distance to the nearest X.",
   "tool": "seed the queue with ALL sources at distance 0, then run one ordinary BFS",
   "invariant": "the first time a cell is reached, it is reached from its nearest source",
   "cx": "O(rows · cols) — the same single pass, no matter how many sources",
   "code": """from collections import deque
def nearest_zero(mat):
    R, C = len(mat), len(mat[0])
    dist = [[-1] * C for _ in range(R)]
    q = deque()
    for r in range(R):
        for c in range(C):
            if mat[r][c] == 0:
                dist[r][c] = 0
                q.append((r, c))      # EVERY source enters before the loop starts
    while q:
        r, c = q.popleft()
        for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and dist[nr][nc] == -1:
                dist[nr][nc] = dist[r][c] + 1
                q.append((nr, nc))
    return dist""",
   "asks": [
     "rotting oranges — minutes until everything rots",
     "01 matrix — distance of each cell to the nearest 0",
     "walls and gates — distance to the nearest gate",
     "as far from land as possible (the maximum distance to any land)",
     "shortest bridge (flood one island, then BFS outward from all of it)",
     "map of highest peak; spreading fire or infection with a time limit",
     "shortest distance from all buildings",
   ],
   "examples": [
     {"n": "Rotting Oranges", "s": "LC 994"},
     {"n": "01 Matrix", "s": "LC 542"},
     {"n": "Walls and Gates", "s": "LC 286"},
     {"n": "As Far from Land as Possible", "s": "LC 1162"},
     {"n": "Shortest Bridge", "s": "LC 934"},
     {"n": "Map of Highest Peak", "s": "LC 1765"},
   ],
   "traps": [
     "Every source must be in the queue BEFORE the loop starts. Running one BFS per source is O(sources · cells) and will time out.",
     "Rotting oranges has to report −1 when something is left unreached — check for survivors at the end.",
     "Counting minutes: either use the level-by-level form, or store the distance in the grid and take the maximum.",
   ]},
 ]},

# ----------------------------------------------------------- topological sort ------
{
 "id": "toposort", "group": "graph", "name": "Topological sort (ordering & cycles)",
 "buys": "a valid order over n tasks in O(V + E), instead of guessing permutations",
 "lives": "directed graph of dependencies (a DAG, if the input is sane)",
 "core": "Whenever the statement says 'before', 'requires', 'prerequisite' or 'depends on', you have a directed "
         "graph and you want an order where every arrow points forward. Kahn's method is the one to memorise: "
         "repeatedly take anything with no remaining prerequisites. If you finish having emitted fewer than n "
         "nodes, the leftovers form a cycle — so the SAME algorithm answers 'is this even possible'.",
 "recognise": [
   {"cue": "<b>prerequisites</b>, 'must come before', dependencies, build order", "note": "the definition"},
   {"cue": "<b>is it possible</b> to finish / 'is there a cycle' in a DIRECTED graph", "note": "count what you emit"},
   {"cue": "<b>alien dictionary</b>, 'deduce the order of the letters'", "note": "build edges from adjacent pairs"},
   {"cue": "<b>longest path in a DAG</b>, 'minimum time to finish all tasks'", "note": "DP along the topological order"},
 ],
 "notwhen": [
   "The graph is UNDIRECTED → cycle detection there is union-find or DFS with a parent check, not topo sort.",
   "You need the shortest path with weights → Dijkstra (unless it is a DAG, where topo order + DP is faster).",
 ],
 "pick": [
   {"if": "produce an order, or detect a cycle, iteratively", "then": "to-kahn"},
   {"if": "you prefer recursion, or need the DFS colouring", "then": "to-dfs"},
 ],
 "variants": [
  {"id": "to-kahn", "name": "Kahn's algorithm (BFS on indegree)",
   "when": "Any ordering or 'is it possible' question. This is the default.",
   "tool": "indegree count per node + a queue of everything currently at indegree 0",
   "invariant": "anything in the queue has all its prerequisites already emitted",
   "cx": "O(V + E)",
   "code": """from collections import deque
def topo(n, edges):                  # edges = [(a, b)] meaning a must come before b
    adj = [[] for _ in range(n)]
    indeg = [0] * n
    for a, b in edges:
        adj[a].append(b)
        indeg[b] += 1
    q = deque(i for i in range(n) if indeg[i] == 0)
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1            # one prerequisite satisfied
            if indeg[v] == 0:
                q.append(v)
    return order if len(order) == n else []   # short -> a cycle exists""",
   "asks": [
     "course schedule — can all courses be finished (cycle detection)",
     "course schedule II — return a valid order",
     "alien dictionary — derive the letter order from a sorted word list",
     "minimum height trees (peel leaves inward, the undirected cousin)",
     "parallel courses / minimum semesters — count the BFS levels",
     "build order, task scheduling with dependencies",
     "sort items by group with dependencies (topo sort twice: groups, then items)",
     "find all possible orderings (topo sort + backtracking)",
   ],
   "examples": [
     {"n": "Course Schedule", "s": "LC 207"},
     {"n": "Course Schedule II", "s": "LC 210"},
     {"n": "Alien Dictionary", "s": "LC 269"},
     {"n": "Minimum Height Trees", "s": "LC 310"},
     {"n": "Parallel Courses", "s": "LC 1136"},
     {"n": "Sort Items by Groups Respecting Dependencies", "s": "LC 1203"},
   ],
   "traps": [
     "Get the edge DIRECTION right. 'To take b you need a' is an edge a→b, and reversing it passes the sample and fails everything else.",
     "The cycle check is <code>len(order) == n</code>. There is no separate cycle pass to write.",
     "Alien dictionary has a trap case: if a longer word comes before its own prefix, the input is invalid regardless of letters.",
     "'Minimum semesters' is the number of BFS ROUNDS, so use the level-by-level form.",
   ]},

  {"id": "to-dfs", "name": "DFS post-order + three-colour cycle check",
   "when": "You prefer recursion, or you want cycle detection with the path visible.",
   "tool": "colours: 0 unvisited, 1 in the current stack, 2 finished. Meeting a 1 means a cycle",
   "invariant": "a node turns 2 only after everything it points to is already 2",
   "cx": "O(V + E)",
   "code": """def topo_dfs(n, adj):
    color = [0] * n           # 0 = new, 1 = on the current path, 2 = done
    order = []
    def dfs(u):
        if color[u] == 1: return False     # back edge -> CYCLE
        if color[u] == 2: return True      # already settled
        color[u] = 1
        for v in adj[u]:
            if not dfs(v): return False
        color[u] = 2
        order.append(u)                     # post-order
        return True
    for i in range(n):
        if not dfs(i): return []
    return order[::-1]                      # reverse the post-order""",
   "asks": [
     "course schedule I / II via DFS",
     "detect a cycle in a directed graph",
     "find eventual safe states (nodes that cannot reach a cycle)",
     "longest path in a DAG; largest colour value in a directed graph",
     "strongly connected components (Kosaraju / Tarjan build on this)",
     "reconstruct itinerary (Hierholzer's post-order, the Eulerian path cousin)",
   ],
   "examples": [
     {"n": "Course Schedule II", "s": "LC 210"},
     {"n": "Find Eventual Safe States", "s": "LC 802"},
     {"n": "Longest Path With Different Adjacent Characters", "s": "LC 2246"},
     {"n": "Reconstruct Itinerary", "s": "LC 332"},
   ],
   "traps": [
     "Two states are not enough. 'Visited' alone cannot tell a cross edge from a back edge — you need the third colour.",
     "The answer is the post-order REVERSED. Forgetting the reverse gives you a valid-looking but wrong order.",
     "Deep graphs overflow Python's recursion limit; Kahn's has no such problem.",
   ]},
 ]},

# -------------------------------------------------------------- shortest path ------
{
 "id": "shortest-path", "group": "graph", "name": "Weighted shortest paths",
 "buys": "exploring every route → O(E log V), by always settling the nearest unfinished node first",
 "lives": "weighted graph — roads with distances, flights with prices, edges with risk",
 "core": "Pick by the weights, and nothing else. All edges equal → BFS. Non-negative weights → Dijkstra, "
         "which is BFS with a priority queue instead of a plain one. Negative edges, or a cap on the number of "
         "edges used → Bellman-Ford. Every pair, with n small → Floyd-Warshall, three nested loops.",
 "recognise": [
   {"cue": "edges carry a <b>cost / distance / time / price</b>, and all are non-negative", "note": "Dijkstra"},
   {"cue": "<b>cheapest</b> / fastest / minimum total, on a weighted graph", "note": "Dijkstra"},
   {"cue": "<b>at most k stops</b> / exactly k edges, or NEGATIVE weights", "note": "Bellman-Ford"},
   {"cue": "<b>all pairs</b>, and n ≤ ~400", "note": "Floyd-Warshall — O(n³) and four lines long"},
   {"cue": "weights are only <b>0 or 1</b>", "note": "0-1 BFS with a deque, O(V+E), no heap needed"},
   {"cue": "'maximise the <b>minimum</b> edge on the path' (signal, capacity)", "note": "modified Dijkstra, or binary search + BFS"},
 ],
 "notwhen": [
   "All edges cost the same → plain BFS; a heap is pure overhead.",
   "You want to connect everything as cheaply as possible, not to travel → that is an MST (Kruskal / Prim), not a shortest path.",
 ],
 "pick": [
   {"if": "non-negative weights, one source", "then": "sp-dijkstra"},
   {"if": "negative edges, or a limit on the number of edges", "then": "sp-bellman"},
   {"if": "every pair of nodes and n is small", "then": "sp-floyd"},
 ],
 "variants": [
  {"id": "sp-dijkstra", "name": "Dijkstra (non-negative weights)",
   "when": "One source, weighted edges, no negatives.",
   "tool": "a min-heap of (distance so far, node); settle the closest unfinished node each time",
   "invariant": "the first time a node is popped, its distance is final — nothing cheaper can appear later",
   "cx": "O(E log V)",
   "code": """import heapq
def dijkstra(n, adj, src):            # adj[u] = [(v, weight), ...]
    dist = [float('inf')] * n
    dist[src] = 0
    h = [(0, src)]
    while h:
        d, u = heapq.heappop(h)
        if d > dist[u]:
            continue                   # a stale copy -- skip it, do not re-expand
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(h, (nd, v))
    return dist""",
   "asks": [
     "network delay time — when does the signal reach everyone",
     "cheapest flights within k stops (needs the k-limit, so usually Bellman-Ford)",
     "path with maximum probability (use −log, or a max-heap)",
     "swim in rising water; path with minimum effort (minimise the MAXIMUM edge)",
     "minimum cost to reach a destination in time",
     "number of ways to arrive at the destination (Dijkstra, counting as you relax)",
     "second minimum time to reach the end",
     "reachable nodes in a subdivided graph",
   ],
   "examples": [
     {"n": "Network Delay Time", "s": "LC 743"},
     {"n": "Path with Maximum Probability", "s": "LC 1514"},
     {"n": "Path With Minimum Effort", "s": "LC 1631"},
     {"n": "Swim in Rising Water", "s": "LC 778"},
     {"n": "Minimum Cost to Reach Destination in Time", "s": "LC 1928"},
     {"n": "Number of Ways to Arrive at Destination", "s": "LC 1976"},
   ],
   "traps": [
     "The <code>if d > dist[u]: continue</code> line is not optional — without it stale heap entries re-expand nodes and the complexity degrades.",
     "Dijkstra is WRONG with negative edges. The 'settled is final' invariant simply does not hold.",
     "For 'minimise the maximum edge', the relaxation becomes <code>max(d, w)</code> rather than <code>d + w</code>.",
     "Python has no decrease-key: push a duplicate and skip stale pops. That is the standard idiom.",
   ]},

  {"id": "sp-bellman", "name": "Bellman-Ford (negatives, or a k-edge cap)",
   "when": "Negative weights, or 'at most k edges / stops'.",
   "tool": "relax EVERY edge, n−1 times — or exactly k+1 times for the k-stop version",
   "invariant": "after round i, every shortest path using at most i edges is correct",
   "cx": "O(V · E)",
   "code": """def cheapest_k_stops(n, flights, src, dst, k):
    dist = [float('inf')] * n
    dist[src] = 0
    for _ in range(k + 1):             # k stops = k+1 edges
        snap = dist[:]                 # use LAST round's values only
        for u, v, w in flights:
            if snap[u] + w < dist[v]:
                dist[v] = snap[u] + w
    return -1 if dist[dst] == float('inf') else dist[dst]""",
   "asks": [
     "cheapest flights within k stops",
     "shortest path with negative edge weights",
     "detect a negative cycle (one extra round still improves something)",
     "currency arbitrage (a negative cycle in log space)",
     "minimum cost with exactly k edges used",
   ],
   "examples": [
     {"n": "Cheapest Flights Within K Stops", "s": "LC 787"},
     {"n": "Network Delay Time", "s": "LC 743 — compare with the Dijkstra version"},
   ],
   "traps": [
     "The snapshot copy is the whole trick for the k-stop version. Relaxing in place lets one round use two edges, which breaks the limit.",
     "k STOPS means k+1 edges. Off by one here is the single most common failure on LC 787.",
     "An n-th round that still improves something proves a negative cycle.",
   ]},

  {"id": "sp-floyd", "name": "Floyd-Warshall (all pairs)",
   "when": "You need distances between EVERY pair and n is small (the n ≤ 100–400 bound is the tell).",
   "tool": "three nested loops, with the intermediate node k on the OUTSIDE",
   "invariant": "after the k-th round, dist[i][j] is optimal using only {0..k} as intermediates",
   "cx": "O(n³) time, O(n²) space",
   "code": """def floyd(n, dist):                 # dist[i][j] pre-filled, inf where no edge
    for k in range(n):               # k MUST be the outer loop
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist""",
   "asks": [
     "find the city with the smallest number of reachable neighbours within a threshold",
     "all-pairs shortest path for a small graph",
     "transitive closure — 'can i reach j' for every pair",
     "course schedule IV — is x a prerequisite of y, answered for many queries",
     "minimum cost to convert one string to another (26 nodes)",
     "evaluate division (ratios between variables)",
   ],
   "examples": [
     {"n": "Find the City With the Smallest Number of Neighbors at a Threshold Distance", "s": "LC 1334"},
     {"n": "Course Schedule IV", "s": "LC 1462"},
     {"n": "Minimum Cost to Convert String I", "s": "LC 2976"},
     {"n": "Evaluate Division", "s": "LC 399"},
   ],
   "traps": [
     "k on the OUTSIDE. Any other loop order gives wrong answers that still look plausible.",
     "n = 400 is 64 million operations — fine in C++, slow in Python. Check the bound before committing.",
     "Initialise dist[i][i] = 0 and everything else to infinity, then lay the edges in.",
   ]},
 ]},

# ------------------------------------------------------------------ union-find -----
{
 "id": "dsu", "group": "graph", "name": "Union-Find (disjoint set union)",
 "buys": "O(V + E) per connectivity query → effectively O(1), and it works as the graph GROWS",
 "lives": "undirected connectivity: friends, networks, merged accounts, equivalent items",
 "core": "Each group keeps one representative. find(x) walks to it, union(a,b) hangs one representative under "
         "the other. The reason it beats DFS is that it answers 'are these two connected' while edges are "
         "STILL ARRIVING — DFS would have to re-run from scratch after every new edge. "
         "This is the one that ambushed you in a real OA.",
 "recognise": [
   {"cue": "<b>merging groups</b> incrementally, 'join these two'", "note": "the definition"},
   {"cue": "<b>are these connected</b>, 'same network', 'same component'", "note": "find(a) == find(b)"},
   {"cue": "<b>number of groups</b> after a stream of operations", "note": "start at n, subtract one per successful union"},
   {"cue": "a <b>cycle in an UNDIRECTED graph</b>, 'the redundant edge'", "note": "an edge whose ends already share a root"},
   {"cue": "<b>cheapest way to connect everything</b>", "note": "Kruskal — sort the edges, union the cheap ones that help"},
   {"cue": "<b>accounts / emails / items to merge</b> transitively", "note": "union by a shared key"},
 ],
 "notwhen": [
   "The graph is DIRECTED and you care about direction → union-find ignores direction entirely.",
   "You must UNDO a union → plain DSU cannot; that needs a rollback variant.",
   "The whole graph is given up front and you only need the components once → a DFS sweep is just as good.",
 ],
 "pick": [
   {"if": "count components, or test connectivity as edges arrive", "then": "dsu-connect"},
   {"if": "find a cycle or a redundant edge in an undirected graph", "then": "dsu-cycle"},
   {"if": "connect everything at minimum total cost", "then": "dsu-kruskal"},
 ],
 "variants": [
  {"id": "dsu-connect", "name": "The structure itself",
   "when": "Connectivity questions, component counts, incremental merging.",
   "tool": "parent array + union by SIZE + path compression",
   "invariant": "every node in a group reaches the same root, and the root knows the group's size",
   "cx": "near O(1) amortised per operation (inverse Ackermann)",
   "code": """class DSU:
    def __init__(self, n):
        self.p = list(range(n))       # everyone is their own root
        self.sz = [1] * n
        self.groups = n
    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]   # path compression, halving as we climb
            x = self.p[x]
        return x
    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb: return False      # already together -- this edge is redundant
        if self.sz[ra] < self.sz[rb]: ra, rb = rb, ra
        self.p[rb] = ra                # SMALL hangs under BIG -> shallow trees
        self.sz[ra] += self.sz[rb]
        self.groups -= 1
        return True""",
   "asks": [
     "number of connected components in an undirected graph",
     "number of provinces / friend circles",
     "number of islands II — land appears one cell at a time",
     "accounts merge; sentence similarity; synonymous expressions",
     "satisfiability of equality equations (union the equals, then check the not-equals)",
     "the earliest moment everyone becomes friends",
     "largest component by size; 'is there a valid path between two nodes'",
     "a capacity rule on merging — reject a union that would exceed the cap",
   ],
   "examples": [
     {"n": "Number of Provinces", "s": "LC 547"},
     {"n": "Number of Islands II", "s": "LC 305"},
     {"n": "Accounts Merge", "s": "LC 721"},
     {"n": "Satisfiability of Equality Equations", "s": "LC 990"},
     {"n": "The Earliest Moment When Everyone Become Friends", "s": "LC 1101"},
     {"n": "Number of Operations to Make Network Connected", "s": "LC 1319"},
   ],
   "traps": [
     "Without union by size AND path compression it degrades to a linked list and times out.",
     "ALWAYS compare roots, never the raw values: <code>find(a) == find(b)</code>.",
     "Have union return a boolean. 'Did this edge actually join anything' is what most problems really ask.",
     "For a capacity rule, test <code>sz[ra] + sz[rb] &gt; CAP</code> BEFORE merging, and leave both sides untouched if it fails.",
   ]},

  {"id": "dsu-cycle", "name": "Cycle / redundancy detection",
   "when": "An undirected graph, and you want the edge that closes a loop.",
   "tool": "union each edge in order; the first union that returns False closes a cycle",
   "invariant": "before adding an edge, its two ends are in the same set exactly when a path already joins them",
   "cx": "O(E · α)",
   "code": """def redundant_connection(edges):
    dsu = DSU(len(edges) + 1)
    for a, b in edges:
        if not dsu.union(a, b):      # both ends already connected -> this edge closes a loop
            return [a, b]
    return []

# a valid TREE on n nodes = exactly n-1 edges AND no cycle at all
def is_tree(n, edges):
    if len(edges) != n - 1: return False
    dsu = DSU(n)
    return all(dsu.union(a, b) for a, b in edges)""",
   "asks": [
     "redundant connection — the edge to remove to restore a tree",
     "graph valid tree",
     "detect a cycle in an undirected graph",
     "number of operations to make the network connected (count spare edges vs components)",
     "remove the maximum number of edges while keeping the graph traversable",
     "checking whether adding an edge would create a loop, as edges stream in",
   ],
   "examples": [
     {"n": "Redundant Connection", "s": "LC 684"},
     {"n": "Graph Valid Tree", "s": "LC 261"},
     {"n": "Number of Operations to Make Network Connected", "s": "LC 1319"},
     {"n": "Remove Max Number of Edges to Keep Graph Fully Traversable", "s": "LC 1579"},
   ],
   "traps": [
     "A tree needs BOTH conditions: exactly n−1 edges and no cycle. Checking only one is a common miss.",
     "Nodes numbered from 1 need a DSU of size n+1, or everything is off by one.",
     "In a DIRECTED graph this does not detect cycles — use the three-colour DFS instead.",
   ]},

  {"id": "dsu-kruskal", "name": "Kruskal — minimum spanning tree",
   "when": "Connect every node as cheaply as possible.",
   "tool": "sort every edge by weight, then union the ones that actually join two groups",
   "invariant": "the cheapest edge crossing any cut is always safe to take (the cut property)",
   "cx": "O(E log E), dominated by the sort",
   "code": """def mst_cost(n, edges):            # edges = [(w, u, v)]
    edges.sort()                     # cheapest first -- this IS the greedy choice
    dsu = DSU(n)
    total, used = 0, 0
    for w, u, v in edges:
        if dsu.union(u, v):          # skip it if both ends are already connected
            total += w
            used += 1
            if used == n - 1: break  # a spanning tree has exactly n-1 edges
    return total if used == n - 1 else -1   # -1: the graph is disconnected""",
   "asks": [
     "minimum cost to connect all points (build the complete graph on Manhattan distances)",
     "connecting cities with minimum cost",
     "optimise water distribution in a village (a virtual node for the wells)",
     "min cost to supply water / to connect all islands",
     "find critical and pseudo-critical edges in an MST",
     "the maximum edge on the MST path — 'minimise the hardest hop'",
   ],
   "examples": [
     {"n": "Min Cost to Connect All Points", "s": "LC 1584"},
     {"n": "Connecting Cities With Minimum Cost", "s": "LC 1135"},
     {"n": "Optimize Water Distribution in a Village", "s": "LC 1168"},
     {"n": "Find Critical and Pseudo-Critical Edges in Minimum Spanning Tree", "s": "LC 1489"},
   ],
   "traps": [
     "MST ≠ shortest path. The MST connects everything cheaply; it does NOT give the shortest route between two particular nodes.",
     "Stop at n−1 edges, and if you never reach n−1 the graph was disconnected — report that rather than returning a partial total.",
     "'A well in a house' becomes an edge from a virtual node 0 — that re-framing is the entire trick in LC 1168.",
   ]},
 ]},
]
