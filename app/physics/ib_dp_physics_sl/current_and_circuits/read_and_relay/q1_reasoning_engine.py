import json
from .utils import *


async def compute_q1(selected_concepts: str, question: str):

    required_concepts = "[Resistance is the opposition a conductor offers to the flow of charge and is expressed by $!$ R = \\frac{V}{I} $!$.]"

    working, answer, is_correct = attempt_question(
        required_concepts, question, selected_concepts)

    return {
        'status': 200,
        'body': {
            'isCorrect': is_correct,
            'working': working,
            'answer': answer,
            'concepts': []
        }
    }
