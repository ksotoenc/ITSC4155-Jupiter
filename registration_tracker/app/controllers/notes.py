import sqlite3

DB_NAME = "reg_tracker.db"

# Function to create a connection to SQLite
def get_db_connection():
    con = sqlite3.connect(DB_NAME)
    con.row_factory = sqlite3.Row  # Enables dictionary-like row access
    return con

# get advisor notes
def get_advisor_notes(advisor_id, plan_id):
    con = get_db_connection()
    query = """
        SELECT content, timestamp FROM Notes
        WHERE advisor_id = ? AND plan_id = ?
        ORDER BY timestamp DESC
    """
    result = con.execute(query, (advisor_id, plan_id)).fetchall()
    con.close()
    return result

# save advisor notes
def save_advisor_note(advisor_id, plan_id, content):
    con = get_db_connection()
    query = """
        INSERT INTO Notes (advisor_id, student_id, plan_id, content, timestamp)
        VALUES (?, NULL, ?, ?, strftime('%s', 'now'))
    """
    con.execute(query, (advisor_id, plan_id, content))
    con.commit()
    con.close()

# get student notes
def get_student_notes(student_id, plan_id):
    con = get_db_connection()
    query = """
        SELECT content, timestamp FROM Notes
        WHERE student_id = ? AND plan_id = ?
        ORDER BY timestamp DESC
    """
    result = con.execute(query, (student_id, plan_id)).fetchall()
    con.close()
    return result

# save student notes
def save_student_note(student_id, plan_id, content):
    con = get_db_connection()
    query = """
        INSERT INTO Notes (advisor_id, student_id, plan_id, content, timestamp)
        VALUES (NULL, ?, ?, ?, strftime('%s', 'now'))
    """
    con.execute(query, (student_id, plan_id, content))
    con.commit()
    con.close()
