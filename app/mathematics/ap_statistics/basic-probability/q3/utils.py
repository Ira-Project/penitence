import json
import math
from time import sleep
import random

from openai_client import client, groq_client
from parameters import *
from knowledge_graph import Graph


def get_embedding(text, model='text-embedding-3-small'):
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text], model=model).data[0].embedding


def create_and_run_missing_concepts_assistant_groq(explanation, concept_questions):

    instructions = missing_concepts_instructions_pre + \
        concept_questions + missing_concepts_instructions_post

    messages = [
        {
            "role": "system",
            "content": instructions
        },
        {
            "role": "user",
            "content": explanation
        }
    ]
    response = groq_client.chat.completions.create(
        model=missing_concepts_assistant_model,
        messages=messages
    )
    return response.choices[0].message.content


def create_and_run_concepts_present_assistant_groq(explanation, check_concept_ids, overall_kg, kg):
    answer_kg = Graph()
    messages = [{
        "role": "system",
        "content": concept_present_instructions
    }]

    start_thread = True
    for concept_id in check_concept_ids:
        user_message = "According to the context provided, " + \
            overall_kg.nodesDict[concept_id].concept_question
        if start_thread:
            messages.append({
                "role": "user",
                "content": "Context:\n'" + explanation + "'\n" + user_message
            })
        else:
            messages.append({
                "role": "user",
                "content": user_message
            })
        response = groq_client.chat.completions.create(
            messages=messages,
            model=concept_present_assistant_model,
            response_format={"type": "json_object"},
            temperature=0.5,
        )
        concept_present_json = response.choices[0].message.content
        concept_present_json = json.loads(concept_present_json)
        if concept_present_json["Answer Present"] == "Yes":
            answer_kg.add_node(concept_id, kg.nodesDict[concept_id].concept_uuid, kg.nodesDict[concept_id].concept_question, concept_present_json["Answer"],
                               kg.nodesDict[concept_id].similar_concepts, "", kg.nodesDict[concept_id].calc_required)
    return answer_kg


def create_and_run_concepts_apply_assistant_groq(problem, explanation_kg, concept_nodes):
    final_message = ""
    messages = [
        {
            "role": "system",
            "content": concept_apply_instructions_pre +
            problem + "\n" + concept_apply_instructions_post,
        },
    ]

    start_thread = True
    for concept_id in concept_nodes:
        if explanation_kg.nodesDict[concept_id].calc_required == "No":
            continue
        if start_thread:
            user_message = explanation_kg.nodesDict[concept_id].concept
            start_thread = False
        else:
            user_message = random.choice(concept_apply_starting_phrase)
            user_message = user_message + \
                explanation_kg.nodesDict[concept_id].concept

        user_message = user_message + "\n" + \
            "Apply this explanation to the given problem and based on the explanation, state the calculation."
        messages.append({
            "role": "user",
            "content": user_message
        })

        rerun = 0
        while (rerun < 5):
            print(rerun)
            rerun = rerun + 1
            try:
                response = groq_client.chat.completions.create(
                    messages=messages,
                    model=concept_apply_assistant_model,
                    response_format={"type": "json_object"},
                    temperature=0.2,
                )
                concept_apply_json = response.choices[0].message.content.replace(
                    '\n', '')
                concept_apply_json = json.loads(concept_apply_json)

                calculation_result = perform_calculation(
                    concept_apply_json["Calculation"])
            except:
                continue

        final_message = final_message + concept_apply_json["Response"] + "\n" + "Calculation: " + \
            str(calculation_result) + "\n"

        messages.append({
            "role": "assistant",
            "content": str(final_message)
        })

    return final_message, calculation_result


def perform_calculation(string):
    if string:
        if isinstance(string, str):
            string_split = string.split("(")
            operation = string_split[0]
            if operation == "add":
                sum = 0
                for num in string_split[1].split(")")[0].split(","):
                    num = float(num.strip())
                    sum = sum + num
                return sum
            if operation == "multiply":
                prod = 1
                for num in string_split[1].split(")")[0].split(","):
                    num = float(num.strip())
                    prod = prod * num
                return prod
            if operation == "subtract":
                sub = 0
                start = True
                for num in string_split[1].split(")")[0].split(","):
                    num = float(num.strip())
                    if start:
                        sub = num
                        start = False
                    else:
                        sub = sub - num
                return sub
            if operation == "divide":
                div = 1
                start = True
                for num in string_split[1].split(")")[0].split(","):
                    num = float(num.strip())
                    if start:
                        div = num
                        start = False
                    else:
                        div = div / num
                return div
        else:
            return string
    else:
        return None


def cosine_similarity(vector1, vector2):
    dot_product = sum(a * b for a, b in zip(vector1, vector2))

    magnitude1 = math.sqrt(sum(a**2 for a in vector1))
    magnitude2 = math.sqrt(sum(b**2 for b in vector2))

    if magnitude1 == 0 or magnitude2 == 0:
        return 0

    cosine_similarity = dot_product / (magnitude1 * magnitude2)

    cosine_distance = 1 - cosine_similarity

    return cosine_distance
