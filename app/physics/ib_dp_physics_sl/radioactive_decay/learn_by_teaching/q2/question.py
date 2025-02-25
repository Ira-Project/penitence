from sympy import *
from ..parameters import *
from ..utils import *

rest_mass = insert_latex("4.002603 u")
num_protons = "2"
num_neutrons = "2"
num_nucleons = str(int(num_protons) + int(num_neutrons))
element_symbol = "X"
element_notation = insert_latex("^{" + num_protons + "}_{" + num_nucleons + "}" + element_symbol)
mass_nucleon = insert_latex("1 u")

question = ("A radioactive nuclide {element_notation} has a rest mass of {rest_mass}. Assuming that the rest mass of a proton and a neutron is {mass_nucleon}, find the energy needed to separate the nucleons of {element_symbol}.").format(element_notation=element_notation, rest_mass=rest_mass, mass_nucleon=mass_nucleon, element_symbol=element_symbol)
question_image = "No"
answer_type = "single_correct"

answer_output = insert_latex("2.424 MeV")
required_concepts = [
    concept_questions[2],
    concept_questions[3],
    concept_questions[4],
    concept_questions[5]
]