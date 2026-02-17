from agents.persona_agent import build_persona
from rag.rag_agent import rag_recommend

persona = build_persona(1, "dark psychological emotional movie")

result = rag_recommend(persona)

print(result)
