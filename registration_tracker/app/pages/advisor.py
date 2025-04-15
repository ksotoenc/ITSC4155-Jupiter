import streamlit as st
import pandas as pd
import controllers.students as c_student
import controllers.advisors as c_advisor
import controllers.plans as c_plan
import controllers.semesters as c_semester
import controllers.courses as c_course
from app_utils import display_plan

if "username" in st.session_state and st.session_state.username:
    st.title("Advisor Dashboard")
    username = st.session_state.username
    st.write(f"Welcome, {username}!\n")
    adv_id = c_advisor.get_advisor_user(st.session_state.username)['id']
    students = c_student.get_students(adv_id)
    student_names = [f"{s['f_name']} {s['l_name']}" for s in students]
    selected_student = st.selectbox("Select a student", student_names)

    # Find selected student data
    student = next((s for s in students if f"{s['f_name']} {s['l_name']}" == selected_student), None)

    if student:
        st.markdown(f"### 📘 Student Profile: {student['f_name']} {student['l_name']}")
        st.write(f"**Student ID:** {student['ID']}")
        st.write(f"**Username:** {student['Username']}")
        st.write(f"**Major:** {student['major_id']}")
        st.write(f"**Graduation Date:** {student['Graduation_Date'] or 'Not set'}")

        tab1, tab2 = st.tabs(["📑 View Plan", "📝 Feedback"])

        with tab1:
            plan = c_plan.get_first_plan(student['id'])
            if plan:
                display_plan(plan['id'])
        with tab2:
            st.text_area("Leave feedback for the student", height=150)
            if st.button("Submit Feedback"):
                st.success("Feedback submitted!")

else:
    st.write("Please log in to view this page.")
    if st.button("Go to Login"):
        st.switch_page("home.py")
