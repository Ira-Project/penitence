# ExplanationReader
read_explanation_model = "gpt-4o"
read_explanation_instructions = "You take the role of a thinker. I need you to carefully read over an explanation and answer some questions for me. Your response should be a valid jsonlist called 'verifications' where each json object has 'verification_question' and 'verification_answer' attributes. The verification_answer can only be 'Yes', 'No', or 'Unknown'. The verification_questions are given as follows:\n"
read_explanation_prompt_pre = "Based on the given explanation, answer each verification_question. Your answer should be based ONLY on the information given below, even if it contradicts common knowledge. \nExplanation: "

# Answer Single Question
answer_explanation_model = "gpt-4o"
answer_explanation_instructions = "You take the role of a thinker. I need you to carefully think over an explanation and answer a question for me. The questions you have to answer is:\n"
answer_explanation_prompt_pre = "Help me answer the question based on the given explanation. \nExplanation: "

# Formula Reader
formula_reader_model = "gpt-4o"
formula_reader_instructions = "You are a latex formula reader. I need you to read over an array in latex and give me a formula. Your response should be a json object called 'formula'. In your response, use the following symbols:\1) tndependent variable should be denoted by 'x'\n2) dependent variable should be denoted by 'y'\n3) slope of the line should be denoted by 'm'\n4) y intercept should be denoted by 'c'\n5)The x coordinate of the first point should be denoted by 'x_1'\n6)The y coordinate of the first point should be denoted by 'y_1'\n7)The x coordinate of the second point should be denoted by 'x_2'\n8)The y coordinate of the second point should be denoted by 'y_2'\nDO NOT use any other symbols in your response. Follow python syntax while writing the formula.\nIn the case that the formula I asked for is not in the array, then respond with 'Unknown'."
formula_reader_prompt_pre = "Read this array and give me a formula for:\n"
formula_reader_prompt_post = "The formula should be based ONLY on the array given below, even if it contradicts common knowledge.\nArray:\n"
