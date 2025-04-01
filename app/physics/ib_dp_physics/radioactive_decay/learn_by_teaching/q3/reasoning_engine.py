from sympy import *
from random import choice
from .question import *
from ..utils import *
from ......input_models import InputModel


async def compute_q3(input: InputModel):
    formulas = input.formula
    explanation = input.explanation

    formulas = "[" + ','.join(formulas) + "]"

    correct_solution = """Correct Solution:
        Starting with Uranium-238, which has 92 protons, I apply the alpha decay process. An alpha particle has 2 protons, so upon emission the new nucleus loses 2 protons.
        $!$92 - 2 = 90$!$
        Next, I apply the beta-minus decay process. Beta-minus decay increases the atomic number by 1 by emitting a beta particle.
        $!$90 + 1 = 91$!$
        Correct Answer: 91"""

    working, answer, is_correct = attempt_question(question, required_concepts, correct_solution, explanation, formulas)

    return {
        'status': 200,
        'body': {
            'isCorrect': is_correct,
            'working': working,
            'answer': answer,
            'concepts': []
        }
    }
