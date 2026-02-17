import sqlite3
import pandas as pd
from pathlib import Path

DATA_DIR = Path("../../data")

db_path = DATA_DIR / "movies.db"

conn = sqlite3.connect(db_path)
print("Connected to DB:", db_path)

selected = pd.read_csv(DATA_DIR / "selected_movies.csv")

movie_ids = set(selected["movieId"])
tmdb_ids = set(selected["tmdbId"])

ml_path = DATA_DIR / "ml-latest-small"

movies = pd.read_csv(ml_path / "movies.csv")
ratings = pd.read_csv(ml_path / "ratings.csv")
tags = pd.read_csv(ml_path / "tags.csv")
links = pd.read_csv(ml_path / "links.csv")

# filter
movies = movies[movies["movieId"].isin(movie_ids)]
ratings = ratings[ratings["movieId"].isin(movie_ids)]
tags = tags[tags["movieId"].isin(movie_ids)]
links = links[links["movieId"].isin(movie_ids)]
tmdb = pd.read_csv(DATA_DIR / "tmdb_clean.csv") 

tmdb = tmdb[tmdb["id"].isin(tmdb_ids)]

tmdb = tmdb.rename(columns={"id":"tmdbId"})

movies.to_sql("movies", conn, if_exists="replace", index=False)
ratings.to_sql("ratings", conn, if_exists="replace", index=False)
tags.to_sql("tags", conn, if_exists="replace", index=False)
tmdb.to_sql("tmdb_info", conn, if_exists="replace", index=False)

conn.close()
print("Database built successfully")
