import os
import pickle
import random

from openai_client import client
from utils import *
from knowledge_graph import Graph
from parameters import *


question = "In a single throw of a dice, find the probability of getting a number greater than 2"
answer_list = ["2/3", str(2/3), 2/3, "0.6667"]


def lambda_handler(event, context):
    kg = Graph()
    kg.populate_graph_from_JSON("concepts.json")
    kg_start_nodes = [1]

    # Read embedding of concepts
    with open('concept_embeddings.pkl', 'rb') as f:
        embedded_concepts = pickle.load(f)

    # Retrieve knowledge graph of a specific question
    with open('question_knowledge_graph.pkl', 'rb') as f:
        question_adjacency_dict = pickle.load(f)

    question_kg = Graph()
    question_kg.populate_graph_from_adjacency_dict(question_adjacency_dict, kg)

    kg.remove_nodes([8])
    question_kg.remove_nodes([8])

    # Get explanation from Input
    body = json.loads(event.get('body'))
    prompt = body.get('explanation')
    if not prompt:
        return {
            'status': 500,
            'body': 'Please enter a valid explanation.'
        }
    prompt_len = len(prompt)

    # --------
    # Check what are the concepts present in the explanation
    # --------

    if prompt_len <= 100:
        threshold = 0.6
    elif prompt_len > 100 and prompt_len <= 200:
        threshold = 0.55
    elif prompt_len > 200 and prompt_len <= 250:
        threshold = 0.50
    else:
        threshold = 0.45

    explanation_embedding = get_embedding(prompt)
    explanation_dict = {}
    concept_ids_present = set()

    for concept_id in question_kg.nodesDict.keys():
        # will consist of cosine similarity values and presence of concept
        explanation_dict[concept_id] = []
        max_cosine_sim = -1000
        for concept_embedding in embedded_concepts[concept_id]:
            cosine_sim = 1 - \
                cosine_similarity(concept_embedding, explanation_embedding)
            if cosine_sim > max_cosine_sim:
                max_cosine_sim = cosine_sim
        explanation_dict[concept_id].append(max_cosine_sim)
        if max_cosine_sim < threshold:
            explanation_dict[concept_id].append("No")
        else:
            explanation_dict[concept_id].append("Yes")
            concept_ids_present.add(concept_id)

    # --------
    # Handle case when no concepts are present in the explanation
    # --------
    response_message = ""
    if len(concept_ids_present) == 0:
        response_message = random.choice(no_explanation_responses)
        return {
            'status': 200,
            'body': {
                'isCorrect': False,
                'working': response_message,
                'answer': 'Could not compute'
            }
        }

    # --------
    # Handle other cases
    # --------

    valid_nodes, isolated_nodes = question_kg.get_valid_subgraph(
        concept_ids_present, kg_start_nodes)
    if len(valid_nodes) == 0:
        missing_concepts = question_kg.get_missing_parent_concepts(
            concept_ids_present, kg_start_nodes)
        missing_concept_questions, _ = kg.get_concept_questions(
            missing_concepts)
        response_message = create_and_run_missing_concepts_assistant_groq(
            prompt, missing_concept_questions)
        return {
            'status': 200,
            'body': {
                'isCorrect': False,
                'working': response_message,
                'answer': 'Could not compute'
            }
        }
    else:
        answer_kg = create_and_run_concepts_present_assistant_groq(
            prompt, concept_ids_present, kg, kg=kg)
        apply_concept_nodes, other_nodes = question_kg.get_valid_subgraph(
            set(answer_kg.nodesDict.keys()), kg_start_nodes)

        if other_nodes:
            missing_concepts = question_kg.get_missing_concepts(
                set(answer_kg.nodesDict.keys()), kg_start_nodes)
            missing_concept_questions, _ = kg.get_concept_questions(
                missing_concepts)
            response_message = create_and_run_missing_concepts_assistant_groq(
                prompt, missing_concept_questions)
            return {
                'status': 200,
                'body': {
                    'isCorrect': False,
                    'working': response_message,
                    'answer': 'Could not compute'
                }
            }

        if apply_concept_nodes:
            response_message, computed_answer = create_and_run_concepts_apply_assistant_groq(
                question, answer_kg, apply_concept_nodes)
            is_correct = computed_answer in answer_list or str(
                computed_answer) in answer_list
            return {
                'status': 200,
                'body': {
                    'isCorrect': is_correct,
                    'working': response_message,
                    'answer': str(round(computed_answer, 4)),
                }
            }

    return {
        'status': 500,
        'body': 'Something went wrong. Please try again.'
    }


if __name__ == '__main__':
    response = lambda_handler({
        "body": "{\"explanation\": \"Probability is equal to the favourable outcomes. Favourable outcomes are the events we want to happen and total outcomes are all the possible things that can happen. For multiple events the probability is computed as the product of each event.\"}"
    }, {})
    print(response)
