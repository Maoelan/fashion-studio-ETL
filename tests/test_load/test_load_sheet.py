import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from utils.load_data.load_sheet import load_to_google_sheets

class TestLoadSheet(unittest.TestCase):

    @patch("utils.load_data.load_sheet.service_account.Credentials.from_service_account_file")
    @patch("utils.load_data.load_sheet.build")
    def test_load_to_google_sheets_success(self, mock_build, mock_creds):
        """Menguji apakah data berhasil diupload ke Google Sheets"""
        mock_creds.return_value = MagicMock()

        mock_service = MagicMock()
        mock_sheets = MagicMock()
        mock_build.return_value.spreadsheets.return_value = mock_sheets

        mock_sheets.values().update.return_value.execute.return_value = {"status": "OK"}

        data = {
            "Title": ["Product A"],
            "Price": [160000],
            "Rating": [4.5],
            "Colors": [3],
            "Size": ["M"],
            "Gender": ["Unisex"]
        }
        df = pd.DataFrame(data)

        load_to_google_sheets(df)

        mock_sheets.values().update.assert_called_once()

    @patch("utils.load_data.load_sheet.service_account.Credentials.from_service_account_file")
    @patch("utils.load_data.load_sheet.build")
    def test_load_to_google_sheets_api_error(self, mock_build, mock_creds):
        """Menguji apakah function menangani error API dengan baik"""
        mock_creds.return_value = MagicMock()

        mock_service = MagicMock()
        mock_sheets = MagicMock()
        mock_build.return_value.spreadsheets.return_value = mock_sheets
        mock_sheets.values().update.side_effect = Exception("Google API Error")

        data = {
            "Title": ["Product B"],
            "Price": [200000],
            "Rating": [4.2],
            "Colors": [2],
            "Size": ["L"],
            "Gender": ["Male"]
        }
        df = pd.DataFrame(data)

        with self.assertLogs(level="ERROR") as log:
            load_to_google_sheets(df)

        self.assertTrue(any("Google API Error" in message for message in log.output))

    @patch("utils.load_data.load_sheet.service_account.Credentials.from_service_account_file")
    @patch("utils.load_data.load_sheet.build")
    def test_load_to_google_sheets_empty_dataframe(self, mock_build, mock_creds):
        """Menguji apakah function menangani dataframe kosong dengan baik"""
        mock_creds.return_value = MagicMock()

        mock_service = MagicMock()
        mock_sheets = MagicMock()
        mock_build.return_value.spreadsheets.return_value = mock_sheets

        df = pd.DataFrame()

        with self.assertLogs(level="WARNING") as log:
            load_to_google_sheets(df)

        self.assertTrue(any("Tidak terdapat data untuk diupload" in message for message in log.output))

if __name__ == "__main__":
    unittest.main()