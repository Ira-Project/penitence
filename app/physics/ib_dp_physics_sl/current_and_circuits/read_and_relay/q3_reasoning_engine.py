import json
from .utils import *


async def compute_q3(selected_concepts: str, question: str):

    required_concepts = "[" + \
        "Resistance is the opposition a conductor offers to the flow of charge and is expressed by $!$ R = \\frac{V}{I} $!$. According to Ohm's law, at constant temperature, the current through a conductor is proportional to the potential difference, or $!$ I \\propto V $!$. Experiments show that a conductor's resistance depends on its physical properties: length, cross-sectional area, and the nature of its material. This relationship is captured by the resistivity formula: $!$ R = \\frac{\\rho L}{A} $!$, where $!$ \\rho $!$ is the resistivity," + \
        "Electric power is the rate of energy conversion or work done. In a circuit component like a resistor, power is given by $!$ P = VI $!$, which is dissipated as heat or used to perform work." + \
        "]"
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
