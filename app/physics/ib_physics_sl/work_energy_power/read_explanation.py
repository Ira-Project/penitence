from sympy import *
from .parameters import *
from .utils import *
from latex2sympy2 import latex2sympy


# Convert concepts to an information checklist
def read_explanation(required_information, explanation, check_only_required=False):
    information_check_dict = {}
    information_list = ""

    if check_only_required:
        for information in required_information:
            information_list = information_list + "Question: " + \
                information_questions[information] + \
                "\nInformation: " + information + "\n"
            information_check_dict[information] = "Unknown"
    else:
        for concept in unknown_concepts:
            for information in unknown_concepts[concept]:
                information_list = information_list + "Question: " + \
                    information_questions[information] + \
                    "\nInformation: " + information + "\n"
                information_check_dict[information] = "Unknown"

    # Perform an automated information check
    checklist_json = check_information(
        information_list, explanation, instructions_post=information_checklist_prompt_post)
    for information in checklist_json['information_checklist']:
        if information['information'] in information_check_dict:
            information_check_dict[information['information']
                                   ] = information['check']
    print(information_check_dict)
    return information_check_dict


# Find the formula for work done
def find_work_formula(formula):
    steps_response = ""
    work_done = None
    max_attempts = 5
    attempts = 0

    while attempts < max_attempts:
        try:
            formula_json = formula_reader(
                "What is the formula for work done?", formula)
            if formula_json['formula'] == "Unknown":
                steps_response = steps_response + \
                    "I am not sure how to proceed further since you have not given me the formula for work done.\n"
            else:
                try:
                    formula_read = formula_json['formula'].split("=")[1]
                except IndexError:
                    formula_read = formula_json['formula']
                print("Sympify Formula Read: ", formula_read)
                work_done = sympify(formula_read)
                steps_response = steps_response + \
                    insert_latex("W = " + latex(work_done)) + "\n"
            return steps_response, work_done
        except Exception as e:
            attempts += 1

    return steps_response, work_done


# Find the formula for gravitational potential energy (gpe)
def find_gpe_formula(formula):
    steps_response = ""
    gpe = None
    max_attempts = 5
    attempts = 0

    while attempts < max_attempts:
        try:
            formula_json = formula_reader(
                "What is the formula for gravitational potential energy?", formula)
            if formula_json['formula'] == "Unknown":
                steps_response = steps_response + \
                    "I am not sure how to calculate gravitational potential energy based on the formula provided.\n"
            else:
                try:
                    formula_read = formula_json['formula'].split("=")[1]
                except IndexError:
                    formula_read = formula_json['formula']
                formula_read = latex2sympy(formula_read)
                gpe = sympify(formula_read)
                steps_response = steps_response + "Gravitational Potential Energy = " +\
                    insert_latex(latex(gpe)) + "\n"
            return steps_response, gpe
        except Exception as e:
            attempts += 1

    return steps_response, gpe


# Find the formula for kinetic energy (ke)
def find_ke_formula(formula):
    steps_response = ""
    ke = None
    max_attempts = 5
    attempts = 0

    while attempts < max_attempts:
        try:
            formula_json = formula_reader(
                "What is the formula for kinetic energy?", formula)
            if formula_json['formula'] == "Unknown":
                print("KE I'm in the formula unknown case")
                steps_response = steps_response + \
                    "I am not sure how to calculate kinetic energy based on the formula provided.\n"
            else:
                try:
                    formula_read = formula_json['formula'].split("=")[1]
                except IndexError:
                    formula_read = formula_json['formula'].trim()
                formula_read = latex2sympy(formula_read)
                ke = sympify(formula_read)
                steps_response = steps_response + "Kinetic Energy = " +\
                    insert_latex(latex(ke)) + "\n"
            return steps_response, ke
        except Exception as e:
            print("KE Exception: ", e)
            attempts += 1

    return steps_response, ke
