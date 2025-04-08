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

# get semesters associated with a plan
def get_semesters(plan_id):
    query = """ SELECT * FROM Semesters s
                JOIN Plan_Semesters ps
                ON s.id = ps.semester_id
                WHERE ps.plan_id = ?
                ORDER BY s.year, 
                    CASE 
                        WHEN s.term = 'Spring' THEN 1
                        WHEN s.term = 'Fall' THEN 2
                    END"""
    con = get_db_connection()
    semesters = con.execute(query, (plan_id,)).fetchall()
    con.close()
    return semesters

# get all entries in Semesters table
def get_all_semesters():
    query = """ SELECT * FROM Semesters """
    con = get_db_connection()
    semesters = con.execute(query).fetchall()
    con.close()
    return semesters

# add a semester
def add_semester(term, year):
    """
    Adds a new semester to the Semesters table.
    """
    query = """ INSERT INTO Semesters (term, year)
                VALUES (?, ?) """
    con = get_db_connection()
    try:
        con.execute(query, (term, year))
        con.commit()
        return {"success": True, "message": "Semester added successfully."}
    except sqlite3.IntegrityError as e:
        return {"success": False, "message": f"Error adding semester: {e}"}
    finally:
        con.close()

# update a semester (admin)
def update_semester(id, term=None, year=None):
    """
    Updates an existing semester in the Semesters table.
    """
    fields = []
    values = []

    if term:
        fields.append("term = ?")
        values.append(term)
    if year:
        fields.append("year = ?")
        values.append(year)

    if not fields:
        return {"success": False, "message": "No fields to update."}

    query = f""" UPDATE Semesters
                 SET {', '.join(fields)}
                 WHERE id = ? """
    values.append(id)

    con = get_db_connection()
    try:
        con.execute(query, values)
        con.commit()
        return {"success": True, "message": "Semester updated successfully."}
    except sqlite3.Error as e:
        return {"success": False, "message": f"Error updating semester: {e}"}
    finally:
        con.close()

# delete a semester (admin)
def delete_semester(id):
    """
    Deletes a semester from the Semesters table.
    """
    query = """ DELETE FROM Semesters
                WHERE id = ? """
    con = get_db_connection()
    try:
        con.execute(query, (id,))
        con.commit()
        return {"success": True, "message": "Semester deleted successfully."}
    except sqlite3.Error as e:
        return {"success": False, "message": f"Error deleting semester: {e}"}
    finally:
        con.close()