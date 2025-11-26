"""Main FastAPI application."""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import init_db
from app.api.routes import auth, credentials, migrations, webhooks

logger = logging.getLogger(__name__)

# Initialize database
init_db()

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="API for migrating photos from iCloud to Google Drive",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
app.include_router(credentials.router, prefix=settings.API_V1_PREFIX)
app.include_router(migrations.router, prefix=settings.API_V1_PREFIX)
app.include_router(webhooks.router, prefix=settings.API_V1_PREFIX)

# Configure QStash webhook URL if QStash is enabled
if settings.QSTASH_TOKEN:
    try:
        from app.services.qstash_service import get_qstash_service
        # Determine base URL from environment or use default
        import os
        base_url = os.getenv("BASE_URL") or os.getenv("RENDER_EXTERNAL_URL") or "http://localhost:8000"
        qstash_service = get_qstash_service()
        qstash_service.set_webhook_url(base_url)
        logger.info(f"QStash webhook URL configured: {qstash_service.webhook_url}")
    except Exception as e:
        logger.warning(f"Failed to configure QStash: {str(e)}")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Cloud Migrate API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


# For Vercel serverless
app = app






