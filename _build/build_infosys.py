# -*- coding: utf-8 -*-
"""Builds '12 - Infosys Drive (test + interview).html'.
Every pseudocode answer is COMPUTED by running the equivalent Python, and every puzzle is brute-forced
for a unique answer, so no answer key is hand-typed.      python build_infosys.py"""
import json, os, random, itertools, html

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "12 - Infosys Drive (test + interview).html")


def cdiv(a, b):                      # C-style integer division (truncates toward zero), what pseudocode means by a / b
    return int(a / b)


# ------------------------------------------------------------------ PSEUDOCODE --------------------------------
# (topic, pseudocode, python that sets ans, the trap / how to read it fast)
PSEUDO = [
("bitwise", """Integer a, b
Set a = 12, b = 10
Print (a & b) + (a | b) + (a ^ b)""",
 "a,b=12,10; ans=(a&b)+(a|b)+(a^b)",
 "Write both in binary: 12 = 1100, 10 = 1010. & keeps bits set in both (1000 = 8), | keeps bits set in either (1110 = 14), ^ keeps bits that differ (0110 = 6)."),
("bitwise", """Integer x
Set x = 5
x = x << 3
x = x >> 1
Print x""",
 "x=5; x=x<<3; x=x>>1; ans=x",
 "x << k multiplies by 2^k, x >> k divides by 2^k (integer). 5 × 8 = 40, then 40 / 2."),
("loops", """Integer a, b, c, i
Set a = 1, b = 1
for (i = 1 to 5)
    c = a + b
    a = b
    b = c
end for
Print b""",
 "a=b=1\nfor i in range(1,6):\n    c=a+b; a=b; b=c\nans=b",
 "This is Fibonacci. Write a small table of a, b per iteration; never do it in your head."),
("digits", """Integer n, s
Set n = 1234, s = 0
while (n > 0)
    s = s * 10 + n mod 10
    n = n / 10
end while
Print s""",
 "n,s=1234,0\nwhile n>0:\n    s=s*10+n%10; n=cdiv(n,10)\nans=s",
 "'n mod 10' takes the last digit, 'n / 10' drops it (integer division). s*10 + digit builds the number backward: it reverses n."),
("digits", """Integer n, c, d
Set n = 5732, c = 0
while (n > 0)
    d = n mod 10
    if (d mod 2 == 1)
        c = c + 1
    end if
    n = n / 10
end while
Print c""",
 "n,c=5732,0\nwhile n>0:\n    d=n%10\n    if d%2==1: c+=1\n    n=cdiv(n,10)\nans=c",
 "It counts odd digits of 5732: 5, 7, 3 are odd."),
("loops", """Integer i, j, count
Set count = 0
for (i = 1 to 5)
    for (j = i to 5)
        count = count + 1
    end for
end for
Print count""",
 "count=0\nfor i in range(1,6):\n    for j in range(i,6): count+=1\nans=count",
 "Inner loop runs 5, 4, 3, 2, 1 times: 5+4+3+2+1 = n(n+1)/2."),
("loops", """Integer i, j, s
Set s = 0
for (i = 1 to 4)
    for (j = 1 to 4)
        if (j == i)
            break
        end if
        s = s + j
    end for
end for
Print s""",
 "s=0\nfor i in range(1,5):\n    for j in range(1,5):\n        if j==i: break\n        s+=j\nans=s",
 "break leaves only the INNER loop. For each i it adds 1..(i-1): 0 + 1 + 3 + 6."),
("recursion", """Function fun(Integer n)
    if (n <= 1)
        return 1
    end if
    return n + fun(n - 2)
End function
Print fun(7)""",
 "def fun(n):\n    return 1 if n<=1 else n+fun(n-2)\nans=fun(7)",
 "Expand it: 7 + fun(5) = 7 + 5 + fun(3) = 7 + 5 + 3 + fun(1), and fun(1) = 1."),
("recursion", """Function fun(Integer n)
    if (n <= 0)
        return 1
    end if
    return fun(n - 1) + fun(n - 2)
End function
Print fun(4)""",
 "def fun(n):\n    return 1 if n<=0 else fun(n-1)+fun(n-2)\nans=fun(4)",
 "Careful with the base case: fun(-1) and fun(0) are BOTH 1. Build up: fun(0)=1, fun(1)=fun(0)+fun(-1)=2, fun(2)=3, fun(3)=5, fun(4)=8."),
("arrays", """Integer arr[8] = {3, 1, 4, 1, 5, 9, 2, 6}
Integer i, s
Set s = 0
for (i = 0 to 7 step 2)
    s = s + arr[i]
end for
Print s""",
 "arr=[3,1,4,1,5,9,2,6]; ans=sum(arr[0:8:2])",
 "Indexes start at 0 and step 2: arr[0], arr[2], arr[4], arr[6] = 3, 4, 5, 2."),
("recognise", """Integer a, b, t
Set a = 48, b = 18
while (b != 0)
    t = b
    b = a mod b
    a = t
end while
Print a""",
 "a,b=48,18\nwhile b: a,b=b,a%b\nans=a",
 "Recognise it: this is Euclid's GCD. Once you recognise a loop, you don't need to trace it."),
("loops", """Integer i, p
Set p = 1
for (i = 1 to 10)
    if (i mod 3 == 0)
        p = p * 2
    end if
end for
Print p""",
 "p=1\nfor i in range(1,11):\n    if i%3==0: p*=2\nans=p",
 "Only i = 3, 6, 9 pass the test, so p doubles three times."),
("conditions", """Integer x, y
Set x = 15
if (x > 10 && x mod 2 == 0)
    y = 1
else if (x > 10 || x < 0)
    y = 2
else
    y = 3
end if
Print y""",
 "x=15\ny=1 if (x>10 and x%2==0) else (2 if (x>10 or x<0) else 3)\nans=y",
 "&& needs both sides true (15 is odd, so no). || needs only one (15 > 10, so yes)."),
("digits", """Integer n, f, i, c
Set n = 10, f = 1, c = 0
for (i = 1 to n)
    f = f * i
end for
while (f mod 10 == 0)
    c = c + 1
    f = f / 10
end while
Print c""",
 "f=1\nfor i in range(1,11): f*=i\nc=0\nwhile f%10==0: c+=1; f//=10\nans=c",
 "Trailing zeros of 10!: count the factors of 5 (5 and 10), which gives 2. Don't multiply it out."),
("loops", """Integer i, j, count, isPrime
Set count = 0
for (i = 2 to 20)
    isPrime = 1
    for (j = 2 to i - 1)
        if (i mod j == 0)
            isPrime = 0
        end if
    end for
    count = count + isPrime
end for
Print count""",
 "ans=sum(1 for i in range(2,21) if all(i%j for j in range(2,i)))",
 "Recognise it: this counts primes from 2 to 20 (2, 3, 5, 7, 11, 13, 17, 19)."),
("bitwise", """Integer n, c
Set n = 29, c = 0
while (n > 0)
    c = c + (n & 1)
    n = n >> 1
end while
Print c""",
 "ans=bin(29).count('1')",
 "n & 1 is the last bit, n >> 1 drops it. It counts the 1-bits: 29 = 11101."),
("bitwise", """Integer n, c
Set n = 40, c = 0
while (n != 0)
    n = n & (n - 1)
    c = c + 1
end while
Print c""",
 "ans=bin(40).count('1')",
 "n & (n-1) deletes the LOWEST set bit. The loop runs once per 1-bit: 40 = 101000."),
("bitwise", """Integer x, i
Set x = 0
for (i = 1 to 10)
    x = x ^ i
end for
Print x""",
 "x=0\nfor i in range(1,11): x^=i\nans=x",
 "XOR from 1 to n follows a cycle of 4: n mod 4 = 0 gives n, 1 gives 1, 2 gives n+1, 3 gives 0. 10 mod 4 = 2, so 11."),
("division", """Integer i, s
Set s = 0
for (i = 1 to 10)
    s = s + i / 3
end for
Print s""",
 "ans=sum(cdiv(i,3) for i in range(1,11))",
 "Integer division throws away the fraction: 1/3 = 0, 2/3 = 0, 3/3 = 1 ... 10/3 = 3."),
("recursion", """Function fun(Integer a, Integer b)
    if (b == 0)
        return 0
    end if
    return a + fun(a, b - 1)
End function
Print fun(6, 4)""",
 "def fun(a,b):\n    return 0 if b==0 else a+fun(a,b-1)\nans=fun(6,4)",
 "Recognise it: adding a, b times, is a × b."),
("recursion", """Function fun(Integer x, Integer n)
    if (n == 0)
        return 1
    end if
    if (n mod 2 == 0)
        return fun(x, n / 2) * fun(x, n / 2)
    end if
    return x * fun(x, n - 1)
End function
Print fun(2, 10)""",
 "ans=2**10",
 "Recognise it: fast power, x^n."),
("recursion", """Integer calls = 0
Function fun(Integer n)
    calls = calls + 1
    if (n <= 1)
        return
    end if
    fun(n - 1)
    fun(n - 2)
End function
fun(5)
Print calls""",
 "c=[0]\ndef fun(n):\n    c[0]+=1\n    if n<=1: return\n    fun(n-1); fun(n-2)\nfun(5); ans=c[0]",
 "Count calls with a table: C(0) = C(1) = 1, C(n) = 1 + C(n-1) + C(n-2). C(2)=3, C(3)=5, C(4)=9, C(5)=15."),
("arrays", """Integer arr[5] = {10, 20, 30, 40, 50}
Integer i, j, t
Set i = 0, j = 4
while (i < j)
    t = arr[i]
    arr[i] = arr[j]
    arr[j] = t
    i = i + 1
    j = j - 1
end while
Print arr[1]""",
 "arr=[10,20,30,40,50]; arr.reverse(); ans=arr[1]",
 "Two pointers swapping from both ends reverse the array. The array becomes 50 40 30 20 10."),
("loops", """Integer i, s
Set s = 0
for (i = 1 to 10)
    if (i mod 2 == 0)
        continue
    end if
    if (i > 7)
        break
    end if
    s = s + i
end for
Print s""",
 "s=0\nfor i in range(1,11):\n    if i%2==0: continue\n    if i>7: break\n    s+=i\nans=s",
 "continue skips the evens. The loop stops at i = 9, so it adds 1 + 3 + 5 + 7."),
("loops", """Integer i
Set i = 10
do
    i = i - 3
while (i > 0)
Print i""",
 "i=10\nwhile True:\n    i-=3\n    if not i>0: break\nans=i",
 "do-while runs the body BEFORE testing: 10 → 7 → 4 → 1 → −2, then the test fails."),
("bitwise", """Integer a, b
Set a = 3, b = 5
a = a ^ b
b = a ^ b
a = a ^ b
Print a * 10 + b""",
 "a,b=3,5; a^=b; b^=a; a^=b; ans=a*10+b",
 "This is the XOR swap: a and b trade values without a temporary variable."),
("bitwise", """Integer x, i
Set x = 0
for (i = 0 to 7)
    if ((100 >> i) & 1 == 1)
        x = x + i
    end if
end for
Print x""",
 "ans=sum(i for i in range(8) if (100>>i)&1)",
 "It adds the POSITIONS of the 1-bits. 100 = 64 + 32 + 4, so positions 6, 5 and 2."),
("arrays", """Integer m[3][3], i, j, s
for (i = 0 to 2)
    for (j = 0 to 2)
        m[i][j] = i * 3 + j
    end for
end for
Set s = 0
for (i = 0 to 2)
    for (j = 0 to 2)
        if (i == j || i + j == 2)
            s = s + m[i][j]
        end if
    end for
end for
Print s""",
 "ans=sum(i*3+j for i in range(3) for j in range(3) if i==j or i+j==2)",
 "Both diagonals: 0, 4, 8 and 2, 4, 6. The centre (4) is ONE cell, so it is counted once."),
("division", """Integer a, b
Set a = 17, b = 5
Print a / b * b + a mod b""",
 "a,b=17,5; ans=cdiv(a,b)*b+a%b",
 "(a / b) × b + a mod b always gives back a. That is the definition of quotient and remainder."),
("recognise", """Integer n, steps
Set n = 6, steps = 0
while (n != 1)
    if (n mod 2 == 0)
        n = n / 2
    else
        n = 3 * n + 1
    end if
    steps = steps + 1
end while
Print steps""",
 "n,s=6,0\nwhile n!=1:\n    n = n//2 if n%2==0 else 3*n+1; s+=1\nans=s",
 "Just trace it: 6, 3, 10, 5, 16, 8, 4, 2, 1. Count the arrows, not the numbers."),
("loops", """Integer i, s
Set s = 0
for (i = 1 to 100)
    if (i mod 3 == 0 || i mod 5 == 0)
        s = s + 1
    end if
end for
Print s""",
 "ans=sum(1 for i in range(1,101) if i%3==0 or i%5==0)",
 "Inclusion-exclusion: 33 multiples of 3, plus 20 of 5, minus 6 of 15."),
("conditions", """Integer a, b, c
Set a = 4, b = 9, c = 6
if (a > b)
    if (a > c) Print a
    else Print c
else
    if (b > c) Print b
    else Print c
end if""",
 "ans=max(4,9,6)",
 "Recognise it: nested ifs that print the largest of three."),
]


def options_for(ans, seed):
    rnd = random.Random(seed)
    pool = [ans + 1, ans - 1, ans + 2, ans - 2, ans * 2, ans + 3, ans + 10, ans - 3, ans // 2 if ans > 3 else ans + 4]
    pool = [p for p in dict.fromkeys(pool) if p != ans]
    rnd.shuffle(pool)
    opts = pool[:3] + [ans]
    rnd.shuffle(opts)
    return opts


pseudo_out = []
for i, (topic, code, py, note) in enumerate(PSEUDO):
    env = {"cdiv": cdiv}
    exec(py, env)
    ans = env["ans"]
    assert isinstance(ans, int), (i, ans)
    opts = options_for(ans, i)
    pseudo_out.append({"topic": topic, "code": code, "opts": [str(o) for o in opts], "a": opts.index(ans), "why": note})


# ------------------------------------------------------------------ PUZZLES (brute-forced) --------------------
def unique(perms, ok, name):
    sols = [p for p in perms if ok(p)]
    assert len(sols) == 1, (name, len(sols))
    return sols[0]

P5 = "ABCDE"
row = unique(itertools.permutations(P5), lambda p: p.index("C") == 2 and p.index("A") == 1 and p.index("E") in (0, 4)
             and abs(p.index("B") - 2) != 1 and p.index("B") < p.index("E"), "row")
tall = unique(itertools.permutations("PQRST"), lambda p: p.index("Q") < p.index("R") and p.index("T") < p.index("Q")
              and p.index("R") < p.index("P") and p[0] == "S", "tall")                     # p[0] = tallest
flr = unique(itertools.permutations("KLMNO"), lambda p: (p.index("M") + 1) % 2 == 0 and p.index("K") == p.index("M") + 1
             and p.index("L") == 4 and p.index("N") < p.index("O"), "floors")             # p[0] = floor 1
box = unique(itertools.permutations(["apples", "mangoes", "grapes"]), lambda p: p[0] not in ("apples", "grapes") and p[1] != "apples", "box")
num = next(x for x in range(1, 10000) if all(x % d == 1 for d in (2, 3, 4, 5, 6)) and x % 7 == 0)
sq = sum((8 - k + 1) ** 2 for k in range(1, 9))
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
today = days[(days.index("Sunday") - 2) % 7]
before_yday = days[(days.index(today) - 2) % 7]
hs = next(n for n in range(1, 100) if n * (n - 1) // 2 == 66)


def puzzle(q, ans, wrong, why):
    opts = [ans] + wrong
    random.Random(q).shuffle(opts)
    return {"q": q, "opts": [str(o) for o in opts], "a": opts.index(ans), "why": why}

PUZZLES = [
    puzzle("Five people A, B, C, D, E sit in a row facing north. C sits in the middle. A sits immediately to the left of C. E sits at one of the ends. B does not sit next to C, and B sits somewhere to the left of E. Who sits at the right end?",
           row[4], [x for x in "ABD" if x != row[4]][:3], "C is 3rd and A is 2nd. B cannot be 2nd or 4th, so B is at an end. E is also at an end, and B is left of E, so B is 1st and E is 5th. D is 4th. Order: " + " ".join(row) + "."),
    puzzle("P, Q, R, S and T have different heights. Q is taller than R but shorter than T. P is shorter than R. S is the tallest. Who is the third tallest?",
           tall[2], [x for x in "TRP" if x != tall[2]], "Chain the facts: S > T > Q > R > P."),
    puzzle("K, L, M, N and O live on floors 1 (bottom) to 5 (top) of a building, one person per floor. M lives on an even floor. K lives directly above M. L lives on the top floor. N lives below O. Who lives on floor 1?",
           flr[0], [x for x in "OKM" if x != flr[0]], "L is on 5. If M were on 4, K would be on 5 (taken), so M is on 2 and K on 3. N and O share floors 1 and 4, and N is lower. Bottom to top: " + " ".join(flr) + "."),
    puzzle("A red box, a blue box and a green box hold apples, mangoes and grapes, one fruit each. The red box holds neither apples nor grapes. The blue box does not hold apples. What is in the green box?",
           box[2], [x for x in ("mangoes", "grapes", "bananas")], "Red can only hold mangoes. Blue then cannot hold apples, so it holds grapes, and green holds apples."),
    puzzle("What is the smallest positive number that leaves remainder 1 when divided by 2, 3, 4, 5 or 6, and is exactly divisible by 7?",
           num, [61, 121, 241], "Remainder 1 by each means the number is LCM(2..6) × k + 1 = 60k + 1. Try k = 1, 2, 3 ... until it divides by 7: 61, 121, 181, 241, 301."),
    puzzle("How many squares of ANY size are there on an 8 × 8 chessboard?", sq, [64, 196, 256], "1×1: 64, 2×2: 49, 3×3: 36 ... 8×8: 1. It is the sum of the squares 1² + 2² + ... + 8²."),
    puzzle("The day after tomorrow is Sunday. What was the day before yesterday?", before_yday, [d for d in ("Thursday", "Friday", "Tuesday") if d != before_yday][:3],
           "Today is " + today + ". Two days back from it is " + before_yday + "."),
    puzzle("At a meeting every person shook hands with every other person exactly once. There were 66 handshakes in total. How many people were there?",
           hs, [11, 13, 33], "n people make n(n−1)/2 handshakes. n(n−1) = 132 = 12 × 11."),
    puzzle("You have 9 identical-looking coins. One is heavier. Using a balance scale, what is the fewest number of weighings that always finds the heavy coin?",
           2, [1, 3, 4], "Split into three groups of 3. Weigh two groups: the heavier side (or the unweighed group if they balance) has it. Repeat with 3 coins: 1 vs 1. Each weighing divides by 3, and 3² = 9."),
]


# ------------------------------------------------------------------ VERBAL (hand-written, rule given) ----------
def vq(q, opts, a, why):
    return {"q": q, "opts": opts, "a": a, "why": why}

VERBAL = [
    vq("Neither the manager nor the employees ___ aware of the change.", ["was", "were", "is", "has been"], 1, "With neither/nor and either/or, the verb agrees with the NEARER subject: 'employees', so plural."),
    vq("Each of the students ___ submitted the form.", ["have", "are", "has", "were"], 2, "'Each', 'every', 'one of' take a singular verb."),
    vq("One of my friends ___ in Mysuru.", ["live", "lives", "are living", "have lived"], 1, "The subject is 'one', not 'friends'. Singular."),
    vq("He has been working here ___ 2022.", ["for", "from", "since", "by"], 2, "'since' + a point in time, 'for' + a length of time (for three years)."),
    vq("She is senior ___ me by two years.", ["than", "to", "from", "over"], 1, "senior, junior, superior, inferior, prior and prefer all take 'to', never 'than'."),
    vq("She prefers tea ___ coffee.", ["than", "over", "to", "from"], 2, "prefer X TO Y."),
    vq("If I ___ you, I would accept the offer.", ["was", "am", "were", "had been"], 2, "An imagined present condition uses 'were' for every subject."),
    vq("He insisted ___ paying the bill.", ["for", "on", "at", "to"], 1, "insist ON, depend ON, rely ON."),
    vq("I look forward to ___ you.", ["meet", "meeting", "met", "be meeting"], 1, "In 'look forward to', 'to' is a preposition, so it takes the -ing form."),
    vq("Hardly had I reached the station ___ the train left.", ["than", "when", "then", "that"], 1, "Hardly / scarcely ... WHEN. No sooner ... THAN."),
    vq("No sooner had he finished his speech ___ the audience started clapping.", ["when", "then", "than", "as"], 2, "No sooner ... THAN."),
    vq("The news ___ good.", ["are", "were", "is", "have been"], 2, "'news', 'information', 'furniture', 'advice' and 'equipment' are uncountable and singular."),
    vq("The committee has submitted ___ report.", ["their", "its", "it's", "there"], 1, "The verb 'has' treats the committee as one unit, so 'its' (possessive; it's = it is)."),
    vq("Between you and ___, the plan will not work.", ["I", "me", "myself", "mine"], 1, "After a preposition (between), use the object form: me."),
    vq("The cost of living ___ risen sharply this year.", ["have", "are", "has", "were"], 2, "The subject is 'cost' (singular). 'of living' does not change it."),
    vq("Find the error.  (A) Despite of the rain  /  (B) the match continued  /  (C) as scheduled.  /  (D) No error", ["A", "B", "C", "D"], 0, "'despite' never takes 'of'. Use 'despite the rain' or 'in spite of the rain'."),
    vq("Find the error.  (A) Each of the boys  /  (B) have brought  /  (C) his own lunch.  /  (D) No error", ["A", "B", "C", "D"], 1, "'Each of' is singular: 'has brought'. The 'his' in (C) confirms it."),
    vq("Find the error.  (A) The furniture in the room  /  (B) were all new  /  (C) and expensive.  /  (D) No error", ["A", "B", "C", "D"], 1, "'furniture' is uncountable, so 'was'."),
    vq("Find the error.  (A) I have seen  /  (B) that film  /  (C) yesterday.  /  (D) No error", ["A", "B", "C", "D"], 0, "A finished past time (yesterday, last week, in 2020) needs the simple past: 'I saw'."),
    vq("Find the error.  (A) He is the most  /  (B) intelligent and hard-working  /  (C) student in the class.  /  (D) No error", ["A", "B", "C", "D"], 3, "Correct as written. Don't hunt for an error that isn't there; 'No error' is a real answer."),
    vq("Choose the correct sentence.", ["He don't like coffee.", "He doesn't likes coffee.", "He doesn't like coffee.", "He not like coffee."], 2, "After does / doesn't / did, use the base form of the verb."),
    vq("Choose the correctly spelt word.", ["accomodate", "acommodate", "accommodate", "accommadate"], 2, "Double c and double m."),
    vq("Synonym of METICULOUS:", ["careless", "careful", "quick", "proud"], 1, "Meticulous means paying close attention to detail."),
    vq("Antonym of TRANSPARENT:", ["clear", "opaque", "bright", "thin"], 1, "Opaque means light cannot pass through it."),
    vq("Arrange into a paragraph.  P: He took the stairs instead.  Q: The lift was out of order.  R: Ravi reached the office early.  S: By the time he reached the tenth floor he was out of breath.",
       ["QRPS", "RQPS", "RPQS", "SRQP"], 1, "Find the opener: R introduces Ravi (the others say 'he'). The cause (Q) comes before the action (P), and the result (S) comes last."),
    vq("Arrange into a paragraph.  P: Then the dough is left to rise for an hour.  Q: First, flour, water and yeast are mixed.  R: Finally, it is baked until golden.  S: After rising, it is shaped into loaves.",
       ["QPSR", "QSPR", "PQSR", "QPRS"], 0, "Follow the signal words: First, Then, After rising, Finally."),
]

RC = {
    "text": ("Many first-year engineers assume that writing more code is the fastest way to become productive. In practice, "
             "the engineers who are trusted earliest are usually the ones who read before they write. They study how an existing "
             "system behaves, ask what problem a piece of code was meant to solve, and only then propose a change. This habit "
             "slows them down for a few weeks, but it saves months later, because their changes rarely break something they "
             "did not understand. Managers notice this quickly: an engineer whose work does not need to be redone is given "
             "harder problems sooner."),
    "qs": [
        vq("What is the main idea of the passage?", ["Writing more code makes engineers productive", "Understanding a system before changing it earns trust faster",
                                                     "Managers prefer slow engineers", "New engineers should avoid existing systems"], 1, "Every sentence supports 'read before you write' and the trust it earns."),
        vq("According to the passage, why does the habit save time later?", ["It lets engineers skip testing", "Their changes rarely break things they did not understand",
                                                                               "Managers give them easier work", "They write less code overall"], 1, "Stated directly: their changes rarely break something they did not understand."),
        vq("The word 'trusted' in the passage is closest in meaning to:", ["feared", "relied upon", "promoted", "tested"], 1, "Being trusted with work means being relied upon."),
    ],
}


# ------------------------------------------------------------------ INTERVIEW --------------------------------
TECH = [
    ("OOP", "What are the four pillars of OOP?", "Encapsulation (data + methods bundled, access controlled), Abstraction (show what, hide how), Inheritance (a child reuses a parent), Polymorphism (one name, many forms). Give a one-line example of each, such as a BankAccount class."),
    ("OOP", "Overloading vs overriding?", "Overloading: same method name, different parameters, in the SAME class, resolved at compile time. Overriding: a child class redefines a parent's method with the same signature, resolved at run time."),
    ("OOP", "Abstract class vs interface?", "An abstract class can hold state and some implemented methods; a class extends only one. An interface is a contract; a class can implement many. Use an interface for 'can do', an abstract class for 'is a' with shared code."),
    ("OOP", "Class vs object?", "A class is the blueprint, an object is one instance of it in memory. 'Car' is a class; your specific car is an object."),
    ("DBMS", "Primary key vs unique key?", "Both are unique. A primary key cannot be NULL, and a table has only one. A table can have many unique keys, and they allow NULL."),
    ("DBMS", "DELETE vs TRUNCATE vs DROP?", "DELETE removes chosen rows (WHERE), is logged and can be rolled back. TRUNCATE removes all rows quickly but keeps the table. DROP removes the table itself."),
    ("DBMS", "What is normalisation? 1NF, 2NF, 3NF?", "Splitting tables to remove redundancy. 1NF: atomic values. 2NF: no column depends on only PART of a composite key. 3NF: no column depends on another non-key column."),
    ("SQL", "Second highest salary?", "SELECT MAX(salary) FROM emp WHERE salary < (SELECT MAX(salary) FROM emp);  — or DENSE_RANK() = 2 for the general N-th."),
    ("SQL", "Types of JOIN?", "INNER (only matches), LEFT (all left rows + matches), RIGHT, FULL OUTER (all from both), CROSS (every pair), SELF (a table joined to itself, such as employee and manager)."),
    ("OS", "Process vs thread?", "A process is a running program with its own memory. Threads live inside a process and share its memory, so they are cheaper to create, but you need locks for shared data."),
    ("OS", "What is a deadlock? Its four conditions?", "Processes wait on each other forever. All four must hold: mutual exclusion, hold and wait, no preemption, circular wait. Break any one to prevent it."),
    ("OS", "Paging vs segmentation?", "Paging splits memory into fixed-size pages (no external fragmentation). Segmentation splits by logical units like code and stack (variable size)."),
    ("CN", "TCP vs UDP?", "TCP: connection-based, reliable, ordered (web, email). UDP: no connection, no guarantee, fast (video calls, games, DNS)."),
    ("CN", "What happens when you type a URL?", "DNS lookup → TCP connection (+ TLS for https) → HTTP request → server responds → browser renders HTML, fetches CSS, JS and images."),
    ("Python", "List vs tuple?", "A list is mutable, a tuple is immutable (so a tuple can be a dict key and is slightly faster). Both are ordered."),
    ("Python", "== vs is?", "== compares values, 'is' compares identity (the same object in memory)."),
    ("C / Java", "What is a pointer? (C)  /  JDK vs JRE vs JVM? (Java)", "A pointer stores a memory address. JVM runs bytecode; JRE = JVM + libraries to run; JDK = JRE + compiler and tools to develop."),
    ("Coding", "Be ready to write these on paper", "Reverse a string, palindrome check, prime check, factorial, Fibonacci, swap two numbers without a temp variable, second largest in an array, count vowels, sum of digits. Say your logic out loud while writing."),
]

HR = [
    ("Tell me about yourself.", "60–90 seconds, in this order: name and branch at BMSIT → strongest skills (a language, DSA, SQL) → ONE project in one line → why this role. Don't repeat your resume line by line. Practise it out loud three times tonight."),
    ("Explain your project.", "Use problem → what you built → your part → one hard problem you solved → result. Your placement hub is a good answer: a Python local server, generated practice pages, a fuzz-tested visualiser, an AI coach that marks your answers. Say what YOU decided and why."),
    ("Why Infosys?", "Be specific: structured training before the first project, work across many clients and domains, a big learning curve in the first two years. Avoid 'it's a big company'."),
    ("Are you willing to relocate / work in shifts?", "Yes. Infosys hires for any location and training is usually away from home. A hesitant answer here is a common reason for rejection."),
    ("Strengths and weaknesses?", "One strength backed by a story (you built a full tool on your own). One real weakness with what you're doing about it, such as 'I used to jump into code too fast, so now I write the approach first.'"),
    ("Where do you see yourself in five years?", "Growing within the company: strong in one technology, leading a small module, trusted by clients. Don't say 'studying for an MS' or 'starting my own company'."),
    ("Do you have any questions for us?", "Always ask one: 'What technologies would freshers in this role typically work on after training?' or 'What does success look like in the first six months?'"),
]

PLAN = [
    ("Tonight (12 Nov) — 1", "Pseudocode drill below, all of it. This section is Infosys-specific and the one most students don't prepare.", "#pseudo"),
    ("Tonight — 2", "Aptitude Sprint: one timed set each of percentages, ratios, time and work, speed, and seating / blood relations / syllogisms.", "/t/7%20-%20Aptitude%20Sprint%20(formulas%20%2B%20practice).html"),
    ("Tonight — 3", "Verbal and puzzle sections below. Read every explanation; the rules repeat.", "#verbal"),
    ("Tonight — 4", "Say your 'tell me about yourself' and project answer out loud, three times. Then sleep. The test starts at 9 AM.", "#hr"),
    ("Morning (13 Nov)", "Skim the pseudocode traps and the verbal rules once. Don't learn anything new.", "#pseudo"),
    ("Evening (13 Nov), if shortlisted", "Technical Q&A below, then CS Core Drill exam mode and the SQL Lab interview section.", "#tech"),
]

DAYOF = [
    "Read the 'Assessment Guidelines' attachment from the placement email. It is the official word on sections and rules, and it overrides anything here.",
    "Complete the Infosys Application Form when it arrives, using your PERSONAL email. College email addresses are rejected.",
    "Carry your college ID, a government ID, printed resume copies and a pen. Charge your phone in case you need OTPs.",
    "Each section usually has its own cut-off, so don't sink time into one section. Mark anything over 90 seconds, move on, come back.",
    "Pseudocode: trace with a table (one column per variable) on rough paper. Don't trace in your head.",
    "Interview day (14 Nov): formal clothes, reach early, and be ready to explain every line of your resume.",
]


# ------------------------------------------------------------------ page --------------------------------------
DATA = {"pseudo": pseudo_out, "puzzles": PUZZLES, "verbal": VERBAL, "rc": RC, "tech": TECH, "hr": HR, "plan": PLAN, "dayof": DAYOF}

PAGE = r"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Infosys Drive</title>
<style>
:root{--bg:#0b1117;--card:#111a22;--edge:#1f2c38;--ink:#d8e2ea;--dim:#8a9aa8;--acc:#4fb3ff;--ok:#3ecf8e;--bad:#ff6b6b;--warn:#ffcc66}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 system-ui,Segoe UI,sans-serif}
.wrap{max-width:min(1200px,96vw);margin:0 auto;padding:18px 16px 80px}
h1{font-size:24px;margin:6px 0 2px}h2{font-size:19px;margin:34px 0 10px;padding-top:8px;border-top:1px solid var(--edge)}
.sub{color:var(--dim)}a{color:var(--acc)}
nav{position:sticky;top:0;background:var(--bg);padding:10px 0;z-index:5;display:flex;flex-wrap:wrap;gap:6px;border-bottom:1px solid var(--edge)}
nav a{padding:4px 10px;border:1px solid var(--edge);border-radius:6px;text-decoration:none;font-size:13px}
.card{background:var(--card);border:1px solid var(--edge);border-radius:10px;padding:14px 16px;margin:10px 0}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:10px}
.grid .card{margin:0}
pre{background:#071018;border:1px solid var(--edge);border-radius:8px;padding:10px 12px;overflow:auto;font:13.5px/1.45 Consolas,monospace;margin:8px 0}
.opts{display:flex;flex-wrap:wrap;gap:8px;margin-top:8px}
.opts button{background:#0d1821;color:var(--ink);border:1px solid var(--edge);border-radius:7px;padding:6px 14px;cursor:pointer;font:inherit}
.opts button:hover{border-color:var(--acc)}.opts button.ok{border-color:var(--ok);color:var(--ok)}.opts button.bad{border-color:var(--bad);color:var(--bad)}
.why{display:none;margin-top:8px;color:var(--dim);border-left:3px solid var(--acc);padding-left:10px}.why.show{display:block}
.tag{font-size:11px;color:var(--dim);border:1px solid var(--edge);border-radius:4px;padding:1px 6px;margin-right:6px}
.score{color:var(--warn);font-weight:600}
.q{font-weight:500}
table{border-collapse:collapse;width:100%}td{border-bottom:1px solid var(--edge);padding:8px 6px;vertical-align:top}td:first-child{white-space:nowrap;color:var(--warn);width:1%}
details{margin:6px 0}summary{cursor:pointer;font-weight:500}details .ans{color:var(--dim);margin:6px 0 4px 16px}
.bar{display:flex;gap:10px;align-items:center;flex-wrap:wrap}.bar button{background:none;border:1px solid var(--edge);color:var(--dim);border-radius:6px;padding:3px 10px;cursor:pointer}
ul{margin:6px 0;padding-left:20px}li{margin:4px 0}
</style></head><body><div class="wrap">
<h1>Infosys drive: test 13 Nov, interviews 14 Nov</h1>
<div class="sub">Systems Engineer (Trainee). The test is in person on campus, with 9 AM and 11:30 AM slots. Shortlisted students are interviewed face to face the next day.</div>
<nav><a href="#plan">Plan</a><a href="#pattern">Test pattern</a><a href="#pseudo">Pseudocode</a><a href="#puzzle">Puzzles</a><a href="#verbal">Verbal</a><a href="#tech">Technical</a><a href="#hr">HR</a><a href="#dayof">Checklist</a><a href="/">Home</a></nav>

<h2 id="plan">The plan until the test</h2><table id="planT"></table>

<h2 id="pattern">What the test usually looks like</h2>
<div class="card">Infosys has not published the exact pattern, and the prep sites disagree, so the attached <b>Assessment Guidelines</b> from your placement cell overrides this. The most reported shape for the SE test: about 100 minutes, <b>sectional cut-offs</b>, <b>no negative marking</b> (so never leave a question blank), five sections:
<div class="grid" style="margin-top:10px">
<div class="card"><b>Mathematical ability</b><br><span class="sub">Percentages, ratios, time and work, speed, number system, P&amp;C, probability.</span><br><a href="/t/7%20-%20Aptitude%20Sprint%20(formulas%20%2B%20practice).html">Aptitude Sprint → Quantitative</a></div>
<div class="card"><b>Logical / analytical reasoning</b><br><span class="sub">Seating, blood relations, syllogisms, series, coding-decoding, directions.</span><br><a href="/t/7%20-%20Aptitude%20Sprint%20(formulas%20%2B%20practice).html">Aptitude Sprint → Logical reasoning</a></div>
<div class="card"><b>Verbal ability</b><br><span class="sub">Grammar, error spotting, fill in the blank, para jumbles, reading comprehension.</span><br><a href="#verbal">Verbal section below</a></div>
<div class="card"><b>Pseudocode</b><br><span class="sub">Trace C-like code: loops, bitwise operators, recursion, integer division.</span><br><a href="#pseudo">Pseudocode drill below</a></div>
<div class="card"><b>Puzzle solving</b><br><span class="sub">Arrangement puzzles and number puzzles.</span><br><a href="#puzzle">Puzzles below</a></div>
</div></div>

<h2 id="pseudo">Pseudocode drill</h2>
<div class="sub">Every answer below was computed by running the code, so the key cannot be wrong. Rules: <b>a / b</b> is integer division (drop the fraction), <b>mod</b> is the remainder, <b>&amp; | ^</b> are bitwise AND, OR and XOR, <b>&lt;&lt; &gt;&gt;</b> shift bits, <b>&amp;&amp; ||</b> are logical AND and OR.</div>
<div class="bar"><span class="score" id="s-pseudo"></span><button onclick="reset('pseudo')">reset</button></div><div id="pseudo-list"></div>

<h2 id="puzzle">Puzzle solving</h2>
<div class="sub">Each arrangement puzzle was solved by checking every possible arrangement, so the answers are certain. Draw the slots on paper before you read the clues.</div>
<div class="bar"><span class="score" id="s-puzzle"></span><button onclick="reset('puzzle')">reset</button></div><div id="puzzle-list"></div>

<h2 id="verbal">Verbal ability</h2>
<div class="sub">Every explanation states a rule that comes back again and again. Learn the rules, not the questions.</div>
<div class="bar"><span class="score" id="s-verbal"></span><button onclick="reset('verbal')">reset</button></div><div id="verbal-list"></div>
<div class="card"><b>Reading comprehension</b><p id="rc-text"></p><div id="rc-list"></div></div>

<h2 id="tech">Technical interview — the questions that keep coming</h2>
<div class="sub">Click a question, answer it OUT LOUD, then open the answer. More depth: <a href="/t/6%20-%20CS%20Core%20Drill%20(OS%20DBMS%20CN%20OOP%20C).html">CS Core Drill</a> and the <a href="/t/5%20-%20SQL%20Lab%20(practice).html">SQL Lab</a> interview section.</div>
<div id="tech-list"></div>

<h2 id="hr">HR questions</h2><div id="hr-list"></div>

<h2 id="dayof">Test-day checklist</h2><div class="card"><ul id="dayofL"></ul></div>
</div>
<script>
var D = __DATA__;
function el(t, c, x) { var e = document.createElement(t); if (c) e.className = c; if (x != null) e.textContent = x; return e; }
var KEY = "infosys-drive-v1", S = {};
try { S = JSON.parse(localStorage.getItem(KEY) || "{}"); } catch (e) { S = {}; }
function save() { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) {} }
function score(sec, n) {
  var r = 0, a = 0; for (var k in S) if (k.indexOf(sec + ":") === 0) { a++; if (S[k]) r++; }
  var s = document.getElementById("s-" + sec); if (s) s.textContent = r + " right of " + a + " tried, " + n + " in total";
}
function reset(sec) { for (var k in S) if (k.indexOf(sec + ":") === 0) delete S[k]; save(); render(); }
function mcq(sec, i, item, host, total, pre) {
  var c = el("div", "card");
  if (item.topic) c.appendChild(el("span", "tag", item.topic));
  c.appendChild(el("span", "q", (i + 1) + ". " + (item.q || "What does this print?")));
  if (pre) { var p = el("pre"); p.textContent = pre; c.appendChild(p); }
  var o = el("div", "opts"), w = el("div", "why", item.why), id = sec + ":" + i, bs = [];
  item.opts.forEach(function (t, j) {
    var b = el("button", null, String.fromCharCode(65 + j) + ")  " + t); bs.push(b);
    b.onclick = function () {
      if (!(id in S)) { S[id] = j === item.a; save(); }
      bs.forEach(function (x, k) { x.className = k === item.a ? "ok" : (k === j ? "bad" : ""); });
      w.className = "why show"; score(sec, total);
    };
    o.appendChild(b);
  });
  if (id in S) { bs[item.a].className = "ok"; w.className = "why show"; }
  c.appendChild(o); c.appendChild(w); host.appendChild(c);
}
function render() {
  ["pseudo", "puzzle", "verbal"].forEach(function (s) { document.getElementById(s + "-list").innerHTML = ""; });
  D.pseudo.forEach(function (q, i) { mcq("pseudo", i, q, document.getElementById("pseudo-list"), D.pseudo.length, q.code); });
  D.puzzles.forEach(function (q, i) { mcq("puzzle", i, q, document.getElementById("puzzle-list"), D.puzzles.length); });
  D.verbal.forEach(function (q, i) { mcq("verbal", i, q, document.getElementById("verbal-list"), D.verbal.length + D.rc.qs.length); });
  var rl = document.getElementById("rc-list"); rl.innerHTML = "";
  D.rc.qs.forEach(function (q, i) { mcq("verbal", 100 + i, q, rl, D.verbal.length + D.rc.qs.length); });
  ["pseudo", "puzzle"].forEach(function (s) { score(s, D[s === "puzzle" ? "puzzles" : s].length); });
  score("verbal", D.verbal.length + D.rc.qs.length);
}
document.getElementById("rc-text").textContent = D.rc.text;
var pt = document.getElementById("planT");
D.plan.forEach(function (p) { var tr = el("tr"); tr.appendChild(el("td", null, p[0])); var td = el("td", null, p[1] + " "); var a = el("a", null, "go →"); a.href = p[2]; td.appendChild(a); tr.appendChild(td); pt.appendChild(tr); });
function qa(list, host, tagged) {
  list.forEach(function (x) { var d = el("details", "card"); var s = el("summary"); if (tagged) s.appendChild(el("span", "tag", x[0])); s.appendChild(document.createTextNode(tagged ? x[1] : x[0]));
    d.appendChild(s); d.appendChild(el("div", "ans", tagged ? x[2] : x[1])); host.appendChild(d); });
}
qa(D.tech, document.getElementById("tech-list"), true);
qa(D.hr, document.getElementById("hr-list"), false);
D.dayof.forEach(function (t) { document.getElementById("dayofL").appendChild(el("li", null, t)); });
render();
</script></body></html>"""

page = PAGE.replace("__DATA__", json.dumps(DATA, ensure_ascii=False).replace("</", "<\\/"))
open(OUT, "w", encoding="utf-8").write(page)
print("built", os.path.basename(OUT), "| pseudocode %d, puzzles %d, verbal %d + RC %d, technical %d, HR %d" %
      (len(pseudo_out), len(PUZZLES), len(VERBAL), len(RC["qs"]), len(TECH), len(HR)))
