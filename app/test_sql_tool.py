from tools.sql_tool import sql_to_text

query = """
SELECT m.title, AVG(r.rating) as avg_rating
FROM movies m
JOIN ratings r ON m.movieId = r.movieId
GROUP BY m.movieId
ORDER BY avg_rating DESC
LIMIT 5
"""

print(sql_to_text(query))
