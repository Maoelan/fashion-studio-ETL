import psycopg2
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

DB_CONFIG = {
    "dbname": "[Database]",
    "user": "[Username]", # silahkan ganti dengan username PostgreSQL kamu
    "password": "[Password]", # silahkan ganti dengan password PostgreSQL kamu
    "host": "[Host]",
    "port": "[Port]"
}

def load_to_postgres(df, table_name="products"):
    """
    Menyimpan dataframe ke PostgreSQL

    Parameters:
    df (pd.DataFrame): Data yang akan dimasukkan
    table_name (str): Nama tabel tujuan (default: "products")

    Returns:
    None
    """
    if df.empty:
        logging.warning("Tidak terdapat data untuk dimasukkan ke PostgreSQL.")
        return
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY,
            title TEXT,
            price FLOAT,
            rating FLOAT,
            colors INT,
            size TEXT,
            gender TEXT,
            timestamp TIMESTAMP
        );
        """
        cur.execute(create_table_query)

        for _, row in df.iterrows():
            insert_query = f"""
            INSERT INTO {table_name} (title, price, rating, colors, size, gender, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
            """
            cur.execute(insert_query, tuple(row))

        conn.commit()
        cur.close()
        conn.close()
        logging.info(f"Data berhasil dimasukkan ke tabel {table_name}.")
    
    except Exception as e:
        logging.error(f"Error saat menyimpan ke PostgreSQL: {e}")