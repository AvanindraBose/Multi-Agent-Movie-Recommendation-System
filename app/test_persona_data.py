from agents.persona_data import *

uid = 1

print(get_user_top_movies(uid).head())
print(get_user_tags(uid)[:10])
print(get_user_favorite_genres(uid))
print(len(get_global_tags()))

