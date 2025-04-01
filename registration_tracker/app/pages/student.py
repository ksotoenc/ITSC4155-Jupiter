import streamlit as st
import pandas as pd
from app_utils import *

if "username" in st.session_state and st.session_state.username:
    st.title("Student Information 📖")
    username = st.session_state.username
    st.write(f"Welcome, {username}!\n")
    student = get_student(username)

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
else:
    st.write("Please log in to view this page.")
    if st.button("Go to Login"):
        st.switch_page("home.py")
