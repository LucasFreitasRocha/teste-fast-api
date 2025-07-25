import inject
from src.data.config.database import db
from src.data.repository.app_repository import AppRepository
from src.data.repository.company_repository import CompanyRepository
from src.data.repository.user_repository import UserRepository
from src.data.repository.user_app_repository import UserAppRepository
from src.service.app_service import AppService
from src.service.auth_service import AuthService
from src.service.company_service import CompanyService
from src.service.user_app_service import UserAppService
from src.service.user_service import UserService

def inject_manager(binder: inject.Binder):
    
    company_repository = CompanyRepository(db.engine)
    company_service = CompanyService(company_repository)
    user_repository = UserRepository(db.engine)
    user_service = UserService(user_repository)
    app_repository = AppRepository(db.engine)
    app_service = AppService(app_repository, company_service)
    user_app_repository = UserAppRepository(db.engine)
    user_app_service = UserAppService(user_app_repository, user_service, app_service)
    auth_service = AuthService(user_app_service)
    
    binder.bind(AppRepository, app_repository)
    binder.bind(AppService, app_service)
    binder.bind(CompanyRepository, company_repository)
    binder.bind(CompanyService, company_service)
    binder.bind(UserRepository, user_repository)
    binder.bind(UserService, user_service)
    binder.bind(UserAppRepository, user_app_repository)
    binder.bind(UserAppService, user_app_service)
    binder.bind(AuthService, auth_service)

def register_manager_injector():
  inject.configure_once(inject_manager)

