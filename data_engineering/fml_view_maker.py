import sqlite3
import pandas as pd
from pathlib import Path

# === CONFIG ===
DB_PATH = Path("/Users/addyhalos/Documents/GitHub/datascience-portfolio/data_engineering/nyse_financials.db")

# === CONNECT TO EXISTING DB ===
conn = sqlite3.connect(DB_PATH)
print(f"Connected to database: {DB_PATH}")

# === (OPTIONAL) CHECK WHAT TABLES EXIST ===
tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
print("\nExisting tables:")
print(tables)

# === HELPER: fix duplicate columns before saving ===
def clean_duplicates(df):
    dupes = df.columns[df.columns.duplicated()].tolist()
    if dupes:
        print(f"Found duplicate columns: {dupes}")
        cols, seen = [], set()
        for c in reversed(df.columns.tolist()):
            if c not in seen:
                seen.add(c)
                cols.append(c)
        cols = list(reversed(cols))
        df = df.loc[:, cols]
        print("→ Duplicates removed.")
    return df

# === CREATE OR REPLACE VIEW ===
print("\n--- Creating or updating view: company_financial_summary ---")

create_view_sql = """
CREATE VIEW company_financial_summary AS
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
    k.marketcap,
    k.enterprisevalue

FROM company_profile p
LEFT JOIN company_quote q       ON p.symbol = q.symbol
LEFT JOIN latest_income li      ON p.symbol = li.symbol
LEFT JOIN company_income i      ON p.symbol = i.symbol AND i.date = li.latest_date
LEFT JOIN company_ratios r      ON p.symbol = r.symbol AND r.date = li.latest_date
LEFT JOIN company_key_metrics k ON p.symbol = k.symbol AND k.date = li.latest_date;
"""

conn.execute("DROP VIEW IF EXISTS company_financial_summary;")
conn.execute(create_view_sql)
print("View `company_financial_summary` created successfully.\n")

create_view_cts = """
CREATE VIEW company_time_series AS
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

conn.execute("DROP VIEW IF EXISTS company_time_series;")
conn.execute(create_view_cts)
print("View `company_time_series` created successfully.\n")

# === VALIDATE & SHOW COUNTS ===
tbls = pd.read_sql("SELECT name FROM sqlite_master WHERE type in ('table','view') ORDER BY name;", conn)
print("DATABASE TABLES PRESENT:")
for t in tbls['name']:
    try:
        cnt = pd.read_sql(f"SELECT COUNT(*) AS cnt FROM `{t}`;", conn).iloc[0]['cnt']
        print(f" - {t}: {cnt} rows")
    except Exception as e:
        print(f" - {t}: error -> {e}")

conn.close()
print("\nAll done.")
