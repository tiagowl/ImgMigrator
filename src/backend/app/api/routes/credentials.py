"""Credential routes."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.api.dependencies import get_current_user
from app.schemas.credential import CredentialCreate, CredentialResponse, CredentialList
from app.services.credential_service import CredentialService

router = APIRouter(prefix="/credentials", tags=["credentials"])


@router.post("", response_model=CredentialResponse, status_code=status.HTTP_201_CREATED)
async def create_credential(
    credential_data: CredentialCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create or update credentials.
    
    For iCloud:
    - Requires apple_id (email) and password
    - Credentials are encrypted before storage
    
    For Google Drive:
    - Use OAuth flow instead of this endpoint
    """
    service = CredentialService(db)
    
    try:
        # Additional validation for iCloud
        if credential_data.service_type == "icloud":
            if not credential_data.apple_id or not credential_data.password:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Apple ID e senha são obrigatórios para iCloud",
                )
            
            # Basic email format validation (already done by Pydantic, but double-check)
            if "@" not in credential_data.apple_id or "." not in credential_data.apple_id.split("@")[1]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Apple ID deve ser um email válido",
                )
        
        credential = service.create_credential(current_user.id, credential_data)
        
        return CredentialResponse(
            id=credential.id,
            service_type=credential.service_type,
            status="configured",
            created_at=credential.created_at,
        )
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except ValueError as e:
        # Handle validation errors
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        # Handle other errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao salvar credenciais: {str(e)}",
        )


@router.get("", response_model=CredentialList)
async def list_credentials(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List all user credentials with status."""
    from datetime import datetime
    from app.services.google_drive_service import GoogleDriveService
    
    service = CredentialService(db)
    credentials = service.get_user_credentials(current_user.id)
    
    credential_responses = []
    for c in credentials:
        status_value = "not_configured"
        if c.encrypted_credentials:
            if c.service_type == "google_drive":
                # Check if token is expired
                is_expired = service.is_google_token_expired(current_user.id)
                if is_expired:
                    status_value = "expired"
                else:
                    # Verify connection
                    try:
                        drive_service = GoogleDriveService(db, current_user.id)
                        is_valid = await drive_service.verify_connection()
                        status_value = "connected" if is_valid else "error"
                    except Exception:
                        status_value = "error"
            else:
                status_value = "configured"
        
        credential_responses.append(
            CredentialResponse(
                id=c.id,
                service_type=c.service_type,
                status=status_value,
                created_at=c.created_at,
            )
        )
    
    return CredentialList(credentials=credential_responses)


@router.get("/google/verify", status_code=status.HTTP_200_OK)
async def verify_google_connection(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Verify Google Drive connection and return status."""
    from app.services.google_drive_service import GoogleDriveService
    
    service = CredentialService(db)
    
    # Check if credential exists
    credential = service.repository.find_by_user_and_service(current_user.id, "google_drive")
    if not credential or not credential.encrypted_credentials:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Google Drive credentials not found. Please connect your Google account first.",
        )
    
    # Check if expired
    is_expired = service.is_google_token_expired(current_user.id)
    if is_expired:
        return {
            "connected": False,
            "status": "expired",
            "message": "Token expired. Please reconnect your Google account.",
        }
    
    # Verify connection
    try:
        drive_service = GoogleDriveService(db, current_user.id)
        is_valid = await drive_service.verify_connection()
        
        if is_valid:
            # Get storage quota
            try:
                quota = await drive_service.get_storage_quota()
                return {
                    "connected": True,
                    "status": "connected",
                    "message": "Google Drive connection is active",
                    "storage_quota": quota.get("storageQuota", {}),
                }
            except Exception:
                return {
                    "connected": True,
                    "status": "connected",
                    "message": "Google Drive connection is active",
                }
        else:
            return {
                "connected": False,
                "status": "error",
                "message": "Unable to verify Google Drive connection",
            }
    except Exception as e:
        return {
            "connected": False,
            "status": "error",
            "message": f"Error verifying connection: {str(e)}",
        }


@router.delete("/{credential_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_credential(
    credential_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a credential."""
    service = CredentialService(db)
    
    success = service.delete_credential(credential_id, current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Credential not found",
        )
