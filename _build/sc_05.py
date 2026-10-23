# -*- coding: utf-8 -*-
"""Scenario questions, batch 5: trie (rest), grids, topological order, shortest paths, union-find, 1-D DP (first).

OA-size stories (around 400 words) with their own Input / Output / Constraints lines. The answer keys
(v, alt, core, why, tell) are the originals.
"""

QUESTIONS = [

{"id": "sc-053", "v": "tr-search", "dom": "monasteries", "diff": "H",
 "title": "The Prior's Letter-Tiles",
 "story": "The abbey of Saint Gall keeps, among its lesser treasures, a tray of glazed letter-tiles made in the "
          "twelfth century for the instruction of novices. The scriptorium lays out this square tray in R rows "
          "and C columns, both at most 12, and the tiles are set in whatever arrangement the novice-master "
          "chose that morning. A list of up to 10^4 candidate words, each of up to 10 letters, is kept by the "
          "prior in a book of his own compiling, and the words are chiefly Latin, chiefly devotional, and "
          "chiefly share their opening syllables, since the Church's vocabulary is built that way.\n\n"
          "A word is 'found' if its letters can be traced through the tray by stepping each time to a tile "
          "directly above, below, left or right of the previous one, never using the same tile twice within one "
          "word. Different words may reuse the same tiles freely; the restriction applies only within a single "
          "word. The prior wants every candidate word that can be found, listed once each however many ways it "
          "can be traced.\n\n"
          "Checking each candidate word separately against the whole tray would take too long, as the prior "
          "discovered when he set two novices to it and lost a week of their copying. He has also noticed "
          "something that he mentions without drawing a conclusion: a great many of his words open with the same "
          "three or four letters, and a novice who has already established that no path spells those letters has "
          "no business starting again from the beginning for the next word in the book.\n\n"
          "The tray's tiles are chipped and one is a replacement in a slightly wrong glaze. The abbey's bees "
          "produce a honey sold at the gate. A novice was disciplined last Lent for arranging the tiles into a "
          "sentence about the cellarer, and the sentence is still remembered.\n\n"
          "Input: line one gives R, C and W. The next R lines give the rows of the tray as strings of C letters. "
          "The next W lines give one candidate word each. Output: the words that can be found, one per line, in "
          "any order.\n\n"
          "Constraints: R and C at most 12; W up to 10^4; each word up to 10 letters, lowercase.",
 "clues": ["stepping each time to a tile directly above, below, left or right of the previous one",
           "never using the same tile twice within one word", "up to 10^4 candidate words",
           "Checking each candidate word separately against the whole tray would take too long",
           "a great many of his words open with the same three or four letters"],
 "decoys": ["The abbey's bees produce a honey sold at the gate",
            "The tray's tiles are chipped and one is a replacement in a slightly wrong glaze",
            "A novice was disciplined last Lent for arranging the tiles into a sentence about the cellarer"],
 "core": "Find which of many dictionary words can be traced through a grid of letters.",
 "gloss": [("scriptorium", "a writing room in a monastery", True), ("prior", "the head of a monastery", True),
           ("tiles", "small flat pieces", True), ("candidate", "a possible choice", True),
           ("traced", "followed along", True), ("devotional", "to do with religious worship", True)],
 "why": {"gr-flood": "That counts connected regions; here the path has to spell particular words.",
         "bk-board": "Searching for one word by backtracking works, but with thousands of words the shared beginnings should be explored once, using the dictionary to cut dead ends."},
 "tell": "Many words traced through a grid: let the dictionary prune the search."},

{"id": "sc-054", "v": "gr-flood", "alt": ["dsu-connect"], "dom": "cartography", "diff": "E",
 "title": "The Hebridean Chart",
 "story": "Miss Elspeth Mackinnon has been surveying the Outer Isles for the Hydrographic Office for eleven "
          "years, in a boat she maintains herself and in weather that would deter most people from leaving the "
          "house. A cartographer of the Hebrides, she sketches a chart of R rows by C columns of cells, each "
          "marked 1 for land or 0 for sea, which is the Office's standard squared form for a preliminary "
          "survey.\n\n"
          "The Office has asked for a count, and the definition it has supplied is exact, because an earlier "
          "survey of the same waters produced a figure that a committee disputed for two years. Two land cells "
          "belong to one island if they touch directly above, below, left or right; diagonal contact does not "
          "join them, since two rocks that touch only at a corner are two rocks and the Office has ruled "
          "accordingly. The cartographer wants to know how many distinct islands the chart shows.\n\n"
          "Tides do not matter, the chart being drawn at mean low water, and the sea around the chart's edge is "
          "treated as sea, so an island running up to the margin is still an island and not something cut off "
          "by the paper. She wants the number alone; the Office will name them later, in consultation with a "
          "committee and the Gaelic Place-Names Commission.\n\n"
          "She works by lamplight and is fond of drawing small sea-serpents in the margin, a habit the Office "
          "has asked her twice to stop. Her boat is called the Puffin and has an engine of uncertain temper. A "
          "colleague in Edinburgh has published a paper on sandbanks that she regards as plagiarism and has not "
          "said so in writing.\n\n"
          "Input: line one gives R and C. The next R lines each give a string of C characters, each 0 or 1. "
          "Output: the number of distinct islands.\n\n"
          "Constraints: R and C up to 1000.",
 "clues": ["touch directly above, below, left or right", "diagonal contact does not join them",
           "how many distinct islands the chart shows"],
 "decoys": ["fond of drawing small sea-serpents in the margin",
            "Her boat is called the Puffin and has an engine of uncertain temper",
            "A colleague in Edinburgh has published a paper on sandbanks"],
 "core": "Count the connected groups of land cells in a grid.",
 "gloss": [("cartographer", "a map maker", True), ("Hebrides", "a group of islands off Scotland", True),
           ("chart", "a map", True), ("distinct", "separate", True),
           ("hydrographic", "to do with surveying seas and rivers", True)],
 "why": {"dsu-connect": "A fair alternative: joining neighbouring cells into groups gives the same count.",
         "gr-bfs": "That finds shortest distances; here only the number of separate groups matters."},
 "tell": "Connected regions on a grid."},

{"id": "sc-055", "v": "gr-bfs", "dom": "island farming", "diff": "M",
 "title": "The Mykonos Terrace",
 "story": "Above the old town on Mykonos, where the tourists do not climb, a goatherd named Stavros Kontarinis "
          "keeps a terrace garden that his family has worked since before the island had a harbour. The terrace "
          "is laid out as R rows by C columns of squares; some squares hold stone walls, marked 1, built from "
          "the rubble cleared off the land over three hundred years, and the rest are open, marked 0.\n\n"
          "Each afternoon one particular goat must be walked from the cistern at the top-left square down to the "
          "pen at the bottom-right square. The goat starts at the top-left square and wishes to reach the "
          "bottom-right square, moving one square at a time to an open square directly above, below, left or "
          "right. It cannot cross a wall, nor move diagonally, the walls being dry-stone and the goat, for all "
          "its ambitions, being a goat.\n\n"
          "The goatherd wants the fewest moves needed, or -1 if no route exists, because the walk is done in the "
          "heat of the day and every extra square is a square of argument. Every move costs him the same effort, "
          "whether it turns a corner or carries straight on.\n\n"
          "The goat is stubborn and the afternoon is hot. A cat on the lower terrace has an understanding with "
          "the goat that neither will acknowledge the other. The island's wind has flattened the fig tree twice "
          "and it has grown back twice. A tour boat passes at four and its loudspeaker can be heard from the "
          "cistern.\n\n"
          "Input: line one gives R and C. The next R lines each give a string of C characters, 0 for open and 1 "
          "for wall. Output: the fewest moves from the top-left square to the bottom-right square, or -1.\n\n"
          "Constraints: R and C up to 1000. Both the top-left and bottom-right squares may be walls, in which "
          "case the answer is -1.",
 "clues": ["moving one square at a time", "directly above, below, left or right", "the fewest moves needed"],
 "decoys": ["The goat is stubborn and the afternoon is hot",
            "A cat on the lower terrace has an understanding with the goat",
            "A tour boat passes at four and its loudspeaker can be heard from the cistern"],
 "core": "The smallest number of steps through a grid of open and blocked squares.",
 "gloss": [("terrace", "a flat step cut into a hillside", True), ("goatherd", "someone who tends goats", True),
           ("squares", "cells of the grid", True), ("cistern", "a tank for storing water", True),
           ("dry-stone", "built of stone without mortar", True)],
 "why": {"gr-flood": "That counts groups; here you need a distance.",
         "dp-grid": "That restricts movement to right and down; here the goat may move in all four directions."},
 "tell": "The fewest steps on a grid where every step costs the same."},

{"id": "sc-056", "v": "gr-multi", "dom": "orchards", "diff": "M",
 "title": "The Tuscan Orchard Fire",
 "story": "The summer has been the driest for forty years, and the hills south of Siena have the colour of "
          "paper. A tinder-dry orchard in Tuscany, planted in the regular pattern the Consorzio insists upon, is "
          "a grid of R rows by C columns of trees, each tree the same distance from its neighbours on all four "
          "sides.\n\n"
          "Before dawn, arsonists light several trees at once, marked 1, moving through the orchard in the dark "
          "and setting fires at points scattered across it; the Carabinieri believe there were at least four of "
          "them and possibly six. Every minute, fire spreads from each burning tree to the four trees directly "
          "above, below, left and right of it, the branches of neighbouring trees having grown together in the "
          "years since the Consorzio last enforced its pruning rules. Diagonal neighbours do not catch, since "
          "the rows are planted wider apart than the trees within a row.\n\n"
          "The fire brigade, arriving at first light, must report how many minutes pass until the last tree in "
          "the orchard is alight, a figure the insurers require and which also settles an argument about whether "
          "the brigade could have arrived in time. All the fires burn from the same moment and spread at the "
          "same rate, so the fronts from different starting trees meet and run together as the minutes pass.\n\n"
          "The orchard's owner is in Rome and has been telephoned. A dog chained at the farmhouse was freed by a "
          "neighbour and is unhurt. The Consorzio's inspector had served a notice about the pruning in April "
          "which the owner had appealed, and the appeal is now of considerable interest to the insurers.\n\n"
          "Input: line one gives R and C. The next R lines each give C digits, 1 for a tree lit at the start and "
          "0 for a tree not yet alight. Output: the number of minutes until every tree is alight.\n\n"
          "Constraints: R and C up to 1000; at least one tree is lit at the start, and every tree is eventually "
          "reached.",
 "clues": ["light several trees at once", "Every minute, fire spreads from each burning tree",
           "until the last tree in the orchard is alight",
           "All the fires burn from the same moment and spread at the same rate"],
 "decoys": ["tinder-dry orchard in Tuscany", "A dog chained at the farmhouse was freed by a neighbour and is unhurt",
            "The orchard's owner is in Rome and has been telephoned"],
 "core": "How long until something spreading from many starting points covers the whole grid?",
 "gloss": [("tinder-dry", "so dry that it ignites easily", True), ("arsonists", "people who set fires deliberately", True),
           ("brigade", "an organised group of workers", True), ("alight", "on fire", True),
           ("Consorzio", "a growers' association", True)],
 "why": {"gr-bfs": "That spreads from one start; running it once per fire would be far too slow.",
         "sp-floyd": "That computes every pair; here only the nearest fire matters."},
 "tell": "Many sources spreading together: start from all of them at once."},

{"id": "sc-057", "v": "to-kahn", "dom": "heavy industry", "diff": "M",
 "title": "The Locomotive Shop",
 "story": "The locomotive shop at Saltley built engines for the Midland Railway and then for its successors, and "
          "it now repairs them, which the works-manager considers a decline and the accountants consider a "
          "business. The works-manager has N jobs on the current overhaul, numbered 0 to N-1, covering "
          "everything from the lifting of the boiler to the lining-out of the cab.\n\n"
          "The jobs cannot be done in any order, and the constraints have been collected from the foremen of the "
          "several trades, who do not always agree but who agree about this. There are M rules of the form 'job "
          "a must be finished before job b may begin', each rule having a physical reason behind it that the "
          "foremen will explain at length if invited. Jobs that are not linked by a rule may be done in any "
          "order, and the shop has enough men to start several jobs at once where the rules allow it.\n\n"
          "Before issuing the shop floor schedule, the works-manager wishes to know merely whether it is "
          "possible to finish every job without breaking any rule. He is not asking for the schedule itself, "
          "which he will draw up with the foremen over a long afternoon; he wants to know whether the rules as "
          "collected are self-consistent, because he suspects that two of the foremen have each insisted on "
          "going first and that somewhere in the list their insistences have closed a ring.\n\n"
          "The foundry is noisy and the foreman is deaf in one ear. A brass plate recording the shop's hundred "
          "thousandth boiler tube is screwed to the wall by the time office. The shop cat is called Midland and "
          "has the freedom of the erecting shop but not the machine shop, a distinction it observes "
          "exactly.\n\n"
          "Input: line one gives N and M. Each of the next M lines gives a and b. Output: YES if every job can "
          "be completed without breaking a rule, NO otherwise.\n\n"
          "Constraints: N up to 10^5, M up to 2*10^5.",
 "clues": ["job a must be finished before job b may begin",
           "whether it is possible to finish every job without breaking any rule"],
 "decoys": ["The foundry is noisy and the foreman is deaf in one ear",
            "A brass plate recording the shop's hundred thousandth boiler tube",
            "The shop cat is called Midland"],
 "core": "Can tasks with 'must come before' rules all be ordered without contradiction?",
 "gloss": [("works-manager", "the person in charge of a factory", True), ("merely", "only", True),
           ("locomotive", "a railway engine", True), ("overhaul", "a thorough repair", True),
           ("erecting shop", "where a locomotive is assembled", True)],
 "why": {"dsu-cycle": "That detects loops in undirected links; these rules have a direction.",
         "sp-dijkstra": "No distances are involved."},
 "tell": "'Must come before' rules: is a valid order possible?"},

{"id": "sc-058", "v": "to-dfs", "alt": ["to-kahn"], "dom": "parliament", "diff": "M",
 "title": "The Standing Orders",
 "story": "The standing orders of the House have been amended piecemeal for three hundred years, and nobody has "
          "ever read all of them in sequence. A parliamentary clerk at Westminster, in the course of preparing a "
          "consolidated edition, has recorded N standing orders, numbered 0 to N-1, together with M dependencies "
          "of the form 'order a must be satisfied before order b can take effect'.\n\n"
          "The dependencies were not designed; they accumulated. An order of 1847 requires a procedure "
          "established in 1912, because the 1912 procedure replaced an earlier one and the cross-reference was "
          "never corrected. Another order requires the Speaker's certificate, and the order governing the "
          "certificate requires, through two further steps, the first order. The Speaker, who suspects a "
          "circular tangle in which some order indirectly depends on itself, asks the clerk to report whether "
          "such a tangle exists.\n\n"
          "If one does, the House cannot proceed with the consolidation and the matter goes to the Procedure "
          "Committee; print LOOP, otherwise print CLEAR. The Speaker does not want the tangle identified, nor a "
          "list of the orders involved, which he says would only produce speeches; he wants the one word.\n\n"
          "The clerk's method is to follow a chain of dependencies as far as it goes, and he has found that the "
          "chains run very deep, in one case through forty-one orders without branching. The House's "
          "snuff-box is kept by the doorkeeper and is still refilled. A division bell in the Press Gallery has "
          "not worked since 1979. The clerk himself has a theory about the 1847 order that he has not yet put in "
          "writing.\n\n"
          "Input: line one gives N and M. Each of the next M lines gives a and b. Output: LOOP or CLEAR.\n\n"
          "Constraints: N up to 10^5; M up to 3*10^5. Chains of dependencies may be extremely long.",
 "clues": ["order a must be satisfied before order b can take effect", "some order indirectly depends on itself",
           "follow a chain of dependencies as far as it goes"],
 "decoys": ["parliamentary clerk at Westminster", "The House's snuff-box is kept by the doorkeeper and is still refilled",
            "A division bell in the Press Gallery has not worked since 1979"],
 "core": "Is there a circular dependency among directed 'must come before' rules?",
 "gloss": [("standing orders", "the formal rules of a parliament", True),
           ("dependencies", "things that rely on others", True),
           ("circular tangle", "a loop that leads back to its start", False),
           ("Speaker", "the chair of a parliament", True), ("consolidated", "gathered into one", True)],
 "why": {"dsu-cycle": "That finds loops in undirected links; here the arrows matter, and a loop must follow them."},
 "tell": "A directed cycle among 'must come before' rules."},

{"id": "sc-059", "v": "sp-dijkstra", "dom": "postal services", "diff": "M",
 "title": "The Prague Courier House",
 "story": "The courier house of Havel a syn has carried parcels out of Prague since the seventeen-nineties, and "
          "it survived the railways by the simple method of carrying what the railways would not. It serves N "
          "towns, numbered 0 to N-1, joined by M two-way roads, each carrying a fee in groschen, the fee being "
          "levied by whichever landowner, town or monastery holds the road.\n\n"
          "The house sits in town 0, and the director, a methodical man named Havel the younger, needs the "
          "cheapest total fee to reach every other town from it, or a note that a town is unreachable. The "
          "figures go into the house's tariff, which is printed and posted up, and a tariff that overstates a "
          "fee loses business while one that understates it loses money.\n\n"
          "A road may be used in either direction at the same fee, and no road has a negative fee, since no "
          "landowner has yet been found who will pay a courier to use his road. The fees vary a great deal, from "
          "a single groschen on a stretch of common land to a sum that the house's drivers describe as "
          "banditry, so a long way round by cheap roads may well cost less than a short way by dear ones, and "
          "the director is not interested in distance or in the number of roads used, only in the total fee.\n\n"
          "The couriers wear green sashes and complain of the cobbles. The house's yard has a mounting block "
          "worn into a hollow. A rival house in Smichov has begun undercutting the tariff on two routes, and "
          "Havel the younger has views about how it manages it.\n\n"
          "Input: line one gives N and M. Each of the next M lines gives u, v and the fee. Output: N numbers, "
          "the cheapest total fee from town 0 to each town in turn, with -1 for a town that cannot be "
          "reached.\n\n"
          "Constraints: N up to 10^5, M up to 3*10^5; fees between 0 and 10^6.",
 "clues": ["two-way roads, each carrying a fee", "cheapest total fee to reach every other town",
           "no road has a negative fee"],
 "decoys": ["The couriers wear green sashes and complain of the cobbles",
            "The house's yard has a mounting block worn into a hollow",
            "A rival house in Smichov has begun undercutting the tariff on two routes"],
 "core": "The cheapest cost from one starting point to every other node in a graph whose costs are never negative.",
 "gloss": [("courier", "a messenger who carries parcels", True), ("groschen", "an old European coin", True),
           ("unreachable", "impossible to get to", True), ("tariff", "a published list of charges", True),
           ("levied", "charged", True)],
 "why": {"gr-bfs": "That works when every step costs the same; these roads have different fees.",
         "dsu-kruskal": "That connects everything cheaply but does not give the cheapest route to each town."},
 "tell": "Weighted roads, no negatives, one source."},

{"id": "sc-060", "v": "sp-bellman", "dom": "airships", "diff": "H",
 "title": "The Zeppelin Syndicate",
 "story": "The Deutsche Luftschiffahrts syndicate operated a scheduled airship service in the years before the "
          "Hindenburg, and its timetable was a thing of baroque complexity, since each airfield's service "
          "depended on which count or municipality had paid for a shed. A zeppelin syndicate offers tickets "
          "between N airfields, numbered 0 to N-1, using M one-way flights, flight i flying from u to v at price "
          "p.\n\n"
          "A passenger leaving airfield 0 wishes to reach airfield N-1 as cheaply as possible while changing "
          "planes at most K times in between, because the syndicate's insurers will not cover a passenger "
          "through more transfers than that, and because each transfer involves a night in a hotel at the "
          "passenger's own expense. The limit is on the number of changes, not on the money: a route with many "
          "changes might well be cheaper and is nonetheless forbidden.\n\n"
          "Some prices are negative. The syndicate pays passengers to travel on certain legs, chiefly the "
          "northbound winter crossings that nobody wants and the inaugural flights it is contractually obliged "
          "to operate, and the accountants have more than once discovered a circuit of airfields that would pay "
          "a sufficiently patient traveller to go round it for ever. Report that least price, or -1 if it cannot "
          "be done within the permitted number of changes.\n\n"
          "The syndicate's founder, an eccentric count, insists on serving champagne on every flight. The "
          "company's shed at Friedrichshafen is the largest building in the state. A steward has written a "
          "memoir which the syndicate's lawyers have read with concern.\n\n"
          "Input: line one gives N, M and K. Each of the next M lines gives u, v and p. Output: the least price "
          "from airfield 0 to airfield N-1 using at most K changes in between, or -1.\n\n"
          "Constraints: N up to 10^3, M up to 10^4, K up to 100; prices between -1000 and 1000.",
 "clues": ["one-way flights", "as cheaply as possible", "changing planes at most K times in between",
           "Some prices are negative"],
 "decoys": ["insists on serving champagne on every flight",
            "The company's shed at Friedrichshafen is the largest building in the state",
            "A steward has written a memoir which the syndicate's lawyers have read with concern"],
 "core": "The cheapest route with a limit on how many hops are allowed.",
 "gloss": [("zeppelin", "a large rigid airship", True), ("syndicate", "a group of companies working together", True),
           ("airfields", "places where aircraft take off and land", True),
           ("inaugural", "the first of its kind", True), ("baroque", "elaborate and ornate", True)],
 "why": {"sp-dijkstra": "The limit on hops breaks the idea that the first time you settle a town its cost is final.",
         "gr-bfs": "That ignores prices."},
 "tell": "Cheapest, but with a cap on the number of hops."},

{"id": "sc-061", "v": "sp-floyd", "alt": ["sp-dijkstra"], "dom": "maritime trade", "diff": "M",
 "title": "The League's Table",
 "story": "The Hanseatic League's postal service was the fastest in northern Europe, and its registrar of routes "
          "at Lubeck kept the figures on which the whole service depended. The service links N depots, N being "
          "at most 100, by two-way sea lanes, each lane having a travel time in days, the times having been "
          "established by long experience and revised only after a formal complaint.\n\n"
          "The registrar wants a complete table giving, for every pair of depots, the shortest travel time "
          "between them, so that any merchant's enquiry can be answered by a single glance at the table. "
          "Merchants come in all day with questions of the form 'how long from Reval to Bruges', and the clerk "
          "who answers them is not the registrar and cannot be trusted with a calculation; he can be trusted "
          "with a table.\n\n"
          "Some depots may be reachable only by passing through others, since not every pair of depots has a "
          "lane of its own and the shortest route between two of them may well run through a third or a fourth. "
          "The registrar is content for the work to be done once, thoroughly, before the table is printed, "
          "however long that takes; what must be quick is the answering of the merchants.\n\n"
          "The League's seal depicts a cog ship. The registrar's office has a floor of Dutch tiles laid in "
          "exchange for a debt. A dispute with the Danish crown over the Sound dues has been running for so long "
          "that both sides have lost the original documents and argue from copies they mistrust.\n\n"
          "Input: line one gives N, M and Q. Each of the next M lines gives u, v and the travel time. Each of "
          "the next Q lines gives two depots. Output: for each enquiry, the shortest travel time, or -1 if there "
          "is no route.\n\n"
          "Constraints: N at most 100; M up to 4000; Q up to 10^5; times between 1 and 10^4.",
 "clues": ["N being at most 100", "for every pair of depots", "the shortest travel time between them"],
 "decoys": ["The League's seal depicts a cog ship",
            "The registrar's office has a floor of Dutch tiles laid in exchange for a debt",
            "A dispute with the Danish crown over the Sound dues"],
 "core": "The shortest distance between every pair of nodes in a small graph.",
 "gloss": [("depots", "places where goods are stored or dispatched", True), ("lanes", "routes", True),
           ("registrar", "an official who keeps records", True), ("cog ship", "a medieval cargo ship", True),
           ("dues", "fees owed", True)],
 "why": {"sp-dijkstra": "A fair alternative, run once from every depot; with only 100 depots the all-pairs table is shorter to write.",
         "dsu-kruskal": "That connects everything cheaply; it does not give shortest distances between pairs."},
 "tell": "All-pairs shortest distances in a small graph."},

{"id": "sc-062", "v": "dsu-connect", "dom": "island communities", "diff": "M",
 "title": "The Faroese Pen-Friends",
 "story": "The village of Gjogv has two hundred inhabitants, a harbour cut into a gorge, and a post office that "
          "is also a shop and in winter also a meeting-place. The postmistress collects pen-friendships as they "
          "are announced: each announcement says that villager a and villager b have begun writing, and the "
          "announcements come in over the counter, one at a time, in the order people happen to mention "
          "them.\n\n"
          "She keeps a record because of the Christmas post. Two villagers are in the same circle if they are "
          "linked by a chain of friendships, directly or through any number of others, and a circle shares a "
          "parcel to save postage, an arrangement the postmistress devised herself and is quietly proud of. A "
          "villager who writes to nobody is a circle of one.\n\n"
          "After each announcement, up to 2*10^5 of them, among up to 2*10^5 villagers across the whole district "
          "the office serves, the postmistress must say how many separate circles now exist, because the figure "
          "goes up on a slate behind the counter and the village has come to treat it as a sort of score. "
          "Friendships are never ended; the postmistress has ruled that a quarrel is not a cancellation, having "
          "watched too many quarrels mend.\n\n"
          "The office's slate was donated by a schoolteacher in 1954. A puffin colony above the village is "
          "counted every June by a man who comes from Denmark expressly for the purpose. The shop sells "
          "liquorice that is popular with the children and, the postmistress suspects, with the "
          "schoolteacher.\n\n"
          "Input: line one gives N and Q. Each of the next Q lines gives a and b. Output: after each "
          "announcement, the number of separate circles.\n\n"
          "Constraints: N and Q up to 2*10^5. An announcement may name two villagers who are already in the same "
          "circle.",
 "clues": ["After each announcement", "how many separate circles now exist", "Friendships are never ended"],
 "decoys": ["The village of Gjogv has two hundred inhabitants",
            "A puffin colony above the village is counted every June",
            "The shop sells liquorice that is popular with the children"],
 "core": "Count the connected groups as links are added one at a time.",
 "gloss": [("postmistress", "a woman in charge of a post office", True), ("announcement", "a public statement", True),
           ("circle", "here, a group of people connected to each other", True), ("gorge", "a narrow rocky valley", True)],
 "why": {"gr-flood": "That counts groups on a grid once the whole picture is known; here links arrive one by one.",
         "to-kahn": "Nothing here has a direction or a required order."},
 "tell": "Groups merging as links arrive, and never splitting."},

{"id": "sc-063", "v": "dsu-cycle", "dom": "communications", "diff": "M",
 "title": "The Odessa Cables",
 "story": "The telegraph board of Odessa was constituted in 1866 to connect the port with the grain country "
          "behind it, and it laid cable with an enthusiasm that outran its bookkeeping. The board lays cables "
          "between N offices, numbered 0 to N-1, one cable at a time, in the given order, each cable joining two "
          "named offices and carrying traffic in both directions.\n\n"
          "An audit has been ordered from Petersburg. A cable is redundant if the two offices it joins are "
          "already connected, directly or through other offices, by cables laid earlier, since a message could "
          "already have passed between them and the copper was therefore bought for nothing. The ministry "
          "suspects that the board has been laying redundant cable deliberately, in the interest of a contractor "
          "who is the brother-in-law of a member.\n\n"
          "The board's engineer, who is not the brother-in-law of anybody and who would like to keep his post, "
          "wishes to know the first cable in the list that is redundant, or to be told that none is. He wants "
          "its position in the order of laying, counting from one, because the ministry's question is when the "
          "practice began and not how much of it there has been.\n\n"
          "A telegraph board in Odessa in those years was a political as much as a technical body. The office at "
          "Nikolaev has a clerk who transmits faster than anyone on the system and is paid no more for it. The "
          "board's chairman keeps a tortoise in his office which the staff feed on lettuce from the market.\n\n"
          "Input: line one gives N and M. Each of the next M lines gives the two offices joined by one cable, in "
          "the order laid. Output: the position of the first redundant cable, counting from 1, or 0 if there is "
          "none.\n\n"
          "Constraints: N up to 10^5; cables up to 2*10^5. No cable joins an office to itself.",
 "clues": ["one cable at a time", "already connected, directly or through other offices",
           "the first cable in the list that is redundant"],
 "decoys": ["A telegraph board in Odessa in those years was a political as much as a technical body",
            "The board's chairman keeps a tortoise in his office",
            "The office at Nikolaev has a clerk who transmits faster than anyone on the system"],
 "core": "Find the first link that closes a loop in an undirected graph.",
 "gloss": [("telegraph", "an old system of sending messages by wire", True), ("redundant", "unnecessary", True),
           ("engineer", "someone who designs and builds things", True), ("audit", "an official examination", True)],
 "why": {"to-dfs": "That finds loops that follow arrows; these cables have no direction.",
         "dsu-kruskal": "That chooses the cheapest connecting cables; here no costs exist."},
 "tell": "The first edge whose two ends are already connected."},

{"id": "sc-064", "v": "dsu-kruskal", "dom": "water engineering", "diff": "M",
 "title": "The Seville Water Board",
 "story": "Seville has watered itself from the Guadalquivir and from a system of reservoirs in the hills since "
          "the Almohads, and the modern water board inherited both the system and the habit of arguing about it. "
          "The board must connect N reservoirs, numbered 0 to N-1, so that water can flow between any two of "
          "them, directly or through others, in order that a shortage in one part of the system can be met from "
          "another.\n\n"
          "Only certain channels may be dug, the terrain and the archaeology between them ruling out most "
          "possibilities, and the engineers have surveyed those that remain: channel i joins a and b at a cost c "
          "in escudos, the cost depending on the rock, the gradient and whether the route passes under anything "
          "the Ministry of Culture cares about.\n\n"
          "The board wants the lowest total cost of channels that connects every reservoir, or -1 if the "
          "permitted channels cannot connect them all. It does not matter how long the journey between two "
          "particular reservoirs is, nor how many channels the water passes through on the way; the board is not "
          "pumping to a schedule, only guaranteeing that the system is one system. It has also been pointed out, "
          "in a memorandum from the chief engineer, that digging a channel between two reservoirs that are "
          "already joined through others is money poured into a hole.\n\n"
          "The water board of Seville occupies a building with a courtyard and a very old orange tree. A "
          "Roman aqueduct crosses one of the proposed routes and has already caused a two-year delay. The "
          "board's president has a nephew in the contracting business and has been careful to say so.\n\n"
          "Input: line one gives N and M. Each of the next M lines gives a, b and c. Output: the lowest total "
          "cost that connects every reservoir, or -1.\n\n"
          "Constraints: N up to 10^5, M up to 3*10^5; costs up to 10^6.",
 "clues": ["connects every reservoir", "the lowest total cost",
           "does not matter how long the journey between two particular reservoirs is",
           "digging a channel between two reservoirs that are already joined through others is money poured into a hole"],
 "decoys": ["The water board of Seville occupies a building with a courtyard and a very old orange tree",
            "A Roman aqueduct crosses one of the proposed routes",
            "The board's president has a nephew in the contracting business"],
 "core": "Connect all the nodes with the cheapest total cost.",
 "gloss": [("reservoirs", "places where water is stored", True), ("channels", "artificial waterways", True),
           ("escudos", "old Iberian currency", True), ("permitted", "allowed", True),
           ("gradient", "a slope", True)],
 "why": {"sp-dijkstra": "That finds the cheapest route between two places; here you want the cheapest total to join all of them.",
         "dsu-connect": "That counts groups; here costs decide which links to choose."},
 "tell": "Connect everything at minimum total cost."},

{"id": "sc-065", "v": "dp-linear", "dom": "fishing", "diff": "M",
 "title": "The Marseille Quay",
 "story": "The fish market on the Quai des Belges has been held every morning for twenty-six centuries, which "
          "the stallholders mention to tourists and to the municipality with equal frequency. The harbour market "
          "has N stalls in a row along the quay, and stall i would earn the fishmonger p[i] francs for the day, "
          "the figure depending on the stall's position, the shade, and its distance from the man with the "
          "accordion.\n\n"
          "A municipal rule forbids trading at two neighbouring stalls on the same day, since the crowd would "
          "block the quay and the quay is also a road. The rule was introduced after a fire engine failed to get "
          "through in 1962 and is enforced by an inspector who takes it personally.\n\n"
          "The fishmonger, who has the concession for the whole row, may choose any stalls obeying the rule and "
          "wishes to know the greatest total earning he can collect. He may leave as many stalls empty as he "
          "likes, and he may take none at all, though that would be a strange day's work. He has attempted simply "
          "taking the best-earning stall and then the best of what remained, and found that it cost him money on "
          "a row of three stalls earning four, five and four francs, where the two ends together beat the "
          "middle.\n\n"
          "The mistral wind has been howling all morning and the gulls are screaming over the nets. A "
          "fishwife at the eastern end has sold the same three species for forty years and refuses to stock "
          "anything else. The inspector's bicycle was stolen in June and recovered, repainted, in August.\n\n"
          "Input: line one gives N. Line two gives the N stall earnings in order along the quay. Output: the "
          "greatest total that can be earned with no two neighbouring stalls taken.\n\n"
          "Constraints: N up to 10^5; each earning between 0 and 10^9. The answer may need a 64-bit integer.",
 "clues": ["forbids trading at two neighbouring stalls", "the greatest total earning",
           "taking the best-earning stall and then the best of what remained"],
 "decoys": ["The mistral wind has been howling all morning and the gulls are screaming over the nets",
            "A fishwife at the eastern end has sold the same three species for forty years",
            "The inspector's bicycle was stolen in June"],
 "core": "Choose items from a row with no two adjacent, to make the total as large as possible.",
 "gloss": [("fishmonger", "a seller of fish", True), ("quay", "a landing place for boats", True),
           ("municipal", "belonging to a town", True), ("francs", "French currency", True),
           ("concession", "the right to trade in a place", True)],
 "why": {"gr-local": "Taking the biggest available stall first can block two better neighbours; a locally best choice is not safe here.",
         "dp-kadane": "That wants one unbroken stretch; here the chosen stalls are scattered."},
 "tell": "No two adjacent, maximize the total."},
]
