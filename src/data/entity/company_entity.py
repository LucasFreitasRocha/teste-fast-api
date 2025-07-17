from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

from src.data.entity.app_entity import AppEntity
from src.service.domain.company_domain import CompanyDomain


class CompanyEntity(SQLModel, table=True):
    __tablename__: str = "companies"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    description: str = Field(max_length=100)
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())
    document: str = Field(max_length=100)
    apps: List["AppEntity"] = Relationship(back_populates="company")

    def __init__(
        self,
        name: str,
        description: str,
        document: str,
        apps: List["AppEntity"],
        id: Optional[int] = None,
    ):
        self.name = name
        self.description = description
        self.document = document
        self.id = id
        self.apps = apps
        date = datetime.now()
        self.created_at = date
        self.updated_at = date

    def to_domain(self, include_apps=True):
        return CompanyDomain(
            id=self.id if self.id else 0,
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
