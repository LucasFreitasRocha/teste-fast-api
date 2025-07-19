from pydantic import BaseModel, field_validator
from validate_docbr import CNPJ

class CompanyRequest(BaseModel):
    name: str
    description: str
    document: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if v is None or len(v) == 0:
            raise ValueError("name is required")
        return v
    
    @field_validator("description")
    @classmethod
    def validate_description(cls, v):
        if v is None or len(v) == 0:
            raise ValueError("description is required")
        return v
    
    @field_validator("document")
    @classmethod
    def validate_document(cls, v):
        if v is None:
            raise ValueError("document is required")
        if not CNPJ().validate(v):
            raise ValueError("document is not a valid CNPJ")
        return v
    