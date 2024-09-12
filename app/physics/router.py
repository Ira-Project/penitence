from fastapi import APIRouter
from .ap_physics_c_em.router import router as ap_physics_c_em_router

router = APIRouter(
    prefix="/physics",
)

router.include_router(ap_physics_c_em_router)


@router.post("/")
async def physics():
    return {"Hello": "Physics"}
