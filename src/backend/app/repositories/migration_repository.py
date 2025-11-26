"""Migration repository."""
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.migration import Migration


class MigrationRepository:
    """Repository for migration data access."""
    
    def __init__(self, db: Session):
        """Initialize repository with database session."""
        self.db = db
    
    def find_by_id(self, migration_id: int) -> Optional[Migration]:
        """Find migration by ID."""
        return self.db.query(Migration).filter(Migration.id == migration_id).first()
    
    def find_by_user_id(
        self,
        user_id: int,
        status: Optional[str] = None,
        page: int = 1,
        limit: int = 20,
    ) -> tuple[list[Migration], int]:
        """Find migrations for a user with pagination."""
        query = self.db.query(Migration).filter(Migration.user_id == user_id)
        
        if status:
            query = query.filter(Migration.status == status)
        
        total = query.count()
        
        migrations = (
            query.order_by(Migration.created_at.desc())
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )
        
        return migrations, total
    
    def create(self, migration: Migration) -> Migration:
        """Create a new migration."""
        self.db.add(migration)
        self.db.commit()
        self.db.refresh(migration)
        return migration
    
    def update(self, migration: Migration) -> Migration:
        """Update migration."""
        self.db.commit()
        self.db.refresh(migration)
        return migration






