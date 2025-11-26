"""Celery background tasks."""
import asyncio
from datetime import datetime
from typing import Optional
from app.workers.celery_app import celery_app
from app.database import SessionLocal
from app.models.migration import Migration
from app.repositories.migration_repository import MigrationRepository
from app.services.icloud_service import ICloudService
from app.services.google_drive_service import GoogleDriveService
from app.services.credential_service import CredentialService
import logging

logger = logging.getLogger(__name__)


async def process_migration_async(migration_id: int, user_id: int, db):
    """
    Async function to process migration.
    
    This function:
    1. Gets credentials from both services
    2. Lists photos from iCloud
    3. Downloads each photo
    4. Uploads to Google Drive
    5. Updates progress
    """
    repository = MigrationRepository(db)
    migration = repository.find_by_id(migration_id)
    
    if not migration:
        raise ValueError("Migration not found")
    
    # Verify credentials exist
    credential_service = CredentialService(db)
    icloud_credential = credential_service.repository.find_by_user_and_service(user_id, "icloud")
    google_credential = credential_service.repository.find_by_user_and_service(user_id, "google_drive")
    
    if not icloud_credential or not icloud_credential.encrypted_credentials:
        raise ValueError("Credenciais do iCloud não encontradas. Configure suas credenciais primeiro.")
    
    if not google_credential or not google_credential.encrypted_credentials:
        raise ValueError("Credenciais do Google Drive não encontradas. Conecte sua conta Google primeiro.")
    
    # Initialize services
    icloud_service = ICloudService(db, user_id)
    drive_service = GoogleDriveService(db, user_id)
    
    # Verify connections
    logger.info(f"Verifying iCloud credentials for migration {migration_id}")
    icloud_valid = await icloud_service.verify_credentials()
    if not icloud_valid:
        raise ValueError("Credenciais do iCloud inválidas. Verifique suas credenciais.")
    
    logger.info(f"Verifying Google Drive connection for migration {migration_id}")
    google_valid = await drive_service.verify_connection()
    if not google_valid:
        raise ValueError("Conexão com Google Drive inválida. Reconecte sua conta Google.")
    
    # Get total photos count
    logger.info(f"Getting total photos count for migration {migration_id}")
    total_photos = await icloud_service.get_total_photos_count()
    
    if total_photos == 0:
        # If count is 0, try to list photos to get count
        try:
            photos = await icloud_service.list_photos(limit=1000)
            total_photos = len(photos)
        except Exception as e:
            logger.warning(f"Could not get photos count: {str(e)}. Will try to process in batches.")
            # Will process in batches and update total as we go
            total_photos = 0
    
    migration.total_photos = total_photos if total_photos > 0 else 1  # At least 1 to avoid division by zero
    db.commit()
    
    logger.info(f"Starting migration {migration_id}: {total_photos if total_photos > 0 else 'unknown'} photos to migrate")
    
    # Create folder in Google Drive for this migration
    folder_name = f"iCloud Migration {migration.created_at.strftime('%Y-%m-%d %H:%M')}"
    try:
        folder = await drive_service.create_folder(folder_name)
        folder_id = folder.get("id")
        logger.info(f"Created folder in Google Drive: {folder_id}")
    except Exception as e:
        logger.warning(f"Could not create folder, uploading to root: {str(e)}")
        folder_id = None
    
    # Process photos in batches
    batch_size = 50
    migrated_count = 0
    failed_count = 0
    offset = 0
    photo_index = 0
    
    while True:
        # Check if migration was paused or cancelled
        db.refresh(migration)
        if migration.status == "paused":
            logger.info(f"Migration {migration_id} paused at {migrated_count} photos")
            return {"status": "paused", "progress": migrated_count / migration.total_photos if migration.total_photos > 0 else 0}
        
        if migration.status == "failed":
            logger.info(f"Migration {migration_id} cancelled")
            return {"status": "cancelled"}
        
        # Get batch of photos
        try:
            photos = await icloud_service.list_photos(limit=batch_size, offset=offset)
        except Exception as e:
            logger.error(f"Error listing photos: {str(e)}")
            # If we can't list photos, break the loop
            break
        
        if not photos:
            # No more photos
            break
        
        # Update total if we didn't know it before
        if total_photos == 0 and len(photos) > 0:
            # Try to get a better estimate
            estimated_total = offset + len(photos) + (batch_size * 10)  # Rough estimate
            migration.total_photos = estimated_total
            total_photos = estimated_total
            db.commit()
        
        for photo in photos:
            photo_index += 1
            
            # Check if migration was paused or cancelled (inside loop)
            db.refresh(migration)
            if migration.status == "paused":
                logger.info(f"Migration {migration_id} paused at photo {photo_index}")
                return {"status": "paused", "progress": migrated_count / migration.total_photos if migration.total_photos > 0 else 0}
            
            if migration.status == "failed":
                logger.info(f"Migration {migration_id} cancelled")
                return {"status": "cancelled"}
            
            try:
                # Get photo metadata
                photo_id = photo.get("id") or str(photo_index)
                photo_metadata = await icloud_service.get_photo_metadata(photo_id)
                filename = photo_metadata.get("filename") or photo.get("filename") or f"photo_{photo_index}.jpg"
                
                # Download photo from iCloud
                logger.info(f"Downloading photo {photo_index}/{migration.total_photos if migration.total_photos > 0 else '?'}: {filename}")
                photo_data = await icloud_service.download_photo(photo_id)
                
                # Determine MIME type
                mime_type = photo_metadata.get("mime_type") or photo.get("mime_type") or "image/jpeg"
                if not filename.endswith(('.jpg', '.jpeg', '.png', '.heic', '.mov', '.mp4')):
                    # Try to determine from extension
                    ext = filename.split('.')[-1].lower() if '.' in filename else 'jpg'
                    mime_types = {
                        'jpg': 'image/jpeg',
                        'jpeg': 'image/jpeg',
                        'png': 'image/png',
                        'heic': 'image/heic',
                        'mov': 'video/quicktime',
                        'mp4': 'video/mp4',
                    }
                    mime_type = mime_types.get(ext, 'image/jpeg')
                
                # Upload to Google Drive
                logger.info(f"Uploading photo {photo_index} to Google Drive")
                result = await drive_service.upload_file(
                    file_data=photo_data,
                    filename=filename,
                    folder_id=folder_id,
                    mime_type=mime_type,
                )
                
                migrated_count += 1
                migration.migrated_photos = migrated_count
                
                logger.info(f"Successfully migrated photo {photo_index}: {result.get('id')}")
                
            except Exception as e:
                failed_count += 1
                migration.failed_photos = failed_count
                logger.error(f"Failed to migrate photo {photo_index}: {str(e)}")
                # Continue with next photo instead of failing entire migration
            
            # Update progress every 10 photos or at the end
            if (migrated_count + failed_count) % 10 == 0:
                db.commit()
                logger.info(f"Progress: {migrated_count}/{migration.total_photos if migration.total_photos > 0 else '?'} migrated, {failed_count} failed")
        
        offset += len(photos)
        
        # If we got fewer photos than batch size, we're done
        if len(photos) < batch_size:
            break
    
    # Update final total if we discovered it during processing
    if migration.total_photos == 1 and total_photos == 0:
        migration.total_photos = migrated_count + failed_count
    
    # Update final total if we discovered it during processing
    if migration.total_photos == 1 and total_photos == 0:
        migration.total_photos = migrated_count + failed_count
    
    # Complete migration
    migration.status = "completed"
    migration.completed_at = datetime.utcnow()
    db.commit()
    
    logger.info(f"Migration {migration_id} completed: {migrated_count} migrated, {failed_count} failed")
    
    return {
        "status": "completed",
        "migration_id": migration_id,
        "total_photos": migration.total_photos,
        "migrated_photos": migrated_count,
        "failed_photos": failed_count,
    }


@celery_app.task(bind=True, max_retries=3)
def process_migration_task(self, migration_id: int, user_id: int):
    """
    Process a migration in the background.
    
    This task:
    1. Verifies credentials for both iCloud and Google Drive
    2. Lists photos from iCloud
    3. Downloads each photo
    4. Uploads to Google Drive
    5. Updates progress in real-time
    6. Handles errors and retries
    """
    db = SessionLocal()
    migration = None
    
    try:
        repository = MigrationRepository(db)
        migration = repository.find_by_id(migration_id)
        
        if not migration:
            logger.error(f"Migration {migration_id} not found")
            return {"error": "Migration not found"}
        
        # Update status to in_progress
        migration.status = "in_progress"
        migration.started_at = datetime.utcnow()
        db.commit()
        
        # Run async migration process
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                process_migration_async(migration_id, user_id, db)
            )
            return result
        finally:
            loop.close()
    
    except ValueError as e:
        # Validation errors - don't retry
        logger.error(f"Validation error in migration {migration_id}: {str(e)}")
        if migration:
            migration.status = "failed"
            migration.error_message = str(e)
            migration.completed_at = datetime.utcnow()
            db.commit()
        return {"error": str(e)}
    
    except Exception as exc:
        # Other errors - retry with exponential backoff
        logger.exception(f"Error processing migration {migration_id}: {str(exc)}")
        
        if migration:
            # Only mark as failed if we've exhausted retries
            if self.request.retries >= self.max_retries:
                migration.status = "failed"
                migration.error_message = f"Erro após {self.max_retries} tentativas: {str(exc)}"
                migration.completed_at = datetime.utcnow()
                db.commit()
        
        # Retry with exponential backoff
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)
    
    finally:
        db.close()
