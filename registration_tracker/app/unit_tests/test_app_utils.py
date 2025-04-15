import unittest
from unittest.mock import patch, MagicMock
import sqlite3
import app_utils

class TestAppUtilsSimple(unittest.TestCase):
    
    def test_get_db_connection(self):
        # Test that get_db_connection connects to the correct database and sets row_factory
        with patch('sqlite3.connect') as mock_connect:
            # Setup mock
            mock_conn = MagicMock()
            mock_connect.return_value = mock_conn
            
            # Call the function
            conn = app_utils.get_db_connection()
            
            # Verify connect was called with correct DB name
            mock_connect.assert_called_once_with(app_utils.DB_NAME)
            
            # Verify row_factory was set
            self.assertEqual(conn.row_factory, sqlite3.Row)

if __name__ == '__main__':
    unittest.main()