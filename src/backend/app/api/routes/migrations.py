"""Migration routes."""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.api.dependencies import get_current_user
from app.schemas.migration import (
    MigrationCreate,
    MigrationResponse,
    MigrationList,
    MigrationProgress,
)
from app.services.migration_service import MigrationService

router = APIRouter(prefix="/migrations", tags=["migrations"])


@router.post("", response_model=MigrationResponse, status_code=status.HTTP_201_CREATED)
async def create_migration(
    migration_data: MigrationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create a new migration.
    
    This endpoint:
    1. Verifies that both iCloud and Google Drive credentials are configured
    2. Creates a migration record
    3. Queues the migration task in the background
    """
    service = MigrationService(db)
    
    try:
        migration = service.create_migration(current_user.id, migration_data)
        response = MigrationResponse(
            id=migration.id,
            status=migration.status,
            total_photos=migration.total_photos,
            migrated_photos=migration.migrated_photos,
            failed_photos=migration.failed_photos,
            started_at=migration.started_at,
            completed_at=migration.completed_at,
            created_at=migration.created_at,
        )
        return response
    except ValueError as e:
        # Validation errors (missing credentials)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar migração: {str(e)}",
        )


@router.get("", response_model=MigrationList)
async def list_migrations(
    status: Optional[str] = Query(None, description="Filter by status"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List user migrations."""
    service = MigrationService(db)
    migrations, total = service.get_user_migrations(
        current_user.id,
        status=status,
        page=page,
        limit=limit,
    )
    
    return MigrationList(
        migrations=[
            MigrationResponse(
                id=m.id,
                status=m.status,
                total_photos=m.total_photos,
                migrated_photos=m.migrated_photos,
                failed_photos=m.failed_photos,
                started_at=m.started_at,
                completed_at=m.completed_at,
                created_at=m.created_at,
            )
            for m in migrations
        ],
        total=total,
        page=page,
        limit=limit,
    )


@router.get("/{migration_id}", response_model=MigrationResponse)
async def get_migration(
    migration_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get migration details."""
    service = MigrationService(db)
    migration = service.get_migration(migration_id, current_user.id)
    
    if not migration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Migration not found",
        )
    
    return MigrationResponse(
        id=migration.id,
        status=migration.status,
        total_photos=migration.total_photos,
        migrated_photos=migration.migrated_photos,
        failed_photos=migration.failed_photos,
        started_at=migration.started_at,
        completed_at=migration.completed_at,
        created_at=migration.created_at,
    )


@router.get("/{migration_id}/progress", response_model=MigrationProgress)
async def get_migration_progress(
    migration_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get migration progress."""
    service = MigrationService(db)
    progress = service.get_migration_progress(migration_id, current_user.id)
    
    if not progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Migration not found",
        )
    
    return MigrationProgress(**progress)


@router.post("/{migration_id}/pause")
async def pause_migration(
    migration_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Pause a migration."""
    service = MigrationService(db)
    success = service.pause_migration(migration_id, current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot pause migration",
        )
    
    return {"success": True, "status": "paused"}


@router.post("/{migration_id}/resume")
async def resume_migration(
    migration_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Resume a paused migration."""
    service = MigrationService(db)
    success = service.resume_migration(migration_id, current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot resume migration",
        )
    
    return {"success": True, "status": "in_progress"}


@router.delete("/{migration_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_migration(
    migration_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Cancel a migration."""
    service = MigrationService(db)
    success = service.cancel_migration(migration_id, current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot cancel migration",
        )

