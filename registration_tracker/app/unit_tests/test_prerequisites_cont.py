import unittest
from unittest.mock import patch, MagicMock
import sqlite3
import sys
import os

# Add parent directory to path to import the controllers
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from controllers import prerequisites

class TestPrerequisitesController(unittest.TestCase):
    
    @patch('controllers.prerequisites.sqlite3.connect')
    def test_get_db_connection(self, mock_connect):
        # Set up the mock
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        
        # Call the function
        conn = prerequisites.get_db_connection()
        
        # Assertions
        mock_connect.assert_called_once_with(prerequisites.DB_NAME)
        self.assertEqual(conn, mock_conn)
        self.assertEqual(conn.row_factory, sqlite3.Row)
    
    @patch('controllers.prerequisites.get_db_connection')
    def test_get_prereq(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Create mock cursor and result
        mock_cursor = MagicMock()
        mock_conn.execute.return_value = mock_cursor
        
        # Mock the prerequisites data
        mock_prereqs = [
            {
                'parent_subject': 'ITSC', 
                'parent_number': 1213,
                'group_id': 0,
                'course_subject': 'ITSC',
                'course_number': 1212,
                'subject': 'ITSC',
                'number': 1212,
                'name': 'Introduction to Computer Science I',
                'credits': 4
            },
            {
                'parent_subject': 'ITSC', 
                'parent_number': 1213,
                'group_id': 1,
                'course_subject': 'MATH',
                'course_number': 1241,
                'subject': 'MATH',
                'number': 1241,
                'name': 'Calculus I',
                'credits': 3
            }
        ]
        mock_cursor.fetchall.return_value = mock_prereqs
        
        # Call the function
        result = prerequisites.get_prereq('ITSC', 1213)
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once_with(
            " SELECT * FROM Prerequisites p\n                JOIN Courses c\n                ON p.course_subject = c.subject AND p.course_number = c.number\n                WHERE parent_subject = ? AND parent_number = ? ", 
            ('ITSC', 1213)
        )
        mock_cursor.fetchall.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertEqual(result, mock_prereqs)
    
    @patch('controllers.prerequisites.get_db_connection')
    def test_get_all_prereqs(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Create mock cursor and result
        mock_cursor = MagicMock()
        mock_conn.execute.return_value = mock_cursor
        
        # Mock the prerequisites data
        mock_prereqs = [
            {
                'parent_subject': 'ITSC', 
                'parent_number': 1213,
                'group_id': 0,
                'course_subject': 'ITSC',
                'course_number': 1212
            },
            {
                'parent_subject': 'ITSC', 
                'parent_number': 1213,
                'group_id': 1,
                'course_subject': 'MATH',
                'course_number': 1241
            },
            {
                'parent_subject': 'ITSC', 
                'parent_number': 2214,
                'group_id': 0,
                'course_subject': 'ITSC',
                'course_number': 1213
            }
        ]
        mock_cursor.fetchall.return_value = mock_prereqs
        
        # Call the function
        result = prerequisites.get_all_prereqs()
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once_with(" SELECT * FROM Prerequisites ")
        mock_cursor.fetchall.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertEqual(result, mock_prereqs)
    
    @patch('controllers.prerequisites.get_db_connection')
    def test_add_prereq_success(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Call the function
        result = prerequisites.add_prereq(
            'ITSC', 
            3155, 
            0, 
            'ITSC', 
            2214
        )
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once_with(
            " INSERT INTO Prerequisites (parent_subject, parent_number, group_id, course_subject, course_number)\n                VALUES (?, ?, ?, ?, ?) ", 
            ('ITSC', 3155, 0, 'ITSC', 2214)
        )
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], "Prerequisite added successfully.")
    
    @patch('controllers.prerequisites.get_db_connection')
    def test_add_prereq_integrity_error(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Make execute throw an IntegrityError
        mock_conn.execute.side_effect = sqlite3.IntegrityError("FOREIGN KEY constraint failed")
        
        # Call the function
        result = prerequisites.add_prereq(
            'ITSC', 
            3155, 
            0, 
            'NONEXISTENT', 
            9999
        )
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once()
        mock_conn.commit.assert_not_called()
        mock_conn.close.assert_called_once()
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], "Error adding prerequisite: FOREIGN KEY constraint failed")
    
    @patch('controllers.prerequisites.get_db_connection')
    def test_update_prereq_all_fields(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Call the function
        result = prerequisites.update_prereq(
            'ITSC',
            3155,
            0,
            course_subject='MATH',
            course_number=1241
        )
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once()
        
        # Check that the query contains all field updates
        call_args = mock_conn.execute.call_args[0]
        query = call_args[0]
        self.assertIn("course_subject = ?", query)
        self.assertIn("course_number = ?", query)
        
        # Check values passed to the query
        values = call_args[1]
        self.assertEqual(values[0], 'MATH')
        self.assertEqual(values[1], 1241)
        self.assertEqual(values[2], 'ITSC')
        self.assertEqual(values[3], 3155)
        self.assertEqual(values[4], 0)
        
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], "Prerequisite updated successfully.")
    
    @patch('controllers.prerequisites.get_db_connection')
    def test_update_prereq_subject_only(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Call the function with only course_subject
        result = prerequisites.update_prereq(
            'ITSC',
            3155,
            0,
            course_subject='MATH'
        )
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once()
        
        # Check that the query contains only course_subject update
        call_args = mock_conn.execute.call_args[0]
        query = call_args[0]
        self.assertIn("course_subject = ?", query)
        self.assertNotIn("course_number = ?", query)
        
        # Check values passed to the query
        values = call_args[1]
        self.assertEqual(values[0], 'MATH')
        self.assertEqual(values[1], 'ITSC')
        self.assertEqual(values[2], 3155)
        self.assertEqual(values[3], 0)
        
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], "Prerequisite updated successfully.")
    
    @patch('controllers.prerequisites.get_db_connection')
    def test_update_prereq_number_only(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Call the function with only course_number
        result = prerequisites.update_prereq(
            'ITSC',
            3155,
            0,
            course_number=1241
        )
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once()
        
        # Check that the query contains only course_number update
        call_args = mock_conn.execute.call_args[0]
        query = call_args[0]
        self.assertNotIn("course_subject = ?", query)
        self.assertIn("course_number = ?", query)
        
        # Check values passed to the query
        values = call_args[1]
        self.assertEqual(values[0], 1241)
        self.assertEqual(values[1], 'ITSC')
        self.assertEqual(values[2], 3155)
        self.assertEqual(values[3], 0)
        
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], "Prerequisite updated successfully.")
    
    @patch('controllers.prerequisites.get_db_connection')
    def test_update_prereq_no_fields(self, mock_get_conn):
        # Call the function with no fields to update
        result = prerequisites.update_prereq('ITSC', 3155, 0)
        
        # Assertions
        mock_get_conn.assert_not_called()  # Should not even connect to DB
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], "No fields to update.")
    
    @patch('controllers.prerequisites.get_db_connection')
    def test_update_prereq_error(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Make execute throw an SQLite error
        mock_conn.execute.side_effect = sqlite3.Error("Database error")
        
        # Call the function
        result = prerequisites.update_prereq(
            'ITSC',
            3155,
            0,
            course_subject='MATH'
        )
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once()
        mock_conn.commit.assert_not_called()
        mock_conn.close.assert_called_once()
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], "Error updating prerequisite: Database error")
    
    @patch('controllers.prerequisites.get_db_connection')
    def test_delete_prereq_success(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Call the function
        result = prerequisites.delete_prereq('ITSC', 3155, 0)
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once_with(
            " DELETE FROM Prerequisites\n                WHERE parent_subject = ? AND parent_number = ? AND group_id = ? ", 
            ('ITSC', 3155, 0)
        )
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], "Prerequisite deleted successfully.")
    
    @patch('controllers.prerequisites.get_db_connection')
    def test_delete_prereq_error(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Make execute throw an SQLite error
        mock_conn.execute.side_effect = sqlite3.Error("Database error")
        
        # Call the function
        result = prerequisites.delete_prereq('ITSC', 3155, 0)
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once()
        mock_conn.commit.assert_not_called()
        mock_conn.close.assert_called_once()
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], "Error deleting prerequisite: Database error")

if __name__ == '__main__':
    unittest.main()