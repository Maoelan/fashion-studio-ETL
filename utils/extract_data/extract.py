import time
import requests
import datetime
import pandas as pd
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

BASE_URL = "https://fashion-studio.dicoding.dev/?page="
MAX_PAGES = 50
TARGET_DATA = 1000

def scrape_page(url: str) -> list:
    """
    Scrape satu halaman dan mengembalikan daftar produk

    Parameters:
    url (str): URL halaman yang akan di-scrape

    Returns:
    list: Daftar produk dengan atribut seperti Title, Price, Rating, Colors, Size, Gender, dan Timestamp
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")
    products = []

    for product in soup.find_all("div", class_="collection-card"):
        title_element = product.find("h3", class_="product-title")
        title = title_element.text.strip() if title_element else "Unknown Product"

        price_element = product.find("span", class_="price")
        price = price_element.text.strip().replace("$", "") if price_element else "N/A"

        rating_element = product.find("p", string=lambda text: text and "Rating" in text)
        rating = rating_element.text.replace("Rating:", "").replace("⭐", "").strip() if rating_element else "Invalid"

        colors_element = product.find("p", string=lambda text: text and "Colors" in text)
        colors = colors_element.text.replace("Colors:", "").strip().split()[0] if colors_element else "N/A"

        size_element = product.find("p", string=lambda text: text and "Size" in text)
        size = size_element.text.replace("Size:", "").strip() if size_element else "N/A"

        gender_element = product.find("p", string=lambda text: text and "Gender" in text)
        gender = gender_element.text.replace("Gender:", "").strip() if gender_element else "N/A"

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        products.append({
            "Title": title,
            "Price": price,
            "Rating": rating,
            "Colors": colors,
            "Size": size,
            "Gender": gender,
            "Timestamp": timestamp
        })

    return products

def scrape_main():
    """
    Scrape semua halaman hingga batas maksimum yang ditentukan

    Returns:
    list: Daftar seluruh produk yang berhasil discrape
    """
    all_products = []
    
    for page in range(1, MAX_PAGES + 1):
        try:
            print(f"Scraping page {page}...")
            url = f"{BASE_URL}{page}"
            page_products = scrape_page(url)
            print(f"Ditemukan {len(page_products)} produk di halaman {page}")
            all_products.extend(page_products)
            time.sleep(1)
        except Exception as e:
            print(f"Error saat scraping halaman {page}: {e}")

    print(f"\nTotal data sebelum filtering: {len(all_products)}")

    cleaned_products = [p for p in all_products if p["Title"] != "Unknown Product"]

    print(f"Total data setelah filtering: {len(cleaned_products)}")
    
    return cleaned_products
