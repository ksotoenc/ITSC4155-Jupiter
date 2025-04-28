import sqlite3
import streamlit as st
import pandas as pd
import controllers.plans as c_plans
import controllers.majors as c_majors
import controllers.courses as c_courses
import controllers.semesters as c_semesters

# Database Configuration (SQLite)
DB_NAME = "reg_tracker.db"

# Function to create a connection to SQLite
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Enables dictionary-like row access
    return conn

def check_prerequisites(plan_id, course_subject, course_number, target_semester_id):
    """
    Check if prerequisites for a course are met in previous semesters.
    Returns: 
        - True if all prerequisites are met
        - False if some prerequisites are not met
        - A list of missing prerequisites if detailed=True
    """
    con = get_db_connection()
    try:
        # Get all prerequisites for this course
        prerequisites = c_courses.get_course_prereq(course_subject, course_number)
        
        if not prerequisites:
            # No prerequisites, so requirements are met
            return True
        
        # Get all previous semesters in this plan (before target_semester_id)
        sem_order_query = """
            SELECT ps.semester_id, s.term, s.year
            FROM Plan_Semesters ps
            JOIN Semesters s ON ps.semester_id = s.id
            WHERE ps.plan_id = ?
            ORDER BY s.year, 
                    CASE WHEN s.term = 'Spring' THEN 0 ELSE 1 END
        """
        all_semesters = con.execute(sem_order_query, (plan_id,)).fetchall()
        
        # Find the index of the target semester
        target_idx = -1
        for i, sem in enumerate(all_semesters):
            if sem[0] == target_semester_id:
                target_idx = i
                break
        
        if target_idx == -1:
            # Target semester not found
            return False
        
        # Get all courses in previous semesters
        previous_courses = []
        for i in range(target_idx):
            semester_id = all_semesters[i][0]
            courses_query = """
                SELECT course_subject, course_number
                FROM Plan_Semester_Courses
                WHERE plan_id = ? AND semester_id = ?
            """
            courses = con.execute(courses_query, (plan_id, semester_id)).fetchall()
            previous_courses.extend([(c[0], c[1]) for c in courses])
        
        # Group prerequisites by group_id
        grouped_prereqs = {}
        for prereq in prerequisites:
            group_id = prereq[0]
            if group_id not in grouped_prereqs:
                grouped_prereqs[group_id] = []
            grouped_prereqs[group_id].append((prereq[1], prereq[2]))
        
        # Check if all prerequisite groups are satisfied
        missing_prereqs = []
        for group_id, prereqs in grouped_prereqs.items():
            group_satisfied = False
            for prereq in prereqs:
                if prereq in previous_courses:
                    group_satisfied = True
                    break
            
            if not group_satisfied:
                missing_prereqs.extend(prereqs)
        
        return len(missing_prereqs) == 0
        
    except Exception as e:
        print(f"Error checking prerequisites: {e}")
        return False
    finally:
        con.close()

def add_course_to_semester(plan_id, semester_id, course_subject, course_number):
    """
    Adds a course to a semester if prerequisites are met.
    Returns a dictionary with success status and message.
    """
    # First, check if prerequisites are met
    prereqs_met = check_prerequisites(plan_id, course_subject, course_number, semester_id)
    
    if not prereqs_met:
        return {
            "success": False,
            "message": "Prerequisites for this course are not met in previous semesters."
        }
    
    # Check if course already exists in this semester
    con = get_db_connection()
    try:
        check_query = """
            SELECT plan_id FROM Plan_Semester_Courses
            WHERE plan_id = ? AND semester_id = ? AND course_subject = ? AND course_number = ?
        """
        existing = con.execute(check_query, 
                              (plan_id, semester_id, course_subject, course_number)).fetchone()
        
        if existing:
            return {
                "success": False,
                "message": "This course is already in this semester."
            }
        
        # Add the course to the semester
        insert_query = """
            INSERT INTO Plan_Semester_Courses (plan_id, semester_id, course_subject, course_number)
            VALUES (?, ?, ?, ?)
        """
        con.execute(insert_query, (plan_id, semester_id, course_subject, course_number))
        con.commit()
        
        return {
            "success": True,
            "message": "Course added successfully."
        }
        
    except Exception as e:
        con.rollback()
        return {
            "success": False,
            "message": f"Error adding course: {e}"
        }
    finally:
        con.close()

def get_available_courses(plan_id, semester_id, major_id):
    """
    Get courses that are required for the major and meet prerequisites for the given semester.
    This function checks major sections, concentrations, and gen ed requirements.
    """
    con = get_db_connection()
    try:
        # Get plan information to check if it has a concentration
        plan_query = """
            SELECT concentration_id FROM Plans
            WHERE id = ?
        """
        plan = con.execute(plan_query, (plan_id,)).fetchone()
        concentration_id = plan['concentration_id'] if plan else None
        
        # Get courses already in the plan
        plan_courses_query = """
            SELECT course_subject, course_number
            FROM Plan_Semester_Courses
            WHERE plan_id = ?
        """
        plan_courses = con.execute(plan_courses_query, (plan_id,)).fetchall()
        plan_course_set = {(c['course_subject'], c['course_number']) for c in plan_courses}
        
        available_courses = []
        
        # 1. Get major section requirements
        major_section_query = """
            SELECT msr.course_subject, msr.course_number, c.name, c.credits, ms.section
            FROM Major_Sections ms
            JOIN Major_Section_Requirements msr ON ms.id = msr.section_id
            JOIN Courses c ON msr.course_subject = c.subject AND msr.course_number = c.number
            WHERE ms.major_id = ?
            ORDER BY ms.section, msr.group_id
        """
        major_courses = con.execute(major_section_query, (major_id,)).fetchall()
        
        # 2. Get concentration requirements if applicable
        concentration_courses = []
        if concentration_id:
            concentration_query = """
                SELECT csr.course_subject, csr.course_number, c.name, c.credits, cs.section
                FROM Concentration_Sections cs
                JOIN Concentration_Section_Requirements csr ON cs.id = csr.section_id
                JOIN Courses c ON csr.course_subject = c.subject AND csr.course_number = c.number
                WHERE cs.concentration_id = ?
                ORDER BY cs.section, csr.group_id
            """
            concentration_courses = con.execute(concentration_query, (concentration_id,)).fetchall()
        
        # 3. Get gen ed requirements
        gen_ed_query = """
            SELECT ger.course_subject, ger.course_number, c.name, c.credits, ges.section
            FROM Gen_Ed_Sections ges
            JOIN Gen_Ed_Section_Requirements ger ON ges.id = ger.section_id
            JOIN Courses c ON ger.course_subject = c.subject AND ger.course_number = c.number
            ORDER BY ges.section, ger.group_id
        """
        gen_ed_courses = con.execute(gen_ed_query).fetchall()
        
  
        # Combine all required courses
        all_courses = major_courses + concentration_courses + gen_ed_courses
        # Process courses to check prerequisites and build available courses list
        for course in all_courses:
            course_key = (course['course_subject'], course['course_number'])
            
            # Skip if already in the plan
            if course_key in plan_course_set:
                continue
            
            # Check prerequisites
            if check_prerequisites(plan_id, course['course_subject'], course['course_number'], semester_id):
                available_courses.append({
                    'subject': course[0],
                    'number': course[1],
                    'name': course[2],
                    'credits': course[3],
                    'section': course[4]  # Include section information for display
                })
        return available_courses
        
        
    except Exception as e:
        print(f"Error getting available courses: {e}")
        return []
    finally:
        con.close()
        
# Add this to your courses controller (c_courses)
def remove_semester_course(plan_id, semester_id, course_subject, course_number):
    """
    Remove a course from a semester.
    Returns a dictionary with success status and message.
    """
    con = get_db_connection()
    try:
        # Check if any courses in future semesters depend on this as a prerequisite
        # First get all future semesters
        sem_order_query = """
            SELECT ps.semester_id, s.term, s.year
            FROM Plan_Semesters ps
            JOIN Semesters s ON ps.semester_id = s.id
            WHERE ps.plan_id = ?
            ORDER BY s.year, 
                    CASE WHEN s.term = 'Spring' THEN 0 ELSE 1 END
        """
        all_semesters = con.execute(sem_order_query, (plan_id,)).fetchall()
        
        # Find the index of the current semester
        current_idx = -1
        for i, sem in enumerate(all_semesters):
            if sem[0] == semester_id:
                current_idx = i
                break
                
        if current_idx == -1:
            return {"success": False, "message": "Semester not found in plan."}
            
        # Check for future semesters' courses that might depend on this course
        dependent_courses = []
        
        for i in range(current_idx + 1, len(all_semesters)):
            future_semester_id = all_semesters[i][0]
            
            # Get courses in this future semester
            future_courses_query = """
                SELECT psc.course_subject, psc.course_number, c.name
                FROM Plan_Semester_Courses psc
                JOIN Courses c ON psc.course_subject = c.subject AND psc.course_number = c.number
                WHERE psc.plan_id = ? AND psc.semester_id = ?
            """
            future_courses = con.execute(future_courses_query, 
                                       (plan_id, future_semester_id)).fetchall()
                                       
            for fc in future_courses:
                # Check if this course depends on the course we're trying to remove
                prereq_query = """
                    SELECT 1 FROM Prerequisites
                    WHERE parent_subject = ? AND parent_number = ? 
                    AND course_subject = ? AND course_number = ?
                """
                is_prereq = con.execute(prereq_query, 
                                      (fc[0], fc[1], course_subject, course_number)).fetchone()
                                      
                if is_prereq:
                    dependent_courses.append(f"{fc[0]} {fc[1]} - {fc[2]}")
        
        if dependent_courses:
            return {
                "success": False,
                "message": f"Cannot remove this course as it's a prerequisite for: {', '.join(dependent_courses)}"
            }
        
        # If no dependencies, remove the course
        delete_query = """
            DELETE FROM Plan_Semester_Courses
            WHERE plan_id = ? AND semester_id = ? AND course_subject = ? AND course_number = ?
        """
        con.execute(delete_query, (plan_id, semester_id, course_subject, course_number))
        con.commit()
        
        return {"success": True, "message": "Course removed successfully."}
        
    except Exception as e:
        con.rollback()
        return {"success": False, "message": f"Error removing course: {e}"}
    finally:
        con.close()

def display_plan(plan_id):
    st.title("Degree Plan")
    
    plan = c_plans.get_plan_from_id(plan_id)

    if not plan:
        st.error("Plan not found")
        return

    major = c_majors.get_major(plan['major_id'])
    
    st.header(f"Plan: {plan['name']}")
    st.subheader(f"Major: {major['name']}")
    
    # Get all semesters in the plan
    semesters = c_semesters.get_semesters(plan_id)
    
    # Initialize total credit count
    total_credits = 0
    
    # Create a container for the progress bar
    progress_container = st.container()
    with progress_container:
        st.write("Total Credits: Calculating...")
        progress_bar = st.progress(0)
    
    # Display each semester in an expander
    for semester in semesters:
        semester_id = semester['id']
        semester_name = f"{semester['term']} {semester['year']}"
        
        # Get courses for this semester
        courses = c_courses.get_semester_courses(semester_id, plan_id)
        
        # Calculate semester credit total
        semester_credits = sum(course['credits'] for course in courses)
        total_credits += semester_credits
        
        # Create an expander for this semester
        with st.expander(f"{semester_name} - {semester_credits} Credits"):
            if courses:
                # Convert to DataFrame for display
                df = pd.DataFrame([dict(c) for c in courses])
                # Add a course code column that combines subject and number
                df['Course'] = df['subject'] + ' ' + df['number'].astype(str)
                # Reorder and rename columns
                df = df[['Course', 'name', 'credits']]
                df.columns = ['Course', 'Course Name', 'Credits']
                
                # Display the courses table
                st.table(df)
            else:
                st.write("No courses assigned to this semester yet.")
            
            # Add course section
            st.subheader("Add Course to Semester")
            
            # Get available courses that can be added (prerequisites met)
            available_courses = get_available_courses(plan_id, semester_id, plan['major_id'])
            
            if available_courses:
                # Create formatted options for the selectbox
                course_options = ["Select a course"] + [
                    f"{c['subject']} {c['number']} - {c['name']} ({c['credits']} cr)" 
                    for c in available_courses
                ]
                
                selected_course = st.selectbox(
                    "Available courses (prerequisites met):", 
                    course_options,
                    key=f"add_course_{semester_id}"
                )
                
                if selected_course != "Select a course":
                    # Parse the selected course information
                    course_info = selected_course.split(" - ")[0].strip()
                    subject, number = course_info.split(" ")
                    
                    # Add button to confirm addition
                    if st.button("Add to Semester", key=f"add_btn_{semester_id}"):
                        result = add_course_to_semester(
                            plan_id, semester_id, subject, number
                        )
                        
                        if result["success"]:
                            st.success(result["message"])
                            st.rerun()  # Refresh the page
                        else:
                            st.error(result["message"])
            else:
                st.info("No available courses that meet prerequisites for this semester.")
            
            # Remove course option
            if courses:
                st.subheader("Remove Course")
                course_remove_options = ["Select a course"] + [
                    f"{c['subject']} {c['number']} - {c['name']}" for c in courses
                ]
                selected_remove = st.selectbox(
                    "Select course to remove:",
                    course_remove_options,
                    key=f"remove_course_{semester_id}"
                )
                
                if selected_remove != "Select a course":
                    if st.button("Remove Course", key=f"remove_btn_{semester_id}"):
                        course_info = selected_remove.split(" - ")[0].strip()
                        subject, number = course_info.split(" ")
                        
                        # Call function to remove course (to be implemented)
                        result = remove_semester_course(
                            plan_id, semester_id, subject, number
                        )
                        
                        if result["success"]:
                            st.success(result["message"])
                            st.rerun()
                        else:
                            st.error(result["message"])
    
    # Update the progress indicator
    # Assuming a typical degree requires 120 credits
    target_credits = 120
    progress_percentage = min(total_credits / target_credits, 1.0)
    
    with progress_container:
        st.write(f"Total Credits: {total_credits}/{target_credits}")
        progress_bar.progress(progress_percentage)
    
    # Display overall plan statistics
    st.subheader("Plan Summary")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Credits", total_credits)
    with col2:
        st.metric("Semesters", len(semesters))
    with col3:
        st.metric("Remaining Credits", max(0, target_credits - total_credits))