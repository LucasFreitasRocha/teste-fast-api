from pydantic import BaseModel, field_validator
from uuid import UUID


class AppRequest(BaseModel):
    name: str
    description: str
    company_id: UUID

    @field_validator("company_id")
    @classmethod
    def validate_company_id(cls, v):
        if v is None:
            raise ValueError("company_id is required")
        if not isinstance(v, UUID):
            try:
                v = UUID(str(v))
            except Exception:
                raise ValueError("company_id must be a valid UUID")
        return v

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if not v or not str(v).strip():
            raise ValueError("name is required and cannot be empty")
        return str(v).strip()

    @field_validator("description")
    @classmethod
    def validate_description(cls, v):
        if not v or not str(v).strip():
            raise ValueError("description is required and cannot be empty")
        return str(v).strip()
