"""Study guide, part 1: DBMS fundamentals, ER model, relational model and keys, relational algebra, functional dependencies."""
from mat_common import *

GA = "A. DBMS fundamentals"
GB = "B. Relational model and normalization"


def build():
    T = []

    # ------------------------------------------------------------------ 1
    T.append(topic("dbms-intro", GA, "DBMS, RDBMS, architecture and SQL families",
        "A **database** is an organised collection of related data. A **DBMS** is the software that stores, retrieves, protects and shares it. An **RDBMS** is a DBMS built on the relational model: data lives in tables (relations) linked by keys. PostgreSQL, MySQL, Oracle and SQL Server are RDBMSs.",
        [
            H("File system vs DBMS"),
            TBL(["Problem in file systems", "How a DBMS fixes it"],
                ["Redundancy and inconsistency: same data copied in many files", "One central store; normalization removes duplicates"],
                ["Hard to query: every new question needs a new program", "A declarative query language (SQL)"],
                ["No atomic updates: a crash half-way leaves files wrong", "Transactions: all or nothing"],
                ["Concurrent access corrupts data", "Locking and MVCC isolate users"],
                ["No security granularity", "Users, roles, GRANT/REVOKE, row-level policies"],
                ["Integrity rules live in application code", "Constraints enforced by the engine (PK, FK, CHECK)"],
                ["Programs depend on file layout", "Data independence (see below)"]),
            H("Three-schema architecture"),
            UL("**External level (view level):** what each user group sees. Views live here.",
               "**Conceptual (logical) level:** the whole database structure: tables, columns, constraints. One per database.",
               "**Internal (physical) level:** files, pages, indexes, storage format."),
            P("The mappings between levels give **data independence**."),
            TBL(["Independence", "Meaning", "Example"],
                ["Logical data independence", "Change the conceptual schema without changing external views or programs", "Add a column to a table; existing views still work"],
                ["Physical data independence", "Change the physical storage without changing the conceptual schema", "Add an index or move a table to another disk; queries are unchanged"]),
            NOTE("Physical independence is easier to achieve and is the one every real DBMS delivers. Logical independence is harder because programs often depend on column lists."),
            H("Tiers"),
            UL("**1-tier:** user works directly on the DBMS (psql, MySQL shell).",
               "**2-tier:** client application talks straight to the DB server (JDBC/ODBC).",
               "**3-tier:** client, application server, database server. Web apps use this; the browser never touches the DB."),
            H("Components of a DBMS"),
            UL("**Query processor:** DDL interpreter, DML compiler (parser, rewriter, optimizer), executor.",
               "**Storage manager:** buffer manager, file manager, authorisation and integrity manager, transaction manager (lock manager, recovery manager).",
               "**Data dictionary (catalog):** metadata about tables, columns, indexes, users. In PostgreSQL see pg_catalog and information_schema; MySQL has information_schema."),
            H("SQL sub-languages"),
            TBL(["Family", "Full name", "Commands", "Purpose"],
                ["DDL", "Data Definition Language", "CREATE, ALTER, DROP, TRUNCATE, RENAME, COMMENT", "Define structure"],
                ["DML", "Data Manipulation Language", "INSERT, UPDATE, DELETE, MERGE", "Change data"],
                ["DQL", "Data Query Language", "SELECT", "Read data (some books fold it into DML)"],
                ["DCL", "Data Control Language", "GRANT, REVOKE", "Permissions"],
                ["TCL", "Transaction Control Language", "COMMIT, ROLLBACK, SAVEPOINT, SET TRANSACTION", "Group statements atomically"]),
            TRAP("TRUNCATE is DDL in the textbooks. In MySQL it commits implicitly and cannot be rolled back. In PostgreSQL it IS transactional and can be rolled back inside a transaction."),
            H("Database users"),
            UL("**DBA:** installs, tunes, secures, backs up.", "**Application programmers:** write code against the DB.", "**Naive users:** use forms and apps.", "**Sophisticated users:** write ad-hoc SQL (analysts)."),
            H("Codd's rules in one line each"),
            P("Information rule (everything is in tables), guaranteed access (table + key + column finds any value), systematic NULL treatment, active online catalog, comprehensive data sub-language, view updating, high-level insert/update/delete, physical data independence, logical data independence, integrity independence, distribution independence, non-subversion (no low-level bypass). Rule 0: the system must manage data using relational capabilities only."),
            ASK("\"Difference between DBMS and RDBMS?\" Say: DBMS may store data as files, hierarchies or documents with no required relationships; RDBMS stores data in related tables, enforces keys and constraints, supports SQL and ACID transactions, and follows Codd's rules."),
        ],
        [
            Q("Changing the storage structure of a table (adding an index) without changing queries demonstrates:", ["Logical data independence", "Physical data independence", "Referential integrity", "Normalization"], 1, "Physical layer changed, conceptual and external layers untouched."),
            Q("Which level of the three-schema architecture does a VIEW belong to?", ["Internal", "Conceptual", "External", "Physical"], 2, "Views are tailored per user group, which is the external level."),
            Q("Which of these is a DCL command?", ["TRUNCATE", "SAVEPOINT", "REVOKE", "MERGE"], 2, "GRANT and REVOKE control permissions. SAVEPOINT is TCL, MERGE is DML, TRUNCATE is DDL."),
            Q("In MySQL, TRUNCATE TABLE inside a transaction:", ["Can be rolled back", "Commits implicitly and cannot be rolled back", "Is blocked", "Only deletes uncommitted rows"], 1, "DDL statements cause an implicit commit in MySQL. PostgreSQL differs: TRUNCATE is transactional."),
            Q("The component that decides the cheapest way to execute a query is the:", ["Buffer manager", "Lock manager", "Query optimizer", "Recovery manager"], 2, "The optimizer chooses a plan from many equivalent ones using statistics and cost estimates."),
        ], star=True, kw="dbms rdbms architecture schema independence ddl dml dcl tcl codd"))

    # ------------------------------------------------------------------ 2
    T.append(topic("er-model", GA, "ER model: entities, attributes, relationships",
        "The ER model describes data before any table exists. Interviews ask you to read a scenario and draw or list entities, attributes, relationship types, cardinality and participation. Do this first, then map to tables.",
        [
            H("Building blocks"),
            TBL(["Concept", "Meaning", "Example"],
                ["Entity", "A real-world thing that can be told apart", "Student 'Asha'"],
                ["Entity set", "All entities of one type", "STUDENT"],
                ["Strong entity", "Has its own key", "STUDENT(roll_no)"],
                ["Weak entity", "No key of its own; identified through an owner entity plus a partial key (discriminator)", "DEPENDENT of EMPLOYEE (identified by employee + dependent name)"],
                ["Attribute", "Property of an entity or relationship", "name, dob"],
                ["Relationship", "Association between entity sets", "STUDENT enrolls_in COURSE"]),
            H("Kinds of attributes"),
            TBL(["Kind", "Meaning", "Example", "Drawn as"],
                ["Simple (atomic)", "Cannot be split", "age", "oval"],
                ["Composite", "Made of sub-parts", "address = street + city + pin", "oval with child ovals"],
                ["Single-valued", "One value", "dob", "oval"],
                ["Multivalued", "Many values", "phone numbers, skills", "double oval"],
                ["Derived", "Computed from others", "age from dob", "dashed oval"],
                ["Key attribute", "Identifies the entity", "roll_no", "underlined"],
                ["Partial key", "Identifies a weak entity within its owner", "dependent_name", "dashed underline"]),
            H("Relationships"),
            UL("**Degree:** unary (recursive, e.g. EMPLOYEE manages EMPLOYEE), binary (most common), ternary (three entity sets at once, e.g. SUPPLIER supplies PART to PROJECT).",
               "**Cardinality ratio:** 1:1, 1:N, N:1, M:N.",
               "**Participation:** **total** (every entity must take part, double line) or **partial** (some may not, single line).",
               "A relationship can carry its own attributes: ENROLLS has grade and semester."),
            TBL(["Scenario", "Cardinality", "Participation"],
                ["One department has many employees; each employee works in exactly one department", "DEPARTMENT 1 : N EMPLOYEE", "EMPLOYEE total, DEPARTMENT partial (a department may be empty)"],
                ["A student enrolls in many courses; a course has many students", "STUDENT M : N COURSE", "usually partial on both sides"],
                ["Each person has at most one passport; each passport belongs to exactly one person", "PERSON 1 : 1 PASSPORT", "PASSPORT total, PERSON partial"],
                ["An employee manages many employees; each employee has at most one manager", "EMPLOYEE 1 : N EMPLOYEE (recursive)", "partial on both"]),
            H("Extended ER"),
            UL("**Specialization:** split an entity set into sub-classes (EMPLOYEE into ENGINEER, MANAGER). Top-down.",
               "**Generalization:** merge similar entity sets into a super-class. Bottom-up.",
               "**Constraints on the hierarchy:** **disjoint** (an entity is in at most one subclass) vs **overlapping**; **total** (every super-class entity is in some subclass) vs **partial**.",
               "**Inheritance:** subclasses inherit the attributes and relationships of the super-class (an 'is-a' relationship).",
               "**Aggregation:** treat a relationship as an entity so it can participate in another relationship (e.g. PROJECT is_assigned_to (EMPLOYEE works_on COURSE))."),
            H("Reading a scenario"),
            P("Nouns become entities or attributes, verbs become relationships. Look for words that give cardinality: 'each', 'at most one', 'many', 'exactly one', 'may have none'. Then ask for each entity: what uniquely identifies it?"),
            TXT("""Scenario: A hospital has doctors and patients. A doctor treats many patients, a patient may see many doctors. Each visit has a date and diagnosis. Each doctor belongs to one department.

Entities     DOCTOR(doctor_id, name, phone[multi]), PATIENT(patient_id, name, dob, age[derived]), DEPARTMENT(dept_id, name)
Relationships DOCTOR  M:N  PATIENT   via TREATS(visit_date, diagnosis)
              DEPARTMENT 1:N DOCTOR  via WORKS_IN   (DOCTOR total)""", "worked example"),
            ASK("\"What is a weak entity?\" An entity that cannot be identified by its own attributes alone; it depends on an owner via an identifying relationship and has total participation in it. Its primary key in tables = owner's key + partial key."),
        ],
        [
            Q("A multivalued attribute such as 'phone numbers' is drawn as:", ["A single oval", "A double oval", "A dashed oval", "An underlined oval"], 1, "Double oval = multivalued. Dashed = derived. Underlined = key."),
            Q("Which is a weak entity?", ["STUDENT with roll_no", "DEPENDENT identified by employee_id + dependent_name", "COURSE with course_id", "BOOK with isbn"], 1, "DEPENDENT has no key of its own and is identified through EMPLOYEE."),
            Q("Each employee works in exactly one department; a department can have many employees. The relationship is:", ["M:N", "1:1", "1:N from DEPARTMENT to EMPLOYEE", "N:1 from DEPARTMENT to EMPLOYEE"], 2, "One department, many employees: 1:N from DEPARTMENT to EMPLOYEE."),
            Q("Splitting EMPLOYEE into ENGINEER and MANAGER is called:", ["Aggregation", "Specialization", "Normalization", "Denormalization"], 1, "Top-down splitting into sub-classes is specialization. Merging them back is generalization."),
            Q("Total participation means:", ["Every entity in the set must take part in the relationship", "Some entities may not take part", "The relationship is 1:1", "The entity is weak"], 0, "Total (drawn with a double line) = every entity participates."),
        ], star=True, kw="er diagram entity weak attribute cardinality participation specialization generalization aggregation"))

    # ------------------------------------------------------------------ 3
    T.append(topic("er-to-tables", GA, "Mapping ER to tables (the design recipe)",
        "Scenario questions ask 'design the tables for this'. Apply these rules mechanically and you get correct tables, keys and foreign keys without thinking twice.",
        [
            H("The seven rules"),
            OL("**Strong entity** becomes a table; its key becomes the primary key; simple and flattened composite attributes become columns.",
               "**Weak entity** becomes a table whose primary key = owner's primary key + partial key. The owner's key is also a foreign key (ON DELETE CASCADE is typical).",
               "**1:N relationship:** put a foreign key on the N side (the 'many' side) pointing to the 1 side. Relationship attributes go with it.",
               "**1:1 relationship:** put the foreign key on the side with total participation and make it UNIQUE. If both are total, consider merging into one table.",
               "**M:N relationship:** a new junction (associative) table with a foreign key to each side. Primary key is the pair (or a surrogate id). Relationship attributes live here.",
               "**Multivalued attribute:** a new table (owner key, value). Primary key is the pair.",
               "**Higher-degree (ternary) relationship:** one table with a foreign key to each participant plus its attributes."),
            TBL(["ER feature", "Table result"],
                ["Composite address", "street, city, pin as separate columns"],
                ["Derived age", "not stored (compute from dob in a query or view)"],
                ["Recursive 1:N manager", "manager_id column in the same table, FK to its own primary key"],
                ["M:N with attributes", "junction table holding those attributes (grade in ENROLLMENT)"]),
            H("Worked example: university"),
            SQL("""CREATE TABLE dept (
  dept_id   INTEGER PRIMARY KEY,
  name      TEXT NOT NULL UNIQUE
);
CREATE TABLE student (
  roll_no   INTEGER PRIMARY KEY,
  name      TEXT NOT NULL,
  dept_id   INTEGER NOT NULL REFERENCES dept(dept_id)   -- 1:N, FK on the many side
);
CREATE TABLE course (
  course_id INTEGER PRIMARY KEY,
  title     TEXT NOT NULL,
  credits   INTEGER CHECK (credits BETWEEN 1 AND 6)
);
CREATE TABLE enrollment (                                -- M:N becomes a junction table
  roll_no   INTEGER REFERENCES student(roll_no) ON DELETE CASCADE,
  course_id INTEGER REFERENCES course(course_id),
  grade     TEXT,
  PRIMARY KEY (roll_no, course_id)
);
CREATE TABLE student_phone (                             -- multivalued attribute
  roll_no   INTEGER REFERENCES student(roll_no) ON DELETE CASCADE,
  phone     TEXT,
  PRIMARY KEY (roll_no, phone)
);
INSERT INTO dept VALUES (1,'CSE');
INSERT INTO student VALUES (10,'Asha',1);
INSERT INTO course VALUES (100,'DBMS',4);
INSERT INTO enrollment VALUES (10,100,'A');
SELECT s.name, c.title, e.grade
FROM enrollment e JOIN student s ON s.roll_no = e.roll_no JOIN course c ON c.course_id = e.course_id;""", "runs on a throwaway copy of the sample DB", run=True),
            H("Weak entity example"),
            SQL("""CREATE TABLE emp (emp_id INTEGER PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE dependent (
  emp_id  INTEGER NOT NULL REFERENCES emp(emp_id) ON DELETE CASCADE,
  dep_name TEXT NOT NULL,          -- partial key
  relation TEXT,
  PRIMARY KEY (emp_id, dep_name)   -- owner key + partial key
);""", "weak entity", run=True),
            H("Mapping a hierarchy (specialization)"),
            TBL(["Option", "How", "Good when", "Cost"],
                ["A. Table per class", "One table for the super-class, one per subclass sharing the same PK (PK is also FK to the parent)", "Subclasses have many own attributes; queries often need only the parent", "Joins to see full object"],
                ["B. Table per subclass only", "Each subclass table holds ALL attributes, no parent table", "Hierarchy is total and disjoint", "Parent-wide queries need UNION; overlapping breaks"],
                ["C. Single table", "One wide table plus a type column; subclass-only columns are NULL", "Few subclass attributes, simple queries", "Many NULLs, weak constraints"],
                ["D. Single table with several flags", "Boolean type flags", "Overlapping subclasses", "Same drawbacks as C"]),
            ASK("\"How do you represent a many-to-many relationship?\" With a junction table holding the two foreign keys as a composite primary key plus relationship attributes. Name the table after the business fact (enrollment, order_item), not 'student_course_link'."),
        ],
        [
            Q("Where does the foreign key go in a 1:N relationship between DEPARTMENT (1) and EMPLOYEE (N)?", ["In DEPARTMENT", "In EMPLOYEE", "In a new junction table", "In both"], 1, "The foreign key sits on the many side and points to the one side."),
            Q("An M:N relationship ENROLLS with attribute grade becomes:", ["A grade column in STUDENT", "A grade column in COURSE", "A junction table with two FKs and grade", "Not representable"], 2, "Junction table holding both keys and the relationship's own attribute."),
            Q("A weak entity's primary key is:", ["Its partial key alone", "Owner's key plus partial key", "A new surrogate only", "Owner's key alone"], 1, "Owner key + partial key; the owner key is also an FK."),
            Q("A multivalued attribute 'skills' of EMPLOYEE is stored as:", ["A comma-separated text column", "A separate table (emp_id, skill)", "A derived column", "Nothing; it is ignored"], 1, "First normal form forbids repeating groups. Use a child table."),
            Q("Which mapping rule is right for a 1:1 relationship where one side has total participation?", ["FK + UNIQUE on the total side", "A junction table is mandatory", "FK on the partial side with no UNIQUE", "No FK needed"], 0, "Put the FK on the total-participation side and make it UNIQUE so only one row can point to each parent."),
        ], star=True, kw="er mapping junction weak entity design tables hierarchy"))

    # ------------------------------------------------------------------ 4
    T.append(topic("relational-keys", GB, "Relational model and every kind of key",
        "This is the topic they ask most directly: super key, candidate key, primary key, alternate key, foreign key, composite key, surrogate key. Learn the definitions as a ladder, then practise counting super keys.",
        [
            H("Terms"),
            TBL(["Term", "Meaning"],
                ["Relation", "A table: a set of tuples over attributes"],
                ["Tuple", "A row"],
                ["Attribute", "A column"],
                ["Domain", "The set of legal values of an attribute (type + constraints)"],
                ["Degree (arity)", "Number of attributes (columns)"],
                ["Cardinality", "Number of tuples (rows)"],
                ["Schema vs instance", "Schema = structure (changes rarely). Instance = the data at one moment."],
                ["Properties of a relation", "Rows are unique, row order and column order are irrelevant, every value is atomic, every column has a distinct name"]),
            H("The key ladder"),
            TBL(["Key", "Definition", "Example in STUDENT(roll_no, email, name, phone, dept_id)"],
                ["Super key", "Any set of attributes that uniquely identifies a row. May contain extras.", "{roll_no}, {roll_no, name}, {email, phone}, {roll_no, email, name}"],
                ["Candidate key", "A MINIMAL super key: remove any attribute and uniqueness is lost.", "{roll_no}, {email}"],
                ["Primary key", "The one candidate key chosen as the main identifier. Not NULL, unique.", "{roll_no}"],
                ["Alternate key", "Candidate keys that were not chosen as primary.", "{email}"],
                ["Composite key", "A key made of two or more attributes.", "{student_id, course_id} in ENROLLMENT"],
                ["Foreign key", "Attribute(s) whose values must appear as a key (usually the primary key) of another table (or the same table).", "dept_id references DEPT(dept_id)"],
                ["Unique key", "A UNIQUE constraint. May allow NULLs (details differ by DBMS).", "email"],
                ["Natural key", "Real-world identifier", "email, passport number, ISBN"],
                ["Surrogate key", "System-generated, meaningless identifier", "id SERIAL / AUTO_INCREMENT / UUID"],
                ["Secondary / non-key attribute", "Any attribute not part of a candidate key", "name, phone"]),
            NOTE("Ladder: every primary key is a candidate key, every candidate key is a super key. Not the other way round."),
            H("Prime and non-prime attributes"),
            P("An attribute is **prime** if it belongs to at least one candidate key, otherwise **non-prime**. Normal-form definitions depend on this split."),
            H("Counting super keys (very common MCQ)"),
            UL("A relation with n attributes and **one single-attribute candidate key** has **2^(n-1)** super keys (the key plus any subset of the other n-1).",
               "R(A,B,C,D), candidate key {A}: 2^3 = **8** super keys.",
               "R(A,B,C,D), candidate keys {A} and {B}: supersets of A (8) + supersets of B (8) - supersets of both A and B (4) = **12**.",
               "R(A,B,C,D), candidate key {A,B}: supersets of AB = 2^2 = **4**.",
               "R(A,B,C), candidate keys {A,B} and {B,C}: supersets of AB (2) + supersets of BC (2) - supersets of ABC (1) = **3**."),
            P("Method: super keys = union of all supersets of each candidate key. Use inclusion-exclusion."),
            H("Integrity constraints"),
            TBL(["Constraint", "Rule"],
                ["Domain", "A value must belong to its attribute's domain (type, range, CHECK)"],
                ["Entity integrity", "No part of a primary key may be NULL"],
                ["Key constraint", "No two rows share the same value of a candidate key"],
                ["Referential integrity", "A foreign key value must match an existing key value in the parent table, or be NULL"],
                ["Semantic (business) constraints", "Triggers, CHECK, assertions: e.g. salary must not exceed manager's salary"]),
            H("What happens on delete or update of a parent row"),
            TBL(["Action", "Effect on child rows"],
                ["NO ACTION / RESTRICT", "Operation on the parent is rejected if children exist (RESTRICT checks immediately; NO ACTION checks at end of statement and can be deferred in PostgreSQL)"],
                ["CASCADE", "Delete or update the children too"],
                ["SET NULL", "Child FK becomes NULL (column must allow NULL)"],
                ["SET DEFAULT", "Child FK becomes its default (PostgreSQL; MySQL InnoDB parses but rejects it)"]),
            TRAP("A foreign key may be NULL (unless declared NOT NULL) and it need not be UNIQUE. A foreign key may reference any UNIQUE or primary key column, not only the primary key."),
            H("Worked key-finding question"),
            TXT("""R(A, B, C, D) with candidate keys {A} and {B,C}.

Super keys containing A:        2^3 = 8
Super keys containing B and C:  2^2 = 4
Containing both (A, B, C):      2^1 = 2
Total = 8 + 4 - 2 = 10""", "counting"),
            ASK("\"Difference between primary key and unique key?\" Primary key: one per table, NOT NULL implied, identifies the row. Unique: many per table, NULLs allowed (PostgreSQL and MySQL allow multiple NULLs; SQL Server allows only one)."),
            ASK("\"Candidate key vs super key?\" Every candidate key is a super key, but a candidate key is minimal: no attribute can be dropped. Super keys can carry redundant attributes."),
        ],
        [
            Q("R(A,B,C,D) has the single candidate key {A}. How many super keys does R have?", ["4", "8", "15", "16"], 1, "A plus any subset of {B,C,D}: 2^3 = 8."),
            Q("R(A,B,C,D) has candidate keys {A} and {B}. How many super keys?", ["8", "10", "12", "16"], 2, "8 + 8 - 4 = 12."),
            Q("Which statement is false?", ["Every primary key is a candidate key", "Every candidate key is a super key", "A candidate key can contain a redundant attribute", "A table may have several candidate keys"], 2, "Candidate keys are minimal, so they never contain redundant attributes."),
            Q("A foreign key column:", ["Must be UNIQUE", "Cannot be NULL", "Can be NULL and need not be unique", "Must be the primary key of its own table"], 2, "FK values may repeat (many children per parent) and may be NULL unless declared otherwise."),
            Q("ON DELETE SET NULL requires that the FK column:", ["Is part of the primary key", "Is declared NOT NULL", "Allows NULL", "Has a default"], 2, "You cannot set a column to NULL if it forbids NULL. A PK column can never be NULL."),
            Q("An attribute that belongs to some candidate key is called:", ["Prime", "Non-prime", "Derived", "Surrogate"], 0, "Prime attributes appear in at least one candidate key."),
        ], star=True, kw="super key candidate key primary key foreign key alternate composite surrogate natural unique integrity referential"))

    # ------------------------------------------------------------------ 5
    T.append(topic("relational-algebra", GB, "Relational algebra and calculus",
        "Relational algebra is the theory behind SQL and behind the query optimizer. GATE-style questions and many interviews ask you to write or read an algebra expression, or to say what a query returns.",
        [
            H("Operators"),
            TBL(["Operator", "Symbol", "SQL equivalent", "Notes"],
                ["Selection", "σ condition (R)", "WHERE", "Filters rows"],
                ["Projection", "π a, b (R)", "SELECT DISTINCT a, b", "Picks columns; removes duplicates in pure algebra"],
                ["Rename", "ρ x (R)", "AS alias", ""],
                ["Union", "R ∪ S", "UNION", "Union-compatible: same number and types of columns"],
                ["Difference", "R − S", "EXCEPT / MINUS", ""],
                ["Intersection", "R ∩ S", "INTERSECT", "R ∩ S = R − (R − S)"],
                ["Cartesian product", "R × S", "CROSS JOIN", "|R| × |S| rows"],
                ["Theta join", "R ⋈θ S", "JOIN ... ON", "σθ (R × S)"],
                ["Equi join", "R ⋈ S on equality", "JOIN ... ON a = b", "Theta join with ="],
                ["Natural join", "R ⋈ S", "NATURAL JOIN", "Equi join on all common attribute names, keeps one copy"],
                ["Outer joins", "⟕ ⟖ ⟗", "LEFT/RIGHT/FULL JOIN", "Keep unmatched rows with NULLs"],
                ["Semi join", "R ⋉ S", "WHERE EXISTS / IN", "Rows of R that have a match in S, only R's columns"],
                ["Anti join", "R ▷ S", "WHERE NOT EXISTS", "Rows of R without a match"],
                ["Division", "R ÷ S", "double NOT EXISTS", "'for all' queries"],
                ["Aggregation", "γ group; f(a) (R)", "GROUP BY", "Extended algebra"]),
            H("Examples on the sample schema"),
            TXT("""π name (σ salary > 100000 (employee))
   -> SELECT name FROM employees WHERE salary > 100000;

π name, dept_name (employee ⋈ employee.dept_id = department.id department)
   -> SELECT e.name, d.name FROM employees e JOIN departments d ON e.dept_id = d.id;

π id (department) − π dept_id (employee)
   -> departments that have no employee (set difference)""", "algebra and its SQL"),
            SQL("""SELECT id FROM departments
EXCEPT
SELECT dept_id FROM employees;""", "departments with no employee", run=True),
            H("Division (for-all queries)"),
            P("R(student, course) ÷ S(course) gives the students who took EVERY course in S. SQL has no division operator; use double NOT EXISTS: there is no required course for which this student has no row."),
            SQL("""-- employees who work on EVERY project in dept 1  (projects 1 and 4)
SELECT e.id, e.name
FROM employees e
WHERE NOT EXISTS (
  SELECT 1 FROM projects p
  WHERE p.dept_id = 1
    AND NOT EXISTS (
      SELECT 1 FROM assignments a
      WHERE a.emp_id = e.id AND a.project_id = p.id));""", "division in SQL", run=True),
            H("Useful identities"),
            UL("Cascade of selections: σc1 (σc2 (R)) = σc1∧c2 (R)",
               "Push selection through join: σc (R ⋈ S) = σc (R) ⋈ S when c uses only attributes of R. The optimizer does this to shrink inputs early.",
               "Projection can be pushed down but must keep join attributes.",
               "Joins are commutative and associative: R ⋈ S = S ⋈ R. The optimizer picks the cheapest order.",
               "Size of R × S = |R| × |S| rows and (columns of R + columns of S) columns."),
            H("Result sizes (typical MCQ)"),
            TBL(["Expression", "Rows"],
                ["R ∪ S", "between max(|R|,|S|) and |R| + |S|"],
                ["R ∩ S", "between 0 and min(|R|,|S|)"],
                ["R − S", "between 0 and |R|"],
                ["R × S", "exactly |R| × |S|"],
                ["Natural join, no common attributes", "same as R × S"],
                ["Natural join of R with S where common attribute is a key of S and a FK in R", "exactly |R| when every FK matches"]),
            H("Relational calculus in two lines"),
            UL("**Tuple relational calculus (TRC):** { t | EMPLOYEE(t) ∧ t.salary > 100000 }. Variables range over tuples.",
               "**Domain relational calculus (DRC):** { <n, s> | ∃e (<e, n, s> ∈ EMPLOYEE ∧ s > 100000) }. Variables range over attribute values.",
               "Calculus is declarative, algebra is procedural. Both have the same power when queries are **safe** (finite results). SQL is based on TRC plus algebra features.")
            ,
            NOTE("Algebra works on **sets** (no duplicate rows). SQL works on **bags** (duplicates allowed unless DISTINCT)."),
        ],
        [
            Q("Which operator corresponds to the SQL WHERE clause?", ["π (projection)", "σ (selection)", "ρ (rename)", "÷ (division)"], 1, "Selection filters rows, projection chooses columns."),
            Q("R has 5 rows and S has 4 rows. How many rows in R × S?", ["9", "20", "5", "Cannot say"], 1, "Cartesian product multiplies: 5 × 4 = 20."),
            Q("Which SQL idiom implements relational division?", ["GROUP BY HAVING", "UNION ALL", "Double NOT EXISTS", "LEFT JOIN ... IS NULL only"], 2, "'There is no required item that the entity lacks' = NOT EXISTS (… NOT EXISTS …)."),
            Q("The natural join joins on:", ["All columns", "Columns with the same name in both tables", "The primary keys only", "The first column of each"], 1, "Natural join pairs equal values of all same-named columns and keeps one copy of each."),
            Q("R ∩ S can be written as:", ["R ∪ (R − S)", "R − (R − S)", "(R − S) − S", "R × S"], 1, "Remove from R everything that is not in S: R − (R − S)."),
        ], kw="relational algebra calculus selection projection join division union"))

    # ------------------------------------------------------------------ 6
    T.append(topic("functional-deps", GB, "Functional dependencies, closure and finding keys",
        "Everything in normalization rests on functional dependencies. Master attribute closure and you can find all candidate keys, test normal forms and compute a minimal cover quickly.",
        [
            H("Definition"),
            P("X → Y (X determines Y) holds in R if whenever two rows agree on X they must agree on Y. Roll number → name is a functional dependency; name → roll number is not (two students can share a name)."),
            TBL(["Kind", "Meaning", "Example"],
                ["Trivial", "Y ⊆ X", "AB → A"],
                ["Non-trivial", "Y ⊄ X", "A → B"],
                ["Completely non-trivial", "X ∩ Y = ∅", "A → B (not AB → BC)"],
                ["Full FD", "Y depends on all of X, not a proper subset", "{student, course} → grade"],
                ["Partial FD", "Y depends on a proper subset of a (composite) key", "{student, course} → student_name, since student → student_name"],
                ["Transitive FD", "X → Y and Y → Z with Y not a key, so X → Z indirectly", "emp_id → dept_id → dept_name"]),
            H("Armstrong's axioms (sound and complete)"),
            UL("**Reflexivity:** if Y ⊆ X then X → Y",
               "**Augmentation:** if X → Y then XZ → YZ",
               "**Transitivity:** if X → Y and Y → Z then X → Z"),
            P("Derived rules: **Union** (X → Y, X → Z gives X → YZ), **Decomposition** (X → YZ gives X → Y and X → Z), **Pseudo-transitivity** (X → Y, WY → Z gives WX → Z). Note: AB → C does NOT give A → C or B → C."),
            H("Attribute closure X+ (the main tool)"),
            OL("Start with result = X.",
               "Repeat: for every FD L → R in F, if L ⊆ result then add R to result.",
               "Stop when nothing new is added. That set is X+."),
            P("**Uses:** (1) X is a super key iff X+ is all attributes. (2) X → Y follows from F iff Y ⊆ X+. (3) Test equivalence of two FD sets."),
            TXT("""R(A,B,C,D,E)   F = { A → B,  BC → D,  D → E }

(AC)+ : start {A,C}
        A → B gives {A,B,C}
        BC → D gives {A,B,C,D}
        D → E gives {A,B,C,D,E}   = all attributes, so AC is a super key
A+  = {A,B}        C+ = {C}      neither is a key, so AC is minimal: candidate key""", "worked closure"),
            H("Finding all candidate keys quickly"),
            OL("Attributes that appear on **no right-hand side** must be in every key. Start from them.",
               "Attributes that appear **only on right-hand sides** are in no key.",
               "Compute the closure of the must-have set. If it is everything, that is the only key.",
               "Otherwise add one more attribute at a time (middle attributes) and test closures. Keep only minimal sets."),
            TXT("""R(A,B,C,D)  F = { A → B, B → C, C → D, D → A }
No attribute is forced. Each of A+, B+, C+, D+ = {A,B,C,D}.
Candidate keys: A, B, C, D   (four keys, all single attributes, all prime)""", "cyclic dependencies give many keys"),
            TXT("""R(A,B,C,D,E)  F = { AB → C, C → D, D → E, E → B }
A is on no RHS so A is in every key.  A+ = {A}.
Try AB: AB+ = {A,B,C,D,E}. Key.
Try AC: C → D → E → B so AC+ = all. Key.  AD: D → E → B, then AB → C: key.  AE: E → B, AB → C...: key.
Candidate keys: AB, AC, AD, AE.""", "several keys"),
            H("Equivalence and minimal (canonical) cover"),
            P("Two FD sets F and G are equivalent if every FD of F follows from G and vice versa. A **minimal cover** is a smallest equivalent set where (1) every right side is a single attribute, (2) no left-side attribute is extraneous, (3) no FD is redundant."),
            OL("Split right sides to single attributes.",
               "Remove extraneous left-side attributes: in AB → C, B is extraneous if C ∈ A+ computed using F.",
               "Remove redundant FDs: drop X → A if A ∈ X+ computed without that FD."),
            TXT("""F = { A → BC, B → C, A → B, AB → C }
Step 1: A → B, A → C, B → C, A → B, AB → C
Step 2: AB → C: A+ already has C (A → C), so B is extraneous -> A → C
Step 3: A → C is redundant (A → B → C).  Remove duplicates.
Minimal cover: { A → B, B → C }""", "worked minimal cover"),
            TRAP("A minimal cover is not unique, but all minimal covers have the same number of FDs only in simple cases. Do the three steps in order: splitting, then extraneous attributes, then redundant FDs."),
            ASK("\"Given R and FDs, find the candidate keys\" and \"what is the highest normal form\" are the two most frequent DBMS theory questions. Practise the closure method until it is automatic."),
        ],
        [
            Q("R(A,B,C,D), F = {A→B, B→C}. What is A+?", ["{A}", "{A,B}", "{A,B,C}", "{A,B,C,D}"], 2, "A → B gives B, B → C gives C. D is not reached."),
            Q("R(A,B,C,D), F = {A→B, B→C}. The candidate key(s) are:", ["{A}", "{A,D}", "{A,B,D}", "{A,C,D}"], 1, "A and D never appear on a RHS (D not at all, A not at all) so both must be in the key. AD+ = ABCD."),
            Q("Which does NOT follow from AB → C?", ["ABD → CD", "AB → AC", "A → C", "AB → ABC"], 2, "A → C is not implied; augmentation and union give the others."),
            Q("An FD X → Y is trivial when:", ["X is a key", "Y ⊆ X", "X ⊆ Y", "X and Y are disjoint"], 1, "If Y is part of X, it holds in every relation."),
            Q("R(A,B,C) with F = {A→B, B→C, C→A}. How many candidate keys?", ["1", "2", "3", "0"], 2, "A, B and C each determine the rest, so each is a candidate key."),
            Q("To test whether X is a super key you compute:", ["Closure of X and check it equals all attributes", "The complement of X", "Whether X is on a RHS", "Whether X is NOT NULL"], 0, "X is a super key iff X+ = all attributes."),
        ], star=True, kw="functional dependency closure armstrong candidate keys minimal cover canonical partial transitive"))

    return T
