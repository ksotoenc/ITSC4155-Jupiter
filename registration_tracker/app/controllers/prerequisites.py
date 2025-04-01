import sqlite3

DB_NAME = "reg_tracker.db"

# Function to create a connection to SQLite
def get_db_connection():
    con = sqlite3.connect(DB_NAME)
    con.row_factory = sqlite3.Row  # Enables dictionary-like row access
    return con

# get all prereqs
def get_prereq(subject, number):
    query = """ SELECT * FROM Prerequisites p
                JOIN Courses c
                ON p.course_subject = c.subject AND p.course_number = c.number
                WHERE parent_subject = ? AND parent_number = ? """
    con = get_db_connection()
    prereqs = con.execute(query, (subject, number)).fetchall()
    con.close()
    return prereqs

# update a prereq (admin)
def update_prereq():
    pass
# delete a course (admin)
def delete_prereq():
    pass