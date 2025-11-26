"""Authentication routes."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.config import settings
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import AuthService
from app.services.credential_service import CredentialService
from app.repositories.user_repository import UserRepository

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    """Register a new user."""
    repository = UserRepository(db)
    
    # Check if user already exists
    existing = repository.find_by_email(user_data.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )
    
    # Create user
    from app.models.user import User
    user = User(email=user_data.email)
    user = repository.create(user)
    
    return user


@router.get("/oauth/google/init")
async def init_google_oauth(
    user_id: int = Query(1, description="User ID (simplified for MVP)"),
):
    """
    Initialize Google OAuth flow.
    
    Returns the authorization URL that the user should be redirected to.
    The redirect URI must be configured in Google Cloud Console.
    
    After user authorizes, they will be redirected to the callback URL
    which will save the OAuth tokens to the database.
    """
    try:
        auth_url, state = AuthService.get_google_authorization_url()
        
        # Store state with user_id for validation (simplified - would use session/redis)
        # For MVP, we'll include user_id in the state or use it in callback
        
        return {
            "auth_url": auth_url,
            "state": state,
            "user_id": user_id,  # Include in response for frontend
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Configuração OAuth inválida: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to initialize OAuth: {str(e)}",
        )


@router.get("/oauth/google/callback")
async def google_oauth_callback(
    code: str = Query(None, description="Authorization code from Google"),
    state: str = Query(None, description="OAuth state"),
    error: str = Query(None, description="Error from Google OAuth"),
    error_description: str = Query(None, description="Error description from Google"),
    user_id: int = Query(1, description="User ID (simplified for MVP)"),
    db: Session = Depends(get_db),
):
    """
    Handle Google OAuth callback.
    
    This endpoint:
    1. Exchanges the authorization code for tokens
    2. Gets user information from Google
    3. Creates/updates user if needed
    4. Saves encrypted OAuth tokens to credentials
    5. Redirects to frontend with success/error status
    
    Args:
        code: Authorization code from Google
        state: OAuth state (for validation)
        error: Error code from Google (if authorization failed)
        error_description: Error description from Google
        user_id: User ID (simplified for MVP)
    """
    from fastapi.responses import RedirectResponse
    from urllib.parse import quote
    import logging
    
    logger = logging.getLogger(__name__)
    
    # Get frontend URL from settings or use default
    frontend_url = (
        settings.ALLOWED_ORIGINS[0] 
        if isinstance(settings.ALLOWED_ORIGINS, list) and len(settings.ALLOWED_ORIGINS) > 0
        else (settings.ALLOWED_ORIGINS if isinstance(settings.ALLOWED_ORIGINS, str) else "http://localhost:3000")
    )
    
    # Check if Google returned an error
    if error:
        error_msg = error_description or error
        logger.error(f"Google OAuth error: {error} - {error_msg}")
        error_message = quote(str(error_msg))
        redirect_url = f"{frontend_url}?oauth=error&service=google_drive&message={error_message}"
        return RedirectResponse(url=redirect_url, status_code=302)
    
    # Check if code is missing
    if not code:
        logger.error("OAuth callback called without authorization code")
        error_message = quote("Código de autorização não fornecido pelo Google")
        redirect_url = f"{frontend_url}?oauth=error&service=google_drive&message={error_message}"
        return RedirectResponse(url=redirect_url, status_code=302)
    
    try:
        # Exchange code for tokens
        logger.info("Exchanging authorization code for tokens")
        token_response = await AuthService.exchange_google_code(code)
        
        access_token = token_response.get("access_token")
        refresh_token = token_response.get("refresh_token")
        expires_in = token_response.get("expires_in", 3600)  # Default 1 hour
        
        if not access_token:
            logger.error("Token response does not contain access_token")
            error_message = quote("Resposta do Google não contém access_token")
            redirect_url = f"{frontend_url}?oauth=error&service=google_drive&message={error_message}"
            return RedirectResponse(url=redirect_url, status_code=302)
        
        logger.info("Successfully obtained access token")
        
        # Get user info from Google
        user_email = None
        try:
            user_info = await AuthService.get_user_info(access_token)
            user_email = user_info.get("email", "")
            if not user_email:
                logger.warning("Google user info does not contain email")
            else:
                logger.info(f"Retrieved user info: {user_email}")
        except Exception as e:
            logger.warning(f"Could not get user info: {str(e)}. Will create user with temporary email")
            # Se não conseguir obter email, vamos criar um email temporário
            user_email = None
        
        # Find or create user
        repository = UserRepository(db)
        user = None
        
        if user_email:
            # Try to find user by email
            user = repository.find_by_email(user_email)
            if not user:
                # Create new user with email from Google
                from app.models.user import User
                user = User(email=user_email)
                user = repository.create(user)
                logger.info(f"Created new user with email: {user_email}")
            else:
                logger.info(f"Found existing user: {user_email}")
        else:
            # If we couldn't get email, try to use provided user_id first
            user = repository.find_by_id(user_id)
            
            if not user:
                # Create a new user with a temporary email based on timestamp
                # This ensures we always have a user to save credentials
                from app.models.user import User
                import time
                temp_email = f"google_user_{int(time.time())}@temp.cloudmigrate.local"
                user = User(email=temp_email)
                user = repository.create(user)
                logger.info(f"Created new user with temporary email: {temp_email}")
            else:
                logger.info(f"Using existing user with ID: {user_id}")
        
        # Save OAuth tokens to credentials
        logger.info(f"Saving OAuth credentials for user {user.id}")
        credential_service = CredentialService(db)
        credential = credential_service.create_google_oauth_credential(
            user_id=user.id,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=expires_in,
        )
        
        logger.info(f"Successfully saved credentials. Redirecting to frontend")
        
        # Redirect to frontend with success parameter
        redirect_url = f"{frontend_url}?oauth=success&service=google_drive"
        return RedirectResponse(url=redirect_url, status_code=302)
        
    except ValueError as e:
        logger.error(f"ValueError in OAuth callback: {str(e)}")
        error_message = quote(str(e))
        redirect_url = f"{frontend_url}?oauth=error&service=google_drive&message={error_message}"
        return RedirectResponse(url=redirect_url, status_code=302)
    except HTTPException as e:
        logger.error(f"HTTPException in OAuth callback: {str(e.detail)}")
        error_message = quote(str(e.detail))
        redirect_url = f"{frontend_url}?oauth=error&service=google_drive&message={error_message}"
        return RedirectResponse(url=redirect_url, status_code=302)
    except Exception as e:
        logger.exception(f"Unexpected error in OAuth callback: {str(e)}")
        error_message = quote(f"Erro inesperado: {str(e)}")
        redirect_url = f"{frontend_url}?oauth=error&service=google_drive&message={error_message}"
        return RedirectResponse(url=redirect_url, status_code=302)

