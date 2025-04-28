import unittest
from unittest.mock import patch, MagicMock
import sqlite3
import sys
import os

# Add parent directory to path to import the controllers
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from controllers import courses

class TestCoursesController(unittest.TestCase):
    
    @patch('controllers.courses.sqlite3.connect')
    def test_get_db_connection(self, mock_connect):
        # Set up the mock
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        
        # Call the function
        conn = courses.get_db_connection()
        
        # Assertions
        mock_connect.assert_called_once_with(courses.DB_NAME)
        self.assertEqual(conn, mock_conn)
        self.assertEqual(conn.row_factory, sqlite3.Row)
    
    @patch('controllers.courses.get_db_connection')
    def test_get_course(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Create mock cursor and result
        mock_cursor = MagicMock()
        mock_conn.execute.return_value = mock_cursor
        
        # Mock the course data
        mock_course = {
            'subject': 'ITSC',
            'number': 1212,
            'name': 'Introduction to Computer Science I',
            'credits': 4
        }
        mock_cursor.fetchone.return_value = mock_course
        
        # Call the function
        result = courses.get_course('ITSC', 1212)
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once_with(
            " SELECT * FROM Courses\n                WHERE subject = ? AND number = ?\n                LIMIT 1 ", 
            ('ITSC', 1212)
        )
        mock_cursor.fetchone.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertEqual(result, mock_course)
    
    @patch('controllers.courses.get_db_connection')
    def test_get_course_prereq(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Create mock cursor and result
        mock_cursor = MagicMock()
        mock_conn.execute.return_value = mock_cursor
        
        # Mock the prerequisites data
        mock_prereqs = [
            (0, 'ITSC', 1212),
            (1, 'MATH', 1241)
        ]
        mock_cursor.fetchall.return_value = mock_prereqs
        
        # Call the function
        result = courses.get_course_prereq('ITSC', 1213)
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once_with(
            " SELECT group_id, course_subject, course_number FROM Prerequisites\n                WHERE parent_subject = ? AND parent_number = ? ", 
            ('ITSC', 1213)
        )
        mock_cursor.fetchall.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertEqual(result, mock_prereqs)
    
    @patch('controllers.courses.get_db_connection')
    def test_get_all_courses(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Create mock cursor and result
        mock_cursor = MagicMock()
        mock_conn.execute.return_value = mock_cursor
        
        # Mock the courses data
        mock_courses = [
            {
                'subject': 'ITSC',
                'number': 1212,
                'name': 'Introduction to Computer Science I',
                'credits': 4
            },
            {
                'subject': 'ITSC',
                'number': 1213,
                'name': 'Introduction to Computer Science II',
                'credits': 4
            },
            {
                'subject': 'MATH',
                'number': 1241,
                'name': 'Calculus I',
                'credits': 3
            }
        ]
        mock_cursor.fetchall.return_value = mock_courses
        
        # Call the function
        result = courses.get_all_courses()
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once_with(" SELECT * FROM Courses ")
        mock_cursor.fetchall.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertEqual(result, mock_courses)
    
    @patch('controllers.courses.get_db_connection')
    def test_get_semester_courses(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Create mock cursor and result
        mock_cursor = MagicMock()
        mock_conn.execute.return_value = mock_cursor
        
        # Mock the semester courses data
        mock_semester_courses = [
            {
                'subject': 'ITSC',
                'number': 1212,
                'name': 'Introduction to Computer Science I',
                'credits': 4,
                'plan_id': 1,
                'semester_id': 1,
                'course_subject': 'ITSC',
                'course_number': 1212
            },
            {
                'subject': 'MATH',
                'number': 1241,
                'name': 'Calculus I',
                'credits': 3,
                'plan_id': 1,
                'semester_id': 1,
                'course_subject': 'MATH',
                'course_number': 1241
            }
        ]
        mock_cursor.fetchall.return_value = mock_semester_courses
        
        # Call the function
        result = courses.get_semester_courses(1, 1)
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once_with(
            " SELECT * FROM Courses c\n                JOIN Plan_Semester_Courses pcs\n                ON c.subject = pcs.course_subject AND c.number = pcs.course_number\n                WHERE pcs.semester_id = ? AND pcs.plan_id = ?\n                ORDER BY c.subject, c.number ", 
            (1, 1)
        )
        mock_cursor.fetchall.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertEqual(result, mock_semester_courses)
    
    @patch('controllers.courses.get_db_connection')
    def test_add_course_success(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Call the function
        result = courses.add_course('ITSC', 3000, 'New Test Course', 3)
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once_with(
            " INSERT INTO Courses (subject, number, name, credits)\n                VALUES (?, ?, ?, ?) ", 
            ('ITSC', 3000, 'New Test Course', 3)
        )
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], "Course added successfully.")
    
    @patch('controllers.courses.get_db_connection')
    def test_add_course_integrity_error(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Make execute throw an IntegrityError
        mock_conn.execute.side_effect = sqlite3.IntegrityError("UNIQUE constraint failed")
        
        # Call the function
        result = courses.add_course('ITSC', 1212, 'Duplicate Course', 4)
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once()
        mock_conn.commit.assert_not_called()
        mock_conn.close.assert_called_once()
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], "Error adding course: UNIQUE constraint failed")
    
    @patch('controllers.courses.get_db_connection')
    def test_update_course_all_fields(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Call the function
        result = courses.update_course(
            'ITSC', 
            1212, 
            name='Updated CS I Course', 
            credits=5
        )
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once()
        
        # Check that the query contains all field updates
        call_args = mock_conn.execute.call_args[0]
        query = call_args[0]
        self.assertIn("name = ?", query)
        self.assertIn("credits = ?", query)
        
        # Check values passed to the query
        values = call_args[1]
        self.assertEqual(values[0], 'Updated CS I Course')
        self.assertEqual(values[1], 5)
        self.assertEqual(values[2], 'ITSC')  # Subject should be the second-to-last parameter
        self.assertEqual(values[3], 1212)  # Number should be the last parameter
        
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], "Course updated successfully.")
    
    @patch('controllers.courses.get_db_connection')
    def test_update_course_name_only(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Call the function with only name field
        result = courses.update_course(
            'ITSC', 
            1212, 
            name='Updated CS I Course'
        )
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once()
        
        # Check that the query contains only name update
        call_args = mock_conn.execute.call_args[0]
        query = call_args[0]
        self.assertIn("name = ?", query)
        self.assertNotIn("credits = ?", query)
        
        # Check values passed to the query
        values = call_args[1]
        self.assertEqual(values[0], 'Updated CS I Course')
        self.assertEqual(values[1], 'ITSC')
        self.assertEqual(values[2], 1212)
        
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], "Course updated successfully.")
    
    @patch('controllers.courses.get_db_connection')
    def test_update_course_credits_only(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Call the function with only credits field
        result = courses.update_course(
            'ITSC', 
            1212, 
            credits=5
        )
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once()
        
        # Check that the query contains only credits update
        call_args = mock_conn.execute.call_args[0]
        query = call_args[0]
        self.assertNotIn("name = ?", query)
        self.assertIn("credits = ?", query)
        
        # Check values passed to the query
        values = call_args[1]
        self.assertEqual(values[0], 5)
        self.assertEqual(values[1], 'ITSC')
        self.assertEqual(values[2], 1212)
        
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], "Course updated successfully.")
    
    @patch('controllers.courses.get_db_connection')
    def test_update_course_no_fields(self, mock_get_conn):
        # Call the function with no fields to update
        result = courses.update_course('ITSC', 1212)
        
        # Assertions
        mock_get_conn.assert_not_called()  # Should not even connect to DB
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], "No fields to update.")
    
    @patch('controllers.courses.get_db_connection')
    def test_update_course_error(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Make execute throw an SQLite error
        mock_conn.execute.side_effect = sqlite3.Error("Database error")
        
        # Call the function
        result = courses.update_course(
            'ITSC', 
            1212, 
            name='Updated Course'
        )
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once()
        mock_conn.commit.assert_not_called()
        mock_conn.close.assert_called_once()
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], "Error updating course: Database error")
    
    @patch('controllers.courses.get_db_connection')
    def test_delete_course_success(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Call the function
        result = courses.delete_course('ITSC', 1212)
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once_with(
            " DELETE FROM Courses\n                WHERE subject = ? AND number = ? ", 
            ('ITSC', 1212)
        )
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], "Course deleted successfully.")
    
    @patch('controllers.courses.get_db_connection')
    def test_delete_course_error(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Make execute throw an SQLite error
        mock_conn.execute.side_effect = sqlite3.Error("Database error")
        
        # Call the function
        result = courses.delete_course('ITSC', 1212)
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once()
        mock_conn.commit.assert_not_called()
        mock_conn.close.assert_called_once()
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], "Error deleting course: Database error")

if __name__ == '__main__':
    unittest.main()