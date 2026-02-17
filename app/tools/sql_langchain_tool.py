from langchain_core.tools import tool
from tools.sql_tool import sql_to_text


@tool
def query_movie_database(sql_query: str) -> str:
    """
    Execute a SQL query on the movie database and return results.
    Only SELECT queries are allowed.
    """
    return sql_to_text(sql_query)