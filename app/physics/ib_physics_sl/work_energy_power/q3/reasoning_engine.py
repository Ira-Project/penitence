from sympy import *
from .question import *
from ..utils import *
from .....input_models import InputModel
from ..read_explanation import *


# Find the work done in changing the velocity
def find_work_done_ke(information_check_dict, formula):
    steps_response = ""
    work_done = None
    if information_check_dict[required_information[0]] == "Yes":
        steps_response = steps_response + \
            "I understand that the work done in changing the velocity of the football is equal to the change in kinetic energy of the football.\n"
        steps_response = steps_response + "This is given by " + \
            insert_latex("\\Delta E_k") + "\n"

        steps_working, ke_formula = find_ke_formula(formula)
        steps_response = steps_response + steps_working

        if ke_formula is None:
            return steps_response, work_done, ke_formula

        if v in ke_formula.free_symbols:
            work_done = ke_formula.subs(v**2, v_final**2 - v_initial**2)
        else:
            work_done = ke_formula
        steps_response = steps_response + \
            insert_latex("W = " + latex(work_done)) + "\n"
    else:
        steps_response = steps_response + \
            "I am not sure how to calculate the work done based on the formulas given.\n"
    return steps_response, work_done, ke_formula


# Evaluate the question
def evaluate(information_check_dict, formula):
    working = ""
    answer = "Could not compute"
    correct = False

    try:
        steps_working, work_done, ke = find_work_done_ke(
            information_check_dict, formula)
        working = working + steps_working
        if ke is None:
            print("IB SL WEP Question 3: ", working, answer, correct)
            return working, answer, correct

    except Exception as E:
        # Intended exception to handle case where some variables are not present in the formula
        working = working + "I understand that the work done in changing the velocity of the football is equal to the change in kinetic energy of the football. The information in the question is not sufficient to solve the problem based on the formula you have given.\n"
        print("IB SL WEP Question 3: ", working, answer, correct)
        return working, answer, correct
    try:
        working = working + insert_latex("W = " + latex(work_done.subs([(m, str(values_dict["m"])), (
            v_initial, str(values_dict["v_initial"])), (v_final, str(values_dict["v_final"]))]))) + "\n"
        working = working + insert_latex("W = " + latex(work_done.subs(
            [(m, values_dict["m"]), (v_initial, values_dict["v_initial"]), (v_final, values_dict["v_final"])]))) + "\n"
        answer = N(work_done.subs([(m, values_dict["m"]), (v_initial,
                   values_dict["v_initial"]), (v_final, values_dict["v_final"])]))
        working = working + \
            insert_latex("W = " + latex(answer) + answer_unit) + "\n"
        if answer - answer_value < 0.00001:
            correct = True
        answer = '{:.2f}'.format(answer) + answer_unit
    except Exception as e:
        working = working + "The information in the question is not sufficient to solve the problem based on the formula you have given.\n"

    print("IB SL WEP Question 3: ", working, answer, correct)

    if working == "":
        working = "I am not sure how to solve this problem."

    return working, answer, correct


async def compute_q3(input: InputModel):
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
