"""Authentication service."""
from typing import Optional
from authlib.integrations.httpx_client import AsyncOAuth2Client
from app.config import settings


class AuthService:
    """Service for OAuth authentication."""
    
    @staticmethod
    def get_google_oauth_client() -> AsyncOAuth2Client:
        """Get Google OAuth client."""
        return AsyncOAuth2Client(
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            redirect_uri=settings.GOOGLE_REDIRECT_URI,
        )
    
    @staticmethod
    def get_google_authorization_url() -> tuple[str, str]:
        """
        Get Google OAuth authorization URL.
        
        Returns:
            Tuple of (authorization_url, state)
        
        Raises:
            ValueError: If OAuth credentials are not configured
        """
        import secrets
        
        # Validar configuração
        if not settings.GOOGLE_CLIENT_ID:
            raise ValueError("GOOGLE_CLIENT_ID não está configurado")
        if not settings.GOOGLE_CLIENT_SECRET:
            raise ValueError("GOOGLE_CLIENT_SECRET não está configurado")
        if not settings.GOOGLE_REDIRECT_URI:
            raise ValueError("GOOGLE_REDIRECT_URI não está configurado")
        
        client = AuthService.get_google_oauth_client()
        state = secrets.token_urlsafe(32)
        
        try:
            # Request full Drive access for migration and user email
            # drive: Full access to Drive (needed to upload photos)
            # userinfo.email: Access to user's email address
            auth_url, _ = client.create_authorization_url(
                "https://accounts.google.com/o/oauth2/v2/auth",
                scope="https://www.googleapis.com/auth/drive https://www.googleapis.com/auth/userinfo.email",
                state=state,
                access_type="offline",  # Request refresh token
                prompt="consent",  # Force consent to get refresh token
            )
        except Exception as e:
            raise ValueError(f"Erro ao criar URL de autorização: {str(e)}. Verifique se GOOGLE_REDIRECT_URI está correto: {settings.GOOGLE_REDIRECT_URI}")
        
        return auth_url, state
    
    @staticmethod
    async def exchange_google_code(code: str) -> dict:
        """
        Exchange authorization code for access token.
        
        Args:
            code: Authorization code from Google
            
        Returns:
            Token response dictionary with:
            - access_token: OAuth access token
            - refresh_token: OAuth refresh token (if provided)
            - expires_in: Token expiration time in seconds
            - token_type: Usually "Bearer"
        """
        if not settings.GOOGLE_CLIENT_ID or not settings.GOOGLE_CLIENT_SECRET:
            raise ValueError("OAuth credentials não configuradas")
        
        if not settings.GOOGLE_REDIRECT_URI:
            raise ValueError("GOOGLE_REDIRECT_URI não configurado")
        
        client = AuthService.get_google_oauth_client()
        
        try:
            token_response = await client.fetch_token(
                "https://oauth2.googleapis.com/token",
                code=code,
            )
            
            # Validar resposta
            if "access_token" not in token_response:
                error_detail = token_response.get("error_description", token_response.get("error", "Unknown error"))
                raise ValueError(f"Resposta do Google não contém access_token: {error_detail}")
            
            return token_response
        except ValueError:
            # Re-raise ValueError as-is
            raise
        except Exception as e:
            error_msg = str(e)
            # Try to extract more details from the error
            if hasattr(e, 'response') and hasattr(e.response, 'json'):
                try:
                    error_data = e.response.json()
                    error_msg = error_data.get('error_description', error_data.get('error', error_msg))
                except:
                    pass
            raise ValueError(f"Erro ao trocar código por token: {error_msg}")
    
    @staticmethod
    async def refresh_google_token(refresh_token: str) -> dict:
        """
        Refresh Google OAuth access token.
        
        Args:
            refresh_token: OAuth refresh token
            
        Returns:
            New token response dictionary
        """
        if not settings.GOOGLE_CLIENT_ID or not settings.GOOGLE_CLIENT_SECRET:
            raise ValueError("OAuth credentials não configuradas")
        
        client = AuthService.get_google_oauth_client()
        
        try:
            token_response = await client.refresh_token(
                "https://oauth2.googleapis.com/token",
                refresh_token=refresh_token,
            )
            
            return token_response
        except Exception as e:
            raise ValueError(f"Erro ao renovar token: {str(e)}")
    
    @staticmethod
    async def get_user_info(access_token: str) -> dict:
        """
        Get user information from Google using access token.
        
        Args:
            access_token: OAuth access token
            
        Returns:
            User information dictionary
        """
        import httpx
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            response.raise_for_status()
            return response.json()

