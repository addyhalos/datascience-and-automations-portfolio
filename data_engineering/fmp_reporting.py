import sqlite3
import pandas as pd
from pathlib import Path

# path to your database file
db_path = Path("/Users/addyhalos/Documents/GitHub/datascience-portfolio/data_engineering/data/nyse_financials.db")

# connect to SQLite
conn = sqlite3.connect(db_path)

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 0)  # lets columns wrap naturally

# get table names
tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)['name'].tolist()

for table in tables:
    df = pd.read_sql(f"SELECT * FROM `{table}`", conn)
    print(df.head(10))

conn.close()