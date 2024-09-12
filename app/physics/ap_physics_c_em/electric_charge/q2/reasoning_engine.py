from ..utils import *
from ..parameters import *
from .....input_models import InputModel
from .question import question_json


async def compute_q2(input: InputModel):

    learner_explanation = input.explanation
    tagged_concepts_dict = input.concepts
    if not tagged_concepts_dict or not learner_explanation:
        return {
            'status': 500,
            'body': 'Please send valid concept dictionaries and a valid explanation'
        }

    # Initialize the dictionaries
    required_concepts_dict = {}
    not_required_concepts_dict = {}

    # Initialize the concepts in the dictionaries
    for concept_array in question_json["required_concepts"]:
        for concept in concept_array:
            required_concepts_dict[concept] = ""
    for concept in question_json["not_required_concepts"]:
        not_required_concepts_dict[concept] = ""

    # Update the dictionaries with the tagged concepts
    for verification in tagged_concepts_dict:
        if verification.verification_question in required_concepts_dict:
            required_concepts_dict[verification.verification_question] = verification.verification_answer
        elif verification.verification_question in not_required_concepts_dict:
            not_required_concepts_dict[verification.verification_question] = verification.verification_answer

    answer = ""
    correct = False
    q = question_json["Question"]
    r_c = question_json["required_concepts"]
    k_c = question_json["known_concepts"]
    n_r_c = question_json["not_required_concepts"]

    if required_concepts_dict[r_c[0][0]] == "Yes":
        k_c.append("there are two types of charges")
        if required_concepts_dict[r_c[0][1]] == "Yes":
            k_c.append(
                "positive and negative charges are the two types of charges")
            if required_concepts_dict[r_c[0][2]] == "Yes":
                k_c.append("opposite charges attract each other")
                answer = answer + "Based on your explanation, I understood that positive and negative charges are two types of charges and opposite charges attract each other."
                answer = answer + " So, one metal sphere will have a postive charge and the other will have a negative charge."
                correct = True
            elif required_concepts_dict[r_c[0][2]] == "No":
                follow_up_json = await read_explanation(
                    "Do opposite charges repel each other?", learner_explanation)
                if follow_up_json["verifications"][0]['verification_answer'] == "Yes":
                    k_c.append("opposite charges repel each other")
                    answer = answer + "Based on your explanation, I understood that positive and negative charges are two types of charges and opposite charges repel each other."
                    answer = answer + " But, I don't know how to figure out which charges are on the spheres."
                elif follow_up_json["verifications"][0]['verification_answer'] == "No":
                    k_c.append(
                        "opposite charges neither attract nor repel each other")
                    answer = answer + "Based on your explanation, I understood that positive and negative charges are two types of charges and opposite charges neither attract nor repel each other."
                    answer = answer + " But, I don't know how to figure out which charges are on the spheres."
                else:
                    follow_up_json = await read_explanation(
                        "Do like charges attract each other?", learner_explanation)
                    if follow_up_json["verifications"][0]['verification_answer'] == "Yes":
                        k_c.append("like charges attract each other")
                        answer = answer + "Based on your explanation, I understood that positive and negative charges are two types of charges and like charges attract each other."
                        answer = answer + \
                            " So, both the metal spheres have a postive charge or both have a negative charge."
                    else:
                        answer = answer + "Based on your explanation, I understood that positive and negative charges are two types of charges and opposite charges do not attract each other."
                        answer = answer + " So, the spheres don't have opposite charges on them. Maybe both the metal spheres have a postive charge or maybe both have a negative charge."
            elif required_concepts_dict[r_c[0][2]] == "Unknown":
                answer = answer + "Based on your explanation, I understood that positive and negative charges are two types of charges but using just that, I don't know how to determine the nature of the charges on the spheres that attract one another."
        elif required_concepts_dict[r_c[0][1]] == "No":
            follow_up_answer = await answer_explanation("What are the two types of charges?", learner_explanation,
                                                        "Your response should be a json object 'charges' containing an array of the two types of charges.")
            charge_1 = follow_up_answer['charges'][0]
            charge_2 = follow_up_answer['charges'][1]
            print(follow_up_answer)
            k_c.append(charge_1 + " and " + charge_2 +
                       " are the two types of charges")
            if required_concepts_dict[r_c[0][2]] == "Yes":
                k_c.append(charge_1 + " and " + charge_2 +
                           " charges attract each other")
                answer = answer + "Based on your explanation, I understood that " + charge_1 + " and " + \
                    charge_2 + " are the two types of charges and opposite charges attract each other."
                answer = answer + " So, one metal sphere will have a " + charge_1 + \
                    " charge and the other will have a " + charge_2 + " charge."
            elif required_concepts_dict[r_c[0][2]] == "No":
                follow_up_json = await read_explanation(
                    "Do opposite charges repel each other?", learner_explanation)
                if follow_up_json["verifications"][0]['verification_answer'] == "Yes":
                    k_c.append("opposite charges repel each other")
                    answer = answer + "Based on your explanation, I understood that " + charge_1 + " and " + \
                        charge_2 + " are the two types of charges and opposite charges repel each other."
                    answer = answer + " But, I don't know how to figure out which charges are on the spheres."
                elif follow_up_json["verifications"][0]['verification_answer'] == "No":
                    k_c.append(
                        "opposite charges neither attract nor repel each other")
                    answer = answer + "Based on your explanation, I understood that " + charge_1 + " and " + charge_2 + \
                        " are the two types of charges and opposite charges neither attract nor repel each other."
                    answer = answer + " But, I don't know how to figure out which charges are on the spheres."
                else:
                    follow_up_json = await read_explanation(
                        "Do like charges attract each other?", learner_explanation)
                    if follow_up_json["verifications"][0]['verification_answer'] == "Yes":
                        k_c.append("like charges attract each other")
                        answer = answer + "Based on your explanation, I understood that " + charge_1 + " and " + \
                            charge_2 + " are the two types of charges and like charges attract each other."
                        answer = answer + " So, both the metal spheres have a " + \
                            charge_1 + " charge or both have a " + charge_2 + " charge."
                    else:
                        answer = answer + "Based on your explanation, I understood that " + charge_1 + " and " + \
                            charge_2 + " are the two types of charges and opposite charges do not attract each other."
                        answer = answer + " So, the spheres don't have opposite charges on them. Maybe both the metal spheres have a " + \
                            charge_1 + " charge or maybe both have a " + charge_2 + " charge."
            elif required_concepts_dict[r_c[0][2]] == "Unknown":
                answer = answer + "Based on your explanation, I understood that " + charge_1 + " and " + charge_2 + \
                    " are the two types of charges but using just that, I don't know how to determine the nature of the charges on the spheres that attract one another."
        elif required_concepts_dict[r_c[0][1]] == "Unknown":
            if required_concepts_dict[r_c[0][2]] == "Yes":
                k_c.append("opposite charges attract each other")
                answer = answer + "Based on your explanation, I understood that there are two types of charges and opposite charges attract each other."
                answer = answer + " So, the two metal spheres will have opposite charges on them. But can you specify what these opposite charges are?"
            elif required_concepts_dict[r_c[0][2]] == "No":
                follow_up_json = await read_explanation(
                    "Do opposite charges repel each other?", learner_explanation)
                if follow_up_json["verifications"][0]['verification_answer'] == "Yes":
                    k_c.append("opposite charges repel each other")
                    answer = answer + "Based on your explanation, I understood that there are two types of charges and opposite charges repel each other."
                    answer = answer + " So, the two metal spheres will not have opposite charges on them. But I do not know what the specific nature of the charges will be."
                elif follow_up_json["verifications"][0]['verification_answer'] == "No":
                    k_c.append(
                        "opposite charges neither attract nor repel each other")
                    answer = answer + "Based on your explanation, I understood that there are two types of charges and opposite charges neither attract nor repel each other."
                    answer = answer + " So, the spheres don't have opposite charges on them but I can't figure out the specific nature of the charges."
                else:
                    follow_up_json = await read_explanation(
                        "Do like charges attract each other?", learner_explanation)
                    if follow_up_json["verifications"][0]['verification_answer'] == "Yes":
                        k_c.append("like charges attract each other")
                        answer = answer + "Based on your explanation, I understood that there are the two types of charges and like charges attract each other."
                        answer = answer + " So, both the metal spheres have like charges."
                    else:
                        answer = answer + "Based on your explanation, I understood that there are two types of charges and opposite charges do not attract each other."
                        answer = answer + " So, the spheres don't have opposite charges on them but I can't figure out the specific nature of the charges."
            elif required_concepts_dict[r_c[0][2]] == "Unknown":
                answer = answer + "Based on your explanation, I understood that there are two types of charges but using just that, I don't know how to determine the nature of the charges on the sphere."
    elif required_concepts_dict[r_c[0][0]] == "No":
        follow_up_json = await read_explanation(
            "Is there less than two types of charges?", learner_explanation)
        if follow_up_json["verifications"][0]['verification_answer'] == "Yes" or follow_up_json["verifications"][0]['verification_answer'] == "Unknown":
            k_c.append("there is one type of charges")
            answer = answer + "Based on your explanation, I understood that there is only one type of charge. So both the spheres will have that charge on them."
        elif follow_up_json["verifications"][0]['verification_answer'] == "No":
            follow_up_answer = await answer_explanation("How many types of charges are there?", learner_explanation,
                                                        "Your response should be a json object 'number of types of charges' containing the number of types of charges")
            number_of_type_of_charges = follow_up_answer['number of types of charges']
            if not isinstance(number_of_type_of_charges, str):
                number_of_type_of_charges = str(number_of_type_of_charges)
            k_c.append("there are " + number_of_type_of_charges +
                       " types of charges")
            if required_concepts_dict[r_c[0][1]] == "Yes":
                k_c.append(
                    "positive and negative charges are two types of charges")
                if required_concepts_dict[r_c[0][2]] == "Yes":
                    k_c.append("opposite charges attract each other")
                    answer = answer + "Based on your explanation, I understood that there are " + \
                        number_of_type_of_charges + \
                        " types of charges and positive and negative charges attract each other."
                    answer = answer + " So, one metal sphere will have a postive charge and the other will have a negative charge."
                elif required_concepts_dict[r_c[0][2]] == "No":
                    follow_up_json = await read_explanation(
                        "Do opposite charges repel each other?", learner_explanation)
                    if follow_up_json["verifications"][0]['verification_answer'] == "Yes":
                        k_c.append("opposite charges repel each other")
                        answer = answer + "Based on your explanation, I understood that there are " + \
                            number_of_type_of_charges + \
                            " types of charges and positive and negative charges repel each other."
                        answer = answer + " So, the two metal spheres will not have opposite charges on them. But I do not know what the specific nature of the charges will be."
                    elif follow_up_json["verifications"][0]['verification_answer'] == "No":
                        k_c.append(
                            "opposite charges neither attract nor repel each other")
                        answer = answer + "Based on your explanation, I understood that there are " + number_of_type_of_charges + \
                            " types of charges and positive and negative charges neither attract nor repel each other."
                        answer = answer + " So, the spheres don't have opposite charges on them but I can't figure out the specific nature of the charges."
                    else:
                        follow_up_json = await read_explanation(
                            "Do like charges attract each other?", learner_explanation)
                        if follow_up_json["verifications"][0]['verification_answer'] == "Yes":
                            k_c.append("like charges attract each other")
                            answer = answer + "Based on your explanation, I understood that there are " + \
                                number_of_type_of_charges + " two types of charges and like charges attract each other."
                            answer = answer + " So, both the metal spheres have like charges on them."
                        else:
                            answer = answer + "Based on your explanation, I understood that there are " + number_of_type_of_charges + \
                                " types of charges and positive and negative charges do not attract each other."
                            answer = answer + " So, the spheres don't have opposite charges on them but I can't figure out the specific nature of the charges."
                elif required_concepts_dict[r_c[0][2]] == "Unknown":
                    follow_up_json = await read_explanation(
                        "Do any of the two charges attract each other?", learner_explanation)
                    if follow_up_json["verifications"][0]['verification_answer'] == "Yes":
                        follow_up_answer = await answer_explanation("Which two charges attract each other?", learner_explanation,
                                                                    "Your response should be a json object 'charges' containing an array of the charges that attract each other.")
                        charge_1 = follow_up_answer['charges'][0]
                        charge_2 = follow_up_answer['charges'][1]
                        k_c.append(charge_1 + " and " + charge_2 +
                                   " charges attract each other")
                        answer = answer + "Based on your explanation, I understood that " + \
                            charge_1 + " and " + charge_2 + " charges attract each other."
                        answer = answer + " So, one metal sphere will have a " + charge_1 + \
                            " charge and the other will have a " + charge_2 + " charge."
                    elif follow_up_json["verifications"][0]['verification_answer'] == "No":
                        answer = answer + "Based on your explanation, I understood that there are " + number_of_type_of_charges + \
                            " and none of them attract each other. So, I don't know how to figure out the nature of the charges on the sphere."
                    else:
                        answer = answer + "Based on your explanation, I understood that there are " + number_of_type_of_charges + \
                            " but using just that, I don't know how to determine the nature of the charges on the sphere."
            elif required_concepts_dict[r_c[0][1]] == "No" or required_concepts_dict[r_c[0][1]] == "Unknown":
                if required_concepts_dict[r_c[0][2]] == "Yes":
                    k_c.append("opposite charges attract each other")
                    answer = answer + "Based on your explanation, I understood that there are " + \
                        number_of_type_of_charges + " types of charges and opposite charges attract each other."
                    answer = answer + " So, the two metal spheres will have opposite charges on them."
                elif required_concepts_dict[r_c[0][2]] == "No":
                    follow_up_json = await read_explanation(
                        "Do opposite charges repel each other?", learner_explanation)
                    if follow_up_json["verifications"][0]['verification_answer'] == "Yes":
                        k_c.append("opposite charges repel each other")
                        answer = answer + "Based on your explanation, I understood that there are " + \
                            number_of_type_of_charges + " types of charges and opposite charges repel each other."
                        answer = answer + " So, the two metal spheres will not have opposite charges on them. But I do not know what the specific nature of the charges will be."
                    elif follow_up_json["verifications"][0]['verification_answer'] == "No":
                        k_c.append(
                            "opposite charges neither attract nor repel each other")
                        answer = answer + "Based on your explanation, I understood that there are " + number_of_type_of_charges + \
                            " types of charges and opposite charges neither attract nor repel each other."
                        answer = answer + " So, the spheres don't have opposite charges on them but I can't figure out the specific nature of the charges."
                    else:
                        follow_up_json = await read_explanation(
                            "Do like charges attract each other?", learner_explanation)
                        if follow_up_json["verifications"][0]['verification_answer'] == "Yes":
                            k_c.append("like charges attract each other")
                            answer = answer + "Based on your explanation, I understood that there are " + \
                                number_of_type_of_charges + " charges and like charges attract each other."
                            answer = answer + " So, both the metal spheres have a like charges on them."
                        else:
                            answer = answer + "Based on your explanation, I understood that there are " + \
                                number_of_type_of_charges + \
                                " types of charges and opposite charges do not attract each other."
                            answer = answer + " So, the spheres don't have opposite charges on them but I can't figure out the specific nature of the charges."
                elif required_concepts_dict[r_c[0][2]] == "Unknown":
                    follow_up_json = await read_explanation(
                        "Do any of the two charges attract each other?", learner_explanation)
                    if follow_up_json["verifications"][0]['verification_answer'] == "Yes":
                        follow_up_answer = await answer_explanation("Which two charges attract each other?", learner_explanation,
                                                                    "Your response should be a json object 'charges' containing an array of the charges that attract each other.")
                        charge_1 = follow_up_answer['charges'][0]
                        charge_2 = follow_up_answer['charges'][1]
                        k_c.append(charge_1 + " and " + charge_2 +
                                   " charges attract each other")
                        answer = answer + "Based on your explanation, I understood that " + \
                            charge_1 + " and " + charge_2 + " charges attract each other."
                        answer = answer + " So, one metal sphere will have a " + charge_1 + \
                            " charge and the other will have a " + charge_2 + " charge."
                    elif follow_up_json["verifications"][0]['verification_answer'] == "No":
                        answer = answer + "Based on your explanation, I understood that there are " + number_of_type_of_charges + \
                            " and none of them attract each other. So, I don't know how to figure out the nature of the charges on the sphere."
                    else:
                        answer = answer + "Based on your explanation, I understood that there are " + number_of_type_of_charges + \
                            " but using just that, I don't know how to determine the nature of the charges on the sphere."
    elif required_concepts_dict[r_c[0][0]] == "Unknown":
        if required_concepts_dict[r_c[0][1]] == "Yes":
            k_c.append("positive and negative charges are two types of charges")
            if required_concepts_dict[r_c[0][2]] == "Yes":
                k_c.append("opposite charges attract each other")
                answer = answer + "Based on your explanation, I understood that positive and negative charges attract each other."
                answer = answer + " So, one metal sphere will have a postive charge and the other will have a negative charge."
            elif required_concepts_dict[r_c[0][2]] == "No":
                follow_up_json = await read_explanation(
                    "Do opposite charges repel each other?", learner_explanation)
                if follow_up_json["verifications"][0]['verification_answer'] == "Yes":
                    k_c.append("opposite charges repel each other")
                    answer = answer + "Based on your explanation, I understood that positive and negative charges repel each other."
                    answer = answer + " So, the two metal spheres will not have opposite charges on them. But I do not know what the specific nature of the charges will be."
                elif follow_up_json["verifications"][0]['verification_answer'] == "No":
                    k_c.append(
                        "opposite charges neither attract nor repel each other")
                    answer = answer + "Based on your explanation, I understood that positive and negative charges neither attract nor repel each other."
                    answer = answer + " So, the spheres don't have opposite charges on them but I can't figure out the specific nature of the charges."
                else:
                    follow_up_json = await read_explanation(
                        "Do like charges attract each other?", learner_explanation)
                    if follow_up_json["verifications"][0]['verification_answer'] == "Yes":
                        k_c.append("like charges attract each other")
                        answer = answer + \
                            "Based on your explanation, I understood that like charges attract each other."
                        answer = answer + \
                            " So, both the metal spheres have a positive charge or both have a negative charge."
                    else:
                        answer = answer + "Based on your explanation, I understood that positive and negative charges do not attract each other."
                        answer = answer + " So, the spheres don't have opposite charges on them but I can't figure out the specific nature of the charges."
            elif required_concepts_dict[r_c[0][2]] == "Unknown":
                answer = answer + "I cannot figure out the nature of the charges on the sphere."
        elif required_concepts_dict[r_c[0][1]] == "No" or required_concepts_dict[r_c[0][1]] == "Unknown":
            if required_concepts_dict[r_c[0][2]] == "Yes":
                follow_up_json = await read_explanation(
                    "Do positive and negative charges attract each other?", learner_explanation)
                if follow_up_json["verifications"][0]['verification_answer'] == "Yes":
                    k_c.append(
                        "positive and negative charges attract each other")
                    answer = answer + "Based on your explanation, I understood that positive and negative charges attract each other."
                    answer = answer + " So, one metal sphere will have a positive charge and the other will have a negative charge."
                    correct = True
                else:
                    k_c.append("opposite charges attract each other")
                    answer = answer + \
                        "Based on your explanation, I understood that opposite charges attract each other."
                    answer = answer + " So, the two metal spheres will have opposite charges on them."
            elif required_concepts_dict[r_c[0][2]] == "No":
                follow_up_json = await read_explanation(
                    "Do opposite charges repel each other?", learner_explanation)
                if follow_up_json["verifications"][0]['verification_answer'] == "Yes":
                    k_c.append("opposite charges repel each other")
                    answer = answer + \
                        "Based on your explanation, I understood that opposite charges repel each other."
                    answer = answer + " So, the two metal spheres will not have opposite charges on them. But I do not know what the specific nature of the charges will be."
                elif follow_up_json["verifications"][0]['verification_answer'] == "No":
                    k_c.append(
                        "opposite charges neither attract nor repel each other")
                    answer = answer + "Based on your explanation, I understood that opposite charges neither attract nor repel each other."
                    answer = answer + " So, the spheres don't have opposite charges on them but I can't figure out the specific nature of the charges."
                else:
                    follow_up_json = await read_explanation(
                        "Do like charges attract each other?", learner_explanation)
                    if follow_up_json["verifications"][0]['verification_answer'] == "Yes":
                        k_c.append("like charges attract each other")
                        answer = answer + \
                            "Based on your explanation, I understood that like charges attract each other."
                        answer = answer + " So, both the metal spheres have like charges but I can't figure out the specific nature of the charges."
                    else:
                        answer = answer + "Based on your explanation, I understood that opposite charges do not attract each other."
                        answer = answer + " So, the spheres don't have opposite charges on them but I can't figure out the specific nature of the charges."
            elif required_concepts_dict[r_c[0][2]] == "Unknown":
                follow_up_json = await read_explanation(
                    "Do any of the two charges attract each other?", learner_explanation)
                if follow_up_json["verifications"][0]['verification_answer'] == "Yes":
                    follow_up_answer = await answer_explanation("Which two charges attract each other?", learner_explanation,
                                                                "Your response should be a json object 'charges' containing an array of the charges that attract each other.")
                    charge_1 = follow_up_answer['charges'][0]
                    charge_2 = follow_up_answer['charges'][1]
                    k_c.append(charge_1 + " and " + charge_2 +
                               " charges attract each other")
                    answer = answer + "Based on your explanation, I understood that " + \
                        charge_1 + " and " + charge_2 + " charges attract each other."
                    answer = answer + " So, one metal sphere will have a " + charge_1 + \
                        " charge and the other will have a " + charge_2 + " charge."
                else:
                    answer = answer + "Based on your explanation, I don't know how to determine the nature of the charges on the sphere."

    working, answer = await output_answer(q, answer)

    return {
        'status': 200,
        'body': {
            'isCorrect': correct,
            'working': working,
            'answer': answer
        }
    }
