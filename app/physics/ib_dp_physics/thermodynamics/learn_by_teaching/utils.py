import json
from .parameters import *
from .....openai_client import client

# Put LaTeX text within delimeters
latex_delimeter = "$!$"


def insert_latex(str):
    return latex_delimeter + str + latex_delimeter

def correct_latex_formatting(text):

    text = text.replace(latex_delimeter, "MYLATEXDELIMETER")
    # Replace faulty delimeters
    text = text.replace("$!", "MYLATEXDELIMETER")
    text = text.replace("!$", "MYLATEXDELIMETER")
    text = text.replace("$", "MYLATEXDELIMETER")

    # Restore delimeters
    text = text.replace("MYLATEXDELIMETER", latex_delimeter)
    text = text.replace("$!$$", latex_delimeter)
    text = text.replace("!$!$", latex_delimeter)
    text = text.replace("$!$!", latex_delimeter)
    text = text.replace("$$!$", latex_delimeter)
    return text

def solve_question(question, required_concepts):
    concepts_string = ""
    start_ind = 1
    for concept_question in required_concepts:
        concepts_string += f"{str(start_ind)}) required_concept: {concept_question}\n"
        concepts_string += f"concept_answer: {concept_answers[concept_question]['concept_answer']}\n"
        concepts_string += f"concept_formula: {concept_answers[concept_question]['concept_formula']}\n"
        start_ind += 1

    messages = [{"role": "developer", "content": ai_solver_instructions_question + question + "\n\n" + ai_solver_instructions_concepts_and_formulas + \
                 concepts_string + "\n\n" + ai_solver_instructions_correct_answer_pointers},
        {"role": "user", "content": "Solve the question by applying ALL the 'required_concepts' provided. Each step should apply only one 'required_concept'. You DO NOT need any other formula to solve the question."}
    ]

    response = client.chat.completions.create(
        model=ai_solver_model,
        messages=messages,
        reasoning_effort="medium",
        response_format={"type": "json_schema", 
                            "json_schema": {
                                "name": "correct_solution",
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "steps": {
                                            "type": "array",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "explanation": {"type": "string"},
                                                    "calculation": {"type": "string"}
                                                },
                                                "required": ["explanation", "calculation"],
                                                "additionalProperties": False
                                            }
                                        },
                                        "final_answer": {"type": "string"}
                                    },
                                    "required": ["steps", "final_answer"],
                                    "additionalProperties": False
                                },
                                "strict": True
                            }
                        }
    )

    # If there is a refusal, return the refusal
    if response.choices[0].message.refusal:
        return "I am sorry I was unable to solve the question. Please try again."
    else:
        # If there is no refusal, return the response
        response_json = json.loads(response.choices[0].message.content)
        correct_solution = "Correct Solution:\n"
        for step in response_json["steps"]:
            correct_solution = correct_solution + step["explanation"] + "\n" + step["calculation"] + "\n"
        correct_solution = correct_solution + "Correct Answer: " + response_json["final_answer"]
        print(correct_solution)
        return correct_solution
    
def attempt_question(question, required_concepts, correct_solution, provided_concepts, provided_formulas):
    provided_explanation = "Explanation: " + provided_concepts + "\n" + "Formulas: " + provided_formulas
    concepts_string = ""
    start_ind = 1
    for concept_question in required_concepts:
        concepts_string += f"{str(start_ind)}) required_concept_question: {concept_question}\n"
        if concept_answers[concept_question]['concept_answer'] != "":
            concepts_string += f"required_concept_answer: {concept_answers[concept_question]['concept_answer']}"
            if concept_answers[concept_question]['concept_formula']:
                for f in concept_answers[concept_question]['concept_formula']:
                    concepts_string += f" OR\nrequired_concept_answer: {f}\n"
            else:
                concepts_string += "\n"
        else:
            for f in concept_answers[concept_question]['concept_formula']:
                if f == concept_answers[concept_question]['concept_formula'][-1]:
                    concepts_string += f"required_concept_answer: {f}\n"
                else:
                    concepts_string += f"required_concept_answer: {f} OR\n"
        start_ind += 1

    messages = [{"role": "developer", "content": attempt_question_instructions_question + question + "\n" + attempt_question_instructions_concepts_and_formulas + \
                 concepts_string + "\n" + correct_solution + "\n\n" + attempt_question_instructions_response + "\n" + attempt_question_instructions_pointers},
        {"role": "user", "content": "Use this explanation and formulas to attempt the question:\n" + provided_explanation + "\n" + \
         "You have to give incorrect solutions till I mention ANY one 'required_concept_answer' for ALL the 'required_concept_questions' needed to solve the question."}
    ]

    response = client.chat.completions.create(
        model=attempt_question_model,
        messages=messages,
        reasoning_effort="low",
        response_format={"type": "json_schema", 
                         "json_schema": {
                            "name": "attempt_question",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "steps": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "explanation": {"type": "string"},
                                                "calculation": {"type": "string"}
                                            },
                                            "required": ["explanation", "calculation"],
                                            "additionalProperties": False
                                        }
                                    },
                                    "final_answer": {"type": "string"},
                                    "is_correct": {"type": "boolean"}
                                },
                                "required": ["steps", "final_answer", "is_correct"],
                                "additionalProperties": False
                            }
                        }
    })

    if response.choices[0].message.refusal:
        working = "I was unable to attempt the question."
        answer = ""
        is_correct = False
        return working, answer, is_correct
    else:
        response_json = json.loads(response.choices[0].message.content)
        working = ""
        for step in response_json["steps"]:
            try:
                working = working + step["explanation"] + \
                    "\n" + insert_latex(step["calculation"]) + "\n"
            except:
                working = working + "I was unable to attempt the question based on the provided explanation."
                continue
        answer = insert_latex(response_json["final_answer"])
        is_correct = response_json["is_correct"]
        if working == "":
            working = "I was unable to attempt the question based on the provided explanation."
        return working, answer, is_correct

def attempt_question_correctly(question, correct_solution, provided_concepts, provided_formulas):
    provided_explanation = "Explanation: " + provided_concepts + "\n" + "Formulas: " + provided_formulas

    messages = [{"role": "developer", "content": "Question: " + question + "\n\n" + correct_solution + "\n" + correct_solver_instructions_response},
        {"role": "user", "content": "Solve the question by using ONLY the explanation and formulas given by me:\n" + provided_explanation}
    ]

    response = client.chat.completions.create(
        model=correct_solver_model,
        messages=messages,
        reasoning_effort="low",
        response_format={"type": "json_schema", 
                         "json_schema": {
                            "name": "correct_solution",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "steps": {
                                            "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "explanation": {"type": "string"},
                                                "calculation": {"type": "string"}
                                            },
                                            "required": ["explanation", "calculation"],
                                            "additionalProperties": False
                                        }
                                    },
                                    "final_answer": {"type": "string"},
                                    "is_correct": {"type": "boolean"}
                                },
                                "required": ["steps", "final_answer", "is_correct"],
                                "additionalProperties": False
                            }
                        }
    })

    if response.choices[0].message.refusal:
        working = "I was unable to attempt the question."
        answer = ""
        is_correct = False
        return working, answer, is_correct
    else:
        response_json = json.loads(response.choices[0].message.content)
        working = ""
        for step in response_json["steps"]:
            try:
                working = working + correct_latex_formatting(step["explanation"]) + \
                    "\n" + correct_latex_formatting(step["calculation"]) + "\n"
            except:
                working = working + "I was unable to attempt the question based on the provided explanation."
                continue
        answer = insert_latex(response_json["final_answer"])
        is_correct = response_json["is_correct"]
        if working == "":
            working = "I was unable to attempt the question based on the provided explanation."
        return working, answer, is_correct

def attempt_question_incorrectly(question, correct_solution, provided_concepts, provided_formulas, parsed_answers, is_parsed_answers_correct):
    
    provided_explanation = "Explanation: " + provided_concepts + "\n" + "Formulas: " + provided_formulas
    incorrect_answers = "The following concept question was answered incorrectly or not answered at all:\n"

    start_ind = 1
    for concept_question in parsed_answers:
        if not is_parsed_answers_correct[concept_question]:
            incorrect_answers += f"{str(start_ind)}) {concept_question}\n"
            start_ind += 1

    messages = [{"role": "developer", "content": attempt_question_incorrectly_instructions_question + question + "\n\n" + attempt_question_incorrectly_instructions_correct_solution + \
                 correct_solution + "\n\n" + attempt_question_incorrectly_instructions_response + "\n" + attempt_question_incorrectly_instructions_pointers},
        {"role": "user", "content": "Give me an incorrect solution to the question based on the explanation and formulas provided:\n" + provided_explanation + \
         "\n" + incorrect_answers + "\nDO NOT MENTION whether your solution is incorrect or incomplete. Just give a solution that is incorrect or incomplete."}
    ]

    response = client.chat.completions.create(
        model=attempt_question_incorrectly_model,
        messages=messages,
        reasoning_effort="low",
        response_format={"type": "json_schema", 
                         "json_schema": {
                            "name": "incorrect_solution",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "steps": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "explanation": {"type": "string"},
                                                "calculation": {"type": "string"}
                                            },
                                            "required": ["explanation", "calculation"],
                                            "additionalProperties": False
                                        }
                                    },
                                    "final_answer": {"type": "string"},
                                    "is_correct": {"type": "boolean"}
                                },
                                "required": ["steps", "final_answer", "is_correct"],
                                "additionalProperties": False
                            }
                        }
    })

    if response.choices[0].message.refusal:
        working = "I was unable to attempt the question."
        answer = ""
        is_correct = False
        return working, answer, is_correct
    else:
        response_json = json.loads(response.choices[0].message.content)
        working = ""
        for step in response_json["steps"]:
            try:
                working = working + correct_latex_formatting(step["explanation"]) + \
                    "\n" + correct_latex_formatting(step["calculation"]) + "\n"
            except:
                working = working + "I was unable to attempt the question based on the provided explanation."
                continue
        answer = insert_latex(response_json["final_answer"])
        is_correct = response_json["is_correct"]
        if working == "":
            working = "I was unable to attempt the question based on the provided explanation."
        return working, answer, is_correct

def attempt_question_incomplete(question, correct_solution, provided_concepts, provided_formulas, parsed_answers):

    provided_explanation = "Explanation: " + provided_concepts + "\n" + "Formulas: " + provided_formulas
    missing_concept_questions = ""
    start_ind = 1
    for concept_question in parsed_answers:
        if parsed_answers[concept_question] == "":
            missing_concept_questions += f"{str(start_ind)}) {concept_question}\n"
            start_ind += 1

    messages = [{"role": "developer", "content": incomplete_solver_instructions_question + question + "\n\n" + incomplete_solver_instructions_concepts_and_formulas + \
                 correct_solution + "\n\n" + incomplete_solver_instructions_response + "\n" + incomplete_solver_instructions_pointers},
        {"role": "user", "content": "Here is the provided explanation:\n" + provided_explanation + "\n" + "Provide an incomplete solution, without mentioning the correct concepts or formulas, because my explanation doesn't answer the following questions:\n" + missing_concept_questions}
    ]

    response = client.chat.completions.create(
        model=incomplete_solver_model,
        messages=messages,
        reasoning_effort="low",
        response_format={"type": "json_schema", 
                         "json_schema": {
                            "name": "incomplete_solution",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "steps": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "explanation": {"type": "string"},
                                                "calculation": {"type": "string"}
                                            },
                                            "required": ["explanation", "calculation"],
                                            "additionalProperties": False
                                        }
                                    }
                                },
                                "required": ["steps"],
                                "additionalProperties": False
                            }
                        }
    })

    if response.choices[0].message.refusal:
        working = "I was unable to attempt the question."
        answer = "Could not compute."
        is_correct = False
        return working, answer, is_correct
    else:
        response_json = json.loads(response.choices[0].message.content)
        working = ""
        for step in response_json["steps"]:
            try:
                working = working + correct_latex_formatting(step["explanation"]) + \
                    "\n" + correct_latex_formatting(step["calculation"]) + "\n"
            except:
                working = working + "I was unable to attempt the question based on the provided explanation."
                continue
        if working == "":
            working = "I was unable to attempt the question based on the provided explanation."
        answer = "Could not compute."
        is_correct = False
        return working, answer, is_correct

def parse_paragraph(provided_concepts, provided_formulas, concept_questions):
    concept_string = ""
    start_ind = 1
    for concept_question in concept_questions:
        concept_string += f"{str(start_ind)}) concept_question: {concept_question}\n"
        start_ind += 1
        if concept_answers[concept_question]['concept_answer'] != "":
            concept_string += f"possible_concept_answers: ['{concept_answers[concept_question]['concept_answer']}'"
            if concept_answers[concept_question]['concept_formula']:
                for f in concept_answers[concept_question]['concept_formula']:
                    if f == concept_answers[concept_question]['concept_formula'][-1]:
                        concept_string += f", '{f}']\n"
                    else:
                        concept_string += f", '{f}'"
            else:
                concept_string += "]\n"
        else:
            for f in concept_answers[concept_question]['concept_formula']:
                if f == concept_answers[concept_question]['concept_formula'][-1]:
                    concept_string += f", '{f}']\n"
                elif f == concept_answers[concept_question]['concept_formula'][0]:
                    concept_string += f"possible_concept_answers: ['{f}'"
                else:
                    concept_string += f", '{f}'"

    user_paragraph = "Paragraph: " + provided_concepts + "\n" + "Formulas: " + provided_formulas

    messages = [{"role": "system", "content": parser_instructions_concepts + concept_string + "\n\n" + parser_instructions_paragraph + \
                 "\n" + parser_instructions_response},
        {"role": "user", "content": "Parse the paragraph and formulas given below to find answers to the concept_questions. Remember, the answer CAN be a formula too.\n" + user_paragraph}
    ]

    response = client.chat.completions.create(
        model=parser_model,
        messages=messages,
        temperature=0.1,
        response_format={"type": "json_schema", 
                         "json_schema": {
                            "name": "user_answers",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "user_answers": {
                                        "type": "array", 
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "concept_question": {"type": "string"},
                                                "concept_answer": {"type": "string"},
                                                "concept_formula": {"type": "string"},
                                                "is_concept_correct": {"type": "boolean"}
                                            },
                                            "required": ["concept_question", "concept_answer", "concept_formula", "is_concept_correct"],
                                            "additionalProperties": False
                                        }
                                    }
                                },
                                "required": ["user_answers"],
                                "additionalProperties": False
                            }
                        }
    })

    parsed_concept_answers = {}
    is_correct_concept_answers = {}
    for concept_question in concept_questions:
        parsed_concept_answers[concept_question] = ""
        is_correct_concept_answers[concept_question] = False

    if response.choices[0].message.refusal:
        for concept_question in concept_questions:  
            parsed_concept_answers[concept_question] = ""
    else:
        response_json = json.loads(response.choices[0].message.content)
        for user_answer in response_json["user_answers"]:
            parsed_concept_answers[user_answer["concept_question"]] = user_answer["concept_answer"]
            if user_answer["concept_formula"] != "":
                parsed_concept_answers[user_answer["concept_question"]] += "\n" + user_answer["concept_formula"]
            is_correct_concept_answers[user_answer["concept_question"]] = user_answer["is_concept_correct"]
    return parsed_concept_answers, is_correct_concept_answers