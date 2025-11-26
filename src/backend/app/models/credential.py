"""Credential model."""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Credential(Base):
    """Credential model."""
    
    __tablename__ = "credentials"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    service_type = Column(String, nullable=False, index=True)
    encrypted_credentials = Column(String, nullable=False)
    salt = Column(String, nullable=False)
    nonce = Column(String, nullable=True)  # Para AES-GCM (OAuth tokens)
    expires_at = Column(DateTime(timezone=True), nullable=True)  # Para tokens OAuth
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="credentials")
    
    # Constraints
    __table_args__ = (
        CheckConstraint(
            "service_type IN ('icloud', 'google_drive')",
            name="check_service_type"
        ),
        {"sqlite_autoincrement": True},
    )

