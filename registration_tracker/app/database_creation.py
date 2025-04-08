import sqlite3

# implicitly creates it if it does not exist
con = sqlite3.connect("reg_tracker.db")
# con represents the connection to the on-disk database

# database cursor to traverse database
cur = con.cursor()

# CREATE TABLE
prereq_table = """  CREATE TABLE IF NOT EXISTS Prerequisites (
                    parent_subject TEXT NOT NULL,
                    parent_number INTEGER NOT NULL,
                    group_id INTEGER NOT NULL,
                    course_subject TEXT,
                    course_number INTEGER,
                    FOREIGN KEY(parent_subject, parent_number) REFERENCES Courses(subject, number),
                    FOREIGN KEY(course_subject, course_number) REFERENCES Courses(subject, number)
                    );
                    """
course_table = """  CREATE TABLE IF NOT EXISTS Courses (
                    subject TEXT,
                    number INTEGER,
                    name TEXT NOT NULL,
                    credits INTEGER NOT NULL,
                    PRIMARY KEY (subject, number)
                    ) WITHOUT ROWID;
                    """
course_semester_table = """ CREATE TABLE IF NOT EXISTS Course_Semesters (
                            semester_id INTEGER,
                            course_subject TEXT,
                            course_number INTEGER,
                            FOREIGN KEY(semester_id) REFERENCES Semesters(id),
                            FOREIGN KEY(course_subject, course_number) REFERENCES Courses(subject, number)
                            );
                            """
semester_table = """    CREATE TABLE IF NOT EXISTS Semesters (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        term TEXT NOT NULL,
                        year INTEGER NOT NULL
                        );
                        """
plan_semester_table = """   CREATE TABLE IF NOT EXISTS Plan_Semesters (
                            semester_id INTEGER,
                            plan_id INTEGER,
                            FOREIGN KEY(semester_id) REFERENCES Semesters(id),
                            FOREIGN KEY(plan_id) REFERENCES Plans(id)
                            );
                            """
plan_table = """    CREATE TABLE IF NOT EXISTS Plans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    major_id INTEGER NOT NULL,
                    num_semesters INTEGER NOT NULL,
                    student_id INTEGER NOT NULL,
                    advisor_id INTEGER,
                    FOREIGN KEY(student_id) REFERENCES Students(id),
                    FOREIGN KEY(advisor_id) REFERENCES Advisors(id)
                    FOREIGN KEY(major_id) REFERENCES Majors(id)
                    );
                    """
student_table = """ CREATE TABLE IF NOT EXISTS Students (
                    id INTEGER PRIMARY KEY,
                    f_name TEXT NOT NULL,
                    l_name TEXT NOT NULL,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL,
                    major_id INTEGER NOT NULL,
                    graduation_date INTEGER,
                    advisor_id INTEGER NOT NULL,
                    FOREIGN KEY(major_id) REFERENCES Majors(id),
                    FOREIGN KEY(advisor_id) REFERENCES Advisors(id)
                    ) WITHOUT ROWID;
                    """
advisor_table = """ CREATE TABLE IF NOT EXISTS Advisors (
                    id INTEGER PRIMARY KEY,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL,
                    f_name TEXT NOT NULL,
                    l_name TEXT NOT NULL
                    ) WITHOUT ROWID;
                    """
note_table = """    CREATE TABLE IF NOT EXISTS Notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    created_at INTEGER NOT NULL,
                    student_id INTEGER,
                    advisor_id INTEGER,
                    plan_id INTEGER NOT NULL,
                    FOREIGN KEY(student_id) REFERENCES Students(id),
                    FOREIGN KEY(advisor_id) REFERENCES Advisors(id),
                    FOREIGN KEY(plan_id) REFERENCES Plans(id),
                    CHECK ((student_id IS NOT NULL AND advisor_id IS NULL) OR (student_id IS NULL AND advisor_id IS NOT NULL))
                    );
                    """
major_table = """   CREATE TABLE IF NOT EXISTS Majors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    department TEXT NOT NULL
                    );
                    """
major_section_table = """   CREATE TABLE IF NOT EXISTS Major_Sections (
                            major_id INTEGER NOT NULL,
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            section TEXT NOT NULL,
                            credit_requirement INTEGER,
                            FOREIGN KEY(major_id) REFERENCES Majors(id)
                            );"""
major_section_req_table = """   CREATE TABLE IF NOT EXISTS Major_Section_Requirements (
                                section_id INTEGER NOT NULL,
                                group_id INTEGER NOT NULL,
                                course_subject TEXT,
                                course_number INTEGER,
                                FOREIGN KEY(section_id) REFERENCES Major_Sections(id),
                                FOREIGN KEY(course_subject, course_number) REFERENCES Courses(subject, number)
                                );"""
gen_ed_section_table = """  CREATE TABLE IF NOT EXISTS Gen_Ed_Sections (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            section TEXT NOT NULL,
                            credit_requirement INTEGER
                            );"""
gen_ed_section_req_table = """  CREATE TABLE IF NOT EXISTS Gen_Ed_Section_Requirements (
                                section_id INTEGER NOT NULL,
                                group_id INTEGER NOT NULL,
                                course_subject TEXT,
                                course_number INTEGER,
                                FOREIGN KEY(section_id) REFERENCES Gen_Ed_Sections(id),
                                FOREIGN KEY(course_subject, course_number) REFERENCES Courses(subject, number)
                                );"""

# Create tables in database if they don't exist
cur.execute(prereq_table)
cur.execute(course_table)
cur.execute(course_semester_table)
cur.execute(semester_table)
cur.execute(plan_semester_table)
cur.execute(plan_table)
cur.execute(student_table)
cur.execute(advisor_table)
cur.execute(note_table)
cur.execute(major_table)
cur.execute(major_section_table)
cur.execute(major_section_req_table)
cur.execute(gen_ed_section_table)
cur.execute(gen_ed_section_req_table)

#region Add temp values into tables
def get_course():
    query = "SELECT * FROM Courses LIMIT 1"
    course = con.execute(query).fetchone()
    return course

if (get_course() is None):
    # courses
    cur.execute("""
                INSERT INTO Courses VALUES
                ('ITSC', 4155, 'Software Development Projects', 3),
                ('ITSC', 2214, 'Data Structures and Algorithms', 3),
                ('ITSC', 1213, 'Introduction to Computer Science II', 4),
                ('ITSC', 1212, 'Introduction to Computer Science I', 4),
                ('MATH', 1101, 'College Algebra with Workshop', 4),
                ('MATH', 1103, 'Precalculus Mathematics for Science and Engineering', 3),
                ('MATH', 1120, 'Calculus', 3),
                ('MATH', 1241, 'Calculus I', 3),
                ('ITSC', 3155, 'Software Engineering', 3),
                ('ITIS', 3300, 'Software Req & Project Mgmt', 3),
                ('ITIS', 3135, 'Web-Based Application Design and Development', 3),
                ('ITIS', 3310, 'Software Arch & Design', 3)
                """)
    con.commit()

# prerequisites
cur.execute("""
            INSERT INTO Prerequisites VALUES
            ('ITSC', 4155, 0, 'ITSC', 2214),
            ('ITSC', 4155, 1, 'ITSC', 3155),
            ('ITSC', 4155, 1, 'ITIS', 3300),
            ('ITSC', 4155, 1, 'ITIS', 3310),
            ('ITSC', 2214, 0, 'ITSC', 1213),
            ('ITSC', 1213, 0, 'ITSC', 1212),
            ('ITSC', 1213, 1, 'MATH', 1101),
            ('ITSC', 1213, 1, 'MATH', 1103),
            ('ITSC', 1213, 1, 'MATH', 1120),
            ('ITSC', 1213, 1, 'MATH', 1241),
            ('ITSC', 3155, 0, 'ITSC', 2214),
            ('ITIS', 3300, 0, 'ITIS', 3135),
            ('ITIS', 3135, 0, 'ITSC', 2214),
            ('ITIS', 3310, 0, 'ITSC', 2214)
            """)
con.commit()

# semesters
cur.execute("""
            INSERT INTO Semesters (term, year) VALUES
            ('Spring', 2025),
            ('Summer', 2024)
            """)
con.commit()

# course_semesters
cur.execute("""
            INSERT INTO Course_Semesters VALUES
            (1, 'ITSC', 4155),
            (1, 'ITIS', 3310),
            (1, 'MATH', 1120),
            (1, 'ITSC', 1213),
            (1, 'MATH', 1241),
            (2, 'ITIS', 3135),
            (2, 'MATH', 1101),
            (2, 'ITSC', 1212),
            (2, 'MATH', 1103)
            """)
con.commit()

# plans
cur.execute("""
            INSERT INTO Plans (name, major_id, num_semesters, student_id, advisor_id) VALUES
            ('test plan', 1, 2, 1600343, 3409243)
            """)
con.commit()

# plan_semesters
cur.execute("""
            INSERT INTO Plan_Semesters VALUES
            (1, 1),
            (2, 1)
            """)
con.commit()

# students
cur.execute("""
            INSERT INTO Students VALUES
            (1600343, 'Terry', 'Trombo', 'tbone', 'password', '1', null, 3409243),
            (1600344, 'Jerry', 'Johnson', 'uname', 'pword', '1', null, 3409243)
            """)
con.commit()

# advisors
cur.execute("""
            INSERT INTO Advisors VALUES
            (3409243, 'adv_username', 'adv_passw0rd', 'Barry', 'Benson')
            """)
con.commit()

# notes
cur.execute("""
            INSERT INTO Notes (content, created_at, student_id, advisor_id, plan_id) VALUES
            ("This is a temporary note created by the advisor to show as an example for the notes feature!", 1748528160, NULL, 3409243, 1),
            ("This is another note created by the student slightly later...", 1748538160, 1600343, NULL, 1)
            """)
con.commit()

# majors
cur.execute("""
            INSERT INTO Majors (name, department) VALUES
            ("Computer Science", "College of Computing and Informatics")
            """)
con.commit()

# major_sections
cur.execute("""
            INSERT INTO Major_Sections (major_id, section, credit_requirement) VALUES
            (1, "Core Courses", 29),
            (1, "Mathematics and Statistics Courses", 6),
            (1, "Elective Courses in Other Disciplines", 15),
            (1, "Capstone Course", 3)
            """)
con.commit()

# major_sections_requirements
cur.execute("""
            INSERT INTO Major_Section_Requirements VALUES
            (1, 0, "ITSC", 1212),
            (1, 1, "ITSC", 1213),
            (1, 2, "ITSC", 1600),
            (1, 2, "ITSC", 2600),
            (1, 3, "ITSC", 2175),
            (1, 3, "MATH", 2165),
            (1, 4, "ITSC", 2181),
            (1, 5, "ITSC", 2214),
            (1, 6, "ITSC", 3146),
            (1, 7, "ITSC", 3155),
            (1, 8, "ITSC", 3688),
            (2, 0, "MATH", 2164),
            (2, 1, "STAT", 2122),
            (3, 0, "!ITSC", NULL),
            (3, 0, "!ITCS", NULL),
            (3, 0, "!ITIS", NULL),
            (4, 0, "ITCS", 4232),
            (4, 0, "ITIS", 4390),
            (4, 0, "ITIS", 4246),
            (4, 0, "ITSC", 4155),
            (4, 0, "ITSC", 4681),
            (4, 0, "ITSC", 4682),
            (4, 0, "ITSC", 4850),
            (4, 0, "ITSC", 4851),
            (4, 0, "ITSC", 4990),
            (4, 0, "ITSC", 4991),
            (4, 0, "ITSC", 4750)
            """)
con.commit()

# gen_ed_sections
cur.execute("""
            INSERT INTO Gen_Ed_Sections (section, credit_requirement) VALUES
            ("Communication Competency", 3),
            ("Quantitative/Dat Competency Courses", 6),
            ("Critical Thinking Competency", 3),
            ("Global and Local Themes", 12),
            ("Natural Sciences", 7)
            """)
con.commit()

# gen_ed_section_requirements
cur.execute("""
            INSERT INTO Gen_Ed_Section_Requirements VALUES
            (1, 0, "WRDS", 1103),
            (1, 0, "WRDS", 1104),
            (2, 0, "ITSC", 1110),
            (2, 0, "MATH", 1100),
            (2, 0, "MATH", 1101),
            (2, 0, "MATH", 1102),
            (2, 0, "MATH", 1103),
            (2, 0, "MATH", 1105),
            (2, 0, "MATH", 1120),
            (2, 0, "MATH", 1121),
            (2, 0, "MATH", 2165),
            (2, 0, "MATH", 1241),
            (2, 0, "MATH", 1242),
            (2, 0, "MATH", 1340),
            (2, 0, "MATH", 1341),
            (2, 0, "PHIL", 2105),
            (2, 0, "STAT", 1220),
            (2, 0, "STAT", 1221),
            (2, 0, "STAT", 1222),
            (2, 0, "STAT", 1322),
            (3, 0, "CTCM", 2530),
            (4, 0, "ANTH", 1511),
            (4, 0, "CJUS", 1511),
            (4, 0, "COMM", 1511),
            (4, 0, "EDUC", 1511),
            (4, 0, "GEOG", 1511),
            (4, 0, "HAHS", 1511),
            (4, 0, "HONR", 1511),
            (4, 0, "POLS", 1511),
            (4, 0, "SOCY", 1511),
            (4, 0, "SOWK", 1511),
            (4, 1, "AFRS", 1512),
            (4, 1, "CAPI", 1512),
            (4, 1, "CHNS", 1512),
            (4, 1, "DANC", 1512),
            (4, 1, "ENGL", 1512),
            (4, 1, "FRAN", 1512),
            (4, 1, "FREN", 1512),
            (4, 1, "HIST", 1512),
            (4, 1, "HONR", 1512),
            (4, 1, "ITLN", 1512),
            (4, 1, "MUSC", 1512),
            (4, 1, "PHIL", 1512),
            (4, 1, "RELS", 1512),
            (4, 1, "SPAN", 1512),
            (4, 1, "THEA", 1512),
            (4, 1, "WGST", 1512),
            (5, 0, "ANTH", 2141),
            (5, 0, "BINF", 1101),
            (5, 0, "BIOL", 1110),
            (5, 0, "BIOL", 1115),
            (5, 0, "CHEM", 1111),
            (5, 0, "CHEM", 1200),
            (5, 0, "CHEM", 1203),
            (5, 0, "CHEM", 1204),
            (5, 0, "CHEM", 1251),
            (5, 0, "CHEM", 1252),
            (5, 0, "ESCI", 1101),
            (5, 0, "EXER", 2168),
            (5, 0, "EXER", 2169),
            (5, 0, "GEOG", 1103),
            (5, 0, "GEOL", 1200),
            (5, 0, "GEOL", 1210),
            (5, 0, "ITIS", 1350),
            (5, 0, "METR", 1102),
            (5, 0, "PHYS", 1100),
            (5, 0, "PHYS", 1101),
            (5, 0, "PHYS", 1102),
            (5, 0, "PHYS", 1130),
            (5, 0, "PHYS", 1201),
            (5, 0, "PHYS", 1202),
            (5, 0, "PHYS", 1203),
            (5, 0, "PHYS", 2101),
            (5, 0, "PHYS", 2102),
            (5, 0, "PSYC", 1101)
            """)
con.commit()

#endregion
con.close()