from pydantic import BaseModel
from typing import List

class RecommendRequest(BaseModel):
    ingredients: List[str]
