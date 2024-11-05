import json

from ....openai_client import client
from .parameters import *

# Put LaTeX text within delimeters
latex_delimeter = "$!$"


async def read_explanation(concept_questions, explanation):
    response = client.chat.completions.create(
        model=read_explanation_model,
        messages=[
            {"role": "system", "content": read_explanation_instructions + concept_questions},
            {"role": "user", "content": read_explanation_prompt_pre + explanation},
        ],
        response_format={"type": "json_object"},
        temperature=0.5
    )
    response_message = json.loads(response.choices[0].message.content)
    return response_message


async def answer_explanation(concept_question, explanation, json_instruction):
    response = client.chat.completions.create(
        model=answer_explanation_model,
        messages=[
            {"role": "system", "content": answer_explanation_instructions +
                concept_question + "\n" + json_instruction},
            {"role": "user", "content": answer_explanation_prompt_pre + explanation},
        ],
        response_format={"type": "json_object"}
    )
    response_message = json.loads(response.choices[0].message.content)
    return response_message


def insert_latex(str):
    return latex_delimeter + str + latex_delimeter


def formula_reader(formula_question, formula_array):
    response = client.chat.completions.create(
        model=formula_reader_model,
        messages=[
            {"role": "system", "content": formula_reader_instructions},
            {"role": "user", "content": formula_reader_prompt_pre +
             formula_question + "\n" + formula_reader_prompt_post + formula_array},
        ],
        response_format={"type": "json_object"},
        temperature=0.3
    )
    response_message = json.loads(response.choices[0].message.content)
    print("Formula Reader Response: ", response_message)
    return response_message
