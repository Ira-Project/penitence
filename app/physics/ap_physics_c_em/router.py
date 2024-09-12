from fastapi import APIRouter
from .electric_charge.router import router as electric_charge_router

router = APIRouter(
    prefix="/ap_physics_c_em"
)

router.include_router(electric_charge_router)


@router.get("/")
async def physics():
    return {"Hello": "AP_Physics_C_EM"}
