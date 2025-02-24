from sympy import *
from ..parameters import *
from ..utils import *

time_t_half = insert_latex("50 s")
time_t = insert_latex("100 s")
num_nuclides_t0 = insert_latex("1000")

question = ("Initially, a radioactive sample contains {num_nuclides_t0} nuclides. The half-life of the sample is {time_t_half}. Find the number of nuclides after {time_t}.").format(num_nuclides_t0=num_nuclides_t0, time_t_half=time_t_half, time_t=time_t)
answer_type = "single_correct"

answer_output = insert_latex("250")
required_concepts = [
    concept_questions[0],
    concept_questions[1]
]
required_formulas = []