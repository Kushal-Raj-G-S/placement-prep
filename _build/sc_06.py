# -*- coding: utf-8 -*-
"""Scenario questions, batch 6: dynamic programming (rest), backtracking, greedy.

OA-size stories (around 400 words) with their own Input / Output / Constraints lines. The answer keys
(v, alt, core, why, tell) are the originals.
"""

QUESTIONS = [

{"id": "sc-066", "v": "dp-kadane", "alt": ["ps-range"], "dom": "glassmaking", "diff": "M",
 "title": "The Murano Furnace",
 "story": "The glassworks of Murano were confined to the island by a decree of 1291, partly to keep their fires "
          "away from the city's timber and partly to keep their secrets away from everybody. The reckoner of one "
          "such glassworks records, for each of N consecutive days, the net profit or loss of the furnace, a "
          "single figure per day entered into the ledger in the order the days fell, so some entries are "
          "negative: a day on which the furnace was relit after a cooling, or a day on which a batch came out "
          "clouded, costs more than it earns.\n\n"
          "The doge's treasurer, who oversees the island's privileges and is looking for something cheerful to "
          "report to the Senate, wishes to commend the most profitable unbroken stretch of days, that is, the "
          "stretch whose entries add to the greatest possible total. The stretch must contain at least one day, "
          "and it must be unbroken: he will not accept a figure assembled from good days scattered through a bad "
          "season, since the point of the commendation is to praise a period of work and not a selection of "
          "lucky mornings.\n\n"
          "He wants the total alone. Which days they were can be established afterwards, and in any case the "
          "treasurer has learned that naming the days invites argument from whichever master was on the "
          "furnace. If every day of the record lost money, he must still commend something, and the stretch will "
          "be the single least bad day.\n\n"
          "Gondoliers ferry the ledgers to the treasury each evening. The works' own cat is said to be "
          "descended from one brought from Alexandria. A master glassblower defected to France in the "
          "seventeenth century and his family was, by the custom of the time, extremely unlucky.\n\n"
          "Input: line one gives N. Line two gives the N daily figures in order. Output: the greatest total of "
          "any unbroken stretch of days.\n\n"
          "Constraints: N up to 10^6; each figure between -10^9 and 10^9; the answer may need a 64-bit integer.",
 "clues": ["some entries are negative", "the most profitable unbroken stretch of days",
           "must contain at least one day"],
 "decoys": ["Gondoliers ferry the ledgers to the treasury each evening",
            "The works' own cat is said to be descended from one brought from Alexandria",
            "A master glassblower defected to France in the seventeenth century"],
 "core": "The largest total of any unbroken stretch of a list that can contain negative numbers.",
 "gloss": [("reckoner", "a person who calculates", True), ("commend", "to praise", True),
           ("treasurer", "an official in charge of money", True),
           ("furnace", "an oven for melting glass or metal", True), ("decree", "an official order", True)],
 "why": {"ps-longest": "That wants the longest stretch hitting a target total; here you want the best total.",
         "sw-longest": "A moving stretch needs totals that only grow; negatives break it.",
         "ps-range": "Prefix totals minus the smallest earlier prefix also give the answer, a fair alternative."},
 "tell": "The best unbroken stretch total, with negatives present."},

{"id": "sc-067", "v": "dp-coin", "dom": "moneychanging", "diff": "M",
 "title": "The Ragusa Moneychanger",
 "story": "Ragusa kept its independence for six hundred years by paying tribute to whoever was strongest, and "
          "its moneychangers consequently handled more currencies than any city of its size. A moneychanger on "
          "the Placa holds coins of D distinct denominations and has an unlimited supply of each, his stock "
          "being replenished from the republic's own mint and from the Turkish trade.\n\n"
          "A customer, a ship's master settling a crew's wages before sailing, needs to be paid exactly A "
          "florins, neither more nor less, since the sum is fixed by the articles and the master will not carry "
          "a surplus coin back aboard. The moneychanger, anxious to keep his strongbox light and his counting "
          "quick, wants to pay with as few coins as possible.\n\n"
          "Taking the largest coin that fits at every step, he has discovered, does not always give the fewest. "
          "The republic's own coinage is to blame: it includes an awkward piece of twelve florins struck for a "
          "jubilee, and with coins of one, five and twelve a sum of fifteen is paid with three fives, whereas "
          "the twelve leads to four coins. He learned this at some cost and no longer trusts the obvious "
          "method. Report the least number of coins, or -1 if the sum cannot be made.\n\n"
          "The Placa is paved with limestone polished by five centuries of feet. The republic abolished the "
          "slave trade in 1416, a fact the moneychanger mentions to foreigners. A Jesuit college in the city taught "
          "mathematics to the sons of merchants, and he attended it for two years before his father died. His scales "
          "were made in Venice, "
          "which he does not mention to anybody.\n\n"
          "Input: line one gives D and A. Line two gives the D denominations. Output: the least number of coins "
          "totalling exactly A, or -1.\n\n"
          "Constraints: D up to 12; A up to 10^4; each denomination between 1 and 10^4.",
 "clues": ["an unlimited supply of each", "exactly A florins", "as few coins as possible",
           "does not always give the fewest"],
 "decoys": ["A moneychanger on the Placa", "The republic abolished the slave trade in 1416",
            "The Placa is paved with limestone polished by five centuries of feet"],
 "core": "The fewest items, each usable any number of times, that add to an exact target.",
 "gloss": [("moneychanger", "someone who exchanges one currency for another", True),
           ("denominations", "the different values of coins", True), ("florins", "old gold coins", True),
           ("strongbox", "a sturdy box for valuables", True), ("jubilee", "a special anniversary", True)],
 "why": {"gr-local": "Taking the biggest coin first is exactly the trap the story warns about.",
         "dp-knapsack": "That allows each item once; here every denomination is unlimited."},
 "tell": "Unlimited items, an exact target, and the fewest items."},

{"id": "sc-068", "v": "dp-lis", "dom": "lighthouses", "diff": "M",
 "title": "The Lisbon Lanterns",
 "story": "The lighthouse at Belem watches the mouth of the Tejo, and its keeper has kept a private record for "
          "thirty years that has no official standing whatever. He notes the brightness of N passing ships' "
          "lanterns in the order they appear on the horizon, a number for each, judged by eye against a scale he "
          "devised himself and which he is confident is consistent.\n\n"
          "A lantern-spotter from the maritime museum has taken an interest in the record, for reasons connected "
          "with a theory about the refitting of the Brazil fleet. She wants to choose some of the lanterns, "
          "keeping the order in which they appeared, such that each chosen lantern is strictly brighter than the "
          "one chosen before it. The choices need not be adjacent in the sequence: she may skip over any number "
          "of lanterns, however many, so long as the ones she keeps are in their original order and climbing in "
          "brightness.\n\n"
          "The spotter wants the greatest number of lanterns that can be chosen this way. She does not want to "
          "know which lanterns they were, nor how many such choices there are; the length of the longest "
          "possible run of choices is the figure her theory turns on, and she has promised it to a journal by "
          "the end of the month.\n\n"
          "The keeper's record is written in three different inks because of a shortage in the nineteen-nineties. "
          "The lighthouse's lamp was converted to electricity in 1949 against the keeper's father's advice. A "
          "cormorant roosts on the gallery rail and is photographed by everyone who visits.\n\n"
          "Input: line one gives N. Line two gives the N brightness values in the order they appeared. Output: "
          "the greatest number of lanterns that can be chosen in order with strictly increasing brightness.\n\n"
          "Constraints: N up to 2500; brightness values up to 10^9.",
 "clues": ["keeping the order in which they appeared", "strictly brighter than the one chosen before it",
           "need not be adjacent in the sequence", "N up to 2500"],
 "decoys": ["He notes the brightness of N passing ships", "A cormorant roosts on the gallery rail",
            "The keeper's record is written in three different inks"],
 "core": "The longest strictly increasing subsequence of a list.",
 "gloss": [("lantern", "a portable light", True), ("horizon", "the line where sea meets sky", True),
           ("strictly", "not merely equal", True), ("spotter", "someone who watches for things", True),
           ("refitting", "repairing and re-equipping a ship", True)],
 "why": {"sw-longest": "A moving stretch needs unbroken runs; these choices are scattered.",
         "dp-kadane": "That adds values along a stretch; here you count the length of a chain."},
 "tell": "The longest increasing chain, with choices that need not be adjacent."},

{"id": "sc-069", "v": "dp-grid", "alt": ["sp-dijkstra"], "dom": "highland trade", "diff": "M",
 "title": "The Salt Plateau",
 "story": "The Salar de Uyuni is the largest salt flat on earth and in the dry season it is crossed by traders "
          "who have no particular interest in its being the largest anything. A mule-driver crossing a salt "
          "plateau in Bolivia faces a rectangular grid of R rows by C columns of salt flats, the grid being the "
          "customs authority's own division of the crossing for the purpose of levying its dues; entering a flat "
          "costs the driver the number of coins printed on it, a digit from 0 to 9, payable at the hut on the far "
          "side where the tally is read off his permit.\n\n"
          "He starts at the top-left flat and must reach the bottom-right flat. The mule will only step one flat "
          "to the right or one flat down, never up or left, not from obstinacy but because the ridges of dried "
          "salt run in those two directions and an animal that crosses them obliquely cuts its feet. The driver "
          "pays for every flat he stands in, including the first and the last.\n\n"
          "The driver wishes to pay the least total of coins along his route. He does not care how many flats "
          "the route covers, which is in any case the same whichever way he goes, nor how long it takes; only "
          "the total of the coins.\n\n"
          "The sun is merciless and the mule is sulking. A railway cemetery outside Uyuni is visited by "
          "travellers who photograph the rusting engines. The customs hut has a radio that receives one station "
          "and a dog that receives everybody.\n\n"
          "Input: line one gives R and C. The next R lines each give C digits. Output: the least total of coins "
          "on any route from the top-left flat to the bottom-right flat moving only right or down.\n\n"
          "Constraints: R and C up to 1000.",
 "clues": ["only step one flat to the right or one flat down", "never up or left",
           "the least total of coins along his route"],
 "decoys": ["The sun is merciless and the mule is sulking",
            "A railway cemetery outside Uyuni is visited by travellers who photograph the rusting engines",
            "The customs hut has a radio that receives one station"],
 "core": "The cheapest path across a grid when you can only move right or down.",
 "gloss": [("plateau", "a high flat area of land", True), ("flats", "here, the squares of the grid", True),
           ("merciless", "showing no pity", True), ("obliquely", "at a slant", True),
           ("dues", "fees owed", True)],
 "why": {"gr-bfs": "That counts steps with all four directions allowed; here costs differ and movement is restricted.",
         "sp-dijkstra": "A fair general tool, but the one-way movement lets a simple table do the job."},
 "tell": "A grid, moves limited to right and down, minimise the cost."},

{"id": "sc-070", "v": "dp-twostring", "dom": "philology", "diff": "H",
 "title": "The Lost Manuscript",
 "story": "The Codex Argenteus was divided in the sixteenth century and its leaves are now scattered across "
          "Europe, which is why the study of it is conducted by correspondence between people who disagree. Two "
          "philologists, one in Leiden and one in Uppsala, each hold a medieval word copied from the same lost "
          "manuscript, copied with scribal slips: letters may have been dropped, but those that remain are in "
          "their original order, since a scribe who skips a letter does not thereby rearrange the others.\n\n"
          "The two words therefore differ, and the question between the scholars is how much of the original can "
          "be recovered with confidence. They wish to know the greatest number of letters that appear in BOTH "
          "words in the same relative order, though not necessarily side by side in either, since a letter lost "
          "from one copy leaves a gap in that copy and not in the other. Report that number.\n\n"
          "Each has separately proposed a method and each has rejected the other's. The Leiden scholar's first "
          "attempt was to compare the two words position by position and count the matches, which gave an absurd "
          "answer as soon as a letter was missing early on, because everything after it was shifted by one. The "
          "Uppsala scholar proposed trying every way of deleting letters from each word, and has not finished.\n\n"
          "The codex is written in silver ink on purple vellum, which is why it has a name at all. A leaf "
          "surfaced in Speyer in 1970 inside a reliquary. The two scholars have met once, at a conference in "
          "Ghent, and the meeting is described differently by each of them.\n\n"
          "Input: line one gives the lengths N and M. Line two gives the Leiden word, line three the Uppsala "
          "word, both in lowercase letters. Output: the greatest number of letters common to both in the same "
          "relative order.\n\n"
          "Constraints: each word up to 3000 letters.",
 "clues": ["letters may have been dropped", "in the same relative order",
           "not necessarily side by side in either"],
 "decoys": ["one in Leiden and one in Uppsala", "A leaf surfaced in Speyer in 1970 inside a reliquary",
            "The codex is written in silver ink on purple vellum"],
 "core": "The longest sequence of letters appearing in both of two strings in the same order.",
 "gloss": [("philologists", "scholars of languages", True), ("manuscript", "a hand-written document", True),
           ("scribal", "of a copyist", True), ("slips", "small mistakes", True),
           ("reliquary", "a container for holy relics", True)],
 "why": {"sw-longest": "That finds a stretch inside ONE string; here letters need not be adjacent and there are two strings.",
         "dp-lis": "That compares values within one sequence."},
 "tell": "Two strings compared; shared letters keep their order but are not adjacent."},

{"id": "sc-071", "v": "dp-knapsack", "dom": "ancient armies", "diff": "M",
 "title": "The Centurion's Cart",
 "story": "The Ninth Legion is moving north from Eboracum, and a centurion named Lucius Vibenna has been given "
          "a single mule cart and a depot full of supplies, which is the kind of arithmetic problem the army "
          "produced in quantity and recorded on wax. He loads the cart with a choice from N bales of supplies, "
          "bale i weighing w[i] pounds, the bales being already made up and corded by the quartermaster.\n\n"
          "The cart can bear at most W pounds before its axle breaks, a figure the wheelwright has given him "
          "with some emphasis, having replaced two axles that month. Each bale can be loaded once or left "
          "behind; bales cannot be split, since a bale cut open is a bale spoiled by the first rain and the "
          "quartermaster has a temper.\n\n"
          "The centurion wishes to load as much total weight as possible without exceeding W, and reports that "
          "weight to the quartermaster, who will then decide which bales those are. He is not choosing by what "
          "the bales contain: the army's view, which he has learned not to question, is that a pound of "
          "anything is a pound of supply. He simply wants the cart as full as it can be.\n\n"
          "The legionaries mutter about the rations. A standard-bearer has lost a boss from his shield and has "
          "been fined for it. The depot's wax tablets are reused until the wax will take no more, and a clerk has "
          "been reprimanded for scraping one that was still wanted. The cart's near-side wheel was made from "
          "green timber by a contractor who is no "
          "longer employed, and it has been described, in a report, as a disgrace.\n\n"
          "Input: line one gives N and W. Line two gives the N bale weights. Output: the greatest total weight "
          "that can be loaded without exceeding W.\n\n"
          "Constraints: N up to 100; W up to 5000; each weight up to W.",
 "clues": ["loaded once or left behind", "bales cannot be split",
           "as much total weight as possible without exceeding W"],
 "decoys": ["The legionaries mutter about the rations",
            "A standard-bearer has lost a boss from his shield and has been fined for it",
            "The cart's near-side wheel was made from green timber"],
 "core": "Pick items, each at most once, to get as close as possible to a limit without exceeding it.",
 "gloss": [("centurion", "an officer of a Roman legion", True), ("bales", "large tied bundles", True),
           ("axle", "the rod a wheel turns on", True), ("legionaries", "soldiers of a Roman legion", True),
           ("quartermaster", "the officer in charge of supplies", True)],
 "why": {"dp-coin": "That allows unlimited copies of each denomination; here each bale is used at most once.",
         "gr-pair": "Pairing by size cannot choose an arbitrary subset."},
 "tell": "Each item once, against a capacity."},

{"id": "sc-072", "v": "dp-interval", "dom": "fireworks", "diff": "H",
 "title": "The Nagoya Fireworks",
 "story": "The fireworks of Nagoya are judged, and the judging has rules that the masters themselves helped to "
          "write, which is why they are strange. A fireworks-master has a row of N crackers, cracker i with "
          "brilliance b[i], mounted on a frame in a fixed order that may not be altered once the frame is "
          "set.\n\n"
          "He fires one cracker at a time. Firing cracker i earns b[left] x b[i] x b[right] points, where left "
          "and right are its neighbours still unfired at that moment, and a missing neighbour counts as "
          "brilliance 1, which is how the rule treats the two ends of the frame. Once fired, a cracker vanishes "
          "and its neighbours become adjacent, so that a cracker which began in the middle of the row may end up "
          "beside one that began far from it.\n\n"
          "He may choose any order of firing, and wishes the greatest total points once every cracker is fired. "
          "Every cracker must be fired; he may not leave one on the frame. The master has observed that firing "
          "the brightest cracker first is not obviously right, since a bright cracker left standing multiplies "
          "its neighbours' scores, and that trying every order of firing is out of the question for a frame of "
          "any size.\n\n"
          "The frame itself is of bamboo lashed with cord, built the same way for two hundred years, and the master "
          "has refused three offers of a steel one. The festival's crowd is estimated at four hundred thousand "
          "and the river bank is closed to traffic. A "
          "rival house in Osaka uses a shell of its own design which the Nagoya masters consider vulgar. The "
          "master's apprentice has burned his hand twice and will not be told.\n\n"
          "Input: line one gives N. Line two gives the N brilliance values in frame order. Output: the greatest "
          "total points obtainable.\n\n"
          "Constraints: N up to 100; each brilliance up to 100.",
 "clues": ["Firing cracker i earns b[left] x b[i] x b[right] points",
           "neighbours still unfired at that moment", "any order of firing"],
 "decoys": ["A fireworks-master has a row of N crackers",
            "A rival house in Osaka uses a shell of its own design which the Nagoya masters consider vulgar",
            "The master's apprentice has burned his hand twice"],
 "core": "Remove items one at a time in the best order, where each removal's reward depends on the neighbours still present.",
 "gloss": [("brilliance", "brightness", True), ("vanishes", "disappears", True),
           ("adjacent", "next to each other", True), ("vulgar", "lacking taste", True)],
 "why": {"dp-linear": "That chooses items along a line with a fixed rule; here the order of removal changes every later reward.",
         "bk-perms": "Trying every order is factorial; thinking about the LAST item removed in a range splits the problem."},
 "tell": "The reward depends on what is still present: think about the last item removed in a range."},

{"id": "sc-073", "v": "bk-subsets", "alt": ["bt-subsets"], "dom": "patisserie", "diff": "M",
 "title": "The Viennese Menu Card",
 "story": "Demel's has supplied the imperial court and then, after the court ceased to exist, everybody else, "
          "and its pastry-chef guards a shelf of flavourings that is the subject of some mythology among the "
          "staff. The chef has N jars of flavourings, some of which share the same flavour code, because the "
          "shelf has been stocked over many years and three different suppliers have delivered what turned out "
          "to be the same vanilla.\n\n"
          "For the spring card he wishes to print a menu card of every distinct combination of jars he could "
          "pick, including picking none, which he intends to print as a line reading 'plain' and which the "
          "manager has already objected to. Two combinations are the same if they use the same flavour codes the "
          "same number of times, regardless of which jars are chosen, so two combinations that differ only in "
          "which of the three vanilla jars was reached for are one combination as far as the card is concerned. "
          "Each combination must be printed once.\n\n"
          "The chef wants the combinations themselves, written out, not a count of them; the card is the point, "
          "and the printer needs the lines. With N at most 15 the card will be long but, he insists, not absurd, "
          "and he has pointed out that the cafe's wine list is longer.\n\n"
          "The cafe's chandeliers are polished every Sunday. The waiters are famously rude and the rudeness is "
          "now a protected tradition. A marble table is reserved every Thursday for a man who has been dead "
          "since 2011, an arrangement his family pays for.\n\n"
          "Input: line one gives N. Line two gives the N flavour codes. Output: every distinct combination, one "
          "per line, codes within a line in non-decreasing order; an empty combination is printed as a blank "
          "line.\n\n"
          "Constraints: N up to 15; flavour codes up to 100.",
 "clues": ["every distinct combination of jars he could pick", "including picking none",
           "regardless of which jars are chosen", "N at most 15"],
 "decoys": ["The cafe's chandeliers are polished every Sunday",
            "The waiters are famously rude and the rudeness is now a protected tradition",
            "A marble table is reserved every Thursday for a man who has been dead since 2011"],
 "core": "List every distinct subset of a collection that may contain repeated values.",
 "gloss": [("pastry-chef", "a cook who makes cakes and pastries", True),
           ("flavourings", "substances that add taste", True),
           ("combination", "a particular selection of items", True), ("mythology", "a body of stories", True)],
 "why": {"dp-knapsack": "That counts or optimises; here every combination must be listed.",
         "bt-subsets": "A fair alternative: a bit mask over all selections, then removing repeats."},
 "tell": "List ALL selections (N small, with repeats), not just count them."},

{"id": "sc-074", "v": "bk-perms", "dom": "stage lighting", "diff": "M",
 "title": "The Salzburg Light Bar",
 "story": "The Festspielhaus at Salzburg has a lighting department whose head technician has outlasted four "
          "artistic directors and intends to outlast a fifth. He has N coloured lamps in a row on a bar above "
          "the forestage, some lamps sharing the same colour, because the stock of gels is what it is and the "
          "budget for this production was spent on a revolve.\n\n"
          "A director has asked to see the possibilities. Each evening before the technical rehearsal the "
          "technician wishes to try every distinct order in which the colours can be arranged along the bar, "
          "recording each arrangement once, since two arrangements are the same if they show the same colours in "
          "the same positions; swapping two lamps of the same colour changes nothing that anybody in the "
          "auditorium can see, and the technician has no intention of climbing the ladder to prove it twice.\n\n"
          "He needs the full list of arrangements, written out, so that the director can be walked through them "
          "and will then choose the one she first described. With N at most 8 the list is long but finite, which "
          "is more than can be said for the director's notes.\n\n"
          "The theatre's chandelier hangs overhead and the pit is dark. A revolve installed for this production has "
          "jammed once in rehearsal and the stage manager has stopped mentioning it. A stage weight fell from the grid in "
          "1987 and the resulting procedure is now three pages long. The technician keeps a bottle of something "
          "in the dimmer room, which everyone knows about and nobody mentions, including the technician.\n\n"
          "Input: line one gives N. Line two gives the N colours as letters, in their current order on the bar. "
          "Output: every distinct arrangement, one per line, in any order of listing.\n\n"
          "Constraints: N at most 8; colours are lowercase letters.",
 "clues": ["every distinct order in which the colours can be arranged", "recording each arrangement once",
           "N at most 8"],
 "decoys": ["The theatre's chandelier hangs overhead and the pit is dark",
            "A stage weight fell from the grid in 1987",
            "The technician keeps a bottle of something in the dimmer room"],
 "core": "List every distinct ordering of a collection that may contain repeated items.",
 "gloss": [("technician", "a skilled worker with equipment", True),
           ("arrangement", "a particular order or layout", True), ("bar", "the rail the lamps hang from", True),
           ("gels", "coloured filters put over stage lights", True), ("forestage", "the front part of a stage", True)],
 "why": {"bk-subsets": "That lists selections where order does not matter; here the positions matter.",
         "dp-lis": "Nothing here is about a longest chain."},
 "tell": "ORDER matters, N is tiny, and repeats must not be repeated."},

{"id": "sc-075", "v": "bk-board", "dom": "palaces", "diff": "H",
 "title": "The Hall of Mirrors",
 "story": "The hall of mirrors at Versailles is seventy-three metres long and was designed to be walked through "
          "rather than guarded, a fact that has caused the king's household some difficulty. The hall has a "
          "square floor of N by N tiles, and the king's guards, N in number, are to be posted on distinct tiles "
          "by order of the steward of the household.\n\n"
          "The difficulty is the mirrors. A guard watches along its whole row, its whole column, and both "
          "diagonals through its tile, because the glass carries his line of sight the length of the hall and "
          "across it, and the household's standing order is that no guard may be on a tile watched by another: "
          "two guards who can see one another are two guards who will talk, and a guard who is talking is not "
          "watching the door.\n\n"
          "The steward wishes to know in how many different ways the N guards can be posted so that none watches "
          "another. The guards are interchangeable, so two postings differ only in which tiles are occupied. He "
          "does not want the postings listed, only counted, and he has established already that for some small "
          "halls the answer is none at all.\n\n"
          "The steward's own office is a windowless room off the north wing, and he has asked twice for a stove. "
          "The hall's mirrors were a deliberate display of wealth, glass of that size being then a Venetian "
          "monopoly. A courtier's wig caught fire from a candle sconce in 1745, after which the household "
          "required the sconces to be set higher, a change that made the hall darker and nobody happier. "
          "The parquet is polished by men "
          "wearing felt overshoes, and the household accounts for the felt separately.\n\n"
          "Input: a single integer N. Output: the number of distinct postings in which no guard watches "
          "another.\n\n"
          "Constraints: N up to 9.",
 "clues": ["watches along its whole row, its whole column, and both diagonals",
           "no guard may be on a tile watched by another", "N up to 9"],
 "decoys": ["The hall of mirrors at Versailles is seventy-three metres long",
            "A courtier's wig caught fire from a candle sconce in 1745",
            "The parquet is polished by men wearing felt overshoes"],
 "core": "Count the ways to place N non-attacking pieces on an N by N board.",
 "gloss": [("steward", "an official who manages a household", True), ("posted", "stationed at a place", True),
           ("diagonals", "slanting lines across the floor", True), ("sconce", "a bracket holding a candle", True),
           ("parquet", "a floor of patterned wooden blocks", True)],
 "why": {"bt-dp": "A fair relative: bit masks track attacked columns and diagonals.",
         "gr-flood": "Nothing here is about connected regions."},
 "tell": "Place pieces on a board with attack lines: place, test, undo."},

{"id": "sc-076", "v": "gr-reach", "dom": "river crossings", "diff": "M",
 "title": "The Neva Stepping Stones",
 "story": "Before the bridges, the Neva was crossed in summer by ferry and in winter on the ice, and in the "
          "weeks between by a line of stepping stones that the city laid and the spring flood took away again. A "
          "ferryman crosses the river by stepping stones numbered 0 to N-1 in a line; from stone i he can leap "
          "forward by at most a[i] stones, and may leap less, where a[i] is carved on the stone by the "
          "engineers who set it, according to how firm its footing is and how far the next ones lie.\n\n"
          "He starts on stone 0 and wishes to know whether he can ever reach stone N-1, which is the far bank. "
          "He may not leap backwards, there being no reason to and the current being what it is. If a stone has "
          "a[i] = 0 he cannot leave it, that stone having been set on mud and marked accordingly, and a ferryman "
          "who steps onto it is there until the water drops.\n\n"
          "He wants a yes or a no; the route itself, and how many leaps it takes, are matters for the day "
          "itself. He has noticed that what governs his progress is not any particular stone but how far along "
          "the line he could possibly have got by the time he reaches each one.\n\n"
          "The river is icy, and the ferryman is fond of singing. The engineers' numbers are repainted each "
          "spring by a man who also paints the railings. A stone near the middle has a crack that has been "
          "reported three times and is still a crack.\n\n"
          "Input: line one gives N. Line two gives the N leap limits a[0] to a[N-1]. Output: YES if stone N-1 "
          "can be reached from stone 0, NO otherwise.\n\n"
          "Constraints: N up to 10^6; each a[i] between 0 and 10^5.",
 "clues": ["by at most a[i] stones, and may leap less", "whether he can ever reach stone N-1",
           "how far along the line he could possibly have got"],
 "decoys": ["The river is icy, and the ferryman is fond of singing",
            "The engineers' numbers are repainted each spring by a man who also paints the railings",
            "A stone near the middle has a crack that has been reported three times"],
 "core": "Can you reach the last position if each position lets you jump up to a given distance?",
 "gloss": [("ferryman", "someone who carries people across water", True), ("leap", "a big jump", True),
           ("carved", "cut into a surface", True), ("footing", "a place to put your foot", True)],
 "why": {"dp-linear": "A table over positions also works but is slower; one number, how far you can get, is enough.",
         "gr-bfs": "Valid, but exploring every jump is far slower than tracking the furthest reach."},
 "tell": "Can I reach the end? Track the furthest reach."},

{"id": "sc-077", "v": "gr-pair", "alt": ["tp-ends"], "dom": "ferries", "diff": "M",
 "title": "The Bosphorus Crossing",
 "story": "The ferries of the Bosphorus have crossed between Europe and Asia since there were names for the two "
          "sides, and the company that runs them keeps a regulation book that is largely a record of past "
          "accidents. At the crossing, N travellers wait to be ferried, traveller i weighing w[i] okka, the "
          "weights having been taken at the gate because the regulation book requires it.\n\n"
          "Each ferry carries at most two travellers. This is not a matter of space but of the boats, which are "
          "small and old and which the harbour authority has restricted after an incident at Kandilli. The "
          "combined weight on any ferry may not exceed the limit L, and every traveller individually weighs no "
          "more than L, so nobody need be turned away; but two travellers who together exceed L must go "
          "separately.\n\n"
          "The ferry company wants the fewest ferry trips that carry everyone, since each trip costs fuel and a "
          "boatman's time and the fare is fixed by the municipality. It does not matter who travels with whom, "
          "and the travellers, who are mostly commuters, have no opinion so long as they cross.\n\n"
          "Gulls wheel overhead and a vendor sells roasted chestnuts, while the old ferries creak but carry on. "
          "The company's regulation book is kept in the Kadikoy office and is consulted chiefly when something "
          "has already gone wrong. "
          "A boatman has worked the crossing for fifty-one years and is pointed out to tourists. The "
          "municipality has proposed a bridge at this point four times and withdrawn the proposal four "
          "times.\n\n"
          "Input: line one gives N and L. Line two gives the N traveller weights, in the order they were taken "
          "at the gate. Output: the fewest ferry trips that carry every traveller.\n\n"
          "Constraints: N up to 10^5; each weight between 1 and L; L up to 10^9.",
 "clues": ["at most two travellers", "combined weight on any ferry may not exceed the limit L",
           "the fewest ferry trips"],
 "decoys": ["Gulls wheel overhead and a vendor sells roasted chestnuts",
            "A boatman has worked the crossing for fifty-one years and is pointed out to tourists",
            "The municipality has proposed a bridge at this point four times"],
 "core": "Pair items so each pair stays within a limit, using as few groups as possible.",
 "gloss": [("okka", "an old Ottoman unit of weight", True), ("ferried", "carried across water", True),
           ("travellers", "people on a journey", True), ("commuters", "people who travel daily to work", True)],
 "why": {"dp-knapsack": "That chooses a subset to fill a capacity; here every traveller must be carried, in pairs.",
         "tp-ends": "Two markers closing in is the mechanism; the decision they make is the greedy one."},
 "tell": "Sort, then pair the lightest with the heaviest."},

{"id": "sc-078", "v": "gr-local", "alt": ["hp-greedy"], "dom": "ceramics", "diff": "H",
 "title": "The Delft Kiln",
 "story": "Delftware is tin-glazed earthenware made in imitation of Chinese porcelain, and the guild that "
          "regulated its making was as particular about the firing as about the painting. A kiln master in Delft "
          "has N pottery batches to fire, each batch of a type marked by a letter, the type being the body and "
          "glaze recipe together. One batch is fired per hour-slot, the kiln holding exactly one batch at a "
          "time.\n\n"
          "By a rule of the guild, two batches of the same type must have at least K idle hour-slots between "
          "their firings, though other types may be fired in those slots. The reason given in the guild's own "
          "ordinance is that the kiln must cool and be re-set for a repeated recipe, and the master, who has "
          "lost a whole firing to a kiln that was still hot, does not dispute it. If nothing is permitted the "
          "kiln simply stands idle for that slot, which costs fuel and earns nothing.\n\n"
          "He wants the shortest total number of hour-slots in which every batch is fired, counting the idle "
          "slots, since the shed is hired by the day. He is free to fire the batches in any order he likes; the "
          "guild's rule is the only constraint, and the order in which the batches arrived at the shed is of no "
          "consequence.\n\n"
          "A kiln master in Delft was traditionally also the master painter, which this one is not, and the "
          "arrangement is the subject of comment. The town's canal is being dredged and the smell is "
          "remarkable. An English merchant has ordered a service of eighty pieces and changed the design "
          "twice.\n\n"
          "Input: line one gives N and K. Line two gives the N batch types as letters. Output: the shortest "
          "number of hour-slots needed to fire every batch.\n\n"
          "Constraints: N up to 10^5; K between 0 and 100; types are lowercase letters.",
 "clues": ["two batches of the same type must have at least K idle hour-slots between their firings",
           "the shortest total number of hour-slots", "free to fire the batches in any order he likes"],
 "decoys": ["A kiln master in Delft was traditionally also the master painter",
            "The town's canal is being dredged and the smell is remarkable",
            "An English merchant has ordered a service of eighty pieces and changed the design twice"],
 "core": "Schedule tasks with a cooling gap between repeats of the same type, minimising the total time.",
 "gloss": [("kiln", "an oven for firing pottery", True), ("batches", "groups made together", True),
           ("idle", "not working", True), ("firing", "baking clay in a kiln", True),
           ("ordinance", "a formal rule", True)],
 "why": {"hp-greedy": "A fair view of the same idea: a heap of what remains lets you always serve the most plentiful type.",
         "dp-linear": "A table over time is unnecessary; a locally best choice is provably safe here."},
 "tell": "Always serve the most frequent type that is off its cooldown."},
]
