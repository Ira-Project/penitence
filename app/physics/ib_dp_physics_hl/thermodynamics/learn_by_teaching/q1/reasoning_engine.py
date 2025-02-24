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
        I note that the process is adiabatic, meaning no heat is exchanged (Q = 0).
        $!$Q = 0!$
        Using the first law of thermodynamics, Q = W + ΔU. For this adiabatic process, 0 = W + ΔU so that W = - ΔU.
        $!$0 = W + \\Delta U \\quad \\Rightarrow \\quad W = -\\Delta $!$
        The internal energy of an ideal gas is given by U = (3/2) n R T. Thus, the change in internal energy is \\Delta U = (3/2) n R (T₂ - T₁).
        $!$\\Delta U = \\frac{3}{2}nR(T_2 - T_1)$!$
        Substitute the given values: n = 20 mol, T₁ = 300 K, and T₂ = 200 K. Hence, T₂ - T₁ = -100 K.
        $!$\\Delta U = \\frac{3}{2} \\times 20 \\times R \\times (200 - 300) = \\frac{3}{2} \\times 20 \\times R \\times (-100)$!$
        Calculate the work done by the gas: W = - ΔU. Simplify the expression.
        $!$W = -\\Delta U = -\\left( \\frac{3}{2} \\times 20 \\times R \\times (-100) \\right) = \\frac{3}{2} \\times 20 \\times R \\times 100$!$
        Simplify numerical factors, then substitute R (\\approx) 8.314 J/mol·K to get the final work done.
        $!$\\frac{3}{2} \\times 20 = 30, \\quad \\text{thus} \\quad W = 30 \\times 100 \\times 8.314 = 3000 \\times 8.314 \\approx 24942\\:J$!$
        Correct Answer: 24942 J"""

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