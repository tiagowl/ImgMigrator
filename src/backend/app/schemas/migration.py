"""Migration schemas."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class MigrationCreate(BaseModel):
    """Migration creation schema."""
    options: dict = {}


class MigrationResponse(BaseModel):
    """Migration response schema."""
    id: int
    status: str
    total_photos: int
    migrated_photos: int
    failed_photos: int
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        """Pydantic config."""
        from_attributes = True
    
    @property
    def progress(self) -> float:
        """Calculate progress percentage."""
        if self.total_photos == 0:
            return 0.0
        return (self.migrated_photos / self.total_photos) * 100
    
    @property
    def duration_minutes(self) -> Optional[float]:
        """Calculate duration in minutes."""
        if self.started_at and self.completed_at:
            delta = self.completed_at - self.started_at
            return delta.total_seconds() / 60
        return None


class MigrationList(BaseModel):
    """Migration list response schema."""
    migrations: list[MigrationResponse]
    total: int
    page: int
    limit: int


class MigrationProgress(BaseModel):
    """Migration progress schema."""
    migration_id: int
    status: str
    total_photos: int
    migrated_photos: int
    failed_photos: int
    progress: float
    current_photo: Optional[str] = None
    speed_mbps: Optional[float] = None
    estimated_time_remaining_minutes: Optional[float] = None

