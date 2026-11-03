# -*- coding: utf-8 -*-
"""
SQL syntax cheat sheet shown in SQL Lab (top bar: "syntax cheat"). MySQL first (that is what you write in the OA),
with the standard form where it is the same, and a short PostgreSQL / SQL Server note only where it differs.
Every item is [what it does, code]. Tables used in the examples: employees(id, name, dept_id, manager_id, salary,
hire_date, city), departments(id, name, budget).
"""

CHEAT = [

{"id": "skeleton", "title": "Query skeleton and order", "items": [
 ["Written order", """SELECT [DISTINCT] col, expr AS alias
FROM table t
[JOIN other o ON t.k = o.k]
WHERE row_filter
GROUP BY col
HAVING group_filter
ORDER BY col [ASC|DESC]
LIMIT n [OFFSET m];"""],
 ["Run order (why a SELECT alias fails in WHERE)", "FROM/JOIN -> WHERE -> GROUP BY -> HAVING -> window functions -> SELECT -> DISTINCT -> ORDER BY -> LIMIT\n-- MySQL lets you use a SELECT alias in GROUP BY, HAVING and ORDER BY, never in WHERE."],
 ["Comments", "-- one line\n# MySQL only, one line\n/* many\n   lines */"],
 ["Run several statements", "End every statement with a semicolon. In an OA, run the statement the question asks for, nothing else."],
]},

{"id": "where", "title": "Filtering (WHERE)", "items": [
 ["Comparison, AND/OR/NOT", "SELECT * FROM employees WHERE salary >= 50000 AND (city = 'Pune' OR city = 'Chennai') AND NOT dept_id = 3;\n-- <> and != both mean not equal. AND binds tighter than OR: use brackets."],
 ["BETWEEN (inclusive), IN", "WHERE salary BETWEEN 50000 AND 90000\nWHERE city IN ('Pune', 'Chennai')\nWHERE dept_id NOT IN (SELECT id FROM departments WHERE budget < 100000)   -- beware NULLs inside NOT IN"],
 ["LIKE: % any length, _ one character", "WHERE name LIKE 'A%'       -- starts with A\nWHERE name LIKE '%a'       -- ends with a\nWHERE name LIKE '_a%'      -- second letter a\nWHERE name LIKE '%50\\%%'   -- a literal %, escaped with \\"],
 ["Regex (MySQL)", "WHERE name REGEXP '^[AEIOU]'          -- starts with a vowel\nWHERE name REGEXP '[aeiou]$'          -- ends with a vowel\nWHERE name RLIKE 'son|sen'"],
 ["NULL tests (never = NULL)", "WHERE manager_id IS NULL\nWHERE manager_id IS NOT NULL\nWHERE manager_id <=> NULL       -- MySQL null-safe equals"],
 ["EXISTS", "WHERE EXISTS (SELECT 1 FROM employees e WHERE e.dept_id = d.id)"],
 ["Case sensitivity", "MySQL string comparison is case-insensitive by default (utf8mb4_0900_ai_ci).\nForce it: WHERE name = BINARY 'asha'    or    WHERE name COLLATE utf8mb4_bin = 'Asha'"],
]},

{"id": "sort", "title": "Sorting, limiting, DISTINCT", "items": [
 ["Sort", "ORDER BY salary DESC, name ASC;\nORDER BY 2 DESC;                     -- by the 2nd selected column\nORDER BY FIELD(city,'Pune','Delhi'); -- custom order (MySQL)\nORDER BY manager_id IS NULL, manager_id;   -- NULLs last in MySQL"],
 ["Top N and pagination", "SELECT * FROM employees ORDER BY salary DESC LIMIT 3;\nSELECT * FROM employees ORDER BY id LIMIT 3 OFFSET 6;     -- rows 7-9\nSELECT * FROM employees ORDER BY id LIMIT 6, 3;           -- same: LIMIT offset, count"],
 ["Always add ORDER BY", "Without ORDER BY the row order is not guaranteed. A checker that compares rows in order will fail a correct query."],
 ["Distinct", "SELECT DISTINCT city FROM employees;\nSELECT DISTINCT dept_id, city FROM employees;         -- distinct pairs\nSELECT COUNT(DISTINCT city) FROM employees;"],
 ["SQL Server / Oracle top N (for reference)", "-- SQL Server:  SELECT TOP 3 * FROM employees ORDER BY salary DESC;\n-- Standard:    ... ORDER BY salary DESC FETCH FIRST 3 ROWS ONLY;   (Postgres, Oracle 12c+, SQL Server with OFFSET 0 ROWS)"],
]},

{"id": "agg", "title": "Aggregates, GROUP BY, HAVING", "items": [
 ["Aggregate functions", "COUNT(*)            -- rows\nCOUNT(col)          -- non-NULL values\nCOUNT(DISTINCT col) -- distinct non-NULL values\nSUM(col)  AVG(col)  MIN(col)  MAX(col)      -- all ignore NULL"],
 ["Group and filter groups", "SELECT dept_id, COUNT(*) AS n, AVG(salary) AS avg_sal\nFROM employees\nWHERE city <> 'Delhi'          -- filters rows BEFORE grouping\nGROUP BY dept_id\nHAVING COUNT(*) >= 3           -- filters groups AFTER grouping\nORDER BY avg_sal DESC;"],
 ["Every non-aggregated SELECT column must be in GROUP BY", "SELECT dept_id, city, COUNT(*) FROM employees GROUP BY dept_id, city;"],
 ["Totals with ROLLUP", "SELECT dept_id, city, SUM(salary) FROM employees GROUP BY dept_id, city WITH ROLLUP;   -- MySQL spelling"],
 ["Join the values of a group", "SELECT dept_id, GROUP_CONCAT(name ORDER BY name SEPARATOR ', ') AS people FROM employees GROUP BY dept_id;"],
 ["Conditional counting", "SELECT dept_id,\n       SUM(city = 'Pune')                       AS in_pune,        -- MySQL: a comparison is 1 or 0\n       SUM(CASE WHEN salary > 90000 THEN 1 ELSE 0 END) AS high_paid\nFROM employees GROUP BY dept_id;"],
 ["Percent of total", "SELECT dept_id, SUM(salary) * 100.0 / (SELECT SUM(salary) FROM employees) AS pct FROM employees GROUP BY dept_id;"],
]},

{"id": "joins", "title": "Joins", "items": [
 ["INNER JOIN (only matches)", "SELECT e.name, d.name AS dept FROM employees e JOIN departments d ON d.id = e.dept_id;"],
 ["LEFT JOIN (all left rows)", "SELECT d.name, COUNT(e.id) AS staff          -- COUNT(e.id), not COUNT(*), so empty depts show 0\nFROM departments d LEFT JOIN employees e ON e.dept_id = d.id GROUP BY d.id, d.name;"],
 ["RIGHT JOIN", "SELECT e.name, d.name FROM employees e RIGHT JOIN departments d ON d.id = e.dept_id;"],
 ["FULL JOIN (MySQL has none: UNION a left and a right)", "SELECT e.name, d.name FROM employees e LEFT JOIN departments d ON d.id = e.dept_id\nUNION\nSELECT e.name, d.name FROM employees e RIGHT JOIN departments d ON d.id = e.dept_id;"],
 ["Anti join: rows with no match", "SELECT d.name FROM departments d LEFT JOIN employees e ON e.dept_id = d.id WHERE e.id IS NULL;\nSELECT d.name FROM departments d WHERE NOT EXISTS (SELECT 1 FROM employees e WHERE e.dept_id = d.id);"],
 ["Self join: employee and manager", "SELECT e.name AS employee, m.name AS manager FROM employees e LEFT JOIN employees m ON m.id = e.manager_id;"],
 ["Pairs without duplicates", "SELECT a.name, b.name FROM employees a JOIN employees b ON a.city = b.city AND a.id < b.id;"],
 ["CROSS JOIN", "SELECT d.name, c.city FROM departments d CROSS JOIN (SELECT DISTINCT city FROM employees) c;"],
 ["USING / NATURAL", "SELECT * FROM employees JOIN departments USING (id);   -- joins on a column with the same name\n-- SELECT * FROM a NATURAL JOIN b;                    -- avoid in real code"],
 ["Three tables", "SELECT e.name, p.name AS project, a.hours\nFROM employees e\nJOIN assignments a ON a.emp_id = e.id\nJOIN projects p    ON p.id = a.project_id;"],
 ["Put the filter in ON or WHERE?", "With a LEFT JOIN, a condition on the right table in WHERE turns it into an inner join. Put it in ON to keep the unmatched left rows."],
]},

{"id": "sub", "title": "Subqueries", "items": [
 ["Scalar subquery (one value)", "SELECT name FROM employees WHERE salary > (SELECT AVG(salary) FROM employees);"],
 ["IN", "SELECT name FROM employees WHERE dept_id IN (SELECT id FROM departments WHERE budget > 500000);"],
 ["Correlated subquery", "SELECT name, salary FROM employees e\nWHERE salary > (SELECT AVG(salary) FROM employees x WHERE x.dept_id = e.dept_id);   -- above their own dept average"],
 ["ANY / ALL", "WHERE salary > ALL (SELECT salary FROM employees WHERE dept_id = 2)\nWHERE salary > ANY (SELECT salary FROM employees WHERE dept_id = 2)"],
 ["Derived table (needs an alias)", "SELECT dept_id, avg_sal FROM (SELECT dept_id, AVG(salary) AS avg_sal FROM employees GROUP BY dept_id) t WHERE avg_sal > 60000;"],
 ["Subquery in SELECT", "SELECT d.name, (SELECT COUNT(*) FROM employees e WHERE e.dept_id = d.id) AS staff FROM departments d;"],
 ["MySQL cannot UPDATE/DELETE a table it selects from directly", "DELETE FROM employees WHERE id IN (SELECT id FROM (SELECT id FROM employees WHERE salary < 20000) t);   -- wrap in a derived table"],
]},

{"id": "setops", "title": "Set operations", "items": [
 ["UNION (removes duplicates) / UNION ALL (keeps them, faster)", "SELECT city FROM employees\nUNION\nSELECT city FROM customers;\n-- same number of columns, compatible types; ORDER BY once, at the very end"],
 ["INTERSECT / EXCEPT (MySQL 8.0.31+)", "SELECT city FROM employees WHERE dept_id = 1\nINTERSECT\nSELECT city FROM employees WHERE dept_id = 2;\n\nSELECT id FROM departments\nEXCEPT\nSELECT dept_id FROM employees;"],
 ["Older MySQL: without INTERSECT / EXCEPT", "SELECT DISTINCT city FROM employees WHERE dept_id = 1 AND city IN (SELECT city FROM employees WHERE dept_id = 2);   -- intersect\nSELECT d.id FROM departments d LEFT JOIN employees e ON e.dept_id = d.id WHERE e.id IS NULL;                        -- except"],
]},

{"id": "case", "title": "CASE, NULL handling", "items": [
 ["CASE", "SELECT name,\n  CASE WHEN salary >= 90000 THEN 'high'\n       WHEN salary >= 50000 THEN 'mid'\n       ELSE 'low' END AS band\nFROM employees;"],
 ["Simple CASE", "CASE dept_id WHEN 1 THEN 'Eng' WHEN 2 THEN 'Ops' ELSE 'Other' END"],
 ["COALESCE, IFNULL, NULLIF, IF", "COALESCE(a, b, 0)        -- first non-NULL\nIFNULL(a, 0)             -- MySQL, two arguments\nNULLIF(a, 0)             -- NULL when a = 0 (avoids divide by zero)\nIF(salary > 50000, 'Y', 'N')   -- MySQL only\nx / NULLIF(y, 0)"],
 ["Three-valued logic", "NULL = NULL is NULL (not true). NULL + 1 is NULL. AND/OR with NULL can be unknown.\nCOUNT(col) skips NULLs. NOT IN (..., NULL) never matches anything. ORDER BY puts NULLs first in ASC."],
]},

{"id": "string", "title": "String functions", "items": [
 ["Join", "CONCAT('Dr. ', name)           -- never use || in MySQL: it means OR\nCONCAT_WS(', ', city, state)     -- with a separator, skips NULLs"],
 ["Length", "CHAR_LENGTH(name)    -- characters\nLENGTH(name)         -- BYTES in MySQL (different for non-ASCII)"],
 ["Case, trim, pad", "UPPER(name)  LOWER(name)\nTRIM(name)  LTRIM(name)  RTRIM(name)  TRIM(BOTH 'x' FROM name)\nLPAD(id, 5, '0')    RPAD(name, 10, '.')"],
 ["Part of a string (positions start at 1)", "SUBSTRING(name, 2, 3)     -- 3 chars from position 2\nSUBSTRING(name, -3)       -- last 3\nLEFT(name, 2)   RIGHT(name, 2)\nSUBSTRING_INDEX(email, '@', 1)    -- before the first @\nSUBSTRING_INDEX(email, '@', -1)   -- after the last @"],
 ["Find, replace, repeat", "LOCATE('a', name)   INSTR(name, 'a')    -- 0 when absent\nREPLACE(name, 'a', '@')\nREVERSE(name)   REPEAT('ab', 3)\nFORMAT(1234567.891, 2)       -- '1,234,567.89'"],
 ["Compare / match", "STRCMP(a, b)             -- -1, 0, 1\nname LIKE 'A%'   name REGEXP '^A'\nREGEXP_REPLACE(name, '[0-9]', '')     -- MySQL 8"],
 ["Palindrome / vowel count tricks", "WHERE name = REVERSE(name)\nCHAR_LENGTH(name) - CHAR_LENGTH(REPLACE(LOWER(name), 'a', ''))   -- how many a's"],
]},

{"id": "num", "title": "Numeric functions", "items": [
 ["Rounding and powers", "ROUND(3.14159, 2)  ROUND(1234, -2)  CEIL(2.1)  FLOOR(2.9)  TRUNCATE(3.987, 1)\nABS(-5)  POWER(2, 10)  SQRT(16)  SIGN(-3)  MOD(10, 3)  10 % 3"],
 ["Division", "SELECT 7 / 2;     -- 3.5000 in MySQL\nSELECT 7 DIV 2;   -- 3  (integer division)\n-- PostgreSQL / SQL Server: 7 / 2 is 3 for integers, so write 7 / 2.0"],
 ["Others", "GREATEST(a, b, c)  LEAST(a, b, c)  RAND()   -- ORDER BY RAND() LIMIT 1 picks a random row\nCAST(x AS DECIMAL(10,2))   CAST('42' AS SIGNED)   CONVERT(x, UNSIGNED)"],
]},

{"id": "date", "title": "Date and time (MySQL)", "items": [
 ["Now", "NOW()  CURDATE()  CURTIME()  CURRENT_TIMESTAMP  UTC_TIMESTAMP()"],
 ["Parts", "YEAR(d)  MONTH(d)  DAY(d)  HOUR(t)  QUARTER(d)  WEEK(d)  DAYOFWEEK(d)   -- Sunday = 1\nDAYNAME(d)  MONTHNAME(d)  DAYOFYEAR(d)  LAST_DAY(d)  EXTRACT(YEAR FROM d)"],
 ["Add / subtract", "DATE_ADD(d, INTERVAL 7 DAY)    DATE_SUB(d, INTERVAL 1 MONTH)    d + INTERVAL 1 YEAR\n-- units: SECOND MINUTE HOUR DAY WEEK MONTH QUARTER YEAR"],
 ["Differences", "DATEDIFF(d1, d2)                 -- days, d1 - d2\nTIMESTAMPDIFF(MONTH, d1, d2)     -- whole units, d2 - d1\nTIMESTAMPDIFF(YEAR, birth_date, CURDATE())   -- age"],
 ["Format and parse", "DATE_FORMAT(d, '%Y-%m-%d')   DATE_FORMAT(d, '%d %b %Y')   DATE_FORMAT(d, '%W')\nSTR_TO_DATE('15-08-2026', '%d-%m-%Y')\n-- %Y 2026  %y 26  %m 08  %d 15  %b Aug  %M August  %H 24h  %i minutes  %s seconds  %W weekday"],
 ["Date types", "DATE (2026-10-28)  DATETIME  TIMESTAMP (auto-updating, time zone aware)  TIME  YEAR"],
 ["Common asks", "WHERE hire_date >= '2025-01-01' AND hire_date < '2026-01-01'          -- a year range (uses an index)\nWHERE YEAR(hire_date) = 2025                                 -- fine, but not index friendly\nGROUP BY YEAR(hire_date), MONTH(hire_date)\nWHERE hire_date >= CURDATE() - INTERVAL 30 DAY             -- last 30 days"],
]},

{"id": "window", "title": "Window functions (MySQL 8+)", "items": [
 ["Shape", "func() OVER (PARTITION BY group_col ORDER BY sort_col [frame])    -- keeps every row, adds a column"],
 ["Ranking", "ROW_NUMBER() OVER (ORDER BY salary DESC)   -- 1,2,3,4 unique\nRANK()       OVER (ORDER BY salary DESC)   -- 1,2,2,4 gaps after ties\nDENSE_RANK() OVER (ORDER BY salary DESC)   -- 1,2,2,3 no gaps\nNTILE(4)     OVER (ORDER BY salary)        -- quartile bucket"],
 ["Rank inside each group", "SELECT * FROM (\n  SELECT name, dept_id, salary, DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS r FROM employees\n) t WHERE r <= 2;                -- top 2 per department"],
 ["Look at neighbours", "LAG(salary, 1, 0) OVER (ORDER BY hire_date)    -- previous row (offset, default)\nLEAD(salary)       OVER (ORDER BY hire_date)    -- next row\nFIRST_VALUE(name) OVER (PARTITION BY dept_id ORDER BY salary DESC)\nLAST_VALUE(name)  OVER (PARTITION BY dept_id ORDER BY salary ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)"],
 ["Running and moving totals", "SUM(amount) OVER (ORDER BY d)                                    -- running total\nSUM(amount) OVER (ORDER BY d ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)   -- 3-row moving sum\nAVG(salary) OVER (PARTITION BY dept_id)                            -- per-group average on every row\nSUM(salary) OVER ()                                                -- grand total on every row"],
 ["Change from previous row", "SELECT yr, hires, hires - LAG(hires) OVER (ORDER BY yr) AS diff_from_prev FROM yearly;"],
 ["You cannot filter a window result in WHERE", "Wrap it: SELECT * FROM (SELECT ..., ROW_NUMBER() OVER (...) AS rn FROM t) x WHERE rn = 1;"],
]},

{"id": "cte", "title": "CTEs and recursion", "items": [
 ["WITH", "WITH dept_avg AS (SELECT dept_id, AVG(salary) AS avg_sal FROM employees GROUP BY dept_id)\nSELECT e.name FROM employees e JOIN dept_avg d ON d.dept_id = e.dept_id WHERE e.salary > d.avg_sal;"],
 ["Several CTEs", "WITH a AS (SELECT ...), b AS (SELECT ... FROM a) SELECT * FROM b;"],
 ["Recursive: management chain", "WITH RECURSIVE org AS (\n  SELECT id, name, manager_id, 0 AS depth, CAST(name AS CHAR(200)) AS path FROM employees WHERE manager_id IS NULL\n  UNION ALL\n  SELECT e.id, e.name, e.manager_id, o.depth + 1, CONCAT(o.path, ' > ', e.name)\n  FROM employees e JOIN org o ON e.manager_id = o.id\n)\nSELECT * FROM org ORDER BY path;"],
 ["Recursive: generate 1..10", "WITH RECURSIVE n AS (SELECT 1 AS x UNION ALL SELECT x + 1 FROM n WHERE x < 10) SELECT x FROM n;"],
]},

{"id": "dml", "title": "INSERT, UPDATE, DELETE", "items": [
 ["INSERT", "INSERT INTO employees (name, dept_id, salary) VALUES ('Asha', 2, 70000);\nINSERT INTO employees (name, dept_id, salary) VALUES ('A', 1, 10), ('B', 2, 20), ('C', 3, 30);   -- many rows\nINSERT INTO archive (id, name) SELECT id, name FROM employees WHERE salary < 20000;                -- from a query"],
 ["Insert or update (upsert)", "INSERT INTO stock (sku, qty) VALUES ('A1', 5)\nON DUPLICATE KEY UPDATE qty = qty + VALUES(qty);     -- needs a PRIMARY KEY or UNIQUE on sku\nINSERT IGNORE INTO stock (sku, qty) VALUES ('A1', 5);   -- skip rows that would fail\nREPLACE INTO stock (sku, qty) VALUES ('A1', 5);          -- delete then insert"],
 ["UPDATE", "UPDATE employees SET salary = salary * 1.10 WHERE dept_id = 3;\nUPDATE employees SET city = 'Pune', salary = salary + 500 WHERE id = 7;"],
 ["UPDATE with a join (MySQL)", "UPDATE employees e JOIN departments d ON d.id = e.dept_id\nSET e.salary = e.salary * 1.05 WHERE d.name = 'Data';"],
 ["UPDATE with CASE", "UPDATE employees SET grade = CASE WHEN salary > 90000 THEN 'A' WHEN salary > 50000 THEN 'B' ELSE 'C' END;"],
 ["Swap two values in one UPDATE", "UPDATE seat SET gender = CASE gender WHEN 'M' THEN 'F' ELSE 'M' END;"],
 ["DELETE", "DELETE FROM employees WHERE id = 7;\nDELETE FROM employees WHERE hire_date < '2015-01-01' ORDER BY id LIMIT 100;"],
 ["DELETE with a join", "DELETE e FROM employees e JOIN departments d ON d.id = e.dept_id WHERE d.name = 'Design';"],
 ["Delete duplicates, keep the smallest id", "DELETE e1 FROM person e1 JOIN person e2 ON e1.email = e2.email AND e1.id > e2.id;"],
 ["DELETE vs TRUNCATE vs DROP", "DELETE FROM t;      -- row by row, can have WHERE, can roll back, keeps AUTO_INCREMENT counter\nTRUNCATE TABLE t;    -- empties the table, resets the counter, DDL (cannot roll back in MySQL)\nDROP TABLE t;        -- removes the table itself\nDROP TABLE IF EXISTS t;"],
 ["No RETURNING in MySQL", "INSERT ...;  SELECT LAST_INSERT_ID();     -- id of the row just inserted\nSELECT ROW_COUNT();                      -- rows changed by the last statement"],
]},

{"id": "ddl", "title": "CREATE TABLE and data types", "items": [
 ["CREATE TABLE with the common constraints", "CREATE TABLE employees (\n  id         INT AUTO_INCREMENT PRIMARY KEY,\n  name       VARCHAR(50)  NOT NULL,\n  email      VARCHAR(100) UNIQUE,\n  dept_id    INT,\n  salary     DECIMAL(10,2) DEFAULT 0 CHECK (salary >= 0),\n  status     ENUM('active','left') DEFAULT 'active',\n  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\n  CONSTRAINT fk_dept FOREIGN KEY (dept_id) REFERENCES departments(id)\n      ON DELETE SET NULL ON UPDATE CASCADE\n);"],
 ["Composite keys", "CREATE TABLE assignments (\n  emp_id INT, project_id INT, hours INT,\n  PRIMARY KEY (emp_id, project_id),\n  FOREIGN KEY (emp_id) REFERENCES employees(id),\n  FOREIGN KEY (project_id) REFERENCES projects(id)\n);"],
 ["Foreign key actions", "ON DELETE CASCADE      -- delete the children too\nON DELETE SET NULL     -- keep children, clear the link\nON DELETE RESTRICT     -- refuse (default; same as NO ACTION in MySQL)\nON UPDATE CASCADE"],
 ["Copy a table", "CREATE TABLE emp_backup AS SELECT * FROM employees;        -- data, no keys\nCREATE TABLE emp_empty LIKE employees;                      -- structure and keys, no data\nCREATE TEMPORARY TABLE t AS SELECT ...;                     -- vanishes when the session ends"],
 ["Integer types", "TINYINT (1 byte)  SMALLINT  MEDIUMINT  INT (4 bytes)  BIGINT (8 bytes)    -- add UNSIGNED for no negatives\nBOOLEAN is TINYINT(1): TRUE = 1, FALSE = 0"],
 ["Decimal and float", "DECIMAL(10,2)   -- exact: 10 digits, 2 after the point. Use for money.\nFLOAT  DOUBLE   -- approximate"],
 ["Text types", "CHAR(10) fixed   VARCHAR(255) variable   TEXT (up to 64 KB)   MEDIUMTEXT   LONGTEXT\nENUM('a','b')   SET('x','y','z')    JSON    BLOB (binary)"],
 ["Date types", "DATE   DATETIME   TIMESTAMP   TIME   YEAR"],
 ["Auto numbering", "id INT AUTO_INCREMENT PRIMARY KEY          -- MySQL\n-- PostgreSQL: id SERIAL or id INT GENERATED ALWAYS AS IDENTITY     SQL Server: id INT IDENTITY(1,1)\nALTER TABLE t AUTO_INCREMENT = 1000;"],
 ["Generated column", "area DECIMAL(10,2) GENERATED ALWAYS AS (w * h) STORED"],
]},

{"id": "alter", "title": "ALTER, DROP, RENAME", "items": [
 ["Columns", "ALTER TABLE employees ADD COLUMN phone VARCHAR(15) AFTER name;\nALTER TABLE employees DROP COLUMN phone;\nALTER TABLE employees MODIFY COLUMN name VARCHAR(100) NOT NULL;     -- change the type\nALTER TABLE employees CHANGE COLUMN name full_name VARCHAR(100);     -- rename and retype\nALTER TABLE employees RENAME COLUMN city TO town;                    -- MySQL 8\nALTER TABLE employees ALTER COLUMN salary SET DEFAULT 0;"],
 ["Constraints", "ALTER TABLE employees ADD PRIMARY KEY (id);\nALTER TABLE employees DROP PRIMARY KEY;\nALTER TABLE employees ADD CONSTRAINT uq_email UNIQUE (email);\nALTER TABLE employees ADD CONSTRAINT fk_dept FOREIGN KEY (dept_id) REFERENCES departments(id);\nALTER TABLE employees DROP FOREIGN KEY fk_dept;\nALTER TABLE employees DROP INDEX uq_email;\nALTER TABLE employees ADD CONSTRAINT ck_sal CHECK (salary >= 0);"],
 ["Tables", "RENAME TABLE old_name TO new_name;      ALTER TABLE old_name RENAME TO new_name;\nDROP TABLE IF EXISTS t;       TRUNCATE TABLE t;"],
 ["Databases", "CREATE DATABASE shop;   USE shop;   DROP DATABASE shop;   SHOW DATABASES;"],
]},

{"id": "index", "title": "Indexes, views, EXPLAIN", "items": [
 ["Index", "CREATE INDEX idx_city ON employees (city);\nCREATE UNIQUE INDEX uq_email ON employees (email);\nCREATE INDEX idx_dept_sal ON employees (dept_id, salary);     -- composite: leftmost column first\nDROP INDEX idx_city ON employees;\nSHOW INDEX FROM employees;"],
 ["When an index is NOT used", "A function on the column (WHERE YEAR(d) = 2025), a leading wildcard (LIKE '%abc'), a type mismatch, OR across different columns, or a composite index used without its leftmost column."],
 ["View", "CREATE VIEW dept_pay AS SELECT dept_id, AVG(salary) AS avg_sal FROM employees GROUP BY dept_id;\nCREATE OR REPLACE VIEW dept_pay AS ...;     DROP VIEW dept_pay;\nSELECT * FROM dept_pay;"],
 ["See the plan", "EXPLAIN SELECT * FROM employees WHERE city = 'Pune';\nEXPLAIN ANALYZE SELECT ...;           -- MySQL 8: runs it and times it\n-- read: type (ALL = full scan, ref/range/const = index), key (index used), rows, Extra"],
]},

{"id": "txn", "title": "Transactions and locking", "items": [
 ["Basic", "START TRANSACTION;        -- or BEGIN;\n  UPDATE accounts SET bal = bal - 500 WHERE id = 1;\n  UPDATE accounts SET bal = bal + 500 WHERE id = 2;\nCOMMIT;                    -- make it permanent\n-- ROLLBACK;               -- undo everything since START"],
 ["Savepoint", "SAVEPOINT sp1;\n  ...\nROLLBACK TO SAVEPOINT sp1;\nRELEASE SAVEPOINT sp1;"],
 ["Autocommit", "SET autocommit = 0;      -- MySQL commits every statement by default (autocommit = 1)"],
 ["Isolation levels (weakest to strongest)", "SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;   -- dirty reads possible\nSET TRANSACTION ISOLATION LEVEL READ COMMITTED;     -- no dirty reads\nSET TRANSACTION ISOLATION LEVEL REPEATABLE READ;    -- MySQL default; no non-repeatable reads\nSET TRANSACTION ISOLATION LEVEL SERIALIZABLE;       -- no phantoms"],
 ["Row locks", "SELECT * FROM accounts WHERE id = 1 FOR UPDATE;          -- exclusive lock on the rows read\nSELECT * FROM accounts WHERE id = 1 FOR SHARE;           -- shared lock\nSELECT ... FOR UPDATE SKIP LOCKED;                         -- take only unlocked rows (queues)\nLOCK TABLES t WRITE;  UNLOCK TABLES;"],
 ["ACID", "Atomicity (all or nothing)  Consistency (rules hold)  Isolation (transactions do not see each other half done)  Durability (committed data survives a crash)"],
 ["Problems and which level stops them", "Dirty read: RU allows.  Non-repeatable read: RC allows.  Phantom read: RR (standard) allows, MySQL InnoDB mostly stops it.  Serializable stops all."],
]},

{"id": "prog", "title": "Procedures, functions, triggers, cursors", "items": [
 ["Stored procedure", "DELIMITER $$\nCREATE PROCEDURE raise_salary (IN p_dept INT, IN p_pct DECIMAL(5,2), OUT p_rows INT)\nBEGIN\n  UPDATE employees SET salary = salary * (1 + p_pct / 100) WHERE dept_id = p_dept;\n  SET p_rows = ROW_COUNT();\nEND$$\nDELIMITER ;\nCALL raise_salary(3, 10, @n);   SELECT @n;"],
 ["Stored function", "DELIMITER $$\nCREATE FUNCTION annual (m DECIMAL(10,2)) RETURNS DECIMAL(12,2) DETERMINISTIC\nBEGIN\n  RETURN m * 12;\nEND$$\nDELIMITER ;\nSELECT name, annual(salary) FROM employees;"],
 ["Variables and control flow", "DECLARE total INT DEFAULT 0;    SET total = total + 1;    SET @session_var = 5;\nIF x > 0 THEN ... ELSEIF x = 0 THEN ... ELSE ... END IF;\nCASE WHEN ... THEN ... END CASE;\nWHILE i < 10 DO ... SET i = i + 1; END WHILE;       LOOP ... LEAVE label; END LOOP;"],
 ["Trigger (BEFORE/AFTER, INSERT/UPDATE/DELETE, row level)", "DELIMITER $$\nCREATE TRIGGER trg_salary_audit AFTER UPDATE ON employees\nFOR EACH ROW\nBEGIN\n  IF OLD.salary <> NEW.salary THEN\n    INSERT INTO salary_audit (emp_id, old_salary, new_salary) VALUES (OLD.id, OLD.salary, NEW.salary);\n  END IF;\nEND$$\nDELIMITER ;\nDROP TRIGGER trg_salary_audit;   SHOW TRIGGERS;"],
 ["Stop a bad insert with a trigger", "CREATE TRIGGER trg_floor BEFORE INSERT ON employees FOR EACH ROW\nBEGIN\n  IF NEW.salary < 20000 THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'salary below minimum'; END IF;\nEND;"],
 ["OLD and NEW", "INSERT: NEW only.   UPDATE: OLD and NEW.   DELETE: OLD only.   BEFORE triggers may change NEW values."],
 ["Cursor", "DECLARE done INT DEFAULT 0;  DECLARE v_name VARCHAR(50);\nDECLARE cur CURSOR FOR SELECT name FROM employees;\nDECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;\nOPEN cur;\nloop1: LOOP\n  FETCH cur INTO v_name;\n  IF done = 1 THEN LEAVE loop1; END IF;\n  -- use v_name\nEND LOOP;\nCLOSE cur;"],
 ["Prepared statement (dynamic SQL)", "SET @sql = CONCAT('SELECT * FROM ', 'employees', ' WHERE id = ?');\nPREPARE stmt FROM @sql;   SET @id = 3;   EXECUTE stmt USING @id;   DEALLOCATE PREPARE stmt;"],
 ["Error handling", "DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK; END;"],
 ["Event (scheduled job)", "CREATE EVENT purge_old ON SCHEDULE EVERY 1 DAY DO DELETE FROM logs WHERE created_at < NOW() - INTERVAL 90 DAY;"],
]},

{"id": "dcl", "title": "Users and permissions", "items": [
 ["Users", "CREATE USER 'analyst'@'localhost' IDENTIFIED BY 'Str0ng#pass';\nDROP USER 'analyst'@'localhost';"],
 ["Grant and revoke", "GRANT SELECT, INSERT ON shop.* TO 'analyst'@'localhost';\nGRANT ALL PRIVILEGES ON shop.* TO 'admin'@'localhost' WITH GRANT OPTION;\nREVOKE INSERT ON shop.* FROM 'analyst'@'localhost';\nSHOW GRANTS FOR 'analyst'@'localhost';\nFLUSH PRIVILEGES;"],
 ["Roles (MySQL 8)", "CREATE ROLE reader;  GRANT SELECT ON shop.* TO reader;  GRANT reader TO 'analyst'@'localhost';"],
 ["The four sub-languages", "DDL: CREATE ALTER DROP TRUNCATE RENAME     DML: INSERT UPDATE DELETE (and SELECT)\nDCL: GRANT REVOKE                           TCL: COMMIT ROLLBACK SAVEPOINT"],
]},

{"id": "meta", "title": "Looking around the database", "items": [
 ["Quick look", "SHOW DATABASES;   USE shop;   SHOW TABLES;   DESCRIBE employees;   -- or DESC employees;\nSHOW CREATE TABLE employees;   SHOW COLUMNS FROM employees;   SHOW INDEX FROM employees;"],
 ["information_schema", "SELECT table_name FROM information_schema.tables WHERE table_schema = DATABASE();\nSELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name = 'employees';\nSELECT constraint_name, table_name, referenced_table_name FROM information_schema.key_column_usage WHERE referenced_table_name IS NOT NULL;"],
 ["Handy", "SELECT DATABASE(), USER(), VERSION();   SELECT @@sql_mode;   SELECT @@transaction_isolation;"],
]},

{"id": "recipes", "title": "Classic interview queries", "items": [
 ["2nd highest salary", "SELECT MAX(salary) FROM employees WHERE salary < (SELECT MAX(salary) FROM employees);\nSELECT DISTINCT salary FROM employees ORDER BY salary DESC LIMIT 1 OFFSET 1;"],
 ["Nth highest salary (N = 3)", "SELECT salary FROM (SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS r FROM employees) t WHERE r = 3 GROUP BY salary;"],
 ["Highest salary in each department", "SELECT e.* FROM employees e JOIN (SELECT dept_id, MAX(salary) m FROM employees GROUP BY dept_id) x ON x.dept_id = e.dept_id AND x.m = e.salary;"],
 ["Top 2 per department", "SELECT * FROM (SELECT *, DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS r FROM employees) t WHERE r <= 2;"],
 ["Find duplicates", "SELECT email, COUNT(*) FROM person GROUP BY email HAVING COUNT(*) > 1;"],
 ["Employees earning more than their manager", "SELECT e.name FROM employees e JOIN employees m ON m.id = e.manager_id WHERE e.salary > m.salary;"],
 ["Departments with no employees", "SELECT d.name FROM departments d LEFT JOIN employees e ON e.dept_id = d.id WHERE e.id IS NULL;"],
 ["Customers who never ordered", "SELECT c.name FROM customers c WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);"],
 ["Running total", "SELECT sale_date, amount, SUM(amount) OVER (ORDER BY sale_date) AS running FROM sales;"],
 ["Month-over-month change", "SELECT m, total, total - LAG(total) OVER (ORDER BY m) AS change_vs_prev FROM (SELECT DATE_FORMAT(sale_date,'%Y-%m') AS m, SUM(amount) AS total FROM sales GROUP BY DATE_FORMAT(sale_date,'%Y-%m')) t;"],
 ["Median salary", "SELECT AVG(salary) FROM (SELECT salary, ROW_NUMBER() OVER (ORDER BY salary) AS rn, COUNT(*) OVER () AS c FROM employees) t WHERE rn IN (FLOOR((c + 1) / 2), CEIL((c + 1) / 2));"],
 ["Pivot with CASE", "SELECT dept_id,\n  SUM(CASE WHEN city = 'Pune'    THEN 1 ELSE 0 END) AS pune,\n  SUM(CASE WHEN city = 'Chennai' THEN 1 ELSE 0 END) AS chennai\nFROM employees GROUP BY dept_id;"],
 ["Consecutive days (gaps and islands)", "WITH x AS (\n  SELECT emp_id, login_date, DATE_SUB(login_date, INTERVAL ROW_NUMBER() OVER (PARTITION BY emp_id ORDER BY login_date) DAY) AS grp FROM logins\n)\nSELECT emp_id, COUNT(*) AS streak, MIN(login_date) AS from_date, MAX(login_date) AS to_date FROM x GROUP BY emp_id, grp ORDER BY streak DESC;"],
 ["Employees hired in the last 6 months", "SELECT name FROM employees WHERE hire_date >= CURDATE() - INTERVAL 6 MONTH;"],
 ["Percentage of total", "SELECT name, salary, ROUND(salary * 100.0 / SUM(salary) OVER (), 2) AS pct FROM employees;"],
 ["Cumulative count of rows meeting a condition", "SELECT SUM(salary > 50000) FROM employees;     -- MySQL: true counts as 1"],
 ["Swap adjacent seats", "SELECT CASE WHEN id % 2 = 1 AND id < (SELECT MAX(id) FROM seat) THEN id + 1 WHEN id % 2 = 0 THEN id - 1 ELSE id END AS id, student FROM seat ORDER BY id;"],
 ["Rows to a comma list", "SELECT dept_id, GROUP_CONCAT(name ORDER BY name SEPARATOR ',') FROM employees GROUP BY dept_id;"],
 ["Odd or even id rows", "SELECT * FROM employees WHERE id % 2 = 1;   SELECT * FROM employees WHERE MOD(id, 2) = 0;"],
 ["Last row / first row", "SELECT * FROM employees ORDER BY id DESC LIMIT 1;   SELECT * FROM employees ORDER BY id LIMIT 1;"],
 ["Names that start and end with a vowel", "SELECT DISTINCT city FROM station WHERE city REGEXP '^[aeiou].*[aeiou]$';"],
]},

{"id": "oa", "title": "OA checklist (queries right but test fails)", "items": [
 ["Before you write", "1. Look at the engine in the language box.  2. Read the output columns and their exact names.  3. Note the required order."],
 ["Output must match", "Use AS to name every column exactly as the problem shows.  Add ORDER BY even if the problem does not say.  Round exactly as asked: ROUND(x, 2)."],
 ["Division", "Make one side decimal: x * 1.0 / y or x / y.  MySQL already returns decimals; PostgreSQL and SQL Server truncate integers."],
 ["NULL traps", "= NULL never matches: use IS NULL.  COUNT(col) skips NULLs.  NOT IN with a NULL in the list returns nothing: use NOT EXISTS.  SUM of no rows is NULL: COALESCE(SUM(x), 0)."],
 ["Strings and case", "Use CONCAT, never ||.  LIKE is case-insensitive in MySQL.  CHAR_LENGTH counts characters."],
 ["Dates", "Compare with ranges (>= start AND < next_start) rather than wrapping the column in YEAR().  DATEDIFF gives days."],
 ["Ties", "Top N with ties: DENSE_RANK or RANK.  Exactly N rows: ROW_NUMBER or LIMIT."],
 ["Semicolons and quotes", "Single quotes for strings, backticks for names that clash with keywords (`order`, `rank`, `change`, `group`).  Double quotes are strings in default MySQL."],
 ["Reserved words used as names", "order, group, rank, key, index, desc, change, date (fine but risky), value, row.  Alias them or use backticks."],
]},

{"id": "diff", "title": "MySQL vs PostgreSQL vs SQL Server (when you must switch)", "items": [
 ["First N rows", "MySQL / PostgreSQL / SQLite:  LIMIT n          SQL Server:  SELECT TOP n          Standard:  FETCH FIRST n ROWS ONLY"],
 ["Join strings", "MySQL: CONCAT(a, b)       PostgreSQL: a || b  (or CONCAT)       SQL Server: a + b  (or CONCAT)"],
 ["NULL default", "MySQL: IFNULL(x, 0)       PostgreSQL / standard: COALESCE(x, 0)       SQL Server: ISNULL(x, 0)"],
 ["Today", "MySQL: CURDATE() NOW()       PostgreSQL: CURRENT_DATE NOW()       SQL Server: GETDATE()"],
 ["Year of a date", "MySQL: YEAR(d)       PostgreSQL: EXTRACT(YEAR FROM d)       SQL Server: YEAR(d)"],
 ["Add days", "MySQL: DATE_ADD(d, INTERVAL 7 DAY)       PostgreSQL: d + INTERVAL '7 days'       SQL Server: DATEADD(day, 7, d)"],
 ["Days between", "MySQL: DATEDIFF(a, b)       PostgreSQL: a - b       SQL Server: DATEDIFF(day, b, a)"],
 ["String length", "MySQL: CHAR_LENGTH(s)       PostgreSQL: LENGTH(s)       SQL Server: LEN(s)"],
 ["Auto id", "MySQL: AUTO_INCREMENT       PostgreSQL: SERIAL or IDENTITY       SQL Server: IDENTITY(1,1)"],
 ["Get the new id", "MySQL: LAST_INSERT_ID()       PostgreSQL: INSERT ... RETURNING id       SQL Server: SCOPE_IDENTITY() or OUTPUT"],
 ["Join strings of a group", "MySQL: GROUP_CONCAT(x SEPARATOR ',')       PostgreSQL / SQL Server 2017+: STRING_AGG(x, ',')"],
 ["Upsert", "MySQL: ON DUPLICATE KEY UPDATE       PostgreSQL: ON CONFLICT (k) DO UPDATE       SQL Server: MERGE"],
 ["Full outer join", "MySQL: not supported (UNION a LEFT and a RIGHT)       PostgreSQL / SQL Server: FULL OUTER JOIN"],
 ["Case-insensitive match", "MySQL: LIKE is already case-insensitive       PostgreSQL: ILIKE       SQL Server: depends on the collation"],
 ["Quoting names", "MySQL: `name`       PostgreSQL: \"name\"       SQL Server: [name] or \"name\""],
 ["Boolean", "MySQL: TINYINT(1), TRUE=1       PostgreSQL: real BOOLEAN       SQL Server: BIT"],
 ["Window functions", "MySQL 8.0+, PostgreSQL, SQL Server 2012+ all support them. MySQL 5.7 does not."],
]},

]


# ----------------------------------------------------------------------------------------------------------------
#  The demo database behind the Run buttons: the company tables + the shop tables (already in SQL Lab) + these extras.
# ----------------------------------------------------------------------------------------------------------------
EXTRA_SQL = """
CREATE TABLE person (id INTEGER PRIMARY KEY, email TEXT);
INSERT INTO person VALUES (1,'a@x.com'),(2,'b@x.com'),(3,'a@x.com'),(4,'c@x.com'),(5,'b@x.com');
CREATE TABLE seat (id INTEGER PRIMARY KEY, student TEXT);
INSERT INTO seat VALUES (1,'Asha'),(2,'Bharat'),(3,'Chitra'),(4,'Deepak'),(5,'Esha');
CREATE TABLE accounts (id INTEGER PRIMARY KEY, holder TEXT, bal INTEGER);
INSERT INTO accounts VALUES (1,'Asha',5000),(2,'Rohan',3000);
CREATE TABLE stock (sku TEXT PRIMARY KEY, qty INTEGER);
INSERT INTO stock VALUES ('A1',5),('B2',0);
CREATE TABLE yearly (yr INTEGER, hires INTEGER);
INSERT INTO yearly VALUES (2022,3),(2023,5),(2024,4),(2025,7);
CREATE TABLE station (id INTEGER PRIMARY KEY, city TEXT);
INSERT INTO station VALUES (1,'Amritsar'),(2,'Indore'),(3,'Aligarh'),(4,'Pune'),(5,'Orai'),(6,'Delhi');
CREATE TABLE sales (id INTEGER PRIMARY KEY, sale_date TEXT, region TEXT, amount INTEGER);
INSERT INTO sales VALUES (1,'2025-01-05','North',1200),(2,'2025-01-20','South',800),(3,'2025-02-03','North',1500),
 (4,'2025-02-18','South',950),(5,'2025-03-02','North',700),(6,'2025-03-25','South',1800),(7,'2025-04-09','North',2100);
"""
EXTRA_TABLES = ["person", "seat", "accounts", "stock", "yearly", "station", "sales"]



# ----------------------------------------------------------------------------------------------------------------
#  SYN: the general form of a statement, shown above the example.   TRY: a version that runs on the SQLite demo
#  (used when the MySQL spelling cannot run there). Keys are the item labels.
# ----------------------------------------------------------------------------------------------------------------
SYN = {
 "Comparison, AND/OR/NOT": "SELECT columns FROM table WHERE condition [AND|OR condition ...];",
 "BETWEEN (inclusive), IN": "WHERE col BETWEEN low AND high      WHERE col [NOT] IN (value, value, ...)",
 "LIKE: % any length, _ one character": "WHERE col [NOT] LIKE 'pattern'        -- % = any number of characters, _ = exactly one",
 "NULL tests (never = NULL)": "WHERE col IS [NOT] NULL",
 "Sort": "ORDER BY col1 [ASC|DESC], col2 [ASC|DESC], ...",
 "Top N and pagination": "SELECT ... ORDER BY col [DESC] LIMIT count [OFFSET skip];",
 "Distinct": "SELECT DISTINCT col1, col2 FROM table;",
 "Group and filter groups": "SELECT group_col, AGG(col) FROM table [WHERE row_filter] GROUP BY group_col [HAVING group_filter] [ORDER BY ...];",
 "INNER JOIN (only matches)": "SELECT cols FROM a [INNER] JOIN b ON a.key = b.key;",
 "LEFT JOIN (all left rows)": "SELECT cols FROM a LEFT [OUTER] JOIN b ON a.key = b.key;      -- unmatched b columns are NULL",
 "Self join: employee and manager": "SELECT x.col, y.col FROM t x JOIN t y ON x.fk = y.pk;        -- the same table twice, two aliases",
 "Scalar subquery (one value)": "SELECT cols FROM t WHERE col > (SELECT AGG(col) FROM t);",
 "IN": "SELECT cols FROM t WHERE col IN (SELECT col FROM other WHERE ...);",
 "Correlated subquery": "SELECT cols FROM t o WHERE col > (SELECT AGG(col) FROM t i WHERE i.group = o.group);",
 "UNION (removes duplicates) / UNION ALL (keeps them, faster)": "SELECT ... UNION [ALL] SELECT ...;      -- same number and types of columns",
 "CASE": "CASE WHEN condition THEN result [WHEN ... THEN ...] [ELSE result] END",
 "COALESCE, IFNULL, NULLIF, IF": "COALESCE(a, b, ...)   IFNULL(a, b)   NULLIF(a, b)   IF(condition, then, else)",
 "Shape": "function() OVER ([PARTITION BY cols] [ORDER BY cols] [ROWS BETWEEN ... AND ...])",
 "WITH": "WITH name AS (SELECT ...) [, name2 AS (SELECT ...)] SELECT ... FROM name;",
 "INSERT": "INSERT INTO table (col1, col2) VALUES (v1, v2) [, (v1, v2) ...];\nINSERT INTO table (cols) SELECT ... ;",
 "UPDATE": "UPDATE table SET col = value [, col = value ...] [WHERE condition];",
 "DELETE": "DELETE FROM table [WHERE condition];",
 "CREATE TABLE with the common constraints": "CREATE TABLE name (col type [constraints], ..., [PRIMARY KEY (...)], [FOREIGN KEY (col) REFERENCES t(col) [ON DELETE action]]);",
 "Index": "CREATE [UNIQUE] INDEX name ON table (col1 [, col2]);",
 "View": "CREATE VIEW name AS SELECT ...;",
 "Basic": "START TRANSACTION; statements; COMMIT | ROLLBACK;",
 "Stored procedure": "CREATE PROCEDURE name ([IN|OUT|INOUT] param type, ...) BEGIN ... END;     CALL name(args);",
 "Trigger (BEFORE/AFTER, INSERT/UPDATE/DELETE, row level)": "CREATE TRIGGER name {BEFORE|AFTER} {INSERT|UPDATE|DELETE} ON table FOR EACH ROW BEGIN ... END;",
 "Grant and revoke": "GRANT privilege [, privilege] ON db.table TO 'user'@'host';    REVOKE privilege ON db.table FROM 'user'@'host';",
}

TRY = {
 "Join the values of a group": "SELECT dept_id, GROUP_CONCAT(name, ', ') AS people FROM employees GROUP BY dept_id;",
 "Totals with ROLLUP": "SELECT dept_id, SUM(salary) AS total FROM employees GROUP BY dept_id\nUNION ALL\nSELECT NULL, SUM(salary) FROM employees;",
 "Put the filter in ON or WHERE?": "SELECT d.name, COUNT(e.id) AS pune_staff\nFROM departments d LEFT JOIN employees e ON e.dept_id = d.id AND e.city = 'Pune'\nGROUP BY d.id, d.name;",
 "INSERT": "CREATE TABLE archive (id INTEGER, name TEXT);\nINSERT INTO archive (id, name) SELECT id, name FROM employees WHERE salary < 100000;\nSELECT * FROM archive;",
 "UPDATE with a join (MySQL)": "UPDATE employees SET salary = salary * 1.05 WHERE dept_id = (SELECT id FROM departments WHERE name = 'Data');\nSELECT name, dept_id, salary FROM employees WHERE dept_id = 2;",
 "UPDATE with CASE": "ALTER TABLE employees ADD COLUMN grade TEXT;\nUPDATE employees SET grade = CASE WHEN salary > 90000 THEN 'A' WHEN salary > 50000 THEN 'B' ELSE 'C' END;\nSELECT name, salary, grade FROM employees;",
 "DELETE": "DELETE FROM employees WHERE id = 7;\nSELECT id, name FROM employees ORDER BY id;",
 "DELETE with a join": "DELETE FROM employees WHERE dept_id = (SELECT id FROM departments WHERE name = 'Design');\nSELECT id, name, dept_id FROM employees;",
 "Delete duplicates, keep the smallest id": "DELETE FROM person WHERE id NOT IN (SELECT MIN(id) FROM person GROUP BY email);\nSELECT * FROM person;",
 "Swap two values in one UPDATE": "UPDATE seat SET student = CASE id WHEN 1 THEN 'Bharat' WHEN 2 THEN 'Asha' ELSE student END;\nSELECT * FROM seat;",
 "Consecutive days (gaps and islands)": "WITH x AS (\n  SELECT emp_id, login_date,\n         date(login_date, '-' || ROW_NUMBER() OVER (PARTITION BY emp_id ORDER BY login_date) || ' day') AS grp\n  FROM logins\n)\nSELECT emp_id, COUNT(*) AS streak, MIN(login_date) AS from_date, MAX(login_date) AS to_date\nFROM x GROUP BY emp_id, grp ORDER BY streak DESC;",
 "Employees hired in the last 6 months": "SELECT name, hire_date FROM employees WHERE hire_date >= date('now', '-6 months');   -- none: nobody was hired recently",
 "Rows to a comma list": "SELECT dept_id, GROUP_CONCAT(name, ',') AS people FROM employees GROUP BY dept_id;",
 "Odd or even id rows": "SELECT * FROM employees WHERE id % 2 = 1;",
 "Last row / first row": "SELECT * FROM employees ORDER BY id DESC LIMIT 1;",
 "Month-over-month change": "SELECT m, total, total - LAG(total) OVER (ORDER BY m) AS change_vs_prev FROM (SELECT strftime('%Y-%m', sale_date) AS m, SUM(amount) AS total FROM sales GROUP BY m) t;",
 "Date types": "",
}

TRY.update({
 "BETWEEN (inclusive), IN": "SELECT name, salary, city FROM employees\nWHERE salary BETWEEN 90000 AND 130000 AND city IN ('Bengaluru', 'Hyderabad');",
 "LIKE: % any length, _ one character": "SELECT name FROM employees WHERE name LIKE 'A%' OR name LIKE '%a' OR name LIKE '_e%';",
 "Regex (MySQL)": "SELECT name FROM employees WHERE name REGEXP '^[AEIOU]';",
 "NULL tests (never = NULL)": "SELECT name, manager_id FROM employees WHERE manager_id IS NULL;",
 "EXISTS": "SELECT d.name FROM departments d WHERE EXISTS (SELECT 1 FROM employees e WHERE e.dept_id = d.id);",
 "Sort": "SELECT name, city, salary FROM employees ORDER BY city ASC, salary DESC;",
 "Aggregate functions": "SELECT COUNT(*) AS rows_, COUNT(manager_id) AS with_manager, COUNT(DISTINCT city) AS cities, SUM(salary) AS total, ROUND(AVG(salary)) AS avg_sal, MIN(salary) AS lo, MAX(salary) AS hi FROM employees;",
 "ANY / ALL": "SELECT name, salary FROM employees WHERE salary > (SELECT MAX(salary) FROM employees WHERE dept_id = 2);      -- same meaning as > ALL (...); SQLite has no ALL, MySQL does",
 "Simple CASE": "SELECT name, CASE dept_id WHEN 1 THEN 'Eng' WHEN 2 THEN 'Data' WHEN 3 THEN 'Platform' ELSE 'Other' END AS dept FROM employees;",
 "COALESCE, IFNULL, NULLIF, IF": "SELECT name, manager_id, COALESCE(manager_id, 0) AS mgr_or_zero, IFNULL(manager_id, -1) AS mgr_or_minus1, NULLIF(dept_id, 1) AS dept_not_1 FROM employees;",
 "Join": "SELECT name, city, CONCAT('Dr. ', name) AS title, CONCAT(name, ' (', city, ')') AS label FROM employees LIMIT 5;",
 "Length": "SELECT name, CHAR_LENGTH(name) AS chars FROM employees ORDER BY chars DESC;",
 "Case, trim, pad": "SELECT UPPER(name) AS up, LOWER(city) AS low, TRIM('  hi  ') AS trimmed FROM employees LIMIT 4;",
 "Part of a string (positions start at 1)": "SELECT name, SUBSTRING(name, 2, 3) AS mid3, LEFT(name, 2) AS first2, RIGHT(name, 2) AS last2 FROM employees;",
 "Find, replace, repeat": "SELECT name, REPLACE(name, 'a', '@') AS swapped, INSTR(name, 'a') AS pos_of_a FROM employees;",
 "Palindrome / vowel count tricks": "SELECT name, CHAR_LENGTH(name) - CHAR_LENGTH(REPLACE(LOWER(name), 'a', '')) AS a_count FROM employees;",
 "Rounding and powers": "SELECT ROUND(3.14159, 2) AS r, ABS(-5) AS a, 10 % 3 AS m, 2 * 2 * 2 AS cube;",
 "Others": "SELECT MAX(salary, 100000) AS at_least_100k, MIN(salary, 100000) AS at_most_100k FROM employees;",
 "Now": "SELECT CURDATE() AS today, NOW() AS now_ts;",
 "Parts": "SELECT name, hire_date, YEAR(hire_date) AS y, MONTH(hire_date) AS m, DAY(hire_date) AS d FROM employees LIMIT 5;",
 "Differences": "SELECT name, hire_date, DATEDIFF(CURDATE(), hire_date) AS days_employed FROM employees ORDER BY days_employed DESC LIMIT 5;",
 "Format and parse": "SELECT name, hire_date, DATE_FORMAT(hire_date, '%d/%m/%Y') AS indian_style, DATE_FORMAT(hire_date, '%Y-%m') AS ym FROM employees LIMIT 5;",
 "Common asks": "SELECT name, hire_date FROM employees WHERE hire_date >= '2020-01-01' AND hire_date < '2021-01-01';",
 "Ranking": "SELECT name, salary,\n  ROW_NUMBER() OVER (ORDER BY salary DESC) AS row_no,\n  RANK() OVER (ORDER BY salary DESC) AS rnk,\n  DENSE_RANK() OVER (ORDER BY salary DESC) AS dense\nFROM employees;",
 "Look at neighbours": "SELECT name, hire_date, salary, LAG(salary) OVER (ORDER BY hire_date) AS prev_salary, LEAD(salary) OVER (ORDER BY hire_date) AS next_salary FROM employees;",
 "Running and moving totals": "SELECT sale_date, amount, SUM(amount) OVER (ORDER BY sale_date) AS running, AVG(amount) OVER (ORDER BY sale_date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS moving_avg FROM sales;",
 "You cannot filter a window result in WHERE": "SELECT * FROM (SELECT name, dept_id, salary, ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rn FROM employees) x WHERE rn = 1;",
 "Several CTEs": "WITH a AS (SELECT dept_id, SUM(salary) AS total FROM employees GROUP BY dept_id),\n     b AS (SELECT dept_id, total, total * 100.0 / (SELECT SUM(total) FROM a) AS pct FROM a)\nSELECT * FROM b ORDER BY pct DESC;",
 "Insert or update (upsert)": "INSERT INTO stock (sku, qty) VALUES ('A1', 5)\nON CONFLICT (sku) DO UPDATE SET qty = qty + excluded.qty;\nSELECT * FROM stock;      -- SQLite / PostgreSQL spelling; MySQL uses ON DUPLICATE KEY UPDATE",
 "No RETURNING in MySQL": "INSERT INTO stock (sku, qty) VALUES ('C3', 1);\nSELECT * FROM stock WHERE sku = 'C3';      -- read the row back, as MySQL has no RETURNING",
})


# ----------------------------------------------------------------------------------------------------------------
#  annotate(): decide, at build time, which items can really run on the demo database, and emit dicts for the page.
#  The Python mirror below registers the same MySQL-flavoured functions the page adds to its SQLite.
# ----------------------------------------------------------------------------------------------------------------
def annotate(seed_sql, shop_sql):
    import datetime, re, sqlite3

    def mk():
        con = sqlite3.connect(":memory:")
        d = lambda x: (datetime.date.fromisoformat(str(x)[:10]) if x else None)
        def safe(fn):
            def w(*a):
                try: return fn(*a)
                except Exception: return None
            return w
        f = con.create_function
        f("YEAR", 1, safe(lambda x: d(x).year)); f("MONTH", 1, safe(lambda x: d(x).month)); f("DAY", 1, safe(lambda x: d(x).day))
        f("CURDATE", 0, lambda: str(datetime.date.today())); f("NOW", 0, lambda: str(datetime.datetime.now())[:19])
        f("DATEDIFF", 2, safe(lambda a, b: (d(a) - d(b)).days)); f("CHAR_LENGTH", 1, lambda x: None if x is None else len(str(x)))
        f("LEFT", 2, lambda s, n: None if s is None else str(s)[:n]); f("RIGHT", 2, lambda s, n: None if s is None else str(s)[-n:])
        f("CONCAT", -1, lambda *a: None if any(x is None for x in a) else "".join(map(str, a)))
        f("DATE_FORMAT", 2, safe(lambda x, fmt: d(x).strftime(fmt.replace("%i", "%M").replace("%b", "%b"))))
        f("REGEXP", 2, lambda p, s: 1 if s is not None and re.search(p, str(s), re.I) else 0)
        con.executescript(seed_sql); con.executescript(shop_sql); con.executescript(EXTRA_SQL)
        return con

    def runs(code):
        stmts = [x.strip() for x in re.split(r";\s*(?:\n|$)", re.sub(r"--[^\n]*", "", code)) if x.strip()]
        if not stmts or "..." in code:
            return False
        con = mk()
        try:
            for x in stmts:
                if not re.match(r"(SELECT|WITH|INSERT|UPDATE|DELETE|CREATE|ALTER|DROP|REPLACE)\b", x, re.I):
                    return False
                con.execute(x).fetchall()
            return True
        except Exception:
            return False

    out, nrun, ntry = [], 0, 0
    for sec in CHEAT:
        items = []
        for lab, code in sec["items"]:
            rc = runs(code)
            t = TRY.get(lab, "")
            rt = bool(t) and runs(t)
            nrun += rc; ntry += (rt and not rc)
            items.append({"l": lab, "c": code, "s": SYN.get(lab, ""), "t": t if rt else "", "rc": rc})
        out.append({"id": sec["id"], "title": sec["title"], "items": items})
    return out, nrun, ntry
