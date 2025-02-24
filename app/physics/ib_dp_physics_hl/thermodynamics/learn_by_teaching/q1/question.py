from ..parameters import *
from ..utils import *

pressure_initial = insert_latex("100 kPa")
volume_initial = insert_latex("0.5 m^3")
volume_final = insert_latex("2 m^3")

question = ("An ideal gas undergoes isothermal expansion. Initially, the gas is at a pressure of {pressure_initial} and a volume of {volume_initial}. The gas is allowed to expand to a final volume of {volume_final}. What is the total work done by the gas?").format(pressure_initial=pressure_initial, volume_initial=volume_initial, volume_final=volume_final)
answer_type = "single_correct"

answer_output = insert_latex("")
required_concepts = [
    concept_questions[0],
    concept_questions[4],
    concept_questions[5]
]