from pydantic import BaseModel, UUID7
from src.service.domain.user.user_domain import UserDomain
from src.service.domain.app.app_domain import AppDomain
from typing import Optional

class UserAppDomain(BaseModel):
    id: Optional[UUID7]
    user: UserDomain
    app: AppDomain
    password: Optional[str] = None

    @classmethod
    def build(cls, user: UserDomain, app: AppDomain, password: Optional[str] = None, id: Optional[UUID7] = None):
        return cls(id=id, user=user, app=app, password=password)
