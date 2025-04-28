import unittest
from unittest.mock import patch, MagicMock
import sqlite3
import sys
import os

# Add parent directory to path to import the controllers
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from controllers import concentration

class TestConcentrationController(unittest.TestCase):
    
    @patch('controllers.concentration.sqlite3.connect')
    def test_get_db_connection(self, mock_connect):
        # Set up the mock
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        
        # Call the function
        conn = concentration.get_db_connection()
        
        # Assertions
        mock_connect.assert_called_once_with(concentration.DB_NAME)
        self.assertEqual(conn, mock_conn)
        self.assertEqual(conn.row_factory, sqlite3.Row)
    
    @patch('controllers.concentration.get_db_connection')
    def test_get_concentration(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Create mock cursor and result
        mock_cursor = MagicMock()
        mock_conn.execute.return_value = mock_cursor
        
        # Mock the concentration data
        mock_concentration = {
            'id': 1,
            'name': 'AI, Robotics, and Gaming, B.S.',
            'major_id': 1
        }
        mock_cursor.fetchone.return_value = mock_concentration
        
        # Call the function
        result = concentration.get_concentration(1)
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once_with(
            " SELECT * FROM Concentrations\n                WHERE id = ?\n                ", 
            (1,)
        )
        mock_cursor.fetchone.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertEqual(result, mock_concentration)

    @patch('controllers.concentration.get_db_connection')
    def test_get_concentration_id(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Create mock cursor and result
        mock_cursor = MagicMock()
        mock_conn.execute.return_value = mock_cursor
        
        # Mock the concentration data
        mock_concentration = {'id': 1}
        mock_cursor.fetchone.return_value = mock_concentration
        
        # Call the function
        result = concentration.get_concentration_id('AI, Robotics, and Gaming, B.S.')
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once_with(
            " SELECT id FROM Concentrations\n                WHERE name = ? ", 
            ('AI, Robotics, and Gaming, B.S.',)
        )
        mock_cursor.fetchone.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertEqual(result, 1)

    @patch('controllers.concentration.get_db_connection')
    def test_get_concentration_id_not_found(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Create mock cursor and result
        mock_cursor = MagicMock()
        mock_conn.execute.return_value = mock_cursor
        
        # Mock concentration not found
        mock_cursor.fetchone.return_value = None
        
        # Call the function
        result = concentration.get_concentration_id('Nonexistent Concentration')
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once()
        mock_cursor.fetchone.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertIsNone(result)

    @patch('controllers.concentration.get_db_connection')
    def test_get_concentrations_by_major(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Create mock cursor and result
        mock_cursor = MagicMock()
        mock_conn.execute.return_value = mock_cursor
        
        # Mock the concentrations data
        mock_concentrations = [
            {
                'id': 1,
                'name': 'AI, Robotics, and Gaming, B.S.',
                'major_id': 1
            },
            {
                'id': 2,
                'name': 'Data Science, B.S.',
                'major_id': 1
            }
        ]
        mock_cursor.fetchall.return_value = mock_concentrations
        
        # Call the function
        result = concentration.get_concentrations_by_major(1)
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once_with(
            " SELECT * FROM Concentrations\n                WHERE major_id = ? ", 
            (1,)
        )
        mock_cursor.fetchall.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertEqual(result, mock_concentrations)

    @patch('controllers.concentration.get_db_connection')
    def test_add_concentration_success(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Call the function
        result = concentration.add_concentration('New Concentration', 1)
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once_with(
            " INSERT INTO Concentrations (name, major_id)\n                VALUES (?, ?) ", 
            ('New Concentration', 1)
        )
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], "Concentration added successfully.")

    @patch('controllers.concentration.get_db_connection')
    def test_add_concentration_integrity_error(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Make execute throw an IntegrityError
        mock_conn.execute.side_effect = sqlite3.IntegrityError("UNIQUE constraint failed")
        
        # Call the function
        result = concentration.add_concentration('AI, Robotics, and Gaming, B.S.', 1)
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once()
        mock_conn.commit.assert_not_called()
        mock_conn.close.assert_called_once()
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], "Error adding concentration: UNIQUE constraint failed")

    @patch('controllers.concentration.get_db_connection')
    def test_update_concentration_all_fields(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Call the function
        result = concentration.update_concentration(
            1,
            name='Updated Concentration',
            major_id=2
        )
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once()
        
        # Check that the query contains all field updates
        call_args = mock_conn.execute.call_args[0]
        query = call_args[0]
        self.assertIn("name = ?", query)
        self.assertIn("major_id = ?", query)
        
        # Check values passed to the query
        values = call_args[1]
        self.assertEqual(values[0], 'Updated Concentration')
        self.assertEqual(values[1], 2)
        self.assertEqual(values[2], 1)  # ID should be the last parameter
        
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], "Concentration updated successfully.")

    @patch('controllers.concentration.get_db_connection')
    def test_update_concentration_name_only(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Call the function with only name field
        result = concentration.update_concentration(
            1,
            name='Updated Concentration'
        )
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once()
        
        # Check that the query contains only name update
        call_args = mock_conn.execute.call_args[0]
        query = call_args[0]
        self.assertIn("name = ?", query)
        self.assertNotIn("major_id = ?", query)
        
        # Check values passed to the query
        values = call_args[1]
        self.assertEqual(values[0], 'Updated Concentration')
        self.assertEqual(values[1], 1)  # ID should be the last parameter
        
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], "Concentration updated successfully.")

    @patch('controllers.concentration.get_db_connection')
    def test_update_concentration_major_id_only(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Call the function with only major_id field
        result = concentration.update_concentration(
            1,
            major_id=2
        )
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once()
        
        # Check that the query contains only major_id update
        call_args = mock_conn.execute.call_args[0]
        query = call_args[0]
        self.assertNotIn("name = ?", query)
        self.assertIn("major_id = ?", query)
        
        # Check values passed to the query
        values = call_args[1]
        self.assertEqual(values[0], 2)
        self.assertEqual(values[1], 1)  # ID should be the last parameter
        
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], "Concentration updated successfully.")

    @patch('controllers.concentration.get_db_connection')
    def test_update_concentration_no_fields(self, mock_get_conn):
        # Call the function with no fields to update
        result = concentration.update_concentration(1)
        
        # Assertions
        mock_get_conn.assert_not_called()  # Should not even connect to DB
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], "No fields to update.")

    @patch('controllers.concentration.get_db_connection')
    def test_update_concentration_error(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Make execute throw an SQLite error
        mock_conn.execute.side_effect = sqlite3.Error("Database error")
        
        # Call the function
        result = concentration.update_concentration(
            1,
            name='Updated Concentration'
        )
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once()
        mock_conn.commit.assert_not_called()
        mock_conn.close.assert_called_once()
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], "Error updating concentration: Database error")

    @patch('controllers.concentration.get_db_connection')
    def test_delete_concentration_success(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Call the function
        result = concentration.delete_concentration(1)
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once_with(
            " DELETE FROM Concentrations\n                WHERE id = ? ", 
            (1,)
        )
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], "Concentration deleted successfully.")

    @patch('controllers.concentration.get_db_connection')
    def test_delete_concentration_error(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Make execute throw an SQLite error
        mock_conn.execute.side_effect = sqlite3.Error("Database error")
        
        # Call the function
        result = concentration.delete_concentration(1)
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once()
        mock_conn.commit.assert_not_called()
        mock_conn.close.assert_called_once()
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], "Error deleting concentration: Database error")

if __name__ == '__main__':
    unittest.main()