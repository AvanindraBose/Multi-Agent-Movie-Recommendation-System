import pandas as pd
import ast
from pathlib import Path

DATA_DIR = Path("../../data")
tmdb_path = DATA_DIR / "tmdb_dataset/tmdb_5000_movies.csv"

tmdb = pd.read_csv(tmdb_path)

# Keep only required columns
tmdb = tmdb[["id", "title", "overview", "release_date", "genres"]]


# Convert genres stringified JSON → readable text
def parse_genres(text):
    try:
        items = ast.literal_eval(text)
        return ", ".join([i["name"] for i in items])
    except:
        return ""

tmdb["genres"] = tmdb["genres"].apply(parse_genres)

# Remove movies with no overview (important for RAG later)
tmdb = tmdb.dropna(subset=["overview"])

# Save cleaned dataset
tmdb.to_csv(DATA_DIR / "tmdb_clean.csv", index=False)

print("tmdb_clean.csv created with rows:", len(tmdb))
