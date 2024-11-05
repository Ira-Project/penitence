from sympy import *
from random import choice
from .question import *
from ..utils import *
from .....input_models import InputModel
from ..read_explanation import *


# Find the work done in changing the velocity
def find_work_done_ke(information_check_dict, formula):
    steps_response = ""
    work_done = None
    ke_formula = None

    if information_check_dict[question_concepts[0]] == "Correct":
        steps_response = steps_response + choice(concept_responses[question_concepts[0]]) + "\n"
        if information_check_dict[question_concepts[1]] == "Correct":
            steps_response = steps_response + choice(concept_responses[question_concepts[1]])
            steps_response = steps_response + "The work done is equal to the change in kinetic energy of the football." + "\n"
            steps_response = steps_response + "So, " + insert_latex("W = \\Delta E_k") + "\n"

            steps_working, ke_formula = find_ke_formula(formula)
            steps_response = steps_response + steps_working

            if ke_formula is None:
                return steps_response, work_done, ke_formula

            work_done = ke_formula
            if v in work_done.free_symbols or v_1 in work_done.free_symbols or v_2 in work_done.free_symbols:
                if v in work_done.free_symbols:
                    work_done = work_done.subs(v**2, v_final**2 - v_initial**2)
                if v_1 in work_done.free_symbols:
                    work_done = work_done.subs(v_1, v_initial)
                if v_2 in work_done.free_symbols:
                    work_done = work_done.subs(v_2, v_final)

            steps_response = steps_response + insert_latex("W = " + latex(work_done)) + "\n"
        elif information_check_dict[question_concepts[1]] == "an object has kinetic energy":
            steps_response = steps_response + choice(partial_concept_responses[information_check_dict[question_concepts[1]]]) + "\n"   
        else:
            steps_response = steps_response + choice(concept_not_mentioned_responses[question_concepts[1]]) + "\n"
    elif information_check_dict[question_concepts[0]] in unknown_concepts_partial_answers[question_concepts[0]]:
        steps_response = steps_response + choice(partial_concept_responses[information_check_dict[question_concepts[0]]]) + "\n"
        if information_check_dict[question_concepts[0]] == "work is equal to change in kinetic energy":
            steps_response = steps_response + "So, " + insert_latex("W = \\Delta E_k") + "\n"

            steps_working, ke_formula = find_ke_formula(formula)
            steps_response = steps_response + steps_working

            if ke_formula is None:
                return steps_response, work_done, ke_formula
            
            work_done = ke_formula
            if v in work_done.free_symbols or v_1 in work_done.free_symbols or v_2 in work_done.free_symbols:
                if v in work_done.free_symbols:
                    work_done = work_done.subs(v**2, v_final**2 - v_initial**2)
                if v_1 in work_done.free_symbols:
                    work_done = work_done.subs(v_1, v_initial)
                if v_2 in work_done.free_symbols:
                    work_done = work_done.subs(v_2, v_final)
    else:
        _, work_done = find_work_formula(formula)
        if work_done:
            steps_response = steps_response + choice([
                "Using the formula that you have given for work done, I am not sure how to find the work done by friction.\n",
                "Based on your provided formula for work done, I don't know how to calculate the work done by friction.\n",
                "The work done formula you've provided doesn't allow me to calculate the work done by friction.\n",
                "I'm unable to compute the work done by friction using your given formula for work done.\n",
                "The formula you provided for work done doesn't give me enough information to determine the work done by friction.\n",
            ])
        else:
            steps_response = steps_response + choice(concept_not_mentioned_responses[question_concepts[0]]) + "\n"
    return steps_response, work_done, ke_formula


# Evaluate the question
def evaluate(information_check_dict, formula):
    working = ""
    answer = "Could not compute"
    correct = False

    try:
        steps_working, work_done, ke = find_work_done_ke(information_check_dict, formula)
        working = working + steps_working
        if ke is None:
            print("IB SL WEP Question 3: ", working, answer, correct)
            return working, answer, correct
    except ImportError as e:
        # Intended exception to handle case where some variables are not present in the formula
        working = working + choice([
            "I understand that the work done in changing the velocity of the football is equal to the change in kinetic energy of the football. The information in the question is not sufficient to solve the problem based on the formula you have given.\n",
            "The relationship between work done and kinetic energy change of the football is clear. But the information in the question is not sufficient to solve the problem based on the formula you have given.\n",
            "I can see that work done should equal the change in kinetic energy of the football, but using the provided formula, the question is missing key information needed for the calculation.\n",
            "While I know that work done equals the football's change in kinetic energy, I cannot complete the calculation with the formula you have provided and the information given in the question.\n",
            "Although the principle of work done equaling the football's change in kinetic energy applies here, the question is missing some information needed to solve the problem using the formula you have given.\n",
        ])
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
        working = working + choice([
            "The information in the question is not sufficient to solve the problem based on the formula you have given.",
            "Based on your formula and the question details provided, there isn't enough information to solve this problem.",
            "I cannot proceed further with the given formula as the question lacks sufficient information needed for the formula.",
            "The question lacks sufficient information needed to solve this using your formula.",
            "With the formula you provided and the available information in the question, I cannot proceed further."
        ])

    print("IB SL WEP Question 3: ", working, answer, correct)

    if working == "":
        working = choice([
            "I am not sure how to solve this problem.",
            "I cannot determine how to solve this problem.",
            "The approach to solve this problem is unclear to me.",
            "I'm unable to identify the correct method to solve this problem.",
            "I don't know how to solve this problem."
        ])

    return working, answer, correct


async def compute_q3(input: InputModel):
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
