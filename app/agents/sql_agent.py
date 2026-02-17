from pathlib import Path

from langchain_ollama import ChatOllama
from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate

from tools.sql_langchain_tool import query_movie_database
from agents.persona_schema import SearchPersona


# ---------- Load DB schema grounding ----------
BASE_DIR = Path(__file__).resolve().parents[2]
SCHEMA_TEXT = (BASE_DIR / "app" / "db" / "schema_description.txt").read_text()


# ---------- LLM ----------
llm = ChatOllama(model="llama3.1", temperature=0)


# ---------- Tools ----------
tools = [query_movie_database]


# ---------- ReAct Prompt ----------
prompt = PromptTemplate.from_template("""
You are a SQL movie recommendation agent.

You can use the following tools:
{tools}

Available tool names:
{tool_names}

DATABASE SCHEMA:
{schema}

STRICT RULES:
- Only use tables: movies, ratings, tags
- NEVER assume rating column exists in movies
- ALWAYS compute AVG(rating)
- ALWAYS JOIN ratings
- ALWAYS GROUP BY movieId
- ORDER BY AVG(rating) DESC
- LIMIT 5 results
- Aggregates like AVG() must NEVER appear in WHERE
- Use HAVING when filtering aggregated values


Persona Preferences:
Tags: {tags}
Genres: {genres}

Use EXACTLY this reasoning format:

Question: Find recommended movies
Thought: reasoning step
Action: one of [{tool_names}]
Action Input: SQL query
Observation: result
... repeat Thought/Action/Observation if needed ...
Thought: I now know the final answer
Final Answer: recommended movies list

Begin!

{agent_scratchpad}
""")


# ---------- Build ReAct Agent ----------
agent = create_react_agent(llm, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True
)


# ---------- Public function ----------
def recommend_with_sql(persona: SearchPersona) -> str:
    response = agent_executor.invoke({
        "schema": SCHEMA_TEXT,
        "tags": ", ".join(persona.target_tags),
        "genres": ", ".join(persona.target_genres)
    })

    return response["output"]

