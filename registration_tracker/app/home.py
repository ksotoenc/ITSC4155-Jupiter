import streamlit as st

# Initialize session stae with current user
if "username" not in st.session_state:
    st.session_state.username = ""

# Streamlit App Configuration
st.set_page_config(page_title="Registration Tracker", page_icon="📚", layout="wide", initial_sidebar_state='collapsed')

st.title("Welcome to the Registration Tracker! 🎓")
st.write("This application helps students and advisors track and manage registration plans. Please log in below")

# Login Form
role = st.radio("Select your role", ["Student", "Advisor"])
username = st.text_input("Username")
st.session_state.username = username
password = st.text_input("Password", type="password")

if st.button("Login"):
    if role == "Student":
        st.switch_page("pages/student.py")
    elif role == "Advisor":
        st.switch_page("pages/advisor.py")
    else:
        st.error("Role selected and/or credentials do not match. Please try again.")

