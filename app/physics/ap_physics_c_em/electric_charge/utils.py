import json

from ....openai_client import client
from .parameters import *


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


async def output_answer(question, solution):
    response = client.chat.completions.create(
        model=output_answer_model,
        messages=[
            {"role": "system", "content": output_answer_instructions},
            {"role": "user", "content": output_answer_prompt_pre +
                question + output_answer_prompt_post + solution},
        ],
        response_format={"type": "json_object"}
    )
    response_message = json.loads(response.choices[0].message.content)
    return response_message.get("answer")
