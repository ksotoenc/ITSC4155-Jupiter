import sqlite3
import streamlit as st

# Database Configuration (SQLite)
DB_NAME = "reg_tracker.db"

# Function to create a connection to SQLite
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Enables dictionary-like row access
    return conn

# Replace with function to get sample student data from SQLite
@st.cache_resource
def get_student():
    query = "SELECT ID, Username, Major, Graduation_Date, advisor_id FROM Students LIMIT 1"
    conn = get_db_connection()
    student = conn.execute(query).fetchone()
    conn.close()
    return student

# Retrieve a student's academic plan including all semesters and courses.
def get_student_plan(student_id):
    conn = get_db_connection()
    
    # Get the plan information for the student
    plan_query = """
    SELECT p.id, p.name, p.num_semesters, a.name as advisor_name
    FROM Plans p
    JOIN Advisors a ON p.advisor_id = a.id
    WHERE p.student_id = ?
    """
    plan = conn.execute(plan_query, (student_id,)).fetchone()
    
    if not plan:
        conn.close()
        return None
    
    # Get all semesters in the plan
    semesters_query = """
    SELECT s.id, s.term, s.year
    FROM Semesters s
    JOIN Plan_Semesters ps ON s.id = ps.semester_id
    WHERE ps.plan_id = ?
    ORDER BY s.year, 
        CASE 
            WHEN s.term = 'Spring' THEN 1
            WHEN s.term = 'Summer' THEN 2
            WHEN s.term = 'Fall' THEN 3
        END
    """
    semesters = conn.execute(semesters_query, (plan['id'],)).fetchall()
    
    # For each semester, get the courses
    plan_data = {
        'id': plan['id'],
        'name': plan['name'],
        'num_semesters': plan['num_semesters'],
        'advisor_name': plan['advisor_name'],
        'semesters': []
    }
    
    for semester in semesters:
        courses_query = """
        SELECT c.subject, c.number, c.name, c.credits
        FROM Courses c
        JOIN Course_Semesters cs ON c.subject = cs.course_subject AND c.number = cs.course_number
        WHERE cs.semester_id = ?
        ORDER BY c.subject, c.number
        """
        courses = conn.execute(courses_query, (semester['id'],)).fetchall()
        
        semester_data = {
            'id': semester['id'],
            'term': semester['term'],
            'year': semester['year'],
            'courses': []
        }
        
        for course in courses:
            semester_data['courses'].append({
                'subject': course['subject'],
                'number': course['number'],
                'name': course['name'],
                'credits': course['credits']
            })
        
        plan_data['semesters'].append(semester_data)
    
    conn.close()
    return plan_data