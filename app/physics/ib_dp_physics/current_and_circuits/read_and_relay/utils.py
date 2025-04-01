import json
from .parameters import *
from .....openai_client import client

# Put LaTeX text within delimeters
latex_delimeter = "$!$"


def insert_latex(str):
    return latex_delimeter + str + latex_delimeter
    
def get_required_concepts(passage, question):
    
    messages = [{"role": "developer", "content": extract_concepts_instructions + passage + "\n\n" + extract_concepts_response_format},
        {"role": "user", "content": "Extract the required concepts for the given question:\n" + question}
    ]

    response = client.chat.completions.create(
        model=extract_concepts_model,
        messages=messages,
        reasoning_effort="medium",
        response_format={"type": "json_schema", 
                            "json_schema": {
                                "name": "required_concepts",
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "extracted_concepts": {
                                            "type": "array", 
                                            "items": {"type": "string"}
                                        }
                                    },
                                    "required": ["extracted_concepts"],
                                    "additionalProperties": False
                                }
                            }
                    }       
    )

def attempt_question(required_concepts, question, given_concepts):

    messages = [{"role": "developer", "content": attempt_question_instructions_question + question + "\n" + \
                attempt_question_instructions_response + attempt_question_instructions_pointers},
        {"role": "user", "content": "These are the concepts you have been given:\n" + given_concepts + "\n" + \
         "You have to give incomplete solutions till I mention the concepts and formulas needed to solve the question. You are NOT ALLOWED to reveal the concepts and formulas to me. If the information provided by me is sufficient to solve the question, you should respond with the correct AND complete solution."}
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
                    }
    )

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
                working = working + step["explanation"] + \
                    "\n" + insert_latex(step["calculation"]) + "\n"
            except:
                working = working + "I was unable to attempt the question based on the provided explanation."
                continue
        if response_json["final_answer"] == "":
            answer = "Could not compute"
        else:
            answer = insert_latex(response_json["final_answer"])
        is_correct = response_json["is_correct"]
        if working == "":
            working = "I was unable to attempt the question based on the provided explanation."

        return working, answer, is_correct
        
