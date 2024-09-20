from ..utils import *
from ..parameters import *
from .....input_models import InputModel
from .question import question_json
from .images import *


async def compute_q4(input: InputModel):

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
            correct1 = True
        elif required_concepts_dict[r_c[0][1]] == "No":
            k_c.append("insulators allow charges to flow freely")
            answer1 = answer1 + "Since charges can't be created or destroyed but they can be transferred through air or plastic, the charges will get neutralized with the environment or ground."
            imageOutput = image1
        elif required_concepts_dict[r_c[0][1]] == "Unknown":
            follow_up_json = await read_explanation("Can charges be transferred through air?" +
                                                    "\n" + "Can charges be transferred through plastic?", learner_explanation)
            if follow_up_json["verifications"][0]['verification_answer'] == "No" and follow_up_json["verifications"][1]['verification_answer'] == "No":
                k_c.append("charges can't flow through air or plastic")
                correct1 = True
            elif follow_up_json["verifications"][0]['verification_answer'] == "No" and follow_up_json["verifications"][1]['verification_answer'] == "Yes":
                k_c.append("charges can flow through plastic")
                answer1 = answer1 + "Since charges can't be created or destroyed but they can be transferred through plastic, the charges will get neutralized with the ground."
                imageOutput = image1
            elif follow_up_json["verifications"][0]['verification_answer'] == "No" and follow_up_json["verifications"][1]['verification_answer'] == "Unknown":
                k_c.append("charges may flow through plastic")
                answer1 = answer1 + "Since charges can't be created or destroyed but they may be transferred through plastic, the charges will get neutralized with the ground."
                imageOutput = image1
            elif follow_up_json["verifications"][0]['verification_answer'] == "Yes" and follow_up_json["verifications"][1]['verification_answer'] == "No":
                k_c.append("charges can flow through air")
                answer1 = answer1 + "Since charges can't be created or destroyed but they can be transferred through air, the charges will get neutralized with the environment."
                imageOutput = image1
            elif (follow_up_json["verifications"][0]['verification_answer'] == "Yes" or follow_up_json["verifications"][0]['verification_answer'] == "Unknown") and (follow_up_json["verifications"][1]['verification_answer'] == "Yes" or follow_up_json["verifications"][1]['verification_answer'] == "Unknown"):
                k_c.append("charges may flow through air or plastic")
                answer1 = answer1 + "Since charges can't be created or destroyed but they can be transferred through air or plastic, the charges will get neutralized."
                imageOutput = image1
            elif follow_up_json["verifications"][0]['verification_answer'] == "Unknown" and follow_up_json["verifications"][1]['verification_answer'] == "No":
                k_c.append("charges may flow through air")
                answer1 = answer1 + "Since charges can't be created or destroyed but they can be transferred through air, the charges will get neutralized with the environment."
                imageOutput = image1
    elif required_concepts_dict[r_c[0][0]] == "No":
        k_c.append("charges are not conserved")
        if required_concepts_dict[r_c[0][1]] == "Yes":
            k_c.append("insulators prevent charges from flowing freely")
            answer1 = answer1 + "I understand that charges can't be transferred through air or plastic but they can be created or destroyed."
            answer1 = answer1 + " So, I can't figure out how to draw that charges."
        elif required_concepts_dict[r_c[0][1]] == "No":
            k_c.append("insulators allow charges to flow freely")
            answer1 = answer1 + "Since charges can be created, destroyed, and transferred through air or plastic, the charges from the rod may flow in all directions."
            answer1 = answer1 + " New charges may also be created or old ones may be destroyed. So, I can't figure out how to draw that charges."
        elif required_concepts_dict[r_c[0][1]] == "Unknown":
            answer1 = answer1 + "New charges may also be created or old ones may be destroyed. So, I can't figure out how to draw that charges."
    elif required_concepts_dict[r_c[0][0]] == "Unknown":
        if required_concepts_dict[r_c[0][1]] == "Yes":
            k_c.append("insulators prevent charges from flowing freely")
            answer1 = answer1 + "I understand that charges can't be transferred through air or plastic but they may be created or destroyed."
            answer1 = answer1 + " So, I can't figure out the charge on the sphere."
        elif required_concepts_dict[r_c[0][1]] == "No":
            k_c.append("insulators allow charges to flow freely")
            answer1 = answer1 + "Since charges can be created, destroyed, and transferred through air or plastic, the charges from the rod may flow in all directions."
            answer1 = answer1 + " New charges may also be created or old ones may be destroyed. So, I can't figure out how to draw that charges."
        elif required_concepts_dict[r_c[0][1]] == "Unknown":
            answer1 = answer1 + "New charges may also be created or old ones may be destroyed. So, I can't figure out how to draw that charges."
    # Second part
    if correct1:
        if required_concepts_dict[r_c[1][0]] == "Yes":
            k_c.append("positive and negative charges attract each other")
            if required_concepts_dict[r_c[1][1]] == "Yes":
                k_c.append("conductors allow free flow of charges within them")
                if required_concepts_dict[r_c[1][2]] == "Yes":
                    k_c.append("grounding removes excess charges")
                    correct2 = True
                    imageOutput = imageCorrect
                elif required_concepts_dict[r_c[1][2]] == "No" or required_concepts_dict[r_c[1][2]] == "Unknown":
                    imageOutput = image2
            elif required_concepts_dict[r_c[1][1]] == "No":
                k_c.append(
                    "conductors prevent free flow of charges within them")
                answer2 = answer2 + "The charges will not be able to flow within the metal spheres."
                imageOutput = image3
            elif required_concepts_dict[r_c[1][1]] == "Unknown":
                if not_required_concepts_dict[n_r_c[0]] == "Yes":
                    k_c.append(
                        "polarization is the separation of charges in a material")
                    if required_concepts_dict[r_c[1][2]] == "Yes":
                        k_c.append("grounding removes excess charges")
                        correct2 = True
                        imageOutput = imageCorrect
                    elif required_concepts_dict[r_c[1][2]] == "No" or required_concepts_dict[r_c[1][2]] == "Unknown":
                        imageOutput = image2
                else:
                    answer2 = answer2 + "The charges in the metal sphere will be attracted towards the oppositel charges but I don't know if they will be able to move."
                    imageOutput = image3
        elif required_concepts_dict[r_c[1][0]] == "No":
            follow_up_json = await read_explanation(
                "Do positive and negative charges repel each other?", learner_explanation)
            if follow_up_json["verifications"][0]['verification_answer'] == "Yes":
                if required_concepts_dict[r_c[1][1]] == "Yes":
                    k_c.append(
                        "conductors allow free flow of charges within them")
                    if required_concepts_dict[r_c[1][2]] == "Yes":
                        k_c.append("grounding removes excess charges")
                        answer2 = answer2 + "I understood that opposite charges will repel each other."
                        imageOutput = image4
                    elif required_concepts_dict[r_c[1][2]] == "No" or required_concepts_dict[r_c[1][2]] == "Unknown":
                        imageOutput = image5
                elif required_concepts_dict[r_c[1][1]] == "No":
                    k_c.append(
                        "conductors prevent free flow of charges within them")
                    answer2 = answer2 + "The charges will not be able to flow within the metal spheres."
                    imageOutput = image3
                elif required_concepts_dict[r_c[1][1]] == "Unknown":
                    if not_required_concepts_dict[n_r_c[0]] == "Yes":
                        k_c.append(
                            "polarization is the separation of charges in a material")
                        if required_concepts_dict[r_c[1][2]] == "Yes":
                            k_c.append("grounding removes excess charges")
                            answer2 = answer2 + "I understood that opposite charges will repel each other."
                            imageOutput = image4
                        elif required_concepts_dict[r_c[1][2]] == "No" or required_concepts_dict[r_c[1][2]] == "Unknown":
                            imageOutput = image5
                    else:
                        answer2 = answer2 + "The charges in the metal sphere will repel from the opposite charge but I don't know if they will be able to move."
                        imageOutput = image3
            elif follow_up_json["verifications"][0]['verification_answer'] == "No":
                k_c.append(
                    "positive and negative charges do not attract or repel each other")
                answer2 = answer2 + \
                    "The charges in the metal sphere will neither be attracted nor be repelled."
                imageOutput = image3
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
            if not_required_concepts_dict[n_r_c[1]] == "Yes":
                answer2 = answer2 + " I understand that transfer of charges without contact is called induction but I don't know how it works."
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
            'concepts': concept_status
        }
    }
