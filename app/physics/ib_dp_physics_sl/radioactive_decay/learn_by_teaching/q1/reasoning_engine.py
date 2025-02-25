from sympy import *
from random import choice
from .question import *
from ..utils import *
from ......input_models import InputModel


async def compute_q1(input: InputModel):
    formulas = input.formula
    explanation = input.explanation

    formulas = "[" + ','.join(formulas) + "]"

    correct_solution = """Correct Solution:
        I use the concept that half-life is the time required for the amount of radioactive nuclides to be reduced by half.
        $!$\\text{Given half-life} = 50\\,s, \\quad \\text{Time elapsed} = 100\\,s, \\quad \\text{Number of half-lives} = \\frac{100}{50} = 2\\,.$!
        Applying the law of radioactive decay, the sample is halved each half-life. After 2 half-lives, the number is reduced by a factor of 2^2.
        $!$N_{final} = \\frac{1000}{2^2} = \\frac{1000}{4} = 250\\,.$!
        Correct Answer: 250"""

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