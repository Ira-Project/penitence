from sympy import *
from random import choice
from .question import *
from ..utils import *
from ......input_models import InputModel
import random


async def compute_q1(input: InputModel):
    formulas = input.formula
    explanation = input.explanation

    formulas = "[" + ','.join(formulas) + "]"

    correct_solution = """Correct Solution:
        An adiabatic process is one in which no heat is exchanged with the surroundings.
        Q = 0
        The internal energy of an ideal gas is calculated using U = (3/2)nRT. We compute the initial and final internal energies.
        U_initial = (3/2) * 20 * R * 300\\nU_final = (3/2) * 20 * R * 200
        The first law of thermodynamics states that Q = W + ΔU. With Q = 0, we have W = -ΔU.
        ΔU = U_final - U_initial\n   = (3/2) * 20 * R * (200 - 300)\n   = (3/2) * 20 * R * (-100)\n   = -3000 * R\nW = - (ΔU) = 3000 * R\nTaking R = 8.314 J/(mol·K),\nW = 3000 * 8.314 = 24942 J
        Correct Answer: 24942 J"""

    
    parsed_dict, is_correct_dict = parse_paragraph(explanation, formulas, required_concepts)
    for concept_question in parsed_dict:
        if parsed_dict[concept_question] == "" and concept_question in concept_missing:
            parsed_dict[concept_question] = concept_missing[concept_question]

    # Check if all values in parsed_dict are empty strings
    all_empty = all(value == "" for value in parsed_dict.values())
    # Check if atleast one value in parsed_dict is empty
    atleast_one_empty = any(value == "" for value in parsed_dict.values())

    if all_empty:
        working = random.choice([
            "I couldn't find any relevant concepts or formulas that I could use to solve this question. Please provide more information.",
            "I was unable to proceed with the question. Can you please provide more information to help me solve it?",
            "The provided information seems insufficient to solve this problem. Could you share additional details?",
            "I would need more context or formulas to properly address this question. Can you help me with that information?"
        ])
        answer = "Could not compute."
        is_correct = False
    elif atleast_one_empty:
        working, answer, is_correct = attempt_question_incomplete(question, correct_solution, explanation, formulas, parsed_dict)
    else:
        # Check if all values in is_correct_dict are true
        all_correct = all(value for value in is_correct_dict.values())
        if all_correct:
            working, answer, is_correct = attempt_question_correctly(question, correct_solution, explanation, formulas)
        else:
            working, answer, is_correct = attempt_question_incorrectly(question, correct_solution, explanation, formulas, parsed_dict, is_correct_dict)

    return {
        'status': 200,
        'body': {
            'isCorrect': is_correct,
            'working': working,
            'answer': answer,
            'concepts': []
        }
    }