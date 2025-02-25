import json
from .parameters import *
from .....openai_client import client

# Put LaTeX text within delimeters
latex_delimeter = "$!$"


def insert_latex(str):
    return latex_delimeter + str + latex_delimeter

def solve_question(question, required_concepts):
    concepts_string = ""
    start_ind = 1
    for concept_question in required_concepts:
        concepts_string += f"{str(start_ind)}) required_concept_question: {concept_question}\n"
        concepts_string += f"concept_answer: {concept_answers[concept_question]['concept_answer']}\n"
        concepts_string += f"concept_formula: {concept_answers[concept_question]['concept_formula']}\n"
        start_ind += 1

    messages = [{"role": "system", "content": ai_solver_instructions_question + question + "\n\n" + ai_solver_instructions_concepts_and_formulas + \
                 concepts_string + "\n\n" + ai_solver_instructions_correct_answer_pointers},
        {"role": "user", "content": "Solve the question by applying ALL the 'concept_answers' and 'concept_formulas' provided. You DO NOT need any other formula to solve the question."}
    ]

    print(ai_solver_instructions_question + question + "\n\n" + ai_solver_instructions_concepts_and_formulas + \
                 concepts_string + "\n\n" + ai_solver_instructions_correct_answer_pointers)

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
        concepts_string += f"required_concept_missing: {concept_missing[concept_question]}\n"
        start_ind += 1

    messages = [{"role": "system", "content": ai_student_instructions_question + question + "\n\n" + ai_student_instructions_required_concepts_and_formulas + \
                concepts_string + "\n\n" + correct_solution + "\n\n" + ai_student_instructions_pointers},
        {"role": "user", "content": "In first person, use the teacher's explanation to attempt the question in steps. Till the teacher correctly mentions ANY ONE of the 'required_concept_answers' for EVERY 'required_concept_question', you CANNOT give the correct solution. Never state ANY OF THE 'required_concept_answers'.\n" + "The teacher explains that:\n" + provided_concepts + "\n" + "The teacher also provides the following formulas:\n" + provided_formulas}
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
        # print("Refusal: ", response.choices[0].message.refusal)
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