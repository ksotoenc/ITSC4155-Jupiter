import sqlite3

DB_NAME = "reg_tracker.db"

# Function to create a connection to SQLite
def get_db_connection():
    con = sqlite3.connect(DB_NAME)
    con.row_factory = sqlite3.Row  # Enables dictionary-like row access
    return con

# get one advisor
def get_advisor(id):
    query = """ SELECT * FROM Advisors
                WHERE id = ?
                LIMIT 1 """
    con = get_db_connection()
    advisor = con.execute(query, (id,)).fetchone()
    con.close()
    return advisor

def get_advisor_user(user):
    query = """ SELECT id FROM Advisors
                WHERE username = ?
                LIMIT 1 """
    con = get_db_connection()
    advisor = con.execute(query, (user,)).fetchone()
    con.close()
    return advisor

# get all advisors
def get_all_advisors():
    query = """ SELECT * FROM Advisors
                """
    con = get_db_connection()
    advisors = con.execute(query).fetchall()
    con.close()
    return advisors

# add an advisor (admin)
def add_advisor(id, username, password, f_name, l_name):
    """
    Adds a new advisor to the Advisors table.
    """
    query = """ INSERT INTO Advisors (id, username, password, f_name, l_name)
                VALUES (?, ?, ?, ?, ?) """
    con = get_db_connection()
    try:
        con.execute(query, (id, username, password, f_name, l_name))
        con.commit()
        return {"success": True, "message": "Advisor added successfully."}
    except sqlite3.IntegrityError as e:
        return {"success": False, "message": f"Error adding advisor: {e}"}
    finally:
        con.close()

# update an advisor (admin)
def update_advisor(id, username=None, password=None, f_name=None, l_name=None):
    fields = []
    values = []

    if username:
        fields.append("username = ?")
        values.append(username)
    if password:
        fields.append("password = ?")
        values.append(password)
    if f_name:
        fields.append("f_name = ?")
        values.append(f_name)
    if l_name:
        fields.append("l_name = ?")
        values.append(l_name)

    if not fields:
        return {"success": False, "message": "No fields to update."}

    query = f""" UPDATE Advisors
                 SET {', '.join(fields)}
                 WHERE id = ? """
    values.append(id)

    con = get_db_connection()
    try:
        con.execute(query, values)
        con.commit()
        return {"success": True, "message": "Advisor updated successfully."}
    except sqlite3.Error as e:
        return {"success": False, "message": f"Error updating advisor: {e}"}
    finally:
        con.close()

# delete an advisor (admin)
def delete_advisor(id):
    query = """ DELETE FROM Advisors
                WHERE id = ? """
    con = get_db_connection()
    try:
        con.execute(query, (id,))
        con.commit()
        return {"success": True, "message": "Advisor deleted successfully."}
    except sqlite3.Error as e:
        return {"success": False, "message": f"Error deleting advisor: {e}"}
    finally:
        con.close()

# create notes
def get_advisor_note(advisor_id, student_id, plan_id):
    con = get_db_connection()
    query = """
        SELECT note_text FROM Advisor_Notes
        WHERE advisor_id = ? AND student_id = ? AND plan_id = ?
        ORDER BY timestamp DESC
        LIMIT 1
    """
    result = con.execute(query, (advisor_id, student_id, plan_id)).fetchone()
    con.close()
    return result["note_text"] if result else ""

# save notes
def save_advisor_note(advisor_id, student_id, plan_id, note_text):
    from datetime import datetime
    con = get_db_connection()
    query = """
        INSERT INTO Advisor_Notes (advisor_id, student_id, plan_id, note_text, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """
    con.execute(query, (advisor_id, student_id, plan_id, note_text, datetime.now().isoformat()))
    con.commit()
    con.close()
