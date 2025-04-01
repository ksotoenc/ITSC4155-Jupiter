import streamlit as st
# import streamlit_authenticator as stauth
from controllers.students import get_all_students
from controllers.advisors import get_all_advisors

s_usernames = []
s_passwords = []
students = get_all_students()
for row in students:
    s_usernames.append(row['username'])
    s_passwords.append(row['password'])
a_usernames = []
a_passwords = []
advisors = get_all_advisors()
for row in advisors:
    a_usernames.append(row['username'])
    a_passwords.append(row['password'])

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
        username_index = -1
        try:
            username_index = s_usernames.index(username)
        except ValueError:
            pass
        if username_index != -1 and s_passwords[username_index] == password:
            st.switch_page("pages/student.py")
        else:
            st.error("Role selected and/or credentials do not match. Please try again.")
    elif role == "Advisor":
        username_index = -1
        try:
            username_index = a_usernames.index(username)
        except ValueError:
            pass
        if username_index != -1 and a_passwords[username_index] == password:
            st.switch_page("pages/advisor.py")
        else:
            st.error("Role selected and/or credentials do not match. Please try again.")
    else:
        st.error("Role selected and/or credentials do not match. Please try again.")

