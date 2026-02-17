from pathlib import Path
from typing import List

from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

from agents.persona_schema import SearchPersona


# ---------- Paths ----------
BASE_DIR = Path(__file__).resolve().parents[2]
VECTOR_DIR = BASE_DIR / "data" / "vector_db"


# ---------- Load Vector Store ----------
def load_vector_store():
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    vectorstore = Chroma(
        persist_directory=str(VECTOR_DIR),
        embedding_function=embeddings
    )

    return vectorstore


# ---------- RAG Retrieval ----------
def retrieve_similar_movies(persona: SearchPersona, k: int = 5) -> List[Document]:
    vectorstore = load_vector_store()

    query = f"""
    {persona.intent}
    Tags: {", ".join(persona.target_tags)}
    Genres: {", ".join(persona.target_genres)}
    """

    docs = vectorstore.similarity_search(query, k=k)

    return docs


# ---------- Optional: LLM-based refinement ----------
llm = ChatOllama(model="llama3.1", temperature=0)


def rag_recommend(persona: SearchPersona) -> str:
    docs = retrieve_similar_movies(persona)

    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""
You are a movie recommendation assistant.

Based on the user's preferences:

Intent: {persona.intent}
Tags: {persona.target_tags}
Genres: {persona.target_genres}

Here are candidate movies:
{context}

Select the best 5 matching movies and briefly explain why.
Return only movie titles with short reasoning.
"""

    response = llm.invoke(prompt)

    return response.content
