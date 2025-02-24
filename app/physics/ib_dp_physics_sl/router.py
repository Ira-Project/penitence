from fastapi import APIRouter
from .work_energy_power.router import router as work_energy_power_router
from .radioactive_decay.router import router as radioactive_decay_router

router = APIRouter(
    prefix="/ib_physics_sl"
)

router.include_router(work_energy_power_router)
router.include_router(radioactive_decay_router)


@router.get("/")
async def physics():
    return {"Hello": "IB_Physics_SL"}
