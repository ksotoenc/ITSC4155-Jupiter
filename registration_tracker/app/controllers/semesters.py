import sqlite3

DB_NAME = "reg_tracker.db"

# Function to create a connection to SQLite
def get_db_connection():
    con = sqlite3.connect(DB_NAME)
    con.row_factory = sqlite3.Row  # Enables dictionary-like row access
    return con

# get one semester
def get_semester(id):
    query = """ SELECT * FROM Semesters
                WHERE id = ?
                LIMIT 1 """
    con = get_db_connection()
    semester = con.execute(query, (id,)).fetchone()
    con.close()
    return semester

# get several semesters
def get_semesters(plan_id):
    query = """ SELECT * FROM Semesters s
                JOIN Plan_Semesters ps
                ON s.id = ps.semester_id
                WHERE ps.plan_id = ?
                ORDER BY s.year, 
                    CASE 
                        WHEN s.term = 'Spring' THEN 1
                        WHEN s.term = 'Summer' THEN 2
                        WHEN s.term = 'Fall' THEN 3
                    END"""
    con = get_db_connection()
    semesters = con.execute(query, (plan_id,)).fetchall()
    con.close()
    return semesters

# update a semester (admin)
def update_semester():
    pass

# delete a course (admin)
def delete_semester():
    pass