import streamlit as st
import controllers.students as c_student
import controllers.majors as c_major
import controllers.concentration as c_concentration
import controllers.advisors as c_advisor
import controllers.plans as c_plan
import controllers.semesters as c_semester
import controllers.courses as c_course
#from app_utils import display_plan, get_available_courses, add_course_to_semester, get_db_connection, remove_from_semester, dis
from app_utils import *

# If student is logged in, show the plans page
if "username" in st.session_state and st.session_state.username:
    st.title("Graduation Plans")
    username = st.session_state.username
    st.write(f"Welcome, {username}!\n")

    # Initialize session state variables
    for key in ["plan_name", "major", "start_term", "current_plan_id", "editing_plan"]:
        if key not in st.session_state:
            st.session_state[key] = "" if key != "editing_plan" else False

    student = c_student.get_student("username", username)

    # Create tabs for different functionalities
    tab1, tab2, tab3, tab4 = st.tabs(["Create New Plan", "View Existing Plans", "Edit Plan", "Review Suggestions"])
    
    with tab1:
        st.write("Let's create a new plan!")
        st.session_state.plan_name = st.text_input("Plan Name", value=st.session_state.plan_name)
        
        majors = c_major.get_all_majors()
        major_options = [major['name'] for major in majors]
        selected_major = st.selectbox("Select Major", options=major_options)
        major_id = c_major.get_major_id(selected_major)
        st.session_state.major = selected_major

        # Handle concentration selection
        concentrations = c_concentration.get_concentrations_by_major(major_id)
        if concentrations:
            concentration_options = [concentration['name'] for concentration in concentrations]
            selected_concentration = st.selectbox("Select Concentration", options=concentration_options)
            concentration_id = c_concentration.get_concentration_id(selected_concentration)
            st.session_state.concentration = selected_concentration
        else:
            st.session_state.concentration = None
            concentration_id = None
      
        # Term selection with dropdowns
        term_col, year_col = st.columns(2)
        with term_col:
            term = st.selectbox("Starting Term", options=["Fall", "Spring"])
        with year_col:
            current_year = 2025
            year = st.selectbox("Starting Year", options=range(current_year, current_year + 3))
        st.session_state.start_term = f"{term} {year}"

        # Number of semesters
        num_semesters = st.slider("Number of Semesters", min_value=1, max_value=12, value=8)

        if st.button('Create Plan'):
            if st.session_state.plan_name and st.session_state.major and st.session_state.start_term:
                # Check if student already has plan with said name
                existing_plan = c_plan.get_plan(st.session_state.plan_name, "student", student['ID'])
                if existing_plan:
                    st.error("A plan with this name already exists. Please choose a different name.")
                else:
                    plan_created = c_plan.create_plan(student['ID'], student['advisor_ID'], st.session_state.plan_name, major_id, concentration_id, st.session_state.start_term)
                    if plan_created:
                        st.success(f"Plan '{st.session_state.plan_name}' created successfully!")
                        plan = c_plan.get_plan(st.session_state.plan_name, "student", student['ID'])
                        
                        # Generate semesters automatically
                        if plan:
                            start_term, start_year = st.session_state.start_term.split()
                            start_year = int(start_year)
                            current_term, current_year = start_term, start_year
                            
                            for i in range(num_semesters):
                                # Create semester and link to plan
                                c_semester.add_semester(current_term, current_year)
                                semester = c_semester.get_semester(current_term, current_year)
                                c_semester.insert_to_plan(plan['id'], semester['id'])
                                
                                # Advance to next term
                                if current_term == "Fall":
                                    current_term = "Spring"
                                    current_year += 1
                                else:
                                    current_term = "Fall"
                            
                            # Set this as the current plan for editing
                            st.session_state.current_plan_id = plan['id']
                            st.session_state.editing_plan = True
                            st.rerun()
                    else:
                        st.error("Failed to create the plan. Please try again.")
            else:
                st.error(f"Please fill in all fields.")
                
    with tab2:
        plans = c_plan.get_plans("student", student['ID'])
        
        if not plans:
            st.info("You don't have any plans yet. Create one in the 'Create New Plan' tab.")
        else:
            plan_names = [plan['name'] for plan in plans]
            plan_names.insert(0, 'Select a plan...')
            selected_plan = st.selectbox("Select a plan to view", options=plan_names, index=0)
            
            if selected_plan != 'Select a plan...':
                plan = c_plan.get_plan(selected_plan, "student", student['ID'])
                # Display the plan details
                display_plan(plan['id'])
    
    with tab3:
        plans = c_plan.get_plans("student", student['ID'])
        
        if not plans:
            st.info("You don't have any plans yet. Create one in the 'Create New Plan' tab.")
        else:
            plan_names = [plan['name'] for plan in plans]
            plan_names.insert(0, 'Select a plan...')
            selected_plan = st.selectbox("Select a plan to edit", options=plan_names, index=0)
            
            if selected_plan != 'Select a plan...':
                plan = c_plan.get_plan(selected_plan, "student", student['ID'])
                st.subheader(f"Editing Plan: {plan['name']}")
                
                # Get plan details
                major = c_major.get_major(plan['major_id'])
                st.write(f"Major: {major['name']}")
                
                if plan['concentration_id']:
                    concentration = c_concentration.get_concentration(plan['concentration_id'])
                    st.write(f"Concentration: {concentration['name']}")
                
                # Get semesters in the plan
                semesters = c_semester.get_semesters(plan['id'])
                
                if not semesters:
                    st.warning("No semesters in this plan. You may need to recreate the plan.")
                else:
                    # For each semester, allow adding courses
                    for semester in semesters:
                        semester_id = semester['id']
                        semester_name = f"{semester['term']} {semester['year']}"
                        
                        with st.expander(f"Edit {semester_name}"):
                            # Display current courses in this semester
                            courses = c_course.get_semester_courses(semester_id, plan['id'])
                            if courses:
                                st.write("Current Courses:")
                                for course in courses:
                                    col1, col2 = st.columns([5, 1])
                                    with col1:
                                        st.write(f"• {course['subject']} {course['number']} - {course['name']} ({course['credits']} credits)")
                                    with col2:
                                        # Add remove button for each course
                                        if st.button("Remove", key=f"remove_{semester_id}_{course['subject']}_{course['number']}"):
                                            # Remove the course from the semester
                                            remove_from_semester(plan['id'], semester_id, course['subject'], course['number'])
                                            st.success(f"Removed {course['subject']} {course['number']} from {semester_name}")
                                            st.rerun()
                            else:
                                st.write("No courses in this semester yet.")
                            
                            # Add new courses section
                            st.subheader("Add Courses")
                            
                            # Get all available courses for this semester
                            all_available = get_available_courses(plan['id'], semester_id, plan['major_id'])
                            
                            # Create dictionaries to store section information
                            major_sections_info = {}
                            concentration_sections_info = {}
                            gen_ed_sections_info = {}
                            
                            # Initialize dictionaries to hold courses by section
                            major_courses = {}
                            concentration_courses = {}
                            gen_ed_courses = {}
                            
                            # Get section information from the database
                            con = get_db_connection()
                            try:
                                # Get major section information
                                major_section_query = """
                                    SELECT id, section FROM Major_Sections 
                                    WHERE major_id = ?
                                """
                                for row in con.execute(major_section_query, (plan['major_id'],)).fetchall():
                                    section_id, section_name = row
                                    major_sections_info[section_id] = section_name
                                    major_courses[section_name] = []
                                
                                # Get concentration section information if this plan has a concentration
                                if plan['concentration_id']:
                                    concentration_section_query = """
                                        SELECT id, section FROM Concentration_Sections 
                                        WHERE concentration_id = ?
                                    """
                                    for row in con.execute(concentration_section_query, (plan['concentration_id'],)).fetchall():
                                        section_id, section_name = row
                                        concentration_sections_info[section_id] = section_name
                                        concentration_courses[section_name] = []
                                
                                # Get gen ed section information
                                gen_ed_section_query = """
                                    SELECT id, section FROM Gen_Ed_Sections
                                """
                                for row in con.execute(gen_ed_section_query).fetchall():
                                    section_id, section_name = row
                                    gen_ed_sections_info[section_id] = section_name
                                    gen_ed_courses[section_name] = []
                                
                                # Categorize all available courses
                                for course in all_available:
                                    course_subject = course['subject']
                                    course_number = int(course['number'])
                                    section_name = course['section']
                                    
                                    # Check if this is a major course requirement
                                    major_section_query = """
                                        SELECT ms.id, ms.section
                                        FROM Major_Sections ms
                                        JOIN Major_Section_Requirements msr ON ms.id = msr.section_id
                                        WHERE ms.major_id = ? AND msr.course_subject = ? AND msr.course_number = ?
                                    """
                                    major_section = con.execute(major_section_query, 
                                                            (plan['major_id'], course_subject, course_number)).fetchone()
                                    
                                    if major_section:
                                        section_id, name = major_section
                                        if name not in major_courses:
                                            major_courses[name] = []
                                        major_courses[name].append(course)
                                        continue
                                    
                                    # Check if this is a concentration course requirement
                                    if plan['concentration_id']:
                                        conc_section_query = """
                                            SELECT cs.id, cs.section
                                            FROM Concentration_Sections cs
                                            JOIN Concentration_Section_Requirements csr ON cs.id = csr.section_id
                                            WHERE cs.concentration_id = ? AND csr.course_subject = ? AND csr.course_number = ?
                                        """
                                        conc_section = con.execute(conc_section_query, 
                                                              (plan['concentration_id'], course_subject, course_number)).fetchone()
                                        
                                        if conc_section:
                                            section_id, name = conc_section
                                            if name not in concentration_courses:
                                                concentration_courses[name] = []
                                            concentration_courses[name].append(course)
                                            continue
                                    
                                    # Check if this is a gen ed course requirement
                                    gen_ed_query = """
                                        SELECT ges.id, ges.section
                                        FROM Gen_Ed_Sections ges
                                        JOIN Gen_Ed_Section_Requirements ger ON ges.id = ger.section_id
                                        WHERE ger.course_subject = ? AND ger.course_number = ?
                                    """
                                    gen_ed_section = con.execute(gen_ed_query, 
                                                            (course_subject, course_number)).fetchone()
                                    
                                    if gen_ed_section:
                                        section_id, name = gen_ed_section
                                        if name not in gen_ed_courses:
                                            gen_ed_courses[name] = []
                                        gen_ed_courses[name].append(course)
                                        continue
                                    
                                    # If we can't categorize the course, add to "Other Courses"
                                    if "Other Courses" not in gen_ed_courses:
                                        gen_ed_courses["Other Courses"] = []
                                    gen_ed_courses["Other Courses"].append(course)
                                    
                            finally:
                                con.close()
                            
                            # Create tabs for different course types
                            course_tabs = st.tabs(["Major Courses", "Concentration Courses", "Gen Ed Courses"])
                            
                            with course_tabs[0]:  # Major Courses
                                for section_name in major_sections_info.values():
                                    courses = major_courses.get(section_name, [])
                                    
                                    # Display section header
                                    st.subheader(section_name)
                                    
                                    if not courses:
                                        st.info(f"No available courses in this section. Choose from other sections to complete prerequisites.")
                                        continue
                                    
                                    # Display courses in this section
                                    section_safe = section_name.replace(" ", "_").replace(":", "_")
                                    course_options = [f"{c['subject']} {c['number']} - {c['name']} ({c['credits']} cr)" for c in courses]
                                    selected_course = st.selectbox(
                                        "Select course", 
                                        options=["Select..."] + course_options,
                                        key=f"major_{section_safe}_{semester_id}"
                                    )
                                    
                                    if selected_course != "Select..." and st.button("Add Course", key=f"add_major_{section_safe}_{semester_id}"):
                                        # Parse course info
                                        course_info = selected_course.split(" - ")[0].strip()
                                        subject, number = course_info.split(" ")
                                        
                                        # Add course to semester
                                        result = add_course_to_semester(plan['id'], semester_id, subject, number)
                                        if result["success"]:
                                            st.success(result["message"])
                                            st.rerun()
                                        else:
                                            st.error(result["message"])
                            
                            with course_tabs[1]:  # Concentration Courses
                                if not plan['concentration_id']:
                                    st.info("This plan does not have a concentration")
                                else:
                                    # Force display of all concentration sections
                                    for section_name in concentration_sections_info.values():
                                        courses = concentration_courses.get(section_name, [])
                                        
                                        # Display section header
                                        st.subheader(section_name)
                                        
                                        if not courses:
                                            st.info(f"No available courses in this section")
                                            continue
                                        
                                        # Display courses in this section
                                        section_safe = section_name.replace(" ", "_").replace(":", "_")
                                        course_options = [f"{c['subject']} {c['number']} - {c['name']} ({c['credits']} cr)" for c in courses]
                                        selected_course = st.selectbox(
                                            "Select course", 
                                            options=["Select..."] + course_options,
                                            key=f"conc_{section_safe}_{semester_id}"
                                        )
                                        
                                        if selected_course != "Select..." and st.button("Add Course", key=f"add_conc_{section_safe}_{semester_id}"):
                                            # Parse course info
                                            course_info = selected_course.split(" - ")[0].strip()
                                            subject, number = course_info.split(" ")
                                            
                                            # Add course to semester
                                            result = add_course_to_semester(plan['id'], semester_id, subject, number)
                                            if result["success"]:
                                                st.success(result["message"])
                                                st.rerun()
                                            else:
                                                st.error(result["message"])
                            
                            with course_tabs[2]:  # Gen Ed Courses
                                # Force display of all gen ed sections
                                for section_name in gen_ed_sections_info.values():
                                    courses = gen_ed_courses.get(section_name, [])
                                    
                                    # Display section header
                                    st.subheader(section_name)
                                    
                                    if not courses:
                                        st.info(f"No available courses in this section")
                                        continue
                                    
                                    # Display courses in this section
                                    section_safe = section_name.replace(" ", "_").replace(":", "_")
                                    course_options = [f"{c['subject']} {c['number']} - {c['name']} ({c['credits']} cr)" for c in courses]
                                    selected_course = st.selectbox(
                                        "Select course", 
                                        options=["Select..."] + course_options,
                                        key=f"gen_ed_{section_safe}_{semester_id}"
                                    )
                                    
                                    if selected_course != "Select..." and st.button("Add Course", key=f"add_gen_ed_{section_safe}_{semester_id}"):
                                        # Parse course info
                                        course_info = selected_course.split(" - ")[0].strip()
                                        subject, number = course_info.split(" ")
                                        
                                        # Add course to semester
                                        result = add_course_to_semester(plan['id'], semester_id, subject, number)
                                        if result["success"]:
                                            st.success(result["message"])
                                            st.rerun()
                                        else:
                                            st.error(result["message"])
                                
                                # Check for "Other Courses" section
                                if "Other Courses" in gen_ed_courses and gen_ed_courses["Other Courses"]:
                                    st.subheader("Other Courses")
                                    courses = gen_ed_courses["Other Courses"]
                                    course_options = [f"{c['subject']} {c['number']} - {c['name']} ({c['credits']} cr)" for c in courses]
                                    selected_course = st.selectbox(
                                        "Select course", 
                                        options=["Select..."] + course_options,
                                        key=f"gen_ed_other_{semester_id}"
                                    )
                                    
                                    if selected_course != "Select..." and st.button("Add Course", key=f"add_gen_ed_other_{semester_id}"):
                                        # Parse course info
                                        course_info = selected_course.split(" - ")[0].strip()
                                        subject, number = course_info.split(" ")
                                        
                                        # Add course to semester
                                        result = add_course_to_semester(plan['id'], semester_id, subject, number)
                                        if result["success"]:
                                            st.success(result["message"])
                                            st.rerun()
                                        else:
                                            st.error(result["message"])
                
                # Done editing button
                if st.button("Done Editing"):
                    st.session_state.editing_plan = False
                    st.session_state.current_plan_id = None
                    st.rerun()
    with tab4:
        st.subheader("Review Plan Suggestions")
        
        # Get all plans for this student
        all_plans = c_plan.get_plans("student", student['ID'])
        
        # Filter out the original plans (not suggestions)
        original_plans = [p for p in all_plans if not p['is_suggestion']]
        
        if not original_plans:
            st.info("You don't have any plans yet. Create one in the 'Create New Plan' tab.")
        else:
            # Filter to find only those original plans that have suggestions
            plans_with_suggestions = []
            for plan in original_plans:
                # Find suggestions for this plan
                suggestions = [p for p in all_plans if p['is_suggestion'] == 1 and p['original_plan_id'] == plan['id']]
                if suggestions:
                    plans_with_suggestions.append((plan, suggestions))
            if not plans_with_suggestions:
                st.info("You don't have any suggestions from advisors yet.")
            else:
                st.write(f"You have advisor suggestions for {len(plans_with_suggestions)} plan(s).")
                
                # Let user select which plan's suggestions to view
                plan_names = [f"{plan['name']} ({len(suggestions)} suggestion{'s' if len(suggestions) > 1 else ''})" 
                              for plan, suggestions in plans_with_suggestions]
                selected_plan_idx = st.selectbox(
                    "Select a plan to view suggestions", 
                    options=range(len(plan_names)),
                    format_func=lambda x: plan_names[x]
                )
                
                selected_plan, suggestions = plans_with_suggestions[selected_plan_idx]
                
                # If there's only one suggestion, show it directly
                if len(suggestions) == 1:
                    suggestion = suggestions[0]
                    display_plan_comparison(selected_plan['id'], suggestion['id'])
                else:
                    # Let user select which suggestion to view
                    suggestion_names = [f"{s['name']} (by {c_advisor.get_advisor(s['advisor_id'])['name']})" for s in suggestions]
                    selected_suggestion_idx = st.selectbox(
                        "Select a suggestion to review", 
                        options=range(len(suggestion_names)),
                        format_func=lambda x: suggestion_names[x]
                    )
                    
                    selected_suggestion = suggestions[selected_suggestion_idx]
                    display_plan_comparison(selected_plan['id'], selected_suggestion['id'])                    
else:
    st.write("Please log in to view this page.")
    # Close the database connection
    if st.button("Go to Login"):
        st.session_state.viewing_plan = False
        st.session_state.creating_plan = False
        st.session_state.editing_plan = False
        st.session_state.plan_name = ""
        st.session_state.major = ""
        st.session_state.start_term = ""
        st.session_state.username = None
        st.session_state.password = None
        st.switch_page("home.py")