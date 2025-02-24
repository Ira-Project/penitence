import json
from .parameters import *
from .....openai_client import client

# Put LaTeX text within delimeters
latex_delimeter = "$!$"


def insert_latex(str):
    return latex_delimeter + str + latex_delimeter


def solve_question(question, required_concepts, required_formulas):

    concept_questions_list = "concept_questions: ["
    for concept in required_concepts:
        concept_questions_list = concept_questions_list + concept + ",\n"
    concept_questions_list = concept_questions_list + "]"

    concept_answers_list = "concept_answers: ["
    for concept in required_concepts:
        concept_answers_list = concept_answers_list + \
            concept_answers[concept] + ",\n"
    concept_answers_list = concept_answers_list + "]"

    concept_formulas_list = "concept_formulas: ["
    for formula in required_formulas:
        concept_formulas_list = concept_formulas_list + formula + ",\n"
    concept_formulas_list = concept_formulas_list + "]"

    messages = [{"role": "system", "content": ai_solver_instructions_question + question + "\n\n" + ai_solver_instructions_concepts +
                 concept_questions_list + "\n" + concept_answers_list + "\n" + ai_solver_instructions_formulas + concept_formulas_list + "\n\n" +
                 ai_solver_instructions_correct_answer_pointers},
                {"role": "user", "content": "Solve the question by applying ALL the 'concept_answers' and 'concept_formulas' provided. You DO NOT need any other formula to solve the question."}
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
            correct_solution = correct_solution + \
                step["explanation"] + "\n" + step["calculation"] + "\n"
        correct_solution = correct_solution + \
            "Correct Answer: " + response_json["final_answer"]
        print(correct_solution)
        return correct_solution


def attempt_question(question, required_concepts, required_formulas, correct_solution, provided_concepts, provided_formulas):
    required_concepts_questions_list = "required_concept_questions: ["
    for concept in required_concepts:
        required_concepts_questions_list = required_concepts_questions_list + concept + ",\n"
    required_concepts_questions_list = required_concepts_questions_list + "]"

    required_concepts_answers_list = "required_concept_answers: ["
    for concept in required_concepts:
        required_concepts_answers_list = required_concepts_answers_list + \
            concept_answers[concept] + ",\n"
    required_concepts_answers_list = required_concepts_answers_list + "]"

    required_formulas_list = "required_formulas: ["
    for formula in required_formulas:
        required_formulas_list = required_formulas_list + formula + ",\n"
    required_formulas_list = required_formulas_list + "]"

    required_concept_missing_list = "required_concept_missing: ["
    for concept in required_concepts:
        required_concept_missing_list = required_concept_missing_list + \
            concept_missing[concept] + ",\n"
    required_concept_missing_list = required_concept_missing_list + "]"

    required_formulas_missing_list = "required_formulas_missing: ["
    for formula in required_formulas:
        required_formulas_missing_list = required_formulas_missing_list + \
            concept_formulas_missing[formula] + ",\n"
    required_formulas_missing_list = required_formulas_missing_list + "]"

    messages = [{"role": "system", "content": ai_student_instructions_question + question + "\n\n" + ai_student_instructions_required_concepts +
                required_concepts_questions_list + "\n" + required_concepts_answers_list + "\n" + ai_student_instructions_required_formulas +
                required_formulas_list + "\n" + ai_student_instructions_required_concept_missing + "\n" + required_concept_missing_list + "\n" +
                ai_student_instructions_required_formulas_missing + "\n" + required_formulas_missing_list + "\n\n" +
                correct_solution + "\n\n" + ai_student_instructions_pointers},
                {"role": "user", "content": "Use the teacher's explanation to attempt the question. Till the teacher correctly mentions all the required_concept_answers and required_formulas, you CANNOT give the correct solution. In the case that NONE of the required_concept_answers are mentioned, you must state that you do not know how to solve the question. Never mention the required concept answers or formulas.\n" +
                    "The teacher states that:\n" + provided_concepts + "\n" + "The teacher also provides the following formulas:\n" + provided_formulas}
                ]

    response = client.chat.completions.create(
        model=ai_student_model,
        messages=messages,
        reasoning_effort="low",
        response_format={"type": "json_schema",
                         "json_schema": {
                             "name": "attempted_solution",
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
                             },
                             "strict": True
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