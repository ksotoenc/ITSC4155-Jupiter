import unittest
from unittest.mock import patch, MagicMock
import sqlite3
import sys
import os

# Add parent directory to path to import the controllers
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from controllers import semesters

class TestSemestersController(unittest.TestCase):
    
    @patch('controllers.semesters.sqlite3.connect')
    def test_get_db_connection(self, mock_connect):
        # Set up the mock
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        
        # Call the function
        conn = semesters.get_db_connection()
        
        # Assertions
        mock_connect.assert_called_once_with(semesters.DB_NAME)
        self.assertEqual(conn, mock_conn)
        self.assertEqual(conn.row_factory, sqlite3.Row)
    
    @patch('controllers.semesters.get_db_connection')
    def test_get_semester(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Create mock cursor and result
        mock_cursor = MagicMock()
        mock_conn.execute.return_value = mock_cursor
        
        # Mock the semester data
        mock_semester = {
            'id': 1,
            'term': 'Fall',
            'year': 2025
        }
        mock_cursor.fetchone.return_value = mock_semester
        
        # Call the function
        result = semesters.get_semester('Fall', 2025)
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once_with(
            " SELECT * FROM Semesters\n                WHERE term = ? AND year = ? \n                LIMIT 1 ", 
            ('Fall', 2025)
        )
        mock_cursor.fetchone.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertEqual(result, mock_semester)
    
    @patch('controllers.semesters.get_db_connection')
    def test_get_semesters(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Create mock cursor and result
        mock_cursor = MagicMock()
        mock_conn.execute.return_value = mock_cursor
        
        # Mock the semesters data
        mock_semesters = [
            {
                'id': 1,
                'term': 'Fall',
                'year': 2025,
                'semester_id': 1,
                'plan_id': 1
            },
            {
                'id': 2,
                'term': 'Spring',
                'year': 2026,
                'semester_id': 2,
                'plan_id': 1
            }
        ]
        mock_cursor.fetchall.return_value = mock_semesters
        
        # Call the function
        result = semesters.get_semesters(1)
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once_with(
            " SELECT * FROM Semesters s\n                JOIN Plan_Semesters ps\n                ON s.id = ps.semester_id\n                WHERE ps.plan_id = ?\n                ORDER BY s.year, \n                    CASE \n                        WHEN s.term = 'Spring' THEN 1\n                        WHEN s.term = 'Summer' THEN 2\n                        WHEN s.term = 'Fall' THEN 3\n                    END", 
            (1,)
        )
        mock_cursor.fetchall.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertEqual(result, mock_semesters)
    
    @patch('controllers.semesters.get_db_connection')
    def test_get_all_semesters(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Create mock cursor and result
        mock_cursor = MagicMock()
        mock_conn.execute.return_value = mock_cursor
        
        # Mock the semesters data
        mock_semesters = [
            {
                'id': 1,
                'term': 'Fall',
                'year': 2025
            },
            {
                'id': 2,
                'term': 'Spring',
                'year': 2026
            },
            {
                'id': 3,
                'term': 'Fall',
                'year': 2026
            }
        ]
        mock_cursor.fetchall.return_value = mock_semesters
        
        # Call the function
        result = semesters.get_all_semesters()
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once_with(" SELECT * FROM Semesters ")
        mock_cursor.fetchall.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertEqual(result, mock_semesters)
    
    @patch('controllers.semesters.get_db_connection')
    def test_insert_to_plan_already_exists(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Create mock cursor and result
        mock_cursor = MagicMock()
        mock_conn.execute.return_value = mock_cursor
        
        # Mock the count result to indicate record exists
        mock_cursor.fetchone.return_value = [1]  # Count > 0
        
        # Call the function
        result = semesters.insert_to_plan(1, 1)
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once_with(
            " SELECT COUNT(*) FROM Plan_Semesters \n                      WHERE plan_id = ? AND semester_id = ? ", 
            (1, 1)
        )
        mock_cursor.fetchone.assert_called_once()
        mock_conn.commit.assert_not_called()  # Should not commit if already exists
        mock_conn.close.assert_called_once()
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], "Semester is already in this plan.")
    
    @patch('controllers.semesters.get_db_connection')
    def test_insert_to_plan_success(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Create mock cursor and results
        mock_cursor = MagicMock()
        mock_conn.execute.return_value = mock_cursor
        
        # Mock the count result to indicate record doesn't exist
        mock_cursor.fetchone.return_value = [0]  # Count = 0
        
        # Call the function
        result = semesters.insert_to_plan(1, 3)
        
        # Assertions
        mock_get_conn.assert_called_once()
        self.assertEqual(mock_conn.execute.call_count, 2)  # One for check, one for insert
        mock_cursor.fetchone.assert_called_once()
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], "Semester added to plan successfully.")
    
    @patch('controllers.semesters.get_db_connection')
    def test_insert_to_plan_error(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Create mock cursor
        mock_cursor = MagicMock()
        mock_conn.execute.return_value = mock_cursor
        
        # Mock the count result to indicate record doesn't exist
        mock_cursor.fetchone.return_value = [0]  # Count = 0
        
        # Make second execute call throw an error
        mock_conn.execute.side_effect = [mock_cursor, sqlite3.Error("Database error")]
        
        # Call the function
        result = semesters.insert_to_plan(1, 3)
        
        # Assertions
        mock_get_conn.assert_called_once()
        self.assertEqual(mock_conn.execute.call_count, 2)  # One for check, one for insert
        mock_cursor.fetchone.assert_called_once()
        mock_conn.commit.assert_not_called()
        mock_conn.close.assert_called_once()
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], "Error adding semester to plan: Database error")
    
    @patch('controllers.semesters.get_db_connection')
    def test_add_semester_success(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Call the function
        result = semesters.add_semester('Fall', 2027)
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once_with(
            " INSERT INTO Semesters (term, year)\n                VALUES (?, ?) ", 
            ('Fall', 2027)
        )
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], "Semester added successfully.")
    
    @patch('controllers.semesters.get_db_connection')
    def test_add_semester_integrity_error(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Make execute throw an IntegrityError
        mock_conn.execute.side_effect = sqlite3.IntegrityError("UNIQUE constraint failed")
        
        # Call the function
        result = semesters.add_semester('Fall', 2025)  # Semester that already exists
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once()
        mock_conn.commit.assert_not_called()
        mock_conn.close.assert_called_once()
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], "Error adding semester: UNIQUE constraint failed")
    
    @patch('controllers.semesters.get_db_connection')
    def test_update_semester_all_fields(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Call the function
        result = semesters.update_semester(
            1,
            term='Spring',
            year=2026
        )
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once()
        
        # Check that the query contains all field updates
        call_args = mock_conn.execute.call_args[0]
        query = call_args[0]
        self.assertIn("term = ?", query)
        self.assertIn("year = ?", query)
        
        # Check values passed to the query
        values = call_args[1]
        self.assertEqual(values[0], 'Spring')
        self.assertEqual(values[1], 2026)
        self.assertEqual(values[2], 1)  # ID should be the last parameter
        
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], "Semester updated successfully.")
    
    @patch('controllers.semesters.get_db_connection')
    def test_update_semester_term_only(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Call the function with only term field
        result = semesters.update_semester(
            1,
            term='Spring'
        )
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once()
        
        # Check that the query contains only term update
        call_args = mock_conn.execute.call_args[0]
        query = call_args[0]
        self.assertIn("term = ?", query)
        self.assertNotIn("year = ?", query)
        
        # Check values passed to the query
        values = call_args[1]
        self.assertEqual(values[0], 'Spring')
        self.assertEqual(values[1], 1)  # ID should be the last parameter
        
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], "Semester updated successfully.")
    
    @patch('controllers.semesters.get_db_connection')
    def test_update_semester_year_only(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Call the function with only year field
        result = semesters.update_semester(
            1,
            year=2026
        )
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once()
        
        # Check that the query contains only year update
        call_args = mock_conn.execute.call_args[0]
        query = call_args[0]
        self.assertNotIn("term = ?", query)
        self.assertIn("year = ?", query)
        
        # Check values passed to the query
        values = call_args[1]
        self.assertEqual(values[0], 2026)
        self.assertEqual(values[1], 1)  # ID should be the last parameter
        
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], "Semester updated successfully.")
    
    @patch('controllers.semesters.get_db_connection')
    def test_update_semester_no_fields(self, mock_get_conn):
        # Call the function with no fields to update
        result = semesters.update_semester(1)
        
        # Assertions
        mock_get_conn.assert_not_called()  # Should not even connect to DB
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], "No fields to update.")
    
    @patch('controllers.semesters.get_db_connection')
    def test_update_semester_error(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Make execute throw an SQLite error
        mock_conn.execute.side_effect = sqlite3.Error("Database error")
        
        # Call the function
        result = semesters.update_semester(
            1,
            term='Spring'
        )
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once()
        mock_conn.commit.assert_not_called()
        mock_conn.close.assert_called_once()
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], "Error updating semester: Database error")
    
    @patch('controllers.semesters.get_db_connection')
    def test_delete_semester_success(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Call the function
        result = semesters.delete_semester(1)
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once_with(
            " DELETE FROM Semesters\n                WHERE id = ? ", 
            (1,)
        )
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], "Semester deleted successfully.")
    
    @patch('controllers.semesters.get_db_connection')
    def test_delete_semester_error(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Make execute throw an SQLite error
        mock_conn.execute.side_effect = sqlite3.Error("Database error")
        
        # Call the function
        result = semesters.delete_semester(1)
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once()
        mock_conn.commit.assert_not_called()
        mock_conn.close.assert_called_once()
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], "Error deleting semester: Database error")

if __name__ == '__main__':
    unittest.main()