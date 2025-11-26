"""API dependencies."""
from typing import Generator
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.repositories.user_repository import UserRepository


def get_current_user(
    user_id: int = 1,  # Simplified for MVP - would use JWT in production
    db: Session = Depends(get_db),
) -> User:
    """
    Get current authenticated user.
    
    Note: This is simplified for MVP. In production, use JWT tokens.
    """
    repository = UserRepository(db)
    user = repository.find_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    return user



