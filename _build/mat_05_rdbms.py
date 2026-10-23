"""Study guide, part 5: PostgreSQL and MySQL essentials, comparison, JSON, metadata, operations, design practice, interview Q&A."""
from mat_common import *

GD = "D. Designing tables (DDL, constraints, scenarios)"
GH = "H. PostgreSQL, MySQL and interview answers"


def build():
    T = []

    # ------------------------------------------------------------------ design best practices
    T.append(topic("design-practices", GD, "Schema design best practices and hierarchy models",
        "The checklist for 'design the schema for X' and the review questions that follow: naming, audit columns, soft delete, multi-tenancy, trees, migrations.",
        [
            H("Conventions interviewers like to hear"),
            UL("**Naming:** snake_case, singular table names (or plural, but consistent), primary key id or table_id, foreign key named parent_id, boolean columns as is_/has_. Avoid reserved words (order, user, group).",
               "**Audit columns:** created_at, updated_at (and created_by when needed) on every table.",
               "**Soft delete:** deleted_at TIMESTAMPTZ NULL or is_active; combine with a partial unique index (UNIQUE (email) WHERE deleted_at IS NULL).",
               "**Constraints first:** NOT NULL by default, CHECKs for ranges and states, FKs for all relationships. The database is the last line of defence.",
               "**Indexes:** every FK, every frequent filter, composite in the right order, partial for hot subsets.",
               "**Money** as NUMERIC or integer minor units, **time** as UTC TIMESTAMPTZ, **ids** as BIGINT identity or UUID.",
               "**Never** store comma-separated lists, repeated columns (phone1, phone2), or derived values that go stale."),
            H("Anti-patterns"),
            TBL(["Anti-pattern", "Problem", "Better"],
                ["Comma-separated ids in a column", "Cannot join, index or constrain", "Junction table"],
                ["EAV (entity, attribute, value)", "No types, no constraints, slow queries", "Real columns, or JSONB for the truly dynamic part"],
                ["One giant table for everything", "Sparse NULLs, unclear meaning", "Normalize; subtype tables"],
                ["Polymorphic FK (target_type + target_id)", "No referential integrity", "Separate FK columns with a CHECK, or one junction table per type"],
                ["Storing files as BLOB rows", "Bloats backups", "Object storage + URL column"],
                ["Using FLOAT for money", "Rounding errors", "NUMERIC(12,2)"],
                ["Natural key as the only PK that can change", "Cascading updates", "Surrogate PK + UNIQUE natural key"],
                ["SELECT * in application code", "Breaks when columns change; extra I/O", "List columns"]),
            H("Multi-tenant design"),
            UL("**Shared tables with tenant_id** on every row: cheapest. Make tenant_id part of unique keys and composite FKs; enforce isolation with row-level security (PostgreSQL).",
               "**Schema per tenant:** stronger isolation, harder migrations.",
               "**Database per tenant:** strongest isolation, highest operating cost."),
            H("Hierarchies (trees) in SQL"),
            TBL(["Model", "Idea", "Read subtree", "Move subtree", "Notes"],
                ["Adjacency list", "parent_id column", "Recursive CTE", "Easy (one update)", "Default choice; simple"],
                ["Path enumeration", "path = '/1/4/9/'", "LIKE '/1/4/%'", "Rewrite paths", "Fast reads; PostgreSQL ltree type"],
                ["Nested sets", "left/right numbers", "Range query", "Expensive renumbering", "Read-heavy, rarely changing trees"],
                ["Closure table", "All ancestor-descendant pairs in a table", "Simple join", "Moderate", "Flexible, extra table"]),
            H("Schema changes without downtime (expand and contract)"),
            OL("**Expand:** add the new column or table nullable; deploy code that writes both.",
               "**Backfill** old rows in small batches.",
               "**Switch** reads to the new structure.",
               "**Contract:** drop the old column once nothing uses it.",
               "Run migrations with a tool (Flyway, Liquibase, Alembic, Prisma Migrate), always in version control. Create indexes CONCURRENTLY in PostgreSQL; know that some ALTERs lock the table."),
            H("Pagination"),
            SQL("""-- OFFSET pagination: simple but slow for deep pages (it reads and discards the skipped rows)
SELECT id, name FROM employees ORDER BY id LIMIT 3 OFFSET 6;
-- keyset (seek) pagination: constant speed, uses the index
SELECT id, name FROM employees WHERE id > 6 ORDER BY id LIMIT 3;""", run=True),
            ASK("\"Design the schema for X\" is graded on process: clarify requirements, list entities, draw relationships and cardinality, write DDL with keys and constraints, add indexes for the main queries, then discuss growth (partitioning, caching) and edge cases (deletes, history, concurrency)."),
        ],
        [
            Q("Why is a comma-separated list of ids in one column bad?", ["It is too long", "You cannot enforce FKs, index it or join cleanly", "It uses too much memory", "Only MySQL forbids it"], 1, "It violates 1NF and loses integrity and query power."),
            Q("Best way to keep email unique only among non-deleted rows in PostgreSQL:", ["UNIQUE (email)", "Partial unique index WHERE deleted_at IS NULL", "CHECK", "Trigger only"], 1, "A partial unique index ignores soft-deleted rows."),
            Q("Keyset pagination is preferred for deep pages because:", ["It is shorter", "It does not read and discard skipped rows", "It uses OFFSET", "It sorts less"], 1, "WHERE id > last_seen uses the index to jump straight to the page."),
            Q("Which tree model makes 'move a subtree' cheapest?", ["Nested sets", "Path enumeration", "Adjacency list", "Closure table"], 2, "Change one parent_id."),
            Q("In expand-and-contract migrations the first step is:", ["Drop the old column", "Add the new structure alongside the old one", "Lock the table", "Rename everything"], 1, "Expand first so old and new code can run together."),
        ], star=True, kw="design best practices naming soft delete multi tenant tree adjacency closure nested set path migration expand contract pagination anti pattern eav"))

    # ------------------------------------------------------------------ PostgreSQL essentials
    T.append(topic("postgres-essentials", GH, "PostgreSQL essentials: architecture, psql, MVCC, VACUUM, extensions",
        "You work with PostgreSQL, so expect to be asked how it works internally and how you operate it.",
        [
            H("What it is"),
            P("PostgreSQL is an open-source object-relational database: full ACID, MVCC, rich types (arrays, JSONB, ranges, enums, geometric, network), extensibility (extensions, custom types, operators, index methods), standards-heavy SQL (CTEs, window functions, LATERAL, MERGE since 15), and procedural languages (PL/pgSQL, PL/Python...). Default port 5432."),
            H("Architecture"),
            UL("**Postmaster** process listens and forks one **backend process per connection**. That is why connection pooling (PgBouncer) matters at scale.",
               "**Shared buffers** (page cache), **WAL buffers**, **work_mem** (per sort/hash operation, per connection), **maintenance_work_mem**, **effective_cache_size** (planner hint).",
               "Background workers: **checkpointer**, **background writer**, **WAL writer**, **autovacuum launcher/workers**, **stats collector**, **WAL sender/receiver** (replication).",
               "Storage: each table is a **heap** of 8 KB pages; indexes are separate structures pointing to tuple ids (ctid). TOAST stores large values out of line.",
               "Hierarchy: cluster → databases → schemas → tables. A cluster is one running server instance."),
            H("MVCC, VACUUM and bloat"),
            UL("An UPDATE writes a **new row version**; the old one stays (xmin = creating transaction, xmax = deleting transaction). A DELETE just marks xmax.",
               "Old versions that no snapshot needs are **dead tuples**. **VACUUM** reclaims their space for reuse; **autovacuum** runs it automatically. **VACUUM FULL** rewrites the table (exclusive lock).",
               "**ANALYZE** refreshes planner statistics. Autovacuum does both.",
               "**Bloat** = dead space. Causes: long-running transactions that hold back cleanup, heavy updates, autovacuum too slow.",
               "**Transaction id wraparound:** ids are 32-bit; VACUUM freezes old rows to avoid it. Never disable autovacuum.",
               "**HOT updates** avoid index writes when no indexed column changes and the page has room (fillfactor)."),
            SQL("""-- the same idea in SQLite terms is not available; in PostgreSQL:
-- SELECT xmin, xmax, ctid, * FROM employees LIMIT 3;
-- SELECT relname, n_live_tup, n_dead_tup, last_autovacuum FROM pg_stat_user_tables ORDER BY n_dead_tup DESC;""", "inspect row versions and dead tuples"),
            H("psql meta-commands"),
            TBL(["Command", "Does"],
                ["\\l", "list databases"],
                ["\\c dbname", "connect to a database"],
                ["\\dt   \\dt schema.*", "list tables"],
                ["\\d table", "describe columns, indexes, constraints, triggers"],
                ["\\d+ table", "same plus size and storage"],
                ["\\dn   \\du   \\df   \\dv   \\di   \\dT", "schemas, roles, functions, views, indexes, types"],
                ["\\x", "toggle expanded (vertical) output"],
                ["\\timing", "show query time"],
                ["\\i file.sql", "run a script"],
                ["\\copy t FROM 'f.csv' CSV HEADER", "client-side bulk import (COPY runs on the server)"],
                ["\\set / \\echo / \\g / \\watch 5", "variables, print, run, repeat every 5 s"],
                ["\\q", "quit"]),
            H("Schemas and search_path"),
            PGSQL("""CREATE SCHEMA hr;
CREATE TABLE hr.employee (id INT PRIMARY KEY);
SHOW search_path;                               -- "$user", public
SET search_path TO hr, public;                  -- unqualified names now look in hr first
ALTER ROLE app SET search_path = hr, public;"""),
            H("Extensions worth naming"),
            TBL(["Extension", "Adds"],
                ["pg_stat_statements", "Per-query statistics: find the slowest queries"],
                ["pgcrypto", "Hashing, encryption, gen_random_uuid() (built in from 13)"],
                ["uuid-ossp", "UUID generators"],
                ["pg_trgm", "Trigram similarity; fast LIKE '%x%' with GIN index"],
                ["btree_gist / btree_gin", "Use scalar types in GiST/GIN (exclusion constraints)"],
                ["PostGIS", "Geospatial types and queries"],
                ["tablefunc", "crosstab pivots"],
                ["postgres_fdw", "Query other PostgreSQL servers"],
                ["pgvector", "Vector similarity search for embeddings"],
                ["timescaledb", "Time-series partitioning and compression"]),
            PGSQL("CREATE EXTENSION IF NOT EXISTS pg_trgm;\nCREATE INDEX idx_name_trgm ON employees USING gin (name gin_trgm_ops);\nSELECT name FROM employees WHERE name ILIKE '%ish%';   -- now index-assisted"),
            H("Distinctive features to mention"),
            UL("Transactional DDL (rollback a CREATE TABLE).",
               "Rich types: arrays, ranges, enums, domains (CREATE DOMAIN), composite types, JSONB, hstore, network types.",
               "Index types: B-tree, Hash, GIN, GiST, SP-GiST, BRIN; partial, expression, covering (INCLUDE), multicolumn.",
               "Declarative partitioning, table inheritance, foreign data wrappers.",
               "Full-text search (tsvector, tsquery, to_tsvector, ts_rank).",
               "LISTEN / NOTIFY for lightweight pub/sub; advisory locks (pg_advisory_lock).",
               "Row-level security, SERIALIZABLE snapshot isolation (SSI), logical replication, generated columns, MERGE (15), SQL/JSON (16/17)."),
            PGSQL("""-- handy PostgreSQL-only snippets
SELECT generate_series(1, 5);
SELECT DISTINCT ON (dept_id) dept_id, name, salary FROM employees ORDER BY dept_id, salary DESC;
SELECT name FROM employees WHERE name ~* '^a.*a$';
SELECT COUNT(*) FILTER (WHERE salary > 100000) FROM employees;
SELECT * FROM employees WHERE id = ANY (ARRAY[1,2,3]);
SELECT string_agg(name, ', ' ORDER BY name) FROM employees;
EXPLAIN (ANALYZE, BUFFERS, VERBOSE) SELECT * FROM employees WHERE dept_id = 2;"""),
            ASK("\"How does PostgreSQL implement MVCC?\" Each row has xmin/xmax; updates create new tuple versions; readers use a snapshot of committed transaction ids; VACUUM later removes dead versions."),
        ],
        [
            Q("PostgreSQL handles each client connection with:", ["A thread in one process", "A separate backend process", "A coroutine", "A shared singleton"], 1, "Process-per-connection; hence pooling."),
            Q("Dead tuples are cleaned up by:", ["ANALYZE", "VACUUM", "REINDEX", "CHECKPOINT"], 1, "VACUUM reclaims space from dead row versions."),
            Q("psql command to describe a table:", ["\\l", "\\dt", "\\d table", "\\x"], 2, "\\d shows columns, indexes and constraints."),
            Q("Which extension helps find the slowest queries?", ["pg_trgm", "pg_stat_statements", "postgis", "tablefunc"], 1, "It aggregates per-statement timing."),
            Q("Setting search_path controls:", ["Where backups are written", "Which schemas are searched for unqualified names", "Index lookup order", "Replication targets"], 1, "Name resolution for unqualified objects."),
            Q("What can PostgreSQL do that MySQL cannot?", ["Transactional DDL", "Primary keys", "Joins", "Views"], 0, "PostgreSQL can roll back DDL; MySQL commits it implicitly."),
        ], star=True, kw="postgresql postgres psql mvcc vacuum autovacuum bloat extension search_path schema pg_stat_statements wal architecture"))

    # ------------------------------------------------------------------ MySQL essentials
    T.append(topic("mysql-essentials", GH, "MySQL essentials: engines, sql_mode, InnoDB, quirks",
        "You learned MySQL, so keep it sharp. The key ideas: pluggable storage engines, InnoDB internals, strict mode and the quirks interviewers love.",
        [
            H("Architecture"),
            UL("**Server layer:** connection handling (thread per connection), parser, optimizer, caches. **Storage engine layer:** pluggable engines.",
               "Default port 3306. Hierarchy: server → databases (= schemas) → tables.",
               "**InnoDB** (default): transactions, row-level locking, foreign keys, MVCC via undo logs, clustered primary key, redo log for crash recovery, doublewrite buffer, buffer pool.",
               "Query cache was removed in 8.0."),
            TBL(["Engine", "Transactions", "FKs", "Locking", "Notes"],
                ["InnoDB", "Yes", "Yes", "Row-level", "Default; crash-safe"],
                ["MyISAM", "No", "No", "Table-level", "Legacy; fast reads, corruption-prone"],
                ["MEMORY", "No", "No", "Table-level", "Data lost on restart"],
                ["ARCHIVE", "No", "No", "Row", "Compressed insert-only logs"],
                ["CSV", "No", "No", "Table", "Plain CSV files"]),
            H("sql_mode"),
            UL("**ONLY_FULL_GROUP_BY** (default in 5.7+): rejects selecting non-grouped, non-aggregated columns.",
               "**STRICT_TRANS_TABLES:** invalid values (out of range, too long) raise errors instead of silent truncation with a warning.",
               "**NO_ZERO_DATE / NO_ZERO_IN_DATE:** forbid '0000-00-00'.",
               "**ANSI_QUOTES:** treat double quotes as identifiers (PostgreSQL style).",
               "**PIPES_AS_CONCAT:** make || concatenate instead of OR.",
               "**ERROR_FOR_DIVISION_BY_ZERO:** error instead of NULL."),
            MYSQL("SELECT @@sql_mode;\nSET SESSION sql_mode = 'STRICT_ALL_TABLES,ONLY_FULL_GROUP_BY,NO_ZERO_DATE';\nSELECT VERSION(), @@transaction_isolation, @@autocommit;"),
            H("InnoDB details worth knowing"),
            UL("The table IS the clustered B+ tree on the PRIMARY KEY. If you declare none, InnoDB picks the first NOT NULL UNIQUE index or a hidden 6-byte row id.",
               "Secondary indexes store the primary key as the row pointer: keep primary keys short.",
               "**Locks:** record locks, gap locks and next-key locks (default in REPEATABLE READ) prevent phantoms; intention locks; deadlock detection is automatic.",
               "**Redo log** gives durability (innodb_flush_log_at_trx_commit = 1 for full ACID), **undo log** gives rollback and MVCC.",
               "**Online DDL:** many ALTER TABLE operations run INPLACE without blocking writes."),
            H("Quirks and traps"),
            TBL(["Quirk", "Detail"],
                ["Case-insensitive comparison", "Default collation (utf8mb4_0900_ai_ci) makes 'A' = 'a'. Use BINARY or a _bin collation for exact matching"],
                ["Table-name case", "Case-sensitive on Linux, insensitive on Windows (lower_case_table_names)"],
                ["utf8 vs utf8mb4", "'utf8' is a 3-byte subset and cannot store emoji. Always use utf8mb4"],
                ["Implicit conversion", "'abc' + 1 = 1 with a warning; comparing varchar to number converts the column and kills the index"],
                ["|| operator", "Logical OR unless PIPES_AS_CONCAT"],
                ["Double-quoted strings", "Treated as strings, not identifiers; identifiers use backticks"],
                ["Silent truncation (non-strict)", "Too-long text is cut, out-of-range numbers are clipped"],
                ["Zero dates", "'0000-00-00' accepted unless NO_ZERO_DATE"],
                ["AUTO_INCREMENT", "Only one per table, must be a key; value lost counters on rollback"],
                ["Division", "5 / 2 = 2.5 (use DIV for integers)"],
                ["TIMESTAMP", "Stored as UTC, range ends in 2038; DATETIME has no time zone conversion"],
                ["Error 1093", "Cannot update a table while selecting from it in a subquery"],
                ["Reserved words", "Backtick them: `order`, `group`"]),
            H("Useful MySQL commands"),
            MYSQL("""SHOW DATABASES;  USE shop;  SHOW TABLES;  DESCRIBE employees;
SHOW CREATE TABLE employees\\G
SHOW INDEX FROM employees;
SHOW PROCESSLIST;      KILL 123;
SHOW VARIABLES LIKE 'innodb_buffer_pool_size';
SHOW ENGINE INNODB STATUS\\G          -- last deadlock, locks, buffer pool
SHOW WARNINGS;
EXPLAIN FORMAT=TREE SELECT ...;       -- 8.0
SELECT * FROM information_schema.TABLES WHERE TABLE_SCHEMA = 'shop';"""),
            H("MySQL 8.0 features (the modern answer)"),
            UL("CTEs including recursive, window functions, LATERAL derived tables.",
               "Roles, invisible indexes (test dropping an index safely), descending indexes, functional indexes.",
               "CHECK constraints enforced (8.0.16), atomic DDL, JSON improvements (JSON_TABLE), utf8mb4 default, EXPLAIN ANALYZE (8.0.18), INTERSECT/EXCEPT (8.0.31)."),
            H("Replication and HA (overview)"),
            UL("Binary log records changes. Source → replica asynchronous replication; semi-synchronous waits for one replica to acknowledge.",
               "GTIDs identify transactions to simplify failover. Group Replication / InnoDB Cluster provide multi-node HA.",
               "Replica lag is the usual operational problem; never read-your-own-write from an async replica without care."),
            ASK("\"MyISAM vs InnoDB?\" InnoDB: ACID transactions, row locks, FKs, crash recovery, clustered PK. MyISAM: no transactions or FKs, table locks, crash-unsafe. Use InnoDB."),
        ],
        [
            Q("Default MySQL storage engine since 5.5:", ["MyISAM", "InnoDB", "MEMORY", "CSV"], 1, "InnoDB."),
            Q("Which sql_mode setting makes SELECT dept_id, name ... GROUP BY dept_id fail?", ["STRICT_TRANS_TABLES", "ONLY_FULL_GROUP_BY", "NO_ZERO_DATE", "ANSI_QUOTES"], 1, "name is neither grouped nor aggregated."),
            Q("InnoDB secondary indexes store, as the row locator:", ["File offset", "Primary key value", "Row hash", "Page number only"], 1, "Hence short primary keys matter."),
            Q("MySQL 'utf8' charset problem:", ["Too slow", "Only 3 bytes per character, no emoji", "Not ASCII-compatible", "Read-only"], 1, "Use utf8mb4."),
            Q("In MySQL, SELECT 'Abc' = 'abc' returns (default collation):", ["0", "1", "NULL", "Error"], 1, "Case-insensitive comparison."),
        ], star=True, kw="mysql innodb myisam sql_mode engine quirks utf8mb4 only_full_group_by replication binlog"))

    # ------------------------------------------------------------------ comparison
    T.append(topic("pg-vs-mysql", GH, "PostgreSQL vs MySQL: the full comparison table",
        "The most direct way to check you know both. Read this before any interview where either might come up.",
        [
            TBL(["Area", "PostgreSQL", "MySQL (InnoDB, 8.0)"],
                ["Positioning", "Feature-rich, standards-focused, extensible object-relational DB", "Fast, simple, widely hosted; strong for web OLTP"],
                ["Default isolation", "READ COMMITTED", "REPEATABLE READ"],
                ["MVCC storage", "New row versions in the table; VACUUM cleans", "Undo log holds old versions; purge thread cleans"],
                ["Table storage", "Heap (rows unordered); PK is just an index", "Clustered B+ tree on the PK"],
                ["Transactional DDL", "Yes", "No (implicit commit)"],
                ["Auto id", "GENERATED ... AS IDENTITY, SERIAL, sequences", "AUTO_INCREMENT"],
                ["Boolean", "Real BOOLEAN", "Alias for TINYINT(1)"],
                ["Strings", "TEXT = VARCHAR, no length cost; case-sensitive comparison", "VARCHAR(n) with byte limits; case-insensitive default collation"],
                ["Identifiers", "Double quotes; folds unquoted names to lower case", "Backticks; case rules depend on OS"],
                ["Concatenation", "||, CONCAT", "CONCAT (|| is OR by default)"],
                ["Integer division", "5/2 = 2", "5/2 = 2.5 (DIV for integer)"],
                ["Type strictness", "Strict, explicit casts", "Lenient implicit conversions"],
                ["Unsigned ints", "No", "Yes"],
                ["Date/time", "DATE, TIME, TIMESTAMP, TIMESTAMPTZ, INTERVAL", "DATE, TIME, DATETIME, TIMESTAMP, YEAR"],
                ["JSON", "JSON, JSONB (binary, GIN indexable, rich operators)", "JSON (binary internally), functional/generated-column indexes"],
                ["Arrays / ranges / enums", "Native arrays, range types, CREATE TYPE enums", "ENUM and SET columns only"],
                ["FULL OUTER JOIN", "Yes", "No (UNION of left and right joins)"],
                ["INTERSECT / EXCEPT", "Yes", "8.0.31+"],
                ["CTE / window functions", "Since 8.4 (2009)", "Since 8.0 (2018)"],
                ["LATERAL joins", "Yes", "8.0.14+"],
                ["RETURNING", "Yes", "No (MariaDB has it)"],
                ["Upsert", "ON CONFLICT ... DO UPDATE", "ON DUPLICATE KEY UPDATE"],
                ["MERGE", "15+", "No"],
                ["UPDATE / DELETE with join", "UPDATE ... FROM, DELETE ... USING", "UPDATE ... JOIN, DELETE ... JOIN"],
                ["Partial / expression indexes", "Yes", "Expression indexes yes (8.0.13), partial no"],
                ["Index types", "B-tree, Hash, GIN, GiST, SP-GiST, BRIN", "B-tree, Hash (MEMORY), FULLTEXT, SPATIAL"],
                ["Materialized views", "Yes", "No"],
                ["Check constraints", "Always enforced", "Enforced since 8.0.16"],
                ["Foreign keys", "All table types, deferrable", "InnoDB only, immediate, no deferrable"],
                ["Exclusion constraints", "Yes", "No"],
                ["Triggers", "Row and statement level, INSTEAD OF, TRUNCATE", "Row-level only"],
                ["Procedural language", "PL/pgSQL (+ Python, Perl, JS...)", "SQL/PSM-style stored routines"],
                ["Row-level security", "Yes", "No"],
                ["Full-text search", "tsvector / tsquery, GIN", "FULLTEXT index, MATCH ... AGAINST"],
                ["GROUP BY strictness", "Strict", "ONLY_FULL_GROUP_BY by default since 5.7"],
                ["NULL ordering", "NULLs last in ASC (NULLS FIRST/LAST available)", "NULLs first in ASC"],
                ["Replication", "Streaming (physical), logical publish/subscribe", "Binlog-based async/semi-sync, Group Replication"],
                ["Extensions", "Rich ecosystem (PostGIS, pgvector, TimescaleDB)", "Plugins; fewer"],
                ["Connections", "Process per connection; use pooler", "Thread per connection"],
                ["Default port", "5432", "3306"],
                ["Typical strengths", "Complex queries, analytics, data integrity, geospatial, JSON", "Simple high-volume reads, mature hosting, easy start"]),
            H("Syntax you must be able to translate on demand"),
            TBL(["Task", "PostgreSQL", "MySQL"],
                ["Limit", "SELECT ... LIMIT 5 OFFSET 10", "SELECT ... LIMIT 5 OFFSET 10 (or LIMIT 10, 5)"],
                ["Auto id", "id BIGINT GENERATED ALWAYS AS IDENTITY", "id BIGINT AUTO_INCREMENT"],
                ["Current time", "now()", "NOW()"],
                ["If null", "COALESCE(a, b)", "COALESCE(a, b) or IFNULL(a, b)"],
                ["If / case", "CASE WHEN ... END", "CASE WHEN ... END or IF(cond, a, b)"],
                ["String aggregate", "STRING_AGG(x, ', ')", "GROUP_CONCAT(x SEPARATOR ', ')"],
                ["Case-insensitive match", "ILIKE", "LIKE"],
                ["Regex", "~ and ~*", "REGEXP"],
                ["Show tables", "\\dt", "SHOW TABLES"],
                ["Describe", "\\d table", "DESCRIBE table"],
                ["Show create", "pg_dump -s -t table", "SHOW CREATE TABLE table"],
                ["Cast", "x::int or CAST", "CAST(x AS SIGNED)"],
                ["Rename column", "ALTER TABLE t RENAME COLUMN a TO b", "same (8.0) or CHANGE"],
                ["Drop FK", "DROP CONSTRAINT name", "DROP FOREIGN KEY name"],
                ["Row count of last statement", "GET DIAGNOSTICS n = ROW_COUNT", "ROW_COUNT()"]),
            ASK("\"Why PostgreSQL over MySQL?\" Stricter correctness, richer types and indexes (JSONB, arrays, ranges, partial/GIN/BRIN), transactional DDL, better planner for complex queries, extensions (PostGIS, pgvector), row-level security. \"Why MySQL?\" Simplicity, ecosystem and hosting ubiquity, fast simple workloads, easy replication."),
        ],
        [
            Q("Which does PostgreSQL support but MySQL does not?", ["INNER JOIN", "FULL OUTER JOIN", "GROUP BY", "LIMIT"], 1, "MySQL emulates it with UNION."),
            Q("Default isolation level of PostgreSQL versus MySQL InnoDB:", ["Both REPEATABLE READ", "READ COMMITTED vs REPEATABLE READ", "SERIALIZABLE vs READ COMMITTED", "Both READ COMMITTED"], 1, "PostgreSQL READ COMMITTED, InnoDB REPEATABLE READ."),
            Q("MySQL's equivalent of PostgreSQL ON CONFLICT DO UPDATE:", ["MERGE", "ON DUPLICATE KEY UPDATE", "REPLACE ONLY", "UPSERT"], 1, "Different syntax, same intent."),
            Q("Which storage design does MySQL InnoDB use?", ["Heap with separate PK index", "Clustered B+ tree on the primary key", "LSM tree", "Hash table"], 1, "Rows live in the primary key index."),
            Q("Case-insensitive pattern match: PostgreSQL vs MySQL default:", ["LIKE vs ILIKE", "ILIKE vs LIKE", "REGEXP vs LIKE", "SOUNDEX vs ILIKE"], 1, "PostgreSQL needs ILIKE; MySQL LIKE is case-insensitive by default collation."),
            Q("RETURNING clause is native to:", ["MySQL", "PostgreSQL", "Both", "Neither"], 1, "MySQL has no RETURNING."),
        ], star=True, kw="postgresql vs mysql comparison difference translate syntax"))

    # ------------------------------------------------------------------ JSON
    T.append(topic("json-support", GH, "JSON in SQL: JSONB and MySQL JSON",
        "Semi-structured data inside a relational table. Know the operators and when JSON is the right tool.",
        [
            SQL("""SELECT json_extract('{"user":"asha","tags":["a","b"],"geo":{"city":"Pune"}}', '$.geo.city') AS city,
       json_extract('{"tags":["a","b"]}', '$.tags[1]') AS second_tag,
       json_array_length('{"tags":["a","b"]}', '$.tags') AS n_tags;""", "SQLite JSON functions, runnable here", run=True),
            H("PostgreSQL JSONB"),
            PGSQL("""CREATE TABLE event (
  id      BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  payload JSONB NOT NULL
);
INSERT INTO event (payload) VALUES ('{"user":"asha","tags":["a","b"],"geo":{"city":"Pune"},"score":7}');

SELECT payload->'user'            AS as_json,       -- -> returns jsonb
       payload->>'user'           AS as_text,       -- ->> returns text
       payload->'geo'->>'city'    AS city,
       payload#>>'{geo,city}'     AS city2,         -- path operator
       (payload->>'score')::int   AS score
FROM event;

SELECT * FROM event WHERE payload @> '{"user":"asha"}';          -- contains
SELECT * FROM event WHERE payload ? 'tags';                        -- key exists
SELECT * FROM event WHERE payload->'tags' ? 'a';                   -- array contains element
SELECT jsonb_array_elements_text(payload->'tags') FROM event;      -- unnest array

UPDATE event SET payload = jsonb_set(payload, '{geo,city}', '"Delhi"');   -- change a nested value
UPDATE event SET payload = payload || '{"vip": true}';                    -- merge keys
UPDATE event SET payload = payload - 'vip';                               -- delete a key

CREATE INDEX idx_event_payload ON event USING gin (payload);             -- supports @>, ?, ?|, ?&
CREATE INDEX idx_event_user ON event ((payload->>'user'));               -- btree on one field

SELECT jsonb_build_object('id', id, 'name', name) FROM employees;        -- build JSON from rows
SELECT jsonb_agg(jsonb_build_object('n', name)) FROM employees WHERE dept_id = 2;"""),
            TBL(["", "JSON", "JSONB"],
                ["Storage", "Text copy, whitespace and key order preserved", "Binary, decomposed, no duplicate keys, key order not kept"],
                ["Speed", "Parsed at each use", "Faster queries, slightly slower writes"],
                ["Indexing", "No", "GIN, expression indexes"],
                ["Use", "Rarely", "Almost always"]),
            H("MySQL JSON"),
            MYSQL("""CREATE TABLE event (id BIGINT AUTO_INCREMENT PRIMARY KEY, payload JSON NOT NULL);
INSERT INTO event (payload) VALUES ('{"user":"asha","tags":["a","b"],"geo":{"city":"Pune"},"score":7}');

SELECT payload->'$.user'              AS as_json,    -- returns JSON (quoted)
       payload->>'$.user'             AS as_text,    -- unquoted text
       JSON_EXTRACT(payload, '$.geo.city')            AS city_json,
       JSON_UNQUOTE(JSON_EXTRACT(payload, '$.geo.city')) AS city
FROM event;

SELECT * FROM event WHERE JSON_CONTAINS(payload, '"a"', '$.tags');
SELECT * FROM event WHERE JSON_EXTRACT(payload, '$.score') > 5;

UPDATE event SET payload = JSON_SET(payload, '$.geo.city', 'Delhi');
UPDATE event SET payload = JSON_REMOVE(payload, '$.score');
SELECT JSON_OBJECT('id', id, 'name', name) FROM employees;
SELECT JSON_ARRAYAGG(name) FROM employees WHERE dept_id = 2;

-- index a JSON field via a generated column
ALTER TABLE event
  ADD COLUMN user_name VARCHAR(50) GENERATED ALWAYS AS (payload->>'$.user') STORED,
  ADD INDEX idx_user (user_name);

-- explode a JSON array into rows (8.0)
SELECT t.tag FROM event, JSON_TABLE(payload, '$.tags[*]' COLUMNS (tag VARCHAR(20) PATH '$')) AS t;"""),
            H("When to use JSON columns"),
            UL("**Good:** truly variable attributes (product specs per category), event payloads and API responses you store verbatim, settings, sparse metadata.",
               "**Bad:** fields you filter, join or aggregate on constantly, anything needing foreign keys, uniqueness or strong types. Promote those to real columns.",
               "Hybrid is normal: relational columns for the core, one JSONB column for the flexible remainder."),
            ASK("\"JSON vs relational columns?\" Use columns for stable, queried, constrained data. Use JSONB for flexible, rarely-queried attributes, and index the hot paths (GIN or generated column)."),
        ],
        [
            Q("In PostgreSQL, payload->>'user' returns:", ["jsonb", "text", "boolean", "an array"], 1, "->> returns text; -> returns JSON."),
            Q("Which operator tests whether JSONB contains another JSONB document?", ["?", "@>", "||", "#>"], 1, "@> is contains."),
            Q("Best index for @> queries over a JSONB column:", ["B-tree", "GIN", "Hash", "BRIN"], 1, "GIN indexes JSONB keys and values."),
            Q("In MySQL you index a JSON field by:", ["CREATE JSON INDEX", "A generated column plus an index", "It is automatic", "Not possible"], 1, "Generated column (or a functional index in 8.0.13+)."),
            Q("Which is a bad use of a JSON column?", ["Storing raw API responses", "Storing the customer_id you join on constantly", "Optional preferences", "Product specs that vary by type"], 1, "Join keys need real columns, FKs and indexes."),
        ], kw="json jsonb operators gin json_extract json_set json_table generated column"))

    # ------------------------------------------------------------------ metadata
    T.append(topic("metadata-queries", GH, "Metadata and monitoring queries (information_schema, catalogs)",
        "Finding out what exists in a database, and what is happening in it right now. Asked as 'how do you find all tables containing column X?'",
        [
            SQL("""SELECT type, name FROM sqlite_master WHERE type IN ('table','view','index','trigger') ORDER BY type, name;""", "SQLite's catalog, runnable", run=True),
            SQL("""SELECT name, type, "notnull", pk FROM pragma_table_info('employees');""", "columns of a table (SQLite)", run=True),
            H("Standard information_schema (both engines)"),
            SQL("""-- all tables in a schema
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE';   -- MySQL: table_schema = 'shop'

-- columns of a table
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns WHERE table_name = 'employees' ORDER BY ordinal_position;

-- every table that has a column called email
SELECT table_schema, table_name FROM information_schema.columns WHERE column_name = 'email';

-- constraints and keys
SELECT constraint_name, constraint_type FROM information_schema.table_constraints WHERE table_name = 'employees';
SELECT constraint_name, column_name FROM information_schema.key_column_usage WHERE table_name = 'employees';""", "not runnable in SQLite"),
            H("Foreign keys referencing a table"),
            PGSQL("""SELECT conrelid::regclass AS child_table, conname, pg_get_constraintdef(oid) AS definition
FROM pg_constraint WHERE contype = 'f' AND confrelid = 'department'::regclass;"""),
            MYSQL("""SELECT TABLE_NAME, COLUMN_NAME, CONSTRAINT_NAME FROM information_schema.KEY_COLUMN_USAGE
WHERE REFERENCED_TABLE_NAME = 'departments' AND TABLE_SCHEMA = DATABASE();"""),
            H("Sizes and counts"),
            PGSQL("""SELECT relname, pg_size_pretty(pg_total_relation_size(oid)) AS total_size
FROM pg_class WHERE relkind = 'r' AND relnamespace = 'public'::regnamespace ORDER BY pg_total_relation_size(oid) DESC LIMIT 10;
SELECT pg_size_pretty(pg_database_size(current_database()));
SELECT relname, n_live_tup FROM pg_stat_user_tables ORDER BY n_live_tup DESC;   -- estimated row counts (fast)"""),
            MYSQL("""SELECT TABLE_NAME, ROUND((DATA_LENGTH + INDEX_LENGTH) / 1024 / 1024, 1) AS size_mb, TABLE_ROWS
FROM information_schema.TABLES WHERE TABLE_SCHEMA = DATABASE() ORDER BY size_mb DESC;"""),
            H("What is running and who is blocking whom"),
            PGSQL("""SELECT pid, usename, state, now() - query_start AS running_for, wait_event_type, left(query, 80) AS query
FROM pg_stat_activity WHERE state <> 'idle' ORDER BY running_for DESC;

SELECT pg_cancel_backend(12345);          -- cancel the current query
SELECT pg_terminate_backend(12345);       -- kill the connection

-- blockers
SELECT blocked.pid AS blocked_pid, blocking.pid AS blocking_pid, blocked.query AS blocked_query
FROM pg_stat_activity blocked
JOIN pg_stat_activity blocking ON blocking.pid = ANY (pg_blocking_pids(blocked.pid));

-- unused / missing indexes
SELECT relname, indexrelname, idx_scan FROM pg_stat_user_indexes ORDER BY idx_scan ASC LIMIT 10;
SELECT relname, seq_scan, idx_scan FROM pg_stat_user_tables WHERE seq_scan > idx_scan ORDER BY seq_scan DESC;"""),
            MYSQL("""SHOW FULL PROCESSLIST;
KILL QUERY 123;   KILL 123;
SELECT * FROM performance_schema.data_lock_waits;      -- 8.0 lock waits
SELECT * FROM sys.statements_with_full_table_scans LIMIT 10;
SELECT * FROM sys.schema_unused_indexes;"""),
            ASK("\"How do you find the slowest queries?\" PostgreSQL: pg_stat_statements, auto_explain, log_min_duration_statement. MySQL: slow query log, performance_schema / sys schema, EXPLAIN ANALYZE."),
        ],
        [
            Q("Query to list all columns named email across tables:", ["SELECT * FROM tables", "SELECT table_name FROM information_schema.columns WHERE column_name = 'email'", "SHOW COLUMNS", "DESCRIBE email"], 1, "information_schema.columns works in both PostgreSQL and MySQL."),
            Q("PostgreSQL view of currently running queries:", ["pg_stat_activity", "pg_tables", "information_queries", "pg_locks_only"], 0, "pg_stat_activity lists sessions and their queries."),
            Q("To stop one running query without dropping the connection in PostgreSQL:", ["pg_terminate_backend", "pg_cancel_backend", "KILL", "ROLLBACK ALL"], 1, "Cancel the query; terminate kills the whole backend."),
            Q("MySQL command listing processes and queries:", ["SHOW PROCESSLIST", "SHOW QUERIES", "LIST SESSIONS", "SELECT PROCESS()"], 0, "SHOW [FULL] PROCESSLIST."),
        ], kw="information_schema metadata catalog pg_stat_activity processlist table size find column pg_class blocking"))

    # ------------------------------------------------------------------ ops
    T.append(topic("ops-backup-replication", GH, "Operations: backups, replication, tuning, common production problems",
        "Questions for roles that touch production: how do you back up, scale reads, tune, and debug.",
        [
            H("Backups"),
            TBL(["Type", "PostgreSQL", "MySQL"],
                ["Logical (SQL/data dump)", "pg_dump -Fc db > db.dump ;  pg_restore -d db db.dump ;  pg_dumpall (roles + all dbs)", "mysqldump --single-transaction --routines --triggers db > db.sql ;  mysql db < db.sql"],
                ["Physical (files)", "pg_basebackup -D /backup -Ft -z -P", "Percona XtraBackup / MySQL Enterprise Backup"],
                ["Point-in-time recovery", "Base backup + archived WAL (archive_command), recovery_target_time", "Full backup + replay binary logs (mysqlbinlog)"],
                ["Consistent snapshot", "pg_dump uses a snapshot of one transaction", "--single-transaction (InnoDB)"]),
            UL("A backup you have not restored is not a backup: test restores regularly.",
               "RPO (how much data you can lose) and RTO (how long you can be down) decide the strategy.",
               "3-2-1 rule: three copies, two media types, one offsite."),
            H("Replication and high availability"),
            TBL(["", "PostgreSQL", "MySQL"],
                ["Physical", "Streaming replication (WAL shipping), sync or async, hot standby for reads", "n/a"],
                ["Logical", "Publication / subscription (per table, cross-version)", "Row-based binlog replication"],
                ["Failover", "Patroni, repmgr, cloud-managed", "InnoDB Cluster, Orchestrator, cloud-managed"],
                ["Multi-primary", "BDR / extensions", "Group Replication multi-primary"]),
            UL("**Read replicas** scale reads but lag; route read-your-own-writes to the primary.",
               "**Synchronous** replication avoids data loss at the price of latency; **asynchronous** is fast but can lose the last transactions on failover.",
               "**Split brain:** two nodes both think they are primary. Prevented by consensus/fencing."),
            H("Tuning knobs"),
            TBL(["Setting", "Rule of thumb"],
                ["PostgreSQL shared_buffers", "About 25% of RAM"],
                ["PostgreSQL effective_cache_size", "50-75% of RAM (planner hint only)"],
                ["PostgreSQL work_mem", "Per sort/hash node per connection: keep modest (4-64 MB), raise per session for big reports"],
                ["PostgreSQL max_connections", "Keep low (100-300) and put PgBouncer in front"],
                ["PostgreSQL autovacuum", "Keep ON; tune scale factors for big tables"],
                ["MySQL innodb_buffer_pool_size", "50-75% of RAM on a dedicated server"],
                ["MySQL innodb_flush_log_at_trx_commit", "1 for full durability, 2 for speed with small risk"],
                ["MySQL max_connections / thread cache", "Pool connections in the app (HikariCP, ProxySQL)"]),
            H("Common production problems and the first thing to check"),
            TBL(["Symptom", "Likely cause", "Check / fix"],
                ["Query suddenly slow", "Plan changed, stale stats, new data distribution", "EXPLAIN (ANALYZE); ANALYZE; add or fix index"],
                ["CPU high with many similar queries", "N+1 queries from the ORM, missing index", "pg_stat_statements; batch the queries"],
                ["Everything waits", "Long transaction holding locks", "pg_stat_activity / pg_locks; kill the blocker; shorten transactions"],
                ["Disk growing, table bloated", "Dead tuples, autovacuum behind", "VACUUM (ANALYZE); tune autovacuum; pg_repack"],
                ["Too many connections", "No pooling, leaked connections", "PgBouncer, pool size limits"],
                ["Replica lag", "Big transactions, slow replica disk", "Smaller batches, better hardware, monitor lag"],
                ["Deadlock errors", "Inconsistent lock order", "Lock in a fixed order; retry"],
                ["Out-of-memory", "Huge work_mem x connections", "Lower work_mem; pool connections"]),
            H("Connection pooling in one paragraph"),
            P("Opening a database connection is expensive and PostgreSQL uses a process per connection. A pooler (application-side like HikariCP, or PgBouncer/ProxySQL) keeps a small set of persistent connections and multiplexes many clients over them. Transaction-level pooling is the most efficient but breaks session features (prepared statements, SET, advisory locks)."),
            ASK("\"Your database is slow in production, walk me through it.\" Check what is running now (activity view), look for blocking and long transactions, find the top queries by total time, EXPLAIN them, check stats/bloat/indexes, then check resources (CPU, memory, IO) and connections."),
        ],
        [
            Q("Tool for a logical backup of one PostgreSQL database:", ["pg_basebackup", "pg_dump", "pg_ctl", "psql -l"], 1, "pg_dump; pg_basebackup is a physical base backup."),
            Q("Point-in-time recovery needs:", ["A logical dump only", "A base backup plus continuous log archive", "Replication only", "A snapshot of the OS"], 1, "WAL (PostgreSQL) or binlog (MySQL) replayed to the target time."),
            Q("A common recommendation for PostgreSQL shared_buffers is roughly:", ["1% RAM", "25% of RAM", "100% of RAM", "512 bytes"], 1, "A quarter of RAM is the usual starting point."),
            Q("Long-running open transactions hurt PostgreSQL because they:", ["Use CPU only", "Prevent VACUUM from removing dead rows", "Disable indexes", "Reset sequences"], 1, "Old snapshots keep dead tuples visible."),
            Q("Read replicas can show stale data because replication is usually:", ["Synchronous", "Asynchronous", "Disabled", "One-way encrypted"], 1, "Async replicas lag behind the primary."),
        ], kw="backup restore pg_dump mysqldump pitr replication failover tuning shared_buffers connection pool pgbouncer production slow"))

    # ------------------------------------------------------------------ interview QA
    T.append(topic("interview-qa", GH, "Interview rapid-fire: 60 questions with model answers",
        "Short crisp answers for the standard questions. Say these in your own words; add one example each.",
        [
            H("Fundamentals"),
            TBL(["Question", "Answer"],
                ["What is a database / DBMS / RDBMS?", "Database: organised data. DBMS: software that manages it. RDBMS: DBMS based on tables, keys, constraints and SQL (PostgreSQL, MySQL)."],
                ["What is SQL?", "Structured Query Language: declarative language to define, manipulate, query and control relational data."],
                ["Difference between SQL and MySQL?", "SQL is the language. MySQL is one database product that implements it."],
                ["DDL, DML, DCL, TCL?", "Define structure (CREATE, ALTER, DROP), change data (INSERT, UPDATE, DELETE), permissions (GRANT, REVOKE), transactions (COMMIT, ROLLBACK, SAVEPOINT)."],
                ["Table, row, column, field?", "Relation, tuple, attribute, a single cell value."],
                ["What is a schema?", "A logical container/namespace of tables and objects; also the structural definition of the database."],
                ["Data integrity?", "Accuracy and consistency of data, enforced by constraints, keys and transactions."],
                ["What is a constraint? Types?", "A rule enforced by the DB: NOT NULL, UNIQUE, PRIMARY KEY, FOREIGN KEY, CHECK, DEFAULT."]),
            H("Keys"),
            TBL(["Question", "Answer"],
                ["Primary vs unique key?", "One PK per table, no NULL; many UNIQUE, NULLs allowed (multiple in PostgreSQL and MySQL)."],
                ["Primary vs foreign key?", "PK identifies a row in its table; FK references a key in another (or same) table to enforce referential integrity."],
                ["Candidate, super, alternate, composite key?", "Super: any unique set. Candidate: minimal super key. Alternate: candidate not chosen as PK. Composite: key with more than one column."],
                ["Surrogate vs natural key?", "Surrogate is a system id with no meaning; natural is a real-world identifier like email or ISBN."],
                ["Can a table have no primary key? Can a PK be NULL?", "It can exist without one (not advisable). A PK can never be NULL."],
                ["Can an FK be NULL or duplicate?", "Yes to both, unless NOT NULL/UNIQUE is declared."]),
            H("Queries"),
            TBL(["Question", "Answer"],
                ["WHERE vs HAVING?", "WHERE filters rows before grouping; HAVING filters groups after aggregation."],
                ["DELETE vs TRUNCATE vs DROP?", "Delete rows (filterable, logged, rollbackable); remove all rows fast keeping structure; remove the whole table."],
                ["UNION vs UNION ALL?", "UNION removes duplicates (cost), UNION ALL keeps them (faster)."],
                ["INNER vs LEFT vs FULL join?", "Matches only; all left plus matches; everything from both sides with NULLs."],
                ["Self join and cross join?", "Table joined to itself via aliases; every combination (m x n rows)."],
                ["IN vs EXISTS?", "IN compares to a list; EXISTS tests whether any row exists and is NULL-safe with NOT. Optimizers often treat them alike."],
                ["Subquery vs join?", "Join combines columns; subquery filters or computes. Joins are often faster and more readable but results can duplicate rows."],
                ["COUNT(*) vs COUNT(col)?", "All rows vs non-NULL values of col."],
                ["char vs varchar vs text?", "Fixed-length padded; variable up to n; unlimited. PostgreSQL: varchar and text perform the same."],
                ["What is NULL?", "Unknown/missing value; compared only with IS NULL; ignored by aggregates."],
                ["RANK vs DENSE_RANK vs ROW_NUMBER?", "Ties share rank with gaps; ties share rank without gaps; unique sequential numbers."],
                ["What is a CTE?", "A named temporary result used within one statement; recursive CTEs walk hierarchies."],
                ["What is a window function?", "Computes over a set of related rows without collapsing them (ranking, running totals, LAG/LEAD)."],
                ["How to find duplicates / delete them?", "GROUP BY cols HAVING COUNT(*) > 1; delete keeping MIN(id) or ROW_NUMBER() > 1."],
                ["Nth highest salary?", "DENSE_RANK() OVER (ORDER BY salary DESC) = N, or ORDER BY ... LIMIT 1 OFFSET N-1 on DISTINCT salary."],
                ["Pagination?", "LIMIT/OFFSET, or keyset: WHERE id > last ORDER BY id LIMIT n."]),
            H("Design and theory"),
            TBL(["Question", "Answer"],
                ["What is normalization?", "Organising tables to remove redundancy and anomalies using functional dependencies: 1NF, 2NF, 3NF, BCNF, 4NF, 5NF."],
                ["1NF / 2NF / 3NF / BCNF in one line each?", "Atomic values; no partial dependency; no transitive dependency; every determinant is a super key."],
                ["Denormalization?", "Deliberately adding redundancy for read speed (reporting, caching), accepting update cost."],
                ["Functional dependency?", "X determines Y: equal X values imply equal Y values."],
                ["ER diagram components?", "Entities, attributes, relationships, cardinality, participation; weak entities; specialization."],
                ["Cardinality types?", "1:1, 1:N, M:N (junction table)."],
                ["What is ACID?", "Atomicity, Consistency, Isolation, Durability."],
                ["Isolation levels and anomalies?", "Read uncommitted, read committed, repeatable read, serializable; dirty read, non-repeatable read, phantom."],
                ["What is a deadlock and how to avoid?", "Circular lock wait; consistent lock ordering, short transactions, timeouts, retries."],
                ["Optimistic vs pessimistic locking?", "Check version at write time and retry on conflict; lock first with FOR UPDATE."],
                ["What is MVCC?", "Multiple row versions so readers do not block writers."],
                ["CAP theorem?", "During a partition choose consistency or availability."],
                ["SQL vs NoSQL?", "Structured, transactional, joins vs flexible schema, horizontal scale; choose by access patterns."],
                ["OLTP vs OLAP?", "Many small transactions vs few large analytical queries; normalized vs star schema."]),
            H("Objects and performance"),
            TBL(["Question", "Answer"],
                ["What is an index? Downsides?", "Structure for fast lookup (B+ tree). Costs storage and slows writes."],
                ["Clustered vs non-clustered?", "Rows stored in key order (one per table) vs separate pointer structure."],
                ["When is an index not used?", "Function on the column, leading wildcard, type mismatch, low selectivity, small table, stale stats."],
                ["View vs materialized view?", "Saved query without data vs stored result refreshed on demand."],
                ["Stored procedure vs function?", "Procedure: CALL, OUT params, transaction control. Function: returns a value, used in queries."],
                ["What is a trigger? Types?", "Auto-run code on INSERT/UPDATE/DELETE; BEFORE/AFTER/INSTEAD OF; row or statement level."],
                ["What is a cursor?", "Handle to fetch result rows one at a time; prefer set-based SQL."],
                ["Temp table vs CTE vs view?", "Session-scoped stored result; single-statement named query; permanent named query."],
                ["How do you optimise a slow query?", "EXPLAIN, index, rewrite for SARGability, reduce columns/rows early, update stats, avoid N+1."],
                ["What is a sequence / auto-increment?", "Generator of unique numbers; non-transactional, so gaps occur."],
                ["SQL injection and prevention?", "Untrusted input changes query logic; prevent with parameterised queries and least privilege."],
                ["Partitioning vs sharding vs replication?", "Split a table in one server; split data across servers; copy data to other servers."],
                ["What is a transaction log / WAL?", "Sequential record of changes written before data pages, enabling durability and recovery."],
                ["PostgreSQL vs MySQL?", "PostgreSQL: richer types/indexes, strict, transactional DDL. MySQL: simple, fast, InnoDB clustered PK."]),
            ASK("Practise saying each answer in 20 seconds, then one follow-up example. Interviews reward structure: define, contrast, example, edge case."),
        ],
        [
            Q("Which pair is correctly described? Primary key vs unique key:", ["Both forbid NULL always", "PK: one per table, not null; UNIQUE: many per table, NULLs allowed", "UNIQUE forbids duplicates but PK allows them", "They are identical"], 1, "That is the standard contrast."),
            Q("Which SQL group does ROLLBACK belong to?", ["DDL", "DML", "TCL", "DCL"], 2, "Transaction control."),
            Q("Finding duplicates needs:", ["WHERE COUNT(*) > 1", "GROUP BY ... HAVING COUNT(*) > 1", "ORDER BY", "LIMIT"], 1, "Group, then filter groups."),
            Q("2NF removes:", ["Transitive dependencies", "Partial dependencies", "Multivalued dependencies", "Join dependencies"], 1, "Partial dependencies on part of a composite key."),
            Q("Which index types can serve a range query best?", ["Hash", "B+ tree", "Bitmap only", "None"], 1, "B+ tree keeps keys ordered with linked leaves."),
            Q("Faster at pulling the last 10 pages of results: OFFSET or keyset?", ["OFFSET", "Keyset", "Same", "Neither works"], 1, "Keyset seeks directly via the index."),
        ], star=True, kw="interview questions answers rapid fire viva dbms sql theory"))

    return T
