"""Aptitude questions, part B2 (logic): Syllogisms, Blood relations, Ages, Data sufficiency, Statement & conclusion, Odd one out, Seating."""
from apt_common import mk

Lg = "logic"
SYL = ["Only I follows", "Only II follows", "Both I and II follow", "Neither I nor II follows"]


def syl(statements, c1, c2, ans, why, tgt=60):
    q = f"Statements: {statements} Conclusions: I. {c1}  II. {c2}"
    right = SYL[ans]
    return mk(Lg, "Syllogisms", tgt, q, right, [o for o in SYL if o != right], why)


def syl_qs():
    L = []
    L.append(syl("All pens are books. All books are tables.", "All pens are tables.", "All tables are pens.", 0,
                 "All A are B and all B are C gives all A are C. The reverse never follows.", 45))
    L.append(syl("Some cats are dogs. All dogs are birds.", "Some cats are birds.", "All cats are birds.", 0,
                 "Some A are B plus all B are C gives some A are C. 'All cats' is too strong.", 45))
    L.append(syl("Some books are pens. Some pens are pencils.", "Some books are pencils.", "Some pencils are books.", 3,
                 "Two 'some' premises: nothing follows.", 45))
    L.append(syl("All fruits are sweet. Some sweet things are cold.", "Some fruits are cold.", "All cold things are sweet.", 3,
                 "The cold sweet things may be entirely outside the fruit circle, so neither is forced.", 60))
    L.append(syl("No stone is paper. All paper is glass.", "No stone is glass.", "Some glass is paper.", 1,
                 "All paper is glass, so some glass is paper. Stones may still be glass, so I fails.", 75))
    L.append(syl("All teachers are readers. No reader is lazy.", "No teacher is lazy.", "Some teachers are lazy.", 0,
                 "Teachers sit inside readers, which sit outside lazy. II contradicts that.", 60))
    L.append(syl("Some doctors are singers. All singers are tall.", "Some doctors are tall.", "All doctors are tall.", 0,
                 "The doctors who sing are tall, so some doctors are tall; 'all' is not forced.", 45))
    L.append(syl("All lions are animals.", "All animals are lions.", "Some animals are lions.", 1,
                 "'All A are B' never gives 'All B are A', but it does give 'Some B are A'.", 45))
    L.append(syl("No man is a bird. Some birds are fish.", "Some fish are not men.", "No fish is a man.", 0,
                 "The fish that are birds cannot be men, so some fish are not men. Other fish are unconstrained, so II fails.", 75))
    L.append(syl("Some roads are lanes. Some lanes are streets. All streets are paths.", "Some lanes are paths.", "Some roads are streets.", 0,
                 "Some lanes are streets and streets are paths: I follows. Roads and streets link only via 'some lanes', so II is not forced.", 75))
    L.append(syl("All metals are conductors. Some conductors are costly.", "Some metals are costly.", "All metals are costly.", 3,
                 "The costly conductors need not be metals.", 60))
    L.append(syl("All books are papers. All papers are leaves. No leaf is a stone.", "No book is a stone.", "Some stones are papers.", 0,
                 "Books ⊂ papers ⊂ leaves, and leaves exclude stones, so I follows and II is false.", 75))
    L.append(syl("Some flowers are red. All red things are bright.", "Some flowers are bright.", "All bright things are red.", 0,
                 "The red flowers are bright. The reverse is not given.", 45))
    L.append(syl("No cow is a horse. No horse is a goat.", "No cow is a goat.", "Some goats are cows.", 3,
                 "Two 'no' premises give nothing. Do not chain them.", 60))
    return L


def blood_qs():
    S = "Blood relations"
    L = []
    L.append(mk(Lg, S, 60, "A is B's sister. B is C's father. How is A related to C?", "Aunt", ["Mother", "Sister", "Grandmother"], "A is the sister of C's father: C's paternal aunt."))
    L.append(mk(Lg, S, 75, "Pointing to a girl, Ravi says, \"She is the daughter of my grandfather's only son.\" How is the girl related to Ravi?", "Sister",
                ["Cousin", "Mother", "Aunt"], "Grandfather's only son is Ravi's father; his daughter is Ravi's sister."))
    L.append(mk(Lg, S, 60, "What is the relation of the person who is 'my mother's only brother's son' to me?", "Cousin", ["Uncle", "Brother", "Nephew"],
                "Mother's brother is the maternal uncle; his son is a cousin."))
    L.append(mk(Lg, S, 60, "B is a man and the brother of A's mother. How is B related to A?", "Maternal uncle", ["Paternal uncle", "Father", "Grandfather"], "A's mother's brother is the maternal uncle."))
    L.append(mk(Lg, S, 75, "Pointing to a man, Sita says, \"His mother is the only daughter of my mother.\" How is the man related to Sita?", "Son", ["Brother", "Nephew", "Father"],
                "My mother's only daughter is Sita herself; his mother is Sita, so he is her son."))
    L.append(mk(Lg, S, 75, "A is the brother of B. B is the sister of C. C is the father of D. How is A related to D?", "Uncle", ["Father", "Brother", "Cousin"],
                "A, B and C are siblings; D is C's child, so A is D's uncle."))
    L.append(mk(Lg, S, 60, "X's father is Y's son. How is Y related to X?", "Grandfather", ["Father", "Uncle", "Great-grandfather"], "Y's son is X's father, so Y is X's grandfather."))
    L.append(mk(Lg, S, 60, "Who is 'my father's father's only son's wife'?", "Mother", ["Grandmother", "Aunt", "Sister"], "Father's father's only son is my father; his wife is my mother."))
    L.append(mk(Lg, S, 60, "Rahul is the son of Meena. Meena is the daughter of Kishan. How is Kishan related to Rahul?", "Maternal grandfather", ["Paternal grandfather", "Father", "Uncle"],
                "Kishan is the father of Rahul's mother."))
    L.append(mk(Lg, S, 75, "A man says, \"Her mother is the only daughter of my mother.\" How is the lady related to him?", "Niece", ["Sister", "Daughter", "Cousin"],
                "My mother's only daughter is my sister; her daughter is my niece."))
    L.append(mk(Lg, S, 75, "A is B's brother. C is A's mother. D is C's father. E is D's mother. How is B related to D?", "Grandchild", ["Child", "Great-grandchild", "Nephew"],
                "B's mother C is D's child, so B is D's grandchild."))
    L.append(mk(Lg, S, 75, "A and B are a married couple, A is male. C is B's brother and D is C's father. How is A related to D?", "Son-in-law", ["Son", "Brother-in-law", "Nephew"],
                "D is B's father, so A (B's husband) is D's son-in-law."))
    L.append(mk(Lg, S, 75, "P is the brother of Q. Q is the mother of R. S is R's father. How is P related to S?", "Brother-in-law", ["Brother", "Uncle", "Father-in-law"],
                "Q is S's wife; P is her brother, hence S's brother-in-law."))
    L.append(mk(Lg, S, 60, "A is the mother of B. B is the father of C. C is the sister of D. How is A related to D?", "Grandmother", ["Mother", "Aunt", "Sister"],
                "D's father is B, whose mother is A."))
    L.append(mk(Lg, S, 45, "A is B's mother. B is C's sister. How is A related to C?", "Mother", ["Aunt", "Grandmother", "Sister"], "Siblings share parents."))
    return L


def age_qs():
    S = "Ages"
    L = []
    L.append(mk(Lg, S, 75, "A father is 3 times as old as his son. In 12 years he will be twice as old. What is the son's present age?", 12, [10, 14, 8],
                "3x + 12 = 2(x + 12) gives x = 12."))
    L.append(mk(Lg, S, 75, "The sum of A's and B's ages is 40. Five years ago A was twice as old as B. What is A's present age?", 25, [20, 30, 28],
                "A = 2B − 5 and A + B = 40 give 3B = 45, B = 15, A = 25."))
    L.append(mk(Lg, S, 75, "The ages of two people are in the ratio 4:5. After 5 years the ratio is 5:6. What is the elder's present age?", 25, [20, 30, 24],
                "(4k + 5)/(5k + 5) = 5/6 gives k = 5; elder = 25."))
    L.append(mk(Lg, S, 75, "A father is 30 years older than his son. After 5 years he will be 3 times as old. What is the son's present age?", 10, [8, 12, 15],
                "S + 35 = 3(S + 5) gives S = 10."))
    L.append(mk(Lg, S, 60, "The average age of A, B and C is 30. B and C average 33. What is A's age?", 24, [27, 30, 21], "Total 90, B + C = 66, so A = 24."))
    L.append(mk(Lg, S, 75, "A mother is 24 years older than her son. In 8 years she will be 3 times as old as him. What is the son's present age?", 4, [6, 8, 5],
                "S + 32 = 3(S + 8) gives S = 4."))
    L.append(mk(Lg, S, 75, "The sum of a father's and son's ages is 56. Four years ago the father was 3 times the son's age. What is the father's present age?", 40, [36, 42, 38],
                "F = 3S − 8 and F + S = 56 give S = 16, F = 40."))
    L.append(mk(Lg, S, 75, "Ten years ago A was half of A's age 10 years from now. What is A's present age?", 30, [20, 25, 40], "A − 10 = (A + 10)/2 gives A = 30."))
    L.append(mk(Lg, S, 60, "The ages of A and B are in the ratio 3:5 and sum to 40. What is the difference of their ages?", 10, [8, 15, 12], "Parts: 15 and 25. Difference 10."))
    L.append(mk(Lg, S, 75, "Ramu is 4 times as old as Shyam. After 6 years Ramu will be 2.5 times as old as Shyam. What is Ramu's present age?", 24, [20, 28, 32],
                "4S + 6 = 2.5(S + 6) gives S = 6, so Ramu = 24."))
    L.append(mk(Lg, S, 60, "A is 8 years older than B. In 4 years the sum of their ages will be 48. What is B's present age?", 16, [18, 20, 14],
                "A + B = 40 now; B = 16, A = 24."))
    L.append(mk(Lg, S, 45, "A is 6 years older than B. What is the difference of their ages after 10 years?", 6, [16, 10, 4], "The age difference never changes."))
    L.append(mk(Lg, S, 60, "Five years ago a boy was one-third of his father's age then. The father is 38 now. What is the boy's age now?", 16, [11, 14, 15],
                "Father then was 33, boy then 11, boy now 16."))
    return L


DS = ["Statement I alone is sufficient", "Statement II alone is sufficient", "Both together are needed",
      "Either statement alone is sufficient", "Even both together are not sufficient"]


def ds(q, i, ii, ans, why, tgt=75):
    full = f"{q} (I) {i} (II) {ii}"
    right = DS[ans]
    pool = [o for o in DS if o != right]
    return mk(Lg, "Data sufficiency", tgt, full, right, pool, why)


def ds_qs():
    L = []
    L.append(ds("What is the price of one pen?", "3 pens and 2 pencils cost ₹40.", "A pencil costs ₹5.", 2, "I alone has two unknowns; II gives pencil = 5, so 3p + 10 = 40 and p = 10. Both are needed."))
    L.append(ds("What is the value of x?", "x² = 9.", "x > 0.", 2, "I gives ±3. II removes the negative. Both together give x = 3."))
    L.append(ds("Is Priya taller than Riya?", "Priya is taller than Sana.", "Sana is taller than Riya.", 2, "Only the chain Priya > Sana > Riya settles it."))
    L.append(ds("What is the area of a square?", "The perimeter is 20 cm.", "The diagonal is 5√2 cm.", 3, "Either gives side 5, area 25. Each alone is sufficient."))
    L.append(ds("What is the speed of the train?", "It covers 120 km.", "It takes 2 hours.", 2, "Speed = distance/time needs both."))
    L.append(ds("What day is it today?", "The day after tomorrow is Friday.", "Yesterday was Tuesday.", 3, "Both fix today as Wednesday."))
    L.append(ds("How many students are in the class?", "40% are girls.", "24 are boys.", 2, "Boys are 60% = 24, so total 40. Needs both."))
    L.append(ds("Is x even?", "x is divisible by 4.", "x is a multiple of 3.", 0, "Every multiple of 4 is even. II alone can be odd or even."))
    L.append(ds("What is the cost price of an article?", "The profit is 20%.", "The selling price is ₹600.", 2, "CP = 600/1.2 = 500, using both."))
    L.append(ds("How old is Raj?", "Raj is 5 years older than Sam.", "Sam is 5 years older than Tina.", 4, "Only relative differences; no age is pinned."))
    L.append(ds("What is the average of three numbers?", "Their sum is 45.", "The largest is 20.", 0, "Average = sum/count = 15 from I alone."))
    L.append(ds("What is the HCF of a and b?", "a × b = 360.", "LCM(a, b) = 60.", 2, "HCF = product/LCM = 6, needs both."))
    L.append(ds("In how many days can A alone finish the job?", "A and B together finish it in 6 days.", "B alone finishes it in 10 days.", 2, "1/6 − 1/10 = 1/15 → 15 days. Both are needed."))
    L.append(ds("Is n positive?", "n² = 16.", "n + 3 > 0.", 2, "I gives ±4; II rules out −4 (−1 is not > 0). Both together give n = 4."))
    L.append(ds("What is the length of the rectangle?", "Its area is 48 cm².", "Its breadth is 6 cm.", 2, "Length = 48/6 = 8; one statement alone leaves two unknowns."))
    L.append(ds("Who is the tallest of A, B and C?", "A is taller than B.", "C is shorter than A.", 2, "Together: A is taller than B and taller than C, so A is the tallest. Each alone leaves one comparison open.", 75))
    return L


def stmt_qs():
    S = "Statement & conclusion"
    L = []
    L.append(mk(Lg, S, 60, "Statement: The government has banned plastic bags in the city. Which assumption is implicit?", "Plastic bags are considered harmful",
                ["Paper bags are cheaper", "Every citizen will obey the ban", "Other cities will follow"], "A ban only makes sense if the thing banned is seen as harmful. The rest add outside claims."))
    L.append(mk(Lg, S, 60, "Statement: 'Wear a helmet; it can save your life.' Which assumption is implicit?", "People value their lives",
                ["Helmets are cheap", "Accidents are always fatal", "Helmets are fashionable"], "The advice persuades only if the reader cares about survival."))
    L.append(mk(Lg, S, 60, "Statement: Students must submit assignments online from next month. Which assumption is implicit?", "Students have access to the internet",
                ["Teachers dislike paper", "Online assignments score higher", "All students own laptops"], "The rule is workable only if students can get online. Owning a laptop is too specific."))
    L.append(mk(Lg, S, 60, "Statement: 'Mobile phones must be switched off in the library.' Which assumption is implicit?", "Phones can disturb readers",
                ["Libraries have no signal", "Phones are banned everywhere", "Readers dislike technology"], "The rule exists because phones cause disturbance."))
    L.append(mk(Lg, S, 75, "Statement: A shop announced a 10% discount on bulk orders. Which assumption is implicit?", "Discounts attract bulk buyers",
                ["Competitors give no discount", "Prices were too high earlier", "Bulk buyers need no discount"], "The offer makes sense only if discounts draw such buyers."))
    L.append(mk(Lg, S, 75, "Statement: All students who scored above 90% got scholarships. Ravi got a scholarship. Conclusion: Ravi scored above 90%.", "Cannot be determined",
                ["Definitely true", "Definitely false", "Follows from statement"], "The rule goes one way. Ravi may have qualified another way."))
    L.append(mk(Lg, S, 60, "Statement: Some employees of Firm X work from home. Conclusion: All employees of Firm X work in the office.", "Definitely false",
                ["Definitely true", "Cannot be determined", "Probably true"], "If some work from home, it cannot be that all work in the office."))
    L.append(mk(Lg, S, 60, "Statement: Rain is forecast for tomorrow. Conclusion: Tomorrow's cricket match will be cancelled.", "Does not follow",
                ["Follows", "Definitely true", "Follows partly"], "Cancellation is an outside inference; the statement says nothing about the match."))
    L.append(mk(Lg, S, 75, "Statement: A hotel advertises, 'Stay with us for the best view of the city.' Which assumption is implicit?", "Guests value a good view",
                ["Other hotels are cheaper", "The hotel is full", "Guests come only for the view"], "The ad persuades only if a good view matters to guests."))
    L.append(mk(Lg, S, 60, "Statement: Only those with ID cards are allowed inside the premises. Conclusion: Anyone inside has an ID card.", "Follows",
                ["Does not follow", "Definitely false", "Cannot be determined"], "Entry requires an ID card, so everyone inside must hold one."))
    L.append(mk(Lg, S, 75, "Statement: The price of tomatoes rose sharply last month due to heavy rain. Conclusion: Heavy rain affected the supply of tomatoes.", "Follows",
                ["Does not follow", "Definitely false", "Cannot be determined"], "The statement itself links the rain to the price rise through supply."))
    L.append(mk(Lg, S, 60, "Statement: 'Buy a ticket early to get a cheaper fare.' Which assumption is implicit?", "Fares rise as the date approaches",
                ["All seats will be sold out", "Late tickets are unavailable", "Airlines lose money otherwise"], "The advice assumes early buying actually saves money."))
    return L


def odd_qs():
    S = "Odd one out"
    L = []
    L.append(mk(Lg, S, 45, "Which does not belong: 3, 5, 7, 9, 11?", 9, [3, 7, 11], "All others are prime; 9 = 3²."))
    L.append(mk(Lg, S, 45, "Which does not belong: 16, 25, 36, 49, 50?", 50, [16, 36, 49], "The rest are perfect squares."))
    L.append(mk(Lg, S, 45, "Which does not belong: Apple, Mango, Potato, Banana, Grape?", "Potato", ["Mango", "Grape", "Banana"], "The rest are fruits; a potato is a vegetable."))
    L.append(mk(Lg, S, 45, "Which does not belong: 121, 144, 169, 196, 200?", 200, [121, 169, 196], "Squares of 11–14; 200 is not a square."))
    L.append(mk(Lg, S, 45, "Which does not belong: 12, 18, 24, 30, 35?", 35, [12, 24, 30], "Multiples of 6 except 35."))
    L.append(mk(Lg, S, 45, "Which does not belong: 8, 27, 64, 125, 150?", 150, [8, 64, 125], "Cubes of 2, 3, 4, 5."))
    L.append(mk(Lg, S, 60, "Which does not belong: 41, 43, 47, 51, 53?", 51, [41, 47, 53], "51 = 3 × 17; the rest are prime."))
    L.append(mk(Lg, S, 60, "Which does not belong: 18, 27, 36, 45, 52?", 52, [18, 36, 45], "The rest have a digit sum of 9."))
    L.append(mk(Lg, S, 45, "Which does not belong: 14, 21, 28, 35, 40?", 40, [14, 28, 35], "Multiples of 7."))
    L.append(mk(Lg, S, 45, "Which does not belong: 2, 4, 8, 16, 18?", 18, [4, 8, 16], "Powers of 2."))
    L.append(mk(Lg, S, 45, "Which does not belong: Lion, Tiger, Leopard, Cow, Cheetah?", "Cow", ["Lion", "Tiger", "Cheetah"], "The rest are big cats."))
    L.append(mk(Lg, S, 60, "Which does not belong: 1, 8, 27, 64, 100?", 100, [1, 27, 64], "Perfect cubes, except 100."))
    L.append(mk(Lg, S, 45, "Which does not belong: Delhi, Mumbai, Chennai, Kolkata, Nile?", "Nile", ["Delhi", "Chennai", "Kolkata"], "The rest are cities."))
    L.append(mk(Lg, S, 60, "Which does not belong: 6, 28, 496, 100?", 100, [6, 28, 496], "6, 28, 496 are perfect numbers."))
    return L


def seat_qs():
    S = "Seating"
    L = []
    L.append(mk(Lg, S, 90, "Five people sit in a row. A is at the left end; C sits immediately right of A; E is at the right end; B is to the left of D. Who sits in the middle?", "B",
                ["A", "C", "D"], "Order: A, C, B, D, E."))
    L.append(mk(Lg, S, 75, "Four friends A, B, C, D sit around a square table facing the centre. A is opposite C, and B is on A's left. Who is on A's right?", "D",
                ["B", "C", "Cannot be determined"], "B is left, C is opposite, so D must be on the right."))
    L.append(mk(Lg, S, 75, "In a row of 9, P sits third from the left and Q sits fourth from the right. How many people are between them?", 2, [1, 3, 4],
                "Q is 6th from the left; between = 6 − 3 − 1 = 2."))
    L.append(mk(Lg, S, 75, "In a row, A is left of B and right of C. D is right of B and left of E. Who is in the middle?", "B", ["A", "D", "C"], "Order: C, A, B, D, E."))
    L.append(mk(Lg, S, 60, "X is 7th from the left and 9th from the right in a row. How many people are in the row?", 15, [16, 14, 17], "7 + 9 − 1 = 15."))
    L.append(mk(Lg, S, 75, "In a row facing north, M is to the immediate right of N and O is to the immediate left of N. Who is at the extreme left of the three?", "O",
                ["N", "M", "Cannot be determined"], "Left to right: O, N, M."))
    L.append(mk(Lg, S, 75, "Seats are numbered 1–8 in a row. P sits at 3, Q two seats to the right of P and R immediately left of Q. Who sits between P and Q?", "R",
                ["Nobody", "Q", "S"], "P at 3, Q at 5, R at 4."))
    L.append(mk(Lg, S, 75, "Six people A–F sit in a row. A is immediately left of B; F is at the right end; C is left of A; D is right of B; E is between D and F. Who is at the left end?", "C",
                ["A", "B", "D"], "Order: C, A, B, D, E, F."))
    return L


def build():
    return syl_qs() + blood_qs() + age_qs() + ds_qs() + stmt_qs() + odd_qs() + seat_qs()


if __name__ == "__main__":
    print(len(build()))
