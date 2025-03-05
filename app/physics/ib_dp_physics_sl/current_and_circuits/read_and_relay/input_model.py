from typing import List
from pydantic import BaseModel


class InputModel(BaseModel):
    highlights: List[str] = []
    formula: List[str] = []
    question: str
