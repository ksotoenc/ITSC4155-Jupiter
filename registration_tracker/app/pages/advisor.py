import streamlit as st
import pandas as pd
import controllers.students as c_student
import controllers.advisors as c_advisor
import controllers.plans as c_plan
import controllers.semesters as c_semester
import controllers.courses as c_course

if "username" in st.session_state and st.session_state.username:
    st.title("Advisor Dashboard")
    username = st.session_state.username
    st.write(f"Welcome, {username}!\n")
    students = c_student.get_all_students()
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
                st.write(f"**Plan Name:** {plan['name']}")
                st.write(f"**Advisor:** {c_advisor.get_advisor(plan['advisor_id'])['f_name']} {c_advisor.get_advisor(plan['advisor_id'])['l_name']}")

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

        with tab2:
            st.text_area("Leave feedback for the student", height=150)
            if st.button("Submit Feedback"):
                st.success("Feedback submitted!")

else:
    st.write("Please log in to view this page.")
    if st.button("Go to Login"):
        st.switch_page("home.py")
