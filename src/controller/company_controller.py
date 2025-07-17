from typing import Optional
from fastapi import APIRouter
import inject
from pydantic import BaseModel
from src.service.company_service import CompanyService
from src.service.domain.company.company_domain import CompanyDomain
from src.service.domain.company.company_request_domain import CompanyRequest





class CompanyResponse(BaseModel):
    id: int
    name: str
    description: str
    document: str


router = APIRouter()


@router.post("")
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
    
