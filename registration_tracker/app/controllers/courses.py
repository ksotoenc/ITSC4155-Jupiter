import sqlite3

DB_NAME = "reg_tracker.db"

# Function to create a connection to SQLite
def get_db_connection():
    con = sqlite3.connect(DB_NAME)
    con.row_factory = sqlite3.Row  # Enables dictionary-like row access
    return con

# get one course
def get_course(subject, number):
    query = """ SELECT * FROM Courses
                WHERE subject = ? AND number = ?
                LIMIT 1 """
    con = get_db_connection()
    course = con.execute(query, (subject, number)).fetchone()
    con.close()
    return course

# get several courses from prereq
def get_courses( ):
    pass

# get several courses from semester
def get_semester_courses(semester_id):
    query = """ SELECT * FROM Courses c
                JOIN Course_Semesters cs
                ON c.subject = cs.course_subject AND c.number = cs.course_number
                WHERE cs.semester_id = ?
                ORDER BY c.subject, c.number """
    con = get_db_connection()
    courses = con.execute(query, (semester_id,)).fetchall()
    con.close()
    return courses

# update a course (admin)
def update_course():
    pass

# delete a course (admin)
def delete_course():
    pass