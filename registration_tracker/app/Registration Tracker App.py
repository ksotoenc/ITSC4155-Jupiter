import streamlit as st
import sqlite3
import pandas as pd

# Database Configuration (SQLite)
DB_NAME = "registration_tracker.db"

# Function to create a connection to SQLite
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Enables dictionary-like row access
    return conn

# Streamlit App Configuration
st.set_page_config(page_title="Registration Tracker", page_icon="📚", layout="wide")

# Navigation Sidebar 
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["Home", "Student", "Advisor"])

# Replace with function to get sample student data from SQLite
@st.cache_resource
def get_student():
    query = "SELECT ID, Username, Major, Graduation_Date, advisor_id FROM Student LIMIT 1"
    conn = get_db_connection()
    student = conn.execute(query).fetchone()
    conn.close()
    return student

# Home Page
if page == "Home":
    st.title("Welcome to the Registration Tracker! 🎓")
    st.write("This application helps students and advisors track and manage registration plans.")

# Student Page(Hopefully will display student data from database for now)
elif page == "Student":
    st.title("Student Information 📖")
    
    student = get_student()
    
    if student:
        st.write(f"**Student ID:** {student['ID']}")
        st.write(f"**Username:** {student['Username']}")
        st.write(f"**Major:** {student['Major']}")
        st.write(f"**Graduation Date:** {student['Graduation_Date']}")
        st.write(f"**Advisor ID:** {student['advisor_id']}")
    else:
        st.warning("No student data found.")

# Advisor Page(BLANK FOR NOW)
elif page == "Advisor":
    st.title("Advisor Dashboard 🏫")
    st.write("Here, advisors can manage and review student plans.")

# Sidebar Footer
st.sidebar.text("Built with ❤️ using Streamlit")
