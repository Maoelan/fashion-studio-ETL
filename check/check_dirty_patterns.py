import pandas as pd

df = pd.read_csv("./products.csv")

dirty_patterns = {
    "Title": ["Unknown Product"],
    "Rating": ["Invalid Rating / 5", "Not Rated"],
    "Price": ["Price Unavailable", None]
}

def check_dirty_data(df, dirty_patterns):
    dirty_rows = []
    
    for column, patterns in dirty_patterns.items():
        if column in df.columns:
            for pattern in patterns:
                if pattern is None:
                    matches = df[df[column].isna()]
                else:
                    matches = df[df[column] == pattern]
                
                if not matches.empty:
                    dirty_rows.append(matches)
    
    return pd.concat(dirty_rows) if dirty_rows else pd.DataFrame()

dirty_data = check_dirty_data(df, dirty_patterns)

if not dirty_data.empty:
    print("Ditemukan data kotor:")
    print(dirty_data)
else:
    print("Tidak ada data kotor yang ditemukan.")
