from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "data" / "movies.db"


def get_connection():
    return sqlite3.connect(DB_PATH)

FORBIDDEN = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE", "PRAGMA"]

def validate_sql(query: str):
    upper = query.upper()
    for word in FORBIDDEN:
        if word in upper:
            raise ValueError(f"Forbidden SQL operation detected: {word}")

    if "SELECT" not in upper:
        raise ValueError("Only SELECT queries are allowed")

def run_sql(query: str) -> pd.DataFrame:
    validate_sql(query)

    conn = get_connection()

    try:
        df = pd.read_sql_query(query, conn)
    except Exception as e:
        conn.close()
        raise RuntimeError(f"SQL execution failed: {e}")

    conn.close()
    return df

def sql_to_text(query: str, limit: int = 10) -> str:
    df = run_sql(query)

    if df.empty:
        return "No results found."

    return df.head(limit).to_string(index=False)
