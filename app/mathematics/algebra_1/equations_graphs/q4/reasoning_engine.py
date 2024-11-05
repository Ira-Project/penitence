from ..utils import *
from ..parameters import *
from .....input_models import InputModel
from .question import question_json


async def compute_q4(input: InputModel):

    correct = False
    working = ""
    answer = "Could not compute"
    concepts = []
    iras_answer = "Could not compute"

    return {
        'status': 200,
        'body': {
            'isCorrect': correct,
            'working': answer,
            'answer': iras_answer,
            'concepts': concepts
        }
    }
