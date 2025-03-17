import pandas as pd

def load_data(df, filename="products.csv"):
    """
    Menyimpan dataframe ke file CSV

    Parameters:
    df (pd.DataFrame): Data yang akan disimpan
    filename (str): Nama file output (default: "products_data.csv")

    Returns:
    None
    """
    if df.empty:
        print("Tidak terdapat data untuk disimpan.")
        return
    
    try:
        df.to_csv(filename, index=False)
        print(f"Data berhasil disimpan di {filename}")
    except Exception as e:
        print(f"Error saat menyimpan data: {e}")
        raise