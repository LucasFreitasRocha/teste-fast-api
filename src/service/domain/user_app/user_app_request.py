from pydantic import BaseModel, field_validator, EmailStr


class UserAppRequest(BaseModel):
    email: EmailStr
    name: str
    phone: str
    app_id: str
    password: str

    @field_validator("app_id")
    @classmethod
    def validate_app_id(cls, v):
        if not v:
            raise ValueError("App ID is required")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if not v:
            raise ValueError("Password is required")
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one number")
        return v
