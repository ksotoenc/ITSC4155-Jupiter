import unittest
from unittest.mock import patch, MagicMock
import sqlite3
import sys
import os

# Add parent directory to path to import the controllers
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from controllers import students

class TestStudentsController(unittest.TestCase):
    
    @patch('controllers.students.sqlite3.connect')
    def test_get_db_connection(self, mock_connect):
        # Set up the mock
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        
        # Call the function
        conn = students.get_db_connection()
        
        # Assertions
        mock_connect.assert_called_once_with(students.DB_NAME)
        self.assertEqual(conn, mock_conn)
        self.assertEqual(conn.row_factory, sqlite3.Row)
    
    @patch('controllers.students.get_db_connection')
    def test_get_student_by_username(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Create mock cursor and result
        mock_cursor = MagicMock()
        mock_conn.execute.return_value = mock_cursor
        
        # Mock the student data
        mock_student = {
            'id': 1600343,
            'f_name': 'Terry',
            'l_name': 'Trombo',
            'username': 'tbone',
            'password': 'password',
            'major_id': 1,
            'graduation_date': None,
            'advisor_id': 3409243
        }
        mock_cursor.fetchone.return_value = mock_student
        
        # Call the function
        result = students.get_student("username", "tbone")
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once_with(
            " SELECT * FROM Students\n                    WHERE username = ?\n                    LIMIT 1 ", 
            ("tbone",)
        )
        mock_cursor.fetchone.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertEqual(result, mock_student)
    
    @patch('controllers.students.get_db_connection')
    def test_get_student_by_id(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Create mock cursor and result
        mock_cursor = MagicMock()
        mock_conn.execute.return_value = mock_cursor
        
        # Mock the student data
        mock_student = {
            'id': 1600343,
            'f_name': 'Terry',
            'l_name': 'Trombo',
            'username': 'tbone',
            'password': 'password',
            'major_id': 1,
            'graduation_date': None,
            'advisor_id': 3409243
        }
        mock_cursor.fetchone.return_value = mock_student
        
        # Call the function
        result = students.get_student("id", 1600343)
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once_with(
            " SELECT * FROM Students\n                    WHERE id = ?\n                    LIMIT 1 ", 
            (1600343,)
        )
        mock_cursor.fetchone.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertEqual(result, mock_student)
    
    @patch('controllers.students.get_db_connection')
    def test_get_students(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Create mock cursor and result
        mock_cursor = MagicMock()
        mock_conn.execute.return_value = mock_cursor
        
        # Mock the students data
        mock_students = [
            {
                'id': 1600343,
                'f_name': 'Terry',
                'l_name': 'Trombo',
                'username': 'tbone',
                'password': 'password',
                'major_id': 1,
                'graduation_date': None,
                'advisor_id': 3409243
            },
            {
                'id': 1600344,
                'f_name': 'Jerry',
                'l_name': 'Johnson',
                'username': 'uname',
                'password': 'pword',
                'major_id': 1,
                'graduation_date': None,
                'advisor_id': 3409243
            }
        ]
        mock_cursor.fetchall.return_value = mock_students
        
        # Call the function
        result = students.get_students(3409243)
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once_with(
            " SELECT * FROM Students\n                WHERE advisor_id = ?\n                ", 
            (3409243,)
        )
        mock_cursor.fetchall.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertEqual(result, mock_students)
    
    @patch('controllers.students.get_db_connection')
    def test_get_all_students(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Create mock cursor and result
        mock_cursor = MagicMock()
        mock_conn.execute.return_value = mock_cursor
        
        # Mock the students data
        mock_students = [
            {
                'id': 1600343,
                'f_name': 'Terry',
                'l_name': 'Trombo',
                'username': 'tbone',
                'password': 'password',
                'major_id': 1,
                'graduation_date': None,
                'advisor_id': 3409243
            },
            {
                'id': 1600344,
                'f_name': 'Jerry',
                'l_name': 'Johnson',
                'username': 'uname',
                'password': 'pword',
                'major_id': 1,
                'graduation_date': None,
                'advisor_id': 3409243
            }
        ]
        mock_cursor.fetchall.return_value = mock_students
        
        # Call the function
        result = students.get_all_students()
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once_with(" SELECT * FROM Students\n                ")
        mock_cursor.fetchall.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertEqual(result, mock_students)
    
    @patch('controllers.students.get_db_connection')
    def test_add_student_success(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Call the function
        result = students.add_student(
            1600345, 
            'Sally', 
            'Smith', 
            'ssmith', 
            'secure_pass', 
            1, 
            None, 
            3409243
        )
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once_with(
            " INSERT INTO Students (id, f_name, l_name, username, password, major_id, graduation_date, advisor_id)\n                VALUES (?, ?, ?, ?, ?, ?, ?, ?) ", 
            (1600345, 'Sally', 'Smith', 'ssmith', 'secure_pass', 1, None, 3409243)
        )
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], "Student added successfully.")
    
    @patch('controllers.students.get_db_connection')
    def test_add_student_integrity_error(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Make execute throw an IntegrityError
        mock_conn.execute.side_effect = sqlite3.IntegrityError("UNIQUE constraint failed")
        
        # Call the function
        result = students.add_student(
            1600343,  # Using an ID that already exists
            'Sally', 
            'Smith', 
            'ssmith', 
            'secure_pass', 
            1, 
            None, 
            3409243
        )
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once()
        mock_conn.commit.assert_not_called()
        mock_conn.close.assert_called_once()
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], "Error adding student: UNIQUE constraint failed")
    
    @patch('controllers.students.get_db_connection')
    def test_update_student_all_fields(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Call the function
        result = students.update_student(
            1600343,
            f_name='Updated',
            l_name='Student',
            username='updated_user',
            password='new_password',
            major_id=2,
            graduation_date='2026-05-15',
            advisor_id=3409244
        )
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once()
        
        # Check that the query contains all field updates
        call_args = mock_conn.execute.call_args[0]
        query = call_args[0]
        self.assertIn("f_name = ?", query)
        self.assertIn("l_name = ?", query)
        self.assertIn("username = ?", query)
        self.assertIn("password = ?", query)
        self.assertIn("major = ?", query)  # Note: this field is named "major" in the SQL, not "major_id"
        self.assertIn("graduation_date = ?", query)
        self.assertIn("advisor_id = ?", query)
        
        # Check values passed to the query
        values = call_args[1]
        self.assertEqual(values[0], 'Updated')
        self.assertEqual(values[1], 'Student')
        self.assertEqual(values[2], 'updated_user')
        self.assertEqual(values[3], 'new_password')
        self.assertEqual(values[4], 2)
        self.assertEqual(values[5], '2026-05-15')
        self.assertEqual(values[6], 3409244)
        self.assertEqual(values[7], 1600343)  # ID should be the last parameter
        
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], "Student updated successfully.")
    
    @patch('controllers.students.get_db_connection')
    def test_update_student_some_fields(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Call the function with only some fields
        result = students.update_student(
            1600343,
            f_name='Updated',
            l_name='Student'
        )
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once()
        
        # Check that the query contains only the specified field updates
        call_args = mock_conn.execute.call_args[0]
        query = call_args[0]
        self.assertIn("f_name = ?", query)
        self.assertIn("l_name = ?", query)
        self.assertNotIn("username = ?", query)
        self.assertNotIn("password = ?", query)
        self.assertNotIn("major = ?", query)
        self.assertNotIn("graduation_date = ?", query)
        self.assertNotIn("advisor_id = ?", query)
        
        # Check values passed to the query
        values = call_args[1]
        self.assertEqual(values[0], 'Updated')
        self.assertEqual(values[1], 'Student')
        self.assertEqual(values[2], 1600343)  # ID should be the last parameter
        
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], "Student updated successfully.")
    
    @patch('controllers.students.get_db_connection')
    def test_update_student_no_fields(self, mock_get_conn):
        # Call the function with no fields to update
        result = students.update_student(1600343)
        
        # Assertions
        mock_get_conn.assert_not_called()  # Should not even connect to DB
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], "No fields to update.")
    
    @patch('controllers.students.get_db_connection')
    def test_update_student_error(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Make execute throw an SQLite error
        mock_conn.execute.side_effect = sqlite3.Error("Database error")
        
        # Call the function
        result = students.update_student(
            1600343,
            f_name='Updated'
        )
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once()
        mock_conn.commit.assert_not_called()
        mock_conn.close.assert_called_once()
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], "Error updating student: Database error")
    
    @patch('controllers.students.get_db_connection')
    def test_delete_student_success(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Call the function
        result = students.delete_student(1600343)
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once_with(
            " DELETE FROM Students\n                WHERE id = ? ", 
            (1600343,)
        )
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], "Student deleted successfully.")
    
    @patch('controllers.students.get_db_connection')
    def test_delete_student_error(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Make execute throw an SQLite error
        mock_conn.execute.side_effect = sqlite3.Error("Database error")
        
        # Call the function
        result = students.delete_student(1600343)
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once()
        mock_conn.commit.assert_not_called()
        mock_conn.close.assert_called_once()
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], "Error deleting student: Database error")

if __name__ == '__main__':
    unittest.main()