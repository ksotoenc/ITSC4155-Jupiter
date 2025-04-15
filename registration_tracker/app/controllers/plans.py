import sqlite3
import controllers.semesters as semesters

DB_NAME = "reg_tracker.db"

# Function to create a connection to SQLite
def get_db_connection():
    con = sqlite3.connect(DB_NAME)
    con.row_factory = sqlite3.Row  # Enables dictionary-like row access
    return con

# Dynamically create a plan, adding semesters and courses as needed
def create_plan(student_id, advisor_id, name, major_id, start_term):
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
            INSERT INTO Plans (name, num_semesters, student_id, advisor_id, major_id)
            VALUES (?, 8, ?, ?, ?)
        """
        cur = con.execute(query, (name, student_id, advisor_id, major_id))
        plan_id = cur.lastrowid  # Get the ID of the newly inserted plan
        
        # Find the semester IDs for the next 8 semesters starting from start_term
        current_term = term
        current_year = year
        semester_ids = []
        
        for i in range(8):
            # Get the semester ID for the current term and year
            semester_query = """
                SELECT id FROM Semesters 
                WHERE term = ? AND year = ?
            """
            semester = con.execute(semester_query, (current_term, current_year)).fetchone()
            
            if semester:
                semester_id = semester[0]
                semester_ids.append(semester_id)
                
                # Link this semester to the plan
                con.execute("""
                    INSERT INTO Plan_Semesters (semester_id, plan_id)
                    VALUES (?, ?)
                """, (semester_id, plan_id))
            else:
                # Handle the case where the semester doesn't exist
                # You might want to create it
                pass
            
            # Move to the next semester
            if current_term == "Fall":
                current_term = "Spring"
                current_year += 1  # Spring of next year
            else:  # current_term == "Spring"
                current_term = "Fall"
                # Year stays the same for Fall
        
        # Now, distribute courses from major requirements across semesters
        # Get all required courses for the major
        major_courses_query = """
            SELECT course_subject, course_number, section
            FROM Major_Requirements
            WHERE major_id = ? AND course_subject IS NOT NULL AND course_number IS NOT NULL
            ORDER BY section, group_id
        """
        major_courses = con.execute(major_courses_query, (major_id,)).fetchall()
        
        # Get all prerequisites information
        prereq_query = """
            SELECT parent_subject, parent_number, group_id, course_subject, course_number
            FROM Prerequisites
        """
        prerequisites = con.execute(prereq_query).fetchall()
        
        # Create a map of courses to their prerequisites
        prereq_map = {}
        for prereq in prerequisites:
            parent = (prereq[0], prereq[1])  # (subject, number)
            if parent not in prereq_map:
                prereq_map[parent] = []
            prereq_map[parent].append({
                'group_id': prereq[2],
                'course': (prereq[3], prereq[4])  # (subject, number)
            })
        
        # Create a dictionary to keep track of which semester each course is assigned to
        course_to_semester = {}
        
        # Distribute courses across semesters while respecting prerequisites
        for semester_index, semester_id in enumerate(semester_ids):
            # For each semester, find courses that can be taken
            # (i.e., their prerequisites have been met)
            available_courses = []
            
            for course in major_courses:
                course_key = (course[0], course[1])
                
                # Skip if already assigned
                if course_key in course_to_semester:
                    continue
                
                # Check prerequisites
                can_take = True
                
                if course_key in prereq_map:
                    # Group prerequisites by group_id
                    groups = {}
                    for p in prereq_map[course_key]:
                        group_id = p['group_id']
                        if group_id not in groups:
                            groups[group_id] = []
                        groups[group_id].append(p['course'])
                    
                    # For each group, check if at least one prerequisite has been satisfied
                    for group_id, prereqs in groups.items():
                        group_satisfied = False
                        for prereq in prereqs:
                            if prereq in course_to_semester and course_to_semester[prereq] < semester_index:
                                group_satisfied = True
                                break
                        
                        if not group_satisfied:
                            can_take = False
                            break
                
                if can_take:
                    available_courses.append(course_key)
            
            # Limit the number of courses per semester (e.g., 4-5 courses)
            max_courses_per_semester = min(5, len(available_courses))
            courses_this_semester = available_courses[:max_courses_per_semester]
            
            # Assign these courses to the current semester
            for course in courses_this_semester:
                course_to_semester[course] = semester_index
                
                # Insert into Plan_Semester_Courses table
                con.execute("""
                    INSERT INTO Plan_Semester_Courses (plan_id, semester_id, course_subject, course_number)
                    VALUES (?, ?, ?, ?)
                """, (plan_id, semester_id, course[0], course[1]))
        
        # Check if all courses were assigned
        unassigned_courses = [c for c in major_courses if (c[0], c[1]) not in course_to_semester]
        if unassigned_courses:
            # There are unassigned courses, try to fit them in later semesters
            # or you could handle this differently based on your requirements
            pass
        
        con.commit()
        return True
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