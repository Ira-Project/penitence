from sympy import *
from .question import *
from ..utils import *
from .....input_models import InputModel
from ..read_explanation import *


# Find the force
def find_force(information_check_dict):
    steps_response = "Let's first try to find the force. "
    force = None
    if information_check_dict[required_information[0]] == "Yes":
        steps_response = steps_response + \
            "Since acceleration is zero, the net force on box is zero. So, the boy is exerting 300 N of force in the direction opposite friction.\n"
        force = values_dict["Friction"]
        steps_response = steps_response + \
            insert_latex("F = " + combine_value_and_unit("F")) + "\n"
    elif information_check_dict[required_information[0]] == "Wrong":
        steps_response = steps_response + \
            "Even if acceleration is zero, the net force on box may not be zero. So, I don't how to determine the force exerted by the boy to pull the box.\n"
    elif information_check_dict[required_information[0]] == "No":
        steps_response = steps_response + \
            "The question only gives us information on frictional force. I don't how to determine the force exerted by the boy.\n"
    return steps_response, force


# Find the angle between force and displacement
def find_theta(work_formula, information_check_dict):
    steps_response = ""
    if theta in work_formula.free_symbols:
        steps_response = "Let's try to find theta.\n"
    angle = values_dict["theta"]
    angle_unit = units_dict["theta"]
    if information_check_dict[required_information[1]] == "Yes":
        if theta in work_formula.free_symbols:
            steps_response = steps_response + \
                "I understand that we only consider the components of the force that are in the direction of displacement caused by the force.\n"
            steps_response = steps_response + "This component is given by " + \
                insert_latex("F cos(\\theta)") + "\n"
        else:
            steps_response = steps_response + \
                "I understand that we only consider the components of the force that are in the direction of displacement caused by the force.\n"
            steps_response = steps_response + "So we will replace " + \
                insert_latex("F") + " with " + \
                insert_latex("F cos(\\theta)") + "\n"
        correct_work_formula = F*s*cos(theta)
        angle = 0
        if simplify(correct_work_formula / work_formula) != 1:
            work_formula = work_formula.subs(F, F*cos(theta))
            steps_response = steps_response + \
                insert_latex("W = " + latex(work_formula)) + "\n"
    else:
        if theta in work_formula.free_symbols:
            steps_response = steps_response + "As given in the question, theta is " +  str(angle) + " " + angle_unit + ".\n"
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
            "I am not sure how to determine the work done based on the information in the question."
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
        if theta in work_done.free_symbols:
            working = working + insert_latex("W = " + latex(work_done.subs(
                [(F, str(force)), (s, str(values_dict["s"])), (theta, str(angle))]))) + "\n"
            working = working + insert_latex("W = " + latex(work_done.subs(
                [(F, str(force)), (s, values_dict["s"]), (theta, angle)])) + answer_unit_into_1000) + "\n"
            answer = N(work_done.subs(
                [(F, values_dict["F"]), (s, values_dict["s"]), (theta, angle)])) / 1000
        else:
            working = working + insert_latex("W = " + latex(work_done.subs(
                [(F, str(force)), (s, str(values_dict["s"]))]))) + "\n"
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
        working = working + "The information in the question is not sufficient to solve the problem based on the formula you have given."

    if working == "":
        working = "I am not sure how to solve this problem."

    print("IB SL WEP Question 1: ", working, answer, correct)
    return working, answer, correct


async def compute_q1(input: InputModel):
    formulas = input.formula
    explanation = input.explanation

    formulas = "[" + ','.join(formulas) + "]"

    information_check_dict = read_explanation(
        required_information, explanation, check_only_required=True)
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
