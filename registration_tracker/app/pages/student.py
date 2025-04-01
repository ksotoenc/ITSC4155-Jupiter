import streamlit as st
import pandas as pd
# from app_utils import get_student, get_student_plan
import controllers.students as c_student
import controllers.advisors as c_advisor
import controllers.plans as c_plan
import controllers.semesters as c_semester
import controllers.courses as c_course

if "username" in st.session_state and st.session_state.username:
    username = st.session_state.username
    student = c_student.get_student("username", username)
    st.title("Student Information 📖")
    st.write(f"Welcome, {student['f_name']} {student['l_name']}!\n")

    if student:
        st.subheader("Student Profile")
        st.write(f"**Student ID:** {student['ID']}")
        st.write(f"**Username:** {student['Username']}")
        st.write(f"**Major:** {student['Major']}")
        st.write(f"**Graduation Date:** {student['Graduation_Date'] or 'Not set'}")
        st.write(f"**Advisor ID:** {student['advisor_id']}")

        col1, col2 = st.columns([1, 2])
        with col1:
            if st.button("View Plans"):
                st.switch_page("pages/plans.py")
        with col2:
            if st.button("Update Profile"):
                st.write("This feature is not yet implemented.")
            st.subheader("Academic Plan")
            
            # Get and display the student's plan
            plan = c_plan.get_first_plan(student['id'])
            
            if plan:
                st.write(f"**Plan Name:** {plan['name']}")
                st.write(f"**Advisor:** {c_advisor.get_advisor(plan['advisor_id'])['name']}")

                # Get all semesters associated with plan
                semesters = c_semester.get_semesters(plan['id'])
                
                # Calculate total credits
                total_credits = 0
                
                # Display each semester with its courses
                for semester in semesters:
                    semester_courses = c_course.get_semester_courses(semester['id'])
                    semester_credits = sum(course['credits'] for course in semester_courses)
                    total_credits += semester_credits
                    
                    with st.expander(f"{semester['term']} {semester['year']} ({semester_credits} credits)", expanded=True):
                        # Create a table for courses
                        course_data = []
                        for course in semester_courses:
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
