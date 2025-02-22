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
        I first calculate the sum of the masses of the individual nucleons. There are 4 nucleons (2 protons and 2 neutrons) with each having 1 u.
        $!$\\text{Sum of nucleon masses} = 2\\,u + 2\\,u = 4\\,u.$!$
        Next, I use the concept that the mass defect is the difference between the sum of the masses and the mass of the element. I take the absolute difference.
        $!$\\Delta m = |(4\\,u) - (4.002603\\,u)| = 0.002603\\,u.$!$
        Finally, employing the formula $!$E=mc^2$!$, the binding energy (energy needed to separate the nucleons) is obtained. Converting 1 u to energy units using 1 u \\( \\approx 931.5\\,MeV/c^2 \\).
        $!$E = \\Delta m\\,c^2 = (0.002603\\,u)\\,c^2 \\approx 0.002603 \\times 931.5\\,MeV \\approx 2.424\\,MeV.$!$
        Correct Answer: $!$2.424\\,MeV$!$"""
    
    working, answer, is_correct = attempt_question(question, required_concepts, required_formulas, correct_solution, explanation, formulas)

    return {
        'status': 200,
        'body': {
            'isCorrect': is_correct,
            'working': working,
            'answer': answer,
            'concepts': []
        }
    }   