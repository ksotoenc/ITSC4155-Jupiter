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

def display_plan(plan_id):
    st.title("Degree Plan")
    
    con = get_db_connection()
    
    # Get plan details
    plan_query = """
        SELECT p.name, p.num_semesters, m.name as major_name
        FROM Plans p
        JOIN Majors m ON p.major_id = m.id
        WHERE p.id = ?
    """
    plan = con.execute(plan_query, (plan_id,)).fetchone()
    
    if not plan:
        st.error("Plan not found")
        return
    
    st.header(f"Plan: {plan['name']}")
    st.subheader(f"Major: {plan['major_name']}")
    
    # Get all semesters in the plan
    semesters_query = """
        SELECT s.id, s.term, s.year
        FROM Plan_Semesters ps
        JOIN Semesters s ON ps.semester_id = s.id
        WHERE ps.plan_id = ?
        ORDER BY s.year, CASE WHEN s.term = 'Fall' THEN 0 ELSE 1 END
    """
    semesters = con.execute(semesters_query, (plan_id,)).fetchall()
    
    # Initialize total credit count
    total_credits = 0
    
    # Create a container for the progress bar
    progress_container = st.container()
    with progress_container:
        st.write("Total Credits: Calculating...")
        progress_bar = st.progress(0)
    
    # Display each semester in an expander
    for semester in semesters:
        semester_id = semester['id']
        semester_name = f"{semester['term']} {semester['year']}"
        
        # Get courses for this semester
        courses_query = """
            SELECT c.subject, c.number, c.name, c.credits
            FROM Plan_Semester_Courses psc
            JOIN Courses c ON psc.course_subject = c.subject AND psc.course_number = c.number
            WHERE psc.plan_id = ? AND psc.semester_id = ?
        """
        courses = con.execute(courses_query, (plan_id, semester_id)).fetchall()
        
        # Calculate semester credit total
        semester_credits = sum(course['credits'] for course in courses)
        total_credits += semester_credits
        
        # Create an expander for this semester
        with st.expander(f"{semester_name} - {semester_credits} Credits"):
            if courses:
                # Convert to DataFrame for display
                df = pd.DataFrame([dict(c) for c in courses])
                # Add a course code column that combines subject and number
                df['Course'] = df['subject'] + ' ' + df['number'].astype(str)
                # Reorder and rename columns
                df = df[['Course', 'name', 'credits']]
                df.columns = ['Course', 'Course Name', 'Credits']
                
                # Display the courses table
                st.table(df)
                
                # Add a dropdown for actions (if needed)
                action = st.selectbox(
                    "Actions",
                    ["Select an action", "Edit Courses", "Remove Semester", "Add Course"],
                    key=f"action_{semester_id}"
                )
                
                if action == "Edit Courses":
                    st.write("Edit functionality would go here")
                elif action == "Remove Semester":
                    st.write("Remove functionality would go here")
                elif action == "Add Course":
                    st.write("Add course functionality would go here")
            else:
                st.write("No courses assigned to this semester yet.")
                st.button("Add Courses", key=f"add_{semester_id}")
    
    # Update the progress indicator
    # Assuming a typical degree requires 120 credits
    target_credits = 120
    progress_percentage = min(total_credits / target_credits, 1.0)
    
    with progress_container:
        st.write(f"Total Credits: {total_credits}/{target_credits}")
        progress_bar.progress(progress_percentage)
    
    # Display overall plan statistics
    st.subheader("Plan Summary")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Credits", total_credits)
    with col2:
        st.metric("Semesters", len(semesters))
    with col3:
        st.metric("Remaining Credits", max(0, target_credits - total_credits))
    
    con.close()
