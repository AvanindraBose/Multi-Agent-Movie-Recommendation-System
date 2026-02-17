import pandas as pd
from pathlib import Path

DATA_DIR = Path("../data")
print(DATA_DIR)
ml_path = DATA_DIR / "ml-latest-small"
tmdb_path = DATA_DIR / "tmdb_dataset"

movies = pd.read_csv(ml_path / "movies.csv")
ratings = pd.read_csv(ml_path / "ratings.csv")
tags = pd.read_csv(ml_path / "tags.csv")
links = pd.read_csv(ml_path / "links.csv")

tmdb = pd.read_csv(tmdb_path / "tmdb_5000_movies.csv")

print(movies.shape, ratings.shape, tags.shape, links.shape, tmdb.shape)

# count ratings per movie
rating_counts = ratings.groupby("movieId").size().reset_index(name="num_ratings")

# keep strong signal movies
popular_movies = rating_counts.sort_values("num_ratings", ascending=False)

print(popular_movies.head())

# merge ratings with links
popular_with_tmdb = popular_movies.merge(links, on="movieId")

# remove missing tmdb ids
popular_with_tmdb = popular_with_tmdb.dropna(subset=["tmdbId"])

print(popular_with_tmdb.head())

tmdb_ids = set(tmdb["id"])

filtered = popular_with_tmdb[popular_with_tmdb["tmdbId"].isin(tmdb_ids)]

print(len(filtered))

selected_500 = filtered.head(500)

print(selected_500.shape)

selected_500.to_csv(DATA_DIR / "selected_movies.csv", index=False)
