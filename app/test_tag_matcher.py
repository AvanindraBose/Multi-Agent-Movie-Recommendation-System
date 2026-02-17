from agents.persona_data import get_global_tags
from agents.tag_matcher import match_query_to_tags

query = "dark emotional psychological character study"

tags = get_global_tags()

print(match_query_to_tags(query, tags))