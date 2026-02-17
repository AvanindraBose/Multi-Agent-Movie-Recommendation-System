from langchain_ollama import ChatOllama
from agents.persona_schema import SearchPersona


llm = ChatOllama(model="llama3.1", temperature=0.2)


def summarize_recommendations(persona: SearchPersona, sql_result: str, rag_movies: list):
    rag_titles = [m["title"] for m in rag_movies]

    prompt = f"""
You are a personalized movie recommendation assistant.

USER PROFILE:
Intent: {persona.intent}
Preferred genres: {persona.target_genres}
Preferred tags: {persona.target_tags}
Taste summary: {persona.user_preference_summary}

CANDIDATES FROM POPULARITY (SQL AGENT):
{sql_result}

CANDIDATES FROM STORY SIMILARITY (RAG AGENT):
{rag_titles}

Instructions:
- Movies appearing in both lists are strong recommendations
- Movies matching genres should rank higher
- Provide a final top 5 list
- Explain each recommendation in 1–2 sentences
- Personalize reasoning using user taste

Final Answer:
"""

    return llm.invoke(prompt).content
