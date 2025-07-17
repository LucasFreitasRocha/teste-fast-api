from fastapi import APIRouter

from src.controller import app_controller, company_controller


api_router = APIRouter()
api_router.include_router(company_controller.router, prefix="/company", tags=["company"])
api_router.include_router(app_controller.router, prefix="/app", tags=["app"])