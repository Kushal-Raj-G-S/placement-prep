"""Study guide, part 3: designing tables (DDL, constraints, keys, scenarios)."""
from mat_common import *

GD = "D. Designing tables (DDL, constraints, scenarios)"


def build():
    T = []

    # ------------------------------------------------------------------ data types
    T.append(topic("data-types", GD, "Data types: standard, PostgreSQL and MySQL",
        "Picking the right type is half of table design. Interviewers ask why you chose NUMERIC for money, TIMESTAMPTZ for time, or VARCHAR over CHAR.",
        [
            TBL(["Need", "PostgreSQL", "MySQL", "Notes"],
                ["Small / normal / big integer", "SMALLINT, INTEGER, BIGINT", "TINYINT, SMALLINT, MEDIUMINT, INT, BIGINT (UNSIGNED allowed)", "PostgreSQL has no unsigned types; use CHECK (x >= 0)"],
                ["Exact decimal", "NUMERIC(p,s) / DECIMAL(p,s)", "DECIMAL(p,s)", "p = total digits, s = digits after the point. Use for money."],
                ["Approximate decimal", "REAL, DOUBLE PRECISION", "FLOAT, DOUBLE", "Rounding errors: never for money"],
                ["Fixed text", "CHAR(n)", "CHAR(n)", "Padded with spaces to n"],
                ["Variable text", "VARCHAR(n), TEXT", "VARCHAR(n), TEXT family", "In PostgreSQL TEXT and VARCHAR perform the same; MySQL VARCHAR is limited by row size"],
                ["True/false", "BOOLEAN", "BOOLEAN (alias of TINYINT(1))", "PostgreSQL has a real boolean type"],
                ["Date only", "DATE", "DATE", ""],
                ["Time of day", "TIME", "TIME", ""],
                ["Date and time", "TIMESTAMP, TIMESTAMPTZ", "DATETIME, TIMESTAMP", "PostgreSQL TIMESTAMPTZ stores UTC and converts to the session zone. MySQL TIMESTAMP is UTC-converted with a 1970-2038 range; DATETIME is not converted"],
                ["Duration", "INTERVAL", "no equivalent (use TIME or integers)", ""],
                ["JSON", "JSON, JSONB (binary, indexable)", "JSON", "Prefer JSONB in PostgreSQL"],
                ["UUID", "UUID", "CHAR(36) or BINARY(16)", "gen_random_uuid() in PostgreSQL 13+, UUID() in MySQL"],
                ["Binary", "BYTEA", "BLOB, VARBINARY", ""],
                ["Enumeration", "CREATE TYPE mood AS ENUM (...)", "column ENUM('a','b')", "Or use a lookup table / CHECK (more flexible)"],
                ["Array", "INTEGER[], TEXT[]", "none", "PostgreSQL only"],
                ["Network / geometric", "INET, CIDR, POINT, ranges (tstzrange)", "SPATIAL types", ""]),
            H("Rules of thumb (the answers interviewers want)"),
            UL("**Money:** NUMERIC(12,2) (or integer paise/cents). Never FLOAT.",
               "**Timestamps:** store in UTC; use TIMESTAMPTZ (PostgreSQL) so zones are handled correctly.",
               "**Phone numbers and pin codes:** TEXT/VARCHAR, not integers (leading zeros, plus signs, no arithmetic).",
               "**Age:** do not store it, store date of birth and compute age.",
               "**CHAR vs VARCHAR:** CHAR for truly fixed-length codes (country code CHAR(2)); VARCHAR otherwise.",
               "**Booleans** as BOOLEAN, not 'Y'/'N' strings.",
               "**Primary keys:** BIGINT identity (or UUID if ids are created in many places).",
               "**Enums vs lookup table:** a lookup table (with FK) is easier to extend than an ENUM."),
            DIF("PostgreSQL does strict type checking (you cannot compare text to integer without a cast). MySQL silently converts in many cases, which can hide bugs. PostgreSQL also rejects over-length strings; MySQL in non-strict mode truncates with a warning."),
            SQL("""SELECT CAST('42' AS INTEGER) + 1 AS n,
       CAST(3.14159 AS REAL)  AS r,
       typeof(1.0 * 2)        AS t;""", "casting (SQLite flavour: typeof is SQLite only)", run=True),
            PGSQL("""SELECT '42'::int + 1;          -- PostgreSQL shorthand cast
SELECT CAST('2026-10-23' AS date);
SELECT now()::date, now() AT TIME ZONE 'Asia/Kolkata';"""),
        ],
        [
            Q("Which type should store a price like 199.99?", ["FLOAT", "DOUBLE", "NUMERIC(10,2)", "TEXT"], 2, "Exact decimal arithmetic; binary floating point cannot represent most decimal fractions exactly."),
            Q("Which PostgreSQL type stores a point in time with time-zone awareness?", ["TIMESTAMP", "TIMESTAMPTZ", "DATETIME", "TIME"], 1, "TIMESTAMPTZ normalises to UTC and displays in the session zone. DATETIME is a MySQL type."),
            Q("A pin code or phone number is best stored as:", ["INTEGER", "BIGINT", "VARCHAR/TEXT", "NUMERIC"], 2, "No arithmetic is done on it, and leading zeros and + signs must survive."),
            Q("PostgreSQL has which type that MySQL lacks?", ["VARCHAR", "BOOLEAN native", "ARRAY", "DATE"], 2, "Array columns exist only in PostgreSQL (MySQL has BOOLEAN as an alias, VARCHAR and DATE too)."),
            Q("Better to store date_of_birth than age because:", ["Age is bigger", "Age becomes stale; it can be derived", "DATE is faster", "Age cannot be an integer"], 1, "Derived data that changes with time should be computed, not stored."),
        ], star=True, kw="data types numeric varchar text timestamp timestamptz boolean json uuid enum money"))

    # ------------------------------------------------------------------ create table
    T.append(topic("create-table", GD, "CREATE TABLE: every clause and every constraint",
        "The most common practical question: 'write the DDL for this scenario with proper constraints'. Know the full syntax and the checklist.",
        [
            H("Syntax"),
            SQL("""CREATE TABLE [IF NOT EXISTS] table_name (
  column_name  data_type  [column_constraints...],
  ...,
  [CONSTRAINT name] table_constraint,
  ...
);""", "skeleton"),
            H("The six constraints"),
            TBL(["Constraint", "Purpose", "Column level", "Table level"],
                ["PRIMARY KEY", "Unique + NOT NULL row identifier (one per table)", "id INTEGER PRIMARY KEY", "PRIMARY KEY (a, b) for composite"],
                ["FOREIGN KEY", "Value must exist in a parent table", "dept_id INT REFERENCES dept(id)", "FOREIGN KEY (dept_id) REFERENCES dept(id)"],
                ["UNIQUE", "No duplicate values (NULLs allowed)", "email TEXT UNIQUE", "UNIQUE (a, b)"],
                ["NOT NULL", "Value required", "name TEXT NOT NULL", "column level only"],
                ["CHECK", "Boolean rule per row", "age INT CHECK (age >= 18)", "CHECK (end_date >= start_date)"],
                ["DEFAULT", "Value used when none supplied", "status TEXT DEFAULT 'new'", "column level only"]),
            NOTE("Use a **table-level** constraint when it involves more than one column (composite key, cross-column CHECK). Name important constraints with CONSTRAINT name so error messages and ALTERs are readable."),
            H("A full example"),
            SQL("""CREATE TABLE customer (
  customer_id INTEGER PRIMARY KEY,
  email       TEXT NOT NULL,
  full_name   TEXT NOT NULL,
  phone       TEXT,
  created_on  TEXT NOT NULL DEFAULT CURRENT_DATE,
  CONSTRAINT uq_customer_email UNIQUE (email),
  CONSTRAINT ck_customer_email CHECK (email LIKE '%_@_%.__%')
);

CREATE TABLE purchase (
  purchase_id  INTEGER PRIMARY KEY,
  customer_id  INTEGER NOT NULL,
  placed_on    TEXT NOT NULL DEFAULT CURRENT_DATE,
  status       TEXT NOT NULL DEFAULT 'new',
  total        NUMERIC NOT NULL CHECK (total >= 0),
  CONSTRAINT fk_purchase_customer FOREIGN KEY (customer_id)
      REFERENCES customer (customer_id) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT ck_purchase_status CHECK (status IN ('new','paid','shipped','cancelled'))
);

INSERT INTO customer (customer_id, email, full_name) VALUES (1,'a@x.com','Asha');
INSERT INTO purchase (purchase_id, customer_id, total) VALUES (1, 1, 499.50);
SELECT * FROM purchase;""", "portable version, runs here", run=True),
            P("The same tables in PostgreSQL production style:"),
            PGSQL("""CREATE TABLE customer (
  customer_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  email       TEXT NOT NULL,
  full_name   TEXT NOT NULL,
  phone       TEXT,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT uq_customer_email UNIQUE (email),
  CONSTRAINT ck_customer_email CHECK (email ~* '^[^@]+@[^@]+\\.[^@]+$')
);

CREATE TABLE purchase (
  purchase_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  customer_id BIGINT NOT NULL,
  placed_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
  status      TEXT NOT NULL DEFAULT 'new',
  total       NUMERIC(12,2) NOT NULL CHECK (total >= 0),
  CONSTRAINT fk_purchase_customer FOREIGN KEY (customer_id)
      REFERENCES customer (customer_id) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT ck_purchase_status CHECK (status IN ('new','paid','shipped','cancelled'))
);
CREATE INDEX idx_purchase_customer ON purchase (customer_id);   -- index the FK"""),
            MYSQL("""CREATE TABLE customer (
  customer_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  email       VARCHAR(255) NOT NULL,
  full_name   VARCHAR(100) NOT NULL,
  phone       VARCHAR(20),
  created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uq_customer_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE purchase (
  purchase_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  customer_id BIGINT UNSIGNED NOT NULL,
  status      ENUM('new','paid','shipped','cancelled') NOT NULL DEFAULT 'new',
  total       DECIMAL(12,2) NOT NULL,
  CONSTRAINT ck_purchase_total CHECK (total >= 0),
  CONSTRAINT fk_purchase_customer FOREIGN KEY (customer_id)
      REFERENCES customer (customer_id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;"""),
            MY("CHECK constraints are enforced from MySQL 8.0.16. Older versions parse and ignore them. Foreign keys only work on InnoDB, not MyISAM."),
            H("More column-level features"),
            PGSQL("""-- generated (computed) column
price NUMERIC(10,2), qty INT, line_total NUMERIC(12,2) GENERATED ALWAYS AS (price * qty) STORED

-- copy structure of another table
CREATE TABLE purchase_archive (LIKE purchase INCLUDING ALL);

-- create from a query
CREATE TABLE big_orders AS SELECT * FROM purchase WHERE total > 10000;

-- session-only table
CREATE TEMP TABLE scratch (id INT, note TEXT);"""),
            MYSQL("""line_total DECIMAL(12,2) GENERATED ALWAYS AS (price * qty) STORED
CREATE TABLE purchase_archive LIKE purchase;
CREATE TEMPORARY TABLE scratch (id INT, note VARCHAR(50));"""),
            H("Scenario checklist (use this every time)"),
            OL("List the entities. Each gets a table with a PRIMARY KEY.",
               "Pick types (NUMERIC for money, TIMESTAMPTZ, TEXT/VARCHAR with sensible lengths).",
               "Mark required columns NOT NULL.",
               "Natural unique things (email, ISBN, registration number) get UNIQUE.",
               "Business rules go in CHECK (price > 0, end_date >= start_date, status IN (...)).",
               "Relationships: FK on the many side, junction table for M:N, with ON DELETE chosen deliberately.",
               "Composite PK or UNIQUE for 'one per pair' rules (a student enrolls in a course once).",
               "Index the foreign keys and the columns you filter on."),
            ASK("\"Write the DDL for a library/bank/hospital system.\" Show the checklist aloud as you write: keys, types, NOT NULL, UNIQUE, CHECK, FKs with actions, junction tables, indexes."),
        ],
        [
            Q("Which constraint enforces a cross-column rule like end_date >= start_date?", ["NOT NULL", "UNIQUE", "CHECK at table level", "DEFAULT"], 2, "A CHECK that references several columns is a table-level constraint."),
            Q("How many PRIMARY KEY constraints can a table have?", ["One", "One per column", "Unlimited", "Two"], 0, "One primary key per table (it may be composite)."),
            Q("Which statement creates a composite primary key on enrollment?", ["student_id INT PRIMARY KEY, course_id INT PRIMARY KEY", "PRIMARY KEY (student_id, course_id)", "UNIQUE (student_id), UNIQUE (course_id)", "CHECK (student_id, course_id)"], 1, "A composite key is declared at table level over both columns."),
            Q("In PostgreSQL the modern standard way to auto-generate ids is:", ["AUTO_INCREMENT", "GENERATED ALWAYS AS IDENTITY", "ROWID", "COUNTER"], 1, "SERIAL still works but IDENTITY is the SQL-standard replacement. AUTO_INCREMENT is MySQL."),
            Q("Foreign key enforcement in MySQL requires which storage engine?", ["MyISAM", "InnoDB", "MEMORY", "CSV"], 1, "Only InnoDB supports foreign keys and transactions."),
            Q("Where should you put UNIQUE (email)?", ["On a derived column", "On a natural identifier that must not repeat", "Only on primary keys", "On every column"], 1, "Natural candidate keys (email, ISBN) get UNIQUE even when a surrogate PK exists."),
        ], star=True, kw="create table constraints primary key foreign key unique check not null default composite generated"))

    # ------------------------------------------------------------------ FK actions
    T.append(topic("fk-actions", GD, "Foreign keys in depth: actions, composite, self-reference, deferrable",
        "Foreign key behaviour is a favourite scenario question: 'what happens when a department is deleted?'",
        [
            H("Syntax"),
            SQL("""FOREIGN KEY (child_col) REFERENCES parent (parent_col)
    [ON DELETE action] [ON UPDATE action]""", "skeleton"),
            TBL(["Action", "On parent DELETE / UPDATE"],
                ["NO ACTION (default)", "Rejects if children exist; checked at end of statement"],
                ["RESTRICT", "Rejects immediately"],
                ["CASCADE", "Delete (or update the key of) the children too"],
                ["SET NULL", "Child FK becomes NULL (column must be nullable)"],
                ["SET DEFAULT", "Child FK becomes its DEFAULT value (PostgreSQL; not usable in MySQL InnoDB)"]),
            H("Choosing the action"),
            UL("**Owned child rows** (order lines of an order, dependents of an employee): ON DELETE CASCADE.",
               "**Important history** (orders of a customer, payments): ON DELETE RESTRICT; use a soft delete (is_active) instead.",
               "**Optional link** (employee.manager_id, product.category_id): ON DELETE SET NULL.",
               "**Key changes** are rare with surrogate keys; ON UPDATE CASCADE is harmless."),
            SQL("""PRAGMA foreign_keys = ON;
CREATE TABLE team (team_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE player (
  player_id INTEGER PRIMARY KEY, name TEXT,
  team_id INTEGER REFERENCES team(team_id) ON DELETE SET NULL
);
CREATE TABLE kit (
  kit_id INTEGER PRIMARY KEY,
  player_id INTEGER REFERENCES player(player_id) ON DELETE CASCADE
);
INSERT INTO team VALUES (1,'Blue');
INSERT INTO player VALUES (1,'Asha',1),(2,'Rohan',1);
INSERT INTO kit VALUES (1,1),(2,2);
DELETE FROM team WHERE team_id = 1;        -- players survive with NULL team
DELETE FROM player WHERE player_id = 1;    -- kit 1 disappears with it
SELECT p.name, p.team_id, (SELECT COUNT(*) FROM kit) AS kits_left FROM player p;""", "SET NULL and CASCADE in action", run=True),
            TRAP("Without ON DELETE CASCADE, deleting a parent that has children fails with a foreign key violation. In SQLite foreign keys are OFF unless you run PRAGMA foreign_keys = ON."),
            H("Self-referencing foreign key"),
            SQL("""CREATE TABLE staff (
  staff_id   INTEGER PRIMARY KEY,
  name       TEXT NOT NULL,
  manager_id INTEGER REFERENCES staff(staff_id)   -- NULL for the top boss
);
INSERT INTO staff VALUES (1,'CEO',NULL),(2,'Lead',1),(3,'Dev',2);
SELECT s.name AS employee, m.name AS manager FROM staff s LEFT JOIN staff m ON m.staff_id = s.manager_id;""", run=True),
            H("Composite foreign key"),
            SQL("""CREATE TABLE section (
  course_id INTEGER, term TEXT, room TEXT,
  PRIMARY KEY (course_id, term)
);
CREATE TABLE class_session (
  session_id INTEGER PRIMARY KEY,
  course_id INTEGER NOT NULL, term TEXT NOT NULL,
  FOREIGN KEY (course_id, term) REFERENCES section (course_id, term)
);""", "both columns must match one parent row", run=True),
            H("Referencing a non-primary column"),
            P("An FK can reference any UNIQUE (or primary key) column set, e.g. REFERENCES customer(email). PostgreSQL requires a unique constraint on the referenced columns. Use primary keys unless you have a reason."),
            H("Deferrable constraints (PostgreSQL)"),
            PGSQL("""-- two tables referencing each other (circular) or swapping keys inside one transaction
ALTER TABLE employee ADD CONSTRAINT fk_emp_dept
  FOREIGN KEY (dept_id) REFERENCES department (dept_id)
  DEFERRABLE INITIALLY DEFERRED;       -- checked at COMMIT, not per statement

BEGIN;
INSERT INTO employee (emp_id, dept_id) VALUES (1, 10);   -- department 10 does not exist yet
INSERT INTO department (dept_id, head) VALUES (10, 1);   -- now it does
COMMIT;                                                   -- constraint checked here"""),
            MY("MySQL InnoDB checks foreign keys row by row immediately and has no DEFERRABLE. To bulk load out of order, temporarily SET FOREIGN_KEY_CHECKS = 0 and turn it back on afterwards."),
            H("Dropping and adding foreign keys later"),
            PGSQL("ALTER TABLE purchase DROP CONSTRAINT fk_purchase_customer;\nALTER TABLE purchase ADD CONSTRAINT fk_purchase_customer FOREIGN KEY (customer_id) REFERENCES customer(customer_id);"),
            MYSQL("ALTER TABLE purchase DROP FOREIGN KEY fk_purchase_customer;\nALTER TABLE purchase ADD CONSTRAINT fk_purchase_customer FOREIGN KEY (customer_id) REFERENCES customer(customer_id);"),
            ASK("\"What happens if you delete a department that has employees?\" Depends on ON DELETE: default NO ACTION rejects; CASCADE removes employees; SET NULL orphans them with NULL dept_id. Good design: RESTRICT or SET NULL, never casually CASCADE on business history."),
        ],
        [
            Q("With ON DELETE SET NULL, deleting a parent row:", ["Deletes children", "Rejects the delete", "Sets the child's FK to NULL", "Sets it to 0"], 2, "Children survive with NULL, so the FK column must be nullable."),
            Q("Which action is the default if none is specified?", ["CASCADE", "SET NULL", "NO ACTION", "SET DEFAULT"], 2, "NO ACTION (reject if children exist)."),
            Q("A foreign key must reference a column that is:", ["Any column", "A primary key or UNIQUE column(s)", "A column with an index only", "A NOT NULL column only"], 1, "The parent side must be unique so every child matches exactly one row."),
            Q("Which lets you insert a child before its parent inside one transaction in PostgreSQL?", ["ON DELETE CASCADE", "DEFERRABLE INITIALLY DEFERRED", "CHECK", "TRUNCATE"], 1, "Deferred constraints are checked at COMMIT."),
            Q("An employee table with manager_id referencing employee_id is:", ["A composite key", "A self-referencing foreign key", "Invalid", "A many-to-many relationship"], 1, "A recursive relationship implemented as a FK pointing to the same table."),
        ], star=True, kw="foreign key on delete cascade set null restrict deferrable self reference composite"))

    # ------------------------------------------------------------------ alter drop
    T.append(topic("alter-drop", GD, "ALTER, DROP, TRUNCATE, RENAME and DELETE compared",
        "Changing a live schema, and the classic question: DELETE vs TRUNCATE vs DROP.",
        [
            H("ALTER TABLE cheat sheet"),
            TBL(["Task", "PostgreSQL", "MySQL"],
                ["Add column", "ALTER TABLE t ADD COLUMN c INT;", "ALTER TABLE t ADD COLUMN c INT [AFTER x];"],
                ["Drop column", "ALTER TABLE t DROP COLUMN c;", "ALTER TABLE t DROP COLUMN c;"],
                ["Change type", "ALTER TABLE t ALTER COLUMN c TYPE BIGINT USING c::bigint;", "ALTER TABLE t MODIFY c BIGINT;"],
                ["Rename column", "ALTER TABLE t RENAME COLUMN c TO d;", "ALTER TABLE t RENAME COLUMN c TO d; (8.0+) or CHANGE c d INT"],
                ["Rename table", "ALTER TABLE t RENAME TO t2;", "RENAME TABLE t TO t2;  or ALTER TABLE t RENAME t2"],
                ["Set NOT NULL", "ALTER TABLE t ALTER COLUMN c SET NOT NULL;", "ALTER TABLE t MODIFY c INT NOT NULL;"],
                ["Drop NOT NULL", "ALTER TABLE t ALTER COLUMN c DROP NOT NULL;", "ALTER TABLE t MODIFY c INT NULL;"],
                ["Set default", "ALTER TABLE t ALTER COLUMN c SET DEFAULT 5;", "ALTER TABLE t ALTER COLUMN c SET DEFAULT 5;"],
                ["Add primary key", "ALTER TABLE t ADD PRIMARY KEY (id);", "ALTER TABLE t ADD PRIMARY KEY (id);"],
                ["Add unique", "ALTER TABLE t ADD CONSTRAINT u UNIQUE (c);", "ALTER TABLE t ADD CONSTRAINT u UNIQUE (c);"],
                ["Add check", "ALTER TABLE t ADD CONSTRAINT ck CHECK (c > 0);", "ALTER TABLE t ADD CONSTRAINT ck CHECK (c > 0);"],
                ["Add foreign key", "ALTER TABLE t ADD CONSTRAINT fk FOREIGN KEY (c) REFERENCES p(id);", "same"],
                ["Drop constraint", "ALTER TABLE t DROP CONSTRAINT name;", "DROP PRIMARY KEY / DROP FOREIGN KEY name / DROP INDEX name / DROP CHECK name"]),
            SQL("""CREATE TABLE gadget (id INTEGER PRIMARY KEY, name TEXT);
ALTER TABLE gadget ADD COLUMN price NUMERIC DEFAULT 0;
ALTER TABLE gadget RENAME COLUMN name TO title;
INSERT INTO gadget (id, title) VALUES (1, 'lamp');
SELECT * FROM gadget;""", "SQLite supports ADD / RENAME COLUMN", run=True),
            H("DELETE vs TRUNCATE vs DROP"),
            TBL(["", "DELETE", "TRUNCATE", "DROP"],
                ["Kind", "DML", "DDL", "DDL"],
                ["What it removes", "Chosen rows (WHERE) or all rows", "All rows, keeps the table", "The whole table: rows, structure, indexes, constraints"],
                ["WHERE clause", "Yes", "No", "No"],
                ["Speed on big tables", "Slow (row by row, logs each row)", "Fast (deallocates pages)", "Fast"],
                ["Fires row triggers", "Yes", "No (PostgreSQL fires TRUNCATE triggers)", "No"],
                ["Rollback", "Yes", "MySQL: no. PostgreSQL: yes", "MySQL: no. PostgreSQL: yes"],
                ["Resets auto-increment", "No", "Yes (MySQL), PostgreSQL only with RESTART IDENTITY", "Gone"],
                ["Needs FK care", "Child rows must be handled", "Blocked if referenced by FK (PostgreSQL: use CASCADE)", "Blocked if referenced (CASCADE in PostgreSQL)"]),
            PGSQL("TRUNCATE TABLE orders, order_items RESTART IDENTITY CASCADE;\nDROP TABLE IF EXISTS scratch CASCADE;"),
            MYSQL("TRUNCATE TABLE orders;           -- fails if a FK references it (unless checks are off)\nDROP TABLE IF EXISTS scratch;"),
            H("Other DDL objects"),
            SQL("""CREATE SCHEMA hr;              -- namespace (PostgreSQL schema; in MySQL a schema = a database)
CREATE DATABASE shop;           -- PostgreSQL / MySQL
DROP DATABASE shop;
COMMENT ON TABLE customer IS 'people who buy';   -- PostgreSQL; MySQL: COMMENT 'text' in the column definition""", "not runnable here"),
            TRAP("Adding a NOT NULL column with no default to a table that already has rows fails. Add it nullable, backfill, then SET NOT NULL, or supply a DEFAULT."),
            ASK("\"Difference between DELETE, TRUNCATE and DROP?\" Delete = remove some or all rows (DML, loggable, WHERE, triggers). Truncate = remove all rows quickly keeping structure (DDL). Drop = remove the table itself."),
        ],
        [
            Q("Which removes all rows fastest while keeping the table definition?", ["DELETE FROM t", "TRUNCATE TABLE t", "DROP TABLE t", "UPDATE t SET ..."], 1, "TRUNCATE deallocates data pages instead of deleting row by row."),
            Q("Which supports a WHERE clause?", ["TRUNCATE", "DROP", "DELETE", "ALTER"], 2, "Only DELETE (and UPDATE/SELECT) take a WHERE filter."),
            Q("In PostgreSQL, to change a column's type you write:", ["ALTER TABLE t MODIFY c BIGINT", "ALTER TABLE t ALTER COLUMN c TYPE BIGINT", "CHANGE COLUMN c BIGINT", "UPDATE COLUMN c BIGINT"], 1, "MODIFY is the MySQL spelling."),
            Q("Adding a NOT NULL column without a default to a table with data:", ["Works, fills NULL", "Fails", "Fills 0", "Deletes rows"], 1, "Existing rows would violate NOT NULL, so supply a default or backfill first."),
            Q("Which is DML?", ["TRUNCATE", "DROP", "DELETE", "ALTER"], 2, "DELETE is a data manipulation statement."),
        ], star=True, kw="alter drop truncate delete rename add column modify cascade"))

    # ------------------------------------------------------------------ identity
    T.append(topic("identity-seq", GD, "Auto-generated keys: SERIAL, IDENTITY, sequences, AUTO_INCREMENT, UUID",
        "How surrogate keys are generated in each system, why gaps appear, and the surrogate vs natural key debate.",
        [
            TBL(["System", "Syntax", "Notes"],
                ["PostgreSQL (modern)", "id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY", "Standard SQL. ALWAYS rejects manual values unless OVERRIDING SYSTEM VALUE; BY DEFAULT allows them"],
                ["PostgreSQL (legacy)", "id SERIAL / BIGSERIAL PRIMARY KEY", "Creates a sequence and sets a default nextval(...). Still very common"],
                ["PostgreSQL sequence", "CREATE SEQUENCE s START 1; nextval('s'); currval('s'); setval('s', 100);", "Independent object, can be shared"],
                ["MySQL", "id BIGINT AUTO_INCREMENT PRIMARY KEY", "One per table; must be indexed (usually the PK). LAST_INSERT_ID() returns the last value generated in this session"],
                ["SQLite", "id INTEGER PRIMARY KEY (AUTOINCREMENT optional)", "INTEGER PRIMARY KEY is an alias for rowid"],
                ["UUID", "id UUID DEFAULT gen_random_uuid()", "MySQL: BINARY(16) with UUID_TO_BIN(UUID())"]),
            PGSQL("""CREATE TABLE ticket (
  ticket_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  subject   TEXT NOT NULL
);
INSERT INTO ticket (subject) VALUES ('printer down') RETURNING ticket_id;   -- get the generated id back
SELECT currval(pg_get_serial_sequence('ticket', 'ticket_id'));
ALTER TABLE ticket ALTER COLUMN ticket_id RESTART WITH 1000;"""),
            MYSQL("""CREATE TABLE ticket (
  ticket_id BIGINT AUTO_INCREMENT PRIMARY KEY,
  subject VARCHAR(200) NOT NULL
);
INSERT INTO ticket (subject) VALUES ('printer down');
SELECT LAST_INSERT_ID();
ALTER TABLE ticket AUTO_INCREMENT = 1000;"""),
            SQL("""CREATE TABLE note (id INTEGER PRIMARY KEY AUTOINCREMENT, body TEXT);
INSERT INTO note (body) VALUES ('first'), ('second');
SELECT last_insert_rowid() AS last_id;""", "SQLite", run=True),
            H("Why do gaps appear?"),
            P("The counter is not transactional on purpose (otherwise inserts would serialize). A rolled-back insert, a failed insert, or a crash still consumed a number. Gaps are normal; never use an id as a gapless counter (invoice numbers need a separate controlled process)."),
            H("Surrogate vs natural key"),
            TBL(["", "Surrogate (id)", "Natural (email, ISBN)"],
                ["Stability", "Never changes", "May change (email) and then cascade everywhere"],
                ["Size", "Small (4-8 bytes) so indexes and FKs are compact", "Can be long text"],
                ["Meaning", "None", "Real-world meaning, no extra lookup"],
                ["Rule of thumb", "Use as PK + keep the natural key as UNIQUE", "Fine for stable codes (country code)"]),
            H("UUID vs sequential ids"),
            UL("UUIDs can be generated anywhere without coordination and do not leak counts.",
               "Random UUIDs (v4) fragment B-tree indexes and need 16 bytes; time-ordered versions (UUIDv7, ULID) fix locality.",
               "In InnoDB the PK is the clustered index, so a random UUID PK hurts inserts badly."),
            ASK("\"Why are there gaps in an auto-increment column?\" Rollbacks and failed inserts consume values and the counter is intentionally non-transactional."),
        ],
        [
            Q("MySQL function that returns the last auto-generated id of the session:", ["LAST_ID()", "LAST_INSERT_ID()", "CURRVAL()", "SCOPE_IDENTITY()"], 1, "LAST_INSERT_ID() is per connection."),
            Q("Which clause returns the new id from an INSERT in PostgreSQL?", ["OUTPUT", "RETURNING", "SELECT LAST", "GET ID"], 1, "INSERT ... RETURNING id."),
            Q("Gaps in a sequence appear because:", ["Bugs", "Rollbacks still consume values", "Deletes renumber", "Indexes fragment"], 1, "Sequences are non-transactional by design."),
            Q("Best practice for a table with a natural unique identifier such as email:", ["Use email as PK only", "Surrogate PK plus UNIQUE on email", "No key", "Two primary keys"], 1, "Stable small surrogate PK; the natural key still gets its UNIQUE constraint."),
            Q("In InnoDB a random UUID primary key mainly causes:", ["Smaller indexes", "Index fragmentation and slower inserts", "Faster joins", "Gapless ids"], 1, "The PK is the clustered index, so random inserts split pages all over the tree."),
        ], kw="auto increment serial identity sequence uuid surrogate natural key nextval last_insert_id"))

    # ------------------------------------------------------------------ scenarios 1
    T.append(topic("scenario-ddl-1", GD, "Scenario to tables: library and online shop",
        "Interviewers describe a system in two sentences and say 'create the tables'. Here are full answers in PostgreSQL style. Read the requirement, try it yourself first, then compare.",
        [
            H("Scenario 1: Library management"),
            TXT("""Requirements:
- Members borrow books. A book title can have several authors and an author can write several books.
- The library owns several physical copies of a title. A loan is for one copy, has a loan date, due date and optional return date.
- A member can have at most 5 open loans (enforce in a trigger/app). A copy cannot be on loan twice at the same time.
- Fines are charged per overdue loan.""", "try first"),
            P("Reasoning: entities = member, author, book (title), copy, loan, fine. author-book is M:N (junction). book-copy is 1:N. loan links member and copy (1:N each). fine belongs to a loan (1:1 optional)."),
            PGSQL("""CREATE TABLE member (
  member_id   BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  full_name   TEXT NOT NULL,
  email       TEXT NOT NULL UNIQUE,
  joined_on   DATE NOT NULL DEFAULT CURRENT_DATE,
  is_active   BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE author (
  author_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name      TEXT NOT NULL
);

CREATE TABLE book (
  book_id   BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  isbn      CHAR(13) NOT NULL UNIQUE,
  title     TEXT NOT NULL,
  publisher TEXT,
  published_year SMALLINT CHECK (published_year BETWEEN 1450 AND 2100)
);

CREATE TABLE book_author (                       -- M:N junction
  book_id   BIGINT REFERENCES book(book_id)     ON DELETE CASCADE,
  author_id BIGINT REFERENCES author(author_id) ON DELETE RESTRICT,
  PRIMARY KEY (book_id, author_id)
);

CREATE TABLE book_copy (
  copy_id   BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  book_id   BIGINT NOT NULL REFERENCES book(book_id) ON DELETE RESTRICT,
  shelf     TEXT,
  status    TEXT NOT NULL DEFAULT 'available' CHECK (status IN ('available','on_loan','lost'))
);

CREATE TABLE loan (
  loan_id     BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  member_id   BIGINT NOT NULL REFERENCES member(member_id) ON DELETE RESTRICT,
  copy_id     BIGINT NOT NULL REFERENCES book_copy(copy_id) ON DELETE RESTRICT,
  loaned_on   DATE NOT NULL DEFAULT CURRENT_DATE,
  due_on      DATE NOT NULL,
  returned_on DATE,
  CONSTRAINT ck_loan_dates CHECK (due_on >= loaned_on AND (returned_on IS NULL OR returned_on >= loaned_on))
);
-- a copy cannot be on loan twice: only one open loan per copy
CREATE UNIQUE INDEX uq_open_loan_per_copy ON loan (copy_id) WHERE returned_on IS NULL;

CREATE TABLE fine (
  loan_id   BIGINT PRIMARY KEY REFERENCES loan(loan_id) ON DELETE CASCADE,   -- 1:1, shares the key
  amount    NUMERIC(8,2) NOT NULL CHECK (amount > 0),
  paid      BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE INDEX idx_loan_member ON loan (member_id);"""),
            NOTE("The partial unique index is the PostgreSQL way to say 'at most one open loan per copy'. In MySQL (no partial indexes) use a trigger or a generated column trick. Mention both."),
            H("Scenario 2: Online shop"),
            TXT("""Requirements:
- Customers have several saved addresses. Products belong to one category (categories form a tree).
- An order is placed by a customer, ships to one address and contains many products with quantity.
- The price paid must be kept on the order line even if the product price changes later.
- Payments: an order can be paid in several instalments. Stock must never go negative.""", "try first"),
            PGSQL("""CREATE TABLE customer (
  customer_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  email       TEXT NOT NULL UNIQUE,
  full_name   TEXT NOT NULL,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE address (
  address_id  BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  customer_id BIGINT NOT NULL REFERENCES customer(customer_id) ON DELETE CASCADE,
  line1 TEXT NOT NULL, city TEXT NOT NULL, pincode CHAR(6) NOT NULL,
  is_default BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE category (
  category_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name        TEXT NOT NULL,
  parent_id   BIGINT REFERENCES category(category_id) ON DELETE SET NULL     -- tree
);

CREATE TABLE product (
  product_id  BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  sku         TEXT NOT NULL UNIQUE,
  name        TEXT NOT NULL,
  category_id BIGINT REFERENCES category(category_id),
  price       NUMERIC(10,2) NOT NULL CHECK (price >= 0),
  stock       INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0)
);

CREATE TABLE orders (                           -- "order" is a reserved word
  order_id    BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  customer_id BIGINT NOT NULL REFERENCES customer(customer_id),
  address_id  BIGINT NOT NULL REFERENCES address(address_id),
  placed_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
  status      TEXT NOT NULL DEFAULT 'new' CHECK (status IN ('new','paid','shipped','delivered','cancelled'))
);

CREATE TABLE order_item (
  order_id    BIGINT REFERENCES orders(order_id) ON DELETE CASCADE,
  product_id  BIGINT REFERENCES product(product_id),
  quantity    INTEGER NOT NULL CHECK (quantity > 0),
  unit_price  NUMERIC(10,2) NOT NULL CHECK (unit_price >= 0),   -- snapshot of the price at purchase time
  PRIMARY KEY (order_id, product_id)
);

CREATE TABLE payment (
  payment_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  order_id   BIGINT NOT NULL REFERENCES orders(order_id),
  amount     NUMERIC(10,2) NOT NULL CHECK (amount > 0),
  method     TEXT NOT NULL CHECK (method IN ('card','upi','cod','netbanking')),
  paid_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_orders_customer ON orders (customer_id);
CREATE INDEX idx_order_item_product ON order_item (product_id);
CREATE INDEX idx_product_category ON product (category_id);"""),
            H("Points to say out loud"),
            UL("order_item stores unit_price so history is stable (a deliberate, justified duplication).",
               "stock >= 0 CHECK protects against overselling at the database level; concurrent decrements are made safe by UPDATE product SET stock = stock - 1 WHERE product_id = ? AND stock >= 1.",
               "Customer deletion is blocked (orders reference it); use is_active or anonymize.",
               "Address FK from orders gives a snapshot problem: if the address is edited, old orders change. Real systems copy the address into the order or make addresses immutable."),
            ASK("\"Why did you store unit_price in order_item?\" Because product prices change; the order must record what was actually charged. It is controlled duplication, not a normalization failure."),
        ],
        [
            Q("Why is book_author a separate table?", ["To save space", "It implements the many-to-many relation between books and authors", "Because ISBN is long", "To enable triggers"], 1, "An M:N relationship needs a junction table with both FKs as a composite PK."),
            Q("How do you ensure a copy cannot have two open loans in PostgreSQL?", ["UNIQUE (copy_id) on all rows", "Partial unique index on copy_id WHERE returned_on IS NULL", "NOT NULL on copy_id", "A CHECK on dates"], 1, "Only open loans (returned_on IS NULL) are constrained."),
            Q("order_item.unit_price duplicates product.price on purpose because:", ["Normalization requires it", "Prices change, the order needs the historical price", "FKs require it", "It speeds up INSERT"], 1, "Snapshot of the price at the time of purchase."),
            Q("Why is the table named orders and not order?", ["Convention only", "ORDER is a reserved SQL keyword", "PostgreSQL forbids singular names", "Because of FK rules"], 1, "ORDER (BY) is reserved; quote it or avoid it."),
            Q("Which keeps stock from going negative?", ["CHECK (stock >= 0)", "NOT NULL", "UNIQUE", "DEFAULT 0"], 0, "A CHECK constraint rejects any update that would make it negative."),
        ], star=True, kw="scenario library shop ecommerce create tables design junction partial unique snapshot price"))

    # ------------------------------------------------------------------ scenarios 2
    T.append(topic("scenario-ddl-2", GD, "Scenario to tables: hospital, bank, college, hotel booking",
        "More full designs. Notice the recurring tricks: junction tables, CHECK rules, overlap prevention, immutable ledgers, and where triggers are needed.",
        [
            H("Scenario 3: Hospital appointments"),
            TXT("""- Doctors belong to a department and have a specialty. Patients have a unique national id.
- A patient books an appointment with a doctor at a time slot. A doctor cannot be double-booked.
- Each appointment may result in prescriptions listing medicines with dosage and days.""", "try first"),
            PGSQL("""CREATE TABLE department (
  dept_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name    TEXT NOT NULL UNIQUE
);
CREATE TABLE doctor (
  doctor_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  full_name TEXT NOT NULL,
  specialty TEXT NOT NULL,
  dept_id   BIGINT NOT NULL REFERENCES department(dept_id)
);
CREATE TABLE patient (
  patient_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  national_id TEXT NOT NULL UNIQUE,
  full_name  TEXT NOT NULL,
  dob        DATE NOT NULL CHECK (dob <= CURRENT_DATE),
  phone      TEXT
);
CREATE TABLE appointment (
  appt_id    BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  patient_id BIGINT NOT NULL REFERENCES patient(patient_id),
  doctor_id  BIGINT NOT NULL REFERENCES doctor(doctor_id),
  slot_start TIMESTAMPTZ NOT NULL,
  slot_end   TIMESTAMPTZ NOT NULL,
  status     TEXT NOT NULL DEFAULT 'booked' CHECK (status IN ('booked','done','cancelled','no_show')),
  CHECK (slot_end > slot_start),
  UNIQUE (doctor_id, slot_start)                       -- simple double-booking guard
);
CREATE TABLE medicine (
  medicine_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name TEXT NOT NULL UNIQUE
);
CREATE TABLE prescription (
  appt_id     BIGINT REFERENCES appointment(appt_id) ON DELETE CASCADE,
  medicine_id BIGINT REFERENCES medicine(medicine_id),
  dosage      TEXT NOT NULL,
  days        SMALLINT NOT NULL CHECK (days > 0),
  PRIMARY KEY (appt_id, medicine_id)
);"""),
            PGSQL("""-- stronger rule: no OVERLAPPING slots for the same doctor (needs btree_gist)
CREATE EXTENSION IF NOT EXISTS btree_gist;
ALTER TABLE appointment ADD CONSTRAINT no_overlap
  EXCLUDE USING gist (doctor_id WITH =, tstzrange(slot_start, slot_end) WITH &&)
  WHERE (status = 'booked');"""),
            H("Scenario 4: Banking (ledger style)"),
            TXT("""- A customer can have several accounts (savings, current). An account has a balance that must never be negative for savings.
- Every deposit, withdrawal or transfer is recorded and never edited or deleted.
- A transfer moves money between two accounts atomically.""", "try first"),
            PGSQL("""CREATE TABLE bank_customer (
  customer_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  pan         CHAR(10) NOT NULL UNIQUE,
  full_name   TEXT NOT NULL
);
CREATE TYPE account_kind AS ENUM ('savings', 'current');
CREATE TABLE account (
  account_no  BIGINT GENERATED ALWAYS AS IDENTITY (START WITH 100000) PRIMARY KEY,
  customer_id BIGINT NOT NULL REFERENCES bank_customer(customer_id),
  kind        account_kind NOT NULL,
  balance     NUMERIC(14,2) NOT NULL DEFAULT 0,
  opened_on   DATE NOT NULL DEFAULT CURRENT_DATE,
  CONSTRAINT ck_savings_non_negative CHECK (kind <> 'savings' OR balance >= 0)
);
CREATE TABLE ledger_entry (                       -- append-only
  entry_id    BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  account_no  BIGINT NOT NULL REFERENCES account(account_no),
  amount      NUMERIC(14,2) NOT NULL CHECK (amount <> 0),   -- +credit / -debit
  txn_id      UUID NOT NULL,                                -- groups the two legs of a transfer
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
  note        TEXT
);
CREATE INDEX idx_ledger_account ON ledger_entry (account_no, created_at);"""),
            PGSQL("""-- atomic transfer: either both legs happen or neither
BEGIN;
UPDATE account SET balance = balance - 500 WHERE account_no = 100001;   -- CHECK stops overdraft
UPDATE account SET balance = balance + 500 WHERE account_no = 100002;
INSERT INTO ledger_entry (account_no, amount, txn_id) VALUES (100001, -500, gen_random_uuid());
COMMIT;"""),
            H("Scenario 5: College"),
            TXT("""- Departments offer courses. Instructors teach course sections each term. Students enroll in sections.
- A student cannot enroll twice in the same section. Grades are only allowed for enrolled students.
- A course can have prerequisite courses (a course may need several).""", "try first"),
            PGSQL("""CREATE TABLE course (
  course_id  TEXT PRIMARY KEY,                    -- natural code like 'CS301'
  title      TEXT NOT NULL,
  credits    SMALLINT NOT NULL CHECK (credits BETWEEN 1 AND 6)
);
CREATE TABLE prerequisite (                       -- self M:N on course
  course_id TEXT REFERENCES course(course_id) ON DELETE CASCADE,
  requires  TEXT REFERENCES course(course_id),
  PRIMARY KEY (course_id, requires),
  CHECK (course_id <> requires)
);
CREATE TABLE instructor (
  instructor_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name TEXT NOT NULL
);
CREATE TABLE section (
  section_id    BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  course_id     TEXT NOT NULL REFERENCES course(course_id),
  term          TEXT NOT NULL,                    -- '2026-ODD'
  instructor_id BIGINT NOT NULL REFERENCES instructor(instructor_id),
  capacity      SMALLINT NOT NULL CHECK (capacity > 0),
  UNIQUE (course_id, term, instructor_id)
);
CREATE TABLE student (
  usn  TEXT PRIMARY KEY,
  name TEXT NOT NULL
);
CREATE TABLE enrollment (
  usn        TEXT REFERENCES student(usn) ON DELETE CASCADE,
  section_id BIGINT REFERENCES section(section_id),
  grade      CHAR(2) CHECK (grade IN ('O','A+','A','B+','B','C','F')),
  PRIMARY KEY (usn, section_id)                   -- one enrollment per student per section
);"""),
            H("Scenario 6: Hotel booking (no double booking)"),
            PGSQL("""CREATE TABLE room (
  room_no INT PRIMARY KEY,
  kind    TEXT NOT NULL CHECK (kind IN ('single','double','suite')),
  rate    NUMERIC(8,2) NOT NULL CHECK (rate > 0)
);
CREATE TABLE guest (
  guest_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name TEXT NOT NULL, phone TEXT NOT NULL
);
CREATE TABLE booking (
  booking_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  room_no  INT    NOT NULL REFERENCES room(room_no),
  guest_id BIGINT NOT NULL REFERENCES guest(guest_id),
  check_in DATE NOT NULL, check_out DATE NOT NULL,
  CHECK (check_out > check_in),
  EXCLUDE USING gist (room_no WITH =, daterange(check_in, check_out) WITH &&)   -- needs btree_gist
);"""),
            MY("MySQL has no EXCLUDE constraints. Prevent overlaps with a trigger that checks SELECT 1 FROM booking WHERE room_no = NEW.room_no AND check_in < NEW.check_out AND check_out > NEW.check_in, or store one row per room-night with UNIQUE (room_no, night)."),
            H("Patterns to name in interviews"),
            UL("**Junction table** for M:N, with relationship attributes.",
               "**Composite PK or UNIQUE** for 'once per pair'.",
               "**CHECK** for ranges, state lists, date ordering, conditional rules.",
               "**Snapshot columns** for history (price, address).",
               "**Append-only ledger** instead of editing balances only.",
               "**Soft delete** (is_active, deleted_at) where deleting would break history.",
               "**Overlap prevention:** EXCLUDE (PostgreSQL), triggers or per-slot rows (MySQL).",
               "**State machine** columns with CHECK lists; transitions in the application or a trigger."),
        ],
        [
            Q("To stop a doctor being booked for overlapping time ranges in PostgreSQL you would use:", ["A plain UNIQUE on slot_start", "An EXCLUDE USING gist constraint on a time range", "A CHECK on slot_end", "A foreign key"], 1, "Exclusion constraints reject rows whose ranges overlap with an existing row."),
            Q("Why model a bank ledger as append-only entries?", ["Smaller table", "Auditability: history is never edited or deleted", "Faster queries", "Because balances cannot be stored"], 1, "Every movement is permanent; the balance is derived or reconciled."),
            Q("A prerequisite table linking course to course is an example of:", ["A weak entity", "A recursive M:N relationship (junction table)", "Specialization", "A view"], 1, "Both columns reference course."),
            Q("Primary key for enrollment so a student enrolls once per section:", ["(usn)", "(section_id)", "(usn, section_id)", "A grade column"], 2, "Composite PK is the 'once per pair' rule."),
            Q("Which MySQL technique replaces EXCLUDE for room overlap?", ["Triggers or one row per room-night with UNIQUE", "CHECK with subquery", "ON DELETE CASCADE", "FULLTEXT index"], 0, "MySQL lacks exclusion constraints and CHECKs cannot see other rows."),
        ], star=True, kw="scenario hospital bank college hotel booking exclude constraint ledger prerequisite design tables"))

    return T
