from sympy import *
from .parameters import *
from .utils import *
from latex2sympy2 import latex2sympy


# Check the explanation for the required information
def read_explanation(required_information, explanation, check_only_required=True):
    explanation_check_dict = {}
    procedural_check = False
    question_list = ""

    if check_only_required:
        for question in required_information:
            question_list = question_list + "concept_question: " + question + "\n" + \
                "valid_answer: " + unknown_concepts_answers[question] + "\n" + \
                "rephrased_answer: " + "\n".join(unknown_concepts_rephrases[question]) + "\n" + \
                "partial_answer: " + "\n".join(unknown_concepts_partial_answers[question].keys()) + "\n\n"
            print(question_list)
            explanation_check_dict[question] = "Unknown"
    else:
        for question in concept_questions:
            question_list = question_list + "concept_question: " + question + "\n" + \
                "valid_answer: " + unknown_concepts_answers[question] + "\n" + \
                "rephrased_answer: " + "\n".join(unknown_concepts_rephrases[question]) + "\n" + \
                "partial_answer: " + "\n".join(unknown_concepts_partial_answers[question].keys()) + "\n\n"
            explanation_check_dict[question] = "Unknown"

    # Perform an automated checklist check  
    checklist_json = check_information(
        question_list, explanation, instructions_post=information_checklist_prompt_post)
    for information in checklist_json['information_checklist']:
        if information['concept_question'] in explanation_check_dict:
            explanation_check_dict[information['concept_question']] = information['check']
            if information['check'] != "Correct":
                if information['partial_answer'] in unknown_concepts_partial_answers[information['concept_question']]:
                    explanation_check_dict[information['concept_question']] = information['partial_answer']
            if information['is_procedural']:
                print("Procedural Check: ", information['concept_question'])
                procedural_check = True
    print(explanation_check_dict)
    return explanation_check_dict, procedural_check


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
                    "I am not sure how to proceed further since you have not given me the formula for work done.\n\n" + "Note: Please enter the formula in the formula box given on the bottom left of the screen.\n"
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
            print("Formula JSON", formula_json)
            if formula_json['formula'] == "Unknown":
                print("KE I'm in the formula unknown case")
                steps_response = steps_response + \
                    "I am not sure how to calculate kinetic energy based on the formula provided.\n"
            else:
                try:
                    formula_read = formula_json['formula'].split("=")[1]
                except IndexError:
                    formula_read = formula_json['formula'].trim()
                ke = sympify(formula_read)
                print("Formula Sympify", formula_read)
                steps_response = steps_response + "Kinetic Energy = " +\
                    insert_latex(latex(ke)) + "\n"
            return steps_response, ke
        except Exception as e:
            print("KE Exception: ", e)
            attempts += 1

    return steps_response, ke
