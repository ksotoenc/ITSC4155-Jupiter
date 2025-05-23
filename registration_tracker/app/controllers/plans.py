import sqlite3
import controllers.semesters as semesters

DB_NAME = "reg_tracker.db"

# Function to create a connection to SQLite
def get_db_connection():
    con = sqlite3.connect(DB_NAME)
    con.row_factory = sqlite3.Row  # Enables dictionary-like row access
    return con

def create_plan(student_id, advisor_id, name, major_id, concentration_id, start_term, is_suggestion=0, original_plan_id=None):
    # Parse the start_term string (expected format: "Fall 2025" or "Spring 2026")
    term_parts = start_term.split()
    if len(term_parts) != 2:
        return False  # Invalid format
    
    term = term_parts[0]  # "Fall" or "Spring"
    year = int(term_parts[1])  # e.g., 2025
    
    con = get_db_connection()
    try:
        # Insert the plan and get its ID
        query = """
            INSERT INTO Plans (name, num_semesters, student_id, advisor_id, concentration_id, major_id, is_suggestion, original_plan_id)
            VALUES (?, 8, ?, ?, ?, ?, ?, ?)
        """
        cur = con.execute(query, (name, student_id, advisor_id, concentration_id, major_id, is_suggestion, original_plan_id))
        plan_id = cur.lastrowid  # Get the ID of the newly inserted plan
        
        # Find the semester IDs for the next 8 semesters starting from start_term
        current_term = term
        current_year = year
        
        for i in range(8):
            # Get the semester ID for the current term and year
            semester_query = """
                SELECT id FROM Semesters 
                WHERE term = ? AND year = ?
            """
            semester = con.execute(semester_query, (current_term, current_year)).fetchone()
            
            if semester:
                semester_id = semester[0]
                
                # Link this semester to the plan
                con.execute("""
                    INSERT INTO Plan_Semesters (semester_id, plan_id)
                    VALUES (?, ?)
                """, (semester_id, plan_id))
            else:
                # Create semester if it doesn't exist
                create_semester_query = """
                    INSERT INTO Semesters (term, year)
                    VALUES (?, ?)
                """
                cur = con.execute(create_semester_query, (current_term, current_year))
                semester_id = cur.lastrowid
                
                # Link this semester to the plan
                con.execute("""
                    INSERT INTO Plan_Semesters (semester_id, plan_id)
                    VALUES (?, ?)
                """, (semester_id, plan_id))
            
            # Move to the next semester
            if current_term == "Fall":
                current_term = "Spring"
                current_year += 1
            else:  
                current_term = "Fall"
                
        con.commit()
        return plan_id
    except Exception as e:
        con.rollback()
        print(f"Error creating plan: {e}")
        return False
    finally:
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

# get one plan from plan id
def get_plan_from_id(plan_id):
    query = """ SELECT * FROM Plans
                WHERE id = ?
                LIMIT 1
                """
    con = get_db_connection()
    plan = con.execute(query, (plan_id,)).fetchone()
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
def update_plan(plan_id, name=None, num_semesters=None, student_id=None, advisor_id=None, suggestion_accepted=False):
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
    if suggestion_accepted:
        fields.append("is_suggestion = ?")
        values.append(0)
        fields.append("original_plan_id = ?")
        values.append(None)

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