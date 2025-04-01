from fastapi import APIRouter
from ....input_models import InputModel
from .learn_by_teaching.q1.reasoning_engine import compute_q1
from .learn_by_teaching.q2.reasoning_engine import compute_q2
from .learn_by_teaching.q3.reasoning_engine import compute_q3

router = APIRouter(
    prefix="/radioactive_decay"
)


@router.post("/1")
async def question1(
    data: InputModel
):
    return await compute_q1(data)


@router.post("/2")
async def question2(
    data: InputModel
):
    return await compute_q2(data)


@router.post("/3")
async def question3(
    data: InputModel
):
    return await compute_q3(data)
