import streamlit as st
import pandas as pd
from app_utils import get_student, get_student_plan

st.title("Advisor Dashboard 🏫")
st.write("Here, advisors can manage and review student plans.")

option = st.selectbox("Select a student",("Student 1", "Student 2", "Student 3"))

st.header("Student: {Name}")
st.header("Expected Graduation Date{Date}")
st.header("Major {Major}")
st.header("GPA {GPA}")

st.button("View Current Plan")
st.button("View Feedback")
