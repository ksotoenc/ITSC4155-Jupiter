import streamlit as st
# import streamlit_authenticator as stauth
from controllers.students import get_all_students
from controllers.advisors import get_all_advisors
from controllers.admins import get_all_admins

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
admin_usernames = []
admin_passwords = []
admins = get_all_admins()
for row in admins:
    admin_usernames.append(row['username'])
    admin_passwords.append(row['password'])

# Initialize session stae with current user
if "username" not in st.session_state:
    st.session_state.username = ""

# Streamlit App Configuration
st.set_page_config(page_title="Registration Tracker", page_icon="📚", layout="wide", initial_sidebar_state='collapsed')

st.title("Welcome to the Registration Tracker! 🎓")
st.write("""
Welcome to the **Registration Tracker**! 

This application is designed to help students and advisors seamlessly plan, track, and manage academic registration plans. Whether you are mapping out your path to graduation or helping students stay on track, this tool offers the flexibility and insights you need. 

Please log in below to access your personalized dashboard.
""")

# Login Form
username = st.text_input("Username")
st.session_state.username = username
password = st.text_input("Password", type="password")

if st.button("Login"):
    username_index = -1
    user_defined = False
    try:
        username_index = s_usernames.index(username)
    except ValueError:
        pass
    if username_index != -1:    # if username is in student username list
        user_defined = True
        if s_passwords[username_index] == password:
            st.switch_page("pages/student.py")
        else:
            st.error("Role selected and/or credentials do not match. Please try again.")
    else:   # check username in advisor username list
        try:
            username_index = a_usernames.index(username)
        except ValueError:
            pass

    if not user_defined and username_index != -1:   # if username is in advisor username list
        user_defined = True
        if a_passwords[username_index] == password:
            st.switch_page("pages/advisor.py")
        else:
            st.error("Role selected and/or credentials do not match. Please try again.")
    else:   # check username in admin username list
        try:
            username_index = admin_usernames.index(username)
        except ValueError:
            pass

    if not user_defined and username_index != -1:   # if username is in admin username list
        user_defined = True     # line not needed but here for symmetry
        if admin_passwords[username_index] == password:
            st.switch_page("pages/admin.py")
        else:
            st.error("Role selected and/or credentials do not match. Please try again.")

st.markdown("""
    <hr>
    <p style='text-align: center;'>Developed by Team Jupiter - Contact us at <a href='mailto:support@registrationtracker.com'>support@registrationtracker.com</a></p>
""", unsafe_allow_html=True)
