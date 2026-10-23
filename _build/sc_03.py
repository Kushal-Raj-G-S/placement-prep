# -*- coding: utf-8 -*-
"""Scenario questions, batch 3: monotonic stack (rest), heap, intervals, bits (first).

OA-size stories (around 400 words) with their own Input / Output / Constraints lines. The answer keys
(v, alt, core, why, tell) are the originals.
"""

QUESTIONS = [

{"id": "sc-027", "v": "ms-hist", "dom": "signwriting", "diff": "H",
 "title": "The Antwerp Hoarding",
 "story": "The redevelopment of the Falconplein in Antwerp has been under way for four years and has reached the "
          "stage at which the hole in the ground must be hidden from the public. A hoarding contractor has "
          "erected N adjoining timber panels, each exactly one ell wide, panel i standing h[i] ells tall. The "
          "panels are of unequal height because they were salvaged from three previous jobs, and the contractor, "
          "a thrifty man named Lodewijk Verhoeven, sees no reason to cut good timber down to match bad.\n\n"
          "The guild of sign-painters will commission a single rectangular banner to hang on the hoarding, and "
          "the terms are strict. The banner must hang wholly upon the panels: it may span any unbroken run of "
          "them, from one panel to as many as the whole row, but it can rise no higher than the lowest panel in "
          "that run, since a banner that overtopped a panel would flap loose at that point and tear in the first "
          "wind off the Scheldt. The banner is a plain rectangle; it cannot be stepped or notched to follow the "
          "tops of the panels.\n\n"
          "The burgomaster, who must approve the commission, demands the greatest banner area obtainable, area "
          "being the number of panels spanned multiplied by the height in ells. He does not want to know where "
          "the banner will hang, only how large it can be, because the figure goes into a budget and the budget "
          "is already late.\n\n"
          "Verhoeven's foreman proposed trying every possible pair of end panels and looking along the run "
          "between them for the lowest, and gave up on the second afternoon. The hoarding has already been "
          "covered in posters for a punk concert, twice. A heron fishes in the flooded excavation and has "
          "acquired a following on the internet. The site's night watchman keeps a brazier and a radio.\n\n"
          "Input: line one gives N. Line two gives the N panel heights, left to right. Output: the greatest "
          "obtainable banner area.\n\n"
          "Constraints: N up to 10^5, h[i] up to 10^9; the answer may need a 64-bit integer.",
 "clues": ["wholly upon the panels", "no higher than the lowest panel in that run",
           "the greatest banner area obtainable"],
 "decoys": ["The guild of sign-painters will commission",
            "A heron fishes in the flooded excavation and has acquired a following on the internet",
            "The site's night watchman keeps a brazier and a radio"],
 "core": "The largest rectangle that fits entirely under a row of bars of different heights.",
 "gloss": [("hoarding", "a large board for advertisements", True), ("ell", "an old unit of length", True),
           ("burgomaster", "a town mayor", True), ("wholly", "completely", True),
           ("salvaged", "saved and reused", True)],
 "why": {"ms-next": "That gives a distance per bar; here you need how far each bar can extend on BOTH sides before a shorter one stops it.",
         "sw-longest": "A moving stretch obeys a fixed rule; the best banner may start and end anywhere, and its height is set by the lowest panel inside."},
 "tell": "The largest rectangle under bars of different heights."},

{"id": "sc-028", "v": "ms-match", "dom": "metalworking", "diff": "E",
 "title": "The Sheffield Castings",
 "story": "The foundry at the bottom of Attercliffe has cast steel since the days when Sheffield cast nothing "
          "else, and its present foundry-master, a woman named Josephine Hartshorn whose grandfather held the "
          "same post, keeps the works' records in a notation her grandfather devised. She records each casting "
          "sequence as a string of brackets: round, square and curly, each pair standing for a mould opened and "
          "later sealed. A round bracket is a sand mould, a square one an investment mould, a curly one a "
          "shell.\n\n"
          "Moulds are nested, because a complex casting is built as a mould within a mould within a mould, and "
          "the physical order of the work imposes a rule. A sequence is acceptable only if every opened mould is "
          "sealed by the SAME kind of bracket and the seals come in the exact reverse order of the openings, so "
          "that an inner mould closes before the one enclosing it. A mould sealed with the wrong kind of bracket "
          "means a sand mould was closed with a shell, which is impossible; a mould sealed out of order means a "
          "mould was closed while something still stood open inside it, which is worse than impossible, because "
          "it means molten steel somewhere it should not be. At the end of the sequence every mould must be "
          "sealed.\n\n"
          "A previous clerk merely compared how many of each kind appeared, declared the sequence sound if the "
          "counts matched, and admitted several faulty sequences, one of which cracked a casting worth four "
          "months of the works' profit. He is no longer employed there and the notation is now checked properly, "
          "which is to say by someone reading it through from the beginning.\n\n"
          "The works' hooter still sounds at seven, to the annoyance of the new flats opposite. A cat called "
          "Crucible lives in the pattern shop. The company's apprentice scheme has a waiting list.\n\n"
          "Input: line one gives T, the number of sequences. Each of the next T lines gives one sequence as a "
          "string of the characters ( ) [ ] { }. Output: for each sequence, YES if it is acceptable, NO "
          "otherwise.\n\n"
          "Constraints: T up to 10^4; each sequence of length up to 10^6.",
 "clues": ["sealed by the SAME kind of bracket", "exact reverse order of the openings",
           "merely compared how many of each kind appeared"],
 "decoys": ["The works' hooter still sounds at seven, to the annoyance of the new flats opposite",
            "A cat called Crucible lives in the pattern shop",
            "The company's apprentice scheme has a waiting list"],
 "core": "Check that brackets are properly paired and nested.",
 "gloss": [("foundry", "a factory where metal is cast", True), ("mould", "a hollow shape that metal is poured into", True),
           ("enclosing", "surrounding", True), ("faulty", "broken or wrong", True),
           ("investment mould", "a mould made by coating a wax model", True)],
 "why": {"hs-freq": "Equal counts of each bracket do not prove correct order, as the story itself warns.",
         "ms-next": "That looks for the next bigger value; here the partner must be the matching kind, and the order of closing is what matters."},
 "tell": "Nesting: the most recently opened thing must be the first to close."},

{"id": "sc-029", "v": "ms-greedy", "dom": "watchmaking", "diff": "H",
 "title": "The Neuchatel Serial",
 "story": "The house of Perrin-Jaquet has made watches in Neuchatel since 1804, and it survived the quartz "
          "crisis by the simple expedient of ignoring it. A watchmaker there engraves each movement with a long "
          "serial of decimal digits, struck one digit at a time with a hand punch, recording the plate, the "
          "batch, the escapement pattern and a good deal else that only the house understands.\n\n"
          "By a quirk of the guild's lottery, instituted in the eighteen-nineties to settle a dispute about "
          "numbering and never since repealed, the house is entitled to strike out exactly K digits from a "
          "serial, leaving the rest in their ORIGINAL order, with no digit moved relative to any other. The "
          "privilege falls to one movement a year, chosen by ballot, and the buyer of that movement receives the "
          "movement whose remaining number is numerically smallest, this being thought, by whoever drafted the "
          "rule, to be the more elegant outcome. Any leading zeros are dropped when the number is read, and if "
          "nothing remains the number is 0.\n\n"
          "Given the serial and K, report the smallest number the house can leave. The present head of the "
          "house, Madame Perrin-Jaquet, has observed that one cannot simply strike out the K largest digits, "
          "since where a digit sits matters more than what it is, and that trying every possible choice of K "
          "digits would outlast the firm.\n\n"
          "The house's workshop has north light and a bench that has been in use for six generations. A "
          "collector in Singapore has offered an indecent sum for the 1911 ledger and been refused. The cat, as "
          "in every watch house, is forbidden the workshop and sleeps there anyway.\n\n"
          "Input: line one gives N, the number of digits, and K. Line two gives the serial as a string of N "
          "digits. Output: the smallest number obtainable, without leading zeros, or 0.\n\n"
          "Constraints: length up to 10^5; 0 <= K <= N.",
 "clues": ["strike out exactly K digits", "in their ORIGINAL order", "numerically smallest"],
 "decoys": ["A watchmaker there engraves each movement",
            "A collector in Singapore has offered an indecent sum for the 1911 ledger",
            "The house's workshop has north light and a bench that has been in use for six generations"],
 "core": "Remove exactly K digits, keeping the order of the rest, so the remaining number is as small as possible.",
 "gloss": [("engraves", "carves into a surface", True), ("quirk", "an odd or unusual rule", True),
           ("movement", "the inner mechanism of a watch", True), ("serial", "a long identifying number", True),
           ("escapement", "the part of a watch that regulates its ticking", True)],
 "why": {"iv-sortkey": "Sorting the digits would break the required order; the result must be what remains of the original.",
         "bk-subsets": "Trying every way to strike out K digits is exponential, and the serial has up to 100000 digits."},
 "tell": "Remove exactly K items, keep the order, make the result as small as possible."},

{"id": "sc-030", "v": "hp-topk", "dom": "sailing", "diff": "M",
 "title": "The Dubrovnik Regatta",
 "story": "The Dubrovnik regatta is sailed every August in the channel between the old city and the island of "
          "Lokrum, and it is organised by a yacht club whose equipment budget has not been revised since "
          "Yugoslavia. The scoreboard receives finishing times one at a time, as the boats cross the line, "
          "shouted down from a man with a stopwatch on the mole and chalked up as they come; a time is never "
          "revisited once announced, because the man with the stopwatch does not write anything down himself and "
          "has never been persuaded to.\n\n"
          "The fleet is large, with up to 10^6 recorded times when the junior and veteran classes are counted "
          "together with the main race. The harbour-master's slate, which is the only working surface on the "
          "mole, can hold at most K+1 entries at any moment, K being at most 100, and the harbour-master has "
          "resisted every suggestion that a larger slate be bought.\n\n"
          "At the close of the day the commodore insists on learning the K-th smallest finishing time recorded, "
          "that is, the time of the boat placed K-th, because the club's prizes go to the first K boats and the "
          "last of them must be identified before the dinner. Sorting the full record is not possible within the "
          "slate, and in any case the full record no longer exists: the times went by as they were called.\n\n"
          "The commodore's own boat has not finished a race in nine years. The club's trophy was melted down "
          "during the siege and replaced with a replica. A dispute about a port-and-starboard incident in the "
          "1998 race is raised, without fail, at every annual general meeting.\n\n"
          "Input: line one gives N and K. Line two gives the N finishing times in the order they were called. "
          "Output: the K-th smallest finishing time.\n\n"
          "Constraints: N up to 10^6, K up to 100 and at most N; times up to 10^9. Memory may grow with K but "
          "not with N.",
 "clues": ["one at a time", "can hold at most K+1 entries", "the K-th smallest finishing time"],
 "decoys": ["The scoreboard receives finishing times",
            "The commodore's own boat has not finished a race in nine years",
            "A dispute about a port-and-starboard incident in the 1998 race"],
 "core": "From a stream of numbers, with memory for only about K of them, report the K-th smallest.",
 "gloss": [("regatta", "a boat race meeting", True), ("commodore", "a senior officer of a yacht club", True),
           ("slate", "a small writing tablet", True), ("mole", "a stone pier or breakwater", True),
           ("fleet", "all the boats taking part", True)],
 "why": {"iv-sortkey": "Sorting everything needs memory for all of it, which the slate cannot hold.",
         "hp-two": "That tracks a median; here only the K-th item matters and K is small."},
 "tell": "A K-th best from a long stream, with memory for only about K items."},

{"id": "sc-031", "v": "hp-merge", "dom": "postal history", "diff": "M",
 "title": "The Vienna Timetable",
 "story": "The imperial post of the Habsburg lands was the wonder of Europe and the despair of its own clerks, "
          "running coaches from Laibach to Lemberg on a timetable published quarterly in three languages. K "
          "provincial depots each send the departure times of their coaches, already in ascending order, to the "
          "central bureau in Vienna, each depot writing out its own times on its own sheet, as its own "
          "postmaster has done since his appointment.\n\n"
          "The bureau's clerk, a Hofrat of the fourth class named Aloys Pemmerl, must weave all of these lists "
          "into one single ascending timetable for the printer, who is waiting and who charges by the hour. He "
          "may take the sheets in any order he likes, but he may only read down each sheet from its top, since "
          "the sheets are gummed into a book at the bureau's insistence and cannot be held open at the middle; "
          "and he has desk room for one line from each sheet at a time, no more.\n\n"
          "The Emperor takes a keen interest in punctuality, which is why the timetable exists at all and why "
          "Pemmerl's predecessor was transferred to Czernowitz. There are at most 1000 depots, and altogether up "
          "to 10^6 times; concatenating and re-sorting everything would waste the fact that every list arrives "
          "already ordered, besides needing a desk the bureau has not got.\n\n"
          "Pemmerl keeps a tin of candied violets in his drawer. The bureau's stove smokes when the wind is in "
          "the east. A clerk in the next room has been writing a comic opera for eleven years and has read parts "
          "of it aloud to anyone who could not escape.\n\n"
          "Input: line one gives K. Each of the next K lines begins with a count M, then M departure times in "
          "ascending order. Output: all the times from all the depots as one non-decreasing sequence.\n\n"
          "Constraints: at most 1000 depots; total times up to 10^6; each time up to 10^9.",
 "clues": ["already in ascending order", "weave all of these lists into one single ascending timetable",
           "at most 1000 depots"],
 "decoys": ["The Emperor takes a keen interest in punctuality",
            "Pemmerl keeps a tin of candied violets in his drawer",
            "has been writing a comic opera for eleven years"],
 "core": "Combine K already-sorted lists into a single sorted list.",
 "gloss": [("provincial", "of a region away from the capital", True), ("depots", "storage or dispatch centres", True),
           ("bureau", "an office", True), ("weave", "to interleave together", True),
           ("Hofrat", "an Austrian civil-service rank", True)],
 "why": {"tp-merge": "That handles exactly two lists; with up to a thousand you need to know which list holds the smallest front item.",
         "iv-sortkey": "Re-sorting everything ignores the order you were given and costs more."},
 "tell": "K sorted sequences to interleave into one."},

{"id": "sc-032", "v": "hp-two", "dom": "bullion trading", "diff": "H",
 "title": "The Amsterdam Quotations",
 "story": "The bullion trade of Amsterdam is conducted in a room off the Damrak that smells of pipe smoke and "
          "wet wool, and its oldest dealer is a man named Gerrit van Oosterhout, who has bought and sold metal "
          "through three wars and two currency collapses. He receives prices for a single ingot, one quotation "
          "at a time, called across the room or brought in by runners, up to 10^6 of them in the course of a "
          "trading season.\n\n"
          "Above his desk hangs a board, and the board is the reason the room is crowded. After EVERY quotation "
          "his board must display the middle price of all quotations received so far; if the count is even, the "
          "board shows the average of the two middle prices. The custom began as a safeguard: a dealer who "
          "posted the highest price would be accused of talking the market up, and one who posted the lowest of "
          "talking it down, so the middle is posted and nobody can complain. A quotation once received is never "
          "withdrawn or amended.\n\n"
          "Rewriting and sorting the whole record upon each arrival would take days, as van Oosterhout's own "
          "clerk established one miserable winter by attempting it. The board must change before the next "
          "quotation arrives, and in a busy hour they arrive every few seconds.\n\n"
          "The dealer's spectacles are always fogged by the canal mist, and he mutters about the cold. There is a "
          "stuffed heron in a case by the door that nobody can account for. A junior dealer has suggested "
          "posting an average of all the quotations instead, and has been told, at length, why that would be "
          "wrong, chiefly by reference to a single enormous quotation received in 1973.\n\n"
          "Input: line one gives N. Line two gives the N quotations in the order received. Output: N lines, the "
          "board's figure after each quotation, each to one decimal place.\n\n"
          "Constraints: N up to 10^6; prices up to 10^9. Each update must cost only a small, slowly growing "
          "amount of work.",
 "clues": ["EVERY quotation his board must display", "the middle price of all quotations received so far",
           "one quotation at a time"],
 "decoys": ["The dealer's spectacles are always fogged by the canal mist",
            "There is a stuffed heron in a case by the door that nobody can account for",
            "chiefly by reference to a single enormous quotation received in 1973"],
 "core": "After each new number arrives, report the median of everything received so far.",
 "gloss": [("bullion", "gold or silver in bulk", True), ("ingot", "a block of metal", True),
           ("quotation", "a stated price", True), ("amended", "changed", True)],
 "why": {"hp-topk": "That tracks one K-th item; the middle moves as the count grows.",
         "bs-partition": "That works on two fixed sorted lists, not a growing stream."},
 "tell": "The median of a growing collection, after each arrival."},

{"id": "sc-033", "v": "hp-greedy", "alt": ["iv-sweep"], "dom": "trade fairs", "diff": "M",
 "title": "The Leipzig Trestles",
 "story": "The Leipzig trade fair has been held twice a year since the twelfth century, and the fairmaster's "
          "office still uses the vocabulary of the mediaeval charter, which is why its forms speak of trestles "
          "and pitches rather than stands and slots. At the fair, N stallholders each book a pitch for the "
          "half-open interval [s, e), the pitch being free again the very moment e arrives, so that a "
          "stallholder who books until noon is gone at noon and the next may have it at noon exactly.\n\n"
          "Trade is done from trestles, which the fair owns and hires out. A single trestle can serve only one "
          "stallholder at a time, but may be moved on to the next stallholder as soon as the previous one "
          "leaves, and the porters are paid to do precisely that. The trestles are interchangeable; no "
          "stallholder may demand a particular one, a point the charter is explicit about after a quarrel in "
          "1498.\n\n"
          "The fairmaster must now tell the carpenters how many trestles to bring from the store, and he is "
          "anxious not to pay for more than he needs, since each is carted in from a yard outside the city and "
          "charged for. He wishes to supply the fewest trestles that will serve every booking, every booking "
          "being one he has already accepted and must honour.\n\n"
          "The fair's bell is rung by hand and the ringer is paid in beer. A dispute over the right to sell "
          "Nuremberg gingerbread has been before the city court for two years. The fairmaster's clerk has a "
          "stammer which worsens when the fairmaster is in the room, a fact the fairmaster has never "
          "noticed.\n\n"
          "Input: line one gives N. Each of the next N lines gives s and e for one booking. Output: the smallest "
          "number of trestles that serves every booking.\n\n"
          "Constraints: N up to 10^5, times up to 10^9, s strictly less than e.",
 "clues": ["the pitch being free again the very moment e arrives",
           "moved on to the next stallholder as soon as the previous one leaves", "the fewest trestles"],
 "decoys": ["The Leipzig trade fair has been held twice a year since the twelfth century",
            "The fair's bell is rung by hand and the ringer is paid in beer",
            "A dispute over the right to sell Nuremberg gingerbread"],
 "core": "The smallest number of resources needed so that no booking is turned away, reusing a resource as soon as its booking ends.",
 "gloss": [("pitch", "a spot for trading", True), ("trestle", "a movable table", True),
           ("stallholder", "a trader at a stall", True), ("charter", "a founding legal document", True),
           ("half-open interval", "includes the start but not the end", True)],
 "why": {"iv-greedy": "That picks the most bookings you can accept with one resource; here every booking must be served.",
         "iv-merge": "Merging overlaps ignores how many are needed at once."},
 "tell": "Reuse the earliest-finishing resource; count the fewest needed to cover every booking."},

{"id": "sc-034", "v": "iv-merge", "dom": "road works", "diff": "E",
 "title": "The Brenner Closures",
 "story": "The Brenner is the lowest of the great Alpine passes and the busiest, and the road over it is in a "
          "permanent condition of being repaired. The wardens of the Brenner Pass close the road for repairs in "
          "stretches, each booking a closure window [s, e] by kilometre-marker, and the bookings are submitted "
          "independently by the gangs responsible for surfacing, for the avalanche galleries, for the drainage "
          "and for the tunnel linings, none of whom speaks to the others more than is strictly required.\n\n"
          "Two bookings that overlap or share an endpoint are treated by the road authority as one continuous "
          "closure, because a motorist who can leave the road at kilometre forty and must immediately rejoin a "
          "closure at kilometre forty has not in any meaningful sense left the road. The authority therefore "
          "publishes not the bookings but the continuous closures, and its notices, which appear on the approach "
          "signs at Innsbruck and Vipiteno, must be accurate.\n\n"
          "Given the N bookings in no particular order, the chief warden wants the final list of continuous "
          "closures, ordered from the lowest marker upward. He does not want to know which gang is responsible "
          "for which stretch, nor how many gangs are at work in any one place; the notice has room only for the "
          "stretches themselves.\n\n"
          "The pass has a chapel at the summit and a petrol station that charges what it likes. Lorry drivers "
          "have an opinion about the Austrian toll system which they share freely. A marmot colony near "
          "kilometre sixty is protected and has halted one gang's work entirely, to the quiet satisfaction of "
          "the other three.\n\n"
          "Input: line one gives N. Each of the next N lines gives s and e for one booking. Output: the "
          "continuous closures, one per line as two numbers, from the lowest marker upward.\n\n"
          "Constraints: N up to 10^5; markers up to 10^9; s no greater than e.",
 "clues": ["overlap or share an endpoint", "treated by the road authority as one continuous closure",
           "in no particular order"],
 "decoys": ["The wardens of the Brenner Pass",
            "A marmot colony near kilometre sixty is protected",
            "The pass has a chapel at the summit and a petrol station that charges what it likes"],
 "core": "Combine overlapping ranges into the smallest set of non-overlapping ranges.",
 "gloss": [("warden", "an official guardian of a place", True), ("marker", "a post showing distance", True),
           ("endpoint", "the end of a range", True), ("closure", "a period when something is shut", True),
           ("galleries", "covered sections built to protect a road", True)],
 "why": {"iv-sweep": "That counts how many overlap at once; it does not produce the combined ranges.",
         "iv-insert": "That adds one range to a list already sorted and disjoint; here everything is unsorted."},
 "tell": "Combine overlapping ranges into continuous blocks."},

{"id": "sc-035", "v": "iv-insert", "alt": ["iv-merge"], "dom": "harbours", "diff": "M",
 "title": "The Cuxhaven Dredging Schedule",
 "story": "Cuxhaven sits where the Elbe becomes the sea, and the channel that carries the container traffic up "
          "to Hamburg silts up as fast as it is cleared. The tide-gauge office there keeps the dredging "
          "schedule, and it already holds a schedule of dredging closures as a list of non-overlapping time "
          "bands, kept in ascending order. The order and the disjointness are not accidents: the office has "
          "maintained the list in that condition for thirty years, and the clerk who maintains it regards any "
          "suggestion that it might be otherwise as a slur.\n\n"
          "A new closure band arrives by telex from the waterways authority, naming a start and an end. It may "
          "fall into a gap between existing bands, in which case it simply takes its place; or it may overlap or "
          "touch one or several existing bands, in which case the harbour-master wants the updated schedule, "
          "with any bands the newcomer overlaps absorbed into it, so that the result is again a list of "
          "non-overlapping bands, still in ascending order.\n\n"
          "Re-sorting the entire schedule for a single arrival would be wasteful, and the clerk has said so in a "
          "memorandum of some length. The schedule runs to as many as 10^5 existing bands and the telexes arrive "
          "all day.\n\n"
          "The gulls, as ever, are indifferent. The office's tide gauge is a float in a well and is checked "
          "against a staff gauge every Monday. A pilot boat crew has a long-running feud with a tug crew over a "
          "parking space, and the harbour-master has declined three times to adjudicate.\n\n"
          "Input: line one gives N and then the new band's s and e. Each of the next N lines gives one existing "
          "band, already in ascending order and non-overlapping. Output: the updated schedule, one band per "
          "line, in ascending order.\n\n"
          "Constraints: up to 10^5 existing bands; times up to 10^9. One sweep along the schedule, with no "
          "sorting, is expected.",
 "clues": ["non-overlapping time bands, kept in ascending order", "A new closure band arrives",
           "Re-sorting the entire schedule for a single arrival would be wasteful"],
 "decoys": ["The gulls, as ever, are indifferent",
            "A pilot boat crew has a long-running feud with a tug crew over a parking space",
            "The office's tide gauge is a float in a well"],
 "core": "Add one range to a sorted, non-overlapping list of ranges, combining it with any it overlaps.",
 "gloss": [("dredging", "clearing the bed of a waterway", True), ("bands", "ranges", True),
           ("absorbed", "taken in and combined", True), ("schedule", "a planned list of times", True),
           ("silts up", "fills with fine mud", True)],
 "why": {"iv-merge": "A fair way (add it and combine everything), but it throws away the sorted order you were given.",
         "iv-sweep": "That counts overlaps; it does not build the updated list."},
 "tell": "One new range into a list that is already sorted and disjoint."},

{"id": "sc-036", "v": "iv-greedy", "dom": "universities", "diff": "M",
 "title": "The Sorbonne Lectures",
 "story": "The Great Hall of the Sorbonne is given over each spring to a season of public lectures, announced on "
          "a single poster that the university prints without any attempt to arrange them conveniently. N public "
          "lectures are announced, lecture i occupying the hours from s[i] to e[i], and because the hall is "
          "shared with the law faculty the times were fixed by whoever applied first. A lecturer may begin "
          "exactly when another ends, the porters having become adept at turning the hall round in no time at "
          "all.\n\n"
          "A single devoted scholar, an elderly woman who has attended the season every year since her "
          "retirement and who is known to the porters by name, wishes to attend as many whole lectures as "
          "possible. She will not walk out of a lecture before the end, considering it discourteous, and she "
          "cannot be in two places at once, so she is never present at two at once. She does not care in the "
          "least which lectures they are: the mathematics and the Mesopotamian pottery are of equal interest to "
          "her, and she has said so to the Dean.\n\n"
          "Report the largest number she can attend. The hall is draughty and the benches are hard, but she is "
          "undeterred. Her own first idea was to start with whichever lecture began earliest and carry on from "
          "there, which once cost her an entire afternoon on a single lecture about canals.\n\n"
          "The Dean has a theory about the acoustics which the lecturers dispute. A bust of Richelieu in the "
          "vestibule is touched for luck by students before examinations, and its nose is correspondingly "
          "bright. The university's coffee is notorious.\n\n"
          "Input: line one gives N. Each of the next N lines gives s and e for one lecture. Output: the largest "
          "number of whole lectures that can be attended with no two overlapping.\n\n"
          "Constraints: N up to 10^5, times up to 10^9, s strictly less than e.",
 "clues": ["as many whole lectures as possible", "never present at two at once",
           "may begin exactly when another ends"],
 "decoys": ["The hall is draughty and the benches are hard",
            "A bust of Richelieu in the vestibule is touched for luck by students",
            "The Dean has a theory about the acoustics which the lecturers dispute"],
 "core": "Choose the largest set of intervals that do not overlap.",
 "gloss": [("devoted", "very committed", True), ("scholar", "a learned person", True),
           ("occupying", "taking up", True), ("vestibule", "an entrance hall", True),
           ("undeterred", "not put off", True)],
 "why": {"hp-greedy": "That finds how many resources are needed to serve every booking; here you choose which bookings to accept.",
         "dp-linear": "A table over the lectures would also work but is slower; sorting by ending time is the whole decision."},
 "tell": "Choose the most non-overlapping bookings; sort by ending time."},

{"id": "sc-037", "v": "iv-sweep", "alt": ["hp-greedy"], "dom": "railways", "diff": "M",
 "title": "The Restaurant Car",
 "story": "The Compagnie Internationale des Wagons-Lits is refitting the restaurant car of the Orient Express, "
          "and the question of how many seats it should contain has become a matter of some feeling among the "
          "staff. To settle it, the company has produced the service records: arrival and departure times are "
          "logged for N parties, party i being seated from a[i] until b[i], and a party leaving at the very "
          "minute another arrives has already left, the stewards being practised at clearing a table while the "
          "next guests are still in the corridor.\n\n"
          "The head waiter, Monsieur Dufour, wants to know how many seats the car must be fitted with, which is "
          "to say he needs the largest number of parties dining at the same moment anywhere in the records. He "
          "does not want the total number of parties served, which the company's accountants have already "
          "produced and which he regards as beside the point; nor the length of the average meal, which the "
          "chef has produced and which he regards as propaganda.\n\n"
          "The records were entered by whichever steward was free, so they are in no order of time, and they run "
          "to many tens of thousands of parties across several seasons. Monsieur Dufour has also observed that "
          "the minutes themselves run into the billions on the company's clock, so a tally kept for every "
          "possible minute is out of the question.\n\n"
          "The chef, meanwhile, is quarrelling with the wine steward about the vintage. The car's marquetry "
          "panels are by a Belgian firm that no longer exists. A spoon stolen in 1956 was returned anonymously "
          "in 1991 with a note of apology.\n\n"
          "Input: line one gives N. Each of the next N lines gives a and b for one party. Output: the greatest "
          "number of parties seated at any one moment.\n\n"
          "Constraints: N up to 10^5, times up to 10^9, a no greater than b.",
 "clues": ["the largest number of parties dining at the same moment", "has already left"],
 "decoys": ["The chef, meanwhile, is quarrelling with the wine steward about the vintage",
            "The car's marquetry panels are by a Belgian firm that no longer exists",
            "A spoon stolen in 1956 was returned anonymously in 1991 with a note of apology"],
 "core": "The largest number of ranges that overlap at a single instant.",
 "gloss": [("vintage", "the year a wine was made", True), ("steward", "a servant who waits on guests", True),
           ("logged", "written down in a record", True), ("marquetry", "decorative inlaid woodwork", True)],
 "why": {"hp-greedy": "A fair alternative: it reaches the same number by reusing the earliest-free seat.",
         "iv-merge": "That produces combined blocks, not a count of overlaps at one moment."},
 "tell": "The most things happening at the same moment."},

{"id": "sc-038", "v": "iv-sortkey", "dom": "festivals", "diff": "H",
 "title": "The Binche Procession",
 "story": "The carnival of Binche is older than any record of it and is guarded by its town with a ferocity that "
          "outsiders find hard to credit. Its central event is the procession of the Gilles, who wear hats of "
          "ostrich plumes so tall that the wearer must duck under the tram wires, and the order in which they "
          "walk is fixed by custom and argued over all year.\n\n"
          "This year the marshal has lost the running order and must rebuild it from the performers' own "
          "statements. N performers line up for the procession, and each performer is described by a pair (h, "
          "k): h is the height of the hat, and k is the number of performers standing IN FRONT of her whose hats "
          "are at least as tall as hers. Each performer gave her own pair from memory, having been asked at the "
          "end of last year's procession what she could see ahead of her, and the town's archivist wrote them "
          "down in the order the answers came in.\n\n"
          "The marshal has these pairs in no particular order and wishes to reconstruct the one line-up that "
          "agrees with every performer's description, from the front of the procession to the back. It is "
          "promised that such a line-up exists and that it is the only one. He does not want to know who is "
          "where by name, only the sequence of hat heights.\n\n"
          "The plumes are hired from a firm in Brussels at a cost the town council publishes reluctantly. "
          "Oranges are thrown into the crowd on the final day and it is an offence to throw one back. A film "
          "crew was expelled in 1987 for reasons the town will not discuss with journalists.\n\n"
          "Input: line one gives N. Each of the next N lines gives h and k for one performer, in no particular "
          "order. Output: the N hat heights in line-up order, front to back.\n\n"
          "Constraints: N up to 2000; heights up to 10^6; 0 <= k < N.",
 "clues": ["k is the number of performers standing IN FRONT of her whose hats are at least as tall as hers",
           "reconstruct the one line-up", "in no particular order"],
 "decoys": ["The carnival of Binche is older than any record of it",
            "Oranges are thrown into the crowd on the final day",
            "A film crew was expelled in 1987 for reasons the town will not discuss"],
 "core": "Rebuild an ordering from each item's (size, how many items at least as big stand before it).",
 "gloss": [("marshal", "an official who organises a procession", True), ("procession", "a parade", True),
           ("performers", "people who take part in a show", True), ("plumes", "large feathers", True),
           ("archivist", "a keeper of records", True)],
 "why": {"bk-perms": "Trying every ordering is factorial; the right sorting key makes it one pass.",
         "dp-lis": "Nothing here asks for a longest chain."},
 "tell": "Choosing the right sort key turns the rebuild into a single pass."},

{"id": "sc-039", "v": "bt-xor", "dom": "coinage", "diff": "M",
 "title": "The Kremnica Dies",
 "story": "The mint at Kremnica has struck coin since 1328 and is the oldest working mint in the world, a fact "
          "the town puts on its road signs. The mint stamps each coin die with an identification number, and "
          "every die is used in a matched pair so that the pair can be compared for wear: when the two faces of "
          "a pair begin to differ, both are withdrawn and recut, which is how the mint has kept its coin "
          "consistent for seven centuries.\n\n"
          "One die, however, was used alone after its twin cracked. It happened during the silver shortage, when "
          "the mint was running three shifts and the warden of the day signed off a batch he should not have "
          "signed off, and the resulting coins are now a famous variety among collectors and a quiet "
          "embarrassment to the mint. The present warden has been instructed by the ministry to identify the die "
          "in question.\n\n"
          "She has the list of N die numbers, taken from the vault in whatever order they came off the racks, "
          "and the vault's counting-board has room for only a few numbers beyond the list itself, the vault "
          "being a strongroom and not an office. She may read the list through as many times as she likes but "
          "may not copy it out, sort it, or carry it upstairs. Report the number of the unpaired die.\n\n"
          "The mint's museum sells replica thalers to tourists. A fire in 1636 destroyed the records of the "
          "preceding century, which is why the mint's own history before that date is vague. The warden's "
          "predecessor retired after an argument about the alloy.\n\n"
          "Input: line one gives N. Line two gives the N die numbers in no order. Output: the number of the one "
          "die that appears an odd number of times.\n\n"
          "Constraints: N odd, up to 10^6, each number up to 10^9. Every other die number appears exactly twice, "
          "and extra memory must not grow with N.",
 "clues": ["matched pair", "used alone", "room for only a few numbers beyond the list itself"],
 "decoys": ["The mint at Kremnica has struck coin since 1328",
            "The mint's museum sells replica thalers to tourists",
            "A fire in 1636 destroyed the records of the preceding century"],
 "core": "Every item appears twice except one; find it using almost no extra memory.",
 "gloss": [("mint", "a place where coins are made", True), ("die", "a metal stamp used to strike coins", True),
           ("warden", "an official keeper", True), ("twin", "its identical partner", True),
           ("thaler", "an old silver coin", True)],
 "why": {"hs-freq": "A tally needs memory proportional to the list, which the counting-board lacks.",
         "hs-cyclic": "That needs the values to lie between 1 and N; here they reach a billion."},
 "tell": "Pairs cancel, and extra memory is nearly forbidden."},
]
