from sympy import *
from ..parameters import *
from ..utils import *

alpha_ = insert_latex("\\alpha")
beta_minus_ = insert_latex("\\beta^-")
num_protons = "92"
num_neutrons = "146"
num_nucleons = str(int(num_protons) + int(num_neutrons))
element_symbol = "U"
element_notation = insert_latex("^{" + num_protons + "}_{" + num_nucleons + "}" + element_symbol)

question = ("Uranium-238 ({element_notation}) undergoes {alpha_} decay followed by {beta_minus_} decay to form element Y. What is the number of protons in element Y?").format(element_notation=element_notation, alpha_=alpha_, beta_minus_=beta_minus_)
question_image = "No"
answer_type = "single_correct"

answer_output = insert_latex("91")
required_concepts = [
    concept_questions[5],
    concept_questions[6],
    concept_questions[7],
    concept_questions[8]
]
required_formulas = []