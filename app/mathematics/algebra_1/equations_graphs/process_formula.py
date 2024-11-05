from sympy import *
from .parameters import *
from .utils import *
from latex2sympy2 import latex2sympy


# Find the formula for slope of the line
def find_slope_formula(formula):
    steps_response = ""
    slope = None
    max_attempts = 5
    attempts = 0

    while attempts < max_attempts:
        try:
            formula_json = formula_reader(
                "What is the formula for slope of the line done?", formula)
            if formula_json['formula'] == "Unknown":
                steps_response = steps_response + \
                    "I am not sure how to proceed further since you have not given me the formula for slope of the line.\n"
            else:
                try:
                    formula_read = formula_json['formula'].split("=")[1]
                except IndexError:
                    formula_read = formula_json['formula']
                print("Sympify Formula Read: ", formula_read)
                slope = sympify(formula_read)
                steps_response = steps_response + \
                    insert_latex("m = " + latex(slope)) + "\n"
            return steps_response, slope
        except Exception as e:
            attempts += 1

    return steps_response, slope


# Find the equation of a line from it's slope and intercept
def find_line_equation_from_slope_and_intercept(formula):
    steps_response = ""
    equation = None
    max_attempts = 5
    attempts = 0

    while attempts < max_attempts:
        try:
            formula_json = formula_reader(
                "What is the formula for the equation of a line from it's slope?", formula)
            if formula_json['formula'] == "Unknown":
                steps_response = steps_response + \
                    "I am not sure how to find the equation of a line based on the formula provided.\n"
            else:
                try:
                    formula_read = formula_json['formula'].split("=")[1]
                except IndexError:
                    formula_read = formula_json['formula']
                formula_read = latex2sympy(formula_read)
                equation = sympify(formula_read)
                steps_response = steps_response + \
                    insert_latex(latex(equation)) + "\n"
            return steps_response, equation
        except Exception as e:
            attempts += 1

    return steps_response, equation


# Find the equation of a line from it's slope and a point on it
def find_line_equation_from_slope_and_point(formula):
    steps_response = ""
    equation = None
    max_attempts = 5
    attempts = 0

    while attempts < max_attempts:
        try:
            formula_json = formula_reader(
                "What is the formula for the equation of a line from it's slope and a point on it?", formula)
            if formula_json['formula'] == "Unknown":
                steps_response = steps_response + \
                    "I am not sure how to find the equation of a line based on the formula provided.\n"
            else:
                try:
                    formula_read = formula_json['formula'].split("=")[1]
                except IndexError:
                    formula_read = formula_json['formula'].trim()
                formula_read = latex2sympy(formula_read)
                equation = sympify(formula_read)
                steps_response = steps_response + \
                    insert_latex(latex(equation)) + "\n"
            return steps_response, equation
        except Exception as e:
            attempts += 1

    return steps_response, equation


# Find the equation of a line from two points on it
def find_line_equation_from_two_points(formula):
    steps_response = ""
    equation = None
    max_attempts = 5
    attempts = 0

    while attempts < max_attempts:
        try:
            formula_json = formula_reader(
                "What is the formula for the equation of a line from two points on it?", formula)
            if formula_json['formula'] == "Unknown":
                steps_response = steps_response + \
                    "I am not sure how to find the equation of a line based on the formula provided.\n"
            else:
                try:
                    formula_read = formula_json['formula'].split("=")[1]
                except IndexError:
                    formula_read = formula_json['formula'].trim()
                formula_read = latex2sympy(formula_read)
                equation = sympify(formula_read)
                steps_response = steps_response + \
                    insert_latex(latex(equation)) + "\n"
            return steps_response, equation
        except Exception as e:
            attempts += 1

    return steps_response, equation
