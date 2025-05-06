import streamlit as st
import pandas as pd
import controllers.students as c_student
import controllers.advisors as c_advisor
import controllers.majors as c_major
import controllers.plans as c_plan
import controllers.semesters as c_semester
import controllers.courses as c_course
from auth_utils import protect_page

# Hide the default page navigation
hide_streamlit_style = """
<style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    .css-18e3th9 {padding-top: 0;}
    /* Hide default sidebar menu items based on navigation sections */
    [data-testid="stSidebarNav"] {
        display: none;
    }
    /* Or to hide specific elements instead of all navigation */
    section[data-testid="stSidebar"] > div.css-1d391kg {
        padding-top: 2rem;
    }
    /* Ensure custom sidebar elements are visible */
    .custom-sidebar {
        display: block !important;
    }
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Role-based protection
protect_page("student")  # Replace with appropriate role

# Sidebar navigation based on user role
with st.sidebar:
    st.markdown('<div class="custom-sidebar">', unsafe_allow_html=True)
    st.title("Navigation")
 
    if st.session_state.user_role == "student":
        if st.button("Student Dashboard"):
            st.switch_page("pages/student.py")
        if st.button("Graduation Plans"):
            st.switch_page("pages/plans.py")
    elif st.session_state.user_role == "advisor":
        if st.button("Advisor Dashboard"):
            st.switch_page("pages/advisor.py")
    elif st.session_state.user_role == "admin":
        if st.button("Admin Dashboard"):
            st.switch_page("pages/admin.py")
    # Add logout button
    if st.button("Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.switch_page("home.py")
    
    st.markdown('</div>', unsafe_allow_html=True)

# If we got past the protection, the user is a student and logged in
username = st.session_state.username
student = c_student.get_student("username", username)
st.title("Student Dashboard")
st.write(f"Welcome, {student['f_name']} {student['l_name']}!\n")

if student:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Student Profile")
        st.write(f"**Student ID:** {student['ID']}")
        st.write(f"**Username:** {student['Username']}")
        major = c_major.get_major(student['major_id'])
        st.write(f"**Major:** {major['name']}")
        st.write(f"**Graduation Date:** {student['Graduation_Date'] or 'Not set'}")
        st.write(f"**Advisor ID:** {student['advisor_id']}")

    with col2:
        # Get and display the student's plan
        st.write("Default Academic Plan")
        plan = c_plan.get_first_plan(student['id'])
        
        if plan:
            st.write(f"**Plan Name:** {plan['name']}")
            st.write(f"**Advisor:** {c_advisor.get_advisor(plan['advisor_id'])['f_name']} {c_advisor.get_advisor(plan['advisor_id'])['l_name']}")

            # Get all semesters associated with plan
            semesters = c_semester.get_semesters(plan['id'])
            
            # Calculate total credits
            total_credits = 0
            
            # Display each semester with its courses
            for semester in semesters:
                semester_courses = c_course.get_semester_courses(semester['id'], plan['id'])
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
