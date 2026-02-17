from agents.persona_agent import build_persona

persona = build_persona(
    user_id=1,
    query="I want a dark psychological emotional movie"
)

print(persona)