import sqlite3
from pathlib import Path

DB_PATH = Path("../../data/movies.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# get tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [t[0] for t in cursor.fetchall()]

print("Tables:\n")
for table in tables:
    print(f"\n=== {table} ===")

    cursor.execute(f"PRAGMA table_info({table});")
    columns = cursor.fetchall()

    for col in columns:
        cid, name, dtype, notnull, default, pk = col
        print(f"{name} ({dtype})")

conn.close()
