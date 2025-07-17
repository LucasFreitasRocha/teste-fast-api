

import inject
from src.data.repository.company_repository import CompanyRepository
from src.service.domain.company_domain import CompanyDomain


class CompanyService:
    
    @inject.autoparams()
    def __init__(self, company_repository: CompanyRepository):
        self.company_repository = company_repository
        
    def create_company(self, company: CompanyDomain):
        
        return self.company_repository.create_company(company)
    
    
    def get_company_by_id(self, company_id: int):
        return self.company_repository.get_company_by_id(company_id)