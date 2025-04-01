from ..parameters import *
from ..utils import *

num_of_particles = insert_latex("5")
initial_num_excited_particles = insert_latex("1")
final_num_excited_particles = insert_latex("3")

question = ("A system, consisting of {num_of_particles} particles, is initially in a state where only {initial_num_excited_particles} particle is in the excited state. The system is then brought into a state where {final_num_excited_particles} particles are in the excited state. What is the change in entropy of the system?").format(num_of_particles=num_of_particles, initial_num_excited_particles=initial_num_excited_particles, final_num_excited_particles=final_num_excited_particles)
answer_type = "single_correct"

answer_output = insert_latex("k_{B} \\ln(2)")
required_concepts = [
    concept_questions[10],
    concept_questions[11],
    concept_questions[12]
]