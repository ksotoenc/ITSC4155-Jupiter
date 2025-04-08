import sqlite3

DB_NAME = "reg_tracker.db"

# Function to create a connection to SQLite
def get_db_connection():
    con = sqlite3.connect(DB_NAME)
    con.row_factory = sqlite3.Row  # Enables dictionary-like row access
    return con

# get one student
def get_student(identifier, value):
    if identifier == "username":
        query = """ SELECT * FROM Students
                    WHERE username = ?
                    LIMIT 1 """
    else:
        query = """ SELECT * FROM Students
                    WHERE id = ?
                    LIMIT 1 """
    con = get_db_connection()
    student = con.execute(query, (value,)).fetchone()
    con.close()
    return student

# get several students from an advisor
def get_students(advisor_id):
    query = """ SELECT * FROM Students
                WHERE advisor_id = ?
                """
    con = get_db_connection()
    students = con.execute(query, (advisor_id,)).fetchall()
    con.close()
    return students

# get all students
def get_all_students():
    query = """ SELECT * FROM Students
                """
    con = get_db_connection()
    students = con.execute(query).fetchall()
    con.close()
    return students

# add a student (admin)
def add_student(id, f_name, l_name, username, password, major_id, graduation_date, advisor_id):
    query = """ INSERT INTO Students (id, f_name, l_name, username, password, major_id, graduation_date, advisor_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?) """
    con = get_db_connection()
    try:
        con.execute(query, (id, f_name, l_name, username, password, major_id, graduation_date, advisor_id))
        con.commit()
        return {"success": True, "message": "Student added successfully."}
    except sqlite3.IntegrityError as e:
        return {"success": False, "message": f"Error adding student: {e}"}
    finally:
        con.close()
        
# update a student (admin)
def update_student(student_id, f_name=None, l_name=None, username=None, password=None, major_id=None, graduation_date=None, advisor_id=None):
    """
    Updates an existing student in the Students table.
    """
    fields = []
    values = []

    if f_name:
        fields.append("f_name = ?")
        values.append(f_name)
    if l_name:
        fields.append("l_name = ?")
        values.append(l_name)
    if username:
        fields.append("username = ?")
        values.append(username)
    if password:
        fields.append("password = ?")
        values.append(password)
    if major_id:
        fields.append("major = ?")
        values.append(major_id)
    if graduation_date:
        fields.append("graduation_date = ?")
        values.append(graduation_date)
    if advisor_id:
        fields.append("advisor_id = ?")
        values.append(advisor_id)

    if not fields:
        return {"success": False, "message": "No fields to update."}

    query = f""" UPDATE Students
                 SET {', '.join(fields)}
                 WHERE id = ? """
    values.append(student_id)

    con = get_db_connection()
    try:
        con.execute(query, values)
        con.commit()
        return {"success": True, "message": "Student updated successfully."}
    except sqlite3.Error as e:
        return {"success": False, "message": f"Error updating student: {e}"}
    finally:
        con.close()

# delete a student (admin)
def delete_student(student_id):
    """
    Deletes a student from the Students table.
    """
    query = """ DELETE FROM Students
                WHERE id = ? """
    con = get_db_connection()
    try:
        con.execute(query, (student_id,))
        con.commit()
        return {"success": True, "message": "Student deleted successfully."}
    except sqlite3.Error as e:
        return {"success": False, "message": f"Error deleting student: {e}"}
    finally:
        con.close()