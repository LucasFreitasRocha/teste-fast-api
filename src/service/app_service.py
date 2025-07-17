from src.data.repository.app_repository import AppRepository
from src.service.company_service import CompanyService
from src.service.domain.app_domain import AppDomain
from src.service.domain.company_domain import CompanyDomain


class AppService:
    def __init__(self, repository: AppRepository, company_service: CompanyService):
        self.repository = repository
        self.company_service = company_service

    def create_app(self, name: str, description: str, company: CompanyDomain):
        if company.id is None:
            raise ValueError("ID da empresa não pode ser None")
        company_obj = self.company_service.get_company_by_id(company.id)
        if company_obj is None:
            raise ValueError("Empresa não encontrada")
        app = AppDomain.build(name, description, company_obj)
        return self.repository.create_app(app)
