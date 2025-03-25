import streamlit as st
import pandas as pd
from app_utils import get_student, get_student_plan

if "username" in st.session_state and st.session_state.username:
    st.title("Student Information 📖")
    username = st.session_state.username
    st.write(f"Welcome, {username}!\n")
    student = get_student()

    if student:
        # Create two columns for layout
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("Student Profile")
            st.write(f"**Student ID:*   * {student['ID']}")
            st.write(f"**Username:** {student['Username']}")
            st.write(f"**Major:** {student['Major']}")
            st.write(f"**Graduation Date:** {student['Graduation_Date'] or 'Not set'}")
            st.write(f"**Advisor ID:** {student['advisor_id']}")
        
        with col2:
            st.subheader("Academic Plan")
            
            # Get and display the student's plan
            plan = get_student_plan(student['ID'])
            
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
                st.warning(f"No academic plan found for student {student['ID']}.")
    else:
        st.warning("No student data found.")
else:
    st.write("Please log in to view this page.")
    if st.button("Go to Login"):
        st.switch_page("home.py")