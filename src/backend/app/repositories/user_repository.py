"""User repository."""
from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User


class UserRepository:
    """Repository for user data access."""
    
    def __init__(self, db: Session):
        """Initialize repository with database session."""
        self.db = db
    
    def find_by_id(self, user_id: int) -> Optional[User]:
        """Find user by ID."""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def find_by_email(self, email: str) -> Optional[User]:
        """Find user by email."""
        return self.db.query(User).filter(User.email == email).first()
    
    def create(self, user: User) -> User:
        """Create a new user."""
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def update(self, user: User) -> User:
        """Update user."""
        self.db.commit()
        self.db.refresh(user)
        return user






