import json
from .utils import *


async def compute_q2(selected_concepts: str, question: str):

    required_concepts = '[' + \
        '"Resistance is the opposition a conductor offers to the flow of charge and is expressed by $!$ R = \\frac{V}{I} $!$",' + \
        '"Electric power is the rate of energy conversion or work done. In a circuit component like a resistor, power is given by $!$ P = VI $!$, which is dissipated as heat or used to perform work."' + \
        ']'

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
