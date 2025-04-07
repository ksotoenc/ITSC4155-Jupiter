import sqlite3
import streamlit as st
import pandas as pd

# Database Configuration (SQLite)
DB_NAME = "reg_tracker.db"

# Function to create a connection to SQLite
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Enables dictionary-like row access
    return conn

# Retrieve a student's academic plan including all semesters and courses.
def get_student_plan(student_id, name):
    conn = get_db_connection()
    
    # Get the plan information for the student
    plan_query = """
    SELECT p.id, p.name, p.num_semesters, a.name as advisor_name
    FROM Plans p
    JOIN Advisors a ON p.advisor_id = a.id
    WHERE p.student_id = ? AND p.name = ?
    """
    plan = conn.execute(plan_query, (student_id,name)).fetchone()
    
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

# Display a given plan
def display_plan(plan):
    """
    Displays the academic plan for a student.

    Args:
        plan (dict): The academic plan data.
    """
    if plan:
        st.write(f"**Plan Name:** {plan['name']}")
        st.write(f"**Advisor:** {plan['advisor_name']}")
        
        # Calculate total credits
        total_credits = 0
        
        # Display each semester with its courses
        for semester in plan['semesters']:
            semester_credits = sum(course['credits'] for course in semester['courses'])
            total_credits += semester_credits
            
            with st.expander(f"{semester['term']} {semester['year']} ({semester_credits} credits)", expanded=True):
                # Create a table for courses
                course_data = []
                for course in semester['courses']:
                    course_data.append([
                        f"{course['subject']} {course['number']}",
                        course['name'],
                        course['credits']
                    ])
                
                if course_data:
                    st.table(pd.DataFrame(
                        course_data,
                        columns=["Course", "Title", "Credits"]
                    ))
                else:
                    st.info("No courses registered for this semester.")
        
        st.metric("Total Credits", total_credits)
    else:
        st.warning(f"No academic plan found.")

# MUST ADD MAJOR AND COURSES ASSIGNED TO THEM TO FUNCTIONALITY TO ACTUALLY CREATE A PLAN
