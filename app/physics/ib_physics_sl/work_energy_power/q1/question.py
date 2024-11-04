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
question_id = 1
question_concepts = [
    concept_questions[0],
    concept_questions[1]
]

other_force = insert_latex("300 N")
angle = insert_latex("30 \\degrees")
displacement = insert_latex("100 m")


given = {
    theta,
    s
}
to_find = {
    F
}
objective = {
    W
}

question = "A boy pulls a box across a rough, horizontal surface using a rope. The box is moving at a steady speed. The friction on the box is {other_force} and the rope is at angle of {angle} to the horizontal. Find the work done by the boy to move the box a distance of {displacement} across the horizontal surface.".format(
    other_force=other_force, angle=angle, displacement=displacement)
question_image = "No"
answer_type = "single_correct"

values_dict = {}
units_dict = {}
values_dict["Friction"] = 300
units_dict["Friction"] = "N"
values_dict["F"] = 300
units_dict["F"] = "N"
values_dict["s"] = 100
units_dict["s"] = "m"
values_dict["theta"] = 30
units_dict["theta"] = "degrees"
values_dict["a"] = 0
answer_value = 30
answer_unit = " kJ"
answer_unit_into_1000 = " J"
answer_output = insert_latex('{:.2f}'.format(answer_value) + answer_unit)


concept_responses = {
    concept_questions[0]: [
        "Based on your explanation, I understand that the net force on box is zero and therefore, the boy is exerting " + combine_value_and_unit("F") + " of force in the direction opposite friction to cancel out the friction force.",
        "I see that since the box moves at constant speed, the boy must apply " + combine_value_and_unit("F") + " to exactly balance out the friction force.",
        "With a constant velocity, the boy's applied force of " + combine_value_and_unit("F") + " must equal the friction force for equilibrium.",
        "I understand that the net force is zero because the boy's " + combine_value_and_unit("F") + " force counteracts the friction completely.",
        "Since the box maintains steady speed, I understand the boy's " + combine_value_and_unit("F") + " force must perfectly oppose the friction force."
    ],
    concept_questions[1]: [
        "I understand that we only consider the components of the force that are in the direction of displacement caused by the force.",
        "I see that the work done depends only on the force components parallel to the direction of movement.",
        "I understand that only the force components that are parallel to the displacement can contribute to the work done.",
        "I've learned that work calculation focuses on the force components that act along the displacement path.",
        "I understand that we only include force components in the same direction as the motion when calculating work."
    ]
}

concept_not_mentioned_responses = {
    concept_questions[0]: [
        "The question only gives us information on frictional force. I don't how to determine the force exerted by the boy.",
        "With only the friction force provided, I'm unsure how to calculate the force the boy applies.",
        "I can see the friction value, but I'm missing information about how much force the boy needs to use. How do I find the force exerted by the boy?",
        "Without knowing the boy's applied force, and only having friction information, I don't know how to proceed.",
        "The friction force is given, but I need help understanding how to find the force the boy exerts."
    ]
}

partial_concept_responses = {
    "stationary objects have zero net force": [
        "I understand that stationary objects have zero net force but the box is in motion. How does this affect the net force on the box?",
        "I know that objects at rest have zero net force, but this box is moving. What does that mean for the forces involved?",
        "While I grasp that stationary objects experience zero net force, this box is moving. What should I consider about the forces?",
        "I see that zero net force applies to stationary objects, but since this box is moving, what should I understand about the forces acting on it?",
        "I've learned about zero net force in stationary objects, but how does this concept apply to a moving box?"
    ],
    "all forces must be added together to get the net force": [
        "I understand that all forces must be added together to get the net force but I don't know the force exerted by the boy. How do I find the net force?",
        "While I know we need to sum all forces to find the net force, I'm missing the boy's applied force. How can I determine the net force?",
        "I recognize that calculating net force requires adding all forces, but without knowing the boy's force, how can I proceed?",
        "Though I understand forces must be summed for the net force, the boy's force is unknown. How can I solve this?",
        "I understand that net force is the sum of all forces, but the boy's force is a missing piece. How can I solve this?"
    ],
    "balanced forces give zero net force": [
        "I understand that balanced forces give zero net force but how do I know if the forces are balanced?",
        "While I know balanced forces result in zero net force, how do I know when these forces are actually balanced?",
        "I grasp that zero net force comes from balanced forces, but what tells me if these forces are balanced?",
        "Though I understand balanced forces create zero net force, how do I determine if these forces are balanced?",
        "I've learned that balanced forces yield zero net force, but how do I know whether forces are balanced here?"
    ],
    "force direction matters for work": [
        "I understand that force direction matters for work but I am not sure how the force direction is considered.",
        "While I know direction of force affects work, could you explain how this direction is taken into account?",
        "I recognize force direction is important for work calculations, but how exactly does direction factor in?",
        "Though I understand force direction impacts work, could you clarify how direction is incorporated?",
        "I understand that force direction plays a role in the work done, but how is this directional component considered?"
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
