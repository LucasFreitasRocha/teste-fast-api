from sqlmodel import SQLModel, Field, UniqueConstraint, Relationship
from pydantic import UUID7
from uuid6 import uuid7
from datetime import datetime
from src.service.domain.user_app.user_app_domain import UserAppDomain
from typing import Optional


class UserAppEntity(SQLModel, table=True):
    __tablename__: str = "user_apps"
    __table_args__ = (UniqueConstraint("user_id", "app_id", name="uq_user_app"),)

    id: UUID7 = Field(default_factory=uuid7, primary_key=True)
    user_id: UUID7 = Field(foreign_key="users.id")
    app_id: UUID7 = Field(foreign_key="apps.id")
    user: "UserEntity" = Relationship()
    app: "AppEntity" = Relationship()
    password: Optional[str] = Field(default=None, max_length=100, nullable=True)
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())

    def to_domain(self):
        return UserAppDomain(
            id=self.id,
            user=self.user.to_domain(),
            app=self.app.to_domain(),
            password=self.password,
        )
