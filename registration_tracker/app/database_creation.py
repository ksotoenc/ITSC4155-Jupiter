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
semester_table = """    CREATE TABLE IF NOT EXISTS Semesters (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        term TEXT NOT NULL,
                        year INTEGER NOT NULL,
                        UNIQUE(term, year)
                        );
                        """
plan_semester_table = """   CREATE TABLE IF NOT EXISTS Plan_Semesters (
                            semester_id INTEGER,
                            plan_id INTEGER,
                            FOREIGN KEY(semester_id) REFERENCES Semesters(id),
                            FOREIGN KEY(plan_id) REFERENCES Plans(id),
                            UNIQUE(semester_id, plan_id)
                            );
                            """
plan_table = """    CREATE TABLE IF NOT EXISTS Plans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    major_id INTEGER NOT NULL,
                    concentration_id INTEGER,
                    num_semesters INTEGER NOT NULL,
                    student_id INTEGER NOT NULL,
                    advisor_id INTEGER,
                    FOREIGN KEY(student_id) REFERENCES Students(id),
                    FOREIGN KEY(advisor_id) REFERENCES Advisors(id)
                    FOREIGN KEY(major_id) REFERENCES Majors(id)
                    FOREIGN KEY(concentration_id) REFERENCES Concentrations(id)
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
admin_table = """   CREATE TABLE IF NOT EXISTS Admins (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL
                    );
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
                            );
                            """
major_section_req_table = """   CREATE TABLE IF NOT EXISTS Major_Section_Requirements (
                                section_id INTEGER NOT NULL,
                                group_id INTEGER NOT NULL,
                                course_subject TEXT,
                                course_number INTEGER,
                                FOREIGN KEY(section_id) REFERENCES Major_Sections(id),
                                FOREIGN KEY(course_subject, course_number) REFERENCES Courses(subject, number)
                                );
                                """
concentration_table = """ CREATE TABLE IF NOT EXISTS Concentrations (
                        major_id INTEGER NOT NULL,
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT UNIQUE NOT NULL,
                        FOREIGN KEY(major_id) REFERENCES Majors(id)
                        );
                        """
concentration_section_table = """   CREATE TABLE IF NOT EXISTS Concentration_Sections (
                                    concentration_id INTEGER NOT NULL,
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    section TEXT NOT NULL,
                                    credit_requirement INTEGER,
                                    FOREIGN KEY(concentration_id) REFERENCES Concentrations(id)
                                    );
                                    """
concentration_section_req_table = """   CREATE TABLE IF NOT EXISTS Concentration_Section_Requirements (
                                        section_id INTEGER NOT NULL,
                                        group_id INTEGER NOT NULL,
                                        course_subject TEXT,
                                        course_number INTEGER,
                                        FOREIGN KEY(section_id) REFERENCES Concentration_Sections(id),
                                        FOREIGN KEY(course_subject, course_number) REFERENCES Courses(subject, number)
                                        );
                                        """
gen_ed_section_table = """  CREATE TABLE IF NOT EXISTS Gen_Ed_Sections (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            section TEXT NOT NULL,
                            credit_requirement INTEGER
                            );
                            """
gen_ed_section_req_table = """  CREATE TABLE IF NOT EXISTS Gen_Ed_Section_Requirements (
                                section_id INTEGER NOT NULL,
                                group_id INTEGER NOT NULL,
                                course_subject TEXT,
                                course_number INTEGER,
                                FOREIGN KEY(section_id) REFERENCES Gen_Ed_Sections(id),
                                FOREIGN KEY(course_subject, course_number) REFERENCES Courses(subject, number)
                                );
                                """
minor_table = """   CREATE TABLE IF NOT EXISTS Minors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL
                    );
                    """
minor_section_table = """   CREATE TABLE IF NOT EXISTS Minor_Sections (
                            minor_id INTEGER NOT NULL,
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            section TEXT NOT NULL,
                            credit_requirement INTEGER,
                            FOREIGN KEY(minor_id) REFERENCES Minors(id)
                            );
                            """
minor_section_req_table = """   CREATE TABLE IF NOT EXISTS Minor_Section_Requirements (
                                section_id INTEGER NOT NULL,
                                group_id INTEGER NOT NULL,
                                course_subject TEXT,
                                course_number INTEGER,
                                FOREIGN KEY(section_id) REFERENCES Minor_Sections(id),
                                FOREIGN KEY(course_subject, course_number) REFERENCES Courses(subject, number)
                                );
                                """

plan_semester_courses_table = """ CREATE TABLE IF NOT EXISTS Plan_Semester_Courses (
                                plan_id INTEGER,
                                semester_id INTEGER,
                                course_subject TEXT,
                                course_number INTEGER,
                                FOREIGN KEY(plan_id) REFERENCES Plans(id),
                                FOREIGN KEY(semester_id) REFERENCES Semesters(id),
                                FOREIGN KEY(course_subject, course_number) REFERENCES Courses(subject, number),
                                UNIQUE(plan_id, semester_id, course_subject, course_number)
                                );
                                """
#endregion

# Create tables in database if they don't exist
cur.execute(prereq_table)
cur.execute(course_table)
cur.execute(semester_table)
cur.execute(plan_semester_table)
cur.execute(plan_table)
cur.execute(student_table)
cur.execute(advisor_table)
cur.execute(admin_table)
cur.execute(note_table)

cur.execute(major_table)
cur.execute(major_section_table)
cur.execute(major_section_req_table)
cur.execute(concentration_table)
cur.execute(concentration_section_table)
cur.execute(concentration_section_req_table)
cur.execute(gen_ed_section_table)
cur.execute(gen_ed_section_req_table)
cur.execute(minor_table)
cur.execute(minor_section_table)
cur.execute(minor_section_req_table)
cur.execute(plan_semester_courses_table)

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
            ('ITIS', 3310, 'Software Arch & Design', 3),

            -- CS MAJOR COURSES
            ('ITSC', 1600, 'Computing Professionals', 2),
            ('ITSC', 2600, 'Computer Science Program, Identity, Career', 2),
            ('ITSC', 2175, 'Logic and Algorithms', 3),
            ('MATH', 2165, 'Introduction to Discrete Structures', 3),
            ('ITSC', 2181, 'Introduction to Computer Systems', 4),
            ('ITSC', 3146, 'Introduction to Operating Systems and Networking', 3),
            ('ITSC', 3688, 'Computers and Their Impact on Society', 3),
            ('MATH', 2164, 'Matrices and Linear Algebra', 3),
            ('STAT', 2122, 'Introduction to Probability and Statistics', 3),
            ('ITCS', 4232, 'Game Design and Development Studio', 3),
            ('ITCS', 4238, 'Intelligent and Interactive System Studio', 3),
            ('ITIS', 4390, 'Interaction Design Projects', 3),
            ('ITIS', 4246, 'Competitive Cyber Defense', 3),
            ('ITSC', 4681, 'Senior Design I', 3),
            ('ITSC', 4682, 'Senior Design II', 3),
            ('ITSC', 4850, 'Senior Project I', 3),
            ('ITSC', 4851, 'Senior Project II', 3),
            ('ITSC', 4990, 'Undergraduate Research', 3),
            ('ITSC', 4991, 'Undergraduate Thesis', 3),
            ('ITSC', 4750, 'Honors Thesis', 3),

            -- CS MAJOR COURSES PREREQS
            ('DTSC', 1302, 'Data and Society B', 3),
            ('DTSC', 1301, 'Data and Society A', 3),
            ('ECGR', 2103, 'Computer Utilization in C++', 3),
            ('MATH', 2120, 'Intermediate Applied Calculus', 3),

            -- GEN ED COURSES
            ('WRDS', 1103, 'Writing and Inquiry in Academic Contexts I and II', 3),
            ('WRDS', 1104, 'Writing and Inquiry in Academic Contexts I and II with Studio', 4),
            ('ITSC', 1110, 'Introduction to Computer Science Principles', 3),
            ('MATH', 1100, 'College Algebra', 3),
            ('MATH', 1102, 'Introduction to Mathematical Thinking', 3),
            ('MATH', 1105, 'Finite Mathematics', 3),
            ('MATH', 1121, 'Calculus for Engineering Technology', 3),
            ('MATH', 1242, 'Calculus II', 3),
            ('MATH', 1340, 'Mathematics for Elementary Teachers I', 3),
            ('MATH', 1341, 'Mathematics for Elementary Teachers II', 3),
            ('PHIL', 2105, 'Deductive Logic', 3),
            ('STAT', 1220, 'Elements of Statistics I (BUSN)', 3),
            ('STAT', 1221, 'Elements of Statistics I', 3),
            ('STAT', 1222, 'Introduction to Statistics', 3),
            ('STAT', 1322, 'Introduction to Statistics II', 3),
            ('CTCM', 2530, 'Interdisciplinary Critical Thinking and Communication', 3),
            ('AFRS', 1501, 'Global Social Science: Africana Studies', 3),
            ('ANTH', 1501, 'Global Social Science: An Introduction to Anthropology', 3),
            ('CAPI', 1501, 'Global Social Science: Capitalism in a Global Context', 3),
            ('COMM', 1501, 'Global Social Science: Global and Intercultural Communication', 3),
            ('ECON', 1501, 'Global Social Science: Economics of Global Issues', 3),
            ('ESCI', 1501, 'Global Social Science: Environment, Society, and Sustainability', 3),
            ('GEOG', 1501, 'Global Social Science: Global Geography', 3),
            ('HONR', 1501, 'Global Social Science: Complex Emergencies, Crisis Management, Health & Development - Global Context', 3),
            ('INTL', 1501, 'Global Social Science: Globalization and Interdependence', 3),
            ('LTAM', 1501, 'Global Social Science: Introduction to Latin American Politics and Society', 3),
            ('POLS', 1501, 'Global Social Science: Introduction to Comparative Politics', 3),
            ('SOCY', 1501, 'Global Social Science: Sociological Approaches to Global Issues', 3),
            ('ARBC', 1502, 'Global Arts/Humanities: Modern Arab Culture', 3),
            ('ARCH', 1502, 'Global Arts/Humanities: Global Architecture, Culture, and Environment', 3),
            ('ARTA', 1502, 'Global Arts/Humanities: Art in a Global Context', 3),
            ('CHNS', 1502, 'Global Arts/Humanities: Chinese Culture in the World', 3),
            ('DANC', 1502, 'Global Arts/Humanities: Dance in Global Contexts', 3),
            ('ENGL', 1502, 'Global Arts/Humanities: Global Connections in English Studies', 3),
            ('FILM', 1502, 'Global Arts/Humanities: Introduction to Film and Media Art', 3),
            ('FRAN', 1502, 'Global Arts/Humanities: French and Francophone Cultures', 3),
            ('FREN', 1502, 'Global Arts/Humanities: French and Francophone Cultures', 3),
            ('GERM', 1502, 'Global Arts/Humanities: German and German-Speaking Cultures', 3),
            ('HIST', 1502, 'Global Arts/Humanities: Issues in Global History', 3),
            ('HONR', 1502, 'Global Arts/Humanities: Inquiry into the Visual Arts', 3),
            ('ITLN', 1502, 'Global Arts/Humanities: Italian Culture in the World', 3),
            ('JAPN', 1502, 'Global Arts/Humanities: Japanese Studies', 3),
            ('LACS', 1502, 'Global Arts/Humanities: Introduction to Global Cultures', 3),
            ('LTAM', 1502, 'Global Arts/Humanities: Introduction to Latin American History and Culture', 3),
            ('MUSC', 1502, 'Global Arts/Humanities: Music in Global Communities', 3),
            ('PHIL', 1502, 'Global Arts/Humanities: Global and Comparative Philosophy', 3),
            ('RELS', 1502, 'Global Arts/Humanities: Other Worlds', 3),
            ('SPAN', 1502, 'Global Arts/Humanities: Cultures of the Hispanic World', 3),
            ('THEA', 1502, 'Global Arts/Humanities: Theatre in Global Contexts', 3),
            ('WGST', 1502, 'Global Arts/Humanities: Introduction to Gender Studies Around the World', 3),
            ('ANTH', 1511, 'Local Social Science: Money, Health, and Happiness', 3),
            ('CJUS', 1511, 'Local Social Science: Foundations of Criminal Justice', 3),
            ('COMM', 1511, 'Local Social Science: Health, Well-Being, and Quality of Life', 3),
            ('EDUC', 1511, 'Local Social Science: Public Education and Schooling in the U.S.', 3),
            ('GEOG', 1511, 'Local Social Science: Urban and Regional Planning', 3),
            ('HAHS', 1511, 'Local Social Science: Issues of Health and Quality of Life', 3),
            ('HONR', 1511, 'Local Social Science: Media Literacy in Contemporary Culture', 3),
            ('POLS', 1511, 'Local Social Science: Introduction to American Politics', 3),
            ('SOCY', 1511, 'Local Social Science: Sociological Approaches to Local Issues', 3),
            ('SOWK', 1511, 'Local Social Science: The Field of Social Work', 3),
            ('AFRS', 1512, 'Local Arts/Humanities: Africana Studies', 3),
            ('CAPI', 1512, 'Local Arts/Humanities: Capitalism in the USA and Beyond', 3),
            ('CHNS', 1512, 'Local Arts/Humanities: Chinese and Chinese Culture in the U.S.', 3),
            ('DANC', 1512, 'Local Arts/Humanities: Dance in the United States', 3),
            ('ENGL', 1512, 'Local Arts/Humanities: Local Connections in English Studies', 3),
            ('FRAN', 1512, 'Local Arts/Humanities: French and Francophone Cultures in the U.S.', 3),
            ('FREN', 1512, 'Local Arts/Humanities: French & Francophone Cultures in the U.S.', 3),
            ('HIST', 1512, 'Local Arts/Humanities: Issues in US History', 3),
            ('HONR', 1512, 'Local Arts/Humanities', 3),
            ('ITLN', 1512, 'Local Arts/Humanities: Italian Culture in the U.S.', 3),
            ('MUSC', 1512, 'Local Arts/Humanities: Music in U.S. Communities', 3),
            ('PHIL', 1512, 'Local Arts/Humanities: Philosophy and Community', 3),
            ('RELS', 1512, 'Local Arts/Humanities: Religions in America', 3),
            ('SPAN', 1512, 'Local Arts/Humanities: US Hispanic, Latina/o/x Topics', 3),
            ('THEA', 1512, 'Local Arts/Humanities: Theatre in the United States', 3),
            ('WGST', 1512, 'Local Arts/Humanities: Introduction to Gender Studies in the U.S.', 3),
            ('ANTH', 2141, 'Our Place in Nature: Introduction to Biological Anthropology', 4),
            ('BINF', 1101, 'Introduction to Bioinformatics and Genomics', 4),
            ('BIOL', 1110, 'Principles of Biology I', 3),
            ('BIOL', 1115, 'Principles of Biology II', 3),
            ('CHEM', 1111, "Chemistry in Today's Society", 3),
            ('CHEM', 1200, 'Fundametals of Chemistry', 3),
            ('CHEM', 1203, 'Introduction to General, Organic, and Biochemistry I', 3),
            ('CHEM', 1204, 'Introduction to General, Organic, and Biochemistry II', 3),
            ('CHEM', 1251, 'General Chemistry I', 3),
            ('CHEM', 1252, 'General Chemistry II', 3),
            ('ESCI', 1101, 'Earth Sciences-Geography', 3),
            ('EXER', 2168, 'Human Anatomy and Physiology for the Health Professions', 3),
            ('EXER', 2169, 'Human Anatomy and Physiology for the Health Professions II', 3),
            ('GEOG', 1103, 'Spatial Thinking', 4),
            ('GEOL', 1200, 'Physical Geology', 3),
            ('GEOL', 1210, 'Earth History', 3),
            ('ITIS', 1350, 'eScience', 4),
            ('METR', 1102, 'Introduction to Meteorology Lab', 3),
            ('PHYS', 1100, 'Conceptual Physics I', 3),
            ('PHYS', 1101, 'Introductory Physics I', 3),
            ('PHYS', 1102, 'Introductory Physics II', 3),
            ('PHYS', 1130, 'Introduction to Astronomy', 3),
            ('PHYS', 1201, 'Sports and Physics', 3),
            ('PHYS', 1202, 'Introduction to Physics in Medicine', 3),
            ('PHYS', 1203, 'Physics of Music', 3),
            ('PHYS', 2101, 'Physics for Science and Engineering I', 3),
            ('PHYS', 2102, 'Physics for Science and Engineering II', 3),
            ('PSYC', 1101, 'General Psychology', 3),

            -- Gen Ed Courses Prerequisites
            ('MATH', 0900, 'Math Study Skills and Algebra Review', 1),

            -- Concentration Courses
            ('ITCS', 3153, 'Introduction to Artificial Intelligence', 3),
            ('ITCS', 3156, 'Introduction to Machine Learning', 3),
            ('ITCS', 3120, 'Introduction to Interactive Computer Graphics', 3),
            ('ITCS', 4101, 'Introduction to Natural Language Processing', 3),
            ('ITCS', 4114, 'Real World Algorithms', 3),
            ('ITCS', 4123, 'Visualization and Visual Communication', 3),
            ('ITCS', 4124, 'Advanced 3D Computer Graphics', 3),
            ('ITCS', 4150, 'Mobile Robotics', 3),
            ('ITCS', 4151, 'Intelligent Robotics', 3),
            ('ITCS', 4152, 'Introduction to Computer Vision', 3),
            ('ITCS', 4230, 'Introduction to Game Design and Development', 3),
            ('ITCS', 4231, 'Advanced Game Design and Development', 3),
            ('ITCS', 4236, 'Artificial Intelligence for Computer Games', 3),

            ('ITCS', 3160, 'Database Design and Implementation', 3),
            ('ITCS', 3162, 'Introduction to Data Mining', 3),
            ('ITCS', 3190, 'Introduction to Cloud Computing for Data Analysis', 3),
            ('ITCS', 3216, 'Introduction to Cognitive Science', 3),
            ('ITCS', 4121, 'Information Visualization', 3),
            ('INFO', 3236, 'Business Analytics', 3),
            ('ITIS', 4310, 'Web Mining', 3),

            ('ITCS', 3143, 'Operating Systems', 3),
            ('ITCS', 3166, 'Introduction to Computer Networks', 3),
            ('ITCS', 4102, 'Programming Languages', 3),
            ('ITCS', 4141, 'Computer Systems and Architecture: A Software Perspective', 3),
            ('ITIS', 3200, 'Introduction to Information Security and Privacy', 3),
            ('ITIS', 3246, 'IT Infrastructure and Security', 3),
            ('ITIS', 4166, 'Network-Based Application Development', 3),

            ('ITIS', 4221, 'Secure Programming and Penetration Testing', 3),
            ('ITIS', 4250, 'Computer Forensics', 3),
            ('ITIS', 4260, 'Introduction to Security Analytics', 3),
            ('ITIS', 4214, 'Usable Security ad Privacy', 3),
            ('ITIS', 4261, 'Introduction to Secured Cloud Computing', 3),

            ('ITIS', 3130, 'Introduction to Human-Centered Computing', 3),
            ('ITIS', 3140, 'User Experience Methods', 3),
            ('ITIS', 4350, 'Design Prototyping', 3),
            ('ITIS', 3216, 'Introduction to Cognitive Science', 3),
            ('ITIS', 4353, 'Social Technology Design', 3),
            ('ITIS', 4355, 'Accessible Design and Implementation', 3),
            ('ITIS', 4358, 'Physical Computing', 3),
            ('ITIS', 4360, 'Human-Centered Artificial Intelligence', 3),

            ('ITCS', 3112, 'Design and Implementation of Object-Oriented Systems', 3),
            ('ITIS', 3320, 'Introduction to Software Testing and Assurance', 3),
            ('ITIS', 4180, 'Mobile Application Development', 3),
            
            ('BINF', 2111, 'Introduction to Bioinformatics Computing', 4),
            ('BINF', 3101, 'Sequence Analysis', 3),
            ('BINF', 4600, 'Bioinformatics and Genomics Seminar', 1),
            ('BIOL', 3111, 'Cell Biology', 3),
            ('BIOL', 3166, 'Genetics', 3),
            ('BINF', 4211, 'Applied Data Mining for Bioinformatics', 4),
            ('BINF', 4171, 'Business of Biotechnology', 3),
            ('BINF', 4191, 'Life Sciences and the Law', 3),
            ('BINF', 3131, 'Bioinformatics Algorithms', 4),
            ('BINF', 3201, 'Genomic Methods', 4),
            
            ('BINF', 3121, 'Statistics for Bioinformatics', 3),

            -- CONCENTRATION PREREQUISITES
            ('BIOL', 2120, 'General Biology I', 3),
            ('BIOL', 2130, 'General Biology II', 3)
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
            ('ITIS', 3310, 0, 'ITSC', 2214),
            ('MATH', 1103, 0, 'MATH', 1100),
            ('MATH', 1103, 0, 'MATH', 1101),

            -- MAJOR COURSE PREREQUISITES
            ('ITSC', 2175, 0, 'ITSC', 1212),
            ('ITSC', 2175, 0, 'DTSC', 1302),
            ('ITSC', 2175, 1, 'MATH', 1120),
            ('ITSC', 2175, 1, 'MATH', 1241),
            ('DTSC', 1302, 0, 'DTSC', 1301),
            ('DTSC', 1302, 1, 'STAT', 1220),
            ('DTSC', 1302, 1, 'STAT', 1221),
            ('DTSC', 1302, 1, 'STAT', 1222),
            ('MATH', 1120, 0, 'MATH', 1100),
            ('MATH', 1120, 0, 'MATH', 1101),
            ('MATH', 1120, 0, 'MATH', 1103),
            ('MATH', 1241, 0, 'MATH', 1103),
            ('MATH', 2165, 0, 'ECGR', 2103),
            ('MATH', 2165, 0, 'ITSC', 1212),
            ('MATH', 2165, 1, 'MATH', 1241),
            ('ITSC', 2181, 0, 'ITSC', 1212),
            ('ITSC', 2181, 0, 'DTSC', 1302),
            ('ITSC', 3146, 0, 'ITSC', 2214),
            ('ITSC', 3146, 1, 'ITSC', 2181),
            ('MATH', 2164, 0, 'MATH', 1120),
            ('MATH', 2164, 0, 'MATH', 1241),
            ('STAT', 2122, 0, 'MATH', 1242),
            ('STAT', 2122, 0, 'MATH', 2120),
            ('ITCS', 4232, 0, 'ITSC', 3155),
            ('ITCS', 4232, 1, 'ITCS', 4231),
            ('ITCS', 4231, 0, 'ITCS', 4230),
            ('ITCS', 4230, 0, 'ITSC', 2214),
            ('ITCS', 4238, 0, 'ITCS', 3153),
            ('ITCS', 3153, 0, 'STAT', 2122),
            ('ITCS', 3153, 1, 'MATH', 2164),
            ('ITCS', 3153, 2, 'ITSC', 2214),
            ('ITIS', 4390, 0, 'ITIS', 3130),
            ('ITIS', 4390, 1, 'ITIS', 3135),
            ('ITIS', 4246, 0, 'ITIS', 3200),
            ('ITIS', 4246, 1, 'ITIS', 3246),
            ('ITIS', 3200, 0, 'ITSC', 2214),
            ('ITIS', 3246, 0, 'ITSC', 3146),
            ('ITSC', 4682, 0, 'ITSC', 4681),
            ('ITSC', 4851, 0, 'ITSC', 4850),
            ('ITSC', 4991, 0, 'ITCS', 4232),
            ('ITSC', 4991, 0, 'ITSC', 4155),
            ('ITSC', 4991, 0, 'ITSC', 4681),
            ('ITSC', 4991, 0, 'ITSC', 4850),
            ('ITSC', 4991, 0, 'ITSC', 4990),

            -- GEN ED PREREQUISITES
            ('MATH', 1100, 0, 'MATH', 0900),
            ('MATH', 1121, 0, 'MATH', 1103),
            ('MATH', 1242, 0, 'MATH', 1241),
            ('MATH', 1341, 0, 'MATH', 1340),
            ('STAT', 1220, 0, 'MATH', 1100),
            ('STAT', 1220, 0, 'MATH', 1101),
            ('STAT', 1220, 0, 'MATH', 1103),
            ('STAT', 1221, 0, 'MATH', 1100),
            ('STAT', 1221, 0, 'MATH', 1101),
            ('STAT', 1221, 0, 'MATH', 1103),
            ('STAT', 1322, 0, 'STAT', 1222),
            ('CTCM', 2530, 0, 'WRDS', 1103),
            ('CTCM', 2530, 0, 'WRDS', 1104),
            ('BIOL', 1115, 0, 'BIOL', 1110),
            ('CHEM', 1204, 0, 'CHEM', 1203),
            ('CHEM', 1251, 0, 'MATH', 1100),
            ('CHEM', 1251, 0, 'MATH', 1101),
            ('CHEM', 1251, 0, 'CHEM', 1200),
            ('CHEM', 1252, 0, 'CHEM', 1251),
            ('EXER', 2169, 0, 'EXER', 2168),
            ('GEOL', 1210, 0, 'GEOL', 1200),
            ('PHYS', 1101, 0, 'MATH', 1100),
            ('PHYS', 1101, 0, 'MATH', 1101),
            ('PHYS', 1102, 0, 'PHYS', 1101),
            ('PHYS', 2101, 0, 'MATH', 1241),
            ('PHYS', 2102, 0, 'PHYS', 2101),
            ('PHYS', 2102, 0, 'MATH', 1242),

            -- CONCENTRATION PREREQUISITES
            ('ITCS', 3156, 0, 'ITSC', 2214),
            ('ITCS', 3156, 1, 'STAT', 2122),
            ('ITCS', 3156, 2, 'MATH', 2164),
            ('ITCS', 3120, 0, 'ITSC', 2214),
            ('ITCS', 3120, 1, 'MATH', 2164),
            ('ITCS', 4101, 0, 'ITCS', 3156),
            ('ITCS', 4114, 0, 'ITSC', 2214),
            ('ITCS', 4114, 1, 'ITSC', 2175),
            ('ITCS', 4123, 0, 'ITSC', 2214),
            ('ITCS', 4124, 0, 'ITCS', 3120),
            ('ITCS', 4150, 0, 'ITSC', 2214),
            ('ITCS', 4150, 1, 'MATH', 2164),
            ('ITCS', 4151, 0, 'ITSC', 2214),
            ('ITCS', 4151, 1, 'MATH', 2164),
            ('ITCS', 4152, 0, 'ITCS', 3156),
            ('ITCS', 4230, 0, 'ITSC', 2214),
            ('ITCS', 4231, 0, 'ITCS', 4230),
            ('ITCS', 4236, 0, 'ITCS', 3153),
            ('ITCS', 3160, 0, 'ITSC', 1213),
            ('ITCS', 3162, 0, 'ITSC', 2214),
            ('ITCS', 3190, 0, 'ITSC', 2214),
            ('ITCS', 3216, 0, 'PSYC', 1101),
            ('ITCS', 4121, 0, 'ITSC', 1213),
            ('ITIS', 4310, 0, 'ITCS', 3160),
            ('ITCS', 3143, 0, 'ITSC', 2214),
            ('ITCS', 3166, 0, 'ITSC', 1213),
            ('ITCS', 4102, 0, 'ITSC', 2214),
            ('ITCS', 4141, 0, 'ITSC', 3146),
            ('ITIS', 3200, 0, 'ITSC', 2214),
            ('ITIS', 3246, 0, 'ITSC', 3146),
            ('ITIS', 4166, 0, 'ITCS', 3160),
            ('ITIS', 4166, 1, 'ITIS', 3135),
            ('ITIS', 4221, 0, 'ITIS', 3135),
            ('ITIS', 4250, 0, 'ITIS', 3135),
            ('ITIS', 4260, 0, 'ITIS', 3200),
            ('ITIS', 4260, 1, 'ITSC', 3146),
            ('ITIS', 4260, 2, 'STAT', 1220),
            ('ITIS', 4261, 0, 'ITSC', 3146),
            ('ITIS', 3216, 0, 'PSYC', 1101),
            ('ITCS', 3112, 0, 'ITSC', 2214),
            ('ITIS', 3320, 0, 'ITIS', 3200),
            ('ITIS', 3320, 1, 'ITIS', 3300),
            ('ITIS', 4180, 0, 'ITSC', 2214),
            ('BINF', 4600, 0, 'BINF', 3101),
            ('BIOL', 3111, 0, 'BIOL', 2120),
            ('BIOL', 3111, 1, 'BIOL', 2130),
            ('BIOL', 3111, 2, 'CHEM', 1252),
            ('BIOL', 3166, 0, 'BIOL', 2120),
            ('BIOL', 3166, 1, 'BIOL', 2130),
            ('BIOL', 3166, 2, 'CHEM', 1252),
            ('BINF', 3201, 0, 'BIOL', 1110),
            ('BINF', 3201, 0, 'BIOL', 2120),
            ('BINF', 3121, 0, 'BINF', 2111),
            ('BINF', 3121, 1, 'MATH', 1103),
            ('BINF', 3121, 1, 'MATH', 1120),
            ('BINF', 3121, 1, 'MATH', 1121),
            ('BINF', 3121, 1, 'MATH', 1241),
            ('BINF', 3121, 1, 'STAT', 1220),
            ('BINF', 3121, 1, 'STAT', 1221),
            ('BINF', 3121, 1, 'STAT', 2122)
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

# plans
cur.execute("""
            INSERT INTO Plans (name, major_id, concentration_id, num_semesters, student_id, advisor_id) VALUES
            ('test plan', 1, 1, 2, 1600343, 3409243)
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

# admins
cur.execute("""
            INSERT INTO Admins (username, password) VALUES
            ('ldeoliv1', 'pword')
            """)

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
            (4, 0, "ITCS", 4238),
            (4, 0, "ITIS", 4390),
            (4, 0, "ITIS", 4246),
            (4, 0, "ITSC", 4155),
            (4, 0, "ITSC", 4681),
            (4, 0, "ITSC", 4682),
            (4, 0, "ITSC", 4750),
            (4, 0, "ITSC", 4850),
            (4, 0, "ITSC", 4851),
            (4, 0, "ITSC", 4990),
            (4, 0, "ITSC", 4991)
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
            ("Quantitative/Data Competency Courses", 6),
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

            (4, 0, "AFRS", 1501),
            (4, 0, "ANTH", 1501),
            (4, 0, "CAPI", 1501),
            (4, 0, "COMM", 1501),
            (4, 0, "ECON", 1501),
            (4, 0, "ESCI", 1501),
            (4, 0, "GEOG", 1501),
            (4, 0, "HONR", 1501),
            (4, 0, "INTL", 1501),
            (4, 0, "LTAM", 1501),
            (4, 0, "POLS", 1501),
            (4, 0, "SOCY", 1501),
            (4, 1, "ARBC", 1502),
            (4, 1, "ARCH", 1502),
            (4, 1, "ARTA", 1502),
            (4, 1, "CHNS", 1502),
            (4, 1, "DANC", 1502),
            (4, 1, "ENGL", 1502),
            (4, 1, "FILM", 1502),
            (4, 1, "FRAN", 1502),
            (4, 1, "FREN", 1502),
            (4, 1, "GERM", 1502),
            (4, 1, "HIST", 1502),
            (4, 1, "HONR", 1502),
            (4, 1, "ITLN", 1502),
            (4, 1, "JAPN", 1502),
            (4, 1, "LACS", 1502),
            (4, 1, "LTAM", 1502),
            (4, 1, "MUSC", 1502),
            (4, 1, "PHIL", 1502),
            (4, 1, "RELS", 1502),
            (4, 1, "SPAN", 1502),
            (4, 1, "THEA", 1502),
            (4, 1, "WGST", 1502),
            (4, 2, "ANTH", 1511),
            (4, 2, "CJUS", 1511),
            (4, 2, "COMM", 1511),
            (4, 2, "EDUC", 1511),
            (4, 2, "GEOG", 1511),
            (4, 2, "HAHS", 1511),
            (4, 2, "HONR", 1511),
            (4, 2, "POLS", 1511),
            (4, 2, "SOCY", 1511),
            (4, 2, "SOWK", 1511),
            (4, 3, "AFRS", 1512),
            (4, 3, "CAPI", 1512),
            (4, 3, "CHNS", 1512),
            (4, 3, "DANC", 1512),
            (4, 3, "ENGL", 1512),
            (4, 3, "FRAN", 1512),
            (4, 3, "FREN", 1512),
            (4, 3, "HIST", 1512),
            (4, 3, "HONR", 1512),
            (4, 3, "ITLN", 1512),
            (4, 3, "MUSC", 1512),
            (4, 3, "PHIL", 1512),
            (4, 3, "RELS", 1512),
            (4, 3, "SPAN", 1512),
            (4, 3, "THEA", 1512),
            (4, 3, "WGST", 1512),
            
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