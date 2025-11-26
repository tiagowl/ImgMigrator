"""Migration service."""
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.migration import Migration
from app.schemas.migration import MigrationCreate
from app.repositories.migration_repository import MigrationRepository
from app.workers.tasks import process_migration_task


class MigrationService:
    """Service for managing migrations."""
    
    def __init__(self, db: Session):
        """Initialize service with database session."""
        self.db = db
        self.repository = MigrationRepository(db)
    
    def create_migration(self, user_id: int, migration_data: MigrationCreate) -> Migration:
        """
        Create a new migration.
        
        Args:
            user_id: User ID
            migration_data: Migration data
            
        Returns:
            Created migration
            
        Raises:
            ValueError: If credentials are not configured
        """
        from app.services.credential_service import CredentialService
        
        # Verify credentials exist before creating migration
        credential_service = CredentialService(self.db)
        
        icloud_credential = credential_service.repository.find_by_user_and_service(user_id, "icloud")
        google_credential = credential_service.repository.find_by_user_and_service(user_id, "google_drive")
        
        if not icloud_credential or not icloud_credential.encrypted_credentials:
            raise ValueError("Credenciais do iCloud não encontradas. Configure suas credenciais primeiro.")
        
        if not google_credential or not google_credential.encrypted_credentials:
            raise ValueError("Credenciais do Google Drive não encontradas. Conecte sua conta Google primeiro.")
        
        migration = Migration(
            user_id=user_id,
            status="pending",
            total_photos=0,
            migrated_photos=0,
            failed_photos=0,
        )
        
        migration = self.repository.create(migration)
        
        # Queue background job
        process_migration_task.delay(migration.id, user_id)
        
        return migration
    
    def get_migration(self, migration_id: int, user_id: int) -> Optional[Migration]:
        """Get migration by ID."""
        migration = self.repository.find_by_id(migration_id)
        
        if migration and migration.user_id == user_id:
            return migration
        
        return None
    
    def get_user_migrations(
        self,
        user_id: int,
        status: Optional[str] = None,
        page: int = 1,
        limit: int = 20,
    ) -> tuple[list[Migration], int]:
        """Get user migrations with pagination."""
        return self.repository.find_by_user_id(user_id, status, page, limit)
    
    def get_migration_progress(self, migration_id: int, user_id: int) -> Optional[dict]:
        """Get migration progress."""
        migration = self.get_migration(migration_id, user_id)
        
        if not migration:
            return None
        
        # Calculate progress
        progress = 0.0
        if migration.total_photos > 0:
            progress = (migration.migrated_photos / migration.total_photos) * 100
        
        return {
            "migration_id": migration.id,
            "status": migration.status,
            "total_photos": migration.total_photos,
            "migrated_photos": migration.migrated_photos,
            "failed_photos": migration.failed_photos,
            "progress": progress,
            "current_photo": None,  # Would be set by worker
            "speed_mbps": None,  # Would be calculated by worker
            "estimated_time_remaining_minutes": None,  # Would be calculated
        }
    
    def pause_migration(self, migration_id: int, user_id: int) -> bool:
        """Pause a migration."""
        migration = self.get_migration(migration_id, user_id)
        
        if not migration or migration.status != "in_progress":
            return False
        
        migration.status = "paused"
        self.db.commit()
        return True
    
    def resume_migration(self, migration_id: int, user_id: int) -> bool:
        """Resume a paused migration."""
        migration = self.get_migration(migration_id, user_id)
        
        if not migration or migration.status != "paused":
            return False
        
        migration.status = "pending"
        self.db.commit()
        
        # Queue background job
        process_migration_task.delay(migration.id, user_id)
        
        return True
    
    def cancel_migration(self, migration_id: int, user_id: int) -> bool:
        """Cancel a migration."""
        migration = self.get_migration(migration_id, user_id)
        
        if not migration or migration.status in ("completed", "failed"):
            return False
        
        migration.status = "failed"
        migration.error_message = "Cancelled by user"
        migration.completed_at = datetime.utcnow()
        self.db.commit()
        
        return True


