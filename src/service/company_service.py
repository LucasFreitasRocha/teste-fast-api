import inject
from fastapi import HTTPException, status
from src.data.repository.company_repository import CompanyRepository
from src.service.domain.company.company_domain import CompanyDomain
from uuid import UUID


class CompanyService:

    @inject.autoparams()
    def __init__(self, company_repository: CompanyRepository):
        self.company_repository = company_repository

    def create_company(self, company: CompanyDomain):

        return self.company_repository.create_company(company)

    def get_company_by_id(self, company_id: UUID):
        company = self.company_repository.get_company_by_id(company_id)
        if company is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company not found with this company_id: " + str(company_id),
            )
        return company
