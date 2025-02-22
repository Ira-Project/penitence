from sympy import *
from random import choice
from .question import *
from ..utils import *
from ......input_models import InputModel

def compute_correct_answer():
    # Solve the question using the chat completion API
    correct_solution = solve_question(question, required_concepts, required_formulas)

    return correct_solution

async def compute_q1(input: InputModel):
    formulas = input.formula
    explanation = input.explanation

    formulas = "[" + ','.join(formulas) + "]"

    correct_solution = """Correct Solution:
    At t=100 s, there are 1000 nuclides and at t=200 s there are 250, so the decay factor is 1/4.
    $!$\\frac{250}{1000}=\\frac{1}{4}\\,.$!$
    Using the half-life concept, a reduction by 1/2 occurs every half-life. A factor of 1/4 corresponds to 2 half-lives in 100 s, so the half-life is 100/2 = 50 s.
    $!$T_{1/2}=\\frac{100\\,s}{2}=50\\,s\\,.$!$
    Going backwards from t=100 s to t=0, we reverse 2 half-lives which doubles the number each half-life: N = 1000 x 2^2 = 4000.
    $!$N=1000\\times2^2=4000\\,.$!$
    Correct Answer: 4000"""

    working, answer, is_correct = attempt_question(question, required_concepts, required_formulas, correct_solution, explanation, formulas)

    print(working)
    print(answer)
    print(is_correct)

    
    return {
        'status': 200,
        'body': {
            'isCorrect': is_correct,
            'working': working,
            'answer': answer,
            'concepts': []
        }
    }   