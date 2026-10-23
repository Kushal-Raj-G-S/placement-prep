"""Study guide, part 3b: writing queries (SELECT, NULL, functions, aggregates, joins, subqueries, sets, CTE, windows, DML, views, indexes)."""
from mat_common import *

GE = "E. Writing queries"
SAMPLE = "Sample tables used by the runnable examples: employees(id, name, dept_id, manager_id, salary, hire_date, city), departments(id, name, budget), projects(id, name, dept_id, budget), assignments(emp_id, project_id, hours), logins(emp_id, login_date). Press run to execute on the live copy."


def build():
    T = []

    # ------------------------------------------------------------------ select basics
    T.append(topic("select-basics", GE, "SELECT, WHERE, ORDER BY, LIMIT, DISTINCT",
        "Everything a basic query can do, plus the order in which the database actually evaluates it. " + SAMPLE,
        [
            H("Skeleton and logical execution order"),
            SQL("""SELECT [DISTINCT] columns / expressions
FROM table [joins]
WHERE row filter
GROUP BY grouping columns
HAVING group filter
ORDER BY sort columns
LIMIT n OFFSET m;""", "written order"),
            TXT("""Executed in this order:
FROM / JOIN  ->  WHERE  ->  GROUP BY  ->  HAVING  ->  window functions  ->  SELECT (aliases born here)
  ->  DISTINCT  ->  ORDER BY  ->  LIMIT / OFFSET"""),
            TRAP("Because SELECT runs after WHERE, you cannot use a SELECT alias inside WHERE (PostgreSQL, standard). You CAN use it in ORDER BY. MySQL lets you use aliases in GROUP BY and HAVING as an extension."),
            H("WHERE operators"),
            TBL(["Operator", "Example", "Notes"],
                ["= <> != < > <= >=", "salary >= 90000", "<> is standard; != works in both"],
                ["AND OR NOT", "city = 'Pune' AND salary > 50000", "AND binds tighter than OR; use parentheses"],
                ["BETWEEN a AND b", "salary BETWEEN 76000 AND 98000", "Inclusive on both ends"],
                ["IN (list)", "city IN ('Pune','Chennai')", "Same as OR chain"],
                ["LIKE", "name LIKE 'A%'", "% any length, _ exactly one character"],
                ["ILIKE (PostgreSQL)", "name ILIKE 'a%'", "Case-insensitive LIKE. MySQL LIKE is already case-insensitive by default collation"],
                ["Regex", "PG: name ~ '^[AB]'   MySQL: name REGEXP '^[AB]'", "~* for case-insensitive in PostgreSQL"],
                ["IS NULL / IS NOT NULL", "manager_id IS NULL", "Never = NULL"],
                ["EXISTS / ANY / ALL", "see the subqueries topic", ""]),
            SQL("""SELECT name, salary, city
FROM employees
WHERE city IN ('Pune', 'Chennai') AND salary BETWEEN 60000 AND 100000 AND name LIKE '%a'
ORDER BY salary DESC, name;""", run=True),
            H("ORDER BY, LIMIT, OFFSET, NULL ordering"),
            SQL("""SELECT name, salary FROM employees ORDER BY salary DESC, name ASC LIMIT 3;          -- top 3
SELECT name, salary FROM employees ORDER BY salary DESC LIMIT 3 OFFSET 3;                 -- rows 4-6 (pagination)""", "PostgreSQL / MySQL / SQLite", run=True),
            TBL(["Task", "PostgreSQL", "MySQL", "SQL Server / Oracle"],
                ["First n rows", "LIMIT n  or  FETCH FIRST n ROWS ONLY", "LIMIT n", "TOP n  /  FETCH FIRST n ROWS ONLY"],
                ["Skip m rows", "OFFSET m", "LIMIT n OFFSET m  or  LIMIT m, n", "OFFSET m ROWS"],
                ["NULL position", "ORDER BY x NULLS FIRST/LAST (NULLs sort as largest, last in ASC)", "NULLs sort as smallest, first in ASC", ""]),
            P("**Ties:** ORDER BY salary LIMIT 3 breaks ties arbitrarily. Add a tiebreaker column (id) for deterministic paging. **WITH TIES** (PostgreSQL 13+: FETCH FIRST 3 ROWS WITH TIES) returns all rows that tie with the last one."),
            H("DISTINCT"),
            UL("DISTINCT applies to the whole row of selected columns, not just the first column.",
               "SELECT DISTINCT dept_id, city returns unique pairs.",
               "**PostgreSQL only:** DISTINCT ON (dept_id) returns the first row per group according to ORDER BY. Handy for 'latest row per group'."),
            SQL("SELECT DISTINCT city FROM employees ORDER BY city;", run=True),
            PGSQL("SELECT DISTINCT ON (dept_id) dept_id, name, salary FROM employees ORDER BY dept_id, salary DESC;   -- top earner per department"),
            H("Expressions, aliases, literals"),
            SQL("""SELECT name,
       salary * 12        AS annual,
       salary / 1000.0    AS in_thousands,
       'Dr. ' || name     AS title,       -- || concatenation (PostgreSQL, SQLite); MySQL uses CONCAT()
       1 + 2              AS three
FROM employees LIMIT 3;""", run=True),
            MY("In MySQL || is logical OR by default; use CONCAT(). Double quotes are string delimiters in MySQL but identifiers in PostgreSQL. Always single-quote strings."),
            ASK("\"Order of execution of a SQL query?\" FROM, WHERE, GROUP BY, HAVING, SELECT, DISTINCT, ORDER BY, LIMIT. This explains why aliases fail in WHERE and why HAVING can use aggregates."),
        ],
        [
            Q("Which clause executes first?", ["SELECT", "WHERE", "FROM", "ORDER BY"], 2, "FROM (and joins) builds the row set before anything is filtered."),
            Q("BETWEEN 76000 AND 98000 includes:", ["Neither end", "Only the lower end", "Both ends", "Only the upper end"], 2, "BETWEEN is inclusive."),
            Q("SELECT name FROM employees WHERE name LIKE '_a%' matches:", ["Names starting with a", "Names whose second letter is a", "Names ending in a", "Names containing a anywhere"], 1, "_ is exactly one character, so the 'a' is in position 2."),
            Q("Why can't you reference a SELECT alias in WHERE in PostgreSQL?", ["Aliases are reserved", "WHERE is evaluated before SELECT", "Aliases can only be numbers", "It is allowed"], 1, "WHERE runs before the SELECT list is computed."),
            Q("Which returns the first row per dept_id (by the ORDER BY) in PostgreSQL?", ["SELECT TOP 1", "DISTINCT ON (dept_id)", "GROUP BY *", "LIMIT PER dept_id"], 1, "DISTINCT ON is a PostgreSQL extension."),
            Q("Pagination page 3 with 10 rows per page uses:", ["LIMIT 10 OFFSET 20", "LIMIT 20 OFFSET 10", "LIMIT 30", "OFFSET 3"], 0, "Skip (page-1) × size rows."),
        ], star=True, kw="select where order by limit offset distinct like between in execution order alias top fetch"))

    # ------------------------------------------------------------------ null/case
    T.append(topic("null-case", GE, "NULL, three-valued logic, COALESCE, NULLIF, CASE",
        "NULL means unknown, not zero and not empty string. It is behind a large share of interview traps.",
        [
            H("Three-valued logic"),
            TBL(["Expression", "Result"],
                ["NULL = NULL", "NULL (unknown), not TRUE"],
                ["NULL <> 5", "NULL"],
                ["x IS NULL", "TRUE or FALSE, never unknown"],
                ["TRUE AND NULL", "NULL"],
                ["FALSE AND NULL", "FALSE"],
                ["TRUE OR NULL", "TRUE"],
                ["FALSE OR NULL", "NULL"],
                ["NOT NULL", "NULL"],
                ["NULL + 5, NULL || 'x'", "NULL"]),
            P("WHERE keeps a row only when the condition is TRUE. FALSE and NULL both drop the row."),
            H("Where NULL bites"),
            UL("**Comparison:** WHERE manager_id = NULL returns nothing. Use IS NULL.",
               "**NOT IN with a NULL in the list returns no rows** at all. Use NOT EXISTS or filter NULLs.",
               "**Aggregates skip NULL:** COUNT(col) counts non-NULLs, COUNT(*) counts rows, AVG ignores NULLs (so it is not sum/rows).",
               "**GROUP BY** treats all NULLs as one group. **DISTINCT** and **UNION** treat NULLs as equal.",
               "**UNIQUE** columns can hold many NULLs (PostgreSQL, MySQL) because NULLs are not equal.",
               "**ORDER BY:** PostgreSQL sorts NULL last in ASC; MySQL first."),
            SQL("""SELECT COUNT(*) AS all_rows, COUNT(dept_id) AS non_null, COUNT(DISTINCT dept_id) AS distinct_depts, AVG(dept_id) AS avg_dept FROM employees;""", "10 rows, 9 non-null", run=True),
            SQL("""-- the NOT IN trap: employees.dept_id contains a NULL (Farhan)
SELECT name FROM departments WHERE id NOT IN (SELECT dept_id FROM employees);      -- returns NOTHING""", "wrong answer, silently", run=True),
            SQL("""SELECT name FROM departments d WHERE NOT EXISTS (SELECT 1 FROM employees e WHERE e.dept_id = d.id);   -- Design""", "correct", run=True),
            H("Handling NULL"),
            TBL(["Function", "Meaning", "Example"],
                ["COALESCE(a, b, c)", "First non-NULL argument (standard, all DBs)", "COALESCE(manager_id, 0)"],
                ["NULLIF(a, b)", "NULL if a = b, else a. Prevents divide by zero", "total / NULLIF(count, 0)"],
                ["IFNULL(a, b) / NVL(a, b)", "MySQL / Oracle two-argument COALESCE", ""],
                ["IS DISTINCT FROM (PostgreSQL)", "NULL-safe not equal: NULL IS DISTINCT FROM NULL is FALSE", "a IS DISTINCT FROM b"],
                ["<=> (MySQL)", "NULL-safe equality", "a <=> b"]),
            SQL("""SELECT name, COALESCE(dept_id, -1) AS dept, COALESCE(manager_id, id) AS boss FROM employees WHERE id IN (1, 9, 2);""", run=True),
            H("CASE expressions"),
            SQL("""-- searched CASE
SELECT name, salary,
  CASE WHEN salary >= 120000 THEN 'senior'
       WHEN salary >= 90000  THEN 'mid'
       ELSE 'junior' END AS band
FROM employees ORDER BY salary DESC;

-- simple CASE
SELECT name, CASE city WHEN 'Pune' THEN 'PN' WHEN 'Bengaluru' THEN 'BLR' ELSE 'OTHER' END AS code FROM employees;""", run=True),
            P("**Conditional aggregation** (pivot without PIVOT):"),
            SQL("""SELECT SUM(CASE WHEN city = 'Pune' THEN 1 ELSE 0 END)      AS pune,
       SUM(CASE WHEN city = 'Bengaluru' THEN 1 ELSE 0 END) AS bengaluru,
       COUNT(*) AS total
FROM employees;""", run=True),
            PGSQL("SELECT COUNT(*) FILTER (WHERE city = 'Pune') AS pune FROM employees;   -- PostgreSQL shorthand"),
            TRAP("CASE returns the FIRST matching branch only. An ELSE-less CASE yields NULL. All branches must produce compatible types."),
            ASK("\"What is the difference between COUNT(*), COUNT(col) and COUNT(DISTINCT col)?\" Rows, non-NULL values, distinct non-NULL values."),
        ],
        [
            Q("SELECT * FROM t WHERE x = NULL returns:", ["Rows where x is null", "No rows", "All rows", "An error"], 1, "x = NULL is unknown for every row; use IS NULL."),
            Q("t has values 1, 2, NULL in column x. COUNT(x) is:", ["3", "2", "1", "0"], 1, "COUNT(col) ignores NULLs."),
            Q("WHERE id NOT IN (SELECT col FROM s) returns no rows if s.col contains:", ["Duplicates", "A NULL", "Zero", "Text"], 1, "id <> NULL is unknown, so no row can pass."),
            Q("Which prevents division by zero?", ["COALESCE(x, 1)", "x / NULLIF(y, 0)", "x / ISNULL", "x % y"], 1, "NULLIF(y, 0) turns 0 into NULL, so the result is NULL instead of an error."),
            Q("AVG over values 10, 20, NULL gives:", ["10", "15", "30", "NULL"], 1, "NULL is ignored: (10+20)/2."),
            Q("FALSE AND NULL evaluates to:", ["NULL", "TRUE", "FALSE", "Error"], 2, "FALSE AND anything is FALSE."),
        ], star=True, kw="null three-valued logic coalesce nullif case when not in is null distinct from conditional aggregation"))

    # ------------------------------------------------------------------ functions
    T.append(topic("functions", GE, "Built-in functions: string, numeric, date and time",
        "Functions differ most between engines. Know the PostgreSQL form first, and its MySQL twin.",
        [
            H("String functions"),
            TBL(["Task", "PostgreSQL", "MySQL"],
                ["Concatenate", "a || b, CONCAT(a, b), CONCAT_WS(',', a, b)", "CONCAT(a, b), CONCAT_WS(',', a, b)"],
                ["Length", "LENGTH(s), CHAR_LENGTH(s)", "CHAR_LENGTH(s), LENGTH(s) = bytes"],
                ["Upper / lower", "UPPER(s), LOWER(s), INITCAP(s)", "UPPER(s), LOWER(s)"],
                ["Substring", "SUBSTRING(s FROM 2 FOR 3), SUBSTR(s, 2, 3), LEFT(s, n), RIGHT(s, n)", "SUBSTRING(s, 2, 3), LEFT, RIGHT"],
                ["Position", "POSITION('x' IN s), STRPOS(s, 'x')", "LOCATE('x', s), INSTR(s, 'x')"],
                ["Replace", "REPLACE(s, 'a', 'b'), TRANSLATE(s, 'abc', 'xyz')", "REPLACE(s, 'a', 'b')"],
                ["Trim", "TRIM(s), LTRIM, RTRIM, TRIM(BOTH 'x' FROM s)", "TRIM, LTRIM, RTRIM"],
                ["Pad", "LPAD(s, 5, '0'), RPAD", "LPAD, RPAD"],
                ["Reverse / repeat", "REVERSE(s), REPEAT(s, n)", "REVERSE(s), REPEAT(s, n)"],
                ["Split", "SPLIT_PART(s, ',', 2), STRING_TO_ARRAY(s, ',')", "SUBSTRING_INDEX(s, ',', 2)"],
                ["Regex replace", "REGEXP_REPLACE(s, pattern, repl)", "REGEXP_REPLACE(s, pattern, repl) (8.0+)"]),
            SQL("""SELECT name, UPPER(name) AS up, LENGTH(name) AS len, SUBSTR(name, 1, 3) AS first3,
       REPLACE(name, 'a', '@') AS swapped, name || ' (' || city || ')' AS label
FROM employees LIMIT 4;""", run=True),
            H("Numeric functions"),
            TBL(["Function", "Meaning"],
                ["ROUND(x, n), CEIL(x), FLOOR(x), TRUNC(x) / TRUNCATE(x, n)", "Rounding; PostgreSQL TRUNC, MySQL TRUNCATE"],
                ["ABS(x), SIGN(x), POWER(x, y), SQRT(x), MOD(x, y) or x % y", "Basic maths"],
                ["RANDOM() (PostgreSQL), RAND() (MySQL)", "Random number in [0,1)"],
                ["x / y with integers", "Integer division in PostgreSQL (5 / 2 = 2); MySQL / gives decimal (5 / 2 = 2.5) and DIV gives integer. Cast to numeric to be safe"],
                ["GREATEST(a, b, ...), LEAST(a, b, ...)", "Max/min across columns (row-wise)"]),
            SQL("SELECT ROUND(95200.456, 1) AS r, ABS(-7) AS a, 7 % 3 AS m, 7 / 2 AS int_div, 7 / 2.0 AS dec_div, MAX(1, 5, 3) AS pick;", "SQLite spelling of row-wise max is MAX(a,b,c)", run=True),
            H("Date and time"),
            TBL(["Task", "PostgreSQL", "MySQL"],
                ["Now", "now(), CURRENT_TIMESTAMP, CURRENT_DATE", "NOW(), CURRENT_DATE, CURDATE()"],
                ["Add days / months", "date + 7;  date + INTERVAL '1 month'", "DATE_ADD(d, INTERVAL 7 DAY), d + INTERVAL 1 MONTH"],
                ["Difference in days", "d2 - d1 (integer for DATE)", "DATEDIFF(d2, d1)"],
                ["Age / interval", "AGE(d2, d1) returns an interval", "TIMESTAMPDIFF(YEAR, d1, d2)"],
                ["Extract part", "EXTRACT(YEAR FROM d), DATE_PART('month', d)", "YEAR(d), MONTH(d), EXTRACT(YEAR FROM d)"],
                ["Truncate to period", "DATE_TRUNC('month', ts)", "DATE_FORMAT(d, '%Y-%m-01')"],
                ["Format as text", "TO_CHAR(d, 'YYYY-MM-DD')", "DATE_FORMAT(d, '%Y-%m-%d')"],
                ["Parse text", "TO_DATE('2026-10-23', 'YYYY-MM-DD')", "STR_TO_DATE('23-10-2026', '%d-%m-%Y')"],
                ["Day of week", "EXTRACT(DOW FROM d) (0 = Sunday)", "DAYOFWEEK(d) (1 = Sunday), WEEKDAY(d) (0 = Monday)"]),
            SQL("""SELECT name, hire_date,
       strftime('%Y', hire_date)                         AS hire_year,
       CAST(julianday('2026-10-23') - julianday(hire_date) AS INTEGER) AS days_employed,
       date(hire_date, '+1 year')                        AS first_anniversary
FROM employees ORDER BY hire_date LIMIT 4;""", "SQLite date functions, for the live demo", run=True),
            PGSQL("""SELECT name,
       EXTRACT(YEAR FROM hire_date)            AS yr,
       AGE(CURRENT_DATE, hire_date)            AS tenure,
       DATE_TRUNC('month', hire_date)::date    AS month_start,
       hire_date + INTERVAL '1 year'           AS anniversary
FROM employees;"""),
            MYSQL("""SELECT name,
       YEAR(hire_date)                             AS yr,
       TIMESTAMPDIFF(YEAR, hire_date, CURDATE())   AS years_employed,
       DATE_FORMAT(hire_date, '%b %Y')             AS pretty,
       DATE_ADD(hire_date, INTERVAL 1 YEAR)        AS anniversary
FROM employees;"""),
            H("Casting and misc"),
            TBL(["Task", "Syntax"],
                ["Cast", "CAST(x AS INTEGER) everywhere; PostgreSQL also x::integer; MySQL CONVERT(x, SIGNED)"],
                ["String to number safely", "PostgreSQL has no TRY_CAST (use a regex check or a function); MySQL converts leniently"],
                ["Current user / database", "CURRENT_USER, current_database()  |  USER(), DATABASE()"],
                ["Conditional", "CASE, COALESCE, NULLIF, GREATEST, LEAST"]),
            ASK("\"Get the number of days between two dates / the first day of the month.\" PostgreSQL: d2 - d1 and DATE_TRUNC('month', d). MySQL: DATEDIFF(d2, d1) and DATE_FORMAT(d, '%Y-%m-01')."),
        ],
        [
            Q("In PostgreSQL, 7 / 2 returns:", ["3.5", "3", "4", "Error"], 1, "Integer division when both operands are integers. MySQL would give 3.5."),
            Q("Which string concatenation form fails to concatenate in default MySQL?", ["CONCAT(a, b)", "a || b", "CONCAT_WS(',', a, b)", "All work"], 1, "|| is logical OR in MySQL unless PIPES_AS_CONCAT is set."),
            Q("First day of the month in PostgreSQL:", ["DATE_FORMAT(d, '%Y-%m-01')", "DATE_TRUNC('month', d)", "MONTH_START(d)", "TRUNC(d)"], 1, "DATE_TRUNC rounds down to the given unit."),
            Q("Number of days between two DATE values in MySQL:", ["d2 - d1", "DATEDIFF(d2, d1)", "AGE(d2, d1)", "DAYS(d1, d2)"], 1, "DATEDIFF returns d2 minus d1 in days."),
            Q("COALESCE(NULL, NULL, 5, 7) returns:", ["NULL", "5", "7", "12"], 1, "First non-NULL argument."),
        ], kw="functions string date time concat substring extract interval datediff date_trunc to_char round cast"))

    # ------------------------------------------------------------------ aggregates
    T.append(topic("aggregates", GE, "Aggregates, GROUP BY, HAVING, ROLLUP",
        "Collapse many rows into summaries. The rules about what may appear in SELECT are asked constantly.",
        [
            H("Aggregate functions"),
            TBL(["Function", "Counts / returns", "NULLs"],
                ["COUNT(*)", "Number of rows", "Includes NULL rows"],
                ["COUNT(col)", "Non-NULL values in col", "Skips"],
                ["COUNT(DISTINCT col)", "Distinct non-NULL values", "Skips"],
                ["SUM, AVG, MIN, MAX", "Obvious", "Skip NULLs; SUM of nothing is NULL"],
                ["STRING_AGG(col, ', ') PG  /  GROUP_CONCAT(col SEPARATOR ', ') MySQL", "Concatenated text", "Skips"],
                ["ARRAY_AGG(col) (PG), JSON_AGG / JSON_ARRAYAGG", "Collect into a list", ""],
                ["BOOL_AND / BOOL_OR (PG), BIT_AND / BIT_OR", "Logical aggregates", ""],
                ["PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY x) (PG)", "Median", ""]),
            H("GROUP BY"),
            SQL("""SELECT dept_id, COUNT(*) AS headcount, SUM(salary) AS payroll, ROUND(AVG(salary)) AS avg_salary, MAX(salary) AS top
FROM employees
GROUP BY dept_id
ORDER BY dept_id;""", "per department", run=True),
            UL("**Rule:** every column in SELECT must either be in GROUP BY or inside an aggregate function.",
               "MySQL with ONLY_FULL_GROUP_BY off (old default) lets you select non-grouped columns and returns an arbitrary row's value: dangerous. Modern MySQL enables ONLY_FULL_GROUP_BY.",
               "PostgreSQL allows selecting other columns of a table if you group by its primary key (functional dependency).",
               "GROUP BY can use column positions (GROUP BY 1) or expressions (GROUP BY EXTRACT(YEAR FROM hire_date))."),
            H("WHERE vs HAVING"),
            TBL(["", "WHERE", "HAVING"],
                ["Filters", "Individual rows before grouping", "Groups after aggregation"],
                ["Can use aggregates", "No", "Yes"],
                ["Can use an index", "Yes", "Usually no (works on grouped data)"]),
            SQL("""SELECT dept_id, COUNT(*) AS n
FROM employees
WHERE city <> 'Chennai'          -- row filter first
GROUP BY dept_id
HAVING COUNT(*) >= 3;            -- group filter""", run=True),
            P("Rule: filter rows as early as possible with WHERE, and use HAVING only for conditions on aggregates."),
            H("Multiple columns and conditional aggregation"),
            SQL("""SELECT city, COUNT(*) AS n,
       SUM(CASE WHEN salary >= 100000 THEN 1 ELSE 0 END) AS high_earners
FROM employees GROUP BY city ORDER BY n DESC, city;""", run=True),
            H("ROLLUP, CUBE, GROUPING SETS (subtotals)"),
            PGSQL("""SELECT dept_id, city, SUM(salary)
FROM employees
GROUP BY ROLLUP (dept_id, city);        -- detail rows, subtotal per dept, grand total

SELECT dept_id, city, SUM(salary) FROM employees GROUP BY CUBE (dept_id, city);               -- all combinations
SELECT dept_id, city, SUM(salary) FROM employees GROUP BY GROUPING SETS ((dept_id), (city), ());   -- chosen sets
SELECT dept_id, GROUPING(dept_id) AS is_total_row FROM employees GROUP BY ROLLUP (dept_id);"""),
            MYSQL("SELECT dept_id, city, SUM(salary) FROM employees GROUP BY dept_id, city WITH ROLLUP;   -- MySQL syntax; no CUBE or GROUPING SETS"),
            H("String aggregation"),
            PGSQL("SELECT dept_id, STRING_AGG(name, ', ' ORDER BY name) AS people FROM employees GROUP BY dept_id;"),
            MYSQL("SELECT dept_id, GROUP_CONCAT(name ORDER BY name SEPARATOR ', ') AS people FROM employees GROUP BY dept_id;"),
            SQL("SELECT dept_id, GROUP_CONCAT(name, ', ') AS people FROM employees GROUP BY dept_id;", "SQLite spelling", run=True),
            H("DISTINCT inside aggregates and aggregate of aggregates"),
            SQL("""SELECT COUNT(DISTINCT city) AS cities, COUNT(DISTINCT dept_id) AS depts FROM employees;
-- average of per-department averages (aggregate of an aggregate needs a subquery)
SELECT ROUND(AVG(avg_sal)) FROM (SELECT AVG(salary) AS avg_sal FROM employees GROUP BY dept_id);""", run=True),
            TRAP("SELECT dept_id, name, COUNT(*) FROM employees GROUP BY dept_id is invalid (name is neither grouped nor aggregated) in PostgreSQL and in MySQL with ONLY_FULL_GROUP_BY."),
            ASK("\"Difference between WHERE and HAVING?\" WHERE filters rows before grouping and cannot use aggregates. HAVING filters groups after grouping and can."),
        ],
        [
            Q("Which is valid in HAVING but not in WHERE?", ["salary > 50000", "COUNT(*) > 2", "city = 'Pune'", "name LIKE 'A%'"], 1, "Aggregates exist only after grouping."),
            Q("SELECT dept_id, name, COUNT(*) FROM employees GROUP BY dept_id fails because:", ["COUNT(*) needs DISTINCT", "name is not grouped or aggregated", "dept_id may be NULL", "GROUP BY requires ORDER BY"], 1, "Every non-aggregated select column must be in GROUP BY."),
            Q("COUNT(*) vs COUNT(dept_id) differ when dept_id:", ["Has duplicates", "Contains NULLs", "Is a key", "Is text"], 1, "COUNT(col) skips NULLs; COUNT(*) does not."),
            Q("GROUP BY ROLLUP (a, b) produces:", ["Only (a, b)", "(a, b), (a), and grand total", "All subsets of {a, b}", "Only the grand total"], 1, "A hierarchy of subtotals; CUBE gives all subsets."),
            Q("MySQL equivalent of PostgreSQL STRING_AGG:", ["CONCAT_AGG", "GROUP_CONCAT", "LISTAGG", "ARRAY_AGG"], 1, "GROUP_CONCAT(col SEPARATOR ', ')."),
        ], star=True, kw="aggregate group by having count sum avg rollup cube grouping sets string_agg group_concat where vs having"))

    # ------------------------------------------------------------------ joins
    T.append(topic("joins", GE, "Joins: inner, outer, cross, self, semi, anti",
        "The most tested SQL topic. Know each join's definition, its result on unmatched rows, and the traps with WHERE and COUNT.",
        [
            H("The join family"),
            TBL(["Join", "Returns", "Unmatched rows"],
                ["INNER JOIN (JOIN)", "Only pairs satisfying ON", "Dropped from both sides"],
                ["LEFT (OUTER) JOIN", "All rows of the left table + matches", "Right columns are NULL"],
                ["RIGHT (OUTER) JOIN", "All rows of the right table + matches", "Left columns are NULL"],
                ["FULL (OUTER) JOIN", "All rows of both", "NULLs on whichever side is missing. MySQL has none (UNION a LEFT and RIGHT)"],
                ["CROSS JOIN", "Every combination (m × n rows)", "n/a (no condition)"],
                ["NATURAL JOIN", "Inner join on all same-named columns", "Fragile: breaks when columns are added. Avoid in real code"],
                ["SELF JOIN", "A table joined to itself via aliases", "Used for hierarchies and pair comparisons"]),
            SQL("""-- INNER: employees with their department
SELECT e.name, d.name AS dept FROM employees e JOIN departments d ON d.id = e.dept_id ORDER BY e.id;""", "Farhan (no dept) disappears", run=True),
            SQL("""-- LEFT: keep every employee
SELECT e.name, d.name AS dept FROM employees e LEFT JOIN departments d ON d.id = e.dept_id ORDER BY e.id;""", "Farhan appears with NULL", run=True),
            SQL("""-- every department including the empty one, with headcount
SELECT d.name, COUNT(e.id) AS headcount FROM departments d LEFT JOIN employees e ON e.dept_id = d.id GROUP BY d.id, d.name;""", "COUNT(e.id), not COUNT(*): Design must show 0", run=True),
            SQL("""-- FULL join emulation (works everywhere, including MySQL)
SELECT e.name, d.name FROM employees e LEFT JOIN departments d ON d.id = e.dept_id
UNION
SELECT e.name, d.name FROM departments d LEFT JOIN employees e ON e.dept_id = d.id;""", "both unmatched sides", run=True),
            PGSQL("SELECT e.name, d.name FROM employees e FULL OUTER JOIN departments d ON d.id = e.dept_id;"),
            H("Self join"),
            SQL("""-- employee with manager name
SELECT e.name AS employee, m.name AS manager FROM employees e LEFT JOIN employees m ON m.id = e.manager_id ORDER BY e.id;""", run=True),
            SQL("""-- employees earning more than their manager
SELECT e.name, e.salary, m.name AS manager, m.salary AS mgr_salary FROM employees e JOIN employees m ON m.id = e.manager_id WHERE e.salary > m.salary;""", "Kiran and Nisha", run=True),
            SQL("""-- all unordered pairs in the same city (a.id < b.id avoids duplicates and self pairs)
SELECT a.name, b.name, a.city FROM employees a JOIN employees b ON a.city = b.city AND a.id < b.id ORDER BY a.city, a.name LIMIT 5;""", run=True),
            H("Many-to-many chain"),
            SQL("""SELECT e.name AS employee, p.name AS project, a.hours
FROM employees e
JOIN assignments a ON a.emp_id = e.id
JOIN projects p    ON p.id = a.project_id
ORDER BY a.hours DESC LIMIT 4;""", "three tables through the junction", run=True),
            H("Anti-join and semi-join patterns"),
            SQL("""-- ANTI: employees with NO assignment (three ways)
SELECT e.name FROM employees e LEFT JOIN assignments a ON a.emp_id = e.id WHERE a.emp_id IS NULL;
SELECT name FROM employees e WHERE NOT EXISTS (SELECT 1 FROM assignments a WHERE a.emp_id = e.id);
SELECT name FROM employees WHERE id NOT IN (SELECT emp_id FROM assignments);       -- safe only because emp_id has no NULLs""", "Asha and Farhan", run=True),
            SQL("""-- SEMI: employees WITH at least one assignment, each listed once
SELECT name FROM employees e WHERE EXISTS (SELECT 1 FROM assignments a WHERE a.emp_id = e.id);""", run=True),
            H("ON vs WHERE in outer joins (classic trap)"),
            SQL("""-- condition in ON: Design stays, its employee columns NULL
SELECT d.name, e.name FROM departments d LEFT JOIN employees e ON e.dept_id = d.id AND e.city = 'Pune';
-- condition in WHERE: filters after the join, silently turning it into an inner join
SELECT d.name, e.name FROM departments d LEFT JOIN employees e ON e.dept_id = d.id WHERE e.city = 'Pune';""", run=True),
            H("USING, NATURAL, non-equi joins"),
            SQL("""-- USING (id) joins on a same-named column and shows it once
SELECT * FROM employees JOIN employees AS b USING (id) LIMIT 1;
-- non-equi: pair each employee with the departments whose budget they could 'fund' 1000x
SELECT e.name, d.name FROM employees e JOIN departments d ON d.budget > e.salary * 5 WHERE e.id <= 2 ORDER BY 1, 2;""", run=True),
            MY("MySQL UPDATE/DELETE can use JOIN directly; PostgreSQL uses UPDATE ... FROM and DELETE ... USING (see DML topic). LEFT JOIN LATERAL is PostgreSQL (MySQL 8.0.14+ has LATERAL derived tables)."),
            H("Row-count rules (MCQ favourites)"),
            TBL(["Join", "Rows"],
                ["m rows join n rows, no condition", "m × n"],
                ["Inner join on FK to PK (every child has a parent)", "exactly the child count"],
                ["Left join", "at least the left count; more if one left row matches several right rows"],
                ["m rows, n rows, no matches, FULL join", "m + n"]),
            ASK("\"INNER vs LEFT JOIN?\" Inner keeps only matching rows. Left keeps all left rows and fills NULLs where there is no match. Use left joins when 'no related row' must still appear."),
        ],
        [
            Q("Table A has 5 rows, B has 4 rows. How many rows does A CROSS JOIN B return?", ["9", "20", "5", "4"], 1, "m × n."),
            Q("To list departments with their employee counts including empty departments you need:", ["INNER JOIN and COUNT(*)", "LEFT JOIN from departments and COUNT(e.id)", "RIGHT JOIN from departments", "CROSS JOIN"], 1, "LEFT JOIN keeps empty departments, and COUNT(e.id) counts 0 for them (COUNT(*) would count 1)."),
            Q("Moving a right-table filter from ON to WHERE in a LEFT JOIN:", ["Changes nothing", "Turns it effectively into an inner join", "Makes it a full join", "Is a syntax error"], 1, "WHERE removes the NULL-extended rows."),
            Q("Which is the standard way to find rows in A with no match in B, NULL-safely?", ["NOT IN (SELECT col FROM B)", "NOT EXISTS (correlated)", "A = B", "UNION"], 1, "NOT EXISTS handles NULLs correctly; NOT IN returns nothing if B.col has a NULL."),
            Q("MySQL has no FULL OUTER JOIN. The workaround is:", ["Two INNER JOINs", "LEFT JOIN UNION RIGHT JOIN", "CROSS JOIN", "NATURAL JOIN"], 1, "UNION of the two outer joins."),
            Q("In a self join for pairs in the same city, the condition a.id < b.id:", ["Orders the output", "Removes duplicate mirrored pairs and self pairs", "Speeds up the join", "Is required syntax"], 1, "Each unordered pair appears once and no row pairs with itself."),
        ], star=True, kw="join inner left right full outer cross natural self anti semi on where using non-equi"))

    # ------------------------------------------------------------------ subqueries
    T.append(topic("subqueries", GE, "Subqueries: scalar, IN, EXISTS, correlated, derived, LATERAL",
        "A query inside a query. Know which kind returns what and when to prefer a join.",
        [
            TBL(["Kind", "Returns", "Where used", "Example"],
                ["Scalar", "Exactly one value", "SELECT list, WHERE, SET", "salary > (SELECT AVG(salary) FROM employees)"],
                ["Row / column list", "A column of values", "IN, ANY, ALL, EXISTS", "id IN (SELECT emp_id FROM assignments)"],
                ["Table (derived table)", "A result set with an alias", "FROM", "FROM (SELECT ...) AS t"],
                ["Correlated", "References the outer row; re-evaluated per row", "WHERE, SELECT", "WHERE salary > (SELECT AVG(salary) FROM employees x WHERE x.dept_id = e.dept_id)"]),
            SQL("""-- scalar subquery
SELECT name, salary FROM employees WHERE salary > (SELECT AVG(salary) FROM employees) ORDER BY salary DESC;""", "above the company average (95200)", run=True),
            SQL("""-- IN with a subquery
SELECT name FROM employees WHERE dept_id IN (SELECT dept_id FROM projects WHERE budget >= 250000);""", run=True),
            SQL("""-- correlated: earns more than the average of their own department
SELECT e.name, e.dept_id, e.salary
FROM employees e
WHERE e.salary > (SELECT AVG(x.salary) FROM employees x WHERE x.dept_id = e.dept_id);""", run=True),
            SQL("""-- scalar subquery in SELECT
SELECT d.name, (SELECT COUNT(*) FROM employees e WHERE e.dept_id = d.id) AS headcount FROM departments d;""", run=True),
            SQL("""-- derived table in FROM
SELECT dept_id, avg_sal FROM (SELECT dept_id, AVG(salary) AS avg_sal FROM employees GROUP BY dept_id) t WHERE avg_sal > 100000;""", run=True),
            H("EXISTS vs IN"),
            UL("EXISTS returns TRUE as soon as the subquery finds one row; it stops early and ignores the select list (SELECT 1 is a convention).",
               "NOT EXISTS is NULL-safe. NOT IN is not (one NULL in the list returns no rows).",
               "Modern optimizers turn both into semi-joins; performance is usually equal. Choose by correctness: prefer EXISTS / NOT EXISTS for correlated membership tests."),
            H("ANY / ALL"),
            SQL("""-- (PostgreSQL / MySQL) salary greater than ALL salaries in dept 3
SELECT name FROM employees WHERE salary > (SELECT MAX(salary) FROM employees WHERE dept_id = 3);
-- ALL / ANY forms:  salary > ALL (SELECT salary FROM employees WHERE dept_id = 3)
--                   salary = ANY (SELECT ...)   is the same as IN""", "SQLite lacks ANY/ALL; MAX works the same", run=True),
            H("Nth highest salary (the classic)"),
            SQL("""-- 2nd highest distinct salary (OFFSET)
SELECT DISTINCT salary FROM employees ORDER BY salary DESC LIMIT 1 OFFSET 1;

-- 2nd highest using a subquery (works on any engine)
SELECT MAX(salary) FROM employees WHERE salary < (SELECT MAX(salary) FROM employees);

-- Nth via correlated count: N = 3 means exactly 2 distinct salaries are higher
SELECT DISTINCT e.salary FROM employees e WHERE (SELECT COUNT(DISTINCT x.salary) FROM employees x WHERE x.salary > e.salary) = 2;""", "120000, then 120000, then 98000", run=True),
            H("Top earner per department (correlated)"),
            SQL("""SELECT name, dept_id, salary FROM employees e
WHERE salary = (SELECT MAX(salary) FROM employees x WHERE x.dept_id = e.dept_id);""", "ties both appear: Meera and Vikram, Kiran and Nisha", run=True),
            H("LATERAL (PostgreSQL, MySQL 8.0.14+)"),
            PGSQL("""-- top 2 highest-paid per department, using LATERAL
SELECT d.name, t.name AS employee, t.salary
FROM departments d
CROSS JOIN LATERAL (SELECT e.name, e.salary FROM employees e WHERE e.dept_id = d.id ORDER BY e.salary DESC LIMIT 2) t;"""),
            H("Subqueries in UPDATE and DELETE"),
            SQL("""UPDATE employees SET salary = salary + 5000 WHERE dept_id IN (SELECT id FROM departments WHERE budget < 600000);
SELECT name, salary FROM employees WHERE dept_id = 3 ORDER BY id;""", run=True),
            MY("MySQL refuses to modify a table and select from the same table in one statement (error 1093) unless you wrap the subquery in a derived table. PostgreSQL has no such restriction."),
            TRAP("A scalar subquery that returns more than one row is an error ('more than one row returned by a subquery used as an expression'). Use LIMIT 1, an aggregate, or IN."),
            ASK("\"Correlated vs non-correlated subquery?\" A non-correlated subquery runs once independently. A correlated one refers to the outer row and is conceptually run once per outer row; it can often be rewritten as a join or window function."),
        ],
        [
            Q("Which subquery refers to a column of the outer query?", ["Scalar", "Derived table", "Correlated", "Uncorrelated"], 2, "That is the definition of correlated."),
            Q("Why is NOT EXISTS safer than NOT IN?", ["It is shorter", "It is not fooled by NULLs in the subquery", "It is always faster", "It allows aggregates"], 1, "NOT IN returns no rows if the list contains a NULL."),
            Q("Second highest distinct salary using only standard features:", ["SELECT MAX(salary) FROM e WHERE salary < (SELECT MAX(salary) FROM e)", "SELECT salary FROM e ORDER BY salary LIMIT 2", "SELECT MIN(salary) FROM e", "SELECT AVG(salary) FROM e"], 0, "Maximum of what remains after removing the maximum."),
            Q("A derived table in the FROM clause must:", ["Return one row", "Have an alias", "Use EXISTS", "Be correlated"], 1, "PostgreSQL and MySQL require an alias for it."),
            Q("MySQL error 1093 occurs when:", ["A join has no ON", "You update a table using a subquery on the same table", "A value is out of range", "A foreign key fails"], 1, "Wrap the subquery in a derived table to get around it."),
        ], star=True, kw="subquery scalar correlated exists not exists in any all derived table lateral nth highest second highest"))

    # ------------------------------------------------------------------ set ops
    T.append(topic("set-ops", GE, "UNION, UNION ALL, INTERSECT, EXCEPT",
        "Combine the results of whole queries. Both sides need the same number of columns with compatible types.",
        [
            TBL(["Operator", "Result", "Duplicates", "Notes"],
                ["UNION", "Rows in either query", "Removed (sort or hash)", "Slower than UNION ALL"],
                ["UNION ALL", "All rows of both", "Kept", "Fast; use when duplicates are impossible or wanted"],
                ["INTERSECT", "Rows in both", "Removed (INTERSECT ALL keeps)", "MySQL 8.0.31+"],
                ["EXCEPT / MINUS", "Rows in the first not in the second", "Removed", "PostgreSQL, SQL Server, SQLite: EXCEPT. Oracle: MINUS. MySQL 8.0.31+: EXCEPT"]),
            SQL("""SELECT city FROM employees WHERE dept_id = 1
UNION
SELECT city FROM employees WHERE dept_id = 3;""", "distinct cities", run=True),
            SQL("""SELECT city FROM employees WHERE dept_id = 1
UNION ALL
SELECT city FROM employees WHERE dept_id = 3;""", "6 rows: duplicates kept", run=True),
            SQL("""SELECT id FROM departments
EXCEPT
SELECT dept_id FROM employees;      -- departments with no employees""", run=True),
            SQL("""SELECT city FROM employees WHERE dept_id = 1
INTERSECT
SELECT city FROM employees WHERE dept_id = 2;      -- cities common to both departments""", run=True),
            UL("Column names come from the FIRST query.",
               "ORDER BY applies to the whole combined result and goes at the very end.",
               "Precedence: INTERSECT binds tighter than UNION and EXCEPT; use parentheses.",
               "NULLs are considered equal for duplicate removal here (unlike in =).",
               "Mismatched column counts or types are errors."),
            SQL("""SELECT name, 'employee' AS kind FROM employees WHERE id <= 2
UNION ALL
SELECT name, 'department' FROM departments
ORDER BY kind, name;""", "tagging rows by source", run=True),
            PGSQL("""-- full outer join vs UNION: finding rows that differ between two copies of a table
(SELECT * FROM t_old EXCEPT SELECT * FROM t_new)
UNION ALL
(SELECT * FROM t_new EXCEPT SELECT * FROM t_old);"""),
            ASK("\"UNION vs UNION ALL?\" UNION removes duplicates (extra sort/hash cost), UNION ALL keeps everything and is faster. Default to UNION ALL when you know rows cannot overlap."),
        ],
        [
            Q("Which keeps duplicate rows?", ["UNION", "INTERSECT", "UNION ALL", "EXCEPT"], 2, "UNION ALL does no duplicate elimination."),
            Q("Oracle's name for EXCEPT is:", ["SUBTRACT", "MINUS", "DIFF", "NOT IN"], 1, "Oracle uses MINUS."),
            Q("The column names of a UNION come from:", ["The second query", "The first query", "Both joined", "Alphabetical order"], 1, "The first SELECT defines the names."),
            Q("Set operations require:", ["Same table", "Same number of columns with compatible types", "Same row count", "A primary key"], 1, "Column count and types must line up."),
            Q("Which pair is guaranteed to give a distinct result?", ["UNION ALL", "UNION", "INTERSECT ALL", "EXCEPT ALL"], 1, "Plain UNION removes duplicates."),
        ], kw="union intersect except minus set operations all"))

    # ------------------------------------------------------------------ CTE
    T.append(topic("cte", GE, "CTEs (WITH) and recursive queries",
        "Common Table Expressions name a subquery so queries read top to bottom. Recursive CTEs walk trees and graphs.",
        [
            H("Basic CTE"),
            SQL("""WITH dept_stats AS (
  SELECT dept_id, AVG(salary) AS avg_sal, COUNT(*) AS n FROM employees WHERE dept_id IS NOT NULL GROUP BY dept_id
),
rich_depts AS (
  SELECT dept_id FROM dept_stats WHERE avg_sal > 100000
)
SELECT e.name, e.salary FROM employees e JOIN rich_depts r ON r.dept_id = e.dept_id ORDER BY e.salary DESC;""", "chained CTEs", run=True),
            UL("A CTE exists only for the one statement that follows it.",
               "Later CTEs can reference earlier ones. A CTE can be used several times in the main query.",
               "PostgreSQL 12+ inlines simple CTEs; use WITH x AS MATERIALIZED (...) or NOT MATERIALIZED to control it. Older versions always materialized them (an optimization fence).",
               "MySQL supports CTEs from 8.0. PostgreSQL also allows data-modifying CTEs (WITH moved AS (DELETE ... RETURNING *) INSERT ...)."),
            H("Recursive CTE: walk a hierarchy"),
            P("A recursive CTE has an anchor query, UNION ALL, and a recursive step that refers to the CTE itself. It stops when the recursive step returns no new rows."),
            SQL("""WITH RECURSIVE org AS (
  SELECT id, name, manager_id, 0 AS depth, name AS path FROM employees WHERE manager_id IS NULL AND id = 1   -- anchor
  UNION ALL
  SELECT e.id, e.name, e.manager_id, o.depth + 1, o.path || ' > ' || e.name
  FROM employees e JOIN org o ON e.manager_id = o.id                                                         -- recursive step
)
SELECT depth, path FROM org ORDER BY path;""", "everyone under Asha with the reporting chain", run=True),
            SQL("""-- generate a number series
WITH RECURSIVE n(x) AS (SELECT 1 UNION ALL SELECT x + 1 FROM n WHERE x < 5)
SELECT x FROM n;""", "PostgreSQL also has generate_series(1,5)", run=True),
            SQL("""-- every subordinate count under each manager
WITH RECURSIVE sub AS (
  SELECT id AS top, id AS member FROM employees
  UNION ALL
  SELECT s.top, e.id FROM sub s JOIN employees e ON e.manager_id = s.member
)
SELECT top, COUNT(*) - 1 AS reports FROM sub GROUP BY top HAVING COUNT(*) > 1 ORDER BY reports DESC;""", "total (direct + indirect) reports", run=True),
            TRAP("Forgetting the stop condition (or a cyclic graph) loops forever. PostgreSQL has CYCLE and SEARCH clauses (14+); MySQL limits depth with cte_max_recursion_depth (default 1000)."),
            H("CTE vs subquery vs temp table vs view"),
            TBL(["", "Best for"],
                ["Subquery", "Small one-off logic"],
                ["CTE", "Readability, reuse inside one statement, recursion"],
                ["Temp table", "Reusing an expensive result across several statements, indexing the intermediate"],
                ["View", "Reusable named query for many statements and users"]),
            ASK("\"What is a CTE and when use a recursive one?\" A named temporary result for one statement; recursive CTEs traverse hierarchies like org charts, category trees and bill of materials."),
        ],
        [
            Q("A CTE is visible:", ["For the whole session", "Only in the statement that follows it", "Across the database", "Until COMMIT"], 1, "It is scoped to the one statement."),
            Q("A recursive CTE consists of:", ["Two SELECTs joined by JOIN", "Anchor member UNION ALL recursive member", "A trigger and a view", "Only one SELECT"], 1, "Anchor + recursive part."),
            Q("What stops a recursive CTE?", ["COMMIT", "The recursive member returns no new rows", "LIMIT only", "A deadlock"], 1, "It runs until an iteration produces nothing."),
            Q("In MySQL, CTEs are available from version:", ["5.6", "5.7", "8.0", "They are not"], 2, "MySQL 8.0 added CTEs and window functions."),
            Q("Best tool to traverse an employee-manager hierarchy:", ["GROUP BY", "Recursive CTE", "UNION", "ORDER BY"], 1, "Recursive CTE walks arbitrary depth."),
        ], kw="cte with recursive hierarchy tree materialized"))

    # ------------------------------------------------------------------ windows
    T.append(topic("window", GE, "Window functions: ranking, LAG/LEAD, running totals",
        "Window functions compute across related rows WITHOUT collapsing them. They solve top-N per group, running totals, differences with the previous row and more. Heavily asked in interviews.",
        [
            H("Syntax"),
            SQL("""function(args) OVER (
  [PARTITION BY cols]       -- restart for each group
  [ORDER BY cols]           -- order inside the partition
  [ROWS | RANGE frame]      -- which rows around the current one
)""", "skeleton"),
            P("Compared with GROUP BY: GROUP BY returns one row per group; a window function keeps every row and adds a computed column. Window functions run after WHERE, GROUP BY and HAVING, so they cannot appear in WHERE: wrap in a subquery or CTE to filter on them."),
            H("Ranking functions"),
            SQL("""SELECT name, salary,
       ROW_NUMBER() OVER (ORDER BY salary DESC, id) AS row_num,   -- 1,2,3,4... no ties
       RANK()       OVER (ORDER BY salary DESC)     AS rnk,       -- ties share, then skip: 1,2,2,4
       DENSE_RANK() OVER (ORDER BY salary DESC)     AS dense      -- ties share, no skip: 1,2,2,3
FROM employees ORDER BY salary DESC, id;""", "compare the three on the tied 120000 and 92000", run=True),
            TBL(["Function", "Ties", "Next value after a tie of 2"],
                ["ROW_NUMBER", "Broken arbitrarily", "Continues 1,2,3,4"],
                ["RANK", "Same rank", "Skips: 1,2,2,4"],
                ["DENSE_RANK", "Same rank", "No skip: 1,2,2,3"],
                ["NTILE(n)", "Splits into n buckets", "Bucket numbers"],
                ["PERCENT_RANK / CUME_DIST", "Relative position 0-1", ""]),
            H("Top N per group"),
            SQL("""SELECT * FROM (
  SELECT name, dept_id, salary, ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC, id) AS rn
  FROM employees WHERE dept_id IS NOT NULL
) t WHERE rn <= 2 ORDER BY dept_id, rn;""", "two highest-paid per department", run=True),
            SQL("""-- all employees tied for the top salary in their department: use RANK
SELECT name, dept_id, salary FROM (
  SELECT name, dept_id, salary, RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS r FROM employees WHERE dept_id IS NOT NULL
) t WHERE r = 1;""", run=True),
            H("LAG, LEAD, FIRST_VALUE, LAST_VALUE"),
            SQL("""SELECT name, hire_date, salary,
       LAG(salary)  OVER (ORDER BY hire_date) AS prev_salary,
       LEAD(salary) OVER (ORDER BY hire_date) AS next_salary,
       salary - LAG(salary, 1, salary) OVER (ORDER BY hire_date) AS change_vs_prev,
       FIRST_VALUE(name) OVER (ORDER BY hire_date) AS first_hire
FROM employees ORDER BY hire_date;""", "LAG(x, offset, default)", run=True),
            H("Running totals, moving averages, shares"),
            SQL("""SELECT name, hire_date, salary,
       SUM(salary) OVER (ORDER BY hire_date, id)                              AS running_total,
       ROUND(AVG(salary) OVER (ORDER BY hire_date, id ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)) AS moving_avg_3,
       ROUND(100.0 * salary / SUM(salary) OVER (), 1)                         AS pct_of_total,
       SUM(salary) OVER (PARTITION BY dept_id)                                AS dept_total
FROM employees ORDER BY hire_date, id;""", "ROWS frame, whole-table window with empty OVER()", run=True),
            H("Frames"),
            UL("Default frame when ORDER BY is present: RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW (peers with the same ORDER BY value are included together).",
               "ROWS counts physical rows; RANGE groups equal values. Use ROWS for exact moving windows.",
               "LAST_VALUE needs an explicit frame (ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) or it just returns the current row.",
               "Named windows: ... OVER w ... WINDOW w AS (PARTITION BY dept_id ORDER BY salary)."),
            H("Deduplicate and gaps"),
            SQL("""-- keep one row per salary (delete-duplicate pattern)
SELECT id, name, salary FROM (
  SELECT id, name, salary, ROW_NUMBER() OVER (PARTITION BY salary ORDER BY id) AS rn FROM employees
) t WHERE rn = 1 ORDER BY id;""", run=True),
            H("Percentiles"),
            PGSQL("SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) AS median FROM employees;"),
            MYSQL("-- MySQL has no PERCENTILE_CONT; compute the median with ROW_NUMBER and COUNT or PERCENT_RANK."),
            ASK("\"RANK vs DENSE_RANK vs ROW_NUMBER?\" ROW_NUMBER gives unique numbers, RANK leaves gaps after ties, DENSE_RANK does not. For 'Nth highest salary with ties' use DENSE_RANK."),
        ],
        [
            Q("Salaries 100, 90, 90, 80. DENSE_RANK of 80 is:", ["2", "3", "4", "1"], 1, "Dense rank has no gaps: 1, 2, 2, 3."),
            Q("Salaries 100, 90, 90, 80. RANK of 80 is:", ["3", "4", "2", "1"], 1, "Ties take rank 2 twice, then the next is 4."),
            Q("Window functions are evaluated:", ["Before WHERE", "After WHERE, GROUP BY and HAVING", "Before FROM", "Only in HAVING"], 1, "That is why you filter on them with a subquery or CTE."),
            Q("Which function gives the previous row's value?", ["LEAD", "LAG", "NTILE", "FIRST_VALUE"], 1, "LAG looks back; LEAD looks forward."),
            Q("SUM(x) OVER () returns:", ["One row total", "The grand total repeated on every row", "A running total", "Per-group totals"], 1, "Empty OVER means one window covering all rows."),
            Q("Top 2 salaries per department is best written with:", ["GROUP BY dept_id LIMIT 2", "ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC) <= 2 in an outer query", "DISTINCT", "HAVING salary < 3"], 1, "Rank inside each partition, then filter in the outer query."),
        ], star=True, kw="window function row_number rank dense_rank lag lead over partition by running total moving average ntile top n per group"))

    return T
