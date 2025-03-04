topic = "current_and_circuits"

extract_concepts_model = "o3-mini"
extract_concepts_instructions = "You have to select the concepts from the passage provided below that will be required to solve a question given by the user. The question might require multiple concepts. A concept is considered to be required ONLY IF it is directly needed to solve the question. Each concept can only be a single line from the passage provided above. Passage:\n"
extract_concepts_response_format = "Your response should be in a JSON format with the following field: 'extracted_concepts'. The 'extracted_concepts' field will be an array of strings containing the concepts required to solve the question. Remember that each 'concept' is a single line from the passage provided above."

attempt_question_model = "o3-mini"
attempt_question_instructions_question = "You have to attempt the following question on " + topic + ". You will be given an array of concepts by the user and using it, you will have to attempt the given question:\n"
attempt_question_instructions_concepts = "To correctly solve the question, you need the following array of 'required_concepts':\n"
attempt_question_instructions_response = "Your response should be a JSON format with the following fields: 'steps', 'final_answer' and 'is_correct'. The 'steps' field will be an array of objects, each containing 'explanation' and 'calculation' fields. The 'explanation' field should contain less than 100 words, while the 'calculation' field should contain all the LaTeX code for calculations done in that step. If there are no calculations, the 'calculation' field should be an empty string. The 'final_answer' field should either be an empty string or contain the correctly computed numerical answer to the question in LaTeX code. The 'is_correct' field should be a boolean value indicating whether your solution is correct or not.\n"
attempt_question_instructions_pointers = "Till the user gives you ALL the required_concepts, you should keep giving an incomplete solution. Keep the following points in mind while giving your response:\n" + \
    "1) You should always respond in first person and address the user in second person.\n" + \
    "2) You should always present your calculations in LaTeX code. Do not enclose them in '$!$' delimiters.\n" + \
    "3) For the missing 'required_concepts', first convey that you have understood the 'required_concept' that the user does provide and then ask the user a question. The question should be such that the answer will be the missing 'required_concept'. But while asking the question, NEVER reveal any part of the missing 'required_concept' to the user.\n" + \
    "4) If NONE of the 'required_concepts' are present in the array provided by the user, you should simply respond that you are unable to attempt the question."
