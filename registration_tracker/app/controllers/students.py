import sqlite3
import streamlit as st

DB_NAME = "reg_tracker.db"

# Function to create a connection to SQLite
def get_db_connection():
    con = sqlite3.connect(DB_NAME)
    con.row_factory = sqlite3.Row  # Enables dictionary-like row access
    return con

# get one student
# gets student based on id by default
def get_student(identifier, value):
    if identifier == "username":
        query = """ SELECT * FROM Students
                    WHERE username = ?
                    LIMIT 1 """
    else:
        query = """ SELECT * FROM Students
                    WHERE id = ?
                    LIMIT 1 """
    con = get_db_connection()
    student = con.execute(query, (value,)).fetchone()
    con.close()
    return student

# get several students from an advisor
def get_students(advisor_id):
    query = """ SELECT * FROM Students
                WHERE advisor_id = ?
                """
    con = get_db_connection()
    students = con.execute(query, (advisor_id,)).fetchall()
    con.close()
    return students

# get all students
def get_all_students():
    query = """ SELECT * FROM Students
                """
    con = get_db_connection()
    students = con.execute(query).fetchall()
    con.close()
    return students

# update a student (admin)
def update_student():
    pass

# delete a course (admin)
def delete_student():
    pass