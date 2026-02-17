from agents.persona_agent import build_persona
from agents.sql_agent import recommend_with_sql

persona = build_persona(1, "dark psychological emotional movie")

result = recommend_with_sql(persona)

print(result)