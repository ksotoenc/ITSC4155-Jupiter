import unittest
from unittest.mock import patch, MagicMock
import sqlite3
import sys
import os

# Add parent directory to path to import the controllers
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from controllers import plans

class TestPlansController(unittest.TestCase):
    
    @patch('controllers.plans.sqlite3.connect')
    def test_get_db_connection(self, mock_connect):
        # Set up the mock
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        
        # Call the function
        conn = plans.get_db_connection()
        
        # Assertions
        mock_connect.assert_called_once_with(plans.DB_NAME)
        self.assertEqual(conn, mock_conn)
        self.assertEqual(conn.row_factory, sqlite3.Row)
    
    @patch('controllers.plans.get_db_connection')
    def test_create_plan_success(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Mock cursor and its behavior
        mock_cursor = MagicMock()
        mock_cursor.lastrowid = 1  # Mock plan_id return value
        mock_conn.execute.return_value = mock_cursor
        
        # Call the function
        result = plans.create_plan(
            student_id=1600343,
            advisor_id=3409243,
            name="Test Degree Plan",
            major_id=1,
            concentration_id=1,
            start_term="Fall 2025"
        )
        
        # Assertions
        mock_get_conn.assert_called_once()
        self.assertGreater(mock_conn.execute.call_count, 1)  # At minimum, there should be more than 1 call
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertEqual(result, 1)  # Should return the plan_id (1)
    
    @patch('controllers.plans.get_db_connection')
    def test_create_plan_invalid_term_format(self, mock_get_conn):
        # Call the function with invalid term format
        result = plans.create_plan(
            student_id=1600343,
            advisor_id=3409243,
            name="Test Degree Plan",
            major_id=1,
            concentration_id=1,
            start_term="Fall2025"  # Invalid format - no space
        )
        
        # Assertions
        mock_get_conn.assert_not_called()  # Should not connect to DB
        self.assertFalse(result)  # Should return False
    
    @patch('controllers.plans.get_db_connection')
    def test_create_plan_db_error(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Make execute throw an SQLite error
        mock_conn.execute.side_effect = sqlite3.Error("Database error")
        
        # Call the function
        result = plans.create_plan(
            student_id=1600343,
            advisor_id=3409243,
            name="Test Degree Plan",
            major_id=1,
            concentration_id=1,
            start_term="Fall 2025"
        )
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once()
        mock_conn.rollback.assert_called_once()
        mock_conn.commit.assert_not_called()
        mock_conn.close.assert_called_once()
        self.assertFalse(result)  # Should return False
    
    @patch('controllers.plans.get_db_connection')
    def test_get_plan_student(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Create mock cursor and result
        mock_cursor = MagicMock()
        mock_conn.execute.return_value = mock_cursor
        
        # Mock the plan data
        mock_plan = {
            'id': 1,
            'name': 'Test Degree Plan',
            'num_semesters': 8,
            'student_id': 1600343,
            'advisor_id': 3409243,
            'major_id': 1,
            'concentration_id': 1
        }
        mock_cursor.fetchone.return_value = mock_plan
        
        # Call the function
        result = plans.get_plan('Test Degree Plan', 'student', 1600343)
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once_with(
            " SELECT * FROM Plans\n                    WHERE name = ? AND student_id = ?\n                    LIMIT 1 ", 
            ('Test Degree Plan', 1600343)
        )
        mock_cursor.fetchone.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertEqual(result, mock_plan)
    
    @patch('controllers.plans.get_db_connection')
    def test_get_plan_advisor(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Create mock cursor and result
        mock_cursor = MagicMock()
        mock_conn.execute.return_value = mock_cursor
        
        # Mock the plan data
        mock_plan = {
            'id': 1,
            'name': 'Test Degree Plan',
            'num_semesters': 8,
            'student_id': 1600343,
            'advisor_id': 3409243,
            'major_id': 1,
            'concentration_id': 1
        }
        mock_cursor.fetchone.return_value = mock_plan
        
        # Call the function
        result = plans.get_plan('Test Degree Plan', 'advisor', 3409243)
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once_with(
            " SELECT * FROM Plans\n                    WHERE name = ? AND advisor_id = ?\n                    LIMIT 1 ", 
            ('Test Degree Plan', 3409243)
        )
        mock_cursor.fetchone.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertEqual(result, mock_plan)
    
    @patch('controllers.plans.get_db_connection')
    def test_get_plan_from_id(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Create mock cursor and result
        mock_cursor = MagicMock()
        mock_conn.execute.return_value = mock_cursor
        
        # Mock the plan data
        mock_plan = {
            'id': 1,
            'name': 'Test Degree Plan',
            'num_semesters': 8,
            'student_id': 1600343,
            'advisor_id': 3409243,
            'major_id': 1,
            'concentration_id': 1
        }
        mock_cursor.fetchone.return_value = mock_plan
        
        # Call the function
        result = plans.get_plan_from_id(1)
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once_with(
            " SELECT * FROM Plans\n                WHERE id = ?\n                LIMIT 1\n                ", 
            (1,)
        )
        mock_cursor.fetchone.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertEqual(result, mock_plan)
    
    @patch('controllers.plans.get_db_connection')
    def test_get_first_plan(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Create mock cursor and result
        mock_cursor = MagicMock()
        mock_conn.execute.return_value = mock_cursor
        
        # Mock the plan data
        mock_plan = {
            'id': 1,
            'name': 'Test Degree Plan',
            'num_semesters': 8,
            'student_id': 1600343,
            'advisor_id': 3409243,
            'major_id': 1,
            'concentration_id': 1
        }
        mock_cursor.fetchone.return_value = mock_plan
        
        # Call the function
        result = plans.get_first_plan(1600343)
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once_with(
            " SELECT * FROM Plans\n                WHERE student_id = ?\n                LIMIT 1 ", 
            (1600343,)
        )
        mock_cursor.fetchone.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertEqual(result, mock_plan)
    
    @patch('controllers.plans.get_db_connection')
    def test_get_all_plans(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Create mock cursor and result
        mock_cursor = MagicMock()
        mock_conn.execute.return_value = mock_cursor
        
        # Mock the plans data
        mock_plans = [
            {
                'id': 1,
                'name': 'Test Degree Plan 1',
                'num_semesters': 8,
                'student_id': 1600343,
                'advisor_id': 3409243,
                'major_id': 1,
                'concentration_id': 1
            },
            {
                'id': 2,
                'name': 'Test Degree Plan 2',
                'num_semesters': 8,
                'student_id': 1600344,
                'advisor_id': 3409243,
                'major_id': 1,
                'concentration_id': 2
            }
        ]
        mock_cursor.fetchall.return_value = mock_plans
        
        # Call the function
        result = plans.get_all_plans()
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once_with(" SELECT * FROM Plans ")
        mock_cursor.fetchall.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertEqual(result, mock_plans)
    
    @patch('controllers.plans.get_db_connection')
    def test_get_plans_student(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Create mock cursor and result
        mock_cursor = MagicMock()
        mock_conn.execute.return_value = mock_cursor
        
        # Mock the plans data
        mock_plans = [
            {
                'id': 1,
                'name': 'Test Degree Plan 1',
                'num_semesters': 8,
                'student_id': 1600343,
                'advisor_id': 3409243,
                'major_id': 1,
                'concentration_id': 1
            },
            {
                'id': 3,
                'name': 'Test Degree Plan 3',
                'num_semesters': 8,
                'student_id': 1600343,
                'advisor_id': 3409243,
                'major_id': 1,
                'concentration_id': 3
            }
        ]
        mock_cursor.fetchall.return_value = mock_plans
        
        # Call the function
        result = plans.get_plans('student', 1600343)
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once_with(
            " SELECT * FROM Plans\n                    WHERE student_id = ?\n                    ", 
            (1600343,)
        )
        mock_cursor.fetchall.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertEqual(result, mock_plans)
    
    @patch('controllers.plans.get_db_connection')
    def test_get_plans_advisor(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Create mock cursor and result
        mock_cursor = MagicMock()
        mock_conn.execute.return_value = mock_cursor
        
        # Mock the plans data
        mock_plans = [
            {
                'id': 1,
                'name': 'Test Degree Plan 1',
                'num_semesters': 8,
                'student_id': 1600343,
                'advisor_id': 3409243,
                'major_id': 1,
                'concentration_id': 1
            },
            {
                'id': 2,
                'name': 'Test Degree Plan 2',
                'num_semesters': 8,
                'student_id': 1600344,
                'advisor_id': 3409243,
                'major_id': 1,
                'concentration_id': 2
            }
        ]
        mock_cursor.fetchall.return_value = mock_plans
        
        # Call the function
        result = plans.get_plans('advisor', 3409243)
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once_with(
            " SELECT * FROM Plans\n                    WHERE advisor_id = ?\n                ", 
            (3409243,)
        )
        mock_cursor.fetchall.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertEqual(result, mock_plans)
    
    @patch('controllers.plans.get_db_connection')
    def test_update_plan_all_fields(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Call the function
        result = plans.update_plan(
            plan_id=1,
            name='Updated Plan Name',
            num_semesters=6,
            student_id=1600344,
            advisor_id=3409244
        )
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once()
        
        # Check that the query contains all field updates
        call_args = mock_conn.execute.call_args[0]
        query = call_args[0]
        self.assertIn("name = ?", query)
        self.assertIn("num_semesters = ?", query)
        self.assertIn("student_id = ?", query)
        self.assertIn("advisor_id = ?", query)
        
        # Check values passed to the query
        values = call_args[1]
        self.assertEqual(values[0], 'Updated Plan Name')
        self.assertEqual(values[1], 6)
        self.assertEqual(values[2], 1600344)
        self.assertEqual(values[3], 3409244)
        self.assertEqual(values[4], 1)  # plan_id should be the last parameter
        
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], "Plan updated successfully.")
    
    @patch('controllers.plans.get_db_connection')
    def test_update_plan_partial_fields(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Call the function with only some fields
        result = plans.update_plan(
            plan_id=1,
            name='Updated Plan Name'
        )
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once()
        
        # Check that the query contains only the name update
        call_args = mock_conn.execute.call_args[0]
        query = call_args[0]
        self.assertIn("name = ?", query)
        self.assertNotIn("num_semesters = ?", query)
        self.assertNotIn("student_id = ?", query)
        self.assertNotIn("advisor_id = ?", query)
        
        # Check values passed to the query
        values = call_args[1]
        self.assertEqual(values[0], 'Updated Plan Name')
        self.assertEqual(values[1], 1)  # plan_id should be the last parameter
        
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], "Plan updated successfully.")
    
    @patch('controllers.plans.get_db_connection')
    def test_update_plan_no_fields(self, mock_get_conn):
        # Call the function with no fields to update
        result = plans.update_plan(1)
        
        # Assertions
        mock_get_conn.assert_not_called()  # Should not even connect to DB
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], "No fields to update.")
    
    @patch('controllers.plans.get_db_connection')
    def test_update_plan_error(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Make execute throw an SQLite error
        mock_conn.execute.side_effect = sqlite3.Error("Database error")
        
        # Call the function
        result = plans.update_plan(
            plan_id=1,
            name='Updated Plan Name'
        )
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once()
        mock_conn.commit.assert_not_called()
        mock_conn.close.assert_called_once()
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], "Error updating plan: Database error")
    
    @patch('controllers.plans.get_db_connection')
    def test_delete_plan_success(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Call the function
        result = plans.delete_plan(1)
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once_with(
            " DELETE FROM Plans\n                WHERE id = ? ", 
            (1,)
        )
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], "Plan deleted successfully.")
    
    @patch('controllers.plans.get_db_connection')
    def test_delete_plan_error(self, mock_get_conn):
        # Set up mocks
        mock_conn = MagicMock()
        mock_get_conn.return_value = mock_conn
        
        # Make execute throw an SQLite error
        mock_conn.execute.side_effect = sqlite3.Error("Database error")
        
        # Call the function
        result = plans.delete_plan(1)
        
        # Assertions
        mock_get_conn.assert_called_once()
        mock_conn.execute.assert_called_once()
        mock_conn.commit.assert_not_called()
        mock_conn.close.assert_called_once()
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], "Error deleting plan: Database error")

if __name__ == '__main__':
    unittest.main()