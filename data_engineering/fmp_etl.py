# 1. IMPORT LIBRARIES
import requests       # For API calls
from pathlib import Path  # For local file paths
import json           # For reading credentials
import sqlite3 as sql # For database connection
import pandas as pd   # For dataframes
import time           # For timestamps and pacing API calls
import os

# 2. DEFINE FILE PATHS, VARIABLES, AND API ENDPOINTS
key_path = Path("/Users/addyhalos/Documents/secrets/keys.json")  # Local API key (not stored in repo)
companies = ["AAPL", "MSFT", "TSLA", "NVDA", "AMZN"]             # Example company symbols
data_dir = Path("/Users/addyhalos/Documents/GitHub/datascience-portfolio/data_engineering/data")
db_path = data_dir / "nyse_financials.db"                        # Database file (staging + final)
sleep = 0.5                                                      # Pause between API calls

# API endpoints to extract data from
endpoints = {
    "company_profile": "https://financialmodelingprep.com/stable/profile",
    "company_ratios": "https://financialmodelingprep.com/stable/ratios",
    "company_income": "https://financialmodelingprep.com/stable/income-statement",
    "company_quote": "https://financialmodelingprep.com/stable/quote",
    "company_key_metrics": "https://financialmodelingprep.com/stable/key-metrics"
}


# 3. LOAD API KEY 
#"""
# Option 1: Local Key - This is for running this script in your local machine. You will need a local copy of the API Key in the key_path
if not key_path.exists():
    raise FileNotFoundError(f"keys.json not found at {key_path}")
with key_path.open("r", encoding="utf-8") as fh:
    data = json.load(fh)
api_key = data.get("fmp_key")
#"""

# Option 2: Github Secret - Use when running on Github Actions - API Key is saved in Github Secrets for this to work
"""
api_key = os.getenv("FMP_KEY")
if not api_key:
    raise ValueError("FMP_KEY not found in GitHub Secrets")
data_dir = Path("data_engineering/data")
db_path = data_dir / "nyse_financials.db"
"""    

# 4. CONNECT TO DATABASE (STAGING + FINAL IN SAME FILE)
data_dir.mkdir(exist_ok=True)
session = requests.Session()
conn = sql.connect(db_path)

# 5. EXTRACT AND LOAD INTO STAGING TABLES
try:
    for table_name, endpoint_url in endpoints.items():
        staging_table = f"staging_{table_name}"  # e.g. staging_company_profile
        all_dfs = []
        print(f"\n--- Extracting from endpoint: {table_name} ---")

        # Iterate through each company symbol
        for symbol in companies:
            try:
                resp = session.get(endpoint_url, params={"symbol": symbol, "apikey": api_key}, timeout=20)
                status = resp.status_code
                text_len = len(resp.text or "")
                print(f"{table_name} | {symbol} -> status: {status} | len: {text_len}")

                # Convert API response into DataFrame
                if status == 200:
                    payload = resp.json()
                    if isinstance(payload, list):
                        df = pd.DataFrame(payload) if payload else pd.DataFrame([{"note": "empty_list"}])
                    elif isinstance(payload, dict):
                        df = pd.DataFrame([payload])
                    else:
                        df = pd.DataFrame([{"raw": str(payload)}])
                else:
                    df = pd.DataFrame([{"error_status": status, "error_text": resp.text[:500]}])

                # Annotate metadata
                df["symbol"] = symbol
                df["endpoint"] = table_name
                df["fetched_at"] = pd.Timestamp.utcnow()
                all_dfs.append(df)

            except Exception as e:
                print(f"EXCEPTION: {table_name} | {symbol} -> {e}")
                all_dfs.append(pd.DataFrame([{
                    "symbol": symbol,
                    "endpoint": table_name,
                    "error": str(e),
                    "fetched_at": pd.Timestamp.utcnow()
                }]))
            finally:
                time.sleep(sleep)

        # Combine all rows for that endpoint
        if all_dfs:
            endpoint_df = pd.concat(all_dfs, ignore_index=True, sort=False)
        else:
            endpoint_df = pd.DataFrame([{"note": "no_data_collected", "endpoint": table_name, "fetched_at": pd.Timestamp.utcnow()}])

        # Write to staging table
        endpoint_df.to_sql(staging_table, conn, if_exists="append", index=False)
        print(f"WROTE {len(endpoint_df)} rows to `{staging_table}`")

# 6. TRANSFORM: CLEAN AND LOAD INTO FINAL TABLES
    for table_name in endpoints.keys():
        staging_table = f"staging_{table_name}"
        print(f"\n--- Transforming data from {staging_table} to {table_name} ---")

        # Load from staging
        df = pd.read_sql(f"SELECT * FROM {staging_table}", conn)

# 7. DATA CLEANING

        # a. Drop duplicate records (same company symbol)
        dedup_cols = [c for c in df.columns if c not in ["fetched_at", "cleaned_at"]]
        df = df.drop_duplicates(subset=dedup_cols, keep="last")

        # b. Remove any rows that failed during API extraction or error handling
        error_cols = ["error_status", "error_text", "error"]
        for col in error_cols:
            if col in df.columns:
                df = df[df[col].isna() | (df[col] == "")]
        df = df.drop(columns=error_cols, errors="ignore")

        # c. Standardize column names (lowercase, underscores)
        df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

        # d. Drop unnecessary metadata columns
        df = df.drop(columns=["endpoint"], errors="ignore")

        # e. Handle missing or invalid values
        # Example: Replace empty strings with NaN, fill some numeric NaNs with 0
        df = df.replace("", pd.NA)
        num_cols = df.select_dtypes(include=["number"]).columns
        df[num_cols] = df[num_cols].fillna(0)

        # f. Add a timestamp for cleaned data
        df["cleaned_at"] = pd.Timestamp.utcnow()

# 8. LOAD INTO FINAL TABLE
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        print(f"Loaded cleaned data into `{table_name}` ({len(df)} rows)")


finally:
# 9. VALIDATION AND SUMMARY
    conn.commit()
    tbls = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;", conn)
    print("\nDATABASE TABLES PRESENT:")
    for t in tbls['name']:
        cnt = pd.read_sql(f"SELECT COUNT(*) AS cnt FROM `{t}`", conn).iloc[0]['cnt']
        print(f" - {t}: {cnt} rows")
    conn.close()
