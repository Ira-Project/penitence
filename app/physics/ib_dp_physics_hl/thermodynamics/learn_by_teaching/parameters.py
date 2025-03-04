topic = "thermodynamics"

ai_solver_model = "o3-mini"
ai_solver_instructions_question = "You have to solve the following question on " + topic + ":\n"
ai_solver_instructions_concepts_and_formulas = "To correctly solve this question, you have to use ONLY the 'concept_answers' and 'concept_formulas' (IF GIVEN) to the corresponding 'required_concepts' as given below:\n"
ai_solver_instructions_correct_answer_pointers = "Keep these points in mind while giving your response:\n" + \
    "1) You must use only the provided 'concept_answers' and 'concept_formulas' to solve the question.\n" + \
    "2) You must give your response in first person.\n" + \
    "3) You should present all calculations in LaTeX code.\n" + \
    "4) The question might also have LaTeX code that will be enclosed in '$!$' delimiters.\n" + \
    "5) Your response should be a JSON format with the following fields: 'steps' and 'final_answer'. In each 'step', you can apply only ONE of the 'required_concepts'. The 'step' field will be an array of objects, containing 'explanation' and 'calculation' fields. The 'explanation' field should contain less than 100 words, while the 'calculation' field should contain all the LaTeX code for calculations done in that step. Do not enclose the LaTeX code in '$!$' delimiters. If there are no calculations, the 'calculation' field should be an empty string. The 'final_answer' field should contain computed numerical answer to the question."


concept_questions = [
    "For an ideal gas, what is the relationship between pressure and volume when the temperature is constant?",
    "For an ideal gas, what is the relationship between pressure and temperature when the volume is constant?",
    "For an ideal gas, what is the relationship between volume and temperature when the pressure is constant?",
    "what is an isothermal process?",
    "what is an adiabatic process?",
    "what is an isobaric process?",
    "what is an isochoric process?",
    "how do you calculate the internal energy of a gas?",
    "does internal energy of gas change when pressure, volume or temperature changes?",
    "what is the law of conservation of energy in thermodynamics or the first law of thermodynamics?"
]

concept_answers = {}
concept_answers[concept_questions[0]] = {}
concept_answers[concept_questions[0]]["concept_answer"] = "For an ideal gas, the pressure and volume are inversely proportional when the temperature is constant."
concept_answers[concept_questions[0]]["concept_formula"] = []
concept_answers[concept_questions[1]] = {}
concept_answers[concept_questions[1]]["concept_answer"] = "For an ideal gas, the pressure and temperature are directly proportional when the volume is constant."
concept_answers[concept_questions[1]]["concept_formula"] = []
concept_answers[concept_questions[2]] = {}
concept_answers[concept_questions[2]]["concept_answer"] = "For an ideal gas, the volume and temperature are directly proportional when the pressure is constant."
concept_answers[concept_questions[2]]["concept_formula"] = []
concept_answers[concept_questions[3]] = {}
concept_answers[concept_questions[3]]["concept_answer"] = "An isothermal process is a process in which the temperature of the system remains constant."
concept_answers[concept_questions[3]]["concept_formula"] = []
concept_answers[concept_questions[4]] = {}
concept_answers[concept_questions[4]]["concept_answer"] = "An adiabatic process is a process in which no heat is exchanged with the surroundings."
concept_answers[concept_questions[4]]["concept_formula"] = []
concept_answers[concept_questions[5]] = {}
concept_answers[concept_questions[5]]["concept_answer"] = "An isobaric process is a process in which the pressure of the system remains constant."
concept_answers[concept_questions[5]]["concept_formula"] = []
concept_answers[concept_questions[6]] = {}
concept_answers[concept_questions[6]]["concept_answer"] = "An isochoric process is a process in which the volume of the system remains constant."
concept_answers[concept_questions[6]]["concept_formula"] = []
concept_answers[concept_questions[7]] = {}
concept_answers[concept_questions[7]]["concept_answer"] = ""
concept_answers[concept_questions[7]]["concept_formula"] = ["$!$U = \\frac{3}{2} nRT$!$", "$!$U = \\frac{3}{2} Nk_B T$!$"]
concept_answers[concept_questions[8]] = {}
concept_answers[concept_questions[8]]["concept_answer"] = "Internal energy of a gas depends on the temperature and changes only when temperature changes."
concept_answers[concept_questions[8]]["concept_formula"] = []
concept_answers[concept_questions[9]] = {}
concept_answers[concept_questions[9]]["concept_answer"] = "It states that heat change of a system is equal to the work done on or by the system plus the change in internal energy of the system."
concept_answers[concept_questions[9]]["concept_formula"] = ["$!$Q = W + \\Delta U$!$"]

parser_model = "gpt-4o-mini"
parser_instructions_concepts = "You have been given the following 'concept_questions' and an array of 'possible_concept_answers' for each 'concept_question':\n"
parser_instructions_paragraph = "The 'possible_concept_answers' may include formulas in LaTeX code enclosed in '$!$' delimiters. Now, you have to go through the paragraph and formulas given by the user and find the users' answers to the 'concept_questions'. The 'formulas' given by the user will be in LaTeX code.\n"
parser_instructions_response = "Your response should be in JSON format with the following field: 'user_answers'. The 'user_answers' field will be an array of objects, each containing 'concept_question', 'concept_answer', 'concept_formula', and 'is_concept_correct' field. The 'concept_question' field will be a string containing the 'concept_question'. The 'concept_answer' field will be a string containing the user's answer to that 'concept_question' and the 'concept_formula' field will be a string containing the formula given by the user for that 'concept_question'. The 'is_concept_correct' field will be a boolean value indicating whether the user's answer is correct or not.\n" + \
    "If the user has not given an answer to a 'concept_question', then the corresponding 'concept_answer' field should be an empty string. Similarly, if the user has not given a formula to a 'concept_question', then the corresponding 'concept_formula' field should be an empty string. " + \
    "If the user mentions ANY ONE of the 'possible_concept_answers' for a 'concept_question', then the 'is_concept_correct' field should be set to True. Otherwise, it should be set to False."
    
concept_missing = {}
concept_missing[concept_questions[8]] = "Internal energy of the gas changes when either pressure, volume or temperature changes."

incomplete_solver_model = "o3-mini"
incomplete_solver_instructions_question = "You have to provide an incomplete solution to the following question on " + topic + ":\n"
incomplete_solver_instructions_concepts_and_formulas = "Your solution will be incomplete because the user has not provided all the required concepts or formulas needed to solve the question. The required concepts and formulas are given below:\n"
incomplete_solver_instructions_response = "Your response should be a JSON format with the following field: 'steps'. The 'steps' field will be an array of objects, each containing 'explanation' and 'calculation' fields. The 'explanation' field should contain less than 100 words, while the 'calculation' field should contain all the LaTeX code for calculations done in that step. If there are no calculations, the 'calculation' field should be an empty string.\n"
incomplete_solver_instructions_pointers = "Keep these points in mind while giving your response:\n" + \
    "1) Your response should always be in first person and the user is always in second person.\n" + \
    "2) You should present all calculations in LaTeX code. DO NOT ENCLOSE THEM IN '$!$' DELIMITERS.\n" + \
    "3) For the missing concepts or formulas, ask the user for clarification. The clarification should be tailored to respond specifically to the user's explanation. But NEVER reveal the correct concepts or formulas mentioned.\n" + \
    "4) NEVER CORRECT ANY PART OF THE USER'S EXPLANATION. You are allowed to ONLY respond to the missing concepts or formulas.\n"

attempt_question_incorrectly_model = "o3-mini"
attempt_question_incorrectly_instructions_question = "You have to give an incorrect solution to the following question on " + topic + ":\n"
attempt_question_incorrectly_instructions_correct_solution = "Your solution will be incorrect because you are given some incorrect concepts or incorrect formulas. The correct concepts and formulas are as follows:\n"
attempt_question_incorrectly_instructions_response = "Your response should be a JSON format with the following fields: 'steps', 'final_answer' and 'is_correct'. The 'steps' field will be an array of objects, each containing 'explanation' and 'calculation' fields. The 'explanation' field should contain less than 100 words, while the 'calculation' field should contain all the LaTeX code for calculations done in that step. If there are no calculations, the 'calculation' field should be an empty string. The 'final_answer' field should either be an empty string or contain the incorrectly computed numerical answer to the question in LaTeX code. The 'is_correct' field should be a boolean value indicating whether your solution matches the correct solution provided above.\n"
attempt_question_incorrectly_instructions_pointers = "Keep these points in mind while giving your response:\n" + \
    "1) Your response should be only in first person and always address the user in second person.\n" + \
    "2) All your calculations must be in LaTeX code. Do not enclose them in '$!$' delimiters.\n" + \
    "3) Use the incorrect concepts or formulas to arrive at an incorrect solution. NEVER CORRECT THE USER or MENTION THAT THE USER'S SOLUTION IS INCORRECT.\n" + \
    "4) Never reveal the correct concepts or formulas to the user.\n"

correct_solver_model = "o3-mini"
correct_solver_instructions_response = "Your response should be a JSON format with the following fields: 'steps', 'final_answer' and 'is_correct'. The 'steps' field will be an array of objects, each containing 'explanation' and 'calculation' fields. The 'explanation' field should contain less than 100 words, while the 'calculation' field should contain all the LaTeX code for calculations done in that step. If there are no calculations, the 'calculation' field should be an empty string. The 'final_answer' field should either be an empty string or contain the correctly computed numerical answer to the question in LaTeX code. The 'is_correct' field should be a boolean value indicating whether your solution matches the correct solution provided above.\n"
correct_solver_instructions_pointers = "Keep these points in mind while giving your response:\n" + \
    "1) Your response should be only in first person and always address the user in second person.\n" + \
    "2) All your calculations must be in LaTeX code. Do not enclose them in '$!$' delimiters.\n" + \
    "3) Any LaTeX code in the 'explanation' field should be enclosed in '$!$' delimiters.\n" + \
    "4) You have to use ONLY the explanation and formulas given by the user to arrive at a correct solution.\n"

attempt_question_model = "o3-mini"
attempt_question_instructions_question = "You have to attempt the following question on " + topic + ". You will be given an explanation by the user and using it, you will have to attempt the question:\n"
attempt_question_instructions_concepts_and_formulas = "To correctly solve the question, you need the user to mention ANY ONE of the 'required_concept_answers' for ALL the corresponding 'required_concept_questions' as stated below:\n"
attempt_question_instructions_response = "Your response should be a JSON format with the following fields: 'steps', 'final_answer' and 'is_correct'. The 'steps' field will be an array of objects, each containing 'explanation' and 'calculation' fields. The 'explanation' field should contain less than 100 words, while the 'calculation' field should contain all the LaTeX code for calculations done in that step. If there are no calculations, the 'calculation' field should be an empty string. The 'final_answer' field should either be an empty string or contain the correctly computed numerical answer to the question in LaTeX code. The 'is_correct' field should be a boolean value indicating whether your solution matches the correct solution provided above.\n"
attempt_question_instructions_pointers = "Till the user correctly answers ALL the required_concept_questions, you should keep giving an incorrect solution. Keep the following points in mind while giving your response:\n" + \
    "1) You should always respond in first person and address the user in second person.\n" + \
    "2) You should always present your calculations in LaTeX code. Do not enclose them in '$!$' delimiters.\n" + \
    "3) If the user gives an incorrect concept or formula, you MUST use that to give an incorrect solution. NEVER CORRECT THE USER.\n" + \
    "4) Remember that for a given 'required_concept_question', the user might not mention all the 'required_concept_answers'. If they mention any one of the 'required_concept_answers', then you can use that concept correctly."