from fastapi import APIRouter
from API.controllers.dashboard_controller import router as dashboard_router

router = APIRouter(prefix="/api")
router.include_router(dashboard_router)