import streamlit as st
import pandas as pd
import controllers.students as c_student
import controllers.advisors as c_advisor
import controllers.plans as c_plan
import controllers.semesters as c_semester
import controllers.courses as c_course

st.title("Advisor Dashboard 🏫")
st.write("Here, advisors can manage and review student plans.")

option = st.selectbox("Select a student",("Student 1", "Student 2", "Student 3"))

st.header("Student: {Name}")
st.header("Expected Graduation Date{Date}")
st.header("Major {Major}")
st.header("GPA {GPA}")

st.button("View Current Plan")
st.button("View Feedback")
