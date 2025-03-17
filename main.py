import pandas as pd
from utils.extract_data.extract import scrape_main
from utils.transform_data.transform import transform_data
from utils.load_data.load_csv import load_data
from utils.load_data.load_postgre import load_to_postgres
from utils.load_data.load_sheet import load_to_google_sheets

def main():
    """Main function untuk menjalankan seluruh proses ETL"""
    try:
        print("Memulai proses ETL...\n")

        print("Menjalankan Extract...")
        raw_data = scrape_main()
        if not raw_data:
            raise ValueError("Extract gagal: Tidak ada data yang ditemukan")

        print("\nMenjalankan Transformasi...")
        transformed_df = transform_data(raw_data)
        if transformed_df.empty:
            raise ValueError("Transformasi gagal: Tidak ada data valid")

        print("\nMenyimpan data...")
        load_data(transformed_df, "products.csv")
        load_to_postgres(transformed_df)
        load_to_google_sheets(transformed_df)

        print("\nProses ETL selesai")

    except Exception as e:
        print(f"\nError dalam proses ETL: {e}")

if __name__ == "__main__":
    main()