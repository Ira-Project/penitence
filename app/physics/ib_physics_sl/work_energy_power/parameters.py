from sympy import *

F, s, theta, W = symbols("F s theta W")
m, a, v = symbols("m a v")
g, h = symbols("g h")
v_final, v_initial = symbols("v_final v_initial")
h_final, h_initial = symbols("h_final h_initial")
h_1, h_2 = symbols("h_1 h_2")
v_1, v_2 = symbols("v_1 v_2")
E_p, E_k, E_s = symbols("E_p E_k E_s")
F_cos_theta = symbols("F_cos_theta")
s_cos_theta = symbols("s_cos_theta")

known_concepts = [
    "if speed is constant, then acceleration is zero or if speed is constant",
    "g is acceleration due to gravity"
]

formulas = {}
formulas[W] = F*s*cos(theta)
formulas[F] = m*a
formulas[F_cos_theta] = F*cos(theta)
formulas[s_cos_theta] = s*cos(theta)
formulas[E_p] = m*g*h
formulas[E_k] = (1/2)*m*v**2


concept_questions = [
    "How to know if the net force is zero?",
    "In addition to stating the force times displacement formula, what else is needed to calculate the work done?",
    "Apart from the force times displacement formula, how else to find the work done?",
    "How to find the total mechanical energy of an object?",
    "Is kinetic energy a form of energy?",
    "Is potential energy a form of energy?",
    "Is the total energy conserved?",
    "When is the total energy conserved?" # CURRENT PROMPT DOES NOT DETECT THIS WELL OR AT ALL
]

unknown_concepts_answers = {
    concept_questions[0]: "if the object is moving at constant speed or is at rest, then the net force is zero",
    concept_questions[1]: "to calculate the work done, only the component of force that is in the direction of the object's displacement is considered",
    concept_questions[2]: "the work done is equal to the change in the object's total energy",
    concept_questions[3]: "the total mechanical energy is the sum of the kinetic energy and the potential energy",
    concept_questions[4]: "kinetic energy is a form of energy that an object has due to it's motion",
    concept_questions[5]: "potential energy is a form of energy that an object has due to it's position in a gravitational field",
    concept_questions[6]: "the total energy is conserved, i.e., it can neither be created nor be destroyed, only transferred",
    concept_questions[7]: "the total energy is conserved only when the object or the system is isolated, i.e, it doesn't exchange any energy with it's surroundings"
}

unknown_concepts_rephrases = {
    concept_questions[0]: [
        "objects moving at constant speed have zero net force",
        "no acceleration means zero net force"   
    ],
    concept_questions[1]: [
        "work calculations only use the force component parallel to displacement",
        "the angle between force and displacement affects work calculations"
    ],
    concept_questions[2]: [
        "work equals the change in the total energy of an object",
        "change in the total energy, and not just kinetic energy, is equal to work done",
        "work is same as change in the energy"
    ],
    concept_questions[3]: [
        "kinetic plus potential energy equals total mechanical energy",
    ],
    concept_questions[4]: [
        "an object's movement gives it kinetic energy",
        "speed helps determine an object's kinetic energy",
        "an object doesn't have kinetic energy unless it is in motion"
    ],
    concept_questions[5]: [
        "an object's height, and not just position, gives it potential energy",
        "objects in a gravitational field have potential energy",
        "higher objects have more gravitational potential energy",
        "an object doesn't have potential energy unless it is in given position AND this position is in a gravitational field",
        "an object's potential depends not just on its position but rather on it's specific position in a gravitational field"
    ],
    concept_questions[6]: [
        "energy cannot be created or destroyed, only transferred or change forms",
        "total energy remains constant but can be transferred or change forms",
        "energy transfers between objects but total energy stays the same",
    ],
    concept_questions[7]: [
        "systems without external energy exchange conserve energy",
        "energy of the system stays constant when no external forces act on the system"
    ]
}

unknown_concepts_partial_answers = {
    concept_questions[0]: {
        "stationary objects have zero net force": "doesn't mention when the net force is zero for an object in motion",
        "all forces must be added together to get the net force": "doesn't mention how to get the net force when all the force values are not known",
        "balanced forces give zero net force": "doesn't mention how to determine if the forces are balanced"
    },
    concept_questions[1]: {
        "force direction matters for work": "doesn't mention how the force direction is considered"
    },
    concept_questions[2]: {
        "work transfers energy": "doesn't mention that it equals the change in total energy",
        "work is equal to change in kinetic energy": "doesn't mention that it equals the change in total energy"
    },
    concept_questions[3]: {
        "energy comes in kinetic and potential forms": "doesn't mention that their sum equals total mechanical energy",
        "kinetic plus potential energy equals total energy": "doesn't mention that it equals total mechanical energy"
    },
    concept_questions[4]: {
        "an object has kinetic energy": "doesn't mention that it has kinetic energy due to its motion"
    },
    concept_questions[5]: {
        "an object has potential energy": "doesn't mention that it has potential energy due to its position",
        "an object has potential energy due to its position": "doesn't mention that it is due to its position in a gravitational field", # CURRENT PROMPT DOES NOT DETECT THIS WELL OR AT ALL
    },
    concept_questions[6]: {
        "energy stays constant": "doesn't mention that it can be transferred or change forms",
        "energy changes forms only": "doesn't mention that it is being conserved",
    },
    concept_questions[7]: {
        "isolated systems conserve energy": "doesn't mention what an isolated system is"
    }
}


information_questions = {}
information_questions["the force is zero"] = "What is the force when acceleration of an object is zero or the object is moving at constant speed?"
information_questions["to calculate the work done, only the component of force that is in the direction of the object's displacement is considered"] = "To calculate work, is the direction of force considered?"
information_questions[
    "it is equal to the change in gravitational potential energy"] = "What is the work done when moving an object (changing it's height) under gravitational force?"
information_questions[
    "it is equal to the change in kinetic energy"] = "What is the work done in moving or stopping (changing it's velocity) an object?"
information_questions["the total mechanical energy of a system/object is the sum of its kinetic and potential energy"] = "What is the total mechanical energy?"
information_questions["the total mechanical energy is conserved, i.e., it can neither be created nor be destroyed"] = "Is the total mechanical energy conserved?"
information_questions["the total mechanical energy is conserved only when the object or the system is isolated"] = "When is total mechanical energy conserved?"
information_questions["a system/object is isolated when it doesn't exchange any energy with it's surroundings, i.e, it doesn't have any external forces acting on it"] = "What does it mean for an object or a system to be isolated?"
information_questions["the net work or total work done on the system/object is equal to a change in it's total energy"] = "What is the net work done?"


information_checklist_model = "gpt-4o"
information_checklist_instructions = "You are an automated checklist. I need you to carefully read my message to check if it contains the answer to some 'concept_questions'. Your response should be a valid jsonlist called 'information_checklist' where each json object has 'concept_question', 'check', 'is_procedural', and 'partial_answer' attributes. The 'check' attribute can be:\n- 'Correct': if the message contains the correct answer or an acceptable rephrase except for the case where the message contains a partial answer\n- 'Wrong': if the message contains an incorrect answer\n- 'Not Present': if the message doesn't have answer the question or contains partial answer similar to the given 'partial_answer'\nThe 'is_procedural' attribute should be:\n- True: if the message describes steps to solve a specific problem or asks to perform calculations to find a value. This also includes messsages that direccly give the answer\n- False: if the answer is not given as a procedure\nThe 'partial_answer' attribute should be:\n- Empty string if the answer is correct\n- The matching 'partial_answer' from the given list if the message contains a partial answer\nCheck against the following concept_questions, their valid_answers, thier rephrased_answers, and their partial_answers:"
information_checklist_prompt_pre = ""
information_checklist_prompt_post = "While reading the message, you do not know any trigonometic identities like cos or sin unless they are given in the message. If they are not given, then you should not use them."


formula_reader_model = "gpt-4o"
formula_reader_instructions = "You are a latex formula reader. I need you to read over an array in latex and give me a formula. Your response should be a json object called 'formula'. In your response, use the following symbols:\1) force should be denoted by 'F'\n2) distance/displacement should be denoted by 's'\n3) angle should be denoted by 'theta'\n4) mass should be denoted by 'm'\n5) acceleration should be denoted by 'a'\n6) velocity should be denoted by 'v'\7) height should be denoted by 'h'\n8) acceleration due to gravity should be denoted by 'g'\n9) gravitational potential energy should be denoted by 'E_p'\n10) kinetic energy should be denoted by 'E_k'\n11) spring potential energy should be denoted by 'E_s'\n12) cosine, sine, tangent, cotangent, cosecant, and secant should be denoted by cos, sin, tan, cot, cosec, and sec respectively\n13) final velocity should be denoted by 'v_2'\n14) initial velocity should be denoted by 'v_1'\n15) final height should be denoted by 'h_2'\n16) initial height should be denoted by 'h_1'\nDO NOT use any other symbols in your response. Follow python syntax while writing the formula.\nIn the case that the formula I asked for is not in the array, then respond with 'Unknown'."
formula_reader_prompt_pre = "Read this array and give me a formula for:\n"
formula_reader_prompt_post = "The formula should be based ONLY on the array given below, even if it contradicts common knowledge.\nArray:\n"

print_working_json_model = "gpt-4o"
print_working_json_instructions = "You are a paraphraser. I need you to read a question and it's working and paraphrase it. Your response should be a json object which has the 'working' attribute. The 'working' will be a paraphrased version of the given working."
print_working_json_prompt_pre = "Help me paraphrase the working to the given question. If no working is given, return an empty string for working. \nQuestion: "
print_working_json_prompt_post = "\nWorking: "

## Other concepts which were not used in the questions
other_concepts = {}

other_concepts["What is the work done against gravity?"] = [
    "it is equal to the change in gravitational potential energy"
]
other_concepts["What is the work done to change the velocity?"] = [
    "it is equal to the change in kinetic energy"
]
other_concepts["What is the conservation of total mechanical energy?"] = [
    "the total mechanical energy of a system/object is the sum of its kinetic and potential energy",
    "the total mechanical energy is conserved, i.e., it can neither be created nor be destroyed",
    "a system/object is isolated when it doesn't exchange any energy with it's surroundings, i.e, it doesn't have any external forces acting on it",
    "the net work or total work done on the system/object is equal to a change in it's total energy",
    "the total mechanical energy is conserved only when the object or the system is isolated"
]