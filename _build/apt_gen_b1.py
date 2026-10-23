"""Aptitude questions, part B1 (logic): Number series, Letter series, Coding-decoding, Cubes, Ranking, Clocks, Calendars, Directions."""
import datetime as dt
import math
from apt_common import mk, fmt

Lg = "logic"
AL = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def sh(word, n):
    return "".join(AL[(AL.index(c) + n) % 26] for c in word)


def ns_qs():
    S = "Number series"
    L = []

    def add(seq, ans, why, wrongs, tgt=60):
        L.append(mk(Lg, S, tgt, "Find the next term: " + ", ".join(str(x) for x in seq) + ", ?", ans, wrongs, why))

    add([3, 7, 11, 15], 19, "Constant difference +4: an AP.", [18, 20, 23], 45)
    add([2, 6, 12, 20, 30], 42, "Differences 4, 6, 8, 10 → next 12. Also n(n + 1): 6 × 7 = 42.", [40, 44, 36], 45)
    add([1, 4, 9, 16, 25], 36, "Squares: 6² = 36.", [30, 34, 49], 45)
    add([2, 5, 10, 17, 26], 37, "n² + 1: 6² + 1 = 37. Differences 3, 5, 7, 9 → 11.", [36, 38, 35], 45)
    add([3, 6, 12, 24], 48, "Each term × 2.", [36, 42, 30], 45)
    add([5, 11, 23, 47], 95, "× 2 + 1 each time: 47 × 2 + 1 = 95.", [94, 96, 93], 60)
    add([1, 8, 27, 64], 125, "Cubes: 5³ = 125.", [100, 120, 216], 45)
    add([2, 3, 5, 7, 11], 13, "Consecutive primes.", [12, 15, 17], 45)
    add([1, 2, 6, 24, 120], 720, "Factorials, or × 2, × 3, × 4, × 5, × 6.", [600, 840, 480], 60)
    add([4, 5, 7, 10, 14], 19, "Differences 1, 2, 3, 4 → next 5.", [18, 20, 21], 60)
    add([1, 3, 7, 13, 21], 31, "Differences 2, 4, 6, 8 → next 10.", [29, 30, 33], 60)
    add([2, 4, 8, 14, 22], 32, "Differences 2, 4, 6, 8 → next 10.", [30, 31, 34], 60)
    add([120, 99, 80, 63, 48], 35, "n² − 1 counting down: 11²−1 … 6²−1 = 35. Differences −21, −19, −17, −15 → −13.", [34, 36, 33], 75)
    add([1, 1, 2, 3, 5, 8], 13, "Each term is the sum of the previous two (Fibonacci).", [11, 12, 14], 45)
    L.append(mk(Lg, S, 60, "Find the missing term: 5, 10, 20, ?, 80", 40, [30, 45, 35], "Each term doubles, so ? = 40."))
    add([3, 8, 15, 24, 35], 48, "n² − 1 starting from 2²: next 7² − 1 = 48. Differences 5, 7, 9, 11 → 13.", [46, 47, 50], 75)
    add([2, 12, 36, 80, 150], 252, "Terms are n²(n + 1): 1²·2, 2²·3, 3²·4, 4²·5, 5²·6, so next is 6²·7 = 252.", [240, 250, 260], 90)
    return L


def ls_qs():
    S = "Letter series"
    L = []
    L.append(mk(Lg, S, 45, "Find the next letter: A, C, E, G, ?", "I", ["H", "J", "K"], "+2 each time."))
    L.append(mk(Lg, S, 45, "Find the next letter: Z, X, V, T, ?", "R", ["S", "Q", "P"], "−2 each time."))
    L.append(mk(Lg, S, 45, "Find the next letter: B, E, H, K, ?", "N", ["M", "O", "L"], "+3 each time."))
    L.append(mk(Lg, S, 60, "Find the next pair: AZ, BY, CX, ?", "DW", ["DV", "EW", "CW"], "First letter moves forward, second moves back; mirrors sum to 27."))
    L.append(mk(Lg, S, 45, "Which letter is the 8th from the end of the alphabet?", "S", ["R", "T", "Q"], "26 − 8 + 1 = 19, which is S."))
    L.append(mk(Lg, S, 45, "What is the mirror letter of K (A↔Z, B↔Y…)?", "P", ["O", "Q", "L"], "Mirrors sum to 27: K = 11, 27 − 11 = 16 = P."))
    L.append(mk(Lg, S, 45, "What is the sum of the positions of the letters in CAB (A=1…Z=26)?", 6, [5, 7, 9], "3 + 1 + 2 = 6."))
    L.append(mk(Lg, S, 60, "Find the next pair: AB, DE, GH, ?", "JK", ["IJ", "JL", "KL"], "Each pair moves 3 forward as a block."))
    L.append(mk(Lg, S, 60, "Find the next pair: ZA, YB, XC, ?", "WD", ["WC", "VD", "XD"], "First letter goes back, second goes forward."))
    L.append(mk(Lg, S, 60, "Find the next letter: A, B, D, G, ?", "K", ["J", "L", "I"], "Gaps 1, 2, 3, 4 → G + 4 = K."))
    L.append(mk(Lg, S, 45, "Find the next letter: C, F, I, L, ?", "O", ["N", "P", "M"], "+3 each time."))
    L.append(mk(Lg, S, 45, "Which letter is 14th from the end of the alphabet?", "M", ["N", "L", "O"], "26 − 14 + 1 = 13 = M."))
    L.append(mk(Lg, S, 60, "Find the next group: ACE, BDF, CEG, ?", "DFH", ["DEG", "CFH", "EGI"], "Each group shifts forward by 1."))
    L.append(mk(Lg, S, 75, "Find the next letter: A, C, F, J, ?", "O", ["N", "M", "P"], "Gaps +2, +3, +4, then +5: J + 5 = O."))
    L.append(mk(Lg, S, 60, "What is the position value of the letter N (A=1…Z=26)?", 14, [13, 15, 12], "N is the 14th letter."))
    return L


def cod_qs():
    S = "Coding–decoding"
    L = []
    L.append(mk(Lg, S, 45, "If PEN is coded as QFO, how is INK coded?", sh("INK", 1), [sh("INK", 2), sh("INK", -1), "JNK"], "Each letter moves +1."))
    L.append(mk(Lg, S, 60, "If BOLD is written as ANKC, how is CAST written?", sh("CAST", -1), [sh("CAST", 1), "BZSU", "BZSR"], "Each letter moves −1."))
    L.append(mk(Lg, S, 45, "If FAN is coded as HCP, how is TEA coded?", sh("TEA", 2), [sh("TEA", 1), sh("TEA", 3), "VGB"], "Each letter moves +2."))
    L.append(mk(Lg, S, 45, "If DELHI is written as IHLED, how is MUMBAI written?", "IABMUM", ["MUMBAI", "IABUMM", "IBAMUM"], "The word is simply reversed."))
    L.append(mk(Lg, S, 45, "If A=1, B=2, … Z=26, what is the value of DOG?", 26, [25, 27, 24], "4 + 15 + 7 = 26."))
    L.append(mk(Lg, S, 60, "If A↔Z, B↔Y, C↔X (mirror coding), how is CAB written?", "XZY", ["XYZ", "ZXY", "YZX"], "C→X, A→Z, B→Y."))
    L.append(mk(Lg, S, 75, "If ABCD is coded as BDDF (alternating +1, +2), how is EFGH coded?", "FHHJ", ["FGHI", "GHIJ", "FHIJ"], "E+1=F, F+2=H, G+1=H, H+2=J."))
    L.append(mk(Lg, S, 60, "If CAT is written as 3-1-20, how is BAD written?", "2-1-4", ["2-2-4", "1-2-4", "2-1-5"], "Alphabet positions: B=2, A=1, D=4."))
    L.append(mk(Lg, S, 60, "If TABLE is written as 20-1-2-12-5, how is LAKE written?", "12-1-11-5", ["12-1-10-5", "11-1-12-5", "12-2-11-5"], "L=12, A=1, K=11, E=5."))
    L.append(mk(Lg, S, 60, "If RAIN is written as SBJO, how is SNOW written?", sh("SNOW", 1), [sh("SNOW", 2), sh("SNOW", -1), "TNPX"], "Each letter +1."))
    L.append(mk(Lg, S, 75, "If MONDAY is coded as NPOEBZ, how is FRIDAY coded?", sh("FRIDAY", 1), [sh("FRIDAY", -1), sh("FRIDAY", 2), "GSJEBY"], "Check the first two letters: M→N, O→P. Rule +1 applied to every letter."))
    L.append(mk(Lg, S, 75, "If in a code, 'LION' is written as 'NKQP', how is 'TIGER' written?", sh("TIGER", 2), [sh("TIGER", 1), sh("TIGER", 3), "VKIGS"], "L→N, I→K: each letter +2."))
    L.append(mk(Lg, S, 60, "If the letters of 'CLOCK' are written by their positions and added, what is the total?", 3 + 12 + 15 + 3 + 11, [43, 45, 47], "3 + 12 + 15 + 3 + 11 = 44."))
    return L


def cube_qs():
    S = "Cubes"
    L = []
    for n in (3, 4, 5, 6):
        L.append(mk(Lg, S, 60, f"A {n}×{n}×{n} cube is painted on all faces and cut into unit cubes. How many have exactly one face painted?", 6 * (n - 2) ** 2,
                    [12 * (n - 2), (n - 2) ** 3, 6 * (n - 1) ** 2], f"Face centres = 6(n − 2)² = 6 × {(n - 2) ** 2} = {6 * (n - 2) ** 2}."))
    for n in (4, 5, 6):
        L.append(mk(Lg, S, 60, f"A {n}×{n}×{n} painted cube is cut into unit cubes. How many have exactly two faces painted?", 12 * (n - 2),
                    [6 * (n - 2) ** 2, 8, 12 * (n - 1)], f"Edges = 12(n − 2) = {12 * (n - 2)}."))
    for n in (3, 5, 6):
        L.append(mk(Lg, S, 60, f"A {n}×{n}×{n} painted cube is cut into unit cubes. How many have no paint at all?", (n - 2) ** 3,
                    [6 * (n - 2) ** 2, n ** 3 - 8, (n - 1) ** 3], f"Interior = (n − 2)³ = {(n - 2) ** 3}."))
    L.append(mk(Lg, S, 45, "How many small cubes of a painted cube always have three faces painted, whatever its size?", 8, [4, 6, 12], "Corners: a cube always has 8."))
    L.append(mk(Lg, S, 60, "A 4 cm cube is painted and cut into 1 cm cubes. How many have at least one painted face?", 56, [48, 64, 32], "64 − interior (2³ = 8) = 56."))
    L.append(mk(Lg, S, 75, "A 5 cm cube is painted and cut into 1 cm cubes. How many have exactly one or two faces painted?", 54 + 36,
                [54, 36, 98], "One face: 6 × 9 = 54. Two faces: 12 × 3 = 36. Sum 90."))
    L.append(mk(Lg, S, 75, "A cube of side 6 is cut into unit cubes. How many cuts (one plane each, no rearranging) are needed in total?", 15, [18, 12, 6],
                "5 cuts along each of 3 directions = 15."))
    return L


def rank_qs():
    S = "Ranking"
    L = []
    L.append(mk(Lg, S, 45, "A is 7th from the top and 12th from the bottom in a class. How many students are there?", 18, [19, 20, 17], "7 + 12 − 1 = 18."))
    L.append(mk(Lg, S, 45, "Rank 5 from the top in a class of 40. What is the rank from the bottom?", 36, [35, 34, 37], "40 + 1 − 5 = 36."))
    L.append(mk(Lg, S, 60, "Rahul is 15th from the left and Mohan is 20th from the right in a row of 40. How many people are between them?", 5, [4, 6, 3],
                "Mohan is 21st from the left; between = 21 − 15 − 1 = 5."))
    L.append(mk(Lg, S, 45, "A is 10th from the left and B is 18th from the left. How many people are between them?", 7, [8, 6, 9], "|18 − 10| − 1 = 7."))
    L.append(mk(Lg, S, 45, "Kiran is 14th from the front and 17th from the back of a queue. How many are in the queue?", 30, [31, 29, 32], "14 + 17 − 1 = 30."))
    L.append(mk(Lg, S, 45, "In a row of 25, a boy is 10th from the left. What is his position from the right?", 16, [15, 14, 17], "25 + 1 − 10 = 16."))
    L.append(mk(Lg, S, 75, "In a class of 40, 25 passed Maths and 22 passed English, and everyone passed at least one. How many passed both?", 7, [3, 8, 10],
                "Overlap = sum − total = 25 + 22 − 40 = 7."))
    L.append(mk(Lg, S, 60, "In a row of 20 students, Ram is 7th from the left and Sham is 9th from the right. How many are between them?", 4, [3, 5, 6],
                "Sham is 12th from the left; 12 − 7 − 1 = 4."))
    L.append(mk(Lg, S, 75, "X is 11th from the top and Y is 11th from the bottom, and there are 7 students between them. How many students in all?", 29, [28, 30, 31],
                "10 above X, 7 between, 10 below Y plus X and Y themselves: 10 + 1 + 7 + 1 + 10 = 29."))
    L.append(mk(Lg, S, 60, "A man is 6th from the left and 9th from the right of a row. How many are in the row?", 14, [15, 13, 16], "6 + 9 − 1 = 14."))
    L.append(mk(Lg, S, 75, "In an exam, 18 students are ahead of Neha and she is 9th from the last. How many students took the exam?", 27, [26, 28, 25],
                "Her rank is 19th from the top: 19 + 9 − 1 = 27."))
    L.append(mk(Lg, S, 60, "Seema is 12th from the left. After she swaps places with the person 8 places to her right she is on which position from the left?", 20, [19, 21, 4],
                "12 + 8 = 20."))
    return L


def clock_qs():
    S = "Clocks"
    L = []

    def ang(h, m):
        a = abs(30 * h - 5.5 * m)
        return a if a <= 180 else 360 - a

    for h, m in [(3, 30), (4, 20), (7, 45), (9, 15), (12, 30), (2, 40), (10, 10), (6, 25)]:
        a = ang(h, m)
        L.append(mk(Lg, S, 75, f"What is the angle between the hands of a clock at {h}:{m:02d}?", fmt(a, "°"),
                    [fmt(x, "°") for x in (a + 15, abs(a - 20), a + 7.5, a + 30, abs(a - 7.5), a + 45)],
                    f"|30H − 5.5M| = |{30 * h} − {5.5 * m}| = {fmt(abs(30 * h - 5.5 * m))}" + ("" if abs(30 * h - 5.5 * m) <= 180 else f"; over 180, so 360 − that = {fmt(a)}") + "°."))
    L.append(mk(Lg, S, 45, "How many degrees does the minute hand move in 25 minutes?", "150°", ["125°", "180°", "75°"], "6° per minute."))
    L.append(mk(Lg, S, 45, "How many degrees does the hour hand move in 40 minutes?", "20°", ["40°", "30°", "10°"], "0.5° per minute."))
    L.append(mk(Lg, S, 60, "How many times do the hands of a clock overlap in 24 hours?", 22, [24, 23, 44], "Every 65 5/11 minutes: 22 times a day."))
    L.append(mk(Lg, S, 75, "At what time between 4 and 5 do the hands coincide?", "21 9/11 min past 4", ["20 min past 4", "22 min past 4", "21 min past 4"], "H × 60/11 = 240/11 = 21 9/11."))
    L.append(mk(Lg, S, 60, "How many times do the hands of a clock make a right angle in 12 hours?", 22, [24, 12, 11], "Hands are at right angles twice every hour, except that in 12 hours two of those coincide: 22 in all."))
    return L


def cal_qs():
    S = "Calendars"
    L = []
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    def wd(y, m, d):
        return days[dt.date(y, m, d).weekday()]

    def wrong3(right):
        i = days.index(right)
        return [days[(i + 1) % 7], days[(i + 2) % 7], days[(i - 1) % 7]]

    L.append(mk(Lg, S, 60, "Today is Monday. What day will it be after 100 days?", "Wednesday", ["Tuesday", "Thursday", "Friday"], "100 mod 7 = 2; Monday + 2 = Wednesday."))
    L.append(mk(Lg, S, 45, "Which of these is a leap year?", "2000", ["1900", "2100", "2200"], "Centuries must divide by 400: only 2000 does."))
    L.append(mk(Lg, S, 45, "If 1 January 2021 was Friday, what day was 1 January 2022?", "Saturday", ["Friday", "Sunday", "Thursday"], "2021 is an ordinary year: +1 day."))
    L.append(mk(Lg, S, 60, "If 1 January 2024 was a Monday, what day was 1 January 2025?", "Wednesday", ["Tuesday", "Thursday", "Monday"], "2024 is a leap year: +2 days."))
    for (y, m, d) in [(1947, 8, 15), (1950, 1, 26), (2000, 1, 1)]:
        r = wd(y, m, d)
        L.append(mk(Lg, S, 90, f"On what day of the week was {d} {dt.date(y, m, d).strftime('%B')} {y}?", r, wrong3(r),
                    "Count odd days: century odd days + remaining years (with leap years) + days into the year, all mod 7."))
    L.append(mk(Lg, S, 45, "How many odd days are there in 100 years?", 5, [4, 6, 1], "100 years = 76 ordinary + 24 leap: 76 + 48 = 124 = 17 weeks + 5."))
    L.append(mk(Lg, S, 45, "How many odd days are there in 200 years?", 3, [2, 4, 5], "5 × 2 = 10 = 7 + 3."))
    L.append(mk(Lg, S, 45, "How many odd days are there in 400 years?", 0, [1, 2, 7], "A full 400-year cycle is a whole number of weeks."))
    L.append(mk(Lg, S, 60, "A 30-day month begins on a Saturday. How many Sundays does it contain?", 5, [4, 6, 3], "Sundays fall on 2, 9, 16, 23 and 30."))
    L.append(mk(Lg, S, 60, "How many days are there from 15 January to 15 March in an ordinary year?", 59, [60, 58, 61], "16 (Jan) + 28 (Feb) + 15 (Mar) = 59."))
    L.append(mk(Lg, S, 60, "1 February 2024 was a Thursday. How many Sundays were there in February 2024?", 4, [5, 3, 2], "Leap year, 29 days. Sundays fall on 4, 11, 18, 25."))
    L.append(mk(Lg, S, 75, "1 January 2000 was a Saturday. What day was 1 March 2000?", "Wednesday", ["Tuesday", "Thursday", "Monday"], "2000 is leap: 31 + 29 = 60 days; 60 mod 7 = 4; Saturday + 4 = Wednesday."))
    return L


def dir_qs():
    S = "Directions"
    L = []
    for a, b in [(6, 8), (9, 12), (5, 12), (8, 15)]:
        c = int(math.hypot(a, b))
        L.append(mk(Lg, S, 60, f"A man walks {a} km east and then {b} km north. How far is he from the start?", f"{c} km", [f"{a + b} km", f"{abs(b - a)} km", f"{c + 1} km"],
                    f"Perpendicular legs: √({a}² + {b}²) = {c}."))
    L.append(mk(Lg, S, 60, "A walks 5 km north, 8 km east and 5 km south. In which direction is he from the start, and how far?", "East, 8 km", ["North, 5 km", "East, 18 km", "South-east, 10 km"],
                "North and south cancel, leaving 8 km east."))
    L.append(mk(Lg, S, 60, "A walks 4 km north, 3 km west and 4 km south. How far is he from the start?", "3 km", ["5 km", "7 km", "11 km"], "Opposite legs cancel; 3 km remains."))
    L.append(mk(Lg, S, 75, "A walks 20 km north and then 15 km east. How far is he from the start?", "25 km",
                ["35 km", "30 km", "5 km"], "√(20² + 15²) = 25."))
    L.append(mk(Lg, S, 45, "Facing north, a man turns 90° right, then 90° right again. Which direction does he face?", "South", ["East", "West", "North"], "N → E → S."))
    L.append(mk(Lg, S, 60, "Facing east, a man turns 90° left, then 180°, then 90° right. Which direction does he face?", "West", ["South", "East", "North"],
                "East → left → North → 180° → South → right → West."))
    L.append(mk(Lg, S, 60, "Facing south-west, a man turns 135° clockwise. Which direction does he face?", "North", ["East", "North-east", "South"], "SW is 225°; +135° = 360°, which is North."))
    L.append(mk(Lg, S, 75, "A walks 10 m north, 6 m east, 10 m south and 2 m west. How far from the start and in which direction?", "4 m east", ["8 m east", "4 m west", "16 m east"],
                "North/south cancel. East 6 − west 2 = 4 east."))
    L.append(mk(Lg, S, 75, "A walks 12 m west, turns right and walks 5 m. How far is he from the start?", "13 m", ["17 m", "7 m", "12 m"], "Perpendicular: √(12² + 5²) = 13."))
    return L


def build():
    return ns_qs() + ls_qs() + cod_qs() + cube_qs() + rank_qs() + clock_qs() + cal_qs() + dir_qs()


if __name__ == "__main__":
    print(len(build()))
