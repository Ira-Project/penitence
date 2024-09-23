from sympy import *
from .question import *
from ..utils import *
from .....input_models import InputModel
from ..read_explanation import *


# Check if the total mechanical energy is conserved
def check_total_mechanical_energy_conserved(information_check_dict, formulas):
    steps_response = ""
    energy_conserved = False
    energy_conserved_isolated = False
    ke = None
    gpe = None
    working = ""
    if information_check_dict[required_information[1]] == "Yes":
        steps_response = steps_response + \
            "I understand that total mechanical energy of the block is conserved.\n"
        energy_conserved = True
    elif information_check_dict[required_information[1]] == "Wrong" or information_check_dict[required_information[1]] == "No":
        if information_check_dict[required_information[3]] == "Yes":
            steps_response = steps_response + "I understand that an isolated system is one that doesn't exchange any energy with it's surroundings and total mechanical energy is conserved only for an isolated system. The block here can be considered an isolated system and it's total mechanical energy is conserved.\n"
            energy_conserved_isolated = True
            steps_working, ke = find_ke_formula(formulas)
            working = working + steps_working
            steps_working, gpe = find_gpe_formula(formulas)
            working = working + steps_working
        else:
            if information_check_dict[required_information[2]] == "Yes":
                steps_response = steps_response + \
                    "I understand that an isolated system is one that doesn't exchange any energy with it's surroundings but I don't know how it is related to this question.\n"
                return steps_response, energy_conserved, energy_conserved_isolated, ke, gpe

    if information_check_dict[required_information[0]] == "Yes":
        steps_working, ke = find_ke_formula(formulas)
        working = working + steps_working
        steps_working, gpe = find_gpe_formula(formulas)
        working = working + steps_working
        if ke is None or gpe is None:
            return steps_response, energy_conserved, energy_conserved_isolated, ke, gpe

        steps_response = steps_response + \
            "The total mechanical energy of the block is the sum of it's kinetic energy and potential energy but I'm not sure how to solve the question using this information.\n"
    elif information_check_dict[required_information[0]] == "No":

        steps_response = steps_response + \
            "I have no idea how to proceed with this question.\n"

    return steps_response, energy_conserved, energy_conserved_isolated, ke, gpe


def evaluate(information_check_dict, formulas):
    working = ""
    answer = "Could not compute"
    correct = False
    steps_working, energy_conserved, energy_conserved_isolated, ke, gpe = check_total_mechanical_energy_conserved(
        information_check_dict, formulas)
    working = working + steps_working
    if not ke or not gpe:
        print("IB SL WEP Question 5: ", working, answer, correct)
        return working, answer, correct

    if energy_conserved or energy_conserved_isolated:
        working = working + insert_latex("Total ME = E_k + E_p") + "\n"
        total_me = factor(ke) + factor(gpe)
        print("Total ME: ", total_me)
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
            working = working + "The information in the question is not sufficient to solve the problem based on the formula you have given.\n"
            print("IB SL WEP Question 5: ", working, answer, correct)
            return working, answer, correct

    if working == "":
        working = "I am not sure how to solve this problem."

    print("IB SL WEP Question 5: ", working, answer, correct)
    return working, answer, correct


async def compute_q5(input: InputModel):
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
