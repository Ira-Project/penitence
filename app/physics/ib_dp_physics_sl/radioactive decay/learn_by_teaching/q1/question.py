from sympy import *
from ..parameters import *
from ..utils import *

# Function to combine value and unit into a string
# def combine_value_and_unit(var):
#     if var in units_dict:
#         return str(values_dict[var]) + " " + units_dict[var]
#     else:
#         return str(values_dict[var])

question_id = "1"

time_t1 = insert_latex("100 s")
time_t2 = insert_latex("200 s")
num_nuclides_t1 = insert_latex("1000")
num_nuclides_t2 = insert_latex("250")

given = {
    N_t1,
    N_t2,
    t1,
    t2
}

find = {
    lambda_
}

objective = {
    N_t0
}

question = ("Initially, a radioactive sample contains " + insert_latex("N") + " nuclides. After {time_t1}, the number of nuclides is {num_nuclides_t1} and after {time_t2}, the number of nuclides is {num_nuclides_t2}. Find the value of " + insert_latex("N") + ".").format(time_t1=time_t1, num_nuclides_t1=num_nuclides_t1, time_t2=time_t2, num_nuclides_t2=num_nuclides_t2)
question_image = "No"
answer_type = "single_correct"

answer_output = insert_latex("4000:\\Bq")
required_concepts = [
    concept_questions[0],
    concept_questions[1]
]
required_formulas = []

question_json = {
    "question_id": question_id,
    "Question": question,
    "Question_image": question_image,
    "Answer": answer_output,
    "Answer_type": answer_type,
    "required_concepts": required_concepts
}