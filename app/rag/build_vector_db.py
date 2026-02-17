from pathlib import Path
import sqlite3
import pandas as pd

from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document



BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "data" / "movies.db"
VECTOR_DIR = BASE_DIR / "data" / "vector_db"


def normalize_title(title: str):
    return title.split("(")[0].strip().lower()

def load_movies():
    conn = sqlite3.connect(DB_PATH)

    movies = pd.read_sql_query("SELECT * FROM movies", conn)
    tmdb = pd.read_sql_query("SELECT * FROM tmdb_info", conn)

    conn.close()

    movies["clean_title"] = movies["title"].apply(normalize_title)
    tmdb["clean_title"] = tmdb["title"].apply(normalize_title)

    df = movies.merge(tmdb, on="clean_title", suffixes=("_ml", "_tmdb"))

    df = df.dropna(subset=["overview"])

    return df



def build_vector_db():
    df = load_movies()

    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    docs = []

    for _, row in df.iterrows():
        content = f"""
        Title: {row['title_ml']}
        Genres: {row['genres_ml']}
        Overview: {row['overview']}
        """.strip()

        docs.append(
            Document(
        page_content=content,
        metadata={
            "movieId": row["movieId"],
            "title": row["title_ml"]
        }
    )
)


    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=str(VECTOR_DIR)
    )

    vectorstore.persist()
    print("Vector DB built with", len(docs), "movies")


if __name__ == "__main__":
    build_vector_db()
