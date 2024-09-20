from typing import List
from pydantic import BaseModel


class InputModel(BaseModel):
    explanation: str
    formula: List[str] = []
