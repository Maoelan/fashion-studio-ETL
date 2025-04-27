import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from utils.load_data.load_postgre import load_to_postgres

class TestLoadPostgre(unittest.TestCase):

    @patch("utils.load_data.load_postgre.psycopg2.connect")
    def test_load_to_postgres_success(self, mock_connect):
        # Menguji apakah data berhasil dimasukkan ke PostgreSQL dengan koneksi yang valid
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        data = {
            "title": ["Product A"],
            "price": [160000],
            "rating": [4.5],
            "colors": [3],
            "size": ["M"],
            "gender": ["Unisex"],
            "timestamp": ["2024-03-17 12:00:00"]
        }
        df = pd.DataFrame(data)

        load_to_postgres(df, table_name="products_test")

        mock_connect.assert_called_once()
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called()
        assert mock_conn.commit.call_count == 1
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch("utils.load_data.load_postgre.psycopg2.connect", side_effect=Exception("Database connection error"))
    def test_load_to_postgres_connection_error(self, mock_connect):
        # Menguji apakah function menangani kesalahan koneksi ke PostgreSQL
        data = {
            "title": ["Product B"],
            "price": [200000],
            "rating": [4.2],
            "colors": [2],
            "size": ["L"],
            "gender": ["Male"],
            "timestamp": ["2024-03-17 12:30:00"]
        }
        df = pd.DataFrame(data)

        with self.assertLogs(level="ERROR") as log:
            load_to_postgres(df, table_name="products_test")

        self.assertTrue(any("Database connection error" in message for message in log.output))

    @patch("utils.load_data.load_postgre.psycopg2.connect")
    def test_load_to_postgres_empty_dataframe(self, mock_connect):
        # Menguji apakah function menangani dataframe kosong dengan benar
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        
        df = pd.DataFrame()
        
        with self.assertLogs(level="WARNING") as log:
            load_to_postgres(df, table_name="products_test")
        
        self.assertTrue(any("Tidak terdapat data untuk dimasukkan ke PostgreSQL" in message for message in log.output))

if __name__ == "__main__":
    unittest.main()