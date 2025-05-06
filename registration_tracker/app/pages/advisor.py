import streamlit as st
import controllers.students as c_student
import controllers.advisors as c_advisor
import controllers.plans as c_plan
import controllers.majors as c_major
import controllers.semesters as c_semester
import controllers.courses as c_course
import controllers.notes as c_notes
from app_utils import display_plan, get_available_courses, add_course_to_semester, get_db_connection, remove_from_semester
from auth_utils import protect_page

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

# Role-based protection
protect_page("advisor")  # Replace with appropriate role

# Sidebar navigation based on user role
with st.sidebar:
    st.markdown('<div class="custom-sidebar">', unsafe_allow_html=True)
    st.title("Navigation")
 
    if st.session_state.user_role == "student":
        if st.button("Dashboard"):
            st.switch_page("pages/student.py")
        if st.button("Graduation Plans"):
            st.switch_page("pages/plans.py")
    elif st.session_state.user_role == "advisor":
        if st.button("Advisor Dashboard"):
            st.switch_page("pages/advisor.py")
    elif st.session_state.user_role == "admin":
        if st.button("Admin Dashboard"):
            st.switch_page("pages/admin.py")
    # Add logout button
    if st.button("Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.switch_page("home.py")
st.markdown('</div>', unsafe_allow_html=True)

# If we got past the protection, the user is an advisor and logged in
username = st.session_state.username
st.write(f"Welcome, {username}!\n")
adv_id = c_advisor.get_advisor_user(st.session_state.username)['id']
students = c_student.get_students(adv_id)
student_names = [f"{s['f_name']} {s['l_name']}" for s in students]
selected_student = st.selectbox("Select a student", student_names)

# Initialize session state variables for suggestions
for key in ["suggesting_plan", "suggestion_name", "current_suggestion_id", "original_plan_id"]:
    if key not in st.session_state:
        st.session_state[key] = "" if key not in ["suggesting_plan"] else False

# Find selected student's data
student = next((s for s in students if f"{s['f_name']} {s['l_name']}" == selected_student), None)
advisor = c_advisor.get_advisor(adv_id)

if student:
    st.markdown(f"### 📘 Student Profile: {student['f_name']} {student['l_name']}")
    st.write(f"**Student ID:** {student['ID']}")
    st.write(f"**Major:** {c_major.get_major(student['major_id'])['name'] if student['major_id'] else 'Not set'}")
    st.write(f"**Graduation Date:** {student['Graduation_Date'] or 'Not set'}")

    tab1, tab2, tab3 = st.tabs(["📑 View Plans", "🔄 Create Suggestion", "📝 Feedback"])

    with tab1:
        # Get all plans for the student
        plans = c_plan.get_plans("student", student['ID'])
        
        if not plans:
            st.info(f"{student['f_name']} doesn't have any plans yet.")
        else:
            plan_names = [plan['name'] for plan in plans]
            selected_plan = st.selectbox("Select a plan to view", options=plan_names)
            
            if selected_plan:
                plan = c_plan.get_plan(selected_plan, "student", student['ID'])
                # Add button to create suggestion based on this plan
                if st.button("Create Suggestion Based on This Plan"):
                    st.session_state.suggesting_plan = True
                    st.session_state.original_plan_id = plan['id']
                    st.rerun()
                display_plan(plan['id'])
    
    with tab2:
        # Check if we are in suggestion mode
        if st.session_state.suggesting_plan and st.session_state.original_plan_id:
            # Get the original plan details
            original_plan = c_plan.get_plan_from_id(st.session_state.original_plan_id)
            
            if not original_plan:
                st.error("Original plan not found. Please try again.")
                st.session_state.suggesting_plan = False
                st.rerun()
            
            st.subheader(f"Creating Suggestion Based on: {original_plan['name']}")
            
            # Input for suggestion name with default value
            suggestion_name = st.text_input(
                "Suggestion Name", 
                value=f"Advisor Suggestion for {original_plan['name']}",
                key="suggestion_name_input"
            )
            
            # Create the suggestion if not already created
            if "current_suggestion_id" not in st.session_state or not st.session_state.current_suggestion_id:
                if st.button("Create Suggestion Copy"):
                    semesters = c_semester.get_semesters(original_plan['id'])
                    first_semester = semesters[0] if semesters else None
                    first_semester = f"{first_semester['term']} {first_semester['year']}"
                    # Create a new plan with the same properties but marked as a suggestion
                    suggestion_created = c_plan.create_plan(
                        student['ID'], 
                        adv_id,
                        suggestion_name, 
                        original_plan['major_id'], 
                        original_plan['concentration_id'], 
                        first_semester,
                        is_suggestion=1,
                        original_plan_id=original_plan['id']
                    )
                    
                    if suggestion_created:
                        suggestion_plan = c_plan.get_plan(suggestion_name, "student", student['ID'])
                        
                        if suggestion_plan:
                            st.session_state.current_suggestion_id = suggestion_plan['id']
                            
                            # Copy all semesters from original plan
                            original_semesters = c_semester.get_semesters(original_plan['id'])
                            
                            for orig_semester in original_semesters:
                                new_semester = c_semester.get_semester(orig_semester['term'], orig_semester['year'])
                                
                                # Link semester to suggestion plan
                                c_semester.insert_to_plan(suggestion_plan['id'], new_semester['id'])
                                
                                # Copy courses from original semester to new semester
                                courses = c_course.get_semester_courses(orig_semester['id'], original_plan['id'])
                                for course in courses:
                                    add_course_to_semester(
                                        suggestion_plan['id'], 
                                        new_semester['id'], 
                                        course['subject'], 
                                        course['number']
                                    )
                            
                            st.success(f"Suggestion plan '{suggestion_name}' created successfully!")
                            st.rerun()
                        else:
                            st.error("Failed to retrieve the created suggestion.")
                    else:
                        st.error("Failed to create the suggestion plan. Please try again.")
            else:
                # We're now editing an existing suggestion
                suggestion_plan = c_plan.get_plan_from_id(st.session_state.current_suggestion_id)
                
                if not suggestion_plan:
                    st.error("Suggestion plan not found. Please try again.")
                    st.session_state.suggesting_plan = False
                    st.session_state.current_suggestion_id = None
                    st.rerun()
                
                st.subheader(f"Editing Suggestion: {suggestion_plan['name']}")

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Submit Suggestion to Student"):
                        st.success("Suggestion submitted to the student successfully!")
                        st.session_state.suggesting_plan = False
                        st.session_state.current_suggestion_id = None
                        st.rerun()

                with col2:
                    if st.button("Cancel Suggestion"):
                        c_plan.delete_plan(st.session_state.current_suggestion_id)
                        st.session_state.suggesting_plan = False
                        st.session_state.current_suggestion_id = None
                        st.info("Suggestion creation canceled.")
                        st.rerun()

                # Get semesters in the suggestion plan
                semesters = c_semester.get_semesters(suggestion_plan['id'])
                
                if not semesters:
                    st.warning("No semesters in this suggestion plan.")
                else:
                    # For each semester, allow adding/removing courses
                    for semester in semesters:
                        semester_id = semester['id']
                        semester_name = f"{semester['term']} {semester['year']}"
                        
                        with st.expander(f"Edit {semester_name}"):
                            # Display current courses in this semester
                            courses = c_course.get_semester_courses(semester_id, suggestion_plan['id'])
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
                                            remove_from_semester(suggestion_plan['id'], semester_id, course['subject'], course['number'])
                                            st.success(f"Removed {course['subject']} {course['number']} from {semester_name}")
                                            st.rerun()
                            else:
                                st.write("No courses in this semester yet.")
                            
                            # Add new courses section
                            st.subheader("Add Courses")
                            
                            # Get all available courses for this semester
                            all_available = get_available_courses(suggestion_plan['id'], semester_id, suggestion_plan['major_id'])
                            
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
                                for row in con.execute(major_section_query, (suggestion_plan['major_id'],)).fetchall():
                                    section_id, section_name = row
                                    major_sections_info[section_id] = section_name
                                    major_courses[section_name] = []
                                
                                # Get concentration section information if this plan has a concentration
                                if suggestion_plan['concentration_id']:
                                    concentration_section_query = """
                                        SELECT id, section FROM Concentration_Sections 
                                        WHERE concentration_id = ?
                                    """
                                    for row in con.execute(concentration_section_query, (suggestion_plan['concentration_id'],)).fetchall():
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
                                                            (suggestion_plan['major_id'], course_subject, course_number)).fetchone()
                                    
                                    if major_section:
                                        section_id, name = major_section
                                        if name not in major_courses:
                                            major_courses[name] = []
                                        major_courses[name].append(course)
                                        continue
                                    
                                    # Check if this is a concentration course requirement
                                    if suggestion_plan['concentration_id']:
                                        conc_section_query = """
                                            SELECT cs.id, cs.section
                                            FROM Concentration_Sections cs
                                            JOIN Concentration_Section_Requirements csr ON cs.id = csr.section_id
                                            WHERE cs.concentration_id = ? AND csr.course_subject = ? AND csr.course_number = ?
                                        """
                                        conc_section = con.execute(conc_section_query, 
                                                                (suggestion_plan['concentration_id'], course_subject, course_number)).fetchone()
                                        
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
                                        st.info(f"No available courses in this section. Prerequisites may not be met.")
                                        continue
                                    
                                    # Display courses in this section
                                    section_safe = section_name.replace(" ", "_").replace(":", "_")
                                    course_options = [f"{c['subject']} {c['number']} - {c['name']} ({c['credits']} cr)" for c in courses]
                                    selected_course = st.selectbox(
                                        "Select course", 
                                        options=["Select..."] + course_options,
                                        key=f"suggest_major_{section_safe}_{semester_id}"
                                    )
                                    
                                    if selected_course != "Select..." and st.button("Add Course", key=f"suggest_add_major_{section_safe}_{semester_id}"):
                                        # Parse course info
                                        course_info = selected_course.split(" - ")[0].strip()
                                        subject, number = course_info.split(" ")
                                        
                                        # Add course to semester
                                        result = add_course_to_semester(suggestion_plan['id'], semester_id, subject, number)
                                        if result["success"]:
                                            st.success(result["message"])
                                            st.rerun()
                                        else:
                                            st.error(result["message"])
                            
                            with course_tabs[1]:  # Concentration Courses
                                if not suggestion_plan['concentration_id']:
                                    st.info("This plan does not have a concentration")
                                else:
                                    for section_name in concentration_sections_info.values():
                                        courses = concentration_courses.get(section_name, [])
                                        st.subheader(section_name)
                        
                                        if not courses:
                                            st.info(f"No available courses in this section. Prerequisites may not be met.")
                                            continue
                                        
                                        # Display courses in this section
                                        section_safe = section_name.replace(" ", "_").replace(":", "_")
                                        course_options = [f"{c['subject']} {c['number']} - {c['name']} ({c['credits']} cr)" for c in courses]
                                        selected_course = st.selectbox(
                                            "Select course", 
                                            options=["Select..."] + course_options,
                                            key=f"suggest_conc_{section_safe}_{semester_id}"
                                        )
                                        
                                        if selected_course != "Select..." and st.button("Add Course", key=f"suggest_add_conc_{section_safe}_{semester_id}"):
                                            course_info = selected_course.split(" - ")[0].strip()
                                            subject, number = course_info.split(" ")
                                            
                                            # Add course to semester
                                            result = add_course_to_semester(suggestion_plan['id'], semester_id, subject, number)
                                            if result["success"]:
                                                st.success(result["message"])
                                                st.rerun()
                                            else:
                                                st.error(result["message"])
                            
                            with course_tabs[2]:  # Gen Ed Courses
                                for section_name in gen_ed_sections_info.values():
                                    courses = gen_ed_courses.get(section_name, [])
                                    st.subheader(section_name)
                                    
                                    if not courses:
                                        st.info(f"No available courses in this section. Prerequisites may not be met.")
                                        continue
                                    
                                    # Display courses in this section
                                    section_safe = section_name.replace(" ", "_").replace(":", "_")
                                    course_options = [f"{c['subject']} {c['number']} - {c['name']} ({c['credits']} cr)" for c in courses]
                                    selected_course = st.selectbox(
                                        "Select course", 
                                        options=["Select..."] + course_options,
                                        key=f"suggest_gen_ed_{section_safe}_{semester_id}"
                                    )
                                    
                                    if selected_course != "Select..." and st.button("Add Course", key=f"suggest_add_gen_ed_{section_safe}_{semester_id}"):
                                        course_info = selected_course.split(" - ")[0].strip()
                                        subject, number = course_info.split(" ")
                                        
                                        # Add course to semester
                                        result = add_course_to_semester(suggestion_plan['id'], semester_id, subject, number)
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
                                        key=f"suggest_gen_ed_other_{semester_id}"
                                    )
                                    
                                    if selected_course != "Select..." and st.button("Add Course", key=f"suggest_add_gen_ed_other_{semester_id}"):
                                        course_info = selected_course.split(" - ")[0].strip()
                                        subject, number = course_info.split(" ")
                                        
                                        # Add course to semester
                                        result = add_course_to_semester(suggestion_plan['id'], semester_id, subject, number)
                                        if result["success"]:
                                            st.success(result["message"])
                                            st.rerun()
                                        else:
                                            st.error(result["message"])
        else:
            st.info("Select a student's plan in the 'View Plans' tab first, then click 'Create Suggestion Based on This Plan'")

    with tab3:
        st.subheader("Student Communication")
        
        # First, get all plans for the selected student
        plans = c_plan.get_plans("student", student['ID'])
        
        if not plans:
            st.info(f"{student['f_name']} doesn't have any plans yet.")
        else:
            # Allow selecting which plan to leave feedback on
            plan_names = [plan['name'] for plan in plans]
            selected_plan_name = st.selectbox("Select a plan for communication", options=plan_names)
            
            if selected_plan_name:
                selected_plan = c_plan.get_plan(selected_plan_name, "student", student['ID'])
                
                # Display existing notes/feedback for this plan
                st.subheader(f"Communication History for '{selected_plan_name}'")
                
                # Get both advisor and student notes for this plan
                advisor_notes = c_notes.get_advisor_notes(adv_id, selected_plan['id'])
                student_notes = c_notes.get_student_notes(student['ID'], selected_plan['id'])
                
                # Combine notes and sort by timestamp (most recent first)
                all_notes = []
                
                # Add advisor notes with source info
                for note in advisor_notes:
                    content, timestamp = note
                    all_notes.append({
                        'content': content,
                        'timestamp': timestamp,
                        'is_advisor': True,
                        'name': f"{advisor['f_name']} {advisor['l_name']}"
                    })
                
                # Add student notes with source info
                for note in student_notes:
                    content, timestamp = note
                    all_notes.append({
                        'content': content,
                        'timestamp': timestamp,
                        'is_advisor': False,
                        'name': f"{student['f_name']} {student['l_name']}"
                    })
                
                # Sort all notes by timestamp (most recent first)
                all_notes.sort(key=lambda x: x['timestamp'], reverse=True)
                
                if all_notes:
                    st.write(f"Found {len(all_notes)} messages")
                    
                    # Display each note with timestamp
                    from datetime import datetime
                    
                    for i, note in enumerate(all_notes):
                        # Convert Unix timestamp to readable format
                        readable_time = datetime.fromtimestamp(note['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
                        
                        # Set message style based on sender
                        message_type = "Advisor" if note['is_advisor'] else "Student"
                        message_icon = "👨‍🏫" if note['is_advisor'] else "👨‍🎓"
                        
                        # Display note in an expander with date and sender info
                        with st.expander(f"Message {len(all_notes) - i} - {readable_time} by {message_icon} {note['name']}", expanded=(i==0)):
                            st.write(note['content'])
                else:
                    st.info("No previous communications for this plan.")
                
                # Input for new note
                st.subheader("Add New Communication")
                new_note = st.text_area("Message for student", height=150)
                
                if st.button("Send Message"):
                    if new_note.strip():  # Check if note is not empty
                        # Save the new note
                        c_notes.save_advisor_note(adv_id, selected_plan['id'], new_note)
                        st.success("Message sent successfully!")
                        st.rerun()
                    else:
                        st.warning("Please enter a message before sending.")
