from typing import List
from pydantic import BaseModel


class VerificationJson(BaseModel):
    verification_question: str
    verification_answer: str


class InputModel(BaseModel):
    explanation: str
    concepts: List[VerificationJson] = []
