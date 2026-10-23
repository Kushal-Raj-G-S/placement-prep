# -*- coding: utf-8 -*-
"""Scenario questions, batch 4: bits (rest), linked lists, trees, trie (first).

OA-size stories (around 400 words) with their own Input / Output / Constraints lines. The answer keys
(v, alt, core, why, tell) are the originals.
"""

QUESTIONS = [

{"id": "sc-040", "v": "bt-subsets", "alt": ["bk-subsets"], "dom": "spice trade", "diff": "M",
 "title": "The Zanzibar Coffers",
 "story": "The spice-merchant Abdulrahman bin Salim keeps a warehouse on the shore road at Zanzibar, below the "
          "old fort, and his trade in cloves has made him rich enough to be worth taxing and not quite rich "
          "enough to be left alone. He owns N sealed coffers, the i-th holding v[i] gold dinars, and the seals "
          "are his own, stamped with a device his grandfather brought from Muscat.\n\n"
          "A tax assessor has arrived from the mainland with a warrant and a clerk. He insists on examining some "
          "selection of coffers, any selection including the empty one, which the merchant finds absurd and the "
          "assessor defends by reference to the regulation as written. The sultan, who has taken a personal "
          "interest for reasons connected with a disputed cargo of ivory, will pardon the merchant only if the "
          "combined value of the chosen coffers equals exactly S dinars, where S may be as large as 10^9.\n\n"
          "The sultan's question, put to his own treasurer rather than to the merchant, is this: in how many "
          "different selections does the combined value equal S? Two selections differ if they include "
          "different coffers, even if their totals are the same, and a coffer is either in a selection or it is "
          "not; none may be opened and part of its contents taken.\n\n"
          "The merchant has few coffers but very large sums in them, N being at most 18, which is why his "
          "grandfather preferred a few strong boxes to many weak ones. The warehouse cats are fed on fish heads "
          "and are a byword in the quarter. The assessor's clerk has a cough that the merchant hopes, "
          "uncharitably, will carry him off before the audit concludes. A dhow from Sur is overdue and the "
          "merchant has not slept well.\n\n"
          "Input: line one gives N and S. Line two gives the N coffer values. Output: the number of selections "
          "of coffers whose values total exactly S.\n\n"
          "Constraints: N up to 18; each value up to 10^9; S up to 10^9. The answer fits in a 64-bit integer.",
 "clues": ["N being at most 18", "any selection including the empty one", "S may be as large as 10^9",
           "how many different selections does the combined value equal S"],
 "decoys": ["The spice-merchant Abdulrahman bin Salim", "The warehouse cats are fed on fish heads",
            "A dhow from Sur is overdue and the merchant has not slept well"],
 "core": "Count the subsets with a given total, when there are very few items but the total can be huge.",
 "gloss": [("coffers", "strong boxes for valuables", True), ("dinars", "old gold coins", True),
           ("assessor", "an official who judges value", True), ("pardon", "to forgive", True),
           ("dhow", "a traditional Arab sailing boat", True)],
 "why": {"dp-knapsack": "A table indexed by the total would be 10^9 wide; with so few items, trying every subset is cheaper.",
         "bk-subsets": "Also enumerates subsets and is a fair alternative; the bit-mask form is the compact one."},
 "tell": "A tiny N (about 18) and a huge target: enumerate every subset."},

{"id": "sc-041", "v": "bt-dp", "dom": "opera", "diff": "H",
 "title": "The Milan Impresario",
 "story": "Signor Gualtiero Bassani has been an impresario in Milan for thirty years, which is to say he has "
          "been bankrupt three times and celebrated twice. He is assembling a season, and a season is a matter "
          "of arithmetic before it is a matter of art. He has N tenors under consideration and N operas to "
          "fill, N being at most 16, and his agent has produced a table: engaging tenor i for opera j costs "
          "c[i][j] lire, a figure that takes in the fee, the lodging, the tenor's wife and whatever else the "
          "tenor's representative has thought to put in it.\n\n"
          "The costs vary wildly and not sensibly. A tenor who is cheap in one opera may be ruinous in another, "
          "because he has sung the first a hundred times and must learn the second, or because he has quarrelled "
          "with the conductor of one and not the other. Every tenor must sing exactly one opera, since a tenor "
          "engaged for the season and left idle must still be paid, and every opera must be sung by exactly one "
          "tenor, since the subscribers have bought tickets for all of them.\n\n"
          "The impresario wants the least total cost of such an assignment. Simply trying all N! pairings would "
          "exceed the season, as his nephew demonstrated with a pencil and a great deal of paper. He has also "
          "noticed that once he has decided which tenors are already placed, it makes no difference at all in "
          "what order he placed them: what the remaining choices cost depends only on who is left.\n\n"
          "The accountant, who is a gloomy man, weeps at every figure. The theatre's chandelier was lowered onto "
          "a dowager in 1894. A claque in the upper gallery can be hired for forty lire and the impresario "
          "budgets for it without writing it down.\n\n"
          "Input: line one gives N. The next N lines give N costs each: row i, column j is the cost of tenor i "
          "in opera j. Output: the least total cost of a complete assignment.\n\n"
          "Constraints: N up to 16; each cost up to 10^6.",
 "clues": ["N tenors under consideration and N operas to fill, N being at most 16", "exactly one opera",
           "exactly one tenor", "the least total cost",
           "it makes no difference at all in what order he placed them"],
 "decoys": ["accountant, who is a gloomy man, weeps at every figure",
            "The theatre's chandelier was lowered onto a dowager in 1894",
            "A claque in the upper gallery can be hired for forty lire"],
 "core": "Assign N workers to N jobs at least total cost, when N is small enough to remember which jobs are already taken.",
 "gloss": [("impresario", "a manager of theatrical productions", True), ("tenor", "a male singer", True),
           ("lire", "old Italian money", True), ("engaging", "hiring", True),
           ("claque", "a group paid to applaud", True)],
 "why": {"gr-pair": "Matching the cheapest pairs first fails because early choices block later ones.",
         "bt-subsets": "That counts selections; here the state must remember WHICH jobs are used while the assignment is built."},
 "tell": "N about 16 and a one-to-one assignment: remember which are used."},

{"id": "sc-042", "v": "bt-tricks", "dom": "railway signalling", "diff": "E",
 "title": "The Crewe Signal-Box",
 "story": "Crewe is the busiest junction on the West Coast line and its signalling has been rebuilt four times "
          "without ever being simplified. The signal-box keeps a status word for each of its signals: a 32-bit "
          "number in which every set bit means one lamp is lit, the bits standing for the aspects, the route "
          "indications, the track circuits and a dozen other things that the men in the box read at a glance "
          "and that nobody else can read at all.\n\n"
          "The regional inspector, Mr Haverfield, is compiling a report on lamp failures, a subject on which he "
          "has become monomaniacal since a signal at Basford Hall was found dark for three weeks. He sends in "
          "10^6 status words, taken from the box's recording drum over a period of months, and wishes to learn, "
          "for each, how many lamps are lit, so that the fault log can be filled in at once. He wants the count "
          "only, not which lamps, and he wants one figure per word in the order the words were recorded.\n\n"
          "Reading each of the 32 positions for every word would be wasteful when only a handful of lamps are "
          "usually lit, a point the box's own relief signalman made to the inspector and which the inspector "
          "has conceded in writing. He has also asked, in a postscript, to be told which of the words have "
          "precisely one lamp lit, since a single lamp usually means the box has been switched out.\n\n"
          "The box has a stove and a kettle and a cat that is officially not there. A model of the layout, built "
          "by a signalman over eleven years, hangs in the mess room. The drum's paper tape jams in damp weather "
          "and is beaten with a ruler.\n\n"
          "Input: line one gives M. Line two gives the M status words. Output: on the first line, M counts of "
          "lit lamps in order; on the second line, the number of words with precisely one lamp lit.\n\n"
          "Constraints: M up to 10^6; each status word below 2^32.",
 "clues": ["32-bit number", "every set bit means one lamp is lit", "how many lamps are lit",
           "only a handful of lamps are usually lit", "precisely one lamp lit"],
 "decoys": ["so that the fault log can be filled in at once",
            "A model of the layout, built by a signalman over eleven years, hangs in the mess room",
            "The box has a stove and a kettle and a cat that is officially not there"],
 "core": "Count how many 1-bits are set in each of many numbers, quickly.",
 "gloss": [("signal-box", "a small building from which railway signals are controlled", True),
           ("status word", "a number that records the state of something", True),
           ("lit", "switched on", True), ("monomaniacal", "obsessed with one subject", True),
           ("aspects", "the colours a railway signal can show", True)],
 "why": {"bt-xor": "That cancels pairs to find an odd one out; this counts set bits.",
         "hs-freq": "That counts occurrences of values; here you count bits inside a single number."},
 "tell": "Count the set bits of a number."},

{"id": "sc-043", "v": "ll-fastslow", "dom": "lighthouses", "diff": "M",
 "title": "The Scottish Beacon Chain",
 "story": "Before the telegraph reached the west coast, the Commissioners of Northern Lights maintained a chain "
          "of beacons by which word of a wreck could be passed from headland to headland. A lighthouse chain on "
          "the Scottish coast joins N beacons, each knowing only the beacon after it; the last beacon knows no "
          "successor, and no beacon knows the one behind it, because the sight-lines were cut one way along the "
          "coast and never surveyed in the other direction.\n\n"
          "Each beacon has a value engraved on its lintel, a number assigned when it was built, and the "
          "Commissioners have asked the present keeper for one particular figure. Standing at the first beacon, "
          "she can walk the chain once from first to last, following each beacon's instruction to the next, but "
          "she cannot count the beacons beforehand and has no list of them: the register was lost when the "
          "Commissioners' office at Oban burned in 1901 and has never been reconstructed. Yet at the end of that "
          "single walk, she must name the value engraved on the middle beacon, and where N is even she must name "
          "the second of the two middle ones.\n\n"
          "She may carry what she can hold in her head, which is to say a few numbers, and she cannot retrace "
          "her steps once she has moved on, since the path between two beacons runs one way round a cliff and "
          "the tide takes it.\n\n"
          "The chain is still lit once a year on the anniversary, chiefly for photographers. A seal colony at the "
          "third beacon has been counted annually since 1963. The keeper's predecessor wrote a monograph on "
          "lichens which is held in some regard by people who care about lichens.\n\n"
          "Input: line one gives N. Line two gives the N engraved values, from the first beacon to the last. "
          "Output: the value on the middle beacon.\n\n"
          "Constraints: N up to 10^6; values up to 10^9. Extra memory must not grow with N.",
 "clues": ["each knowing only the beacon after it", "cannot count the beacons beforehand", "that single walk",
           "the middle beacon"],
 "decoys": ["A lighthouse chain on the Scottish coast",
            "A seal colony at the third beacon has been counted annually since 1963",
            "wrote a monograph on lichens which is held in some regard"],
 "core": "Find the middle item of a one-way chain in a single pass, without knowing its length.",
 "gloss": [("beacon", "a signal fire or light", True), ("engraved", "carved into a surface", True),
           ("successor", "the one that follows", True), ("lintel", "the stone across the top of a door", True),
           ("monograph", "a detailed study of one subject", True)],
 "why": {"ll-reverse": "Reversing the chain rewires links but does not locate the middle.",
         "hs-index": "Storing every beacon by position needs memory for the whole chain."},
 "tell": "The middle of a one-way chain, in one pass, with the length unknown."},

{"id": "sc-044", "v": "ll-reverse", "dom": "rail travel", "diff": "E",
 "title": "The Trans-Siberian Carriages",
 "story": "At Vladivostok the Trans-Siberian is made up for its return journey, and the making-up is done in a "
          "yard laid out in 1908 for shorter trains than the ones that use it now. The carriages of the "
          "Trans-Siberian, N in all, are coupled one behind another, each carriage knowing only the one it is "
          "coupled to, because the coupling records are kept on a plate at the rear of each carriage and there "
          "is no corresponding plate at the front.\n\n"
          "The yardmaster wishes to turn the whole train around so that the last carriage leads and the first "
          "trails. The reason is the restaurant car, which must sit behind the locomotive on the westbound run "
          "and ahead of it on the eastbound, a rule that dates from a minister's complaint about smoke and that "
          "has survived both the revolution and the end of steam.\n\n"
          "The siding has no spare track: the carriages must be re-coupled in place, without moving them to a "
          "second track or copying the list. The yard's only spare road has been occupied since March by a crane "
          "that cannot be moved until a part arrives from Yekaterinburg. Report the new order from the engine's "
          "end.\n\n"
          "The samovar in carriage four has been in service since the Brezhnev era and is the subject of a "
          "preservation campaign. A conductor keeps a cactus on the window ledge of her compartment. The yard "
          "cat has produced four kittens in the brake van and the yardmaster has been told about it by everyone "
          "except the conductor responsible.\n\n"
          "Input: line one gives N. Line two gives the N carriage numbers from the engine's end to the tail. "
          "Output: the N carriage numbers after the turning, from the engine's end.\n\n"
          "Constraints: N up to 10^6; carriage numbers up to 10^9. Only the couplings between neighbours may be "
          "altered, and extra memory must not grow with N.",
 "clues": ["each carriage knowing only the one it is coupled to", "re-coupled in place",
           "without moving them to a second track or copying the list"],
 "decoys": ["The yardmaster wishes to turn the whole train around",
            "The samovar in carriage four has been in service since the Brezhnev era",
            "The yard cat has produced four kittens in the brake van"],
 "core": "Reverse a one-way chain of items in place.",
 "gloss": [("coupled", "joined together", True), ("yardmaster", "the officer in charge of a railway yard", True),
           ("siding", "a short side track", True), ("trails", "comes last", True),
           ("samovar", "a Russian urn for heating water", True)],
 "why": {"ll-dummy": "A dummy front node helps when the first item might be deleted; here nothing is deleted.",
         "tp-ends": "That reverses an array by swapping from both ends; a one-way chain cannot be walked backward."},
 "tell": "Reverse a linked list in place."},

{"id": "sc-045", "v": "ll-dummy", "dom": "church bells", "diff": "M",
 "title": "The Bell-Ringers' Roll",
 "story": "St Mary's has a ring of eight and a band of ringers who have fallen out with one another in every "
          "possible combination over the past forty years. The bell-ringers' roll is a chain of N entries, each "
          "holding a peal number and knowing only the entry after it, kept in that form since the Victorian "
          "restoration because the roll is written on a single long strip pasted into the tower book.\n\n"
          "A difficulty has arisen over the peals rung during the incumbency of a previous vicar, which the "
          "diocese has ruled were not properly recorded and must come out of the roll. The present vicar "
          "therefore decrees that every entry bearing the forbidden number V be struck from the roll, wherever "
          "it stands, and V may well appear in the very first entry as well as in later ones, even several in a "
          "row, since the peals in question were rung in a burst one summer.\n\n"
          "The chain must be edited where it stands, the strip being pasted in and the tower book being, by the "
          "diocese's own ruling, the primary record. What survives must stay in its original order, and the "
          "vicar wants the new first entry, since the roll is read aloud from its head at the annual "
          "meeting.\n\n"
          "The tenor bell is cracked and has been rung half-muffled since 2011. A ringer has been banned from "
          "the tower twice and reinstated twice. The tower captain keeps a biscuit tin to which he alone has the "
          "key, a fact that is resented more than the bell.\n\n"
          "Input: line one gives N and V. Line two gives the N peal numbers in roll order. Output: the surviving "
          "peal numbers in order, or the word EMPTY if none survive.\n\n"
          "Constraints: N up to 10^6; peal numbers up to 10^9. The chain is edited in place by re-linking; no "
          "second roll may be written out.",
 "clues": ["every entry bearing the forbidden number V be struck from the roll",
           "in the very first entry as well as in later ones", "even several in a row"],
 "decoys": ["The present vicar therefore decrees", "The tenor bell is cracked and has been rung half-muffled since 2011",
            "The tower captain keeps a biscuit tin to which he alone has the key"],
 "core": "Delete every item with a given value from a one-way chain, including possibly the first.",
 "gloss": [("peal", "a set of bell chimes", True), ("vicar", "a parish priest", True),
           ("decrees", "orders officially", True), ("struck", "removed", True),
           ("incumbency", "the period someone holds a post", True)],
 "why": {"ll-reverse": "Nothing here asks for the order to be reversed.",
         "tp-write": "That compacts an array in place; a chain is edited by re-linking, and the first entry may be removed."},
 "tell": "Deleting from a linked list where the head itself may go."},

{"id": "sc-046", "v": "ll-merge", "dom": "navigation", "diff": "E",
 "title": "The Two Almanacs",
 "story": "The two university presses have published rival tide almanacs since the seventeenth century, and the "
          "rivalry is now the only reason either of them still does it. Two almanac-makers, one in Oxford and "
          "one in Cambridge, each keep a chain of tide entries, every entry knowing only the next, and each "
          "chain already ordered by ascending hour, because each maker enters his observations as he makes them "
          "and neither has ever had cause to reorder anything.\n\n"
          "This year the Admiralty, which pays for both and has grown tired of paying twice, has required a "
          "single combined almanac. The printer, who is notoriously impatient and who has the presses standing "
          "idle, demands a single chain, ordered by ascending hour, formed by re-linking the existing entries; "
          "no new entry may be created, since the type has already been set for each entry individually and "
          "setting a fresh one would mean a fresh plate and a fresh bill.\n\n"
          "If two entries share the same hour, either may come first; the Admiralty has ruled on the point "
          "specifically, to the disappointment of both makers, each of whom had prepared an argument.\n\n"
          "The two makers have not spoken since a quarrel over a misprinted equinox. One of them keeps "
          "racing pigeons, and the Cambridge maker once compiled a table of eclipses that was wrong and has never quite lived it down. The Admiralty's representative is a retired commander who refers to both presses, in "
          "his letters, as the contractors, which neither of them has forgiven.\n\n"
          "Input: line one gives A and B, the lengths of the two chains. Line two gives A hours in ascending "
          "order; line three gives B hours in ascending order. Output: the combined chain's hours from its head, "
          "in non-decreasing order.\n\n"
          "Constraints: A and B up to 10^6; hours up to 10^9. The existing entries are to be re-linked; no new "
          "entry may be allocated.",
 "clues": ["each chain already ordered by ascending hour", "a single chain", "no new entry may be created"],
 "decoys": ["The printer, who is notoriously impatient",
            "The two makers have not spoken since a quarrel over a misprinted equinox",
            "One of them keeps racing pigeons"],
 "core": "Merge two sorted one-way chains into one by re-linking.",
 "gloss": [("almanac", "a yearly book of tide, weather and calendar facts", True),
           ("tide entries", "records of when the sea rises and falls", True),
           ("re-linking", "joining up again differently", True), ("equinox", "when day and night are equal length", True)],
 "why": {"tp-merge": "That merges arrays by position; chains are rewired, not indexed.",
         "hp-merge": "That handles many lists with a heap; two need only a front marker on each."},
 "tell": "Merge two sorted linked lists."},

{"id": "sc-047", "v": "td-up", "alt": ["tb-levels"], "dom": "empire", "diff": "E",
 "title": "The Ottoman Divan",
 "story": "The Divan of the Sublime Porte was the council through which the Ottoman state was governed, and its "
          "structure, as recorded in the registers of the chancery, was a strict hierarchy. The Grand Vizier "
          "stands at the top, and every official has at most two direct subordinates, a left and a right, the "
          "left being the senior by custom and the right the junior, a distinction that mattered enormously to "
          "the officials and not at all to anyone else.\n\n"
          "The sultan has conceived a suspicion about the length of his own chain of command. He has been told "
          "by the Grand Vizier that an order reaches the humblest clerk in four steps, and by a disaffected "
          "pasha that it reaches him in eleven. He therefore asks for the longest chain of command, counting the "
          "officials along it from the Grand Vizier down to the most junior official at the bottom of that "
          "chain, so that he may know which of the two men has been lying to him.\n\n"
          "The hierarchy is given level by level, with a dot for a missing subordinate, as the chancery's own "
          "registers set it out. The sultan wants the number of officials in that longest chain, not their "
          "names; he has made clear that names can wait until after the number.\n\n"
          "The Divan met in a chamber with a grilled window behind the throne through which the sultan could "
          "listen unseen, and everyone knew it. The chancery's seals were kept in a bag carried by an official "
          "whose sole duty that was. A pasha's dismissal was traditionally conveyed by a gift of a particular "
          "kind of robe, and the recipients learned to dread tailors.\n\n"
          "Input: line one gives N, the number of officials. Line two gives the hierarchy level by level from "
          "the Grand Vizier, with a dot for a missing subordinate. Output: the number of officials in the "
          "longest chain of command.\n\n"
          "Constraints: up to 10^5 officials.",
 "clues": ["at most two direct subordinates, a left and a right", "the longest chain of command",
           "from the Grand Vizier down to the most junior official"],
 "decoys": ["The Divan of the Sublime Porte was the council through which the Ottoman state was governed",
            "A pasha's dismissal was traditionally conveyed by a gift of a particular kind of robe",
            "The chancery's seals were kept in a bag carried by an official whose sole duty that was"],
 "core": "The height (number of levels) of a binary tree.",
 "gloss": [("Divan", "a council of state", True), ("vizier", "a high minister", True),
           ("hierarchy", "ranked levels of authority", True), ("subordinates", "people ranked beneath someone", True),
           ("chancery", "an office that keeps official records", True)],
 "why": {"tb-levels": "Counting levels by sweeping across each one also gives the height, a fair alternative.",
         "td-down": "That passes information from the root toward the leaves; here each official reports upward."},
 "tell": "Information flows up: an official's answer is built from the subordinates' answers."},

{"id": "sc-048", "v": "td-down", "dom": "caravan trade", "diff": "M",
 "title": "The Oasis Tolls",
 "story": "The caravan routes of the western desert were mapped in the ninth century by a geographer whose work "
          "survives in a single copy, and the map has an unusual property: a caravan route between oases forms a "
          "tree. From the first oasis, each oasis leads on to at most two further oases, a left road and a right "
          "road, and no road ever rejoins another, because the wells that make a route possible lie where they "
          "lie and the geographer recorded only the routes that water allows.\n\n"
          "Each oasis levies a toll on every caravan that halts there, the toll being set by whoever holds the "
          "well and varying from a few coins to an extortion. A journey runs from the first oasis down to a "
          "terminal oasis, one with no further roads, and the cost of a journey is the sum of the tolls at every "
          "oasis along it, the first and the terminal one included.\n\n"
          "The vizier, who is drafting a complaint to the caliph about the tolls and wants a figure in it, "
          "wishes to know how many such journeys have tolls totalling exactly T. He has chosen T because it is "
          "the sum a merchant petitioned him about last spring, and he wants to know whether that merchant's "
          "route was unusual or whether half the desert is paying the same. He does not want the routes "
          "themselves listed.\n\n"
          "The geographer's copy is in a library in Cairo and is not lent. One of the wells has been poisoned "
          "twice in living memory, each time during a succession dispute. A species of small fox at the "
          "fourth oasis is considered lucky and is fed by the caravaneers against the advice of everyone.\n\n"
          "Input: line one gives N and T. The next N lines each give an oasis's toll and the numbers of its left "
          "and right roads, 0 meaning none; oasis 1 is the first. Output: the number of journeys whose tolls "
          "total exactly T.\n\n"
          "Constraints: up to 10^5 oases; tolls between -1000 and 1000; T between -10^9 and 10^9.",
 "clues": ["from the first oasis down to a terminal oasis", "one with no further roads",
           "how many such journeys have tolls totalling exactly T"],
 "decoys": ["The caravan routes of the western desert were mapped in the ninth century",
            "A species of small fox at the fourth oasis is considered lucky",
            "One of the wells has been poisoned twice in living memory"],
 "core": "Count root-to-leaf paths whose values add up to a target.",
 "gloss": [("levies", "charges", True), ("terminal", "at the very end", True), ("toll", "a fee for passing", True),
           ("vizier", "a high minister", True), ("caliph", "a Muslim ruler", True)],
 "why": {"td-up": "That builds an answer from the children's answers; here the running total travels down from above.",
         "ps-count": "That counts stretches of an array; this is a tree with a fixed start and a fixed kind of end."},
 "tell": "Root-to-leaf paths, with a running total carried downward."},

{"id": "sc-049", "v": "td-bst", "dom": "merchant league", "diff": "M",
 "title": "The Hanseatic Tally-House",
 "story": "The tally-house of the Hanse at Bergen is a timber building on the wharf that has burned down five "
          "times and been rebuilt five times to the same plan. Inside, merchants' ledgers hang from a frame in "
          "an arrangement that strikes every visitor as eccentric and that the clerks defend as the only "
          "sensible one: the left branch of any ledger holds only strictly smaller account numbers, and the "
          "right branch only strictly larger. No two accounts share a number, the league having been strict "
          "about that since a fraud in 1398.\n\n"
          "An auditor has come from Lubeck with instructions to report on the smaller accounts, the league "
          "suspecting that a number of dormant accounts are being used to move goods without duty. He wants the "
          "K-th smallest account number in the whole tally-house, without gathering and sorting every number "
          "first, since the ledgers are heavy, hang from hooks, and may not be taken down without the "
          "permission of the merchant whose account they record.\n\n"
          "He would also prefer to stop as soon as he has what he came for, rather than handle every ledger in "
          "the building, and he has been told that the arrangement of the frame already puts the accounts in "
          "their order if only he will read them in the right way.\n\n"
          "The tally-house smells of old parchment and cold tallow, and its clerks work by candlelight, which "
          "the league's own fire regulations forbid. The wharf's winch is operated by a horse that is older than "
          "two of the clerks. A dispute about the measure of a barrel has been running with the Norwegian crown "
          "for a decade.\n\n"
          "Input: line one gives N and K. The next N lines each give a ledger's account number and the numbers "
          "of its left and right branches, 0 meaning none; ledger 1 hangs at the top. Output: the K-th smallest "
          "account number.\n\n"
          "Constraints: up to 10^5 ledgers; 1 <= K <= N; account numbers up to 10^9. Memory may grow with the "
          "depth of the frame, not with N.",
 "clues": ["the left branch of any ledger holds only strictly smaller account numbers",
           "the right branch only strictly larger", "the K-th smallest account number"],
 "decoys": ["The tally-house of the Hanse at Bergen is a timber building on the wharf",
            "The wharf's winch is operated by a horse that is older than two of the clerks",
            "A dispute about the measure of a barrel has been running with the Norwegian crown"],
 "core": "The K-th smallest value in a tree where everything on the left is smaller and everything on the right is larger.",
 "gloss": [("Hanse", "the medieval north-German trading league", True), ("ledger", "an official book of accounts", True),
           ("auditor", "someone who checks accounts", True), ("tallow", "animal fat used for candles", True),
           ("dormant", "inactive", True)],
 "why": {"hp-topk": "A heap would work but ignores the order the tree already gives you.",
         "tb-levels": "Level order does not follow the sorted order."},
 "tell": "The order is built into the tree; walk it in order."},

{"id": "sc-050", "v": "td-lca", "dom": "genealogy", "diff": "M",
 "title": "The Medici Descent",
 "story": "The Medici archive in Florence holds the family's own record of itself, and the record is recorded as "
          "a tree of descent in which each person has at most two recorded children. The archive is candid that "
          "the tree is a simplification: children who died young were often left out, and at least one line was "
          "removed on the instructions of a cardinal. What survives, though, is consistent, and all names in it "
          "are distinct, the family having numbered its repeated Christian names with a care that modern "
          "genealogists are grateful for.\n\n"
          "A genealogist working on a question of inheritance has two distinct individuals, A and B, both of "
          "whom appear in the tree. She wishes to name their nearest shared ancestor, that is, the deepest "
          "person from whom both descend, and a person counts as descending from themselves, so that if one of "
          "the two is an ancestor of the other then that one is the answer. The question matters because a "
          "bequest made in 1537 passes to the descendants of whoever that person turns out to be, and a bank in "
          "Milan has been holding the money ever since.\n\n"
          "She must answer many such questions, a pair at a time, as the lawyers work through the claimants, and "
          "the tree runs deep and is in places little more than a long thin line of fathers and sons, so "
          "climbing one step at a time from each of the two people would be slow where it matters most.\n\n"
          "The portraits in the gallery, it is said, never agree on anyone's nose. A forged codicil of 1604 is "
          "itself now a valuable document. The archive's reading room allows pencils only, and the genealogist "
          "has had two confiscated.\n\n"
          "Input: line one gives N and Q. The next N lines give each person's two children, 0 for none; person "
          "1 is at the top. The next Q lines each give two person numbers. Output: for each pair, the number of "
          "their nearest shared ancestor.\n\n"
          "Constraints: up to 10^5 people; Q up to 10^5.",
 "clues": ["nearest shared ancestor", "the deepest person from whom both descend",
           "a person counts as descending from themselves"],
 "decoys": ["The Medici archive in Florence holds the family's own record of itself",
            "The portraits in the gallery, it is said, never agree on anyone's nose",
            "A forged codicil of 1604 is itself now a valuable document"],
 "core": "The lowest common ancestor of two nodes in a tree.",
 "gloss": [("genealogist", "a student of family histories", True), ("descent", "the line of a family through time", True),
           ("ancestor", "an earlier relative", True), ("codicil", "an addition to a will", True),
           ("bequest", "something left in a will", True)],
 "why": {"td-up": "A close relative: the answer comes from the subtrees, but the split point is what you report.",
         "gr-bfs": "That finds a shortest route; here you want the meeting point above both."},
 "tell": "The deepest node that sits above both given nodes."},

{"id": "sc-051", "v": "tb-levels", "dom": "insurance", "diff": "E",
 "title": "The Syndicate Floors",
 "story": "A Lloyd's underwriting syndicate is a curious institution: a group of people who have agreed to lose "
          "money together in an orderly fashion, organised in a hierarchy that the Corporation requires to be "
          "documented. The organisation chart of one such syndicate is a tree: the chairman at the top, and "
          "every member having at most two direct reports, an arrangement that arose from a merger and that "
          "nobody has since had the authority to tidy.\n\n"
          "For the annual dinner the secretary seats the syndicate floor by floor of the hierarchy, a practice "
          "begun in the nineteen-fifties on the theory that it encourages promotion and continued because any "
          "change to it would require a vote. She wants a list of the members at each floor, from the top floor "
          "downward, in left-to-right order within a floor, so that the caterers can be given a seating plan "
          "and the chairman can be told who he will be sitting with before he finds out at the table.\n\n"
          "The chart is supplied to her as the Corporation holds it, with each member's two reports named, and "
          "it runs to as many as 10^5 members across the syndicate's several classes of business.\n\n"
          "The dinner is to be held in a draughty hall by the river, and the secretary is anxious about the "
          "soup. A member who resigned in 1998 still receives an invitation every year through an error nobody "
          "can trace. The syndicate's lucky mascot is a stuffed badger that is brought out at the dinner and "
          "returned to a cupboard the following morning.\n\n"
          "Input: line one gives N. The next N lines give each member's two direct reports, 0 for none; member 1 "
          "is the chairman. Output: one line per floor, from the top downward, listing that floor's members "
          "left to right.\n\n"
          "Constraints: up to 10^5 members.",
 "clues": ["floor by floor of the hierarchy", "the members at each floor, from the top floor downward",
           "left-to-right order within a floor"],
 "decoys": ["For the annual dinner the secretary seats the syndicate",
            "A member who resigned in 1998 still receives an invitation every year",
            "The syndicate's lucky mascot is a stuffed badger"],
 "core": "List the nodes of a tree level by level.",
 "gloss": [("syndicate", "a group that shares a business risk", True), ("underwriting", "insuring against risk", True),
           ("hierarchy", "ranked levels of authority", True), ("Corporation", "here, the body that governs Lloyd's", True)],
 "why": {"td-down": "That carries a running value along root-to-leaf paths; here you group by depth."},
 "tell": "Group the tree by level."},

{"id": "sc-052", "v": "tr-basic", "dom": "linguistics", "diff": "M",
 "title": "The Basque Dictionary",
 "story": "Basque is unrelated to any living language, and the standard dictionary of it has been compiled over "
          "four decades by a team at the university in Bilbao who are not, among themselves, in complete "
          "agreement about anything. The dictionary is kept as a tree in which each branch is a letter, so that "
          "every stored word is spelt out along a path from the top, a structure the team adopted because Basque "
          "builds long words from shorter ones and the shared beginnings would otherwise be written out "
          "thousands of times over.\n\n"
          "The compiler must support two actions on a very large word list. The first is asking whether a word "
          "is stored in full, which the editors need when they are deciding whether a form they have found in "
          "the field is already recorded. The second is asking whether ANY stored word begins with a given "
          "prefix, which the typesetters need, because the dictionary is printed in fascicles and a fascicle "
          "must not begin in the middle of nothing.\n\n"
          "Every question must be answered in time proportional to the length of the question word alone, not "
          "the number of stored words, a requirement that came from the team's computing officer after an "
          "unfortunate demonstration to the university's funding committee.\n\n"
          "A dictionary of the Basque language published in 1745 is still cited, mostly to be disagreed with. "
          "The team's coffee machine is the subject of a rota that nobody honours. One member has not spoken to "
          "another since a conference in Vitoria, and the two now communicate through a third who finds the "
          "arrangement entertaining.\n\n"
          "Input: line one gives Q. Each of the next Q lines gives an action: 1 and a word to store, 2 and a "
          "word to look up in full, or 3 and a prefix. Output: for each action of type 2 or 3, YES or NO.\n\n"
          "Constraints: Q up to 5*10^5; total length of all words and prefixes up to 5*10^6; lowercase letters "
          "only.",
 "clues": ["each branch is a letter", "ANY stored word begins with a given prefix",
           "proportional to the length of the question word alone"],
 "decoys": ["A dictionary of the Basque language published in 1745 is still cited",
            "The team's coffee machine is the subject of a rota that nobody honours",
            "One member has not spoken to another since a conference in Vitoria"],
 "core": "Store many words so that 'is this word stored?' and 'does any word start with this?' cost only the length of the question.",
 "gloss": [("compiler", "here, the person who assembles a dictionary", True), ("prefix", "the opening letters of a word", True),
           ("spelt", "written out letter by letter", True), ("fascicles", "instalments of a book published separately", True)],
 "why": {"hs-seen": "A set answers whole-word questions but cannot answer 'does any word begin with this'.",
         "tr-search": "That prunes a grid search using the dictionary; nothing is searched here."},
 "tell": "Prefix questions on a big word list."},
]
