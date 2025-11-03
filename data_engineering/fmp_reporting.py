import sqlite3
import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials

# === CONFIG ===
DB_PATH = "/Users/addyhalos/Documents/GitHub/datascience-portfolio/data_engineering/nyse_financials.db"
GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1PoCHCiYhW_ZFRMuCnsw65GNHUY3CRRqN_fC9gDnb_bI/edit#gid=0"
SERVICE_ACCOUNT_FILE = "/Users/addyhalos/Documents/secrets/google_fmp_key.json"  # <-- change this path

# === SQL QUERIES ===
company_financial_summary = """
WITH latest_income AS (
    SELECT symbol, MAX(date) AS latest_date
    FROM company_income
    GROUP BY symbol
)
SELECT
    p.symbol,
    p.companyname,
    p.sector,
    p.industry,
    p.ceo,
    p.city,
    p.state,
    p.ipodate,
    p.lastdividend,
    p.website,

    q.price,
    q.marketcap,
    q.changepercentage,

    i.date AS financial_date,
    i.revenue,
    i.netincome,
    i.eps,

    r.pricetoearningsratio AS pe_ratio,
    CASE
        WHEN r.shareholdersequitypershare IS NULL OR r.shareholdersequitypershare = 0 THEN NULL
        ELSE (r.netincomepershare * 1.0 / r.shareholdersequitypershare)
    END AS roe,
    r.currentratio,
    r.debttoequityratio,

    k.returnonassets,
    k.returnoninvestedcapital,
    k.returnonequity,
    k.freecashflowyield,
    k.enterprisevalue

FROM company_profile p
LEFT JOIN company_quote q       ON p.symbol = q.symbol
LEFT JOIN latest_income li      ON p.symbol = li.symbol
LEFT JOIN company_income i      ON p.symbol = i.symbol AND i.date = li.latest_date
LEFT JOIN company_ratios r      ON p.symbol = r.symbol AND r.date = li.latest_date
LEFT JOIN company_key_metrics k ON p.symbol = k.symbol AND k.date = li.latest_date;
"""

company_time_series = """
WITH all_dates AS (
    SELECT symbol, date AS dt FROM company_income
    UNION
    SELECT symbol, date AS dt FROM company_ratios
    UNION
    SELECT symbol, date AS dt FROM company_key_metrics
)
SELECT
    d.symbol,
    d.dt AS date,

    -- income statement snapshots (may be NULL for some dates)
    i.revenue,
    i.netincome,
    i.eps,
    i.operatingincome,
    i.ebitda,

    -- ratios (many financial ratios keyed by same date)
    r.pricetoearningsratio,
    r.pricetobookratio,
    r.currentratio,
    r.debttoequityratio,
    r.ebitdamargin,
    r.bookvaluepershare,
    r.netincomepershare,
    r.shareholdersequitypershare,

    -- derived: ROE (safe)
    CASE
      WHEN r.shareholdersequitypershare IS NULL OR r.shareholdersequitypershare = 0 THEN NULL
      ELSE (r.netincomepershare * 1.0 / r.shareholdersequitypershare)
    END AS roe,

    -- key metrics
    k.marketcap,
    k.enterprisevalue,
    k.freecashflowtofirm,
    k.freecashflowtoequity,
    k.returnonassets,
    k.returnoninvestedcapital,
    k.returnonequity,

    -- housekeeping
    i.fiscalyear AS income_fiscalyear,
    r.fiscalyear AS ratios_fiscalyear,
    k.fiscalyear AS keymetrics_fiscalyear

FROM all_dates d
LEFT JOIN company_income           i ON i.symbol = d.symbol AND i.date = d.dt
LEFT JOIN company_ratios           r ON r.symbol = d.symbol AND r.date = d.dt
LEFT JOIN company_key_metrics      k ON k.symbol = d.symbol AND k.date = d.dt
ORDER BY d.symbol, d.dt;
"""

# === MAIN LOGIC ===
def main():
    # Authorize Google Sheets API
    print("Connecting to Google Sheets...")
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scopes)
    client = gspread.authorize(creds)

    # Open the target spreadsheet
    queries = {
        "company_financial_summary": company_financial_summary,
        "company_time_series": company_time_series
    }
    sh = client.open_by_url(GOOGLE_SHEET_URL)
    conn = sqlite3.connect(DB_PATH)
    for sheet_name,query in queries.items():
        try:
            worksheet = sh.worksheet(sheet_name)
            print(f"Found existing worksheet: {sheet_name}")
            worksheet.clear()
            df = pd.read_sql(query, conn)
            print(f"{sheet_name} returned {len(df)} rows and {len(df.columns)} columns.")
            set_with_dataframe(worksheet, df, include_index=False, include_column_header=True, resize=True)

        except gspread.exceptions.WorksheetNotFound:
            print(f"Worksheet not found")

    conn.close()
    print("Upload completed successfully!")
    print(f"Data uploaded to: {GOOGLE_SHEET_URL}")

if __name__ == "__main__":
    main()
