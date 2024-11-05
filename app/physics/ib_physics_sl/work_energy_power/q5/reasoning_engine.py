from sympy import *
from random import choice
from .question import *
from ..utils import *
from .....input_models import InputModel
from ..read_explanation import *


# Check if the total energy is conserved
def check_total_energy_conserved(information_check_dict, formulas):
    steps_response = ""
    energy_conserved = False
    energy_conserved_isolated = False
    ke = None
    gpe = None
    working = ""
    if information_check_dict[question_concepts[3]] == "Correct":
        energy_conserved_isolated = True
    if information_check_dict[question_concepts[2]] == "Correct":
        steps_response = steps_response + choice(concept_responses[question_concepts[2]]) + "\n"
        energy_conserved = True
        if information_check_dict[question_concepts[0]] == "Correct" and information_check_dict[question_concepts[1]] == "Correct":
            steps_response = steps_response + choice(concept_responses[question_concepts[0]]) + " "
            steps_response = steps_response + choice(concept_responses[question_concepts[1]]) + "\n"
            steps_working, ke = find_ke_formula(formulas)
            steps_response = steps_response + steps_working
            steps_working, gpe = find_gpe_formula(formulas)
            steps_response = steps_response + steps_working
            return steps_response, energy_conserved, energy_conserved_isolated, ke, gpe
        elif information_check_dict[question_concepts[0]] == "Correct" and information_check_dict[question_concepts[1]] != "Correct":
            steps_response = steps_response + choice(concept_responses[question_concepts[0]]) + "\n"
            steps_working, ke = find_ke_formula(formulas)
            steps_response = steps_response + steps_working
            if information_check_dict[question_concepts[1]] in unknown_concepts_partial_answers[question_concepts[1]]:
                steps_response = steps_response + choice(partial_concept_responses[information_check_dict[question_concepts[1]]]) + "\n"
                return steps_response, energy_conserved, energy_conserved_isolated, ke, gpe
            else:
                return steps_response, energy_conserved, energy_conserved_isolated, ke, gpe
        elif information_check_dict[question_concepts[0]] != "Correct" and information_check_dict[question_concepts[1]] == "Correct":
            steps_response = steps_response + choice(concept_responses[question_concepts[1]]) + "\n"
            steps_working, gpe = find_gpe_formula(formulas)
            steps_response = steps_response + steps_working
            if information_check_dict[question_concepts[0]] in unknown_concepts_partial_answers[question_concepts[0]]:
                steps_response = steps_response + choice(partial_concept_responses[information_check_dict[question_concepts[0]]]) + "\n"
                return steps_response, energy_conserved, energy_conserved_isolated, ke, gpe
            else:
                return steps_response, energy_conserved, energy_conserved_isolated, ke, gpe
        else:
            if information_check_dict[question_concepts[0]] in unknown_concepts_partial_answers[question_concepts[0]]:
                steps_response = steps_response + choice(partial_concept_responses[information_check_dict[question_concepts[0]]]) + "\n"
            if information_check_dict[question_concepts[1]] in unknown_concepts_partial_answers[question_concepts[1]]:
                steps_response = steps_response + choice(partial_concept_responses[information_check_dict[question_concepts[1]]]) + "\n"
            steps_response = steps_response + choice([
                "I am not sure how to proceed using just the information you have given.\n",
                "With this information provided, I cannot determine how to proceed with solving this question.\n",
                "The given information seems insufficient for me to continue solving this problem.\n",
                "I need additional information to proceed with solving this question.\n",
                "Based on this information alone, I cannot determine how to proceed.\n"
            ])
            return steps_response, energy_conserved, energy_conserved_isolated, ke, gpe
    elif information_check_dict[question_concepts[2]] in unknown_concepts_partial_answers[question_concepts[2]]:
        steps_response = steps_response + choice(partial_concept_responses[information_check_dict[question_concepts[2]]]) + "\n"
        return steps_response, energy_conserved, energy_conserved_isolated, ke, gpe
    else:
        if information_check_dict[question_concepts[0]] == "Correct" and information_check_dict[question_concepts[1]] == "Correct":
            steps_response = steps_response + choice(concept_responses[question_concepts[0]]) + " "
            steps_response = steps_response + choice(concept_responses[question_concepts[1]]) + "\n"
            steps_working, ke = find_ke_formula(formulas)
            steps_response = steps_response + steps_working
            steps_working, gpe = find_gpe_formula(formulas)
            steps_response = steps_response + steps_working
            return steps_response, energy_conserved, energy_conserved_isolated, ke, gpe
        elif information_check_dict[question_concepts[0]] == "Correct" and information_check_dict[question_concepts[1]] != "Correct":
            steps_response = steps_response + choice(concept_responses[question_concepts[0]]) + "\n"
            steps_working, ke = find_ke_formula(formulas)
            steps_response = steps_response + steps_working
            if information_check_dict[question_concepts[1]] in unknown_concepts_partial_answers[question_concepts[1]]:
                steps_response = steps_response + choice(partial_concept_responses[information_check_dict[question_concepts[1]]]) + "\n"
                return steps_response, energy_conserved, energy_conserved_isolated, ke, gpe
            else:
                return steps_response, energy_conserved, energy_conserved_isolated, ke, gpe
        elif information_check_dict[question_concepts[0]] != "Correct" and information_check_dict[question_concepts[1]] == "Correct":
            steps_response = steps_response + choice(concept_responses[question_concepts[1]]) + "\n"
            steps_working, gpe = find_gpe_formula(formulas)
            steps_response = steps_response + steps_working
            if information_check_dict[question_concepts[0]] in unknown_concepts_partial_answers[question_concepts[0]]:
                steps_response = steps_response + choice(partial_concept_responses[information_check_dict[question_concepts[0]]]) + "\n"
                return steps_response, energy_conserved, energy_conserved_isolated, ke, gpe
            else:
                return steps_response, energy_conserved, energy_conserved_isolated, ke, gpe 
        else:
            if information_check_dict[question_concepts[0]] in unknown_concepts_partial_answers[question_concepts[0]]:
                steps_response = steps_response + choice(partial_concept_responses[information_check_dict[question_concepts[0]]]) + "\n"
            if information_check_dict[question_concepts[1]] in unknown_concepts_partial_answers[question_concepts[1]]:
                steps_response = steps_response + choice(partial_concept_responses[information_check_dict[question_concepts[1]]]) + "\n"
            steps_response = steps_response + choice([
                "I am not sure how to proceed using just the information you have given.\n",
                "With this information provided, I cannot determine how to proceed with solving this question.\n",
                "The given information seems insufficient for me to continue solving this problem.\n",
                "I need additional information to proceed with solving this question.\n",
                "Based on this information alone, I cannot determine how to proceed.\n"
            ])
            return steps_response, energy_conserved, energy_conserved_isolated, ke, gpe


def evaluate(information_check_dict, formulas):
    working = ""
    answer = "Could not compute"
    correct = False
    steps_working, energy_conserved, energy_conserved_isolated, ke, gpe = check_total_energy_conserved(information_check_dict, formulas)
    working = working + steps_working
    if ke and not gpe:
        working = working + choice([
            "Using just the information you have given about kinetic energy, I cannot determine how to proceed with solving this question.\n",
            "With only the kinetic energy information provided, I cannot complete the solution to this problem.\n",
            "The kinetic energy concepts alone seem to be insufficient to solve this question completely.\n",
            "I would need additional information beyond kinetic energy to solve this problem.\n",
            "I am not sure how to solve this question using only the information about kinetic energy you've provided.\n"
        ])
        return working, answer, correct
    elif not ke and gpe:
        working = working + choice([
            "Using just the information you have given about potential energy, I cannot determine how to proceed with solving this question.\n",
            "With only the potential energy information provided, I cannot complete the solution to this problem.\n",
            "The potential energy concepts alone seem to be insufficient to solve this question completely.\n",
            "I would need additional information beyond potential energy to solve this problem.\n",
            "I am not sure how to solve this question using only the information about potential energy you've provided.\n"
        ])
        return working, answer, correct
    elif not ke and not gpe:
        print("IB SL WEP Question 5: ", working, answer, correct)
        return working, answer, correct

    if energy_conserved:
        working = working + insert_latex("Total energy = E_k + E_p") + "\n"
        total_me = factor(ke) + factor(gpe)
        print("Total energy: ", total_me)
        working = working + \
            insert_latex(
                "E_{{k_{{initial}}}} + E_{{p_{{initial}}}} = E_{{k_{{final}}}} + E_{{p_{{final}}}}") + "\n"
        try:
            if v_1 in total_me.free_symbols and v_2 in total_me.free_symbols:
                total_me = total_me.subs([((v_1 - v_2)*(v_1 + v_2), -v**2)])
            if h_1 in total_me.free_symbols and h_2 in total_me.free_symbols:
                total_me = total_me.subs([(h_2 - h_1, h)])
            working = working + insert_latex(latex(total_me.subs([(m, m), (v, "v_initial"), (g, "g"), (h, "h")])) + " = " + latex(
                total_me.subs([(m, "m"), (v, "v_final"), (g, "g"), (h, 0)]))) + "\n"
            total_me_equation = Eq(total_me.subs([(m, values_dict["m"]), (v, values_dict["v_initial"]), (g, values_dict["g"]), (
                h, values_dict["h"])]), total_me.subs([(m, values_dict["m"]), (v, "v_final"), (g, values_dict["g"]), (h, 0)]))
            working = working + insert_latex(latex(total_me_equation)) + "\n"
            answer_array = solve(total_me_equation, v_final)
            for val in answer_array:
                if val > 0:
                    answer = val
                    break
            working = working +\
                insert_latex("v_{{final}} =" +
                             '{:.2f}'.format(answer) + answer_unit) + "\n"
            if abs(answer - answer_value) < 0.00001:
                correct = True
            answer = '{:.2f}'.format(
                answer) + answer_unit

        except Exception as e:
            # Intended exception to handle case where some variables are not present in the formula
            working = working + choice([
                "The information in the question is not sufficient to solve the problem based on the formula you have given.",
                "Based on your formula and the question details provided, there isn't enough information to solve this problem.",
                "I cannot proceed further with the given formula as the question lacks sufficient information needed for the formula.",
                "The question lacks sufficient information needed to solve this using your formula.",
                "With the formula you provided and the available information in the question, I cannot proceed further."
        ])
            print("IB SL WEP Question 5: ", working, answer, correct)
            return working, answer, correct

    if working == "":
        working = choice([
            "I am not sure how to solve this problem.",
            "I cannot determine how to solve this problem.",
            "The approach to solve this problem is unclear to me.",
            "I'm unable to identify the correct method to solve this problem.",
            "I don't know how to solve this problem."
        ])

    print("IB SL WEP Question 5: ", working, answer, correct)
    return working, answer, correct


async def compute_q5(input: InputModel):
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
