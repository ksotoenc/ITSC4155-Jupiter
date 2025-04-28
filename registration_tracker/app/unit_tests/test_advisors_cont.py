import unittest
from unittest.mock import patch, MagicMock
import sqlite3
import sys
import os

# Add parent directory to path to import the controllers
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from controllers import advisors

class TestAdvisorsController(unittest.TestCase):
    
    @patch('controllers.advisors.sqlite3.connect')
    def test_get_db_connection(self, mock_connect):
        # Set up the mock
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        
        # Call the function
        conn = advisors.get_db_connection()
        
        # Assertions
        mock_connect.assert_called_once_with(advisors.DB_NAME)
        self.assertEqual(conn, mock_conn)
        self.assertEqual(conn.row_factory, sqlite3.Row)
    
    @patch('controllers.advisors.get_db_connection')
    def test_get_advisor(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Create mock cursor and result
        mock_cursor = MagicMock()
        mock_conn.execute.return_value = mock_cursor
        
        # Mock the advisor data
        mock_advisor = {
            'id': 3409243,
            'username': 'adv_username',
            'password': 'adv_passw0rd',
            'f_name': 'Barry',
            'l_name': 'Benson'
        }
        mock_cursor.fetchone.return_value = mock_advisor
        
        # Call the function
        result = advisors.get_advisor(3409243)
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once_with(
            " SELECT * FROM Advisors\n                WHERE id = ?\n                LIMIT 1 ", 
            (3409243,)
        )
        mock_cursor.fetchone.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertEqual(result, mock_advisor)
    
    @patch('controllers.advisors.get_db_connection')
    def test_get_advisor_user(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Create mock cursor and result
        mock_cursor = MagicMock()
        mock_conn.execute.return_value = mock_cursor
        
        # Mock the advisor ID
        mock_advisor = {'id': 3409243}
        mock_cursor.fetchone.return_value = mock_advisor
        
        # Call the function
        result = advisors.get_advisor_user('adv_username')
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once_with(
            " SELECT id FROM Advisors\n                WHERE username = ?\n                LIMIT 1 ", 
            ('adv_username',)
        )
        mock_cursor.fetchone.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertEqual(result, mock_advisor)
    
    @patch('controllers.advisors.get_db_connection')
    def test_get_all_advisors(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Create mock cursor and result
        mock_cursor = MagicMock()
        mock_conn.execute.return_value = mock_cursor
        
        # Mock the advisors data
        mock_advisors = [
            {
                'id': 3409243,
                'username': 'adv_username',
                'password': 'adv_passw0rd',
                'f_name': 'Barry',
                'l_name': 'Benson'
            },
            {
                'id': 3409244,
                'username': 'adv_username2',
                'password': 'adv_passw0rd2',
                'f_name': 'Larry',
                'l_name': 'Johnson'
            }
        ]
        mock_cursor.fetchall.return_value = mock_advisors
        
        # Call the function
        result = advisors.get_all_advisors()
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once_with(" SELECT * FROM Advisors\n                ")
        mock_cursor.fetchall.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertEqual(result, mock_advisors)
    
    @patch('controllers.advisors.get_db_connection')
    def test_add_advisor_success(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Call the function
        result = advisors.add_advisor(
            3409245, 
            'new_advisor', 
            'secure_password', 
            'Jane', 
            'Smith'
        )
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once_with(
            " INSERT INTO Advisors (id, username, password, f_name, l_name)\n                VALUES (?, ?, ?, ?, ?) ", 
            (3409245, 'new_advisor', 'secure_password', 'Jane', 'Smith')
        )
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], "Advisor added successfully.")
    
    @patch('controllers.advisors.get_db_connection')
    def test_add_advisor_integrity_error(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Make execute throw an IntegrityError
        mock_conn.execute.side_effect = sqlite3.IntegrityError("UNIQUE constraint failed")
        
        # Call the function
        result = advisors.add_advisor(
            3409243,  # Using an ID that already exists
            'adv_username', 
            'secure_password', 
            'Jane', 
            'Smith'
        )
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once()
        mock_conn.commit.assert_not_called()
        mock_conn.close.assert_called_once()
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], "Error adding advisor: UNIQUE constraint failed")
    
    @patch('controllers.advisors.get_db_connection')
    def test_update_advisor_all_fields(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Call the function
        result = advisors.update_advisor(
            3409243,
            username='updated_username',
            password='new_password',
            f_name='Updated',
            l_name='Name'
        )
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once()
        # Check that the query contains all field updates
        call_args = mock_conn.execute.call_args[0]
        query = call_args[0]
        self.assertIn("username = ?", query)
        self.assertIn("password = ?", query)
        self.assertIn("f_name = ?", query)
        self.assertIn("l_name = ?", query)
        
        # Check values passed to the query
        values = call_args[1]
        self.assertEqual(values[0], 'updated_username')
        self.assertEqual(values[1], 'new_password')
        self.assertEqual(values[2], 'Updated')
        self.assertEqual(values[3], 'Name')
        self.assertEqual(values[4], 3409243)  # ID should be the last parameter
        
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], "Advisor updated successfully.")
    
    @patch('controllers.advisors.get_db_connection')
    def test_update_advisor_single_field(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Call the function with only one field
        result = advisors.update_advisor(
            3409243,
            username='updated_username'
        )
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once()
        
        # Check that the query contains only username update
        call_args = mock_conn.execute.call_args[0]
        query = call_args[0]
        self.assertIn("username = ?", query)
        self.assertNotIn("password = ?", query)
        self.assertNotIn("f_name = ?", query)
        self.assertNotIn("l_name = ?", query)
        
        # Check values passed to the query
        values = call_args[1]
        self.assertEqual(values[0], 'updated_username')
        self.assertEqual(values[1], 3409243)  # ID should be the last parameter
        
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], "Advisor updated successfully.")
    
    @patch('controllers.advisors.get_db_connection')
    def test_update_advisor_no_fields(self, mock_get_conn):
        # Call the function with no fields to update
        result = advisors.update_advisor(3409243)
        
        # Assertions
        mock_get_conn.assert_not_called()  # Should not even connect to DB
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], "No fields to update.")
    
    @patch('controllers.advisors.get_db_connection')
    def test_update_advisor_error(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Make execute throw an SQLite error
        mock_conn.execute.side_effect = sqlite3.Error("Database error")
        
        # Call the function
        result = advisors.update_advisor(
            3409243,
            username='updated_username'
        )
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once()
        mock_conn.commit.assert_not_called()
        mock_conn.close.assert_called_once()
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], "Error updating advisor: Database error")
    
    @patch('controllers.advisors.get_db_connection')
    def test_delete_advisor_success(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Call the function
        result = advisors.delete_advisor(3409243)
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once_with(
            " DELETE FROM Advisors\n                WHERE id = ? ", 
            (3409243,)
        )
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], "Advisor deleted successfully.")
    
    @patch('controllers.advisors.get_db_connection')
    def test_delete_advisor_error(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Make execute throw an SQLite error
        mock_conn.execute.side_effect = sqlite3.Error("Database error")
        
        # Call the function
        result = advisors.delete_advisor(3409243)
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once()
        mock_conn.commit.assert_not_called()
        mock_conn.close.assert_called_once()
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], "Error deleting advisor: Database error")

if __name__ == '__main__':
    unittest.main()