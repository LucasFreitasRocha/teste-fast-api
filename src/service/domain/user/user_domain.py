from pydantic import UUID7, BaseModel
from datetime import datetime
from typing import Optional


class UserDomain(BaseModel):
    id: Optional[UUID7]
    name: str
    email: str
    phone: str
    created_at: datetime
    updated_at: datetime
    @classmethod
    def build(
        cls,
        name: str,
        email: str,
        phone: str,
        id: Optional[UUID7] = None,
        created_at: Optional[datetime] = datetime.now(),
        updated_at: Optional[datetime] = datetime.now(),
    ):
        return UserDomain(
          id=id ,
          name=name,
          email=email,
          phone=phone,
          created_at=created_at,
          updated_at=updated_at)
