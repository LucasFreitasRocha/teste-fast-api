from fastapi import FastAPI
from src.config.init_config import init_config
from src.controller.base_controller import api_router
from src.config.inject_manager import register_manager_injector
from src.service.domain.company.company_domain import CompanyDomain
from src.service.domain.app.app_domain import AppDomain

register_manager_injector()
app = FastAPI(title="API", description="API for the application")
app.include_router(api_router)
init_config()


AppDomain.model_rebuild()
CompanyDomain.model_rebuild()
