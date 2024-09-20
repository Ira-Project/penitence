from ..utils import *
from ..parameters import *
from .....input_models import InputModel
from .question import question_json


async def compute_q1(input: InputModel):

    learner_explanation = input.explanation

    # Initialize the dictionaries
    required_concepts_dict = {}
    not_required_concepts_dict = {}

    # Initialize the concepts in the dictionaries
    for concept_array in question_json["required_concepts"]:
        for concept in concept_array:
            required_concepts_dict[concept] = ""
    for concept in question_json["not_required_concepts"]:
        not_required_concepts_dict[concept] = ""

    # Convert required and not_required concepts to a list of questions
    question_list = ""
    for concept_question in required_concepts_dict.keys():
        question_list = question_list + concept_question + "\n"
    for concept_question in not_required_concepts_dict.keys():
        question_list = question_list + concept_question + "\n"

    # Get answers to the question_list
    tagged_concepts_dict = await read_explanation(question_list, learner_explanation)

    if not tagged_concepts_dict or not learner_explanation:
        return {
            'status': 500,
            'body': 'Please send valid concept dictionaries and a valid explanation'
        }

    # Initialize the dictionaries
    required_concepts_dict = {}
    not_required_concepts_dict = {}
    concept_status = []

    # Initialize the concepts in the dictionaries
    for concept_array in question_json["required_concepts"]:
        for concept in concept_array:
            required_concepts_dict[concept] = ""
    for concept in question_json["not_required_concepts"]:
        not_required_concepts_dict[concept] = ""

    # Update the dictionaries with the tagged concepts
    for verification in tagged_concepts_dict["verifications"]:
        if verification['verification_question'] in required_concepts_dict:
            required_concepts_dict[verification['verification_question']
                                   ] = verification['verification_answer']
            concept_status.append({
                'text': verification['verification_question'],
                'status': verification['verification_answer']
            })
        elif verification['verification_question'] in not_required_concepts_dict:
            not_required_concepts_dict[verification['verification_question']
                                       ] = verification['verification_answer']
            concept_status.append({
                'text': verification['verification_question'],
                'status': verification['verification_answer']
            })

    answer = ""
    correct = False
    q = question_json["Question"]
    r_c = question_json["required_concepts"]
    k_c = question_json["known_concepts"]
    n_r_c = question_json["not_required_concepts"]
    if required_concepts_dict[r_c[0][0]] == "Yes":
        k_c.append("negative charges will repel one another")
        answer = answer + "Based on your explanation, I understood that negative charges will repel one another."
        if required_concepts_dict[r_c[0][1]] == "Yes" and required_concepts_dict[r_c[0][2]] == "No":
            k_c.append("conductors and insulators allow free flow of charge")
            answer = answer + "\nI also understood that conductors and insulators both allow charges to flow freely within them, so I think the negative charges present within the wollen ball and the metal sphere will try to move away from each other and come to reside on the surface."
        elif required_concepts_dict[r_c[0][1]] == "Yes" and required_concepts_dict[r_c[0][2]] == "Unknown":
            k_c.append("conductors allow free flow of charge")
            answer = answer + "\nI also understood that conductors allow charges to flow freely within them, so I think the negative charges present within the metal sphere will try to move away from each other and come to reside on the surface."
            answer = answer + " But, I do not know how to find out where the charges will reside on the woollen ball."
        elif required_concepts_dict[r_c[0][1]] == "Yes" and required_concepts_dict[r_c[0][2]] == "Yes":
            k_c.append(
                "conductors allow free flow of charge and insulators prevent free flow of charge")
            answer = answer + " I also understood that conductors allow charges to flow freely within them while insulators prevent charges from freely flowing within them."
            answer = answer + " \nSo, the negative charges present within the metal sphere will move away from each other and come to reside on the surface while in case of the woollen ball, they will be unable to move away from each other and be distributed across the entire volume."
            correct = True
        elif required_concepts_dict[r_c[0][1]] == "No" and required_concepts_dict[r_c[0][2]] == "Yes":
            k_c.append(
                "conductors and insulators both prevent charge from flowing freely within them")
            answer = answer + "\nI also understood that conductors and insulators both prevent charges from flowing freely within them, so I think the negative charges present within the wollen ball and the metal sphere will be unable to move away from each other and be distributed across the entire volume."
        elif required_concepts_dict[r_c[0][1]] == "No" and required_concepts_dict[r_c[0][2]] == "Unknown":
            k_c.append(
                "conductors prevent charge from flowing freely within them")
            answer = answer + "\nI also understood that conductors prevent charges from flowing freely within them, so I think the negative charges present within the metal sphere will be unable to move away from each other and be distributed across the entire volume."
            answer = answer + " But, I do not know how to find out where the charges will reside on the woollen ball."
        elif required_concepts_dict[r_c[0][1]] == "No" and required_concepts_dict[r_c[0][2]] == "No":
            k_c.append(
                "insulators allow free flow of charge and conductors prevent free flow of charge")
            answer = answer + " I also understood that insulators allow charges to flow freely within them while conductors prevent charges from freely flowing within them."
            answer = answer + " \nSo, the negative charges present within the woollen ball will move away from each other and come to reside on the surface while in case of the metal sphere, they will be unable to move away from each other and be distributed across the entire volume."
        elif required_concepts_dict[r_c[0][1]] == "Unknown" and required_concepts_dict[r_c[0][2]] == "Yes":
            k_c.append(
                "insulators prevent charge from flowing freely within them")
            answer = answer + "\nI also understood that insulators prevent charges from flowing freely within them, so I think the negative charges present within the woollen ball will be unable to move away from each other and be distributed across the entire volume."
            answer = answer + " But, I do not know how to find out where the charges will reside on the metal sphere."
        elif required_concepts_dict[r_c[0][1]] == "Unknown" and required_concepts_dict[r_c[0][2]] == "No":
            k_c.append("insulators allow free flow of charge")
            answer = answer + "\nI also understood that insulators allow charges to flow freely within them, so I think the negative charges present within the woollen ball will try to move away from each other and come to reside on the surface."
            answer = answer + " But, I do not know how to find out where the charges will reside on the metal sphere."
        elif required_concepts_dict[r_c[0][1]] == "Unknown" and required_concepts_dict[r_c[0][2]] == "Unknown":
            answer = answer + " So, for both the woollen ball and the metal sphere, I think the charges will try to move away from each other and reside on the surface."
    elif required_concepts_dict[r_c[0][0]] == "Unknown":
        if required_concepts_dict[r_c[0][1]] == "Yes" and required_concepts_dict[r_c[0][2]] == "No":
            k_c.append("conductors and insulators allow free flow of charge")
            answer = answer + "Based on your explanation, I understood that conductors and insulators both allow charges to flow freely within them, but I am not sure how to figure out where the charges will reside."
        elif required_concepts_dict[r_c[0][1]] == "Yes" and required_concepts_dict[r_c[0][2]] == "Unknown":
            k_c.append("conductors allow free flow of charge")
            answer = answer + "Based on your explanation, I understood that conductors allow charges to flow freely within them. But I don't know how to figure out where the charges will reside on both the woollen ball and the metal sphere."
        elif required_concepts_dict[r_c[0][1]] == "Yes" and required_concepts_dict[r_c[0][2]] == "Yes":
            k_c.append(
                "conductors allow free flow of charge and insulators prevent free flow of charge")
            answer = answer + "Based on your explanation, I understood that conductors allow charges to flow freely within them while insulators prevent charges from freely flowing within them."
            answer = answer + " But I don't know how to figure out where these charges will reside."
        elif required_concepts_dict[r_c[0][1]] == "No" and required_concepts_dict[r_c[0][2]] == "Yes":
            k_c.append(
                "conductors and insulators both prevent charge from flowing freely within them")
            answer = answer + "Based on your explanation, I understood that conductors and insulators both prevent charges from flowing freely within them, but I am not sure how to figure out where the charges will reside."
        elif required_concepts_dict[r_c[0][1]] == "No" and required_concepts_dict[r_c[0][2]] == "Unknown":
            k_c.append(
                "conductors prevent charge from flowing freely within them")
            answer = answer + "Based on your explantion, I understood that conductors prevent charges from flowing freely within them. But I don't know how to figure out where the charges will reside."
        elif required_concepts_dict[r_c[0][1]] == "No" and required_concepts_dict[r_c[0][2]] == "No":
            k_c.append(
                "insulators allow free flow of charge and conductors prevent free flow of charge")
            answer = answer + "Based on your explanation, I understood that insulators allow charges to flow freely within them while conductors prevent charges from freely flowing within them."
            answer = answer + " But I don't know how to figure out where these charges they will reside."
        elif required_concepts_dict[r_c[0][1]] == "Unknown" and required_concepts_dict[r_c[0][2]] == "Yes":
            k_c.append(
                "insulators prevent charge from flowing freely within them")
            answer = answer + "Based on your explanation, I understood that insulators prevent charges from flowing freely within them, but I am not sure how to figure out where these charges will reside."
        elif required_concepts_dict[r_c[0][1]] == "Unknown" and required_concepts_dict[r_c[0][2]] == "No":
            k_c.append("insulators allow free flow of charge")
            answer = answer + "Based on your explanation, I understood that insulators allow charges to flow freely within them, but I am not sure how how to figure out where these charges will reside."
        elif required_concepts_dict[r_c[0][1]] == "Unknown" and required_concepts_dict[r_c[0][2]] == "Unknown":
            answer = answer + "I can't figure how to answer this question based on your explanation."
    elif required_concepts_dict[r_c[0][0]] == "No":
        follow_up_json = await read_explanation(
            "1) Do negative charges attract each other?", learner_explanation)
        if follow_up_json["verifications"][0]['verification_answer'] == "Yes":
            k_c.append("negative charges will attract one another")
            answer = answer + "Based on your explanation, I understood that negative charges will attract one another."
            if required_concepts_dict[r_c[0][1]] == "Yes" and required_concepts_dict[r_c[0][2]] == "No":
                k_c.append(
                    "conductors and insulators allow free flow of charge")
                answer = answer + "\nI also understood that conductors and insulators both allow charges to flow freely within them, so I think the negative charges present within the wollen ball and the metal sphere will try to move towards each other and come to reside in the center."
            elif required_concepts_dict[r_c[0][1]] == "Yes" and required_concepts_dict[r_c[0][2]] == "Unknown":
                k_c.append("conductors allow free flow of charge")
                answer = answer + "\nI also understood that conductors allow charges to flow freely within them, so I think the negative charges present within the metal sphere will try to move towards each other and come to reside in the center."
                answer = answer + " But, I do not know how to find out where the charges will reside on the woollen ball."
            elif required_concepts_dict[r_c[0][1]] == "Yes" and required_concepts_dict[r_c[0][2]] == "Yes":
                k_c.append(
                    "conductors allow free flow of charge and insulators prevent free flow of charge")
                answer = answer + " I also understood that conductors allow charges to flow freely within them while insulators prevent charges from freely flowing within them."
                answer = answer + " \nSo, the negative charges present within the metal sphere will move towards each other and come to reside in the center while in case of the woollen ball, they will be unable to move towards each other and be distributed across the entire volume."
            elif required_concepts_dict[r_c[0][1]] == "No" and required_concepts_dict[r_c[0][2]] == "Yes":
                k_c.append(
                    "conductors and insulators both prevent charge from flowing freely within them")
                answer = answer + "\nI also understood that conductors and insulators both prevent charges from flowing freely within them, so I think the negative charges present within the wollen ball and the metal sphere will be unable to move towards each other and be distributed across the entire volume."
            elif required_concepts_dict[r_c[0][1]] == "No" and required_concepts_dict[r_c[0][2]] == "Unknown":
                k_c.append(
                    "conductors prevent charge from flowing freely within them")
                answer = answer + "\nI also understood that conductors prevent charges from flowing freely within them, so I think the negative charges present within the metal sphere will be unable to move towards each other and be distributed across the entire volume."
                answer = answer + " But, I do not know how to find out where the charges will reside on the woollen ball."
            elif required_concepts_dict[r_c[0][1]] == "No" and required_concepts_dict[r_c[0][2]] == "No":
                k_c.append(
                    "insulators allow free flow of charge and conductors prevent free flow of charge")
                answer = answer + " I also understood that insulators allow charges to flow freely within them while conductors prevent charges from freely flowing within them."
                answer = answer + " \nSo, the negative charges present within the woollen ball will move towards each other and come to reside in the center while in case of the metal sphere, they will be unable to move towards each other and be distributed across the entire volume."
            elif required_concepts_dict[r_c[0][1]] == "Unknown" and required_concepts_dict[r_c[0][2]] == "Yes":
                k_c.append(
                    "insulators prevent charge from flowing freely within them")
                answer = answer + "\nI also understood that insulators prevent charges from flowing freely within them, so I think the negative charges present within the woollen ball will be unable to move towards each other and be distributed across the entire volume."
                answer = answer + " But, I do not know how to find out where the charges will reside on the metal sphere."
            elif required_concepts_dict[r_c[0][1]] == "Unknown" and required_concepts_dict[r_c[0][2]] == "No":
                k_c.append("insulators allow free flow of charge")
                answer = answer + "\nI also understood that insulators allow charges to flow freely within them, so I think the negative charges present within the woollen ball will try to move towards each other and come to reside in the center."
                answer = answer + " But, I do not know how to find out where the charges will reside on the metal sphere."
            elif required_concepts_dict[r_c[0][1]] == "Unknown" and required_concepts_dict[r_c[0][2]] == "Unknown":
                answer = answer + " So, for both the woollen ball and the metal sphere, I think the charges will try to move towards each other and reside in the center."
        else:
            k_c.append(
                "negative charges will neither attract nor repel one another")
            answer = answer + "Based on your explanation, I understood that negative charges will have no effect on each other. So the charges will be distributed across the entire volume in both the woollen ball and the metal sphere."
    if not correct:
        if not_required_concepts_dict[n_r_c[0]] == "Yes" and not_required_concepts_dict[n_r_c[1]] == "Yes":
            answer = "You mentioned that charges reside on the surface of the conductor and are present across the volume of an insulator. But can you explain how to come to that conclusion?\n" + answer
        else:
            if not_required_concepts_dict[n_r_c[0]] == "Yes":
                answer = "You mentioned that charges reside on the surface of the conductor. But can you explain how to come to that conclusion?" + "\n" + answer
            if not_required_concepts_dict[n_r_c[1]] == "Yes":
                answer = "You mentioned that charges are present across the volume of an insulator. But can you explain how to come to that conclusion?" + "\n" + answer
    working, answer = await output_answer(q, answer)

    return {
        'status': 200,
        'body': {
            'isCorrect': correct,
            'working': working,
            'answer': answer,
            'concepts': concept_status
        }
    }
