import sqlite3

DB_NAME = "reg_tracker.db"

# Function to create a connection to SQLite
def get_db_connection():
    con = sqlite3.connect(DB_NAME)
    con.row_factory = sqlite3.Row  # Enables dictionary-like row access
    return con

# get one course
def get_course(subject, number):
    query = """ SELECT * FROM Courses
                WHERE subject = ? AND number = ?
                LIMIT 1 """
    con = get_db_connection()
    course = con.execute(query, (subject, number)).fetchone()
    con.close()
    return course

# get several courses from prereq
def get_course_prereq(course_subject, course_number):
    query = """ SELECT group_id, course_subject, course_number FROM Prerequisites
                WHERE parent_subject = ? AND parent_number = ? """
    con = get_db_connection()
    prereqs = con.execute(query, (course_subject, course_number)).fetchall()
    con.close()
    return prereqs

def get_all_courses():
    query = """ SELECT * FROM Courses """
    con = get_db_connection()
    courses = con.execute(query).fetchall()
    con.close()
    return courses

# get several courses from semester
def get_semester_courses(semester_id, plan_id):
    query = """ SELECT * FROM Courses c
                JOIN Plan_Semester_Courses pcs
                ON c.subject = pcs.course_subject AND c.number = pcs.course_number
                WHERE pcs.semester_id = ? AND pcs.plan_id = ?
                ORDER BY c.subject, c.number """
    con = get_db_connection()
    courses = con.execute(query, (semester_id, plan_id)).fetchall()
    con.close()
    return courses

# add a course (admin)
def add_course(subject, number, name, credits):
    query = """ INSERT INTO Courses (subject, number, name, credits)
                VALUES (?, ?, ?, ?) """
    con = get_db_connection()
    try:
        con.execute(query, (subject, number, name, credits))
        con.commit()
        return {"success": True, "message": "Course added successfully."}
    except sqlite3.IntegrityError as e:
        return {"success": False, "message": f"Error adding course: {e}"}
    finally:
        con.close()

# update a course (admin)
def update_course(subject, number, name=None, credits=None):
    fields = []
    values = []

    if name:
        fields.append("name = ?")
        values.append(name)
    if credits:
        fields.append("credits = ?")
        values.append(credits)

    if not fields:
        return {"success": False, "message": "No fields to update."}

    query = f""" UPDATE Courses
                 SET {', '.join(fields)}
                 WHERE subject = ? AND number = ? """
    values.extend([subject, number])

    con = get_db_connection()
    try:
        con.execute(query, values)
        con.commit()
        return {"success": True, "message": "Course updated successfully."}
    except sqlite3.Error as e:
        return {"success": False, "message": f"Error updating course: {e}"}
    finally:
        con.close()

# delete a course (admin)
def delete_course(subject, number):
    query = """ DELETE FROM Courses
                WHERE subject = ? AND number = ? """
    con = get_db_connection()
    try:
        con.execute(query, (subject, number))
        con.commit()
        return {"success": True, "message": "Course deleted successfully."}
    except sqlite3.Error as e:
        return {"success": False, "message": f"Error deleting course: {e}"}
    finally:
        con.close()