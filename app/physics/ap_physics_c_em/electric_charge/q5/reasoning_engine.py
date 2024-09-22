from ..utils import *
from ..parameters import *
from .....input_models import InputModel
from .question import question_json


async def compute_q5(input: InputModel):

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

    print("DICT: ", tagged_concepts_dict)

    if not tagged_concepts_dict or not learner_explanation:
        return {
            'status': 500,
            'body': 'Please send a valid explanation'
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
        k_c.append("charges are conserved")
        if required_concepts_dict[r_c[0][1]] == "Yes":
            k_c.append("positive charges repel each other")
            if required_concepts_dict[r_c[0][2]] == "Yes":
                k_c.append(
                    "conductors allow charges to flow freely within them")
                answer = answer + "The positive charges will repel each other and move away towards the metal ruler, which will have a positive charge."
                correct = True
            elif required_concepts_dict[r_c[0][2]] == "No":
                k_c.append(
                    "conductors do not allow charges to flow freely within them")
                answer = answer + \
                    "The positive charges will repel each other and but won't be able to move away."
                answer = answer + " The metal ruler will remain neutral."
            elif required_concepts_dict[r_c[0][2]] == "Unknown":
                if not_required_concepts_dict[n_r_c[0]] == "Yes":
                    k_c.append(
                        "conduction is the transfer of charges by contact")
                    answer = answer + "I understand that conduction will happen and the positive charges will repel each other and move away towards the metal ruler. The ruler will have a positive charge. "
                    correct = True
                else:
                    answer = answer + "I understand that the positive charges will repel each other but I am not sure how they will move."
        elif required_concepts_dict[r_c[0][1]] == "No":
            follow_up_json = await read_explanation(
                "Do positive charges attract each other?", learner_explanation)
            if follow_up_json["verifications"][0]['verification_answer'] == "Yes":
                k_c.append("positive charges attract each other")
                if required_concepts_dict[r_c[0][2]] == "Yes":
                    k_c.append(
                        "conductors allow charges to flow freely within them")
                    answer = answer + "The positive charges will move towards each other and be concentrated in the center of the rod. The ruler will remain neutral."
                elif required_concepts_dict[r_c[0][2]] == "No":
                    k_c.append(
                        "conductors do not allow charges to flow freely within them")
                    answer = answer + "The positive charges will won't be able to move towards each other."
                    answer = answer + " The metal ruler will remain neutral."
                elif required_concepts_dict[r_c[0][2]] == "Unknown":
                    if not_required_concepts_dict[n_r_c[0]] == "Yes":
                        k_c.append(
                            "conduction is the transfer of charges by contact")
                        answer = answer + "I understand that conduction will happen and the positive charges will move towards each other and be concentrated in the center of the rod. The ruler will remain neutral."
                    else:
                        answer = answer + "I understand that the positive charges will attract each other but I am not sure how they will move."
            elif follow_up_json["verifications"][0]['verification_answer'] == "No":
                k_c.append(
                    "positive charges will neither attract nor repel each other")
                answer = answer + "The positive charges will neither attract nor repel each other. The metal ruler will remain neutral."
            elif follow_up_json["verifications"][0]['verification_answer'] == "No":
                k_c.append("positive charges will not attract each other")
                answer = answer + "The positive charges will not attract each other but based on that, I don't know how to figure out the charge on the metal ruler."
        elif required_concepts_dict[r_c[0][1]] == "Unknown":
            answer = answer + "I understand that the charges will be conserved but I don't know if the positive charges will move. So, I think metal ruler will remain neutral."
    elif required_concepts_dict[r_c[0][0]] == "No":
        k_c.append("charges are not conserved")
        answer = answer + "I understand that the charges can be created or be destroyed so, I don't know how to figure out the charges on the metal ruler."
    elif required_concepts_dict[r_c[0][0]] == "Unknown":
        answer = answer + "I am not sure if charges can be created or be destroyed so, I don't know how to figure out the charges on the metal ruler."

    iras_answer = await output_answer(q, answer)

    return {
        'status': 200,
        'body': {
            'isCorrect': correct,
            'working': answer,
            'answer': iras_answer,
            'concepts': concept_status
        }
    }
