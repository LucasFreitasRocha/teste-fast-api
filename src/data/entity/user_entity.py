from pydantic import UUID7
from sqlmodel import SQLModel, Field
from uuid6 import uuid7
from datetime import datetime
from src.service.domain.user.user_domain import UserDomain


class UserEntity(SQLModel, table=True):
    __tablename__: str = "users"
    id: UUID7 = Field(default_factory=uuid7, primary_key=True)
    name: str = Field(max_length=100)
    email: str = Field(max_length=100, unique=True)
    phone: str = Field(max_length=20)
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())

    def to_domain(self) -> UserDomain:
        return UserDomain(
            id=self.id,
            name=self.name,
            email=self.email,
            phone=self.phone,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
