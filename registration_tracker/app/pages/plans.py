import streamlit as st
import controllers.students as c_student
import controllers.majors as c_major
import controllers.advisors as c_advisor
import controllers.plans as c_plan
import controllers.semesters as c_semester
import controllers.courses as c_course
from app_utils import display_plan

# If user is logged in, show the plans page
if "username" in st.session_state and st.session_state.username:
    st.title("Graduation Plans")
    username = st.session_state.username
    st.write(f"Welcome, {username}!\n")

    # Initialize session state variables only if they don't exist
    if "plan_name" not in st.session_state:
        st.session_state.plan_name = ""
    if "major" not in st.session_state:
        st.session_state.major = ""
    if "start_term" not in st.session_state:
        st.session_state.start_term = ""

    student = c_student.get_student("username", username)

    tab1, tab2 = st.tabs(["Create New Plan", "View Existing Plans"])
    with tab1:
        st.write("Let's create a new plan!")
        st.session_state.plan_name = st.text_input("Plan Name", value=st.session_state.plan_name)
        majors = c_major.get_all_majors()
        major_options = [major['name'] for major in majors]
        # Link text_input directly to session_state keys
        selected_major = st.selectbox(
            "Select Major", 
            options=major_options,
        )
        major_id = c_major.get_major_id(selected_major)
        st.session_state.major = selected_major
        # Term selection with dropdowns
        term_col, year_col = st.columns(2)
        with term_col:
            term = st.selectbox("Starting Term", options=["Fall", "Spring"])
        with year_col:
            current_year = 2025  # Adjust as needed
            year = st.selectbox("Starting Year", options=range(current_year, current_year + 3))
        st.session_state.start_term = f"{term} {year}"

        if st.button('Run'):
            if st.session_state.plan_name and st.session_state.major and st.session_state.start_term:
                # Check if student already has plan with said name. If it does, return an error message.
                existing_plan = c_plan.get_plan(st.session_state.plan_name, "student", student['ID'])
                if existing_plan:
                    st.error("A plan with this name already exists. Please choose a different name.")
                else:
                    # Call the create_plan function
                    plan_created = c_plan.create_plan(student['ID'],  student['advisor_ID'], st.session_state.plan_name, major_id, st.session_state.start_term)
                    if plan_created:
                        st.success(f"Plan '{st.session_state.plan_name}' created successfully!")
                        plan = c_plan.get_plan(st.session_state.plan_name, "student", student['ID'],)
                    else:
                        st.error("Failed to create the plan. Please try again.")
            else:
                st.error(f"Please fill in all fields.")
    with tab2:
        plans = c_plan.get_plans("student", student['ID'])
        plan_names = [plan['name'] for plan in plans]
        plan_names.insert(0, 'Select a plan...')
        selected_plan = st.selectbox("Select a plan to view", options=plan_names, placeholder='')  # Replace with actual plan names from the database
        if selected_plan != 'Select a plan...':
            plan = c_plan.get_plan(selected_plan, "student", student['ID'])
            display_plan(plan['id'])
else:
    st.write("Please log in to view this page.")
    # Close the database connection
    if st.button("Go to Login"):
        st.session_state.viewing_plan = False
        st.session_state.creating_plan = False
        st.session_state.plan_name = ""
        st.session_state.major = ""
        st.session_state.start_term = ""
        st.session_state.username = None
        st.session_state.password = None
        st.switch_page("home.py")
