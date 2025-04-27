import unittest
from unittest.mock import patch
import requests
from utils.extract_data.extract import scrape_page

class TestExtract(unittest.TestCase):

    @patch("utils.extract_data.extract.requests.get")
    def test_scrape_page_success(self, mock_get):
        # Menguji scraping dengan HTML yang valid
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = """
            <div class="collection-card">
                <h3 class="product-title">Test Product</h3>
                <span class="price">$10</span>
                <p>Rating: ⭐ 4.5</p>
                <p>Colors: 3 options</p>
                <p>Size: M</p>
                <p>Gender: Unisex</p>
            </div>
        """
        result = scrape_page("https://test-url.com")
        self.assertEqual(len(result), 1)

        expected_data = {
            "Title": "Test Product",
            "Price": "10",
            "Rating": "4.5",
            "Colors": "3",
            "Size": "M",
            "Gender": "Unisex"
        }

        for key in expected_data:
            self.assertEqual(result[0][key], expected_data[key])

    @patch("utils.extract_data.extract.requests.get")
    def test_scrape_page_invalid_url(self, mock_get):
        # Menguji scraping pada URL yang tidak valid
        mock_get.side_effect = requests.exceptions.RequestException("Connection error")
        result = scrape_page("https://invalid-url.com")
        self.assertEqual(result, [])

    @patch("utils.extract_data.extract.requests.get")
    def test_scrape_page_timeout(self, mock_get):
        # Menguji scraping saat timeout terjadi
        mock_get.side_effect = requests.exceptions.Timeout("Request timed out")
        result = scrape_page("https://timeout-url.com")
        self.assertEqual(result, [])

    @patch("utils.extract_data.extract.requests.get")
    def test_scrape_page_no_products(self, mock_get):
        # Menguji scraping pada halaman tanpa produk
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = "<div>No products found</div>"
        result = scrape_page("https://empty-page.com")
        self.assertEqual(result, [])

    @patch("utils.extract_data.extract.requests.get")
    def test_scrape_page_missing_elements(self, mock_get):
        # Menguji scraping pada halaman dengan elemen yang hilang
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = """
            <div class="collection-card">
                <h3 class="product-title">Incomplete Product</h3>
            </div>
        """
        result = scrape_page("https://missing-elements.com")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["Title"], "Incomplete Product")
        self.assertEqual(result[0]["Price"], "N/A")
        self.assertEqual(result[0]["Rating"], "Invalid")
        self.assertEqual(result[0]["Colors"], "N/A")
        self.assertEqual(result[0]["Size"], "N/A")
        self.assertEqual(result[0]["Gender"], "N/A")

if __name__ == "__main__":
    unittest.main()