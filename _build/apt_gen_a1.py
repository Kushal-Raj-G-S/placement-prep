"""Aptitude questions, part A1: Percentages, Profit & loss, Averages, Ratio, Speed & distance, Time & work.
Every answer is computed from the formula the question is meant to drill; wrong options are the usual mistakes."""
from fractions import Fraction as Fr
from apt_common import mk, fmt, near

Qn = "quant"


def pct_qs():
    S = "Percentages"
    L = []
    for p, y in [(35, 480), (12.5, 640), (18, 250)]:
        r = p * y / 100
        L.append(mk(Qn, S, 45, f"What is {fmt(p)}% of {y}?", fmt(r),
                    [fmt(p * y / 10), fmt(y - r), fmt(r + 10)],
                    f"x% of y = xy/100. {fmt(p)} × {y} / 100 = {fmt(r)}."))
    for a, b in [(20, 30), (25, 20), (10, 40)]:
        net = a + b + a * b / 100
        L.append(mk(Qn, S, 60, f"A quantity rises {a}% and then rises a further {b}%. What is the overall increase?",
                    fmt(net, "%"), [fmt(a + b, "%"), fmt(net - a * b / 100 + 2 * a * b / 100 / 2 + 1, "%"), fmt(net - 2, "%")],
                    f"Net = a + b + ab/100 = {a} + {b} + {fmt(a * b / 100)} = {fmt(net)}%. The plain sum {a + b}% is the trap."))
    for a, b in [(20, 10), (30, 20)]:
        net = a + b - a * b / 100
        L.append(mk(Qn, S, 60, f"A shirt gets a {a}% discount, then a further {b}% off the reduced price. What is the single equivalent discount?",
                    fmt(net, "%"), [fmt(a + b, "%"), fmt(net + 4, "%"), fmt(net - 3, "%")],
                    f"Treat discounts as negatives in a + b + ab/100, which gives {a} + {b} − {a}×{b}/100 = {fmt(net)}%."))
    for x in (25, 20, 10):
        L.append(mk(Qn, S, 60, f"The price of sugar rises by {x}%. By what percentage must a family cut consumption to keep the spend unchanged?",
                    fmt(100 * x / (100 + x), "%"), [fmt(x, "%"), fmt(100 * x / (100 - x), "%"), fmt(x / 2, "%")],
                    f"Consumption must fall 100x/(100 + x) = {100 * x}/{100 + x} = {fmt(100 * x / (100 + x))}%. It is never the same x%."))
    for x in (20, 25):
        L.append(mk(Qn, S, 60, f"The price of rice falls by {x}%. By what percentage can consumption rise for the same expenditure?",
                    fmt(100 * x / (100 - x), "%"), [fmt(x, "%"), fmt(100 * x / (100 + x), "%"), fmt(x + 10, "%")],
                    f"Consumption rises 100x/(100 − x) = {100 * x}/{100 - x} = {fmt(100 * x / (100 - x))}%."))
    for x in (10, 20):
        L.append(mk(Qn, S, 60, f"A town's population rises {x}% in one year and falls {x}% the next. What is the net change?",
                    f"{fmt(x * x / 100)}% decrease", ["No change", f"{x}% decrease", f"{fmt(x * x / 100)}% increase"],
                    f"x% up then x% down is always a net LOSS of x²/100 = {fmt(x * x / 100)}%."))
    L.append(mk(Qn, S, 60, "A is 25% more than B. B is what percentage less than A?", "20%", ["25%", "16.67%", "33.33%"],
                "A = 1.25 B, so B = A/1.25 = 0.8 A: 20% less. The base switches, so the percentage changes."))
    L.append(mk(Qn, S, 60, "A number increased by 15% becomes 345. What is the number?", "300", ["310", "293.25", "330"],
                "Divide by the multiplier: 345 / 1.15 = 300. Never subtract 15% of 345."))
    L.append(mk(Qn, S, 75, "A candidate needs 40% to pass, scores 180 and fails by 30 marks. What are the total marks?", "525",
                ["450", "500", "600"], "Pass mark = 180 + 30 = 210 = 40% of total, so total = 210 × 100/40 = 525."))
    L.append(mk(Qn, S, 75, "In a two-candidate election the winner gets 55% of the votes and wins by 400 votes. How many votes were cast?", "4000",
                ["2000", "3600", "4400"], "Margin = 55% − 45% = 10% of votes = 400, so total = 4000."))
    L.append(mk(Qn, S, 75, "A salary is cut by 20%. By what percentage must the reduced salary be raised to restore the original?", "25%",
                ["20%", "22.5%", "30%"], "Raise = 100×20/(100 − 20) = 25%. Same shape as the price/consumption formula."))
    L.append(mk(Qn, S, 75, "Three successive increases of 10%, 20% and 25% are applied. What is the total increase?", "65%",
                ["55%", "60%", "70%"], "Multiply: 1.10 × 1.20 × 1.25 = 1.65, so +65%."))
    L.append(mk(Qn, S, 60, "A is 150% of B. B is what percentage of A?", "66.67%", ["50%", "150%", "33.33%"],
                "A = 1.5 B, so B/A = 1/1.5 = 2/3 = 66.67%."))
    L.append(mk(Qn, S, 45, "1/8 of 2400 equals what percentage of 2400, and what value?", "12.5%, 300", ["8%, 300", "12.5%, 200", "15%, 360"],
                "1/8 = 12.5% from the fraction table, and 2400/8 = 300."))
    return L


def pl_qs():
    S = "Profit & loss"
    L = []
    for cp, sp in [(800, 920), (640, 720), (250, 300)]:
        p = (sp - cp) * 100 / cp
        L.append(mk(Qn, S, 45, f"An article bought for ₹{cp} is sold for ₹{sp}. What is the profit percentage?", fmt(p, "%"),
                    [fmt((sp - cp) * 100 / sp, "%"), fmt(sp - cp, "%"), fmt(p + 2.5, "%")],
                    f"Profit % is on cost: ({sp} − {cp})/{cp} × 100 = {fmt(p)}%."))
    for cp, sp in [(500, 425), (1200, 1080)]:
        l = (cp - sp) * 100 / cp
        L.append(mk(Qn, S, 45, f"An article bought for ₹{cp} is sold for ₹{sp}. What is the loss percentage?", fmt(l, "%"),
                    [fmt((cp - sp) * 100 / sp, "%"), fmt(l + 5, "%"), fmt(cp - sp, "%")],
                    f"Loss % = ({cp} − {sp})/{cp} × 100 = {fmt(l)}%, again on cost."))
    L.append(mk(Qn, S, 60, "A shopkeeper marks goods 30% above cost and allows a 10% discount. What is his profit percentage?", "17%",
                ["20%", "15%", "23%"], "SP = CP × 1.30 × 0.90 = 1.17 CP, so 17%."))
    L.append(mk(Qn, S, 60, "At what price (₹) must an article costing ₹900 be marked so that, after a 10% discount, it still earns 20% profit?", "1200",
                ["1080", "1100", "1350"], "SP = 900 × 1.2 = 1080. Marked × 0.9 = 1080 so marked = 1200."))
    L.append(mk(Qn, S, 60, "Two articles are sold at ₹1200 each; one at a 20% gain and the other at a 20% loss. What is the overall result?", "4% loss",
                ["No gain, no loss", "4% gain", "2% loss"], "Same SP with ±x% is always a loss of x²/100 = 400/100 = 4%."))
    L.append(mk(Qn, S, 75, "Two articles are sold at ₹1200 each, one at 20% gain and one at 20% loss. What is the total loss in rupees?", "100",
                ["0", "96", "200"], "CP1 = 1200/1.2 = 1000, CP2 = 1200/0.8 = 1500. Total CP 2500, total SP 2400, loss ₹100."))
    L.append(mk(Qn, S, 60, "A trader uses a 900 g weight for 1 kg but sells at cost price. What is his gain percentage?", "11.11%",
                ["10%", "9.09%", "12.5%"], "Gain % = error/(true − error) = 100/900 = 11.11%."))
    L.append(mk(Qn, S, 60, "A dishonest dealer sells at cost price but uses an 800 g weight for 1 kg. His profit percentage is", "25%",
                ["20%", "16.67%", "22%"], "Gain % = 200/(1000 − 200) × 100 = 25%."))
    L.append(mk(Qn, S, 75, "A man buys 12 pens for ₹10 and sells 10 pens for ₹12. What is his profit percentage?", "44%",
                ["20%", "40%", "50%"], "CP per pen = 10/12, SP per pen = 12/10. Ratio = 1.2 / 0.8333 = 1.44, so 44%."))
    L.append(mk(Qn, S, 75, "The selling price of 15 articles equals the cost price of 20 articles. What is the profit percentage?", "33.33%",
                ["25%", "20%", "40%"], "Let CP = 1: SP of 15 = 20, so SP each = 20/15. Profit = (20 − 15)/15 = 33.33%."))
    L.append(mk(Qn, S, 75, "The marked price is ₹2000. A 15% discount and then an extra 10% discount are given. What is the selling price (₹)?", "1530",
                ["1500", "1600", "1450"], "2000 × 0.85 × 0.90 = 1530. Successive discounts multiply, they do not add to 25%."))
    L.append(mk(Qn, S, 75, "Two articles of the same cost are sold, one at 20% profit and the other at 10% loss. What is the overall profit?", "5%",
                ["10%", "15%", "0%"], "Take CP = 100 each: SP = 120 + 90 = 210 on 200. Profit 10/200 = 5%."))
    L.append(mk(Qn, S, 45, "An article sold at ₹360 gives a 10% loss. What is the cost price (₹)?", "400", ["396", "360", "324"],
                "CP = SP / (1 − 0.10) = 360/0.9 = 400."))
    L.append(mk(Qn, S, 45, "Marked price ₹750, selling price ₹600. What is the discount percentage?", "20%", ["25%", "15%", "18%"],
                "Discount is on the MARKED price: 150/750 = 20%."))
    return L


def avg_qs():
    S = "Averages"
    L = []
    L.append(mk(Qn, S, 45, "The average of five numbers is 24. A sixth number, 36, is added. What is the new average?", "26",
                ["25", "27", "30"], "Shift = (36 − 24)/6 = 2, so the average becomes 26."))
    L.append(mk(Qn, S, 60, "The average age of 8 people is 40. One person aged 32 is replaced and the average rises by 2. What is the new person's age?", "48",
                ["42", "44", "50"], "New = removed + count × change = 32 + 8 × 2 = 48."))
    L.append(mk(Qn, S, 60, "30 students average 60 marks and another 20 students average 75. What is the average of all 50?", "66",
                ["67.5", "65", "68"], "Total = 1800 + 1500 = 3300; 3300/50 = 66. Never average the two averages."))
    L.append(mk(Qn, S, 45, "What is the average of the first 15 natural numbers?", "8", ["7.5", "7", "15"], "(n + 1)/2 = 16/2 = 8."))
    L.append(mk(Qn, S, 60, "The average of seven consecutive integers is 24. What is the largest?", "27", ["28", "26", "30"],
                "The average is the middle term (24), so the largest is 24 + 3 = 27."))
    L.append(mk(Qn, S, 45, "What is the average of the first ten multiples of 5?", "27.5", ["25", "30", "22.5"],
                "Evenly spaced: (first + last)/2 = (5 + 50)/2 = 27.5."))
    L.append(mk(Qn, S, 60, "A batsman averages 40 after 10 innings. He scores 62 in his 11th innings. What is his new average?", "42",
                ["41", "40", "44"], "Shift = (62 − 40)/11 = 2, so 42."))
    L.append(mk(Qn, S, 75, "A batsman averages 32 after 15 innings. What must he score in the 16th to lift the average to 34?", "64",
                ["58", "66", "72"], "Needed = old average + 16 × 2 = 32 + 32 = 64."))
    L.append(mk(Qn, S, 60, "The average of 6 numbers is 25. When one is removed the average of the remaining 5 is 23. What was removed?", "35",
                ["30", "33", "40"], "Total 150 − 115 = 35."))
    L.append(mk(Qn, S, 75, "Five numbers average 30. The first three average 28 and the last three average 33. What is the middle number?", "33",
                ["30", "28", "36"], "3 × 28 + 3 × 33 = 183, which counts the middle twice. 183 − 150 = 33."))
    L.append(mk(Qn, S, 45, "The average of three numbers is 20. Adding a fourth number lifts the average to 22. What is the fourth number?", "28",
                ["26", "30", "24"], "New = old avg + 4 × 2 = 20 + 8 = 28."))
    L.append(mk(Qn, S, 45, "A student's average in 4 subjects is 70. What must he score in the 5th for an overall average of 72?", "80",
                ["76", "78", "82"], "70 + 5 × 2 = 80."))
    L.append(mk(Qn, S, 45, "What is the average of the first 20 even numbers?", "21", ["20", "22", "10"],
                "Evenly spaced from 2 to 40: (2 + 40)/2 = 21."))
    L.append(mk(Qn, S, 75, "Mon–Wed average temperature is 36°C and Tue–Thu is 38°C. If Thursday is 40°C, what was Monday's?", "34",
                ["32", "36", "38"], "Sums: 108 and 114. Thu − Mon = 6, so Monday = 34."))
    return L


def ratio_qs():
    S = "Ratio"
    L = []
    for tot, r in [(960, (3, 5, 4)), (1800, (2, 3, 4))]:
        k = tot // sum(r)
        L.append(mk(Qn, S, 45, f"₹{tot} is divided in the ratio {r[0]}:{r[1]}:{r[2]}. What is the smallest share (₹)?", min(r) * k,
                    [max(r) * k, tot // 3, min(r) * k // 2], f"One part = {tot}/{sum(r)} = {k}; smallest = {min(r)} × {k} = {min(r) * k}."))
    L.append(mk(Qn, S, 60, "If a:b = 2:3 and b:c = 4:5, then a:b:c is", "8:12:15", ["2:3:5", "8:12:10", "6:9:15"],
                "Scale b to the LCM of 3 and 4 = 12: a:b = 8:12 and b:c = 12:15."))
    L.append(mk(Qn, S, 60, "Rice at ₹30/kg is mixed with rice at ₹45/kg so the mixture is worth ₹36/kg. In what ratio (cheaper : dearer)?", "3:2",
                ["2:3", "1:1", "4:3"], "Cheaper/dearer = (45 − 36)/(36 − 30) = 9/6 = 3:2."))
    L.append(mk(Qn, S, 75, "A 60 L mixture has milk and water in the ratio 7:3. How much water must be added to make it 1:1?", "24 L",
                ["18 L", "12 L", "30 L"], "Milk 42, water 18. For 1:1, water must equal 42, so add 24."))
    L.append(mk(Qn, S, 45, "Two ages are in the ratio 5:7 and sum to 96. What is the older age?", "56", ["40", "48", "60"],
                "One part = 96/12 = 8; older = 7 × 8 = 56."))
    L.append(mk(Qn, S, 75, "A and B have incomes in the ratio 5:4 and expenses in the ratio 3:2. Each saves ₹800. What is A's income (₹)?", "2000",
                ["1600", "2400", "1800"], "5x − 3y = 800 and 4x − 2y = 800 give x = 400, so A earns 5 × 400 = 2000."))
    L.append(mk(Qn, S, 60, "₹1400 is shared among A, B, C with A:B = 2:3 and B:C = 4:5. How much does C get (₹)?", "600",
                ["500", "560", "700"], "A:B:C = 8:12:15, sum 35, part = 40; C = 15 × 40 = 600."))
    L.append(mk(Qn, S, 75, "Two numbers are in the ratio 2:3. Adding 6 to each makes the ratio 3:4. What is the larger number?", "18",
                ["12", "24", "15"], "(2k + 6)/(3k + 6) = 3/4 gives 8k + 24 = 9k + 18 so k = 6; larger = 18."))
    L.append(mk(Qn, S, 60, "What is the mean proportional between 4 and 25?", "10", ["14.5", "12", "9"], "√(4 × 25) = 10."))
    L.append(mk(Qn, S, 45, "Find the fourth proportional to 6, 9 and 10.", "15", ["12", "13.5", "18"], "6:9 = 10:x so x = 9 × 10 / 6 = 15."))
    L.append(mk(Qn, S, 45, "Boys and girls in a class are in the ratio 5:4 with 90 boys. How many students in total?", "162",
                ["150", "180", "144"], "One part = 18; total parts 9; 9 × 18 = 162."))
    L.append(mk(Qn, S, 45, "₹2400 is split in the ratio 1:2:3. What is the largest share (₹)?", "1200", ["800", "1000", "600"],
                "Part = 2400/6 = 400; largest = 3 × 400 = 1200."))
    L.append(mk(Qn, S, 60, "Two ratios 2:3 and 4:5 are compounded. The result is", "8:15", ["6:8", "2:5", "10:12"],
                "Multiply antecedents and consequents: 2×4 : 3×5 = 8:15."))
    L.append(mk(Qn, S, 60, "If a:b = 3:4 and the sum a + b = 91, what is the value of b?", "52", ["39", "48", "56"],
                "One part = 91/7 = 13; b = 4 × 13 = 52."))
    return L


def sd_qs():
    S = "Speed & distance"
    L = []
    L.append(mk(Qn, S, 45, "Convert 72 km/h into m/s.", "20 m/s", ["25 m/s", "18 m/s", "15 m/s"], "km/h × 5/18 = 72 × 5/18 = 20."))
    L.append(mk(Qn, S, 45, "Convert 25 m/s into km/h.", "90 km/h", ["80 km/h", "75 km/h", "100 km/h"], "m/s × 18/5 = 25 × 3.6 = 90."))
    for a, b in [(40, 60), (30, 70)]:
        L.append(mk(Qn, S, 45, f"A car covers the first half of a trip at {a} km/h and the second half at {b} km/h. What is the average speed?",
                    fmt(2 * a * b / (a + b), " km/h"), [fmt((a + b) / 2, " km/h"), fmt(2 * a * b / (a + b) + 3, " km/h"), fmt(2 * a * b / (a + b) - 4, " km/h")],
                    f"Equal distances: 2ab/(a + b) = {2 * a * b}/{a + b} = {fmt(2 * a * b / (a + b))}. The plain mean is the trap."))
    L.append(mk(Qn, S, 45, "A 150 m long train moving at 54 km/h passes a pole. How long does it take?", "10 s", ["8 s", "12 s", "15 s"],
                "54 km/h = 15 m/s. Pole: only its own length, 150/15 = 10 s."))
    L.append(mk(Qn, S, 60, "A 200 m train crosses a 300 m platform in 25 s. What is its speed?", "72 km/h", ["60 km/h", "80 km/h", "54 km/h"],
                "Distance = 500 m; speed = 20 m/s = 72 km/h."))
    L.append(mk(Qn, S, 75, "Two trains of 120 m and 180 m run on parallel tracks in opposite directions at 60 km/h and 90 km/h. How long to cross each other completely?", "7.2 s",
                ["10 s", "12 s", "6 s"], "Relative speed 150 km/h = 125/3 m/s; distance 300 m; time = 300 × 3/125 = 7.2 s."))
    L.append(mk(Qn, S, 75, "A 140 m train at 50 km/h overtakes a 160 m train running the same way at 32 km/h. How long does the overtake take?", "60 s",
                ["30 s", "45 s", "90 s"], "Relative speed 18 km/h = 5 m/s; distance 300 m; 300/5 = 60 s."))
    L.append(mk(Qn, S, 60, "A boat does 12 km/h in still water and the stream flows at 3 km/h. How long to go 45 km upstream?", "5 h",
                ["3 h", "3.75 h", "4 h"], "Upstream speed = 12 − 3 = 9 km/h; 45/9 = 5 h."))
    L.append(mk(Qn, S, 75, "A boat goes 24 km downstream in 2 h and returns in 3 h. What is the speed of the stream?", "2 km/h",
                ["4 km/h", "1 km/h", "3 km/h"], "d = 12, u = 8. Stream = (d − u)/2 = 2 km/h (still water 10)."))
    L.append(mk(Qn, S, 75, "Walking at 5 km/h a man is 12 min late; at 6 km/h he is 8 min early. How far (km) is the destination?", "10",
                ["8", "12", "6"], "d/5 − d/6 = 20/60 = 1/3, so d/30 = 1/3 and d = 10."))
    L.append(mk(Qn, S, 45, "Two towns are 300 km apart. Two cars start towards each other at 40 km/h and 60 km/h. When do they meet?", "3 h",
                ["4 h", "2.5 h", "6 h"], "Opposite directions: speeds add, 300/100 = 3 h."))
    L.append(mk(Qn, S, 60, "Walking at 3/4 of his usual speed a man takes 10 minutes more than usual. What is his usual time (minutes)?", "30",
                ["20", "40", "25"], "Speed ratio 3:4 means time ratio 4:3; the extra 1 part is 10 min, so usual (3 parts) is 30."))
    L.append(mk(Qn, S, 60, "A man travels uphill at 30 km/h and returns downhill over the same road at 20 km/h. What is the average speed?", "24 km/h",
                ["25 km/h", "26 km/h", "22 km/h"], "2ab/(a + b) = 1200/50 = 24."))
    L.append(mk(Qn, S, 75, "A man rows at 8 km/h in still water against a 2 km/h current. He rows 30 km downstream and returns. Total time?", "8 h",
                ["7.5 h", "6 h", "9 h"], "Down 30/10 = 3 h, up 30/6 = 5 h; total 8 h."))
    return L


def tw_qs():
    S = "Time & work"
    L = []
    L.append(mk(Qn, S, 45, "A can finish a job in 12 days and B in 18 days. Together how many days?", "7.2", ["15", "6", "7.5"],
                "LCM 36: rates 3 + 2 = 5 units/day, 36/5 = 7.2 days."))
    L.append(mk(Qn, S, 60, "A and B together finish a job in 10 days. A alone takes 15 days. How long would B alone take?", "30",
                ["25", "20", "5"], "LCM 30: together 3/day, A 2/day, so B 1/day: 30 days."))
    L.append(mk(Qn, S, 45, "A, B and C can finish a job in 20, 30 and 60 days respectively. Working together how many days?", "10",
                ["15", "12", "8"], "LCM 60: 3 + 2 + 1 = 6/day, 60/6 = 10."))
    L.append(mk(Qn, S, 60, "A alone does a job in 10 days. With B he finishes it in 6 days. How long would B alone take?", "15",
                ["12", "16", "20"], "LCM 30: together 5/day, A 3/day, so B 2/day: 15 days."))
    L.append(mk(Qn, S, 60, "Pipe A fills a tank in 12 h and pipe B empties it in 20 h. With both open, how long to fill the empty tank?", "30 h",
                ["32 h", "16 h", "8 h"], "LCM 60: +5 − 3 = 2/day, 60/2 = 30 h."))
    L.append(mk(Qn, S, 60, "Three pipes fill a tank in 10, 15 and 30 hours. All open together, the tank fills in", "5 h",
                ["6 h", "10 h", "7.5 h"], "LCM 30: 3 + 2 + 1 = 6/h, 30/6 = 5 h."))
    L.append(mk(Qn, S, 45, "12 men finish a job in 20 days. How many days would 15 men take?", "16", ["25", "18", "15"],
                "Men × days is constant: 12 × 20/15 = 16."))
    L.append(mk(Qn, S, 75, "8 men build 400 m of road in 12 days. How many days will 10 men take to build 500 m?", "12",
                ["10", "15", "9.6"], "M1D1/W1 = M2D2/W2: 8×12/400 = 10×D/500, so D = 12."))
    L.append(mk(Qn, S, 60, "A is twice as efficient as B. Together they finish a job in 12 days. How long would A alone take?", "18",
                ["24", "36", "20"], "Rates 2 + 1 = 3/day, total 36 units. A: 36/2 = 18 days."))
    L.append(mk(Qn, S, 75, "A can do a job in 15 days and B in 20 days. A works 3 days and leaves. How many more days does B need?", "16",
                ["12", "15", "20"], "A did 3/15 = 1/5; 4/5 left. B: 4/5 × 20 = 16 days."))
    L.append(mk(Qn, S, 90, "A takes 10 days and B takes 15 days. They work on alternate days, A first. How many days to finish?", "12",
                ["13", "12.5", "10"], "LCM 30: A 3 units, B 2 units, 5 per two days; 30/5 = 6 pairs = 12 days."))
    L.append(mk(Qn, S, 60, "A takes 6 days and B takes 9 days for a job. They earn ₹1500 for it together. What is A's share (₹)?", "900",
                ["750", "600", "1000"], "Share is by work done, ratio of rates 1/6 : 1/9 = 3:2. A gets 3/5 × 1500 = 900."))
    L.append(mk(Qn, S, 90, "A+B finish a job in 8 days, B+C in 12 days, A+C in 24 days. How long will all three together take?", "8",
                ["6", "12", "10"], "Rates: 1/8 + 1/12 + 1/24 = 6/24 = 2(A+B+C), so A+B+C = 1/8: 8 days."))
    L.append(mk(Qn, S, 75, "A pipe fills a tank in 6 h but a leak makes it take 8 h. How long would the leak alone take to empty the full tank?", "24 h",
                ["12 h", "14 h", "48 h"], "Leak rate = 1/6 − 1/8 = 1/24: 24 h."))
    return L


def build():
    return pct_qs() + pl_qs() + avg_qs() + ratio_qs() + sd_qs() + tw_qs()


if __name__ == "__main__":
    b = build()
    print(len(b))
