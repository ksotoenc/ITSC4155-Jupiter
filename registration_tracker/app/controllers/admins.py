import sqlite3

DB_NAME = "reg_tracker.db"

# Function to create a connection to SQLite
def get_db_connection():
    con = sqlite3.connect(DB_NAME)
    con.row_factory = sqlite3.Row  # Enables dictionary-like row access
    return con

# get one admin
def get_admin(id):
    query = """ SELECT * FROM Admins
                WHERE id = ?
                LIMIT 1 """
    con = get_db_connection()
    admin = con.execute(query, (id,)).fetchone()
    con.close()
    return admin

def get_admin_user(user):
    query = """ SELECT id FROM Admins
                WHERE username = ?
                LIMIT 1 """
    con = get_db_connection()
    admin = con.execute(query, (user,)).fetchone()
    con.close()
    return admin

# get all admins
def get_all_admins():
    query = """ SELECT * FROM Admins
                """
    con = get_db_connection()
    admins = con.execute(query).fetchall()
    con.close()
    return admins

# # add an admin (admin)
# def add_advisor(id, username, password, f_name, l_name):
#     """
#     Adds a new advisor to the Advisors table.
#     """
#     query = """ INSERT INTO Advisors (id, username, password, f_name, l_name)
#                 VALUES (?, ?, ?, ?, ?) """
#     con = get_db_connection()
#     try:
#         con.execute(query, (id, username, password, f_name, l_name))
#         con.commit()
#         return {"success": True, "message": "Advisor added successfully."}
#     except sqlite3.IntegrityError as e:
#         return {"success": False, "message": f"Error adding advisor: {e}"}
#     finally:
#         con.close()

# # update an advisor (admin)
# def update_advisor(id, username=None, password=None, f_name=None, l_name=None):
#     fields = []
#     values = []

#     if username:
#         fields.append("username = ?")
#         values.append(username)
#     if password:
#         fields.append("password = ?")
#         values.append(password)
#     if f_name:
#         fields.append("f_name = ?")
#         values.append(f_name)
#     if l_name:
#         fields.append("l_name = ?")
#         values.append(l_name)

#     if not fields:
#         return {"success": False, "message": "No fields to update."}

#     query = f""" UPDATE Advisors
#                  SET {', '.join(fields)}
#                  WHERE id = ? """
#     values.append(id)

#     con = get_db_connection()
#     try:
#         con.execute(query, values)
#         con.commit()
#         return {"success": True, "message": "Advisor updated successfully."}
#     except sqlite3.Error as e:
#         return {"success": False, "message": f"Error updating advisor: {e}"}
#     finally:
#         con.close()

# # delete an advisor (admin)
# def delete_advisor(id):
#     query = """ DELETE FROM Advisors
#                 WHERE id = ? """
#     con = get_db_connection()
#     try:
#         con.execute(query, (id,))
#         con.commit()
#         return {"success": True, "message": "Advisor deleted successfully."}
#     except sqlite3.Error as e:
#         return {"success": False, "message": f"Error deleting advisor: {e}"}
#     finally:
#         con.close()