from typing import Optional, TYPE_CHECKING


class AppDomain:
    id: Optional[int]
    name: str
    description: str
    company: Optional["CompanyDomain"] = None

    def __init__(
        self,
        name: str,
        description: str,
        company: Optional["CompanyDomain"] = None,
        id: Optional[int] = None,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.company = company

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
    from src.service.domain.company_domain import CompanyDomain
