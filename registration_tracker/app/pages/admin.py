import streamlit as st
import pandas as pd

# Import controller functions
from controllers.students import add_student, update_student, delete_student
from controllers.advisors import add_advisor, update_advisor, delete_advisor
from controllers.courses import add_course, update_course, delete_course
from controllers.semesters import add_semester, update_semester, delete_semester
from controllers.plans import update_plan, delete_plan
from controllers.prerequisites import add_prereq, update_prereq, delete_prereq
from controllers.majors import add_major, update_major, delete_major

# Dictionary to store form configurations for each controller
CONTROLLER_CONFIGS = {
    "Students": {
        "Add": {
            "functions": add_student,
            "fields": [
                {"name": "id", "label": "Student ID", "optional": False},
                {"name": "f_name", "label": "First Name", "optional": False},
                {"name": "l_name", "label": "Last Name", "optional": False},
                {"name": "username", "label": "Username", "optional": False},
                {"name": "password", "label": "Password", "optional": False, "password": True},
                {"name": "major_id", "label": "Major", "optional": False},
                {"name": "graduation_date", "label": "Graduation Date (YYYYMMDD)", "optional": False},
                {"name": "advisor_id", "label": "Advisor ID", "optional": False}
            ]
        },
        "Update": {
            "functions": update_student,
            "fields": [
                {"name": "student_id", "label": "Student ID", "optional": False},
                {"name": "f_name", "label": "First Name", "optional": True},
                {"name": "l_name", "label": "Last Name", "optional": True},
                {"name": "username", "label": "Username", "optional": True},
                {"name": "password", "label": "Password", "optional": True, "password": True},
                {"name": "major_id", "label": "Major", "optional": True},
                {"name": "graduation_date", "label": "Graduation Date", "optional": True},
                {"name": "advisor_id", "label": "Advisor ID", "optional": True}
            ]
        },
        "Delete": {
            "functions": delete_student,
            "fields": [
                {"name": "student_id", "label": "Student ID", "optional": False}
            ]
        }
    },
    "Advisors": {
        "Add": {
            "functions": add_advisor,
            "fields": [
                {"name": "id", "label": "Advisor ID", "optional": False},
                {"name": "username", "label": "Username", "optional": False},
                {"name": "password", "label": "Password", "optional": False, "password": True},
                {"name": "f_name", "label": "First Name", "optional": False},
                {"name": "l_name", "label": "Last Name", "optional": False}
            ]
        },
        "Update": {
            "functions": update_advisor,
            "fields": [
                {"name": "id", "label": "Advisor ID", "optional": False},
                {"name": "username", "label": "Username", "optional": True},
                {"name": "password", "label": "Password", "optional": True, "password": True},
                {"name": "f_name", "label": "First Name", "optional": True},
                {"name": "l_name", "label": "Last Name", "optional": True}
            ]
        },
        "Delete": {
            "functions": delete_advisor,
            "fields": [
                {"name": "id", "label": "Advisor ID", "optional": False}
            ]
        }
    },
    "Courses": {
        "Add": {
            "functions": add_course,
            "fields": [
                {"name": "subject", "label": "Course Subject", "optional": False},
                {"name": "number", "label": "Course Number", "optional": False},
                {"name": "name", "label": "Course Name", "optional": False},
                {"name": "credits", "label": "Credits", "optional": False}
            ]
        },
        "Update": {
            "functions": update_course,
            "fields": [
                {"name": "subject", "label": "Course Subject", "optional": False},
                {"name": "number", "label": "Course Number", "optional": False},
                {"name": "name", "label": "Course Name", "optional": True},
                {"name": "credits", "label": "Credits", "optional": True}
            ]
        },
        "Delete": {
            "functions": delete_course,
            "fields": [
                {"name": "subject", "label": "Course Subject", "optional": False},
                {"name": "number", "label": "Course Number", "optional": False}
            ]
        }
    },
    "Semesters": {
        "Add": {
            "functions": add_semester,
            "fields": [
                {"name": "term", "label": "Term (e.g., Spring, Summer, Fall)", "optional": False},
                {"name": "year", "label": "Year", "optional": False}
            ]
        },
        "Update": {
            "functions": update_semester,
            "fields": [
                {"name": "id", "label": "Semester ID", "optional": False},
                {"name": "term", "label": "Term", "optional": True},
                {"name": "year", "label": "Year", "optional": True}
            ]
        },
        "Delete": {
            "functions": delete_semester,
            "fields": [
                {"name": "id", "label": "Semester ID", "optional": False}
            ]
        }
    },
    "Plans": {
        "Update": {
            "functions": update_plan,
            "fields": [
                {"name": "plan_id", "label": "Plan ID", "optional": False},
                {"name": "name", "label": "Plan Name", "optional": True},
                {"name": "num_semesters", "label": "Number of Semesters", "optional": True},
                {"name": "student_id", "label": "Student ID", "optional": True},
                {"name": "advisor_id", "label": "Advisor ID", "optional": True}
            ]
        },
        "Delete": {
            "functions": delete_plan,
            "fields": [
                {"name": "plan_id", "label": "Plan ID", "optional": False}
            ]
        }
    },
    "Prerequisites": {
        "Add": {
            "functions": add_prereq,
            "fields": [
                {"name": "parent_subject", "label": "Parent Course Subject", "optional": False},
                {"name": "parent_number", "label": "Parent Course Number", "optional": False},
                {"name": "group_id", "label": "Group ID", "optional": False},
                {"name": "course_subject", "label": "Prerequisite Course Subject", "optional": False},
                {"name": "course_number", "label": "Prerequisite Course Number", "optional": False}
            ]
        },
        "Update": {
            "functions": update_prereq,
            "fields": [
                {"name": "parent_subject", "label": "Parent Course Subject", "optional": False},
                {"name": "parent_number", "label": "Parent Course Number", "optional": False},
                {"name": "group_id", "label": "Group ID", "optional": False},
                {"name": "course_subject", "label": "Prerequisite Course Subject", "optional": True},
                {"name": "course_number", "label": "Prerequisite Course Number", "optional": True}
            ]
        },
        "Delete": {
            "functions": delete_prereq,
            "fields": [
                {"name": "parent_subject", "label": "Parent Course Subject", "optional": False},
                {"name": "parent_number", "label": "Parent Course Number", "optional": False},
                {"name": "group_id", "label": "Group ID", "optional": False}
            ]
        }
    },
    "Majors": {
        "Add": {
            "functions": add_major,
            "fields": [
                {"name": "name", "label": "Major Name", "optional": False},
                {"name": "department", "label": "Department", "optional": False}
            ]
        },
        "Update": {
            "functions": update_major,
            "fields": [
                {"name": "major_id", "label": "Major ID", "optional": False},
                {"name": "name", "label": "Major Name", "optional": True},
                {"name": "department", "label": "Department", "optional": True}
            ]
        },
        "Delete": {
            "functions": delete_major,
            "fields": [
                {"name": "major_id", "label": "Major ID", "optional": False}
            ]
        }
    }
}

# Streamlit app
st.title("Admin Panel")
st.write("Use this panel to manage database entries.")

# Select a controller
controller = st.selectbox(
    "Select a table to manage:",
    list(CONTROLLER_CONFIGS.keys())
)

# Add tabs for different operations
tab_manage, tab_view = st.tabs(["Manage Records", "View Table"])

with tab_manage:
    # Determine available actions for selected controller
    available_actions = list(CONTROLLER_CONFIGS[controller].keys())
    action = st.radio("Select an action:", available_actions)
    
    # Display form based on selected controller and action
    st.subheader(f"{action} a {controller[:-1]}")

    # Get the configuration for the selected controller and action
    config = CONTROLLER_CONFIGS[controller][action]
    form_data = {}

    # Create input fields based on configuration
    for field in config["fields"]:
        optional_text = " (optional)" if field.get("optional", False) else ""
        if field.get("password", False):
            form_data[field["name"]] = st.text_input(f"{field['label']}{optional_text}", type="password")
        else:
            form_data[field["name"]] = st.text_input(f"{field['label']}{optional_text}")

    # Create button with appropriate label
    button_label = f"{action} {controller[:-1]}"
    if st.button(button_label):
        # Call the appropriate function with form data
        result = config["functions"](**form_data)
        if result["success"]:
            st.success(result["message"])
        else:
            st.error(result["message"])

# Add view functionality in the View tab
with tab_view:
    st.subheader(f"View {controller} Table")
    
    if st.button(f"Refresh {controller} Data"):
        # Import necessary functions based on controller
        if controller == "Students":
            from controllers.students import get_all_students
            data = get_all_students()
            if data:
                students = pd.DataFrame(data, columns=data[0].keys())
                st.dataframe(students)
            else:
                st.info("No students found in the database.")        
        elif controller == "Advisors":
            from controllers.advisors import get_all_advisors
            data = get_all_advisors()
            if data:
                advisors = pd.DataFrame(data, columns=data[0].keys())
                st.dataframe(advisors)
            else:
                st.info("No advisors found in the database.")  
        elif controller == "Courses":
            from controllers.courses import get_all_courses
            data = get_all_courses()
            if data:
                courses = pd.DataFrame(data, columns=data[0].keys())
                st.dataframe(courses)
            else:
                st.info("No courses found in the database.")  
        elif controller == "Semesters":
            from controllers.semesters import get_all_semesters
            data = get_all_semesters()
            if data:
                semesters = pd.DataFrame(data, columns=data[0].keys())
                st.dataframe(semesters)
            else:
                st.info("No semesters found in the database.")  
        elif controller == "Plans":
            from controllers.plans import get_all_plans
            data = get_all_plans()
            if data:
                plans = pd.DataFrame(data, columns=data[0].keys())
                st.dataframe(plans)
            else:
                st.info("No plans found in the database.")  
        elif controller == "Prerequisites":
            from controllers.prerequisites import get_all_prereqs
            data = get_all_prereqs()
            if data:
                prerequisites = pd.DataFrame(data, columns=data[0].keys())
                st.dataframe(prerequisites)
            else:
                st.info("No prerequisites found in the database.")
        elif controller == "Majors":
            from controllers.majors import get_all_majors
            data = get_all_majors()
            if data:
                majors = pd.DataFrame(data, columns=data[0].keys())
                st.dataframe(majors)
            else:
                st.info("No majors found in the database.")
