from sympy import *
from ..parameters import *
from ..utils import *
import math

# Function to combine value and unit into a string


def combine_value_and_unit(var):
    if var in units_dict:
        return str(values_dict[var]) + " " + units_dict[var]
    else:
        return str(values_dict[var])


# Question Parameters
question_id = 5
question_concepts = [
    concept_questions[4],
    concept_questions[5],
    concept_questions[6],
    concept_questions[7]
]


mass = insert_latex("2 kg")
initial_speed = insert_latex("10 m/s")
height = insert_latex("3 m")

given = {
    m,
    v_initial,
    h
}

objective = {
    v_final
}

question = "A {mass} block is thrown from a height of {height} above the ground at a speed of {initial_speed}. What is the final speed of the block just before it hits the ground? Will the final speed be the same if we consider air resistance?".format(
    mass=mass, height=height, initial_speed=initial_speed)
question_image = "No"
answer_type = "multi_correct"

values_dict = {}
units_dict = {}
values_dict["m"] = 2
units_dict["m"] = "kg"
values_dict["v_initial"] = 10
units_dict["v_initial"] = "m/s"
values_dict["h"] = 3
units_dict["h"] = "m"
values_dict["g"] = 9.8
units_dict["g"] = "m/s^2"
answer_value = math.sqrt(
    2 * values_dict["g"] * values_dict["h"] + values_dict["v_initial"]**2)
answer_unit = " m/s"
answer_output = insert_latex('{:.2f}'.format(
    answer_value) + answer_unit) + ", the final speed won't be the same"

concept_responses = {
    concept_questions[4]: [
        "When the block is in motion, it has kinetic energy.",
        "The block possesses kinetic energy as it in motion.",
        "The block has kinetic energy due to its motion when it is falling.",
        "The falling block possesses kinetic energy due to its motion.",
        "Due to its motion, the block has kinetic energy when it is falling.",
    ],
    concept_questions[5]: [
        "It has gravitational potential energy due to its position above the ground.",
        "It possesses gravitational potential energy because of its elevated position above the ground.",
        "Due to its height above the ground, it has gravitational potential energy.",
        "It's height gives it gravitational potential energy.",
        "It has gravitational potential energy because of its height above the ground.",
    ],
    concept_questions[6]: [
        "I understand that the block's total energy will be conserved and it can only change forms.",
        "The total energy of the block will be conserved throughout its motion. It can only change forms.",
        "According to the law of conservation of energy, the block's total energy stays the same and can only change forms.",
        "I've learned that the block's total energy is conserved and it can only change forms.",
        "I understand that the block's total energy is conserved at all times and it can only change forms.",
    ],
    concept_questions[7]: [
        "The block and the earth form an isolated system as there are no external forces acting on them.",
        "Since no external forces are acting on them, the block-earth system can be considered isolated.",
        "We can treat the block and earth as an isolated system because there are no external forces acting on them.",
        "The system consisting of both the block and earth is isolated due to the absence of any external forces.",
        "With no external forces acting on them, we can consider the block and earth as an isolated system.",
    ],
}


partial_concept_responses = {
    "an object has kinetic energy": [
        "Based on your explanation, the football has kinetic energy. But can you explain how you know that?",
        "I understand that the football possesses kinetic energy, but could you help me understand why?",
        "You mentioned the football has kinetic energy - could you explain what makes you say that?",
        "I see that the football has kinetic energy, but what's the reasoning behind this?",
        "You're saying the football has kinetic energy - could you walk me through how you came to that conclusion?",
    ],
    "an object has potential energy": [
        "You mention that the block has potential energy but can you explain how you know that?",
        "You say that the block has potential energy but can you help me understand why?",
        "Based on your explanation, the block has potential energy. But can you explain how you know that?",
        "I see you've identified potential energy in the block. Could you elaborate why it has this energy?",
        "Since you mentioned that the block has potential energy, could you explain how you know that?",
    ],
    "an object has potential energy due to its position": [
        "So the block has potential energy due to its position. But could you clarify more on what you mean by position?",
        "You mentioned the block's position gives it potential energy. Could you clarify more on what you mean by position?",
        "I understand that block's position gives it potential energy, but can you explain more on what you mean by position?",
        "When you say the block's position gives it potential energy, what exactly about its position are you referring to?",
        "I understand that the block has potential energy due to its position, but could you explain more on what you mean by position?",
    ],
    "energy stays constant": [
        "I understand that the block's energy will remain the same. So, all forms of it's energy will be constant. How do I use this information to find the final speed?",
        "You mentioned that the block's energy is conserved and so all forms of it's energy will be constant. Can you explain how I can use this information to calculate the final speed?",
        "I see that the total energy of the block doesn't change and so all forms of it's energy will be constant. But how do I use this to determine the final speed?",
        "The block's energy is conserved and so all forms of it's energy will be constant. But how do I use this principle to solve for the final speed?",
        "Now that I know the block's energy will remain constant, I understand that all forms of it's energy will remain the same. How do I use this to find the block's final speed?",
    ],
    "energy changes forms only": [
        "I understand that the block's energy can change forms. It might also increase or decrease. How do I use this information to find the final speed?",
        "You mentioned that the block's energy can convert between different forms. Could it also increase or decrease? How can I use this to calculate the final speed?",
        "Since the block's energy can convert between forms, it might also increase or decrease. How can I use this to determine the final speed?",
        "I see that the block's energy can change from one form to another. It might also increase or decrease. How do I use this to find the final speed?",
        "The block's energy can change forms and can also increase or decrease. How do I use this information to solve for the final speed?",
    ],
    "isolated systems conserve energy": [
        "I understand that isolated systems conserve energy. But can you explain what an isolated system is?",
        "You mentioned that energy is conserved in isolated systems. Could you clarify what makes a system isolated?",
        "Since we're talking about isolated systems and energy conservation, can you help me understand what an isolated system is?",
        "I see that energy conservation applies to isolated systems. But what exactly do you mean by isolated systems?",
        "When you say energy is conserved in isolated systems, could you explain what makes a system isolated?",
    ]
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
