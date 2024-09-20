from fastapi import APIRouter
from ....input_models import InputModel
from .q1.reasoning_engine import compute_q1
from .q2.reasoning_engine import compute_q2
from .q3.reasoning_engine import compute_q3
from .q4.reasoning_engine import compute_q4
from .q5.reasoning_engine import compute_q5

router = APIRouter(
    prefix="/work_energy_power"
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


@router.post("/4")
async def question4(
    data: InputModel
):
    return await compute_q4(data)


@router.post("/5")
async def question5(
    data: InputModel
):
    return await compute_q5(data)
