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

# get all entries in Prerequisites table
def get_all_prereqs():
    query = """ SELECT * FROM Prerequisites """
    con = get_db_connection()
    prereqs = con.execute(query).fetchall()
    con.close()
    return prereqs

# add a prereq (admin)
def add_prereq(parent_subject, parent_number, group_id, course_subject, course_number):
    query = """ INSERT INTO Prerequisites (parent_subject, parent_number, group_id, course_subject, course_number)
                VALUES (?, ?, ?, ?, ?) """
    con = get_db_connection()
    try:
        con.execute(query, (parent_subject, parent_number, group_id, course_subject, course_number))
        con.commit()
        return {"success": True, "message": "Prerequisite added successfully."}
    except sqlite3.IntegrityError as e:
        return {"success": False, "message": f"Error adding prerequisite: {e}"}
    finally:
        con.close()

# update a prereq (admin)
def update_prereq(parent_subject, parent_number, group_id, course_subject=None, course_number=None):
    fields = []
    values = []

    if course_subject:
        fields.append("course_subject = ?")
        values.append(course_subject)
    if course_number:
        fields.append("course_number = ?")
        values.append(course_number)

    if not fields:
        return {"success": False, "message": "No fields to update."}

    query = f""" UPDATE Prerequisites
                 SET {', '.join(fields)}
                 WHERE parent_subject = ? AND parent_number = ? AND group_id = ? """
    values.extend([parent_subject, parent_number, group_id])

    con = get_db_connection()
    try:
        con.execute(query, values)
        con.commit()
        return {"success": True, "message": "Prerequisite updated successfully."}
    except sqlite3.Error as e:
        return {"success": False, "message": f"Error updating prerequisite: {e}"}
    finally:
        con.close()

# delete a prereq (admin)
def delete_prereq(parent_subject, parent_number, group_id):
    query = """ DELETE FROM Prerequisites
                WHERE parent_subject = ? AND parent_number = ? AND group_id = ? """
    con = get_db_connection()
    try:
        con.execute(query, (parent_subject, parent_number, group_id))
        con.commit()
        return {"success": True, "message": "Prerequisite deleted successfully."}
    except sqlite3.Error as e:
        return {"success": False, "message": f"Error deleting prerequisite: {e}"}
    finally:
        con.close()