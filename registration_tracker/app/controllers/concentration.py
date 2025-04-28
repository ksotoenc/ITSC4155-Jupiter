import sqlite3

DB_NAME = "reg_tracker.db"

# Function to create a connection to SQLite
def get_db_connection():
    con = sqlite3.connect(DB_NAME)
    con.row_factory = sqlite3.Row  # Enables dictionary-like row access
    return con

# Get a specific concentration
def get_concentration(id):
    query = """ SELECT * FROM Concentrations
                WHERE id = ?
                """
    con = get_db_connection()
    concentration = con.execute(query, (id,)).fetchone()
    con.close()
    return concentration

# Get a concentration ID by name
def get_concentration_id(name):
    """
    Retrieves the ID of a concentration by its name.
    """
    query = """ SELECT id FROM Concentrations
                WHERE name = ? """
    con = get_db_connection()
    concentration = con.execute(query, (name,)).fetchone()
    con.close()
    return concentration['id'] if concentration else None

# Get concentrations by major_id
def get_concentrations_by_major(major_id):
    """
    Retrieves all concentrations associated with a specific major.
    """
    query = """ SELECT * FROM Concentrations
                WHERE major_id = ? """
    con = get_db_connection()
    concentrations = con.execute(query, (major_id,)).fetchall()
    con.close()
    return concentrations

# Add a concentration (admin)
def add_concentration(name, major_id):
    """
    Adds a new concentration to the Concentration table.
    """
    query = """ INSERT INTO Concentrations (name, major_id)
                VALUES (?, ?) """
    con = get_db_connection()
    try:
        con.execute(query, (name, major_id))
        con.commit()
        return {"success": True, "message": "Concentration added successfully."}
    except sqlite3.IntegrityError as e:
        return {"success": False, "message": f"Error adding concentration: {e}"}
    finally:
        con.close()

# Update a concentration (admin)
def update_concentration(concentration_id, name=None, major_id=None):
    """
    Updates an existing concentration in the Concentration table.
    """
    fields = []
    values = []

    if name:
        fields.append("name = ?")
        values.append(name)
    if major_id:
        fields.append("major_id = ?")
        values.append(major_id)

    if not fields:
        return {"success": False, "message": "No fields to update."}

    query = f""" UPDATE Concentrations
                 SET {', '.join(fields)}
                 WHERE id = ? """
    values.append(concentration_id)

    con = get_db_connection()
    try:
        con.execute(query, values)
        con.commit()
        return {"success": True, "message": "Concentration updated successfully."}
    except sqlite3.Error as e:
        return {"success": False, "message": f"Error updating concentration: {e}"}
    finally:
        con.close()

# Delete a concentration (admin)
def delete_concentration(concentration_id):
    """
    Deletes a concentration from the Concentration table.
    """
    query = """ DELETE FROM Concentrations
                WHERE id = ? """
    con = get_db_connection()
    try:
        con.execute(query, (concentration_id,))
        con.commit()
        return {"success": True, "message": "Concentration deleted successfully."}
    except sqlite3.Error as e:
        return {"success": False, "message": f"Error deleting concentration: {e}"}
    finally:
        con.close()