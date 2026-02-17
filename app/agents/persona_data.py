from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "data" / "movies.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def get_user_top_movies(user_id: int) -> pd.DataFrame:
    conn = get_connection()

    query = """
    SELECT m.movieId, m.title, AVG(r.rating) as avg_rating
    FROM ratings r
    JOIN movies m ON r.movieId = m.movieId
    WHERE r.userId = ?
    GROUP BY m.movieId
    HAVING avg_rating >= 4
    ORDER BY avg_rating DESC
    LIMIT 20
    """

    df = pd.read_sql_query(query, conn, params=(user_id,))
    conn.close()
    return df

def get_user_tags(user_id: int) -> list[str]:
    conn = get_connection()

    query = """
    SELECT DISTINCT tag
    FROM tags
    WHERE userId = ?
    """

    df = pd.read_sql_query(query, conn, params=(user_id,))
    conn.close()

    return df["tag"].dropna().str.lower().tolist()

def get_global_tags() -> list[str]:
    conn = get_connection()

    query = """
    SELECT DISTINCT tag FROM tags
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    return df["tag"].dropna().str.lower().tolist()

def get_user_favorite_genres(user_id: int) -> list[str]:
    conn = get_connection()

    query = """
    SELECT m.genres
    FROM ratings r
    JOIN movies m ON r.movieId = m.movieId
    WHERE r.userId = ? AND r.rating >= 4
    """

    df = pd.read_sql_query(query, conn, params=(user_id,))
    conn.close()

    if df.empty:
        return []

    genres = (
        df["genres"]
        .str.split("|")
        .explode()
        .str.strip()
        .str.lower()
        .value_counts()
        .head(5)
        .index.tolist()
    )

    return genres
