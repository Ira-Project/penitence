from fastapi import APIRouter
from .equations_graphs.router import router as equations_graphs_router

router = APIRouter(
    prefix="/algebra_1"
)

router.include_router(equations_graphs_router)


@router.get("/")
async def algebra():
    return {"Hello": "Algebra_1"}
