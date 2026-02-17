from pydantic import BaseModel, Field
from typing import List


class SearchPersona(BaseModel):
    intent: str = Field(description="short description of what user wants")
    user_preference_summary: str = Field(description="summary of user's taste from history")
    target_tags: List[str] = Field(description="tags to filter movies")
    target_genres: List[str] = Field(description="preferred genres")
    reasoning: str = Field(description="why these tags were chosen")
