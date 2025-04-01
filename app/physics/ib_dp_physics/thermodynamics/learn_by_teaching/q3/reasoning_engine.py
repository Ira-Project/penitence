from sympy import *
from random import choice
from .question import *
from ..utils import *
from ......input_models import InputModel
import random


async def compute_q3(input: InputModel):
    formulas = input.formula
    explanation = input.explanation

    formulas = "[" + ','.join(formulas) + "]"

    correct_solution = """Correct Solution:
        A macrostate is any observable state of the system characterized by macroscopic properties such as the number of excited particles.
        A given macrostate (e.g., a specific number of excited particles) can be realized by many different microstates determined by the microscopic arrangements of particles.
        Finally, I apply the Boltzmann entropy formula which relates the number of microstates (W) to the entropy of a given macrostate (S). The change in entropy is computed from the logarithm of the ratio of the microstates in the final and initial macrostates.
        W_{initial} = \\binom{5}{1} = 5 
        W_{final} = \\binom{5}{3} = 10 
        \\Delta S = k_B \\ln W_{final} - k_B \\ln W_{initial} = k_B \\ln(10) - k_B \\ln(5) = k_B \\ln\\left(\\frac{10}{5}\\right) = k_B \\ln(2)
        Correct Answer: k_B \\ln(2)"""

    parsed_dict, is_correct_dict = parse_paragraph(
        explanation, formulas, required_concepts)
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
        working, answer, is_correct = attempt_question_incomplete(
            question, correct_solution, explanation, formulas, parsed_dict)
    else:
        # Check if all values in is_correct_dict are true
        all_correct = all(value for value in is_correct_dict.values())
        if all_correct:
            working, answer, is_correct = attempt_question_correctly(
                question, correct_solution, explanation, formulas)
        else:
            working, answer, is_correct = attempt_question_incorrectly(
                question, correct_solution, explanation, formulas, parsed_dict, is_correct_dict)

    return {
        'status': 200,
        'body': {
            'isCorrect': is_correct,
            'working': working,
            'answer': answer,
            'concepts': []
        }
    }
