from ..parameters import *
from ..utils import *

num_of_particles = insert_latex("2")

question = ("Consider a system consisting of {num_of_particles} different particles. Each of the {num_of_particles} particles can occupy one of two energy levels - normal and excited. Find all the possible macrostates of the system and determine which of them is the most probable?").format(num_of_particles=num_of_particles)
answer_type = "single_correct"

answer_output = "One excited particle and one normal particle"
required_concepts = [
    concept_questions[10],
    concept_questions[11]
]