import unittest
from unittest.mock import patch, MagicMock
import sqlite3
import sys
import os

# Add parent directory to path to import the controllers
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from controllers import majors

class TestMajorsController(unittest.TestCase):
    
    @patch('controllers.majors.sqlite3.connect')
    def test_get_db_connection(self, mock_connect):
        # Set up the mock
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        
        # Call the function
        conn = majors.get_db_connection()
        
        # Assertions
        mock_connect.assert_called_once_with(majors.DB_NAME)
        self.assertEqual(conn, mock_conn)
        self.assertEqual(conn.row_factory, sqlite3.Row)
    
    @patch('controllers.majors.get_db_connection')
    def test_get_major(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Create mock cursor and result
        mock_cursor = MagicMock()
        mock_conn.execute.return_value = mock_cursor
        
        # Mock the major data
        mock_major = {
            'id': 1,
            'name': 'Computer Science',
            'department': 'College of Computing and Informatics'
        }
        mock_cursor.fetchone.return_value = mock_major
        
        # Call the function
        result = majors.get_major(1)
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once_with(
            " SELECT * FROM Majors\n                WHERE id = ?\n                ", 
            (1,)
        )
        mock_cursor.fetchone.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertEqual(result, mock_major)
    
    @patch('controllers.majors.get_db_connection')
    def test_get_major_id(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Create mock cursor and result
        mock_cursor = MagicMock()
        mock_conn.execute.return_value = mock_cursor
        
        # Mock the major ID result
        mock_major = {'id': 1}
        mock_cursor.fetchone.return_value = mock_major
        
        # Call the function
        result = majors.get_major_id('Computer Science')
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once_with(
            " SELECT id FROM Majors\n                WHERE name = ? ", 
            ('Computer Science',)
        )
        mock_cursor.fetchone.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertEqual(result, 1)
    
    @patch('controllers.majors.get_db_connection')
    def test_get_major_id_not_found(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Create mock cursor and result
        mock_cursor = MagicMock()
        mock_conn.execute.return_value = mock_cursor
        
        # Mock major not found
        mock_cursor.fetchone.return_value = None
        
        # Call the function
        result = majors.get_major_id('Nonexistent Major')
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once()
        mock_cursor.fetchone.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertIsNone(result)
    
    @patch('controllers.majors.get_db_connection')
    def test_get_all_majors(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Create mock cursor and result
        mock_cursor = MagicMock()
        mock_conn.execute.return_value = mock_cursor
        
        # Mock the majors data
        mock_majors = [
            {
                'id': 1,
                'name': 'Computer Science',
                'department': 'College of Computing and Informatics'
            },
            {
                'id': 2,
                'name': 'Data Science',
                'department': 'College of Computing and Informatics'
            }
        ]
        mock_cursor.fetchall.return_value = mock_majors
        
        # Call the function
        result = majors.get_all_majors()
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once_with(" SELECT * FROM Majors ")
        mock_cursor.fetchall.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertEqual(result, mock_majors)
    
    @patch('controllers.majors.get_db_connection')
    def test_add_major_success(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Call the function
        result = majors.add_major(
            'Software Engineering', 
            'College of Computing and Informatics'
        )
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once_with(
            " INSERT INTO Majors (name, department)\n                VALUES (?, ?) ", 
            ('Software Engineering', 'College of Computing and Informatics')
        )
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], "Major added successfully.")
    
    @patch('controllers.majors.get_db_connection')
    def test_add_major_integrity_error(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Make execute throw an IntegrityError
        mock_conn.execute.side_effect = sqlite3.IntegrityError("UNIQUE constraint failed")
        
        # Call the function
        result = majors.add_major(
            'Computer Science',  # Using a name that already exists
            'College of Computing and Informatics'
        )
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once()
        mock_conn.commit.assert_not_called()
        mock_conn.close.assert_called_once()
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], "Error adding major: UNIQUE constraint failed")
    
    @patch('controllers.majors.get_db_connection')
    def test_update_major_all_fields(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Call the function
        result = majors.update_major(
            1,
            name='Updated Computer Science',
            department='Updated Department'
        )
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once()
        
        # Check that the query contains all field updates
        call_args = mock_conn.execute.call_args[0]
        query = call_args[0]
        self.assertIn("name = ?", query)
        self.assertIn("department = ?", query)
        
        # Check values passed to the query
        values = call_args[1]
        self.assertEqual(values[0], 'Updated Computer Science')
        self.assertEqual(values[1], 'Updated Department')
        self.assertEqual(values[2], 1)  # ID should be the last parameter
        
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], "Major updated successfully.")
    
    @patch('controllers.majors.get_db_connection')
    def test_update_major_name_only(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Call the function with only name field
        result = majors.update_major(
            1,
            name='Updated Computer Science'
        )
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once()
        
        # Check that the query contains only name update
        call_args = mock_conn.execute.call_args[0]
        query = call_args[0]
        self.assertIn("name = ?", query)
        self.assertNotIn("department = ?", query)
        
        # Check values passed to the query
        values = call_args[1]
        self.assertEqual(values[0], 'Updated Computer Science')
        self.assertEqual(values[1], 1)  # ID should be the last parameter
        
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], "Major updated successfully.")
    
    @patch('controllers.majors.get_db_connection')
    def test_update_major_department_only(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Call the function with only department field
        result = majors.update_major(
            1,
            department='Updated Department'
        )
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once()
        
        # Check that the query contains only department update
        call_args = mock_conn.execute.call_args[0]
        query = call_args[0]
        self.assertNotIn("name = ?", query)
        self.assertIn("department = ?", query)
        
        # Check values passed to the query
        values = call_args[1]
        self.assertEqual(values[0], 'Updated Department')
        self.assertEqual(values[1], 1)  # ID should be the last parameter
        
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], "Major updated successfully.")
    
    @patch('controllers.majors.get_db_connection')
    def test_update_major_no_fields(self, mock_get_conn):
        # Call the function with no fields to update
        result = majors.update_major(1)
        
        # Assertions
        mock_get_conn.assert_not_called()  # Should not even connect to DB
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], "No fields to update.")
    
    @patch('controllers.majors.get_db_connection')
    def test_update_major_error(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Make execute throw an SQLite error
        mock_conn.execute.side_effect = sqlite3.Error("Database error")
        
        # Call the function
        result = majors.update_major(
            1,
            name='Updated Major'
        )
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once()
        mock_conn.commit.assert_not_called()
        mock_conn.close.assert_called_once()
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], "Error updating major: Database error")
    
    @patch('controllers.majors.get_db_connection')
    def test_delete_major_success(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Call the function
        result = majors.delete_major(1)
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once_with(
            " DELETE FROM Majors\n                WHERE id = ? ", 
            (1,)
        )
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], "Major deleted successfully.")
    
    @patch('controllers.majors.get_db_connection')
    def test_delete_major_error(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Make execute throw an SQLite error
        mock_conn.execute.side_effect = sqlite3.Error("Database error")
        
        # Call the function
        result = majors.delete_major(1)
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once()
        mock_conn.commit.assert_not_called()
        mock_conn.close.assert_called_once()
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], "Error deleting major: Database error")

if __name__ == '__main__':
    unittest.main()