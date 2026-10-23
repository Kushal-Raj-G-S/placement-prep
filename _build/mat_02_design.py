"""Study guide, part 2: normal forms (1NF to 6NF), transactions, concurrency, recovery, indexing, query processing, distributed/OLAP."""
from mat_common import *

GB = "B. Relational model and normalization"
GC = "C. Transactions, storage and architecture"


def build():
    T = []

    # ------------------------------------------------------------------ NF 1-BCNF
    T.append(topic("normal-forms", GB, "Normalization: anomalies, 1NF, 2NF, 3NF, BCNF",
        "Normalization splits a badly designed table into smaller ones so each fact is stored once. It is driven by functional dependencies. You must be able to name the highest normal form of a relation and decompose it.",
        [
            H("Why: the three anomalies"),
            TXT("""EMP_DEPT(emp_id, emp_name, dept_id, dept_name, dept_head)
 101  Asha   D1  Data   Meera
 102  Rohan  D1  Data   Meera
 103  Kiran  D2  Cloud  Vikram

Update anomaly : rename Data to Analytics -> must change every employee row, miss one and it is inconsistent
Insert anomaly : cannot add a new department until it has an employee (emp_id is the key)
Delete anomaly : delete Kiran and you lose the fact that D2 'Cloud' exists"""),
            H("1NF: atomic values"),
            UL("Every cell holds a single indivisible value. No repeating groups, no lists, no arrays-in-a-cell, no composite values you need to query parts of.",
               "Every row is unique (a key exists). Column and row order carry no meaning."),
            TXT("""Violates 1NF:                       Fixed:
 student  phones                      student  phone
 Asha     98450, 98451                Asha     98450
 Rohan    90000                       Asha     98451
                                      Rohan    90000"""),
            NOTE("PostgreSQL ARRAY and JSONB columns, and MySQL JSON, technically hold non-atomic values. They are tools for special cases; strict relational design still uses a child table."),
            H("2NF: no partial dependency"),
            P("A relation is in 2NF if it is in 1NF and **no non-prime attribute depends on a proper subset of a candidate key**. Only matters when the key is composite. If every key is a single attribute, a 1NF relation is automatically 2NF."),
            TXT("""ENROLL(student_id, course_id, student_name, grade)
Key: {student_id, course_id}
student_id -> student_name   is a PARTIAL dependency (part of the key decides student_name)

Decompose:
  STUDENT(student_id, student_name)
  ENROLL(student_id, course_id, grade)"""),
            H("3NF: no transitive dependency"),
            P("In 2NF and, for every non-trivial FD X → A, **either X is a super key or A is a prime attribute**. In words: non-prime attributes depend on the key, the whole key and nothing but the key."),
            TXT("""EMP(emp_id, emp_name, dept_id, dept_name)
Key: emp_id.   emp_id -> dept_id -> dept_name   (transitive)

Decompose:
  EMP(emp_id, emp_name, dept_id)
  DEPT(dept_id, dept_name)"""),
            H("BCNF: every determinant is a key"),
            P("For every non-trivial FD X → Y, **X must be a super key**. This is stricter than 3NF because it drops the 'or A is prime' escape hatch."),
            TXT("""TEACH(student, course, instructor)
FDs: {student, course} -> instructor       (a student has one instructor per course)
     instructor -> course                  (each instructor teaches one course)
Candidate keys: {student, course} and {student, instructor}  -> all attributes are prime
3NF: yes (every RHS attribute is prime).
BCNF: NO. instructor -> course, but instructor is not a super key.

BCNF decomposition:  R1(instructor, course)   R2(student, instructor)
Lossless: yes.  Dependency preserving: NO, {student, course} -> instructor is lost."""),
            H("Testing the highest normal form (procedure)"),
            OL("Find all candidate keys (closure method). List prime attributes.",
               "For each FD X → Y: if X is a super key, fine. If X is not a super key and Y ⊆ X, ignore (trivial).",
               "If X is not a super key and Y has a non-prime attribute: check X. If X is a proper subset of a key, it is a **partial** dependency: violates 2NF. If X is not a subset of any key, it is **transitive**: violates 3NF.",
               "If X is not a super key but every attribute of Y is prime: 3NF holds, BCNF fails.",
               "The relation is in the normal form given by the worst violation."),
            TXT("""R(A,B,C,D)  F = { AB → C, B → D }
Key: A and B are on no RHS, so AB. AB+ = ABCD. Key = {A,B}, prime = A,B; non-prime = C,D.
B → D : B is a proper subset of the key and D is non-prime: PARTIAL dependency.  => 1NF only.

R(A,B,C)  F = { A → B, B → C }
Key = A.  B → C: B not a super key, C non-prime, B not a subset of a key: TRANSITIVE.  => 2NF, not 3NF.

R(A,B,C)  F = { AB → C, C → B }
Keys: AB and AC.  All prime.  C → B has C not a super key but B is prime.  => 3NF, not BCNF."""),
            H("Comparison"),
            TBL(["Normal form", "Condition", "Removes"],
                ["1NF", "Atomic values, key exists", "Repeating groups"],
                ["2NF", "1NF + no partial dependency", "Redundancy from part of a composite key"],
                ["3NF", "2NF + for X → A: X super key or A prime", "Transitive dependencies"],
                ["BCNF", "For every non-trivial X → Y: X is a super key", "Remaining FD redundancy"],
                ["4NF", "BCNF + no non-trivial MVD except on a super key", "Multivalued redundancy"],
                ["5NF (PJNF)", "4NF + every join dependency implied by candidate keys", "Join-dependency redundancy"]),
            H("Properties of decompositions"),
            UL("**Lossless join:** joining the pieces gets back exactly the original rows. For a binary split R into R1, R2 it is lossless iff (R1 ∩ R2) → R1 or (R1 ∩ R2) → R2.",
               "**Dependency preserving:** every original FD can be checked inside a single piece.",
               "**BCNF** decomposition is always lossless but may not preserve dependencies.",
               "**3NF** decomposition (synthesis algorithm using a minimal cover) is always lossless AND dependency preserving."),
            P("Quick facts: every relation with 2 attributes is in BCNF. Every BCNF relation is in 3NF, every 3NF in 2NF, every 2NF in 1NF. If all attributes are prime, the relation is at least 3NF."),
            H("When to denormalize"),
            P("Read-heavy reporting systems may deliberately duplicate columns (store customer_name in orders, keep a precomputed total) to avoid joins. You trade extra storage and the risk of inconsistency for read speed. Normalize first; denormalize with a measured reason."),
            ASK("\"What is the difference between 3NF and BCNF?\" 3NF permits a dependency X → A when A is prime even if X is not a key; BCNF does not. They differ only when a relation has overlapping composite candidate keys."),
        ],
        [
            Q("R(A,B,C,D) with F = {AB→C, B→D}. The highest normal form is:", ["1NF", "2NF", "3NF", "BCNF"], 0, "Key is AB. B → D is a partial dependency of non-prime D on part of the key."),
            Q("R(A,B,C) with F = {A→B, B→C}. The highest normal form is:", ["1NF", "2NF", "3NF", "BCNF"], 1, "Key A. B → C is transitive, so 3NF fails; no partial dependency since the key is one attribute."),
            Q("R(A,B,C) with F = {AB→C, C→B}. The highest normal form is:", ["2NF", "3NF but not BCNF", "BCNF", "1NF"], 1, "Keys AB and AC, everything prime, so 3NF. C → B violates BCNF since C is not a super key."),
            Q("A relation with only two attributes is always in at least:", ["1NF only", "2NF only", "BCNF", "4NF only"], 2, "Any non-trivial FD in a 2-attribute relation has a key on its left side or leaves nothing to violate, so BCNF holds."),
            Q("Which decomposition is always lossless AND dependency preserving?", ["BCNF decomposition", "3NF synthesis from a minimal cover", "Any binary split", "Splitting by columns alphabetically"], 1, "3NF synthesis guarantees both. BCNF cannot guarantee dependency preservation."),
            Q("Splitting R into R1 and R2 is lossless if:", ["R1 and R2 have no common attribute", "R1 ∩ R2 is a key of R1 or of R2", "R1 and R2 have equal row counts", "Both are in BCNF"], 1, "The common attributes must functionally determine all of R1 or all of R2."),
            Q("Which anomaly appears when you cannot record a new department until it has an employee?", ["Update", "Insert", "Delete", "Select"], 1, "That is an insertion anomaly caused by storing department facts in the employee table."),
        ], star=True, kw="normalization 1nf 2nf 3nf bcnf anomaly partial transitive decomposition lossless dependency preserving"))

    # ------------------------------------------------------------------ 4NF 5NF
    T.append(topic("higher-nf", GB, "4NF, 5NF, 6NF and DKNF",
        "Higher normal forms deal with redundancy that functional dependencies cannot see: independent multi-valued facts and join dependencies. Interviews ask for definitions and one example of each.",
        [
            H("Multivalued dependency (MVD)"),
            P("X ↠ Y holds if, for a given X, the set of Y values is independent of the other attributes. It means a table has two or more independent 'lists' for the same X, forcing a cross product of rows."),
            TXT("""EMP_SKILL_LANG(emp, skill, language)     -- skills and languages are independent
 Asha  SQL     English
 Asha  SQL     Hindi
 Asha  Python  English
 Asha  Python  Hindi

emp ↠ skill   and   emp ↠ language
Redundancy: adding one new language for Asha needs a row for EVERY skill."""),
            H("4NF"),
            P("A relation is in 4NF if it is in BCNF and for every non-trivial MVD X ↠ Y, X is a super key. Fix: split into independent tables."),
            TXT("""EMP_SKILL(emp, skill)       EMP_LANG(emp, language)"""),
            UL("A trivial MVD: Y ⊆ X, or X ∪ Y = all attributes of R.",
               "Every FD is an MVD (X → Y implies X ↠ Y), so 4NF implies BCNF.",
               "MVDs only occur in relations with at least three attributes."),
            H("Join dependency and 5NF (PJNF)"),
            P("A join dependency says a relation equals the natural join of some of its projections. **5NF** (project-join normal form): every non-trivial join dependency is implied by the candidate keys. A relation not in 5NF cannot be split into two lossless pieces, but can be split into three or more."),
            TXT("""SUPPLIES(supplier, part, project)  with the rule:
  if S supplies part P, P is used in project J, and S supplies to J, then S supplies P to J.

No FD or MVD helps, but the table equals the join of three pairs:
  SP(supplier, part)   PJ(part, project)   SJ(supplier, project)
This 3-way decomposition is 5NF."""),
            H("6NF and DKNF"),
            UL("**6NF:** every join dependency is trivial, so each table has the key plus at most one other attribute. Used in temporal / anchor modelling and data warehouses to track history per attribute.",
               "**DKNF (domain-key normal form):** every constraint is a logical consequence of domain constraints and key constraints. It is the theoretical ideal; there is no general algorithm to reach it.",
               "**EKNF** (elementary key) sits between 3NF and BCNF; rarely asked."),
            H("The hierarchy"),
            TXT("""1NF  ⊃  2NF  ⊃  3NF  ⊃  BCNF  ⊃  4NF  ⊃  5NF  ⊃  6NF   (each is a subset of the previous)
DKNF is a different axis: it guarantees no anomalies at all."""),
            TBL(["NF", "Dependency type it handles", "Typical sign you have a violation"],
                ["2NF", "Partial FD", "Composite key and some columns depend on only one part"],
                ["3NF", "Transitive FD", "A column that describes another non-key column"],
                ["BCNF", "FD whose left side is not a key", "Overlapping candidate keys"],
                ["4NF", "Multi-valued dependency", "Cross product of two independent lists in one table"],
                ["5NF", "Join dependency", "Rows only reconstructable by a 3-way join"]),
            ASK("\"Explain 4NF with an example.\" Use employee-skill-language: skills and languages are independent facts about an employee, so keep them in separate tables to avoid cross-product rows."),
        ],
        [
            Q("4NF is violated when a relation has:", ["A partial dependency", "A non-trivial multi-valued dependency whose left side is not a super key", "A transitive dependency", "A non-prime attribute"], 1, "4NF = BCNF + every non-trivial MVD has a super key on the left."),
            Q("Table EMP(emp, skill, language) where skills and languages are independent is best fixed by:", ["Making emp the primary key", "Splitting into (emp, skill) and (emp, language)", "Adding a surrogate key", "Merging skill and language into one column"], 1, "Independent multi-valued facts belong in separate tables."),
            Q("5NF is also called:", ["Domain-key normal form", "Project-join normal form", "Elementary key normal form", "Boyce-Codd normal form"], 1, "PJNF, because it deals with join dependencies."),
            Q("Which statement is true?", ["Every 4NF relation is in BCNF", "Every BCNF relation is in 4NF", "5NF is weaker than 3NF", "6NF allows non-trivial join dependencies"], 0, "The chain runs 1NF ⊃ 2NF ⊃ 3NF ⊃ BCNF ⊃ 4NF ⊃ 5NF."),
            Q("Which normal form guarantees no anomalies because all constraints follow from domains and keys?", ["BCNF", "4NF", "5NF", "DKNF"], 3, "Domain-key normal form."),
        ], kw="4nf 5nf 6nf dknf mvd multivalued join dependency pjnf"))

    # ------------------------------------------------------------------ transactions
    T.append(topic("transactions", GC, "Transactions, ACID, schedules and serializability",
        "A transaction is a unit of work that must succeed entirely or not at all. This topic explains the ACID guarantees, the problems that appear when transactions interleave, and how to decide whether a schedule is correct.",
        [
            H("ACID"),
            TBL(["Property", "Meaning", "Example", "Enforced by"],
                ["Atomicity", "All operations happen or none do", "Transfer: debit and credit both commit or both roll back", "Undo log / rollback"],
                ["Consistency", "A transaction moves the database from one valid state to another; constraints hold", "Total money before = total after; no FK violated", "Constraints, triggers, application logic"],
                ["Isolation", "Concurrent transactions behave as if run one after another", "Two transfers do not see each other's half-done work", "Locks, MVCC"],
                ["Durability", "Once committed, it survives crashes", "Power cut after COMMIT does not lose the transfer", "Write-ahead log, fsync"]),
            H("Transaction states"),
            TXT("""Active -> Partially committed -> Committed -> (Terminated)
   |              |
   v              v
 Failed  ------> Aborted -> (rolled back, restart or kill) -> Terminated"""),
            UL("**Active:** executing. **Partially committed:** last statement run, not yet durable. **Committed:** changes are permanent. **Failed:** cannot continue. **Aborted:** rolled back."),
            H("Problems when transactions interleave"),
            TBL(["Anomaly", "What happens"],
                ["Dirty read", "T2 reads a value T1 changed but has not committed; T1 then rolls back"],
                ["Non-repeatable read", "T1 reads a row twice; T2 updated and committed it in between, so the values differ"],
                ["Phantom read", "T1 runs the same range query twice; T2 inserted or deleted a matching row in between"],
                ["Lost update", "T1 and T2 read the same value, both write; one write overwrites the other"],
                ["Write skew", "Two transactions read overlapping data, each writes something different based on it, and together they break a rule (two doctors both go off call)"]),
            H("Schedules"),
            UL("**Serial schedule:** transactions run one after another. Always correct, no concurrency.",
               "**Serializable schedule:** interleaved but equivalent to some serial order.",
               "**Conflicting operations** belong to different transactions, touch the same item and at least one is a write: R-W, W-R, W-W."),
            H("Conflict serializability and the precedence graph"),
            OL("Draw a node for each transaction.",
               "Draw an edge Ti → Tj for each conflicting pair where Ti's operation comes first.",
               "The schedule is conflict-serializable iff the graph has **no cycle**. A topological order gives an equivalent serial schedule."),
            TXT("""S:  R1(A)  W1(A)  R2(A)  W2(A)  R1(B)  W1(B)
Conflicts on A: W1(A)->R2(A), W1(A)->W2(A), R1(A)->W2(A) all give T1 -> T2
Conflicts on B: only T1 touches B.
Graph: T1 -> T2, no cycle => conflict-serializable, equivalent to T1 then T2.

S2: R1(A) R2(A) W1(A) W2(A)
R1(A)->W2(A) gives T1->T2;  R2(A)->W1(A) gives T2->T1  => cycle => NOT serializable (this is a lost update)."""),
            P("**View serializability** is a weaker test (same initial reads, same final writes, same read-from relations). Every conflict-serializable schedule is view-serializable; the reverse needs blind writes. Deciding view serializability is NP-complete."),
            H("Recoverability"),
            TBL(["Class", "Rule", "Notes"],
                ["Recoverable", "If T2 reads data written by T1, T1 must commit before T2 commits", "Otherwise a rollback of T1 leaves T2 committed on bad data"],
                ["Cascadeless (ACA)", "T2 reads only data already committed by others", "Avoids cascading rollbacks"],
                ["Strict", "No read OR write of an item until the last writer has committed or aborted", "Easiest to recover; what strict 2PL produces"]),
            P("Strict ⊂ Cascadeless ⊂ Recoverable. A schedule can be serializable yet not recoverable."),
            H("SQL isolation levels"),
            TBL(["Level", "Dirty read", "Non-repeatable read", "Phantom"],
                ["READ UNCOMMITTED", "Possible", "Possible", "Possible"],
                ["READ COMMITTED", "Prevented", "Possible", "Possible"],
                ["REPEATABLE READ", "Prevented", "Prevented", "Possible (standard)"],
                ["SERIALIZABLE", "Prevented", "Prevented", "Prevented"]),
            PG("PostgreSQL treats READ UNCOMMITTED as READ COMMITTED (it never allows dirty reads). Its REPEATABLE READ is snapshot isolation and also prevents phantoms. SERIALIZABLE uses SSI and may abort with 'could not serialize'; retry. Default: READ COMMITTED."),
            MY("MySQL InnoDB default is REPEATABLE READ. InnoDB uses next-key locks to prevent most phantoms for locking reads. SERIALIZABLE turns plain SELECTs into shared-locking reads."),
            ASK("\"Which isolation level is default in PostgreSQL / MySQL?\" PostgreSQL: READ COMMITTED. MySQL InnoDB: REPEATABLE READ."),
        ],
        [
            Q("Which property is implemented mainly by the write-ahead log and forced flush on commit?", ["Atomicity", "Consistency", "Isolation", "Durability"], 3, "Durability: the commit record must be on stable storage. The log also supports atomicity via undo."),
            Q("T2 reads a row T1 changed but T1 later rolls back. This is a:", ["Dirty read", "Phantom read", "Lost update", "Non-repeatable read"], 0, "Reading uncommitted data = dirty read."),
            Q("A schedule is conflict-serializable if its precedence graph:", ["Has a cycle", "Has no cycle", "Has exactly one edge", "Is empty"], 1, "Acyclic precedence graph = conflict-serializable."),
            Q("S: R1(A) R2(A) W1(A) W2(A). Is it conflict-serializable?", ["Yes, T1 then T2", "Yes, T2 then T1", "No, it has a cycle", "Cannot tell"], 2, "R1(A)->W2(A) gives T1->T2 and R2(A)->W1(A) gives T2->T1: a cycle."),
            Q("Which isolation level prevents dirty reads but allows non-repeatable reads?", ["READ UNCOMMITTED", "READ COMMITTED", "REPEATABLE READ", "SERIALIZABLE"], 1, "READ COMMITTED: you only see committed data, but a second read may see a newer committed value."),
            Q("Default isolation level of MySQL InnoDB is:", ["READ UNCOMMITTED", "READ COMMITTED", "REPEATABLE READ", "SERIALIZABLE"], 2, "PostgreSQL uses READ COMMITTED, InnoDB uses REPEATABLE READ."),
        ], star=True, kw="transaction acid isolation level dirty read phantom serializability precedence graph recoverable cascadeless strict"))

    # ------------------------------------------------------------------ concurrency
    T.append(topic("concurrency", GC, "Concurrency control: locking, deadlocks, timestamps, MVCC",
        "How the DBMS makes interleaved transactions behave like serial ones.",
        [
            H("Lock modes and compatibility"),
            TBL(["", "Held: S (shared)", "Held: X (exclusive)"],
                ["Request S", "Granted", "Wait"],
                ["Request X", "Wait", "Wait"]),
            P("Shared lock = read, many allowed. Exclusive lock = write, only one holder."),
            H("Two-phase locking (2PL)"),
            UL("**Growing phase:** a transaction may acquire locks but not release any.",
               "**Shrinking phase:** it may release locks but not acquire any.",
               "2PL guarantees conflict serializability (the lock point gives the serial order) but allows deadlocks and cascading rollbacks.",
               "**Strict 2PL:** holds all EXCLUSIVE locks until commit/abort. Gives strict (and so cascadeless) schedules.",
               "**Rigorous 2PL:** holds ALL locks until commit.",
               "**Conservative 2PL:** acquires all locks before starting; deadlock-free but impractical (must know the read/write sets)."),
            H("Deadlock"),
            P("T1 holds a lock on A and wants B; T2 holds B and wants A. Neither can proceed."),
            UL("**Detection:** build a wait-for graph; a cycle means deadlock. Pick a victim and abort it (PostgreSQL does this after deadlock_timeout; InnoDB detects immediately).",
               "**Prevention with timestamps:** older transaction = smaller timestamp. **Wait-die:** if the requester is older it waits, if younger it dies (aborts). **Wound-wait:** if the requester is older it wounds (aborts) the holder, if younger it waits.",
               "**Timeout:** abort anything waiting too long.",
               "**Avoidance in code:** always lock rows in a consistent order (e.g. ascending id)."),
            TRAP("In wait-die only younger transactions are killed and they restart with their ORIGINAL timestamp, so they eventually become old and cannot starve."),
            H("Multiple granularity locking"),
            P("Locks can sit on a database, table, page or row. **Intention locks** on the ancestors say what is happening below: IS (intend to take S below), IX (intend to take X below), SIX (S on the whole plus X on some parts). A table lock request checks compatibility with intention locks instead of scanning every row."),
            H("Timestamp ordering"),
            UL("Each transaction gets a timestamp TS(T) at start. Each item keeps the largest read timestamp RTS and write timestamp WTS.",
               "Read(X) by T: if TS(T) < WTS(X) the value was written by a younger transaction, so T rolls back; otherwise allowed and RTS = max(RTS, TS(T)).",
               "Write(X) by T: if TS(T) < RTS(X) or TS(T) < WTS(X), T rolls back. **Thomas write rule:** if only TS(T) < WTS(X) the obsolete write is just ignored.",
               "No locks, so no deadlock, but possible starvation and cascading aborts."),
            H("MVCC (multi-version concurrency control)"),
            P("Keep several versions of a row. Readers see the snapshot that was current when their transaction (or statement) began, so **readers never block writers and writers never block readers**. Writers still block other writers on the same row."),
            PG("PostgreSQL stores old versions as dead tuples inside the table itself; VACUUM cleans them. Each row has hidden xmin/xmax transaction ids."),
            MY("InnoDB keeps old versions in the undo log (rollback segment) and purges them when no snapshot needs them."),
            H("Optimistic concurrency control"),
            P("Three phases: read (work on private copies), validate (check no conflicting commit happened), write. Good when conflicts are rare. In application code you implement it with a version column: UPDATE ... WHERE id = ? AND version = ?, then check rows affected."),
            SQL("""UPDATE employees SET salary = 99000, name = name
WHERE id = 2 AND salary = 98000;   -- 0 rows affected means someone changed it first""", "optimistic update by comparing old value", run=True),
            H("Explicit locks in SQL"),
            PGSQL("""BEGIN;
SELECT * FROM accounts WHERE id = 1 FOR UPDATE;         -- X lock the row
SELECT * FROM jobs WHERE state = 'new' LIMIT 1 FOR UPDATE SKIP LOCKED;  -- queue worker pattern
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
COMMIT;"""),
            ASK("\"How do you prevent lost updates?\" SELECT ... FOR UPDATE, SERIALIZABLE isolation, atomic UPDATE balance = balance - 100, or optimistic version checks."),
        ],
        [
            Q("In strict 2PL a transaction releases its exclusive locks:", ["Right after use", "At commit or abort", "Never", "Before acquiring any other lock"], 1, "Holding X locks until the end yields strict, cascadeless schedules."),
            Q("In the wait-die scheme, when an OLDER transaction requests a lock held by a younger one:", ["Older dies", "Older waits", "Younger is wounded", "Both abort"], 1, "Wait-die: older waits, younger dies."),
            Q("A deadlock is detected by finding:", ["A cycle in the wait-for graph", "A cycle in the ER diagram", "A table with no PK", "Two shared locks"], 0, "Cycle in the wait-for graph = deadlock."),
            Q("In MVCC, readers:", ["Block writers", "Are blocked by writers", "Do not block and are not blocked by writers", "Always see uncommitted data"], 2, "Snapshots mean read and write don't block each other."),
            Q("Which lock modes are compatible?", ["S and X", "X and X", "S and S", "X and S on the same row"], 2, "Only shared with shared."),
            Q("Under the Thomas write rule, a write with TS(T) < WTS(X) (and TS(T) >= RTS(X)) is:", ["Rolled back", "Ignored", "Applied", "Converted to a read"], 1, "The write is obsolete, so it is skipped instead of aborting."),
        ], kw="locking 2pl deadlock wait-die wound-wait timestamp mvcc optimistic lock for update skip locked"))

    # ------------------------------------------------------------------ recovery
    T.append(topic("recovery", GC, "Recovery: logs, WAL, checkpoints, ARIES",
        "What the database does after a crash so committed work survives (durability) and uncommitted work disappears (atomicity).",
        [
            H("Failure types"),
            UL("**Transaction failure:** logical error or deadlock victim. Undo the one transaction.",
               "**System crash:** memory lost, disk fine. Redo committed work, undo uncommitted work.",
               "**Media failure:** disk lost. Restore from backup and replay the log (point-in-time recovery)."),
            H("The log and write-ahead logging (WAL)"),
            P("The log is a sequential file of records like <T1, start>, <T1, A, old=500, new=400>, <T1, commit>. **WAL rule:** a log record describing a change must reach disk BEFORE the changed data page does, and all of a transaction's log records must be on disk before it commits."),
            TBL(["Policy", "Meaning", "Needs"],
                ["STEAL", "Dirty pages of uncommitted transactions may be written to disk", "UNDO"],
                ["NO-STEAL", "Uncommitted pages stay in memory", "No undo, but memory pressure"],
                ["FORCE", "All of a transaction's pages are written to disk at commit", "No REDO, but slow commits"],
                ["NO-FORCE", "Pages may be written lazily after commit", "REDO"]),
            P("Real systems use **STEAL + NO-FORCE**, which is why they need both undo and redo logging."),
            H("Update strategies"),
            UL("**Deferred update:** changes written to the DB only after commit. Needs REDO only.",
               "**Immediate update:** changes may be written before commit. Needs UNDO and REDO."),
            H("Checkpoints"),
            P("Periodically flush dirty pages and write a checkpoint record that lists active transactions. After a crash, recovery starts from the last checkpoint instead of the start of the log."),
            H("Recovery steps (after a crash)"),
            OL("Find the last checkpoint.",
               "**Redo list:** transactions with both <start> and <commit> after the checkpoint. Reapply their changes (REDO).",
               "**Undo list:** transactions with <start> but no <commit>. Roll back their changes in reverse order (UNDO), writing compensation records."),
            H("ARIES in three passes"),
            UL("**Analysis:** from the checkpoint, rebuild the dirty page table and the list of active transactions.",
               "**Redo:** repeat history. Reapply every logged change (even of transactions that will be undone) from the earliest needed point, using page LSNs to skip changes already on disk.",
               "**Undo:** roll back the losers, writing compensation log records (CLRs) so a crash during recovery is safe."),
            P("Terms: **LSN** (log sequence number), **dirty page table**, **transaction table**, **pageLSN**, **CLR**."),
            H("Shadow paging"),
            P("Keep a page table; on update write a new copy of the page and switch the table pointer atomically at commit. No log needed, but fragmentation and costly copying. Rarely used now."),
            H("Backups"),
            UL("**Logical** (pg_dump, mysqldump): SQL or data export, portable, slower to restore.",
               "**Physical** (file copy, pg_basebackup, xtrabackup) plus archived WAL / binary logs: allows **point-in-time recovery**."),
            ASK("\"What is WAL and why does it exist?\" Log first, data later. It turns random page writes into sequential log appends (fast commits) and makes crash recovery possible."),
        ],
        [
            Q("Write-ahead logging requires that:", ["Data pages are written before log records", "Log records reach disk before the corresponding data pages", "The log is kept only in memory", "Commits skip the log"], 1, "WAL = log first."),
            Q("A system with STEAL and NO-FORCE needs:", ["Only redo", "Only undo", "Both undo and redo", "Neither"], 2, "STEAL requires undo, NO-FORCE requires redo."),
            Q("After a crash, transactions with a start and commit record after the last checkpoint are:", ["Undone", "Redone", "Ignored", "Restarted"], 1, "Committed work must survive, so it is redone."),
            Q("Which ARIES pass repeats history?", ["Analysis", "Redo", "Undo", "Checkpoint"], 1, "Redo reapplies all logged changes; Undo then rolls back losers."),
            Q("Point-in-time recovery needs a base backup plus:", ["The query cache", "Archived transaction logs (WAL / binlog)", "The index files only", "A schema dump"], 1, "Replay the log forward to the chosen moment."),
        ], kw="recovery wal log checkpoint aries undo redo steal force shadow paging backup"))

    # ------------------------------------------------------------------ indexing
    T.append(topic("indexing-theory", GC, "File organisation and indexing (B+ tree, hashing)",
        "An index is a separate structure that lets the database find rows without scanning the table. Know the kinds, the B+ tree, the cost arithmetic, and when an index helps or hurts.",
        [
            H("Storage basics"),
            UL("Data is stored in fixed-size **blocks / pages** (8 KB in PostgreSQL, 16 KB in InnoDB). I/O cost is counted in block reads.",
               "**Blocking factor** bf = floor(block size / record size). Blocks needed = ceil(records / bf).",
               "**Heap file:** unordered, fast insert, search is a full scan. **Sorted file:** binary search possible. **Hashed file:** direct location by hash."),
            TXT("""30,000 records, record = 100 bytes, block = 1,000 bytes
bf = 1000 / 100 = 10 records per block
blocks = 30,000 / 10 = 3,000
linear scan = 3,000 block reads (worst), binary search on sorted file = ceil(log2 3000) = 12"""),
            H("Types of indexes"),
            TBL(["Type", "Definition"],
                ["Primary index", "On the ordering key field of a sorted file; usually sparse"],
                ["Clustering index", "On a non-key ordering field of a sorted file"],
                ["Secondary index", "On a non-ordering field; must be dense; many per table"],
                ["Dense", "An index entry for every record"],
                ["Sparse", "An entry per block; file must be sorted on that key"],
                ["Multilevel", "An index on the index; B-trees are the balanced form"],
                ["Unique", "Also enforces uniqueness"],
                ["Composite (multicolumn)", "On several columns; usable by the leftmost-prefix rule"],
                ["Covering", "Contains every column the query needs, so the table is never visited (index-only scan)"]),
            H("B-tree vs B+ tree"),
            TBL(["", "B-tree", "B+ tree"],
                ["Data pointers", "In every node", "Only in leaf nodes"],
                ["Internal nodes hold", "Keys + data pointers", "Keys only (more keys per node, higher fan-out, shorter tree)"],
                ["Leaves linked", "No", "Yes, in a sequence: great for range scans"],
                ["Search cost", "Variable", "Always root-to-leaf (same height)"]),
            UL("A B+ tree of order p: internal node holds up to p-1 keys and p pointers; leaf holds up to p-1 key/pointer pairs; nodes are at least half full.",
               "Height grows like log base fan-out of N. With fan-out of a few hundred, 3 or 4 levels hold hundreds of millions of rows.",
               "Lookup, insert and delete are O(log N). Range queries find the first key then walk the leaf chain.",
               "Order calculation: block 1024 B, key 10 B, pointer 6 B → p×6 + (p-1)×10 ≤ 1024 → p = 64 (internal node fits 64 pointers and 63 keys)."),
            H("Hash indexes"),
            UL("Equality only, O(1) average, no ranges or ordering.",
               "**Static hashing:** fixed number of buckets, overflow chains degrade performance.",
               "**Extendible hashing:** a directory doubles when a bucket splits. **Linear hashing:** splits buckets in a round-robin order without a directory.",
               "Bitmap indexes: one bit-vector per distinct value, good for low-cardinality columns in warehouses (Oracle, not default in PostgreSQL/MySQL)."),
            H("Index design rules"),
            UL("Index columns used in WHERE, JOIN ON, ORDER BY and GROUP BY of frequent queries.",
               "Foreign key columns are not indexed automatically in PostgreSQL (and InnoDB creates one if none exists); index them for joins and for fast parent deletes.",
               "Composite index (a, b, c) serves filters on a; a,b; a,b,c; but not b alone or c alone.",
               "Put equality columns first, then the range column.",
               "**Selectivity:** an index on a column with few distinct values (gender) rarely helps. High-cardinality columns are best.",
               "Indexes cost writes and space: every INSERT, UPDATE of an indexed column and DELETE must maintain them.",
               "A function on the column defeats the index: WHERE UPPER(name) = 'ASHA' cannot use an index on name (use an expression index in PostgreSQL, or a generated column in MySQL).",
               "A leading wildcard defeats it: LIKE '%son' scans; LIKE 'son%' can use the index."),
            PG("Index types: **btree** (default), **hash**, **GIN** (arrays, jsonb, full-text), **GiST** (geometry, ranges, nearest neighbour), **SP-GiST**, **BRIN** (very large, naturally ordered tables like time-series). Partial and expression indexes are supported."),
            MY("InnoDB tables ARE a B+ tree on the primary key (clustered index). Secondary indexes store the primary key value as the row pointer, so a long primary key bloats every secondary index. MyISAM has a heap with separate indexes. Also FULLTEXT and SPATIAL indexes."),
            ASK("\"Clustered vs non-clustered index?\" Clustered: the table rows themselves are stored in key order (one per table, InnoDB primary key; PostgreSQL has CLUSTER as a one-time reorder only). Non-clustered: separate structure with pointers to the rows (many per table)."),
        ],
        [
            Q("3,200 records of 200 bytes each with 1,000-byte blocks occupy:", ["640 blocks", "800 blocks", "3,200 blocks", "160 blocks"], 0, "bf = 1000 / 200 = 5 records per block, so 3200 / 5 = 640 blocks."),
            Q("Why do B+ trees beat B-trees for range queries?", ["They store fewer keys", "Leaf nodes are linked in sorted order", "They have no leaves", "They use hashing"], 1, "Find the start, then follow leaf pointers."),
            Q("An index on (last_name, first_name) can help which query?", ["WHERE first_name = 'Asha'", "WHERE last_name = 'Rao'", "WHERE first_name LIKE '%a'", "WHERE UPPER(last_name) = 'RAO'"], 1, "Leftmost-prefix rule; the other filters skip the first column or wrap it in a function."),
            Q("Which is true of a hash index?", ["Supports ORDER BY", "Supports range queries", "Fast for equality lookups", "Is the default in PostgreSQL"], 2, "Hashing gives O(1) equality but no ordering."),
            Q("In InnoDB a secondary index entry stores:", ["The row's physical address", "The primary key value", "A copy of the whole row", "Nothing"], 1, "Lookup through a secondary index then goes through the clustered primary key index."),
        ], kw="index btree b+ tree hash clustered covering composite selectivity blocking factor"))

    # ------------------------------------------------------------------ query processing
    T.append(topic("query-processing", GC, "Query processing and optimization",
        "How SQL text becomes an execution plan, and how to read it. This is what 'optimize this slow query' questions are about.",
        [
            H("The pipeline"),
            TXT("""SQL text -> parser (syntax, names) -> rewriter (views expanded)
        -> optimizer (choose a plan using statistics) -> executor (run the plan)"""),
            H("Heuristic rules"),
            UL("Perform selections as early as possible (push σ down).",
               "Perform projections early, but keep join columns.",
               "Replace Cartesian product followed by selection with a join.",
               "Join the smallest intermediate results first; choose join order with the fewest rows.",
               "Use indexes for selective predicates."),
            H("Join algorithms"),
            TBL(["Algorithm", "Idea", "Best when"],
                ["Nested loop", "For each outer row, scan the inner table", "Tiny inputs, or inner table indexed (index nested loop)"],
                ["Block nested loop", "Read the outer in blocks, scan inner once per block", "No index, small outer"],
                ["Hash join", "Build a hash table on the smaller input, probe with the other", "Large unsorted inputs, equality joins"],
                ["Sort-merge join", "Sort both inputs on the join key, merge", "Inputs already sorted, or non-equality range joins"]),
            TXT("""Cost with nr, ns blocks for outer/inner and M buffer blocks:
 nested loop (block):  nr + ceil(nr / (M-2)) * ns
 hash join:            3 * (nr + ns)   when the build side fits after one partitioning
 sort-merge:           sort cost of each input + (nr + ns)"""),
            H("Reading a plan"),
            PGSQL("""EXPLAIN ANALYZE
SELECT e.name FROM employees e JOIN departments d ON d.id = e.dept_id WHERE d.name = 'Data';
-- look for: Seq Scan (full table), Index Scan, Hash Join / Nested Loop / Merge Join,
-- estimated rows vs actual rows (big mismatch means stale statistics -> run ANALYZE)"""),
            MYSQL("""EXPLAIN SELECT e.name FROM employees e JOIN departments d ON d.id = e.dept_id WHERE d.name = 'Data';
-- columns to read: type (ALL = full scan, ref/eq_ref/const = index use), key, rows, Extra (Using filesort, Using temporary are warnings)
EXPLAIN ANALYZE ...   -- MySQL 8.0.18+ shows real timings"""),
            SQL("""EXPLAIN QUERY PLAN SELECT * FROM employees WHERE dept_id = 2;""", "SQLite's own flavour, runs here", run=True),
            H("Writing SARGable queries"),
            P("A predicate is SARGable (search-argument-able) if the engine can use an index for it. Keep the column bare on one side."),
            TBL(["Slow (cannot use an index on the column)", "Fast rewrite"],
                ["WHERE YEAR(hire_date) = 2022", "WHERE hire_date >= '2022-01-01' AND hire_date < '2023-01-01'"],
                ["WHERE salary * 12 > 1200000", "WHERE salary > 100000"],
                ["WHERE name LIKE '%an'", "full-text / trigram index, or reverse-string index"],
                ["WHERE UPPER(city) = 'PUNE'", "expression index on UPPER(city), or store normalised"],
                ["WHERE a = 1 OR b = 2", "UNION of two indexed queries, or a bitmap-or plan"],
                ["WHERE col::text = '5' (cast on the column)", "compare with the column's own type"]),
            H("Common tuning moves"),
            UL("Select only the columns you need, not SELECT *.",
               "Add an index for the filter + join columns; check with EXPLAIN that it is used.",
               "Replace correlated subqueries with joins or window functions.",
               "Use EXISTS instead of IN with huge lists, and keyset pagination (WHERE id > last_id LIMIT 50) instead of large OFFSET.",
               "Batch inserts (multi-row INSERT, COPY / LOAD DATA).",
               "Keep statistics fresh: ANALYZE in PostgreSQL, ANALYZE TABLE in MySQL.",
               "Avoid functions on indexed columns; avoid implicit type conversions (comparing a varchar column to a number).",
               "Partition very large tables and archive old data."),
            ASK("\"A query is slow, what do you do?\" Run EXPLAIN (ANALYZE). Look for full scans, wrong row estimates, sorts and temp tables. Add or fix an index, rewrite non-SARGable predicates, update statistics, cut columns and rows early."),
        ],
        [
            Q("Which rule belongs to heuristic optimization?", ["Delay selections until after joins", "Push selections down before joins", "Always use nested loop", "Always select all columns"], 1, "Filtering early reduces the size of intermediate results."),
            Q("Which predicate can use a plain B-tree index on hire_date?", ["WHERE YEAR(hire_date) = 2022", "WHERE hire_date >= '2022-01-01' AND hire_date < '2023-01-01'", "WHERE CAST(hire_date AS TEXT) LIKE '2022%'", "WHERE hire_date + 1 > '2022-01-01'"], 1, "The bare column is compared to constants."),
            Q("A hash join is typically chosen when:", ["Inputs are tiny", "Inputs are large, unsorted, joined on equality", "The join is a < comparison", "There is an index on both sides"], 1, "Hash join excels for large equality joins."),
            Q("In EXPLAIN output, 'Seq Scan' (PostgreSQL) or type=ALL (MySQL) means:", ["The index was used", "A full table scan", "A hash join", "A constant lookup"], 1, "No index was used for that access."),
            Q("Stale optimizer statistics are fixed by:", ["VACUUM FULL only", "ANALYZE", "TRUNCATE", "Restarting the app"], 1, "ANALYZE (PostgreSQL) or ANALYZE TABLE (MySQL) refreshes the stats."),
        ], kw="query processing optimizer explain join algorithm hash nested loop merge sargable tuning"))

    # ------------------------------------------------------------------ distributed
    T.append(topic("distributed-olap", GC, "OLTP vs OLAP, warehousing, NoSQL, CAP, replication, sharding",
        "The wider picture beyond a single relational server. Short definitions are enough for most interviews, but you must be crisp.",
        [
            H("OLTP vs OLAP"),
            TBL(["", "OLTP", "OLAP"],
                ["Purpose", "Run the business (orders, payments)", "Analyse the business (trends, reports)"],
                ["Operations", "Many short reads/writes of single rows", "Few huge scans and aggregations"],
                ["Design", "Highly normalized (3NF)", "Denormalized star / snowflake schema"],
                ["Data", "Current, detailed", "Historical, summarised"],
                ["Metric", "Transactions per second", "Query response time on big data"],
                ["Examples", "PostgreSQL, MySQL", "Redshift, BigQuery, Snowflake, ClickHouse"]),
            H("Data warehouse schemas"),
            UL("**Fact table:** measurable events (sales amount, quantity) with foreign keys to dimensions. Very large.",
               "**Dimension tables:** descriptive context (customer, product, date, store). Small, wide, denormalized.",
               "**Star schema:** one fact table surrounded by flat dimensions. **Snowflake:** dimensions normalized into sub-tables (less storage, more joins).",
               "**ETL:** extract, transform, load. **ELT** loads first and transforms in the warehouse.",
               "OLAP operations: **roll-up** (aggregate up a hierarchy), **drill-down**, **slice** (fix one dimension), **dice** (fix several), **pivot**. SQL: GROUP BY ROLLUP / CUBE / GROUPING SETS."),
            H("NoSQL families"),
            TBL(["Type", "Model", "Examples", "Good for"],
                ["Key-value", "key -> blob", "Redis, DynamoDB", "Caching, sessions"],
                ["Document", "JSON documents", "MongoDB, Couchbase", "Flexible schema, aggregates read as a unit"],
                ["Wide-column", "Row key + column families", "Cassandra, HBase", "Huge write volumes, time-series"],
                ["Graph", "Nodes and edges", "Neo4j", "Relationships, recommendations"]),
            H("CAP, ACID and BASE"),
            UL("**CAP theorem:** in the presence of a network partition a distributed store can guarantee only one of Consistency and Availability. (Partition tolerance is not optional.)",
               "CP systems refuse requests to stay consistent (HBase, MongoDB by default). AP systems keep answering and reconcile later (Cassandra, DynamoDB).",
               "**BASE:** Basically Available, Soft state, Eventually consistent: the NoSQL counterpart to ACID.",
               "**PACELC** extends CAP: else, trade latency against consistency."),
            H("Scaling out"),
            UL("**Replication:** copies of the same data. Primary-replica (writes to primary, reads from replicas), synchronous (safe, slower) or asynchronous (fast, replica lag). Gives availability and read scale.",
               "**Partitioning:** split one big table inside one server (range, list, hash). Helps pruning and maintenance.",
               "**Sharding:** split data across servers by a shard key. Gives write scale. Cross-shard joins and transactions are hard; a bad shard key creates hot spots.",
               "**Distributed transactions:** two-phase commit (2PC): prepare/vote, then commit/abort. Blocks if the coordinator dies. Sagas (compensating actions) are the usual alternative.",
               "**Consistency models:** strong, eventual, read-your-writes, causal."),
            ASK("\"When would you choose NoSQL over a relational DB?\" Huge scale with simple access patterns, flexible or changing schema, very high write throughput, or data that is naturally a document or graph. Stay relational for multi-row transactions, complex joins and reporting."),
        ],
        [
            Q("A star schema consists of:", ["A fact table with normalized sub-dimensions", "A fact table surrounded by denormalized dimension tables", "Only dimension tables", "A single flat table"], 1, "Snowflake normalizes dimensions; star keeps them flat."),
            Q("According to CAP, during a network partition a system must choose between:", ["Consistency and Availability", "Atomicity and Durability", "Speed and Cost", "Isolation and Consistency"], 0, "Partition tolerance is required, so pick C or A."),
            Q("Splitting rows of one logical table across several servers by a key is:", ["Replication", "Sharding", "Normalization", "Indexing"], 1, "Sharding = horizontal partitioning across machines."),
            Q("Which is an OLAP operation?", ["INSERT a new order", "Roll-up from city to country", "Rollback", "Row-level lock"], 1, "Roll-up aggregates along a dimension hierarchy."),
            Q("In two-phase commit the coordinator first asks participants to:", ["Commit", "Prepare and vote", "Rollback", "Take a snapshot"], 1, "Phase 1: prepare/vote. Phase 2: commit or abort."),
        ], kw="oltp olap warehouse star snowflake nosql cap base replication sharding partitioning 2pc"))

    return T
