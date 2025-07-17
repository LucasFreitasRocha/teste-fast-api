from fastapi import FastAPI
from src.config.init_config import init_config
from src.controller.base_controller import api_router
from src.config.inject_manager import register_manager_injector

register_manager_injector()
app = FastAPI(title="API", description="API for the application")
app.include_router(api_router)
init_config()
