from typing import List
from pydantic import BaseModel


class InputModel(BaseModel):
    highlights: List[str] = []
    formulas: List[str] = []
    question: str
