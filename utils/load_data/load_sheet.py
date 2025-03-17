import pandas as pd
import logging
from googleapiclient.discovery import build
from google.oauth2 import service_account

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SPREADSHEET_ID = "19vweQTnSLL-9Qy52-YH0OZOJlevBm0uBqRRSpRS8dl8"
SHEET_NAME = "Sheet1"

def load_to_google_sheets(df: pd.DataFrame):
    """
    Upload dataframe ke Google Sheets

    Parameters:
    df (pd.DataFrame): Data yang akan diupload

    Returns:
    dict | None: Respons dari API Google Sheets jika berhasil, None jika terjadi kesalahan.
    """
    if df.empty:
        logger.warning("Tidak terdapat data untuk diupload ke Google Sheets.")
        return
    
    try:
        creds = service_account.Credentials.from_service_account_file(
            "google-sheets-api.json", scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()

        values = [df.columns.tolist()] + df.values.tolist()

        request = sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=SHEET_NAME,
            valueInputOption="RAW",
            body={"values": values}
        )
        response = request.execute()

        logger.info("\nData berhasil diupload ke Google Sheets")
        return response

    except Exception as e:
        logger.error(f"Error saat mengupload ke Google Sheets: {e}")
        return None