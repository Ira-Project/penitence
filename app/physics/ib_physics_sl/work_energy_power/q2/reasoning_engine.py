from sympy import *
from .question import *
from ..utils import *
from .....input_models import InputModel
from ..read_explanation import *


# Find the work done against gravity
def find_work_done_gpe(information_check_dict, formula):
    steps_response = ""
    work_done = None
    if information_check_dict[required_information[0]] == "Yes":
        steps_response = steps_response + \
            "I understand that the work done in lifting the dumbbell against gravity is the same as the change in gravitational potential energy of the dumbbell.\n"
        steps_response = steps_response + "This is given by " + \
            insert_latex("\\Delta Gravitational Potential Energy (E_p)") + "\n"
        steps_working, gpe_formula = find_gpe_formula(formula)
        steps_response = steps_response + steps_working
        if gpe_formula is None:
            return steps_response, work_done, gpe_formula

        if h in gpe_formula.free_symbols:
            work_done = gpe_formula.subs(h, h_final - h_initial)
        else:
            work_done = gpe_formula
        steps_response = steps_response + \
            insert_latex("W = " + latex(work_done)) + "\n"
    else:
        steps_response = steps_response + \
            "I am not sure how to calculate the work done based on the formulas given.\n"
    return steps_response, work_done, gpe_formula


# Evaluate the question
def evaluate(information_check_dict, formula):
    working = ""
    answer = "Could not compute"
    correct = False
    try:
        steps_working, work_done, gpe = find_work_done_gpe(
            gpe, information_check_dict, formula)
        working = working + steps_working
        if gpe is None:
            print("IB SL WEP Question 2: ", working, answer, correct)
            return working, answer, correct
    except Exception as E:
        # Intended exception to handle case where some variables are not present in the formula
        working = working + "I understand that the work done in lifting the dumbbell against gravity is the same as the change in gravitational potential energy of the dumbbell. The information in the question is not sufficient to solve the problem based on the formula you have given.\n"
        print("IB SL WEP Question 2: ", working, answer, correct)
        return working, answer, correct
    try:
        working = working + insert_latex("W = " + latex(work_done.subs([(m, str(values_dict["m"])), (g, str(
            values_dict["g"])), (h_initial, str(values_dict["h1"])), (h_final, str(values_dict["h2"]))]))) + "\n"
        working = working + insert_latex("W = " + latex(work_done.subs([(m, values_dict["m"]), (
            g, values_dict["g"]), (h_initial, values_dict["h1"]), (h_final, values_dict["h2"])])) + answer_unit) + "\n"
        answer = N(work_done.subs([(m, values_dict["m"]), (g, values_dict["g"]), (
            h_initial, values_dict["h1"]), (h_final, values_dict["h2"])]))
        working = working + \
            insert_latex("W = " + '{:.2f}'.format(answer) + answer_unit)
        if abs(answer - answer_value) < 0.00001:
            correct = True
        answer = '{:.2f}'.format(answer) + answer_unit
    except Exception as e:
        # Intended exception to handle case where some variables are not present in the formula
        working = working + "The information in the question is not sufficient to solve the problem based on the formula you have given."

    if working == "":
        working = "I am not sure how to solve this problem."

    print("IB SL WEP Question 2: ", working, answer, correct)
    return working, answer, correct


async def compute_q2(input: InputModel):
    formulas = input.formula
    explanation = input.explanation

    formulas = "[" + ','.join(formulas) + "]"

    information_check_dict = read_explanation(
        required_information, explanation)
    working, answer, correct = evaluate(information_check_dict, formulas)

    return {
        'status': 200,
        'body': {
            'isCorrect': correct,
            'working': working,
            'answer': answer,
            'concepts': []
        }
    }
