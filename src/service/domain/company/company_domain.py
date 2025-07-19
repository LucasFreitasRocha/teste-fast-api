from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from uuid import UUID

from pydantic import BaseModel


class CompanyDomain(BaseModel):
    id: Optional[UUID]
    name: str
    description: str
    document: str
    created_at: datetime
    updated_at: datetime
    apps: List["AppDomain"]

    @classmethod
    def build(
        cls,
        name: str,
        description: str,
        document: str,
        apps: List["AppDomain"],
        id: Optional[UUID] = None,
    ):
        return CompanyDomain(
            id=id,
            name=name,
            description=description,
            document=document,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            apps=apps,
        )


if TYPE_CHECKING:
    from src.service.domain.app.app_domain import AppDomain
