from datetime import datetime
from typing import Optional, List, TYPE_CHECKING


class CompanyDomain:
    id: Optional[int]
    name: str
    description: str
    document: str
    created_at: datetime
    updated_at: datetime
    apps: List["AppDomain"]

    def __init__(
        self,
        name: str,
        description: str,
        document: str,
        created_at: datetime,
        updated_at: datetime,
        apps: List["AppDomain"],
        id: Optional[int] = None,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.document = document
        self.created_at = created_at
        self.updated_at = updated_at
        self.apps = apps

    @classmethod
    def build(
        cls,
        name: str,
        description: str,
        document: str,
        apps: List["AppDomain"],
        id: Optional[int] = None,
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
    from src.service.domain.app_domain import AppDomain
