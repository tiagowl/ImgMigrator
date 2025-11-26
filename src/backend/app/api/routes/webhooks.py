"""Webhook routes for QStash."""
import asyncio
import json
from fastapi import APIRouter, Request, HTTPException, status, Header, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.workers.tasks import process_migration_async
from app.services.qstash_service import get_qstash_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("/qstash")
async def qstash_webhook(
    request: Request,
    upstash_signature: str = Header(None, alias="Upstash-Signature"),
    db: Session = Depends(get_db),
):
    """
    Webhook endpoint for QStash to process migration tasks.
    
    This endpoint:
    1. Verifies the QStash signature
    2. Extracts migration_id and user_id from payload
    3. Processes the migration asynchronously
    """
    try:
        # Read request body
        body = await request.body()
        
        # Verify signature if provided
        if upstash_signature:
            try:
                qstash_service = get_qstash_service()
                if not qstash_service.verify_signature(body, upstash_signature):
                    logger.warning("Invalid QStash signature")
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid signature",
                    )
            except ValueError:
                # QStash not configured, skip verification in development
                logger.warning("QStash not configured, skipping signature verification")
        
        # Parse payload
        payload = json.loads(body.decode())
        
        migration_id = payload.get("migration_id")
        user_id = payload.get("user_id")
        
        if not migration_id or not user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing migration_id or user_id",
            )
        
        logger.info(f"Received QStash task for migration {migration_id}, user {user_id}")
        
        # Process migration asynchronously
        # Note: QStash espera uma resposta rápida, então processamos em background
        try:
            result = await process_migration_async(migration_id, user_id, db)
            logger.info(f"Migration {migration_id} processed successfully")
            return {
                "success": True,
                "migration_id": migration_id,
                "result": result,
            }
        except ValueError as e:
            # Validation errors
            logger.error(f"Validation error in migration {migration_id}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "migration_id": migration_id,
            }
        except Exception as e:
            # Other errors
            logger.exception(f"Error processing migration {migration_id}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "migration_id": migration_id,
            }
    
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid JSON payload",
        )
    except Exception as e:
        logger.exception(f"Error in QStash webhook: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal server error: {str(e)}",
            )

