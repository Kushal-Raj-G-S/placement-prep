"""Write-it bank, part 2: CREATE TABLE tasks graded by behaviour, and paper-only tasks (self-marked against a rubric).

DDL task: the student's statements run on an empty database (after `pre`, if given). Then every check runs on a fresh
copy with foreign keys ON:  run `setup` (must succeed), run `sql` (must succeed when ok=True, must fail when ok=False),
optionally run `after` (a SELECT) and compare its first cell with `expect`.
"""


def C(label, sql, ok=True, setup="", after=None, expect=None):
    return {"label": label, "sql": sql, "ok": ok, "setup": setup, "after": after, "expect": expect}


def D(id, tier, tag, title, task, ref, checks, pre="", mins=None):
    return {"id": id, "kind": "ddl", "db": "empty", "tier": tier, "tag": tag, "title": title, "task": task, "ref": ref.strip(),
            "checks": checks, "pre": pre.strip(), "mins": mins or {1: 6, 2: 10, 3: 15}[tier]}


def P(id, tier, tag, title, task, model, rubric, mins=None):
    return {"id": id, "kind": "paper", "db": "none", "tier": tier, "tag": tag, "title": title, "task": task, "model": model.strip("\n"),
            "rubric": rubric, "mins": mins or {1: 6, 2: 10, 3: 15}[tier]}


DDL = [
    D("d01", 2, "M:N", "Students and courses",
      "Create three tables.\n\nstudent(student_id INTEGER primary key, name text required)\ncourse(course_id INTEGER primary key, title text required, credits integer that must be between 1 and 6)\nenrollment(student_id, course_id, grade text) where a student can enrol in a course only once, an enrollment disappears when its student is deleted, and a course that still has enrollments cannot be deleted.",
      """CREATE TABLE student (student_id INTEGER PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE course (course_id INTEGER PRIMARY KEY, title TEXT NOT NULL, credits INTEGER CHECK (credits BETWEEN 1 AND 6));
CREATE TABLE enrollment (
  student_id INTEGER NOT NULL REFERENCES student(student_id) ON DELETE CASCADE,
  course_id  INTEGER NOT NULL REFERENCES course(course_id) ON DELETE RESTRICT,
  grade TEXT,
  PRIMARY KEY (student_id, course_id));""",
      [C("student has student_id, name", "SELECT student_id, name FROM student LIMIT 0"),
       C("course has course_id, title, credits", "SELECT course_id, title, credits FROM course LIMIT 0"),
       C("enrollment has student_id, course_id, grade", "SELECT student_id, course_id, grade FROM enrollment LIMIT 0"),
       C("valid enrollment is accepted", "INSERT INTO enrollment VALUES (1, 10, 'A')", True, "INSERT INTO student VALUES (1,'Asha'); INSERT INTO course VALUES (10,'DBMS',4);"),
       C("second enrollment in the same course is rejected", "INSERT INTO enrollment VALUES (1, 10, 'B')", False, "INSERT INTO student VALUES (1,'Asha'); INSERT INTO course VALUES (10,'DBMS',4); INSERT INTO enrollment VALUES (1,10,'A');"),
       C("credits of 9 are rejected", "INSERT INTO course VALUES (11, 'Big', 9)", False),
       C("name is required", "INSERT INTO student VALUES (2, NULL)", False),
       C("enrollment for a missing student is rejected", "INSERT INTO enrollment VALUES (99, 10, 'A')", False, "INSERT INTO course VALUES (10,'DBMS',4);"),
       C("deleting a student removes their enrollments", "DELETE FROM student WHERE student_id = 1", True, "INSERT INTO student VALUES (1,'Asha'); INSERT INTO course VALUES (10,'DBMS',4); INSERT INTO enrollment VALUES (1,10,'A');", "SELECT COUNT(*) FROM enrollment", "0"),
       C("a course with enrollments cannot be deleted", "DELETE FROM course WHERE course_id = 10", False, "INSERT INTO student VALUES (1,'Asha'); INSERT INTO course VALUES (10,'DBMS',4); INSERT INTO enrollment VALUES (1,10,'A');")]),
    D("d02", 1, "constraints", "Employee rules",
      "Create table employee with: emp_id (integer primary key), email (text, required, no two employees may share an email), salary (integer, must be greater than 0), status (text, defaults to 'active'), hired_on (text, required).",
      "CREATE TABLE employee (emp_id INTEGER PRIMARY KEY, email TEXT NOT NULL UNIQUE, salary INTEGER CHECK (salary > 0), status TEXT DEFAULT 'active', hired_on TEXT NOT NULL);",
      [C("columns exist", "SELECT emp_id, email, salary, status, hired_on FROM employee LIMIT 0"),
       C("valid row accepted", "INSERT INTO employee (emp_id, email, salary, hired_on) VALUES (1,'a@x.com',50000,'2026-01-01')"),
       C("status defaults to active", "INSERT INTO employee (emp_id, email, salary, hired_on) VALUES (1,'a@x.com',50000,'2026-01-01')", True, "", "SELECT status FROM employee WHERE emp_id = 1", "active"),
       C("duplicate email rejected", "INSERT INTO employee (emp_id, email, salary, hired_on) VALUES (2,'a@x.com',60000,'2026-01-02')", False, "INSERT INTO employee (emp_id, email, salary, hired_on) VALUES (1,'a@x.com',50000,'2026-01-01');"),
       C("zero salary rejected", "INSERT INTO employee (emp_id, email, salary, hired_on) VALUES (3,'b@x.com',0,'2026-01-01')", False),
       C("missing email rejected", "INSERT INTO employee (emp_id, email, salary, hired_on) VALUES (4,NULL,100,'2026-01-01')", False),
       C("missing hired_on rejected", "INSERT INTO employee (emp_id, email, salary) VALUES (5,'c@x.com',100)", False)]),
    D("d03", 2, "1:N", "Library loans",
      "Create member(member_id integer pk, name required), book(book_id integer pk, isbn required and unique, title required) and loan(loan_id integer pk, member_id, book_id, loaned_on required, due_on required, returned_on optional). A loan must reference an existing member and book, and due_on must not be earlier than loaned_on. Dates are text in YYYY-MM-DD form.",
      """CREATE TABLE member (member_id INTEGER PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE book (book_id INTEGER PRIMARY KEY, isbn TEXT NOT NULL UNIQUE, title TEXT NOT NULL);
CREATE TABLE loan (loan_id INTEGER PRIMARY KEY, member_id INTEGER NOT NULL REFERENCES member(member_id), book_id INTEGER NOT NULL REFERENCES book(book_id),
  loaned_on TEXT NOT NULL, due_on TEXT NOT NULL, returned_on TEXT, CHECK (due_on >= loaned_on));""",
      [C("member columns", "SELECT member_id, name FROM member LIMIT 0"), C("book columns", "SELECT book_id, isbn, title FROM book LIMIT 0"),
       C("loan columns", "SELECT loan_id, member_id, book_id, loaned_on, due_on, returned_on FROM loan LIMIT 0"),
       C("valid loan accepted", "INSERT INTO loan VALUES (1,1,1,'2026-01-01','2026-01-15',NULL)", True, "INSERT INTO member VALUES (1,'A'); INSERT INTO book VALUES (1,'111','T');"),
       C("due date before loan date rejected", "INSERT INTO loan VALUES (1,1,1,'2026-01-10','2026-01-01',NULL)", False, "INSERT INTO member VALUES (1,'A'); INSERT INTO book VALUES (1,'111','T');"),
       C("unknown member rejected", "INSERT INTO loan VALUES (1,9,1,'2026-01-01','2026-01-15',NULL)", False, "INSERT INTO book VALUES (1,'111','T');"),
       C("duplicate isbn rejected", "INSERT INTO book VALUES (2,'111','T2')", False, "INSERT INTO book VALUES (1,'111','T');")]),
    D("d04", 2, "self-reference", "Org chart",
      "Create table staff(staff_id integer pk, name required, manager_id) where manager_id refers to another staff member (or is NULL for the top person). If a manager is deleted, their reports must stay and their manager_id becomes NULL.",
      "CREATE TABLE staff (staff_id INTEGER PRIMARY KEY, name TEXT NOT NULL, manager_id INTEGER REFERENCES staff(staff_id) ON DELETE SET NULL);",
      [C("columns", "SELECT staff_id, name, manager_id FROM staff LIMIT 0"),
       C("top person with NULL manager accepted", "INSERT INTO staff VALUES (1,'CEO',NULL)"),
       C("unknown manager rejected", "INSERT INTO staff VALUES (2,'Dev',99)", False),
       C("deleting a manager nulls their reports' manager_id", "DELETE FROM staff WHERE staff_id = 1", True, "INSERT INTO staff VALUES (1,'CEO',NULL); INSERT INTO staff VALUES (2,'Dev',1);", "SELECT COUNT(*) FROM staff WHERE staff_id = 2 AND manager_id IS NULL", "1"),
       C("name required", "INSERT INTO staff VALUES (3, NULL, NULL)", False)]),
    D("d05", 2, "composite key", "Order lines",
      "Create orders(order_id integer pk, customer text required) and order_line(order_id, line_no, product text required, qty integer greater than 0, unit_price integer not negative). A line is identified by (order_id, line_no). Deleting an order deletes its lines.",
      """CREATE TABLE orders (order_id INTEGER PRIMARY KEY, customer TEXT NOT NULL);
CREATE TABLE order_line (order_id INTEGER NOT NULL REFERENCES orders(order_id) ON DELETE CASCADE, line_no INTEGER NOT NULL, product TEXT NOT NULL,
  qty INTEGER CHECK (qty > 0), unit_price INTEGER CHECK (unit_price >= 0), PRIMARY KEY (order_id, line_no));""",
      [C("orders columns", "SELECT order_id, customer FROM orders LIMIT 0"), C("order_line columns", "SELECT order_id, line_no, product, qty, unit_price FROM order_line LIMIT 0"),
       C("valid line accepted", "INSERT INTO order_line VALUES (1,1,'Pen',2,10)", True, "INSERT INTO orders VALUES (1,'A');"),
       C("same line number twice in one order rejected", "INSERT INTO order_line VALUES (1,1,'Ink',1,5)", False, "INSERT INTO orders VALUES (1,'A'); INSERT INTO order_line VALUES (1,1,'Pen',2,10);"),
       C("same line number in another order accepted", "INSERT INTO order_line VALUES (2,1,'Ink',1,5)", True, "INSERT INTO orders VALUES (1,'A'),(2,'B'); INSERT INTO order_line VALUES (1,1,'Pen',2,10);"),
       C("qty 0 rejected", "INSERT INTO order_line VALUES (1,2,'Pen',0,10)", False, "INSERT INTO orders VALUES (1,'A');"),
       C("negative price rejected", "INSERT INTO order_line VALUES (1,2,'Pen',1,-5)", False, "INSERT INTO orders VALUES (1,'A');"),
       C("deleting an order deletes its lines", "DELETE FROM orders WHERE order_id = 1", True, "INSERT INTO orders VALUES (1,'A'); INSERT INTO order_line VALUES (1,1,'Pen',2,10);", "SELECT COUNT(*) FROM order_line", "0")]),
    D("d06", 2, "weak entity", "Dependents of employees",
      "Model a weak entity: emp(emp_id integer pk, name required) and dependent(emp_id, dep_name, relation). A dependent is identified by the employee plus the dependent's name, must belong to an existing employee, and is deleted with the employee.",
      """CREATE TABLE emp (emp_id INTEGER PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE dependent (emp_id INTEGER NOT NULL REFERENCES emp(emp_id) ON DELETE CASCADE, dep_name TEXT NOT NULL, relation TEXT, PRIMARY KEY (emp_id, dep_name));""",
      [C("emp columns", "SELECT emp_id, name FROM emp LIMIT 0"), C("dependent columns", "SELECT emp_id, dep_name, relation FROM dependent LIMIT 0"),
       C("dependent accepted", "INSERT INTO dependent VALUES (1,'Tina','daughter')", True, "INSERT INTO emp VALUES (1,'A');"),
       C("same name twice for one employee rejected", "INSERT INTO dependent VALUES (1,'Tina','niece')", False, "INSERT INTO emp VALUES (1,'A'); INSERT INTO dependent VALUES (1,'Tina','daughter');"),
       C("same name for another employee accepted", "INSERT INTO dependent VALUES (2,'Tina','daughter')", True, "INSERT INTO emp VALUES (1,'A'),(2,'B'); INSERT INTO dependent VALUES (1,'Tina','daughter');"),
       C("dependent without employee rejected", "INSERT INTO dependent VALUES (9,'X','son')", False),
       C("employee deletion cascades", "DELETE FROM emp WHERE emp_id = 1", True, "INSERT INTO emp VALUES (1,'A'); INSERT INTO dependent VALUES (1,'Tina','daughter');", "SELECT COUNT(*) FROM dependent", "0")]),
    D("d07", 2, "set null", "Products and categories",
      "Create category(category_id integer pk, name required and unique) and product(product_id integer pk, name required, category_id optional, price must be greater than 0). If a category is deleted, its products stay with category_id set to NULL.",
      """CREATE TABLE category (category_id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE);
CREATE TABLE product (product_id INTEGER PRIMARY KEY, name TEXT NOT NULL, category_id INTEGER REFERENCES category(category_id) ON DELETE SET NULL, price INTEGER CHECK (price > 0));""",
      [C("category columns", "SELECT category_id, name FROM category LIMIT 0"), C("product columns", "SELECT product_id, name, category_id, price FROM product LIMIT 0"),
       C("product without a category accepted", "INSERT INTO product VALUES (1,'Pen',NULL,10)"),
       C("duplicate category name rejected", "INSERT INTO category VALUES (2,'Toys')", False, "INSERT INTO category VALUES (1,'Toys');"),
       C("price 0 rejected", "INSERT INTO product VALUES (1,'Pen',NULL,0)", False),
       C("unknown category rejected", "INSERT INTO product VALUES (1,'Pen',99,10)", False),
       C("deleting a category keeps products with NULL category", "DELETE FROM category WHERE category_id = 1", True, "INSERT INTO category VALUES (1,'Toys'); INSERT INTO product VALUES (1,'Car',1,100);", "SELECT COUNT(*) FROM product WHERE category_id IS NULL", "1")]),
    D("d08", 2, "unique pair", "No double booking",
      "Create room(room_no integer pk) and booking(booking_id integer pk, room_no, night text, guest text required). A room can be booked for a given night only once. Bookings must refer to an existing room.",
      """CREATE TABLE room (room_no INTEGER PRIMARY KEY);
CREATE TABLE booking (booking_id INTEGER PRIMARY KEY, room_no INTEGER NOT NULL REFERENCES room(room_no), night TEXT NOT NULL, guest TEXT NOT NULL, UNIQUE (room_no, night));""",
      [C("room columns", "SELECT room_no FROM room LIMIT 0"), C("booking columns", "SELECT booking_id, room_no, night, guest FROM booking LIMIT 0"),
       C("booking accepted", "INSERT INTO booking VALUES (1,101,'2026-05-01','Asha')", True, "INSERT INTO room VALUES (101);"),
       C("same room same night rejected", "INSERT INTO booking VALUES (2,101,'2026-05-01','Rohan')", False, "INSERT INTO room VALUES (101); INSERT INTO booking VALUES (1,101,'2026-05-01','Asha');"),
       C("same room different night accepted", "INSERT INTO booking VALUES (2,101,'2026-05-02','Rohan')", True, "INSERT INTO room VALUES (101); INSERT INTO booking VALUES (1,101,'2026-05-01','Asha');"),
       C("unknown room rejected", "INSERT INTO booking VALUES (3,999,'2026-05-01','X')", False),
       C("guest required", "INSERT INTO booking VALUES (4,101,'2026-05-03',NULL)", False, "INSERT INTO room VALUES (101);")]),
    D("d09", 3, "business rules", "Bank accounts",
      "Create account(account_no integer pk, owner required, balance integer default 0 and never negative) and transfer_log(log_id integer pk, from_acct, to_acct, amount). Both account columns reference account, amount must be greater than 0, and money cannot be transferred from an account to itself.",
      """CREATE TABLE account (account_no INTEGER PRIMARY KEY, owner TEXT NOT NULL, balance INTEGER NOT NULL DEFAULT 0 CHECK (balance >= 0));
CREATE TABLE transfer_log (log_id INTEGER PRIMARY KEY, from_acct INTEGER NOT NULL REFERENCES account(account_no), to_acct INTEGER NOT NULL REFERENCES account(account_no),
  amount INTEGER NOT NULL CHECK (amount > 0), CHECK (from_acct <> to_acct));""",
      [C("account columns", "SELECT account_no, owner, balance FROM account LIMIT 0"), C("transfer_log columns", "SELECT log_id, from_acct, to_acct, amount FROM transfer_log LIMIT 0"),
       C("balance defaults to 0", "INSERT INTO account (account_no, owner) VALUES (1,'A')", True, "", "SELECT balance FROM account WHERE account_no = 1", "0"),
       C("negative balance rejected", "INSERT INTO account VALUES (2,'B',-5)", False),
       C("valid transfer accepted", "INSERT INTO transfer_log VALUES (1,1,2,50)", True, "INSERT INTO account VALUES (1,'A',100),(2,'B',0);"),
       C("transfer to the same account rejected", "INSERT INTO transfer_log VALUES (1,1,1,50)", False, "INSERT INTO account VALUES (1,'A',100);"),
       C("zero amount rejected", "INSERT INTO transfer_log VALUES (1,1,2,0)", False, "INSERT INTO account VALUES (1,'A',100),(2,'B',0);"),
       C("unknown account rejected", "INSERT INTO transfer_log VALUES (1,1,99,10)", False, "INSERT INTO account VALUES (1,'A',100);")]),
    D("d10", 2, "1:1", "People and passports",
      "Create person(person_id integer pk, name required) and passport(passport_no text pk, person_id, issued_on text). Each passport belongs to exactly one existing person, and each person can have at most one passport.",
      """CREATE TABLE person (person_id INTEGER PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE passport (passport_no TEXT PRIMARY KEY, person_id INTEGER NOT NULL UNIQUE REFERENCES person(person_id), issued_on TEXT);""",
      [C("person columns", "SELECT person_id, name FROM person LIMIT 0"), C("passport columns", "SELECT passport_no, person_id, issued_on FROM passport LIMIT 0"),
       C("passport accepted", "INSERT INTO passport VALUES ('P1',1,'2026-01-01')", True, "INSERT INTO person VALUES (1,'A');"),
       C("second passport for the same person rejected", "INSERT INTO passport VALUES ('P2',1,'2026-02-01')", False, "INSERT INTO person VALUES (1,'A'); INSERT INTO passport VALUES ('P1',1,'2026-01-01');"),
       C("passport without a person rejected", "INSERT INTO passport VALUES ('P3',NULL,'2026-01-01')", False),
       C("passport for unknown person rejected", "INSERT INTO passport VALUES ('P4',99,'2026-01-01')", False)]),
    D("d11", 2, "composite key", "One vote per poll",
      "Create poll(poll_id integer pk, question required) and vote(poll_id, voter text, rating integer from 1 to 5). A voter can vote only once in each poll. Votes are deleted if the poll is deleted.",
      """CREATE TABLE poll (poll_id INTEGER PRIMARY KEY, question TEXT NOT NULL);
CREATE TABLE vote (poll_id INTEGER NOT NULL REFERENCES poll(poll_id) ON DELETE CASCADE, voter TEXT NOT NULL, rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5), PRIMARY KEY (poll_id, voter));""",
      [C("poll columns", "SELECT poll_id, question FROM poll LIMIT 0"), C("vote columns", "SELECT poll_id, voter, rating FROM vote LIMIT 0"),
       C("vote accepted", "INSERT INTO vote VALUES (1,'asha',4)", True, "INSERT INTO poll VALUES (1,'Q');"),
       C("same voter twice in a poll rejected", "INSERT INTO vote VALUES (1,'asha',5)", False, "INSERT INTO poll VALUES (1,'Q'); INSERT INTO vote VALUES (1,'asha',4);"),
       C("same voter in another poll accepted", "INSERT INTO vote VALUES (2,'asha',5)", True, "INSERT INTO poll VALUES (1,'Q'),(2,'R'); INSERT INTO vote VALUES (1,'asha',4);"),
       C("rating 6 rejected", "INSERT INTO vote VALUES (1,'rohan',6)", False, "INSERT INTO poll VALUES (1,'Q');"),
       C("deleting a poll deletes votes", "DELETE FROM poll WHERE poll_id = 1", True, "INSERT INTO poll VALUES (1,'Q'); INSERT INTO vote VALUES (1,'asha',4);", "SELECT COUNT(*) FROM vote", "0")]),
    D("d12", 1, "defaults", "Audit log",
      "Create audit_log(log_id integer pk, action text required, actor text, created_at text that is filled with the current timestamp automatically when not supplied).",
      "CREATE TABLE audit_log (log_id INTEGER PRIMARY KEY, action TEXT NOT NULL, actor TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP);",
      [C("columns", "SELECT log_id, action, actor, created_at FROM audit_log LIMIT 0"),
       C("created_at filled automatically", "INSERT INTO audit_log (action, actor) VALUES ('login','asha')", True, "", "SELECT created_at IS NOT NULL FROM audit_log", "1"),
       C("action required", "INSERT INTO audit_log (actor) VALUES ('asha')", False)]),
    D("d13", 2, "restrict", "Departments and employees",
      "Create department(dept_id integer pk, name required and unique) and employee(emp_id integer pk, name required, dept_id required). Every employee must belong to an existing department, and a department that still has employees cannot be deleted.",
      """CREATE TABLE department (dept_id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE);
CREATE TABLE employee (emp_id INTEGER PRIMARY KEY, name TEXT NOT NULL, dept_id INTEGER NOT NULL REFERENCES department(dept_id) ON DELETE RESTRICT);""",
      [C("department columns", "SELECT dept_id, name FROM department LIMIT 0"), C("employee columns", "SELECT emp_id, name, dept_id FROM employee LIMIT 0"),
       C("employee accepted", "INSERT INTO employee VALUES (1,'A',1)", True, "INSERT INTO department VALUES (1,'Data');"),
       C("employee without department rejected", "INSERT INTO employee VALUES (1,'A',NULL)", False),
       C("employee in unknown department rejected", "INSERT INTO employee VALUES (1,'A',9)", False),
       C("department with employees cannot be deleted", "DELETE FROM department WHERE dept_id = 1", False, "INSERT INTO department VALUES (1,'Data'); INSERT INTO employee VALUES (1,'A',1);"),
       C("empty department can be deleted", "DELETE FROM department WHERE dept_id = 2", True, "INSERT INTO department VALUES (1,'Data'),(2,'Ops'); INSERT INTO employee VALUES (1,'A',1);"),
       C("duplicate department name rejected", "INSERT INTO department VALUES (2,'Data')", False, "INSERT INTO department VALUES (1,'Data');")]),
    D("d14", 3, "scheduling", "Doctor appointments",
      "Create doctor(doctor_id integer pk, name required), patient(patient_id integer pk, name required) and appointment(appt_id integer pk, doctor_id, patient_id, slot text, status text default 'booked' limited to 'booked', 'done' or 'cancelled'). A doctor cannot have two appointments in the same slot. All references must exist.",
      """CREATE TABLE doctor (doctor_id INTEGER PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE patient (patient_id INTEGER PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE appointment (appt_id INTEGER PRIMARY KEY, doctor_id INTEGER NOT NULL REFERENCES doctor(doctor_id), patient_id INTEGER NOT NULL REFERENCES patient(patient_id),
  slot TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'booked' CHECK (status IN ('booked','done','cancelled')), UNIQUE (doctor_id, slot));""",
      [C("doctor columns", "SELECT doctor_id, name FROM doctor LIMIT 0"), C("patient columns", "SELECT patient_id, name FROM patient LIMIT 0"),
       C("appointment columns", "SELECT appt_id, doctor_id, patient_id, slot, status FROM appointment LIMIT 0"),
       C("status defaults to booked", "INSERT INTO appointment (appt_id, doctor_id, patient_id, slot) VALUES (1,1,1,'2026-05-01 10:00')", True, "INSERT INTO doctor VALUES (1,'D'); INSERT INTO patient VALUES (1,'P');", "SELECT status FROM appointment", "booked"),
       C("same doctor same slot rejected", "INSERT INTO appointment (appt_id, doctor_id, patient_id, slot) VALUES (2,1,2,'2026-05-01 10:00')", False, "INSERT INTO doctor VALUES (1,'D'); INSERT INTO patient VALUES (1,'P'),(2,'Q'); INSERT INTO appointment (appt_id, doctor_id, patient_id, slot) VALUES (1,1,1,'2026-05-01 10:00');"),
       C("different doctor same slot accepted", "INSERT INTO appointment (appt_id, doctor_id, patient_id, slot) VALUES (2,2,2,'2026-05-01 10:00')", True, "INSERT INTO doctor VALUES (1,'D'),(2,'E'); INSERT INTO patient VALUES (1,'P'),(2,'Q'); INSERT INTO appointment (appt_id, doctor_id, patient_id, slot) VALUES (1,1,1,'2026-05-01 10:00');"),
       C("invalid status rejected", "INSERT INTO appointment (appt_id, doctor_id, patient_id, slot, status) VALUES (1,1,1,'x','lost')", False, "INSERT INTO doctor VALUES (1,'D'); INSERT INTO patient VALUES (1,'P');"),
       C("unknown patient rejected", "INSERT INTO appointment (appt_id, doctor_id, patient_id, slot) VALUES (1,1,9,'x')", False, "INSERT INTO doctor VALUES (1,'D');")]),
    D("d15", 2, "ALTER", "Evolve a table",
      "The table gadget(id INTEGER PRIMARY KEY, name TEXT) already exists with one row. Write statements so that: (1) a new column price (integer, required, default 0) exists and the existing row gets price 0, (2) the column name is renamed to title, and (3) an index called idx_gadget_title exists on title.",
      "ALTER TABLE gadget ADD COLUMN price INTEGER NOT NULL DEFAULT 0; ALTER TABLE gadget RENAME COLUMN name TO title; CREATE INDEX idx_gadget_title ON gadget (title);",
      [C("price column exists with default 0 on the old row", "SELECT price FROM gadget WHERE id = 1", True, "", "SELECT price FROM gadget WHERE id = 1", "0"),
       C("column renamed to title", "SELECT title FROM gadget WHERE id = 1", True, "", "SELECT title FROM gadget WHERE id = 1", "lamp"),
       C("old column name is gone", "SELECT name FROM gadget", False),
       C("new rows get the default price", "INSERT INTO gadget (id, title) VALUES (2, 'fan')", True, "", "SELECT price FROM gadget WHERE id = 2", "0"),
       C("index idx_gadget_title exists", "SELECT name FROM sqlite_master WHERE type = 'index' AND name = 'idx_gadget_title'", True, "", "SELECT COUNT(*) FROM sqlite_master WHERE type = 'index' AND name = 'idx_gadget_title'", "1")],
      pre="CREATE TABLE gadget (id INTEGER PRIMARY KEY, name TEXT); INSERT INTO gadget VALUES (1, 'lamp');"),
]

PAPER = [
    P("p01", 3, "normalization", "Decompose to 3NF / BCNF",
      "Relation ENROLL(StudentID, CourseID, InstructorID, InstructorName, Grade) with F = { StudentID, CourseID → Grade ; CourseID → InstructorID ; InstructorID → InstructorName }. Find the candidate key, name the highest normal form, and decompose into relations in 3NF/BCNF.",
      """Candidate key: {StudentID, CourseID}. StudentID and CourseID appear on no right-hand side, so both are in every key; their closure is every attribute.
Prime: StudentID, CourseID. Non-prime: InstructorID, InstructorName, Grade.
CourseID → InstructorID is a partial dependency (part of the key determines a non-prime attribute): violates 2NF. Highest normal form: 1NF.
InstructorID → InstructorName is a transitive dependency.

Decomposition (3NF and BCNF, lossless and dependency preserving):
  ENROLLMENT(StudentID, CourseID, Grade)         key (StudentID, CourseID)
  COURSE(CourseID, InstructorID)                 key CourseID
  INSTRUCTOR(InstructorID, InstructorName)       key InstructorID""",
      ["Finds the key {StudentID, CourseID} with a reason (closure or 'on no RHS')", "Names the partial dependency CourseID → InstructorID and concludes 1NF", "Notes the transitive dependency InstructorID → InstructorName", "Produces the three relations with keys", "States that the decomposition is lossless / dependency preserving"]),
    P("p02", 3, "normalization", "Keys and normal form by closure",
      "R(A, B, C, D, E) with F = { AB → C, C → D, D → E, E → B }. Find every candidate key, list the prime attributes and give the highest normal form with the reason.",
      """A is on no right-hand side, so A is in every key.
AB+ = ABCDE (AB→C, C→D, D→E). Key.
AC+ = ACDEB (C→D, D→E, E→B). Key.   AD+ = ADEBC. Key.   AE+ = AEBCD. Key.
Candidate keys: AB, AC, AD, AE.  Prime attributes: A, B, C, D, E (all of them).
3NF: every right-hand side attribute is prime, so yes.
BCNF: C → D has C as determinant but C+ = {C,D,E,B} does not contain A, so C is not a super key: BCNF fails.
Highest normal form: 3NF (not BCNF).""",
      ["Argues A must be in every key", "Lists AB, AC, AD, AE", "States all attributes are prime", "Concludes 3NF because every RHS attribute is prime", "Shows a BCNF violation such as C → D with C not a super key"]),
    P("p03", 2, "ER to tables", "Hospital design on paper",
      "A hospital has doctors, patients and departments. Each doctor belongs to one department. A patient can see many doctors and a doctor many patients; each visit has a date and a diagnosis. Give the entities, relationships with cardinality, and the resulting tables with primary and foreign keys.",
      """Entities: DEPARTMENT(dept_id, name), DOCTOR(doctor_id, name, specialty), PATIENT(patient_id, name, dob).
Relationships: DEPARTMENT 1:N DOCTOR (works_in, DOCTOR total participation). DOCTOR M:N PATIENT through VISIT(visit_date, diagnosis).

Tables:
  department(dept_id PK, name UNIQUE NOT NULL)
  doctor(doctor_id PK, name NOT NULL, specialty, dept_id FK → department NOT NULL)
  patient(patient_id PK, name NOT NULL, dob)
  visit(visit_id PK, doctor_id FK → doctor, patient_id FK → patient, visit_date NOT NULL, diagnosis,
        UNIQUE (doctor_id, patient_id, visit_date))
Index the foreign keys.""",
      ["Identifies the three entities with keys", "Gives DEPARTMENT 1:N DOCTOR and puts dept_id in doctor", "Makes visit a junction table for the M:N with its own attributes", "Shows primary and foreign keys for each table", "Mentions NOT NULL / UNIQUE or indexing"]),
    P("p04", 2, "trigger", "PostgreSQL audit trigger",
      "Table employees(id, name, salary) exists, plus salary_audit(audit_id, emp_id, old_salary, new_salary, changed_at). Write the PostgreSQL trigger function and trigger that records every change of salary.",
      """CREATE OR REPLACE FUNCTION fn_salary_audit() RETURNS trigger
LANGUAGE plpgsql AS $$
BEGIN
  IF NEW.salary IS DISTINCT FROM OLD.salary THEN
    INSERT INTO salary_audit (emp_id, old_salary, new_salary, changed_at)
    VALUES (OLD.id, OLD.salary, NEW.salary, now());
  END IF;
  RETURN NEW;
END;
$$;

CREATE TRIGGER trg_salary_audit
AFTER UPDATE OF salary ON employees
FOR EACH ROW
EXECUTE FUNCTION fn_salary_audit();""",
      ["Function declared RETURNS trigger in plpgsql", "Uses OLD and NEW and only logs when the salary really changed", "Inserts the audit row with the old and new values and a timestamp", "Returns NEW (or NULL for an AFTER trigger)", "CREATE TRIGGER with AFTER UPDATE ... FOR EACH ROW EXECUTE FUNCTION"]),
    P("p05", 2, "trigger", "MySQL validation trigger",
      "In MySQL, products(product_id, stock) must never get a negative stock through UPDATE. Write a trigger that rejects such updates with a clear message.",
      """DELIMITER $$
CREATE TRIGGER trg_product_stock_check
BEFORE UPDATE ON products
FOR EACH ROW
BEGIN
  IF NEW.stock < 0 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'stock cannot be negative';
  END IF;
END$$
DELIMITER ;
-- A CHECK (stock >= 0) constraint (MySQL 8.0.16+) would be simpler and is preferred.""",
      ["BEFORE UPDATE trigger FOR EACH ROW", "Tests NEW.stock < 0", "Raises the error with SIGNAL SQLSTATE '45000' and a message", "Uses DELIMITER (or notes it) around the body", "Mentions that a CHECK constraint is the better tool"]),
    P("p06", 2, "function", "PostgreSQL function",
      "Write a PostgreSQL function annual_bonus(salary NUMERIC, years INT) returning 15% of salary for 5 or more years, 10% for 2 to 4 years, 5% otherwise, rounded to 2 decimals. Show a query that uses it.",
      """CREATE OR REPLACE FUNCTION annual_bonus(p_salary NUMERIC, p_years INT)
RETURNS NUMERIC
LANGUAGE plpgsql IMMUTABLE AS $$
BEGIN
  RETURN ROUND(p_salary * CASE WHEN p_years >= 5 THEN 0.15
                               WHEN p_years >= 2 THEN 0.10
                               ELSE 0.05 END, 2);
END;
$$;

SELECT name, annual_bonus(salary, 3) FROM employees;""",
      ["CREATE FUNCTION with parameters and RETURNS NUMERIC", "Correct three-way logic (CASE or IF/ELSIF)", "ROUND(..., 2)", "LANGUAGE plpgsql with BEGIN ... RETURN ... END and $$ quoting", "A SELECT calling the function"]),
    P("p07", 3, "procedure", "Money transfer procedure",
      "Write a PostgreSQL procedure transfer(from_acct, to_acct, amount) on account(account_no, balance) that moves money atomically, rejecting non-positive amounts and missing accounts. Show how to call it.",
      """CREATE OR REPLACE PROCEDURE transfer(p_from BIGINT, p_to BIGINT, p_amount NUMERIC)
LANGUAGE plpgsql AS $$
BEGIN
  IF p_amount <= 0 THEN
    RAISE EXCEPTION 'amount must be positive';
  END IF;
  UPDATE account SET balance = balance - p_amount WHERE account_no = p_from;
  IF NOT FOUND THEN RAISE EXCEPTION 'source account % missing', p_from; END IF;
  UPDATE account SET balance = balance + p_amount WHERE account_no = p_to;
  IF NOT FOUND THEN RAISE EXCEPTION 'target account % missing', p_to; END IF;
END;
$$;
CALL transfer(100001, 100002, 500);   -- any exception rolls back both updates
-- balance >= 0 is enforced by CHECK; to be safe against races lock the rows first (SELECT ... FOR UPDATE, lower account number first).""",
      ["CREATE PROCEDURE ... LANGUAGE plpgsql", "Validates the amount with RAISE EXCEPTION", "Debit and credit in one unit, checks FOUND for missing accounts", "Explains that an exception rolls everything back (atomicity)", "CALL syntax; bonus: row locking or CHECK for overdraft"]),
    P("p08", 1, "views and grants", "Hide salaries from analysts",
      "Analysts may see employee names, department and city, but never salaries. Write the PostgreSQL statements: a view, a role analyst, and the grants.",
      """CREATE VIEW employee_public AS
SELECT id, name, dept_id, city FROM employees;

CREATE ROLE analyst NOLOGIN;
REVOKE ALL ON employees FROM analyst;           -- (and from PUBLIC if needed)
GRANT SELECT ON employee_public TO analyst;
-- alternative: column-level grant  GRANT SELECT (id, name, dept_id, city) ON employees TO analyst;""",
      ["CREATE VIEW without the salary column", "Creates the role", "GRANT SELECT on the view (or column list) only", "Keeps direct access to the base table closed"]),
    P("p09", 2, "indexing", "Choose indexes",
      "Table orders(order_id, customer_id, status, created_at, total) has 50 million rows. Frequent queries: (1) WHERE customer_id = ? ORDER BY created_at DESC LIMIT 20; (2) WHERE status = 'pending' (about 0.2% of rows); (3) WHERE created_at >= ? AND created_at < ?; (4) WHERE LOWER(email) = ? on the customers table. Write the CREATE INDEX statements for PostgreSQL and justify each.",
      """(1) CREATE INDEX idx_orders_cust_created ON orders (customer_id, created_at DESC);
    Equality column first, then the ORDER BY column: the top 20 rows are read straight from the index.
(2) CREATE INDEX idx_orders_pending ON orders (order_id) WHERE status = 'pending';
    A partial index: tiny, because only 0.2% of rows qualify. (A plain index on status would have poor selectivity.)
(3) CREATE INDEX idx_orders_created ON orders (created_at);   -- or BRIN if the table is append-only and ordered by time
(4) CREATE INDEX idx_customers_lower_email ON customers (LOWER(email));
    An expression index, because a plain index on email cannot serve LOWER(email).""",
      ["Composite index with equality column before the sort column", "Partial index for the rare status value", "Index on created_at for the range (BRIN as a bonus)", "Expression index for LOWER(email)", "Gives a reason for each choice"]),
    P("p10", 2, "partitioning", "Partition by month",
      "Write PostgreSQL DDL for a table event(id, occurred_at, payload) partitioned by month on occurred_at, with partitions for January and February 2026 and a default partition. Explain how you drop old data.",
      """CREATE TABLE event (
  id BIGINT GENERATED ALWAYS AS IDENTITY,
  occurred_at TIMESTAMPTZ NOT NULL,
  payload JSONB,
  PRIMARY KEY (id, occurred_at)          -- the key must contain the partition column
) PARTITION BY RANGE (occurred_at);

CREATE TABLE event_2026_01 PARTITION OF event FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
CREATE TABLE event_2026_02 PARTITION OF event FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');
CREATE TABLE event_default PARTITION OF event DEFAULT;

-- old data: ALTER TABLE event DETACH PARTITION event_2026_01;  then archive or DROP TABLE event_2026_01;  (instant, unlike DELETE)""",
      ["PARTITION BY RANGE (occurred_at) on the parent", "Primary key includes the partition column", "Two PARTITION OF ... FOR VALUES FROM ... TO ... with correct bounds", "A DEFAULT partition", "Drops old data by detaching/dropping a partition"]),
    P("p11", 2, "window", "Top N per group (PostgreSQL)",
      "Using employees(id, name, dept_id, salary), write one query returning the top 2 earners per department, and a second PostgreSQL-specific query returning only the single top earner per department.",
      """SELECT * FROM (
  SELECT id, name, dept_id, salary,
         ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC, id) AS rn
  FROM employees
) t WHERE rn <= 2;

SELECT DISTINCT ON (dept_id) id, name, dept_id, salary
FROM employees
ORDER BY dept_id, salary DESC, id;""",
      ["Window function with PARTITION BY dept_id ORDER BY salary DESC", "Filters rn <= 2 in an outer query (not in WHERE of the same level)", "Uses DISTINCT ON (dept_id) for the second query", "ORDER BY begins with dept_id and sorts salary descending", "Mentions a tiebreaker or RANK for ties"]),
    P("p12", 2, "upsert", "Insert or update, both engines",
      "stock(sku PRIMARY KEY, qty). Write the statement that adds 5 units to sku 'A1', inserting the row if it does not exist, in PostgreSQL and in MySQL.",
      """-- PostgreSQL
INSERT INTO stock (sku, qty) VALUES ('A1', 5)
ON CONFLICT (sku) DO UPDATE SET qty = stock.qty + EXCLUDED.qty;

-- MySQL
INSERT INTO stock (sku, qty) VALUES ('A1', 5)
ON DUPLICATE KEY UPDATE qty = qty + VALUES(qty);""",
      ["PostgreSQL ON CONFLICT (sku) DO UPDATE", "Adds to the existing quantity rather than overwriting", "MySQL ON DUPLICATE KEY UPDATE", "Uses EXCLUDED / VALUES to refer to the new row"]),
    P("p13", 1, "theory", "DELETE vs TRUNCATE vs DROP",
      "Explain the differences between DELETE, TRUNCATE and DROP TABLE in an interview-style answer. Include at least five points.",
      """DELETE: DML. Removes chosen rows (WHERE), row by row, logged per row, fires row triggers, can be rolled back, does not reset auto-increment, table and indexes stay.
TRUNCATE: DDL. Removes all rows at once by deallocating pages, very fast, no WHERE, no row triggers, resets identity (RESTART IDENTITY in PostgreSQL), blocked when referenced by foreign keys (CASCADE in PostgreSQL). Rollback works in PostgreSQL but not in MySQL (implicit commit).
DROP TABLE: DDL. Removes the table itself: structure, rows, indexes, constraints and privileges. Anything depending on it breaks (views, foreign keys unless CASCADE).""",
      ["DELETE is DML with WHERE; TRUNCATE and DROP are DDL", "TRUNCATE is faster / removes all rows only", "DROP removes the structure as well", "Rollback and trigger behaviour differ", "Mentions identity reset or foreign-key restrictions"]),
    P("p14", 2, "theory", "Explain ACID with a transfer",
      "Using a bank transfer of 500 from account A to account B, explain each ACID property and name the mechanism that provides it.",
      """Atomicity: debit and credit both happen or neither does (rollback using the undo log).
Consistency: constraints and rules still hold afterwards (balance >= 0, total money unchanged); enforced by constraints, triggers and correct application logic.
Isolation: a concurrent transaction never sees a half-done transfer (locking or MVCC; isolation levels control how strict).
Durability: after COMMIT the transfer survives a crash because the commit record is flushed to the write-ahead log before acknowledging.""",
      ["Atomicity with the debit/credit example and rollback", "Consistency with a named rule", "Isolation with locking or MVCC", "Durability with the write-ahead log", "Names mechanisms rather than only definitions"]),
    P("p15", 2, "theory", "Isolation anomalies",
      "Define dirty read, non-repeatable read and phantom read with a short example each, and say which isolation level prevents each.",
      """Dirty read: T2 reads a row T1 changed but has not committed; T1 rolls back, so T2 used data that never existed. Prevented from READ COMMITTED upward.
Non-repeatable read: T1 reads a row twice; T2 updates and commits in between, so the values differ. Prevented from REPEATABLE READ upward.
Phantom read: T1 runs the same range query twice; T2 inserts or deletes a matching row in between, so the row set differs. Prevented by SERIALIZABLE in the standard (PostgreSQL REPEATABLE READ also prevents it; InnoDB prevents most with next-key locks).""",
      ["Dirty read definition with uncommitted data and rollback", "Non-repeatable read: same row, different value", "Phantom read: same predicate, different rows", "Maps each to an isolation level", "Mentions the default levels of PostgreSQL or MySQL"]),
    P("p16", 3, "concurrency", "Deadlock",
      "Describe a concrete two-transaction deadlock on rows of an accounts table, say how the database reacts, and give two ways to avoid it.",
      """T1: UPDATE accounts SET ... WHERE id = 1;   T2: UPDATE accounts SET ... WHERE id = 2;
T1: UPDATE accounts SET ... WHERE id = 2;   (waits for T2's lock)
T2: UPDATE accounts SET ... WHERE id = 1;   (waits for T1's lock)  -> circular wait.
The database detects the cycle in its wait-for graph and aborts one transaction (the victim) with a deadlock error; the other continues.
Avoid: always lock/update rows in the same order (for example ascending id); keep transactions short; take all locks up front with SELECT ... FOR UPDATE in a fixed order; retry the aborted transaction.""",
      ["Concrete interleaving with two rows and two transactions", "Names the circular wait / wait-for graph", "Database aborts a victim", "Consistent lock ordering", "Short transactions or retry logic"]),
    P("p17", 3, "normalization", "Normalize an invoice",
      "Unnormalized: INVOICE(inv_no, inv_date, cust_id, cust_name, cust_city, items{ product_id, product_name, unit_price, qty }). Normalize to 3NF and give the final tables with keys.",
      """1NF: remove the repeating group: one row per invoice line. Key (inv_no, product_id).
2NF: inv_date, cust_id, cust_name, cust_city depend on inv_no only; product_name, unit_price depend on product_id only. Split.
3NF: cust_name and cust_city depend on cust_id, not on inv_no: split customer out.

  CUSTOMER(cust_id PK, cust_name, cust_city)
  INVOICE(inv_no PK, inv_date, cust_id FK)
  PRODUCT(product_id PK, product_name, unit_price)
  INVOICE_LINE(inv_no FK, product_id FK, qty, PK (inv_no, product_id))
Note: store the price actually charged in INVOICE_LINE.unit_price if prices change over time.""",
      ["Removes the repeating group for 1NF", "Identifies partial dependencies and splits invoice and product", "Identifies the transitive customer dependency", "Final four tables with correct keys", "Mentions the price snapshot subtlety (bonus)"]),
    P("p18", 2, "relational algebra", "Write algebra expressions",
      "With relations EMP(eid, name, dept, salary) and DEPT(dept, dname), write relational algebra for: (a) names of employees earning more than 50000; (b) names of employees with their department names; (c) departments that have no employees.",
      """(a) π name ( σ salary > 50000 (EMP) )
(b) π name, dname ( EMP ⋈ DEPT )              (natural join on dept)
(c) π dept (DEPT) − π dept (EMP)                (set difference of department ids)""",
      ["(a) selection then projection in the right order", "(b) join on dept then projection", "(c) set difference of the department sets", "Uses the correct symbols σ π ⋈ −"]),
]


def build():
    return DDL + PAPER
