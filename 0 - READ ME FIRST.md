# Placement prep — what's in here

Built 2026-09-07. Target: **10-12 LPA minimum.**

---

## The HTML files are the main thing — just open them

Double-click any file below. Every tool links to the others at the bottom of its page, and when you're
running them off disk those links point at the **sibling files in this folder**, so you can hop between
them without touching a browser tab. (The same pages detect when they're loaded online and switch the
links back automatically — you don't have to think about it.)

One thing to know: progress ticked in a local file is saved **in that browser only**. If you open the
tracker in Brave and then in Chrome, they won't share ticks. The live links below are the same pages with
cloud-synced progress, if you ever want that — but the local files are self-contained and work offline.

| Open this file | What it is | Cloud-synced version |
|---|---|---|
| `1 - Twenty Weeks to AC (tracker).html` | the plan and progress tracker | [link](https://claude.ai/code/artifact/32b165b3-0cee-4121-9470-b0e8d6d17c16) |
| `2 - Stdin Trainer (drill).html` | **start here** — reading input | [link](https://claude.ai/code/artifact/00d12bf6-5548-4e56-b449-d0f33193a495) |
| `3 - Stdin Survival Kit (manual).html` | the written stdin manual | [link](https://claude.ai/code/artifact/49b64e1a-a87a-4924-b42d-2a7a614ab41a) |
| `5 - SQL Lab (practice).html` | 50-topic DBMS/SQL/PostgreSQL/MySQL study guide with tests + 24 SQLite exercises | [link](https://claude.ai/code/artifact/0f564ee0-0ae9-4f76-b0db-9cbaf04a5664) |
| `6 - CS Core Drill (OS DBMS CN OOP C).html` | 68 MCQs + exam mode | [link](https://claude.ai/code/artifact/3a19c5c3-5b45-4744-a980-20f138d77859) |
| `7 - Aptitude Sprint (formulas + practice).html` | formula sheets + timed practice | [link](https://claude.ai/code/artifact/1176c004-05c1-4ebd-bd08-041957dd07f6) |
| `8 - Pattern Radar (name the pattern).html` | which DSA pattern is this? | [link](https://claude.ai/code/artifact/9c7876de-143f-4f4d-bead-a8204d0f63ad) |
| `9 - Decoder (read the story, name the pattern).html` | 140 story-wrapped statements — strip the story, name the pattern, learn *why not* the wrong one | [link](https://claude.ai/code/artifact/ca3214a6-ec8f-4b10-b757-9c025a98ba47) |
| `10 - Mock OA (timed exam).html` | **the real thing** — full OA problems, hard 20-min-per-question lock, write your plan, then bring it here | [link](https://claude.ai/code/artifact/ea757a13-0226-4bad-9065-96ca4927af42) |

`4 - Stdin Survival Kit.pdf` — 13 pages, print it or keep it open during a real assessment.

---

## Where to start, in order

1. **Stdin Trainer** — 20 minutes. 13 input shapes, pick the line that parses each one. This is the gap
   that cost you the Infosys attempt: your 97 LeetCode solves gave you a pre-parsed function signature,
   and roughly half your target companies hand you a blank editor instead.
2. **The tracker, Track 0** — the week-1 bench setup. Format, not algorithms.
3. **Track G, CS fundamentals block** — highest points-per-hour thing on the page. It's the gate at
   Walmart, Oracle, Cisco, Qualcomm, Nutanix, ServiceNow and SAP, and every one of those clears 10 LPA.
4. **Track D, Phase 1** — the DSA patterns. Binary search on the answer is the single highest-return block.
5. **Track C** — one LeetCode contest every Sunday, starting week 2. Not week 16.

---

## The three things worth remembering

**Your salary floor changes the strategy.** TCS Ninja ~3.5-3.9 LPA, Infosys SE ~3.6, Wipro Elite ~3.5,
Cognizant GenC ~4, Accenture ~4.5-6.5 — all below your number. Their heavy aptitude batteries are
therefore not your problem. The nine "GO NOW" companies in the tracker's table are: Walmart, Oracle,
ServiceNow, Salesforce, Amazon, Cisco, SAP, Nutanix, Qualcomm. They pay 12-24 LPA, their coding rounds
are easy-to-medium, and most gate on a CS-fundamentals MCQ section instead of hard algorithms.

**Partial credit changes how you play the 90 minutes.** Nearly every platform scores per test case.
Walmart's real bar was "one complete and one partial". So: minutes 0-25 fully solve the easier problem,
25-35 ship the obvious brute force on the second to bank the small cases, 35-80 optimise on top of it.
Never leave one blank. Never delete a working brute force to try an optimisation — copy it first.

**Output format is not a detail.** The grader compares character by character. `print("Output:", ans)`
scores 0 of 7 test cases with perfectly correct logic. Print the answer and nothing else.

---

## SQL Lab — how it works

**Roadmap and quiz (2026-10-23).** The SQL Lab home opens with a roadmap: 11 stages in a sensible order, a tick box per
topic (ticks also happen automatically when you finish a topic's test), a progress bar, time left, and a "next up"
button. A "mixed quiz" button runs random questions across everything: 404 questions in all, including 140 whose
answers were computed by code (candidate keys, closures, normal forms, super-key counts, and "what does this query
return" on the sample database). Choose areas, length, timer, exam mode, or only the questions you missed before.
Results show a breakdown by area and a review of every miss. Missed questions and scores are remembered.

**Write it (added 2026-10-23): the assessment-style practice.** 95 tasks where YOU write the SQL. 62 query tasks on two
databases (the company one and a shop one you have not seen) are graded by running your query and comparing the result,
including UPDATE / DELETE / INSERT tasks graded by the table that results. 15 "create tables" tasks are graded by loading
your schema and trying good and bad rows (duplicate rejected? cascade works? default applied?). 18 paper-only tasks
(triggers, procedures, normalization, theory, indexing choices) have no run button: write, reveal the model answer, tick the
rubric. "Paper mode" can also be switched on for any query or create-table task. A clock runs against a target time.
Build checks that every reference solution and every create-table check agrees before it ships.

**Study guide (added 2026-10-23).** Open SQL Lab and press the roadmap button: 50 topics in eight groups, each ending
with a short test whose best score is remembered. A: DBMS basics, ER model, ER-to-tables. B: keys (super, candidate,
primary, foreign...), relational algebra, functional dependencies, 1NF to BCNF, 4NF, 5NF, 6NF. C: ACID, schedules,
locking, recovery, indexing, query optimisation, OLAP/NoSQL/CAP. D: data types, CREATE TABLE with every constraint,
foreign-key actions, six full scenario-to-DDL designs (library, shop, hospital, bank, college, hotel), design practice.
E: SELECT through window functions, DML, views, indexes. F: 24 classic interview queries. G: transactions, triggers (two
topics), procedures, cursors, permissions, partitioning. H: PostgreSQL essentials, MySQL essentials, a full
PostgreSQL-vs-MySQL table, JSON, metadata queries, operations, and 60 rapid-fire interview answers.
Green "run" buttons execute the example on a throwaway copy of the sample database (SQLite). PostgreSQL and MySQL
specific blocks are labelled and are read-only.
It is generated: content lives in `_build/mat_0*.py`; rebuild with one command, `python _build/build_sqlstudy.py`
(it also executes every runnable example and refuses to build if one fails).

**Practice below it.**

A real SQLite database runs inside the page. Five tables, seeded to punish sloppy queries: two pairs of
tied salaries, one employee with no department, one department with no employees, and a manager who earns
less than the person reporting to him. You type SQL, hit run, and get graded on the **actual result set** —
so there's no way to be "nearly right".

24 exercises across six tiers: filtering → aggregates → joins → subqueries → window functions → the
assessment classics (Nth highest salary, duplicate detection, consecutive days). There's also a free-query
mode for poking at the data. All 24 reference solutions were executed and verified before shipping.

Dialect differences live inside the exercises that need them, not in a lecture. The one that actually
matters: **Postgres rejects a `GROUP BY` query where MySQL quietly allows it** — Postgres wants every
non-aggregated column listed. Write it Postgres-strict and it's correct on both.

## CS Core Drill — how it works

68 MCQs across five tracks: **OS** (15), **Computer Networks** (15), **DBMS theory** (14), **OOP** (12),
**C/C++ output prediction** (12). Every question explains the right answer *and* why the specific wrong
option you picked is tempting — that second part is where the learning is.

**Exam mode is the feature to use.** 22 questions, 35 minutes, no feedback until you submit — the exact
shape of Walmart's technical section. You get a per-topic breakdown at the end plus a review of everything
you missed. Around 70% is the usual shortlisting bar.

Everything you get wrong lands in a redo pile that persists, so "drill my mistakes" always has something in it.

Two deliberate decisions in the C track:
- **Only well-defined behaviour**, with assumptions stated (64-bit, `sizeof(int)`=4, `sizeof(void*)`=8).
- **Two questions where the correct answer IS "undefined behaviour"** — because a lot of the C output
  questions circulating online (`i = i++ + ++i` and friends) have *no* defined answer, and different
  compilers genuinely print different numbers. Recognising those is worth more than memorising one
  compiler's accident.
- Nothing to install: links to programiz, onlineGDB and godbolt are on the home screen so you can paste
  any snippet and run it yourself.

## Aptitude Sprint — how it works

**Formulas and tricks first, practice underneath.** 27 sub-topics, each with its own sheet: the formulas
in one block, then the shortcuts that actually save time. Click any sub-topic chip to read the sheet, then
hit "practise these N" at the bottom of it. There's also an **all formulas & tricks** button that puts
every sheet on one page — that's your pre-exam skim.

**444 questions (2026-10-23):** 13-26 per sub-topic, each one tied to a formula on its sheet. The 387 new ones are
generated by `_build/apt_gen_*.py` with the answers computed, then merged by `python _build/build_aptitude.py`
(safe to rerun; the original 57 keep their numbers so saved progress still lines up).

Aptitude is a *speed* test, so every question is timed against a target (45–90s, averaging ~61s, which is
about what TCS gives you). Getting it right in 110 seconds is tracked as a failure, and there's a
**"speed up N slow"** button for questions you got right but too slowly.

**Negative marking toggle.** Turn it on and wrong answers cost 0.25 while blanks cost nothing — the DE
Shaw and Arcesium format. It changes the correct behaviour: guess only once you've eliminated two options,
otherwise skip. Exam mode is 20 questions in 25 minutes with a skip button.

All the arithmetic was independently recomputed before shipping — every percentage chain, LCM, combination
and clock angle verified in Python, not just eyeballed.

## Pattern Radar — now two halves: LEARN, then DRILL

**LEARN** is the map. The premise is that the countable things are countable: a handful of data
structures, a handful of patterns on them, and inside each pattern a **closed set of variants**. A
variant fixes the template, and the template fixes the family of questions that can be built on it.
**21 patterns, 78 variants, 515 question families**, across all six groups:

| Group | Patterns |
|---|---|
| Arrays & strings | two pointers, sliding window, prefix sum, binary search, hashing, monotonic stack, heap, sorting & intervals, bits |
| Linked lists | linked list surgery |
| Trees | tree DFS, tree BFS, trie |
| Graphs & grids | grid traversal, topological sort, weighted shortest paths, union-find |
| Dynamic programming | 1-D DP, 2-D DP |
| Search & greedy | backtracking, greedy |

Each pattern page gives you the tells, **"but NOT this pattern when"**, a one-line rule for picking
the variant, and then each variant with: when / tool / invariant / complexity, a Python template,
the numbered question families, problems to go solve, and the traps. Every variant has a "got it"
tick that persists.

**Every one of the 78 variants has a live trace** (marked `▶ trace`). Press play, or step with the arrow
keys, and you watch the pointers move, the window shade, the stack pop and the hashmap fill — while
the matching line of code lights up and a sentence explains why that step had to happen.

**Type your own input.** Every trace has input boxes above it — the array, the string, k, the target,
the intervals. Change them, hit *run it*, and the whole animation re-runs on your numbers. The
generators execute in the browser, so nothing is pre-baked. Bad input is explained rather than
swallowed ("k must be ≤ the array length"), and the ones that need order (binary search, two
pointers) sort your input and tell you they did.

That is trustworthy because of `viz_test.js`: it fuzzes every generator against a **brute-force
implementation of the same problem** — about 300 random inputs each, **22,000 cases and 148,000
frames** — and also checks every frame points at a real code line and a real cell on its stage.
`build_radar.py` runs it through Node and **refuses to build** if anything disagrees. It has caught
nine real bugs so far, including an inverted highlight range, a wrong interval-merge definition,
an LCA that is ambiguous when tree values repeat, and a queue-reconstruction input that no queue
can satisfy.

There are **four stages**, picked to suit what each variant actually is:

| Stage | Used by | What you watch |
|---|---|---|
| row (51) | arrays, strings, linked lists, timelines | pointers moving, windows shading, stacks popping |
| grid (16) | grid traversal, DP tables, matrices, n-queens | a board or table filling in, cell by cell |
| tree (6) | every tree pattern and the trie | values flowing up or context flowing down, edges drawn |
| graph (5) | Dijkstra, Bellman-Ford, Kruskal, three-colour DFS, DSU cycles | nodes settling and edges lighting up as they are relaxed, accepted or rejected |

**818 verified problem links across 8 platforms** — LeetCode, GeeksforGeeks, HackerRank, HackerEarth,
CodeChef, InterviewBit and Codeforces — with a platform filter per pattern, so you can decide to
spend a day on HackerEarth instead of LeetCode. Nothing here is a guessed URL: LeetCode links are
resolved against LeetCode's own problem index (which also corrected 13 of my titles and flags the
premium ones), Codeforces problems are pulled from the Codeforces API by tag and ranked by how many
people solved them, and every other link is fetched and dropped if it does not answer 200. Where a
platform has no topic page for a pattern, that platform's button is simply absent — a live link to
the wrong topic is worse than no link.

> Pattern Radar is **generated**, from the files in `_build/`. Content lives in `pattern_library.py` plus
> `lib_list_tree.py`, `lib_graph.py` and `lib_dp_search.py`; links in `pattern_links.py`; traces in
> `viz_engine.js` through `viz_engine_f.js` (the first one also holds the shared helpers and input parsers).
> Then, from the materials folder, run `python _build/verify_links.py` followed by `python _build/build_radar.py`
> (which needs Node on PATH to fuzz-test the traces). Do not hand-edit the HTML — the next build overwrites
> it from the pristine stash `_build/.radar_src.html`.

### DRILL — the original half

Track D in the tracker links 235 problems to solve, but nothing was training the skill *underneath* all
of them: read a statement, glance at the constraints, and name the pattern in under a minute. That's what
an assessment actually tests in its first two minutes, and it was the last real gap.

34 problem statements, each with its **real constraint bounds**, and you pick the approach from four
plausible candidates. Every explanation names **the tell** — the phrase or bound that gave it away — and
every wrong option explains why it's tempting.

The constraint ladder and a 22-line "tells" table (phrase on the left, pattern on the right) sit on the
first screen. That table is the single highest-leverage page in this whole folder: *"contiguous + longest"*
→ sliding window. *"contiguous + sum equals K + negatives"* → prefix sum + hashmap. *"minimum X such that"*
→ binary search on the answer. *"n ≤ 12"* → bitmask DP.

Some questions exist purely to teach constraint-reading — the LIS one gives you `n ≤ 2500` and `n ≤ 10⁵`
and asks which algorithm each demands. Same problem, two different required solutions, decided only by
the bound.

## Decoder — the deeper version of the same skill

Pattern Radar asks *which pattern*. The Decoder trains the thing you said actually beats you: **the long,
padded, contextual statement** you barely finish reading, and the second-guessing that follows —
*"why this, why should I ignore that"* — that ate 30 minutes of your last OA before you realised it was DSU.

140 statements you will not find on any judge — I wrote them in the exact wordy OA voice (cities, servers,
kingdoms, printers) hiding a bare algorithmic core — across **7 optimisation families**: union-find,
binary search on the answer, greedy, DP, sliding window, heaps, and graph BFS/Dijkstra. 20 per family.

The point is the reveal. Every answer shows **the clue** (the exact phrase that gives it away), the
statement **stripped to its core**, the complexity, and — the part built for you — **"why NOT the others"**:
for each tempting wrong option, a line on why the clue does *not* point there. That is the doubt-killer.

Under each family sits a grind-list of **real problems, across judges** — 20 LeetCode (clean statements) and
8 Codeforces (long narrative statements, closest to a real OA) per pattern, plus topic-hub links to
**HackerEarth and HackerRank** (the platforms most company OAs actually run on) and GeeksforGeeks. Every one
of those ~250 links was verified live. So once you can decode the story, you go solve the clean versions.

DSU, the one that surprised you, is family one and also lives in the tracker's Phase 3 (block b6). You have
not been ambushed by a missing topic — you just had not reached it yet, and you had never drilled *reading*
the wrapper. Now you can.

## Mock OA - read the story, find the clues

This is now a **scenario-decoding** trainer, not a coding one. The idea: the approach behind a question never
changes, only the wording does, and what beats you is an unfamiliar word hiding a pattern you already know.

**156 scenarios, every one OA-size** (301 to 426 words, average 355), each with the story, an Input / Output
paragraph and a Constraints line like a real statement. There are no short ones, on purpose: a real assessment
that is short is a direct question, and only the long contextual ones need decoding. Two per variant across all
78 variants, in 150+ domains (falconry, tide mills, lock museums, ropewalks, seed vaults, bell foundries, salt
pans...), written in deliberately hard vocabulary with decoy sentences that change nothing.

There are **no options to click and nothing to pick from a list**. One blank box: you **type what the story is
really asking for, which words told you, and what you would do**, in your own words, the way you would say it
out loud. No technical name is needed - a correct idea in plain English scores the same as the jargon.

### How it is marked
The **coach** (the NVIDIA-API model) reads what you typed against the question's own answer key and returns one
of four verdicts, plus one indirect nudge:

| verdict | means | score |
|---|---|---|
| that is it | what you describe would produce what the story asks for | 1 |
| right neighbourhood | right family, or the right idea with one material piece wrong | 0.5 |
| not this one | would not produce what is asked | 0 |
| not enough to judge | a bare structure name, or a question instead of an answer | 0 |

Then you can **write back to the coach** and ask for another nudge; each exchange escalates the hint level. The
answer is only shown when you press "show me the answer" yourself, so you can rewrite and check again as often
as you like.

The coach never tells you the answer, and that is enforced in two places. The prompt
(`_build/llm_prompts.py`) forbids it from naming the approach, saying what a clue means, describing a step of a
solution, quoting the story, or supplying the deciding word (longest, shortest, exactly, unbroken...) unless you
used it first. Then `_build/llm_coach.py` **reads the reply back and checks it**; if it leaks, the model is asked
again with a warning, and if it leaks twice the reply is thrown away and a nudge written by the tool is sent
instead. The verdict always survives, because one word cannot give anything away.

If the key is missing, the hub is not running, or no model answers, the page says so and you mark yourself on the
reveal with the **right / pattern only / wrong** buttons. Those buttons are always there, so you can overrule the
coach when you think it has misjudged you.

### The reveal
The story again with the clue phrases highlighted in green and the decoys struck through, what you wrote, the
story stripped to a plain one-line core, what the clues add up to, every tempting neighbour and why it is not
the answer, a glossary of the hard words, and a link that opens the exact variant (and its animated trace) in
Pattern Radar. Words from questions you miss are remembered and listed on the setup screen.

Modes: *practice* (reveal after each) or *exam* (hard time lock, reveal at the end). Focus: unseen first, my weak
variants, or random.

Add scenarios in `_build/sc_*.py`, then `python _build/build_mock.py`. `sc_check.py` refuses to build if a clue
phrase is not verbatim in its story, if a story contains a technique word that gives the pattern away, or if a
story is under 300 words.

(The old 150-problem mock is gone; those problems live on in OA Solve, in `data/oa_bank.json`.)

### The coach's wiring
`python _build/llm_check.py` checks the key, the API and the model in three steps. `_build/llm_bench.py` scores
candidate models. The default is `z-ai/glm-5.3-flash`; `_build/llm_config.py` holds a **fallback chain**
(gpt-oss-20b, glm-5.3, deepseek-v4.1-flash) because providers do go down, and a model that just failed is skipped
for 90 seconds so one dead provider does not slow every later call. Expect 15 to 90 seconds a reply, longer when
a leaky first reply has to be asked again. The API key is read from `.env` on the server and never reaches the
page.

---

## Everything is built

Nothing outstanding. Eight tools plus the tracker: input parsing, pattern recognition, statement decoding, the
timed Mock OA, SQL, CS fundamentals, aptitude. What's left is reps — Track 0 first, then one contest every Sunday,
and a Mock OA whenever you want to feel the clock.

---

## Folder layout

`start.bat` + `app.py` = the hub. Numbered files = the tools. `data/` = all your progress and question banks.
`_build/` = the generators (you only touch it to add content). `.env` = your API key. `my notes/` = your own files.

## Your own files

Your own notes are in `my notes/`: the four pattern pictures, `Sliding Window.docx`, `Resume n mail writing.docx`,
and the solved HackerEarth OA.


---

## SQL practice on real platforms
- HackerRank SQL: https://www.hackerrank.com/domains/sql (closest to a real OA; pick MySQL in the language box)
- LeetCode Database: https://leetcode.com/problemset/database/ (blocks scripts, opens fine in a browser)
- DataLemur: https://datalemur.com/
- StrataScratch: https://www.stratascratch.com/
- SQLZoo: https://sqlzoo.net/

SQL Lab (tool 5) runs SQLite in the page, but accepts the common MySQL functions (CONCAT, IFNULL, YEAR, MONTH, DAY,
DATEDIFF, DATE_FORMAT, CURDATE, NOW, LEFT, RIGHT, CHAR_LENGTH, LIMIT). Not available there: INTERVAL arithmetic and
GROUP_CONCAT ... SEPARATOR. Every generic query in the guide now has its MySQL version under it where they differ.
