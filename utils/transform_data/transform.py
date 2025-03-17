import pandas as pd

EXCHANGE_RATE = 16000

def transform_data(data):
    """
    Membersihkan dan mengubah format data

    Proses transformasi mencakup:
    - Konversi Price ke mata uang rupiah
    - Mengubah Rating menjadi tipe data float
    - Mengubah Colors ke tipe data integer
    - Menghapus data duplikat dan data tidak valid

    Parameters:
    data (list of dict): Raw data hasil scraping

    Returns:
    pd.DataFrame: Data yang telah ditransformasi
    """
    try:
        df = pd.DataFrame(data).copy()

        if df.empty:
            print("Data kosong setelah scraping")
            return df

        required_columns = {"Price", "Rating", "Colors"}
        if not required_columns.issubset(df.columns):
            missing_cols = required_columns - set(df.columns)
            print(f"Terdapat kolom yang tidak ditemukan: {missing_cols}")
            return pd.DataFrame()

        df["Price"] = pd.to_numeric(df["Price"], errors="coerce") * EXCHANGE_RATE

        df["Rating"] = df["Rating"].astype(str).str.extract(r"([\d.]+)").astype(float)

        df.dropna(subset=["Rating"], inplace=True)

        df["Colors"] = pd.to_numeric(df["Colors"], errors="coerce").fillna(0).astype(int, errors="ignore")

        df.drop_duplicates(inplace=True)
        df.dropna(inplace=True)

        print("Proses transformasi selesai.")
        return df

    except Exception as e:
        print(f"Error saat proses transformasi: {e}")
        return pd.DataFrame()