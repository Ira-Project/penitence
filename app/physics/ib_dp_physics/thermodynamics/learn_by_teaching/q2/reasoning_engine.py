from sympy import *
from random import choice
from .question import *
from ..utils import *
from ......input_models import InputModel
import random


async def compute_q2(input: InputModel):
    formulas = input.formula
    explanation = input.explanation

    formulas = "[" + ','.join(formulas) + "]"

    correct_solution = """Correct Solution:
        A macrostate is any observable or measurable state of a system, characterized by macroscopic properties. Here, the macrostate is given by the number of particles in the excited state. Thus, each macrostate corresponds to an integer number n, where 0 ≤ n ≤ 2. 
        The possible macrostates are n = 0, 1, 2.
        Each macrostate (with n excited particles) can be realized by many corresponding microstates defined by the specific arrangement of particles. The total number of microstates for a given n is given by the binomial coefficient.
        \\Omega(n) = \\binom{N}{n} = \\frac{N!}{n! (N-n)!}.
        The most probable macrostate is the one with the highest number of corresponding microstates.
        \\Omega(0) = 1, \\Omega(1) = 2, \\Omega(2) = 1.
        Therefore, the most probable macrostate is n = 1.
        Correct Answer: One excited particle and one normal particle"""

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
                question, correct_solution, explanation, formulas, insert_latex_final_answer=False)
        else:
            working, answer, is_correct = attempt_question_incorrectly(
                question, correct_solution, explanation, formulas, parsed_dict, is_correct_dict, insert_latex_final_answer=False)

    if is_correct:
        answer = "One excited particle and one normal particle"

    return {
        'status': 200,
        'body': {
            'isCorrect': is_correct,
            'working': working,
            'answer': answer,
            'concepts': []
        }
    }
