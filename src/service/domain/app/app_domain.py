from typing import Optional, TYPE_CHECKING
from pydantic import BaseModel


class AppDomain(BaseModel):
    id: Optional[int]
    name: str
    description: str
    company: Optional["CompanyDomain"] = None

    @classmethod
    def build(
        cls,
        name: str,
        description: str,
        company: Optional["CompanyDomain"] = None,
        id: Optional[int] = None,
    ):
        return cls(name=name, description=description, company=company, id=id)


if TYPE_CHECKING:
    from src.service.domain.company.company_domain import CompanyDomain
