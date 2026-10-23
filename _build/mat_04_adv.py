"""Study guide, part 4: transactions in SQL, triggers, functions and procedures, cursors, security, partitioning."""
from mat_common import *

GG = "G. Programmability, transactions and security"


def build():
    T = []

    # ------------------------------------------------------------------ transactions in SQL
    T.append(topic("transactions-sql", GG, "Transactions in SQL: BEGIN, COMMIT, SAVEPOINT, locking reads",
        "The commands behind ACID. The standard demo is a money transfer.",
        [
            TBL(["Task", "PostgreSQL", "MySQL (InnoDB)"],
                ["Start", "BEGIN;  or START TRANSACTION;", "START TRANSACTION;  or BEGIN;"],
                ["Make permanent", "COMMIT;", "COMMIT;"],
                ["Undo", "ROLLBACK;", "ROLLBACK;"],
                ["Partial undo", "SAVEPOINT sp; ... ROLLBACK TO sp; RELEASE sp;", "same"],
                ["Autocommit", "Each statement commits itself unless inside BEGIN (psql, and drivers per setting)", "SET autocommit = 0 disables it; default ON"],
                ["Isolation level", "BEGIN ISOLATION LEVEL REPEATABLE READ;  or SET TRANSACTION ISOLATION LEVEL ...", "SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ;"],
                ["DDL inside", "Transactional: CREATE/ALTER/DROP can be rolled back", "Implicit commit: DDL ends the transaction"],
                ["Error inside", "Whole transaction becomes aborted: every command fails until ROLLBACK", "Only the failing statement is rolled back (by default)"]),
            SQL("""CREATE TABLE acct (id INTEGER PRIMARY KEY, owner TEXT, balance INTEGER CHECK (balance >= 0));
INSERT INTO acct VALUES (1,'Asha',1000),(2,'Rohan',200);

BEGIN;
UPDATE acct SET balance = balance - 300 WHERE id = 1;
SAVEPOINT after_debit;
UPDATE acct SET balance = balance + 300 WHERE id = 99;          -- wrong account: affects 0 rows
ROLLBACK TO after_debit;                                        -- undo only the bad step
UPDATE acct SET balance = balance + 300 WHERE id = 2;
COMMIT;
SELECT * FROM acct;""", "debit and credit in one unit; savepoint undoes just the mistake", run=True),
            SQL("""BEGIN;
UPDATE employees SET salary = 0;
SELECT COUNT(*) AS zero_paid FROM employees WHERE salary = 0;
ROLLBACK;
SELECT COUNT(*) AS zero_paid_after_rollback FROM employees WHERE salary = 0;""", "rollback restores everything", run=True),
            H("Locking reads"),
            PGSQL("""BEGIN;
SELECT balance FROM account WHERE account_no = 100001 FOR UPDATE;          -- blocks other writers/lockers on this row
UPDATE account SET balance = balance - 500 WHERE account_no = 100001;
COMMIT;

SELECT ... FOR SHARE;                       -- others may read-lock but not modify
SELECT ... FOR UPDATE NOWAIT;               -- error at once instead of waiting
SELECT ... FOR UPDATE SKIP LOCKED;          -- skip rows locked by others (job queues)
LOCK TABLE account IN EXCLUSIVE MODE;       -- explicit table lock"""),
            MYSQL("""START TRANSACTION;
SELECT balance FROM account WHERE account_no = 100001 FOR UPDATE;
UPDATE account SET balance = balance - 500 WHERE account_no = 100001;
COMMIT;
-- 8.0 adds: FOR UPDATE NOWAIT / SKIP LOCKED, and FOR SHARE (older: LOCK IN SHARE MODE)"""),
            H("Lost update, step by step"),
            TXT("""Balance = 100. Two sessions each add 10.

 T1: SELECT balance      -> 100
 T2: SELECT balance      -> 100
 T1: UPDATE balance = 110 ; COMMIT
 T2: UPDATE balance = 110 ; COMMIT          <- T1's +10 is lost

Fixes: (1) atomic UPDATE acct SET balance = balance + 10
       (2) SELECT ... FOR UPDATE before reading
       (3) SERIALIZABLE isolation and retry on failure
       (4) optimistic check:  UPDATE ... WHERE id = ? AND version = ?"""),
            H("Deadlock demo and avoidance"),
            TXT("""T1: UPDATE acct SET ... WHERE id = 1;   T2: UPDATE acct SET ... WHERE id = 2;
T1: UPDATE acct SET ... WHERE id = 2;   (waits for T2)
T2: UPDATE acct SET ... WHERE id = 1;   (waits for T1)  -> deadlock, DB aborts one with an error

Avoid: always touch rows in the same order (for a transfer, lock the lower account id first),
keep transactions short, retry the aborted transaction."""),
            H("Good habits"),
            UL("Keep transactions short; never hold one open while waiting for a user.",
               "Do not mix slow external calls (HTTP, email) inside a transaction.",
               "Retry on serialization failures (SQLSTATE 40001) and deadlocks (40P01 in PostgreSQL, 1213 in MySQL).",
               "Use constraints (CHECK balance >= 0) as the last line of defence.",
               "A single statement is already atomic; use that where possible (UPDATE ... SET x = x + 1)."),
            ASK("\"Explain a bank transfer in SQL.\" BEGIN, debit, credit, COMMIT; if anything fails, ROLLBACK. Add FOR UPDATE or an atomic UPDATE with a balance check, consistent lock ordering and a retry loop."),
        ],
        [
            Q("In PostgreSQL, after an error inside a transaction block:", ["Only that statement fails", "All further commands fail until ROLLBACK", "The transaction commits", "The session closes"], 1, "The transaction is marked aborted ('current transaction is aborted')."),
            Q("DDL inside a MySQL transaction:", ["Is rolled back with it", "Causes an implicit commit", "Is forbidden", "Is deferred"], 1, "DDL statements commit implicitly in MySQL; PostgreSQL DDL is transactional."),
            Q("SAVEPOINT allows:", ["Committing part of a transaction", "Rolling back to a point without ending the transaction", "Nested databases", "Faster commits"], 1, "ROLLBACK TO savepoint undoes later work only."),
            Q("Which prevents the lost update without changing isolation level?", ["SELECT ... FOR UPDATE", "SELECT DISTINCT", "ORDER BY", "LIMIT 1"], 0, "It locks the row until the transaction ends."),
            Q("SKIP LOCKED is mainly used for:", ["Reports", "Work queues where workers take unlocked rows", "Backups", "Indexes"], 1, "Each worker grabs a different available row."),
        ], star=True, kw="transaction begin commit rollback savepoint autocommit for update skip locked nowait deadlock lost update isolation"))

    # ------------------------------------------------------------------ triggers 1
    T.append(topic("triggers-basics", GG, "Triggers: what they are, timing, row vs statement, OLD and NEW",
        "A trigger is code the database runs automatically when an INSERT, UPDATE or DELETE happens on a table. Triggers are a standard interview topic: definition, types, syntax, an example, and when NOT to use them.",
        [
            H("Definition and use cases"),
            P("A **trigger** is a stored block of code bound to a table (or view) event. The database fires it automatically; the application never calls it."),
            UL("Audit logging (who changed what).",
               "Enforcing complex business rules that CHECK cannot express (rules across rows or tables).",
               "Maintaining derived or denormalized data (running totals, counters, search columns).",
               "Setting values automatically (updated_at, normalising text).",
               "Cascading custom actions, soft delete, history tables.",
               "Making a view updatable (INSTEAD OF triggers)."),
            H("Classification"),
            TBL(["Dimension", "Options", "Meaning"],
                ["Timing", "BEFORE", "Runs before the change is applied; can modify NEW values or cancel the operation. Use for validation and defaults"],
                ["", "AFTER", "Runs after the change; the row is already written. Use for audit, cascading to other tables"],
                ["", "INSTEAD OF", "Replaces the operation; used on views (PostgreSQL, SQL Server, Oracle). MySQL has none"],
                ["Event", "INSERT, UPDATE [OF cols], DELETE, TRUNCATE (PostgreSQL)", "What fires it"],
                ["Level", "FOR EACH ROW", "Once per affected row; can see OLD / NEW"],
                ["", "FOR EACH STATEMENT", "Once per statement regardless of rows. PostgreSQL supports it; MySQL only has row-level"]),
            TBL(["Event", "OLD", "NEW"],
                ["INSERT", "not available", "the row being inserted"],
                ["UPDATE", "the row before", "the row after"],
                ["DELETE", "the row being deleted", "not available"]),
            P("That gives the familiar count: 3 events × 2 timings × 2 levels = 12 types in the textbook."),
            H("Runnable example: an audit trigger (SQLite syntax)"),
            SQL("""CREATE TABLE salary_audit (
  audit_id   INTEGER PRIMARY KEY AUTOINCREMENT,
  emp_id     INTEGER, old_salary INTEGER, new_salary INTEGER,
  changed_at TEXT DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER trg_salary_audit
AFTER UPDATE OF salary ON employees
FOR EACH ROW
WHEN OLD.salary <> NEW.salary
BEGIN
  INSERT INTO salary_audit (emp_id, old_salary, new_salary) VALUES (OLD.id, OLD.salary, NEW.salary);
END;

UPDATE employees SET salary = salary + 2000 WHERE dept_id = 3;     -- fires once per row changed (3 rows)
UPDATE employees SET salary = salary WHERE id = 1;                   -- no real change: WHEN stops it
SELECT emp_id, old_salary, new_salary FROM salary_audit ORDER BY audit_id;""", "AFTER UPDATE trigger, row level, with WHEN", run=True),
            MYSQL("""CREATE TABLE salary_audit (
  audit_id   INT AUTO_INCREMENT PRIMARY KEY,
  emp_id     INT, old_salary INT, new_salary INT,
  changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
DELIMITER $$
CREATE TRIGGER trg_salary_audit AFTER UPDATE ON employees
FOR EACH ROW
BEGIN
  IF OLD.salary <> NEW.salary THEN           -- MySQL has no WHEN clause: test inside the body
    INSERT INTO salary_audit (emp_id, old_salary, new_salary) VALUES (OLD.id, OLD.salary, NEW.salary);
  END IF;
END$$
DELIMITER ;""", 'MySQL: no WHEN, DELIMITER, IF ... END IF'),
            H("Runnable example: a BEFORE trigger that validates"),
            SQL("""CREATE TRIGGER trg_salary_floor
BEFORE INSERT ON employees
FOR EACH ROW
WHEN NEW.salary < 20000
BEGIN
  SELECT RAISE(ABORT, 'salary below minimum wage');
END;
-- INSERT INTO employees (id, name, salary) VALUES (99, 'Test', 10000);   -- fails with: salary below minimum wage
INSERT INTO employees (id, name, salary) VALUES (99, 'Test', 30000);        -- allowed
SELECT COUNT(*) AS rows_now FROM employees;""", "BEFORE trigger cancels bad rows", run=True),
            H("PostgreSQL syntax: function + trigger"),
            P("In PostgreSQL the logic lives in a trigger FUNCTION (returns trigger) and CREATE TRIGGER just attaches it. One function can serve many triggers."),
            PGSQL("""CREATE OR REPLACE FUNCTION fn_salary_audit() RETURNS trigger
LANGUAGE plpgsql AS $$
BEGIN
  IF NEW.salary IS DISTINCT FROM OLD.salary THEN
    INSERT INTO salary_audit (emp_id, old_salary, new_salary, changed_at)
    VALUES (OLD.id, OLD.salary, NEW.salary, now());
  END IF;
  RETURN NEW;                 -- AFTER triggers ignore the value; BEFORE row triggers must return NEW (or OLD for DELETE) or NULL to skip the row
END;
$$;

CREATE TRIGGER trg_salary_audit
AFTER UPDATE OF salary ON employees
FOR EACH ROW
WHEN (OLD.salary IS DISTINCT FROM NEW.salary)
EXECUTE FUNCTION fn_salary_audit();              -- PostgreSQL 11+; older: EXECUTE PROCEDURE"""),
            PGSQL("""CREATE OR REPLACE FUNCTION fn_salary_floor() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  IF NEW.salary < 20000 THEN
    RAISE EXCEPTION 'salary % is below minimum', NEW.salary USING ERRCODE = 'check_violation';
  END IF;
  RETURN NEW;
END; $$;

CREATE TRIGGER trg_salary_floor BEFORE INSERT OR UPDATE ON employees
FOR EACH ROW EXECUTE FUNCTION fn_salary_floor();"""),
            TBL(["Special variable (PostgreSQL)", "Value"],
                ["NEW / OLD", "Row after / before"],
                ["TG_OP", "'INSERT', 'UPDATE', 'DELETE', 'TRUNCATE'"],
                ["TG_TABLE_NAME, TG_TABLE_SCHEMA", "Table the trigger is on"],
                ["TG_WHEN, TG_LEVEL", "'BEFORE'/'AFTER'/'INSTEAD OF', 'ROW'/'STATEMENT'"],
                ["TG_ARGV[n]", "Arguments passed in CREATE TRIGGER"]),
            H("MySQL syntax: body written inline"),
            MYSQL("""DELIMITER $$
CREATE TRIGGER trg_salary_audit
AFTER UPDATE ON employees
FOR EACH ROW
BEGIN
  IF NEW.salary <> OLD.salary THEN
    INSERT INTO salary_audit (emp_id, old_salary, new_salary) VALUES (OLD.id, OLD.salary, NEW.salary);
  END IF;
END$$

CREATE TRIGGER trg_salary_floor
BEFORE INSERT ON employees
FOR EACH ROW
BEGIN
  IF NEW.salary < 20000 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'salary below minimum';
  END IF;
END$$
DELIMITER ;"""),
            MY("DELIMITER is a client-side command of the mysql shell (not SQL). It lets the shell treat the semicolons inside the BEGIN...END body as part of one statement. Drivers and GUI tools do not need it."),
            H("PostgreSQL vs MySQL vs SQLite at a glance"),
            TBL(["Feature", "PostgreSQL", "MySQL", "SQLite"],
                ["Body location", "Separate trigger function", "Inline BEGIN...END", "Inline BEGIN...END"],
                ["Row-level", "Yes", "Yes (only)", "Yes (only)"],
                ["Statement-level", "Yes (with transition tables REFERENCING NEW TABLE)", "No", "No"],
                ["INSTEAD OF", "Yes (views)", "No", "Yes (views)"],
                ["TRUNCATE trigger", "Yes", "No", "No"],
                ["Raise an error", "RAISE EXCEPTION", "SIGNAL SQLSTATE", "RAISE(ABORT, msg)"],
                ["Conditional firing", "WHEN (condition) on the trigger", "IF inside the body", "WHEN on the trigger"],
                ["Fired by FK cascade actions", "Yes", "No (InnoDB cascades do not fire triggers)", "Yes"],
                ["Order of several triggers", "Alphabetical by name", "Creation order, or FOLLOWS / PRECEDES", "Undefined"],
                ["Drop", "DROP TRIGGER name ON table;", "DROP TRIGGER name;", "DROP TRIGGER name;"],
                ["Disable", "ALTER TABLE t DISABLE TRIGGER name;", "no switch (drop it)", "no switch"]),
            H("When NOT to use triggers"),
            UL("Rules that a CHECK, UNIQUE, FK or generated column can express: use the constraint (clearer, faster, visible).",
               "Heavy logic or calls to external services: triggers run inside the writer's transaction and slow every write.",
               "Chains of triggers that fire other triggers: hard to debug (and recursion risk).",
               "Business logic that the team should see in application code: triggers are invisible side effects.",
               "Bulk loads: they fire per row; disable or load differently."),
            TRAP("A BEFORE UPDATE trigger that itself UPDATEs the same table can recurse forever. Modify NEW instead of running another UPDATE, or guard with pg_trigger_depth() / WHEN."),
            ASK("\"What is a trigger? Types? Example?\" Answer in this order: definition (automatic code on INSERT/UPDATE/DELETE), BEFORE vs AFTER vs INSTEAD OF, row vs statement level, OLD/NEW, then give the audit-log example, then the drawbacks."),
        ],
        [
            Q("Which trigger can change the values being inserted before they are stored?", ["AFTER INSERT", "BEFORE INSERT", "INSTEAD OF DELETE", "AFTER DELETE"], 1, "BEFORE row triggers may modify NEW."),
            Q("In a DELETE trigger which row reference is available?", ["NEW only", "OLD only", "Both", "Neither"], 1, "There is no new row after a delete."),
            Q("Which database does NOT support statement-level triggers?", ["PostgreSQL", "Oracle", "MySQL", "SQL Server"], 2, "MySQL triggers are FOR EACH ROW only."),
            Q("In PostgreSQL a trigger's logic is placed in:", ["The CREATE TRIGGER body", "A function that returns trigger", "A view", "A procedure called by the app"], 1, "CREATE TRIGGER merely attaches the trigger function."),
            Q("INSTEAD OF triggers are used to:", ["Speed up inserts", "Make complex views accept writes", "Replace indexes", "Enforce NOT NULL"], 1, "They intercept the write to the view and redirect it to base tables."),
            Q("Which is a good reason NOT to use a trigger?", ["Audit logging", "Rule is expressible as a CHECK constraint", "Maintaining updated_at", "Complex cross-table validation"], 1, "Use the declarative constraint when possible."),
        ], star=True, kw="trigger before after instead of row statement old new audit plpgsql create trigger raise exception signal delimiter"))

    # ------------------------------------------------------------------ triggers 2
    T.append(topic("triggers-patterns", GG, "Trigger patterns interviewers ask you to write",
        "Six scenarios you can write from memory. Each is shown in PostgreSQL and MySQL.",
        [
            H("1. Automatic updated_at timestamp"),
            PGSQL("""CREATE OR REPLACE FUNCTION set_updated_at() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  NEW.updated_at := now();
  RETURN NEW;
END; $$;

CREATE TRIGGER trg_employee_updated BEFORE UPDATE ON employees
FOR EACH ROW EXECUTE FUNCTION set_updated_at();"""),
            MYSQL("""-- simplest in MySQL needs no trigger at all:
updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"""),
            H("2. Full audit log (who, what, when) for any table"),
            PGSQL("""CREATE TABLE audit_log (
  audit_id   BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  table_name TEXT NOT NULL, op TEXT NOT NULL,
  row_before JSONB, row_after JSONB,
  changed_by TEXT NOT NULL DEFAULT current_user,
  changed_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE OR REPLACE FUNCTION fn_audit() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  INSERT INTO audit_log (table_name, op, row_before, row_after)
  VALUES (TG_TABLE_NAME, TG_OP,
          CASE WHEN TG_OP IN ('UPDATE','DELETE') THEN to_jsonb(OLD) END,
          CASE WHEN TG_OP IN ('INSERT','UPDATE') THEN to_jsonb(NEW) END);
  RETURN NULL;                              -- AFTER trigger: return value is ignored
END; $$;

CREATE TRIGGER trg_audit_employees AFTER INSERT OR UPDATE OR DELETE ON employees
FOR EACH ROW EXECUTE FUNCTION fn_audit();"""),
            MYSQL("""CREATE TRIGGER trg_emp_audit_upd AFTER UPDATE ON employees FOR EACH ROW
INSERT INTO audit_log (table_name, op, row_before, row_after, changed_by)
VALUES ('employees', 'UPDATE', JSON_OBJECT('id', OLD.id, 'salary', OLD.salary), JSON_OBJECT('id', NEW.id, 'salary', NEW.salary), CURRENT_USER());
-- MySQL needs one trigger per event (INSERT / UPDATE / DELETE)"""),
            H("3. Keep stock in sync when an order line is added"),
            PGSQL("""CREATE OR REPLACE FUNCTION fn_reduce_stock() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  UPDATE product SET stock = stock - NEW.quantity WHERE product_id = NEW.product_id;   -- CHECK (stock >= 0) rejects overselling
  RETURN NULL;
END; $$;
CREATE TRIGGER trg_order_item_stock AFTER INSERT ON order_item FOR EACH ROW EXECUTE FUNCTION fn_reduce_stock();"""),
            MYSQL("""DELIMITER $$
CREATE TRIGGER trg_order_item_stock AFTER INSERT ON order_item FOR EACH ROW
BEGIN
  UPDATE product SET stock = stock - NEW.quantity WHERE product_id = NEW.product_id;
END$$
DELIMITER ;"""),
            H("4. Enforce a rule across rows: max 5 open loans"),
            PGSQL("""CREATE OR REPLACE FUNCTION fn_max_open_loans() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  IF (SELECT COUNT(*) FROM loan WHERE member_id = NEW.member_id AND returned_on IS NULL) >= 5 THEN
    RAISE EXCEPTION 'member % already has 5 open loans', NEW.member_id;
  END IF;
  RETURN NEW;
END; $$;
CREATE TRIGGER trg_max_open_loans BEFORE INSERT ON loan FOR EACH ROW EXECUTE FUNCTION fn_max_open_loans();"""),
            MYSQL("""DELIMITER $$
CREATE TRIGGER trg_max_open_loans BEFORE INSERT ON loan FOR EACH ROW
BEGIN
  IF (SELECT COUNT(*) FROM loan WHERE member_id = NEW.member_id AND returned_on IS NULL) >= 5 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'member already has 5 open loans';
  END IF;
END$$
DELIMITER ;"""),
            NOTE("This rule is racy: two concurrent inserts can both see 4 loans. Lock the member row first (SELECT ... FOR UPDATE on member) or use SERIALIZABLE isolation. A good answer mentions this."),
            H("5. Soft delete: turn DELETE into an update"),
            PGSQL("""CREATE OR REPLACE FUNCTION fn_soft_delete() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  UPDATE employees SET deleted_at = now() WHERE id = OLD.id;
  RETURN NULL;                    -- cancel the physical delete
END; $$;
CREATE TRIGGER trg_soft_delete BEFORE DELETE ON employees FOR EACH ROW EXECUTE FUNCTION fn_soft_delete();"""),
            H("6. Writable view with INSTEAD OF"),
            PGSQL("""CREATE VIEW emp_directory AS SELECT e.id, e.name, d.name AS dept FROM employees e JOIN departments d ON d.id = e.dept_id;

CREATE OR REPLACE FUNCTION fn_emp_directory_insert() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  INSERT INTO employees (name, dept_id) VALUES (NEW.name, (SELECT id FROM departments WHERE name = NEW.dept));
  RETURN NEW;
END; $$;
CREATE TRIGGER trg_emp_directory_ins INSTEAD OF INSERT ON emp_directory FOR EACH ROW EXECUTE FUNCTION fn_emp_directory_insert();"""),
            H("Runnable: history table with SQLite triggers"),
            SQL("""CREATE TABLE emp_history (emp_id INTEGER, name TEXT, deleted_at TEXT DEFAULT CURRENT_TIMESTAMP);
CREATE TRIGGER trg_emp_deleted AFTER DELETE ON employees
FOR EACH ROW
BEGIN
  INSERT INTO emp_history (emp_id, name) VALUES (OLD.id, OLD.name);
END;
DELETE FROM employees WHERE id = 9;
SELECT emp_id, name FROM emp_history;""", "archive deleted rows", run=True),
            H("Statement-level trigger with transition tables (PostgreSQL)"),
            PGSQL("""CREATE OR REPLACE FUNCTION fn_log_bulk() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  INSERT INTO bulk_log (table_name, rows_affected) SELECT TG_TABLE_NAME, COUNT(*) FROM new_rows;
  RETURN NULL;
END; $$;
CREATE TRIGGER trg_bulk AFTER INSERT ON employees REFERENCING NEW TABLE AS new_rows
FOR EACH STATEMENT EXECUTE FUNCTION fn_log_bulk();"""),
            H("Managing triggers"),
            PGSQL("""SELECT tgname, tgenabled FROM pg_trigger WHERE tgrelid = 'employees'::regclass AND NOT tgisinternal;
ALTER TABLE employees DISABLE TRIGGER trg_audit_employees;
ALTER TABLE employees ENABLE TRIGGER ALL;
DROP TRIGGER trg_audit_employees ON employees;"""),
            MYSQL("""SHOW TRIGGERS LIKE 'employees';
DROP TRIGGER IF EXISTS trg_emp_audit_upd;"""),
            ASK("\"Write a trigger that logs salary changes.\" Know pattern 2 cold. Mention OLD vs NEW, that AFTER is right for logging, the row-level FOR EACH ROW, and the performance cost on bulk updates."),
        ],
        [
            Q("Best timing for a trigger that logs changes to an audit table:", ["BEFORE (to block the change)", "AFTER (the change succeeded)", "INSTEAD OF", "Neither"], 1, "Log only after the change is applied."),
            Q("A PostgreSQL BEFORE row trigger returning NULL:", ["Commits the row", "Skips the operation for that row", "Rolls back the transaction", "Raises an error"], 1, "Returning NULL cancels the row-level operation silently."),
            Q("In MySQL the standard way to reject a row from a trigger is:", ["RAISE EXCEPTION", "SIGNAL SQLSTATE '45000'", "ROLLBACK", "THROW"], 1, "SIGNAL raises a user-defined error. RAISE EXCEPTION is PostgreSQL."),
            Q("The 'max 5 open loans' trigger can still be violated because:", ["Triggers are optional", "Concurrent transactions may both count 4", "MySQL ignores triggers", "COUNT is slow"], 1, "Two sessions read before either writes, a race that needs locking or SERIALIZABLE."),
            Q("Automatic updated_at in MySQL needs no trigger because of:", ["ON UPDATE CURRENT_TIMESTAMP on the column", "A view", "A sequence", "An index"], 0, "The column definition does it declaratively."),
        ], star=True, kw="trigger patterns audit updated_at soft delete instead of view stock max loans history statement-level transition tables"))

    # ------------------------------------------------------------------ functions & procedures
    T.append(topic("procs-functions", GG, "Stored functions and procedures (PostgreSQL PL/pgSQL, MySQL)",
        "Reusable server-side code. Interviews ask for function vs procedure, parameters, control flow, error handling and one small example.",
        [
            H("Function vs procedure"),
            TBL(["", "Function", "Procedure"],
                ["Returns", "A value (scalar, row, or table)", "Nothing (OUT / INOUT parameters instead)"],
                ["Called with", "SELECT fn(...)  or inside expressions", "CALL proc(...)"],
                ["Use inside a query", "Yes", "No"],
                ["Transaction control (COMMIT / ROLLBACK)", "No", "PostgreSQL 11+: yes (when not already inside a transaction block). MySQL: yes"],
                ["Typical use", "Computations, lookups, trigger bodies", "Multi-step workflows, batch jobs, transfers"]),
            H("PostgreSQL: scalar function"),
            PGSQL("""CREATE OR REPLACE FUNCTION annual_bonus(p_salary NUMERIC, p_years INT)
RETURNS NUMERIC
LANGUAGE plpgsql IMMUTABLE AS $$
DECLARE
  pct NUMERIC;
BEGIN
  pct := CASE WHEN p_years >= 5 THEN 0.15
              WHEN p_years >= 2 THEN 0.10
              ELSE 0.05 END;
  RETURN ROUND(p_salary * pct, 2);
END;
$$;

SELECT name, annual_bonus(salary, 3) AS bonus FROM employees;"""),
            PGSQL("""-- table-returning function in plain SQL
CREATE FUNCTION dept_employees(p_dept INT)
RETURNS TABLE (emp_id INT, emp_name TEXT, salary INT)
LANGUAGE sql STABLE AS $$
  SELECT id, name, salary FROM employees WHERE dept_id = p_dept ORDER BY salary DESC
$$;
SELECT * FROM dept_employees(2);"""),
            PGSQL("""-- OUT parameters and RETURN QUERY
CREATE FUNCTION salary_stats(p_dept INT, OUT lowest INT, OUT highest INT, OUT average NUMERIC)
LANGUAGE sql AS $$ SELECT MIN(salary), MAX(salary), AVG(salary) FROM employees WHERE dept_id = p_dept $$;
SELECT * FROM salary_stats(2);"""),
            H("PostgreSQL: procedure"),
            PGSQL("""CREATE OR REPLACE PROCEDURE transfer(p_from BIGINT, p_to BIGINT, p_amount NUMERIC)
LANGUAGE plpgsql AS $$
BEGIN
  IF p_amount <= 0 THEN
    RAISE EXCEPTION 'amount must be positive';
  END IF;
  UPDATE account SET balance = balance - p_amount WHERE account_no = p_from;
  IF NOT FOUND THEN RAISE EXCEPTION 'source account % does not exist', p_from; END IF;
  UPDATE account SET balance = balance + p_amount WHERE account_no = p_to;
  IF NOT FOUND THEN RAISE EXCEPTION 'target account % does not exist', p_to; END IF;
END;
$$;

CALL transfer(100001, 100002, 500);       -- an exception rolls back both updates"""),
            H("PL/pgSQL building blocks"),
            PGSQL("""DO $$                                      -- anonymous block
DECLARE
  v_count INT;
  r RECORD;
BEGIN
  SELECT COUNT(*) INTO v_count FROM employees;                   -- query into variable
  IF v_count > 100 THEN RAISE NOTICE 'big'; ELSIF v_count > 10 THEN RAISE NOTICE 'medium'; ELSE RAISE NOTICE 'small'; END IF;

  FOR r IN SELECT id, name FROM employees WHERE dept_id = 2 LOOP          -- loop over a query
    RAISE NOTICE '% %', r.id, r.name;
  END LOOP;

  FOR i IN 1..3 LOOP RAISE NOTICE 'i=%', i; END LOOP;                     -- counted loop
  WHILE v_count > 0 LOOP v_count := v_count - 5; END LOOP;               -- while loop
  CASE WHEN v_count < 0 THEN RAISE NOTICE 'negative'; ELSE NULL; END CASE;
EXCEPTION
  WHEN unique_violation THEN RAISE NOTICE 'duplicate key';
  WHEN division_by_zero THEN RAISE NOTICE 'divide by zero';
  WHEN OTHERS THEN RAISE NOTICE 'error: %', SQLERRM;
END $$;"""),
            UL("Variables: DECLARE name type; assign with := or SELECT ... INTO.",
               "FOUND is set by the last statement; GET DIAGNOSTICS n = ROW_COUNT.",
               "RAISE NOTICE / WARNING / EXCEPTION for messages and errors.",
               "Volatility markers: IMMUTABLE (same input, same output), STABLE (consistent within a statement), VOLATILE (default). Let the planner optimize.",
               "SECURITY DEFINER runs with the owner's privileges (set search_path!)."),
            H("MySQL: function and procedure"),
            MYSQL("""DELIMITER $$
CREATE FUNCTION annual_bonus(p_salary DECIMAL(12,2), p_years INT)
RETURNS DECIMAL(12,2) DETERMINISTIC
BEGIN
  DECLARE pct DECIMAL(4,2);
  IF p_years >= 5 THEN SET pct = 0.15;
  ELSEIF p_years >= 2 THEN SET pct = 0.10;
  ELSE SET pct = 0.05;
  END IF;
  RETURN ROUND(p_salary * pct, 2);
END$$

CREATE PROCEDURE raise_dept_salary(IN p_dept INT, IN p_pct DECIMAL(5,2), OUT p_rows INT)
BEGIN
  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    ROLLBACK;
    RESIGNAL;
  END;
  START TRANSACTION;
  UPDATE employees SET salary = salary * (1 + p_pct / 100) WHERE dept_id = p_dept;
  SET p_rows = ROW_COUNT();
  COMMIT;
END$$
DELIMITER ;

CALL raise_dept_salary(2, 5, @n);
SELECT @n;                       -- rows affected
SELECT name, annual_bonus(salary, 3) FROM employees;"""),
            TBL(["Parameter modes", "Meaning"],
                ["IN", "Value passed in (default)"],
                ["OUT", "Value returned to the caller"],
                ["INOUT", "Passed in, modified, passed back"]),
            H("Error handling compared"),
            TBL(["", "PostgreSQL", "MySQL"],
                ["Catch", "BEGIN ... EXCEPTION WHEN condition THEN ... END", "DECLARE {EXIT | CONTINUE} HANDLER FOR SQLEXCEPTION | SQLSTATE '23000' | NOT FOUND"],
                ["Raise", "RAISE EXCEPTION 'msg %', val", "SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'msg'"],
                ["Re-raise", "RAISE;", "RESIGNAL;"],
                ["Error text / code", "SQLERRM, SQLSTATE", "GET DIAGNOSTICS CONDITION 1 ... MESSAGE_TEXT"]),
            PG("A PostgreSQL EXCEPTION block opens a subtransaction (a savepoint), so it has a cost; do not wrap tight loops needlessly."),
            H("Pros and cons"),
            UL("**Pros:** fewer round trips, logic near the data, reuse, permission boundary (GRANT EXECUTE only), precompiled/cached plans.",
               "**Cons:** harder to version-control and test, vendor-specific language (hard to migrate), business logic hidden from application code, debugging is clumsy."),
            SQL("-- not runnable here: SQLite has no stored routines.\n-- Use CREATE FUNCTION (PostgreSQL), CREATE PROCEDURE / FUNCTION (MySQL).", "SQLite note"),
            ASK("\"Function vs stored procedure?\" Function returns a value and can be used inside SELECT; procedure is invoked with CALL, can have OUT parameters and (in PostgreSQL 11+/MySQL) can control transactions."),
        ],
        [
            Q("A PostgreSQL stored procedure is executed with:", ["SELECT proc()", "CALL proc()", "EXEC proc", "RUN proc"], 1, "Functions are called in queries; procedures with CALL."),
            Q("Which can be used directly inside a SELECT list?", ["Procedure", "Function", "Trigger", "Cursor"], 1, "Functions return values usable in expressions."),
            Q("MySQL delimiter is changed in the shell because:", ["The body contains semicolons", "MySQL cannot parse BEGIN", "To enable triggers", "To speed up compile"], 0, "Otherwise the shell ends the statement at the first semicolon inside the body."),
            Q("Which marks a PostgreSQL function as always returning the same result for the same arguments?", ["VOLATILE", "STABLE", "IMMUTABLE", "STRICT"], 2, "IMMUTABLE lets the planner pre-evaluate and index on it."),
            Q("In MySQL, an exit handler for any SQL error is declared:", ["ON ERROR EXIT", "DECLARE EXIT HANDLER FOR SQLEXCEPTION", "TRY ... CATCH", "EXCEPTION WHEN OTHERS"], 1, "EXCEPTION WHEN OTHERS is PostgreSQL."),
        ], star=True, kw="stored procedure function plpgsql create function call out parameter exception handler delimiter"))

    # ------------------------------------------------------------------ cursors and dynamic sql
    T.append(topic("cursors-dynamic", GG, "Cursors, prepared statements and dynamic SQL",
        "Row-by-row processing and statements built at runtime: both are tools of last resort, and both attract interview questions.",
        [
            H("Cursor"),
            P("A cursor is a handle on a query result that lets procedural code fetch rows one at a time. Lifecycle: **DECLARE, OPEN, FETCH, CLOSE**."),
            PGSQL("""DO $$
DECLARE
  cur CURSOR FOR SELECT id, salary FROM employees ORDER BY id;
  rec RECORD;
BEGIN
  OPEN cur;
  LOOP
    FETCH cur INTO rec;
    EXIT WHEN NOT FOUND;
    RAISE NOTICE 'employee % earns %', rec.id, rec.salary;
  END LOOP;
  CLOSE cur;
END $$;
-- much simpler: an implicit cursor
-- FOR rec IN SELECT id, salary FROM employees LOOP ... END LOOP;"""),
            MYSQL("""DELIMITER $$
CREATE PROCEDURE print_salaries()
BEGIN
  DECLARE done INT DEFAULT 0;
  DECLARE v_id INT; DECLARE v_sal INT;
  DECLARE cur CURSOR FOR SELECT id, salary FROM employees;
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
  OPEN cur;
  read_loop: LOOP
    FETCH cur INTO v_id, v_sal;
    IF done = 1 THEN LEAVE read_loop; END IF;
    SELECT v_id, v_sal;
  END LOOP;
  CLOSE cur;
END$$
DELIMITER ;"""),
            UL("**Prefer set-based SQL.** One UPDATE over all rows is orders of magnitude faster than looping with a cursor.",
               "Good cursor uses: calling a procedure per row, processing huge results in batches, administration scripts.",
               "PostgreSQL also has client-side/server-side cursors: DECLARE c CURSOR FOR ...; FETCH 100 FROM c; for paging big results (WITH HOLD to survive commits).",
               "Types: forward-only vs scrollable; read-only vs updatable (WHERE CURRENT OF)."),
            H("Prepared statements"),
            P("The SQL text is parsed and planned once, then executed many times with different parameters. Benefits: speed for repeated queries and, more importantly, **protection from SQL injection** because parameters are never parsed as SQL."),
            PGSQL("""PREPARE emp_by_dept (INT) AS SELECT name FROM employees WHERE dept_id = $1;
EXECUTE emp_by_dept(2);
DEALLOCATE emp_by_dept;"""),
            MYSQL("""PREPARE stmt FROM 'SELECT name FROM employees WHERE dept_id = ?';
SET @d = 2;
EXECUTE stmt USING @d;
DEALLOCATE PREPARE stmt;"""),
            H("Dynamic SQL"),
            P("Dynamic SQL builds the statement text at runtime (table or column names chosen by a variable). Identifiers cannot be bound as parameters, so quote them properly."),
            PGSQL("""CREATE OR REPLACE FUNCTION count_rows(p_table TEXT) RETURNS BIGINT LANGUAGE plpgsql AS $$
DECLARE n BIGINT;
BEGIN
  EXECUTE format('SELECT COUNT(*) FROM %I', p_table) INTO n;                 -- %I quotes an identifier safely
  RETURN n;
END; $$;

-- values go through USING, never through string concatenation
EXECUTE format('SELECT name FROM %I WHERE id = $1', 'employees') USING 3;"""),
            MYSQL("""SET @sql = CONCAT('SELECT COUNT(*) FROM ', 'employees');    -- identifier must be validated by you (whitelist!)
PREPARE s FROM @sql; EXECUTE s; DEALLOCATE PREPARE s;"""),
            H("SQL injection in one picture"),
            TXT("""Vulnerable app code (string building):
  query = "SELECT * FROM users WHERE name = '" + input + "'"
  input = ' OR '1'='1          ->  SELECT * FROM users WHERE name = '' OR '1'='1'   (returns everyone)
  input = '; DROP TABLE users; --   ->  stacked statement

Fix: parameterised query
  cursor.execute("SELECT * FROM users WHERE name = %s", (input,))      # driver sends the value separately"""),
            UL("Always use parameter placeholders (?, $1, %s, named) from the application driver.",
               "Whitelist dynamic identifiers (table or column names) against a fixed list.",
               "Least privilege: the app account should not own the schema or DROP tables.",
               "ORMs parameterise for you, but raw-SQL escape hatches do not."),
            ASK("\"What is SQL injection and how do you prevent it?\" Untrusted input changes the meaning of the query. Prevent with parameterised/prepared statements, input validation, least-privilege accounts, and never concatenating user input into SQL."),
        ],
        [
            Q("The correct order of cursor operations is:", ["OPEN, DECLARE, FETCH, CLOSE", "DECLARE, OPEN, FETCH, CLOSE", "FETCH, OPEN, DECLARE, CLOSE", "DECLARE, FETCH, OPEN, CLOSE"], 1, "Declare it, open it, fetch rows, close it."),
            Q("Row-by-row cursor loops are usually:", ["Faster than set-based SQL", "Slower than a single set-based statement", "Required for UPDATE", "Illegal"], 1, "Set-based operations let the optimizer work on all rows at once."),
            Q("Prepared statements help prevent SQL injection because:", ["They encrypt data", "Parameters are sent separately and never parsed as SQL", "They block DROP", "They hash inputs"], 1, "The structure is fixed before values are supplied."),
            Q("Table names in dynamic SQL cannot be bound as parameters, so you should:", ["Concatenate raw input", "Quote with format('%I') / whitelist", "Skip validation", "Use LIKE"], 1, "Quote or whitelist identifiers."),
            Q("In a MySQL cursor loop, the NOT FOUND handler is used to:", ["Open the cursor", "Detect end of rows", "Reset variables", "Commit"], 1, "It sets a flag when FETCH has no more rows."),
        ], kw="cursor declare open fetch close prepare execute dynamic sql injection parameterised format"))

    # ------------------------------------------------------------------ DCL / security
    T.append(topic("dcl-security", GG, "Users, roles, GRANT / REVOKE, row-level security",
        "Who can do what. Expect questions on GRANT syntax, roles, least privilege, and how to give analysts read-only access.",
        [
            H("Privileges"),
            TBL(["Privilege", "On", "Allows"],
                ["SELECT, INSERT, UPDATE, DELETE", "table / column", "Read and change data"],
                ["REFERENCES", "table", "Create a foreign key to it"],
                ["TRIGGER, TRUNCATE (PostgreSQL)", "table", "Create triggers, truncate"],
                ["EXECUTE", "function / procedure", "Call it"],
                ["USAGE", "schema, sequence", "Use objects in the schema; call nextval"],
                ["CREATE", "database / schema", "Create objects"],
                ["CONNECT", "database", "Connect to it"],
                ["ALL PRIVILEGES", "any", "Everything on that object"]),
            H("PostgreSQL"),
            PGSQL("""CREATE ROLE app_read NOLOGIN;                                   -- a group role
GRANT CONNECT ON DATABASE shop TO app_read;
GRANT USAGE ON SCHEMA public TO app_read;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO app_read;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO app_read;   -- future tables too

CREATE ROLE alice LOGIN PASSWORD 'use-a-secret-manager';
GRANT app_read TO alice;                                          -- membership

GRANT INSERT, UPDATE ON orders TO app_writer;
GRANT SELECT (id, name, dept_id) ON employees TO analyst;         -- column-level: salary stays hidden
REVOKE ALL ON customer FROM PUBLIC;
REVOKE INSERT ON orders FROM app_writer;
GRANT app_read TO alice WITH ADMIN OPTION;                        -- she may grant the role onward
\\du            -- list roles (psql)
\\dp orders     -- list privileges (psql)"""),
            MYSQL("""CREATE USER 'alice'@'%' IDENTIFIED BY 'use-a-secret-manager';
CREATE ROLE 'app_read';
GRANT SELECT ON shop.* TO 'app_read';
GRANT 'app_read' TO 'alice'@'%';
SET DEFAULT ROLE 'app_read' TO 'alice'@'%';
GRANT SELECT (id, name) ON shop.employees TO 'analyst'@'%';
GRANT SELECT ON shop.* TO 'bob'@'localhost' WITH GRANT OPTION;
REVOKE INSERT ON shop.orders FROM 'alice'@'%';
SHOW GRANTS FOR 'alice'@'%';
DROP USER 'alice'@'%';"""),
            MY("MySQL accounts are user@host pairs. 'alice'@'%' and 'alice'@'localhost' are different accounts."),
            H("Principle of least privilege"),
            UL("Application account: DML on its tables only. Never superuser, never schema owner.",
               "Migrations account: DDL rights, used only during deployments.",
               "Analysts: read-only role, ideally through views that hide sensitive columns.",
               "Revoke default PUBLIC rights; rotate passwords; use TLS."),
            H("Views as a security layer"),
            SQL("""CREATE VIEW employee_public AS SELECT id, name, dept_id, city FROM employees;     -- no salary
-- then: GRANT SELECT ON employee_public TO analyst;   and keep the base table closed
SELECT * FROM employee_public LIMIT 3;""", run=True),
            H("Row-level security (PostgreSQL)"),
            PGSQL("""ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
CREATE POLICY own_orders ON orders
  USING (customer_id = current_setting('app.customer_id')::bigint)          -- which rows are visible
  WITH CHECK (customer_id = current_setting('app.customer_id')::bigint);    -- which rows can be written

-- the app does:  SET app.customer_id = '42';  SELECT * FROM orders;   -- only customer 42's rows"""),
            MY("MySQL has no built-in row-level security; use views with WHERE clauses plus definer rights, or filter in the application."),
            H("Other security basics"),
            UL("Encryption in transit (TLS) and at rest; hash passwords in the app (bcrypt/argon2), never store plain text in the database.",
               "Auditing: log DDL and failed logins; PostgreSQL pgaudit extension; MySQL audit plugin.",
               "SQL injection: see the prepared statements topic.",
               "pg_hba.conf (PostgreSQL) controls who may connect from where and how they authenticate."),
            ASK("\"How would you give a reporting team read-only access without exposing salaries?\" Create a role with SELECT only on a view or on specific columns, grant the role to the users, revoke access to the base table."),
        ],
        [
            Q("Which statement removes a privilege?", ["DENY", "REVOKE", "DROP GRANT", "REMOVE"], 1, "REVOKE is the standard command."),
            Q("Column-level read access in PostgreSQL:", ["GRANT SELECT (id, name) ON t TO r", "GRANT SELECT ON t.id TO r", "GRANT COLUMNS ON t", "Not possible"], 0, "List the columns in parentheses after the privilege."),
            Q("WITH GRANT OPTION (or WITH ADMIN OPTION for roles) lets the grantee:", ["Drop the table", "Pass the privilege on to others", "Bypass constraints", "Log in as owner"], 1, "It delegates granting rights."),
            Q("Which database has built-in row-level security policies?", ["MySQL", "PostgreSQL", "SQLite", "None"], 1, "PostgreSQL CREATE POLICY."),
            Q("Least privilege means:", ["Everyone gets ALL PRIVILEGES", "Each account gets only the permissions it needs", "No passwords", "Only superusers log in"], 1, "Limit the blast radius of mistakes and breaches."),
        ], kw="grant revoke role user privilege permissions row level security policy least privilege view"))

    # ------------------------------------------------------------------ partitioning
    T.append(topic("partitioning", GG, "Table partitioning (range, list, hash) in PostgreSQL and MySQL",
        "Splitting one huge table into smaller physical pieces while queries still see one table.",
        [
            P("Benefits: **partition pruning** (queries touching one month read only that partition), fast bulk deletes (drop a partition instead of DELETE), smaller indexes, easier archiving."),
            TBL(["Method", "Rule", "Example key"],
                ["RANGE", "Each partition covers an interval", "order date by month or year"],
                ["LIST", "Each partition holds listed values", "country, region"],
                ["HASH", "hash(key) mod N spreads rows evenly", "customer_id"]),
            PGSQL("""CREATE TABLE measurement (
  city_id  INT  NOT NULL,
  logdate  DATE NOT NULL,
  temp     INT,
  PRIMARY KEY (city_id, logdate)                -- the PK must include the partition key
) PARTITION BY RANGE (logdate);

CREATE TABLE measurement_2026_h1 PARTITION OF measurement FOR VALUES FROM ('2026-01-01') TO ('2026-07-01');
CREATE TABLE measurement_2026_h2 PARTITION OF measurement FOR VALUES FROM ('2026-07-01') TO ('2027-01-01');
CREATE TABLE measurement_default PARTITION OF measurement DEFAULT;

-- list and hash
CREATE TABLE customer_region (id INT, region TEXT, PRIMARY KEY (id, region)) PARTITION BY LIST (region);
CREATE TABLE cr_south PARTITION OF customer_region FOR VALUES IN ('KA','TN','KL');
CREATE TABLE events (id BIGINT, payload JSONB, PRIMARY KEY (id)) PARTITION BY HASH (id);
CREATE TABLE events_p0 PARTITION OF events FOR VALUES WITH (MODULUS 4, REMAINDER 0);

-- maintenance
ALTER TABLE measurement DETACH PARTITION measurement_2026_h1;    -- then archive or DROP it instantly
EXPLAIN SELECT * FROM measurement WHERE logdate = '2026-08-01';   -- should scan only h2"""),
            MYSQL("""CREATE TABLE sales (
  id INT NOT NULL, sold_on DATE NOT NULL, amount DECIMAL(10,2),
  PRIMARY KEY (id, sold_on)
)
PARTITION BY RANGE (YEAR(sold_on)) (
  PARTITION p2025 VALUES LESS THAN (2026),
  PARTITION p2026 VALUES LESS THAN (2027),
  PARTITION pmax  VALUES LESS THAN MAXVALUE
);
ALTER TABLE sales DROP PARTITION p2025;"""),
            MY("MySQL partitioned InnoDB tables cannot have foreign keys (neither as parent nor child), and every unique key must include the partitioning column."),
            H("Partitioning vs sharding vs replication"),
            TBL(["", "What", "Scope"],
                ["Partitioning", "Split a table inside one database server", "One server"],
                ["Sharding", "Split data across several servers by a shard key", "Many servers (application or middleware routing)"],
                ["Replication", "Copies of the same data on other servers", "Read scale and failover"]),
            ASK("\"When do you partition a table?\" When it is very large and queries or maintenance naturally target one slice (time ranges, tenants), so pruning and partition drops pay off."),
        ],
        [
            Q("The main performance idea behind partitioning is:", ["Compression", "Partition pruning", "Encryption", "Locking"], 1, "The planner skips partitions that cannot contain matching rows."),
            Q("In PostgreSQL a primary key on a partitioned table must:", ["Be a single column", "Include the partition key", "Be a UUID", "Not exist"], 1, "Uniqueness is enforced per partition, so the key must include the partitioning columns."),
            Q("Quickest way to remove a year of old data from a range-partitioned table:", ["DELETE WHERE year = X", "Drop or detach that partition", "TRUNCATE the parent", "VACUUM"], 1, "Dropping a partition is nearly instant."),
            Q("Which partitioning type spreads rows evenly without ranges?", ["RANGE", "LIST", "HASH", "DEFAULT"], 2, "HASH distributes by hash modulo N."),
            Q("Sharding differs from partitioning because it:", ["Uses one server", "Spreads data over multiple servers", "Needs no key", "Removes indexes"], 1, "Shards live on different machines."),
        ], kw="partition range list hash prune sharding detach"))

    return T
