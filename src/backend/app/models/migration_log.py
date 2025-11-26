"""Migration log model."""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class MigrationLog(Base):
    """Migration log model."""
    
    __tablename__ = "migration_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    migration_id = Column(Integer, ForeignKey("migrations.id", ondelete="CASCADE"), nullable=False, index=True)
    photo_name = Column(String, nullable=False)
    photo_path = Column(String, nullable=True)
    status = Column(String, nullable=False, index=True)
    error_message = Column(String, nullable=True)
    file_size = Column(Integer, nullable=True)
    checksum = Column(String, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Relationships
    migration = relationship("Migration", back_populates="logs")
    
    # Constraints
    __table_args__ = (
        CheckConstraint(
            "status IN ('pending', 'downloading', 'uploading', 'completed', 'failed')",
            name="check_log_status"
        ),
        {"sqlite_autoincrement": True},
    )






