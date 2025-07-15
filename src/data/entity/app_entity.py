from sqlmodel import SQLModel, Field
from typing import Optional

from service.domain.app_domain import AppDomain

class AppEntity(SQLModel, table=True, table_name="apps"):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    description: str = Field(max_length=100)
    def __init__(self, name: str, description: str, id: Optional[int] = None):
        self.name = name
        self.description = description
        self.id = id
        
    def to_domain(self):
        return AppDomain(id=self.id, name=self.name, description=self.description)