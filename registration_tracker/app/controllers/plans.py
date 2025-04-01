import sqlite3

DB_NAME = "reg_tracker.db"

# Function to create a connection to SQLite
def get_db_connection():
    con = sqlite3.connect(DB_NAME)
    con.row_factory = sqlite3.Row  # Enables dictionary-like row access
    return con

# create a plan
def create_plan(student_id, advisor_id, name="Registration Plan"):
    query = """ INSERT INTO Plans (name, num_semesters, student_id, advisor_id)
                VALUES
                (?, 0, ?, ?) """
    con = get_db_connection()
    plan = con.execute(query, (name, student_id, advisor_id))
    con.commit()
    con.close()

# get one plan from id
def get_plan(id):
    query = """ SELECT * FROM Plans
                WHERE id = ?
                LIMIT 1 """
    con = get_db_connection()
    plan = con.execute(query, (id,)).fetchone()
    con.close()
    return plan

# get first plan attatched to student
def get_first_plan(student_id):
    query = """ SELECT * FROM Plans
                WHERE student_id = ?
                LIMIT 1 """
    con = get_db_connection()
    plan = con.execute(query, (student_id,)).fetchone()
    con.close()
    return plan

# get several plans from a student
def get_plans(student_id):
    query = """ SELECT * FROM Plans
                WHERE student_id = ?
                """
    con = get_db_connection()
    plans = con.execute(query, (student_id,)).fetchall()
    con.close()
    return plans

# update a plan (admin)
def update_plan():
    pass

# delete a course (admin)
def delete_plan():
    pass