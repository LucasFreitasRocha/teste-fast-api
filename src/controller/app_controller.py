from fastapi import APIRouter
from pydantic import BaseModel
from src.service.app_service import AppService
import inject
from src.service.domain.company_domain import CompanyDomain
from typing import Optional


class AppRequest(BaseModel):
    name: str
    description: str
    company_id: int


class CompanyResponse(BaseModel):
    id: int
    name: str
    description: str
    # Adicione outros campos conforme necessário

    @classmethod
    def from_domain(cls, domain):
        return cls(
            id=domain.id,
            name=domain.name,
            description=domain.description,
            # Adicione outros campos conforme necessário
        )


class AppResponse(BaseModel):
    id: int
    name: str
    description: str
    company: Optional[CompanyResponse] = None

    class Config:
        arbitrary_types_allowed = True


router = APIRouter()


@router.post("")
def create_app(app: AppRequest):
    app_service = inject.instance(AppService)
    response = app_service.create_app(
        app.name,
        app.description,
        CompanyDomain.build(
            id=app.company_id, name="", description="", document="", apps=[]
        ),
    )
    return AppResponse(
        id=response.id if response.id else 0,
        name=response.name,
        description=response.description,
        company=(
            CompanyResponse.from_domain(response.company) if response.company else None
        ),
    )
