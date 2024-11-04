from sympy import *
from random import choice
from .question import *
from ..utils import *
from .....input_models import InputModel
from ..read_explanation import *


# Find the force
def find_force(information_check_dict):
    steps_response = "Let's first try to find the force.\n"
    force = None
    if information_check_dict[question_concepts[0]] == "Correct":
        steps_response = steps_response + choice(concept_responses[question_concepts[0]]) + "\n"
        force = values_dict["Friction"]
        steps_response = steps_response + \
            insert_latex("F = " + combine_value_and_unit("F")) + "\n"
    elif information_check_dict[question_concepts[0]] == "Not Present":
        steps_response = steps_response + choice(concept_not_mentioned_responses[question_concepts[0]]) + "\n"
    elif information_check_dict[question_concepts[0]] in unknown_concepts_partial_answers[question_concepts[0]]:
        steps_response = steps_response + choice(partial_concept_responses[information_check_dict[question_concepts[0]]]) + "\n"
    return steps_response, force


# Find the angle between force and displacement
def find_theta(work_formula, information_check_dict):
    steps_response = ""
    if theta in work_formula.free_symbols:
        steps_response = "Let's try to find theta.\n"
    angle = values_dict["theta"]
    if information_check_dict[question_concepts[1]] == "Correct":
        if theta in work_formula.free_symbols:
            steps_response = steps_response + choice(concept_responses[question_concepts[1]]) + "\n"
            steps_response = steps_response + "So, " + insert_latex("F cos(\\theta) = " + combine_value_and_unit("F")) + "\n"
        else:
            steps_response = steps_response + choice(concept_not_mentioned_responses[question_concepts[1]]) + "\n"
            steps_response = steps_response + "This is given by " + insert_latex("F = " + combine_value_and_unit("F")) + "\n"
        correct_work_formula = F*s*cos(theta)
        angle = 0
        if simplify(correct_work_formula / work_formula) != 1:
            work_formula = work_formula.subs(F, F*cos(theta))
            steps_response = steps_response + \
                insert_latex("W = " + latex(work_formula)) + "\n"
    elif information_check_dict[question_concepts[1]] in unknown_concepts_partial_answers[question_concepts[1]]:
        steps_response = steps_response + choice(partial_concept_responses[information_check_dict[question_concepts[1]]]) + "\n"
    else:
        if theta in work_formula.free_symbols:
            steps_response = steps_response + "As given in the question, theta is " +  combine_value_and_unit("theta") + ".\n"
    return steps_response, angle, work_formula


# Evaluate the question
def evaluate(information_check_dict, formula):
    working = ""
    answer = "Could not compute"
    correct = False
    steps_working, work_done = find_work_formula(formula)
    working = working + steps_working
    if work_done is None:
        print("IB SL WEP Question 1: ", working, answer, correct)
        return working, answer, correct

    if F not in work_done.free_symbols and s not in work_done.free_symbols:
        working = working + \
            choice([
                "I am not sure how to determine the work done based on the formula and the information provided in the question.",
                "Based on the given formula and information in the question, I cannot calculate the work done.",
                "Using the formula and information provided in the question, I cannot compute the work done.",
                "I am unable to calculate work done with the formula and available information in the question.",
                "The provided formula and question details don't allow me to calculate the work done."
            ])
        print("IB SL WEP Question 1: ", working, answer, correct)
        return working, answer, correct

    steps_working, force = find_force(information_check_dict)
    working = working + steps_working
    if not force:
        print("IB SL WEP Question 1: ", working, answer, correct)
        return working, answer, correct
    steps_working, angle, work_done = find_theta(
        work_done, information_check_dict)
    working = working + steps_working

    try:
        working = working + insert_latex("s = " + combine_value_and_unit("s")) + "\n"
        if theta in work_done.free_symbols:
            working = working + insert_latex("W = " + latex(work_done.subs(
                [(F, UnevaluatedExpr(force)), (s, values_dict["s"]), (theta, angle)])) + answer_unit_into_1000) + "\n"
            working = working + insert_latex("W = " + latex(N(work_done.subs(
                [(F, force), (s, values_dict["s"]), (theta, angle)]))) + answer_unit_into_1000) + "\n"
            answer = N(work_done.subs(
                [(F, values_dict["F"]), (s, values_dict["s"]), (theta, angle)])) / 1000
        else:
            working = working + insert_latex("W = " + latex(work_done.subs(
                [(F, UnevaluatedExpr(force)), (s, values_dict["s"])])) + answer_unit_into_1000) + "\n"
            working = working + insert_latex("W = " + latex(work_done.subs(
                [(F, force), (s, values_dict["s"])])) + answer_unit_into_1000) + "\n"
            answer = N(work_done.subs(
                [(F, values_dict["F"]), (s, values_dict["s"])])) / 1000
        working = working + \
            insert_latex("W = " + '{:.2f}'.format(answer) + answer_unit)
        if abs(answer - answer_value) < 0.00001:
            correct = True
        answer = '{:.2f}'.format(answer) + answer_unit
    except Exception as e:
        # Intended exception occured
        working = working + choice([
            "The information in the question is not sufficient to solve the problem based on the formula you have given.",
            "Based on your formula and the question details provided, there isn't enough information to solve this problem.",
            "I cannot proceed further with the given formula as the question lacks sufficient information needed for the formula.",
            "The question lacks sufficient information needed to solve this using your formula.",
            "With the formula you provided and the available information in the question, I cannot proceed further."
        ])

    if working == "":
        working = choice([
            "I am not sure how to solve this problem.",
            "I cannot determine how to solve this problem.",
            "The approach to solve this problem is unclear to me.",
            "I'm unable to identify the correct method to solve this problem.",
            "I don't know how to solve this problem."
        ])

    print("IB SL WEP Question 1: ", working, answer, correct)
    return working, answer, correct


async def compute_q1(input: InputModel):
    formulas = input.formula
    explanation = input.explanation

    formulas = "[" + ','.join(formulas) + "]"

    information_check_dict, procedural_check = read_explanation(
        question_concepts, explanation, check_only_required=True)
    if procedural_check:
        working = choice(procedural_explanation_responses)
        answer = "Could not compute"
        correct = False
    else:
        working, answer, correct = evaluate(information_check_dict, formulas)
        

    return {
        'status': 200,
        'body': {
            'isCorrect': correct,
            'working': working,
            'answer': str(answer),
            'concepts': []
        }
    }
