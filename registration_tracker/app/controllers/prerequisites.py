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
                JOIN Course_Prerequisites cp
                ON c.parent_subject = cp.course_subject AND c.parent_number = cp.course_number AND c.group_id = cp.prequisite_group_id
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