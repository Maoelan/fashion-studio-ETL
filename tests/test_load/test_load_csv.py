import unittest
import pandas as pd
import os
import tempfile
from utils.load_data.load_csv import load_data

class TestLoad(unittest.TestCase):

    def setUp(self):
        # Setup file sementara untuk pengujian
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
        self.filename = self.temp_file.name
        self.temp_file.close()

    def tearDown(self):
        # Hapus file setelah pengujian selesai
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_load_data_success(self):
        # Menguji apakah data berhasil disimpan ke file CSV
        data = {
            "Title": ["Product A"],
            "Price": [160000],
            "Rating": [4.5],
            "Colors": [3],
            "Size": ["M"],
            "Gender": ["Unisex"]
        }
        df = pd.DataFrame(data)

        load_data(df, self.filename)
        
        self.assertTrue(os.path.exists(self.filename))

        df_loaded = pd.read_csv(self.filename)
        pd.testing.assert_frame_equal(df, df_loaded, check_dtype=False)

    def test_load_data_failure(self):
        # Menguji apakah exception ditangani dengan benar jika path tidak valid
        data = {
            "Title": ["Product A"],
            "Price": [160000],
            "Rating": [4.5],
            "Colors": [3],
            "Size": ["M"],
            "Gender": ["Unisex"]
        }
        df = pd.DataFrame(data)

        invalid_filename = "/invalid_path/test_fashion_data.csv"

        with self.assertRaises(Exception):
            load_data(df, invalid_filename)

if __name__ == "__main__":
    unittest.main()