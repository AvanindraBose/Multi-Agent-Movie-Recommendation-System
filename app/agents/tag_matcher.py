from rapidfuzz import process, fuzz


def match_query_to_tags(query: str, global_tags: list[str], limit: int = 25) -> list[str]:
    """
    Find tags similar to user query text
    """
    if not query:
        return []

    matches = process.extract(
        query.lower(),
        global_tags,
        scorer=fuzz.partial_ratio,
        limit=limit
    )

    # keep reasonably similar tags
    filtered = [tag for tag, score, _ in matches if score >= 60]

    return list(set(filtered))
