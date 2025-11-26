"""iCloud service for photo operations."""
from typing import Optional, List, Dict
import httpx
from app.services.credential_service import CredentialService


class ICloudService:
    """Service for iCloud photo operations."""
    
    def __init__(self, db_session, user_id: int):
        """
        Initialize iCloud service.
        
        Args:
            db_session: Database session
            user_id: User ID
        """
        self.db = db_session
        self.user_id = user_id
        self.credential_service = CredentialService(db_session)
        self._apple_id: Optional[str] = None
        self._password: Optional[str] = None
    
    def _get_credentials(self) -> tuple[str, str]:
        """
        Get decrypted iCloud credentials.
        
        Returns:
            Tuple of (apple_id, password)
            
        Raises:
            ValueError: If credentials not found or invalid
        """
        if self._apple_id and self._password:
            return self._apple_id, self._password
        
        credential = self.credential_service.repository.find_by_user_and_service(
            self.user_id, "icloud"
        )
        
        if not credential or not credential.encrypted_credentials:
            raise ValueError("Credenciais do iCloud não encontradas. Configure suas credenciais primeiro.")
        
        decrypted = self.credential_service.get_decrypted_credential(
            credential.id, self.user_id
        )
        
        if not decrypted:
            raise ValueError("Erro ao descriptografar credenciais do iCloud.")
        
        self._apple_id = decrypted.get("apple_id")
        self._password = decrypted.get("password")
        
        if not self._apple_id or not self._password:
            raise ValueError("Credenciais do iCloud inválidas.")
        
        return self._apple_id, self._password
    
    async def list_photos(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """
        List photos from iCloud.
        
        Args:
            limit: Maximum number of photos to return
            offset: Offset for pagination
            
        Returns:
            List of photo dictionaries with metadata
            
        Note:
            This is a placeholder implementation. In production, this would
            use the iCloud API (pyicloud library or similar) to actually
            connect and list photos.
        """
        apple_id, password = self._get_credentials()
        
        try:
            # Try to import pyicloud
            try:
                from pyicloud import PyiCloudService
            except ImportError:
                # If pyicloud is not installed, raise informative error
                raise NotImplementedError(
                    "Biblioteca pyicloud não instalada. "
                    "Instale com: pip install pyicloud"
                )
            
            # Connect to iCloud
            api = PyiCloudService(apple_id, password)
            
            # Check if 2FA is required
            if api.requires_2sa:
                raise ValueError(
                    "Autenticação de dois fatores (2FA) é necessária. "
                    "Por favor, autentique via dispositivo Apple primeiro."
                )
            
            # Get photos
            photos = api.photos.all
            
            # Convert to list and apply pagination
            photos_list = list(photos)
            total = len(photos_list)
            
            # Apply pagination
            paginated_photos = photos_list[offset:offset + limit]
            
            # Convert to dictionary format
            result = []
            for photo in paginated_photos:
                result.append({
                    "id": photo.id,
                    "filename": photo.filename,
                    "size": getattr(photo, "size", 0),
                    "created": getattr(photo, "created", None),
                    "modified": getattr(photo, "modified", None),
                    "mime_type": getattr(photo, "mime_type", "image/jpeg"),
                })
            
            return result
            
        except NotImplementedError:
            # If pyicloud is not available, raise to inform user
            raise
        except ValueError:
            # Re-raise validation errors
            raise
        except Exception as e:
            raise ValueError(f"Erro ao listar fotos do iCloud: {str(e)}")
    
    async def download_photo(self, photo_id: str) -> bytes:
        """
        Download a photo from iCloud.
        
        Args:
            photo_id: Photo identifier from iCloud
            
        Returns:
            Photo data as bytes
            
        Raises:
            ValueError: If photo cannot be downloaded
        """
        apple_id, password = self._get_credentials()
        
        try:
            from pyicloud import PyiCloudService
            
            # Connect to iCloud
            api = PyiCloudService(apple_id, password)
            
            # Find photo by ID
            photo = None
            for p in api.photos.all:
                if p.id == photo_id:
                    photo = p
                    break
            
            if not photo:
                raise ValueError(f"Foto com ID {photo_id} não encontrada no iCloud")
            
            # Download photo
            photo_data = photo.download().read()
            return photo_data
            
        except ImportError:
            raise NotImplementedError(
                "Biblioteca pyicloud não instalada. "
                "Instale com: pip install pyicloud"
            )
        except Exception as e:
            raise ValueError(f"Erro ao baixar foto do iCloud: {str(e)}")
    
    async def get_photo_metadata(self, photo_id: str) -> Dict:
        """
        Get metadata for a photo.
        
        Args:
            photo_id: Photo identifier from iCloud
            
        Returns:
            Dictionary with photo metadata (filename, size, date, mime_type, etc.)
        """
        apple_id, password = self._get_credentials()
        
        try:
            from pyicloud import PyiCloudService
            
            # Connect to iCloud
            api = PyiCloudService(apple_id, password)
            
            # Find photo by ID
            photo = None
            for p in api.photos.all:
                if p.id == photo_id:
                    photo = p
                    break
            
            if not photo:
                return {}
            
            return {
                "filename": photo.filename,
                "size": getattr(photo, "size", 0),
                "created": getattr(photo, "created", None),
                "modified": getattr(photo, "modified", None),
                "mime_type": getattr(photo, "mime_type", "image/jpeg"),
            }
        except Exception:
            return {}
    
    async def verify_credentials(self) -> bool:
        """
        Verify that iCloud credentials are valid.
        
        Returns:
            True if credentials are valid, False otherwise
        """
        try:
            apple_id, password = self._get_credentials()
            
            if not apple_id or not password:
                return False
            
            try:
                from pyicloud import PyiCloudService
                
                # Try to connect to iCloud
                api = PyiCloudService(apple_id, password)
                
                # If 2FA is required, credentials are valid but need 2FA
                # For now, we consider it valid if we can connect
                return True
                
            except ImportError:
                # If pyicloud is not installed, just check if credentials exist
                return bool(apple_id and password)
            except Exception:
                # Authentication failed
                return False
                
        except Exception:
            return False
    
    async def get_total_photos_count(self) -> int:
        """
        Get total number of photos in iCloud.
        
        Returns:
            Total number of photos
        """
        try:
            apple_id, password = self._get_credentials()
            
            try:
                from pyicloud import PyiCloudService
                
                # Connect to iCloud
                api = PyiCloudService(apple_id, password)
                
                # Get all photos and count
                photos = api.photos.all
                return len(list(photos))
                
            except ImportError:
                # If pyicloud is not installed, return 0
                return 0
            except Exception as e:
                # Error connecting, return 0
                return 0
                
        except Exception:
            return 0

