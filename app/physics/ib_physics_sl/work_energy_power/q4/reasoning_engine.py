from sympy import *
from .question import *
from ..utils import *
from .....input_models import InputModel
from ..read_explanation import *


# Find the work done in changing the velocity
def find_work_done_ke(information_check_dict, formula):
    steps_response = ""
    work_done = None
    compute_using_alternate_formula = False
    if information_check_dict[required_information[0]] == "Yes":
        steps_response = steps_response + \
            "I understand that the work done in dragging the box is equal to the change in kinetic energy of the box.\n"
        steps_response = steps_response + "This is given by " + \
            insert_latex("\\Delta E_k") + "\n"

        steps_working, ke_formula = find_ke_formula(formula)
        steps_response = steps_response + steps_working

        if ke_formula is None:
            return steps_response, work_done, ke_formula

        work_done = ke_formula
        if v in work_done.free_symbols or v_1 in work_done.free_symbols or v_2 in work_done.free_symbols:
            if v in work_done.free_symbols:
                work_done = work_done.subs(v, v_final - v_initial)
            if v_1 in work_done.free_symbols:
                work_done = work_done.subs(v_1, v_initial)
            if v_2 in work_done.free_symbols:
                work_done = work_done.subs(v_2, v_final)

        steps_response = steps_response + \
            insert_latex("W = " + latex(work_done)) + "\n"
    else:
        compute_using_alternate_formula = True

    return steps_response, work_done, ke_formula, compute_using_alternate_formula


# Check if the total mechanical energy is conserved
def check_total_mechanical_energy_conserved(information_check_dict, formulas):
    steps_response = ""
    energy_conserved = False
    energy_conserved_isolated = False
    if information_check_dict[required_information[1]] == "Yes":
        steps_response = steps_response + \
            "I understand that total mechanical energy of the block is conserved.\n"
        energy_conserved = True
    elif information_check_dict[required_information[1]] == "Wrong":
        if information_check_dict[required_information[3]] == "Yes":
            if information_check_dict[required_information[2]] == "Yes":
                steps_response = steps_response + "I understand that an isolated system is one that doesn't exchange any energy with it's surroundings and total mechanical energy is conserved only for an isolated system. The block here can be considered an isolated system and it's total mechanical energy is conserved.\n"
                energy_conserved_isolated = True
            else:
                steps_response = steps_response + \
                    "I understand that total mechanical energy is only conserved for an isolated system but I am not sure what is an isolated system and I don't know if the block is isolated or not.\n"
                return steps_response, energy_conserved, energy_conserved_isolated
        else:
            if information_check_dict[required_information[2]] == "Yes":
                steps_response = steps_response + \
                    "I understand that an isolated system is one that doesn't exchange any energy with it's surroundings but I don't know how it is related to this question.\n"
                return steps_response, energy_conserved, energy_conserved_isolated

    if information_check_dict[required_information[0]] == "Yes":
        steps_working, ke = find_ke_formula(formulas)
        working = working + steps_working
        steps_working, gpe = find_gpe_formula(formulas)
        working = working + steps_working
        if ke is None or gpe is None:
            return steps_response, energy_conserved, energy_conserved_isolated, ke, gpe

        steps_response = steps_response + \
            "Also the total mechanical energy of the block is the sum of it's kinetic energy and potential energy.\n"
    elif information_check_dict[required_information[0]] == "No":

        steps_response = steps_response + \
            "But, I am not sure how to calculate the total mechanical energy.\n"

    return steps_response, energy_conserved, energy_conserved_isolated, ke, gpe


def evaluate(information_check_dict, formulas):

    working = ""
    answer = "Could not compute"
    correct = False

    try:
        steps_working, work_done, ke, compute_using_alternate_formula = find_work_done_ke(
            information_check_dict, formulas)
        working = working + steps_working

        print("Find Work Done KE: ", steps_working,
              work_done, compute_using_alternate_formula)

        if ke is None and not compute_using_alternate_formula:
            print("IB SL WEP Question 4: ", working, answer, correct)
            return working, answer, correct

        if ke is not None:
            try:
                print("KE: ", work_done)
                answer = simplify(work_done.subs(
                    [(m, "m"), (v_final, values_dict["v2"]), (v_initial, values_dict["v1"])]))
                working = working + \
                    insert_latex(
                        str="W = " + '{:.2f}'.format(answer) + answer_unit)
                if abs(answer - answer_value) < 0.00001:
                    correct = True
                answer = '{:.2f}'.format(answer) + answer_unit

            except Exception as e:
                # Intended exception to handle case where some variables are not present in the formula
                working = working + "The information in the question is not sufficient to solve the problem based on the formula you have given.\n"

    except Exception as e:
        # Intended exception to handle case where some variables are not present in the formula
        working = working + "I understand that the work done in dragging the box is the change in kinetic energy of the box. The information in the question is not sufficient to solve the problem based on the formula you have given.\n"
        print("IB SL WEP Question 4: ", working, answer, correct)
        return working, answer, correct

    if information_check_dict[required_information[4]] == "Yes":
        # work done by external forces on a system or an object transfers energy to or from the system or the object thus, changing it's total mechanical energy
        answer = "Could not compute"
        working = "I understand that the total work done on the block is a result of all the forces acting on the block. Here we are calculating only the work done by the dragging force but I'm not sure how to calculate it based on the formulas given.\n"
        compute_using_alternate_formula = True

    if compute_using_alternate_formula:
        steps_working, work_done = find_work_formula(formulas)
        print("Work Done: ", work_done)
        try:
            working = working + \
                insert_latex(
                    "W = " + latex(work_done.subs([(s, values_dict["s_old"])]))) + "\n"
            working = working + \
                insert_latex(
                    "100 J = " + latex(work_done.subs([(s, values_dict["s_old"])]))) + "\n"
            work_done_old = work_done.subs([(s, values_dict["s_old"])])
            working = working + "Substituting " + \
                insert_latex(latex(values_dict["s_old"])) + " for " + \
                insert_latex(latex(values_dict["s_new"])) + "\n"
            working = working + \
                insert_latex(
                    "W = " + latex(work_done.subs([(s, values_dict["s_new"])]))) + "\n"
            work_done_new = work_done.subs([(s, values_dict["s_new"])])
            answer = work_done_new / work_done_old * values_dict["W"]
            working = working + \
                insert_latex("W = " + '{:.2f}'.format(answer) + answer_unit)
            if abs(answer - answer_value) < 0.00001:
                correct = True
            answer = '{:.2f}'.format(answer) + answer_unit

            if ke:
                working = working + "\nThe kinetic energy of the box doesn't change as the net work done by all the external forces on the box is zero. This is because the work done by the dragging force is equal and opposite to the work done by friction.\n"

        except Exception as e:
            # Intended exception to handle case where some variables are not present in the formula
            working = working + "The information in the question is not sufficient to solve the problem based on the formula you have given.\n"
            print("IB SL WEP Question 4: ", working, answer, correct)
            return working, answer, correct

    if working == "":
        working = "I am not sure how to solve this problem."

    print("IB SL WEP Question 4: ", working, answer, correct)
    return working, answer, correct


async def compute_q4(input: InputModel):
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
