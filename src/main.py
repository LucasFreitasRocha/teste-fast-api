from dotenv import load_dotenv
import secrets

# Load environment variables FIRST, before any other imports that need them
load_dotenv()

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from src.config.init_config import init_config
from src.controller.base_controller import api_router
from src.config.inject_manager import register_manager_injector
from src.service.domain.company.company_domain import CompanyDomain
from src.service.domain.app.app_domain import AppDomain

register_manager_injector()
app = FastAPI(title="API", description="API for the application")

# Add SessionMiddleware for OAuth
app.add_middleware(
    SessionMiddleware,
    secret_key=secrets.token_urlsafe(32),
    session_cookie="oauth_session",
    max_age=3600,  # 1 hour
    same_site="lax",
    https_only=False,  # Set to True in production
)

app.include_router(api_router)
init_config()


AppDomain.model_rebuild()
CompanyDomain.model_rebuild()
