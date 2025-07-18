import inject
from fastapi import APIRouter, status
from src.service.company_service import CompanyService
from src.service.domain.company.company_domain import CompanyDomain
from src.service.domain.company.company_request_domain import CompanyRequest


router = APIRouter()


@router.post("", response_model=CompanyDomain, status_code=status.HTTP_201_CREATED, response_model_exclude_none=True)
def create_company(company: CompanyRequest):
    company_service = inject.instance(CompanyService)
    return company_service.create_company(
        CompanyDomain.build(
            name=company.name,
            description=company.description,
            document=company.document,
            apps=[],
        )
    )
