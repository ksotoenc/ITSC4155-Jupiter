import sqlite3

DB_NAME = "reg_tracker.db"

# Function to create a connection to SQLite
def get_db_connection():
    con = sqlite3.connect(DB_NAME)
    con.row_factory = sqlite3.Row  # Enables dictionary-like row access
    return con

# get one advisor
def get_advisor(id, selection="*"):
    query = """ SELECT ? FROM Advisors
                WHERE id = ?
                LIMIT 1 """
    con = get_db_connection()
    advisor = con.execute(query, (selection, id,)).fetchone()
    con.close()
    return advisor

# get several advisors
def get_advisors():

# update a advisor (admin)
def update_advisor():

# delete a course (admin)
def delete_advisor():