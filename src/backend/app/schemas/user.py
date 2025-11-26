"""User schemas."""
from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """User creation schema."""
    email: EmailStr


class UserResponse(BaseModel):
    """User response schema."""
    id: int
    email: str
    created_at: datetime
    
    class Config:
        """Pydantic config."""
        from_attributes = True






