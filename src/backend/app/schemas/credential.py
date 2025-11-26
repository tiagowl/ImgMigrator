"""Credential schemas."""
from datetime import datetime
from typing import Literal
from pydantic import BaseModel, EmailStr, model_validator


class CredentialCreate(BaseModel):
    """Credential creation schema."""
    service_type: Literal["icloud", "google_drive"]
    apple_id: EmailStr | None = None
    password: str | None = None
    
    @model_validator(mode='after')
    def validate_icloud_credentials(self):
        """Validate that iCloud credentials are provided when service_type is icloud."""
        if self.service_type == "icloud":
            if not self.apple_id:
                raise ValueError("apple_id é obrigatório para iCloud")
            if not self.password:
                raise ValueError("password é obrigatório para iCloud")
            if len(self.password.strip()) < 1:
                raise ValueError("password não pode estar vazio")
        return self


class CredentialResponse(BaseModel):
    """Credential response schema."""
    id: int
    service_type: str
    status: str = "configured"
    created_at: datetime
    
    class Config:
        """Pydantic config."""
        from_attributes = True


class CredentialList(BaseModel):
    """Credential list response schema."""
    credentials: list[CredentialResponse]


