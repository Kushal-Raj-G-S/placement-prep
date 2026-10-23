"""Aptitude questions, part A2: Permutations, Combinations, Probability, Number system, Progressions, Data interpretation."""
from fractions import Fraction as Fr
from math import comb, factorial as f, perm, gcd, isqrt
from apt_common import mk, fmt

Qn = "quant"


def perm_qs():
    S = "Permutations"
    L = []
    L.append(mk(Qn, S, 45, "In how many ways can 3 distinct prizes be given to 5 contestants (one each)?", perm(5, 3),
                [comb(5, 3), 125, 120], "Order matters: 5P3 = 5 × 4 × 3 = 60."))
    L.append(mk(Qn, S, 60, "How many distinct arrangements are there of the letters of LEVEL?", f(5) // (f(2) * f(2)),
                [f(5), f(5) // f(2), 15], "Two Ls and two Es repeat: 5!/(2!·2!) = 30."))
    L.append(mk(Qn, S, 45, "In how many ways can 6 people sit around a circular table?", f(5), [f(6), 60, 24],
                "Circular arrangements of n = (n − 1)! = 5! = 120."))
    L.append(mk(Qn, S, 60, "4 boys and 3 girls stand in a row with the girls always together. How many arrangements?", f(5) * f(3),
                [f(7), f(4) * f(3), 1440], "Glue the girls into one block: 5 units → 5!, girls inside → 3!. 120 × 6 = 720."))
    L.append(mk(Qn, S, 45, "How many 3-digit numbers can be made from the digits 1–5 with no digit repeated?", 60, [125, 120, 10],
                "5P3 = 60."))
    L.append(mk(Qn, S, 60, "How many even 3-digit numbers can be formed from 1, 2, 3, 4, 5 without repetition?", 24, [30, 36, 60],
                "Fix the units digit first: 2 or 4 (2 ways). The other two places: 4 × 3 = 12. 2 × 12 = 24."))
    L.append(mk(Qn, S, 60, "In how many ways can the letters of TOMATO be arranged?", f(6) // (f(2) * f(2)),
                [f(6) // f(2), 720, 90], "T and O each appear twice: 6!/(2!·2!) = 180."))
    L.append(mk(Qn, S, 75, "How many distinct arrangements are there of the letters of MISSISSIPPI?", f(11) // (f(4) * f(4) * f(2)),
                [f(11) // (f(4) * f(4)), f(11) // (f(4) * f(2)), f(11)], "I×4, S×4, P×2: 11!/(4!·4!·2!) = 34650."))
    L.append(mk(Qn, S, 60, "How many distinct arrangements are there of the letters of BANANA?", 60, [120, 720, 30],
                "A×3, N×2: 6!/(3!·2!) = 60."))
    L.append(mk(Qn, S, 75, "7 people sit around a circular table, two particular people always sitting together. How many arrangements?", f(5) * 2,
                [f(6), f(5), 1440], "Glue the pair: 6 units around a circle → 5!; pair can swap → ×2 = 240."))
    L.append(mk(Qn, S, 75, "In the word EQUATION all vowels stay together. How many arrangements are there?", f(4) * f(5),
                [f(8), f(5) * f(3), 5040], "Five vowels glued as one block: 4 units → 4! = 24; vowels inside 5! = 120. 24 × 120 = 2880."))
    L.append(mk(Qn, S, 45, "How many 4-digit PINs can be made from the digits 0–9 with no digit repeated?", perm(10, 4),
                [10 ** 4, comb(10, 4), 9 * perm(9, 3)], "10P4 = 10 × 9 × 8 × 7 = 5040. (PINs may start with 0.)"))
    L.append(mk(Qn, S, 90, "5 men and 3 women stand in a row so that no two women are together. How many arrangements?", f(5) * perm(6, 3),
                [f(8), f(5) * f(3), 7200], "Seat the men: 5! = 120. This creates 6 gaps; women choose gaps in order: 6P3 = 120. Product 14400."))
    L.append(mk(Qn, S, 45, "How many 2-letter codes can be formed from the letters A, B, C, D, E with no repeated letter?", 20, [25, 10, 120],
                "5P2 = 20."))
    return L


def comb_qs():
    S = "Combinations"
    L = []
    L.append(mk(Qn, S, 45, "In how many ways can a team of 3 be chosen from 8 people?", comb(8, 3), [perm(8, 3), 24, 28], "8C3 = 56."))
    L.append(mk(Qn, S, 60, "A committee of 3 is to be formed from 6 men and 4 women with at least one woman. How many ways?", comb(10, 3) - comb(6, 3),
                [comb(4, 1) * comb(9, 2), 120, 80], "At least one = total − none: 10C3 − 6C3 = 120 − 20 = 100."))
    L.append(mk(Qn, S, 45, "12 people each shake hands once with every other person. How many handshakes?", comb(12, 2), [132, 144, 78], "12C2 = 66."))
    L.append(mk(Qn, S, 60, "How many diagonals does an octagon have?", comb(8, 2) - 8, [28, 24, 16], "nC2 − n = 28 − 8 = 20."))
    L.append(mk(Qn, S, 45, "How many lines can be drawn through 7 points, no three collinear?", 21, [42, 35, 14], "7C2 = 21."))
    L.append(mk(Qn, S, 60, "How many triangles can be formed from 7 points, no three collinear?", 35, [21, 42, 210], "7C3 = 35."))
    L.append(mk(Qn, S, 60, "Choose 2 men from 5 and 3 women from 6. How many selections?", comb(5, 2) * comb(6, 3),
                [comb(11, 5), 150, 300], "5C2 × 6C3 = 10 × 20 = 200. 'AND' means multiply."))
    L.append(mk(Qn, S, 75, "10 points lie in a plane, 4 of them collinear and no other three collinear. How many triangles?", comb(10, 3) - comb(4, 3),
                [comb(10, 3), 112, 100], "10C3 − 4C3 = 120 − 4 = 116."))
    L.append(mk(Qn, S, 45, "8 teams play a round-robin where every pair meets once. How many matches?", 28, [56, 16, 36], "8C2 = 28."))
    L.append(mk(Qn, S, 60, "In how many ways can 4 be chosen from 9 people if two particular people must be included?", comb(7, 2),
                [comb(9, 4), comb(7, 4), 35], "Fix the two; choose the remaining 2 from 7: 7C2 = 21."))
    L.append(mk(Qn, S, 45, "A cricket squad of 14 players must provide an XI. How many different XIs are possible?", comb(14, 11),
                [comb(14, 3) + 1, 3003, 2002], "14C11 = 14C3 = 364."))
    L.append(mk(Qn, S, 60, "An exam asks you to answer any 6 of 8 questions, but the first two are compulsory. How many ways?", comb(6, 4),
                [comb(8, 6), 28, 20], "Two fixed, choose the remaining 4 from 6: 6C4 = 15."))
    L.append(mk(Qn, S, 75, "How many parallelograms are formed when 4 parallel lines cut 3 other parallel lines?", comb(4, 2) * comb(3, 2),
                [12, 24, 7], "Choose 2 of each family: 4C2 × 3C2 = 6 × 3 = 18."))
    L.append(mk(Qn, S, 60, "From 5 consonants and 3 vowels, how many 5-letter groups have exactly 2 vowels (selection only)?", comb(3, 2) * comb(5, 3),
                [comb(8, 5), 56, 15], "3C2 × 5C3 = 3 × 10 = 30."))
    L.append(mk(Qn, S, 45, "What is the value of 10C8?", 45, [90, 80, 10], "10C8 = 10C2 = 45."))
    return L


def prob_qs():
    S = "Probability"
    L = []
    L.append(mk(Qn, S, 45, "A fair coin is tossed 3 times. What is the probability of exactly 2 heads?", "3/8", ["1/4", "1/2", "1/8"],
                "3C2 = 3 favourable out of 8 outcomes."))
    L.append(mk(Qn, S, 45, "Two dice are thrown. What is the probability that the sum is 8?", "5/36", ["1/6", "1/9", "7/36"],
                "(2,6),(3,5),(4,4),(5,3),(6,2) = 5 of 36."))
    L.append(mk(Qn, S, 45, "A card is drawn from a standard deck. What is the probability it is a red face card?", "3/26", ["3/13", "1/13", "6/13"],
                "6 red face cards out of 52 = 3/26."))
    L.append(mk(Qn, S, 45, "A bag holds 5 red, 3 blue and 2 green balls. One is drawn. P(green) =", "1/5", ["1/10", "2/5", "3/10"], "2/10 = 1/5."))
    L.append(mk(Qn, S, 60, "Two cards are drawn without replacement. What is the probability both are aces?", "1/221", ["1/169", "1/52", "4/663"],
                "4/52 × 3/51 = 12/2652 = 1/221."))
    L.append(mk(Qn, S, 45, "A coin is tossed 3 times. What is the probability of at least one head?", "7/8", ["3/4", "1/8", "1/2"],
                "At least one = 1 − none = 1 − 1/8."))
    L.append(mk(Qn, S, 45, "P(A) = 0.4, P(B) = 0.5, P(A and B) = 0.2. What is P(A or B)?", "0.7", ["0.9", "0.6", "0.8"],
                "0.4 + 0.5 − 0.2 = 0.7. Subtract the overlap."))
    L.append(mk(Qn, S, 60, "A bag has 4 red and 6 blue balls. Two are drawn at once. P(both red) =", "2/15", ["4/25", "1/5", "6/25"],
                "4C2/10C2 = 6/45 = 2/15."))
    L.append(mk(Qn, S, 45, "A die is rolled once. What is the probability of a prime?", "1/2", ["1/3", "2/3", "5/6"], "2, 3, 5 = 3 of 6."))
    L.append(mk(Qn, S, 60, "A die is rolled. What is the probability of an even number or a number greater than 4?", "2/3", ["1/2", "5/6", "1/3"],
                "{2, 4, 6, 5} = 4 of 6; 6 is counted once (subtract the overlap)."))
    L.append(mk(Qn, S, 60, "Two dice are thrown. What is the probability that at least one shows a six?", "11/36", ["1/3", "1/6", "5/36"],
                "1 − (5/6)² = 11/36."))
    L.append(mk(Qn, S, 75, "A solves a problem with probability 1/3 and B with 1/4, independently. What is the probability it gets solved?", "1/2",
                ["7/12", "1/12", "5/12"], "1 − (2/3)(3/4) = 1 − 1/2 = 1/2."))
    L.append(mk(Qn, S, 45, "Two dice are thrown. What is the probability that the sum is 7?", "1/6", ["1/12", "5/36", "7/36"], "6 of 36 outcomes."))
    L.append(mk(Qn, S, 60, "A card is drawn from a deck. What is the probability it is a king or a heart?", "4/13", ["17/52", "1/4", "5/13"],
                "4 + 13 − 1 = 16 cards: 16/52 = 4/13."))
    L.append(mk(Qn, S, 60, "A coin is tossed 4 times. What is the probability of exactly 2 heads?", "3/8", ["1/4", "1/2", "5/16"], "4C2/16 = 6/16 = 3/8."))
    return L


def ns_qs():
    S = "Number system"
    L = []
    L.append(mk(Qn, S, 45, "What is the HCF of 36 and 48?", 12, [6, 24, 4], "36 = 2²·3², 48 = 2⁴·3. Lowest powers: 2²·3 = 12."))
    L.append(mk(Qn, S, 45, "What is the LCM of 36 and 48?", 144, [72, 288, 12], "Highest powers: 2⁴·3² = 144."))
    L.append(mk(Qn, S, 60, "HCF = 6, LCM = 180 and one number is 30. What is the other?", 36, [30, 60, 18], "Product = HCF × LCM = 1080; 1080/30 = 36."))
    L.append(mk(Qn, S, 60, "What is the smallest number that leaves remainder 3 when divided by 8, 12 and 20?", 123, [120, 243, 63],
                "LCM(8, 12, 20) = 120; answer LCM + r = 123."))
    L.append(mk(Qn, S, 45, "What is the unit digit of 7⁴³?", 3, [7, 9, 1], "43 mod 4 = 3; 7³ = 343 ends in 3."))
    L.append(mk(Qn, S, 45, "What is the unit digit of 3⁵⁸?", 9, [3, 1, 7], "58 mod 4 = 2; 3² = 9."))
    L.append(mk(Qn, S, 45, "What is the unit digit of 4⁵⁷?", 4, [6, 2, 8], "Powers of 4 alternate 4, 6. Odd exponent → 4."))
    L.append(mk(Qn, S, 45, "How many trailing zeros does 100! have?", 24, [20, 25, 22], "⌊100/5⌋ + ⌊100/25⌋ = 20 + 4 = 24."))
    L.append(mk(Qn, S, 60, "How many trailing zeros does 130! have?", 130 // 5 + 130 // 25 + 130 // 125, [26, 30, 25],
                "26 + 5 + 1 = 32."))
    L.append(mk(Qn, S, 60, "What is the greatest number that divides 60, 84 and 108 exactly?", 12, [6, 24, 4], "HCF of the three = 12."))
    L.append(mk(Qn, S, 75, "What is the greatest number that divides 100 and 160 leaving remainders 4 and 7 respectively?", 3, [6, 12, 9],
                "Divisor divides 96 and 153. HCF(96, 153) = 3."))
    L.append(mk(Qn, S, 60, "How many factors does 72 have?", 12, [9, 10, 8], "72 = 2³·3²: (3+1)(2+1) = 12."))
    L.append(mk(Qn, S, 60, "How many factors does 360 have?", 24, [18, 20, 30], "360 = 2³·3²·5: 4 × 3 × 2 = 24."))
    L.append(mk(Qn, S, 45, "What is the largest 4-digit number divisible by 12?", 9996, [9999, 9992, 9984], "9999 mod 12 = 3 → 9996."))
    L.append(mk(Qn, S, 45, "What is the largest 3-digit number divisible by 17?", 986, [999, 969, 982], "999 mod 17 = 13 → 999 − 13 = 986."))
    L.append(mk(Qn, S, 60, "Three bells toll at intervals of 6, 8 and 12 minutes. After how many minutes will they toll together again?", 24, [12, 48, 36],
                "LCM(6, 8, 12) = 24."))
    L.append(mk(Qn, S, 45, "What is the smallest number to be added to 1000 to make it divisible by 7?", 1, [2, 6, 7], "1000 = 7×142 + 6, so add 1."))
    return L


def prog_qs():
    S = "Progressions"
    L = []
    L.append(mk(Qn, S, 45, "What is the 5th term of the AP 3, 7, 11, …?", 19, [15, 23, 17], "a + 4d = 3 + 16 = 19."))
    L.append(mk(Qn, S, 60, "What is the sum of the first 20 terms of the AP 2, 5, 8, …?", 610, [600, 620, 590],
                "n/2 [2a + (n − 1)d] = 10 × (4 + 57) = 610."))
    L.append(mk(Qn, S, 45, "What is 1 + 2 + 3 + … + 50?", 1275, [1250, 1300, 1225], "n(n + 1)/2 = 50 × 51/2 = 1275."))
    L.append(mk(Qn, S, 45, "What is the sum of the first 15 odd numbers?", 225, [240, 210, 255], "First n odd numbers sum to n² = 225."))
    L.append(mk(Qn, S, 45, "What is the sum of the first 10 even numbers?", 110, [100, 120, 90], "n(n + 1) = 10 × 11 = 110."))
    L.append(mk(Qn, S, 60, "What is the 6th term of the GP 2, 6, 18, …?", 486, [162, 1458, 324], "a r^(n−1) = 2 × 3⁵ = 486."))
    L.append(mk(Qn, S, 60, "What is the sum of the first 6 terms of the GP 3, 6, 12, …?", 189, [192, 126, 93], "a(rⁿ − 1)/(r − 1) = 3 × 63 = 189."))
    L.append(mk(Qn, S, 60, "What is the sum to infinity of 12, 4, 4/3, …?", 18, [16, 24, 15], "a/(1 − r) = 12/(2/3) = 18."))
    L.append(mk(Qn, S, 60, "How many terms are in the AP 7, 11, 15, …, 99?", 24, [23, 25, 22], "n = (last − first)/d + 1 = 92/4 + 1 = 24."))
    L.append(mk(Qn, S, 60, "What is the sum of the squares 1² + 2² + … + 10²?", 385, [330, 440, 385 + 55], "n(n + 1)(2n + 1)/6 = 10 × 11 × 21/6 = 385."))
    L.append(mk(Qn, S, 60, "What is the sum of the cubes 1³ + 2³ + … + 8³?", 1296, [1024, 1156, 1600], "[n(n + 1)/2]² = 36² = 1296."))
    L.append(mk(Qn, S, 75, "In an AP the 3rd term is 11 and the 7th is 27. What is the 10th term?", 39, [35, 43, 41],
                "d = (27 − 11)/4 = 4; a = 3; 10th = 3 + 36 = 39."))
    L.append(mk(Qn, S, 60, "What is the sum of all multiples of 7 from 1 to 100?", 735, [700, 770, 686], "7 × (1 + … + 14) = 7 × 105 = 735."))
    L.append(mk(Qn, S, 75, "A GP has first term 5 and common ratio 2. Which term is 320?", 7, [6, 8, 9], "5 × 2^(n−1) = 320 → 2^(n−1) = 64 → n = 7."))
    L.append(mk(Qn, S, 75, "The sum of the first n terms of an AP is n(n + 2). What is the 10th term?", 21, [20, 24, 22],
                "T₁₀ = S₁₀ − S₉ = 120 − 99 = 21."))
    return L


def di_qs():
    S = "Data interpretation"
    L = []
    L.append(mk(Qn, S, 60, "Sales were ₹200 in January and ₹250 in February. What is the percentage growth?", "25%", ["20%", "50%", "30%"],
                "Growth is on the PREVIOUS value: 50/200 = 25%."))
    L.append(mk(Qn, S, 60, "Revenue fell from ₹400 to ₹300. What is the percentage decline?", "25%", ["33.33%", "20%", "100%"], "100/400 = 25%."))
    L.append(mk(Qn, S, 60, "A product's market share rose from 20% to 25%. By how many percentage points, and by what percentage growth?", "5 points, 25%",
                ["5%, 5%", "25 points, 5%", "5 points, 20%"], "Points are subtracted (5). Growth = 5/20 = 25%."))
    L.append(mk(Qn, S, 75, "A company's profit was 120 (2019), 150 (2020), 180 (2021). Which year's growth rate was higher?", "2020 (25% vs 20%)",
                ["2021 (30 vs 30)", "2021 (20% vs 25%)", "Both equal"], "Both rises are 30, but 30/120 = 25% beats 30/150 = 20%."))
    L.append(mk(Qn, S, 45, "Production over five years was 40, 50, 60, 70, 80 units. What was the mean annual production?", 60, [55, 65, 50], "Sum 300 / 5 = 60."))
    L.append(mk(Qn, S, 45, "In a household budget pie chart, rent takes 25%. What angle does the rent sector subtend?", "90°", ["72°", "100°", "45°"], "25% of 360° = 90°."))
    L.append(mk(Qn, S, 45, "Sales were 450 in 2021 and 540 in 2022. The percentage growth is", "20%", ["16.67%", "18%", "25%"], "90/450 = 20%."))
    L.append(mk(Qn, S, 60, "Three branches sold 240, 320 and 440 units. What share of the total did the second branch have?", "32%", ["30%", "36%", "40%"], "320/1000 = 32%."))
    L.append(mk(Qn, S, 45, "A student scored 45 out of 60 in Physics. What percentage is that?", "75%", ["70%", "80%", "72%"], "45/60 = 0.75."))
    L.append(mk(Qn, S, 60, "Output in year X was 20% higher than in year Y, and Y was 250. What was X?", 300, [270, 275, 320], "250 × 1.2 = 300."))
    L.append(mk(Qn, S, 75, "A town of 50,000 grows 10% each year. What is its population after 2 years?", 60500, [60000, 61000, 55000],
                "Compound: 50000 × 1.1 × 1.1 = 60500."))
    L.append(mk(Qn, S, 75, "Exports were 80, 100, 90 (in crore) over three years. What was the percentage change from the 2nd to the 3rd year?", "10% fall",
                ["10% rise", "11.11% fall", "12.5% fall"], "(90 − 100)/100 = −10%. Base is the previous year (100)."))
    L.append(mk(Qn, S, 60, "In a pie chart totalling ₹1200, one sector is 72°. What value does it represent (₹)?", 240, [200, 300, 180], "72/360 = 20% of 1200 = 240."))
    L.append(mk(Qn, S, 75, "Table: Sales (A) 120, (B) 150. B's sales are what percentage more than A's, and A's what percentage less than B's?", "25% more, 20% less",
                ["25% more, 25% less", "20% more, 25% less", "30% more, 20% less"], "30/120 = 25% more; 30/150 = 20% less. The base changes."))
    return L


def build():
    return perm_qs() + comb_qs() + prob_qs() + ns_qs() + prog_qs() + di_qs()


if __name__ == "__main__":
    print(len(build()))
