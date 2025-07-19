from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from uuid6 import uuid7
from uuid import UUID

from src.service.domain.app.app_domain import AppDomain

if TYPE_CHECKING:
    from src.data.entity.company_entity import CompanyEntity


class AppEntity(SQLModel, table=True):
    __tablename__: str = "apps"

    id: Optional[UUID] = Field(default_factory=uuid7, primary_key=True)
    name: str = Field(max_length=100)
    description: str = Field(max_length=100)
    company_id: UUID = Field(foreign_key="companies.id")
    company: "CompanyEntity" = Relationship(back_populates="apps")

    def __init__(
        self, name: str, description: str, company_id: UUID, id: Optional[UUID] = None
    ):
        self.name = name
        self.description = description
        self.id = id if id is not None else uuid7()
        self.company_id = company_id

    def to_domain(self, include_company=True):
        return AppDomain(
            id=self.id,
            name=self.name,
            description=self.description,
            company=(
                self.company.to_domain(include_apps=False)
                if (self.company and include_company)
                else None
            ),
        )
