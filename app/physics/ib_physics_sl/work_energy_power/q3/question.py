from sympy import *
from ..parameters import *
from ..utils import *


# Function to combine value and unit into a string
def combine_value_and_unit(var):
    if var in units_dict:
        return str(values_dict[var]) + " " + units_dict[var]
    else:
        return str(values_dict[var])


# Question Parameters
question_id = 3
question_concepts = [
    concept_questions[2],
    concept_questions[4],
]

mass = insert_latex("200 g")
initial_velocity = insert_latex("20 m/s")
final_velocity = insert_latex("0 m/s")

given = {
    mass,
    initial_velocity,
    final_velocity
}

objective = {
    W
}

question = "A {mass} football is kicked along the field at an initial speed of {v_initial}. What is the work done by friction to bring the football to a stop?".format(
    mass=mass, v_initial=v_initial)
question_image = "No"
answer_type = "single_correct"

values_dict = {}
units_dict = {}
values_dict["m"] = 0.2
units_dict["m"] = "kg"
values_dict["v_initial"] = 20
units_dict["v_initial"] = "m/s"
values_dict["v_final"] = 0
units_dict["v_final"] = "m/s"
answer_value = -40
answer_unit = " J"
answer_output = insert_latex('{:.2f}'.format(answer_value) + answer_unit)

concept_responses = {
    concept_questions[2]: [
        "I understand that the work done by friction is equal to the change in the football's total energy.",
        "The work performed by frictional forces equals to the change in the total energy of the football.",
        "The work done by friction equals the change in the football's total energy.",
        "I understand that the work done by friction can be calculated by finding the change in the football's total energy.",
        "The amount of work done by friction equals the change in the football's total energy.",
    ],
    concept_questions[4]: [
        "Since the football is in motion, it has kinetic energy.",
        "The moving football possesses kinetic energy due to its motion.",
        "The football possesses kinetic energy because it is moving.",
        "The football has kinetic energy because it is in moving.",
        "As the football is in motion, it contains kinetic energy.",
    ],
}

partial_concept_responses = {
    "work transfers energy": [
        "I understand that work done transfers energy but using just that, I don't know how to find the work done by friction.",
        "While I know work transfers energy, I'm not sure how to calculate the work done by friction.",
        "I understand that work is related to energy transfer, but I can't determine the work done by friction from this alone.",
        "Although I understand work transfers energy, I need more information to solve for the work done by friction.",
        "I recognize that work is related to energy transfer, but I am not sure how to find the work done by friction from this.",
    ],
    "work is equal to change in kinetic energy": [
        "I understand that the work done in by friction will be equal to the change in kinetic energy of the football.",
        "The work done by friction equals the change in kinetic energy of the football.",
        "I recognize that the work by friction is equal to the change in the football's kinetic energy.",
        "I see that the work done by friction is equal to how much the football's kinetic energy changes.",
        "I understand the work done by friction equals the change in the football's kinetic energy.",
    ],
    "an object has kinetic energy": [
        "Based on your explanation, the football has kinetic energy. But can you explain how you know that?",
        "I understand that the football possesses kinetic energy, but could you help me understand why?",
        "You mentioned the football has kinetic energy - could you explain what makes you say that?",
        "I see that the football has kinetic energy, but what's the reasoning behind this?",
        "You're saying the football has kinetic energy - could you walk me through how you came to that conclusion?",
    ],
}

concept_not_mentioned_responses = {
    concept_questions[2]: [
        "I am not sure how to calculate the work done by friction.",
        "I don't understand how to compute the work performed by friction.",
        "I don't know how to determine the work that friction does.",
        "I can't figure out how to calculate the work done by friction.",
        "I'm unable to calculate the amount of work friction does.",
    ],
    concept_questions[4]: [
        "I don't know what type of energy the football possesses.",
        "I'm unsure about what form of energy the football has.",
        "I can't identify the type of energies associated with the football.",
        "I'm not sure how to determine what type of energy the football has.",
        "I don't understand which form of energy the football possesses.",
    ],
}

procedural_explanation_responses = [
    "I think you are trying to give me the procedural explanation or the direct answer for this question. Instead, please explain the concepts that I will need to understand to solve this question.",
    "You are giving me the procedural explanation or the direct answer for this question. Instead, please explain the concepts that I will need to understand to solve this question.",
    "I notice you are providing me the procedural explanation or the direct answer for this question. Instead, please explain the concepts that I will need to understand to solve this question.",
    "I think you are trying to give me the procedural explanation or the direct answer for this question. Instead, please explain the concepts that I will need to understand to solve this question.",
    "You are giving me the procedural explanation or the direct answer for this question. Instead, please explain the concepts that I will need to understand to solve this question."
]

question_json = {
    "question_id": question_id,
    "Question": question,
    "Question_image": question_image,
    "Answer": answer_output,
    "Answer_type": answer_type,
    "required_concepts": question_concepts,
}
