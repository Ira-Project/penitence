from ..utils import *
from ..parameters import *
from .....input_models import InputModel
from .question import question_json
from .images import *


async def compute_q3(input: InputModel):

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

    answer1 = ""
    answer2 = ""
    correct1 = False
    correct2 = False
    imageOutput = ""
    q = question_json["Question"]
    r_c = question_json["required_concepts"]
    k_c = question_json["known_concepts"]
    n_r_c = question_json["not_required_concepts"]

    if required_concepts_dict[r_c[0][0]] == "Yes":
        k_c.append("charges are conserved")
        if required_concepts_dict[r_c[0][1]] == "Yes":
            k_c.append("insulators prevent charges from flowing freely")
            answer1 = answer1 + "Since charges can't be created or destroyed and they can't be transferred through air, the metal sphere will remain neutral."
            correct1 = True
        elif required_concepts_dict[r_c[0][1]] == "No":
            k_c.append("insulators allow charges to flow freely")
            answer1 = answer1 + "Since charges can't be created or destroyed but they can be transferred through air, the charges from the negative plate will flow through air and the metal sphere and cancel out the charges on the positive plate."
            imageOutput = image1
        elif required_concepts_dict[r_c[0][1]] == "Unknown":
            follow_up_json = await read_explanation(
                "Can charges be transferred through air?", learner_explanation)
            if follow_up_json["verifications"][0]['verification_answer'] == "No":
                k_c.append("charges can't flow through air")
                answer1 = answer1 + "Since charges can't be created or destroyed and they can't be transferred through air, the metal sphere will remain neutral."
                correct1 = True
            elif follow_up_json["verifications"][0]['verification_answer'] == "Yes":
                k_c.append("charges can flow through air")
                answer1 = answer1 + "Since charges can't be created or destroyed but they can be transferred through air, the charges from the negative plate will flow through air and the metal sphere and cancel out the charges on the positive plate."
                imageOutput = image1
            else:
                k_c.append("charges may flow through air")
                answer1 = answer1 + "Since charges can't be created or destroyed but they may be transferred through air, the charges from the negative plate may flow through air and the metal sphere and cancel out the charges on the positive plate."
                imageOutput = image1
    elif required_concepts_dict[r_c[0][0]] == "No":
        k_c.append("charges are not conserved")
        if required_concepts_dict[r_c[0][1]] == "Yes":
            k_c.append("insulators prevent charges from flowing freely")
            answer1 = answer1 + "I understand that charges can't be transferred through air but they can be created or destroyed."
            answer1 = answer1 + " So, I can't figure out the charge on the sphere."
        elif required_concepts_dict[r_c[0][1]] == "No":
            k_c.append("insulators allow charges to flow freely")
            answer1 = answer1 + "Since charges can be created, destroyed, and transferred through air, the charges from the negative plate may flow through air and the metal sphere and cancel out the charges on the positive plate."
            answer1 = answer1 + " New charges may also be created or old ones may be destroyed. So, I can't figure out the charge on the sphere."
        elif required_concepts_dict[r_c[0][1]] == "Unknown":
            answer1 = answer1 + " New charges may also be created or old ones may be destroyed. So, I can't figure out the charge on the sphere."
    elif required_concepts_dict[r_c[0][0]] == "Unknown":
        if required_concepts_dict[r_c[0][1]] == "Yes":
            k_c.append("insulators prevent charges from flowing freely")
            answer1 = answer1 + "I understand that charges can't be transferred through air but they may be created or destroyed."
            answer1 = answer1 + " So, I can't figure out the charge on the sphere."
        elif required_concepts_dict[r_c[0][1]] == "No":
            k_c.append("insulators allow charges to flow freely")
            answer1 = answer1 + "Since charges can be transferred through air, the charges from the negative plate may flow through air and the metal sphere and cancel out the charges on the positive plate."
            answer1 = answer1 + " But, new charges may also be created or old ones may be destroyed. So, I can't figure out the charge on the sphere."
        elif required_concepts_dict[r_c[0][1]] == "Unknown":
            answer1 = answer1 + " New charges may also be created or old ones may be destroyed. So, I can't figure out the charge on the sphere."
    # Second part
    if correct1:
        if required_concepts_dict[r_c[1][0]] == "Yes":
            k_c.append("positive and negative charges attract each other")
            if required_concepts_dict[r_c[1][1]] == "Yes":
                k_c.append("conductors allow free flow of charges within them")
                answer2 = answer2 + "The charges in the metal sphere will be attracted towards the oppositely charged metal plate."
                correct2 = True
                imageOutput = imageCorrect
            elif required_concepts_dict[r_c[1][1]] == "No":
                k_c.append(
                    "conductors prevent free flow of charges within them")
                answer2 = answer2 + "The charges in the metal sphere will be attracted towards the oppositely charged metal plate but won't be able to move through the conductor."
                imageOutput = image2
            elif required_concepts_dict[r_c[1][1]] == "Unknown":
                if not_required_concepts_dict[n_r_c[0]] == "Yes":
                    k_c.append(
                        "polarization is the separation of charges in a material")
                    answer2 = answer2 + "I understand that metal sphere might be polarized and the charges in the metal sphere will be attracted towards the oppositely charged metal plate."
                    correct2 = True
                    imageOutput = imageCorrect
                else:
                    answer2 = answer2 + "The charges in the metal sphere will be attracted towards the oppositely charged metal plate but I don't know if they will be able to move."
                    imageOutput = image2
        elif required_concepts_dict[r_c[1][0]] == "No":
            follow_up_json = await read_explanation(
                "Do positive and negative charges repel each other?", learner_explanation)
            if follow_up_json["verifications"][0]['verification_answer'] == "Yes":
                k_c.append("positive and negative charges repel each other")
                if required_concepts_dict[r_c[1][1]] == "Yes":
                    k_c.append(
                        "conductors allow free flow of charges within them")
                    answer2 = answer2 + \
                        "The charges in the metal sphere will be attracted towards the similarly charged metal plate."
                    imageOutput = image3
                elif required_concepts_dict[r_c[1][1]] == "No":
                    k_c.append(
                        "conductors prevent free flow of charges within them")
                    answer2 = answer2 + "The charges in the metal sphere will be attracted towards the similarly charged metal plate but won't be able to move through the conductor."
                    imageOutput = image2
                elif required_concepts_dict[r_c[1][1]] == "Unknown":
                    if not_required_concepts_dict[n_r_c[0]] == "Yes":
                        k_c.append(
                            "polarization is the separation of charges in a material")
                        answer2 = answer2 + "I understand that metal sphere might be polarized and the charges in the metal sphere will be attracted towards the similarly charged metal plate."
                        imageOutput = image3
                    else:
                        answer2 = answer2 + "The charges in the metal sphere will be attracted towards the similarly charged metal plate but I don't know if they will be able to move."
                        imageOutput = image2
            elif follow_up_json["verifications"][0]['verification_answer'] == "No":
                k_c.append(
                    "positive and negative charges do not attract or repel each other")
                answer2 = answer2 + \
                    "The charges in the metal sphere will neither be attracted nor be repelled."
                imageOutput = image2
            elif follow_up_json["verifications"][0]['verification_answer'] == "Unknown":
                k_c.append(
                    "positive and negative charges do not attract each other")
                answer2 = answer2 + \
                    "I understand that positive and negative charges do not attract each other."
                answer2 = answer2 + " But, I am not sure how to draw the charges on the sphere."
        elif required_concepts_dict[r_c[1][0]] == "Unknown":
            if not_required_concepts_dict[n_r_c[0]] == "Yes":
                k_c.append(
                    "polarization is the separation of charges in a material")
                answer2 = answer2 + \
                    "I understand that metal sphere might be polarized but I am not sure how."
            else:
                answer2 = answer2 + \
                    "Based on your explanation, I am not sure how to draw the charges on the sphere."

    answer = answer1 + "\n" + answer2
    correct = correct1 and correct2

    working, answer = await output_answer(q, answer)

    return {
        'status': 200,
        'body': {
            'isCorrect': correct,
            'working': working,
            'answer': answer,
            'image': imageOutput,
            'imageHeight': 150,
            'imageWidth': 150
        }
    }
