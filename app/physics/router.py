from fastapi import APIRouter
from .ap_physics_c_em.router import router as ap_physics_c_em_router
from .ib_dp_physics.router import router as ib_dp_physics_router

router = APIRouter(
    prefix="/physics",
)

router.include_router(ap_physics_c_em_router)
router.include_router(ib_dp_physics_router)


@router.post("/")
async def physics():
    return {"Hello": "Physics"}
