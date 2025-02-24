topic = "thermodynamics"

ai_solver_model = "o3-mini"
ai_solver_instructions_question = "You have to solve the following question on " + topic + ":\n"
ai_solver_instructions_concepts = "To correctly solve this question, you have to use ONLY the 'concept_answers' to the corresponding 'concept_questions' given below:\n"
ai_solver_instructions_formulas = "You have to also use any formulas given in 'concept_formulas' below:\n"
ai_solver_instructions_correct_answer_pointers = "Keep these points in mind while giving your response:\n" + \
    "1) You must use only the provided 'concept_answers' and 'concept_formulas' to solve the question.\n" + \
    "2) You must give your response in first person.\n" + \
    "3) You should present all calculations in LaTeX code and enclose them in '$!$' delimiters.\n" + \
    "4) The question might also have LaTeX code that will be enclosed in '$!$' delimiters.\n" + \
    "5) Your response should be a JSON format with the following fields: 'steps' and 'final_answer'. The 'steps' field will be an array of objects, each containing 'explanation' and 'calculation' fields. The 'explanation' field should contain less than 100 words, while the 'calculation' field should contain all the LaTeX code for the calculations done in that step. If there are no calculations done in a step, the 'calculation' field should be an empty string. The 'final_answer' field should contain computed numerical answer to the question."

known_concepts = [
    "in an isothermal expansion, the temperature remains constant"
]

concept_questions = [
    "For an ideal gas, what is the relationship between pressure and volume when the temperature is constant?",
    "For an ideal gas, what is the relationship between pressure and temperature when the volume is constant?",
    "For an ideal gas, what is the relationship between volume and temperature when the pressure is constant?",
    "how is internal energy of gas related to its temperature?",
    "does internal energy of gas change when pressure, volume or temperature changes?",
    "what is the law of conservation of energy in thermodynamics or the first law of thermodynamics?"
]

concept_answers = {}
concept_answers[concept_questions[0]] = {}
concept_answers[concept_questions[0]]["concept_answer"] = "For an ideal gas, the pressure and volume are inversely proportional when the temperature is constant."
concept_answers[concept_questions[0]]["concept_formula"] = ""
concept_answers[concept_questions[1]] = {}
concept_answers[concept_questions[1]]["concept_answer"] = "For an ideal gas, the pressure and temperature are directly proportional when the volume is constant."
concept_answers[concept_questions[1]]["concept_formula"] = ""
concept_answers[concept_questions[2]] = {}
concept_answers[concept_questions[2]]["concept_answer"] = "For an ideal gas, the volume and temperature are directly proportional when the pressure is constant."
concept_answers[concept_questions[2]]["concept_formula"] = ""
concept_answers[concept_questions[3]] = {}
concept_answers[concept_questions[3]]["concept_answer"] = "The internal energy of a gas is directly proportional to the temperature of the gas."
concept_answers[concept_questions[3]]["concept_formula"] = "$!$U \\propto T$!$"
concept_answers[concept_questions[4]] = {}
concept_answers[concept_questions[4]]["concept_answer"] = "Internal energy of a gas depends on the temperature and changes only when temperature changes."
concept_answers[concept_questions[4]]["concept_formula"] = ""
concept_answers[concept_questions[5]] = {}
concept_answers[concept_questions[5]]["concept_answer"] = "The the first law of thermodynamics applies the law of conservation of energy and states that heat change of a system is equal to the work done on or by the system plus the change in internal energy of the system."
concept_answers[concept_questions[5]]["concept_formula"] = "$!$Q = W + \\Delta U$!$"

concept_missing = {}
concept_missing[concept_questions[0]] = "Ask what is the relationship between pressure and volume when the temperature remains constant for an ideal gas."
concept_missing[concept_questions[1]] = "Ask what is the relationship between pressure and temperature when the volume remains constant for an ideal gas."
concept_missing[concept_questions[2]] = "Ask what is the relationship between volume and temperature when the pressure remains constant for an ideal gas."
concept_missing[concept_questions[3]] = "Ask what is the relationship between internal energy and temperature of a gas."
concept_missing[concept_questions[4]] = "Assume internal energy of the gas changes when either pressure, volume or temperature changes."
concept_missing[concept_questions[5]] = "Ask how can we apply the law of conservation of energy to thermodynamics."