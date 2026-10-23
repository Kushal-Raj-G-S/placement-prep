# -*- coding: utf-8 -*-
"""Scenario questions, batch 1: two pointers, sliding window, prefix sum (first half).

Every story here is OA-size (around 400 words) with its own Input / Output / Constraints lines, because a
real assessment almost never gives you a short contextual question: if it is short it is direct, and if it
has a context it is long. The answer keys (v, alt, core, why, tell) are the originals.

Fields: v = answer variant, alt = other variants that are also valid, dom = domain of the story,
clues / decoys = EXACT substrings of the story (the page highlights them),
gloss = (word, plain meaning, safe_to_define). safe=False means defining the word would give the clue away.
"""

QUESTIONS = [

{"id": "sc-001", "v": "tp-ends", "alt": ["hs-index"], "dom": "maritime", "diff": "E",
 "title": "The Gantry Manifest",
 "story": "Port Merrow has worked cargo since the reign of the second George, and its stevedores are a proud, "
          "unhurried body of men who regard the harbourmaster's paperwork as an affliction sent to try them. "
          "The present harbourmaster, a thin and anxious man named Crispin Dallimore, inherited the post from an "
          "uncle who had held it for thirty-one years and who left behind a filing system that nobody has ever "
          "fully understood. Each morning Dallimore receives the day's lading in a manifest that lists every "
          "crate waiting on the quay together with its mass in kilograms, and by a custom older than anyone can "
          "remember the manifest is sorted from the lightest crate to the heaviest.\n\n"
          "The quay is served by a single travelling gantry, and the gantry's spreader, which is the steel beam "
          "that grips a load, can be clamped to exactly two crates at a time. Harbour regulations, drawn up after "
          "an accident in 1911 that nobody discusses, stipulate that their combined mass must equal the "
          "spreader's rated load L, no more and no less, so that the beam is neither strained nor left slack. "
          "Before booking the berth, the harbourmaster merely wishes to ascertain whether any such couple exists "
          "in the manifest. He does not need to know which two crates they are, nor how many such couples the "
          "manifest contains, nor in what order they might be lifted; the berth is booked or it is not.\n\n"
          "The gantry driver, a cheerful woman named Bettany, keeps a terrier that rides in the cab with her and "
          "barks at seagulls. The quay's weighbridge was condemned two years ago and has not been replaced. There "
          "is a persistent rumour that the Merrow Company intends to sell the whole wharf to a developer of "
          "flats, and the stevedores discuss it endlessly over their tea without ever reaching a conclusion.\n\n"
          "Input: the first line gives N, the number of crates, and L, the spreader's rated load. The second line "
          "gives the N masses. Output: the single word YES if two crates can be clamped together to make exactly "
          "L, and NO otherwise.\n\n"
          "Constraints: N up to 2*10^5, masses up to 10^9, L up to 2*10^9; the manifest already arrives in "
          "non-decreasing order, and Dallimore is forbidden by the Company's auditors from copying it onto fresh "
          "paper or keeping working notes longer than a few lines.",
 "clues": ["sorted from the lightest crate to the heaviest", "exactly two crates at a time",
           "combined mass must equal the spreader's rated load L", "whether any such couple exists",
           "already arrives in non-decreasing order"],
 "decoys": ["Before booking the berth", "keeps a terrier that rides in the cab with her and barks at seagulls",
            "The quay's weighbridge was condemned two years ago"],
 "core": "A list that is already in order, and one yes-or-no question: do two of its items add up to a target?",
 "gloss": [("stevedores", "dock workers who load and unload ships", True), ("lading", "the cargo being carried", True),
           ("manifest", "a written list of cargo", True), ("gantry", "a tall frame with a lifting arm", True),
           ("stipulate", "to require as a condition", True), ("ascertain", "to find out", True),
           ("couple", "a pair", True)],
 "why": {"hs-index": "A lookup table also finds a pair, but the list is handed over already sorted and only existence is asked, so no table is needed.",
         "bs-exact": "Searching for each crate's partner repeats work that a single inward sweep avoids."},
 "tell": "Sorted input plus 'is there a pair that hits a target?' points to two markers closing in from the ends."},

{"id": "sc-002", "v": "tp-write", "dom": "apothecary", "diff": "E",
 "title": "The Dispensary Shelf",
 "story": "The dispensary of Saint Aldric's is a narrow room behind the infirmary, lit by one high window, and it "
          "has been run for forty years by an apothecary named Mother Ambrosine, who is said to have cured a "
          "bishop of the gout and who certainly cured the abbot of an ailment he has never named. Her apprentice "
          "this season is a boy called Tobias, willing enough but easily distracted, and the task that has been "
          "set him is the one every apprentice dreads: the apprentice must tidy a long shelf of N phials.\n\n"
          "The phials stand in a single row along the shelf, in the order in which they were filled, and each "
          "carries a mark. A phial that has been emptied is marked 0, while a full one carries its dose in drams. "
          "Over a long winter of fevers the emptied phials have come to be scattered the whole length of the "
          "shelf, mixed in among the full ones, and Mother Ambrosine wants them gathered out of the way. The "
          "apothecary has forbidden the use of a second shelf, because the only other shelf in the room holds the "
          "poisons and she will not have the two confused, so everything must be rearranged where it stands: "
          "every full phial slides toward the front without disturbing the order in which the full ones were "
          "arranged, and the emptied ones gather at the far end. The order of the emptied phials among themselves "
          "is of no interest to anybody. Report the shelf as it appears afterward.\n\n"
          "Tobias is under the impression that the dose marks indicate strength, and has been told twice that "
          "they do not. The infirmary cat sleeps in the empty crate by the door and objects to being moved. A "
          "travelling physician is expected on Thursday and Mother Ambrosine has strong views about him which she "
          "shares with anyone who stands still long enough.\n\n"
          "Input: the first line gives N. The second line gives the N marks along the shelf, front to back. "
          "Output: the N marks after the tidying, front to back.\n\n"
          "Constraints: N up to 10^6; each dose up to 10^9; only a constant amount of extra room is permitted, "
          "and a phial may only be exchanged with another phial already on the shelf.",
 "clues": ["forbidden the use of a second shelf", "without disturbing the order in which the full ones were arranged",
           "only a constant amount of extra room is permitted"],
 "decoys": ["the apprentice must tidy a long shelf", "The infirmary cat sleeps in the empty crate by the door",
            "A travelling physician is expected on Thursday"],
 "core": "Move the unwanted items to the back of the list, in place, keeping the order of everything else.",
 "gloss": [("dispensary", "a place where medicine is prepared and handed out", True),
           ("phial", "a small glass bottle", True), ("apothecary", "an old word for a pharmacist", True),
           ("dram", "a tiny unit of weight or volume", True)],
 "why": {"tp-partition": "Swapping items into groups scrambles the order of the ones you keep; here their order must survive.",
         "hs-freq": "Counting the empties does not rearrange anything."},
 "tell": "Rewrite in place, keep the survivors' order, and no spare memory."},

{"id": "sc-003", "v": "tp-merge", "dom": "monastery", "diff": "M",
 "title": "Two Scriptoria",
 "story": "The Cistercian houses of Clairvaux and Fontenay were founded within a decade of one another and have "
          "quarrelled, politely, ever since. Each maintains one of the two scriptoria, and each scriptorium maintains a "
          "register of the catalogue numbers of the codices it holds. The registers are the pride of their "
          "respective librarians: both were begun in the same century, both are written on vellum in a hand that "
          "has not changed in two hundred years, and both are entered in strictly ascending order, a discipline "
          "the librarians regard as the first duty of a learned house.\n\n"
          "The abbot of the mother house has lately conceived a plan. Books are costly, and a house that holds "
          "two copies of a common work while lacking a rare one is a house that has managed its library badly. He "
          "therefore wishes to know which numbers appear in BOTH registers, so that duplicate volumes can be "
          "exchanged for rarer ones with the booksellers of Troyes. He wants the shared numbers written out in "
          "ascending order on a single sheet, and he wants them soon, because the booksellers come only at "
          "Michaelmas.\n\n"
          "There is a practical difficulty. The registers are very long, running to as many as a million entries "
          "each, and the cellarer, who guards the memory-slates on which any working list would have to be "
          "drafted, has refused to issue any extra slate beyond the registers themselves. He has refused in "
          "writing, and he has refused twice. The abbot, who dislikes a quarrel with the cellarer more than he "
          "dislikes a badly managed library, will not press the point.\n\n"
          "The monk set to the work, Brother Fulbert, suffers from poor eyesight and reads with a lens ground for "
          "him in Paris. The refectory has served the same lentil pottage every Friday since Lent. A novice has "
          "been caught keeping a dog in the dormitory and the matter is before the chapter.\n\n"
          "Input: line one gives A and B, the lengths of the two registers. Line two gives the A numbers of "
          "Clairvaux, ascending; line three the B numbers of Fontenay, ascending. Output: the numbers present in "
          "both, in ascending order, or the word NONE.\n\n"
          "Constraints: A and B up to 10^6; catalogue numbers up to 10^9, with no number repeated within a "
          "register. Brother Fulbert may read down each register once and may not sort, copy or rewrite either.",
 "clues": ["entered in strictly ascending order", "which numbers appear in BOTH registers",
           "refused to issue any extra slate beyond the registers themselves"],
 "decoys": ["so that duplicate volumes can be exchanged for rarer ones",
            "suffers from poor eyesight and reads with a lens ground for him in Paris",
            "A novice has been caught keeping a dog in the dormitory"],
 "core": "Two lists that are already in order: list the values they share, without building any extra storage.",
 "gloss": [("scriptoria", "writing rooms of a monastery", True), ("codices", "hand-written books", True),
           ("cellarer", "the monk in charge of supplies", True), ("register", "an official written list", True)],
 "why": {"hs-seen": "A set would answer instantly but needs exactly the extra storage the cellarer refuses to give.",
         "hp-merge": "That uses a heap for many lists; with only two, a marker on each is enough."},
 "tell": "Two sorted sequences, find the common items, with no spare memory."},

{"id": "sc-004", "v": "tp-partition", "alt": ["hs-freq"], "dom": "railway", "diff": "M",
 "title": "The Karst Signal Gantry",
 "story": "On the Karst branch line, which climbs from the river valley to the limestone plateau through eleven "
          "tunnels and a viaduct that frightens the nervous, the signalling is done in the old way, by lamps hung "
          "along a gantry above the running lines. There are N signal lamps in a row, and each of them shows one "
          "of three states: 0 (red), 1 (amber) or 2 (green). The lamps are hung in whatever order the "
          "lampman happened to carry them up the ladder, which is to say in no order at all, and the district "
          "inspector has decided that this will no longer do.\n\n"
          "The inspector's order is that the lamps be regrouped so that, read from the first lamp to the last, "
          "all the reds come first, then all the ambers, then all the greens. The work must be done with the "
          "signalman's rotating crank, a device that can swap any two lamps on the gantry. The crank is mounted "
          "on a carriage that runs along the gantry, and here is the difficulty: it can be wound along the gantry "
          "exactly once, from the first lamp to the last, because winding it backwards strips the pinion, and the "
          "Company has not replaced a pinion since the war. There is no room on the gantry for a staging rack, so "
          "the lamps cannot be taken down and stood somewhere while the work proceeds. Report the final "
          "arrangement.\n\n"
          "The signalman on duty, a laconic man named Vrba, has worked the branch for twenty-two years and can "
          "tell which train is coming by the sound it makes in the second tunnel. The branch is famous among "
          "enthusiasts for a water tower in the shape of a mushroom. A goat belonging to the stationmaster at "
          "Horni Lhota has twice been found standing on the platform canopy, and no one can explain it.\n\n"
          "Input: line one gives N. Line two gives the N lamp states in order along the gantry. Output: the N "
          "states after the regrouping.\n\n"
          "Constraints: N up to 10^6; every state is 0, 1 or 2. The inspector has expressly forbidden the obvious "
          "dodge of counting how many lamps of each colour there are and then rewriting the gantry from the "
          "counts, since he wants the actual lamps moved.",
 "clues": ["one of three states", "exactly once, from the first lamp to the last",
           "no room on the gantry for a staging rack"],
 "decoys": ["On the Karst branch line", "famous among enthusiasts for a water tower in the shape of a mushroom",
            "A goat belonging to the stationmaster at Horni Lhota"],
 "core": "Arrange items of only three kinds into groups in a single pass, with no extra space.",
 "gloss": [("gantry", "a frame over a railway track that carries signals", True),
           ("pinion", "a small gear wheel", True),
           ("amber", "yellow-orange", True), ("signalman", "a railway worker who operates signals", True),
           ("laconic", "using very few words", True)],
 "why": {"tp-write": "Compacting handles two groups (keep or drop); three groups need two boundaries moving at once.",
         "hs-freq": "Counting and rewriting is correct but is a second pass; the statement allows only one."},
 "tell": "Exactly three kinds, one pass, in place."},

{"id": "sc-005", "v": "sw-fixed", "alt": ["ps-range"], "dom": "astronomy", "diff": "E",
 "title": "The Visiting Astronomer",
 "story": "The Halden Observatory stands on a basalt shoulder above the treeline, four hours by road from the "
          "nearest town, and it has been photographing the night sky since 1897. Its director, a formidable woman "
          "named Dr Ottilie Brandt, has spent her career defending the place from committees who would rather "
          "spend the money on a radio dish. The observatory logs, for each of N consecutive nights, the number of "
          "meteors its plates captured, one figure per night, written into a ledger in the order the nights "
          "occurred.\n\n"
          "An endowment allows the observatory to host one visiting astronomer each year, and the terms of the "
          "endowment, written by a benefactor with a tidy mind and no imagination, are precise: the visitor is "
          "permitted a residency of exactly K successive nights. The visitor this year, a young man from Uppsala "
          "with a great many opinions, will naturally choose the stretch that yields the greatest total number of "
          "captured meteors, since his paper depends upon it. The residency can neither be shortened nor split, "
          "and he may begin on any night he pleases so long as K nights remain. The director wonders, before he "
          "arrives and begins arguing, what that greatest total could be.\n\n"
          "The observatory's dome has a squeak that appears only in cold weather and that three engineers have "
          "failed to locate. The cook makes a cloudberry preserve that visitors write home about. There is a "
          "long-running dispute with a neighbouring farmer about a track across his land, and a gate that is "
          "sometimes locked and sometimes not.\n\n"
          "Input: line one gives N and K. Line two gives the N meteor counts in order of night. Output: the "
          "greatest total number of meteors over any K consecutive nights.\n\n"
          "Constraints: K at most N, N up to 2*10^5, each count up to 10^4. The director's calculating machine is "
          "elderly and she would rather not re-add K numbers afresh for every possible starting night, since the "
          "same figures would be added over and over.",
 "clues": ["exactly K successive nights", "the greatest total number of captured meteors",
           "can neither be shortened nor split"],
 "decoys": ["The observatory logs", "The cook makes a cloudberry preserve that visitors write home about",
            "a long-running dispute with a neighbouring farmer about a track across his land"],
 "core": "The biggest total over any run of exactly K neighbouring numbers.",
 "gloss": [("residency", "a fixed period of stay", True), ("successive", "following one right after another", True),
           ("plates", "glass photographic sheets used in old telescopes", True),
           ("endowment", "money given to support an institution", True)],
 "why": {"sw-longest": "Nothing asks for the longest or shortest stretch; the length is fixed in advance.",
         "ps-range": "A prefix table also gives every K-total and is a fair alternative; the moving version needs no table."},
 "tell": "A run of exactly K neighbours, with a total over each."},

{"id": "sc-006", "v": "sw-longest", "dom": "heraldry", "diff": "M",
 "title": "The Eastgate Herald",
 "story": "The Eastgate of the free city of Vehlbruck is the only gate through which an armed company may pass, "
          "and by an ordinance of the Diet every pennant carried beneath its arch must be recorded. The work "
          "falls to the herald, an elderly gentleman named Ser Albrecht Konigsmann, who stands in a wooden booth "
          "in all weathers with a slate and a stick of chalk. As each pennant passes he chalks the sigil of every "
          "pennant passing beneath the arch, one glyph per pennant, in strict order of passage. He has held the "
          "post for thirty-four years and is said never once to have left his booth before the gate was shut.\n\n"
          "The registrar of heraldry, a younger and more ambitious official, has been asked by the Diet to "
          "prepare a report on the movement of companies through the city, and he has fixed on a particular "
          "measurement. He wishes to learn the length of the longest unbroken procession in which no sigil "
          "recurs, since such a procession needs no cross-checking of the tally. A procession, for his purposes, "
          "is a run of pennants that passed one after another with none left out in the middle; he is not "
          "interested in which pennants it was made of, nor when it passed, only in how many pennants it "
          "contained.\n\n"
          "The herald is elderly and works slowly, but he has never once skipped a pennant. His chalk is supplied "
          "by the city at a cost that appears in the accounts each year and that the Treasurer has twice queried. "
          "The booth has a leaking roof. A pedlar sells hot chestnuts by the gate in winter and has an "
          "understanding with the gatekeeper that nobody writes down.\n\n"
          "Input: line one gives N, the number of glyphs in the chalk-log. Line two gives the N glyphs as a "
          "string of characters, in order of passage. Output: the length of the longest run of consecutive glyphs "
          "in which no glyph appears twice.\n\n"
          "Constraints: N up to 10^6; glyphs are printable characters from an alphabet of at most 256 marks. The "
          "registrar's clerk will not accept a method that examines every possible run separately.",
 "clues": ["in strict order of passage", "the longest unbroken procession in which no sigil recurs"],
 "decoys": ["since such a procession needs no cross-checking of the tally", "The booth has a leaking roof",
            "A pedlar sells hot chestnuts by the gate in winter"],
 "core": "The longest stretch of a sequence in which nothing repeats.",
 "gloss": [("sigil", "a symbol or emblem", True), ("pennant", "a small pointed flag", True),
           ("heraldry", "the study of coats of arms and emblems", True), ("ordinance", "a local law", True),
           ("recurs", "happens again", False), ("unbroken", "continuous, with no gap", False)],
 "why": {"hs-seen": "A set only says whether something was seen before; it cannot tell you where the valid stretch begins.",
         "sw-exact": "That counts stretches with exactly K of something; here you want the single longest one."},
 "tell": "The longest unbroken stretch obeying a rule that a repeat would break."},

{"id": "sc-007", "v": "sw-shortest", "dom": "irrigation", "diff": "M",
 "title": "The Drought Petition",
 "story": "The Lower Fen Canal Authority administers a system of waterways cut across the peat in the eighteenth "
          "century by a company that went bankrupt twice before finishing. The Authority has strung N sluice "
          "basins in a row along the main cut, each basin fed from the one above it, and the engineer's book "
          "records what each can give: basin i can release a[i] kilolitres each day. The basins are numbered from "
          "the head of the cut to its mouth, and that numbering has not changed since 1802, which is why basin "
          "seventeen lies between basins four and five on the ground, a fact that causes trouble every summer.\n\n"
          "This has been the driest spring in living memory. A drought-stricken farmer whose land lies along the "
          "cut needs a daily draw of at least T kilolitres to keep her herd alive, and she is entitled to apply "
          "for it. But under the canal statutes she may only draw from a run of basins that adjoin one another, "
          "with no gap, because the Authority will not open a gate that has a closed gate below it. Every basin "
          "she petitions for must be surveyed by an inspector at her own expense, at eleven guineas a basin, and "
          "she has not got eleven guineas to spare. She therefore wishes to petition as few basins as possible. "
          "Report the least number of adjoining basins whose combined release reaches T, or 0 if even the whole "
          "canal cannot.\n\n"
          "The Authority's offices are in a converted maltings and smell of it. The clerk who issues the "
          "petitions has a cold he has had since Candlemas. A heron has taken up residence on basin nine and is "
          "regarded by the lightermen as a bird of ill omen, though the engineer says it is simply a heron.\n\n"
          "Input: line one gives N and T. Line two gives the N daily releases in order along the cut. Output: the "
          "smallest number of adjoining basins whose releases total at least T, or 0.\n\n"
          "Constraints: N up to 10^5, T up to 10^9, a[i] at least 1 and at most 10^4. Checking every possible run "
          "of basins separately would cost the farmer her summer.",
 "clues": ["a run of basins that adjoin one another, with no gap", "as few basins as possible",
           "at least T kilolitres", "a[i] at least 1"],
 "decoys": ["drought-stricken", "petition", "A heron has taken up residence on basin nine",
            "The Authority's offices are in a converted maltings and smell of it"],
 "core": "The shortest stretch of neighbouring positive numbers whose total reaches a target.",
 "gloss": [("sluice", "a gate that controls the flow of water", True), ("statutes", "written laws", True),
           ("petition", "to formally request", True), ("adjoin", "to lie right next to", True),
           ("maltings", "a building where grain is prepared for brewing", True)],
 "why": {"sw-longest": "That wants the longest valid stretch; here shorter is better.",
         "ps-count": "There are no negatives, so no table of earlier totals is needed."},
 "tell": "Neighbouring, as few as possible, 'at least', and every value positive."},

{"id": "sc-008", "v": "sw-exact", "dom": "textile", "diff": "H",
 "title": "The Guild Examiner",
 "story": "Calder Mill has dyed cloth for six generations of the same family, and the dye-works at the bottom of "
          "the yard is the oldest part of it, a low building of blackened brick where the vats stand in two rows "
          "and the floor is permanently wet. Bolts of cloth emerge from the vats in a fixed sequence, each "
          "stamped with a shade number as it comes off the roller, and the sequence is never shuffled afterwards, "
          "because the stamping clerk writes the numbers into the day-book as they pass and the day-book is what "
          "the Guild inspects.\n\n"
          "The guild examiner, a dry and unhurried man named Mr Pargeter, comes twice a year from Halifax. He "
          "inspects any run of consecutive bolts, meaning a stretch of the day's output with nothing left out in "
          "the middle, and he will certify a run only if it displays exactly K distinct shades, no more and no "
          "fewer, a rule that dates from a dispute about the mixing of dye-lots and that nobody has thought to "
          "revise. Two runs are different if their first or last bolt differs, even if the shades in them are "
          "the same. For the pattern-book, the examiner needs the total number of certifiable runs in the "
          "day's output.\n\n"
          "The mill's own pattern-book is bound in green buckram and kept in a cupboard that sticks. Mr Pargeter "
          "takes his tea with three sugars, a thing the office remarks on every time. The dye-works cat has a "
          "patch of permanently blue fur from an incident with a vat of woad, and is known throughout the valley "
          "on that account.\n\n"
          "Input: line one gives N, the number of bolts, and K. Line two gives the N shade numbers in the order "
          "they came off the roller. Output: the number of runs of consecutive bolts containing exactly K "
          "distinct shades.\n\n"
          "Constraints: N up to 10^5 bolts, 1 <= K <= N, shade numbers up to 10^9. The answer may be large enough "
          "to need a 64-bit integer. Mr Pargeter has a train to catch and will not wait while every run is "
          "examined against every other.",
 "clues": ["any run of consecutive bolts", "exactly K distinct shades, no more and no fewer",
           "the total number of certifiable runs"],
 "decoys": ["For the pattern-book", "takes his tea with three sugars",
            "The dye-works cat has a patch of permanently blue fur"],
 "core": "Count every stretch that contains exactly K different values.",
 "gloss": [("bolts", "rolls of cloth", True), ("guild", "a trade association", True),
           ("certify", "to officially approve", True), ("vats", "large tubs for liquids", True),
           ("buckram", "a stiff cloth used for binding books", True)],
 "why": {"sw-longest": "That finds one best stretch; this counts every qualifying stretch.",
         "ps-count": "Prefix totals count stretches with a given sum; 'K different values' is not a sum."},
 "tell": "A COUNT of stretches with EXACTLY K distinct items."},

{"id": "sc-009", "v": "sw-deque", "dom": "lighthouse", "diff": "M",
 "title": "The Skerry Light",
 "story": "The Skerry light stands on a rock three miles off a coast that has wrecked more ships than the county "
          "has churches, and it is kept by a man named Ewan Blaikie, who came out for a six-month relief in 1978 "
          "and never went back. The light's duties include a weather log, and the log is exacting: the keeper "
          "records the swell height in the channel once every minute for N minutes, one figure per minute, in the "
          "order the minutes occur. He has done it through two hurricanes and one appendicitis.\n\n"
          "The Board of Trinity, which has authority over the lights, has issued a new instruction. It demands, "
          "for every unbroken span of K minutes, the single highest swell seen in that span, so that mariners may "
          "be warned of surges before they reach the shipping lane. The spans overlap: the first covers minutes "
          "one to K, the next covers minutes two to K plus one, and so on to the end of the log. The keeper must "
          "produce one figure per span, from the earliest span to the latest, within a time proportional to N, "
          "because the figures go out on the shipping forecast and the forecast will not be held back for "
          "him.\n\n"
          "Blaikie's first attempt at the instruction was to look through all K minutes of each span and pick out "
          "the largest, which took him until the following afternoon and produced a letter from the Board. The "
          "rock has a colony of grey seals that bark through the night in spring. The relief boat comes "
          "fortnightly, weather permitting, and in February it often does not. There is a chess game in progress "
          "by letter with a keeper in the Hebrides that has lasted eleven months.\n\n"
          "Input: line one gives N and K. Line two gives the N swell heights in order of minute. Output: N - K + "
          "1 figures, the highest swell within each span, in order.\n\n"
          "Constraints: K at most N, N up to 10^6, heights up to 10^9. The work done per minute of the log must "
          "stay roughly constant, however large K becomes.",
 "clues": ["every unbroken span of K minutes", "the single highest swell seen in that span",
           "within a time proportional to N"],
 "decoys": ["so that mariners may be warned of surges", "The rock has a colony of grey seals that bark through the night",
            "There is a chess game in progress by letter with a keeper in the Hebrides"],
 "core": "For every fixed-size stretch, report its maximum, within linear time.",
 "gloss": [("swell", "a long rolling wave", True), ("Board of Trinity", "an old authority over lighthouses", True),
           ("mariners", "sailors", True), ("proportional", "growing at the same rate as", True),
           ("relief", "a replacement worker, or their period of duty", True)],
 "why": {"sw-fixed": "A running total can add one number and drop one; a maximum cannot be updated that way.",
         "hp-topk": "That works in N log N; the linear limit asks for something leaner."},
 "tell": "The maximum of EVERY fixed-size stretch, in linear time."},

{"id": "sc-010", "v": "ps-range", "dom": "archive", "diff": "E",
 "title": "The Muniment Room",
 "story": "Castle Harrow has been in the same family since the Conquest, give or take a confiscation under the "
          "Tudors, and the muniment room on its second floor holds the paper record of all of it. The room has N "
          "shelves along one wall; shelf i holds a[i] bound deeds, and nothing is ever added or removed, the "
          "family having deposited the whole archive with the county under an agreement that forbids it. The "
          "archivist, a patient man named Mr Enderby, has catalogued the shelves from the window end to the door "
          "end and considers the job the great work of his life.\n\n"
          "Since the agreement was signed, surveyors descend in great numbers. They come from the Land "
          "Registry, from two universities, from a firm of solicitors pursuing a boundary dispute that began in "
          "1736, and from a television company. Each wishes to know, for a stretch of shelves from L to R, how "
          "many deeds lie upon them in total, because the fee they pay the county is reckoned per deed consulted "
          "and they must budget in advance. The stretches they ask about are all different, some covering two "
          "shelves and some covering nearly the whole wall, and they ask one after another, all day.\n\n"
          "With as many as 2*10^5 surveyors and shelves, the archivist declines to count by hand each time. He "
          "has noticed, in the course of a long and irritating fortnight, that he keeps adding up the very same "
          "shelves over and over for one surveyor after another.\n\n"
          "The muniment room is kept at a fixed humidity by a machine that hums. The castle's tea room sells a "
          "fruit cake made to a recipe attributed, on no evidence at all, to a Victorian countess. A barn owl "
          "roosts in the gatehouse and is on the county's letterhead.\n\n"
          "Input: line one gives N and Q, the number of shelves and of surveyors. Line two gives the N shelf "
          "counts. Each of the next Q lines gives L and R. Output: for each surveyor, the total number of deeds "
          "on shelves L to R inclusive.\n\n"
          "Constraints: N and Q up to 2*10^5; each shelf holds up to 10^4 deeds. Every answer should take about "
          "the same time to produce, however wide the stretch asked about.",
 "clues": ["nothing is ever added or removed",
           "for a stretch of shelves from L to R, how many deeds lie upon them in total",
           "as many as 2*10^5 surveyors"],
 "decoys": ["Castle Harrow", "A barn owl roosts in the gatehouse and is on the county's letterhead",
            "a fruit cake made to a recipe attributed, on no evidence at all, to a Victorian countess"],
 "core": "Many questions about the total of a range of a list that never changes.",
 "gloss": [("muniment room", "a room for keeping important documents", True),
           ("deeds", "legal documents about owning property", True), ("archivist", "a keeper of records", True),
           ("confiscation", "the taking of property by authority", True)],
 "why": {"sw-fixed": "A fixed-width window handles one repeated width; these ranges differ in length and position.",
         "ps-diff": "That is for many updates read once; here the data is fixed and the questions are many."},
 "tell": "Many range totals over data that never changes."},

{"id": "sc-011", "v": "ps-count", "dom": "commerce", "diff": "M",
 "title": "The Counting-House Daybook",
 "story": "The counting-house of Merchant Orsini occupies the ground floor of a tall narrow building on the "
          "Riva degli Schiavoni, and it has traded in pepper, alum and, latterly, insurance since the reign of "
          "the old duke. Its books are famously tidy. Each day the counting-house enters either a gain or a loss, "
          "never both and never nothing, so the daybook is a row of N signed figures, one for each day the house "
          "has traded, in the order the days fell.\n\n"
          "An auditor has been appointed by the Council, following an unrelated scandal at a rival house, and he "
          "has become curious about unbroken stretches of days. His question is this: how many different "
          "stretches have a net result of exactly T? A stretch is a run of days with none omitted from the "
          "middle, and stretches are distinct when their first or last day differ, even if the figures within "
          "them happen to be the same. He does not want the stretches themselves written out, which would fill a "
          "room; he wants the count.\n\n"
          "The auditor is aware of a trap. Because the house enters losses as well as gains, figures may be "
          "negative, and so lengthening a stretch does not necessarily push its total upward; a long stretch can "
          "have a smaller total than a short one inside it. He mentions this in his instructions because his "
          "predecessor got it wrong and the resulting report was withdrawn.\n\n"
          "Orsini's clerk keeps a tame starling in the office that can imitate the bell of the Arsenale. The "
          "house's gondolier is paid more than its bookkeeper, a fact the bookkeeper raises annually. There is a "
          "painting of the founder in the hall which the family privately agrees is a poor likeness.\n\n"
          "Input: line one gives N and T. Line two gives the N daily figures in order. Output: the number of "
          "runs of consecutive days whose figures total exactly T.\n\n"
          "Constraints: N up to 2*10^5; each figure between -10^9 and 10^9; T between -10^14 and 10^14. The "
          "answer may need a 64-bit integer. Examining every stretch against every other is beyond the auditor's "
          "patience and his fee.",
 "clues": ["how many different stretches have a net result of exactly T", "figures may be negative",
           "unbroken stretches of days"],
 "decoys": ["Merchant Orsini", "keeps a tame starling in the office that can imitate the bell of the Arsenale",
            "There is a painting of the founder in the hall which the family privately agrees is a poor likeness"],
 "core": "Count the stretches whose total equals a target, when values can be negative.",
 "gloss": [("daybook", "an old ledger of daily transactions", True), ("auditor", "someone who checks accounts", True),
           ("net", "what is left after subtracting losses", True), ("alum", "a mineral salt used in dyeing", True)],
 "why": {"sw-exact": "Shrinking a stretch only lowers its total when the numbers are positive; with negatives that fails.",
         "ps-longest": "That wants the single longest such stretch, not how many there are."},
 "tell": "A count, a target total, and negatives allowed."},

{"id": "sc-012", "v": "ps-longest", "dom": "beekeeping", "diff": "M",
 "title": "The Apiarist's Scale",
 "story": "Mrs Honoria Veale, an apiarist by trade, keeps bees on the edge of a heath in the west of the county, and she has done so for "
          "long enough that the local honey show has been renamed in her honour, a thing she affects to find "
          "embarrassing. Her hives stand on scales of her late husband's making, and she weighs the hive at dusk "
          "on each of N evenings and notes how much it gained or lost since the previous evening (a loss is a "
          "negative figure). The figures go into a notebook with a rubber band round it, one line per evening, in "
          "order.\n\n"
          "A scientist from the agricultural college has written to her about a theory of his concerning forage "
          "and colony mass, and he wants a particular measurement from her records. He hopes to find the most "
          "extended run of consecutive evenings during which the hive's net change was exactly K grams. A run is "
          "a stretch of evenings with none skipped in the middle; he does not care when it occurred, nor how many "
          "such runs there were, only which is the longest. Report the number of evenings in that longest run, or "
          "0 if no run reaches K.\n\n"
          "Mrs Veale has pointed out, in a letter the scientist has not yet answered, that because a hive can "
          "lose weight as easily as gain it, a longer stretch is not necessarily a heavier one, and that this "
          "has caught out at least one previous correspondent of hers from a university she declines to name.\n\n"
          "The heath is grazed by Dartmoor ponies that lean on the hive stands. Her smoker is fuelled with dried "
          "lavender, which she maintains the bees prefer and which the college man says can make no difference. "
          "A badger took three frames in 2019 and the fence has been electrified ever since.\n\n"
          "Input: line one gives N and K. Line two gives the N nightly changes in order of evening. Output: the "
          "number of evenings in the longest run of consecutive evenings whose changes total exactly K, or 0.\n\n"
          "Constraints: N up to 2*10^5; each change between -10^6 and 10^6; K between -10^9 and 10^9. Trying "
          "every start against every end will not finish before the honey show.",
 "clues": ["the most extended run of consecutive evenings", "net change was exactly K grams",
           "a loss is a negative figure"],
 "decoys": ["weighs the hive at dusk", "Her smoker is fuelled with dried lavender",
            "The heath is grazed by Dartmoor ponies that lean on the hive stands"],
 "core": "The longest stretch whose total equals a target, with negative values possible.",
 "gloss": [("apiarist", "a beekeeper", True), ("extended", "long, covering a large span", True),
           ("net change", "the overall difference after gains and losses are combined", True),
           ("forage", "food that animals find for themselves", True)],
 "why": {"sw-longest": "A moving stretch needs totals that only grow; negatives break that.",
         "ps-count": "That counts stretches; you need only the widest one."},
 "tell": "The longest stretch, a target total, and negatives present."},

{"id": "sc-013", "v": "ps-2d", "dom": "vineyard", "diff": "M",
 "title": "The Brevet Vineyard",
 "story": "Chateau Brevet lies on a south-facing slope above a river that floods about once a decade, and it has "
          "been making a wine of respectable rather than distinguished quality since the eighteen-forties. The "
          "estate is surveyed as a grid of R rows by C columns of vines, a scheme imposed by a Napoleonic "
          "surveyor and never revised, and each plot is recorded by a single digit, the number of crates it "
          "yielded at the last harvest. The register of yields hangs in the cellar office on a board, and the "
          "regisseur consults it a dozen times a day.\n\n"
          "The estate sells chiefly to brokers, and brokers telephone constantly with requests of the form: for "
          "the rectangle whose opposite corners are (r1, c1) and (r2, c2), what was the total yield? They ask "
          "because they buy by the parcel and a parcel is always a rectangle of plots. The rectangles they ask "
          "about overlap one another freely, some covering a few vines and some covering most of the slope, and "
          "the broker on the line expects an answer while he waits, because he has four other estates to call "
          "before noon.\n\n"
          "The yields are never revised; the harvest is over and the figures are lodged with the appellation "
          "authority, so no plot's number will change between one telephone call and the next. But there may be "
          "up to 10^5 calls in a season, and each answer must be returned almost instantly. The regisseur, who "
          "has been adding up plots by hand with a ruler laid across the board, has observed that he adds the "
          "same plots again and again, call after call.\n\n"
          "The estate's dog is a lurcher of uncertain parentage that sleeps in the fermentation shed. A heatwave "
          "in the third week of August is still discussed. The owner's son has ideas about orange wine which the "
          "owner has described, in writing, as a fashion.\n\n"
          "Input: line one gives R, C and Q. The next R lines give C digits each, the yields. The next Q lines "
          "each give r1, c1, r2, c2. Output: for each call, the total yield inside that rectangle, borders "
          "included.\n\n"
          "Constraints: R and C up to 1000; Q up to 10^5; each yield a single digit 0 to 9.",
 "clues": ["for the rectangle whose opposite corners are (r1, c1) and (r2, c2), what was the total yield",
           "never revised", "up to 10^5 calls"],
 "decoys": ["Chateau Brevet", "The estate's dog is a lurcher of uncertain parentage",
            "The owner's son has ideas about orange wine"],
 "core": "Many questions about the total of a rectangle in a grid that never changes.",
 "gloss": [("brokers", "middlemen who arrange sales", True), ("surveyed", "measured and mapped", True),
           ("yield", "the amount produced", True), ("plot", "a small piece of land", True),
           ("regisseur", "the manager of a wine estate", True)],
 "why": {"ps-range": "A one-dimensional table handles a stretch of one row; a rectangle needs both directions.",
         "dp-grid": "That finds best paths or counts of paths; these are plain totals."},
 "tell": "Many rectangle totals over a grid that never changes."},
]
