from agents.persona_agent import build_persona
from agents.sql_agent import recommend_with_sql
from rag.rag_agent import rag_recommend
from agents.summarizer_agent import summarize_recommendations

persona = build_persona(1, "dark psychological emotional movie")

sql_result = recommend_with_sql(persona)
rag_movies = rag_recommend(persona)

final = summarize_recommendations(persona, sql_result, rag_movies)

print(final)