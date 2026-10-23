"""Study guide, part 3c: DML, views, index syntax, classic interview queries."""
from mat_common import *

GE = "E. Writing queries"
GI = "F. Classic interview queries"


def build():
    T = []

    # ------------------------------------------------------------------ DML
    T.append(topic("dml", GE, "INSERT, UPDATE, DELETE, UPSERT, MERGE, RETURNING",
        "Changing data. Interviews ask for the upsert forms, UPDATE with a join, and how to delete duplicates.",
        [
            H("INSERT"),
            SQL("""CREATE TABLE gadget (id INTEGER PRIMARY KEY, name TEXT NOT NULL, price NUMERIC DEFAULT 0, qty INTEGER DEFAULT 0);
INSERT INTO gadget (id, name, price, qty) VALUES (1, 'lamp', 499, 10);                       -- one row
INSERT INTO gadget (id, name, price) VALUES (2, 'fan', 1899), (3, 'kettle', 999);             -- several rows, qty uses DEFAULT
INSERT INTO gadget (id, name) SELECT id + 100, name || ' copy' FROM gadget WHERE id <= 2;       -- INSERT ... SELECT
SELECT * FROM gadget ORDER BY id;""", "column list is optional but always write it", run=True),
            UL("Always list the columns; a bare INSERT INTO t VALUES (...) breaks when the table gains a column.",
               "Omitted columns get their DEFAULT, or NULL, or an error if they are NOT NULL without a default.",
               "PostgreSQL: INSERT INTO t DEFAULT VALUES; also INSERT ... RETURNING id. MySQL: INSERT IGNORE skips rows that violate unique keys; REPLACE INTO deletes the old row then inserts (avoid, it fires delete triggers and breaks FKs).",
               "Bulk loads: PostgreSQL COPY t FROM '/path.csv' CSV HEADER (or \\copy in psql); MySQL LOAD DATA INFILE. Far faster than thousands of INSERTs."),
            H("UPDATE"),
            SQL("""CREATE TABLE gadget (id INTEGER PRIMARY KEY, name TEXT NOT NULL, price NUMERIC DEFAULT 0, qty INTEGER DEFAULT 0);
INSERT INTO gadget VALUES (1,'lamp',499,10),(2,'fan',1899,0),(101,'lamp copy',0,0);
UPDATE gadget SET price = price * 1.10 WHERE name = 'lamp';                -- expression using the old value
UPDATE gadget SET price = 0, qty = 0 WHERE id > 100;                              -- several columns
UPDATE gadget SET qty = (SELECT COUNT(*) FROM employees) WHERE id = 1;            -- value from a subquery
SELECT id, name, price, qty FROM gadget ORDER BY id;""", run=True),
            TRAP("UPDATE or DELETE without WHERE changes every row. In an interview, say 'I would run it as a SELECT first, and inside a transaction'."),
            H("UPDATE with a join (syntax differs)"),
            PGSQL("""UPDATE employees e
SET    salary = e.salary * 1.05
FROM   departments d
WHERE  d.id = e.dept_id AND d.name = 'Data';"""),
            MYSQL("""UPDATE employees e
JOIN   departments d ON d.id = e.dept_id
SET    e.salary = e.salary * 1.05
WHERE  d.name = 'Data';"""),
            SQL("""-- portable form with a subquery (runs everywhere)
UPDATE employees SET salary = salary * 1.05 WHERE dept_id IN (SELECT id FROM departments WHERE name = 'Data');
SELECT name, salary FROM employees WHERE dept_id = 2 ORDER BY id;""", run=True),
            H("DELETE (and deleting with a join)"),
            SQL("""CREATE TABLE gadget (id INTEGER PRIMARY KEY, name TEXT NOT NULL, price NUMERIC DEFAULT 0, qty INTEGER DEFAULT 0);
INSERT INTO gadget VALUES (1,'lamp',499,10),(2,'fan',1899,0),(101,'lamp copy',0,0);
DELETE FROM gadget WHERE id > 100;
SELECT COUNT(*) AS left_rows FROM gadget;""", run=True),
            PGSQL("DELETE FROM assignments a USING projects p WHERE p.id = a.project_id AND p.budget < 150000;"),
            MYSQL("DELETE a FROM assignments a JOIN projects p ON p.id = a.project_id WHERE p.budget < 150000;"),
            H("Delete duplicate rows, keep one"),
            SQL("""CREATE TABLE emailing (id INTEGER PRIMARY KEY, email TEXT);
INSERT INTO emailing VALUES (1,'a@x'),(2,'b@x'),(3,'a@x'),(4,'a@x'),(5,'b@x');
DELETE FROM emailing WHERE id NOT IN (SELECT MIN(id) FROM emailing GROUP BY email);   -- keep the smallest id per email
SELECT * FROM emailing ORDER BY id;""", "left with ids 1 and 2", run=True),
            PGSQL("""DELETE FROM emailing a USING emailing b WHERE a.email = b.email AND a.id > b.id;       -- self-join delete
-- or with a window function:
DELETE FROM emailing WHERE id IN (SELECT id FROM (SELECT id, ROW_NUMBER() OVER (PARTITION BY email ORDER BY id) rn FROM emailing) t WHERE rn > 1);"""),
            H("UPSERT: insert or update if it exists"),
            SQL("""CREATE TABLE stock (sku TEXT PRIMARY KEY, qty INTEGER NOT NULL);
INSERT INTO stock VALUES ('A1', 5);
INSERT INTO stock (sku, qty) VALUES ('A1', 3) ON CONFLICT (sku) DO UPDATE SET qty = stock.qty + excluded.qty;
INSERT INTO stock (sku, qty) VALUES ('B2', 7) ON CONFLICT (sku) DO NOTHING;
SELECT * FROM stock ORDER BY sku;""", "PostgreSQL and SQLite syntax: A1 becomes 8", run=True),
            MYSQL("""INSERT INTO stock (sku, qty) VALUES ('A1', 3)
ON DUPLICATE KEY UPDATE qty = qty + VALUES(qty);      -- newer: AS new ... qty = qty + new.qty
INSERT IGNORE INTO stock (sku, qty) VALUES ('B2', 7);"""),
            H("MERGE (SQL standard)"),
            PGSQL("""MERGE INTO stock s                                    -- PostgreSQL 15+
USING incoming i ON s.sku = i.sku
WHEN MATCHED THEN UPDATE SET qty = s.qty + i.qty
WHEN NOT MATCHED THEN INSERT (sku, qty) VALUES (i.sku, i.qty);"""),
            MY("MySQL has no MERGE; use INSERT ... ON DUPLICATE KEY UPDATE. Oracle and SQL Server do have MERGE."),
            H("RETURNING (PostgreSQL, SQLite 3.35+, MariaDB)"),
            SQL("""CREATE TABLE stock (sku TEXT PRIMARY KEY, qty INTEGER NOT NULL);
INSERT INTO stock (sku, qty) VALUES ('C3', 1) RETURNING sku, qty;
UPDATE stock SET qty = qty + 1 WHERE sku = 'C3' RETURNING *;""", "get changed rows back without a second query", run=True),
            ASK("\"How do you insert if not exists, update otherwise?\" PostgreSQL: INSERT ... ON CONFLICT (key) DO UPDATE. MySQL: INSERT ... ON DUPLICATE KEY UPDATE. Standard: MERGE."),
        ],
        [
            Q("PostgreSQL upsert clause:", ["ON DUPLICATE KEY UPDATE", "ON CONFLICT ... DO UPDATE", "REPLACE INTO", "UPSERT INTO"], 1, "The first is MySQL, REPLACE INTO deletes and reinserts."),
            Q("Which statement forgets WHERE and updates every row?", ["UPDATE t SET x = 1", "UPDATE t SET x = 1 WHERE id = 1", "SELECT x FROM t", "DELETE FROM t WHERE id = 1"], 0, "No WHERE means all rows."),
            Q("Updating with a join in PostgreSQL uses:", ["UPDATE ... JOIN ... SET", "UPDATE ... FROM ... WHERE", "UPDATE ... INNER USING", "MERGE only"], 1, "MySQL uses UPDATE ... JOIN ... SET."),
            Q("Which returns the generated id of an insert in PostgreSQL?", ["OUTPUT", "RETURNING", "GETID", "SCOPE_IDENTITY"], 1, "INSERT ... RETURNING."),
            Q("To delete duplicates but keep the first, you can delete rows where id NOT IN:", ["SELECT MAX(id) ... GROUP BY key (keeps last)", "SELECT MIN(id) ... GROUP BY key (keeps first)", "SELECT COUNT(*)", "SELECT DISTINCT *"], 1, "MIN(id) per group keeps the first row of each."),
        ], star=True, kw="insert update delete upsert on conflict merge returning bulk copy delete duplicates update join"))

    # ------------------------------------------------------------------ views
    T.append(topic("views", GE, "Views and materialized views",
        "A view is a stored query that behaves like a table. Interviews ask what they are for and whether they can be updated.",
        [
            SQL("""CREATE VIEW dept_summary AS
SELECT d.id AS dept_id, d.name AS dept, COUNT(e.id) AS headcount, COALESCE(SUM(e.salary), 0) AS payroll
FROM departments d LEFT JOIN employees e ON e.dept_id = d.id
GROUP BY d.id, d.name;
SELECT * FROM dept_summary ORDER BY payroll DESC;""", run=True),
            UL("A view stores **no data**, only the query. Each use re-runs it (the optimizer merges it into the outer query).",
               "**Uses:** hide complexity, give users a restricted view (column or row security), keep a stable interface when tables change (logical data independence), reuse business definitions.",
               "ALTER/REPLACE: CREATE OR REPLACE VIEW (PostgreSQL, MySQL). DROP VIEW v. PostgreSQL ALTER VIEW only renames or changes ownership/defaults.",
               "**Updatable views:** simple views on one table without DISTINCT, GROUP BY, aggregates, window functions or set operations can take INSERT/UPDATE/DELETE, which pass through to the base table. Complex views are read-only unless you add INSTEAD OF triggers (PostgreSQL)."),
            H("WITH CHECK OPTION"),
            SQL("""CREATE VIEW pune_staff AS SELECT id, name, city FROM employees WHERE city = 'Pune' WITH CHECK OPTION;
-- UPDATE pune_staff SET city = 'Delhi' WHERE id = 5;   -- rejected: the row would leave the view""", "PostgreSQL / MySQL (SQLite has no CHECK OPTION)"),
            PG("PostgreSQL supports WITH LOCAL | CASCADED CHECK OPTION and security_barrier views. Revoke access to the base table and GRANT SELECT on the view to expose only some columns."),
            H("Materialized views"),
            PGSQL("""CREATE MATERIALIZED VIEW sales_by_month AS
SELECT date_trunc('month', placed_at) AS month, SUM(total) AS revenue FROM orders GROUP BY 1;

CREATE UNIQUE INDEX ON sales_by_month (month);
REFRESH MATERIALIZED VIEW sales_by_month;                     -- locks readers
REFRESH MATERIALIZED VIEW CONCURRENTLY sales_by_month;       -- needs a unique index, no read lock"""),
            MY("MySQL has no materialized views. Emulate with a summary table refreshed by a scheduled EVENT or application job."),
            TBL(["", "View", "Materialized view", "Table"],
                ["Stores data", "No", "Yes (snapshot)", "Yes"],
                ["Always current", "Yes", "Only after refresh", "Yes"],
                ["Can be indexed", "No", "Yes (PostgreSQL)", "Yes"],
                ["Speed", "Same as the query", "Fast reads", "Fast"]),
            ASK("\"View vs table? Can you insert into a view?\" A view is a saved query with no data of its own. Simple single-table views are updatable; joins, aggregates and DISTINCT views are not, unless INSTEAD OF triggers handle the write."),
        ],
        [
            Q("A standard view stores:", ["A copy of the data", "Only the query definition", "Indexes only", "Permissions only"], 1, "Data is read from base tables at query time."),
            Q("WITH CHECK OPTION prevents:", ["Selects", "Writes that make a row disappear from the view", "Indexing", "Joins"], 1, "Rows inserted or updated through the view must still satisfy its WHERE."),
            Q("Which view is typically NOT updatable?", ["SELECT a, b FROM t WHERE a > 1", "SELECT dept_id, COUNT(*) FROM t GROUP BY dept_id", "SELECT * FROM t", "SELECT a FROM t WHERE b = 2"], 1, "Aggregation loses the mapping to base rows."),
            Q("Which engine lacks materialized views?", ["PostgreSQL", "Oracle", "MySQL", "SQL Server (indexed views)"], 2, "MySQL has none; use summary tables."),
            Q("REFRESH MATERIALIZED VIEW CONCURRENTLY requires:", ["A trigger", "A unique index on the view", "Superuser", "A partition"], 1, "PostgreSQL needs a unique index to diff the old and new contents."),
        ], kw="view materialized view with check option updatable instead of security"))

    # ------------------------------------------------------------------ index sql
    T.append(topic("indexes-sql", GE, "Creating and using indexes (syntax and EXPLAIN)",
        "The SQL side of indexing. Theory is in 'File organisation and indexing'.",
        [
            SQL("""CREATE INDEX idx_emp_dept ON employees (dept_id);                       -- single column
CREATE INDEX idx_emp_city_sal ON employees (city, salary DESC);               -- composite
CREATE UNIQUE INDEX uq_emp_name_city ON employees (name, city);               -- enforces uniqueness
EXPLAIN QUERY PLAN SELECT * FROM employees WHERE dept_id = 2;                 -- shows SEARCH using index
EXPLAIN QUERY PLAN SELECT * FROM employees WHERE salary > 1;                  -- SCAN (no index on salary)""", "SQLite shows the plan here", run=True),
            TBL(["Task", "PostgreSQL", "MySQL"],
                ["Create", "CREATE INDEX name ON t (col);", "CREATE INDEX name ON t (col);  or ALTER TABLE t ADD INDEX ..."],
                ["Unique", "CREATE UNIQUE INDEX ...", "CREATE UNIQUE INDEX ..."],
                ["Partial index", "CREATE INDEX ... ON t (col) WHERE active;", "Not supported"],
                ["Expression index", "CREATE INDEX ... ON t (LOWER(email));", "Functional key parts (8.0.13+): ((LOWER(email)))"],
                ["Index type", "USING btree | hash | gin | gist | brin", "USING BTREE | HASH; FULLTEXT; SPATIAL"],
                ["Build without blocking writes", "CREATE INDEX CONCURRENTLY ...", "ALGORITHM=INPLACE, LOCK=NONE (online DDL)"],
                ["Drop", "DROP INDEX name;", "DROP INDEX name ON t;"],
                ["Covering columns", "CREATE INDEX ... ON t (a) INCLUDE (b);", "put columns in the index itself"],
                ["Show indexes", "\\d table  or  pg_indexes", "SHOW INDEX FROM t;"],
                ["Plan", "EXPLAIN (ANALYZE, BUFFERS) query;", "EXPLAIN [ANALYZE] query;"]),
            PGSQL("""CREATE INDEX idx_orders_open ON orders (customer_id) WHERE status = 'new';      -- small, targeted
CREATE INDEX idx_users_lower_email ON users (LOWER(email));                              -- serves WHERE LOWER(email) = ...
CREATE INDEX idx_docs_tsv ON docs USING gin (to_tsvector('english', body));              -- full text
CREATE INDEX idx_events_brin ON events USING brin (created_at);                          -- huge append-only table
CREATE INDEX CONCURRENTLY idx_big ON big_table (col);                                    -- no write lock (cannot run in a transaction)"""),
            H("Checklist"),
            UL("Unique and primary key constraints create their own indexes automatically.",
               "Index every foreign key column (PostgreSQL does not; InnoDB does).",
               "Composite order: equality columns first, then range, then ORDER BY columns.",
               "Verify with EXPLAIN; an unused index only slows writes.",
               "Rebuild / maintain: PostgreSQL REINDEX, VACUUM ANALYZE; MySQL OPTIMIZE TABLE, ANALYZE TABLE."),
            ASK("\"Table has 10 million rows and the query is slow: what first?\" EXPLAIN it, find the scan, index the filter/join columns in the right order, re-check the plan."),
        ],
        [
            Q("Which index only exists in PostgreSQL among the two?", ["Composite", "Partial", "Unique", "B-tree"], 1, "MySQL cannot index a subset of rows."),
            Q("Build an index in PostgreSQL without blocking writes:", ["CREATE INDEX ONLINE", "CREATE INDEX CONCURRENTLY", "CREATE LAZY INDEX", "ALTER INDEX NOWAIT"], 1, "CONCURRENTLY, and it cannot run inside a transaction block."),
            Q("PRIMARY KEY and UNIQUE automatically create:", ["A view", "An index", "A trigger", "A sequence only"], 1, "A unique index backs each of them."),
            Q("An index on LOWER(email) is called:", ["Partial", "Covering", "Expression (functional)", "Bitmap"], 2, "It indexes the result of an expression."),
            Q("Which index type suits a huge append-only time-series table in PostgreSQL?", ["BRIN", "Hash", "GIN", "Bitmap"], 0, "BRIN stores min/max per block range with tiny size."),
        ], kw="create index unique composite partial expression covering concurrently explain drop"))

    # ================================================================== CLASSICS
    T.append(topic("classics-1", GI, "Classic interview queries, set 1: the basics (12)",
        "These are the queries companies reuse. Each has the problem, a tested solution on the sample database, and the idea to say out loud. " + "Tables: employees(id, name, dept_id, manager_id, salary, hire_date, city), departments(id, name, budget), projects, assignments(emp_id, project_id, hours), logins(emp_id, login_date).",
        [
            H("1. Second highest salary"),
            P("Return the second highest distinct salary."),
            SQL("""SELECT MAX(salary) AS second_highest FROM employees WHERE salary < (SELECT MAX(salary) FROM employees);
-- or: SELECT DISTINCT salary FROM employees ORDER BY salary DESC LIMIT 1 OFFSET 1;
-- or: SELECT salary FROM (SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) r FROM employees) t WHERE r = 2 LIMIT 1;""", run=True),
            NOTE("Return NULL (not an error) when there is no second salary: the MAX form does that naturally. State the tie handling: DISTINCT / DENSE_RANK treats equal salaries as one rank."),
            H("2. Nth highest salary in general"),
            SQL("""SELECT salary FROM (
  SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS r FROM employees
) t WHERE r = 3 GROUP BY salary;     -- change 3 to N""", "98000", run=True),
            H("3. Find duplicate values"),
            SQL("""SELECT salary, COUNT(*) AS times FROM employees GROUP BY salary HAVING COUNT(*) > 1;""", "92000 and 120000 appear twice", run=True),
            H("4. Employees who earn more than their manager"),
            SQL("""SELECT e.name FROM employees e JOIN employees m ON m.id = e.manager_id WHERE e.salary > m.salary;""", "Kiran, Nisha", run=True),
            H("5. Departments with no employees"),
            SQL("""SELECT d.name FROM departments d LEFT JOIN employees e ON e.dept_id = d.id WHERE e.id IS NULL;
-- or NOT EXISTS / EXCEPT""", "Design", run=True),
            H("6. Employees with no department"),
            SQL("""SELECT name FROM employees WHERE dept_id IS NULL;""", "Farhan", run=True),
            H("7. Department-wise highest paid (with ties)"),
            SQL("""SELECT d.name AS dept, e.name, e.salary
FROM employees e JOIN departments d ON d.id = e.dept_id
WHERE e.salary = (SELECT MAX(salary) FROM employees x WHERE x.dept_id = e.dept_id)
ORDER BY d.name;""", run=True),
            H("8. Employees earning above their department average"),
            SQL("""SELECT e.name, e.salary FROM employees e
WHERE e.salary > (SELECT AVG(x.salary) FROM employees x WHERE x.dept_id = e.dept_id);""", "correlated; the window version avoids the repeated subquery", run=True),
            SQL("""SELECT name, salary FROM (SELECT name, salary, AVG(salary) OVER (PARTITION BY dept_id) AS dept_avg FROM employees) t WHERE salary > dept_avg;""", "window version", run=True),
            H("9. Headcount per department including zeros"),
            SQL("""SELECT d.name, COUNT(e.id) AS headcount FROM departments d LEFT JOIN employees e ON e.dept_id = d.id GROUP BY d.id, d.name ORDER BY headcount DESC;""", run=True),
            H("10. Departments with more than 2 employees"),
            SQL("""SELECT d.name, COUNT(*) AS n FROM employees e JOIN departments d ON d.id = e.dept_id GROUP BY d.id, d.name HAVING COUNT(*) > 2;""", run=True),
            H("11. Top 3 salaries (with ties) overall"),
            SQL("""SELECT name, salary FROM (SELECT name, salary, DENSE_RANK() OVER (ORDER BY salary DESC) r FROM employees) t WHERE r <= 3 ORDER BY salary DESC, name;""", "ROW_NUMBER would cut tied rows", run=True),
            H("12. Employees assigned to every project of department 1 (relational division)"),
            SQL("""-- employees assigned to ALL projects of dept 1
SELECT e.name FROM employees e
WHERE NOT EXISTS (SELECT 1 FROM projects p WHERE p.dept_id = 1
                  AND NOT EXISTS (SELECT 1 FROM assignments a WHERE a.emp_id = e.id AND a.project_id = p.id));
-- GROUP BY form: count distinct required projects and compare
SELECT a.emp_id FROM assignments a JOIN projects p ON p.id = a.project_id WHERE p.dept_id = 1
GROUP BY a.emp_id HAVING COUNT(DISTINCT p.id) = (SELECT COUNT(*) FROM projects WHERE dept_id = 1);""", "Rohan (id 2)", run=True),
            ASK("When you give an answer, name the edge cases unprompted: ties, NULLs, empty groups, and what the query returns when nothing matches."),
        ],
        [
            Q("Which function keeps ties together when finding the 3rd highest salary?", ["ROW_NUMBER", "RANK", "DENSE_RANK", "NTILE"], 2, "DENSE_RANK has no gaps, so 'third distinct salary' is rank 3."),
            Q("How many employees earn more than their manager in the sample data?", ["0", "2", "3", "4"], 1, "Kiran (92000 vs Arjun 88000) and Nisha (92000 vs Arjun 88000)."),
            Q("To list departments with zero employees you use:", ["INNER JOIN", "LEFT JOIN ... WHERE e.id IS NULL", "CROSS JOIN", "UNION"], 1, "Anti-join: unmatched left rows have NULL right columns."),
            Q("The HAVING clause in 'departments with more than 2 employees' is needed because:", ["WHERE cannot filter on COUNT(*)", "HAVING is faster", "GROUP BY requires it", "JOIN requires it"], 0, "The count exists only after grouping."),
            Q("Duplicates in a column are found with:", ["GROUP BY col HAVING COUNT(*) > 1", "ORDER BY col", "DISTINCT col", "LIMIT 1"], 0, "Group, count, keep groups with more than one row."),
        ], star=True, kw="interview classic queries second highest nth salary duplicates manager department no employees top n ties division"))

    T.append(topic("classics-2", GI, "Classic interview queries, set 2: window, gaps, pivot, hierarchy (12)",
        "The harder tier asked by product companies. Each solution is tested on the sample data.",
        [
            H("13. Running total"),
            SQL("""SELECT name, hire_date, salary, SUM(salary) OVER (ORDER BY hire_date, id) AS running_payroll FROM employees ORDER BY hire_date, id;""", run=True),
            H("14. Consecutive login streaks (gaps and islands)"),
            P("Idea: subtract the row number from the date. Consecutive days give the same constant, which labels the island."),
            SQL("""WITH x AS (
  SELECT emp_id, login_date,
         date(login_date, '-' || ROW_NUMBER() OVER (PARTITION BY emp_id ORDER BY login_date) || ' day') AS grp
  FROM logins
)
SELECT emp_id, COUNT(*) AS streak, MIN(login_date) AS from_date, MAX(login_date) AS to_date
FROM x GROUP BY emp_id, grp ORDER BY streak DESC, emp_id;""", "Employee 7 has the longest streak: 4 days", run=True),
            PGSQL("""-- PostgreSQL form of the same idea
SELECT emp_id, COUNT(*) AS streak, MIN(login_date), MAX(login_date)
FROM (SELECT emp_id, login_date, login_date::date - (ROW_NUMBER() OVER (PARTITION BY emp_id ORDER BY login_date))::int AS grp FROM logins) t
GROUP BY emp_id, grp;"""),
            H("15. Users who logged in 3 days in a row"),
            SQL("""SELECT DISTINCT a.emp_id FROM logins a
JOIN logins b ON b.emp_id = a.emp_id AND b.login_date = date(a.login_date, '+1 day')
JOIN logins c ON c.emp_id = a.emp_id AND c.login_date = date(a.login_date, '+2 day');""", "self-join method (employees 2 and 7)", run=True),
            H("16. Change versus the previous row"),
            SQL("""SELECT name, hire_date, salary, salary - LAG(salary) OVER (ORDER BY hire_date, id) AS diff_from_previous_hire FROM employees ORDER BY hire_date, id;""", run=True),
            H("17. Pivot rows to columns"),
            SQL("""SELECT dept_id,
       SUM(CASE WHEN city = 'Bengaluru' THEN 1 ELSE 0 END) AS bengaluru,
       SUM(CASE WHEN city = 'Hyderabad' THEN 1 ELSE 0 END) AS hyderabad,
       SUM(CASE WHEN city = 'Pune'      THEN 1 ELSE 0 END) AS pune
FROM employees WHERE dept_id IS NOT NULL GROUP BY dept_id ORDER BY dept_id;""", run=True),
            PGSQL("SELECT * FROM crosstab('SELECT dept_id, city, COUNT(*) FROM employees GROUP BY 1,2 ORDER BY 1,2') AS ct(dept_id int, bengaluru int, hyderabad int, pune int);   -- needs the tablefunc extension"),
            H("18. Median salary"),
            SQL("""SELECT AVG(salary) AS median FROM (
  SELECT salary, ROW_NUMBER() OVER (ORDER BY salary) AS rn, COUNT(*) OVER () AS cnt FROM employees
) t WHERE rn IN ((cnt + 1) / 2, (cnt + 2) / 2);""", "works on any engine with window functions", run=True),
            PGSQL("SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) FROM employees;"),
            H("19. Find missing numbers in a sequence"),
            SQL("""CREATE TABLE seq (n INTEGER);
INSERT INTO seq VALUES (1),(2),(4),(7),(8);
WITH RECURSIVE all_n(x) AS (SELECT 1 UNION ALL SELECT x + 1 FROM all_n WHERE x < (SELECT MAX(n) FROM seq))
SELECT x AS missing FROM all_n WHERE x NOT IN (SELECT n FROM seq);""", "3, 5, 6", run=True),
            PGSQL("SELECT x FROM generate_series(1, (SELECT MAX(n) FROM seq)) x WHERE x NOT IN (SELECT n FROM seq);"),
            H("20. Cumulative percentage and share of total"),
            SQL("""SELECT name, salary,
       ROUND(100.0 * salary / SUM(salary) OVER (), 1) AS pct,
       ROUND(100.0 * SUM(salary) OVER (ORDER BY salary DESC, id) / SUM(salary) OVER (), 1) AS cum_pct
FROM employees ORDER BY salary DESC, id;""", run=True),
            H("21. First and last record per group"),
            SQL("""SELECT DISTINCT dept_id,
       FIRST_VALUE(name) OVER (PARTITION BY dept_id ORDER BY hire_date ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS first_hire,
       LAST_VALUE(name)  OVER (PARTITION BY dept_id ORDER BY hire_date ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS latest_hire
FROM employees WHERE dept_id IS NOT NULL ORDER BY dept_id;""", "LAST_VALUE needs the full frame", run=True),
            H("22. Org chart: everyone under a manager"),
            SQL("""WITH RECURSIVE t AS (SELECT id, name, 0 AS lvl FROM employees WHERE id = 3
  UNION ALL SELECT e.id, e.name, t.lvl + 1 FROM employees e JOIN t ON e.manager_id = t.id)
SELECT * FROM t ORDER BY lvl, id;""", run=True),
            H("23. Hires per year with year-over-year change"),
            SQL("""WITH y AS (SELECT strftime('%Y', hire_date) AS yr, COUNT(*) AS hires FROM employees GROUP BY 1)
SELECT yr, hires, hires - LAG(hires) OVER (ORDER BY yr) AS change FROM y ORDER BY yr;""", "strftime is SQLite; PostgreSQL uses EXTRACT(YEAR FROM hire_date)", run=True),
            H("24. Projects nobody is assigned to / employees on several projects"),
            SQL("""SELECT p.name FROM projects p WHERE NOT EXISTS (SELECT 1 FROM assignments a WHERE a.project_id = p.id);
SELECT e.name, COUNT(*) AS projects FROM employees e JOIN assignments a ON a.emp_id = e.id GROUP BY e.id, e.name HAVING COUNT(*) > 1;""", "no idle project; Rohan is on 2", run=True),
            H("Swap values with CASE (a classic)"),
            SQL("""CREATE TABLE seat (id INTEGER, student TEXT);
INSERT INTO seat VALUES (1,'A'),(2,'B'),(3,'C'),(4,'D'),(5,'E');
SELECT CASE WHEN id % 2 = 1 AND id < (SELECT MAX(id) FROM seat) THEN id + 1
            WHEN id % 2 = 0 THEN id - 1 ELSE id END AS id, student
FROM seat ORDER BY 1;""", "swap adjacent seats; the last odd one stays", run=True),
            ASK("For streak and island problems say the trick: 'row number minus the value is constant inside a run.' For nth-per-group say: 'rank inside the partition, filter outside.'"),
        ],
        [
            Q("The 'date minus row_number' trick finds:", ["Duplicates", "Consecutive runs (gaps and islands)", "Medians", "Hierarchies"], 1, "Within a run both advance by 1, so the difference is constant."),
            Q("LAST_VALUE(x) OVER (ORDER BY y) without a frame returns:", ["The last row of the partition", "The current row's value (default frame ends at current row)", "NULL", "An error"], 1, "Specify ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING."),
            Q("Pivoting rows to columns without PIVOT uses:", ["UNION", "SUM(CASE WHEN ...) per column", "JOIN", "LIMIT"], 1, "Conditional aggregation."),
            Q("Median of an even number of rows is:", ["The lower middle", "The average of the two middle values", "The mean of all", "The mode"], 1, "That is why the query averages rows (cnt+1)/2 and (cnt+2)/2."),
            Q("Walking a hierarchy of unknown depth needs:", ["A self join per level", "A recursive CTE", "GROUP BY", "DISTINCT"], 1, "A recursive CTE handles any depth."),
        ], star=True, kw="interview classic running total consecutive streak gaps islands pivot median missing numbers cumulative recursive hierarchy swap"))

    return T
