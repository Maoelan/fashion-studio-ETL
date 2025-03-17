import unittest
import pandas as pd
from utils.transform_data.transform import transform_data

class TestTransform(unittest.TestCase):

    def test_transform_valid_data(self):
        """Menguji apakah transformasi data berhasil dengan data yang benar"""
        data = [
            {"Title": "Product A", "Price": "10", "Rating": "4.5", "Colors": "3", "Size": "M", "Gender": "Unisex"},
            {"Title": "Product B", "Price": "15", "Rating": "4.0", "Colors": "2", "Size": "L", "Gender": "Male"},
        ]
        df = transform_data(data)

        expected_data = {
            "Title": ["Product A", "Product B"],
            "Price": [10 * 16000, 15 * 16000],
            "Rating": [4.5, 4.0],
            "Colors": [3, 2],
            "Size": ["M", "L"],
            "Gender": ["Unisex", "Male"],
        }
        expected_df = pd.DataFrame(expected_data)

        pd.testing.assert_frame_equal(df, expected_df, check_dtype=False)

    def test_transform_invalid_data(self):
        """Menguji apakah transformasi data gagal jika semua nilai tidak valid"""
        data = [{"Title": "Product A", "Price": "N/A", "Rating": "Invalid", "Colors": "NaN"}]
        df = transform_data(data)
        self.assertEqual(len(df), 0)

    def test_transform_partial_invalid_data(self):
        """Menguji apakah hanya baris yang valid yang masuk ke dataframe"""
        data = [
            {"Title": "Product A", "Price": "10", "Rating": "4.5", "Colors": "3", "Size": "M", "Gender": "Unisex"},
            {"Title": "Product B", "Price": "N/A", "Rating": "Invalid", "Colors": "NaN"}
        ]
        df = transform_data(data)
        self.assertEqual(len(df), 1)
        self.assertEqual(df.iloc[0]["Title"], "Product A")

    def test_transform_invalid_price(self):
        """Menguji apakah data dengan harga tidak valid akan dibuang"""
        data = [{"Title": "Product A", "Price": "N/A", "Rating": "4.5", "Colors": "3", "Size": "M", "Gender": "Unisex"}]
        df = transform_data(data)
        self.assertEqual(len(df), 0)

    def test_transform_empty_data(self):
        """Menguji apakah function menangani input kosong tanpa error."""
        df = transform_data([])
        self.assertTrue(isinstance(df, pd.DataFrame))
        self.assertEqual(len(df), 0)

    def test_transform_none_data(self):
        """Menguji apakah function menangani None sebagai input tanpa error"""
        df = transform_data(None)
        self.assertTrue(isinstance(df, pd.DataFrame))
        self.assertEqual(len(df), 0)

if __name__ == "__main__":
    unittest.main()