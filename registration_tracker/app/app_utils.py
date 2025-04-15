import sqlite3
import streamlit as st
import pandas as pd
import controllers.plans as c_plans
import controllers.majors as c_majors
import controllers.courses as c_courses
import controllers.semesters as c_semesters

# Database Configuration (SQLite)
DB_NAME = "reg_tracker.db"

# Function to create a connection to SQLite
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Enables dictionary-like row access
    return conn

def display_plan(plan_id):
    st.title("Degree Plan")
    
    plan = c_plans.get_plan_from_id(plan_id)

    if not plan:
        st.error("Plan not found")
        return

    major = c_majors.get_major(plan['major_id'])
    
    st.header(f"Plan: {plan['name']}")
    st.subheader(f"Major: {major['name']}")
    
    # Get all semesters in the plan
    semesters = c_semesters.get_semesters(plan_id)
    
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
        courses = c_courses.get_semester_courses(semester['id'])
        
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
