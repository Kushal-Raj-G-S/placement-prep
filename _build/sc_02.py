# -*- coding: utf-8 -*-
"""Scenario questions, batch 2: prefix sum (rest), binary search, hashing, monotonic stack (first).

OA-size stories (around 400 words) with their own Input / Output / Constraints lines. The answer keys
(v, alt, core, why, tell) are the originals.
"""

QUESTIONS = [

{"id": "sc-014", "v": "ps-diff", "alt": ["iv-sweep"], "dom": "textile restoration", "diff": "M",
 "title": "The Aubrey Tapestry",
 "story": "The Aubrey tapestry is a seventeenth-century hunting scene twenty-two feet long, and it has been "
          "hanging in the long gallery of a house in Wiltshire since it was woven, which is precisely the "
          "trouble: three centuries of daylight and coal smoke have left the wool as fragile as ash. The "
          "restorers of the Aubrey tapestry have divided its border into N numbered panels, each beginning with "
          "no thread repaired, and the whole programme of work is reckoned panel by panel.\n\n"
          "Money arrives in fits and starts, from a trust, from a county fund, and from the family itself, and "
          "each gift pays for a different stretch of the border. Throughout the season there are M commissions, "
          "and each instructs the weavers to add V stitches' worth of reinforcement to every panel from L through "
          "R, both panels included. The commissions overlap freely, since a benefactor rarely knows or cares what "
          "another has already paid for, and some of them cover almost the whole border while others cover a "
          "handful of panels.\n\n"
          "The conservator in charge, Dr Annelise Fairbrother, is a careful woman who refuses to be hurried. She "
          "never inspects the border between commissions, holding that a tapestry handled repeatedly is a "
          "tapestry damaged repeatedly; only when the last is done will she ask how much reinforcement each panel "
          "carries, panel by panel from the first to the last, for her final report to the trust.\n\n"
          "Her predecessor's method was to work through every commission panel by panel, entering the figure "
          "against each panel in turn, and he retired early. Applying every commission panel by panel would take "
          "far too long for M and N up to 2*10^5.\n\n"
          "The gallery is kept at eighteen degrees and the family complains of it. A conservation student has "
          "written a dissertation on the dog in the bottom left corner, which may be a later addition. The house "
          "cat is banned from the gallery and resents it visibly.\n\n"
          "Input: line one gives N and M. Each of the next M lines gives L, R and V. Output: N numbers, the "
          "reinforcement standing against each panel at the end of the season, in panel order.\n\n"
          "Constraints: M and N up to 2*10^5; V between 1 and 10^4; 1 <= L <= R <= N.",
 "clues": ["add V stitches' worth of reinforcement to every panel from L through R",
           "never inspects the border between commissions", "only when the last is done will she ask",
           "M and N up to 2*10^5"],
 "decoys": ["The restorers of the Aubrey tapestry",
            "a dissertation on the dog in the bottom left corner",
            "The house cat is banned from the gallery and resents it visibly"],
 "core": "Many additions to ranges of a list, with the final values read only once at the very end.",
 "gloss": [("tapestry", "a woven wall hanging", True), ("conservator", "an expert who preserves old artefacts", True),
           ("commissions", "jobs given to someone to carry out", True), ("reinforcement", "extra strengthening", True),
           ("benefactor", "someone who gives money to a cause", True)],
 "why": {"ps-range": "Prefix tables answer many reads over fixed data; here the data is rewritten again and again and read once.",
         "iv-sweep": "The same idea seen as a timeline of starts and ends; a fair alternative to the difference array."},
 "tell": "Many range updates, read once at the end."},

{"id": "sc-015", "v": "ps-suffix", "dom": "statecraft", "diff": "M",
 "title": "The Council Seals",
 "story": "The Venetian Council of Ten, which was never composed of ten men and which outlasted every republic "
          "around it, conducted its business by a system of seals so elaborate that its own clerks complained. "
          "The Council assigns each of its N sworn auditors a seal multiplier m[i], a small whole number struck "
          "into a brass token that the auditor carries on a chain and surrenders only at death.\n\n"
          "Every report an auditor submits must be sealed before the Council will read it, and the rule of "
          "sealing is the Council's own protection against a single corrupt official: the sealing of each "
          "auditor's report requires the product of the multipliers of every OTHER auditor, never including the "
          "auditor's own. The reasoning, set down in 1457, is that no auditor can forge his own seal without the "
          "cooperation of all his colleagues, and the Council of Ten did not believe that all its auditors could "
          "agree on anything.\n\n"
          "The work falls to the Doge's cipher-clerk, a careful and much-abused man named Zanetto Barbarigo, who "
          "must derive every report's seal. His difficulty is a mechanical one: his abacus cannot perform "
          "division, having been built in Ragusa to a design that never provided for it, and the Arsenal has "
          "twice refused his request for a new one. He must therefore reach each seal by multiplication alone.\n\n"
          "The council meets only on feast days and its auditors are elected for life, so the roll changes "
          "rarely. Barbarigo's office has a window that will not close and a view of a wall. He is owed eleven "
          "months of salary, a matter he has raised in writing four times.\n\n"
          "Input: line one gives N. Line two gives the N multipliers. Output: N numbers, the seal for each "
          "auditor's report, in the order the auditors appear on the roll.\n\n"
          "Constraints: N up to 10^5, 1 <= m[i] <= 100; every seal fits in a signed 64-bit integer. Division is "
          "not available at any point, so a grand total divided by each multiplier is not open to him.",
 "clues": ["the product of the multipliers of every OTHER auditor", "never including the auditor's own",
           "cannot perform division"],
 "decoys": ["The council meets only on feast days and its auditors are elected for life",
            "Barbarigo's office has a window that will not close and a view of a wall",
            "He is owed eleven months of salary"],
 "core": "For each item, the product of all the other items, without dividing.",
 "gloss": [("auditors", "officials who check accounts", True), ("multiplier", "a number you multiply by", True),
           ("abacus", "an ancient counting frame", True), ("cipher-clerk", "someone who handles coded messages", True),
           ("Doge", "the elected ruler of Venice", True)],
 "why": {"ps-range": "A range total adds a contiguous block; the excluded auditor sits in the middle, so you need what lies on both sides.",
         "hs-freq": "Counting does not produce products."},
 "tell": "Everything except me, and division is forbidden."},

{"id": "sc-016", "v": "bs-exact", "alt": ["hs-seen"], "dom": "library", "diff": "E",
 "title": "The Ostrava Ledger",
 "story": "The Ostrava lending library was founded by a steelworkers' benevolent society in 1891 and has been "
          "run since the war on a budget that its keeper describes as theoretical. The keeper, a brisk woman "
          "named Mrs Blazena Dvorakova, holds N accession numbers on a ledger, ordered from the smallest to the "
          "largest, with none repeated, because a number is issued once when a book enters the collection and is "
          "never reissued, even when the book itself is lost, stolen or eaten by a reader's dog.\n\n"
          "Since the catalogue went onto the regional network, readers send enquiries by the thousand, each "
          "naming one accession number and asking only whether the library has ever recorded it. A reader asks "
          "because another library's catalogue has pointed them here, or because they are tracing a book "
          "mentioned in a footnote; what they want is a yes or a no, and the staff are instructed to give one "
          "without comment. The enquiries arrive in no connection with the order of the ledger, and each must be "
          "answered on its own.\n\n"
          "With N and the count of enquiries both near 10^6, scanning the ledger from its first line for every "
          "enquiry would keep the readers waiting for years, as the one member of staff who attempted it can "
          "confirm. Mrs Dvorakova also declines to have the ledger copied into any other arrangement, since the "
          "ledger's order is the order in which the library grew and is itself a historical record.\n\n"
          "The reading room has a stove that must be lit by hand. A retired metallurgist comes every Tuesday to "
          "read the newspapers and falls asleep in the same chair. The library's cat is called Svejk and is "
          "fed, against the rules, by three separate members of staff who are each unaware of the others.\n\n"
          "Input: line one gives N and Q. Line two gives the N accession numbers in increasing order. Each of "
          "the next Q lines gives one number enquired about. Output: for each enquiry, YES or NO.\n\n"
          "Constraints: N and Q up to 10^6; accession numbers up to 10^18.",
 "clues": ["ordered from the smallest to the largest", "whether the library has ever recorded it",
           "N and the count of enquiries both near 10^6"],
 "decoys": ["Ostrava lending library", "A retired metallurgist comes every Tuesday to read the newspapers",
            "The library's cat is called Svejk"],
 "core": "A sorted list and a huge number of yes-or-no membership questions.",
 "gloss": [("accession number", "a number given to a newly acquired item", True),
           ("ledger", "an official book of records", True), ("enquiries", "questions", True),
           ("benevolent society", "a club that supports its members in hardship", True)],
 "why": {"hs-seen": "A set also answers each query instantly and is a fair alternative; the order you are handed makes it unnecessary.",
         "tp-ends": "Two markers look for a pair; each enquiry here is about a single value."},
 "tell": "A sorted list and a huge number of membership questions."},

{"id": "sc-017", "v": "bs-bound", "dom": "commerce", "diff": "M",
 "title": "The Lisbon Cut-Off",
 "story": "Bidding at the Lisbon wool exchange is done by bell: a bidder presses a brass button at his desk, a "
          "bell sounds in the clerks' gallery above, and the moment is filed. The auctioneer at the Lisbon wool "
          "exchange files the arrival time of every bid on a slate that is sorted from earliest to latest, "
          "because the filing clerk writes each bid down as the bell rings and has never once been asked to "
          "rearrange them. Several bidders may press the bell within the same second, so times can repeat, "
          "sometimes four or five times over when the bidding is fierce.\n\n"
          "A dispute has arisen over a lot of merino that was knocked down at a price two bidders say they had "
          "already beaten. A magistrate has been appointed, and his method is statistical rather than "
          "testimonial: he distrusts witnesses and trusts slates. Wishing to know how many bids arrived strictly "
          "before a stated cut-off instant, he will pose many such questions, naming a different instant each "
          "time as he works through the afternoon's lots one by one. An instant he names need not be an instant "
          "at which any bid actually arrived.\n\n"
          "The exchange's clerks have been instructed to cooperate fully, an instruction they resent. The "
          "building has a tiled frontage that appears on postcards. The auctioneer, Senhor Vasconcelos, has a "
          "parrot in his office which the magistrate has asked to have removed during the hearing, and the "
          "request has been refused on the grounds that the parrot predates the magistrate.\n\n"
          "Input: line one gives N and Q. Line two gives the N bid times in non-decreasing order. Each of the "
          "next Q lines gives one cut-off instant. Output: for each, the number of bids that arrived strictly "
          "before it.\n\n"
          "Constraints: N and the number of cut-offs up to 10^6; times up to 10^9. Each answer must be found "
          "without reading most of the slate.",
 "clues": ["sorted from earliest to latest", "times can repeat",
           "how many bids arrived strictly before a stated cut-off instant"],
 "decoys": ["at the Lisbon wool exchange", "The building has a tiled frontage that appears on postcards",
            "has a parrot in his office which the magistrate has asked to have removed"],
 "core": "In a sorted list with repeats, count how many items are strictly below a given value, for many different values.",
 "gloss": [("slate", "a writing tablet", True), ("magistrate", "a judge or public official", True),
           ("cut-off instant", "a deadline moment", True), ("strictly", "not counting equal values", True),
           ("merino", "a fine kind of wool", True)],
 "why": {"bs-exact": "That finds one specific value; the cut-off may not be in the list, and repeats mean you want the FIRST place it could sit.",
         "hs-freq": "A tally per value does not give you everything below a boundary."},
 "tell": "A count of items below a threshold in sorted data, which is where the threshold would be inserted."},

{"id": "sc-018", "v": "bs-answer", "dom": "brewing", "diff": "M",
 "title": "The Lubeck Malting Floor",
 "story": "The Hanse brewers of Lubeck hold their privileges from the Emperor himself, and among those "
          "privileges is the right to sell at the autumn fair, which is the single event on which the year's "
          "accounts turn. Before they can brew they must malt, and this season they must malt N barley lots "
          "before the autumn fair, lot i weighing c[i] stone. The lots arrive from the estates of the hinterland "
          "in whatever order the carters bring them, and the guild's book records their weights in that same "
          "order.\n\n"
          "The brewers share a single malting floor, a vast heated room beneath the guild hall, and it can "
          "process exactly R stone per day at a steady pace. By guild custom, which is enforced by a warden with "
          "a ledger and a bad temper, the floor never mixes two lots within a day; whatever remains of a lot "
          "after its last pass that day waits idle until the morrow. So a day's work is spent on lots taken in "
          "order, and a lot that will not fit in what is left of the day's capacity must wait.\n\n"
          "The fair opens in D days, and every lot must be done by then, or the guild forfeits its stall and, "
          "worse, its precedence in the procession. The brewers are therefore not asking how long the work will "
          "take at a given rate. They want to know what rate they must hire the floor at, and since the floor is "
          "charged by its daily rate they want the cheapest that will serve: find the lowest daily rate R that "
          "suffices.\n\n"
          "The guild's seal shows a barrel and a lion. One of the brewers has introduced a hopped beer that the "
          "elders mistrust. The warden's ledger was dropped in the Trave in 1483 and has been illegible from "
          "page sixty onwards ever since.\n\n"
          "Input: line one gives N and D. Line two gives the N lot weights in the order the carters delivered "
          "them. Output: the smallest whole-number daily rate R with which all lots are malted within D days.\n\n"
          "Constraints: N up to 10^5, c[i] and D up to 10^9. A faster floor can never make the work take longer.",
 "clues": ["lowest daily rate R that suffices", "never mixes two lots within a day", "c[i] and D up to 10^9"],
 "decoys": ["before the autumn fair", "The guild's seal shows a barrel and a lion",
            "The warden's ledger was dropped in the Trave in 1483"],
 "core": "Find the smallest value of a setting such that a job finishes in time, when the range of settings is enormous.",
 "gloss": [("malt", "to prepare grain for brewing", True), ("lot", "a batch", True),
           ("stone", "an old unit of weight", True), ("morrow", "the next day", True),
           ("suffices", "is enough", True), ("hinterland", "the land behind a port", True)],
 "why": {"bs-exact": "There is no sorted list to search; the thing you search is the range of possible rates.",
         "dp-coin": "That builds a minimum over combinations; here a faster rate can only help, which is what lets you halve the range."},
 "tell": "The smallest value of a dial that makes a condition hold, with a huge range and an easy test."},

{"id": "sc-019", "v": "bs-rotated", "dom": "horology", "diff": "M",
 "title": "The Prague Drum",
 "story": "The great clock of Prague has been rebuilt, repaired, and in one disastrous year improved, by "
          "clockmakers of six centuries, and the mechanism that strikes the hours is the oldest surviving part of "
          "it. Deep in the frame it turns a drum bearing N bell-tags engraved with distinct numbers, each number "
          "the pitch of a bell the tag releases. When cast, the tags ran in increasing order from the first "
          "notch, climbing from the deepest bell to the highest, a pleasing arrangement that the founder "
          "recorded in his will.\n\n"
          "The drum has since been rotated by some unknown number of notches. It happened during a repair, "
          "probably the repair of 1787, and no record was kept; the result is that the sequence now begins "
          "mid-way and wraps around, running up to the highest pitch, falling to the deepest, and climbing again "
          "to the tag that originally stood just before the new start. Nobody knows how far it was turned, and "
          "the frame cannot now be opened without dismantling the striking train.\n\n"
          "The bell-ringer, who is also the clock's custodian and sells postcards in the interval, must decide "
          "whether a given number is on the drum at all, because visiting campanologists write to ask and the "
          "city has promised them an answer. The guild's rule, laid down when the clock was first put under "
          "guild care, says each decision must take time proportional only to the logarithm of N, a rule the "
          "guild inherited from a mathematician mayor and has never understood but always obeyed.\n\n"
          "The clock's astronomical dial is admired by tourists who do not know what it shows. A legend says the "
          "builder was blinded so he could not repeat the work, which is untrue. A pigeon problem has defeated "
          "three successive contractors.\n\n"
          "Input: line one gives N and the pitch P being asked about. Line two gives the N pitches as the drum "
          "now reads them, from the first notch onward. Output: the position of P on the drum counting from 1, "
          "or -1 if it is absent.\n\n"
          "Constraints: N up to 10^6; pitches are distinct and up to 10^9.",
 "clues": ["rotated by some unknown number of notches", "begins mid-way and wraps around",
           "proportional only to the logarithm of N"],
 "decoys": ["The great clock of Prague", "A legend says the builder was blinded so he could not repeat the work",
            "A pigeon problem has defeated three successive contractors"],
 "core": "A sorted list that has been rotated by an unknown amount: is a value present, in logarithmic time?",
 "gloss": [("drum", "a rotating cylinder", True), ("notches", "small cuts or marks", True),
           ("engraved", "carved into a surface", True), ("campanologists", "people who study or ring bells", True),
           ("logarithm", "how many times you can halve something", False)],
 "why": {"bs-exact": "Plain halving assumes the whole list is in order; after a rotation only one half around the middle is guaranteed sorted.",
         "tp-ends": "A sweep is linear, which the logarithmic rule rules out."},
 "tell": "Sorted, then rotated by an unknown amount, in logarithmic time."},

{"id": "sc-020", "v": "bs-partition", "dom": "medicine", "diff": "H",
 "title": "The Physician's Two Rolls",
 "story": "The apothecary guilds of Padua and Bologna have been rivals since the universities were founded, and "
          "the rivalry is conducted chiefly through their price rolls. Two apothecary guilds, one in Padua and "
          "one in Bologna, each keep a price roll of their remedies, listed from cheapest to dearest, and each "
          "guild regards the other's roll as a work of fiction. The rolls are long, because the guilds list every "
          "preparation they have ever sold, including several that are now illegal.\n\n"
          "A visiting physician from Montpellier has been engaged by the city of Verona to advise on what it "
          "should pay for medicines, and his method is to take the typical price rather than the cheapest or the "
          "dearest, since a city that buys only the cheapest medicine soon buys a great deal of it. He therefore "
          "wants the median price across both rolls combined, meaning the middle value if all prices were "
          "gathered in one list, and where the combined number of prices is even he wants the average of the two "
          "middle values.\n\n"
          "There are two difficulties. The guilds will not permit their rolls to be copied, transcribed or "
          "merged, each suspecting the other of wanting a look; and the physician's satchel has no room for a "
          "merged copy in any case, since it already holds his instruments and a change of linen. The city, "
          "which is paying him by the day, has stipulated that the answer must be found in time proportional to "
          "the logarithm of the smaller roll.\n\n"
          "The physician is a believer in the new anatomy and has quarrelled about it publicly. Verona's own "
          "apothecary has written to the council objecting to the whole enquiry. The rolls hold up to 10^6 "
          "prices each, which neither guild considers excessive.\n\n"
          "Input: line one gives A and B. Line two gives the A prices of Padua, ascending; line three the B "
          "prices of Bologna, ascending. Output: the median price of all A + B prices, to one decimal place.\n\n"
          "Constraints: A and B up to 10^6, at least one non-empty; prices up to 10^9.",
 "clues": ["listed from cheapest to dearest", "the median price across both rolls combined",
           "no room for a merged copy", "logarithm of the smaller roll"],
 "decoys": ["A visiting physician", "The physician is a believer in the new anatomy and has quarrelled about it publicly",
            "Verona's own apothecary has written to the council objecting to the whole enquiry"],
 "core": "The middle value of two sorted lists taken together, without merging them, in logarithmic time.",
 "gloss": [("price roll", "a list of prices", True), ("remedies", "cures or medicines", True),
           ("satchel", "a small shoulder bag", True), ("transcribed", "copied out by hand", True),
           ("median", "the middle value", False)],
 "why": {"tp-merge": "Walking both lists together costs time proportional to their total length, which the limit forbids.",
         "hp-two": "Two heaps track the median of a stream; these are two fixed sorted lists."},
 "tell": "The median of two sorted arrays, with no merging, in logarithmic time."},

{"id": "sc-021", "v": "hs-seen", "dom": "theatre", "diff": "E",
 "title": "The Salzburg Tape",
 "story": "The opera house at Salzburg has a front-of-house manager named Herr Kasimir Stettner, a man whose "
          "devotion to procedure is spoken of with awe by the ushers and with weariness by everyone else. At his "
          "insistence, every patron's ticket is stamped with a serial at the door, and the stamping machine "
          "prints the serial onto a continuous paper tape as it works, producing a long tape of N serials in no "
          "particular order, since the order is simply the order in which people happened to arrive.\n\n"
          "This season the house has had trouble. Two patrons were found in the same seat during the second act "
          "of a Mozart, and a third produced a ticket for a performance that had been cancelled in 1998. Herr "
          "Stettner suspects forgery, and specifically he suspects that a forger has copied a genuine ticket, "
          "which would show itself as the same serial coming through the door twice. He wishes to discover, the "
          "moment the doors close, whether any serial was stamped more than once. He does not want to know which "
          "serial, nor how many duplicates there were; a single yes or no will tell him whether to call the "
          "police before the interval.\n\n"
          "The serials cannot be put in order: the tape is evidence and the Staatsanwalt has said so in writing. "
          "They are also large, each as large as a billion, because the house's numbering scheme encodes the "
          "season, the performance and the price band, a scheme Herr Stettner devised himself and defends "
          "vigorously.\n\n"
          "The orchestra has already begun the overture, and the manager is anxious to return to his box. The "
          "house's chandelier is lowered once a year for cleaning, an operation that draws a small crowd. The "
          "chief usher has worked there for forty years and claims to recognise every regular patron by their "
          "cough.\n\n"
          "Input: line one gives N. Line two gives the N serials in the order they were stamped. Output: YES if "
          "any serial appears more than once, NO otherwise.\n\n"
          "Constraints: N up to 10^6; serials up to 10^9.",
 "clues": ["in no particular order", "whether any serial was stamped more than once", "each as large as a billion"],
 "decoys": ["The orchestra has already begun the overture",
            "The house's chandelier is lowered once a year for cleaning",
            "claims to recognise every regular patron by their cough"],
 "core": "An unsorted list of big numbers: does any value appear twice?",
 "gloss": [("patron", "a regular customer", True), ("serial", "a unique identifying number", True),
           ("forgery", "a fake copy", True), ("overture", "the opening piece of music", True),
           ("Staatsanwalt", "a public prosecutor", True)],
 "why": {"tp-ends": "Two markers need sorted data, and sorting adds cost without telling you anything extra.",
         "hs-cyclic": "Marking inside the list only works if values are valid positions, 1 to N; here they reach a billion."},
 "tell": "Unsorted, large values, and the only question is 'have I seen this before?'"},

{"id": "sc-022", "v": "hs-freq", "dom": "caravan trade", "diff": "E",
 "title": "The Caravanserai Record",
 "story": "The caravanserai at Tash Rabat stands where three roads meet, a squat stone building with a courtyard "
          "and a well, and it has sheltered merchants, pilgrims and a certain number of thieves for seven "
          "hundred years. Its keeper is required by the khan's writ to keep a record, and so the caravanserai "
          "records the origin of each camel train as it halts, one letter per train, naming the oasis it set out "
          "from. The letters go into a scroll in the order the trains arrive, which is the order in which they "
          "happen to come over the pass, and nothing is ever reordered.\n\n"
          "At the end of the season the scroll goes to the khan, who has lately become interested in where his "
          "traffic actually comes from, having been told by one of his ministers that it comes chiefly from the "
          "west and by another that it comes chiefly from the south. After a season of N halts, the khan wishes "
          "to learn which single oasis supplied the greatest number of trains and exactly how many that was. He "
          "is not interested in the order of arrivals, nor in when the busiest month fell, nor in any oasis but "
          "the first; and he has been assured by the keeper that there is guaranteed to be no tie for first "
          "place.\n\n"
          "Dust storms delayed the record-keeping twice, and the scribe complains about the heat, a complaint he "
          "has entered into the scroll itself on two occasions. The well was redug in the spring and the water is "
          "said to be better. A dispute between two merchants over a lame camel was settled by the keeper in a "
          "manner neither party has accepted.\n\n"
          "Input: line one gives N. Line two gives a string of N letters, the origins in order of arrival. "
          "Output: the letter of the busiest oasis, and the number of trains it supplied.\n\n"
          "Constraints: N up to 10^6; origins are lowercase letters a to z.",
 "clues": ["which single oasis supplied the greatest number of trains", "exactly how many that was",
           "no tie for first place"],
 "decoys": ["Dust storms delayed the record-keeping twice", "The well was redug in the spring",
            "A dispute between two merchants over a lame camel"],
 "core": "Find the most frequent item in a long list, and how many times it occurs.",
 "gloss": [("caravanserai", "an inn for travelling merchants", True), ("oasis", "a green spot in a desert", True),
           ("khan", "a ruler or chief", True), ("halts", "stops", True), ("writ", "a formal written order", True)],
 "why": {"hs-seen": "A set only remembers that something happened, not how often.",
         "sw-longest": "The order of the records does not matter at all."},
 "tell": "How many times each thing occurs, and the answer is the biggest count."},

{"id": "sc-023", "v": "hs-index", "dom": "moneylending", "diff": "M",
 "title": "The Pawnbroker's Shelf",
 "story": "Signor Fosco Malatesta keeps a pawnbroker's shop in a street so narrow that the upper storeys almost "
          "meet, and he is, by the standards of his trade, an honest man: his interest is usurious but his "
          "records are exact. A pawnbroker's shelf behind the counter holds N pledges in a row, and pledge i is "
          "valued at p[i] ducats, the valuation being Malatesta's own and entered in his book when the pledge "
          "came in. The pledges stand in the order they were pawned, so the values are unsorted and always have "
          "been.\n\n"
          "A client arrives on a wet evening with a debt of exactly B ducats to settle and a proposal. He wishes "
          "to redeem precisely two different pledges whose values add to B, so that the redemption exactly "
          "cancels the debt and no coin need change hands, an arrangement that suits him for reasons he does not "
          "explain and that suits Malatesta because it closes an account. The clerk, a nephew of the house, must "
          "hand them over by their shelf positions, counting from zero, since the shelf is labelled by position "
          "and not by value; so he needs the two POSITIONS, smaller first. It is certain that exactly one such "
          "pair exists, Malatesta having already satisfied himself of that much while the client was taking off "
          "his cloak.\n\n"
          "The nephew is slow at figures and knows it. The shop's sign is a trio of golden balls, repainted last "
          "year. There is a dog on a chain in the back room whose job is to look fiercer than it is, and a canary "
          "whose cage is covered at dusk.\n\n"
          "Input: line one gives N and B. Line two gives the N pledge values in shelf order. Output: the two "
          "positions, counting from zero, smaller first.\n\n"
          "Constraints: N up to 10^6; values and B up to 10^9. The shelf must not be reordered, since the "
          "positions are what the clerk has to report.",
 "clues": ["values are unsorted", "the two POSITIONS, smaller first", "exactly one such pair exists"],
 "decoys": ["A pawnbroker's shelf", "The shop's sign is a trio of golden balls, repainted last year",
            "a canary whose cage is covered at dusk"],
 "core": "In an unsorted list, find the positions of two items that add up to a target.",
 "gloss": [("pawnbroker", "a lender who takes goods as security for a loan", True),
           ("pledges", "items left as security", True), ("ducats", "old gold coins", True),
           ("redeem", "to buy back", True), ("usurious", "charging unfairly high interest", True)],
 "why": {"tp-ends": "Two markers need the data sorted, and sorting scrambles the positions you must report.",
         "bs-exact": "That also needs sorted order and would also lose the original positions."},
 "tell": "Unsorted, and you must report the positions of the partner."},

{"id": "sc-024", "v": "hs-group", "dom": "locksmithing", "diff": "M",
 "title": "The Nuremberg Key Families",
 "story": "The locksmiths of Nuremberg were the finest in Europe for two centuries, and the guild's filing "
          "system was one of their lesser secrets. A locksmith in the guild of Nuremberg files each master key "
          "under a short word stamped on its bow, the word being a mnemonic for the ward pattern inside the lock "
          "it opens. The practice began as a convenience and hardened into a rule, and the rule brought with it "
          "an oddity that the guild has never resolved.\n\n"
          "Two keys belong to one family whenever the letters of one word can be rearranged to spell the other, "
          "so that 'tea', 'ate' and 'eat' are kin. The reason is mechanical: the stamp is cut from the same set "
          "of letter punches, and a key whose word uses the same punches in a different order was cut on the same "
          "bench from the same blank, whatever lock it was afterwards filed for. A key whose word shares no such "
          "relation with any other stands alone and is a family of one.\n\n"
          "The guild secretary, preparing an inventory for the city council, wishes to know how many distinct "
          "families exist among the keys now held. He does not want the families written out, nor the keys within "
          "them listed; the council's form has a single box for the number. Identical words count as the same "
          "family, as one would expect, since two keys stamped with the very same word were certainly cut "
          "together.\n\n"
          "The guild's hall has a door with eleven locks, only three of which work. An apprentice was expelled in "
          "1623 for cutting a key for a man who turned out to be a burglar, and the case is still taught. The "
          "secretary's own key to the strongbox has been lost since Whitsun and he has told nobody.\n\n"
          "Input: line one gives N. Each of the next N lines gives one stamped word. Output: the number of "
          "distinct families.\n\n"
          "Constraints: N up to 10^5, each of up to 20 lowercase letters. Comparing every word against every "
          "other letter by letter is too slow at this size.",
 "clues": ["letters of one word can be rearranged to spell the other", "how many distinct families exist"],
 "decoys": ["guild secretary", "The guild's hall has a door with eleven locks, only three of which work",
            "An apprentice was expelled in 1623 for cutting a key for a man who turned out to be a burglar"],
 "core": "Group words that are rearrangements of each other, and count the groups.",
 "gloss": [("bow", "the loop at the top of a key", True), ("kin", "relatives", True),
           ("stamped", "pressed in with a die", True), ("mnemonic", "something that helps you remember", True),
           ("ward", "the ridges inside a lock", True)],
 "why": {"hs-freq": "A tally counts one kind of thing; here the thing counted is a family, and you must first invent a label shared by every member.",
         "tr-basic": "A prefix tree is for words that share beginnings; rearrangements share letters, not beginnings."},
 "tell": "Group by rearrangement; the trick is the key you give each item."},

{"id": "sc-025", "v": "hs-cyclic", "dom": "fairground", "diff": "H",
 "title": "The Bruges Raffle Drum",
 "story": "The Bruges fair runs for eleven days in May and ends with a raffle whose prize, by tradition, is a "
          "live goose. The raffle drum at the Bruges fair holds N tickets, each printed with a number from 1 to "
          "N, which is how the printer was instructed and how it has always been done, one ticket for each "
          "number and no number left out.\n\n"
          "This year the printing went wrong. A fault in the press duplicated some numbers and therefore omitted "
          "others, so that the drum now holds N tickets as it should, but some numbers appear twice or more and "
          "the numbers they displaced appear not at all. The fault was not noticed until the drum was sealed, and "
          "the guild of mercers, which runs the raffle, has ruled that the drum may not be unsealed; it may only "
          "be emptied onto the steward's table and examined there.\n\n"
          "The steward must proclaim every number that never appears, in increasing order, so that anyone "
          "holding a ticket with such a number knows at once that it is a forgery and not merely unlucky. The "
          "steward's tally-board is tiny: apart from the tickets themselves, which he may freely rearrange, he "
          "may keep only a handful of notes. He has asked for a second board and been refused, the mercers "
          "having spent the year's budget on the bunting.\n\n"
          "The goose, meanwhile, is kept in a pen behind the weighhouse and has bitten two children. A "
          "fire-eater performs at dusk by the belfry and is thought by the guild to be a hazard. The fair's "
          "accounts have not balanced since 1544 and nobody expects them to.\n\n"
          "Input: line one gives N. Line two gives the N ticket numbers as they came out of the drum, in no "
          "order. Output: every number from 1 to N that does not appear, in increasing order, or the word NONE.\n\n"
          "Constraints: N up to 10^5; every ticket number lies between 1 and N. Extra memory must not grow with "
          "N, and the tickets themselves are the only working space available.",
 "clues": ["a number from 1 to N", "omitted others",
           "apart from the tickets themselves, which he may freely rearrange, he may keep only a handful of notes"],
 "decoys": ["at the Bruges fair", "The goose, meanwhile, is kept in a pen behind the weighhouse and has bitten two children",
            "The fair's accounts have not balanced since 1544"],
 "core": "The values are exactly 1 to N with some repeated; find those that are missing, using almost no extra memory.",
 "gloss": [("steward", "an attendant who manages arrangements", True), ("proclaim", "to announce publicly", True),
           ("omitted", "left out", True), ("duplicated", "copied so it appears twice", True),
           ("mercers", "dealers in fine cloth", True)],
 "why": {"hs-seen": "A set solves it but needs memory proportional to N, which the steward lacks.",
         "bt-xor": "That cancels pairs to find ONE odd item; here several numbers are missing and several duplicated."},
 "tell": "Every value lies between 1 and N, and spare memory is almost forbidden."},

{"id": "sc-026", "v": "ms-next", "dom": "ancient trackways", "diff": "M",
 "title": "The Ridgeway Cairns",
 "story": "The Ridgeway is the oldest road in Britain, a chalk track along the crest of the downs that was in "
          "use before the stone circles were raised, and a trust now maintains it. Along the Ridgeway, a "
          "surveyor has planted N cairns, cairn i rising h[i] metres, at intervals along the path from the "
          "eastern end to the western. They are numbered in that order, and the trust's register lists their "
          "heights in that order, east to west.\n\n"
          "The cairns are inspected each year by the waymarker, a cheerful fellow who whistles as he walks, and "
          "his report this year must answer a question the trust's surveyor has put to him. The surveyor wants to "
          "know, for every cairn on the path, the distance to the next cairn that actually stands out above it, "
          "because a cairn that is overtopped by nothing for miles is a cairn that sightseers will walk past "
          "without noticing. So the waymarker stands at the base of each cairn in turn and gazes westward along "
          "the path, wishing to learn how many cairns further on he must walk to reach one strictly taller than "
          "the cairn beside him. If the path ends first, he notes 0.\n\n"
          "The waymarker has pointed out that walking westward from every single cairn until he finds a taller "
          "one means walking the whole path again and again, and that on the long gentle descent from the barrow "
          "at Wayland's Smithy he would be walking almost to the end each time. The surveyor has told him to "
          "think of something better.\n\n"
          "The cairns are limewashed every spring. A trust volunteer has planted harebells at the eastern end "
          "against instructions. There is an argument with a farmer about a gate, as there always is, and the "
          "trust's solicitor has written a letter that has not been answered.\n\n"
          "Input: line one gives N. Line two gives the N cairn heights, east to west. Output: N numbers, for "
          "each cairn the number of cairns onward to the nearest strictly taller one, or 0 if there is none.\n\n"
          "Constraints: N up to 10^6; heights up to 10^9.",
 "clues": ["gazes westward along the path", "how many cairns further on he must walk",
           "strictly taller than the cairn beside him"],
 "decoys": ["a cheerful fellow who whistles as he walks", "limewashed every spring",
            "A trust volunteer has planted harebells at the eastern end against instructions"],
 "core": "For every item, how far along is the nearest strictly larger item on one side?",
 "gloss": [("cairn", "a pile of stones used as a marker", True), ("waymarker", "someone who marks a route", True),
           ("limewashed", "painted white with lime", True), ("barrow", "an ancient burial mound", True),
           ("strictly", "greater, not merely equal", True)],
 "why": {"sw-deque": "That needs the maximum of a fixed-width span; here no width is given, and the answer can be anywhere along the path.",
         "ms-hist": "That asks about an area; this asks only for a distance."},
 "tell": "For each item, the next bigger one on a chosen side, and how far away it is."},
]
