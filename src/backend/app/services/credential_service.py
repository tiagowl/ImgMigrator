"""Credential service."""
from typing import Optional
from sqlalchemy.orm import Session
from app.models.credential import Credential
from app.models.user import User
from app.schemas.credential import CredentialCreate
from app.services.encryption_service import EncryptionService
from app.repositories.credential_repository import CredentialRepository


class CredentialService:
    """Service for managing credentials."""
    
    def __init__(self, db: Session):
        """Initialize service with database session."""
        self.db = db
        self.repository = CredentialRepository(db)
    
    def create_credential(
        self,
        user_id: int,
        credential_data: CredentialCreate,
    ) -> Credential:
        """
        Create or update credential.
        
        Args:
            user_id: User ID
            credential_data: Credential data
            
        Returns:
            Created credential
        """
        # Encrypt credentials if provided
        encrypted_data = None
        salt = None
        nonce = None
        
        if credential_data.service_type == "icloud":
            if not credential_data.apple_id or not credential_data.password:
                raise ValueError("Apple ID e senha são obrigatórios para iCloud")
            
            # Validate email format
            if "@" not in credential_data.apple_id:
                raise ValueError("Apple ID deve ser um email válido")
            
            # Encrypt credentials
            credentials_str = f"{credential_data.apple_id}:{credential_data.password}"
            encrypted_data, salt, nonce = EncryptionService.encrypt(credentials_str)
        
        # Check if credential already exists
        existing = self.repository.find_by_user_and_service(user_id, credential_data.service_type)
        
        if existing:
            # Update existing
            if encrypted_data:
                existing.encrypted_credentials = encrypted_data
                existing.salt = salt
                existing.nonce = nonce
            self.db.commit()
            self.db.refresh(existing)
            return existing
        
        # Create new
        credential = Credential(
            user_id=user_id,
            service_type=credential_data.service_type,
            encrypted_credentials=encrypted_data or "",
            salt=salt or "",
            nonce=nonce or "",
        )
        
        return self.repository.create(credential)
    
    def create_google_oauth_credential(
        self,
        user_id: int,
        access_token: str,
        refresh_token: str = None,
        expires_in: int = None,
    ) -> Credential:
        """
        Create or update Google OAuth credential.
        
        Args:
            user_id: User ID
            access_token: OAuth access token
            refresh_token: OAuth refresh token
            expires_in: Token expiration time in seconds
            
        Returns:
            Created or updated credential
        """
        from datetime import datetime, timedelta
        
        # Encrypt OAuth tokens
        encrypted_data, salt, nonce = EncryptionService.encrypt_oauth_tokens(
            access_token,
            refresh_token,
        )
        
        # Calculate expiration time
        expires_at = None
        if expires_in:
            expires_at = datetime.utcnow() + timedelta(seconds=expires_in)
        
        # Check if credential already exists
        existing = self.repository.find_by_user_and_service(user_id, "google_drive")
        
        if existing:
            # Update existing
            existing.encrypted_credentials = encrypted_data
            existing.salt = salt
            existing.nonce = nonce
            existing.expires_at = expires_at
            self.db.commit()
            self.db.refresh(existing)
            return existing
        
        # Create new
        credential = Credential(
            user_id=user_id,
            service_type="google_drive",
            encrypted_credentials=encrypted_data,
            salt=salt,
            nonce=nonce,
            expires_at=expires_at,
        )
        
        return self.repository.create(credential)
    
    def get_google_oauth_tokens(self, user_id: int) -> Optional[dict]:
        """
        Get decrypted Google OAuth tokens for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            Dictionary with access_token and refresh_token, or None if not found
        """
        credential = self.repository.find_by_user_and_service(user_id, "google_drive")
        
        if not credential or not credential.encrypted_credentials:
            return None
        
        try:
            tokens = EncryptionService.decrypt_oauth_tokens(
                credential.encrypted_credentials,
                credential.salt,
                credential.nonce or "",
            )
            return tokens
        except Exception as e:
            # Log error but don't expose details
            return None
    
    def is_google_token_expired(self, user_id: int) -> bool:
        """
        Check if Google OAuth token is expired.
        
        Args:
            user_id: User ID
            
        Returns:
            True if expired or not found, False if still valid
        """
        credential = self.repository.find_by_user_and_service(user_id, "google_drive")
        
        if not credential or not credential.expires_at:
            return True
        
        from datetime import datetime
        return datetime.utcnow() >= credential.expires_at
    
    def get_user_credentials(self, user_id: int) -> list[Credential]:
        """Get all credentials for a user."""
        return self.repository.find_by_user_id(user_id)
    
    def delete_credential(self, credential_id: int, user_id: int) -> bool:
        """Delete credential."""
        credential = self.repository.find_by_id(credential_id)
        
        if not credential or credential.user_id != user_id:
            return False
        
        self.repository.delete(credential_id)
        return True
    
    def get_decrypted_credential(self, credential_id: int, user_id: int) -> Optional[dict]:
        """Get decrypted credential (for internal use only)."""
        credential = self.repository.find_by_id(credential_id)
        
        if not credential or credential.user_id != user_id:
            return None
        
        if credential.service_type == "icloud" and credential.encrypted_credentials:
            decrypted = EncryptionService.decrypt(
                credential.encrypted_credentials,
                credential.salt,
                credential.nonce or "",
            )
            parts = decrypted.split(":", 1)
            return {
                "apple_id": parts[0] if len(parts) > 0 else "",
                "password": parts[1] if len(parts) > 1 else "",
            }
        
        return None

