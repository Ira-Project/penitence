from ..parameters import *
from ..utils import *

temperature_initial = insert_latex("300\\:K")
temperature_final = insert_latex("200\\:K")
num_moles = insert_latex("20\\:mol")

question = ("{num_moles} of an ideal gas undergoes adiabatic expansion. Initially, the gas is at a temperature of {temperature_initial} and finally, the temperature of the gas is {temperature_final}. What is the total work done by the gas?").format(num_moles=num_moles, temperature_initial=temperature_initial, temperature_final=temperature_final)
answer_type = "single_correct"

answer_output = insert_latex("24942\\:J")
required_concepts = [
    concept_questions[4],
    concept_questions[7],
    concept_questions[9]
]