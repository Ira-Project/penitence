from fastapi import APIRouter
from .read_and_relay.input_model import InputModel
from .read_and_relay.q1_reasoning_engine import compute_q1
from .read_and_relay.q2_reasoning_engine import compute_q2
from .read_and_relay.q3_reasoning_engine import compute_q3

router = APIRouter(
    prefix="/current_and_circuits"
)


@router.post("/read_and_relay/1")
async def question1(
    data: InputModel
):
    question = data.question
    selected_concepts = "\n".join(
        data.highlights) + "\n" + "\n".join(data.formulas)
    return await compute_q1(selected_concepts, question)


@router.post("/read_and_relay/2")
async def question2(
    data: InputModel
):
    question = data.question
    selected_concepts = "\n".join(
        data.highlights) + "\n" + "\n".join(data.formulas)
    return await compute_q2(selected_concepts, question)


@router.post("/read_and_relay/3")
async def question3(
    data: InputModel
):
    question = data.question
    selected_concepts = "\n".join(
        data.highlights) + "\n" + "\n".join(data.formulas)
    return await compute_q3(selected_concepts, question)
