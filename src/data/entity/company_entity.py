from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from pydantic import UUID7
from uuid6 import uuid7


from src.data.entity.app_entity import AppEntity
from src.service.domain.company.company_domain import CompanyDomain


class CompanyEntity(SQLModel, table=True):
    __tablename__: str = "companies"
    id: Optional[UUID7] = Field(default_factory=uuid7, primary_key=True)
    name: str = Field(max_length=100)
    description: str = Field(max_length=100)
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())
    document: str = Field(max_length=100, unique=True)
    apps: List["AppEntity"] = Relationship(back_populates="company")

    def __init__(
        self,
        name: str,
        description: str,
        document: str,
        apps: List["AppEntity"],
        id: Optional[UUID7] = None,
    ):
        self.name = name
        self.description = description
        self.document = document
        self.id = id if id is not None else uuid7()
        self.apps = apps
        date = datetime.now()
        self.created_at = date
        self.updated_at = date

    def to_domain(self, include_apps=True):
        return CompanyDomain(
            id=self.id if self.id else None,
            name=self.name,
            description=self.description,
            document=self.document,
            created_at=self.created_at,
            updated_at=self.updated_at,
            apps=(
                [app.to_domain(include_company=False) for app in self.apps]
                if include_apps
                else []
            ),
        )
