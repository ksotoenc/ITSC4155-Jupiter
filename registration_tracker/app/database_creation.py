import sqlite3

# implicitly creates it if it does not exist
con = sqlite3.connect("reg_tracker.db")
# con represents the connection to the on-disk database

# database cursor to traverse database
cur = con.cursor()

#region Create table queries
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
concentration_table = """ CREATE TABLE IF NOT EXISTS Concentrations (
                        major_id INTEGER NOT NULL,
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT UNIQUE NOT NULL,
                        FOREIGN KEY(major_id) REFERENCES Majors(id)
                        );"""
concentration_section_table = """   CREATE TABLE IF NOT EXISTS Concentration_Sections (
                                    concentration_id INTEGER NOT NULL,
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    section TEXT NOT NULL,
                                    credit_requirement INTEGER,
                                    FOREIGN KEY(concentration_id) REFERENCES Concentrations(id)
                                    );"""
concentration_section_req_table = """   CREATE TABLE IF NOT EXISTS Concentration_Section_Requirements (
                                        section_id INTEGER NOT NULL,
                                        group_id INTEGER NOT NULL,
                                        course_subject TEXT,
                                        course_number INTEGER,
                                        FOREIGN KEY(section_id) REFERENCES Concentration_Sections(id),
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

plan_semester_courses_table = """ CREATE TABLE IF NOT EXISTS Plan_Semester_Courses (
                                plan_id INTEGER,
                                semester_id INTEGER,
                                course_subject TEXT,
                                course_number INTEGER,
                                FOREIGN KEY(plan_id) REFERENCES Plans(id),
                                FOREIGN KEY(semester_id) REFERENCES Semesters(id),
                                FOREIGN KEY(course_subject, course_number) REFERENCES Courses(subject, number)
                                );"""
#endregion

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
cur.execute(concentration_table)
cur.execute(concentration_section_table)
cur.execute(concentration_section_req_table)
cur.execute(gen_ed_section_table)
cur.execute(gen_ed_section_req_table)

#cur.execute(plan_semester_courses_table)

#region Add temp values into tables

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
            ('Fall', 2025),
            ('Spring', 2026),
            ('Fall', 2026), 
            ('Spring', 2027),
            ('Fall', 2027),
            ('Spring', 2028),
            ('Fall', 2028),
            ('Spring', 2029)
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

# major_section_requirements
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

# concentrations
cur.execute("""
            INSERT INTO Concentrations (major_id, name) VALUES
            (1, "AI, Robotics, and Gaming, B.S."),
            (1, "Data Science, B.S."),
            (1, "Systems and Networks, B.S."),
            (1, "Cybersecurity, B.S."),
            (1, "Human-Computer Interaction, B.A."),
            (1, "Information Technology, B.A."),
            (1, "Web/Mobile Development and Software Engineering, B.S."),
            (1, "Bioinformatics, B.A."),
            (1, "Bioinformatics, B.S.")
            """)
con.commit()

# concentration_sections
cur.execute("""
            INSERT INTO Concentration_Sections (concentration_id, section, credit_requirement) VALUES
            (1, "Concentration Required Course", 3),
            (1, "Concentration Elective Courses", 12),
            (1, "Concentration Technical Elective Courses", 6),

            (2, "Concentration Required Courses", 6),
            (2, "Concentration Elective Courses", 9),
            (2, "Concentration Technical Elective Courses", 6),

            (3, "Concentration Elective Courses", 15),
            (3, "Concentration Technical Elective Courses", 6),

            (4, "Concentration Required Courses", 24),
            (4, "Concentration Technical Elective Courses", 3),

            (5, "Concentration Core Courses", 12),
            (5, "Elective Courses", 6),
            (5, "Concentration Technical Elective Courses", 9),

            (6, "Concentration Core Courses", 15),
            (6, "Concentration Technical Elective Courses", 18),

            (7, "Required Concentration Courses", 12),
            (7, "Elective Concentration Courses", 9),
            (7, "Technical Elective Concentration Courses", 6),

            (8, "Required Concentration Courses", 18),
            (8, "Concentration Elective Courses", 11),
            
            (9, "Required Concentration Courses", 12),
            (9, "Concentration Elective Courses", 10)
            """)
con.commit()

# concentration_section_requirements
cur.execute("""
            INSERT INTO Concentration_Section_Requirements VALUES
            (1, 0, "ITCS", 3153),
            (1, 0, "ITCS", 3156),
            (2, 0, "ITCS", 3120),
            (2, 0, "ITCS", 3153),
            (2, 0, "ITCS", 3156),
            (2, 0, "ITCS", 4101),
            (2, 0, "ITCS", 4114),
            (2, 0, "ITCS", 4123),
            (2, 0, "ITCS", 4124),
            (2, 0, "ITCS", 4150),
            (2, 0, "ITCS", 4151),
            (2, 0, "ITCS", 4152),
            (2, 0, "ITCS", 4230),
            (2, 0, "ITCS", 4231),
            (2, 0, "ITCS", 4236),
            (3, 0, "ITSC", 3000),
            (3, 0, "ITSC", 4000),
            (3, 0, "ITCS", 3000),
            (3, 0, "ITCS", 4000),
            (3, 0, "ITIS", 3000),
            (3, 0, "ITIS", 4000),

            (4, 0, "ITCS", 3160),
            (4, 1, "ITCS", 3162),
            (5, 0, "ITCS", 3156),
            (5, 0, "ITCS", 3190),
            (5, 0, "ITCS", 3216),
            (5, 0, "ITCS", 4114),
            (5, 0, "ITCS", 4121),
            (5, 0, "ITCS", 4152),
            (5, 0, "INFO", 3236),
            (5, 0, "ITIS", 4310),
            (6, 0, "ITSC", 3000),
            (6, 0, "ITSC", 4000),
            (6, 0, "ITCS", 3000),
            (6, 0, "ITCS", 4000),
            (6, 0, "ITIS", 3000),
            (6, 0, "ITIS", 4000),

            (7, 0, "ITCS", 3143),
            (7, 0, "ITCS", 3156),
            (7, 0, "ITCS", 3160),
            (7, 0, "ITCS", 3166),
            (7, 0, "ITCS", 3190),
            (7, 0, "ITCS", 4102),
            (7, 0, "ITCS", 4141),
            (7, 0, "ITIS", 3200),
            (7, 0, "ITIS", 3246),
            (7, 0, "ITIS", 4166),
            (8, 0, "ITSC", 3000),
            (8, 0, "ITSC", 4000),
            (8, 0, "ITCS", 3000),
            (8, 0, "ITCS", 4000),
            (8, 0, "ITIS", 3000),
            (8, 0, "ITIS", 4000),

            (9, 0, "ITCS", 3160),
            (9, 1, "ITIS", 3135),
            (9, 2, "ITIS", 3200),
            (9, 3, "ITIS", 3246),
            (9, 4, "ITIS", 4166),
            (9, 5, "ITIS", 4221),
            (9, 6, "ITIS", 4250),
            (9, 7, "ITIS", 4260),
            (9, 7, "ITIS", 4214),
            (9, 7, "ITIS", 4261),
            (10, 0, "ITSC", 3000),
            (10, 0, "ITSC", 4000),
            (10, 0, "ITCS", 3000),
            (10, 0, "ITCS", 4000),
            (10, 0, "ITIS", 3000),
            (10, 0, "ITIS", 4000),

            (11, 0, "ITIS", 3130),
            (11, 1, "ITIS", 3135),
            (11, 2, "ITIS", 3140),
            (11, 3, "ITIS", 4350),
            (12, 0, "ITIS", 3216),
            (12, 0, "ITIS", 4214),
            (12, 0, "ITIS", 4353),
            (12, 0, "ITIS", 4355),
            (12, 0, "ITIS", 4358),
            (12, 0, "ITIS", 4360),
            (13, 0, "ITSC", 3000),
            (13, 0, "ITSC", 4000),
            (13, 0, "ITCS", 3000),
            (13, 0, "ITCS", 4000),
            (13, 0, "ITIS", 3000),
            (13, 0, "ITIS", 4000),

            (14, 0, "ITIS", 3130),
            (14, 1, "ITIS", 3135),
            (14, 2, "ITIS", 3200),
            (14, 3, "ITIS", 3300),
            (14, 4, "ITCS", 3160),
            (15, 0, "ITSC", 3000),
            (15, 0, "ITSC", 4000),
            (15, 0, "ITCS", 3000),
            (15, 0, "ITCS", 4000),
            (15, 0, "ITIS", 3000),
            (15, 0, "ITIS", 4000),

            (16, 0, "ITCS", 3160),
            (16, 1, "ITIS", 3135),
            (16, 2, "ITIS", 3310),
            (16, 3, "ITIS", 4221),
            (17, 0, "ITCS", 3112),
            (17, 0, "ITIS", 3130),
            (17, 0, "ITIS", 4350),
            (17, 0, "ITIS", 3300),
            (17, 0, "ITIS", 3320),
            (17, 0, "ITIS", 4166),
            (17, 0, "ITIS", 4180),
            (18, 0, "ITSC", 3000),
            (18, 0, "ITSC", 4000),
            (18, 0, "ITCS", 3000),
            (18, 0, "ITCS", 4000),
            (18, 0, "ITIS", 3000),
            (18, 0, "ITIS", 4000),
            
            (19, 0, "BINF", 1101),
            (19, 1, "BINF", 2111),
            (19, 2, "BINF", 3101),
            (19, 3, "BINF", 4600),
            (19, 4, "BIOL", 3111),
            (19, 5, "BIOL", 3166),
            (20, 0, "BINF", 4211),
            (20, 1, "BINF", 4171),
            (20, 1, "BINF", 4191),
            (20, 2, "BINF", 3131),
            (20, 2, "BINF", 3201),
            
            (21, 0, "BINF", 1101),
            (21, 1, "BINF", 2111),
            (21, 2, "BINF", 3101),
            (21, 3, "BINF", 4600),
            (22, 0, "BINF", 3121),
            (22, 0, "BINF", 4211),
            (22, 1, "BINF", 4171),
            (22, 1, "BINF", 4191),
            (22, 2, "BINF", 3131),
            (22, 2, "BINF", 3201)
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