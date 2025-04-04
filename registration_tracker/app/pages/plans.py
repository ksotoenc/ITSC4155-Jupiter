import streamlit as st
from app_utils import *

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

    conn = get_db_connection()
    student = get_student(username)

    col1, col2 = st.columns([1, 2])
    with col1:
        # Toggle to create a new plan
        if st.button("Create New Plan"):
            st.session_state.viewing_plan = False 
            st.session_state.creating_plan = True  

        if st.session_state.get("creating_plan", False):  # Only show inputs if user clicked the button
            st.write("Let's create a new plan!")

            # Link text_input directly to session_state keys
            st.session_state.plan_name = st.text_input("Plan Name", value=st.session_state.plan_name)
            st.session_state.major = st.text_input("Major", placeholder="CS", value=st.session_state.major)
            st.session_state.start_term = st.text_input(
                "Starting term",
                placeholder="Type in format Semester Year (i.e. Fall 2026)",
                value=st.session_state.start_term
            )

            if st.button('Run'):
                if st.session_state.plan_name and st.session_state.major and st.session_state.start_term:
                    # Check if student already has plan with said name. If it does, return an error message.
                    existing_plan_query = "SELECT * FROM Plans WHERE name = ? AND student_id = ?"
                    existing_plan = conn.execute(existing_plan_query, (st.session_state.plan_name, student['ID'])).fetchone()
                    
                    if existing_plan:
                        st.error("A plan with this name already exists. Please choose a different name.")
                    else:
                        # Call the create_plan function
                        plan_created = create_plan(student['ID'], st.session_state.plan_name, st.session_state.major, st.session_state.start_term)
                        if plan_created:
                            st.success(f"Plan '{st.session_state.plan_name}' created successfully!")
                            plan = get_student_plan(student['ID'], st.session_state.plan_name)
                        else:
                            st.error("Failed to create the plan. Please try again.")
                else:
                    st.error("Please fill in all fields.")
    with col2:
        # Toggle to only view existing plans
        if st.button("View Existing Plans"):
            st.session_state.creating_plan = False
            st.session_state.viewing_plan = True

        if st.session_state.get("viewing_plan", False):
            selected_plan = st.selectbox("Select a plan to view", options=get_plan_names(student['ID']), placeholder='')  # Replace with actual plan names from the database
            if selected_plan != 'Select a plan...':
                plan = get_student_plan(student['ID'], selected_plan)
                display_plan(plan)
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
