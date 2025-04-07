import sqlite3

DB_NAME = "reg_tracker.db"

# Function to create a connection to SQLite
def get_db_connection():
    con = sqlite3.connect(DB_NAME)
    con.row_factory = sqlite3.Row  # Enables dictionary-like row access
    return con

# create a plan
def create_plan(student_id, advisor_id, name):
    query = """ INSERT INTO Plans (name, num_semesters, student_id, advisor_id)
                VALUES
                (?, 0, ?, ?) """
    con = get_db_connection()
    con.execute(query, (name, student_id, advisor_id))
    con.commit()
    con.close()

# get one plan from id
def get_plan(name, user, user_id):
    if user == "student":
        query = """ SELECT * FROM Plans
                    WHERE name = ? AND student_id = ?
                    LIMIT 1 """
    else:
        query = """ SELECT * FROM Plans
                    WHERE name = ? AND advisor_id = ?
                    LIMIT 1 """
    con = get_db_connection()
    plan = con.execute(query, (name, user_id)).fetchone()
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

# get all entries in Plans table
def get_all_plans():
    query = """ SELECT * FROM Plans """
    con = get_db_connection()
    plans = con.execute(query).fetchall()
    con.close()
    return plans

# get several plans from a student
def get_plans(user, user_id):
    if user == "student":
        query = """ SELECT * FROM Plans
                    WHERE student_id = ?
                    """
    else:
        query = """ SELECT * FROM Plans
                    WHERE advisor_id = ?
                """
    con = get_db_connection()
    plans = con.execute(query, (user_id,)).fetchall()
    con.close()
    return plans

# update a plan (admin)
def update_plan(plan_id, name=None, num_semesters=None, student_id=None, advisor_id=None):
    fields = []
    values = []

    if name:
        fields.append("name = ?")
        values.append(name)
    if num_semesters:
        fields.append("num_semesters = ?")
        values.append(num_semesters)
    if student_id:
        fields.append("student_id = ?")
        values.append(student_id)
    if advisor_id:
        fields.append("advisor_id = ?")
        values.append(advisor_id)

    if not fields:
        return {"success": False, "message": "No fields to update."}

    query = f""" UPDATE Plans
                 SET {', '.join(fields)}
                 WHERE id = ? """
    values.append(plan_id)

    con = get_db_connection()
    try:
        con.execute(query, values)
        con.commit()
        return {"success": True, "message": "Plan updated successfully."}
    except sqlite3.Error as e:
        return {"success": False, "message": f"Error updating plan: {e}"}
    finally:
        con.close()

# delete a plan (admin)
def delete_plan(plan_id):
    query = """ DELETE FROM Plans
                WHERE id = ? """
    con = get_db_connection()
    try:
        con.execute(query, (plan_id,))
        con.commit()
        return {"success": True, "message": "Plan deleted successfully."}
    except sqlite3.Error as e:
        return {"success": False, "message": f"Error deleting plan: {e}"}
    finally:
        con.close()