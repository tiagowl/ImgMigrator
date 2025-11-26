"""Credential repository."""
from typing import Optional
from sqlalchemy.orm import Session
from app.models.credential import Credential


class CredentialRepository:
    """Repository for credential data access."""
    
    def __init__(self, db: Session):
        """Initialize repository with database session."""
        self.db = db
    
    def find_by_id(self, credential_id: int) -> Optional[Credential]:
        """Find credential by ID."""
        return self.db.query(Credential).filter(Credential.id == credential_id).first()
    
    def find_by_user_id(self, user_id: int) -> list[Credential]:
        """Find all credentials for a user."""
        return self.db.query(Credential).filter(Credential.user_id == user_id).all()
    
    def find_by_user_and_service(
        self,
        user_id: int,
        service_type: str,
    ) -> Optional[Credential]:
        """Find credential by user and service type."""
        return (
            self.db.query(Credential)
            .filter(
                Credential.user_id == user_id,
                Credential.service_type == service_type,
            )
            .first()
        )
    
    def create(self, credential: Credential) -> Credential:
        """Create a new credential."""
        self.db.add(credential)
        self.db.commit()
        self.db.refresh(credential)
        return credential
    
    def delete(self, credential_id: int) -> bool:
        """Delete credential."""
        credential = self.find_by_id(credential_id)
        if credential:
            self.db.delete(credential)
            self.db.commit()
            return True
        return False



