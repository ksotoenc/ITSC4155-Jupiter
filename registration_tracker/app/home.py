import streamlit as st

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

st.markdown("""
    <hr>
    <p style='text-align: center;'>Developed by Team Jupiter - Contact us at <a href='mailto:support@registrationtracker.com'>support@registrationtracker.com</a></p>
""", unsafe_allow_html=True)
