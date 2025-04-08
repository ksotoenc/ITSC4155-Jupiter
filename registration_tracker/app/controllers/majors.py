import sqlite3

DB_NAME = "reg_tracker.db"

# Function to create a connection to SQLite
def get_db_connection():
    con = sqlite3.connect(DB_NAME)
    con.row_factory = sqlite3.Row  # Enables dictionary-like row access
    return con

# Get a major ID by name
def get_major_id(name):
    """
    Retrieves the ID of a major by its name.
    """
    query = """ SELECT id FROM Majors
                WHERE name = ? """
    con = get_db_connection()
    major = con.execute(query, (name,)).fetchone()
    con.close()
    return major['id'] if major else None

# Get all majors
def get_all_majors():
    """
    Retrieves all majors from the Majors table.
    """
    query = """ SELECT * FROM Majors """
    con = get_db_connection()
    majors = con.execute(query).fetchall()
    con.close()
    return majors

# Add a major (admin)
def add_major(name, department):
    """
    Adds a new major to the Majors table.
    """
    query = """ INSERT INTO Majors (name, department)
                VALUES (?, ?) """
    con = get_db_connection()
    try:
        con.execute(query, (name, department))
        con.commit()
        return {"success": True, "message": "Major added successfully."}
    except sqlite3.IntegrityError as e:
        return {"success": False, "message": f"Error adding major: {e}"}
    finally:
        con.close()

# Update a major (admin)
def update_major(major_id, name=None, department=None):
    """
    Updates an existing major in the Majors table.
    """
    fields = []
    values = []

    if name:
        fields.append("name = ?")
        values.append(name)
    if department:
        fields.append("department = ?")
        values.append(department)

    if not fields:
        return {"success": False, "message": "No fields to update."}

    query = f""" UPDATE Majors
                 SET {', '.join(fields)}
                 WHERE id = ? """
    values.append(major_id)

    con = get_db_connection()
    try:
        con.execute(query, values)
        con.commit()
        return {"success": True, "message": "Major updated successfully."}
    except sqlite3.Error as e:
        return {"success": False, "message": f"Error updating major: {e}"}
    finally:
        con.close()

# Delete a major (admin)
def delete_major(major_id):
    """
    Deletes a major from the Majors table.
    """
    query = """ DELETE FROM Majors
                WHERE id = ? """
    con = get_db_connection()
    try:
        con.execute(query, (major_id,))
        con.commit()
        return {"success": True, "message": "Major deleted successfully."}
    except sqlite3.Error as e:
        return {"success": False, "message": f"Error deleting major: {e}"}
    finally:
        con.close()