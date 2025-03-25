import sqlite3

DB_NAME = "reg_tracker.db"

# Function to create a connection to SQLite
def get_db_connection():
    con = sqlite3.connect(DB_NAME)
    con.row_factory = sqlite3.Row  # Enables dictionary-like row access
    return con

# get one semester
def get_semester(id, selection="*"):
    query = """ SELECT ? FROM Semesters
                WHERE id = ?
                LIMIT 1 """
    con = get_db_connection()
    semester = con.execute(query, (selection, id,)).fetchone()
    con.close()
    return semester

# get several semesters
def get_semesters():

# update a semester (admin)
def update_semester():

# delete a course (admin)
def delete_semester():