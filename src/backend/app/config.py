"""Application configuration."""
import os
from typing import Optional, Union
from pydantic import field_validator

try:
    from pydantic_settings import BaseSettings
except ImportError:
    # Fallback para pydantic v1
    try:
        from pydantic import BaseSettings
    except ImportError:
        # Se ainda falhar, usar BaseModel
        from pydantic import BaseModel as BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # App
    APP_NAME: str = "Cloud Migrate API"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    
    # Database
    DATABASE_URL: str = "sqlite:///./cloud_migrate.db"
    
    # Security
    SECRET_KEY: str = "change-me-in-production"
    MASTER_ENCRYPTION_KEY: str = "change-me-in-production-32-bytes-key-here"
    
    # OAuth Google
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/api/v1/auth/oauth/google/callback"
    
    # Redis/Celery
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    
    # CORS - aceita string separada por vírgulas ou lista
    ALLOWED_ORIGINS: Union[str, list[str]] = "http://localhost:3000,http://localhost:3001"
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    
    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_allowed_origins(cls, v: Union[str, list]) -> list[str]:
        """Parse ALLOWED_ORIGINS from string or list."""
        if isinstance(v, str):
            # Remove espaços e divide por vírgula
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        elif isinstance(v, list):
            return v
        return ["http://localhost:3000"]
    
    @field_validator("DEBUG", mode="before")
    @classmethod
    def parse_debug(cls, v: Union[str, bool]) -> bool:
        """Parse DEBUG from string or bool."""
        if isinstance(v, str):
            return v.lower() in ("true", "1", "yes", "on")
        return bool(v)
    
    class Config:
        """Pydantic config."""
        env_file = ".env"
        case_sensitive = True


settings = Settings()

