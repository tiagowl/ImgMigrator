"""Google Drive service for file operations."""
from typing import Optional, BinaryIO
import json
import httpx
from app.services.auth_service import AuthService
from app.services.credential_service import CredentialService
from app.config import settings


class GoogleDriveService:
    """Service for Google Drive operations."""
    
    def __init__(self, db_session, user_id: int):
        """
        Initialize Google Drive service.
        
        Args:
            db_session: Database session
            user_id: User ID
        """
        self.db = db_session
        self.user_id = user_id
        self.credential_service = CredentialService(db_session)
        self._access_token: Optional[str] = None
    
    async def _get_access_token(self, force_refresh: bool = False) -> str:
        """
        Get valid access token, refreshing if necessary.
        
        Args:
            force_refresh: Force token refresh even if not expired
            
        Returns:
            Valid access token
        """
        # Check if token is expired
        is_expired = self.credential_service.is_google_token_expired(self.user_id)
        
        if force_refresh or is_expired:
            # Get refresh token
            tokens = self.credential_service.get_google_oauth_tokens(self.user_id)
            if not tokens or not tokens.get("refresh_token"):
                raise ValueError("Refresh token não disponível. Refaça a autenticação OAuth.")
            
            # Refresh token
            new_tokens = await AuthService.refresh_google_token(tokens["refresh_token"])
            
            # Update credentials with new tokens
            access_token = new_tokens.get("access_token")
            refresh_token = new_tokens.get("refresh_token", tokens.get("refresh_token"))
            expires_in = new_tokens.get("expires_in", 3600)
            
            self.credential_service.create_google_oauth_credential(
                user_id=self.user_id,
                access_token=access_token,
                refresh_token=refresh_token,
                expires_in=expires_in,
            )
            
            self._access_token = access_token
            return access_token
        
        # Use cached token or get from credentials
        if not self._access_token:
            tokens = self.credential_service.get_google_oauth_tokens(self.user_id)
            if not tokens:
                raise ValueError("Credenciais do Google Drive não encontradas. Refaça a autenticação OAuth.")
            self._access_token = tokens.get("access_token")
        
        return self._access_token
    
    async def upload_file(
        self,
        file_data: bytes,
        filename: str,
        folder_id: str = None,
        mime_type: str = "image/jpeg",
    ) -> dict:
        """
        Upload file to Google Drive.
        
        Args:
            file_data: File content as bytes
            filename: Name of the file
            folder_id: Optional folder ID to upload to
            mime_type: MIME type of the file
            
        Returns:
            Dictionary with file ID and other metadata
        """
        import json
        access_token = await self._get_access_token()
        
        # Prepare metadata
        metadata = {
            "name": filename,
            "mimeType": mime_type,
        }
        if folder_id:
            metadata["parents"] = [folder_id]
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            # Upload file using multipart upload
            # httpx supports multipart/form-data natively
            files = {
                "metadata": (None, json.dumps(metadata), "application/json"),
                "file": (filename, file_data, mime_type),
            }
            
            response = await client.post(
                "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
                headers={"Authorization": f"Bearer {access_token}"},
                files=files,
            )
            
            if response.status_code == 401:
                # Token expired, try refreshing
                access_token = await self._get_access_token(force_refresh=True)
                response = await client.post(
                    "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
                    headers={"Authorization": f"Bearer {access_token}"},
                    files=files,
                )
            
            response.raise_for_status()
            return response.json()
    
    async def create_folder(self, name: str, parent_id: str = None) -> dict:
        """
        Create folder in Google Drive.
        
        Args:
            name: Folder name
            parent_id: Optional parent folder ID
            
        Returns:
            Dictionary with folder ID and metadata
        """
        access_token = await self._get_access_token()
        
        metadata = {
            "name": name,
            "mimeType": "application/vnd.google-apps.folder",
        }
        if parent_id:
            metadata["parents"] = [parent_id]
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://www.googleapis.com/drive/v3/files",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json",
                },
                json=metadata,
            )
            
            if response.status_code == 401:
                access_token = await self._get_access_token(force_refresh=True)
                response = await client.post(
                    "https://www.googleapis.com/drive/v3/files",
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Content-Type": "application/json",
                    },
                    json=metadata,
                )
            
            response.raise_for_status()
            return response.json()
    
    async def get_storage_quota(self) -> dict:
        """
        Get Google Drive storage quota information.
        
        Returns:
            Dictionary with quota information
        """
        access_token = await self._get_access_token()
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://www.googleapis.com/drive/v3/about?fields=storageQuota",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            
            if response.status_code == 401:
                access_token = await self._get_access_token(force_refresh=True)
                response = await client.get(
                    "https://www.googleapis.com/drive/v3/about?fields=storageQuota",
                    headers={"Authorization": f"Bearer {access_token}"},
                )
            
            response.raise_for_status()
            return response.json()
    
    async def verify_connection(self) -> bool:
        """
        Verify that Google Drive connection is working.
        
        Returns:
            True if connection is valid, False otherwise
        """
        try:
            await self.get_storage_quota()
            return True
        except Exception:
            return False

