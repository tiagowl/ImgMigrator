"""QStash service for background task processing."""
import json
import httpx
from typing import Optional
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class QStashService:
    """Service for publishing tasks to QStash."""
    
    def __init__(self):
        """Initialize QStash service."""
        if not settings.QSTASH_TOKEN:
            raise ValueError("QSTASH_TOKEN não está configurado")
        
        self.token = settings.QSTASH_TOKEN
        self.base_url = settings.QSTASH_URL
        self.webhook_url = None  # Será configurado com a URL base da aplicação
    
    def set_webhook_url(self, base_url: str):
        """Set the webhook URL for receiving tasks."""
        self.webhook_url = f"{base_url.rstrip('/')}/api/v1/webhooks/qstash"
    
    async def publish_migration_task(
        self,
        migration_id: int,
        user_id: int,
        delay_seconds: Optional[int] = None,
    ) -> dict:
        """
        Publish a migration task to QStash.
        
        Args:
            migration_id: Migration ID
            user_id: User ID
            delay_seconds: Optional delay in seconds before executing
            
        Returns:
            Response from QStash
        """
        if not self.webhook_url:
            raise ValueError("Webhook URL não configurado. Chame set_webhook_url() primeiro.")
        
        payload = {
            "migration_id": migration_id,
            "user_id": user_id,
        }
        
        # QStash API endpoint - formato: https://qstash.upstash.io/v2/publish/{destination}
        qstash_api_url = "https://qstash.upstash.io/v2/publish"
        
        # QStash precisa do destino codificado na URL
        import urllib.parse
        encoded_destination = urllib.parse.quote(self.webhook_url, safe='')
        url = f"{qstash_api_url}/{encoded_destination}"
        
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        
        # Adicionar delay se especificado
        if delay_seconds:
            headers["Upstash-Delay"] = str(delay_seconds)
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    url,
                    json=payload,
                    headers=headers,
                    timeout=30.0,
                )
                response.raise_for_status()
                
                result = response.json()
                message_id = result.get("messageId") or result.get("id")
                logger.info(f"Task published to QStash for migration {migration_id}: {message_id}")
                return result
                
            except httpx.HTTPError as e:
                error_detail = str(e)
                if hasattr(e, 'response') and e.response is not None:
                    try:
                        error_detail = e.response.json()
                    except:
                        error_detail = e.response.text
                logger.error(f"Error publishing task to QStash: {error_detail}")
                raise ValueError(f"Erro ao publicar tarefa no QStash: {error_detail}")
    
    def verify_signature(self, body: bytes, signature: str, signing_key: Optional[str] = None) -> bool:
        """
        Verify QStash message signature.
        
        Args:
            body: Request body
            signature: Signature from Upstash-Signature header
            signing_key: Signing key (uses QSTASH_CURRENT_SIGNING_KEY if not provided)
            
        Returns:
            True if signature is valid
        """
        import hmac
        import hashlib
        
        if not signing_key:
            signing_key = settings.QSTASH_CURRENT_SIGNING_KEY or settings.QSTASH_NEXT_SIGNING_KEY
        
        if not signing_key:
            logger.warning("No signing key configured, skipping signature verification")
            return True  # Em desenvolvimento, pode pular verificação
        
        try:
            # QStash usa HMAC SHA256
            expected_signature = hmac.new(
                signing_key.encode(),
                body,
                hashlib.sha256
            ).hexdigest()
            
            # Comparar assinaturas de forma segura
            return hmac.compare_digest(expected_signature, signature)
        except Exception as e:
            logger.error(f"Error verifying signature: {str(e)}")
            return False


# Singleton instance
_qstash_service: Optional[QStashService] = None


def get_qstash_service() -> QStashService:
    """Get QStash service instance."""
    global _qstash_service
    
    if _qstash_service is None:
        _qstash_service = QStashService()
    
    return _qstash_service

