import json
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

from agents.persona_schema import SearchPersona
from agents.persona_data import (
    get_user_top_movies,
    get_user_tags,
    get_user_favorite_genres,
    get_global_tags
)
from agents.tag_matcher import match_query_to_tags


llm = ChatOllama(model="llama3.1", temperature=0)


def build_persona(user_id: int, query: str) -> SearchPersona:
    # deterministic evidence
    top_movies = get_user_top_movies(user_id)
    user_tags = get_user_tags(user_id)
    fav_genres = get_user_favorite_genres(user_id)
    global_tags = get_global_tags()

    candidate_tags = match_query_to_tags(query, global_tags)

    prompt = ChatPromptTemplate.from_template("""
You are a movie taste analyst.

Return ONLY valid JSON. No explanation text.

JSON schema:
{{
  "intent": string,
  "user_preference_summary": string,
  "target_tags": list[string],
  "target_genres": list[string],
  "reasoning": string
}}

RULES:
- Only choose tags from: {candidate_tags}
- Do not invent tags
- Keep response short

USER REQUEST:
{query}

USER FAVORITE MOVIES:
{movies}

USER HISTORICAL TAGS:
{user_tags}

FAVORITE GENRES:
{genres}
""")

    chain = prompt | llm

    response = chain.invoke({
        "query": query,
        "movies": top_movies.to_string(index=False),
        "user_tags": user_tags,
        "genres": fav_genres,
        "candidate_tags": candidate_tags
    })

    text = response.content.strip()

    # remove markdown json fences if model adds them
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]

    data = json.loads(text)

    return SearchPersona(**data)
