"""Extra quiz-only questions for the SQL Lab quiz mode.
 1. Functional-dependency / key / normal-form calculations, generated and verified by code.
 2. 'What does this query return?' on the sample database, answers produced by actually running the query.
 3. Hand-written scenario, DDL, PostgreSQL-vs-MySQL, trigger and transaction questions.
Each question: {"area", "q", "o" (4 options), "a", "w"}."""
import json
import random
import sqlite3
from itertools import combinations

A_FD = "Keys and normal forms (calculate)"
A_SQL = "Predict the query result"
A_SCN = "Scenarios and design"
A_RDB = "PostgreSQL vs MySQL"
A_TRX = "Transactions and triggers"

ALL_AREAS = [A_FD, A_SQL, A_SCN, A_RDB, A_TRX]


# ---------------------------------------------------------------- FD machinery
def closure(attrs, fds):
    res = set(attrs)
    changed = True
    while changed:
        changed = False
        for l, r in fds:
            if set(l) <= res and not set(r) <= res:
                res |= set(r)
                changed = True
    return res


def subsets(R):
    for k in range(1, len(R) + 1):
        for c in combinations(R, k):
            yield frozenset(c)


def candidate_keys(R, fds):
    sup = [s for s in subsets(R) if closure(s, fds) >= set(R)]
    return [k for k in sup if not any(o < k for o in sup)]


def super_key_count(R, fds):
    return sum(1 for s in subsets(R) if closure(s, fds) >= set(R))


def highest_nf(R, fds):
    keys = candidate_keys(R, fds)
    prime = set().union(*keys)
    nonprime = set(R) - prime
    def is_super(x): return closure(x, fds) >= set(R)
    bcnf = all(is_super(l) or set(r) <= set(l) for l, r in fds)
    nf3 = all(is_super(l) or all(a in l or a in prime for a in r) for l, r in fds)
    nf2 = True
    for k in keys:
        for sub in subsets(k):
            if sub < k and (closure(sub, fds) & nonprime) - set(sub):
                nf2 = False
    if bcnf: return "BCNF"
    if nf3: return "3NF"
    if nf2: return "2NF"
    return "1NF"


def fmt_set(s): return "{" + ",".join(sorted(s)) + "}"
def fmt_fd(f): return "".join(sorted(f[0])) + " → " + "".join(sorted(f[1]))
def fmt_F(fds): return "{ " + ", ".join(fmt_fd(f) for f in fds) + " }"
def fmt_keys(ks): return ", ".join(fmt_set(k) for k in sorted(ks, key=lambda k: (len(k), sorted(k))))


def random_schema(rng, n):
    R = list("ABCDEF"[:n])
    for _ in range(200):
        nfd = rng.randint(2, 4)
        fds = []
        for _ in range(nfd):
            lhs = tuple(sorted(rng.sample(R, rng.choice([1, 1, 2]))))
            rest = [x for x in R if x not in lhs]
            rhs = tuple(sorted(rng.sample(rest, rng.choice([1, 1, 2]))))
            if (lhs, rhs) not in fds:
                fds.append((lhs, rhs))
        keys = candidate_keys(R, fds)
        if keys and len(keys[0]) < n:
            return R, fds
    return R, [(("A",), ("B",))]


def mkq(area, q, right, wrongs, why, rng):
    right = str(right)
    ws = []
    for w in wrongs:
        w = str(w)
        if w != right and w not in ws:
            ws.append(w)
    if len(ws) < 3:
        return None
    opts = [right] + ws[:3]
    rng.shuffle(opts)
    return {"area": area, "q": q, "o": opts, "a": opts.index(right), "w": why}


def gen_fd(rng, target=70):
    out, seen = [], set()
    kinds = ["key", "nf", "closure", "nkeys", "nsuper", "implied", "prime"]
    guard = 0
    while len(out) < target and guard < 4000:
        guard += 1
        n = rng.choice([4, 4, 5])
        R, fds = random_schema(rng, n)
        sig = (tuple(R), tuple(fds))
        kind = kinds[len(out) % len(kinds)]
        if sig in seen and guard < 3000:
            continue
        head = "R(" + ", ".join(R) + ") with F = " + fmt_F(fds) + ". "
        keys = candidate_keys(R, fds)
        q = None
        if kind == "key":
            right = fmt_keys(keys)
            wr = []
            for _ in range(10):
                s = frozenset(rng.sample(R, rng.randint(1, min(3, n))))
                alt = [s] if rng.random() < .6 else [s, frozenset(rng.sample(R, 1))]
                wr.append(fmt_keys(alt))
            wr.append(fmt_keys([min(keys, key=len) | {rng.choice(R)}]))
            q = mkq(A_FD, head + "What are the candidate key(s)?", right, wr,
                    "Attributes that appear on no right-hand side must be in every key; then test closures. Keys: " + right + ".", rng)
        elif kind == "nf":
            right = highest_nf(R, fds)
            q = mkq(A_FD, head + "What is the highest normal form of R?", right, ["1NF", "2NF", "3NF", "BCNF"],
                    "Keys: " + fmt_keys(keys) + ". Check partial dependencies (2NF), then each X → A for X being a super key or A prime (3NF), then every determinant a super key (BCNF).", rng)
        elif kind == "closure":
            x = frozenset(rng.sample(R, rng.choice([1, 2])))
            c = closure(x, fds)
            if c == x: continue
            wr = []
            for extra in R:
                wr.append(fmt_set(c - {extra} if extra in c and extra not in x else c | {extra}))
            wr.append(fmt_set(x))
            q = mkq(A_FD, head + "What is the closure of " + fmt_set(x) + "?", fmt_set(c), wr,
                    "Start from " + fmt_set(x) + " and keep applying FDs whose left side is already inside: result " + fmt_set(c) + ".", rng)
        elif kind == "nkeys":
            right = len(keys)
            q = mkq(A_FD, head + "How many candidate keys does R have?", right, [right + 1, right + 2, max(0, right - 1), 1, 0, 3], "Candidate keys: " + fmt_keys(keys) + ".", rng)
        elif kind == "nsuper":
            right = super_key_count(R, fds)
            q = mkq(A_FD, head + "How many super keys does R have?", right, [right + 1, right * 2, right - 1, 2 ** (n - 1), 2 ** n - 1, right + 3], "Count every attribute set whose closure is all of R, i.e. all supersets of a candidate key (" + fmt_keys(keys) + ").", rng)
        elif kind == "implied":
            cands = []
            for _ in range(60):
                l = tuple(sorted(rng.sample(R, rng.choice([1, 2]))))
                r = tuple(sorted(rng.sample([x for x in R if x not in l], 1)))
                cands.append((l, r))
            good = [c for c in cands if set(c[1]) <= closure(c[0], fds) and c not in fds]
            bad = [c for c in cands if not set(c[1]) <= closure(c[0], fds)]
            if not good or len(set(bad)) < 3: continue
            right = fmt_fd(good[0])
            wr = [fmt_fd(b) for b in dict.fromkeys(bad)]
            q = mkq(A_FD, head + "Which dependency follows from F?", right, wr,
                    "Compute the closure of the left side: " + fmt_set(closure(good[0][0], fds)) + " contains " + "".join(good[0][1]) + ". The others are not in their left sides' closures.", rng)
        elif kind == "prime":
            prime = set().union(*keys)
            right = fmt_set(prime)
            wr = [fmt_set(prime | {x}) for x in R if x not in prime] + [fmt_set(prime - {x}) for x in prime if len(prime) > 1] + [fmt_set(set(R) - prime)]
            q = mkq(A_FD, head + "Which attributes are prime (part of some candidate key)? Keys: " + fmt_keys(keys) + ".", right, wr,
                    "Union of all candidate keys: " + right + ".", rng)
        if q and q["q"] not in {x["q"] for x in out}:
            out.append(q)
            seen.add(sig)
    return out


# ---------------------------------------------------------------- SQL result prediction
def fmt_result(rows, cols):
    def v(x):
        if x is None: return "NULL"
        if isinstance(x, float): return str(int(x)) if x == int(x) else ("%.1f" % x)
        return str(x)
    if not rows: return "no rows"
    if len(rows) == 1 and len(cols) == 1: return v(rows[0][0])
    if len(cols) == 1:
        s = ", ".join(v(r[0]) for r in rows[:8])
        return s + (", ..." if len(rows) > 8 else "")
    s = "; ".join("(" + ", ".join(v(c) for c in r) + ")" for r in rows[:5])
    return s + ("; ..." if len(rows) > 5 else "")


SQL_ITEMS = [
    ("How many rows does this return?", "SELECT COUNT(*) FROM employees WHERE dept_id IS NULL;",
     ["SELECT COUNT(*) FROM employees WHERE dept_id = NULL;", "SELECT COUNT(dept_id) FROM employees;", "SELECT COUNT(*) FROM employees;"],
     "IS NULL finds the one employee without a department. = NULL is never true; COUNT(dept_id) skips NULLs."),
    ("What does this return?", "SELECT COUNT(*), COUNT(dept_id), COUNT(DISTINCT dept_id) FROM employees;",
     ["SELECT COUNT(*), COUNT(city), COUNT(DISTINCT city) FROM employees;", "SELECT COUNT(*), COUNT(manager_id), COUNT(DISTINCT manager_id) FROM employees;", "SELECT COUNT(*), COUNT(id), COUNT(DISTINCT salary) FROM employees;"],
     "10 rows, 9 non-NULL dept_id values, 3 distinct departments."),
    ("What does this return?", "SELECT name FROM employees WHERE salary > (SELECT AVG(salary) FROM employees) ORDER BY salary DESC, name;",
     ["SELECT name FROM employees WHERE salary >= 98000 ORDER BY salary DESC, name;", "SELECT name FROM employees WHERE salary > (SELECT MAX(salary) FROM employees) ORDER BY name;", "SELECT name FROM employees WHERE salary > 100000 ORDER BY salary DESC, name;"],
     "The average is 95200, so Asha, Meera, Vikram and Rohan are above it."),
    ("What does this return?", "SELECT d.name, COUNT(e.id) FROM departments d LEFT JOIN employees e ON e.dept_id = d.id GROUP BY d.id, d.name ORDER BY d.id;",
     ["SELECT d.name, COUNT(*) FROM departments d LEFT JOIN employees e ON e.dept_id = d.id GROUP BY d.id, d.name ORDER BY d.id;", "SELECT d.name, COUNT(e.id) FROM departments d JOIN employees e ON e.dept_id = d.id GROUP BY d.id, d.name ORDER BY d.id;", "SELECT d.name, COUNT(e.id) FROM employees e LEFT JOIN departments d ON e.dept_id = d.id GROUP BY d.id, d.name ORDER BY d.id;"],
     "LEFT JOIN keeps Design; COUNT(e.id) counts 0 for it, while COUNT(*) would count 1."),
    ("What does this return?", "SELECT name FROM departments WHERE id NOT IN (SELECT dept_id FROM employees);",
     ["SELECT name FROM departments d WHERE NOT EXISTS (SELECT 1 FROM employees e WHERE e.dept_id = d.id);", "SELECT name FROM departments WHERE id IN (SELECT dept_id FROM employees);", "SELECT name FROM departments WHERE id NOT IN (SELECT dept_id FROM employees WHERE dept_id IS NOT NULL);"],
     "employees.dept_id contains a NULL, so NOT IN is never true: it returns no rows."),
    ("What does this return?", "SELECT name FROM departments d WHERE NOT EXISTS (SELECT 1 FROM employees e WHERE e.dept_id = d.id);",
     ["SELECT name FROM departments WHERE id IN (SELECT dept_id FROM employees);", "SELECT name FROM departments WHERE id NOT IN (SELECT dept_id FROM employees);", "SELECT name FROM departments WHERE budget > 600000;"],
     "NOT EXISTS is NULL-safe and finds the department with no employees."),
    ("What does this return?", "SELECT name, DENSE_RANK() OVER (ORDER BY salary DESC) FROM employees WHERE id IN (3, 4, 2, 7) ORDER BY id;",
     ["SELECT name, RANK() OVER (ORDER BY salary DESC) FROM employees WHERE id IN (3, 4, 2, 7) ORDER BY id;", "SELECT name, ROW_NUMBER() OVER (ORDER BY salary DESC, id) FROM employees WHERE id IN (3, 4, 2, 7) ORDER BY id;", "SELECT name, DENSE_RANK() OVER (ORDER BY salary) FROM employees WHERE id IN (3, 4, 2, 7) ORDER BY id;"],
     "Meera and Vikram tie at 120000 (rank 1), Rohan 98000 is rank 2, Kiran 92000 is rank 3 with DENSE_RANK."),
    ("What does this return?", "SELECT name, RANK() OVER (ORDER BY salary DESC) FROM employees WHERE id IN (3, 4, 2, 7) ORDER BY id;",
     ["SELECT name, DENSE_RANK() OVER (ORDER BY salary DESC) FROM employees WHERE id IN (3, 4, 2, 7) ORDER BY id;", "SELECT name, ROW_NUMBER() OVER (ORDER BY salary DESC, id) FROM employees WHERE id IN (3, 4, 2, 7) ORDER BY id;", "SELECT name, RANK() OVER (ORDER BY salary) FROM employees WHERE id IN (3, 4, 2, 7) ORDER BY id;"],
     "With RANK a tie leaves a gap: 1, 1, 3, 4."),
    ("What does this return?", "SELECT MAX(salary) FROM employees WHERE salary < (SELECT MAX(salary) FROM employees);",
     ["SELECT MAX(salary) FROM employees;", "SELECT MIN(salary) FROM employees WHERE salary > (SELECT MIN(salary) FROM employees);", "SELECT salary FROM employees ORDER BY salary DESC LIMIT 1 OFFSET 3;"],
     "The second highest distinct salary is 120000."),
    ("What does this return?", "SELECT city, COUNT(*) FROM employees GROUP BY city HAVING COUNT(*) >= 3 ORDER BY city;",
     ["SELECT city, COUNT(*) FROM employees GROUP BY city HAVING COUNT(*) >= 2 ORDER BY city;", "SELECT city, COUNT(*) FROM employees WHERE salary > 90000 GROUP BY city ORDER BY city;", "SELECT city, COUNT(*) FROM employees GROUP BY city HAVING COUNT(*) = 1 ORDER BY city;"],
     "Bengaluru has 4 and Pune has 3; Hyderabad 2 and Chennai 1 are filtered out."),
    ("What does this return?", "SELECT e.name FROM employees e JOIN employees m ON m.id = e.manager_id WHERE e.salary > m.salary ORDER BY e.name;",
     ["SELECT e.name FROM employees e JOIN employees m ON m.id = e.manager_id WHERE e.salary < m.salary ORDER BY e.name;", "SELECT e.name FROM employees e LEFT JOIN employees m ON m.id = e.manager_id WHERE m.id IS NULL ORDER BY e.name;", "SELECT e.name FROM employees e JOIN employees m ON m.id = e.manager_id WHERE e.salary = m.salary ORDER BY e.name;"],
     "Kiran and Nisha (92000) report to Arjun (88000)."),
    ("What does this return?", "SELECT name FROM employees WHERE manager_id IS NULL ORDER BY name;",
     ["SELECT name FROM employees WHERE manager_id IS NOT NULL ORDER BY name LIMIT 3;", "SELECT name FROM employees WHERE dept_id IS NULL ORDER BY name;", "SELECT name FROM employees WHERE manager_id = 1 ORDER BY name;"],
     "Asha (the top boss) and Farhan (no manager)."),
    ("What does this return?", "SELECT COUNT(*) FROM employees e CROSS JOIN departments d;",
     ["SELECT COUNT(*) FROM employees e JOIN departments d ON d.id = e.dept_id;", "SELECT COUNT(*) FROM employees e LEFT JOIN departments d ON d.id = e.dept_id;", "SELECT COUNT(*) FROM employees;"],
     "10 employees times 4 departments."),
    ("What does this return?", "SELECT COUNT(*) FROM employees e JOIN departments d ON d.id = e.dept_id;",
     ["SELECT COUNT(*) FROM employees e CROSS JOIN departments d;", "SELECT COUNT(*) FROM departments;", "SELECT COUNT(*) FROM employees e FULL JOIN departments d ON d.id = e.dept_id;"],
     "Farhan has no department and drops out of the inner join: 9 rows."),
    ("What does this return?", "SELECT dept_id, SUM(salary) FROM employees GROUP BY dept_id ORDER BY dept_id;",
     ["SELECT dept_id, AVG(salary) FROM employees GROUP BY dept_id ORDER BY dept_id;", "SELECT dept_id, SUM(salary) FROM employees WHERE dept_id IS NOT NULL GROUP BY dept_id ORDER BY dept_id;", "SELECT dept_id, MAX(salary) FROM employees GROUP BY dept_id ORDER BY dept_id;"],
     "GROUP BY puts the NULL department in its own group (NULL sorts first in SQLite)."),
    ("What does this return?", "SELECT name FROM employees WHERE name LIKE '_a%' ORDER BY name;",
     ["SELECT name FROM employees WHERE name LIKE 'a%' ORDER BY name;", "SELECT name FROM employees WHERE name LIKE '%a' ORDER BY name;", "SELECT name FROM employees WHERE name LIKE '%a%' ORDER BY name;"],
     "_ is exactly one character, so the second letter must be a. Only Farhan qualifies."),
    ("What does this return?", "SELECT salary, COUNT(*) FROM employees GROUP BY salary HAVING COUNT(*) > 1 ORDER BY salary;",
     ["SELECT salary, COUNT(*) FROM employees GROUP BY salary ORDER BY salary LIMIT 2;", "SELECT dept_id, COUNT(*) FROM employees GROUP BY dept_id HAVING COUNT(*) > 1 ORDER BY dept_id;", "SELECT salary, COUNT(*) FROM employees GROUP BY salary HAVING COUNT(*) > 2 ORDER BY salary;"],
     "Two salaries repeat: 92000 (Kiran, Nisha) and 120000 (Meera, Vikram)."),
    ("What does this return?", "SELECT name, COALESCE(dept_id, -1) FROM employees WHERE id IN (1, 9) ORDER BY id;",
     ["SELECT name, dept_id FROM employees WHERE id IN (1, 9) ORDER BY id;", "SELECT name, COALESCE(manager_id, -1) FROM employees WHERE id IN (1, 9) ORDER BY id;", "SELECT name, IFNULL(dept_id, 0) FROM employees WHERE id IN (1, 9) ORDER BY id;"],
     "COALESCE replaces NULL with -1 for Farhan."),
    ("What does this return?", "SELECT SUM(CASE WHEN city = 'Pune' THEN 1 ELSE 0 END), SUM(CASE WHEN city = 'Bengaluru' THEN 1 ELSE 0 END) FROM employees;",
     ["SELECT COUNT(*), COUNT(DISTINCT city) FROM employees;", "SELECT SUM(CASE WHEN city = 'Pune' THEN salary ELSE 0 END), 0 FROM employees;", "SELECT SUM(CASE WHEN city = 'Chennai' THEN 1 ELSE 0 END), SUM(CASE WHEN city = 'Hyderabad' THEN 1 ELSE 0 END) FROM employees;"],
     "Conditional aggregation: 3 in Pune and 4 in Bengaluru."),
    ("What does this return?", "SELECT id FROM departments EXCEPT SELECT dept_id FROM employees;",
     ["SELECT id FROM departments UNION SELECT dept_id FROM employees;", "SELECT id FROM departments INTERSECT SELECT dept_id FROM employees;", "SELECT dept_id FROM employees EXCEPT SELECT id FROM departments;"],
     "Department 4 (Design) has no employees."),
    ("What does this return?", "SELECT city FROM employees WHERE dept_id = 1 UNION SELECT city FROM employees WHERE dept_id = 3 ORDER BY city;",
     ["SELECT city FROM employees WHERE dept_id = 1 INTERSECT SELECT city FROM employees WHERE dept_id = 3 ORDER BY city;", "SELECT city FROM employees WHERE dept_id = 1 EXCEPT SELECT city FROM employees WHERE dept_id = 3 ORDER BY city;", "SELECT city FROM employees WHERE dept_id = 2 UNION SELECT city FROM employees WHERE dept_id = 3 ORDER BY city;"],
     "UNION removes duplicates: Bengaluru, Chennai, Pune."),
    ("What does this return?", "SELECT COUNT(*) FROM (SELECT city FROM employees WHERE dept_id = 1 UNION ALL SELECT city FROM employees WHERE dept_id = 3);",
     ["SELECT COUNT(*) FROM (SELECT city FROM employees WHERE dept_id = 1 UNION SELECT city FROM employees WHERE dept_id = 3);", "SELECT COUNT(*) FROM employees;", "SELECT COUNT(*) FROM (SELECT city FROM employees WHERE dept_id = 1 INTERSECT SELECT city FROM employees WHERE dept_id = 3);"],
     "UNION ALL keeps all 3 + 3 rows."),
    ("What does this return?", "SELECT name FROM employees ORDER BY salary DESC, name LIMIT 3 OFFSET 2;",
     ["SELECT name FROM employees ORDER BY salary DESC, name LIMIT 3;", "SELECT name FROM employees ORDER BY salary, name LIMIT 3 OFFSET 2;", "SELECT name FROM employees ORDER BY salary DESC, name LIMIT 2 OFFSET 3;"],
     "Skip the top two (Asha, Meera) and take the next three."),
    ("What does this return?", "SELECT name, salary - LAG(salary) OVER (ORDER BY hire_date) FROM employees WHERE id IN (3, 1, 2) ORDER BY hire_date;",
     ["SELECT name, LEAD(salary) OVER (ORDER BY hire_date) FROM employees WHERE id IN (3, 1, 2) ORDER BY hire_date;", "SELECT name, salary - LEAD(salary) OVER (ORDER BY hire_date) FROM employees WHERE id IN (3, 1, 2) ORDER BY hire_date;", "SELECT name, salary - LAG(salary) OVER (ORDER BY salary) FROM employees WHERE id IN (3, 1, 2) ORDER BY hire_date;"],
     "Hire order: Meera, Asha, Rohan. LAG looks at the previous row, and the first row has none (NULL)."),
    ("What does this return?", "SELECT SUM(salary) OVER (ORDER BY hire_date) FROM employees WHERE id IN (3, 1, 2) ORDER BY hire_date;",
     ["SELECT SUM(salary) OVER () FROM employees WHERE id IN (3, 1, 2) ORDER BY hire_date;", "SELECT salary FROM employees WHERE id IN (3, 1, 2) ORDER BY hire_date;", "SELECT SUM(salary) OVER (ORDER BY hire_date DESC) FROM employees WHERE id IN (3, 1, 2) ORDER BY hire_date;"],
     "Running total in hire order: 120000, 265000, 363000."),
    ("What does this return?", "SELECT e.name FROM employees e WHERE e.salary = (SELECT MAX(salary) FROM employees x WHERE x.dept_id = e.dept_id) ORDER BY e.name;",
     ["SELECT e.name FROM employees e WHERE e.salary = (SELECT MAX(salary) FROM employees) ORDER BY e.name;", "SELECT e.name FROM employees e WHERE e.salary = (SELECT MIN(salary) FROM employees x WHERE x.dept_id = e.dept_id) ORDER BY e.name;", "SELECT e.name FROM employees e WHERE e.salary > (SELECT AVG(salary) FROM employees x WHERE x.dept_id = e.dept_id) ORDER BY e.name;"],
     "Top earner per department including ties (Farhan has a NULL dept so the comparison with NULL never matches)."),
    ("What does this return?", "SELECT p.name, SUM(a.hours) FROM projects p JOIN assignments a ON a.project_id = p.id GROUP BY p.id, p.name ORDER BY SUM(a.hours) DESC;",
     ["SELECT p.name, COUNT(a.hours) FROM projects p JOIN assignments a ON a.project_id = p.id GROUP BY p.id, p.name ORDER BY COUNT(a.hours) DESC;", "SELECT p.name, MAX(a.hours) FROM projects p JOIN assignments a ON a.project_id = p.id GROUP BY p.id, p.name ORDER BY MAX(a.hours) DESC;", "SELECT p.name, SUM(a.hours) FROM projects p JOIN assignments a ON a.project_id = p.id GROUP BY p.id, p.name ORDER BY p.name;"],
     "Beacon 400, Cobalt 350, Atlas 180, Delta 30."),
    ("What does this return?", "SELECT name FROM employees WHERE id NOT IN (SELECT emp_id FROM assignments) ORDER BY name;",
     ["SELECT name FROM employees WHERE id IN (SELECT emp_id FROM assignments) ORDER BY name;", "SELECT name FROM employees WHERE dept_id NOT IN (SELECT dept_id FROM projects) ORDER BY name;", "SELECT name FROM employees WHERE manager_id NOT IN (SELECT emp_id FROM assignments) ORDER BY name;"],
     "assignments.emp_id has no NULLs, so NOT IN works here: Asha and Farhan have no assignment."),
    ("What does this return?", "SELECT strftime('%Y', hire_date), COUNT(*) FROM employees GROUP BY 1 ORDER BY 1 LIMIT 3;",
     ["SELECT strftime('%Y', hire_date), SUM(salary) FROM employees GROUP BY 1 ORDER BY 1 LIMIT 3;", "SELECT strftime('%m', hire_date), COUNT(*) FROM employees GROUP BY 1 ORDER BY 1 LIMIT 3;", "SELECT strftime('%Y', hire_date), COUNT(*) FROM employees GROUP BY 1 ORDER BY 1 DESC LIMIT 3;"],
     "Hires per year, earliest years first."),
    ("What does this return?", "SELECT name, salary FROM employees WHERE salary BETWEEN 88000 AND 98000 ORDER BY salary, name;",
     ["SELECT name, salary FROM employees WHERE salary > 88000 AND salary < 98000 ORDER BY salary, name;", "SELECT name, salary FROM employees WHERE salary BETWEEN 98000 AND 88000 ORDER BY salary, name;", "SELECT name, salary FROM employees WHERE salary >= 88000 ORDER BY salary, name;"],
     "BETWEEN is inclusive on both ends: Arjun 88000, Kiran and Nisha 92000, Rohan 98000."),
    ("What does this return?", "SELECT dept_id, COUNT(*) FROM employees WHERE salary > 90000 GROUP BY dept_id ORDER BY dept_id;",
     ["SELECT dept_id, COUNT(*) FROM employees GROUP BY dept_id HAVING COUNT(*) > 90000 ORDER BY dept_id;", "SELECT dept_id, COUNT(*) FROM employees GROUP BY dept_id ORDER BY dept_id;", "SELECT dept_id, COUNT(*) FROM employees WHERE salary < 90000 GROUP BY dept_id ORDER BY dept_id;"],
     "WHERE filters rows first (salary above 90000), then the survivors are grouped."),
]


def gen_sql(rng, seed_sql):
    out = []
    for stem, right_q, wrong_qs, why in SQL_ITEMS:
        con = sqlite3.connect(":memory:")
        con.executescript(seed_sql)
        def run(sql):
            cur = con.execute(sql)
            return fmt_result(cur.fetchall(), [d[0] for d in cur.description])
        right = run(right_q)
        wrongs = []
        for w in wrong_qs:
            r = run(w)
            if r != right and r not in wrongs:
                wrongs.append(r)
        for filler in ("no rows", "NULL", "an error"):
            if len(wrongs) < 3 and filler != right and filler not in wrongs:
                wrongs.append(filler)
        q = mkq(A_SQL, stem + " (sample database: employees, departments, projects, assignments, logins)\n\n" + right_q, right, wrongs, why, rng)
        con.close()
        if q:
            out.append(q)
        else:
            raise SystemExit("not enough distinct options for: " + right_q)
    return out


# ---------------------------------------------------------------- handwritten
def H(area, q, o, a, w): return {"area": area, "q": q, "o": o, "a": a, "w": w}


HAND = [
    # scenarios and design
    H(A_SCN, "A library lets a book have several authors and an author write several books. Which design is correct?",
      ["book(author_id) with a comma-separated list", "book_author(book_id, author_id) with PRIMARY KEY (book_id, author_id)", "author(book_id) with duplicate author rows", "One table with columns author1, author2, author3"], 1, "Many-to-many needs a junction table with both foreign keys as a composite key."),
    H(A_SCN, "An order must keep the price a customer actually paid even if the product price later changes. Where do you store it?",
      ["Only in product.price", "In order_item.unit_price copied at purchase time", "In a trigger log only", "In the customer table"], 1, "A deliberate snapshot of the price on the order line keeps history stable."),
    H(A_SCN, "Each employee has at most one parking spot and each spot belongs to at most one employee. Which constraint pair models it?",
      ["parking.employee_id with UNIQUE and a foreign key", "employee.parking_id without UNIQUE", "A junction table without keys", "Two primary keys in employee"], 0, "A 1:1 relationship is a foreign key with a UNIQUE constraint on it."),
    H(A_SCN, "Which CREATE TABLE has a bug?",
      ["CREATE TABLE t (id INT PRIMARY KEY, a INT NOT NULL, b INT CHECK (b > 0));", "CREATE TABLE t (id INT, id2 INT, PRIMARY KEY (id, id2));", "CREATE TABLE t (id INT PRIMARY KEY, PRIMARY KEY (id));", "CREATE TABLE t (id INT PRIMARY KEY, a INT UNIQUE);"], 2, "A table can have only one primary key declaration; here it is declared twice."),
    H(A_SCN, "You need 'a student enrolls in a course at most once per term'. Which constraint?",
      ["PRIMARY KEY (student_id)", "UNIQUE (student_id, course_id, term)", "CHECK (term > 0)", "FOREIGN KEY (term)"], 1, "The combination of the three columns must be unique."),
    H(A_SCN, "A comments table needs replies to comments (a tree). Which column does it need?",
      ["reply_count INT", "parent_id referencing comments(id), NULL for top level", "A separate table per level", "A TEXT list of child ids"], 1, "Adjacency list: a self-referencing foreign key."),
    H(A_SCN, "Which is the better primary key for a table of customers that also has a unique email?",
      ["email only", "A surrogate id plus UNIQUE (email)", "name", "No primary key"], 1, "Emails change; keep a stable surrogate key and still enforce uniqueness of the natural key."),
    H(A_SCN, "When a department is deleted its employees should stay but lose the department link. Which foreign key action?",
      ["ON DELETE CASCADE", "ON DELETE SET NULL", "ON DELETE RESTRICT", "ON UPDATE CASCADE"], 1, "SET NULL orphans the children gracefully (the FK column must allow NULL)."),
    H(A_SCN, "An invoice number must never repeat and never have gaps. What is the right approach?",
      ["An auto-increment id", "A separately controlled counter row updated in the same transaction (with locking)", "MAX(id) + 1 in application code", "A random UUID"], 1, "Auto-increment can skip values after rollbacks; gapless numbering needs a locked counter."),
    H(A_SCN, "Which design allows a doctor to be booked only once for a given start time?",
      ["UNIQUE (doctor_id, slot_start) on appointment", "CHECK (slot_start > now())", "An index on slot_start", "A trigger on SELECT"], 0, "A unique constraint over the pair prevents a second booking."),
    H(A_SCN, "A table has columns (student, course, instructor) with course determined by instructor. Which statement is true?",
      ["It is in BCNF", "It is in 3NF but not BCNF if the keys overlap", "It has a multivalued dependency only", "It violates 1NF"], 1, "instructor → course has a non-key determinant whose RHS is prime: 3NF, not BCNF."),
    H(A_SCN, "To represent a multivalued attribute such as an employee's skills you should:",
      ["Store a comma-separated string", "Create employee_skill(emp_id, skill) with a composite key", "Add skill1..skill5 columns", "Use a derived attribute"], 1, "Child table keeps 1NF and lets you query and constrain skills."),
    H(A_SCN, "Soft delete with a unique email should be implemented in PostgreSQL as:",
      ["UNIQUE (email)", "CREATE UNIQUE INDEX ... ON users (email) WHERE deleted_at IS NULL", "CHECK (deleted_at IS NULL)", "DEFAULT NULL"], 1, "A partial unique index ignores soft-deleted rows."),
    H(A_SCN, "Which is the best type for storing money amounts like 1499.99?",
      ["FLOAT", "NUMERIC(12,2)", "TEXT", "DOUBLE PRECISION"], 1, "Exact decimals avoid rounding errors."),
    H(A_SCN, "A query filters WHERE LOWER(email) = 'a@x.com' on a big table. The right fix in PostgreSQL is:",
      ["An index on email", "An expression index on LOWER(email)", "A hash join", "SELECT *"], 1, "A plain index cannot serve a function of the column."),
    # PG vs MySQL
    H(A_RDB, "Which statement inserts or updates on a duplicate key in PostgreSQL?",
      ["INSERT ... ON DUPLICATE KEY UPDATE", "INSERT ... ON CONFLICT (key) DO UPDATE", "REPLACE INTO", "UPSERT"], 1, "ON DUPLICATE KEY UPDATE is the MySQL spelling."),
    H(A_RDB, "In MySQL the expression 'a' || 'b' returns (default sql_mode):", ["'ab'", "0 (logical OR of two strings)", "An error", "NULL"], 1, "|| is logical OR in MySQL unless PIPES_AS_CONCAT is on."),
    H(A_RDB, "SELECT 7 / 2 returns 3 in:", ["MySQL", "PostgreSQL", "Both", "Neither"], 1, "PostgreSQL performs integer division for two integers; MySQL returns 3.5."),
    H(A_RDB, "Which is a PostgreSQL-only feature?", ["Primary keys", "Transactional DDL", "Foreign keys", "Views"], 1, "MySQL implicitly commits on DDL."),
    H(A_RDB, "MySQL equivalent of PostgreSQL STRING_AGG(name, ', '):", ["LISTAGG", "GROUP_CONCAT(name SEPARATOR ', ')", "CONCAT_AGG", "ARRAY_TO_STRING"], 1, "GROUP_CONCAT with SEPARATOR."),
    H(A_RDB, "You need the first row per group in PostgreSQL in one clause. Use:", ["TOP 1 WITH TIES", "DISTINCT ON (group_col)", "LIMIT PER GROUP", "GROUP FIRST"], 1, "DISTINCT ON keeps the first row per key according to ORDER BY."),
    H(A_RDB, "The InnoDB storage layout is best described as:", ["Heap plus separate primary-key index", "Clustered B+ tree on the primary key", "Hash table", "Column store"], 1, "The table is stored inside the primary key index."),
    H(A_RDB, "Which command shows the structure of a table in MySQL and in psql respectively?", ["DESCRIBE t / \\d t", "\\d t / DESCRIBE t", "SHOW t / LIST t", "INFO t / \\i t"], 0, "MySQL DESCRIBE, psql \\d."),
    H(A_RDB, "Which of these syntaxes is MySQL (not PostgreSQL) for a join-update?", ["UPDATE a SET x = b.x FROM b WHERE a.id = b.id", "UPDATE a JOIN b ON a.id = b.id SET a.x = b.x", "MERGE INTO a USING b", "UPDATE a, b WITH"], 1, "PostgreSQL uses UPDATE ... FROM; MySQL uses UPDATE ... JOIN ... SET."),
    H(A_RDB, "Default isolation level: PostgreSQL / MySQL InnoDB:", ["READ COMMITTED / REPEATABLE READ", "REPEATABLE READ / READ COMMITTED", "SERIALIZABLE / SERIALIZABLE", "READ UNCOMMITTED / READ COMMITTED"], 0, "That difference is frequently asked."),
    H(A_RDB, "A MySQL column declared TIMESTAMP differs from DATETIME because it:", ["Has no time part", "Is stored in UTC and limited to 1970-2038", "Stores only dates", "Cannot be indexed"], 1, "TIMESTAMP is converted to the session time zone and has a limited range."),
    H(A_RDB, "In which database does a partial index exist natively?", ["MySQL", "PostgreSQL", "Both", "Neither"], 1, "CREATE INDEX ... WHERE condition is PostgreSQL."),
    # transactions and triggers
    H(A_TRX, "A BEFORE INSERT trigger is the right place to:", ["Write an audit row for a successful insert", "Validate or fix the incoming row", "Update other tables after commit", "Replace a view"], 1, "BEFORE triggers can modify NEW or reject the row."),
    H(A_TRX, "In a PostgreSQL BEFORE row trigger, RETURN NULL means:", ["Allow the row", "Skip the operation for this row", "Roll back the transaction", "Error"], 1, "The row-level operation is silently cancelled."),
    H(A_TRX, "Which trigger event has no NEW row?", ["INSERT", "UPDATE", "DELETE", "None"], 2, "DELETE only has OLD."),
    H(A_TRX, "Two transactions each read balance 100 and write 110. Final balance is 110. This is:", ["Dirty read", "Lost update", "Phantom read", "Deadlock"], 1, "One write overwrote the other."),
    H(A_TRX, "SELECT ... FOR UPDATE SKIP LOCKED is typically used for:", ["Backups", "Job queues with several workers", "Reporting", "Creating indexes"], 1, "Each worker claims a different unlocked row."),
    H(A_TRX, "A transaction in PostgreSQL gets an error. What happens to later statements in the same transaction block?", ["They run normally", "They all fail until ROLLBACK", "They auto-commit", "The connection closes"], 1, "The transaction is aborted."),
    H(A_TRX, "To avoid deadlocks between two transfer transactions you should:", ["Increase isolation to READ UNCOMMITTED", "Always lock accounts in the same order", "Use autocommit", "Disable indexes"], 1, "Consistent lock ordering removes the cycle."),
    H(A_TRX, "MySQL InnoDB cascading foreign-key actions:", ["Fire triggers", "Do not fire triggers", "Are not supported", "Run in a separate transaction"], 1, "Triggers are not activated by foreign key cascades in MySQL."),
    H(A_TRX, "Schedule R1(A) W2(A) W1(A) is checked by a precedence graph. The edges are:", ["T1 → T2 only", "T2 → T1 only", "T1 → T2 and T2 → T1 (cycle)", "No edges"], 2, "R1 before W2 gives T1→T2; W2 before W1 gives T2→T1."),
    H(A_TRX, "Which isolation level prevents phantom reads according to the SQL standard?", ["READ COMMITTED", "REPEATABLE READ", "SERIALIZABLE", "READ UNCOMMITTED"], 2, "Only SERIALIZABLE forbids all three anomalies."),
    H(A_TRX, "A trigger that UPDATEs its own table inside a BEFORE UPDATE trigger is risky because:", ["It is syntactically invalid", "It can recurse indefinitely", "It cannot see NEW", "It locks the database"], 1, "Modify NEW instead, or guard against recursion."),
    H(A_TRX, "Write-ahead logging requires that log records:", ["Reach disk before the data pages they describe", "Are written after commit only", "Are kept in memory", "Replace the data"], 0, "Log first, data later."),
]


def build(seed_sql):
    rng = random.Random(1234)
    qs = gen_fd(rng) + gen_sql(rng, seed_sql)
    for h in HAND:
        right = h["o"][h["a"]]
        opts = list(h["o"])
        rng.shuffle(opts)
        qs.append({"area": h["area"], "q": h["q"], "o": opts, "a": opts.index(right), "w": h["w"]})
    return qs


if __name__ == "__main__":
    html = open("sqllab_base.html", encoding="utf8").read()
    seed = json.loads(html.split('<script type="application/json" id="seed">')[1].split("</script>")[0])["sql"]
    b = build(seed)
    import collections
    print(len(b), collections.Counter(q["area"] for q in b))
