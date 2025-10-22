import sqlite3
import pandas as pd
from pathlib import Path

# path to your database file
db_path = Path("/Users/addyhalos/Documents/GitHub/datascience-portfolio/data_engineering/data/nyse_financials.db")

# connect to SQLite
conn = sqlite3.connect(db_path)

# get table names
tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)['name'].tolist()

# export each table to CSV
for table in tables:
    df = pd.read_sql(f"SELECT * FROM `{table}`", conn)
    csv_path = db_path.parent / f"{table}.csv"
    df.to_csv(csv_path, index=False)
    print(f"✅ Exported {table} → {csv_path}")

conn.close()
