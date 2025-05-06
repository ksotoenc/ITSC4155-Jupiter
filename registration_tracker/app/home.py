import streamlit as st
from controllers.students import get_all_students
from controllers.advisors import get_all_advisors
from controllers.admins import get_all_admins

# Fetch all users from the database
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

# Initialize session state variables
if "username" not in st.session_state:
    st.session_state.username = ""
    
# Add user_role to session state to track the user's role
if "user_role" not in st.session_state:
    st.session_state.user_role = ""

# Streamlit App Configuration
st.set_page_config(page_title="Registration Tracker", page_icon="📚", layout="wide", initial_sidebar_state='collapsed')

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

st.title("Welcome to the Registration Tracker! 🎓")
st.write("""
Welcome to the **Registration Tracker**! 

This application is designed to help students and advisors seamlessly plan, track, and manage academic registration plans. Whether you are mapping out your path to graduation or helping students stay on track, this tool offers the flexibility and insights you need. 

Please log in below to access your personalized dashboard.
""")

# Only show login form if user is not already logged in
if not st.session_state.username or not st.session_state.user_role:
    # Login Form
    username = st.text_input("Username")
    st.session_state.username = username  # Update session state
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        username_index = -1
        user_defined = False
        
        # Check if username is in student list
        try:
            username_index = s_usernames.index(username)
        except ValueError:
            pass
            
        if username_index != -1:  # if username is in student username list
            user_defined = True
            if s_passwords[username_index] == password:
                st.session_state.user_role = "student"  # Set the user role in session state
                st.switch_page("pages/student.py")
            else:
                st.error("Credentials do not match. Please try again.")
        
        else:  # check username in advisor username list
            try:
                username_index = a_usernames.index(username)
            except ValueError:
                pass

        if not user_defined and username_index != -1:  # if username is in advisor username list
            user_defined = True
            if a_passwords[username_index] == password:
                st.session_state.user_role = "advisor"  # Set the user role in session state
                st.switch_page("pages/advisor.py")
            else:
                st.error("Credentials do not match. Please try again.")
        
        else:  # check username in admin username list
            try:
                username_index = admin_usernames.index(username)
            except ValueError:
                pass

        if not user_defined and username_index != -1:  # if username is in admin username list
            if admin_passwords[username_index] == password:
                st.session_state.user_role = "admin"  # Set the user role in session state
                st.switch_page("pages/admin.py")
            else:
                st.error("Credentials do not match. Please try again.")
        
        # If we get here and user is still not defined, username doesn't exist
        if not user_defined and username:
            st.error("Username not found. Please try again.")

st.markdown("""
    <hr>
    <p style='text-align: center;'>Developed by Team Jupiter - Contact us at <a href='mailto:support@registrationtracker.com'>support@registrationtracker.com</a></p>
""", unsafe_allow_html=True)