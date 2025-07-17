import inject
from src.data.config.database import db
from src.data.repository.app_repository import AppRepository
from src.data.repository.company_repository import CompanyRepository
from src.service.app_service import AppService
from src.service.company_service import CompanyService

def inject_manager(binder: inject.Binder):
    
    company_repository = CompanyRepository(db.engine)
    company_service = CompanyService(company_repository)
    app_repository = AppRepository(db.engine)
    app_service = AppService(app_repository, company_service)
   
    
    binder.bind(AppRepository, app_repository)
    binder.bind(AppService, app_service)
    binder.bind(CompanyRepository, company_repository)
    binder.bind(CompanyService, company_service)


def register_manager_injector():
  inject.configure_once(inject_manager)

