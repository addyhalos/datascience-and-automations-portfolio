import sqlite3
import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials

# === CONFIG ===
DB_PATH = "/Users/addyhalos/Documents/GitHub/datascience-portfolio/data_engineering/data/nyse_financials.db"  # local path
#VIEW_NAME = "company_financial_summary"
SPREADSHEET_ID = "1PoCHCiYhW_ZFRMuCnsw65GNHUY3CRRqN_fC9gDnb_bI"

# === GOOGLE AUTH ===
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("/Users/addyhalos/Documents/secrets/google_fmp_key.json", scopes=SCOPES)
gc = gspread.authorize(creds)

# === CONNECT TO SQLITE ===
conn = sqlite3.connect(DB_PATH)

# === READ VIEW INTO DATAFRAME ===
df = pd.read_sql_query(f"SELECT * FROM company_financial_summary;", conn)

# === UPLOAD TO GOOGLE SHEET ===
sheet = gc.open_by_key(SPREADSHEET_ID)
worksheet_name = "Financial Summary"
try:
    worksheet = sheet.worksheet(worksheet_name)
    worksheet.clear()
except gspread.exceptions.WorksheetNotFound:
    worksheet = sheet.add_worksheet(title=worksheet_name, rows=1000, cols=20)

# Write DataFrame to sheet
set_with_dataframe(worksheet, df)

print(f"✅ Successfully uploaded view '{VIEW_NAME}' to tab '{worksheet_name}' in Google Sheet.")
